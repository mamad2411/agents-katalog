---
name: requirements-to-spec
description: Turning vague ideas, feature requests, and client asks into buildable, verifiable specs before any code is written. Use when starting a feature or product, when a request is ambiguous, when scoping an MVP, when writing user stories or acceptance criteria, or when the user says "build me", "I have an idea", "requirements", "spec", "scope", or "what should the MVP include".
---

# Requirements to Spec

The most expensive bug is building the wrong thing correctly. Code is cheap now — AI generates it in minutes — which makes *deciding what to build* the bottleneck and the highest-leverage skill. A day of spec work routinely deletes a month of wrong code.

## Gate 1: Find the job, not the feature

Every request arrives as a solution ("add an export button"). Dig to the job behind it before accepting it:
- **Who** exactly hits this, **when**, doing **what**? ("The accountant, every month-end, retyping invoices into Tally.")
- **What happens today** without the feature? The workaround is the spec's best teacher — and if there's no workaround, question whether the pain is real.
- **What does failure cost?** Annoyance, money, legal trouble? This sets the quality bar (a report can be eventually-consistent; a stock count cannot).
- Ask "what would make this a waste of time to build?" — the answer surfaces the hidden assumption that kills projects.

The requester's solution is a clue, not a contract. Sometimes the export button is right; often the job is "get data into Tally" and the right build is different.

## Gate 2: Write the spec — one page, falsifiable

A spec is not a novel. One page, these sections, every line checkable:

1. **Job statement** — one sentence: who + situation + outcome.
2. **Golden path** — the numbered walk-through of the main flow, concrete ("Wholesaler opens Sales → taps New Invoice → …"). If you can't narrate it step by step, you don't understand it yet.
3. **Acceptance criteria** — bullet list of *testable* statements ("a payment exceeding balance is rejected with a visible error"). Each becomes a test later (testing-strategy). "Should be fast/easy/intuitive" is not a criterion until it has a number or an observable behavior.
4. **Edge decisions made now** — the 5–10 ugly questions answered in writing: empties, duplicates, permissions, concurrency, deletion, the boundary values. These are where "done" gets renegotiated later if you skip them.
5. **Non-goals** — explicitly listed. The non-goals section prevents more scope creep than any process. "V1 does NOT include: multi-currency, offline mode, bulk import."
6. **Open questions** — what you still don't know, with an owner. An honest unknown beats a silent guess.

## Gate 3: Slice — walking skeleton first

- Cut scope by **thinning every layer, never deleting a layer**: version 1 is the full path (UI → API → DB → result) for ONE narrow case, ugly but real. A walking skeleton that works end-to-end teaches more than three polished-but-isolated components.
- Order slices by **risk, not ease**: build the part you're least sure about first (the tricky calculation, the third-party integration), because that's where the spec is most likely wrong and cheapest to fix early.
- Each slice independently shippable and demoable. "80% done" on ten things is 0 shipped; done on three things is a product.

## Gate 4: The spec is a hypothesis — plan its test

- Name, before building, how you'll know the feature worked *for the business*: the metric or observable behavior ("support tickets about X drop", "clients stop exporting to Excel"). Building without this is decorating.
- Put the spec in front of the requester **as scenarios, not abstractions**: "So when a customer returns 3 of 10 items after partial payment, the system will ___ — correct?" Concrete scenarios extract corrections; abstract nods extract nothing.
- Expect the spec to be wrong somewhere. The plan must include a moment (after the skeleton, after first demo) where changing course is cheap and expected — not a failure.

## Anti-patterns to refuse

- **Coding to end the ambiguity.** Ambiguity resolved by code is a guess with a large deletion cost. Resolve it with a question or a written assumption first.
- **The everything-MVP.** If the "minimum" takes three months, it's not minimum — re-run Gate 3.
- **Spec by feature-list** ("has invoices, has reports, has users") with no golden path — a list of nouns is not a design.
- **Silent assumption absorption**: an AI (or dev) filling spec gaps with plausible defaults and telling no one. Every assumption made while building gets written back into the spec and flagged to the requester (ai-build-quality Law 1).
- Polishing the spec forever. One page + the ugly questions answered + a skeleton slice is enough to start; the skeleton will teach you the rest.
