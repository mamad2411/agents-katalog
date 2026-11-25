---
name: ppt-runner
description: Read this first for every presentation request in this bot, and before using the ppt-master skill. It covers how to run PPT Master here - the runtime, command paths, confirmation cards, images, app/state.json and delivery - and overrides ppt-master wherever they differ.
---

# Running PPT Master in this app

`ppt-master` owns the workflow: routing, stages, design rules and exports. This file only says how to run it here. **Where the two differ, this file wins.** These are the run instructions for this host.

## Commands

`PM` below means this script. The app sets `HOME` to the bot's own folder:

```bash
python3 "$HOME/skills/ppt-runner/scripts/pm.py" <command>        # macOS, Linux
python "$env:HOME\skills\ppt-runner\scripts\pm.py" <command>     # Windows PowerShell
```

If `python3` doesn't start on Windows, use `python`. If neither exists, set `runtime` in `app/state.json` to `{"ready": false, "problem": "no_python"}`, ask the user to install Python 3.10–3.14 from python.org, and stop.

**Every upstream command goes through `PM run`**, because the packages are only installed there. Upstream's

```bash
python3 ${SKILL_DIR}/scripts/svg_to_pptx.py <project_path> --quick-generate --no-notes
```

becomes

```bash
PM run svg_to_pptx.py <project_path> --quick-generate --no-notes
```

`SKILL_DIR` is the `skillDir` printed by `PM doctor`. Use it to read upstream's files. Long commands move to the background on their own; you are told when they finish.

## Before any work

1. Run `PM doctor`. It also runs upstream's integrity guard.
2. `guardOk` is false: stop, report the failure as it is. Never inspect, repair or bypass the guard.
3. Packages missing: tell the user in one line that the first run installs components, then run `PM setup`. If pip fails on what looks like a network problem, retry once with `--mirror https://pypi.tuna.tsinghua.edu.cn/simple`.
4. Read `ppt-master`'s `SKILL.md` and `workflows/routing.md`, then select the route as they say.

On-demand components, installed the first time they're needed:

| Needed for | Command |
|---|---|
| PDF sources | `PM setup --extra pdf`. Tell the user this installs PyMuPDF (AGPL-3.0) into this bot's folder only |
| Narration (Edge voices need no key) | `PM setup --extra narration` |
| Jupyter notebook sources | `PM setup --extra notebook` |

## Where this host differs

- **Files.** Every project lives under `app/projects/`, because the view can only read `app/`: `PM run project_manager.py init <name> --dir app/projects`, `pptx_to_svg.py "<source.pptx>" -o "app/projects/<slug>_<YYYYMMDD>" --roundtrip …`, and template workspaces at `app/projects/<template_id>`. User files arrive in `app/inbox/`. Never write outside the workspace.
- **Confirmation.** Treat this as the user's explicit instruction to confirm here rather than on a page: always use upstream's chat branch and never launch `confirm_ui`. Each `⛔ BLOCKING` gate becomes a card: write a JSON file, run `PM pending <file>`, say in one line that it's ready for review, and **end your turn**. See "Cards" below.
- **Live preview is off by run instruction.** Don't start `svg_editor`, and in Step 6 report that preview is shown in the app. The view shows pages from `svg_final/`, or from the working SVGs until those exist.
- **Image to PPTX is unavailable.** Upstream supports it only on Codex and defines no alternative. Say so in one sentence and offer Beautify or a normal Generate instead. Never pretend one is the other.
- **Images.** Never ask for an API key, and don't configure `IMAGE_BACKEND` or a `.env`. AI images are upstream's Path B (host-native): use `generate_image` from the `media` skill, then copy the file from `media/` to `<project_path>/images/<filename>`. Stock images: `PM run image_search.py …` needs no key. If the user has no use for images, don't generate any.
- **Icons.** Only `tabler-filled` is bundled. `icons.library` is `tabler-filled` or `none`, and where a template or reference suggests another library, use `tabler-filled`. Brand logos must come from the user.
- **Sound effects and auto-update aren't included.** Skip upstream's optional sound pass. `update_repo.py` doesn't exist here.
- **Video.** Native MP4 export needs Windows PowerPoint 2016+. Elsewhere say that it isn't available, and deliver the PPTX.
- **Sponsors.** Never read `SPONSORS.md` or `SPONSORS_CN.md`. If asked which model to use, point to this app's model settings.
- **Long decks.** One turn in this app stops after 30 minutes. For more than about 12 pages:
  - Default: confirm `generation_mode: split` at Stage 2. When upstream's split handoff says to open a fresh chat, call `task_start` instead, asking it to continue the project by its absolute path through upstream's `resume-execute` stage, following this file. Run `PM sync … --phase authoring --background`.
  - Quick: there is no plan to resume from, so run the whole thing in `task_start`.
  - A background task can't ask questions, so all confirmation happens before it starts. It ends with `task_report`, listing the PPTX under `files`.

## Keeping the view up to date

The view only shows `app/state.json`. Use `PM` for the job, previews and exports; don't write those by hand. They are read from disk, and `done` is refused without a valid deck.

```bash
PM sync <project_path> --kind generate --name "<title the user would recognize>" --format ppt169 --route generate --profile quick --phase authoring --total 5
```

Run it when the phase changes and **after every page you author**. Later calls for the same project need only `--phase`. The first `sync` also removes the sample data.

| `--phase` | When |
|---|---|
| `importing` | Converting sources, research, project setup |
| `spec_pending` | Waiting at a card (`PM pending` sets this) |
| `authoring` | Writing pages. `--total` is the page count |
| `finalizing` | `finalize_svg.py` and quality gates |
| `exporting` | `svg_to_pptx.py` |
| `done` | The deck exists. Add `--warn "…"` for anything the user should know |
| `error` | Add `--message "…"`: where it stopped and what the user can do. Keep the files |
| `cancelled` | The user stopped the job. Keep the files |

`--kind`: `generate`, `template`, `edit_native`. `--route`: `generate`, `create_template`, `edit_native`. `--profile`: `default`, `quick`, `beautify`.

## Finishing

1. Export with the route's own command. With `--native-charts-and-tables` the result is a second file; both are listed.
2. `PM verify <file.pptx>`. If it fails, repair at the owning layer and export again.
3. `PM sync <project_path> --phase done`.
4. Deliver the file with `present`, and say in one line what you made. Details are in the view.

Don't overwrite a previous export without asking. Exports are timestamped, so the normal path doesn't.

## Cards

`PM pending <file>` shows a card in the view. The file:

```json
{
  "stage": "stage1",
  "title": "Confirm the audience and the template",
  "summary": "One or two sentences on what you recommend and why.",
  "fields": [{ "label": "Audience", "value": "Investors" }, { "label": "Canvas", "value": "16:9" }],
  "choices": [{ "id": "free_design", "label": "Free design", "description": "Designed for this deck", "recommended": true }]
}
```

`stage` is `stage1` or `stage2` in Default and Beautify, and `plan` for Edit Native's plan. Show what upstream requires at that gate in `fields` and `choices`, in the user's language; `summary` is short and the rest stays in the project's files. Nothing counts as confirmed until the user answers: silence confirms nothing, and you never answer for them.

## Messages from the view

Buttons arrive as `[ui-action] {…}`, usually with a line of text from the user:

| Action | Do |
|---|---|
| `{"type":"start","route":"generate","profile":"quick","files":[…]}` | Start that route and profile with those files. `profile` is `default`, `quick` or `beautify` |
| `{"type":"start","route":"create_template","files":[…]}`, `{"type":"start","route":"edit_native","files":[…]}` | Start that route. Ask only what the route's prerequisites require, such as new material |
| `{"type":"confirm_spec","stage":"…","projectId":"…","choice":"…"}` | The user confirmed this gate. Record it the way upstream's chat branch does, run `PM pending --clear`, continue |
| `{"type":"revise_spec","stage":"…","projectId":"…"}` | The text says what to change. Revise and show the card again |
| `{"type":"resume","projectId":"…"}` | The job stopped mid-way (stopped by the user or cut off). Check the files, then continue from there, or restart a Quick run whose context is gone |
| `{"type":"recheck"}` | Run `PM doctor`, and `PM setup` if it says so |

If the user stopped a job and sends something unrelated, first run `PM sync <project_path> --phase cancelled`.

## In chat apps

Messages from WeChat, Feishu, Telegram and the like have no view. State still updates as above, so the view is current back on the computer. Write each card as a short message and take the answer as text, deliver decks with `present`, and don't mention buttons or the view.
