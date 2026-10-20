---
name: prd-creator
description: Creates a Product Requirements Document (PRD) for a new feature based on user input. The PRD is a detailed document that guides junior builders on what to build and why. The agent will ask questions to gather necessary information before generating the PRD.
---

# Rule: Make Big Paper For Feature

## Goal

Big Paper called PRD. PRD tell junior builder what to build and why. PRD must be clear. Junior builder must understand easily and detailed.

## Process

1. **Get First Words:** User give short idea. Idea about new thing to build.
2. **Ask Questions:** AI not write yet. AI ask questions first. AI need to know _what_ and _why_. Not _how_. Builder figure out _how_ later.
3. **Make PRD:** User answer questions. AI take answers. AI make big paper using structure below.
4. **Save Paper:** AI save paper. Paper go in `/tasks` folder. Name paper `prd-[feature-name].md`.

## How To Ask Questions

AI must use numbered list. List can have small questions under big questions. Use dot marks like this: 1, 2, 2.1, 2.2, 3.

Example:

1. Big question one?
2. Big question two?
   2.1. Small question under two?
   2.2. Another small question under two?
3. Big question three?

Only one question per line. No mixing.

AI change real questions based on what user say. AI try to learn about:

- **Problem/Goal:** What pain does feature fix? What is main goal?
- **Target User:** Who use this feature?
- **Core Work:** What must user be able to do?
- **User Stories:** Give example like "As [user] want [action] so that [good thing happen]"?
- **Done Means Done:** How know feature work good?
- **Walls:** What feature must NOT do?
- **Data:** What information show or saved?
- **Look and Feel:** Any pictures of design? Any style rules?
- **Bad Things:** What if something go wrong? What strange situations can happen?

## PRD Structure

Big paper must have these parts:

1. **What Is This:** Short say what feature is. What problem it fix. What goal is.
2. **Goals:** List what feature must achieve. Must be clear. Must be able to measure.
3. **User Stories:** Tell stories of user using feature. Show benefit.
4. **Must Do List:** List all things feature must do. Say clearly. Use words like "System must let user do X." Give each one a number.
5. **Not Doing List:** Say what feature will NOT do. Keep work small and focused.
6. **How It Look (If Know):** Link to pictures. Say UI rules. Say which parts to use.
7. **Tech Thoughts (If Know):** Say any limits. Say what other parts this touch. Say any known hard things.
8. **How Know Success:** Say how measure if feature work. Example: "Less help tickets" or "More users do X."
9. **Still Do Not Know:** List things still not clear. List things need more talk.

## Who Read This

Junior builder read PRD. Words must be simple, clear and not confusing. Give enough detail so builder know what to build and why.

## Output Rules

- **Type:** Markdown file `.md`
- **Where:** Put in `docs/PRDs/` folder
- **Name:** `prd-[good-name-for-feature].md`

## Last Rules

1. Do NOT start building. Only make paper.
2. Must ask questions before making paper.
3. Take answers. Make paper better.
