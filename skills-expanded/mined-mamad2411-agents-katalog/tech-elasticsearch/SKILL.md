---
name: tech-elasticsearch
description: Elasticsearch and OpenSearch cluster security review — identifies unauthenticated cluster access, index enumeration risk, anonymous data exposure, Kibana/OpenSearch Dashboards unauthenticated console access, snapshot repository misconfiguration, insecure authentication realms, TLS configuration gaps, version-specific known vulnerabilities, and excessive cluster privileges. All probes are read-only and low-rate. No data exfiltration, no index mutation, no snapshot creation, no credential testing beyond confirming anonymous access.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, blue-team, offensive, grey-hat, forensic]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft, cluster-security-audit, index-exposure-report]
---

# Elasticsearch and OpenSearch cluster security review

Use this skill to assess the security posture of Elasticsearch and OpenSearch clusters. The review covers cluster endpoint exposure, authentication configuration, anonymous access vectors, index enumeration and data sensitivity classification, Kibana/OpenSearch Dashboards security, snapshot repository access control, TLS configuration, and version-specific vulnerability assessment. All probes are read-only HTTP requests at a low rate targeting well-known REST API endpoints. This skill never exfiltrates index data, creates or restores snapshots, tests credential guessing, modifies cluster configuration, or exploits known RCE vulnerabilities. Active probing is gated behind `pentest_agent_execute_tool` with scope and authorization validation.

## Required inputs

- Target Elasticsearch or OpenSearch cluster base URL(s) (e.g., `https://TARGET:9200`, `http://TARGET:9200`).
- Associated Kibana or OpenSearch Dashboards URL(s) if in scope (e.g., `https://TARGET:5601`).
- Scope file confirming which hosts, ports, and API endpoints are in scope.
- Rate limits: max requests per second, max concurrent connections per host.
- Authorization cache valid for every target host.
- Optional: user-provided cluster configuration files (`elasticsearch.yml`, `opensearch.yml`, `kibana.yml`, `roles.yml`) for offline review. If provided, prefer offline review over live probing.
- Optional: user-provided index name list (from cluster admin) for targeted checks instead of broad index enumeration.

## Required gates

1. `pentest_agent_load_config` and `pentest_agent_validate_policy` before any active probing.
2. `pentest_agent_parse_scope` and `pentest_agent_validate_target` for every host before requests.
3. `pentest_agent_check_authorization` before any HTTP request.
4. `pentest_agent_build_command` for dry-run argv preview.
5. `pentest_agent_execute_tool` for all live probing — rate-limit enforcement, approval for any risky requests.
6. `pentest_agent_append_evidence` with redacted output.

## Workflow

### Phase 1 — Cluster discovery and version fingerprinting

Determine cluster type, version, and authentication posture.

1. **Cluster root endpoint** (passive, low-noise):
   - `curl -s -k https://TARGET:9200/ | jq '. | {name, cluster_name, tagline, version: .version.number, lucene_version: .version.lucene_version}'`.
   - Elasticsearch returns: `"tagline": "You Know, for Search"`, `version.number` like `7.17.10` or `8.11.0`.
   - OpenSearch returns: `"version.distribution": "opensearch"`, `version.number` like `2.11.0`.
   - If no authentication is required, the response body will appear. If authentication is required, HTTP 401 with `WWW-Authenticate: Basic realm="security"` or `"error": {"type": "security_exception", "reason": "missing authentication credentials..."}`.
   - **Finding**: unauthenticated cluster access → CRITICAL. Anyone on the network can read and write all indices.
2. **Cluster health** (unauthenticated access indicates weak security):
   - `curl -s -k https://TARGET:9200/_cluster/health | jq '{cluster_name, status, number_of_nodes, number_of_data_nodes, active_primary_shards, active_shards, unassigned_shards}'`.
   - `status` values: `green` (all shards assigned), `yellow` (all primary shards assigned but some replicas unassigned), `red` (some primary shards unassigned — data loss risk).
   - This endpoint is frequently unauthenticated even when the root endpoint requires credentials.
3. **Node information**:
   - `curl -s -k https://TARGET:9200/_nodes/_all | jq '.nodes | to_entries | map({name: .value.name, version: .value.version, host: .value.host, ip: .value.ip, roles: .value.roles})'`.
   - Lists every node in the cluster: name, version, host OS, IP address, and node roles (master, data, ingest, ml, remote_cluster_client).
   - **Finding**: nodes endpoint accessible without auth → HIGH. Full cluster topology exposed.
4. **Security features check**:
   - `curl -s -k https://TARGET:9200/_xpack | jq '{security: .features.security.enabled, ssl: .features.ssl.enabled}'` (Elasticsearch 7.x-8.x).
   - If `security.enabled: false` → CRITICAL. X-Pack Security is the primary Elasticsearch authentication layer. Without it, the cluster is open.
   - OpenSearch equivalent: check `/` response for `distribution: opensearch`. Security plugin is bundled and enabled by default since 2.x.
5. **License check** (Elasticsearch only):
   - `curl -s -k https://TARGET:9200/_license | jq '{license_type: .license.type, status: .license.status, expiry: .license.expiry_date_in_millis}'`.
   - License types: `basic` (free, limited security features), `trial` (full features for 30 days), `platinum` / `enterprise` (full security: SAML, OIDC, LDAP, field-level security, audit logging).
   - Basic license → authentication is possible but advanced security features (LDAP/SAML/OIDC realms, field-level security, audit logging) are not available. MEDIUM if basic license and unauthenticated.

### Phase 2 — Index enumeration and data sensitivity assessment

If the cluster allows unauthenticated read access, enumerate indices and assess exposed data sensitivity.

1. **List all indices** (read-only, low-noise):
   - `curl -s -k https://TARGET:9200/_cat/indices?v&h=index,health,status,docs.count,store.size,pri.store.size`.
   - Lists every index, document count, and storage size. This is a HIGH finding if accessible without auth — an attacker knows exactly what data is available.
   - Alternative (OpenSearch-compatible newer API): `curl -s -k https://TARGET:9200/_cat/indices?format=json | jq '.[] | {index: .index, docs: .["docs.count"], size: .["store.size"]}'`.
2. **Index naming patterns and sensitivity classification** (inspect names only, do not read data):
   - Look for indices named: `users`, `accounts`, `customers`, `orders`, `payments`, `credit_cards`, `invoices`, `passwords`, `secrets`, `credentials`, `emails`, `employees`, `patients`, `health_records`, `logs-*`, `audit-*`, `security-*`, `transactions`, `sessions`, `tokens`.
   - Classify each index by sensitivity: PII (personally identifiable information), FINANCIAL (payment data, transactions), CREDENTIALS (passwords, API keys, tokens), HEALTH (PHI — protected health information), AUDIT (security logs — useful for attacker reconnaissance), APPLICATION (application data, configs), SYSTEM (cluster-internal indices like `.kibana*`, `.security*`, `.monitoring*`).
3. **Sample query for index mapping** (schema only, no data):
   - `curl -s -k https://TARGET:9200/users/_mapping | jq '.users.mappings.properties | keys'` — reveals field names in the `users` index.
   - Check for field names: `password`, `password_hash`, `ssn`, `credit_card`, `email`, `phone`, `address`, `dob`, `api_key`, `token`, `secret`, `access_key`.
   - **STOP**: if mapping reveals sensitive field names → do not query actual data. Document the index sensitivity based on field names alone.
4. **Low-count index safety probe** (only if scope explicitly allows read probes on non-sensitive indices):
   - `curl -s -k https://TARGET:9200/some-app-index/_search?size=1 | jq '.hits.hits[0]._source | keys'`
   - Limits: size=1, read a single document's field keys only. Do not read field values.
   - **PROHIBITED**: do not use `_search` on indices classified as CREDENTIALS, FINANCIAL, or HEALTH.
5. **Alias enumeration**:
   - `curl -s -k https://TARGET:9200/_cat/aliases?v | column -t`.
   - Aliases can hide the real index name. An alias like `prod_users` pointing to `users_v3` is informative.

### Phase 3 — Kibana / OpenSearch Dashboards security

Assess the web dashboard frontend.

1. **Dashboard version and status**:
   - `curl -s -k https://TARGET:5601/api/status | jq '{name: .name, version: .version.number, state: .status.overall.state, metrics_status: .status.statuses."plugin:kibana@...".state}'`.
   - If accessible without login → HIGH finding. The dashboard grants full cluster access.
2. **Console proxy access** (Kibana console allows direct Elasticsearch API calls):
   - Kibana Console (Dev Tools) is a browser-based API client. If the dashboard is unauthenticated, the console can issue arbitrary Elasticsearch queries.
   - Test endpoint: `curl -s -k -X POST https://TARGET:5601/api/console/proxy?path=_cat/indices&method=GET -H "kbn-xsrf: true"`.
   - If response contains index listing → CRITICAL. The console proxy bypasses any API-level authentication because the dashboard acts as a trusted proxy.
   - OpenSearch Dashboards equivalent: `curl -s -k -X POST https://TARGET:5601/api/console/proxy?path=_cat/indices&method=GET -H "osd-xsrf: true"`.
3. **Saved objects and configuration exposure**:
   - `curl -s -k https://TARGET:5601/api/saved_objects/_find?type=index-pattern` — reveals all configured index patterns (data sources).
   - `curl -s -k https://TARGET:5601/api/saved_objects/_find?type=config` — reveals dashboard configuration including default index.
4. **Timelion / Vega / Canvas plugin access**:
   - Some Kibana plugins allow arbitrary expression execution that can access cluster data.
   - Document that these plugins are available if the dashboard is accessible; do not attempt to exploit them.

### Phase 4 — Snapshot repository security

Snapshots can be abused for data exfiltration if the repository is misconfigured.

1. **List snapshot repositories**:
   - `curl -s -k https://TARGET:9200/_snapshot | jq 'keys'`.
   - Repository types: `fs` (filesystem — local path), `s3` (AWS S3), `gcs` (Google Cloud Storage), `azure` (Azure Blob), `hdfs`.
   - **Finding**: snapshot repositories listed without auth → MEDIUM. An attacker with write access could create a snapshot to an attacker-controlled path and exfiltrate data.
2. **Repository configuration inspection**:
   - `curl -s -k https://TARGET:9200/_snapshot/REPO_NAME | jq '.[].settings'`.
   - For `fs` type, check the `location` path. A world-writable location or user-controlled path could allow snapshot injection.
   - **PROHIBITED**: do not create snapshots, restore snapshots, or modify repository configuration.
3. **List existing snapshots**:
   - `curl -s -k https://TARGET:9200/_snapshot/REPO_NAME/_all | jq '.snapshots[] | {snapshot, state, start_time, indices, duration}'`.
   - Reveals which indices have been snapshotted, when, and their state.

### Phase 5 — TLS and transport security

Assess cluster communication security.

1. **TLS on HTTP API** (port 9200):
   - If `https://` is used: check with `testssl https://TARGET:9200` or `sslscan TARGET:9200`.
   - TLS 1.0/1.1 support → HIGH. TLS 1.2 minimum recommended. TLS 1.3 preferred.
   - Self-signed certificate → LOW for internal, MEDIUM for internet-facing.
2. **Inter-node transport encryption** (port 9300):
   - `curl -s -k https://TARGET:9200/_nodes/_all | jq '.nodes[].settings.transport | {type, "xpack.security.transport.ssl.enabled"}'`.
   - If `xpack.security.transport.ssl.enabled: false` → MEDIUM. Inter-node communication (gossip, shard relocation, replication) is in plaintext. Anyone who can sniff the network can capture cluster data.
3. **HTTP compression / GZIP**:
   - Check if `http.compression: true` is set in configuration. BREACH attack possible if compression + user-controllable data in response + CSRF on same origin.

### Phase 6 — Version-specific vulnerability assessment

Cross-reference the detected version against known CVEs. Do not attempt exploitation.

1. **Elasticsearch version vulnerability mapping** (reference-only, do not exploit):
   - **CVE-2015-1427**: Groovy scripting RCE (Elasticsearch < 1.4.0). Groovy sandbox escape via `Runtime.getRuntime().exec()`. CRITICAL if version ≤ 1.3.x.
   - **CVE-2015-5377**: Elasticsearch Java deserialization RCE (Elasticsearch 1.5.0-1.5.2). CRITICAL if version in range.
   - **CVE-2021-22145**: Information disclosure via `_update_by_query` (Elasticsearch 7.10.0-7.13.3). MEDIUM.
   - **CVE-2021-44228** (Log4Shell): Elasticsearch 6.x/7.x and OpenSearch 1.x bundled vulnerable Log4j versions. CRITICAL if version ≤ 7.16.0 (Elasticsearch) or ≤ 1.2.4 (OpenSearch) without mitigation.
   - **CVE-2023-46673**: Elasticsearch 8.x prototype pollution. MEDIUM.
   - Document: detected version, relevant CVEs, CVSS score, remediation (upgrade to specific fixed version).
2. **Kibana version vulnerability mapping**:
   - **CVE-2019-7609**: Kibana Prototype Pollution RCE via Timelion (Kibana < 6.6.1). CRITICAL if version ≤ 6.6.0.
   - **CVE-2020-7019**: Kibana Privilege Escalation (Kibana 7.0.0-7.6.0). HIGH.
   - **CVE-2023-31415**: Kibana RCE via file upload (Kibana 8.7.0). HIGH.
3. **End-of-life version check**:
   - Elasticsearch 6.x: EOL February 2022.
   - Elasticsearch 7.x: EOL on release of 9.0 (TBD, anticipated 2025).
   - Elasticsearch 8.x: current.
   - OpenSearch 1.x: maintained with backports.
   - OpenSearch 2.x: current.
   - EOL version → MEDIUM (no security patches). Recommend upgrade to supported version.

## Decision points

- **Cluster is unauthenticated but contains only publicly available data** (e.g., open data indices): flag as MEDIUM (configuration control gap) rather than CRITICAL. An attacker could still enumerate infrastructure, modify data, or abuse the cluster for cryptomining.
- **Kibana dashboard is exposed without authentication but Elasticsearch API requires auth**: the Kibana console proxy may still bypass API auth. Test with a `_cat/indices` request through the proxy. If it succeeds, CRITICAL.
- **Version is vulnerable to Log4Shell (CVE-2021-44228)**: flag as CRITICAL. Do not send a Log4j test payload. Document the version, the CVE, and the recommended fix (upgrade or set `-Dlog4j2.formatMsgNoLookups=true`).
- **Index mapping reveals sensitive field names but index is behind authentication**: document as informational — field names are metadata and may be accessible via field capabilities API even when data is protected.
- **`_nodes` endpoint reveals hostnames, IPs, and OS versions**: this is normal cluster behavior but should be gated behind authentication. Document as LOW (information disclosure) if unauthenticated.

## Prohibited behavior

- Querying actual document data from indices classified as CREDENTIALS, FINANCIAL, or HEALTH.
- Dumping or storing index data beyond what is needed for a minimal proof (size=1 schema inspection).
- Creating, restoring, or deleting snapshots.
- Sending Log4j, Groovy injection, or other exploit payloads.
- Testing credentials or brute-forcing authentication.
- Modifying index mappings, settings, or aliases.
- Accessing Kibana plugins (Timelion, Vega, Canvas) beyond confirming their availability.
- Probing the transport layer (port 9300) with custom Java serialization payloads.
- Using `_search` with `scroll` or large `size` parameters to enumerate bulk data.
- Storing any credentials, tokens, API keys, or PII extracted from cluster responses in evidence files.

## Stop conditions

- Cluster root endpoint returns HTTP 200 with cluster metadata and version without any authentication → CRITICAL finding. Stop enumeration of data contents; focus on documenting the access vector and cluster topology.
- Kibana Console proxy returns index listing → CRITICAL. Do not enumerate further through the proxy; document the vector.
- Response contains real user data (PII, credentials, payment information) → stop reading immediately. Document the index and field names where data was encountered. Do not store the data.
- HTTP 429 (rate limiting) is returned → reduce rate by 50% or pause probing. Do not attempt to bypass rate limits.
- HTTP 403 or 401 is consistently returned for all endpoints → the cluster has authentication configured. Document as a positive control and move to offline configuration review if config files were provided.

## Evidence

For each finding, record: target host, finding type, specific API endpoint, HTTP response metadata (status code, content-type, response size), sensitivity classification, severity, and remediation. Evidence template:

```text
Elasticsearch/OpenSearch cluster security review for: [TARGET_HOST:PORT]
Cluster: [Elasticsearch/OpenSearch] [VERSION]
Dashboard: [Kibana/OpenSearch Dashboards] [URL / not in scope]
Review date: [DATE]

Cluster authentication:
  Unauth root access: [yes (CRITICAL) / no (OK)]
  Unauth _cluster/health: [yes (HIGH) / no]
  Unauth _nodes: [yes (HIGH) / no]
  Security features: [xpack.security.enabled: false (CRITICAL) / enabled (OK)]
  License type: [basic / trial / platinum / enterprise]
  TLS enabled: [yes (TLS 1.X) / no (CRITICAL)]
  Inter-node encryption: [enabled (OK) / disabled (MEDIUM)]

Index exposure (unauthenticated):
  Total indices visible: [N]
  PII indices: [N] — [index names redacted]
  Financial indices: [N] — [index names redacted]
  Credential indices: [N] — [index names redacted]
  Application indices: [N]
  System indices: [N]

Dashboard security:
  Unauthenticated dashboard access: [yes (CRITICAL) / no]
  Console proxy accessible: [yes (CRITICAL) / blocked / not tested]
  Saved objects accessible: [yes / no]

Snapshot repositories:
  Repositories visible: [N]
  Repository types: [fs / s3 / gcs / azure]
  Existing snapshots: [N]

Vulnerability assessment:
  CVEs relevant to detected version: [list with CVSS]
  End-of-life: [yes / no]
  Log4Shell (CVE-2021-44228) vulnerable: [yes (CRITICAL) / no / mitigated]

Redaction notes:
  - No index data was dumped or stored.
  - Index names containing PII or credential indicators are redacted.
  - Cluster name and node hostnames are redacted.
  - No exploit payloads were sent.
  - No snapshots were created, restored, or deleted.
  - No cluster configuration was modified.
```

## Report handoff

1. `pentest_agent_record_finding` for each finding with: host, finding type, severity, redacted evidence excerpt, specific remediation (e.g., "enable xpack.security.enabled in elasticsearch.yml", "enable TLS for HTTP API", "upgrade to Elasticsearch 8.11+"), and verification test.
2. Priority matrix: CRITICAL (unauthenticated cluster access, unauthenticated Kibana console proxy, Log4Shell-vulnerable version, known RCE CVE on detected version). HIGH (unauthenticated `_nodes`, unauthenticated `_cluster/health`, index listing without auth, exposed snapshot repository list). MEDIUM (inter-node encryption disabled, EOL version, basic license without security features, self-signed cert on internet-facing cluster). LOW (hostnames/IPs in node info, verbose error messages).
3. Provide an Elasticsearch hardening checklist: enable xpack.security, enable TLS for HTTP and transport, require authentication for `_cat`, `_nodes`, `_cluster/health` endpoints (set `xpack.security.authc.anonymous.*` to restrict), upgrade to supported version, restrict Kibana console access, and configure snapshot repository access controls.
4. Explicitly note: no index data was exfiltrated, no snapshots were created or restored, no cluster configuration was modified, no exploit payloads were delivered, and no authentication credentials were tested.
