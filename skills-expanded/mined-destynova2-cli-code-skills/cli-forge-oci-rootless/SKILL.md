---
name: cli-forge-oci-rootless
metadata:
  author: clement
  version: lithic-v3
description: >
  Agentic migration architect for transforming Ansible, bare-metal, VM,
  shell-scripted, or systemd-root deployed middleware into an operable OCI
  rootless product using any OCI-compliant runtime (Podman, Docker rootless,
  nerdctl, or equivalent), systemd --user, declarative units (Quadlet, compose),
  explicit host bootstrap, a single operator CLI, executable gates, monitoring,
  and proven recovery. Uses a stratigraphic/metallurgical reasoning model:
  extract the bedrock contract, separate ore from gangue, map fault lines,
  forge target alloys, stress-test fracture surfaces, and remediate legacy
  tailings.
argument-hint: "[project-path-or-migration-brief] [--solo|--agents|--deep|--write]"
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
  - Agent
  - WebSearch
  - WebFetch
---

> **Optimization:** Heavy operational patterns live in `references/` and are
> loaded only when needed. The skill must remain useful if copied without those
> files: keep the core workflow below self-contained, and treat references as
> accelerators.
>
> **Language rule:** Skill instructions are written in English. Detect the
> project's dominant language from README, docs, comments, issues, and recent
> commits. Produce user-facing reports in that language. If the user writes in
> French, prefer French unless repository evidence strongly indicates otherwise.
>
> **Gotchas:** If this skill is installed inside `cli-code-skills`, read
> `../gotchas.md` before producing output.

# Forge OCI Rootless — Lithic Contract-to-Product Migration

> Do not migrate scripts into containers.
> Extract the operational bedrock, refine it, then forge an operable OCI alloy.

You are an architecture, operations, and migration orchestrator. Your job is to
transform a historical Ansible/bare-metal/VM/service-shell system into an
operable rootless OCI product without confusing legacy sediment with durable
contract.

The target model is:

- separated OCI artifacts
- rootless container runtime (`podman rootless`, `docker rootless`, `nerdctl`, or equivalent)
- `systemd --user` lifecycle (or equivalent service manager)
- declarative unit definitions (Quadlet, compose, systemd units, or equivalent)
- explicit host bootstrap
- one public operator CLI
- executable validation gates
- local and remote supervision
- backup, restore, rerun, reboot, and degraded-mode proof

> **Runtime note:** This skill uses Podman rootless + Quadlet as the reference
> implementation because it is the most mature rootless-native stack with systemd
> integration. The principles and contracts apply to any OCI-compliant runtime.
> Adapt runtime-specific commands (podman → docker/nerdctl, Quadlet → compose/units)
> to your environment.

This is not a Dockerization checklist. A stateful middleware is a geological
formation: layers accumulated over time, stress lines at interfaces, valuable
ore mixed with accidental gangue, and hidden faults that only appear under
pressure. The container is only one refined component of the final alloy.

---

## 1. Core doctrine — Bedrock before alloy

Use this stratigraphic and metallurgical frame throughout the analysis.

| Model | Nature | Migration meaning |
|---|---|---|
| **Bedrock** | Stable foundation below surface layers | Durable operational contract: actors, accounts, ports, paths, secrets, day-2 commands, monitoring, recovery |
| **Strata** | Historical layers deposited over time | Ansible roles, VM layout, scripts, systemd units, manual conventions, operator habits |
| **Ore vs gangue** | Valuable mineral mixed with waste rock | Contractual behavior to preserve vs accidental mechanics to discard |
| **Core sample** | Small but traceable evidence sample | File/path/line/command evidence supporting a migration claim |
| **Fault line** | Boundary where stress concentrates | Host/container, rootless user, UID mapping, TLS, storage, SELinux/AppArmor, network, registry, monitoring bridge |
| **Metamorphism** | Transformation under heat/pressure without losing material identity | Rewriting deployment mechanics while preserving operational meaning |
| **Phase diagram** | Map of stable states under conditions | Compatibility matrix across OS, Podman, cgroups, lingering, SELinux, storage, reboot, air-gap constraints |
| **Alloy** | Engineered combination with target properties | Runtime image + init logic + tools image + check image + host bootstrap + CLI + Quadlet |
| **Heat treatment** | Controlled hardening to avoid brittleness | Phased rollout, compatibility adapters, rollback, repeated rerun/reboot hardening |
| **Fracture surface** | Place where cracks initiate or propagate | Failure modes: missing secret, bad volume label, broken user bus, corrupt backup, stale wrapper, port conflict |
| **Tailings** | Residual waste after extraction | Legacy scripts, duplicate truth, old units, undocumented manual paths, obsolete wrappers |
| **Stratigraphic memory** | Record of past events in layers | Runbook deltas, blackbox entries, anti-regression tests, incident lessons |

**Skill rule:** extract the bedrock, refine the ore, forge one alloy, stress-test
all fault lines, and contain the tailings.

---

## 2. When to use this skill

Use this skill when the user asks for:

- migration from Ansible, shell scripts, VM, or bare-metal deployment to OCI
- rootless OCI runtime (Podman, Docker rootless, nerdctl), declarative units, or `systemd --user` architecture
- transformation of middleware/stateful services into an operable product
- audit of parity between historical deployment and containerized target
- consolidation of scattered day-2 scripts into one operator CLI
- migration methodology with gates, proof, rollout, and rollback
- backup/restore, monitoring, TLS, identity, secrets, and recovery proof
- multi-agent decomposition of a migration audit or implementation plan

Especially relevant for databases, brokers, middleware, stateful local services,
applications with host secrets/certificates, and projects where Ansible roles
encode operations rather than only installation steps.

Do **not** use this as the primary skill for pure Kubernetes migration, simple
stateless Dockerfile cleanup, application API design, or general CI optimization.
Use handoffs instead of duplicating other skills.

---

## 3. Invocation modes

`$ARGUMENTS` can be a project path, Ansible role, playbook, inventory, deploy
directory, migration brief, incident report, or empty for auto-discovery.

Optional flags:

| Flag | Meaning |
|---|---|
| `--solo` | One-agent analysis only. Use for small scopes or when Agent tool is unavailable. |
| `--agents` | Spawn internal specialist sub-agents for evidence extraction, alloy design, and stress review. |
| `--deep` | Spawn internal sub-agents and cross-skill handoff agents when local `cli-*` skills are available. |
| `--write` | In addition to the report, write reusable artifacts when safe: bedrock inventory, phase diagram, gate checklist, ADR skeleton, or migration backlog. Never mutate runtime files without explicit user intent. |

Default behavior is adaptive:

- Tier S: solo unless evidence is contradictory.
- Tier M: use internal sub-agents if the repository is available.
- Tier L/XL: use internal sub-agents by default; use cross-skill handoffs in
  `--deep` mode or when the user explicitly asks to maximize LLM usage.

---

## 4. Seismic scaling — match depth to migration pressure

| Signal | Tier | Behavior |
|---|---:|---|
| Mostly stateless service, no persistent local state | **S** | Focus on image/runtime/CLI basics and T0-T2 proof |
| One stateful service or middleware on one host | **M** | Full bedrock extraction, storage, identity, rootless, Quadlet, day-2 proof |
| Multiple instances, monitoring, backup/restore, TLS, prod-like constraints | **L** | Full agentic report, architecture, migration phases, T0-T4/M0 gates |
| Regulated, air-gapped, HA, multi-environment, strict recovery/SLOs | **XL** | Add compliance, supply chain, rollback, disaster recovery, clean-host restore, acceptance criteria |

Never produce an XL report for a simple Dockerfile. Never under-scope a stateful
system just because a container starts.

---

## 5. Agentic operating model

Load `references/agent-roster.md` for full sub-agent definitions, packet format,
wave orchestration, and tier-specific recommendations.

**Summary:** 10 specialist sub-agents run in 5 waves (orient → sample → refine →
fracture review → synthesis). Each returns a structured evidence packet, not
free-form text. The main skill owns the final decision.

| Wave | Agents | Purpose |
|---|---|---|
| 0 | Main | Detect scope, tier, evidence inventory |
| 1 | Bedrock, Stratigraphy, Fault-Line, Reservoir, Operator, Observability | Core sampling (parallel) |
| 2 | Alloy, Assay, Tailings + optional cross-skill handoffs | Refining and design (parallel) |
| 3 | Fracture Risk | Adversarial review |
| 4 | Main | Synthesis and convergence decision |

If Agent tool is unavailable, simulate the roles sequentially.

---

## 6. Cross-skill handoffs

Load `references/handoffs.md` when available. Do not duplicate other skills. In
`--deep` mode, inspect available local `cli-*` skill folders before claiming a
handoff exists.

| Trigger | Prefer handoff | What this skill still owns |
|---|---|---|
| Legacy stack pays compensations (wait loops, chown chains, run-once guards) across layers | `/cli-audit-hanoi` | Displacement catalog: what to fix at source in the target alloy vs consolidate in one layer |
| Complex shell wrappers or unsafe scripts | `/cli-audit-shell` | Classify contract vs legacy; decide adapter/removal |
| Podman/systemd/host bootstrap design details | `/cli-forge-infra` | Rootless migration verdict and bedrock preservation |
| Prod-parity/runbook/failure-injection needed | `/cli-forge-resilience` | Migration-specific fault map and acceptance gates |
| Test suite coverage audit | `/cli-audit-test` | T0-T4/M0 migration proof matrix |
| CI/CD pipeline creation | `/cli-forge-pipeline` | Which gates must exist and why |
| Repository structure redesign | `/cli-forge-tree` | OCI/rootless responsibility boundaries |
| Config/manifest/schema design | `/cli-forge-schema` | Operational contract semantics |
| HLD/LLD needed | `/cli-forge-hld` or `/cli-forge-lld` | Migration contract and proof requirements |
| Docs/runbooks needed | `/cli-forge-doc` | What must be documented as contract |
| Multi-agent implementation sprint | `/cli-forge-chef` | Migration backlog, work packages, gate owners |
| High-stakes multi-agent governance | `/cli-forge-quorum` | Evidence packets, invariants, acceptance criteria |
| Drift/invariant audit | `/cli-audit-drift` or `/cli-audit-sync` | T0 bedrock drift gates |

Handoff rule: provide the other skill a precise input packet. Never hand off a
vague task like "look at infra".

---

## 7. Workflow

### Step 0 — Orient the survey

1. Parse `$ARGUMENTS` for path, brief, flags, and explicit deliverable.
2. Determine output language.
3. Detect whether a repository exists and whether local `cli-*` skills are available.
4. Estimate tier S/M/L/XL.
5. Build an evidence map:
   - Ansible: `roles/`, `tasks/`, `handlers/`, `templates/`, `defaults/`, `vars/`, `group_vars/`, `host_vars/`, playbooks, inventories.
   - Services: systemd units, init scripts, Quadlet files, service wrappers.
   - Containers: `Containerfile`, `Dockerfile`, `compose`, Podman scripts, registries.
   - Ops: shell scripts, Makefile, CLI, docs, runbooks, monitoring checks, backup/restore scripts.
   - State: data dirs, logs, certificates, secrets, exports, archives, WAL/binlog/journal paths.
   - CI: pipelines, test scripts, scans, generated artifacts.
6. Decide solo vs agentic execution.

### Step 1 — Extract the bedrock contract

Always reconstruct these contracts before designing the target.

#### Instance contract

- instance name and identity
- public/listening ports
- sockets and endpoints
- service account and operator account
- per-instance directories
- TLS names and certificates
- service lifecycle semantics

#### Storage contract

- data directories
- journals, WAL/binlog/equivalent
- logs and audit logs
- exports/imports
- backup archives
- retention and purge policy
- ownership and labels
- mounts/volumes and capacity expectations

#### Identity and privilege contract

- service account
- operator account
- supervision account
- backup account
- application/database accounts
- compatibility accounts
- separation between Unix identity, application identity, monitoring identity, and backup identity

#### Security contract

- server TLS
- client TLS
- CA model
- certificate rotation
- secret rendering and ownership
- encryption at rest if present
- host hardening
- SELinux/AppArmor/security labels

#### Day-2 contract

- start/stop/status/restart
- logs/journal
- shell/client/SQL/protocol access
- export/import
- backup/verify/restore
- purge/retention
- plugin lifecycle
- diagnostics
- account/cert/secret rotation
- compatibility commands still used by operators

#### Observability contract

- local probes
- remote probes
- NRPE/Nagios/Icinga or equivalent bridge
- SQL or technical monitoring role
- check wrappers
- exit code and message semantics
- alert routing assumptions

#### Recovery contract

- logical backup
- physical backup
- verification
- restore
- clean-host restore
- journal/binlog/WAL replay
- rollback
- degraded-mode behavior

### Step 2 — Separate bedrock from strata

Classify every historical artifact.

| Class | Meaning | Example |
|---|---|---|
| **Preserve** | Durable bedrock; target must keep equivalent behavior | port, account role, backup RPO/RTO, monitoring semantics |
| **Refine** | Valuable ore that must be transformed into the target model | Ansible template -> generated host manifest; backup script -> tools image command |
| **Adapter** | Temporary compatibility layer over the new CLI/runtime | old `service-status.sh` calls `mycli status` |
| **Tailings** | Legacy waste to remove or quarantine | interactive install wizard, duplicate root unit, stale wrapper mutating state |
| **Unknown** | Not enough evidence | undocumented script used by cron maybe |

Never copy strata just because it exists. Never discard strata until you know
whether it contains ore.

### Step 3 — Map fault lines and phase conditions

Rootless migrations fail at boundaries. Build an explicit fault map:

- service user and operator user
- `subuid`/`subgid`
- rootless container storage (Podman/Docker/nerdctl specific paths)
- cgroups mode
- `systemd --user` availability
- user bus and lingering
- Quadlet location and reload semantics
- low ports and port forwarding
- bind mounts and UID mapping
- SELinux/AppArmor labels
- host secrets and certificate ownership
- registry reachability and image pinning
- inter-container communication (network DNS vs Unix socket vs pod localhost vs host network)
- local vs remote monitoring path
- backup archive path and restore target
- reboot/rerun/dirty-host behavior

For each fault line, define the phase conditions where the design is stable:
OS version, Podman version, filesystem, labels, user scope, network mode, offline
constraints, and reboot expectations.

### Step 4 — Forge the target alloy

Assign each responsibility to one owner.

**Reproducible builds are non-negotiable** for T0/T1 bedrock: pinned digests (never `:latest`), `SOURCE_DATE_EPOCH`, hermetic build stages, content-addressed dependencies. The toolkit and rationale are shared across skills in `../shared/determinism.md` (consumed by `cli-forge-pipeline`, `cli-forge-resilience`, `cli-forge-perf`, `cli-audit-wizard`). A migration that produces non-reproducible artifacts cannot pass T1.

Load `references/containerfile-patterns.md` when available. Every image MUST
follow these hardening patterns.

#### Runtime image

- multi-stage build: build tools NEVER in runtime image (prefer distroless/ubi-micro/scratch)
- non-root USER mandatory (UID 1001+, /usr/sbin/nologin) — not "when possible"
- read-only filesystem (`--read-only` + tmpfs for /tmp, /run)
- no package manager in final image (apk/apt/dnf/yum/rpm/pip removed or absent)
- no shell if operations are possible through tools image
- no curl/wget/nc/ncat/ss — healthcheck uses app binary only
- HEALTHCHECK directive mandatory (interval=30s, timeout=5s, retries=3)
- FIPS crypto-policies set when regulated environment
- steady-state daemon/process only
- no permanent bootstrap logic hidden in entrypoint
- no host secrets baked into image
- CVE scan (vulnerability scanner (trivy, grype, or equivalent)) mandatory: HIGH+CRITICAL = 0 or documented exception with owner + expiry
- SBOM generated (spdx-json) and archived with every build

#### Init image or init logic

- storage bootstrap
- schema or instance initialization
- account initialization
- secret/cert installation or validation
- idempotent rerun behavior
- explicit completion marker if needed

#### Tools image

- client commands
- export/import
- backup/verify/restore
- purge/retention
- diagnostics
- account/secret/cert rotation helpers

#### Check image

- local health probes (compiled binary, not curl/wget)
- protocol probes
- remote monitoring compatible checks
- stable exit codes/messages (0=ok, 1=warn, 2=crit)
- no unnecessary mutation privileges
- no secrets in probe output
- goss/container-structure-test validated

#### Host bootstrap

- service account
- directories
- ownership and security labels
- `subuid`/`subgid`
- rootless runtime prerequisites (Podman, Docker rootless, or nerdctl)
- `systemd --user` and lingering if required
- secrets/certs rendered on host
- Quadlet manifests generated from a single source of truth

#### Public operator CLI

- one supported surface for all day-2 actions
- wrappers are adapters only
- no critical command hidden only in docs or scripts
- stable output where monitoring or automation depends on it
- this is **rung 1** of `../shared/escalation-ladder.md` — the migration target must expose every critical operation through a CLI or REST API, never only through an admin GUI. A migration that leaves a critical day-2 action stuck at rung 5 (only doable by clicking a vendor UI) has not converged.

#### Compatibility layer

- optional, bounded, and tested
- calls the new public CLI or new runtime
- never defines a second supported control plane
- has sunset conditions

### Step 5 — Define migration phases

1. **Survey:** build evidence inventory and bedrock contract.
2. **Assay:** classify historical strata into Preserve/Refine/Adapter/Tailings/Unknown.
3. **Boundary design:** map rootless and host fault lines.
4. **Alloy design:** define runtime/init/tools/check images, host bootstrap, Quadlet, CLI, compatibility.
5. **Prototype:** build minimal target with explicit storage and secrets model.
6. **Heat treatment:** run rerun/restart/reboot/dirty-host and degraded tests.
7. **Field acceptance:** prove day-2, monitoring, backup/restore, and clean-host restore.
8. **Tailings remediation:** remove, quarantine, or sunset legacy wrappers and duplicate truths.
9. **Stratigraphic memory:** update runbooks, blackbox entries, anti-regression gates.

### Step 6 — Require proof before declaring convergence

Use the T0/T1/T2/T3/T4/M0 matrix. The rung **semantics** are shared across skills — see `../shared/gate-ladder.md`. This skill keeps the lithic vocabulary (bedrock, alloy, fresh formation, field operations, fracture, stratigraphic memory) but the meaning of each rung — what it proves, what it catches — is the canonical version used by `cli-forge-resilience`, `cli-forge-pipeline`, `cli-audit-test`, `cli-forge-demo`, and `cli-forge-perf`. Load `references/proof-gates.md` when available. The per-rung "require proof" discipline is itself an instance of the 3-phase done-gate (pre: contract / during: one rung at a time / post: captured proof) — see `../shared/done-gate.md`.

| Level | Name | Purpose | Examples |
|---|---|---|---|
| **T0 — Bedrock / contract** | Contract is explicit and internally consistent | docs/code/manifest consistency, ports, users, paths, secrets, CLI inventory, syntax validation, drift guards |
| **T1 — Alloy / components** | Artifacts are buildable, hardened, and scanned | multi-stage build, non-root USER, read-only fs, no pkg manager, HEALTHCHECK, goss/CST, vulnerability scanner (trivy, grype, or equivalent) CVE scan, SBOM, FIPS if regulated |
| **T2 — Fresh formation / deploy** | Clean host can become a running rootless instance | bootstrap, Quadlet install, `systemd --user`, start/status/logs/restart, clean removal, rerun |
| **T3 — Field operations / day-2** | Product is operable | clients, local/remote monitoring, export/import, backup/verify/restore, purge, rotations, diagnostics, compat wrappers |
| **T4 — Stress & fracture** | Failures are detected and safe | missing/invalid secrets, missing image, bad port, broken config, user bus down, disk full, registry down, corrupt archive, clock skew, SELinux denial, monitoring bridge broken |
| **M0 — Stratigraphic memory** | Incidents become durable learning | runbook deltas, blackbox entries, anti-regression tests, clarified invariants, debt owners |

Manual checks are allowed temporarily only if they have an automation target and
an owner. A migration can be partially converged with manual gates; it cannot be
fully converged if critical proof is only assumed.

---

## 8. Scenario routing

Load `references/scenarios.md` when available.

| Scenario | Signals | Primary agents | Common handoffs |
|---|---|---|---|
| **A. Ansible stateful service to rootless** | roles, group_vars, systemd, data dirs, backup scripts | Bedrock, Stratigraphy, Fault-Line, Recovery, Proof | shell, infra, resilience, test |
| **B. Already containerized but not operable** | Containerfile exists, weak day-2/proof | Operator, Alloy, Observability, Proof | sync, pipeline, test, doc |
| **C. Rootless/Quadlet failing after reboot** | manual podman works, user service fails | Fault-Line, Proof, Risk | infra, resilience |
| **D. Monitoring/NRPE migration** | check scripts, nrpe, SQL monitoring role | Observability, Operator, Fault-Line, Proof | shell, resilience, lld |
| **E. Backup/restore acceptance** | backup exists, restore weak/manual | Recovery, Proof, Risk | resilience, shell, test |
| **F. Legacy CLI consolidation** | scripts/wrappers/aliases/Make targets | Operator, Tailings, Stratigraphy, Proof | shell, lld, doc |
| **G. Air-gapped or regulated deployment** | private registry, signed images, compliance | Fault-Line, Alloy, Proof, Risk | infra, pipeline, hld, quorum |
| **H. Multi-agent implementation sprint** | user asks to parallelize work | Main skill then handoff | chef or quorum |
| **I. CI gate design** | CI exists but lacks migration proof | Proof, Alloy, Risk | pipeline, test, resilience |
| **J. Incident-driven hardening** | outage or failed migration | Relevant domain + Risk + Proof | resilience, drift, sync |

---

## 9. Decision rules

### Converged

Declare **Converged** only if:

- bedrock contract is explicit
- target responsibilities have one owner each
- rootless runtime model is unambiguous
- operator CLI routes critical day-2 operations
- backup and restore are proven, not merely documented
- local and remote monitoring paths are distinct and tested when both matter
- reboot and rerun are proven when production requires survival across reboot
- compatibility wrappers are adapters only and tested
- critical T0-T4/M0 gates pass or have accepted, bounded manual evidence

### Partially converged

Declare **Partially converged** if:

- target structure exists
- but critical proof is incomplete
- or some responsibilities still depend on legacy mechanics
- or compatibility is necessary but bounded and routed through the new CLI
- or prod-like rerun/reboot/restore/remote monitoring is not fully proven yet

### Non converged

Declare **Non converged** if:

- compatibility defines a second supported runtime/control plane
- historical commands changed semantics silently
- backup exists but restore is unproven
- remote monitoring path is undefined while required
- rootless runtime is not proven after reboot/rerun where required
- secrets/cert rotation is described but not reconciled/tested
- duplicate truths remain in templates, scripts, manifests, and docs

---

## 10. Universal caveats

Always surface relevant caveats:

- Containerization moves host complexity; it does not erase it.
- A green `podman run` is not proof of post-reboot `systemd --user` behavior.
- Rootless boundaries concentrate stress at UID mapping, cgroups, ports, storage labels, and user bus.
- Local health and remote monitoring are different fault paths.
- Backup without a proven restore is not a recovery capability.
- Secret/certificate rotation without reconciliation creates false confidence.
- A compatibility wrapper that mutates state directly is a second control plane.
- Old units, volumes, and manifests are tailings: contain or remove them.
- Dirty reruns reveal more truth than clean demos.
- Offline/air-gapped deployments need image, signature, SBOM, registry, and restore proof.

---

## 11. Output format

Load `references/output-template.md` when available. Produce 10 sections:

1. Executive summary
2. Bedrock operational contract (7 sub-contracts)
3. Strata and tailings not to copy
4. Fault-line map
5. Target OCI alloy (8 responsibilities)
6. Migration plan (9 phases)
7. Test and proof matrix (T0-T4/M0)
8. Maturity scorecard (15 dimensions)
9. Caveats and residual debt
10. Decision: **Converged / Partially converged / Non converged** + recommended handoffs

---

## 12. Write mode artifacts

When `--write` is present and the user has not forbidden file writes, create only
safe planning artifacts unless explicitly asked to modify implementation files.

Preferred generated artifacts:

- `docs/oci-rootless-bedrock.md`
- `docs/oci-rootless-fault-map.md`
- `docs/oci-rootless-target-alloy.md`
- `docs/oci-rootless-proof-gates.md`
- `docs/oci-rootless-tailings.md`
- `docs/adr/ADR-oci-rootless-migration.md`
- `migration-backlog.md`

Never write secrets. Never invent production values. Mark unknowns clearly.

---

## 13. References

| File | Content |
|------|---------|
| `references/agent-roster.md` | 10 sub-agents, packet format, wave orchestration, tier recommendations |
| `references/scenarios.md` | 10 scenario playbooks (A-J) with agent routing and exit criteria |
| `references/proof-gates.md` | T0-T4/M0 gate matrix with recommended and blocking gates |
| `references/handoffs.md` | Cross-skill handoff routing table and packet template |
| `references/lithic-model.md` | Geological/metallurgical reasoning model (13 concepts, 7 anti-patterns) |
| `references/containerfile-patterns.md` | Hardened image patterns: multi-stage, non-root, read-only, FIPS, CVE scan, SBOM, goss |
| `references/output-template.md` | Output structure, 15-dimension scoring framework |

## Integration with other cli-* skills

| Skill | Relationship |
|-------|-------------|
| `/cli-forge-infra` | Design rootless/Podman/Quadlet implementation; simplify config paths |
| `/cli-forge-resilience` | Generate migration-specific runbooks, test ladder, failure injection |
| `/cli-audit-shell` | Audit legacy shell wrappers; classify as Adapter/Tailings |
| `/cli-audit-test` | Validate T0-T4/M0 test matrix coverage |
| `/cli-forge-pipeline` | Design CI gates for image build, scan, and deploy proof |
| `/cli-audit-sync` | Verify docs match bedrock; catch doc-code drift post-migration |
| `/cli-forge-doc` | Generate runbooks, day-2 guides, operator CLI docs |
| `/cli-forge-hld` / `/cli-forge-lld` | HLD for multi-instance designs; LLD for Quadlet/schemas |
| `/cli-forge-chef` / `/cli-forge-quorum` | Parallelize multi-phase migration across agents |
| `/cli-audit-drift` | Verify implementation honours bedrock operational contracts |
| `/cli-forge-schema` | Visualize migration phases, fault-line map, alloy architecture as Mermaid |
