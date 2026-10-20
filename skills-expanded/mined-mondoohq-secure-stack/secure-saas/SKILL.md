---
name: secure-saas
description: Audit SaaS and identity-provider security posture — scan GitHub, GitLab, Okta, Google Workspace, Microsoft 365, Slack, Atlassian, and Snowflake with cnspec for access, MFA, sharing, and configuration risks, mapped to compliance. Use to check a SaaS tenant, org, or identity provider's settings.
allowed-tools: Bash Read
---

# Secure SaaS

Check whether a SaaS tenant or identity provider is configured securely, by running
[cnspec](https://github.com/mondoohq/cnspec) against its API. You ask "is our GitHub org / Okta
tenant / Google Workspace hardened?" and this skill picks the right scan; cnspec carries the policies.

## When to use

- Auditing a source-control org (GitHub / GitLab): branch protection, 2FA enforcement, repo
  visibility, token/app policies.
- Auditing an identity provider (Okta, Microsoft 365, Google Workspace): MFA, admin roles,
  session and sharing settings.
- Auditing collaboration / data SaaS (Slack, Atlassian, Snowflake) for access and config risks.

## What cnspec checks

- **Source control** — `mondoo-github-security`, `mondoo-github-best-practices`, `mondoo-gitlab-security`
- **Identity / productivity** — `mondoo-okta-security`, `mondoo-m365-security`, `mondoo-google-workspace-security`
- **Collaboration / data** — `mondoo-slack-security`, `mondoo-atlassian-security`, `mondoo-snowflake-security`

## Run a scan

```bash
cnspec scan github --organization <org>   -o sarif   # requires a GitHub token
cnspec scan okta                          -o sarif   # requires Okta org + API token
cnspec scan ms365                         -o sarif   # requires an Entra ID app registration
cnspec scan google-workspace              -o sarif   # requires a service account
cnspec scan slack                         -o sarif   # requires a Slack token
```

- Each provider authenticates with that SaaS's API credentials — the exact flags/env for token,
  org, and app registration are in the [cnspec docs](https://mondoo.com/docs/cnspec/) per provider.
- Logged in to Mondoo Platform, assigned policies run automatically; otherwise `--incognito -f <bundle>`.
- `-o sarif` for a CI gate; cnspec exits non-zero on failures.

## Reference, don't duplicate

cnspec owns the policies and authoring (see the
[cnspec repo](https://github.com/mondoohq/cnspec/tree/main/skills)). This skill invokes cnspec
and interprets results — it does not reimplement policy.

## Compliance

SaaS policies map to CIS benchmarks (where published), SOC 2, ISO 27001, and vendor best
practices — a scan doubles as a compliance check.

## Part of the secure-your-stack toolkit

`secure-saas` is the **SaaS & identity** pillar of posture, alongside `secure-os` (hosts),
`secure-cloud` (cloud accounts), and `secure-ai-services` (AI). Needs `cnspec`
([install](https://mondoo.com/docs/cnspec/install)) plus API credentials for the target SaaS.
