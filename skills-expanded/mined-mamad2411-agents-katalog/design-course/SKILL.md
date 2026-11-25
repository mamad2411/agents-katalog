---
name: design-course
description: Interview the user to define a course structure, then fan out module cards to the CourseModuleFactory pipeline.
---

# Design Course

Interview the user to define a course structure, then fan out module cards to the CourseModuleFactory pipeline.

## When to Use

When the user wants to create a new course. This skill runs BEFORE the pipeline — it produces the module cards that the pipeline processes.

## Configuration

**Project path:** Ask the user where the CourseModuleFactory project is located on first use. Default: `/Volumes/Extreme Pro/users/loudalo/GitHub/code experiments/CourseModuleFactory`

## Steps

### 1. Set Project Path

Ask the user to confirm or provide the CourseModuleFactory project path. Verify the path exists and contains `trello_ops.py`.

### 2. Interview

Conduct a structured conversation. Ask these questions ONE AT A TIME (do not dump all questions at once). Wait for each answer before asking the next:

1. **Who is this course for?**
   Ask for a specific learner persona within the knowledge entrepreneur audience.
   Good: "Coaches transitioning from 1:1 to group programs"
   Bad: "Business owners" (too vague — push back)

2. **What transformation does the course deliver?**
   What can the learner DO after completing the course that they can't do now?
   Must be concrete and demonstrable, not just "understand" something.

3. **What's the learner's current state?**
   What do they already know? What have they tried? What's blocking them?

4. **What's the course title?**
   Working title is fine. Can be refined later.

5. **How many modules?**
   Rough count, or say "propose based on scope" and you'll suggest a number.
   Typical range: 4-8 modules for a focused course.

6. **Any must-include topics?**
   Specific concepts, tools, frameworks, or methods they want covered.

7. **Any explicit exclusions?**
   What this course is NOT. Topics to avoid, approaches to skip.

### 3. Propose Module List

Based on the interview, propose a complete module list. For each module, provide:

```
Module {N}: {Topic}
Learning Goal: {SMART goal — specific, measurable, achievable in 20-45 min}
Type: Foundation | Practice | Deep Dive
```

### 4. SMART Goal Validation

Before presenting the module list, validate each learning goal:

- **Specific:** Not "understand pricing" but "Choose between three pricing models based on your business stage"
- **Measurable:** The learner can demonstrate the outcome
- **Achievable:** Within one module (~20-45 min)
- **Relevant:** Directly serves the course transformation from step 2
- **Time-bound:** Implicitly bounded by module duration

If a goal is vague, rewrite it to be SMART before including it in the proposal.

### 5. User Approval

Present the full module list and ask the user to:
- Approve as-is
- Add modules
- Remove modules
- Reorder modules
- Revise any learning goals

Iterate until the user approves.

### 6. Generate Course Brief

Save a Course Brief to `{project_path}/artifacts/{course_id}/course_brief.md`:

```markdown
# Course Brief

**Course ID:** {course_id}
**Title:** {course_name}
**Created:** {date}

## Target Learner
{from interview Q1 + Q3}

## Course Transformation
{from interview Q2}

## Modules

| # | Topic | Learning Goal | Type |
|---|-------|---------------|------|
| 1 | ... | ... | Foundation |
| 2 | ... | ... | Practice |
| ... | ... | ... | ... |

## Exclusions
{from interview Q7}

## Design Notes
{any relevant context from the interview}
```

### 7. Create Trello Cards

Execute these commands from the project directory:

**a) Create course reference card:**
```bash
python3 trello_ops.py create Courses "COURSE: {course_name}" "{course_brief_content}"
python3 trello_ops.py update_metadata {course_card_id} '{"id": "{course_id}", "type": "course", "status": "reference"}'
python3 trello_ops.py attach {course_card_id} artifacts/{course_id}/course_brief.md
```

**b) Submit each module card:**
```bash
python3 trello_ops.py submit "{topic}" "{learning_goal}" --course-id {course_id} --course-name "{course_name}" --module-num {N}
```

Run all submit commands and collect the card IDs.

### 8. Confirm

Show the user:
- Course Brief file path
- Trello board URL (from `python3 trello_ops.py status`)
- Number of module cards created
- Instruction: "Run the orchestrator loop to start processing modules"

## Course ID

Generated as `course-{timestamp}` where timestamp is `int(time.time())`.

## Important Rules

- Ask interview questions ONE AT A TIME
- Push back on vague learner personas and learning goals
- Never propose more than 8 modules without user agreement
- Each module must be completable in 20-45 minutes
- Module topics should NOT overlap — each covers distinct ground
- The first module should be Foundation type (establishes baseline)
- The last module should be Practice or Deep Dive (applies everything)
