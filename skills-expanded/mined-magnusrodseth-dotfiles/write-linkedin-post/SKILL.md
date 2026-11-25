---
name: write-linkedin-post
description: Draft a LinkedIn post as Magnus Rødseth. Asks what kind of post it is, then tunes hook, length and CTA to that type. Use for "write a LinkedIn post", "lag et LinkedIn-innlegg", "post this on LinkedIn", or turning a blog post, talk or shipped project into a post.
---

# Write a LinkedIn post

Draft a post that reads as Magnus wrote it and is shaped for the feed.

Two skills split the work. **[write-in-my-voice](../write-in-my-voice/SKILL.md)
owns sentence-level voice**: word choice, warmth, the hard bans, æ/ø/å. This skill
owns **post shape**: which archetype, the hook, the fold, length, emoji bullets,
the CTA and where the link goes. Read write-in-my-voice's Norwegian profile
before writing prose, and apply its hard bans with the one exception below.

## The one place this skill overrides write-in-my-voice

write-in-my-voice bans one-sentence dramatic paragraphs. **On LinkedIn they are
correct and expected.** Every post he has published opens on a standalone
one-sentence paragraph, the feed truncates at the fold, and white space is what
makes a post scannable on a phone. Single-sentence paragraphs are allowed
anywhere in a LinkedIn post.

Every other hard ban holds in full. No "det er ikke X, det er Y" reframes, no
hype words (revolusjonerende, game-changer, magisk), no inflated openings, never
🙏, no em dashes, a space before every emoji.

## Step 1 - ask, unless he already answered

Ask the three questions below in **one `AskUserQuestion` call**. Every option
carries "(Recommended)" on the one you are recommending, plus a one-line
justification in its description grounded in his real posts.

**Skip any question he has already answered in the prompt.** "kort teaser for
kode24-saken, lenke i kommentarfeltet" answers type, length and CTA. Do not ask
back what he just told you. If all three are answered, write.

For **Q1 you infer the likely type from what he gave you** and mark that one
Recommended, justified from his own input ("du beskriver noe du har bygget og
publisert, så dette er en byggpost"). Q2 and Q3 have stable defaults.

### Q1. Hva slags innlegg er dette? (header: `Post type`)

Present the 3-4 most plausible archetypes from
[references/post-types.md](references/post-types.md), never all five:

| Type | Trigger |
|---|---|
| **Bygg / ship** | He made, shipped or published a thing |
| **Arrangement** | Talk, conference, hackathon, meetup. Recap or promo |
| **Omtale** | Someone else published about him (kode24, podcast, press) |
| **Forklaring / nyhet** | He digested something so the reader does not have to |
| **Mening** | He has a take and wants to argue it |

The type decides hook, body shape, CTA and default length. Get it right before
writing a word.

### Q2. Hvor hardt skal kroken dra? (header: `Hook`)

All four are drawn from posts he actually published. None of them is clickbait,
because clickbait is hard-banned.

- **Understated result-first (Recommended by default)** - "Jeg har laget et lite
  verktøy for å snakke med banken min gjennom AI-agenter!" Justify it with the
  numbers: his two best-performing posts (15.8k and 13.5k impressions) both open
  understated. Deliberate smallness is his strongest signature.
- **Curiosity question** - "Hvor langt kan du egentlig ta Claude Fable på én
  dag?" Best for experiments where the answer is the payoff.
- **Flat opinion** - "Ærlig talt, de fleste AI-demoer du ser om dagen er litt
  meningsløse." Only for Mening posts, and only when he will defend it in the body.
- **News lead** - "Fellesferien er over, og den første fristen i EU AI Act som
  faktisk betyr noe for utviklere, er om under en uke." For Forklaring / nyhet,
  where the fact is the hook.

### Q3. Hvor langt? (header: `Length`)

- **Standard, ~150-300 ord (Recommended by default)** - his median and the shape
  of most of his best posts. Room for the story plus one concrete section.
- **Teaser, ~50-100 ord** - the "Ukas koder i Kode24" shape. Use when a link or a
  video does the real work and the post only has to earn the click.
- **Dyp gjennomgang, ~350-500 ord** - the EU AI Act shape. Emoji-bulleted
  sections, real standalone value, link at the end for those who want everything.
  Use when the post must be worth reading even if nobody clicks through.

## Step 2 - write it

Open [references/post-types.md](references/post-types.md) for the chosen
archetype and [references/linkedin-posts.md](references/linkedin-posts.md) for
the verbatim corpus. Mirror the corpus.

**Language: Norwegian.** All twelve of his own posts are Norwegian, including the
Eden Stack and Product Hunt launches aimed at an international audience. Write NO
unless he says otherwise. If the topic genuinely reads better in English (an
international launch, a devto crosspost, an English-speaking audience), say so in
one line after the draft and offer to switch. Never switch silently.

### Format rules the feed imposes

- **The fold.** LinkedIn truncates at roughly 210 characters on desktop and less
  on mobile, then shows "…mer". Everything that earns the click must sit above
  it. Never let the hook run past the first two short paragraphs.
- **No markdown.** LinkedIn strips `**bold**`, `*italics*`, `#` headers and `-`
  bullet lists. Write plain text. For emphasis use a line break; for lists use
  emoji or `→` as the bullet, one per line, as in the sb1 and Eden Stack posts.
- **Inline code is Unicode monospace, not backticks.** LinkedIn has no code
  formatting, so a command or filename in backticks shows up as literal
  backticks. Use the Mathematical Monospace block instead: 𝚟𝚌 𝚍𝚎𝚟, 𝙰𝙶𝙴𝙽𝚃𝚂.𝚖𝚍,
  𝚜𝚕𝚎𝚎𝚙(𝟷). Generate it with `python3 scripts/mono.py 'npx sandbox@latest sh'`
  and paste the output into the draft; never hand-type it. The full rule, with
  what gets it and what stays plain, is in
  [references/inline-code.md](references/inline-code.md).
- **Paragraphs are one to three sentences**, each separated by a blank line.
  Dense blocks do not get read on a phone.
- **Tag people in full.** Every event post names participants and says what each
  one specifically did or covered. This is warmth and it is also his reach
  mechanic, since tagged people surface the post to their networks.
- **Link placement.** Default is inline at the end on a `👉🏽` line
  ("👉🏽 Les hele gjennomgangen her: <url>"). Use "Lenke i kommentarfeltet 👇🏽"
  instead when the post stands on its own without the link and reach matters
  more than the click. State which one you chose so he can flip it.
- **Numbers early and exact.** 30 000 kr, 135 tester, halvannen til to timer,
  3 år. Never "massevis" where a real number exists.
- **No hashtags.** He does not use them. Do not introduce them.

### Voice moves specific to LinkedIn

- **Understatement.** "et lite verktøy", "et lite hobbyprosjekt jeg syns er litt
  gøy", "noe så glamorøst som ukeshandelen min". Shrink the thing, let the reader
  decide it is big.
- **Close on a question to the reader.** "Hvordan står det til hos dere?",
  "Kommer butikkene til å bygge for det, eller finner kundene sine egne veier dit
  først?", "Hva savner du innsikt i?"
- **Self-deprecating honesty near the end.** "Selvsagt ser den litt ræva ut, men
  det var et morsomt eksperiment.", "Litt flaut, men ærlig."
- **Plain disclaimers, never buried.** "Dette er et personlig og uoffisielt
  verktøy. Det er ikke laget av eller tilknyttet SpareBank 1."
- **Quote real people verbatim** when someone said something good, with the
  Norwegian quote marks he uses: «Helvete så addicting».
- **Emoji set**: 🕺🏽 🤠 🫶🏽 🚀 👉🏽 👇🏽 🤷 🔗. One or two per post plus the
  bullet emoji. Always a space before. Never 🙏.
- **Never invent** a number, a quote, an outcome or a person's reaction. If the
  post shape wants a specific he has not given you, ask him for it or leave a
  clearly marked gap. A fabricated detail on a public post is worse than a bland one.

## Step 3 - self-check

- [ ] Hook lands above the fold, roughly 210 characters, and is not inflated
- [ ] No markdown syntax anywhere. Emoji or `→` do the bullets
- [ ] Commands, flags, filenames and identifiers are in Unicode monospace via
      `scripts/mono.py`; product names, URLs and Norwegian words are plain
- [ ] No em dashes, no colon standing in for one, no "ikke X, men Y" reframe
- [ ] No hype words, no hashtags, never 🙏, space before every emoji
- [ ] æ/ø/å intact throughout
- [ ] Every number, quote and name comes from what he gave you
- [ ] People are tagged by full name with what they specifically did
- [ ] Post ends on either a question to the reader or a clear next step
- [ ] Length matches what he picked in Q3

## Step 4 - hand back

Return three things:

1. **The full draft**, ready to paste, plain text.
2. **Two alternative hooks**, each one a different Q2 mode from the one used, so
   he can see the post open a different way without rereading the body.
3. **A short note** covering the link placement you chose, anything you left as a
   gap for him to fill, and the language flag if English would serve the topic
   better.

If the post needs a first comment (link, credits, påmelding), draft that too.

## Refreshing the corpus

[references/linkedin-posts.md](references/linkedin-posts.md) is a snapshot taken
28.07.2026 via the `linkedin-mcp` skill, extended 26.08.2026. Refresh it when his style moves or after
a run of new posts, with `get_my_profile(sections="posts", max_scrolls=20)`.
Known issue: that call renders a partial feed (12 of 27 items on 28.07.2026,
items 1-5 and 13-29 on 26.08.2026) and silently skips a block in the middle, so
treat any single fetch as partial and add to the corpus rather than replacing it.
