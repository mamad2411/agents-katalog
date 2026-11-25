---
name: new
description: "Use when starting a brand-new Power Apps app from scratch: stage 1 of the kit pipeline (Orchestrator). Takes the idea, creates the project folder, git, power-platform.config.json, 00-READ-ME-FIRST.md and STATE.md, and points to the next command. Do not use for an app that already exists (describe the problem and the `power-platform` orchestrator picks the path) or to continue a project already started (use `/pp-en:progress`)."
argument-hint: "[the app idea: a sentence, a list or pasted text]"
user-invocable: true
disable-model-invocation: true
---

# /pp-en:new — Orchestrator: project start

First stage of the pipeline (`KIT/skills/power-platform/references/pipeline.md`). In 5 minutes the
project gets the structure every following stage reads. No screens, tables or flows here.

`KIT` = `${CLAUDE_PLUGIN_ROOT}` (the plugin folder). Banner, checkpoint and next-step format:
`KIT/skills/power-platform/references/output-format.md`. State script:

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/estado.py" <command>
```

## Before you start

1. Look for `STATE.md` in the current folder and the ones above it. **If it exists**, the project was
   already started: run `estado.py mostrar`, show the output and stop.
2. Show the `PP ► NEW PROJECT` banner and say in one sentence what is about to happen.

## Steps

1. **The idea, as it comes.** If `$ARGUMENTS` brought it, use it. Otherwise ask: "Tell me the app
   idea: a sentence, a messy list, pasted text, a screenshot or a spreadsheet all work. The more
   comes in now, the fewer questions the brainstorm will ask." Accept whatever comes, without asking
   for a format.
   - Extract the **idea in one sentence** (what it solves and for whom) for `STATE.md`.
   - Password, key or token in the middle: do not save it, and warn the user to change it.
   - Only one sentence came: carry on; the brainstorm leads the rest.
2. **The name.** Propose a short name derived from the idea (e.g. `Orders`) and confirm it. No
   spaces or accents in the folder name.
3. **Three choices in one round:** a single `AskUserQuestion` call with the three questions
   (they are independent; the user answers all at once):
   - header `Folder`: "Use this folder" (recommended when it is empty or only has project material)
     or "Create the `<Name>/` subfolder here";
   - header `Commits`: "Each stage makes a commit at the end (Recommended)" or "I handle the commits";
   - header `Models`, "Who thinks and who executes?": Balanced (Recommended), Maximum, Economical,
     Inherit. The `preview` of each option is the profile block that
     `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/modelos.py" perfis` prints;
     the description, the "when" sentence from `KIT/skills/power-platform/references/models.md` §1.
   Free-text answer on Models (e.g. "Opus on everything"): the closest profile plus the
   `--sessao`, `--planejamento`, `--execucao` swaps from step 5.
   For the subfolder, warn right away: the next sessions must be opened **inside it** (close and
   reopen Claude Code there; `/clear` does not change folders).
4. **Create the structure** at the project root:
   - `git init` if the folder is not inside a repository;
   - `.gitignore` with: `dist/`, `.env`, `*.msapp`, `*.zip`, `__pycache__/`, `*.tmp`,
     `AS-BUILT-ENVIRONMENT/capturas/`, `docs/planning/**/capturas/`, `.claude/settings.local.json`;
   - `power-platform.config.json` from `KIT/skills/power-platform/assets/power-platform.config.example.json`:
     `projeto` = name; **remove** `trilha_dados` and `prefixo_publisher` (the architecture decides);
     `git_commit_por_etapa` from the answer on Commits;
   - `00-READ-ME-FIRST.md` from `KIT/skills/power-platform/assets/read-me-first-template.md`, with the idea;
   - folders `docs/planning/` and `docs/decisions/`;
   - `docs/planning/raw-idea.md` from the template `KIT/skills/power-platform/assets/raw-idea-template.md`:
     what came in step 1 (text as it came; screenshot or spreadsheet described in the attachments
     table) and section 3 filled in with what can already be extracted, each item with its source.
     Do not complete what the idea does not say: a block with no information stays "—".
5. **Models:** `modelos.py aplicar <profile> [swaps]` from the project root (for the subfolder,
   `--raiz <Name>` before `aplicar`). Show the output and say in one line: the next stages
   open the session on `<model>` and each agent gets its own; this session stays on the current model.
6. **State:** `estado.py iniciar --projeto "<Name>" --ideia "<idea in one sentence>"` (for the
   subfolder, add `--raiz <Name>`).
7. **Commit** (if `git_commit_por_etapa`): `git add -A` and `git commit -m "pp(new): project structure <Name>"`.
   `.claude/settings.local.json` stays out (it is personal).

## Exit gate

`STATE.md`, `power-platform.config.json` (with `modelos`) and `00-READ-ME-FIRST.md` exist at the root,
and `docs/planning/raw-idea.md` holds everything the user sent;
`git status` works. Check with `ls` and `modelos.py mostrar` before closing.

## Wrap up

Summary in up to 4 lines (folder, files created) and the "Next step" block that `iniciar`
printed, unchanged. If the project went into a subfolder, add one line before the block:
"Open Claude Code inside `<Name>/` for the next stage".
