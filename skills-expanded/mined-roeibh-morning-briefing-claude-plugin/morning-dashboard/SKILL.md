---
name: morning-dashboard
description: Combine all morning briefing outputs into a single unified HTML dashboard. This skill runs LAST, after all other workstreams have completed. Automatically invoked by the start skill.
---

# Morning Dashboard

You are a dashboard builder. After all other morning briefing skills have produced their reports, combine them into a polished HTML dashboard that serves as the user's morning command center.

## CRITICAL: Read Local Config First

Read `morning-briefing.local.md` for the user's name (for the greeting) and role context.

## CRITICAL: Every Item Must Be Clickable

The dashboard is a command center — the user needs to jump directly to every item. Enforce these rules:

- **Every PR** must link to `https://github.com/ORG/REPO/pull/NUMBER`
- **Every Slack thread** must link to `https://WORKSPACE.slack.com/archives/CHANNEL_ID/pMESSAGE_TS`
- **Every Morning Reading article** must link to the source URL
- **Every competitor news item** must link to the source URL
- **Every calendar event** should link to the Google Calendar event or meeting URL (Zoom/Teams/Meet)
- **Every email** should link to `https://mail.google.com/mail/u/0/#inbox/MESSAGE_ID` if available

If a source briefing file doesn't include a URL for an item, render the title as plain text but add a small "🔗 missing" indicator so the user knows the link wasn't captured.

Use `<a href="URL" target="_blank" style="color: #60a5fa;">Title</a>` for all links. They must open in a new tab.

## CRITICAL: HTML Validation

Before saving the HTML file:
- Verify all `<script>` tags are properly closed
- Verify all functions have complete closing braces
- The file must end with `</html>`
- Test that `copyPriorities()` function is complete

## CRITICAL: Generated Timestamp

Include a footer with: "Generated [DATE] at [TIME] by Morning Briefing v2.0"

## Process

### Step 1: Read All Briefing Files

Look for these files in the working folder (all dated today):
- `briefing-email-YYYY-MM-DD.md`
- `briefing-slack-YYYY-MM-DD.md`
- `briefing-calendar-YYYY-MM-DD.md`
- `morning-reading-YYYY-MM-DD.md`
- `briefing-github-YYYY-MM-DD.md`
- `briefing-competitors-YYYY-MM-DD.md`

### Step 2: Extract Key Metrics

From each file, pull top-level numbers:
- Emails: count per tier, drafts created
- Slack: unread count, mentions, DMs waiting
- Calendar: meetings count, hours blocked, focus time
- GitHub: PRs needing review, failing CI
- Industry: must-read article count
- Competitors: any high-threat moves

### Step 3: Build the HTML Dashboard

Create a self-contained HTML file with:

**Design requirements:**
- Dark theme (background: #0f172a or gradient, cards: #1e293b, text: #e2e8f0)
- CSS Grid layout, responsive
- Zero external dependencies — everything inline (CSS + JS)
- Color coding: red (#ef4444) for urgent, amber (#f59e0b) for important, green (#22c55e) for FYI
- Clean, modern aesthetic with subtle card shadows and rounded corners

**Interactive features (JavaScript):**
- **Every card MUST be collapsible** — clicking the card header toggles the content. Use a toggle icon (▼/▶) that rotates on collapse. The Urgent Actions card should start expanded, others can start expanded too.
- **"Copy Priorities" button** — copies top 5 priorities to clipboard. Use inline feedback: change button text to "✅ Copied!" for 2 seconds. Do NOT use `alert()`.
- Smooth CSS transitions on collapse/expand

**Dashboard sections:**

1. **Header**
   - Greeting with user's name + current date + day of week
   - Quick stats bar: emails | Slack mentions | meetings | PRs to review
   - Small "connection status" row showing which method each workstream used (e.g., "📧 Gmail connector ✅ | 💬 Slack connector ✅ | 📅 Calendar Chrome | 🐙 GitHub connector ✅")

2. **🔴 Immediate Actions Card**
   - Combined list of ALL urgent items across every workstream
   - Each item: source icon + one-liner + what to do
   - This is the most important card — make it prominent

3. **📅 Today's Schedule Card**
   - Visual timeline of meetings with gaps for focus time
   - Color-coded by meeting type
   - Show duration for each block
   - **For each meeting: include 1-2 prep actions** (from the calendar briefing), not just the title
   - Include meeting join links (Zoom/Meet/Teams) when available
   - Highlight conflicts in red

4. **📧 Email Summary Card**
   - Show which accounts were checked and how (e.g., "[Gmail via connector] [Outlook via Chrome]")
   - Tier 1 items with subject + action
   - Count of Tier 2 and Tier 3
   - Note how many draft replies were created
   - **Cleanup stats: "[X] archived, [Y] marked read, [Z] unsubscribed"**
   - **Inbox status: "[X] unread remaining (all Tier 1)"**

5. **💬 Slack Summary Card**
   - Threads needing response (with deep links)
   - For high unread counts: include a 1-line summary of what's being discussed, not just the number
   - Channel activity summary should say WHAT happened, not just "75 unread"

6. **🐙 GitHub Card**
   - PRs awaiting review with CI status badges
   - What shipped yesterday
   - Stale PRs flagged separately

7. **📰 Morning Reading Card**
   - Top 5 curated links with titles and one-line descriptions
   - Every title MUST be a clickable `<a href>` link

8. **🏁 Competitor Intel Card**
   - Any moves with clickable source links (or "All quiet")

9. **💡 Today's Priorities Card**
   - AI-generated top 5 priorities based on urgency, deadlines, and schedule
   - Synthesized from all workstreams

### Step 4: Generate Summary

Also produce `briefing-summary-YYYY-MM-DD.md` — a 30-second scannable text version:

```markdown
# ☀️ Morning Briefing Summary — [DATE]

**🔴 Urgent**: [count] items need immediate attention
**📅 Today**: [count] meetings ([hours] blocked), [focus windows]
**📧 Email**: [Tier 1 count] action required, [Tier 2 count] important, [drafts] drafted
**💬 Slack**: [mentions] mentions, [unreads] unread
**🐙 GitHub**: [PRs] PRs need review, CI [status]
**📰 Reading**: [count] must-read articles today
**🏁 Competitors**: [notable or "all quiet"]

## Top 5 Priorities Today
1. [Priority 1 — source and reason]
2. [Priority 2]
3. [Priority 3]
4. [Priority 4]
5. [Priority 5]
```

### Step 5: Save and Open

- Save HTML as `morning-dashboard-YYYY-MM-DD.html`
- Save summary as `briefing-summary-YYYY-MM-DD.md`
- Open the HTML dashboard in the browser

## Fallback

If some briefing files are missing, build the dashboard with whatever is available. Show a subtle "⚠️ [Section] data unavailable" note for missing sections. Never fail entirely because one workstream didn't complete.
