---
name: humanizer
description: >-
  Rewrite, audit, or draft text so it reads like a human wrote it. Kills em
  dashes, robotic tone, AI-giveaway words, negative-parallelism reframes,
  forced analogies, and formulaic structure. Use this skill whenever the user
  invokes /humanizer or /delete-ai-words, asks to humanize text, "delete the
  AI words", "de-AI this", "make this sound less like AI", "audit this
  against the writing rules", "fix the AI writing", removes the "ChatGPT
  voice", or complains that a draft sounds robotic, stiff, or generated.
  Also trigger when the user says "audit your text" (target = your own most
  recent draft), and use it proactively whenever drafting content that will
  be read as the user's own words: emails, LinkedIn posts, blog articles,
  essays, bios, cover letters, newsletters, website copy, and social posts.
  Do NOT use for code, legal contracts, academic citations, or technical
  reference docs where formality is required.
---

# Humanizer

AI-generated text has a recognizable accent. Readers in 2026 pattern-match it in seconds, and the moment they detect it, trust drops: the writing reads as low-effort, and the sender reads as someone who couldn't be bothered. This skill removes the accent. The goal is not to trick anyone; it is to make writing sound like the specific person who sent it, because generic voice fails at the one job writing has: being read.

Every rule below exists because the pattern it bans is statistically overrepresented in AI output. Individually each is harmless; a human might use any one of them. It's the density that gives it away. You are managing density.

> Optional personal layer: if a separate `anti-ai-writing-style.md` (or similar voice file) exists in context or in the user's folder, read it and let it override these defaults where they conflict. [ ADD ANYTHING SPECIFIC TO YOUR VOICE HERE — e.g. your banned words beyond the list, your preferred greeting, regional spelling. ]

## Rule priority (use when rules collide)

1. Be accurate.
2. Be clear.
3. Be specific.
4. Sound human.
5. Use style only when it improves the sentence.

Do not follow a style rule so strictly that the result gets awkward. Accuracy beats every style rule: if removing a pattern loses the meaning, keep the meaning.

## Workflow

1. **Find the target text.** If the user pasted text, that's the target. If they say "audit your text" or "humanise your last answer," the target is your most recent draft. If drafting fresh, ask for or infer register (who's reading it, what's the relationship) before writing. If no text is present, ask what to humanise (one short question, then stop).
2. **Establish voice.** If rewriting the user's text, their existing word choices, formality level, and quirks are the target voice; preserve them.
3. **Rewrite at sentence level, not word level.** Swapping banned words for synonyms leaves the robotic skeleton intact. Restructure the sentence around its actual point.
4. **Preserve every fact.** Humanizing must not change meaning, numbers, names, or commitments. If shortening loses a fact, keep the fact.
5. **Run the final pass** (bottom of this file) before returning anything.
6. **Show, don't lecture.** Return the clean rewritten text only, no commentary. If the user asks to "show changes" or "explain," list the specific patterns you removed and why, with before/after for each. Never annotate the text itself with meta-commentary.

## Default voice

Write directly, specifically, and naturally. Start with the useful point.

Short paragraphs, 1 or 2 sentences by default, 3 or 4 sometimes. Vary rhythm: short sentence, longer sentence, the occasional fragment when it sounds natural. Do not write in a steady medium-length pattern.

Use contractions: don't, can't, it's, you're. Use "I" and "you" when natural. Prefer active voice. Take a stance when the evidence supports one. If the point is made, stop. Short and accurate beats long and padded.

## The big one: negative parallelism / reframe ban

This is the hardest ban. Do not reject one frame and replace it with another to fake depth.

A sentence, pair of sentences, heading, or caption fails if it (1) dismisses, minimizes, or questions X, then (2) asserts or upgrades to Y. The ban applies even when the word "not" never appears.

Banned shapes:
- This isn't X. This is Y.
- Not X. Y. / No X. Just Y.
- Forget X. Focus on Y.
- Less X, more Y.
- Not only X, but also Y.
- It's not just about X, it's about Y.
- X? No. Y.
- Stop thinking X. Start thinking Y.
- X is dead. Y is the future.
- The question isn't X, it's Y.
- You don't need X. You need Y.
- It was never about X. It was always about Y.

Sneaky versions (same structure, softer words): "While X may seem...", "Although X appears...", "Sure, X...", "At first glance, X...", "On the surface, X...", "Most people think X...", "Conventional wisdom says X..." — if it then pivots to Y, rewrite it.

Watch the pivot words when they perform a reframe: but, yet, actually, really, instead, rather, ultimately, in reality, the truth is, what matters is, the real, the deeper, the hidden, the overlooked.

The ban crosses sentence boundaries:
- Bad: "Most teams think they have a hiring problem. They have a standards problem." → Better: "The team's standards are unclear."
- Bad: "People blame the algorithm. The input data is broken." → Better: "The input data is broken."

Rhetorical-question version is also banned:
- Bad: "Is this a productivity problem? No. It's an attention problem." → Better: "Attention is the constraint."

Reframe headings are banned ("Not a tool. A system.", "From chaos to clarity", "The real problem"). Use direct headings ("The system", "Input problems").

**Fix rule:** when you find a reframe, delete the rejected half, then rewrite the positive claim as a direct sentence. "It's not about the prompt. It's about the context." → "Context controls the output."

**Allowed contrast:** only when correcting a specific factual, legal, technical, date, number, name, or scope mistake. "The meeting is on Tuesday, not Thursday." Never use contrast for style, drama, or fake insight.

## The kill list: punctuation and structure

**Em dashes (—).** The single loudest tell. Do not use them, even correctly. Restructure instead:
- Two sentences: "The launch failed. Nobody had tested payments."
- A comma: "It works, mostly."
- Parentheses for true asides: "The budget (all $40 of it) ran out."
- A colon when introducing: "One thing mattered: speed."

Do not replace em dashes with spaced hyphens ( - ) as a mechanical swap; if the sentence needed a dash, it usually needed restructuring.

**Formulaic rhythm.** These constructions are fingerprints:
- The rule of three, everywhere: "faster, smarter, and more reliable." One triple per piece, maximum. Prefer pairs, single adjectives, or 4 items if that's what's true.
- Perfectly parallel sentences and paragraphs of identical length. Humans write lopsided. Vary hard: follow a 30-word sentence with a 4-word one.
- "Whether you're a beginner or a seasoned pro..."
- Ending every section with a tidy summary sentence.

**Structural tells:**
- Bullet points for content that should be prose. Bullets are for genuine lists, not for thinking.
- The bold-term-colon pattern repeated down a page. (Used sparingly in a reference doc, fine. As the skeleton of an essay, a tell.)
- Headers on a 400-word piece. Short writing doesn't need navigation.
- An intro that announces what the piece will say and a conclusion that repeats what it said. Cut both. Start inside the point; stop when done.
- Emoji as section decoration.

## Banned vocabulary

Cut these unless quoting or naming the pattern itself:

delve, tapestry, testament, landscape (metaphorical), realm, journey (metaphorical), embark, unlock, unleash, elevate, empower, supercharge, game-changer, seamless, robust, leverage (as a verb), utilize, navigate (metaphorical), dive into, deep dive, harness, paradigm, paradigm-shifting, cutting-edge, revolutionize, intricate, intricacies, showcase, showcasing, crucial, pivotal, surpass, meticulous, meticulously, vibrant, unparalleled, underscore, synergy, synergize, innovative, commendable, highlight, emphasize, boast, boasts, groundbreaking, align, foster, enhance, holistic, garner, accentuate, pioneering, trailblazing, versatile, transformative, redefine, reimagine, optimize, scalable, breakthrough, streamline, frictionless, adaptive, effortless, data-driven, insightful, proactive, mission-critical, visionary, disruptive, unprecedented, intuitive, leading-edge, democratize, accelerate, state-of-the-art, best-in-class, dynamic, immersive, predictive, transparent, proprietary, integrated, plug-and-play, turnkey, future-proof, enduring, interplay, valuable, captivate, bustling, nestled, rich history, hidden gem, must-visit, comprehensive, look no further, rest assured.

Replacements are boring on purpose: "use" not "utilize", "big" not "significant", "helps" not "empowers", "also" not "additionally". If a banned word carries real meaning in context (e.g., "robust" in a statistics paper), keep it; the ban targets decoration, not meaning.

[ ADD YOUR OWN BANNED WORDS HERE — the words that give away AI in your field. ]

## Banned phrase shapes (copulative avoidance)

Don't use bloated verbs to dodge "is" or "has": serves as, stands as, marks a, represents a, boasts a, features a, offers a, plays a role in, helps to, aims to, seeks to. Use the plain verb: is, has, uses, gives, shows, causes, changes, removes, adds.

- "The report serves as a guide." → "The report is a guide."
- "The app boasts a dashboard." → "The app has a dashboard."

## Dead openings, transitions, and bait

Openings to cut: In today's..., In today's fast-paced world, In an era of, It is important to note that..., It is worth noting..., Notably, In order to, Let's dive in, Let's explore, Let's unpack, At the end of the day, Moving forward, In other words, It goes without saying, Nobody is talking about, Most people don't realize, In this article I will, Despite its strengths X faces challenges.

Transitions to cut: Furthermore, Additionally, Moreover, Thus, Hence, Overall (sentence-initial), In conclusion, Ultimately, That said, That being said, With that in mind, On top of that. Use a real transition or none.

Engagement bait to cut: Let that sink in, Read that again, Full stop, This changes everything, Are you paying attention?, You're not ready for this.

Email boilerplate to cut: I hope this email finds you well, please don't hesitate, feel free to, I wanted to reach out to touch base regarding.

Assistant chatter to cut (in chat-style replies): Certainly, Of course, Happy to help, Great question, I hope this helps, Would you like me to.

Cutoff disclaimers to cut: As of my last update, Based on available information, I don't have real-time access.

## Analogy and metaphor control

Default: no analogies. Don't explain ordinary ideas through metaphor or decorate clear points with imagery.

Use an analogy only if ALL of these pass: the subject is unfamiliar/abstract/technical; the analogy makes it easier; it's shorter than the literal version; it's exact enough not to mislead; it reads normally aloud. Otherwise write literally.

Frequency: 0 analogies under 800 words. Max 1 for 800-1,500 words. Max 1 per 1,500 words beyond that. Never stack metaphors.

Banned setups: Think of it as, Imagine, Picture, It's like, As if, As though, The X of Y, Works like, Acts like, Functions as, A bridge between, A lens for, A roadmap for, The engine of, The backbone of, The DNA of.

Banned metaphor families for abstract work: journey, battlefield, machine-for-people, ecosystem, engine/fuel, map/compass, signal/noise (unless literal), iceberg, north star, flywheel, scaffolding, plumbing, gardening, chess, sports, puzzle.

Banned metaphor verbs for ideas/strategy/products: sanded down, bolted on, stripped back, stitched together, woven, layered, carved out, baked in, distilled, unpacked, crystallized, sharpened, surfaced, amplified, anchored, framed, mapped, cemented, bridged. Use literal verbs: cut, added, removed, changed, joined, caused, showed, explained, reduced, clarified, fixed, named, listed, compared, chose, rejected.

- "Your onboarding is a leaky bucket." → "42% of users leave on step 2 because the form asks for billing details before showing the product."
- "The strategy is a compass." → "The strategy says which customers to ignore."

## What humans do instead

**Specifics over abstractions.** "Increased efficiency across multiple workflows" says nothing. "Cut invoice processing from two days to twenty minutes" says everything. Use numbers, names, dates, places, prices, constraints, tradeoffs, real examples. When the source text is vague, ask the user for the concrete detail rather than inventing one.

**Contractions.** It's, don't, we're, can't. Their absence is stiffness. (Exception: keep the user's register; a formal legal letter stays formal.)

**Claims with an owner.** AI hedges into mush: "This could potentially be seen as somewhat problematic." A person writes: "I think this is a mistake." One hedge is honest; three is evasion.

**Mild imperfection.** Fragments are fine. Starting with And or But is fine. A slightly informal aside is fine. Do NOT fake typos or inject slang; overcorrection into forced casualness is its own tell, and worse than the original stiffness.

**Write like you'd say it.** The test for any sentence: would the user plausibly say this out loud to a colleague? "I wanted to reach out to touch base regarding..." fails. "Quick question about..." passes.

## Other AI tells to catch

- **Puffery**: don't inflate normal facts (a pivotal moment, a major shift, broader implications). State the fact, let the reader judge weight.
- **False ranges**: "from ancient traditions to modern innovation." If there's no meaningful middle, delete it.
- **Elegant variation**: don't rename the same thing to dodge repetition ("Sarah" → "the seasoned operator" → "she"). Use the name again.
- **Meta commentary**: don't announce the writing ("In this section", "This article will cover", "Let me walk you through"). Say the thing.
- **Fake-depth participles**: highlighting its importance, underscoring its significance, reflecting broader trends, paving the way for, opening the door to. If the analysis matters, give it a real sentence with a specific claim.
- **Metronome rhythm**: vary sentence and paragraph length.

## Formatting

Short paragraphs. Digits for numbers (3 years, 500 users). No em dashes. Bold sparingly, 1-2 moments per section. Sentence case in headers. Headers and bullets only when they help reading. Code blocks for exact prompts or commands.

## Example

**Before (AI accent):**
"In today's fast-paced business landscape, effective communication is crucial. Our comprehensive platform doesn't just streamline workflows — it empowers teams to unlock their full potential. Whether you're a startup founder or a seasoned executive, our robust suite of tools will elevate your productivity journey."

**After (human):**
"Most teams waste hours a week on status updates. Ours cuts that to one 15-minute sync. We built it for our own team first, and we still use it every day."

Note what changed: the abstraction became a number, the em dash became a period, the negation pivot ("doesn't just X, it Y") disappeared, the audience-pandering line disappeared, and the credibility now comes from a concrete detail instead of adjectives.

## Register warning

Humanizing is not the same as casualizing. A condolence note, a board memo, and a group-chat message are all human, and none of them sound alike. Match the situation. The skill removes the AI accent from whatever register the writing needs; it does not drag everything toward breezy startup-speak.

## Anti-overfitting (don't swing too far)

This describes taste, it doesn't replace judgment. Don't imitate the voice too hard, force jokes, insert slang to sound human, make every sentence punchy, or make every paragraph one sentence. Don't avoid a useful word if it's the exact word and nothing cleaner exists. Don't turn the output into a checklist of avoided mistakes.

Write normally first, then remove the parts that sound machine-made. The test: "Does this sound like something a person would actually write, or like an AI trying hard to imitate one?" If it feels forced, simplify it.

## Final pass before returning

Run silently:
1. Cut the first sentence if it's throat-clearing.
2. Replace vague claims with specific ones.
3. Remove fake importance.
4. Break up repeated sentence shapes.
5. Remove assistant chatter.
6. Replace bloated verbs with plain ones.
7. Search for negative parallelism across sentence boundaries and delete rejected-frame constructions.
8. Search for unnecessary analogies and metaphor verbs; delete unless they pass the permission test.
9. Hunt for any em dash, any banned word, more than one triple, uniform paragraph lengths.
10. Cut the ending if it only repeats the point.
11. Ask: does this sound useful, or overworked? Return the cleaner version.
