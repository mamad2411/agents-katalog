---
name: complete-cicd-pipeline-for-vm-based-workloads-from-scratch
description: >
  Builds a complete CI/CD pipeline for a VM-based workload from an empty
  repo — source checkout, build, immutable machine-image baking
  (Packer-style AMI, not a container image or a zip), SCA/SAST security
  gates, and a deploy step that's either a blue-green instance-group swap
  or a config-management push (Ansible) to existing long-lived VMs,
  distinct from both container and serverless deploy mechanics. Use when
  the user asks to "build a full CI/CD pipeline for EC2/VM workloads from
  scratch," "bake an AMI in CI and roll it out blue-green," "push
  Ansible-managed config to existing VMs from a pipeline," or "go from an
  empty repo to a VM fleet deployed with a golden image and Auto Scaling
  Group swap."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: cicd-tooling
  maturity: stable
---

# Complete CI/CD Pipeline Deployment for VM-Based Workloads, From Scratch

## Purpose

VM-based deployment splits into two genuinely different mechanical models,
and this skill covers both because a team's choice between them changes
almost everything downstream of the build step: **immutable image
replacement** (bake a golden AMI with Packer, swap an Auto Scaling
Group/instance group to it, blue-green) versus **mutable config push**
(long-lived VMs stay running, and a config-management tool like Ansible
pushes the new application version/config onto them in place). Neither
looks like the Kubernetes variant of this skill (no container image, no
GitOps handoff) or the serverless variant (no zip/layer, no alias-based
traffic shift) — the build artifact here is either a whole bootable
machine image or nothing at all (just new config/binaries pushed onto
existing hosts), and "deploy" means either swapping which image an
instance group boots or running a playbook against a live fleet.

## When to use

- A new VM-based service (EC2 Auto Scaling Group, an on-prem VM pool, or
  equivalent) has no pipeline yet, and the team wants source-to-deployed
  wired up in one pass.
- Deciding between immutable-image (Packer + blue-green ASG swap) and
  mutable-config-push (Ansible against existing VMs) for a given
  workload's change frequency and risk tolerance.
- An existing pipeline manually bakes AMIs or manually runs Ansible by
  hand, and the user wants both paths automated with security gates.
- The user wants to understand exactly how VM-based build/deploy mechanics
  differ from a container/Kubernetes or serverless pipeline — the
  comparison point most useful when a team is deciding which compute model
  a new workload should even target.

## Prerequisites & environment

- A Git host and CI platform already available — examples below use
  GitHub Actions; the same shape applies to
  [jenkins-declarative-pipeline-per-repo](../jenkins-declarative-pipeline-per-repo/SKILL.md).
- **Packer** ≥ 1.10 (or an equivalent image-building tool) installed on the
  CI runner for the immutable-image path, with cloud credentials scoped to
  build and register an image (`ec2:RunInstances`, `ec2:CreateImage`, and
  related — least-privilege, per
  [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md)).
- For the immutable-image path: an existing Auto Scaling Group/instance
  group and load balancer already provisioned — see
  [aws-codepipeline-and-codedeploy](../aws-codepipeline-and-codedeploy/SKILL.md)
  for the blue/green deployment-group mechanics this skill's Phase 5
  builds on.
- For the mutable-config-push path:
  [ansible-playbook-and-role-design](../../../iac-and-automation-tooling/skills/ansible-playbook-and-role-design/SKILL.md)
  already read for playbook/inventory/idempotency mechanics, plus SSH (or
  WinRM) access from the CI runner (or a bastion/runner fleet) to the
  target VMs.
- SAST/SCA tooling chosen per
  [sast-integration](../../../devsecops/skills/sast-integration/SKILL.md)
  and
  [software-composition-analysis-sca](../../../devsecops/skills/software-composition-analysis-sca/SKILL.md).

## Step-by-step guidance

### Phase 1 — Source and trigger scoping

Standard PR/push trigger setup per
[ci-cd-pipeline-design](../../../devops/skills/ci-cd-pipeline-design/SKILL.md).

### Phase 2 — Build the application artifact

Compile/package the application binary or bundle exactly as any pipeline
would (`npm run build`, `mvn package`, `go build`, etc.) — this step alone
looks identical to any other pipeline. What differs is what happens to
that artifact next.

### Phase 3 — SAST and SCA gates, before baking anything

Run static analysis and dependency scanning against the source/build
output **before** either downstream path — baking a full machine image
(Phase 4) is comparatively expensive and slow, so failing fast here avoids
wasting a 10-20 minute image-build cycle on code that wouldn't have
passed anyway:
```yaml
jobs:
  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - run: semgrep ci --config p/owasp-top-ten --baseline-commit "${{ github.event.pull_request.base.sha }}"
  sca:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: aquasecurity/trivy-action@0.24.0
        with: { scan-type: 'fs', severity: 'CRITICAL,HIGH', exit-code: '1', ignore-unfixed: true }
```

### Phase 4a — Immutable path: bake a golden machine image with Packer

```json
// payments-api.pkr.hcl (HCL2, abbreviated)
source "amazon-ebs" "payments_api" {
  ami_name      = "payments-api-{{timestamp}}"
  instance_type = "t3.medium"
  region        = "us-east-1"
  source_ami_filter {
    filters = { name = "al2023-ami-*-x86_64", virtualization-type = "hvm" }
    owners  = ["amazon"]
    most_recent = true
  }
  ssh_username = "ec2-user"
}
build {
  sources = ["source.amazon-ebs.payments_api"]
  provisioner "file" {
    source      = "dist/payments-api.tar.gz"
    destination = "/tmp/payments-api.tar.gz"
  }
  provisioner "shell" {
    script = "scripts/install-and-harden.sh"
  }
}
```
```bash
packer build -var "build_number=${GITHUB_SHA}" payments-api.pkr.hcl
```
`scripts/install-and-harden.sh` installs the built artifact, applies
CIS-aligned OS hardening, and removes build-time tooling — this is the
machine-image analog of a container's multi-stage build
([container-build-and-release](../../../devops/skills/container-build-and-release/SKILL.md))
except the "final stage" is an entire bootable OS image, not a set of
layered filesystem diffs.

### Phase 4b — Mutable path: skip image baking, prepare a config-push payload instead

If the team's chosen model is config-management push rather than
immutable replacement, Phase 4a is skipped entirely and the built artifact
(Phase 2's output) is instead packaged for
[ansible-playbook-and-role-design](../../../iac-and-automation-tooling/skills/ansible-playbook-and-role-design/SKILL.md)
to push directly — e.g. uploaded to an artifact store the playbook's
`fetch`/`unarchive` tasks will pull from, with no machine image produced at
all.

### Phase 5a — Deploy: blue-green instance-group/ASG swap (immutable path)

```bash
aws autoscaling create-launch-template-version \
  --launch-template-name payments-api-lt \
  --source-version 1 \
  --launch-template-data "{\"ImageId\":\"${NEW_AMI_ID}\"}"

aws autoscaling start-instance-refresh \
  --auto-scaling-group-name payments-api-asg \
  --preferences '{"MinHealthyPercentage": 90, "InstanceWarmup": 120}'
```
An **instance refresh** replaces instances gradually behind the existing
load balancer, honoring health checks — this is the VM-fleet analog of
[blue-green-canary-deployments](../../../devops/skills/blue-green-canary-deployments/SKILL.md)'s
Kubernetes Service-selector flip, but operating on EC2 instances inside one
Auto Scaling Group rather than pods behind a Kubernetes Service. For a
harder cutover with an explicit separate "green" ASG and load-balancer
target-group swap (full blue-green, not a rolling instance refresh), the
CodeDeploy EC2 blue/green mechanics in
[aws-codepipeline-and-codedeploy](../aws-codepipeline-and-codedeploy/SKILL.md)
apply directly, with this pipeline's baked AMI (Phase 4a) as the launch
template's image instead of an existing one.

> **Warning — destructive/irreversible step:** an instance refresh or ASG
> swap **terminates** old instances as it progresses. Always set
> `MinHealthyPercentage` high enough that capacity never drops
> dangerously, and confirm the new AMI passes health checks on a small
> batch before letting the refresh proceed to the full fleet — an instance
> refresh has no automatic rollback the way a GitOps `Application` revert
> does; rolling back means starting a *new* instance refresh pointed at
> the previous launch template version.

### Phase 5b — Deploy: Ansible push to existing VMs (mutable path)

```yaml
# deploy.yml
- hosts: payments_api_fleet
  serial: "25%"
  tasks:
    - name: Fetch new build artifact
      ansible.builtin.unarchive:
        src: "https://artifacts.internal.example.com/payments-api/{{ build_sha }}.tar.gz"
        dest: /opt/payments-api
        remote_src: true
    - name: Restart service
      ansible.builtin.systemd:
        name: payments-api
        state: restarted
      register: restart_result
    - name: Health check
      ansible.builtin.uri:
        url: "http://localhost:8080/healthz"
        status_code: 200
      retries: 5
      delay: 3
```
```bash
ansible-playbook -i inventories/prod deploy.yml --extra-vars "build_sha=${GITHUB_SHA}"
```
`serial: "25%"` rolls the change out to a quarter of the fleet at a time —
the config-push analog of a canary percentage, but implemented as batched
SSH-driven task execution across existing long-lived hosts rather than
either a Kubernetes traffic split or an ASG instance replacement. See
[ansible-playbook-and-role-design](../../../iac-and-automation-tooling/skills/ansible-playbook-and-role-design/SKILL.md)
for idempotent task design and dry-run (`--check`) practice before this
runs against production.

### Phase 6 — Verify

Immutable path: `aws autoscaling describe-instance-refreshes` shows
`Successful`, and the target group's healthy-host count matches the ASG's
desired capacity. Mutable path: re-run the playbook's health-check task
against the full inventory, or a separate smoke-test job, to confirm every
batch converged, not just the last one Ansible reported on.

## Best practices

- Decide immutable-image vs. mutable-config-push per workload's actual
  change frequency and blast-radius tolerance, not as a blanket team
  policy — a rarely-changing, security-sensitive fleet often benefits from
  immutable baking (every deployed instance is provably identical to what
  was scanned), while a fast-iterating internal tool may be better served
  by Ansible push (much faster cycle time, no image-build wait).
- For the immutable path, rescan and rebake the base image on a schedule
  even when application code hasn't changed — an AMI baked once and
  reused for months accumulates unpatched OS CVEs exactly like a stale
  container base image, per the equivalent guidance in
  [container-build-and-release](../../../devops/skills/container-build-and-release/SKILL.md).
- For the mutable path, always run `ansible-playbook --check --diff`
  against a subset of the inventory before the real run, and keep
  `serial:` batching conservative enough that a bad playbook run doesn't
  reach the whole fleet before someone notices.
- Tag every baked AMI and every Ansible-pushed artifact with the exact
  commit SHA it came from, so a running VM's version is traceable back to
  the pipeline run that produced it, exactly as
  [container-build-and-release](../../../devops/skills/container-build-and-release/SKILL.md)
  recommends for image tags.
- Never bake secrets into the AMI itself (Packer provisioner scripts that
  echo/write credentials persist in the resulting image's filesystem) —
  fetch runtime secrets from a secrets manager at boot time instead, per
  [secrets-management](../../../devsecops/skills/secrets-management/SKILL.md).

## Common pitfalls

- **Symptom:** An instance refresh is started against production with a
  bad AMI, and by the time anyone notices, most of the fleet has already
  been replaced and is failing health checks.
  **Fix:** This is the destructive-step warning in Phase 5a in practice —
  set `MinHealthyPercentage` conservatively and watch the refresh's
  progress on the first batch before it proceeds; if it's already
  underway and failing, `aws autoscaling cancel-instance-refresh` halts
  further replacement, and a second instance refresh targeting the prior
  launch template version is the rollback path (there is no automatic
  revert).

- **Symptom:** An Ansible `deploy.yml` run against `serial: "100%"` (the
  whole fleet at once) fails partway through, leaving half the fleet on
  the new version and half on the old, with no clear record of which
  hosts got which.
  **Fix:** Use a conservative `serial:` batch size (e.g. `25%`) so a
  failure is caught and can be halted (`ansible-playbook` stops the play
  on a batch's failure by default) before it reaches the rest of the
  fleet, and query `ansible -i inventories/prod payments_api_fleet -m
  shell -a "cat /opt/payments-api/VERSION"` afterward to get an explicit
  per-host version inventory rather than assuming uniformity.

- **Symptom:** The team assumes "we bake an AMI" means secrets can be
  safely embedded during the Packer build "since it's a private image,"
  and a database password ends up recoverable from a launched instance's
  root filesystem or an old, still-registered AMI snapshot.
  **Fix:** Treat a baked AMI exactly like a container image for secrets
  purposes — nothing written during the build should be assumed private
  once the image is registered and shared/copied across accounts/regions;
  fetch secrets at boot via a secrets manager instead of Packer
  provisioning them in.

- **Symptom:** SAST/SCA gates (Phase 3) are placed *after* the Packer bake
  (Phase 4a) "since the image build takes longer anyway," and a failing
  gate is only discovered after a 15-minute AMI build already completed.
  **Fix:** Order gates before the expensive image-bake step, not after —
  identical sequencing lesson to the Kubernetes and serverless variants of
  this skill, just more costly here because rebuilding a machine image is
  slower than rebuilding a container layer or a zip.

## Worked example

**Scenario:** `payments-api` runs on an EC2 Auto Scaling Group behind an
ALB. The team chooses the immutable-image path: PR-time SAST/SCA, a
Packer-baked AMI on merge to `main`, and a gradual instance refresh with a
conservative health threshold.

```yaml
name: ci-cd
on:
  pull_request: { branches: [main] }
  push: { branches: [main] }

jobs:
  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - run: semgrep ci --config p/owasp-top-ten --baseline-commit "${{ github.event.pull_request.base.sha }}"

  sca:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: aquasecurity/trivy-action@0.24.0
        with: { scan-type: 'fs', severity: 'CRITICAL,HIGH', exit-code: '1' }

  build:
    needs: [sast, sca]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: make build   # produces dist/payments-api.tar.gz

  bake-and-deploy:
    needs: build
    if: github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-packer@v3
      - run: packer build -var "build_number=${{ github.sha }}" payments-api.pkr.hcl
      - run: |
          NEW_AMI_ID=$(cat manifest.json | jq -r '.builds[-1].artifact_id' | cut -d: -f2)
          aws autoscaling create-launch-template-version \
            --launch-template-name payments-api-lt --source-version 1 \
            --launch-template-data "{\"ImageId\":\"$NEW_AMI_ID\"}"
          aws autoscaling start-instance-refresh \
            --auto-scaling-group-name payments-api-asg \
            --preferences '{"MinHealthyPercentage": 90, "InstanceWarmup": 120}'
```
`aws autoscaling describe-instance-refreshes --auto-scaling-group-name
payments-api-asg` is polled (or alerted on) until `Status: Successful`,
confirming every instance in the ASG is now running the new AMI — with
`MinHealthyPercentage: 90` ensuring the ALB always has enough healthy
capacity behind it during the swap.

## Cross-references

- [aws-codepipeline-and-codedeploy](../aws-codepipeline-and-codedeploy/SKILL.md) — CodeDeploy's blue/green EC2 deployment-group mechanics, an alternative to the instance-refresh approach shown in Phase 5a.
- [ansible-playbook-and-role-design](../../../iac-and-automation-tooling/skills/ansible-playbook-and-role-design/SKILL.md) — playbook/inventory/idempotency mechanics used in Phase 5b.
- [sast-integration](../../../devsecops/skills/sast-integration/SKILL.md) and [software-composition-analysis-sca](../../../devsecops/skills/software-composition-analysis-sca/SKILL.md) — Phase 3's scan mechanics.
- [container-build-and-release](../../../devops/skills/container-build-and-release/SKILL.md) — the container-image analog of Phase 4a's immutable-artifact discipline (tagging, rebuild cadence, no baked secrets).
- [blue-green-canary-deployments](../../../devops/skills/blue-green-canary-deployments/SKILL.md) — the vendor-neutral progressive-delivery concepts Phase 5a's instance refresh implements for a VM fleet.
- [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md) — least-privilege scoping for the CI role that bakes images and triggers instance refreshes.
- [complete-cicd-pipeline-deployment-for-kubernetes-from-scratch](../complete-cicd-pipeline-deployment-for-kubernetes-from-scratch/SKILL.md) and [complete-cicd-pipeline-deployment-for-serverless-from-scratch](../complete-cicd-pipeline-deployment-for-serverless-from-scratch/SKILL.md) — the same source-to-deploy shape for a fundamentally different build artifact and deploy mechanism.
