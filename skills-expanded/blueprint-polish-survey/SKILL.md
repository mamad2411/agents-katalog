---
name: blueprint-polish-survey
description: "Measure the named documents with chaff and choose which to polish, within the agreed number — changing nothing yet."
---

# Choose what to polish

`.blueprint/answers.json` names the documents (`targets`), the style, how far to go (`scope`), the most
files to polish (`maxFiles`) and what to leave alone (`avoid`). The person may not be an engineer: say
what you do in plain words.

Change nothing in the repository: this step only reads and measures. The person approves the list before
any file is touched.

## Measure

Run chaff through the base pack's wrapper, from the folder: `sh <base pack>/checks/chaff.sh <file>`
(add `--compact` for one line per finding). The folder's `chaff.yaml` applies when the answer `style` is
the folder's style; if it is and there is no `chaff.yaml`, stop and say the style has to be made first. The
folder's style is its `chaff.yaml`: `STYLE.md` is read only when `scope` asks to follow the guide, so when it
does not, a folder without one lacks nothing, and the report does not say it does. When `scope` asks for the
guide and there is no `STYLE.md`, stop and say the guide is missing.
When the answer `shelved` is 「棚上げした指摘も直す」, add `--show-baseline` to every chaff run as well: the findings
the folder's `.chaff-baseline.json` shelved are then measured and polished like any other. With chaff's own style, the answer `kind` says what kind of document this is: measure it as that kind by
adding `--genre <genre>` to every chaff run, taking the genre for the answer from `<usecase pack>/kinds.json`
(a kind whose genre is `null` adds nothing). The checks measure the same way, so a count taken without it
will not match.

For each Markdown or text file under the named paths, count the warnings and errors. Leave out what
`avoid` names.

## Choose

- With `scope` "chaff が指摘した所だけ", or no `scope` at all (it is asked only with this folder's style, so
  chaff's default style has no guide to follow), choose files that have findings, most findings first.
- With `scope` including the guide, a file without findings may still be worth polishing against
  `STYLE.md`; say why for each.
- When the answer `kind` has viewpoints in `<usecase pack>/viewpoints.json`, every named document is worth
  polishing, findings or not: the polish step reads each for its kind. Choose them all, most findings first.
- No more than `maxFiles`. The rest are for another run: name them in the report.

Write `.blueprint/polish.json`:

```json
{ "targets": [{ "file": "docs/setup.md", "before": 7, "status": "todo" }] }
```

`before` is the number of warnings and errors chaff reports for that file now; the check measures it
again and refuses a number that does not match.

**When nothing needs polishing** — every named document has no finding, or has one only in a file `avoid`
asks you to leave alone, and the kind has no viewpoints — that is an answer, not a failure: write an empty list, naming the files left
alone, and do not ask the person how to go on.

```json
{ "targets": [], "avoided": ["notes/draft.md"] }
```

The check measures every Markdown or text file under the named paths again, and refuses an empty list while
one that is not in `avoided` has a finding. `avoided` may hold only files at or under a path the answer `avoid` names;
when `avoid` describes files in words rather than paths, ask the person which files it means.

## Done when

`node <usecase pack>/checks/targets.mjs survey` (with `BLUEPRINT_BASE` and `BLUEPRINT_USECASE` set to the
pack folders from your prompt) passes.
