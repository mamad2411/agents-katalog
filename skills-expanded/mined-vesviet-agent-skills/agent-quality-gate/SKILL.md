---
name: agent-quality-gate
description: Run and interpret repository quality gates for agent-delivered changes, including validators, lint, tests, build checks, diff sanity checks, and phase-exit evidence. Use when reporting completion, advancing a bug or feature to the next phase, or declaring a pack, role, workflow, or code change ready.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
version: "1.0.0"
---

# Agent Quality Gate

Use this skill when changes need evidence that they are complete, valid, and aligned with repo-local checks before a phase can close.

## When to Use

- reporting a change as complete to a user or phase
- advancing a bug/feature to the next phase
- declaring a pack, role, workflow, or code change ready
- producing phase-exit evidence (validators, lint, tests, build)
- validating AI evaluations, distributed trace spans, query budgets, or contract compatibility
- evaluating agent tool-calling trajectories and execution graphs before task completion
- running consumer-provider contract checks prior to staging or production releases

## Core Rules

- run the repo's own validators before declaring completion
- choose targeted checks first, then broader checks when risk justifies them
- do not hide skipped checks or failing validation; fix introduced issues when local
- never treat a clean diff or passing lint as proof of full behavioral safety
- do not allow a bug or feature to exit validation without explicit residual-risk handling
- trace-based span assertions: verify that every request produces the expected telemetry DAG
- query complexity bounds: reject any change that exhibits N+1 query patterns ($O(N)$ query loops)
- contract compatibility gate: require successful Pact Broker matrix check before release

### AI & Agentic Verification Gates

When evaluating autonomous agents, generative features, or RAG pipelines:
- **Calibrated LLM-as-a-Judge:** require >= 85% statistical agreement (Cohen's Kappa or Pearson correlation) against human gold labels on benchmark datasets (>= 100 samples) before trusting automated judge scores; decompose rubrics into atomic evaluation criteria with Chain-of-Thought reasoning.
- **RAG Triad Thresholds:** enforce Faithfulness >= 0.85 (grounded in context, zero hallucinations), Context Relevancy >= 0.85 (retrieval precision without distractor noise), and Answer Relevancy >= 0.85 (directly addresses user query).
- **Trajectory DAG Loop Detection:** validate tool-call sequences as a directed acyclic graph; detect and abort repeated identical tool calls, alternating ping-pong states, and state hash collisions.
- **Prompt Regression & Red Teaming:** evaluate prompt assets against golden test datasets to prevent intent drift, jailbreak vulnerabilities, and output format degradation.

### Trace-Based Span Verification & Query Budgets

- **OpenTelemetry Span Assertions:** validate distributed trace hierarchy (HTTP -> Service -> DB -> Event) with Kubeshop Tracetest DSL; assert required span attributes and enforce P95/P99 latency limits per span.
- **Query Complexity Budgets:** enforce $O(1)$ query complexity per request; execute automated DB query counting in integration tests to reject $O(N)$ query loops ($N+1$ query cascades).
- **Execution Plan Assertions:** verify that database operations utilize index scans and avoid unindexed sequential scans on critical tables.

### Consumer-Driven Contract Release Gate

- **Pact Broker can-i-deploy:** require successful matrix verification (`pact-broker can-i-deploy --pacticipant <service> --version <sha> --to-environment <env>`) before approving release promotion.
- **Provider State Verification:** ensure provider state handlers isolate mock data setup without persistent database pollution.
- **Schema Compatibility:** enforce Protobuf wire compatibility via `buf breaking --against` (`WIRE_JSON` rules) and OpenAPI 3.1 diff validation to prevent downstream breaking changes.

### Trust Tiers for AI-Generated Changes

- **T1 (low-risk):** documentation, comments, formatting, isolated tests — standard validator pass is sufficient.
- **T2 (medium-risk):** logic in existing modules, new helpers, config — require targeted behavioral tests covering changed paths in addition to validators.
- **T3 (high-risk):** code touching auth, payments, data retention, public APIs, deployment manifests, or security controls — require adversarial diff review.
- **Adversarial Diff Review:** for T3 changes, scan for: (a) invented package imports not in lockfiles, (b) hardcoded secrets or credentials, (c) overly permissive IAM or CORS rules, (d) test assertion weakening, and (e) OWASP ASI risks (Goal Hijack, Confused Deputy).
- **Human Sign-Off:** do not advance a T3 change without explicit human sign-off; record approver in the quality gate report.

## Suggested Process

### 1. Identify Required Gates
Inspect the repo for applicable checks:
- validation scripts and linters
- unit, integration, and contract tests
- AI evaluation benchmarks and trajectory DAG checks
- OpenTelemetry trace assertions and database query counts
- consumer and provider contracts via Pact Broker
- build commands, schema diffs, and formatters

### 2. Match Gates To Change Risk
- run narrow checks for documentation or isolated tests
- enforce T1–T3 trust tiers and adversarial diff reviews for AI-generated code
- verify reproduction evidence, preserved behavior, and impact radius for bug fixes

### 3. Run Checks Safely
- use repo-local commands without inventing unapproved workflows
- run calibrated evals, trace assertions, and contract tests in isolated environments
- explain trade-offs transparently if skipping any environment-dependent check

### 4. Interpret Failures
When a check fails:
- isolate whether the failure was introduced by the current change
- identify root cause (e.g. N+1 query loop, judge disagreement, broken contract, lint error)
- fix local failures and rerun checks; reopen prior phase if assumptions are invalidated
- rerun trace-based span assertions to verify N+1 query resolution
- re-verify Pact matrix after provider contract updates before phase exit

### 5. Report Evidence
Summarize:
- exact checks run and pass/fail status
- skipped checks and residual risk
- whether the current phase may close and required human sign-off

## Output Format

```markdown
## Quality Gate Result

Phase under review:
- ...

Checks run:
- ...

Results:
- ...

Skipped checks:
- ...

Residual risk:
- ...

Phase exit decision:
- Advance | Rework | Escalate

Risk acceptance owner if needed:
- ...
```

## Checklist

- [ ] required repo-local gates, lints, tests, and builds identified and run
- [ ] AI/LLM evals meet thresholds (calibrated judge >= 85%, RAG triad >= 0.85)
- [ ] agent execution trajectory checked for loops, cycles, and schema conformity
- [ ] OTel trace spans verified for latency limits and O(1) query complexity (zero N+1 queries)
- [ ] Pact Broker can-i-deploy verified for cross-service contract changes
- [ ] check scope matched to change risk (T1–T3 trust tiers and adversarial diff)
- [ ] provider state handlers verified for state isolation without DB pollution
- [ ] Protobuf wire compatibility checked via buf breaking --against
- [ ] failures investigated, skipped checks explained, and residual risk documented
- [ ] final status reported with residual risk and explicit phase exit decision
- [ ] human sign-off obtained for T3 high-risk changes before phase advancement

## Red Flags

| Rationalization Thought | Positive Corrective Action |
|---|---|
| "Targeted test passed, so full CI is fine." | Match gate scope to risk tier (`T1`–`T3`) and run the full repo validator and test suite before declaring done. |
| "It is only a docs or checklist tweak." | Run repo validators and regression tests; docs and checklists are contract-tested in CI. |
| "Lint is clean, so behavior is safe." | Verify runtime behavior, exit codes, and side effects directly before closing the phase. |
| "Skip the failing test; it looks unrelated." | Reproduce and isolate root cause first; record any unresolvable blocker explicitly instead of hiding skips. |

## Failure Modes

- **Gate bypassed under release pressure**: a release skips the gate to meet a deadline. **Mitigation:** release pipeline rejects unverified artifacts; surface bypass in postmortem.
- **Uncalibrated LLM judge drift**: automated evaluator drifts or suffers sycophancy bias. **Mitigation:** mandate >= 85% agreement against human gold labels.
- **Silent N+1 query cascade**: passing unit tests hide $O(N)$ database query explosions. **Mitigation:** enforce OTel trace span assertions and automated query budgets in CI.
- **Contract drift release failure**: microservice deploys breaking changes to consumers. **Mitigation:** enforce Pact Broker `can-i-deploy` matrix verification prior to promotion.
- **Agent trajectory infinite loop**: autonomous agent enters ping-pong or cycle state. **Mitigation:** terminate on consecutive state hash collisions or repeated tool calls.
- **Assertion theater without runtime inspection**: tests assert HTTP 200 while database operations fail. **Mitigation:** enforce trace-based assertions and query budgets.
- **Provider state leakage**: provider tests mutate database state across verification runs. **Mitigation:** mandate transactional rollbacks and isolated state handlers.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: verify agent outputs against authorized specifications; reject self-assigned scope expansion.
- **ASI02 Tool Misdirection**: validate tool parameters and schemas against canonical definitions; abort unconstrained tool calling.
- **ASI04 Supply Chain**: inspect diffs for hallucinated dependencies, typosquatting packages, or unvetted scripts.
- **ASI05 RCE Guard**: gate execution commands inside sandboxed environments; reject unsanitized shell invocations.
- **ASI07 Inter-Agent Communication**: validate A2A task contracts, trajectory DAGs, and Pact contract matrices.
- **ASI09 Trust Exploitation**: require explicit human sign-off on T3 high-risk changes; never trust AI evaluation blindly.

## Output Contracts

When evaluating phase-exit criteria, validator outputs, or test execution results, emit:

- **`contracts/schemas/validation-result.json`** — Emitted when completing a quality gate evaluation across linters, static analysis, type checks, build commands, and repository validators, documenting gate status and phase-exit readiness.
- **`contracts/schemas/test-report.json`** — Emitted when aggregating test suite execution results, coverage metrics, passed/failed test counts, and regression evidence for phase verification.
- **`contracts/schemas/implementation-result.json`** — Emitted when gating, consolidating, or validating multi-slice implementation outcomes against technical delivery plan criteria.

Skip emission for local scratch test runs during active development iterations.

## Related Skills

- **agent-tool-orchestration**: Run checks in the right order
- **agent-context-management**: Track validation evidence across long tasks
- **agent-prompt-lifecycle**: Include prompt evaluation as a quality gate when prompt assets change
- **agent-handoff**: Communicate validation results clearly
- **write-tests**: Add coverage when risk is not protected
- **commit-code**: Validate changes before approved commit creation

