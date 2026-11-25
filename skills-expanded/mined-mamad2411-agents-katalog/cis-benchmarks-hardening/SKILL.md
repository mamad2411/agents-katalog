---
name: cis-benchmarks-hardening
description: >
  Guides applying CIS Benchmarks (Kubernetes, Docker/containers, Linux
  distributions, and cloud provider foundations benchmarks for AWS/Azure/
  GCP) using automated scanners such as kube-bench, Docker Bench for
  Security, and CIS-CAT, interpreting PASS/FAIL/WARN findings against the
  actual benchmark text, and running a documented exception/waiver process
  for findings that legitimately do not apply to a given environment. Use
  when a user asks to "run a CIS benchmark scan", "harden this cluster/host
  to CIS standards", "interpret kube-bench output", "fix Docker Bench
  findings", "why did we fail CIS control 5.2.x", or "document an exception
  for a benchmark check we can't remediate". A scan pass is a hardening
  signal, not a certification — it does not itself prove compliance to an
  auditor.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: standards-and-compliance-frameworks
  maturity: stable
---

# CIS Benchmarks Hardening

## Purpose

The Center for Internet Security (CIS) publishes consensus-based, vendor-reviewed
configuration benchmarks (Kubernetes, Docker, Linux distributions such as
Ubuntu/RHEL/Amazon Linux, and cloud foundations benchmarks for AWS/Azure/GCP)
that translate abstract "harden your systems" advice into specific, testable
configuration checks. This skill guides running the right automated scanner
for the target (kube-bench for Kubernetes, Docker Bench for Security for
container hosts, CIS-CAT Pro or `oscap`/OpenSCAP for Linux OS, cloud-native
tools or Prowler/ScoutSuite for cloud foundations benchmarks), reading the
findings against the actual benchmark rationale (not just the pass/fail
label), remediating what should be remediated, and — critically — running a
documented, reviewed exception process for findings that do not apply to a
given environment instead of silently ignoring or globally disabling checks.
A passed scan is evidence of a hardening baseline; it is not by itself proof
of "CIS compliance," since CIS does not issue compliance certifications for
individual organizations — some cloud/SaaS compliance programs (e.g. FedRAMP,
StateRAMP) reference CIS Benchmarks as a required baseline, but the actual
attestation still comes from a separate audit process.

## When to use

- A user asks to "run a CIS benchmark scan against this Kubernetes cluster /
  Docker host / Linux server."
- Interpreting kube-bench, Docker Bench, or CIS-CAT scan output and deciding
  what to fix first.
- A security or compliance team requires "CIS Level 1" or "CIS Level 2"
  hardening evidence for an environment.
- A specific benchmark control fails and the user asks "why did we fail
  control X.Y.Z" or "how do I fix this finding."
- A finding is a false positive or genuinely inapplicable (e.g. a managed
  Kubernetes control plane check that only applies to self-managed
  clusters) and needs a documented, approved waiver rather than silent
  suppression.
- Building a recurring hardening/drift-detection pipeline so benchmark
  scans run on every image build or infrastructure change, not once.

## Prerequisites & environment

- Know which CIS Benchmark and profile level applies: e.g. "CIS Kubernetes
  Benchmark v1.9 (aligned to Kubernetes 1.27+)", "CIS Docker Benchmark
  v1.6", "CIS Distribution Independent Linux Benchmark" or a distro-specific
  one (CIS Ubuntu 22.04 Benchmark, CIS Amazon Linux 2023 Benchmark), or a
  cloud foundations benchmark (CIS AWS Foundations Benchmark v3.0, CIS
  Azure Foundations Benchmark, CIS Google Cloud Platform Foundation
  Benchmark). Benchmark control numbers and text change between versions —
  always confirm which version a scanner ships against and which version
  the organization has committed to.
- Level 1 vs Level 2 profiles: Level 1 recommendations are broadly
  applicable with minimal operational impact; Level 2 is more restrictive
  and intended for higher-security environments where some operational
  friction is accepted. Pick the profile deliberately, do not default to
  scanning both and treating every Level 2 finding as mandatory.
- Tooling, matched to target:
  - **kube-bench** (Aqua Security) for Kubernetes control-plane and
    worker-node checks — run as a Job/DaemonSet inside the cluster or as a
    standalone binary on each node. Note that managed Kubernetes (EKS,
    AKS, GKE) hides or manages the control-plane node, so most
    control-plane checks in the benchmark's "master node" section are
    the cloud provider's responsibility, not yours — this is one of the
    most common sources of "false fail."
  - **Docker Bench for Security** for Docker Engine hosts — shell script
    that inspects the daemon config, running containers, and host files.
  - **CIS-CAT Pro** or **OpenSCAP (`oscap`)** with a CIS SCAP profile for
    Linux OS-level benchmarks.
  - **Prowler**, **ScoutSuite**, or a CSPM tool for cloud foundations
    benchmarks (these overlap heavily with
    [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md)
    and the landing-zone skills).
  - Cluster/host access sufficient to read the relevant config files
    (kubelet config, `/etc/docker/daemon.json`, systemd unit files, etc.)
    — most checks are read-only inspection, not exploitation.
- An exception/waiver tracking mechanism — a spreadsheet is a starting
  point, but a ticket system or a version-controlled YAML/JSON waiver file
  reviewed in pull requests is far more defensible in an audit.

## Step-by-step guidance

1. **Confirm scope and benchmark version.** Identify the target (cluster,
   node image, host fleet), the applicable CIS Benchmark and version, and
   the target profile (Level 1 or Level 2). Record this decision — it is
   the baseline against which every future scan is compared.
2. **Run the automated scan.**
   - Kubernetes, as a Job using the upstream kube-bench image against a
     cluster node:
     ```bash
     kubectl run kube-bench --rm -it --restart=Never \
       --image=docker.io/aquasec/kube-bench:v0.9.3 \
       --overrides='{"spec":{"hostPID":true,"nodeSelector":{"kubernetes.io/os":"linux"}}}' \
       -- --benchmark cis-1.24 --json > kube-bench-results.json
     ```
   - Docker host:
     ```bash
     docker run --rm --net host --pid host --userns host --cap-add audit_control \
       -v /etc:/etc:ro -v /usr/bin/containerd:/usr/bin/containerd:ro \
       -v /usr/bin/runc:/usr/bin/runc:ro -v /usr/lib/systemd:/usr/lib/systemd:ro \
       -v /var/lib:/var/lib:ro -v /var/run/docker.sock:/var/run/docker.sock:ro \
       --label docker_bench_security \
       docker/docker-bench-security
     ```
3. **Read the raw output, not just the summary counts.** A `[WARN]` in
   kube-bench often means "requires manual verification" — the tool
   cannot automatically inspect the value and is telling the operator to
   check it, not that it failed. Treat `WARN` as "needs a decision," `FAIL`
   as "needs remediation or an approved exception," and `PASS` as
   confirmed-compliant-with-that-check only.
4. **Triage each FAIL/WARN against the benchmark's own rationale text**,
   not just the one-line check description — the full CIS Benchmark PDF/
   spreadsheet gives the "Rationale," "Audit," "Remediation," and "Impact"
   for each control, which is what determines whether the fix is safe to
   apply automatically.
5. **Remediate what applies.** Common remediations: set kubelet
   `--anonymous-auth=false`, restrict `--protect-kernel-defaults=true`,
   disable Docker legacy registry/`--insecure-registry` flags, set
   `docker.sock` permissions to non-world-writable, enable auditd rules
   for Linux host benchmarks. Where remediation overlaps container image
   configuration (non-root user, read-only rootfs, dropped capabilities),
   apply it via
   [container-image-hardening](../../../devsecops/skills/container-image-hardening/SKILL.md)
   rather than re-deriving it here.
6. **For findings that do not apply, open a documented exception** — not
   a silent skip. Minimum fields: control ID and title, why it does not
   apply (e.g. "control-plane managed by cloud provider — verified in
   provider's shared-responsibility matrix"), compensating control if any,
   approver, and a review/expiry date. Store this as version-controlled
   data (e.g. a `waivers.yaml` next to the scan config) so it is itself
   auditable.
7. **Re-run the scan and diff against the previous run** to confirm the
   remediated findings now pass and no new regressions appeared.
8. **Wire the scan into CI/CD or a scheduled job** so hardening is
   continuously verified rather than a point-in-time exercise — a scan run
   once during onboarding tells you nothing about the state six months
   later after configuration drift.
9. **Produce a scored summary** (see Worked example) for the person who
   asked for "CIS hardening evidence" — pass count, fail count with
   severity, exceptions with justification and expiry, and the benchmark
   version/profile used.

## Best practices

- Scan against the profile level you have actually decided to target
  (Level 1 vs Level 2) — reporting Level 2 failures as if they were
  required Level 1 gaps overstates risk and burns remediation effort on
  lower-priority items.
- Pin the scanner and benchmark version in CI (e.g. `kube-bench:v0.9.3`
  with `--benchmark cis-1.24`) so results are reproducible; an upgraded
  scanner can silently change which controls run.
- Treat kube-bench/Docker Bench findings on managed cloud services (EKS,
  AKS, GKE, ECS) with skepticism for anything under the provider's
  shared-responsibility boundary — verify against the provider's own
  compliance documentation before spending remediation effort on
  something you cannot change.
- Automate remediation only for checks with a clearly safe, idempotent
  fix (e.g. a kubelet flag, a file permission) — checks whose remediation
  could break running workloads (e.g. tightening `NetworkPolicy` defaults,
  disabling a needed Docker feature) need a change-managed rollout, not an
  auto-apply script.
- Keep the waiver file next to the scan configuration in version control
  and require peer review on any waiver change — this is what makes the
  exception process defensible when an auditor or new team member asks
  "why is this failing check tolerated."
- Re-run scans on every base image update and on a recurring schedule
  (e.g. nightly or on each cluster upgrade) — CIS Benchmark versions
  themselves are periodically revised as new Kubernetes/Docker/OS versions
  ship, so "we scanned it once" ages out.
- Cross-check overlapping findings instead of fixing the same class of
  issue twice — a kube-bench "containers should not run as root" finding
  and a container-image-hardening non-root-user recommendation are the
  same underlying control; fix it once at the image/PodSecurity level.

## Common pitfalls

- **Symptom:** Team reports "we passed our CIS scan" and treats hardening
  as complete, with no record of what was skipped.
  **Fix:** A pass count alone is meaningless without knowing the profile
  level scanned and reviewing every WARN/FAIL and every exception. Require
  the summary report (pass/fail/warn/exception counts, benchmark version,
  profile level, exception list with expiry) as the actual deliverable,
  not just "green" in a dashboard.
- **Symptom:** kube-bench reports dozens of FAILs on a managed EKS/AKS/GKE
  cluster's control-plane checks, and the team spends days trying to
  "fix" settings they do not control.
  **Fix:** Managed Kubernetes control planes are operated by the cloud
  provider; most master/control-plane section checks are out of scope and
  should be recorded as "not applicable — managed service" exceptions
  citing the provider's shared-responsibility documentation, not chased
  as remediation work.
- **Symptom:** Findings are suppressed by editing the scanner's config to
  skip check IDs, with no record of who approved it or why.
  **Fix:** Use a reviewed, version-controlled waiver file with
  justification, compensating control, approver, and expiry date per
  excluded check — not an undocumented scanner flag. An auditor (or a
  future incident responder) needs to be able to answer "was this
  intentional and reviewed" without archaeology.
- **Symptom:** A benchmark remediation (e.g. disabling anonymous kubelet
  auth, tightening a Docker daemon flag) is applied directly to production
  and breaks an in-cluster integration that depended on the old, insecure
  default.
  **Fix:** Test remediations in a non-production environment first and
  roll out through normal change management, especially for flags that
  affect authentication or networking; treat "safe to auto-remediate" as
  the exception, not the default.
- **Symptom:** The organization cites "we ran a CIS Benchmark scan" as
  evidence of compliance in a customer security questionnaire or audit,
  and the auditor pushes back.
  **Fix:** Be explicit that CIS does not certify individual organizations
  — a scan result is a technical hardening artifact, useful as supporting
  evidence for something like SOC 2 or ISO 27001 control testing (see
  [security-compliance-mapping-soc2-iso-pci-nist](../security-compliance-mapping-soc2-iso-pci-nist/SKILL.md)),
  but the compliance attestation itself comes from a qualified third-party
  audit, not from the scan tool.

## Worked example

Illustrative kube-bench run against a self-managed Kubernetes 1.27 cluster,
CIS Kubernetes Benchmark v1.24 profile, Level 1:

```json
{
  "Totals": { "total_pass": 46, "total_fail": 3, "total_warn": 12, "total_info": 0 },
  "Controls": [
    {
      "id": "1.2.1",
      "text": "Ensure that the --anonymous-auth argument is set to false (Automated)",
      "status": "FAIL",
      "actual_value": "--anonymous-auth=true"
    },
    {
      "id": "4.2.6",
      "text": "Ensure that the --protect-kernel-defaults argument is set to true (Automated)",
      "status": "FAIL",
      "actual_value": "--protect-kernel-defaults not set"
    },
    {
      "id": "1.1.12",
      "text": "Ensure that the etcd data directory ownership is set to etcd:etcd (Automated)",
      "status": "WARN",
      "reason": "requires manual verification of host filesystem"
    }
  ]
}
```

Illustrative triage and remediation table:

| Control | Finding | Decision | Action |
|---|---|---|---|
| 1.2.1 | API server allows anonymous auth | Remediate | Set `--anonymous-auth=false` on `kube-apiserver`; roll out via config-managed control-plane change |
| 4.2.6 | Kubelet not protecting kernel defaults | Remediate | Set `--protect-kernel-defaults=true` in kubelet config; verify no workload depends on relaxed sysctls first |
| 1.1.12 | etcd data dir ownership (manual check) | Verify then close | Confirmed `etcd:etcd` ownership via `ls -l /var/lib/etcd`; mark PASS with evidence attached |
| 1.3.7 (illustrative) | "Ensure `--bind-address` is set to 127.0.0.1" on a managed control-plane component that the cloud provider operates | Exception | Waiver: `control-plane managed by <CLOUD_PROVIDER>; verified in provider shared-responsibility doc <LINK_PLACEHOLDER>`, approver `<SECURITY_LEAD_PLACEHOLDER>`, expiry `<REVIEW_DATE_PLACEHOLDER>` |

Illustrative `waivers.yaml` entry:

```yaml
waivers:
  - control_id: "1.3.7"
    benchmark: "CIS Kubernetes Benchmark v1.24"
    reason: "Control-plane component managed by cloud provider; not accessible to customer."
    compensating_control: "Provider's own SOC 2 report covers this control (see vendor attestation)."
    approved_by: "<SECURITY_LEAD_PLACEHOLDER>"
    approved_date: "2026-06-01"
    review_by: "2027-06-01"
```

Summary reported to the requester: "46 pass / 3 fail / 12 warn against CIS
Kubernetes Benchmark v1.24, Level 1. 2 of 3 fails remediated this sprint
(1.2.1, 4.2.6); 1 fail converted to a reviewed, time-boxed exception
(control-plane check, cloud-managed). This is a hardening baseline, not a
compliance certification — see the compliance-mapping skill if this is
feeding a SOC 2 / ISO 27001 audit."

## Cross-references

- [cloud-well-architected-framework-review](../cloud-well-architected-framework-review/SKILL.md) — broader workload review (security is one pillar) that CIS hardening findings feed into.
- [security-compliance-mapping-soc2-iso-pci-nist](../security-compliance-mapping-soc2-iso-pci-nist/SKILL.md) — mapping CIS scan evidence to formal framework controls for audit readiness.
- [owasp-top-10-secure-coding-standards](../owasp-top-10-secure-coding-standards/SKILL.md) — application-layer counterpart; CIS Benchmarks cover infrastructure/OS/platform configuration, not app code.
- [container-image-hardening](../../../devsecops/skills/container-image-hardening/SKILL.md) — non-root users, read-only rootfs, and capability drops that satisfy many Docker/Kubernetes CIS controls at the image level.
- [policy-as-code-guardrails](../../../devsecops/skills/policy-as-code-guardrails/SKILL.md) — enforcing CIS-derived rules automatically via OPA/Kyverno admission control instead of relying solely on point-in-time scans.
- [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md) — the IAM-specific controls underlying cloud foundations benchmark checks (AWS/Azure/GCP).
- [aws-landing-zone-setup](../../../cloud/skills/aws-landing-zone-setup/SKILL.md), [azure-landing-zone-setup](../../../cloud/skills/azure-landing-zone-setup/SKILL.md), [gcp-landing-zone-setup](../../../cloud/skills/gcp-landing-zone-setup/SKILL.md) — where cloud foundations benchmark guardrails are typically established organization-wide.
