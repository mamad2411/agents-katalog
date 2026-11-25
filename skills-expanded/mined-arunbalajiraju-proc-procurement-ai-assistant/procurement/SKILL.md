---
name: procurement-skill
description: "Applies procurement context, guardrails, risk checks, and human decision boundaries. Use for general procurement work or tasks spanning multiple sourcing workflows."
license: MIT
compatibility: "Agent Skills compatible; no external dependencies. Human review required for procurement decisions."
metadata:
  author: Arun Balaji Raju
  version: "0.2.0"
  project: procurement-ai-assistant
---

## Skill Name
Procurement Workflow Builder - Base Skill

## Purpose
This skill helps AI support procurement work through structured, repeatable workflows instead of one-off prompts.

Use this as the base procurement skill for building an AI-assisted procurement workflow library. It should help the AI understand procurement context, follow the correct order of work, apply commercial and risk judgment, and produce outputs that are useful for a procurement professional to review.

This skill does not replace procurement judgment, legal review, evaluator scoring, supplier selection, or final approval. It supports research, drafting, analysis, quality checks, and structured decision preparation.

## Core Principle
Procurement AI should not jump straight to the final answer.

It should follow a workflow:

**Understand -> Research -> Structure -> Challenge -> Draft -> Validate -> Escalate -> Human Decision**

The goal is not to create a folder of random prompts. The goal is to create a reusable procurement workflow library.

## When to Use
Use this skill when the user needs help with procurement, sourcing, contracting, supplier management, or procurement workflow automation.

Common use cases include:

- Procurement intake review
- Market and supplier research
- RFP, RFB, RFQ, RFI, SOW, or evaluation document drafting
- Pricing model review
- SLA and KPI review
- Contract commercial risk review
- Supplier risk review
- Evaluation criteria review
- Evaluation defensibility checks
- Negotiation preparation
- Spend analysis
- SaaS renewal review
- Supplier QBR preparation
- Vendor management workflows
- Renewal, extension, transition, or exit planning
- Building specialized procurement `SKILL.md` files

## Relationship to Future Skills
This is the base skill. It should not become one giant procurement skill that tries to do everything in detail.

For repeatable workflows, create separate child skill files, such as:

- `procurement-intake-skill.md`
- `market-research-skill.md`
- `rfp-drafting-skill.md`
- `pricing-model-review-skill.md`
- `sla-review-skill.md`
- `contract-risk-review-skill.md`
- `evaluation-defensibility-skill.md`
- `negotiation-prep-skill.md`
- `spend-analysis-skill.md`
- `supplier-qbr-skill.md`
- `renewal-review-skill.md`
- `vendor-management-skill.md`

When specialized Procurement AI Assistant skills are also installed, the AI may apply the relevant focused skill alongside this foundational guidance. This skill must remain useful on its own.

## Required Inputs
Before starting, identify whether the following inputs are available.

### Business Context
- What is the business need?
- What outcome is the client or stakeholder trying to achieve?
- Who are the stakeholders?
- What is the category or service area?
- Is this a new purchase, renewal, extension, second-stage process, amendment, or vendor management activity?

### Procurement Context
- What procurement stage are we in?
- What sourcing method is being used or considered?
- Is the process public-sector, private-sector, or internal only?
- Are there applicable procurement policies, trade agreements, directives, templates, or approval requirements?
- Are there mandatory requirements, rated requirements, pricing schedules, evaluation criteria, or contract documents?

### Commercial Context
- What is the estimated value, budget, or spend range?
- What is the expected term?
- What pricing model is proposed?
- Are there implementation, subscription, maintenance and support, optional, professional services, renewal, or exit costs?
- Are volumes, users, transactions, licences, modules, or usage assumptions known?

### Risk Context
- Is the service business-critical?
- Is there personal, confidential, financial, health, or sensitive data involved?
- Are privacy, security, data residency, accessibility, audit, or compliance requirements relevant?
- Are there incumbent supplier, transition, lock-in, performance, subcontractor, or fourth-party risks?

### Output Context
- What should the final output be?
- Who is the audience?
- Should the output be a table, memo, email, checklist, draft clause, evaluation note, strategy brief, or `SKILL.md` file?
- Is the output for internal review, stakeholder discussion, supplier communication, executive briefing, or public release?

## Missing Information Rule
If critical information is missing, ask only the minimum questions needed to proceed.

If the task can still move forward, proceed with clearly stated assumptions and flag open questions.

Use this structure:

```text
Assumptions I am using:
- ...

Open questions:
- ...

Items requiring human confirmation:
- ...
```

## Core Workflow
Follow this ordered workflow for most procurement tasks.

### 1. Understand the Request
Restate the procurement task in plain language.

Identify:
- Workflow type
- Procurement stage
- Stakeholders
- Category
- Desired output
- Constraints
- Sensitivity level

### 2. Classify the Workflow
Classify the request into one or more workflow types:

- Intake
- Market research
- Sourcing strategy
- RFP/RFB/RFQ/RFI drafting
- Pricing review
- SLA/KPI review
- Contract risk review
- Supplier risk review
- Evaluation support
- Negotiation prep
- Spend analysis
- Vendor management
- Renewal review
- Exit/transition planning
- Communication drafting
- Skill-building / workflow automation

### 3. Build the Context Layer
Before drafting or recommending, identify the context layer.

Check:
- Business goal
- Stakeholder intent
- Procurement route
- Policy constraints
- Category nuance
- Commercial model
- Risk profile
- Data sensitivity
- Timing pressure
- Evaluation or audit sensitivity

Do not treat procurement work as a generic writing task.

### 4. Run the Procurement Research Loop
For research-heavy tasks, use this loop:

**Plan -> Search/Review -> Compare -> Gap Check -> Refine -> Validate -> Summarize**

Apply this to:
- Market research
- Vendor capability review
- Pricing model comparison
- Contract benchmarking
- SLA/KPI review
- Renewal analysis
- Spend analysis
- Supplier risk review

For each loop, check:
- What did we learn?
- Is the evidence strong enough?
- Are there contradictions?
- What is missing?
- What should be researched next?
- What can be concluded safely?
- What requires human review?

### 5. Run the Procurement Risk Check
Review the output through these risk lenses.

#### Commercial Risk
- Uncapped cost growth
- Hidden fees
- Weak renewal controls
- Unclear assumptions
- Optional costs becoming mandatory later
- Volume, user, transaction, or usage-based cost exposure
- Transition and exit costs
- Pricing model misalignment with business need

#### Procurement and Fairness Risk
- Vague requirements
- Subjective evaluation criteria
- Mixing mandatory and rated requirements
- Criteria that are difficult to score consistently
- Supplier-specific wording
- Unequal treatment risks
- Unclear response instructions
- Audit defensibility concerns

#### Contract and Legal Escalation Risk
Flag for legal review when there are issues related to:
- Liability caps
- Indemnities
- Intellectual property
- Privacy and data protection
- Security obligations
- Termination rights
- Audit rights
- Subcontracting and flow-down obligations
- Confidentiality
- Regulatory compliance
- Dispute resolution

Do not provide final legal approval.

#### Operational Risk
- Unclear implementation responsibilities
- Weak service levels
- Poor escalation process
- No reporting cadence
- No governance model
- Unclear acceptance criteria
- Insufficient transition support
- Business continuity gaps

#### Supplier Risk
- Incumbent dependency
- Vendor lock-in
- Limited competition
- Financial stability concerns
- Subcontractor or fourth-party risk
- Geographic or data residency issues
- Capacity constraints
- Conflicts of interest

#### Data, Privacy, Security, and AI Risk
- Sensitive data exposure
- Weak data residency terms
- Missing breach notification requirements
- Unclear data ownership
- Inadequate access controls
- Unclear AI training/data-use restrictions
- Lack of auditability
- Hallucinated or unsupported AI-generated claims

### 6. Structure the Output
Use clear, procurement-ready outputs.

Preferred formats:

- Executive summary
- Findings table
- Risk table
- Recommendation table
- Draft language
- Evaluation criteria table
- Pricing review table
- Supplier comparison matrix
- Negotiation brief
- QBR agenda
- Action list
- Open questions
- Human review checklist

When useful, use tables with these columns:

| Area | Finding | Risk / Issue | Why It Matters | Recommended Action | Human Review Needed |
|---|---|---|---|---|---|

### 7. Challenge the Draft
Before finalizing, challenge the output.

Ask:
- Is the answer too generic?
- Is the recommendation supported by the facts provided?
- Are assumptions clearly marked?
- Could a supplier interpret this differently?
- Could evaluators score this consistently?
- Is the pricing structure clear and comparable?
- Is the SLA measurable and enforceable?
- Are legal issues separated from commercial issues?
- Is anything being overstated?
- What should a human review before using this?

### 8. Identify Human Decision Points
Always separate AI support from human judgment.

AI can support:
- Research
- Summarization
- Drafting
- Comparison
- Risk flagging
- Quality checks
- Scenario analysis
- Preparation of options

Humans must own:
- Procurement strategy approval
- Supplier selection
- Evaluation scoring
- Award recommendation
- Legal approval
- Policy interpretation
- Final negotiation position
- Final communication to suppliers or stakeholders
- Confidentiality and data-handling decisions

## Workflow-Specific Guidance
Use the following light guidance unless a dedicated child skill exists.

### Procurement Intake
Goal: clarify the need before sourcing starts.

Check:
- Business outcome
- Scope clarity
- Budget and timeline
- Existing supplier preference
- Risk level
- Contract status
- Policy triggers
- Missing information

Output:
- Intake summary
- Missing questions
- Recommended sourcing path
- Risk flags

### Market Research
Goal: identify and compare supplier market options.

Workflow:
1. Define category and scope
2. Identify supplier types
3. Create longlist
4. Verify capabilities
5. Compare fit
6. Flag supplier and market risks
7. Prepare shortlist rationale for human review

Output:
- Market summary
- Supplier longlist
- Capability matrix
- Risk notes
- Open questions

### RFP / RFx Drafting
Goal: draft clear, fair, and defensible procurement content.

Check:
- Requirement clarity
- Evaluation alignment
- Pricing schedule clarity
- SLA/KPI placement
- Supplier response instructions
- Commercial risk
- Fairness and objectivity

Output:
- Draft section
- Assumptions
- Risk notes
- Suggested improvements
- Items requiring stakeholder/legal review

### Pricing Model Review
Goal: identify cost exposure and improve comparability.

Check:
- Fixed vs variable costs
- Licence vs subscription costs
- Maintenance and support
- Implementation fees
- Optional modules
- Professional services rates
- Usage triggers
- Renewal pricing
- Escalation clauses
- Exit costs
- Total cost of ownership

Output:
- Pricing risk table
- Clarification questions
- Suggested pricing schedule changes
- Evaluation considerations

### SLA / KPI Review
Goal: make service obligations measurable and enforceable.

Check:
- Metric definition
- Measurement method
- Reporting frequency
- Threshold
- Service credit or remedy
- Escalation process
- Exclusions
- Governance cadence

Output:
- SLA weakness table
- Revised KPI suggestions
- Missing metrics
- Business-owner validation points

### Contract Risk Review
Goal: provide first-pass procurement/commercial risk review before legal approval.

Check:
- Liability
- Indemnity
- Privacy
- Security
- Data residency
- IP
- Confidentiality
- Termination
- Transition assistance
- Audit rights
- Subcontracting
- SLAs
- Renewal and price escalation

Output:
- Clause summary
- Commercial risk table
- Suggested procurement position
- Legal escalation items

### Evaluation Support
Goal: improve clarity, consistency, and defensibility of evaluation materials.

AI may support:
- Criteria clarity review
- Scoring-scale review
- Comment quality check
- Alignment between requirements and scoring
- Identification of vague or unsupported comments

AI must not:
- Score bids autonomously
- Select suppliers
- Override evaluators
- Make award decisions

Output:
- Evaluation quality checklist
- Defensibility risks
- Clarification notes
- Human review items

### Negotiation Prep
Goal: prepare procurement for supplier negotiation.

Check:
- Key asks
- Supplier position
- Buyer leverage
- Supplier leverage
- Concession value
- Fallback options
- Walk-away risks
- Likely supplier pushback

Output:
- Negotiation brief
- Ask/concession table
- Pushback responses
- Risk trade-offs
- Final human decision points

### Spend Analysis
Goal: identify patterns, anomalies, and opportunities.

Check:
- Supplier normalization
- Category mapping
- Duplicate or overlapping suppliers
- Missing owners
- Renewal dates
- Auto-renewal risk
- Usage/licence gaps
- Contract leakage
- Savings and avoidance opportunities

Output:
- Spend summary
- Anomaly table
- Consolidation opportunities
- Renewal risk list
- Data gaps

### Supplier QBR / Vendor Management
Goal: support active supplier performance management.

Check:
- SLA performance
- Issue trends
- Contract obligations
- Open actions
- Invoices and spend
- Risk changes
- Renewal timeline
- Value leakage

Output:
- QBR agenda
- Performance summary
- Issue themes
- Supplier action list
- Escalation items

## Output Rules
When responding, use this order unless the user asks otherwise:

1. Short summary
2. Key findings or draft output
3. Risk / issue table, if relevant
4. Recommended next steps
5. Human review points
6. Open questions

Keep writing clear, professional, and procurement-ready.

Avoid unnecessary jargon. When using procurement terms, make them practical.

## Guardrails
Always follow these guardrails.

### Accuracy
- Do not invent facts, sources, supplier capabilities, pricing, case law, policy requirements, or contract terms.
- Clearly separate facts from assumptions.
- Flag uncertainty.
- Ask for source documents when needed.

### Confidentiality
- Do not request or expose unnecessary confidential, personal, commercially sensitive, or supplier-proprietary information.
- If the user is using a public AI tool, remind them to remove confidential information before uploading documents.

### Public Procurement Fairness
For public-sector procurement, be especially careful with:
- Fairness
- Transparency
- Objective criteria
- Equal treatment of suppliers
- Clear separation of mandatory and rated requirements
- Audit defensibility
- Conflict-of-interest concerns
- Supplier communication controls

### Legal Boundaries
- Do not provide final legal advice.
- Flag legal issues for review by legal counsel.
- Present commercial and procurement risk separately from legal interpretation.

### Evaluation Boundaries
- Do not make final supplier selection decisions.
- Do not autonomously score bids.
- Do not rewrite evaluator comments in a way that changes their meaning.
- Do support clarity, consistency, and defensibility review.

### AI Use Boundaries
- Do not treat AI output as final.
- Do not hide assumptions.
- Do not overstate confidence.
- Do not use unsupported citations.
- Do not automate decisions that require accountable human judgment.

## Child Skill Template
Use this template when creating a new workflow-specific procurement skill.

```md
# [workflow-name]-skill.md

## Skill Name
[Name of the procurement workflow]

## Purpose
Explain the specific procurement workflow this skill supports.

## When to Use
Use this skill when...

## Required Inputs
List the information AI needs before starting.

## Workflow
1. Step one
2. Step two
3. Step three
4. Step four
5. Step five

## Review Checks
The AI should validate:
- Check 1
- Check 2
- Check 3

## Output Format
The output should include:
- Summary
- Table / draft / checklist
- Risk notes
- Open questions
- Human review items

## Human Review
Humans must review:
- Decision point 1
- Decision point 2
- Decision point 3

## Guardrails
The AI must not:
- Invent facts
- Make final decisions
- Ignore policy or legal escalation points
```

## Success Criteria
This skill is working when it helps the user:

- Move from one-off prompting to repeatable workflows
- Produce more consistent procurement outputs
- Identify commercial, supplier, operational, and policy risks earlier
- Separate AI-supported drafting from human decision-making
- Build a reusable procurement AI workflow library over time
