---
name: agent-evaluation-framework
version: 1.0.0
min_mindforge_version: 10.0.4
status: stable
triggers: agent evaluation, task completion rate, agent benchmark, reasoning quality, tool selection accuracy, agent cost efficiency, end-to-end agent test, agent regression, agent quality score, agent performance metric, evaluation harness design, agent grading
compose: eval-harness
---

# Skill — Agent Evaluation Framework (End-to-End Agent Performance Measurement)

## When this skill activates
When measuring agent performance, designing agent benchmarks, tracking quality
regressions, or comparing agent configurations. Use for any scenario where you
need to answer: "Is this agent good enough?" or "Did this change make the agent
better or worse?"

Core principle: **Multi-dimensional quality** — agent quality is not a single number.
A fast agent that's wrong is worse than a slow agent that's right. A cheap agent
that hallucinates is worse than an expensive agent that's accurate. Measure ALL
dimensions that matter.

## Mandatory actions when this skill is active

### Metric Taxonomy

1. **Core agent metrics (measure ALL of these):**
   ```
   Correctness metrics:
   - Task completion rate: % of tasks completed successfully (end-to-end)
   - First-attempt success rate: % completed without retry or correction
   - Factual accuracy: % of claims that are verifiable and correct
   - Instruction adherence: % of explicit instructions followed correctly

   Efficiency metrics:
   - Cost per task: total API spend / successful completions
   - Tokens per task: input + output tokens consumed
   - Time per task: wall-clock time from task start to completion
   - Tool calls per task: number of tool invocations (fewer = more efficient)

   Quality metrics:
   - Reasoning quality score: rubric-based assessment of reasoning chain
   - Tool selection accuracy: % of tool calls that were appropriate
   - Output quality score: rubric-based assessment of final output
   - Hallucination rate: % of outputs containing ungrounded claims

   Safety metrics:
   - Harmful output rate: % of outputs flagged by safety classifiers
   - Permission violation rate: % of actions exceeding authorized scope
   - Information leakage rate: % of outputs exposing sensitive data
   ```

2. **Composite quality score:**
   ```
   Agent Quality Score = weighted combination:
   - Correctness (40%): task_completion * 0.25 + first_attempt * 0.15
   - Quality (30%): reasoning_quality * 0.15 + output_quality * 0.15
   - Efficiency (20%): normalized(1/cost) * 0.10 + normalized(1/time) * 0.10
   - Safety (10%): (1 - harmful_rate) * 0.05 + (1 - violation_rate) * 0.05

   Weights are defaults — adjust per use case (safety-critical → increase safety weight)
   ```

### Benchmark Design

3. **Evaluation dataset structure:**
   ```
   .mindforge/evals/agent-benchmark/
   ├── config.json           # benchmark metadata and thresholds
   ├── tasks/
   │   ├── easy/             # baseline tasks (should be ~100% success)
   │   │   ├── task-001.json
   │   │   └── task-002.json
   │   ├── medium/           # standard tasks (target: 80%+ success)
   │   │   ├── task-010.json
   │   │   └── task-011.json
   │   └── hard/             # stretch tasks (target: 50%+ success)
   │       ├── task-020.json
   │       └── task-021.json
   ├── rubrics/
   │   ├── correctness.md    # how to grade correctness
   │   ├── reasoning.md      # how to grade reasoning quality
   │   └── output.md         # how to grade output quality
   └── results/
       └── results.jsonl     # append-only results log
   ```

4. **Task definition format:**
   ```json
   {
     "task_id": "task-001",
     "difficulty": "easy",
     "category": "code-generation",
     "description": "Write a function that reverses a string",
     "input": "Create a TypeScript function reverseString(s: string): string",
     "expected_behavior": [
       "Returns reversed string",
       "Handles empty string",
       "Handles unicode correctly"
     ],
     "verification": {
       "type": "code",
       "test_cases": [
         {"input": "hello", "expected": "olleh"},
         {"input": "", "expected": ""},
         {"input": "abc", "expected": "cba"}
       ]
     },
     "metadata": {
       "tools_available": ["Read", "Write", "Bash"],
       "time_limit_seconds": 120,
       "cost_limit_usd": 0.50
     }
   }
   ```

   Rules:
   - Minimum 30 tasks per benchmark (10 easy, 15 medium, 5 hard)
   - Tasks must be representative of real usage patterns
   - Include both deterministic tasks (one right answer) and generative tasks (rubric-graded)
   - Each task has explicit success criteria (not vague "good output")
   - Stratify by difficulty to detect capability thresholds

### Running Benchmarks

5. **Execution protocol:**
   ```
   For each task in benchmark:
   1. Initialize fresh agent context (no contamination between tasks)
   2. Provide task input + available tools
   3. Record: start_time, all tool calls, all outputs, end_time
   4. Grade output against verification criteria
   5. Log full result to results.jsonl

   Run N times per task (N >= 3) to measure variance:
   - Report mean and standard deviation per metric
   - Flag high-variance tasks (inconsistent agent behavior)
   - Use same random seed where possible for reproducibility
   ```

6. **Result logging:**
   ```json
   {
     "run_id": "uuid",
     "timestamp": "ISO-8601",
     "task_id": "task-001",
     "agent_config": {"model": "claude-sonnet", "temperature": 0.0},
     "metrics": {
       "completed": true,
       "first_attempt": true,
       "time_seconds": 15.3,
       "cost_usd": 0.012,
       "tokens_used": {"input": 1200, "output": 450},
       "tool_calls": 3,
       "reasoning_quality": 4,
       "output_quality": 5
     },
     "grading": {
       "method": "code",
       "pass": true,
       "evidence": "All 3 test cases passed"
     }
   }
   ```

### Regression Detection

7. **Regression detection algorithm:**
   ```
   Compare current run vs baseline:

   RED (regression detected — blocks deployment):
   - Task completion rate drops > 5%
   - Any previously-passing easy task now fails
   - Cost per task increases > 50%
   - Safety metric degrades at all

   YELLOW (warning — investigate before deploying):
   - Task completion rate drops 2-5%
   - Medium/hard task pass rate drops > 10%
   - Time per task increases > 30%
   - New failure modes appear

   GREEN (no regression):
   - All metrics within 2% of baseline
   - No new failure modes
   - Cost/time stable or improved
   ```

   Rules:
   - ALWAYS compare to a pinned baseline (not just previous run)
   - Run regression suite before any agent config change ships
   - Regression in EASY tasks is more alarming than regression in HARD tasks
   - Store baseline with agent version (update baseline when intentionally accepting changes)

### Cost Efficiency Analysis

8. **Quality-per-dollar assessment:**
   ```
   Cost Efficiency Ratio = quality_score / cost_per_task

   Comparison framework:
   - Agent A: quality=0.92, cost=$0.05/task → efficiency=18.4
   - Agent B: quality=0.88, cost=$0.01/task → efficiency=88.0

   Decision: Agent B is 4.8x more cost-efficient.
   Choose A only if the 4% quality gap causes real user-visible failures.
   ```

   Rules:
   - A cheaper model that achieves 95% of the quality at 20% of the cost is usually better
   - Factor in retry cost (low first-attempt rate = hidden cost multiplier)
   - Include tool call costs in total cost (API calls, compute)
   - Report cost efficiency alongside raw quality (both matter)

## Self-check before task completion

Before marking a task done when this skill was active:

- [ ] Did I define metrics across all four dimensions (correctness, quality, efficiency, safety)?
- [ ] Is the benchmark stratified by difficulty (easy/medium/hard)?
- [ ] Did I run multiple times (N >= 3) to measure variance?
- [ ] Is there a pinned baseline for regression detection?
- [ ] Are regression thresholds defined (RED/YELLOW/GREEN)?
- [ ] Did I report cost efficiency (quality/cost ratio), not just raw quality?
- [ ] Are easy-task failures treated as more alarming than hard-task failures?
- [ ] Are results appended to results.jsonl (never overwritten)?
