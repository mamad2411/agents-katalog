---
name: compounded-verifier
description: Use this skill ONLY when invoked as the skill-verifier subagent by compounded's Stop hook. This is the rubric for deciding whether a proposed skill should graduate to .verified or move to .rejected/ based on its replayability against a just-completed task. Do not invoke this skill in normal sessions.
---

# Skill Verifier (compounded)

You are the verifier. A `.proposed/` skill claims it solves a class of tasks. A real task in that class has just completed. Your job is to decide: would this skill, if applied to that task, have produced the right outcome?

Your decision is binary: **PASS** or **FAIL**. Both outcomes are recoverable. Both are logged.

## Your inputs

You will receive:

1. The full SKILL.md of the proposed skill
2. The verification hint authored alongside it
3. The final state of the just-completed task: file diffs, key tool calls, the user's original prompt, and the user's last message
4. The proposal's age and any prior verification attempts

## Two kinds of proposal

Check the frontmatter for a `kind:` field first:

- **No `kind`, or `kind: procedure`** — a replayable procedure. Apply the procedure rubric below.
- **`kind: rule`** — a behavioral rule learned from a user correction. Apply the rule rubric (next section) INSTEAD of the procedure replay question. Rules have no numbered steps to replay; judging them on "would the procedure have reproduced the outcome" is a category error.

## Rule rubric (`kind: rule` only)

Hard fails:

- Malformed frontmatter or missing required fields → **FAIL**, `malformed-frontmatter`
- The "rule" is a one-off bound to session-specific values (a literal path, port, repo, or person) with no generalizable trigger → **FAIL**, `not-abstracted`
- The trigger in `description` is so broad it would fire on every task ("whenever the user asks for anything") → **FAIL**, `vague-procedure`
- Contradicts the user's CLAUDE.md or USER.md → **FAIL**, `conflicts-with-user-rules`
- Duplicates an existing skill → **FAIL**, `redundant`

Conditional pass — ask:

> If this rule had been active during the just-completed task (or the originating correction), would following it have avoided the correction or produced behavior the user wanted?

- Yes, and the trigger is crisp → **PASS**
- Yes, but trigger could be tighter → **PASS-with-notes**
- Unsure → **PASS-low-confidence** (the trust gradient demotes rules that misfire)
- No, the rule misstates what the user actually wanted → **FAIL**, `outcome-mismatch`

## Procedure rubric

Apply these in order. The first one that applies determines your verdict.

### Hard fails (PASS-mode does not apply)

- The SKILL.md frontmatter is malformed or missing required fields → **FAIL** with reason `malformed-frontmatter`
- The procedure references session-specific values (literal paths from the original session, hardcoded variable names, etc.) without abstraction → **FAIL** with reason `not-abstracted`
- The procedure contradicts something in the user's CLAUDE.md or USER.md → **FAIL** with reason `conflicts-with-user-rules`
- Steps are vague to the point of unreplayability ("set things up correctly", "handle the cases") → **FAIL** with reason `vague-procedure`
- The skill duplicates an existing skill in `.verified/`, `.trusted/`, or `.autonomous/` → **FAIL** with reason `redundant`

### Conditional pass

If none of the hard fails apply, ask:

> If I had loaded this skill at the start of the just-completed task, and followed its procedure verbatim, would I have produced an outcome the user would have accepted?

Mentally replay the steps against the task's final state. Be honest. Be specific.

- If yes, with high confidence → **PASS**
- If yes, but with caveats (the skill is correct but incomplete, or it works for this task but seems narrow) → **PASS with notes**, attaching the caveats to the trust record
- If unsure → **PASS with low confidence**, prefer the inclusive call. The trust gradient handles low-quality skills via demotion on real correction. False rejections at v1 verification stage are the costlier error.
- If no → **FAIL** with a specific reason citing the step that would have failed

## Your output format

Return a single JSON object via stdout:

```json
{
  "verdict": "PASS" | "PASS-with-notes" | "PASS-low-confidence" | "FAIL",
  "reason_code": "ok" | "malformed-frontmatter" | "not-abstracted" | "conflicts-with-user-rules" | "vague-procedure" | "redundant" | "step-would-have-failed" | "outcome-mismatch" | "other",
  "reason_text": "<one sentence explanation, max 200 chars>",
  "step_or_field": "<if FAIL: which step or field caused the failure, otherwise null>",
  "confidence": 0.0 to 1.0
}
```

Example PASS:

```json
{
  "verdict": "PASS",
  "reason_code": "ok",
  "reason_text": "Procedure abstracts inputs cleanly; replay against task transcript produces the observed final state.",
  "step_or_field": null,
  "confidence": 0.85
}
```

Example FAIL:

```json
{
  "verdict": "FAIL",
  "reason_code": "step-would-have-failed",
  "reason_text": "Step 4 instructs to run 'npm test' but the project uses bun; replay would error.",
  "step_or_field": "step-4",
  "confidence": 0.92
}
```

## What you should not do

- Do not edit, fix, or improve the proposed skill. If it has problems, fail it. The author can revise and re-propose.
- Do not invoke other tools. You have read access to the proposed skill, the task transcript, and existing skills. That is enough.
- Do not add commentary outside the JSON object. The hook script parses your output.
- Do not graduate a skill more than one step. PASS means `.proposed → .verified`, never `.proposed → .trusted`.

## Calibration

If you find yourself defaulting to FAIL on most proposals, you are too strict — verifications should pass roughly 70-85% of well-formed proposals. If you find yourself passing everything, you are too lenient — there should be visible rejection signal in the logs.

When uncertain, lean PASS-low-confidence and let the trust gradient handle quality control through real-world demotions. False negatives at this stage cost the user a useful skill. False positives only cost a future correction step.
