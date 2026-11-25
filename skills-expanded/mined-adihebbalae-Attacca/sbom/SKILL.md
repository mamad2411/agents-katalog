---
name: sbom
description: "Generate a Software Bill of Materials (SBOM) and scan for CVEs. Use before production pushes, when dependency files change, or on security request. Artifacts written to .attacca/sbom/."
---

<!-- Delete when: native Claude Code dependency graph visualization with automatic CVE detection is available -->

# SBOM Generation Skill

Generate a real, machine-readable Software Bill of Materials (SBOM) capturing all dependencies. Scan for CVEs. Artifacts go to `.attacca/sbom/`.

## When to Use
- Before production pushes
- When dependency files change (`package.json`, `requirements.txt`, `go.mod`, etc.)
- Monthly audit of long-lived systems
- On security request

## Quick Flow

1. **Generate SBOM** using syft or cdxgen
2. **Scan for CVEs** using osv-scanner or grype
3. **Report** to `.attacca/sbom/latest.json` (CycloneDX format)
4. **Triage**: CRITICAL/HIGH → block push; MEDIUM/LOW → flag for review

---

## Step 1: Detect SBOM Tool

Check what's available (in order):

```bash
syft version 2>/dev/null && echo "syft available"
npx @cyclonedx/cdxgen --version 2>/dev/null && echo "cdxgen available"
npm sbom --version 2>/dev/null && echo "npm-sbom available"
```

If none available, install syft:

```bash
# Mac / Linux
curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin

# Windows
winget install anchore.syft
```

---

## Step 2: Generate SBOM

### Option A: syft (recommended)

```bash
mkdir -p .attacca/sbom
syft . -o cyclonedx-json=.attacca/sbom/latest.json
```

### Option B: cdxgen

```bash
mkdir -p .attacca/sbom
npx @cyclonedx/cdxgen -o .attacca/sbom/latest.json
```

### Option C: npm sbom

```bash
mkdir -p .attacca/sbom
npm sbom --sbom-format cyclonedx --sbom-type library > .attacca/sbom/latest.json
```

---

## Step 3: Scan for CVEs

```bash
# Using osv-scanner (recommended)
osv-scanner --sbom .attacca/sbom/latest.json

# Or using grype
grype sbom:.attacca/sbom/latest.json

# Install osv-scanner if needed
go install github.com/google/osv-scanner/cmd/osv-scanner@latest
```

---

## Step 4: Parse Summary

Extract summary from SBOM:

```bash
python3 << 'EOF'
import json
with open('.attacca/sbom/latest.json') as f:
    sbom = json.load(f)
comps = sbom.get('components', [])
print(f'Total packages: {len(comps)}')
for c in comps[:10]:
    print(f"  {c.get('name')}@{c.get('version','?')}")
if len(comps) > 10:
    print(f'  ... and {len(comps)-10} more')
EOF
```

---

## Step 5: Report Template

Write findings to `.attacca/sbom/report.md`:

```markdown
# SBOM Report — [project] — [date]

## Generation
- Tool: syft / cdxgen / npm
- Format: CycloneDX JSON
- Time: [ISO timestamp]

## Inventory
- Total packages: [n]
- Direct: [n]
- Transitive: [n]

## CVE Scan
- CRITICAL: [n]
- HIGH: [n]
- MEDIUM: [n]
- LOW: [n]

### CRITICAL/HIGH Findings
[List any, with links to advisories]

## Anomalies
- [ ] Non-standard registries: [yes/no]
- [ ] Missing licenses: [yes/no]
- [ ] Old packages (2+ years): [yes/no]

## Gate Status
- CRITICAL/HIGH found: ❌ BLOCK PUSH
- All clean: ✅ APPROVED
```

---

## Pass / Fail

| Check | Pass | Fail |
|-------|------|------|
| SBOM generated | ✅ | ❌ Error |
| CRITICAL CVEs | ✅ Zero | ❌ Found |
| HIGH CVEs | ✅ Zero | ⚠️ Review |
| Licensed | ✅ All | ❌ Unlicensed |
| Lock file | ✅ Present | ⚠️ Missing |

**BLOCK PUSH if**: any CRITICAL CVEs found.

---

## Optional: Commit SBOM

If your policy requires SBOM in source control:

```bash
git add .attacca/sbom/
git commit -m "chore: update SBOM"
```

Or add to .gitignore if SBOM should stay private:

```bash
echo ".attacca/sbom/" >> .gitignore
```

---

## Run Before Production Pushes

Include this in your pre-push checklist before shipping to production.
