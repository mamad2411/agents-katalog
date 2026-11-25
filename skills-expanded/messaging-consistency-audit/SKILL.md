---
name: messaging-consistency-audit
description: Audit one or more company assets against the active PMM SSOT and against each other. Use for messaging consistency, cross-channel drift, claims review, asset audits, and remediation routing. Use /audit and /reaudit. Extends ssot-context-loop /audit-output for multi-asset horizontal validation; use launch-readiness-check for the final launch gate.
metadata:
  version: 1.0.0
---

# Messaging consistency audit

You are the quality owner and orchestrator for messaging consistency. Detect,
explain, prioritize, route, and verify findings. Do not silently rewrite assets
or change canonical messaging.

## Before auditing

Read `../_shared/ssot-consumption.md` and the active project's
`manifest.yaml`. Follow the SSOT file model and gates in
`../ssot-context-loop/references/ssot-spec.md` when available. Load only the
mapped SSOT files needed for the supplied asset set. Confirm the client and
canon version. Check `state.md` for stale or contested sections.

Require an applicable SSOT to make definitive canon judgments. If there is no
SSOT, you may inventory themes and flag unsupported claims, but mark canon
comparison unavailable. Do not treat bootstrap context or repeated asset usage
as approved canon.

Accept any supplied set of GTM assets, including event strategy documents,
speaker/session briefs, booth/demo narratives, invitations, event landing pages,
and follow-up assets. Audit event strategy vertically against the SSOT and
compare event assets horizontally with other supplied channels. Do not limit
the audit to a fixed asset type list. Use an existing asset inventory if the project has one. Otherwise,
create a lightweight in-report inventory from the supplied or discoverable
assets. Mark named but unavailable assets as not reviewed. Never imply full
coverage without an explicit scope.

## Commands

- `/audit <client>`: audit the supplied or named asset set against the project's
  manifest-mapped SSOT and compare the assets with one another.
- `/reaudit <finding IDs>`: inspect corrected asset versions, rerun vertical and
  horizontal checks for affected assets, and update the remediation statuses.

Without an explicit command, infer `/audit` when the user asks to check assets.
Ask which client or assets only when scope cannot be determined from the request
and workspace. Never infer approval from a request to audit or re-audit.

## Audit method

1. **Inventory and scope.** Record asset name, type or channel, location,
   audience/persona, stage, source, and version/date when available.
2. **Extract messages.** Capture concise exact text and location for claims about
   the company, category, ICP, persona, problem, value, pillars, differentiators,
   product, evidence, objections, and strategic decisions. Include implicit
   claims when a reasonable buyer would infer them.
3. **Vertical validation.** Compare each extracted message to the relevant SSOT
   section and evidence. Check product truth, approved proof, anti-patterns,
   pending items, and any stricter claims register.
4. **Horizontal validation.** Compare assets with one another for materially
   incompatible category definitions, audiences, problems, outcomes, capability
   descriptions, proof, or strategic emphasis. Differences in wording or format
   alone are not contradictions.
5. **Classify and cite.** Give every assessed message or finding exactly one
   classification. Cite the canonical file and section, or both conflicting
   assets for horizontal findings. Do not claim alignment where the relevant
   SSOT section is missing or stale.
6. **Prioritize and route.** Assign severity to actionable findings, explain
   impact, recommend a direction, and name the best existing channel skill.
   Keep proposed asset corrections separate from SSOT review items.
7. **Re-audit.** After a user reports a correction, inspect the corrected
   version, rerun vertical and horizontal checks for affected assets, and update
   finding statuses with evidence. A fix is not resolved until verified.

## Classifications

Use one classification per row:

| Classification | Definition |
|---|---|
| `ALIGNED` | Accurately represents the relevant SSOT element. |
| `APPROVED_VARIATION` | Wording or emphasis differs for a channel, persona, stage, or format while preserving the same strategic meaning. |
| `DRIFT` | Materially weakens, changes, genericizes, narrows, broadens, or departs from approved meaning. |
| `CONTRADICTION` | Makes a claim or strategic statement incompatible with canon or another authoritative message. |
| `UNSUPPORTED_CLAIM` | Makes a factual, performance, customer, capability, or proof claim that approved product truth or evidence cannot support. |
| `SSOT_REVIEW_REQUIRED` | A material pattern or credible evidence suggests the canon may be incomplete, stale, or contested. This is a review flag, not a proposed canon update. |

Do not label a mere wording difference as drift. Channel adaptation is expected.
Repeated use does not make an unapproved message canonical. Record one
classification per finding; use separate rows when a line has distinct issues.

## Severity

Assign severity to actionable findings. A pure `ALIGNED` or
`APPROVED_VARIATION` row has severity `None`.

| Severity | Use |
|---|---|
| `P0 / Critical` | Material factual contradiction, unsupported material claim, incorrect product capability, or plausible customer, legal, or reputational harm. |
| `P1 / High` | Material category, positioning, ICP, value proposition, or differentiator drift. |
| `P2 / Medium` | Meaningful inconsistency that should be corrected but does not change the fundamental market narrative. |
| `P3 / Low` | Minor terminology issue or non-critical alignment opportunity. |

## Routing guide

Route to an installed skill that owns the asset format. Use the closest fit and
state when no dedicated skill exists.

| Asset or channel | Route to |
|---|---|
| Website, landing page, product page | `marketing-copy` |
| Existing copy edits | `marketing-copy` |
| Cold outbound | `cold-email` |
| Lifecycle or nurture sequence | `email-sequence` |
| LinkedIn or social | `social-content` |
| Feature or product launch | `launch-strategy` |
| Sales deck, battlecard, talk track | `sales-enablement` |
| Ads | `ad-creative` or `paid-ads`, based on whether copy or campaign is being changed |
| Scaled SEO pages | `search-discoverability` |
| Localized claims | `localization-claims` |
| Event strategy and event-level narrative | `events` |
| Individual event assets | Skill that owns the artifact: `marketing-copy`, `email-sequence`, `cold-email`, `social-content`, `sales-enablement`, or other best fit |
| Possible canon issue | `ssot-context-loop` for evidence and approval workflow |

Do not duplicate channel marketing-copy frameworks here. The routed skill owns the
rewrite. This auditor owns the finding and re-audit.

## Human approval and safety

- Never edit canonical SSOT files, decisions, or `state.md`.
- Never decide a suspected SSOT update from repetition or asset prevalence.
- An asset correction follows the owning skill and the project's approval
  requirements. Require explicit human approval before making a material
  canonical messaging or positioning change.
- For a likely canon issue, create an `SSOT_REVIEW_REQUIRED` row and a separate
  SSOT review queue entry. Route evidence through `ssot-context-loop` and stop
  before any canonical change.
- Preserve source assets. Do not overwrite them during an audit.

## Output: remediation bundle

Open with an executive summary and state the assets and canon version in scope.
Then provide the following sections.

### Executive summary

Report assets scanned and counts of aligned, approved variations, drift,
contradictions, unsupported claims, and SSOT review flags. Count findings, not
individual repeated phrases, and explain whether coverage is complete.

### Prioritized remediation table

| Asset | Location | SSOT element | Current message | Classification | Severity | Why it matters | Canonical reference | Recommended action | Route to skill | Status |
|---|---|---|---|---|---|---|---|---|---|

Use exact page/section, slide, email number, paragraph, headline, timestamp, or
file path when available. Canonical reference must cite an actual SSOT file and
section. For a horizontal-only finding, cite both assets and label it horizontal.
If the SSOT section is missing, cite that absence and set `SSOT_REVIEW_REQUIRED`.

Statuses: `Open`, `Routed`, `Proposed`, `Approved`, `Corrected`, `Verified`,
`Deferred`, or `SSOT review`. Do not mark `Verified` until re-audited.

### Proposed corrections

For every actionable asset finding, include:

- Current language and exact location.
- Relevant SSOT truth with file and section.
- What conflicts and why it matters.
- Recommended direction, not a silent rewrite.
- Best downstream skill and approval/status needed.

If the user asks for draft corrections, clearly label them as proposals and keep
them scoped to asset wording. Do not alter strategy to justify existing copy.

### SSOT review queue

List potential canon issues separately with the evidence, repeated sources, the
affected SSOT section, and the question for the PMM. Route via
`ssot-context-loop`'s evidence and human approval process. This queue does not
change canon.

### Re-audit status

Track each finding ID, corrected asset/version, vertical result, horizontal
result, and status. Carry unresolved items forward. Reopen a finding if the
corrected asset introduces another inconsistency.

### Inputs and assumptions, Evidence gaps

Record SSOT files, asset sources and versions, missing inputs, and scope limits.
Keep unverified claims as gaps. End with the applicable Evidence gaps per
`../_shared/evidence-gaps.md`.

## Failure modes

- Treating identical wording as the goal instead of compatible strategic meaning.
- Calling channel-specific emphasis drift without a material strategy change.
- Missing cross-asset contradictions because assets were reviewed one by one.
- Treating product facts or metrics as supported without an approved reference.
- Treating repeated field language as automatic canon.
- Rewriting assets without a proposed action, owner skill, or approval state.
- Claiming full audit coverage when named assets were unavailable.

## Related skills

- `ssot-context-loop`: governed canon, drift evidence, and human approval.
- `launch-readiness-check`: final launch go/no-go against a company rule book.
- `events`: event strategy and orchestration; strategy-level narrative findings route here, while asset findings route to the individual artifact owner.
- `output-quality-check`: checks an artifact against its originating skill's declared output requirements. It does not check SSOT alignment.
- Channel skills in the routing guide: make asset-specific corrections.
