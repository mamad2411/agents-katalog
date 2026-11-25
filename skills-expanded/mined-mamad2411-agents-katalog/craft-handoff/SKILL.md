---
name: craft-handoff
description: >-
  Produce a copy-paste-ready continuation prompt that bootstraps the next
  session. Use proactively whenever a session is wrapping up. Triggers: "wrap
  up", "마무리", "세션 정리", "핸드오프", "다음 세션으로 넘겨",
  "next session으로 넘겨", or before /clear.
---

# craft-handoff

## Purpose

End the current session cleanly by producing a **continuation prompt** the next session can paste in to resume work without losing context. The prompt is short, structural, and copy-paste-ready.

This is *not* a session-summary doc for humans. It is an LLM-targeted prompt designed to bootstrap the next agent session with exactly the context it needs — and nothing more.

## Use this when

- the user says "wrap up", "마무리", "세션 정리", "핸드오프", "다음 세션으로 넘겨", or "next session으로 넘겨"
- the user is about to run `/clear` and wants continuity
- a long session is ending and the next session should pick up cleanly
- a task is paused mid-flight and needs a clean resume point

Skip when the session was a quick Q&A with no state worth carrying.

## How it differs from related skills

- `/session-handoff` (sungjunlee-claude-config) — writes a verbose `docs/handoff/HANDOFF-*.md` into the project. Use that for multi-day continuity with team-readable docs.
- `craft-prompt` — the composition engine. `craft-handoff` gathers session state, distills it, then delegates composition to craft-prompt's `templates/session-handoff.md` and `SKILL.md` §Step 3. Use craft-prompt directly when you want to author a prompt without session-state gathering.
- `reflect` (jangpm-meta-skills) — focuses on docs/automation/learnings post-session. `craft-handoff` focuses on the next-session bootstrap prompt.

## Inputs

Auto-collected via the gather script. Run it from anywhere inside the worktree using the agent's shell:

```bash
node <skill-dir>/scripts/gather-state.mjs
```

`<skill-dir>` is wherever this skill is installed (your runtime knows the path). The script prints worktree root, branch, short status, diffstat, and recent commits. Read the output before composing.

If Node isn't available, fall back to the equivalent commands:

```bash
git rev-parse --show-toplevel
git rev-parse --abbrev-ref HEAD
git status --short | head -40
git diff --stat | tail -20
git log --oneline -8
```

Drawn from the conversation (you must extract these — no script can):

- **Done** — what was actually accomplished this session (not what was attempted)
- **Decisions** — non-obvious choices with their rationale ("chose X because Y"). Skip if none.
- **Blockers** — anything that stopped progress and needs resolution. Skip if none.
- **Next** — concrete next steps the new session should take

Optionally ask the user (one terse question, only if genuinely ambiguous): which next step to prioritize.

## Steps

### Step 0 — Confirm intent before side effects

This skill mutates the clipboard and writes a file. Both are visible side effects. If the trigger was ambiguous (e.g. the user said "let's wrap up this thread" while still mid-task, not "wrap up the session"), ask a one-line confirmation first: *"Generate a session-handoff prompt and copy it to the clipboard?"*

Skip the confirmation when the user explicitly invoked `/craft-handoff` or used a clear trigger phrase. The cost of one extra question is much lower than overwriting the user's clipboard during normal work.

### Step 1 — Gather

Run `node <skill-dir>/scripts/gather-state.mjs` (or the fallback commands in §Inputs). Read its output. Then scan the conversation for done / decisions / blockers / next. If a section has nothing real, omit it — empty headers add noise.

### Step 2 — Distill

For each section, write the *minimum* a future agent needs:

- **Done**: 2–5 bullets, outcomes not narration ("added auth middleware" not "we discussed and then implemented…")
- **State**: branch, ahead/behind, test status if known, blockers
- **Decisions**: only the non-obvious ones, each with its because-clause
- **Next**: 1–3 concrete tasks with success criteria

Use **worktree-relative paths** (`src/auth.ts:45`, not absolute paths). All paths are relative to the worktree root reported above.

### Step 3 — Compose (delegate to craft-prompt)

craft-prompt owns prompt composition — don't re-specify templates here. Read and apply.

**Prerequisite**: craft-prompt must be co-installed. The two skills ship together in craftkit; if craft-handoff was copied standalone, see the fallback in `## Failure modes` below.

1. Read the sibling skill file `craft-prompt/templates/session-handoff.md` (in the same `skills/` directory, or the same commands/agents layout where craft-handoff itself was loaded from). Pick the variant:
   - **Continuation** — normal wrap-up (most common)
   - **Debug Handoff** — mid-investigation session
2. Read `craft-prompt/SKILL.md` §Step 3 (sizing + building blocks), §Step 4 (Sharpen checklist), and §Principles §4 (generic cut order). Apply them to decide which blocks to include and what to trim.
3. Fill the chosen template with the distilled material from Step 2. Omit blocks with no content.

**Required signals** (enforce after fill):

- `## Done` items name outcomes, not narration.
- Every `## Decisions` item carries a rationale clause (`because <reason>` or `— <reason>`); drop lines without one.
- `<task>` has a `Success criteria:` (or `성공 기준:`) list with at least one measurable item.
- `<rules>` names at least one key file for the next session to read first (e.g., `Read src/auth.ts first`). If there is genuinely nothing worth pointing at, omit the line rather than invent one.
- All paths are worktree-relative — strip `/Users/…`, `/home/…`, `C:\…` before writing.
- Verify command matches the input project's actual stack. If no tests ran this session and the stack is unclear, omit the command rather than guess.

**Size budget**: ≤ 800 tokens (inherited from the template). If over budget after craft-prompt's cut order, call it out to the user rather than silently truncating.

### Step 4 — Persist + copy

1. Use your agent's file-write tool to write the composed XML block to `~/.craftkit/handoff/pending.md`. Create the directory first if needed (`mkdir -p ~/.craftkit/handoff`). Writing through the file tool avoids heredoc-EOF collisions when the prompt body contains shell metacharacters.
2. Copy it to the clipboard:

```bash
bash <skill-dir>/scripts/copy-clipboard.sh < ~/.craftkit/handoff/pending.md
```

The wrapper auto-detects the platform (`pbcopy` → `wl-copy` → `xclip` → `xsel` → `clip.exe`). If none are available it exits non-zero and prints to stderr — surface that to the user. The file write still succeeded; the user can `cat` it manually.

### Step 5 — Inform

Show the prompt before the confirmation — the user wants to verify the artifact first. You can't detect from inside the skill whether the optional SessionStart hook is installed, so always give the manual `/clear`-and-paste instruction and append the auto-load pointer.

Deliver, in this order:

1. The composed prompt in a fenced code block so the user can verify.
2. "Copied to clipboard. Saved to `~/.craftkit/handoff/pending.md`."
3. "Run `/clear`, then paste."
4. *"On Claude Code, you can skip the paste step by installing the SessionStart hook — see `references/auto-load-hook.md`."*

## Output format

Always deliver in this order:

1. The composed prompt (fenced XML code block)
2. A 1-line confirmation: file path + clipboard status
3. The next-step instruction (one line)

Do not summarize what you put in the prompt — the user can read it. Do not add a "session retrospective" — that's a different skill.

## Cross-platform notes

| Platform | Clipboard tool | Notes |
|---|---|---|
| macOS | `pbcopy` | Bundled |
| Linux Wayland | `wl-copy` | `wl-clipboard` package |
| Linux X11 | `xclip` or `xsel` | Most distros, may need install |
| Windows / WSL | `clip.exe` | Bundled with Windows |

The wrapper script tries them in that order. If your system has none, the prompt is still saved to `~/.craftkit/handoff/pending.md` — you can `cat` it manually.

## Auto-load on `/clear` (Claude Code only, optional)

This is a Claude-Code-specific convenience — skip on Codex or other agents (the clipboard step above is the cross-agent path).

`/clear` itself can't be invoked from a skill — built-in commands are not exposed to the Skill tool. But a `SessionStart` hook with `matcher: "clear"` *can* inject `additionalContext` into the post-clear session. That's the bridge.

See `references/auto-load-hook.md` for the one-time installation (settings.json snippet + a 15-line Node script).

## Failure modes

- **Empty handoff**: skill ran on a no-state session. Tell the user there's nothing to hand off and skip the file write.
- **Outside a git repo**: `gather-state.mjs` reports `(not a git repo)` for branch and `(clean)` for status. Drop the State block from the composed prompt and lean on the conversation-derived sections.
- **Multi-subtask session**: the conversation covered several unrelated threads. Don't merge them into one Next — ask the user which thread to carry forward, or pick the most recently active one and say so explicitly in the prompt body.
- **Stale pending.md**: a previous handoff was never consumed. Overwrite without asking — the new state supersedes. On the auto-load side, the hook treats pending.md older than 72h (configurable via `CRAFTKIT_HANDOFF_TTL_HOURS`; set to `0` to disable) as stale and archives it without injection. See `references/auto-load-hook.md`.
- **Bloated prompt**: token budget blown. Trim *before* writing. Handoff-specific cut order (supersedes craft-prompt's generic role/context/hedging sequence for this case): cut decisions first, then state details, never the next-step block. If still over budget after trimming, call it out to the user instead of silently truncating.
- **Auto-load injects when not wanted** (Claude Code only): user ran `/clear` to truly reset, but `pending.md` was lurking. The hook archives after injection (one-shot) and skips injection for handoffs older than 72h (TTL configurable via `CRAFTKIT_HANDOFF_TTL_HOURS`). Manual cleanup: `rm ~/.craftkit/handoff/pending.md`. Past handoffs live in `~/.craftkit/handoff/archive/`.
- **Malformed `settings.json` after manual hook install** (Claude Code only): the hook silently fails to fire. Validate the JSON (`node -e "JSON.parse(require('fs').readFileSync(process.env.HOME+'/.claude/settings.json','utf-8'))"`) and check `~/.claude/logs/` if available.
- **craft-prompt not installed**: Step 3 delegates to craft-prompt's template and sizing guidance. If craft-prompt is absent (craft-handoff was copied standalone), fall back to composing the prompt directly using the Required signals in Step 3 and this `<context>/<task>/<rules>` shape from the Example section below. Tell the user they should install craft-prompt for ongoing use — the two skills ship together in craftkit.

## Example

### Input situation

Session spent 90 minutes adding JWT auth middleware. Two files modified, one decision made (rejected sessions in favor of JWT for stateless deploy). Tests passing. Next step: wire the middleware into the route table.

### Output

```xml
<context>
## Project
acme-api — Node/Express REST backend

## Done
- Added JWT verification middleware at `src/middleware/auth.ts`
- Wired token issuance into `src/routes/login.ts:42`

## State
- Branch: feat/jwt-auth (3 ahead of main)
- Tests: passing (`npm test`)

## Decisions
- Chose JWT over server sessions — because deploy target is stateless (Cloud Run, no sticky)
</context>

<task>
Wire the auth middleware into the protected route group in `src/routes/index.ts`.
Add an integration test that hits `/api/me` with and without a valid token.

Success criteria:
- `/api/me` returns 401 without token, 200 with valid token
- `npm test` stays green
</task>

<rules>
- All paths are relative to the worktree root
- Read `src/middleware/auth.ts` first to confirm the export shape
- Run `npm test` before declaring done
</rules>
```

Copied to clipboard. Saved to `~/.craftkit/handoff/pending.md`.
Run `/clear`, then paste.

## References (load on demand)

- `references/auto-load-hook.md` — Optional `SessionStart` hook that auto-injects `pending.md` after `/clear`, removing the manual paste step.
