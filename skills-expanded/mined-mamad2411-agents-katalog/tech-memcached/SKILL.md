---
name: tech-memcached
description: Memcached security review — identifies unauthenticated access, UDP amplification abuse potential, stats information disclosure, slab and key enumeration, SASL authentication gaps, and network exposure misconfigurations. All probes are read-only binary/text protocol commands. No data mutation, no key deletion, no amplification testing, no DoS.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, blue-team, offensive, grey-hat]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft, memcached-security-audit]
---

# Memcached security review

Use this skill to assess the security posture of Memcached servers. The review covers network exposure, authentication configuration, information disclosure via statistics commands, cache data enumeration risk, UDP amplification potential, and SASL authentication posture. All probes are read-only Memcached ASCII protocol commands. This skill never stores, modifies, or deletes cached data; never performs UDP amplification or reflection tests; never dumps cache contents beyond key name and size metadata; and never tests DoS conditions.

## Required inputs

- Target Memcached server host:port (default: `TARGET_IP:11211` for TCP, `TARGET_IP:11211` for UDP).
- Scope file confirming which hosts and ports are in scope.
- Authorization cache valid for the target host.
- Optional: Memcached configuration file (`memcached.conf` or command-line flags) for offline review.

## Required gates

1. `pentest_agent_load_config` and `pentest_agent_validate_policy` before any active probing.
2. `pentest_agent_parse_scope` and `pentest_agent_validate_target` for the Memcached host before connection.
3. `pentest_agent_check_authorization` before any network connection.
4. `pentest_agent_build_command` for dry-run argv preview.
5. `pentest_agent_execute_tool` for all live probing — rate-limit enforcement, approval.
6. `pentest_agent_append_evidence` with redacted output.

## Workflow

### Phase 1 — Server discovery and connectivity

1. **TCP connectivity test** (read-only, low-noise):
   - `echo -e "stats\r\nquit\r\n" | nc -w 3 TARGET_IP 11211`.
   - If response starts with `STAT pid`, `STAT uptime`, `STAT version` → Memcached accessible over TCP. HIGH (unauthenticated).
   - If `nc` returns "Connection refused" → port not open or firewalled. OK.
2. **Version and build info**:
   - `echo -e "stats\r\nquit\r\n" | nc -w 3 TARGET_IP 11211 | grep -E "^STAT (version|pointer_size|libevent|rusage_user)"`.
   - Memcached versions < 1.5.6: built without SASL support by default. No authentication possible.
   - Memcached versions ≥ 1.5.6: SASL authentication via binary protocol available.
3. **Process information**:
   - `STAT pid`, `STAT uptime` → how long the server has been running, its process ID. LOW informational.
   - `STAT time` → server's current UNIX time. Can be compared to actual time to detect clock skew.

### Phase 2 — Authentication and access control

1. **SASL authentication status**:
   - `echo -e "stats\r\nquit\r\n" | nc -w 3 TARGET_IP 11211 | grep -c "STAT"`. If `stats` returns data without any authentication → CRITICAL. No authentication configured.
   - Memcached SASL uses the binary protocol. The ASCII `stats` command bypasses SASL entirely in most configurations. SASL only protects the binary protocol.
   - **Finding**: stats accessible without auth → CRITICAL. SASL authentication does not protect the stats command in default configurations.
2. **Access control check**:
   - Memcached has no built-in IP-based access control except via the `-l` (listen) flag. Check `STAT auth_enabled_sasl`. If `no` → no auth. CRITICAL.
   - If Memcached is listening on `0.0.0.0` or a public interface → any network-adjacent host can access it. HIGH.

### Phase 3 — Statistics and information disclosure

The `stats` command family reveals extensive operational information without authentication.

1. **General statistics** (`stats`):
   - `echo -e "stats\r\nquit\r\n" | nc -w 3 TARGET_IP 11211 | sort | head -50`.
   - Key fields: `STAT curr_items` (number of stored items), `STAT total_items` (items stored since server start), `STAT bytes` (memory used), `STAT limit_maxbytes` (cache size), `STAT curr_connections` (active clients), `STAT total_connections` (connections since start), `STAT get_hits` / `STAT get_misses` (cache hit ratio), `STAT cmd_get` / `STAT cmd_set` (total operations), `STAT evictions` (items evicted to free space), `STAT bytes_read` / `STAT bytes_written` (total data transferred).
   - **Finding**: `STAT evictions` is high → cache undersized. Data may be pushed out before it's used. LOW informational.
   - **Finding**: `STAT total_connections` reveals traffic volume. An attacker can gauge service utilization.
2. **Slab statistics** (`stats slabs`):
   - `echo -e "stats slabs\r\nquit\r\n" | nc -w 3 TARGET_IP 11211`.
   - Reveals memory allocation slabs, chunk sizes, memory usage per slab class, and LRU statistics.
   - This gives insight into the types of data stored (small chunks = IDs/tokens, medium chunks = serialized objects, large chunks = files/images).
3. **Item statistics** (`stats items`):
   - `echo -e "stats items\r\nquit\r\n" | nc -w 3 TARGET_IP 11211`.
   - Reveals per-slab-class item counts, ages, eviction rates, and out-of-memory counts.
   - An attacker can identify which slab classes contain the most data (e.g., class 1 with 50K items → likely session tokens).
4. **Connection statistics** (`stats conns`):
   - `echo -e "stats conns\r\nquit\r\n" | nc -w 3 TARGET_IP 11211`.
   - Lists all active connections with state. May reveal client IPs. HIGH if client IPs are exposed.
5. **Settings dump** (`stats settings`):
   - `echo -e "stats settings\r\nquit\r\n" | nc -w 3 TARGET_IP 11211`.
   - Reveals all runtime configuration: `maxbytes`, `maxconns`, `tcpport`, `udpport`, `verbosity`, `num_threads`, `binding_protocol`, `auth_enabled_sasl`, `maxconns_fast`, `slab_automove`.
   - **Finding**: `udpport` not `0` → UDP is enabled. See Phase 5 for UDP risk.
   - **Finding**: `binding_protocol` is `auto` → both ASCII and binary protocols accepted. MEDIUM — wider attack surface than binary-only.

### Phase 4 — Key enumeration and data exposure assessment

Cache keys and their metadata may reveal the nature of stored data.

1. **Cache dump via `lru_crawler`** (if enabled, read-only metadata):
   - `echo -e "lru_crawler metadump all\r\nquit\r\n" | nc -w 5 TARGET_IP 11211 | head -30`.
   - Each line: `key=KEY exp=-1 la=12345 clsid=1 fetch=yes cls=1 size=80`.
   - Returns: key name, expiration time, last access time, slab class, fetch status, and data size. No data values.
   - **Finding**: key names exposed → MEDIUM to HIGH depending on key naming. Examples: `session:abc123` (session tokens), `user:42:profile` (user data), `rate_limit:192.168.1.1` (rate limit keys), `cart:session_id` (shopping carts), `cache:query:SELECT+FROM+users` (SQL queries), `jwt:eyJ...` (JWT tokens as keys).
   - **CRITICAL**: if `KEY` values contain JWTs, session tokens, or API keys directly.
   - **PROHIBITED**: do not dump all keys or store key lists containing sensitive identifiers. Sample 20-30 keys, redact sensitive segments.
2. **Key access test** (never retrieve data values, check existence only):
   - `echo -e "get KEY_NAME\r\nquit\r\n" | nc -w 3 TARGET_IP 11211`. If it returns `VALUE KEY_NAME ...` followed by data → key exists and is readable. CRITICAL if data is returned without auth.
   - **PROHIBITED**: do not issue `get` commands on real keys unless needed to confirm accessibility. If used, set a short timeout and do not read or store the returned data value.
   - This test proves that data values are accessible, not just metadata.
3. **Cachedump** (slab-class dump):
   - `echo -e "stats cachedump SLAB_ID 0\r\nquit\r\n" | nc -w 3 TARGET_IP 11211`.
   - Lists all keys in a given slab class. The `0` argument requests all keys (in practice limited to 2MB of response data).
   - **Finding**: full key listing without auth → HIGH.

### Phase 5 — UDP amplification risk assessment

Memcached over UDP is the source of one of the largest DDoS amplification attack vectors.

1. **UDP port check**:
   - `echo -e "stats\r\nquit\r\n" | nc -u -w 2 TARGET_IP 11211`.
   - If `stats` returns via UDP → UDP is enabled. CRITICAL for amplification risk.
   - Memcached over UDP disabled by default since version 1.5.6 (`-U 0`). Earlier versions listen on UDP by default.
2. **Amplification factor estimation** (never perform amplification test):
   - Do not send amplification test payloads.
   - Document the risk: if a 15-byte UDP `stats` request results in a multi-kilobyte response, the amplification factor can exceed 10,000x. Memcached is the #1 UDP amplification vector.
   - **Finding**: UDP enabled on internet-facing Memcached → CRITICAL. The server can be abused in DDoS amplification attacks.
3. **UDP source IP validation**:
   - Memcached does not validate the source IP of UDP packets. An attacker can spoof the source IP to redirect amplification traffic to a victim. CRITICAL.

### Phase 6 — Network exposure and binding

1. **Listening interfaces**:
   - Check `STAT version` and cross-reference with config: `-l 0.0.0.0` → listening on all interfaces. HIGH if not firewalled.
   - Check: is Memcached on a public IP? CRITICAL if combined with no authentication.
2. **Firewall validation**:
   - Document whether the port is accessible from the test origin. If it is and the test origin is external, firewall rules are insufficient. HIGH.
3. **TLS support**:
   - Memcached has no native TLS support. All data is transmitted in plaintext. An on-path network observer can see all keys and values. MEDIUM.
   - Proxy-based TLS termination (stunnel, HAProxy) recommended for sensitive deployments.

## Decision points

- **Stats returns data but key listing is blocked or slow**: Memcached's `lru_crawler metadump` may be disabled. Document that stats access is still HIGH (operational data, connection IPs, slab sizes).
- **UDP is enabled on an internal-only server**: the amplification risk is lower (not internet-accessible) but still present for internal DDoS. Flag as MEDIUM for internal, CRITICAL for external.
- **Server responds but key names are non-sensitive** (e.g., static asset cache like `html:/index`, `css:/style.css`): access is still HIGH (anyone can read/write cache) but data sensitivity is lower. Document context.

## Prohibited behavior

- Reading data values via `get` beyond a single proof-of-access check.
- Modifying, deleting, or flushing cache data (`set`, `add`, `replace`, `delete`, `flush_all`).
- Sending UDP amplification test payloads.
- Attempting to crash or overload the server.
- Dumping more than 30 keys in evidence.
- Storing cache data values in evidence.
- Using `stats cachedump` with large slab IDs repeatedly.

## Stop conditions

- `get KEY` returns data that looks like a session token, JWT, API key, or PII → stop reading data immediately. Document that data is accessible.
- Key names reveal application-specific secrets or identifiers → stop key enumeration. Document the pattern.
- `stats conns` reveals client IP addresses → document. Redact IPs in evidence.
- Memcached responds on UDP → document as CRITICAL.

## Evidence

For each finding, record: host:port, finding type, protocol, access level, severity, and remediation. Evidence template:

```text
Memcached security review for: [TARGET_IP:PORT]
Version: [VERSION]
Uptime: [SECONDS] seconds
Review date: [DATE]

Access:
  TCP accessible: [yes — no auth (CRITICAL) / yes — SASL / no]
  UDP enabled: [yes (CRITICAL) / no (OK)]
  Listening interface: [0.0.0.0 / specific IP / 127.0.0.1]
  SASL enabled: [yes / no]
  Stats accessible: [yes / no]

Cache information:
  Current items: [N]
  Memory used: [BYTES] / [LIMIT] bytes
  Slab classes: [N]
  Key enumeration possible: [yes — metadump (HIGH) / yes — cachedump (HIGH) / no]

Data exposure:
  Keys sampled: [N]
  Sensitive key patterns: [N] — [patterns redacted]
  Data values readable: [yes (CRITICAL) / not tested / blocked]

UDP amplification risk:
  UDP stats response size: [N] bytes (amplification factor ~[X]x)
  Internet-facing: [yes / no]

Redaction notes:
  - No cache data values were stored.
  - Key names containing sensitive identifiers are redacted.
  - No UDP amplification test was performed.
  - Client IPs from connection stats are redacted.
  - No cache entries were created, modified, or deleted.
```

## Report handoff

1. `pentest_agent_record_finding` for each finding with: host, finding type, severity, remediation (specific `memcached` command-line flag change, firewall rule, SASL configuration), and verification test.
2. Priority matrix: CRITICAL (no auth + internet-facing, UDP enabled on internet-facing server, data values readable, session/JWT tokens in keys). HIGH (no auth internal, stats accessible, key names exposed, UDP enabled internal). MEDIUM (plaintext protocol, stats info disclosure, listening on 0.0.0.0 behind firewall). LOW (version info, uptime disclosure).
3. Provide a Memcached hardening checklist: bind to localhost or internal IP only (`-l 127.0.0.1`), disable UDP (`-U 0`), enable SASL authentication, use stunnel/TLS proxy, place behind a firewall that restricts source IPs, upgrade to latest version, disable ASCII protocol if only binary is needed.
4. Explicitly note: no data values were stored, no keys were deleted or modified, no amplification tests were performed, and no cache operations beyond read-only stats and metadata were executed.
