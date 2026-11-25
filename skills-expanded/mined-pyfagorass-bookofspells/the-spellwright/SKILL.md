---
name: the-spellwright
description: >-
  Forge a new skill ("spell") from scratch — author a well-formed SKILL.md with
  discoverable frontmatter, lean progressive-disclosure structure, and optional
  references/scripts. Use whenever the user wants to create, write, author, draft,
  or scaffold a new skill or SKILL.md; package a repeatable workflow as a reusable
  skill; improve a skill's description so an agent reliably triggers it; or learn
  how skills are structured. The companion to the-grimoire: that one finds
  existing spells, this one makes new ones.
---

# 🪶 The Spellwright — How to Forge a Spell

A *spell* (skill) is a folder holding a `SKILL.md` — a short, plain-language
instruction another agent will read and obey when the moment calls for it. A good
spell turns a workflow you'd otherwise re-explain every time into something a
conduit can summon on its own. This is how a wizard teaches their demon a new
trick once, and never again.

You are the spellwright. Forge spells that are **easy to discover**, **lean to
load**, and **honest to obey.**

## The anatomy of a spell

```
my-spell/
├── SKILL.md          # required — frontmatter + instructions
├── references/       # optional — deep docs, read on demand
├── scripts/          # optional — deterministic helpers the spell can run
└── assets/           # optional — templates, images, fixtures
```

`SKILL.md` begins with YAML frontmatter, then the body:

```markdown
---
name: my-spell
description: Use when ... — what it does and exactly when to reach for it.
---

# My Spell

## When to use
...
## Steps
...
```

## The one rule that matters most: the description is the summoning-sign

A conduit does **not** load every spell's body — only its `name` and
`description` sit in view, and the `description` is the *entire* basis on which
the agent decides whether to summon the spell. A vague description is an
unsummonable spell. So:

- **Lead with the trigger.** Write *"Use when the user…"* — name the situations,
  verbs, file types, and tools that should invoke it. Be concrete.
- **Say what it does and what it does not.** Bound it. *"Use for X and Y; do not
  use for Z."*
- **Spend your words here.** The description earns more than any other line in the
  spell. Most spells that never fire died at their description.

## Forge lean — let depth wait

Mirror the Book's own way (see `the-grimoire`): keep `SKILL.md` short and put the
heavy detail where it loads only when needed.

- **`SKILL.md` is the map, not the territory.** A page or two: when to use, the
  steps, the wards. If it grows long, move detail into `references/` and tell the
  agent to read the relevant file at the relevant step.
- **`references/` is read on demand.** Long API docs, edge cases, lookup tables —
  one file each, named for its contents, so the agent greps and reads only what
  the task needs.
- **`scripts/` are deterministic hands.** When a step is mechanical and exact,
  ship a script and have the spell call it, rather than asking the agent to
  improvise the same code each time.

## The Rite of Forging

1. **Name it.** Lowercase-kebab, unique, descriptive: `migrate-to-vitest`, not
   `helper`. The folder name is the spell's true name.
2. **Write the description first.** Trigger-led, specific, bounded (see above).
   If you can't say *when* to use it in one sentence, the spell isn't scoped yet.
3. **Draft `SKILL.md` lean.** When-to-use, the steps, the wards. Plain imperative
   prose — you are writing instructions for an agent, not prose for a human.
4. **Push depth to `references/`.** Anything long or occasional moves out of the
   body; the body points to it at the right step.
5. **Add `scripts/` for the mechanical parts.** Exact, repeatable work belongs in
   code the spell invokes.
6. **Test by summoning.** Invoke it on a real task. Did the conduit reach for it
   unprompted (description working)? Did it have what it needed (body complete)?
   Tighten and repeat.

## Wards

- **A spell is obeyed, not merely read.** Write only instructions you'd want acted
  on. Never embed secrets, tokens, or destructive commands; never write something
  that, read aloud to a demon, would do harm.
- **Honest framing.** Say plainly what the spell does. A spell that hides its
  effect is dark magic — and this Book scries for exactly that (`scry()` in
  `transcribe-spells.py`).

## Deeper magics

- **The canonical rule of the form.** The SKILL.md form is an *open standard*,
  first cut by the House of Anthropic and now honoured across many houses. When in
  doubt about the letter of the rite, consult the
  [Agent Skills Specification](https://agentskills.io/specification) — the shared
  law a spell must keep to be read by any conduit.
- **Your conduit's own forge.** For packaging and installation specific to your
  conduit, summon your house's creator through `the-grimoire` — e.g.
  `openai-skill-creator`, `openai-plugin-creator`, `commandcode-skill-creator`,
  or `google-agent-platform-skill-registry`. This spell teaches the craft; those
  teach each house's particular rites.
- **Spells that write themselves.** The frontier is *automated* skill discovery —
  agents that find, draft, and refine their own spells from experience. See
  **EvoSkill** (https://github.com/sentient-agi/EvoSkill), a research framework on
  exactly this. One day the spellwright's hand may be the demon's own.
- **Adding a spell to *this* Book.** The Book of Spells gathers spells from
  accountable houses rather than hand-authoring them — see
  [`CONTRIBUTING.md`](../CONTRIBUTING.md). To keep a personal spell, install it
  into your own conduit's skills directory instead.

*Forge well. A spell outlives the forging.* 🕯️
