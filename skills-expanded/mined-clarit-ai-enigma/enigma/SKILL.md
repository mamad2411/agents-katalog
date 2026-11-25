---
name: enigma
description: Use whenever a task needs a secret value — an API key, token, password, or connection string — to configure, run, or test something, or whenever you are about to read a .env file, an environment variable, or a credential store. Also use immediately when a tool call is denied by Enigma's read-guard hook. Never ask the user to paste a secret into the chat instead of using this skill.
---

# Enigma: getting a secret without ever seeing it

Enigma exists for one reason: **a secret's value must never enter your context window.** Everything below follows from that. If you ever find yourself about to type "paste your API key here" or "what's the value of X" — stop. That single act is the failure this entire plugin exists to prevent, no matter how well the rest of a task goes.

## The rule, stated plainly

- **Never ask the user to paste a secret into the chat.** Not "just this once," not "temporarily," not "so I can debug it." There is no exception. If you need a value stored, call `enigma_request`. If you need a value used, call `enigma run -- <command>`. There is no third way that keeps the value out of your context.
- **You never read a secret value. Ever.** Not from a file, not from an environment variable, not from a tool's output, not from the user's message. If a task seems to require you to see a value, the task is wrong, not the rule — re-scope it to use `enigma run` instead.

## Getting a value into a place that needs it

- **To store a new secret or rotate one**: call the `enigma_request` MCP tool with the `names` you need, a short `reason`, and `usage: "interactive"` or `"unattended"` (see the depository section below for why `usage` matters). It opens an out-of-band form for the human; you get back only a names-and-status summary, never the value. The human may also add secrets you did not ask for (extra rows or a pasted `.env` blob); those come back marked `— added by user`, and a count like `2 invalid names skipped` when some of what they typed wasn't a valid name. If the client doesn't support URL-mode elicitation, or advertises it but declines, cancels, errors or doesn't answer (a headless/non-interactive host declines automatically, so the user was never shown a form), it returns `{ request_id, url, expiresAt }` with a local link instead of a cancel — tell the user to open that URL in their browser (it is local only), then call `enigma_await` with that id once they say they've submitted the form. On macOS you can instead call `enigma_request` again with `ui: "native"` for a system dialog.
- **A host background-watch tool (Claude Code's `Monitor`, etc.) can poll the request link to wake the turn the moment the human submits the form** — `enigma_request` itself cannot push a notification into a host turn. The local server exposes `GET /r/<request_id>/status`, which returns `{"state":"pending"}` until the human submits, `{"state":"fulfilled"}` once results are recorded, and `404` once the link has been swept. The body carries no names and never consumes the outcome, so polling it is free. **Stop the watch on the first non-`pending` response — `fulfilled`, `404`, and a connection failure all mean the watch is over — then call `enigma_await` with the request id; its result is the authoritative outcome.** Never keep polling a dead link: a `404` or an unreachable server will never become `fulfilled`. If your host has no background-watch tool, just call `enigma_await` immediately after `enigma_request` and keep the turn open — that is the simpler, always-correct fallback.
- **`enigma_request` with `ui: "native"` (macOS system dialogs)** shows one dialog per name, titled and numbered ("1 of 3", "2 of 3", ...), each asking for that single value only. Every dialog also shows your one `reason`, so keep the `reason` short and about the whole request; do not describe each credential in it, and never ask the user to put several values into one field.
- **To run something that needs the real value**: call `enigma run -- <command> [args...]` (via Bash, or tell the user to run it). It injects the actual values into the child process's environment; you see only the child's stdout/stderr, never the injected values. **Narrow what a worker process receives with `enigma run --only A,B -- <command>`** — the child gets only the named secrets injected, not everything registered for the project. Prefer it whenever a subprocess needs one or two names out of many.
- **To let the user see a value themselves**: call `enigma_reveal` (or point them at `/enigma:reveal NAME`). It opens a one-time, out-of-band disclosure to the human. It is human-initiated by design — you should not invoke it on your own judgment; only when the user actually asks to see a value.
- **To see what secrets exist** (names only, never values): `enigma_list` or `/enigma:list`.
- **To check the local setup**: `enigma_doctor` or `/enigma:doctor` — platform, which depositories are available, 1Password CLI status, tunnel binaries, any pending unconfirmed requests (the recovery signal for a request/import whose outcome you never received — `call enigma_await(id)` to re-fetch it; SessionStart does not surface this, because the request store lives in the MCP process), and any legacy project-scope entries left over from before projectIds became repo-level.
- **When doctor or the SessionStart context flags legacy project-scope entries**: entries stored before `projectId` became the canonical repo identity (linked worktrees, symlinked clone paths, submodules) are invisible until re-keyed — there is no read fallback, by design. Run `enigma migrate-scope` (dry run: prints each entry's name, depository, recorded path, and class — `adoptable`, `orphaned-adoptable`, `orphaned-unrecoverable`, or `conflict`), then `enigma migrate-scope --apply` to re-key. It is index-only: it never resolves a value and never calls a depository, so there are no prompts. `orphaned-adoptable` entries (recorded path deleted) need `--from <recorded path>` as the user's attestation that they belong to this repo; `orphaned-unrecoverable` entries (`env` depository, deleted `.env`) can only be reported or pruned with `--prune-unrecoverable` — the value is gone, so re-request the name.
- **Never** `enigma get NAME`, `enigma env`, `cat .env`, `echo $NAME`, or any other direct read. If a name is already stored and you just need it applied, that's what `enigma run` is for — there is no "get" path for you, by design.

## A read-guard denial is an instruction, not an obstacle

Enigma installs a `PreToolUse` hook that denies tool calls that would put a secret's value into your context — reading a `.env` file, catting Enigma's config directory, echoing a tracked variable, `enigma get`, reading the Keychain or 1Password directly, and a few other shapes. **Every denial's message tells you exactly what to do instead** — call `enigma_request`, or use `enigma run -- <command>`.

When you hit one of these denials:
- **Follow the instruction in the denial message.** It is not a bug, not a false positive to route around, and not a wall to climb over some other way (renaming the file, encoding it, reading it through an interpreter, `source`-ing it into a shell). An agent that treats a denial as an obstacle to defeat rather than a redirect to follow is exactly the failure mode this hook exists to catch — you would be demonstrating the threat model, not working around a limitation.
- **Do not retry the same read a different way.** If `Read(.env)` is denied, do not try `Bash("cat .env")`, `Bash("base64 .env")`, or piping it through `python`. All of these defeat the point of the guard even if some of them technically slip past its pattern matching.
- If a denial seems wrong for what you're actually trying to do (e.g. you only wanted to check whether a `.env` file exists, not read its contents), say so to the user and ask how they want to proceed — don't silently find a different way to read it anyway.

## Choosing a depository: this is the user's call, not yours

A depository's **prompt profile** is its interaction cost on every read — this is a real tradeoff, not a technical detail, and it belongs to the user because they're the one who will be interrupted by it:

| Depository | Prompt profile | What that means |
|---|---|---|
| `env` | none | No prompt. Same trust level as any other file on disk. |
| `encrypted` | none | No prompt. Enigma's own AES-256-GCM store; key lives locally. |
| `keychain` (macOS) / `secret-service` (Linux) | may-prompt | May trigger a Touch ID / password prompt on read, depending on OS-level access rules. |
| `1password` | prompts-each-read | Prompts (biometric or 1Password unlock) on *every single read* — no exceptions. |

Match this against the `usage` you pass to `enigma_request`:
- **`usage: "unattended"`** — something that will run later with no one watching (a cron job, a CI step, a long-running background process). A `prompts-each-read` depository here doesn't just add friction, it **breaks the job** the first time it runs unattended and nothing is there to answer the prompt. Say this plainly to the user if they're heading toward 1Password for an unattended job, and let the picker's `none`-profile default (env/encrypted) do its job instead.
- **`usage: "interactive"`** — a human is present and will finish the flow. A `may-prompt` or `prompts-each-read` depository is a reasonable, sometimes preferable choice here (extra assurance the human is present each time).

**Don't pick the depository yourself and present it as settled.** Explain the tradeoff — what the biometric/prompt friction actually is, and how it interacts with the `usage` they told you — and let the user make the call, or let the request page's picker ask them directly. Only pass an explicit `depository` to `enigma_request` when the user has actually told you which one they want.

## Quick reference

| Need | Do this |
|---|---|
| Store or rotate a secret | `enigma_request` (or `/enigma:request`) |
| Use a secret in a command | `enigma run -- <command>` (narrow to named secrets with `--only A,B`) |
| Show a secret to the human | `enigma_reveal` (or `/enigma:reveal`, human-initiated) |
| See what's registered | `enigma_list` (or `/enigma:list`) |
| Check local setup/health | `enigma_doctor` (or `/enigma:doctor`) — also lists pending unconfirmed requests |
| Move values out of a `.env` file | `/enigma:import` (human-initiated — it rewrites the file) |
| Re-key legacy project-scope entries (pre-repo-identity) | `enigma migrate-scope` to preview, then `enigma migrate-scope --apply` |
| Delete a secret | `enigma_remove` (or `/enigma:remove NAME [scope]`, human-initiated — destructive, cannot be undone) |
| A tool call was denied | Read the denial message and do what it says — don't route around it |
