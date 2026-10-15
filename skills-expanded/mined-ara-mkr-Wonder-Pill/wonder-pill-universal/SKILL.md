---
name: wonder-pill-universal
description: Turns open-ended requests into things to think WITH instead of answers to accept. Audits the hidden assumptions inside a topic, inverts them into sharp "what if" provocations, branches each one outward, and delivers a mind map plus written wonderings. Portable version, no vendor-specific tools required, works on any conversational assistant. Fire this when the person signals they want to open up a space and think alongside the assistant: "wonder about X", "what are the weird angles on X", "help me think about what this could be", "I want to explore, not decide yet". Do NOT fire when the same topic is attached to a request for concrete, usable, or decided output: a named deliverable, a count ("give me 5 names"), a deadline, or a "which / what should I pick" question. When it is genuinely unclear which they want, this skill opens by asking one line rather than branching. Not for factual lookups or executing a plan already chosen.
---

# Wonder Pill (Universal)

This is a portable version of the Wonder Pill skill. It works as plain written instructions for any conversational assistant — ChatGPT, Kimi, opencode, Antigravity, Z.ai, or anything else that can read a system prompt / custom instructions and hold a conversation. It assumes nothing vendor-specific: no special question-asking UI, no dedicated diagramming tool, no guaranteed live JavaScript execution.

## What this skill is for

Ordinary brainstorming gets treated like a search query: find the nearest well-trodden answers, rank them, hand them over. That produces a list the person picks from, which quietly makes them the *chooser* instead of the *thinker*, and anchors them to whatever was said first.

This skill produces something different: **provocations to think with.** Questioned assumptions, sharp what-ifs, and branches that keep going — handed back as a map of the thought-space rather than a recommendation. The person stays the thinker. Nothing converges unless they ask it to.

## The one failure mode that matters

The thing that kills this skill is **"generic wild"** — what-ifs that *sound* expansive but have no hook to pull on. "What if plants were different?" is worse than useless: it hands the work back without giving anything to push against. "What if plants could hear?" is alive, because you can immediately feel what would have to change.

Everything below exists to force specificity. The central mechanism:

> **Never invent a what-if freely. Always derive it by inverting a named assumption.**

That traceability is the whole trick. If you can't say which assumption a what-if is pushing against, it isn't ready.

---

## Before you run: is this actually a wonder-pill ask?

This skill is easy to trigger by accident on someone who just wants ideas they can use. Check first:

- **If the request clearly wants concrete or decided output** (a named deliverable, a count, a deadline, "which should I pick"), don't run. Answer normally, and mention the skill is there if they'd rather open the space than close it.
- **If it's genuinely ambiguous**, ask exactly one line before any intake: *"Want a wonder pill, questioned assumptions and what-ifs to think with, or a straight list of ideas you can act on?"* Only start branching if they pick the wonder pill.
- **An explicit "/wonder", "/wonderpill", or "wonder about X" skips this check.** They asked for it by name; go straight to Stage 0.

---

## Stage 0 — Intake

Ask **three questions, no more**, before any thinking. Ask them as a plain numbered list in the chat and wait for a reply:

1. **Leash length** — "Pure wondering, or does something eventually have to get built / submitted / decided?"
2. **Hard walls** — "Anything I shouldn't bother questioning? (budget, timeline, materials on hand, or nothing — go wild)"
3. **Opening move** — "Want me to hunt for a genuinely weird real fact to start from, or work from your framing as-is?"

These aren't generic clarification — the quality of a what-if is almost entirely determined by how far it's allowed to drift from the person's reality, and that's unguessable. "What if plants could hear" is great for a curious kid and useless for someone submitting a materials list in three days.

**Skip intake entirely** if the request already answers all three. A person who writes "I have two weeks, $30, and it has to fit on a poster board" has told you everything; asking again is annoying and wastes their patience.

---

## Stage 1 — Oddity hunt (once per session only)

If Stage 0 gave permission, take **one cheap pass** to find a genuinely odd, specific fact or unresolved tension in the topic. Use a search tool if one is available; otherwise draw on what you already know. This becomes the session's opening spark and sets the tone — it's the most alive entry point because it's rooted in something real rather than an abstract inversion.

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
- **Then invert each one. The inversion IS the what-if.** One per assumption. Write it as a full self-contained sentence that names the mechanism or consequence, something a stranger could read cold and know what changed. "What if plants could hear, and had been responding to sound the whole time?" not "plant hearing". That sentence, trimmed, becomes the node's **handle** on the map. A noun fragment is never a handle. Pair each what-if with a one-clause **pull**: what you would push on, what would have to change, why it is alive.
- **Keep the seed.** When an assumption came from somewhere — a real fact, a historical precedent, an oddity from Stage 1 — record where. These become *seed* nodes on the map, sitting outside their branch, showing why the thought happened at all. A map that shows its provenance is far more useful than one that presents conclusions from nowhere.

### Good vs. bad inversions

| Assumption | Weak what-if (generic wild) | Strong what-if (has a hook) |
|---|---|---|
| A project has to be finished to be judged | What if it weren't finished? | What if the project were a *thing still running* — measurements arriving during the judging, no known result yet? |
| Plants don't perceive stimuli like animals do | What if plants were different? | What if plants could hear, and had been responding to sound the whole time? |
| The experiment happens where you are | What if location changed? | What if the same experiment ran in 40 kitchens at once and the *disagreement between them* was the data? |

The pattern: strong what-ifs name a specific mechanism or consequence, so there's something to grab. Weak ones just negate. The strong-column phrasing *is* the map handle, so write the what-if that way the first time.

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

**Vary which dimensions you use across branches.** Running all branches through "scale" makes the output read like a template, which is its own kind of death.

**Let depth be uneven.** Some branches deserve one hop; some deserve four. If a tendril opens a real question, follow it — tendril to sub-wondering to sub-sub-wondering. A map where every branch is exactly three deep is a map that stopped thinking on schedule rather than when the thread ran out. Uneven depth is evidence of actual attention.

**Keep the scraps — and show the reasoning behind each one.** When a what-if gets generated and then discarded, don't delete it. Log three separate things, not one blended line:

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

Three parts, **in this order.**

### 1. The mind map

Build **one self-contained HTML file** — inline CSS and JS only, no external stylesheets, fonts, CDNs, or network calls, since most sandboxes block them and you can't rely on internet access at render time anyway. Then:

- **If your host has a canvas / artifact / live-preview pane that renders HTML inline, use it, so the person sees the map directly.**
- **If it doesn't, or you're not sure it does, just hand over the file** — as a normal code block the person can save as `example.html` and open in any browser, or written directly to disk if you have file-write access (coding-agent style tools). It is the exact same content either way; only the delivery path changes. Don't spend time guessing what a specific platform supports — produce the file, then use whichever delivery path is available.
- **If a host genuinely cannot accept a large HTML block at all** (rare — some bare-bones text-only APIs), fall back to the plain markdown outline described at the end of this section instead.

Build rules for the HTML file:

- No `position: fixed`. Controls go in normal document flow.
- Support both light and dark viewing: define colors as CSS custom properties on `:root`, then override them under `@media (prefers-color-scheme: dark)`. Never hardcode a hex color directly on an element.
- Never rely on color alone to distinguish node types — pair every category with a border style (solid / dashed / dotted) and/or a text label.
- Every visible node carries two lines that render on the node itself: a **handle** (a full plain-language phrase, about 4 to 9 words, saying what the node is) and a **pull** (one shorter muted clause naming what to push on or why it is alive). The map should read on a first pass without clicking anything; the click is for the gut-check, not for decoding the node.
- Node types and their styling:
  - `topic` — solid border, filled background, medium weight text, handle only
  - `branch` — solid border, tinted background, premise shown as a smaller muted line above the handle, then handle, then pull
  - `tendril` — no border or a single side rule, plain background, handle then pull
  - `seed` — dotted border, muted text, labeled "seed", handle then pull
  - `scrapped` — dashed border, reduced opacity, handle struck through; show its derivation as a small muted line and put the flaw + judgment in a detail area
  - `feral` branch — dashed border instead of solid, labeled "feral"
- Layout radially but **deliberately unevenly** — branches sit at different distances and angles from the center topic, not a tidy uniform ring. Seeds sit further out than the branch they caused. Scrapped nodes float in an unused margin, connected by nothing or a faint dotted stub. A few dashed cross-links connect branches that landed on the same underlying tension, but a cross-link must never cut through a node box.
- Minimum interaction, in order of importance: pan (drag), zoom (`+`/`−`/reset buttons — skip wheel-zoom, it hijacks page scroll), and click-a-node to reveal its full text (premise, tendrils, gut-check, or for scrapped nodes: derivation/flaw/judgment) in a detail area below the map, never a floating overlay.
- Build the map from a small JS data array (nodes + edges) and render it in a loop, rather than hand-writing dozens of absolutely-positioned elements — it's far less error-prone and easier to keep consistent.

**Plain markdown outline (rare fallback only):** if HTML genuinely isn't an option, render the same structure as a nested outline instead:

```
TOPIC: <topic>

SEED: <fact> (why: <which branch it seeded>)

BRANCH: <what-if handle> [tethered|feral]
  premise: <assumption>
  - <tendril handle> — <pull>
    - <sub-tendril handle> — <pull>
  - <tendril handle> — <pull>
  gut-check: <where the difficulty hides>

~~SCRAPPED: <what-if>~~
  derivation: <assumption/dimension it came from>
  flaw: <what's wrong with it>
  judgment: <why that flaw was disqualifying — generativity, not plausibility>
```

Keep the same rules even in plain text: uneven depth per branch, scraps struck through with all three fields, seeds shown with what they seeded, feral branches labeled.

### 2. Orientation paragraph

Short. Names the **throughlines, not the nodes**: which tension kept recurring, which direction turned out most interesting, where it went genuinely feral. This orients the person *before* they read the map — it is not a synopsis of it. Listing the nodes back in prose is wasted space; they're right there in the map.

### 3. The written wonderings

The readable linear companion, for anyone who'd rather read than scan. Per branch, exactly this spine:

```
### [Short branch title]
**Premise:** [the assumption, stated plainly]
**What if:** [the sharp provocation, the full handle sentence]
- **[tendril handle]** — [the pull: what it opens or what you would push on]
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

---

## Portability notes

This file makes no assumption about vendor-specific tools, function-calling conventions, or UI widgets. It only assumes the host is a conversational assistant that can:

- read and follow multi-stage written instructions
- ask the user plain-text questions and wait for replies
- produce a fenced HTML code block, and either render it inline or hand it over as a file

That covers general-purpose chat assistants (ChatGPT, Kimi, Z.ai, and similar), coding-agent CLIs that write files to disk (opencode, Antigravity, and similar), and anything in between. If a host offers a genuinely better rendering surface than plain HTML, use it — the point of Stage 5 is "richest thing you can actually deliver," not "exactly this file format forever."
