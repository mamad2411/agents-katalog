---
name: linux-security-audit
description: Perform explicitly authorized, read-only Linux host inspection for a cross-layer Hetzner audit.
---

# Linux Host Security Audit

Prefer the owner-run bundle: `hetzner-audit host-bundle > host-bundle.sh`, show it to the owner, let them run it (`ssh HOST 'sudo HETZNER_AUDIT_SERVER=<server name> sh -s' < host-bundle.sh > HOST.bundle`), and pass the output with `--host-bundle`. The agent never runs it over SSH itself unless the operator explicitly asks.

Use only when the operator explicitly enables SSH or supplies a host fixture. Required permission is a least-privilege inspection account. Never use `sudo` unless separately approved; never change files, packages, services, firewall state, or authentication.

Allowed commands are bounded reads such as `ss -lntup`, `sshd -T`, `uname -a`, package update simulation/status, `systemctl list-units`, `systemctl cat <named-unit>`, `ufw status`, `nft list ruleset`, `iptables-save`, mount metadata, and narrowly scoped permission metadata. Do not read secret contents or enumerate unrelated home directories.

Collect sshd effective settings, listening sockets/binds, firewall policy, kernel/packages, update automation, AppArmor/SELinux, auditd, scheduled services, world-writable executable paths, mounts, and Docker socket permissions. Correlate sockets with Hetzner reachability. Verify effective configuration and compensating controls; return facts and candidates, never self-confirmed findings.

