---
description: Interview the author and write a goal.md sidecar that anchors a new skill from manual practice through harness-clean SKILL.md
---

# Purpose

The user invoked `/goal-new-skill $ARGUMENTS`. They want to anchor a not-yet-written skill with a measurable `/goal` condition so the work toward "skill exists and passes the harness" is driven by a verifiable end state, not vibes.

This command **does not write SKILL.md or tests.md**. Those come from manual practice runs — the skill-kit workflow codifies skills from real, hand-executed runs, never from imagination. This command writes a single artifact — `.claude/skills/<name>/goal.md` — and prints the `/goal` line for the user to invoke separately.

## Steps

1. **Parse the argument.**
   - `$ARGUMENTS` should be a kebab-case skill name in gerund form (e.g. `summarizing-prs`, `triaging-issues`).
   - If empty, ask: "What's the skill name? (kebab-case, prefer gerund form like `processing-pdfs`.)"
   - If it contains uppercase, spaces, or fails `^[a-z0-9-]+$`, push back and ask for a fix.
   - If the first hyphen-separated segment doesn't end in `-ing`, point that out (gerund-form names are the skill-kit convention; the check-skill harness warns otherwise) but accept the user's call.
   - Set `<name>` to the validated value for the rest of this run.

2. **Check for existing artifacts.**
   - If `.claude/skills/<name>/goal.md` already exists, read it and ask whether to overwrite, edit, or abort.
   - If `.claude/skills/<name>/SKILL.md` already exists, the skill is already authored — point that out and suggest `/skill-kit:goal-improve-skill` instead.

3. **Interview, one question per turn, in plain chat.** Wait for each answer before asking the next. Do NOT use AskUserQuestion — the answers are open-ended.
   - **Q1 (Task):** "In one sentence, action verb first: what concrete task should this skill perform? (Example: 'Summarize a GitHub PR diff into a 5-bullet changelog entry.')"
   - **Q2 (Verifiable success):** "What does a single successful run of that task produce that you can point at? Describe the output shape concretely. (Example: 'A fenced markdown block with exactly 5 bullets, each ≤120 chars, naming the changed top-level modules.')"
   - **Q3 (Three practice inputs):** "Name three distinct inputs you'll exercise the manual runs against. Aim for diversity — golden path, an edge case, and something weird (empty / malformed / oversized). Real inputs, not hypotheticals."
   - **Q4 (Out of scope):** "What is this skill explicitly NOT trying to do? List 1–3 anti-goals so the practice runs don't drift."

4. **Synthesize the `/goal` condition.** Build one string ≤4000 chars with the four parts the official `/goal` docs reward — end state, stated check, constraints, turn bound. Use this exact template, substituting answers:

   ```
   I have performed <task> manually on three distinct inputs: <input-1>, <input-2>, <input-3>. Each run is captured in .claude/skills/<name>/tests.md as a separate scenario with the actual input, the actual output, and a `Last verified: <today>` line at the top. .claude/skills/<name>/SKILL.md exists with frontmatter that has a third-person `description` covering both what the skill does and when to use it, and the body documents the workflow I just exercised. `check-skill .claude/skills/<name>` exits 0 with zero FAILs. The skill must NOT <anti-goals from Q4>. Or stop after 30 turns.
   ```

   Today's date comes from the `currentDate` system reminder.

5. **Write `.claude/skills/<name>/goal.md`** with the structure below. Create `.claude/skills/<name>/` if it doesn't exist (`mkdir -p`).

6. **Print the launch instructions** to the user — see Output section.

## goal.md structure

```markdown
# Goal — <name>

**Created:** <today's date>
**Workflow:** new-skill
**Target:** .claude/skills/<name>/

## End state

<one-sentence restatement of Q1 + Q2 — what "done" looks like>

## How Claude proves it

- `check-skill .claude/skills/<name>` exits 0
- `.claude/skills/<name>/tests.md` has ≥3 scenarios with a `Last verified` date, each capturing one practice run
- `.claude/skills/<name>/SKILL.md` has a third-person `description` field that includes both *what* and *when*

## Constraints

- Every kept iteration of SKILL.md must pass the harness with zero FAILs
- Practice runs must use the three inputs below, not invented ones
- tests.md scenarios must include actual outputs from real runs (no fabricated examples)

## Practice inputs

1. <input-1>
2. <input-2>
3. <input-3>

## Out of scope

- <anti-goal 1>
- <anti-goal 2>

## Synthesized /goal condition

```
/goal <full condition string>
```

## Interview transcript

- **Task:** <Q1 answer>
- **Verifiable success:** <Q2 answer>
- **Practice inputs:** <Q3 answer>
- **Out of scope:** <Q4 answer>
```

## Output

After writing the file, print verbatim:

```
Goal drafted: .claude/skills/<name>/goal.md

Run this in chat to start working toward it:

  /goal <synthesized condition>

The first practice run begins as soon as you invoke /goal. Edit goal.md and re-run /goal-new-skill if you want to refine first.
```

## Constraints

- Do NOT write SKILL.md, tests.md, or any other skill file. The goal anchors future work; it does not do that work.
- Do NOT invoke `/goal` yourself — slash commands cannot call other slash commands. Print the line so the user runs it.
- `/goal` is not part of this plugin or stock Claude Code — it comes from the user's own environment. If their environment has no `/goal` command, say so in the printed output and tell them the written goal.md serves as the acceptance checklist to work against manually.
- If the user's answers are too vague to synthesize a measurable condition (e.g. Q2 = "good output"), push back once with a specific request for concreteness before accepting.
