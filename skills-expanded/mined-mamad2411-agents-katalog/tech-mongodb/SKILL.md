---
name: tech-mongodb
description: MongoDB security review — identifies unauthenticated access, database and collection enumeration, document exposure, MongoDB Atlas API misconfiguration, sharded cluster exposure, oplog information disclosure, TLS configuration gaps, authentication mechanism weaknesses, and role-based access control over-permissioning. All probes are read-only MongoDB wire protocol commands via driver or mongo shell. No document modification, no database drop, no user creation, no data exfiltration, no oplog replay.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, blue-team, offensive, grey-hat]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft, mongodb-security-audit, collection-exposure-report]
---

# MongoDB security review

Use this skill to assess the security posture of MongoDB deployments, including standalone instances, replica sets, sharded clusters, and MongoDB Atlas. The review covers authentication configuration, anonymous access, database and collection enumeration, role-based access control (RBAC) analysis, network exposure, TLS configuration, and version-specific vulnerability assessment. All probes are read-only MongoDB commands that enumerate metadata (server status, database list, collection list, index definitions, user roles). This skill never queries document data beyond metadata, never modifies or deletes data, never creates users or roles, and never accesses the oplog or diagnostic data that may contain document contents.

## Required inputs

- MongoDB connection string or host:port (default: `mongodb://TARGET_IP:27017` or `mongodb://TARGET_IP:27018` for shard).
- Scope file confirming which database hosts are in scope.
- Authorization cache valid for the target host.
- Optional: MongoDB configuration file (`mongod.conf`) for offline review.
- Optional: MongoDB user credentials if authenticated review is requested.

## Required gates

1. `pentest_agent_load_config` and `pentest_agent_validate_policy` before any active probing.
2. `pentest_agent_parse_scope` and `pentest_agent_validate_target` for the MongoDB host before connection.
3. `pentest_agent_check_authorization` before any database connection.
4. `pentest_agent_build_command` for dry-run argv preview.
5. `pentest_agent_execute_tool` for all live probing — rate-limit enforcement, approval.
6. `pentest_agent_append_evidence` with redacted output.

## Workflow

### Phase 1 — Server discovery and authentication check

1. **Basic connectivity test**:
   - `mongosh --quiet --eval "db.version()" mongodb://TARGET_IP:27017 2>&1`.
   - If returns version string → MongoDB accessible. If returns "MongoServerError: Authentication failed" → auth required. If "connect ECONNREFUSED" → port closed or firewalled.
2. **Unauthenticated server info** (read-only, low-noise):
   - `mongosh --quiet --eval "JSON.stringify(db.adminCommand({buildInfo: 1}), null, 2)" mongodb://TARGET_IP:27017 2>&1`.
   - Returns: `version`, `gitVersion`, `modules`, `buildEnvironment`, `openssl` version, `bits` (32/64), `javascriptEngine`.
   - **Finding**: returns data without auth → CRITICAL. MongoDB has enforced authentication by default since version 3.6 (2018), but older instances and misconfigurations persist.
   - Pre-3.0 MongoDB had no authentication at all by default. Pre-3.6 had `localhost` exception — auth required for network connections but localhost could bypass it.
3. **Server status** (requires `clusterMonitor` role in authenticated context):
   - `mongosh --quiet --eval "JSON.stringify(db.adminCommand({serverStatus: 1}).connections, null, 2)" mongodb://TARGET_IP:27017 2>&1`.
   - Key fields: `current` (active connections), `available` (remaining connection slots), `totalCreated` (connections since start), `active` (currently executing operations).
   - **Finding**: accessible without auth → MEDIUM (operational information disclosure).
4. **Host info** (`hostInfo` command):
   - `mongosh --quiet --eval "JSON.stringify(db.adminCommand({hostInfo: 1}).system, null, 2)" mongodb://TARGET_IP:27017 2>&1`.
   - Returns: OS name, OS version, hostname, CPU architecture, memory size, CPU count.
   - **Finding**: OS details exposed → MEDIUM (useful for targeted exploits).

### Phase 2 — Database and collection enumeration

If the server allows unauthenticated access, enumerate the database structure.

1. **List databases**:
   - `mongosh --quiet --eval "JSON.stringify(db.adminCommand({listDatabases: 1}).databases.map(d => ({name: d.name, sizeOnDisk: d.sizeOnDisk})), null, 2)" mongodb://TARGET_IP:27017 2>&1`.
   - **Finding**: database list without auth → HIGH. Reveals all database names and disk sizes.
   - Common sensitive database names: `admin`, `config`, `local` (system DBs), `users`, `accounts`, `customers`, `orders`, `transactions`, `payments`, `auth`, `credentials`, `secrets`, `sessions`, `tokens`.
2. **List collections per database**:
   - `mongosh --quiet --eval "JSON.stringify(db.getSiblingDB('DATABASE_NAME').getCollectionNames(), null, 2)" mongodb://TARGET_IP:27017 2>&1`.
   - **Finding**: collection names exposed → MEDIUM to HIGH. Collection names like `users`, `passwords`, `creditCards`, `apiKeys`, `sessions` directly reveal data structure.
3. **Index enumeration** (metadata only):
   - `mongosh --quiet --eval "JSON.stringify(db.getSiblingDB('DATABASE_NAME').COLLECTION_NAME.getIndexes(), null, 2)" mongodb://TARGET_IP:27017 2>&1`.
   - Returns index keys and options. Index definitions reveal which fields are queried most often: `{email: 1}` (email lookup), `{token: 1}` (token lookup), `{userId: 1}` (user-to-document join).
   - **Finding**: indices reveal query patterns and field names → LOW informational.
4. **Collection stats** (metadata only, no document data):
   - `mongosh --quiet --eval "JSON.stringify(db.getSiblingDB('DATABASE_NAME').COLLECTION_NAME.stats({scale: 1024}), null, 2)" mongodb://TARGET_IP:27017 2>&1`.
   - Returns: document `count`, average `size`, `storageSize`, `totalIndexSize`, `nindexes`.
   - **PROHIBITED**: do not query documents. Use only metadata commands (`stats`, `getIndexes`, `listCollections`, `listDatabases`).

### Phase 3 — Authentication and RBAC analysis

If authenticated with valid credentials, review the security configuration.

1. **Authentication mechanism** (from `buildInfo` or `serverStatus`):
   - `mongosh --quiet --eval "JSON.stringify(db.adminCommand({getCmdLineOpts: 1}).parsed.security, null, 2)" mongodb://TARGET_IP:27017 2>&1` (requires `clusterMonitor`).
   - Check: `authorization: enabled` — if absent or `disabled` → CRITICAL. No access control at all.
   - Authentication mechanisms: `SCRAM-SHA-1` (weak, deprecated since 5.0), `SCRAM-SHA-256` (current standard), `MONGODB-X509` (client certificate), `MONGODB-AWS` (IAM), `GSSAPI` (Kerberos/LDAP).
   - **Finding**: SCRAM-SHA-1 still enabled → MEDIUM. SHA-1 is cryptographically weak.
   - **Finding**: `transitionToAuth: true` → cluster is in migration; some nodes may not enforce auth. MEDIUM.
2. **User enumeration** (requires `viewUser` privilege):
   - `mongosh --quiet --eval "JSON.stringify(db.getSiblingDB('admin').getUsers().map(u => ({user: u.user, roles: u.roles, mechanisms: Object.keys(u.mechanisms || {})})), null, 2)" mongodb://TARGET_IP:27017 2>&1`.
   - **Finding**: over-privileged users → `root` role on a user, `__system` role, `userAdminAnyDatabase` without scoping. CRITICAL.
   - **Finding**: users with empty password or `pwd` field that matches a known-weak hash format. HIGH.
3. **Custom role enumeration**:
   - `mongosh --quiet --eval "JSON.stringify(db.getSiblingDB('admin').getRoles({showPrivileges: true}), null, 2)" mongodb://TARGET_IP:27017 2>&1`.
   - Check for roles with: `anyResource: true` combined with `actions` that include `find`, `insert`, `update`, `remove` on all databases. HIGH.

### Phase 4 — Sharding and replica set security

1. **Replica set status** (metadata, no data):
   - `mongosh --quiet --eval "JSON.stringify(db.adminCommand({replSetGetStatus: 1}).members.map(m => ({name: m.name, stateStr: m.stateStr, health: m.health})), null, 2)" mongodb://TARGET_IP:27017 2>&1`.
   - Reveals all replica set member hostnames and health status. MEDIUM.
2. **Shard status**:
   - `mongosh --quiet --eval "JSON.stringify(db.adminCommand({listShards: 1}).shards.map(s => ({id: s._id, host: s.host})), null, 2)" mongodb://TARGET_IP:27017 2>&1`.
   - Reveals all shard hostnames. MEDIUM.
3. **Config server access**:
   - Config servers store sharding metadata. If accessible without auth, an attacker can learn the entire cluster topology and database/chunk distribution.
   - **Finding**: config server accessible → HIGH.

### Phase 5 — Network exposure and TLS

1. **Listening interface check** (from `getCmdLineOpts` or `netstat`):
   - `net.bindIp` in `mongod.conf`: `0.0.0.0` → listening on all interfaces. HIGH if no firewall or authentication.
   - Default changed in MongoDB 3.6+ to `127.0.0.1` only. Older installs defaulted to all interfaces.
2. **TLS configuration** (from `getCmdLineOpts`):
   - `net.ssl.mode`: `disabled` → no TLS. ALL data transmitted in plaintext. CRITICAL if combined with internet exposure.
   - `net.ssl.mode: allowSSL` → TLS optional, downgrade possible. MEDIUM.
   - `net.ssl.mode: preferSSL` → TLS preferred but fallback. MEDIUM.
   - `net.ssl.mode: requireSSL` → TLS enforced. OK.
   - **Finding**: no TLS on internet-facing MongoDB → CRITICAL.
3. **MongoDB Express / web admin panels**:
   - Check for `mongo-express` on common web ports (8081, 8080). These web interfaces often lack authentication or use default credentials. HIGH if accessible.

### Phase 6 — Version-specific vulnerability assessment

1. **MongoDB version CVE cross-reference**:
   - MongoDB < 3.0: no authentication by default. CRITICAL.
   - MongoDB < 3.6: localhost exception allows bypass on localhost. MEDIUM if on shared host.
   - CVE-2019-2386: user privilege escalation via `applyOps`. MongoDB < 4.0.9. HIGH.
   - CVE-2020-7921: authorization bypass via crafted `$regex` operators. MongoDB < 4.4.1. HIGH.
   - CVE-2021-20330: denial of service via specific `find` queries. MEDIUM.
   - CVE-2023-0436: information disclosure via side-channel in TLS. MEDIUM.
2. **End-of-life version check**:
   - MongoDB 4.0: EOL April 2022.
   - MongoDB 4.2: EOL April 2023.
   - MongoDB 4.4: EOL February 2024.
   - MongoDB 5.0: expected EOL October 2024.
   - MongoDB 6.0+: current.
   - EOL version → MEDIUM (no security patches).

## Decision points

- **Unauthenticated access but the database appears empty** (no databases beyond `admin`, `local`, `config`): still a finding. An empty unauthenticated MongoDB can still be used by an attacker to store data (e.g., stolen data, malware payloads). Access itself is a CRITICAL configuration gap.
- **SCRAM-SHA-1 is the only mechanism**: SHA-1 collision resistance is broken. Recommend upgrading to SCRAM-SHA-256 and re-creating user credentials. MEDIUM.
- **`localhost` exception is needed for automation scripts**: MongoDB ≥ 5.0 removed the `localhost` exception. For earlier versions, if the automation is on localhost, ensure the automation account has a proper password.
- **MongoDB Express panel is accessible but requires login**: do not attempt login. Document the exposure. HIGH if internet-facing.

## Prohibited behavior

- Querying or dumping document data (`find`, `aggregate`, `findOne`, `mapReduce`).
- Creating, modifying, or deleting databases, collections, or documents.
- Creating, deleting, or modifying users and roles.
- Running diagnostic commands that extract data (`getLog`, `validate`, `currentOp` with query details, `explain` on find queries).
- Accessing or replaying the oplog.
- Connecting to config servers or shards beyond topology enumeration.
- Brute-forcing authentication.
- Executing JavaScript functions via `$where` or `eval`.

## Stop conditions

- `listDatabases` returns a database named `passwords`, `secrets`, `credentials`, or `tokens` → CRITICAL. Document the database name; do not enumerate collections or data.
- Server version is < 3.0 → CRITICAL. No authentication existed by default.
- `getCmdLineOpts` reveals `security.authorization: disabled` → CRITICAL. Stop probing and document.
- Any document data appears in command output (e.g., `hostInfo` containing unexpected system secrets) → stop and redact.

## Evidence

For each finding, record: host:port, finding type, access level, severity, and remediation. Evidence template:

```text
MongoDB security review for: [TARGET_IP:PORT]
MongoDB version: [VERSION]
Review date: [DATE]

Authentication:
  Authorization enabled: [yes / no (CRITICAL)]
  Auth mechanism: [SCRAM-SHA-256 / SCRAM-SHA-1 (MEDIUM) / MONGODB-X509 / none]
  Default (localhost exception): [present / removed (OK)]

Anonymous access findings:
  Server info readable: [yes (CRITICAL — no auth) / no (auth required)]
  Database list accessible: [yes — N databases (HIGH) / no]
  Collection metadata accessible: [yes — N collections (MEDIUM) / no]

Database exposure:
  Databases found: [N] — [NAMES redacted if sensitive]
  Collections per DB (avg): [N]
  Estimated documents: [N] total (from collection stats)

RBAC analysis (authenticated):
  Users with root role: [N]
  Users with __system role: [N]
  Custom roles: [N]
  Roles with anyResource: [N]

Network and TLS:
  Bind IP: [127.0.0.1 (OK) / 0.0.0.0 (HIGH) / specific IP]
  TLS mode: [requireSSL (OK) / preferSSL / allowSSL / disabled (CRITICAL)]
  Internet-facing: [yes / no]

Vulnerabilities:
  EOL version: [yes (MEDIUM) / no]
  Known CVEs: [N] relevant

Redaction notes:
  - No document data was queried or stored.
  - Database and collection names containing PII or credential hints are redacted.
  - No users were created, modified, or deleted.
  - No oplog data was accessed.
  - All enumeration was read-only metadata commands.
```

## Report handoff

1. `pentest_agent_record_finding` for each finding with: host, finding type, severity, remediation (specific `mongod.conf` change, user role change, TLS configuration), and verification test.
2. Priority matrix: CRITICAL (no authentication, authorization disabled, internet-facing without TLS, pre-3.0 version). HIGH (database list accessible, collection metadata accessible, users with root role, SCRAM-SHA-1 only). MEDIUM (no TLS on internal network, EOL version, config server accessible, `bindIp` 0.0.0.0 behind firewall). LOW (collection stats, index definitions, replica set member names).
3. Provide a MongoDB hardening checklist: enable authorization (`security.authorization: enabled`), use SCRAM-SHA-256, bind to specific internal IPs, enable TLS with `requireSSL`, implement network-level firewall rules, use MongoDB Atlas or Ops Manager for monitoring, limit user roles to least privilege, and upgrade to a supported version.
4. Explicitly note: no document data was queried, no databases or collections were created or modified, no users or roles were changed, and all probes were read-only metadata commands.
