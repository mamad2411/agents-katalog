---
name: brand-voice
description: "Use when writing or rewriting any external-facing copy in the owner's voice: email, social post, deck section, proposal, cold outreach, landing page, tagline, workshop title; or on \"in my voice\", \"sound like me\", \"make this human\", \"less AI\", \"spicier\". Also captures the voice profile from the owner's own writing (`capture`). Language-agnostic; runs `/founder-pipeline:humanize` as its base layer."
allowed-tools: Read, Grep, Glob, Write
argument-hint: "[what to write, paste to rewrite, or \"capture\" to build the voice profile]"
---

# Brand Voice

> **Model floor: your top-tier model.** Reader-facing copy is where model tiers separate — cheaper
> tiers produce rule-compliant but AI-smooth output. If this is running in a lower-tier session,
> say so before delivering. When dispatching this work to an agent, set the agent to your top tier.
> Name a **tier**, never a model codename: codenames age out, the floor has to outlive them.

This skill has two modes.

- **Capture** — build `brand_context/voice-profile.md` from the owner's own writing. Run once, then
  refresh when the voice drifts or a new channel appears. Start here if no profile exists.
- **Apply** — write or rewrite copy against that profile. This is the default mode.

## Step 0: mandatory base layer

**REQUIRED SUB-SKILL:** invoke `/founder-pipeline:humanize` first and apply its FULL ruleset. A draft
that fails humanize fails brand-voice. Humanize removes the machine; this skill adds the person.
Neither substitutes for the other.

---

# Mode A — Capture the voice

The profile is only as good as the corpus. Most bad voice profiles are built from the wrong material.

## What to collect

**Collect the owner's own sent writing. Not their marketing copy.**

Marketing copy — the website, the brochure, the launch email — was usually shaped by an agency, a
copywriter, a template, or a model. It records somebody else's house style. Sent mail, DMs, chat
messages, and hand-written posts record how this person actually sounds when they want something
from a reader.

| Collect | Exclude |
|---|---|
| Sent email the owner typed themselves | Anything AI-drafted or AI-edited — if unsure, exclude it |
| DMs and chat messages to peers, partners, customers | Ghostwritten posts, agency-written pages |
| Hand-written blog posts or social posts they can vouch for | Legal, HR and templated transactional copy |
| Talk scripts and voice-memo transcripts | Anything older than the current positioning, unless flagged as historical |

**Volume:** 10–15 samples is enough to see the pattern; below 8 you will over-fit to one mood. Spread
them over time rather than taking a single week.

**Coverage rules:**
- At least 3 samples per language the owner publishes in.
- At least 2 samples carrying a *hard* message — bad news, a chase, a boundary, a refusal. Register
  shows itself under pressure; a corpus of cheerful announcements teaches nothing.
- At least one two-line reply. Short messages reveal the default; long ones reveal the effort mode.
- One sample per channel the profile will govern. A channel with no sample gets no rules — say so in
  the profile rather than guessing.

## What to extract from each sample

Go through the corpus once per row, not once per sample — you are looking for what repeats.

1. **Greeting form**, per language and per relationship. Exact punctuation and word order.
2. **The job of line 1** — does it anchor on a shared moment, state the ask, or set context?
3. **Length**: median message length, and the spread. Note the shortest complete message.
4. **Unit of thought** — one idea per line, or built paragraphs?
5. **Ask count** per message, and how the ask is phrased.
6. **Proof density** — how many numbers appear, and whether proof is stated or linked.
7. **Link behaviour** — bare URLs inline, anchored text, or links at the end?
8. **Close and sign-off** — the exact strings, with their frequency.
9. **Emoji** — which ones, how many, in what positions.
10. **Contraction rate**, formality, and any consistent grammar habits (including non-native
    constructions the author reliably produces — those belong in the fingerprint, see
    `/founder-pipeline:humanize`).
11. **Punctuation and typography** habits, per language.
12. **Recurring phrases, verbatim.** Quote them. Paraphrased signature phrases are worthless.
13. **What never appears.** The absences are half the profile: no pleasantries, no hedges, no
    exclamation marks, whatever it is. Absences are what most AI drafts violate first.

Then write `brand_context/voice-profile.md` from the template below, and get the owner to correct it.
Their corrections are the highest-value data in the whole exercise — log the ones that change a rule.

## The voice-profile template

Copy this into `brand_context/voice-profile.md` and fill it in. Every row needs evidence from the
corpus; a row you cannot evidence is a guess and should be left empty.

```markdown
# Voice profile — <brand or person>

Built <date> from <N> hand-written samples (<channels>, <languages>). AI-assisted material excluded.

## Identity contrasts

| <Brand> IS | <Brand> IS NOT |
|---|---|
| <trait> — <evidence from the corpus> | <the near-miss it gets confused with> |
| ... | ... |

Five to eight rows. Each row is a *contrast*, not an adjective: the right-hand column is the thing a
competent writer would produce if they missed by one degree. "Warm through specifics" vs "warm
through phrases" is a usable row; "authentic" vs "fake" is not.

## Banned words

| Word / phrase | Why | Set by |
|---|---|---|
| <word> | <the reason, in one line> | <owner / audit / channel policy> |

Owner-specific bans only. Generic AI vocabulary lives in the humanize skill's
`references/forbidden-words.md` — do not duplicate it here.
Record the equivalent in every language the brand publishes in; a ban that only exists in English
leaks straight through the translation.

## Register per channel

| Channel | Register | Hard constraints |
|---|---|---|
| <channel> | <one line> | <e.g. one ask, no jargon, spell out numbers> |

Include the conservative override for regulated or C-level audiences if the brand has one.

## Signature constructions

Verbatim lines from the corpus, quoted exactly. This is the register bank — the drafting model
matches *these*, not a description of them. 6–12 lines, refreshed when the corpus is refreshed.

- "<line>"
- "<line>"

Also record: sentence shapes that repeat, the contrast connector of choice, how the author opens a
paragraph, how they end a piece.

## Language rules

Per language:
- Typography and diacritics, per channel (they often differ between email and web).
- Greeting word order and closers, exact strings.
- Which loanwords stay untranslated.
- Register drift: many languages have a drier professional register than English. Translating
  English enthusiasm literally is the fastest way to sound machine-made.
- What to do with mixed-language input.

## Grounding sources

Where verifiable specifics come from, so the model never invents one:
- Numbers: <the registry, database, or file — with how to read it>
- Terminology and product naming: <the glossary file>
- Stories, scars, positions: from the owner directly, never generated
- People and company names: exactly as given in the brief

## Budgets

- Proof numbers per email: <default 1>
- Asks per message: <default 1>
- Emoji per piece: <range>
- Formatting: <bold, lists, headers — what is allowed where>
```

---

# The portable principles

These hold regardless of whose profile is loaded. They survive a change of owner, brand and language.

**Lead with the reader's outcome, not your output.** Test: any sentence starting with "we / our /
the platform / the product" gets rewritten around the reader. In email the outcome can be a plain
imperative — "Build a network you can call on." A short imperative is not an AI tell; a benefit
paragraph about your own excellence is.

**Never invent. Ground every specific, or ask.** Numbers come from the registry named in the
profile, quoted in the form the registry gives them. Product terminology comes from the glossary.
Stories, scars and contrarian positions come from the owner — never write a story they did not live
or a position they have not confirmed. People's names appear exactly as the brief gives them: do not
add surnames, titles or roles you were not given, even when you believe you know them. If the
grounding source is silent, ask one question or drop the claim. Dropping it is usually cheaper.

**One proof number, maximum, in an email.** Stat-stacking reads as a pitch and gets skimmed. The
second number weakens the first. Dates, times and durations are facts, not proof — they don't count
against the budget. Decks and web pages have room for more; a message asking one person for one
thing does not.

**Links carry the proof.** Show the list, don't describe it. A URL where the reader can see the
speakers, the pricing, the roster or the schedule does more than three sentences summarising it —
and it cannot be accused of exaggerating.

**Logistics live on the landing page.** Date and city belong in the message; times, addresses,
parking and agenda belong behind the link. Every logistical line you keep pushes the ask further
down.

**One ask per message.** A second ask does not double the response rate, it halves the first.

**Clickbait test, everywhere.** If a line could open a content-mill listicle, rewrite it. Curiosity
gaps, "here's what nobody tells you", and cleverness-over-clarity subjects all fail.

**Self-check before delivery, every time.** The checklist at the end of this file is not optional
polish; it is the step that catches the drift that creeps in during drafting.

**Model tier floor.** See the top of this file.

---

# Mode B — Apply

## Default channel shape: email

Use this when the profile has no email section yet, and override it wherever the profile disagrees.
An email is these parts, in this order.

1. **Subject:** descriptive, front-loaded, period-separated fragments — what it is, when, what you
   get. Short noun phrases work too. No wordplay, no curiosity gap.
2. **Image slot** at the top, for invitations and announcements only.
3. **Greeting** in the profile's exact form for that language and relationship.
4. **Line 1 = anchor** — the last shared moment, or straight to the question. Never a pleasantry.
5. **Body: 3–8 short lines, one idea per line.** Bold the two or three words that carry the message.
   Numbered list for a recap or to mirror someone's numbered questions; bullets for an agenda.
6. **One proof number, maximum.**
7. **Links inline where the action is.**
8. **Logistics on the landing page.**
9. **Delegate in-thread by @-mention** when someone else owns the next step, naming their role.
10. **Close: imperative next step, benefit optional, then stop.** Sign-off from the profile's list;
    the signature block appends itself, so no ceremony.
11. **"We" for organisational operations, "I" for personal commitment.**
12. **Emoji within the profile's budget.** Zero is a legitimate default.
13. **Simple language by default.** Many readers are not native speakers of the language you are
    writing in. Short words, plain verbs, no idioms.

A reply can be two words and still be complete. When a full answer has to wait: acknowledge now, say
when.

Other channels take their shape from the profile's register table. Where a channel has no profile
row, ask rather than inventing one — and add the row afterwards.

## Workflow

1. Invoke `/founder-pipeline:humanize` and load its full ruleset.
2. Load `brand_context/voice-profile.md`. **Missing?** Say so in one line, offer Mode A, and
   meanwhile work from the portable principles above plus three questions to the owner: who is the
   reader, what is the one ask, what verifiable specific can we use.
3. Load the grounding sources the profile names. For email, pick at most one number.
4. Draft to the channel's shape, matching the register bank rather than describing it.
5. Run the self-check. Deliver the draft with no preamble.

## Self-check before delivery

**First: humanize's full self-verification (15/15).** Then each of these is zero, or fixed:

- grep every word in the profile's banned list, in every language present.
- grep categorical absolutes about people or outcomes (`never|every |always |nobody`) — replace with
  a probability word (most, usually, rarely, hard to) unless the absolute is literally verifiable: a
  cap, a contract term, a seat count. Verifiable absolutes stay.
- grep the terms the glossary forbids or renames.
- Any number, claim, or named person not traceable to a grounding source. Any story or position the
  owner has not confirmed.
- Any sentence about the product or offer that leads with "we / our / the platform" instead of the
  reader.
- **Email checks:** more than one proof number · more than one ask · body over ~10 lines · logistics
  the landing page owns · a clever-not-clear subject · a missing proof link · idioms or hard
  vocabulary · typography that breaks the profile's language rule · "I" where organisational
  operations mean "we" · emoji over budget.
- Signature phrases used only from the register bank, or supplied by the owner in this conversation.

If a check fails and fixing it would cost the meaning, deliver anyway and tell the owner which rule
you bent and why. Silent rule-bending is what erodes a profile.

---

# Calibration exercise: AI draft vs. your own edit

The single fastest way to find what a voice profile is missing. Run it when you build the profile,
then again whenever the copy starts drifting.

**How to run it**

1. Pick one message the owner wrote themselves and was happy with. An email works best — it has an
   ask, so the deltas are consequential.
2. Write the brief that message answered: reader, occasion, ask, the facts available. Nothing else.
3. Have a model draft the same message from that brief alone, **without seeing the original.**
4. Put the two side by side and list the deltas. Not "it's better" — what specifically changed:
   length, number of proof points, where the link went, what was cut entirely.
5. Every delta becomes a row: an identity contrast, a banned construction, or a budget.
6. Repeat with a second message in a different register. Two runs usually surface every major rule;
   the third rarely pays for itself.

The deltas that show up most often across owners: the human version is roughly half the length,
carries one number instead of four, replaces a described list with a link to it, drops the logistics
entirely, and closes with a plain imperative instead of a wedge.

## Fictional worked example

Invented brand, invented event, invented URLs. Use it as a demonstration of the *method*, not as
copy to imitate — your own run will produce different deltas.

**Brief:** Bellrock (fictional community for data-platform leads) is putting past speakers on a
harbour boat. Invite one member personally. Non-transferable seat. RSVP required and will be
approved.

**AI draft — kill this:**

> Subject: One seat for you at the Bellrock harbour evening, 14 May
>
> On 14 May we are bringing every past Bellrock speaker together on a boat in the harbour. 17:30 to
> 20:00, North Quay, Berth 4C. A regular meetup has 120+ people and you end up talking to whoever is
> standing next to you. This boat has 60 people, and every one of them has spoken at Bellrock. Since
> 2020, only 74 of our 2,900 members have done that. Partner companies hire from this room roughly
> twice a month.

**The owner's edit:**

> Subject: Private invite: Bellrock Harbour Evening. May 14th. Meet every past speaker.
>
> [image]
>
> Hi [First name],
>
> On 14 May we are putting every past Bellrock speaker on a boat in the harbour.
>
> No stage, no talks. Meet the 60 people who have spoken at Bellrock.
>
> See the full list and pick who you want to talk to: https://example.com/bellrock/speakers
>
> These are the people other data leads listen to.
>
> The seat is for you personally. Please don't send someone from your sales team.
>
> Ask for your seat here: https://example.com/bellrock/rsvp
>
> Every request needs approval. We will approve yours immediately.
>
> The boat holds 60. Build a network you can call on. Click today.

**Deltas, and the profile rows they produced:** descriptive subject over clever subject → identity
contrast row. Half the length → budget row. Four numbers down to one → proof-number budget. A link
to the speaker list instead of statistics about it → "links carry the proof". Logistics gone → they
live on the landing page. "We" for the organisation. Plain imperative close, then stop.
