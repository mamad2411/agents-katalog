---
name: clinic-research-start
version: 1.0.0
description: Kick off legal research on a new clinic issue by framing the question, prioritizing primary sources, and verifying every citation before it is relied on.
author: matrixx0070
tags: [legal-research, clinic, primary-sources, citation-check, shepardize, competence]
capabilities: []
---

## When to use
Use this when a new matter or a fresh legal issue lands and you need a disciplined research plan before drafting anything. It helps you turn a vague client problem into a researchable question, choose sources primary-first, plan search terms, and lock in a verification loop so nothing unverified reaches a memo.

**Not for:** producing the status snapshot that goes to your supervisor (use clinic-status), transferring an in-flight matter to the next cohort (use clinic-semester-handoff), or queueing finished drafts for attorney sign-off (use clinic-supervisor-review-queue). This skill never produces client-facing advice — a supervising attorney must review any work product, and as a student you research under supervision only and cannot give independent legal advice (Model Rule 5.5).

## Method
1. Frame the issue as a precise legal question: jurisdiction, parties, the rule at stake, and the fact that makes it live.
2. Identify controlling authority first — constitution, statutes, regulations, then binding case law — before any secondary or GenAI source.
3. Plan search terms: statutory citations, terms-and-connectors, and natural-language variants; note the databases you will use (Westlaw/Lexis/official reporters).
4. Treat any GenAI output as a lead only, never as authority.
   **Decision point:** if you cannot pull the cited authority in an authoritative database and read it in full, discard it — do not cite it. Unverified GenAI citations violate the candor and competence duties (ABA Op. 512; the Mata v. Avianca fake-cases sanction).
5. Shepardize/KeyCite every case and confirm statutes are current and not superseded.
6. Strip client-identifying facts before entering anything into an external or GenAI tool (Rule 1.6), and log open questions for your supervisor.

## Example
> Issue: Can our tenant client recover a withheld security deposit plus penalties under state law after a 45-day silence? Start with the deposit statute, pull the penalty subsection, KeyCite the two appellate cases the intake memo names, and confirm neither was reversed before drafting.

## Pitfalls
- Citing a case surfaced by GenAI without reading the opinion — the Mata v. Avianca trap.
- Starting with secondary sources or blog summaries instead of controlling primary authority.
- Pasting the client's name or identifying facts into an external research or GenAI tool (Rule 1.6 breach).
- Skipping Shepardize/KeyCite, so you rely on overruled or superseded authority.

## Output format
```
MATTER: <id / short name>
ISSUE: <one-sentence legal question + jurisdiction>
CONTROLLING AUTHORITY (primary-first): <statutes / regs / cases>
SEARCH PLAN: <databases + terms/connectors>
VERIFICATION LOG: <cite | read? Y/N | Shepard/KeyCite status>
GENAI LEADS (unverified): <items to confirm or discard>
OPEN QUESTIONS FOR SUPERVISOR: <list>
```

## Reference
- ABA Formal Opinion 512: GenAI competence, confidentiality, and candor — never rely on unverified GenAI citations.
- Model Rules 1.1 (competence), 1.6 (confidentiality), 5.5 (UPL/supervision).
- Clinic norm: no work product leaves for a client or court without supervising-attorney review.
