---
name: post-merge-test-kit
description: Create or run a post-merge validation kit for a PR after it lands. Use when the user asks how to test a merged PR, validate a release, smoke-test production, verify deploy behavior, or choose agent-run versus human-run post-merge checks.
---

# Post-Merge Test Kit

Use this skill after a PR has merged, or just before merge when the team needs the post-merge validation kit drafted in advance. The goal is to make release validation mechanical: exact checks, exact expected results, exact evidence, explicit evidence statuses, and clear stop or rollback triggers.

This skill does not replace `enterprise-verify`, `enterprise-harness`, `deploy-checklist`, or PR review. Those prove readiness before merge. This skill proves the merged and deployed behavior in the target environment.

## Lifecycle

Run the skill in one of two lifecycle phases and state the phase in the output.

- `draft-before-merge`: create the validation kit before merge so nobody invents release checks under pressure.
- `execute-after-deploy`: run or hand off the kit after the target environment is deployed.

Best practice is both phases: draft before merge, execute after deploy. If the user asks after merge and no draft exists, create the kit and execute only the checks that are safe for the declared environment and mutation boundary.

## Release State Model

Classify the release state before writing the plan or evidence verdict.

- `merged-not-deployed`: PR has merged, but target environment does not prove the merge SHA is deployed.
- `deploying`: deploy is in progress or not yet healthy.
- `deployed-sha-confirmed`: target environment proves the deployed SHA matches the merge SHA or an explicit expected deploy SHA.
- `deployed-sha-mismatch`: target environment proves a different SHA is running.
- `rollback-detected`: target environment was rolled back after the merge.
- `unknown`: release state cannot be proven from available systems.

For `execute-after-deploy`, return `BLOCKED` unless the state is `deployed-sha-confirmed`, or unless the kit is explicitly scoped to diagnosing `deploying`, `deployed-sha-mismatch`, `rollback-detected`, or `unknown`.

## Modes

Choose exactly one mode and state it in the output.

- `agent-run`: the agent runs the safe checks directly and captures evidence.
- `human-run`: the agent writes a checklist a human can execute without guessing.

If the user does not choose a mode, default to `agent-run` when the agent has safe tool access and the validation is read-only. Default to `human-run` when checks require privileged access, manual judgment, physical operations, payment actions, live purchasing actions, or production mutation.

## Required Inputs

Fail closed if any required input is missing and cannot be discovered safely.

- PR number or merge identifier
- Merge SHA or deployed commit SHA
- Deployed SHA or explicit proof that deployed SHA cannot be read
- Target environment, such as `dev`, `staging`, `production`, or a named Render service
- Expected behavior after merge
- Validation owner, either `agent` or named human/team
- Mutation boundary: `read-only`, `approval-required`, or `mutating-approved`

For PR-driven work, discover missing context from GitHub, local git, CI/deploy status, PR body, review threads, changed files, and enterprise artifacts before asking the user.

## Source-Grounded Packet Build

Build the kit from real release context, not a generic smoke-test list.

Read or inspect:

1. PR title, body, comments, review threads, labels, and merge status.
2. Merge SHA, deployed SHA, target branch, and target environment.
3. Changed files and changed runtime surfaces.
4. CI and deploy status for the merged commit.
5. Enterprise plan, contract, review, forge, verify, harness, and deploy artifacts when present.
6. Feature flags, env vars, migrations, background jobs, integrations, and rollback notes when relevant.

Never treat CI, pre-merge tests, or previous enterprise verification as post-merge proof by themselves. They can seed the kit, but post-merge signoff requires target-environment evidence.

Classify every changed surface:

- backend/API
- database, query, migration, or data repair
- frontend/browser UI
- PDF, file upload, preview, download, or rendered output
- background worker, cron, queue, webhook, or sync
- integration such as REX, Shopify, payment, email, or Render
- auth, tenant, permission, ownership, or security boundary
- config, environment, feature flag, or deployment wiring
- documentation or non-runtime artifact

## Hard Gates

Return `BLOCKED` instead of a kit when these are true:

- The request only says vague validation such as "test the app" and no PR/env/expected behavior can be discovered.
- PR number or merge SHA is unknown.
- Target environment is unknown.
- Expected behavior is unknown.
- Mutation boundary is unknown.
- `execute-after-deploy` is requested and deployed SHA is unknown, mismatched, or rolled back without an explicit diagnostic scope.
- The kit cannot distinguish read-only checks from mutating checks.
- Production mutation is required but approval is missing.
- CI or pre-merge verification is the only proof offered for deployed behavior.
- A UI, PDF, file, modal, navigation, or rendered-output change has no browser proof step.
- A schema, query, migration, data repair, tenant, money, order, invoice, inventory, or ownership change has no DB/readback proof step.
- A worker, sync, webhook, or scheduled job change has no log, job, queue, or readback proof step.
- A config, env var, deploy, or feature flag change has no runtime config/deploy status proof step.
- There is no `known not tested` section.
- There are no stop, rollback, or escalation triggers with a named owner.
- Evidence would print secrets, tokens, cookies, auth headers, DSNs, API keys, customer PII, payment details, or private supplier/customer data.

## Evidence Statuses

Every planned and executed check must use exactly one status.

- `PENDING`: planned but not run yet.
- `PASS`: executed in the target environment and matched the expected result.
- `FAIL`: executed and did not match the expected result.
- `BLOCKED`: could not execute because a required precondition, permission, tool, environment, fixture, or approval is missing.
- `NOT_TESTED_WITH_REASON`: intentionally not tested, with a concrete reason and owner for the risk.

Do not use ambiguous statuses such as `OK`, `done`, `looks good`, `n/a`, `skipped`, or `probably`.

## Secret-Safe Evidence

Evidence must prove behavior without leaking sensitive values.

- Redact secrets as `[REDACTED:<type>]`.
- Prove env vars by presence, hash, length, config version, deploy event, or service metadata, not by printing values.
- Do not paste tokens, cookies, auth headers, DSNs, API keys, payment details, customer PII, supplier private data, or full production records into artifacts.
- For DB/readback proof, select only fields needed to prove the behavior and mask sensitive columns.
- If safe evidence cannot be captured, mark the check `BLOCKED` or `NOT_TESTED_WITH_REASON`; do not leak data to make proof look complete.

## Agent-Run Rules

For `agent-run`:

1. Run only checks inside the declared mutation boundary.
2. Prefer read-only API calls, browser checks, DB readbacks, logs, deploy status, and command receipts.
3. Use headless browser proof for UI, PDF, upload, preview, download, modal, navigation, and rendered-output behavior.
4. Use live or migrated-integration DB proof for schema, query, tenant, order, invoice, inventory, money, ownership, or data-sensitive behavior.
5. Stop before production writes, purchasing actions, payment actions, email sends, irreversible syncs, or customer-visible mutation unless `mutating-approved` is explicit.
6. Record the command, URL, environment, timestamp, release state, merge SHA, deployed SHA, status, expected result, actual result, owner, and artifact path for every evidence item.
7. Return `FAIL` when a required check cannot run. Do not silently downgrade required proof to manual confidence.

## Human-Run Rules

For `human-run`:

1. Write steps that a human can execute without reading the code or asking follow-up questions.
2. Include exact URLs, commands, accounts/roles to use, fixtures/orders/items to inspect, and expected visible results.
3. Mark any step that mutates production as `APPROVAL REQUIRED`.
4. Include screenshots, log snippets, DB readbacks, or copied response fields the human should capture.
5. Include what to do if a step fails and who owns the decision.
6. Include evidence status choices so the human reports `PASS`, `FAIL`, `BLOCKED`, or `NOT_TESTED_WITH_REASON`.
7. Keep the checklist short enough to run, but complete enough to prove the changed surfaces.

## Output Template

Use this exact structure.

```markdown
# POST-MERGE TEST KIT: PR #[number] - [short title]

**Mode**: agent-run | human-run
**Lifecycle Phase**: draft-before-merge | execute-after-deploy
**Verdict**: READY | BLOCKED | PASS | FAIL
**PR**: #[number] [url if available]
**Merge SHA**: [sha]
**Deployed SHA**: [sha or UNKNOWN]
**Release State**: merged-not-deployed | deploying | deployed-sha-confirmed | deployed-sha-mismatch | rollback-detected | unknown
**Environment**: [target]
**Owner**: [agent or human/team]
**Mutation Boundary**: read-only | approval-required | mutating-approved

## Release Intent
[What merged and what must now be true.]

## Changed Surface Map
| Surface | Changed paths or PR evidence | Required proof |
|---------|------------------------------|----------------|

## Deploy / SHA Gate
| Check | Expected | Actual | Status | Owner |
|-------|----------|--------|--------|-------|

## Stop / Rollback Triggers
- [Exact trigger] -> [owner] -> [action]

## Agent-Run Plan
| Step | Command / Action | Expected Result | Status | Evidence |
|------|------------------|-----------------|--------|----------|

## Human-Run Checklist
| Step | Action | Expected Result | Status Choices | Capture |
|------|--------|-----------------|----------------|---------|

## Evidence Ledger
| Check | Status | Timestamp | Merge SHA | Deployed SHA | Owner | Artifact / Output |
|-------|--------|-----------|-----------|--------------|-------|-------------------|

## Known Not Tested
- [Surface] -> [NOT_TESTED_WITH_REASON] -> [owner] -> [risk/next action]

## Signoff
[PASS/FAIL/BLOCKED with one sentence. Do not say "looks good" without evidence.]
```

If the chosen mode is `agent-run`, keep the human checklist brief or mark it `not selected`. If the chosen mode is `human-run`, keep the agent-run plan brief or mark it `not selected`.

## Artifact Rules

When working in a repository, write the kit to:

```text
docs/test-kits/YYYY-MM-DD-pr-####-post-merge.md
```

When an enterprise state directory exists, also write or update:

```text
.codex/enterprise-state/<slug>-post-merge-test-kit.json
```

The JSON artifact must use this schema shape:

```json
{
  "skill": "post-merge-test-kit",
  "pr": { "number": 0, "url": "", "title": "" },
  "mode": "agent-run",
  "lifecycle_phase": "draft-before-merge",
  "verdict": "READY",
  "merge_sha": "",
  "deployed_sha": "",
  "release_state": "unknown",
  "environment": "",
  "owner": "",
  "mutation_boundary": "read-only",
  "changed_surfaces": [
    {
      "surface": "backend/API",
      "paths_or_evidence": [],
      "required_proof": []
    }
  ],
  "deploy_sha_gate": [
    {
      "check": "",
      "expected": "",
      "actual": "",
      "status": "PENDING",
      "owner": ""
    }
  ],
  "evidence_records": [
    {
      "check": "",
      "status": "PENDING",
      "timestamp": "",
      "merge_sha": "",
      "deployed_sha": "",
      "environment": "",
      "command_or_action": "",
      "expected": "",
      "actual_redacted": "",
      "artifact": "",
      "owner": ""
    }
  ],
  "known_not_tested": [
    {
      "surface": "",
      "reason": "",
      "owner": "",
      "risk": "",
      "next_action": ""
    }
  ],
  "stop_rollback_triggers": [
    {
      "trigger": "",
      "owner": "",
      "action": ""
    }
  ]
}
```

Allowed verdicts are `READY`, `BLOCKED`, `PASS`, and `FAIL`. Allowed evidence statuses are `PENDING`, `PASS`, `FAIL`, `BLOCKED`, and `NOT_TESTED_WITH_REASON`. Reject artifacts with any other verdict or evidence status.

## Quality Bar

A good kit can be handed to either an agent or a human and run without improvisation. It proves the actual merged behavior, names what it did not prove, and makes rollback decisions obvious.

Do not accept:

- generic smoke tests
- stale pre-merge verification as post-merge proof
- CI-only proof for deployed behavior
- deployed SHA mismatch hidden as a successful validation
- secret-bearing evidence
- migration-only proof for runtime query behavior
- mock-only proof for data behavior
- manual GUI confidence where browser proof is required
- "monitor logs" without exact log source, query, time window, and failure pattern
- "ask Ben to test" without exact human-run steps
- rollback or escalation triggers without a named owner
