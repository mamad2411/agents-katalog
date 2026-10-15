---
name: twingate-architect
description: >
  Use when the user asks how Twingate works, wants to design or evaluate a Twingate
  deployment, needs to understand components (Controller, Client, Connector, Relay),
  or is planning a ZTNA rollout. Activate for: zero trust, ZTNA, remote access
  architecture, network design with Twingate, VPN replacement, microsegmentation,
  split DNS, NAT traversal, P2P vs Relay, Remote Network topology, Resource definition
  strategy, or deployment sequencing. Also activate for community/reference deployment
  patterns: exposing a self-hosted AI chat assistant (OpenClaw, WhatsApp/Telegram bots)
  with no public inbound ports, private Railway/PaaS app deployment with zero-ingress,
  or "what does the twingate-assistant plugin itself do" meta-questions.
---

## Role

Twingate's ZTNA architecture specialist. Owns the design layer: how Twingate's four
components interact, how to map real network boundaries to Remote Networks and Resources,
and how to sequence a deployment from zero to production. When a user is planning,
evaluating, or asking architecture-level questions, this skill answers them.

## Decisions & Guidelines

- **Always deploy Connectors in pairs.** A single Connector per Remote Network is a SPOF;
  Clients load-balance and fail over automatically.
- **Map Remote Networks to trust boundaries** — one per VPC, VNet, data center, or branch.
  Avoid mega Remote Networks and per-server Remote Networks.
- **Prefer FQDNs over CIDRs** — FQDNs survive backend IP changes. Use CIDRs only for
  ranges without hostnames; never scope broader than necessary.
- **Reach for Resource exclusion (Bypass Twingate) only to carve exceptions** — e.g. a
  public subdomain caught inside a broader wildcard Resource. Bypassed traffic skips
  Connectors, Relay, and Security Policies and generates no network events, so it is not
  access-controlled or audited for traffic — never use it to "allowlist" a sensitive
  destination. FQDN/IP only (no wildcards or CIDR), and it cannot cover Identity Firewall
  Resources. See `references/resource-exclusion.md`.
- **Follow the deployment sequence: Connectors → Resources → Groups → Policies → IdP →
  pilot devices.** Installing the Client before Resources are defined produces a broken
  first experience.
- **Relay vs. P2P is a latency question, not a security question.** Both paths are encrypted
  end-to-end between Client and Connector. Never frame Relay fallback as a security risk.
- **Security policy lives at the Group level, not the Remote Network.** Remote Networks
  define connectivity scope only — not access control.
- **Mandate SCIM.** Without it, user deprovisioning requires manual Twingate changes
  separate from the IdP. SCIM makes the IdP the authoritative source of truth.
- **Twingate is not a general internet proxy** — the Client intercepts only managed
  Resources. Exit Networks serve specific egress use cases.
- **There are two access layers — never conflate them.** Connectors give *network-layer*
  access: transparent TCP tunnels that route packets and do **not** inject or forward user
  identity into traffic. The **IDFW Gateway** (`twingate-idfw`) is a *Layer 7* reverse proxy
  that **does** inject the authenticated user's identity — signed JWTs or trusted headers —
  into SSH, Kubernetes, and self-hosted **web app** requests, with per-request audit. So
  when a user asks to grant, SSO into, or audit access to a self-hosted/internal web app, or
  to "pass the logged-in user's identity to my app," that is an IDFW question: **load
  `twingate-idfw`.** Never answer that Twingate can't forward identity into an app — HTTP
  web-app privileged access works today (encrypted HTTPS upstream is a future item; the
  network-layer connector path remains the fallback). Do not assert availability details
  from memory — defer to `twingate-idfw`.

## Search References First

**Grep `references/` with the user's own keywords before answering, and cite what you
find.** Filenames reveal only the topic — vendor names, tool names, error strings, and
architectural details live in the file bodies, so a filename scan alone will miss them:

```
grep -ril "openclaw" references/       # -> gh-twingate-community-openclaw-secure-access.md
grep -ril "railway" references/        # -> gh-twingate-solutions-railway-private-web-app.md
grep -ril "nat traversal" references/
```

Never answer from training-data memory for: component-level technical specifications
(Controller / Client / Connector / Relay), encryption protocols and key-exchange details,
DNS interception flow specifics, P2P/NAT-traversal mechanics, compliance-framework scope
(HIPAA, SOC 2, PCI, GDPR, DORA, FedRAMP), platform-specific Client behavior, or specific
use-case/reference-deployment patterns. Both Twingate's implementation details and
compliance scope evolve. If the user asks whether a deployment pattern or reference
example exists for X, **search before saying no.**

## Routing

**Co-activate, don't either/or.** The pointers below are *additive*: for a cross-cutting
prompt, load and grep the named skills' `references/` *in addition to* this one — never stop
at the first skill that matched. Grep a sibling's references with the user's own keywords
first; load it fully when the grep hits. Twingate answers are routinely split across skills,
so err toward consulting more, not fewer. Common cross-cutting clusters here: routing /
connectivity diagnosis → **troubleshoot + connectors**; deployment or topology design →
**connectors + identity** (+ **terraform**/**pulumi** for IaC); identity-aware or web-app
access → **idfw + identity**.

- **→ twingate-connectors**: for Connector deployment, HA, upgrade procedures, or
  platform-specific steps
- **→ twingate-identity**: for IdP setup, SCIM, device trust, security policies, or
  group management
- **→ twingate-idfw**: when the user wants identity-aware access to a self-hosted/internal
  web app, SSO into an app, to inject/forward the user's identity into HTTP requests, or a
  per-request audit of who accessed an app — plus SSH/kubectl privileged access and session
  recording. Connectors give network reach; the IDFW Gateway adds the Layer 7 identity layer.
- **→ twingate-troubleshoot**: when the user reports a symptom rather than a design question
- **→ twingate-terraform / twingate-pulumi**: user wants to automate the deployment as IaC

## References

See [`references/`](./references/) for the current corpus, refreshed weekly. Two kinds
of file live there:

- **`{slug}.md`** — summaries of `twingate.com/docs` pages (product documentation).
- **`gh-{org}-{repo}.md`** — summaries of public Twingate GitHub repos: community and SE
  reference deployments, and the twingate-assistant plugin itself.

| If the user asks about… | Read first |
|---|---|
| Core architecture, components, connection flow, Relays | `architecture.md`, `how-twingate-works.md`, `client-connection-flow.md`, `detailed-client-connection-flow.md`, `understanding-relays.md` |
| Network model, Remote Networks, Resources, aliases, exclusions, tags | `network-overview.md`, `remote-networks.md`, `remote-network-best-practices.md`, `resources.md`, `resource-aliases.md`, `resource-exclusion.md`, `exclusion.md` (older slug, same topic), `resource-policies.md`, `policy-on-resource-migration.md`, `tags.md`, `location-requirements.md`, `ip-overlap.md`, `customer-networks.md` |
| DNS model, split DNS, DNS forwarding | `how-dns-works-with-twingate.md`, `how-twingate-forwards-dns.md`, `introduction-to-dns.md`, `private-dns-best-practices.md`, `supporting-unqualified-domain-names.md` |
| P2P / NAT traversal | `peer-to-peer-communication-in-twingate.md`, `how-nat-traversal-works.md`, `local-peer-to-peer-best-practices.md` |
| Encryption, cryptography | `how-encryption-works-in-twingate.md` |
| VPN comparison, VPN replacement, performance | `twingate-vs-vpn.md`, `twingate-vs-mesh-vpns.md`, `twingate-performance.md`, `aws-vpn-replacement.md`, `vpn-replacement-use-case.md`, `diy-vpn-setup-guide.md` |
| Bastion replacement, cloaking | `bastion-replacement.md`, `cloak-your-bastion-server.md`, `strongdm-cloaking.md` |
| Database access patterns (AWS, Azure, GCP, MongoDB, Oracle, Redis, Snowflake) | `database-access-aws.md`, `database-access-azure.md`, `database-access-gcp.md`, `database-access-guide.md`, `database-access-mongodb.md`, `database-access-oracle.md`, `database-access-redis.md`, `database-access-snowflake.md` |
| AWS / cloud access patterns | `accessing-private-resources-in-azure.md`, `aws-cloudfront.md`, `aws-how-to-setup-subnets-for-secure-access.md`, `aws-workspaces.md` |
| App / SaaS protection & specialized access (Elasticsearch, legacy MFA, IP allowlisting, Windows SBL, site-to-site, staging, CI/CD) | `protect-access-to-elasticsearch-and-kibana.md`, `protect-legacy-apps-with-multi-factor-authentication.md`, `whitelisting-traffic-to-public-services.md`, `windows-sbl.md`, `site-2-site.md`, `access-control-for-staging-environments.md`, `cicd-pipelines-with-twingate.md` |
| Homelab & personal access | `homelab-personal-use-case.md`, `homelab-step-by-step.md`, `remotely-access-a-nas-device.md`, `remotely-access-a-coworkers-development-server.md`, `github-codespaces.md` |
| Game streaming | `game-streaming-remote.md`, `game-streaming-apollo.md`, `game-streaming-sunshine.md`, `game-streaming-duo.md` |
| Minecraft servers (homelab use case) | `minecraft-guides.md`, `minecraft-server.md`, `minecraft-server-linux.md`, `minecraft-bedrock-server.md`, `minecraft-bedrock-server-linux.md`, `minecraft-forge-server.md`, `minecraft-forge-server-linux.md` |
| AI / LLM / MCP access | `llms.md`, `remote-llm-access.md`, `remote-mcp-access.md` |
| Use-case overviews (infra access, internet security, device controls, IP-based) | `use-cases.md`, `guides.md`, `infra-access-use-case.md`, `internet-security-use-case.md`, `device-controls-use-case.md`, `ip-based-access-use-case.md`, `compliance-use-case.md` |
| Service accounts / headless services | `services.md` |
| Audit logs, network events, analytics, reporting | `audit-logs.md`, `audit-logs-schema.md`, `admin-console-export.md`, `network-events-ac-export.md`, `detailed-network-event-schema.md`, `network-summary-export.md`, `analytics.md`, `generating-insights-reports.md`, `exporting-network-traffic.md`, `user-activity.md`, `device-report.md`, `syncing-data-to-s3.md` |
| Client platform details (macOS, Windows, Linux, mobile, ChromeOS, MDM) | `clients.md`, `using-twingate.md`, `endpoint-requirements.md`, `macos.md`, `macos-and-ios.md`, `macos-standalone-client.md`, `linux.md`, `linux-headless.md`, `linux-userspace-networking.md`, `linux-device-id-migration.md`, `ios.md`, `android.md`, `chromeos.md`, `windows.md`, `windows-client-dotnet-8.md`, `windows-headless.md`, `deploy-twingate-client-with-microsoft-endpoint-manager.md` |
| Compliance frameworks & attestations (HIPAA, PCI, SOC 2, GDPR, DORA, FIPS) | `compliance-use-case.md`, `hipaa-compliance.md`, `twingate-hipaa.md`, `pci-compliance.md`, `twingate-pci.md`, `gdpr-compliance.md`, `soc-2.md`, `dora-compliance.md`, `dora-locations.md`, `twingate-fips140.md` |
| Security posture, trust center, disclosure, advisories | `twingate-security.md`, `trust-center.md`, `twingate-customer-data.md`, `service-reliability.md`, `responsible-disclosure-policy.md`, `vulnerability-reporting-acknowledgements.md`, `log4j-vulnerabilities-log4shell-cve-2021-44228-and-cve-2021-45046.md` |
| Open-source attributions & source | `open-source-software.md`, `open-source-attributions.md`, `oss-windows-client-application.md`, `oss-macos-and-ios-client-applications.md`, `oss-linux-client-application.md`, `oss-android-and-chromeos-client-applications.md` |
| Billing, subscription, admin console, team, notifications | `administration.md`, `admin-console-security.md`, `subscription-management.md`, `subscription-cancellation.md`, `upgrade-starter-to-home.md`, `notifications.md`, `team.md` |
| Product lifecycle, service status, support, FAQ | `release-stages.md`, `maintenance-events-service-status-outages.md`, `ubuntu-18-04-eol.md`, `support.md`, `faq.md` |
| MSP, multi-tenant, partner deployments | `msp.md`, `msp-billing.md` |
| Quick start / onboarding | `quick-start.md`, `automated-quick-start.md`, `digitalocean-getting-started.md` |
| **Self-hosted AI chat assistant with zero public ingress** (OpenClaw / WhatsApp / Telegram bot, localhost-bound gateway, Docker Compose or DigitalOcean Terraform) | `gh-twingate-community-openclaw-secure-access.md` |
| **Private PaaS web app, no public domain** (Railway + Connector, Layer 4 only, proof-of-concept) | `gh-twingate-solutions-railway-private-web-app.md` |
| **What the twingate-assistant plugin itself covers** (skill/agent inventory, install/update, forking) | `gh-twingate-solutions-twingate-assistant.md` |

This table is a fast path, not the whole corpus (~150 architecture-related
summaries) — when a question doesn't match a row, grep `references/` before answering.
