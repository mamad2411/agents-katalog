---
name: test-scenarios
description: "Generate a sign-off-ready test plan from PRD, Figma designs, and Jira epics. PM-first perspective: validates the feature ships in the right state, the user experience holds under failure, and the business is protected. Covers happy path, validation, error recovery, integration failures, financial accuracy, state transitions, and access control. Outputs prioritised manual test cases with a PM sign-off gate."
---

# Write Test Cases — PM Validation Mode

## Purpose

Help a PM answer one question: **is this feature ready to ship, and what do I need to see before I say yes?**

The output is a structured test plan the PM can hand to the team, walk through in a review session, or use to run checks themselves. Every case maps to a product promise. Every expected result is something a non-engineer can observe. The sign-off gate is what the PM holds the team to before approving launch.

---

## Core principles

**1. Start from the product promise, not the code.**
Every test case should trace back to something the feature is supposed to do for the user. If you cannot connect a test to a user benefit or a business protection, question whether it belongs in the PM's test plan.

**2. Expected results must be observable without engineering tools.**
"API returns 200" is an engineering check. "User sees a success screen with the confirmed amount and a reference number" is a PM check. Frame expected results as what a person looking at the product would see, hear, or receive. Where backend verification is needed, note it explicitly as an engineering check alongside the user-facing assertion.

**3. For every flow that works, test what happens when it breaks.**
The error path is where users lose trust. A broken success screen is bad. A broken error screen — one that leaves the user stranded with no next step — is worse. Every happy path needs at least one failure counterpart.

**4. Flag what the spec does not answer.**
If the PRD does not describe what happens when the payment fails, the error state does not exist in the product. Write the test case anyway, mark it `[SPEC GAP]`, and surface it to the designer and engineer before testing begins. Untested states ship as incidents.

**5. Pre-conditions must be set up, not assumed.**
Do not write "user has completed onboarding." Write "User account: test-user-01, status: verified, balance: $500 — set up via [method]." Anyone on the team should be able to reproduce the setup independently.

**6. The sign-off gate is a ship decision, not a formality.**
Define in advance what "done" looks like — which cases must pass, which open issues are acceptable, who gives the final approval. If the gate is vague, sign-off is meaningless.

---

## Input processing

### Mandatory inputs

The quality of the test plan is directly limited by the inputs provided. Before generating any test cases, confirm what is available:

| Input | What it unlocks | If unavailable |
|-------|----------------|----------------|
| **PRD** | Acceptance criteria, business logic, constraints, compliance requirements | Test plan cannot map to product requirements — all cases will be inferred, not traced |
| **Figma** | UI states, error screen copy, empty states, loading states, navigation flows | UI-facing assertions will be incomplete — error copy, loading behavior, and edge states will be marked `[SPEC GAP]` |
| **Jira epic / stories** | Scope boundaries, cross-team dependencies, definition of done, known risks | Integration points and adjacent feature impact will be unknown |

If any of these is missing, ask the user to provide it or confirm explicitly that it is not available. Then flag in the test plan what coverage is missing as a result.

### Extracting from PRD
- List every acceptance criterion — each one must map to at least one test case
- Note every constraint or limit — these define boundary tests
- Identify every third-party dependency — each needs a failure test
- Extract every compliance or regulatory requirement — these are always P0

Flag if the PRD does not cover:
- What the user sees when an action fails
- What happens when a partner system is unavailable
- How the user recovers from an error
- Behavior at edge inputs (zero value, maximum value, unusual characters)

### Extracting from Figma
For every screen, extract each distinct state:
- **Empty state** — what appears before data loads or when there are no results?
- **Loading state** — is there a spinner or skeleton? What triggers it?
- **Success state** — the designed happy path
- **Error state** — form errors, action failures, permission blocks
- **Warning or partial state** — data available but incomplete or stale
- **Edge display states** — long text, maximum list items, zero balance

Also extract:
- Exact copy for all error messages, confirmations, and labels (these become assertion anchors)
- Navigation on each screen (back button, close, deep link entry)
- Conditional visibility — what is shown or hidden based on user state?

Flag if Figma is missing error states, empty states, or loading states for any interactive element.

### Extracting from Jira
- What is explicitly in scope and out of scope?
- Which other systems, teams, or features does this touch?
- What is the definition of done?
- Are there known risks or open questions in the ticket comments?
- What happens if this feature is rolled back?

---

## Test categories

Generate cases across all applicable categories. If a category does not apply, state why rather than silently skipping it.

### 1. Happy path
The feature works as designed for the primary user journey. Cover all distinct entry points and user types — if there are 3 ways to reach this feature, test all 3.

### 2. Input and boundary checks
For every user input:
- Left blank when required
- Below the minimum allowed value or length
- Above the maximum allowed value or length
- Wrong format (email without @, ID with letters where digits are expected)
- Valid edge case — exactly at the maximum allowed value

Expected result for each: the exact error message shown to the user, or `[SPEC GAP]` if not defined in the PRD or Figma.

### 3. Error recovery
What happens when something goes wrong and the user tries to continue:
- Action fails — can the user retry from where they stopped, or do they lose progress?
- Session expires mid-flow — are they redirected correctly? Is their progress saved?
- User taps the button twice quickly — does it submit twice, or is it handled safely?
- User goes back and comes forward again — does the screen reflect the correct state?
- User fixes a validation error and resubmits — does the error message clear?

### 4. Partner and integration failures
Every call to an external system can fail. For each integration point in the feature:
- The partner takes too long to respond — what does the user see?
- The partner returns an error — is the message user-friendly, or does it expose technical details?
- The partner is completely unavailable — is there a fallback, or is the feature blocked entirely?

This is a PM check because the answer determines whether a partner outage creates a user-visible incident.

### 5. State and flow sequencing
Users do not always follow the intended path:
- User navigates back mid-flow — does the previous screen show the right state?
- User opens the same flow in two tabs or sessions — what happens?
- User leaves and returns after 30 minutes — where does the flow resume?
- User tries to do step 2 before step 1 is complete — are they blocked with a clear message?
- User submits the same action twice (same payment, same form) — is the duplicate caught?

### 6. Financial and data accuracy
Apply to any feature involving money, amounts, fees, limits, or records:
- The amount shown to the user matches what is charged or credited
- Fees, taxes, and charges are calculated correctly at the boundaries (just under the limit, at the limit, just over)
- A refund or reversal restores exactly the right amount
- Limits are enforced at the time of the action, not just at setup
- What the user sees in the app matches what is recorded in the backend — check for discrepancies, not just success

### 7. Access and permissions
- A user who is not logged in cannot access protected screens
- A user without the required status (verification incomplete, account restricted) is declined with a clear reason and a next step
- A user cannot view or act on another user's data
- A logged-out session cannot be reused

### 8. Cross-platform checks (apply if the feature has a UI)
- The feature works on both primary platforms (iOS and Android, or web and mobile)
- Key interactions work on smaller screen sizes
- The feature does not break in dark mode if the product supports it

---

## Test case format

| Field | What to write |
|-------|--------------|
| **TC ID** | `TC-[FEATURE PREFIX]-[NUMBER]` |
| **Category** | One of the 8 categories above |
| **Scenario** | Specific — not "happy path" but "user with verified account completes first-time purchase with saved card, sufficient balance" |
| **Pre-conditions** | Exact account state, feature flag status, test data values — no assumptions |
| **Steps** | Numbered, one action per step, with the immediate observable result noted inline where relevant |
| **Expected result** | What a person looking at the product sees — UI state, message text, amount displayed. Add "Engineering check:" for any backend verification needed alongside it. |
| **Maps to** | The PRD acceptance criterion or Jira story this test validates |
| **Priority** | P0 / P1 / P2 |
| **Notes** | Spec gaps, setup dependencies, known risks |

**Priority definitions:**
- **P0 — Must pass before ship**: Feature's core promise broken, user loses money or data, user is stranded with no next step, compliance requirement unmet
- **P1 — Must pass before GA**: Important flows broken, error states leave users confused, partner failure has no graceful handling
- **P2 — Fix in next cycle**: Edge cases with low user frequency, non-critical polish, minor copy or display issues

---

## Output structure

```
## Test Plan: [Feature Name]

**PRD**: [link or "not provided — coverage is inferred"]
**Figma**: [link or "not provided — UI state assertions are incomplete"]
**Jira**: [link or "not provided — scope boundaries and dependencies unconfirmed"]
**Date**: [today]
**Feature owner**: [PM name]
**Test environment**: [staging / UAT / production — controlled access]

---

### Spec gaps
[States or behaviors not defined in the inputs. Each is an untested risk that must be resolved before ship.]
1. [What is missing and which input should define it]

---

### Pre-test setup
[What must be true before any test runs — test accounts, feature flags, partner sandbox configuration, data setup method]

---

### Test suite

| TC ID | Category | Scenario | Pre-conditions | Steps | Expected Result | Maps to | Priority | Notes |
|-------|----------|----------|----------------|-------|-----------------|---------|----------|-------|

---

### Coverage summary

| Acceptance criterion | Test cases | Status |
|----------------------|------------|--------|
| AC-01: [criterion]   | TC-X-001, TC-X-002 | |
| AC-02: [criterion]   | TC-X-003 | |

---

### Sign-off gate

Before approving ship, confirm:
1. All P0 cases executed and passed
2. All P1 cases executed — any failures have a documented workaround or accepted risk with owner named
3. [Feature-specific condition — e.g., "financial accuracy cases verified by [team]"]
4. All spec gaps resolved or explicitly accepted as known risk before GA
5. [Who gives final sign-off and by when]

---

### What this plan cannot verify
[Risks that require additional spec, a different environment, or partner confirmation to test]
```

---

## Anti-patterns — flag and fix

| Anti-pattern | Example | Fix |
|---|---|---|
| Vague expected result | "Screen should display correctly" | Name the specific element, its state, and the exact text |
| Chained pre-conditions | "Assuming prior test completed" | Write as standalone setup — specify the exact account state |
| Generic input values | "Enter a valid email address" | Use a specific value, plus a boundary case value |
| No failure counterpart | Only a success test for a user action | Add at least one case for what happens when it fails |
| Unverifiable assertion | "Performance should be acceptable" | Specify the observable threshold — "page loads before the spinner disappears" |
| Missing error copy | "User sees an error" | Specify the exact message or mark `[SPEC GAP]` |
| Unmapped test | Test case with no AC or story reference | Every case must trace to a requirement |

---

## Domain modules

Apply the relevant module for the product area. These are the failure modes and accuracy checks a generic template misses.

### Payments and money movement
- Duplicate submission: same payment initiated twice produces exactly one charge — not two, not zero
- Failed debit with successful credit (or vice versa): the user is not left in a partially transacted state without notification
- Notification accuracy: the amount, recipient, and timestamp in the notification match the transaction record exactly
- Refund treatment: the reversal restores the right amount — verify whether fees and taxes are refunded or retained per the product policy
- Limit enforcement: checked at the moment of the transaction, not at account setup — test at the exact limit and just over it

### Lending and credit
- Eligibility is evaluated at the time of the request, not cached from a prior check
- The repayment amount shown to the user matches what is actually charged on the due date
- All required disclosures and consent steps are present, timestamped, and verifiable
- A missed payment produces the correct user communication and account state change

### Insurance
- Policy state changes (active to lapsed, claim submitted to approved) produce the correct UI update and user notification
- A claim can only be filed for events and periods the policy covers — test a claim just outside the coverage window
- Downloaded policy documents match the live policy data — verify key fields, not just that the file opens
- Two active policies do not show conflicting information on the same screen

### Onboarding and identity verification
- Each third-party verification step (ID check, document scan, database lookup) has a user-friendly failure path — not a blank screen or an error code
- A user who drops out mid-onboarding and returns picks up at the correct step, with their previous inputs intact
- A user who has already onboarded cannot start the process again and create a duplicate record
- A declined verification result shows the user a clear next step — not a dead end

### Real-time data feeds (prices, inventory, availability)
- The UI communicates clearly when data is delayed or unavailable — no silent stale display
- Threshold alerts fire at the exact configured value, not approximately
- Two users or sessions acting on the same item simultaneously produce a deterministic outcome for both
- Behavior at time boundaries (market open, sale end, session expiry) is defined and tested

### E-commerce and marketplace
- Cart contents persist across session expiry, device switch, and a failed payment
- Two users attempting to purchase the last unit simultaneously: exactly one succeeds, the other receives a clear "no longer available" outcome
- A price change between cart addition and checkout is communicated to the user before they confirm payment
- Each order status change (confirmed, shipped, delivered, returned) triggers the correct notification and UI update

### SaaS and subscription
- Feature access changes at the exact moment of plan upgrade or trial expiry — no gap or overlap
- Features removed on downgrade are inaccessible immediately; data from the higher tier is retained or clearly archived, not silently deleted
- The invoice reflects actual usage at the correct tier price — test at tier boundaries
- A failed payment during the grace period produces the correct access state and user communication

### Developer tools and APIs
- Requests over the rate limit return a clear, actionable error with retry guidance — not a silent failure
- An expired or revoked token returns the correct error response — not an internal server error
- Webhooks retry on failure and the consumer handles a duplicate delivery without creating a duplicate record
- Paginated endpoints return a clear end-of-results signal on the last page; an empty result returns an empty list, not an error

---

## Optional add-ons

Offer these after delivering the core test plan. Do not include them by default.

**Regression map** — "Want me to identify which existing flows this feature touches and suggest checks to run on them?"
Use when: the feature changes shared state, modifies a core flow, or touches a system used by other features.

**Automation candidates** — "Want me to flag which cases are candidates for automated testing?"
Use when: the team has a test automation practice and wants to identify scripted vs exploratory coverage.

**Test data setup** — "Want me to write the setup instructions or scripts for the pre-conditions?"
Use when: pre-conditions are complex, require specific account states, or need to be repeatable across test runs.

**Exploratory testing brief** — "Want me to write a 30-minute exploratory testing brief for a team member to run alongside the scripted cases?"
Use when: the feature is complex, has many edge states, or is in a high-risk area. Exploratory testing finds what scripted cases miss.
