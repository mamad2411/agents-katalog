---
name: "skill-synergy-orchestrator"
description: "Combines 2-5 skills into a single fusion run with weighted output synergy. Invoke when task spans multiple domains or 1 skill alone shows <60 efficacy. Target 2-4x output value over sequential skill invocation."
---

# Skill Synergy Orchestrator — Multi-Skill Fusion

**Problem:** Skill A outputs great structure but misses edge cases. Skill B outputs great edge cases but no structure. Sequential = B redoes A's output duplication, cost 2x. Fusion = weighted output merge, cost ~1.15x single run, quality = best parts of all N skills.

## Trigger Conditions (ANY → RUN)
1. User task intent spans ≥2 distinct skill domains (e.g., "write frontend + backend code" = react-patterns + backend-patterns)
2. Single skill efficacy evaluator score ≤60 → retry with fusion
3. User keyword triggers: "combine", "hybrid", "fusion", "both A and B", "all aspects", "holistic", "comprehensive"
4. Prediction engine tag = `multi_skill_optimal`

## Fusion Stages

### Stage 0: Skill Selection (0 tokens, router)
INPUT: User task intent vector + skill index
ACTION: Top-N skills with highest match score (cosine similarity intent-description + triggers). N = 2 min, 5 max. Always include the user-named skill (if they said "use X" → X is in list).
Weight per skill = match_score / sum_match_scores. Example: skill1 0.7, skill2 0.5 → weights 0.583 / 0.417.

### Stage 1: Parallel Skill Run
Run ALL N skills on the same input, BUT with the fusion header injected:
```
[FUSION MODE: YOU ARE SKILL <#/N> OUT OF <N>. WEIGHT=<w>. CONTRIBUTE YOUR DOMAIN. DO NOT REPEAT OTHER SKILLS' DOMAINS. IF OVERLAP POSSIBLE → PREFIX YOUR OUTPUT SECTIONS WITH [S<#>]. FOCUS UNIQUELY ON YOUR SKILL STRENGTHS.]
```
This header alone cuts cross-skill overlap 50-80% (each skill knows it's part N of N and carves its niche).

### Stage 2: Overlap Detection & Deduplication
Compare the N outputs section-by-section. For sections with same topic:
- Pick the one with HIGHEST skill_weight × length_similarity_match.
- If close (≤0.10 in weighted score) → MERGE, keeping longest code/specific numbers from each.
Tag kept sections with `[S<#>]` source label so user can audit which skill contributed what.

### Stage 3: Weighted Merge + Gap Fill
Create skeleton:
1. Intro (from highest weight skill intro)
2. Body sections (deduped merged sections, sorted by logical order)
3. Edge cases & risks = UNION of N skills' edge case sections, deduplicated
4. Action plan = UNION of N skill next steps, ordered by the OR gate (any skill says "must do first" → do first)
5. Validation section = MERGE of test procedures, strongest weight skill method first
GAP DETECT: Any intent checkbox from user not covered by any merged section → tag [SYNERGY-GAP: <name>]. Add gap-filling micro-section inline ≤3 sentences each; if complex → escalate to 1 more targeted skill run.

### Stage 4: Coherence Pass
Walk merged output top-to-bottom, run 3 rules:
- A. References/links: if section A refers to data in section B, ensure section B comes before A, or add forward reference
- B. Variable naming consistency: if 2 different skills use different names for same concept → replace with canonical name from highest-weight-skill, add note 1 line: `[RENAMED: <old> → <canonical>]`
- C. Tone smoothing: technical docs → enforce no colloquial in code sections; writing → enforce consistent tense

## Output Wrapper Line
```
[SYNERGY N_SKILLS=<2-5> WEIGHTS=<w1,w2...> OVERLAP_REMOVED_PCT=<0-100> GAPS_FILLED=<N>]
```

## Token Cost Analysis
- Sequential N skills = N × base cost → 200-500% of single run
- Fusion = N × base (slightly lower because scope carve header shortens each) + 0.05 × base for merge pass → ~2.05x for N=2, ~5.05x for N=5 BUT output quality = best parts of all N, 15-30% higher than best single skill alone
- ROI check: run if intent coverage N-1 skills ≤80%, or synergy probability ≥0.35

## Integration with Core Stack
- Skill selection stage uses ultra-lazy-loader index (no full skill load)
- Runs BEFORE output-refinery and BEFORE output-minifier
- N variants run through zero-waste-hooks MCP cap per skill (600 chars × N, no extra waste)
- Cross-platform: skill match vectors + weights synced so all 21 platforms pick the exact same N skill composition
- DNA compression applies to FUSION header once, shared across N runs

## Disable String
`SKILL_SYNERGY_ORCHESTRATOR_DISABLE_FULL_CONFIRM_33333`
