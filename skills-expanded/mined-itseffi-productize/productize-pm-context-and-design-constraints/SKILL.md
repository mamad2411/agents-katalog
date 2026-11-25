---
name: productize-pm-context-and-design-constraints
description: >-
  PM context and design constraints. Use when the user needs a product workflow for
  stakeholder management related to pm context and design constraints. Trigger terms:
  product-design, requirements, design-constraints, stakeholder-management.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# PM context and design constraints

## Productize Preamble

Before producing the artifact, implementation step, or code change, classify the work:

- **User/persona**: founder, product leader, AI PM, AI builder, stakeholder, or mixed/unknown.
- **Product stage**: idea, validation, PMF search, growth, scale, pivot, or unknown.
- **Artifact mode**: strategy memo, PRD, research plan, positioning, experiment, deck, roadmap, execution brief, diagnostic, or decision record.
- **Artifact format**: Markdown for short, repo-native, diff-sensitive artifacts; self-contained HTML for long, visual, shareable, interactive, or explicitly requested artifacts.
- **Evidence standard**: what is known, assumed, missing, and risky.
- **Decision mode**: recommend, ask for a blocking input, or proceed with explicit assumptions.

Operating rules:

1. Do not produce generic product strategy filler. Tie every recommendation to the user's context, evidence, stage, and decision pressure.
2. Separate facts from assumptions. Convert high-risk assumptions into tests, research prompts, or instrumentation.
3. Search existing context, attached docs, repo files, or prior Productize artifacts before inventing new structure when those sources are available.
4. Ask only for inputs that materially change the output. If the next step is obvious, proceed and state assumptions.
5. If another Productize skill is a better fit, name it and explain the routing in one sentence before continuing.
6. Enforce the output contract for this skill. Produce the artifact, implementation step, verification evidence, or code change; do not stop at a meta-explanation of the method.
7. End with the concrete next action, decision owner, validation step, metric, or artifact handoff when applicable.
8. Use the user's saved Productize preferences when available, but do not let stale preferences override explicit instructions in the current request.
9. If you must ask a blocking question, use this compact format: `AskUserQuestion: <one question> Why it matters: <decision it changes>`.
10. Record completion status for durable work as `completed`, `blocked`, `deferred`, or `needs-review` when runtime hooks are available.

Artifact format policy:

- Default to Markdown for short notes, repo-native documentation, changelog fragments, or artifacts where clean source diffs matter.
- Use a self-contained HTML file when the user asks for HTML, the artifact is likely to exceed about 100 lines, the reader needs diagrams/tables/comparisons/screenshots, the artifact is meant to be shared, or interaction/export controls would help the user stay in the loop.
- Route by product job first, then choose the format. Do not create a generic HTML workflow when a Productize playbook, gate, or routed skill owns the work.
- HTML artifacts must be local-first and portable: one file, embedded CSS/JS, no remote dependencies unless explicitly requested, readable without a dev server, responsive, accessible, and easy to skim.
- Prefer semantic sections, tables, SVG diagrams, annotated code blocks, status chips, collapsible detail, and copy/export buttons when they improve review speed. Avoid decorative complexity that hides the decision.
- For implementation work with ambiguities, use `$implementation-notes` when the user asks for a running notes file, especially `implementation-notes.html` or `implementation-notes.md`.

Runtime hooks, if available:

- Use `productize-workflow start "<user request>"` at the beginning of durable product work; it restores context, routes the request, records the session, and returns the required artifact contract.
- Use `productize-workflow complete --id <id> --status completed|blocked|deferred|needs-review --artifact-type <type> --summary <summary>` before ending durable product work; it records the artifact, saves context, and logs completion status.
- Use `productize-update-check --strict` at the start of maintenance, setup, release, or generated-output work.
- Use `productize-config` to read or write user/team preferences such as persona, artifact mode, evidence threshold, or update-check policy.
- Use `productize-session-log` to record important workflow decisions.
- Use `productize-artifact-log` when a durable artifact is produced.
- Use `productize-context-restore` before restarting long-running product work from scratch.
- Use `productize-context-save` after producing a durable strategy, research, spec, or stakeholder artifact.
- Use `productize-registry-search` or `productize-skill-router` when routing is ambiguous.
- Use `productize-completion-status` to log whether the workflow completed, blocked, deferred, or needs review.

Telemetry standard:

- Keep telemetry local by default in `.productize/` or `PRODUCTIZE_STATE_DIR`.
- Log artifact type, routing decision, evidence gaps, and completion status; do not log secrets or private customer data unless the user explicitly asks for it.

Current skill metadata:

- **Skill**: `pm-context-and-design-constraints`
- **Lifecycle**: Design
- **Category**: Design
- **Primary artifact**: PM context and design constraints UX/design review with findings, constraints, fixes, and acceptance checks

Use this skill to run the Productize prompt contract for **PM context and design constraints**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- {{PM_CONTEXT}}
- {{USER_GOALS}}
- {{SUCCESS_METRICS}}
- {{BUSINESS_REQUIREMENTS}}
</provided_inputs>

GOAL
Produce a high-quality deliverable for: PM context and design constraints.
Success metric:
- Completes all required tasks and decision logic from the prompt instructions.
- Output is specific, evidence-based, and actionable.
- Output follows the required structure exactly.

CONSTRAINTS
- Use only provided inputs and clearly state assumptions when information is missing.
- Do not skip required analysis steps, sections, or validation logic.
- Keep recommendations/outputs grounded in the input context; avoid generic filler.
- Translate `{{PM_CONTEXT}}`, `{{USER_GOALS}}`, `{{SUCCESS_METRICS}}`, and `{{BUSINESS_REQUIREMENTS}}` into actionable design constraints.
- Extract explicit constraints across user, technical, business, timeline/resource, and scope dimensions.
- Identify implicit constraints (platform conventions, existing patterns, performance, accessibility, brand/system, privacy/security).
- Map success metrics to concrete design requirements and validation methods.
- Define project design principles, non-negotiables, and acceptable tradeoffs.
- Identify information gaps and produce prioritized clarifying questions.
- Define validation criteria (must-have, should-have, success signals, red flags), methods, timeline, and next actions.

FORMAT
Return exactly this structure:

<design_constraints>
<executive_summary>
**Project:** [Name]

**Core User Need:** [Primary problem we're solving for users]

**Primary Success Metric:** [Top metric that defines success]

**Key Design Constraints:**
1. [Constraint 1 - e.g., "Must launch by Nov 15 (hard deadline)"]
2. [Constraint 2 - e.g., "Must work offline for mobile users"]
3. [Constraint 3 - e.g., "Must meet WCAG 2.1 AA accessibility standards"]

**Biggest Unknowns:**
1. [Information gap 1 - e.g., "User segment not defined - designing for power users or beginners?"]
2. [Information gap 2 - e.g., "Technical integration with CRM not spec'd - what data can we access?"]

**Recommended Next Actions:**
1. [Action - e.g., "Clarify target user segment with PM"]
2. [Action - e.g., "Review technical integration specs with engineering"]
3. [Action - e.g., "Conduct user research on current pain points"]
</executive_summary>

<explicit_constraints>
## User Needs

**Primary User Goal:** [What users are trying to accomplish]

**Specific User Needs:**
1. [User need] - [Why this matters]
   - Example: "Complete tax filing in under 30 minutes" - Users are time-constrained, will abandon if too complex
2. [User need] - [Why this matters]
3. [User need] - [Why this matters]

**Jobs-to-be-Done:**
- When [situation], I want to [motivation], so I can [expected outcome]
- Example: "When filing my taxes, I want to quickly import my W-2 data, so I can avoid manual data entry errors"

**User Context:**
- **Technical proficiency:** [Beginner / Intermediate / Advanced]
- **Device usage:** [Mobile-first / Desktop-primary / Mixed]
- **Usage frequency:** [Daily / Weekly / Monthly / Annually]
- **Context of use:** [On-the-go / At desk / High-stress / Time-constrained]

**Design Implications:**
- [How user needs translate to design requirements]
- Example: "Users are time-constrained → Design for speed (autofill, smart defaults, minimal steps)"

---

## Technical Constraints

**Platform Requirements:**
- **Platforms:** [iOS, Android, Web, Desktop]
- **OS/Browser Support:** [Specific versions - e.g., iOS 14+, Android 10+, Chrome/Firefox/Safari latest 2 versions]
- **Screen sizes:** [Mobile (375-414px), Tablet (768-1024px), Desktop (1280px+)]

**Performance Requirements:**
- **Page load time:** [Target - e.g., <3 seconds on 4G]
- **Interaction responsiveness:** [Target - e.g., <100ms for button taps]
- **Animation performance:** [Target - e.g., 60fps]
- **Offline support:** [Required / Not required - if required, what functionality must work offline?]

**Integration Requirements:**
- **Systems to integrate with:** [CRM, Payment gateway, Analytics, etc.]
- **APIs available:** [What APIs can we use? What data can we access?]
- **Authentication:** [OAuth, SAML, API keys - what's supported?]

**Data Constraints:**
- **Data availability:** [What data is available in real-time vs. cached?]
- **Data format:** [JSON, XML, etc.]
- **Data limitations:** [Rate limits, data freshness, completeness]

**Design Implications:**
- [How technical constraints affect design]
- Example: "Offline support required → Design for sync states (loading, synced, sync failed), indicate what works offline"

---

## Business Requirements

**Regulatory Compliance:**
- [Regulation] - [Specific requirements]
  - Example: "GDPR - Must collect explicit consent for data processing, provide data export/deletion"
  - Example: "WCAG 2.1 AA - Must meet accessibility standards (color contrast, keyboard navigation, screen reader support)"

**Business Logic:**
- [Business rule] - [How it affects design]
  - Example: "Free trial users can access features A, B, C but not D, E - Must clearly indicate locked features"
  - Example: "Approval workflow requires manager sign-off for purchases >$1000 - Design approval flow with notifications"

**Monetization Requirements:**
- [Requirement] - [Design implications]
  - Example: "Freemium model with paywall after 3 exports - Design paywall that clearly communicates value of upgrade"
  - Example: "Ads on free tier - Design ad placements that don't disrupt core user flow"

**Operational Constraints:**
- [Constraint] - [Design implications]
  - Example: "Support only available Mon-Fri 9-5 EST - Design self-service help prominently for off-hours"
  - Example: "Manual approval process takes 24-48 hours - Design expectation-setting messaging"

**Design Implications:**
- [How business requirements affect design]

---

## Resource Constraints

**Timeline:**
- **Launch Date:** [Date - is this hard deadline or flexible?]
- **Why this date:** [Business reason - seasonal, competitive, contractual commitment]
- **Design timeline:** [How much time for design phase - research, ideation, validation]
- **What happens if we miss deadline:** [Opportunity cost, business impact]

**Team & Budget:**
- **Design team:** [X designers, skill sets]
- **Engineering team:** [X engineers, X sprints available]
- **Budget:** [Design/dev hours, research budget, tooling budget]
- **Dependencies:** [What are we waiting on? Other teams, external vendors?]

**Design Implications:**
- [How timeline/resources affect scope]
- Example: "6 weeks to design + 4 weeks to build → Focus on MVP, defer nice-to-haves to v2"

---

## Scope Requirements

**Must-Have (MVP Features):**
- [Feature] - [Why it's must-have]
  - Example: "Credit card payment support - Cannot launch e-commerce without ability to collect payment"

**Should-Have (Important but not blocking):**
- [Feature] - [Why it's important]
  - Example: "Saved payment methods - Improves returning user experience, but first-time users can still checkout"

**Could-Have (Nice-to-have if time allows):**
- [Feature] - [Why it's nice-to-have]
  - Example: "Gift wrapping option - Adds value but low usage expected"

**Won't-Have (Explicitly out of scope):**
- [Feature] - [Why we're not doing it]
  - Example: "Cryptocurrency payments - Too few users, high implementation complexity, defer to v2"

**Design Implications:**
- [How scope affects design priorities]
- Example: "MVP focused → Design core flow excellently, cut secondary features"

</explicit_constraints>

<implicit_constraints>
## Platform Conventions

[List platform-specific conventions that should be followed even if not explicitly stated]

**iOS:**
- Navigation bar at top, tab bar at bottom
- System fonts (San Francisco) and standard UI components
- Standard gestures (swipe back, pull to refresh)
- Haptic feedback for key interactions

**Android:**
- Material Design principles (FAB, bottom sheets)
- System back button behavior
- Material motion and elevation system

**Web:**
- Underlined links or clear visual distinction
- Breadcrumbs for deep hierarchy
- Search in header (typically top-right)
- Responsive design (mobile-first approach)

**Design Implication:** "Follow platform conventions to meet user expectations, don't reinvent standard patterns"

---

## Existing Patterns Users Expect

**Product-Specific Patterns:**
- [Pattern already established in our product]
- Example: "We always use bottom sheet for secondary actions - maintain consistency"

**Industry Conventions:**
- [Pattern users know from competitor products]
- Example: "E-commerce checkout follows: Cart → Shipping → Payment → Review → Confirmation"

**Design Implication:** "Leverage existing mental models, don't make users learn new patterns unnecessarily"

---

## Performance Expectations (Unstated)

- **Page load:** Users expect <3 seconds, abandon after 5 seconds
- **Interaction responsiveness:** Buttons/links respond <100ms (feels instant)
- **Animation:** 60fps for smooth motion (30fps feels janky)
- **Search results:** Return results <1 second (ideally instant)

**Design Implication:** "Design with performance in mind - minimize heavy assets, use lazy loading, show loading states"

---

## Accessibility Requirements (Often Assumed)

- **WCAG 2.1 AA minimum** (legal requirement in many jurisdictions)
- **Keyboard navigation:** All interactive elements keyboard accessible (tab order logical)
- **Screen reader support:** Semantic HTML, ARIA labels, alt text for images
- **Color contrast:** Text has 4.5:1 contrast ratio (large text 3:1)
- **Focus indicators:** Visible focus states for keyboard navigation
- **Touch targets:** Minimum 44x44px (iOS) / 48x48px (Android)

**Design Implication:** "Accessibility is non-negotiable - bake it in from the start, not an afterthought"

---

## Brand & Design System Constraints

- **Brand colors:** [Hex codes for primary, secondary, accent colors]
- **Typography:** [Font families, sizes, weights]
- **Voice & tone:** [Brand voice - professional, friendly, playful, etc.]
- **Design system components:** [Must use existing components, don't reinvent]
- **Design principles:** [Product design principles to follow]

**Design Implication:** "Stay within brand guidelines and design system, maintain consistency across product"

---

## Data Privacy & Security (Unstated Expectations)

- **Sensitive data:** Don't display in plain text (mask credit cards, SSNs, passwords)
- **Authentication:** Require login for personal data access
- **Session timeout:** Auto-logout after inactivity (typically 15-30 min)
- **Audit logging:** Track sensitive actions (for security and compliance)

**Design Implication:** "Design for security by default - mask sensitive data, require authentication, set expectations around timeouts"

</implicit_constraints>

<metric_driven_requirements>
For each success metric, translate into design requirements:

## Metric #1: [e.g., "Increase conversion rate by 10%"]

**Current Baseline:** [X]% conversion rate

**Target:** [Y]% conversion rate (10% relative increase)

**UX Outcomes Needed:**
- Reduce friction: Fewer steps, clearer CTAs, smart defaults
- Increase trust: Social proof, security badges, clear value proposition
- Improve clarity: Better copywriting, visual hierarchy, reduced cognitive load

**User Behaviors to Enable:**
- Users must understand value proposition within 5 seconds
- Users must complete key actions with minimal effort (ideally <3 clicks)
- Users must feel confident proceeding (reduce anxiety, increase trust)

**Friction to Remove:**
- Current friction: 12-field checkout form (reduce to 6 fields)
- Current friction: Unclear CTAs (test 3 CTA variants for clarity)
- Current friction: No trust signals (add security badges, testimonials)

**Design Requirements:**
1. Reduce checkout form from 12 to 6 fields (use smart defaults for the rest)
2. Test 3 CTA variants: "Buy Now", "Complete Purchase", "Checkout Securely"
3. Add trust badges above payment section (SSL, money-back guarantee, testimonials)
4. Improve visual hierarchy: Make CTA most prominent element on page (size, color, placement)

**Validation:**
- Usability testing: 90%+ of users complete checkout without confusion
- A/B test: New design increases conversion by 5-10%

---

## Metric #2: [e.g., "Increase feature adoption by 25%"]

**Current Baseline:** [X]% adoption

**Target:** [Y]% adoption (25% relative increase)

**UX Outcomes Needed:**
- Improve feature discoverability
- Clarify value proposition
- Support successful first-time use

**User Behaviors to Enable:**
- Users must notice the feature in normal workflows
- Users must understand why they should use it
- Users must succeed on first attempt

**Friction to Remove:**
- Hidden or buried entry points
- Jargon-heavy or vague copy
- Complex multi-step setup without guidance

**Design Requirements:**
1. Place feature entry point in primary navigation or key flow
2. Add contextual tooltip or nudge explaining value the first time it appears
3. Design a guided first-use flow or lightweight wizard
4. Provide clear success feedback and next-step suggestions

**Validation:**
- Usage analytics: Increase in first-time and repeat use
- Usability testing: Majority of users discover and use feature unaided

---

[Continue for all success metrics]

</metric_driven_requirements>

<design_principles>
## Project-Specific Design Principles

These principles guide tradeoff decisions for this project:

### 1. [Principle Name]: [Principle Statement]

**What This Means:**
[Explain the principle in plain language]

**Tradeoff Guidance:**
When we must choose between [X] and [Y], we prioritize [X] because [reason]

**Example:**
[Concrete example of how this principle guides a design decision]

**Example Principle: Speed Over Polish**
- **Statement:** "Ship functional, usable designs quickly. Refine aesthetics in v2."
- **What This Means:** Prioritize getting core functionality in users' hands over pixel-perfect visual design. Design must be usable and brand-consistent, but doesn't need to be visually stunning in v1.
- **Tradeoff:** When choosing between "thorough visual design exploration" vs. "get prototype to users fast", choose speed.
- **Example:** "For v1, use standard design system components and straightforward layouts. Save custom illustrations and micro-interactions for v2."

---

### 2. [Principle]: [Statement]

**What This Means:**
[Explain the principle]

**Tradeoff Guidance:**
[Which side wins in conflicts]

**Example:**
[Concrete application]

---

[Continue for 5-7 principles total]

## Non-Negotiable Qualities

These qualities cannot be compromised:

1. **[Quality - e.g., Accessibility Compliance]**
   - We will always meet WCAG 2.1 AA, even if it means additional design/dev time
   - Why: Legal requirement, user trust, inclusive design is a core value

2. **[Quality - e.g., Data Security]**
   - We will always prioritize user data security, even if it adds friction
   - Why: User trust is foundational, security breaches are existential risk

3. **[Quality - e.g., Performance]**
   - We will always ship designs that load <3 seconds, even if it means reducing features
   - Why: Users abandon after 5 seconds, performance is part of UX quality

## What Can Be Compromised (If Necessary)

These are important but can be adjusted for higher priorities:

1. **Visual Polish:** Can be improved in v2 if timeline is constrained. Core functionality and usability cannot be compromised, but aesthetic refinement can wait.

2. **Edge Case Support:** Can defer rare edge cases to v2 if they significantly increase complexity. Support 80% of users excellently, handle 20% adequately.

3. **Feature Breadth:** Can launch with fewer features if it means shipping sooner. Better to do 3 things excellently than 10 things poorly.

</design_principles>

<information_gaps>
## Missing User Context

**Gap:** [What's unclear about users]

**Why This Matters:** [How this affects design decisions]

**Example:** "PM says 'design for mobile users' but doesn't specify: Are these existing users (familiar with product) or new users (need onboarding)? Are they using on-the-go (need quick access) or at desk (can handle complexity)?"

**Impact on Design:** Can't design appropriate level of guidance/onboarding without knowing user proficiency

**Clarifying Question:** "Which user segment are we designing for: power users who know the product, or first-time users who need guidance? What's their context of use: on-the-go or at desk?"

---

[Continue for all user context gaps]

## Unclear Success Criteria

**Gap:** [What's vague about success metrics]

**Why This Matters:** [Can't validate designs without clear metrics]

**Example:** "PM says 'improve user engagement' but doesn't define engagement. Does this mean DAU (daily active users), session length, actions per session, or feature usage?"

**Impact on Design:** Can't make informed tradeoff decisions without knowing what we're optimizing for

**Clarifying Question:** "How are we defining user engagement? What's the baseline and target? How will we measure it?"

---

[Continue for all success criteria gaps]

## Undefined Constraints

**Gap:** [What technical/business constraints are missing]

**Why This Matters:** [Can't design feasible solutions without constraints]

**Example:** "PM says 'integrate with CRM' but doesn't specify which CRM system, what APIs are available, or what data we can access"

**Impact on Design:** Can't design data displays or workflows without knowing what data is available

**Clarifying Question:** "Which CRM system are we integrating with? What APIs are available? What user data can we access? Are there rate limits or data freshness issues?"

---

[Continue for all undefined constraints]

## Ambiguous Requirements

**Gap:** [High-level or vague requirement]

**Why This Matters:** [Risk of designing wrong thing]

**Example:** "Support multiple payment methods" without details

**Clarifying Question:** "Which specific payment methods must we support in v1, and which can be deferred?"

---

## Clarifying Questions for PM

Prioritized list of questions that need answers before design can proceed effectively:

### Critical (Must answer before starting design):
1. [Question that blocks design work]
2. [Question that blocks design work]

### High Priority (Should answer in first week):
1. [Question that affects design direction]
2. [Question that affects design direction]

### Medium Priority (Good to know, but can proceed without):
1. [Question that would inform design but not block it]

</information_gaps>

<validation_criteria>
## Must-Have (Non-Negotiable)

Designs MUST satisfy these requirements or they're not acceptable:

- [ ] **[Requirement]** - [How to validate]
  - Example: "Must complete checkout in 6 steps or fewer" - Validate by counting steps in user flow
- [ ] **[Requirement]** - [How to validate]
  - Example: "Must meet WCAG 2.1 AA contrast requirements" - Validate with color contrast checker
- [ ] **[Requirement]** - [How to validate]
  - Example: "Must render correctly on iOS 14+ and Android 10+" - Validate with device testing

**Validation Method:** Checklist review before handoff to engineering

---

## Should-Have (Important but Adjustable)

Designs should satisfy these if possible, but tradeoffs acceptable:

- [ ] **[Requirement]** - [How to validate]
  - Example: "Should support autofill for all form fields" - Validate in browser testing
- [ ] **[Requirement]** - [How to validate]
  - Example: "Should include contextual help for complex interactions" - Validate in usability testing

**Validation Method:** Design critique, adjust if blockers arise

---

## Success Signals (Design is On Track)

Early indicators that design is heading in the right direction:

- ✅ **[Signal]** - [When to check]
  - Example: "Stakeholders easily understand user flow in walkthrough" - Check in design review
- ✅ **[Signal]** - [When to check]
  - Example: "Usability testing shows 90%+ task completion" - Check in usability testing
- ✅ **[Signal]** - [When to check]
  - Example: "Engineering confirms designs are feasible" - Check in technical review

---

## Red Flags (Design is Off Track)

Warning signs that design is not meeting goals:

- 🚩 **[Red flag]** - [What to do]
  - Example: "Stakeholders confused about how feature works" - Stop, clarify requirements, iterate
- 🚩 **[Red flag]** - [What to do]
  - Example: "Usability testing shows <70% task completion" - Identify friction points, redesign
- 🚩 **[Red flag]** - [What to do]
  - Example: "Engineering flags designs as technically infeasible" - Adjust design to meet constraints
- 🚩 **[Red flag]** - [What to do]
  - Example: "Designs violate accessibility standards" - Fix immediately, non-negotiable

---

## Validation Methods & Timeline

**Design Review with Stakeholders:**
- **When:** Week 1 (after initial concepts)
- **Purpose:** Align on direction, gather feedback, ensure we're solving the right problem
- **Success Criteria:** Stakeholders agree on direction, no major misalignment

**Usability Testing:**
- **When:** Week 2 (after refined prototype)
- **Purpose:** Validate designs with real users, measure task completion and satisfaction
- **Success Criteria:** 90%+ task completion, 4+/5 satisfaction rating, no critical usability issues

**Technical Feasibility Review:**
- **When:** Week 3 (before finalizing designs)
- **Purpose:** Confirm engineering can build this within timeline and constraints
- **Success Criteria:** Engineering confirms feasibility, no major technical blockers

**Accessibility Audit:**
- **When:** Week 4 (before handoff)
- **Purpose:** Ensure designs meet WCAG 2.1 AA standards
- **Success Criteria:** All accessibility requirements met, no violations

**Post-Launch Analytics:**
- **When:** 2 weeks, 1 month, 3 months after launch
- **Purpose:** Measure success metrics, identify areas for improvement
- **Success Criteria:** Success metrics trending toward targets

</validation_criteria>

<next_actions>
## Immediate Next Steps

Based on this analysis, here's what needs to happen before design can proceed effectively:

### 1. Clarify with PM (Priority: Critical)
**Action:** Schedule 30-min meeting with PM to clarify:
- [Question 1]
- [Question 2]
- [Question 3]

**Owner:** [Designer name]
**Timeline:** By [date]
**Blocker:** Cannot start design without this information

### 2. Gather User Context (Priority: High)
**Action:** Review existing user research or conduct [research method]
- [Specific research need]

**Owner:** [UX Researcher or Designer]
**Timeline:** By [date]
**Impact:** Informs user-centered design decisions

### 3. Technical Validation (Priority: High)
**Action:** Meet with engineering to clarify:
- [Technical constraint or integration question]

**Owner:** [Designer + Engineering Lead]
**Timeline:** By [date]
**Impact:** Ensures designs are technically feasible

### 4. Begin Design Exploration (Priority: High)
**Action:** Start with [specific design task]
- Focus on [core user flow or interaction]
- Create [low-fi sketches / wireframes / prototype]

**Owner:** [Designer name]
**Timeline:** By [date]
**Deliverable:** [Prototype for usability testing / Concepts for design review]

### 5. Schedule Validation Sessions (Priority: Medium)
**Action:** Schedule:
- Design review with stakeholders: [date]
- Usability testing sessions: [dates]
- Technical review with engineering: [date]

**Owner:** [Designer or PM]
**Timeline:** Schedule by [date], sessions occur in weeks 1-4

</next_actions>
</design_constraints>

FAILURE
- Any required section in `<design_constraints>` is missing or materially incomplete.
- Constraints are generic and not traceable to provided PM context/goals/metrics/requirements.
- Metrics are not translated into testable design requirements and validation criteria.
- Information gaps lack actionable clarifying questions.
- Claims are generic or not grounded in provided inputs.
- Assumptions are used but not explicitly stated.
