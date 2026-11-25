---
name: help
description: Guide to career-agent skills and workflows. Lists available skills, explains how a specific skill works on request, and walks through common multi-skill workflows (new application, interview prep, etc.). Conversational, read-only. Use when the user says "/help", "what can you do", "how does X work", "what skill do I need for Y", "I'm new here".
---

# Help

## When to use
Whenever the user wants to know what's available or how to do something. Trigger phrases: "/help", "what can you do", "how does <skill> work", "what skill do I use for <goal>", "I'm new here", "remind me how X works".

For first-time setup of a fresh clone, use `onboard` instead. `/help` assumes the user already has $PERSONAL bootstrapped.

## What it produces
A conversational response. **Read-only**: no files written, no state changed.

## Workflow

`/help` is conversational. Always start with the directory, then ask what they want to dig into. Don't dump everything at once.

### Step 1: Print the directory

Always lead with this compact table:

```
career-agent skills:

  /onboard            First-time setup. Bootstraps $PERSONAL and interviews you for the four core docs.
  /help               This. Directory + skill explainer + workflow walk-throughs.
  /morning            AM briefing on yesterday's open items and one suggested first move.
  /job-analyzer       Paste a Job Description, get a grounded fit analysis. Persists to applications/<company>/<role>/role.md.
  /resume-builder     Tailored resume in Markdown, .docx, .pdf.
  /cover-letter-builder  Tailored cover letter in .md and .docx.
  /star-stories       Convert your projects into STAR-format files for behavioral interviews.
  /interview-prep     Behavioral coverage audit, mock interviews, company briefs, round cheat-sheets.
  /coding-prep        Coding interview practice. Tutoring, evaluation, or timed mock.
  /daily-summary      EOD log of what you did, open loops, next steps.
```

Keep the descriptions terse. Detail comes in Step 2.

### Step 2: Offer the three follow-ups

After the directory, ask:

> Want me to explain one of these in detail, walk through a common workflow, or recommend a skill for something specific?

Then branch based on the response.

### Branch A: Explain a specific skill

When the user names a skill (or says something like "how does resume-builder work"):

Read the skill's own `SKILL.md` from `.claude/skills/<name>/SKILL.md`. Summarize:

1. **What it does** (1 to 2 lines).
2. **When to use it** (the trigger phrases).
3. **Inputs** (what the user provides, what the skill reads from $PERSONAL).
4. **Outputs** (files written, where they land).
5. **Dependencies** (which $PERSONAL docs need to be filled for this skill to work well; which other skills feed into or out of it).
6. **One usage example** (a realistic trigger phrase or short scenario).

Keep it tight, under ~15 lines for any single skill. Don't paste the full SKILL.md back.

End with: *"Want to try it now, or have questions about another?"*

### Branch B: Walk through a common workflow

When the user asks "how do I X" or picks a workflow, walk them through it. Use one of the recipes below as a starting point and adapt to their specifics.

#### Recipe: New application end-to-end
For a new Job Description from a company they want to pursue.
1. `/job-analyzer` with the Job Description text or URL. Lands at `$PERSONAL/applications/<company>/<role>/role.md` with fit analysis.
2. If the fit verdict is "pursue", run `/resume-builder` for that role. Output: `resume.md`, `.docx`, `.pdf` in the same folder.
3. `/cover-letter-builder` for the same role.
4. Apply through the company's portal. Mention "applied today" in chat so the role.md gets a `date_applied` field updated.

#### Recipe: Interview prep, full ramp
From "got an onsite" to "ready to walk in".
1. `/interview-prep` company brief mode: *"Research <company> before <date>"*. Lands at `applications/<company>/<role>/brief.md`.
2. `/interview-prep` coverage audit: *"Where are my story gaps for this round?"*. Tells you which behavioral competencies are thin.
3. If gaps point at projects you haven't STARified yet, run `/star-stories <project>` for each. Lands at `$PERSONAL/career/star/<slug>.md`.
4. `/interview-prep` cheat-sheet mode for each round: *"Build a cheat-sheet for the <round> at <company>"*.
5. `/interview-prep` mock mode the day before: *"Mock me on a <round>-style interview"*.
6. For coding rounds, `/coding-prep` mock: *"Mock me on a medium graph problem, 45 min"*.

#### Recipe: Brand-new repo
First session after cloning.
1. `/onboard`. Bootstraps $PERSONAL, runs the four-doc interview.
2. `/help` (this skill). Pick a first skill to try based on what's on your plate.
3. Try `/job-analyzer` with a real Job Description. The whole flow becomes obvious from there.

#### Recipe: Idle / what should I do
When the user has time and doesn't know where to start.
1. `/morning`. Surfaces yesterday's open items and one suggested move.
2. If nothing pending, `/morning` falls back to suggesting a fresh job analysis grounded in `goals.md`.

When walking through a recipe, list the steps tersely (like above). After listing, ask: *"Want to start at step 1 now?"*

### Branch C: Recommend a skill from a goal

When the user describes a goal ("I have a Pinecone HM call Friday"), pick the best-fit skill(s) and order. Use the recipes above as templates.

If the goal maps to multiple skills, list them in order with a one-line reason for each. If it maps to one, just say so and offer to start.

## Behaviors and edge cases

- **Read SKILL.md files at runtime, don't memorize.** Skill descriptions change. When the user asks about a specific skill, open its `SKILL.md` and summarize from the live file. The directory table above is a stable index but individual skill behavior is the source file.
- **If a skill the user names doesn't exist**, say so and suggest the closest match from the directory. Don't invent skills.
- **If the user asks about a workflow that isn't in the recipes above**, build a recipe on the fly from the skill descriptions. Don't refuse just because there's no canned answer.
- **CLAUDE.md is the authoritative project doc.** If a question is about project layout, file locations, or the $PERSONAL convention rather than a skill, point at CLAUDE.md sections rather than reproducing them.

## Anti-patterns

- **Don't dump the full directory plus every skill detail in one response.** The user can't scan that. Lead with the table, then let them pick.
- **Don't run skills inside /help.** Help is read-only and conversational. The user invokes the recommended skill themselves.
- **Don't list every possible workflow.** The recipes above cover the common cases. Build novel ones on demand.
- **Don't recite SKILL.md verbatim.** Summarize. The user came to `/help` because the full SKILL.md is too much.
- **Don't include skills that aren't actually installed.** If `.claude/skills/<name>/` doesn't exist, drop it from the directory. The table above is the canonical list **only** if it matches `ls .claude/skills/` — verify before printing if unsure.
- **Don't pad.** No "great question", no "happy to help". Just the directory and the follow-up question.
