---
name: story-architect-skill
description: Engineer fiction-writing projects for Claude Code from idea through final manuscript. Use when initializing or adopting a short story, novella, novel, or serial project; designing characters, worlds, plots, timelines, scenes, prose, or revisions; reviewing chapters; checking continuity, clues, promises, and payoffs; or maintaining structured story files, project commands, context packs, and writing progress.
---

# Story Architect

Build stories as maintainable creative systems while preserving the author's final authority.

## Operating contract

1. Treat the author's latest explicit instruction as highest priority.
2. Preserve existing prose and project files unless the author requests changes.
3. Separate proposals from canon. Never turn brainstorming into established fact silently.
4. Read only the context required for the current stage; use the routing table below.
5. Ask only when a missing choice would materially change the result. Mark smaller assumptions as `Proposed`.
6. Keep creative decisions inspectable without exposing hidden chain-of-thought. In prompt templates, `<thinking>` means a concise decision summary, not private reasoning.
7. Verify file changes and run the relevant project checks before reporting completion.

## Initialize or adopt a project

Resolve the requested destination before writing. If the directory contains files, preserve them and report collisions rather than overwriting.

Run:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/init_story_project.py" \
  --destination "<project-directory>" \
  --title "<story-title>" \
  --genre "<genre-or-comma-separated-genres>" \
  --length "<short|novella|novel|serial>" \
  --language "<language>" \
  --collaboration-mode "<author|muse|artisan|debater|creator|curator>"
```

Use `--dry-run` when the destination or scope is uncertain. Use `--adopt-existing` for an existing manuscript; the script creates the framework without moving or rewriting source files.

After initialization:

1. Read `<project>/CLAUDE.md`.
2. Fill `00_Project/story-brief.md` with confirmed information.
3. Record consequential choices in `00_Project/decisions.md`.
4. Run:

```bash
python3 "<project>/.story/tools/story_lint.py" --root "<project>"
python3 "<project>/.story/tools/story_status.py" --root "<project>"
```

## Source-of-truth order

Resolve conflicts in this order:

1. Latest explicit author instruction
2. `00_Project/decisions.md`
3. `06_Continuity/canon.md`
4. Approved character and world files
5. Approved outlines, timeline, and thread ledger
6. Existing draft prose
7. Research notes and discarded ideas

Flag unresolved conflicts. Do not choose silently when the choice changes plot, character motivation, theme, POV, or ending.

## Workflow router

| Task | Read first | Then use |
| --- | --- | --- |
| Establish project rules | `references/project-schema.md` | `references/collaboration-modes.md` |
| Develop premise or theme | project brief | `references/story-foundations.md` |
| Create or revise characters | brief, decisions, outline, canon, relationship files | `references/character-design.md` |
| Build a setting or system | brief, decisions, canon, relevant characters | `references/worldbuilding.md`, then `references/genre-guides.md` |
| Create an outline | brief, characters, world, decisions | `references/plot-structures.md`, `references/story-foundations.md` |
| Plan a scene | outline, timeline, threads, relevant character/world files | `references/scene-and-prose.md` |
| Write prose | scene plan, style guide, relevant canon, prior/next scene context | `references/scene-and-prose.md`, relevant genre section |
| Review or revise | target draft, style guide, scene purpose, canon | `references/revision-and-continuity.md` |
| Check consistency | timeline, canon, threads, knowledge state, affected drafts | `references/revision-and-continuity.md` |
| Engineer a prompt | requested command template | `references/prompt-contract.md` |

Do not load every reference by default.

## Project commands

Initialization installs these project commands under `.claude/commands/`:

- `/generate_character` — create or update a structured character card.
- `/build_world` — expand setting, systems, culture, institutions, and consequences.
- `/plot_outline` — select a fitting structure and create an act/sequence/scene outline.
- `/plan_scene` — create a scene contract before prose.
- `/write_scene` — write one bounded scene and update factual ledgers.
- `/review_chapter` — diagnose a chapter without editing it by default.
- `/revise_chapter` — apply an approved revision brief.
- `/check_continuity` — audit chronology, canon, knowledge, causality, and voice.
- `/manage_threads` — maintain setups, promises, clues, and payoffs.
- `/brainstorm_story` — generate deliberately varied options with tradeoffs.
- `/story_status` — summarize progress, counts, open tasks, and markers.
- `/finalize_story` — run release checks and create a clean final copy.
- `/import_manuscript` — adopt existing prose without relocating or overwriting it.

Use the command's XML contract exactly. Map `$ARGUMENTS` to its `{{variables}}`; resolve remaining variables from project files or ask one focused question.

## Drafting protocol

Before writing prose:

1. Confirm the target scene and file.
2. Read the scene contract, style guide, POV character, location, active threads, timeline, knowledge state, and immediately adjacent prose.
3. Check what the viewpoint character knows at scene start.
4. Produce a compact `<thinking>` decision summary containing scene goal, opposition, turn, emotional movement, and continuity constraints.
5. Write the prose in `<draft>`.

While drafting:

- Make every scene alter value, knowledge, relationship, position, or commitment.
- Prefer concrete nouns and active verbs; use description selectively.
- Use sensory detail as evidence of viewpoint, not as a checklist.
- Keep dialogue driven by desire, resistance, and subtext.
- Control pace through narration-versus-dramatization, sentence rhythm, and scene compression.
- Preserve established voice, tense, POV, rules, and knowledge boundaries.

After drafting:

1. Update `03_Outlines/timeline.md` with what actually happened.
2. Update `03_Outlines/threads.md` for setups and payoffs actually present.
3. Add only confirmed facts to `06_Continuity/canon.md`.
4. Update `06_Continuity/knowledge-state.md` when character knowledge changes.
5. Update `00_Project/progress.md`.
6. Run the linter on the affected project.

## Review protocol

When the author asks only for review, diagnose and report; do not rewrite.

Assess in this order:

1. Story purpose and scene function
2. Causality, stakes, and escalation
3. Character agency, motivation, and arc
4. POV, knowledge, timeline, and canon
5. Pacing and information flow
6. Dialogue, description, sentence craft, and repetition

Rank findings as blocking, major, moderate, or optional. Cite exact file sections or short excerpts. Distinguish objective contradiction from subjective preference.

## Context and maintenance tools

Use:

```bash
python3 ".story/tools/build_context_pack.py" --root "." --task "<task>" --focus "<path>"
python3 ".story/tools/story_lint.py" --root "."
python3 ".story/tools/story_status.py" --root "."
```

Read `references/project-schema.md` for file ownership, annotation syntax, adaptive genre files, and tool behavior.

## Knowledge references

- `references/story-foundations.md` — premise, story engine, theme, stakes, scene change, and length scaling.
- `references/character-design.md` — character cards, arcs, relationships, voice, and knowledge boundaries.
- `references/worldbuilding.md` — causal worldbuilding, systems, culture, institutions, and research.
- `references/plot-structures.md` — structure selection, three-act, hero's journey, snowflake, sequence, and serial design.
- `references/scene-and-prose.md` — scene contracts, narration, description, dialogue, camera, senses, time, and transitions.
- `references/revision-and-continuity.md` — layered revision, continuity auditing, clue fairness, and finalization.
- `references/genre-guides.md` — genre-specific promises and failure modes.
- `references/collaboration-modes.md` — six human-AI collaboration modes.
- `references/prompt-contract.md` — XML prompt and variable conventions.
- `references/project-schema.md` — scaffold layout and canonical file responsibilities.
