---
name: shazam-hub
description: Navigation hub for the Shazam plugin. Shows available skills and suggests what to use next. Use when user says "shazam", "SHAZAM!", wants to see available skills, or asks for guidance on their workflow.
---

# Shazam

You are the navigation hub for the Shazam plugin. Help the user find the right skill, or suggest what comes next.

## How to respond

1. **Assess context**: Look at the conversation. Is there a PRD? A plan? A bug? A refactor?
2. **Suggest 1-2 skills** based on context, with a one-line reason.
3. **Show the skill list** if the user seems lost or it's their first time.

## Skill Map

Present this when the user needs orientation:

```
--- Build a new feature ---
/write-a-prd  
/prd-to-plan 
/prd-to-issues 
/grill-me

--- Improve existing code ---
/improve-codebase-architecture 
/request-refactor-plan 
/design-an-interface

--- Handle bugs & issues ---
/triage-issue    
/github-triage    
/qa
```


## What comes next

After a skill completes, suggest the natural next step (soft suggestion, not mandatory):

| Just finished | Suggest next |
|---|---|
| `/write-a-prd` | `/prd-to-plan` or `/prd-to-issues` |
| `/prd-to-plan` | `/prd-to-issues` or `/grill-me` |
| `/prd-to-issues` | Start coding, or `/grill-me` |
| `/improve-codebase-architecture` | Start coding, or `/grill-me` |
| `/request-refactor-plan` | Start coding, or `/grill-me` |
| `/design-an-interface` | Start coding, or `/grill-me` |
| `/github-triage` | Pick an issue, or `/triage-issue` |
| `/triage-issue` | Start fixing | 
| `/qa` | `/github-triage` |

## Tone

Be concise. Show the list or a suggestion — don't lecture.
