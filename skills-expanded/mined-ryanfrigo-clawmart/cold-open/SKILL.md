---
name: cold-open
description: Draft a personalized, non-templated first-touch email or DM from prospect research — one specific observation, one hypothesis, one soft ask.
metadata: { "openclaw": { "emoji": "✉️" } }
---

# Cold Open

Write the first-touch message that actually earns a reply: short, specific, and built on one real observation about the prospect — never a mail-merge template with a `{{first_name}}` bolted on.

## When to use (trigger phrases)

Use this skill when the user says:
- "write a cold email to <person / company>"
- "draft a first touch for this lead"
- "reach out to <name> at <company>"
- "cold open <domain>" or "open <prospect> for me"
- "send a first DM to <person> on LinkedIn/Twitter"

If there's no research card yet, run the `prospect-research` skill first — the message is only as good as the observation it's built on.

## How it works

1. **Load the research card.** Pull the output of `prospect-research`: the company one-liner, the person's role, the recent signals, and the single best angle. If none exists, run that skill first. Never write from a blank slate — a generic opener is worse than no opener.
2. **Pick exactly one trigger.** Choose the single strongest, most recent, most verifiable signal (a funding round, a new hire in a relevant seat, a job posting, a product launch, a public complaint). One idea per message. Discard the rest.
3. **Form a value hypothesis.** State, in your own head, "Because <trigger>, they probably care about <outcome>, and we help by <mechanism>." The whole email is one sentence of this hypothesis made human.
4. **Write the subject line.** 2–4 words, lowercase or sentence case, no clickbait, no emojis, no "Quick question." Reference the specific thing: `series a + hiring`, `your returns flow`, `re: the SDR req`. It should read like a note from a peer, not a campaign.
5. **Write the body in four beats, ~50–90 words total:**
   - **Observation (1 line):** the specific trigger, shown not told. "Saw you posted two AE roles last week."
   - **Bridge (1 line):** why that connects to a problem you solve. "Usually means pipeline is outpacing the team that works it."
   - **Proof / mechanism (1 line):** how you help, concretely, no adjectives. "We book the top-of-funnel research + first touch so new reps ramp on live conversations, not list-building."
   - **Soft CTA (1 line):** ask for interest, not a 30-minute meeting. "Worth a look, or is outbound already handled?"
6. **Match the channel.** Email: plain text, no images, no tracking links in the first touch (they hurt deliverability and read as spam). LinkedIn/Twitter DM: drop the subject, cut to ~40 words, even more casual. Keep the sender identity the one the user configured.
7. **Produce two variants.** One leading with the trigger, one leading with the outcome. Label each and note which angle it uses so the user can pick.
8. **Never do these:** "I hope this email finds you well," "I noticed you're the <title>," fake flattery, three paragraphs, a link, a calendar link, or more than one ask. If you catch yourself writing any of them, cut it.

## Output

Return the subject and body as ready-to-send text, plus a one-line note on the angle. Example:

```
Angle: hiring signal → ramp problem

Subject: two AE reqs

Hey Dana — saw Acme opened two AE roles last week. Usually
means pipeline is coming in faster than the team can work it,
and new reps burn their first month on list-building instead
of live calls.

We run the research + first touch so reps ramp on real
conversations. Happy to show you what that looks like on a few
of your named accounts — worth a look, or is outbound already
covered?

— <sender>

---
Variant B (outcome-led)

Subject: ramping the new AEs

Hey Dana — quickest way I know to get two new AEs to quota is
to hand them warm-ish conversations on day one instead of a
list and a login...
```

Then ask: "Want me to queue the follow-up cadence?" (hands off to `followup-sequence`).

## Notes

- **You configure the email/DM channel and sender identity in OpenClaw.** This skill drafts; it sends only through the channel and credentials you've set up. Confirm the send-from address is a warmed domain, not your primary one, if you're doing volume.
- **Deliverability is a real constraint.** No links or images in touch one, keep daily volume sane, and don't send identical bodies at scale — the two-variant + per-prospect observation approach exists partly for this reason.
- **Compliance is on you.** Cold outbound is regulated differently by region (CAN-SPAM in the US requires a real physical address and opt-out honoring; GDPR/PECR in the EU/UK are stricter and often require a lawful basis). This skill won't add an unsubscribe footer or check consent unless you tell it to. Know your obligations before sending.
- **Honesty:** every claim in the message must be true and defensible. If the research card's signal is unverified, don't assert it as fact — soften to "looks like" or drop it. A confidently wrong opener kills the thread and your credibility.
- **This is a draft, not an autosend.** Keep a human in the loop for the first batch until you trust the voice; it's easy to review 10 drafts and catch the one that's off.
