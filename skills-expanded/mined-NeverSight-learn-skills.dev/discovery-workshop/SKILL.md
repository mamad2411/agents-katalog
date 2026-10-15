---
name: discovery-workshop
description: Guide synthesis of Action Mapping workshop outputs into structured discovery documents. Use when processing workshop notes, creating needs analysis, building learner personas, summarizing discovery sessions, or preparing design briefs from stakeholder meetings.
allowed-tools: Read, Write, Edit, Grep, Glob, AskUserQuestion
model: claude-opus-4-5-20251101
user-invocable: true
---

# Discovery Workshop Synthesis

Transform your Action Mapping workshop outputs into all four key discovery documents through a guided interview process.

## What This Skill Does

After you've facilitated a discovery workshop with stakeholders and SMEs, this skill helps you:

1. **Synthesize** raw workshop notes into structured insights
2. **Generate** four key deliverables:
   - Meeting Summary
   - Formal Needs Analysis
   - Action Map Summary
   - Design Brief
3. **Create** Learner Persona(s)
4. **Ensure** all documents align with your adapted Action Mapping methodology

## Your Adapted Action Mapping Process

This skill follows your team's adapted methodology:

```
1. Content Audit → Review existing training/content BEFORE stakeholder sessions
2. Business Goal → Define measurable business outcome with stakeholders
3. Behaviors + Obstacles → Map both what people should do AND why they're not doing it
4. Practice Activities → Design realistic scenarios for behavior change
5. Knowledge Pull → Identify what info learners need during activities
```

For detailed methodology reference, see [adapted-action-mapping.md](adapted-action-mapping.md)

---

## How to Use This Skill

### Option 1: Full Guided Process
Say: "Help me process my discovery workshop outputs" or invoke `/discovery-workshop`

I will interview you through each phase:
1. Content audit findings
2. Business goal identification
3. Behaviors and obstacles mapping
4. Target audience insights
5. Document generation

### Option 2: Specific Document
If you only need one output:
- "Create a needs analysis from my workshop notes"
- "Generate a design brief for this project"
- "Build a learner persona for [audience]"
- "Summarize my workshop into a meeting summary"

### Option 3: Process Raw Notes
Paste your workshop notes and say: "Synthesize these into discovery documents"

---

## Interview Process

I'll guide you through these questions:

### Phase 1: Content Audit
- What existing training or content did you review before the workshop?
- What were the key findings? (What's good? What's outdated? What's missing?)
- Is any existing content reusable?

### Phase 2: Business Goal
- What business problem are we trying to solve?
- How is this problem currently measured?
- What does success look like? What metrics will change?
- Who requested this training and why now?

### Phase 3: Behaviors + Obstacles
- What specific actions should people be doing on the job?
- Which behaviors have the highest impact on the business goal?
- Why aren't people performing these behaviors now?
  - Knowledge gaps?
  - Skill gaps?
  - Environmental barriers?
  - Motivation issues?

### Phase 4: Target Audience
- Who exactly needs this training?
- What do they already know?
- What's their attitude toward this training?
- What constraints do they have (time, technology, environment)?

### Phase 5: Constraints & Context
- What's the timeline?
- What technology/platform will be used?
- Are there compliance or accessibility requirements?
- Who are the key stakeholders?

---

## Output Documents

### 1. Meeting Summary
Quick reference document capturing:
- Key decisions made
- Action items with owners
- Open questions
- Notable quotes and insights

**Template:** [meeting-summary-template.md](meeting-summary-template.md)

### 2. Formal Needs Analysis
Comprehensive discovery document including:
- Business goal and success metrics
- Current vs. desired state gap analysis
- Target audience profile
- Key behaviors and obstacles
- Content requirements
- Constraints and considerations
- Recommended solution

**Template:** [needs-analysis-template.md](needs-analysis-template.md)

### 3. Action Map Summary
Text representation of your action map:
- Business goal at center
- Priority behaviors listed
- Obstacles mapped to each behavior
- Practice activity ideas

**Template:** [action-map-template.md](action-map-template.md)

### 4. Design Brief
Concise document for handoff to design phase:
- One-sentence project summary
- Business goal
- Target audience summary
- Key behaviors to address
- Proposed solution overview
- Success metrics
- Constraints

**Template:** [design-brief-template.md](design-brief-template.md)

### 5. Learner Persona(s)
Detailed fictional profiles:
- Demographics and background
- Goals and motivations
- Challenges and pain points
- Learning preferences
- Technology profile
- Design implications

**Template:** [learner-persona-template.md](learner-persona-template.md)

---

## Tips for Better Discovery

### Before the Workshop
- Review existing content/training first
- Prepare a clear agenda
- Identify who needs to be in the room

### During the Workshop
- Focus on behaviors, not content
- Capture specific examples and quotes
- Challenge assumptions ("How do you know that?")
- Note disagreements—they reveal important tensions

### After the Workshop
- Process notes within 24-48 hours while fresh
- Send meeting summary for validation
- Flag open questions that need follow-up

---

## Examples

See [examples/sample-discovery-outputs.md](examples/sample-discovery-outputs.md) for sample outputs from a completed discovery process.

---

## Related Commands

- `/objectives` - Generate learning objectives from behaviors
- `/synthesize-notes` - Quick note synthesis without full workflow
- `/learner-persona` - Generate a single persona quickly
- `/bloom-verbs` - Reference for objective writing

---

## Getting Started

Ready to process your workshop? Tell me:

1. **What project is this for?** (client/project name)
2. **Do you have raw notes to share?** (paste them or reference a file)
3. **Which outputs do you need?** (all four, or specific documents)

Or just paste your workshop notes and I'll guide you through the process.
