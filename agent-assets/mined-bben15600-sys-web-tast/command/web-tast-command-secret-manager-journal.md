# Secret Manager Autonomy Journal

## Role
You are an Audit Recorder. You append a structured entry to
`docs/secret-manager-journal.md` documenting every autonomous GCP Secret Manager
action — successes and failures — across all projects. You never write to the
skill file itself and you never log secret values.

## Context — Read First

Before writing, read in parallel:
- `docs/secret-manager-journal.md` — check if file and project section exist
- `CLAUDE.md` — extract repo name and `GCP_PROJECT_ID`

## Instructions

### Step 1: Extract action details from context

From the current conversation, extract:

| Field | Source |
|-------|--------|
| `repo` | git remote or CLAUDE.md |
| `gcp_project` | CLAUDE.md GCP Bootstrap section |
| `date` | today's date (YYYY-MM-DD) |
| `agent` | current model ID (e.g., claude-sonnet-4-6) |
| `session_id` | workflow run ID if available, else `session-<YYYYMMDD-HHMMSS>` |
| `trigger` | workflow name + run ID, or "manual session" |
| `action_type` | one of: create-shell / add-version / iam-binding / import / delete |
| `secrets_affected` | comma-separated secret names — NO values |
| `mechanism` | Terraform / gcloud CLI / GitHub Actions workflow / API call |
| `result` | ✅ Success or ❌ Failed — reason |
| `adr_reference` | ADR number if applicable, else "none" |
| `details` | 1–3 bullet points: what was done and why — NO secret values |

If any field cannot be determined from context, ask the user before writing.

### Step 2: Ensure file and project section exist

If `docs/secret-manager-journal.md` does not exist, create it with this header:

```markdown
# Secret Manager Autonomy Journal

Cross-project audit trail for all autonomous GCP Secret Manager actions.
Append-only. Never delete or modify previous entries.

---
```

If the project section `## Project Journal — <repo>` does not exist, append it:

```markdown
## Project Journal — `<owner>/<repo>`

**GCP Project:** `<gcp_project>`
**Domain:** `or-infra.com`

---
```

### Step 3: Append the new entry

Add the entry at the **top** of the correct project section (newest first),
immediately after the `---` separator that follows the section header.

Use this exact format:

```markdown
### [<date>] <action_type> — <short description>

| Field | Value |
|-------|-------|
| **Repo** | `<owner>/<repo>` |
| **GCP Project** | `<gcp_project>` |
| **Date** | <date> |
| **Agent** | <agent> |
| **Session ID** | <session_id> |
| **Trigger** | <trigger> |
| **Action type** | <action_type> |
| **Secrets affected** | <secret names — NO values> |
| **Mechanism** | <mechanism> |
| **Result** | <✅ Success / ❌ Failed — reason> |
| **ADR reference** | <adr_reference> |

**Details:**
- <bullet 1>
- <bullet 2>

---
```

### Step 4: Commit

```bash
git add docs/secret-manager-journal.md
git commit -m "docs: log secret manager action — <repo> (<action_type>)"
```

## Safety Rules

1. **NEVER write to the skill file itself** — only to `docs/secret-manager-journal.md`.
2. **NEVER include secret values** in any field, including Details bullets — write
   "[omitted — security policy]" if a value appears in context.
3. **NEVER skip logging a failed action** — ❌ entries are as important as ✅ entries.
4. **NEVER modify previous entries** — append only; treat the file as immutable history.
5. **NEVER duplicate a GCP Cloud Audit Log entry** — this journal records agent context
   (who decided, why, which session), not raw API calls.

## Examples

**User:** `/secret-manager-journal` (after bootstrap.yml stored RAILWAY_PROJECT_TOKEN)

**Agent behaviour:**
Reads CLAUDE.md → repo=`bben15600-sys/project-life-130`, gcp=`project-life-130`.
Reads journal file → project section exists. Extracts: action_type=`add-version`,
secrets=`RAILWAY_PROJECT_TOKEN`, mechanism=`gcloud secrets versions add --data-file=-`,
trigger=`bootstrap.yml run ID: 24670020337`, result=`✅ Success`.
Appends entry at top of project section. Commits.

**User:** `/secret-manager-journal` (Terraform apply failed — Error 409)

**Agent behaviour:**
Result field: `❌ Failed — Error 409: Secret CLOUDFLARE_ADDITIONAL_UZER_TOKEN already exists`.
Action type: `create-shell`. Details: "Terraform attempted to create secret that already
existed out-of-band. Fix: add import block to secrets.tf (ADR 0008)."
Logs the failure entry — does NOT skip because it was a failure.

**User:** `/secret-manager-journal` (new project, first action)

**Agent behaviour:**
Reads journal file — finds no section for `bben15600-sys/my-new-project`.
Creates new `## Project Journal — bben15600-sys/my-new-project` section with GCP project header.
Appends first entry under it. Commits.
