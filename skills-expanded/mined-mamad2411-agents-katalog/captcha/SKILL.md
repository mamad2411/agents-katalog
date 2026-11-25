---
name: captcha
description: Save repository-specific "do-not-repeat" rules when the user says things like "캡차에 저장해놔", "captcha 저장", "다음부터 이건 하지 않게 기록해", "save this to captcha", "remember this rule", "don't do this again", or "add this to the repo captcha". Also use this skill before planning, editing, or verifying work whenever the target repository already contains `captcha/CAPTCHA.md`.
---

# Captcha

## Purpose

Use `captcha` to maintain a repository-specific rulebook of things the agent should not repeat.

These are not long notes, general preferences, or postmortems. Store only reusable rules that should change future behavior in the current repository.

## Use This Skill When

Use `captcha` in either of these situations:

1. The user asks to save a mistake, exclusion, or "don't do this again" rule.
2. The target repository already contains `captcha/CAPTCHA.md` and you are about to plan, edit, or verify work.

Common trigger phrases include:

- `캡차에 저장해놔`
- `captcha 저장`
- `다음부터 이건 하지 않게 기록해`
- `save this to captcha`
- `remember this rule`
- `don't do this again`
- `add this to the repo captcha`

## Core Guardrails

- Keep all repository rules in one file only: `captcha/CAPTCHA.md`
- Never split categories into multiple Markdown files
- Categorize automatically; do not make the user manage categories
- Prefer merging into an existing rule over creating a near-duplicate
- Rewrite feedback into reusable `avoid` / `do` rules
- If the meaning is unclear, ask a short multiple-choice question
- The final multiple-choice option must always allow free-form input

## Read Before Work

Before planning or editing:

1. Check whether `captcha/CAPTCHA.md` exists in the target repository.
2. Always read the `Global` section.
3. Use the `Category Index` in `captcha/CAPTCHA.md` to choose task-relevant categories.
4. Read only the matched sections before continuing.
5. If the task expands into a new area, read more sections before proceeding.
6. For broad refactors, migrations, or cross-cutting tasks, read the whole file.

If `captcha/CAPTCHA.md` does not exist, continue normally unless the user explicitly asks you to save a rule.

## Save Workflow

When the user asks to save something:

1. Inspect the recent work context.
2. Identify the action or mistake the user wants excluded in future work.
3. Rewrite it into a future-facing rule with:
   - `avoid`: what not to do
   - `do`: what to do instead
4. Choose the best category automatically.
5. If `captcha/CAPTCHA.md` does not exist:
   - create `captcha/`
   - initialize `captcha/CAPTCHA.md` using `assets/CAPTCHA.template.md`
6. Search for an existing rule with the same meaning.
7. If a matching rule exists, merge into it.
8. Otherwise append a new rule to the selected category.
9. Update metadata fields and optional examples.

## What To Save

Save only rules with clear future value:

- repeatable mistakes
- scope-control rules
- validation rules
- risky actions that should be avoided
- repository-specific exclusions that should change later work

Do not save:

- one-off preferences with no future value
- vague frustration without an actionable rule
- items that cannot be tied to recent work context
- temporary directions that should not become repository policy

If the user's feedback is too vague or too temporary, explain briefly why you did not store it.

## Category Selection

Choose the category from the task itself, not from user bookkeeping.

- `Global`: repository-wide restrictions; always read
- `Requirements-Scope`: "only", "just", partial edits, "don't touch"
- `Implementation`: bugfixes, features, refactors, logic, structure, performance
- `UI-UX`: layout, style, copy, spacing, components, interactions
- `Data-API`: schema, migrations, queries, contracts, response shapes
- `Testing-Verification`: tests, validation, repro, completion claims
- `Dependencies-Env`: installs, package versions, config, env changes
- `Git-Workspace`: revert, delete, branch, commit, workspace hygiene
- `Deployment-Infra`: deploy, release, production, infrastructure, operations
- `Security-Secrets`: credentials, tokens, auth, privacy, sensitive data
- `Docs-Automation`: docs, scripts, automations, generated artifacts

If the best category is unclear, default to:

- `Global` plus `Requirements-Scope` plus `Implementation` for reading
- `Requirements-Scope` or `Implementation` for saving, whichever is narrower

## Ambiguity Handling

If you cannot clearly tell what the user wants excluded, ask a short multiple-choice question based on the recent work context.

Rules for the question:

- Offer 2-4 concrete choices.
- Put the best guess first.
- Make the final option a free-form answer.
- Keep each option short enough that the user can reply with a number.

Template:

```text
어떤 규칙으로 저장할까요?

1. [best guess]
2. [second guess]
3. [third guess, if needed]
4. 직접 적을게
```

If the user chooses the free-form option, convert their answer into a reusable rule. If the answer still cannot be generalized into a rule, explain why you did not save it.

## Duplicate Handling

Prefer merge over duplication.

Merge when:

- the rule belongs in the same category
- the core `avoid` meaning is the same
- the future prevention value is effectively identical

When merging:

- keep the existing rule ID
- improve wording if clarity gets better
- update `updated`
- append new examples only if they add value

Create a new rule only when merging would make the existing rule too broad or inaccurate.

## File Format

Follow `references/captcha-format.md` for the exact `captcha/CAPTCHA.md` structure.

If you need to initialize a new file, use `assets/CAPTCHA.template.md` as the starting structure.
