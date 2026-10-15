---
name: triage-ideas
description: "Process Obsidian Ideas.md inbox — route ideas to project roadmaps. NOT for direct roadmap edits or reviews."
user-invocable: true
---

# Triage Ideas — Obsidian Inbox to Project Roadmaps

Process the Ideas inbox — route each idea to the appropriate project roadmap.

**Obsidian CLI** (for read/search only — no edit command):
```bash
OBS="<path-to-obsidian-binary>"
# All commands need 2>&1 | grep -v "Loading\|out of date"
```

**Obsidian vault path**: `{{vault_path}}`
**Roadmap file**: `{{vault_path}}/{{project}}/Roadmap.md`
**Ideas file**: `{{vault_path}}/Ideas.md`

## Step 1 — Read the inbox

```bash
"$OBS" read path="Ideas.md" 2>&1 | grep -v "Loading\|out of date"
```

If the only content is the frontmatter and `# Ideas` header with no bullets, report "Ideas inbox is clear" and stop.

## Step 2 — Classify each idea

Analyze each idea and classify:
- **Project**: Which project does this belong to?
- **Type**: Roadmap item (future work), Todo (actionable now), or Feature request
- **Priority**: BLOCKING, CRITICAL, High, Medium, Low, or "When needed"
- **Effort**: Low, Medium, Large
- **Table**: Immediate Backlog (actionable items) or Long-Term Ideas (exploratory/future)

Use vault context to flesh out the idea (run searches in parallel):
```bash
"$OBS" search query="{relevant keywords}" limit=10 2>&1 | grep -v "Loading\|out of date"
```

Also read the roadmap to check for duplicates.

Present the triage plan to the user before executing:
```
| # | Idea | Project | Type | Priority | Effort | Table |
|---|------|---------|------|----------|--------|-------|
| 1 | ... | Project A | Roadmap | Medium | Low | Immediate |
| 2 | ... | Project A | Roadmap | Low | Medium | Long-Term |
```

Ask the user to confirm or adjust before proceeding.

## Step 3 — Route to ALL destinations

For each confirmed idea, update destinations:

### 3a. Obsidian Roadmap.md

Use the **Read tool** then **Edit tool** on the actual file path (NOT Obsidian CLI — it has no edit command):
- **Immediate Backlog items**: Insert new row in the Immediate table
- **Long-Term Ideas items**: Append to the Long-Term Ideas table

Row format:
```
| {Priority} | **{Title}** — {Description} | Ideas inbox {YYYY-MM-DD} | {Effort} |
```

### 3b. Database (if applicable)

If using a database for roadmap tracking (e.g., D1, SQLite), batch ALL ideas into a single SQL file to minimize round-trips:

```bash
cat > tmp-ideas.sql << 'EOSQL'
INSERT INTO roadmap_items (id, title, description, project, status, createdDate, createdBy, updatedAt, updatedBy, estimatedTime)
VALUES
('idea-xxx', 'Title 1', 'Description. Priority: Medium.', 'your-project', 'planned', 'YYYY-MM-DD', 'claude', 'YYYY-MM-DDTHH:MM:SSZ', 'claude', 'Medium'),
('idea-yyy', 'Title 2', 'Description. Priority: Low.', 'your-project', 'planned', 'YYYY-MM-DD', 'claude', 'YYYY-MM-DDTHH:MM:SSZ', 'claude', 'Large');
EOSQL

# Execute against your database(s)
# npx wrangler d1 execute your-db --remote --file=tmp-ideas.sql

rm tmp-ideas.sql
```

### 3c. Other project roadmaps

For items routed to other projects, use the Edit tool on:
`{{vault_path}}/{Project}/Roadmap.md`

If no Roadmap.md exists, create one with the Write tool:
```markdown
---
type: roadmap
last_updated: {today}
---

# {Project} — Roadmap

## Backlog

| Priority | Item | Notes | Effort |
|----------|------|-------|--------|

## Completed
```

## Step 4 — Clear the inbox

Use the **Read tool** then **Edit tool** on `{{vault_path}}/Ideas.md`.

Replace all idea content, leaving only:
```markdown
---
type: ideas
---
# Ideas

```

**IMPORTANT**: Do NOT use Obsidian CLI for editing — it doesn't support it. Always use Read + Edit tools on the actual file path.

## Step 5 — Report summary

```
## Ideas Triaged

Processed X ideas from inbox:
- → ProjectA/Roadmap.md (Immediate): "idea 1", "idea 2"
- → ProjectA/Roadmap.md (Long-Term): "idea 3"
- → ProjectB/Roadmap.md: "idea 4"
- Marked as already done: "idea 5"

Ideas inbox cleared.
```

## Gotchas

- **Obsidian CLI has NO edit command** — always use Read + Edit tools on full file paths
- **Batch database inserts** — combine all ideas into one SQL file, run against all environments
- **Database has no priority column** — encode priority in the description text if needed
- **Dedup check** — search the roadmap for similar items before adding duplicates
- **Immediate vs Long-Term** — actionable items with clear scope go to Immediate Backlog; exploratory/meta/tooling ideas go to Long-Term Ideas
- **Clean up tmp files** — always remove temp SQL files after execution
