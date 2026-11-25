---
name: skill-creator
description: Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy.
---

# skill creator

Use this skill when the task matches the description above.
Keep the initial response concise and only open bundled references or scripts when they are clearly needed.

## Quick cues

- Decide what you want the skill to do and roughly how it should do it
- Write a draft of the skill
- Create a few test prompts and run claude-with-access-to-the-skill on them
- Help the user evaluate the results both qualitatively and quantitatively
- Use the `eval-viewer/generate_review.py` script to show the user the results for them to look at, and also let them look at the quantitative metrics
- Repeat until you're satisfied
- Expand the test set and try again at larger scale
- "evaluation" and "benchmark" are borderline, but OK

## Available sections

- Skill Creator
- Communicating with the user
- Creating a skill
- Capture Intent
- Interview and Research
- Write the SKILL.md
- Skill Writing Guide
- Report structure
- [Title]
- Executive summary
- Key findings
- Recommendations

## Bundled resources

- agents
- assets
- eval-viewer
- references
- scripts

Open these resources only if the current task needs deeper detail or executable helpers.
