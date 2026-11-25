---
name: cloud-incident-response
description: Guides incident response in AWS, Azure, GCP and Microsoft 365/Entra, covering the logs that matter and their default retention, preserving evidence before auto-remediation, credential/session revocation order, identity-plane compromise (federation, app registrations, OAuth grants) and snapshot-based acquisition. Use when the user is responding to a cloud account or tenant compromise, leaked cloud keys, or needs to collect cloud forensic evidence.
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Cloud incident response

Cloud IR is mostly **identity-plane IR**. The attacker drives your control-plane API with stolen keys or tokens. The evidence is API logs and snapshots, not a disk you can seize.

This skill covers what's different in the cloud. General phases are in `load_skill incident-response`; decisions and comms are in `load_skill incident-response-leadership`; acquisition rigour and chain of custody are in `load_skill digital-forensics`.

## Log sources and default retention (know before the incident)

| Source                                | Default                                                                               | Gotcha                                                                                                                    |
| :------------------------------------ | :------------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------ |
| AWS CloudTrail **Event history**      | 90 days of management events, per account and Region                                  | No data events (S3 object, Lambda invoke); those need a trail or event data store and are off by default                  |
| Azure **Activity Log**                | 90 days                                                                               | Export via diagnostic setting (Log Analytics: up to 12 years). A management-group setting misses some subscription events |
| Entra **sign-in / audit**             | 7 days on Free, 30 days on P1/P2                                                      | Risky sign-ins: 90 days on P2. **Graph activity logs** aren't retained unless exported                                    |
| M365 **Unified Audit Log** (Purview)  | Standard: 180 days. Premium: 1 year for Exchange/SharePoint/OneDrive/Entra (E5 users) | Service-principal and other non-user records: fixed 1 year. 10-year add-on available                                      |
| GCP **Admin Activity / System Event** | 400 days in `_Required`, fixed                                                        | Always on                                                                                                                 |
| GCP **Data Access**                   | Off by default (except BigQuery)                                                      | Lands in `_Default` (30 days); route to a sink to keep longer                                                             |

verify: https://docs.aws.amazon.com/awscloudtrail/latest/userguide/view-cloudtrail-events.html, https://learn.microsoft.com/en-us/entra/identity/monitoring-health/reference-reports-data-retention, https://learn.microsoft.com/en-us/purview/audit-log-retention-policies, https://docs.cloud.google.com/logging/docs/audit

- **Centralise logs where the attacker can't reach them.** Use a log-archive account/subscription/project with immutability (S3 Object Lock, immutable blob). The compromised principal must not be able to delete them.
- **Entra has four sign-in streams:** interactive, non-interactive, service-principal and managed-identity. Token replay and app abuse live in the last three, which few people open.
- **Mailbox scoping:** `MailItemsAccessed` answers "what did they read". Licence coverage has shifted, so verify it (CISA Microsoft Expanded Cloud Logs playbook, revised 2026).
- **Kubernetes:** audit logs are off by default on EKS (control-plane logging) and on self-managed clusters; AKS needs a diagnostic setting. **Events expire after 1 hour.**
- **Flow logs** (VPC/VNet) are opt-in on all three clouds.
- **A log that wasn't on can't answer anything.** Write "unknowable", not "no evidence", and carry it into lessons learned.

## First hour: preserve before you remediate

- **Pause evidence-destroying automation.**
  - Auto-remediation: GuardDuty/Security Hub/Defender actions, SOAR playbooks, and Config/Policy rules that delete, rotate or terminate.
  - Autoscaling replacement: suspend processes and set termination protection.
  - Spot/preemptible reclaim.
  - A bot that deletes a leaked key also destroys the key-ID pivot you need for scoping.
- **Export the current state** to a separate IR account before anything changes. The attacker may revert changes, so this is your baseline.
  - IAM: users, keys, roles and trust policies, SAML/OIDC providers.
  - Entra: app registrations and service principals with their credentials, OAuth grants, Conditional Access policies, domains and federation settings.
  - GCP: IAM bindings and SA keys.
- **Work from clean identities.** Use break-glass or IR accounts that aren't federated through a possibly compromised IdP, operating from a separate forensics account or tenant.

## Containment: revocation order

Cut what lets the attacker **mint new credentials** first, then live sessions, then keys. Get the order wrong and they simply re-issue.

1. **Find the abused root of trust.** It's usually one of: a federation trust or IdP, credentials on an app or service principal, a long-lived access key, a CI OIDC trust, or a human session.
2. **Remove persistence.**
   - Federated domains or IdP signing certs the attacker added.
   - New secrets, certificates or federated identity credentials on apps.
   - New IAM users or keys.
   - Role trust policies that admit outside accounts.
   - GCP SA keys and `serviceAccountTokenCreator` grants.
   - Automation backdoors (Lambda, runbooks, Cloud Functions).
3. **Revoke access.**
   - **AWS:**
     - Issued STS credentials can't be cancelled, only denied. Use the role's _Revoke active sessions_ (an `AWSRevokeOlderSessions` deny on `aws:TokenIssueTime`).
     - **Deactivate** access keys rather than deleting them; the key ID is evidence.
     - Put the same TokenIssueTime deny on the user too. Session tokens minted from a key survive its deactivation.
     - Revoke Identity Center sessions separately. verify: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_revoke-sessions.html
   - **Entra:**
     - Block sign-in, then reset the password.
     - `revokeSignInSessions` kills refresh tokens, but **issued access tokens live about 1 hour** unless the app supports CAE. Bridge that gap with a Conditional Access block.
     - Remove MFA methods and devices the attacker registered, and disable a compromised device (its Primary Refresh Token). verify: https://learn.microsoft.com/en-us/entra/identity/users/users-revoke-access
   - **GCP:** disable the SA key or the SA itself, strip IAM bindings, and reset and sign out the user via Workspace/Cloud Identity.
4. **Rotate every secret the principal could read:** secret managers, Key Vault, K8s Secrets, CI variables. Readable means read.

Revoking tips off the attacker. Against a capable actor, plan a coordinated eviction rather than piecemeal kills (`load_skill incident-response-leadership`).

## Identity-plane compromise

- **Federation backdoor.** An admin-level attacker adds or changes a federated domain or signing cert, then mints tokens for any user and bypasses MFA.
  - Entra audit events: _Set domain authentication_, _Set federation settings on domain_, a newly verified domain.
  - AWS: a new SAML/OIDC provider, or a role that trusts one.
  - GCP: workforce or workload identity pool changes.
- **App registrations and service principals.** The pattern: credentials added to an existing (often forgotten) app, which then gets application permissions like `Mail.Read` or `full_access_as_app` via admin consent and reads data with no user involved.
  - Audit events: `Add service principal credentials`, `Update application – Certificates and secrets management`, `Add app role assignment to service principal`.
  - Read the service-principal sign-in log for what the app did.
- **OAuth consent grants (delegated).** Illicit apps holding `offline_access` survive a password reset.
  - Enumerate `oauth2PermissionGrants`, revoke the grants and disable the app.
  - Turn on the admin-consent workflow.
- **Mailbox persistence:** inbox rules, forwarding, delegates, mailbox permissions.
- **CI workload identity.** A cloud role that trusts a CI OIDC issuer without a tight `sub` condition can be assumed by _any_ repo on that platform. Review the trust policy, not just the keys.

## Acquisition (snapshots, not seizure)

- **Memory first.** Capture RAM through the agent or SSM/Run Command _before_ you stop or isolate the instance; stopping it loses memory.
- **Isolate without destroying.**
  - Apply a quarantine SG/NSG and tag the instance.
  - In AWS an SG change doesn't cut already-tracked connections, so add a NACL.
  - Detach the instance from autoscaling.
  - Credentials it already took from IMDS stay valid until expiry, so revoke them as above.
- **Disk.**
  - AWS: EBS snapshot shared to the forensics account. That needs a customer-managed KMS key; snapshots under the default `aws/ebs` key can't be shared.
  - Azure: managed-disk snapshot copied to the forensics subscription.
  - GCP: persistent-disk snapshot or image in a forensics project.
  - Mount the copy read-only in an isolated VPC, and hash it.
- **Kubernetes.**
  - Cordon the node and isolate the pod with a label plus a deny-all NetworkPolicy. **Don't delete the pod**; that destroys its filesystem.
  - Copy pod logs, `describe` output and events (1-hour TTL).
  - Snapshot the node disk, and checkpoint the container where the kubelet supports it.
- **Serverless and object stores.** Collect function code and versions, env vars, the execution role and logs. Without data events or access logs, "what was read" stays unknown; say so.

## marq tie-in

marq holds no cloud credentials and wraps no cloud CLI.

- **Stage evidence:** put exported logs and IAM dumps under `/work` with `write_file`; read them back with `read_file`.
- **Enrich source IPs:** `asnmap` and `shodan_host`, then `load_skill indicator-enrichment`.
- **Examine artefacts:** YARA and capa on recovered binaries, and an image scanner such as trivy on the image a compromised pod ran, in your own sandbox.
- **Trace a leaked key's origin:** `trufflehog` on the public repo (marq's tool never verifies; verifying a key calls the provider with it and pollutes the trail you're reading), or gitleaks in your own checkout.
- **Report:** `report_finding` for each conclusion with its log source and event ID; `render_report` for the timeline.

## Pitfalls

- Deleting the key, user or instance before recording it.
- Revoking sessions but not the persistence that mints new ones.
- Treating Event history or the portal's 7 to 90-day windows as "the logs".
- Investigating from an identity that runs through the compromised IdP.
