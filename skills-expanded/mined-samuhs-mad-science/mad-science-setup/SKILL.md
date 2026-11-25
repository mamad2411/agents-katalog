---
name: mad-science-setup
description: "Set up a repository for the mad-science data science skills: experiment tracker folder, domain glossary, agent instructions block and .env.example. Run once per repo before the other skills, or when the user says 'set up mad-science' or 'configure this repo for experiments'."
mode: true
icon: crown
color: yellow
---

## Setup Mad Science Skills

1. Explore
Look at the current repo to understand its starting state. Read whatever exists; don't assume:

- git remote -v and .git/config: is this a GitHub repo? Which one?
- AGENTS.md and CLAUDE.md at the repo root: does either exist? Is there already an ## Agent skills section in either?
- GLOSSARY.md and GLOSSARY-MAP.md at the repo root
- Monorepo signals: a pnpm-workspace.yaml, a workspaces field in package.json, or a populated packages/* with its own src/. These are present only in a genuinely large multi-package repo; their absence means single-context, which is almost every repo.

2. Show the Finds and Ask

Summarize what's present and what's missing. Then take the sections in order. One section, one answer, then the next.

#### Section A: 

Experiment tracker: The experiment tracker lives in this repo at docs/experiments-pipeline. 


#### Section B:
Domain docs:  Default to single-context (one GLOSSARY.md at the repo root). This fits almost every repo; write it without asking.

Offer multi-context (a root GLOSSARY-MAP.md pointing to per-context GLOSSARY.md files) only when exploration found monorepo signals. Then confirm which layout they want.


3. Confirm and edit

Show the user a draft of:

- The ## Agent skills block to add to whichever of CLAUDE.md / AGENTS.md is being edited (see step 4 for selection rules)

4. Write
Pick the file to edit:

- If CLAUDE.md exists, edit it.
- Else if AGENTS.md exists, edit it.
- If neither exists, ask the user which one to create; don't pick for them.

Never create AGENTS.md when CLAUDE.md already exists (or vice versa); always edit the one that's already there.

If you create the file, add these rules to it:

- The file must indicate that the `docs/` folder is the main source of truth for the experiments.
- Add a rule to keep this file in sync with the docs folder, updated as experiments are created.
- Create a section in the file with this template:


```
## Docs Indice


### Articles
<article_name_file.md> : <article short description>

### Experiments Docs
<experiments_name_file.md> : <experiment short summary> - 
** Already complete? ** : Answer yes or no. If yes, add the date.


### Experiments Pipeline
<experiments_pipeline_name_file.md> : <experiment pipeline short summary> - 
** Already complete? ** : Answer yes or no. If yes, add the date.

```

5. Optional — Configure "notify human wait"

Ask the user whether they want the repo to notify a human when a **flow skill**
is in progress and the turn waits for human input. Explain briefly what it does
(Google Chat card with the open question + project name). One yes/no.

- If **no**: skip the section, continue.
- If **yes**:
  - Add `GCHAT_WEBHOOK_URL=CHANGE_ME` to `.env.example` (if not present) and tell
    the user to set the real webhook URL in `.env` (never versioned).
  - Add the **"Flow skills — notify human wait"** block to `CLAUDE.md` (or the file
    being edited), listing the flow skills currently in this repo
    (e.g. `let-it-rip`, `literature-research`, `to-article`) plus the rule
    "notify whenever work inside a listed flow skill is waiting for a human
    response". Keep the list maintainable: new flow skills are added here.

6. Done 

Tell the user the setup is complete and which engineering skills will now read from these files.