---
name: linux-server-troubleshooting
description: "Evidence-driven troubleshooting for Linux server evidence bundles, tarballs, sosreports, command outputs, syslog/journalctl/auth/kern/dmesg logs, systemd service state, kernel/resource/storage/network evidence, container runtime logs, and Kubernetes worker/control-plane node host symptoms. Use when diagnosing Linux host failures, service crashes, boot or kernel issues, OOM/resource pressure, disk or filesystem problems, NIC/routing/DNS/NTP failures, SSH/auth/security issues, kubelet/containerd/docker node problems, or application outages where host evidence may explain Kubernetes or distributed-system symptoms."
---

# Linux Server Troubleshooting

## Mission

Troubleshoot Linux server evidence like a senior escalation engineer. Preserve customer artifacts, start broad, maintain competing hypotheses, correlate host signals with application and Kubernetes symptoms, and separate directly observed facts from inferences and unknowns.

Use this skill as the host-level companion to Kubernetes or network-device troubleshooting. If the evidence is mostly Kubernetes object state, pod logs, manifests, events, or must-gather output, use the Kubernetes troubleshooting workflow as well. If the evidence is mostly router/switch show output, use the relevant network-device workflow instead.

## Intake

1. Treat the customer's `data/` directory and uploaded bundles as read-only evidence.
2. List supplied files, sizes, timestamps, archive types, and top-level archive contents before deep analysis.
3. Extract archives into scratch space such as `work/<bundle-name>/`, preserving directory structure. Unpack nested archives into the same scratch tree.
4. Build a quick inventory of logs, command outputs, configs, systemd units, kernel data, network data, storage data, container runtime evidence, Kubernetes node evidence, sosreport directories, README/index files, and collection metadata.
5. Identify hostnames, roles, IPs, OS release, kernel version, virtualization/cloud platform, container runtime, kubelet role, affected services, and collection time. If any identity is inferred from filenames or log content, label it as an inference.
6. Read summaries, README files, sosreport manifests, collection scripts, operator notes, and support indexes before raw logs.

## Useful Tool Choices

Prefer read-only tooling first: `rg`, `find`/`Get-ChildItem`, `tar -tf`, `tar -xf` into scratch, `unzip -l`, `jq`, `yq`, `awk`, `sed`, `journalctl --file` for copied journal files, and packet tools only after a relevant time window and interface are known.

Use structured parsing when available:

- `jq` for JSON command output such as `systemctl show`, `ip -j`, `podman inspect`, `docker inspect`, or Kubernetes JSON.
- `yq` or a YAML parser for config, manifests, cloud-init, netplan, kubelet config, container runtime config, and systemd drop-ins.
- Offline file analysis by default. Use live commands only when the user explicitly requests live checks and access is available.

If a parser fails, keep raw text as source of truth and note the parser limitation.

## Artifact Classification

Classify each major artifact before interpreting it:

- Collection metadata: README, manifest, index, sosreport metadata, collection commands, timestamps.
- System logs: `/var/log/syslog`, `/var/log/messages`, `journalctl`, `kern.log`, `dmesg`, boot logs, rotated/compressed logs.
- Service state: `systemctl status`, unit files, drop-ins, restart counters, service-specific logs, timers, sockets.
- Kernel and hardware: panics, call traces, driver errors, machine checks, disk/NIC errors, udev, firmware, virtualization messages.
- Resource evidence: CPU/load, memory/OOM, swap, PSI, disk capacity, inode usage, file descriptors, process/thread counts, cgroups.
- Storage and filesystem: mounts, fstab, multipath, LVM, RAID, CSI mounts, NFS/iSCSI, ext4/XFS errors, read-only remounts.
- Network evidence: interface state, routes, policy routing, ARP/neighbor, DNS, NTP, firewall, nftables/iptables, conntrack, MTU, packet captures.
- Security/auth: SSH, sudo, PAM, SELinux/AppArmor, audit logs, certificate/TLS errors, permission denials.
- Container and Kubernetes node evidence: kubelet, containerd, docker, CRI-O, pod sandbox errors, CNI bridges/veth, kube-proxy, flannel/calico/cilium, node leases.
- Application evidence: app logs, supervisors, ports/listeners, dependency errors, health checks, rollout or automation markers.

## Broad First Pass

Run broad searches before focusing on one theory. Useful keyword groups:

```text
error|fail|failed|timeout|timed out|refused|reset|unreachable|no route to host|network is unreachable|i/o timeout
oom|out of memory|killed process|memory allocation failure|evict|pressure|swap|hung task|blocked for more than
panic|BUG:|Oops|call trace|segfault|core dumped|assert|fatal|aborted|watchdog|soft lockup|hard lockup
disk full|no space|inode|read-only|EXT4-fs error|XFS|I/O error|blk_update_request|nvme|sda|multipath|mount|umount
link is down|link becomes ready|carrier|duplex|mtu|drop|crc|tx timeout|reset adapter|renamed network interface|conntrack
DNS|SERVFAIL|NXDOMAIN|temporary failure in name resolution|certificate|x509|TLS|clock skew|NTP|timedate
systemd|failed with result|start request repeated too quickly|dependency failed|watchdog|restart counter
sshd|sudo|pam|denied|forbidden|permission denied|apparmor|SELinux|audit
kubelet|containerd|docker|crio|podman|CNI|flannel|calico|cilium|kube-proxy|node status|lease|PLEG
```

Capture context around hits, not isolated lines. Collapse repeated noisy streams by `(host, component, message pattern, affected object, time range)` so high-volume errors do not hide sparse causal clues.

Do not over-weight desktop/session noise, telemetry retries, Bluetooth/audio activation failures, or benign automation messages unless they align with the reported impact. Treat Ansible, SSH, sudo, health-checker, log-collector, and collection-script lines as timeline anchors unless they directly cause the symptom.

## Hypothesis Loop

After the first pass, maintain 2-5 competing hypotheses. Use this table shape in notes and final output when useful:

| ID | Hypothesis | Status | Confidence | Supporting evidence | Refuting evidence | Next check |
| --- | --- | --- | --- | --- | --- | --- |

Allowed statuses: `Open`, `Strengthening`, `Weakening`, `Rejected`, `Confirmed`.

For each hypothesis, actively search for support and refutation. Stop when one hypothesis explains the observed symptoms materially better than alternatives and the evidence is consistent across host logs, command state, configuration, and timeline.

## Linux Lenses

### Services And Systemd

For service outages, check the desired unit, dependencies, sockets, timers, drop-ins, environment files, restart policy, exit status, signal, core dump references, and whether systemd failures are primary or user-session noise.

Correlate:

- `systemctl status` or captured status output.
- Unit and drop-in files.
- Journal/syslog entries before the first failure.
- Service-specific logs.
- Recent package/config/secret/certificate changes.
- Port/listener conflicts and permissions.

### Kernel, Hardware, And Boot

For panics, lockups, driver issues, and boot failures, follow the kernel timeline from the earliest warning through recovery or collection end. Confirm whether messages are current, previous boot, or historical rotated logs.

Prioritize call traces, machine checks, disk/NIC driver resets, firmware errors, filesystem remounts, watchdogs, and repeated hardware paths. Do not call hardware root cause from a single generic kernel warning without corroborating counters, repeated paths, or adjacent failures.

### Resource Pressure

For CPU, memory, disk, inode, file descriptor, process, or cgroup exhaustion, correlate pressure evidence with affected services and timestamps.

For OOM, identify victim process, cgroup/container, allocation context, node memory, swap, kubelet eviction messages, container termination reason if present, and whether application restarts or probe failures follow the kill.

For disk/inode pressure, distinguish data filesystem, root filesystem, logs, container image storage, kubelet pod volumes, overlayfs, and CSI mounts. A full container runtime partition can produce Kubernetes symptoms without an application bug.

### Storage And Filesystems

For storage incidents, check mount lifecycle, fstab/systemd mount units, filesystem errors, read-only remounts, NFS/iSCSI/multipath state, LVM/RAID state, disk latency, and application write errors.

Separate storage-control failures from application-level database initialization, migration, schema, or permission problems.

### Network, DNS, And Time

For reachability failures, work from local host outward:

1. Interface state, carrier, IP addresses, MTU, routes, VRFs/namespaces if present.
2. ARP/neighbor and gateway reachability.
3. Firewall, nftables/iptables, security groups, policy routing, reverse path filtering, conntrack.
4. DNS resolver config, search domains, upstream errors, split DNS, `/etc/hosts`.
5. TLS/certificate and clock validity.
6. Remote service listener and logs if available.

`No route to host`, `network is unreachable`, and ARP/neighbor failures point to host/path routing or L2/L3 reachability until disproven. `Connection refused` means the peer replied but no listener accepted the connection. `Timeout` needs correlation with packet drops, firewall policy, service overload, DNS, or remote unavailability.

For NTP/clock symptoms, check whether timeouts are external-only egress noise or whether local skew affects certificates, tokens, leases, distributed consensus, or logs.

### Security And Auth

For SSH, sudo, PAM, or authorization failures, correlate auth logs with user, source IP, session ID, command, PAM module, account lockout, key/certificate state, and SELinux/AppArmor/audit denials.

Redact secrets. Do not expose tokens, private keys, passwords, kubeconfigs, bearer tokens, cloud keys, certificates, or sensitive customer addresses unless essential, and then quote minimally.

### Containers And Kubernetes Nodes

For Kubernetes node symptoms, determine whether the Linux host is causing cluster fallout or merely reporting it.

Correlate kubelet/container runtime messages with:

- Node reachability to the API server and node lease updates.
- Container runtime health, image filesystem pressure, sandbox creation, CRI errors, and cgroup driver mismatches.
- CNI bridge/veth changes, routes, iptables/IPVS, conntrack, MTU, and plugin logs.
- Kubelet logs, node status updates, PLEG health, pod volume mounts, and eviction messages.
- Host DNS, NTP, firewall, proxy, and certificate state.

Repeated kubelet failures to reach `https://<api-server>:6443`, update node status, renew leases, or fetch service account tokens can explain pod and cluster symptoms. Prove whether the API endpoint is unreachable from one host, a subset of nodes, or all nodes before blaming kubelet itself.

## Timeline Rules

Build a timeline from the earliest high-signal event through recovery or collection end.

- Normalize timestamps across syslog, journal, kernel logs, application logs, auth logs, container logs, and file metadata.
- Linux logs may omit year and timezone. Infer year only from file metadata or surrounding evidence and label that inference.
- Account for locale differences such as `May` versus `Mai`, monotonic kernel timestamps, rotated logs, and previous-boot journal entries.
- Put automation actions, service restarts, node status changes, network failures, OOM kills, filesystem errors, and user sessions on the same timeline.

## Evidence Standards

Every important claim should cite concrete evidence:

- File path and line number, or command section and source file.
- Concise excerpt or summary of the relevant lines.
- Why the evidence matters.

Use labels:

- **Fact**: directly observed in evidence.
- **Inference**: reasoned from one or more facts.
- **Unknown**: missing, ambiguous, or inconclusive evidence.

Prefer corroborated conclusions over clever guesses. A root cause should explain timing, scope, affected hosts/services, and downstream symptoms better than alternatives.

## Output

Lead with the answer, then show evidence. Prefer a few strong findings over a long list of weak clues.

Use this final shape unless the user requests otherwise:

1. **Executive Summary**: most likely issue, scope/impact, confidence.
2. **Current Hypotheses**: statuses and why each strengthened, weakened, or remains open.
3. **Strongest Evidence**: supporting and refuting evidence with paths/lines or command sections.
4. **Timeline**: ordered key events with timestamp assumptions.
5. **Conclusion**: confirmed root cause if justified; otherwise most likely cause and remaining uncertainty.
6. **Next Actions**: safest remediation or exact additional evidence needed.

If evidence is insufficient, say so early and specify the missing discriminator, such as incident description, exact affected host/service, full `journalctl` window, `dmesg`, `systemctl status`, `ip addr/route/neigh`, `ss -tulpn`, firewall rules, DNS resolver config, disk/memory snapshots, kubelet/container runtime logs, pod/node state, packet capture, or logs from the peer endpoint.

## Safety

Prefer offline analysis and read-only live checks. Do not recommend disruptive commands casually. Avoid suggesting service restarts, node drains, kubelet/container runtime restarts, filesystem repair, route/firewall changes, package changes, or rebooting unless evidence supports them and safer validation steps are exhausted.
