---
name: geo-client
description: >
  Per-site folder manager. Creates and maintains a folder per audited domain
  under `site-client/<slug>/` to group all artefacts (audits, PDFs, evolution
  reports, assets) of a same site together. Auto-generates an INDEX.md
  dashboard. Use when starting work on a new domain or to navigate existing
  audits.
version: 2.0.0
tags: [geo, audit, folders, organization]
allowed-tools: Bash, Read, Write
---

# GEO Per-Site Folder Manager

## Purpose

Organise all GEO audit artefacts (audits, PDFs, delta reports, generated assets) **by audited site**, not by file type. Each domain audited has a dedicated folder under `site-client/`.

This skill is the **storage backbone** used by `/geo audit`, `/geo report`, `/geo report-pdf`, `/geo compare` — they all route their output into the relevant site folder owned by this skill. It is a pure organisational layer with no CRM or commercial responsibilities.

---

## Folder Convention

The client folder lives **inside the repo**, at `<repo>/site-client/` — one level above `skills/`, `agents/`, `scripts/`. It's gitignored by default so client data stays local.

```
<repo>/site-client/
├── INDEX.md                          ← auto-generated dashboard
└── <slug>/                           ← one folder per audited site
    ├── info.json                     ← minimal metadata (name, last score, audit count)
    ├── audits/
    │   ├── YYYY-MM-DD-audit.md       ← /geo audit output
    │   ├── YYYY-MM-DD-audit.pdf      ← /geo report-pdf output
    │   ├── YYYY-MM-DD-data.json      ← intermediate data for PDF generation
    │   └── YYYY-MM-DD-report.md      ← /geo report synthesis
    ├── reports/
    │   └── YYYY-MM-delta.md          ← /geo compare output (audit deltas)
    └── assets/                       ← screenshots, generated schema JSON, notes
```

Resolution: `scripts/client_paths.py` computes the absolute path via `Path(__file__).resolve().parent.parent / "site-client"` — so it works regardless of CWD or whether the skill was invoked via symlink. Override with env var `SITE_CLIENT_ROOT` if you need a different location.

### Slug rules

A "slug" is a normalized domain used as folder name:
- Strip `http://` / `https://`
- Strip leading `www.`
- Keep subdomains (`blog.example.com` stays distinct from `example.com`)
- Lowercase, drop path/query/fragment

Examples:
- `https://www.slidor.fr/` → `slidor.fr`
- `Example.COM/path?q=1` → `example.com`
- `blog.example.co.uk` → `blog.example.co.uk`

Always use `scripts/client_paths.py slug <url>` to compute the slug — never do it manually.

---

## Commands

| Command | What It Does |
|---|---|
| `/geo client new <domain> [--name "Company"]` | Create client folder + info.json |
| `/geo client list` | Tabular view of all clients |
| `/geo client show <domain>` | Client detail + artifact tree |
| `/geo client open <domain>` | Open client folder in Finder |
| `/geo client index` | Regenerate `site-client/INDEX.md` |
| `/geo client paths <url>` | Print shell paths for a client (used by other skills) |

---

## Orchestration

### `/geo client new <domain> [--name "Company"]`

```bash
python3 ~/.claude/skills/geo/scripts/client_paths.py init "<domain>" --name "<Company>"
python3 ~/.claude/skills/geo/scripts/client_paths.py index
```

If the symlinked path doesn't resolve, fall back to invoking the script from the repo root:
`python3 -m scripts.client_paths` (run with the repo as the current working directory).

Confirm to user:
```
✓ Client folder created: site-client/<slug>/
  info.json, audits/, reports/, assets/ ready
  Next: /geo audit https://<domain>
```

### `/geo client list`

```bash
python3 <path>/client_paths.py list
```

### `/geo client show <domain>`

```bash
python3 <path>/client_paths.py show "<domain>"
```

### `/geo client open <domain>`

```bash
eval "$(python3 ~/.claude/skills/geo/scripts/client_paths.py paths '<domain>')"
open "$CLIENT_DIR"
```

### `/geo client index`

```bash
python3 <path>/client_paths.py index
```

### `/geo client paths <url>` (internal helper)

Used by `/geo audit`, `/geo report-pdf`, etc. to get all output paths at once. Returns shell-evalable KEY=VALUE lines:

```bash
eval "$(python3 <path>/client_paths.py paths '<url>')"
# Now $CLIENT_DIR, $AUDIT_MD, $AUDIT_PDF, $PROPOSAL_MD, $COMPARE_MD, $INFO_JSON are set
```

The folder structure is **auto-created** by this call — no need to run `/geo client new` first.

---

## info.json schema (minimal — audit metadata only)

```json
{
  "domain": "slidor.fr",
  "name": "Slidor",
  "url": "https://www.slidor.fr/",
  "country": "FR",
  "language": "fr",
  "geo_score": null,
  "last_audit_date": null,
  "audit_count": 0,
  "created_at": "2026-04-23",
  "updated_at": "2026-04-23",
  "tags": []
}
```

The schema is intentionally minimal: domain, display name, URL, locale, last score, and free-form tags for the user to organise sites. **No CRM fields** (no status, monthly value, contacts, contract dates) — those belong to a separate sales tool, not to a GEO audit toolkit.

When another skill updates a site (e.g. `/geo audit` finishes), it should:
1. Read `info.json`
2. Update `geo_score`, `last_audit_date`, increment `audit_count`, set `updated_at`
3. Write `info.json` back
4. Run `client_paths.py index` to refresh the dashboard

---

## Integration points

- `/geo audit <url>` → calls `client_paths.py paths <url>` → writes to `$AUDIT_MD`, updates `info.json.geo_score`, regenerates INDEX
- `/geo report <url>` → writes to `$REPORT_MD` (synthesis)
- `/geo report-pdf <url>` → writes to `$AUDIT_PDF` in same folder
- `/geo compare <domain>` → writes to `$COMPARE_MD` in `reports/`

---

## Notes

- `site-client/` is **visible in Finder** (no dot prefix) — intentional, to let the user browse artifacts directly.
- Legacy path `~/.geo-prospects/` from upstream is **deprecated and removed**. All paths route through `<repo>/site-client/<slug>/`.
- `info.json` is the source of truth per audited site. No central JSON DB (scan `site-client/*/info.json` on demand).
