---
name: superforge-handoff
description: >
  Write the session state to a structured capsule in .handoff/, then commit and
  push it, so a different AI tool or model (Codex, Gemini CLI, Antigravity,
  Cursor, another Claude account) can resume the work from the repository.
  Use before credits or a usage limit run out, or when switching tools. Not
  needed to continue inside Claude Code itself: compaction, /compact, /clear,
  and docs/ already cover that. Also packages work for an async cloud agent
  such as Devin — deciding whether a task belongs locally or should be sent,
  and generating the brief with scope, completion criteria, and known traps.
  Use when the user says "handoff", "switch tools", "hand this to Codex",
  "credits are running out", "usage limit", "send this to Devin",
  "should Devin do this", "引き継ぎ", "ハンドオフ", "別のAIに引き継ぐ",
  "クレジットが切れそう", "使用量の上限", "Devinに投げる", "Devinでやるべき",
  or runs /superforge-handoff or /handoff.
license: MIT
metadata:
  author: Takao Umehara
  version: "2.2"
compatibility: >
  Standalone.
  Writes .handoff/ in the project root, then commits and pushes it.
  No other document or skill required.
  The Devin brief reads docs/plan.md and docs/failforward.md when they exist.
---

# Superforge Handoff — Cross-Model Session Transition Protocol

Use this skill when the work must continue in a **different tool or model**, most
often because credits or a usage limit are about to run out. It writes a
structured capsule to `.handoff/`, commits it, and pushes it, so whatever reads
the repository next can resume.

**Not for continuing inside Claude Code.** A long thread is handled by automatic
compaction, `/compact <what to keep>`, or `/clear` plus `docs/`; a later Claude
Code session reads `CLAUDE.md` and `docs/` on its own. Writing a capsule there
spends tokens to restate what is already on disk.

**Run it early.** Writing the capsule costs tokens too. Start while there is
budget left to finish and push it, not on the last message before the limit.

---

## 1. Triggering Handoff (`/handoff` or `/superforge-handoff`)

1. Ensure directory `.handoff/` exists.
2. Create capsule file: `.handoff/YYYY-MM-DD-<slug>.md`.
3. Populate the **Resume Capsule** (under 80 lines):
   - Project & Passphrase (`<repo>: <catchy phrase>`)
   - Objective & Verified State
   - Running Processes & Active Ports
   - **The `docs/` ledger** — see below. This is the part that carries the
     decisions; without it the capsule carries the conversation instead
   - Immediate Next Steps
   - Files to Read First

### The `docs/` ledger — do not skip this

**List every file in `docs/`, not a summary of them.** One row each, read from
the file's own header block:

```markdown
## docs/
| File | Status | Last updated | Open questions |
|---|---|---|---|
| superforge.md | agreed | 2026-07-29 | — （会話=日本語 / ファイル=英語） |
| product-idea.md | agreed | 2026-07-30 | none |
| business-model.md | draft | 2026-07-31 | pricing tier 3 undecided |
| design.md + design.html | agreed | 2026-07-31 | — |
| accessibility.md | draft | 2026-07-29 | 3 criteria not assessed |
| verification.md | — | — | **not run yet** |
| security.md | FINDINGS-OPEN | 2026-07-31 | 1 High 未対応 |
| ship-readiness.md | — | — | **not run yet** |
| failforward.md | 6 entries | 2026-07-31 | 1 mitigation, cause still unknown |
```

Five rules that make this worth writing:

- **`superforge.md` goes first, and its language settings travel with it.**
  A resumed session that starts replying in the wrong language has lost
  something the user set explicitly, and will be corrected manually every time.
- **A file that does not exist gets a row saying so.** "verification.md — not
  run yet" is the single most useful line in the capsule, because it tells the
  next session what has *not* been proven. A missing row reads as "handled."
- **Copy the `Status` and `Last updated` from each file's own header**, not from
  memory. A capsule that claims `agreed` for something still marked `draft` is
  worse than no capsule.
- **Carry every `## Open questions` section forward.** Those are exactly the
  decisions an unattended run is allowed to make with a logged default —
  losing them means the next session either re-asks or re-decides silently.
- **`failforward.md` is the one row that is a count, not a status.** Note the
  number of entries and, specifically, any mitigation shipped without a root
  cause — an open failure the next session would otherwise rediscover the hard
  way.

The capsule **points at** these files rather than restating them. That is what
keeps it under 80 lines while losing nothing.

4. **Commit and push** — the step that makes the capsule exist for anyone else:
   - Commit the capsule *and* any finished, verified work it describes. Never
     commit a secret; if one is staged, stop and route to `superforge-secure`.
   - If `.handoff/` is git-ignored, add it with `git add -f`.
   - Push under the branch policy in `docs/superforge.md`. With no policy
     recorded, push the current branch, but never the default branch unless
     the user asked for it. Retry a network failure; if the push still fails, say so plainly — an unpushed
     capsule in a cloud session is lost when the container is reclaimed, and
     no other tool can read it.
   - Put the branch name and commit hash in the resume prompt.

5. Output the copy-paste-ready **Chat Resume Prompt**:

~~~text
次の作業を再開してください。

Project: <repo>
Branch: <branch> @ <commit>
Handoff file: .handoff/YYYY-MM-DD-<slug>.md
Goal: <Goal>
State: <Verified state>
Next: <Immediate next step>
Read first: <Files to read>

上記のNextから開始してください。
~~~

Show the prompt even when the push succeeded: it is the user's copy if the
repository is unreachable from the next tool.

---

## 2. Resuming Session

When a session opens with a Resume Capsule, pull the named branch, read the
indicated file in `.handoff/`, and jump straight to `Next` without asking
redundant background questions.

---

## 3. Prevent the emergency: push at every checkpoint

A handoff written after the limit is hit is too late — the work that matters is
whatever was never pushed. In a cloud session (Claude Code on the web) that work
exists only in a temporary container. The durable fix is a project rule, not this
skill: commit and push at each verified checkpoint. The rule lives in
`AGENTS.md` so every tool follows it, imported by `CLAUDE.md` and `GEMINI.md`;
an optional Stop hook does it automatically → **`references/checkpoint-push.md`**.
If the project has no `AGENTS.md` rules block, offer the first-run setup
(`superforge/references/setup.md`) once; with it, the next tool also knows to
read `.handoff/` without being told.

---

## Artifact

The capsule in `.handoff/` is the artifact. Before writing it, make sure every
skill that ran this session has already written its own `docs/` file — the
capsule points at those files rather than restating them, which is what keeps
it under 80 lines.

**A capsule written without reading `docs/` is a summary of the conversation,
which is the one thing the conversation already was.** The value of this skill
is entirely in the ledger: what was decided, where it is written down, what is
still open, and what was never run.

## Deeper reference

**`references/external-agents.md`** — the other direction of handoff: packaging
work so somebody else's agent runs it **without you**, on their machine, and
returns a pull request. Devin is the reference case and the shape generalises.
Covers the one-line tools question to ask once and record in `docs/superforge.md`,
the routing test (*is the value in you being there?*), what belongs in Knowledge
versus a Playbook versus repo setup, the brief to **generate rather than describe**,
what to run on the PR when it comes back, and the honest limit — handing work out
does not make you faster at reviewing it.

The test worth remembering even if you never read the file: **a task too vague to
hand to Devin is too vague to run unattended anywhere.** `docs/plan.md` already
carries one outcome, a proof line, and a file list per task; that *is* the brief.

## Delegate when a sharper skill is installed

`cross-model-handoff:handoff`, `handoff-setup` (tool-agnostic notes) ·
`memory` (long-term facts worth keeping beyond this project).
