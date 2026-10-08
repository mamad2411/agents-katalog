---
name: outreach-message-skill
description: When a LinkedIn prospect connects, updates their status in the master tracker, creates their outreach message file, and generates a ready-to-post comment on their latest post.
categories: [linkedin, outreach, prospecting, crm, sales]
---

# Skill: Outreach Message Skill

## What This Skill Does
Handles everything that needs to happen the moment a LinkedIn prospect accepts a connection request. One trigger — three outputs: status updated in the master tracker, outreach file created with context and Phase 1 DM drafted, and a personalized comment ready to post on their latest content.

## When to Use
- A LinkedIn prospect just accepted your connection request
- You want to log the connection, create their tracking file, and warm them up with a comment — all at once
- You're working through a batch of new connections and need to action each one fast

## Inputs Required
Provide the following when running this skill:

1. **Prospect name** — first and last name exactly as it appears on LinkedIn
2. **Title and company** — their current role and organization
3. **LinkedIn URL** — their profile link
4. **Which list they're in** — 200K Club / Certification, JV Partner, Coaching, Jetpack Buyer, or Strategic Partner
5. **Latest post content** — paste the full text of their most recent LinkedIn post
6. **CR reply (optional)** — if they replied to your connection request, paste it here
7. **Context about them (optional)** — books, frameworks, audience, anything relevant

---

## Core Approach: Preeminence Before Pipeline

Every action this skill takes follows one rule: give genuine value before asking for anything.

The comment is not a foot-in-the-door tactic. It is a real contribution to their thinking. The outreach file is not a sales tracker — it is a relationship log. The Phase 1 DM is not a pitch — it is a question that shows you understand their world.

If any output from this skill would feel transactional or hollow if they saw the process behind it — rewrite it.

---

## Step-by-Step Instructions

### Step 1 — Update master-prospect-tracker.md

**File:** `/Users/admin/Documents/JV Deals/Simon/Simon Partnership/Prospects/master-prospect-tracker.md`

1. Search for the prospect by name in their relevant section (based on which list they're in)
2. Update their status field:
   - From: `CR Sent [date]`
   - To: `Connected ✅ [today's date]`
3. If they replied to the connection request, append: `— Replied: "[their exact reply]"`
4. If they are not found in the tracker, add a note in the output flagging this — do not add them silently

**Status format examples:**
```
Connected ✅ Apr 30
Connected ✅ Apr 30 — Replied: "Thanks for connecting, happy to be here."
```

---

### Step 2 — Create outreach message file

**Location:** `/Users/admin/Documents/JV Deals/Simon/Simon Partnership/Outreach Messages/`

**Filename:** `[firstname-lastname]-linkedin.md`

Build the file using this exact template:

```
# [Full Name] — LinkedIn Outreach
**Goal:** [Primary goal — e.g., "Podcast guest → Certification referral partnership"]
**Status:** ✅ Connected [date] — Comment 1 queued
**LinkedIn:** [LinkedIn URL]
**Updated:** [today's date]

---

## Context

[2–3 sentence paragraph: who they are, what they're known for, why they're relevant to Simon's world]

**What we know about them:**
- [Role / company]
- [Key credential — book, methodology, community, audience size]
- [Strategic fit: how their audience or work connects to Simon's Certification or The Sales Show]

---

## Conversation Log

| Date | Who | Message |
|------|-----|---------|
| [CR sent date — pull from tracker if available, else write "Unknown"] | Haider | Connection request sent |
| [Today] | [Name] | ✅ Accepted |
[If they replied to the CR:]
| [Today] | [Name] | "[Their exact CR reply]" |

---

## Phase 1 DM — Trust-Building
*(Send after Comment 1 gets a reaction or reply)*

[Write a tailored Phase 1 DM using the Preeminence approach:
- Reference something specific from their work (book, framework, methodology, post)
- Ask one genuine question about their thinking — something you actually want to know
- No pitch, no mention of Simon, no CTA
- 3–5 sentences max
- Plain text only]

---

## Sequence Plan

| Step | Action | Status |
|------|--------|--------|
| 1 | Connection request sent | ✅ Done |
| 2 | Comment on Post 1 | ⬜ Ready to post |
| 3 | Phase 1 DM — trust-building question | ⬜ After Comment 1 reaction |
| 4 | Comment on Post 2 | ⬜ After Phase 1 DM sent |
| 5 | Phase 2 — Podcast + Certification pitch | ⬜ After Phase 1 reply |
```

---

### Step 3 — Generate LinkedIn comment

Write a comment on their latest post following these rules:

**What the comment must do:**
- Reference a SPECIFIC idea, phrase, or detail from their post — not the topic in general
- Add a genuine insight, extension, or real-world observation that builds on their point
- 3–5 sentences. No more.
- End with a thought that invites dialogue — a contrarian observation, a pattern you've noticed, or an open thread. Not always a question.

**What to avoid:**
| ❌ Don't | ✅ Do instead |
|---------|-------------|
| "Great post!" or "Love this insight" | Name the specific idea that landed |
| Generic industry observation | A concrete pattern from real work |
| Asking a hollow question | A thought that genuinely opens the conversation |
| Hashtags or emojis | Plain text only |
| Commenting on the topic not the post | Show you read this specific post |

**The test:** Would this comment make them pause and want to know who wrote it? If yes — output it. If no — rewrite it.

**Output format for the comment:**
Plain text, no markdown, no labels. Just the comment text, ready to copy and paste directly into LinkedIn.

---

## Output Format

Deliver in this order:

1. **Tracker update confirmation** — one line: "Updated [Name] in [Section] → Connected ✅ [date]" (or flag if not found)

2. **Outreach file confirmation** — one line: "Created [filename] in Outreach Messages"

3. **LinkedIn Comment — ready to post:**
[plain text comment, no markdown, no label above it except this header]

4. **Phase 1 DM — for reference:**
[plain text DM, copy-paste ready — remind user to send after Comment 1 gets a reaction]

---

## Pro Tips

- Post the comment within 24 hours of connecting — you're fresh in their mind and the post is still getting traction
- The comment does more than warm them up — it signals that you actually read their work. Most people don't.
- If their latest post is weak or generic, find an older post worth commenting on. A sharp comment on a good post beats a hollow one on a recent post.
- The Phase 1 DM should feel like it comes from someone who has thought about their work — not someone who just Googled them. Use what they shared in the post.
- Never send the Phase 1 DM the same day you comment. Let the comment breathe for 24–48 hours first.
- If they reply to the comment before you send the DM — use their reply as your DM opener. "Your point about X in the comments made me think about this..."

---

## Example Output

**Input:**
- Name: Marcus Chan
- Title: Founder, Venli Consulting Group
- LinkedIn: linkedin.com/in/marcuschan
- List: 200K Club / Certification
- Latest post: "Most salespeople wait to build rapport at the start of a call. The problem? By then, the prospect is already judging you. Rapport isn't a phase — it's the entire call. Every question, every pause, every reframe is either building trust or eroding it. Act accordingly."

---

**Output:**

Tracker update confirmation:
Updated Marcus Chan in Section 1: 200K Club & Certification → Connected ✅ Apr 30

Outreach file confirmation:
Created marcus-chan-linkedin.md in Outreach Messages

LinkedIn Comment — ready to post:

The reframe from "rapport phase" to "rapport is the entire call" is the one most sales trainers miss. When you treat rapport as a discrete step, you're essentially telling yourself it's optional once you hit the next phase — and that's exactly when prospects feel the shift. The salespeople who close without resistance aren't smoother talkers, they're the ones who never stopped being curious about the person on the other end.

Phase 1 DM — for reference:

Marcus — the distinction you drew between rapport as a phase versus rapport as the entire call is something I think about a lot in sprint-based sales work. Most frameworks treat it as a warmup. Curious: in your experience, at what point in a deal do you see trust erode fastest — and is it always something the rep did, or is some of it just timing?
