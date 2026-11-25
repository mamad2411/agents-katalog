---
name: vozo-auth
description: Handle Vozo CLI sign-in state, browser login, logout, remaining points, and membership checks. Use when the user needs to authenticate, verify the active session, inspect credits, or confirm subscription status before project actions.
compatibility: cursor, codex, claude-code, workbuddy
metadata:
  author: vozo
  version: '0.5.2'
  homepage: https://www.vozo.ai
  repository: https://github.com/vozoai/cli
  npm: https://www.npmjs.com/package/@vozoai/cli
---

# Vozo Auth

## CLI prerequisite

Requires the official `vozo-cli` from npm [`@vozoai/cli`](https://www.npmjs.com/package/@vozoai/cli) (source: [github.com/vozoai/cli](https://github.com/vozoai/cli)). Install with `npm install -g @vozoai/cli` or `npx @vozoai/cli@latest install`. Do not install from third-party mirrors or untrusted tarballs. Never print tokens.

## Applicable Scenario

Use this skill when the user wants to:

- sign in to the CLI
- check whether the CLI is already signed in
- log out of the current CLI session
- check remaining points
- check membership status

Before any `project` create or download work, prefer `auth status` (and `auth points` / `auth membership` when quota matters). Hand off to `vozo-project` after auth is clear.

## Preferred Commands

| Command                    | Purpose                            |
| -------------------------- | ---------------------------------- |
| `vozo-cli auth status`     | Current session and user summary   |
| `vozo-cli auth login --timeout-seconds 600` | **Default:** single blocking browser sign-in; wait for it to finish |
| `vozo-cli auth login --background` | Fallback: start sign-in and return immediately; only when your tool runner cannot hold a command open long enough |
| `vozo-cli auth wait`       | Fallback: poll in short chunks after `--background` login |
| `vozo-cli auth logout`     | Clear local session                |
| `vozo-cli auth points`     | Remaining point balances           |
| `vozo-cli auth membership` | Plan, expiry, mapped tier          |

## Hard Rule: Open The Login Page At Most Once

**In one login attempt, call `auth login` at most once.** Do not open the browser again because a tool timed out, a poll timed out, or you are unsure whether login finished.

| Do | Do not |
| --- | --- |
| One `auth login` (blocking or `--background`) to start sign-in | Call `auth login` again on timeout / uncertainty |
| After starting login, only use `auth status` / `auth wait` | Start both blocking login and `--background` login in the same attempt |
| Tell the user to finish in the already-opened browser (or the printed `loginUrl`) | Loop `auth login` until it succeeds |

If your previous `auth login` was interrupted (tool timeout / killed process):

1. Run `auth status` first — sign-in may already have completed.
2. If still `auth_required`, prefer `auth wait --timeout-seconds 30` (repeat as needed) over a new login.
3. Only if wait cannot finish and the user still needs to sign in, start **one** new login. Prefer `auth login --background`, then continue with `auth wait`. Never loop `auth login`.

## Call Order

1. Run `vozo-cli auth status` first.
2. If already signed in and the user only asked for status, summarize and stop.
3. If not signed in, explain that login opens the browser for sign-in.
4. **Default: run a single blocking `vozo-cli auth login --timeout-seconds 600` and wait for it to finish.** Set your own shell-tool timeout to at least 600s (most runners default to ~120s but accept an explicit longer value). One call, one result: the final stdout JSON tells you definitively whether sign-in succeeded — no polling loop, no ambiguity. Watch stderr for `VOZO_CLI_EVENT` lines (`auth_pending`, `auth_waiting`, `auth_callback_received`) for progress, and do not run a separate `auth status` after it succeeds; the final stdout JSON already means authenticated.
5. While it waits, tell the user to complete sign-in in the browser that opened (or open the `loginUrl` printed on stderr manually if it didn't). **Do not start another login while waiting.**
6. Only fall back to the non-blocking flow when your tool runner genuinely cannot hold a command open long enough (no way to raise its timeout): run **one** `vozo-cli auth login --background` (returns immediately with `loginUrl`/`callbackUrl`), then poll `vozo-cli auth wait --timeout-seconds 30` in a loop:
   - If it returns `authenticated: true`, summarize success and stop.
   - If it throws a timeout error, just call `auth wait` again — do not treat one chunk's timeout as failure, and do **not** call `auth login` again. Give the user a short progress update between calls (e.g. "still waiting for you to finish in the browser") instead of polling silently.
   - If it throws a real error (not a timeout), report it and offer to retry.
   - Stop retrying and check in with the user after a few minutes of no progress (e.g. ~5 chunks) rather than looping forever.
7. Run `auth points` or `auth membership` only when the user asked, or when upcoming `project` work depends on quota or plan tier.
8. Run `auth logout` only when the user explicitly wants to sign out.

## Display Requirements

- **"Vozo" is a brand name — never translate, transliterate, or localize it.** Always keep it exactly as `Vozo` (capital V) in every language and in all user-facing text, summaries, and messages.
- Do not dump raw auth JSON unless the user explicitly asks.
- Summarize `auth status`:
  - signed in / not signed in
  - account email or display ID when available
- For `auth membership`, use a stable human-readable summary:
  - `Account`
  - `Membership`
  - `Status` when not free
  - `VIP status` when available
  - `Started at` when available
  - `Expires at` when available
  - `Payment type` when available
  - `Upcoming plan` when available
- For `auth points`, use a stable human-readable summary:
  - `Account`
  - `Total available points`
  - `Point buckets`
  - each bucket in `available X / total Y` form
- After login: short success message (account identifier), never token or refresh token values.

## Confirmation Rules

| Policy | Commands |
| --- | --- |
| Read-only (run immediately) | `auth status`, `auth points`, `auth membership` |
| Run when user asks to sign in | single blocking `auth login --timeout-seconds 600` (default) |
| Fallback, only if your tool cannot hold a call open long enough | **one** `auth login --background`, then poll `auth wait` |
| Confirm if user did not ask to sign out | `auth logout` |

## Failure Recovery

| Situation                             | Action                                                                                                                                                                                                                                                                                                                                      |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| No session                            | Blocking `auth login --timeout-seconds 600` (**once**)                                                                                                                                                                                                                                                                                      |
| `missing_session` / `invalid_session` | Explain briefly; offer blocking `auth login --timeout-seconds 600` (**once**)                                                                                                                                                                                                                                                               |
| Blocking `auth login` got killed by your own tool timeout | This means your tool cut the command off, not that the CLI failed. Run `auth status`. If still `auth_required`, run `auth wait` first — do **not** immediately run another `auth login`. Only if wait cannot finish, start **one** `auth login --background` and continue with `auth wait`. |
| `auth wait` chunk times out (fallback flow) | **Do not assume login failed, and do not call `auth login` again.** A single `auth wait --timeout-seconds N` call timing out only means that chunk elapsed. Just call `auth wait` again. Only after several chunks with no progress should you run `auth status` to sanity-check, tell the user, and ask before restarting login. |
| Expired session                       | Refresh may run automatically; if still failing, **one** blocking `auth login --timeout-seconds 600`                                                                                                                                                                                                                                          |
| Auth OK but `project` fails           | Re-check `auth status`; hand off to `vozo-project` with auth summary                                                                                                                                                                                                                                                                        |
| Points / membership fetch fails       | Report error; do not retry create until entitlements are readable                                                                                                                                                                                                                                                                           |

## Examples

**User:** Check whether I am signed in and how many points I have.

```text
1. vozo-cli auth status
2. vozo-cli auth points   (only if status shows authenticated)
```

**Agent output (example):**

```text
Vozo CLI is signed in.
Account: user@example.com

Remaining points:
- general: 128.50
```

**User:** Login timed out.

```text
1. vozo-cli auth status   (verify whether sign-in actually succeeded)
2. If still auth_required: vozo-cli auth wait --timeout-seconds 30 (repeat; do not auth login yet)
3. Only if wait cannot complete: one vozo-cli auth login --background, then auth wait
```

**User:** Log me in.

```text
1. Briefly explain the browser sign-in flow
2. vozo-cli auth login --timeout-seconds 600   (run with a >=600s tool timeout; wait for it to finish; do not start a second login)
3. The final stdout JSON reports the result; on authenticated: true, summarize success
```

## Relation to `vozo-project`

- `vozo-project` assumes auth is handled first via this skill.
- For create/download, membership and points from this skill gate whether to proceed or warn about limits.
