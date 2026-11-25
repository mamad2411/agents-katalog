---
name: meeting-prep
description: >
  Prepare a comprehensive pre-meeting briefing by pulling together everything you need to walk in ready. Use this skill whenever the user asks to "prep me for my meeting", "what do I have coming up", "brief me before my call", "meeting prep", "get me ready for [meeting name]", or any similar phrasing. Also trigger automatically when the user opens Claude and there is a meeting starting within the next 20–30 minutes — proactively offer the briefing without waiting to be asked. Covers upcoming calendar events, attendee email history, open action items, agenda/notes from the invite, and optional web context about attendees or their company.
---

# Meeting Prep Skill

Generate a concise, actionable pre-meeting briefing by combining calendar data, email history, and optional web research.

---

## Workflow

### Step 1: Find the Target Meeting

Use Google Calendar to identify the meeting:
- If the user asked about a **specific meeting by name**, search for it.
- If the user asked generically ("prep me", "what's next"), fetch events for today and find the **next upcoming meeting** from the current time.
- If triggered proactively (Claude notices it's ~20 min before a meeting starts), surface that meeting.

Fetch the full event details: title, start/end time, location or video link (Zoom/Meet/Teams URL), description/agenda, and **attendee list with email addresses**.

---

### Step 2: Pull Email Context

Search Gmail for recent threads involving the meeting attendees.

**Search strategy:**
- Search by attendee email addresses and/or names.
- Determine how far back to look *smartly*:
  - If you find emails from within the last **2 weeks**, focus there.
  - If the last relevant email is older, expand to **1 month**, then **3 months**, stopping when you find substantive threads.
  - For brand-new contacts (no prior email history), note this explicitly.

**What to extract from emails:**
1. **Open action items** — anything that was promised, assigned, or requested but doesn't appear to have been resolved. Flag who owes what.
2. **Key discussion points** — topics that came up in recent threads relevant to this meeting.
3. **Thread summaries** — brief summary of the 2–3 most relevant recent threads.
4. **Tone / relationship context** — is this a new relationship, ongoing project, escalation, etc.?

---

### Step 3: Extract Agenda from Invite

Check the calendar event's description field for:
- A formal agenda
- Pre-read materials or links
- Goals or expected outcomes
- Any notes the user added

If there's no agenda, note it so the user is aware.

---

### Step 4: Optional Web Context

If the meeting involves **external attendees** (people outside the user's organization) or **company names** are mentioned in the invite/emails:
- Search the web briefly for recent news about those companies or individuals.
- Prioritize: funding rounds, product launches, leadership changes, recent press.
- Keep this section tight — 2–3 bullets max. Skip if nothing relevant surfaces.

---

### Step 5: Deliver the Briefing

Format the output as a clean, scannable briefing. Use this structure:

---

## 📅 [Meeting Title]
**When:** [Day, Date • Start–End Time]
**Where:** [Location / Video link]
**With:** [Attendee names and roles if known]

---

### 🗒️ Agenda
[Bullet points from invite, or "No agenda provided — consider setting one."]

---

### 📬 Email Summary
[2–3 sentence summary of recent threads with these attendees]

**Key threads:**
- [Thread title / topic] — [1-line summary]
- ...

---

### ✅ Open Action Items
- [ ] [Action item] — owed by [person] (from [email date])
- [ ] ...

*(If none found: "No outstanding action items found in recent emails.")*

---

### 🌐 Context & News  *(only if external attendees)*
- [Company/person]: [1-line recent news item]
- ...

---

### 💡 Suggested Talking Points
Based on the above, 2–3 suggested things to raise or be ready to address.

---

## Tone & Length

- Be concise. The goal is a 60-second scan, not a report.
- Use plain language. Avoid restating obvious things.
- If something is missing (no agenda, no prior emails), say so clearly — don't pad.
- If the meeting is with many attendees (5+), focus email search on the **organizer** and any VIPs, not every attendee.

---

## Edge Cases

- **Internal all-hands or recurring standups**: Skip email search unless the user asks. Just show agenda + time.
- **No attendees listed**: Work with whatever info the invite has. Note the gap.
- **Multiple meetings in the next 30 min**: Surface all of them, ask which one to prep for.
- **User asks for a specific meeting that's days away**: Still run the full workflow, just note it's not imminent.
