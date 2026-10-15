---
name: camera-ready-finalizer
description: Finalize an accepted ML or AI paper for camera-ready submission after reviews, rebuttal, and acceptance. Use this skill whenever the user has an accepted paper, camera-ready deadline, final revision, acceptance email, meta-review, rebuttal promises, author-response commitments, de-anonymization tasks, supplement updates, code links, acknowledgements, final LaTeX checks, or needs to ensure the accepted paper's claims, figures, references, and artifacts are consistent before final submission.
argument-hint: "[paper-dir] [--venue <venue>] [--mode audit|finalize|check|handoff]"
allowed-tools: Read, Write, Edit, Bash, Glob, WebSearch, WebFetch
---

# Camera-Ready Finalizer

Finalize an accepted paper so the submitted camera-ready version is consistent, de-anonymized, claim-safe, and ready to hand off to code release or artifact evaluation.

Use this skill when:

- a paper has been accepted and the user needs the camera-ready version
- author-response or discussion promises must be checked against the final PDF
- anonymized submission text must become final author-facing text
- acknowledgements, author metadata, code links, project pages, or funding statements must be added
- final figures, tables, captions, appendix, supplement, and references must be synchronized
- new rebuttal experiments or reviewer-requested edits must be integrated cleanly
- the paper needs a final claim/evidence/citation/code-release consistency pass before upload

Do not use this skill for pre-submission readiness. Use `submit-paper` before initial submission. Use `rebuttal-strategist` while reviews are still active. Use `release-code` for the public code repository after paper-facing obligations are clear.

Pair this skill with:

- `rebuttal-strategist` to recover reviewer issues, response promises, and promised revisions
- `paper-evidence-board` to close final claim/evidence/risk/action links
- `figure-results-review` to recheck final figures, captions, and tables after edits
- `citation-audit` for final BibTeX, citation, label, and metadata correctness
- `citation-coverage-audit` when accepted-paper edits reveal missing related work
- `conference-writing-adapter` for final wording of accepted reviewer criticism or limitations
- `submit-paper` for final format and compile checks
- `release-code` and `artifact-evaluation-prep` for public code and artifact handoff
- `add-git-tag` when marking the accepted/camera-ready milestone
- `research-project-memory` when final paper status should persist across sessions

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
└── references/
    ├── claim-evidence-final-lock.md
    ├── de-anonymization.md
    ├── final-submission-audit.md
    ├── memory-writeback.md
    ├── rebuttal-promise-audit.md
    ├── release-handoff.md
    ├── report-template.md
    └── supplement-consistency.md
```

## Progressive Loading

- Always read `references/rebuttal-promise-audit.md`, `references/de-anonymization.md`, `references/claim-evidence-final-lock.md`, and `references/final-submission-audit.md`.
- Read `references/supplement-consistency.md` when appendix, supplement, checklist, or extra material exists.
- Read `references/release-handoff.md` when code, project page, artifact, data, checkpoints, or reproduction links are involved.
- Read `references/report-template.md` before writing the final report.
- Read `references/memory-writeback.md` when the project has `memory/`, component `.agent/` folders, or the user asks for persistent memory.
- If venue-specific camera-ready rules matter, verify current official venue instructions before making hard claims about page limits, required sections, licenses, checklists, or upload fields.

## Core Principles

- Camera-ready is a consistency and obligation closeout, not a new paper rewrite.
- Every rebuttal promise should be either fulfilled, explicitly superseded, or documented as not applicable.
- De-anonymization must be complete but should not introduce new claims or unsupported links.
- Final claims must match final evidence, figures, tables, supplement, and code.
- New post-acceptance edits should reduce risk, not reopen novelty or evaluation disputes.
- The main paper, appendix, supplement, metadata, and code links must tell the same story.
- The final output should leave a clear handoff to release, artifact evaluation, tagging, and archival memory.

## Step 1 - Recover Acceptance Context

Collect:

- paper directory and main LaTeX file
- target venue and camera-ready deadline
- acceptance email, meta-review, reviews, discussion, and author responses
- rebuttal promise list, if available
- current accepted draft and current camera-ready draft
- final figures, tables, supplement, appendix, checklist, and bibliography
- author list, affiliations, acknowledgements, funding, project/code/data links
- code release or artifact expectations
- project memory IDs such as `CLM-###`, `EVD-###`, `RSK-###`, `ACT-###`, `REV-###`, or `PROM-###`

If no promise list exists, create one from reviews, rebuttal, and discussion before editing the paper.

## Step 2 - Audit Rebuttal Promises

Read `references/rebuttal-promise-audit.md`.

Build a promise ledger:

- reviewer/source
- promise or implied commitment
- required paper change
- current status
- location in final draft
- evidence or artifact link
- risk if omitted

Statuses:

- `fulfilled`
- `partially-fulfilled`
- `superseded`
- `not-applicable`
- `missing`
- `needs-author-decision`

Do not silently drop a promise because it is inconvenient. If a promise cannot be fulfilled, mark the risk and draft a conservative note or limitation if needed.

## Step 3 - De-Anonymize and Restore Final Metadata

Read `references/de-anonymization.md`.

Check:

- author names, order, affiliations, emails, and footnotes
- acknowledgements, funding, compute grants, institutional resources
- code, data, project page, model, and appendix links
- self-citations and anonymized references
- removed anonymity placeholders
- PDF metadata and artifact metadata where applicable
- license, copyright, and publisher-specific final metadata if required

Do not invent funding, affiliation, or author-order details. Ask the user if a required personal/institutional detail is missing.

## Step 4 - Lock Claims Against Final Evidence

Read `references/claim-evidence-final-lock.md`.

For each main claim:

- final paper location
- supporting figure/table/theorem/experiment/citation
- final status: supported, narrowed, moved-to-appendix, limitation, or cut
- whether new rebuttal experiments changed the claim
- whether captions and result prose match final numbers
- whether supplement and code agree with the paper

If a claim is unsupported, either narrow it, move it to limitations/future work, or cut it.

## Step 5 - Check Supplement and Appendix Consistency

Read `references/supplement-consistency.md` when relevant.

Check:

- main paper references to appendix/supplement resolve
- appendix numbering, figure/table labels, and cross-references are correct
- supplement claims do not contradict the main paper
- extra experiments are summarized consistently
- reviewer-requested details are easy to find
- checklists, ethics, limitations, broader impacts, and reproducibility sections match final venue requirements

## Step 6 - Run Final Submission Audit

Read `references/final-submission-audit.md`.

Check:

- venue camera-ready instructions and upload requirements
- page limits and final formatting
- compile status and final PDF sanity
- bibliography and metadata
- labels, references, figures, tables, algorithms, equations, and appendices
- stale TODOs, comments, draft macros, anonymization text, or hidden placeholders
- final title, abstract, author metadata, and PDF filename
- final link reachability if links are included

Use `citation-audit` and `submit-paper` for detailed checks when needed.

## Step 7 - Prepare Release and Artifact Handoff

Read `references/release-handoff.md` when relevant.

Produce handoff items for:

- `release-code`: repository visibility, README, license, citation file, tag, model/data links, reproduction commands
- `artifact-evaluation-prep`: install instructions, expected runtime, minimal demo, hardware, checkpoints, data, troubleshooting
- `add-git-tag`: accepted/camera-ready milestone summary
- project memory closeout

Keep paper finalization separate from code release, but make obligations explicit.

## Step 8 - Write the Camera-Ready Report

Read `references/report-template.md`.

If saving to a project and no path is given, use:

```text
docs/submission/camera_ready_audit_YYYY-MM-DD_<venue>.md
```

The report must include:

- readiness decision
- blocking issues
- promise ledger
- de-anonymization status
- final claim/evidence lock
- supplement/appendix consistency
- final submission audit
- release/artifact handoff
- memory update section

## Step 9 - Write Back to Project Memory

Read `references/memory-writeback.md` when memory exists.

Update:

- `memory/decision-log.md`: acceptance and camera-ready decisions
- `memory/claim-board.md`: final claim status
- `memory/evidence-board.md`: final paper-ready evidence and artifact links
- `memory/risk-board.md`: any residual accepted risks
- `memory/action-board.md`: final blockers, release tasks, artifact tasks, and tag tasks
- `paper/.agent/`: camera-ready status, final metadata, final PDF path, final upload notes
- `rebuttal/.agent/`: promise fulfillment status and accepted outcome

## Final Sanity Check

Before finalizing:

- all rebuttal promises are accounted for
- author metadata and acknowledgements are complete
- no anonymity placeholders remain
- final claims match final evidence
- figures/tables/captions/supplement/code links are consistent
- final references and labels are clean or routed to `citation-audit`
- final format is clean or routed to `submit-paper`
- code/artifact/release obligations are routed
- project memory records the accepted/camera-ready state
