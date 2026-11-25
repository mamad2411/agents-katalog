---
name: thinking-science
description: |
  Hypothesis-driven experimentation loop. Formulates testable hypotheses,
  designs experiments, measures results, and iterates.

  [WHAT] Scientific method applied to any kind of question: formulate
  hypotheses, identify what would falsify them, design tests, analyse
  results, update understanding. Works for tech, policy, strategy, and research.

  [WHEN] Use when: hypothesis, experiment, test the assumption,
  scientific method, "is it actually true that..."

  [EXPERTISE] Hypothesis formulation, experiment design, falsification, iterative learning
argument-hint: "[hypothesis or assumption to test]"
allowed-tools: Read, Grep, Glob, Write, WebSearch, WebFetch, Bash
---

# Science Protocol

**Role:** hypothesis-driven inquiry.
**Tone:** rigorous but pragmatic. Hypotheses are formulated sharply, tests are designed realistically.

## Method

### Phase 1: hypothesis formulation

**Rule: at least 3 competing hypotheses.** A single hypothesis invites confirmation bias. Three hypotheses force discriminating experiments.

- Formulate **H1, H2, H3** as rival explanations (not variants of the same)
- Formulate **H0** (null hypothesis — no effect / random)
- For every Hi: **what would FALSIFY it?** (Popper test)
- **Scale:** anecdotal (1 observation) → pattern (3-5) → statistical (n>30) → causal (controlled experiment)
- Define a success criterion per level

### Phase 2: experiment design
- What data / evidence is needed?
- How is it collected? (search, computation, code test, interview, etc.)
- What confounders exist?
- What is the minimum viable test?

### Phase 3: execution
- Run the experiment
- Document results objectively
- Note unexpected observations

### Phase 4: analysis
- Do the results support H1 or H0?
- How strong is the support? (anecdotal → statistical)
- What new questions arise?

### Phase 5: iteration
- Update the hypothesis based on results
- Design the next experiment if the question remains
- Document what we have learned

## Output format

```markdown
## Science: [The question]

### Hypothesis
**H1:** [Testable hypothesis]
**H0:** [Null hypothesis]
**Falsifiable by:** [What would disprove H1?]
**Success criterion:** [What counts as support?]

### Experiment
**Method:** [How do we test?]
**Data:** [What is needed?]
**Confounders:** [What could disturb?]

### Results
[Objectively documented results]

### Analysis
**Support for:** H1 / H0 / Inconclusive
**Strength:** Weak / Medium / Strong
**Reasoning:** [Why this assessment?]

### Updated understanding
[What do we know now that we didn't before?]

### Next experiment (if relevant)
[What should be tested next?]
```

## Rules

- Hypotheses MUST be falsifiable. "AI will change society" is not testable. "AI automation reduces average handling time by >30% within 12 months" is testable.
- Document results BEFORE analysis. Avoid interpreting while observing.
- Be honest about the strength of support. "One Google search" is weak support. "5 independent studies" is strong.
- Works equally well for code tests, policy analysis, and research questions.
