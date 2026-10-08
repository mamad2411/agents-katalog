---
description: Bootstrap a new context-skill repo by running deep research and materializing it (scaffold → deep-research → raw_outputs → enrich → synthesize → manifest → validate).
argument-hint: <skill-name> [target-dir] [themes...]
---

You are bootstrapping a new **context skill**: $ARGUMENTS

Invoke the `bootstrap-context-skill` skill and follow its pipeline end to end. Before
researching, confirm (ask only for whatever wasn't supplied above):

1. **Domain / topic** — what the skill is a reference on.
2. **Themes** — the sections to cover (each becomes one deep-research run + one guide section).
3. **Target directory** — where to create the repo (default: a new sibling dir named after the skill).

Then:
- Copy `${CLAUDE_PLUGIN_ROOT}/assets/template/` into the target and replace placeholders.
- For each theme, run the **`deep-research`** skill (it does the searching, fetching, and
  3-vote adversarial verification) and save its report JSON. Do **not** add a second verifier.
- Materialize each report with
  `node ${CLAUDE_PLUGIN_ROOT}/assets/research-to-raw-outputs.mjs <report.json> <target> --theme "<Theme>"`,
  then WebFetch the source URLs to enrich the source files.
- Synthesize the anchored, inline-cited guide and the routing `SKILL.md`.
- Emit `index.json` (paste the mapper's `sources[]`, add `sections[]`), then run
  `node scripts/validate-index.mjs --fix && node scripts/validate-index.mjs` and do not
  finish until it exits 0.

Surface any gap (e.g. a theme deep-research came back inconclusive on) instead of papering
over it.
