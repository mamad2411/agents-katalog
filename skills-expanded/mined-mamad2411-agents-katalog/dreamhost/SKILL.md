---
name: dreamhost-skill
description: Manage DreamHost DNS records. Use when the user asks to manage DNS for domains hosted at DreamHost, set up DNS records, check DNS propagation, or configure A/AAAA/CNAME/TXT records on DreamHost-managed domains.
allowed-tools: Bash, Read
---

# DreamHost Skill - DNS Management

Manage DNS records via the DreamHost API. Add, remove, and update A/AAAA/CNAME/TXT records, check propagation.

## CRITICAL: DNS Modification Confirmation Required

**Before modifying ANY DNS records, you MUST get explicit user confirmation.**

When the user asks to change DNS:
1. First, show current records using `get-records`
2. Show the proposed changes clearly
3. Ask: "Do you want me to apply these DNS changes?"
4. ONLY run set/add/remove commands AFTER the user explicitly confirms
5. NEVER modify DNS without confirmation

## Important Limitations

- **No MX record management** — MX records are managed by DreamHost automatically. Cannot add/remove MX via API.
- **No native update** — To update a record, the skill removes the old and adds the new (set-record handles this).
- **Editable field** — Some records are DreamHost-managed (editable=false) and cannot be modified via the API.
- **Supported types for add/remove**: A, AAAA, CNAME, NS, NAPTR, SRV, TXT

## First-Time Setup (~2 minutes)

### 1. Get API Key

1. Log into [DreamHost Web Panel](https://panel.dreamhost.com)
2. Navigate to the API section (search for "API" in panel)
3. Click **Generate a new API Key**
4. **Select permissions**: `dns-list_records`, `dns-add_record`, `dns-remove_record`
5. Copy the API Key

### 2. Save Credentials

```bash
cat > ~/.claude/skills/dreamhost-skill/config.json << 'EOF'
{
  "api_key": "YOUR_API_KEY"
}
EOF
```

## Commands

### List Domains

Lists all unique domains (zones) in the account with record counts.

```bash
python3 ~/.claude/skills/dreamhost-skill/dreamhost_skill.py list-domains
```

### Get DNS Records

```bash
python3 ~/.claude/skills/dreamhost-skill/dreamhost_skill.py get-records DOMAIN [--type TYPE] [--name NAME]
```

**Examples:**
```bash
# All records
python3 ~/.claude/skills/dreamhost-skill/dreamhost_skill.py get-records epochml.com

# Only A records
python3 ~/.claude/skills/dreamhost-skill/dreamhost_skill.py get-records epochml.com --type A

# Root A records
python3 ~/.claude/skills/dreamhost-skill/dreamhost_skill.py get-records epochml.com --type A --name @
```

### Set DNS Record (Replace)

Removes existing editable records of the same type+name, then adds the new one.

```bash
python3 ~/.claude/skills/dreamhost-skill/dreamhost_skill.py set-record DOMAIN TYPE NAME DATA [--comment COMMENT]
```

**Examples:**
```bash
# Point root to IP
python3 ~/.claude/skills/dreamhost-skill/dreamhost_skill.py set-record epochml.com A @ 66.241.125.165

# Point www to CNAME
python3 ~/.claude/skills/dreamhost-skill/dreamhost_skill.py set-record epochml.com CNAME www myapp.fly.dev

# Add ACME challenge
python3 ~/.claude/skills/dreamhost-skill/dreamhost_skill.py set-record epochml.com CNAME _acme-challenge domain.flydns.net
```

### Add DNS Record

Adds a record without removing existing ones.

```bash
python3 ~/.claude/skills/dreamhost-skill/dreamhost_skill.py add-record DOMAIN TYPE NAME DATA [--comment COMMENT]
```

### Remove DNS Record

Removes a specific record (must specify exact type, name, AND value).

```bash
python3 ~/.claude/skills/dreamhost-skill/dreamhost_skill.py remove-record DOMAIN TYPE NAME VALUE
```

**Example:**
```bash
python3 ~/.claude/skills/dreamhost-skill/dreamhost_skill.py remove-record epochml.com A @ 216.24.57.7
```

### Bulk Set (Multiple Records)

Set many records at once from JSON. For each record, removes existing editable records of the same type+name first.

```bash
# From inline JSON
python3 ~/.claude/skills/dreamhost-skill/dreamhost_skill.py bulk-set DOMAIN '[{"type":"A","name":"@","data":"1.2.3.4"},{"type":"CNAME","name":"www","data":"app.fly.dev"}]'

# From a JSON file
python3 ~/.claude/skills/dreamhost-skill/dreamhost_skill.py bulk-set DOMAIN /path/to/records.json
```

**JSON format:**
```json
[
  {"type": "A", "name": "@", "data": "66.241.125.165"},
  {"type": "AAAA", "name": "@", "data": "2a09:8280:1::d2:59e0:0"},
  {"type": "CNAME", "name": "www", "data": "myapp.fly.dev"},
  {"type": "CNAME", "name": "_acme-challenge", "data": "domain.flydns.net"}
]
```

### Check DNS Propagation

Uses local `dig` to check what DNS currently resolves to.

```bash
python3 ~/.claude/skills/dreamhost-skill/dreamhost_skill.py check-dns DOMAIN
```

## Common Workflows

### Point Domain to Fly.io

```bash
# 1. Check current records
python3 ~/.claude/skills/dreamhost-skill/dreamhost_skill.py get-records mydomain.com

# 2. Set the records Fly.io needs
python3 ~/.claude/skills/dreamhost-skill/dreamhost_skill.py bulk-set mydomain.com '[
  {"type":"A","name":"@","data":"FLY_IPV4"},
  {"type":"AAAA","name":"@","data":"FLY_IPV6"},
  {"type":"CNAME","name":"www","data":"APP.fly.dev"},
  {"type":"CNAME","name":"_acme-challenge","data":"DOMAIN.flydns.net"}
]'

# 3. Verify propagation
python3 ~/.claude/skills/dreamhost-skill/dreamhost_skill.py check-dns mydomain.com
```

## Output Format

All commands output JSON for easy parsing. Errors include detail messages from the DreamHost API.
