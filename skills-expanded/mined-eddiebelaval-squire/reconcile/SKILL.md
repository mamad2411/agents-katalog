---
name: Reconcile
slug: reconcile
description: Living document reconciliation — maintain the VISION/SPEC/BUILDING triangle
category: operations
complexity: complex
version: "1.0.0"
author: "id8Labs"
triggers:
  - "reconcile"
  - "reconcile docs"
  - "update vision"
  - "update spec"
  - "sync documents"
  - "triad reconciliation"
tags:
  - documentation
  - triad
  - operations
  - vision
  - spec
---

# Reconcile — Living Document Reconciliation

Maintain the three-document triangle: VISION.md (north star), SPEC.md (contract), BUILDING.md (journal). This skill is **conversational** — it asks questions, listens, and writes the docs. Eddie talks, Claude writes.

## Core Workflows

### Workflow 1: Reconciliation Interview
1. Detect environment and locate triangle documents
2. Read all existing docs into context
3. Interview Eddie conversationally about changes
4. Update affected documents
5. Report delta between VISION and SPEC (= roadmap)

### Workflow 2: Initialize Triangle
1. Create VISION.md, SPEC.md, BUILDING.md from conversation
2. Interview for each document in sequence
3. Write all three with consistent voice

## Core Philosophy

> The triangle self-corrects through conversation. VISION evolves when Eddie learns something. SPEC evolves when reality changes. BUILDING records what happened. The gap between VISION and SPEC IS the roadmap.

**CRITICAL:** This is an interview, not a form. Use `AskUserQuestion` for structured choices. Use natural conversation for open-ended questions. NEVER hand Eddie a template with brackets to fill in. Ask, listen, write.

---

## Step 0: Detect Environment

1. Identify the project from `--project` flag or current directory.
2. Resolve the project root using the same logic as workspace generators (walk up to `.git` or use known project paths).
3. Check which triangle documents exist:
   - `VISION.md` at project root
   - `SPEC.md` at project root
   - `BUILDING.md` at project root
4. Read all existing triangle documents into context.
5. State: "Reconciling **[PROJECT]** on branch **[BRANCH]**"
6. If mode is `init` and documents already exist, warn and confirm before overwriting.

---

## Mode: `init` — Initialize the Triangle

When VISION.md and/or SPEC.md don't exist yet. BUILDING.md is assumed to exist (or will be created separately per existing conventions).

### Phase 1: Soul Interview (for VISION.md)

Start with the most important question. Use `AskUserQuestion`:

**Q1:** "In one breath — why does [PRODUCT] exist? Not what it does. Why it exists. What world does it create?"

Listen. Write the Soul section from their answer. Read it back for confirmation.

**Q2:** "Who is this for? Not demographics — tell me about the person. What are they feeling before they find [PRODUCT]? What do they feel after?"

Listen. Write the User Truth section.

**Q3:** "What are the 3-7 commitments this product makes? The things it MUST be or do to fulfill that soul. Don't think about features — think about promises."

For each pillar they name, ask: "Is this realized today, partially built, or still unrealized?"

Write the Pillars section with status markers.

**Q4:** "What must [PRODUCT] NEVER become? What are the traps, the tempting-but-wrong directions?"

Write the Anti-Vision section.

**Q5:** "Where does [PRODUCT] end? What adjacent problems does it deliberately refuse to solve?"

Write the Edges section.

Create `VISION.md` at the project root using the template structure from `~/.claude/doc-templates/vision.md`. Populate the Evolution Log with a single entry: today's date, "Initial vision captured", "Triangle initialization".

### Phase 2: Reality Scan (for SPEC.md)

This phase is **automated** — scan the codebase, don't ask Eddie about what already exists.

1. **Read existing docs:** BUILDING.md, CLAUDE.md, README.md, package.json
2. **Scan architecture:** Glob for key patterns:
   - `**/app/api/**/route.ts` (API routes)
   - `**/app/**/page.tsx` (pages)
   - `**/components/**/*.tsx` (components)
   - `**/lib/**/*` (core logic)
   - `**/*.test.*` or `**/*.spec.*` (tests)
   - `**/migrations/**` (database)
   - `.env*` patterns (integrations)
3. **Extract capabilities:** From routes, pages, and components, derive what the product CAN DO today.
4. **Extract architecture:** From imports and config, derive the tech stack.
5. **Extract boundaries:** From what's NOT in the codebase (reference VISION pillars marked UNREALIZED).
6. **Build verification surface:** For each capability, write a testable assertion.

Draft SPEC.md and present a summary to Eddie:
- "Here's what I found. [N] capabilities, [M] integrations, [K] things that don't exist yet."
- "Does this match your understanding of what [PRODUCT] is today?"

If Eddie corrects anything, update and re-present.

Create `SPEC.md` at the project root using the template structure from `~/.claude/doc-templates/spec.md`.

### Phase 3: Triangle Summary

Show the completed triangle:
```
VISION: [Soul — one sentence]
  [N] pillars ([R] realized, [P] partial, [U] unrealized)

SPEC: [Identity — one sentence]
  [C] capabilities, [I] integrations
  Verification: [V] assertions

BUILDING: [exists/created]

Distance: [X]% (VISION pillars realized in SPEC)
```

---

## Mode: `scan` — Drift Detection

Read VISION.md and SPEC.md. Scan for drift without making changes.

### Scan 1: SPEC vs. Codebase

Check whether SPEC.md matches reality:

1. **Capabilities check:** For each capability listed in SPEC, verify the referenced routes/components/pages still exist and function as described.
2. **Architecture check:** Verify the tech stack table matches actual dependencies in package.json and imports.
3. **Integrations check:** Verify listed integrations are still active (env vars present, imports exist).
4. **New capabilities:** Scan for routes/pages/features NOT listed in SPEC (things that shipped but weren't recorded).
5. **Dead capabilities:** Check for SPEC entries whose backing code was removed.

### Scan 2: VISION vs. SPEC

Check alignment between north star and current state:

1. **Pillar status audit:** For each VISION pillar, check whether SPEC capabilities support its current status marker. Flag if a pillar says UNREALIZED but SPEC shows related capabilities, or vice versa.
2. **Distance calculation:** Recalculate the "X% of pillars realized" metric.
3. **Boundary alignment:** Check SPEC boundaries against VISION edges — are they consistent?

### Scan 3: BUILDING vs. Both

Quick check for major events in BUILDING.md that should have triggered updates:

1. Look at BUILDING.md entries after the last SPEC reconciliation date.
2. Flag any entries that describe new capabilities, architecture changes, or pivots that aren't reflected in SPEC or VISION.

### Output

Present a drift report:

```
DRIFT REPORT — [PROJECT] — [DATE]

SPEC Drift:
  [N] capabilities match codebase
  [M] capabilities not in codebase (stale)
  [K] codebase features not in SPEC (undocumented)
  [J] architecture mismatches

VISION Drift:
  [P] pillar status changes detected
  Distance: SPEC says [X]%, actual appears to be [Y]%

BUILDING Gap:
  [B] entries since last reconciliation not reflected in SPEC/VISION

Overall: [CURRENT / DRIFTED / STALE]
```

If drift is found, ask: "Want me to reconcile now, or just flag this for later?"

---

## Mode: `vision` — North Star Evolution

Something changed in Eddie's understanding of the product. This is the most conversational mode.

### The Interview

**Do NOT ask "what changed?"** — that's too open. Ask specific questions:

**Q1 (AskUserQuestion):** "Which part of the vision shifted?"
Options:
- Soul (why this exists)
- A pillar changed status
- New pillar needed
- A pillar should be removed
- User truth evolved (who this is for)
- Edges/Anti-Vision changed
- Something else

Based on their answer, dive deeper:

**If Soul:** "That's a pivot signal. What happened that changed why [PRODUCT] exists? What did you learn?"

**If Pillar status:** "Which pillar?" (list them with current status). Then: "What's the new status? What evidence or signal drove this change?"

**If New pillar:** "What's the commitment? Why is it essential — what breaks without it? Is it realized, partial, or unrealized right now?"

**If Remove pillar:** "Which one? Why isn't it a commitment anymore? Was it wrong from the start, or did the product outgrow it?"

**If User truth:** "What did you learn about the user? Was this from a real conversation, usage data, or a realization?"

**If Edges/Anti-Vision:** "What new boundary or failure mode did you identify? What prompted this?"

### Write the Update

1. Read current VISION.md.
2. **REWRITE** the affected section (don't append — overwrite with the new truth).
3. Add an entry to the Evolution Log with: date, what shifted, the signal that caused it, which section was rewritten.
4. Update the distance/confidence metrics in the header if applicable.
5. Present the diff to Eddie: "Here's what changed in VISION.md — [summary]."
6. If the VISION change implies SPEC should change too (e.g., a pillar went from UNREALIZED to PARTIAL), flag it: "This also means SPEC.md needs updating. Want me to reconcile SPEC too?"

---

## Mode: `spec` — Contract Reconciliation

Something shipped or changed in the codebase. SPEC needs to match reality.

### Phase 1: Auto-Scan

Run the same codebase scan as `scan` mode, Scan 1 (SPEC vs. Codebase). Identify:
- New capabilities to add
- Stale capabilities to remove or update
- Architecture changes
- New/removed integrations

### Phase 2: Conversational Confirmation

Present findings to Eddie:

"I scanned the codebase and found [N] things that changed since SPEC was last reconciled:"

List each finding as a short bullet. Then ask:

**For new capabilities:** "Should I add [CAPABILITY] to the spec? Here's what I'd write: [one-line description]."

**For stale entries:** "This capability is listed but the backing code is gone: [CAPABILITY]. Remove from SPEC?"

**For architecture changes:** "The stack changed — [OLD] is now [NEW]. Update the architecture contract?"

### Phase 3: Write Updates

1. Read current SPEC.md.
2. **REWRITE** affected sections (capabilities, architecture, integrations, boundaries).
3. Update the Drift Log with entries for each change.
4. Recalculate VISION alignment percentage.
5. Update the header (last reconciled date, drift status → CURRENT, stage if applicable).
6. **Update Verification Surface:** For each new capability, add a testable assertion. For removed capabilities, remove the assertion.
7. Present summary: "SPEC.md reconciled. [N] capabilities added, [M] removed, [K] updated. Verification surface now has [V] assertions."

### Phase 4: VISION Check

After SPEC update, check if any VISION pillars changed status as a result:
- "Pillar [X] was marked PARTIAL — based on what just shipped, should this be REALIZED now?"
- If yes, offer to update VISION.md too (switch to `vision` mode for that section).

---

## Mode: Full Reconcile (default, no arguments)

Run all modes in sequence:

1. **Scan** — detect all drift
2. **SPEC reconcile** — update contract to match codebase
3. **VISION interview** — ask what shifted in understanding
4. Present final triangle summary

This is the "quarterly checkup" mode. Use it before major releases, after pivots, or when things feel off.

---

## Rules

1. **NEVER hand Eddie a doc full of brackets.** Interview him. He talks, you write.
2. **Rewrite, don't append.** VISION and SPEC are present-tense documents. When something changes, the section is rewritten to be true NOW. The logs (Evolution Log, Drift Log) capture what changed and why.
3. **Present tense only in SPEC.** "The system DOES X" — never "will do" or "should do."
4. **Directional language in VISION.** "This product exists to..." — aspirational but grounded.
5. **Always update logs.** Every change to VISION gets an Evolution Log entry. Every change to SPEC gets a Drift Log entry. No exceptions.
6. **Flag cross-document impact.** If a VISION change implies SPEC changes (or vice versa), say so explicitly and offer to update both.
7. **Don't touch BUILDING.md.** That document is updated as part of the release SOP, not during reconciliation. It's the journal — it captures what happened when it happened.
8. **Distance metric must stay accurate.** After any update, recalculate the pillar realization percentage in both document headers.
9. **Use the project's existing voice.** Read BUILDING.md and VISION.md before writing to match tone. Parallax sounds different than Homer.
10. **Respect the Anti-Vision.** If a proposed SPEC capability contradicts the VISION Anti-Vision section, flag it immediately: "This conflicts with your Anti-Vision: [quote]. Proceed anyway?"

---

## Integration with Pipeline

- **Gate passes (any stage):** Run `/reconcile spec` — something shipped, SPEC should reflect it.
- **Pivots or learning moments:** Run `/reconcile vision` — the north star shifted.
- **Before release PR to main:** Run `/reconcile scan` — ensure the triangle is tight.
- **New project initialization:** Run `/reconcile init --project [name]` — start the triangle.
- **Quarterly or when things feel off:** Run `/reconcile` (full) — the complete checkup.

---

## Derived Outputs (Triad Derivation Engine)

The triangle doesn't just maintain itself — it **produces computed outputs**. These are views over the three source documents, never stored, always fresh:

| Command | Function | Inputs |
|---------|----------|--------|
| `/roadmap` | Prioritized build order | `f(VISION, SPEC, BUILDING)` |
| `/drift` | Trajectory analysis — converging or wandering? | `f(VISION, BUILDING)` |
| `/changelog` | What shipped recently | `f(BUILDING, SPEC)` |
| `/pitch` | Investor/user-facing narrative | `f(VISION, SPEC)` |
| `/debt` | Technical + product debt report | `f(SPEC, VISION, BUILDING)` |
| `/onboard` | New contributor orientation | `f(BUILDING, SPEC)` |

Full specifications: `.claude/skills/triad-derive/SKILL.md`

After any `/reconcile` operation that changes VISION or SPEC, mention that derived outputs (`/roadmap`, `/drift`, etc.) will reflect the changes automatically.

---

## Quick Reference

| Situation | Command | What Happens |
|-----------|---------|-------------|
| New project needs the triangle | `/reconcile init` | Soul interview + codebase scan |
| Something shipped | `/reconcile spec` | Scan code, update contract |
| I learned something about the product | `/reconcile vision` | Conversational interview, update north star |
| Things feel off / pre-release | `/reconcile scan` | Drift report, no edits |
| Full checkup | `/reconcile` | Scan + SPEC update + VISION interview |
| What should I build next? | `/roadmap` | Prioritized gap analysis |
| Are we building the right things? | `/drift` | Trajectory + scope creep detection |
| What shipped? | `/changelog` | Recent changes by type |
| Explain this product to someone | `/pitch` | Vision + proof narrative |
| What's rotting? | `/debt` | Tech + product debt scan |
| New team member joining | `/onboard` | Context + gotchas guide |
