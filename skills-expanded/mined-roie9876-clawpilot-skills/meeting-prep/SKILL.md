---
name: meeting-prep
description: "Build a share-ready meeting preparation brief from M365 calendar, email, and meeting data. Writes the prep brief to the customer repo with a git commit. Triggers include: 'meeting prep', 'prep for meeting', 'prepare for meeting', 'meeting brief', 'prep brief', 'get ready for my meeting', or any request to prepare context before a customer meeting."
---

# /meeting-prep — Meeting Preparation Brief

Build a comprehensive preparation brief before a customer meeting by aggregating
calendar context, prior meeting notes, email threads, open follow-ups, and
facilitator notes from Microsoft 365. Write the brief to the customer engagement
repo and commit it.

## Platform Compatibility

This skill runs on **macOS, Linux, and Windows**. Detect the OS before running shell commands and pick the right syntax. See `_shared/PLATFORM.md` (relative to the skills repo root) for the full translation table. Quick reference:

| Action | macOS / Linux (bash) | Windows (PowerShell) |
|--------|----------------------|----------------------|
| Make dir | `mkdir -p X` | `New-Item -ItemType Directory -Force -Path X` |
| List dir | `ls X` | `Get-ChildItem X` |
| Open file in Edge | `open -a "Microsoft Edge" file` | `Start-Process msedge.exe file` |
| Home dir | `~` or `$HOME` | `$HOME` |

Detect OS via `$IsWindows` (PowerShell) or `[ "$(uname)" = "Darwin" ]` / `[ "$(uname)" = "Linux" ]` (bash). Default to POSIX, fall back to PowerShell on Windows.

## Core Principles

- **Never fabricate context.** Only include information retrieved from M365 tools or the local customer repo. If a source is unavailable, say so explicitly in the brief.
- **Preserve source language.** Section headings are always English. Content (meeting body, email excerpts, notes, action items) stays in its original language — do not translate Hebrew to English or vice versa. Preserve Hebrew text as-is.
- **Graceful degradation.** Every data source can fail. The brief must still be useful even when some sources return nothing. Note what's missing so the user knows what to check manually.
- **Best-effort customer detection.** Use attendee email domains as the primary signal, then folder scanning, then meeting subject. Suggest when ambiguous, ask when unknown — never guess a customer name.
- **One brief per meeting.** Output is both `.html` (RTL, dark-theme, auto-opened in Edge) and `.md` (for git). Path is deterministic: `~/customer-engagements/{slug}/projects/{project}/meetings/{date}-{subject-slug}.*`. If files already exist, ask whether to overwrite or append.
- **Commit immediately.** After writing the brief, commit to git so it's versioned and findable.

## Prerequisite Auto-Install

Before running, verify all dependencies are present. **Install anything missing automatically.**

### Required Sibling Skills

This skill requires the following sibling skill from the same repository
(`https://github.com/roie9876/clawpilot-skills`):

| Skill | Purpose | Required? |
|-------|---------|-----------|
| `/customer-repo` | Customer engagement folder structure (`~/customer-engagements/`) | ✅ For storing prep briefs |

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

### Required Tools

| Tool | Check (POSIX) | Check (Windows) | Install (macOS) | Install (Windows) |
|------|---------------|-----------------|-----------------|-------------------|
| git | `git --version` | `Get-Command git` | Pre-installed | `winget install Git.Git` |

### M365 Sign-In

Check `m_m365_status`. If not signed in → call `m_m365_sign_in`.

---

## Step 1: Identify the Target Meeting

Ask the user which meeting to prepare for, or accept it from the prompt (e.g., "/meeting-prep Contoso sync tomorrow").

**If the user names a specific meeting:**
2. Match the user's description against event subjects (case-insensitive, partial match).
3. If multiple matches, present a numbered list and ask the user to pick.

**If the user says "my next meeting" or similar:**

1. Call `m365_list_events(limit: 5)` with default range (next 7 days).
2. Filter out all-day events and cancelled events.
3. Present the next upcoming event and confirm with the user.

**If no events are found:**

- Report: "No upcoming meetings found in the next 7 days. Try specifying a date range or meeting subject."
- Stop and wait for user input.

Once confirmed, call `m365_get_event(eventId)` to load the full event with attendees, body, and online meeting details.

## Step 2: Detect the Customer

Extract the customer from the meeting context using this priority chain:

1. **Attendee email domains** — From the event attendees, identify email domains that are NOT your organization's internal domain (configure your own internal domain, e.g. `@yourcompany.com`). External domains are the strongest customer signal.
2. **Folder scanning** — Run `ls ~/customer-engagements/` and match external domains or company names against existing folder names.
3. **Meeting subject** — Look for company names in the meeting subject line.
4. **User prompt** — If the user mentioned a customer name in their request, use that.

**Resolution rules:**

- If exactly one external domain matches a folder → use that customer.
- If multiple external domains → present the options and ask the user.
- If no external domain but the subject contains a known folder name → use that, confirm with the user.
- If no match at all → ask the user for the customer name.
- If the customer has no folder in `~/customer-engagements/` → offer to chain `/customer-repo` to scaffold one, then continue.

Set `{slug}` to the customer folder name (lowercase, hyphenated).

## Step 3: Detect/Select Project

Within the detected customer repo, identify which project this meeting relates to:

1. **List projects** — Run `ls ~/customer-engagements/{slug}/projects/` to enumerate project subfolders.
2. **Auto-select if only one project exists** — Use it without asking.
3. **Auto-match by meeting subject keywords** — Compare the meeting subject against project folder names using fuzzy, case-insensitive matching. Example: a meeting titled "SASE Architecture Review" matches a project folder named `sase`.
4. **If multiple projects and no auto-match** → Present a numbered list of projects and ask the user to pick.
5. **If no `projects/` directory or no project folders exist** → Offer to create one via `/customer-repo {customer}/{suggested-name}` (derive the suggested name from the meeting subject). If the user confirms, scaffold the project and continue. If the user declines, fall back to the customer-level folder.

Set `{project}` to the selected project folder name.

## Step 4: Gather Prior Context from Customer Repo

Read existing files from the customer engagement folder to build context:

1. **Prior meeting notes** — `ls ~/customer-engagements/{slug}/projects/{project}/meetings/` and read the 2-3 most recent files. Extract key decisions, open items, and follow-ups.
2. **Open follow-ups** — Check if `~/customer-engagements/{slug}/projects/{project}/followups.md` exists. Read and extract open items.
3. **Account context** — Check for `~/customer-engagements/{slug}/README.md` for background on the engagement (stakeholders, overall relationship, etc.).
4. **Project context** — Check for `~/customer-engagements/{slug}/projects/{project}/README.md` for project-specific scope, goals, and architecture context.

If any file is missing, skip silently — these are optional enrichments. If the project-level README.md is missing, note "Project README not found — project-specific context unavailable" in the brief.

## Step 5: Gather M365 Data

Run these tool calls to collect meeting intelligence. Each call has an explicit failure path — if a tool fails, note the gap in the brief and continue with remaining sources.

### 5a. Prior Email Threads

Search for recent emails involving the customer or meeting subject:

```
m365_search_emails(query: "{customer-name} OR {meeting-subject}", startDate: "{30-days-ago}", endDate: "{today}", limit: 10)
```

- Extract key topics, decisions, and open questions from the email threads.
- If the search fails or returns no results → note "Email context unavailable" in the brief.

### 5b. Prior Meeting Notes (Facilitator / Copilot)

If the meeting is recurring or has a prior occurrence, try to get facilitator notes from the last instance:

```
m365_get_facilitator_notes(joinUrl: "{prior-meeting-join-url}")
```

Or search by topic if no join URL:

```
m365_get_facilitator_notes(topic: "{meeting-subject}")
```

- Extract meeting notes and action items.
- If unavailable → note "Facilitator notes unavailable (requires organizer role + Microsoft 365 Copilot license)" in the brief.

### 5c. Prior Meeting Transcript

If a prior meeting had a Teams recording:

```
m365_get_transcript(joinUrl: "{prior-meeting-join-url}")
```

- Summarize key discussion points if the transcript is available.
- If unavailable → note "No transcript available for the prior meeting" in the brief.

### 5d. Attendee Lookup

For external attendees, enrich with organizational context:

```
m365_search_people(query: "{attendee-name-or-email}")
```

- Extract job title, department, and company for each attendee.
- If lookup fails for an attendee → list them with email only, no role.

## Step 6: Generate the Prep Brief

**Output format: RTL HTML** — The brief is generated as a self-contained `.html` file with `dir="rtl"` and dark-theme styling. This ensures mixed Hebrew/English content is properly right-aligned and renders beautifully in a browser.

Also write a `.md` version for git tracking and plain-text use.

### HTML Template

Use this HTML structure as the base. Populate sections with gathered data:

```html
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Meeting Prep: {subject}</title>
<style>
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
    max-width: 800px;
    margin: 40px auto;
    padding: 0 24px;
    background: #1e1e1e;
    color: #d4d4d4;
    line-height: 1.7;
    direction: rtl;
    text-align: right;
  }
  h1 { color: #569cd6; border-bottom: 2px solid #333; padding-bottom: 12px; font-size: 1.6em; }
  h2 { color: #4ec9b0; margin-top: 2em; border-bottom: 1px solid #333; padding-bottom: 6px; }
  strong { color: #dcdcaa; }
  code { background: #2d2d2d; padding: 2px 6px; border-radius: 3px; font-size: 0.9em; }
  table { border-collapse: collapse; width: 100%; margin: 12px 0; }
  th, td { border: 1px solid #444; padding: 8px 12px; text-align: right; }
  th { background: #2d2d2d; color: #9cdcfe; }
  ul, ol { padding-right: 24px; padding-left: 0; }
  li { margin-bottom: 6px; }
  .ltr { direction: ltr; text-align: left; }
  .meta { color: #9cdcfe; }
  .note { background: #2d2d30; border-right: 3px solid #569cd6; padding: 12px 16px; margin: 12px 0; border-radius: 4px; }
  .tag { display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 0.8em; margin-left: 6px; }
  .tag-pending { background: #4e4e21; color: #dcdcaa; }
  .tag-done { background: #1e3a1e; color: #4ec9b0; }
  hr { border: none; border-top: 1px solid #333; margin: 2em 0; }
  .footer { color: #666; font-size: 0.85em; font-style: italic; }
</style>
</head>
<body>
<!-- Populate sections: h1 title, metadata table (including Project row), attendees table,
     Prior Context (ul), Open Follow-ups (ul with .tag-pending spans),
     Facilitator Notes, Key Topics/Agenda (ol), Preparation Notes (ul with emoji prefixes),
     footer -->
</body>
</html>
```

**Key HTML patterns:**
- Meeting metadata → `<table>` with th/td rows (date, customer, project, partner, location, organizer)
- Attendees → `<table>` with columns: שם, אימייל, ארגון / תפקיד. Email cells get `class="ltr"`.
- Important notes → `<div class="note">` with right-border accent
- Open follow-ups → `<ul>` items with `<span class="tag tag-pending">ממתין</span>` prefix
- LTR content (emails, URLs, code) → wrap in `<span class="ltr">` or add `class="ltr"` to cell

### Markdown Template (secondary)

Also write a standard `.md` file with the same content for git tracking:

```markdown
# Meeting Prep: {subject}

**Date:** {date} {time} ({timezone})
**Customer:** {customer-name}
**Project:** {project}
**Attendees:**
- {name} ({email}) — {role/title, if known}

## Prior Context
{bullet points}

## Open Follow-ups
- [ ] {action item} — {owner} (from {source})

## Facilitator Notes (Previous Meeting)
{notes or unavailability notice}

## Key Topics / Agenda
{numbered list}

## Preparation Notes
{bullet points}

---
*Generated by /meeting-prep on {timestamp}*
```

### Content Language Rules

- All section headings → English (both in HTML and markdown).
- Content within sections → preserve the original language as-is.
- Action items → extract from both English and Hebrew text. Do not translate.
- Attendee names → preserve original form.

## Step 7: Write Files, Commit, and Open

1. **Compute the output paths:**
   ```
   ~/customer-engagements/{slug}/projects/{project}/meetings/{YYYY-MM-DD}-{subject-slug}.html   (primary — for viewing)
   ~/customer-engagements/{slug}/projects/{project}/meetings/{YYYY-MM-DD}-{subject-slug}.md     (secondary — for git)
   ```
   Where `{subject-slug}` is the meeting subject lowercased, spaces replaced with hyphens, special characters removed, truncated to 60 characters.

2. **Check if the file exists** — If either file exists, read it and ask the user:
   - "A prep brief already exists for this meeting. Overwrite, append, or skip?"

3. **Create the meetings directory if needed:**
   ```bash
   mkdir -p ~/customer-engagements/{slug}/projects/{project}/meetings
   ```

4. **Write both files** — the `.html` (RTL, dark-theme, styled) and `.md` (plain markdown).

5. **Commit to git:**
   ```bash
   cd ~/customer-engagements/{slug}
   git add projects/{project}/meetings/{YYYY-MM-DD}-{subject-slug}.html projects/{project}/meetings/{YYYY-MM-DD}-{subject-slug}.md
   git commit -m "meeting-prep: {customer-name}/{project} — {meeting-subject}"
   ```

   If the repo is not a git repo or the commit fails, inform the user but do not fail the skill — the brief is still written.

6. **Open the HTML brief in Microsoft Edge** (use the syntax matching the host OS):

   **macOS:**
   ```bash
   open -a "Microsoft Edge" "$HOME/customer-engagements/{slug}/projects/{project}/meetings/{YYYY-MM-DD}-{subject-slug}.html" 2>/dev/null \
     || open "$HOME/customer-engagements/{slug}/projects/{project}/meetings/{YYYY-MM-DD}-{subject-slug}.html"
   ```

   **Linux:**
   ```bash
   xdg-open "$HOME/customer-engagements/{slug}/projects/{project}/meetings/{YYYY-MM-DD}-{subject-slug}.html"
   ```

   **Windows (PowerShell):**
   ```powershell
   $brief = "$HOME/customer-engagements/{slug}/projects/{project}/meetings/{YYYY-MM-DD}-{subject-slug}.html"
   try { Start-Process msedge.exe $brief -ErrorAction Stop } catch { Invoke-Item $brief }
   ```

   If Edge is not installed, fall back to the OS default browser. Do not fail the skill if the open command fails — the brief is already written and committed.

## Error Handling

Every m365_* tool call can fail. Handle each failure individually so a single unavailable source doesn't block the entire brief.

| Tool Call | Failure Behavior |
|-----------|-----------------|
| `m365_list_events` returns no events | Report "No upcoming meetings found in the next 7 days." Stop and ask user for clarification. |
| `m365_get_event` fails | Report "Could not load meeting details for event {id}." Stop — cannot proceed without the base event. |
| `m365_search_emails` fails or returns empty | Note "Email context unavailable" in the Prior Context section. Continue. |
| `m365_get_facilitator_notes` fails | Note "Facilitator notes unavailable (requires organizer role + Copilot license)" in the brief. Continue. |
| `m365_get_transcript` fails | Note "No transcript available for the prior meeting" in the brief. Continue. |
| `m365_search_people` fails for an attendee | List the attendee with email only, no role/title. Continue. |
| Customer folder not found in `~/customer-engagements/` | Offer to run `/customer-repo` to scaffold the folder. If user declines, use a temp folder or ask where to write the brief. |
| No `projects/` directory found under customer folder | Offer to create the project structure via `/customer-repo {customer}/{suggested-name}`. If user declines, fall back to customer-level folder. |
| Multiple projects, no auto-match to meeting subject | Present a numbered list of projects and ask the user to pick. |
| Project `README.md` missing | Skip project-specific context. Note "Project README not found — project-specific context unavailable" in the brief. Continue. |
| `git commit` fails | Inform the user the brief was written but not committed. Do not fail the skill. |
| Meeting has no attendees | Skip customer detection from domains. Fall back to subject line and user prompt. |
| Meeting is cancelled | Warn the user: "This meeting is marked as cancelled. Proceed anyway?" |
