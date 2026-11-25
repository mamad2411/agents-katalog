---
name: terraform-review
description: "Reviews a Terraform plan for what scanners cannot judge: blast radius, destructive replacement, orphaned state. Use when reviewing a Terraform merge request or a plan before apply. Not for lint or security rules (use code-review-core:review) or authoring conventions (use terraform-standards)."
license: MIT
---

# Reviewing a Terraform Change

`code-review-core`'s `terraform` detector already runs `terraform fmt`, `tflint` (including its
default Terraform ruleset) and `checkov`/`tfsec` on every change. Skip formatting, deprecated
syntax, missing constraints and known-bad resource settings; restating them trains authors to
skim. This skill covers the three questions no scanner can answer:

1. **What is the blast radius if this is wrong?**
2. **Is anything destroyed and rebuilt, and can it survive that?**
3. **Does state end up matching reality?**

## Get the plan

Review the **plan**, not the diff. A three-line diff can destroy a database; a two-hundred-line
refactor can be a no-op. Ask for the plan from the pipeline job for the environment being
changed; when a change goes to several environments, the production plan is the one that
matters.

Accepted inputs, best first:

- `terraform show -json tfplan` output. Read `resource_changes[].change.actions`
  (`["delete","create"]` is destroy-then-create, `["create","delete"]` is create-before-destroy)
  and `resource_changes[].change.replace_paths` (the attributes forcing replacement).
- The human-readable plan pasted from the job log.
- On web or without credentials: whatever of the above the user pastes. Do not run `plan`
  yourself against a shared environment; if there is no plan, ask for it rather than reviewing
  the diff alone.

A saved plan file and its JSON rendering contain sensitive values in plaintext. Ask for the
relevant excerpt rather than the whole file when secrets could be in it, and never commit or
attach a plan file to a merge request.

## Reading the plan

| Symbol | Meaning | Reviewer's reaction |
| --- | --- | --- |
| `+` | create | Check it does not duplicate something that already exists outside Terraform. |
| `~` | update in place | Read which attribute changed. |
| `-/+` | **destroy then create** | The main event — see below. |
| `+/-` | create then destroy (`create_before_destroy`) | Safer ordering, but a new id, endpoint and ARN. Hardcoded references to the old one break. |
| `-` | destroy, no replacement | Intentional removal, or something fell out of the configuration? |
| `# forces replacement` | the attribute that caused `-/+` | Find every one. |
| `(known after apply)` on an attribute others depend on | a cascade | Downstream resources may replace too. |

Start at the summary line (`Plan: 3 to add, 1 to change, 2 to destroy`), then read the body.

### The replacement question

For every `-/+`, answer: **what is lost between the destroy and the create?**

| Resource class | What replacement costs |
| --- | --- |
| Stateless compute, a function version, a task definition | Usually nothing. |
| A database instance or cluster | **The data**, unless restored from a final snapshot — a different resource with a different endpoint. Never a routine approval. |
| An RDS engine upgrade or parameter change shown as `~` | Not a replacement, but an in-place modify can still mean downtime. For MySQL, MariaDB and PostgreSQL instances without replicas (backups on), `blue_green_update { enabled = true }` makes the provider run an RDS Blue/Green deployment and switch over. Check `apply_immediately` too: `false` defers the change to the maintenance window, so the apply "succeeds" and the outage happens later. |
| A storage bucket or container registry | The contents if `force_destroy` is set; if not, the destroy fails and leaves a partially applied change. |
| Anything with a cached DNS name or endpoint | An outage for as long as propagation takes. |
| A security group or subnet with dependents | Cascading replacement of everything attached. |
| An IAM role | Every live session, and any external trust policy naming it by ARN. |
| A KMS key | Data encrypted under it, if it is really scheduled for deletion. |

Common unintended replacement triggers: a changed `name`/`name_prefix`, availability zone or
subnet, a changed `count`/`for_each` key, and a provider upgrade that made an attribute
force-new. The `# forces replacement` marker (or `replace_paths`) names the attribute; trust it
over your memory of which attributes are force-new.

Guardrails to look for: `lifecycle { prevent_destroy = true }` on unrecoverable resources,
`deletion_protection = true` where the provider offers it, and `skip_final_snapshot = false`
on anything holding data. Know their limits:

- `prevent_destroy` makes a plan that would destroy the resource — including a `-/+` — fail
  with an error. It is not a finding to "work around" by removing it in the same change.
- `prevent_destroy` lives in the resource block. Delete the block (or the module call around
  it) and the guard goes with it, and the plan shows a plain destroy. `deletion_protection`
  is enforced by AWS and survives that; prefer it where it exists.
- A change that removes any of these guardrails is the change under review, whatever else
  is in the diff.

### Count and for_each index shifts

`count` over a list addresses by position: remove the second element and every later instance
shifts index and is replaced. `for_each` over a map addresses by key; prefer it. Converting
`count` to `for_each` re-addresses every instance, so it must arrive with `moved` blocks in the
same change and a plan showing zero replacements.

## State orphaning

State and reality disagree, and nothing errors.

| Situation | What happens | What the change should contain |
| --- | --- | --- |
| A resource or module is **renamed** | destroy + create | A `moved` block from old to new address, and a plan showing no changes for it |
| A resource is **deleted from config** but must keep existing | destroyed | A `removed` block naming the old address, with `lifecycle { destroy = false }` (see below) |
| A resource exists in the cloud but not in state | create fails on a name conflict, or creates a duplicate | An `import` block, reviewed against the real resource's id |
| Someone ran `terraform state rm` | the resource is live and unmanaged | Nothing in the change; ask what problem it solved and replace it with a `removed` block |
| A resource **moves between root modules** | one state destroys it, the other creates it, in whatever order the pipelines run | Sequenced: `import` into the new state first, then `removed` with `destroy = false` from the old |
| The apply was **`-target`ed** | state is a partial application; the next full plan shows surprises | `-target` in a pipeline is a finding |

```hcl
removed {
  from = aws_s3_bucket.legacy

  lifecycle {
    destroy = false
  }
}
```

Any change to a resource's address deserves the same scrutiny as a change to its arguments.

## Blast radius

- **How many resources, in which environment?** 40 in production is a different review from 2
  in a sandbox.
- **Is it shared?** A VPC, shared subnet, transit attachment, shared key or central logging
  change affects every workload in the account.
- **Who consumes this stack's outputs?** Renaming or removing an output breaks a consumer at
  its next apply, not this one.
- **Is it reversible?** Revert-and-apply restores most things, not deleted data.
- **Has it applied cleanly in a lower environment?** If not, the description should say why.

## Cross-cutting checks

- **Secrets.** A new secret-reading data source puts that secret in state, so it is also a
  question about who can read the state bucket (`dev-standards:secrets-management`).
- **Provider upgrades bundled with resource changes.** Ask to split them; otherwise an
  unexpected replacement has two possible causes.
- **Environment parity.** A change going to one environment only should say why.
- **Tags.** Cost attribution, incident routing, and often what IAM conditions match on.
- **IAM and trust policies** in the change: review them with `aws-iam-boundaries`.

## The approval sentence

Before approving, write one sentence: *"This changes `<what>` in `<environment>`; the
destructive operations are `<list, or none>`; if it is wrong, `<what breaks>` and recovery is
`<how>`."* If the plan cannot support that sentence, ask for what is missing instead of
approving on a clean scan.

End the review with one verdict line, `Verdict: <APPROVE | REQUEST_CHANGES | NEEDS_PLAN>`:

| Verdict | When |
| --- | --- |
| `APPROVE` | The approval sentence is complete and every destructive operation is intended and survivable. |
| `REQUEST_CHANGES` | The plan is trustworthy but the change needs something first: a `moved` block, a guardrail, a safer upgrade path. |
| `NEEDS_PLAN` | There is no plan, it is for the wrong environment, or it cannot be trusted (for example, all creates against an existing environment). |

<example>
Plan (production): `Plan: 0 to add, 1 to change, 0 to destroy`, `~ aws_db_instance.main`,
`engine_version: "15.7" -> "16.4"`, `allow_major_version_upgrade = true`,
`apply_immediately = true`, no `blue_green_update` block.

Review: This changes the primary PostgreSQL instance in production; the destructive operations
are none, but a major in-place upgrade takes the database offline for the upgrade's duration,
starting at apply. If it is wrong, every service on this database is down until the upgrade
completes or the instance is restored from snapshot. Request: add `blue_green_update { enabled = true }`
(the instance has no replicas and backups are on) or schedule a window, and confirm a manual
snapshot is taken first.

Verdict: REQUEST_CHANGES
</example>

<example>
Diff: `aws_s3_bucket.logs` renamed to `aws_s3_bucket.access_logs`. Plan (staging):
`Plan: 1 to add, 0 to change, 1 to destroy`, `- aws_s3_bucket.logs`, `+ aws_s3_bucket.access_logs`.

Review: This changes the access-log bucket in staging; the destructive operation is a destroy of
the existing bucket (it fails if the bucket is not empty and `force_destroy` is unset, leaving
a half-applied change). The rename needs a plan showing no changes for the bucket and this block:

```hcl
moved {
  from = aws_s3_bucket.logs
  to   = aws_s3_bucket.access_logs
}
```

Verdict: REQUEST_CHANGES
</example>

<example>
Plan (dev): `Plan: 214 to add, 0 to change, 0 to destroy` for a stack that has run in dev for
months; the diff only edits one variable default.

Review: Not reviewable as a change. A plan that creates an existing environment means the
backend `key` or `-backend-config` file points at an empty state. Check the init command in the
job log against `backends/dev.s3.tfbackend` before anything is applied.

Verdict: NEEDS_PLAN
</example>

## Verify

Before posting the review:

1. Every `-/+`, `-` and `# forces replacement` in the plan is named in the review, or you
   have stated that there are none.
2. Every renamed or removed address has a matching `moved` or `removed` block, or a finding.
3. The approval sentence is written and every blank in it is filled from the plan.
4. The review ends with exactly one `Verdict:` line from the table above.

If there is no plan (only a diff), return a single finding asking for the plan for the target
environment, with `Verdict: NEEDS_PLAN`.
