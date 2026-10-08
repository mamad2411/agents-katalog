---
name: crucible-research-foundations
description: Validate findings, design shuffled nulls, check label leakage, review causal features. TRIGGERS - shuffled null, label leakage
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Research Foundations — 6 epistemic disciplines

> **Self-Evolving Skill**: This skill improves through use. If a discipline's guidance fails in practice or a new trap emerges, update the relevant section AND append to `references/evolution-log.md`. Don't defer.

Read these in order. The first three (causal, labels, nulls) are the hardest prerequisites — violating any of them silently invalidates every downstream result.

---

## 1. Causal-feature invariant (bars[:i])

Every feature `f[i]` used at trigger/decision bar `i` must be computable using only `bars[0:i]` — never `bars[i]`, never `bars[i+1:]`. Violation produces look-ahead bias; findings silently become worthless.

**Canonical pattern**:

```python
for i in range(n):
    lo = max(0, i - window)
    wind = values[lo:i]  # EXCLUSIVE upper bound — no peeking
    f[i] = compute(wind)
```

Note `lo:i` (exclusive), not `lo:i+1`. This discipline "feels off by one" but is correct.

**Verification test** (add to every new feature function):

```python
def test_causality(fn, n=1000):
    bars = generate_test_bars(n)
    f_orig = fn(bars)
    bars_mod = bars.copy()
    bars_mod[500:] *= 2  # perturb the FUTURE
    f_mod = fn(bars_mod)
    assert np.array_equal(f_orig[:500], f_mod[:500]), "look-ahead detected"
```

**Silent-bug signature**: impossibly clean results (tw > 10 bps on FX, win rate > 70%, OOS matches IS perfectly).

Full reference: `findings/methodology/10-causal-feature-invariant.md`.

---

## 2. Label-leakage (bar-local scaling kills window leakage)

Forward labels must be scaled to the **triggering bar's own range**, NEVER to a window-wide scale. Window-relative labels are tautological.

**Trap**: If you label `fwd+H = UP when close[i+H] - close[i] > window.span/20`, then when `close[i]` is near `window.min` (loc=B), `fwd=UP` is near-automatic. Agents will report spurious "signals".

**Fix**: use bar-local triple-barrier labels:

```python
r = high[i] - low[i]   # THIS bar's range, not window's
tp_level = close[i] + tp_mult * r
sl_level = close[i] - sl_mult * r
# walk forward, exit at first tp/sl/expiry
```

**Symptom that you fell into the trap**: apparent signal strengthens monotonically with `loc` quintile; collapses when you test adjacent cells.

Full reference: `findings/methodology/02-label-leakage-bar-local-scaling.md`.

---

## 3. Shuffled-null design (3 null types — get the right one)

Shuffled-null tests are mandatory before trust, but the **choice of what to shuffle** is a design decision.

| Hypothesis class                             | Shuffle WHAT                                                  | Session example                                           |
| -------------------------------------------- | ------------------------------------------------------------- | --------------------------------------------------------- |
| "Feature X predicts outcomes"                | Shuffle the feature values                                    | Phase F-B (used wrong null, "falsified" a real signal)    |
| "Trigger pattern fires at informative times" | Shuffle the trigger mask (preserve fire-rate, move locations) | Phase C (validated ngram_triple_fast_up at z=+5.74)       |
| "Filter improves selection"                  | Shuffle which trades pass the filter                          | Phase L-C (evaluated filters against N-size random draws) |

**Rule**: ask "what is the alternative hypothesis, in one sentence?" If you can't state it, you don't know what you're testing.

**Common mistakes**:

- Using feature-shuffle when testing a trigger pattern → destroys temporal structure the pattern depends on → real signal looks worse than shuffled noise
- Under-tight null (null std huge relative to observed effect) → no statistical power
- Over-tight null (too few permutations) → unreliable z-estimates; use ≥100 for z<3, ≥1000 for z<2

Full reference: `findings/methodology/03-shuffled-null-design.md`.

---

## 4. Agent significance corrections (z-scores are overstated 2-3×)

LLM agents systematically overstate z-scores. Treat agent-reported p-values as **upper bounds**.

**Three overstatement patterns**:

1. **Ignored multiple-testing burden**: agent tests 25 variants, reports z=2.43 vs nominal 1.96 threshold. True Bonferroni threshold is `sqrt(2 * ln(N))` — for N=25 that's z>2.8.
2. **Confused sample-mean z with binomial-proportion z**: 53.5% vs 50% on N=840 gives z≈2.0 not 4.2.
3. **Extremum-of-K treated as single test**: "top combo from 17,280" has expected null-max `null_mean + null_std × sqrt(2 ln K)` ≈ null_mean + 4.5σ. An observed tw that's below that expectation is not a finding.

**Always verify**:

- How many implicit tests did the agent run?
- Re-derive z yourself: `(real - null.mean) / null.std`
- Bonferroni threshold for K tests: `z > sqrt(2 * ln K)`

**Trust thresholds**:

- z > 5, N > 500: likely real, test further
- z in [3, 5]: promising, mandatory gate validation
- z in [2, 3]: suspect, require adjacent-cell gradient + null test
- z < 2: treat as null

Full reference: `findings/methodology/09-agent-significance-corrections.md`.

---

## 5. Record-keeping discipline (append-only ledger + audit folders)

Every investigation — positive or null — must produce a permanent, discoverable record.

**3-layer architecture**:

```
findings/
├── evolution/
│   ├── evolution.jsonl              # append-only ledger
│   └── audits/
│       └── YYYY-MM-DD-slug/
│           ├── CLAUDE.md            # navigator
│           ├── verdict.md           # plain-English conclusion
│           ├── CHRONICLE.md         # narrative (for major findings)
│           ├── <reproducer>.py      # script that regenerates headline numbers
│           └── <artifact>.json      # raw telemetry
└── methodology/                     # universal principles
```

**Ledger entry fields**: `id`, `date`, `status`, `supersedes`, `superseded_by`, `headline`, `key_numbers`, `evidence` (file paths), `sha256_results`.

**The supersedes pattern**: when a later finding replaces an earlier one, ADD a new entry with `supersedes: "OLD-ID"`; UPDATE the old entry with `superseded_by: "NEW-ID"`. **Do NOT delete** the older audit folder.

Full reference: `findings/methodology/07-record-keeping-discipline.md`.

---

## 6. Post-mortem-before-abandon

Before declaring a signal dead, enrich every trade with causal pre-entry features and hunt filters on individual losses. A "sometimes works" signal is often a filterable signal in disguise.

**Pipeline**:

1. Run the signal across full history; collect N trade outcomes
2. Compute ~20-30 causal features at each trigger bar
3. Emit per-trade parquet + CSV (one row per trade)
4. Ship to multi-lens agents (see Skill B)
5. Each agent hunts filters that separate winners from losers
6. Evaluate filters against shuffled-null (see §3)

**Kill-selectivity metric**: `losers_killed / max(1, winners_killed)`. < 1.0 = harmful; 1.0-1.2 = marginal; 1.2-1.5 = useful; > 1.5 = strong.

Session example: `+0.178 bps` baseline → `+0.514 bps` after Phase-L filter. 2.9× lift from enrichment-driven filter hunt.

Full reference: `findings/methodology/06-per-trade-enrichment-postmortem.md`.

---

## Confirmation counts (provisional, as of session ca9d7ffa)

| Principle                   | Confirmed         | Notes                                                                            |
| --------------------------- | ----------------- | -------------------------------------------------------------------------------- |
| 1. causal-feature-invariant | 18+ (every phase) | Fundamental; drop only with proof                                                |
| 2. label-leakage            | 2                 | Directly caught spurious "lower-rejection-at-bottom"                             |
| 3. shuffled-null-design     | 4                 | Phase F-B wrong-null, Phase C right-null, Phase L filter-null, Phase M mgmt-null |
| 4. agent-sig-corrections    | 5+                | Combinatorialist, transition-asymmetry, trade-mgmt agents all overstated         |
| 5. record-keeping           | 5 ledger entries  | Full chain for NGRAM3FU-STRADDLE                                                 |
| 6. post-mortem              | 1                 | Phase L delivered the filter; needs re-confirmation on other campaigns           |

Higher `confirmed` = more trustworthy. Principle 6 has only one confirmation and should be treated as provisional.

---

## Post-Execution Reflection

After invoking this skill:

1. Did applying a principle catch a bug or false positive? Increment its `confirmed` count in the table above; note the session where it fired in `references/evolution-log.md`.
2. Did a principle fail (bad guidance)? Demote it in the table; add a `superseded_by` pointer in `references/archive/` with `resurrect_if:` conditions.
3. New trap that isn't covered? Draft a new section here and append to the evolution log.
4. Never silently move on. This skill's value compounds only if reality-corrections flow back.
