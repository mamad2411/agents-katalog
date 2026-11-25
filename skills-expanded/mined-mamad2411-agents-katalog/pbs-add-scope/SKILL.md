---
name: pbs-add-scope
description: "Use when a project in construction needs new scope — client requests new features, business logic changes mid-project, pivot requires rethinking architecture, or new requirements arrive that don't fit in the current roadmap"
---

# Add Scope

## Overview

Handle scope changes in a project already in construction — from a new client requirement to a full architectural pivot.

**Core principle:** Living documents ALWAYS reflect the current state of the project. When scope changes, the documents must change too — but the original exploration history remains untouched as an audit trail. Scope changes are ADDITIVE: new artifacts in `scopes/`, new sections in living docs, new phases in the roadmap.

**Announce at start:** "I'm using the pbs-add-scope skill to add new scope to this project."

## When to Use

- A business logic change requires new features or modifications to planned features
- A large new feature arrives that needs more than one phase to implement
- A pivot requires rethinking parts of the architecture or roadmap
- New requirements emerge mid-project that affect the remaining phases
- The client says "we also need X" and X doesn't fit in any existing phase
- A regulatory or compliance change forces modifications to the planned scope

## When NOT to Use

- Small tweaks that fit within the current phase → add them to the current phase's tasks
- Bug fixes → use pbs-fixing-issues
- The project hasn't started construction yet → use pbs-exploration-brainstorming and pbs-exploration-discovery instead

## The Iron Law

```
ORIGINAL EXPLORATION DOCS ARE IMMUTABLE.
LIVING DOCS GET UPDATED ADDITIVELY.
COMPLETED PHASES ARE FROZEN.
```

Scope changes create NEW artifacts in `scopes/`. They UPDATE living documents additively. They NEVER modify original exploration files or completed phase artifacts.

## Input

**Living documents (required):**
- `.pbs-framework/00-project-brief.md`
- `.pbs-framework/01-system-overview.md`
- `.pbs-framework/02-technical-design.md`
- `.pbs-framework/03-decision-log.md`
- `.pbs-framework/04-roadmap.md`

**Optional:**
- `.pbs-framework/05-tech-debt-register.md` (if exists)
- `.pbs-framework/06-architecture-snapshot.md` (if exists)
- Previous closure report (if the scope change follows a phase closure)

## The Process

### Step 1: Understand the Change

Ask the human:
1. **What** is changing? (new feature, business rule change, pivot, new integration)
2. **Why** is it changing? (client request, market shift, technical discovery, regulatory)
3. **How big** is it? (quick assessment: hours / days / weeks of new work)

Read ALL living documents to understand the current state of the project.

### Step 2: Generate Scope Record

Determine the next SC number by checking `.pbs-framework/scopes/` (or SC-01 if none exist).

Generate `.pbs-framework/scopes/SC-XX-[nombre]/scope-record.md` using the template at `templates/scope-record.md.template`:

1. **Qué cambia** — describe the change clearly
2. **Por qué** — document the motivation
3. **Impacto** — which modules and phases are affected
4. **Decisiones afectadas** — cross-reference DEC-XXX entries from the Decision Log:
   - For each affected decision: state whether it's `vigente` (still valid) or `reemplazada` (superseded), and why
   - If no existing decisions are affected, state it explicitly
5. **Alcance propuesto** — what's included and excluded in this scope change
6. **Fases nuevas propuestas** — initial estimate of new phases needed

<HARD-GATE>
The human MUST review and approve the Scope Record before continuing.
If the human disagrees with the impact assessment or scope boundaries, iterate.
Do NOT proceed to exploration until the Scope Record is approved.
</HARD-GATE>

### Step 3: Inline Brainstorming (Lightweight)

Guide the human through Blocks 1-3 from the brainstorming questionnaire:

- **Block 1: The Problem** — What concrete problem does this scope change solve?
- **Block 2: Proposed Solution** — What's the simplest path to address it?
- **Block 3: Scope and Limits** — What's IN and what's OUT of this change?

Ask questions **one at a time** — never dump all questions at once.

Generate `.pbs-framework/scopes/SC-XX-[nombre]/brainstorming-synthesis.md` with the conclusions.

### Step 4: Inline Discovery (Optional)

Ask the human: **"Does this scope change introduce technical unknowns that need investigation?"**

- If **no** → skip to Step 5
- If **yes** → guide a focused discovery covering only the new technical questions:
  - New APIs or integrations needed?
  - New technology decisions?
  - Feasibility concerns?
  - Generate `.pbs-framework/scopes/SC-XX-[nombre]/discovery-synthesis.md`

If spikes are needed:

**REQUIRED:** Use pbs-spike-planning to generate spike specs. Pause for spike execution before continuing.

### Step 5: Update Living Documents

Update each living document ADDITIVELY — do not rewrite existing content, add sections for the scope change.

#### Project Brief (`00-project-brief.md`)
- Add a section at the end: `## SC-XX: [Nombre]`
- Include: what changes in scope, new constraints, updated success criteria (if applicable)

#### System Overview (`01-system-overview.md`)
- Add new entities, capabilities, or integrations if the scope change introduces them
- Mark which existing capabilities are affected

#### Technical Design (`02-technical-design.md`)
- Add new modules or update module responsibilities if the scope change requires it
- Update data flow if it changes

#### Decision Log (`03-decision-log.md`)
- Add new decisions introduced by this scope change with origin `SC-XX`
- For superseded decisions: add a new entry noting the supersession and reference both the old DEC and the new one

#### Roadmap (`04-roadmap.md`)
- Add new phases for the scope change
- Phases continue the existing numbering (e.g., if last phase was 5, new phases start at 6)
- Each new phase must have at minimum: objective + deliverable + dependencies
- Mark which existing pending phases are affected (if any)

### Step 6: Verify Updates

**REQUIRED:** Use superpowers:verification-before-completion

Check that all documents were updated correctly:
- [ ] Scope Record exists with all sections filled
- [ ] Brainstorming synthesis exists
- [ ] Discovery synthesis exists (if discovery was done)
- [ ] All living documents have SC-XX sections or updates
- [ ] Decision Log has new entries with SC-XX origin
- [ ] Roadmap has new phases with proper numbering and dependencies
- [ ] No original exploration files were modified
- [ ] No completed phase artifacts were modified

### Step 7: Present to Human

Summarize:
- What was documented (Scope Record, brainstorming, optional discovery)
- Which living documents were updated and what changed in each
- New phases added to the roadmap (count, estimated scope)
- Any open questions or decisions the human needs to make

<HARD-GATE>
The human MUST validate that:
1. The Scope Record accurately describes the change and its impact
2. Living documents reflect the new reality
3. New phases in the roadmap are properly scoped
4. Affected decisions are correctly marked as vigente or reemplazada
5. Original exploration docs and completed phases were NOT modified

Do NOT proceed to phase-planning for the new phases until the human approves.
</HARD-GATE>

## What This Skill Does NOT Handle

- **Scope changes during an in-progress phase** — finish or pause the current phase first, then add scope
- **Reverting a previous scope change** — that's a new scope change that supersedes the previous one
- **Splitting or merging existing phases** — that's roadmap restructuring, handled during phase-closure
- **Deleting or archiving scope records** — scope records are permanent audit artifacts

## Common Mistakes

- **Modifying original exploration files** — the `exploration/` directory is immutable history. Scope changes create new artifacts in `scopes/`.
- **Rewriting living documents instead of adding** — updates are ADDITIVE. Don't delete existing sections, add SC-XX sections.
- **Skipping the Scope Record** — jumping straight to brainstorming loses the "why" of the change. Always document the motivation first.
- **Not cross-referencing affected decisions** — every scope change should check if existing DEC-XXX entries are still valid.
- **Numbering new phases from 1** — new phases continue the existing roadmap numbering. If Phase 5 was last, new phases start at Phase 6.

## Red Flags

Signs the agent is about to violate the process — if you catch yourself thinking any of these, STOP:

- "I'll just update the exploration synthesis with the new info" → NO. Exploration docs are immutable.
- "This change is small, no need for a Scope Record" → Every scope change gets documented. Small changes have small records.
- "I'll rewrite the project brief to incorporate this" → ADDITIVE updates only. Add a SC-XX section.
- "The completed phases need updating too" → Completed phases are frozen. Never touch them.
- "I'll skip brainstorming, the change is obvious" → Blocks 1-3 take 15 minutes. The synthesis prevents misunderstandings.
- "Let me start planning the new phases now" → HARD-GATE. Human approves the scope change first.
- "This decision replaces the old one, I'll just edit DEC-003" → Add a NEW decision entry. The old entry stays for audit.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "The exploration docs are outdated anyway" | They're historical record. Create new artifacts in `scopes/` instead. |
| "This scope change is too small for all this process" | Small scope changes have small Scope Records. The process scales down. |
| "The living docs will get too long with all these SC sections" | Long docs that reflect reality > short docs that lie. Trim in a dedicated cleanup phase if needed. |
| "I already know what phases we need" | Document the reasoning in the Scope Record. Future-you needs the "why". |
| "The old decision was wrong, let me fix it" | Decisions aren't wrong — they were right for the context. Add a new decision that supersedes. |
| "Discovery isn't needed, I know this tech" | Ask the human. They decide if discovery is needed, not you. |
| "Let me update the completed phase closure report" | Completed phases are frozen. Document any relevant context in the Scope Record instead. |

## Integration

**Called after:**
- pbs-phase-closure — when new scope is identified after closing a phase
- Any point between phases — when the human identifies new scope to add

**Delegates spike spec generation to:**
- pbs-spike-planning — if the scope change introduces uncertain technical questions

**Calls next:**
- pbs-phase-planning — for the new phases, after human approves the scope change

**Does NOT modify:**
- pbs-phase-planning — reads updated living docs without changes
- pbs-phase-closure — continues consolidating as before
- Any existing skill — this skill is additive to the framework

**Required skills:**
- **REQUIRED:** superpowers:verification-before-completion — verify all docs are updated correctly

**Language:** Write all `.pbs-framework/` documents in the language defined in AGENTS.md `framework_language` field.
