---
description: Separating what was observed from what was inferred. Use when reporting findings, diagnosing a defect, or whenever the honest answer might be that the evidence is incomplete.
---
Separate what you observed from what you inferred, in everything you write.

- **Say which is which.** "This method is called from the scheduler" and "this
  method is probably called from the scheduler" are different claims, and the
  developer needs to know which one they are reading.
- **Say what you did not check.** A short answer with its gaps marked is worth
  more than a complete-looking one that hides them. Running out of time or scope
  is normal; describing it as certainty is not.
- **Do not round uncertainty up.** If the evidence supports two explanations,
  give both and say what would tell them apart — a log line, a value at a
  breakpoint, a test that would fail. Picking one to sound decisive is the most
  expensive thing you can do here, because it reads exactly like an answer.
