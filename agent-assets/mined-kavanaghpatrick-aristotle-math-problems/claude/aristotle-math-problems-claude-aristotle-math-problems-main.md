# CLAUDE.md - Math Project

## Mission

**Solve open mathematical problems** by submitting bare conjecture statements to Aristotle and letting it find novel proofs.

We do NOT develop proof strategies. We do NOT write step-by-step proof outlines. We state the open gap, attach prior Aristotle results as context, and submit. Aristotle constructs the proof.

> **Strategy belongs in the airlock companion (`.fusion.json`), NOT in the `.txt` sketch.** The `.txt` sketch states the bare gap (≤30 lines, no proof guidance). When a `.fusion.json` companion is present, `aristotle_informal.py` assembles an informal-mode prompt at submission time, invoking Aristotle's lemma-based reasoner subsystem. This is the documented Harmonic pattern (per arXiv:2510.01346 §3) and was empirically confirmed by the I9 smoke test (May 30 2026, UUID `8d500201-0786-4bb2-8489-2f6aad91be91`) — informal mode produces an "Informal proof:" section + formalization, qualitatively different from BARE-mode output. Canonical reference: `docs/research/aristotle_smoke_test_euclid_may30.md`.

---

## Aristotle System Facts (W-team findings, May 30 2026)

**Aristotle is built by Harmonic AI** (NOT Anthropic). Harmonic is a math-AI startup co-founded by Vlad Tenev (also Robinhood CEO). Endpoint: `https://aristotle.harmonic.fun`. SDK: `aristotlelib` (0.7.0 at the time of the W-team audit; now 2.0.0 — `Project.create`/`create_from_directory`/`ask`, outcome on the latest `AgentTask`).

**Aristotle is a HYBRID solver-formalizer, not a pure formalizer.** It has three subsystems (per arXiv:2510.01346):

1. **Monte Carlo Graph Search (MCGS)** — 200B+ parameter transformer as policy + value function over Lean states. This is the formalizer that fires on bare-gap submissions.
2. **Lemma-based informal reasoning system** — natural-language proof generation, lemma decomposition, autoformalization, Lean REPL feedback loop. This subsystem fires only when given an informal prompt or paired with a strategy.
3. **Yuclid geometry solver** — AlphaGeometry-style; plane geometry only (fired for IMO 2025 P2).

Test-Time Training (TTT): mid-attempt, Aristotle retrains the model on search traces from failed attempts — it literally learns during a single submission.

**Documented benchmarks** (May 2026): IMO 2025 5/6 gold-level (fully verified Lean); ProofBench #1 at 71% (15 points ahead of GPT-5.4 at 56% and Claude Opus 4.7 at 54%); Polya-Szegő 100/100 formalizations.

**Documented novel solves** (Aristotle-credited or paired): E124 (Boris Alexeev, 6 hours, informal-mode bare problem statement); E728 (paired with GPT-5.2 Pro, Jan 2026, first Erdős problem fully resolved by an AI system per arXiv:2601.07421); E481 (Barreto, Aristotle alone); E1026 (Aristotle, formalize-and-extend role); E729 + E401 (derivative). Tao framing: "lowest hanging fruit" — easy-tail Erdős problems, not breakthroughs on famous conjectures.

**Honesty caveat (W7 finding)**: Aristotle proves ~97.6% of theorems it attempts but only ~67% are semantically correct (Igor Rivin). It can "prove the wrong theorem a third of the time, fluently and confidently." Our audit gate (`audit_proven.py`) exists to catch this.

**Calibration**: This project's empirical gap-resolution hit rate is ~0.8% on the harder Erdős long tail. Tao's "long tail" framing applies: easy-tail Erdős = AI sweet spot, deep open problems = expect 0%.

---

## The Pipeline (4 lanes)

Four lanes, depending on what we know about the problem (per I2 schema unification, May 30 2026). The `submissions.lane` column persists the value.

1. **BARE lane** (default) — ≤30-line .txt sketch with the bare open gap. Auto-context attaches prior Aristotle results. INFORMAL .txt. Invokes ONLY the MCGS formalizer subsystem. Historical default for all 1166 pre-May-30 submissions. Hit rate on hard problems: ~0.8%.

2. **CLOSURE lane** — Same ≤30-line bare sketch, paired with a `.closure.json` companion (per `docs/closure_axis_companion_spec.md`). The gate (`check_closure_axis()`) reads the companion and refuses submission unless `real_closure_candidate=true` OR `--rubric-points` is passed. Use for targeting a real-closure outcome rather than a bounded extension.

3. **FUSION lane** — Bare gap + ≤80-line `.fusion.json` companion containing informal strategy + sources (paired-LLM dossier). Airlocked until human review. CLI flag: `--fusion-lane`. The companion captures research-fusion metadata; the MCGS server still runs the formalization.

4. **INFORMAL lane** — Invokes Aristotle's informal-reasoner subsystem directly (W8 finding: this project has historically never used it; active lane as of May 30 2026). CLI flag: `--informal-mode`; sets `informal_mode_used=1`. Use for novel problems where bare-gap submission has returned `compiled_no_advance` and no formal scaffold yet exists.

Lane precedence in `safe_submit()`:
1. `--informal-mode` → `lane='informal'`
2. `--fusion-lane` → `lane='fusion'`
3. Companion has `real_closure_candidate=true` → `lane='closure'`
4. Default → `lane='bare'`

For all four lanes: confirm the gap is open (not in Mathlib, not solved). No proof guidance INSIDE the .txt sketch — sketch stays bare. Strategy lives in the companion JSON, not the sketch.

---

## Sketch Format (bare conjecture, <=30 lines)

```
OPEN GAP: [Problem Name]
Source: [formal-conjectures path or Erdos number]
Domain: [nt / algebra / combinatorics / analysis]

[1-3 sentence English statement of the unsolved conjecture]

theorem problem_name (vars : Types) : conclusion := by sorry

Status: OPEN. [One sentence on what's known]
```

Nothing else. No "Proof Strategy". No "Key Lemmas". No "Proposed Approach". No multiple approaches. No computational evidence. Let Aristotle find the path.

---

## Hard Rules

1. **Every submission targets an OPEN GAP** -- no known results, no infrastructure, no bounded verification of known things
2. **Sketches are bare conjecture statements** -- no proof strategy, no lemmas, no guidance inside the .txt
3. **≤30 lines per sketch (BARE and CLOSURE lanes)** -- enforced by pipeline gate, no override on `.txt` budget
4. **FUSION lane allows ≤80 lines in the companion `.fusion.json`** -- but the `.txt` sketch itself stays ≤30 bare lines. Strategy lives in the companion, not the sketch. Companion is airlocked until human review.
5. **INFORMAL only (.txt)** -- no .lean submissions. Gap-targeting is always INFORMAL
6. **Prior Aristotle results auto-attached as context** -- Aristotle builds on its own work
7. **No override on the gap-targeting gate** -- `check_gap_targeting()` rejection is final
8. **Closure-axis gate**: For the CLOSURE lane, the `.closure.json` companion is read by `check_closure_axis()`. `real_closure_candidate=false` REJECTS unless `--rubric-points` is passed (logs `RUBRIC_POINTS_OVERRIDE`). Spec: `docs/closure_axis_companion_spec.md`.
9. **Falsification is valid gap-targeting** -- "is this gap real?" is a valid question
10. **HAVE FAITH IN ARISTOTLE** -- submit aggressively, fear nothing
11. **Never submit without tracking** -- every submission gets a DB entry
12. **Check DB before submitting** -- `mk failed` and `false_lemmas` table
13. **Cross-domain literature check (NEW, May 30 2026)** -- F2 audit found 0/220 sketches had cross-domain literature attached. Before submitting a `structural-open` target, attach the most recent (≤2 years) literature on the conjecture as part of auto-context. Stale or absent literature is a F2 failure mode.
14. **Process every result** -- `/fetch` or `/process-result`
15. **"compiled clean" != "resolved the gap"** -- only celebrate actual gap resolutions
16. **NEVER state a gap as `(P) ∨ ¬ (P)`** -- that's the law of excluded middle. Aristotle discharges it with `exact em _` in one line and resolves nothing. State the gap as an *existence* claim (`∃ x, P x`) OR an *impossibility* claim (`¬ ∃ x, P x`), never their disjunction. Gate enforces this via `_looks_like_em_tautology()`. Root-cause documented in `docs/research/PILOT_ERDOS850.md`.

---

## Status Enum (Canonical, post-2026-05-28)

The `submissions.status` column takes exactly one of these 5 values. No other strings. The `status_legacy` column preserves the pre-2026-05-28 label.

| Status | Meaning | Entry condition |
|---|---|---|
| `submitted` | Job submitted to Aristotle, not yet returned | Default on insert |
| `compile_failed` | Aristotle returned a Lean file that fails `lake build` | `lake build` exits non-zero |
| `compiled_partial` | Compiles but has residual `sorry` or `axiom` not auto-attached | `sorry_count > 0` OR new `axiom` introduced |
| `compiled_no_advance` | Compiles clean, but the target conjecture is not resolved | `target_resolved=0` (proof avoids the goal) |
| `compiled_advance` | Compiles clean AND the target is genuinely advanced | `contribution_statement NOT NULL` AND `axiomatizes_prior_work=0` AND `target_resolved=1` |
| `disproven` | Aristotle returned a counterexample (the conjecture was wrong) | Counterexample verified |

`compiled_advance` is **opt-in**: the audit phase must affirmatively populate `contribution_statement` and verify `target_resolved=1`. Any of the three conditions failing keeps the row at `compiled_no_advance` or `compiled_partial`.

---

## When to Use Each Lane (decision tree)

```
Is this an OPEN gap (not in Mathlib, not solved)?
├── NO → STOP. Don't submit.
└── YES → Has this problem been submitted before?
    ├── NO → Is it on the easy tail (combinatorics, NT, finite-verification)?
    │   ├── YES → BARE lane
    │   └── NO  → Is the closure mechanism known and explicit?
    │       ├── YES → CLOSURE lane (bare + .closure.json, real_closure_candidate=true)
    │       └── NO  → Do we have a paired-LLM strategy dossier?
    │           ├── YES → FUSION lane (--fusion-lane, .fusion.json airlocked, --paired-llm <name>)
    │           └── NO  → INFORMAL lane (--informal-mode; problem statement only)
    └── YES (prior submissions exist) → What was the last verdict?
        ├── compile_failed       → BARE lane, possibly disprove
        ├── compiled_partial     → BARE lane, narrow the residual
        ├── compiled_no_advance  → FUSION or INFORMAL lane (bare exhausted; engage subsystem #2)
        ├── compiled_advance     → Don't resubmit; advance to the next sub-question
        └── disproven            → Don't resubmit; the conjecture is dead
```

**F-team findings driving this tree** (May 30 2026):
- F1: 57% of historical `compiled_advance` rows were brute-force bounded extensions, not closure (→ `mathematical_content_score` column)
- F2: 0/220 sketches had cross-domain literature attached; the auto-context query was silently broken (I1 fix: query rewrite to artifact-based filter; canary warning; 94 silently-context-less submissions across 7 problems would now attach properly)
- F3: 87% of LLM consultations were meta-process, not math → fix by routing strategy work into the FUSION lane `.fusion.json` companion
- W8: We have never used Aristotle's informal-reasoning subsystem → INFORMAL lane is the lever

---

## Commands

```
/codex-prove <problem>    # Codex proof loop: write Lean 4, iterate against lake build
/sketch <problem>         # Write bare-gap sketch (<=30 lines)

## Proof Orchestrator (autonomous Codex → Aristotle queue)

```
python3 scripts/proof_orchestrator.py enqueue "<problem>" --problem-id <id>  # Add to queue
python3 scripts/proof_orchestrator.py run [--single-pass]                    # Run orchestrator
python3 scripts/proof_orchestrator.py status                                 # Show queue
python3 scripts/proof_orchestrator.py cancel <id>                            # Cancel a job
python3 scripts/proof_orchestrator.py retry <id>                             # Reset to QUEUED
```
/submit <file> [slot]     # Gap-targeting gate -> auto-context -> submit INFORMAL
/sweep [--domain nt]      # Scan for open gaps -> state bare -> submit
/fetch <uuid-or-slot>     # Download result -> audit -> gap-resolution assessment
/status [uuid-or-slot]    # Check Aristotle queue & job status
/screen <problem>         # Binary: OPEN -> submit, NOT OPEN -> skip
/screen-batch <dir>       # Batch screen: OPEN vs SKIP
/audit <file.lean>        # Audit result for gap resolution
/process-result <file>    # Audit local result -> DB
/debate "topic"           # Multi-AI debate to identify the exact open gap
/optimize <file>          # Always: "State the gap bare, submit INFORMAL"
```

---

## math-forge CLI

```
mk search "<query>"          # FTS5 search findings
mk find "<problem_id>"       # All findings for a problem
mk failed [keyword]          # Failed approaches -- check BEFORE sketching
mk context <problem_id>      # Prior Aristotle results for auto-context
mk gaps                      # Open gaps being targeted + status
mk stats                     # Knowledge base dashboard
mk codex [problem_id]        # Codex proof history
mk codex-best <problem_id>   # Best compiled Codex proof path
```

---

## Database

All state in `submissions/tracking.db`:

| Table | Purpose |
|-------|---------|
| `submissions` | All Aristotle jobs. See Status Enum section above for the 5 canonical statuses. `compiled_advance` is opt-in: requires `contribution_statement NOT NULL` AND `axiomatizes_prior_work=0` AND `target_resolved=1`. `status_legacy` preserves the pre-2026-05-28 label. Honesty columns: `axiom_count`, `axiomatizes_prior_work`, `cost_usd`. Sketch-provenance columns: `sketch_model_primary`, `sketch_model_secondary`, `sketch_hash`, `candidate_lemmas_json`, `prior_context_used`, `experiment_arm`. **Closure-axis columns (May 30 2026)**: `closure_axis_json` (TEXT, JSON-serialized CS/CM/CR/HM + `real_closure_candidate`). **Lane columns (May 30 2026, I2 migration)**: `lane` ∈ {`bare`, `closure`, `fusion`, `informal`} (default `bare`; 1166 prior rows backfilled), `informal_mode_used` (0/1; default 0), `paired_llm` (model name or `none`), `fusion_json` (TEXT, JSON dossier metadata for FUSION lane), `mathematical_content_score` (INTEGER 0-10, audit-populated). |
| `submissions_audit` | Read-only view exposing every audit axis on `submissions` in stable column order. Created by `scripts/migrate_add_lane_columns_may30.py`. Use this for cross-cutting audit queries. |
| `codex_proofs` | Codex proof loop results (problem_id, sorry_count, compiled, lean_file) |
| `proof_queue` | Autonomous orchestrator queue (state machine, Codex↔Aristotle loop) |
| `false_lemmas` | Disproven claims -- always check before submitting |
| `failed_approaches` | What doesn't work and why |

Useful queries (use the `submissions_audit` view for cross-cutting columns):

```sql
-- All real-closure candidates submitted in last 7 days
SELECT id, filename, lane, status
  FROM submissions_audit
 WHERE submitted_at >= date('now', '-7 days')
   AND json_extract(closure_axis_json, '$.real_closure_candidate') = 1;

-- Lane breakdown
SELECT lane, COUNT(*) AS n
  FROM submissions_audit
 GROUP BY lane ORDER BY n DESC;

-- Pair-LLM productivity (which strategy LLMs produce real advances?)
SELECT paired_llm, COUNT(*) AS total,
       AVG(mathematical_content_score) AS avg_mcs,
       SUM(CASE WHEN target_resolved = 1 THEN 1 ELSE 0 END) AS resolutions
  FROM submissions_audit
 GROUP BY paired_llm ORDER BY avg_mcs DESC NULLS LAST;

-- Honest advances: compiled_advance with mathematical_content_score >= 5
SELECT id, filename, mathematical_content_score, contribution_statement
  FROM submissions_audit
 WHERE status = 'compiled_advance' AND mathematical_content_score >= 5;

-- Regression candidates: advances that are brute force (mcs <= 2)
SELECT id, filename, paired_llm, mathematical_content_score
  FROM submissions_audit
 WHERE status = 'compiled_advance' AND mathematical_content_score <= 2
 ORDER BY submitted_at DESC;
```

Knowledge base in `math-forge/data/knowledge.db` with FTS5 search.

---

## Hooks

- **SessionStart** (`context-loader.sh`): Injects gap-targeting reminder + queue status
- **PostToolUse** (`lean-validator.sh`): Warns on proof strategy patterns in .txt sketches

---

## When Stuck

1. `mk failed <keywords>` -- already disproven?
2. `mk context <problem>` -- what did Aristotle try before?
3. Try a different problem -- plenty of open gaps
4. Run `/debate` to identify the exact open gap
5. Accept that some problems are too hard right now -- move on
