---
name: readme-review
description: Use when a user asks to review a README for setup clarity, usage examples, scope boundaries, and contributor readiness.
---

# README Review

## Description

Review README drafts for practical developer onboarding quality.

## When To Use This Skill

Use this skill when a user provides a README draft and wants clear, actionable documentation feedback.

## When Not To Use This Skill

Do not use this skill for general code review, product strategy, or marketing copywriting.

## Required Inputs

- Path to the README file.
- Intended audience for the project.
- Current setup, test, lint, and run commands if known.

## Workflow Steps

1. Read the README from top to bottom.
2. Check project positioning, install steps, quickstart, command examples, and scope boundaries.
3. Identify unclear or missing sections.
4. Produce prioritized fixes with concrete wording suggestions.

## Output Format

A concise Markdown report with PASS/WARN/FAIL findings and suggested README edits.

## Quality Bar

Feedback should be specific, repo-aware, and focused on helping a developer start using the project quickly.

## Failure Handling

If the README path is missing or the project goal is unclear, report the blocker and ask for the minimum missing context.
