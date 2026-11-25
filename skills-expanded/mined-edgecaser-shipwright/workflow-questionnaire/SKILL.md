---
name: workflow-questionnaire
description: "Generates constraint-aware questionnaires that map a prospect or customer's workflows, surface friction points, and identify where processes can be optimized or eliminated. Accepts a configurable lens (e.g., AI/automation readiness, tool consolidation, compliance) that focuses all questions on a specific angle."
category: discovery
default_depth: standard
---

# Workflow Questionnaire

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Generates constraint-aware questionnaires that map a prospect or customer's workflows, surface friction points, and identify where processes can be optimized or eliminated. Accepts a configurable lens (e.g., AI/automation readiness, tool consolidation, compliance gaps) that scopes every question toward a specific optimization angle, so the questionnaire discovers what you need, not everything there is to know.

## When to Use

- Pre-sales discovery: understanding a prospect's current workflows before proposing a solution
- Scoping an automation or AI initiative inside a customer's operations
- Identifying friction, waste, or redundancy across a department or team
- Preparing for a process redesign, tool migration, or digital transformation engagement
- Building the evidence base for a business case or ROI model

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Quick pre-call prep or a single workflow area | Lens Definition + Core Questionnaire (one workflow domain) |
| **Standard** | Full prospect discovery covering multiple workflow domains | All sections |
| **Deep** | Enterprise engagement with multiple departments, compliance requirements, or transformation scope | All sections + cross-department dependency mapping questions, change readiness assessment, data maturity probe |

**Omit rules:** At Light depth, skip Scoring Rubric, Response Analysis Guide, and Follow-Up Decision Tree. Produce only the lens definition and a ready-to-use question set for the scoped workflow domain.

## Framework

### Step 1: Define the Lens

The lens constrains every question in the questionnaire. Without a lens, questionnaires sprawl into generic process audits that produce unfocused data.

**Inputs needed from the PM:**
- **Lens statement:** One sentence describing the optimization angle (e.g., "Identify where AI and automation can reduce manual effort in the prospect's data operations")
- **Target company/persona:** Who will answer these questions (role, department, company stage)
- **Workflow domains to cover:** Which areas of the business to probe (e.g., data ingestion, reporting, customer onboarding)
- **Out-of-scope declaration:** What the questionnaire should NOT explore (e.g., "not evaluating tool purchases" or "not assessing org structure")

```markdown
## Questionnaire Lens

**Lens:** [One sentence, the optimization angle]
**Target respondent:** [Role, department, seniority]
**Workflow domains:** [Comma-separated list]
**Out of scope:** [What we are deliberately not asking about]
**Company context:** [Industry, size, stage, if known]
```

**Lens validation rules:**
- The lens must be specific enough that you could explain to the respondent WHY each question is being asked
- If the lens is "understand their workflows" with no angle, push back, that produces an unfocused audit, not actionable discovery
- The lens determines question inclusion: if a question doesn't serve the lens, cut it

### Step 2: Map Workflow Domains to Question Themes

For each workflow domain, generate question themes that serve the lens. Every theme must trace back to the lens.

```markdown
## Theme Map

| Workflow Domain | Theme | Lens Connection | Question Count |
|---|---|---|---|
| [e.g., Data ingestion] | Current process & tools | Maps existing state before identifying automation targets | 3-5 |
| [e.g., Data ingestion] | Manual touchpoints & handoffs | Surfaces specific steps where AI/automation can replace human effort | 3-5 |
| [e.g., Data ingestion] | Failure modes & rework | Identifies error-prone steps where automation improves reliability | 2-3 |
| [e.g., Reporting] | Current process & tools | ... | 3-5 |
```

**Theme categories (select per domain based on lens):**
- **Current process & tools**, What exists today, who does it, what tools are involved
- **Manual touchpoints & handoffs**, Where humans intervene, pass work, wait, or re-key data
- **Failure modes & rework**, What breaks, what gets redone, what causes delays
- **Volume & frequency**, How often, how many, how long, establishes scale for ROI
- **Decision points**, Where judgment is required vs. where rules could apply
- **Pain & friction**, What frustrates the team, what they've tried to fix, what they've given up on
- **Desired outcomes**, What "better" looks like to them, in their words

Not every theme applies to every lens. A compliance lens would emphasize failure modes and decision points; an AI lens would emphasize manual touchpoints and decision points. Select themes that serve the lens.

### Step 3: Generate the Questionnaire

**Question design principles:**

1. **Behavioral, not hypothetical**, "Walk me through what happens when a new data file arrives" not "Would you benefit from automated ingestion?"
2. **Specific, not generic**, "How many hours per week does your team spend reformatting reports?" not "Is reporting a challenge?"
3. **Sequenced by workflow stage**, Questions follow the natural order of the work, not an arbitrary thematic order
4. **Calibrated to the respondent**, Executive questions focus on outcomes and costs; practitioner questions focus on steps and tools
5. **Lens-filtered**, Every question must pass the test: "Does the answer to this question help us evaluate [lens]?" If not, cut it.
6. **No leading questions**, "What's working well and what isn't?" not "Don't you find this process inefficient?"
7. **Closed + open pairing**, Pair quantitative questions (frequency, duration, count) with open follow-ups (why, what happens when, walk me through)

**Questionnaire structure:**

```markdown
# Workflow Discovery Questionnaire
## Lens: [lens statement]
## Respondent: [target role/persona]
## Estimated completion: [time estimate]

---

### Section 1: Context & Role (3-5 questions)
These questions establish the respondent's position in the workflow.

1. What is your role, and how long have you been in it?
2. Which of the following workflow areas do you personally touch? [list domains]
3. How many people on your team are involved in [domain]?
4. [Open] What does a typical week look like for you in terms of [domain] work?

---

### Section 2: [Workflow Domain A] ([N] questions)

#### Current State
5. Walk me through what happens when [triggering event]. Who does what, in what order?
6. What tools or systems are involved in this process? List all of them, including spreadsheets, email, and manual steps.
7. [Quantitative] How many [units] does your team process per [time period]?

#### [Theme from Step 2, filtered by lens]
8. [Behavioral question targeting the lens]
9. [Quantitative question establishing scale]
10. [Open follow-up probing for specifics]

#### Friction & Outcomes
11. What's the most time-consuming part of this process?
12. When this process fails or produces errors, what happens? How often?
13. If you could change one thing about how [domain] works today, what would it be and why?

---

### Section 3: [Workflow Domain B] ([N] questions)
[Same structure as Section 2, adapted to domain]

---

### Section 4: Cross-Cutting (3-5 questions)
These questions surface patterns that span workflow domains.

14. Where do you see the same data being entered or handled more than once?
15. Which handoffs between teams or systems cause the most delays?
16. [Lens-specific] Where do you think [optimization angle] could have the biggest impact? Why?
17. What has your team already tried to improve these processes? What happened?

---

### DO NOT ASK
- Leading questions: "Wouldn't automation solve this?"
- Solution-pitching questions: "How would you feel about a tool that does X?"
- Hypothetical questions: "If you had unlimited budget, what would you build?"
- Questions outside the declared lens scope
- Questions that assume problems exist: "What's broken in your process?"
  (Ask "Walk me through..." and let them surface the friction themselves)
```

### Step 4: Build the Scoring Rubric

Create a rubric for analyzing completed questionnaire responses. The rubric converts qualitative answers into structured, comparable data.

```markdown
## Response Scoring Rubric

### Per-Question Scoring

For quantitative questions, record the raw value.

For qualitative questions, score on two dimensions:

**Friction Severity (1-5):**
| Score | Meaning | Signal Words |
|---|---|---|
| 1 | No friction, process works smoothly | "works fine," "no issues," "happy with it" |
| 2 | Minor annoyance, workaround exists and is fast | "slightly annoying," "we just [quick fix]" |
| 3 | Moderate friction, regular time cost or error rate | "takes too long," "happens weekly," "we lose time" |
| 4 | Significant friction, major time cost, frequent errors, team frustration | "constant problem," "hours per week," "we've complained" |
| 5 | Critical, blocking business outcomes, causing churn/revenue loss | "can't scale," "losing customers," "compliance risk" |

**Lens Relevance (1-3):**
| Score | Meaning |
|---|---|
| 1 | Tangentially related to the lens, nice to know |
| 2 | Directly relevant, the lens applies to this friction point |
| 3 | High-impact target, strong lens fit AND high friction severity |

### Opportunity Score
**Opportunity = Friction Severity x Lens Relevance**

| Score Range | Interpretation |
|---|---|
| 12-15 | Top priority, high friction, strong lens fit |
| 7-11 | Worth pursuing, meaningful opportunity |
| 3-6 | Low priority, monitor but don't lead with |
| 1-2 | Out of scope or negligible friction |
```

### Step 5: Response Analysis Guide

Provide a template for synthesizing responses across multiple respondents.

```markdown
## Response Analysis Template

### Respondent Summary
| ID | Role | Department | Domain Coverage | Completion |
|---|---|---|---|---|
| R1 | [role] | [dept] | [domains answered] | Full / Partial |

### Friction Heatmap (by domain x theme)
| Domain | Current State | Manual Touchpoints | Failure Modes | Volume | Decision Points | Pain |
|---|---|---|---|---|---|---|
| [Domain A] | [avg score] | [avg score] | [avg score] | [raw data] | [avg score] | [avg score] |

### Top Opportunities (ranked by Opportunity Score)
| Rank | Domain | Friction Point | Avg Severity | Lens Relevance | Opp. Score | Evidence |
|---|---|---|---|---|---|---|
| 1 | [domain] | [specific friction] | [N] | [N] | [N] | "[respondent quote or data point]" |

### Cross-Respondent Patterns
- [Pattern 1: friction point mentioned by N of M respondents]
- [Pattern 2: workflow domain with highest aggregate friction]

### Contradictions & Outliers
- [Where respondents disagree, signals different roles experience the workflow differently]
```

### Step 6: Follow-Up Decision Tree

Map questionnaire findings to next actions.

```markdown
## Follow-Up Decision Tree

| Finding Pattern | Next Action | Shipwright Skill |
|---|---|---|
| High friction + high lens relevance across respondents | Deep-dive interview on top 3 friction points | discovery-interview-prep |
| High friction but LOW lens relevance | Park, real problem, but not in scope for this engagement | (none, log for future) |
| Low friction across the board | Revisit lens, either the lens is wrong or this isn't a pain area | Re-run Step 1 with refined lens |
| Contradictory responses across roles | Map the workflow end-to-end with multiple stakeholders | customer-journey-mapping |
| Clear opportunity with quantifiable scale | Build the business case | lean-canvas or pricing-strategy |
| Respondent describes desired outcome clearly | Frame as JTBD and validate | jobs-to-be-done |
```

## Minimum Evidence Bar

**Required inputs:** A lens statement with a specific optimization angle, a target respondent role, and at least one workflow domain to cover.

**Acceptable evidence:** Prior customer conversations, sales call notes, industry knowledge, existing process documentation, support tickets, or stated business objectives from the prospect.

**Insufficient evidence:** If no lens statement is provided or the lens is too vague to filter questions (e.g., "understand their business"), state "Insufficient evidence: lens is undefined or too broad to generate a focused questionnaire" and stop. Recommend the PM define a specific optimization angle before proceeding. If no workflow domains are specified, ask the PM to identify at least one domain or provide context about the prospect's business so domains can be inferred.

**Hypotheses vs. findings:**
- **Findings:** The questionnaire structure and question design are outputs of this skill, they are artifacts, not claims about the customer.
- **Hypotheses:** The theme map (Step 2) hypothesizes which themes will surface the most useful data for the lens. Label theme selections as "hypothesis, validate after first 2-3 responses" and adjust the questionnaire if early responses indicate a theme is unproductive.

## Output Format

Produce up to six artifacts depending on depth:

1. **Questionnaire Lens**, lens statement, target respondent, domains, out-of-scope declaration
2. **Theme Map**, workflow domains mapped to question themes with lens connection
3. **Questionnaire**, ready-to-use, numbered question set organized by workflow domain
4. **Scoring Rubric**, friction severity and lens relevance scales with opportunity scoring
5. **Response Analysis Template**, synthesis framework for multiple respondents
6. **Follow-Up Decision Tree**, maps finding patterns to next actions and Shipwright skills

**Shipwright Signature (required closing):**
7. **Decision Frame**, Primary lens and workflow domains selected, trade-off between questionnaire breadth (more domains) vs. depth (more questions per domain), confidence that the lens will surface actionable data with evidence quality, owner, date, revisit trigger (e.g., "revisit lens after first 3 responses if top opportunities don't emerge")
8. **Unknowns & Evidence Gaps**, Workflow domains not covered, respondent roles not represented, assumptions about the prospect's operations that the questionnaire itself will test
9. **Pass/Fail Readiness**, PASS if the questionnaire has a defined lens, every included question traces to it, each in-scope workflow domain has sufficient behavioral coverage for the decision, and no question is leading or hypothetical. At Light depth, the scoring rubric is not required. Do not manufacture questions for a domain with no supported workflow evidence; omit it and name the gap. FAIL if the lens is undefined, questions are leading/hypothetical, or questions fall outside declared scope.
10. **Recommended Next Artifact**, Which Shipwright skill to run next and why (typically discovery-interview-prep for deep-dive follow-ups, or jobs-to-be-done for framing validated friction as job statements)

## Common Mistakes to Avoid

- **No lens or a vague lens**, "Understand their workflows" is not a lens. Without a specific angle, the questionnaire becomes an unfocused process audit that wastes the respondent's time and produces data you can't act on.
- **Leading questions that pitch the solution**, "How much time would you save with automation?" presumes the answer. Ask "How much time does your team spend on [specific manual step] per week?" and let the implication land on its own.
- **Asking about hypothetical futures instead of current behavior**, "Would you use an AI tool for this?" produces unreliable data. "Walk me through what happens when [trigger]" produces real workflow intelligence.
- **Too many questions without prioritization**, A 60-question questionnaire gets abandoned. Standard depth should target 25-35 questions. If you need more, split into domain-specific modules the respondent can complete in stages.
- **Skipping the scoring rubric**, Raw qualitative responses are hard to compare across respondents. The rubric converts "this is really painful" into a severity score you can rank and prioritize.
- **Asking the same question with different wording**, Review the full questionnaire for redundancy. Each question should surface unique information. If two questions would get the same answer, cut one.
- **Ignoring the out-of-scope declaration**, If the lens says "not evaluating tool purchases," don't ask "what tools would you consider buying?" Scope discipline keeps the questionnaire credible.

## Weak vs. Strong Output

**Weak:**
> "What challenges do you face in your day-to-day work?"

No lens, no workflow specificity, invites vague opinion. A respondent could answer this in a hundred directions, none of which help you evaluate a specific optimization angle.

**Strong:**
> "Walk me through what happens after a customer submits a support ticket. Who touches it first, what system does it go into, and how does it get to the person who resolves it?"
> Follow-up: "How many tickets per week require someone to manually re-enter information from one system to another?"

Anchored to a specific workflow domain, behavioral, sequenced (process first, then quantitative), and directly serves an automation lens by surfacing manual data re-entry.
