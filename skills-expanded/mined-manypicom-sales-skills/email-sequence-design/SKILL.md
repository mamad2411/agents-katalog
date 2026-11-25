---
name: email-sequence-design
description: Design multi-step cold email sequences — how many steps, what each one says, timing, and when to stop. Use whenever the user mentions email sequences, follow-ups, drip campaigns, cadences, multi-step outreach, bump emails, or asks how many times to follow up. Also use when a first email gets replies but the sequence doesn't, or when someone is writing follow-ups that just say "just checking in".
---

# Email Sequence Design

Most replies to cold outreach come from follow-ups, not from the first email. Most senders either stop after one, or send five that all say the same thing in a slightly more irritated tone.

The principle: **every step must be worth opening on its own.** A follow-up that adds nothing is worse than no follow-up, because it converts a neutral non-response into mild annoyance.

## The shape

Four steps over roughly two weeks is the reliable default.

| Step | Day | Job | Length |
|---|---|---|---|
| 1 | 0 | The pitch, personalised | 60-90 words |
| 2 | +3 | New angle, or proof | 40-60 words |
| 3 | +7 | Different value — resource, insight, question | 40-60 words |
| 4 | +14 | The close-out | 20-30 words |

Get shorter as you go. By step four you're asking one question in two lines.

Longer sequences work in some markets, particularly where the buying cycle is long, but the marginal reply rate falls quickly and the complaint rate rises. If steps five through eight are needed, the problem is usually targeting rather than persistence.

## What each step does

**Step 1.** The specific first line, the connection, the one-sentence pitch, the small ask. Covered in `cold-email-copywriting`.

**Step 2 — a different angle, not a repeat.** The most common failure. If step one led with the hiring signal, step two leads with a customer result. If step one asked about their process, step two offers a concrete observation. Same person, new reason to reply.

> Different thought — the three agencies we work with your size all had the same problem: verified lists, good copy, and replies going to an inbox nobody owned. Fixing the routing was worth more than any copy change.
>
> Is that a thing on your side?

**Step 3 — give something.** No ask, or a very small one. A relevant teardown, a number from your own data, a useful observation about their site. This is the step that converts the people who found step one plausible but not urgent.

**Step 4 — the close-out.** Short, no guilt, easy to reply to. The permission-to-close-the-file email genuinely produces replies, because it's the first one that doesn't want anything.

> Haven't heard back, so I'll assume the timing's wrong and leave it there.
>
> If it's worth revisiting later, just reply and I'll pick it up.

Don't dress it up as a breakup. "I guess you're not interested" is passive-aggressive and people read it that way.

## Timing

- **3 days after step one.** Long enough not to nag, short enough to stay in context.
- **4 to 7 days between later steps.** Widen the gaps as you go.
- **Working days only**, in the recipient's timezone.
- **Avoid Monday morning and Friday afternoon.** Tuesday to Thursday, mid-morning, is the conventional window and it's conventional because it works.
- **Never send two steps in the same 24 hours.**

Thread or fresh subject? Threading step two onto step one gives context and looks like a normal follow-up. A fresh subject on step three gives a second chance at the open. A common pattern is threading steps one and two, then a new thread for three and four.

## Merge variables and fallbacks

Every variable is a chance to look automated.

```
Hi {{first_name|there}},
```

Set fallbacks on everything. `Hi {{first_name}},` rendering as `Hi ,` is the single most recognisable automation failure, and it invalidates the whole email.

Rules:

- **Fallback on every variable**, and make the fallback read naturally.
- **Never put a variable in the subject line without checking the fallback.**
- **Normalise the data first.** `{{first_name}}` pulling "DR. SARAH JONES-SMITH" is a data problem, and it renders in front of the prospect. See `crm-data-hygiene`.
- **Test-render 20 real leads** before launching. Read all 20. This catches things nothing else does.
- **Prefer a researched custom column** over a firmographic variable. "Saw you're hiring two SDRs" beats "As a company in the {{industry}} space".

## When the sequence stops

Automatic stops, and every one of these should be enforced by the system rather than by a person:

| Event | Effect |
|---|---|
| They reply | Cancel all remaining steps immediately |
| They unsubscribe | Cancel, and suppress the address permanently |
| Hard bounce | Cancel, mark undeliverable, don't retry |
| Out-of-office auto-reply | Pause, resume after the stated return date |
| Someone else at the account replies | Cancel for the whole account, not just the person |

That last one matters and is often missed. Continuing to email three people at a company after one of them replied looks careless and undermines the reply you got.

The reply-stop must be immediate and reliable. A follow-up sent after someone answered is the fastest way to lose a warm conversation.

## Sequences for multiple people at one account

When targeting several people at the same company, coordinate rather than running parallel sequences:

- **Stagger by a few days** rather than emailing everyone at once.
- **Vary the angle by role.** The same email to the VP and the analyst reads as a mail merge, and they do talk.
- **Stop the whole account on any reply.**
- **Cap at three people per company** for most segments. More looks like a blast.

## Reviewing an existing sequence

1. **Read all four in a row as the recipient.** Most sequences read as one email sent four times.
2. **Does each step stand alone?** Someone who missed step one should understand step three.
3. **Does any step say "just checking in" or "bumping this"?** Rewrite it — those add nothing.
4. **Does the length decrease?**
5. **Test-render 20 real leads.** Look for broken variables and awkward fallbacks.
6. **Is the reply-stop actually working?** Test it with a real address.
7. **Is step four gracious?**

## What the metrics tell you

- **Step one gets replies, later steps don't** — the sequence is repeating itself. Rewrite steps two and three with genuinely new angles.
- **Nothing gets replies** — it's targeting or copy, not cadence. Adding steps five and six will not help.
- **Replies but wrong-fit** — the ICP is wrong. See `icp-definition`.
- **Unsubscribes rising through the sequence** — too many steps, or the wrong audience.
- **Opens fall sharply after step one** — a deliverability signal, not a copy signal. See `email-deliverability`.

Benchmarks in `outbound-metrics-benchmarks`.

## Don't do these

- **Don't write "just following up".** It's the clearest signal that the email has no reason to exist.
- **Don't guilt.** "I've tried reaching you three times" makes it their fault for not answering a stranger.
- **Don't fake a reply thread** with "Re:" on a first email.
- **Don't run eight steps.** Diminishing returns, rising complaints.
- **Don't reuse the same sequence across segments.** The angle should differ by who it's for.
- **Don't let a follow-up go out after a reply.** Fix the automation, not the apology.

## Running it

The enforcement matters more than the writing. Reply detection, out-of-office handling, account-level stops, send windows and per-inbox caps all have to happen automatically, because at any volume nobody is watching.

[ManyPI](https://manypi.com) separates the sequence (the steps and timing) from the campaign (which inbox, which window, which limits), so one sequence can run across brands and inboxes without being rewritten. The scheduler checks the send window, the warmup-aware inbox cap, the campaign limit, suppression status and reply state before every send, and cancels remaining steps the moment a lead replies. Over MCP:

```bash
claude mcp add --transport http manypi https://mcp.manypi.com/mcp -s user
```

## Related skills

`cold-email-copywriting`, `subject-line-optimization`, `personalization-at-scale`, `outbound-campaign-ops`, `reply-handling`, `outbound-metrics-benchmarks`
