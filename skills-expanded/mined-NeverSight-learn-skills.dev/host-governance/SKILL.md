---
name: host-governance
description: Query and govern shared host infrastructure across projects, including safe service-deployment inventory, guarded initial Linux server bootstrap, Docker installation and bounded Docker/BuildKit cache cleanup, reusable operational-function productization, GitHub Actions self-hosted runners, Jenkins installation, upgrades, controller and agent configuration, credentials, plugins, jobs and Android/iOS packaging; Tailscale; Caddy; PostgreSQL; Cloudflare Tunnel, DNS, Access, WAF/Rulesets, and selective Cloudflare HTTP 403 diagnosis. Use when an agent needs authoritative host inventory, server onboarding, container-runtime installation, Docker cache-retention automation, CI runner configuration, deployed-service and resource observations, Cloudflare security-event or WAF diagnosis, inspection, planning, writes, verification, rollback, or asks to make a host procedure such as installing specific software a reusable host-governance function.
---

# Host Governance

Use one control workflow for infrastructure shared by multiple projects. Keep
application identity and build intent in the consuming project, and shared
compute, CI, network, ingress, DNS, and host ownership in the host
infrastructure repository.

## Query Shared Context

When another project needs shared host facts, locate the authoritative host
repository instead of copying an inventory into the consuming project or this
skill. Use the first unambiguous source in this order:

1. an exact repository path supplied by the current user;
2. a repository already established as authoritative in the current task;
3. the `HOST_INFRA_ROOT` environment variable;
4. the runtime locator documented in [context.md](references/context.md).

Resolve the `context` task against the authoritative host repository, not the
consuming repository. Read every returned policy reference before execution:

```bash
uv run python <skill-root>/scripts/resolve.py \
  --cwd <host-root> --task context --operation <operation> --format json
uv run python <skill-root>/scripts/host-governance.py \
  --cwd <host-root> execute --task context --operation <operation> \
  [contracted arguments]
```

Use `catalog` when identities are unknown, `search` to get candidate metadata,
and `get` with one exact kind and ID to retrieve authoritative content. Use
`current-device` only when the project contract provides it; stop rather than
guess when no device or multiple devices match.

Context results are repository declarations with their stated provenance and
freshness. They are not live observations. Do not fetch or pull implicitly,
probe networks, call provider APIs, or convert repository-declared values into
runtime claims. Do not persist a derived inventory or return secret-bearing
fields. Resolve `control` separately for live inspection or mutation.

## Inspect Deployed Services

When the task asks which services, containers, listeners, resource limits, or
data paths exist on a host, use the project-owned read-only
`service-inventory-inspect` control operation when it is configured. Pass one
exact device ID at a time and use only the SSH alias declared by that device's
manifest. Do not scan networks, guess addresses, install a collector, or
execute arbitrary remote commands.

When a safe snapshot already exists and the task asks for drift or sizing
advice, use the project-owned read-only `service-inventory-report` operation.
It may compare only against an explicitly declared per-device baseline; a
missing baseline or missing historical metrics is a finding, not permission to
infer desired services or resize a host.

Treat the result as a dated runtime observation, not a new source of truth.
Keep the safe JSON snapshot outside Git by default. Compare it with the
device's declared service baseline only after resolving the project profile;
promoting an observation into a repository declaration is a separate
repository-write request.

The inventory must be secret-safe: collect service names, managers, states,
versions, listeners, persistence indicators, resource limits, and bounded
capacity signals, but never environment variables, full command lines, logs,
credentials, tokens, private keys, or container secret contents. Read the
project-owned inventory reference when present for schema, platform support,
redaction, and retention rules.

## Resolve Project Behavior

Before inspecting or changing infrastructure, resolve the `control` task from
the consuming Git repository. Prefer the JSON operation contract when the
repository uses `host-governance.config.v2`:

```bash
uv run python <skill-root>/scripts/resolve.py \
  --cwd <project-root> --task control --operation <operation> --format json
```

Execute a configured operation only through the validated runner:

```bash
uv run python <skill-root>/scripts/host-governance.py \
  --cwd <project-root> control <operation> [contracted arguments]
```

Use `--authorized` only after the current user authorizes a non-read-only
operation. The flag is a mechanical gate, not proof of authorization. Never
bypass a v2 contract with its underlying command. The resolver validates argv,
mutability, authorization, parameters, output schema, exit states, and allowed
next states without executing project code.

Legacy `host-governance.config.v1` profiles and the generic fallback remain
readable composed instructions. Read the returned `instructions.path` whenever
`instructions_id` changes, but do not execute legacy declared command strings
as a substitute for a v2 contract. Without a configured transaction contract,
leave shared host infrastructure unchanged unless the one-round emergency
manual authorization below explicitly applies.

Read [project_config.md](references/project_config.md) before creating or
changing a project profile.

## Apply One-Round Emergency Manual Authorization

Normally, every remote write, reload, policy save, DNS mutation, migration, or
rollback must use a project-configured, validated operation. When the current
user explicitly states `授权手动进行紧急操作` or an unambiguous equivalent,
grant one emergency manual-operation round for the current bounded task. This
is a narrow exception to the configured-operation requirement, not a general
permission to run arbitrary remote commands.

- Define one round as the current assistant execution turn. It starts only
  after the explicit authorization and ends when the task completes, blocks,
  or control returns to the user. Multiple tool calls needed for that same
  bounded task are covered; do not ask for reauthorization between them.
- Limit the authorization to the exact targets, actions, and material effects
  established in the current request and plan. It does not authorize a new
  host, provider, task, target, or scope expansion.
- Use an available governed operation when it can complete the task. Use
  manual SSH, API, console, or other remote steps only for the emergency gap
  that the current authorization explicitly covers; never turn the exception
  into a persistent arbitrary-command capability.
- Before the first mutation, inspect the exact target and current state,
  establish a bounded recovery path, and preserve secret-safe evidence. Apply
  only the necessary steps, verify each material effect, and report every
  manual change and remaining recovery gap.
- Preserve target validation, transaction locking when available, secret
  handling, exposure checks, and separate authorization boundaries for
  destructive, billable, identity-changing, or otherwise materially broader
  outcomes.
- Expire the authorization at the end of this round, even if the task is
  incomplete. A later assistant turn or new task requires the user to state
  the emergency manual authorization again. Never infer it from an earlier
  turn, an earlier conversation, or ordinary SSH authorization.

## Productize Requested Procedures

When the user asks to make a procedure a host-governance function, read
[procedure-productization.md](references/procedure-productization.md). Treat
the request as authorization to capture the successful method, implement a
deterministic project-owned controller, parameterize reviewed variations, add
contracted operations and tests, and use that controller for the current task.
Do not stop after documenting the procedure or leave the next invocation to
reconstruct shell commands.

On later invocations, resolve and execute the existing contracted controller
first. Inspect or extend it only when the requested option is not represented,
the target platform is unsupported, or live evidence shows the contract is
stale. Never replace a reusable function with an ad hoc remote command merely
because the one-off command would be shorter.

## Establish Authority

1. Identify the consuming project and its deployment intent.
2. Locate the host infrastructure repository using an explicit user path,
   `HOST_INFRA_ROOT`, or the runtime locator described in the resolved
   instructions. Do not guess a path or copy infrastructure facts locally.
3. Read the infrastructure repository's root scope, module boundaries, storage
   rules, operations policy, and target device or provider resource.
4. Inspect the current live state of every affected system before proposing a
   write. Repository intent and live state are separate evidence.
5. Classify each requested change by owner and executor. A consuming project
   may request infrastructure but does not acquire authority to rewrite shared
   configuration.

## Apply Conversation-Scoped SSH Authorization

When the user states `本次对话允许执行SSH读写` or an unambiguous equivalent,
treat it as standing authorization for the current conversation and current
task. Autonomously run the SSH read and write commands needed to complete that
task against targets unambiguously established by the request or authoritative
host context; do not request per-command or per-turn SSH approval.

Use this standing authorization to satisfy the user-authorization prerequisite
for an in-scope contracted SSH mutation, including its `--authorized` gate. It
does not bypass a required v2 contract, target or alias validation, transaction
lock, secret handling rule, or verification and rollback requirement. It also
does not independently authorize an unrequested release, deployment, rollback,
destructive or identity-changing outcome, billable action, provider API or
console action, browser action, local credential change, a different host, or a
new task. Require explicit task intent for those outcomes, but do not repeat SSH
approval when that intent and the standing authorization already cover the
command. Ask once before execution when the target, task boundary, or material
effect remains ambiguous.

Expire the authorization when the task completes, the conversation ends, or
the user revokes or narrows it. Never carry it into another conversation or
infer it from an earlier one.

## Preserve Safety Invariants

- Treat `inspect` and `plan` as read-only. Without conversation-scoped SSH or
  active one-round emergency manual authorization, require current-turn
  authorization for each remote write, reload, policy save, DNS mutation,
  migration, or rollback target. With either authorization, do not repeat
  approval for in-scope tool calls; preserve every separate authorization
  boundary defined above.
- For an initial server-bootstrap request, treat local key creation, manifest
  edits, host-key scans, `inspect`, `plan`, and `apply` as intermediate states,
  never as proof that the server was initialized. End the task only as
  `verified complete`, `explicitly blocked`, or `rolled back`; report the
  exact remote changes and verification evidence for that terminal state.
- Consume a bootstrap password only through the contracted hidden prompt or
  approved secret source, only for the first SSH connection, and never persist,
  echo, recover from page state, or place it in argv. If the credential is not
  available when needed, stop and report the initialization as blocked; do not
  imply that password authentication was attempted.
- Treat a device ID, hostname, direct target, SSH alias, and jump-host alias as
  distinct identities. Use only aliases declared by authoritative device
  manifests or a fixed operation contract. Never guess an SSH alias from a
  device ID, and use the same declared jump route for host-key observation,
  password bootstrap, administrator-key verification, and finalize checks.
- Require a successful password-bootstrap transport to disable remote PTY
  allocation, wait for an authenticated remote-ready marker before sending a
  script, send an explicit remote exit, and distinguish pre-auth closure from
  rejected credentials. Never fall back to a direct connection when the
  contract declares a jump host.
- Treat an SSH connectivity or credential blocker as scoped to SSH. Do not
  open a provider console, call a provider API, inspect a credential-bearing
  login page, or read browser autofill values unless the user separately and
  explicitly authorizes that exact provider action.
- Never expose or persist API tokens, auth keys, private keys, session data,
  environment dumps, or secret-bearing request bodies.
- When an authorized Tailscale installation uses interactive authentication,
  capture the exact `https://login.tailscale.com/a/...` URL emitted by the
  target and return it to the user as soon as it appears. Do not wait silently
  for browser authorization, replace it with an Admin Console detour, or skip
  dependent services merely because no auth key is available. Keep the
  transaction in `awaiting-tailnet-auth`, never persist the URL, and resume
  only after the user completes authentication and live node identity is
  verified. Use only a project-contracted interactive operation when a v2
  contract is active; a missing operation is an explicit contract blocker.
- Never treat a live service inventory as a desired declaration or use a single
  point-in-time sample as proof of long-term capacity. Report freshness and
  missing historical evidence explicitly.
- Never recommend or apply fixed PostgreSQL memory, connection, checkpoint, or
  WAL settings without first running the hardware-aware sizing workflow in
  [postgresql.md](references/postgresql.md). A shared host defaults to the
  conservative eligible option; balanced and dedicated options require their
  declared evidence and may not be selected merely because startup succeeds.
- Snapshot the exact current resource and keep a tested recovery path before a
  shared configuration change.
- Require one host-owned serialized transaction for each shared-resource
  mutation. Record its stable transaction ID, owner, target, base and result
  generation, desired resource digest, composed candidate digest, phase, and
  verification state without copying secrets or complete private configuration.
- Re-read authoritative and live state under the executor lock before apply.
  Treat an earlier plan as advisory; never install a stale rendered candidate.
- Detect overlapping hostnames, listeners, routes, selectors, resource IDs,
  and ownership before editing. Stop on an unresolved collision.
- Generate the complete combined plan before the first mutation. Do not let a
  successful application deployment imply that Caddy, Tailscale, DNS, or TLS
  is correct.
- Do not report a Tailscale installation as complete until its effective update
  channel, automatic-update behavior, package reachability, and recovery path
  have been inspected and either verified or reported as an explicit gap.
- Do not report a Docker installation as complete until package ownership,
  daemon and Compose readiness, cgroup mode, smoke-test cleanup, effective
  listeners, firewall exposure, automatic BuildKit cache-cleanup posture, and
  recovery state have been verified. For hosts expected to build images, make
  bounded automatic BuildKit cache cleanup part of the desired installation
  state; never broaden it to Docker image, volume, container, or data-root
  deletion. Treat Docker group membership as root-equivalent access requiring
  separate intent.
- Treat Jenkins installation, controller configuration, plugin state, agents,
  credentials, shared job runtime, backups, and upgrades as host-owned state.
  Preserve application identity and signing intent from the consuming project;
  never make a mobile build green by adopting another application's identity.
- Treat a Cloudflare public application as one coupled transaction spanning
  the origin, connector, tunnel ingress, proxied DNS, Access application, and
  Access policy. Never report a partially configured path as published or
  protected.
- Prefer product-specific skills when available. This skill remains the
  transaction owner and must reconcile their results into one final report.
- Do not broaden network access to make verification pass. Verify required
  flows positively and forbidden flows negatively.
- Keep billable, destructive, or identity-changing actions separate from
  ordinary deployment authorization.

## Control Workflow

1. Resolve the project profile and authoritative host infrastructure root.
2. Build a change matrix: owner, target, current state, desired state,
   executor, validation, rollback, and authorization state.
3. For service inventory, inspect only the exact requested devices and record
   collection provenance, freshness, capability gaps, and redaction status.
4. Inspect all involved products and compute one ordered plan without writes.
   Resolve contracted credential sources and verify exact API capability before
   proposing interactive browser or Dashboard authentication.
   For SSH port changes, inspect effective `sshd -T` ports, actual listeners,
   and `ssh.socket` activation and overrides. Treat a declared port without a
   live listener as blocked.
5. Present material exposure, deletion, billing, downtime, and recovery
   effects before requesting any missing authority.
6. Apply only authorized steps, using the relevant product reference:
   - A procedure requested as a reusable host-governance function: read
     [procedure-productization.md](references/procedure-productization.md).
   - Initial Linux server bootstrap: read [server-bootstrap.md](references/server-bootstrap.md).
   - Docker Engine or Compose installation: read [docker-install.md](references/docker-install.md).
   - GitHub Actions self-hosted runner installation or lifecycle: read
     [github-actions-runner.md](references/github-actions-runner.md).
   - Caddy or HTTP/TLS ingress: read [caddy.md](references/caddy.md).
   - Shared PostgreSQL service deployment, sizing, parameter changes, or lifecycle:
     read [postgresql.md](references/postgresql.md) and run
     `scripts/postgres_sizing.py` before rendering configuration.
   - Jenkins installation, upgrades, security, nodes, credentials, jobs, or
     Android/iOS packaging: read [jenkins.md](references/jenkins.md).
   - Tailscale installation, update readiness, policy, or node settings: read
     [tailscale.md](references/tailscale.md).
   - Cloudflare accounts, zones, DNS, WAF/Rulesets, selective edge blocks, or Terraform state: read
     [cloudflare.md](references/cloudflare.md).
   - Cloudflare Tunnel public hostnames and Access protection: read
     [cloudflare-tunnel.md](references/cloudflare-tunnel.md).
7. Apply through the host-owned lock and transaction journal. Compose from the
   latest accepted per-owner declarations, validate the complete candidate,
   atomically install, and preserve a recoverable prior generation.
8. Validate each component immediately after its change. Stop the forward
   sequence on failure and preserve evidence. A retry must resume or safely
   supersede according to the authoritative transaction, not start a blind write.
9. For initial server bootstrap, verify a fresh administrator-key connection
   on the desired SSH port plus rejection of password and prohibited root login
   before retiring the old key, closing the bootstrap port, or claiming
   completion. Treat service installation and external enrollment checks as
   separate required evidence when enabled.
   When systemd socket activation owns SSH listeners, snapshot and configure
   its override in the same host transaction; reloading only `ssh.service` is
   not evidence that a new port is listening. Keep the old listener until the
   new one is positively reachable through the declared route.
10. Run end-to-end and negative-path checks after all components pass.
    Treat local key generation, the local SSH host block, plaintext credential
    removal, identity-file migration, and old-key retirement as explicit local
    host operations. If the executor cannot write `~/.ssh`, report that exact
    permission blocker and emit a bounded patch; never imply the remote
    transaction updated local SSH configuration.
11. Report repository changes, live changes, transaction identity and
   generation, credentials/configuration needed,
   compatibility, rollback state, and every item still unverified.

`inspect`, `plan`, and `verify` are read-only. `apply` and `reconcile` require
current write authority for the exact target, normally through the configured
operation contract. The explicitly authorized one-round emergency manual
operation above is the only exception. `rollback` requires separate current
authority and must restore only the selected owner's declaration by
recomposing the latest complete host state; it must never restore a historical
monolithic shared configuration.

## Ownership Boundaries

| Surface | Primary authority | Runtime authority |
| --- | --- | --- |
| Application port and health contract | Consuming project | Deployed application |
| Application source, identity, build, and signing intent | Consuming project | Source and signing authorities |
| Desired per-device service deployment baseline | Host infrastructure repository | Repository declaration and owning runtime |
| Live service inventory and capacity observation | Runtime host | Bounded read-only collector |
| Target host and service exposure | Host infrastructure repository | Target host and network |
| Docker package source, daemon lifecycle, and host-level container runtime | Host infrastructure repository | Package manager, systemd, and Docker daemon |
| Jenkins installation, controller, plugins, nodes, credentials, backups, and upgrades | Host infrastructure repository | Jenkins controller and agents |
| Jenkins job definition and execution state | Host infrastructure repository | Jenkins controller and agents |
| Caddy host mapping and shared ingress | Host infrastructure repository | Running Caddy instance |
| Tailnet access intent | Host infrastructure repository | Saved Tailscale policy and nodes |
| Cloudflare desired resources | Host infrastructure repository | Cloudflare API and IaC state |
| Cloudflare connector placement and runtime | Host infrastructure repository | Target host and Cloudflare edge |
| Cloudflare Access application and policy | Host infrastructure repository | Cloudflare Access API |

Generated Caddy fragments, plans, caches, and inventories are derived artifacts,
not additional authorities.
