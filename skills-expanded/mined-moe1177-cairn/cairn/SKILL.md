---
name: cairn
description: Maintain the cairn workspace map: write repo summaries and settle unconfirmed cross-repo links. Use when the user runs /cairn or `cairn status` shows work to do.
---

# cairn

Keep the cairn workspace map accurate. Work from the workspace root (the folder containing `.cairn/`).

0. If there is no map yet (no `.cairn/` in this folder or above it, or `cairn status` says "No map found"):
   - Find the folder that holds the user's repos: usually the parent of the current repo, the one with several git repos in it.
   - Ask the user to confirm that folder. Building the map only reads the repos; it writes `.cairn/` in that folder.
   - Run `cairn init <folder>` and report the summary line it prints, then continue from step 1 in that folder.
1. Run `cairn status`.
2. For each repo under "Repos without an authored summary" or "Possibly stale summaries":
   - Read `.cairn/cards/<repo>.md`, then the repo's README if needed (stop after ~200 lines).
     The card's first line may start with cairn's draft (what kind of repo it is, from what cairn
     detected): keep what's right, fix what isn't.
   - Write one or two plain sentences: what the repo does and who or what uses it.
   - Save: `cairn set-summary <repo> "<summary>"`. Add `--alias <name>` for names people really use.
3. For each line under "Unconfirmed links":
   - Read the evidence files listed for that link in `.cairn/workspace.json`.
   - Decide, then run `cairn annotate-edge <key> --confirm` or `--reject`, adding `--why "<one line>"`.
4. Run `cairn status` again and report what changed in two or three lines.

Never edit `.cairn/workspace.json`, cards, or INDEX.md by hand; they are regenerated on every scan.
