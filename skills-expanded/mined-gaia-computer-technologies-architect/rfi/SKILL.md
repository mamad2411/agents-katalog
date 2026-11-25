---
name: rfi
description: Drafts Requests for Information (RFIs / technical queries) and the architect's responses, each tied to drawing, specification, and model references, and keeps a numbered RFI log with status, dates, and response times. Use when the architect wants to "write an RFI", "respond to this RFI", "answer the contractor's query", "update the RFI log", or "is this a variation?". Flags any response that would amount to a change, a variation, a design responsibility shift, or an instruction that should be issued formally. Hands formal instructions to contract-admin-letter and meeting follow-ups to meeting-minutes.
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# RFI

An RFI is a question about the contract information: something missing, unclear, or contradictory. Its answer clarifies the design intent. The danger is that an answer quietly changes the design, the cost, or who is responsible, without anyone treating it as a change. This skill writes clear questions, careful answers, and a log that shows what happened.

## When to use

- Contractor or subcontractor has raised a query and the architect needs to respond.
- The architect needs to ask a consultant, client, or supplier for missing information (design-team RFI).
- Setting up or updating the RFI log for a project.
- Deciding whether a query is really an RFI or a change in disguise.

## Input

- The query (or the issue, if drafting one): text, marked-up drawing, photo, or clause.
- References: drawing numbers and revisions, specification sections, model element IDs, schedule references, previous RFIs.
- The contract form and the role of the architect (designer only, or also contract administrator). If unknown, ask; it changes what a response can do.
- Required response time, if the contract or the RFI sets one.
- The existing RFI log, if any.

## Process

1. **Restate the question precisely.** One RFI, one question. If the query bundles three issues, split them (RFI-041a, b, c) so each can close separately.
2. **Locate the conflict.** Cite exactly which documents say what: "Drawing A-201 rev C shows 100 mm insulation; spec section 07 21 00 cl. 2.3 calls for 120 mm." If the documents do not conflict and the answer is already in them, say so and point to it.
3. **Answer the design intent, not the method.** The architect states what the design requires. Means, methods, and temporary works usually belong to the contractor; do not take them on.
4. **Run the change test.** Before finalising a response, check whether it:
   - adds, removes, or alters work shown or specified;
   - changes a specified product, performance, or standard;
   - is likely to change cost or time;
   - moves design responsibility (e.g. "contractor to design the fixing" where the documents did not say so, or the architect designing what was contractor-designed);
   - needs input from another consultant (structure, MEP, fire) before it can be answered.
   If any is true, flag it in the response box and the log: "This response may constitute a change. Recommend issue as a formal instruction / change order under [contract clause, to be confirmed] before work proceeds." Hand to `contract-admin-letter`.
5. **Route specialist questions.** Structural, fire, acoustic, MEP, and accessibility answers come from the responsible consultant. Draft the forwarding note; do not answer it yourself.
6. **Update the log.** Number, date raised, raised by, subject, references, date due, date answered, status, change flag, cost/time flag.

## Domain knowledge

- **Terminology varies.** RFI (US, international), Technical Query or TQ (UK, some EU), Request for Clarification. The log works the same way.
- **Response times.** Some contracts or specifications set a period for answering information requests; late answers can support a delay claim. Ask for the period and track it; do not assume one.
- **Contract forms differ** on who can instruct and how: e.g. JCT and NEC (UK), AIA A201 (US), FIDIC (international), and many national forms. Under some, an RFI response is not itself an instruction; under others it can be treated as one. Ask which applies and flag the uncertainty.
- **Design-intent wording.** "The design intent is X. Contractor to propose a detail achieving X for architect's comment" keeps the responsibility where it already sits. "Contractor to install X" may instruct.
- **Volume is a signal.** A cluster of RFIs on one area often means the information there is incomplete. Note patterns in the log summary.

## Output format

```
RFI [No.]   Project: [ ]   Date raised: [ ]   Raised by: [ ]
Subject: [ ]
References: [drawing no. rev, spec section, model ID, previous RFI]

QUESTION
[One precise question, with the conflicting or missing information cited.]

RESPONSE (Architect)
[Design intent, referenced. Or: answer is in [doc] — see [ref].]

CHANGE CHECK
- Alters scope/specification: [Y/N — why]
- Likely cost or time effect: [Y/N/Unknown]
- Design responsibility affected: [Y/N — why]
- Needs consultant input: [who]
Recommendation: [Close as clarification / Issue formal instruction under [clause tbc] / Forward to [consultant]]

RFI LOG
| No. | Date raised | From | Subject | Refs | Due | Answered | Status | Change? |
```

End every response that contains a change flag, a contractual reference, or a performance statement with:

```markdown
> **Disclaimer:** AI-generated analysis for preliminary purposes only. All figures, standards, and references must be verified by a qualified professional before use in design, permitting, costing, contracts, or regulatory submission.

<!-- architect:requires-disclaimer -->
```

Copy the disclaimer exactly as shown, including the `<!-- architect:requires-disclaimer -->` line. That line is the machine-readable marker the plugin checks for, so keep it even in a chat reply.

## What you don't do

- Don't invent drawing numbers, revisions, spec clauses, or contract clauses. Use [ref tbc] and list them.
- Don't give structural, fire, MEP, acoustic, or accessibility answers. Route to the responsible consultant.
- Don't decide whether something is a variation or who pays. Flag it; the contract administrator decides.
- Don't take on means and methods or temporary works.
- Don't say a proposed alternative "complies". Say it "appears consistent with the specified performance, subject to verification by [consultant / datasheet]".
