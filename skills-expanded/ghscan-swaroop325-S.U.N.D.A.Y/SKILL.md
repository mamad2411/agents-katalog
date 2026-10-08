# SUNDAY Phase 3 — AppleScript bridge + Calendar skill + tool-calling

**Goal:** Introduce the skill/tool-calling layer. Agents can now call macOS-backed tools to read real data. Ship the AppleScript bridge, a skill registry, a tool-calling loop for the Ollama agent, and the first skill (`calendar.list_events`).

**Scope:** Tool-calling is implemented ONLY for the Ollama agent in Phase 3. Cloud providers in Phase 4.

## Tasks (execute in order, one commit each)

### Task P3-1: AppleScript bridge (`backend/applescript/bridge.py`)

Create `backend/applescript/__init__.py` (empty) and `backend/applescript/bridge.py`. The module must expose:

- `class AppleScriptError(Exception)` with fields `script_kind: str`, `returncode: int`, `stderr: str`
- `async def run_osascript(script: str, timeout: float = 10.0) -> str` — runs `osascript -e <script>` and returns stdout
- `async def run_jxa(script: str, timeout: float = 10.0) -> str` — runs `osascript -l JavaScript -e <script>` and returns stdout
- `async def run_jxa_json(script: str, timeout: float = 10.0) -> object` — runs JXA expected to print a JSON string, parses and returns

Use `asyncio.create_subprocess_exec` (NOT `subprocess.run` — we need async). Pipe stdout/stderr. Await with `asyncio.wait_for(proc.communicate(), timeout=timeout)`. On timeout, `proc.kill()` then raise AppleScriptError with returncode -1. On nonzero returncode, raise AppleScriptError with the stderr decoded.

Tests `tests/test_applescript_bridge.py` using real osascript:
- `test_osascript_hello_world`: `run_osascript('return "hello"')` returns `"hello\n"` or similar
- `test_osascript_error_propagates`: `run_osascript('error "nope"')` raises `AppleScriptError`
- `test_jxa_basic`: `run_jxa('(() => "world")()')` returns `"world\n"`
- `test_jxa_json_returns_parsed_object`: script `(() => JSON.stringify({a:1,b:[2,3]}))()` returns dict `{"a":1,"b":[2,3]}`
- `test_jxa_json_rejects_malformed`: script returning non-JSON raises `AppleScriptError`

All tests are `@pytest.mark.asyncio`.

Commit: `feat(applescript): async osascript + JXA bridge`

### Task P3-2: Skill protocol + registry

Create `backend/skills/__init__.py` (empty), `backend/skills/base.py`, and `backend/skills/registry.py`.

`backend/skills/base.py`:
```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    parameters: dict  # JSON Schema

    def to_openai_tool(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }


class Skill(Protocol):
    spec: ToolSpec

    async def invoke(self, **kwargs: Any) -> dict: ...
```

`backend/skills/registry.py`:
```python
from __future__ import annotations

import logging
from typing import Any

from backend.skills.base import Skill, ToolSpec

_log = logging.getLogger(__name__)


class SkillRegistry:
    def __init__(self) -> None:
        self._skills: dict[str, Skill] = {}

    def register(self, skill: Skill) -> None:
        name = skill.spec.name
        if name in self._skills:
            raise ValueError(f"skill {name!r} already registered")
        self._skills[name] = skill

    def names(self) -> list[str]:
        return sorted(self._skills.keys())

    def tool_specs(self) -> list[ToolSpec]:
        return [s.spec for s in self._skills.values()]

    def as_openai_tools(self) -> list[dict]:
        return [s.spec.to_openai_tool() for s in self._skills.values()]

    async def invoke(self, name: str, arguments: dict[str, Any]) -> dict:
        if name not in self._skills:
            return {"error": f"unknown skill: {name}"}
        skill = self._skills[name]
        try:
            return await skill.invoke(**arguments)
        except TypeError as e:
            return {"error": f"bad arguments for {name}: {e}"}
        except Exception as e:
            _log.exception("skill %s crashed", name)
            return {"error": f"{name} failed: {e}"}
```

Tests `tests/test_skill_registry.py` with an in-file `EchoSkill` and `CrashSkill` — verify register, invoke, unknown-skill error, bad-args error, crash-captured error, duplicate-register raises, openai_tools schema shape.

Commit: `feat(skills): skill protocol + registry with OpenAI tool schema`

### Task P3-3: Calendar skill

Create `backend/skills/calendar.py`. Class `CalendarListEventsSkill` with `spec: ToolSpec` (name `calendar_list_events`, JSON-Schema params `start` + `end` ISO datetimes, both required) and `async invoke(start, end)`.

The skill builds a JXA script that:
1. Parses `start` and `end` as JS Dates
2. Iterates `Application('Calendar').calendars()`
3. For each calendar, uses `cal.events.whose({_and:[{startDate:{_greaterThanEquals:start}},{startDate:{_lessThan:end}}]})()` to filter
4. Collects each matching event's `calendar`, `summary`, `location`, `start` (ISO), `end` (ISO), `all_day` flag
5. Wraps in try/catch per event so one malformed event doesn't fail the whole batch
6. Sorts by start
7. Returns `JSON.stringify(results)` so `run_jxa_json` can parse it

The Python side then calls `run_jxa_json(script, timeout=15.0)` and wraps the result as `{"events": [...], "count": N}`, or `{"error": "..."}` on failure. Reject non-list results with a clear error.

Also export a helper `def today_window() -> tuple[str, str]` returning `(start_iso, end_iso)` for today (midnight to next midnight, local time) for CLI testing convenience.

Tests `tests/test_calendar_skill.py`:
- `test_calendar_skill_parses_bridge_result` — mocks `run_jxa_json` via `unittest.mock.patch`, returns a fake list with one event, asserts the skill wraps it as `{"events":[...], "count":1}`
- `test_calendar_skill_handles_bridge_error` — mock raises RuntimeError, assert result has `error`
- `test_calendar_skill_rejects_non_list_result` — mock returns a string, assert error
- `test_today_window_is_midnight_pair` — synchronous, asserts both ISO strings are midnight

Do NOT write a live Calendar.app integration test — the unit tests mock the bridge.

Commit: `feat(skills): calendar.list_events via JXA to Calendar.app`

### Task P3-4: Tool-calling loop in Ollama agent

Extend `backend/agent/ollama_agent.py` to accept an optional `registry: Optional[SkillRegistry] = None` parameter. Behavior change:

- **No registry:** Current streaming behavior, unchanged.
- **With registry:** Use `registry.as_openai_tools()` as `payload["tools"]` and implement a tool-calling loop:
  - Up to `MAX_TOOL_ROUNDS = 5` iterations
  - Each iteration streams the response. Any `message.content` chunks get yielded to the caller AND accumulated in `assistant_content`. Any `message.tool_calls` get collected into `tool_calls` list. When `done=true`, break the inner loop.
  - After stream ends, if `tool_calls` is empty, return (final answer already streamed).
  - Otherwise: append an assistant message (with `content` and `tool_calls`), then for each call invoke `registry.invoke(name, args)` (args may come as a JSON string — parse), append a `{"role":"tool","content":json.dumps(result)}` message, loop back.
  - If the loop exhausts, yield `"  (I've called a lot of tools, stopping here.)"`.

Use the direct httpx client path (not the shared `_http_stream.py` helper) because the tool-call loop is more stateful than that helper expresses.

Tests `tests/test_ollama_tool_calling.py`:
- `FakeStream` / `FakeClient` fixture classes (inline) that return queued stream bodies
- `WeatherSkill` — stub skill with a simple `get_weather(city)` that returns fake data
- `test_ollama_tool_calling_single_round`:
  - Response 1 (tool call): `{"message":{"role":"assistant","content":"","tool_calls":[{"function":{"name":"get_weather","arguments":{"city":"Paris"}}}]},"done":true}`
  - Response 2 (final text): `{"message":{"content":"It is sunny "},"done":false}\n{"message":{"content":"in Paris."},"done":true}`
  - Assert the yielded stream concatenates to a string containing "sunny" and "Paris"
  - Assert the second HTTP call's `messages` included a `role=tool` message with Paris data
- `test_ollama_no_tools_path_unchanged`:
  - Agent without a registry — verify `tools` is NOT in the payload and the stream concatenates correctly

Use `monkeypatch.setattr(mod.httpx, "AsyncClient", fake)` to inject fakes.

Commit: `feat(agent): Ollama tool-calling loop with skill registry`

### Task P3-5: Wire registry into app.py

Update `backend/agent/factory.py` to accept `registry: Optional[SkillRegistry] = None` and pass it to `OllamaAgent(...)`. Cloud agents ignore it in Phase 3.

Update `backend/app.py:main()`:
```python
from backend.skills.registry import SkillRegistry
from backend.skills.calendar import CalendarListEventsSkill

# ...existing...
registry = SkillRegistry()
registry.register(CalendarListEventsSkill())
agent = build_agent(config.agent, registry=registry)
```

Update `tests/test_agent_factory.py` if it constructs agents directly — pass a fresh `SkillRegistry()` for the Ollama case.

Verify the whole suite still passes.

Commit: `feat(app): register calendar skill and pass to agent factory`

### Task P3-6: Suite run + optional live Calendar.app check

```bash
uv run pytest -q
```

Expected: roughly 65+ tests passing (55 before + ~10 new).

OPTIONAL live check — if time permits and Calendar.app has events:
```bash
uv run python -c "
import asyncio
from backend.skills.calendar import CalendarListEventsSkill, today_window
async def main():
    skill = CalendarListEventsSkill()
    s, e = today_window()
    print(await skill.invoke(start=s, end=e))
asyncio.run(main())
"
```

If this fails with an AppleEvents permission error, it means macOS hasn't granted Calendar automation access to the terminal yet — that's a one-time user-side grant via System Settings, not a code bug. Note in report.

Commit: `test: phase 3 final verification` (or skip if nothing new to commit)
