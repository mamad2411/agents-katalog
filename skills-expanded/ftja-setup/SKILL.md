---
name: ftja-setup
description: One-time (but re-invocable) onboarding for FTJA — interviews the user and creates local rubric.md + criteria.json. Invoke when rubric.md/criteria.json don't exist yet, or when the user asks to "set up again" / "reset rubric" / "redo onboarding".
---

# FTJA setup

## Resume from the protocol

Once FTJA and its environment are installed, at the start of every onboarding turn run `venv/bin/python -m
ftja.onboarding . next`. Follow its `next_action`, and read the returned
state instead of reconstructing progress from the chat. The same directive
is returned after draft saves and confirmed waits. All decisions in the
summary → search → filter sequence belong in the viewer.

For `draft_search_settings`, propose recent roles and close equivalents
from the confirmed resume, plus role phrases for keywords. Missing product
names do not require a question: use the work and frameworks described in
the resume. These are editable proposals, never confirmed preferences.
If essential information has no defensible draft, run
`venv/bin/python -m ftja.onboarding . ask-search --question "..."`, then
`venv/bin/python -m ftja.onboarding . wait-for-action --type answer_search_question --timeout 900`.
The viewer presents the question. Resume drafting using `search_answers`
from the returned state. Never ask these questions in chat or leave the
viewer showing a working spinner while waiting for a chat answer.

Interview the user conversationally (not a rigid form — follow up, don't
just fire a checklist) to produce two files at the project root. Do not
guess at confirmed preferences. Draft search settings and filters from the
resume for the user to edit and confirm in the viewer. Request essential
missing information through the viewer's `ask-search` protocol.

This is the Codex copy of the skill. Codex has no folder connector and no
browser pane, so this copy never calls `mcp__…` tools: it works on the
FTJA folder's absolute path and opens the viewer in the user's own
browser.

This runs in two turns. Turn 1 installs FTJA in a folder and opens the web
view, then stops and asks one question. Turn 2 (triggered by the user's
reply) creates the native checklist and drives the actual interview. Do
not collapse these into one turn — see "Why two turns" below.

**First, the platform.** Read `windows.md` (Windows) or `mac.md` (macOS),
next to this file, before running any command, and follow it in every
step. The commands below are the macOS forms; on Windows use the forms
`windows.md` gives.

**Approval mode.** These commands can run outside the sandbox only when
the session's approval mode allows it ("Approve for me" in the Codex
app). In "Ask for approval" mode Codex rejects any request to leave the
sandbox without asking (`approval_policy` granular with
`sandbox_approval: false`), and fetching into `.git` fails even with extra
permissions. If a request to run outside the sandbox is rejected that
way, stop and tell the user to switch the mode under the message box to
"Approve for me" and send their request again.

**Codex sandbox.** Codex's default sandbox (`workspace-write`) has no
network, and does not let a sandboxed command write the folder's `.git`
or `.agents`. So these commands need to run outside the sandbox: `git
clone`/`fetch`/`pull`, `pip install`, the scrape, and starting the
viewer. Request that (escalated permissions, with a one-line reason)
on the first try for exactly these commands, instead of trying them in
the sandbox first and working around the failure. Never fetch a file
through the browser, a web tool or `Invoke-WebRequest` to get round a
refused command: everything this skill needs is in the repository.

**Long commands — keep waiting until they exit.** The `wait-for-action
... --timeout 900` commands below block until the user clicks in the
viewer, and the click only reaches you through that command's exit. In
Codex, `exec_command` hands back a `session_id` after `yield_time_ms` while
the command is still running. That is not the result: do not end your
turn there. Start the wait with a long `yield_time_ms` (300000), and while
it is still running keep calling `write_stdin` on that `session_id` with
empty `chars` and `yield_time_ms` 300000 until it prints its JSON and
exits. Ending the turn while it runs leaves the viewer spinning with
nobody to answer it (a live test stopped exactly there after the user
confirmed their files). The same holds for `ftja.run_bridge wait` and
every other wait or long command in these skills.

## Turn 1: install and open the web view

Do this without asking the user anything mid-way (except to install Git or
Python, as the platform file says, or to approve a command as above), then
end the turn with exactly one question. Do not create the checklist or
start any `wait-for-action` call in this turn.

1. Find or install FTJA in this chat's project folder (`pwd`). In Codex
   FTJA lives in a **project**: the user creates a project for it (a
   folder, e.g. `FTJA`) and starts this chat inside it, so that later
   chats in that project are already in the FTJA folder. Codex cannot
   create a project or move a running chat into one; only the user can.
   - `pwd` is an FTJA install (it has `ftja/server.py` and
     `.agents/skills/ftja-setup/SKILL.md`): use it.
   - `pwd` is a chat without a project: a folder the Codex app made
     under `Documents/Codex/<date>/` (Windows: `Documents\Codex\<date>\`).
     Do not install there. Stop and tell the user: in the ChatGPT desktop app, switch to Codex
     (click ChatGPT at the top left) and start a new chat;
     above the message box click **Choose project** → **New project**,
     name it `FTJA`, click **Create project**, then **Trust folder**; and
     paste the same request in that chat.
   - `pwd` is inside another Git repository with history (`git
     rev-parse HEAD` succeeds and it is not FTJA): stop and ask for a
     project folder of its own. Never install into another project. A
     repository with no commits yet (Codex may `git init` a new project
     folder) counts as empty.
   - Otherwise install into `pwd` itself, not a subfolder. `git clone`
     refuses a folder that is not empty, so fetch into it (`<branch>` is
     the one the user named, `main` otherwise; Git first, as the platform
     file says; run these outside the sandbox — they need the network and
     write `.git`):

     ```
     git init
     git remote add origin <url>
     git fetch origin <branch>
     git checkout -B <branch> --track origin/<branch>
     ```

     (`git remote add` fails harmlessly when `origin` is already there;
     use `git remote set-url origin <url>` then.)

   From here on run every command in this folder.
2. Create the repository's Python environment (`venv`) and install
   dependencies if they don't already exist, with the Python the platform
   file finds (3.10 or newer).
3. Initialize or resume `onboarding-state.json` in the FTJA folder.
4. First check whose viewer holds port 8765, even when one answers:
   `curl -s --max-time 3 http://127.0.0.1:8765/api/version` (every FTJA
   folder uses this one port, so an answering viewer may be another
   folder's). If it names this FTJA folder as `project_dir`, use it. If it
   names another folder (or has no `project_dir`), it is that folder's
   viewer: do not use it and do not open it. Tell the user which folder's
   viewer is running and ask before stopping it — don't silently kill
   another workspace's server; after a yes, stop it (`lsof
   -tiTCP:8765 -sTCP:LISTEN | xargs kill`) and start this folder's. If
   nothing answers, start this folder's. Start the server in Codex as a long-running command, not a
   detached one: run `venv/bin/python -m ftja.server --port 8765`
   (Windows: `venv\Scripts\python -m ftja.server --port 8765`) with
   `exec_command` and a short `yield_time_ms`, outside the sandbox (it
   serves a local port), and leave that command session running — do not
   stop it, and do not use `nohup`/`Start-Process` instead of it: on
   Windows the sandbox stops children of a command once that command
   exits, so a detached server dies. Then check `/api/ping` (3-second
   limit, a few tries over about 10 seconds).
5. Open the viewer in the user's browser: `open http://127.0.0.1:8765/`
   (Windows: `Start-Process http://127.0.0.1:8765/`). Then confirm it
   serves the page: `curl -s --max-time 3 http://127.0.0.1:8765/` returns
   the FTJA page. Do not describe the viewer as open until this
   navigation/page-text check succeeds. Always give the user the address
   `http://127.0.0.1:8765/` too, in case no browser window came up.
6. End the turn by asking exactly one question, e.g.: "FTJA is installed
   in this project (<path>) — next time, start a new chat in the FTJA
   project to run it. I've opened the web view in your browser
   (http://127.0.0.1:8765/) — ready to start onboarding?" Say nothing about background files, checklists, or next
   steps yet; that all belongs to turn 2.

### Why two turns

The user needs to see the web view before the interview starts, and the
interview's first step blocks on a click there. Ending turn 1 with one
question gives them that moment. Do not add a workaround (a background
`sleep` command, an immediate self-recheck) to skip the turn boundary.

### Move quickly through routine steps

A full onboarding pass is mostly the user reading a card, deciding, and
clicking — that time is theirs and isn't something to optimize. But a live
run of this skill has taken 20+ minutes on stretches with nothing for the
user to look at, and the cause was this skill routing simple, one-shot
steps through several extra tool calls each:

- Retrying a failed tool call more than once or two before trying a
  genuinely different approach. If a call is refused or errors, don't loop
  on the identical call. Start the server with the platform file's one
  command, which returns at once, and check it with a time limit; a
  server-start command left waiting in the foreground, or a check without
  a limit, has been the site of long, silent stalls in this step.
- Re-verifying something right after writing it to
  `onboarding-state.json`. The web's poll-and-render loop is exercised by
  this project's own test suite; once you've confirmed the state file has
  what you meant to write, the browser will render it.
- Multiple small exploratory commands (checking if a port is free, whether
  a process exists, whether a file exists) where one targeted command would
  do. Prefer the one-shot commands this skill already gives you over
  rediscovering them by hand.

## Turn 2 onward: the native checklist

### Client-native task list

- In Codex, use `update_plan` with `pending`, `in_progress`, and `completed`
  statuses. Its contract permits at most one `in_progress` item. If
  `update_plan` is unavailable, say so once and keep the list as a short
  numbered list in your messages instead.
- Do not enter Plan Mode, `/plan`, or a collaboration Plan Mode for this
  workflow. The native checklist is an execution-progress mechanism, not a
  planning mode.

Create these 8 items, in this order. Each is something the *user* does or
reviews — the infrastructure (clone, connect, server, browser) is
already done and does not belong on this list:

1. `Add your background files`
2. `Review your profile summary`
3. `Review your search settings`
4. `Review the code-based filter`
5. `Answer three questions about your ideal role`
6. `Confirm your judgment rubric`
7. `Run your first job search`
8. `Review your first results`

Keep exactly one item `in_progress` at a time. A command invocation alone
cannot complete a checklist item; complete one only after its required
evidence is observed (see "Evidence and checklist advancement" below). The
checklist mirrors durable `onboarding-state.json` and observed client or
browser results; it never replaces that state machine or hides completed
work. Item 5 covers three sequential sub-answers (clear yes, dealbreakers,
preferences) — keep it `in_progress` across all three; it completes only
once the third is confirmed.

### Narrate long operations

Between two `wait-for-action` calls — writing `profile/summary.md`,
deriving titles/keywords, drafting the rubric — the web has nothing to show
and would otherwise look stuck or disconnected. Before starting one of
these, run:

```bash
venv/bin/python -m ftja.onboarding . status working "Writing your profile summary from your files"
```

The web shows this label with a spinner, and the matching checklist item
does the same, instead of a plain "connecting" notice. Write a short,
specific label for what you're actually doing right now (not a generic
"working..."). The next `wait-for-action` call automatically clears this
and marks the bridge listening again — no separate "stop working" call is
needed in the normal flow.

### Evidence and checklist advancement

- For `confirm_profile_sources`, `confirm_profile_summary`, `confirm_profile`,
  `confirm_stage0`, each ordered `answer_rubric_question` (`clear_yes`, then
  `dealbreakers`, then `preferences`), and `confirm_rubric`: advance only after
  `wait-for-action` returns `status: confirmed`, then read the returned action
  and the full durable state. The three rubric answers must remain strictly
  ordered. Build or mark drafts only after their preceding confirmation.
- Do not mark `Run your first job search` complete because `/ftja-run` was
  merely suggested — it needs a real completed run. Do not mark `Review your
  first results` complete until that run has an observable result surface or
  run artifact; a valid empty result must be verified and explained, never
  fabricated.

### Routine chat copy

The native checklist carries progress. Normal successful chat output is one or
two short sentences: state only what was just verified when useful and the
single next user action (or that no action is needed yet). Keep recovery and
timeout detail only in failure messages. Do not repeat the whole checklist or
web-card fields in ordinary prose.

## File-driven onboarding contract

The local web onboarding is a viewer and decision surface, not a wizard. Never
advance it with a `Next` button and never ask the user to repeat structured
answers in chat. The setup chat is the driver; it writes the local files and
`onboarding-state.json`, while the browser polls that state and shows only the
current stage.

Use the repository helper for every transition:

```bash
venv/bin/python -m ftja.onboarding . init
venv/bin/python -m ftja.onboarding . message agent "..."
venv/bin/python -m ftja.onboarding . set-state --stage profile --phase profile_summary --status waiting --json '{"profile":{"summary":"...","sources":[...]}}'
```

The web sends decisions to `POST /api/onboarding-action`. The server is the
onboarding state machine: it validates the current stage and revision, rejects
stale or out-of-order actions, writes the next `onboarding-state.json` state
atomically, and records every web action in `onboarding-action.json`. The action
types are `set_profile_sources`, `confirm_profile_sources`,
`set_profile_summary`, `confirm_profile_summary`, `set_profile_draft`,
`confirm_profile`, `set_stage0_draft`, `confirm_stage0`,
`answer_rubric_question`, and `confirm_rubric`. The agent/LLM may produce drafts,
but it must not choose the next stage or promote unconfirmed data into active
configuration.


The only onboarding order is:

1. **Profile** — wait for the resume file (portfolio and folder sources are
   switched off in the viewer during the beta), write a concise
   `profile/summary.md`, get an explicit profile-summary confirmation, then
   propose editable job titles. Propose location from
   the user's country as a starting point, but use **Europe** in the public
   example; propose non-remote and postings from the past 24 hours as defaults.
   Do not save these defaults until the user confirms them in the web card.
2. **Rubric** — propose keywords, readable languages, and exclude words for
   Stage 0. After confirmation, the web asks exactly one judgment question at a
   time (clear yes, dealbreakers, then preferences). Wait for each answer before
   proceeding. The web then shows the rubric as one line per criterion, built from the
   three answers by code (each "clear yes" line is its own pass criterion —
   a job passes on any one), for a final confirmation; do not write or
   rewrite that list yourself, and do not show separate Stage 1 or Stage 2
   confirmation cards.
3. **Run** — after the rubric is confirmed the web opens the Pipeline tab with
   a banner asking for one last review of everything on it. Your last chat
   message must say the same, in one or two sentences: setup is finished, and
   once they have reviewed the Pipeline tab they should type `/ftja-run` in
   this FTJA-connected session to start the first run. The existing
   Results/Pipeline surfaces remain the source of truth and update from local
   files.
4. **Learn** — record apply/skip decisions and reasons in Results. On a later
   interactive run, propose rubric changes for approval; never silently apply
   them.

A stage is complete only after the corresponding local action has been read and
its next state has been written. The browser must be safe to reload: it should
resume from `onboarding-state.json`, not localStorage or a guessed step.

## Web-driven profile sources

The web view is the only source-material input surface. Never use
a question tool (`AskUserQuestion`, `request_user_input`) to ask where a resume or portfolio lives, and never ask
for an absolute source path in chat. In this same turn, write the
source-material instruction as your response text, then immediately run the
blocking `wait-for-action --type confirm_profile_sources` command below —
don't end the turn or ask the user to click before that command is running.
The web card's recovery phrase is a fallback for a delayed turn, not the
normal startup path. If a user message arrives saying they already acted,
run the same wait command immediately anyway; it recovers the most recent
valid action from the connected state instead of asking them to click again.

```bash
venv/bin/python -m ftja.onboarding . wait-for-action --type confirm_profile_sources --timeout 900
```

Do not continue the profile interview, write a summary, or ask another source
question until that command returns `status: confirmed`. When it returns, read
every path from `onboarding-state.json` and continue in this same setup session.
If it returns `status: timeout`, tell the user to type `I uploaded my background
files, continue the setup` in the FTJA setup chat and then resume from the state
file. If the user adds more sources before confirming, re-read the full source
list before writing `profile/summary.md`.

Read every path from `onboarding-state.json`, then inspect/copy the selected
sources into the gitignored `profile/` folder as needed. This folder is a
private local cache and derived workspace for repeatable daily runs; it is
not an upload, public snapshot, or Git commit. Do not require a
resume/portfolio label: the UI uses the selected file or folder name.

Mark bridge status `working` before reading and summarizing the files (see
"Narrate long operations"), then write `profile/summary.md`. The web must
then show the summary for an explicit `Confirm profile summary` decision.
Hand the viewer the file's exact text — its headings, paragraphs and
lists, line breaks included — never a one-line retyping of it: the viewer
renders the summary as Markdown, and a summary flattened into one line
shows as a single block of text. Build the JSON from the file instead of
typing it:

```bash
venv/bin/python -c "import json; s=open('profile/summary.md',encoding='utf-8').read(); json.dump({'profile':{'summary':s}},open('.ftja-run/summary-state.json','w',encoding='utf-8'))"
venv/bin/python -m ftja.onboarding . set-state --stage profile --phase profile_summary --status waiting --json-file .ftja-run/summary-state.json
```
Send a short review instruction as your response text, then wait:

```bash
venv/bin/python -m ftja.onboarding . wait-for-action --type confirm_profile_summary --timeout 900
```

Only after that action returns `status: confirmed`, read the confirmed profile
summary and create **one structured proposal covering both upcoming deterministic
screens**:

1. scraping/search settings: titles, location, published-within, and results
   wanted;
2. Stage 0: matching keywords, readable languages, and hard-exclude words.

Do not show either screen until this combined proposal has been written to
`onboarding-state.json`. This is a required protocol step, not optional LLM
judgment. The LLM may derive candidate values from the profile, but the state
machine validates their JSON shape and rejects missing required fields. Never
write empty title, keyword, or language arrays, `...` placeholders, or generic
blank defaults.

Use profile evidence: target roles become search titles; the candidate's base
location becomes the initial location; target roles and product/AI work become
matching keywords; languages the candidate can actually read become ISO 639-1
language filters; explicit dealbreakers or clearly non-target work become
exclude words. Excludes may be empty only when the profile provides no defensible
negative signal. Do not invent unsupported values merely to satisfy validation.

When the profile does not say which roles the user wants next, do not stop
to ask in the chat: the web keeps showing "Deriving suggested job titles"
and the user does not know to look at the chat. Propose what the resume
itself supports — their recent role titles and the closest names for the
same work — and say in one sentence that these come from their past roles
and that they can change them on the card. The card is where titles are
corrected; nothing is saved until they confirm it. Only when the profile
names no role at all, use `ask-search` and wait for `answer_search_question`
in the viewer, as specified in “Resume from the protocol”.

Write the complete combined proposal in a single command **before** instructing
the user to review search settings:

```bash
venv/bin/python -m ftja.onboarding . set-state --stage profile --phase title_proposal --status waiting --json '{"profile":{"titles":["Product Builder","AI Product Manager","Founding Product Manager"],"criteria":{"search_terms":["Product Builder","AI Product Manager","Founding Product Manager"],"location":"France","hours_old":24,"keywords":{"tier1":["AI product","LLM","Product Builder","produit IA","chef de produit IA"],"tier1_language":{"AI product":"en","Product Builder":"en","produit IA":"fr","chef de produit IA":"fr"}},"languages":["en","fr"],"exclude_keywords":["pure sales"]}},"cards":{"stage0":{"keywords":["AI product","LLM","Product Builder","produit IA","chef de produit IA"],"keyword_language":{"AI product":"en","Product Builder":"en","produit IA":"fr","chef de produit IA":"fr"},"languages":["en","fr"],"exclude_keywords":["pure sales"]}}}'
```

The `set-state` helper records drafts only. It must leave the state at
`profile/title_proposal`; it must never call `confirm_profile` or move to Stage 0.
Verify all of the following by reading `onboarding-state.json` back (do not
open the browser to check — the web polls and renders that same file, and a
separate navigate/screenshot here is a slow, redundant round trip, not extra
safety; see "Move quickly through routine steps"):

- state is still `profile/title_proposal`;
- the search-settings card contains the proposed titles and location;
- `cards.stage0` already contains non-empty keywords and languages, with
  keywords in every one of those languages and `keyword_language` saying
  which language each is in.

Tell the user both upcoming screens were prefilled from the confirmed profile and
remain editable. Then wait for `confirm_profile`. When it returns, the state
machine must transition to `rubric/stage0` while preserving the already-populated
`cards.stage0`; confirm that in the returned state, not by reopening the browser.
Never insert a blank intermediate Stage 0 state.

Before each card, write the instruction as your response text, then run only
the matching command:

```bash
venv/bin/python -m ftja.onboarding . wait-for-action --type confirm_profile --timeout 900
venv/bin/python -m ftja.onboarding . wait-for-action --type confirm_stage0 --type request_stage0_keywords --timeout 900
venv/bin/python -m ftja.onboarding . wait-for-action --type answer_rubric_question --timeout 900
venv/bin/python -m ftja.onboarding . wait-for-action --type confirm_rubric --timeout 900
```

**The filter card can ask you for keywords.** On the code-based filter
card the user can add a language they read and press "Add <language>
keywords with my agent" (or type "add <language> keywords to the filter"
in the chat). The wait then returns `request_stage0_keywords` with
`action.language`. Do not treat it as a confirmation:

1. Read `cards.stage0` from `onboarding-state.json`: it holds the card as
   the user has it now (`keywords`, `keyword_language`, `languages`).
2. Write the keywords a posting **in that language** would use for the
   same things the existing keywords catch. Do not translate word for
   word; give the terms postings in that language really use, list the
   word forms yourself (singular and plural, masculine and feminine), skip
   names that are the same in every language, and add no place names.
3. Save the card with the new keywords appended and each of them recorded
   under that language, leaving everything else as it was:

   ```bash
   venv/bin/python -m ftja.onboarding . set-state --stage rubric --phase stage0 --status waiting --json '{"cards":{"stage0":{"keywords":[<all existing>, <the new ones>],"keyword_language":{<existing entries>, "<new keyword>":"<language code>"},"languages":[<as on the card>],"exclude_keywords":[<as on the card>]}}}'
   ```

4. Say in one line what you added, then run the same wait command again.
   The card shows the new keywords by itself.

Use only the command for the card currently shown. The helper watches the
connected project folder and also recovers an action that completed immediately
before the helper started, so a delayed chat turn does not lose a web decision.
There are three sequential `answer_rubric_question` actions; after each one,
re-read the state so the next web question remains the source of truth. After
`status: confirmed`, read the returned `action` and the full
`onboarding-state.json` before writing
the next draft or message. Never assume that a changed web card reached the
setup chat without the helper result. If a later wait times out, tell the user
the matching recovery phrase shown by the web card (for example, `I confirmed
my search settings, continue the setup`) and do not claim that the chat resumed.


## What you need to learn

**For `criteria.json` (Rubric stage, after Profile — Stage 0 deterministic, used by `ftja/scrape.py` and
`ftja/filter_stage0.py`):**
- `search_terms`: list of LinkedIn search strings (e.g. `["Product Manager", "Founding PM"]`)
- `location`, `hours_old` — this is the ONLY place location is
  controlled. There is no remote-only setting: LinkedIn ignores its
  workplace filter for logged-out searches, so a candidate who wants remote
  roles gets them through the **Remote check**, a separate stage they set
  up afterwards on the Pipeline tab (`/ftja-remote`); say so when they
  mention remote work. Do not put remote-work words ("remote", "hybrid",
  "on-site", "télétravail", ...) in `keywords.tier1`: Stage 1 would then
  read benefit and location sentences and judge them against a rubric that
  is about the role. The one exception is a rubric that itself has a
  remote criterion in its Pass or Fail section. Do not write `is_remote`
  to `criteria.json`.
- `locations` (optional list, e.g. `["France", "Germany", "Switzerland"]`):
  for a candidate who wants more than one place. `/ftja-run` then searches
  every search term in every location (3 titles × 3 locations = 9
  searches), so say what that does to the
  length of a run. When `locations` is set it is used instead of
  `location`. The search-settings card takes several: propose every place
  the candidate's profile says they want (`"locations": ["France",
  "Germany"]` in the `criteria` you pass to `set-state`, next to
  `location`), and the user adds or removes them on the card. If the
  candidate mentions more than one region, don't silently scope to just
  the first one they said.
- Titles are the whole search: only postings whose title contains a
  search term are scraped, as a run of whole words in any word form and
  any case. "Product Manager" finds "Senior Product Manager", "AI Product
  Manager" and "Product Managers (m/f/d)", and does not find "Product
  Owner", "Product Marketing Manager", "Head of Product" or "Chef de
  produit". LinkedIn's own search matches by meaning and would return
  those too; FTJA leaves them out. Tell the user this rule in one sentence
  with an example from their own titles, then propose the other names the
  same job goes by for them to pick from: common variants and the title in
  each language they read for the places they search. Each one they keep
  is its own title. There is no cap per search: `/ftja-run` scrapes every
  matching posting of every title, merges them into one list, and only
  then runs the code-based filter and LLM judgment once over the merged
  set. Do not write `results_wanted` or `title_must_match` to
  `criteria.json`.
- `exclude_keywords`: a blunt bare-word exclusion list — if any of these
  words appear ANYWHERE in the JD (title or body), the job is dropped, no
  phrase-matching ("fluent in X", "X required") involved. Propose only
  exclusions supported by explicit profile evidence; otherwise leave this
  list empty. The user can add tools, companies, industries or other words
  on the filter card before confirming.
- `languages`: ISO 639-1 codes (e.g. `["en","fr","ko"]`) of languages the
  candidate can actually work in. A JD whose own text isn't detected as one
  of these gets dropped at Stage 0 (via `langdetect`) even if it never
  explicitly states a language *requirement*. Propose readable languages
  from the resume for correction on the filter card; if none can be
  established, use `ask-search` in the viewer. Stage 0 also drops a JD that plainly requires
  fluency in a language NOT on this list ("Fluent in German and English"),
  so a language requirement does not need an `exclude_keywords` entry — and
  a bare language name there would also drop "the German market".
- `keywords.tier1`: the keyword phrases that must appear in a JD sentence
  for it to even reach Stage 1. Stage 1 reads only the sentences around
  them and judges those against the rubric's Pass and Fail, so every
  keyword has to be a word that shows up where a posting talks about what
  those criteria are about. **Write them in every language in
  `languages`, not only English**: a posting written in French is caught
  only by French keywords, so a candidate who reads English and French
  gets both sets. Do not translate word for word; give the terms postings
  in that language really use, and, since word forms are only folded the
  English way, list the forms yourself (singular and plural, masculine and
  feminine). Record which language each keyword is in as
  `keywords.tier1_language` (`{"prototypage": "fr"}`), and in the Stage 0
  card as `keyword_language`; a name that is the same in every language
  ("LLM", "Cursor") goes under the first. A keyword matches whole words and their
  forms ("remote" matches "remotely", not "premote"; "time zone" matches
  "time zones"), so write full words, never a fragment like "tele". A
  keyword in capitals ("UTC") matches only those capitals. Include the
  words where a FAIL criterion would be stated as well as a pass one (for
  a remote search: "hybrid", "on-site", country names), so Stage 1 is shown
  those sentences. When drafting from the resume, consider both:
  - **Tools and technologies actually supported by the resume**, such as
    Figma, Jira or Python. Do not require this category to be populated.
  - **Concrete work and domain phrases**, such as product discovery,
    prototyping, supplier risk or risk assessment.
  Propose the supported keywords on the editable filter card for the user
  to add, remove and confirm. Do not ask separate tool or work-keyword
  questions. If the resume names no tools, draft from its work and domain
  evidence alone.

**For `rubric.md` (Rubric stage, after Profile — read by the judgment workers):**
- What makes a role a clear yes for them (be specific — role type, seniority,
  what they'd actually be doing day to day)
- Dealbreakers (things that auto-fail regardless of everything else)
- Preferences that matter but aren't dealbreakers (comp range, remote policy,
  company stage, etc.)
- The web source picker is the only way to provide profile sources. It accepts
  one or more files (folders are switched off during the beta) and records
  local paths without uploading contents. Read those paths from `onboarding-state.json`; do not ask for them
  in chat and do not require a resume/portfolio label.

## Write the files

`criteria.json` — structured, machine-read:
```json
{
  "search_terms": ["..."],
  "location": "...",
  "hours_old": 72,
  "exclude_keywords": ["..."],
  "languages": ["en", "fr", "ko"],
  "keywords": {"tier1": ["...", "..."]}
}
```

Search terms are sent to LinkedIn as written, and a posting is scraped
only if its title contains the term that found it (see the search
settings above). Quoting a term changes nothing. A phrase that has to
appear in the posting's text goes in `keywords.tier1`, which Stage 0
checks. Do not write `exact_phrase_search` to `criteria.json`.

`rubric.md` — free-form markdown, written in the user's own words as much as
possible (this is what the Stage 2 subagent reads verbatim — write it as
instructions TO that subagent, e.g. "Pass if..." / "Fail if..." sections),
covering: clear-yes signals, dealbreakers, preferences.

`profile/summary.md` — a condensed distillation of the resume/portfolio you
just read (a few hundred words: role history highlights, key skills/tools,
notable achievements — whatever a judge would need to assess fit). **Not
optional**: Stage 2 reads this file on every job, every day, instead of the
raw resume/portfolio — the first real run measured ~44-86k tokens/call
reading the full files directly, and this is the fix. Write it yourself
from what you already read in `profile/`, don't just copy-paste the raw
files. If the candidate's background changes materially later, this file
should be regenerated (mention that if `/ftja-tune` ever touches profile
info).

After writing all three, do not git-add or commit the user's criteria, rubric, profile, or run data. These files are intentionally gitignored in the public FTJA workspace. If the user wants version history, they can opt into a separate private repository.

Tell the user both `rubric.md`/`criteria.json` are ready to review/edit by
hand if they want, and that `/ftja-run` is the next step (recommend a
manual run first — M1 in SPEC.md — before setting up the launchd schedule).
Once a run produces passed/failed jobs, the same server's Results tab is
where they record apply/skip decisions — see `/ftja-review` for how those
decisions feed back into criteria.json/rubric.md.
