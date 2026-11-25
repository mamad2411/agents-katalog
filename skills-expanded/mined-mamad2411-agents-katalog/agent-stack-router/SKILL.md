---
name: agent-stack-router
description: >-
  Route work between global standard agents in the tools repository and project-specialized agents such as tui-translator agents. Use this skill whenever the user mentions agents, agent chuẩn, specialized agents, project agents, tui-translator, cross-review, tentacle review, performance/security bug prevention, verification gates, or asks which agent/skill/hook should handle a task. Prefer this skill before dispatching agents so the workflow uses the most specific available agent and produces evidence instead of review-only approval.
---

# Agent Stack Router

Use this skill to choose the right agent stack for a task when there are global
standard agents in `~/.copilot/tools` and project-specific agents in a target
repository such as `tui-translator`.

The goal is to avoid a common failure mode: sending every task to generic
reviewers. Generic reviewers help with breadth, but performance and security
bugs usually need project-specific context plus tool evidence.

## Agent source hierarchy

Resolve agents in this order:

1. **Project-specialized agents** in the target repo, usually
   `<project>/.github/agents/*.agent.md`.
2. **Project instructions** in `<project>/AGENTS.md`, `.github/copilot-instructions.md`,
   or equivalent if no specialized `.agent.md` files exist.
3. **Global standard agents** in `~/.copilot/tools/.github/agents/*.agent.md`.
4. **Reference templates** in `~/.copilot/tools/skills/agent-creator/references/*.agent.md`.
5. Built-in/default agents only when no custom or standard agent fits.

If the project-specialized agent is missing, say so explicitly and route to the
best global standard agent. Do not pretend the specialist exists.

## Standard tools agents

Use these global agents as durable building blocks:

| Agent | Use when |
|---|---|
| `whole-app-impact-auditor` | Planning or auditing a change that may affect docs, hooks, skills, agents, CI, install/update, or operator workflows. |
| `verification-gate` | Before closeout, merge, issue closure, or after code changes; it runs existing tests/build/lint/typecheck and reports evidence. |
| `research-planner` | Ambiguous architecture/product research, issue specs, handoff prompts, or when requirements are unclear. |
| `browser-security-reviewer` | Browser-to-localhost, CORS, PNA, token, tunnel, hosted shell, pairing, or local backend exposure risks. |
| `python-browse-backend` | Python backend routes, auth, CORS/PNA, pairing, health/discovery endpoints, CLI flags, and Python tests. |
| `browse-ui-host-state` | HostProvider, host profiles, localStorage host state, UI host selection, and browse-ui tests. |
| `hosted-shell-bootstrap` | Hosted UI local backend detection, loopback bootstrap, PNA CORS, pairing/manual token flows. |

For generic templates, prefer:

| Template | Use when |
|---|---|
| `security-reviewer.agent.md` | Threat model, secrets, auth, injection, token, CORS, OWASP/ASVS review. |
| `qa-specialist.agent.md` | Test strategy, regression coverage, edge cases, and validation plans. |
| `staff-engineer.agent.md` | Architecture tradeoffs, design risk, and broad technical direction. |
| `debug.agent.md` | Reproduction-first debugging with logs, stack traces, and hypotheses. |

## Expected tui-translator specialists

For `tui-translator`, look for or create project agents with these roles:

| Specialist | Trigger | Evidence expected |
|---|---|---|
| `tui-rust-code-reviewer` | Rust/Tokio/WASAPI/ratatui/pipeline/provider changes | File:line findings, resource lifetime/backpressure review, `cargo test`/`cargo clippy` evidence. |
| `tui-security-auditor` | `google_api_key`, config, logs, sessions, audio archives, path handling, network calls | STRIDE notes, secret scan/SAST/SCA output, HIGH/CRITICAL risk register. |
| `tui-soak-monitor` | 30-minute crash, memory growth, render latency, audio drops, long-running stability | RSS time series, p95 latency/error counts, crash-free duration, soak command output. |
| `crash-root-cause` | `.dmp`, panic, OOM, access violation, `audio_stability_proof` crash | WinDbg/CDB `!analyze -v`, exception code, stack frames, faulting module, symbol limitations. |
| `nfr-verification-gate` | Closeout for performance/security-sensitive changes | Evidence ledger that covers correctness, perf, memory, security, dependencies, and soak when applicable. |

If these files are absent, route to the matching global standard/template agent
and include a **missing specialist** note in the plan.

## Routing workflow

### 1. Inventory before dispatch

Read the target repo's agent surfaces first:

- `<project>/.github/agents/*.agent.md`
- `<project>/AGENTS.md`
- `<project>/.github/copilot-instructions.md`
- Global fallback: `~/.copilot/tools/.github/agents/*.agent.md`

Summarize what exists and what is missing. This prevents silent fallback to
generic agents.

### 2. Classify the task

Assign one or more dimensions:

| Dimension | Signals | Preferred route |
|---|---|---|
| Correctness | feature, bug fix, refactor, test failure | project code reviewer + verification-gate |
| Performance | crash after time, memory, latency, O(n), backpressure, soak | `tui-soak-monitor` + perf/memory specialist + verification-gate |
| Security | API key, token, log, CORS, path, command, dependency, auth | `tui-security-auditor` or security-reviewer template on opus-tier model |
| Architecture | WBS, tentacle plan, decomposition, project-wide impact | whole-app-impact-auditor + research-planner |
| Crash/incident | dump, panic, OOM, access violation, stack trace | crash-root-cause + debug agent |
| Dependency/supply chain | Cargo.toml, Cargo.lock, package manifest | dependency audit agent or security reviewer |

### 3. Dispatch with evidence requirements

Every specialist prompt should require:

- exact files/lines or command outputs;
- pass/fail verdict, not "looks good";
- explicit limitations and unknowns;
- next command to close any evidence gap.

For security work, use a security-tier model. For code generation/review, use
sonnet-tier or stronger. Use exploration/haiku only for file discovery, never
as the final security or code-review authority.

If any inventory, classification, risk, dependency, or specialist choice is below confidence
`1.0`, stop routing. Add a leading `research-planner`/validation step on the strongest
available model (`claude-opus-4.7` when available; otherwise newest opus-class model), split
the ambiguity into atomic questions, and block implementation/review/merge routing until the
synthesized confidence is `1.0` or an explicit user override is recorded.

### 4. Require independent verification

Do not accept cross-review as proof. Require tool evidence:

| Claim | Evidence |
|---|---|
| Tests pass | Test runner output with pass/fail summary. |
| Security safe | SAST/SCA/secret scan output plus threat-model notes for the changed surface. |
| Performance stable | Benchmark/soak output with baseline and threshold. |
| Memory leak fixed | RSS trend, heap profile, or bounded data-structure test. |
| Crash explained | Dump analysis or explicit statement that debugger/symbols are missing. |

### 5. Close the loop

Before final closeout, ask the verification agent to check:

- all claimed gates have fresh evidence;
- missing project specialists were either created or documented as a gap;
- broad changes have whole-app impact coverage;
- any new repeated lesson was recorded in session knowledge.

## Output format

When this skill triggers, return an agent routing plan:

```markdown
## Agent inventory
| Scope | Found | Missing |

## Task classification
| Dimension | Why it applies | Risk |

## Dispatch plan
| Step | Agent | Scope | Model tier | Evidence required |

## Verification gates
| Gate | Command/artifact | Blocking? |
| Decision confidence | confidence `1.0` or research evidence + explicit override | Yes |

## Missing specialists / follow-up
```

## Examples

### Example: tui-translator 30-minute crash

Route to:

1. `crash-root-cause` if dumps exist; require WinDbg/CDB evidence.
2. `tui-soak-monitor` for RSS/p95/error-count soak evidence.
3. `tui-rust-code-reviewer` for `SubtitlePane`, pipeline, WASAPI, provider retry.
4. `verification-gate` for `cargo test`, `cargo clippy`, and soak artifacts.

Do not close based only on code review.

### Example: API key/log/session change

Route to:

1. `tui-security-auditor` if present, otherwise the global security reviewer template.
2. `dependency-audit-agent` if manifests changed.
3. `verification-gate` to confirm `gitleaks`, `semgrep`, `cargo audit`, and tests ran.

Block closeout if API keys can appear in source, logs, session exports, or URLs
without an explicit risk decision.

### Example: new cross-agent workflow

Route to:

1. `research-planner` for unclear requirements.
2. `whole-app-impact-auditor` for docs/hooks/skills/agents synchronization.
3. `verification-gate` for final evidence.

If the workflow affects `tui-translator`, prefer project specialists for the
project-local review and global agents for the shared tools ecosystem review.
