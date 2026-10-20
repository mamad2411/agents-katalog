---
name: secure-os
description: Audit and harden operating systems and network devices — scan a Linux, macOS, or Windows host (or a container image, or network gear like Cisco/Arista/Fortinet/Juniper/PAN-OS) against CIS and vendor benchmarks with cnspec, surfacing misconfigurations and vulnerable packages mapped to compliance. Use to check a server, workstation, image, or device's security posture.
allowed-tools: Bash Read
---

# Secure OS

Check whether an operating system or network device is configured and patched securely, by
running [cnspec](https://github.com/mondoohq/cnspec) against it. cnspec carries the policies;
this skill routes the outcome ("is this host hardened?") to the right scan and reads the result.

## When to use

- Auditing a server, workstation, VM, or container image against a CIS / vendor benchmark.
- Checking a host for missing patches and vulnerable packages.
- Hardening a network device (Cisco IOS-XE/-XR/NX-OS, Arista EOS, FortiOS, Junos, PAN-OS).

For scanning the *code* or *IaC* an agent writes, use `secure-pipeline` instead — this skill is
for the posture of a running (or imaged) system.

## What cnspec checks

cnspec ships hardening + vulnerability policies for, among others:

- **Linux** — `mondoo-linux-security`, `mondoo-linux-workstation-security`, operational/SNMP policies
- **macOS** — `mondoo-macos-security`
- **Windows** — `mondoo-windows-security`, `mondoo-windows-workstation-security`, update readiness
- **Network devices** — `mondoo-cisco-iosxe/iosxr/nxos-security`, `mondoo-arista-eos-security`,
  `mondoo-fortios-security`, `mondoo-junos-security`, `mondoo-panos-security`

## Run a scan

```bash
cnspec scan local                       -o sarif   # the machine you're on
cnspec scan ssh <user>@<host>           -o sarif   # a remote host over SSH
cnspec scan docker <image|container>    -o sarif   # a container image or running container
# network devices connect over SSH / vendor API — see the cnspec provider docs
```

- Logged in to Mondoo Platform, cnspec runs the policies assigned to the asset automatically.
  Otherwise add `--incognito` and `-f <bundle>` (e.g. `-f mondoo-linux-security.mql.yaml`) to run
  a specific bundle locally — see [cnspec install & usage](https://mondoo.com/docs/cnspec/).
- `-o sarif` emits findings for a code-review UI / CI gate; cnspec exits non-zero on failures.

## Reference, don't duplicate

cnspec owns the policies and their authoring (its `mql` / `policy-graph` skills live in the
[cnspec repo](https://github.com/mondoohq/cnspec/tree/main/skills)). This skill invokes cnspec
and interprets results — it does not reimplement policy. For the exact provider connection and
auth per target, follow the [cnspec docs](https://mondoo.com/docs/cnspec/).

## Compliance

cnspec policies carry framework mappings (CIS benchmarks, DISA STIG, SOC 2, ISO 27001, PCI-DSS,
and vendor hardening guides), so a scan doubles as a compliance check — filter or report by the
framework you need.

## Part of the secure-your-stack toolkit

`secure-os` is the **host/device** pillar of posture. Its siblings cover the rest of what you
run — `secure-cloud` (cloud accounts), `secure-saas` (SaaS & identity), `secure-ai-services`
(AI services & tooling) — while the secure development skills (`secure-coding`,
`secure-pipeline`, …) secure the code you ship onto these systems. Needs `cnspec`
([install](https://mondoo.com/docs/cnspec/install)) plus access to the target.
