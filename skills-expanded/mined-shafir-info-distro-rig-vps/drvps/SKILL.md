---
name: drvps
description: Use when driving throwaway VMs or requesting egress splices on this host's distro-rig-vps rig as a `drvpsctl`/`drvpsvc` group member -- create / exec / snapshot / destroy VMs and manage egress-splice destinations, all through the single `rigctl` command (no sudo, no /dev/kvm). Covers the lifecycle verbs, the egress-splice request flow, result privacy, and timeout / `--idem` reconciliation. Full reference bundled in references/AGENT-GUIDE.md.
---

# distro-rig-vps -- agent skill (drive the rig via `rigctl`)

You are a rig **agent**: an unprivileged user in the `drvpsctl` group (and, for egress, the `drvpsvc`
group). You drive throwaway VMs through ONE command -- **`rigctl`** -- with **no sudo and no `/dev/kvm`**.
The operator owns the host, goldens, and network; you only use the rig via `rigctl`. You never need the
project source or host internals.

If `rigctl` says **"could not reach the submit socket"**, either you are not in `drvpsctl` yet (ask the
operator: `usermod -aG drvpsctl <you>`, then log out and back in) or the service is down.

## Start here

```
rigctl distros                    # the golden distros the operator built (id  distro  built_at)
vmid=$(rigctl create dev fedora44 | jq -r 'select(.status=="ok" and .exit_code==0).stdout' | tr -d '[:space:]')   # the id is the envelope's .stdout
rigctl wait "$vmid"               # block until boot + cloud-init + ssh are ready
rigctl exec <id> 'uname -a'       # run a command INSIDE the guest (unrestricted in-box)
rigctl list                       # id  state  name  artifact_id
rigctl status <id>                # state | generation | artifact_id | egress_gen
rigctl snapshot <id>              # freeze installed state as a reusable snapshot (secrets scrubbed)
rigctl destroy <id>               # stop + remove the VM (every VM also has a mandatory auto-reaped TTL)
```

`exec` is intentionally unrestricted inside the box -- break the guest freely, then `rigctl recreate <id>`
to reset it to its pinned base. You cannot set the network, ssh key, or project; numeric caps (ttl / mem /
cpus) are range-checked. Guests reach only the host caching proxy and configured mock ports -- not the open
internet, not each other.

## Egress splices (`drvpsvc` members only)

Register a CRM/callback host the operator opens end-to-end (never MITM'd). The submit is a REQUEST; the
operator applies it later after a dry-run + YES, and you learn the outcome by polling status:

```
rigctl egress add-splice callback.crm.example        # request a splice (default port 443) -> pending + reqid
rigctl egress list                                   # your splice requests + each state
rigctl egress status <reqid>                         # that request's outcome: pending | under-review | applied | rejected | expired (reqid from add-splice)
```

Non-members are refused (exit 12). The operator's decision (`applied` | `rejected` | `expired`) is learned
only by polling `egress status`.

## Two things that bite

- **Result privacy.** By default each result -- including `pull` file bytes and `exec` stdout -- is written
  `0600` with a POSIX ACL for YOUR account only (`ls -l` shows the `0640` mask; `getfacl` shows the real
  grant). A rig MAY run the legacy group-readable mode -- ask your operator which is active before moving a
  secret through `exec`/`pull`.
- **Timeouts are INDETERMINATE for mutations.** `rigctl` waits up to `RIGCTL_TIMEOUT` (default 360s) but a
  lifecycle op can run ~900s, so a mutation can time out while still queued or running. Reads
  (`list`/`status`/`inspect`/`snap-ls`) are always safe to re-issue. For mutations, pass `--idem <key>` on
  the FIRST attempt so a replay never double-executes; otherwise reconcile with `list`/`status` (VM
  lifecycle) or `snap-ls` (snapshots) before retrying -- never let an inconclusive check justify a blind retry.

## Full reference

This skill is the Claude Code adapter for the drvps agent domain. The vendor-neutral orientation that
other agents load from persistent memory is `share/agent-context/drvps/DOMAIN.md` in the installed
tree; the guides bundled here are the same contract.

- `references/AGENT-GUIDE.md` -- the complete agent guide (every verb + flag, all error/recovery cases).
- `references/ORCHESTRATOR-GUIDE.md` -- the service-orchestrator contract (snapshot/secret-restore policy,
  service-class VMs) for building a long-lived orchestrator on top of the rig.

Anything needing sudo -- installing the rig, building goldens, allow-listing a mirror, changing caps -- is
the operator's job, not the agent's.
