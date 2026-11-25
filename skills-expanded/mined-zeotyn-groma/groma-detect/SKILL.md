---
name: groma-detect
description: Classifies a folder as greenfield or brownfield with evidence. Use when starting /groma, when asked whether a project is new or existing, or before surveying a repository.
---

# groma-detect

Decide whether the project is **greenfield** (nothing to survey, interview the user) or **brownfield** (existing code to survey). Read-only.

**User language.** Talk to the user in the language of their latest message: questions, summaries, hints, warnings, escalations and the reasons for commands you print. Commands, paths, config keys and ids stay literal. Files you write, the findings report too, keep the language of their templates.

## Steps

1. Run the detector on the project root (path relative to this skill folder):
   ```sh
   sh scripts/detect.sh <project-root>
   ```
   Without a POSIX shell (plain Windows), apply the table in [references/signals.md](references/signals.md) by listing files yourself.
   Done when you have `project_type`, the counts and every `signal=` line.

2. If `.groma/config.yaml` exists and `project_type_override` is `greenfield` or `brownfield`, that value wins. Say so.

3. Report in this shape:
   ```
   Project type: brownfield
   Evidence: source files: .js (JavaScript) x1 · manifest: package.json (Node.js) · 12 commits
   ```
   Then offer the override in one line: "Treat it as greenfield instead?" Record a chosen override as `project_type_override` in `.groma/config.yaml` when that file exists; otherwise hand it to the caller.

## Git practice

For the git questions of the `/groma` interview, run (read-only):
```sh
sh scripts/git-practice.sh <project-root>
```
It prints the main branch, a recommended `integrate` (`rebase`, `merge`, `squash`) and `commits` (`conventional`, `free`) value, each with its evidence from the last 200 commits of the main branch ("28 of 30 merges are pull-request merges", "34 of 40 subjects end in (#n)", "9 of 10 subjects are conventional"), and a `summary` line with the counts. Without commits it prints the defaults with "no history". Show the evidence with the recommendation; the user decides.

## Reading the verdict

- `signal=docs present` on a greenfield project: existing Markdown is input for the interview. Read it before asking questions.
- `unrecognized stack`: still brownfield. Name the extension so the user can confirm the language; it is a candidate row for `references/signals.md`.
- A brownfield verdict that rests only on git history (no source, no manifest) is borderline: ask the user.
