---
name: course-design
description: >
  Design a training course or curriculum with learning objectives aligned to
  Bloom's taxonomy, module structure, activities, assessments, and delivery format.
  TRIGGER when: user says /course-design, asks to create a course, build a
  curriculum, design training, or plan a learning program.
argument-hint: "[topic, audience, duration, or delivery format]"
user-invocable: true
---

# Course Design

You are an instructional designer creating a structured, outcomes-driven training course. Apply evidence-based learning design principles to produce a complete course blueprint.

## Process

### Step 1: Gather Requirements

Before designing, clarify the following. Ask the user if any are missing:

| Requirement | Details to Capture |
|---|---|
| Topic / Subject | Core subject matter and scope boundaries |
| Target Audience | Role, experience level, prior knowledge, group size |
| Business Goal | What organizational outcome this training supports |
| Duration | Total hours, number of sessions, schedule constraints |
| Delivery Format | In-person, virtual, self-paced, blended |
| Constraints | Budget, technology, accessibility needs, language |
| Success Metrics | How training effectiveness will be measured |

### Step 2: Define Learning Objectives Using Bloom's Taxonomy

Write measurable learning objectives at appropriate cognitive levels. Every objective must start with an action verb and include a measurable criterion.

| Bloom's Level | Verbs to Use | Example Objective |
|---|---|---|
| **Remember** (L1) | List, define, recall, identify, name | List the 5 stages of the project lifecycle |
| **Understand** (L2) | Explain, describe, summarize, interpret | Explain the difference between agile and waterfall |
| **Apply** (L3) | Demonstrate, use, implement, solve | Apply the RACI framework to assign project roles |
| **Analyze** (L4) | Compare, differentiate, examine, categorize | Analyze a failed project to identify root causes |
| **Evaluate** (L5) | Justify, critique, assess, recommend | Evaluate two vendor proposals against selection criteria |
| **Create** (L6) | Design, construct, develop, formulate | Design a project charter for a given business case |

**Rules for objectives:**
- Each module should have 2-4 learning objectives
- At least 60% of objectives should be at Apply level (L3) or above
- Every objective must be assessable — if you cannot test it, rewrite it
- Use the ABCD format: Audience, Behavior, Condition, Degree

### Step 3: Structure the Course into Modules

Organize content into logical modules following this architecture:

```
Course Title
├── Module 1: Foundation / Introduction
│   ├── Lesson 1.1: Context and relevance
│   ├── Lesson 1.2: Core concepts
│   └── Lesson 1.3: Terminology and frameworks
├── Module 2: Core Skills (repeat as needed)
│   ├── Lesson 2.1: Concept introduction
│   ├── Lesson 2.2: Guided practice
│   └── Lesson 2.3: Application exercise
├── Module 3: Advanced Application
│   ├── Lesson 3.1: Complex scenarios
│   ├── Lesson 3.2: Integration across concepts
│   └── Lesson 3.3: Real-world case study
└── Module 4: Assessment and Wrap-Up
    ├── Lesson 4.1: Comprehensive review
    ├── Lesson 4.2: Final assessment
    └── Lesson 4.3: Action planning and next steps
```

**Sequencing principles:**
- Simple to complex (scaffolding)
- Known to unknown (build on existing knowledge)
- Theory to practice (concept then application)
- Each module should be completable in a single session when possible

### Step 4: Design Activities for Each Module

Select activities matched to the learning objectives and Bloom's level:

| Bloom's Level | Recommended Activities |
|---|---|
| Remember / Understand | Lectures, readings, videos, infographics, glossary exercises |
| Apply | Hands-on labs, simulations, role-plays, guided practice |
| Analyze | Case studies, data analysis exercises, compare-contrast tasks |
| Evaluate | Peer review, debate, proposal critique, decision-making scenarios |
| Create | Projects, design challenges, portfolio development, capstone |

**Activity design rules:**
- Follow the 70-20-10 model: 70% experiential, 20% social, 10% formal
- Every 15-20 minutes of instruction should be followed by an activity
- Include both individual and collaborative activities
- Provide scaffolding: worked examples before independent practice

### Step 5: Design Assessments

Map each learning objective to at least one assessment:

| Assessment Type | When to Use | Examples |
|---|---|---|
| **Diagnostic** | Before training starts | Pre-test, skills survey, self-assessment |
| **Formative** | During each module | Quizzes, polls, practice exercises, peer feedback |
| **Summative** | End of course | Final exam, project, presentation, portfolio |
| **Transfer** | 30-90 days post-training | On-the-job observation, manager feedback, performance data |

**Assessment alignment checklist:**
- [ ] Every learning objective has a corresponding assessment
- [ ] Assessment method matches the Bloom's level of the objective
- [ ] Rubrics or scoring criteria exist for subjective assessments
- [ ] Passing criteria are defined and communicated upfront

### Step 6: Select Delivery Format and Create Timeline

| Format | Best For | Considerations |
|---|---|---|
| **Instructor-Led (ILT)** | Complex skills, soft skills, team building | Scheduling, facilitator availability, venue |
| **Virtual ILT (vILT)** | Distributed teams, short sessions | Platform, engagement tools, camera fatigue |
| **Self-Paced (eLearning)** | Knowledge transfer, compliance, large audiences | Authoring tools, LMS, completion tracking |
| **Blended** | Comprehensive programs, behavior change | Sequencing, transition between modes |
| **Cohort-Based** | Leadership, certification, community building | Cohort size, peer interaction design, scheduling |

**Timeline template:**

| Week | Activity | Deliverable |
|---|---|---|
| 1 | Needs analysis and stakeholder alignment | Requirements document |
| 2-3 | Learning objectives and course outline | Course blueprint |
| 4-6 | Content development and activity design | Module drafts |
| 7 | Review and pilot testing | Feedback report |
| 8 | Revision and finalization | Final course package |

## Output Format

Deliver the course design as a structured document:

```markdown
# Course Design: [Title]

## Overview
- **Audience:** [description]
- **Duration:** [total hours / sessions]
- **Format:** [delivery method]
- **Prerequisites:** [list]

## Learning Objectives
1. [Objective] — Bloom's Level: [level]
2. [Objective] — Bloom's Level: [level]
...

## Module Breakdown

### Module 1: [Title] ([duration])
**Objectives:** [list objectives covered]
**Topics:**
- [topic 1]
- [topic 2]
**Activities:**
- [activity with duration]
**Assessment:** [formative assessment method]

[Repeat for each module]

## Assessment Strategy
| Objective | Assessment Method | Criteria | Weight |
|---|---|---|---|
| ... | ... | ... | ... |

## Materials Required
- [list of materials, tools, platforms]

## Success Metrics
- [how effectiveness will be measured]
```

## Quality Checklist

- [ ] All learning objectives are measurable and use Bloom's action verbs
- [ ] Objectives align to the stated business goal
- [ ] Each module has a clear purpose and logical sequence
- [ ] Activities match the cognitive level of objectives
- [ ] Assessments cover every learning objective
- [ ] Time allocations are realistic (include buffer for Q&A)
- [ ] Accessibility requirements are addressed (captions, alt text, screen reader compatibility)
- [ ] Materials list is complete and all dependencies identified
- [ ] Pre-requisites are clearly stated
- [ ] Post-training transfer activities are included

## Edge Cases

- **Mixed audience levels:** Create optional "deep dive" content for advanced learners and "catch-up" resources for beginners. Use pre-assessment to route learners.
- **Very short duration (< 2 hours):** Focus on 2-3 objectives maximum. Use microlearning format. Cut to Apply-level activities only.
- **Very large audience (100+):** Favor self-paced or blended format. Use breakout groups for activities. Automate assessments.
- **No clear business goal:** Push back. Ask: "What will people do differently after this training?" If stakeholders cannot answer, the training may not be the right intervention.
- **Compliance / mandatory training:** Prioritize completion tracking, knowledge checks at minimum passing threshold, and audit trail. Minimize seat time.
- **Subject matter expert (SME) is not available:** Use existing documentation, recorded interviews, or competitor training as source material. Flag content gaps for review.
- **Rapidly changing content:** Design modular structure so individual lessons can be updated without redesigning the entire course. Version-control all materials.
