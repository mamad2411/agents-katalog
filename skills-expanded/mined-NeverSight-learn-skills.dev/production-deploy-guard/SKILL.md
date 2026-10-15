---
name: production-deploy-guard
description: Plan approval-gated production deployments for a single Linux server using Docker Compose and Nginx. Use when defining a deployment contract, choosing between private-Git source builds and CI-built image pulls, generating a read-only server audit, sanitizing and analyzing audit or execution logs, producing bootstrap/Nginx/deploy/verify/rollback bundles, validating shell safety and artifact integrity, or diagnosing deployment failures. Never use it to SSH into a server or automatically execute production writes.
---

# Production Deploy Guard

Build a reviewable deployment bundle from explicit user intent and observed server facts. Keep every operation local until the user manually transfers and runs an approved script on the target server.

## Non-negotiable boundaries

- Never open SSH sessions, invoke remote shells, or run commands on a production server.
- Never execute generated production-write scripts on the user's behalf.
- Never read an unsanitized audit or execution log into agent context. Invoke the local sanitizer with the raw file path, then read only its sanitized output and report.
- Never request, store, echo, or place secret values in a contract, prompt, log, Git repository, image, generated bundle, or command argument.
- Store only environment-variable names and secret references. Reject fields such as `value`, `password`, `token`, `private_key`, and `connection_string` when they could contain credentials.
- Never infer unknown ports, paths, credentials, migration safety, shared-resource ownership, downtime tolerance, or rollback viability.
- Never approve a contract, plan, bundle, shared-resource change, execution, or business result for the user.
- Treat any artifact change as invalidating downstream validation and approval.
- Never generate or accept `git reset --hard`, destructive Git clean, unbounded recursive deletion, `docker system prune`, volume deletion, `chmod -R 777`, unscoped recursive ownership changes, remote-script pipes, or unconfirmed database migrations.

Read [security-policy.md](references/security-policy.md) before generating any production-write bundle or diagnosing a suggested fix that changes production.

## Supported MVP boundary

Proceed only when the target can be represented by all of these dimensions:

- one Linux server;
- `apt` or `dnf` operating-system family;
- `systemd`;
- Docker Engine and Docker Compose v2, either already installed or explicitly planned for installation;
- host Nginx, containerized shared Nginx, external ingress, or no ingress;
- `source_build` from a GitHub repository with a read-only Deploy Key, or `image_pull` from an immutable image tag/digest;
- `amd64` or `arm64`.

Stop with `UNSUPPORTED_TARGET_PROFILE` for Kubernetes, Swarm, multi-host/high-availability orchestration, Windows servers, unsupported init systems, direct cloud mutations, or any profile without a tested template. Read [platform-profiles.md](references/platform-profiles.md) when classifying an environment.

## Local runner

Use the bundled dependency-free Node runner for deterministic work:

```bash
node <skill-root>/scripts/deployguard.mjs help
```

Require Node.js 20 or newer. The runner performs local file operations only. It has no telemetry and does not upload contracts or logs. Read [cli-reference.md](references/cli-reference.md) before invoking a command for the first time in a session.

Initialize an explicit local session directory, normally inside the user's project:

```bash
node <skill-root>/scripts/deployguard.mjs session init \
  --session-dir <absolute-project-path>/.deployguard
```

Do not initialize a session until the user agrees to local file creation. The session directory contains its own deny-all `.gitignore`; still verify it is not tracked by Git.

## Entry routing

Choose the entry point from the user's available artifacts:

| User has | Start or resume at | Required action |
| --- | --- | --- |
| only a deployment goal | `DRAFT_CONTRACT` | clarify and validate a contract |
| a draft contract | `DRAFT_CONTRACT` | validate, summarize unknowns, request confirmation |
| a confirmed contract | `CONTRACT_CONFIRMED` | generate the read-only audit script |
| a raw server audit log | `AUDIT_SCRIPT_GENERATED` | sanitize without reading it |
| a sanitized audit log | `AUDIT_LOG_SANITIZED` | analyze environment facts |
| an environment report | `ENVIRONMENT_ANALYZED` | draft and validate a deployment plan |
| a confirmed plan | `PLAN_CONFIRMED` | generate and validate a bundle |
| a raw execution/verification log | `USER_APPROVED` or later | sanitize, record execution, diagnose or verify |

If the claimed state is inconsistent with artifact hashes in `session.json`, stop and report the mismatch. Do not skip ahead based only on conversational memory.

## State and approval workflow

Follow this order exactly. Read [workflow.md](references/workflow.md) and [approval-gates.md](references/approval-gates.md) for transition details.

### 1. `DRAFT_CONTRACT`

1. Read [contract-and-state.md](references/contract-and-state.md).
2. Ask only for missing deployment decisions that materially affect safety or architecture.
3. Write a JSON contract that conforms to `assets/schemas/deployment-contract.schema.json`.
4. Use variable names and secret references only. Never place an example secret value in the contract.
5. Run `contract validate`.
6. Present a concise summary, unknowns, assumptions explicitly marked as unconfirmed, and the selected deployment-mode preference.
7. Obtain Gate G1 confirmation from the user before running `contract confirm`.

Do not confirm a contract with unresolved high-risk unknowns: absolute production paths, ingress ownership, persistent-data scope, public exposure, delivery mode, secret locations, downtime, or rollback target.

### 2. `CONTRACT_CONFIRMED` to `AUDIT_SCRIPT_GENERATED`

1. Run `audit generate` from the confirmed contract.
2. Run the runner's read-only policy checks and calculate the script hash.
3. Tell the user exactly what metadata the script collects and whether its optional DNS/HTTP probes access the network.
4. Obtain Gate G2 approval for that exact script hash.
5. Instruct the user to transfer and execute the script manually, redirecting stdout to a log file.

Never suggest piping a downloaded script directly to a shell.

### 3. `AUDIT_SCRIPT_GENERATED` to `AUDIT_LOG_SANITIZED`

Given a raw audit log path, do not open, preview, grep, count, summarize, or otherwise read its contents. Run:

```bash
node <skill-root>/scripts/deployguard.mjs audit sanitize \
  --input <absolute-raw-log-path> \
  --output <absolute-sanitized-log-path> \
  --report <absolute-sanitization-report-path> \
  --privacy standard \
  --session-dir <absolute-session-dir>
```

Read the sanitization report first. If it reports residual high-confidence secret material or an incomplete private-key block, stop with `SANITIZATION_INCOMPLETE`. Only then read the sanitized log.

### 4. `AUDIT_LOG_SANITIZED` to `ENVIRONMENT_ANALYZED`

1. Run `audit analyze` on the sanitized log.
2. Compare the report with the confirmed contract.
3. List observed facts, conflicts, missing facts, unsupported dimensions, shared resources, and changes requiring approval.
4. Do not convert missing facts into defaults.
5. Stop if the server profile is unsupported or the evidence is insufficient for a safe plan.

### 5. `ENVIRONMENT_ANALYZED` to `PLAN_CONFIRMED`

1. Read [deployment-modes.md](references/deployment-modes.md).
2. Draft a plan conforming to `assets/schemas/deployment-plan.schema.json`.
3. Select exactly one delivery mode. Explain the selection and preserve the user's explicit choice unless it is unsafe or unsupported.
4. Separate one-time bootstrap, one-time ingress, routine deploy, read-only verification, rollback, database/manual steps, and shared-resource changes.
5. Run `plan validate`.
6. Present precise paths, ports, packages, identities, networks, ingress files, persistent-data boundaries, downtime, verification, rollback limits, and required approvals.
7. Obtain Gate G3 confirmation before `plan confirm`.

Any mode or plan revision invalidates an existing bundle and approval.

### 6. `PLAN_CONFIRMED` to `BUNDLE_VALIDATED`

1. Run `bundle generate` using the confirmed contract, environment report, and plan.
2. Generate only files required by the plan. Keep one-time scripts separate from routine deployment.
3. Run `bundle validate` and require `status: passed` with zero hard failures.
4. Inspect `REVIEW.md`, `MANIFEST.json`, and the validation report.
5. Summarize every production write and each shared-resource or persistent-data implication.

Never weaken a hard-fail rule to make a bundle pass. Fix the generator input, plan, template, or script instead.

### 7. `BUNDLE_VALIDATED` to `USER_APPROVED`

Pause. The user must run `approval record` themselves in an interactive terminal and type the displayed approval phrase containing the current manifest hash. Do not invoke it, type into it, or simulate user input.

Shared Nginx, shared Docker network, system-package, permission-scope, database, and persistent-data changes require their own explicit acknowledgements in addition to the bundle approval.

### 8. `USER_APPROVED` to `USER_EXECUTED`

Tell the user to transfer only the approved bundle and verify its manifest hash on the server before manual execution. Do not execute it remotely. When the user returns an execution log:

1. sanitize it without reading the raw file;
2. record the exact manifest hash the user states they executed;
3. reject mismatches against the approved manifest;
4. transition only after the sanitized execution evidence is recorded.

### 9. `USER_EXECUTED` to `DEPLOYMENT_VERIFIED`

Require technical verification from `50-verify.sh` and a user-confirmed business smoke result. Container health or HTTP 200 alone is not business acceptance. Record the deployed commit/image, public result, smoke result, log path, and rollback target.

Do not mark verification successful when the application starts but the business smoke test fails.

## Failure diagnosis

For raw failure logs, follow the same no-read-before-sanitize rule. Run `diagnose analyze` only on sanitized logs. Read [failure-diagnosis.md](references/failure-diagnosis.md) to classify evidence such as:

- Git `FETCH_HEAD` ownership or permissions;
- dirty Git worktree or non-fast-forward updates;
- missing environment-variable names;
- persistent-directory permissions;
- registry authentication, missing digest, or architecture mismatch;
- port 80/443/application-port conflicts;
- Nginx reload transition with transient old-worker 404s;
- container health failure;
- successful infrastructure deployment with failed business smoke tests.

Return evidence, likely causes with confidence, safe read-only follow-up checks, and separately gated remediation. Never turn a diagnosis request into an unapproved production fix.

## Resource routing

| Need | Read or run |
| --- | --- |
| state transitions and artifact invalidation | [workflow.md](references/workflow.md) |
| contract fields and secret references | [contract-and-state.md](references/contract-and-state.md) |
| hard safety rules | [security-policy.md](references/security-policy.md) |
| `source_build` versus `image_pull` | [deployment-modes.md](references/deployment-modes.md) |
| OS, ingress, architecture support | [platform-profiles.md](references/platform-profiles.md) |
| human approval gates | [approval-gates.md](references/approval-gates.md) |
| command syntax and outputs | [cli-reference.md](references/cli-reference.md) |
| failure classification | [failure-diagnosis.md](references/failure-diagnosis.md) |
| deterministic local work | `scripts/deployguard.mjs` |
| schemas and render inputs | `assets/schemas/` |
| reviewed output templates | `assets/templates/` |

## Response discipline

At every turn, state the current session state, evidence used, blockers, the next safe action, and whether that action is local-only, read-only server work, or production-writing server work. Use the runner's structured error code when a command fails. Mark unknown information as unknown; do not hide it in prose.
