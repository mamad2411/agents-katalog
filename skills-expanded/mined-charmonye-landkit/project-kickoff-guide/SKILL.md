---
name: project-kickoff-guide
description: Primary local starter skill for a copied landscape project folder. Use when a designer starts a new project, asks what to do next, provides photos/measurements/client wishes, or needs guided onboarding through briefing, BDD-style site scenarios, and SDD-style spatial decisions.
---

# Project Kickoff Guide

## Goal

Guide the designer from "we have a client, photos, measurements, or first context" to a manageable project: project card, brief, site use scenarios, constraints, concept branches, and the next verifiable step.

## When To Use

- A new project folder is created from `template`.
- The designer has just opened the project and asks where to start.
- It is unclear what is missing before AI generation.
- The designer describes the site in voice/text and the agent must structure the work.
- The project is stuck between photos, measurements, wishes, and concepts.

## Process

1. Read `START_HERE.md`, `FLOW.md`, `PROJECT_INDEX.md`, `99_project_logs/HANDOFF.md`, `99_project_logs/WORK_LOG.md`, `00_project_admin/PROJECT_CARD.md`, `03_client_context/BRIEF.md`, and `03_client_context/SITE_ANALYSIS.md`.
2. Inspect project structure: which folders contain files, what is empty, whether raw photos, measurements, questionnaire, and references exist.
3. Formulate a short project brief: client, site, agreed service scope, main goal, constraints.
4. Create 3-7 BDD-style site scenarios in the format "When..., the client should..., so that...".
5. Create an SDD sketch: zones, routes, privacy, water/slope, materials, planting, phasing, AI artifacts.
6. Find gaps: missing photos, measurements, client answers, or decisions.
7. Update relevant Markdown files if the user provided data.
8. Suggest the next minimum step. If data is insufficient, ask no more than 3 questions.

## Starter Questions

Do not ask all questions at once. Choose 1-3 most important for the situation:

- What is the project/site name and site area?
- What service scope did the studio agree to prepare for this client?
- What files already exist: photos, video, measured plan, questionnaire, references?
- What does the client definitely want on the site?
- What must not change: house, trees, entry, structures, utilities?
- Is there a budget reference and will implementation happen in stages?

## Autofill Rules

When the user gives free-form data, distribute it into files:

- contacts, agreed scope, deadlines -> `00_project_admin/PROJECT_CARD.md`;
- family, scenarios, wishes -> `03_client_context/BRIEF.md`;
- sun, soil, water, neighbors, utilities -> `03_client_context/SITE_ANALYSIS.md`;
- stage status -> `PROJECT_INDEX.md`;
- short current context -> `99_project_logs/HANDOFF.md`;
- work progress and gaps -> `99_project_logs/WORK_LOG.md`.

Do not overwrite already filled fields without a reason. If new input conflicts with old data, record the conflict and clarify.

## BDD/SDD Adaptation

BDD describes external garden behavior: how people enter, rest, host guests, care for the site, view the garden from the house, and use sauna/grill/parking.

SDD describes the design solution: how layout, surfaces, planting, engineering, and visualizations support those scenarios.

## Output

- Short brief.
- BDD scenarios.
- SDD sketch.
- Missing data list.
- One next step.
- Updated starter files if new data was provided.
