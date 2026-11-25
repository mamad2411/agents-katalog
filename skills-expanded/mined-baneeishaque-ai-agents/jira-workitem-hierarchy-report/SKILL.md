---
name: jira-workitem-hierarchy-report
description: "Given a JQL query, fetch matching Jira work items with full metadata (type, parent, subtasks), build a parent-child hierarchy tree, and output a markdown report with clickable links and per-type tables — splitting dev subtasks from testing/QA items."
category: Atlassian Jira
---

# Jira Work Item Hierarchy Report Skill

> **Skill ID:** `jira-workitem-hierarchy-report`

Generate a markdown hierarchy report from a Jira JQL query. The report includes a visual tree with clickable links, summary tables grouped by issue type, and a separate "Testing Subtasks" section for items not owned by development.

---

## Environment & Dependencies

| Tool | Verification | Installation |
| :--- | :--- | :--- |
| `acli` | `which acli` | `brew install acli` or `npm install -g @atlassian/cli` |
| `python3` | `python3 --version` (3.10+) | Bundled with macOS / via `brew` |
| `acli` auth | `acli jira auth status` | See [`jira-acli-operations`](../jira-acli-operations/SKILL.md) §2.1 |

---

## Script

[`scripts/jira-hierarchy-report.py`](scripts/jira-hierarchy-report.py) — Python script that accepts a JQL query and outputs a markdown report.

### Usage

```bash
# Print to stdout
python3 .agents/skills/jira-workitem-hierarchy-report/scripts/jira-hierarchy-report.py \
  --jql 'project = AES AND status = "In Progress"'

# Write to file
python3 .agents/skills/jira-workitem-hierarchy-report/scripts/jira-hierarchy-report.py \
  --jql 'summary ~ "system memory"' \
  --output docs/jira-system-memory-work-items.md

# Custom base URL
python3 .agents/skills/jira-workitem-hierarchy-report/scripts/jira-hierarchy-report.py \
  --jql 'key = AES-53' \
  --base-url 'https://my-org.atlassian.net/browse'
```

### Arguments

| Flag | Required | Description |
| :--- | :--- | :--- |
| `--jql` | Yes | JQL query (wrap in single quotes) |
| `--output` | No | File path to write markdown report (default: stdout) |
| `--base-url` | No | Jira base URL for browse links (default: `https://ompventure.atlassian.net/browse`) |

---

## Operational Logic

### Step 1: Authenticate

Verify `acli` is authenticated:

```bash
acli jira auth status
```

Expected: `✓ Authenticated` with the site name.

> **Note:** `acli jira workitem list --max 1` does NOT exist in current acli
> versions — the auth check above is the reliable form.

If not authenticated, run:

```bash
acli jira auth login --web
```

See [`jira-acli-operations`](../jira-acli-operations/SKILL.md) §2.1 for full auth options.

### Step 2: Run the Script

```bash
python3 scripts/jira-hierarchy-report.py --jql '<YOUR_JQL>' --output <path>
```

> **Epic children JQL:** use `parent = <epic-key>` (e.g. `parent = AES-415`).
> The `"Epic Link"` custom field does NOT exist on this site — `acli` JQL
> search fails with *"field 'epic link' does not exist"*. The script passes
> `--limit 1000` to the search so epics with many children are not silently
> truncated (acli defaults to 30 results).

The script will:

1. **Search** — run `acli jira workitem search --jql "<jql>" --json`
2. **Fetch metadata** — for each result, run `acli jira workitem view <key> --fields '*all' --json` to get type, parent, subtasks
3. **Build tree** — identify the epic (if any), group stories/tasks under it, nest subtasks under their parent
4. **Render markdown** — produce a report with a visual hierarchy tree, summary table, and per-type detail tables

### Step 3: Understand the Output

The report has four sections:

- **Hierarchy** — a `<pre>` block with box-drawing characters and clickable HTML links
- **Summary** — count of items per type (Epic, Story, Task, Subtask)
- **Story/Task tables** — detail tables with key, summary, status
- **Subtask tables** — split into "Dev Subtasks" and "Testing Subtasks — not dev responsibility"

### Classification Rules

A subtask is classified as **testing/QA** (not dev responsibility) if its summary contains `test` or `qa` (case-insensitive). All other subtasks are classified as **dev subtasks**.

---

## SSOT Compliance

| Standard | Location |
| :--- | :--- |
| `acli` CLI operations | [`jira-acli-operations`](../jira-acli-operations/SKILL.md) |
| Markdown generation | [`markdown-generation`](../markdown-generation/SKILL.md) |
| Skill metadata structure | [`skill-factory`](../skill-factory/SKILL.md) |

---

## Related Skills

- [`jira-acli-operations`](../jira-acli-operations/SKILL.md) — base skill documenting all `acli jira` commands (search, view, create, edit, etc.)
- [`jira-automation-rules`](../jira-automation-rules/SKILL.md) — building and debugging Jira Cloud native automation rules

---

## Related Conversations & Traceability

| Session | Date | Context |
| :--- | :--- | :--- |
| Jira system memory work items | 2026-06-09 | Extracted hierarchy of 13 items under AES-53 epic, identified testing vs dev subtasks |
