---
name: handoff-updater
description: "Updates HANDOFF.md with sprint outcomes. Required as part of DoD - sprint cannot close without HANDOFF update. Validated by handoff-keeper subagent (fresh context) for meaningful content. Runs at end of each sprint and at task cycle completion."
---

# HANDOFF Updater

Обновляет HANDOFF.md - обязательно для закрытия sprint.

## Когда применять

- В конце каждого sprint (DoD requirement)
- В конце всего task cycle (executive summary)
- Когда executor вызывает /sprint:checkin claiming "HANDOFF.md updated"

## HANDOFF.md philosophy

HANDOFF.md - **живой документ**:
- Читается в начале каждой Claude Code сессии (контекст)
- Обновляется в конце work units
- Передаёт state между сессиями
- Most recent at top (LIFO order)

## Required structure

```markdown
# Project HANDOFF

Last updated: {{TIMESTAMP}}

## Sprint cycle: {{TASK_NAME}} ({{DATE}})

### Recent activity

{2-4 sentences describing what was done in this sprint cycle}

### Important decisions

- {Decision 1}: {rationale}
- {Decision 2}: {rationale}

или "No significant decisions in this cycle."

### Open questions

- {Question}: {context, why deferred}

или "No open questions."

### Next session priorities

1. {Priority 1}
2. {Priority 2}

### Tracker references (if integrated)

- T-1 → {ticket-link}
- T-2 → {ticket-link}

### Reports

- HTML report: [{archive-path}/report.html]({archive-path}/report.html)
- Retrospective: [{archive-path}/retrospective.md]({archive-path}/retrospective.md)

---

## Sprint cycle: {{PREVIOUS_TASK}} ({{PREVIOUS_DATE}})

[... previous cycle content unchanged ...]

---

## [Original/older HANDOFF content]

[... preserved ...]
```

## Workflow

### 1. Read existing HANDOFF.md

```bash
HANDOFF_PATH="HANDOFF.md"
[ -f "$HANDOFF_PATH" ] || echo "# Project HANDOFF\n\n(empty)" > "$HANDOFF_PATH"
```

### 2. Detect external changes

If HANDOFF.md was modified outside of sprint cycle (manual user edits):

```bash
# Compare with our pre-sprint snapshot
HANDOFF_PRE=$(cat .sprints/active/_handoff-pre-sprint.md 2>/dev/null)
HANDOFF_CURRENT=$(cat HANDOFF.md)

if [ "$HANDOFF_PRE" != "$HANDOFF_CURRENT" ]; then
    # External changes detected - propose merge, не overwrite
    echo "WARNING: HANDOFF.md was modified outside sprint cycle."
    echo "Propose merge - не overwrite."
fi
```

### 3. Generate new section

For sprint completion:
- Pull data from sprint-{N}.md (goal, achievement)
- Pull decisions from se-review (any decisions documented)
- Pull open questions from retrospective.md
- Pull tracker tickets if integration enabled
- Pull HTML report path

For task cycle completion:
- Aggregate across all sprints
- Executive summary
- Forward-looking priorities

### 4. Insert at top

New section goes at top of "Sprint cycle:" sections (most recent first).
Original/older content preserved below.

### 5. Validate via handoff-keeper subagent

Запустить `handoff-keeper` agent (fresh context):

Subagent reads:
- Pre-update HANDOFF.md
- Post-update HANDOFF.md
- Sprint state

Verifies:
- Required sections present
- Content meaningful (not just timestamps)
- Sprint goal reflected
- Decisions captured
- Forward-looking priorities present

If validation fails - revise update, retry.

### 6. Commit timing

HANDOFF.md update is part of DoD - executor must `/sprint:checkin "HANDOFF.md updated"` after this skill runs.

dod-validator confirms HANDOFF.md modification timestamp within sprint window.

## Validation rules (handoff-keeper checks)

### Section completeness

All required sections present:
- ✓ Recent activity (non-empty, specific)
- ✓ Important decisions (или explicit "none")
- ✓ Open questions (или explicit "none")
- ✓ Next session priorities

### Content meaningfulness

**Recent activity check**:
- Length >= 50 chars
- References specific sprint outcomes (не generic "work done")
- Should mention sprint goal achievement

**Decisions check**:
- If listed - each имеет rationale
- Не just "decided X" without context

**Open questions check**:
- If listed - each имеет context (why open, what blocks resolution)

**Priorities check**:
- Actionable items (start with verb или specific question)
- Не vague ("continue work" - bad; "Address remaining audit findings" - good)

### Tracker references (если applicable)

If tracker integration enabled:
- Ticket numbers present
- Links valid format

### Reports references

- HTML report path correct
- Retrospective path correct
- Both files exist

## Conflict handling

When user manually edited HANDOFF.md между sprint cycles:

### Detection

Pre-sprint snapshot stored. Diff at update time.

### Resolution strategy: **merge, не overwrite**

1. Show user diff:
   ```
   HANDOFF.md was modified externally:
   + Added section "Custom user notes"
   ~ Modified "Recent activity" of last cycle
   
   Propose merge:
   - Keep your "Custom user notes" section
   - Append new sprint cycle section above your edits
   - Preserve your modifications to old cycle
   ```

2. Wait for user OK или resolution
3. Apply merge (preserve user edits + add new cycle)

In non-interactive mode:
- Default: append new section, не overwrite anything
- Log conflict for next interactive session

## Auto-archive when too long

After 30 sprint cycle sections в HANDOFF.md:
- Move oldest to HANDOFF-archive.md
- Keep most recent 30 in HANDOFF.md
- Add reference link to archive

## Integration с claude-solo-factory kit (если установлен)

Kit имеет skill `wiki-workflow` который описывает **knowledge architecture** проекта (4 layers):

1. **Layer 1**: `docs/specs/<feature>/` - per-feature briefs/PRDs (lifecycle: feature lifetime)
2. **Layer 2**: `docs/architecture/` - decisions/designs (lifecycle: append-only)
3. **Layer 3**: `docs/data-sources/` - data source references (lifecycle: investigated once)
4. **Layer 4**: Wiki via kfchou/wiki-skills plugin (lifecycle: ongoing knowledge)

ai-scrum's HANDOFF.md - это **operational continuity** layer (different concern).

### Detection

```bash
test -f .claude/skills/wiki-workflow/SKILL.md
```

### Если kit's wiki-workflow available

handoff-updater:
1. **Updates HANDOFF.md** as usual (sprint cycle outcomes)
2. **Identifies knowledge** that should go to specific layers:
   - Architectural decisions → suggest creating ADR (kit's adr-writer)
   - New feature understanding → suggest updating brief/PRD (kit's prd-writer)
   - Data source insights → suggest data-source-research skill
   - Long-term wisdom → suggest wiki entry (via wiki-skills plugin)
3. Adds **routing recommendations** в HANDOFF.md update:

```markdown
## Sprint cycle: ... 

### Knowledge routing recommendations

The following items might belong in specific layers (not just HANDOFF):

- Architectural decision about Stripe library version → create ADR-0042
- Data source schema for `payments` table → run data-source-research skill
- Long-term insight about VIP customer behavior → consider wiki entry
```

This avoids HANDOFF.md becoming a knowledge graveyard.

### Если kit absent

handoff-updater работает **standalone** - все knowledge goes в HANDOFF.md. 

Recommendation в final summary: "Consider installing claude-solo-factory kit for proper knowledge layer architecture."

## Output

Updated HANDOFF.md.
Optionally HANDOFF-archive.md (after auto-archive).

Validation report (from handoff-keeper subagent):
`.sprints/active/handoff-validation.md`:

```markdown
# HANDOFF.md Validation

**Validated at**: {timestamp}
**Validated by**: handoff-keeper subagent (fresh context)

## Checks

✓ All required sections present
✓ Recent activity meaningful (78 chars)
✓ Decisions documented (2 decisions with rationale)
✓ Open questions present (1 question with context)
✓ Priorities actionable (3 specific next steps)
✓ Tracker references (4 tickets linked)
✓ Reports linked (HTML, retrospective)

Verdict: PASS - HANDOFF.md update complete and valid.
```
