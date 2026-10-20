---
name: security-gate-exception-management
description: >
  Guides granting a scoped, time-boxed exception to a specific security
  gate (a suppressed SAST/SCA finding, a bypassed admission policy, a
  waived compliance control) with a mandatory owner, justification, and
  expiry date, and reviewing/renewing or closing exceptions before a
  waiver list grows into an unbounded shadow policy. Use when the user
  asks to "grant an exception to a security gate", "waive this finding
  for now", "how do we approve a temporary policy exception", "our
  exception list has hundreds of entries and half are expired", or
  "design an exception approval workflow". Distinct from disabling a
  gate entirely, which this skill explicitly treats as a separate,
  much riskier action requiring its own scrutiny.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: devsecops
  maturity: stable
---

# Security Gate Exception Management

## Purpose

Every security gate — a SAST/SCA severity threshold, an admission-policy
`deny` rule, a compliance control — will eventually encounter a
legitimate case where blocking is the wrong call: a finding with no
available fix yet, a policy that doesn't account for a genuine
architectural exception, a control that doesn't apply to a specific
system for a documented reason. Refusing to ever grant an exception
just pushes teams toward disabling the gate entirely to unblock
themselves, which is strictly worse. But an exception process with no
discipline degrades the same way: waivers get granted informally, never
reviewed, never expire, and a year later the "temporary" exception list
is longer than the set of things actually being enforced — at which
point the gate is exceptions-driven security theater rather than a real
control. This skill covers designing and operating the exception
process itself: what a valid exception request must contain, who can
approve it, how expiry and renewal work, and how to keep the aggregate
waiver list itself under review rather than a write-only log nobody
revisits.

## When to use

- A specific finding, policy violation, or compliance control can't be
  immediately remediated and someone needs a documented, approved
  temporary exception rather than an ad hoc bypass.
- The user asks to design or formalize an exception-approval workflow
  from scratch (who approves, what fields are required, how long an
  exception can last by default).
- An existing exception/waiver list has grown large, has expired entries
  still silently in effect, or nobody can say who approved a specific
  waiver or why.
- The user is deciding between "grant a scoped exception" and
  "reconfigure the gate itself" for a recurring pattern of exception
  requests against the same rule.
- An auditor or compliance review asks for evidence of how security
  exceptions are governed, tracked, and reviewed.
- Someone proposes disabling a security gate entirely to unblock a
  release, and the user needs to evaluate whether a scoped exception is
  the safer alternative (it almost always is).

## Prerequisites & environment

- An underlying gate or control already in place to grant exceptions
  against — SAST/SCA suppression syntax
  ([sast-integration](../sast-integration/SKILL.md),
  [software-composition-analysis-sca](../software-composition-analysis-sca/SKILL.md)),
  an admission-policy exclusion mechanism
  ([opa-gatekeeper-policy-authoring](../../../policy-and-governance-tooling/skills/opa-gatekeeper-policy-authoring/SKILL.md),
  [kyverno-policy-management](../../../policy-and-governance-tooling/skills/kyverno-policy-management/SKILL.md)),
  or a compliance-framework control tracked in a GRC tool.
  This skill governs the process wrapped around those mechanisms, not
  the suppression syntax itself.
- A ticketing system or exception registry capable of recording, per
  exception: the specific finding/control/policy, scope, justification,
  approver, grant date, and — non-negotiably — an expiry date. A
  spreadsheet is an acceptable starting registry; a dedicated
  GRC/AppSec platform (DefectDojo, ServiceNow GRC, a policy-engine's own
  exception CRD/annotation) is the steady-state target once volume
  justifies it.
- A defined approval authority per exception severity/scope — who can
  approve a low-risk, narrowly-scoped exception (e.g. a team lead) vs.
  who must approve a broad or high-risk one (e.g. a security lead or
  CISO delegate) — agreed before the first request, not improvised
  under deadline pressure.
- A recurring review cadence (calendar reminder, automated report, or a
  scheduled job querying the registry) to catch exceptions nearing or
  past expiry — an expiry date that nobody actually checks is
  equivalent to no expiry date.

## Step-by-step guidance

1. **Require five fields on every exception request**, with none
   optional: the specific finding/rule/control being excepted (not "all
   SAST findings in this repo"), the scope it applies to (a specific
   file/service/namespace, not org-wide), a written justification, a
   named owner accountable for eventual remediation, and an explicit
   expiry date. A request missing any of these is not ready for
   approval.
   ```yaml
   # exceptions/EXC-2026-0142.yaml — example exception registry entry
   id: EXC-2026-0142
   control: "sca.trivy.CVE-2024-EXAMPLE-1"
   scope: "service: internal-report-generator (build-tooling only, not shipped to prod)"
   justification: >
     No upstream fix available yet; affected code path only runs in the
     internal build pipeline, never in a deployed artifact or exposed to
     untrusted input.
   owner: "platform-team (jane.doe@example.com)"
   approved_by: "security-lead (alex.chen@example.com)"
   granted: 2026-07-01
   expires: 2026-10-01
   status: active
   ```

2. **Scope every exception as narrowly as the underlying mechanism
   allows** — a specific finding ID/CVE in a specific
   service/namespace, never a blanket "disable this rule everywhere" or
   "exclude this whole namespace from all policies." Narrow scoping is
   what keeps an exception from silently covering future, unrelated
   findings that happen to match the same broad exclusion.
   ```yaml
   # Good: scoped to the exact rule and exact namespace
   exclude:
     any:
       - resources:
           namespaces: ["legacy-migration"]
   # (paired with a specific rule name in the policy, not a wildcard match)
   ```
   > **Warning:** an exception scoped broadly enough to match resources
   > or findings beyond the one it was actually granted for is
   > functionally equivalent to disabling the gate for that whole scope
   > — treat over-broad scoping in an exception request as a rejection
   > reason, not a minor style note.

3. **Route approval by risk tier**, matching the severity/scope of what's
   being excepted:
   ```
   | Exception scope/severity          | Required approver            |
   |------------------------------------|-------------------------------|
   | Low severity, single service       | Team lead                     |
   | High/critical severity, any scope  | Security lead or delegate      |
   | Any scope spanning multiple teams  | Security lead + affected leads |
   | Compliance-control exception       | Compliance/GRC owner          |
   ```
   Never allow the requester to also be the sole approver for
   anything above the lowest tier — a second, independent set of eyes on
   the justification is the whole point of an approval step.

4. **Set a default maximum exception duration** (e.g. 90 days) rather
   than allowing indefinite or multi-year grants, and require an
   explicit, justified renewal — not an automatic extension — for
   anything that needs longer:
   ```yaml
   status: active
   expires: 2026-10-01     # default cap; extend only via a new, reviewed renewal entry
   renewal_of: null        # set to the prior exception ID if this is a renewal
   ```

5. **Automate expiry enforcement where the underlying tool supports
   it** — configure the gate to revert to blocking automatically once
   an exception's expiry passes, rather than relying on someone to
   manually remove a suppression on the right day:
   ```bash
   # Example: a scheduled CI job that fails if any exception's expiry has passed
   python3 scripts/check_exception_expiry.py --registry exceptions/ --fail-on-expired
   ```
   ```python
   # scripts/check_exception_expiry.py (illustrative, not production code)
   import sys, yaml, datetime, pathlib

   today = datetime.date.today()
   expired = []
   for f in pathlib.Path("exceptions").glob("*.yaml"):
       entry = yaml.safe_load(f.read_text())
       if entry["status"] == "active" and entry["expires"] < str(today):
           expired.append(entry["id"])

   if expired:
       print(f"Expired, unreviewed exceptions: {expired}")
       sys.exit(1)
   ```

6. **Review the exception nearing expiry, not after it's already lapsed**
   — trigger a review (ticket, notification) a fixed lead time before
   `expires` (e.g. 2 weeks), so the owner has time to either close out
   remediation, or submit a justified renewal request through the same
   approval process, before the gate reverts to blocking unexpectedly.

7. **Track the exception list itself as a metric**, not just individual
   exceptions — total active count, count by age, count nearing expiry,
   and count renewed more than once (a repeatedly-renewed exception is a
   signal the underlying issue needs a real fix, not more waivers). Feed
   this into
   [security-posture-metrics-and-trend-analysis](../security-posture-metrics-and-trend-analysis/SKILL.md).

8. **Distinguish a scoped exception from disabling the gate**, explicitly,
   every time someone proposes the latter as a shortcut:
   > **Warning — destructive action risk:** disabling a security gate
   > entirely (turning off a required CI check, deleting/disabling an
   > admission policy, setting a webhook's `failurePolicy` to `Ignore`
   > indefinitely) removes protection for *every* finding/violation that
   > gate would have caught, not just the one blocking the current
   > release — including ones nobody has looked at yet. A scoped
   > exception, in contrast, only bypasses the one specific,
   > reviewed, time-boxed case. If a release is blocked and the
   > pressure is to "just turn the check off," that is exactly the
   > moment to insist on a scoped exception through this process
   > instead, however much slower it feels in the moment.

## Best practices

- Require all five fields (control, scope, justification, owner, expiry)
  on every exception with no exceptions to the exception process itself
  — a request missing an owner or an expiry date is not a smaller ask,
  it's an unbounded one.
- Cap default exception duration and require an explicit, re-approved
  renewal for anything longer, rather than allowing "no expiry" or
  multi-year grants as a default option.
- Scope exceptions to the narrowest unit the underlying tool supports
  (a specific finding ID, a specific namespace/service) — never a
  rule-wide or org-wide exclusion for a problem that only affects one
  case.
- Automate expiry enforcement so a lapsed exception reverts to blocking
  by default, rather than depending on someone remembering to manually
  re-enable a check on the right date.
- Route approval by risk tier, and never let the requester also be the
  sole approver above the lowest tier — independent review is the
  control, not a formality.
- Report on the exception list itself (count, age, renewal frequency) on
  the same cadence as other security posture metrics — a growing or
  aging waiver list is itself a finding, not just administrative
  overhead.
- Treat "disable the gate" as a categorically different, far riskier
  request than "grant a scoped exception," and require materially higher
  scrutiny (documented sign-off from a security lead, an explicit
  re-enable deadline, no exceptions for indefinite disabling) before
  ever agreeing to it.

## Common pitfalls

- **Symptom:** An exception list has hundreds of entries, many with no
  expiry date or an expiry date long past, and no one can say who
  approved several of them.
  **Fix:** Migrate to a registry that enforces the five required fields
  at creation time (a schema-validated file, a ticket template with
  required fields, a GRC tool), run the expired-entry check
  script/report immediately to surface the current backlog, and require
  every already-lapsed entry to go through fresh review (renew with
  justification, or close/remediate) rather than grandfathering them in
  indefinitely.

- **Symptom:** A developer under deadline pressure adds a broad
  suppression (`# nosemgrep` with no rule ID, an `excludedNamespaces`
  covering an entire team's namespace) to unblock a release, without
  going through approval.
  **Fix:** Require CI/policy tooling itself to reject unscoped or
  unattributed suppressions at merge time where feasible (e.g. a linter
  step failing on a bare `# nosemgrep` with no rule ID and comment), and
  treat an after-the-fact discovered unapproved suppression as a
  process violation to remediate, not a precedent to formalize
  retroactively.

- **Symptom:** The same exception has been renewed six times over two
  years, each renewal approved with minimal scrutiny because "it's just
  the usual renewal."
  **Fix:** Flag exceptions renewed more than once (or open longer than
  some threshold, e.g. a year cumulative) for escalated review — a
  repeatedly-renewed exception usually means the underlying issue needs
  a committed remediation project, not indefinite waiver renewal, and
  should be raised to a level empowered to fund that work.

- **Symptom:** Facing a blocked release, a team disables the entire
  security gate (turns off the required CI check, or sets a webhook's
  `failurePolicy` to `Ignore`) instead of requesting a scoped exception
  for the one specific finding blocking them.
  **Fix:** This removes coverage for every other finding the gate would
  have caught, not just the one causing the immediate block. Insist on
  the scoped-exception path even under time pressure — if the exception
  process itself is too slow to use in a genuine emergency, that's a
  signal to fix the process's turnaround time (an expedited path for
  genuinely urgent requests, mirroring
  [critical-vulnerability-emergency-response](../critical-vulnerability-emergency-response/SKILL.md)),
  not to bypass it by disabling the whole gate.

- **Symptom:** An automated expiry check exists but nobody acts on its
  output, so expired exceptions accumulate in the report without being
  resolved.
  **Fix:** Wire the expiry check's output into an actual accountable
  workflow (auto-created ticket assigned to the exception's owner, a
  required agenda item in the recurring triage meeting from
  [security-finding-backlog-triage](../security-finding-backlog-triage/SKILL.md)) —
  a report nobody is required to act on is equivalent to no check at
  all.

## Worked example

A team needs a temporary exception for a Trivy SCA finding
(`CVE-2024-EXAMPLE-9`, illustrative) in a build-tooling-only dependency
with no upstream fix yet, alongside an unrelated request to fully
disable the SCA gate that gets redirected to a proper scoped exception
instead.

**Request 1 (properly scoped, approved):**
```yaml
# exceptions/EXC-2026-0207.yaml
id: EXC-2026-0207
control: "sca.trivy.CVE-2024-EXAMPLE-9"
scope: "service: report-builder (build-time dependency only, not in shipped artifact)"
justification: >
  Upstream project has acknowledged the CVE but no patched release yet
  (tracked at UPSTREAM-ISSUE-1183). Dependency is used only by the build
  toolchain and is never included in the deployed container image.
owner: "platform-team (jane.doe@example.com)"
approved_by: "security-lead (alex.chen@example.com)"
granted: 2026-07-15
expires: 2026-09-15
status: active
renewal_of: null
```
Wired into the pipeline as a scoped `.trivyignore` entry limited to that
one service's scan job, with the same expiry date and a comment pointing
at the exception record:
```
# .trivyignore (report-builder service only)
# EXC-2026-0207: build-time-only dependency, no upstream fix yet.
# Approved by alex.chen, expires 2026-09-15. Do not renew without re-review.
CVE-2024-EXAMPLE-9
```

**Request 2 (redirected):** A separate team, blocked by an unrelated
critical finding in a different service, initially asks to set
`exit-code: '0'` on the Trivy CI step for their whole repository "just
for this release." This is declined as a full gate disablement covering
every current and future finding, not just the one blocking them; they
are redirected to file a properly scoped exception for the single
blocking finding instead, following the same template as Request 1.

**Expiry automation:** A scheduled job runs
`check_exception_expiry.py` weekly; on 2026-09-01 (two weeks before
EXC-2026-0207's expiry) it opens a renewal-or-close reminder ticket
assigned to `jane.doe@example.com`, who confirms the upstream fix has
now shipped and closes the exception by upgrading the dependency instead
of renewing it.

## Cross-references

- [security-finding-backlog-triage](../security-finding-backlog-triage/SKILL.md) —
  the ongoing triage process that routes findings into the "accepted
  risk" lane this skill's formal exception workflow governs.
- [critical-vulnerability-emergency-response](../critical-vulnerability-emergency-response/SKILL.md) —
  when a finding genuinely cannot be remediated during an emergency
  response, the resulting temporary exception should still be recorded
  through this process rather than left informal.
- [secure-cicd-gates](../secure-cicd-gates/SKILL.md) — the gate design
  (severity-to-action table, blocking vs. warning) that exceptions are
  granted against.
- [security-posture-metrics-and-trend-analysis](../security-posture-metrics-and-trend-analysis/SKILL.md) —
  tracking exception-list size, age, and renewal frequency as an ongoing
  posture metric.
- [opa-gatekeeper-policy-authoring](../../../policy-and-governance-tooling/skills/opa-gatekeeper-policy-authoring/SKILL.md) —
  `excludedNamespaces` and Constraint-scoping mechanics that an
  admission-policy exception is implemented through.
