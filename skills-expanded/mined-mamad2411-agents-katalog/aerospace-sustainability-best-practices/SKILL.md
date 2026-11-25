---
name: aerospace-sustainability-best-practices
description: Use when applying aerospace sustainability best practices.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [aerospace, green, sustainability]
---

# Aerospace Sustainability Best Practices

"Use when applying aerospace sustainability best practices."

## Trigger

Activate this skill when the user mentions:
- aerospace,  green,  sustainability workflows or issues
- Building, fixing, or optimizing aerospace sustainability best practices
- Questions about aerospace best practices

## Core Concepts

- Model selection and evaluation
- Feature engineering and data prep
- Training methodology
- Deployment and serving patterns
- Monitoring and drift detection

## Step-by-Step Workflow

1. **Frame** — Define problem, success metric, baseline
   - Expected: Clear problem statement
2. **Explore** — EDA, feature analysis
   - Expected: Understanding of data relationships
3. **Build** — Train models, track experiments
   - Expected: Logged reproducible experiments
4. **Evaluate** — Test on holdout, check bias
   - Expected: Evaluation report with confidence
5. **Deploy** — Serve with monitoring
   - Expected: Production model with drift detection

## Tools & Technologies

- Experiment tracking
- Model registry
- Feature store
- Model serving

## Best Practices

- Document decisions and rationale (ADRs, design docs, runbooks)
- Version everything - code, configs, data, and documentation
- Test incrementally; never claim passing without verification
- Respect domain-specific regulations and ethical standards
- Measure outcomes with meaningful metrics

## Common Pitfalls

- **Data leakage** → Overly optimistic metrics → Strict temporal splits
- **No monitoring** → Silent degradation → Monitor prediction distribution

## Tags

`aerospace, green, sustainability`

---

*LoopyLuci/Skills - 2026-09-24*
