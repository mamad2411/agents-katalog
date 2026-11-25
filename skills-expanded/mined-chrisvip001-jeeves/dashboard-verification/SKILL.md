---
name: dashboard-verification
description: Verify a dashboard change end to end before calling it done. Use when changing the Web workbench in web/, its backend in jeeves-ops, the protocol schema, or sw.js. Runs the real product, collects reusable evidence (status codes, API responses, screenshots), and reports what passed.
---

# Dashboard verification

A change is not done when it compiles. Prove the user path still works, keep the
proof, and report facts — not "I think it works". This is **verify-only**: do not
fix issues found here in the same pass; report them with the evidence.

## Function map — what to prove

| Function | How to reach it | How to confirm it worked |
|---|---|---|
| Front page | `GET /` | 200, `text/html`, `cache-control: no-store`, script tag carries `main.js?v=<stamp>` |
| Versioned script | `GET /main.js?v=<stamp>` from the page's own tag | 200, contains the `/api/*` routes the UI calls |
| Session state | `/api/data`, `/api/session`, `/api/session/meta` | 200 with the current session and turn state |
| Turn stream | `/api/turn/start` with `fake_sse_server.py` | SSE events arrive in order; the full reply reads back |
| Steering / follow-up | `/api/turn/steer`, `/api/turn/follow-up` | Refuse when no turn is running; accept when one is |
| Capabilities | `/api/skills`, `/api/skills/install`, `/api/skills/remove`, `/api/mcp`, `/api/mcp/save`, `/api/mcp/remove` | Lists match fixtures; built-ins greyed out; writes return an outcome receipt |
| Memory center | `/api/ledger/turns`, `/api/memory/index`, `/api/memory/page`, `/api/context`, `/api/skills/stats`, `/api/compact` | Each answers from the real app-server, no stubs |
| Schedules | `/api/schedules/jobs`, `/api/schedules/save`, `/api/schedules/remove` | Create → list → bad cron refused → delete |
| Approval labels | inspect the built `main.js` | Allow-once, session-always and remember labels are present |
| Browser ids | compare `must("…")` calls in `workspace.ts` with `dist/index.html` | Every required id exists in the served page |

## Reusable commands

Run from the repo root, in this order. Each command exits non-zero on failure.

```sh
cargo build -p jeeves-cli                 # engine + dashboard binary
npm run build --workspace @jeeves/dashboard             # typecheck + bundle + version stamp
cd .. && just check                        # all static gates
bash scripts/smoke-dashboard.sh            # real Runtime, curl as the browser
```

For visual checks, use the Playwright smoke with a screenshot directory:

```sh
JEEVES_UI_SCREENSHOT_DIR=<artifact-dir> node scripts/smoke-approval-notice.mjs
```

`smoke-dashboard.sh` already pins the `/api/*` strings, the `must()` ids and the
version stamp. When adding a new route or id, add its assertion there in the same
change — the check is only as good as the path it covers.

## Evidence to keep

Save these next to the change report:

1. The command output above (status codes and `✓` lines count as evidence).
2. `dist/index.html` with its `main.js?v=` stamp, so a stale cache cannot be blamed later.
3. Screenshots of the affected panel, before and after, when the change is visual.
4. The failing step and the observed value when something breaks — not a summary of it.

## Report format

- What was verified, by which command, with the pass/fail lines.
- What could not be verified and why (missing key, no browser, flaky timing).
- Exact evidence paths. If no screenshot was taken, say so plainly.
