---
name: duolog-calibrate
description: Use only in a project that has .duolog/config.yaml, and only when the person asks for calibration by name; never suggest it. Calibrates duolog routing for this project.
metadata:
  duolog-version: "1.11.1"
---

Stop unless this project has `.duolog/config.yaml`.

# Calibrate duolog for this project

Run this only because the person asked for it. Never start calibration on
your own, never mention it unasked, never raise caps
(`calibration.max_weekly_share`, `calibration.max_window_share`), and never
write AGENTS.md or CLAUDE.md. When several leads are active, pass
`--lead <id>` with the lead id from SessionStart to `run`, `resume` and
`judge`.

Run the steps in order. Show each command's output. Where a step says stop,
end your turn and wait for the person; do not go on by yourself.

1. `duolog calibrate survey`. Show the findings.
2. `duolog calibrate classes`. Show the config diff. **Stop:** the person
   approves or edits. Then run `duolog calibrate classes --apply`, with
   `--skip <name>` for each part the person left out.
3. `duolog calibrate mine`. Show the counts per class and the exclusions.
4. `duolog calibrate plan`. Show the plan as printed. **Stop:** ask for one
   approval of the costed run. On approval, run
   `duolog calibrate plan --approve <hash>` with the hash the plan printed.
5. `duolog calibrate run`. On a pause or stop, report the reason and end
   your turn; the person asks later and you run `duolog calibrate resume`.
   When it says `re-approve`, go back to step 4 and run `plan` again. When
   it stops at `approved cap`, the run part is over: go on to step 6.
6. `duolog calibrate judge`. On a pause or stop, report it and end your
   turn; the person asks later and you run `judge` again. **Stop:** show
   each class batch. Record each of
   the person's answers with `duolog verdict <id> confirm` or
   `duolog verdict <id> correct <criterion>=<o>/<p>`. When the person asks to
   drop a rewritten task, run `duolog calibrate drop <task>`.
7. `duolog calibrate propose`. Show the per-class diff and the project-part
   diff. **Stop:** the person applies the order with `duolog learn --apply`
   (run it only when they say so) and approves the project part; on that
   approval, run `duolog calibrate propose --apply-project`.

`duolog calibrate status` shows where the run is.
