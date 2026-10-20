---
name: certificate-automation
description: "Move a certificate estate onto automated ACME issuance and renewal ahead of the CA/Browser Forum's shrinking maximum lifetimes. Inventory from outside first — CT logs and endpoint scans, not only what the team tracks — because the one nobody owns is the risk. Classify endpoints as native-ACME, cert-manager, cloud-managed, or an appliance that cannot automate, then automate renewal on ACME Renewal Information where supported and a lifetime-fraction backstop otherwise, and alert on renewal failure, not the clock alone. Use for an ACME rollout, a certificate inventory, a schedule ahead of a validity cut, or an appliance stuck on manual renewal. Not for a leaked or compromised certificate or key (secret-rotation), whether an expiry alert pages or tickets (alert-design), a Terraform diff on a certificate resource (iac-review), or migrating the CA or PKI vendor (plan-platform-migration)."
allowed-tools: "Bash(openssl:*), Bash(certbot:*), Bash(kubectl:*), Bash(aws:*), Bash(gcloud:*), Bash(az:*), Bash(curl:*), Bash(jq:*), Read, Grep, Glob"
---

# Certificate Automation

A finished migration is one where no certificate in the estate is renewed by a person, expiry is monitored from outside the renewal path rather than trusted to it, and the schedule already accommodates the shortest maximum validity the Baseline Requirements will permit before the next renewal comes due.

The job is hard because the deadline moves under you. Ballot SC-081, adopted 2025-04-11, cuts maximum TLS certificate validity from 398 days to 200 days from 2026-03-15, 100 days from 2027-03-15 and 47 days from 2029-03-15 — and cuts how long domain-validation evidence can be reused on the same dates, to 200, then 100, then 10 days. A manual renewal process that just barely worked at 398 days does not degrade gracefully as the interval shrinks; it fails outright, because the person who used to get a calendar reminder every year now needs one every six weeks, and nobody scales a manual process that way on purpose. The other reason it is hard is that the estate is never what the inventory says it is: a certificate issued by someone who left, an appliance nobody remembers is internet-facing, a wildcard covering a subdomain spun up for a demo — none of those show up until something outside the organization finds them first, usually a browser warning or a certificate-transparency log.

## Scope

Use for: inventorying an estate's TLS certificates including the ones nobody has tracked; deciding which endpoints can run ACME directly, via cert-manager, via a cloud-managed certificate service, or not at all; standing up automated issuance and renewal with a monitored failure mode; setting a renewal schedule that survives the 2026–2029 validity cuts; and building a runbook for the appliances that cannot automate.

Do not use for: rotating or containing a certificate or private key that has already leaked or is suspected compromised — that is an incident, and `secret-rotation` owns it; deciding whether a certificate-expiry signal should page or only ticket — that is `alert-design`'s classification, not this skill's; reviewing a Terraform or OpenTofu diff that happens to touch a certificate resource — that is `iac-review`; or replacing the CA or PKI vendor itself as a project — that is `plan-platform-migration`. This skill assumes the CA and the endpoints are trusted and intact; it automates keeping them current.

## Hard gates

1. **No endpoint may depend on a certificate lifetime longer than the renewal schedule allows.** The estate's slowest renewal process sets the floor, not the CA's current ceiling — an appliance that can only be updated during a quarterly maintenance window cannot run on a certificate that expires in 47 days, and that has to be fixed before 2029-03-15, not discovered on it.
2. **Inventory from outside the organization before trusting what the team believes it runs.** Certificate-transparency logs and an external endpoint scan find what internal knowledge misses. A certificate nobody owns is the finding, not a footnote.
3. **A leaked or compromised certificate or key is an incident, not a renewal.** Stop here and hand it to `secret-rotation`; issuing a replacement on the normal schedule while the old key is still valid solves nothing.
4. **Every automated renewal path has a monitored failure mode.** A cron job or ACME client that renews silently also fails silently. Alerting on the certificate's expiry clock alone tells you the automation is late; it does not tell you the automation exists.
5. **Automate ahead of the deadline that forces it, not on it.** 2027-03-15 and 2029-03-15 are calendar dates known years in advance. An estate that starts automating the week validity drops is an estate that will miss the first renewal cycle under the new schedule.

## Workflow

### 0. Choose where this estate needs work

Most engagements need more than one of these, but they start from different evidence and end at different milestones. Decide which is missing before doing any of them.

| Signal | Classification | Start at |
| --- | --- | --- |
| "What certificates do we even have" cannot be answered from a single source of truth | Inventory | Step 1 |
| Certificates are known and tracked, but renewal is still a person running a command or clicking a console | Automation | Step 3 |
| Renewal is already automated, but nobody would notice a renewal failure before the certificate expired | Monitoring | Step 5 |
| An appliance or vendor product cannot run ACME at all | Endpoint playbook | `references/endpoint-playbooks.md` |

### 1. Inventory every certificate from the outside first

Start from evidence the organization does not control, then reconcile against what the team already tracks. The gap between the two is the actual risk.

```bash
# Certificate-transparency logs: every certificate ever issued for the domain and its subdomains,
# including the ones nobody on the team requested
curl -s "https://crt.sh/?q=%25.example.com&output=json" | jq -r '.[].name_value' | sort -u

# Confirm what is actually served today, not merely what was once issued
openssl s_client -connect host.example.com:443 -servername host.example.com </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates -ext subjectAltName

# Sweep a range you operate for anything answering TLS at all, including hosts nobody remembers standing up
nmap -p 443,8443 --open -oG - 10.0.0.0/16 | awk '/Up$/{print $2}'
```

`nmap` is deliberately left out of this skill's `allowed-tools`: it scans a network rather than reading one host, and that should prompt for confirmation of the range and authorization rather than run unattended.

Reconcile against the inventory your team maintains — cert-manager `Certificate` resources, the cloud account's certificate manager, the load balancer and CDN configuration, and any spreadsheet still being used as the source of truth. Anything present in the CT log or the scan but absent from the tracked inventory is the finding: it is either an undocumented endpoint that will expire with nobody watching, or a certificate issued by a process that has since been forgotten. Record an owner for every certificate before moving to classification; an unowned certificate is the one most likely to lapse silently.

### 2. Classify every endpoint by whether it can run ACME

The automation approach differs entirely by what the endpoint can do, so classify before choosing a client.

| Class | What it looks like | Automation path |
| --- | --- | --- |
| Native ACME client | A host or service that can run `certbot`, `acme.sh` or an equivalent agent directly | Install the client, point it at the CA, schedule the renewal |
| Orchestrator-managed | Kubernetes workloads behind an ingress or gateway | `cert-manager` with an `Issuer` or `ClusterIssuer`, `Certificate` resources per host |
| Cloud-managed | A load balancer, CDN or API gateway that terminates TLS for you | The provider's own managed-certificate service (for example ACM), which renews on its own once validation stays in place |
| Appliance, no ACME support | A firewall, a load balancer with no ACME integration, a vendor SaaS console, embedded device firmware | Cannot self-automate; needs a runbook and a compensating schedule — read `references/endpoint-playbooks.md` |

Do not assume a class from the vendor name alone; confirm by checking for ACME support in the current firmware or product tier, since it changes between releases.

### 3. Automate issuance and renewal per class

For a native client, `certbot` is the reference implementation and its defaults already track the shrinking schedule below:

```bash
certbot certonly --standalone -d host.example.com --deploy-hook "systemctl reload nginx"
certbot renew --dry-run

# The renewal timer's unit name depends on how certbot was installed — find it before enabling it
systemctl list-timers --all | grep -i certbot
```

Enable whichever unit that command shows: `certbot-renew.timer` on an EPEL install, `certbot.timer` from Debian or Ubuntu's `apt` package, or `snap.certbot.renew.timer` from the snap. `systemctl` is deliberately left out of this skill's `allowed-tools` alongside `nmap`, since enabling a timer changes host state and should prompt rather than run unattended.

For an orchestrator-managed estate, `cert-manager`'s `Certificate` resource already renews at a third of the certificate's issued lifetime by default when both `renewBefore` and `renewBeforePercentage` are left unset — the same fraction as this skill's lifetime-fraction backstop. Set `renewBeforePercentage` only when a specific certificate needs to renew earlier than that default, for example to `50`:

```bash
kubectl get certificate -A -o custom-columns=NAME:.metadata.name,READY:.status.conditions[0].status,NOTAFTER:.status.notAfter
```

For a cloud-managed certificate, confirm the domain-validation records that keep it renewing automatically are still in place — this is the step teams skip, and it is why a managed certificate still occasionally expires: the CNAME or DNS validation record was removed when a workload moved, and the renewal silently stopped succeeding with no error visible until the certificate lapses.

### 4. Schedule by ACME Renewal Information, backed by the lifetime-fraction rule

Where the CA and client both support it, check ACME Renewal Information (ARI) rather than a fixed calendar offset — it lets the CA tell clients when to renew, which absorbs both routine schedule changes and an unplanned mass revocation without every client needing a new hard-coded interval. Recommended practice is to check ARI at least twice a day.

As a backstop where ARI is unavailable, or as the rule ARI itself falls back to: renew when a third of the certificate's total lifetime remains, or half the lifetime for certificates issued with a validity under 10 days. `certbot` 4.0.0 implemented exactly this rule, and 4.1.0 added automatic ARI checking on `certbot renew`. `cert-manager` already defaults to the same third-of-lifetime fraction; encode it explicitly in any other custom renewal timer rather than a fixed day count, because a fixed offset written against a 90-day certificate is wrong the day the estate moves to a 47-day one.

`references/lifetime-schedule.md` has the full validity and domain-validation-reuse schedule with its dates and sources; read it when setting a renewal interval or explaining to a stakeholder why the cadence is changing again in 2027 and 2029.

### 5. Monitor expiry and alert on renewal failure

Two signals, and both matter: days until expiry, and whether the last renewal attempt succeeded. A certificate can be days from expiring because renewal is broken, or because it is deliberately short-lived and due to renew tonight — the expiry clock alone cannot tell those apart, but a failed renewal attempt always means something.

```bash
# Days remaining, scriptable per endpoint
echo | openssl s_client -connect host.example.com:443 -servername host.example.com 2>/dev/null \
  | openssl x509 -noout -enddate
```

Whether a given expiry or renewal-failure signal should page someone or only open a ticket is `alert-design`'s classification, not this skill's — hand it off rather than deciding severity here. What this skill owns is making sure the signal exists at all and is generated from outside the renewal automation, so a client that has silently stopped running is still caught.

### 6. Handle the failure modes that survive automation

Automating issuance does not remove every way a certificate outage still happens. Check each of these once automation is in place, not only when one bites.

| Failure mode | What goes wrong | The fix |
| --- | --- | --- |
| Pinned intermediate certificate | A client trusts a specific intermediate by fingerprint; the CA rotates intermediates and the pin breaks every subsequent issuance | Pin the root, or the CA itself, never an intermediate that the CA can reissue |
| Hard-coded certificate chain | A client or appliance bundles a fixed chain file rather than fetching the current one at connection time | Serve the full current chain from the endpoint on every renewal, not a chain file written once at setup |
| OCSP caching | A client assumes an OCSP responder exists and caches a stapled response indefinitely; Let's Encrypt no longer runs an OCSP service at all | Stop depending on OCSP for a CA that has retired it, and confirm any client-side revocation checking has a working fallback |
| Appliance with no ACME support | Renewal stays a manual action indefinitely | Put it on a compensating schedule with a named owner and a calendar reminder set from the lifetime-fraction rule, tracked in `references/endpoint-playbooks.md`, and treat it as the estate's highest-priority automation gap |

## Output format

```markdown
## Path
[inventory | automation | monitoring | endpoint playbook — and why]

## Estate summary
[certificate count found from CT logs and scans versus the tracked inventory, and how many are unowned]

## Endpoint classification
[count per class: native client, orchestrator-managed, cloud-managed, appliance with no ACME support]

## Automation status
[per class: automated and monitored | automated, no monitoring | manual, with owner and cadence]

## Schedule
[ARI where supported; otherwise the lifetime-fraction backstop applied, and against which validity period]

## Failure modes checked
[pinned intermediates, hard-coded chains, OCSP dependence, appliance runbooks — each confirmed or flagged]

## Handed off
[anything routed to secret-rotation, alert-design, iac-review or plan-platform-migration, and why]

## Remaining risk
[unowned certificates, appliances with no automation path yet, and the date each becomes urgent]
```

## Anti-patterns

**Trusting the tracked inventory instead of checking from outside.** A spreadsheet or a cert-manager listing records what the team remembers configuring, not what is actually being served. The certificate that expires unannounced is reliably the one nobody thought to add to the list — it is found first by a browser warning or a CT-log alert service run by someone outside the organization, which is the worst way to learn about it.

**Hard-coding a fixed renewal offset from the current validity period.** A 60-day renewal trigger written against a 90-day certificate becomes wrong, not merely conservative, the day the estate issues a 47-day one — it can leave no time to react to a failed renewal. Encode the lifetime fraction, not a day count.

**Automating issuance without a monitored failure mode.** A renewal cron job that has been silently failing for months looks identical to one that has never needed to run, right up until the certificate expires. The alert has to come from checking the certificate itself, not from trusting the automation that is supposed to have renewed it.

**Leaving an appliance's manual renewal undocumented.** "Someone will remember" survives one renewal cycle at 398 days and fails the first time the cycle shortens to 47. Every appliance that cannot automate needs a named owner, a calendar-driven reminder set from the lifetime-fraction rule, and a runbook, or it becomes the next unplanned outage.

**Pinning an intermediate certificate instead of the root.** It works until the CA's next routine intermediate rotation, which is a "when", not an "if" — and it fails every client that pinned it at once, on a schedule the client's own operator does not control.

**Treating a leaked certificate or key as a renewal.** Issuing a fresh certificate on the normal schedule while the compromised private key is still valid leaves the exposure open for as long as both certificates remain trusted. That is `secret-rotation`'s incident path, not this skill's planned one.

## Reference files

- `references/lifetime-schedule.md` — read when setting or explaining a renewal interval: the full CA/Browser Forum validity and domain-validation-reuse schedule with its effective dates, ballot SC-081's adoption date, and the Let's Encrypt profile and ARI figures, each with its source.
- `references/endpoint-playbooks.md` — read once an endpoint is classified in step 2: the exact automation commands per class, and the runbook shape for an appliance that cannot run ACME at all.
