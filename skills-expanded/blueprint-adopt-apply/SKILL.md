---
name: blueprint-adopt-apply
description: "Set chaff up in the folder: chaff.yaml for the chosen genre, today's findings shelved in .chaff-baseline.json, and, when asked, a GitHub workflow that puts new findings on the pull request's lines."
---

# Set chaff up

The person approved the setup in `.blueprint/adopt.json`. The documents stay exactly as they are: fixing what is
shelved is 「文書を整える」's work, later.

## 1. chaff.yaml

Write the folder's `chaff.yaml` with the genre from `.blueprint/adopt.json` and the documents' `language`
(`npx chaffjs init --genre <genre>` writes a commented one). If the folder already has one, set its `genre` to the
chosen one and **keep every other line it has** — the check refuses any other line of the old file that is gone. Add the rule
levels the person agreed to at the gate, nothing else.

## 2. Shelve today's findings

Run `sh <base pack>/checks/chaff.sh baseline <place> …` with every place. It writes `.chaff-baseline.json` in the
folder: the findings there today are not reported again; new ones are. Tell the person to commit it with
`chaff.yaml`.

## 3. The workflow — only when `ci` is 「GitHub の PR に指摘を出すワークフローを作る」

Copy `<usecase pack>/templates/chaff.yml` to `.github/workflows/chaff.yml`, replacing `{{PATHS}}` with the places
separated by spaces, and change nothing else: the check compares the file with the template filled in that way, line
for line. Its `permissions:` let the workflow read the documents (`contents: read`) and upload findings
(`security-events: write`), nothing more. A place whose name has a space or a character a shell reads (`$`, `;`, `*`,
quotes…) cannot go into the workflow: the interview refuses it, so ask the person to name a folder above it instead. When `ci` is 「作らない」, add nothing under `.github/`.

## 4. The report

Write `.blueprint/adopt-report.md` for the person, in their language and in plain words:

- `## 入れたもの` / `## What was set up` — `chaff.yaml` (the genre, and why), `.chaff-baseline.json`, and the
  workflow `.github/workflows/chaff.yml` when one was made. The check looks for each file's name.
- `## 棚に上げた指摘` / `## Shelved findings` — how many were shelved, by rule, in plain words.
- `## これから` / `## From now on` — only new findings are reported (run `npx chaffjs <places>` by hand, or see them
  on the pull request's lines); how to lower the shelf later (「文書を整える」, then `chaff baseline` again); that
  the workflow needs code scanning enabled on the repository (a public repository has it; a private one needs
  GitHub Advanced Security).

## Done when

`node <usecase pack>/checks/adopt.mjs apply` and then `node <usecase pack>/checks/report.mjs` (with `BLUEPRINT_BASE`
and `BLUEPRINT_USECASE` set) pass.
