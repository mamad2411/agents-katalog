---
name: followups
description: "Surface open action items and unresponded customer emails across all customer engagements. Triggers include: 'followups', 'open items', 'what's pending', 'action items', 'follow up', 'what do I need to do', 'pending actions', 'unresponded emails', or any request to see outstanding work across customers."
---

# /followups — Cross-Customer Follow-up Tracker

Scan all customer engagement repos for open action items and identify unresponded
customer emails via Microsoft 365. Presents a unified view grouped by customer and
project so nothing falls through the cracks.

## Folder Structure

Each customer engagement repo uses a project-subfolder model:

```
~/customer-engagements/{customer-slug}/
├── README.md              ← customer-level overview
├── stakeholders.md        ← shared; used for email domain lookup
├── projects/
│   ├── {project-slug}/
│   │   ├── README.md
│   │   ├── followups.md   ← action items live here (per-project)
│   │   ├── meetings/
│   │   ├── decisions/
│   │   └── architecture/
```

Key points:
- `followups.md` lives inside each **project**, not at the customer root.
- `stakeholders.md` remains at the **customer** root.
- A single customer can have multiple projects, each with its own followups.

## Platform Compatibility

This skill runs on **macOS, Linux, and Windows**. It is read-only — it just lists directories and reads files. Detect the OS and pick the right syntax. See `_shared/PLATFORM.md` (skills repo root) for the full table.

| Action | macOS / Linux (bash) | Windows (PowerShell) |
|--------|----------------------|----------------------|
| List dir | `ls $HOME/customer-engagements/` | `Get-ChildItem $HOME/customer-engagements/` |
| Test file exists | `[ -f file ]` | `Test-Path file` |
| Home dir | `~` or `$HOME` | `$HOME` |

Default to POSIX commands; use PowerShell on Windows native (not WSL/Git Bash).

## Core Principles

- **Never fabricate content.** Only include action items found in followups.md files and emails retrieved from M365 tools. If a source is unavailable, say so explicitly — do not invent action items or email threads.
- **Preserve source language.** Section headings are always English. Content (action item text, email subjects) stays in its original language — do not translate Hebrew to English or vice versa. Preserve Hebrew text as-is. Extract action items from both English and Hebrew text.
- **Graceful degradation.** Every data source can fail independently. The report must still be useful even when some sources return nothing. Note what's missing so the user knows what to check manually.
- **Read-only operation.** This skill never writes to any file. It reads followups.md, stakeholders.md, and queries M365 — but modifies nothing on disk. No git operations.
- **Cross-platform paths.** All paths use `~` prefix (e.g., `~/customer-engagements/`) for portability across environments.

## Prerequisite Auto-Install

Before running, verify all dependencies are present. **Install anything missing automatically.**

### Required Sibling Skills

This skill requires the following sibling skill from the same repository
(`https://github.com/roie9876/clawpilot-skills`):

| Skill | Purpose | Required? |
|-------|---------|-----------|
| `/customer-repo` | Customer engagement folder structure (`~/customer-engagements/`) | ✅ For reading follow-ups |

Check if it is installed:

```bash
# macOS / Linux
[ -f "$HOME/.copilot/skills/customer-repo/SKILL.md" ] && echo "✅ customer-repo" || echo "❌ customer-repo MISSING"
```

```powershell
# Windows
if (Test-Path "$HOME\.copilot\skills\customer-repo\SKILL.md") { "✅ customer-repo" } else { "❌ customer-repo MISSING" }
```

**If missing**, install all skills from the repository:

1. Clone the repo (skip if already cloned):
   ```bash
   # macOS / Linux
   [ -d "$HOME/customer-skills/.git" ] || git clone https://github.com/roie9876/clawpilot-skills.git "$HOME/customer-skills"
   ```
   ```powershell
   # Windows
   if (-not (Test-Path "$HOME\customer-skills\.git")) {
       git clone https://github.com/roie9876/clawpilot-skills.git "$HOME\customer-skills"
   }
   ```

2. Run the installer (idempotent — safe to re-run):
   ```bash
   # macOS / Linux
   bash "$HOME/customer-skills/scripts/install.sh"
   ```
   ```powershell
   # Windows
   pwsh "$HOME\customer-skills\scripts\install.ps1"
   ```

3. Verify installed. If still missing, stop and report the error.

### M365 Sign-In

Check `m_m365_status`. If not signed in → call `m_m365_sign_in`.

---

## Step 1: Determine Scope

Decide whether to scan all customers, a single customer (all projects), or a specific customer/project.

**Default: ALL customers, all projects**

If the user did not name a specific customer (e.g., just "/followups"):

1. Run `ls ~/customer-engagements/` to list all customer folders.
2. Set `{slugs}` to the full list of folder names. Each slug will have all its projects scanned.
3. If the directory is empty or does not exist → report "No customer engagement folders found at ~/customer-engagements/. Run /customer-repo to create one." and stop.

**Single customer mode (all projects):**

If the user names a specific customer (e.g., "/followups checkpoint"), use the 4-tier detection chain to resolve the customer:

1. **Folder name match** — Check if the user's input (lowercased, hyphenated) matches an existing folder in `~/customer-engagements/` exactly.
2. **Folder scan** — Run `ls ~/customer-engagements/` and fuzzy-match the user's input against folder names (case-insensitive, partial match, with/without hyphens).
3. **Meeting subject** — If no folder match, check recent meeting subjects for the customer name to confirm they exist.
4. **User prompt** — If still ambiguous, present the closest matches and ask the user to pick, or confirm the intended customer.

If the customer folder is not found → report "No folder found for '{customer}' in ~/customer-engagements/. Did you mean one of these: {closest matches}?" and stop.

Set `{slugs}` to the single matched folder name. All projects under that customer will be scanned.

**Customer/project mode (single project):**

If the user specifies a customer and project separated by a slash (e.g., "/followups checkpoint/sase"):

1. Split the input on `/` into `{customer-input}` and `{project-input}`.
2. Resolve `{customer-input}` using the same 4-tier detection chain above.
3. Check if `~/customer-engagements/{customer-slug}/projects/{project-input}` exists.
4. If the project folder exists → set `{slugs}` to the single customer and restrict scanning to only that project.
5. If the project folder does not exist → run `ls ~/customer-engagements/{customer-slug}/projects/` and fuzzy-match. If ambiguous, present closest matches and ask the user to pick. If no projects/ directory → report "No projects/ directory found for '{customer}'." and stop.

## Step 2: Scan followups.md Files

For each `{slug}` in `{slugs}`:

1. **List projects:** Run `ls ~/customer-engagements/{slug}/projects/` to get all project subfolders. If in customer/project mode, use only the specified project.
2. **For each `{project}` in the project list:**
   a. **Read the file:** `~/customer-engagements/{slug}/projects/{project}/followups.md`
   b. **Locate the `## Open` section** and parse the markdown table rows.
   c. **Collect rows where Status is `🔴 Open`.** Extract the Action, Owner, and Due columns.
   d. **Attribute each item** with both the customer name (derived from `{slug}` — convert hyphens to spaces, title-case) and the project name (derived from `{project}` — convert hyphens to spaces, title-case).

**Edge cases:**

- **No `projects/` directory for a customer** → Skip this customer. Record: "{customer}: no projects/ directory found."
- **`projects/` directory exists but is empty** → Skip this customer. Record: "{customer}: no projects found."
- **`followups.md` missing for a project** → Skip that project. Record: "{customer}/{project}: followups.md not found."
- **File contains only placeholder HTML comments** (e.g., `<!-- Describe the action item -->`) → Treat as empty. Record: "{customer}/{project}: no open action items."
- **No `## Open` section** → Skip this project. Record: "{customer}/{project}: no Open section in followups.md."
- **`## Open` section exists but table is empty or has only the header** → Record: "{customer}/{project}: no open action items."

## Step 3: Find Unresponded Customer Emails

Email checking operates at the **customer level**, not the project level. `stakeholders.md` is at the customer root.

For each `{slug}` in `{slugs}`:

1. **Extract the customer email domain:** Read `~/customer-engagements/{slug}/stakeholders.md`. Parse the stakeholder table and extract email addresses from the Email column. Identify the external domain (e.g., `contoso.com` from `alice@contoso.com`). Use the first non-internal domain found.

2. **Search for recent inbound emails from the customer:**

   ```
   m365_search_emails(query: "from:{customer-domain}", folder: "inbox", startDate: "{14-days-ago}", limit: 20)
   ```

   This returns recent emails received from the customer domain.

3. **Load recent sent emails:**

   ```
   m365_list_emails(folder: "sent", startDate: "{14-days-ago}", limit: 50)
   ```

4. **Cross-reference to find unresponded emails:**
   - For each inbound email, check if there is a sent email with a matching `conversationId`.
   - If no matching `conversationId` is found, fall back to subject-line matching (case-insensitive, ignoring `Re:` / `Fwd:` prefixes).
   - Emails that have no matching sent reply are flagged as **unresponded**.

   > **Note:** This is a heuristic approach. There is no direct "unreplied" API in Microsoft Graph. Responses sent from other clients, shared mailboxes, or delegated accounts may not be detected. The results are best-effort.

5. **Collect unresponded emails** with: sender name, subject, received date.

**Edge cases:**

- **stakeholders.md missing** → Skip email check for this customer. Record: "{customer}: stakeholders.md not found — skipped email check."
- **stakeholders.md has no email addresses or only placeholder comments** → Skip email check. Record: "{customer}: no stakeholder emails found — skipped email check."
- **m365_search_emails fails** → Skip email check for this customer. Record: "{customer}: email search failed — {error}."
- **m365_list_emails fails** → Cannot cross-reference replies. Report inbound emails without reply status. Record: "{customer}: sent email lookup failed — showing all recent inbound emails."
- **No inbound emails found** → Record: "{customer}: no recent inbound emails."

## Step 4: Present Results

Assemble the collected data into a unified report grouped by customer, then by project within each customer.

**Summary counts first:**

Show a quick overview at the top so the user can see the big picture at a glance. The summary includes project counts.

**Then detail per customer:**

For each customer that has at least one open action item or unresponded email, show:
1. Projects with open action items (grouped by project)
2. Unresponded emails (at the customer level, not nested under projects)

Customers with neither open items nor unresponded emails are omitted from the detail section but counted in the summary.

### Content Language Rules

- All section headings → English.
- Action item text, email subjects → preserve in original language (English or Hebrew). Do not translate.
- Customer names → use the display name derived from the folder slug.
- Project names → use the display name derived from the project folder slug.

## Error Handling

| Failure Mode | Behavior |
|-------------|----------|
| `~/customer-engagements/` directory missing or empty | Report "No customer engagement folders found at ~/customer-engagements/." Stop. |
| No `projects/` directory for a customer | Skip that customer's action items. Note "{customer}: no projects/ directory found" in the report. |
| `projects/` directory empty for a customer | Note "{customer}: no projects found" in the report. |
| `followups.md` missing for a project | Skip that project's action items. Note "{customer}/{project}: followups.md not found" in the report. |
| `followups.md` has no `## Open` section or is placeholder-only | Treat as zero open items. Note in report. |
| `stakeholders.md` missing for a customer | Skip email check for that customer. Note "{customer}: skipped email check — no stakeholders.md." |
| `stakeholders.md` has no parseable email addresses | Skip email check for that customer. Note "{customer}: no stakeholder emails found." |
| `m365_search_emails` fails or returns error | Skip email check for that customer. Note "{customer}: email search failed." Continue with other customers. |
| `m365_list_emails` fails or returns error | Cannot determine reply status. Show inbound emails without unresponded filtering. Note the limitation. |
| Single customer not found in `~/customer-engagements/` | Report "No folder found for '{name}'." Suggest closest matches if available. Stop. |
| Project not found under a customer | Report "No project '{project}' found under '{customer}'." Suggest closest matches from `projects/`. Stop. |
| All customers scanned but none have open items or emails | Report "🎉 All clear — no open action items or unresponded emails found across {N} customers." |

## Output Template

```markdown
# 📋 Follow-up Report

**Generated:** {timestamp}
**Scope:** {All customers | {customer-name} | {customer-name}/{project-name}}
**Customers scanned:** {N}
**Projects scanned:** {N}

## Summary

- **Open action items:** {total-count} across {project-count} projects in {customer-count} customers
- **Unresponded emails:** {total-count} across {customer-count} customers
- **Customers with no pending items:** {count}

{If any customers/projects had errors, list them here:}
- ⚠️ {customer}: {error-note}
- ⚠️ {customer}/{project}: {error-note}

---

## {Customer Name}

### Project: {project-name}

#### Open Action Items

| Action | Owner | Due | Status |
|--------|-------|-----|--------|
| {action text} | {owner} | {due date} | 🔴 Open |
| {action text} | {owner} | {due date} | 🔴 Open |

### Project: {project-name-2}

#### Open Action Items

| Action | Owner | Due | Status |
|--------|-------|-----|--------|
| {action text} | {owner} | {due date} | 🔴 Open |

### Unresponded Emails (Last 14 Days)

- **{sender-name}** — "{email-subject}" — received {YYYY-MM-DD}
- **{sender-name}** — "{email-subject}" — received {YYYY-MM-DD}

---

## {Customer Name 2}

### Project: {project-name}

#### Open Action Items

{same format as above}

### Unresponded Emails (Last 14 Days)

{same format as above}

---

{Repeat for each customer with open items or unresponded emails.}

*Generated by /followups on {timestamp}*
```
