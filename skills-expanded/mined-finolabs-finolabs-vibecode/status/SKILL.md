---
name: status
description: Open the finolabs-vibecode usage dashboard, a local page with how often the router and skills fired, what they cost to load, and how delegated runs and reviews went. Refreshes its numbers from the usage events and the dispatch ledger first, and lists dispatches still open. Run only when the user asks for it, or to delete the recorded usage data.
argument-hint: "[purge]"
disable-model-invocation: true
---

# Usage dashboard

The dashboard is a static page, `dashboard.html`, in the resolved data root's `state/` folder. An absolute `FNL_STATE_DIR` remains a dashboard/events override; before relocation, an existing `${XDG_STATE_HOME:-~/.local/state}/finolabs-vibecode` is used while the default state folder is absent. It loads its numbers from a `data.js` beside it and its code from the shipped local `dashboard.js`; refresh copies both page assets. This skill never writes or edits the page; a script rebuilds the data and copies the shipped page.

The page has two title-bar tabs, `overview` and `now`: [references/dashboard.md](references/dashboard.md) "Page" says what each shows.

The scripts are in this skill's base directory: `scripts/refresh.py` builds the dashboard data, and the `delegate` skill beside this one holds `scripts/ledger.py`. Without `delegate`, the dashboard still shows the usage events and names the ledger as a missing source.

**Arguments:** $ARGUMENTS

## Steps

1. Run `python3 -I <refresh.py> run --open --register-here`. With recorded metrics consent, this names the repository locally using its folder name; hook refreshes never name repositories. It rebuilds `data.js`, copies the page and opens it in the default browser. Done when it prints its one-line summary. While its tab is visible the page reloads `data.js` every 5 seconds, and the hooks rebuild it during a session, so the user can leave it open.
2. Scope the answer to the repository you run in: report only what concerns it, and leave other repositories' sessions, dispatches, projects and totals out of your reply (the page lists them and the user opens it for those; say so in one line, with the page path from the output). From the output line, relay its status and name each missing source it lists and what fixes it: consent not given means `setup`; no events means the plugin's hooks need the whole plugin installed and a session started after consent; a missing ledger means `delegate` "Ledger".
3. Run `python3 -I <ledger.py> open --project <this repository's ledger project>`, which is its `ledger` value in the repository's own settings file when one is set, else, only when the settings were never configured, the repository's folder name (agent judgment; the script enforces only the exact-name filter). When the project settings need setup again (the session line or the page shows the ledger join unknown), stop at that unknown join: never guess the folder name, report it and point to `setup`.
   It prints each of this repository's open dispatches with its age against its budget (an empty list while the ledger holds other open dispatches may only mean the project name does not match: check the name and the page before saying nothing is open, agent judgment); without `--project` it lists every repository's, which this step must not report, and the same `running` block of the generated `data.js` (the `now` tab) holds the same dispatches, with the fields [references/open-runs.md](references/open-runs.md) "Running block" lists. If the ledger is missing, report that source.
   For each run past its check deadline, check artifacts as `delegate` "Budget and liveness" says and report **running**, **stalled** or **ended without a finish line**; these verdicts are advisory (agent judgment), not inferred from process names. A coordinator closes a record only when its log or the repository shows how the run ended, with that outcome and a note that it was closed late; otherwise list it and ask the user.
   Then run `python3 -I <ledger.py> stale` on every status run, whatever `open` showed. When it lists records, follow [references/open-runs.md](references/open-runs.md) "Stale records". When it lists none, say nothing about it.
4. Read the `Review by` date (ISO, `YYYY-MM-DD`) at the top of `references/models.md` in the `delegate` folder. When today is past it, the capability map is stale: say so, with the date, since routing still reads it.

## Purge

Questions below ask through the host's native question tool when the session has one. Ask in text when the session has no such tool, the tool is refused or fails, nobody can answer (a delegated or headless run records the open decision and never assumes or invents an answer), or the decision is free text. The enforcer is agent judgment, so this is advisory.

**Advisory (agent judgment):** Talk to the user in the language they are using, including questions and option labels; keep command names, flags, file paths, skill names and other technical names unchanged. Script output stays English; report it to the user in their language (advisory, agent judgment).

When the argument is `purge`, skip the steps above and ask the user through the host's native question tool when the session has one to confirm deleting the recorded events, `data.js`, `dashboard.html`, `dashboard.js` and registered names in `projects.json`. Offer neutral Yes and No choices with none preselected or marked recommended; a default, a timeout or an auto-selected option never counts as the yes. Only after a clear yes, run `python3 -I <refresh.py> purge --yes`, and report how many files it removed. Never run it unasked.

Host config stays unchanged, including project settings and labels; the purge script does not delete it. Their consent record stays, so recording continues; to stop it as well, ask separately whether to withdraw consent, through the host's native question tool when the session has one. Offer neutral Yes and No choices with none preselected or marked recommended; a default, a timeout or an auto-selected option never counts as the yes. Only after a second yes run `python3 -I <refresh.py> consent --revoke --yes` (or the user sets `FNL_METRICS=off`).

## What is recorded

Only when the user consented in `setup`: the plugin's hooks append metadata to `events-YYYY-MM.jsonl` in the state folder (a time, a session id, a short repository code, a skill or agent name, a depth, a review verdict, a kept-task count with its reason and who settled it, judge receipt site, grader, result and followed status), never prompts, code, command text or file paths. Nothing is sent anywhere.

The process snapshot has a separate setup consent, off by default. It keeps only fixed family names, counts, elapsed seconds and its time in the overwritten `data.js`, never in events; `FNL_AGENT_SNAPSHOT=off` disables it. It is machine-wide for the current user, shows the agent family only (the model of a dispatch is on its lane, taken from the ledger), cannot identify sub-agents or list desktop app sessions, and makes no repository attribution.

The Now project pane and its work records, the `running.live` and `running.quota` blocks and the rest of project progress are described in [references/dashboard.md](references/dashboard.md).

Project progress is on by default with metrics consent and a safely resolved host config. `Project progress: off` under `## Project progress` in canonical host config, or `FNL_PROGRESS=off`, disables it; missing or ambiguous config is off.
