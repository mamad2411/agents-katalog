---
name: twingate-connectors
description: >
  Use when the user needs to deploy, configure, upgrade, or troubleshoot Twingate
  Connectors on any platform. Activate for: Docker connector, Linux connector, systemd
  connector, ECS connector, Azure Container Instances, GCE, Helm chart connector,
  connector tokens, connector HA, connector health, connector metrics, connector
  logging, connector upgrades, DEAD_NO_RELAYS, DEAD_NO_HEARTBEAT, or connector
  placement questions. Also activate for connector deployment tooling and unofficial
  platform support: Raspberry Pi, Ubiquiti/UniFi (UDM Pro, UDM SE, UXG) gateways,
  Unraid, Home Assistant, Steam Deck / Decky Loader, Hyper-V, Chocolatey packaging,
  custom or hardened connector containers, GitHub Codespaces, Coder workspaces,
  render.com, Spacelift CI runners, connector log shipping to S3, connector fleet
  autoscaling, Grafana connector dashboards, PagerDuty connector alerting, or
  Docker container auto-updating for connector hosts.
---

## Role

Twingate Connector deployment and operations specialist. Owns everything from token
generation and platform selection to high availability design and dead-connector
diagnosis. When a user needs to get a Connector running, keep it running, or understand
why it stopped, this skill answers those questions.

## Decisions & Guidelines

- **Never deploy a single Connector per Remote Network.** It is a SPOF. The Twingate
  Client load-balances and fails over across Connectors automatically — no external
  load balancer is needed.
- **Each Connector requires its own unique token pair.** Never share tokens between
  Connectors. Tokens are tied to one Connector's identity; sharing causes authentication
  conflicts and unpredictable behavior.
- **Always use the rolling major-version tag, never pin to a patch version.**
  The rolling tag self-updates on restart. Pinned images accumulate
  vulnerabilities and miss bug fixes. Current tag string is in
  `references/connector-deployment.md`.
- **Scale by adding more Connectors, not by sizing up the host.** Connectors are
  lightweight — a small instance handles hundreds of concurrent users. Achieve HA through
  parallelism, not vertical scale.
- **The Connector host must have line-of-sight to backend resources.** A Connector that
  authenticates successfully but cannot reach its resources shows ALIVE in the console but
  silently fails to proxy. Always test from the Connector host, never from the user's machine.
- **`DEAD_NO_RELAYS` always means the connector cannot reach Twingate's
  control/relay infrastructure.** The most common cause is DPI/SSL inspection
  on `*.twingate.com`, but it can also be one of the required outbound ports
  being blocked, or — less commonly — an IPv6-only host with no public IPv4 path to
  the Relay. The full network requirements live in
  `references/connector-best-practices.md` — verify the customer's egress path
  permits all of them before assuming DPI is the cause.
- **Connector tokens are credentials.** Never store them in Dockerfiles, Compose files,
  or IaC source committed to version control. Inject via secrets management.
- **Always set a restart policy on container deployments** so the Connector
  recovers after host reboots without manual intervention. Current Docker flag
  and Compose / systemd equivalents are in `references/docker.md`,
  `references/deploy-connector-with-docker-compose.md`, and
  `references/systemd-service.md`.
- **Prefer official deployment paths first.** The community, Labs, and SE repos indexed
  below are reference implementations for platforms Twingate doesn't officially package
  for (Raspberry Pi images, Ubiquiti gateways, Steam Deck, Hyper-V, CI runners, fleet
  autoscaling, etc.) — useful and often the only option, but tell the user plainly which
  ones are community-maintained, which are unsupported SE examples, and which are
  experimental, rather than presenting any of them as a Twingate-supported product.

## Search References First

**Grep `references/` with the user's own keywords before answering, and cite what you
find.** This skill has the largest GitHub-tooling surface of any Twingate skill — 19
repos covering everything from Raspberry Pi image builders to CI runner sidecars — and
filenames alone will not surface most of it. Vendor names, hardware models, exact error
strings, and CLI flags live in the file bodies, not the filenames:

```
grep -ril "too many open files" references/     # -> 1422554451-connector-offline-too-many-open-files-in-logs.md
grep -ril "proxytunnel" references/             # -> gh-twingate-solutions-twingate-client-userspace-spacelift.md
grep -ril "decky\|steam deck" references/       # -> gh-twingate-community-twindeck.md
```

Never answer from training-data memory for: outbound port numbers, container image
tags or Helm values keys, platform-specific deployment commands, hardware sizing,
connector log paths or metric names, or upgrade/shutdown procedures — these change
between releases and the references are the source of truth. The same applies to
tooling questions: if the user asks whether something exists for a given platform,
CI system, or ops workflow — Ubiquiti, Unraid, Home Assistant, Steam Deck, Hyper-V,
Codespaces, Coder, Spacelift, log shipping, autoscaling, dashboards, alerting —
**search before saying no.**

## Routing

**Co-activate, don't either/or.** The pointers below are *additive*: for a cross-cutting
prompt, load and grep the named skills' `references/` *in addition to* this one — never stop
at the first skill that matched. Grep a sibling's references with the user's own keywords
first; load it fully when the grep hits. Twingate answers are routinely split across skills,
so err toward consulting more, not fewer. Common cross-cutting clusters here: DEAD connector
/ unreachable resource → **troubleshoot + architect**; IaC token provisioning →
**terraform**/**pulumi**; Kubernetes hosting → **kubernetes**; identity-aware gateway access
→ **idfw**.

- **→ twingate-architect**: for questions about Remote Network topology or Resource
  definition strategy
- **→ twingate-kubernetes**: for Helm chart deployment or K8s-specific Connector patterns
- **→ twingate-terraform / twingate-pulumi**: for IaC-automated token generation
- **→ twingate-troubleshoot**: when a Connector is DEAD or a user cannot reach a resource

## References

See [`references/`](./references/) for the current corpus, refreshed weekly. Three kinds
of file live there:

- **`{slug}.md`** — summaries of `twingate.com/docs` pages (product documentation).
- **`{numeric-id}-{slug}.md`** — Twingate help-center articles: symptom-shaped support
  content, exact error strings, and per-platform gotchas.
- **`gh-{org}-{repo}.md`** — summaries of public Twingate GitHub repos: SE and community
  tooling, reference implementations, and automation — 19 of them for this skill alone.

### Core deployment & operations

| If the user asks about… | Read first |
|---|---|
| What a Connector is, how it registers, connection concepts | `connectors.md`, `understanding-connectors.md`, `connector-client-registration.md` |
| Network requirements, ports, firewall/SG/NSG rules, egress | `connector-best-practices.md` |
| Cloud deployment overview (universal pattern, all providers) | `cloud-providers-guide.md` |
| AWS-specific deployment (ECS, EC2, EKS) | `aws-connector-patterns.md`, `aws.md`, `aws-ecs-headless-configurations.md` |
| Azure-specific deployment (ACI, VMs, AKS); **Docker Hub rate limits blocking ACI deploy/restart** (`RegistryErrorResponse`, `index.docker.io`) | `azure-connector-patterns.md`, `azure.md`, `6965244612-azure-container-docker-hub-rate-limits-block-connector-deployment-or-restart.md` |
| GCP-specific deployment (GCE, GKE, Cloud Run, MIG) | `gcp-connector-patterns.md`, `gcp.md` |
| Docker / Docker Compose deployment | `docker.md`, `deploy-connector-with-docker-compose.md` |
| Linux / systemd deployment | `connectors-on-linux.md`, `systemd-service.md` |
| PaaS / managed container platforms (Aptible) | `aptible.md` |
| Homelab / NAS overview, getting started | `homelabs-guide.md`, `home-assistant-getting-started.md`, `headless-iot-gateway.md` |
| NAS, homelab, on-prem (Synology, QNAP, TrueNAS, Proxmox, Unraid, Firewalla, CasaOS, ZimaOS, Ubiquiti) — official doc pages | `how-to-set-up-twingate-on-a-synology-nas-dsm-7.md`, `how-to-set-up-twingate-on-a-synology-nas-dsm-6.md`, `nas-qnap-install.md`, `truenas-container-deployment.md`, `proxmox-container-deployment.md`, `proxmox-getting-started.md`, `unraid-getting-started.md`, `deploy-connector-on-firewalla.md`, `casaos-getting-started.md`, `zimaos-getting-started.md`, `deploy-connector-on-ubiquiti.md` |
| Connector image tag, container env vars, deployment commands | `connector-deployment.md`, `connector-metadata.md`, `connector-details.md` |
| Semi-automated / scripted deployment (Terraform, API) | `deployment-semi-automation.md` |
| Connector upgrades; **`apt upgrade` fails with `NO_PUBKEY` GPG error** | `upgrading-connectors.md`, `5202917932-connector-upgrade-produces-gpg-error-in-apt.md` |
| `DEAD_NO_RELAYS`, `DEAD_NO_HEARTBEAT`, health diagnosis | `connector-real-time-logs.md`, `connector-monitoring.md`, `connector-health-checks.md` |
| Logs, metrics, monitoring, SIEM integration; **enabling debug-level (`TWINGATE_LOG_LEVEL=7`) logging and exporting logs** | `connector-metrics.md`, `connector-monitoring.md`, `connector-real-time-logs.md`, `siem-guide.md`, `2906603735-twingate-connector-logs.md` |
| **Real-time connection logs to S3 fail with "Your S3 sync is experiencing issues" (SSE-KMS)** | `5872386799-using-sse-kms-s3-realtime-connector-logs-sync-results-in-your-s3-sync-is-experiencing-issues.md` |
| Hardware sizing, HA topology, placement | `connector-best-practices.md`, `connector-placement-best-practices.md` |
| Headless / service account clients | `services-headless-clients.md`, `aws-ecs-headless-configurations.md` |
| Connector shutdown, restart, lifecycle | `connector-shutdown-process.md`, `advanced-connector-management.md` |

### Connector offline / flapping diagnostics (symptom-shaped help articles)

| Symptom | Read first |
|---|---|
| **Repeating `Token is expired` 403 in logs** — benign, PubNub Access Manager token auto-renewal, no action needed | `1364033881-repeating-token-is-expired-error-in-connector-logs.md` |
| **"too many open files"** — host `ulimit` of 1024 fds capping ~128 concurrent clients; ECS Fargate can't override it | `1422554451-connector-offline-too-many-open-files-in-logs.md` |
| **Status flapping offline/online, or dies days after restart** — host clock drift >5s vs. Controller; fix with `chronyd`, not `ntpd` alone | `4104282255-connector-offline-status-flapping-offline-online-or-goes-offline-some-time-after-restart.md` |
| **"Gone, code 410" in logs** — tokens expired/deleted server-side, unrecoverable; requires `apt purge twingate-connector` and full re-deploy with fresh tokens | `4908519978-connector-offline-gone-code-410-in-logs.md` |
| **Connector healthy but zero Resource connections succeed** — host has only a public IPv6 address; Relay requires IPv4, assign an Elastic IP / external IPv4 | `4995810632-connector-cannot-connect-to-the-twingate-relay.md` |

### GitHub repository tooling

These 19 repos are **not bundled** — clone/inspect at runtime. Each solves a distinct
deployment or ops problem; read the file's `## Summary` and `## Key Information` before
recommending one, and flag community/Labs/SE-example status per the guideline above.

**Platform-specific deployments (hardware and OS targets Twingate doesn't officially package for):**

| Platform | What it does | Read first |
|---|---|---|
| **Raspberry Pi — turnkey SD image** | Builds a flashable Raspberry Pi OS image that auto-provisions a Connector via the Twingate API on first boot (systemd `twingate-firstboot` service); daily CI checks for new Connector/OS versions | `gh-twingate-community-pi-starter.md` |
| **Raspberry Pi — install scripts** | Official Twingate-Solutions install scripts for running the Twingate client directly on an already-running Pi (ARM32/ARM64), service-key based — distinct from the pi-starter image builder above | `gh-twingate-solutions-twingate-raspberry-pi.md` |
| **Ubiquiti / UniFi gateways (UDM Pro, UDM SE, UXG-Pro, UXG-Max)** | Deploys a Connector inside a `systemd-nspawn` Debian container on the gateway itself; boot hook + `unifi-common` service persist it across UniFi OS firmware upgrades | `gh-twingate-community-ubiquiti-connector.md` |
| **Unraid** | Official Docker template XML for Unraid's Community Apps UI — drop-in template exposing Access Token / Refresh Token / Network Name fields | `gh-twingate-community-unraid-template.md` |
| **Home Assistant** | Packages the Connector as a Home Assistant Supervisor add-on (`aarch64`/`amd64`/`armv7`); requires HAOS/Supervised, not Core-only installs | `gh-twingate-community-home-assistant-add-on.md` |
| **Steam Deck (Decky Loader / QAM)** | `Twindeck` — a Decky Loader plugin running the Twingate Headless Client from the Quick Access Menu without leaving gaming mode; needs a Service Account key | `gh-twingate-community-twindeck.md` |
| **Windows Server / Hyper-V** | PowerShell scripts (`Deploy-TwingateConnector.ps1`) that provision Connector VMs on Hyper-V via cloud-init Ubuntu 24.04 images, with full create/update/repair/remove lifecycle through the Twingate API | `gh-twingate-solutions-twingate-connector-hyperv.md` |
| **Windows Chocolatey packaging** | Chocolatey package definitions for `choco install twingate` — silent/automated Windows client install, upgrade, uninstall | `gh-twingate-labs-chocolatey-packages.md` |
| **Custom/hardened connector container** | Example Docker image adding shell access, a pluggable `/healthchecks.d/` healthcheck system, and structured JSON resource metrics on stderr (separated from connector stdout) | `gh-twingate-solutions-twingate-custom-connector-container.md` |

**CI/CD and ephemeral dev-environment runners:**

| Environment | What it does | Read first |
|---|---|---|
| **Coder workspaces** | Terraform templates replacing Coder's default `main.tf` to run a Twingate client inside a workspace, supporting both interactive user auth and Service Account (headless) auth | `gh-twingate-labs-tg-coder.md` |
| **GitHub Codespaces** | `.devcontainer` Dockerfile + two `devcontainer.json` variants (Service Account or interactive) so a Codespace can reach Twingate-protected private resources | `gh-twingate-labs-tg-github-codespaces.md` |
| **render.com** | One-click "Deploy to Render" button that stands up a Connector as a render.com service using tokens generated in the Admin Console | `gh-twingate-labs-tg-render.md` |
| **Spacelift CI runners** | Runs Twingate's **userspace HTTP proxy mode** plus `proxytunnel` inside an unprivileged Spacelift runner container — no root, no TUN device, no `NET_ADMIN` — to bridge Postgres/MySQL/SSH through Twingate's HTTP CONNECT proxy | `gh-twingate-solutions-twingate-client-userspace-spacelift.md` |

**Observability, ops, and fleet automation:**

| Capability | What it does | Read first |
|---|---|---|
| **Grafana dashboards** | Community Grafana dashboard (`grafana/insights.json`) visualizing Connector transport breakdown (direct/relay-hydra/relay-quic), traffic, and uptime from a Prometheus-fed metrics export; needs Grafana 12.2.1+ | `gh-twingate-community-dashboards.md` |
| **PagerDuty alerting** | Bash/systemd service that tails Connector logs via `journalctl -f`, forwards `Offline`/`Error`/`Unrecoverable error` state changes to PagerDuty's Events API v2, and auto-resolves on recovery | `gh-twingate-labs-twingate-pagerduty.md` |
| **Log shipping to S3** | Python sidecar/systemd service that captures `ANALYTICS`-prefixed Connector stdout, batches it, and uploads gzip NDJSON to any S3-compatible store (AWS S3, MinIO, R2, B2, Spaces); requires `TWINGATE_LOG_ANALYTICS=v2` | `gh-twingate-solutions-twingate-connector-log-shipper.md` |
| **Local connector status UI** | Lightweight web dashboard running alongside a Connector on the same host for on-box status/diagnostics without the Admin Console — no built-in auth, restrict via firewall | `gh-twingate-solutions-connector-local-ui.md` |
| **Generic Docker auto-updater (Janus)** | Label-driven container updater (`janus.autoupdate.enable=true`) that recreates any labeled container — including custom connector containers — when a newer image is available, with rollback on failure; not Compose-aware | `gh-twingate-solutions-janus-updater-service.md` |
| **Connector fleet autoscaling** | "Fleet Commander" — an async control-plane loop that discovers, scales, and retires Connector containers across Docker/ECS/ACI backends via the Docker socket and the Twingate GraphQL Admin API; exposes `/healthz`, `/readyz`, `/metrics` | `gh-twingate-solutions-twingate-fleet-commander.md` |

This table is a fast path, not the whole corpus — when a question doesn't match a row,
grep `references/` before answering.
