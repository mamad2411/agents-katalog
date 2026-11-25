---
name: content-humanize
description: >
  Use when text a model drafted is about to be read by a customer, a prospect or an
  audience — captions, ads, landing copy, emails, proposals, reports. Also when someone says
  a text "sounds like AI", "sounds like ChatGPT", reads flat, or when a batch of copy needs to
  hold one voice across every piece.
  Triggers on: "humanize this copy", "make this sound human", "does this read like AI",
  "suena a IA", "humaniza este texto", "quita las muletillas de IA", "copy gate".
  Self-contained: no other skills required.
version: 0.1.0
author: GrowthLab (growthlab.mx)
license: MIT
upstream: humanizalo by Hainrixz (https://github.com/Hainrixz/humanizalo), MIT — see NOTICE.md
---

# content-humanize

> Fork and extension of [`humanizalo`](https://github.com/Hainrixz/humanizalo) by Hainrixz,
> MIT licensed — full attribution in [`NOTICE.md`](NOTICE.md). Everything added on top is
> GrowthLab-original and MIT licensed too.

> **Purpose:** the gate a piece of LLM-drafted copy passes before it reaches a reader. It takes
> the draft and returns three things: the rewritten copy, a scored verdict (PASA / NO PASA /
> REVISIÓN MANUAL), and the list of what changed and why.

**Dependencies: none.** This skill does not call other skills. Everything it needs is inline.
It reads `product-marketing.md` (see the `product-marketing-md` skill) when one exists — that is
where the voice comes from — but it runs without one, telling you what it assumed.

**What this skill adds over the upstream it forks** (each item traces to a real production run,
see `references/worked-examples.md`):

| # | Addition | Why it exists |
|---|----------|---------------|
| 1 | es-MX pattern library | The upstream is English-only. Spanish has its own tells. |
| 2 | Bundle-level repetition check | A client rejected a caption wave verbatim because the brand name opened every caption. Per-piece scoring never sees it. |
| 3 | Truth-and-framing hard rules | "Add soul, have opinions, be specific" pushes models to invent figures and cases. Non-negotiable in client work. |
| 4 | POV check | A real post addressed the business owner in third person while speaking to that owner. |
| 5 | es-MX locale gate | Spain-isms, `usted` drift, `€`, `MM/DD/YYYY`. |
| 6 | Five format profiles + thresholds | Generic advice ("let some mess in", "add a tangent", "cut anything quotable") destroys a 40-character headline. |
| 7 | Anti-overcorrection section | Blind rules ("kill every adverb", "zero em dashes") mangle Spanish, where `ya`/`todavía` are structural and the raya is legitimate punctuation. |
| 8 | `check_tells.py` | A self-reported score is a vibe. The countable tells get counted. |

---

## The set

This skill is one of five in the same repo. Two of them write a context file; three read it.

`product-marketing-md` writes `product-marketing.md` (what you sell, to whom, why they buy).
`design-md` writes `design.md` (how you look and how you sound). Those two files are read by
`landing-md`, `social-calendar` and `content-humanize`.

**You need none of them to run this one.** They are separate downloads from
[github.com/jeremidelacruz/growthlab-skills](https://github.com/jeremidelacruz/growthlab-skills),
and if this file is all you have, everything below still works.

**You are here: `content-humanize`** — the copy gate. `landing-md` and `social-calendar` both
route their copy through it before shipping; it reads `product-marketing.md` for voice when that
file exists.

---

## Before starting

> **If you cannot ask** — running unattended, or inside someone else's workflow — do not stop at
> the requirements below. Jump to "When you cannot ask" at the top of Process, state your
> assumptions, and keep going.

1. **Read `product-marketing.md`** if it exists in the project (also check `.agents/`) — it
   carries the brand's tone, audience, ICP and forbidden topics. Voice comes from that file,
   never from the model's idea of what sounds edgy.
   - If it does not exist: ask for three things minimum — who the reader is, the brand's tone in
     a sentence, and any topics or claims that are off-limits. State what you assumed.
2. **Read `design.md`** (see the `design-md` skill) when the copy will be rendered into a visual
   — its voice section applies to the copy too.
3. **Confirm which format profile applies** — this decides the ruleset AND the passing threshold.
   See Step 0. Do not run a generic pass.

---

## Inputs

| Input | Required | Notes |
|-------|----------|-------|
| The draft copy | Yes | One block or a whole bundle. Bundles are preferred: Step 7 only works on bundles. |
| `product-marketing.md` | Recommended | Tone, audience, ICP, vetoes. Without it, ask and state assumptions. |
| Format profile | Yes | Step 0 — social · ads · web · email · doc |
| Validated figures / approved claims | If the copy cites numbers | From the person who owns the data, or a citable public source. If absent, the mechanism rule in Step 4 applies. |
| First-person material (anecdotes, angles) | Optional | From the author or a real conversation — never invented |

---

## Process

### When you cannot ask

If you are running unattended, or inside someone else's workflow, and something below cannot be
answered: **do not stop, and do not assume silently.** State the question, answer it with the most
defensible assumption you can support, mark it, and put it in an `## Assumptions` block at the top
of what you deliver. The reader needs to see the guesses before they see the work.

### Step 0 — Pick the format profile

The profile decides which rules apply and what score the copy must clear. Picking wrong is the
most common failure: applying the social profile to ad copy produces charming headlines that get
truncated at 40 characters.

| Profile | Covers | Threshold | Dominant rules |
|---------|--------|-----------|----------------|
| `social` | IG/FB captions, carousels, Reels scripts, Stories, LinkedIn posts | **42/60** | Full voice injection, hook discipline, one CTA |
| `ads` | Meta primary/headline/description, Google RSA, display | **42/60 + budgets** | Every element within its character budget is a hard pass/fail, not a score bump |
| `web` | Landing sections, FAQ, forms, buttons, errors, thank-you | **42/60** | Clarity over voice, microcopy rules, message match with the ad |
| `email` | Welcome, nurture, reactivation, post-purchase sequences | **42/60** | Subject + preheader budgets, one idea per email |
| `doc` | Proposals, monthly reports, decks, audits, briefs | **42/60** | Professional register, honest hedges kept, no jokes |

**If you do not know the channel, do not guess silently.** Ask. If you cannot ask, default to
`web` — it is the least destructive: it keeps clarity over voice and imposes no character budget
you might be violating without knowing. Mark the choice `[ASSUMED]` in your Assumptions block and
say what would change if it is wrong. Picking a profile by how the text *looks* is a hunch, and
the profile decides which rules apply.

Full rules, character budgets and per-profile exceptions: `references/format-profiles.md`.

### Step 1 — Load voice context

Extract from `product-marketing.md`, and hold it for the whole batch (switching context per piece
is what makes a 30-post package drift tonally):

- the voice traits, verbatim
- the audience (who reads this — feeds the POV check in Step 5)
- vetoes (forbidden topics, terms, claims)
- approved claims and validated figures
- the positioning line the brand competes on

### Step 2 — Deterministic pre-check (run the script before reading)

```bash
python <ruta-de-esta-skill>/check_tells.py <file-or-dir> --profile social --lang es

# or pipe a draft through stdin
cat draft.md | python <ruta-de-esta-skill>/check_tells.py - --profile ads --brand "Nombre"
```

Options: `--profile {social,ads,web,email,doc}` · `--lang {es,en,auto}` · `--brand "Nombre"`
(bundle check) · `--json` · `--quiet`. Exit code 1 when there are hits, so it works as a gate in
a script. Stdlib only, no install step.

The script counts what is countable: em dashes, banned phrases (ES + EN), Spain-isms, `-mente`
adverb density, sentence-length uniformity, passive markers, forced triads, bold and emoji density,
hedge stacks, chatbot openers, character-budget overruns, and cross-file repetition.

Treat its output as the evidence file for the rest of the pass. It does not produce the 6-dimension
score — that is judgment — but a block with 14 script hits does not get an 8 in Density because
the rewrite "felt tighter". Run it again after the rewrite; hits must go down.

### Step 3 — Pattern sweep (the 40 patterns)

Work through the five categories against `references/patterns-es-mx.md` (default) or
`references/patterns-en.md` (English deliverables). Flag every hit with its pattern ID, then rewrite.

| Category | Patterns | One-line fix |
|----------|----------|--------------|
| A · Content inflation | P01–P08 | Replace with a specific fact or cut the sentence |
| B · Vocabulary | P09–P14 | Plain words. `es`, not `funge como`. Kill filler adverbs. |
| C · Structure | P15–P26 | State the point. Drop the runway, the negation, the forced triad. |
| D · Formatting | P27–P31 | Sentence case, minimal bold, no decorative emoji, punctuation a person would type |
| E · Communication artifacts | P32–P40 | Cut chatbot scaffolding, hedge stacks and meta-commentary outright |

### Step 4 — Truth and framing (hard rules — these override every other instruction)

**When you do not know the mechanism either.** The rule says: no figure you cannot source, so
rewrite around the mechanism instead. That assumes you know how the thing works and are only
missing numbers. On a thin brief you have neither. Then write around what you *do* have that is
true: **the reader's situation.** The Sunday spent hunting receipts is real without knowing a
single thing about the product's architecture. Specificity about the reader is always available
and never a fabrication.

The upstream tells the model to "have opinions" and "be specific". Applied without a brake, that
produces invented case studies. These rules win over any stylistic advice in this skill.

1. **No invented figures, cases or results.** A number ships only if the person who owns the data
   validated it or it comes from a citable public source. If you have neither, **rewrite around
   the mechanism** — explain *how* the result happens — and do not leave a `[dato pendiente]`
   marker in the copy.
2. **Brand non-negotiables hold.** Facts the brand never discloses (team size, private figures)
   and topics it cannot advertise stay out, no matter how much "specificity" they would add.
3. **Filler is not an angle.** A fact irrelevant to the reader (usually geography) must not anchor
   a hook, a headline or an aside.
4. **Positioning holds.** A challenger brand does not borrow the incumbent's proof. Check the
   brand's positioning line from Step 1 before writing any claim of scale.
5. **Superlatives need a source.** "El mejor", "líderes", "únicos" without a citation is a HIGH
   flag.
6. **First-person material must be real.** If a piece needs an anecdote and you do not have one,
   ask for it. An invented "la semana pasada un cliente me dijo…" is a fabrication with a
   friendly tone.

Any hit here blocks delivery regardless of the score. See `references/hard-rules.md`.

### Step 5 — POV and locale gate

**POV check.** Name the reader from the audience definition, then verify the copy speaks *to* that
person and not *about* them. A piece written for business owners that says "tu dueño quiere
saber…" has the reader watching someone else's conversation. Second person, consistent, all the
way through. Check that the CTA addresses the same person as the hook.

**Locale gate (es-MX).** Full tables in `references/locale-es-mx.md`:

- `tú` register unless the brand specifies formal
- zero Spain-isms (`vosotros`, `ordenador`, `móvil`, `coche`, `coger`, `bolígrafo`, `aparcar`)
- `$` MXN, never `€` · dates `DD/MM/AAAA` · `correo`, not `email`, in formal copy
- no España as the reference point for Spanish
- active verbs, no nominalizations (`tomar una decisión` → `decidir`)

Skip this gate only when the deliverable itself is in English.

### Step 6 — Voice injection (from the brand, not from the model)

Strip-only produces clean, dead text. That is still a fail — voiceless writing is the loudest tell
there is. Inject voice from the sources loaded in Step 1:

- Use the brand's actual traits, verbatim. "Cercano y directo" is an instruction, not a decoration.
- Vary rhythm deliberately: a short sentence, then one that runs longer before it lands.
- Take a position. React to the fact instead of reporting it neutrally.
- Put the reader in the room: `tú`, not "las empresas" or "uno".
- Trust the reader. Cut the justification and the hand-holding.

**Where the voice comes from matters.** For personal-brand content the angle belongs to the
author and gets co-created with them. The model supplies the craft, not the life.

### Step 7 — Bundle pass (never skippable when there is a bundle)

Per-piece scoring is blind to the failure mode that actually got copy rejected by a client. Run
these across the whole wave, not inside one block:

1. **Anchor-phrase repetition.** No phrase repeated as an opener or a hook across ≥3 pieces of the
   same wave. The script flags candidates; you decide.
2. **Brand name placement.** The brand must not open every section, paragraph or caption.
3. **CTA variety.** Same canonical CTA is fine; identical closing sentence across the bundle is not.
4. **Structural sameness.** If every piece is hook → three bullets → question, two of them get
   restructured.
5. **Text budget vs. the visual.** If the copy on a card buries the image, cut copy, not image.

### Step 8 — Score and audit loop

Score every block on the 6 dimensions below, then:

- Below the profile threshold → name the two lowest dimensions, rewrite those specifically, rescore.
- Maximum 3 passes. Still short after 3 → ship the block flagged `[REVISIÓN MANUAL — score X/60]`
  with the two blocking dimensions named. Do not quietly deliver it as passing.
- Re-run `check_tells.py`. Script hits must be lower than the pre-check. If they are not, the
  rewrite did not happen.

#### Scoring rubric

| Dimension | 1–3 (obvio IA) | 4–6 (neutro) | 7–10 (humano) |
|-----------|----------------|--------------|---------------|
| **Directness** | Hedges every claim, qualifies everything | Mostly direct, occasional hedge | States it flat out, no apology |
| **Rhythm** | Uniform sentence length, metronomic | Some variation | Short punches mixed with longer ideas |
| **Trust** | Hype and unsourced superlatives | Measured claims | Specific fact or concrete mechanism, earns credibility |
| **Authenticity** | Could be any brand in any category | Recognizable niche voice | Unmistakably this brand in this category |
| **Density** | Padded, ideas restated, low signal per word | Reasonable | Every sentence advances the idea |
| **Soul** | Institutional, no personality | Mild personality | A person wrote this, and you could guess who |

**The honest limit.** This is a structured judgment, not a measurement. It reliably separates a
30 from a 50 and tells you nothing useful between 44 and 46. Write half a sentence of
justification next to each number — a score you cannot justify is a number you picked to pass.
Treat the threshold as the line under which you do not hand the text over, not as a certification.

**Threshold: 42/60 for every profile.** There used to be a stricter 45 for `ads`; it was removed
because this instrument cannot tell 44 from 46, so a three-point bump was fake precision dressed
as rigour. What `ads` gets instead is a real gate: **every element inside its character budget,
checked, or it does not ship.** That is binary and countable, which a score is not.

A hard-rule hit (Step 4) blocks at any score.

---

## When NOT to apply a rule

Blind application is its own failure mode. These are the calibrations that keep the gate from
mangling good copy:

- **Em dashes in Spanish.** The upstream says zero tolerance. In es-MX the raya is legitimate for
  dialogue and for parenthetical asides in editorial prose. The rule here: no em dash *chains*,
  no more than one per paragraph, and never as a substitute for deciding where the sentence ends.
- **Adverbs in Spanish.** `ya`, `todavía`, `apenas`, `casi` are structural, not filler. Kill the
  `-mente` intensifier pile (`realmente`, `verdaderamente`, `sumamente`), keep the ones carrying
  meaning.
- **"Cut anything quotable."** True for essays, false for ad copy. A headline is *supposed* to be
  memorable. In the `ads` profile this rule is off.
- **"Let some mess in."** Off for `ads`, `web` microcopy and `doc`. A tangent inside a form error
  message is a bug, not personality.
- **Rule of three.** Off when the three items are real (three campaign phases, three deliverables).
  The pattern is about *forced* triads, not about counting.
- **Hedging.** One honest qualifier survives. `doc` profile in particular: a report that overstates
  certainty to score higher on Directness is worse than one that hedges accurately.
- **Repetition.** Repeating the right noun beats synonym cycling (P24). Do not "fix" a repeat that
  was correct.
- **Brand-mandated formality.** If the brand's context file says `usted`, the locale gate follows
  the brand, not the default.

---

## Output

The labels below are English because this file is. **The copy itself keeps its own language** —
you are humanizing Spanish, the rewritten block comes back in Spanish. Localize these labels if
that suits your team; just keep them consistent across a bundle.

**Format (per block):**

```
### <block ID / slot>

<copy humanizado, listo para publicar>

**Score:** [47/60] — Directness 8, Rhythm 8, Trust 7, Authenticity 8, Density 8, Soul 8
**What changed:** <1–2 lines: which tells dominated, and what you did about them>
```

**Bundle verdict:**

```
GATE PASSED — <N> blocks · mean score <X>/60 · <N> flagged for review
   Reglas duras: sin cifras inventadas · sin no-negociables de marca · sin ancla de relleno
   Bundle: no anchor phrase repeated across 3+ pieces · brand does not open every block
   Pre-check: <hits antes> → <hits después>
```

or

```
GATE FAILED — <N> blocks below threshold · <N> hard-rule hits
   Bloqueantes: <lista>
```

**Checklist before handing back:**

- [ ] Voice matches the brand's traits, verbatim, from `product-marketing.md`
- [ ] Zero invented figures, cases or results
- [ ] No brand non-negotiables disclosed, no filler anchors
- [ ] es-MX locale clean when the deliverable is Spanish (no Spain-isms, `$` MXN, DD/MM/AAAA)
- [ ] Character budgets respected for the profile
- [ ] Bundle checks run, not just per-piece
- [ ] `check_tells.py` re-run after the rewrite, hits down

---

## References & credits

### Included with this skill

- `references/patterns-es-mx.md` — the 40 patterns with es-MX signals and replacement tables (default lane)
- `references/patterns-en.md` — the English tables, forked from `humanizalo`, condensed
- `references/format-profiles.md` — the 5 profiles: rules, thresholds, character budgets per platform
- `references/locale-es-mx.md` — es-MX locale gate, Spain→México substitution table, register rules
- `references/hard-rules.md` — truth-and-framing rules with the production evidence behind each
- `references/worked-examples.md` — real before/after from shipped copy
- `check_tells.py` — deterministic pre-check, stdlib only, no dependencies

### Upstream

- [`humanizalo`](https://github.com/Hainrixz/humanizalo) by **Hainrixz**, MIT — the 40-pattern
  taxonomy, the 6-dimension rubric, the 3-pass audit loop and the soul/voice section. Forked
  whole, then translated to es-MX, extended and calibrated (see "When NOT to apply a rule").
  The full MIT notice travels with this skill in [`NOTICE.md`](NOTICE.md).

### Companions in this repo

- `product-marketing-md` — writes the context file this gate reads its voice from
- `design-md` — the visual half of the same context
- `landing-md` — routes its page copy through this gate before the QA step
- `social-calendar` — routes its captions through this gate at Step 6

---

### About GrowthLab

These skills are the free half of a working method. [GrowthLab](https://growthlab.mx) is a
paid-media agency in México that runs its delivery on Claude Code — the context files, the
gates and the QA you just used are how our own client work ships. If you would rather have
the campaigns, the pages and the content *run for you* on top of this method, that is the
paid half: [growthlab.mx](https://growthlab.mx) · hola@growthlab.mx.

---

## Changelog

**v0.1.0** — First public release. Fork of `humanizalo` (40 patterns, 6-dimension rubric,
3-pass audit loop) extended with: es-MX pattern library, five format profiles with their own
thresholds and character budgets, truth-and-framing hard rules, POV check, es-MX locale gate,
non-skippable bundle pass, anti-overcorrection calibrations, and `check_tells.py`.
