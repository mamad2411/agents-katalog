---
name: tech-redis
description: Redis security review — identifies unauthenticated access, key enumeration and data exposure, CONFIG command abuse potential (directory and file write), replication and slave configuration risks, protected-mode bypass scenarios, ACL and user permission misconfigurations (Redis 6+), command renaming gaps, module loading risks, Lua script execution exposure, and version-specific vulnerabilities. All probes are read-only Redis commands. No key modification, no CONFIG write, no module loading, no replica creation, no data exfiltration.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, blue-team, offensive, grey-hat]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft, redis-security-audit, key-exposure-report]
---

# Redis security review

Use this skill to assess the security posture of Redis servers. The review covers authentication configuration, network exposure, key space enumeration, configuration command accessibility, dangerous runtime settings, ACL models (Redis 6+), replication security, module loading capability, and Lua script execution surfaces. All probes are read-only Redis commands that inspect configuration, enumerate key metadata, and evaluate permission boundaries. This skill never modifies keys, writes configuration, loads modules, creates replicas, or runs Lua scripts beyond confirming execution availability. Redis is designed as a high-performance in-memory data store and is vulnerable by design when exposed without proper hardening.

## Required inputs

- Redis server host:port (default: `TARGET_IP:6379`).
- Optional: Redis password if authentication is configured (for authenticated review).
- Scope file confirming which hosts are in scope.
- Authorization cache valid for the target host.
- Optional: `redis.conf` for offline security review.

## Required gates

1. `pentest_agent_load_config` and `pentest_agent_validate_policy` before any active probing.
2. `pentest_agent_parse_scope` and `pentest_agent_validate_target` for the Redis host before connection.
3. `pentest_agent_check_authorization` before any Redis connection.
4. `pentest_agent_build_command` for dry-run argv preview.
5. `pentest_agent_execute_tool` for all live probing — rate-limit enforcement, approval.
6. `pentest_agent_append_evidence` with redacted output.

## Workflow

### Phase 1 — Server discovery and authentication check

1. **Basic PING check** (read-only, minimal noise):
   - `echo -e "PING\r\nQUIT\r\n" | nc -w 3 TARGET_IP 6379`. If `+PONG` → Redis accessible.
   - `redis-cli -h TARGET_IP -p 6379 --no-auth-warning PING 2>&1`. If `PONG` → no authentication required. CRITICAL.
   - If `NOAUTH Authentication required.` → authentication is enabled. Document as positive control.
2. **Server information** (unauthenticated `INFO`, read-only):
   - `redis-cli -h TARGET_IP -p 6379 --no-auth-warning INFO server 2>&1`.
   - Key fields: `redis_version`, `redis_mode` (standalone, sentinel, cluster), `os` (Linux, Darwin), `arch_bits`, `multiplexing_api`, `gcc_version`, `process_id`, `tcp_port`, `uptime_in_seconds`, `uptime_in_days`, `executable` (path to redis-server binary).
   - **Finding**: `INFO` accessible without auth → CRITICAL. Full server details exposed.
   - `INFO` reveals: server version, OS, uptime (how long since restart), connected clients count, used memory, replication role, cluster status, and keyspace statistics.
3. **Connected client information**:
   - `redis-cli -h TARGET_IP -p 6379 --no-auth-warning CLIENT LIST 2>&1`.
   - Returns every active client connection: `id`, `addr`, `fd`, `name`, `age`, `idle`, `flags`, `db`, `sub`, `psub`, `cmd`.
   - Client IP addresses are exposed → MEDIUM (operational data leak).
4. **Configuration dump** (unauthenticated `CONFIG GET *`, read-only):
   - `redis-cli -h TARGET_IP -p 6379 --no-auth-warning CONFIG GET '*' 2>&1`.
   - CRITICAL finding if successful without auth. Reveals every runtime configuration including:
     - `requirepass` (password setting — value itself if auth is set, or empty if not).
     - `masterauth` (password for the master if this is a replica).
     - `dir` (working directory — used for RDB/rewrite attacks).
     - `dbfilename` (RDB filename).
     - `bind` (listening interfaces).
     - `protected-mode` (safety feature that restricts access when no password is set).
     - `rename-command` (which commands are renamed/disabled).
     - `slave-read-only` (whether replicas accept writes).
     - `repl-diskless-sync` (replication settings).
   - **PROHIBITED**: do not record the value of `requirepass` or `masterauth` if they are set. Document only whether they are set.
5. **Protected mode status**:
   - Redis ≥ 3.2 has "protected mode" enabled by default. When protected mode is on AND no password is set AND `bind` is not explicitly set, Redis only accepts connections from `127.0.0.1` or `::1`.
   - Check via `CONFIG GET protected-mode`. If `yes` → connections from external IPs are rejected. This is a safety measure that prevents accidental exposure. If `no` → and no password → CRITICAL.

### Phase 2 — ACL analysis (Redis 6+)

Redis 6 introduced Access Control Lists (ACLs) for fine-grained user permissions.

1. **ACL list** (requires authentication or unrestricted `ACL LIST`):
   - `redis-cli -h TARGET_IP -p 6379 --no-auth-warning ACL LIST 2>&1`.
   - Returns every user definition: `user default on nopass ~* &* +@all` → `default` user with no password, all keys, all channels, all commands. CRITICAL.
   - `nopass` → no password required for this user. HIGH risk if the user has dangerous permissions.
   - `on` → user is enabled. `off` → disabled.
   - `+@all` → all commands allowed. `+@admin +@dangerous` → administrative and dangerous commands allowed.
   - `~*` → all keys accessible. `~prefix:*` → only keys with prefix.
   - `&*` → all pub/sub channels accessible.
   - **Finding**: `ACL LIST` accessible without auth → CRITICAL. User definitions exposed.
2. **Current user check**:
   - `redis-cli -h TARGET_IP -p 6379 --no-auth-warning ACL WHOAMI 2>&1`.
   - Reveals which user the current connection is authenticated as. If `default` with unrestricted permissions → CRITICAL.
3. **ACL categories** (permission groups):
   - `redis-cli -h TARGET_IP -p 6379 --no-auth-warning ACL CAT 2>&1` — lists all command categories.
   - Dangerous categories: `@admin` (CONFIG, DEBUG, SAVE, SHUTDOWN), `@dangerous` (FLUSHDB, FLUSHALL, KEYS, MIGRATE, RESTORE, SORT, SORT_RO), `@slow` (KEYS, SCAN, FLUSHALL, FLUSHDB), `@keyspace` (all read/write key commands), `@write` (all key mutations).
   - If current user has `+@admin` or `+@dangerous` → HIGH finding.

### Phase 3 — Keyspace enumeration and data exposure assessment

If the server is accessible, enumerate key space and assess data sensitivity.

1. **Keyspace statistics** (from `INFO keyspace`):
   - `redis-cli -h TARGET_IP -p 6379 --no-auth-warning INFO keyspace 2>&1`.
   - Returns: `db0:keys=15423,expires=432,avg_ttl=86400000` — total keys, keys with expiry, average TTL per database.
   - **Finding**: key count revealed → MEDIUM. An attacker knows how much data is cached.
2. **Key enumeration** (metadata only, no commands that output data):
   - `redis-cli -h TARGET_IP -p 6379 --no-auth-warning DBSIZE 2>&1` — returns count of keys in current database. LOW.
   - `redis-cli -h TARGET_IP -p 6379 --no-auth-warning SCAN 0 COUNT 10 2>&1` — iterates keys in batches. Returns key names.
   - **PROHIBITED**: do not use `KEYS *` (blocking, slow, dangerous on production). Use `SCAN` with small COUNT (10-20 max).
   - Key naming patterns to flag: `session:`, `jwt:`, `token:`, `user:`, `auth:`, `cred:`, `api_key:`, `secret:`, `password:`, `credit_card:`, `payment:`, `cart:`, `ratelimit:`, `cache:`, `queue:`.
   - **STOP**: if key names contain session IDs, JWTs, tokens, or PII → document the naming pattern without storing the full key names. Limit to 10-20 keys scanned.
3. **Key type check** (schema inspection only):
   - For representative keys: `redis-cli -h TARGET_IP -p 6379 --no-auth-warning TYPE KEY_NAME 2>&1`.
   - Returns: `string`, `list`, `set`, `zset`, `hash`, `stream`. Does NOT read data.
   - **PROHIBITED**: do not use `GET`, `LRANGE`, `SMEMBERS`, `HGETALL`, `ZRANGE`, or any command that returns data values.
4. **Memory usage inspection** (metadata):
   - `redis-cli -h TARGET_IP -p 6379 --no-auth-warning MEMORY USAGE KEY_NAME 2>&1` — returns bytes used by a key. Does not expose data.

### Phase 4 — Dangerous configuration and write-surface assessment

The `CONFIG` command can be used to write files to disk, enabling RCE. Do not exploit — document the risk only.

1. **Directory write capability** (inspect, never execute):
   - `redis-cli -h TARGET_IP -p 6379 --no-auth-warning CONFIG GET dir 2>&1` — reveals current working directory.
   - `redis-cli -h TARGET_IP -p 6379 --no-auth-warning CONFIG GET dbfilename 2>&1` — reveals RDB filename (default: `dump.rdb`).
   - If `CONFIG SET dir` and `CONFIG SET dbfilename` are not disabled → an attacker can write the RDB to arbitrary paths. This is the basis for Redis RCE:
     - Write to `/var/spool/cron/` → cron job injection.
     - Write to `/root/.ssh/authorized_keys` → SSH key injection.
     - Write to `/var/www/html/` → web shell drop.
   - **Finding**: `CONFIG SET` commands not disabled → CRITICAL.
   - **Finding**: `dir` is writable and user-controllable → CRITICAL.
   - **PROHIBITED**: do not execute `CONFIG SET` to change any setting. Document risk only.
2. **Command renaming** (defense check):
   - `redis-cli -h TARGET_IP -p 6379 --no-auth-warning CONFIG GET rename-command 2>&1`.
   - If `CONFIG` is renamed to an empty string (e.g., `rename-command CONFIG ""`) → `CONFIG` is disabled. This is a strong security control. Positive.
   - Also check: `FLUSHDB`, `FLUSHALL`, `DEBUG`, `SHUTDOWN`, `SLAVEOF`, `REPLICAOF`, `MODULE`, `EVAL`, `SCRIPT` — all should be disabled or renamed on production.
   - **Finding**: dangerous commands not renamed → MEDIUM to HIGH depending on authentication state.
3. **Replication configuration** (inspect, never modify):
   - `redis-cli -h TARGET_IP -p 6379 --no-auth-warning INFO replication 2>&1`.
   - Reveals replication role: `role:master` or `role:slave`. If master, lists connected replicas. If replica, lists master host and port, link status.
   - **Finding**: `SLAVEOF` / `REPLICAOF` not disabled → an attacker can make this instance a replica of an attacker-controlled master, syncing all data off-site. CRITICAL.
4. **Module loading** (check, never execute):
   - `redis-cli -h TARGET_IP -p 6379 --no-auth-warning MODULE LIST 2>&1`.
   - If loaded modules exist, they may extend Redis functionality with custom commands.
   - **Finding**: `MODULE LOAD` not disabled → CRITICAL. Arbitrary `.so` module loading enables full system compromise.
   - **PROHIBITED**: do not attempt `MODULE LOAD`.

### Phase 5 — Lua scripting surface

Lua scripts can access Redis internals.

1. **Script execution availability** (check, never execute):
   - `redis-cli -h TARGET_IP -p 6379 --no-auth-warning SCRIPT EXISTS 0 2>&1`.
   - If the command returns a response (not "unknown command") → Lua scripting is available.
   - **Finding**: `EVAL` not disabled → MEDIUM (Lua sandbox escapes are rare but have existed; scripts can block Redis for extended periods).
   - **PROHIBITED**: do not execute `EVAL` or `EVALSHA` with any script, including no-ops.
2. **Function availability** (Redis 7+):
   - `redis-cli -h TARGET_IP -p 6379 --no-auth-warning FUNCTION LIST 2>&1`.
   - Redis Functions replace Lua scripts in Redis 7+. Same risk profile.

### Phase 6 — Network exposure and bind configuration

1. **Listening interfaces** (`CONFIG GET bind`):
   - `bind 127.0.0.1` → only localhost. Secure.
   - `bind 0.0.0.0` or `bind` empty → listening on all interfaces. HIGH if no firewall or auth.
   - Multiple IPs: `bind 10.0.0.5 127.0.0.1` — restricted to two interfaces.
2. **Firewall check**:
   - If the test origin is external and `PING` succeeds, the port is exposed through the firewall. HIGH.
3. **TLS support**:
   - Redis ≥ 6.0 supports TLS natively (`tls-port`, `tls-cert-file`, `tls-key-file`).
   - Pre-6.0: no TLS. stunnel or HAProxy required for encryption.
   - **Finding**: no TLS on internet-facing Redis → CRITICAL.

### Phase 7 — Version-specific vulnerability assessment

1. **Redis version CVE cross-reference**:
   - Redis < 2.8: no authentication at all. CRITICAL.
   - Redis 2.8 — 3.2.x: Lua sandbox escape via `cmsgpack` / `cjson` (CVE-2015-4335, CVE-2016-8339). CRITICAL if version in range and `EVAL` not disabled.
   - Redis 4.x: `MODULE LOAD` unrestricted. CRITICAL.
   - Redis 5.x: heap buffer overflow in hyperloglog (CVE-2021-32675, CVE-2021-32687). HIGH.
   - Redis 6.x: ACL bypass via specially crafted commands (CVE-2021-41099). MEDIUM.
   - Redis 7.x: integer overflow in `XAUTOCLAIM` (CVE-2022-35951). MEDIUM.
2. **End-of-life version**:
   - Redis 4.x: EOL.
   - Redis 5.x: EOL.
   - Redis 6.x: in extended support.
   - Redis 7.x: current.
   - EOL → MEDIUM.

## Decision points

- **`protected-mode` is `yes` but `bind` is set to a public IP**: protected mode disengages when `bind` is explicitly set. The safety feature only applies to default `bind` configurations. This is intentional Redis behavior but counterintuitive. Flag the combination of `bind` to a public IP + no password as CRITICAL.
- **`SCAN` returns key names that appear to be user IDs/emails**: document the pattern (e.g., "keys match pattern `user:*`") without storing the actual key names.
- **Redis is used as a cache-only, no persistent data**: the server is still a target. A compromised Redis can be used for malware staging, cryptomining proxy, or lateral movement.

## Prohibited behavior

- Reading data values via `GET`, `LRANGE`, `HGETALL`, `SMEMBERS`, `ZRANGE`, `GETRANGE`, or any data-access command.
- Modifying or deleting keys (`SET`, `DEL`, `FLUSHDB`, `FLUSHALL`, `RENAME`, `EXPIRE`, `PERSIST`).
- Modifying configuration (`CONFIG SET`, `CONFIG REWRITE`).
- Enabling or creating replicas (`SLAVEOF`, `REPLICAOF`).
- Loading modules (`MODULE LOAD`).
- Executing Lua scripts (`EVAL`, `EVALSHA`, `FUNCTION LOAD`).
- Triggering persistence (`SAVE`, `BGSAVE`, `BGREWRITEAOF`).
- Shutting down or restarting (`SHUTDOWN`, `DEBUG RESTART`).
- Brute-forcing `AUTH` with common passwords beyond checking if `nopass` is set.
- Using `KEYS *` instead of `SCAN`.

## Stop conditions

- `CONFIG GET requirepass` reveals a password → document that authentication IS configured. Redact the password value. Do not attempt to authenticate with it.
- `CONFIG GET masterauth` reveals a non-empty value → document that replication authentication is configured. Redact the value.
- `SCAN` reveals keys containing session tokens, JWTs, or PII → stop key enumeration. Document the key naming pattern.
- `ACL LIST` reveals user definitions without auth → CRITICAL. Document the ACL configuration.
- `CONFIG SET` is not disabled and the server is internet-facing → CRITICAL. Document the RCE risk.

## Evidence

For each finding, record: host:port, finding type, command, access level, severity, and remediation. Evidence template:

```text
Redis security review for: [TARGET_IP:PORT]
Redis version: [VERSION]
Redis mode: [standalone / sentinel / cluster]
Review date: [DATE]

Authentication:
  Password set: [yes (OK) / no (CRITICAL)]
  Protected mode: [yes — external blocked / no (CRITICAL if no password)]
  ACL enabled: [yes — Redis 6+/7 / no (pre-6 ACLs not available)]

Access findings:
  INFO accessible: [yes (CRITICAL — no auth) / no]
  CONFIG GET accessible: [yes (CRITICAL — no auth) / no]
  CLIENT LIST accessible: [yes (MEDIUM) / no]
  ACL LIST accessible: [yes (CRITICAL) / no / N/A]
  Keyspace stats: [N] databases, [N] total keys

Keyspace:
  Keys sampled: [N] via SCAN
  Key patterns: [user:* / session:* / cache:* / etc — redacted if sensitive]
  Key types: [string / hash / list / set / zset / stream]

Dangerous commands:
  CONFIG SET disabled: [yes (OK) / no (CRITICAL)]
  EVAL disabled: [yes / no (MEDIUM)]
  SLAVEOF/REPLICAOF disabled: [yes / no (CRITICAL)]
  MODULE LOAD disabled: [yes / no (CRITICAL)]
  FLUSHDB/FLUSHALL disabled: [yes / no (MEDIUM)]
  SHUTDOWN disabled: [yes / no (LOW)]

Network:
  Bind: [127.0.0.1 (OK) / 0.0.0.0 (HIGH) / specific IP]
  TLS: [enabled (OK) / not available (pre-6) / disabled (CRITICAL)]
  Internet-facing: [yes / no]

Vulnerabilities:
  EOL version: [yes (MEDIUM) / no]
  Known CVEs: [N] relevant

Redaction notes:
  - No key data values were read or stored.
  - Password values from CONFIG GET are redacted.
  - Key names containing sensitive patterns are redacted.
  - No CONFIG SET, module load, replication, or script execution was attempted.
  - No keys were created, modified, or deleted.
```

## Report handoff

1. `pentest_agent_record_finding` for each finding with: host, finding type, severity, remediation (specific `redis.conf` change, `rename-command` addition, `ACL` rule, firewall change), and verification test.
2. Priority matrix: CRITICAL (no password + internet-facing, CONFIG SET not disabled, SLAVEOF not disabled, MODULE LOAD not disabled, ACL default user with `nopass` and `+@all`, protected-mode disabled). HIGH (INFO accessible without auth, CONFIG GET accessible, keyspace exposed, key enumeration possible, no TLS). MEDIUM (EOL version, EVAL not disabled, FLUSH commands not disabled, CLIENT LIST accessible). LOW (version disclosure, keyspace stats, uptime info).
3. Provide a Redis hardening checklist: set a strong `requirepass`, rename or disable dangerous commands (`CONFIG`, `SLAVEOF`, `MODULE`, `EVAL`, `FLUSHDB`, `FLUSHALL`, `DEBUG`, `SHUTDOWN`), enable `protected-mode`, bind to specific IP, use Redis 7+ with ACLs (create limited users, disable default user), enable TLS (`tls-port`), use firewall rules, and never expose Redis directly to the internet.
4. Explicitly note: no data values were read, no configuration was modified, no commands were renamed or disabled, no modules were loaded, no replication was established, no Lua scripts were executed, and no keys were created, modified, or deleted. Redis is designed as a trusted internal component; exposure without hardening is a known and critical security risk.
