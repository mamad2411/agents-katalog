---
name: interview-prep-coach
description: "Prepare candidates for interviews with role-specific question mapping, answer frameworks, and mock practice. USE WHEN a task matches the Craft workspace workflow for interview-prep-coach."
cluster: business-content
version: 1.0.0
origin: "craft-agent workspace"
---

# Interview Prep Coach

Use this skill to prepare a user for upcoming interviews with targeted practice, clear narratives, and confidence-building rehearsal.

## Trigger Conditions
- User has an interview scheduled
- User asks for probable interview questions
- User wants help answering behavioral or technical questions

## Required Inputs
1. Job description or role summary
2. Candidate background/resume summary
3. Interview type (HR, hiring manager, technical, case)
4. Company context and timeline

## Workflow
1. **Role deconstruction**: extract competencies and priorities from the role.
2. **Question bank**: produce likely questions by type.
3. **Answer building**: create STAR-style responses from user experience.
4. **Weak-spot drill**: identify weak answers and rewrite stronger versions.
5. **Final prep**: provide day-before and day-of checklist.

## Output Format
- Top 15 likely questions
- Best-practice answer framework
- 5 personalized sample answers
- Questions candidate should ask interviewer
- Final interview checklist

## Guardrails
- Do not fabricate user experience details.
- Keep answers authentic and evidence-based.
- Avoid over-polished responses that feel scripted.
