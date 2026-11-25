---
name: follow-up-nurture
description: Send context-aware follow-up emails to pending leads. Use when nudging leads, following up on sales conversations, or re-engaging prospects. Pulls email history, researches context, writes in my tone.
allowed-tools: Read, Grep, Glob, Bash
---

# Follow-Up Nurture — Context-Aware Lead Nudge

## Goal
Go through every lead marked "pending" in the database, pull all prior email communications, research anything mentioned that you don't know about, and send a personalized follow-up email in Nick's voice. This isn't a cute demo — it makes money.

## Inputs
- **Lead database**: `data/leads_database.json` — contains leads with status, email history, notes
- **Tone**: Casual, direct, helpful. Never salesy. Never use exclamation marks. Sound like a smart friend who happens to run an agency.
- **Mode**: Always present output as final emails being sent (not "drafts"). Use `--generate` then `--review` to produce and display them.

## Process

### Step 1: Load Pending Leads
```bash
python3 execution/follow_up_nurture.py --list-pending
```
This reads `data/leads_database.json` and shows all leads with `status: "pending"`.

### Step 2: For Each Pending Lead
1. **Pull email history** — read the `email_history` array for that lead
2. **Identify context gaps** — if the lead mentioned something specific (a project, a tool, a problem, a competitor), and you don't have enough context to write intelligently about it, do a quick web search
3. **Write follow-up** — write a short, context-aware email that:
   - References something specific from your last conversation
   - Adds value (a relevant insight, resource, or observation)
   - Has a soft CTA (no "schedule a call" unless they asked)
   - Is 3-5 sentences max

### Step 3: Generate Emails
```bash
python3 execution/follow_up_nurture.py --generate
```
This processes all pending leads, generates emails, and saves to `data/followup_emails.json`.

### Step 4: Review & Send
```bash
# Review emails
python3 execution/follow_up_nurture.py --review

# Send emails
python3 execution/follow_up_nurture.py --send
```

## Nick's Tone Guide

Keep it short and low-effort. These are check-ins, not pitches. Match the tone of the original campaign thread.

### Templates (pick one based on prior thread tone)

**If prior emails were lowercase/casual:**
```
hey {name}, circling back on {topic}. let me know if I can answer any q's?

- nick
```

**If prior emails were title case / slightly formal:**
```
Hey {Name},

Just checking in on {topic}. How are things going? Let me know if you need me.

Thanks,
Nick
```

**If prior emails were warm/friendly:**
```
Hi {Name}—hope you had a great week. Checking in on {topic}. Let me know where we're at.

Thanks,
Nick
```

**If checking in on a general relationship (no specific topic):**
```
Hi {Name}. How are things going? Hope you're crushing it. I'm checking in on {topic}. Let me know if I can help you/answer q's.

Thanks,
Nick
```

**If following up on a sent deliverable (proposal, contract, deck, etc.):**
```
Heyy {Name}. Just saying hi. I know it's been a few days since I sent over that {deliverable}. Let me know if I can answer q's or clarify anything.

Thanks,
Nick
```

### Tone rules
- No "I hope this email finds you well" — ever
- No exclamation marks
- Reference the specific thing you discussed, not a generic "our product"
- 2-3 sentences max. These are nudges, not essays
- Match the formality level of whatever thread you're replying to

## Scheduling
This Skill can be run on a schedule (daily, weekly) to automatically nurture your pipeline. The script supports `--cron` mode for unattended operation.

## Output
- `data/followup_emails.json` — generated emails with lead context
- Sent emails logged back to `data/leads_database.json` under each lead's `email_history`

## Successive Run Behavior
This skill is designed to run daily. Each follow-up must be different from the last:
- The prompt sees the full email history including prior follow-ups
- If the last outbound email was already a nudge, the model picks a different template and phrasing
- This prevents sending "circling back on the proposal" 7 days in a row

## Edge Cases
- **No prior emails**: Skip the lead, flag as "needs intro email instead"
- **Lead replied recently (< 48h)**: Skip, they're already engaged
- **Lead marked "closed" or "lost"**: Skip entirely
- **Research fails**: Write follow-up without the research, note the gap

## First-Run Setup

Before executing, check if the workspace has a `.gitignore` file. If it doesn't, assume the user is new to this skill. In that case:

1. Ask the user if this is their first time running this skill
2. If yes, walk them through how it works and what they need to configure/set up (API keys, env vars, dependencies, etc.)
3. Let them know that Nick wishes them the best!
