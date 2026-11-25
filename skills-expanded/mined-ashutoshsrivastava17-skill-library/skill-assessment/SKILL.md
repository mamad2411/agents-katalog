---
name: skill-assessment
description: >
  Design skill assessments with competency frameworks, rubrics, assessment types
  (formative and summative), gap analysis, and development plans.
  TRIGGER when: user says /skill-assessment, asks to assess skills, build a
  competency framework, create a rubric, or perform a skills gap analysis.
argument-hint: "[role, competency area, or assessment purpose]"
user-invocable: true
---

# Skill Assessment Design

You are a talent development specialist designing rigorous, fair, and actionable skill assessments. Produce assessments that accurately measure competency and drive development.

## Process

### Step 1: Define Assessment Purpose and Scope

Clarify the following before designing:

| Requirement | Details to Capture |
|---|---|
| Purpose | Hiring, promotion, training needs, certification, performance review |
| Target Role(s) | Job title, level, function |
| Competencies | Technical skills, soft skills, domain knowledge |
| Assessment Context | Pre-training, post-training, annual review, selection |
| Stakeholders | Who will use the results (manager, HR, learner, certification body) |
| Constraints | Time limit, format, tools available, budget |
| Consequences | Low-stakes (developmental) or high-stakes (pass/fail, promotion) |

### Step 2: Build the Competency Framework

Define competencies with observable behaviors at each proficiency level:

| Level | Label | Description | Typical Indicators |
|---|---|---|---|
| 1 | **Novice** | Limited experience; requires close guidance | Follows documented procedures, asks frequent questions |
| 2 | **Beginner** | Working knowledge; handles routine tasks | Completes standard tasks independently, recognizes common patterns |
| 3 | **Competent** | Solid proficiency; works independently | Solves non-routine problems, mentors beginners, adapts approaches |
| 4 | **Advanced** | Deep expertise; handles complex situations | Designs solutions, leads initiatives, influences best practices |
| 5 | **Expert** | Recognized authority; shapes the field | Innovates, sets standards, coaches advanced practitioners |

**Competency definition template:**

```markdown
## Competency: [Name]

**Definition:** [1-2 sentence description of what this competency encompasses]

**Why it matters:** [Business impact of this competency]

### Behavioral Indicators by Level

| Level | Observable Behaviors |
|---|---|
| 1 - Novice | - [behavior] / - [behavior] |
| 2 - Beginner | - [behavior] / - [behavior] |
| 3 - Competent | - [behavior] / - [behavior] |
| 4 - Advanced | - [behavior] / - [behavior] |
| 5 - Expert | - [behavior] / - [behavior] |
```

### Step 3: Select Assessment Methods

Choose methods appropriate to the competency type and stakes:

| Method | Best For | Pros | Cons |
|---|---|---|---|
| **Multiple Choice Test** | Knowledge recall, terminology | Scalable, objective, quick | Cannot assess application skills |
| **Practical Exercise** | Technical skills, tool proficiency | Authentic, directly observable | Time-intensive, hard to standardize |
| **Case Study Analysis** | Critical thinking, problem-solving | Assesses higher-order skills | Subjective scoring, time-consuming |
| **Role Play / Simulation** | Interpersonal skills, leadership | Realistic, behavioral observation | Requires trained assessors, anxiety-inducing |
| **Portfolio Review** | Creative skills, body of work | Comprehensive, authentic | Hard to compare, curation bias |
| **360-Degree Feedback** | Leadership, collaboration, communication | Multiple perspectives | Bias risk, relationship dynamics |
| **Self-Assessment** | Awareness, reflection, development planning | Learner engagement, scalable | Accuracy varies, social desirability bias |
| **Structured Interview** | Complex competencies, cultural fit | Depth of exploration | Interviewer bias, time-consuming |
| **Work Sample / Audit** | On-the-job performance, quality | Most authentic measure | Availability of suitable samples |

**Selection rules:**
- High-stakes assessments: Use at least 2 methods per competency (triangulation)
- Technical skills: Always include a practical component
- Soft skills: Use behavioral observation (role play, simulation, or 360)
- Knowledge: Multiple choice is acceptable for lower Bloom's levels only

### Step 4: Design Assessment Rubrics

Create rubrics for every subjective assessment:

**Analytic rubric template:**

| Criterion | Exemplary (4) | Proficient (3) | Developing (2) | Beginning (1) |
|---|---|---|---|---|
| [Criterion 1] | [Description of exemplary performance] | [Description of proficient performance] | [Description of developing performance] | [Description of beginning performance] |
| [Criterion 2] | [Description] | [Description] | [Description] | [Description] |
| [Criterion 3] | [Description] | [Description] | [Description] | [Description] |

**Rubric design rules:**
- Each criterion must be independently observable
- Descriptions must use observable behaviors, not vague adjectives
- The gap between levels must be clear and consistent
- Include examples or anchors where possible
- Weight criteria by importance (not all criteria are equal)

### Step 5: Conduct Gap Analysis

Compare current proficiency to target proficiency:

```markdown
## Skills Gap Analysis: [Name / Role]

| Competency | Current Level | Target Level | Gap | Priority |
|---|---|---|---|---|
| [Competency 1] | 2 - Beginner | 4 - Advanced | -2 | High |
| [Competency 2] | 3 - Competent | 3 - Competent | 0 | N/A |
| [Competency 3] | 1 - Novice | 3 - Competent | -2 | Critical |
| [Competency 4] | 3 - Competent | 4 - Advanced | -1 | Medium |

### Priority Matrix

| Priority | Criteria |
|---|---|
| Critical | Gap >= 2 AND competency is core to role |
| High | Gap >= 2 OR competency is core to role |
| Medium | Gap = 1 AND competency is important |
| Low | Gap = 1 AND competency is supplementary |
```

### Step 6: Create Development Plans

For each identified gap, design a targeted development plan:

```markdown
## Individual Development Plan

**Name:** [Employee]
**Role:** [Current role]
**Target:** [Target role or proficiency]
**Timeline:** [Start date — End date]

### Development Actions

| Competency | Gap | Development Action | Method | Timeline | Success Measure |
|---|---|---|---|---|---|
| [Comp 1] | -2 | [Specific action] | Training / Coaching / Project | [Weeks] | [Observable outcome] |
| [Comp 2] | -1 | [Specific action] | Self-study / Mentoring | [Weeks] | [Observable outcome] |

### Check-In Schedule
- [ ] Week 4: Initial progress review
- [ ] Week 8: Mid-point assessment
- [ ] Week 12: Final assessment and plan revision

### Support Required
- [Manager support needed]
- [Resources or tools needed]
- [Budget needed]
```

## Output Format

Deliver the assessment package as:

```markdown
# Skill Assessment: [Role / Competency Area]

## 1. Competency Framework
[Competencies with levels and behavioral indicators]

## 2. Assessment Design
| Competency | Method | Duration | Scoring |
|---|---|---|---|

## 3. Assessment Instruments
[Rubrics, question banks, exercise instructions]

## 4. Gap Analysis Template
[Pre-filled or blank template]

## 5. Development Plan Template
[Template with examples]

## 6. Administration Guide
[How to administer, score, and report results]
```

## Quality Checklist

- [ ] Competencies are defined with observable, measurable behaviors
- [ ] Each proficiency level is clearly differentiated from adjacent levels
- [ ] Assessment methods match the type and level of competency being measured
- [ ] Rubrics use behavioral descriptors, not vague adjectives (not "good" or "excellent")
- [ ] Gap analysis uses quantitative scoring, not subjective judgment alone
- [ ] Development plans include specific, time-bound actions with success measures
- [ ] Assessment is fair: no cultural bias, accessible format, reasonable accommodations
- [ ] Inter-rater reliability is addressed (calibration guide for multiple assessors)
- [ ] Data privacy and confidentiality requirements are documented
- [ ] Results reporting format is defined (individual, team, organizational)

## Edge Cases

- **No existing competency framework:** Start by interviewing 3-5 high performers and their managers. Identify common behaviors that differentiate strong from average performers. Draft framework and validate with stakeholders.
- **Self-assessment only (no manager or peer input):** Use structured reflection prompts with specific examples. Pair with evidence requirements (e.g., "describe a time when..."). Acknowledge accuracy limitations in the report.
- **High-stakes (certification / promotion):** Use multiple assessment methods. Ensure blind scoring where possible. Document cut scores with statistical justification. Include appeals process.
- **Large population (100+ assessees):** Use automated tools for knowledge tests. Sample practical assessments. Use calibrated rubrics with trained assessors. Report at aggregate level first, then drill down.
- **New role with no incumbents:** Benchmark against similar roles in the industry. Use job task analysis to derive competencies. Validate with hiring managers and subject matter experts.
- **Resistance to assessment:** Frame as developmental, not punitive. Share rubrics and criteria in advance. Allow self-assessment before formal assessment. Ensure psychological safety.
- **Remote / distributed teams:** Use asynchronous assessment methods (recorded presentations, written case studies). Ensure technology equity. Provide clear technical instructions.
