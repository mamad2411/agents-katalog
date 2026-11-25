---
name: hetzner-cloud-audit
description: Collect and assess authorized Hetzner Cloud assets in read-only mode as part of a Hetzner security audit.
---

# Hetzner Cloud Audit

Use for Hetzner servers, types, images, locations, networks/routes, firewalls, IPs, load balancers, volumes, snapshots/backups, SSH keys, labels, placement groups, and certificates.

Required permission: an authorized project token created with **Read** permission and supplied only as `HCLOUD_TOKEN`. Allowed actions are API `GET` operations. Never log the token. Provider changes, power actions, console access, deletes, or firewall edits are prohibited. For exact setup and revocation, use the project's [read-only token guide](https://github.com/jpolec/hetzner-cloud-audit-skills/blob/main/docs/token-setup.md).

For live collection, direct the operator to the target project in Hetzner Console: **Security → API tokens → Generate API token → Read**. Do not ask them to paste the value into chat. Hetzner shows the full token only once and binds it to that project. The collector must not attempt a write to prove that the permission is read-only.

Workflow: run `hetzner-audit inventory --format json --read-only --no-ssh`; record successful and failed endpoints; normalize IDs, public interfaces, labels, firewall attachments, network membership, protection and backup state; emit facts only. Compare labels and observed state to explicit expectations only after collection. Missing evidence is `unknown`, not `false`.

Expected output: assets, edges, evidence timestamps, endpoint coverage, and candidate inputs. Verify asset identity, firewall attachment, pagination completeness, and collection errors before using absence as evidence.
