---
name: cloud-resource-post-provisioning-validation-and-drift-detection
description: >
  Verifies what actually got provisioned in AWS/Azure/GCP matches
  declared intent, via terraform plan drift checks, AWS Config
  conformance packs, and Azure Policy compliance scans, plus tag/policy
  compliance checks against a resource baseline. Use when a user asks to
  "check for drift," "verify this deployment matches the Terraform
  state," "run a compliance scan on this account," "why does the console
  show something Terraform doesn't know about," "audit whether tags are
  being enforced," or "confirm what actually got provisioned after that
  change." Complements aws-codepipeline-and-codedeploy/deploy-time
  validation by checking provisioned infrastructure after the fact, on a
  recurring basis, not just at deploy time.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: cloud
  maturity: stable
---

# Cloud Resource Post-Provisioning Validation and Drift Detection

## Purpose

Infrastructure-as-code declares intent, but the running cloud account is
the only source of truth for what's actually there — and the two diverge
constantly: a console click-fix during an incident that never made it
back into Terraform, a policy exemption granted temporarily and
forgotten, a resource created by an entirely separate pipeline or a
different team that the "official" IaC state doesn't know about. Left
unchecked, this drift compounds until nobody can say with confidence
what a `terraform apply` will actually change, whether tag/policy
guardrails from the landing zone are still being enforced, or whether a
resource flagged in a security review was ever actually remediated. This
skill covers detecting that divergence — via `terraform plan` drift
detection, AWS Config conformance packs, Azure Policy compliance scans,
and tag/policy checks against a declared baseline — as a recurring
operational practice, distinct from validating a deploy's *success* at
deploy time (covered in the CI/CD-specific skills) and distinct from
*designing* the guardrails being checked against (covered in the
landing-zone skills).

## When to use

- Confirming that infrastructure provisioned by a recent change (a
  Terraform apply, a manual console change, an incident hotfix) matches
  what was actually intended/declared.
- Running a scheduled or ad hoc drift check to catch out-of-band console
  changes before they cause a surprising `terraform apply` diff later.
- Auditing tag/label compliance against the organization's tagging
  policy (see [cloud-cost-finops-optimization](../cloud-cost-finops-optimization/SKILL.md))
  or Azure Policy/AWS Config/GCP Organization Policy compliance.
- Investigating "why does the console show a resource/setting Terraform
  doesn't know about" or "why did `terraform plan` show unexpected
  changes on an otherwise-untouched module."
- Preparing evidence for a compliance/security review that guardrails
  (encryption-at-rest, public-access blocks, required tags) are actually
  enforced across the account/subscription, not just declared in policy
  documents.
- Validating, after a landing-zone or IAM-hardening change, that the new
  guardrail is actually taking effect on real resources.

## Prerequisites & environment

- Terraform ≥ 1.5 (state `refresh`/`plan -refresh-only` behavior is
  stable from 1.x but confirm the exact drift-detection UX — `plan
  -refresh-only` was introduced in 1.1) with read access to the state
  backend and the cloud provider's read-only API scope at minimum.
- AWS Config enabled with a recorder covering the resource types in
  scope, plus either AWS-managed conformance packs or custom Config
  rules for the specific guardrails being checked (tag policies,
  encryption requirements, public-access blocks).
- Azure Policy assigned at the Management Group/subscription scope with
  the relevant built-in or custom policy definitions (tagging, allowed
  locations, required diagnostic settings) in an audit or deny effect.
- GCP equivalent: Organization Policy constraints plus Security Command
  Center's Security Health Analytics / Policy Controller (if using
  Anthos Config Management/GKE), or a scheduled `gcloud asset
  search-all-resources` inventory diffed against declared IaC.
- A declared baseline to check against: Terraform state/config as the
  primary source for IaC-managed resources, plus an explicit,
  version-controlled tag/policy taxonomy (not tribal knowledge) for
  compliance checks — see
  [cloud-cost-finops-optimization](../cloud-cost-finops-optimization/SKILL.md)
  and the landing-zone skills for where that taxonomy is typically
  defined.
- Read-only credentials are sufficient for detection; do not grant
  drift-detection tooling write/remediation permissions by default (see
  Best practices).

## Step-by-step guidance

1. **Run `terraform plan` in refresh-only mode to detect drift without
   risking an unintended apply.** This updates state to reflect real
   infrastructure and shows the diff, without proposing to change
   anything:
   ```bash
   terraform plan -refresh-only -out=drift.tfplan
   terraform show -json drift.tfplan | jq '.resource_changes[] | select(.change.actions != ["no-op"])'
   ```
   Any non-empty output is drift: a resource's real-world state differs
   from what Terraform's state file last recorded. Distinguish this from
   a normal `terraform plan` (no `-refresh-only`), which also shows
   *config* changes not yet applied — refresh-only isolates just the
   "reality moved without us" signal.

2. **Classify each drifted resource before deciding what to do.**
   - **Expected/benign drift**: a cloud-managed attribute that changes on
     its own (e.g. an AMI's `most_recent` resolution, an auto-assigned
     ID) — usually safe to accept into state via `terraform apply
     -refresh-only` after review, or exclude via `lifecycle {
     ignore_changes }` if it recurs.
   - **Out-of-band manual change**: someone changed a setting via
     console/CLI directly (e.g. widened a security group rule during an
     incident, changed an instance type by hand). Decide explicitly:
     revert to match IaC (if the manual change wasn't supposed to be
     permanent) or import the new reality into Terraform config (if it
     should be the new intent) — never leave it drifted indefinitely,
     since every subsequent `plan` will keep surfacing it as noise.
   - **Unmanaged/unknown resource**: a resource visible in the account
     but not represented in any Terraform state at all. This needs
     separate discovery (step 4), since `terraform plan` only reports
     drift on resources it already knows about.

3. **Run AWS Config / Azure Policy / GCP Organization Policy compliance
   scans for guardrail-level checks that `terraform plan` won't catch**
   (things that are compliant/non-compliant regardless of which tool
   created the resource):
   ```bash
   # AWS: check compliance status of a specific Config rule across the account
   aws configservice get-compliance-details-by-config-rule \
     --config-rule-name required-tags \
     --compliance-types NON_COMPLIANT
   ```
   ```bash
   # AWS: evaluate an entire conformance pack on demand rather than waiting for the next periodic scan
   aws configservice start-config-rules-evaluation --config-rule-names required-tags encrypted-volumes
   ```
   ```bash
   # Azure: list non-compliant resources for a specific policy assignment
   az policy state list \
     --filter "complianceState eq 'NonCompliant' and policyAssignmentId eq '<POLICY_ASSIGNMENT_ID>'" \
     --query "[].{Resource:resourceId, Policy:policyDefinitionName}"
   ```
   ```bash
   # GCP: list resources violating an Organization Policy constraint, via Security Command Center findings
   gcloud scc findings list <ORGANIZATION_ID> \
     --source=<SECURITY_HEALTH_ANALYTICS_SOURCE_ID> \
     --filter="category=\"MFA_NOT_ENFORCED\" OR category=\"PUBLIC_BUCKET_ACL\""
   ```
   These checks catch resources created entirely outside Terraform (a
   console-created S3 bucket, a manually spun-up VM) that a Terraform-
   only drift check would never see, since Config/Policy/SCC evaluate
   every resource in scope regardless of how it was created.

4. **Reconcile the full resource inventory against IaC state to find
   unmanaged resources**, not just drifted ones:
   ```bash
   # AWS: list all resources of a type, compare resource IDs against terraform state
   aws resourcegroupstaggingapi get-resources --resource-type-filters ec2:instance \
     --query "ResourceTagMappingList[].ResourceARN" > all-instances.json
   terraform state list | grep aws_instance # then diff resource IDs by hand or with a small script
   ```
   ```bash
   # GCP: full asset inventory, diffable against declared Terraform-managed resources
   gcloud asset search-all-resources --scope=projects/<PROJECT_ID> --asset-types=compute.googleapis.com/Instance
   ```
   A resource present in the inventory but absent from Terraform state
   is either legitimately unmanaged (a one-off sandbox resource, fine as
   long as it's tagged and low-risk) or a governance gap (something that
   should have gone through IaC and didn't) — flag for the owning team
   to confirm which, don't assume.

5. **Check tag/label compliance against the declared taxonomy**
   specifically, since tag drift is usually the highest-volume, lowest-
   individual-severity finding and benefits from a dedicated query rather
   than being buried in general compliance output:
   ```bash
   aws resourcegroupstaggingapi get-resources \
     --tags-per-page 100 \
     --query "ResourceTagMappingList[?!contains(Tags[].Key, 'cost-center')].ResourceARN"
   ```
   ```bash
   az resource list --query "[?tags.\"cost-center\" == null].{Name:name, Type:type, ResourceGroup:resourceGroup}"
   ```
   Feed missing-tag findings back into
   [cloud-cost-finops-optimization](../cloud-cost-finops-optimization/SKILL.md)'s
   tag-backfill process rather than treating tag drift as a one-off
   cleanup.

6. **Automate drift/compliance checks as a scheduled recurring job**
   (nightly or per-merge for `terraform plan -refresh-only` in CI;
   Config/Policy scans typically run on their own periodic schedule but
   confirm the evaluation frequency matches the risk tolerance — some
   Config rules default to 24-hour periodic evaluation, which may be too
   slow for a Tier 0 guardrail). Route findings to a dashboard or ticket
   queue, not just a log nobody reads.

7. **Decide remediation deliberately, and prefer proposing rather than
   auto-applying** for anything beyond the most routine, pre-approved
   drift categories:
   > **Warning:** Auto-remediating drift (an automatic `terraform apply`
   > to force reality back to declared state, or an AWS Config
   > auto-remediation action) can be as disruptive as an unreviewed
   > manual change if the drifted state was actually a deliberate,
   > undocumented fix (e.g. a security-group rule widened during an
   > active incident, a manually scaled-up instance count keeping a
   > degraded service afloat). Default to alerting a human with the diff
   > and requiring explicit confirmation before applying any
   > corrective change to production resources; reserve auto-
   > remediation for narrowly scoped, well-understood, low-risk drift
   > categories (e.g. re-tagging) with a proven track record of safety.

8. **Track drift/compliance trend over time, not just point-in-time
   snapshots** — a recurring scan that shows the same category of drift
   reappearing every cycle (e.g. the same security group repeatedly
   drifting wider) is a signal to fix the underlying process (who has
   console write access, why the IaC pipeline isn't the only path to
   change) rather than just reverting the symptom each time.

## Best practices

- **Grant drift-detection tooling read-only access by default** —
  detection and remediation are different risk levels; a scan that can
  only observe cannot itself cause an incident, and remediation should be
  a deliberate, separately authorized action per step 7.
- **Use `terraform plan -refresh-only` for drift specifically**, not a
  regular `plan`, when the goal is "did reality diverge from last-known
  state" rather than "what would applying pending config changes do" —
  conflating the two makes it hard to tell whether a diff is drift or
  an unapplied intentional change.
- **Treat unmanaged resources (in inventory, absent from IaC state) as
  their own finding category**, separate from drift on already-managed
  resources — the fix for each is different (import into IaC vs. revert
  a manual change vs. accept as legitimately out-of-scope).
- **Scope Config rules/Policy assignments to the guardrails that
  actually matter for the workload's risk tier**, mirroring the tiering
  approach in
  [disaster-recovery-and-backup-strategy](../disaster-recovery-and-backup-strategy/SKILL.md) —
  not every account needs every possible conformance pack rule active at
  the strictest setting.
- **Feed tag-compliance findings into the FinOps tagging backfill
  process** rather than treating them as a separate, one-off cleanup —
  see [cloud-cost-finops-optimization](../cloud-cost-finops-optimization/SKILL.md).
- **Prefer importing a deliberate manual change into IaC over reverting
  it blind**, when the manual change turns out to have been the right
  call — drift detection's job is to surface the divergence and force a
  decision, not to always mean "revert."
- **Version and review Config rules/Policy definitions themselves in
  Git**, the same as the IaC they check — a compliance guardrail that
  only exists as console configuration is itself a form of drift risk.

## Common pitfalls

- **Symptom:** `terraform plan` shows unexpected changes on a resource
  nobody touched in the Terraform config, and the team assumes it's a
  provider bug.
  **Fix:** This is almost always drift from an out-of-band change (a
  console edit, a separate automation, an AWS-side attribute
  auto-updating). Run `terraform plan -refresh-only` first to isolate
  drift from pending config changes, and check CloudTrail/Activity
  Log/Cloud Audit Logs for the resource ID over the relevant window to
  identify who or what made the out-of-band change before assuming
  tooling is at fault.

- **Symptom:** A drift-detection job auto-applies `terraform apply` to
  "fix" drift on a production resource, and it turns out the drift was a
  deliberate manual mitigation an on-call engineer made during an active
  incident, which the auto-apply just reverted mid-incident.
  **Fix:** **Never auto-remediate drift on production resources without
  a human-reviewed confirmation step** — this can undo a legitimate,
  time-sensitive fix. Default drift detection to alert-and-propose, and
  reserve automatic correction for narrowly scoped, pre-approved,
  low-risk categories only (see step 7's warning).

- **Symptom:** An AWS Config conformance pack shows 100% compliance, but
  a manual review finds several non-compliant resources that were
  created after the last scheduled evaluation.
  **Fix:** Config rules have an evaluation frequency (often 24 hours by
  default for periodic rules), and compliance status reflects the last
  evaluation, not real time. For Tier 0 guardrails, trigger evaluation
  on-demand after significant changes
  (`start-config-rules-evaluation`) or switch to change-triggered
  evaluation where the rule type supports it, rather than relying solely
  on the periodic schedule.

- **Symptom:** A resource shows up in the cloud console and in the
  billing export, but nobody can find it in any Terraform state file
  across any of the team's repositories, and it's unclear whether it's
  safe to just leave alone.
  **Fix:** This is an unmanaged resource, not drift — `terraform plan`
  will never surface it since it isn't in state to begin with. Run the
  full inventory reconciliation (step 4) on a recurring basis, not just
  ad hoc when someone happens to notice, and require every unmanaged
  resource to be explicitly classified (import into IaC, confirmed
  legitimate one-off, or a candidate for
  [orphaned-cloud-resource-cleanup](../orphaned-cloud-resource-cleanup/SKILL.md)
  if it also looks unused).

- **Symptom:** Tag-compliance scans keep flagging the same handful of
  resources every cycle, and the finding gets silently ignored because
  it's become routine noise.
  **Fix:** A repeatedly-ignored recurring finding is worse than no
  finding at all — it trains reviewers to skip real issues. Either fix
  the resource (backfill the tag) or, if there's a legitimate reason it
  can never be tagged that way, add an explicit, documented policy
  exemption with an owner and expiry rather than letting it recur as
  unresolved noise indefinitely.

## Worked example

**Scenario:** A quarterly infrastructure audit is scheduled for the
`payments-prod` AWS account ahead of a compliance review, to confirm
provisioned resources match Terraform-declared intent and required
guardrails (encryption, tagging, no public S3 buckets) are actually
enforced.

1. Run `terraform plan -refresh-only` across all `payments-prod`-scoped
   Terraform workspaces (step 1): the diff shows one drifted resource —
   a security group's ingress rule now allows `0.0.0.0/0` on port 22,
   where the declared config specifies a restricted CIDR.
2. Classify the drift (step 2): CloudTrail shows the rule was widened
   manually three weeks ago by an on-call engineer during an incident
   requiring emergency SSH access, and never reverted afterward.
   Decision: revert to the declared restricted CIDR via the normal
   Terraform pipeline (not a manual console fix), since the incident
   that justified the temporary widening closed two weeks ago.
3. Run the AWS Config conformance pack for encryption and public-access
   guardrails (step 3):
   `get-compliance-details-by-config-rule --config-rule-name
   s3-bucket-public-read-prohibited --compliance-types NON_COMPLIANT`
   returns zero results (compliant); a separate rule for
   `encrypted-volumes` flags two EBS volumes without encryption enabled.
4. Reconcile the full EC2 inventory against Terraform state (step 4):
   one EC2 instance appears in `resourcegroupstaggingapi get-resources`
   output with no matching entry in any known Terraform state — traced
   via CloudTrail to a one-off instance launched directly via console
   for a proof-of-concept two months ago and never imported into IaC or
   decommissioned.
5. Run the tag-compliance check (step 5): 8 resources across the account
   are missing the required `cost-center` tag, overlapping partly with
   the untagged instance from step 4.
6. Findings routed for remediation, not auto-applied: security group
   revert scheduled through the normal PR/apply pipeline; the two
   unencrypted volumes flagged to their owning team with a remediation
   ticket (encryption-at-rest can't be enabled in-place on an existing
   AWS EBS volume, so the fix is a snapshot-and-recreate scheduled during
   a maintenance window); the unmanaged POC instance confirmed with its
   creator as safe to decommission and handed to
   [orphaned-cloud-resource-cleanup](../orphaned-cloud-resource-cleanup/SKILL.md);
   the 8 untagged resources backfilled per
   [cloud-cost-finops-optimization](../cloud-cost-finops-optimization/SKILL.md).
7. Because this account has now had two consecutive quarters of manual
   security-group drift from incident response, recommend adding a
   scheduled, change-triggered Config rule evaluation plus a follow-up
   process requiring incident-related manual changes to be tracked in a
   ticket with an explicit revert date, rather than relying on the next
   quarterly audit to catch it.

## Cross-references

- [aws-landing-zone-setup](../aws-landing-zone-setup/SKILL.md) — the
  OU-level SCPs and Config/CloudTrail baseline this skill's compliance
  scans check against.
- [cloud-iam-hardening](../cloud-iam-hardening/SKILL.md) — scope
  drift-detection tooling to read-only access; treat any finding of
  broader-than-expected IAM permissions surfaced during a scan per that
  skill's guidance.
- [cloud-cost-finops-optimization](../cloud-cost-finops-optimization/SKILL.md) —
  where tag-compliance findings from this skill's step 5 get backfilled
  and where the tagging taxonomy itself is defined.
- [orphaned-cloud-resource-cleanup](../orphaned-cloud-resource-cleanup/SKILL.md) —
  hand off an unmanaged resource discovered during inventory
  reconciliation here if it also looks unused, rather than deleting it
  as part of a drift-remediation pass.
