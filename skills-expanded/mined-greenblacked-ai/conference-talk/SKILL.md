---
name: conference-talk
description: "Take a conference talk from an idea to a proposal that gets accepted and a delivery that lands — the single takeaway, an abstract and outline a committee can say yes to, a structure that survives being heard once, slides that serve the spoken word, rehearsal, timing, delivery and Q and A. Use this skill whenever the user is submitting to a CFP or preparing to speak: drafting an abstract, choosing between talk ideas, building the outline or the deck, handling a rejection, cutting a talk to its slot, rehearsing, planning a live demo, or preparing for questions — including phrasings like \"the CFP closes friday\", \"i have 60 minutes of material and a 40 minute slot\", or \"how do i not fall apart on stage\". Do not use it for an article or blog post (that is write-technical-article), internal or executive updates (status-update), interview preparation (job-search), or notes on a talk you attended (learning-notes)."
allowed-tools: Read, Write, Edit, Glob, Grep, WebFetch
---

# Conference Talk

A talk has landed when someone in row twelve can repeat your one sentence to a colleague on Monday and act on it. Everything else in the deck exists to make that sentence believable.

The job is hard because a talk looks like an article delivered aloud, and it is not. A reader can re-read a sentence, skim to the part they need, look up a term and come back. An audience gets one pass, at your pace, in a dark room, after lunch, with a phone in their hand — so a structure that reads fine on paper falls apart when heard once. The proposal is a second, separate craft: a programme committee reads two hundred submissions and rejects most of them for reasons that have nothing to do with whether the talk would have been good. And the failure mode nobody warns about is preparation that feels like work but is not — building slides for a week and rehearsing in your head, then finding out on stage that the talk is nine minutes long or twenty over.

## Scope

Use for: choosing which talk to give, writing and rewriting a CFP submission, the abstract, the outline and the bio, finding the single takeaway, structuring the talk, building slides, planning a demo and its fallback, rehearsal and timing, delivery mechanics, Q and A, accessibility, and the follow-up after the talk.

Do not use for: written articles, blog posts and case studies (that is `write-technical-article` — hand the talk to it afterwards to turn it into a written piece), internal status or executive reporting (that is `status-update`), preparing for interviews (that is `job-search`), or capturing notes from a talk you attended (that is `learning-notes`).

## The honesty rules

These are not stylistic. A talk is a public claim about your own experience, delivered to people who work in the same field and will ask about it in the corridor afterwards.

- Do not invent an incident, a number, an outage, or an outcome. A talk built on an experience you did not have gets found out in the hallway track, by the one person in the room who ran that system.
- Do not present someone else's war story as yours. Credit it, and say what you learned from watching it rather than implying you were holding the pager.
- Get permission before naming an employer's outage, customer, or internal system, and get it from someone who can actually give it. Anonymise where the agreement requires it — "a payments provider at mid-eight-figure monthly volume" carries the mechanism without the name.
- Say "roughly" when it is roughly, and say "I do not have the number" rather than supplying a plausible one. The audience's trust in every other number in the talk rests on this.
- Where a claim comes from someone else's research or writing, name the source on the slide.

Mark anything you cannot yet evidence as `[TK: what you need]` in the draft and resolve it before the deck is finished. A `[TK]` that survives into a rehearsal becomes an unsupported sentence on stage.

## Workflow

### 1. Write the takeaway before anything else

One sentence. If an audience remembers exactly one thing, what is it. Write it down, then judge every candidate section by whether it makes that sentence more believable.

A takeaway is a claim someone could disagree with, not a topic. "Kubernetes operators" is a topic. "Most teams reach for an operator when a cron job and a health check would have done, and the operator costs you a maintainer" is a takeaway.

A talk with three main points has none, because an audience hearing it once retains the strongest and discards the others in an order you do not control. Three supporting movements under one claim is the same material, correctly arranged.

### 2. Choose the talk only you could give

Programme committees are selecting for a small number of things, and they are visible in the abstract.

| What the committee is looking for | What it looks like when missing |
| --- | --- |
| A specific claim, not a subject area | "An introduction to observability" — no reason to accept this one over the other eleven |
| A talk only this speaker could give | Material assembled from documentation and conference talks the committee has already seen |
| A named audience with a stated takeaway | "For everyone" — nobody leaves with anything |
| Evidence the talk exists | A description of a subject with no shape, which is how a half-formed idea reads |
| A speaker who can carry it | A bio inflated past what the talk demonstrates |

The strongest source of material is something you did that went differently than expected, with detail nobody who was not there could supply. Scars beat surveys.

### 3. Write the proposal as a separate piece of work

Most rejections are proposal problems, not topic problems. The committee is reading fast, comparing against similar submissions, and filling a schedule that needs range.

- **Title** — concrete and honest about what it is. Puns are fine when the subtitle carries the information; a pun alone is a submission the committee cannot place.
- **Abstract** — the audience-facing text, usually 150 to 250 words. Open with the specific problem, not with context-setting. State who this is for, what happened, and what they will be able to do afterwards. Write it in the voice the talk will be delivered in.
- **Outline** — the part that shows the talk exists. Sections with minutes against them and a one-line purpose each. A committee cannot tell a shaped talk from an intention without this, and the outline is where most submissions quietly fail.
- **Notes to the committee** — where the honesty goes: what is new here, what you are still building, whether it has been given before and where, what a related talk on the schedule would overlap with.
- **Bio** — establish standing for this specific talk in two or three sentences. What you built, what you run, how long. Inflating it is worse than a modest bio, because the talk then has to clear a bar you set yourself.

If a rejection comes back, read it as a scheduling and framing outcome rather than a verdict, rewrite the abstract around a sharper claim, and submit again elsewhere. Where a conference offers feedback, ask for it.

`references/proposal-craft.md` — read this while writing or rewriting a submission: worked abstracts before and after, how outlines are read, bios, and the CFP mechanics.

### 4. Structure it so it survives being heard once

Four parts, in this order.

1. **An opening that earns attention.** A concrete problem, a specific moment, a claim the audience did not expect. You have about ninety seconds before people decide whether to look at their phone, and an agenda slide spends all of them telling the audience what they are about to be told.
2. **Three or four movements.** Each one advances the takeaway and can be named in a short phrase. More than four and nobody can hold the shape; fewer and it is a lightning talk with padding.
3. **Signposting between them.** Say where you are: "that is the first of three failures — here is the one that actually cost us the weekend". People drift for thirty seconds at a time and rejoin at the signposts. Without them they rejoin lost and stay lost.
4. **An ending that concludes.** Return to the takeaway, say it once more in the words you want repeated, and stop. A questions slide is not an ending; it is the absence of one at the moment the audience is most likely to remember what you said.

Repetition that would be tedious in writing is necessary out loud. Say the takeaway at the start, at each movement boundary, and at the end.

### 5. Ground it in the specific

Real systems, real constraints, real numbers where you have them, and the moment where the obvious approach turned out to be wrong. Under the honesty rules above: what you cannot evidence does not go in.

Concrete detail is also what makes a talk memorable. "It was slow" is forgettable; "the p99 was 4.2 seconds and the SLO was 300 milliseconds, and it had been that way for five months without anyone noticing" is the sentence someone quotes.

### 6. Build slides that serve the spoken word

The deck is not the talk. If the deck reads perfectly on its own, one of the two is redundant, and it is not the deck that gets cut.

- One idea per slide. A slide that needs two sentences of explanation is two slides.
- No paragraph you intend to read out. The audience reads faster than you speak, finishes ahead of you, and then listens to you catch up.
- Diagrams legible from the back of a large room and in a photograph taken from it. Real minimum: 24pt body text, thick strokes, no more than about seven elements in a single view. Build a complex diagram up in stages instead of revealing it complete.
- Colour and contrast that survive a bad projector: high contrast, no thin light grey on white, no meaning carried by colour alone. Assume the room is bright and the projector is washing out.
- Slide numbers, so a questioner can refer to one.
- Your last slide holds the takeaway and how to reach you, not the word "questions". It is on screen for the whole Q and A.

### 7. Plan the demo and its fallback, or drop the demo

Live demos fail — network, laptop, a rate limit, a certificate that expired this morning, the projector negotiating a resolution your terminal hates. Assume something will.

Record a screencast of the demo working, at the pace you would run it, with the terminal font already enlarged. Decide in advance the exact moment you switch to it: one attempt, thirty seconds, no debugging on stage. Then say "here is the recording" and carry on. The audience forgives a fallback instantly and remembers four minutes of you squinting at a stack trace for years.

Prepare the environment too: everything pre-authenticated, notifications off, a clean shell, a font size chosen from the back of a room rather than at a desk.

### 8. Rehearse out loud, standing, timed

This is the step that separates talks that land from talks that do not, and it is the one that gets skipped because it is uncomfortable.

- Out loud. Rehearsing in your head runs about twice as fast as speech and hides every sentence you cannot actually say.
- Standing, with the slides advancing, in something like the posture you will be in.
- Timed, every run, written down. Note where you were at each movement boundary so you know mid-talk whether you are ahead or behind.
- At least once in front of a person who will tell you the truth, and ask them for the takeaway afterwards in their own words. If it is not your sentence, the structure is wrong, not the audience.
- Three full runs is a reasonable floor. The first is a mess; that is what it is for.

Time it to comfortably under the slot. A 30 minute slot means a 24 minute talk, a 45 minute slot means a 35 minute talk. Everyone runs long on stage — you speak faster in some places, you add a sentence, the previous session overruns, the microphone takes four minutes. Being cut off destroys the ending you built, which is the part that carries the takeaway.

### 9. Deliver

The mechanics are learnable, and none of them are personality.

| Element | What to do |
| --- | --- |
| Pace | Slower than feels natural. Nerves speed you up by a noticeable margin and you cannot feel it happening |
| Pauses | Stop for two seconds after each important sentence. It feels endless to you and reads as confidence to the room |
| Hands | Give them a job: the clicker, gesture at the screen. Not pockets, not the lectern edge, not your face |
| Eyes | Pick three points in the room, left, centre, right, and rotate. In a dark room aim at where the faces are, not the screen |
| Filler | Replace "um" with a pause. You do not have to fill the silence; the audience does not experience it as long |
| Notes | Speaker notes for structure and numbers, not a script. A read script sounds read |
| The screen | Do not turn your back on the room to read your own slides |

Nerves are not visible from the audience at anything close to the intensity you feel them. The racing heart, the shaking hands, the certainty that everyone can see it: none of that reaches row four. What does reach them is speaking too fast, so the one adjustment worth making mid-talk is slowing down.

Practical: arrive early and test the connector, the resolution and the microphone. Wear something the lapel microphone can clip to. Have water. Know whether there is a countdown clock and where it is.

### 10. Make it accessible by default

This is not an accommodation added at the end; it is a set of habits that make the talk better for everyone in the room and for everyone who watches the recording.

- Read the content of the slide aloud rather than saying "as you can see here". People at the back, people watching later on a phone, and people who cannot see the screen all get the same content.
- Describe the diagram in words as you walk it: what the boxes are, which way the arrows go, what changed between this build and the last.
- Repeat every question before answering it. The room usually cannot hear the questioner, and the recording certainly cannot.
- Speak into the microphone even when you think you are loud. The captions, the recording and the hearing loop all come from that feed, and stepping away from it silently drops all three.
- Do not carry meaning in colour alone; label the lines.
- Send slides or a transcript to the organisers in advance if captioning is being done live.

### 11. Run Q and A on purpose

Repeat the question, answer it briefly, move on. Two minutes per answer at most; a long answer is a second talk nobody chose.

- **When you do not know**: say so. "I do not know — that is a good question, find me afterwards and let us work it out" costs nothing and is the most credible sentence available to you. Inventing an answer is the fastest way to lose a room that had been with you.
- **The statement disguised as a question**: let them finish, extract anything answerable, respond to that in one sentence, and go to the next hand. "That sounds like a different experience from ours, and I would be interested to hear about it afterwards" ends it without a fight.
- **The hostile question**: answer the technical content, ignore the tone, and do not get drawn. The room is on your side more than it feels.
- **The question that is really about their situation**: give the general principle in one sentence and offer to talk afterwards.
- **When there are no questions**: have one ready. "The thing people usually ask me is..." restarts a stalled room.

### 12. Finish the job afterwards

- Post the slides within a couple of days, with the speaker notes included so the deck stands alone for people who were not there.
- Follow up with anyone whose question you could not answer. That is the highest-value contact the talk produced.
- Write the talk up. The article version reaches more people than the room did and lasts longer, and hand it to `write-technical-article` — the written form needs a different structure, not a transcript.
- Note what you would change while it is fresh: what ran long, which slide confused people, which question came up three times and belongs in the talk.

## Output format

```markdown
## Proposal — [conference], [deadline]

### Title
[Concrete. Says what the talk is about.]

### Takeaway
[The one sentence. Not submitted; everything below is judged against it.]

### Audience
[Who specifically, and what they already believe or currently do.]

### Abstract
[150-250 words, audience-facing, in the talk's voice. Opens with the problem.]

### Outline
[Section | minutes | purpose. Must add up to well under the slot length.]

### Why me
[The experience this rests on. What you actually did, and when.]

### Notes to the committee
[What is new, what is still being built, whether it has been given before.]

### Bio
[Two or three sentences. Standing for this talk, not a career summary.]

### Evidence to confirm
[Every [TK:] — numbers, permissions to name a system, sources to cite.]
```

```markdown
## Talk outline — [title], [slot length], [target length]

### Takeaway
[The sentence, in the words you want repeated.]

### Opening ([minutes])
[The concrete problem or moment. No agenda slide.]

### Movement 1 / 2 / 3 ([minutes] each)
[Per movement: the claim, the evidence, the slides, the transition line into
the next one.]

### Ending ([minutes])
[The takeaway restated, then stop. Final slide holds it plus contact details.]

### Demo
[What runs live, the fallback recording, and the exact moment you switch.]

### Cuts
[What comes out first if you are running long, decided now rather than on
stage.]

### Rehearsal log
[Date | run time | where it dragged | what changed]
```

## Anti-patterns

**A proposal about a topic rather than a claim.** The committee has eleven submissions on that subject and no reason to prefer yours. A claim is what makes the talk yours and the choice easy.

**Three main points.** An audience hearing it once keeps the strongest and loses the rest, so you do not control what they leave with. One takeaway with three movements under it is the same material with the retention problem removed.

**Reading the slides.** The audience reads faster than you speak, finishes before you, and disengages. It also means the deck already contains the talk, which raises the question of why they came.

**An agenda slide as the opening.** It spends the ninety seconds where attention is highest on telling people what they are about to be told, and it signals a talk assembled from a template rather than a claim worth making.

**A live demo with no fallback.** Demos fail on unfamiliar networks and projectors. Without a recording and a pre-decided switch point, the failure costs the middle of your talk and the audience's attention for the rest of it.

**Rehearsing in your head.** Silent rehearsal runs at roughly twice speaking pace, hides sentences you cannot actually say aloud, and gives you a timing figure that is wrong in the dangerous direction.

**Timing it to the exact slot length.** Nerves, a late start, microphone trouble and one extra sentence per section all push the same way. Being cut off removes the ending, which is where the takeaway lives.

**A deck that works without you.** If the slides carry the full argument, the talk is redundant and the audience is reading rather than listening. The deck should be unusable without the speaker and worth posting afterwards only because the notes are attached.

## Reference files

- `references/proposal-craft.md` — read while writing or rewriting a CFP submission: how committees read, worked abstracts before and after, outlines, bios, and handling rejection.
- `references/delivery-and-rehearsal.md` — read in the two weeks before the talk: the rehearsal protocol, cutting to time, the room and equipment checklist, voice and nerves, and Q and A handling.
