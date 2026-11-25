---
name: cobesy
version: 1.3.1
description: >
  Turn knowledge into adoption plans, briefings, and structured writing with
  COBESY's culture, cognitive, and network lenses. Use for rollouts, buy-in,
  resistance, onboarding, or organizing a blog post, thesis, article, or slides
  before drafting. Produces framing, content structure, and an adoption path.
  Skip factual lookup and single-fact questions.
---

# COBESY: Cognitive Behavioral Systemic

COBESY turns static knowledge into something an organization can use. A document
does not change much by itself. People change when the idea is framed safely,
made easy to understand, and routed through the parts of the network that others
trust.

> Static knowledge -> COBESY compiler -> operational skill
> (Docs, repos, architecture) -> (layered stack engine) -> (adoption, agendas, buy-in)

This skill is for the messy part after the deck exists. It avoids chronological
agendas, all-hands blasts, icebreakers, and pressure campaigns. It uses nine
source works on culture, networks, learning, and influence. See
`references/source-map.md` for the bibliography and substitutions.

The same Cognitive engine has a second output. Instead of a live agenda it can
structure a written or projected piece: a blog post, a thesis, slides, or a
journal article. By default, this path emits a first-pass `composition_blueprint`:
a skeleton grid with headlines, bullets, emphasis, writing advice, style
guidance, audience-leading cues, and keywords to use. Do not write the article,
paper, or slide prose unless the user explicitly asks for prose or a full draft.
See `references/composition.md`. Use it when the knowledge is there but the
structure keeps getting lost as the material grows.

---

## The execution stack

Read it top-down, because that is what the audience experiences. Run it
bottom-up, because culture decides whether anything sticks:

```
┌──────────────────────────────────────────────────────────────┐
│  3. COGNITIVE INTERFACE   Minto · Dirksen · Knowles            │  ← what they see
│     (compress knowledge to fit working memory + adult learners)│
└───────────────────────────────┬──────────────────────────────┘
                                ▼
┌──────────────────────────────────────────────────────────────┐
│            THE COBESY COMPILER  (this agent)                  │
│     translates compressed hierarchies into execution skill     │
└───────────────────────────────┬──────────────────────────────┘
                                ▼
┌──────────────────────────────────────────────────────────────┐
│  2. BEHAVIORAL VECTOR   Centola · Jackson · Berger · cascades  │  ← how it spreads
│     (engineer the transmission path for voluntary adoption)    │
└───────────────────────────────┬──────────────────────────────┘
                                ▼
┌──────────────────────────────────────────────────────────────┐
│  1. SYSTEMIC BASE   Schein · Edmondson · Scientist Mode        │  ← whether it survives
│     (map + neutralize the hidden rules of the organization)    │
└──────────────────────────────────────────────────────────────┘
```

Run order: Systemic → Cognitive → Behavioral → Assemble → Validate.
You diagnose the ground (systemic) before you compress the message (cognitive)
before you route it through people (behavioral). The cognitive layer sits at the
top of the stack the audience experiences, but it is compiled second, because
content that ignores the culture gets rejected regardless of how clear it is.

---

## The three compiler inputs

Map the work to these three inputs. If one is missing, ask for it or say exactly
what you are inferring in Phase 0.

| Input | Question it answers | Feeds layer | Output artifact |
|---|---|---|---|
| `raw_knowledge` | *What* are we transferring? (docs, repo, decision, tool) | Cognitive | `agenda_structure` or `composition_blueprint` |
| `cultural_assumptions` | *Where* are we landing it? (hidden rules, safety level) | Systemic | `framing_protocol` |
| `network_topology` | *Through whom* does it spread? (anchors, clusters) | Behavioral | `target_nodes` |

The Cognitive layer has two back-ends off the same Minto hierarchy. The default
emits `agenda_structure` for a live session. When the deliverable is a piece of
writing, the composition back-end emits `composition_blueprint` instead; the
Behavioral layer is then optional (a thesis has readers, not a rollout).

The `AISkillCompiler` mental model and the legacy-vs-COBESY comparison live in
`references/compiler.md`.

---

## When to use / when not

Use it when the goal is to make an organization do something with knowledge:
roll out a tool/process, get buy-in, design an agenda or briefing, overcome
resistance, make something stick, onboard a team, plan a change.

Do not load it for factual lookup, a single-fact answer, or a task with no human
adoption problem. If nobody needs to change behavior, COBESY is overhead.

---

## The COMPILE workflow

### Phase 0: Intake
Gather the three inputs. Then state these in one line each:
- Target behavior: the specific action you want a named group to take. Not "awareness". An action.
- Hidden assumption: one suspected rule that governs this group (Schein).
- High-leverage anchor: one person or group whose adoption would pull others (Jackson).

If you cannot name the target behavior as an observable action, stop and fix
that first. Use `assets/diagnostic-intake.md`.

### Phase 1: Systemic filter (the ground)
Run the audience through `references/01-systemic-layer.md`.
- Map artifacts -> espoused values -> basic underlying assumption (Schein).
- Locate the org on the Edmondson safety × accountability 2×2.
- Produce `framing_protocol`: how to frame this work as a learning problem,
  what not to say, and an explicit disproof condition ("we are wrong if ___").
- Gate: if the org sits in the Anxiety quadrant (low safety / high
  accountability), raise safety *before* pushing content. Do not skip.

### Phase 2: Cognitive compression (the message)
Run `raw_knowledge` through `references/03-cognitive-layer.md`.
- Build a Minto pyramid: lead with the conclusion, group support MECE, open
  with SCQA.
- Cut to working-memory limits and speak to motivation as well as analysis (Dirksen's Elephant and Rider).
- If the audience is senior/expert, apply Knowles andragogy (respect experience,
  problem-centered, self-direction).
- Produce `agenda_structure`: a top-down hierarchy, not a chronological list.

If the deliverable is a written or projected piece, run the same hierarchy
through the composition back-end in `references/composition.md` instead. It sorts
the work by four grains (macro governing idea, opening, paragraph move, sentence),
adapts to the format (blog, thesis, slides, journal article), and emits a
first-pass `composition_blueprint` via `assets/composition-blueprint.md`. Default
to a skeleton grid: headlines, bullet points, emphasis guidance, writing advice,
style guidance, audience-leading cues, and keywords to use. Avoid marketing
language. Do not draft the article, paper, or slide prose unless the user
explicitly asks for a draft, prose, final copy, or full article.

### Phase 3: Behavioral sequencing (the path)
Run the rollout through `references/02-behavioral-layer.md`.
- Classify the change: simple contagion (info) or complex contagion (costly
  behavior change). Most adoptions are complex, so they need wide bridges, not broadcasts.
- Pick targets by centrality (Jackson): eigenvector anchors for cascades.
- Design clustered seeding (Centola): adjacent trusted team adopts first.
- Remove barriers with REDUCE (Berger) instead of pushing harder.
- Sequence respected, objective voices first to start a positive cascade.
- Produce `target_nodes`: who adopts in what order, through which clusters.

### Phase 4: Assemble & facilitate
Emit the three artifacts (`framing_protocol`, `agenda_structure`, `target_nodes`)
into the relevant templates in `assets/`. If a live session is needed, pick
exercises from `references/facilitation-games.md` (Gamestorming), respecting the
open→explore→close shape. Hand the user the matching prompts from
`assets/prompt-library.md`.

### Phase 5: Validate (anti-cringe gate)
Before delivery, run every artifact through the validation gate in
`references/compiler.md`:

| Check | Layer | Fail action |
|---|---|---|
| MECE? | Cognitive | Regroup the pyramid |
| Within working memory? | Cognitive | Chunk / add job aid |
| Delivered at the point of action? | Cognitive | Embed it / make an in-workflow job aid |
| Safe enough to say? | Systemic | Reframe / raise safety first |
| Disproof condition stated? | Systemic | Add falsifiability or reject item |
| Cascade, not broadcast? | Behavioral | Re-sequence through clusters |
| Removes barriers vs pushes? | Behavioral | Switch to REDUCE |

If any check fails, return to that layer. Do not ship around a failed gate.

For a `composition_blueprint`, also run the writing linter in
`references/composition.md` (first-paragraph drop-off, info overload, mismatched
TOC, scope creep, flat exposition, expert fog, sentence sprawl, reader mismatch,
AI slop / generic voice). Same rule: a failed check sends you back to the grain
that owns it.

If the user explicitly asked for prose, run the humanizer pass before delivery.
Drafted prose must pass these output conditions:
- no significance inflation, vague authority, forced trios, generic upbeat endings, or chatbot phrasing;
- no AI-looking output symbols: em dashes, curly quotes, emoji decoration, emoticons, decorative bold, or chatbot-style visual formatting unless the user explicitly asks for them;
- sentence rhythm varies without turning cute or over-written;
- the author's voice, reader level, and tolerance for detail are preserved;
- the agent can answer "what still makes this sound AI-generated?" and repair the answer.

---

## Decision points

- Simple vs complex contagion: broadcast is fine only for simple info;
  anything costly/risky/identity-relevant needs clustered wide bridges.
- Low psychological safety: systemic layer first; content is wasted in the
  Anxiety quadrant.
- High resistance / reactance: switch from persuasion to Berger's REDUCE
  (remove the barrier; pushing harder backfires).
- Senior or expert audience: lead with Knowles (their experience is the
  curriculum; never treat them as empty vessels).

---

## Cross-skill handoffs

COBESY handles adoption. It takes a knowledge asset or decision and turns it
into a path for action. It does not render draw.io diagrams, so it sends analysis
to the visualization skills and pulls verified inputs from the analysis skills.
Keep actor, cluster, and assumption names stable across skills so the artifacts
line up. Map each handoff to a COMPILE phase:

| Sibling skill | Direction | Phase | What flows |
|---|---|---|---|
| `reflect` | in | Phase 0 | Turn a vague "drive adoption of X" request into a clear prompt with the three compiler inputs before COMPILE starts. |
| `strategic-foresight-viz` | in | Phase 0–2 | Import PESTLE drivers / scenarios as the Complication in the SCQA opener: the external reason the change is needed now. |
| `intana-viz` | both | Phase 1–3 | Render the diagnostics: Schein Cultural Web, Edmondson 2×2, stakeholder / network maps, the Minto agenda pyramid, the adoption map. Route a contested `framing_protocol` assumption through Key Assumptions Check, Red Teaming, or Pre-Mortem and bring the verified version back. |
| `premortem` | both | Phase 3–5 | Stress-test the assembled `target_nodes` rollout: assume the adoption failed, reason backward, then feed the failure modes back into REDUCE barriers and the framing protocol. The Phase 5 anti-cringe gate is a lighter inline version of this. |
| `game-theory-negotiation` | both | Phase 3 | When buy-in needs a bargain (resourcing, mandate, an anchor's commitment), hand the named eigenvector anchor and the incentive question to the negotiation skill; bring back a concession plan and incentive-compatible profit-share / bonus sizing for the adoption design. |
| `humanizer` | out | Phase 4 / Phase 5 | Clean the emitted brief, agenda, or composition output so the deliverable reads human, not AI-generated. This is the writing-level companion to COBESY's structural anti-cringe gate. |

Rule of thumb: analysis skills verify the inputs, viz skills draw the artifacts,
COBESY sequences the adoption. A premortem surfaces a barrier →
COBESY routes around it; a negotiation secures an anchor → COBESY seeds from it;
intana-viz renders the cultural map → COBESY frames against it.

Use the shared context packet defined in `references/shared-context-packet.md`.
It keeps stable IDs (`A1 buyer`, `S2 recession case`, …) across artifacts and
works without installing a sibling skill. COBESY reads and writes the same
fields rather than inventing parallel names:

| Packet field | COBESY role |
|---|---|
| `Assumptions` | COBESY is a primary producer. Schein basic underlying assumptions become packet assumptions; route contested ones through `intana-viz` to verify. |
| `Actors` | COBESY annotates actors with network role: eigenvector anchor, bridge, seed cluster. Keep actor IDs identical to the negotiation/investigation diagrams. |
| `Scenarios` | Consumed from `strategic-foresight-viz` as the SCQA Complication. |
| `Constraints` | The framing protocol's "safe to say" limits and disproof conditions are cultural constraints. |
| `Open questions` | Each disproof condition ("we are wrong if ___") is an open question other skills can pick up. |

---

## Files

References, load as needed:
- `references/compiler.md`: the compiler contract, I/O, legacy-vs-COBESY, validation gate.
- `references/01-systemic-layer.md`: Schein, Edmondson, Scientist Mode -> `framing_protocol`.
- `references/02-behavioral-layer.md`: Centola, Jackson, Berger, cascades -> `target_nodes`.
- `references/03-cognitive-layer.md`: Minto, Dirksen, Knowles -> `agenda_structure`.
- `references/composition.md`: the writing back-end (Belcher, Cron, Kolin, Graff & Birkenstein, Klinkenborg, Williams & Bizup) -> `composition_blueprint`.
- `references/facilitation-games.md`: Gamestorming exercises per phase.
- `references/source-map.md`: bibliography, layer mapping, substitutions.

Templates, fill and deliver:
- `assets/diagnostic-intake.md`: Phase 0 intake.
- `assets/change-brief.md`: the assembled three-artifact deliverable.
- `assets/agenda-pyramid.md`: Minto agenda skeleton.
- `assets/adoption-map.md`: Centola/Jackson rollout plan.
- `assets/composition-blueprint.md`: first-pass messaging skeleton for written or projected pieces (blog, thesis, slides, journal article).
- `assets/prompt-library.md`: ready prompts to drive the agent per layer.
