---
name: productize-privacy-policy
description: >-
  Privacy Policy. Use when drafting or updating a privacy policy for a product, launch,
  website, app, or customer-facing workflow.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Privacy Policy

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

- **Skill**: `privacy-policy`
- **Lifecycle**: Launch & Learn
- **Category**: Operations
- **Primary artifact**: Privacy policy draft for legal review with data practices, assumptions, and compliance flags

Use when drafting or updating a privacy policy for a product, launch, website, app, or customer-facing workflow.

## Productize Contract

- **Primary lifecycle**: Launch & Learn
- **Supporting lifecycle**: none
- **Primary artifact**: Privacy policy draft for legal review with data practices, assumptions, and compliance flags
- **Source method**: pm-skills-main/pm-toolkit/skills/privacy-policy/SKILL.md

## Legal Review Guardrail

This skill creates a product/legal working draft for review. Do not present the output as legal advice or final compliance approval. Flag jurisdiction, data, party, and policy assumptions for qualified review.

## Method

You are an experienced data privacy and compliance specialist. Your role is to help draft comprehensive, clear, and compliant privacy policies for digital products and services.

## Purpose
Draft a detailed privacy policy for a product or service. The policy covers data types handled, applicable jurisdiction, and clearly marks clauses that require legal review. Provide plain-language explanations to ensure accessibility and transparency.

## Important Disclaimer
**This is for informational purposes only and does not constitute legal advice. Always have a qualified attorney specializing in data privacy law review the final policy before publication. Privacy policies are legally binding documents that establish your company's responsibilities and users' rights; professional legal review is essential.**

## Input Arguments
- `$PRODUCT_NAME`: Name of the product or service
- `$PRODUCT_URL`: URL or description of the product (optional; will be researched if provided)
- `$COMPANY_NAME`: Legal name of your company
- `$COMPANY_ADDRESS`: Company headquarters or registered address
- `$CONTACT_EMAIL`: Email for privacy inquiries (e.g., privacy@company.com)
- `$INFORMATION_TYPES`: Types of data collected (e.g., "names, emails, usage behavior, location data, payment information, device identifiers")
- `$JURISDICTION`: Applicable jurisdiction (e.g., "United States," "European Union (GDPR)," "California (CCPA)")

## Process

### Step 1: Research (if URL provided)
If $PRODUCT_URL is provided:
- Visit the product website
- Identify what data is collected (forms, tracking, login, payments)
- Note any third-party integrations (analytics, payment processors, SDKs)
- Understand the product's primary features and use cases

### Step 2: Clarify Data Collection
Map out all data your product collects:
- **Direct collection**: What users enter (name, email, preferences)
- **Automatic collection**: What is tracked (IP address, usage behavior, device info, cookies)
- **Third-party data**: What comes from partners, integrations, or service providers
- **Special categories**: Does the product handle health data, financial data, children's data, biometric data?

### Step 3: Identify Applicable Laws
Note which laws apply:
- **GDPR** (EU users): Stricter; requires explicit consent, data subject rights, DPA
- **CCPA/CPRA** (California): Consumer rights to access, delete, opt-out
- **Other US states**: Laws like VIPA, TDPSA emerging
- **Industry-specific**: HIPAA (health), GLBA (finance), FERPA (education)
- Determine if your product serves international users

### Step 4: Structure the Privacy Policy
Organize in standard sections (detailed below).

### Step 5: Use Plain Language
Write clearly and accessibly. Avoid technical jargon. Define terms when first used. Help users understand what data you collect and why.

### Step 6: Highlight Areas Needing Legal Review
Mark sections with [ LEGAL REVIEW REQUIRED] where jurisdiction-specific language, specific data rights, or legal clauses are needed.

### Step 7: Provide Context
Include notes explaining:
- Why each section is important
- What decisions the company must make
- Compliance considerations

## Privacy Policy Template Structure

### Preamble
A brief introduction explaining:
- What the policy covers
- When it was last updated
- How users can contact you with questions

### Key Sections

#### 1. Information We Collect
Categories of data:
- Personal information (name, email, account info)
- Usage data (pages viewed, features used, time spent)
- Device information (type, OS, browser, IP address)
- Location data (if applicable)
- Payment information (handled securely, often by third parties)
- Communications (if users contact support)
- [ LEGAL REVIEW REQUIRED] Sensitive or special categories (health, biometric, etc.)

#### 2. How We Collect Information
Methods:
- Directly from users (forms, registration, preferences)
- Automatically (cookies, analytics, device sensors)
- From third parties (partners, service providers, data brokers)

#### 3. How We Use Information
Purposes (be specific, not vague):
- Providing the service and customer support
- Improving and personalizing the product
- Analytics and understanding user behavior
- Marketing and promotional communications
- Security and fraud prevention
- Legal compliance
- [ LEGAL REVIEW REQUIRED] Other purposes (must be explicitly stated if you plan to use data for new purposes later)

#### 4. Legal Basis for Processing
[ LEGAL REVIEW REQUIRED] Especially important for GDPR:
- **Consent**: User has explicitly agreed
- **Contract**: Data is needed to provide the service
- **Legal obligation**: Law requires processing
- **Vital interests**: Protection of life or health
- **Public task**: Part of your official function
- **Legitimate interests**: Company has a legitimate business need

#### 5. Data Sharing and Third Parties
Who has access to data:
- Service providers (hosting, analytics, email, payments)
- Business partners (if applicable)
- Legal authorities (if required by law)
- [ LEGAL REVIEW REQUIRED] Where third parties are located (especially if outside user's jurisdiction)

#### 6. International Data Transfer
[ LEGAL REVIEW REQUIRED] If applicable:
- How data is transferred across borders
- Mechanisms used (Standard Contractual Clauses, adequacy decisions, user consent)
- Where data is stored and processed

#### 7. Data Retention
How long you keep data:
- Account data: As long as account is active, then X months/years
- Usage logs: X months
- Deleted content: Y days before permanent deletion
- [ LEGAL REVIEW REQUIRED] Be specific, not vague; many regulations require this

#### 8. User Rights
[ LEGAL REVIEW REQUIRED] Varies by jurisdiction:
- **Right to access**: Users can request copy of their data
- **Right to deletion**: Users can request data be deleted ("right to be forgotten")
- **Right to correct**: Users can update inaccurate data
- **Right to restrict processing**: Users can limit how data is used
- **Right to data portability**: Users can download their data
- **Right to opt-out**: Users can unsubscribe from marketing
- **Right to lodge complaints**: Users can contact data protection authorities
- How users exercise these rights (contact info, process)

#### 9. Cookies and Tracking
[ LEGAL REVIEW REQUIRED] Detailed info:
- What cookies and tracking tools are used
- Why each is used (functionality, analytics, marketing)
- How to manage/disable cookies
- Whether explicit consent is required (GDPR requires it for non-essential cookies)

#### 10. Security
Measures taken to protect data:
- Encryption in transit and at rest
- Access controls and authentication
- Regular security audits
- Incident response procedures
- Limitations (no system is 100% secure)

#### 11. Children's Privacy
[ LEGAL REVIEW REQUIRED] If product serves users under 13:
- Parental consent mechanisms
- Age gates or verification
- Compliance with COPPA (US), UK Children's Code, similar laws

#### 12. Contact and Rights
How users contact you:
- Privacy contact email
- Mailing address
- Response timeframe for requests
- Data Protection Officer (if required)

#### 13. Policy Changes
How you'll communicate changes:
- Notice period (e.g., 30 days)
- How you'll notify (email, in-app, website)
- User's ability to opt-out if changes are material

#### 14. Additional Provisions
- **No sale of data**: Whether you sell/share data (if not, explicitly state)
- **Third-party links**: You're not responsible for external sites
- **Governing law**: Which jurisdiction's laws govern
- **Effective date**: When policy became active

---

## Content Guidelines

- **Be specific**: Don't say "we use your data for product improvement"; say "we analyze usage patterns to identify features that users find confusing and prioritize improvements to those features"
- **Plain language**: Write for a general audience, not lawyers. Explain what data you collect and why in simple terms
- **Transparency**: Be honest about all data collection, including analytics, third parties, and uses
- **User control**: Explain how users can access, delete, or opt-out of data processing
- **Align with practice**: The policy must match what your product actually does; if it doesn't, change the product or the policy
- **Complete information types**: Use $INFORMATION_TYPES to make the policy specific to your actual data collection

---

## Output Format

Present the privacy policy in three parts:

### Part 1: Summary
Quick reference:
- Product name and purpose
- Data types collected
- Jurisdiction(s) covered
- Key user rights
- Retention periods
- Contact information

### Part 2: Full Privacy Policy Document
A complete, ready-to-publish privacy policy.

### Part 3: Customization and Compliance Notes
Guidance on:
- Sections marked for legal review
- Jurisdiction-specific considerations (GDPR, CCPA, etc.)
- Compliance checklist
- Common modifications based on product type
- Next steps (legal review, implementation, user communication)

---

## Key Compliance Reminders

- **GDPR compliance** (if serving EU users): Requires explicit consent, clear rights, DPA with processors, DPIA for risky processing
- **CCPA/CPRA** (California users): Requires rights to access, delete, opt-out; detailed disclosures; no discrimination for exercising rights
- **Transparency**: Users must understand what data is collected, how it's used, and who can access it
- **Accuracy**: Keep your policy updated as data practices change
- **Enforcement**: Privacy violations can result in fines, user lawsuits, and reputational damage
- **Get legal review**: Before publishing, have a data privacy attorney in your jurisdiction review the policy

---

## Before You Publish

- [ ] Have a data privacy attorney review the policy
- [ ] Ensure the policy matches your actual data collection and use
- [ ] Make privacy request processes easy for users (accessible contact info, quick response)
- [ ] Implement technical measures mentioned in the policy (encryption, access controls, etc.)
- [ ] Set up systems to handle data subject rights requests (access, deletion, etc.)
- [ ] Document your legal basis for each type of processing
- [ ] Have a Data Processing Agreement (DPA) with all third-party processors
- [ ] Notify users of material changes; consider giving them a choice to opt-out

## Productize Output Rules

- Produce the artifact named in the Productize contract, not a generic framework summary.
- Separate known facts, assumptions, missing evidence, and risky leaps before recommending.
- Convert uncertain claims into validation steps, metrics, owner decisions, or launch/readout checks.
- If this reference method conflicts with Productize evidence standards, keep the Productize standard.
