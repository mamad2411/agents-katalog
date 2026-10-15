---
name: ubiquitous-business-logic
description: Extract and document core business rules, domain knowledge, edge cases, implementation oddities, deeplinks, and analytics instrumentation by analyzing the current conversation and codebase, writing `docs/UBIQUITOUS_BUSINESS_LOGIC.md` grounded in real code paths. Use when hidden logic needs codifying, a domain-specific technical decision needs its rationale documented, routes or deeplinks need mapping, or analytics params need auditing for screen, error, and track events. Do not use for terminology and glossaries; use `$ubiquitous-language` for those.
disable-model-invocation: true
---

# Ubiquitous Business Logic

## Outcome

The actual business rules, domain knowledge, edge cases, deeplinks, analytics instrumentation, and implementation oddities, as they exist in the codebase, extracted and centralized in `docs/UBIQUITOUS_BUSINESS_LOGIC.md`. The goal is not a generic architecture document; it is to make hidden product behavior easy to understand, verify, and maintain without losing precision.

## Inputs and preconditions

The current conversation's claims about behavior, the existing `docs/UBIQUITOUS_BUSINESS_LOGIC.md` when present, and the codebase. Ensure a `docs` directory exists in the project root before writing, creating it if needed.

## Workflow

```text
Conversation context
        |
        v
Existing docs/UBIQUITOUS_BUSINESS_LOGIC.md
        |
        v
Code search: rules, schemas, constants, routes, analytics
        |
        v
Trace enforcement: inputs -> guards -> persistence -> presentation -> events
        |
        v
Organize by bounded context / feature area
        |
        v
Write visual documentation with evidence tables
        |
        v
Final verification pass + short inline summary
```

1. Extract claims from the current conversation.
   Capture rules, constraints, policies, workarounds, edge cases, deeplink expectations, analytics requirements, and any stated rationale. Pay special attention to:
   - the reason the logic exists
   - the user-visible behavior
   - affected screens, routes, or flows
   - analytics events and required params
   - stated exceptions, overrides, and legacy behavior
   - places where the user says the code should behave differently than it currently does

2. Read the existing business logic document if it exists. Merge forward instead of overwriting:

   | Existing content status | Action |
   | --- | --- |
   | Still matches implementation | Preserve and refresh evidence if needed. |
   | More specific than new findings | Keep the specific version and add new supporting details. |
   | Contradicted by code | Record the discrepancy and cite the code evidence. |
   | No longer enforced | Move to `Retired Logic` only when the conversation or code explicitly supports retirement. |
   | Unverified but important | Keep it only if clearly marked as needing verification. |

3. Inspect the codebase for implemented rules. Prioritize searches in:
   - `use-cases` / `usecases`
   - `services` / `handlers`
   - `domain`
   - `validators` / `schemas`
   - `utils` / `helpers`
   - `constants` / `config`
   - `routes` / `navigation` / `linking` / `deeplink` / `deep-link`
   - `analytics` / `tracking` / `events` / `telemetry` / `instrumentation`
   - feature folders containing screens, controllers, view models, forms, or API clients

   Use code search patterns such as:

   ```text
   throw new
   return false
   return null
   if (
   switch (
   TODO|FIXME|NOTE|HACK|WORKAROUND|legacy|grandfather
   MAX_|MIN_|DEFAULT_|LIMIT_|THRESHOLD_|GRACE_
   track|analytics|event|screen|error|telemetry
   route|path|deeplink|deepLink|linking|url|scheme
   ```

4. Trace enforcement end to end. For each important rule, trace the path where possible:

   ```text
   User/API input
     -> validation or schema rule
     -> use case / service guard clause
     -> persistence or external API call
     -> UI/screen presentation
     -> deeplink behavior, if applicable
     -> analytics events, if applicable
   ```

   Document the concrete enforcement point, not just the call site. Guard clauses, thrown errors, validators, enum checks, and constants usually encode the real invariant.

5. Identify oddities, edge cases, and magic values. Actively look for:
   - complex `if/else` or `switch` logic
   - hardcoded IDs, dates, thresholds, status maps, and tenant-specific exceptions
   - workarounds for third-party API limits
   - legacy data handling and migration cutoffs
   - domain constraints that feel counter-intuitive
   - behavior that differs by platform, environment, app version, tenant, locale, or feature flag
   - error states that are intentionally suppressed, transformed, or tracked differently
   - analytics params that are conditionally included or renamed

6. Extract deeplinks and route behavior when the codebase contains route/linking behavior or the conversation asks for it. Look for:
   - app schemes, universal links, route paths, URL builders, navigation config, and link parsers
   - required, optional, deprecated, and ignored params
   - screen destinations and fallback behavior
   - auth or permission gates
   - error handling for malformed, expired, or unauthorized links
   - analytics fired when a link is opened, rejected, or redirected

   Treat deeplinks as product behavior. A route that silently redirects, drops a param, or requires a specific auth state is business logic.

7. Extract analytics instrumentation when the codebase contains analytics/tracking behavior or the conversation asks for it. Split analytics by event category:

   | Category | What to document |
   | --- | --- |
   | Screen events | screen/view events, screen names, route or component source, required params, optional params, firing conditions |
   | Error events | error names, error codes, failure surfaces, suppression rules, retry/fallback behavior, user-visible message mapping |
   | Track events | action events, event names, required params, optional params, triggering user/system action, dedupe or throttling behavior |

   For each event, document the source file and the condition that causes the event to fire. If event params are assembled across multiple helper functions, cite both the event call and the param builder.

8. Categorize findings by bounded context or feature area such as Billing, Identity, Inventory, Scheduling, Eligibility, Onboarding, Notifications, Navigation, Deeplinks, or Analytics. When a rule spans multiple areas, place it in the context where the business decision lives and cross-reference related enforcement locations in the evidence table.

9. Write or rewrite the document using the output contract below. Keep every section, even if some tables contain `None found` or `Needs verification` rows.

10. Return a short inline summary with:
    - the most critical rules found
    - the weirdest oddities uncovered
    - deeplinks or analytics coverage added
    - discrepancies between user claims and actual code behavior
    - any areas needing follow-up verification

### Investigation heuristics

- Start at guard clauses and thrown errors. These usually encode the real invariants.
- Read validation schemas for format rules, bounds, enums, and conditional requirements.
- Search comments near complex logic for `TODO`, `FIXME`, `NOTE`, and `HACK`.
- Inspect third-party integration code for business rules forced by vendor limitations.
- Treat constants and config files as likely sources of status maps, limits, grace periods, feature flags, and analytics names.
- Follow important domain values from input validation through persistence and outward-facing presentation.
- For deeplinks, test route matching mentally from URL shape to destination screen and fallback behavior.
- For analytics, verify both the event name and the params. A correct event with wrong or missing params is incomplete instrumentation documentation.

### Visual documentation patterns

Use these patterns to make the output easier to scan while preserving detail.

Context map, near the top of the generated document when multiple areas interact:

```text
[Eligibility] -> gates -> [Checkout]
[Checkout] -> emits -> [Billing Analytics]
[Deeplink] -> routes to -> [Plan Selection]
[Errors] -> maps to -> [User-facing Messages]
```

Rule lifecycle, for rules that move through multiple layers:

```text
Input constraint -> validator -> service guard -> persisted state -> UI outcome -> analytics event
```

Confidence labels, used consistently:

| Status | Meaning |
| --- | --- |
| Confirmed | Directly verified in code. |
| Partially confirmed | Some evidence found, but implementation path is incomplete. |
| Contradicted | Conversation or existing doc conflicts with current code. |
| Needs verification | Important claim exists but code evidence was not found. |
| Retired | Evidence shows the system no longer enforces this logic. |

## Constraints

- Preserve existing knowledge. Merge forward from the existing document instead of replacing it wholesale.
- Ground every claim in code. Include file names, functions, constants, schemas, route names, event names, or guard clauses wherever possible.
- Favor visual structure. Use diagrams, maps, checklists, matrices, and compact tables so readers can understand the system quickly.
- Separate product truth from implementation weirdness. Intended behavior, hacks, legacy support, vendor workarounds, and retired rules should not be mixed together.
- Be explicit about uncertainty. Mark behavior as `Confirmed`, `Partially confirmed`, `Contradicted`, or `Needs verification` based on the evidence found.
- Do not remove details. If information is still valid, keep it. If the code contradicts it, move it to discrepancies or retired logic only when evidence supports that change.
- Be precise. State the rule clearly, then explain why it exists when evidence supports it.
- Focus on business logic, not framework or infrastructure choices.
- Be honest about weirdness. If the code contains tenant-specific hacks or legacy cutoffs, document them directly.
- Keep retired logic limited to rules the system no longer enforces.
- Keep visual aids factual. Do not invent relationships just to make the document look complete.
- Prefer concise table rows with exact evidence over long prose paragraphs.

## Failure handling

- A claimed rule has no code evidence: keep it only when important, labeled `Needs verification`; never present it as `Confirmed`.
- The conversation says the code should behave differently than it does: record the gap in `Discrepancies & Open Questions`; do not document the wished-for behavior as current behavior.
- No deeplink or analytics infrastructure exists: keep the sections with `None found` rows rather than omitting them.

## Output contract

Write `docs/UBIQUITOUS_BUSINESS_LOGIC.md` with exactly this structure:

```md
# Ubiquitous Business Logic

## How to Read This Document

This document captures business behavior as implemented in code, not just intended product behavior.

| Label | Meaning |
| --- | --- |
| Confirmed | Directly verified in code. |
| Partially confirmed | Some evidence found, but the full path is incomplete. |
| Contradicted | Existing docs or conversation claims conflict with current implementation. |
| Needs verification | Important claim exists, but code evidence was not found. |
| Retired | Evidence shows the system no longer enforces this logic. |

## System / Context Map

```text
[Add a compact map of the relevant bounded contexts, flows, routes, analytics, and integrations.]
```

## Bounded Context: [Context Name, e.g., Billing]

### Quick Mental Model

```text
[Summarize the context in 3-8 lines: inputs -> decisions -> outputs -> analytics/deeplinks if applicable.]
```

### Core Business Rules

| Rule | Description & Rationale | Enforced In | Status |
| --- | --- | --- | --- |
| **Proration on Downgrade** | When a user downgrades mid-cycle, the remaining balance is credited to their account, not refunded to their card. *Rationale: Reduces transaction fees and prevents refund abuse.* | `SubscriptionService.downgrade()` | Confirmed |
| **Minimum Charge** | Invoices under $0.50 are deferred to the next billing cycle. *Rationale: Stripe minimum processing fees.* | `InvoiceGenerator`, `Constants.MIN_CHARGE` | Confirmed |

### Rule Flow / Decision Points

| Flow Step | Decision / Branch | Outcome | Evidence |
| --- | --- | --- | --- |
| Downgrade request | User is mid-cycle | Credit remaining balance to account | `SubscriptionService.downgrade()` |
| Invoice generation | Invoice total is below minimum charge | Defer invoice to next billing cycle | `InvoiceGenerator`, `Constants.MIN_CHARGE` |

### Edge Cases & Oddities

| Oddity | Description & Rationale | Location / Workaround | Status |
| --- | --- | --- | --- |
| **Legacy Grandfathering** | Users created before Jan 1, 2022, bypass the `max_projects` limit. *Rationale: Promised unlimited projects in early beta.* | `PlanValidator.canCreateProject()` | Confirmed |
| **The "Acme Corp" Hack** | If `tenantId == 'acme-123'`, skip email verification. *Rationale: Enterprise client has strict firewall blocking our verification emails.* | `AuthService.register()` | Confirmed |

### Domain Constants & Magic Numbers

| Constant / Value | Meaning | Rationale | Evidence | Status |
| --- | --- | --- | --- | --- |
| `MAX_RETRY_ATTEMPTS = 3` | Number of retries before lockout. | Upstream API locks accounts after 4 failures. | `AuthConstants.MAX_RETRY_ATTEMPTS` | Confirmed |
| `DEFAULT_GRACE_PERIOD_DAYS = 7` | Days a user has to update an expired card before losing access. | Standard billing grace period. | `BillingConfig.DEFAULT_GRACE_PERIOD_DAYS` | Confirmed |

### Deeplinks & Routes

| Deeplink / Route | Destination Screen | Required Params | Optional Params | Guards / Fallbacks | Analytics | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `app://billing/invoice/:invoiceId` | Invoice Detail | `invoiceId` | `source` | Requires authenticated user; unauthorized users are redirected to login. | `deeplink_opened`, `invoice_viewed` | `linking.ts`, `InvoiceScreen` | Confirmed |

### Analytics Instrumentation

#### Screen Events

| Event | Screen / Source | Required Params | Optional Params | Fires When | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| `billing_invoice_screen_viewed` | Invoice Detail | `invoice_id` | `source`, `deeplink` | Invoice screen mounts after invoice load succeeds. | `InvoiceScreen.trackView()` | Confirmed |

#### Error Events

| Event | Error / Failure State | Required Params | Optional Params | Fires When | User-Facing Outcome | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `billing_invoice_load_failed` | Invoice lookup fails | `invoice_id`, `error_code` | `source` | API returns not found or permission denied. | Shows invoice unavailable state. | `InvoiceScreen.loadInvoice()` | Confirmed |

#### Track Events

| Event | User / System Action | Required Params | Optional Params | Fires When | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| `billing_downgrade_submitted` | User submits downgrade | `plan_id`, `account_id` | `coupon_id` | Downgrade CTA is submitted. | `BillingAnalytics.trackDowngradeSubmitted()` | Confirmed |

*(Repeat the Bounded Context block above for other contexts, e.g., Identity, Inventory, Scheduling, Eligibility, Navigation, Analytics, etc.)*

---

## Cross-Cutting Deeplink Inventory

| Deeplink / Route | Context | Destination | Required Params | Optional Params | Guards / Fallbacks | Related Events | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `app://billing/invoice/:invoiceId` | Billing | Invoice Detail | `invoiceId` | `source` | Login redirect when unauthenticated. | `deeplink_opened`, `invoice_viewed` | `linking.ts`, `InvoiceScreen` | Confirmed |

## Cross-Cutting Analytics Inventory

### Screen Events

| Event | Context | Screen / Source | Required Params | Optional Params | Fires When | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `billing_invoice_screen_viewed` | Billing | Invoice Detail | `invoice_id` | `source`, `deeplink` | Invoice screen mounts after invoice load succeeds. | `InvoiceScreen.trackView()` | Confirmed |

### Error Events

| Event | Context | Error / Failure State | Required Params | Optional Params | Fires When | User-Facing Outcome | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `billing_invoice_load_failed` | Billing | Invoice lookup fails | `invoice_id`, `error_code` | `source` | API returns not found or permission denied. | Shows invoice unavailable state. | `InvoiceScreen.loadInvoice()` | Confirmed |

### Track Events

| Event | Context | User / System Action | Required Params | Optional Params | Fires When | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `billing_downgrade_submitted` | Billing | User submits downgrade | `plan_id`, `account_id` | `coupon_id` | Downgrade CTA is submitted. | `BillingAnalytics.trackDowngradeSubmitted()` | Confirmed |

## Codebase Evidence & Verification

| Rule / Concept | Context | Primary Implementation | Supporting Evidence | Status |
| --- | --- | --- | --- | --- |
| Proration on Downgrade | Billing | `services/subscription.ts` | `SubscriptionService.downgrade()` credits account balance. | Confirmed |
| Legacy Grandfathering | Identity | `utils/legacy-checks.ts` | Hardcoded date `2022-01-01` found. | Confirmed |

## Discrepancies & Open Questions

| Claim / Expectation | What Code Does | Evidence | Recommended Follow-Up |
| --- | --- | --- | --- |
| [Conversation or existing doc claim] | [Actual implementation] | `[file/function]` | [Clarify, fix code, or update product expectation] |

## Retired Logic

| Legacy Rule | Replaced By / Removed Because | Evidence | Status |
| --- | --- | --- | --- |
| **Manual Invoice Approval** | Removed. All invoices are now auto-charged. | Code was stripped from `InvoiceService` in PR #402. | Retired |
```

### Final checks

Re-read the generated document before finishing.

- Ensure the file is saved strictly as `docs/UBIQUITOUS_BUSINESS_LOGIC.md`.
- Ensure generic technical details are omitted in favor of actual domain constraints.
- Ensure the `System / Context Map` and `Quick Mental Model` sections make the document easier to understand without simplifying away important details.
- Ensure each bounded context keeps the required tables, even when there are no deeplinks or analytics events found.
- Ensure deeplinks include destination, required params, optional params, guards/fallbacks, related analytics, evidence, and status.
- Ensure analytics are split into `Screen Events`, `Error Events`, and `Track Events`, with required and optional params documented separately.
- Ensure the `Edge Cases & Oddities` section is brutally honest about hacks and workarounds found in the code.
- Ensure the retired section contains only rules the system actively no longer enforces.
- Ensure every non-obvious claim has code evidence or is explicitly marked as needing verification.
