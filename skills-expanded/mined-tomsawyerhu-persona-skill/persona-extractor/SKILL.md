---
name: persona-extractor
description: Build a reusable, evidence-grounded persona artifact from raw source material such as interviews, memoirs, speeches, letters, biographies, transcripts, diaries, articles, or mixed dossiers. Use this skill when the goal is to produce an engineering-grade persona package for downstream simulation, roleplay, analysis, or evaluation rather than an informal character sketch.
---

# Persona Extractor

This skill is for turning a corpus about one person into a standardized persona artifact.

The output is not just a summary. It is a structured package with:

- source inventory
- extraction config
- normalized evidence index
- persona synthesis
- scenario library
- simulation contract
- runtime modules
- load profiles

The canonical final artifact is:

- `personas/<persona_slug>/persona.json`

The extraction pipeline is config-driven. Do not hardcode dimensions, domain assumptions, or source-specific heuristics into the final persona.

Read these references first:

- `references/pipeline.md`
- `references/dimension_catalog.md`
- `references/output_contract.md`
- `references/quality_rubric.md`

## Standard Workflow

1. Scaffold the project.
   Generate a generic working folder and config:

```bash
python skills/persona-extractor/scripts/scaffold_persona_project.py \
  --output-dir personas/<persona_slug> \
  --persona-id <persona_slug> \
  --display-name "<display_name>"
```

This creates:

- `extractor_config.json`
- `persona.template.json`
- `notes.md`

2. Define the extraction boundary.
   Fill `extractor_config.json`:
   - corpus root
   - source types
   - time span
   - chosen dimensions
   - scenario axes
   - optional seed terms per dimension

3. Build the evidence pack.
   Run:

```bash
python skills/persona-extractor/scripts/persona_evidence_builder.py \
  --source-dir <corpus_dir> \
  --output-dir personas/<persona_slug> \
  --config personas/<persona_slug>/extractor_config.json
```

This generates:

- `source_index.json`
- `block_index.json`
- `candidate_passages.json`
- `candidate_evidence.md`

4. Synthesize the persona.
   Write `persona.json` by combining:
   - source facts
   - normalized evidence ids
   - dimension summaries
   - scenario answers
   - roleplay contract

5. Validate before use.
   Template-stage validation:

```bash
python skills/persona-extractor/scripts/validate_persona.py \
  personas/<persona_slug>/persona.template.json \
  --mode template
```

   Final artifact validation:

```bash
python skills/persona-extractor/scripts/validate_persona.py \
  personas/<persona_slug>/persona.json \
  --mode final
```

6. Render human-readable mirrors.

```bash
python skills/persona-extractor/scripts/render_persona_markdown.py \
  personas/<persona_slug>/persona.json
```

7. Build runtime modules for partial loading.

```bash
python skills/persona-extractor/scripts/build_persona_modules.py \
  personas/<persona_slug>/persona.json
```

This writes:

- `personas/<persona_slug>/modules/*.json`

and updates:

- `module_registry`
- `load_profiles`

## Design Rules

- Make the schema fit the corpus, not the other way around.
- Prefer reusable behavioral dimensions over biographical trivia.
- Separate evidence, inference, and extrapolation.
- Preserve drift over time when the persona changes.
- Record uncertainty explicitly instead of forcing false precision.
- Keep the artifact generic enough for any downstream simulator, not just one roleplay style.
- Keep the runtime layer modular enough that later invocation can load only the slices needed for a scene.

## Quality Bar

- The artifact must be understandable without reopening the raw corpus.
- Every major synthesis claim should trace back to evidence ids.
- Dimensions should capture stable behavior patterns, not just famous slogans.
- Scenario answers should reflect the extracted method, values, and voice, not cosplay.
- The artifact should remain useful even if the person is not political, historical, or public-facing.

## Output Rule

`persona.json` is the source of truth.

Markdown files are mirrors for review.

The roleplay skill should consume the final artifact generically via the simulation contract and scenario library, not via person-specific patches.
