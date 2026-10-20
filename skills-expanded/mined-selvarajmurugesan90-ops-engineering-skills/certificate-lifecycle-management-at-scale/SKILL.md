---
name: certificate-lifecycle-management-at-scale
description: >
  Guides managing TLS/mTLS certificate lifecycle across many services and
  environments beyond a single Kubernetes cluster — enterprise CA
  integration (ACME private CA, Microsoft AD CS, cloud-managed private
  CAs), cross-service rotation automation, expiry monitoring/alerting,
  and CA hierarchy/trust-chain management for a mixed fleet of VMs,
  on-prem servers, and multiple clusters. Use when the user asks to
  "automate cert rotation across our whole fleet," "integrate with our
  enterprise CA," "why do we keep having certificate expiry outages,"
  "design a CA hierarchy for the org," "track every certificate's expiry
  date across environments," or "cert-manager only covers our Kubernetes
  clusters, what about everything else." Distinct from cert-manager's
  Kubernetes-native scope — see
  `../../../kubernetes-platform/skills/cert-manager-tls-automation/SKILL.md`.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: security-scanning-tooling
  maturity: stable
---

# Certificate Lifecycle Management at Scale

## Purpose

An expired certificate is one of the most preventable outages in
production — the fix (renew it) is trivial, but the failure mode (a
service silently stops accepting connections at exactly midnight on
expiry, with no gradual degradation to warn anyone) is brutal, and it
recurs constantly because certificate expiry is invisible until it
happens. [cert-manager-tls-automation](../../../kubernetes-platform/skills/cert-manager-tls-automation/SKILL.md)
solves this well *inside* a single Kubernetes cluster via a
reconciliation loop, but most enterprises have a fleet that isn't just
Kubernetes: VMs, on-prem load balancers, network appliances, multiple
clusters across clouds, and internal services trusting an enterprise CA
(Microsoft AD CS, a cloud-managed private CA, or a hand-rolled internal
root) rather than a public ACME CA. This skill covers that broader
scope — integrating with an enterprise/internal CA as the trust root,
automating rotation across a heterogeneous fleet where no single
Kubernetes controller has visibility, building expiry monitoring that
covers every certificate regardless of where it lives, and designing a
CA hierarchy (root/intermediate/issuing tiers) that scales across many
teams and services without becoming an unmanageable sprawl of
independently-issued, independently-tracked certificates.

## When to use

- Standing up or reviewing an enterprise CA hierarchy (root, one or more
  intermediate/issuing CAs) that will back internal TLS/mTLS across many
  services, not just one Kubernetes cluster.
- Integrating a fleet's certificate issuance with an enterprise CA —
  Microsoft Active Directory Certificate Services (AD CS), a cloud
  provider's private CA service (AWS Private CA, Google CA Service,
  Azure Key Vault-integrated CA), or HashiCorp Vault's PKI engine used
  as the org-wide issuing point (see
  [vault-operations-and-pki-engine-configuration](../vault-operations-and-pki-engine-configuration/SKILL.md)
  for operating that engine itself).
- Automating certificate rotation across a mixed fleet — VMs, on-prem
  appliances, multiple Kubernetes clusters, load balancers — where no
  single cluster-scoped controller has visibility into every
  certificate.
- Building or improving fleet-wide certificate expiry monitoring and
  alerting, so an expiring cert is caught weeks ahead rather than
  discovered as an outage.
- Investigating a recurring pattern of expiry-related outages and
  wanting a systemic fix (inventory, automation, alerting) rather than
  repeatedly firefighting the next individual expiry.
- Migrating certificate issuance off manual/ad hoc processes (a shared
  spreadsheet of expiry dates, a person who "just remembers") onto an
  automated, auditable pipeline.
- Deciding the right split between cert-manager (for in-cluster
  Kubernetes workloads) and enterprise-CA-integrated automation (for
  everything else) in an org with both.

## Prerequisites & environment

- Clarity on the CA hierarchy already in place (or to be built): a
  **root CA** (rarely used, ideally offline/HSM-backed), one or more
  **intermediate/issuing CAs** that actually sign leaf certificates day
  to day, and — critically — an accurate inventory of which
  intermediate signs for which environment/business unit. A
  "hierarchy" that is actually one flat root signing everything
  directly is a design gap to fix, not a starting point to build
  automation on top of.
- Administrative access to the chosen enterprise CA integration point:
  AD CS's Certificate Enrollment Web Services / `certreq` for Windows-
  centric fleets, a cloud private CA's API/IAM permissions (AWS Private
  CA's `IssueCertificate` action, GCP CA Service's issuer pool), or
  Vault's PKI engine API if Vault is the org's chosen internal CA.
- An inventory mechanism — even a lightweight one — covering every
  certificate in scope: hostname/SAN, issuing CA, expiry date, and an
  owning team, before automating anything. Automation applied to an
  incomplete inventory just automates the certificates someone
  remembered to list.
- A distribution/rotation mechanism appropriate to each fleet segment:
  a configuration management tool (Ansible/Puppet/Chef) pushing renewed
  certs to VMs and appliances, `cert-manager` for in-cluster Kubernetes
  workloads, and a scripted ACME/CA-API client for anything else (load
  balancers, network appliances without native ACME support).
- Monitoring/alerting infrastructure (Prometheus + a blackbox/certificate
  exporter, a dedicated certificate-monitoring SaaS, or a scheduled
  script) capable of checking expiry across every certificate in the
  inventory, not just the ones already covered by an in-cluster
  controller.
- Change-management awareness for anything issued from a shared
  enterprise CA — a compromised or misissued intermediate affects every
  certificate it has ever signed, so intermediate-level changes (new
  intermediate, revocation, key rotation) need broader review than a
  single service's certificate renewal.

## Step-by-step guidance

1. **Build (or validate) the CA hierarchy before automating rotation on
   top of it.** A minimum viable enterprise hierarchy is root →
   environment-scoped intermediate(s) (e.g. one for production, one for
   internal/dev) → leaf certificates, never leaf certificates signed
   directly by the root:
   ```
   Enterprise Root CA (offline, HSM-backed, years-long validity)
     └── Production Issuing CA (online, signs leaf certs for prod services)
     └── Internal/Dev Issuing CA (online, signs leaf certs for non-prod)
   ```
   If the org already runs Vault's PKI engine for internal issuance, its
   intermediate ([vault-operations-and-pki-engine-configuration](../vault-operations-and-pki-engine-configuration/SKILL.md))
   can itself be the "Production Issuing CA" node — this skill is about
   scaling rotation and inventory *across* however many issuing points
   like that the org has, not replacing them.

2. **Integrate with the enterprise CA's issuance API** rather than a
   manual certificate-request form per service. Microsoft AD CS example
   (via its REST-like enrollment web service or `certreq` scripted
   against a certificate template):
   ```powershell
   # certreq against an AD CS certificate template (illustrative)
   certreq -submit -config "ca-server\Production-Issuing-CA" `
     -attrib "CertificateTemplate:WebServerAutomated" request.csr cert.crt
   ```
   AWS Private CA example (API-driven, suitable for scripting across a
   fleet):
   ```bash
   aws acm-pca issue-certificate \
     --certificate-authority-arn arn:aws:acm-pca:us-east-1:<AWS_ACCOUNT_ID>:certificate-authority/<CA_ID> \
     --csr fileb://service.csr \
     --signing-algorithm SHA256WITHRSA \
     --validity Value=90,Type=DAYS
   ```
   Both patterns are automatable from a central rotation pipeline rather
   than a human filling out a request form per certificate.

3. **Build a fleet-wide certificate inventory as the source of truth**,
   populated from active scanning plus CA-issuance records rather than
   trusted to a manually maintained list:
   ```bash
   # Illustrative: scan a list of known endpoints for cert expiry,
   # feeding a central inventory (a small script, not a heavyweight tool)
   for host in $(cat fleet_endpoints.txt); do
     expiry=$(echo | openssl s_client -connect "${host}:443" -servername "${host}" 2>/dev/null \
       | openssl x509 -noout -enddate | cut -d= -f2)
     echo "${host},${expiry}"
   done >> cert_inventory.csv
   ```
   Cross-reference this active-scan inventory against the issuing CA's
   own issuance log/database — a certificate the scan can't reach
   (internal-only, firewalled) still needs to appear in inventory via
   the CA's records, and a certificate the CA issued but that scanning
   finds already replaced flags a stale or orphaned inventory entry.

4. **Automate rotation per fleet segment, matched to that segment's
   deployment mechanism** — there is no single tool that reaches VMs,
   appliances, and multiple Kubernetes clusters uniformly:
   - **Kubernetes workloads:** `cert-manager` per cluster remains the
     right tool — see
     [cert-manager-tls-automation](../../../kubernetes-platform/skills/cert-manager-tls-automation/SKILL.md) —
     configured with an `Issuer`/`ClusterIssuer` pointed at the
     enterprise CA (Vault PKI backend, or a cert-manager
     `venafi-issuer`/ACME-fronted enterprise CA integration where
     available) rather than a public ACME CA.
   - **VMs/on-prem servers:** a configuration management run (Ansible
     example) that requests renewal ahead of `renewBefore`-equivalent
     margin and redeploys the cert + reloads the consuming service:
     ```yaml
     # ansible playbook task (illustrative)
     - name: renew certificate if within 30 days of expiry
       when: cert_days_remaining | int < 30
       block:
         - name: request renewed cert from enterprise CA
           command: >
             certreq -submit -config "ca-server\Production-Issuing-CA"
             {{ csr_path }} {{ cert_path }}
         - name: reload nginx to pick up renewed cert
           systemd:
             name: nginx
             state: reloaded
     ```
   - **Network appliances/load balancers without native ACME/API
     support:** a scripted client calling the CA's API and pushing the
     result via the appliance's own management API/SSH, run on a
     schedule well ahead of expiry.

5. **Set `renewBefore`-equivalent margins deliberately per fleet
   segment**, accounting for the segment's actual deployment lead time
   — a VM fleet needing a change-management-approved deployment window
   needs a longer lead time than an automated Kubernetes reconcile loop:
   ```
   Kubernetes (cert-manager, automated reconcile): renew 15-30 days before expiry
   VM fleet (config-management run, may need a change window): renew 45-60 days before expiry
   Network appliances (manual-adjacent, longer lead time): renew 60-90 days before expiry
   ```

6. **Alert on expiry as a first-class, fleet-wide signal**, independent
   of whether automation is expected to have already renewed it —
   automation failing silently is exactly the case alerting exists to
   catch:
   ```yaml
   # Prometheus alerting rule using a blackbox/certificate exporter
   - alert: CertificateExpiringSoon
     expr: probe_ssl_earliest_cert_expiry - time() < 30 * 86400
     for: 1h
     labels: { severity: warning }
     annotations:
       summary: "Certificate for {{ $labels.instance }} expires in under 30 days"
   - alert: CertificateExpiringCritical
     expr: probe_ssl_earliest_cert_expiry - time() < 7 * 86400
     for: 1h
     labels: { severity: critical }
     annotations:
       summary: "Certificate for {{ $labels.instance }} expires in under 7 days — page on-call"
   ```
   Route the critical-tier alert into the paging tool's escalation
   policy (see
   [pagerduty-and-opsgenie-oncall-configuration](../../../incident-tooling-and-itsm/skills/pagerduty-and-opsgenie-oncall-configuration/SKILL.md)),
   not just a dashboard — an expiry alert nobody's paged for is no
   better than no alert.

7. **Plan and rehearse intermediate/root CA rotation** as a
   fleet-wide, high-blast-radius event, distinct from routine leaf
   certificate renewal:
   ```
   1. Generate/sign new intermediate under the (offline) root.
   2. Distribute the new intermediate + updated trust chain to every
      consuming service/trust store *before* any leaf cert is issued
      from it — a leaf signed by an intermediate no one trusts yet is a
      guaranteed outage.
   3. Begin issuing new leaf certificates from the new intermediate.
   4. Only after every leaf certificate has rotated onto the new chain,
      retire trust in the old intermediate.
   ```
   > **Warning:** rotating or revoking an intermediate CA before every
   > downstream trust store has the new chain is a fleet-wide outage
   > risk, not a routine change — treat it with the same rehearsal
   > discipline as a Vault seal migration (see
   > [vault-operations-and-pki-engine-configuration](../vault-operations-and-pki-engine-configuration/SKILL.md)),
   > including a non-production rehearsal and a documented rollback
   > plan, before touching a production root/intermediate.

8. **Reconcile CA-issued certificate records against actual CRL/OCSP
   revocation status periodically**, so a revoked certificate (e.g.
   after a suspected key compromise) is confirmed to actually be
   rejected by consuming services, not just marked revoked in the CA's
   database:
   ```bash
   openssl ocsp -issuer intermediate.crt -cert leaf.crt \
     -url http://ocsp.example.internal -CAfile chain.pem
   ```

## Best practices

- Never issue leaf certificates directly from a root CA at any point in
  the fleet — always through at least one intermediate, keeping the
  root itself as rarely-used/offline as operationally feasible.
- Build the fleet-wide inventory before automating rotation — automating
  renewal for the certificates you already know about does nothing for
  the ones inventory is missing, and those are exactly the ones that
  cause surprise outages.
- Match rotation automation to each fleet segment's actual deployment
  mechanism and lead time (Kubernetes reconcile loop vs. a
  change-managed VM deployment window) rather than assuming one
  `renewBefore` value fits every environment.
- Alert on expiry independently of whether automation "should" have
  already handled it — a silent automation failure is precisely the
  scenario expiry alerting exists to catch, and it should page, not just
  log.
- Treat intermediate/root CA rotation as a rehearsed, fleet-wide event
  with a distribution-before-issuance ordering, never a routine change
  applied directly to production.
- Prefer a single enterprise CA integration point (Vault PKI, AD CS, or
  a cloud private CA) that every fleet segment issues from, over
  multiple independently-managed CAs per team — consolidated issuance
  is what makes a single fleet-wide inventory and monitoring approach
  actually complete.
- Cross-reference active-scan-based inventory against the CA's own
  issuance log — either source alone can miss certificates the other
  would catch (an internal-only host active scanning can't reach; a
  certificate issued but never actually deployed).

## Common pitfalls

- **Symptom:** A production outage occurs at exactly midnight with no
  warning, traced to a certificate that expired — and it turns out
  nobody had that host in the monitored inventory at all.
  **Fix:** This is an inventory gap, not a monitoring-tool failure —
  build inventory from both active scanning and the issuing CA's own
  records (step 3), and treat "certificate not in inventory" the same
  as any other unmanaged-asset finding, since automation and alerting
  built on an incomplete inventory only ever protects what's already
  known.

- **Symptom:** A new intermediate CA is issued and starts signing leaf
  certificates immediately, but a subset of consuming services rejects
  every certificate signed by it with a trust-chain error.
  **Fix:** The new intermediate's chain wasn't distributed to every
  consuming trust store before issuance began. Always distribute the
  new chain fleet-wide first, confirm it's trusted everywhere, and only
  then begin issuing leaf certificates from the new intermediate (step
  7's ordering).

- **Symptom:** A VM fleet's certificate renewal automation runs, but a
  renewed certificate sits on disk unused because the consuming service
  (nginx, an appliance) was never reloaded/restarted to pick it up, and
  the old certificate still expires on schedule.
  **Fix:** Rotation automation must include the reload/restart step for
  every consuming service, not just the file replacement — verify
  post-renewal that the live-serving certificate (via `openssl s_client`
  against the actual endpoint) matches the renewed one, not just that a
  new file exists on disk.

- **Symptom:** Different teams have each stood up their own small
  internal CA over time (a self-signed root here, a Vault PKI mount
  there), and there's no single place to answer "what's our total
  certificate expiry exposure this month."
  **Fix:** Consolidate onto a single enterprise CA integration point
  going forward, and treat existing shadow CAs as a migration backlog —
  fragmented issuance points are the root cause of an incomplete,
  unreliable fleet-wide inventory.

- **Symptom:** A certificate is revoked in the CA's records after a
  suspected private-key compromise, but a consuming service continues
  accepting connections using it for days afterward.
  **Fix:** Confirm CRL/OCSP distribution is actually configured and
  reachable by consuming services (step 8), and that those services
  check revocation status rather than only validating the certificate
  chain and expiry — a CA-side revocation record with no enforced
  distribution mechanism doesn't actually stop anything from trusting
  the revoked certificate.

## Worked example

**Scenario:** An enterprise runs three fleet segments — 40 Kubernetes
clusters across two clouds, ~300 VMs running internal services, and a
dozen on-prem load balancers — all needing certificates trusted under
one enterprise root, with fleet-wide expiry monitoring after a recent
outage caused by an unmanaged VM's certificate expiring unnoticed.

1. CA hierarchy consolidated onto Vault's PKI engine as the single
   Production Issuing CA, itself signed by an offline enterprise root
   (see
   [vault-operations-and-pki-engine-configuration](../vault-operations-and-pki-engine-configuration/SKILL.md)
   for that setup).

2. Kubernetes clusters: each cluster's cert-manager `ClusterIssuer` is
   pointed at Vault's PKI engine instead of a public ACME CA:
   ```yaml
   apiVersion: cert-manager.io/v1
   kind: ClusterIssuer
   metadata: { name: vault-enterprise-ca }
   spec:
     vault:
       server: "https://vault.example.internal:8200"
       path: "pki_int/sign/production-services"
       auth:
         kubernetes:
           role: "cert-manager"
           mountPath: "/v1/auth/kubernetes"
   ```

3. VM fleet: an Ansible playbook run nightly checks each host's
   certificate expiry against a 45-day threshold, requests renewal from
   Vault's PKI `issue` endpoint, deploys the renewed cert, and reloads
   the consuming service — logging every action to the central
   inventory system.

4. Fleet-wide inventory reconciles active scan results (step 3 of the
   guidance) against Vault's PKI issuance log nightly, flagging any
   certificate present in one source but not the other for manual
   investigation — this is exactly how the previously-unmanaged VM
   (root cause of the earlier outage) gets caught this time, three
   weeks before its next certificate would have expired.

5. Prometheus alerting (step 6) fires a `warning` at 30 days and a
   `critical`, paging alert at 7 days for any certificate across all
   three fleet segments, routed through the existing on-call escalation
   policy.

Result: a single enterprise CA (Vault-backed), one consolidated
inventory covering all three fleet segments regardless of deployment
mechanism, and expiry alerting that pages on-call well before any
outage — rather than three independently-tracked, partially-automated
certificate populations.

## Cross-references

- [cert-manager-tls-automation](../../../kubernetes-platform/skills/cert-manager-tls-automation/SKILL.md) —
  the Kubernetes-native reconciliation piece this skill's fleet-wide
  scope wraps around; use cert-manager as-is for in-cluster workloads
  and point its `Issuer`/`ClusterIssuer` at the enterprise CA described
  here.
- [vault-operations-and-pki-engine-configuration](../vault-operations-and-pki-engine-configuration/SKILL.md) —
  operating the PKI engine that can serve as the enterprise CA's
  issuing point referenced throughout this skill.
- [enterprise-sso-and-idp-federation-configuration](../enterprise-sso-and-idp-federation-configuration/SKILL.md) —
  a comparable trust-chain expiry problem (IdP/SP signing certificates)
  in a different federation context.
- [pagerduty-and-opsgenie-oncall-configuration](../../../incident-tooling-and-itsm/skills/pagerduty-and-opsgenie-oncall-configuration/SKILL.md) —
  where fleet-wide expiry alerts should route so a critical-tier warning
  actually pages a human, not just logs to a dashboard.
