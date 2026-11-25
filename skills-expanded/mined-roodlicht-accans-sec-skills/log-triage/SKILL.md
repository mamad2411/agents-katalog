---
name: log-triage
description: Identity-log triage workflow — anomaly patterns per provider (AWS CloudTrail, Azure AD/Entra, Google Workspace, Okta), session and token misuse, MFA-bypass signals, conditional-access evasion, and cross-provider correlation. Produces a prioritized finding list routed to ir-runbook or detection-engineer.
---

# Log Triage

> **Identity-first context**: the bulk of modern incidents starts or escalates via identity providers. Logs are the truth source — UIs are stale snapshots. This skill covers audit/identity logs from the major IdPs; network logs and endpoint EDR touch on this but live in other skills.

## When to use

A log-triage question begins with "something is odd in the logs, take a look". This skill provides, per provider, the pattern set you can use to triage where people get lost in volume.

Triggers on:

- A question like "look at these CloudTrail events", "is this Azure AD sign-in anomaly real", "Google Workspace audit log has N login failures", "what is the anomaly here in Okta", "compromised-account investigation".
- A handoff from `detection-engineer` (rule fired, asks for deeper triage), `ir-runbook` (incident investigation), `ioc-hunter` (IOC match in an identity log).
- A proactive hunting session focused on identity anomalies — overlap with `threat-hunt`.
- A post-incident investigation where the identity path must be reconstructed for `forensics-assist` or regulatory reporting.

### When NOT (handoff)

- Generic SIEM-query building → `siem-query`.
- Writing a detection rule based on the pattern → `detection-engineer`.
- A threat-hunt session as a whole → `threat-hunt` (command).
- Forensic memory/disk analysis → `forensics-assist`.
- Network-flow triage or EDR process events → out of scope here; covered in generic SIEM-query or an EDR-tool skill.
- IOC curation or enrichment → `ioc-hunter`.
- Regulatory reporting → `ir-runbook` plus `nis2`/`gdpr-pia`.

## Approach

Six phases. Phase 1 (provider context) and phase 4 (cross-provider correlation) are where triage builds from isolated events into a meaningful path.

### 1. Provider context and log-source inventory

Identity logs differ per provider in event shape, retention, and accessibility. Triage starts with "which provider, which log stream, which retention".

- **AWS**: CloudTrail (management + data events), CloudTrail Insights (anomaly detection, paid), GuardDuty (managed detection, IAM-relevant findings).
- **Azure / Entra ID**: Sign-in logs (interactive + non-interactive + service-principal), Audit logs (directory changes), Risk Detections (Identity Protection), Provisioning logs.
- **Google Workspace**: Login audit, Admin audit, OAuth Token audit, Drive audit.
- **Okta**: System Log (all auth events plus admin actions), Tableau Insights (managed anomaly).
- **JumpCloud / OneLogin / Ping**: comparable structure.
- **On-prem AD**: Security Event Log via Sysmon/Windows Audit; via DC SIEM forwarder.

Per source: retention window (default often shorter than the compliance requirement), log completeness (are all event types enabled?), log integrity (forwarding to SIEM complete?).

Pre-triage check: do you have access to all relevant streams for the time window of the incident, not just the "obvious" stream?

### 2. Anomaly patterns per provider

Per IdP, a pattern set you walk through by default. Not exhaustive; a starting point for triage.

**AWS CloudTrail**:

- **Console login without MFA** where policy requires MFA. Event: `ConsoleLogin` with `additionalEventData.MFAUsed=No`.
- **GetSecretValue / Decrypt bursts** by one principal in a short window — credential-harvesting pattern.
- **AssumeRole-cross-account** from an unexpected source account.
- **CreateAccessKey + persist** for an existing user (pattern T1098.001 — additional cloud credentials).
- **DisableLogging** events: StopLogging on Trails, DeleteTrail, UpdateConfigurationRecorder. Pattern T1562.008.
- **Mass S3 GetObject** or `ListBuckets` over a short window — exfil discovery.
- **IAM policy with `Resource: "*"` plus `Action: "*"`** — overly permissive setup.
- **Region anomaly**: activity in regions the org never deploys to.

**Azure AD / Entra ID**:

- **Sign-in from impossible travel**: geo-pattern with velocity > realistic flight time. Identity Protection flags this, but verify in detail (VPN effects, mobile roaming).
- **MFA-fatigue pattern**: multiple MFA prompts in quick succession followed by an approve. T1621 pattern. Conditional Access can block this with "request-frequency limit".
- **Service-principal misuse**: a principal with an admin role suddenly signing in from non-authorized locations.
- **Legacy auth-protocol use**: Basic Authentication, IMAP, POP — usually MFA-bypassing. Should be off.
- **Conditional-Access bypass attempts**: failures on a CA policy followed by success via another route.
- **Application consent grants** with sensitive scopes (Mail.ReadWrite, Files.ReadWrite.All) by regular users — illicit consent grant T1528.
- **Token replay**: same token from different locations.

**Google Workspace**:

- **OAuth grants** with external apps by regular users — Drive-data-leak vector.
- **Admin-Add / Role-Change**: privilege elevation.
- **Mass mail-forward-rule set**: BEC classifier T1114.003.
- **Login from unusual location** plus device-fingerprint mismatch.
- **2SV disabled** for an account that previously had 2SV — recovery or abuse.
- **Drive scope-share** "anyone with link" on sensitive data.

**Okta**:

- **Push-notification reject** followed by push-accept elsewhere — MFA fatigue.
- **Factor reset** by an admin on a user — backdoor pattern.
- **API-token creation** by an admin with a high scope.
- **App-instance-add / OIN-app grant** with a high scope.
- **Bypass** of network-zone policies.

### 3. Per-event triage: question row

For each suspicious event, answer:

- **Actor**: user, service account, or API token? Was the behavior expected for this actor?
- **Source**: IP, ASN, geographic, device fingerprint. Match this against known employee locations / mobile providers / VPN exit points / cloud-provider IP ranges.
- **Authentication chain**: how did the actor sign in (password, certificate, SAML assertion, OAuth token replay)? MFA used? Which factor?
- **Time**: within working hours for this actor? Coherent with other activity (before/after)?
- **Outcome**: success, failure, partial. On failure: what is the exact error? Which control caught it?
- **Prior behavior**: what did this actor do 24h before? Pattern shift?

Collect answers in incident-table form. Without structure you lose consistency across events.

### 4. Cross-provider correlation

Real attacks spread across identity providers. A disturbance in Azure AD often propagates into AWS via federated auth, into Google Workspace via SAML, into SaaS tools via OAuth.

Correlation strategies:

- **User-identity mapping**: the same person in Azure AD + Google + Okta + AWS. Email match works often. Document the mapping in advance so triage does not become a lookup loop.
- **Time-window overlap**: actor X active in Azure AND a GuardDuty finding in AWS in the same 30-minute window.
- **IP correlation**: the same IP for a sign-in in two providers within a short window.
- **Token-trail tracking**: a SAML assertion from IdP A produces an AccessKey on cloud B that is used to hit SaaS resource C.

SIEM tooling with cross-provider data is critical here (see `siem-query`). Manual correlation works for small investigations; for larger incidents, a unified data layer is needed.

### 5. Prioritization and triage output

Per finding:

- **Severity classification**:
  - **Confirmed compromise**: evidence of real misuse, route directly to `ir-runbook`.
  - **High-suspicion**: pattern matches, no direct evidence, asks for deeper action (force MFA reset, verify with user).
  - **Anomalous but explainable**: looks anomalous but matches a legitimate situation. Document for the baseline.
  - **Background noise**: false-positive pattern. Handoff to `alert-tuning` for rule adjustment.

- **Recommended action** per finding: account disable, force pw reset, MFA re-enroll, key rotation, conditional-access tighten, deeper forensics.

- **Handoffs**: high-suspicion and confirmed → `ir-runbook`; pattern feedback → `detection-engineer`; new IOCs → `ioc-hunter`; tuning input → `alert-tuning`.

### 6. Verification-loop

Layer 1: scope (all relevant streams checked for the time window, no blind spots like service-principal logs or OAuth-grant logs?), assumptions (user confirmed or denied the activity?), gaps (cross-provider correlation done, not just single-provider tunnel vision?). Layer 2: event-type names match current provider docs, no invented field names or API event IDs, ATT&CK T-IDs correct.

## Output

```
Log triage — <scope / actor / event-cluster>
Time window: <start → end UTC>
Streams checked: <provider × log source>

Findings (per actor, per provider):
  Actor:       <user-ID + provider>
  Provider:    <AWS/Azure/Google/Okta>
  Pattern:     <impossible-travel / mfa-fatigue / illicit-consent / etc>
  Events:      <event IDs + timestamps>
  Severity:    <confirmed | high-suspicion | anomalous-explainable | noise>

Cross-provider correlation:
  IP overlap:    <IP found in providers X, Y>
  Time overlap:  <actor cluster within N minutes>
  Token trail:   <if relevant>

Recommended actions per finding:
  - <actor>: <account-disable / force-pw / MFA-reset / key-rotate / etc>

Handoffs:
  ir-runbook:         <confirmed compromises>
  detection-engineer: <pattern supports a new rule>
  ioc-hunter:         <new IOCs for enrichment>
  alert-tuning:       <noise rules for lifecycle treatment>

Verification-loop: ...
```

## References

- **AWS CloudTrail user guide** — [https://docs.aws.amazon.com/awscloudtrail/latest/userguide/](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/). Event types, log formats.
- **AWS CloudTrail Reference (Mitiga)** — external analysis resource for CloudTrail event mapping to ATT&CK.
- **Microsoft Entra ID monitoring docs** — [https://learn.microsoft.com/en-us/entra/identity/monitoring-health/](https://learn.microsoft.com/en-us/entra/identity/monitoring-health/). Sign-in / Audit / Risk logs.
- **Microsoft Defender for Identity** — [https://learn.microsoft.com/en-us/defender-for-identity/](https://learn.microsoft.com/en-us/defender-for-identity/). On-prem AD monitoring.
- **Google Workspace Audit Logs** — [https://support.google.com/a/answer/9725452](https://support.google.com/a/answer/9725452).
- **Okta System Log API** — [https://developer.okta.com/docs/reference/api/system-log/](https://developer.okta.com/docs/reference/api/system-log/).
- **MITRE ATT&CK — Cloud matrix** — [https://attack.mitre.org/matrices/enterprise/cloud/](https://attack.mitre.org/matrices/enterprise/cloud/).
- **Mandiant — Threats to identity providers** — periodic reports via [https://www.mandiant.com/resources](https://www.mandiant.com/resources).
- **CISA — Cloud and identity hardening guidance** — [https://www.cisa.gov/](https://www.cisa.gov/).

## Categories

- blue
