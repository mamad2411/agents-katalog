---
name: humanize
description: "Use when a draft sounds AI-generated or must not read as AI: \"humanize\", \"de-AI\", \"make this sound human\", \"less AI\", \"sounds like ChatGPT\", AI-detector concerns, or any external-facing text before delivery. The base layer `/founder-pipeline:brand-voice` runs on every string. English rules are explicit; a method and one worked example cover other languages."
allowed-tools: Read, Grep, Glob
argument-hint: "[paste the draft to humanize]"
---

# Humanize

Make the draft sound like *someone* — not like AI, and not like AI that was scrubbed. Two failure modes, equally fatal:

1. **AI tells** — the machine's own patterns.
2. **Scrub artifacts** — the fingerprint of a humanizer checklist: no dashes but the AI skeleton intact, staccato aphorisms, word swaps on an unchanged structure. Laundered text is as recognizable as slop.

Passing a checklist is not the goal. A piece can grep clean and still read as humanized AI. Stance: authentic writing, never detector tricks.

**Priority order is fixed: architecture → constructions → vocabulary.** Rhythm restructuring drives ~90% of the improvement; word swaps alone make text MORE detectable, not less. Never delete a flagged word without rebuilding its sentence — edit, don't excise.

## Step 1 — Architecture and rhythm (do this first)

- **Rebuild the paragraph skeleton.** If every paragraph runs topic → support → transition, the fingerprint survives any word swap. Merge, split, reorder. One paragraph should do a job the others don't: a digression, an example told at length, an objection answered.
- **Rhythm must track meaning.** Long sentences for building an argument, a short one where the argument turns. Variation driven by counting ("insert a fragment every 120 words") is itself a tell — readers feel the metronome. Diagnostic, not quota: in human prose, sentence lengths within a paragraph swing hard — on the order of 10–15 words of standard deviation [operating assumption; calibrate it against the author's own hand-written corpus] — while AI sits in one narrow band. If most sentences live in the 10–20 word range, restructure until they don't — by rethinking what each sentence carries, not by chopping.
- **Keep connectives where logic needs them.** "Because", "so", "which is why", "even though" are human. Connective-stripped choppy prose is a known signature of automated cleanup. Cut only the stacked formal ones (Furthermore / Moreover / Additionally).
- **Let one thing go unresolved.** AI compulsively resolves; honest writing sometimes sits with the discomfort. No recap, no bow, no lesson extracted from every anecdote. End where the thinking actually ended.
- **Don't compress into aphorisms.** If the rewrite is much shorter and every sentence became a punchline, you flattened it. Restore the reasoning; a human shows work.

## Step 2 — Constructions (the durable tells)

Vocabulary lists decay as models get patched; these structures persist. Fix by restructuring the thought, not by rewording the frame.

- **Contrastive phrasing, the whole family:** "It's not just X—it's Y", "Not X. Not Y. Just Z.", "Teams don't need X. They need Y.", "Not because X, but because Y", "isn't a destination; it's a journey". Roughly three times more common in AI text than in hand-written prose [operating assumption, from repeated corpus comparisons — measure it on your own corpus before quoting the ratio], and it's the tell readers now name first. Budget: **at most one per piece**, and only if it corrects a misconception a real reader actually holds. Zero is better. Includes the de-dashed variant: **fragment-contrast epigrams** ("Not a title. A scope.", "Wrong is survivable. Silent is invisible.") — this is what a dash-scrubbed pipeline produces instead of em-dash rhetoric, and it reads just as machine-made. Same budget. Watch for "vibes" as the strawman ("Specifics, not vibes") — a known generator tic.
- **Copula dodge:** "serves as", "stands as", "functions as", "marks", "boasts", "features" where *is/has* belongs. Write is. Write has.
- **Theatrical pause-and-reveal:** "The result? Devastating.", "Why? Because...", "But here's the kicker". A person being honest just says the thing.
- **Quotable-closer stacking:** every paragraph landing like a mic drop. One earned punchline per piece; the rest is prose. The density is the tell, not any single line: no human sustains one aphorism per numbered item across a 6-item list, or a pull-quote blockquote per section, without a single flat stretch. Let some sections end flat — a paragraph that just stops is human.
- **Uncontracted register:** "do not / It is / cannot" sustained through casual prose is a drafting tell. Match the author's contraction rate; blog and social writing contracts.
- **Manufactured-dread scene openers:** "The Sunday-evening panic", "The Tuesday call you were dreading", "It is Sunday, 9pm. You have been drafting the same message for three weeks." — the templated second-person-anxiety cold open. One pipeline stamps it on every post. Also curiosity-gap title parentheticals: "(or doesn't)", "(with receipts)", "(and what they skim)".
- **Reflexive rule of three** — but judge by content, not count. If there genuinely are three things, keep three; mechanically collapsing every triad to two is the scrubbed version of the same reflex. Kill only triads that exist for rhythm ("clear, concise, and compelling").
- **-ing openers and participle tails:** "Offering a wide range...", "...contributing to the broader development of the region". Give the action a subject and a verb.
- **Inanimate agency:** "The data tells a story", "The market spoke". People do things.
- **Performed casualness:** "Here's the thing", "Look,", "I'll be honest", "The truth is". These are the *simulation* of candor — were you being dishonest before? Delete, say the thing.
- **Uniform enthusiasm / relentless positivity:** a product launch and a policy note getting the same excitement. Things that sucked stay sucked; "I don't know" is allowed.
- **Abstraction and restatement:** "a unique mix of smells" → "burnt espresso and old books". A 500-word section with 100 words of information is AI padding; cut restatement, keep information.

## Step 3 — Vocabulary (last, and only with restructuring)

**Baseline list: `${CLAUDE_PLUGIN_ROOT}/skills/humanize/references/forbidden-words.md`.** Load it for
any external-facing draft. Tier 1 is zero-tolerance (no instance ships); Tier 2 is budgeted and each
use must be justifiable. It also records what must NOT be scrubbed — words the author's own corpus
attests, third-party quotes, and factual records. Treat that file as the source of truth: if you
also run an automated content check over your published pages, mirror the list into it and keep the
two in sync, because a ban with no automated check decays quietly.

Flag list (2023–2025 era; decays as models patch — trust structure over words): delve, tapestry, testament, pivotal, intricate, meticulous, landscape (abstract), realm, underscore, showcase, vibrant, robust, leverage, harness, unlock, unleash, foster, holistic, seamless, transformative, game-changer, synergy, elevate, empower, multifaceted, nuanced, comprehensive, crucial (dense), utilize, facilitate, streamline, navigate (metaphor), garner, boasts, commendable, paradigm, myriad, plethora. Latinate padding: "in order to" → to, "prior to" → before, "commence" → start, "approximately" → about.

Banned openers: "In today's...", "In an era where...", "Have you ever wondered", "Picture this", "As a [role], I've learned", "Let me share", "I'm excited to announce", "It's no secret that". Start mid-story: a scene, a number, a claim.

Banned closers: "In conclusion", "At the end of the day", "the key takeaway", "I'd love to hear your thoughts", "What strategies have worked for you?", any recap or optimistic bow.

Stock collocations to kill: "vibrant community", "invaluable insights", "seamless experience", "actionable takeaways", "meaningful impact", "fast-paced world".

**Rule for every hit: rewrite the sentence around the idea.** A deleted adverb on an untouched sentence reads worse than the original.

## Punctuation and formatting

- **Em dashes: density and cadence, not existence.** English default: at most one per ~1,000 words. If the author's own samples use them, match the sample's frequency — matching the author beats scrubbing the tell. The laundering fingerprint is zero dashes with AI rhetoric intact; don't produce it. Never fake a dash with a spaced hyphen ( - ) — that's a scrub scar.
- **The dash budget is an English-language rule.** In several languages the dash is ordinary typography rather than an AI tell — Czech and Slovak (*pomlčka*) are the worked example below. Check the convention for the language you are writing in before stripping anything, and expect that language's real tells to be different (see the worked example).
- **Semicolons are allowed.** AI underuses them; confident human writers don't.
- **Hedging: cap at 1 per 300 words**, never two in a sentence, and keep a hedge where uncertainty is genuine — false confidence is its own tell.
- Parens for citations and URLs; asides get restructured into sentences.
- Social and email: minimal formatting, bold 1–2 phrases max, no headers, no decorative emoji, no bold-header-plus-explanation bullets, list items unequal in length and grammar.
- Consistent quote style; don't mix curly and straight in one piece.

## Building the tell list for another language — one worked example

The English lists above do not translate. For most languages no public taxonomy of AI tells exists
at all, so you build your own and extend it as you find hits. The method: collect a dozen
model-generated pieces in that language beside a dozen hand-written ones, and write down what only
the machine does. The tells are almost always **calques and register**, not a vocabulary list —
which is why a translated English word list catches nothing.

Czech and Slovak below, as a filled-in example of what the output looks like. Replace it with yours;
keep it in the workspace, not in this file, so it can grow.

- Openers: "V dnešní uspěchané / dynamické / digitální době...", "V neposlední řadě", "Pojďme se ponořit do...", "Není žádným tajemstvím, že..."
- Filler: "Je důležité si uvědomit, že...", "Stojí za zmínku, že...", "hraje klíčovou roli", "zásadní krok"
- Contrast reflex: "nejen..., ale i..." more than once per piece; "Není to X, je to Y."
- Segmentation: "Ať už jste X, nebo Y..." (whether-you're framing)
- Calques from English: "adresovat problém" (řešit), "být nadšený oznámit" (announcement-speak), "dávat smysl" is fine but "To rezonuje" is not
- Nominalization chains ("realizace implementace řešení") where a verb belongs; over-formal register in casual channels
- Uniform enthusiasm reads even more foreign in Czech than in English — the Czech professional register is drier; keep it dry. **This generalises:** most languages have a drier professional register than marketing English, and translated English enthusiasm is one of the loudest machine tells in any of them.

## Corpus-level tells (multi-post sites, series, content pipelines)

A single post can pass every check above and still be outed by its siblings. Before shipping anything into a body of published work:

- **Grep the published corpus for the draft's best lines.** Pipelines recycle their favorite coinages ("X wearing a Y costume" in 4 posts, one aphorism verbatim in 2). A phrase that already exists on the site kills both posts.
- **Vary the scaffold between sibling posts.** Seven role pages all running definition → credibility paragraph → numbered "what the role owns" → comparison table → failure modes → CTA is a production line in plain sight. Same for one fixed credibility paragraph ("<N>+ sessions delivered since <year>…") pasted verbatim into every post — vary where it appears, and whether it appears at all.
- **Batch publish dates are visible.** Six posts dated the same day in the archive/sitemap reads as a generation run. Stagger real dates; publish when actually published.
- **FAQ/schema blocks must paraphrase, not repeat.** An FAQ answer that duplicates a body sentence verbatim is copy-consistency no human maintains.
- **Templated hook formulas across posts** (same dread-opener shape, same "Why [naive advice] fails" first header) — one instance is a choice, five are a template.

## Specificity — retrieve, never invent

Every "many people / various companies / several leaders / significant growth" becomes a real number, name, or date — **pulled from the author's material**: `brand_context/` in the active workspace, their notes and session records, previous project files, published posts, or the conversation you are in. If nothing exists, ask the user for one real detail (one question, not a quiz) instead of fabricating texture. Invented "concrete" detail is fabrication even when it's plausible — a fake-precise number is a worse tell than a vague one. The one messy real detail ("inherited 30 microservices and almost no docs") beats the perfectly illustrative version, but only if it's true.

## Voice overrides rules

If a voice sample or `brand_context/voice-profile.md` exists, it outranks every rule here, including dash and construction rules: match the author's habits at the author's frequency. This skill removes the machine; `/founder-pipeline:brand-voice` adds the person. Don't strip a feature the author genuinely uses.

**Author imperfection profile.** For an author writing in a second language, flawless native prose is itself the strongest tell — an author who reliably writes "help you to", article slips and "on a X basis" by hand, then publishes eleven posts with zero second-language residue, has signed the pipeline's name. Preserve the author's genuine constructions when editing their drafts; never grammar-fix a quirk the author reliably produces. Keep the author's verified fingerprint in `brand_context/voice-fingerprint.md` and load it whenever humanizing their prose. The template and a worked example ship at `${CLAUDE_PLUGIN_ROOT}/skills/humanize/references/voice-fingerprint.md`; derive the real one from the author's hand-written corpus before relying on it.

**Fingerprint constructions in fresh prose.** When authoring fresh prose as the author, the same license applies: writing a construction from the verified fingerprint is voice-matching, not error-planting. The criterion is attestation, not grammaticality — a quirk qualifies if the author's hand-written corpus reliably produces it (that's also why "connect with commas" is licensed: it's attested), or if it appears on the plausible-slip list the author has explicitly approved in their fingerprint file. **Never use an unapproved slip list**: the author signs off on that section, in writing, before a single slip ships. Dosage: two or three fingerprint quirks per piece, never one per paragraph; at most ONE slip from the plausible list per piece, and most pieces carry none — occasional means every second or third piece, not every piece. Vary which quirks between sibling pieces, never the same quirk twice in one piece. Slips are grammar only, never spelling — a misspelling is still a banned trick — and never in a headline, a price, a name, or a sentence whose meaning the slip could bend. Never write an error type that is neither attested nor on the approved list.

**Cluster judgment.** One tell is coincidence; clusters are a confession. Don't mangle a good sentence to purge a single flagged word — over-editing is how scrub artifacts happen. Register gate: technical, legal, and academic text keeps its formal connectives and hedges; plain and neutral *is* the human voice there. Spoken scripts (talks, video) allow false starts, repetition, and contractions that written prose wouldn't.

## What NOT to do

No evasion tricks: no homoglyphs, no invisible characters, no invented typos or planted errors, no paraphrase-spinning. Random injected errors are a *documented failed tactic* — detectors measure whole-passage predictability, not spelling, and are now trained on adversarially-modified text directly — and systematic error patterns (every apostrophe missing) fingerprint the tool that made them. The line: an error the author's verified fingerprint records, written at the author's frequency, is voice (see Author imperfection profile); an error invented to fool a detector is a trick. If a draft only "passes" because of a trick, it failed. The honest imperfection is structural: a digression, an unresolved ending, a sentence starting with And or But.

Never route a draft through a commercial humanizer tool (Undetectable, StealthGPT, QuillBot Humanizer, etc.). Humanized-AI is now a class detectors are trained on directly, the tools degrade quality on average, and they leave named artifacts. A careful edit under this skill is the alternative, not a pre-processing step before one.

Keep the draft's version history. Revision trail is the strongest provenance evidence there is, and the best defense if anyone falsely claims the text is AI.

## Self-verification before delivery

**Grep (zero or fixed):**
1. Banned words, openers, closers, stock collocations (Step 3 lists)
2. Contrastive constructions: `[Ii]t's not just|[Ii]sn't just|not only.*but|[Nn]ot because.*but because|[Dd]on't need.*[Tt]hey need|[Ii]sn't a .*it's a` — max 1 total
3. `serves as|stands as|functions as|boasts` 
4. `Here's the thing|The truth is|I'll be honest|But here's`
5. Em dashes over budget (en dashes as sentence punctuation: same budget; languages where the dash is standard typography are exempt — see the punctuation section)
6. Spaced hyphens doing dash work: ` - `
7. Vague quantifiers: `[Mm]any |[Vv]arious |[Ss]everal ` + plural noun without a sourced specific
8. Hedges over 1 per 300 words
8a. Fragment-contrast epigrams (`^Not [A-Z]|\. Not a |\. It is [A-Z]`) — max 1; count aphorisms per section, none may sustain one-per-item across a list
8b. Contraction rate roughly matches the author's; no sustained "do not / It is / cannot" in casual prose
8c. If publishing into an existing corpus: grep the site for the draft's coinages and best lines — zero reuse; scaffold differs from sibling posts

**Anti-scrub pass (judgment, all must pass):**
9. Paragraph skeleton actually changed — not the original architecture with swapped words
10. Rhythm varies *with the argument*, no metronomic short-long alternation, no fragment inserted just to hit a quota
11. Not compressed into aphorisms; connectives present where logic needs them; no quotable-closer stacking, max one pause-and-reveal — zero is better
12. No register-mismatched synonym (a word the author would never reach for)
13. Specifics are real (traceable to the author's material or the source), none invented
14. A side is picked; negatives stay negative; something is allowed to stay unresolved
15. Read it aloud: does it sound like *someone* — this author — or like no one? Would the author defend every sentence as their own?

Below 15/15: fix and re-run, or tell the user exactly which check failed and why it stays.
