---
name: workflows-analysis
version: "1.0"
description: Guides Slice MCP workflow analysis using workflow list/get-one tools, exercise payment reconciliation, and tax withholding tools. Use when answering questions about grant letters, corporate approvals, share certificate workflows, exercise workflows, pending payments, tax withholding, workflow status, stuck workflows, documents, trustee updates, or stakeholder/security workflow progress.
---

# Workflows Analysis

## Scope

Use for workflow process state, payments, and tax withholding. MCP cannot approve or mutate workflows. For compliance tickets, use compliance-analysis. For grant economics or vesting, use securities-analysis or equity-compensation-analysis.

## Core Principle

Workflow tools are read-only operational views. Use them to inspect process state, documents, payments, tax withholding, trustee updates, and workflow progress. Do not imply that MCP can approve, run, resend, cancel, or mutate workflows.

Start broad with workflow pages, then fetch one workflow only after you have a UUID. Use securities, stakeholder, cap-table, compliance, and valuation tools for business context; workflow tools show process state, not the full source-of-truth economics.

## Supported Workflow Types

`workflows_list` and `workflows_get_one` require `type` to be one of:

- `grantLetter`: grant or award letter execution workflows.
- `corporateApproval`: board/corporate approval workflows for grants.
- `shareCertificate`: share certificate signing and delivery workflows.
- `exercise`: exercise request workflows, including exercise notice, payment, tax withholding, share issuance, and optional share certificate steps.

Use the exact enum values above. Do not pass internal workflow enum names such as `executeAwardLetter` or `exerciseRequestNested` to the MCP workflow tools.

## Tool Selection

1. Use `workflows_list` for discovery by workflow type. It returns `{ type, data }` with the page payload for that type.
2. Use `workflows_get_one` when you have a `mainWorkflowExecutionId` or workflow UUID and need details for one workflow.
3. Use `payments_get_pending_list` for pending exercise-payment reconciliation rows across the company.
4. Use `tax_withholding_get_list` for exercise tax-withholding rows across the company.
5. Use securities or stakeholder tools to resolve IDs found in workflow rows when the user asks about the underlying grant, share, stakeholder, or ownership impact.
6. Use compliance tools separately if the user asks whether a workflow has compliance tickets or blockers.

`workflows_get_one` response shapes differ by type: grant-letter details can return an array, corporate approval returns one item, share-certificate details can return an array, and exercise details can return an array of exercise request display items.

## What To Inspect

For all workflow types, look for `mainWorkflowExecutionId`, `workflowName` or `name`, `customerFacingStatus`, `workflowLivenessStatus`, `createdAt`, `createdBy`, `deletedAt`, and related documents or email data.

For `grantLetter` and `corporateApproval`, inspect `stakeholdersData`, `grantsData`, countries, tax treatments, related documents, predefined approval date, trustee email data, and whether the workflow is live, paused, completed, draft, or deleted.

For `shareCertificate`, inspect stakeholder data, `sharesData`, customer-facing status, related share certificate documents, send-to-stakeholder email data, trustee update status, and deleted workflow metadata.

For `exercise`, inspect stakeholder data, associated grants, units to exercise, exercise prices, total price including tax, payment data, tax withholding data, exercise notice documents, share certificate documents, country/tax-treatment data, customer-facing status, inner status, and workflow liveness.

## Exercise Payments And Tax Withholding

Use `payments_get_pending_list` when the question is about exercise payments awaiting reconciliation or collection. Use `tax_withholding_get_list` when the question is about tax withholding work. These tools return exercise rows with `unitsToExercise` omitted; use `workflows_get_one` with `type: "exercise"` for one exercise workflow if unit-level detail is needed.

When payment or withholding rows need business context, resolve the associated grants through `securities_get_one` or `securities_find`, and use valuation/tax-treatment context only when the user asks why a tax or withholding issue exists.

## Combining With Other Tools

- Stakeholder workflow status: resolve stakeholder first, then list the relevant workflow type and filter rows by stakeholder ID/name. Fetch one workflow only if needed.
- Grant workflow status: use securities tools to resolve the grant, then inspect `grantLetter` and `corporateApproval` workflows for matching grant IDs or customer-facing IDs.
- Share certificate status: resolve the share with securities tools or cap-table rows, then inspect `shareCertificate` workflows for matching share IDs/customer-facing IDs.
- Exercise status: inspect `exercise` workflows, then use securities and vesting tools to explain the underlying grants, exercisable quantities, or resulting shares.
- Compliance blockers: use workflow rows to identify affected objects, then `compliance_get_object_tickets` for those specific objects.

Keep workflow status separate from legal/economic state. A completed workflow may update securities, shares, or documents, but use the relevant domain tool to confirm the resulting record.

## Large Requests

Aggregate workflow lists by type, status, stakeholder, or date. Fetch `workflows_get_one` only for representative or user-specified IDs. Summarize in chat; for full exports, note file-report is the right shape — do not dump raw arrays.

## Response Style

Lead with operational status: counts by workflow type/status, blockers, pending user/company/trustee actions, overdue-looking items when dates support that, and the specific workflow IDs that need attention. Mention permission-scoped empty results carefully: empty workflow results can mean no workflows of that type or insufficient MCP/workflow access.
