---
name: campaign-creator
description: >
  Takes an approved content brief and executes a campaign end-to-end: builds the
  posting calendar, creates social-post visuals with claude.ai/design, drafts
  caption and email copy, and stages social sends in Clarify. Designs are
  generated in-session with claude.ai/design (Instagram, Facebook, X, LinkedIn);
  email content is drafted as plain text and surfaced inline for the owner to
  send from their own tool. Every step requires explicit owner approval. Use when
  the user says "make the content," "generate the posts," "create the assets,"
  "turn this into a campaign," or hands off an approved brief for execution.
---

# Campaign Creator

Turns an approved content brief into ready-to-schedule social posts and drafted
emails. Visuals are made with **claude.ai/design** — Claude designs each post in
the session from the brief and the owner's brand inputs. There is no external
design tool, template library, or asset-upload API: you describe and generate
the design directly, the owner reacts, you refine.

## Scope

Five sequential stages, each gated by owner approval:

```
brief → calendar → design (claude.ai/design) → copy → Clarify staging
```

| Path | Channels | What this skill produces |
|------|----------|--------------------------|
| Social | Instagram, Facebook, X/Twitter, LinkedIn | claude.ai/design visual + caption + scheduled Clarify post |
| Text-only | Email (newsletter, marketing, drip) | Subject + preheader + body, surfaced inline for the owner to send |

Email rows get **no visual** — email content is plain text the owner drops into their email tool. Don't generate designs for email rows.

## Pre-flight

Before Stage 1, confirm:

1. **Brief.** The user has referenced or pasted an approved brief. If not: "I'll need the content brief before I can build the campaign. Do you have one from the content-strategy skill, or would you like to write one now?"
2. **Brand inputs for the visuals.** Ask for what claude.ai/design should work from: product photos (file paths), brand colors (hex), logo, fonts or vibe. The owner can also say "just use my product photos and keep it clean" — capture whatever they give and proceed; claude.ai/design fills gaps tastefully rather than blocking.
3. **Clarify staging.** Social scheduling uses Clarify's `create-or-update-campaign`. If the owner doesn't want posts staged in Clarify, offer a CSV export instead (see `reference/clarify-staging.md`).

## Workflow

### Stage 1 — Posting calendar

Pull from the brief: content themes, channels, cadence, hard dates (launches, sales, holidays). Build a calendar table with a `Path` column routing every row to Social or Text-only:

| Date | Channel | Path | Theme | Caption/Subject angle |
|------|---------|------|-------|-----------------------|
| Jun 2 | Instagram feed | Social | Linen launch | "finally, a dress…" |
| Jun 5 | Email | Text-only | Linen launch | "Linen that actually breathes" |

Tag every email row `Text-only`. Cap at 30 days unless the brief says otherwise. Flag scheduling conflicts (two posts same day, same product) up front.

**Checkpoint 1.** Present the calendar. "Does this match the plan? Any dates to shift, channels to add, themes to swap?" Iterate until approved, then restate the split — "N social rows, M email rows" — before moving on.

### Stage 2 — Design the social posts (claude.ai/design)

For each `Social` row, one at a time:

1. **Compose the design brief for the post.** From the calendar row + brand inputs, decide the visual: the product/photo to feature, the headline text on the design, the channel's aspect ratio (Instagram feed 1:1 or 4:5, Stories 9:16, X/LinkedIn 16:9, Facebook 1:1), and the brand colors/vibe.
2. **Generate the design with claude.ai/design.** Produce the visual in-session. If the owner gave product photos, incorporate them; otherwise design around the brand colors and text. Default to 2–3 variations per post unless the owner wants one.
3. **Present and let the owner pick.** Show the variations for that row. "Which one for the Jun 9 post — or want me to adjust the colors/crop/headline?" Refine in place on request.
4. **Lock the pick, move to the next row.** Keep the chosen design's file reference for Stage 5 (attached to the Clarify post).

No rate limits, polling, asset IDs, or template selection — claude.ai/design generates directly. If a design comes back off (wrong product, unreadable text over a busy photo, wrong aspect ratio), regenerate that one with a corrected brief.

**Checkpoint 2.** Satisfied once the owner has picked one design per social row.

### Stage 3 — Copy drafting

Draft copy for each row. Social rows get a caption; email rows get a full email.

**Social captions** — Instagram, Facebook, X, LinkedIn:
- Length: channel-appropriate (Instagram ≤ 2,200; Facebook ≤ 500 recommended; X ≤ 280).
- Structure: hook → one product benefit → CTA → 3–5 hashtags (not 30).
- Voice: match the brief's tone markers. No filler — no "Exciting news!" or "We're thrilled to announce." Open with the value.

**Email content** — Claude writes the whole email; no visual:
- Subject: ≤ 50 chars, specific, no clickbait. "Spring projects are booking up" beats "Don't miss out!"
- Preheader: ≤ 90 chars, complements the subject.
- Body: plain prose, 100–250 words. Opening line that earns the read → 1–2 paragraphs of substance → single clear CTA → sign-off.
- Voice: same tone markers as social. No "see image above." One CTA per email.

Present captions inline below each social row; full emails inline below each email row:

```
Subject: <subject line>
Preheader: <preheader text>

<body text>
```

**Checkpoint 3.** "Any captions or emails to rewrite? Flag the date and what to change." Iterate until approved.

### Stage 4 — Clarify staging + email handoff

Stage social posts in Clarify; surface email content inline for the owner. See `reference/clarify-staging.md`.

1. **Create the campaign** with `create-or-update-campaign` (name + start/end dates from the calendar).
2. **Stage each social post** under the campaign: channel, scheduled datetime (confirm it's in the future), the approved caption, and the chosen claude.ai/design visual as the attachment. Stage as scheduled — never publish/send.
3. **Confirm the queue.** Show the scheduled list and link to the Clarify campaign view.
4. **Surface email content for handoff.** Present each approved email (subject + preheader + body) grouped by send date. The owner copies these into their email tool (Clarify email, Mailchimp, Gmail).

**Final checkpoint.**

```
Your social posts are scheduled in Clarify: [link]
You can cancel or edit any post in Clarify before it goes out.

Email content is drafted below — copy each into your email tool when ready:
  Jun 5 — "Spring projects are booking up"
  Jul 15 — "Summer maintenance windows are filling"

Anything to change before we're done?
```

## Approval gates

**Release Owner gate (high-stakes).** Before staging the scheduled campaign in Clarify, present the exact content and the recipient, amount, or target (the channels, the scheduled send times, and the segment each post reaches), then stop. Do not proceed until one named human approves with their initials and the date. Record the decision to the shared gate log: run `python3 "Taskade/_Shared Files/_gate-log/record_decision.py" --skill frontier-founder-smb:campaign-creator --tier high-stakes --action "<summary>" --target "<recipient/amount/target>" --decision signed|stopped|overridden|edited --approver "<named human>" --requested-at <ISO-8601>` (one row per decision; never edit past rows). Roll up override rate and response time anytime with `override_report.py`. Never auto-approve, and never sign on the owner's behalf. Watch the override rate over time; a low override rate signals rubber-stamping.

- **No designs for email rows.** Re-check the `Path` column before generating.
- **No publishing/sending.** Every Clarify post is staged, not sent; the owner controls go-live.
- **One social row at a time in Stage 2.** Present, get the pick, then the next row.
- **Never skip Checkpoint 1.** Generating before the calendar is approved is the biggest source of wasted work.
- **Regenerate, don't ship, an off design.** Wrong product, unreadable text, or wrong aspect ratio gets a corrected regeneration.

## Reference

- [reference/clarify-staging.md](reference/clarify-staging.md) — Clarify campaign staging (`create-or-update-campaign`) and CSV fallback
- [reference/gotchas.md](reference/gotchas.md) — Good / Bad patterns for campaign execution
