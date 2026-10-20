---
name: keeper-pam
description: Work with KeeperPAM privileged access via Commander - listing PAM resources and gateways, brokering recorded SSH/RDP/database sessions with pam launch, tunnels, just-in-time access workflows, and credential rotation, all without exposing the underlying credential. Use when asked to launch a privileged session, find a PAM resource, set up a tunnel, configure just-in-time access, or rotate a PAM credential.
---

# KeeperPAM

KeeperPAM delivers zero-trust privileged access: people connect to
infrastructure through recorded sessions where the **credential is never
exposed** - the Keeper Gateway injects it on the far side of an
end-to-end-encrypted channel. Drive Commander through the tmux shell pattern
in the **keeper-admin** skill.

## The PAM model

- **PAM Machine** - an SSH / RDP / VNC / Telnet / Kubernetes target.
- **PAM Database** - a MySQL / Postgres / SQL Server / Oracle / MariaDB target.
- **PAM User** - holds the credential that is injected and rotated; its rotation settings reference a target resource.
- **Gateway** - an outbound-only broker (Docker / Linux / Windows) that touches the infrastructure; it pulls needed secrets via KSM APIs.
- **PAM Configuration** - holds cloud rights (AWS/Azure/GCP) for rotation and discovery.

Sessions ride an encrypted WebRTC channel (Apache Guacamole for graphical
protocols); recordings are encrypted with a per-session AES-256 key.

## Brokering a session

```bash
My Vault> pam gateway list               # gateways and reachability
My Vault> pam configuration list
My Vault> search bastion                 # find pamMachine/pamDatabase records (metadata)
My Vault> pam launch <RECORD_UID>        # recorded interactive session - MUTATING/SENSITIVE
```

Always **disambiguate** the resource before launching - the wrong host is an
incident. Confirm the requester's context and entitlement, verify a gateway can
reach the target, and launch only after explicit confirmation of the exact UID.
Never fetch or display the credential to "use it for the session" - the whole
point is that the user connects without it.

## Connections vs tunnels

A **connection** (`pam launch`) is an interactive recorded session. A
**tunnel** port-forwards a local port to the target for a native tool:

```bash
My Vault> pam tunnel start <RECORD_UID> --port 5432
# Non-interactive modes: --foreground | --background | --run "<command>", --timeout, --pid-file
```

Choose a connection for interactive work and a tunnel only when a local tool
genuinely needs the port. Tunnels pair well with rotation so the forwarded
credential is ephemeral.

## Just-in-time access and rotation

**JIT** provisions credentials or elevated privilege only for a session's
duration and reverses it on close - prefer it over standing privilege:

```bash
My Vault> pam workflow create "Prod Server" -n 1 -co -rm -d 2h   # admin: define the gate
My Vault> pam workflow request <record> --reason "CR-4821"       # requester
My Vault> pam workflow start <record>                            # check out after approval
My Vault> pam workflow end <record>                              # check in (may trigger rotation)
```

Rotation runs through the Gateway:

```bash
My Vault> pam rotation list
My Vault> pam action rotate -r <RECORD_UID>
My Vault> pam action job-info <JOB_ID>
```

Confirm the record, target, and gateway before rotating, and never display the
rotated value.

## Safe handling

Never expose the credential behind a resource - broker the session, never the
secret. Disambiguate the target, confirm context and entitlement, prefer JIT,
launch only on explicit confirmation, and treat every session as recorded,
monitored, and auditable. Detailed flag reference: `keeper-admin` skill's
`references/pam-commands.md`.
