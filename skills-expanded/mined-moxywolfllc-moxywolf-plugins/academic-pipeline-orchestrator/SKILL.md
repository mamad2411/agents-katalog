---
name: academic-pipeline-orchestrator
description: Coordinate the full academic content pipeline from a BibTeX file to a critiqued, publication-ready article — theme analysis, perspective, voice, formatting, structure, iterative drafting, bibliography, and a professor critique. Use when the user asks to run the academic pipeline, write an article from a bibliography, or take a .bib file all the way to a finished paper.
license: Proprietary - MoxyWolf LLC
---

# Academic Pipeline Orchestrator

Run an academic `.bib` file all the way to a publication-ready, professor-critiqued article. Eight stages (plus an optional Stage 0), three human checkpoints, one run folder.

## Pipeline

```
BibTeX input
    |
[0] bibtex-abstract-generator   (optional)   -> enriched .bib
    |
[1] bibtex-theme-analyzer                    -> theme_analysis.json, <target-slug>-themes.md, TARGET_TITLE
    |
[1.5] /scamper                    (optional)  -> scamper_results.json, scamper_outline.md (novelty-ranked thesis)
    |
[2] academic-perspective-builder   * HITL    -> perspective.json            (3 questions)
    |
[3] academic-voice                 * HITL    -> voice_context.json          (8 questions)
    |
[4] academia-formatting                      -> formatting_requirements.json
    |
[5] research-analyst               * HITL    -> handoff_for_writer.json     (structure approval)
    |
[6] research-writer                          -> draft_document.md
    |
[7] bibliography-generator                   -> <target-slug>.md
    |
[8] professor                                -> critique_report.md, improvement_plan.md
    |
[9] release_gate.py                          -> five named checks, blocking
```

`* HITL` = a human checkpoint. Three of them, twelve questions total.

## The key idea: voice-first

Most AI writing pipelines draft first, then try to bolt a voice and a format on afterward, then rewrite. This pipeline fixes **voice (Stage 3)** and **formatting (Stage 4)** *before* a word is drafted, so Stage 6 writes in the author's authentic voice and in Academia.edu structure from the first sentence. No retrofitting.

## How to run it

### Step A — Establish the run folder

Every artifact from one run lives in a single **run folder**:

- In a MoxyWolf project session, use `<active project>/11 – Project Knowledge/Papers/<target-slug>/`. The slug comes from the Stage 1 `TARGET_TITLE`; until Stage 1 names it, stage to a temporary `academic-pipeline-run/` folder and rename once the title is set.
- Outside a project, ask the user where to save, or use the Cowork outputs folder.

Layout:

```
<run folder>/
├── <target-slug>-themes.md          <- deliverable
├── <target-slug>.md        <- MAIN deliverable
├── critique_report.md          <- deliverable
├── improvement_plan.md         <- deliverable
└── pipeline/                   <- intermediate artifacts
    ├── enriched.bib            (only if Stage 0 ran)
    ├── theme_analysis.json
    ├── perspective.json
    ├── voice_context.json
    ├── formatting_requirements.json
    ├── handoff_for_writer.json
    └── draft_document.md
```

### Deliverable naming

Reader-facing deliverables are named from the run, never from a constant. `<target-slug>` is the kebab-cased `TARGET_TITLE` confirmed in Stage 1, the same slug the run folder uses. The paper is `<target-slug>.md` and the theme tree is `<target-slug>-themes.md`.

This matters because the run folder usually sits in an Obsidian vault, where the filename is the note title. A deliverable called `complete_document` is an unusable note title and collides in search with every other run's. Intermediate artifacts under `pipeline/` keep fixed names; they are machine inputs, not notes.

### Step B — Track the stages

Create a task list (TaskCreate) with one task per stage you will run, so the user can watch progress. Mark each `in_progress` when you start it and `completed` when its artifact is written.

### Step C — Choose a checkpoint mode

Ask the user once, up front, how they want the three HITL stages handled:

- **Stage-by-stage (default)** — the pipeline pauses at Stages 2, 3, and 5 and asks the questions in context. Best when the user wants to stay in the loop.
- **Front-loaded** — collect all twelve answers at the start (perspective 3, voice 8, plus advance permission to auto-approve a reasonable structure at Stage 5), then run straight through.

### Step D — Run the stages

Invoke each stage's skill in order, passing the run folder. Read the prior stage's artifact before starting the next. Each skill below has its own `SKILL.md` with full detail — the orchestrator's job is sequencing, the run folder, and the checkpoints.

## Stages

### Stage 0 — Enrich the bibliography (optional)

**Skill:** `bibtex-abstract-generator`. Run only if the input `.bib` has entries missing `abstract` fields — Stage 1 needs abstracts to map themes. Output: `pipeline/enriched.bib`, which becomes Stage 1's input. Skip silently if abstracts are already present.

### Stage 1 — Theme analysis

**Skill:** `bibtex-theme-analyzer`. Reads the `.bib`, builds a Mermaid theme tree, proposes and confirms `TARGET_TITLE`. Outputs: `pipeline/theme_analysis.json`, `<target-slug>-themes.md`. Title confirmation is a light touch, not one of the three formal HITL stages.

### Stage 1.5 — SCAMPER defixation (optional)

**Command:** `/scamper` (`scripts/scamper.py`, stdlib). Distill the Stage 1 themes into a literature baseline, run the seven SCAMPER operators, score each candidate thesis by TF-IDF distance from the baseline, and outline the top one. Runs only when prescribed: `/academic-pipeline --scamper`, or a yes to the SCAMPER option in the Step C checkpoint question. Use when the bibliography's consensus reading is the fixation to break. The confirmed thesis feeds Stage 2's `writing_perspective`. Outputs: `pipeline/scamper_baseline.json`, `pipeline/scamper_results.json`, `pipeline/scamper_outline.md`.

### Stage 2 — Perspective  * HITL (3 questions)

**Skill:** `academic-perspective-builder`. Three questions via AskUserQuestion: `writing_perspective`, `target_market`, `sub_themes`. Output: `pipeline/perspective.json`.

### Stage 3 — Voice  * HITL (8 questions)

**Skill:** `academic-voice`. Reads the standing voice profile from the vault, then asks eight article-specific questions via AskUserQuestion: `trigger`, `evidence`, `contrarian_take`, `authority`, `specific_reader`, `business_connection`, `call_to_action`, `emotional_core`. Output: `pipeline/voice_context.json`.

### Stage 4 — Formatting requirements

**Skill:** `academia-formatting` in **pipeline mode** (automatic — no voice interview; Stage 3 already covered voice). Distills Academia.edu structure and MoxyWolf anti-AI rules into `pipeline/formatting_requirements.json`.

### Stage 5 — Research analysis  * HITL (structure approval)

**Skill:** `research-analyst`. Consumes Stages 1–4, analyzes the sources, designs a section-by-section structure, and presents it for approval via AskUserQuestion (approve / modify / reject). Output: `pipeline/handoff_for_writer.json`.

### Stage 6 — Iterative writing

**Skill:** `research-writer`. Writes the paper section by section in an internal loop, applying voice and formatting while drafting. Output: `pipeline/draft_document.md` with a `## Bibliography` placeholder.

### Stage 7 — Bibliography

**Skill:** `bibliography-generator`. Formats every cited source in the handoff's citation style and replaces the placeholder. Output: **`<target-slug>.md`** — the main deliverable.

### Stage 8 — Professor critique

**Skill:** `professor`. Runs the 10-phase review (AI-detection first, then integrity, citations, logic, methodology, literature, evidence, writing, contribution) on `<target-slug>.md`. Outputs: `critique_report.md`, `improvement_plan.md`.

## HITL behavior

The three checkpoints use the **AskUserQuestion tool** directly — ask, get the answer, continue. There is no HITL request file, no blocking handoff, no GSD executor. If checkpoint mode is *front-loaded*, collect the twelve answers at Step C and pass them into Stages 2, 3, and 5 so those skills skip their prompts.

## Stage 9 — The release gate

Before presenting anything as finished, run the gate. It is not a checklist to remember; it is a command that exits nonzero.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/release_gate.py" \
  --paper "<run folder>/<target-slug>.md" \
  --requirements "<run folder>/pipeline/formatting_requirements.json"
```

Five checks, each named with its result: `em_dashes` (zero), `forbidden_phrases` (zero, from the Stage 4 list), `sections_present` (every `section_order` entry appears as a heading), `duplicate_sources` (no two references share a normalized DOI or URL), and `citation_order` (the renumber pass reports zero renumbered, for Vancouver).

**A failing gate blocks the completion report.** Do not narrate around it, do not present the deliverable with a note about what did not pass, and do not ask the user to accept it. Fix what failed, rerun, and only then continue. Report the gate's five lines verbatim as part of the completion summary, passing or failing, so the reader can see which checks ran rather than trusting that they did.

The gate is mechanical and therefore narrow. It cannot tell whether an argument holds, whether a citation supports the claim resting on it, or whether the paper is any good. Stage 8's critique does that, and the gate does not replace it.

## On completion

When all stages finish:

1. Present `<target-slug>.md` as the main deliverable, with a `computer://` link.
2. Present `critique_report.md` and `improvement_plan.md`, and surface the professor's headline verdict and grade in chat.
3. List the run folder and the nine (or ten, with Stage 0) artifacts.
4. Offer next steps: review the critique, apply the improvement plan and re-run Stage 8, or render `<target-slug>.md` as a formatted `.docx`/PDF via the `academia-formatting` skill plus the `docx`/`pdf` skills.

## Artifact summary

| Stage | Artifact | Location |
|-------|----------|----------|
| 0 | `enriched.bib` | `pipeline/` |
| 1 | `theme_analysis.json` | `pipeline/` |
| 1 | `<target-slug>-themes.md` | run folder |
| 2 | `perspective.json` | `pipeline/` |
| 3 | `voice_context.json` | `pipeline/` |
| 4 | `formatting_requirements.json` | `pipeline/` |
| 5 | `handoff_for_writer.json` | `pipeline/` |
| 6 | `draft_document.md` | `pipeline/` |
| 7 | `<target-slug>.md` | run folder — **main deliverable** |
| 8 | `critique_report.md`, `improvement_plan.md` | run folder |
| 9 | gate result (five named checks) | reported in chat, blocking |

## Notes

- Run stages in order; each reads the previous artifact. If a stage fails, stop and report — don't fabricate a downstream artifact.
- The pipeline reads BibTeX files directly. There is no document-retrieval pagination step.
- One run, one run folder. Don't scatter artifacts across the workspace.
