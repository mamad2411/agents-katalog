---
name: friskeval
description: >-
  Frisk your skill catalog for routing collisions and scope overclaim before you ship a new skill.
  Triggers automatically when you are about to report a coding task done and your diff added or changed
  a SKILL.md (or on /friskeval). Two skills whose descriptions overlap fight for the same prompt, and a
  security skill that claims another's domain silently misroutes — so the agent picks the wrong skill and
  the user never knows. friskeval builds a TF-IDF model of every skill description, flags near-duplicate
  pairs and skills that carry another's discriminative vocabulary, checks that each trigger prompt still
  routes to its owner, and refuses to say "done" while a new skill collides with one already in the catalog.
---

# friskeval — routing linter for a skill catalog

When you add a skill to a catalog, its `description` is the only thing the agent
reads to decide *when* to fire it. Add a second skill whose description overlaps,
and the two silently compete for the same prompts — the router picks one, the user
never sees the other, and no test catches it because nothing crashed. This is worst
in a **security** catalog, where descriptions are structurally alike ("frisk your X
for Y before you ship") and a skill that drifts into a neighbour's domain misroutes
real audits. friskeval is the check the agent runs on the catalog itself.

## When to run

- **Automatically**, when you are about to report a task done and your diff added or
  changed a `SKILL.md` (a new skill, or an edited `description`).
- **On demand** when the user types `/friskeval`.

## What it looks at

Only the skill **descriptions** in the catalog — the frontmatter `name` +
`description` of every `SKILL.md`, plus an optional `cases.json` of trigger prompts.
It does not read or grade skill bodies; routing is decided by descriptions, so that
is all it needs. Deterministic, offline, no tokens.

## The process

1. **Build the corpus** — tokenize every description (light stem, drop stopwords),
   weight the skill `name` 2x, compute TF-IDF across the catalog.
2. **Collision** — cosine-similarity every pair of descriptions. `≥0.75` is an error
   (two skills are near-duplicates), `≥0.5` a warning (drifting toward overlap).
3. **Scope overclaim** *(security catalogs)* — derive each skill's discriminative
   terms (rare across the catalog) and flag any other skill whose description carries
   ≥50% of them: skill A is promising to cover skill B's territory.
4. **Trigger routing** — for each positive prompt in `cases.json`, the owning skill
   must rank in the top-k (default 3); each negative prompt must NOT rank #1 with a
   real score. A #1 at score ~0 is an off-topic prompt nobody owns — not a failure.

## What to do with findings / output

- **Do the safe, mechanical thing yourself** — when a collision or overclaim is a
  wording problem, rewrite the newer skill's description to name its own domain and
  drop the borrowed vocabulary, then re-run.
- **Escalate** a genuine scope conflict — two skills that really do the same job.
  Describe the overlap, offer to merge them or narrow one, ask which.
- **Never invent** a problem. A catalog that passes all four checks is clean — say so
  and stop.

## The hard rule

Do not say "done" after adding or editing a skill while its description collides with
(cosine ≥0.75) or overclaims (≥50% of the domain terms of) a skill already in the
catalog.

## Output format

```
friskeval — <N> skills · <clean | M issue(s)>
  <symbol> <label>  <skillA> ~ <skillB>  <metric> → <fix>
  ✓ <what was clean>
<closing line: what the user must decide before this is finished>
```

Be terse. Real signal only.
