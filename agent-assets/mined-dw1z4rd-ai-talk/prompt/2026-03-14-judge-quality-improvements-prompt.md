# Plan: 10 Judge Quality Improvements

**TL;DR**: Fix an opening-turn bounds bug, improve divergence framing, and progressively strengthen the judge prompts from per-turn independence through claim-type taxonomy to a fully separate convergence detector. Design tests for each improvement, including a smoke test for the convergence detector.

---

## Phase 1 — Quick Fixes (Issues 1–3)

**1. Parser bounds (the Turn 3 bug)** — Two complementary fixes:
- In `src/lib/live-judge/core.ts` (~line 163), the opening-turn fallback block initializes `logicalCoherence: 50, rhetoricalForce: 50, tacticalEffectiveness: 50` — all above their native-scale ceilings (40/30/30). Change to `20 / 15 / 15` (scale midpoints), leaving `frameControl / credibilityScore / overallScore` at 50 (0-100 scale, correct).
- In `src/lib/live-judge/analysis.ts` `parseJudgeAnalysis()`, add a 3-line defensive clamp directly before building the `scores` object: `Math.min(40,…) / Math.min(30,…) / Math.min(30,…)` — never triggers under correct parsing but catches any future regressed path.

**2. Divergence explanation — drop majority-vote framing entirely**
- Per-turn `totalScore` and pairwise win-count are correlated outputs of the same judge (different granularity, not independent votes). The 2-1 framing is misleading.
- Instead: in `core.ts` `generateNarrativeVerdict()` (~line 493), when `!agreesWithScorecard`, compute whether the win-count leader ≠ the cumulative-points leader across `currentScores`. When they differ, that internal gap is diagnostic ("won exchanges but lost arc, or vice versa").
- Update the `generateConflictResolution` prompt in `analysis.ts` (~line 918) to receive this signal and surface it: *"The two scorecard measures themselves disagree — [X] leads on dimension wins but [Y] leads on total points. This usually means X won exchanges but Y held position better across the arc."*
- Add `scorecardInternallyConsistent: boolean` to `NarrativeVerdict` in `types.ts`.
- Update `src/routes/+page.svelte` (~line 1694): replace the "⚡ Narrative Disagrees" label with "⚡ Narrative Arc Diverges" and append the internal-split note if `!scorecardInternallyConsistent`.

**3. Per-turn score anchoring** — 1-sentence prompt addition in `generateJudgeSystemPrompt()` (`analysis.ts` ~line 1120):
> *"Score this turn entirely on its own merits. Do not anchor to or attempt consistency with previous turns. Each turn recalibrates to zero — smooth score trajectories indicate anchoring bias, not accuracy."*

---

## Phase 2 — Prompt Refinements (Issues 4–7)

**4. Rhetoric standard** — both `generatePairwiseSystemPrompt()` and `generateJudgeSystemPrompt()` RHETORIC sections:
- Add: *"Test: do this turn's rhetorical choices make the argument clearer and more defensible — or do they substitute for argument structure? Vivid delivery that doesn't advance the core claim scores below plain expression that directly develops it."*
- Add a hard cap rule: if Expression quality (Component 1) would push the score above 6 while Framing and Structural Clarity are both weak, Expression cannot override to above 6.

**5. Thesis drift (Tactics-primary / Logic-conditional)** — two coordinated changes in `generatePairwiseSystemPrompt()`:
- **TACTICS section**: add *"Positional consistency: if PREVIOUS ROUND NOTE shows the core claim has materially shifted (not refined) under pressure, penalize −1 for abandoning defensible ground. Refinement = same claim + new mechanism. Drift = different coexisting claim. Contradiction = logically inconsistent with a prior committed position. Drift alone = Tactics −1 only."*
- **LOGIC section**: narrow the existing "Thesis drift: −1" to apply only when drift also produces a logical contradiction: *"Pure drift without contradiction belongs in TACTICS, not LOGIC. Both penalties apply when the drift is also contradictory."*

**6. Symmetric superlative flag (both turns fail)** — TACTICS section of `generatePairwiseSystemPrompt()`:
- Add pre-scoring scan: *"If the motion contains an undefined comparative or superlative ('most', 'greatest', 'best', 'worst', 'more X than'), scan both turns before scoring: did either establish a measurement standard? If neither did, apply −1 to each and describe the structural gap in `tactics_delta`."*

**7. Grounded precision reward** — LOGIC sections of both prompt functions, after the hollow specificity `-1`:
- Add: *"+1 Grounded precision (symmetric counterpart to hollow specificity): a claim that names a specific, verifiable datum AND supplies a mechanism chain linking it to the turn's core argument earns +1. These two bonuses can coexist. The symmetry is explicit: hollow = specificity without mechanism (−1); grounded = specificity with mechanism (+1)."*

---

## Phase 3 — Prompt Architecture (Issues 8–9)

**8. Domain-sensitive evidentiary standards** — expand the "Claim types" paragraph in both LOGIC sections:
- Existing three (conceptual / empirical / normative) stay.
- Add **Phenomenological**: claims about how a phenomenon is experienced or operates in practice (distinct from measurement or definition). Assess whether the argument's model of the phenomenon maps accurately onto observed behavior. Incorrect mapping = −1 unsupported assumption. No empirical measurement required, but accurate phenomenon modeling is.
- Add: *"Classify each major claim before applying standards. Applying empirical requirements to conceptual or phenomenological claims is a scoring error."*

**9. Logic ceiling calibration** — add `--- LOGIC CALIBRATION ANCHORS ---` section to `generateJudgeSystemPrompt()` with **5-6 examples across three anchor bands**:
- **HIGH (36–40)**: specific mechanism present, falsifiable, directly addresses the opponent's load-bearing assumption, all three cause→process→consequence elements — one philosophy/phenomenology example, one empirical/social-science example.
- **MID (24–28)**: correct claim, some mechanism, but missing consequence chain or not engaging the opponent.
- **LOW (16–20)**: assert-only, no mechanism, no consequence.
- *Each labeled with the structural reason* ("scores HIGH because: mechanism falsifiable, addresses opponent's weakest load-bearing claim") not just content.
- Also add brief anchor descriptions (no full examples needed) to `generatePairwiseSystemPrompt()` for relative calibration context.

---

## Phase 4 — Convergence Detector (Issue 10)

**10. Separate LLM call for positional convergence**

**New `PositionalConvergenceAnalysis` interface** in `types.ts`:
```typescript
interface PositionalConvergenceAnalysis {
  detected: boolean;
  convergenceTurnRange: string | null;        // e.g. "Turns 5-6"
  coreClaimAgentA_early: string;              // T1-T2 position
  coreClaimAgentA_late:  string;              // last 2 turns
  coreClaimAgentB_early: string;
  coreClaimAgentB_late:  string;
  positionalGapDescription: string;           // what they still genuinely disagree on
  remainingDisagreementType: "substantive" | "definitional" | "degree" | "none";
  motionViability: "viable" | "degenerate_convergence" | "inconclusive";
}
```
Add `convergence?: PositionalConvergenceAnalysis` to `NarrativeVerdict`.

**New `detectPositionalConvergence()` in `analysis.ts`**:
- Takes full transcript + agent names + topic
- Temperature 0.4, JSON output
- System prompt compares early (T1–T2) vs late (T(n−1)–Tn) positions per agent and determines whether the gap has collapsed to a definitional or degree dispute
- Guard: only run if transcript has ≥ 10 turns (5+ per agent)

**Core integration** in `generateNarrativeVerdict()` `core.ts` (~line 493):
- Run `detectPositionalConvergence` in parallel with the existing rubric harmonization call; 15s timeout
- Attach result to `verdict.convergence`

**Display** in `src/routes/+page.svelte`:
- If `convergence.detected`: show a distinct card below the verdict with turn range, remaining disagreement description, and motion viability verdict

---

## Files to Modify

| File | Changes |
|------|---------|
| `src/lib/live-judge/analysis.ts` | Opening clamp, per-turn independence prompt, rhetoric cap, drift distinction (both sections), symmetric superlative, grounded precision reward, phenomenological claim type, calibration anchors, new `detectPositionalConvergence()` |
| `src/lib/live-judge/core.ts` | Neutral score fix (~L163), scorecard-internal consistency computation, convergence call |
| `src/lib/live-judge/types.ts` | `NarrativeVerdict` extension (`scorecardInternallyConsistent`, `convergence`), new `PositionalConvergenceAnalysis` type |
| `src/routes/+page.svelte` | Divergence label update, convergence banner |
| `src/routes/api/chat/+server.ts` | Pass-through of `convergence` field if callers need it |

---

## Design Decisions

- **Issue 2**: No majority-vote framing. The narrative is the only independent signal; diverge from scorecard and explain arc-level pattern. Scorecard-internal split (wins ≠ points) is a diagnostic, not a vote.
- **Issue 5**: Tactics owns drift; Logic only picks up when drift creates a contradiction with a prior committed position.
- **Issue 9**: Domain-specific calibration examples with explicit structural labels, three domains (philosophy, empirical, technical) per anchor band.
- **Issue 10**: Separate LLM call, not a paragraph addition to the narrative prompt. Guards at ≥10 turns.

---

## Verification Checklist

- [ ] Unit test: `parseJudgeAnalysis` with `logic_score: 50` → must clamp to `logicalCoherence: 40`, not 200
- [ ] Unit test: opening fallback scores — no field exceeds native max
- [ ] Run economics debate through upgraded judge; per-turn Logic scores must vary ≥ 3 points between consecutive turns for the same model (validates anchoring fix)
- [ ] Spot-check rhetoric scores on a vivid-but-weak-structure turn: should not exceed 6 after cap rule
- [ ] Convergence smoke test: ≥ 10-turn debate designed to converge (each agent with ≥ 2 early and ≥ 2 late turns) → `detected: true`, `motionViability: "degenerate_convergence"`
