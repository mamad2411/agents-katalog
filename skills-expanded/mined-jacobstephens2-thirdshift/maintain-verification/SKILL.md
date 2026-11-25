---
name: maintain-verification-skill
description: "Audit and resync a project-local verification skill and its feature map against current code and live behavior."
disable-model-invocation: true
---

# Maintain a verification skill

Imported from [Cursor pstack](https://github.com/cursor/plugins/blob/eb4db2b55b2b7dec3d9282754cddf0a56bf4ff10/pstack/skills/maintain-verification-skill/SKILL.md)
at `eb4db2b55b2b7dec3d9282754cddf0a56bf4ff10`; [MIT license](LICENSE).
Local adaptation: target project-local `.agents/skills/verify-*/` skills with feature maps
(separate from Factory `skills/`), enforce `verify-ui` (Factory: `thirdshift-verify-ui`) isolation,
`trap ... EXIT` cleanup, conditional `verify-env`, and **Visual evidence** checks, and edit using `/writing-for-agents`.

A feature map rots the moment routes or setup change. Audit every mapped feature against source and drive every feature live to keep the skill trustworthy.

## Outcomes

Report one outcome:

- **clean:** every feature passed source and live checks; no changes needed.
- **changed:** one PR ships proven doc, helper, or feature-map corrections.
- **blocked:** coverage could not finish or a proven correction could not ship safely; state the exact blocker.

## Edit scope

Edit only the target `verify-<app>/` directory (`SKILL.md`, `features/`, and its helper scripts). Leave product code and Factory `skills/` untouched; report broken app behavior as a product gap rather than papering over it in the map.

## Pass

0. **Locate the target.** Find the project-local skill with `Launch`/`Drive` sections and `features/` under `.agents/skills/verify-*/` (or `.claude/skills/verify-*/`). Ask when several match; stop and point at `/create-verification-skill` when none exists.

1. **Index hygiene.** Compare `features/README.md` against sibling files in `features/`; repair missing, extra, duplicate, or dead links.

2. **Source wave.** Launch one read-only subagent per feature file concurrently. Each reads current source, explains the user-facing behavior, flags doc/selector drift with citations, and returns one concise live recipe (`feature summary / source entry points / likely drift or none / one recipe`). Subagents read only and make no edits.

3. **Reconcile.** Merge overlapping live recipes into minimal app states, spot-check cited drift, and sweep recent commits for unmapped user-facing routes or controls (citing concrete source paths for any gap).

4. **Live pass.** Exercise every mapped feature live inside isolated `( ... )` subshells following `verify-ui` / `thirdshift-verify-ui` isolation (single `trap ... EXIT` cleanup, OS-assigned ephemeral ports, isolated `mktemp -d` state, sourcing `~/.config/thirdshift/verify-env/<owner>/<repo>.env` only when the documented setup requires host credentials and leaving Launch-directory `.env` untouched). Hold four invariants throughout:
   - **Doctor before driving:** run `Doctor` before the first drive, on each fresh session, and after any failed drive; reset state or relaunch on wedged UI state.
   - **Evidence survives cleanup:** write `.png` and H.264 (`yuv420p`, `+faststart`, `<= 8 MB`) `.mp4` proof captures with `mktemp` outside the cleaned state directory (per `verify-ui` / `thirdshift-verify-ui`) and confirm readability/playback after teardown.
   - **Zero leaked processes:** stop and wait for tracked server PIDs/process groups and browser contexts/daemons on success, failure, and interruption; confirm zero server or browser children remain.
   - **Strict skip reporting:** mark a path `verified-unreachable` only with its attempted route and unmet prerequisite (adding missing prerequisites to `Gotchas` as doc drift).

   Fix `Doctor` or harness drift under edit scope and re-drive every repaired path live before finishing.

5. **Triage.** Fix stale user-POV descriptions or `Gotchas` (`doc drift`), fix broken selectors or executable helpers documented in `SKILL.md` (`harness gap`), and report broken app behavior separately (`product gap`).

6. **Ship or stop.** For `changed`, re-read every modified file and open one PR of proven updates; for `clean` or `blocked`, open no PR and report coverage, outcomes, and scratch notes (kept out of git).
