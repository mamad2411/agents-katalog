---
name: obsidian-update
description: "End-of-session knowledge extraction into the MoxyWolf Obsidian vault. Scans the current Cowork conversation for durable knowledge — decisions made, research findings, meeting discussions, cross-project insights, action items, and new contacts — then writes properly formatted, cross-linked Markdown notes to the vault. Use this skill whenever Dorian says 'obsidian update', 'update the vault', 'save to obsidian', 'capture this session', 'write to the vault', 'vault update', 'end of session', 'save session knowledge', or any request to persist conversation knowledge into the Obsidian knowledge base. Also trigger when Dorian asks to 'log this decision', 'save this research', 'add this to the vault', or references the Obsidian vault in any write context. This skill should trigger aggressively for anything that involves writing durable knowledge to the vault."
---

# Obsidian Vault Update — Session Knowledge Extraction

You are capturing durable knowledge from the current Cowork session and writing it to the MoxyWolf Obsidian vault. The vault is the company's AI-readable knowledge layer — the connective tissue between projects, decisions, research, and operational knowledge.

The goal is not to dump a conversation log. It's to extract the **facts, decisions, and insights that will still matter next week** and place them where they'll be findable by both humans and future Claude sessions.

---

## Step 0: Locate and Load the Vault

The vault is located by checking in order:

1. **Cowork workspace mount**: Check if the current workspace folder (`/sessions/*/mnt/*/`) contains `CLAUDE.md` at root with MoxyWolf Vault markers. If yes, that IS the vault.
2. **Google Drive mount**: Check `/sessions/*/mnt/GoogleDrive-dorianc@moxywolf.com/Shared drives/MoxyWolf Shared Files/MoxyWolf Vault/`
3. **Google Drive REST API fallback**: Use the bundled `${CLAUDE_PLUGIN_ROOT}/scripts/drive_rest.py` helper. Team Drive ID: `0AHxJ5CazJqxOUk9PVA`. Requires the one-time service-account setup at `~/.config/moxywolf/drive-service-account.json` — see `references/scheduled-task-vm-setup.md`.
4. If none work: use `request_cowork_directory` to ask Dorian to mount the vault.

Once located, set `${VAULT}` to the resolved path.

**Load context for smarter extraction:**

1. Read `${VAULT}/CLAUDE.md` — vault conventions, project list, folder structure, frontmatter format, tagging system, linking rules. Follow them exactly.
2. Read `${VAULT}/_System/MEMORY.md` — active project states, relationships, shorthand decoder, and operational context. This makes extraction smarter by correctly attributing knowledge to projects and people.
3. Scan existing project index files in `${VAULT}/Projects/*/00-Hub/` to understand what's already captured. Prevents duplicates and enables cross-linking.

---

## Step 1: Scan the Session

Review the full conversation from this Cowork session. You have access to the conversation history — use it. Look for these categories of extractable knowledge:

### Knowledge Categories

| Category | What to look for | Vault note type | Template |
|----------|-----------------|-----------------|----------|
| **Decisions** | Choices made with reasoning — tech stack picks, strategy pivots, pricing changes, architecture decisions | Decision Record | `_Templates/Decision Record.md` |
| **Research Findings** | Web searches performed, sources consulted, facts learned, competitive intel gathered | Research Note | `_Templates/Research Note.md` |
| **Meeting-like Discussions** | Structured conversations about a specific topic with outcomes and action items | Meeting Note | `_Templates/Meeting Note.md` |
| **Cross-project Insights** | Patterns noticed across multiple projects, reusable learnings, "aha" moments | Insight | `_Templates/Insight.md` |
| **Compliance Findings** | STIG/CMMC/NIST findings, security observations, control mappings | Compliance Finding | `_Templates/Compliance Finding.md` |
| **Action Items** | Tasks committed to, follow-ups needed, deadlines mentioned | Appended to project index or Kanban board |
| **New People/Contacts** | Names, roles, companies, relationship context mentioned | People page | `People/` directory |
| **Council Deliberations** | Deliberation outcomes, model evaluations, verification results | Decision Record | Cross-linked to deliberation log |

### Extraction Rules

- **Be selective.** Not everything in a conversation is worth persisting. A quick factual Q&A? Probably not. A 20-minute exploration of vault architecture? Yes — that's a decision + research note.
- **Combine related items.** If the session had a long discussion about pricing strategy that included research, a decision, and action items — that's one rich note, not four thin ones.
- **Attribute to projects.** Every note should map to a project if possible. If cross-cutting, it goes to `_Shared Knowledge/`.
- **Capture the "why" not just the "what."** "We chose Supabase" is useless. "We chose Supabase over Firebase because of Row Level Security for multi-tenant compliance data" is a durable decision record.
- **Check for Council deliberation records.** If the session included a Council deliberation, check whether the deliberation-engine already wrote a decision record via its Step 8d vault sync. Look in `${VAULT}/_Shared Knowledge/Agents and Plugins/council-deliberation-log.md` for the deliberation ID. If already logged, create a reference link rather than a duplicate note.

### Action Item Detection

When extracting action items, also check if they should be added to the Kanban board:
- If the action item is concrete and has an owner (Dorian), create a task file in `${VAULT}/Tasks/` and add to `${VAULT}/Tasks/KANBAN_VIEW.md`
- Use priority inference: explicit deadline within 48h → P0, this week → P1, no deadline → P2/Backlog
- Present detected tasks for approval before writing

---

## Step 2: Draft the Extraction Plan

Before writing any files, present a summary to Dorian:

```
## Session Knowledge Extraction

I found [N] items worth capturing from this session:

1. **[Type]: [Title]** → `Projects/[Project]/[Subfolder]/[filename].md`
   _Brief description of what will be captured_

2. **[Type]: [Title]** → `_Shared Knowledge/[Area]/[filename].md`
   _Brief description_

[If action items detected:]
Plus [N] action items for the Kanban board — want me to add those too?

[If Council deliberation occurred in session:]
Note: Council deliberation [id] was [already logged / not yet logged] to the vault.

Shall I write these to the vault, or do you want to adjust anything?
```

Wait for confirmation before writing. Dorian might say "skip #3" or "actually that belongs in RegGenome not SAMS" or just "go for it."

---

## Step 2.5: Council Verification Gate (Optional)

After Dorian approves the extraction plan, and **before writing files**, optionally run a lightweight Council evaluation on the plan. This catches attribution errors, missing items, and ephemeral state that shouldn't be persisted.

**Activation conditions:**
- The Council deliberation-engine plugin is available (check for the Council plugin in workspace or remote-plugins)
- Dorian hasn't disabled the gate via `--no-council` flag or `/obsidian-update config council_gate false`
- The extraction plan has 3+ items (not worth the cost for trivial extractions)

**If conditions are not met:** Skip silently. Proceed to Step 3.

**Process:**

1. **Build the Council query.** Send to the deliberation-engine in `--fast` mode (skip peer review, collect + synthesize only, ~$0.04-0.06):

   ```
   Evaluate this knowledge extraction plan for an Obsidian vault. The vault organizes
   knowledge by projects, with decision records, research notes, and cross-cutting insights.

   SESSION TOPICS: [brief summary of what the session covered]

   EXTRACTION PLAN:
   [numbered list of items with types, titles, target paths, and descriptions]

   Evaluate on these dimensions:
   1. Attribution accuracy — are items placed in the correct project folders?
   2. Completeness — is anything significant from the session missing?
   3. Ephemeral filtering — are any items too transient to persist (debugging steps,
      temporary state, already-documented patterns)?
   4. Deduplication — would any of these duplicate knowledge that likely already exists
      in the vault?

   Return specific, actionable findings only. Skip items that look correct.
   ```

2. **Present Council findings to Dorian** alongside the original plan:

   ```
   ## Council Review of Extraction Plan

   The Council flagged:
   - [finding 1 — e.g., "Item #3 attributes to STIGViewer but the discussion was about RegGenome"]
   - [finding 2 — e.g., "Missing: the cross-LLM variance insight from the research discussion"]

   Suggested adjustments:
   - [adjustment 1 — e.g., "Re-attribute item #3 to Projects/RegGenome/11-Knowledge/"]
   - [adjustment 2 — e.g., "Add insight note about cross-LLM variance to _Shared Knowledge/"]

   Proceed with original plan, apply Council suggestions, or adjust manually?
   ```

3. **Process Dorian's response:**
   - "apply" / "go for it" / "yes" → Pass Council adjustments to memory-system Sub-operation C, which returns the adjusted extraction plan for Step 3
   - "skip" / "original" / "no" → Proceed with original plan unchanged
   - Manual adjustments → Apply Dorian's specific changes

**Cost note:** This gate adds ~$0.05 per vault update. The `--fast` flag keeps it to 5 API calls (collect from 4 models + synthesize, no peer review). Disable with `/obsidian-update --no-council` or `/obsidian-update config council_gate false`.

---

## Step 3: Write the Notes

For each approved item:

### 3a. Read the appropriate template
Read the matching template from `${VAULT}/_Templates/` to get the structure right.

### 3b. Generate the note content
Fill in the template with extracted content. Key rules from `CLAUDE.md`:

**Frontmatter** — every note gets this:
```yaml
---
title: "Note Title"
date: YYYY-MM-DD
project: project-name
type: meeting | decision | research | insight | reference
tags: [relevant, tags]
participants: [dorian, others-if-applicable]
status: draft | active
---
```

**File naming** — use kebab-case with dates:
- Decision records: `DR-XXX-short-description.md`
- Meeting notes: `meeting-project-topic-YYYY-MM-DD.md`
- Research notes: `research-topic-YYYY-MM-DD.md`
- Insights: `insight-short-description-YYYY-MM-DD.md`

**For decision record numbering**: Check the project's existing files to find the highest DR number and increment. If no DRs exist yet, start at DR-001.

### 3c. Cross-link aggressively
- Link to project index files: `[[Projects/SAMS/00-Hub/SAMS Index]]`
- Link to people: `[[People/Dorian Cougias]]`
- Link to related notes if they exist in the vault
- Link to compliance frameworks if referenced: `[[_Shared Knowledge/Compliance Frameworks/framework-name]]`
- If a finding applies to multiple projects, note that explicitly with links to each project's folder

### 3d. Write the file
Use the `Write` tool to create the file at the correct vault path. Do not overwrite existing files — if a filename collision occurs, append a sequence number.

**For Decision Records specifically**: before deciding the destination folder, read `references/dr-auto-routing.md` and apply Rules 1–4 in order. The reference supersedes any ad-hoc placement in the rest of this SKILL — it picks the destination by topic class, appends one row to the Company Decision Log master index at `_Shared Knowledge/Operating Norms/_INDEX.md`, updates the project hub's `<P> Decisions.md` when project-scoped, and handles supersedes/superseded-by linking and Council verification flags.

### 3e. Update MEMORY.md if warranted
If the session produced significant new context (new contacts, project state changes, decisions), also update `${VAULT}/_System/MEMORY.md` with the relevant facts. This keeps the personal-os memory layer current without waiting for the nightly extraction.

### 3f. Cross-link Council deliberation records
If the session included a Council deliberation:
- Check `${VAULT}/_Shared Knowledge/Agents and Plugins/council-deliberation-log.md` for the deliberation ID
- If the deliberation was already logged by deliberation-engine Step 8d, add a wikilink to the relevant vault note: `Evaluated by: [[_Shared Knowledge/Agents and Plugins/council-deliberation-log|Council Deliberation {id}]]`
- If the deliberation-engine also created a decision record for this deliberation, link to that too: `See also: [[_Shared Knowledge/Agents and Plugins/council-decision-{slug}|Council Decision Record]]` or the project-specific path if it was attributed to a project
- If the deliberation was NOT already logged (e.g., vault wasn't available during the deliberation), capture the outcome as part of the session's decision record rather than creating a separate Council note

---

## Step 4: Update Project Indices (if warranted)

If the session produced significant knowledge for a project, consider updating that project's index file (`${VAULT}/Projects/[Name]/00-Hub/[Project] Index.md`):

- Add to the "Recent Activity" section with a date and link to the new note
- Update the "Status" section if the project phase changed
- Add to "Open Questions" if new unknowns surfaced
- Update "Key Decisions" with links to new decision records

Use the `Edit` tool for index updates — don't rewrite the whole file.

---

## Step 5: Report What Was Written

After writing all files, give Dorian a clean summary:

```
## Vault Updated

Written [N] notes to the MoxyWolf Vault:

- ✅ `Projects/SAMS/06-Engineering/DR-003-chose-obsidian-over-notion.md`
  Decision record: Why we chose Obsidian as the knowledge layer

- ✅ `_Shared Knowledge/Agents and Plugins/research-obsidian-claude-integration-2026-03-20.md`
  Research findings: Obsidian + Claude ecosystem analysis

Updated indices:
- 📝 `Projects/SAMS/00-Hub/SAMS Index.md` — added recent activity

Cross-links created: 4 inter-note links, 2 project references

[If MEMORY.md updated:]
Memory updated: added [N] new facts to _System/MEMORY.md

[If tasks added:]
Kanban updated: added [N] tasks to Tasks/KANBAN_VIEW.md

[If Council gate was used:]
Council review: accepted [N] suggestions, rejected [M] (cost: $X.XX)

[If Council deliberation records were cross-linked:]
Council links: [N] notes linked to deliberation log
```

Keep it factual and scannable. Dorian can go look at the files in Obsidian if he wants the detail.

---

## Edge Cases

**Session had no extractable knowledge**: This happens — maybe it was a quick question or casual chat. Say so honestly: "This session didn't produce knowledge worth persisting to the vault. Nothing to extract." Don't manufacture notes.

**Can't determine which project**: Put it in `_Shared Knowledge/` with appropriate subfolder. Cross-cutting knowledge is valuable too.

**Session produced a file (doc, spreadsheet, presentation)**: Don't duplicate the file into the vault. Instead, create a reference note that describes what was created, why, and where the actual file lives.

**Dorian asks to capture something specific**: If he says "save this research to the vault" mid-session (not at end-of-session), write just that item immediately. Don't wait for the full extraction pass.

**Very large sessions**: If the session was long and dense, prioritize. The top 5-7 most durable knowledge items are better than 20 thin ones. Note at the bottom "Additional topics discussed but not captured: X, Y, Z" for potential expansion.

**Session included a Council deliberation**: Check whether the deliberation-engine already wrote a decision record to the vault via its Step 8d vault sync. Look for the deliberation ID in `${VAULT}/_Shared Knowledge/Agents and Plugins/council-deliberation-log.md`. If already logged, create a reference link in your notes (Step 3f) rather than a duplicate. If not logged (vault was unavailable during the deliberation), capture the deliberation outcome as part of the session's decision record — include the query, chairman, key findings, and what was accepted/rejected.

---

## Reference: Vault Location Quick Guide

| Content Type | Vault Path |
|-------------|-----------|
| Project decisions | `Projects/[Name]/[##-Category]/DR-XXX-*.md` |
| Project research | `Projects/[Name]/11-Knowledge/*.md` |
| Project meetings | `Projects/[Name]/00-Hub/meeting-*.md` |
| Sprint notes | `Projects/[Name]/04-Sprints/*.md` |
| Compliance findings | `Projects/[Name]/07-Compliance/*.md` |
| Engineering decisions | `Projects/[Name]/06-Engineering/*.md` |
| GTM/marketing | `Projects/[Name]/08-GTM/*.md` or `12-MARCOM/*.md` |
| Cross-project insights | `_Shared Knowledge/[relevant area]/*.md` |
| Tech stack decisions | `_Shared Knowledge/Tech Stack/*.md` |
| Agent/plugin knowledge | `_Shared Knowledge/Agents and Plugins/*.md` |
| Council deliberation logs | `_Shared Knowledge/Agents and Plugins/council-deliberation-log.md` |
| Council model performance | `_Shared Knowledge/Agents and Plugins/council-model-performance.md` |
| Council routing intelligence | `_Shared Knowledge/Agents and Plugins/council-routing-intelligence.md` |
| People/contacts | `People/[Full Name].md` |
| Daily standups | `Daily Journal/YYYY-MM-DD.md` |
| System memory | `_System/MEMORY.md` |
| System identity | `_System/IDENTITY.md` |
| Task files | `Tasks/*.md` |
| Kanban board | `Tasks/KANBAN_VIEW.md` |

## Composio fallback — apps with no native MCP

If a step in this skill needs an app or service that has no native Cowork MCP connector — for example Notion, Linear, Jira, HubSpot, Salesforce, Stripe, Airtable, or Calendly — and the Composio connector is installed, reach the app through Composio's Tool Router rather than giving up or asking the user to do it by hand. Discover the tool with `COMPOSIO_SEARCH_TOOLS`, authenticate with `COMPOSIO_MANAGE_CONNECTIONS` if needed, then execute. See the `composio` plugin's `composio-tools` skill for the full pattern.

Native MCP connectors still come first — this is a fallback for reach, not a replacement for the native paths this skill already uses.
