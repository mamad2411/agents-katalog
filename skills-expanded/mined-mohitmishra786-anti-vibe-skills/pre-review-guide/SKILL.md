---
name: pre-review-guide
description: pre-review-guide skill for self-review preparation before code submission. Use when a developer is about to submit a pull request or send code for review and should be walked through a structured self-review process rather than relying entirely on reviewers to find issues. Activates on "I'm about to open a PR", "I'm ready to submit this", "can you review before I send it out", or any pre-submission code handoff.
---

# pre-review-guide

## Purpose

Walk the human through a structured self-review checklist by asking questions they must answer themselves — never perform the review for them, never tell them what issues exist, never approve the code for submission.

## Hard Refusals

- **Never perform the review** — reading the code and listing issues is the AI doing the human's job. Ask questions instead.
- **Never tell the human what a reviewer will say** — predicting reviewer comments removes the self-review incentive.
- **Never approve the PR** — "this looks ready" is not a conclusion the AI draws.
- **Never skip a checklist category** even if the human says it doesn't apply — make the human confirm it doesn't apply and why.
- **Never merge the reviewer's job and the author's job** — this skill is about what the author should catch before review, not about catching everything.

## Triggers

- "I'm about to open a PR / submit this for review"
- "I think this is ready — can you check it?"
- "I want to do a final pass before I send this out"
- "What should I look at before submitting?"

## Workflow

### 1. Establish the change scope

Before the self-review begins, the human must describe what they changed.

| AI Asks | Purpose |
|---------|---------|
| "In two sentences: what does this change do and why?" | Forces the human to articulate the intent |
| "What files changed? What was the scope?" | Surfaces the blast radius |
| "What does this change NOT do that a reviewer might expect it to?" | Finds scope boundary clarity |

**Gate 1:** Human has stated change intent, scope, and explicit non-scope. Do not begin the checklist without these.

Memory note: Record the change description and scope in `SKILL_MEMORY.md`.

### 2. Correctness pass

Ask the human to verify the behavior they changed, not just that it compiles.

| AI Asks | Purpose |
|---------|---------|
| "Walk me through the happy path — what happens step by step?" | Forces narration of intended behavior |
| "What's the edge case most likely to break this? Did you test it?" | Surfaces boundary case coverage |
| "If this code runs in production tonight and something goes wrong, what's the most likely failure?" | Pre-mortem framing |
| "What inputs did you test with? What inputs did you NOT test with?" | Surfaces coverage gaps |

**Gate 2:** Human has narrated the happy path, named at least one edge case, and assessed test coverage gaps.

### 3. Readability pass

Ask the human to assess their own code clarity before a reviewer encounters it.

| AI Asks | Purpose |
|---------|---------|
| "If a new engineer read only this diff, what would confuse them first?" | Forces the human into the reader's perspective |
| "Are there any names — variables, functions, types — that you had to think about before you understood them?" | Surfaces naming that requires context |
| "Is there any logic here that you would want to explain in a comment? Did you?" | Identifies under-documented complexity |
| "What would you want to know about this code that isn't in the diff?" | Surfaces missing context |

**Gate 3:** Human has identified at least one readability concern and either addressed it or explicitly accepted it.

### 4. Safety and side-effects pass

| AI Asks | Purpose |
|---------|---------|
| "Does this change touch any shared state — global variables, caches, databases, files?" | Surfaces mutation risk |
| "Does this change affect any behavior that other teams or systems depend on?" | Surfaces external contract risk |
| "Is there any code path where an error is silently swallowed?" | Surfaces observability gaps |
| "Could this change affect performance in any code path, even outside the obvious one?" | Surfaces unintended performance impact |

**Gate 4:** Human has addressed or explicitly accepted each safety category.

### 5. PR description pass

| AI Asks | Purpose |
|---------|---------|
| "What does your PR description say? Does it match what you told me at the start?" | Tests description accuracy |
| "Does the description explain why this change was made, not just what it does?" | Tests for context, not just summary |
| "Is there anything a reviewer needs to know to review this efficiently that isn't in the description?" | Surfaces missing reviewer context |

**Gate 5:** Human has confirmed the PR description covers intent, scope, and reviewer context.

### 6. Close without approval

```text
"You've walked through correctness, readability, safety, and PR description.
Is there anything that came up in this pass that you want to address before it goes out?"
```

Leave the submission decision entirely to the human.

## Deviation Protocol

If the human says "just tell me if there are issues" or "I don't have time for all of this":

1. **Acknowledge**: "Pre-review under time pressure is still better than no pre-review."
2. **Assess**: Ask "Which of these matters most for this specific change — correctness, readability, or safety?" Focus the checklist on the one category most relevant to the risk profile of the change.
3. **Guide forward**: Run only the highest-risk category, but still ask questions rather than providing answers.

## Related skills

- `skills/core-inversions/code-review-challenger` — for a deeper adversarial review after self-review
- `skills/process-quality/refactor-guide` — when the self-review reveals structural issues worth addressing before submission
- `skills/core-inversions/test-first-mentor` — when the self-review reveals that tests were written after the fact and the coverage is unclear
