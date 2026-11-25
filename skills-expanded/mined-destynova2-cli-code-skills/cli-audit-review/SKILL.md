---
name: cli-audit-review
metadata:
  author: ThomasD343
  version: "3.0.0"
description: "Scored MR/PR/diff review skill calibrated for strict infrastructure and automation changes. Use for merge-request reviews, pull-request reviews, scored reviewer gates, convention compliance, Ansible roles/collections, Molecule, GitLab CI, semantic-release, packaging, Go/Cobra CLIs, PowerShell, shell/Python helpers, Kubernetes/containers, Terraform/OpenTofu, and operator documentation reviewed through a contract -> validation -> execution -> proof -> docs/release methodology. Produces RMI scoring, gate decisions, and reviewer-style actionable comments. For generic code quality, code smells, clean-code compliance, or tech debt audits, use cli-audit-code instead."
argument-hint: "[file-or-directory-or-diff]"
context: fork
agent: general-purpose
---

> **Optimization:** This skill uses on-demand loading. Read only the reference files relevant to the target, except `references/scoring.md`, which is mandatory for every scored review.

> **Language rule:** By default, write user-facing reviews in French when the prompt or repository context is French. Keep code identifiers, file paths, module names, commit types, and product names unchanged. Use English only when the user asks for it or when the project is clearly English-only.

> **Privacy rule:** Never mention the training corpus, reviewer identity, personal names, e-mails, private/internal URLs, organization names, project names, commit hashes, issue/MR IDs, or raw examples from the corpus. The skill must behave as a neutral review methodology.

# Audit Review — Review Methodology Index (RMI)

Use this skill when the user asks for a MR/PR/diff review, scored reviewer gate, strict infrastructure or automation review, Ansible review, CI/release review, idempotence audit, Molecule proof review, or convention compliance review.

Do not use it for generic code quality, code smell, clean-code compliance, or tech debt audits. Use `cli-audit-code` for that. For a shell-only quality audit, use `cli-audit-shell`. For pipeline design or optimization rather than review gate feedback, use `cli-forge-pipeline`.

The goal is not to produce generic lint feedback. The goal is to review like a strict production reviewer: contract first, validation before execution, idempotence, proof, documentation, release safety, then style.

## Core Principles

1. **Intent first** — understand the MR/PR description, linked issue, changed behavior, and review scope before reading line-level diffs.
2. **Evidence first** — every actionable finding needs `file:line`, or `repo-wide`/`diff-wide` when no single line owns the issue.
3. **Contract chain** — public behavior must propagate through: `contract -> validation -> implementation -> proof -> docs/CI/release`.
4. **Desired state over actions** — for infrastructure and Ansible, prefer modeling the final state rather than introducing imperative action flags.
5. **Fail fast** — bad configuration must be rejected before packages, services, filesystems, clusters, remote APIs, or credentials are touched.
6. **Idempotence is mandatory** — repeated execution must converge cleanly; commands/shell tasks need explicit state/change/failure controls.
7. **Secrets are toxic by default** — tokens, passwords, keys, credentials, and sensitive command output must be contained in logs, templates, CI variables, artifacts, and errors.
8. **Proof is part of the change** — deployable behavior needs Molecule, CI, integration tests, idempotence checks, or equivalent proof.
9. **CI/release is production code** — pipelines, semantic-release, packaging metadata, branch rules, tokens, and artifacts are reviewed as runtime behavior.
10. **Recent conventions win** — when conventions conflict, apply `references/conflict-resolution.md` and prefer the newest relevant pattern unless it is less safe.
11. **Risk beats cosmetic style** — do not spend review budget on whitespace while contract, proof, idempotence, or security is broken.
12. **Approve improvement, not perfection** — block regressions and unproven risk; mark polish as non-blocking when code health is improving.
13. **Smallest useful correction** — ask for the minimal change that closes the risk. Avoid rewrite requests unless the design is unsafe.
14. **Positive signal matters** — include what is good: clear propagation, good assertions, maintained docs, useful tests, safe release handling.

## Input

`$ARGUMENTS` may be:

- a MR/PR diff or patch,
- a file,
- a directory,
- empty, in which case review the current repository with priority on changed files, infrastructure entry points, and public contract files.

Primary fit: infrastructure automation repositories. Secondary fit: application code, CLIs, scripts, documentation, and release tooling when they affect deployable behavior.

When a diff contains PostgreSQL migrations, SQLx queries, repository transaction changes, or
durable business-state transitions, recommend `/cli-audit-data` for the database-specific
invariant and concurrency gate.

## Mandatory Reference Loading

| Target situation | Read |
|---|---|
| Any scored review | `references/scoring.md` |
| Any conflict between possible conventions | `references/conflict-resolution.md` |
| Any final report or MR comments | `references/comment-style.md`, `references/output-template.md` |
| Ansible, Molecule, roles, collections | `references/conventions-ansible.md`, `references/reviewer-methodology.md` |
| GitLab CI, semantic-release, packaging, Galaxy, commit hygiene | `references/conventions-ci-release.md` |
| Go, PowerShell, shell, Python, Kubernetes, containers, Terraform/OpenTofu | `references/conventions-language.md` |
| Any generated artifact or report | `references/privacy.md` |

## 12-Dimension Review Framework

Score every applicable dimension from **0.0 to 1.0**, then compute the weighted RMI.

| # | Category | Weight | Key question |
|---|---:|---:|---|
| R1 | Public Contract & Naming | 11% | Are public variables/config/API/flags named as desired states, scoped, defaulted or intentionally undefined, documented, and understandable? |
| R2 | Validation & Fail-Fast | 11% | Are type, bounds, emptiness, enum, platform, topology, and prerequisite checks done before risky work? |
| R3 | Idempotence & State Convergence | 12% | Does repeated execution converge without false changes, duplicate state, or uncontrolled shell/command side effects? |
| R4 | Change Propagation & Coherence | 9% | Do defaults/config, assertions, tasks/templates, handlers, tests, docs, CI, and release metadata move together? |
| R5 | Secrets & Security Boundaries | 11% | Are secrets protected from logs, templates, artifacts, command output, committed files, and unsafe CI variables? |
| R6 | Test, Molecule & CI Proof | 12% | Is the changed behavior proven by the right scenario, matrix, integration test, lint job, or idempotence run? |
| R7 | Platform, OS & Topology Variants | 8% | Are RedHat/Windows, Linux/Windows, single-node/HA, online/airgap, backend, runtime, and cluster variants separated and covered? |
| R8 | CI, Release & Packaging Safety | 7% | Are workflow rules, branch behavior, tokens, semantic-release, Galaxy/package metadata, artifacts, and release commits coherent? |
| R9 | Documentation & Operator Clarity | 6% | Can an operator understand defaults, prerequisites, limits, airgap behavior, upgrade impact, rollback, and failure modes? |
| R10 | Language & Ecosystem Idioms | 6% | Does the implementation follow the relevant idioms for Ansible, YAML, Go, PowerShell, shell, Python, Kubernetes, containers, or Terraform? |
| R11 | Reviewability & Commit Hygiene | 4% | Are PR/MR description, commits, scopes, diff size, WIP noise, file moves, and renames easy to review and release-safe? |
| R12 | Local Style & Formatting | 3% | Are EOF newlines, spacing, YAML quotes, task separators, lint formatting, and naming details aligned after higher risks are handled? |

Formula:

```text
RMI = Σ(wᵢ × sᵢ) / Σ(wᵢ) × 10
```

## Workflow

### Step 0 — Understand the change

Before reading individual files:

1. identify the intended change from the PR/MR description, issue links, commit messages, or diff summary;
2. collect the diff shape: changed files, generated/vendor/lock files, migration files, tests, docs, CI, release metadata;
3. decide the review order: main design path first, tests first when they clarify behavior, generated files last;
4. if the diff is too large or mixes unrelated behavior, review the main design early and ask for a split when that is the smallest way to make the review reliable.

### Step 1 — Discover review scope

For a broad review, inspect in this order:

1. public contract files: `defaults/`, schemas, CLI flags, env vars, public API, `README`, `meta`, `galaxy.yml`, package metadata;
2. validation files: `tasks/assert*.yml`, schemas, preflight scripts, input validators;
3. execution paths: `tasks/main.yml`, setup/configure tasks, handlers, templates, shell/Python/Go/PowerShell helpers;
4. proof: `molecule/`, tests, CI matrices, lint jobs, integration checks, idempotence checks;
5. release and packaging: `.gitlab-ci.yml`, `.releaserc*`, release scripts, `requirements.yml`, `galaxy.yml`, container files, charts, bundles;
6. docs/operator material: README, examples, troubleshooting, upgrade notes.

### Step 2 — Classify the change

Tag each changed area as one or more of:

- public contract / default / config / flag / env var / API,
- validation / assertion / schema,
- runtime behavior / task / template / handler / command,
- test / Molecule / CI proof,
- documentation / operator contract,
- CI / release / packaging,
- security / secrets / credentials,
- platform / topology / airgap / backend variant,
- refactor-only,
- style-only.

### Step 3 — Trace the contract chain

For every behavior change, verify:

```text
public contract -> validation/assertion -> consumer implementation -> proof -> documentation/CI/release
```

Create findings for missing links. A new public variable, CLI flag, environment variable, module option, or YAML key is incomplete until it has validation, consumer proof, and operator documentation when relevant.

### Step 4 — Apply operational gates before scoring

Before writing style comments, identify gate failures:

- secret/token/password/key can leak or is committed;
- destructive or long-running operation runs before validation;
- public contract changed without validation or consumer proof;
- command/shell task mutates durable state without idempotence controls;
- deployable behavior changed without Molecule/CI/integration proof;
- OS/topology/airgap/runtime variant can regress silently;
- CI/release variables, tokens, branch rules, artifacts, or semantic-release behavior are unsafe;
- docs/README/Molecule/CI paths are stale after renames or scenario splits.

Apply the caps in `references/scoring.md`. The lowest cap wins.

### Step 5 — Review with domain-specific rules

Use the relevant reference file:

- Ansible/Molecule/YAML: `references/conventions-ansible.md`
- CI/release/packaging/commits: `references/conventions-ci-release.md`
- Go/PowerShell/shell/Python/Kubernetes/containers/Terraform: `references/conventions-language.md`
- convention conflicts: `references/conflict-resolution.md`

### Step 6 — Score all applicable dimensions

Score with evidence, not intuition. If a dimension is truly not applicable, mark it `N/A` and redistribute weight only across applicable dimensions. If it applies but you did not inspect it, score it low and state the scope limitation.

### Step 7 — Write reviewer-style output

Use `references/comment-style.md` and `references/output-template.md`.

Every substantive finding should include:

- severity and R category,
- `file:line`,
- concrete risk,
- deployable consequence,
- smallest correction,
- proof expected,
- confidence,
- disproof condition when uncertainty exists.

For simple line-level convention comments, be concise: one sentence is enough when the fix is obvious and not blocking.

If the exact correction is short and syntax-sensitive, include a ready-to-paste suggestion. If only non-blocking suggestions remain, say so explicitly and do not turn polish into a merge blocker.

## Decision Rules

| Decision | Condition |
|---|---|
| `REQUEST_CHANGES` | Any blocker gate, any critical finding without proof, or final RMI `< 6.0`. |
| `COMMENT` | No blocker, but RMI `6.0-7.9`, missing proof/docs, uncertain variant behavior, or significant non-blocking methodology gap. |
| `APPROVE_WITH_NOTES` | RMI `8.0-8.9`, no gate failure, only minor follow-ups or style issues. |
| `APPROVE` | RMI `>= 9.0`, no gate failure, coherent proof/docs/release path. |

Never approve deployable behavior when the required proof is absent, even if the implementation looks correct.

## Output Format

Use `references/output-template.md` unless the user asks for another format.

Minimum output sections:

1. decision and RMI score,
2. gate status,
3. weighted scorecard,
4. findings ordered by risk,
5. good practices found,
6. smallest next actions,
7. approval conditions when not fully approved.

When run under `cli-cycle`, also emit `.claude/cli-audit-review.json` following `../shared/result-schema.md` so the cycle can aggregate score, findings, strengths, and handoffs without parsing prose.

## What This Skill Does NOT Do

- It does not identify or imitate any individual person.
- It does not expose training data, personal identities, private URLs, internal repositories, or raw corpus examples.
- It does not auto-fix code unless explicitly asked for a patch.
- It does not replace linters; it reviews production risk and methodology compliance.
- It does not approve on style alone; proof, idempotence, contract coherence, and release safety are required.

## Dynamic Handoffs

Recommend, do not auto-run:

| Condition detected | Recommend |
|---|---|
| Generic clean-code smells dominate | `/cli-audit-code` |
| Shell scripts have significant behavior | `/cli-audit-shell` |
| Test strategy is weak beyond one MR | `/cli-audit-test` |
| Documentation drift is broad | `/cli-audit-doc` or `/cli-audit-sync` |
| CI/CD design is central | `/cli-forge-pipeline` |
| Architecture/design is ambiguous | `/cli-forge-hld` or `/cli-forge-lld` |
| Ansible role structure is tangled | `/cli-audit-tangle` |
| Diff changes PostgreSQL/SQLx schema, transactions, migrations, or durable state | `/cli-audit-data` |
