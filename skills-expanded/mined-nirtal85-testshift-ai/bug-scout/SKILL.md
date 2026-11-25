---
name: bug-scout
description: Investigate CI and test automation failures, classify them as product defect, stale automation, flaky infrastructure, or insufficient evidence, and produce concise evidence-backed issue proposals with RCA candidates. Use when a test failure may represent a product bug, when a user asks to triage a CI failure, connect a failure to recent code changes, or draft a Jira/GitHub issue from automation evidence.
---

# Bug Scout

## Goal

Turn automation failures into governed, evidence-backed issue proposals.

Default outcome: propose.

Do not create tickets, modify code, or open pull requests without explicit human approval.

## Core Rules

- Treat correlation as suspicion, not proof.
- Use read-only evidence collection by default.
- Classify the failure before drafting a ticket.
- Do not open weak tickets.
- Suppress Medium/Low RCA claims inside the ticket proposal.
- Classify weak signals honestly as `Insufficient evidence`.
- Do not weaken tests to hide product defects.
- Describe product behavior, not test-framework noise.

## Required Evidence

Before proposing a ticket, gather:

- Failing test title and file path.
- Environment and scope.
- Test report, trace, screenshot, video, or CI artifact link.
- Actual product behavior.
- Expected product behavior.
- First-fail time and last-pass time when available.
- Relevant UI selector, API endpoint, status code, response body, or log line.
- Recent code changes in relevant repositories when RCA is requested.
- Similar historical issues when available.

If environment scope, artifact link, or reproduction path is missing, ask for more data.

## Classification

Classify every failure first:

| Classification | Meaning | Output |
|---|---|---|
| Product defect | Application behavior probably regressed | Issue proposal with evidence |
| Stale automation | Test no longer matches intended behavior | Test-fix proposal |
| Flaky infrastructure | Runner, timing, network, or environment instability | No product bug |
| Insufficient evidence | Signal too weak | Ask for more data |

## RCA Workflow

1. Extract failure keywords:
   - product area
   - endpoint
   - selector
   - error text
   - environment
   - feature flag
   - data shape
   - first-fail timestamp

2. Check flakiness signals:
   - passed on rerun
   - many unrelated tests failed
   - runner or network errors
   - no matching product change
   - environment-only instability

3. Search historical issues:
   - automation-found bugs
   - same endpoint
   - same selector
   - same error text
   - same product area

4. Search recent code changes:

```bash
gh pr list -R ORG/REPO --state merged --search "merged:>=YYYY-MM-DD" --json number,title,mergedAt,author,labels,url
gh pr view PR_NUMBER -R ORG/REPO --json title,body,files,commits,mergedAt,author,url
```

5. Rank suspects:
   - High: same endpoint/component/selector/data path changed near first-fail.
   - Medium: same product area, but not same code path.
   - Low: shared infra, dependency, environment, or timing only.

Only include High-confidence suspects in the proposal.

## Ticket Template

```markdown
## Summary
[2-4 sentences. Product-facing. Include actual vs expected. Avoid test jargon.]

## Environment
- Env: [environment and scope]
- Report: [artifact/report link]

## Steps To Reproduce
1. ...
2. ...
3. [Final step states the observed product outcome.]

## Failing Tests
- [test title]

First-fail: YYYY-MM-DD HH:mm

## RCA Triage

[One sentence explaining the merge-window theory.]

| Suspect | Confidence | Reason |
|---|---|---|
| ISSUE-KEY / PR #123 | High | Changed the same code path shortly before first-fail. |
```

## Do Not Include

- Empty sections.
- Raw investigator notes.
- Missing-data checklist.
- Medium/Low RCA suspects.
- Long artifact dumps.
- Internal IDs unless needed for reproduction.
- Unknown placeholders like `TBD`.
- Summaries framed as `Automation failed because...`.

## Output Before Any Write Action

```markdown
## Proposed Issue

Summary:
Project:
Priority:
Labels:
Component:

Description:
[lean ticket body]

## High-Confidence RCA Candidates
- [candidate] - [reason]

## Missing Data
- [internal checklist; do not ship in ticket]
```

After approval, create the ticket and return the URL.

## Cost Controls

Do not run deep RCA on every red build.

Prefer:

1. Deduplicate similar failures.
2. Filter obvious infra noise cheaply.
3. Run Bug Scout on new, recurring, or release-blocking failures.
4. Require human approval for write actions.

## Evaluation

Track:

- RCA precision.
- RCA recall.
- false ticket rate.
- flake classification accuracy.
- median triage latency.
- cost per accepted ticket.

Historical issue labels are noisy. Treat known root cause as reviewed evidence, not absolute truth.
