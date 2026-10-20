---
name: experiment-platform
version: 1.0.0
min_mindforge_version: 10.6.0
status: stable
triggers: experiment platform design, experimentation infrastructure, statistical rigor experiment, guardrail metric design, experiment velocity, feature flag experiment, experiment analysis automation, sample size calculation, multi-variant testing, experiment platform lifecycle, experiment review process, sequential testing
compose: experiment-design
---

# Skill — Experiment Platform

## When this skill activates
This skill activates when building experimentation infrastructure, implementing statistical testing frameworks, or designing A/B testing platforms. Use when organizations need to scale testing velocity while maintaining statistical rigor.

## Mandatory actions when this skill is active

### Before writing any code
1. Define experiment framework components: randomization service, exposure logging, metric computation pipeline, and statistical analysis engine
2. Establish statistical rigor standards: minimum sample size, power (80%+), significance level (5%), minimum detectable effect, and multiple comparison corrections
3. Design guardrail metrics framework: business health (revenue, retention), user experience (latency, errors), and ecosystem health (partner impact)
4. Plan experiment lifecycle states: draft, review, running, paused, completed, archived with transition criteria and approval gates

### During implementation
- Implement consistent randomization using stable hashing (user_id + experiment_id) ensuring users see same variant across sessions
- Build exposure logging capturing: timestamp, user_id, experiment_id, variant, context for accurate sample size and covariate adjustment
- Create metric computation pipeline with: numerator/denominator structure, winsorization for outliers, delta method for ratios, bootstrap for confidence intervals
- Design sequential testing capability for early stopping: alpha spending functions, futility boundaries, and minimum runtime requirements
- Implement stratified analysis for heterogeneous treatment effects: by platform, user segment, geography with interaction effect testing
- Build automated guardrail checks: alert on significant negative movement in critical metrics with experiment auto-pause capability
- Create experiment metadata repository: hypothesis, success criteria, related experiments, learnings, and decision outcome for institutional knowledge

### After implementation
- Generate automated experiment scorecards: primary metric movement, guardrail status, statistical significance, practical significance, recommendation
- Build experiment catalog with search and discovery: hypothesis library, metric glossary, analysis templates, and historical results
- Create experimentation health dashboard: velocity (experiments/week), quality (statistical power distribution), impact (significant wins), and coverage (features tested)
- Document statistical methodology: test selection, variance reduction techniques, multiple comparison approach, and sequential testing procedures

## Self-check before task completion
- [ ] Randomization service ensures stable assignment and balanced allocation across variants
- [ ] Exposure logging captures all necessary context for accurate analysis and debugging
- [ ] Statistical analysis engine implements proper corrections for multiple comparisons and peeking
- [ ] Guardrail metrics monitored automatically with alerting and experiment pause capability
- [ ] Experiment lifecycle enforces minimum runtime and sample size before declaring results
