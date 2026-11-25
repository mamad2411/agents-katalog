---
name: yocto-security-ota
description: Yocto security hardening and OTA/update skill for AI coding agents. Use for CVE checks, package/license review, firewall policy, SSH hardening, systemd security, read-only rootfs, dm-verity, secure boot, measured boot, signed artifacts, SBOM, SPDX, vulnerability triage, SWUpdate, RAUC, Mender, OSTree, A/B updates, rollback strategy, and production image hardening.
---

# Yocto Security OTA

## Workflow

1. Identify threat model, update model, physical access assumptions, recovery path, and regulatory constraints.
2. Inspect image package set, enabled services, network listeners, users, credentials, SSH policy, firewall, and debug features.
3. Check Yocto release security status, CVE tooling, license manifests, and SBOM/SPDX output.
4. Select update strategy: full image, package feed, A/B slots, bootloader-managed rollback, OSTree, RAUC, Mender, SWUpdate, or vendor OTA.
5. Tie secure boot and artifact signing to key management and manufacturing flows.
6. Verify with boot tests, rollback tests, power-cut tests, and update failure tests.

## References

- [security-ota-playbook.md](references/security-ota-playbook.md): hardening, CVE/SBOM, firewall, secure boot, and OTA workflows.

## Guardrails

- Do not promise security from package removal alone.
- Do not add firewall rules without documenting network services and default policy.
- Do not recommend OTA updates without rollback and recovery planning.
- Do not put signing keys, credentials, or production secrets in layers or CI logs.
