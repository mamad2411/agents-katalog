---
name: persona
description: Unified persona skill for distilling, listing, fusing, switching, and exiting personas. Use this skill for all persona workflows through `/persona ...`.
argument-hint: "<subcommand-or-persona-name> ..."
version: "2.0.0"
user-invocable: true
---

# Persona

This is the single public entrypoint for all persona workflows.

Use `/persona ...` for:

- help
- language
- distill
- delete
- list
- fuse
- switch
- exit

Primary runtime data:

- `store/personas/catalog.json`

Primary scripts:

- `scripts/cli/persona_cli.py`
- `scripts/extraction/scaffold_persona_project.py`
- `scripts/extraction/validate_persona.py`
- `scripts/extraction/build_persona_modules.py`
- `scripts/runtime/build_persona_catalog.py`
- `scripts/runtime/select_persona_modules.py`

Read these references when needed:

- `references/extraction/output_contract.md`
- `references/runtime/roleplay_contract.md`
- `references/extraction/dimension_catalog.md`
- `references/extraction/agentic_distill_workflow.md`
- `references/extraction/distill_execution_prompt.md`
- `references/extraction/pipeline.md`
- `references/extraction/quality_rubric.md`

## Commands

### 1. Help

Show all available persona commands:

```text
/persona help
```

Use:

```bash
python skills/persona/scripts/cli/persona_cli.py help
```

### 2. Language

Show or set the active response language:

```text
/persona language
/persona language 中文
/persona language English
/persona language default
```

Use:

```bash
python skills/persona/scripts/cli/persona_cli.py language
python skills/persona/scripts/cli/persona_cli.py language English
python skills/persona/scripts/cli/persona_cli.py language default
```

If no override is active, roleplay uses the persona default language.

### 3. Distill

Create or refresh a persona workspace from a supplied corpus directory:

```text
/persona distill <persona_name> <data_dir>
```

Example:

```text
/persona distill mao_zedong data/MaoZeDongAnthology-master/src
```

What this should do:

1. create `store/personas/<persona_name>/`
2. scaffold the project
3. set `corpus_root`
4. inspect the raw corpus directory directly
5. choose source-grounded dimensions, evidence, voice, and scenarios
6. write or rewrite `persona.json`
7. validate the artifact
8. build runtime modules
9. refresh the catalog
10. finish only when the persona is usable or a concrete blocker has been identified

Use:

```bash
python skills/persona/scripts/cli/persona_cli.py distill <persona_name> <data_dir>
```

Important:

- `/persona distill` is an end-to-end skill workflow
- do not stop after bootstrap unless the user explicitly asked for initialization only
- the CLI script above is the bootstrap helper used inside the workflow, not the whole workflow by itself
- the scaffold should provide a rich multi-dimensional template, not an empty shell
- the agent should prune unsupported dimensions and fill supported ones from direct corpus reading
- it does not generate candidate passages, block indexes, keyword search packs, or heuristic drafts
- a `bootstrapped` or `draft` persona is not a successful `/persona distill` result unless the user explicitly asked to stop early

If a persona with the same name already exists:

- do not overwrite silently
- in the interactive skill workflow, ask the user whether to delete and rebuild
- if the operator is using the CLI helper directly, fail with a clear message and point them to `/persona delete <name>`

## Distill Rule

For `/persona distill`, the extraction method is agentic direct reading.

Before doing any work, load and obey:

- `references/extraction/distill_execution_prompt.md`

The assistant should:

1. bootstrap the workspace with the CLI helper if the persona directory does not already exist or needs rebuilding
2. if a persona with the same name already exists, ask the user whether to delete and rebuild instead of overwriting silently
3. read the raw corpus directory directly
4. choose dimensions based on the actual source material instead of forcing a fixed template
5. manually author `source_index` and `evidence_index` only for the sources and excerpts actually used
6. write or rewrite `persona.json` from direct source understanding
7. run final validation
8. build runtime modules
9. refresh the catalog
10. confirm whether the persona is now router-ready

Unless the user explicitly asks to stop early, `/persona distill` should complete the full extraction in one command flow.

For actual execution, this means:

- after bootstrap, immediately inspect the corpus directory and start reading source files in the same turn
- do not wait for another user message such as “继续蒸馏”
- do not summarize a plan and stop
- do not hand the user a partially prepared workspace as if that fulfilled the command
- keep writing and validating until the artifact reaches `final` and becomes router-ready

## Distill Acceptance Criteria

Treat `/persona distill` as incomplete unless all of the following are true:

1. `persona.json` is populated from direct corpus reading rather than left as a template shell
2. `source_index` is non-empty and reflects the actual source files used
3. `evidence_index` is non-empty and each important dimension is anchored to real evidence
4. there are enough filled dimensions to model the persona in detail, not just a few generic traits
5. `scenario_library` is populated with representative source-grounded or clearly marked synthetic cases
6. `validate_persona.py --mode final` passes
7. `build_persona_modules.py` has been run
8. the catalog has been refreshed
9. the persona is router-ready

Do not answer as if distillation succeeded when the artifact is only a scaffold, only a bootstrap, or missing evidence.

Do not generate or rely on `candidate_passages.json`, `candidate_evidence.md`, `block_index.json`, or heuristic draft synthesis.

## Distill Enforcement

When the user invokes `/persona distill <name> <data_dir>`, treat it as an execution order, not a planning request.

Required behavior:

1. do not stop after calling the bootstrap CLI helper
2. do not return a “next steps” message as the main result
3. do not claim success until final validation passes and the persona is router-ready
4. continue reading files, writing `persona.json`, validating, and rebuilding until either:
   - the distill completes successfully, or
   - a concrete blocker is found that cannot be resolved within the current turn
5. if a blocker occurs, report the blocker precisely and include the exact file, command, or validation failure

Forbidden completion states for `/persona distill`:

- `bootstrapped`
- `draft` without passing final validation
- empty `source_index`
- empty `evidence_index`
- empty or near-empty `scenario_library`
- template-like dimensions with blank synthesis summaries

Forbidden assistant outcomes for `/persona distill`:

- replying mainly with “bootstrap ready”
- replying mainly with “next steps”
- asking the user to manually continue distillation in a follow-up turn
- claiming the command succeeded when the persona is not `final`
- switching the persona before final validation passes

### 4. Delete

Delete a distilled persona:

```text
/persona delete <persona_name>
```

Use:

```bash
python skills/persona/scripts/cli/persona_cli.py delete <persona_name>
```

Rules:

- if the persona does not exist, say it does not exist
- do not delete the built-in `starter_template`

### 5. List

List all distilled personas:

```text
/persona list
```

By default this should list distilled personas and hide template personas.

Use:

```bash
python skills/persona/scripts/cli/persona_cli.py list
```

### 6. Switch / Use

Enter persona mode:

```text
/persona <persona_name>
/persona <persona_name> <scene>
/persona switch <persona_name>
/persona switch <persona_name> <scene>
```

Supported scene hints:

- `default`
- `decision`
- `conflict`
- `analysis`

Example:

```text
/persona mao_zedong
/persona mao_zedong conflict
```

Use:

```bash
python skills/persona/scripts/cli/persona_cli.py use <persona_name> [scene]
```

Explicit switch alias:

```bash
python skills/persona/scripts/cli/persona_cli.py switch <persona_name> [scene]
```

### 7. Exit

Leave persona mode:

```text
/persona exit
/persona off
/persona quit
退出persona
退出角色
退出skill
```

### 8. Fuse

Create a fused final persona from 2-3 existing final personas:

```text
/persona fuse <new_persona_name> <name1> <name2>
/persona fuse <new_persona_name> <name1> <name2> <name3>
```

Example:

```text
/persona fuse mao_hybrid mao_zedong lu_xun
```

Use:

```bash
python skills/persona/scripts/cli/persona_cli.py fuse <new_name> <name1> <name2> [name3]
```

More than 3 source personas is not supported by default. If the user insists, warn that output quality is not guaranteed.

Rules:

- do not overwrite an existing target persona silently
- source personas should already be `final`
- `/persona fuse` should finish by building modules, passing final validation, refreshing the catalog, and making the fused persona router-ready
- if the fused artifact cannot pass final validation, report the exact blocker instead of calling it complete

## Router Behavior

If the first argument matches:

- `help`
- `language`
- `list`
- `distill`
- `delete`
- `fuse`
- `exit`
- `off`
- `quit`

then treat it as a subcommand.

Otherwise treat it as a persona switch request:

```text
/persona <persona_name> [scene]
```

## Roleplay Rule

When persona mode is active:

- remain fully in character until exit
- answer in first person as the persona in ordinary dialogue
- if asked `你是谁` or `who are you`, answer as the persona would identify themselves
- if asked whether you are literally the real person, the underlying model, or a simulation, answer truthfully that this is a persona-based simulation, then continue according to the user's requested mode
- do not drift back to neutral assistant style unless the user exits or explicitly requests out-of-character analysis
- if `/persona language <language>` is active, answer in that language while preserving persona voice
- if no override is active, answer in the persona default language

## Runtime Selection

For switching into a persona:

1. resolve persona from `store/personas/catalog.json`
2. choose a load profile by explicit scene or scene heuristic
3. load only the modules required for that profile
4. avoid loading the full artifact unless deep analysis is required

## Agentic Distill

When extracting a new persona, prefer this order of authority:

1. direct reading of source texts in the user-provided corpus directory
2. the scaffold dimension template as a modeling checklist
3. validation failures as feedback on what still needs to be authored

The extraction workflow should be controlled by the assistant's reading and judgment, not by fixed keyword rules alone.

## Internal Layout

This skill is organized as one unified directory:

- `scripts/cli/` for public command routing
- `scripts/extraction/` for distillation and validation
- `scripts/runtime/` for switching, cataloging, prompt rendering, and fuse
- `scripts/shared/` for shared path resolution helpers
- `store/personas/` for portable distilled persona artifacts bundled with the skill
- `references/extraction/` for extraction contracts and modeling references
- `references/runtime/` for roleplay/runtime rules
- `legacy/` for archived pre-merge skill folders retained only for reference
