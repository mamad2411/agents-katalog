---
name: character-card-author-en
description: Author roleplay character cards for English-speaking communities (SillyTavern chara_card_v2/v3 compatible), with conventions calibrated on Western community evidence — a 30-card sample of top-starred SFW cards from a major community card hub, the rentry-era guide canon (Ali:Chat, PLists, pixi, Sukino), and platform docs (SillyTavern, JanitorAI, Chub). Sister skill of character-card-author (the Chinese-native skill in this repo): the method skeleton is shared, but length bands, formats, slop lexicon, naming, POV rules and compliance traps are English-native, not translated. Use when the user says "write an English character card", "make a card for SillyTavern/JanitorAI-style audiences", or "make this card read Western, not translated". Scorer: tools/score_card_en.py. Example cards: cards/en/.
---

# Character Card Authoring, English-Native (character-card-author-en)

> Use this skill when the card's audience reads English. For Chinese-audience cards use `character-card-author` (its `SKILL.en.md` is a translated mirror of the Chinese methodology — that is a different thing from this skill, which is English-*native*: recalibrated against what English-speaking communities actually publish and reward).
>
> Why a separate skill exists: we wrote three English cards with the Chinese methodology first (they remain in `cards/en/` — Rosalind, Caleb, The Lighthouse — as an honest contrast group). They are not bad cards, but they carry Chinese engineering habits: ~700-word greetings against a community median of ~180, heavy status-panel instincts against a community that ships zero rich HTML, numeric affection ladders against a community that writes warmth as observable behavior. Translating a discipline is not the same as re-deriving it from local evidence. This skill is the re-derivation.

Fact baseline (from a 30-card sample of top-starred SFW English cards on a major community card hub, July 2026, cross-checked against community guides; don't invent a different baseline):

- Hot-card **first messages run a median of 178.5 words** (P25=123 / P75=219 / observed max 529; a 40-word self-intro also charted). "Greeting length = reply length" is ecosystem consensus (SillyTavern docs: the model picks up style and length from the first message more than from anything else). Write the greeting as long as you want the replies to be.
- **0 of 30 cards use rich HTML** (div/CSS/img). There is no status-bar/collapsible-panel culture in Western cards; format = prose + `*asterisk actions*` (70%) or pure novel prose (30%) + "quoted dialogue". RPG/simulator cards use **plain-text code fences or bracketed key-value lines** (17%), never HTML.
- Description mainstream is **plain prose (67%)**; key-value attribute lists (PList family, no brackets) 13% and prose/list hybrids 7% are a legitimate minority — their niche is *prose for personality, lists for inventories* (appearance, clothing, skills). W++ survives only in 2023-era legacy cards. Strict bracketed PLists, JSON, or interview-format main definitions: 0 of 30.
- **Permanent tokens (description + personality + scenario): target 800–1500, red line 2000.** JanitorAI's two official tutorials cap at 2k/2.5k; pixi says 500–1000; the sampled cards' full-card median is 1085 tokens. Token budgeting is an English-side hard constraint with no Chinese-side equivalent.
- **"Don't speak or act for {{user}}" is the single strongest quality norm in Western communities** (JanitorAI official help calls it users' most common and most hated complaint; 25 of 30 sampled cards observe it strictly). A user action/line/thought in a greeting = auto-fail. The only folk exemption: RPG/isekai openers may do one **passive-perception hand-off** ("You wake up…") — scene only, never decisions or dialogue.
- **Lorebooks are not standard equipment** in these communities (6 of 30 cards carry one; 5 of those are RPG/scenario cards). Modern contexts are large; a lorebook's residual value is conditional reveal (secrets, plot switches) and organization. This repo's house standard is still 4–10 entries per card — deliberately above the community baseline — but don't transplant the Chinese 8–15-constant-entries pattern.
- Example dialogs are **mainstream equipment (70% usage; `<START>` grouping is the de facto standard)**: light-verbal-tic cards use 2–4 groups, heavy-tic cards use double digits (including char-only monologue groups that lock speech habits). "Lock voice with samples, not adjectives."
- Alternate greetings: 40% of cards carry them (mean 1.9), and cards that do treat them as a selling point ("20 Greetings!" in taglines). Either give none, or give 2–4 production-grade different *situations*. House standard here: always 2–4.
- Audience structure: the largest English RP platforms skew heavily female (roughly 70–80% on the biggest one); the content gravity is BookTok-style romantasy tension, all of it expressible SFW. **AnyPOV is default politeness.** Supply-side, female characters outnumber male roughly 23:5 in the sample.

## 0. First step: audience x genre x trope x POV

Write a one-line positioning note (**frontmatter comment only — never in Creator Notes**; product words in author notes are an instant tell). Four axes:

- **Audience quadrant** (pick one): `fem-audience` (male love interest, female gaze) / `male-audience` / `all-audience` (companionship, adventure, ensemble).
- **Genre** (pick one): fantasy / modern / campus (**university only, everyone adult**) / sci-fi / historical-flavored (invented history; avoid real sensitive periods) / supernatural.
- **Tropes** (1–3, in the audience's own search language):
  - Safe zone (SFW-ready): `enemies-to-lovers` (keep the conflict heat controlled) · `slow-burn` · `hurt/comfort` · `found-family` · `grumpy-x-sunshine` · `forced-proximity` · `fake-dating` · `friends-to-lovers` · `second-chance` · `royalty` · `arranged-marriage` (soften the power gap) · `rivals` · `cozy` · `mentor`.
  - Conditional (de-darkened): `yandere` = in Western SFW usage, "possessively devoted"; stay away from stalking/confinement depiction. `morally-gray`. `tsundere` (avoid the bully variant).
  - Off the table for SFW cards: omegaverse/A/B/O (the system itself carries heat-cycle semantics), dark romance (dubcon/captive), Dead Dove categories, anything minor-coded.
- **POV**: default `anypov` (user's gender unanchored; pronoun engineering in §2.3); `fempov` / `malepov` only when explicitly tagged. A POV tag in `tags` is mandatory.

Hard compliance screens (before any creativity): **zero real celebrities; zero recognizable IP** (rename test: mask every proper noun — if the setting is still identifiable as a specific franchise, rewrite). No therapist/psychologist naming or clinical claims (comfort cards use listener/companion framing). Everyone adult, in appearance, behavior and setup.

Character naming: avoid **naming slop** — the model-fixated names that read as AI on sight (the Antislop paper measured "Elara" at 85,513x over the human baseline): Elara, Kael, Seraphina, Lyra, Aria, Silas-the-mysterious, Sarah Chen. Naming method: anchor in a real language culture (Irish, Polish, Nigerian, Welsh surnames…) or coin something, then search the name to confirm no major IP collision.

## 1. Card file structure

Write `cards/en/<slug>/card.md` (or any working directory). Format spec: [`docs/card-md-format.md`](../../docs/card-md-format.md); converter: `tools/card_md_to_st.py` (md → chara_card_v2 JSON + v3 PNG).

```
---
# positioning: fem-audience / fantasy / enemies-to-lovers + forced-proximity / anypov  (comment line)
name: Character Name
license: CC-BY-4.0
scenario: One always-true sentence (no temporary states — see §2.4)
system_prompt: <six segments, §2.5>
tags: [fem-audience, fantasy, enemies-to-lovers, slow-burn, anypov, single-character]
image_prompt: <cover skeleton, §5>
creator: your signature
character_version: "1.0"
---

## Description        <- labeled prose (§2.1)
## Personality        <- scene-based behavior + language fingerprint (§2.2)
## Scenario           <- always-true one-liner
## First Message      <- §3
## Alternate Greeting 1 / 2 …   <- house standard 2–4
## Example Dialogue   <- voice weapon (§4)
## Lorebook           <- 4–10 entries (§4.5)
## Creator Notes      <- §6
```

Whole card in English (lorebook and Creator Notes included). Tags lowercase-hyphenated (the community's search language).

## 2. Persona and play rules

### 2.1 Description: prose as the body, labels as the frame

Evidence: pure prose 67% mainstream; key-value lists a legitimate 13% minority whose division of labor is "prose for personality, lists for inventories". House style hybridizes the two — **labeled sections with natural-prose values**: under each label, complete prose sentences, not semicolon inventories. Personality, relationships and history must be prose; only enumerable info (appearance, dress) may go listy. No W++ pseudocode, no bracket parameter piles, no `trait("a"+"b")` syntax:

```
[<Name>]
Identity: one sentence of who + age + how they make rent.
Appearance: paintable specifics (asymmetries / scars / dominant hand / the object never taken off). No empty "beautiful/handsome".
Voice: register + the physical side of how they talk (low, level, carries without rising…).
Dress: specific garments worn specific ways. Clothing is characterization.
Habits: 2–3 quirks, at least 1 of them "useless" (serves no plot function — see §7 anti-uniformity).
Temperament: personality as situations ("in scene X, does Y"), not adjective labels.
Toward {{user}}: the relationship's close-up + current tension (one piece of say-one-thing-do-another evidence welcome).
History: where they came from (a causal chain — explain why the personality grew this shape; a model with causes can extrapolate behavior in new scenes).
```

Discipline:

- **Description carries facts; the prose flair goes in the greeting and examples** (community iron law: "the prose goes in example dialogue and the greeting"). Fancy adjectives in the description waste tokens *and* teach the model the wrong style.
- **Permanent budget**: Description + Personality + Scenario at 800–1500 tokens (≈600–1100 English words); over 2000 must be cut. Check the estimate line in `tools/score_card_en.py` output.
- Physical anchoring: write the specific ("a 1997 Saab the colour of wet slate"), not the abstract ("an old car"). Numbers in spoken form ("ten seconds nine-something"); decorative fake-precision (0.5 seconds / 18:47) capped at 3 per card.

### 2.2 Personality: scenes plus a language fingerprint

- 4–6 "in this scene, they do this" behavior cases (bullets or short paragraphs). No numbered taxonomies, no parenthetical spec notes ("(voice lower)" belongs in a lorebook director entry).
- A **Language fingerprint** subsection, always: sentence-length habit (clipped fragments / run-on rambler), catchphrases, dialect or regional English (Scouse / Southern drawl / Aussie slang — real regional language culture is the English equivalent of dialect anchoring), address habits (whether they use names; pet-name tiers: luv, pet, sunshine, kid — pick by region and persona), refusal phrasing, praise ceiling.
- All nine liveliness techniques from the sister skill carry over (micro-flaws / say-do gaps / refusal & boundaries / a private life on stage / language fingerprint / physical anchoring / unfinished business / cognitive limits & misreads / emotional inertia). English-native example seeds: left on read; replies "fine." with the period; "I'm not doing this."; group-chat friends heckling; a verbal tic ("mmm" before disagreeing); rent due Friday; assumes {{user}} is here to collect a debt, and is wrong; still short-tempered from the morning's phone call.

### 2.3 AnyPOV pronoun engineering (English-specific hard rule)

- Permanent fields (Description/Personality/Scenario/Lorebook) **never anchor {{user}} with he/she, and avoid they** (singular they sticks permanently and creeps back after edits). Write subjectless or nounified: `Toward {{user}}: a regular now. Gets the corner booth without asking.`
- Greetings may use second-person "you" (gamebook tradition, immersive and legitimate) — but only for {{user}}'s observable situation, never their actions/dialogue/thoughts (§3.2).
- Only explicitly tagged fempov/malepov cards may anchor user gender, and tags must match.

### 2.4 Scenario: always-true only

`{{user}} is on a date with {{char}}` in Scenario = the model drifts back to the date long after the breakup. Temporary situations belong in the First Message; Scenario gets one permanently-true sentence ("Runs the only diner open past midnight on Halsey Street.").

### 2.5 system_prompt in six segments

1. **You are <Name>** + one persona anchor.
2. **[Style]** dialogue-shape constraints (fragment share / sentence caps / praise ceiling), baseline stance toward {{user}}, and **tense + narrative person pinned** (one choice, whole card).
3. **[Adversity]** what the character concretely does when crossed / humiliated / ignored (in-character, no lectures, no collapse).
4. **[Boundaries]** (positive phrasing — bare don't/never is unreliable on LLMs): **Speak and act only for <Name>**; narrate only what <Name> can observe; {{user}}'s words, actions and thoughts belong to {{user}} alone. Stay in character; never mention AI or models. Then an explicit slop ban: pick 6–10 high-risk phrases for this genre from §7 ("never write 'barely above a whisper', 'eyes sparkling with mischief', 'shivers down', 'a mix of X and Y', 'not X, but Y' constructions").
5. **[Cognitive limits]** the character knows {{user}} only through observation and what's been said; guesses wrong; repairs wrong guesses with actions, not apology speeches.
6. **[Emotional inertia + Output rhythm]**:
   - Default reply ≤120 words including narration (long-form cards may raise it — and must then demonstrate the length in the greeting); open up only at scene changes or long user turns; no fixed action-dialogue-action template.
   - Narration = observable physical fact; no emotion commentary ("clearly", "obviously", "a hint of", "she couldn't hide") — interpretation belongs to the reader.
   - First beat when offended = emotion only (flat "Ha." / silence + one action / a counter-question, ≤25 words); no same-turn self-defense; explanations arrive a turn late and grudgingly.
   - Fragments and one-word lines ≥1/3 of dialogue; mouth and hands may contradict. Information released one layer per turn. Cold endings allowed: no "what do you say?" / "the choice is yours" fishing.

## 3. First Message

### 3.1 Length and format band (English-native; replaces the Chinese 800–2,600-char band)

- **Main band 150–350 words** (anchored on the sampled median of 179 and the greeting-equals-reply-length rule). Secondary bands 80–150 / 350–550. RPG/scenario cards (paradigm D) may run to 550. **Above 600 words is bloat.**
- Pick one format and hold it: **novel prose** (narration + quoted dialogue) or **asterisk style** (`*She looks up.*`). No mixing, no tense drift.
- **No HTML status bars or panels** (0/30 in the wild; Western readers read Chinese-style panels as foreign-body). RPG/system cards may use one light bracketed status line (`[Day 3 · Supplies: low]`) — that's the whole allowance.

### 3.2 Three jobs + the user red line

Three jobs: **scene** (time/place/weather in one stroke) → **character entry** (mid-action doing something characterful, ≥1 line of dialogue as personality proof) → **answerable hook** (the next move belongs entirely to {{user}}).

User discipline (red line; the scorer auto-fails on it):

- **Zero {{user}}/you actions, dialogue, or inner thoughts.** Rewrite by **subject inversion**: ~~`You are surprised to see him here.`~~ → `The sight of him here doesn't fit.`; ~~`You pick up the letter.`~~ → `The letter sits where anyone could pick it up.` The character observing {{user}} is legal (`She clocks the mud on your boots.` — the watching is *her* action). RPG/isekai exemption: one passive-perception hand-off ("You wake up in…"), never decisions or speech.
- Endings: the mainstream close is a **social-pressure action**, not a question (only 23% of sampled cards end on a question): the character does something {{user}} cannot not respond to. Ban "He waits for your answer." / "What will you do?" / "The night is still young."

Self-check (fix anything missing):

- [ ] Time/place/mood landed in one sentence, no worldbuilding lecture.
- [ ] An in-progress, unfinished event (not a static self-intro).
- [ ] ≥1 line of character dialogue that proves personality.
- [ ] {{user}} has a clear response opening; zero user actions/lines/thoughts.
- [ ] ≥1 piece of private-life evidence (the world contains other people: an unanswered text, a plate left out after closing).
- [ ] Tense/person/format consistent; inside the band.
- [ ] Ends on the character's words or actions; no fishing.

### 3.3 Paradigms

- **A — event scene** (default): 61 words can chart if it's "happening now + answerable".
- **B — undercurrent** (slow-burn romantasy): the character caught having just done something they'd deny meaning.
- **C — confrontation** (enemies-to-lovers opens mid-standoff): specific conflict, visible stakes.
- **D — world broadcast** (RPG/scenario): second-person situation report + one line per NPC to set faces + hand the camera to {{user}}; may run to ~500 words.
- **E — console** (sim/helper): operating instructions, short, with sample inputs.

### 3.4 Alternate greetings: 2–4, always

Each one changes the **entry situation** (time / place / relationship temperature / event stage), not the wording. Main greeting most universal; alternates can experiment. Same §3.2 checklist.

## 4. Example Dialogue (house standard; the voice weapon)

70% of sampled hot cards use it; `<START>` grouping is the standard. House rule: **2–4 short exchanges** (`{{user}}:` / `{{char}}:`) teaching syntax, not plot; at least one is a **refusal / cold-shoulder turn**. Heavy-tic characters (accent spelling, one-word lines, silence beats) may add a **char-only monologue group** (no user turns — pure voice-lock). No all-Q&A sets (they train an interview bot). Hand-write them; pasted model output carries that model's biases.

## 4.5 Lorebook (4–10 entries, conditional reveal first)

Entry-header syntax per [`docs/card-md-format.md`](../../docs/card-md-format.md) (`### Name | keys: a, b | constant | order: N | prob/secondary/sticky…`). English-side rebalance:

- **Standard five**: ① voice samples (constant, order 320 — pure dialogue bank by situation, no narration mixed in) ② behavior director (constant, order 900 — the runtime contract; a condensed rewrite of system_prompt segment 6) ③ backstory vault (keyed on names/places/events — **density-locked**: one reveal per scene, secrets never volunteered wholesale) ④ relationship tiers or house rules (constant — warmth tiers as observable behavior differences, never bare percentages) ⑤ NPC ecosystem (keyed on NPC names — each gets one face-setting line + their own schedule; they are not props).
- Optional: random-event entry (`prob: 15 | cooldown: 6`), $command artifact entries (RPG/sim cards only; plain-text artifacts, no HTML).
- Entry bodies in English, self-contained subjects (trigger keys are not injected with the content); one entry = one matter, 150–1200 words; constants ≤ half.
- **Every keyed entry needs keys** (keys empty + not constant = a dead entry that never fires; the converter guards this, but don't write it).

## 5. Cover art (English-market recipe)

The Chinese-card cover convention (vertical calligraphy title + vermilion seal) **does not transplant** — no cultural anchor. Three rules:

1. **Style routed by genre** (use the 18 style guides in [`../character-card-author/styles/`](../character-card-author/styles/)): realistic photo (modern / workplace / girl-next-door), ethereal (romantasy / fantasy), anime-impasto or anime-cel (anime-adjacent), amcomic (noir / crime), gothic (supernatural). Fantasy settings avoid realistic photo (uncanny valley).
2. **Composition**: vertical 9:16, face in the upper half (eyes near the upper third), a prop that carries character information in hand, one accent color, slight low/high angle, eyes off-camera.
3. **Text rule: default "no text anywhere in the image, no letters, no logos, no watermarks."** Generated English lettering is error-prone and Western card faces carry no title-calligraphy tradition; typography belongs to the UI layer.

Age safety: "a woman in her thirties"-style phrasing, no on-image age digits. Verify every generated cover by eye (face intact / hands / no stray glyphs).

## 6. Creator Notes (the Western social contract, seven items)

Register = casual bot-maker aside, not product copy (no "positioning/differentiation/mechanics"):

1. **POV/audience declaration**, first line: `AnyPOV. Written with a fem-leaning gaze but anyone's welcome.`
2. **Content notes**: SFW statement + content warnings for heavy themes (grief, injury) + a heat note (`Slow burn, fade-to-black territory. This one's about the tension.`).
3. **Art attribution**: `Art: AI-generated (style).` Don't impersonate an illustrator.
4. **Model advice**: one line (what runs the clipped voice well / how long-form models drift / when to re-roll).
5. **First-line guide**: 2 sample opening moves (one cooperative, one contrarian, both in-flavor) — the Western equivalent of cold-start lubrication.
6. **Version line**: `v1.0 (2026-07)`.
7. **One in-voice closer** (the author's note is also performance).

## 7. Anti-slop discipline (English lexicon; scorer speaks the same language)

### 7.1 The lexicon

The full 95-phrase grouped list lives with the scorer (`tools/score_card_en.py`, `SLOP_PHRASES` + `SLOP_REGEX`; sources: Sukino's Banned Tokens list, the Antislop paper (arXiv 2510.15061), EQ-Bench's slop score, community complaint threads). Top clusters to just not write:

- Body: shivers down her spine (whole family) / breath hitches / heart hammered against ribs / swallowed hard / knuckles white / takes a deep breath.
- Voice: barely above a whisper / husky voice / murmured-dependency / chuckles darkly / voice thick with.
- Eyes: eyes sparkling with mischief (gleam/glint/glow family) / eyes never leaving / half-lidded / a smile that didn't reach her eyes / calculating gaze.
- Motion: ministrations / tracing a finger / practiced ease / tucking a strand of hair.
- Metaphor nouns: tapestry / symphony of / kaleidoscope / like a moth to a flame / a dance as old as time.
- Atmosphere: dimly lit / the air is thick with / casting long shadows / dust motes dancing / words hung in the air.
- Endings: they would face it together / was only just beginning / for now, that was enough / ready to face whatever lay ahead.
- NSFW cluster: on SFW cards, any hit is a red line (FAIL, not a deduction).

Usage note (the sources agree): slop is judged by **cluster density**, not single occurrences; and slop fingerprints cluster by model family. The lexicon is a detector + rewrite trigger, not a word ban.

### 7.2 Pattern quotas (whole card)

| Pattern | Quota | Note |
| --- | --- | --- |
| "not X, but Y" / "It's not just X, it's Y" | ≤1 | the #1 LLM rhetorical crutch (EQ-Bench weights contrast patterns at 25% on their own) |
| "a mix of X and Y" | 0 | the emotion-cocktail formula |
| "couldn't help but" | ≤1 | |
| em-dash (—) density | ≤6/1000 narration words (house lint) | **Calibration finding: em-dash does not separate human from AI in English RP prose** — in our 30-card human sample roughly a quarter of top cards exceed 3/1000w (human asterisk-RP prose uses it liberally). It is a tidiness budget, not an AI signal, and costs no anti-slop points (the *opposite* of Chinese, where the long dash is the #1 machine tell — don't port that rule) |
| adjective triads (rule of three) | ≤1 | |
| "little did X know" / narrator winks | 0 | |
| "for what felt like an eternity" | 0 | |
| decorative fake-precision numbers | ≤3 | numbers with narrative function (bills, countdowns, scores) exempt |

### 7.3 Anti-uniformity (structure is the deepest tell)

- Big sentence-length variance: fragments against 30+-word sentences; five equal-length sentences in a row is a signal.
- At least one "useless" idle detail per card; a card where every detail serves a function reads generated.
- Flat closings allowed. "Cleverness density is AI density" — read aloud; whichever line makes you think *nice line* — flatten it.
- Uniform wit = AI: quote-capped facts ≤1, antithesis flips ≤1, aphorism closers ≤1.
- **Common ≠ fake**: the Western mainstream texture is also tropey (mafia boss / arranged marriage / grumpy neighbor). Loose execution with burrs beats sentence-by-sentence polish.

## 8. Score, red-line, ship

```
python3 tools/score_card_en.py cards/en/<slug>/card.md
```

Eight dimensions (100): fields 13 / greeting 18 / liveliness-nine 24 / tags & positioning 10 / format & replayability 12 / lorebook 8 / image prompt 10 / anti-slop 5.

- **Red lines (any hit = FAIL regardless of score)**: user actions/dialogue in the greeting; NSFW lexicon (this skill targets SFW cards); naming-slop character names; real-celebrity/IP fingerprints; therapy claims; permanent estimate >2000 tokens.
- ≥85 ship; 75–84 usable with a weakness list; <75 fix by issues, max 3 rounds.
- **Run the §7 self-check before first submission** (first-draft outputs reliably blow the quotas; "not X, but Y" and em-dash patches are the habitual English offenders).
- If you use an LLM judge at all: calibrate it on human-consensus gold anchors first, and use it only for relative before/after comparison of the same card — see [`docs/blind-review-experiment.md`](../../docs/blind-review-experiment.md) for why (our four-judge panel agreed 86% and was right 12% of the time).
- Convert & import: `python3 tools/card_md_to_st.py cards/en/<slug>/card.md --avatar cards/en/<slug>/cover.png --outdir out/ --slug <slug>` → v2 JSON + v3 PNG, drag into SillyTavern or any v2/v3 frontend.

## 9. Example cards (read one same-quadrant card before writing)

Three cards in [`cards/en/`](../../cards/en/) were authored by this skill and are its structural templates:

- `edmund-harrower/` — fem-audience · fantasy · enemies-to-lovers + forced-proximity · A/C hybrid paradigm. Labeled prose + a density-locked backstory vault.
- `frankie-doyle/` — all-audience · modern cozy · grumpy-x-sunshine + found-family · paradigm A with a short greeting (~160 words). Comfort-without-therapy boundary work.
- `redline-salvage/` — anypov ensemble · sci-fi · adventure + found-family · paradigm D world broadcast. Light bracketed status line + NPC roster + a random-event entry.

The other three (`rosalind/`, `caleb/`, `the-lighthouse/`) predate this skill — written with the Chinese methodology on an English surface. They stay as an honest contrast group: read them to see what "translated discipline" looks like versus "re-derived discipline".

Learn structure and hand-feel from examples; personas, verbal tics and openings must be original. No reskins.

## 10. Field notes (learned the hard way; read before batch production)

1. **First-draft English offenders differ from Chinese ones**: Chinese drafts over-produce 「不是A，而是B」; English drafts over-produce "not X, but Y" and the em-dash patch (`statement—qualifier`). Grep `—` and `not .*, but` before scoring, and unpick sentences at the hit sites. But note the em-dash's *nature* is language-dependent (§7.2): in English it's a style budget, not an AI signal.
2. **"Character observes user" vs "user acts"**: `She clocks the mud on your boots.` (legal — the verb's subject is the character) vs `You track mud across her floor.` (violation — {{user}} got assigned an action). Point at the verb subject of every sentence containing you/{{user}}.
3. **AnyPOV cards leak pronouns in NPC dialogue** — NPCs referring to {{user}} say he/she before you notice. Make NPCs use nouns ("the new regular", "your friend").
4. **Fade-to-black needs an explicit exit**: on SFW romance cards, write the cut into system_prompt ("If things heat past kissing, cut the scene and pick up after.") — without a stated exit the model will cross the line on its own.
5. **Don't study old cards as format guides**: W++-era cards still float around the archives; when researching, read them as history, not as a spec. §2.1's labeled prose is the spec here.
