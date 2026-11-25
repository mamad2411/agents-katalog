---
name: crucible-investigation-methodology
description: actively investigating a hypothesis — running a sweep, dispatching multi-agent analysis, designing serial adversarial gates,
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

# Investigation Methodology — 6 execution patterns

> **Self-Evolving Skill**: If any pattern here fails in practice (wrong results, wasted compute), update the section AND append to `references/evolution-log.md`. Don't defer.

These 6 patterns executed in service of `a-research-foundations`. They are the "how" to the foundations' "why". Apply in roughly this order for a new hypothesis.

---

## 1. LLM-native data representation — quintile tokens

Before asking an agent to "look at" numerical market data, encode as per-bar token sequences using **rolling quintile ranks** within a causal window.

**Canonical schema**:

```
idx  dir  body_q  range_q  dur_q  uwick_q  lwick_q  loc  sess  fwd+H...
```

Each quintile is `1..5` in a causal 200-bar rolling window (see Skill A §1). Agents can spot motifs like `+1:5:1|+1:5:1|+1:5:1` (three consecutive fast big-up bars) that are invisible in float-space.

Context-budget rule: 60 KB tokenized stats-table fits in agent context; 67 MB raw bars don't.

Full reference: `findings/methodology/01-llm-native-data-representation.md`.

---

## 2. Serial adversarial gates (A/B/C/D/E protocol)

Before trusting any in-sample positive, survive 4-5 independent gates in series.

| Gate                                     | Question                                     | Catches                                               |
| ---------------------------------------- | -------------------------------------------- | ----------------------------------------------------- |
| A — Directional breakdown                | Is edge from long/short/both?                | Diffusive-looking edges that are actually directional |
| B — Mirror symmetry                      | Does the inverse trigger show mirror edge?   | Sample-window drift inflating one side                |
| C — OOS time-split (80/20 chronological) | Does finding survive on held-out later data? | In-sample overfit                                     |
| D — Cross-asset replay                   | Does it replicate on other symbols?          | Asset-specific overfit                                |
| E — Full-history per-year                | Is it positive in ≥60% of years?             | Single-year-luck                                      |

**Gate C is non-negotiable.** Never report a positive without time-split OOS.

**Classify verdicts**:

- All pass → `validated-cross-asset` (promote)
- A+B+C pass, D fails → `validated-asset-specific` (narrow scope, don't kill)
- C fails → kill and archive with `resurrect_if:` conditions

Full reference: `findings/methodology/05-serial-adversarial-gates.md`.

---

## 3. Multi-lens agent synthesis (4-5 parallel specialists)

When brute force is infeasible, launch 4-5 specialist agents in parallel with distinct analytical lenses. Convergence = validation; divergence = diagnostic.

**Canonical lens set**:

1. Pattern-motif / n-gram
2. Regime / trend classifier
3. Morphology / wick hunter
4. Information theorist / surprisal
5. **Hidden-signal hunter / skeptic critic** — ALWAYS include; prevents confirmation bias

**Rules**:

- Same raw data, different lens prompts
- Each agent briefed: "test against shuffled-null, estimate multiple-testing burden, require null-test z > 2 AND per-year stability"
- 5th agent explicitly asks: "prior 4 agreed; do you concur or dissent?"
- ≥3/5 convergence = likely real; only 1 agent = likely lens-specific artifact

**Disagreement is information**. If two agents find different signals, test both independently.

Full reference: `findings/methodology/04-multi-lens-agent-synthesis.md`.

---

## 4. Per-trade enrichment for loss postmortem

When a signal works sometimes and fails sometimes, convert aggregate question → row-level question.

**Pipeline**:

```
Step 1 — Run signal across full history → collect N trade outcomes
Step 2 — Compute 20-30 causal features at each trigger bar
Step 3 — Emit parquet (per-trade × feature matrix)
Step 4 — Ship to multi-lens agents (§3)
Step 5 — Each agent hunts filters
Step 6 — Evaluate filters via shuffled-null + OOS
```

**Must-have feature categories** (at least one from each):

- Trend/regime (SMAs, slopes, autocorrelations)
- Volatility regime (rv, range compression, Kaufman ER)
- Pattern context (quintiles at trigger + lags)
- Exhaustion/cluster (bars-since-last-signal, signal-count-in-window)
- Position (dist-to-swing-high ATR-normalized)
- Calendar (hour, weekday, month, session)

Session example: turned +0.178 bps baseline → +0.514 bps filtered (2.9× lift).

Full reference: `findings/methodology/06-per-trade-enrichment-postmortem.md`.

---

## 5. Agnostic-null cascade (orthogonal null retest)

When a signal passes one null type, retest with an **orthogonal** null before trust. Example from session:

- Phase F-B shuffled the vol-forecast column → +0.370 signal "lost" to z=−5.15 under that null
- Phase C shuffled the trigger mask (proper null) → +0.439 signal passed at z=+5.74

If Phase C had been the only test, we'd have trusted a potentially wrong null. If Phase F-B had been the only test, we'd have missed a real signal.

**Rule**: whenever a positive emerges, identify AT LEAST ONE orthogonal null and retest. Common orthogonal pairs:

- Feature-shuffle AND mask-shuffle
- Permutation AND block-bootstrap
- Shuffled-selection AND parametric (e.g., binomial tail)

If signal passes both, trust more. If it passes one but fails the other, investigate why — the divergence tells you something about the signal's mechanism.

---

## 6. Compute orchestration (pueue + wrapper scripts)

Long parallel sweeps go through pueue on gpu-host-1 with a specific discipline.

**Anti-pattern** (silently fails, 0-second "successes"):

```bash
ssh gpu-host-1 '~/.local/bin/pueue add -- bash -c "VAR=1 python script.py"'
```

**Correct pattern**:

```bash
cat > /tmp/run.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
export VAR="${VAR:-default}"
cd /tmp
exec uv run --python 3.14 --with numpy --with pandas python -u /tmp/script.py
EOF
scp /tmp/run.sh gpu-host-1:/tmp/
ssh gpu-host-1 'chmod +x /tmp/run.sh && ~/.local/bin/pueue add --group mygroup --label "job" -w /tmp -- /tmp/run.sh'
ssh gpu-host-1 '~/.local/bin/pueue wait <id> --quiet; tail -50 ~/.local/share/pueue/task_logs/<id>.log'
```

Key points:

- Wrapper script (never inline `bash -c`) — pueue's `sh -c` wrapping strips inline quotes
- `python -u` for unbuffered stdout (otherwise logs stay empty for 40 min)
- `pueue restart --in-place <id>` (not bare `restart`, which creates new task IDs)
- Use `fork` multiprocessing context to share pre-computed arrays via COW

Full reference: `findings/methodology/08-compute-orchestration-pueue.md`.

See also: `Skill(devops-tools:pueue-job-orchestration)` for extended patterns.

---

## Confirmation counts (provisional)

| Pattern                    | Confirmed                      | Notes                                                     |
| -------------------------- | ------------------------------ | --------------------------------------------------------- |
| 1. quintile-tokens         | 3                              | Qualitative scan, Phase B stats, per-trade CSV            |
| 2. serial-gates            | 1 major (NGRAM3FU 4-gate pass) | Proven template                                           |
| 3. multi-lens agents       | 3                              | Act-2 qualitative, Phase C stats, Phase L loss-postmortem |
| 4. per-trade-enrichment    | 1                              | Phase L — needs re-confirmation                           |
| 5. orthogonal null cascade | 1                              | F-B vs C — the discovery of the principle itself          |
| 6. pueue orchestration     | 30+ tasks                      | Very high confidence; standard infra                      |

---

## Post-Execution Reflection

After invoking this skill:

1. Did a pattern catch a bug, save time, or produce a validated finding? Increment `confirmed` in the table above; note the session/audit folder in `references/evolution-log.md`.
2. Did a pattern fail (misled you, wasted compute)? Demote in the table with a brief note; add to evolution log with link to the failing session.
3. New execution pattern emerged? Draft a new section + append to evolution log.
4. Compute anti-pattern caught you again? Re-check §6 wording — clarify the trap.
