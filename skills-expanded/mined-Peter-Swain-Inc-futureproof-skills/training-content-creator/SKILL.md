---
name: training-content-creator
description: |
  Creates training content — onboarding modules, workshop curricula,
  enablement playbooks, knowledge base articles, and microlearning — using
  ADDIE diagnostics, Mager performance objectives, and Bloom's taxonomy.
  Use when a user says "build a training module for new hires", "design a
  workshop on X", "create an enablement playbook for the sales team", or
  "write a course curriculum on Y". For learner-facing training material
  that teaches a skill, not procedural SOPs (use sop-builder) or
  client-side activation flows (use client-onboarding-designer).
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="training-content-creator")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly any existing brand voice guidelines, team structure, ICA definitions, product/service descriptions, and prior training content that has been created or tested.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **Content type**: What are you building? (onboarding module, SOP, knowledge base article, workshop curriculum, video script, enablement playbook, assessment/quiz, microlearning sequence)
- **Target learner**: Who will consume this content? (new hires, existing team members, contractors, clients, partners — role, seniority, current skill level)
- **Subject matter**: What specific process, skill, or knowledge domain must the training cover?
- **Performance outcome**: What should the learner be able to *do* after completing this training? (specific behaviour, not vague comprehension)
- **Existing materials**: Any current documentation, recordings, tribal knowledge, or subject-matter expert notes to incorporate?
- **Delivery constraints**: Format requirements, platform limitations (LMS, Notion, Google Docs, Loom), maximum duration or length, compliance or regulatory requirements?

## Step 3: Conduct Training Needs Analysis

Before creating content, perform a structured needs analysis using the **ADDIE-aligned diagnostic framework**:

### 3a. Gap Identification
- **Current state**: What does the target learner currently know or do regarding this subject?
- **Desired state**: What is the specific, observable performance standard expected post-training?
- **Gap severity**: Classify as foundational (no prior exposure), remedial (inconsistent execution), or advanced (optimisation of existing competence)

### 3b. Learning Objective Architecture
Construct objectives using the **Mager Performance Objective Model** — each objective must contain:
1. **Performance**: The observable action the learner will demonstrate (use Bloom's taxonomy action verbs — *identify*, *execute*, *evaluate*, not *understand* or *know*)
2. **Condition**: The context in which performance occurs (tools available, information provided, time constraints)
3. **Criterion**: The measurable standard of acceptable performance (accuracy threshold, time-to-completion, quality rubric score)

Draft 3–7 learning objectives depending on content scope. Prioritise using a **MoSCoW matrix** (Must / Should / Could / Won't) based on business impact and learner readiness.

### 3c. Instructional Strategy Selection
Based on the gap analysis and content type, recommend the optimal instructional strategy:

| Content Type | Recommended Strategy | Rationale |
|---|---|---|
| Procedural SOP | Step-by-step with decision trees + embedded screenshots | Reduces cognitive load for sequential tasks |
| Conceptual onboarding | Scenario-based with progressive disclosure | Builds mental models through contextual anchoring |
| Skill-based enablement | Demonstrate → Practice → Feedback loop | Aligns with Kolb's experiential learning cycle |
| Compliance/regulatory | Case-study-driven with assessment gates | Satisfies audit requirements while maintaining engagement |
| Workshop curriculum | Facilitator guide + participant workbook + debrief protocol | Ensures consistent delivery across facilitators |

Apply any user-specific `instructions` from FutureProof context — particularly brand voice, terminology standards, and any organisational learning design preferences.

## Step 4: Build Content Architecture

Create the **Training Content Blueprint** before writing any body content:

### 4a. Module Structure Map
```
Module Title: [Descriptive, action-oriented title]
├── Learning Objectives (from Step 3b)
├── Prerequisites (what the learner must already know/have access to)
├── Section 1: [Topic]
│   ├── Concept introduction (context-setting narrative)
│   ├── Core instruction (the "what" and "how")
│   ├── Worked example or scenario
│   └── Knowledge check (formative assessment)
├── Section 2: [Topic]
│   ├── ...
├── Section N: [Topic]
│   ├── ...
├── Synthesis exercise (summative — ties all sections together)
├── Quick reference card (one-page job aid for post-training use)
└── Assessment / Certification gate (if applicable)
```

### 4b. Content Density Calibration
Apply the **7±2 rule** (Miller's Law) to each section:
- No more than 7 key concepts per module
- No more than 5 steps per procedural block before a checkpoint
- Chunk complex processes into sub-procedures with clear entry/exit criteria

### 4c. Media and Interaction Mapping
For each section, specify:
- **Primary content format**: Written narrative, annotated screenshot sequence, video walkthrough script, interactive decision tree, or facilitator-led discussion prompt
- **Supporting assets needed**: Diagrams, templates, checklists, screen recordings, role-play scenarios
- **Engagement mechanism**: Reflection question, practice exercise, peer discussion prompt, quiz, or simulation

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Develop Training Content

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


Write the full training content following the architecture from Step 4. Apply these quality standards throughout:

### 5a. Writing Standards
- **Voice**: Match the organisation's established tone from FutureProof context; default to professional-conversational (authoritative but approachable, second-person address)
- **Sentence structure**: Maximum 25 words per sentence for procedural content; maximum 35 for conceptual content
- **Terminology**: Use the learner's operational vocabulary — define specialised terms on first use with inline definitions
- **ICA alignment**: Where training involves customer-facing activities, ensure all examples, scenarios, and language reflect the ICA's context, pain points, and vocabulary

### 5b. Instructional Design Principles Applied
1. **Advance organisers**: Open each section with a brief statement connecting new content to what the learner already knows
2. **Worked examples**: Provide at least one fully worked example per procedural section — show the *thinking*, not just the *doing*
3. **Error anticipation**: For each critical step, include a "Common mistakes" callout identifying the 2–3 most frequent errors and their corrections
4. **Spaced retrieval**: Embed callback references to earlier sections to reinforce retention
5. **Dual coding**: Pair text-based instruction with visual representations (flowcharts, annotated diagrams, comparison tables)

### 5c. Assessment Design
Build assessments that test *performance*, not *recall*:
- **Formative** (per-section): Scenario-based questions requiring application of the concept just taught — "Given [situation], what would you do and why?"
- **Summative** (end-of-module): A realistic task or simulation that requires the learner to integrate multiple objectives — scored against the criterion standards from Step 3b
- **Assessment rubric**: Provide a scoring guide with explicit descriptors for each performance level (Exceeds / Meets / Approaching / Does Not Meet)

## Step 6: Deliver Output

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


Produce the following structured deliverables, formatted for the user's specified platform:

### Deliverable 1: Training Content Document
Complete, publish-ready training content including:
- Title page with module metadata (version, author, date, target audience, estimated completion time)
- Table of contents with section durations
- All sections with instruction, examples, visuals specifications, and knowledge checks
- Quick reference card (one-page job aid summarising key procedures and decision criteria)
- Glossary of terms (if applicable)

### Deliverable 2: Facilitator Guide (if workshop/live training)
- Session-by-session run sheet with timing, facilitator actions, and participant activities
- Discussion facilitation prompts with expected response themes
- Troubleshooting notes for common facilitation challenges
- Materials checklist and room/platform setup requirements

### Deliverable 3: Assessment Package
- All formative and summative assessments with answer keys
- Scoring rubric with performance level descriptors
- Recommended passing threshold with rationale
- Remediation pathway for learners who do not meet standard

### Deliverable 4: Implementation Memo
A one-page briefing document for the stakeholder/manager containing:
- Training purpose and scope
- Target learner profile
- Recommended delivery schedule (sequencing, spacing, reinforcement touchpoints)
- Success metrics and measurement approach
- Dependencies and prerequisites for rollout

## Step 7: Propose Experiments

> **Session summary must be fact-dense:** include the user's stated preferences,
> personal context (company, ICA, industry), what was delivered, any corrections
> given, and end with **"Next session defaults: [3-5 things to pre-fill on next
> connect()]"** so returning users get immediate personalisation.
>
> **Outcomes array:** one concrete fact per item (format, tone, ICA, length,
> constraints). Each outcome should be extractable as a standalone user preference.


```
FutureProof:save_experiment(skill="training-content-creator", experiment={
  hypothesis: "Replacing text-heavy procedural sections with annotated screenshot sequences reduces time-to-competency for new hires",
  variants: ["control: current text-based SOP format", "variant: annotated visual walkthrough with minimal text"],
  measurement: "Time from training completion to first unassisted task execution, error rate in first 10 task completions",
  expected_impact: "25% reduction in time-to-competency, 30% reduction in first-month error rate"
})
```

```
FutureProof:save_experiment(skill="training-content-creator", experiment={
  hypothesis: "Adding scenario-based pre-assessment before training improves learner engagement and completion rates by activating prior knowledge and creating productive struggle",
  variants: ["control: training begins with content delivery", "variant: training opens with a diagnostic scenario the learner attempts before instruction"],
  measurement: "Module completion rate, post-training assessment scores, learner satisfaction rating",
  expected_impact: "15% improvement in completion rate, 10% improvement in assessment scores"
})
```

## Step 8: Request Research

```
FutureProof:request_research(skill="training-content-creator",
  query="Evidence-based microlearning design patterns for operational training — optimal content chunk duration, spaced repetition intervals, and multimedia formats with highest retention rates 2024",
  reason="Ensure training content structure aligns with current cognitive science and adult learning research to maximise knowledge retention and transfer to on-the-job performance"
)
```

```
FutureProof:request_research(skill="training-content-creator",
  query="LMS and knowledge base platform capabilities comparison — Notion, Trainual, Lessonly, Google Docs — for structured training content delivery with assessment and progress tracking",
  reason="Recommend optimal delivery platform based on user's team size, content complexity, and existing tool stack"
)
```

## Step 9: Save Session

```
FutureProof:save_session(skill="training-content-creator", session={
  summary: "...[fact-dense: ICA, format, tone, constraints, what was delivered, amends made. End with: Next session defaults: ...]",
  outcomes: [
    "Format: [format chosen]",
    "Tone: [tone and constraints]",
    "ICA: [ICA description]",
    "Deliverable: [what was produced]"
  ],
  metadata: {}
})
```