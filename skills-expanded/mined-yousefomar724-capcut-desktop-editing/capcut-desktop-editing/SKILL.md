---
name: capcut-desktop-editing
description: Edit video in the real CapCut desktop app on Windows through computer use — driving the UI the way a person does (grid screenshots, keyboard shortcuts and the UI Automation tree wherever CapCut exposes it) instead of generating video from code. Builds and applies user-approved CapCut procedures one demonstrated capability at a time and writes each exact working procedure back into this skill. Use this whenever the user wants anything done inside CapCut or CapCut Pro — splits, trims, removing pauses or filler words, bad takes, jump cuts, push-ins, auto captions, text animations, B-roll, 9:16 reframes, vocal isolation, background removal, camera tracking, transitions, color, export — or asks to map CapCut's controls, train or teach the agent on CapCut, or continue the CapCut capability ladder. Not for code-rendered video (HyperFrames, Remotion, ffmpeg pipelines) or CapCut web/mobile.
metadata:
  compatibility: "Windows 10/11 with CapCut desktop (mapped on 9.4.0.4015) and uv for the bundled Python venv. Written for both Claude Code and Codex."
---

# CapCut Desktop Editing

You edit in CapCut the way a human editor does: you look at the app, operate its real controls,
check what happened, and keep a written record of the exact route that worked. The skill is a
**capability ladder**. Each rung is a native CapCut procedure that has been demonstrated on real
footage, verified, written down here, and approved by the user. Nothing advances until the previous
capability is demonstrated and approved.

The references are a living document: they get better every time you run the loop. Treat anything
not marked verified as a hypothesis to test, not a fact.

For a requested production edit, reuse the approved procedures and read
`references/house-style.md`; the capability loop below applies to learning new procedures.
When all ladder rows are approved, proceed with the requested edit rather than restarting the
ladder or asking for approval of each already-approved operation. Prior training projects are
examples, not the target of a new editing request. Use the footage/project from the current task.
For Codex, the platform file determines which control backend is usable; the `cc.py` commands
below describe the bundled-script backend.

## 0. Orient yourself (every session)

1. **Read your platform file first.** It tells you how to run the scripts and view screenshots with
   your tools.
   - Claude Code → `references/platform-claude-code.md`
   - Codex → `references/platform-codex.md`
2. **Read `references/capability-ladder.md`.** It is the gate. Find the lowest rung that is not
   `approved`. That rung is the only new thing you may work on.
3. **Check the CapCut version.** Run `cc.py version`. If it is newer than the version recorded in
   `accessibility-controls.md`, say so and re-verify controls before relying on them. CapCut
   auto-updates and moves things around.
4. **First run on a machine:** run `scripts/setup.ps1` (creates `scripts/.venv`), then
   `cc.py windows` to confirm CapCut is visible.

Commands below use `PY` for `<skill>\scripts\.venv\Scripts\python.exe` and `<skill>` for this
skill's folder (resolve it from where you loaded this file).

## 1. Rules, and why they exist

1. **Approval gate.** Demonstrate one capability, then stop and wait for the user's explicit
   approval. You may freely reuse approved capabilities while demonstrating the next one. *Why:* a
   procedure that looked fine to you can still be editorially wrong. The user's taste is the spec,
   and unapproved procedures compound errors.
2. **Label your evidence.** Every claim in the references and your reports is exactly one of:
   - `observed`: seen in the tree or a screenshot
   - `executed`: the action was sent
   - `agent-verified`: the result was confirmed by a screenshot **and**, where it applies, the draft
     diff
   - `user-approved`

   Never upgrade a label you didn't earn. *Why:* the ladder is only trustworthy if "verified" means
   verified.
3. **Native UI only.** Every edit goes through CapCut's own UI. Never write, patch or restore
   `draft_content.json` or other project files. Read them only (`draft_inspect.py`). *Why:* the
   goal is a skill that operates CapCut, and hand-edited drafts can corrupt projects or desync
   CapCut's cache.
4. **Work on a duplicate.** Before editing, duplicate the project through CapCut itself (route in
   `references/project-safety.md`) and edit the copy. Never edit the user's original unless they
   explicitly ask for that project.
5. **Tree first, screenshots second, coordinates last.** Read `references/control-strategy.md`.
   - Re-read the tree after every action batch, because indices and rectangles are transient.
   - Never store pixel coordinates in references. Store names, AutomationIds, control types, menu
     routes, shortcuts and visual landmarks ("scissors icon, timeline toolbar, 3rd from left").
6. **Confirm before side effects.** Stop and ask before:
   - any purchase, subscription, upgrade or upsell dialog
   - account or login changes, or changes to CapCut settings
   - cloud upload/sync, publishing or sharing (TikTok/YouTube)
   - deleting projects or media from disk
   - any AI feature that spends credits

   Close upsell popups; never accept them. **Menu ▸ Account holds a single item, "Delete
   account"**, next to Settings and Back to home page. Move the pointer through that menu
   deliberately and never click inside the Account submenu. *Why:* these are irreversible or cost money, and
   subscribing to Pro was the user's decision, not a licence for you to spend.
7. **Keep your hands off the user's desktop when not editing.** Input goes to the foreground
   window. Tell the user before a batch starts that they shouldn't use the mouse or keyboard until
   you report back.

## 2. The capability loop

Run this for the lowest rung that isn't `approved`:

1. **Research the native route.** Check `accessibility-controls.md`, `pro-features.md` and
   `keyboard-shortcuts.md`, then look at the live UI (tree + screenshot). Prefer routes a CapCut
   editor would use: toolbar buttons, the right-hand inspector, the transcript editor, shortcuts.
2. **Prepare.**
   - Duplicate the practice project and open the copy.
   - Run `cc.py evidence <rung>-before --project "<copy name>"`.
   - Write down the goal and what "done" looks like.
3. **Execute in small batches.** Two to five actions, then re-read the tree or take a screenshot.
   When something unexpected appears (modal, upsell, wrong panel), stop the batch and deal with it.
4. **Verify.**
   - Take a screenshot of the result (zoom into the region that matters).
   - Let CapCut save: its autosave writes the draft. Returning to the home screen forces a write.
   - Run `cc.py evidence <rung>-after --project "<copy>"` and
     `draft_inspect.py diff <before summary> <after summary>`.
   - The diff must show exactly the intended change and nothing else.
5. **Test undo** when the capability is destructive: Ctrl+Z restores the state, then redo it.
6. **Write back.** Create or update `references/capabilities/NN-<slug>.md` using
   `references/capability-template.md`, with the exact route that worked:
   - the control identifiers
   - shortcuts
   - wait conditions
   - parameters, marking which ones are shot-specific
   - failure modes you hit and how you recovered
   - evidence paths

   Update `accessibility-controls.md` with every new control you touched. Set the ladder row to
   `demonstrated` with the date.
7. **Report and stop.** Tell the user what you did, show before/after screenshots, the diff summary
   and any open questions, and ask for approval or corrections.
8. **On approval:**
   - Set the row to `approved` (date plus the user's words) and update the evidence labels to
     `user-approved`.
   - Commit in the skill folder: `git add -A && git commit -m "capability NN approved: <slug>"`.
   - Only then may the next rung start.

   **On corrections:** fold them into the procedure, re-run, re-verify, report again.

## 3. Control stack (summary — details in `references/control-strategy.md`)

| Layer | Use for | Tool |
|---|---|---|
| UI Automation tree | Named buttons, tabs, menus, dialogs, fields, toggles and their state | `cc.py tree`, `find`, `act` |
| Keyboard shortcuts / menus | Split, undo, play, import, export: stable across layouts | `cc.py key` |
| Screenshots with grid | Timeline clips, waveforms, playhead, preview canvas, thumbnails, icon-only buttons | `cc.py screenshot --grid`, `click`, `drag` |
| Draft JSON (read-only) | Proving what an edit changed: segments, timings, texts, effects | `draft_inspect.py summary/diff` |

CapCut 9.x is built on **Qt 6 (Qt Quick/QML + Widgets) with CEF web panels**.

**Observed on 9.4.0.4015: the home window exposes only its root element to UI Automation. No child
controls are reachable through any walker, hit-testing or MSAA.** Until
`accessibility-controls.md` records otherwise for a given area, assume that area is
**screenshot-driven**:
1. Take a grid screenshot.
2. Identify the control by its visual landmark and hover tooltip.
3. Click the grid coordinate or use a shortcut.
4. Verify by screenshot and draft diff.

Always try `cc.py tree` first in each new area (editor, dialogs, popups, web panels), because
coverage can differ per window. Record what you find.

## 4. Script cheat sheet

```
PY <skill>\scripts\cc.py version                      # install path, installed + running version
PY <skill>\scripts\cc.py windows                      # CapCut top-level windows, rects, DPI
PY <skill>\scripts\cc.py focus --maximize             # bring CapCut forward (do before input)
PY <skill>\scripts\cc.py tree --filter interactive    # named controls; --depth, --root, --json
PY <skill>\scripts\cc.py find --contains Export       # --name/--regex/--type/--id, prints indices
PY <skill>\scripts\cc.py act invoke --name "Export"   # invoke|toggle|select|expand|collapse|set-value|click|double|right|hover
PY <skill>\scripts\cc.py act click --index 42         # index from the last tree/find (re-located live)
PY <skill>\scripts\cc.py screenshot --grid --scale 0.6            # labels are SCREEN coordinates
PY <skill>\scripts\cc.py screenshot --region 0,700,1920,1080 --grid  # zoom into the timeline
PY <skill>\scripts\cc.py click 812 904 [--double|--right]
PY <skill>\scripts\cc.py drag 800 900 1000 900 --steps 20
PY <skill>\scripts\cc.py scroll 960 900 -3 [--horizontal] [--ctrl]
PY <skill>\scripts\cc.py key ctrl+b                   # combos, space-separated sequences
PY <skill>\scripts\cc.py type "Hello"                 # Unicode-safe (Arabic OK); paste "..." uses clipboard
PY <skill>\scripts\cc.py wait-for --contains "Export" --timeout 30 [--gone]
PY <skill>\scripts\cc.py evidence 01-split-after --project "0707 copy"
PY <skill>\scripts\draft_inspect.py list
PY <skill>\scripts\draft_inspect.py summary "0707 copy" [--json out.json]
PY <skill>\scripts\draft_inspect.py diff before.json after.json
PY <skill>\scripts\draft_inspect.py words "0914 (4)" --around 295 --window 8   # caption word timings (after Auto captions)
PY <skill>\scripts\draft_inspect.py gaps "0914 (4)" --min 0.6 --keep 0.125     # silences between words + proposed cuts (flags edit joins)
PY <skill>\scripts\draft_inspect.py keyframes "0914 (4)"                        # segment keyframes on the timeline clock: property, value, curve + Bezier handles
PY <skill>\scripts\tighten_gaps.py --project "0914 (4)" --dry-run                # plan silence tightening (needs Auto captions; no input)
PY <skill>\scripts\tighten_gaps.py --project "0914 (4)" --count 5 --undo-captions  # do it natively: exact splits + W, verified per cut (rung 5)
```

Every command prints what it did. Input commands fail loudly if Windows blocked `SendInput`
(elevated window or sandbox).

## 5. Where things live

| File | Read it when |
|---|---|
| `references/capability-ladder.md` | Every session. It's the gate and the done-criteria per rung. |
| `references/house-style.md` | Before any real edit. It holds the user's approved defaults (e.g. Arabic-only captions with the black-box template). |
| `references/capabilities/NN-*.md` | Reusing or extending an approved procedure. |
| `references/accessibility-controls.md` | Locating any control. Update it whenever you touch a new one. |
| `references/pro-features.md` | Any Pro/AI feature: route, tier badge, credits, verification status. |
| `references/keyboard-shortcuts.md` | Before reaching for the mouse. |
| `references/control-strategy.md` | Tree/screenshot technique, DPI, Qt quirks, timeline positioning. |
| `references/project-safety.md` | Duplicating, backups, recovering from a bad edit. |
| `references/capability-template.md` | Writing a procedure back. |
| `references/platform-*.md` | How your agent runs this skill. |

## 6. Writing procedures back

Write procedures so a fresh agent with no memory of this session can repeat them exactly:

- **Steps are imperative and observable:** "Invoke `Button "Split"` (timeline toolbar) → expect
  the clip under the playhead to become two segments."
- **Identify each control** by tree query when it's exposed (`--type Button --name "Split"`), by
  shortcut when one exists, or by visual landmark when it's canvas-only. Always say which.
- **Record wait conditions** for anything async (AI captions, vocal isolation, export): what
  appears when it's done.
- **Separate universal settings from shot-specific values** ("scale 110% worked for this framing;
  judge per shot").
- **Record failures honestly.** Wrong turns and their fixes are the most valuable lines.

## 7. Adapting to the user's style

These procedures follow one editor's taste. The way to change them is the same loop that built
them: the user describes or shows the edit they want, you reproduce it natively in CapCut, verify
it, they approve, and you write it back. Add new rungs to the ladder when the user asks for a
capability that isn't listed. They start as `not-started` and follow the same gate.
