---
name: cyc-teach
description: "Teach a concept through the learner's own project with a plain definition, a worked example from their code, and a small practice task. Use when the user says \"explain\", \"teach me\", \"help me understand\", \"why does this work\", or is a student or newer developer learning while building."
---

# Teach through the real work

Aim for understanding the learner can use elsewhere, not a longer answer. Follow the [handoff contract](../../docs/skill-contract.md).

This method is for a requested lesson or practice. Ordinary implementation already includes explanations through the shared [engineering understanding standard](../../docs/response-standard.md#engineering-understanding-throughout-the-work); do not require a separate teaching playbook, quiz, or learner response to provide them.

## The core loop

1. **Find the starting point from what they said.** Their wording, their code, and past questions show their level. Don't give a placement quiz. If it's genuinely unclear, ask one question.
2. **Define it plainly first.** One or two sentences with no jargon they haven't seen. "State is the data your app remembers between clicks."
3. **Tie it to their code immediately.** Show where the concept lives in *their* project, with the file and line. Read the code first; never teach from an imagined version of it.
4. **Build the picture in steps.** For a flow, draw A → B, then add C, then the return path. Do not start with the full diagram.
5. **Show one decision and its tradeoff.** "We saved to localStorage because the app has no accounts. The cost: it doesn't sync across devices." This is where understanding forms.
6. **Give the smallest complete answer, then stop.** Offer to go deeper; don't pre-empt it.
7. **Offer one practice task on a nearby variation.** "Now make the *delete* button update the count the same way." Give hints in steps if they ask. Provide the solution when asked.
8. **Check transfer, not recall.** Ask them to predict what happens in a new case ("What if two tabs are open?") rather than repeat the definition.

## Done when

The explanation is correct, grounded in files you read, and pitched at their level, and practice is offered. Learning is only shown by the learner's own attempt or prediction. Delivering a lesson doesn't prove it landed; say so if no attempt was made.

## Anti-patterns

| Name | The tell | Fix |
| --- | --- | --- |
| Jargon cascade | Explaining a term with three new terms | Define with words they already use |
| Generic example | A textbook "foo/bar" example | Use their project |
| Lecture | Five paragraphs before any code | Definition, then their code, then stop |
| Drama framing | "Here's the key insight", "this is the tricky part" | Just say it |
| Solving their practice | Writing the solution before they try | Hint in steps unless they ask |
| Invented voice | Presenting AI-written advice as the project creator's teaching | Label who wrote it; only use reviewed material as theirs |

## Handoff

Return the explanation, the practice task, and what was actually assessed (for example, "the learner predicted the two-tab case correctly" or "no attempt yet"). If the learner needs to respond before continuing, return blocked on their participation.
