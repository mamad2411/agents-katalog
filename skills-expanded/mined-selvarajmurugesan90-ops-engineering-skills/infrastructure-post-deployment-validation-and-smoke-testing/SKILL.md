---
name: infrastructure-post-deployment-validation-and-smoke-testing
description: >
  Verifies that a Terraform apply, CloudFormation deploy, or Ansible
  playbook run actually produced working infrastructure — resource
  existence and configuration checks, connectivity/health smoke tests, and
  automated post-apply assertions — rather than treating a clean "apply
  succeeded" exit code as proof the system works. Use when the user asks
  to "verify this deployment actually worked," "write a smoke test after
  terraform apply/cloudformation deploy," "check the resource is actually
  reachable/configured correctly post-deploy," "add post-deployment
  validation to the pipeline," or "our apply succeeded but the service is
  down."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: iac-and-automation-tooling
  maturity: stable
---

# Infrastructure Post-Deployment Validation and Smoke Testing

## Purpose

`terraform apply` exiting 0, a CloudFormation stack reaching
`UPDATE_COMPLETE`, or `ansible-playbook` reporting no failed tasks all
mean exactly one thing: the tool successfully executed the operations it
was told to perform. None of them mean the resulting system actually
works — a security group with an unreachable rule, a load balancer
target group with zero healthy targets, a database that came up but
rejects the application's connection string, or a service that started
but never became ready are all fully consistent with a "successful"
apply. This skill covers the validation layer that has to run *after* the
IaC/config-management tool reports success: checking that resources
actually exist with the expected configuration, and — going one step
further — that the system is functionally healthy from the outside, the
way a real client would observe it. Without this layer, "the pipeline is
green" and "the service works" are two different claims that get
conflated until an incident proves they weren't the same thing.

## When to use

- Immediately after any `terraform apply`, CloudFormation stack
  create/update, or Ansible playbook run that provisions or reconfigures
  production-facing infrastructure, before considering the deployment
  complete.
- Adding an automated post-deploy validation/smoke-test stage to a CI/CD
  pipeline, distinct from and running after the apply/deploy stage itself.
  Also see
  [aws-codepipeline-and-codedeploy](../../../cicd-tooling/skills/aws-codepipeline-and-codedeploy/SKILL.md)
  for CodeDeploy's built-in `ValidateService` lifecycle hook, which is one
  concrete mechanism for wiring this in on AWS.
- Investigating an incident where the deployment tooling reported success
  but the service is degraded or fully down — determining what a
  pre-existing smoke test would have caught.
- Deciding what to actually assert post-deploy: existence checks (does
  the resource exist with the right configuration) versus functional
  smoke tests (does the system respond correctly to a real request) are
  different validation layers and most deployments need both.

## Prerequisites & environment

- Read access to whichever cloud/API surface is being validated (AWS
  CLI/SDK, `kubectl`, a database client) with credentials scoped to
  read-only where the validation itself doesn't need write access.
- The deployment tool's own state/output as the source of truth for
  *what* to check: Terraform outputs (`terraform output -json`),
  CloudFormation stack outputs (`aws cloudformation describe-stacks
  --query Stacks[0].Outputs`), or an Ansible fact/registered variable —
  validation should check the resources the deployment *actually*
  produced, not a hardcoded list that can drift out of sync with the
  IaC.
- A place for smoke tests to run from that has real network access to
  the target (not just IAM/API access) — a security-group or firewall
  rule that blocks the validation runner itself will produce false
  failures indistinguishable from a real outage unless the runner's own
  connectivity is understood.
- For functional smoke tests specifically: a defined "healthy" contract
  for the service being validated (a `/healthz` endpoint, an expected
  response code/body, an expected DB query result) — validation without
  a concrete pass/fail contract degenerates into someone eyeballing
  dashboards.
- A rollback or remediation path already decided *before* running
  validation, not designed in the moment a check fails — post-deploy
  validation is only useful if there's a defined next action (automatic
  rollback, page on-call, block pipeline progression) when it fails.

## Step-by-step guidance

1. **Separate "did the resource get created" from "does the system
   work" as two distinct check categories**, and run both — existence
   checks are necessary but not sufficient:
   ```bash
   # Existence/configuration check (Terraform-managed AWS RDS instance)
   aws rds describe-db-instances \
     --db-instance-identifier checkout-db-prod \
     --query 'DBInstances[0].{Status:DBInstanceStatus,Engine:Engine,MultiAZ:MultiAZ}'
   # Expect: {"Status": "available", "Engine": "postgres", "MultiAZ": true}
   ```
   ```bash
   # Functional smoke test — actually connect and query
   PGPASSWORD="${DB_SMOKE_TEST_PASSWORD}" psql \
     -h "$(terraform output -raw db_endpoint)" -U smoke_test_ro -d checkout \
     -c "SELECT 1;" -tA
   # Expect: "1" — proves network reachability, auth, and query execution,
   # none of which "DBInstanceStatus: available" alone guarantees.
   ```

2. **Derive what to check from the deployment tool's own outputs**,
   never a separately maintained hardcoded list that can silently drift:
   ```bash
   ENDPOINT=$(terraform output -raw alb_dns_name)
   EXPECTED_TG_ARN=$(terraform output -raw target_group_arn)

   aws elbv2 describe-target-health --target-group-arn "$EXPECTED_TG_ARN" \
     --query 'TargetHealthDescriptions[].TargetHealth.State'
   # Expect every entry: "healthy" — not just "the target group exists"
   ```
   For CloudFormation, the equivalent is reading `Outputs` from
   `describe-stacks` rather than assuming a resource's name/ARN pattern;
   for Ansible, register the actual result of a task
   (`register: db_result`) and assert against it in a subsequent task
   rather than assuming success from the play recap alone.

3. **Write functional smoke tests that exercise the actual failure modes
   that matter**, not just "the process is running":
   ```bash
   #!/usr/bin/env bash
   set -euo pipefail

   ENDPOINT="https://$(terraform output -raw alb_dns_name)"

   status=$(curl -s -o /dev/null -w '%{http_code}' --max-time 5 "${ENDPOINT}/healthz")
   if [[ "$status" != "200" ]]; then
     echo "FAIL: /healthz returned ${status}, expected 200" >&2
     exit 1
   fi

   # A shallow health check that only pings the process is not enough —
   # exercise a real dependency path the health check should cover:
   body=$(curl -s --max-time 5 "${ENDPOINT}/api/v1/checkout/ping")
   if [[ "$body" != *'"database":"ok"'* ]]; then
     echo "FAIL: checkout ping did not report database ok: ${body}" >&2
     exit 1
   fi

   echo "PASS: smoke test succeeded against ${ENDPOINT}"
   ```
   A health check that only confirms the process/port is listening
   ("liveness") is a much weaker signal than one that confirms the
   process can actually reach its dependencies and serve a real request
   ("readiness") — write smoke tests against the latter.

4. **Run validation as its own pipeline stage, after apply/deploy,
   gating progression to the next environment**:
   ```yaml
   # GitHub Actions, abbreviated
   jobs:
     terraform-apply:
       runs-on: ubuntu-latest
       steps:
         - run: terraform apply -auto-approve tfplan

     post-deploy-validation:
       needs: terraform-apply
       runs-on: ubuntu-latest
       steps:
         - name: Resource existence checks
           run: ./scripts/validate_resources.sh
         - name: Functional smoke tests
           run: ./scripts/smoke_test.sh
         - name: Fail pipeline (and trigger rollback) on any check failure
           if: failure()
           run: ./scripts/trigger_rollback.sh
   ```
   Keep this as a genuinely separate stage/job from the apply itself —
   folding a smoke test into the same job as `terraform apply` makes it
   easy to accidentally skip on a partial retry, and separates "did the
   tool succeed" from "did validation pass" in the pipeline's own status
   history.

5. **For CloudFormation, use `ValidateService`-equivalent hooks or
   `cfn-signal`/custom resources where the platform provides them**,
   rather than only checking stack status:
   ```bash
   aws cloudformation describe-stacks --stack-name checkout-api-prod \
     --query 'Stacks[0].StackStatus'
   # "UPDATE_COMPLETE" means CloudFormation finished its operations —
   # it says nothing about whether the new resources are functionally
   # healthy; always follow with the same existence + functional checks
   # as step 1-3.
   ```

6. **For Ansible, assert against registered results rather than trusting
   the play recap alone**:
   ```yaml
   - name: Check application health endpoint post-deploy
     ansible.builtin.uri:
       url: "http://{{ inventory_hostname }}:8080/healthz"
       status_code: 200
       timeout: 5
     register: health_check
     retries: 5
     delay: 10
     until: health_check.status == 200

   - name: Fail the play explicitly if health check never passed
     ansible.builtin.fail:
       msg: "Post-deploy health check failed on {{ inventory_hostname }}"
     when: health_check.status != 200
   ```
   `retries`/`until` accounts for a service that takes a few seconds to
   become ready after the process starts — a smoke test run too
   immediately after "service started" is a common source of false
   failures.

7. **Decide and wire the failure response before it's needed** — a
   validation stage that fails and does nothing but print red text in CI
   isn't actually protecting anything:
   > **Warning:** Automatic rollback (`terraform apply` of the previous
   > known-good plan, CloudFormation stack rollback, redeploying a prior
   > CodeDeploy revision) is itself a change to production and should be
   > exercised/tested before relying on it during a real incident — an
   > untested rollback path can fail exactly when it's needed most.
   At minimum, a failed post-deploy validation stage should block
   promotion to the next environment and page on-call rather than
   silently leaving a partially-validated deployment in place.

## Best practices

- Treat "apply succeeded" and "deployment validated" as two separate,
  separately-reported outcomes in the pipeline — never collapse them into
  one green checkmark.
- Prefer a small number of smoke tests that exercise real dependency
  paths (database connectivity, downstream service calls, actual request/
  response shape) over a large number of shallow checks (process
  running, port open) that give false confidence.
- Source what to validate from the IaC tool's own outputs/state, never a
  parallel hardcoded inventory that can drift.
- Make validation idempotent and safe to re-run — a validation script
  that mutates state (rather than only reading/exercising read paths) can
  itself become a source of incidents.
- Time-box smoke tests with short, explicit timeouts (`--max-time`,
  `timeout:`) so a hung dependency fails the validation stage quickly
  rather than hanging the pipeline.
- Version and review smoke test scripts with the same rigor as the IaC
  they validate — a stale smoke test asserting against an endpoint that
  no longer exists gives false green just as dangerously as no smoke
  test at all.
- Where the platform supports it (CodeDeploy's `ValidateService`,
  Kubernetes readiness probes), wire the smoke test into the deployment
  tool's own gating mechanism rather than only as an after-the-fact CI
  step, so a failing check can block traffic shift automatically.

## Common pitfalls

- **Symptom:** `terraform apply`/CloudFormation stack update reports
  success, but the service is down or degraded minutes later.
  **Fix:** This is precisely the gap this skill exists to close — add a
  post-deploy validation stage with both existence checks (step 1) and a
  functional smoke test (step 3) that actually exercises the request
  path a real user/client takes, not just a resource-status API call.

- **Symptom:** A smoke test run immediately after deploy fails, but
  manually checking the same endpoint 30 seconds later succeeds fine.
  **Fix:** The service takes a few seconds to become ready (connection
  pools warming, health checks stabilizing) after it starts. Add
  `retries`/backoff to the smoke test (as in the Ansible example, step
  6) rather than treating a single immediate check as authoritative, and
  set the retry window based on the service's actual observed startup
  time, not an arbitrary guess.

- **Symptom:** A health check endpoint always returns `200 OK` even when
  a critical downstream dependency (database, cache, queue) is down.
  **Fix:** The health check is shallow — it confirms the process is
  alive, not that it can do its job. Extend it to check real
  dependencies (a lightweight query against the database, a ping to a
  required downstream service) and report a distinct failure state, then
  have the smoke test assert against that deeper signal rather than just
  process liveness.

- **Symptom:** A post-deploy validation script itself fails intermittently
  in CI with a connection timeout, even though the actual service is
  fine.
  **Fix:** The validation runner (CI runner, Lambda, whatever executes
  the smoke test) likely lacks network path to the target — a security
  group/firewall rule scoped to expected clients doesn't include the
  validation runner's egress IP/VPC. Confirm the runner's own
  connectivity as a prerequisite check before trusting a failure as a
  real signal about the deployed service.

- **Symptom:** A deployment's post-deploy validation fails, the pipeline
  shows red, but nothing actually stops the bad deployment from serving
  production traffic.
  **Fix:** The validation stage isn't wired to an actual gate/rollback —
  a red CI stage that nobody's paged for and that doesn't block traffic
  shift is validation theater. Wire the failure to block promotion (fail
  the pipeline before a subsequent "shift traffic"/"promote to next
  environment" stage can run) and to page on-call, or — where the
  platform supports it — tie it directly into the deploy tool's native
  traffic-shifting gate (e.g. CodeDeploy's `ValidateService` hook
  blocking `AllowTraffic`).

## Worked example

**Scenario:** A Terraform apply provisions a new ALB + target group +
ECS service for a checkout API. The team wants automated post-deploy
validation — resource existence/health plus a functional smoke test —
gating promotion to the next environment.

`scripts/validate_resources.sh`:
```bash
#!/usr/bin/env bash
set -euo pipefail

TG_ARN=$(terraform output -raw target_group_arn)
UNHEALTHY=$(aws elbv2 describe-target-health --target-group-arn "$TG_ARN" \
  --query "TargetHealthDescriptions[?TargetHealth.State!='healthy'] | length(@)")

if [[ "$UNHEALTHY" -gt 0 ]]; then
  echo "FAIL: $UNHEALTHY target(s) not healthy in target group $TG_ARN" >&2
  aws elbv2 describe-target-health --target-group-arn "$TG_ARN"
  exit 1
fi

echo "PASS: all targets healthy in $TG_ARN"
```

`scripts/smoke_test.sh`:
```bash
#!/usr/bin/env bash
set -euo pipefail

ENDPOINT="https://$(terraform output -raw alb_dns_name)"
MAX_ATTEMPTS=6
DELAY_SECONDS=10

for attempt in $(seq 1 "$MAX_ATTEMPTS"); do
  status=$(curl -s -o /tmp/body.json -w '%{http_code}' --max-time 5 \
    "${ENDPOINT}/api/v1/checkout/ping" || echo "000")
  if [[ "$status" == "200" ]] && grep -q '"database":"ok"' /tmp/body.json; then
    echo "PASS: smoke test succeeded on attempt ${attempt}"
    exit 0
  fi
  echo "Attempt ${attempt}/${MAX_ATTEMPTS}: status=${status}, retrying in ${DELAY_SECONDS}s"
  sleep "$DELAY_SECONDS"
done

echo "FAIL: smoke test did not pass after ${MAX_ATTEMPTS} attempts" >&2
exit 1
```

Pipeline stage (GitHub Actions), gating promotion to `staging`:
```yaml
post-deploy-validation:
  needs: terraform-apply
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - run: terraform init && terraform output -raw target_group_arn > /dev/null
    - name: Validate resources
      run: ./scripts/validate_resources.sh
    - name: Smoke test
      run: ./scripts/smoke_test.sh

promote-to-staging:
  needs: post-deploy-validation   # only runs if validation passed
  runs-on: ubuntu-latest
  steps:
    - run: ./scripts/promote.sh --env staging
```
If `validate_resources.sh` or `smoke_test.sh` exits non-zero, the
`promote-to-staging` job never runs — the pipeline stops with the
deployment applied but unpromoted, and the failure notification routes to
the on-call channel for investigation rather than the change silently
reaching the next environment.

## Cross-references

- [infrastructure-as-code-terraform](../../../devops/skills/infrastructure-as-code-terraform/SKILL.md) — the apply/plan-review workflow this skill's validation stage runs after.
- [aws-cloudformation-templates](../aws-cloudformation-templates/SKILL.md) — stack status and output patterns referenced for the CloudFormation-specific validation steps here.
- [ansible-playbook-and-role-design](../ansible-playbook-and-role-design/SKILL.md) — registered-result assertion pattern for validating a playbook run's actual effect, not just its recap.
- [aws-codepipeline-and-codedeploy](../../../cicd-tooling/skills/aws-codepipeline-and-codedeploy/SKILL.md) — the `ValidateService` lifecycle hook as a native mechanism for gating traffic shift on exactly this kind of check.
- [terragrunt-configuration-and-dry-run-validation](../terragrunt-configuration-and-dry-run-validation/SKILL.md) — the plan-time (pre-apply) validation layer this skill's post-apply checks complement.
