---
name: dev-sciomc
description: Scientific method scaffolding — hypothesis → experiment → evidence → conclusion. Use when you need rigorous causal reasoning rather than vibes-based debugging.
---

# Dev Sciomc (Scientific Method)

Derived from oh-my-claudecode (MIT, Yeachan Heo). Adapted for the EvoNexus Engineering Layer.

Scientific method discipline applied to engineering investigations. Forces explicit hypothesis statement, experimental design, evidence collection, and provisional conclusions.

## Use When
- Investigation requires rigor beyond "let me try X"
- Performance optimization (you need controls and measurements, not guesses)
- A/B comparison of two implementations
- Anything where the cost of being wrong is high

## Do Not Use When
- Trivial bug → use `@hawk-debugger`
- Pure exploration → use `@scout-explorer`

## Workflow

### Phase 1 — Hypothesis
- State the hypothesis as a falsifiable claim
- "X is faster than Y" not "X feels faster"
- Identify the dependent variable, independent variables, controls

### Phase 2 — Experiment Design
- What measurement will prove/disprove the hypothesis?
- What's the minimum sample size for statistical significance?
- What confounders need to be controlled?

### Phase 3 — Evidence Collection
- Run the experiment
- Collect raw data
- Note environmental factors that could affect results

### Phase 4 — Analysis
- Apply statistical tests (delegate to `@prism-scientist`)
- Calculate effect size, CI, p-value
- Compare against the hypothesis

### Phase 5 — Conclusion
- Provisional, never absolute
- State limitations
- Identify follow-up experiments

## Output
Saved to `workspace/development/research/[C]sciomc-{topic}-{date}.md`:

```markdown
## Scientific Investigation — {topic}

### Hypothesis
{Falsifiable claim}

### Experimental Design
- Dependent variable: {what we measure}
- Independent variables: {what we vary}
- Controls: {what we hold constant}
- Sample size: {N}

### Method
{Step-by-step protocol}

### Results
{Raw data summary}

### Statistical Analysis
[delegated to @prism-scientist]

### Conclusion
{Provisional conclusion + limitations}

### Follow-ups
- {next experiment}
```

## Pairs With
- `@prism-scientist` (for statistical analysis)
- `@trail-tracer` (when investigation is causal)
- `@apex-architect` (when conclusion implies architecture change)
