---
name: rfp-drafting-skill
description: "Drafts and challenges RFx content for clarity, fairness, measurability, evaluation alignment, and commercial risk. Use for RFP, RFB, RFQ, RFI, or SOW drafting."
license: MIT
compatibility: "Agent Skills compatible; no external dependencies. Human review required for procurement decisions."
metadata:
  author: Arun Balaji Raju
  version: "0.2.0"
  project: procurement-ai-assistant
---

## Skill Name
Procurement RFx Drafting Skill

## Purpose
This skill helps AI support procurement professionals with structured, repeatable RFx drafting.

Use this skill when drafting or improving sections of an RFP, RFB, RFQ, RFI, SOW, evaluation criteria, response instructions, pricing instructions, service requirements, vendor performance language, or related procurement documents.

This skill should not simply generate procurement text. It should help create clear, fair, measurable, commercially sound, evaluable, and defensible procurement content.

This skill does not release procurement documents, approve sourcing strategy, interpret policy as final authority, make award recommendations, or replace procurement, legal, privacy, security, accessibility, finance, or business-owner review.

## Composability
This skill is standalone. If other Procurement AI Assistant skills are installed, the AI may combine relevant skills for a multi-step procurement request. Do not assume another skill is available; preserve this skill's own guardrails and human review points.

## Core Principle
Procurement does not need AI to write more words.

Procurement needs AI to help draft documents that are:

- Clear
- Fair
- Measurable
- Commercially sound
- Evaluable
- Defensible
- Aligned to the business need
- Ready for human review

The AI should follow this workflow:

**Understand -> Classify -> Identify Gaps -> Structure -> Draft -> Challenge -> Revise -> Validate -> Escalate**

The goal is to move from AI-generated text to AI-assisted procurement drafting.

## When to Use
Use this skill when the user needs help with:

- RFP, RFB, RFQ, RFI, or SOW drafting
- Mandatory requirements
- Rated requirements
- Evaluation criteria
- Response instructions
- Pricing instructions
- Commercial envelope language
- Technical envelope language
- Scope of work drafting
- Deliverables
- Service requirements
- SLA/KPI placement
- Vendor performance management sections
- Supplier reporting requirements
- Governance language
- Implementation requirements
- Transition requirements
- Exit requirements
- Clarification questions
- Procurement document quality review
- Fairness and defensibility checks
- Draft improvement without changing core content

## Do Not Use This Skill For
Do not use this skill to:

- Make final procurement strategy decisions
- Release RFx documents
- Approve legal terms
- Replace legal, privacy, security, accessibility, finance, or policy review
- Make supplier selection or award decisions
- Score supplier submissions
- Rewrite evaluator comments in a way that changes meaning
- Create supplier-specific or biased requirements
- Invent business requirements
- Add policy obligations without validation
- Change final approved content without user direction

## Required Inputs
Before drafting, identify which of the following inputs are available.

### Business and Scope Inputs
- What is being procured?
- What business outcome is required?
- Who are the stakeholders and end users?
- What is in scope?
- What is out of scope?
- Is this goods, services, software, SaaS, professional services, managed services, hardware, implementation, support, or a hybrid?
- Are there streams, categories, lots, modules, or service tiers?
- What are the expected deliverables?

### Procurement Inputs
- Is this an RFP, RFB, RFQ, RFI, SOW, second-stage process, amendment, renewal, or market sounding?
- Is the process binding or non-binding, where relevant?
- Is this public-sector, private-sector, internal, or enterprise-wide procurement?
- Are there existing templates, standard terms, policies, directives, trade agreement considerations, or approval gates?
- Are mandatory and rated requirements already identified?
- Is the evaluation model known?
- Is pricing evaluated, pass/fail, or used for ranking?

### Commercial Inputs
- Estimated budget or spend range
- Contract term
- Optional extension periods
- Pricing model
- One-time and recurring costs
- Implementation, support, professional services, renewal, and exit costs
- Volume or usage assumptions
- Desired pricing schedule structure
- Need for total cost of ownership review

### Risk Inputs
- Business criticality
- Operational dependencies
- Implementation complexity
- Data sensitivity
- Privacy/security/accessibility requirements
- Supplier lock-in risk
- Incumbent risk
- Transition/exit risk
- Performance management needs
- Governance requirements

### Output Inputs
- Which section needs to be drafted?
- Is the user asking for new drafting, revision, formatting, challenge review, or risk review?
- What tone and format are required?
- Is the output for internal review, stakeholder review, legal review, supplier-facing release, or executive briefing?

## Missing Information Rule
If critical information is missing, ask only the minimum questions needed to continue.

If drafting can proceed, continue with assumptions and flag the missing items.

Use this format:

```text
Assumptions I am using:
- ...

Missing information:
- ...

Questions to confirm:
- ...

Items requiring human review:
- ...
```

Do not invent facts, requirements, scoring weights, legal obligations, policy requirements, or supplier capabilities.

## Workflow

### Step 1: Understand the Drafting Request
Restate the drafting task in plain language.

Identify:

- RFx type
- Section being drafted
- Procurement stage
- Business outcome
- Audience
- Level of risk
- Human reviewers needed
- Whether the output is supplier-facing or internal only

### Step 2: Classify the Section
Classify the content into one or more section types:

- Background / opportunity summary
- Scope of work
- Deliverables
- Mandatory requirements
- Rated requirements
- Evaluation criteria
- Response instructions
- Pricing instructions
- Commercial envelope
- Technical envelope
- SLA / KPI requirements
- Implementation requirements
- Transition requirements
- Exit requirements
- Reporting and governance
- Vendor performance management
- Contract management requirements
- Supplier qualification requirements
- Clarification questions
- Addendum / amendment language

### Step 3: Identify Missing Information
Before drafting, identify missing information that could affect clarity, fairness, evaluation, pricing, or contract management.

Check:

- Is the business need clear?
- Are deliverables measurable?
- Are assumptions defined?
- Are mandatory requirements truly mandatory?
- Are rated criteria objective?
- Are supplier response expectations clear?
- Are pricing instructions complete?
- Are SLAs/KPIs measurable?
- Are implementation responsibilities clear?
- Are acceptance criteria defined?
- Are reporting and governance expectations clear?
- Are transition and exit obligations addressed?

### Step 4: Separate Requirement Types
Do not mix requirement types.

Separate:

#### Mandatory Requirements
Use for minimum pass/fail requirements.

Check that mandatory requirements are:

- Objective
- Clearly stated
- Easy to verify
- Not unnecessarily restrictive
- Not supplier-specific
- Not subjective
- Aligned to actual business need

#### Rated Requirements
Use for qualitative or value-based evaluation.

Check that rated criteria are:

- Evaluable
- Linked to scoring guidance
- Clear to suppliers
- Clear to evaluators
- Not duplicative
- Not overly subjective
- Supported by requested response content

#### Pricing Requirements
Use for commercial response and evaluation.

Check that pricing requirements are:

- Comparable
- Complete
- Clear on assumptions
- Clear on required vs optional items
- Clear on one-time vs recurring costs
- Clear on implementation, support, renewal, and exit costs

#### Contractual Requirements
Use for legal/commercial obligations.

Check that contractual requirements are:

- Properly placed in the document
- Escalated for legal review where needed
- Clear on obligations, remedies, reporting, and governance
- Not used as evaluation criteria unless intentionally designed that way

### Step 5: Draft the Section
Draft in plain, supplier-facing procurement language.

Use:

- Clear headings
- Short paragraphs
- Numbered lists where useful
- Defined terms where needed
- Measurable requirements
- Direct supplier instructions
- Consistent terminology
- Neutral, non-supplier-specific language

Avoid:

- Vague statements
- Marketing-style language
- Unnecessary complexity
- Mixed obligations
- Ambiguous verbs
- “As required” without context
- “Timely” without defined timing
- “Reasonable” without criteria
- Requirements that cannot be evaluated or enforced

### Step 6: Challenge the Draft
After drafting, review the section as a procurement challenger.

Ask:

- Could a supplier interpret this in more than one way?
- Could evaluators score this consistently?
- Is the response instruction clear?
- Is the requirement measurable?
- Is this actually mandatory, or should it be rated?
- Is the pricing structure clear?
- Is there hidden commercial exposure?
- Is there operational risk after award?
- Is there any supplier-specific language?
- Is this too restrictive for the market?
- Does this need legal, privacy, security, accessibility, finance, or business-owner review?

### Step 7: Review for Public Procurement Fairness
For public-sector procurement, check:

- Equal treatment of suppliers
- Objective wording
- Clear response instructions
- Clear evaluation approach
- No hidden preferences
- No unnecessary barriers to competition
- No criteria that are impossible to score consistently
- Clear separation of mandatory, rated, pricing, and contractual requirements
- Audit defensibility
- Clarification risks

### Step 8: Review for Commercial and Operational Risk
Check whether the draft creates risk in:

- Pricing
- Scope clarity
- Implementation
- Service levels
- Governance
- Reporting
- Acceptance criteria
- Renewal
- Change orders
- Supplier lock-in
- Transition and exit
- Data/privacy/security
- Subcontracting
- Vendor performance management

### Step 9: Prepare Human Review Items
Identify what must be reviewed by humans.

Examples:

- Business owner: scope, deliverables, acceptance criteria, service levels
- Procurement: sourcing strategy, evaluation structure, fairness, document consistency
- Legal: terms, liability, indemnities, IP, termination, dispute resolution, remedies
- Privacy/security: data, access, hosting, security controls, incident reporting
- Finance: pricing model, affordability, budget treatment, TCO
- Accessibility: accessibility requirements and compliance needs
- Evaluation team: scoring clarity and evidence expectations

## Output Format

### Default Output Structure
Use this format unless the user asks otherwise:

1. Draft section
2. Assumptions
3. Missing information
4. Drafting rationale
5. Risk / issue table
6. Human review items
7. Suggested stakeholder questions

### Drafting Risk Table
Use this table:

| Area | Issue / Risk | Why It Matters | Suggested Change | Human Review Needed |
|---|---|---|---|---|

### Requirement Table
Use this table when drafting requirements:

| Requirement Type | Draft Requirement | Supplier Response Expected | Evaluation / Review Note |
|---|---|---|---|

### Evaluation Alignment Table
Use this table when drafting rated criteria:

| Criterion | What Supplier Must Provide | How Evaluators Can Assess | Risk / Clarification Needed |
|---|---|---|---|

### Pricing Instruction Review Table
Use this table when drafting pricing instructions:

| Pricing Item | Required / Optional | Evaluation Treatment | Risk / Clarification Needed |
|---|---|---|---|

### Human Review Checklist
Use this table:

| Reviewer | Item to Review | Why It Matters |
|---|---|---|

## Review Checks
Before finalizing, check:

- Is the business outcome clear?
- Is the section appropriate for the RFx type?
- Are mandatory and rated requirements separated?
- Are requirements measurable?
- Are supplier instructions clear?
- Are pricing instructions comparable?
- Are evaluation implications clear?
- Are contractual obligations escalated where needed?
- Are assumptions clearly marked?
- Are missing inputs flagged?
- Are legal/privacy/security/accessibility/finance items identified?
- Does the draft avoid supplier-specific or biased wording?
- Does the output remain draft-only for human review?

## Human Review
Humans must review and approve:

- Final sourcing strategy
- Final RFx structure
- Mandatory requirements
- Rated criteria
- Pricing model and evaluation treatment
- Supplier-facing document language
- Legal terms
- Privacy, security, accessibility, and compliance requirements
- Final release of procurement documents
- Supplier communications
- Addenda and clarifications

## Guardrails
The AI must not:

- Invent requirements
- Create supplier-specific language
- Make final legal decisions
- Interpret policy as final authority
- Score bids
- Select suppliers
- Make award recommendations
- Release procurement documents
- Replace procurement review
- Replace legal/privacy/security/accessibility/finance review
- Hide assumptions
- Ignore missing information
- Mix mandatory and rated requirements without clearly flagging the issue
- Rewrite approved legal clauses without legal review
- Change the meaning of user-provided content unless asked

## Example User Request
```text
Use the rfp-drafting-skill.md workflow to draft the service requirements section for this procurement. Separate mandatory requirements, rated requirements, supplier response instructions, risks, assumptions, and human review items.
```

## Example Output Instruction
```text
Do not simply write generic RFP language. First identify the business need, requirement type, missing information, evaluation implications, pricing implications, and risk areas. Then draft supplier-facing language and provide a human review checklist.
```

## Success Criteria
This skill is working when it helps the user:

- Move from generic AI drafting to structured procurement drafting
- Produce clearer RFx language
- Separate mandatory, rated, pricing, and contractual content
- Improve supplier response clarity
- Improve evaluation consistency
- Identify commercial and operational risks before release
- Keep final procurement decisions with accountable humans
