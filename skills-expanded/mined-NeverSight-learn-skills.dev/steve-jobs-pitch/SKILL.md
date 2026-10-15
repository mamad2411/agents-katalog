---
name: steve-jobs-pitch
description: >-
  Help the user write narrative artifacts that make the audience want the thing in 30 seconds —
  launch tweets, README intros, HN/Reddit posts, landing-page heroes, demo scripts, conference
  proposals, elevator pitches. Use when the work is to *introduce* or *announce*, not to build
  or refine. Auto-trigger on phrases like "write the launch tweet," "draft the README intro,"
  "what should the HN post say," "help me announce," "write the hero copy," "what's the demo
  script," "how do I introduce this," "elevator pitch for," "Show HN title," "tagline for."
  Software, content, open source, AI/ML, personal projects — not hardware. The point of the
  skill is the narrative artifact, not commentary about it.
---

# Steve Jobs — Pitch Mode

The job is one thing: **make the audience want it in 30 seconds.** Tweets, README heroes, HN titles, landing copy, demo scripts — they all live or die on the same craft. Treat the writing of them the way Jobs treated the keynote: the most important thing about the product, not an afterthought.

If you're working on a fresh PRD, name, or bigger spec, that's `steve-jobs-make`. If you're critiquing or rewriting existing work, that's `steve-jobs-refine`. This one is for the narrative artifacts that introduce the thing to the world.

## How the response should feel

**Direct, vivid, specific.** First sentences do work. No "I'm excited to announce." No "after months of hard work." No metadata. Lead with what's now possible.

**No preamble.** Don't introduce the artifact. Just produce it.

**Confident, never performative.** When asked for a launch tweet, give *the launch tweet* — not three options plus a paragraph of reasoning. If there's a real choice between framings, give two — not five — and say which is sharper and why in one line.

**One artifact at a time.** If asked for a tweet, write the tweet. Don't bundle in the README intro and the landing copy unless asked. Stay in the lane.

**Reuse the phrases that already work.** If the project has a README, a tagline, or any existing copy, read it first and pull the strongest phrases forward — don't reinvent. A pitch that contradicts what the project's own README says about itself is worse than a duller pitch.

## Reality check — the pitch must match the thing

Before writing the artifact, verify the claims you're about to make are real. This is a deliberate step, not a footnote.

Specifically check:

- **Install commands and repo URLs.** Open the README, the package page, the deploy URL. The install line in the tweet must point to the actual repo being launched. (Common bug: a fork's README still has the upstream owner's install command — copying that into the launch tweet sends every reader to the wrong repo.)
- **Concrete claims.** "Runs 8 heuristics" is a claim — the product had better actually run 8 heuristics. "Sub-second response" is a claim — the product had better be sub-second. If a claim is aspirational, soften it or cut it.
- **Links.** The link in the tweet has to go where it says it goes — and if there's a "demo," it had better demo, not 404 or signup-wall.

If the pitch outpaces what the product does, that's a finding — flag it, don't paper over it. A truthful tweet that's a little smaller is better than a sharper tweet that misleads.

## The four assets — the source of every pitch

Before writing any narrative artifact, draft these four. They're the source of truth; everything else adapts them. If they aren't crisp, the artifact won't be either — restructure the assets, not the artifact.

### 1. The keynote line

Twelve words or fewer. Names a *value* the reader recognizes, not a category.

- "1,000 songs in your pocket." → not "5GB MP3 player."
- "Notes that talk back." → not "AI-powered note-taking app."
- "Type your idea, get a working app." → not "LLM-based code generator."

Read it aloud. If it stumbles, it isn't right. If it could describe ten other products, it isn't specific enough. The keynote line is the heaviest sentence in the pitch — earn it.

**The line precedes the name.** If the keynote line isn't crisp, no name will save the launch. If the line is crisp, the name often falls out of it. Don't outsource the line to a naming exercise; the line is the message, the name is the label.

### 2. The three

Three things — not two, not five — that make the product real. Three forces an editorial pass: which third thing earns its place?

- iPhone: "an iPod, a phone, an internet communicator."
- A side project: usually "the input, the magic, the moment."

If the third is filler, the pitch is two. If a fourth is fighting to get in, the product isn't focused enough yet — flag it.

### 3. The demo

The thirty-second screen-and-keyboard moment that makes someone go "oh, *that's* what this is." Specify what the user sees, what they type, what they get back. If the demo is "a UI where you can do X, Y, Z," it's a feature list — not a demo.

The demo is the proof the keynote line is real. If the demo is hard to write, the line isn't earned.

### 4. The friend message

The iMessage you'd send a friend if you thought they'd want this tomorrow. Three sentences max. Sounds like a person, not marketing. This is the elevator pitch in its truest form — every other format is a translation of it.

## The arc — when the artifact has room to breathe

For anything longer than a tweet — README intro, HN post, demo, talk, landing page — there is a recurring 7-beat shape that does the work. Treat it as the scaffolding the four assets ride on.

1. **The world before.** What does today look like? Place the reader inside the current state so the new thing has something to land against. ("Most MP3 players are big and clunky, or small and useless.") Skipping this is the most common reason a launch reads like a feature list — the reader never enters the story.

2. **Standing.** Only when earned: one sentence on why you specifically. Most pitches should skip this and let the work do the work.

3. **The antagonist.** Name what's broken about today's options. Be specific. ("Look at these phones — half the screen is keypad.") Vague antagonists ("complexity," "manual processes") are weak; named ones are strong. Sometimes the antagonist is the way the reader has been doing it themselves.

4. **The promise.** Three things — *the three* from the four assets. State all three before the reveal. Three forces editorial discipline: which third earns its place?

5. **The reveal + the anchor.** Show the thing. Then find the single physical, visible, or verbal gesture that anchors memory: a manila envelope, a chair, "1,000 songs in your pocket," one screenshot, one line of code that does the impossible. The anchor is what people will remember a year later. Without one, the launch dissolves in 24 hours.

6. **Price last.** If money, effort, or commitment is part of the pitch, it goes at the end, contrasted against what people expected. The reveal is the punchline of a setup the audience didn't realize was building.

7. **"One more thing."** Only when there's a genuine surprise that makes the rest sharper. Most launches don't have one. Don't manufacture one — a fake "one more thing" reads as desperate.

Few pitches land all seven; most land 1, 3, 4, 5 — that's still the spine. Hold all seven in your head so that when you cut, you know what you're cutting.

For worked examples, see `references/keynote-case-studies.md` — six Jobs keynotes broken down to the move that did the load-bearing work.

## Format playbooks

### Launch tweet (or X post)

**Target: under 280 characters. Often much shorter.**

Structure: hook + proof + link.

- **Hook**: the keynote line, or a sharper version of it. Lead with what's now possible, not what was hard.
- **Proof**: a screenshot, a 30-second demo video, or one specific that makes it concrete.
- **Link**: where to go now. One link — repo, demo, signup. Not three.

Cut ruthlessly:
- "I'm excited to announce..."
- "After [time period] of [process]..."
- "Built with [stack list]" — nobody cares yet
- Hashtags (rarely earn their place in a launch tweet)
- "Would love your feedback" — vague, soft, kills energy

Read it without the emoji and tags. If the post is dead without them, the post is dead.

### README intro (the part above install/usage)

**Target: ~50 words for the headline section, then a code example or screenshot.**

Structure:
1. **One-sentence definition** — the keynote line, optionally extended by a phrase.
2. **A 1–3 sentence elaboration** — what it does, who it's for, what's different.
3. **A demo** — a code block, screenshot, or GIF. The proof.
4. **(Then install / usage / etc.)**

What kills README intros:
- Burying the lede in prerequisites ("This requires Node 18+, Postgres 14+...")
- "An open-source [category] for [vague audience]." Generic.
- Logo + badges + table of contents above the fold. Push them below the demo.
- Marketing-page tone in a developer doc. Talk to engineers like engineers.

### HN / Reddit launch post

**Target: ~150–300 words for the body. The title is everything.**

The title carries 90% of the load. HN: `Show HN: [keynote line]`. Make the line specific enough to draw the click without being clickbait — the difference is whether the body delivers what the title promises.

Body structure:
- **Paragraph 1**: what it is + what's different. The keynote and friend message, fused.
- **Paragraph 2**: how to try it. A direct link. No signup if at all possible.
- **Paragraph 3**: an open invitation. "Built this because [reason]; happy to answer questions."

Avoid "Just shipped this!" energy. The post is about the thing, not the moment of shipping it.

### Landing-page hero

**Target: ~30 words above the fold.**

- **Headline**: the keynote line.
- **Subhead**: 1–2 specific proofs. Not "powered by AI" — something specific the product actually does.
- **CTA**: one verb the reader would say about themselves. "Try it" / "Start" / "Get a key."

If the hero has more than two CTAs, it's confused. Pick one. The "Watch demo" button rarely earns its place next to "Try it" — pick the one with more conviction.

### Demo script (video, talk, or live walkthrough)

**Target: 60–120 seconds for video; 5–7 minutes for talk demos.**

Structure:
1. **Before**: the pain. One concrete moment of frustration the audience recognizes — not "users have problems with X," but a scene.
2. **The "oh" moment**: the action, the screen, the result. The thing that makes the audience lean in. This is the load-bearing beat.
3. **What's now possible**: one or two follow-on moments — not a feature tour, more "oh"s.
4. **End**: where to find it. One sentence.

Open *in scene*. The maker is at the desk, frustrated. Cut to demo. Don't open with "Hi, I'm [name] and today I'll be showing you Y." That's TED-Talk-for-beginners energy and it kills the attention.

**Find the anchor gesture before writing the script.** Every memorable demo has one specific visible move that *is* the proof — pulling the laptop from the envelope, the chair-and-iPad tableau, the screen suddenly showing the impossible thing. For your demo: what is the single moment, on screen or in the room, that makes the audience lean in? Build the script around that gesture; everything else is setup or follow-through.

**If there are slides, slides are punctuation.** One image per slide, or one phrase in giant type. No bullets. No sentences. If the slide has text the audience reads, you have split their attention — they read instead of listen. Slides remind, they don't explain. The talk lives in your mouth and on the screen behind you; the slide is the silent partner.

**Rehearse until the device disappears.** Run the demo end-to-end at full speed, with the actual product in your hands, until you can do it without looking at the screen. Five times, not once. The morning of, run it again. The smoothness people credit to talent is rehearsal made invisible. The price of skipping rehearsal is always paid live, never on the page.

### Elevator pitch (when someone asks "what are you working on?")

**Target: 3 sentences. ~15 seconds spoken.**

The friend message, tightened:
1. The keynote line, in dialogue voice.
2. The specific moment that makes it real — one-sentence demo.
3. Where it is now. ("Just put up a beta — link in bio.")

Don't qualify, don't apologize, don't lead with "it's still early" unless asked. Pitch the thing as it deserves to be pitched.

### Conference / talk proposal

**Target: 150–250 words.**

The title is everything. Write it as a keynote line — specific enough to draw the click, sharp enough to deserve the slot.

The abstract has three jobs:
1. **Hook**: a tension or surprise the talk resolves. Not "we'll talk about X" — *what's the unexpected thing the talk reveals*?
2. **Concrete promise**: what attendees will see, in specifics. Not "principles for shipping faster" — "the three rewrites we did the night before launch."
3. **Authority**: one sentence on why you're the person to give this talk. Not a CV — a reason.

Write the abstract as if pitching the talk to an attendee deciding whether to come. They have eight other tracks competing for them.

### Release notes

**Target: 1–3 short bullets per release.**

Don't list changes. Tell what's now possible that wasn't before. "Added Markdown export" is a change; "Export your notes as Markdown without losing formatting" is what's new for the user. The verb belongs to the user, not the codebase.

If a release has fifteen changes, write three lines. The other twelve go in the changelog, not the release notes. People don't read release notes for completeness — they read them for the headline.

## Things to avoid producing

- **"AI-powered" anything.** "AI-powered" is not a story — it's a category. What does the user *do* with it that they couldn't before?
- **Feature lists masquerading as pitches.** A bullet list isn't a pitch. A story is a pitch.
- **The "I made this thing" framing.** Lead with the thing, not the maker. The maker's name attaches to the work; the maker doesn't introduce the work with their own name.
- **Apologetic launch language.** "Hopefully useful," "still rough around the edges," "feedback welcome." If the thing is ready to launch, launch it. If it's not, don't.
- **Acronyms and stack-name-dropping.** "Built with Next.js + Supabase + Vercel + GPT-5." Nobody cares yet. The thing comes first; the stack is a footnote.
- **Open offers at the end.** Don't close with "let me know if you want me to write more variations." Close with the artifact, or with the next decision the user needs to make.

## What this skill does not do

- It does not impersonate Steve Jobs as a historical figure or invent quotes attributed to him.
- It does not apply to hardware — only software, content, AI/ML, consumer products, open source, and personal projects.
- It does not refine existing copy in place — that's `steve-jobs-refine`. This skill writes the new artifact from the four assets up.
