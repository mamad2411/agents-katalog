---
name: migrate-to-dovetail
description: Migrate data from Notion, Confluence, Google Drive, Airtable, Marvin, Condens, EnjoyHQ, Productboard, or local files into Dovetail using the dt CLI.
license: MIT
metadata:
  author: dovetail
  version: "1.0"
---

# Migrate data into Dovetail

Use the `dt` CLI to import content from an existing tool into your Dovetail workspace. Always **preview before importing** and wait for user approval before running the actual migration.

## Prerequisites

1. `dt` is installed — if not, run `npm install -g @heydovetail/dt`
2. Workspace is configured — if not, run `dt init`
3. `DOVETAIL_API_KEY` is set (from workspace Settings > API)

## Standard workflow

```
install → init → source add → validate → preview → [user approves] → migrate run
```

```bash
# 1. Connect a source
dt source add <source>

# 2. Test connectivity
dt source validate <source>

# 3. Preview what will be imported
dt migrate run --source <source> --preview

# 4. [Wait for user approval]

# 5. Run the import
dt migrate run --source <source>
```

**Always show the preview output to the user and ask for explicit approval before step 5.**

---

## dt.json config structure

When writing `dt.json` manually, migrations follow this structure:

```json
{
  "dovetail": {
    "api_key": "your-api-key",
    "base_url": "https://mycompany.dovetail.com"
  },
  "sources": {
    "<source>": {
      "<option-key>": "<value>"
    }
  },
  "migrations": [
    {
      "source": "<source>",
      "content": ["<url-id-or-type>"],
      "destination": {
        "type": "data",
        "parent": {
          "type": "project",
          "name": "Destination Project Name"
        }
      },
      "options": {}
    }
  ]
}
```

- `content` — array of URLs, IDs, space keys, or type names passed to the source
- `destination.type` — `"data"` (recordings, transcripts, files) or `"doc"` (reports, notes)
- `destination.parent.type` — `"project"` or `"folder"`
- `options` — source-specific extras; rarely needed (see Marvin and Local below)

---

## Sources

### Notion

**What migrates:** Pages and database entries, formatting, attachments, metadata, child pages (up to 3 levels deep).

**Prerequisites:** Create a Notion integration at https://www.notion.so/my-integrations and share your databases with it.

```bash
export NOTION_TOKEN="ntn_xxxxxxxxxxxx"
dt source add notion
dt source validate notion
dt migrate run --source notion --preview
# wait for approval
dt migrate run --source notion
```

**Manual `dt.json`:**
```json
{
  "sources": {
    "notion": {
      "token": "ntn_xxxxxxxxxxxx"
    }
  },
  "migrations": [
    {
      "source": "notion",
      "content": ["notion-database-id-here"],
      "destination": {
        "type": "data",
        "parent": { "type": "project", "name": "Customer Research" }
      }
    }
  ]
}
```

---

### Confluence

**What migrates:** Cloud pages and blog posts, attachments, labels, author info, creation/modification dates.

**Prerequisites:** Create a Confluence API token at https://id.atlassian.com/manage-profile/security/api-tokens.

```bash
export CONFLUENCE_API_TOKEN="your-api-token"
dt source add confluence
dt source validate confluence
dt migrate run --source confluence --preview
# wait for approval
dt migrate run --source confluence
```

**Manual `dt.json`:**
```json
{
  "sources": {
    "confluence": {
      "base_url": "https://mycompany.atlassian.net/wiki",
      "email": "you@company.com",
      "token": ""
    }
  },
  "migrations": [
    {
      "source": "confluence",
      "content": ["PROD"],
      "destination": {
        "type": "doc",
        "parent": { "type": "project", "name": "Product Knowledge Base" }
      }
    }
  ]
}
```

The `content` value is the Confluence space key (e.g. `"PROD"`).

---

### Google Drive

**What migrates:** Google Docs (as HTML), optionally Sheets (as CSV), PDFs, images, and other files. Folder structure is preserved.

**Prerequisites (choose one):**
- **OAuth:** Create a Google Cloud project, enable the Drive API, create an OAuth Desktop client ID. The wizard opens a browser sign-in.
- **Service account:** Create a service account, download the JSON key, share your Drive folder with the service account email.

```bash
# Service account only:
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"

dt source add gdrive
dt source validate gdrive
dt migrate run --source gdrive --preview
# wait for approval
dt migrate run --source gdrive
```

**Manual `dt.json`:**
```json
{
  "sources": {
    "gdrive": {
      "credentials_file": "/path/to/key.json",
      "recursive": "true",
      "include_binary": "true"
    }
  },
  "migrations": [
    {
      "source": "gdrive",
      "content": ["1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs"],
      "destination": {
        "type": "data",
        "parent": { "type": "project", "name": "UX Research Archive" }
      }
    }
  ]
}
```

The `content` value is the Google Drive folder ID.

---

### Airtable

**What migrates:** Records with all field values, attachments, linked records, and metadata.

**Prerequisites:** Create a personal access token at https://airtable.com/create/tokens with `data.records:read` and `schema.bases:read` scopes.

```bash
export AIRTABLE_TOKEN="your-token"
dt source add airtable
dt source validate airtable
dt migrate run --source airtable --preview
# wait for approval
dt migrate run --source airtable
```

**Manual `dt.json`:**
```json
{
  "sources": {
    "airtable": {
      "token": ""
    }
  },
  "migrations": [
    {
      "source": "airtable",
      "content": ["https://airtable.com/appXXXXXXXXXXXXXX/tblXXXXXXXXXXXXXX"],
      "destination": {
        "type": "data",
        "parent": { "type": "project", "name": "User Interview Tracker" }
      }
    }
  ]
}
```

The `content` value is the full URL to the Airtable table.

---

### Marvin

**What migrates:** Video/audio recordings (Dovetail auto-transcribes) and insights as docs.

Marvin has no public export API. You must first export your data locally:

**Step 1: Export from Marvin**

Use the `/marvin-download` skill to automate this with browser automation, or manually:
- Download recordings from each project: All Actions > Download Video
- Copy insight content into markdown files

Expected export structure:
```
marvin-export/
  Project Name/
    files/
      Interview 1.mp4
    insights/
      My Report/
        content.md
        metadata.json
```

**Step 2: Import with dt**

```bash
dt source add marvin
dt migrate run --source marvin --preview
# wait for approval
dt migrate run --source marvin
```

**Manual `dt.json`:**
```json
{
  "migrations": [
    {
      "source": "marvin",
      "content": ["./marvin-export/Customer Interviews"],
      "destination": {
        "type": "data",
        "parent": { "type": "project", "name": "Customer Interviews" }
      },
      "options": { "types": "files" }
    },
    {
      "source": "marvin",
      "content": ["./marvin-export/Customer Interviews"],
      "destination": {
        "type": "doc",
        "parent": { "type": "project", "name": "Customer Interviews" }
      },
      "options": { "types": "insights" }
    }
  ]
}
```

The `content` value is the path to the exported project directory. `options.types` is `"files"` or `"insights"`.

---

### Condens

**What migrates:** Sessions (notes, transcripts, video) as data; artifacts (reports) as docs.

**Step 1: Export from Condens**

In Condens: **Project > Settings > Export data** — download the `.zip` file.

**Step 2: Import with dt**

```bash
dt source add condens
dt migrate run --source condens --preview
# wait for approval
dt migrate run --source condens
```

**Manual `dt.json`:**
```json
{
  "migrations": [
    {
      "source": "condens",
      "content": ["/path/to/Onboarding Research.abc123.zip"],
      "destination": {
        "type": "data",
        "parent": { "type": "project", "name": "Onboarding Research" }
      }
    }
  ]
}
```

The `content` value is the path to the Condens export zip file.

---

### EnjoyHQ

**What migrates:** Stories, projects, and documents with labels, state, customer info, and tags.

**Prerequisites:** Get your API token from EnjoyHQ workspace settings.

```bash
export ENJOYHQ_API_TOKEN="your-token"
dt source add enjoyhq
dt source validate enjoyhq
dt migrate run --source enjoyhq --preview
# wait for approval
dt migrate run --source enjoyhq
```

---

### Productboard

**What migrates:** Notes (customer feedback) and features (with descriptions and metadata).

**Prerequisites:** Go to **Settings → Integrations → Public API → Generate Access Token**.

```bash
export PRODUCTBOARD_API_TOKEN="your-token"
dt source add productboard
dt source validate productboard
dt migrate run --source productboard --preview
# wait for approval
dt migrate run --source productboard
```

**Manual `dt.json`:**
```json
{
  "sources": {
    "productboard": {
      "token": ""
    }
  },
  "migrations": [
    {
      "source": "productboard",
      "content": ["notes"],
      "destination": {
        "type": "data",
        "parent": { "type": "project", "name": "Productboard Notes" }
      }
    },
    {
      "source": "productboard",
      "content": ["features"],
      "destination": {
        "type": "data",
        "parent": { "type": "project", "name": "Productboard Features" }
      }
    }
  ]
}
```

The `content` value is the entity type: `"notes"` or `"features"`. Both import as data.

---

### Local files

**What migrates:** `.md`, `.txt`, `.html` files become the record body. Everything else (PDFs, videos, images, Word docs) is uploaded as an attachment.

```bash
dt source add local
dt migrate run --source local --preview
# wait for approval
dt migrate run --source local
```

**Manual `dt.json`:**
```json
{
  "migrations": [
    {
      "source": "local",
      "content": ["/path/to/your/folder"],
      "destination": {
        "type": "data",
        "parent": { "type": "project", "name": "Research Files" }
      },
      "options": { "extensions": ".md,.pdf,.mp4" }
    }
  ]
}
```

The `content` value is the path to the local folder. `options.extensions` is optional; omit to include all files.

---

## Useful flags

| Flag | Description |
|------|-------------|
| `--preview` | Show what would be migrated without fetching |
| `--dry-run` | Fetch and transform but skip upload |
| `--upsert` | Re-run without creating duplicates |
| `--limit N` | Process at most N records per migration |
| `--filter "title:X"` | Filter by title |
| `--filter "created_after:2024-01-01"` | Filter by creation date |
| `--filter "updated_after:2024-01-01"` | Filter by update date |
| `--verbose` | Detailed per-record progress logs |
| `--source X` | Run only migrations for source X |

## Destination types

When using `--project` and `--type` flags on the CLI, use the legacy type strings:

| `--type` | `destination.type` in dt.json | `destination.parent.type` | Description |
|----------|-------------------------------|---------------------------|-------------|
| `project-data` | `"data"` | `"project"` | Data (recordings, transcripts, files) inside a project |
| `project-doc` | `"doc"` | `"project"` | Docs inside a project |
| `folder-doc` | `"doc"` | `"folder"` | Docs directly in a folder |

## Running all migrations at once

If multiple sources are configured in `dt.json`:

```bash
dt migrate run           # run everything
dt migrate run --source notion  # run one source only
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "no records fetched" | Check source access: Notion database shared with integration, Drive folder shared with service account, correct Confluence space key, valid Airtable token scopes |
| "403 Forbidden" | Dovetail API key may lack permissions, or source account doesn't have read access |
| "401 Unauthorized" | API key or token is invalid or expired |
| Rate limited | Automatic — the CLI retries with exponential backoff |
| Migration interrupted | Run `dt migrate resume` to continue from where it stopped |
| Migration seems stuck | Run `dt migrate run --verbose` for detailed progress |

Run `dt doctor` for a full environment and connectivity diagnostic.
