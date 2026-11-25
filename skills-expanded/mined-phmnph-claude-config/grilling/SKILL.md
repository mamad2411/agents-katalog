---
name: grilling
description: Clarify an ambiguous plan or stress-test a proposed decision before implementation.
---

# Clarify the decision

Establish the intended outcome, meaningful constraints, and evidence of success.
Read relevant code and existing decisions before asking questions whose answers
are available there. Gather a small fact directly; delegate a bounded independent
investigation only when it usefully overlaps other work.

Choose routine implementation details yourself and explain consequential choices
through observable behavior. Ask the user about unresolved goals, behavior,
material tradeoffs, or authority that the repository cannot establish. Offer a
recommended answer with a reason. Reuse answers and authorization already given.

Ask the smallest useful batch of questions. Continue independent work while a
blocking answer is pending. If the user explicitly requests an exhaustive
interview, explore more branches; otherwise stop when remaining uncertainty no
longer changes the next step. Do not require the user to choose classes, patterns,
or test seams that you can responsibly select from the code.

Record the chosen direction, assumptions, acceptance criteria, and unresolved
material decisions. Use $domain-modeling only when terminology or durable design
records need changing. If implementation is authorized, continue into it once
blocking decisions are settled. If the request is planning-only, deliver the
plan without adding an extra confirmation round.
