# Inspect & Amend — Self-Improving Skills Loop

## Trigger
- "Inspect skills", "Check skill health", "Review skill performance"
- "Amend {skill_name}", "Improve {skill_name}"
- "Calibrate skills" — run inspection across all skills
- Automatically suggested when `_logs/_flags.md` has 3+ entries for the same skill

## Purpose
Close the self-improvement loop: observe → inspect → amend → evaluate.
Content generation skills degrade when platforms change algorithms, voice drifts, Brain data grows stale, or audience preferences shift. This skill detects degradation and proposes evidence-based amendments.

## Process

### Phase 1 — Inspect
1. Read all observation logs from `_logs/` for the target skill
2. Read `_logs/_flags.md` for flagged issues
3. Identify patterns:
   - **Rubber Duck failures**: Which phases consistently score low? (e.g., CHALLENGE always fails = weak counterarguments)
   - **Format drift**: A format that used to pass now consistently fails
   - **Angle bias**: System always picks the same angle (contrarian overuse)
   - **Expert mismatch**: Wrong expert library loaded for task type
   - **Decontamination noise**: Same banned patterns keep triggering (instruction unclear)
   - **Brain staleness**: Research skill finds data already in Brain, or Brain data contradicts current reality
   - **Revision loops**: Too many rounds needed — instructions may be ambiguous

4. Generate an **Inspection Report**:
```markdown
## Inspection Report: {skill_name}
**Date**: {YYYY-MM-DD}
**Observation window**: {date range}
**Total runs observed**: {N}
**Pass rate (Rubber Duck 8+)**: {N}%
**Avg revision rounds**: {N}

### Patterns Detected
1. {Pattern with evidence — cite specific log entries}
2. {Pattern with evidence}

### Root Cause Analysis
- Is the issue in the skill instructions?
- Is it in the reference files (practices, expert libraries)?
- Is it in the Brain data (stale models, missing evidence)?
- Is it in the routing (wrong skill triggered)?

### Recommendation
{Amend skill | Update reference | Refresh Brain section | Adjust routing | Monitor}
```

### Phase 2 — Amend
If inspection recommends amendment:

1. **Read the current SKILL.md** for the target skill
2. **Propose a specific change** — one of:
   - Tighten angle selection criteria
   - Add missing generation step
   - Update format constraints (character counts, structure)
   - Adjust Rubber Duck phase weights or criteria
   - Update expert library loading rules
   - Add/remove decontamination patterns
   - Clarify ambiguous instructions causing revision loops
   - Update Brain loading priorities

3. **Version the current skill before changing**:
   - Create `skills/{skill_name}/_versions/` if it doesn't exist
   - Copy current `SKILL.md` → `_versions/v{N}.md`
   - Write amendment rationale to `_versions/_changelog.md`:
     ```
     ## v{N+1} — {YYYY-MM-DD}
     **Trigger**: {What pattern triggered this amendment}
     **Change**: {What was changed and why}
     **Evidence**: {Log entries that support this change}
     **Expected improvement**: {What metric should improve}
     ```

4. **Present the proposed diff to the user** for approval
   - Show exact lines changed
   - Explain the evidence chain: logs → pattern → root cause → fix
   - Never apply without user confirmation

### Phase 3 — Evaluate
After amendment is applied:

1. Mark in `_logs/_flags.md`:
   ```
   - [EVAL] {skill_name} v{N+1} applied {date} — monitoring
   ```

2. After 3-5 subsequent runs, compare:
   - Rubber Duck pass rate before vs. after
   - Avg revision rounds before vs. after
   - Phase-specific scores before vs. after
   - Decontamination trigger frequency

3. Generate **Evaluation Report**:
   ```markdown
   ## Evaluation: {skill_name} v{N+1}
   **Amendment date**: {date}
   **Runs since**: {N}
   **Result**: Improved | No change | Degraded

   ### Metrics Comparison
   | Metric | Before | After |
   |--------|--------|-------|
   | Pass rate | {x}% | {x}% |
   | Avg revisions | {x} | {x} |
   | Weakest phase | {x} | {x} |

   ### Decision
   {Keep | Roll back to v{N}}
   ```

4. If degraded: restore from `_versions/v{N}.md`, log the rollback

## Amendment Thresholds
- **Trigger threshold**: Only propose amendment when Rubber Duck first-attempt pass rate drops below **50%** over 10+ runs, OR when 3+ flags accumulate for the same skill
- **Improvement bar**: An amendment must improve the pass rate by at least **15 percentage points** OR reduce average revision rounds by at least **1 round**
- **Revert rule**: If an amended skill doesn't improve the primary metric within **5 subsequent runs**, auto-revert. No exceptions.
- **Cooldown**: After a revert, wait for **3 clean runs** before proposing a new amendment to the same skill

## Rules
- Never amend without inspection evidence
- Never apply without user approval
- Always version before amending
- One amendment per cycle — don't stack changes
- Evaluate before proposing next amendment
- Smallest change that addresses the pattern
- If root cause is in references (not skill), update the reference file instead
