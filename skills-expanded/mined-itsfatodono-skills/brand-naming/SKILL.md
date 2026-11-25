---
name: brand-naming
description: Create and evaluate brand, product, company, or feature names with a naming-agency process: a strategy brief, blind parallel exploration at volume, sound-symbolism engineering, and screening down to 3-5 defensible finalists. Use this whenever the user needs to name or rename anything — company, product, app, feature, library, open-source project, model, domain, tagline-adjacent naming — or wants existing candidates judged. Trigger on phrasings like "what should we call this", "need a name for", "naming ideas", "is X a good name", "help me rebrand", "working title", "codename", or whenever a project is running on a placeholder name and the user asks for something better. Also trigger when the user has a shortlist and wants it critiqued, scored, or narrowed. Not for naming code identifiers such as variables, functions or files.
---

# Brand Naming

The naming researchers behind roughly 4,000 brands over 40+ years — Pentium, PowerBook,
BlackBerry, Swiffer, Febreze, Dasani, Sonos, Outback, Impossible, Azure, Vercel, Windsurf, Navan —
work in an unusual way. They treat a name as an engineering problem with a strategy layer, a volume
layer, a linguistics layer, and a screening layer — not as a brainstorm.

This skill reproduces that process, as the researchers have described it in public interviews and
talks. It exists mostly to defeat one failure mode: an LLM asked for names produces twelve
comfortable, descriptive, category-obvious candidates in thirty seconds (`FlashSync`, `LumiWave`,
`CrowdGlow`), and everybody nods. Those names are free to copy, hard to remember, and legally
unavailable. Everything below is machinery for getting past them.

## The idea underneath everything

David Placek, who led most of that work, puts it this way: **"The best names don't describe
reality; they change it."** P&G's device was a "new mop." Research said nobody likes mopping. So
the name didn't describe a mop — `Swiffer` made the act feel quick and playful, and built a $5B
brand while the competitor's honest, descriptive `ReadyMop` stayed small.

Two consequences worth holding onto:

- **A name is not a label, it's the most-repeated asset you own.** Design changes, messaging
  changes, the product changes. The name gets spoken, typed, and searched for decades. That's why
  it earns real work.
- **Comfort is the enemy.** "If your team is comfortable with the name, chances are you don't have
  the name yet." Intel's committee split over `Pentium` — half wanted the safe "ProChip." Andy
  Grove read the split as energy and shipped it. Expect the strongest candidate to be the one that
  makes someone in the room uneasy.

## Pick a mode

| Mode | When | Output |
|---|---|---|
| **Full** | Naming a company, product line, or anything the user will live with for years | Brief → 400+ candidates → screening → 3-5 finalists with rationale |
| **Fast** | Internal tool, feature, side project, "give me options today" | Compressed brief → 100+ candidates → 5-8 finalists |
| **Evaluate** | User already has candidates and wants judgment | Scored critique + repair suggestions, no generation unless asked |

Say which mode you're running and why. If the user hasn't given enough strategy to do Phase 0, ask
for it — but ask 3-4 sharp questions, not a questionnaire, and offer your own best guesses as
defaults so an unanswered question doesn't block the work.

---

## Phase 0 — Strategy: the Diamond

The process starts by refusing to talk about words. Four questions (Placek's "Diamond"):

1. **What does winning look like?** Not "a good name" — what does the company look like in five
   years if this works? Windsurf's answer was "the most beloved tool developers open every morning."
2. **What do we have to win with?** Existing assets: technology, founder story, a category you
   invented, an unfair advantage.
3. **What do we need to win?** The gap. Credibility? Approachability? Permission to charge more?
4. **What do we need to say?** The one idea a person should walk away with — usually not a feature.

Then, before any word exists, write the **sound strategy**. This is the step most people skip and
the reason most names come out mushy. Decide what the name should *sound* like independent of
meaning: fast or full? sharp or soft? light or heavy? reliable or daring? Dasani was designed
before it was found: a crisp `da-`, the Latin health root `san`, a light thin `-i`.

Write Phase 0 output down (a short brief block) before generating. It becomes the scoring rubric
later, and if you skip it, you'll unconsciously score names on "do I like it."

**Also decide the name's job in the architecture**: is this the master brand, a product under an
existing brand, or a feature? A feature under a strong parent can afford to be descriptive;
a master brand almost never can.

---

## Phase 1 — Territories and blind briefs

The researchers deliberately make their own process inefficient. They run **two or three small teams of two
people** in parallel, and only one team knows the truth:

- **Team A** gets the real brief.
- **Team B** is told they're naming the competitor who will beat the client.
- **Team C** is told they're naming something else entirely — a bicycle, when the client is
  actually building an IDE.

Team C is not a joke; it's where `Windsurf` came from. A team riffing freely on *flow* — with no
knowledge that software was involved — produced the name that a room full of people thinking about
code editors would never have reached. The mechanism is cognitive distance: the moment you know the
category, your vocabulary collapses onto that category's clichés.

**Doing this as one agent:** you can't unknow the brief, so approximate it by ordering and sealing
the passes.

1. **Run the displaced pass first.** Choose a domain whose *feeling* matches the sound strategy, not
   the product — Japanese knives, sailing, jazz labels, alpine weather, brewing, astronomy,
   cartography, textile mills. Generate 60-100 names *for that thing*, honestly, without once
   mentioning the real product. Only afterwards ask which of them transplant.
2. **Then the rival pass.** "A competitor is launching next month and will take this market. Name
   them." This reliably produces braver names, because you're not protecting anything.
3. **Then the true-brief pass**, informed by the sound strategy.

If subagents are available, actually spawn them with genuinely different briefs and no shared
context — that's closer to the real thing than sequencing, and worth the tokens on a Full run.

**Exploration territories** — the researchers call this a treasure hunt ("you need to explore in places
where you think there may be no chance of finding the name"). Use at least six, and count them:

Greek/Latin/Sanskrit roots · the periodic table and scientific nomenclature · mythology and
constellations · geography and cartography · other languages (Japanese, Finnish, Turkish, Swahili,
Icelandic) · nautical, aviation and rail vocabulary · crafts and materials · music theory and
instrument names · optics, light and color terms · animal behavior · archaic and obsolete English ·
sensory verbs · onomatopoeia · surnames and mythic figures · nonsense built from the sound strategy.

---

## Phase 2 — Generation at volume

The rule is blunt: **quantity leads to quality.** Placek asks for 1,000-1,500 ideas before expecting
gems; from 3,000 ideas maybe 250 deserve a second look. The reason isn't mysticism — the first
50 ideas are retrieved, not created. They're the category's existing vocabulary rearranged.

Practical targets:

- **Full mode:** at least **400** written candidates before any filtering, from ≥6 territories and
  all three passes.
- **Fast mode:** at least **100**.

**Write them to a file** (`naming/candidates.md` or the scratchpad), grouped by territory, and state
the count. This matters more than it sounds: writing them down is what separates actually exploring
from claiming to have explored, and it lets you re-mine the list later when the finalists get shot
down by trademark — which they will.

**Suspend judgment while generating.** The researchers ban evaluation during creation, and coach leaders
never to say "that won't clear legal" but instead "how could we change it so it clears?" Killing
ideas mid-generation collapses the range. Filter in Phase 4, not here.

**The morpheme matrix.** For invented names, don't free-associate — build combinatorially, the way
Vercel was built: 55 prefixes × 102 suffixes, three rounds over two weeks, each round producing
~60 ideas (which Placek calls "ideas, not solutions"). Assemble parts that each carry a charge:

- prefixes/suffixes signalling speed, precision, flow
- classical roots signalling reliability and authority (`penta-`, `-ium`, `san`, `luc-`, `nova`)
- fast-sounding letters from the sound strategy

Use `scripts/combine.py` in this skill's folder to expand the matrix rather than typing combinations by hand:

```bash
python3 <this skill's folder>/scripts/combine.py --parts prefixes.txt suffixes.txt \
  --min-len 4 --max-len 9 --require v,z --elide --out candidates.txt
```

`--elide` also emits seam-collapsed forms, which is where the good ones usually hide — fed the right
parts, the matrix regenerates `pentium`, `vercel` and `dasani` unprompted. Run `--help` for the rest.

---

## Phase 3 — Sound symbolism

This is the researchers' signature and their moat: ~$2-3M and five years of cross-cultural research into
what letters *feel* like before they mean anything. Will Leben, a Stanford linguistics professor,
built the in-house practice; the team now works with a network of 100+ linguists in 75 countries.

The canonical demonstration is BlackBerry. The prototype's keys looked like seeds, so someone said
"Strawberry." Leben objected: `straw-` is a *slow* syllable, wrong for a device selling
instantaneity. But `-berry` was right — the **b** reads as reliable, the short **e** reads as fast.
Find another b-plus-short-vowel syllable and you're done. Within seconds: BlackBerry.

Load `references/sound-symbolism.md` before doing this work. It carries the phoneme→connotation
tables (front vs. back vowels, stops vs. fricatives, voiced vs. voiceless), the researchers' own
letter-level claims, the structural devices (compounds, palindromes, root grafts, transplanted real
words), and — importantly — how much of this is actually established science versus proprietary
house doctrine. Don't invent phonetic claims from memory; the tables exist so rationales stay honest.

Two constraints to hold while engineering sound:

- **"Surprising, but surprisingly familiar."** The brain is lazy and likes the familiar, so
  breakthrough names use familiar *parts* in an unfamiliar *assembly*. Azure works because "zure"
  rhymes with "sure" — trust — while the z does the arresting. Pure novelty is a tax on the
  listener; pure familiarity is invisible.
- **Compounds punch above their length.** BlackBerry, PowerBook, Impossible Burger are all long,
  and all beat shorter rivals, because two known concepts generate a denser associative network than
  one. Length is a much weaker constraint than people think. Do not filter on "under seven letters."

---

## Phase 4 — Screening

Four gates, in this order, because each is cheaper than the next:

**1. Processing fluency.** Say it out loud. Spell it over a phone. Type it. Read it in a sentence:
"We're building X." If it needs a spelling explanation every time, that's a permanent tax — this is
exactly why Codeium became Windsurf.

**2. Legal reality.** Trademark kills roughly 90% of a shortlist; it's the single largest source of
candidate mortality and the reason you keep the long list. Check the obvious conflicts in USPTO,
EUIPO, and WIPO's Global Brand Database, plus a plain web search for existing use in the same class.
**Be explicit that this is a pre-screen, not clearance** — a real name needs a trademark attorney,
and professional naming teams staff paralegals and attorneys for exactly this. Never tell a user a name is "clear."

**3. Linguistic and cultural screening.** Check every candidate in the languages of every market the
user actually operates in — professional teams screen 10-25 languages per project. Look for obscenity, unwanted
meanings, mispronunciation, and transliteration problems in non-Latin scripts. Details in
`references/screening.md`.

**4. Digital.** Domain, handles, search collision. Placek's position on the .com is direct: *"the
.com has become just an area code"* — buyable for $15-30K, or sidestepped with a prefix or another
TLD. **Do not let domain availability drive the naming decision**; it is the most common way a great
name dies for a bad reason. Report the domain situation, don't rank by it.

**Verify, don't assert.** Every screening claim — a live mark, an operating company on the domain, a
competitor already using the word — is a claim the user will repeat to a board, an investor, or a
lawyer. A plausible-sounding fabricated conflict is the most expensive error this process can
produce: it kills a good name invisibly, and it destroys your credibility the moment someone checks.
So look it up — registry search, WHOIS/RDAP, DNS, the company's actual homepage — and mark each
claim `verified` (you checked a live source this run) or `unverified` (you have reason to believe it
but couldn't confirm). Never launder the second into the first, and never report a conflict you
didn't actually look for. Stated uncertainty is useful to the user; false precision is not.

---

## Phase 5 — Presentation and decision

The researchers never hand over a list — they build a **proof of concept**, showing names in an ad, on a
shelf, on a device, in use, "so decision-makers can experience the names rather than read them."
A name on a spreadsheet row is being judged on comfort. A name in a headline is being judged on work.

Present **3-5 finalists**. For each:

- **The name**, written the way it would actually appear.
- **In context** — a headline, an app icon label, a sentence a customer would say, and the name
  sitting next to two real competitors.
- **Strategy fit** — which part of the Diamond it delivers.
- **Sound rationale** — the specific phonetic construction and what it signals. Concrete, not
  "sounds modern."
- **Structure** — compound, root graft, transplanted word, coined, palindrome.
- **Risks** — legal exposure, language issues, spelling friction, competitor proximity, each marked
  verified or unverified.
- **Provenance** — which pass and territory it came from. If a finalist was built at shortlist stage
  rather than selected from the pool (refining `Tambor` into `Tambora` is legitimate — that's the
  BlackBerry move), say so. Volume work you then bypass is theatre, and the user deserves to know
  whether the name survived the funnel or skipped it.

Then give the user two tools for deciding:

- **The competitor test.** Never ask "do you like this name?" — that measures comfort. Ask: *"Your
  competitor just launched under this name. What's your reaction?"* That measures threat, which is
  what you actually want to know.
- **The polarization read.** Say plainly which finalist is safe and which is polarizing, and name
  the risk of each. Placek's whole record says the polarizing one is usually right, but the user
  is the one who has to live with it — give them the honest read, not a sales pitch.

Close with the runners-up list (10-15) so nothing is lost when legal eliminates a finalist.

---

## Failure modes

These are the ways this goes wrong. Watch for them in your own output.

- **Descriptive names.** `Infoseek`, `TripActions`, `ReadyMop` — instantly understood, permanently
  generic, and a cage when the company expands. TripActions had to become Navan to sell financial
  services. Suggest; don't describe.
- **Stopping at 30 candidates.** The gems are past the point where it stops being fun. If your
  candidate file is short, you skipped the work.
- **Sound symbolism as decoration.** Generating names first and inventing phonetic justifications
  afterwards is astrology. The sound strategy comes *before* generation, in Phase 0.
- **Volume as theatre.** Generating 5,000 candidates and then presenting a finalist that appears
  nowhere in the pool. Refining a candidate is fine and expected — say which one it came from.
- **Fabricated screening.** Reporting a trademark or domain conflict you didn't verify. This one is
  worse than being wrong about a name, because the user repeats it to other people.
- **Optimizing for consensus.** A name everyone likes on first hearing is a name that reminded
  everyone of something they already knew.
- **Domain-first naming.** Ranking candidates by .com availability guarantees you pick from what
  nobody else wanted.
- **Over-claiming the science.** Don't say a letter "means" something. Say what the research
  supports, at the strength it supports it. See the honesty note in `references/sound-symbolism.md`.
- **One territory.** If every candidate came from the same semantic well, you ran one team, not three.

---

## References

- `references/sound-symbolism.md` — phoneme→connotation tables, the researchers' letter claims, structural
  devices, and what the evidence actually supports. Read before Phase 3.
- `references/case-studies.md` — 12 worked examples (Pentium, Swiffer, BlackBerry, Dasani, Azure,
  Vercel, Windsurf, Sonos, Navan, Febreze, Impossible, Outback), each as
  situation → insight → construction → lesson. Read when you need a pattern to reason from.
- `references/screening.md` — trademark, linguistic, and digital screening procedure and limits.
- `assets/brief-template.md` — the Diamond brief plus sound strategy, ready to fill in.
- `scripts/combine.py` — morpheme matrix expander for Phase 2.
