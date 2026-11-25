# L159 — Load Recent Memories into System Prompt

**Status:** Spec only
**Branch:** `feature/l159-load-memories-into-system-prompt` (from `feature/workflow-builder`)
**Depends on:** L158 (auto-save memory at session end)

## Intent

Even with auto-saved session summaries, the model starts every new session with a blank slate. The user has to re-explain context repeatedly ("I already told you about the LinkedIn login tool"). This loop injects relevant past memories into the system prompt at session start so the model has continuity.

## Review carry-forward

- *(none)*

## Scope

### §1 — Memory epoch prefix builder

Add `src/hestia/context/memory_epoch.py`:

```python
"""Build a memory-epoch prefix from recent memories for the system prompt."""

import logging
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hestia.memory import MemoryStore

logger = logging.getLogger(__name__)

_MAX_MEMORIES = 5
_MAX_AGE_DAYS = 30
_MAX_CHARS = 1500


class MemoryEpochBuilder:
    """Fetches recent memories and formats them as a system-prompt prefix."""

    def __init__(self, memory_store: "MemoryStore") -> None:
        self._store = memory_store

    async def build_prefix(
        self,
        platform: str,
        platform_user: str,
        query: str = "",
    ) -> str:
        """Return a formatted memory block or empty string."""
        try:
            since = datetime.now(timezone.utc) - timedelta(days=_MAX_AGE_DAYS)
            memories = await self._store.search_recent(
                platform=platform,
                platform_user=platform_user,
                since=since,
                limit=_MAX_MEMORIES,
            )
        except Exception as exc:
            logger.warning("Memory search failed: %s", exc)
            return ""

        if not memories:
            return ""

        lines = ["## Previous context"]
        for m in memories:
            lines.append(f"- [{m.tags}] {m.content}")

        text = "\n".join(lines)
        if len(text) > _MAX_CHARS:
            text = text[:_MAX_CHARS] + "\n... (truncated)"

        return text
```

**Requires:** Add `search_recent` to `MemoryStore` if it doesn't exist. If `MemoryStore` only has `search(query)` and `list_recent(limit)`, use those and filter by `platform`/`platform_user` in Python.

**Commit:** `feat(context): MemoryEpochBuilder for system-prompt prefix injection`

### §2 — Inject memory epoch into context build

Modify `src/hestia/context/builder.py` `ContextBuilder.build()`:

1. Accept an optional `memory_epoch_prefix: str` parameter.
2. If provided and non-empty, prepend it to the system prompt (before the main system prompt, after any identity prefix).

Modify `src/hestia/orchestrator/assembly.py` `TurnAssembly.prepare()`:

1. Before calling `self._builder.build()`, if `AppContext` has a `memory_epoch_builder`, call `build_prefix(platform, platform_user)`.
2. Pass the result as `memory_epoch_prefix` to `ContextBuilder.build()`.

```python
memory_epoch_prefix = ""
if hasattr(app_ctx, "memory_epoch_builder") and app_ctx.memory_epoch_builder:
    memory_epoch_prefix = await app_ctx.memory_epoch_builder.build_prefix(
        session.platform, session.platform_user
    )

ctx.build_result = await self._builder.build(
    session=session,
    history=history,
    system_prompt=effective_system_prompt,
    tools=ctx.tools,
    new_user_message=ctx.user_message,
    memory_epoch_prefix=memory_epoch_prefix,
)
```

**Commit:** `feat(orchestrator): inject memory epoch prefix at session start`

### §3 — Wire into app context

In `src/hestia/app.py`:
1. Add a lazy `memory_epoch_builder` property that creates `MemoryEpochBuilder(self.memory_store)`.
2. Pass it to the `Orchestrator` via `TurnAssembly`.

**Commit:** `feat(app): wire MemoryEpochBuilder into AppContext`

### §4 — Tests

In `tests/unit/context/test_memory_epoch.py`:
1. Test `build_prefix` returns empty string when no memories exist.
2. Test `build_prefix` returns formatted block with memories.
3. Test truncation when memories exceed `_MAX_CHARS`.
4. Test graceful failure when `MemoryStore` raises an exception.

In `tests/unit/orchestrator/test_assembly.py` (or existing test):
1. Assert that `ContextBuilder.build()` receives `memory_epoch_prefix` when a builder is configured.
2. Assert no prefix is passed when builder is None.

Run quality gates.

**Commit:** `test(context): memory epoch builder and injection coverage`

## Acceptance

- `pytest tests/unit/ tests/integration/ -q` green
- `mypy src/hestia` reports 0 errors
- Starting a new session after L158 has saved memories causes the system prompt to include a `## Previous context` block

## Handoff

- Write `docs/handoffs/L159-load-memories-into-system-prompt-handoff.md`
- Update `docs/development-process/kimi-loop-log.md`
