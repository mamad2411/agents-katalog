---
name: connect
description: "Prepare and fill your Microsoft 1:1 Connect with your manager. Reads past Connect history for tone, gathers accomplishments from M365 (emails, meetings, Teams), discovers optional data sources (CRM, Kanban, customer repos), drafts content, and fills the form on v2.msconnect.microsoft.com via browser automation. You review and submit. Triggers include: 'connect', 'prepare connect', 'fill connect', 'manager connect', '1:1 connect', 'performance review', 'write my connect', or any request to prepare the semi-annual Connect check-in."
---

# /connect — Microsoft 1:1 Manager Connect

Prepare and fill your semi-annual Microsoft Connect (employee-manager check-in) on
v2.msconnect.microsoft.com. The skill auto-discovers your profile, gathers
accomplishments from M365 and any available local tools, reads your past Connects
for tone and style, drafts all sections, and fills the form via browser. You review
and submit.

**This skill is generic** — any Microsoft employee running Clawpilot can use it.
No hardcoded names, paths, or roles. Everything is discovered at runtime.

## Platform Compatibility

This skill runs on **macOS, Linux, and Windows**. Detect the OS first and pick the right syntax. See `_shared/PLATFORM.md` (skills repo root) for the full reference.

| Action | macOS / Linux (bash) | Windows (PowerShell) |
|--------|----------------------|----------------------|
| List dir | `ls $HOME/customer-engagements/` | `Get-ChildItem $HOME/customer-engagements/` |
| Run node script | `node $HOME/path/run-tool.mjs ...` | `node $HOME/path/run-tool.mjs ...` (same) |
| HTTP GET | `curl -s --max-time 3 http://...` | `Invoke-RestMethod -Uri http://... -TimeoutSec 3` |
| Find executable | `which node` | `Get-Command node` |
| Home dir | `~` or `$HOME` | `$HOME` |

Default to POSIX commands; use PowerShell on Windows native (not WSL/Git Bash).

## Core Principles

- **Never fabricate accomplishments.** Only include information retrieved from real data sources. If a source is unavailable, note the gap — do not invent achievements.
- **Preserve source language.** Section headings follow the Connect form's English. Content (meeting notes, email excerpts, CRM descriptions) stays in its original language — do not translate.
- **Match the user's voice.** Read past Connects to learn the user's writing style, tone, and level of detail. The draft should sound like the user wrote it, not like an AI.
- **Graceful degradation.** Every data source can fail independently. The draft must still be useful even when some sources return nothing. Core sources (M365 calendar + email) are always available. Everything else is optional enrichment.
- **Never submit.** Fill the form and stop. The user always reviews and submits manually.
- **Default lookback: 6 months.** The reflection period defaults to the last 6 months from today. The user can override with a custom date range (e.g., "/connect from 2025-06-01 to 2025-11-30").

## URLs

| Page | URL |
|------|-----|
| Dashboard | `https://msconnect.microsoft.com/` |
| View History | `https://msconnect.microsoft.com/viewhistory/` |
| Current Connect (v2) | `https://v2.msconnect.microsoft.com/` |
| Past Connect (v2) | `https://v2.msconnect.microsoft.com/historygsmorag?connectid={id}&pernr={pernr}` |
| View Feedback | `https://msconnect.microsoft.com/perspective/view` |

## Connect Form Structure (v2 — 4 questions)

The current Connect form has these sections:

### Section 1: Reflect on the past
**Question:** "What results did you deliver, and how did you do it?"
- Covers both WHAT (results/impact) and HOW (behaviors/collaboration)
- Rich text editor — supports bold, bullets, paragraphs

### Section 2: Reflect on recent setbacks
**Question:** "Reflect on recent setbacks - what did you learn and how did you grow?"
- Growth mindset reflection
- Rich text editor

### Section 3: Plan for the future
**Question:** "What are your goals for the upcoming period?"
- Multiple numbered goals (Goal #1 through #N), each with a title and description
- Goals may carry over from the previous Connect with "Modified" labels
- Rich text editor per goal

### Section 4: Conversation starters (optional)
**Question:** "Choose any of these optional prompts to continue great conversations with your manager."
- Brief 1-15 word responses
- Skip this section unless the user asks for it

### Status lifecycle
Draft → In Review → Posted

**Important:** Only Draft status Connects are editable. If the current Connect is "In review" or "Posted", inform the user and offer to draft content to a file instead.

---

## Prerequisite Auto-Install

Before running, verify all dependencies are present. **Install anything missing automatically.**

### Optional Sibling Skills

This skill can optionally enrich content from sibling skills in the same repository
(`https://github.com/roie9876/clawpilot-skills`). None are strictly required — the
skill degrades gracefully if they are absent.

| Skill | Purpose | Required? |
|-------|---------|-----------|
| `/customer-repo` | Customer engagement repos with meeting notes, follow-ups, decisions | ⚠️ Optional enrichment |
| `/msx-crm` | CRM data — opportunities, milestones, customer wins | ⚠️ Optional enrichment |

Check if optional skills are installed:

```bash
# macOS / Linux
for skill in customer-repo msx-crm; do
  [ -f "$HOME/.copilot/skills/$skill/SKILL.md" ] && echo "✅ $skill" || echo "⚠️ $skill not installed (optional)"
done
```

```powershell
# Windows
foreach ($skill in @('customer-repo','msx-crm')) {
    if (Test-Path "$HOME\.copilot\skills\$skill\SKILL.md") { "✅ $skill" } else { "⚠️ $skill not installed (optional)" }
}
```

**If any optional skills are missing and you want the full experience**, install all skills:

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

If the user declines or skills remain uninstalled, proceed without them — the skill
will note which enrichment sources were unavailable.

### M365 Sign-In

Check `m_m365_status`. If not signed in → call `m_m365_sign_in`.

---

## Step 0: First-Run Profile Discovery

On first invocation, the skill must discover who the user is. Check `m_recall("connect profile")` for a cached profile. If not found, build it:

### 0a. Get M365 profile

```
m365_get_my_profile()   → name, email, job title, department, office
m365_get_my_manager()   → manager name, email, title
```

### 0b. Get Connect-specific identifiers from the dashboard

Navigate to the MS Connect dashboard and extract:

```javascript
// From the dashboard page at https://msconnect.microsoft.com/
// Extract: display name, alias, role title, manager name, pernr (from history links)
```

The `pernr` (personnel number) is embedded in the history link URLs as a query parameter. Extract it from any Connect history link:
```javascript
Array.from(document.querySelectorAll('a'))
  .filter(a => a.href.includes('pernr='))
  .map(a => new URL(a.href).searchParams.get('pernr'))[0]
```

### 0c. Cache the profile

Store the discovered profile using `m_remember`:

```
m_remember(category: "context", fact: "Connect profile: {name}, {role}, manager: {manager_name} ({manager_email}), pernr: {pernr}")
```

On subsequent runs, recall this instead of re-discovering:
```
m_recall(query: "connect profile")
```

### 0d. Discover optional data sources

Probe for optional enrichment sources. Each probe is silent — if it fails, the source is simply skipped.

| Source | Probe | What it provides |
|--------|-------|-----------------|
| Customer engagement repos | `ls ~/customer-engagements/ 2>/dev/null` | Meeting notes, follow-ups, decisions, project context |
| CRM / MSX tool | `ls ~/.copilot/skills/msx-crm/crm-tools/run-tool.mjs 2>/dev/null` | Opportunities, milestones, customer wins |
| Kanban board | `curl -s --max-time 2 http://localhost:3456/api/health 2>/dev/null` | Completed tasks, work evidence |
| Browser-harness | `which browser-harness 2>/dev/null || ls ~/.local/bin/browser-harness 2>/dev/null` | Direct browser automation (preferred) |

If browser-harness is not available, fall back to Playwright MCP tools (`playwright-browser_*`).

Store discovered sources:
```
m_remember(category: "context", fact: "Connect data sources available: {list of discovered sources}")
```

---

## Step 1: Read Past Connect History

Use the browser to read the user's past Connect for style reference.

### Browser tool selection

Use whichever browser tool is available:
- **If browser-harness exists:** Use `goto()`, `wait_for_load()`, `js()`, `screenshot()` from browser-harness
- **If not:** Use Playwright MCP tools: `playwright-browser_navigate`, `playwright-browser_snapshot`, `playwright-browser_evaluate`, `playwright-browser_take_screenshot`

### Procedure

1. **Navigate to history page:** `https://msconnect.microsoft.com/viewhistory/`

2. **Extract history links:**
   ```javascript
   Array.from(document.querySelectorAll('a'))
     .filter(a => a.href.includes('v2.msconnect'))
     .map(a => ({ text: a.textContent.trim(), href: a.href }))
   ```

3. **Read the most recent past Connect** — Navigate to the most recent history link and extract the full content:
   ```javascript
   // Extract all section headings and content
   var sections = document.querySelectorAll('h2, p, li, div.display-item');
   Array.from(sections).map(e => e.tagName + ': ' + e.textContent.trim().substring(0, 300))
     .filter(t => t.length > 5).join('\n')
   ```

4. **Store the past content** — Save the extracted text to use as style/tone reference when drafting. Pay attention to:
   - How achievements are phrased (bullet points vs. paragraphs)
   - Level of specificity (metrics, customer names, project names)
   - Use of bold for emphasis
   - Balance of WHAT (results) vs. HOW (behaviors)
   - How setbacks/learnings are framed (growth mindset language)
   - Goal structure (title + description pattern)

## Step 2: Check Current Connect Status

1. **Navigate to current Connect:** `https://v2.msconnect.microsoft.com/`

2. **Check status** — Look for the status indicator at the top of the page (Draft / In review / Posted).

3. **If not Draft:**
   - Inform the user: "Your current Connect is '{status}'. It's not editable."
   - Offer to draft the content as a markdown file instead, which the user can paste manually later.
   - If the user agrees, skip to Step 5 and output to file instead of browser.

4. **If Draft:** Read any existing content already filled in (the user may have started).

5. **Extract the reflection period dates** from the Connect header (e.g., "Reflection Period: Nov 11, 2024 - May 4, 2025"). Use these as the lookback window instead of the default 6 months.

## Step 3: Gather Accomplishment Data

Run these data collection steps in parallel where possible. Each source is independent — if one fails, continue with the rest.

### 3a. Calendar — Key Meetings & Engagements (CORE — always available)

```
m365_list_events(startDate: "{period_start}", endDate: "{period_end}", limit: 50)
```

- Identify recurring customer engagements, architecture sessions, POCs, hackathons
- Group by customer/theme
- Note significant one-off events (executive briefings, partner meetings, team offsites)
- If the API limits results, paginate or narrow by month

### 3b. Email — Customer Interactions & Milestones (CORE — always available)

```
m365_search_emails(query: "architecture OR POC OR migration OR deployment OR pilot OR delivered OR launched", startDate: "{period_start}", endDate: "{period_end}", limit: 20)
```

Also search for:
- Sent emails (folder: "sent") for deliverables and outbound communication
- Key project milestone keywords relevant to the user's role

Extract: customer names, project milestones, key decisions, deliverables sent.

### 3c. Teams Messages — Key Discussions (CORE — always available)

Search for significant contributions in Teams channels:

```
m365_search_chats(query: "architecture OR POC OR customer OR demo OR delivered", limit: 20)
```

Look for: knowledge sharing, helping colleagues, cross-team collaboration evidence.

### 3d. Feedback Received (CORE — always available)

Navigate to the MS Connect feedback page:
```
https://msconnect.microsoft.com/perspective/view
```

Extract any feedback received during the period — useful for both "Reflect" and "Setbacks" sections.

### 3e. Customer Engagement Repos (OPTIONAL — skip if not found)

Only if `~/customer-engagements/` exists:

```bash
# macOS / Linux / WSL / Git Bash
ls "$HOME/customer-engagements/" 2>/dev/null
```

```powershell
# Windows PowerShell
Get-ChildItem -Path "$HOME/customer-engagements/" -ErrorAction SilentlyContinue
```

For each customer with a repo:
- Read `README.md` for engagement context
- List projects under `projects/`
- Read recent meeting notes from `meetings/`
- Check `followups.md` for completed items (evidence of delivery)
- Check `decisions/` for architectural decisions made

### 3f. CRM / MSX Data (OPTIONAL — skip if tool not found)

Only if the CRM tool exists at `~/.copilot/skills/msx-crm/crm-tools/run-tool.mjs`:

```bash
node ~/.copilot/skills/msx-crm/crm-tools/run-tool.mjs list-milestones --status active
node ~/.copilot/skills/msx-crm/crm-tools/run-tool.mjs list-opportunities
```

Extract: deals progressed, milestones achieved, customer wins, pipeline contribution.

### 3g. Kanban Board — Completed Tasks (OPTIONAL — skip if server not running)

Only if the Kanban server responds at `localhost:3456`:

```bash
# macOS / Linux / WSL / Git Bash
curl -s --max-time 3 http://localhost:3456/api/tasks | jq '[.[] | select(.status == "done")]'
```

```powershell
# Windows PowerShell
try { Invoke-RestMethod -Uri http://localhost:3456/api/tasks -TimeoutSec 3 | Where-Object { $_.status -eq 'done' } } catch { }
```

Extract: completed tasks with their descriptions and dates — evidence of execution.

## Step 4: Draft the Content

Using the gathered data and the past Connect as style reference, draft each section.

### Section 1: Reflect on the past

Structure the reflection as:
1. **Opening paragraph** — High-level summary of role and key impact theme (1-2 sentences). Use the user's job title from their profile.
2. **Key achievements** — Bullet points with bold lead-ins, each covering:
   - WHAT was delivered (specific result, customer, project)
   - HOW it was done (collaboration, innovation, technical depth)
3. **Closing paragraph** — Broader impact or role evolution narrative

**Style guidelines (adapt based on past Connect analysis):**
- Use bold for key phrases/achievements
- Be specific: name customers, projects, technologies
- Balance technical depth with business impact
- Show cross-team collaboration
- 200-400 words typical length

### Section 2: Reflect on recent setbacks

Structure as:
1. **Challenge faced** — Honest description of a difficulty or gap
2. **Learning/growth** — What was learned and how it changed approach
3. **Bold key insight** — One-line takeaway in bold

**Guidelines:**
- Frame setbacks through a growth mindset lens
- Connect the learning to a concrete action or change
- Keep it authentic — not everything needs to be a hidden strength
- 50-150 words typical length

### Section 3: Plan for the future (goal tweaks)

For each existing goal in the current Connect:
1. Read the current goal title and description
2. Based on gathered data, suggest specific tweaks:
   - Update descriptions to reflect current priorities
   - Add new customer engagements or projects as examples
   - Adjust targets based on what's been achieved
3. If a goal is no longer relevant, flag it for the user

If new goals are needed (based on current work patterns), suggest them.

**Guidelines:**
- Keep goal titles concise and measurable
- Descriptions should have 3-5 bullet points
- Include specific customer names, technologies, certifications
- Align with the user's role and team priorities

## Step 5: Fill the Form via Browser

**IMPORTANT:** Only fill if the Connect status is Draft.

### Using browser-harness (preferred)

1. Navigate to `https://v2.msconnect.microsoft.com/`
2. Wait for page load (React SPA — allow extra time for hydration)
3. Identify the rich text editors:
   ```javascript
   document.querySelectorAll('[contenteditable="true"], [role="textbox"], textarea, .ql-editor, .ProseMirror, [class*="editor"]')
   ```
4. For each section, click into the editor and type the drafted content
5. Take a screenshot for the user to preview
6. **Do NOT click Submit/Save**

### Using Playwright MCP (fallback)

1. `playwright-browser_navigate` to `https://v2.msconnect.microsoft.com/`
2. `playwright-browser_snapshot` to discover element refs
3. `playwright-browser_type` or `playwright-browser_fill_form` to fill editors
4. `playwright-browser_take_screenshot` to preview
5. **Do NOT click Submit/Save**

### Fallback: Output to File

If the Connect is not in Draft status, or browser automation fails:

1. Write the draft to a markdown file in the user's working directory:
   ```
   ./connect-draft-{YYYY-MM}.md
   ```

2. Also display the content in the chat for easy copy-paste.

## Step 6: Present to User

After filling the form (or writing the file), summarize what was done:

```
✅ Connect draft filled for {Connect period name}

**Sources used:**
- Calendar: {N} meetings analyzed
- Email: {N} threads reviewed
- Teams: {N} conversations reviewed
- Feedback: {N} items found
{only list optional sources that were actually available and used:}
- Customer repos: {list of customers}
- CRM: {N} opportunities / {N} milestones
- Kanban: {N} completed tasks

**Sections filled:**
1. Reflect on the past — {word count} words
2. Reflect on setbacks — {word count} words
3. Goals — {N} goals updated

⚠️ Please review the content before submitting.
The form is open at: https://v2.msconnect.microsoft.com/
```

## Error Handling

| Source | Failure Behavior |
|--------|-----------------|
| Browser can't reach msconnect | Inform user, offer to draft to file only |
| Connect is not in Draft status | Inform user, draft to file instead |
| Past Connect history empty | Skip style matching, use default professional tone |
| `m365_get_my_profile` fails | Ask user for their name and role |
| `m365_get_my_manager` fails | Read manager from the dashboard page header |
| `m365_list_events` fails | Note "Calendar data unavailable" — continue with other sources |
| `m365_search_emails` fails | Note "Email data unavailable" — continue |
| Customer repos don't exist | Silent skip — not mentioned in output |
| CRM tool not found | Silent skip — not mentioned in output |
| Kanban server not running | Silent skip — not mentioned in output |
| browser-harness not found | Fall back to Playwright MCP tools |
| Playwright MCP not available | Fall back to file output, inform user |
| Rich text editor not found | Fall back to file output, inform user |
| Form has changed structure | Take screenshot, show user, ask for guidance |

## Browser Notes

The skill uses whichever browser automation is available:

1. **browser-harness** (preferred if installed) — attaches to user's running Edge/Chrome via CDP, reuses login sessions. API: `goto()`, `new_tab()`, `wait_for_load()`, `js()`, `screenshot()`, `type_text()`, `click()`, `scroll()`, `page_info()`.
2. **Playwright MCP** (fallback) — uses `playwright-browser_*` tools. Works out of the box but runs a separate browser instance.

Always check which is available in Step 0d before starting browser operations.
