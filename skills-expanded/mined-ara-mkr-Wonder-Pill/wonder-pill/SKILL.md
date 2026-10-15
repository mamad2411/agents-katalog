---
name: wonder-pill
description: Turns open-ended requests into things to think WITH instead of answers to accept. Audits the hidden assumptions inside a topic, inverts them into sharp "what if" provocations, branches each one outward, and delivers a fully-expanded mind map image plus the written wonderings. Fire this when the person signals they want to open up a space and think alongside you — "wonder about X", "what are the weird angles on X", "help me think about what this could be", "I want to explore, not decide yet" — or when they invoke /wonder or /wonderpill. Do NOT fire when the same topic is attached to a request for concrete, usable, or decided output: a named deliverable, a count ("give me 5 names"), a deadline ("ideas I can ship this week"), or a "which / what should I pick" question — those want straight answers, not a wonder pill. When it is genuinely unclear which they want, this skill opens by asking one line rather than branching. Not for factual lookups or executing a plan already chosen.
---

# Wonder Pill

## What this skill is for

Ordinary brainstorming gets treated like a search query: find the nearest well-trodden answers, rank them, hand them over. That produces a list the person picks from, which quietly makes them the *chooser* instead of the *thinker*, and anchors them to whatever you happened to say first.

This skill produces something different: **provocations to think with.** Questioned assumptions, sharp what-ifs, and branches that keep going — handed back as a map of the thought-space rather than a recommendation. The person stays the thinker. Nothing converges unless they ask it to.

## The one failure mode that matters

The thing that kills this skill is **"generic wild"** — what-ifs that *sound* expansive but have no hook to pull on. "What if plants were different?" is worse than useless: it hands the work back without giving anything to push against. "What if plants could hear?" is alive, because you can immediately feel what would have to change.

Everything below exists to force specificity. The central mechanism:

> **Never invent a what-if freely. Always derive it by inverting a named assumption.**

That traceability is the whole trick. If you can't say which assumption a what-if is pushing against, it isn't ready.

---

## Before you run: is this actually a wonder-pill ask?

This skill is easy to trigger by accident on someone who just wants ideas they can use. Check first:

- **If the request clearly wants concrete or decided output** — a named deliverable, a count, a deadline, "which should I pick" — don't run. Answer normally, and mention the skill is there if they'd rather open the space than close it.
- **If it's genuinely ambiguous**, ask exactly one line before any intake, using `ask_user_input_v0` (tappable): *"Want a wonder pill — questioned assumptions and what-ifs to think with — or a straight list of ideas you can act on?"* Only start branching if they pick the wonder pill.
- **An explicit `/wonder`, `/wonderpill`, or "wonder about X" skips this check.** They asked for it by name; go straight to Stage 0.

---

## Stage 0 — Intake

Ask **three questions, no more**, before any thinking. These aren't generic clarification — the quality of a what-if is almost entirely determined by how far it's allowed to drift from the person's reality, and that's unguessable. "What if plants could hear" is great for a curious kid and useless for someone submitting a materials list in three days.

Use `ask_user_input_v0` (tappable options are much easier than typing):

1. **Leash length** — "Pure wondering, or does something eventually have to get built/submitted/decided?" → options like *Pure wondering* / *Should be buildable eventually* / *Has a real deadline*
2. **Hard walls** — "Anything I shouldn't bother questioning?" → options like *Budget* / *Timeline* / *Materials on hand* / *Nothing, go wild*
3. **Opening move** — "Want me to hunt for a genuinely weird real fact to start from, or work from your framing as-is?" → *Go find something weird* / *Start from my framing*

**Skip intake entirely** if the request already answers all three. A person who writes "I have two weeks, $30, and it has to fit on a poster board" has told you everything; asking again is annoying and wastes their patience.

---

## Stage 1 — Oddity hunt (once per session only)

If Stage 0 gave permission, take **one cheap pass** to find a genuinely odd, specific fact or unresolved tension in the topic. Search if that helps. This becomes the session's opening spark and sets the tone — it's the most alive entry point because it's rooted in something real rather than an abstract inversion.

Two rules:

- **Once per session, never per branch.** Per-branch oddity hunting becomes padding, slows everything down, and starts to feel like showing off.
- **Fail fast.** If nothing genuinely odd surfaces quickly, drop it without ceremony and move on. A forced "huh, interesting" is worse than not doing this at all.

A real oddity is specific and slightly uncomfortable — a thing that shouldn't work but does, a measurement nobody can explain, two accepted facts that don't quite fit together. Not a trivia factoid.

---

## Stage 2 — Assumption audit (the backbone)

Surface **3–5 load-bearing assumptions** buried in the request. Load-bearing means: if it stopped being true, the shape of the whole thing would change.

For "science fair project," the buried assumptions might be:
- it needs a physical demo
- it needs results measurable in one sitting
- one person builds it
- it uses materials you can buy
- the judges have to understand it in three minutes

Rules that keep this honest:

- **State each assumption plainly as a premise, not as a question.** The premise is a separate artifact from the what-if, and writing it out is what prevents drift into vagueness.
- **Drop anything the person named as a hard wall.** Those aren't up for inversion — inverting them produces useless output dressed as boldness.
- **Prefer the assumptions nobody says out loud.** "Needs to be safe" is stated. "Has to be *finished*" usually isn't, and inverting it is far more interesting.
- **Then invert each one. The inversion IS the what-if.** One per assumption. Write it as a **full self-contained sentence that names the mechanism or consequence** — something a stranger could read cold and know what changed. "What if plants could hear, and had been responding to sound the whole time?" — not "plant hearing". This sentence, trimmed, becomes the node's **handle** on the map (see Stage 5); a noun fragment is never a handle.
- **Keep the seed.** When an assumption came from somewhere — a real fact, a historical precedent, an oddity from Stage 1 — record where. These become *seed* nodes on the map, sitting outside their branch, showing why the thought happened at all. A map that shows its provenance is far more useful than one that presents conclusions from nowhere.

### Good vs. bad inversions

| Assumption | Weak what-if (generic wild) | Strong what-if (has a hook) |
|---|---|---|
| A project has to be finished to be judged | What if it weren't finished? | What if the project were a *thing still running* — measurements arriving during the judging, no known result yet? |
| Plants don't perceive stimuli like animals do | What if plants were different? | What if plants could hear, and had been responding to sound the whole time? |
| The experiment happens where you are | What if location changed? | What if the same experiment ran in 40 kitchens at once and the *disagreement between them* was the data? |

The pattern: strong what-ifs name a specific mechanism or consequence, so there's something to grab. Weak ones just negate. The strong-column phrasing *is* the map handle — write the what-if that way the first time and you don't have to reword it later.

Then pair each what-if with a one-clause **pull**: what you'd push on, what would have to change, why it's alive. "…and every acoustics choice in the room becomes a growing decision." The handle says what the what-if is; the pull says where the thread has tension. Both ride on the node.

---

## Stage 3 — Tendrils (keep branches from dead-ending)

Each what-if from Stage 2 spawns **2–3 follow-on what-ifs** — "and if that's true, then…". This is where the *wondering* quality comes from; a single question that stops after one hop reads like a prompt, not thinking.

Each tendril gets the same two parts as a branch: a **handle** (a full sentence that could stand alone on the map, not a fragment) and a one-clause **pull**. "seawater as a curing agent" is not a tendril; "what if seawater cured the concrete instead of weakening it, the way Roman harbour concrete did" is.

Generate tendrils by running the branch through these **dimensions**, rather than freewheeling (freewheeled tendrils feel arbitrary):

- **Scale** — 1000× bigger, or small enough to be invisible
- **Time** — much slower, much faster, or running forever
- **Reversal** — swap cause and effect; run it backwards
- **Audience** — built for someone it was never meant for
- **Material** — made of the wrong substance entirely
- **Sense** — perceived through a different channel (sound, smell, touch)
- **Causality** — what if the thing you thought was the output is actually the input

**Vary which dimensions you use across branches.** Running all five branches through "scale" makes the output read like a template, which is its own kind of death.

**Let depth be uneven.** Some branches deserve one hop; some deserve four. If a tendril opens a real question, follow it — tendril to sub-wondering to sub-sub-wondering. A map where every branch is exactly three deep is a map that stopped thinking on schedule rather than when the thread ran out. Uneven depth is evidence of actual attention.

**Keep the scraps.** When a what-if gets generated and then discarded, don't delete it — log three separate things about it, not one blended line:

- **Derivation** — which assumption or dimension it came from, same as a branch's premise.
- **Flaw** — what's actually wrong with it, stated plainly.
- **Judgment call** — a separate sentence saying *why that flaw was disqualifying.* Not a restatement of the flaw — the reasoning that got from flaw to "kill it."

**Plausibility and generativity are different axes, and only one of them may kill a what-if.** A what-if may be scrapped for failing *generativity* — it's a genuine dead end, nothing more to ask once you're standing in it. It may **never** be scrapped for failing *plausibility* — sounding unlikely, weird, or hard to build is not a valid reason on its own. Implausible-but-generative stays every time; plausible-and-flat can still die. Say so explicitly in the judgment-call line: name that this was checked against "does it open anything further," not "does it sound reasonable."

This distinction has to be written down and applied deliberately because the kill decision happens in the same breath as the generation — there's no outside check on it, which is exactly the moment a bias toward safe-sounding output would sneak back in unannounced.

Worked example: "What if the bridge floated?" — **derivation:** inverting the assumption that a bridge has to be a fixed structure. **flaw:** trades a 500-year erosion problem for a 5-year mooring-maintenance problem. **judgment:** scrapped for generativity, not plausibility — floating is perfectly buildable, but the thread just swaps one bounded maintenance problem for another and doesn't open a new question past that trade.

Scrapped threads live detached at the edge of the map, not attached to any branch — and the person can still see all three fields and disagree with the call.

---

## Stage 4 — Gut-check pass

One line per branch naming **where the real difficulty or interest is buried.** Not an answer. Not a feasibility verdict. It tells the person where to push if they chase that thread.

Shape: *"This only gets interesting if the hard part is actually X, not Y."*

Also tag each branch **tethered** or **feral**:
- **tethered** — has a plausible shadow back in reality; something could be built or tested from it
- **feral** — pure provocation, kept deliberately because it might spark something sideways

**Never prune the feral ones.** They're not failures of the process, they're the point of allowing the process to run loose. The tags feed the map's styling in Stage 5.

---

## Stage 5 — Deliverable

Three parts, **in this order**. Read `references/mindmap.md` before rendering the map — clutter is the real risk and that file has the layout spec.

### 1. The mind map — interactive

An explorable HTML map rendered inline, fully expanded from the start: drag to pan, buttons to zoom, click any node to read its gut-check. Nothing hidden behind a reveal — the whole thought-space exists at once and the person moves around inside it.

It must **not** look like a tidy tree radiating uniformly from a center. Real thinking isn't uniform, and a map that pretends otherwise hides the information the person actually wants. So:

- **Branches sit at different distances and different angles** around the topic, in whatever direction they were reached from.
- **Seed nodes sit outside their branch**, further from the center than the thing they caused — the map reads inward as well as outward. This is where "why did it think that" lives.
- **Depth varies per branch.** One hop where the thread ended, four where it kept going.
- **Scrapped what-ifs float detached** at the edges, struck through, showing all three of: where it came from, what's wrong with it, and why that was judged disqualifying.
- **Cross-links** connect branches that collided on the same tension — this is what makes it a web rather than a tree.
- **Every node states itself in plain language.** Handle is a full phrase, pull line names what to push on. The map should be readable on a first pan-through without clicking a single node — the click is for the deeper gut-check, not for decoding what the node meant.

Render it with the Visualizer (call `visualize:read_me` with the `diagram` module first, silently — never narrate loading it). Read `references/mindmap.md` for the build spec; it is written against the Visualizer's real constraints, which are stricter than they look. When someone wants to record or present the map, also write a standalone `.html` copy to the outputs directory and present it.

### 2. Orientation paragraph

Short. Names the **throughlines, not the nodes**: which tension kept recurring, which direction turned out most interesting, where it went genuinely feral. This orients the person *before* they read the map — it is not a synopsis of it. Listing the nodes back in prose is wasted space; they're right there in the image.

### 3. The written wonderings

The readable linear companion, for anyone who'd rather read than scan. Per branch, exactly this spine:

```
### [Short branch title]
**Premise:** [the assumption, stated plainly]
**What if:** [the sharp provocation — the full handle sentence]
- **[tendril handle]** — [the pull: what it opens or what you'd push on]
- **[tendril handle]** — [the pull]
- **[tendril handle]** — [the pull]
**Gut-check:** [where the real difficulty or interest hides]
```

---

## Stage 6 — End open

**Do not converge.** Close with an invitation only — something like *"if one of these is itching at you, say which and I'll go deeper on just that thread."*

The strongest temptation in this whole skill is to quietly turn back into a recommendation engine by the last paragraph — ranking the branches, picking a favorite, suggesting which is most practical. That undercuts the entire premise. The person asked for a space to think in, not a verdict. If they want convergence they'll say so, and then you can help them land one.

## If they pick a thread

Re-run Stages 2–4 on that single branch. The branch becomes the new topic; its tendrils become the new assumptions to audit. Skip intake (already calibrated) and skip the oddity hunt (already spent). Still don't converge.
