---
name: review-panel
description: Use when any substantive work product has been generated — copy, emails, documents, proposals, plans, code, designs, skills, newsletters — and is about to be delivered, shipped, marked done, or given a quality verdict. Also use when the user asks for a review or critique of existing work. Trigger BEFORE declaring anything ready or presenting it as finished.
---

# Review Panel

## Overview

**The maker never grades its own homework.** The agent that produced work never decides it's ready — a panel of independent, hard-to-please reviewer subagents grades it against documented standards first. A model reviewing its own output is structurally compromised: it reuses the same reasoning that produced the work, forgives the gaps it already knows about, and mixes maker-knowledge into the verdict ("I couldn't verify X, so I left it out" is the maker lobbying, not a review). Self-reflection inside the maker plus independent graders outside it stack; neither replaces the other.

## The Iron Rule

No READY / done / ship verdict on self-generated work without independent panel verdicts. Not for small artifacts, not under time pressure, not because the self-review "already found the issues."

## Process

1. **Fix the standards first.** Find the documented standards the work must meet (project docs, skill checklists, brand voice, user requirements). None written? Extract a checklist from the user's request before empaneling — reviewers grade against a checklist, not vibes.
2. **Empanel 2–4 reviewers with distinct lenses.** Each is a fresh subagent that receives ONLY: the task brief, the artifact, the standards, and its reviewer charge. Never the maker's reasoning, self-evaluation, or "known limitations."
3. **Reviewer charge (include verbatim):** "You are a hard-to-please reviewer. Your job is to find reasons this fails the standards, not to appreciate it. Grade each standard PASS/FAIL with evidence. Uncertain → FAIL. End with verdict: SHIP or REVISE, plus your top 3 specific objections."
4. **Iterate.** REVISE verdicts go back to the maker with the objections; revise; re-run the failed reviewers on the new version. Max 3 rounds — then deliver to the human with unresolved objections attached. Run reviewers in the foreground and collect every verdict before proceeding — never end your turn while reviewers are still running.
5. **Report.** Deliver the work with panel verdicts and what changed per round. Never present panel-less work as finished.

## Default panels by work type

| Work | Lenses |
|---|---|
| Copy / emails / marketing | standards checker · target-reader skeptic (would THIS person reply?) · AI-tell hunter |
| Docs / proposals / reports | requirements-compliance checker · hostile evaluator scoring as the recipient · clarity editor |
| Plans / strategies | feasibility engineer · value skeptic (why does this matter?) · risk finder |
| Code | correctness · simplicity/maintainability · edge cases + security — or route to your code-review tooling (`/review`, `/code-review`, or a second-model reviewer) |
| Research | source verifier · missing-perspective finder (storm-research Phase 4 is self-critique — still empanel) |

Scaling: 1 reviewer minimum for small-stakes artifacts; the full panel is the default; high-stakes work adds a second-model reviewer (a different vendor's model, if you have one wired up).

## Rationalization table

| Excuse | Reality |
|---|---|
| "I already critiqued it myself, honestly" | The baseline failure. Self-review reuses the maker's blind spots and forgives known gaps. |
| "It's small / just a draft" | Small artifacts get 1 reviewer, not zero. Anything shown to the human is a deliverable. |
| "User is waiting / time pressure" | A reviewer round takes 1–2 minutes. Shipping unvetted work costs more. |
| "The model self-validates at high effort" | Self-validation makes the maker honest inside its role; the independent grader sits outside it. Stack both. |
| "Reviewers will just agree with me" | Then the charge is too soft — a reviewer that never FAILs anything is broken; re-charge it. |

## Red flags — stop and empanel

- About to type "READY", "done", "ship it", or a self-assigned quality score
- Writing a "quality evaluation" section about your own output
- Passing your own caveats or justifications along to a reviewer
- Skipping re-review after revising
