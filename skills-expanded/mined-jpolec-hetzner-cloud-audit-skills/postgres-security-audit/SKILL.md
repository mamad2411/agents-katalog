---
name: postgres-security-audit
description: Audit PostgreSQL authentication, authorization, transport, operations, and cross-layer reachability on authorized Hetzner infrastructure.
---

# PostgreSQL Security Audit

This is a read-only module. Use operator-provided configuration/query output or a database role limited to catalog inspection. Never alter roles, grants, settings, extensions, data, backups, or replication.

Collect effective `listen_addresses`, port/TLS settings, ordered `pg_hba.conf`, roles and role attributes, memberships, risky grants, public-schema privileges, relevant extensions, logging, version/support status, replication, backups, and restore-test evidence. Do not collect password hashes or application data.

Correlate in this order: Hetzner interface and routes → Hetzner firewall → host firewall → Docker publication/network → PostgreSQL bind → first matching HBA rule → authentication → role privilege. Run `hetzner-audit postgres --input snapshot.json --verify`.

Verify the exact selected HBA rule and source address. A broad `listen_addresses` is not by itself a finding when the network path is blocked. Cross-environment reachability that contradicts explicit isolation is a primary finding. Output evidence per layer, prerequisites, and the verifier's verdict.
