---
name: bid-response
description: Answer a tender, RFP, RFQ, PQQ or framework bid by mapping every answer to the evaluation criteria and weightings, building a compliance matrix, and reusing the practice's own past bid text and case studies. Never invents projects, staff, awards, figures or testimonials; every missing piece of evidence is flagged. Use when the architect wants to "respond to an RFP", "write a tender response", "answer quality questions", "build a compliance matrix", "pick case studies for a bid", or "score our draft against the criteria". Hands to fee-proposal for the commercial envelope and project-description for case-study copy.
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# Bid Response

Win work by answering the question the evaluator scores, with evidence the practice can prove. AEC marketers report spending most of their time on proposals, and most of that time goes on re-finding old text. This skill organises the reuse and keeps the claims honest.

## When to use

- A public or private tender, RFP, RFQ, PQQ/SQ, or framework application has landed.
- The practice has a draft and wants it scored against the criteria before submission.
- The team needs to choose which case studies and CVs to put forward.

## Input

- **The tender documents:** instructions to bidders, evaluation criteria and weightings, word or page limits, mandatory forms, deadline, clarification deadline.
- **The practice's library:** past bid answers, case studies, CVs, policies (quality, environmental, health and safety, equality, data), accreditations, insurance certificates, financial information.
- **The project team** proposed, and who is available.

If the library is missing, ask for it. Do not write a case study the practice has not supplied.

## Process

1. **Parse the tender into a requirements list.** Extract every question, mandatory requirement, pass/fail gate, form, and limit. Number them as the tender does.
2. **Build the compliance matrix first.** One row per requirement: where it's answered, evidence used, status (complete / draft / missing evidence). Pass/fail gates go at the top; failing one makes the rest irrelevant.
3. **Weight the effort.** Allocate words and time in proportion to the scoring weights. A 30% question gets more care than a 5% one.
4. **Answer the question as scored.** Restate what the evaluator is looking for, then answer it in that order. Use the client's own terms from the brief. Lead each answer with the direct response, then the evidence.
5. **Pull evidence from the library.** For each claim, cite the source document it came from (past bid, case study, policy). Choose case studies by relevance to *this* brief: type, scale, procurement route, client type, recency.
6. **Flag gaps honestly.** Where the practice lacks the evidence a question wants, say so and suggest the nearest truthful answer (a comparable project, a partner's experience, a stated approach). Never paper over it.
7. **Score the draft.** Against each criterion, give a self-assessment on the tender's own scoring scale, with the reason, and the one change that would lift it.

## Domain knowledge

- **Evaluators score against a scheme, not an impression.** Mirror the criterion's wording, address each sub-point, and make the evidence easy to find.
- **Specific beats general.** "We reduced the client's energy use by X% on [project], measured in [year]" (with a source) beats "we are committed to sustainability".
- **Social value, sustainability and quality-management questions often carry real weight** in public procurement. Answer them with measurable commitments the practice will actually keep.
- **Clarification questions are free.** If a requirement is ambiguous, draft a clarification question before the deadline rather than guessing.
- **Public procurement rules differ by jurisdiction** (UK Procurement Act 2023 regime, EU directives as transposed nationally, US federal SF330 and state rules). Ask which regime applies; don't assume.

## Output format

```
## Bid Response — [Tender name], [Client], due [date]

### Pass/fail gates
| Ref | Requirement | Status | Evidence / document |
|---|---|---|---|

### Compliance matrix
| Ref | Question | Weight | Limit | Answer location | Evidence used | Status |
|---|---|---|---|---|---|---|

### Answers
#### [Ref] [Question] — [weight]%, [limit] words
[Answer: direct response first, then evidence. Each claim tagged with its library source.]
Word count: [n] / [limit]

### Evidence gaps
- [Ref]: [what the question wants] — [what we have] — [suggested truthful response or action]

### Self-assessment
| Ref | Score (tender scale) | Why | One change to lift it |
|---|---|---|---|

### Clarification questions to send
- ...
```

## What you don't do

- Don't invent projects, clients, staff, CVs, awards, testimonials, figures, accreditations, or certifications. If it isn't in the library, it isn't in the bid.
- Don't exaggerate a role. "Delivery architect" and "concept architect" are different claims; use what the practice actually did.
- Don't give legal or procurement-law advice on eligibility, exclusion grounds, or contract terms. Flag them.
- Don't exceed limits. An answer over the word count may not be read past the limit.
