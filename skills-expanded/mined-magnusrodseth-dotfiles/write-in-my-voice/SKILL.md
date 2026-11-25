---
name: write-in-my-voice
description: Draft or rewrite text in Magnus Rødseth's own voice, in Norwegian or English. Use when Magnus asks to write, draft, reply to, or rewrite a message, email, LinkedIn DM, post, outreach, testimonial, or blog post / article "in my voice", "as me", "how I'd say it", "sound like me", or wants AI-drafted text to read as if he wrote it. Auto-selects language and register (casual DM, professional email, or long-form blog post).
---

# Write in my voice

Make text read as if Magnus wrote it himself, not as if an AI drafted it for him.
The voice was distilled from his real sent LinkedIn DMs, emails, and published
blog posts (DMs/emails: EN + NO; blog: NO).

Invoke `writing-whip` with the Skill tool before drafting (in Codex or Zed,
read [../writing-whip/SKILL.md](../writing-whip/SKILL.md) instead). It bans the
generation-time behaviours (preamble, premise stacking, tie-back, self-answered
questions, invented concept labels) that no voice profile repairs afterwards.
The Hard bans below overlap it on purpose; where the two disagree, the
exceptions listed under "Working with the neighbouring skills" win. After the
draft, invoke `humanize` on it with the narrow scope given there.

## When this fires

Drafting or rewriting anything outward-facing in first person: emails, LinkedIn
DMs, social posts, cold outreach, replies, testimonials, intros, and blog posts /
long-form articles. If the language or register is unstated, infer it (see below)
and say which you picked.

**LinkedIn feed posts go to
[write-linkedin-post](../write-linkedin-post/SKILL.md) instead.** That skill owns
post shape (archetype, hook, the fold, emoji bullets, CTA, link placement) and
reads this file for sentence-level voice. It carries the one sanctioned exception
to the hard bans below, since one-sentence paragraphs are correct on LinkedIn and
appear in every post he has published. LinkedIn *DMs* stay here.

## Hard bans - apply to EVERY register

These override the verbatim samples. The samples are real and some of them break
these rules (older writing); the rules win. Going forward, never:

- **"It's not X, it's Y" reframes.** Banned in all communication, personal and
  blog. Covers every form: "ikke X, men Y", "det er ikke X, det er Y",
  "ikke en mur; det er en nedtelling", "not a pitch, it's a tip", and the punchy
  two-clause aphorisms that wear the same setup-payoff cadence
  ("Du legger skinnene; agenten kjører på dem"). If you catch this rhythm, rewrite
  it as a plain statement.
- **One-sentence dramatic paragraphs.** No standalone one-liner paragraphs for
  effect ("Nei. Ikke godt nok."). Paragraphs carry at least two sentences.
- **Over-styled metaphor catchphrases** like "nådeløs redaktør". Say it plainly.
- **Hype words**: revolusjonerende, game-changer, magisk (and EN: revolutionary,
  game-changer, magical, "changes everything"). His own blog docs forbid these.
- **Clickbait / inflated openings** ("Barrieren for å skrive kode har kollapset").
  The hook must fit what the piece is actually about; result-first and concrete
  beats grand claims.
- **The pray emoji 🙏 (any skin tone, e.g. 🙏🏽).** Never use it in any message or
  register. If a thank-you or please-feel reads like it wants it, say it in words
  instead ("takk", "setter pris på det", "thanks").

Conditional (not banned, but use with judgement):
- **Rule-of-three**: only when there are genuinely three real points. Never as
  rhythmic filler.
- **Confident intensifiers** (fundamental, enorm, fantastisk, kraftig, robust):
  sparingly. Watch density; don't stack them.
- **Negative parallelism** beyond the hard-banned form: leans not-allowed. When
  in doubt, state it straight.

## Step 1 - pick language + register

| Signal | Language |
|---|---|
| Recipient is Norwegian / thread is in NO / Magnus wrote the prompt in NO | **Norwegian** (his default, most natural register) |
| Recipient is non-Norwegian, or it's product/marketing/cold outreach in English | **English** |

| Register | Use for | Feel |
|---|---|---|
| **Casual** | DMs, friends, warm/known contacts, partner/family | Emoji-forward, "Halla/Hei, [Name]!", playful, code-switched |
| **Professional** | New contacts, cold outreach, formal email, editors/publications | Crisp, structured, light-to-no emoji, fixed identity line in EN |
| **Long-form / blog** | Blog posts, articles, leserinnlegg, technical write-ups | Teacherly, opinionated, no flattery, **no greeting/sign-off, emoji-free prose**. See profile |

Then open the matching profile and **mirror the verbatim samples** (subject to the
Hard bans above):
- Norwegian → [references/voice-norwegian.md](references/voice-norwegian.md)
- English → [references/voice-english.md](references/voice-english.md)
- Blog / long-form (NO) → [references/voice-blog.md](references/voice-blog.md)

## Step 2 - apply the shared rules (both languages)

These hold regardless of language:

- **Warmth + directness together.** State the real thing plainly (salary, notice
  period, a no, a constraint) but cushion it with genuine warmth and specific
  compliments. Never cold, never over-apologetic.
- **Short sentences, tight rhythm.** Mostly 1-3 sentence messages; short
  paragraphs (2-4 sentences) in long-form. A colon earns its place only before a
  genuine list or a quotation. No aphoristic reframes (see Hard bans), no
  appositive "X: Y" punchlines, and never as the stand-in for a banned em dash -
  write the full sentence instead. Watch colon density across a piece, and never
  repeat a labeled opener as section scaffolding ("Regelen: ..." section after
  section).
- **Don't echo the incoming message back.** In a reply, cut clauses that just
  restate or paraphrase what the other person said - acknowledgment padding like
  "supert at [X] blir med", "jeg skjønner at det er travelt", "great that you can
  join", "I understand it's busy". Acknowledge in a few words ("Høres topp ut!",
  "Gøy å høre!") and move straight to substance or the next action. Mirroring
  earns its place only when it engages with a specific idea that genuinely
  resonated (the meaty content), never the logistics or pleasantries. Test each
  clause: if it only tells the recipient something they already know, delete it.
- **Greet only when you open contact.** A greeting ("Hei Kasper,", "Hi Sara!")
  belongs on the first message in a thread, on your first reply to it, on a
  reply after a pause of several days, and when someone new joins. In a
  running thread, open on the substance: "Ja, det passer fint.", "Takk!
  Torsdag funker." Mirror the other person: once they drop the greeting,
  drop it too. The sign-off follows the same rule; in a quick back-and-forth
  it shrinks to the name or goes.
- **Honesty framing.** Recurring tells: "Jeg skal være ærlig på at...", "med
  åpne kort", "my honest view is this", "to be clear".
- **Hand the next move to the recipient.** Almost every message closes with an
  action handoff: "Si gjerne fra hvis...", "Let me know if...", "Don't hesitate
  to reach out". A proposed concrete time/place counts.
- **Low-pressure signals** when appropriate: "Ingen hast", "No rush", "Det
  haster ikke fra min side".
- **Never em dashes.** For asides use a spaced hyphen " - " or restructure. Do
  not promote a colon into the em dash's old job; prefer the full sentence.
- **Space before every emoji.** Always separate the emoji from the text with a
  space: "uklart 😊", never "uklart😊". Applies to any emoji in any register.
  Older verbatim samples jam the emoji onto the last word; this rule wins.
- **Code-switch naturally.** Keep English tech/product terms in English inside
  Norwegian prose ("shippe en fix", "background jobs", "agentisk handel").
- **Correct æ/ø/å, always.** Never ASCII-degrade to ae/o/a.

## Step 3 - self-check before presenting

- [ ] **No hard-ban violations**: no "it's not X, it's Y" reframe anywhere, no
      one-sentence dramatic paragraphs, no hype words, no clickbait opening
- [ ] Greeting/sign-off matches the register and the thread position (running thread: open on the substance; long-form: none - open on the hook, close on a resource list + bio line)
- [ ] Emoji density fits register (heavy in NO casual, near-zero in EN professional, **none in blog prose**), every emoji has a space before it ("for tiden 😊", never "for tiden😊"); **never the pray emoji 🙏 / 🙏🏽**
- [ ] No em dashes, and no colons doing em-dash work (genuine lists and quotations only, density low); æ/ø/å intact; any triad is three real points, not filler
- [ ] Messages end by handing the next step to the recipient
- [ ] No echo padding: the reply doesn't restate the other person's logistics or pleasantries back to them
- [ ] Reads like the samples, not like generic AI politeness (no "I hope this email finds you well", no "delve")
- [ ] **Long-form only: no voice drift.** In a long piece the draft slides back toward generic prose as it goes, so the tail reads blander than the opening. Sentences lengthen, edges round off, the teacherly stance flattens into summary. Re-read the last third against the samples specifically, not just the first paragraphs. The voice has to hold as strongly at the closing resource list as at the hook.

When unsure between two phrasings, prefer the plainer one, then the one closer to
a verbatim sample. Don't invent catchphrases.

## Working with the neighbouring skills

Three skills form one pipeline for prose in his name: `/writing-whip` governs
generation, this file adds his voice on top, and `/humanize` is the edit-time
pass over the result. Invoke both with the Skill tool as part of this workflow
(Codex and Zed: read their SKILL.md files). The whip is loaded first and stays
in force throughout.
Its rules yield only to the voice profile on the points this file names
explicitly: a rule of three with three real points, a genuine rhetorical
question, second-person "du", parenthetical glosses of English terms, his
sparing confident intensifiers, and one-sentence paragraphs on LinkedIn (owned
by write-linkedin-post). Everything else in the whip applies unchanged.

His prose already passes the highest-signal AI tests (no em dashes, none of the
English slop vocab). So run `/humanize` on his text **narrowly**: apply its em-dash, **emphatic-colon**,
slop-vocabulary, didactic-disclaimer, and **clustered negative-parallelism** fixes,
but do **not** let it strip his genuine voice: rule-of-three (when real),
rhetorical questions, second-person "du" address, parenthetical glosses of English
terms, or his sparing confident intensifiers. Two places the two skills fully
agree: kill "it's not X, it's Y", and kill colons doing em-dash work. Humanize
scans for the emphatic colon on every pass, narrow or not.
