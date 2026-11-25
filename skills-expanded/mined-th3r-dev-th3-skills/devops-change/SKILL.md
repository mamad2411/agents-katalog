---
name: devops-change
description: >-
  Any infra work that touches a real machine — ssh into a VM through a jump host, kubectl on a
  cluster, reading or changing HAProxy / ingress / CoreDNS / Vault-backed secrets, hunting the root
  cause of an incident — done in a fixed order (triage → read-only investigation → evidence → plan +
  approval → change in small steps → verify with the same commands → blameless review) and closed
  with a change report (before / steps / after / rollback) or an incident report with a SEV level
  and a timeline. Use WHENEVER the work is "ssh to <ip>", "run kubectl on nonprod/prod", "edit
  haproxy.cfg", "health check too frequent", "write the root cause / postmortem", "before/after
  rollback summary", "snapshot the running config", "เขียน rootcause", "สรุปก่อนแก้หลังแก้" — or
  before any command that changes the state of a shared machine.
---

# devops-change

Keep a knowledge base beside this skill in the project: `docs/` (servers, network), `incidents/`
(root-cause work) and `changes/` (every change already made). **Read those two folders before
guessing anything about a machine** — the trap you are about to hit is usually written down.

Companion skills for Kubernetes: a cluster-triage skill (symptoms → playbooks) and a manifest-review
skill. Facts about *your* machines in `docs/` beat those skills' generic advice (a vSphere / Tanzu
cluster is not EKS; a bare-metal HAProxy is not an ALB).

## 1. Getting on a machine

```bash
S=skills/devops/change/scripts
$S/jssh.py 'hostname'                               # the jump host
$S/jssh.py --host 10.0.0.48 'docker ps'             # another VM, via -J
$S/jssh.py --sudo --host 10.0.0.48 'ss -tlnp'
$S/jssh.py --kube 'kubectl get pods -A'             # runs the [kube] token refresh first
$S/jssh.py --forward 15211:10.0.0.53:1521           # DB tunnel through the jump host
$S/snapshot_haproxy.sh 10.0.0.48 snapshots          # what every HAProxy container is really running
```

Credentials come from `~/.config/devops/hosts.ini` (`[ssh]` / `[kube]`, layout in the script's
docstring; `chmod 600`, never inside a repo). **Never put a password on a command line, in a report
or in chat.** `Connection timed out during banner exchange` = your VPN is down; tell the user, do not
loop on retries.

## 2. Severity — decide before acting, write it at the top of the report

| level | means | response |
|---|---|---|
| SEV-1 | whole system down · data corrupted · security breach | now; tell the owner before anything else |
| SEV-2 | core feature degraded, a large user group affected | within 15 min |
| SEV-3 | partial failure with a workaround | within 1 h |
| SEV-4 | minor (e.g. stray traffic annoying a remote party) | business hours |

## 3. The order you do not skip

Five phases of incident response: detect → triage → investigate → fix → review.

1. **Detect + triage.** Write the symptom as the reporter said it. Ask three things: when did it
   start, what changed recently (deploy, secret, GitOps sync, config on a VM), how wide is the impact.
2. **Investigate read-only.** Form a hypothesis and prove it with real things (`tcpdump`, `ss`, logs,
   the config that is *running*, not the file on disk). Kill wrong hypotheses with evidence and keep
   them in the report. **Walk every cluster / environment** — the forgotten caller is usually in the
   one you did not look at. Search secrets by key name, not only by value.
3. **Capture evidence before touching anything.** `snapshot_haproxy.sh` or the equivalent + md5 +
   inode + container `StartedAt` + the numbers you will measure the result by → the "Before" section.
4. **Write the plan and get approval.** Copy `references/change-template-<th|en>.md` to
   `changes/<YYYYMMDD>-<slug>/README.md` (root-cause work: `references/incident-template.md` into
   `incidents/<YYYYMMDD>-<slug>/`). Offer options with their impact. An option that removes something
   must answer "who still uses it" with logs, not memory. Shared machines need a per-change yes;
   prod always does.
5. **Change one step at a time.** Back up `<file>.bak-<YYYYMMDD>` (`cp -p`) · syntax-check before
   reload · graceful reload before restart, always · when something unplanned shows up, stop and assess
   who it affects before going on, then log it in the timeline.
6. **Verify** by re-running the exact commands of step 3 and comparing the numbers — not by "no
   errors".
7. **Blameless review.** What went to plan, what did not, prevention work with an owner. Update
   `docs/` when a fact about a machine changed.

The rollback is written in step 4, with the command that proves it worked. Anything *you* did to the
system while investigating (a test TCP connect, a probe) gets a timestamp — the remote side may see
it and call it a symptom.

## 4. Language in the report

The team's language (Thai through the `kien-thai` rules, or English). Terms people say in English stay
English (`pod`, `route`, `health check`, `rollback`, `config`, `reload`). Command output is pasted as
it came, untrimmed. Times are the target machine's UTC.

## 5. Diagram

A Deployment diagram (zone = network segment, node = VM / pod / container) saved as `rootcause.html`
beside the report, with at most two orange highlights, on the cause. A fact that contradicts the
diagram fixes the diagram, not only the README. (`diagram-design` skill if available.)

## 6. Secrets and config that do not live on the machine

Cluster secrets synced from a vault (External Secrets Operator or similar): `kubectl edit secret` is
overwritten on the next sync; the source of truth is the vault. Before changing a value there, record
the old value in the report (non-secret values only), check the sync status (`kubectl get
externalsecret` → `SecretSynced`), and remember a pod that reads env needs a restart to see it
(a reloader controller may do it for you).

## 7. Traps already paid for

- `the server has asked for the client to provide credentials` from kubectl = an expired cluster
  token; refresh both the management and the workload context (`jssh.py --kube` runs the refresh).
- A single-file bind mount into a container (HAProxy's `haproxy.cfg` is the classic) keeps the **old
  inode** after an editor saves a new file (vim, nano, `sed -i`). The process keeps reading the old
  content; HUP does nothing; `/proc/<pid>/mountinfo` ends in `//deleted`. Write in place with
  `cat new > haproxy.cfg`; once it is stale, only a container restart helps. `snapshot_haproxy.sh`
  flags it.
- HAProxy in master-worker mode (`-W`): `docker kill -s HUP` = graceful reload, no dropped connections.
- A default `check` on a backend probes TCP every 2 s even when nobody uses the frontend; without
  `timeout check` a probe waits as long as `inter` while the kernel re-sends SYNs. A remote party
  sees that as a scan. A one-server backend gains nothing from `check`.
- A pod CIDR that overlaps a partner's network needs /32 host routes injected on the nodes (a
  DaemonSet) — not a CIDR change under running workloads.
- A prod workload may still depend on a nonprod proxy through a secret value (an LDAP URL in the
  vault). Grep every environment for the host:port before deleting a route.
- A container with thousands of restarts and no errors may simply be `sleep 3600` ending every hour.
- A reverse proxy in TCP mode cannot emit HTTP 504; the 504 comes from the HTTP layer behind it.
  Check which ingress / listener actually terminates the request before blaming a timeout value.
