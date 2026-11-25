---
name: agent-evaluation
description: Use when constructing representative agent evaluation benchmark suites, defining scoring rubrics, implementing deterministic and LLM-as-a-judge graders, classifying failure taxonomies, and establishing reproducible agent release gates.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build]
version: 2.0.0
---

# Agent Evaluation

Establish empirical benchmark suites, calibrated multi-dimensional scoring rubrics, automated evaluation harnesses, and standardized failure taxonomies to validate agent reliability before production deployment.

## When to Use

- Benchmarking agent performance across prompt adjustments or model version migrations
- Quantifying regression risk during skill, tool definition, or system prompt updates
- Establishing automated CI release gates for agent pipelines and multi-agent teams
- Diagnosing recurring behavioral defects such as hallucinations, tool breaches, or reasoning loops
- Scoring complex agent outputs using hybrid deterministic and model-graded rubrics

## Core Rules

- **Representative Evaluation Dataset Design**:
  - Evaluation suites must comprise at least 30 diverse test cases stratified across three tiers:
    1. *Nominal Happy Paths ($40\%$)*: Standard domain requests exercising core capabilities.
    2. *Adversarial & Edge Cases ($40\%$)*: Malformed inputs, ambiguous requests, and boundary conditions.
    3. *Hostile & Safety Probes ($20\%$)*: Prompt injection attempts, forbidden tool requests, and policy traps.
  - Every test case must maintain immutable inputs paired with explicit ground-truth criteria.
- **Hybrid Grader Hierarchy**:
  - *Tier 1 (Deterministic Graders)*: Exact token presence (`must_include`), forbidden token absence (`must_not_include`), regex patterns, and JSON Schema Draft 2020-12 validation. Deterministic failures fail fast.
  - *Tier 2 (Heuristic Graders)*: Token length boundaries, execution step counts, and latency percentiles ($p50$, $p95$).
  - *Tier 3 (Model-Based Evaluators)*: LLM-as-a-judge rubrics evaluating qualitative traits (faithfulness, conciseness, reasoning depth) using 1–5 Likert scales with explicit rubric anchors.
- **Composite Scoring and Release Gates**:
  - Compute weighted composite score across rubric dimensions:
    $$S_{\text{composite}} = \sum_{i=1}^n w_i \cdot s_i \quad \text{where} \quad \sum w_i = 1.0$$
  - *Release Thresholds*:
    - Pass: Overall pass rate $\ge 90\%$, zero safety violations, composite score $\ge 0.85$.
    - Conditional Approval: Pass rate between $80\%-89\%$ with non-critical edge case failures only.
    - Fail-Closed: Pass rate $< 80\%$, any safety/injection breach, or any structural contract invalidity.
- **Structured Failure Taxonomy**:
  - Every failure must be categorized into standard defect classes: `hallucination`, `goal_hijack`, `schema_violation`, `trajectory_loop`, `tool_breach`, or `timeout`.
- **2026 Benchmark Calibration & pass^k Reliability**:
  - Calibrate internal suites against the current agentic landscape: τ²-bench (dual-control world state; τ-i18n/voice in Bench 2.0), Terminal-Bench 2.0 (hard and unsaturated), BrowseComp (near-saturated ~92%), SWE-bench Verified (saturated — ~1.7-point spread across top-5; prefer harder enterprise variants for discrimination).
  - Report **pass^k** (k-run reliability) alongside single-pass scores — headline single-run scores are gameable and unreproducible; a release gate on pass^1 alone is not evidence of reliability.

## Suggested Process

1. **Curate Benchmark Test Suites**:
   - Assemble representative evaluation fixtures pairing raw prompt inputs with expected criteria.
   - Version-control evaluation datasets in jsonl or paired json test files.
2. **Configure Deterministic and Model-Based Rubrics**:
   - Define exact contract schema assertions and structural invariants.
   - Write explicit rubric prompts for qualitative judges, specifying criteria for each point on the scale.
3. **Execute Evaluation Harness**:
   - Run the agent through all test fixtures in an isolated sandbox environment.
   - Capture comprehensive execution telemetry: turn count, tool calls, token usage, and latency.
4. **Grade and Classify Outputs**:
   - Run deterministic schema and regex assertions first.
   - Run model-based judges with temperature $0.0$ for reproducible qualitative scoring.
   - Aggregate failure metrics across the standardized failure taxonomy.
5. **Emit Evaluation Report and Enforce Gate**:
   - Compile benchmark results into the standardized contract schema.
   - Trigger automated build failure if the evaluation run violates release thresholds.

## Output Contracts

When completing an evaluation benchmark, emit `contracts/schemas/agent-eval-report.json`:
- `eval_run_id`: Unique identifier for the evaluation execution.
- `summary`: Total cases, pass rate, latency percentiles, and overall pass/fail status.
- `rubrics`: Weighted rubric scores and threshold compliance flags.
- `failure_taxonomy`: Quantified failure distribution across defect classes.
- `verdict`: Automated release recommendation (`pass`, `conditional_approval`, `fail_closed`).

## Failure Modes

- **Evaluation Dataset Contamination**: Training or tuning system prompts directly on the test set. Mitigation: maintain strict separation between few-shot prompt examples and held-out evaluation splits.
- **LLM Judge Self-Preference Bias**: Using the same LLM family to judge its own outputs, inflating scores. Mitigation: use cross-family judges or calibrate model judges against human golden annotations.
- **Flaky Heuristic Assertions**: Writing overly fragile string matching assertions that fail on valid synonymous phrasing. Mitigation: use semantic assertions and regex flexibility for prose while reserving strict matching for schemas and IDs.
- **Silent Degradation on Edge Cases**: Masking critical edge case failures beneath high overall aggregate pass rates. Mitigation: enforce zero-tolerance floor gates on safety and structural schema rubrics regardless of aggregate score.

## Checklist

- [ ] Evaluation dataset covers nominal ($40\%$), edge case ($40\%$), and hostile safety ($20\%$) suites
- [ ] Every test case includes immutable inputs and verifiable expected behaviors
- [ ] Deterministic schema validations executed before qualitative model judges
- [ ] LLM judges configured with temperature 0.0 and anchored 1–5 scoring definitions
- [ ] Weighted composite score calculated with explicit threshold boundaries
- [ ] All test failures classified into standardized failure taxonomy categories
- [ ] Output artifacts strictly validate against `agent-eval-report.json`
- [ ] Automated gate blocks release upon safety violations or pass rate below 90%
- [ ] pass^k reliability reported alongside single-pass scores; suite calibrated against the 2026 landscape (τ²-bench, Terminal-Bench 2.0)

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: the 20% hostile safety probes contain real injection payloads that can hijack the harness or the executing agent under test. Mitigation: run all fixtures in the isolated sandbox; grade safety probes with deterministic `must_not_include` assertions so injected content never reaches an executing tool or a free-text judge.
- **ASI04 Supply Chain**: benchmark suites imported from external registries carry poisoned fixtures or golden labels. Mitigation: version-control all fixtures in-repo with immutable inputs; verify provenance and schema before importing any external suite.
- **ASI06 Context & Memory Poisoning**: LLM-as-judge rubric prompts read adversarial test outputs that can instruct the judge to award top scores. Mitigation: wrap judge inputs as untrusted reference material, anchor every Likert point explicitly, and run judges at temperature 0.0.
- **ASI07 Inter-Agent Communication**: `agent-eval-report.json` is consumed by Technical Lead, Prompt Engineer, and automated release gates. Mitigation: emit only schema-validated reports so downstream agents and CI gates never parse partial or schema-drifted results.
- **ASI08 Cascading Failures**: a flaky gate or partial run silently unblocks (or blocks) a downstream release. Mitigation: fail-closed on any structural contract invalidity; declare evaluation failure explicitly instead of propagating partial results.
- **ASI09 Human-Agent Trust Exploitation**: self-preference-biased scores, or a `conditional_approval` dressed as a pass, are presented as objective evidence to ship. Mitigation: disclose judge identity and calibration; fail-closed on any safety/injection breach regardless of the composite score.

## Related Skills

- **write-tests**: Authoring unit and integration tests for software components.
- **agent-quality-gate**: Enforcing quality and validation thresholds in agentic pipelines.
- **context-optimization**: Optimizing prompt contexts to maximize evaluation benchmark scores.
- **prompt-injection-defense**: Verifying agent resilience against adversarial prompt injection attacks.
- **combinatorial-testing**: Generating combinatorial input matrices for exhaustive test coverage.
