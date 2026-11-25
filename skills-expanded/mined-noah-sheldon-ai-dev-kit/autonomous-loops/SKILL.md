---
name: autonomous-loops
description: Autonomous loop patterns: self-improving workflows, continuous feedback loops, quality gates, loop termination conditions, retry strategies, bounded iteration, and convergence detection.
origin: AI Dev Kit
disable-model-invocation: false
---

# Autonomous Loops

Patterns for building self-improving, bounded autonomous loops: continuous feedback cycles, quality gates, convergence detection, retry strategies, loop health monitoring, and safe termination conditions.

## When to Use

- Building self-correcting agent workflows that iterate until quality thresholds are met
- Implementing retry loops with exponential backoff and jitter
- Designing convergence detection (stop when improvements plateau)
- Creating quality-gated iteration (loop until lint/test/quality checks pass)
- Building bounded iteration with hard limits to prevent runaway loops
- Implementing progressive refinement (draft → review → revise → finalize)

## Core Concepts

### 1. Loop Anatomy

Every autonomous loop has four phases:

```
┌─────────┐    ┌──────────┐    ┌───────────┐    ┌────────────┐
│  GENERATE│───▶│ VALIDATE │───▶│  IMPROVE  │───▶│ TERMINATE? │
│          │    │          │    │           │    │            │
│ - Draft  │    │ - Quality│    │ - Diff    │    │ - Converged│
│ - Plan   │    │   gates  │    │ - Fix     │    │ - Max iters│
│ - Execute│    │ - Score  │    │ - Retry   │    │ - Timed out│
└─────────┘    └──────────┘    └───────────┘    └────────────┘
       ▲                                                    │
       │              ┌───────────┐                         │
       └──────────────│  LOG &   │◀────────────────────────┘
                      │  METRICS │
                      └──────────┘
```

### 2. Bounded Iteration Loop

**Python — Generic Autonomous Loop with Quality Gates:**

```python
from dataclasses import dataclass, field
from typing import Callable, Any
from enum import Enum
import logging
import time

logger = logging.getLogger(__name__)


class LoopExitReason(Enum):
    CONVERGED = "converged"
    MAX_ITERATIONS = "max_iterations"
    TIMEOUT = "timeout"
    QUALITY_PASSED = "quality_passed"
    QUALITY_FAILED = "quality_failed"
    ERROR = "error"


@dataclass
class LoopState:
    """Carries mutable state through loop iterations."""
    iteration: int = 0
    score: float = 0.0
    previous_score: float = 0.0
    result: Any = None
    errors: list[str] = field(default_factory=list)
    exit_reason: LoopExitReason | None = None
    started_at: float = field(default_factory=time.time)


@dataclass
class LoopConfig:
    max_iterations: int = 10
    convergence_threshold: float = 0.01  # Score delta below which we stop improving
    quality_threshold: float = 0.85      # Minimum acceptable score
    timeout_seconds: float = 300.0       # 5 minute hard limit
    backoff_base: float = 1.0            # Retry backoff base seconds
    backoff_max: float = 30.0            # Max backoff seconds


def autonomous_loop(
    generate_fn: Callable[[LoopState], Any],
    validate_fn: Callable[[Any], dict],   # Returns {"score": 0.0-1.0, "passed": bool, "feedback": str}
    improve_fn: Callable[[Any, dict], Any],  # Takes result + feedback, returns improved result
    config: LoopConfig = LoopConfig(),
) -> LoopState:
    """
    Run a bounded autonomous loop with quality gates and convergence detection.

    The loop continues until one of:
    - Quality gate passes (score >= threshold)
    - Score converges (delta < convergence_threshold for 2 consecutive iters)
    - Max iterations reached
    - Timeout exceeded
    """
    state = LoopState()

    while True:
        # Timeout check
        elapsed = time.time() - state.started_at
        if elapsed > config.timeout_seconds:
            state.exit_reason = LoopExitReason.TIMEOUT
            logger.warning("Loop timed out after %.1fs at iteration %d", elapsed, state.iteration)
            break

        # Max iterations check
        if state.iteration >= config.max_iterations:
            state.exit_reason = LoopExitReason.MAX_ITERATIONS
            logger.warning("Loop hit max iterations (%d), best score: %.3f",
                          config.max_iterations, state.score)
            break

        state.iteration += 1
        logger.info("=== Loop iteration %d/%d (score: %.3f) ===",
                    state.iteration, config.max_iterations, state.score)

        # Phase 1: Generate / Execute
        try:
            if state.iteration == 1:
                state.result = generate_fn(state)
            else:
                # On subsequent iterations, improve based on previous feedback
                feedback = {"score": state.score, "errors": state.errors}
                state.result = improve_fn(state.result, feedback)
        except Exception as e:
            state.errors.append(str(e))
            logger.error("Generation failed at iteration %d: %s", state.iteration, e)
            state.exit_reason = LoopExitReason.ERROR
            break

        # Phase 2: Validate
        try:
            validation = validate_fn(state.result)
            state.previous_score = state.score
            state.score = validation["score"]
            state.errors = validation.get("errors", [])
        except Exception as e:
            state.errors = [str(e)]
            state.score = 0.0
            logger.error("Validation failed at iteration %d: %s", state.iteration, e)

        # Phase 3: Check exit conditions

        # Quality gate passed
        if validation.get("passed", False) and state.score >= config.quality_threshold:
            state.exit_reason = LoopExitReason.QUALITY_PASSED
            logger.info("Quality gate passed: score %.3f >= %.3f",
                       state.score, config.quality_threshold)
            break

        # Convergence detection (score not improving meaningfully)
        if state.iteration >= 2:
            score_delta = abs(state.score - state.previous_score)
            if score_delta < config.convergence_threshold:
                state.exit_reason = LoopExitReason.CONVERGED
                logger.info("Score converged at %.3f (delta: %.4f < %.4f)",
                           state.score, score_delta, config.convergence_threshold)
                break

        # Quality validation failed catastrophically
        if state.score < 0.1 and state.iteration >= 3:
            state.exit_reason = LoopExitReason.QUALITY_FAILED
            logger.error("Score too low (%.3f) after %d iterations, aborting",
                        state.score, state.iteration)
            break

        # Backoff before next iteration (avoids hammering resources)
        backoff = min(config.backoff_base * (2 ** (state.iteration - 1)), config.backoff_max)
        logger.debug("Backoff: %.1fs", backoff)
        time.sleep(backoff)

    logger.info("Loop exited: %s (iterations: %d, final score: %.3f, elapsed: %.1fs)",
                state.exit_reason.value, state.iteration, state.score,
                time.time() - state.started_at)

    return state
```

### 3. Quality Gates

Quality gates are the loop's decision function. Each gate produces a normalized score (0.0-1.0) and a pass/fail verdict.

```python
from dataclasses import dataclass


@dataclass
class QualityGateResult:
    score: float           # 0.0 to 1.0
    passed: bool           # Above threshold?
    feedback: str          # Human-readable feedback
    errors: list[str] = field(default_factory=list)


def composite_quality_gate(
    checks: list[tuple[Callable, float]],  # (check_fn, weight)
    result: Any,
) -> QualityGateResult:
    """Combine multiple quality checks into a weighted score."""
    total_weight = sum(w for _, w in checks)
    weighted_sum = 0.0

    for check_fn, weight in checks:
        try:
            check_result = check_fn(result)
            weighted_sum += check_result * weight
        except Exception as e:
            weighted_sum += 0.0 * weight  # Failed check = 0 score
    score = weighted_sum / total_weight if total_weight > 0 else 0.0

    return QualityGateResult(
        score=score,
        passed=score >= 0.85,
        feedback=f"Composite quality score: {score:.3f}",
    )


# Example checks for code generation loop
def check_tests_pass(result: dict) -> float:
    """0.0 if tests fail, 1.0 if all pass."""
    test_results = result.get("test_results", {})
    if test_results.get("failed", 0) > 0:
        return 0.0
    return 1.0


def check_lint_clean(result: dict) -> float:
    """0.0 if lint errors, 1.0 if clean, 0.5 if warnings only."""
    lint_results = result.get("lint_results", {})
    errors = lint_results.get("errors", 0)
    warnings = lint_results.get("warnings", 0)
    if errors > 0:
        return 0.0
    if warnings > 5:
        return 0.5
    return 1.0


def check_coverage(result: dict) -> float:
    """Linear score based on test coverage percentage."""
    coverage = result.get("coverage_pct", 0)
    return min(coverage / 80.0, 1.0)  # 80% = 1.0


def code_quality_gate(result: dict) -> float:
    """Single quality score for code output."""
    checks = [
        (check_tests_pass, 0.4),
        (check_lint_clean, 0.2),
        (check_coverage, 0.3),
        (lambda r: 1.0 if r.get("no_todos") else 0.5, 0.1),
    ]
    gate_result = composite_quality_gate(checks, result)
    return gate_result.score
```

### 4. Retry Strategies

Not all failures are equal. Different error types need different retry strategies.

**TypeScript — Smart Retry with Backoff and Jitter:**

```typescript
interface RetryConfig {
  maxAttempts: number;
  baseDelayMs: number;
  maxDelayMs: number;
  jitterFactor: number;  // 0.0-1.0, adds randomness to avoid thundering herd
  retryableErrors: string[];  // Only retry these error types
}

const DEFAULT_RETRY_CONFIG: RetryConfig = {
  maxAttempts: 5,
  baseDelayMs: 1000,
  maxDelayMs: 30000,
  jitterFactor: 0.25,
  retryableErrors: ["TIMEOUT", "RATE_LIMIT", "NETWORK_ERROR", "TEMPORARY_FAILURE"],
};

function isRetryable(error: Error, config: RetryConfig): boolean {
  return config.retryableErrors.some(
    (code) => error.message.includes(code) || error.name.includes(code),
  );
}

function calculateBackoff(attempt: number, config: RetryConfig): number {
  // Exponential backoff with jitter
  const exponential = config.baseDelayMs * Math.pow(2, attempt - 1);
  const capped = Math.min(exponential, config.maxDelayMs);
  const jitter = capped * config.jitterFactor * (Math.random() - 0.5) * 2;
  return Math.max(0, capped + jitter);
}

async function smartRetry<T>(
  fn: () => Promise<T>,
  config: RetryConfig = DEFAULT_RETRY_CONFIG,
): Promise<T> {
  let lastError: Error | undefined;

  for (let attempt = 1; attempt <= config.maxAttempts; attempt++) {
    try {
      const result = await fn();

      if (attempt > 1) {
        console.log(`[retry] Succeeded on attempt ${attempt}/${config.maxAttempts}`);
      }
      return result;
    } catch (error: unknown) {
      lastError = error instanceof Error ? error : new Error(String(error));

      if (!isRetryable(lastError, config)) {
        throw lastError;  // Non-retryable — fail immediately
      }

      if (attempt === config.maxAttempts) {
        break;  // Will throw after loop
      }

      const delay = calculateBackoff(attempt, config);
      console.warn(
        `[retry] Attempt ${attempt}/${config.maxAttempts} failed: ${lastError.message}. ` +
        `Retrying in ${Math.round(delay)}ms`,
      );
      await sleep(delay);
    }
  }

  throw new Error(
    `Failed after ${config.maxAttempts} attempts. Last error: ${lastError?.message}`,
  );
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// Usage: retry with specific config for rate-limited APIs
const rateLimitedRetry: RetryConfig = {
  ...DEFAULT_RETRY_CONFIG,
  maxAttempts: 8,
  baseDelayMs: 2000,
  maxDelayMs: 60000,
  retryableErrors: ["RATE_LIMIT", "429", "TIMEOUT"],
};

const response = await smartRetry(() => fetchWithRateLimit("/api/generate"), rateLimitedRetry);
```

### 5. Convergence Detection

Detect when the loop stops making meaningful progress and terminate early.

```python
class ConvergenceDetector:
    """Detects when a metric has stopped improving meaningfully."""

    def __init__(
        self,
        window: int = 3,              # Look at last N iterations
        threshold: float = 0.01,      # Delta below which considered converged
        min_iterations: int = 3,      # Don't converge before this
    ):
        self.history: list[float] = []
        self.window = window
        self.threshold = threshold
        self.min_iterations = min_iterations

    def add_score(self, score: float) -> None:
        self.history.append(score)

    def is_converged(self) -> bool:
        """Check if scores have stabilized within the threshold."""
        if len(self.history) < self.min_iterations:
            return False

        recent = self.history[-self.window:]
        if len(recent) < 2:
            return False

        # Check consecutive deltas
        deltas = [abs(recent[i] - recent[i-1]) for i in range(1, len(recent))]
        return all(d < self.threshold for d in deltas)

    def trend(self) -> str:
        """Return 'improving', 'degrading', or 'stable'."""
        if len(self.history) < 2:
            return "unknown"
        delta = self.history[-1] - self.history[-2]
        if delta > self.threshold:
            return "improving"
        elif delta < -self.threshold:
            return "degrading"
        return "stable"


# Usage in a loop
detector = ConvergenceDetector(window=3, threshold=0.02)

for i in range(10):
    score = evaluate(current_result)
    detector.add_score(score)

    if detector.is_converged():
        print(f"Converged at iteration {i+1}, score={score:.3f}, trend={detector.trend()}")
        break
```

### 6. Loop Health Monitoring

Track loop metrics to detect problematic patterns (oscillation, runaway, degradation).

```python
from dataclasses import dataclass, field


@dataclass
class LoopHealthMetrics:
    """Tracks health metrics across loop iterations."""
    scores: list[float] = field(default_factory=list)
    iteration_times: list[float] = field(default_factory=list)
    error_counts: list[int] = field(default_factory=list)

    @property
    def is_oscillating(self) -> bool:
        """Score is bouncing up and down without progress."""
        if len(self.scores) < 4:
            return False
        recent = self.scores[-4:]
        # Check for alternating up/down pattern
        directions = [recent[i] < recent[i+1] for i in range(len(recent)-1)]
        return all(directions[i] != directions[i+1] for i in range(len(directions)-1))

    @property
    def is_degrading(self) -> bool:
        """Last 3 iterations show consistent decline."""
        if len(self.scores) < 3:
            return False
        recent = self.scores[-3:]
        return all(recent[i] > recent[i+1] for i in range(len(recent)-1))

    @property
    def is_slowing_down(self) -> bool:
        """Iteration times are increasing."""
        if len(self.iteration_times) < 3:
            return False
        recent = self.iteration_times[-3:]
        return all(recent[i] < recent[i+1] for i in range(len(recent)-1))

    def summary(self) -> str:
        issues = []
        if self.is_oscillating:
            issues.append("OSCILLATING")
        if self.is_degrading:
            issues.append("DEGRADING")
        if self.is_slowing_down:
            issues.append("SLOWING")
        if issues:
            return f"⚠️ Loop health issues: {', '.join(issues)}"
        return "✅ Loop healthy"
```

## Workflow: Progressive Refinement Loop

A concrete pattern for code improvement loops:

```
Iteration 1: Generate initial draft
Iteration 2: Fix lint errors
Iteration 3: Fix failing tests
Iteration 4: Improve edge cases
Iteration 5: Optimize performance
...
```

```python
def progressive_refinement_loop(
    task: str,
    initial_draft: str,
    config: LoopConfig = LoopConfig(max_iterations=10),
) -> LoopState:
    """Iteratively refine code through quality-gated improvement."""

    def generate(state: LoopState) -> dict:
        return {"code": initial_draft, "task": task}

    def validate(result: dict) -> dict:
        code = result["code"]
        # Run actual checks
        test_result = run_tests(code)
        lint_result = run_linter(code)
        coverage = measure_coverage(code)

        score = code_quality_gate({
            "test_results": test_result,
            "lint_results": lint_result,
            "coverage_pct": coverage,
            "no_todos": "TODO" not in code and "FIXME" not in code,
        })

        feedback_parts = []
        if test_result.get("failed", 0) > 0:
            feedback_parts.append(f"{test_result['failed']} failing tests")
        if lint_result.get("errors", 0) > 0:
            feedback_parts.append(f"{lint_result['errors']} lint errors")
        if coverage < 80:
            feedback_parts.append(f"Low coverage: {coverage}%")

        return {
            "score": score,
            "passed": score >= 0.85,
            "feedback": "; ".join(feedback_parts) if feedback_parts else "All checks passed",
            "errors": feedback_parts,
        }

    def improve(result: dict, feedback: dict) -> dict:
        # Feed errors back into the generator for targeted fixes
        code = result["code"]
        task = result["task"]
        improvement_prompt = (
            f"Fix these issues in the code:\n{feedback.get('feedback', 'Unknown issues')}\n\n"
            f"Current code:\n{code}\n\n"
            f"Return only the improved code."
        )
        improved_code = llm_generate(improvement_prompt, max_tokens=4000)
        return {"code": improved_code, "task": task}

    return autonomous_loop(generate, validate, improve, config)
```

## Anti-Patterns

| Anti-Pattern | Symptom | Fix |
|---|---|---|
| No hard stop | Infinite loops, runaway costs | Always set max_iterations + timeout |
| No backoff | API rate limit bans | Exponential backoff with jitter |
| Retrying everything | Wasting attempts on permanent errors | Only retry retryable error types |
| No convergence check | Continuing after plateau | Track score deltas, stop when stable |
| Single quality metric | Passing one check, failing others | Composite weighted quality gate |
| No health monitoring | Undetected oscillation/degradation | Track trends, alert on anomalies |
| Blind iteration | Loop doesn adapt to feedback | Feed validation errors back to generator |

## Success Checklist

- [ ] Hard iteration limit set (max_iterations)
- [ ] Hard timeout configured (timeout_seconds)
- [ ] Quality gate with composite scoring defined
- [ ] Convergence detector active
- [ ] Exponential backoff with jitter configured
- [ ] Only retryable errors trigger retries
- [ ] Loop health metrics tracked (oscillation, degradation, slowdown)
- [ ] Every iteration logged with score and duration
- [ ] Exit reason recorded (converged, max_iterations, timeout, quality)
- [ ] Best result preserved even if loop exits without passing
