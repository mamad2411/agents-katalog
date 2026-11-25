---
name: playbook
description: Use when the user wants to create, refine, or use a reusable playbook for repeated tasks — a structured prompt template with Procedure, Specifications, Advice, Forbidden Actions, and Required-from-User sections. Replicates Devin cloud's Playbook feature (.devin.md files, macros, team/community library) for the CLI.
triggers: [user, model]
---

# Playbook (CLI replica of Devin cloud Playbooks)

## What this replicates

Cloud Devin has a **Playbook** feature — reusable, shareable prompt
templates for repeated tasks. Playbooks have a structured format
(Procedure, Specifications, Advice, Forbidden Actions, Required from
User), support macros (`!macro-name`), and can be attached as
`.devin.md` files or selected from a team/community library.

The CLI has no playbook system. This skill fills that gap by providing
the playbook format, creation workflow, and a local library structure.

**Sources:**
- docs.devin.ai/product-guides/creating-playbooks (format + writing guide)
- docs.devin.ai/product-guides/using-playbooks (usage + macros)
- docs.devin.ai/work-with-devin/advanced-capabilities (create from sessions)
- docs.devin.ai/product-guides/automations (automation triggers)

## When to Use

- "Create a playbook for X" / "Make this reusable"
- "I keep repeating the same instructions to Devin"
- "Turn this successful session into a playbook"
- "Refine/improve this playbook"
- "Use playbook X for this task"
- Any repeated multi-step task that would benefit from a structured prompt

## When NOT to Use

- One-off task — just describe it directly
- Style guide / project conventions — use Knowledge entries instead
  (cloud feature; in CLI, put in `.devin/global_rules.md`, `.devin/rules/*.md`, or a skill)
- Simple single-step task — a playbook adds overhead without value

## Playbook format

A playbook is a Markdown file with the following sections:

```markdown
# <Playbook Name>

## Goal
<One sentence: the outcome Devin should achieve>

## Procedure
1. <imperative step — setup>
2. <imperative step — main task>
3. <imperative step — delivery>
   - <sub-bullet: step-specific advice>

## Specifications
<Postconditions — what should be true when done?>
- <condition 1>
- <condition 2>

## Advice
<Tips that apply to the whole task>
- <pointer 1>
- <pointer 2>

## Forbidden Actions
<What Devin must NOT do>
- <prohibition 1>
- <prohibition 2>

## Required from User
<What the user must provide that Devin cannot obtain>
- <input 1>
- <input 2>
```

## Procedure (creating a playbook)

### Step 1 — Define the outcome

1. Ask: "What should be true when this playbook is applied successfully?"
2. Write the Goal in one sentence
3. Write Specifications as postconditions (testable conditions)

### Step 2 — Outline the procedure

1. List every step imperatively ("Write X", "Navigate to Y", "Run Z")
2. Cover the entire scope: setup -> main task -> delivery
3. Make steps Mutually Exclusive and Collectively Exhaustive
4. Add sub-bullets for step-specific advice
5. Don't over-specify — leave room for Devin to problem-solve

### Step 3 — Add advice and constraints

1. **Advice**: preferred approaches, corrections to Devin's priors
2. **Forbidden Actions**: what to never do (e.g., "Don't push to main")
3. **Required from User**: tokens, credentials, decisions only the
   user can make

### Step 4 — Save the playbook

1. Write to `.devin/playbooks/<name>.devin.md` (project-level) or
   `~/.config/devin/playbooks/<name>.devin.md` (user-level)
2. The `.devin.md` extension matches cloud convention — if the user
   later uses cloud Devin, the file is directly attachable

### Step 5 — Test and iterate

1. Apply the playbook to a real task
2. Note where Devin needed help or deviated
3. Refine: add steps, advice, or forbidden actions
4. Re-test until Devin succeeds without intervention

## Procedure (using a playbook)

1. `read` the playbook file
2. Follow the Procedure section step-by-step
3. Check Specifications after completion — all postconditions met?
4. Respect Forbidden Actions throughout
5. If "Required from User" items are missing, ask before proceeding

## Procedure (creating from a past session)

Cloud Devin can analyze session links and produce a playbook. In the
CLI:

1. `read` the session transcript (if saved) or ask the user to describe
   what worked
2. Extract: what was the goal, what steps were taken, what went wrong
   and was fixed, what advice would prevent the wrong turns
3. Structure into the playbook format
4. Save and test

## Local playbook library

```
.devin/playbooks/          # project-level playbooks
  <name>.devin.md
~/.config/devin/playbooks/  # user-level playbooks (cross-project)
  <name>.devin.md
```

To list available playbooks: `glob` for `**/*.devin.md` in both
locations.

## Macros (CLI adaptation)

Cloud playbooks support `!macro-name` shortcuts. The CLI has no macro
system, but you can approximate it:

1. Name playbook files descriptively: `hotfix-memory-leak.devin.md`
2. The user references them by name: "use the hotfix-memory-leak
   playbook"
3. For frequently used playbooks, add a one-line alias in `.devin/global_rules.md`:
   `!memleak -> .devin/playbooks/hotfix-memory-leak.devin.md`

## Cross-skills

- Use `writing-skills` to ensure the playbook is written in an agent-readable style.
- Use `devin-config` when a playbook grows into a reusable skill or rule.

## CLI-specific notes

- No team/community library: cloud playbooks are shareable across
  orgs. The CLI playbooks are local files — share via git or manual
  copy.
- No automation triggers: cloud playbooks can be triggered by
  Automations (Slack, GitHub, schedules). The CLI has no automation
  system — playbooks are invoked manually.
- No inline editing UI: cloud playbooks show a blue pill with an
  edit component. The CLI requires `edit` on the file directly.
- No "Playbook Devin Mode" pinning: cloud playbooks can specify a
  Devin mode (Fast/Normal). The CLI user selects the mode with
  `/mode` before applying the playbook.
