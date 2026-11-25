---
name: setup-hosting
description: Set up or check how the tool runs live, including moving it to another host or recipe. Record whether merges deploy automatically or need a manual deploy; this skill never merges code. Run the evidence run and the review first, and record any risk area's caution.
---

# Setup hosting

The first run puts `main` live and records whether later merges deploy
automatically or need a manual deploy. A later run compares the live copy with
`main` and repairs differences.

## Before acting

Read the risk record in the masterplan. If a `Recheck when` item occurred since
`Last checked`, run `fit-check` first. For each risk area, say whether its
caution is done, accepted or not yet done. Run the risk-area check and
stop if it disagrees.

Read the `Recipe:` line in AGENTS.md's stack section and the matching folder's
`recipe.md`, not `PROVEN.md`. An old `.md` recipe name means its folder.
`Recipe: none`, a missing line or folder means no recipe. The recipe launch
checks do not apply; follow "On no recipe" below for help by hand. If a live
address is recorded, follow
`references/later-run.md`. Leave open pull requests open; say `/implement`
merges one after approval, then explain deployment using the recorded
`Deploys on merge:` answer or the recipe's automatic deployment procedure.
The Python document-worker and read-only existing-database recipe parts are
not offered yet. The recipes' `Fits:` lines describe tool shapes, not those
unavailable parts.

## Launch

Load `references/build-run.md`.

### On a recipe

Follow `recipe.md` in order, run its action scripts from the project root and
follow any hosting request it names. Then load `references/recipe-launch.md`.

### On no recipe

Load `references/recipe-launch.md`: one notice, the choice recorded, no
refusal. Then help by hand. For a server this session cannot reach, use
`references/hosting-request.md`.

For a risk area, follow `fit-check`'s "Rechecks and going live".

Before any live change, load `references/live-records.md`.

Connect one service at a time, starting with harmless parts. Print the hosting
request's address and setting names when its instructions require them, never
secret values. Give the live-change warning before asking
the person to go live.

When going live changes the risk record or names a risk area, record why,
its caution and which work continues or waits.

## Done when

The address is recorded, each check has its line, warnings and gaps are in one
dated changelog entry, and no code was merged.
