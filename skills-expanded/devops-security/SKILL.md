---
name: devops-security
description: "Securing pipelines and infrastructure: secrets management and rotation, scanning for leaked secrets, the software supply chain (lockfiles, pinned actions, SBOMs, signed images), least-privilege identities, network exposure, TLS everywhere, hardened containers, encrypted backups, audit logs, and incident basics. Read before touching secrets, IAM, CI permissions or anything exposed to the internet."
---

# Securing pipelines and infrastructure

The generated setup keeps an administrator access key in a CI secret and on a
laptop, a `.env` with production values committed "for now", actions pinned to
tags anyone with the maintainer's token can move, `npm install` running every
package's install script, Postgres and Redis on public IPs behind a firewall
that Docker quietly bypasses, SSH open to the world with passwords, and backups
in the same account an attacker now controls. This is how to keep secrets out
of reach, the build chain honest, identities narrow and exposure small, and
what to do when something leaks. App-level rules (injection, uploads,
headers) are in `backend-security`. One part of devops; the whole is in the
`devops` skill.

## 1. Secrets

- One app: the platform's secret variables (GitHub environments, Vercel, Fly,
  Render, Coolify). Several services or people: a manager (AWS Secrets
  Manager or SSM Parameter Store, Google Secret Manager, Azure Key Vault,
  Vault or OpenBao, Infisical, Doppler, 1Password with `op run`).
- Injected at runtime as variables or mounted files; never in an image, the
  repository, a URL, a log or a report.
- Scoped per environment: production secrets readable by production
  workloads and a few people, reached from CI only through protected
  environments (`devops-ci`).
- In git only encrypted, and only when they must live there: SOPS with age or
  KMS, Sealed Secrets for Kubernetes; the decryption key lives elsewhere.
- `.env` in `.gitignore`; `.env.example` committed with every name, a
  comment and no real value.
- Short-lived beats rotated: OIDC tokens for CI, workload identity for
  services, dynamic database credentials (Vault), RDS-managed passwords
  (rotated every 7 days by default). What must stay static is rotated on a
  schedule, when someone leaves, and on any suspicion; accept old and new
  keys together during a rotation so it needs no downtime.

## 2. Leaks: prevention and response

- Scan before it lands: gitleaks as a pre-commit hook
  (`gitleaks git --pre-commit --redact --staged`) and over the whole history
  once (`gitleaks git --redact`); GitHub secret scanning with push protection
  on for the organisation; `trufflehog git file://. --results=verified` to find
  the ones that still work.
- When a secret leaks (pushed to any remote, pasted in a ticket, printed in a
  CI log, shipped in a bundle or an image):
  1. Revoke or rotate it at once. Bots read public pushes within minutes, and
     deleting the commit does not unpublish it.
  2. Check the provider's logs for use since the leak (CloudTrail, the API's
     key usage, database connections).
  3. Put the new value everywhere the old one was used and redeploy.
  4. Then clean history (`git filter-repo --replace-text`, force-push, ask
     GitHub to purge cached views); forks and clones keep it, which is why
     step 1 comes first.
  5. Close the path it took (a hook, a scanner rule, a `.gitignore` line).
- An agent that finds a secret reports the file, the line and whether it
  looks live, never the value.

## 3. Supply chain

- Lockfiles committed and installed frozen (`npm ci`,
  `pnpm install --frozen-lockfile`, `uv sync --locked`,
  `cargo build --locked`, `go mod verify`).
- Install scripts run code: pnpm runs dependency lifecycle scripts only for
  packages you allow (`allowBuilds` since pnpm 11); with npm, consider
  `--ignore-scripts` in CI and rebuild the few that need it.
- A minimum release age lets registries pull a compromised version before
  you install it: pnpm 11 and later default `minimumReleaseAge` to one day;
  Renovate's `config:best-practices` waits 3 days for npm, and 14 days is
  sensible where updates merge automatically.
- Renovate or Dependabot with grouped updates, automerge only for passing
  minor and patch updates of development tools, weekly lockfile maintenance.
- Pinned by content, not by name: CI actions by commit SHA (the
  `tj-actions/changed-files` tags in March 2025 and 76 of 77
  `aquasecurity/trivy-action` tags in March 2026 were rewritten to steal CI
  secrets), downloaded tools by version and checksum (`sha256sum -c`), base
  images by digest.
- Scan: `osv-scanner scan source -r .` for dependencies, `trivy image` or
  `grype` for images, `npm audit signatures` for registry signatures and
  provenance. Fail CI on fixable high and critical findings; give the rest an
  owner and a date. Pin the scanners too: Trivy's own release was
  compromised in the same attack.
- An SBOM per release (`syft <image> -o cyclonedx-json`, or BuildKit's
  `--sbom=true`) kept with it.
- Provenance and signatures, keyless from CI (`id-token: write`):
  `actions/attest-build-provenance`, checked with
  `gh attestation verify oci://ghcr.io/acme/shop@sha256:<digest> --owner acme`,
  or cosign:

```sh
cosign sign --yes ghcr.io/acme/shop@sha256:<digest>
cosign verify ghcr.io/acme/shop@sha256:<digest> \
  --certificate-identity-regexp '^https://github.com/acme/shop/.github/workflows/release.yml@refs/tags/v' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
```

  A cluster can refuse unsigned images with Kyverno or the Sigstore policy
  controller.
- Publish packages through trusted publishing (OIDC) on npm and PyPI, with
  provenance and 2FA for maintainers. npm revoked all classic tokens in
  December 2025 and limits write tokens to 90 days.
- OpenSSF Scorecard (`scorecard --repo=github.com/acme/shop`) lists the gaps
  in your own repositories.

## 4. Identities

- People: SSO with MFA everywhere that matters (cloud, GitHub, registrar, DNS,
  password manager), hardware keys or passkeys for admins, no shared
  accounts, access reviewed each quarter and removed the day someone leaves.
- No long-lived cloud keys: IAM Identity Center for people, OIDC roles for
  CI, task and instance roles or workload identity for services (Google
  workload identity federation, Azure managed identities). An IAM user with
  an access key is a finding.
- Least privilege per service: its own role, named actions on named
  resources; separate plan (read) and apply (write) roles for IaC;
  production in its own account or project, with organisation policies as
  guard rails (no disabling CloudTrail, an allowed-regions list).
- Break-glass: one or two emergency admin accounts with hardware MFA,
  credentials sealed away, every use raising an alert.
- The registrar and DNS accounts are as critical as the cloud root: MFA and a
  registrar lock.

## 5. Network exposure

- Closed by default: databases, caches, queues, admin interfaces and internal
  services on private networks; the public surface is the proxy or load
  balancer on 80 and 443 (UDP 443 too for HTTP/3).
- Firewalls and security groups name ports and sources; `0.0.0.0/0` only on
  80 and 443.
- Docker publishes ports through its own firewall rules, ahead of ufw and
  firewalld: `-p 5432:5432` is reachable from the internet even when ufw
  denies 5432. Publish to `127.0.0.1`, use internal networks without
  published ports, or filter in the `DOCKER-USER` chain.
- Never on the internet: the Docker socket or API (2375, 2376: root on the
  host), Redis, MongoDB, Elasticsearch, Postgres, and dashboards (Grafana,
  Portainer, pgAdmin, Coolify, Kubernetes) without SSO. Put admin surfaces
  behind Tailscale, Cloudflare Access or a cloud identity-aware proxy.
- SSH keys only, no root login, or no SSH at all (SSM Session Manager,
  Tailscale SSH):

```text
# /etc/ssh/sshd_config.d/10-hardening.conf
PasswordAuthentication no
KbdInteractiveAuthentication no
PermitRootLogin no
AllowUsers deploy
MaxAuthTries 3
```

  Run `sshd -t`, reload, and keep a second session open until a new login
  works. fail2ban or CrowdSec for what stays exposed; automatic security
  updates (`unattended-upgrades`) on every host.
- At the edge: WAF rules and rate limits on sign-in, APIs and expensive
  endpoints, and the origin locked to the CDN (its IP ranges, authenticated
  origin pulls, or a tunnel) so nobody goes around it (`devops-networking`).
- Hosts that need no internet get no egress; sensitive ones get an allow-list.

## 6. In transit, in containers, at rest

- HTTPS everywhere with HSTS, automatic renewal and expiry alerts, TLS 1.2 at
  least (`devops-networking`). Database connections verify the server
  (`sslmode=verify-full` with the provider's CA; `require` encrypts but
  trusts anyone). mTLS through a mesh or Tailscale where the network is not
  trusted.
- Containers non-root with a read-only root filesystem, all capabilities
  dropped, no privilege escalation, the runtime's default seccomp; no
  `privileged`, host network or host path mounts; the Docker socket only in a
  trusted proxy that needs it, read-only or behind a socket proxy
  (`devops-containers`, `devops-kubernetes`).
- Disks, buckets, databases and snapshots encrypted with managed keys;
  buckets private with public access blocked at the account level.

## 7. Backups

- 3-2-1: three copies, two kinds of storage, one off-site in another account
  or provider; encrypted (restic, pgBackRest, WAL-G); immutable (S3 Object
  Lock, an append-only restic repository), so production credentials cannot
  delete them.
- Backup credentials can write but not delete, and are not the production
  credentials.
- Restores tested monthly for the main database, timed and written down; an
  untested backup is a hope. Retention follows the law and the business
  (daily for 30 days, monthly for a year is common); personal data in backups
  ages out too.

## 8. Audit logs

- The cloud control plane: an organisation-wide CloudTrail in every region,
  delivered to a separate log account with file validation; Google Cloud's
  Admin Activity logs are always on, Data Access logs are off until enabled;
  Azure's Activity Log keeps 90 days unless exported.
- Also the GitHub organisation audit log, Kubernetes audit logs, database
  logins and DDL, the secret manager's access log and SSO sign-ins.
- Kept a year or more where compliance asks, out of reach of the people
  audited, with alerts on rare events: root sign-in, MFA removed, a new admin,
  logging stopped, a secret read by an unusual identity.

## 9. Incidents

1. Declare it: one incident lead, one channel, a timeline from the start.
2. Contain: revoke keys, block the account or address, isolate the host
   (snapshot it for forensics before rebuilding), take the feature offline.
3. Eradicate and recover: patch, rotate everything the attacker could reach,
   restore from clean backups, watch for a return.
4. Communicate honestly on the status page and to customers. Regulators run
   on a clock: under GDPR, 72 hours to the supervisory authority once aware
   of a personal data breach; under Indonesia's UU PDP, written notice within
   3 x 24 hours to the people affected and the authority.
5. A blameless post-mortem within a week: timeline, impact, contributing
   causes, actions with owners and dates.

## Check it

- `gitleaks git --redact` and `trufflehog git file://. --results=verified`: no
  live secrets anywhere in history.
- `osv-scanner scan source -r .`, a pinned `trivy image --severity
  HIGH,CRITICAL <image>`, `pinact run --check`, `uvx zizmor .github/workflows`.
- On a host you are responsible for, from outside:
  `nmap -Pn --top-ports 1000 <public-ip>` shows only the ports you meant; on
  the host, `ss -tlnp` shows internal services bound to `127.0.0.1` or
  private addresses.
- `aws iam list-users` and `aws iam list-access-keys --user-name <user>`: no
  active keys for people or apps; `kubectl auth can-i --list` for CI
  identities.
- The last restore test is recorded with its date, duration and result.

## Avoid

Long-lived cloud keys in CI or on laptops; secrets in git, images, logs or
reports; deleting a leaked secret's commit instead of rotating it first;
actions and base images pinned by tag; install scripts from every package;
brand-new releases installed within hours; scanners left unpinned; databases,
caches, the Docker API or admin panels on the internet; trusting ufw with
published Docker ports; SSH with passwords or root login; backups the
production account can delete, or never restored; audit logs off or in reach
of the people they audit; an incident with no lead and no timeline.
