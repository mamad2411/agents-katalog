---
name: sb-research-methodology
description: The discipline that turns a hunch into an accepted result in the second-brain plugin repo — load when proposing a new mechanism, scoring change, or feature hypothesis; adopting a technique from a paper (mem0, Generative Agents, Graphiti, GraphRAG); asking "was this tried before?"; designing an experiment or measurement; deciding whether a finding counts as proven; running or requesting adversarial/refute review; or deciding to retire/kill a feature. Keywords - evidence bar, hypothesis, predict numbers, prior art, refuter panel, skeptic, negative result, idea lifecycle, retire, borrow ledger. NOT for - the specific open frontier problems (use sb-research-frontier), test-suite mechanics and add-a-test (sb-validation-and-qa), step-by-step analysis recipes (sb-proof-and-analysis-toolkit), the full incident chronicle (sb-failure-archaeology), or live-failure triage (sb-debugging-playbook).
---

# sb-research-methodology — from hunch to accepted result

This repo (the second-brain Claude Code plugin) has shipped 188 plugin versions in ~68 days
with zero literal `git revert` commits — every idea either graduated through a fixed
lifecycle or was retired forward, in writing, with a guard against its return. This skill is
that lifecycle: the evidence bar a claim must clear, the stages an idea moves through, where
the good ideas actually came from (with hit-rate honesty), and when to stop.

Terms used below (full definitions live in sb-architecture-contract): **dream** = the
background consolidation job that stages a modified copy of the wiki for accept/reject;
**FORGET** = the consolidation phase that archives low-importance redundant pages;
**drainer** = the out-of-band process that mines archived transcripts into the knowledge
base. Config flags are `SB_*` environment variables (inventory: sb-config-and-flags).

---

## 1. The evidence bar

Three rules. A substantive claim (bug diagnosis, design justification, measurement result)
is not accepted here until it clears all three.

### Rule 1 — One mechanism must explain ALL observations, including the negatives

A proposed root cause that explains why something fails but not why the adjacent thing
*works* is a partial explanation, and partial-explanation fixes get rejected — twice in this
repo's history they shipped and the bug survived them.

| Worked example | The negative the mechanism had to explain | Outcome of the partial fix |
|---|---|---|
| jq CRLF poisoning (0.30.1) | Why did the LAST record of a JSONL file parse fine while every non-last record failed? (Text-mode stdout converts `\n`→`\r\n`; a final line with no trailing newline gets no CR.) | "Strip CR at the failing call site" would have left 120 other sites broken; the accepted mechanism ("Windows Git-Bash jq emits CRLF in `-r` output even on clean LF input") mandated fixing the leverage point (`sb_config_get`) + all 121 captures across 29 scripts. archive/docs:CHANGELOG.md `## 0.30.1`. |
| Active-slug hijack (0.24.29 → 0.24.30) | Why did the hijack persist after the 0.24.29 fix, and why were all tests green? (`CLAUDE_PROJECT_DIR` is *inconsistently present* across MCP spawns; every test sandbox set it.) | 0.24.29 shipped green and did not work; 0.24.30's CHANGELOG names the anti-pattern verbatim: "green tests over real-env correctness". archive/docs:CHANGELOG.md `## 0.24.30`. |

Full walkthroughs of both, plus the P7 measured-negative template:
[references/worked-examples.md](references/worked-examples.md).

Practical test: write the mechanism as one sentence, then list every observation — including
"X still works" and "the test was green" — and check each follows from that sentence. If any
observation needs a second mechanism, you have not found the root cause yet
(discriminating-experiment recipes: sb-proof-and-analysis-toolkit).

### Rule 2 — Predict the number before you run the measurement

Hypotheses here carry a numeric prediction written down *before* the experiment, so the
result can falsify it. Verified instances:

- **P1c injection measurement** (as of 0.33.30): the spec criterion "wiki body is not
  injected every turn" was committed first; the measurement then produced ~662 B / ~165
  tokens per-turn (`persona-context.sh`), confirming it. archive/docs:CHANGELOG.md:26.
- **F1 staging-validity floor**: the prediction "a consolidation merges/archives a FEW
  pages; it never guts the wiki" is encoded as a number — dream-accept refuses when staging
  has fewer than `SB_DREAM_ACCEPT_MIN_RATIO`% (default 50) of live pages, or is empty.
  `scripts/dream-accept.sh:94-115`.
- **Strict recall gate**: the retrieval release gate is recall@2 **= 1.0** over 12 golden
  queries, not "recall is good" — chosen because "the hub-boost bug showed up as exactly one
  displaced page while the old 0.8 gate stayed green." `tests/test-knowledge-eval.sh:10-14`.
- **P7 graph-boost measurement** (0.33.22): outcome classes (improved/degraded/unchanged
  gold-page rank) were defined before running; result 6 / 6 / 80 of 92 = a wash → demote.
  archive/docs:CHANGELOG.md:162-169.

A threshold with no rationale is a phantom knob (a documented failure class here — undo
table row 20 in sb-failure-archaeology). When you pick a number, write WHY that number in a
comment at the definition site, the way `dream-accept.sh:94-100` does.

### Rule 3 — Assigned adversarial refutation before adoption

Findings and designs face a reviewer whose *job* is to refute them — not a second opinion,
an assigned opponent. The in-repo machinery:

| Mechanism | Protocol | Evidence |
|---|---|---|
| Refuter panel (code-review-deep Pass 3 — skill removed 0.44.0; the protocol remains the house pattern, dispatched via `persona_think` today) | Every critical/high finding is scored by 1 normal scorer + 2 dispatched in REFUTE MODE; final score = median of 3 (== confirmed iff ≥2 of 3 score ≥70). Refuters inherit the session/best model — "a refuter must out-reason the finder; do NOT pin them to a cheaper model." | pre-0.44.0 `skills/code-review-deep/SKILL.md:152-162` |
| `/second-brain:doubt` | Starts from "this probably does NOT work"; branches 2-3 attack vectors per claim; anti-self-deception rule: a vector may be labeled `impossible` only with a defending file:line citation; a critic subagent audits the full branch log for over-pruning. | `skills/doubt/SKILL.md:123-136,154-165` |
| Deep audits | The 2026-07-02 deep audit ran 11 area agents with a verification pass; ledger records 88 confirmed AND 1 refuted finding — refutation is a recorded outcome, not a discard. | audit ledger structure per sb-failure-archaeology §disposition |
| Review-as-pipeline-step | `fix(review): apply deep-review findings` is a named commit stage (18 such commits); features have been killed at this stage pre-ship — 0.32.0's designed "machine heartbeat" was REFUTED during adversarial verification and dropped for a simpler clamp. | `git log --oneline --grep='fix(review)'`; `git show archive/docs:CHANGELOG.md` `## 0.32.0` |

The stakes are documented: in 0.31.0 the first review *missed* a regression (the un-starve
escape would have poison-pilled good transcripts — the exact failure commit `ee8a74c`'s
defer existed to prevent); a second, FP-aware multi-agent review caught it before ship.
One review is not the bar; an *assigned refuter* is. Default posture on uncertainty is
refute/hold: the (0.44.0-removed) code-review-deep's 16-69 band was surfaced as explicitly
unconfirmed, never promoted (pre-0.44.0 `skills/code-review-deep/SKILL.md:163-170`; skill since removed). (UNVERIFIED — a default-refute
filter reportedly cut the 0.33.31 candidate list from 19 to 13 findings before the batch;
no repo artifact records those counts. Check: `episodic_search "deep audit refute 0.33.31"`.)

---

## 2. The idea lifecycle

Stages with exit criteria. Do not skip stages; the repo's worst regressions are recorded
skips (0.24.29 skipped live verification; 0.30.2 skipped the release gate).

| # | Stage | What you do | Exit criterion |
|---|---|---|---|
| 0 | Hunch | State the mechanism + expected benefit in one sentence each. | You can name the observation that would falsify it. |
| 1 | Prior art | Run the §3 "before you propose" checks: episodic/wiki search, git/CHANGELOG grep, the undo table in sb-failure-archaeology, the two plan trees. | Either "never tried", or "tried and retired for reason R, and R no longer applies (cite where R is recorded)". |
| 2 | Design + fence | For non-trivial work: spec → plan (`docs(spec)` → `docs(plan)` commits, house pipeline). Plans here explicitly FENCE wrong paths with the reason — copy that habit. Examples: P2 fences regex-subsumption contradiction detection ("undecidable, false-positive prone; exact-string identity only", p2 plan :295); P3a fences node-tree-sitter ("REJECT — reintroduces the exact problem CONSTITUTION.md forbids", p3a plan :90); P6 fences blanket `--unshare-net` (CHANGELOG.md:27). | Plan exists with fenced wrong paths AND the Rule-2 predicted numbers. Check it against CONSTITUTION.md hard constraints + "the test" (:38: an item that doesn't guide a future decision doesn't belong). |
| 3 | Experiment behind an `SB_*` flag | Ship the mechanism gated. Default matches evidence: unproven/risky ⇒ default-OFF opt-in (post-demote `SB_GRAPH_RANKING_BOOST=1`); evidence-backed with residual risk ⇒ default-ON with a kill switch (`SB_DREAM_REFLECT`, `SB_PLAN_FIRST_NUDGE=off`, `SB_CAPTURE_DEDUP=off`). Kill switches must be MACHINE-enforced, not prose (`graph-cluster.sh --gate` returns `[]`; asserted both ways in `tests/test-graph-cluster-shim.sh`). Add-a-flag checklist: sb-config-and-flags. | The measurement ran and the result is compared against the Stage-2 predicted number, on OUR corpus (P7 measured on the real wiki: 96 pages / 170 edges — not on a benchmark). |
| 4 | Adversarial review | Rule 3 machinery: refuter panel for critical/high findings, `/second-brain:doubt` for subsystem claims, a deep-review pass for the diff. | Findings applied (`fix(review):` commit) or the idea is killed here — pre-ship kills are normal (0.32.0 heartbeat). |
| 5a | Adoption | Default-on (or keep the earned default) + CHANGELOG entry + a MACHINE LOCK — a test that goes RED if the result is silently reverted: default-off lock `mcp/src/tools/retrieval-guards.test.ts:114-139`; source-scan locks (`brain-paths.test.ts`, `agent-grants.test.ts`); regression-lock comments naming the one-line mutation that flips the test (house pattern, sb-validation-and-qa). Release lockstep + gates: sb-change-control. | Gates green; the lock demonstrably fails on the pre-adoption shape (test-the-test). |
| 5b | Retirement (equally first-class) | Forward-fix commit with the rationale in the body — often a "Supersedes"/"CORRECTS" marker — plus, where the retired shape is dangerous, an INVERTED or new guard so it cannot return (the 0.24.35 validator now FAILS on the manifest form 0.24.5 required). CHANGELOG entry states what was cut and why. | The chronicle records it (sb-failure-archaeology undo table); the knobs left behind are either removed or documented inert (0.33.25: `SB_FORGET_W_ACCESS`/`_W_RECENCY` "now inert — backward-compatible"). |

There are ZERO `git revert` commits in the full history
(`git log --all --oneline --grep="^Revert" | wc -l` → 0, verified 2026-07-05): retirement
here is documentation plus a lock, never silent deletion.

---

## 3. Before you propose — checklist

Run from repo root. All read-only.

```bash
# 1. Was it tried? (three lanes: commits, narrative, plans)
git log --all -i --grep='<term>' --oneline | head -20
git show archive/docs:CHANGELOG.md | grep -in .<term>. | head -20  # pre-1.0 narrative only
ls docs/plans/                                  # live plans
git ls-tree --name-only archive/docs:docs/superpowers/plans/  # pre-1.0 plans (removed 0.34.0)
```

```
# 2. Memory lanes (MCP tools shipped by this plugin):
#    knowledge_search "<term>"   — wiki prior art
#    episodic_search "<term>"    — past session transcripts
# 3. The undo table: sb-failure-archaeology — 20+ tried-and-backed-out entries.
#    Proposing anything on that list requires citing why the retirement reason no
#    longer applies (e.g. embeddings returned in 0.24.39 only WITH the
#    degraded:'bm25-only' honesty flag the v1.0 removal lacked).
```

Then, before writing code:

- [ ] Mechanism in one sentence; falsifying observation named (Rule 1).
- [ ] Predicted number written down, with the WHY at the definition site (Rule 2).
- [ ] Checked against CONSTITUTION.md hard constraints (autonomy, untrusted-content
      isolation, cross-platform, no-frequency-ranking) and "the test" (:38).
- [ ] If a queued plan (P2 / P3a / P6 remainder) touches the same area: read its
      fenced-wrong-paths section first — those fences are prior negative results.
- [ ] Kill-switch name chosen (`SB_*`), default justified by current evidence level.
- [ ] Machine lock you will add at Stage 5a named (which test, what it asserts).
- [ ] Surface-budget headroom checked (`.claude-plugin/surface-budget.json`; enforced by
      `scripts/validate-plugin.sh` R8) — prefer folding into existing files.

---

## 4. Where good ideas came from (hit-rate honesty)

Four sources, in observed order of yield. The point: every source is *vetted small* before
anything ships, and the negative verdicts shaped the design as much as the adoptions.

### 4a. Paper borrows, via the ledger

The spec (`archive/docs:docs/superpowers/specs/2026-06-26-second-brain-constitution-and-diet-design.md`,
references §11 at :301-313) keeps a citation ledger; every borrow entered the §2 lifecycle
individually. Technique mechanics: sb-memory-systems-reference. Ecosystem/novelty claims:
sb-external-positioning. What this skill owns is the VETTING pattern, visible in verdicts:

| Borrow | Verdict | The vetting move |
|---|---|---|
| mem0 ADD/UPDATE/NOOP write path | ADOPTED (0.33.29 capture; re-planned for P6 writer) | Scoped smaller than the paper: capture-time NOOP scans only the unprocessed inbox, never the wiki; kill switch `SB_CAPTURE_DEDUP=off`. |
| Generative Agents reflection | ADOPTED with cadence REJECTED (0.33.28) | Took "the one memory op with ablation support"; rejected the importance-accumulator cadence — "assumes a continuous agent loop we don't have" (archive/docs:CHANGELOG.md:60-63). Adapt to OUR runtime, don't transplant. |
| Graphiti bi-temporal `supersedes` | ADOPTED; survived the P7 demote | Kept for the mechanism it uniquely fixes (suppressing superseded facts), even while the graph's *ranking* role was cut. |
| GraphRAG-Bench skepticism | ADOPTED as justify-or-demote (0.33.22) | A skeptical paper triggered a MEASUREMENT, not a rewrite: instrument first, demote on the wash result. |
| ARC incremental capture | ADOPTED (0.33.18) | Chosen over threshold-triggered capture on the paper's ablation numbers (31% vs 24-27%), then verified by the repo's own criterion (compaction loses no captured decisions). |
| Aider repo-map (tree-sitter + PageRank) | ACCEPTED-with-modification; P3a Phases 1-3 shipped (PageRank code-map live), Phases 4-5 still queued | PageRank borrowed; tree-sitter demoted to opt-in WASM tier after a cross-platform risk spike (p3a plan :84-101). |
| CaMeL dual-LLM quarantine | ACCEPTED, plan-queued (P6); ~7-pt utility cost explicitly budgeted | Cost of the borrow written into the plan before implementation. |
| Cross-encoder reranker | ACCEPTED in spec, NOT started | Stays labeled not-started; no code, no plan doc — claim discipline. |
| Usage-frequency ranking (recsys) | REJECTED twice (0.33.25 FORGET, 0.33.30 search) | The rich-get-richer hub bias — "literally our ~10,000× score-inflation bug" — now enshrined as a CONSTITUTION.md:44-45 constraint. |

### 4b. Deep audits

Structured whole-plugin sweeps, each finding independently verified, each batch becoming a
release: the 2026-06-10 deep-dive spec → repair waves R1-R8 (0.24.37-0.24.50); the 0.29.4
adversarial audit (4 silently-wrong-output bugs, "EVERY finding reproduced by running the
script"); the 2026-07-02 deep audit (11 areas, 88 confirmed findings) → the 0.33.31 batch
closing all 9 HIGHs (archive/docs:CHANGELOG.md:7-18). The open medium/low remainder of that audit is the
current improvement backlog (sb-failure-archaeology owns the ledger).

### 4c. Live incidents

Most of the cross-platform doctrine (path normalization at the boundary, mawk/BSD rules,
CRLF discipline) was extracted from production failures, not designed up front. The
stories and their symptom→cause records: sb-failure-archaeology; triage:
sb-debugging-playbook.

### 4d. Negative results — cutting is a first-class result

Design-shaping cuts, each with a measurement or refutation behind it and a release entry
like any adoption: graph ranking boost demoted after the 6/6/80-of-92 wash (0.33.22);
access-frequency cut from search ranking (0.33.30 P4b) and from the FORGET score (0.33.25);
the first graph layer deprecated as "never used in practice" (0.7.0) — and its 0.22.0
return was typed/bi-temporal, i.e. re-admitted only in the shape that fixed the original
objection; the machine heartbeat refuted pre-ship (0.32.0). A cut result gets the same
Stage-5a treatment: CHANGELOG + machine lock (the P7 default-off lock,
`retrieval-guards.test.ts:114-139`).

---

## 5. When to stop

House discipline (project direction — practiced, not written in any single repo doc):

- **Refuted twice → chronicle it.** If an idea's load-bearing claim fails assigned
  refutation twice (or its fix ships twice and the symptom survives, as in 0.24.29/0.24.48),
  stop iterating in place. Write the retirement: what was tried, the mechanism that killed
  it, the evidence — into the plan doc or CHANGELOG, so the undo table can carry it. The
  0.24.48→0.24.49 YAML re-ship shows the alternative: the same class shipping twice bought a
  root-cause gate (a real parser + property test), not a third patch.
- **Dry rounds → rotate, don't grind.** The doubt skill encodes this for audits: "If recent
  runs keep finding 0 issues on the same layers, those layers may be well-hardened — the
  skill should prioritize untested layers more aggressively"
  (`skills/doubt/SKILL.md:215-228`, with per-run calibration counters).
- **Never leave an idea in limbo.** The one recorded violation is instructive: R5.2's
  cost-router's (removed 0.35.x) "dogfood 2 weeks → dated keep-or-kill decision" was never recorded anywhere in
  the repo (`git log --all -i --grep="keep-or-kill"` → empty); the debt was finally mooted by
  removal — cost-router was absorbed and removed in 0.35.x without the decision ever being
  stamped. Undecided ≠ undocumented: stamp a date on the decision you are deferring.

A documented retirement is a *result*. The undo table (sb-failure-archaeology) is the
highest-leverage research artifact this repo has: it is what makes Stage 1 cheap.

---

## When NOT to use this skill

- Picking WHICH frontier problem to attack, or its assets/milestones → sb-research-frontier.
- How to write/run tests, CI lanes, add-a-test mechanics → sb-validation-and-qa.
- Step-by-step measurement/analysis recipes with worked numbers → sb-proof-and-analysis-toolkit.
- What happened in a specific incident → sb-failure-archaeology.
- Classifying/gating/releasing a change you already believe in → sb-change-control.

---

## Provenance and maintenance

Derived from repo evidence only (paths as of 0.33.31 — CHANGELOG.md and the docs history
moved to `archive/docs` in 0.34.0; code-review-deep was removed in 0.44.0): `CHANGELOG.md`
(0.24.29-0.33.31 entries),
`CONSTITUTION.md`, `archive/docs:docs/superpowers/specs/2026-06-26-second-brain-constitution-and-diet-design.md`,
`docs/specs/2026-06-18-project-scoping-model-design.md`, the three queued plans under
`docs/superpowers/plans/2026-06-30-*`, `skills/code-review-deep/SKILL.md` (removed 0.44.0),
`skills/doubt/SKILL.md`, `scripts/dream-accept.sh`, `tests/test-knowledge-eval.sh`,
`mcp/src/tools/retrieval-guards.test.ts`, and read-only `git log` queries run 2026-07-05.

Authored 2026-07-05 against the UNCOMMITTED 0.33.31 working tree (HEAD `6fba312` =
release 0.33.30). Facts stamped "as of 0.33.31" live in the working tree, not yet in a
commit.

Re-verification one-liners (volatile fact classes):

```bash
git log --all --oneline --grep="^Revert" | wc -l          # still 0 true reverts?
git log --oneline --grep='fix(review)' | wc -l            # review-step commits (was 18)
grep -n "SB_DREAM_ACCEPT_MIN_RATIO" scripts/dream-accept.sh   # F1 floor default (was 50)
grep -n "SB_EVAL_MIN_RECALL" tests/test-knowledge-eval.sh     # strict gate (was 1.0)
wc -l < tests/fixtures/eval-queries.jsonl                     # golden queries (was 12)
grep -n "SB_GRAPH_RANKING_BOOST" mcp/src/tools/retrieval-guards.test.ts  # default-off lock present?
# (Rule-3 panel home skills/code-review-deep was removed 0.44.0 — protocol history at any pre-0.44.0 ref)
git show archive/docs:CHANGELOG.md | grep -i "662 B"          # P1c measured number (history moved to archive/docs, 0.34.0)
git show archive/docs:CHANGELOG.md | grep -c '^## '           # release-entry archive (131; ## 0.33.19 heading still missing there)
```
