---
name: okr-to-jira
description: >
  Convert OKR scoping docs (Google Docs) into a Jira ticket hierarchy — Initiatives, Epics, and Stories.
  Read one or more Google Doc URLs, extract Objectives and Key Results, preview the full hierarchy,
  then create tickets live via Jira REST API or export a Jira-importable CSV.
  Trigger on: "convert my OKRs to Jira tickets", "create tickets from OKR doc",
  "map OKRs to epics and stories", "turn our OKRs into a backlog", or /okr-to-jira.
---

# OKR to Jira Workflow

Converts OKR scoping documents into a Jira ticket hierarchy:

| OKR Element | Jira Issue Type |
|---|---|
| Objective | Initiative (or Feature, depending on Jira configuration) |
| Key Result | Epic (linked to parent Initiative) |
| Inferred implementation step | Story (under Epic, when clearly inferable) |

OKR parsing heuristics: `references/okr-mapping-logic.md`
CSV format specification: `references/jira-csv-format.md`

## Capabilities

- Parse OKR documents in any format (flat lists, numbered, tables, prose) from Google Doc URLs
- Extract Objectives → Initiatives, Key Results → Epics, inferred steps → Stories
- Merge and deduplicate Objectives across multiple input documents
- Show a full detailed preview (titles, descriptions, parent links, labels) with an edit loop before writing
- Create tickets live in Jira via REST API with correct parent-child hierarchy links
- Export a Jira-importable CSV compatible with both classic and next-gen Jira project types
- Apply custom labels per ticket level (Initiatives, Epics, Stories)

## Workflow

1. **Explain** — describe the OKR→Jira mapping before asking for input
2. **Collect** — ask for one or more Google Doc URLs; read all docs
3. **Extract** — parse Objectives, Key Results, and inferred implementation steps
4. **Preview** — show full ticket hierarchy with edit loop; iterate until user confirms
5. **Labels** — ask whether to add labels beyond the automatic `okr-import`
6. **Destination** — choose live Jira creation (project key) or CSV export
7. **Create/Export** — write tickets in order (Initiatives → Epics → Stories) or generate CSV
8. **Summary** — show all created ticket keys with links, or CSV file path

## Examples

### Example: Convert a single OKR doc to Jira tickets
User says: "Convert my OKRs to Jira tickets — here's the doc: docs.google.com/..."
Result: Reads the doc, shows a full preview of Initiatives/Epics/Stories, user edits and confirms, tickets created in Jira with parent-child links set.

### Example: Export OKRs as CSV for bulk import
User says: "Turn our OKRs into a backlog — I don't have a Jira project yet"
Result: Reads the doc, previews hierarchy, exports `~/okr-to-jira-export-<date>.csv` with correct Parent and Epic Link columns for Jira bulk import.

### Example: Multi-doc merge
User says: "Map OKRs to epics and stories — we have two planning docs"
Result: Reads both docs, merges duplicate Objectives into single Initiatives, combines all Key Results, shows unified preview before creating anything.

## Trigger Phrases

- "convert my OKRs to Jira tickets"
- "create tickets from OKR doc"
- "map OKRs to epics and stories"
- "turn our OKRs into a backlog"
- User runs `/okr-to-jira`

---

## Phase 0: Explain the Approach

Before asking for any input, explain the mapping:

> "Here's how I'll convert your OKRs into Jira tickets:
>
> - **Initiatives** (or Features) — one per Objective (the high-level qualitative goal)
> - **Epics** — one per Key Result, linked to its parent Initiative
> - **Stories** — created under an Epic when the Key Result or doc implies concrete implementation steps
>
> I'll read your scoping doc(s) from Google Doc URLs, show you a full preview of the ticket hierarchy, and get your confirmation before creating anything.
>
> You can then either provide a **Jira project key** to create tickets live, or choose **CSV export** to get a Jira-importable file (useful for external or non-Databricks Jira instances).
>
> Story points are **not added by default** — let me know if you'd like estimates included."

---

## Phase 1: Collect Inputs

Ask the user for one or more Google Doc URLs containing OKR scoping documents.

Use the `fe-google-tools:google-docs` skill to read each document. Example invocation:

```
Skill: fe-google-tools:google-docs
Task: Read the content of this Google Doc: <url>
```

If multiple URLs are provided, read all documents before proceeding. After reading, merge content and deduplicate Objectives that appear identical or near-identical across documents (see `references/okr-mapping-logic.md` for multi-doc handling).

---

## Phase 2: Extract & Analyze OKRs

Parse the document content to identify Objectives and Key Results. Refer to `references/okr-mapping-logic.md` for detailed parsing heuristics and document structure patterns.

For each Key Result, determine whether Sub-tasks are warranted:
- Generate Sub-tasks only when the doc or KR contains clear, imperative implementation steps
- Omit Sub-tasks when the KR is purely a metric with no inferable steps

If the OKR structure is ambiguous, show what you found and ask **one** targeted clarifying question before proceeding.

---

## Phase 3: Preview Ticket Hierarchy

Show the full proposed ticket details and get explicit confirmation before proceeding. For each ticket, display its type, title, description, and inferred parent link:

```
## Proposed Jira Ticket Hierarchy

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Initiative] <Objective 1 title>
  Description: <objective description>
  Labels: okr-import <user-labels>

  ┣━ [Epic] <Key Result 1.1 title>
  ┃    Description: <epic description>
  ┃    Parent: <Objective 1 title>
  ┃    Labels: okr-import <user-labels>
  ┃
  ┃    ┣━ [Story] <inferred step title>
  ┃    ┃    Parent: <Key Result 1.1 title>
  ┃    ┃    Labels: okr-import <user-labels>
  ┃    ┗━ [Story] <inferred step title>
  ┃         Parent: <Key Result 1.1 title>
  ┃         Labels: okr-import <user-labels>
  ┃
  ┗━ [Epic] <Key Result 1.2 title>
       Description: <epic description>
       Parent: <Objective 1 title>
       Labels: okr-import <user-labels>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Initiative] <Objective 2 title>
  ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Totals: X Initiatives · Y Epics · Z Stories

You can ask me to make changes before I create anything. Examples:
  • "Rename epic 1.2 to '...'"
  • "Update the description on initiative 2"
  • "Remove story 'X'"
  • "Add a story under epic 1.1: '...'"
  • "Merge epics 2.1 and 2.2"
  • "Split initiative 1 into two separate initiatives"

Type **"looks good"** (or similar) to proceed, or describe any changes.
```

**Edit loop:**
1. Apply any requested changes immediately.
2. Re-display the full updated preview after each round of edits.
3. Repeat until the user explicitly confirms (e.g., "looks good", "proceed", "create them", "yes").
4. Do not advance to Phase 3.5 until confirmation is received — not even if the user seems satisfied but hasn't explicitly confirmed.

---

## Phase 3.5: Labels

After the hierarchy is confirmed, ask:

> "Would you like to add any labels to your tickets? Labels help with filtering and searching in Jira.
>
> You can specify:
> - **Labels for all tickets** (e.g., `okr-2026-q2 team-platform`)
> - **Labels per level** — different labels for Initiatives, Epics, and Stories
> - Or skip labels entirely
>
> `okr-import` will always be added automatically."

Collect the user's response and resolve the final label sets:

- **Initiative labels**: user-provided initiative labels + `okr-import`
- **Epic labels**: user-provided epic labels + `okr-import`
- **Story labels**: user-provided story labels + `okr-import`

If the user provides a single flat list (e.g., "add `team-platform q2`"), apply those labels to all three levels. If the user specifies per-level labels, apply each to the appropriate level only. If the user skips, apply only `okr-import` to all levels.

---

## Phase 4: Choose Jira Destination

After confirming the hierarchy, ask:

> "How would you like to create these tickets?
>
> **Option A — Live Jira creation**: Provide a Jira project key (e.g., `PROJ`). I'll create Initiatives, Epics, and Stories directly in your Jira project using the REST API.
>
> **Option B — CSV export**: Choose this if you don't have a Jira project available yet, or if you're using an external Jira instance. I'll generate a Jira-importable CSV file."

---

## Phase 5a: Live Jira Creation

### Credentials Check

Check whether `~/.jira-credentials` exists:

```bash
cat ~/.jira-credentials 2>/dev/null
```

If the file does not exist, stop and show setup instructions:

```
To create Jira tickets, save your credentials first:

  cat > ~/.jira-credentials << 'EOF'
  email=you@databricks.com
  token=your-api-token
  base_url=https://databricks.atlassian.net
  EOF
  chmod 600 ~/.jira-credentials

Generate a Classic API token at: https://id.atlassian.com/manage-profile/security/api-tokens

The base_url field is optional and defaults to https://databricks.atlassian.net.
Set it to your company's Jira URL if you're not using Databricks Jira.
```

### Read Credentials

```bash
EMAIL=$(grep '^email=' ~/.jira-credentials | cut -d= -f2-)
TOKEN=$(grep '^token=' ~/.jira-credentials | cut -d= -f2-)
BASE_URL=$(grep '^base_url=' ~/.jira-credentials | cut -d= -f2-)
BASE_URL=${BASE_URL:-https://databricks.atlassian.net}
AUTH=$(echo -n "${EMAIL}:${TOKEN}" | base64)
```

### Create Initiatives

For each Objective, create an Initiative. The issue type name may be `Initiative` or `Feature` depending on the Jira configuration — check available issue types first if unsure:

```bash
curl -s \
  "${BASE_URL}/rest/api/2/issue/createmeta?projectKeys=<PROJECT_KEY>&expand=projects.issuetypes" \
  -H "Authorization: Basic ${AUTH}" \
  -H "Content-Type: application/json"
```

Then create the Initiative:

```bash
curl -s -X POST \
  "${BASE_URL}/rest/api/2/issue" \
  -H "Authorization: Basic ${AUTH}" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "project": {"key": "<PROJECT_KEY>"},
      "issuetype": {"name": "Initiative"},
      "summary": "<objective_text>",
      "description": "<objective_description>",
      "labels": ["okr-import", "<initiative_label_1>", "<initiative_label_2>"]
    }
  }'
```

Omit extra label entries if the user provided none beyond `okr-import`. Save the returned `key` (e.g., `PROJ-10`) for linking Epics.

### Create Epics

For each Key Result, create an Epic with `parent` set to the Initiative key to establish the hierarchy link:

```bash
curl -s -X POST \
  "${BASE_URL}/rest/api/2/issue" \
  -H "Authorization: Basic ${AUTH}" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "project": {"key": "<PROJECT_KEY>"},
      "issuetype": {"name": "Epic"},
      "summary": "<key_result_text>",
      "customfield_10011": "<key_result_text>",
      "description": "<description>",
      "parent": {"key": "<initiative_key>"},
      "labels": ["okr-import", "<epic_label_1>", "<epic_label_2>"]
    }
  }'
```

If the `parent` field is rejected (classic Jira projects that don't support hierarchy above Epic), retry without `parent` and note to the user that the Initiative→Epic link must be set manually in the roadmap view.

Save the returned `key` for linking Stories.

**Epic description format** (Jira wiki markup):
```
h2. Objective Context
<the parent Objective this KR contributes to>

h2. Key Result
<the measurable outcome>

h2. Acceptance Criteria
* <criterion 1>
* <criterion 2>
```

### Create Stories

For each inferred implementation step, create a Story with both `parent` (next-gen) and `customfield_10014` / Epic Link (classic) set to the parent Epic key:

```bash
curl -s -X POST \
  "${BASE_URL}/rest/api/2/issue" \
  -H "Authorization: Basic ${AUTH}" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "project": {"key": "<PROJECT_KEY>"},
      "issuetype": {"name": "Story"},
      "summary": "<step_text>",
      "parent": {"key": "<epic_key>"},
      "customfield_10014": "<epic_key>",
      "labels": ["okr-import", "<story_label_1>", "<story_label_2>"]
    }
  }'
```

`parent` covers next-gen/team-managed projects; `customfield_10014` covers classic projects. Jira will ignore whichever field doesn't apply to the project type.

**On any failure (non-2xx response):** print the full error body and stop. Do not silently skip tickets or continue after an error.

**Creation order:** Initiatives first → Epics → Stories. Never attempt to link a child before its parent exists.

---

## Phase 5b: CSV Export

Generate a Jira-importable CSV file. Refer to `references/jira-csv-format.md` for the full column spec, row ordering requirements, and import instructions.

**File path:** `~/okr-to-jira-export-<YYYY-MM-DD>.csv`

```python
import csv
import datetime

filename = f"okr-to-jira-export-{datetime.date.today()}.csv"
filepath = f"{os.path.expanduser('~')}/{filename}"

fieldnames = ["Issue Type", "Summary", "Description", "Epic Name", "Epic Link", "Parent", "Priority", "Labels"]

# Labels collected in Phase 3.5 — space-separated strings for Jira CSV import
initiative_labels = " ".join(initiative_label_set)  # e.g. "okr-import team-platform q2"
epic_labels = " ".join(epic_label_set)              # e.g. "okr-import team-platform q2"
story_labels = " ".join(story_label_set)            # e.g. "okr-import team-platform q2"

rows = []
# Add all Initiatives first
for obj in objectives:
    rows.append({
        "Issue Type": "Initiative",
        "Summary": obj.summary,
        "Description": obj.description,
        "Epic Name": "",
        "Epic Link": "",
        "Parent": "",
        "Priority": "Medium",
        "Labels": initiative_labels
    })
# Then all Epics
for kr in key_results:
    rows.append({
        "Issue Type": "Epic",
        "Summary": kr.summary,
        "Description": kr.description,
        "Epic Name": kr.summary,
        "Epic Link": "",
        "Parent": kr.parent_objective_summary,
        "Priority": "Medium",
        "Labels": epic_labels
    })
# Then all Stories
for task in stories:
    rows.append({
        "Issue Type": "Story",
        "Summary": task.summary,
        "Description": "",
        "Epic Name": "",
        "Epic Link": task.parent_kr_summary,   # classic Jira: links Story to Epic
        "Parent": task.parent_kr_summary,       # next-gen Jira: links Story to Epic
        "Priority": "Medium",
        "Labels": story_labels
    })

with open(filepath, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
```

After generating the file, print:

```
CSV exported to: ~/okr-to-jira-export-<date>.csv

To import into Jira:
1. Go to Jira → Settings (gear icon) → System → External System Import
2. Select "CSV"
3. Upload the file and map columns to your Jira fields
4. Set the target Project, review the preview, and click Import

Note: Map "Epic Name" and "Epic Link" to the custom fields in your Jira instance.
These field names may differ — look for fields labeled "Epic Name" and "Epic Link" in the column mapping step.
```

---

## Phase 6: Summary

### After Live Jira Creation

```
## OKR Tickets Created

Initiative: <Objective 1> [PROJ-10]
  Epic: <Key Result 1.1> [PROJ-11] → <base_url>/browse/PROJ-11
    Story: <step> [PROJ-12]
  Epic: <Key Result 1.2> [PROJ-13] → <base_url>/browse/PROJ-13

Initiative: <Objective 2> [PROJ-14]
  Epic: <Key Result 2.1> [PROJ-15] → <base_url>/browse/PROJ-15

Totals: X Initiatives | Y Epics | Z Stories
```

### After CSV Export

Print the file path, totals, and import instructions (as shown in Phase 5b).

---

## Notes

- **No story points by default.** Omit from both ticket creation and CSV unless the user explicitly requests them.
- **Labels.** Always include `okr-import` on every ticket. Additional labels are collected in Phase 3.5 — the user may specify a flat list (applied to all levels) or per-level labels (Initiatives, Epics, Stories independently).
- **Preview is mandatory.** Always show the full hierarchy and get confirmation before any writes.
- **Never delete or modify existing tickets.** Only create new tickets in the current session.
- **Track session tickets.** Keep a record of every ticket key created. Only edit tickets from the current session.
- **Stories are optional.** Only generate them when implementation steps are clearly inferable from the document. When in doubt, omit.
- **Initiative issue type.** The top-level issue type may be named `Initiative` or `Feature` depending on the Jira project configuration. Check available issue types via the createmeta API if the first attempt fails.
- **Error handling.** On any REST API failure, print the full error and stop. Do not continue creating tickets until the user resolves the issue.
- **Credentials file field `base_url`.** Defaults to `https://databricks.atlassian.net`. Read from credentials file to support non-Databricks Jira instances.
