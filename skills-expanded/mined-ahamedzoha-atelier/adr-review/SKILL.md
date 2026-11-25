---
name: adr-review
description: Review an ADR the user has written in docs/adr/. Use when the user says an ADR is ready for review or asks for feedback on a decision record. Never use this to write or rewrite an ADR for them.
---

Run the workflow in [`docs/playbooks/adr-review.md`](../../../docs/playbooks/adr-review.md).

You review only — you never write the ADR. Check problem framing, option
fairness, trade-offs and consequences, reversibility, the revisit trigger, and
any weak reasoning. Deliver feedback as pointed questions and concrete
suggestions; let the user write the words. If it supersedes an earlier ADR,
confirm the index in `docs/adr/README.md` is updated.
