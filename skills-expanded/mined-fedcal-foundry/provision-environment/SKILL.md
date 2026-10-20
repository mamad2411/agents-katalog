---
name: provision-environment
description: Create or extend Terraform/OpenTofu for a new environment, with remote state and locking, secrets handling and least-privilege identity for CI and workloads. Use when adding staging or production, splitting a shared account, moving from local state to remote, or replacing long-lived cloud keys with OIDC federation.
user-invocable: true
argument-hint: "[env-name] [--cloud aws|azure|gcp] [--layer network|data|platform|apps] [--plan-only]"
model: opus
effort: high
metadata:
  foundry.vertical: operations
  foundry.io: "environment request -> IaC root module + backend + identity + risk.v1"
license: Apache-2.0
---

# Provision environment

Stands up a new environment as code, with the three things that are usually retrofitted painfully
later: **state that is safe**, **secrets that are never in git**, and **identity that is scoped to
one environment**.

**Do not use it** to decide *which* cloud or service (`cloud-architect` first), for the very first
bootstrap of an organisation (the account/subscription/project hierarchy and its guardrails are a
separate, mostly manual, one-time task), or to hand-provision resources through a console.

Assume `terraform`; substitute `tofu` throughout if the repository uses OpenTofu. Pick one per
repository and record which in the README.

## Step 0 — Runbook first

Foundry's standing rule: check for an existing runbook before improvising.

```
runbook_list          # MCP tool from foundry-core
```

If a runbook covers this environment or this layer, follow it and update it afterwards. If none
exists and this task will recur, you will create one at step 8.

## Step 1 — Read what exists

```bash
find . -name '*.tf' -not -path './.terraform/*' | head -40
grep -rn 'backend "' --include='*.tf' .
grep -rn 'source\s*=' --include='*.tf' . | grep -v '^\s*#'      # module pins
terraform version
terraform providers            # what is actually in play
ls -1 envs/ environments/ 2>/dev/null
```

Record: the existing layout, whether state is local (a `terraform.tfstate` file in the repo is a
`critical` finding — it may contain plaintext secrets and it may be committed), which modules are
unpinned, and whether workspaces are being used to separate production.

Check for the worst case explicitly:

```bash
git log --all --oneline -- '*.tfstate' | head       # state ever committed?
grep -rniE 'password|secret|api_key|private_key' --include='*.tfvars' . | head
```

Anything found here is rotated **before** anything else proceeds.

## Step 2 — Decide the boundaries

Two decisions, both hard to change later.

**Account boundary.** One cloud account / subscription / project **per environment**. This is the
only boundary that survives a wrong `-var-file`, a stolen CI token or a misconfigured provider.
Network segmentation inside one account does not stop an IAM mistake. If the request is "add
staging to the existing production account", push back and record the risk.

**Layer boundary.** One state per environment per layer, because it bounds blast radius and keeps
plan times short:

```
network/    VPC, subnets, routing, DNS zones        - changes twice a year
data/       databases, object storage, keys         - changes rarely, destroys hurt
platform/   cluster, registry, CI identity, secrets - changes monthly
apps/       per-service resources                   - changes weekly
```

Target: **plan time < 3 minutes per layer.** Above that, people stop reading the plan, and a plan
nobody reads is not a control.

Cross-layer references go through explicit outputs or data sources. Use
`terraform_remote_state` sparingly and never in the direction of higher-churn → lower-churn.

## Step 3 — Layout

Root module per environment, shared modules underneath. See
`references/terraform-layout.md` for the full rationale and the two alternatives.

```
infra/
  modules/<name>/{main,variables,outputs,versions}.tf
  envs/<env>/<layer>/
    main.tf            # ~30 lines: module calls with this environment's inputs
    variables.tf
    backend.tf         # backend block; values via -backend-config
    <env>.backend.hcl  # bucket/key/region - not secret, but environment-specific
    terraform.tfvars
    versions.tf        # required_version + required_providers, pinned
    .terraform.lock.hcl  # COMMITTED, covering every platform you build on
```

**Do not use CLI workspaces to separate production from non-production.** They share one backend
and one credential set; the only thing standing between you and production is which workspace
happens to be selected in your shell. Workspaces are fine for ephemeral, identical copies such as
per-PR review environments, where a mistake is cheap.

Copy-paste detector — run it before you finish:

```bash
diff envs/<existing-env>/<layer>/main.tf envs/<new-env>/<layer>/main.tf
```

Every difference must be a deliberate policy difference (multi-AZ, deletion protection, retention,
sizing). Anything else means the module boundary is in the wrong place.

## Step 4 — Bootstrap state

The state backend cannot itself live in the state it stores. Handle the chicken-and-egg once,
deliberately, using `references/backend-bootstrap.tf`.

Requirements, all of them:

- Encryption at rest with a customer-managed key. **State contains secrets in plaintext** —
  generated passwords, private keys, anything a resource returns.
- Versioning on the bucket/container. State corruption is recoverable *only* from a previous
  object version.
- Access restricted to the CI identity plus a small break-glass role. Access logging on.
- Locking configured **and verified**:

```bash
terraform init -backend-config=<env>.backend.hcl
terraform plan &            # start one
terraform plan              # the second must block or fail on the lock
```

  A backend you *believe* locks is not a backend that locks.
- `prevent_destroy` on the state bucket itself.

Stuck lock recovery (a cancelled CI job): `terraform force-unlock <LOCK-ID>` — **only** after
confirming no apply is still running. Force-unlocking a live apply corrupts state.

## Step 5 — Identity: least privilege, no long-lived keys

Two distinct identities. Do not merge them.

**CI identity** — OIDC federation from GitHub Actions, no static keys anywhere. Full trust-policy
detail in `references/oidc-github-cloud.tf`. The subject condition is the control:

- deploy role: `repo:<ORG>/<REPO>:environment:<ENV>` — strongest, because the GitHub environment
  can also require reviewers;
- plan-only role (pull requests): read-only permissions, `repo:<ORG>/<REPO>:pull_request`;
- **`repo:<ORG>/<REPO>:*` is a finding, not a configuration.**

Split plan from apply: the PR lane gets read + plan; only the environment-gated lane can apply.

**Workload identity** — the running application authenticates as itself
(IRSA / EKS Pod Identity, Azure workload identity, GCP Workload Identity), scoped to the
resources that one service needs. No shared "app" credential across services.

Verify nothing static survives:

```bash
gh secret list --repo <OWNER>/<REPO>
gh api repos/<OWNER>/<REPO>/environments --jq '.environments[].name' \
  | xargs -I{} gh secret list --env {} --repo <OWNER>/<REPO>
```

Rotate anything key-shaped at the provider **before** deleting it from GitHub — deleting the
secret does not invalidate the credential.

## Step 6 — Secrets

Rules, in `references/secrets.md` with the full reasoning:

1. **No secret values in `.tf` or `.tfvars`, ever.** They end up in git and in state.
2. Secrets live in the cloud secret manager. Terraform creates the *container* and the *access
   policy*; a human or a separate pipeline puts the *value* in, and Terraform never reads it back.
3. Where a value must be generated, generate it in the cloud (a provider-managed password) rather
   than with a Terraform random resource whose output lands in state in plaintext.
4. Applications read secrets at runtime via workload identity — not through environment variables
   baked at deploy time, which are visible in the pod spec to anyone with `get pod`.
5. Rotation is designed on day one: the mechanism, the cadence, and what breaks during rotation.

## Step 7 — Guard the apply

Wire the policy and the safety rails before the first production apply.
`references/policy-checks.md` has the starter rule set.

```bash
terraform plan -out=tfplan -lock-timeout=<DURATION> -input=false
terraform show -json tfplan > tfplan.json

# the auto-apply gate: destroys and replacements must be ZERO
DANGEROUS=$(jq '[.resource_changes[] | select(.change.actions | index("delete"))] | length' tfplan.json)
echo "destroy/replace actions: $DANGEROUS"
test "$DANGEROUS" -eq 0 || echo "HUMAN REVIEW REQUIRED"

# what exactly, and why
jq -r '.resource_changes[] | select(.change.actions | index("delete"))
       | "\(.change.actions|join("+"))\t\(.address)"' tfplan.json

terraform apply tfplan          # apply the SAVED plan, never a fresh one
```

**Applying a re-plan is the most common way a reviewed change becomes an unreviewed one.**
Between plan and apply, someone else's merge or a drifted resource changes the outcome.

Also add now, not later:
- `prevent_destroy` on every stateful resource whose loss would be an incident;
- a scheduled drift job per layer (`terraform plan -detailed-exitcode`, exit code 2 = drift) that
  **alerts and never auto-applies** — auto-reverting can undo an emergency fix currently keeping
  production alive;
- the mandatory tag set (owner, environment, cost-centre, data-classification), enforced by
  policy. This is what makes cost allocation possible later.

## Step 8 — Record

Emit `risk.v1` to `.foundry/blackboard/<wave>/iac-engineer.json` via `blackboard_write`: one
artifact per dangerous operation identified, each with `detection`, `mitigation` and
`contingency`.

Write `.foundry/runbooks/provision-<env>.md` (frontmatter `title` and `trigger`) with the exact
command sequence, the bootstrap order, and the traps you hit. Foundry's standing rule: after the
work, update the runbook.

If `superpowers` is installed, invoke `superpowers:writing-plans` before a multi-layer change and
`superpowers:verification-before-completion` before claiming done.

## Rollback

**Reverting the commit does not restore deleted data.** Say this in every review.

1. **Before every production apply:** `terraform state pull > .foundry/scratch/<session>/state-<LAYER>-<UTC>.json`
   (contains secrets — treat and delete accordingly) and keep `tfplan.json` as the record of what
   was intended.
2. **Configuration-only regression:** `git revert <SHA>` → plan → review → apply. Minutes.
3. **A resource was replaced or destroyed:** reverting the code recreates an *empty* resource with
   the same name. Real recovery is restore-from-snapshot, then `terraform import` the restored
   resource, then a plan that shows no changes. Rehearse this per stateful resource; an untested
   restore is not a backup.
4. **State corrupted or partially applied:** restore the previous object version from the
   versioned bucket, `force-unlock` if required, then plan and read the delta before acting.
5. **CI identity locked itself out:** use the break-glass human identity — provisioned in advance,
   MFA-protected, its use alerting. A break-glass path created during an incident is not a control.
6. **Something became publicly exposed:** containment before correctness. Make it private, then
   fix the code, then rotate everything that was reachable.

## References

- `references/terraform-layout.md` — layers, root modules, module versioning, the three
  environment-separation patterns and why workspaces are not one of them.
- `references/backend-bootstrap.tf` — state bucket/table with encryption, versioning, locking,
  and the bootstrap order.
- `references/oidc-github-cloud.tf` — CI federation for AWS, Azure and GCP, with the subject
  conditions spelled out.
- `references/secrets.md` — what Terraform may and may not know, generation, rotation, runtime
  access.
- `references/policy-checks.md` — the starter policy set and the auto-apply gate.

## Deliberately not covered

- Organisation bootstrap: account hierarchy, SCPs/management groups, billing, SSO.
- CloudFormation, Bicep/ARM, Pulumi, CDK/CDKTF.
- Application deployment into the environment — `deploy-strategy`, `scaffold-pipeline`.
- Kubernetes objects. Provision the cluster here; deploy into it with GitOps. Terraform's
  plan/apply model and Kubernetes' continuous reconciliation disagree, and manifest resources that
  need the cluster to exist at plan time create a bootstrap ordering problem.
- Cost modelling — `foundry-economics`; this skill only guarantees the tags that make it possible.

## Exit criteria

- [ ] Environment has its own cloud account/subscription/project, or the exception is recorded as
      a `risk.v1` with an owner.
- [ ] Remote backend: encrypted with a customer-managed key, versioned, access-logged,
      `prevent_destroy` set, and locking **verified by a concurrent-plan test**.
- [ ] Zero local state files; `git log --all -- '*.tfstate'` is empty, or every leaked secret has
      been rotated.
- [ ] Plan time **< 3 min** per layer.
- [ ] Zero unpinned module or provider sources; `.terraform.lock.hcl` committed for every build
      platform.
- [ ] No prod/non-prod separation by CLI workspace.
- [ ] `diff` against the sibling environment shows only deliberate policy differences.
- [ ] CI authenticates by OIDC with an environment- or ref-scoped subject; **no wildcard subject**;
      **zero** long-lived cloud keys in repository or environment secrets.
- [ ] Plan and apply lanes are separate identities with different permissions.
- [ ] Zero secret values in `.tf`/`.tfvars`; secret containers created by Terraform, values not.
- [ ] Policy checks run against `tfplan.json` as a required check.
- [ ] Auto-apply lane provably restricted to plans with **0 delete and 0 replace**.
- [ ] `prevent_destroy` on every stateful resource whose loss would be an incident.
- [ ] Scheduled drift job per layer, alerting, with a named owner.
- [ ] Restore-from-backup rehearsed and **timed** for at least one stateful resource, recorded in
      `.foundry/runbooks/restore-<layer>.md`.
