---
name: bootstrap-context-skill
description: >-
  Bootstrapping a new "context skill" — running deep research on a topic and turning the
  verified findings into a cited, LLM-navigable reference repo that ships as a Claude Code
  plugin. Use when the user says they want to "build a context skill", "research X and
  package it as a skill", "turn this research into a skill/guide", or points at deep-research
  outputs and asks for the agent-harness-best-practices format (manifest + anchored guide +
  samples + provenance chain + validator).
---

# Bootstrap a context skill from deep research

A **context skill** is a knowledge repository structured so an LLM agent navigates it
cheaply, answers from it confidently, and can trust what it finds — packaged as a Claude
Code plugin whose skill routes Claude to the **one** relevant, cited section on demand
(never dumping the whole guide into context). The reference implementation is
`agent-harness-best-practices`. This skill replicates that pattern for any domain.

**The goal to design for** (the whole pattern serves this one sentence): drive the common
question to **one manifest lookup + one bounded, self-contained, already-cited read.**

## The engine: deep-research does the gathering and verification

Don't hand-roll search or claim verification — the **`deep-research` skill** already
fans out web searches, fetches sources, and runs **3-vote adversarial verification** per
claim (a claim survives only if fewer than 2 of 3 skeptics refute it). This skill's job is
to **run deep-research and materialize its verified output** into the context-skill format.
Treat deep-research's surviving findings as the verified evidence; do **not** re-verify them.

## The build pipeline — follow in order

Full step-by-step in `${CLAUDE_PLUGIN_ROOT}/assets/pipeline.md`. The arc:

```
deep-research  →  scaffold  →  materialize evidence  →  enrich sources  →  synthesize  →  manifest + validate
(per theme)       template      report → raw_outputs/    WebFetch text     guide + samples   index.json, green
```

1. **Scaffold.** Copy `${CLAUDE_PLUGIN_ROOT}/assets/template/` into the target repo and
   replace the placeholder tokens (`__SKILL_NAME__`, `__DOMAIN__`, …; list in the pipeline
   doc). The template is born-green (passes the validator out of the box).

2. **Run deep-research.** Decide the **themes** the skill should cover (each becomes a guide
   section). For each theme, invoke the `deep-research` skill with a focused question as its
   args; if the topic is underspecified, ask 2–3 scoping questions first. Save each returned
   report object to a JSON file (e.g. `report-<theme>.json`).

3. **Materialize the evidence (`raw_outputs/`).** For each saved report, run the mapper:

   ```bash
   node "${CLAUDE_PLUGIN_ROOT}/assets/research-to-raw-outputs.mjs" <report.json> <target-repo> --theme "<Theme>"
   ```

   It writes `raw_outputs/{sources/sources.json, sources/INDEX.md, sources/source-NN.md
   stubs, claims/verified-claims.json (survivors ← findings, dropped ← refuted),
   synthesis/findings-digest.md}` and prints a ready-to-paste `sources[]` array for
   `index.json`. It is additive and de-dupes sources by URL, so run it once per theme.

4. **Enrich the sources.** The mapper writes header-only source stubs. WebFetch each source
   URL and paste the extracted primary text into its `raw_outputs/sources/source-NN.md` so
   the provenance chain is complete (a claim → its source → the supporting text).

5. **Synthesize the guide (`docs/`).** Write one themed section per research theme from the
   findings digest. Each section: `principle → concrete practices → inline citation key per
   claim ([key], defined in the bibliography) → "→ Code:" pointer`. Give every section a
   stable opaque anchor `<a id="sN"></a>` (anchors are the durable contract; line numbers are
   derived). End with a decision cheat-sheet + anti-patterns.

6. **Code samples (optional, preferred).** One runnable, dense-header, version-pinned sample
   per theme under `code_samples/`. State the exact verification level.

7. **Author the routing skill.** Edit `skills/<name>/SKILL.md` in the target so it triggers
   on the domain and routes: read `index.json` → read just the matched section's line range →
   open its sample/source → claims ledger only if provenance is in question.

8. **Emit + validate the manifest.** Write `index.json` (paste in the mapper's `sources[]`,
   add `sections[]` with the anchors and the keys each cites), then
   `node scripts/validate-index.mjs --fix && node scripts/validate-index.mjs`. It must exit 0
   before the repo is done.

## The seven structural patterns (the bar each step is held to)

Full rationale + how-to in `${CLAUDE_PLUGIN_ROOT}/assets/playbook.md`. In brief:
1. A machine-readable **manifest that pre-joins** sections ↔ samples ↔ sources (`index.json`).
2. **Stable opaque anchors** decoupled from line numbers and titles.
3. **Self-contained, individually-cited units** that close the loop (no chasing 3 more files).
4. **Layer by load cost** — `llms.txt` → guide → samples → raw sources → claims ledger; label heavy artifacts.
5. A **provenance chain** with documented join keys (claim → source → URL, verbatim quote stored).
6. **CI-enforced consistency** — the validator asserts every invariant; `--fix` regenerates derived data.
7. **Redundant entry points, single source of truth** — `llms.txt`/README/indexes are projections of the manifest.

Verify your output against `${CLAUDE_PLUGIN_ROOT}/assets/checklist.md` before finishing.

## Note on verification

deep-research is the single source of verification — its survivors are already adversarially
checked, and the ledger records that. If you add or substantially reword a claim **by hand**
(outside deep-research), source it to a primary URL and quote the supporting text yourself;
don't ship an unsourced claim. There is deliberately no second, duplicate verifier here.

## Kickoff

The `/new-context-skill <name>` command (in `commands/`) sets up a run. If invoked without
it, ask for: the **domain/topic**, the **themes** to cover, and the **target directory**.
Then start at step 1.
