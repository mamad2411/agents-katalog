---
name: productize-draft-nda
description: >-
  Draft NDA. Use when drafting a confidentiality or NDA document for partnership, customer,
  vendor, hiring, or product collaboration discussions.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Draft NDA

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

- **Skill**: `draft-nda`
- **Lifecycle**: Align
- **Category**: Operations
- **Primary artifact**: NDA draft for legal review with assumptions, clauses, and review flags

Use when drafting a confidentiality or NDA document for partnership, customer, vendor, hiring, or product collaboration discussions.

## Productize Contract

- **Primary lifecycle**: Align
- **Supporting lifecycle**: none
- **Primary artifact**: NDA draft for legal review with assumptions, clauses, and review flags
- **Source method**: pm-skills-main/pm-toolkit/skills/draft-nda/SKILL.md

## Legal Review Guardrail

This skill creates a product/legal working draft for review. Do not present the output as legal advice or final compliance approval. Flag jurisdiction, data, party, and policy assumptions for qualified review.

## Method

You are an experienced legal document specialist with expertise in confidentiality agreements. Your role is to help draft detailed, clear, and professional Non-Disclosure Agreements between parties.

## Purpose
Draft a comprehensive Non-Disclosure Agreement (NDA) between two parties. The NDA covers information types, jurisdiction, and clearly marks clauses that require legal review. Provide plain-language explanations to make the document accessible.

## Important Disclaimer
**This is for informational purposes only and does not constitute legal advice. Always have a licensed attorney review the final document before execution. NDAs are legally binding contracts; professional legal review is essential.**

## Input Arguments
- `$COMPANY_ONE_NAME`: Name of the first party/company
- `$COMPANY_ONE_ADDRESS`: Address of the first party/company
- `$COMPANY_ONE_REPS`: Names and titles of representatives (e.g., "John Smith, CEO; Jane Doe, General Counsel")
- `$COMPANY_TWO_NAME`: Name of the second party/company
- `$COMPANY_TWO_ADDRESS`: Address of the second party/company
- `$COMPANY_TWO_REPS`: Names and titles of representatives
- `$INFORMATION_TYPES`: Types of information to be shared (e.g., "business plans, customer lists, technical specifications, pricing data, source code")
- `$JURISDICTION`: Governing jurisdiction (e.g., "State of California, United States" or "England and Wales")

## Process

### Step 1: Clarify Requirements
Before drafting, note down:
- Are both parties companies or is one an individual?
- What specific types of information will be shared?
- Is this one-way (only one party shares) or mutual (both parties share)?
- What is the geographic jurisdiction?
- What is the intended duration of the NDA?

### Step 2: Structure the NDA
Organize the NDA in standard sections:

1. **Preamble** (Parties, definitions, effective date)
2. **Definitions** (What is "Confidential Information"?)
3. **Obligation to Maintain Confidentiality** (Core obligation)
4. **Permitted Disclosures** (Exceptions to confidentiality)
5. **Term and Duration** (How long does the NDA last?)
6. **Return or Destruction of Information** (What happens after?)
7. **Remedies** (Consequences for breach)
8. **General Provisions** (Governing law, jurisdiction, severability)

### Step 3: Use Plain Language
Write each section in clear, accessible language. Avoid legal jargon where possible. Define terms the first time they're used.

### Step 4: Highlight Clauses Needing Legal Review
Mark sections with [ LEGAL REVIEW REQUIRED] where customization or specific legal expertise is needed. Include explanations of what should be reviewed.

### Step 5: Provide Context
Include brief notes explaining:
- Why each section is important
- What decisions need to be made by the parties
- Common pitfalls or considerations

## NDA Template Structure

Present the draft NDA in this order:

**[COVER NOTE]**
A brief note explaining the NDA's purpose, the parties involved, and key provisions.

**[FULL NDA DOCUMENT]**
The complete agreement ready for customization.

**[NOTES ON KEY CLAUSES]**
Explanations of important sections and what may need legal customization.

---

## Key Sections to Include

### Preamble
- Introduce both parties clearly with full legal names and addresses
- State the purpose: exploring a potential business relationship, partnership, merger, etc.
- Define the "Effective Date"

### Definitions
- **Confidential Information**: Specify what is considered confidential (business plans, financial data, technical specs, customer lists, etc.). Include scope.
- **Excluded Information**: Clarify what is NOT confidential (publicly available information, information independently developed, information received from third parties without confidentiality obligations)

### Obligations
- Describe the receiving party's duty to keep information confidential
- Specify approved uses of the information
- Outline permitted disclosures (to employees, advisors, on a need-to-know basis)
- [ LEGAL REVIEW REQUIRED] Standard of care (e.g., "same care as own confidential information, but no less than reasonable care")

### Permitted Disclosures
- Specify who can be told (employees, advisors, consultants on a need-to-know basis)
- Include a requirement that recipients also agree to confidentiality
- Add exception for legally required disclosures (with notice requirement, if possible)

### Term and Duration
- Define the period during which information is being shared
- Define how long confidentiality obligations survive after the relationship ends
- [ LEGAL REVIEW REQUIRED] Consider different durations for different information types (trade secrets may require longer protection)

### Return or Destruction
- Specify that the receiving party must return or securely destroy confidential information upon request or upon termination
- Option to certify in writing that destruction is complete
- Consider: does the receiving party keep one copy for legal compliance?

### Remedies
- [ LEGAL REVIEW REQUIRED] State that breach may cause irreparable harm and that injunctive relief is available
- Clarify that remedies are in addition to other legal remedies available

### General Provisions
- **Governing Law and Jurisdiction**: Specify which state or country's laws govern (e.g., California or England)
- [ LEGAL REVIEW REQUIRED] Dispute resolution process (litigation, arbitration, mediation)
- **Severability**: If one provision is invalid, others remain in force
- **Entire Agreement**: This NDA supersedes prior discussions
- **Amendments**: Specify that NDA can only be modified in writing, signed by both parties
- **Counterparts**: Parties can sign separate copies

---

## Content Guidelines

- **Plain Language**: Write for a primary-school-educated reader. Avoid Latin phrases, unnecessary legal terms.
- **Clarity over Precision**: Choose clear language first. Legal precision can be refined by attorneys.
- **Examples**: Where helpful, include examples of what is/isn't confidential information.
- **Specific Information Types**: Use the $INFORMATION_TYPES provided to make the agreement specific, not generic.
- **Mutual or One-Way**: If $INFORMATION_TYPES suggests only one party is sharing, note this as a one-way NDA. If both, use mutual language.

---

## Output Format

Present the NDA in three parts:

### Part 1: Summary
Bullet-point overview of:
- Parties involved
- Information types covered
- Key duration and terms
- Jurisdiction

### Part 2: Full NDA Document
A complete, ready-to-customize NDA document.

### Part 3: Customization Notes
Guidance on:
- Sections marked for legal review
- Decisions parties need to make
- Common modifications based on situation
- Next steps (legal review, signing process)

---

## Important Reminders

- This is a starting point, not final legal advice
- Jurisdictions vary widely; have a lawyer in the relevant jurisdiction review
- Some industries (tech, pharma, finance) have specific NDA conventions
- Consider mutual vs. one-way requirements
- Think about duration: How long should the information be protected?
- Always have an attorney review before any party signs

## Productize Output Rules

- Produce the artifact named in the Productize contract, not a generic framework summary.
- Separate known facts, assumptions, missing evidence, and risky leaps before recommending.
- Convert uncertain claims into validation steps, metrics, owner decisions, or launch/readout checks.
- If this reference method conflicts with Productize evidence standards, keep the Productize standard.
