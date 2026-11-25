---
name: finish-phase
description: Graduate a completed exec-plan from active/ to completed/, synthesize an outcome section (results / pitfalls / remaining), and update the index. Daily harness hygiene — keeps the project's "where are we now" pointer accurate so new agent sessions don't waste context rebuilding state.
allowed-tools: Read, Glob, Grep, Write, Edit, Bash(git log:*), Bash(git diff:*), Bash(git status:*), Bash(ls:*), Bash(mv:*), AskUserQuestion
---

# finish-phase

Close out an exec-plan cleanly. The single most-referenced harness ritual: it's what keeps the harness honest about *what's done* and *what's still in flight*.

## When to use

- A milestone / sprint / W-phase / feature ships
- An exec-plan in `docs/exec-plans/active/` is no longer being worked on
- You feel the urge to delete the active plan file (don't — graduate it)

## When NOT to use

- The work isn't actually done — finish the work first
- The repo has no harness yet — run `/bootstrap-harness` first
- The plan was abandoned, not completed — just `mv` it to `docs/exec-plans/abandoned/` (no synthesis needed)

---

## Why this exists (the vibe-coding tie-in)

Industry surveys show teams spend **20-30% of sprint capacity** fixing bugs that trace back to vibe-coded work where *nobody wrote down what was actually done*. The pattern is consistent: code ships, no closing note is written, three months later the next change breaks because the original constraints are forgotten.

GitHub's 2,500-repo AGENTS.md study found that the single most-queried piece of context an agent asks for is **"what's the current state of this work?"** — and the single most-rotted artifact is the planning doc that was never closed out.

Finish-phase forces 60 seconds of synthesis at the right moment.

---

## Workflow — 5 steps

### Step 1 — Discover active plans

```bash
ls docs/exec-plans/active/*.md 2>/dev/null
```

If empty: tell the user there's nothing to finish; suggest running `/review-harness` instead.

If one file: that's the candidate.

If multiple: ask which one (AskUserQuestion).

### Step 2 — Gather closing evidence

In parallel, run:

```bash
git log --oneline -30
git diff <plan-creation-commit>..HEAD --stat   # if you can infer the start point
git status --short
```

Also read the plan file itself. Note:
- What was the plan's goal (top of file)
- What's the recent code activity
- What did the user discuss in this conversation that touched the plan

### Step 3 — Draft the outcome section

The outcome section appended to the plan file uses this exact shape:

```markdown
---

## 结果 / Outcome

- <2-4 bullets: what shipped, with file paths or commits>

## 踩坑 / Pitfalls

- <0-3 bullets: what surprised us, with enough context to be useful 6 months later>

## 遗留 / Remaining

- <0-3 bullets: known shortcuts / debt — link each to `tech-debt-tracker.md` if added there>

**Completed**: <YYYY-MM-DD>
```

Keep each bullet to one line. Link, don't restate.

**Show the draft to the user before writing it** — outcomes are the user's voice, not the agent's.

### Step 4 — Graduate the file

After the user approves the outcome section:

```bash
# Append the section to the plan file
# Then move it
mv docs/exec-plans/active/<plan>.md docs/exec-plans/completed/<plan>.md
```

### Step 5 — Update the index

Edit `docs/exec-plans/README.md`:
- Remove the row from the **Active** table
- Add a row to the **Completed** table with `<plan-name> | <YYYY-MM-DD> | completed/<plan>.md`

### Step 6 — Suggest follow-up

End the skill by saying one of:

- "Worth running `/review-harness` to check whether this phase introduced harness drift?" (if the phase touched architecture, dependencies, or core conventions)
- "Anything from this phase that's been hit ≥2 times? Run `/promote-lesson`." (if `docs/lessons.md` got new entries)
- Nothing, if neither applies.

---

## Anti-patterns

- ❌ **Writing the outcome section without user review** — outcomes are testimony, not invention. The agent drafts; the user approves.
- ❌ **Deleting the active file instead of moving it** — completed plans are searchable history. They're the harness's long-term memory.
- ❌ **Inventing pitfalls to fill the section** — if there were no real pitfalls, leave that block empty or write "none worth recording."
- ❌ **Updating the index without graduating the file** (or vice versa) — they must move in lockstep, or future sessions get a "ghost" row pointing to a missing file.
- ❌ **Auto-triggering `/review-harness`** — suggest, don't run. The user decides when to spend the audit cycles.
- ❌ **Touching files outside `docs/exec-plans/`** — finish-phase is narrow. Architecture updates belong to `/review-harness`.

---

## Sources

- [GitHub 2,500-repo AGENTS.md study](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/) — the "where are we now" finding
- [The Vibe Coding Hangover — dev.to](https://dev.to/paulthedev/the-vibe-coding-hangover-is-real-what-nobody-tells-you-about-ai-generated-code-in-production-399h) — the 20-30% sprint-capacity drain on unrecorded vibe-coded work
