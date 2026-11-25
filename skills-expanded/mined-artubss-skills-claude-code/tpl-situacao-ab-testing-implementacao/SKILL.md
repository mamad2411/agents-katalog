---
name: tpl-situacao-ab-testing-implementacao
description: Template do pack (situacao/17-ab-testing-implementacao.md). Orienta o agente em tarefas situacionais como debug, seguranca e refactor alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: situacao/17-ab-testing-implementacao.md
  generated_by: install_pack_templates_as_claude_skills
---

# SITUATION: A/B Testing Implementation

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `situacao/17-ab-testing-implementacao.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## CONTEXT
Use this configuration when implementing A/B tests (split tests), multivariate tests, or feature flag-driven experiments. A/B testing is not just a marketing tool — it's an engineering discipline. Badly implemented experiments produce misleading data that leads to wrong product decisions. This configuration ensures statistical rigor, implementation correctness, and clean winner deployment.

## OBJECTIVES
- Run experiments that produce statistically valid and actionable results
- Prevent experiment pollution (interactions between experiments)
- Ensure consistent user assignment across sessions (sticky bucketing)
- Define success metrics and minimum sample size before starting
- Deploy winning variants cleanly and remove experiment code when done

## APPROACH RULES

1. **One variable at a time.** An A/B test must change exactly one variable. Changing button color AND copy in the same test makes it impossible to attribute the result. If you need to test multiple things, run sequential or multivariate tests with proper design.

2. **Define the success metric before starting.** What exactly will you measure? What minimum effect size would justify shipping? What sample size do you need to detect it? These answers must exist before traffic is split. Post-hoc metric selection is p-hacking.

3. **Calculate minimum sample size before starting.** Use a power calculator. Typical parameters: 80% statistical power, 95% confidence level, effect size based on minimum meaningful change. Never end an experiment early because "it looks good."

4. **Sticky bucketing is non-negotiable.** A user assigned to variant A must always see variant A. Assignment must be deterministic (hash of user ID + experiment ID), not random per request. Changing assignment mid-experiment invalidates the data.

5. **Guard against novelty effect.** New UI elements always get more clicks initially due to novelty. Run experiments for at least one full business cycle (usually 1-2 weeks minimum) to account for day-of-week effects and novelty decay.

6. **Stop experiments only when sample size is reached or for safety.** Do not stop when you see a positive result "too early." Do not keep running indefinitely. Automated stopping rules (sequential testing) are valid only if configured before the experiment starts.

7. **Clean up experiment code.** A winner means: remove the losing variant, remove the feature flag, promote the winning code to be the permanent implementation. Technical debt from undead experiments compounds quickly.

## ROUTING TABLE

| If you encounter | Then |
|-----------------|------|
| "Let's just run it and see" | Stop. Define hypothesis, primary metric, and sample size first. |
| Experiment changing 2+ things at once | Split into separate sequential experiments or design as a proper multivariate test |
| Sample size < calculated minimum | Do not analyze. Continue running until sample size is reached. |
| User seeing different variants across sessions | Sticky bucketing is broken. Fix assignment logic before results are valid. |
| Metric improving but only for 3 days | Novelty effect suspected. Continue to 2 full weeks. |
| "It's significant! Let's ship!" | Verify: correct one-tailed vs two-tailed test, no data leakage between variants, experiment ran full duration |
| Two experiments running on same page/flow | Experiment interaction risk. Analyze interaction effects or serialize experiments. |
| Winning variant deployed but flag left on | Remove the flag, remove the losing variant code. Experiment must be fully cleaned up. |
| No holdback group defined | For long-running experiments, maintain a holdback (no change) to measure long-term effects. |
| Bot/spider traffic included in experiment | Filter non-human traffic before analysis. It inflates sample size and dilutes signal. |

## Experiment Design Template

```markdown
## Experiment: [Name]

**Hypothesis:**
If we [change X], then [metric Y] will [increase/decrease] by [Z%],
because [user psychology/behavior reason].

**Variants:**
- Control (A): [Current behavior - describe precisely]
- Variant B: [What changes - describe precisely]

**Primary Metric:** [One metric. If you have multiple, pick the most important.]
- Checkout completion rate

**Secondary Metrics (monitoring, not decision):**
- Revenue per visitor
- Bounce rate
- Time on page

**Guardrail Metrics (must not degrade):**
- Site error rate
- Page load time P95

**Minimum Detectable Effect:** 5% relative improvement
**Statistical Power:** 80%
**Confidence Level:** 95%
**Required Sample Size:** 12,400 users per variant (calculated via power analysis)
**Estimated Duration:** 10 days at current traffic volume

**Traffic Split:** 50% control / 50% variant
**Targeting:** All logged-in users on checkout page

**Assignment:** hash(user_id + "experiment_checkout_cta_v2") % 100 < 50 → control

**Start Date:** [date]
**Minimum End Date:** [start + duration. Never end before this.]
**Decision Date:** [start + duration + 2 days analysis buffer]
```

## Feature Flag Architecture

```typescript
interface ExperimentAssignment {
  variant: 'control' | 'treatment'
  experimentId: string
  userId: string
  assignedAt: string
}

class ExperimentService {
  /**
   * Deterministic, sticky assignment using user ID hash.
   * Same user always gets same variant for same experiment.
   */
  getVariant(userId: string, experimentId: string): 'control' | 'treatment' {
    // Hash must be consistent — not time-dependent
    const hash = murmurhash(`${userId}:${experimentId}`)
    const bucket = hash % 100
    
    const experiment = this.getExperiment(experimentId)
    
    if (!experiment || !experiment.isActive) {
      return 'control' // Default: show control when no experiment
    }
    
    return bucket < experiment.treatmentPercentage ? 'treatment' : 'control'
  }

  /** Always log assignments for analysis */
  assignAndLog(userId: string, experimentId: string): ExperimentAssignment {
    const variant = this.getVariant(userId, experimentId)
    
    const assignment: ExperimentAssignment = {
      variant,
      experimentId,
      userId,
      assignedAt: new Date().toISOString()
    }
    
    // Log once per user per experiment (not every request)
    if (!this.hasLoggedAssignment(userId, experimentId)) {
      this.analyticsClient.track('experiment_enrolled', assignment)
      this.cacheAssignment(userId, experimentId)
    }
    
    return assignment
  }
}
```

## Statistical Analysis

```python
from scipy import stats
import numpy as np

def analyze_ab_test(
    control_conversions: int, 
    control_visitors: int,
    treatment_conversions: int,
    treatment_visitors: int,
    alpha: float = 0.05
) -> dict:
    """Returns analysis result with clear ship/no-ship recommendation."""
    
    control_rate = control_conversions / control_visitors
    treatment_rate = treatment_conversions / treatment_visitors
    relative_lift = (treatment_rate - control_rate) / control_rate
    
    # Two-proportion z-test
    stat, p_value = stats.proportions_ztest(
        [treatment_conversions, control_conversions],
        [treatment_visitors, control_visitors]
    )
    
    is_significant = p_value < alpha
    
    return {
        'control_rate': f"{control_rate:.2%}",
        'treatment_rate': f"{treatment_rate:.2%}",
        'relative_lift': f"{relative_lift:+.1%}",
        'p_value': round(p_value, 4),
        'is_significant': is_significant,
        'recommendation': 'SHIP' if (is_significant and relative_lift > 0) else 'NO_SHIP',
        'confidence': f"{(1-p_value)*100:.1f}%"
    }
```

## DO NOT

- **DO NOT** analyze results before minimum sample size is reached
- **DO NOT** change the primary metric after the experiment starts
- **DO NOT** run an experiment on < 1 week of data (day-of-week effects)
- **DO NOT** make a decision based on secondary metrics if the primary metric is flat
- **DO NOT** leave losing variant code in the codebase after concluding the experiment
- **DO NOT** count the same user's sessions as independent samples
- **DO NOT** run experiments on new or infrequent users only (survivorship bias)
- **DO NOT** include bot/crawler traffic in experiment analysis

## OUTPUT FORMAT

At experiment conclusion, produce an **Experiment Report:**

```markdown
## Experiment Report: [Name]

**Duration:** 2024-01-01 to 2024-01-14 (14 days)
**Total Visitors:** 28,400 (14,200 per variant)

### Results

| Variant | Visitors | Conversions | Rate | vs Control |
|---------|----------|-------------|------|-----------|
| Control | 14,200 | 852 | 6.00% | — |
| Treatment | 14,200 | 924 | 6.51% | +8.4% |

**p-value:** 0.023 (statistically significant at 95% confidence)
**Relative Lift:** +8.4% on checkout completion rate

### Decision: **SHIP TREATMENT** ✅

### Next Steps
- [ ] Deploy treatment as permanent implementation
- [ ] Remove control variant code
- [ ] Archive experiment config (keep 90 days for reference)
- [ ] Remove feature flag
- [ ] Document learnings in team wiki
```

## QUALITY GATES

- [ ] Hypothesis written before experiment starts
- [ ] Primary metric defined before experiment starts
- [ ] Sample size calculated with power analysis before starting
- [ ] Minimum experiment duration respected (no early stopping except safety)
- [ ] Sticky bucketing verified: same user always gets same variant
- [ ] Bot traffic excluded from analysis
- [ ] One primary metric — not "any of these 5 look good"
- [ ] Both losing variant code AND feature flag removed after conclusion
- [ ] Experiment report documented and accessible to product/leadership
- [ ] Guardrail metrics checked: no degradation in error rate or performance
