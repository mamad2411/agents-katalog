---
name: wizspec
description: Route a request to the skill in this repository that fits it. Use as the entry point when it is unclear which skill applies, or when one workflow needs to hand off to another.
license: MIT
---

# Wizspec

Pick the skill in this repository that fits the request, then run it. This skill routes; it does not
do the work itself.

## Skills

| Skill | Use it when |
| --- | --- |
| `brainstorm` | The user wants to explore, develop or put into words an idea, or has a goal but not yet its shape. Produces the idea drawn out through rough versions to react to, and a Brainstorm file with a status. |
| `grill` | A plan, design, or decision is still unsettled and has to be interrogated until it holds up. Produces shared understanding, a `CONTEXT.md` glossary, and a written decision for each call that was genuinely hard. |
| `document-writing-orchestrator` | A substantial document has to perform a real job for a real reader. Produces the document through a writer and a reviewer drawn from that job, with sources tracked and claims checked against them. |
| `user-facing-text` | Text that the people using a product read has to be written or reviewed: docs, interface strings, errors, READMEs, release notes. Produces direct prose in the project's own terms, or findings with suggested rewrites. |
| `fresh-eyes` | The user wants something new, and the risk is that it comes out like what has been done before. Produces an idea from an agent that knows nothing about the project, grounded in the facts needed to make it real. |

## Routing

Ask what the request is short of, and route on that.

**An idea to think through goes to `brainstorm`.** The signs are "let's brainstorm", "I have an
idea but…", "what could we do about…", or a goal with no shape yet. The risk is settling on the
first version, or on what was decided before, before the idea has had room to move. Once the
user picks a direction, `grill` can settle the hard calls it leaves.

**Unsettled thinking goes to `grill`.** The signs are that the user cannot yet state the decision,
uses a term two ways in consecutive sentences, or has not faced the trade-off the plan turns on.
Drafting now would commit prose to choices nobody has made.

**A deliverable that has to work on someone goes to `document-writing-orchestrator`.** The signs are
a named reader, an evaluator, or an action the document must produce — a proposal, a runbook, a
policy, a report, a guide. The thinking is settled enough that the remaining risk is in the writing.

**Text a user will read goes to `user-facing-text`.** The signs are a label, a tooltip, an error
message, a README, release notes, or a docs page to write or review, where the risk is in the
sentences rather than in the structure or the sources. A substantial document goes to
`document-writing-orchestrator`, which can apply `user-facing-text` to the prose it produces.

**A request for something new goes to `fresh-eyes`.** The signs are that the user wants an idea
rather than help with one they already have, or says that results keep coming out like the last
ones. The risk is in where the idea comes from. When the user instead wants to think an idea
through with you, that is `brainstorm`. Once the user has chosen an idea, `grill` can
pressure-test it, and the work of making it goes wherever that work fits.

**Both, in that order, when the user asks for a document about something they have not decided
yet.** Run `grill` first and let it settle the vocabulary and the hard calls, then hand its
`CONTEXT.md` and decisions to `document-writing-orchestrator` as authoritative sources.
Skipping the first step produces a fluent document that argues for nothing in particular.

**Neither, when the request has one correct answer.** Routine implementation, a factual lookup, a
narrow copyedit, or a format conversion is ordinary work. Do it directly and say that no skill
applied, rather than dressing a small task in a workflow.

## Personas are not routed to

Do not pick or suggest `personas` from here, even when a request looks persona-shaped. Persona work
runs only when the user asks for it by name. Other skills may still use it as a step of their own,
as `brainstorm` does when it brings in outside opinions.

State which skill you picked and why in one sentence before you start, so the user can redirect you
before the work rather than after it.
