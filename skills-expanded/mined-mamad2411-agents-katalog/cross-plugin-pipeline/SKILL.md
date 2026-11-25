---
name: cross-plugin-pipeline
description: |
  This skill should be used when the user mentions "handoff to elliot", "pipeline to elliot", "cross-plugin", "elliot handoff", "transfer to elliot", "handoff package", "generate handoff", "build handoff", "elliot engagement", "pass to elliot", "bridge to elliot", "return flow", "elliot return", "post-exploitation return", "feed back to tyrell", "ingest from elliot", "credential handoff", "target enrichment", "intel handoff", "handoff-builder", "handoff-tracker", "finding correlation", "leak to pentest", "data to exploitation", "breach to engagement", or discusses sending tyrell-acquired data to elliot for active exploitation, building an engagement package from leak intelligence, correlating breach data with pentest targets, enriching elliot's target intel from acquired dumps, generating wordlists from breached credentials, mapping leak data to attack surface, routing protected databases to elliot for exploitation, or receiving post-exploitation data back from elliot to expand tyrell's source intelligence. Always use this skill when the task involves moving data between tyrell and elliot — even if the user says something like "we found credentials, now what?" or "this database needs exploitation" or "send this intel to the pentest team".
---

# Cross-Plugin Pipeline

Bridge between tyrell's passive data acquisition and elliot's active exploitation. tyrell discovers exposed databases, acquires breach data, and extracts intelligence. When targets require active exploitation or acquired credentials need validation against live services, the pipeline packages tyrell's intelligence into an elliot-compatible engagement and routes it for active testing. Post-exploitation, elliot's discoveries flow back to tyrell to expand the intelligence picture.

## Pipeline Flow

```
TYRELL                                              ELLIOT
─────                                              ──────
leak-sources.jsonl ─┐
acquisitions.jsonl  ├─ ENRICH ─ CORRELATE ─ BUILD ─── handoffs/<id>/
dumps/<id>/*.jsonl ─┘     │         │          │         ├─ HANDOFF.md
                          │         │          │         ├─ scope.md
                          │         │          │         ├─ target-intel.jsonl
                          │         │          │         └─ attachments/
                          │         │          │              ├─ wordlist.txt
                          │         │          │              └─ sample-records.jsonl
                          │         │          │
                          │         │          └─ handoff-builder.js create
                          │         └─ Match credentials to services
                          └─ Extract domains, IPs, keys from dumps
                                                        │
                    RETURN FLOW                          │
                    ───────────                          ▼
acquisition-tracker.js add ◄──── elliot post-exploitation data
  --source-plugin elliot          (internal creds, pivots, new targets)
```

---

## Phase 1: Intelligence Enrichment

Before building a handoff, extract maximum value from acquired data. Raw dumps contain far more than credentials — they reveal infrastructure, internal services, cloud keys, and organizational structure.

### What to Extract from Dumps

Scan each acquired dump for the following intelligence categories. Use the extraction commands below or analyze manually.

| Category | What to Look For | Example |
|----------|-----------------|---------|
| **Credentials** | email:password pairs, email:hash pairs, API keys, tokens | `admin@corp.com:P@ssw0rd1` |
| **Domains** | Subdomains, internal hostnames, staging environments | `staging.internal.corp.com` |
| **IP Ranges** | Internal IPs, server addresses, CIDR blocks in configs | `10.0.0.0/8`, `192.168.1.50` |
| **Cloud Keys** | AWS access keys, GCP service accounts, Azure tokens | `AKIA...`, `AIza...` |
| **Connection Strings** | Database URIs, LDAP binds, SMTP configs | `mongodb://user:pass@internal:27017/prod` |
| **Email Patterns** | Naming conventions, distribution lists, admin accounts | `first.last@corp.com` |
| **Service Endpoints** | API URLs, webhook receivers, admin panels | `https://api.corp.com/v2/admin` |

### Extraction Commands

Search normalized JSONL dumps for high-value patterns:

```bash
# AWS access keys
grep -hoP 'AKIA[A-Z0-9]{16}' dumps/<id>/*.jsonl | sort -u

# Connection strings
grep -hoP '(mongodb|mysql|postgres|redis)://[^\s"]+' dumps/<id>/*.jsonl | sort -u

# Internal IPs (RFC1918)
grep -hoP '(10\.\d+\.\d+\.\d+|172\.(1[6-9]|2\d|3[01])\.\d+\.\d+|192\.168\.\d+\.\d+)' dumps/<id>/*.jsonl | sort -u

# Subdomains from email addresses
grep -hoP '@[\w.-]+\.\w+' dumps/<id>/*.jsonl | sed 's/@//' | sort -u

# API keys and tokens (generic patterns)
grep -hoiP '(api[_-]?key|token|secret|authorization)["\s:=]+["\s]*[A-Za-z0-9_\-]{20,}' dumps/<id>/*.jsonl
```

---

## Phase 2: Finding Correlation

Match tyrell's intelligence against elliot's attack surface. This is where passive data turns into actionable attack vectors.

### Credential-to-Service Mapping

For each credential set discovered in dumps, identify which live services they target:

| Credential Type | Target Services | Attack Vector |
|----------------|----------------|---------------|
| `email:plaintext` | Webmail, VPN, SSO, SaaS apps | Credential stuffing / direct login |
| `email:md5` | Same services after cracking | Hashcat mode 0, then stuffing |
| `email:bcrypt` | Low priority — cracking is slow | Skip unless high-value target |
| `username:password` (no @) | SSH, RDP, database logins, admin panels | Direct authentication |
| AWS access key + secret | AWS console, CLI, SDK | `aws sts get-caller-identity` to validate |
| Database connection string | Internal databases | Direct connection if network path exists |

### Correlation Decision Tree

```
For each credential set in dumps:
│
├─ Are the target services reachable from our position?
│   ├─ YES → Include in handoff as P1 attack vector
│   └─ NO → Check if VPN/jump host credentials exist in dumps
│       ├─ YES → Include VPN creds as P0 (prerequisite) + service creds as P1
│       └─ NO → Include as P2 (requires network pivot after initial access)
│
├─ Is the password plaintext or a weak hash (MD5/SHA1)?
│   ├─ PLAINTEXT → Ready to use, mark confidence: high
│   ├─ MD5/SHA1 → Crack first (hashcat), then include if successful
│   └─ BCRYPT/SCRAM → Deprioritize unless <100 hashes
│
└─ How many unique passwords in the set?
    ├─ High reuse (>30% same password) → Credential stuffing viable
    └─ Low reuse → Targeted per-account attempts only
```

---

## Phase 3: Build Handoff Package

Generate the engagement package using `handoff-builder.js`. The builder reads from the source tracker, acquisition tracker, and hunt profile to assemble a structured directory that elliot can consume immediately.

### Generate

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/handoff-builder.js create <source-id> \
  [--tech-stack <mongo|elastic|redis|mysql|postgres|mixed>] \
  [--defenses <none|waf|ids|auth|unknown>]
```

The builder:
1. Reads the source entry from `leak-sources.jsonl` by ID
2. Extracts target host, port, service type, and access method
3. Generates `HANDOFF.md` (engagement brief), `scope.md` (target scope), and `target-intel.jsonl` (machine-readable intel)
4. Auto-registers the handoff in `handoffs.jsonl` via `handoff-tracker.js`
5. Updates the source status to `handed-off`

Output directory: `handoffs/<source-id>/`

### Manual Enrichment After Build

The auto-generated package is a starting point. Before passing to elliot, enrich it manually:

1. **Add credential wordlists** — Extract unique passwords from dumps and save as `attachments/wordlist.txt`
2. **Add sample records** — Include 10-50 representative dump records as `attachments/sample-records.jsonl` for context
3. **Update HANDOFF.md** — Add recommended attack vectors based on Phase 2 correlation
4. **Update scope.md** — Add discovered domains, IPs, and cloud assets from Phase 1 enrichment
5. **Append to target-intel.jsonl** — Add extracted infrastructure intel in elliot's format

### target-intel.jsonl Record Schema

Each line is a JSON object compatible with elliot's `target-intel.js add` command:

```json
{
  "target": "corp.com",
  "category": "credential|service|network|tech-stack|defense|endpoint|note",
  "key": "descriptive-key",
  "value": "the actual value",
  "source": "tyrell"
}
```

**Elliot's valid categories**: `tech-stack`, `defense`, `credential`, `network`, `note`, `service`, `endpoint`

To bulk-import the handoff intel into elliot:
```bash
# From the elliot engagement directory
while IFS= read -r line; do
  target=$(echo "$line" | python3 -c "import sys,json; print(json.load(sys.stdin)['target'])")
  cat=$(echo "$line" | python3 -c "import sys,json; print(json.load(sys.stdin)['category'])")
  key=$(echo "$line" | python3 -c "import sys,json; print(json.load(sys.stdin)['key'])")
  val=$(echo "$line" | python3 -c "import sys,json; print(json.load(sys.stdin)['value'])")
  node ${CLAUDE_PLUGIN_ROOT}/scripts/target-intel.js add "$target" "$cat" "$key" "$val" --source tyrell
done < handoffs/<source-id>/target-intel.jsonl
```

---

## Phase 4: Track and Monitor

### Register and Track Handoffs

The builder auto-registers, but you can also manage handoffs manually:

```bash
# List all handoffs
node ${CLAUDE_PLUGIN_ROOT}/scripts/handoff-tracker.js list

# Filter by status
node ${CLAUDE_PLUGIN_ROOT}/scripts/handoff-tracker.js list --status pending

# Update status after elliot picks up the package
node ${CLAUDE_PLUGIN_ROOT}/scripts/handoff-tracker.js update <id> status active

# Mark completed after elliot engagement finishes
node ${CLAUDE_PLUGIN_ROOT}/scripts/handoff-tracker.js update <id> status completed

# Summary
node ${CLAUDE_PLUGIN_ROOT}/scripts/handoff-tracker.js summary
```

### Handoff Status Lifecycle

```
pending → active → completed
                 → failed (if elliot cannot exploit)
```

| Status | Meaning |
|--------|---------|
| `pending` | Package generated, waiting for elliot operator |
| `active` | Elliot engagement in progress |
| `completed` | Elliot finished, return data (if any) ingested |
| `failed` | Target not exploitable or out of scope |

---

## Phase 5: Return Flow (elliot to tyrell)

After elliot completes an engagement, new intelligence discovered during active testing flows back to tyrell. This expands the target picture and may reveal new databases or credentials not accessible from the outside.

### What elliot Returns

| Data Type | Example | Tyrell Action |
|-----------|---------|--------------|
| Internal credentials | LSASS dumps, config file passwords | Add to source tracker as `login` access method |
| Internal databases | MongoDB on 10.0.0.x discovered via pivot | Add as new source, probe if reachable |
| Network maps | Internal subnet layout, service inventory | Add to source tracker notes |
| New domains | Subsidiaries, acquired companies, partner portals | Feed back into hunt engine for new discovery cycle |
| Exfiltrated records | Database dumps from internal systems | Register in acquisition tracker |

### Ingesting Return Data

```bash
# Register elliot's output in tyrell's acquisition tracker
node ${CLAUDE_PLUGIN_ROOT}/scripts/acquisition-tracker.js add \
  elliot-return \
  <path-to-elliot-output> \
  jsonl \
  --records <N> \
  --source-plugin elliot

# If elliot discovered new internal databases, add them as sources
node ${CLAUDE_PLUGIN_ROOT}/scripts/source-tracker.js add \
  exposed-db <internal-host:port> "Internal <db-type> discovered via elliot pivot" \
  --service <mongo|elastic|redis|mysql|postgres> \
  --access-method login
```

### Closing the Loop

The return flow creates a feedback loop:

```
tyrell finds exposed DB → acquires data → hands off to elliot
                                                    │
elliot exploits target → discovers internal DB ─────┘
                                                    │
tyrell receives internal intel → new hunt cycle ────┘
```

Each iteration deepens access. Track iterations by noting the `source-plugin` field in acquisition entries.

---

## Routing Decision Matrix

Use this to decide whether to route through the pipeline or handle within tyrell:

| Scenario | Route | Why |
|----------|-------|-----|
| Open database, no auth | **Stay in tyrell** — data-acquisition skill | Direct dump, no exploitation needed |
| Protected database, no credentials | **Handoff to elliot** | Needs active exploitation (auth bypass, injection) |
| Protected database, credentials found in dumps | **Try in tyrell first**, then handoff if creds fail | Attempt direct auth before escalating |
| Cloud keys discovered (AWS/GCP/Azure) | **Handoff to elliot** | Cloud exploitation requires elliot's lateral movement skills |
| Web application credentials (admin panels) | **Handoff to elliot** | Web exploitation is elliot's domain |
| VPN/SSH credentials | **Handoff to elliot** | Network access enables pivot, which is elliot's workflow |
| Internal database discovered via elliot pivot | **Return to tyrell** | Data acquisition is tyrell's domain |

---

## Additional Resources

- **`references/elliot-handoff.md`** — Handoff package structure, HANDOFF.md template, scope.md format, target-intel.jsonl schema, attachment guidelines, and worked examples
- **`references/target-enrichment.md`** — Intelligence extraction from dumps, credential analysis, infrastructure mapping, wordlist generation, and correlation methodology
- **`references/return-flow.md`** — Post-exploitation data ingestion, internal database handling, feedback loop patterns, and multi-iteration campaign management
