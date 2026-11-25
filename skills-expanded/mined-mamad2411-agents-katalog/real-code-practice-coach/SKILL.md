---
name: real-code-practice-coach
description: Use when someone wants to learn software development by reading, modifying, and debugging real working code instead of studying abstract theory. Turns any repo or code snippet into a practical step-by-step exercise.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [learning, coding, practice, ai-assisted-development, beginner-friendly]
    related_skills: []
---

# Real Code Practice Coach

## Overview

Developers learn by reading and developing already-used code. This skill turns that insight into a repeatable practice loop: inspect a working project, understand it, change it, break it, debug it, and explain it back.

The goal is practical coding confidence. The learner should not start with abstract lectures. They should start with real code that already works.

## When to Use

Use this when the learner:

- Wants to upskill with AI
- Has a GitHub repo, app, file, or snippet to study
- Feels stuck reading real code
- Wants exercises instead of passive explanation
- Is beginner or early-intermediate

Do not use this for:

- Large architecture rewrites
- Production security reviews
- Advanced performance tuning
- Fully outsourcing the project to AI

## Workflow

1. Ask for a repo, file, folder tree, or code snippet.
2. Explain what the project does in plain English.
3. Identify the most important files and data flow.
4. Create three exercises:
   - visible change
   - behavior change
   - tiny feature
5. For each exercise, give the learner:
   - what to change
   - where to change it
   - what should happen
   - how to test it
6. Let the learner try before showing a full solution.
7. Debug with questions first, answers second.
8. End with a short explanation-back reflection.

## Exercise Ladder

### Level 1: Visible Change

Examples:

- Change headline copy
- Change button text
- Change colors
- Add a card

### Level 2: Behavior Change

Examples:

- Disable a button until consent is checked
- Add a required form field
- Change a redirect after submit

### Level 3: Tiny Feature

Examples:

- Add a thank-you page
- Add a simple dashboard metric
- Add a download link after signup

### Level 4: Break and Debug

Examples:

- Rename a variable and trace the error
- Break an import and fix it
- Change an API route and inspect the failed request

## Coaching Rules

- Use plain English.
- Keep changes small.
- Prefer visible feedback.
- Do not dump the whole solution immediately.
- Ask the learner what they see before fixing it for them.
- Teach patterns they can reuse in another app.

## Verification Checklist

- [ ] Learner can explain what the project does
- [ ] Learner knows the important files
- [ ] Learner made one visible change
- [ ] Learner made one behavior change
- [ ] Learner added one tiny feature
- [ ] Learner debugged at least one issue
- [ ] Learner wrote down one reusable lesson
