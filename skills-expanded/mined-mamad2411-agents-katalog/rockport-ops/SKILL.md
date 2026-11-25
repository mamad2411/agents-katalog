---
name: rockport-ops
description: "Diagnose, fix, and advise on Rockport infrastructure issues. ALWAYS USE THIS SKILL when the user asks anything about Rockport infrastructure — including casual questions like 'is it ok', 'is it up', 'is it working', 'check the infra', 'how's rockport', 'did the deploy work', or 'is everything healthy'. Also use when: debugging errors (timeouts, 403s, 502s, model not found), checking health or status, receiving error output from another Claude instance using Rockport, investigating spend or cost issues, troubleshooting video/image generation failures, or when the user mentions rockport is down, broken, slow, or erroring. Also use when the user pastes HTTP error responses from an OpenAI-compatible API that routes through Rockport."
user-invocable: true
argument-hint: "[symptom or error description]"
allowed-tools: "Read, Grep, Glob, Bash, Agent"
effort: high
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

Diagnose infrastructure issues, fix them through the speckit pipeline (preserving full history), and produce structured advice for any calling Claude instance that depends on Rockport.

Input can be:
- Free-form symptom descriptions ("chat completions are timing out")
- Raw error output pasted from another Claude Code instance
- Health check requests ("is rockport healthy?")
- Specific error messages or HTTP status codes

## Workflow

Execute these 5 phases in order. Every phase is mandatory.

### Phase 1: Triage

Investigate the issue using **subagents** to keep diagnostic noise out of the main context. The main context stays clean for reasoning and speckit.

**Delegate diagnostic work to subagents.** Each subagent should:
- Run the specific AWS CLI / SSM / curl commands needed
- Return a **summary** (5-10 lines max), not raw output
- Include specific error messages, timestamps, and status codes

Use the diagnostic procedures in [diagnostics.md](references/diagnostics.md) for the exact commands. Work top-down through the layers, but skip layers that clearly aren't relevant to the symptom.

**Layer order:**
1. Instance state (running? SSM reachable?)
2. Service health (systemd status for litellm, cloudflared, rockport-video, postgresql)
3. Health endpoints (localhost:4000/health, localhost:4001/v1/videos/health)
4. Recent logs (journalctl errors from the relevant service, last 10 minutes)
5. External reachability (curl through tunnel with CF-Access headers)
6. Bedrock / IAM (only if symptoms suggest model invocation failures)
7. Idle shutdown state (was the instance recently stopped by Lambda?)
8. Security posture (WAF active, Access application active, API key health)

**Security posture check** (Layer 8 — include in triage when symptoms suggest security issues):
- Check WAF ruleset is deployed (verify waf.tf exists and was applied)
- Check Access application is active (verify access.tf was applied)
- List API keys via `rockport.sh key list` and flag any over-budget or expired
- If a recent pentest report exists under `pentest/reports/rockport/`, note its timestamp and high-level findings

**Security incident triage path** — trigger when symptoms include "unauthorized access", "unexpected spend", "403s", "suspected breach":
- Check CloudTrail for unusual API calls (last 24h)
- Check spend logs for anomalous keys (`rockport.sh spend today`)
- Cross-reference latest pentest report if available
- Check if any API keys were created outside normal workflow

**Cost discipline:** Use logs and status checks first. Only make a test API call if you cannot determine the issue from logs. If a test call is needed, use the cheapest option: `claude-haiku-4-5-20251001` with `max_tokens: 1`.

**AWS profile:** Run `./scripts/rockport.sh auth --role readonly` first, then use `AWS_PROFILE=rockport-readonly` for diagnostic commands (the long-lived `rockport` profile only holds `sts:AssumeRole`). See [aws-access.md](references/aws-access.md) for role capabilities and escalation.

### Phase 2: Diagnosis

Based on subagent findings, determine:

1. **What is broken** — specific service, endpoint, or component
2. **Root cause** — why it broke (OOM, config error, IAM drift, Bedrock outage, etc.)
3. **Layer** — which architectural layer is affected
4. **Severity** — operational (restart fixes it) vs. code/config bug vs. infrastructure issue

Consult [common-issues.md](references/common-issues.md) for known symptom-to-cause mappings.

**Immediate operational actions** (restart a stopped instance, restart a crashed service) can be taken now to restore service. These do NOT skip the speckit requirement — if the root cause is a bug, it still gets a spec. But don't leave the service down while writing a spec.

Report your diagnosis to the user before proceeding to Phase 3.

### Phase 3: Fix via Speckit

**All fixes go through speckit.** This is non-negotiable. Even small config changes get a spec so there is a complete history in `specs/`.

**OPS prefix convention:**
- Ops specs use `OPS-` in the short name to distinguish from feature specs
- The create-new-feature script auto-assigns the next number, so the directory becomes `specs/NNN-OPS-short-name/` (e.g., `specs/013-OPS-litellm-oom-fix/`)
- Pass `--short-name "OPS-short-description"` to the script. Example: `--short-name "OPS-litellm-oom-fix"`
- When invoking `/speckit.specify`, prefix the description with `OPS:` so it's clear this is an operational fix

**Speckit pipeline — run all phases:**
1. `/speckit.specify` — Describe the symptom, root cause, and proposed fix as the feature description
2. `/speckit.plan` — Technical plan for the fix
3. `/speckit.tasks` — Task breakdown
4. `/speckit.analyze` — Cross-artifact consistency check
5. `/speckit.implement` — Execute the fix

**IaC is truth.** If the fix involves infrastructure changes:
- The terraform files MUST be updated
- Changes MUST be applied via `./scripts/rockport.sh deploy` or `config push`
- Never make AWS changes that aren't reflected in the codebase
- If you fixed something operationally in Phase 2 (e.g., restarted a service), the speckit fix must address the root cause so it doesn't recur

**Constitution compliance.** All fixes must comply with the Rockport constitution at `.specify/memory/constitution.md`. The speckit pipeline enforces this, but pay special attention to:
- Cost Minimization (Principle I) — fixes must not increase monthly costs
- Scope Containment (Principle IV) — don't add features disguised as fixes
- Explicit Bash Error Handling (Principle VI) — no `set -euo pipefail`
- LiteLLM-First (Principle III) — prefer configuration over custom code

### Phase 4: Verify

After the fix is implemented and deployed:

1. **Run the full smoke test suite** using a subagent:
   ```
   Use a subagent to run: cd $PROJECT_ROOT && bash tests/smoke-test.sh
   Report: total tests, passed, failed, and details of any failures.
   ```

2. **Re-check the original symptom** — verify the specific thing that was broken is now working

3. If smoke tests fail, diagnose the failure and loop back to Phase 3 for an additional fix (new spec if it's a different issue, update existing spec if related).

### Phase 5: Advise

**Always produce this output.** This is the final deliverable of every rockport-ops invocation.

```markdown
## Rockport Ops Report

**Status**: RESOLVED | MITIGATED | ESCALATED
**Spec**: OPS-NNN — short description
**Root cause**: What actually broke and why
**Fix applied**: What changed (files, config, infra)
**Deployed**: Yes/No — whether config push/deploy was run
**Smoke tests**: NN/NN passed | N failures (listed)

### For the calling project
- [Action needed / no action needed]
- [Specific guidance: retry request, use different model, wait for X, etc.]
- [Any behavior changes to be aware of — new endpoints, changed limits, etc.]
- [If the issue was on the caller's side, explain what they should change]
```

**Status definitions:**
- **RESOLVED** — Root cause identified and fixed, smoke tests passing
- **MITIGATED** — Service restored but root cause fix is pending or partial
- **ESCALATED** — Cannot be fixed automatically (e.g., AWS outage, requires manual console action, needs admin IAM)

## Conventions

- `$PROJECT_ROOT` in reference files means the repository root (the current working directory). Resolve it before running commands.

## Gotchas

- **SSM commands return async.** `send-command` returns immediately. You must `sleep 3` then `get-command-invocation` to read output. Forgetting this gives empty results.
- **Instance takes ~3 minutes after start.** If idle shutdown stopped the instance, starting it is not enough — services need time to boot. Don't report "service down" until SSM shows the instance online for 3+ minutes.
- **Smoke tests need a temp API key.** `smoke-test.sh` creates and cleans up its own key. If the master key is wrong or LiteLLM is down, key creation fails and all 43 tests show as failures — the root cause is auth, not the individual tests.
- **Config push is not atomic.** The SSM command stops services, downloads, extracts, restarts. If it fails mid-way, services may be down. Check SSM command output for which step failed before assuming the config is bad.
- **`terraform output` needs init.** If terraform hasn't been initialized in this session, `terraform output` fails. Run `terraform -chdir=$PROJECT_ROOT/terraform init -backend=false` first if needed, or read values from `terraform.tfvars` directly.
- **Operator-role profiles drive AWS access (017).** The CLI no longer relies on a long-lived `AWS_PROFILE=rockport`. Each subcommand resolves through `SUBCOMMAND_ROLE` and assumes one of `rockport-readonly-role`, `rockport-runtime-ops-role`, or `rockport-deploy-role` via MFA-gated STS. If a session is missing/expired the CLI prompts for a TOTP code. Run `./scripts/rockport.sh auth` once at session start and `auth status` to inspect cached sessions. The legacy `rockport` profile is not auto-used; the only escape hatch for IAM-bootstrap is `ROCKPORT_AUTH_DISABLED=1`.
- **Cloudflare 403 vs LiteLLM 403.** Both return 403 but for different reasons. Cloudflare 403 = missing CF-Access headers or WAF block. LiteLLM 403 = invalid/expired API key or --claude-only restriction. Check response body to distinguish.
- **Journalctl errors may be stale.** Always use `--since "10 min ago"` to scope log queries. Old errors from previous incidents will mislead diagnosis.

## Rules

1. **Subagents for I/O, main context for decisions.** All AWS CLI output, log dumps, curl responses, and smoke test output go through subagents. The main context only sees summaries.

2. **Readonly role by default (017).** Diagnostics run under `rockport-readonly-role` — no `ssm:SendCommand`, no IAM, no mutate. The CLI's `SUBCOMMAND_ROLE` map already ensures this; just call subcommands and let MFA escalation happen as needed. Escalate to `runtime-ops` for `config push`, `upgrade`, `start`, `stop`, `logs`, or `status --instance`. Escalate to `deploy` only for `terraform apply` / `destroy`. Escalate to admin (unset AWS_PROFILE; uses `rockport-admin` directly) only for IAM policy changes or `rockport.sh init`. See [aws-access.md](references/aws-access.md).

3. **Speckit for everything.** No direct code edits outside the speckit pipeline. The only exception is immediate operational actions (restart, start instance) to restore service — and even those get a spec if the root cause is a bug.

4. **IaC must match reality.** If you change anything on AWS, the terraform and project code must reflect it. Never let code and infrastructure diverge.

5. **Cost-conscious testing.** When a test API call is needed, use the cheapest model (Haiku) with minimal tokens. Never generate images or videos as diagnostic tests.

6. **Full smoke tests after every fix.** No exceptions. The 43-assertion suite costs ~$0.05 and catches regressions.

7. **Phase 5 is mandatory.** Every invocation produces the structured ops report, whether the issue was a simple restart or a complex multi-file fix.
