---
name: user-flows
description: End-to-end user task journey modeling, multi-branch decision trees, edge-case identification, error recovery loops, and Mermaid state flowcharts.
---

# User Flows Engineering & Task Journey Contract

## 1. Purpose
Design, map, and audit end-to-end user task flows, interaction journeys, and decision branches across product surfaces. Eliminate dead ends, minimize cognitive friction, ensure graceful error recovery loops, and formalize clear state transition models using standardized diagrammatic notation (Mermaid).

---

## 2. Use When
- Designing new user experiences, onboarding journeys, multi-step wizards, or transactional checkout funnels.
- Identifying and eliminating dead ends, orphaned states, and infinite loops in existing features.
- Mapping state transitions across asynchronous background events (e.g. email verification, payment processing, KYC webhook).
- Establishing clear specifications for engineering implementation and QA acceptance test scenarios.

---

## 3. Do Not Use When
- Designing visual styling, CSS tokens, or color palettes (use `design-tokens` or `design-system`).
- Auditing low-level pixel diffs or layout rendering (use `visual-regression` or `visual-qa`).
- Simple static content pages without multi-step decision branches or interactive workflows.

---

## 4. Required Context
Before mapping user flows, obtain:
1. **User Goal & Persona / JTBD**: Primary objective the user seeks to accomplish (Job-To-Be-Done).
2. **System Pre-Conditions**: User authentication state, device type, network connectivity, feature flags, permissions.
3. **Trigger & Entry Points**: Deep link, push notification, contextual CTA, global navigation.
4. **Success & Exit Criteria**: Measurable business/task completion state, confirmation artifacts, analytics events.

---

## 5. Procedure

### Step 1: Happy Path (Primary Task Flow)
1. Define the ideal, friction-free sequential path from entry point to goal achievement.
2. Minimize interaction steps: eliminate redundant inputs, defer non-essential profile completion, and leverage defaults.
3. Identify all system actions (data fetching, validating, computing) versus user actions (tapping, filling, deciding).

### Step 2: Decision Trees & Alternative Branches
1. Map every user choice and conditional system fork:
   - Authenticated vs. Guest / Anonymous users.
   - Permissions granted vs. denied (camera, location, notifications).
   - Validation success vs. failure.
   - Payment method variants (Credit Card, Apple Pay, Bank Transfer, Invoice).
2. Document explicit branching criteria at each decision diamond.

### Step 3: Edge Cases, Interruptions & Error Recovery Loops
1. Map all potential failure states and edge cases:
   - Network timeout / offline mode.
   - Session expiration during multi-step forms.
   - Payment declined / invalid OTP / duplicate submission.
2. Guarantee that every error state has an explicit recovery loop (e.g., retry button, alternative payment method, save draft and resume later).
3. Strictly prohibit dead ends (screens with no actionable forward or backward navigation).

### Step 4: Asynchronous & Cross-Channel Handoffs
1. Map background tasks and external interruptions:
   - 2FA SMS / authenticator app switching.
   - Email magic link verification.
   - Webhook-driven asynchronous status updates.
2. Specify loading, polling, and push-driven state transitions while the user awaits async confirmation.

### Step 5: Diagrammatic Formalization & Documentation
1. Formalize the flow using Mermaid syntax (`flowchart TD` or `stateDiagram-v2`).
2. Label each node with its screen name or system state, and each edge with the triggering event.
3. Review against usability heuristics and cognitive load constraints.

---

## 6. Decision Rules
1. **Zero Dead Ends**: Every screen or state must have at least one valid path forward, an explicit cancellation/exit path, or a recovery loop.
2. **Preserve User Input on Failure**: In any error or validation loop, previously entered valid user data must be preserved. Never force a user to re-enter unaffected fields.
3. **Explicit Undo / Cancel Mechanisms**: Destructive or irreversible actions must provide either an explicit confirmation step or a timed undo window.
4. **Clear Feedback on Long-Running Steps**: Any transition exceeding 1.0 second must specify a loading state; any step exceeding 10 seconds must offer background processing with progress indicators.

---

## 7. Evidence Required
- **Mermaid Flow Diagram**: Complete syntactically valid flowchart with labeled nodes and transitions.
- **Branch Completeness Table**: Matrix documenting nominal path, alternate paths, and error recovery routes.
- **Dead-End Audit**: Formal verification confirming zero orphaned terminal states outside intentional exit points.

---

## 8. Output Contract
A production user flow deliverable must contain:
1. Formal User Flow Specification (`templates/user-flow-spec.md`).
2. Embeddable Mermaid diagram source code.
3. Table of interaction states and error recovery policies.
4. Acceptance criteria for QA test case generation.

---

## 9. Stop Conditions
- All entry points reach valid terminal states (success, abandonment, save-for-later).
- 100% of error states have defined recovery paths.
- Mermaid diagram renders without syntax errors.

---

## 10. Escalation Rules
- Escalate to Product Management if business rules require mandatory user data collection that causes excessive drop-off friction.
- Escalate to Security/Compliance Lead if authentication or KYC legal requirements conflict with streamlined user flows.
