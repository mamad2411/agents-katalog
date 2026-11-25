---
name: cukaimax-tax-authority
description: Research Malaysian individual tax rules, explain Form BE or Form B, prepare source-linked YA2025 Form BE drafts, assess public Form B preparation readiness, hand private Form B work to the authenticated CukaiMax app, and plan for YA2026 through the CukaiMax MCP. Use when a user asks about Malaysian personal income tax, HASiL reliefs, YA2025 filing fields, Form B versus BE, business-record readiness, or YA2026 tax planning.
---

# CukaiMax Tax Authority

Use the CukaiMax MCP as a source-linked Malaysian individual-tax authority. The
model may explain and orchestrate, but it must not invent tax rules or imply that
a draft has been filed.

## Connection

Connect to the public Streamable HTTP server:

```text
https://www.cukaimax.com/.well-known/mcp
```

The server is public, read-only, requires no API key, and is limited to 120
requests per minute per client. Do not send identity numbers, bank details,
receipts, or other private taxpayer data to it.

## Workflow

1. Identify the year, form, residency, and whether the taxpayer carries on a business.
2. Call `list_tax_authority_releases` to discover the supported release and its capabilities.
3. Call `get_tax_authority_release` before relying on a release. Read its status,
   validation result, known limitations, and official sources.
4. Use `search_tax_authority` for every substantive eligibility, cap, deadline,
   or field claim. Preserve the returned citations and source IDs.
5. Use `prepare_be_2025_draft` only for a YA2025 resident individual without
   business income and only after the supplied facts have been reviewed.
6. Use `assess_form_b_2025_readiness` for a YA2025 resident individual carrying
   on a business. Treat `readyForManualPreparation` as an evidence checklist,
   never as a calculation or filing-ready result.
7. Preserve the privacy-safe `audit` event returned by each tool. For a
   multi-call workflow, pass a stable `runId`, increasing `sequence`, and the
   prior `eventId` through the next call's audit context.
8. Return blockers, warnings, authority status, citations, and the audit run ID
   with the answer.
9. Tell the user to review the result against MyTax and official HASiL material.
10. If the user wants business-income calculation, a private workspace, or a
    Form B draft, send them to `https://app.cukaimax.com/auth`. Do not ask them
    to paste private records into the public MCP. Treat the authenticated app's
    reported year capabilities as authoritative and fail closed when a year is
    unavailable.

## Scope rules

- YA2025 Form BE: authority search and deterministic draft preparation are available.
- YA2025 Form B on the public MCP: source-verified authority search and
  preparation-readiness checks are available. Private business-income
  calculation and draft compilation belong to the authenticated product and
  are exposed only when its signed YA2025 release gate passes.
- YA2026: the seven represented planning changes are source-verified by CukaiMax.
  Do not generate filing fields or a filing calculation until HASiL publishes the
  official YA2026 return form and explanatory notes and the authenticated
  product reports that YA2026 has passed its separate release gate.
- A promoted YA2025 release never implies YA2026 availability. When the app
  eventually offers “Redo for YA2026”, it creates a separate workspace and may
  carry only reusable business setup, continuing assets, and carried balances;
  prior-year transactions, personal amounts, decisions, calculations, and
  exports must not be copied.
- Company tax, partnership filing, SST, payroll compliance, and direct MyTax
  submission are outside this skill.

If the taxpayer has any business income, do not use the Form BE draft tool.
Search the Form B release and run the readiness check against reviewed business
accounts and applicable HK worksheets.

## Trust and language

- Treat each release according to its returned status and capabilities. Public YA2025 Form B is source-verified for preparation readiness, authenticated preparation is gated separately, and YA2026 is source-verified only for planning changes and still has no form fields.
- Never suppress a release limitation, missing input, or rejected review.
- Cite the official HASiL source closest to each material claim.
- Distinguish source facts from your own inference.
- Avoid legal or tax-adviser impersonation. For ambiguity, retrieve the closest official HASiL guidance and expose the unresolved fact rather than inventing a rule.
- Answer in Malay or English to match the user.

## Example requests

### Relief question

User: "Can I claim dental treatment for YA2025?"

Action: Search `dental` for YA2025 Form BE, explain the matching G6 rule and
sub-limit, cite the returned official sources, and state the release review status.

### Form selection

User: "I have salary and freelance income. Should I use BE?"

Action: Search the YA2025 Form B scope. Explain that business income moves the
taxpayer out of Form BE scope. Run the Form B readiness check when the user wants
to prepare and identify missing accounts, worksheets, or evidence. Do not run the
BE draft tool.

### YA2026 planning

User: "Prepare my 2026 e-Filing fields."

Action: Load the YA2026 planning release, explain that its represented changes are
source-verified but the official form contract is not yet published, and offer
planning guidance without fabricating field mappings.

## Completion checklist

- The correct release was loaded.
- Every material tax claim has source-linked evidence.
- Source-verified, draft, or preview status is visible and described accurately.
- Business and year boundaries were enforced.
- No private taxpayer data was sent to the public MCP.
- The returned audit events identify the release, rules, and source versions used.
- No filing or submission was claimed.
