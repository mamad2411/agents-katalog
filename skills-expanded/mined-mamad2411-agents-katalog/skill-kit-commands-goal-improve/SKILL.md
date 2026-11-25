---
description: Interview the user and write a goal.md sidecar that anchors an improving-skills run against an existing SKILL.md with measurable targets
---

# Purpose

The user invoked `/goal-improve-skill $ARGUMENTS`. They want a measurable `/goal` condition for an autoresearch run against an existing SKILL.md, so the loop stops on real progress rather than only on the default iteration cap or stuck threshold.

This command writes one artifact — `<skill-dir>/goal.md` — and prints the `/goal` line plus the `/skill-kit:improving-skills` follow-up for the user to invoke.

## Steps

1. **Parse the argument.**
   - `$ARGUMENTS` should be a path to a SKILL.md or its containing directory (e.g. `.claude/skills/foo` or `.claude/skills/foo/SKILL.md`).
   - Normalize to `<skill-dir>` (the directory containing SKILL.md).
   - If empty or path doesn't exist, ask: "Which SKILL.md? Give me a path like `.claude/skills/<name>` or `.claude/skills/<name>/SKILL.md`."

2. **Verify prerequisites** — `improving-skills` requires all three before it will run:
   - `<skill-dir>/SKILL.md` exists
   - `<skill-dir>/tests.md` exists with ≥3 `## ` scenario headings
   - `<skill-dir>/test-prompts.md` exists and is non-empty
   
   If any are missing, stop and tell the user exactly which file to create. Do not proceed.

3. **Inspect current state** to inform the interview:
   - Read SKILL.md. Compute a rough token estimate (word count × 1.3 is fine — this is for the suggestion, not a contract).
   - Check whether `.skill-kit/runs/` exists for previous improving-skills runs on this skill. If so, mention the most recent run's results.tsv so the user can pick a target relative to known scores.
   - If `<skill-dir>/goal.md` already exists, read it and ask whether to overwrite.

4. **Interview, one question per turn.** Use plain chat for freeform answers; you MAY use AskUserQuestion for Q1 since it's a closed choice.
   - **Q1 (Primary axis):** Which is the main improvement axis?
     - Tighter triggers (raise trigger accuracy on `test-prompts.md`)
     - Smaller body (reduce token count without quality loss)
     - Sharper instructions (raise quality scores on `tests.md` scenarios)
     - Progressive disclosure (move detail into supporting files)
     - Other (let user describe)
   - **Q2 (Numeric target):** "What concrete number marks success? Examples: `tokens ≤ 600`, `composite ≥ 0.85`, `trigger accuracy = 1.0 on positive prompts`, `body ≤ 150 lines`. Give one number tied to the axis from Q1." Note the current baseline (tokens or whatever applies) in your question so they pick a meaningful delta.
   - **Q3 (Behavior to preserve):** "What must NOT change? At minimum, every positive prompt in `test-prompts.md` must still fire. Anything else — a specific section, a tone, a code example?"
   - **Q4 (Iteration cap):** "Default cap is 20 iterations (the loop's `eval.json` default). Accept default or override?"

5. **Synthesize the `/goal` condition.** Build one string ≤4000 chars with end state, stated check, constraints, turn bound. Template:

   ```
   The improving-skills loop on <skill-dir>/SKILL.md has produced a kept iteration whose row in .skill-kit/runs/<run-id>/results.tsv shows <numeric target from Q2>. The most recent kept iteration's harness column is PASS. All rows marked positive in <skill-dir>/test-prompts.md still fire under the candidate's description (trigger accuracy on positive prompts = 1.0). <Behavior-preservation constraints from Q3>. Or stop after <Q4 cap> iterations or 5 consecutive iterations with no score improvement.
   ```

6. **Write `<skill-dir>/goal.md`** with the structure below.

7. **Print the launch instructions** — see Output section.

## goal.md structure

```markdown
# Goal — improve <skill-name>

**Created:** <today's date>
**Workflow:** improving-skill
**Target:** <skill-dir>/SKILL.md
**Baseline tokens:** <rough estimate from step 3>

## End state

<one-sentence restatement: axis from Q1 + numeric target from Q2>

## How Claude proves it

- A row in `.skill-kit/runs/<run-id>/results.tsv` with `kept=yes` shows the target metric
- That row's `harness` column is `PASS`
- The candidate's description still fires every positive prompt in `<skill-dir>/test-prompts.md`

## Must not change

- <each Q3 item>
- All kept iterations pass `check-skill` with zero FAILs

## Iteration cap

<Q4 cap> iterations, or 5 consecutive iterations without improvement.

## Synthesized /goal condition

```
/goal <full condition string>
```

## Interview transcript

- **Primary axis:** <Q1 answer>
- **Numeric target:** <Q2 answer>
- **Behavior to preserve:** <Q3 answer>
- **Iteration cap:** <Q4 answer>
```

## Output

After writing the file, print verbatim:

```
Goal drafted: <skill-dir>/goal.md

Run these two in chat to launch the run with the goal active:

  /goal <synthesized condition>
  /skill-kit:improving-skills <skill-dir>/SKILL.md

The improving-skills loop will see <skill-dir>/goal.md and can seed .skill-kit/runs/<run-id>/program.md from it.
```

## Constraints

- Do NOT start the improving-skills loop yourself — print the lines for the user.
- `/goal` is not part of this plugin or stock Claude Code — it comes from the user's own environment. If their environment has no `/goal` command, say so in the printed output and tell them the written goal.md serves as the acceptance checklist to work against manually.
- Do NOT modify SKILL.md, tests.md, or test-prompts.md.
- Do NOT invent baseline numbers. If the token estimate is rough, say so.
- If the user's numeric target in Q2 is unmeasurable from the conversation (e.g. "make it feel sharper"), push back once for a concrete metric the `/goal` evaluator can judge.
