---
name: white-box-trace
description: White-box code-path tracing in two modes. REAL — empirical verification of completed code via CFG/MPC traversal, Counterfactual + optional Live Mutation Testing, PBT hook, Tandem-FL on FAIL, Killer-Path-First, FAIL-FAST, persistent index-prefixed JSONL trace with resume + confidence decay, Reviewer Agent re-rank, Reflexion lessons, structured fix_proposal + repro_snippet. VIRTUAL — pre-implementation falsification of RCA reports / Implementation Blueprints / Plans / freeform ideas via Planner-Simulator, POPPER falsification-first, LTL plan consistency, cross-artifact drift detection, defended against Mental-Reality Gap. Use WHEN user says /trace, /trace.real, /trace.virtual, /verify-plan, "verify this code", "trace these paths", "check coverage", "verify this plan", "falsify my RCA", "is this blueprint sound", "will this implementation work", "will my fix work", "white-box tracing", "mutation testing", "CFG analysis", "MPC", "SBFL", "Tandem-FL", "fault localization". Investigation only — never modifies source. Anti-hallucination (Citation-Grounded re-read, Mutation Counterfactual, CoVe, Disconfirmation-First, Sycophancy guard); declares INCONCLUSIVE rather than fabricate. Do NOT use for fix implementation (/bug.fix), root-cause investigation (/bug.why = root-cause-analysis skill), or distributed tracing (B-085).
allowed-tools: Read, Glob, Grep, Bash, Agent, WebSearch, WebFetch
---

# White-Box Trace (REAL + VIRTUAL)

> **MISSION**: prove correctness — of code that exists (REAL) or of an artifact describing code that does not yet exist (VIRTUAL) — by **falsifying** every conclusion before declaring it. Investigation only. NO source modification. Skipping any MANDATORY gate ⇒ INVALID DELIVERABLE → REDO.

> **Layering**: skill = trace-specific layer over `CLAUDE.md`. Cite §N — DO NOT duplicate. CLAUDE.md provides Tier (§3), Checkpoint (§4), Evidence ladder (§4.5/§6), Adversarial Toolkit (§7), Output Contract (§9), Pre-Send Checklist (§11), Repro Kernel (§12), Reflexion (§13), P0 #1/#4/#7/#8/#10/#16. **Read CLAUDE.md FIRST.**

---

## 0. Hard rules — VIOLATING ANY ⇒ INVALID DELIVERABLE → REDO

1. **No source modification.** NEVER `Edit` or `Write` production code. Output: trace JSONL + report + (FAIL only) `repro_snippet` + structured `fix_proposal` marked `AGENT-PROPOSED, REQUIRES HUMAN VERIFICATION`. Fixes consumed by `/bug.fix`.
2. **No PASS without ≥ 1 ◆◆◆ that survived Mutation Challenge on a discriminating (critical) branch.** "Should work", "looks correct", "code reaches the line" are NOT evidence. REAL: live mutant kill OR counterfactual mutation. VIRTUAL: artifact-grounded counterfactual on the proposed logic.
3. **Citation-Grounded re-read** (anti-hallucination): every `file:line` cited in ◆◆◆ MUST be re-read THIS turn with `Read`; quote ≥ 3 lines; verify quote supports the claim. Hallucinated citation ⇒ downgrade ◆◆◆ → ◆○○; recompute verdict.
4. **No HIGH+ verdict without a Refuter** (CLAUDE.md P0 #8). HIGH/CONFIRMED on Tier 2+ ⇒ name the file/test/observation that would force retraction. Missing Refuter ⇒ downgrade to MEDIUM.
5. **INCONCLUSIVE is a valid verdict.** Honest "need [X], because [Y]" beats fabricated PASS/FAIL. Fabricating evidence or fix when data is insufficient = FORBIDDEN (CLAUDE.md P0 #7).
6. **Data security** (CLAUDE.md P0 #10): any data-access path ⇒ check authorization scope. Auto-Tier 3 if data-leak class.
7. **Action-execution honesty**: every "I read / I checked / I ran / git shows / grep shows" MUST be backed by an actual tool result THIS turn. Otherwise prefix `**ASSUMPTION**:`.
8. **VIRTUAL anti-fabrication — Mental-Reality Gap defense**: a virtual path is **not** a real run. Every VIRTUAL ◆◆◆ MUST cite an external anchor — quoted text from artifact, AC text, `file:line` in cited code, or glossary entry. Pure "I imagined the code would do X" is ◆○○, NEVER ◆◆◆. Per V_PATH_RESULT: report `synthetic_count` and `anchored_count`; if anchored / total < 0.50 ⇒ V_INCONCLUSIVE.
9. **Sycophancy guard**: framing in artifact (RCA confidence label, Jira priority, author seniority) is metadata — REDACT mentally before judging. Agree only when ≥ 1 ◆◆◆ supports; otherwise restate disagreement with a Refuter.
10. **YAGNI** (CLAUDE.md P0 #4): trace ONLY paths in scope of artifact + blast radius. NEVER trace whole codebase. NEVER refactor / "modernize" the artifact under review.

---

## 1. Mode selection — DECIDE FIRST (before any phase)

The Checkpoint header (§4 of CLAUDE.md) MUST declare `Mode: REAL | VIRTUAL` on the FIRST visible response. Wrong mode = wrong evidence rules = INVALID.

```
Code file / commit / completed feature / *.cs / *.py / *.ts diff
  → REAL (Phases 1R–9R)

Artifact: RCA-*.md | IMP-*.md | PLAN-*.md | FIX-*.md | SPEC-*.md | ADR-*.md
  | freeform plan / pseudocode / "we will do X"
  AND code-not-yet-written-or-only-partially-modified
  → VIRTUAL (Phases 1V–8V)

Both: code exists AND user explicitly asks "also check the plan"
  → REAL first; chain VIRTUAL on plan deviations only (split into two reports)

Ambiguous / user did not say which → ASK USER. Do not assume.
```

**Mode is sticky.** Never silently switch mid-run; emit a new report.

---

## 2. Phase 0 — Common Pre-Execution (BOTH modes)

| Step | Action |
|------|--------|
| 0.1 Path discovery | `Glob("**/Domain_Glossary.md")` → `DOCS_ROOT`; `Glob("**/LOCAL-MEMORY")` → `OUTPUT_ROOT`. Forward slashes, absolute. |
| 0.2 Param validation | Empty input ⇒ exit. Jira `[A-Z]{2,10}-\d+` → `mcp__claude_ai_Atlassian__getJiraIssue`. Markdown artifact → `Read`. Folder → `Glob`. |
| 0.3 Capability probe | `which {YOUR_MUTATION_TEST_TOOL}` (mutation_available); `import hypothesis` or `{YOUR_TEST_RUNNER} --filter Property` (pbt_available); `Glob("**/.codegraph/*.db")` (ckg_available); detect runner. Cache once per session. |
| 0.4 Requirements pre-flight | Load `requirements-analysis` (when present). Classify Task / Bug / Both. Normalize each AC to **EARS**: "When `<trigger>`, the `<system>` shall `<action>`". Produce **GWT** per AC. Assign canonical **`req_id`**. Open Questions with ⚠️ ASSUMPTION per gap. **`open_questions.critical > 0` ⇒ ASK USER** before Phase 1. |
| **0.4.5 Architecture Pre-Read (MANDATORY when ANY of:** scope crosses ≥ 3 architectural layers (DB → ORM → Domain → Core/Services → Web/API → UI) · touches `Core/`, domain layer, `{YOUR_SERVICE_LAYER}`, `{YOUR_DATA_ACCESS_LAYER}` · security boundary · data-integrity class **)** | `Read` `context/01_Solution_Overview/Project_Overview.md` AND `context/03_Projects/{ProjectName}.md` when applicable. Record: layer-boundary the data crosses · governing patterns (F/B/D-XXX from `Code_Patterns_Index.md`) · invariants the boundary enforces. **Skipping ⇒ INVALID DELIVERABLE → REDO** — without architecture context every PATH_PASS confirms only local correctness while missing inter-layer contract violations (FM-6). |
| 0.5 Reflexion memo load | `OUTPUT_ROOT/CURRENT_TASK/TRACE-LESSONS-{task-slug}.md` exists ⇒ inject "Prior lessons to avoid: …" into Phase-3 prompts. |
| 0.6 Trace file (REAL) | `OUTPUT_ROOT/CURRENT_TASK/TRACE-{task-slug}-{YYYYMMDD}-{HHmm}.jsonl`; existing ⇒ parse SCHEMA + HEADER + index-prefixed lines, recompute `pass_file_hash`, queue `DECAY_QUEUED` and `INTERRUPTED` (§8.3). |
| 0.7 Report file (VIRTUAL) | `OUTPUT_ROOT/CURRENT_TASK/V-TRACE-REPORT-{artifact-slug}-{YYYYMMDD}-{HHmm}.md`; optional sidecar `V-TRACE-{artifact-slug}-{YYYYMMDD}-{HHmm}.jsonl`. |
| 0.8 Output Checkpoint | Per CLAUDE.md §4. **MUST include**: `Mode: REAL\|VIRTUAL`, `Tooling probe: mutation=… pbt=… ckg=…`, `Path budget: tier-aware`, `Lessons memo: loaded:Y/N entries:N`, `Architecture Context: <layer-boundary; governing F/B/D-XXX; invariants>` **[when 0.4.5 fires; otherwise N/A]**, `Critical Insight`, `Killer Hypothesis` (REAL = most-likely-broken HAPPY; VIRTUAL = most-likely-falsifiable claim), `Refuter`, `Confidence`. **Confidence < MEDIUM ⇒ ASK USER** before Phase 1. |

**STOP rules**: max 30 paths/run (`--max-paths` overrides); per-path adaptive budget = `4_000 × (1 + cyclomatic_complexity / 5)` tokens; 3× consumed ⇒ `PATH_DEFERRED{reason: "budget exhausted"}`. **Tier-aware default budget**: T0=8, T1=15, T2=25, T3=40 paths.

---

## 3. REAL mode — Phases 1R–9R

### 3.1 Phase 1R · CFG Construction (MODE=NEW)
- Identify target files/methods (load `codebase-search-protocol`; if `ckg_available`, switch to `MATCH (m:METHOD)-[:CALLS*1..3]-(n)` query).
- Build CFG: `if`/`switch`/`try-catch`/loops/early return/throw. Apply **MPC** — minimum paths covering every statement (C0) and every branch T/F (C1). Path cap = `min(--max-paths, cyclomatic × 3)`. ≥ 5 branches ⇒ prioritize critical business branches (validation, authorization, permissions, exceptions). Loop policy: 0/1/N iterations.
- Categorize HAPPY / NEGATIVE / EDGE; adversarial stance on NEGATIVE — actively seek failure modes.
- Write `CFG_SUMMARY` + one `PATH` record per path: `id` (P001…), **`req_id`** MANDATORY, `category`, `description`, `entry`, `branches`, `status=PENDING`, `shared_prefix_hash`, `killer` (boolean).
- **Killer-Path-First election**: among HAPPY, mark exactly one `killer=true` — highest-cyclomatic node, newest code (≤ 7 d via `git log`), layer-boundary crossing, recently-fixed area (per memo / `git blame`). Killer is traversed FIRST.

### 3.2 Phase 2R · Resume
`pending = all_paths − completed − INTERRUPTED − DEFERRED − DECAY_QUEUED`. Write `RESUME_START` (with `lessons_memo_hash`).

### 3.3 Phase 3R · Per-Path Protocol — order: Killer HAPPY → other HAPPY → NEGATIVE → EDGE
1. **Stale context check** — re-read entry + key branch lines; mismatch ⇒ `PATH_DEFERRED`, queue.
2. Write `PATH_START`.
3. Read entry / branches / exit (`codebase-search-protocol` or CKG).
4. Set context (input data, expected behavior from `req_id`).
5. **Trace** — per step write `PATH_EVIDENCE` (file, line, quoted_code, weight ◆◆◆ / ◆◆○ / ◆○○, supports). External lib / API / CVE ⇒ `web-search-protocol`, ◆◆○ + cite URL. **Inter-path coverage propagation** — `shared_prefix_hash` matches earlier PASS path ⇒ reuse prefix evidence as ◆◆○ (one-step downgrade); collect fresh ◆◆◆ on divergent suffix only.
6. Verify postcondition (return value / side effect / exception).
7. **Mutation Challenge — counterfactual (MANDATORY)**: per ◆◆◆ apply ≥ 3 mutations (condition flip `≤ → <`, off-by-one `i<n → i<=n`, wrong enum, swap operand, wrong source). ALL mutants would still produce PASS ⇒ downgrade ◆◆◆ → ◆◆○ (non-discriminating). ≥ 1 mutant clearly fails ⇒ keep ◆◆◆. Record `mutation_tested=true`, `mutation_outcome ∈ {killed, survived}`. **Absent fields = INVALID PATH_RESULT — REDO.** PATH_PASS REQUIRES ≥ 1 ◆◆◆ that survived.
8. **Live Mutation (`mutation_available && --mutation∈{live,hybrid}`)** — `{YOUR_MUTATION_TEST_TOOL} --since=HEAD~1 [scoped to changed files only — NEVER prod]`. Killed mutants ⇒ ◆◆◆ empirical. Survivors ⇒ `coverage_gap`; PATH_PASS REQUIRES `mutation_kill_rate ≥ 0.75` on changed lines.
9. **PBT (`pbt_available && --pbt=on && path.has_invariant`)** — property-based test on path invariants × 100. All pass ⇒ ◆◆◆+ (strongest). Any fail ⇒ minimal counterexample = `repro_snippet`; STATUS=FAIL.
10. **Agentic Concolic (≥ 3 chained boolean conditions)** — natural-language constraint summarization; ask "exists input violating this path's expectation while satisfying all conditions?". Constructive counterexample ⇒ STATUS=FAIL with input as `repro_snippet`.
11. **Discriminating-evidence rule**: ≥ 1 PASS ◆◆◆ MUST be on this path's **critical branch** (the branch distinguishing this path from a CFG sibling). All ◆◆◆ in shared prefix only ⇒ STATUS=FAIL, `failure_reason="no discriminating evidence"`.
12. **Evidence Re-Read Gate (CoVe, MANDATORY)** — per ◆◆◆ → `Read` exact `file:line`, quote ≥ 3 lines, verify quote supports claim. Use **targeted phrasing only**: "Does the quoted code support this step's claim?" — NEVER "find all your mistakes" / unbounded critique. Failure ⇒ downgrade or STATUS=FAIL. **Absent gate = INVALID PATH_RESULT — REDO.**
13. Output to chat: `#### Path P00X Verdict: PASS | FAIL — [one phrase: why]`.
14. Write `PATH_RESULT` (status, verdict, evidence_count, strong_evidence, mutation_tested, mutation_outcome, mutation_kill_rate, pbt_applied, pbt_passed, **`pass_file_hash`**, failure_location, failure_reason, **`repro_snippet`** 5–15 lines, **`fix_proposal`** structured JSON, `reviewer_disagreement`).
15. Write `COVERAGE`.

**FAIL-FAST**: first HAPPY=FAIL ⇒ `FOOTER{status=FAIL_FAST}`, skip remaining HAPPY/NEGATIVE/EDGE, jump to Phase 6R + 7R + 9R.

**Proof-of-Negative**: HAPPY=FAIL ∧ (NEGATIVE=PASS ∨ EDGE=PASS) ⇒ write `PROOF_OF_NEGATIVE` — regression-class signature.

### 3.4 Phase 4R · Coverage
Statement C0 ≥ 80%; Branch C1 ≥ 70%; Mutation kill rate ≥ 75% (live); HAPPY 100% / NEGATIVE 80% / EDGE 60%. **Discriminating-coverage gate**: every covered `req_id` MUST have ≥ 1 PASS path with ◆◆◆ that survived mutation AND on its critical branch — otherwise the req moves to `non_discriminating_requirements` and verdict ≥ ISSUES.

### 3.5 Phase 5R · Blast Radius
Trigger: public/shared method, domain entity/DB schema, cyclomatic > 3. Forward-slice; add BLAST_RADIUS paths to plan; same per-path protocol.

### 3.6 Phase 6R · Failure Diagnosis (FAIL paths only)
**Error Propagation Table (MANDATORY)** — Hop | Layer | File:Line | Component | Expected | Actual | Valid? | Note — from `failure_location` (Hop 0) to **Corruption Point** (first ✅→❌ flip) to **Root Cause**. Depth: 2–3 single-method, 4–6 cross-layer, max 8. **Tandem-FL** (4+ hops or value-propagation): SBFL Ochiai top-N → dynamic backward slice from `(failure_location, failing_var)`. `ROOT_CAUSE_BOX` references the table by Hop. `repro_snippet` (5–15 lines, runnable) + structured `fix_proposal` MANDATORY.

### 3.7 Phase 7R · Reviewer Agent Pass
Trigger: `--reviewer-agent=auto` ∧ ≥ 1 FAIL path. Spawn `Agent` (subagent_type: Explore) with **isolated context** (no Debugger contamination): "Re-rank the top-N suspicious lines from Tandem-FL. Are any clear red herrings? Is the true root cause possibly outside this set?" Disagreement ⇒ `reviewer_disagreement` field; both rankings in report §5; verdict = consensus or `ISSUES_REVIEW_CONFLICT` if conflict + similar confidence.

### 3.8 Phase 8R · Final Verification (CHAT ONLY — never saved)
1. **Contradiction Detector** (CLAUDE.md §11.9 — seven types) + new types: mutation gap (live mode but kill_rate < 0.75), discriminating gap (any req in `non_discriminating_requirements`), reviewer conflict.
2. **CoVe micro-check** — Draft → Verify ("does every PASS have ≥ 1 ◆◆◆ mutation_tested=true on critical branch?" — filter PATH_RESULT + PATH_EVIDENCE) → Synthesize. No ⇒ downgrade.
3. **Disconfirmation-First on PASS** — MUST output in chat: "Disconfirmation check: <single most likely reason this PASS is wrong>. Result: <holds | falsified>." Falsified ⇒ downgrade. **Absent line = REDO.**
4. **Self-Consistency vote** (borderline only) — one PASS barely survived mutation OR coverage within 5% of threshold ⇒ re-traverse that path 3× with fresh seeds; majority verdict; record `SELF_CONSISTENCY_VOTE`.
5. **Sycophancy guard** — re-read artifact framing; flag any "HIGH confidence" / "trivial fix" / "should already work" not backed by evidence.
6. **Pre-Send Checklist** (CLAUDE.md §11) — all 12 items.
7. Write `FOOTER`. On FAIL retry, write **Reflexion memo** → `TRACE-LESSONS-{task-slug}.md`: "What was hypothesized PASS but FAILed; branch most underestimated; mutation that killed strongest evidence; tip for next attempt".

### 3.9 Phase 9R · Report
`TRACE-REPORT-{task-slug}-{YYYYMMDD}-{HHmm}.md` per `report-template.md` §B (Sections 0–11). **Phase 8R outputs NEVER in saved files — chat only.**

---

## 4. VIRTUAL mode — Phases 1V–8V

> **VIRTUAL ≠ REAL.** No code is run. The artifact is the unit of analysis. Evidence = **artifact-grounded** (quoted text + cited `file:line` if any) — NOT "I imagined the code did X" (= ◆○○ or `**ASSUMPTION**:`). Mental-Reality Gap is the central anti-pattern (§0 rule 8).

### 4.1 Phase 1V · Artifact Ingestion
Identify type: **RCA / IMP / PLAN / FIX / SPEC / ADR / freeform**. `Read` the artifact in full. Extract:
- RCA: proposed Root Cause + Invariant + Repro Spec + Primary Fix Box + Hypotheses table.
- IMP/Plan: target files, target methods, declared logic, ACs, invariants, security claims.
- Freeform: convert to EARS+GWT (Phase 0.4).

`fingerprint = sha256(artifact_text || referenced_file:line_content_currently_on_disk)`.

### 4.2 Phase 2V · Virtual CFG Construction (Planner-Simulator)
- Build a CFG **of the intended logic** from the artifact text — not from existing code (which may not exist). Branch points come from the artifact's stated conditions, validations, error handling, loops.
- Artifact references existing files (`file:line`) ⇒ `Read` them — they are real anchors. Mark each CFG node **anchored** (real code) or **synthetic** (only described).
- Apply MPC; categorize HAPPY / NEGATIVE / EDGE; assign **`req_id`** per AC.
- Emit `V_CFG_SUMMARY`, `V_PATH` records (schema mirrors REAL `PATH` plus `kind="virtual"`, `anchored:[file:line list]`, `synthetic_branches:[…]`).

### 4.3 Phase 3V · Virtual Path Traversal — order: Killer-AC-First → other ACs → negative ACs → edge ACs
1. Write `V_PATH_START`.
2. State the precondition + AC literal text the path is supposed to satisfy.
3. Walk the artifact's stated logic step-by-step; per step write `V_PATH_EVIDENCE`:
   - Quote the artifact text (`source: artifact`, `line_in_artifact: N`) → ◆◆○ baseline.
   - Step references existing code (`file:line`) ⇒ `Read`, quote ≥ 3 lines, verify support → ◆◆◆ (anchored).
   - Pure inference ("the developer probably meant X") → ◆○○; NEVER PASS-grade.
4. **AC satisfaction check** — does the walked logic *necessarily* produce the AC's expected output under the stated precondition? Yes / No / Unknown.
5. **Virtual Mutation Challenge (artifact-grounded)** — apply ≥ 3 mutations *to the artifact's stated logic*: flip a condition the artifact describes, drop a validation step it lists, swap order of stated calls, weaken an invariant. Mutated logic still satisfies AC ⇒ artifact is **under-specified** (non-discriminating); downgrade ◆◆◆ → ◆◆○ and add an Open Question. Mutation breaks AC ⇒ keep ◆◆◆.
6. **Cross-artifact drift check** — parent exists (RCA → IMP, IMP → SPEC) ⇒ every claim MUST be consistent with parent. Drift ⇒ `V_DRIFT` record; verdict ≥ V_ISSUES.
7. **LTL-style consistency** — convert path's stated steps to ordered logical predicates: `step₁ ⇒ step₂ ⇒ … ⇒ AC`. Inconsistency / ordering bug ⇒ STATUS=V_FAIL with the contradiction printed.
8. **Mental-Reality Gap audit (MANDATORY)** — name explicitly which steps are **anchored** vs **synthetic**. > 50% synthetic ◆◆◆ in this path ⇒ downgrade to V_INCONCLUSIVE, reason "Verification Gap — too much imagined trace, not enough reality".
9. **Citation-Grounded re-read** (§0 rule 3) — every cited `file:line` re-read THIS turn.
10. Output to chat: `#### V-Path V00X Verdict: V_PASS | V_FAIL | V_INCONCLUSIVE — [phrase]`.
11. Write `V_PATH_RESULT` (+ for V_FAIL: `repro_snippet_pseudocode` 5–15-line input violating AC under artifact logic; `fix_proposal_to_artifact` — what to add/edit IN THE ARTIFACT, NOT in code).

### 4.4 Phase 4V · POPPER Falsification-First
For each surviving V_PASS hypothesis (proposed root cause / proposed plan path), name the **single most discriminating mental experiment** that would falsify it. Run it (mentally + grounded in artifact). Survives ⇒ keep V_PASS. Falls ⇒ V_FAIL. Cannot design ⇒ V_INCONCLUSIVE.

### 4.5 Phase 5V · Cross-Artifact Consistency
4-column table: Claim | Source artifact (RCA/IMP/SPEC) | Conflicts with | Severity. Drift on Root Cause / Invariant / AC / `file:line` target ⇒ V_ISSUES. Output feeds `/bug.fix` or `/howto.implement` so they don't act on stale plan.

### 4.6 Phase 6V · Virtual Coverage + AC Map
| Coverage | Min |
|----------|-----|
| AC coverage | 100% — each AC has ≥ 1 V_PASS path with discriminating ◆◆◆ |
| Anchored evidence ratio | ≥ 50% of V_PASS ◆◆◆ are anchored (`file:line`) |
| Synthetic-only paths | ≤ 30% — else V_INCONCLUSIVE |
| Auth scope | 100% on every data-touch path |

### 4.7 Phase 7V · Final Verification (CHAT ONLY)
Same gates as REAL Phase 8R (Contradiction Detector, CoVe, Disconfirmation-First on V_PASS, Sycophancy guard, Pre-Send Checklist) **plus Mental-Reality Gap final audit** (anchored-vs-synthetic ratio across whole report).

### 4.8 Phase 8V · Report
`V-TRACE-REPORT-{artifact-slug}-{YYYYMMDD}-{HHmm}.md` per `report-template.md` §C (Sections V0–V11). **Output IS the deliverable — never modify the source artifact.**

---

## 5. Shared Evidence Framework

| Weight | Symbol | REAL rule | VIRTUAL rule |
|--------|--------|-----------|--------------|
| STRONGEST | ◆◆◆+ | Direct read `file:line` + quoted_code + survived **live** mutation + PBT properties hold | Direct quote from artifact + verified `file:line` anchor + survived virtual mutation + LTL consistent |
| STRONG | ◆◆◆ | Direct read `file:line` + quoted_code + survived **counterfactual** mutation on critical branch | Direct quote from artifact + verified `file:line` anchor + survived virtual mutation |
| MODERATE | ◆◆○ | Inferred from related code; or ◆◆◆ where mutation survived but did not kill | Quote from artifact only (no code anchor); or step where artifact + glossary agree |
| WEAK | ◆○○ | Assumption / analogy; **NEVER** allowed for PATH_PASS | Pure inference / "the developer probably meant"; **NEVER** allowed for V_PATH_PASS |

**No ◆◆◆ ⇒ no PASS.** **No ◆◆◆ that survived Mutation Challenge on critical branch ⇒ no PASS.** **VIRTUAL: anchored ◆◆◆ ratio < 0.50 ⇒ V_INCONCLUSIVE.**

---

## 6. Anti-Hallucination Gate Stack — run all in chat, never in saved files

| Gate | When | Defends against |
|------|------|-----------------|
| **Citation-Grounded re-read** | Per ◆◆◆, before any PASS | Fabricated `file:line`, out-of-range citation |
| **Mutation Counterfactual** | Per ◆◆◆, before PATH_PASS / V_PATH_PASS | Non-discriminating evidence; FL fragility |
| **CoVe micro-check** | Before final verdict | Hallucinated trace, fact drift |
| **Disconfirmation-First on PASS** | Before final PASS — chat output MANDATORY | Confirmation bias, overconfidence |
| **Sycophancy guard** | Before final verdict | Adversarial framing, false-PASS |
| **Self-Consistency vote** | Borderline only | Single-trace luck |
| **Mental-Reality Gap audit** (VIRTUAL) | Before V_PASS | Imagined-trace self-affirmation loop |

---

## 7. Verdict Matrix

| Mode | Verdicts (best → worst) |
|------|------------------------|
| REAL | PASS · PASS_WITH_NOTES · ISSUES · ISSUES_REVIEW_CONFLICT · FAIL · FAIL_FAST |
| VIRTUAL | V_PASS · V_PASS_WITH_NOTES · V_ISSUES · V_INCONCLUSIVE · V_FAIL |

**Completion gates** (PASS / V_PASS):
- All planned paths resolved.
- HAPPY / NEGATIVE / EDGE (REAL) or AC (VIRTUAL) covered.
- `unverified_claims == 0`; `uncovered_requirements == 0`; `non_discriminating_requirements == 0`.
- (REAL live) `mutation_kill_rate ≥ 0.75`.
- (VIRTUAL) `anchored_evidence_ratio ≥ 0.50`.
- All §6 gates passed.

---

## 8. Output paths + JSONL format

### 8.1 Paths (forward slashes, absolute)
- REAL trace: `OUTPUT_ROOT/CURRENT_TASK/TRACE-{task-slug}-{YYYYMMDD}-{HHmm}.jsonl`
- REAL report: `OUTPUT_ROOT/CURRENT_TASK/TRACE-REPORT-{task-slug}-{YYYYMMDD}-{HHmm}.md`
- VIRTUAL report: `OUTPUT_ROOT/CURRENT_TASK/V-TRACE-REPORT-{artifact-slug}-{YYYYMMDD}-{HHmm}.md`
- VIRTUAL JSONL (optional): `…/V-TRACE-{artifact-slug}-{YYYYMMDD}-{HHmm}.jsonl`
- Lessons memo (BOTH): `…/TRACE-LESSONS-{task-slug}.md`
- BUG-* / STORY-* subfolders override `CURRENT_TASK` when artifact lives there.
- YAML frontmatter MANDATORY per CLAUDE.md §9: `artifact_type: TRACE | V-TRACE | LESSON`, `producer: claude-code`, `state: draft|verified|superseded`, `inputs_consumed[]`, `fingerprint`, `tier`, `targets_failure_modes`, `verification` block.

### 8.2 JSONL — Index-Prefix Append (only allowed format)
```
0001:{"type":"SCHEMA","version":"2.1","mode":"REAL|VIRTUAL","resume_format":"index-prefix","mutation_mode":"…","pbt_mode":"…"}
0002:{"type":"HEADER","task_ref":"…","task_fingerprint":"sha256:…","target_files":[…],"created":"…","session_id":"…"}
NNNN:{"type":"PATH_START|PATH_EVIDENCE|PATH_RESULT|COVERAGE|PROOF_OF_NEGATIVE|SELF_CONSISTENCY_VOTE|RESUME_START|FOOTER", …}
```
Append protocol: `next_seq = max(existing_seq) + 1`; line begins with `NNNN:`. Resume parse: split lines → parse `seq:json` → sort by seq → filter `PATH_RESULT` → `{path_id, status, pass_file_hash}`. Variant-C marker (legacy) is **DEPRECATED — FORBIDDEN in new traces**.

### 8.3 Resume table
| Path status | Action |
|-------------|--------|
| PASS, hash unchanged | Skip |
| PASS, whitespace-only diff | Skip + stale-warn |
| PASS, code diff | DECAY_QUEUED → re-traverse |
| FAIL, target unchanged | Skip |
| FAIL, target changed | Re-check |
| INTERRUPTED / DEFERRED / DECAY_QUEUED / PENDING | Traverse |

---

## 9. Tool / skill usage

| Situation | Action |
|-----------|--------|
| Searches / file location | `codebase-search-protocol` (CLASSIFY → LOCATE → FILTER → SCAN). |
| 8-method theory / formulas / scientific anchors | `reference.md` — never inline. |
| Deep RCA on FAIL | Hand off to `root-cause-analysis` (`/bug.why`); pass trace + Error Propagation Table. |
| Implementation after V_PASS | Hand off to `/howto.implement`; pass V-TRACE report. |
| Fix application after FAIL | Hand off to `/bug.fix`; pass trace + `fix_proposal` JSON + `repro_snippet`. |
| Multi-layer (≥ 3 layers) | Spawn `Agent` (subagent_type: Explore) per layer; main agent writes (CLAUDE.md §14). |
| Jira / Confluence | Atlassian MCP (`mcp__claude_ai_Atlassian__*`). |
| External library / CVE | `WebSearch` then `WebFetch` known URL — ◆◆○ MODERATE; cite source URL. |
| Mermaid CFG / Error Propagation | `mermaid-diagrams`. |

---

## 10. Anti-Patterns — FORBIDDEN

| ❌ | ✅ |
|----|----|
| Modify source code | Read only — output trace + report |
| PASS without ◆◆◆ on critical branch | ≥ 1 ◆◆◆ on the discriminating branch |
| ◆◆◆ without Mutation Challenge | Counterfactual ≥ 3 mutations + (when available) live |
| "Should work" / "looks correct" / "code reaches here" | Concrete code quote + mutation outcome |
| Skip NEGATIVE or EDGE (REAL) / skip an AC (VIRTUAL) | Cover all categories / all ACs |
| Write all results at end | Append after each path with index-prefix |
| Variant-C marker (legacy) | Index-prefix sequence numbers (only allowed) |
| Ignore INTERRUPTED / DEFERRED / DECAY_QUEUED | Resume + re-traverse |
| Trace whole codebase | Scope = artifact + blast radius |
| Skip Evidence Re-Read Gate (§3.3 step 12) | Re-read each ◆◆◆ THIS turn, quote ≥ 3 lines |
| "Find all your mistakes" / unbounded self-critique | Targeted phrasing only |
| FAIL without Error Propagation Table + repro_snippet + fix_proposal | All three MANDATORY |
| Skip Reviewer Agent on FAIL when available | Run with isolated context |
| Apply mutation testing or PBT to production | Dev/staging only; scoped to changed files |
| VIRTUAL ◆◆◆ from imagined trace | Anchor every ◆◆◆ to artifact text + (when present) `file:line` |
| > 50% synthetic ◆◆◆ in V_PASS | Downgrade to V_INCONCLUSIVE — Mental-Reality Gap |
| Apply `fix_proposal` from this skill | That is `/bug.fix`'s job |
| Save Phase 8R / 7V verification in trace/report | Chat only |
| Trust artifact framing ("HIGH confidence" / "trivial" / "obvious") | Sycophancy guard — redact + re-evaluate |
| Cross-layer ≥ 3 trace without Architecture Pre-Read (§2 step 0.4.5) | Read `Project_Overview.md` + project doc; record layer-boundary + governing F/B/D-XXX + invariants in Checkpoint |

---

## 11. When NOT to use

- Implementing a fix from already-identified root cause → `/bug.fix`.
- Investigating WHY a bug happens (no proposed cause yet) → `/bug.why` (`root-cause-analysis`).
- Greenfield design without an artifact to falsify → `/howto.implement`.
- Distributed cross-service tracing (APM, OpenTelemetry) → `B-085`.
- Pure code review without coverage / path / mutation question → `/review`.
- Trivial change (typo, label rename) → `/verify`, no `/trace`.

---

## 12. Failure modes + recovery

**FM-A (REAL)**: PATH_PASS declared, mutation challenge skipped or all mutants survived ⇒ INVALID. Recovery: rerun §3.3 step 7; no mutant fails ⇒ STATUS=FAIL "non-discriminating evidence".

**FM-B (REAL)**: legacy Variant-C marker corrupted by autosave on long trace ⇒ resume failure. Recovery: SCHEMA at line 1 must say `resume_format: index-prefix`; an old trace using `marker` ⇒ recreate the trace file from PATH_RESULT records via `Glob` + parse.

**FM-C (VIRTUAL)**: Mental-Reality Gap fires (> 50% synthetic ◆◆◆ in V_PASS). Recovery: V_INCONCLUSIVE; emit Investigation Continuation Plan listing "what real code we need to read OR what tests we need to run before V_PASS is justified".

**FM-D (BOTH)**: Sycophancy fires on user pushback ("but the RCA says HIGH"). Recovery: re-anchor on evidence per §6 Sycophancy guard — agree only if ≥ 1 ◆◆◆ supports; otherwise restate disagreement with Refuter.

**FM-E (BOTH)**: Hallucinated `file:line` slipped past Citation-Grounded check. Recovery: rerun the gate THIS turn with explicit `Read`; downgrade ◆◆◆ → ◆○○; recompute verdict.

---

## 13. See also

- [reference.md](reference.md) — 8-method hierarchy, MPC / SBFL / Ochiai / Tandem-FL formulas, technique inventory.
- [report-template.md](report-template.md) — TRACE-REPORT (REAL §0–11) + V-TRACE-REPORT (VIRTUAL §V0–V11) skeletons; YAML frontmatter; anti-bloat rules.
- `CLAUDE.md` — project doctrine. **Read FIRST.** Tier (§3), Checkpoint (§4), Adversarial Toolkit (§7), Output Contract (§9), Pre-Send Checklist (§11), Repro Kernel (§12), Reflexion (§13), P0 #1–16.
- `.claude/skills/root-cause-analysis/SKILL.md` — sibling for `/bug.why`. White-box-trace consumes RCA reports in VIRTUAL mode and feeds `/bug.fix` from REAL FAIL.
- `context/05_AI_Rules_And_Context/FAILURE-MODE-REGISTRY.md` — FM tagging. Typical for this skill: FM-2, FM-4, FM-7, FM-9, FM-11, FM-16, FM-19, FM-20, FM-21, FM-22.
