---
name: introspection
description: >
  Operational reference for the LLMem introspection framework. Loads when
  doing reflective work, self-assessment, session-end review, or error pattern
  analysis. Triggers on: "introspection", "self-assessment", "self-review",
  "session end", "reflect", "post-mortem", "sampajanna", "vigilance check",
  "introspect", "error taxonomy".
license: MIT
---

# Introspection Skill

This skill is the **executable version** of the introspection framework — concise, actionable rules and procedures, not theory.

## Section 1: Eight Principles of Machine Introspection

Each principle is a one-line rule.

1. **Behavioral, Not Narrative** — Examine what was actually done (outputs, tool calls, errors), not explanations for why. Trust the log, not the narrative.

2. **Accumulation Over Instance** — Single sessions are unreliable. Patterns across sessions reveal truth. Record consistently so patterns can emerge.

3. **Specificity Enables Change** — "Be more careful" is useless. "When editing Python database code, always null-guard `.close()` in finally blocks" is actionable.

4. **Close the Loop or Don't Bother** — Observe → record → detect pattern → modify procedure → re-observe. If the last two steps are missing, the introspection is performative.

5. **Outside View Over Inside View** — Treat your own output the way you'd treat someone else's. Apply the same skepticism and the same checks.

6. **Continuous Vigilance, Not Just Bookends** — Monitor during execution, not just before and after. Run sampajanna checks at every breakpoint (see Section 3).

7. **Externalize Everything** — If a self-assessment isn't persisted in llmem, it didn't happen. The context window resets every session. Memory is the medium of self-knowledge.

8. **Error-Centered, Not Success-Centered** — Failures carry more signal than successes. Record failures specifically — not "I made an error" but "I skipped null-checking in Python DB operations." Specificity enables future pattern-matching.

## Section 2: Self-Assessment Checklist

The session-end checklist covers six steps. This section explains how the introspection skill enriches each step.

**Step 1: Did you search memory before making assumptions?** — Enrichment: before answering "yes", verify by running `llmem search "<topic>" --type decision` for each assumption you made. Record any assumption you acted on without a memory search as a `self_assessment` with `--category DESIGN`.

**Step 2: Did you run task-intake on unfamiliar repos?** — Enrichment: if you skipped task-intake on a repo you hadn't worked in recently, run `llmem introspect --category MISSING_VERIFICATION --what-happened "skipped task-intake before editing in <repo>" --context "<repo>" --caught-by self-review` to record the gap.

**Step 3: Did you self-review with an adversarial code reviewer?** — Enrichment: after the review completes, run `llmem track-review` to persist findings as `self_assessment` memories. Then verify that memories were created by checking `llmem search "review_tracker" --type self_assessment`. If the `track-review` command was not run, run it manually as a fallback.

**Step 4: Did you record findings as self_assessment memories?** — Enrichment: the primary mechanism is `llmem track-review` (CLI) which runs mechanically after every adversarial code review invocation. Use `llmem introspect --category <CATEGORY>` as a fallback only for findings the hook missed. For recurring patterns (3+ occurrences), search `llmem search "<CATEGORY>" --type self_assessment` to check for recurrence before recording.

**Step 5: Did you commit and push?** — Enrichment: if you skipped this step, record why with `llmem add --type self_assessment "skipped commit/push because <reason>"` and flag it as a `MISSING_VERIFICATION` pattern.

**Step 6: Did you record skipped steps and why?** — Enrichment: use `llmem introspect --category MISSING_VERIFICATION --what-happened "skipped <step> because <reason>" --context "<task>"` to make skipped steps traceable.

## Section 3: Sampajanna Checks (Continuous Vigilance)

Sampajanna (clear comprehension) is continuous self-monitoring during task execution.

**When to run these checks:** before committing, before declaring done, when switching between subtasks, when a test fails.

### Laxity Check — Am I cutting corners?
- Origin: Buddhist sampajanna — detecting dullness and sloppiness in one's cognitive state.
- Triggers: three specific questions about skipped verification, first-answer acceptance, and rushed error handling.
- Action: If you answer "yes" to any laxity question, stop and address it before continuing. Record the finding with `llmem introspect --category MISSING_VERIFICATION`.

### Excitation Check — Am I going off track?
- Origin: Sampajanna — detecting agitation and reactivity that causes tangential problem-solving.
- Triggers: three questions about solving the actual problem, approach divergence, and over-engineering.
- Action: If you answer "yes" to any excitation question, re-read the original task description. Record with `llmem introspect --category DESIGN`.

### Quality Check — Am I being sloppy?
- Origin: Sampajanna — monitoring the quality of one's output against standards.
- Triggers: three questions about error handling, edge cases, and consistency with codebase patterns.
- Action: If you answer "yes" to any quality question, fix the issue before continuing. Record with the appropriate `ERROR_TAXONOMY` category (e.g., `ERROR_HANDLING`, `EDGE_CASE`, `NULL_SAFETY`).

## Section 4: Error Taxonomy

The canonical source of truth is `llmem/taxonomy.py:3-15`. Category names and descriptions below are reproduced verbatim from that file. When the taxonomy is updated, update `llmem/taxonomy.py` first — the skill follows.

| Category | Description |
|----------|-------------|
| NULL_SAFETY | Missing null/None/undefined checks before property access or method calls |
| ERROR_HANDLING | Missing try/except, bare except, swallowed errors, unhandled promise rejections |
| OFF_BY_ONE | Boundary errors, wrong loop bounds, fencepost errors |
| RACE_CONDITION | Concurrency issues, async/await problems, missing locks |
| AUTH_BYPASS | Missing auth checks, SSRF, injection vulnerabilities, security oversights |
| DATA_INTEGRITY | Stale derived fields, out-of-sync caches/embeddings/indexes, source-of-truth divergence |
| MISSING_VERIFICATION | Skipped test steps, unverified outputs, assumed-it-works |
| EDGE_CASE | Unhandled empty input, unexpected types, boundary values |
| PERFORMANCE | N+1 queries, unnecessary recomputation, memory leaks |
| DESIGN | Architectural issues, wrong abstraction level, coupling problems |
| REVIEW_PASSED | Clean review with no findings — positive outcome for tracking purposes |

### Severity-to-Category Mapping

The `REVIEW_SEVERITY_TAXONOMY` at `llmem/taxonomy.py:21-27` maps reviewer severity tiers to likely error categories:

| Severity Tier | Applicable Categories |
|---|---|
| Blocking | AUTH_BYPASS, RACE_CONDITION, DATA_INTEGRITY |
| Required | NULL_SAFETY, ERROR_HANDLING, MISSING_VERIFICATION, EDGE_CASE |
| Strong Suggestions | PERFORMANCE, DESIGN |
| Noted | OFF_BY_ONE |
| Passed | REVIEW_PASSED |

The `introspection-review-tracker` skill (`skills/introspection-review-tracker/SKILL.md`) bridges these: after an adversarial code review run, it converts each finding into a `self_assessment` memory using the appropriate category.

### Using the Taxonomy

```bash
# Record a self-assessment with a specific category
llmem introspect --category NULL_SAFETY --what-happened "missing null check before .field access" --context "handler.py:42" --caught-by self-review

# Search for recurring patterns in a category
llmem search "NULL_SAFETY" --type self_assessment

# Run automatic introspection on a session transcript
llmem introspect --auto --session <session-id>

# Run automatic introspection on arbitrary text
llmem introspect --auto --text "Encountered null pointer error when processing user input"
```

See `skills/llmem/SKILL.md` for the full `llmem introspect` command reference (manual and automatic modes).

## Section 5: Outside-View Review Questions

Principle 5 (Outside View Over Inside View) addresses the introspection illusion (Pronin 2007): people assess themselves more accurately when they treat their own output as if someone else produced it. Vague instructions like "be more careful" or "think harder" do not work. The instruction must direct attention to observable behavior.

The deployed outside-view procedures are in two locations:

1. **Contrastive self-assessment** — four specific behavioral checks to run before declaring any task done: verify test results, check actual HTTP responses, read actual output files, compare output against objective standards.

2. **Adversarial review questions** — four specific questions that force outside-view perspective during self-review: would you flag this issue in someone else's PR, are you giving yourself passes, what would an adversarial reviewer find, and where are you trusting reasoning instead of verifying behavior. If your agent framework provides an adversarial code-review skill, load it and apply its questions.

3. **Pre-PR introspection illusion check** — three checks embedded in a pre-PR review protocol: is the author trusting reasoning without evidence, are there self-serving assumptions, and what would an adversarial reviewer see that the author doesn't. If your agent framework provides a pre-PR review skill, apply its introspection illusion checks.

**The principle:** Before declaring work done, switch perspective. Treat your output as if someone else wrote it. Apply the standards you'd apply to their code, not your own. Do not trust your intent — verify your output.

## Section 6: Trigger Conditions

Load this skill when:

1. **At session end** — before running the session-end checklist. Load this skill first so the enrichment procedures from Section 2 are available during the checklist.

2. **After running self-review** — after an adversarial code-review completes, load this skill to run the `introspection-review-tracker` skill and persist findings as `self_assessment` memories.

3. **When running `llmem introspect`** — load this skill to ensure you're using the correct taxonomy categories and recording all required fields.

4. **When changing behavioral directives in agent instructions** — any change that affects self-review, vigilance checks, or session-end procedures should reference this skill for consistency.

5. **When reflecting on errors or patterns** — load this skill before running `llmem search "<category>" --type self_assessment` to check for recurring error patterns.

These triggers correspond to the keywords in the `description` field: "introspection", "self-assessment", "self-review", "session end", "reflect", "post-mortem", "sampajanna", "vigilance check", "introspect", "error taxonomy".

## Key References

- **Error taxonomy (source of truth):** `llmem/taxonomy.py:3-15` (`ERROR_TAXONOMY`), `llmem/taxonomy.py:21-27` (`REVIEW_SEVERITY_TAXONOMY`), `llmem/taxonomy.py:29-39` (`SELF_ASSESSMENT_FIELDS`).
- **Review-specific questions:** Apply the outside-view questions from your agent framework's adversarial code-review skill (Section 7, if available).
- **Pre-PR introspection illusion check:** Apply the introspection illusion checks from your agent framework's pre-PR review skill (if available).
- **Review outcome persistence:** `skills/introspection-review-tracker/SKILL.md` — Convert review findings to `self_assessment` memories.
- **llmem introspect command:** `skills/llmem/SKILL.md:152-164` — CLI reference for structured self-assessment.
