---
name: academic-paper-review
description: Use when the user asks to review, critique, summarize, or assess one academic paper, preprint, or research article, especially for referee reports, methodology checks, contribution assessment, top-journal internal review, or social-science-style evidence review.
---

# Academic Paper Review

Use this skill for one-paper tasks. If the user wants a topic review across multiple papers, use `systematic-literature-review` instead. If the user provides reviewer comments and asks for a response letter, use `reviewer-response-pack` through the `writing-export` route.

## Required Contract

Before reviewing, read:

- `<VELA_RUNTIME_ROOT>/skills/catalog/peer_review_workflow.json`
- `<VELA_RUNTIME_ROOT>/skills/catalog/writing_quality_rules.json`
- `<VELA_RUNTIME_ROOT>/skills/catalog/publication_style_rules.json`
- `<VELA_RUNTIME_ROOT>/skills/catalog/citation_verification_rules.json`

The review must follow the selected mode in `peer_review_workflow.json`.

## Mode Selection

- `standard_single_review`: normal one-paper review. Do not default to a real multi-agent panel; simulate role checks inside one review report.
- `top_journal_internal_review`: use when the user asks for top-journal review, submission-before-review audit, major-revision internal review, multiple reviewers, or a high-stakes manuscript check.
- `domain_calibrated_review`: only propose this when the user has a stable research area plus enough verified public review evidence or anonymized high/normal sample papers.

Do not select `revision_response_review`; that belongs to `reviewer-response-pack`.

## Non-Negotiables

1. Do not fabricate citations, DOI, venue, authors, publication status, data, line numbers, p values, sample sizes, robustness checks, or appendices.
2. Bibliographic metadata must be verified before a formal reference is presented.
3. DOI is strong evidence, but not the only gate. User-provided sources, complete paper PDFs, and public academic index records can waive the requirement that every reference must have a DOI.
4. DOI waiver does not waive verification. Record the verification basis.
5. If the paper text is incomplete, state the access boundary and do not review unread sections as if they were read.
6. Reviewers must not directly modify the submitted manuscript. Produce review reports, ledgers, and revision priorities only.
7. For social science papers, prioritize theory, evidence, identification, measurement, ethics, reproducibility, and claim boundary over decorative polish.
8. Do not turn review into automatic self-weakening. Identify real limits and unsupported claims, but also preserve contributions that the evidence can support.

## Review Workflow

1. Build `review_run_card`:
   - paper path or source
   - review mode
   - target venue or review standard if supplied
   - material boundary
   - whether subagents are actually needed
2. Verify metadata and access:
   - title, authors, year, venue, DOI if present, publication status
   - PDF/text completeness and unread sections
   - DOI waiver evidence when no DOI is available
3. Extract claims before judging:
   - research question
   - contribution
   - theory or mechanism
   - data and measurement
   - identification or analytic design
   - main empirical or interpretive claims
4. Create an issue ledger using the required fields in `peer_review_workflow.issue_contract`.
5. Run the core review dimensions:
   - theory and literature positioning
   - data and measurement
   - research design and identification
   - method or empirical strategy
   - interpretation and claim strength
   - transparency, reproducibility, and ethics
   - writing structure and reader path
   - figures, tables, and evidence presentation when present
6. Always include a standalone subtle logic flaw audit:
   - causality gap
   - proxy metric substitution
   - setting mismatch
   - baseline or comparison unfairness
   - theory-implementation gap
   - scope inflation
   - correlation-as-mechanism
   - visualization-as-evidence
   - revision fragility
   Mark non-applicable items explicitly.
7. If in `top_journal_internal_review`, add:
   - reviewer configuration card
   - runtime literature context pack when novelty, baseline, or missing-literature claims are made
   - independent role memos or a clear reason why role subagents were not needed
8. Integrate findings:
   - separate blocking, major, minor, and informational issues
   - preserve real disagreements between theory, method, evidence, and writing checks
   - give a revision priority map

## Runtime Literature Context Gate

Use this only when the review makes strong claims about novelty, missing baselines, missing comparisons, or field positioning.

The context pack must distinguish:

- `full-text-read`
- `partial-full-text`
- `metadata-only`
- `inaccessible`

Metadata-only records cannot support strong novelty, baseline, or missing-comparison judgments. If full text cannot be obtained, state the limitation and lower confidence.

## Reviewer-Perspective Adapter

The local workflow absorbs useful review prompt constraints from `Leey21/awesome-ai-research-writing`, but keeps the local peer-review contract as the source of truth.

When the user asks for a whole-paper reviewer view, top-journal internal review, or submission-readiness judgment:

- Distinguish true blocking or fatal issues from fixable weaknesses. Do not inflate minor wording problems into method failure.
- Strengths must be real contributions, not generic praise.
- Weaknesses must point to a concrete location, claim, experimental/design setting, evidence gap, or wording risk.
- Rating or recommendation must be tied to the actual level of contribution, rigor, and presentation, not to a fixed harsh template.
- Strategic advice must separate root cause, fixability, and concrete action: what can be fixed by writing, what needs analysis/evidence, and what is structural.

This adapter does not allow the reviewer to edit the manuscript directly, invent missing experiments, or claim unread appendices were checked.

## Stop Slop Review Check

When reviewing manuscript prose, use `writing_quality_rules.json` to flag surface problems that make the paper sound generic or machine-written:

- filler openings, vague importance claims, and performative emphasis;
- formulaic "not X but Y" reversals and negative-listing setups;
- mechanical `rather than`, `since`, `however`, `therefore`, and `not only but also` structures that delay the real claim;
- defensive or limitation-first phrasing that weakens the contribution before stating what the paper shows;
- hidden actors, false agency, and passive constructions that obscure responsibility when actor identity matters;
- repeated three-part rhythm, uniform short paragraph blocks, identical sentence cadence, slogan endings, and paragraph conclusions that sound like pull quotes;
- Chinese terms that appear to be invented from English rather than grounded in Chinese scholarship or established Chinese academic usage;
- reader-facing internal workflow or engineering terms that should stay outside the manuscript.

Treat these as writing issues, not scientific defects. Do not let surface style concerns outrank theory, evidence, identification, measurement, ethics, reproducibility, or citation integrity. A strong review should state what the paper can credibly contribute, what must be fixed, and which limits need to be named without turning the manuscript into a defensive limitations list.

## Output Contract

Default output:

```markdown
# Paper Review: [Title]

## Review Run Card
- Mode:
- Materials read:
- Materials not read:
- Target standard:
- Subagent use:

## Verified Metadata
- Authors:
- Year:
- Venue/source:
- DOI:
- Verification basis:
- Publication status:

## Core Question And Contribution

## Summary Of The Paper

## Main Strengths

## Blocking Or Major Concerns
Each concern must include: location, claim/object, evidence seen, diagnosis, required action, confidence.

## Minor Concerns

## Methodology Assessment
- Theory and literature:
- Data and measurement:
- Design and identification:
- Analysis:
- Interpretation:
- Transparency and ethics:

## Subtle Logic Flaw Audit
| Flaw type | Where it appears | Why it matters | Evidence needed | Review wording | Revision path |
|---|---|---|---|---|---|

## Issue Ledger Summary

## Recommendation
- Overall judgment:
- Confidence:
- Conditions or revisions needed:
```

When writing a venue-style judgment, use:

- strong accept
- accept
- weak accept
- borderline
- weak reject
- reject

When the user did not ask for a venue-style label, prefer:

- publishable with minor revision
- major revision required
- evidence too weak for current claims

## Failure Rules

Stop or downgrade the output when:

- the paper cannot be accessed beyond title and abstract
- metadata cannot be verified
- DOI appears in evidence but cannot be verified
- no DOI and no acceptable DOI-waiver evidence exists for formal reference output
- the review would require pretending to know unread appendices, data, code, proofs, or tables
- the task is actually a response letter or revision package
