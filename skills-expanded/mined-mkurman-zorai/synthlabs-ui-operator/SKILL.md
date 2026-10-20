---
name: synthlabs-ui-operator
description: Use when SynthLabs work must be driven through the visual app for verifier review, data preview, settings changes, DEEP mode, or other browser-led workflows.

tags: [synthlabs, synthlabs-ui-operator]
---

# SynthLabs UI Operator

## Overview

Use this skill when SynthLabs is best operated as an application instead of a backend route. Assume `synthlabs-setup` already confirmed a healthy instance before you begin. This skill does not provide dedicated zorai SynthLabs tools; it maps the work onto zorai's existing browser workflow.

## When to Use

Use this skill when:

- the task requires verifier review, manual approval, or row-level inspection,
- the operator needs data preview or visible confirmation of dataset state,
- settings changes or settings inspection must happen in the app,
- DEEP mode is part of the requested workflow,
- or the operator explicitly wants browser-led operation instead of backend automation.

Do not use this skill when:

- the task is session discovery, session creation, or repeatable generation that fits backend routes,
- the task is autoscore, rewrite, remove-items, migrate-reasoning, or job polling,
- or the local SynthLabs instance still needs to be started or repaired.

## Agent Rules

- Use browser tools only after `synthlabs-setup` confirmed SynthLabs is healthy.
- Prefer UI navigation for verifier review, data preview, settings changes, and DEEP mode.
- Follow the browser workflow in `skills/operating/browser.md`: start by opening a browser pane, read the DOM before interacting, use element discovery instead of guessing selectors, prefer text-based clicks when possible, and read the DOM again after navigation.
- Use existing browser tooling such as `open_canvas_browser`, `browser_read_dom`, `browser_get_elements`, `browser_click`, and `browser_type`; do not imply SynthLabs-specific zorai tools exist.
- Do not use the browser just to confirm data or trigger work that stable backend routes already cover.
- Hand session CRUD and repeatable generation work back to `synthlabs-generation`.
- Hand autoscore, rewrite, remove-items, migrate-reasoning, orphan checks, and job polling back to `synthlabs-curation`.

## Browser-Led Workflow

1. Confirm the SynthLabs URL from the operator or from the healthy local instance already validated by `synthlabs-setup`.
2. Open the app in a browser pane and read the page before clicking anything.
3. Discover the relevant controls for the target surface: Verifier, Data Preview, Settings, Generator/Engine, or DEEP mode.
4. Capture the visible state you are reviewing or changing so follow-up work can resume from the correct session or screen.
5. If the task becomes repeatable through `/api/sessions`, `/api/ai/generate`, or `/api/jobs`, stop using the browser and switch to the backend-focused skill that owns that route.

## Owned Visual Surfaces

### Generator And Engine Screens

- inspect visible session configuration,
- review prompt fields and generation options before a run,
- confirm which mode or screen the operator is using,
- and capture any visual state that should be handed back to backend generation work later.

### Verifier Review

- inspect rows,
- compare outputs,
- approve or reject entries,
- and record issues when quality judgment depends on visual review.

### Data Preview

- browse tables,
- inspect row details,
- confirm column meaning,
- and visually validate imported or generated content.

### Settings Changes

- update provider settings,
- inspect DB mode or storage settings,
- adjust visible workflow options,
- and confirm that a settings change took effect in the app.

### DEEP Mode And Other Visual Workflows

- navigate DEEP mode when the operator needs visible state and intermediate steps,
- inspect mode-specific controls or panels,
- and keep visually complex flows in the browser until they can be handed back to a backend-repeatable path.
- capture enough visual state to hand the work back to `synthlabs-generation` or `synthlabs-curation` when the UI-only phase is complete.

## Handoff Rules

- If the task can be expressed as `GET /api/sessions`, `POST /api/sessions`, or `POST /api/ai/generate`, switch to `synthlabs-generation`.
- If the task can be expressed as `GET /api/jobs`, `GET /api/jobs/:id`, or a `/api/jobs/*` curation route, switch to `synthlabs-curation`.
- Stay in this skill only while the UI is the real control surface.

## Common Mistakes

- Opening the browser just to confirm data already exposed by `/api/sessions` or `/api/jobs`.
- Repeating setup instructions here instead of requiring `synthlabs-setup` first.
- Treating DEEP mode as a promised backend route when the task is explicitly visual.
- Blurring the boundary between manual verifier review and repeatable backend generation or curation.