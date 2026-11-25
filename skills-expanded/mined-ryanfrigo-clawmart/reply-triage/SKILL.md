---
name: reply-triage
description: Classify an inbound reply (interested / not now / objection / referral / OOO / opt-out / bounce), extract the facts that matter, and draft the right next move.
metadata: { "openclaw": { "emoji": "📥" } }
---

# Reply Triage

A reply is where outbound actually starts. This skill reads inbound responses, sorts them into the categories that change what you do next, extracts the load-bearing facts, and drafts the reply — including the ones you never want to fumble, like opt-outs and hot leads.

## When to use (trigger phrases)

Use this skill when the user says:
- "triage my replies" / "what came back today?"
- "how should I respond to <name>'s reply?"
- "classify this reply: <pasted email>"
- "handle the inbox for the outbound campaign"
- (Automatic) whenever `followup-sequence` detects a reply.

## How it works

1. **Read the reply in context.** Pull the original thread and the prospect's `pipeline-log` entry so you know the angle you opened with and what stage they're at.
2. **Classify into one category.** Pick the single best fit:
   - **Interested / positive** — wants to talk, asks a question, says "tell me more." → hand to `meeting-booker` or answer the question, then propose a call.
   - **Referral** — "you want <other person>." → thank them, ask for a warm intro, start a new thread with the named person (fresh `prospect-research`).
   - **Not now / later** — "circle back in Q3," "no bandwidth." → agree, set a dated nurture reminder in `pipeline-log`, stop the active cadence.
   - **Objection** — price, timing, incumbent tool, "no need," "not the buyer." → respond per the playbook below; don't argue.
   - **Auto-reply / OOO** — out of office, parental leave. → extract the return date, pause the cadence until then, resume automatically.
   - **Opt-out / negative** — "remove me," "stop," "not interested," hostility. → one-line acknowledgment (or none), **suppress immediately and permanently**, cancel all sequences.
   - **Bounce / not here** — hard bounce, "no longer with the company." → mark invalid, ask the reply for the right contact if it's a human, else close.
3. **Extract the facts that matter.** Named competitor, budget or timeline, the real decision-maker, a specific objection, a return date. These update the deal, not just the reply.
4. **Handle objections without fighting.** Short, honest, one move each:
   - *"We already use <tool>."* → acknowledge, ask what's not covered, position as complement not rip-and-replace. If no gap, back off gracefully.
   - *"No budget / too expensive."* → don't discount reflexively; reframe on cost of the status quo, or offer a smaller starting scope.
   - *"Bad timing."* → agree, pin an exact recheck date, leave one useful resource.
   - *"I'm not the right person."* → treat as a referral; ask who is.
   - *"Not interested."* → one graceful line, suppress, move on. Never a rebuttal.
5. **Draft the next move.** Match the prospect's energy and length — a two-line reply gets a two-line answer, not a wall of text. Keep it in-thread.
6. **Update `pipeline-log`.** New stage, next step, next-step date, and any extracted fact (competitor, timeline, buyer). The log is the memory.
7. **Escalate hot leads to the human.** If interested or a real opportunity, flag it clearly ("🔥 Dana replied, wants a call") rather than auto-negotiating a deal. The agent books meetings; humans close.

## Output

Classification, confidence, extracted facts, a drafted reply, and the log update. Example:

```
REPLY — Dana Ruiz @ Acme
Category: OBJECTION (incumbent tool)  ·  Confidence: high
Facts: uses "Outreach" for sequencing; pain is research, not sending.

Draft reply (in-thread):
  Totally fair — Outreach handles the sending well. Where we tend to
  help isn't the cadence, it's the 40 min of research before each
  first touch. If that part's already covered, I'll happily back off;
  if it's eating your reps' mornings, worth a quick look?

Pipeline-log: stage engaged → next step "await reply", +2 days,
  note "incumbent: Outreach; wedge = research not sending."

Action: no meeting yet; keep cadence paused pending reply.
```

## Notes

- **Requires inbox access.** This skill reads the mailbox your cold opens send from; configure that channel in OpenClaw. Without read access it can only triage replies you paste in manually.
- **Opt-outs are non-negotiable and immediate.** Any "stop/remove/unsubscribe" suppresses the contact everywhere, same day. This is legal (CAN-SPAM/GDPR) and reputational. Never re-add a suppressed contact.
- **Don't auto-send to hot or hostile replies without review** — at least until you trust the voice. Positive replies are worth a human glance; angry ones should get suppression, not a clever comeback.
- **Confidence, not certainty.** When classification is ambiguous ("thanks" could be polite-no or genuine interest), say so and default to the softer, lower-risk move.
- **No fabrication in responses.** Don't invent case studies, customer names, or capabilities to win an objection. If we don't do the thing they need, say so and bow out — it protects the sender reputation and your integrity.
