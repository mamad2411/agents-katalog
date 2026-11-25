---
name: continuous-agent-loop
description: Continuous agent loop patterns: bounded automation loops, quality-gated iteration, loop health monitoring, termination criteria, human-in-the-loop gates, loop state management, failure recovery, and idempotent operations.
origin: AI Dev Kit
disable-model-invocation: false
---

# Continuous Agent Loop

Patterns for running autonomous agent loops with quality gates, health monitoring, human-in-the-loop gates, idempotent operations, failure recovery, and bounded execution. Builds on autonomous-loops but focuses on agent-specific orchestration.

## When to Use

- Building continuous agent workflows that iterate until quality thresholds are met
- Orchestrating multi-step agent tasks with validation between steps
- Implementing human approval gates in automated workflows
- Designing idempotent agent operations (safe to retry)
- Setting up loop health monitoring and anomaly detection
- Building failure recovery and state persistence
- Creating scheduled agent loops (cron-triggered automation)

## Core Concepts

### 1. Loop Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                        ORCHESTRATOR                                  │
│                                                                      │
│  ┌─────────┐    ┌──────────┐    ┌──────────┐    ┌────────────────┐  │
│  │ SCHEDULER│───▶│  AGENT   │───▶│ QUALITY  │───▶│ HUMAN GATE     │  │
│  │          │    │  STEP    │    │   GATE   │    │ (optional)     │  │
│  │ - Cron   │    │ - LLM    │    │ - Tests  │    │ - Approval     │  │
│  │ - Event  │    │ - Tools  │    │ - Lint   │    │ - Review       │  │
│  │ - Manual │    │ - State  │    │ - Score  │    │ - Override     │  │
│  └─────────┘    └──────────┘    └──────────┘    └───────┬────────┘  │
│                                                         │           │
│  ┌──────────────┐    ┌──────────┐    ┌──────────┐      │           │
│  │ STATE STORE  │◀───│ PERSIST  │◀───│ TERMINATE│◀─────┘           │
│  │ - Loop state │    │ - JSON   │    │ - Check  │                  │
│  │ - Step log   │    │ - DB     │    │ - Save   │                  │
│  │ - Metrics    │    │ - S3     │    │ - Report │                  │
│  └──────────────┘    └──────────┘    └──────────┘                  │
└──────────────────────────────────────────────────────────────────────┘
```

### 2. Idempotent Agent Operations

Every agent action must be **idempotent** — safe to execute multiple times with the same result. This is critical for retry logic and loop recovery.

**Python — Idempotent File Write:**

```python
import hashlib
import json
import os
import logging
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class IdempotentWriteResult:
    wrote: bool          # True if file was actually written
    skipped: bool        # True if content was identical (no-op)
    path: str
    content_hash: str


def idempotent_write(filepath: str, content: str) -> IdempotentWriteResult:
    """
    Write content to file only if it has changed.

    This is idempotent: running it multiple times with the same
    content produces the same filesystem state and returns skipped=True
    on subsequent calls.
    """
    path = Path(filepath)
    content_hash = hashlib.sha256(content.encode()).hexdigest()[:12]

    # Check if file exists with identical content
    if path.exists():
        existing = path.read_text()
        existing_hash = hashlib.sha256(existing.encode()).hexdigest()[:12]

        if content_hash == existing_hash:
            logger.debug("Skipping write (identical content): %s", filepath)
            return IdempotentWriteResult(
                wrote=False,
                skipped=True,
                path=filepath,
                content_hash=content_hash,
            )

    # Write atomically: write to temp, then rename
    temp_path = path.with_suffix(f"{path.suffix}.tmp.{os.getpid()}")
    try:
        temp_path.write_text(content)
        temp_path.rename(path)  # Atomic on POSIX
        logger.info("Wrote (changed): %s (hash: %s)", filepath, content_hash)
        return IdempotentWriteResult(
            wrote=True,
            skipped=False,
            path=filepath,
            content_hash=content_hash,
        )
    except Exception as e:
        temp_path.unlink(missing_ok=True)
        raise RuntimeError(f"Failed to write {filepath}: {e}") from e


def idempotent_command(command: str, state_file: str) -> dict:
    """
    Execute a command idempotently using a state file to track completion.

    If the command has already been executed (state file exists with matching
    command hash), skip execution and return the cached result.
    """
    state_path = Path(state_file)
    command_hash = hashlib.sha256(command.encode()).hexdigest()[:12]

    # Check if already executed
    if state_path.exists():
        state = json.loads(state_path.read_text())
        if state.get("command_hash") == command_hash and state.get("status") == "success":
            logger.info("Skipping command (already executed): %s", command[:80])
            return {"skipped": True, "cached_result": state.get("result")}

    # Execute command
    import subprocess
    result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=300)

    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {result.stderr}")

    # Save state
    state_path.write_text(json.dumps({
        "command_hash": command_hash,
        "command": command[:200],  # Truncate for storage
        "status": "success",
        "result": result.stdout[:1000],
    }))

    return {"skipped": False, "output": result.stdout}
```

### 3. Loop State Management

Persist loop state so it survives crashes, restarts, and session handoffs.

```python
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
import json
import logging

logger = logging.getLogger(__name__)


class LoopPhase(Enum):
    PLANNING = "planning"
    EXECUTING = "executing"
    VALIDATING = "validating"
    HUMAN_REVIEW = "human_review"
    COMPLETE = "complete"
    FAILED = "failed"
    STOPPED = "stopped"


@dataclass
class LoopState:
    """Persistent state of a continuous agent loop."""
    loop_id: str
    task: str
    phase: LoopPhase = LoopPhase.PLANNING
    iteration: int = 0
    max_iterations: int = 20
    score: float = 0.0
    best_score: float = 0.0
    best_result: str = ""
    errors: list[str] = field(default_factory=list)
    step_log: list[dict] = field(default_factory=list)
    started_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    last_updated: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    human_approved: bool = False
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        data = asdict(self)
        data["phase"] = self.phase.value
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "LoopState":
        data["phase"] = LoopPhase(data["phase"])
        return cls(**data)

    def save(self, state_dir: str = ".agent-state") -> None:
        """Persist state to disk."""
        path = Path(state_dir) / f"{self.loop_id}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        self.last_updated = datetime.utcnow().isoformat()
        path.write_text(json.dumps(self.to_dict(), indent=2))
        logger.debug("State saved: %s", path)

    @classmethod
    def load(cls, loop_id: str, state_dir: str = ".agent-state") -> "LoopState | None":
        """Load state from disk (resume after crash)."""
        path = Path(state_dir) / f"{loop_id}.json"
        if not path.exists():
            return None
        return cls.from_dict(json.loads(path.read_text()))


class LoopStateManager:
    """Manages loop state persistence and recovery."""

    def __init__(self, state_dir: str = ".agent-state"):
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)

    def save_checkpoint(self, state: LoopState) -> None:
        """Save a checkpoint (every N iterations or on phase change)."""
        state.save(str(self.state_dir))
        # Also save a numbered checkpoint for history
        checkpoint = self.state_dir / f"checkpoints" / f"{state.loop_id}-{state.iteration:04d}.json"
        checkpoint.parent.mkdir(parents=True, exist_ok=True)
        checkpoint.write_text(json.dumps(state.to_dict(), indent=2))

    def recover(self, loop_id: str) -> LoopState | None:
        """Recover the most recent state for a loop."""
        return LoopState.load(loop_id, str(self.state_dir))

    def list_active_loops(self) -> list[dict]:
        """List all active (not complete/failed/stopped) loops."""
        loops = []
        for path in self.state_dir.glob("*.json"):
            state = LoopState.load(path.stem, str(self.state_dir))
            if state and state.phase not in (
                LoopPhase.COMPLETE, LoopPhase.FAILED, LoopPhase.STOPPED,
            ):
                loops.append({
                    "loop_id": state.loop_id,
                    "task": state.task,
                    "iteration": state.iteration,
                    "score": state.score,
                    "phase": state.phase.value,
                    "started_at": state.started_at,
                })
        return sorted(loops, key=lambda x: x["started_at"], reverse=True)
```

### 4. Quality-Gated Iteration

Each loop iteration must pass quality gates before proceeding. Gates are composable and can require human approval.

**TypeScript — Quality Gate Pipeline:**

```typescript
interface QualityGate {
  name: string;
  run: (context: LoopContext) => Promise<GateResult>;
  required: boolean;  // If false, failure is a warning not a blocker
}

interface GateResult {
  passed: boolean;
  score: number;      // 0.0 - 1.0
  message: string;
  details?: string;
}

interface LoopContext {
  iteration: number;
  currentOutput: string;
  previousOutput?: string;
  testResults?: TestSummary;
  lintResults?: LintSummary;
}

interface TestSummary {
  passed: number;
  failed: number;
  skipped: number;
  coverage: number;
}

interface LintSummary {
  errors: number;
  warnings: number;
}

class QualityPipeline {
  private gates: QualityGate[] = [];

  addGate(gate: QualityGate): this {
    this.gates.push(gate);
    return this;
  }

  async evaluate(context: LoopContext): Promise<{
    passed: boolean;
    score: number;
    results: Record<string, GateResult>;
    blockers: string[];
  }> {
    const results: Record<string, GateResult> = {};
    const blockers: string[] = [];
    let totalScore = 0;
    let totalWeight = 0;

    for (const gate of this.gates) {
      const weight = gate.required ? 2 : 1;
      const result = await gate.run(context);
      results[gate.name] = result;
      totalScore += result.score * weight;
      totalWeight += weight;

      if (!result.passed && gate.required) {
        blockers.push(`${gate.name}: ${result.message}`);
      }
    }

    const overallScore = totalWeight > 0 ? totalScore / totalWeight : 0;
    const passed = blockers.length === 0 && overallScore >= 0.7;

    return { passed, score: overallScore, results, blockers };
  }
}

// Example gates
const testGate: QualityGate = {
  name: "tests",
  required: true,
  run: async (ctx) => {
    const { passed, failed, coverage } = ctx.testResults ?? { passed: 0, failed: 1, coverage: 0 };

    if (failed > 0) {
      return { passed: false, score: 0, message: `${failed} failing tests` };
    }
    if (coverage < 80) {
      return {
        passed: true,  // Warning but not blocker
        score: coverage / 100,
        message: `Coverage: ${coverage}% (target: 80%)`,
      };
    }
    return { passed: true, score: 1, message: `All ${passed} tests passing` };
  },
};

const lintGate: QualityGate = {
  name: "lint",
  required: true,
  run: async (ctx) => {
    const { errors, warnings } = ctx.lintResults ?? { errors: 1, warnings: 0 };

    if (errors > 0) {
      return { passed: false, score: 0, message: `${errors} lint errors` };
    }
    if (warnings > 10) {
      return { passed: true, score: 0.5, message: `${warnings} lint warnings` };
    }
    return { passed: true, score: 1, message: "Clean" };
  },
};

const humanApprovalGate: QualityGate = {
  name: "human-approval",
  required: true,
  run: async (ctx) => {
    // In production, this would send a notification and wait for approval
    const approved = await requestHumanApproval({
      iteration: ctx.iteration,
      output: ctx.currentOutput,
      qualityScore: ctx.testResults?.coverage ?? 0,
    });

    if (!approved) {
      return { passed: false, score: 0, message: "Rejected by human reviewer" };
    }
    return { passed: true, score: 1, message: "Approved" };
  },
};

async function requestHumanApproval(params: {
  iteration: number;
  output: string;
  qualityScore: number;
}): Promise<boolean> {
  // Integration with Slack, email, or web UI for human approval
  // For now, simulate with a timeout-based check
  console.log(`⏸️  Human approval requested for iteration ${params.iteration}`);
  console.log(`Quality score: ${params.qualityScore}`);
  console.log(`Output preview: ${params.output.slice(0, 200)}...`);

  // In production: send Slack message, wait for response via webhook
  // Return true if approved within timeout, false otherwise
  return true;  // Placeholder
}
```

### 5. Loop Health Monitoring

Monitor loop health to detect anomalies (oscillation, degradation, runaway) and trigger alerts.

```python
from dataclasses import dataclass, field
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class LoopHealthMonitor:
    """Monitors loop health and detects anomalies."""
    score_history: list[float] = field(default_factory=list)
    iteration_times: list[float] = field(default_factory=list)
    error_history: list[str] = field(default_factory=list)
    alerts: list[dict] = field(default_factory=list)

    def record_iteration(self, score: float, duration: float, errors: list[str] | None = None):
        self.score_history.append(score)
        self.iteration_times.append(duration)
        if errors:
            self.error_history.extend(errors)

        # Run health checks
        self._check_oscillation()
        self._check_degradation()
        self._check_slowdown()
        self._check_error_rate()

    def _check_oscillation(self):
        """Detect score bouncing up and down without progress."""
        if len(self.score_history) < 6:
            return
        recent = self.score_history[-6:]
        deltas = [recent[i+1] - recent[i] for i in range(len(recent)-1)]
        directions = [d > 0 for d in deltas]
        # Check for alternating pattern
        alternations = sum(1 for i in range(len(directions)-1) if directions[i] != directions[i+1])
        if alternations >= 4:
            self._alert("OSCILLATION", f"Score oscillating (avg: {sum(recent)/len(recent):.3f})")

    def _check_degradation(self):
        """Detect consistent score decline."""
        if len(self.score_history) < 4:
            return
        recent = self.score_history[-4:]
        if all(recent[i] > recent[i+1] for i in range(len(recent)-1)):
            decline = recent[0] - recent[-1]
            self._alert("DEGRADATION", f"Score declining: {recent[0]:.3f} → {recent[-1]:.3f} (Δ: -{decline:.3f})")

    def _check_slowdown(self):
        """Detect increasing iteration times."""
        if len(self.iteration_times) < 4:
            return
        recent = self.iteration_times[-4:]
        if all(recent[i] < recent[i+1] for i in range(len(recent)-1)):
            slowdown = recent[-1] / recent[0] if recent[0] > 0 else float("inf")
            self._alert("SLOWDOWN", f"Iteration time increasing: {recent[0]:.1f}s → {recent[-1]:.1f}s ({slowdown:.1f}x)")

    def _check_error_rate(self):
        """Detect high error rate in recent iterations."""
        if len(self.error_history) < 5:
            return
        recent_errors = len(self.error_history[-5:])
        total_iterations = max(len(self.score_history), 1)
        error_rate = recent_errors / total_iterations
        if error_rate > 0.5:
            self._alert("HIGH_ERROR_RATE", f"Error rate: {error_rate:.0%} in recent iterations")

    def _alert(self, alert_type: str, message: str):
        """Record an alert (deduplicated: only alert once per type per 3 iterations)."""
        # Don't spam: check if same alert was fired recently
        for existing in reversed(self.alerts[-3:]):
            if existing["type"] == alert_type:
                return  # Already alerted

        alert = {
            "type": alert_type,
            "message": message,
            "iteration": len(self.score_history),
            "timestamp": datetime.utcnow().isoformat(),
        }
        self.alerts.append(alert)
        logger.warning("⚠️ Loop health alert [%s]: %s", alert_type, message)

    @property
    def is_healthy(self) -> bool:
        """Loop is healthy if no active alerts."""
        if not self.alerts:
            return True
        # Check if most recent alert was more than 3 iterations ago
        last_alert = self.alerts[-1]
        iterations_since_alert = len(self.score_history) - last_alert["iteration"]
        return iterations_since_alert >= 3

    def summary(self) -> str:
        """One-line health summary."""
        if self.is_healthy:
            return f"✅ Healthy (iterations: {len(self.score_history)}, avg score: {self._avg_score():.3f})"
        active_alerts = [
            a for a in self.alerts[-3:]
            if len(self.score_history) - a["iteration"] < 3
        ]
        types = ", ".join(a["type"] for a in active_alerts)
        return f"⚠️ Issues: {types}"

    def _avg_score(self) -> float:
        return sum(self.score_history) / len(self.score_history) if self.score_history else 0.0
```

### 6. Termination Criteria

Multiple termination conditions ensure the loop exits cleanly:

```python
class TerminationChecker:
    """Evaluates whether a loop should terminate."""

    def __init__(
        self,
        max_iterations: int = 20,
        max_duration_minutes: float = 30.0,
        quality_threshold: float = 0.85,
        convergence_window: int = 3,
        convergence_threshold: float = 0.01,
        max_consecutive_errors: int = 3,
    ):
        self.max_iterations = max_iterations
        self.max_duration_minutes = max_duration_minutes
        self.quality_threshold = quality_threshold
        self.convergence_window = convergence_window
        self.convergence_threshold = convergence_threshold
        self.max_consecutive_errors = max_consecutive_errors

    def should_terminate(self, state: LoopState) -> tuple[bool, str]:
        """
        Check all termination conditions.
        Returns (should_terminate, reason).
        """
        # 1. Max iterations
        if state.iteration >= self.max_iterations:
            return True, f"Max iterations reached ({self.max_iterations})"

        # 2. Timeout
        started = datetime.fromisoformat(state.started_at)
        elapsed = (datetime.utcnow() - started).total_seconds() / 60
        if elapsed >= self.max_duration_minutes:
            return True, f"Timeout ({elapsed:.1f}m >= {self.max_duration_minutes}m)"

        # 3. Quality threshold met
        if state.score >= self.quality_threshold:
            return True, f"Quality threshold met ({state.score:.3f} >= {self.quality_threshold})"

        # 4. Convergence (score stopped improving)
        if self._is_converged(state):
            return True, f"Score converged (no meaningful improvement in {self.convergence_window} iterations)"

        # 5. Consecutive errors
        consecutive = self._count_consecutive_errors(state)
        if consecutive >= self.max_consecutive_errors:
            return True, f"{consecutive} consecutive errors"

        # 6. Human stop
        if state.phase == LoopPhase.STOPPED:
            return True, "Manually stopped"

        return False, ""

    def _is_converged(self, state: LoopState) -> bool:
        steps = [s.get("score") for s in state.step_log[-self.convergence_window:] if s.get("score") is not None]
        if len(steps) < self.convergence_window:
            return False
        deltas = [abs(steps[i] - steps[i-1]) for i in range(1, len(steps))]
        return all(d < self.convergence_threshold for d in deltas)

    def _count_consecutive_errors(self, state: LoopState) -> int:
        count = 0
        for step in reversed(state.step_log):
            if step.get("error"):
                count += 1
            else:
                break
        return count
```

### 7. Full Continuous Loop Implementation

```python
def continuous_agent_loop(
    loop_id: str,
    task: str,
    agent_fn,          # Callable: (task, context) -> result
    validate_fn,       # Callable: (result) -> {score, passed, feedback}
    improve_fn,        # Callable: (result, feedback) -> improved_result
    state_manager: LoopStateManager,
    termination: TerminationChecker,
    health_monitor: LoopHealthMonitor,
    quality_pipeline: "QualityPipeline",  # From TypeScript section (conceptually same)
    require_human_approval: bool = False,
) -> LoopState:
    """
    Run a continuous agent loop with all safety features:
    - Idempotent operations
    - Quality gates
    - Human approval (optional)
    - Health monitoring
    - State persistence and recovery
    - Multiple termination criteria
    """
    # Try to recover from previous run
    state = state_manager.recover(loop_id)
    if state:
        logger.info("Resuming loop %s from iteration %d", loop_id, state.iteration)
    else:
        state = LoopState(loop_id=loop_id, task=task)
        state_manager.save_checkpoint(state)

    start_time = datetime.utcnow()

    while True:
        state.iteration += 1
        state.phase = LoopPhase.EXECUTING
        iteration_start = datetime.utcnow()

        logger.info("=== Iteration %d/%d ===", state.iteration, termination.max_iterations)

        # Generate / Improve
        try:
            if state.iteration == 1:
                result = agent_fn(state.task, context={"iteration": state.iteration})
            else:
                result = improve_fn(state.best_result, feedback={
                    "score": state.score,
                    "errors": state.errors,
                })
        except Exception as e:
            state.errors.append(str(e))
            state.step_log.append({"iteration": state.iteration, "error": str(e)})
            state_manager.save_checkpoint(state)
            continue

        # Quality gates
        state.phase = LoopPhase.VALIDATING
        validation = validate_fn(result)
        state.score = validation["score"]

        # Record health metrics
        iteration_duration = (datetime.utcnow() - iteration_start).total_seconds()
        health_monitor.record_iteration(
            score=state.score,
            duration=iteration_duration,
            errors=validation.get("errors"),
        )

        # Check loop health
        if not health_monitor.is_healthy:
            logger.warning("Loop health degraded: %s", health_monitor.summary())

        state.step_log.append({
            "iteration": state.iteration,
            "score": state.score,
            "duration": iteration_duration,
            "health": health_monitor.summary(),
        })

        # Human approval gate
        if require_human_approval and state.score >= 0.7:
            state.phase = LoopPhase.HUMAN_REVIEW
            state_manager.save_checkpoint(state)
            # In production: send notification, wait for webhook
            approved = True  # Placeholder
            if not approved:
                state.phase = LoopPhase.STOPPED
                state_manager.save_checkpoint(state)
                logger.info("Loop stopped: human rejected")
                break

        # Track best result
        if state.score > state.best_score:
            state.best_score = state.score
            state.best_result = result

        state_manager.save_checkpoint(state)

        # Termination check
        should_stop, reason = termination.should_terminate(state)
        if should_stop:
            state.phase = LoopPhase.COMPLETE if state.score >= termination.quality_threshold else LoopPhase.FAILED
            state_manager.save_checkpoint(state)
            logger.info("Loop terminated: %s (score: %.3f)", reason, state.score)
            break

        # Health alert: stop if critically unhealthy
        if len(health_monitor.alerts) >= 5:
            state.phase = LoopPhase.STOPPED
            state_manager.save_checkpoint(state)
            logger.critical("Loop stopped: too many health alerts (%d)", len(health_monitor.alerts))
            break

    total_duration = (datetime.utcnow() - start_time).total_seconds()
    logger.info(
        "Loop %s complete: %s in %d iterations, best score: %.3f, duration: %.1fs",
        loop_id, state.phase.value, state.iteration, state.best_score, total_duration,
    )

    return state
```

## Anti-Patterns

| Anti-Pattern | Symptom | Fix |
|---|---|---|
| Non-idempotent operations | Retries produce duplicate/wrong results | Check-before-write, state files |
| No state persistence | Crash = restart from zero | Save checkpoint every iteration |
| No human gate | Agent commits bad code | Quality gate + human approval for production |
| Single termination condition | Runaway or premature exit | Multi-condition checker (iterations, timeout, quality, convergence, errors) |
| No health monitoring | Undetected oscillation/degradation | Track scores, times, errors; alert on anomalies |
| No error budget | Loop continues despite constant failures | Max consecutive errors → stop |
| Blind retries | Retrying permanent failures | Distinguish retryable vs permanent errors |

## Success Checklist

- [ ] All agent operations are idempotent (check-before-write, state files)
- [ ] Loop state persisted after every iteration
- [ ] State recovery on restart (crash resilience)
- [ ] Quality pipeline with multiple gates (tests, lint, score)
- [ ] Human approval gate configured (for production-affecting loops)
- [ ] Health monitor active (oscillation, degradation, slowdown, error rate detection)
- [ ] Termination checker with multiple conditions (iterations, timeout, quality, convergence, errors)
- [ ] Checkpoints saved to `.agent-state/` directory
- [ ] Active loop listing available (`state_manager.list_active_loops()`)
- [ ] Health alerts logged and deduplicated
