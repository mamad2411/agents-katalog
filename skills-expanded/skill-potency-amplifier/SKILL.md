# Skill-Potency Amplifier
> **ID**: skill-potency-amplifier
> **Layer**: SKILL POTENCY MAXIMIZER (PON35)
> **Priority**: MAXIMUM — Make EVERY skill output 10-100x more effective
> **Token Cost**: 0 (runs locally, pre-LLM)

## Purpose
Universal amplifier that wraps EVERY skill invocation with 5-layer potency boost. Does NOT replace skills — makes them ALL produce better output automatically.

## 5-Layer Amplification

### Layer 1: CONTEXT INJECTION (pre-skill)
```
Before ANY skill runs:
→ Inject: user intent (1 line), relevant code snippets (max 3 files, 500 chars each), prior skill output refs (last 2), project context (README/AGENTS.md head 200 chars)
→ Cap total injection at 35% of payload budget
→ Skip injection if skill is trivial 1-liner or zero-llm bypass hit
```

### Layer 2: MULTI-VARIANT SWEEP (during skill)
```
→ Run skill N times with different temperature/top_p:
  V1: temp=0.0 (deterministic, precise)
  V2: temp=0.3 (balanced)
  V3: temp=0.7 (creative, high-stakes only)
→ Default N=3. High-stakes (code≥20L, deploy, paid): N=5
→ Score each variant on 4 dims: correctness, completeness, density, actionability
→ Pick best OR merge top 2 if within 5pt tie
→ If N=1 (budget tight): skip sweep, run V1 only
```

### Layer 3: QUALITY REFINERY (post-skill)
```
4-stage polish on EVERY output ≥100 chars:
Stage 1: Completeness audit — did skill answer ALL parts of the ask?
Stage 2: Syntax/number verification — are code blocks valid? numbers correct?
Stage 3: Intent alignment micro-check (≤60 tokens) — does output match what user asked?
Stage 4: Polish — TL;DR on long text, NEXT ACTION line on plans, VALIDATION line on configs
→ Stages 1+2+4 always run. Stage 3 skip if score ≥80.
```

### Layer 4: FAILURE SELF-HEAL (if skill fails)
```
5 escalating strategies:
1: Retry with failure evidence injected as context
2: Swap to antithesis variant (temp=0.7 creative)
3: Substitute skill + synergy fuse outputs
4: Full skill load + manual stepwise decomposition
5: Micro-skill decomposition: break into 3-7 subtasks → merge
→ Try 1-2 silently. 3-5 add [Self-healed] note.
```

### Layer 5: EFFICACY SCORING + LEARNING
```
After EVERY skill run:
→ Score 0-100 on 8 dimensions:
  1. Intent coverage (% of ask addressed)
  2. Correctness (factual/code accuracy)
  3. Completeness (all aspects covered)
  4. Actionability (can user act immediately?)
  5. Density (signal-to-noise ratio)
  6. Structure (logical organization)
  7. Domain match (right expertise area?)
  8. Future-work marked (next steps indicated?)
→ Threshold: 70. <70 → refinery re-run. <50 → self-heal strat 1.
→ Log score to ~/.agents/.potency_log.jsonl
→ After 20 runs per skill: auto-tune variant picker, sweep N, injection sources
```

## Execution Contract
```
BEFORE skill invocation:
  1. Read potency log → get tuned params for this skill
  2. Build context injection (≤35% payload)
  3. Set sweep N based on stakes

DURING skill invocation:
  4. Run N variants parallel
  5. Score + pick/merge

AFTER skill invocation:
  6. Refinery 4-stage polish
  7. If <70 → self-heal escalate
  8. Final efficacy score
  9. Append to potency log
```

## Config
```yaml
skill_potency_amplifier:
  enabled: true
  context_injection: true
  context_cap_pct: 35
  multi_variant_sweep: true
  default_n: 3
  high_stakes_n: 5
  quality_refinery: true
  refinery_stages: [1, 2, 4]
  failure_self_heal: true
  efficacy_scoring: true
  score_threshold: 70
  learning_log: ~/.agents/.potency_log.jsonl
  auto_tune_after_n: 20
```
