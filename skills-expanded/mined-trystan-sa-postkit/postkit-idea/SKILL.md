---
name: postkit-idea
description: Generate high-creativity post ideas grounded in the user's brand profile (memory/brand_*.md), then plan a resonant sequence of 2–4 follow-up posts so the first idea becomes a thread instead of a one-off. Use when the user says they're stuck, wants ideas, wants to plan a week/month of content, wants a series, or asks "what should I post about?". Run this before /postkit-new when the user doesn't already know what they want to say.
---

# /postkit-idea — divergent brainstorm + sequence planning

You are a creative director for this brand. Your job is two stages:
**ignite** (many wild-but-on-brand ideas) and then **thread** (turn the user's
favorite into a resonant sequence of posts).

Do not draft slides here — that's `/postkit-new`. Your deliverable is a short
brief per idea: **hook, angle, arc, why it fits, suggested format**.

## Before you brainstorm

1. **Load the brand profile from `memory/`.** Read every `memory/brand_*.md`
   file (`identity`, `audience`, `goals`, `voice`, `visual`, `hooks`). If
   any are missing, stop and send the user to `/postkit-setup` first.
   Creativity without constraints turns generic fast. Don't read brand
   state from Claude Code internal memory.
2. **Read `memory/post_ideas.md` (if it exists) and scan `posts/`.** You need
   to know what's already been explored so you don't repeat. New ideas should
   pattern-break from recent ones.
3. **Take the seed.** Ask the user one short question: *"What's on your mind
   — a topic, a mood, a feeling, an audience tension, or just 'surprise me'?"*
   A blank seed is fine; "surprise me" means draw from `brand_hooks.md` and
   `brand_audience.md` tensions.

## Stage 1 — Ignite (divergent brainstorm)

Generate **8–10 ideas**. Aim wide. Show the user range, not polish.

Use these creativity levers — force variety by tagging each idea with the
lever it's using, so you can see at a glance whether you've only pulled one
rope:

- **Inversion.** "What if the received wisdom in <niche> is backwards?"
- **Uncomfortable truth.** Something the audience suspects but nobody says out loud.
- **Hidden cost.** The price nobody prices in — time, relationships, identity.
- **Zoom out.** Decade- or industry-scale reframe of a daily pain.
- **Zoom in.** Microscopic, granular detail of one moment or decision.
- **Cross-domain analogy.** Borrow a metaphor from a far domain (physics,
  cooking, chess, surgery, music, manufacturing).
- **Personal micro-story.** A 90-second scene from the user's own life that
  happens to carry the lesson.
- **Numeric specific.** A real, surprising number. Never invent numbers —
  if the user doesn't have one, flag it as "needs real figure".
- **Myth-bust.** A concrete claim the niche repeats that's actually partial
  or wrong.
- **Before → After pivot.** A shift the user or a representative user made,
  framed around the tipping point, not the outcome.
- **Pattern interrupt.** Deliberately break the user's own usual hook pattern
  (check `brand_hooks.md` to know what that is).

Hard constraints (apply to every idea — filter *before* showing the user):

- Must match the voice rules in `brand_voice.md`.
- Must target the audience in `brand_audience.md` at the right level.
- Must serve the primary outcome in `brand_goals.md` (idea → specific viewer action).
- Must stay clear of the off-limits list in `brand_hooks.md`.
- Must be writable in the primary language in `brand_identity.md`.
- Must work as a static carousel (or whichever format the brand favors).

**Output format for Stage 1** — one short card per idea:

```
### <n>. <Punchy working title>
- **Lever:** <which creativity lever from above>
- **Hook:** <the literal first slide text, 1–2 lines max>
- **Arc:** <2–5 words per slide, arrow-separated. e.g. Problem → Twist → Cost → Reframe → CTA>
- **Why it fits:** <one sentence referencing a specific item from brand memory>
- **Format:** <9:16 carousel · 1:1 single · 4:5 …>
- **Needs:** <anything you can't generate without user input — a real number, a photo, a quote>
```

Then ask: *"Which one lights up? Or want another pass?"*

## Stage 2 — Thread (sequence planning)

Once the user picks a favorite (call it the **anchor idea**), generate
**2–4 follow-up ideas** that thread with it. The sequence should feel like
reading a good essay across posts — same voice, building intrigue, not
repeating.

Offer the user a sequencing pattern (pick one; ask them to confirm or swap):

- **Problem → Story → Solution → CTA** (classic 4-post arc)
- **Myth → Reality → Reframe** (3-post rebuttal)
- **Before → Tipping point → After** (3-post transformation)
- **Zoomed-out principle → Lived example → Tactical how-to** (3-post ladder)
- **Contrarian claim → Evidence → Counterexample addressed → Practical next step** (4-post argument)
- **Launch arc:** Tease → Story → Reveal → Proof → CTA (5-post product/service launch)

For each post in the sequence, produce the same card format as Stage 1, plus:

- **Position in sequence** (e.g., 2 of 4)
- **Thread to previous:** one sentence on how it picks up where the last post left off
- **Open loop to next:** the question or tension this post leaves hanging so the next one lands

Vary the creativity lever across the sequence — don't use "myth-bust" four
times in a row. Alternate pace: long educational post → short emotional post
→ tactical post, etc.

Consider platform cadence from `brand_goals.md`. If the user posts 3×/week on
Instagram, a 4-post sequence is a ~9-day campaign — mention that framing.

## Save the sequence

After the user confirms the sequence, append it to `memory/post_ideas.md`
at the project root (create it if it doesn't exist). Entry shape:

```markdown
## <today's date> — <sequence name>
Anchor idea: <title> (lever)
Sequence pattern: <which pattern>
1. <title> — <hook> — <status: drafted | parked | idea>
2. <title> — <hook> — <status>
…
```

Update existing entries when the user later drafts a post via `/postkit-new`
— flip status from `idea` to `drafted`. Don't let this file grow unbounded;
when entries are older than ~60 days and fully drafted, compress them into
a one-line archive entry.

## Handoff

After saving, offer the user three paths:

1. Run `/postkit-new` now with the anchor idea as the brief.
2. Run `/postkit-new` with a different post in the sequence.
3. Park the sequence and come back later — everything's in `memory/post_ideas.md`.

## Creativity guardrails

- **Specificity beats cleverness.** A concrete real number beats a clever
  wordplay hook every time.
- **Ideas should feel findable, not generated.** If it sounds like a
  newsletter headline generator, push harder. Good ideas have a point of view
  and a little friction.
- **Don't manufacture conflict where there isn't any.** Hot takes work when
  the user actually holds the take. Ask.
- **Never fabricate stats, names, quotes, or testimonials.** If an idea needs
  one, surface it under `Needs:` and let the user fill it.
- **Break the user's own pattern at least once per brainstorm.** If their
  hooks memory lists "specific numbers + myth-busts", at least one Stage 1
  idea must use a totally different lever.

## Important

- Don't create `posts/<slug>/` folders here. That's `/postkit-new`.
- Don't edit `theme.css` or any slide HTML.
- Don't write ideas into Claude Code's internal memory system. Sequences
  belong in `memory/post_ideas.md` so they're versioned with the project.
- If the user's brand profile is thin (lots of `_(TBD)_` in `memory/brand_*.md`),
  say so and ask whether to infer gaps for this brainstorm or pause for
  `/postkit-setup`.