---
name: setup-senior-dev-squad
description: "Interactive onboarding wizard that captures project conventions and writes them into CONTEXT.md so every squad skill adapts to your project. Use when starting a new project or onboarding the squad to an existing one."
---

# Setup Senior Dev Squad

## Overview

Configure the senior-dev-squad skill suite for your specific project in under five minutes. This wizard asks a handful of precise questions about your workflow, then writes a `## Squad Config` block into your project's `CONTEXT.md`. Every downstream skill — grill, triage, spec-first-development, task-breaker, issue-triage-bot — reads that block to adapt its output to your project rather than a generic template.

Skip this step and each skill falls back to reasonable defaults. Complete it and every skill speaks your project's language: the right issue tracker, the right label taxonomy, the right paths for ADRs and specs.

**Core principle:** One configuration pass, every skill in sync.

## The Iron Law

```
NEVER GUESS PROJECT CONVENTIONS — ASK ONCE, WRITE ONCE, REUSE EVERYWHERE
```

## When to Use

**Use this when:**
- Starting a greenfield project and connecting the squad for the first time
- Onboarding the squad to an existing codebase that has no `CONTEXT.md` yet
- Your team changes its issue tracker, label scheme, or doc structure
- A squad skill is producing output that doesn't match your project's conventions

**Use this ESPECIALLY when:**
- Someone says "just use GitHub" or "we use Linear" — capture it formally so no skill has to ask again
- The team has custom triage labels that don't match any default set
- Docs, ADRs, and specs live in non-standard paths

**Don't skip when:**
- The project seems simple (even a solo side-project has a tracker and a doc folder)
- You think the defaults are fine (explicit config beats implicit assumptions every time)

## Interactive Setup Flow

Work through the questions **one at a time**. Wait for the user's answer before asking the next question. Do not batch multiple questions into a single message.

---

### Step 1 — Issue Tracker

Ask:

> Which issue tracker does this project use?
> Options: **GitHub Issues**, **GitLab Issues**, **Linear**, **Local markdown files** (e.g. `docs/issues/`), or something else — just name it.

Accept any free-text answer. Record it as a lowercase slug: `github`, `gitlab`, `linear`, `markdown`, or a custom string the user provides.

---

### Step 2 — Triage Labels

Ask:

> What labels (or states/categories) does your team use for triage?
> List them comma-separated, e.g.: `bug, feature, chore, p0, p1, p2`
> Press Enter to accept that default set, or type your own list.

Parse the response into an array. If the user presses Enter or types nothing meaningful, use the default: `[bug, feature, chore, p0, p1, p2]`.

---

### Step 3 — Doc Locations

Ask:

> Where should generated docs live? Confirm or change these paths:
> - Project config: `CONTEXT.md`
> - Architecture Decision Records: `docs/adr/`
> - Feature specs: `docs/specs/`
>
> Type new paths separated by commas (in the same order), or press Enter to accept the defaults.

Parse three paths in order. If only some are changed, keep the unchanged ones at their defaults.

---

### Step 4 — Write the Config Block

After collecting all three answers, write (or update) the `## Squad Config` section in the project's `CONTEXT.md`. If the file does not exist, create it with a minimal header first. If `## Squad Config` already exists, replace only that section — do not touch anything else in the file.

The exact format to write:

```md
## Squad Config
- issue-tracker: github
- triage-labels: [bug, feature, chore, p0, p1, p2]
- docs: { context: CONTEXT.md, adr: docs/adr/, specs: docs/specs/ }
```

Substitute the user's actual answers for the example values above. After writing, show the user the final block and confirm:

> Config written to `CONTEXT.md`. All squad skills will now use these settings.
> Run `/setup-senior-dev-squad` again any time to update.

---

### Step 5 — Suggest Next Steps

Based on the answers, recommend the most relevant next skill to run:

- If the project has no spec yet → **spec-first-development**
- If there are open issues that need sorting → **issue-triage-bot**
- If scope is unclear → **grill**
- Otherwise → **task-breaker** to break the first feature into tasks

## Red Flags — STOP and Follow Process

If you catch yourself:
- Filling in config values without asking the user ("I'll assume GitHub")
- Writing to any file other than the path the user confirmed for `CONTEXT.md`
- Asking two or more questions in the same message (breaks the one-at-a-time rule)
- Skipping Step 4 because "the user will remember" — configuration must be persisted
- Modifying existing `CONTEXT.md` content outside the `## Squad Config` block

**All of these mean: STOP. Return to the relevant step.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "The team obviously uses GitHub, no need to ask" | Projects switch trackers. Ask explicitly so the config is always current. |
| "I'll remember the labels from earlier in the conversation" | Memory doesn't persist across sessions. Written config does. |
| "CONTEXT.md doesn't exist yet, so I'll skip writing" | Create the file. An absent config is not a reason to skip capturing it. |
| "The defaults are fine, let's move on" | Defaults that are wrong waste time on every downstream skill invocation. |
| "I'll ask all three questions at once to save time" | One question at a time ensures accurate answers; batching produces rushed, incomplete responses. |

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Wait, that's not our tracker" — You assumed a value instead of asking
- "Why is it using those labels?" — You skipped Step 2 or wrote the defaults without confirming
- "Where did that spec end up?" — The doc path was never captured or was captured incorrectly
- "Can you re-run setup?" — The previous run didn't persist the config properly

**When you see these:** STOP. Return to Step 1, ask all questions again, and rewrite the config block from scratch.

## Related Skills

- **grill** — interrogates implementation plans using the conventions captured in `## Squad Config`
- **grill** — run before setup when the codebase is unfamiliar and scope is unclear
- **spec-first-development** — the recommended next step after setup on a new feature
- **task-breaker** — breaks an approved spec into atomic tasks, respecting the issue tracker set in config
- **issue-triage-bot** — applies the triage labels configured in Step 2 to incoming issues automatically

## Verification

- [ ] All three questions were asked one at a time (tracker, labels, doc paths)
- [ ] User confirmed or changed each answer before the next question was asked
- [ ] `## Squad Config` block is present in `CONTEXT.md` with no placeholder values
- [ ] Only the `## Squad Config` section was modified if `CONTEXT.md` already existed
- [ ] Config block uses the exact format shown in Step 4 (keys, brackets, braces)
- [ ] User was shown the written config and acknowledged it
- [ ] A next-step skill was recommended based on the project's current state
