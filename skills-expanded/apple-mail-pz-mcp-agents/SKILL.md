# Apple Mail PingZero MCP Server

An MCP server bridging AI agents and Apple Mail via AppleScript on macOS.

**Stack:** Python 3.10+, FastMCP 4 / MCP SDK 2, AppleScript (via `osascript`)
**Version:** v0.12.0 | **Tests:** 1812 unit / 44 e2e / 76 integration | **Coverage:** 90%

This file is the canonical agent guide. Codex reads it directly; Claude Code
reaches it via [`.claude/CLAUDE.md`](.claude/CLAUDE.md). Edit it here.

**Origins.** This project continues `apple-mail-fast-mcp` by Morgan Jeffries
(MIT). The architecture, security model, and test discipline are inherited from
that project — see [Credits and origins](README.md#credits-and-origins). It
diverges on one axis: the tool surface is tuned for **LLM efficiency** (fewer
round-trips, tighter payloads, predictable behavior across MCP hosts) rather
than for human API aesthetics. When you add or change a tool, that is the
tiebreaker.

The distribution, console script, and plugin are named `apple-mail-pz-mcp`; the
Python import package remains `apple_mail_fast_mcp`, and the Keychain service
prefix remains `apple-mail-fast-mcp.imap.` — both name persistent state and are
not renamed casually. See `keychain.py`.

## Commands

```bash
make install-tool          # Install the CLI from this checkout, pinned to uv.lock
make test                  # Unit tests (~1s, mocked AppleScript)
make test-integration      # Real Mail.app tests (requires test account)
make test-e2e              # End-to-end MCP tool tests
make lint                  # Ruff linting
make format                # Ruff formatting
make typecheck             # Mypy strict mode
make check-all             # All checks (lint, typecheck, test, complexity, version-sync, parity)
make coverage              # Coverage report
./scripts/check_complexity.sh          # Cyclomatic complexity check
./scripts/check_client_server_parity.sh  # Verify all connector methods are exposed
./scripts/check_version_sync.sh        # Version consistency across files
```

**Running the server:** `uv run python -m apple_mail_fast_mcp.server` (add `--read-only` to match the shipped default), or via an MCP client config.

## API Surface (27 MCP tools)

**Core:** list_mailboxes, search_messages, get_messages, update_message
**Drafts lifecycle (#134):** create_draft, update_draft, delete_draft
**Mailbox CRUD:** create_mailbox, update_mailbox (rename + move via IMAP), delete_mailbox (IMAP-only)
**Attachments & Management:** save_attachments, get_attachment_content (#250, inline read), delete_messages
**Discovery & Rules:** list_accounts, list_rules, get_thread, create_rule, update_rule, delete_rule
**Diagnostics:** diagnose_mail_access, get_server_version (version/commit/build date)
**Analytics (#378):** get_statistics (inbox stats: volume / read-ratio / top senders; compose-only)
**Templates:** list_templates, get_template, save_template, delete_template, render_template

Split 13 read-only / 14 mutating. `--read-only` (#217) skips registration of the
mutating 14 — see `_tool()` in `server.py`. The tool count is asserted by
`./scripts/check_readme_claims.sh`; update README, `mcpb/manifest.json`, and this
file together when it changes.

## MCP Client Compatibility

The shipped artifacts register all 27 tools. Read-only mode is opt-in, via
`--read-only` or `APPLE_MAIL_MCP_READ_ONLY=1` (the `.mcpb` bundle exposes it as
a boolean `user_config` that lands in the env). Writes are a first-class mode;
do not narrow the default surface to route around a host limitation.

| Behavior | Claude Code | Claude Desktop / Cowork | Codex CLI |
|---|---|---|---|
| MCP elicitation | Yes | **No** (Cowork: `anthropics/claude-ai-mcp#153`) | Yes, ≥ ~v0.119 |
| Stringifies array/dict tool args | No | **Yes** (`anthropics/claude-code#26094`) | **Yes**, via schema flattening (`openai/codex#15164`) |
| Per-tool approval | Yes | Yes (`toolPolicy`) | Yes (`approval_mode`) |
| Startup timeout | generous | generous | **10s default** (`startup_timeout_sec`) |

Two consequences drive real code:

- **Every destructive tool gates on `_elicit_confirmation`, which fails closed
  (#226).** On a host without elicitation the gated tools *can never succeed* —
  they return `error_type: "confirmation_required"` on every call. That is a
  host gap, not a reason to ship fewer tools; users who want them hidden pass
  `--read-only`. Do not "fix" this by letting the gate pass silently; that was
  the pre-#226 bypass. A confirm-token second call is the design worth exploring
  if writes must work on elicitation-less hosts.
- **Deletes are staged, so they need no gate.** `delete_messages` /
  `delete_mailbox` move their target under the account's `To Delete` mailbox
  (`APPLE_MAIL_MCP_DELETE_STAGING`; `off` disables) for the owner to delete.
  Nothing is destroyed, so no confirmation — which is what makes deletes work
  on elicitation-less hosts. Only a target already inside the staging mailbox
  takes the real, gated delete. Keep it that way: staging must never destroy.
- **Confirmation speaks both protocol eras.** On the 2025-11-25 handshake
  (what Claude Code and Desktop negotiate today) `_elicit_confirmation` sends
  a server-initiated elicitation. MCP 2026-07-28 removed that back-channel, so
  there it returns an `InputRequiredResult` and the client retries the call
  with the answer (`_confirm_by_input_request`). The sealed `request_state` is
  a digest of `(operation, params)`, so a "yes" only counts for the call that
  was shown. Gated tools therefore return `dict | InputRequiredResult`.
- **A host can take the prompt and never answer.** Claude Code in print mode
  (`-p`) logs the elicitation request and sends nothing back; unbounded, that
  hung `delete_mailbox` for 70 minutes. The wait is capped at 120s
  (`APPLE_MAIL_MCP_ELICITATION_TIMEOUT_S`) and returns
  `error_type: "confirmation_timeout"` — still fail-closed.
- **Hosts that stringify args** are handled by the `BeforeValidator` aliases at
  the top of `server.py`. Optional params must use the `Opt*` aliases
  (`OptStrList`, not `StrList | None`) — annotating the union is what lets a
  stringified `'null'` coerce to `None`. Spelling it `StrList | None` puts the
  validator inside the list branch, where the coerced `None` fails `list_type`.
  Scalars (`int`/`bool`/`float`) need no alias: Pydantic's lax mode already
  coerces `"50"` → `50`.

## Measuring LLM Efficiency

The thesis is worth nothing unless it is falsifiable. Three instruments:

| Instrument | Measures | Run it |
|---|---|---|
| `scripts/schema_budget.py` | Bytes of `tools/list` paid on **every** request | `make schema-budget` |
| `evals/agent_tool_usability/task_eval.py` | Round-trips + tokens per **completed** task | `make eval-tasks` |
| `evals/agent_tool_usability/run_eval.py` | Can a model pick the right tool at all? | `make eval-tools` |

`make check-all` ratchets the schema budget against `evals/schema_budget.json`.
Growth is not forbidden — a new tool costs bytes — but it must be re-recorded
with `--update` and justified, never allowed to drift.

Measure before optimizing the tool surface. A fatter `search_messages` costs
schema bytes on every request and saves round-trips on some; which wins is an
empirical question, and `task_eval.py` is the referee. Each task's `budget` is
the number of calls a competent agent needs. `batch-mark-read` is the
discriminating case: `update_message` takes a list of ids, and an agent that
ignores that still *succeeds* — just expensively. Tool descriptions are part of
this budget; keep only prose that changes what the model does.

## Core Principles

- **TDD always** — RED/GREEN/REFACTOR. Tests before implementation.
- **Backend + frontend together** — Every feature touches `mail_connector.py` AND `server.py`. Verify with `check_client_server_parity.sh`.
- **Sanitize everything twice** — All user input: `sanitize_input()` then `escape_applescript_string()` before AppleScript.
- **Structured responses** — Every tool returns `{"success": bool, ...}`. Errors include `error` and `error_type`.
- **Async tools never block the event loop** — FastMCP threads plain `def` tools but runs `async def` ones on the loop. Inside an async tool, every connector call (or sync helper that makes one) goes through `await _run_blocking(fn, ...)`. `test_server.py` ratchets this statically.
- **Security checklist per feature** — see [`docs/guides/SECURITY_CHECKLIST.md`](docs/guides/SECURITY_CHECKLIST.md) for the canonical reference (5 concerns: input sanitization, AppleScript escaping, path-traversal-safe name validation, rate limiting, audit logging). Don't duplicate guidance here; link out instead.
- **If you touched AppleScript, write integration tests** — Unit tests mock `_run_applescript()` and CANNOT catch AppleScript bugs.

## AppleScript Gotchas

**JSON output from AppleScript:** Scripts emit JSON via ASObjC + `NSJSONSerialization` (wrap with `_wrap_as_json_script`, parse with `parse_applescript_json`). Always quote the `name` record key as `|name|:` — the bare form is silently dropped during NSDictionary conversion. Coerce `missing value` to safe defaults (`{}` / `0`) before serializing. See applescript-mail skill for details.

**Gmail mode:** Gmail's label-based system doesn't support standard IMAP move. The `update_message` tool has a `gmail_mode` parameter that uses copy+delete instead of move.

**Message ID lookup:** Finding a message by ID requires searching across all accounts and mailboxes. AppleScript `whose` clauses are used for efficiency.

**String escaping:** Always use `escape_applescript_string()` for user text. Unescaped quotes/backslashes break AppleScript silently.

**Attachment paths:** Use POSIX file references (`POSIX file "/path/to/file"`) in AppleScript. Path objects converted via `.as_posix()`.

**Timeout:** Default 60s, configurable via `AppleMailConnector(timeout=N)`. Some operations on large mailboxes may need more.

**One osascript at a time:** `_run_applescript` holds a process-wide lock (`_APPLESCRIPT_LOCK`). Mail answers Apple Events serially anyway; overlapping calls only queued inside Mail, where the wait ate each caller's timeout. A call waits up to `timeout` for its turn, then gets a full `timeout` to run. A timeout does not undo work Mail already started, so the error tells the caller to re-check before retrying.

## Performance Constraints

- Each `osascript` subprocess call: 100-300ms overhead minimum
- Search: ~1-5s for typical mailboxes (uses `whose` clauses)
- Send: ~1-2s
- Read: <1s per message
- Bulk operations capped at 100 items

## User Data on Disk

- All persistent user data lives under `~/.apple_mail_mcp/`. Override the location with `APPLE_MAIL_MCP_HOME=/some/path` (the subdirectory layout is appended automatically).
- Current subdirs: `templates/` (one `<name>.md` file per email template, see `src/apple_mail_fast_mcp/templates.py`).
- Names that get used as filename stems must be regex-validated **before** building any path — see `_validate_name` in `templates.py` for the path-traversal-safe pattern. Don't `Path(user_input)` directly.
- Storage objects should resolve their root at use time, not import time, so env-var overrides and test-time monkeypatching are honored. Example: `_get_template_store()` in `server.py`.

## Testing Requirements

| Type | When Required | How |
|------|--------------|-----|
| Unit tests | Every code change | `make test` |
| Integration tests | New/modified AppleScript | `make test-integration` |
| E2E tests | New/modified tools | `make test-e2e` |

**Hard rule:** If you wrote or modified AppleScript in the connector, integration tests must cover it before merge.

**Integration test safety:** When running tests via `server.py` tools, set `MAIL_TEST_MODE=true` and `MAIL_TEST_ACCOUNT=<test account name>`. The safety gate blocks destructive operations on non-test accounts and blocks sends to non-reserved recipient domains (must be @example.com, .test, .invalid, .localhost, etc.). See `check_test_mode_safety` in [src/apple_mail_fast_mcp/security.py](src/apple_mail_fast_mcp/security.py).

## Branch Convention

`{type}/issue-{num}-{description}` — e.g., `feature/issue-42-thread-support`, `fix/issue-99-timeout`

CHANGELOG.md is only updated on release branches, never on feature branches.

## Skills

Claude Code loads these from `.claude/skills/`. Other agents should read the
`SKILL.md` files directly when working in their domains.

- **release** — Full release workflow: milestone check, version bump, changelog, validation, tagging, PR
- **applescript-mail** — Apple Mail AppleScript patterns, quirks, workarounds, JSON emission via ASObjC
- **api-design** — Tool design philosophy, decision tree for new tools
- **integration-testing** — Real Mail.app testing, why mocks miss AppleScript bugs
- **performance-patterns** — Operation timings, `whose` clause optimization, batch patterns, Gmail notes

## Key Files

- `src/apple_mail_fast_mcp/mail_connector.py` — Core AppleScript client (~6770 lines)
- `src/apple_mail_fast_mcp/server.py` — FastMCP server wrapping the connector (~3800 lines)
- `src/apple_mail_fast_mcp/imap_connector.py` — IMAP fast path (~2800 lines)
- `src/apple_mail_fast_mcp/security.py` — Input validation, audit logging, confirmation flows
- `src/apple_mail_fast_mcp/utils.py` — Pure functions: escaping, parsing, validation, host-arg coercion, `env_flag`
- `src/apple_mail_fast_mcp/version.py` — Version/commit/build-date provenance (`--version`, `serverInfo`, `diagnose_mail_access`)
- `src/apple_mail_fast_mcp/exceptions.py` — Custom exception hierarchy
- `hatch_build.py` — Freezes the git commit into `_build_info.py` at wheel-build time
- `docs/reference/TOOLS.md` — Complete API reference

## Version Provenance

`version.build_info()` resolves in descending order of trust: the build-hook
generated `_build_info.py`, then live `git` in a source checkout, then
`unknown`. An installed wheel has no `.git`, which is why `hatch_build.py`
exists — and why it must `force_include` the generated file, since `_build_info.py`
is gitignored and hatchling drops VCS-ignored paths from the wheel by default.
Never let this raise: a version banner must not be able to take the server down.
