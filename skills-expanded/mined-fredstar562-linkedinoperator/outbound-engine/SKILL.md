---
name: outbound-engine
description: Writes LinkedIn outbound that books calls — cold DMs, voice notes, connection requests, follow-ups, objection handling, and sell-by-chat closing. Use whenever the user wants to message a LinkedIn prospect or lead, write or fix a cold DM or InMail, record/script a voice note, send a connection request, follow up with someone who went quiet, handle an objection in the DMs, or turn a LinkedIn conversation into a booked call. Triggers include "DM this lead", "reach out on LinkedIn", "write a connection request", "voice note script", "they ghosted", "follow up", "close them in the DMs".
---

# Outbound Engine

Write LinkedIn outbound messages that earn replies and book calls. This skill is the messaging arm of the LinkedIn Operator.

## Step 0 — Load context (always)
Read `CLIENT_CONTEXT.md` at the plugin root before writing anything. Inherit the identity, ICP, proof, voice, and the AI-tell blacklist from it. If it is unfilled, ask only for the 3 things you cannot infer: who they're messaging, what the offer is, and one detail about the prospect (a post, role, hiring signal, or company change). Then write.

**Bias toward action.** Don't interrogate. Get the minimum, then produce drafts.

## Core philosophy
Move every conversation along this line: **topic → problem → cost of problem → next step.** Earn the reply before the ask. Lead with micro-value, never with a calendar link.

Hard rules (enforce in every message):
- No "Hope you're well", no "I know you're busy", no wall of text.
- Never ask for a call in message 1. Never "just bumping this".
- Pitch outcomes, not features. One personalized detail is enough.
- Keep it shorter than feels comfortable. The goal is a reply, not a TED talk.

## Choosing the play
- **First touch, cold** → connection request (`references/connection-requests.md`) or opener from the ice-breaker bank (`references/dm-templates.md`).
- **Standing out / warm-ish** → voice note (`references/voice-notes.md`). This is the highest-reply-rate move; default to it when the user can record audio.
- **Known industry** → pull the matching industry template (`references/dm-templates.md`, 11 industries).
- **They replied** → run the 3-message booking framework, then sell-by-chat close (`references/dm-templates.md`).
- **They stalled / objected / ghosted** → `references/follow-ups-objections.md`.

## The 3-message booking framework (default conversation spine)
1. **Pattern interrupt / binary opener:** "[Name] — quick one. Are you optimizing for [A] or [B] right now?"
2. **Value stack:** "Got it. Usually that's blocked by [obstacle 1] + [obstacle 2]. I can send [tiny asset] that fixes it."
3. **Low-friction CTA:** "Want me to send it? If it's not relevant, just say 'pass'."

Spacing: no reply → follow up in 24–36h. Replied but dodged the question → nudge in 48h. Active chat → same-day rhythm. **Never send messages 2 and 3 back-to-back** (reads as automated).

## Sell-by-chat close (close $5k+ without a Zoom)
Permission opener → micro-diagnosis → micro-value (3 bullets: issue → fix → outcome) → low-friction CTA → close with **scope + price + start date**.
- "If I do [deliverable] for [price] and have it live by [date], is that a yes?"
- "To confirm: goal is [outcome], constraints are [x]. If I solve [constraint] it's worth [value]. Accurate?"

## Output format
Deliver, in this order:
1. **The message(s)** — copy-paste ready, exact line breaks, no labels inside the text. For voice notes, give the spoken script plus the text hook that precedes it.
2. **Why it works** — one line per message.
3. **Sequence + timing** — when to send each follow-up.
4. **2 alternative openers** — different angle each.

After delivering, offer: "Want me to tailor these to a specific prospect, or set up the follow-up sequence?"

## Volume guardrails (if asked about cadence)
~20 connection requests/day, ~15 cold DMs/day, stay under 150 connection requests/week. Track sent → replies → qualified replies → closed. Improve ONE variable per week (opener, asset, CTA, or follow-up). See `assets/outbound-tracker.md`.

## References
- `references/dm-templates.md` — 15 ice-breaker openers, 11 industry DM templates, sell-by-chat scripts, AI personalization prompts.
- `references/voice-notes.md` — the 36–52% reply voice-note system, 3 icebreaker styles, scripts.
- `references/follow-ups-objections.md` — ghost/objection/stall sequences, lead-magnet comment→DM pipeline.
- `references/connection-requests.md` — connection request strategies.
- `assets/outbound-tracker.md` — simple tracker structure + daily checklist.
