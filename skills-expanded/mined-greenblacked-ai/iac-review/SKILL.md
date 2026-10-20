---
name: iac-review
description: "Review an infrastructure-as-code change against the machine-readable plan JSON rather than the human-readable plan text — blast radius and destroys first, then replacement causes, drift, state moves, secrets in state, pinning, the policy-as-code gate, cost, and a verdict. Also covers Ansible review via check mode, --diff, and idempotence. Use this skill whenever the user asks you to review, sanity-check, approve, risk-assess, or explain a Terraform or OpenTofu plan, an IaC pull request, a .tf or .tfvars diff, a tfplan or plan.json file, a backend or state change, or an Ansible playbook change — including casual phrasings like \"is this safe to apply\", \"why is it recreating my database\", or \"what will this actually do\". Do not use it for authoring new modules, debugging a provider crash, or open-ended cloud architecture advice."
allowed-tools: Bash(terraform:*), Bash(tofu:*), Bash(jq:*), Bash(tflint:*), Bash(checkov:*), Bash(tfsec:*), Read, Grep, Glob
---

# Infrastructure-as-Code Review

A good review answers one question with evidence: *what does this destroy, and can we get it back?* Everything else is secondary.

The job is hard because the artefact most people review is designed for reading, not for auditing. Terraform's plan text elides — `(30 unchanged attributes hidden)`, nested blocks collapsed, long diffs paged past. The one line that matters, `# forces replacement`, sits mid-scroll in a wall of green `+` symbols, and a human eye that has already read 400 lines will not catch it. Meanwhile the reviewer approves a plan generated on Tuesday and the pipeline applies a plan generated on Thursday against a state that moved underneath it. Every rule below exists because one of those two things cost someone a database.

## Scope

Use for: reviewing a Terraform/OpenTofu plan or PR, assessing the risk of an apply, explaining why a resource is being replaced, auditing state-moving operations (`moved`, `import`, `state mv`, `state rm`), checking pinning and policy gates, reviewing an Ansible change.

Do not use for: writing new modules, debugging provider errors, or greenfield architecture design.

## Workflow

### 1. Generate the reviewable artefact

Never review the plan text. Review the plan JSON. Produce it yourself rather than trusting a pasted excerpt — a pasted excerpt is precisely where truncation hides.

```bash
terraform init -input=false -lockfile=readonly
terraform validate
terraform fmt -check -recursive -diff
terraform plan -input=false -lock-timeout=120s -out=tfplan
terraform show -json tfplan > plan.json
```

`-lockfile=readonly` verifies checksums against `.terraform.lock.hcl` and refuses to rewrite it, so an unreviewed provider bump fails the build instead of landing silently. The saved `tfplan` is the artefact that gets applied later; `plan.json` is the artefact you review. They are the same plan, which is the entire point.

If you cannot run Terraform (no credentials, no state access), say so plainly and review the configuration diff only, labelling the verdict as partial. A configuration review is not a plan review and should not be presented as one.

Gate on the plan-level flags before reading anything else (Terraform 1.8+):

```bash
jq -r 'def f(k): if has(k) then (.[k]|tostring) else "n/a" end;
       "applyable=\(f("applyable")) complete=\(f("complete")) errored=\(f("errored"))"' plan.json
```

Use `has()` rather than `//` here: these are booleans, and jq's alternative operator treats `false` as absent, so `.complete // "n/a"` reports a genuinely incomplete plan as unknown.

Automation should use `applyable` as its primary condition — the docs say so explicitly, because the exact definition may shift in future versions. A plan that is `applyable` but not `complete` will not converge in one round; it needs another plan/apply cycle, and the reviewer should know that before approving. In CI, `terraform plan -detailed-exitcode` returns `0` for an empty diff, `1` for an error, and `2` for changes present.

### 2. Blast radius, destroys before creates

Once `plan.json` exists and the flags gate above has passed, if the plan is large — hundreds of resource changes, a whole workspace — hand it to the `plan-reviewer` subagent instead of reading it here. It returns what the apply will actually do, destroys first, with the reason each resource is being replaced, and the JSON itself never enters this conversation. The rest of this step is for plans small enough to read.

Read deletions first. Creates are recoverable; deletions frequently are not.

The valid `actions` values are exactly `["no-op"]`, `["create"]`, `["read"]`, `["update"]`, `["delete","create"]`, `["create","delete"]`, and `["delete"]`. The two replace forms are spelled out as pairs deliberately, so a caller can scan the array for `"delete"` and catch all three situations in which an object goes away. So the canonical test is membership, not a string match on the word "replace":

```bash
# Action histogram — the shape of the change in one screen
jq -r '.resource_changes[] | select(.change.actions != ["no-op"])
       | .change.actions | join("+")' plan.json | sort | uniq -c | sort -rn

# Everything that will be deleted, with the reason Terraform gives
jq -r '.resource_changes[] | select(.change.actions | index("delete"))
       | [(.change.actions|join("+")), .address, (.action_reason // "no_reason_given")]
       | @tsv' plan.json | column -t
```

Then run the stateful tripwire. This is a coarse regex on resource type and it is meant to be coarse — a false positive costs thirty seconds, a false negative costs a restore:

```bash
jq -r --arg re 'db_instance|rds_cluster|s3_bucket|ebs_volume|disk|kms_key|dns_zone|eip|efs_file_system|sql_database_instance|storage_bucket' '
  .resource_changes[]
  | select(.change.actions | index("delete"))
  | select(.type | test($re))
  | [.address, .type, (.action_reason // "-")] | @tsv' plan.json
```

### 3. Establish why

For each deletion or replacement, name the cause. `action_reason` carries it, with this enumerated set:

| Value | What it means for the reviewer |
| --- | --- |
| `replace_because_tainted` | Someone marked the object tainted. Ask who and why; prefer `-replace` going forward |
| `replace_because_cannot_update` | The provider says the change is not updatable in place. Read `replace_paths` |
| `replace_by_request` | A human passed `-replace=`. The request itself needs justifying |
| `delete_because_no_resource_config` | The resource block was removed from config. Intentional, or a bad merge? |
| `delete_because_no_module` | A module call disappeared, or its `count`/`for_each` changed |
| `delete_because_wrong_repetition` | Instance key type no longer matches the repetition mode |
| `delete_because_count_index` | `count` shrank and this index fell off the end |
| `delete_because_each_key` | A `for_each` key vanished — usually a map rename |
| `read_because_config_unknown` | Data source deferred to apply; the plan is partially blind here |
| `read_because_dependency_pending` | Data source waits on a managed resource in the same plan |

Treat unrecognised values as unspecified rather than assuming they are benign; the set is documented as a display hint that may grow.

When the reason is `replace_because_cannot_update`, `replace_paths` names the attribute that forced it. That attribute is the review target — often it is a tag, a name, or a subnet list that someone changed without realising it is immutable:

```bash
jq -r '.resource_changes[] | select(.change.replace_paths != null)
       | .address as $a | .change.replace_paths[]
       | [$a, (map(tostring)|join("."))] | @tsv' plan.json
```

### 4. Drift

A non-empty `resource_drift` means the world changed outside Terraform since the last apply. Never wave it through as noise:

```bash
jq -r '.resource_drift[]? | [.address, (.change.actions|join(","))] | @tsv' plan.json
jq -r '.relevant_attributes[]? | [.resource, (.attribute|tostring)] | @tsv' plan.json
```

`relevant_attributes` tells you which of those external changes actually feed the plan result, so you can separate "someone clicked in the console and it matters" from "someone clicked in the console and it does not". Reconcile drift with `terraform apply -refresh-only`, which prompts before committing detected changes to state. `terraform refresh` is deprecated in favour of that flag precisely because it committed silently.

### 5. State safety

State moves are the operations where a typo deletes production. Prefer the declarative, reviewable forms:

- `moved` blocks for renames and re-parenting. They appear in the plan as `previous_address`, so a reviewer can see the rename rather than infer it from a destroy/create pair.
- `import` blocks for adopting existing infrastructure, with `terraform plan -generate-config-out=generated.tf` to draft the resource bodies. The import shows up in the plan JSON under `change.importing`.

```bash
jq -r '.resource_changes[] | select(.previous_address)
       | [.previous_address, "->", .address, (.change.actions|join(","))] | @tsv' plan.json
jq -r '.resource_changes[] | select(.change.importing)
       | [.address, .change.importing.id] | @tsv' plan.json
jq -r '.resource_changes[] | select(.deposed)
       | [.address, .deposed, (.change.actions|join(","))] | @tsv' plan.json
```

A `deposed` entry means a `create_before_destroy` replacement left an old object behind that a previous apply failed to clean up. It is still real and still billed. Chase it.

`terraform state mv` and `state rm` are break-glass: imperative, unreviewable, and invisible to the next plan's diff. When they are genuinely unavoidable, the runbook begins with `terraform state pull > state-backup-$(date +%s).json` and that backup is attached to the change record before anything else runs.

For forcing a rebuild, use `terraform apply -replace=ADDRESS` rather than `terraform taint`. HashiCorp's stated reasoning is worth repeating verbatim because it is the whole argument: the `-replace` option is recommended "because the change will be reflected in the Terraform plan, letting you understand how it will affect your infrastructure before you take any externally-visible action. When you use `terraform taint`, other users could create a new plan against your tainted object before you can review the effects." `taint` mutates shared state ahead of review; `-replace` puts the decision inside the artefact under review.

### 6. Secrets and state

`sensitive = true` suppresses CLI and UI output. It does nothing else. Terraform still stores the value in plaintext in state and in the plan file. Any review that concludes "it is marked sensitive, so it is fine" has answered a different question than the one asked.

```bash
# Attributes the provider or config marks sensitive, by path
jq -r '.resource_changes[] as $rc | ($rc.change.after_sensitive // {})
       | paths(. == true) as $p
       | [$rc.address, ($p|map(tostring)|join("."))] | @tsv' plan.json

# Sensitive root outputs
jq -r '(.output_changes // {}) | to_entries[] | (.value.change // .value) as $c
       | select($c.after_sensitive == true or $c.before_sensitive == true)
       | [.key, ($c.actions|join(","))] | @tsv' plan.json
```

The actual control is to keep the secret out of state: `ephemeral` variables and blocks (1.10+) and write-only resource arguments (1.11+) are omitted from state and plan files entirely. Where the value must be stored, treat every state file as a secret store in its own right, which for an S3 backend means: remote backend with locking, SSE-KMS under a customer-managed key, a public-access block, a bucket policy denying non-TLS requests, versioning enabled so a corrupt write is recoverable, and read access granted separately from write — plenty of people need to run `plan`, far fewer should be able to read every credential the estate has ever provisioned.

### 7. Pinning

Reproducibility is the difference between a plan you reviewed and a plan you got.

- `required_version` set on the root module; `required_providers` constrained with `~>` so patch releases flow and majors do not.
- `.terraform.lock.hcl` committed, and generated for every platform your consumers run on: `terraform providers lock -platform=linux_amd64 -platform=darwin_arm64 -platform=windows_amd64`. Without this, a Mac developer's `init` rewrites the lockfile the Linux runner depends on.
- CI runs `init -lockfile=readonly` so a lock change fails the build rather than being absorbed into an unrelated PR.
- Module sources pinned to an exact registry version or a 40-character commit SHA. A branch reference such as `?ref=main` means the module you reviewed and the module that applies are different artefacts, and no one will notice until they diverge badly.

Module hygiene belongs here too: child modules do not declare `provider` blocks — that makes them impossible to remove cleanly from state — and a module that needs to act in a second region takes a provider alias through `providers = {}`, not a region string it uses to build its own provider.

### 8. Policy gate

Human review does not scale and does not stay awake. Run the machine checks and treat their output as review evidence, not decoration: `tflint`, `trivy config`, `checkov`, `terrascan` over the source, and Conftest/OPA over `plan.json` for anything that depends on the planned action rather than the configuration text. Sentinel enforcement levels map cleanly onto how much you trust each rule: advisory (log), soft-mandatory (overridable by a named role), hard-mandatory (no override). Read `references/policy-as-code.md` for exact invocations and a worked Rego policy that denies stateful destroys.

### 9. Cost

`infracost diff --path plan.json` against the same artefact you reviewed. A replacement that reads as harmless in the plan can carry a provisioned-IOPS volume or a NAT gateway per subnet. Report the delta as a number.

### 10. Verdict

```markdown
## Verdict
[Approve | Approve with conditions | Block] — one sentence of reasoning.

## Blast radius
[N create, N update, N replace, N destroy. Every destroy and replace listed by
address, with its action_reason and, where relevant, the replace_paths attribute.]

## Stateful resources at risk
[Each one, or "none". For each: named approver required, and the recovery plan.]

## Drift
[resource_drift entries and whether they are expected, or "none".]

## State operations
[moved / import / state mv / state rm, and whether a state backup precedes them.]

## Findings
[Ordered by severity. Each: what, where, why it matters, the fix.]

## Checks run
[Commands run and their results. Checks that could not run, and why.]
```

## The stateful-destroy rule

Any plan that deletes or replaces a stateful resource requires a named human approver and a written recovery plan before it is applied. This holds in every environment, dev included.

The reasoning is not ceremony. "Named" matters because a team-wide approval is nobody's approval at 2am, and the recovery plan needs an owner who knows the restore path. "Written" matters because the recovery plan is where you discover that the RDS instance has `skip_final_snapshot = true`, or that the S3 bucket had versioning off, or that the KMS key you are about to destroy still decrypts four other things — you find that out while writing it down, not while executing it. And "dev included" matters because dev is where the muscle memory forms; a team that rubber-stamps destroys in dev will rubber-stamp one in prod, and the only difference between those two plans is a string in a workspace name.

Encode it as a policy rule as well as a human one, so the gate holds when the reviewer is tired.

## Ansible

The same discipline transfers, with different commands. Review the diff of what would change, not the playbook's intent.

```bash
ansible-lint site.yml
ansible-playbook site.yml --check --diff --limit staging
```

`--check` predicts changes without making them; `--diff` shows the actual file and template deltas, which is the Ansible equivalent of reading the plan JSON rather than the summary line. Check mode is honest only where modules support it — a `command`/`shell` task without `check_mode` and `changed_when` is a blind spot, and a review should name those tasks explicitly rather than assume they are no-ops.

The acceptance test is idempotence: run the playbook, then run it again. The second run must report zero `changed`. A task that reports changed on every run is either lying about the state it manages or genuinely fighting something else for ownership, and both cases mean the playbook cannot be used to answer "is this host converged?".

## Anti-patterns

**Reviewing plan text instead of plan JSON.** `(30 unchanged attributes hidden)` is where the security group rule you did not approve lives.

**Planning at review time and re-planning at apply time.** You approved one plan and applied another. Apply the saved `-out=tfplan` artefact, and if state moved in between, the apply fails loudly — which is the correct outcome.

**`-auto-approve` with no policy gate.** Auto-approve is fine when a machine has already checked what a human would have. Without that, it is an unreviewed apply with extra steps.

**Routine `-target`.** Legitimate for surgical recovery, and a smell anywhere in a runbook. It applies a subset of the dependency graph, so the resulting state is consistent with no plan anyone reviewed, and the next full plan surfaces the difference at the worst moment.

**Assuming `sensitive` protects state.** It suppresses output. The plaintext is still in state and in the plan file.

**Missing `create_before_destroy` on name-unique resources.** IAM roles, security groups, target groups, and log groups collide with themselves during replacement. Without the lifecycle block the apply fails halfway; with a failed destroy you get a `deposed` object that keeps billing and keeps holding the name.

**Monolithic state.** One state file for the whole estate means every plan locks every team, every apply risks everything, and blast radius is unbounded by construction.

**A gitignored lockfile.** Guarantees that the provider set you reviewed is not the provider set that applies.

**`ignore_changes` to hide drift.** It silences the symptom and leaves the ownership question unanswered. If another system legitimately owns that attribute, say so in a comment and scope the ignore to that attribute; if nothing owns it, fix the config.

**Waving through `resource_drift` on every plan.** Persistent drift means the config is no longer a description of reality, and at that point the plan's blast radius calculation is built on a fiction.

## Reference files

- `references/plan-json.md` — the plan JSON schema field by field and a fuller `jq` cookbook. Read it when you need a query beyond the ones inline above, or when a field's meaning is load-bearing for the verdict.
- `references/policy-as-code.md` — exact invocations for tflint, trivy, checkov, terrascan, Conftest/OPA, Sentinel, and infracost, plus a worked Rego policy denying stateful destroys. Read it when setting up or auditing the automated gate.
