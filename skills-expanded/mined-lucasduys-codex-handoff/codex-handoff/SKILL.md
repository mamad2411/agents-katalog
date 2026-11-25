---
name: codex-handoff
description: >
  Delegate an owner-side task to the local OpenAI Codex CLI and return its
  evidence — shell commands run as the owner, or GUI/computer-use work on this
  Mac's desktop (clicking through consoles, native apps, logged-in dashboards).
  ALWAYS use instead of telling the user to do it themselves when a step needs
  their login credentials, accounts, or logged-in sessions: creating Google
  OAuth clients, Supabase/GCP/Vercel/DNS/console setup, generating API keys,
  changing account settings. Also on "codex-handoff", "hand this to codex",
  "have codex do X". Not for ordinary coding tasks Claude can do itself.
---

# codex-handoff

Get one owner-side task actually done, and bring back proof it happened.

**Pick the surface before you pick the transport.** Codex is one of the
surfaces, not the default one:

| Task | Surface | Where |
|---|---|---|
| Shell as the owner | Codex, MCP server or `codex exec` | §3 |
| Browser the owner is already signed into | `claude-in-chrome`, driven by you | §4a |
| Native macOS app | Codex computer-use, only if §4c says the app is open | §4b |

Reaching for Codex on a browser task is the most common way this skill fails.
Codex computer-use is gated by a per-app owner approval, browsers usually do not
have it, and the resulting handoff returns nothing while looking like it worked.

## 0. Resolve the log dir (always)

`LOG=${CLAUDE_CONFIG_DIR:-$HOME/.claude}/logs/codex-handoff` (created by
install.sh; `mkdir -p` if missing). Every run — success, failure or BLOCKED —
writes two files there: `<UTC-timestamp>-<slug>.prompt.md` (the exact prompt
sent) and `<UTC-timestamp>-<slug>.result.md` (the full result/evidence). No
exceptions.

A `.prompt.md` with no matching `.result.md` means the handoff died without
returning evidence, which is the failure this skill exists to prevent.
`check-handoff-logs.sh` in this repo fails on any such orphan.

Writing the result file is your job. `-o "$LOG/<ts>-<slug>.result.md"` on exec
runs writes only when the run finishes, so a run that times out or is killed
leaves nothing behind (verified). Hand-write the result file in that case, and
for MCP runs, and for BLOCKED outcomes.

A prompt the owner has agreed to run by hand is pending, not orphaned: write it
to `$LOG/pending/` and move it up beside its result when the result comes back.
The check only looks at the top level.

## 1. Classify the task

- **Shell-doable**: achievable with commands and files as the owner (CLIs, git,
  local services, cloud CLIs already authenticated on this machine). → §3.
- **Browser with the owner's session**: a console, dashboard or webmail the
  owner is signed into. → §4a, `claude-in-chrome`, NOT Codex.
- **Native macOS app**: clicking, typing or reading a desktop app. → §4b, Codex
  computer-use, after §4c says the app is open.

## 2. Safety gate (before any handoff)

- If the task itself is **moving money, purchasing, deleting an account, or
  changing billing/plans**: do NOT hand it off autonomously. Use §5 so the human
  drives; Codex may only navigate up to the confirmation screen.
- For every autonomous run, the prompt to Codex MUST include:
  "Never move money, purchase, delete accounts, or change billing/plans. If a
  step would do so, stop and report instead of acting."
- **Secrets never travel through prompts or chat.** If Codex needs a secret,
  write it to an env file on disk (`chmod 600`), pass the file path, and say so
  in the log.
- Never use `--dangerously-bypass-approvals-and-sandbox` or
  `sandbox: danger-full-access`.

## 3. Shell tasks — registered MCP transport (preferred)

The `codex` MCP server is registered at user scope. Tools (load via ToolSearch
`select:mcp__codex__codex,mcp__codex__codex-reply` if deferred):

- `mcp__codex__codex` — args: `prompt`, `cwd`, `sandbox`
  (`read-only` | `workspace-write`), `approval-policy` (`never` for unattended),
  optional `model`. Returns final message + `threadId`.
- `mcp__codex__codex-reply` — `threadId` + `prompt` to continue that session.

Recipe: `sandbox: "read-only"` for inspection, `workspace-write` when Codex
must write files. Always set `approval-policy: "never"` (unattended) and an
explicit `cwd`.

**Fallback** (MCP unavailable in this session) — Bash, verified flags:

```bash
codex exec --skip-git-repo-check -s read-only -C "$DIR" \
  -o "$LOG/<ts>-<slug>.result.md" "<prompt>"
```

`-m <model>` selects model; `--output-schema <file>` forces a JSON final
answer; `--json` streams events and is worth it on anything that might hang,
because it shows where the run stalled even if the run never produces `-o`.

Shell runs take 30s–3min; set Bash timeout ≥300s. Computer-use runs are slower,
because the agent reads the plugin's own skill file before it acts: one app is
about 30s, and a single run asked to touch three apps has been measured past 8
minutes and killed. Keep computer-use to one app per run.

For long tasks prefer this exec form over the MCP tool even when MCP is
available — a whole Codex session runs inside one MCP tool call and can hit
the client's per-call timeout. Known codex issue: approval elicitation can
hang forever in MCP mode, so `approval-policy: never` is mandatory, not just
recommended.

## 4. GUI tasks — the surface decides the transport

### 4a. Browser, owner already signed in → `claude-in-chrome`, not Codex

Drive it yourself with the `claude-in-chrome` MCP against the owner's live
browser session. It needs nothing from the owner and serves the delegation rule
better than a handoff that cannot run. Proven this way: reading DNS records in a
hosting dashboard, changing auth settings in a backend console, clicking through
a real OAuth consent screen, sending mail from a signed-in webmail.

Codex computer-use reaches a browser only if that browser has been approved in
Codex's per-app permission system, which on many machines it has not. Two traps:

- `sky.list_apps()` lists browsers whether or not they are approved. It is a
  discovery list, not an approval list, and a model that reads it will claim the
  browser is approved and be wrong. Verified: `list_apps` returned Google
  Chrome, and control of Chrome failed with `Error: Computer Use was not
  approved to use Google Chrome`.
- Approval is machine state, not a fact to hard-code here or to carry over from
  a previous session. Probe it (§4c).

### 4b. Native macOS app → Codex computer-use, transport of §3

`computer-use@openai-bundled` drives macOS apps via the accessibility tree
(`sky` API) and loads in headless `codex exec` and MCP runs. Loading is not the
same as being allowed to act.

**Settle this before you plan around §4b at all.** Controlling an app takes
interactive owner consent, and that consent may not reach a headless run.
Measured on the machine this skill was built on, in one morning: the Codex
desktop app drove Chrome for twelve minutes and saved a real DNS record, while
headless `codex exec` probes launched two minutes later returned `Error:
Computer Use was not approved to use Google Chrome`, and the same for Notes. The
desktop app can show the confirmation dialog; `codex exec` has nowhere to show
it and is refused. Approving an app in the desktop app does not unblock the
transport in §3, so this is not a pending click you can wait out.

Probe first (§4c) and believe the probe. If it says BLOCKED there is no
autonomous Codex GUI surface on that machine: use §4a if the task is in a
browser, otherwise §5. Do not send a GUI handoff into it to see what happens.

Prompt shape:

```
Use your computer-use skill (sky API) to <task> in <app>.
Steps: <numbered steps>.
Evidence: after finishing, report the accessibility-tree text or screenshot
of the final state proving completion, plus a step-by-step log of what you
clicked/typed.
Never move money, purchase, delete accounts, or change billing/plans — stop
and report instead.
```

On an unapproved app the headless run reports the permission error and changes
nothing. Keep one GUI task per run; use `codex-reply` for follow-ups on the same
thread.

### 4c. Probe before assuming a surface is open

Read-only, one app per probe, about 30s, changes nothing:

```bash
codex exec --skip-git-repo-check -s read-only -C "$HOME" \
  "READ-ONLY PROBE. Using computer-use (sky API), call get_app_state once for
   <app> and reply with exactly 'OK ' followed by the first 60 characters of
   state.text, or exactly 'BLOCKED ' followed by the verbatim error. Do not
   click, type, navigate or open anything. Do not call list_apps. Do not take
   screenshots."
```

Read the error, do not just read the word BLOCKED: not every failure is a
permission failure. A bundle ID that resolves to more than one install (an app
running from `/Applications` while its installer disk image is still mounted
under `/Volumes`) fails with `Ambiguous app identifier`, which says nothing
about approval. On that error, re-probe with the full app path, for example
`/Applications/Google Chrome.app`.

`get_app_state` launches the app in the background if it is not running, so
prefer probing apps the owner already has open. Trust the probe over
`list_apps()` and over anything written in this file.

## 5. Blocked or human-only tasks — report, never fire-and-forget

A blocked surface is a RESULT, not a reason to hand the task back to the human
and end the turn. Write the verbatim error to `.result.md`, report BLOCKED, and
name the single action that would unblock it.

The `codex://threads/new?prompt=...` deep link pre-fills the Codex desktop
chatbox but never executes and returns nothing to this session. It is the one
path with no evidence channel: in the run log that produced this rule it left 8
orphaned prompts across 17 handoffs, several of them reported as successes. Use
it ONLY when the owner has said they want to drive the task by hand, and write
the prompt under `pending/` so the check does not count it as an orphan:

```bash
open "codex://threads/new?prompt=$(python3 -c 'import urllib.parse,sys;print(urllib.parse.quote(open(sys.argv[1]).read()))' "$LOG/pending/<ts>-<slug>.prompt.md")"
```

Never report a deep-linked task as done — nothing ran.

Before reaching for it, re-check §4a: for a site the owner is signed into,
`claude-in-chrome` finishes the task now. For a site with no live session the
fastest unblock is asking the owner to sign in once, not handing over the whole
task.

## 6. Evidence rule (always)

Never report a handoff as done without evidence in hand: raw command output for
shell tasks, final-state accessibility text or screenshot plus an action log for
GUI tasks. If Codex returns a bare "done", send one `codex-reply` demanding the
evidence before reporting back. Summarize for the user AND save the full
evidence to the `.result.md` log.

Evidence must come from the surface that did the work, not from the agent's own
account of it — Codex asserted a browser was approved on the strength of
`list_apps()` while control of it was in fact blocked. Where a claim is
checkable, check it: for a sent message, read it back from the destination.

The turn does not end on a promise. If the chosen surface is blocked, either
finish the task on the surface §4a names or report BLOCKED with the verbatim
error. "Pre-filled it, press Enter" is not an outcome.
