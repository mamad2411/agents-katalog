---
name: sdd-prd
description: 'Create or update the shared PRD — discover product vision, map user journeys, define functional requirements, and write success criteria and NFRs. Use when defining product requirements, revising the product vision, or updating the PRD. Do not use for architecture decisions, UX design, or implementing features.'
---

Create or update the shared PRD at `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/prd.md`.
This is a **shared project document** — not tied to any specific change. It defines WHAT the product is and WHY, and serves as context for all future changes.

**Output**: `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/prd.md`

**Template**: Use `assets/prd.md` as the document structure.

> [!IMPORTANT]
> This skill is designed to be used with the **sdd-team:sdd-pm.agent** agent.
> Switch to it in the agent selector before invoking this skill for the full interactive experience.
> If you are already using **sdd-team:sdd-pm.agent**, proceed with the workflow below.

---

## Entry point

1. **Check if PRD already exists**

   Read `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/prd.md` or any file provided by the user. If it exists:
   - Summarize current content to the user.
   - Ask: "Do you want to **revise** the existing PRD or **start fresh**?" Skip this question if you detect from existing document or user input.
   - If revise → follow **Edit PRD Workflow** below.
   - If fresh → follow **Create PRD Workflow** below.

2. **Context gathering** (always)
   - Read existing project docs (README, package.json, any brief or research docs).
   - Read `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/architecture.md` and `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/ux.md` if they exist — for alignment.
   - Ask the user for additional context if needed.

---

## Create PRD Workflow

Collaborative, step-by-step facilitation to produce a comprehensive Product Requirements Document.

### Step 1 — Context gathering

1. If no docs were found, ask: *"Any product briefs, research docs, project context files, or existing project docs to load?"*
2. Read all provided files fully.
3. **If no input docs available:** gather product information directly from the user via chat.
4. Detect: brownfield (existing project docs) vs greenfield (new product). Report findings to user.
5. Confirm gathered context before proceeding.

Output: `✅ Context loaded — ready to build PRD.`

### Step 2 — Project discovery & classification

Discover and classify the project through natural conversation:

1. **Project type:** web app, API, mobile, SaaS, CLI, desktop, IoT, etc.
2. **Domain:** healthcare, fintech, edtech, general, etc.
3. **Complexity:** low / medium / high (based on domain regulations, integrations, novel tech).
4. **Context:** greenfield (new) vs brownfield (existing system enhancement).

Use loaded docs as conversation starters. Present your assessment for confirmation:

*"I'm hearing this as: **Type:** web app | **Domain:** general | **Complexity:** low | **Context:** greenfield. Sound right?"*

### Step 3 — Product vision discovery

Explore what makes this product special through conversation (no content generation yet):

- **User delight:** *"What would make users say 'this is exactly what I needed'?"*
- **Differentiation:** *"What's the moment where users realize this is different?"*
- **Core insight:** *"What insight makes this product possible or unique?"*
- **Problem framing:** *"What's the real problem — not the surface symptom, but the deeper need?"*
- **Why now:** *"Why is this the right time to build this?"*

Reflect back understanding and get user confirmation before proceeding.

### Step 4 — Executive Summary

Draft the Executive Summary using insights from Steps 2–3:

- **Vision alignment:** product vision, target users, problem being solved (dense, precise)
- **What Makes This Special:** product differentiator, core insight, why users choose it
- **Project Classification:** type, domain, complexity, greenfield/brownfield

> **For each section (Steps 4–12):** present draft, refine collaboratively, then append to output file.

### Step 5 — Success Criteria

Facilitate defining what "winning" looks like:

1. **User success:** guide from vague to measurable — NOT "users are happy" → "users complete [action] within [timeframe]".
2. **Business success:** 3-month / 12-month success, key metrics.
3. **Technical success:** reliability, performance targets, scale expectations.
4. **Challenge vague metrics:** "10,000 users" → "What kind of users? Doing what?" / "Fast" → "How fast, specifically?"
5. **Scope negotiation:** MVP (must work) vs Growth (competitive) vs Vision (dream).

Present drafted content. Refine with user. Append.

### Step 6 — User Journey mapping

Map ALL user types that interact with the system using narrative story-based journeys:

1. **Identify user types:** primary users, admins, moderators, support, API consumers, internal ops.
2. **Create narrative journeys** for each user type:
   - **Opening scene:** Where/how do we meet them? Current pain?
   - **Rising action:** Steps they take, what they discover
   - **Climax:** Critical moment of product value delivery
   - **Resolution:** How their situation improves
3. **Connect journeys to capabilities:** explicitly state what each journey reveals about required features.
4. **Ensure coverage:** primary happy path, primary edge case, secondary users, API consumers (if applicable).

Target: 3–4 compelling narrative journeys minimum. Present and refine. Append.

### Step 7 — Domain requirements (optional)

**Skip if domain complexity is low.** For medium/high complexity: compliance (HIPAA, PCI-DSS, GDPR), security constraints, integration requirements, domain-specific risks. Present and append if applicable.

### Step 8 — Innovation discovery (optional)

**Skip if no genuine innovation signals detected.** If signals present ("nothing like this exists", novel tech combinations): explore what's novel, validate with market context, define risk fallbacks. Append if applicable.

### Step 9 — Project-type deep dive

Conduct project-type specific requirements discovery:

- **Web app:** SPA/MPA, browser support, SEO, accessibility, real-time?
- **API:** endpoints, authentication, data formats, rate limits, versioning?
- **SaaS B2B:** multi-tenancy, permissions, subscriptions, integrations?
- **Mobile:** native/cross-platform, offline mode, push notifications, device features?
- **Other types:** adapt questions to relevant platform concerns.

Present and append.

### Step 10 — Scoping exercise

1. **Review** all PRD content built so far.
2. **MVP strategy:** minimum that makes users say "this is useful"? Fastest path to validated learning?
3. **Feature prioritization:** Must-have vs Nice-to-have. Ask: *Without this, does the product fail?*
4. **Phased roadmap:** Phase 1 (MVP), Phase 2 (growth), Phase 3 (expansion).
5. **Risk analysis:** technical, market, resource risks with mitigation strategies.

Present and append.

### Step 11 — Functional Requirements

**This is THE CAPABILITY CONTRACT for the entire product.** What's not listed here won't exist.

1. Extract capabilities from all previous sections.
2. Organize by capability area (5–8 areas): "User Management" not "Authentication System".
3. **Format:** `FR#: [Actor] can [capability] [context/constraint]`. Target 20–50 FRs.
4. **Altitude check:** WHAT capability exists, NOT HOW to implement.
5. **Self-validate:** Every MVP capability covered? Domain requirements included? Readable by UX designer and architect?

Present and refine collaboratively. Append.

### Step 12 — Non-Functional Requirements

Define quality attributes — **only those that matter for this product.** Make each measurable: NOT "fast" → "User actions complete within 2 seconds". Skip irrelevant categories.

Present and append.

### Step 13 — Polish & completion

1. Read complete document start to finish.
2. Polish: flow, de-duplication, consistent terminology, `##` Level 2 headers.
3. Quality check: zero fluff, no anti-patterns ("the system will allow" → "Users can").
4. Save final `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/prd.md`.
5. Present a **completion recap** and suggest `/arch` or `/ux` next.

---

## Edit PRD Workflow

Structured improvement of an existing PRD.

### Step 1 — Discovery

1. Load `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/prd.md` completely.
2. Ask: *"What would you like to change?"* (fix issues, add sections, improve structure, general improvements).
3. **Detect PRD format** — check for core sections: Executive Summary, Success Criteria, Product Scope, User Journeys, Functional Requirements, Non-Functional Requirements.

### Step 2 — Deep review & change plan

1. Read the entire PRD thoroughly.
2. Analyze against quality standards: information density, structure/flow, completeness, measurability, traceability, implementation leakage.
3. Build section-by-section change plan: current state, issues found, changes needed, priority (Critical/High/Medium/Low).
4. Present change plan with summary: additions, updates, removals, restructuring.
5. Get user approval on the plan before proceeding.

### Step 3 — Apply edits

1. Follow approved change plan systematically, section by section, in priority order.
2. For each section: load current content → apply changes → verify quality standards.
3. If restructuring: reorganize to standard structure with proper ## Level 2 headers.
4. Show progress after each major section update.
5. Final review: load complete updated document, verify all changes applied correctly.

### Step 4 — Completion

1. Apply all edits directly to `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/prd.md`.
2. Present a **completion recap**: sections modified, changes applied, quality assessment.

---

## Tracker Update

After saving `prd.md`, follow the **`sdd-tracker` skill** — update `shared.prd` and changelog (only if PRD was revised, not for new documents).

---

## Guardrails

{SKILL_ASSETS_NOTICE}
- **Adopt the PM agent's persona** — from: `agents/pm.agent.md`
- **Never generate content without user input** — facilitate, Do not dictate.
- Challenge vague requirements, push for specificity.
- High information density: every sentence carries weight, zero fluff.
- FR format: `FR#: [Actor] can [capability]` — implementation-agnostic, testable.
