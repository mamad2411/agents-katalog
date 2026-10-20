---
description: Keep .env.example in sync when adding or changing environment variables (operator vs advanced tiers).
globs: src/**/*.py,.env.example
---

# `.env.example` maintenance (mandatory)

When you **add, rename, or change the default** of any environment variable read from `os.environ` / `load_plumber_lint_config_from_environ` / UI `_ENV_KEY_MAP`, update [`.env.example`](.env.example) in the **same task** — without waiting for the user to ask.

## When to update

| Trigger | Action |
|---------|--------|
| New `os.environ.get("MATRYCA_…")`, `_env_int`, `_map_bool(env, …)`, or `_*_ENV = "…"` in `src/` | Add key to `.env.example` in the correct tier |
| Changed Python default (e.g. `DEFAULT_*`, `_map_*` fallback, dataclass default) | Update **Default (code)** comment; adjust **Template** only if the safe install profile should change |
| New Settings field → `_ENV_KEY_MAP` in `ui_server.py` | Document under **Operator essentials** (UI-exposed keys) |
| Variable becomes **deprecated** or **reserved** (not read) | Move to deprecated block; add to `tests/test_env_example_coverage.py` `_ALLOWLIST_UNREAD` if still listed |

Do **not** edit the operator's local `.env` unless they explicitly ask.

## File structure (two tiers)

```text
[Header + legend]
=== OPERATOR ESSENTIALS ===     ← paths, LLM, thermal, map-reduce, low-priority, basic UI token
=== ADVANCED / HIGH IMPACT ===  ← explicit WARNING banner; mutating lint, compression, MCP, flock, limits, edge
```

- **Operator essentials:** settings mirrored in the Sovereign UI or needed on day one (`LOGSEQ_GRAPH_PATH`, LLM URL/model, thermal, map-reduce, `MATRYCA_PLUMBER_LOW_PRIORITY_MODE`, `MATRYCA_UI_TOKEN` / LAN basics).
- **Advanced / high impact:** mutating graph behavior, security surface expansion, diagnostics that leak data, or tuning that can corrupt prompts/cache — prefix section with a clear **do not change unless you understand the risk** banner.

## Per-key comment block (required)

```bash
# <What it does — one sentence>. <src/module.py>
# Default (code): <value when unset/empty in Python>
# Template: <value on the line below for new installs; omit line if same as Default (code)>
# Range / notes: <clamps, security, when to enable>  (optional)
KEY=value
```

- **Default (code)** must match the actual fallback in code (`plumber_config.py`, module `_DEFAULT_*`, or `_map_bool(..., True)`).
- **Template** is the safe 16GB / test-vault profile (often `false` for mutating lint). If Template differs from Default (code), state both.
- Cite the resolving function or file path (e.g. `src/agent/llm_client.py`).

## LLM key precedence (document in header)

- `LLM_BASE_URL` / `LLM_MODEL_NAME` override `MATRYCA_LM_*` when non-empty; Settings UI persists `LLM_*`.

## Verification (same task)

```bash
uv run pytest tests/test_env_example_coverage.py -q --no-cov
```

Fix allowlist only for **reserved** (`MATRYCA_LLM_PROMPT_CACHE_MODE`) or **deprecated** (`MATRYCA_LM_INSTRUCTOR_*`) keys not read by runtime.

## Changelog

If the env change is user-visible, also add a bullet under `CHANGELOG.md` `## [Unreleased]` per [`.cursor/rules/06-auto-changelog.mdc`](06-auto-changelog.mdc).
