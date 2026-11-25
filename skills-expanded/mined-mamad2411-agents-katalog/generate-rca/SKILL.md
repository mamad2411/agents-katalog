---
name: generate-rca
description: Top-level reporting workflow for transforming a completed investigation report and supporting evidence into concise, professional Root Cause Analysis Markdown and PDF deliverables. Use when asked to generate an RCA from completed findings, confirmed or unconfirmed root cause, impact, timeline, fixes, verification evidence, tickets, commits, or deployment details; do not use to investigate or discover the root cause.
---

# Generate RCA

## Purpose

Transform a completed investigation report into a professional Root Cause Analysis. The `technical-documentation-specialist` should lead this workflow, but the RCA must rely on evidence from the actual investigation and primary investigator.

Do not investigate, speculate, or invent missing information. If the investigation does not contain a confirmed root cause, state that clearly and do not manufacture one.

## Inputs

Use only supported information from:

- Investigation reports.
- Confirmed root cause and confidence level.
- Supporting evidence.
- Fix and deployment details.
- Impact assessment.
- Incident timeline.
- Related tickets, commits, deployment IDs, or incident IDs.

## Workflow

1. Read the completed investigation or supplied findings.
2. Use only the investigation report and supporting evidence.
3. Extract confirmed facts, supported conclusions, impact, timeline, resolution, preventive actions, verification evidence, owners, and traceability references.
4. Separate confirmed facts from recommendations.
5. Draft the RCA markdown first.
6. Omit sections with no available content.
7. If confidence is low or the root cause is unconfirmed, state that plainly and include the investigation confidence level when available.
8. Generate a PDF from the finalized RCA markdown, not directly from raw investigation notes.
9. Verify the PDF is not empty and matches the populated RCA markdown sections.
10. Return the markdown report, PDF filename, and PDF location.

## Rules

- Do not perform the investigation.
- Do not invent missing information.
- Do not fabricate a root cause.
- Keep the RCA concise, professional, and actionable.
- Include preventive action owners when available.
- Include traceability references when available.
- Mention investigation confidence level when available.

## RCA Markdown Format

```markdown
# Root Cause Analysis

## Issue Summary

Brief description of the issue.

Include:

- What was the issue?
- Which feature/system was affected?

## Impact

Who or what was affected.

Include:

- Affected users/systems
- Scope of impact
- Error rate / occurrence frequency
- Business impact

## Timeline

Important incident/investigation events, if available.

## Root Cause

The confirmed technical reason for the issue.

If no confirmed root cause exists, state:

> Root cause has not been conclusively determined.

## Why It Happened

The underlying process, design, configuration, data, deployment, or implementation reason.

## Why It Was Not Detected

Explain detection gaps, such as missing test coverage, missing validation, monitoring limitations, code review gaps, or an edge case not considered.

## Resolution

What was done or needs to be done to fix the issue.

Include:

- Code changes
- Configuration changes
- Data corrections
- Deployment actions

## Preventive Actions

Action items to prevent recurrence. Use checkboxes where appropriate:

- [ ] Add or update unit tests
- [ ] Add integration/API tests
- [ ] Improve monitoring and alerting
- [ ] Update documentation
- [ ] Update code review checklist
- [ ] Add validation/safeguards
- [ ] Other

## Verification Evidence

Evidence that the fix works or how it should be verified.

## Lessons Learned

What went well, what could be improved, and what should be done differently.

## Appendix

Include only when available:

- Investigation identifier
- Related ticket number
- Incident number
- Relevant commit IDs
- Deployment IDs
- Supporting evidence references
```

## PDF Requirements

- Generate a new PDF after generating the finalized RCA markdown.
- Generate the PDF from the finalized RCA markdown, not directly from raw investigation findings.
- Include all populated RCA sections.
- Omit sections with no content.
- Include report generation timestamp.
- Use a professional engineering/reporting layout.
- Make the PDF understandable without the original investigation report.
- Ensure the PDF matches the RCA markdown content.
- Include investigation confidence level when available.
- Do not fabricate a root cause.
- If no confirmed root cause exists, include: `Root cause has not been conclusively determined.`

Use the user-specified output directory when provided. Otherwise place generated RCA PDFs under `output/rca/`.

## PDF Naming

Use:

```text
RCA_<issue-name>_<yyyy-mm-dd>.pdf
```

Example:

```text
RCA_SSO_Admin_Permission_Error_2026-06-22.pdf
```

## Failure Handling

If PDF generation fails:

1. Return the RCA markdown.
2. Report the PDF generation error.
3. Do not silently skip PDF creation.

## Required Deliverables

- RCA markdown document.
- PDF version of the RCA report.
- PDF filename.
- PDF file location or reference.
