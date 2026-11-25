---
name: vividness
description: Pushes a draft from abstract toward concrete at two scales. Noun-level (replaces "dog" with "German shepherd," "customer" with "Sarah at JPMorgan's options-trading desk," "many" with "47 of 100") and scene-level (turns "I was angry" into the body signal, room, and dialogue). Implements Kramon's "specific over abstract" rule, Kristof's "real names, real numbers, real interviews," and Lauren Weinstein's "could a director recreate this scene?" test. Use when a draft is technically correct but flat, when category nouns leak through, when stories tell instead of show, or when the user says "be specific," "show don't tell," "more vivid," "less abstract," "make it concrete," "find the colors." Pass --mode noun-level|scene-level|both (default both).
---

# Vividness

Source: `points/core-rules.md` rule 2 (know your audience), Kramon's rule that **stories are 12× more memorable than statistics alone**, Lauren Weinstein's guest lecture in Glenn Kramon's *Winning Writing* (GSB, Spring 2026).

## What this skill does

Two modes behind one skill. Both push abstract → concrete; they operate at different scales:

| Mode | Replaces | Use when |
|---|---|---|
| **noun-level** | "dog" → "German shepherd," "customer" → "Sarah at JPMorgan," "many" → "47 of 100" | Draft has category nouns the reader has to fill in |
| **scene-level** | "I was angry" → body signal + room + dialogue + moment | Story is technically correct but flat |

Default `--mode both` runs noun-level first (fixes generic words), then scene-level (turns key moments into scenes). The order matters: noun replacements provide the concrete material a scene needs.

## How to invoke

```
/vividness "draft text"
/vividness --mode noun-level "draft text"
/vividness --mode scene-level "draft text"
/vividness --mode both "draft text"
```

Without `--mode`, default to `both`.

## A note on examples

Named "Sarah at JPMorgan" and "Priya at DoorDash" cases below are *fictional* people in fictional scenarios at real public companies. They exist as teaching shapes — named person + named institution + specific quote — not as anyone's real story. The real version of this skill uses real names.

---

## Mode 1 — noun-level

Generic nouns force the reader to do work the writer should have done.

> *"A scientist studied dogs."*

Forgettable. The reader pictures nothing.

> *"Dr. Chen at UC Davis studied 47 German shepherds at a sheep-herding farm in Petaluma."*

The reader can see it. Specificity is the single highest-leverage rewrite a draft ever gets.

### The replacement table

| Generic | Specific |
|---|---|
| dog | German shepherd, Alma my golden retriever, the puppy at the rescue |
| engineer | John, the SRE on the payments team |
| customer | Sarah at JPMorgan's options-trading desk |
| city | Bozeman (population 56,000, mountain west) |
| big company | Stripe (~7,000 employees, $1T+ payment volume annually) |
| recent study | the 2024 Stanford HAI paper on agent reliability |
| many people | 47 of the 100 PMs I interviewed |
| a long time | 38 minutes |
| somewhere | the Fillmore in 1989 (named venue, named year) |
| early | 2:47 a.m. last Wednesday |
| executives | the VP of Talent at Stripe |
| consultant | a McKinsey BA who left to start a SaaS company |
| AI tool | Claude Sonnet 4.6 with the web_search tool |
| school | Stanford GSB's section H |
| job | director of products at a 20-person fintech in Austin |
| money | $64M in net savings |
| feedback | "this is good but the part about latency is wrong" |

### Six categories to fix (priority order)

**1. People** — first names + roles + locations wherever you have permission.
❌ *"A customer told us our latency was a problem."*
✅ *"Sarah at JPMorgan's options-trading desk told us in March: 'every 100ms costs us a million dollars in slippage.'"*

If no permission, use a *specific archetype*: *"a senior options trader at a top-tier investment bank, 12 years in the seat."*

**2. Numbers** — actual numbers or tight ranges, not "many" / "few" / "significant."
❌ *"We saw a significant drop in errors."*
✅ *"Errors dropped from 4,200/day to 380/day — a 91% reduction."*

If you don't know it, get it before publishing. If you can't, name the closest measurable proxy.

**3. Places** — named locations. Specificity here is free.
❌ *"At a tech company in California…"*
✅ *"At Stripe's South San Francisco office on Oyster Point…"*

**4. Times** — dates and durations.
❌ *"We launched the new pricing recently."*
✅ *"We launched the new pricing on March 14, 2026 — six weeks ago."*

**5. Things** — make/model/version/brand.
❌ *"a robot," "a coding model," "a phone"*
✅ *"the Meccano MeccaNoid G15," "Claude Sonnet 4.6," "an iPhone 16 Pro"*

Especially load-bearing in tech writing — *"an LLM"* is almost meaningless in 2026.

**6. Quotes vs. summaries** — the actual sentence in quotes.
❌ *"Customers love the new feature."*
✅ *"Priya at DoorDash, last Thursday: 'The brief is good, but it doesn't save us from the part that hurts.'"*

### When generic wins (three cases)

1. **Privacy / NDA.** Use a precise archetype; don't fake a name.
2. **Universality is the point.** *"Most people who fall in love"* shouldn't have a name — specificity shrinks the claim.
3. **Specificity would distract.** Naming a product is fine; naming MSRP, review count, star rating is a fetish.

---

## Mode 2 — scene-level

Most people summarize their stories:

> *"It was a difficult time. I didn't have money. I didn't have hope. Things looked dismal."*

That tells the audience what happened. The same story, shown:

> *"Six days a week I ate beans and weenies. I dug for change in the crevices of my couch so I could buy my son milk. There were nights my heart raced. I got sick of my own story."*

Same facts. Now the reader is in the room.

The work is what Weinstein called *finding the colors*: going back through the story and naming what the storyteller was thinking, seeing, and feeling in the body.

### The three questions (for every important moment)

**1. What were you seeing?**
The room, the couch, the phone, the food, the facial expression, the screen, the weather, the temperature, the object in your hand.

**2. What were you thinking?**
The internal dialogue. The question you were asking yourself. The fear in the back of your mind.

**3. What were you feeling in your body?**
Not the emotion label. The body signal. Heart racing. Throat tight. Chest heavy. Hands shaking. Heat rising. Wanting to disappear.

If the storyteller can answer these three for the pivotal moment, the scene starts to come alive.

### The director test

Weinstein's standard:

> **Could a movie director recreate this scene from what you wrote?**

If yes, vivid. If no, still abstract.

Three examples that pass:

- **Steve Jobs** doesn't say "I was resourceful." He says he was 12, looked up Bill Hewlett's number in the Palo Alto phone book, called him, asked for spare parts, got a summer job.
- **Oprah** doesn't say "Sidney Poitier inspired me." She says she was sitting on the linoleum floor of her mother's house in Milwaukee, watching the Oscars, while her mother came home bone-tired from cleaning other people's houses.
- **Brené Brown** doesn't say "I felt ashamed after reading online comments." She shows herself checking the YouTube view count, reading cruel comments, sitting in Houston with peanut butter, *Downton Abbey*, Uggs, a hoodie, the thermostat at 58.

### Replace emotion labels with body signals

| Label | Body signal |
|---|---|
| I was stressed | I refreshed the inbox every thirty seconds, knowing nothing had changed |
| I was poor | I counted coins from the couch cushions to buy milk |
| I was angry | The hair on my neck stood up; I bit back the sentence I knew I'd regret |
| I was scared | I read the message three times, then put the phone face-down |
| I worked hard | The office was dark except my screen; the deck still had 17 red comments at midnight |
| I was proud | When the customer said yes, I looked down because I didn't want the team to see me tear up |
| I was exhausted | I sat in the car for ten minutes before I could open the door |
| I was disappointed | I closed the laptop without saying anything and walked to the kitchen |

The pattern: name the action, the object, the body, or the moment that made the emotion show.

### Story spine — Situation → Action → Result

A vivid scene still needs a spine:

1. **Situation.** Person, place, time, tension. Who, where, when, what's at stake.
2. **Action.** Something happens. The character does something specific.
3. **Result.** Something changes. The audience learns something.

Steve Jobs: *Situation:* 12, Palo Alto, wants a frequency counter. *Action:* Calls Hewlett cold. *Result:* Gets parts and a summer job. Audience learns: this kid asks.

Each example above is Situation → Action → Result. Each one passes the director test.

### Avoid melodrama

The opposite failure mode is overwriting:

- **One body signal per moment, not three.** "My heart raced and my throat tightened and my hands shook" reads as parody.
- **Specific objects beat lyrical adjectives.** "Beans and weenies" beats "humble fare." "Thermostat at 58" beats "the room was cold."
- **Trust the reader.** Don't follow the scene with a paragraph explaining what it meant.

---

## How to run the pass

### Pass 1 — Inventory

**noun-level:** underline every generic noun (user, customer, engineer, many, recently, a city, an app). Count.

**scene-level:** mark every abstract / summarized line ("it was hard," "I felt lost," "I worked through it"). Count.

### Pass 2 — Replace

**noun-level:** for each generic, find the most specific replacement you can verify. If unknown, write `[lookup: …]` so the user can fill in.

**scene-level:** pick the pivotal moment (not every line). Ask the three questions. Add the concrete details. Run the director test.

### Pass 3 — Spine check

Confirm Situation → Action → Result is visible in any rewritten story.

### Pass 4 — Cut what doesn't carry weight

If a generic noun is doing real work (universality), keep it. If a sentence is throat-clearing, cut it. Don't replace vague with longer vague.

## Output format

```
## Inventory
noun-level hits: N (generic words)
scene-level hits: N (abstract claims)

## Noun-level replacements
1. Line X: "the original sentence"
   → "the rewritten sentence with specifics"
   Replaced: <generic> → <specific>
   Source: <interview / podcast / lookup needed>

## Scene-level rewrites
1. Abstract claim: "[the line]"
   → vivid scene: "[the rewrite]"
   Added: object/setting + body signal + dialogue + moment
   Director test: yes/no, one-line justification
   Spine: Situation / Action / Result

## Lookups needed
- [lookup: customer name in the JPMorgan story]
- [lookup: exact MAU number in March 2026]

## Clean draft
[Full text with replacements applied. Lookup placeholders preserved.]
```

## The litmus test

After the rewrite, can the reader picture the scene?

- Do they see a specific dog, or a category dog?
- Do they hear Priya's voice, or a paraphrase?
- Did the writer tell them they felt sad, or did the reader feel sad reading it?

If still "category" anywhere, run another pass.

## When NOT to use

- **Status updates, operational memos.** Exec readers want the headline. Use `bluf-rewriter` or `headline-as-claim`.
- **Technical specs, design docs.** The reader wants the system, not the writer's interior life.
- **Resume bullets.** Bullets compress; scenes expand.
- **Twitter, headlines, six-word summaries.** Compression beats vividness.
- **Writing where the user wasn't actually present.** Don't fabricate sensory detail you didn't experience.
- **NDA / privacy constraints on names.** Use precise archetypes instead.

## The Kramon + Weinstein rule

> *"Stories are 12× more memorable than statistics alone."* — Kramon
> *"Could a director recreate this scene?"* — Weinstein

The most memorable writing has both: the named person, doing the specific thing, in the named place, with the actual number, with the body signal that makes the moment real. Take any forgettable sentence and ask: *whose face is in the picture? Could a film crew shoot this?* If the answer is no to either, run a pass.
