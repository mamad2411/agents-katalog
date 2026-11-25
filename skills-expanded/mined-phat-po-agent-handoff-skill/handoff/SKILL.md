---
name: handoff
description: "Generate an intelligent context handoff document for the next agent AND update the project's STATUS.md log (auto-compressed). Updating STATUS.md is a mandatory part of every handoff, not optional. Triggers on: handoff, hand off, pass to next agent, context handoff, next agent, session done, stage done, wrap up for next agent, update status, 更新状态, 更新进度, /handoff"
---

# Handoff — Intelligent Context Handoff for Next Agent

Generate a handoff document that gives the next agent in a fresh conversation the minimum context needed to fully understand the project state and immediately continue work — using the fewest tokens possible.

**This is NOT a template.** Every handoff is different. The structure, length, sections, and language of the handoff doc must be adapted to what actually happened and what comes next. The only thing that's fixed is the investigation process below.

---

## Non-Negotiables (read first)

Every completed handoff produces **four artifacts — all four are required, none is optional**:

1. **The handoff document** (Phase 5)
2. **An updated `STATUS.md` entry** at the project root, dated today (Phase 6) — **a handoff without a fresh STATUS.md entry is INCOMPLETE.** This is the single most-skipped step; do not skip it.
3. **A snapshot commit** (Phase 7)
4. **A copy-paste prompt** for the next session (Phase 8) — **printed directly in your chat reply as a fenced code block**, not saved to a file. This is the operator's one-click entry point for the next session; it is the second most-skipped step, so do not trail off before printing it.

You are NOT done after writing the handoff doc. You are done only after the **Completion Checklist** in Phase 8 passes — and that checklist fails if `STATUS.md` does not show today's date. Run every phase in order; do not stop early because the doc "looks finished."

---

## When to Use

- A task or stage is complete and the next step will be done in a new conversation
- The operator says "handoff", "wrap up", "done with this stage", "pass to next agent"
- Context window is getting large and work should continue in a fresh session

---

## Visual Output Format

When executing this skill, render all output using the clack-style visual system below. This makes the handoff process scannable and satisfying to watch.

### Banner

At the very start of the skill, display the banner via bash:

```bash
echo -e "\033[36m╭──────────────────────────────────────────────────╮\033[0m"
echo -e "\033[36m│\033[0m                                                  \033[36m│\033[0m"
echo -e "\033[36m│\033[0m   \033[1;37m◆  H A N D O F F\033[0m                              \033[36m│\033[0m"
echo -e "\033[36m│\033[0m   \033[2mIntelligent Context Handoff for Next Agent\033[0m     \033[36m│\033[0m"
echo -e "\033[36m│\033[0m                                                  \033[36m│\033[0m"
echo -e "\033[36m╰──────────────────────────────────────────────────╯\033[0m"
echo ""
```

### Symbol Reference

| Symbol | Meaning | Usage |
|--------|---------|-------|
| `◇` | Completed step | Phase finished successfully |
| `◆` | Active step | Currently executing phase |
| `●` | Info item | Findings, details, file paths |
| `▲` | Warning | Issues, stale docs, risks |
| `┌│└` | Guide bar | Vertical thread wrapping the flow |
| `╭╮╰╯` | Arc-corner box | Summary boxes |
| `├╯` | Branch point | Box title with horizontal extension |

### Guide Bar Rules

The entire handoff flow is wrapped in a vertical guide bar. Every line of output is prefixed with `│` to create a continuous visual thread:

```
┌
│  ◆ Phase N: Title
│
│    ● finding or detail
│    ● finding or detail
│
│  ◇ Phase N complete
│
└  Done
```

- Start with `┌` on its own line
- End with `└  Done` (or `└  Handoff complete`)
- Every content line between them starts with `│` + 2 spaces
- Phase headers: `│  ◆ Phase N: Title` (active) → `│  ◇ Phase N: Title` (done)
- Findings/details: `│    ● description`
- Warnings: `│    ▲ description`
- Empty `│` line between phases for breathing room

### Phase Header Format

Each phase output follows this pattern:

**Starting a phase:**
```
│
│  ◆ Phase N: Title
│
```

**Reporting findings (inline as you work):**
```
│    ● Found 2 prior handoff docs
│    ● Located PROJECT.md, roadmap.md
│    ● Current task: phase-3 implementation
```

**Phase complete:**
```
│
│  ◇ Phase N: Title — done
│
```

### Summary Box (End of Phase 8)

After generating the copy-paste prompt and passing the Completion Checklist, display a summary box:

```bash
echo -e "\033[36m│\033[0m"
echo -e "\033[36m├──────────────────────────────────────────────────╮\033[0m"
echo -e "\033[36m│\033[0m                                                  \033[36m│\033[0m"
echo -e "\033[36m│\033[0m  \033[1;32m◇\033[0m \033[1;37mHandoff Complete\033[0m                             \033[36m│\033[0m"
echo -e "\033[36m│\033[0m                                                  \033[36m│\033[0m"
echo -e "\033[36m│\033[0m  Handoff doc: <absolute path>                    \033[36m│\033[0m"
echo -e "\033[36m│\033[0m  STATUS.md:   <absolute path>                    \033[36m│\033[0m"
echo -e "\033[36m│\033[0m  Snapshot:    <commit hash>                       \033[36m│\033[0m"
echo -e "\033[36m│\033[0m                                                  \033[36m│\033[0m"
echo -e "\033[36m╰──────────────────────────────────────────────────╯\033[0m"
echo ""
```

Replace `<absolute path>` and `<commit hash>` with actual values. Pad lines with spaces so the right `│` aligns at column 52.

---

## The Process

### Phase 1: Trace the Chain (Look Backward)

**Before doing anything else**, display the banner (see Visual Output Format above) and start the guide bar with `┌`. Then begin Phase 1 with `│  ◆ Phase 1: Trace the Chain`.

Investigate:

1. **Find prior handoff docs** — search the project directory for files with "handoff" in the name, or files that look like they served as context transfers between agents. Read them to understand the chain of work.
2. **Find project structure docs** — look for task breakdowns, roadmaps, phase plans, SOPs, `CLAUDE.md` / `AGENTS.md`, `PROJECT.md`, or any planning documents that define the overall mission and stages.
3. **Find the current task definition** — locate the specific task doc, issue, or plan that was being worked on this session.

If prior handoff docs exist, the new handoff should be written as a continuation — the next agent should be able to read ONLY the new handoff doc (not the old ones) and still have everything it needs.

### Phase 2: Audit This Session (Look at the Present)

Gather concrete facts about what happened:

1. **Git diff / git log** — what files were created, modified, or deleted since the session started (or since the last commit before this session's work). Use `git diff --stat` and `git log --oneline` to get a clear picture.
2. **Key decisions made** — review the conversation for decisions, constraints discovered, trade-offs chosen, things that broke and how they were fixed, architectural choices.
3. **Current state** — does the code build? Are there failing tests? Uncommitted changes? Pending migrations? Anything half-finished?
4. **What was explicitly NOT done** — things that were discussed but deliberately deferred, out-of-scope items, known shortcuts taken.

### Phase 3: Scan Forward (Look at What's Next)

Cross-reference future work:

1. **Identify the next task(s)** — from task breakdowns, roadmaps, or conversation context, determine what the next agent should work on.
2. **Check for ripple effects** — did anything done this session change assumptions, invalidate plans, create new dependencies, or affect future tasks? This is critical — if we changed a database schema, renamed a type, or discovered a constraint, future task docs may now be partially wrong.
3. **Flag stale docs** — if any planning documents are now out of date because of this session's work, explicitly call this out.

### Phase 4: Build the Minimum Reading List

Figure out the smallest set of files the next agent needs to read:

1. **Docs** — only the task definitions, SOPs, or reference docs actually needed for the next step. NOT everything that was read this session.
2. **Code** — only the entry points, types, and modules the next agent will need to touch or understand. Provide absolute paths.
3. **Order them** — put the most important files first. The next agent should be able to stop reading early if context is tight.

### Phase 5: Write the Handoff Doc

Now write the handoff document. Adapt the structure to what's actually needed — don't force sections that have nothing useful to say, and add sections that the specific situation demands.

**General principles:**
- Write for an agent that knows NOTHING about this project — assume zero prior context
- Be precise: file paths must be absolute, type names must be exact, command examples must be copy-pasteable
- Include verification commands the next agent should run before starting (e.g., `git status`, `rg "some_symbol"`, build/lint checks)
- Include constraints and "do NOT touch" rules if applicable
- If the task has sub-steps, specify the exact order
- Use the same language the operator has been using in this session (Chinese, English, or mixed)

**Where to save the file:**
- If there's an existing pattern of handoff docs or task docs in the project, follow that pattern (same directory, similar naming)
- If not, save it in the project root or a planning/docs directory that makes sense
- Name it descriptively — include the stage/task name and "handoff" (e.g., `04-18A-完成-handoff给18B.md`, `handoff-phase2-complete.md`)

### Phase 6: Update STATUS.md (MANDATORY)

Maintain a running progress log at the **project root** as `STATUS.md`. This is the single file a fresh agent reads to orient itself — even without any handoff prompt. **This phase is mandatory. A handoff that does not end with a fresh, today-dated entry in `STATUS.md` is incomplete — even if the handoff doc itself is perfect.**

**Step 1 — Run the helper to get the real date and metrics (do not guess the date):**

```bash
HANDOFF_SCRIPTS="$(ls -d "$HOME"/.codex/skills/handoff/scripts "$HOME"/.claude/skills/handoff/scripts 2>/dev/null | head -1)"
bash "$HANDOFF_SCRIPTS/status-check.sh" "<project-root-absolute-path>"
```

The first line resolves the helper whether this skill is installed under Codex CLI (`~/.codex/skills/handoff/`) or Claude Code (`~/.claude/skills/handoff/`) — the script is byte-identical in both. It prints `TODAY=`, `STATUS_EXISTS=`, `TOTAL_LINES=`, `MILESTONE_COUNT=`, `COMPRESSION_NEEDED=`, and a recommended `ACTION=`. The helper is **read-only** — it never edits `STATUS.md`. Use its `TODAY=` value as the entry date; never invent a date from memory. (If the helper is unavailable, fall back to `date +%F` and `wc -l STATUS.md`.)

**Step 2 — If `STATUS_EXISTS=no`, create it with the three-layer template:**

```markdown
# [Project Name] — Status

## ▲ Current

_(No entries yet. This will be filled by the first handoff.)_

## ■ Milestones

_(empty)_

## ▼ Archive

_(empty)_
```

**Step 3 — If `COMPRESSION_NEEDED=yes` (>100 lines OR >15 milestones), compress BEFORE appending:**

1. Move all entries from `▲ Current` except the most recent → `■ Milestones` as one-line summaries (format: `- [YYYY-MM-DD] 一句话描述 | ✅/⚠️/🔴`)
2. If `■ Milestones` then exceeds 15 entries, move the oldest entries to `▼ Archive`. Only **delete** an entry outright if `▼ Archive` already holds >10 entries AND that content is already committed to git (verify the prior STATUS.md is in `git log` first — git history is the only safety net for deleted entries).

**Step 4 — Append the new entry to the top of `▲ Current`** using this format:

```markdown
---

## [TODAY] | [one-line session summary]

**Done this session:**
- [concrete completed item]
- [concrete completed item]

**Current state:**
[Where exactly things stand — what's working, what's half-done, any broken or unstable state]

**Next steps:**
1. [Most immediate action — specific enough to act on]
2. [Following action]
3. [Further if known]

**Decisions / notes:**
- [Non-obvious choices made, constraints discovered, things not to forget]
```

Keep each entry self-contained. Someone reading only the `▲ Current` section should be able to orient immediately. Replace `[TODAY]` with the helper's `TODAY=` value.

### Phase 7: Snapshot Commit

After writing the handoff doc and updating STATUS.md, create a snapshot commit so the repo state matches the handoff exactly. This gives the next agent a clean starting point and a restore point if anything goes wrong.

**Step 1 — Confirm this is a git repo.** If `git rev-parse --git-dir` fails, skip this phase and note in the summary that no snapshot was taken (not a git repo).

**Step 2 — Scan for secrets before staging** (per the workspace no-secrets rule — this must return zero real credentials):

```bash
grep -rn "sk-\|supabase\|Bearer\|password\|secret\|token" --include="*.ts" --include="*.js" --include="*.py" .
```

Review the matches. If any are actual credentials (not variable names or imports), stop — do not commit. Move the secret to `.env`, ensure `.env` is gitignored, then continue. If there are files that should never be committed (e.g. `.mcp.json` with keys, `.env`), add them to `.gitignore` first.

**Step 3 — Review what will be staged, then commit.** Run `git status --short` first. If the working tree has unrelated changes, prefer staging only the handoff doc and `STATUS.md`. Use blanket `git add -A` only when the operator wants a full snapshot.

```bash
git add -A && git commit -m "snapshot: before [next task/phase name]"
```

Never `git push` here — pushing requires explicit operator confirmation.

### Phase 8: Generate the Prompt + Completion Checklist

**This prompt is REQUIRED output. Print it directly in your chat reply as a fenced code block — do NOT save it to a file, and do NOT skip it.** It is the operator's single copy-paste entry point for the next session; without it, the operator has to hand-write the launch prompt themselves, which defeats the skill. Omitting this prompt is the second most common failure of this skill (after skipping STATUS.md) — even when the handoff doc is comprehensive, the separate copy-paste prompt is still mandatory. It must be the last content you print before the Summary Box.

Output a short prompt block that the operator can copy-paste into a new conversation. This prompt should:

- Point the new agent to the handoff file path (absolute)
- State the core task in 1-2 sentences
- Include any critical constraints in 1-2 sentences
- Tell the agent to read the handoff file first, then follow its instructions
- Be as short as possible — the handoff doc has the details, the prompt is just the entry point

**Format — print exactly like this** (a fenced code block, adapted to the real situation):

````markdown
```
请先阅读 /abs/path/to/handoff-phaseN.md，它包含你需要的全部上下文。

任务：[一句话核心任务]。
约束：[1-2 句关键约束 — 例如 别碰 X、先跑 Y 验证]。

读完 handoff 文件后按它的说明继续。
```
````

(Match the operator's working language — Chinese, English, or mixed. The example above is illustrative; rewrite it for the actual task.)

**Then run the Completion Checklist (Definition of Done).** Echo each item with its actual value. **If any item is unchecked, the handoff is NOT complete — go back and finish it before reporting done:**

- [ ] Handoff doc written — `<absolute path>`
- [ ] `STATUS.md` `▲ Current` shows an entry dated **today** — verify with `grep -m1 "$(date +%F)" STATUS.md` (must print a line)
- [ ] Compression check ran — `COMPRESSION_NEEDED=<yes/no>` from the helper
- [ ] Snapshot commit created — `<commit hash>` (or noted as skipped: not a git repo / operator declined)
- [ ] Copy-paste prompt printed above

After the checklist passes, display the **Summary Box** (see Visual Output Format above) with the actual handoff doc path, STATUS.md path, and snapshot commit hash. End the entire flow with `└  Done`.

---

## Fresh Session Orientation

When a new chat opens and the operator asks something like **"帮我看一下这个project进行到什么程度了"** or **"where are we? what's next?"** — without any handoff prompt — do the following:

1. Look for `STATUS.md` in the **project root** (current working directory)
2. Read **only** the `▲ Current` section (the most recent 1-2 entries) and the top 5 lines of `■ Milestones`. Do NOT read the full file — use line-limited reads or `head`.
3. Run `git log --oneline -5` to check for any commits since the last STATUS.md entry
4. Present a clear, direct orientation:
   - What was done last session
   - Current state of the project
   - Recommended next steps in priority order
   - Any outstanding blockers or decisions
5. **Passive compression check**: if `STATUS.md` exceeds 100 lines, note this to the operator and offer to compress it. Do NOT auto-compress during orientation — it's a read-first moment.

Do NOT wait for the operator to find the file or point you to it. Finding and reading `STATUS.md` is the default first move when asked about project status.

---

## Anti-Patterns

- **Don't write a conversation transcript** — the next agent doesn't need to know what we discussed, only what was decided and what exists now.
- **Don't include context the next agent can derive from the code** — if something is obvious from reading a file, don't duplicate it in the handoff. Just point to the file.
- **Don't pad with boilerplate sections** — if there are no constraints, don't add an empty "Constraints" section. If there's no schema change, don't add a "Database" section.
- **Don't over-include the reading list** — every extra file costs tokens. Be ruthless about what's truly needed vs. nice-to-have.
- **Don't assume the next agent will read prior handoff docs** — each handoff should be self-contained. If info from a prior handoff is still relevant, carry it forward.

---

## Maintainer note (cross-tool, single source)

This skill is **tool-agnostic** and runs identically under **Claude Code** and **Codex CLI**. There is **one** source of truth — this `SKILL.md` plus `scripts/status-check.sh` — installed (copied, not symlinked) to both `~/.claude/skills/handoff/` and `~/.codex/skills/handoff/`.

- **Never** fork a tool-specific copy — that is exactly how the two installs drifted before. Edit the source repo, then run `scripts/install.sh` to sync both tools.
- The only tool-aware line is the helper-path resolver in Phase 6 Step 1, which finds `status-check.sh` under whichever tool directory exists.
- Copies (not symlinks) are deliberate: the source repo may live on an external volume that isn't always mounted, so each tool keeps a self-contained copy on the internal disk.
