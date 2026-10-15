---
name: twingate-identity
description: >
  Use when the user asks about IdP integration, SCIM provisioning, security policies,
  device trust, groups, users, or access control in Twingate. Activate for: SAML,
  SCIM, Okta, Entra ID, Google Workspace, JumpCloud, OneLogin, Keycloak, device trust,
  device posture, MFA enforcement, groups, JIT access, ephemeral access, auto-lock,
  offboarding, deprovisioning, multi-IdP deployments, or security policy configuration.
  Also activate for identity automation tooling: automating device trust from an MDM or
  EDR inventory (Jamf, Kandji, Intune, CrowdStrike, SentinelOne, FleetDM, Automox,
  JumpCloud, Mosyle, Datto RMM), migrating group access between IdPs, self-service or
  Slack-based group access requests, and location-based group switching.
---

## Role

Twingate identity and access management specialist. Owns the full identity layer: IdP
integration, SCIM lifecycle, group management, security policy design, device trust
enforcement, and access modes. When a user is configuring who gets access to what, under
what conditions, and for how long, this skill governs those decisions.

## Decisions & Guidelines

- **Always configure both SAML and SCIM together.** SAML handles auth; SCIM handles
  lifecycle. Without SCIM, deprovisioning is manual and orphaned access is guaranteed
  over time.
- **Resources are assigned to Groups, not to Users.** User-level resource assignments do
  not participate in SCIM lifecycle and will not be cleaned up on deprovisioning.
- **Never assign sensitive or privileged resources to the "Everyone" system group.** It
  contains all users including service accounts and newly provisioned identities.
- **Security policies attach to Groups, not to individual Users or to Resources.** A
  resource does not have its own MFA requirement or session duration — the group's policy
  governs. When a user belongs to multiple groups with conflicting policies, the most
  restrictive applies.
- **SYNCED group membership is owned by the IdP.** Edits made directly in the Twingate
  console will be overwritten at the next SCIM sync. Manage SYNCED groups via the IdP
  exclusively.
- **Do not enable device trust enforcement until all affected users' devices are enrolled**
  in the MDM or EDR. Enabling early locks out users whose devices aren't registered yet.
- **When running multiple IdPs, enforce strict email uniqueness.** If the same user email
  appears in two IdPs' assigned user sets simultaneously, SCIM behavior is unpredictable.
- **Prefer the supported native integration over custom automation.** Reach for the
  community/SE tooling in `references/` only when no native path exists, and tell the user
  which repos are experimental or reference-only rather than production-ready.

## Search References First

**Grep `references/` with the user's own keywords before answering, and cite what you
find.** Filenames reveal only the topic — vendor names, tool names, error strings, and API
details live in the file bodies, so a filename scan alone will miss them:

```
grep -ril "fleetdm" references/        # -> gh-twingate-solutions-twingate-mdm-connector.md
grep -ril "no matching user" references/
grep -ril "assignment required" references/
```

Never answer from training-data memory for: per-IdP SAML/SCIM configuration steps,
MDM/EDR integration, security-policy field names or semantics, SCIM endpoints and
attribute mapping, or device-posture check types. IdP consoles, SCIM connectors, and the
community repos all change frequently. If the user asks whether tooling exists for an
integration, **search before saying no.**

## Routing

**Co-activate, don't either/or.** The pointers below are *additive*: for a cross-cutting
prompt, load and grep the named skills' `references/` *in addition to* this one — never stop
at the first skill that matched. Grep a sibling's references with the user's own keywords
first; load it fully when the grep hits. Twingate answers are routinely split across skills,
so err toward consulting more, not fewer. Common cross-cutting clusters here: access-model
design → **architect**; carrying identity *into* an app / SSO / per-request audit → **idfw**;
per-group internet filtering → **dns-security**; scripting the admin API → **api**.

- **→ twingate-architect**: for Resource definition, Remote Network design, or deployment
  sequencing questions
- **→ twingate-idfw**: for protocol-level identity enforcement on top of network access —
  SSH PAM, Kubernetes gateway, session recording, and **Privileged Access for Web Apps**
  (SSO into a self-hosted app, injecting/forwarding the user's identity into HTTP requests,
  per-request access audit). If the user asks how to carry IdP identity *into* an app, or to
  audit app access per user, load it.
- **→ twingate-troubleshoot**: when the user reports access failures tied to policy
  misconfiguration, device trust, group sync, or SCIM errors
- **→ twingate-dns-security**: for DNS Security Profiles, exit networks, and per-group
  internet filtering — separate from access security policies
- **→ twingate-api**: when the real task is scripting the Admin GraphQL API rather than
  designing the identity model

## References

See [`references/`](./references/) for the current corpus, refreshed weekly. Three kinds
of file live there:

- **`{slug}.md`** — summaries of `twingate.com/docs` pages (product documentation).
- **`{numeric-id}-{slug}.md`** — Twingate help-center articles: symptom-shaped support
  content, exact error strings, and per-IdP gotchas.
- **`gh-{org}-{repo}.md`** — summaries of public Twingate GitHub repos: SE and community
  tooling, reference implementations, and automation.

| If the user asks about… | Read first |
|---|---|
| General IdP overview, choosing an IdP | `identity-providers.md`, `identity-provider-setup.md` |
| Okta SAML / SCIM | `okta-configuration.md`, `okta-app-configuration.md`, `okta-scim-configuration.md`, `saas-app-gating-with-okta.md` |
| Entra ID SAML / SCIM, Office 365 gating | `entra-id-configuration.md`, `entra-id-app-gating-office-365.md`, `saas-app-gating-with-entra-id.md` |
| Google Workspace SAML / SCIM | `google-workspace-configuration.md`, `saas-app-gating-with-google-workspace.md` |
| JumpCloud SAML / SCIM | `jumpcloud-configuration.md`, `saas-app-gating-with-jumpcloud.md` |
| OneLogin SAML / SCIM | `onelogin-configuration.md`, `onelogin-configuration-scim.md`, `saas-app-gating-with-onelogin.md` |
| Keycloak | `keycloak-configuration.md` |
| Active Directory | `using-active-directory-with-twingate.md` |
| SCIM endpoint, provisioning API, attribute mapping | `scim-provisioning-api.md` |
| Security policies (overview, design, migration, sign-in) | `security-policies.md`, `security-policies-best-practices.md`, `security-policy-guides.md`, `security-policies-migration-guide.md`, `sign-in-policy.md` |
| MFA / 2FA enforcement | `two-factor-authentication.md`, `two-factor-authentication-security-policies.md` |
| Device trust (overview, posture checks, managed devices) | `trusted-devices.md`, `device-posture-checks.md`, `managed-devices.md`, `device-security-guide.md`, `windows-managed-devices.md`, `manually-verified-devices.md`, `managing-devices.md`, `device-failures.md`, `devices.md`, `device-only-resource-policies.md` |
| MDM / EDR integration (native, per-vendor) | `jamf-configuration.md`, `jamf-mdm.md`, `kandji-configuration.md`, `kandji-mdm.md`, `iru-configuration.md`, `iru-mdm.md`, `intune-configuration.md`, `omnissa-workspace-one-mdm.md`, `crowdstrike-configuration.md`, `sentinelone-configuration.md`, `1password-configuration.md` |
| **Automating device trust from an MDM/EDR inventory** — bridge/middleware for FleetDM, Automox, JumpCloud, Mosyle, Datto RMM and others; sets `isTrusted` via the API | `gh-twingate-solutions-twingate-mdm-connector.md` |
| **Migrating group→resource access between IdPs** (fuzzy group matching, dry-run, rollback) | `gh-twingate-solutions-idp-migrator.md` |
| **Self-service group access via Slack** (profiles, approval workflows, time-bound) | `gh-twingate-labs-tg-group-profile-manager.md`, `gh-twingate-labs-tg-group-profile-manager-helm.md` (Helm deploy) |
| **Location-based group switching** (office vs. remote; experimental template) | `gh-twingate-solutions-twingate-wayfinder-app.md` |
| **SAML SP reference implementation** (Django + pysaml2, JumpCloud IdP) | `gh-twingate-labs-saml_service_provider.md` |
| JIT / ephemeral access, contractor patterns | `jit-access-requests.md`, `resources-reviewing-access-requests.md`, `ephemeral-access-to-resources.md`, `vendor-and-contractor-access-management.md`, `usage-based-auto-lock.md` |
| Groups, users, admins, offboarding | `groups.md`, `users.md`, `admins.md`, `offboarding-users.md` |
| Authentication, sessions, social logins | `authentication.md`, `how-sessions-work.md`, `social-logins.md` |
| Service accounts | `service-accounts-guide.md` |
| SaaS app gating | `saas-app-gating.md`, `saas-app-gating-best-practices.md` |
| Entra ID login anomalies (unassigned users can log in; social login "no matching user") | `4707021810-entra-id-all-users-are-able-to-log-into-twingate-even-though-they-are-not-assigned.md`, `4139538626-microsoft-social-logins-fail-with-an-entraid-account-there-is-no-matching-user-in-this-tenant.md` |

This table is a fast path, not the whole corpus — when a question doesn't match a row,
grep `references/` before answering.
