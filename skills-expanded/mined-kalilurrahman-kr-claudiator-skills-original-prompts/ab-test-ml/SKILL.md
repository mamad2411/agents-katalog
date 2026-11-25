---
name: ab-test-ml
description: Design and analyze A/B tests for ML models in production, including traffic splitting, metric selection, statistical significance testing, and safe rollout strategies.
argument-hint: [model type, business metric, traffic volume, acceptable risk level]
allowed-tools: Read, Write, Bash
---

# A/B Testing for ML Models

Testing ML models in production is fundamentally different from testing features — model behavior is probabilistic, metrics are delayed, and interactions between models complicate attribution. Rigorous A/B testing is the only way to know if a new model actually moves business metrics.

## Process

1. **Define the hypothesis** — what improvement does the challenger model provide and how?
2. **Choose the primary metric** — one business metric (revenue, conversion, retention), not ML metrics.
3. **Power analysis** — calculate required sample size for statistical significance.
4. **Design traffic split** — percentage, assignment unit (user/session/item), exclusions.
5. **Implement model routing** — shadow, canary, or full A/B.
6. **Run until significance** — don't stop early; use sequential testing if needed.
7. **Analyze results** — primary + guardrail metrics, segment breakdowns.
8. **Make deployment decision** — ship, iterate, or rollback with documented rationale.

## Output Format

### Experiment Design

```python
# experiment_design.py
import numpy as np
from scipy import stats
from dataclasses import dataclass
from typing import Optional

@dataclass
class ExperimentDesign:
    name: str
    hypothesis: str
    primary_metric: str
    guardrail_metrics: list[str]
    baseline_value: float
    minimum_detectable_effect: float  # MDE — smallest meaningful difference
    statistical_power: float = 0.80
    significance_level: float = 0.05
    traffic_pct: float = 0.50          # Fraction of traffic in experiment
    
    def required_sample_size(self) -> dict:
        """Calculate required sample size per arm for two-sample test."""
        # Effect size (Cohen's d for continuous, relative risk for proportions)
        if self.baseline_value < 1.0:  # Proportion metric (conversion rate)
            effect = self.minimum_detectable_effect
            p1 = self.baseline_value
            p2 = p1 * (1 + effect)
            
            # Two-proportion z-test
            from statsmodels.stats.power import NormalIndPower
            pooled = (p1 + p2) / 2
            h = 2 * np.arcsin(np.sqrt(p2)) - 2 * np.arcsin(np.sqrt(p1))  # Cohen's h
            
            analysis = NormalIndPower()
            n = analysis.solve_power(
                effect_size=h,
                alpha=self.significance_level,
                power=self.statistical_power,
                alternative='two-sided'
            )
        else:  # Continuous metric (revenue, time-on-site)
            # Assume 30% CV (coefficient of variation) if not provided
            std = self.baseline_value * 0.30
            delta = self.baseline_value * self.minimum_detectable_effect
            
            from statsmodels.stats.power import TTestIndPower
            analysis = TTestIndPower()
            n = analysis.solve_power(
                effect_size=delta / std,
                alpha=self.significance_level,
                power=self.statistical_power,
                alternative='two-sided'
            )
        
        n_per_arm = int(np.ceil(n))
        total = n_per_arm * 2
        
        return {
            "n_per_arm": n_per_arm,
            "total_needed": total,
            "traffic_pct": self.traffic_pct,
        }
    
    def estimated_runtime_days(self, daily_eligible_users: int) -> float:
        """Estimate how long the experiment needs to run."""
        size = self.required_sample_size()
        daily_in_experiment = daily_eligible_users * self.traffic_pct
        return size["total_needed"] / daily_in_experiment


# Example: recommendation model A/B test
design = ExperimentDesign(
    name="rec-model-v2-ab-test",
    hypothesis="New recommendation model increases click-through rate by 5%",
    primary_metric="click_through_rate",
    guardrail_metrics=["revenue_per_user", "session_duration", "error_rate"],
    baseline_value=0.12,              # 12% baseline CTR
    minimum_detectable_effect=0.05,   # 5% relative improvement = 12.6% CTR
    traffic_pct=0.20,                 # 20% in experiment (10% each arm)
)

sizing = design.required_sample_size()
runtime = design.estimated_runtime_days(daily_eligible_users=100_000)

print(f"Required: {sizing['n_per_arm']:,} per arm, {sizing['total_needed']:,} total")
print(f"Estimated runtime: {runtime:.1f} days")
```

### Traffic Splitting & Model Routing

```python
# routing/model_router.py
import hashlib
import mlflow
from typing import Optional
from enum import Enum

class VariantAssignment(Enum):
    CONTROL = "control"
    TREATMENT = "treatment"
    SHADOW = "shadow"       # Runs both, uses control output

class ModelRouter:
    """
    Routes requests to control (champion) or treatment (challenger) model.
    Uses deterministic hashing for sticky assignment.
    """
    
    def __init__(
        self,
        experiment_id: str,
        treatment_pct: float = 0.10,   # 10% to challenger
        assignment_unit: str = "user_id",
        shadow_mode: bool = False
    ):
        self.experiment_id = experiment_id
        self.treatment_pct = treatment_pct
        self.assignment_unit = assignment_unit
        self.shadow_mode = shadow_mode
        
        # Load both models
        self.control_model = mlflow.pyfunc.load_model("models:/rec-model/Production")
        self.treatment_model = mlflow.pyfunc.load_model("models:/rec-model/Staging")
    
    def assign_variant(self, unit_id: str) -> VariantAssignment:
        """Deterministic, sticky assignment using hash."""
        hash_input = f"{self.experiment_id}:{unit_id}".encode()
        hash_value = int(hashlib.md5(hash_input).hexdigest(), 16)
        bucket = (hash_value % 1000) / 1000  # 0.0 to 0.999
        
        if bucket < self.treatment_pct:
            return VariantAssignment.TREATMENT
        return VariantAssignment.CONTROL
    
    async def predict(self, user_id: str, features: dict) -> dict:
        variant = self.assign_variant(user_id)
        
        if self.shadow_mode:
            # Shadow: run both, return control output
            control_result = await self._run_model(self.control_model, features)
            treatment_result = await self._run_model(self.treatment_model, features)
            
            self._log_shadow_comparison(user_id, control_result, treatment_result)
            return {**control_result, "variant": "shadow-control"}
        
        if variant == VariantAssignment.TREATMENT:
            result = await self._run_model(self.treatment_model, features)
        else:
            result = await self._run_model(self.control_model, features)
        
        # Log assignment for analysis
        self._log_assignment(user_id, variant.value, result)
        
        return {**result, "variant": variant.value, "experiment_id": self.experiment_id}
    
    async def _run_model(self, model, features: dict) -> dict:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, model.predict, features)
    
    def _log_assignment(self, user_id: str, variant: str, predictions: dict):
        """Log to experiment tracking for analysis."""
        event_bus.publish("ml.experiment.assignment", {
            "experiment_id": self.experiment_id,
            "user_id": user_id,
            "variant": variant,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model_output_hash": hashlib.md5(
                str(predictions).encode()
            ).hexdigest()[:8],
        })
    
    def _log_shadow_comparison(self, user_id: str, control: dict, treatment: dict):
        """Compare outputs in shadow mode without affecting production."""
        metrics.histogram(
            "shadow_prediction_diff",
            value=compute_output_distance(control, treatment),
            tags={"experiment": self.experiment_id}
        )
```

### Statistical Analysis

```python
# analysis/experiment_analyzer.py
import pandas as pd
import numpy as np
from scipy import stats
from dataclasses import dataclass
from typing import Optional

@dataclass
class ExperimentResult:
    metric: str
    control_mean: float
    treatment_mean: float
    relative_lift: float
    p_value: float
    confidence_interval_lower: float
    confidence_interval_upper: float
    is_significant: bool
    is_practically_significant: bool  # Meets MDE threshold
    sample_size_control: int
    sample_size_treatment: int
    recommendation: str

class ExperimentAnalyzer:
    def __init__(
        self,
        significance_level: float = 0.05,
        mde: float = 0.05
    ):
        self.alpha = significance_level
        self.mde = mde
    
    def analyze(
        self,
        df: pd.DataFrame,
        metric_col: str,
        variant_col: str = "variant",
        control_label: str = "control",
        treatment_label: str = "treatment"
    ) -> ExperimentResult:
        """Analyze experiment results using two-sample t-test."""
        
        control = df[df[variant_col] == control_label][metric_col].dropna()
        treatment = df[df[variant_col] == treatment_label][metric_col].dropna()
        
        # Two-sample t-test
        statistic, p_value = stats.ttest_ind(control, treatment, equal_var=False)
        
        # Confidence interval for the difference
        diff = treatment.mean() - control.mean()
        se = np.sqrt(control.std()**2 / len(control) + treatment.std()**2 / len(treatment))
        ci_margin = stats.t.ppf(1 - self.alpha/2, df=len(control) + len(treatment) - 2) * se
        
        relative_lift = (treatment.mean() - control.mean()) / control.mean()
        
        return ExperimentResult(
            metric=metric_col,
            control_mean=control.mean(),
            treatment_mean=treatment.mean(),
            relative_lift=relative_lift,
            p_value=p_value,
            confidence_interval_lower=diff - ci_margin,
            confidence_interval_upper=diff + ci_margin,
            is_significant=p_value < self.alpha,
            is_practically_significant=abs(relative_lift) >= self.mde,
            sample_size_control=len(control),
            sample_size_treatment=len(treatment),
            recommendation=self._recommend(p_value, relative_lift)
        )
    
    def _recommend(self, p_value: float, lift: float) -> str:
        if p_value < self.alpha and lift >= self.mde:
            return "SHIP: Statistically and practically significant improvement"
        elif p_value < self.alpha and lift < 0:
            return "ROLLBACK: Statistically significant degradation"
        elif p_value >= self.alpha:
            return f"CONTINUE: Not yet significant (p={p_value:.3f})"
        else:
            return "ITERATE: Significant but below MDE threshold"
    
    def full_report(
        self,
        df: pd.DataFrame,
        primary_metric: str,
        guardrail_metrics: list[str],
    ) -> dict:
        
        primary = self.analyze(df, primary_metric)
        guardrails = [self.analyze(df, m) for m in guardrail_metrics]
        
        # Check guardrails: block ship if any guardrail is significantly degraded
        guardrail_failures = [
            g for g in guardrails
            if g.is_significant and g.relative_lift < -0.02  # >2% degradation
        ]
        
        overall_recommendation = primary.recommendation
        if guardrail_failures:
            overall_recommendation = f"BLOCK: {len(guardrail_failures)} guardrail(s) failed"
        
        return {
            "primary_metric": vars(primary),
            "guardrail_metrics": [vars(g) for g in guardrails],
            "guardrail_failures": [g.metric for g in guardrail_failures],
            "overall_recommendation": overall_recommendation,
            "run_duration_days": (df["timestamp"].max() - df["timestamp"].min()).days,
        }


# Usage
df = pd.read_parquet("s3://experiment-data/rec-model-v2-ab-test/results.parquet")
analyzer = ExperimentAnalyzer(significance_level=0.05, mde=0.05)

report = analyzer.full_report(
    df=df,
    primary_metric="click_through_rate",
    guardrail_metrics=["revenue_per_user", "session_duration", "error_rate"]
)

print(f"Recommendation: {report['overall_recommendation']}")
print(f"CTR lift: {report['primary_metric']['relative_lift']:.2%}")
print(f"P-value: {report['primary_metric']['p_value']:.4f}")
```

### Experiment Registry

```yaml
# experiments/rec-model-v2.yaml — version-controlled experiment spec
name: rec-model-v2-ab-test
description: "Test new collaborative filtering model vs. baseline matrix factorization"
created_by: ml-team@example.com
created_at: 2024-01-15

hypothesis: "New model improves CTR by 5% through better user embedding representation"

model:
  control: "rec-model/Production (v8)"
  treatment: "rec-model/Staging (v9)"

traffic:
  total_pct: 20              # 20% of eligible users in experiment
  control_split: 50          # 50/50 within experiment
  treatment_split: 50
  assignment_unit: user_id   # Sticky by user
  eligible_filter: "registered_users_30d_active"
  excluded: ["new_users", "enterprise_accounts"]

metrics:
  primary: click_through_rate
  guardrails:
    - revenue_per_user         # No revenue regression
    - session_duration         # No engagement drop
    - error_rate               # No reliability issues
    - p99_latency_ms           # No latency regression

success_criteria:
  primary_metric_lift: 0.05     # 5% relative improvement
  p_value_threshold: 0.05
  guardrail_degradation_max: 0.02  # Max 2% degradation on guardrails

timeline:
  start_date: 2024-01-20
  minimum_runtime_days: 14    # Never stop before this
  expected_completion: 2024-02-10
  
status: running
```

## Rules

- **One primary metric** — multiple primary metrics cause multiple testing problems.
- **Pre-register the hypothesis** — define success criteria before looking at data.
- **Never stop early based on significance** — p-values fluctuate; run the full planned duration.
- **Guardrail metrics block shipping** — significant degradation in revenue or reliability blocks even a successful primary metric.
- **Sticky assignment** — users must always see the same variant; session-based assignment causes flip-flopping.
- **Exclude novelty effects** — first-week results often reflect novelty bias; analyze week 2+ separately.
- **Sample ratio mismatch check** — if treatment has 10% but you get 12%, the experiment is broken.
- **Segment analysis after significance** — don't hunt for winning segments before the primary metric is significant.
- **Document the decision** — the decision rationale (ship/rollback/iterate) is as valuable as the data.
- **Power analysis before starting** — never start an experiment you can't power within your timeline.
