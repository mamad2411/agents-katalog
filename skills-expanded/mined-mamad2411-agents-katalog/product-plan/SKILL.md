---
name: product-plan
description: Turn a product-brainstorm doc into a structured plan — user personas, user flows, in/out of scope, epics, and stories with acceptance criteria. Outputs docs/product-plans/<slug>.md. Usage — /product-plan <slug>
argument-hint: "<feature-slug>"
arguments:
  - name: slug
    description: "Feature slug — matches the brainstorm doc filename"
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Bash(find *)
  - Bash(ls *)
---

# Product Plan

Parse `$ARGUMENTS[0]` as the feature slug.

---

## Step 1 — Load the brainstorm doc

```bash
# Look for the brainstorm doc
find docs/product-brainstorm/ -name "<slug>*.md" | head -3
```

If found: read it fully before proceeding.
If not found: tell the PM and ask them to run `/product-brainstorm <slug>` first. Stop.

---

## Step 2 — Define user personas

Based on the brainstorm, propose 1–3 user personas. For each, ask the PM to confirm or correct:

> I've identified these personas from the brainstorm. Confirm or edit:
>
> **Persona 1: <Name> (<Role>)**
> - Goals: …
> - Pain points: …
> - Tech literacy: …
>
> Are these right? Any to add or change?

Wait for confirmation.

---

## Step 3 — Define user flows

For each persona, describe their end-to-end flow as numbered steps.

> Here's the user flow for <Persona>:
> 1. …
> 2. …
> 3. …
>
> Does this flow match your expectation? Any steps missing or wrong?

Wait for confirmation before moving to scope.

---

## Step 4 — Confirm scope

Present the in-scope and out-of-scope items captured from the brainstorm. Ask the PM to confirm:

> **In scope (initial version):**
> - …
>
> **Out of scope:**
> - … — reason
>
> Any changes before I write the stories?

---

## Step 5 — Define epics and stories

ultrathink

Break the in-scope work into epics (themes of related work) then stories within each epic.

For each story:
- Use the format: **As a** <persona>, **I want** <action>, **so that** <benefit>
- Write 3–5 acceptance criteria as checkboxes
- Estimate size: XS / S / M / L / XL
- Flag dependencies on other stories

Present each epic with its stories and ask:

> Here are the stories for **Epic: <Name>**:
> <list>
>
> Any stories missing? Any acceptance criteria to adjust?

Wait for confirmation per epic.

---

## Step 6 — Write the output document

Write to `docs/product-plans/<slug>.md`:

```markdown
# Product Plan: <Feature Name>
_Date: <today> · Status: Draft_
_Source: docs/product-brainstorm/<slug>.md_

## User Personas

### <Name> (<Role>)
- **Goals:** …
- **Pain points:** …
- **Tech literacy:** Low / Medium / High

## User Flows

### <Persona Name> — <Flow Name>
1. …
2. …
3. …

## Scope

### In Scope
- …

### Out of Scope
- … — reason

## Epics & Stories

### Epic 1: <Name>
_Goal: …_

#### Story 1.1 — <Title>
**As a** <persona>, **I want** <action>, **so that** <benefit>.
**Size:** S
**Depends on:** —

**Acceptance Criteria:**
- [ ] …
- [ ] …

#### Story 1.2 — <Title>
…

### Epic 2: <Name>
…

## Open Questions
| Question | Owner | Status |
|---|---|---|

## Next Step
→ Run `/product-tasks <slug>` to create GitHub issues and milestones.
```

---

## Step 7 — Hand off

After writing:

> Plan saved to `docs/product-plans/<slug>.md`.
>
> Ready to create GitHub issues and milestones?
> ```
> /product-tasks <slug>
> ```
