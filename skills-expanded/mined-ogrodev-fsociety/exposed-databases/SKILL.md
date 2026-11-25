---
name: exposed-databases
description: |
  This skill should be used when the user mentions "Shodan", "Censys", "MongoDB exposed", "Elasticsearch open", "Redis no auth", "open database", "unauthenticated database", "exposed MongoDB", "exposed Elasticsearch", "exposed Redis", "exposed CouchDB", "exposed MySQL", "exposed PostgreSQL", "port 27017", "port 9200", "port 6379", "port 5984", "port 3306", "port 5432", "find open databases", "database hunting", "scan for databases", "internet-facing database", "no authentication database", "database fingerprinting", "Kibana exposed", "Mongo Express", "phpMyAdmin exposed", or discusses finding internet-facing databases with no authentication, scanning for specific database ports, fingerprinting exposed data services, or triaging Shodan/Censys results to identify high-value targets. Always use this skill when the task involves discovering or probing exposed databases, even if the user doesn't use these exact phrases — for instance, "check if their MongoDB is open" or "look for exposed services on that IP range" should trigger this skill.
---

# Exposed Database Hunting

Discover internet-facing databases with no authentication, triage them by value, probe safely to confirm access, and route confirmed targets into the acquisition pipeline.

## Workflow

The exposed database hunting process follows five phases. Complete each phase before moving to the next — skipping triage leads to wasted probes on low-value or out-of-scope targets.

```
SCOPE → DISCOVER → TRIAGE → PROBE → ROUTE
  │         │          │        │        │
  │         │          │        │        ├─ open → data-acquisition skill
  │         │          │        │        └─ protected → cross-plugin-pipeline (elliot handoff)
  │         │          │        └─ dumper.js probe + source-tracker.js add
  │         │          └─ prioritize by data value, size, auth certainty
  │         └─ hunt-engine.js (shodan, dork, github) + Censys
  └─ verify target is in-scope for the active engagement
```

---

## Phase 1: Scope Check

Before generating any queries, verify the target is authorized:

1. Check `engagement.json` or the active campaign's scope definition
2. Confirm the target domain, IP range, or organization is explicitly in-scope
3. If no engagement is active, ask the operator to confirm authorization before proceeding

Never probe hosts outside the authorized scope, regardless of what Shodan/Censys returns.

---

## Phase 2: Discovery

Generate queries across multiple sources to maximize coverage. The hunt engine produces structured queries — it does not execute them. You execute them via MCP tools (Hexstrike Shodan, Brave Search) or direct API calls.

### Shodan Queries

```
node ${CLAUDE_PLUGIN_ROOT}/scripts/hunt-engine.js shodan <target> [--service mongo|elastic|redis|couch|mysql|postgres|all]
```

The engine generates queries filtered by service type and scoped to the target (by hostname for domains, by CIDR for IP ranges). Covers MongoDB (27017), Elasticsearch (9200), Redis (6379), CouchDB (5984), MySQL (3306), PostgreSQL (5432), and Kibana (5601).

Execute each generated query via MCP Shodan tool. For each result, extract:
- **IP and port** — the probe target
- **ASN and organization** — verify it belongs to the target's infrastructure
- **Banner data** — version string, auth status indicators, database/index names if visible

### Censys Queries

Censys uses a SQL-like search syntax. Generate equivalent queries manually:

| Database | Censys Query |
|----------|-------------|
| MongoDB | `services.port=27017 AND services.service_name=MONGODB AND autonomous_system.name="Target Org"` |
| Elasticsearch | `services.port=9200 AND services.http.response.body:"You Know, for Search" AND labels="Target"` |
| Redis | `services.port=6379 AND services.banner:"redis_version" AND autonomous_system.name="Target Org"` |
| CouchDB | `services.port=5984 AND services.http.response.body:"couchdb" AND autonomous_system.name="Target Org"` |
| MySQL | `services.port=3306 AND services.service_name=MYSQL AND autonomous_system.name="Target Org"` |
| PostgreSQL | `services.port=5432 AND services.service_name=POSTGRESQL AND autonomous_system.name="Target Org"` |

Replace `"Target Org"` with the actual ASN organization name or use `ip:` for CIDR ranges.

### Google Dorks

```
node ${CLAUDE_PLUGIN_ROOT}/scripts/hunt-engine.js dork <target> --category exposed-db
```

Generates dorks for phpMyAdmin panels, exposed Elasticsearch `_cat/indices` endpoints, MongoDB HTTP interfaces, CouchDB Futon/Fauxton UIs, and Adminer. These catch web-facing admin UIs that Shodan might miss.

### GitHub Leak Search

```
node ${CLAUDE_PLUGIN_ROOT}/scripts/hunt-engine.js github <target> --type secrets
```

Finds connection strings (`mongodb+srv://`, `redis://`, JDBC URLs) leaked in public repos. A leaked connection string with credentials is a direct path to a database that may not appear on Shodan at all.

---

## Phase 3: Triage

Discovery will produce a list of candidate hosts. Probe them in priority order — not randomly. Each result has signals in the Shodan/Censys banner that help you decide what to probe first.

### Priority Matrix

| Priority | Signal | Why |
|----------|--------|-----|
| **P1 — Probe immediately** | Banner shows database names containing `users`, `customers`, `accounts`, `credentials`, `emails`, or PII-related terms. Auth is confirmed disabled (MongoDB `ok: 1`, Elasticsearch `200`, Redis version info without `NOAUTH`). | High-value data, confirmed open — maximum ROI. |
| **P2 — Probe soon** | Port is open and service is identified, but banner doesn't reveal auth status or data content. Large estimated size. | Needs verification but likely worth it. |
| **P3 — Probe if time allows** | Service detected but port is non-standard, or banner suggests auth is enabled (401, `NOAUTH`, `code: 13`). | Low probability of open access. |
| **Skip** | IP/ASN doesn't belong to target. Out-of-scope geography. Banner confirms auth enabled with certainty. | Not in scope or confirmed protected. |

### Auth Status from Banners

Read auth status directly from discovery results before probing — this saves time on hosts that are clearly protected:

- **MongoDB**: `"ok": 1.0` in banner = open. `"code": 13` or `"code": 18` = protected.
- **Elasticsearch**: Banner contains cluster info JSON with `200` status = open. `401` or `security_exception` = protected.
- **Redis**: `redis_version:X.Y.Z` in banner = open. `NOAUTH Authentication required` = protected.
- **CouchDB**: `"couchdb":"Welcome"` in banner = service running (need to check `/_all_dbs` to confirm auth).
- **MySQL/PostgreSQL**: Port open doesn't indicate auth status — these always need a connection attempt.

See `references/database-fingerprints.md` for complete banner patterns and authentication detection tables.

---

## Phase 4: Probe and Log

For each P1/P2 target, probe using `dumper.js` and log the result with `source-tracker.js`. These two steps always happen together — never probe without logging.

### Probe

```
node ${CLAUDE_PLUGIN_ROOT}/scripts/dumper.js probe <host:port> [--service auto|mongo|elastic|redis|couch|mysql|postgres]
```

The probe is read-only. It detects the service type, attempts a single metadata query (list databases/indices/keys), and reports whether the service is open or requires authentication. Auto-detection works for most services based on port number and banner response.

If `dumper.js probe` is unavailable or the target requires a non-standard approach, fall back to manual probing — but stick to read-only operations:

| Service | Manual Probe Command | What It Returns |
|---------|---------------------|-----------------|
| MongoDB | `mongosh --host <ip> --port 27017 --eval 'JSON.stringify(db.adminCommand("listDatabases"))' --quiet` | Database names and sizes |
| Elasticsearch | `curl -s http://<ip>:9200/_cat/indices?v` | Index names, doc counts, sizes |
| Redis | `redis-cli -h <ip> -p 6379 INFO server` then `DBSIZE` | Version, key count |
| CouchDB | `curl -s http://<ip>:5984/_all_dbs` | Database names |
| MySQL | `mysql -h <ip> -P 3306 --connect-timeout=5 -N -B -e 'SHOW DATABASES'` | Database names (blank password) |
| PostgreSQL | `psql -h <ip> -p 5432 -U postgres -t -A -c 'SELECT datname FROM pg_database WHERE datistemplate = false'` | Database names |

Never issue write, update, or delete commands. Read-only enumeration only.

### Log Immediately After Probing

Every probed host gets logged, whether open or closed. This prevents re-probing the same host and builds the intelligence picture.

**If open:**
```
node ${CLAUDE_PLUGIN_ROOT}/scripts/source-tracker.js add exposed-db <ip:port> "<db-type> vX.Y, databases: [list], ~N records" \
  --service <mongo|elastic|redis|couch|mysql|postgres> \
  --access-method open \
  --data-types email,password,name \
  --records <estimated-count>
```

Then classify:
```
node ${CLAUDE_PLUGIN_ROOT}/scripts/source-tracker.js classify <id> \
  --credibility high \
  --freshness <YYYY-MM> \
  --access-method open
```

**If protected:**
```
node ${CLAUDE_PLUGIN_ROOT}/scripts/source-tracker.js add exposed-db <ip:port> "<db-type> vX.Y — auth required" \
  --service <mongo|elastic|redis|couch|mysql|postgres> \
  --access-method exploit
```

---

## Phase 5: Route

After probing and logging, route each confirmed source to the appropriate next step:

| Access Status | Route | Action |
|--------------|-------|--------|
| **Open** (no auth) | **data-acquisition skill** | Run `dumper.js dump` to acquire data. The data-acquisition skill covers dump execution, safety limits, format conversion, and acquisition tracking. |
| **Protected** (auth required, but credentials found in leaks/GitHub) | **data-acquisition skill** | Attempt connection with discovered credentials first. |
| **Protected** (no credentials available) | **cross-plugin-pipeline skill** | Generate an elliot handoff package with the target intel for active exploitation. |
| **Stale/Down** | **Mark as stale** | `source-tracker.js update <id> status stale` — move on. |

---

## OPSEC Considerations

The active hunt profile affects how you execute this workflow:

| Profile | Discovery | Probing | Timing |
|---------|-----------|---------|--------|
| `surface` | Shodan/Censys API, Google dorks, GitHub | Direct probes, no delays | Immediate |
| `deep` | + forum searches, paid APIs | Direct probes with 1-5s delays between hosts | Paced |
| `dark` | + .onion sources, hidden services | Probes through Tor/proxychains, 3-10s delays | Slow |
| `ghost` | Same as dark, max anonymity | Single probe at a time, 10-60s random delays | Very slow |

Check the active profile before starting:
```
node ${CLAUDE_PLUGIN_ROOT}/scripts/hunt-profile.js show
```

On `deep`/`dark`/`ghost` profiles, space out probes to avoid triggering IDS alerts or rate limits. On `surface` (lab/CTF environments), probe freely.

---

## Handling Failures

| Problem | Response |
|---------|----------|
| **Shodan API rate limit** | Switch to Censys queries or Google dorks. Wait and retry Shodan later. |
| **Probe timeout** | Host may be firewalled or down. Log as `stale`, move to next target. |
| **Service detected but auth status unclear** | Try `dumper.js probe` with explicit `--service` flag. If still unclear, attempt manual metadata query. |
| **Port open but not the expected service** | Honeypot or misconfigured service. Log it but deprioritize. Check if other ports on the same host reveal the actual database. |
| **Censys/Shodan data is stale** | Results can be days or weeks old. Always probe to confirm current state before acquisition. |

---

## Additional Resources

- **`references/shodan-queries.md`** — Full Shodan query syntax for each database type, filters, combining filters, geographic scoping, SSL certificate hunting, and result interpretation
- **`references/database-fingerprints.md`** — Default ports, banner patterns, response signatures, authentication detection tables, version detection methods, and the quick-reference port-to-service mapping
