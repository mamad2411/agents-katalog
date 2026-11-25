---
name: skill-authoring
description: Writes or extends a Keystone skill, including product-specific domain packs. Triggers - add a new skill to this pack, this skill never triggers when I ask for it, write a domain pack for our product, skill too long, agent does not follow the skill, retire or merge skills, extend keystone.
---

# Skill Authoring

A skill is a procedure an agent reliably follows. Two things decide whether it
works: whether it **triggers** at the right moment, and whether its body is
**actionable** once loaded. Everything else is decoration.

## Before writing: earn the slot

Answer honestly. Any "no" means don't create the skill.

- Does this cover work that no existing skill covers? (Overlap makes routing
  worse — two skills that half-answer the same question compete.)
- Would a competent engineer do this differently without the skill? If the
  agent already behaves correctly, a skill adds tokens and no behavior.
- Can the procedure be written as concrete steps with a verifiable end state?
  Advice that cannot be checked is not a skill.
- Has the gap been felt at least twice in real work?

**Search before you write.** List the skills already installed — this pack,
other plugins, the project's own — and read the descriptions of the nearest
neighbors. When one half-covers the work, extend it. A second skill that
half-answers the same prompt makes routing worse for both.

## Anatomy

```text
skills/<kebab-name>/
  SKILL.md              required — frontmatter + body
  references/*.md       optional — loaded only when the body points to them
  templates/*           optional — artifacts the skill produces
```

### Frontmatter

```yaml
---
name: <kebab-name>                 # must equal the directory name
description: <one English sentence: what it does and when to use it>. Triggers - <phrases users actually type>.
---
```

The description is the **entire** basis for routing. The body is invisible
until the skill is selected. Consequences:

- Write the description last, after the body tells you what the skill really is.
- Include the words a person types under pressure ("it's slow", "this broke",
  "should I use a queue"), not the words an architect writes in a document.
- Include non-English trigger phrases when the team works in another language;
  routing is lexical enough that this matters.
- State the boundary when two skills are adjacent: "for X use `other-skill`".
- Keep it under 500 characters. A description that needs more is two skills.

### Body

| Section | Purpose |
|---|---|
| One-paragraph opening | The concrete failure this prevents. Not a definition. |
| When to use / when not | The "not" list prevents over-triggering |
| The procedure | Numbered, with observable outcomes |
| Decision tables | Where judgment is needed, give the axes and the defaults |
| Failure modes / anti-patterns | Name each one and its cost |
| Exit checklist | Verifiable statements, not aspirations |

Target 400–1400 words. Beyond that, split content into `references/` — the body
is loaded every time the skill fires; references are loaded when needed.

### Portable across agents

Keystone skills use the Agent Skills format. `name` (lowercase letters, digits
and single hyphens, at most 64 characters, equal to the directory name) and
`description` are the only fields every agent reads. Optional fields —
`license`, `compatibility`, `metadata`, `allowed-tools` — are honored by some
agents and ignored by others, so no rule the skill depends on may live there.
Keep reference chains one level deep: the body points to a reference; the
reference does not send the reader on to a third file for the rule.

## Writing rules

1. **Stack-agnostic by default.** Say "the project's focused-test command", not
   `pytest -k`. Where a concrete example clarifies, give two in different
   languages, or pseudocode.
2. **Imperative, second person.** "Write the failing test first." Not "It is
   recommended that tests be written first."
3. **Numbers over adjectives.** "≤ 400 ms p95" beats "fast".
4. **Name the cost.** "Skipping this produces X" is what makes an agent comply.
5. **No overlap with `CLAUDE.md`.** Invariants live there; don't restate them.
6. **Never contradict another skill.** Cross-reference instead: linking is free,
   duplication drifts.

## Fixing a skill that does not trigger

The body is almost never the problem.

1. Reproduce: fresh session, type the user's actual phrasing, see what fires.
2. Compare the phrasing to the description's vocabulary. Missing words?
3. Add the real trigger phrases. Do not lengthen the body.
4. Add the failing prompt to `evals/cases/<name>.json` as a positive case.
5. Run `python3 scripts/check_triggers.py`.

If a *different* skill fires instead, the two descriptions overlap — sharpen
both, and state the boundary in each.

## Measure that it is followed

`make triggers` proves a prompt shares vocabulary with the right description;
it cannot prove an agent applies the skill. `make evals-live` (optional, calls
a model) runs each eval prompt with and without naming the skill and grades
the answer against the exit checklist:

| Result | Meaning | Fix |
|---|---|---|
| Explicit high, implicit low | Selected only when named | The description |
| Explicit low | Selected but not followed | The body: steps too vague, or a checklist item missing |
| Both high | Working | Nothing — record the run |

Run it on every changed skill before a release, and record the model, the
number of runs and the scores. When it cannot be run, say so in the release
notes.

## Retire and merge

Every description is loaded into every session, so the catalog has a budget
(`CONSTRAINTS.md`). Review it each release: a skill whose prompts keep routing
elsewhere, that never applies in live evals, or that overlaps a neighbor gets
merged into the neighbor or removed — and the removal is recorded
(`documentation-and-knowledge`). Fewer, sharper skills route better than many
adjacent ones.

## Domain packs

Keystone is domain-neutral. Product-specific procedure belongs in a pack layered
on top — see `examples/domain-pack/`.

- Same structure: `skills/<name>/SKILL.md` with the same rules.
- Name domain skills after the domain noun (`invoice-reconciliation`), not the
  generic verb, so they don't compete with core skills for routing.
- A domain skill may cite core skills, never contradict them. If it must
  contradict one, that is a project-level `CLAUDE.md` decision instead.
- Keep the pack in the product's repository, so it versions with the code that
  it describes.

## Exit checklist

- [ ] `name` equals the directory name
- [ ] Description: one sentence + real trigger phrases, under 500 characters
- [ ] Body 400–1400 words; longer material moved to `references/`
- [ ] Contains a "when not to use" statement
- [ ] Ends with a verifiable exit checklist
- [ ] Eval case added with ≥3 positive and ≥2 negative prompts
- [ ] `make validate` and `scripts/check_triggers.py` pass
- [ ] No overlap introduced with an existing skill's description; installed
      skills searched before writing
- [ ] Behavior depends only on `name`, `description` and the body
- [ ] `make evals-live` run on the changed skill with the result recorded, or
      the missing run reported
