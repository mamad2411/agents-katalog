---
name: find-research
description: "Search your team's user research library on Google Drive and surface relevant findings for a topic, question, or PRD. Reads configured Drive folders, identifies relevant studies, reads their reports, and outputs findings either as a quick reference or as a formatted PRD evidence block. Configurable per team — works with any research library structure (numbered subfolders or flat files, native Google docs or Office files). Use when writing a PRD, validating a problem statement, or checking what your team already knows about a topic before starting new research."
tool_integration: Google Workspace
---

# Find Research

## Prerequisite

**Google Workspace MCP must be connected before this skill can run.**

Silently attempt to list files from the primary research folder. If the call fails or returns an auth error, stop immediately and tell the user:

> "This skill requires Google Workspace MCP to access your research library. Connect the Google Workspace MCP integration and restart. Without it, the skill cannot run."

Do not proceed past this check if MCP is unavailable.

---

## Configuration

This skill reads its research library configuration from `~/.claude/configs/pm-skills-config.md` under the `## Research Library` section.

### On invocation, check the config

Try to read `~/.claude/configs/pm-skills-config.md`. Look for the `## Research Library` section.

**If the file exists and the section has at least one library with a Google Drive folder ID:** read all configured libraries (name, folder ID, structure, format, excluded subfolders, product areas, owner email) and use these values throughout the skill. Proceed to Phase 1.

**If the file is missing, the section is empty, or no folder ID is set:** run interactive setup before anything else.

### Interactive setup (first run)

Tell the user:

> "Looks like you have not configured your research library yet. I'll walk you through a quick setup — should take 30 seconds. I'll save your answers to `~/.claude/configs/pm-skills-config.md` so future runs reuse them automatically.
>
> 1. What is the name of your primary research library? (e.g. 'UX Research Drive')
> 2. What is its Google Drive folder ID? (the long string in the folder URL, e.g. `1abc...xyz`)
> 3. Is the library structured (reports live inside numbered subfolders like `1. Plan`, `2. Reports`) or flat (report files sit directly in each study folder)?
> 4. What file format dominates — native Google Docs/Slides, Office files (.docx/.pptx), or mixed?
> 5. Do you have a secondary library? If yes, repeat 1-4. If no, say `skip`.
> 6. Which email should I tell users to ask for access when a folder is inaccessible? (your work email is fine)
> 7. Any subfolder names to always skip during scanning? (admin/template/process folders — comma-separated, or `none`)
> 8. Comma-separated list of product areas/features your studies cover, for tagging findings (e.g. `onboarding, checkout, search`)"

After getting answers, write to `~/.claude/configs/pm-skills-config.md`:
- If the file does not exist, create it with the full template (use `config-template.md` from the plugin repo as the base — find it via the plugin install path or recreate from this skill's reference).
- If the file exists but the `## Research Library` section is missing or incomplete, write or update that section in place. Do not touch other sections.

Then proceed to Phase 1 using the answers just collected.

---

## Research Libraries to Scan

Use the libraries defined in the user's config. For each library, the skill needs:
- **Folder ID** — the Google Drive folder to scan
- **Structure** — `structured` (numbered subfolders inside study folders) or `flat` (files at study folder root) or `mixed`
- **Format** — `google-native` or `office` or `mixed`

If a configured folder returns "File not found" or permission error, note which one is inaccessible and continue with the others. Do not fail the skill. Tell the user:

> "Note: [library name] is not accessible with the current Google account. Results will only cover the accessible libraries. To fix this, ask the folder owner to share it with [owner email from config]."

---

## Phase 1 — Understand the Query

Accept `$ARGUMENTS` directly as the research topic or question.

If `$ARGUMENTS` is empty, ask one question:

> "What are you researching? A topic (e.g. 'onboarding drop-off', 'checkout abandonment', 'feature X adoption') or a specific question works. Also: is this for a PRD, or a quick reference lookup?"

The answer to the second part selects the output mode in Phase 4. Default to Quick Lookup if not specified.

---

## Phase 2 — Scan the Libraries (Metadata Only)

List the top-level contents of every configured library folder using `list_files`. Do not read any file content yet.

For each study folder found, score its name against the query on a simple 3-point scale:
- **Strong match** — the folder name directly names the topic (e.g. query: "onboarding", folder: "Onboarding Flow Optimization Study [Oct 2025]")
- **Possible match** — the folder name shares a product area or theme (e.g. query: "checkout", folder: "Cart Abandonment Research [Jan 2026]")
- **No match** — unrelated

Exclude the subfolders configured in the user's `Subfolders to exclude` list. These are admin, process, template, or non-study folders.

Tell the user what was found before reading anything:

> "Found [N] studies across [X] librar(y/ies). [N] look relevant to '[topic]':
> - [Study name] ([date]) — Strong match
> - [Study name] ([date]) — Possible match
>
> Reading their reports now…"

**Token guard:** If more than 5 studies match, list them all and ask:
> "Found [N] relevant studies — reading all of them will use significant context. Want me to read all [N], or narrow to the top 3 most relevant?"

Wait for confirmation before proceeding.

---

## Phase 3 — Navigate to Reports and Extract Findings

For each matched study, navigate to the report using the structure detection rules below. Then export and extract.

### Structure Detection

The user's config specifies whether each library is `structured`, `flat`, or `mixed`. Use that as the primary hint, but also detect from the actual folder contents — a single library can have inconsistent studies.

**Structured layout (numbered subfolders):**

After listing the study folder contents, if you see numbered subfolders (e.g. `1. Research Plan`, `2. Raw Data`, `3. Reports`):
1. Find the subfolder named `Reports`, `Final Reports`, `3. Reports`, or `5. Final Reports`
2. List its contents
3. Export the Google Doc or Slides file as `text/plain`

**Flat layout (files at root):**

If files appear directly in the study folder with no numbered subfolders:
1. Look for a file with "Insights", "Report", "Findings", or "Analysis" in the name
2. For Office files (`.docx`, `.pptx`) — prefer `.docx` over `.pptx` when both exist; text extraction is cleaner
3. Export using `export_file` with `mimeType: text/plain` — this works for both Office and native Google formats
4. Skip `.xlsx`, `.csv`, and `.pdf` files — these are raw data, not insights reports

### Extraction Rules

From each report, extract:
- **Study metadata:** name, date, method (survey / usability test / competitive / quantitative), sample size (N=) if stated
- **Key findings:** the 3–5 most concrete findings — state as facts, not summaries. Include numbers and percentages where present.
- **Direct quotes:** 1–2 user quotes that best illustrate the core finding, if available
- **Product areas tagged:** which features or journeys the study covers. Use the product areas configured in the user's config as the controlled vocabulary; tag any that apply.

**Do not read raw data folders** (`Survey Responses`, `Raw Data`, `Session Recordings`). Reports and Final Reports only.

**If a report is a Google Slides presentation:** export as `text/plain` and extract slide titles and body text. The structure is less clean than a Doc — focus on slide titles that name findings and any data callouts in the body.

---

## Phase 4 — Output

### Quick Lookup (default)

Use this when the PM wants a fast reference or is exploring what exists.

```
## Research findings: [topic]
Searched [N] studies across [X] librar(y/ies). [N] relevant.

---

**[Study Name]** | [Date] | [Method] | N=[n]
- [Finding — concrete, with number or data point if available]
- [Finding]
- [Finding]
> "[Direct quote if available]"
Source: [Drive link]

---

**[Next study]** | ...
```

### PRD Evidence Block

Use this when the PM says this is for a PRD.

```
## Research Evidence — [topic]

> Use this section in your PRD's Problem Statement or User Insights.
> Each block is one study. Edit the implication line to fit your specific initiative.

---

**[Study Name]** ([Date] | [Method] | N=[n])
**Key finding:** [1–2 sentence finding, grounded in data]
**Supporting data:** [specific stat, percentage, or quote]
**Implication:** [1 sentence on what this means for the PRD — keep it factual, not prescriptive]
[Drive link]

---
```

For the Implication line: write it as "This suggests [product area] has [specific gap/opportunity]" — not as a recommendation. Leave the PM to draw the conclusion.

---

## Quality Rules

- Never state a finding without a source study
- If a report is a Slides deck and the text extraction is ambiguous, note: "This study is a presentation — extracted from slide text, which may be incomplete"
- If sample size is not stated in the report, write N=unknown
- If no relevant studies are found: tell the user plainly and suggest which studies exist that are closest, in case they want to read a partial match
- Do not read more than 6 report files per run — flag if the query matches more and ask the user to narrow it

---

## Suggest Next Steps

After output, offer:

- "Want me to `/synthesize-research` across these findings to identify themes?"
- "Should I pull this into a PRD? Run `/create-prd [topic]` and reference this evidence."
- "Need more depth on one study? Tell me which one and I'll read the full report."
