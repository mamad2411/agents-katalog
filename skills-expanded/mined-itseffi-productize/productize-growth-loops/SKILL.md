---
name: productize-growth-loops
description: >-
  Growth Loops. Use when designing product-led growth loops, referral loops, collaboration
  loops, usage loops, or flywheels that reduce dependence on paid acquisition.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Growth Loops

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

- **Skill**: `growth-loops`
- **Lifecycle**: Growth
- **Category**: Growth
- **Primary artifact**: Growth loop map with loop mechanics, inputs, outputs, constraints, and experiments

Use when designing product-led growth loops, referral loops, collaboration loops, usage loops, or flywheels that reduce dependence on paid acquisition.

## Productize Contract

- **Primary lifecycle**: Growth
- **Supporting lifecycle**: none
- **Primary artifact**: Growth loop map with loop mechanics, inputs, outputs, constraints, and experiments
- **Source method**: pm-skills-main/pm-go-to-market/skills/growth-loops/SKILL.md

## Method

## Overview
Identify and design growth loops (flywheels) that create sustainable traction. This skill evaluates five proven growth loop mechanisms to reduce reliance on paid acquisition and build product-led growth.

## When to Use
- Designing growth mechanisms for a product
- Building sustainable viral or referral traction
- Reducing reliance on paid acquisition
- Analyzing competitor growth strategies
- Optimizing product for product-led growth

## The 5 Growth Loop Types

### 1. Viral Loop
Product content created by users gets shared on external platforms, bringing new users back to the product.
- **Mechanism**: Users create content in-product -> Share on social/external platforms -> New users discover and signup
- **Example**: Figma designs shared as links, Loom videos shared in emails
- **Strength**: Exponential user acquisition if content is inherently shareable
- **Challenge**: Requires highly shareable output and strong incentive to share

### 2. Usage Loop
Users create content or value within the product, then share it, which invites new users or drives re-engagement.
- **Mechanism**: User creates -> Shares creation -> Others consume -> Become engaged users
- **Example**: Twitter threads, Medium articles, Notion templates shared publicly
- **Strength**: Growth tied directly to product usage and network effects
- **Challenge**: Requires content creation friction to be very low

### 3. Collaboration Loop
Users invite colleagues to co-create or collaborate within the product, expanding the user base within organizations.
- **Mechanism**: User creates -> Invites colleagues for collaboration -> Colleagues discover product value
- **Example**: Google Docs invitations, Figma team projects, Slack channels
- **Strength**: Deep organizational penetration and high retention
- **Challenge**: Works best for collaborative/team-based products

### 4. User-Generated Loop
Users discover new content or features through other users' creations, then create and share their own content.
- **Mechanism**: User discovers content -> Creates similar content -> Shares creation -> Others discover
- **Example**: TikTok, Pinterest, YouTube trends driving creator participation
- **Strength**: Creates content flywheel and network effects
- **Challenge**: Requires critical mass of quality content to sustain

### 5. Referral Loop
Users invite other potential users in exchange for rewards, incentives, or social recognition.
- **Mechanism**: User refers -> Referred user joins -> Referrer gets reward -> Shares more referrals
- **Example**: Dropbox referral bonus, Uber rider referrals, PayPal signup bonuses
- **Strength**: Directly incentivizes acquisition; easy to measure ROI
- **Challenge**: Requires valuable incentive without eroding unit economics

## How It Works

### Step 1: Define Product Value
Clarify the core value users experience:
- Primary action users take in your product
- Value created per user action
- Network effects present (if any)
- Friction points in the experience

### Step 2: Evaluate Loop Fit
Assess which growth loops align with your product:
- Product type (collaborative, content-based, utility, etc.)
- Target user behavior and sharing habits
- Network effects already present
- Existing user base and engagement

### Step 3: Design Loop Mechanics
Create specific loop implementation:
- Trigger that initiates sharing or invitations
- Incentive for participation (intrinsic or extrinsic)
- Ease of sharing mechanism
- Conversion rate from invite to activation
- Frequency of loop repetition per user

### Step 4: Calculate Loop Coefficient
Estimate growth velocity:
- Invites/shares per user per cycle
- Conversion rate of invites to new users
- Net new users per cycle
- Time per cycle iteration

### Step 5: Build the Loop
Implement the highest-leverage loop first:
- Start with the most natural loop for your product
- Optimize messaging and friction
- Measure loop metrics and conversion rates
- Compound results over time

## Input Format
Use $ARGUMENTS to pass:
- Product description and primary user action
- Target user demographics and behavior
- Existing sharing/collaboration features
- Current growth channels and metrics
- Constraints or opportunities

## Output
A growth loops analysis including:
- Ranked evaluation of all 5 loop types for your product
- Recommended primary growth loop with implementation plan
- Secondary loops to layer over time
- Key metrics and measurement framework
- 30-60-90 day implementation roadmap
- Potential loop coefficient and growth projections

## Framework
Based on growth loops research by Ognjen Boskovic. Focuses on compounding user acquisition through built-in, product-native sharing and collaboration mechanisms.

## Tips
- Start with one loop and master it before adding complexity
- Viral loops compound fastest but take time to build
- Collaboration loops create strongest retention and LTV
- Measure loop health weekly during optimization phase
- Combine loops for multiplicative effect once operating at scale

---

### Further Reading

- [Product-Led Growth 101, Part 1/2](https://www.productcompass.pm/p/product-led-growth-101-12)
- [OpenAI's Product Leader Shares 3-Layer Distribution Framework To Win Mind & Market Share in the AI World](https://www.productcompass.pm/p/distribution-framework-ai-products)
- [How to Design a Value Proposition Customers Can't Resist?](https://www.productcompass.pm/p/how-to-design-value-proposition-template)

## Productize Output Rules

- Produce the artifact named in the Productize contract, not a generic framework summary.
- Separate known facts, assumptions, missing evidence, and risky leaps before recommending.
- Convert uncertain claims into validation steps, metrics, owner decisions, or launch/readout checks.
- If this reference method conflicts with Productize evidence standards, keep the Productize standard.
