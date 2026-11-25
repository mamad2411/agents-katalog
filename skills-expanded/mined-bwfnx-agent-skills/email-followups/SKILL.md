---
name: "email-followups"
description: "Break through follow-up email paralysis: find the threads that actually need the user's reply, triage them into a small concrete list, and draft responses in their voice as ready-to-send drafts. Use whenever the user says they're behind on email, can't get themselves to respond, are avoiding the inbox, feel overwhelmed by email, ask \"who am I ignoring\" or \"what do I owe people,\" or want help catching up on replies. Also runs as a scheduled weekly fallback. Trigger even when they don't say the word \"skill\" — this is for the emotional avoidance of email, not literal inbox management."
---

# Email Follow-Ups — Getting Unstuck

## What this is for

Follow-up paralysis: threads pile up, replying feels heavier than it should, and the pile *feels* bigger than it is. The job of this skill is not "manage the inbox" — it's to dissolve the wall: make the pile small and concrete, do the heavy lifting, and hand back ready-to-send drafts so all that's left is a glance and a click.

Design everything around lowering the activation energy. Every choice should reduce the number of decisions the user has to make, not add them.

## Setup (first run, then remembered)

Ask once, in one message, and keep the answers in `TASKS.md` under `## Email follow-ups config` or wherever the user prefers:

1. **Lookback window** — default 30 days.
2. **Priority label** — a label the user or an automation applies to threads that matter (many people have one; if not, skip this).
3. **Key people** — colleagues and clients whose threads always count. Names and addresses. Add to this over time.
4. **Working window for scheduling** — default 10:00 AM–2:00 PM local; meeting length default 50 minutes.

## The core loop

1. **Find** the threads where the ball is genuinely in the user's court.
2. **Triage** them into a tight list: *Needs you* vs *Optional* vs *Skip*.
3. **Show** the list — small, calm, one clear next action. Lead with reassurance when the pile is smaller than it feels ("Only three actually need you").
4. **Draft** replies in the user's voice for the *Needs you* ones, as drafts in their mail tool. Never send.
5. **Hand off** — say the drafts are sitting in the mail tool, ready to review and send.

Work the whole loop in one pass unless stopped. Don't ask permission to start drafting — drafts are safe and reversible; sending is the only gated action.

## Step 1 — Find the threads

Start with the priority label if there is one. In Gmail, search by label **name**, not internal id: `label:"Follow Up"`. Then broaden as a safety net:

```
in:inbox newer_than:30d -category:promotions -category:social -category:updates -category:forums
```

Adjust the window if asked ("last week", "since I got back"). Pull enough threads to see the whole picture (40+), then read the message list.

**A thread "needs a reply" when the last real message is from someone else and the user hasn't answered it.** That's the signal — not unread status, and not the label alone. If the user sent the most recent message, the ball is in the other court — skip it.

Judgment calls the label can't make:

- **Already replied** → skip.
- **Emoji/reaction-only last message** → not a real reply. Look at the last substantive message.
- **Conversationally closed** ("Sounds good," "Will do," "Thanks!") → no reply owed. Don't manufacture one.
- **Stale but open** → still owed, but flag the age ("This one's from February — still want to reply?") and, if drafting, acknowledge the gap gracefully.
- **Mixed/forwarded threads** → if the user looped a colleague in but never answered the original external sender, they may still owe that sender. Surface as borderline rather than confidently drafting.

## Step 2 — Triage

**Scope: clients and key people.** Skip pure internal chatter, automated notices, and newsletters. "From a key person" does not by itself mean "Needs you" — a group FYI is *Optional*. The deciding test: *is this person waiting on a real answer or decision from the user specifically?*

- **Needs you** — a client or key colleague is waiting on a real answer or decision. These get drafted.
- **Optional** — cc'd on a thread flowing fine, an RSVP, an FYI. One line each; draft only if asked.
- **Skip** — noise, handled, or the ball's with the other person. Don't clutter the list.

## Step 3 — Show the list

Lead with the headline count ("Five threads hit your inbox; only two actually need you"). For each *Needs you* thread: who, one sentence on what they want, what the reply will do. One or two lines each. List *Optional* ones briefly underneath.

## Step 4 — Draft the replies

**Voice:** draft as the user. If a writing-style skill or note exists, follow it; otherwise short, warm, direct, plain language. First name. Every reply lands a concrete next step. Natural sign-off, no over-thanking, no corporate filler.

**Draft only, never send.** Create each reply as a draft threaded to the right conversation (in Gmail: `create_draft` with `replyToMessageId` = the id of the latest message). Sending on the user's behalf is an approval-gated action this skill never crosses.

Drafts must be sendable as-is — no `[placeholders]`. If a fact is missing, write around it or make the reasonable assumption and note it outside the draft.

## Step 5 — Scheduling: ask before proposing times

When a reply needs a meeting time, **pause and ask before proposing slots**, even if the other person already listed availability. On go-ahead: pull the calendar for the target week, treat recurring focus/planning/lunch blocks as busy, find open windows in the working window long enough for the meeting, offer two options in the draft (different first choices for different people in the same week), and don't create the event until the other person picks and the user says go.

**Unattended weekly run:** don't propose slots or touch the calendar. Draft the reply asking for a couple of windows that work for them (or acknowledge windows they sent and say the user will confirm shortly).

## What stays gated

Never without explicit go-ahead: sending any email, creating or sending calendar invites, contacting anyone on the user's behalf. Reading, triaging, drafting, and checking the calendar are fine unprompted.

## How it runs

- **On-demand** — full interactive loop including the scheduling ask.
- **Weekly fallback** — a Monday-morning scheduled run scans the label and recent key-people threads, drafts replies, and leaves a short summary of what's waiting. Never sends.

## Tone reminder

The user came here because the task feels heavy, not because they can't operate email. Be the calm hand that shrinks the pile — reassuring, concrete, done *with* them, never a lecture about staying on top of the inbox.
