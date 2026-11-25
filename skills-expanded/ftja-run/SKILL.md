---
name: ftja-run
description: Run the daily FTJA job-search pipeline (scrape LinkedIn -> deterministic filter -> cheap-model sentence-block judgment -> mid-model resume/portfolio judgment -> digest + notification). Invoke when the user says "run job search", "run FTJA", "check today's postings", or on the scheduled launchd trigger. Also invoke for "choose my FTJA judge models" (pick the API models to judge with), and for "/ftja-run continue" or "continue to Stage 1 / Stage 2", which takes a run that stopped early through one more stage.
---

# FTJA run

You are executing one pass of the FTJA pipeline defined in `SPEC.md`. Follow
these steps in order. Every python call below uses `venv/bin/python` — if
`venv/` doesn't exist yet, run `python3 -m venv venv && venv/bin/pip install -r requirements.txt` first.

**On Windows**, read every `venv/bin/python` below as `venv\Scripts\python`
(and `venv/bin/pip` as `venv\Scripts\pip`), and run commands in PowerShell. The rules for each system (one shell, time limits, never cutting a command's output short) are in `.agents/skills/ftja-setup/windows.md` and `mac.md`: read the one for this system first.
Create a missing `venv` with `python -m venv venv; venv\Scripts\pip install -r requirements.txt`.
Where a step uses `curl`, `lsof` or `open`, use the Windows form it names.

**This is the Codex copy.** Where the steps below name a Claude Code tool,
do this instead:

- **The `Agent` tool with `model: "haiku"` / `"sonnet"`** (Remote check,
  Stage 1, Stage 2): if this session can start sub-agents, start one with
  the same prompt, the same batching (Stage 2: one job each) and the same
  output file; ask for a small, fast model for the Remote check and Stage
  1. If it cannot, judge each job yourself, one prompt file at a time:
  read `<n>.txt`, follow it exactly as a sub-agent would, and write only
  the JSON it asks for to `<n>.out.json`. The `check-*` commands and
  `finalize` work the same either way.
- **`record-tokens`**: Codex does not hand a sub-agent's tokens back with
  its answer, but writes them to that sub-agent's own session log. After
  each wave of sub-agents finishes, read their total with
  `venv/bin/python -m ftja.codex_tokens <agent id> [<agent id> ...]` (the
  ids `spawn_agent` returned) and pass that number to `record-tokens`.
  If it prints nothing and exits 1, record nothing for that wave: the
  run's total then shows as "-", which is true. When you judged jobs
  yourself (no sub-agents), record nothing either.
- **Long commands** (`wait`, the scrape): `exec_command` hands back a
  `session_id` after `yield_time_ms` while the command still runs; that is
  not its result. Keep calling `write_stdin` on it with empty `chars` and
  `yield_time_ms` 300000 until it exits, and never end your turn while one
  runs: a `wait` that nobody reads loses the user's button press.
- **Sandbox**: Codex's default sandbox has no network and does not let a
  sandboxed command write `.git` or `.agents`. Run `git pull`, `pip
  install`, the scrape and the viewer outside the sandbox (escalated
  permissions, one-line reason) on the first try, rather than failing
  in the sandbox first; never fetch files through a browser or web tool
  to get round a refused command.

**If the user asked to continue a run** ("/ftja-run continue", with or
without a run id and a stage, or "continue to Stage 1 / Stage 2"): do step
0a, then go straight to "Continuing a run that stopped early" at the end
of this file. Do not start a new run.

**Which stages a run does.** A run judges postings in up to three stages,
always in this order: the **Remote check** (`remote`), **Stage 1**
(`stage1`), **Stage 2** (`stage2`). The user switches each on or off on the
Pipeline tab. `ftja.live start` prints the run's `stages`: do the steps
for exactly those, and skip the others. A stage judges what the stage
before it let through. A command for a stage that is not in the list
refuses and says so; that is the guard against spending by mistake, not
something to work around. With the Remote check off (`stages` is
`["stage1", "stage2"]`), a run is exactly what it was before that stage
existed.

## 0a. Reattach the existing workspace and viewer

When `/ftja-run` is invoked in a new Codex session, find the existing
FTJA repository before running anything:

1. The FTJA folder is the session's own folder (`pwd`): check it has
   `ftja/server.py`. If it does not, stop and tell the user to start a
   new chat in their FTJA project (Projects in the Codex sidebar) and run
   this there.
   Do not clone a new copy or choose a similarly named folder.
2. Run every command below in that folder; never run against a scratch
   folder.
3. Make sure the viewer on port 8765 is THIS folder's. Every FTJA clone
   uses the same port, so a viewer that answers may be showing another
   folder's data, and this run would never appear in it.
   `curl -s --max-time 3 http://127.0.0.1:8765/api/version` returns `project_dir`
   (Windows: `Invoke-RestMethod -TimeoutSec 3 http://127.0.0.1:8765/api/version`).
   - It matches the FTJA folder: the viewer is fine, go on.
   - No answer: start it from this folder as a long-running command
     session (`venv/bin/python -m ftja.server` via `exec_command`, short
     `yield_time_ms`, outside the sandbox, left running; not `nohup` or
     `Start-Process`, which the Windows sandbox stops) and verify with
     `curl`.
   - It names another folder, or has no `project_dir` (an older viewer):
     that viewer belongs to a different clone. Stop it (`lsof
     -tiTCP:8765 -sTCP:LISTEN | xargs kill`; Windows: `Stop-Process -Id
     (Get-NetTCPConnection -LocalPort 8765 -State Listen).OwningProcess`),
     start this folder's as above,
     and tell the user in your report that you switched the viewer from
     that folder to this one.
4. On an interactive run, put the viewer in front of the user every time,
   whether you started it or it was already running: on macOS run
   `open http://127.0.0.1:8765` (Windows: `Start-Process
   http://127.0.0.1:8765`), and give the user that address in the chat. The run is watched there; a
   viewer that is running but not on screen shows the user nothing. (On an
   unattended run, open nothing.)

## Keep the user informed (interactive runs)

A run takes minutes, sometimes an hour. The user must never be left
looking at a silent chat wondering whether anything is happening. Say one
short, plain line in the chat at each of these moments, in the user's
language, with the numbers you have:

- **Before scraping**: that the run has started, how many searches it has
  (every search term in every location: 3 terms × 4 locations is 12
  searches), that each search scrapes every posting whose title contains
  its term and ends when LinkedIn's results stop containing it, roughly
  how long that will take (a posting that matches takes about 3 seconds,
  so a search with 100 of them is about 6 minutes; reading LinkedIn's
  results to find them adds up to 10 minutes for a common title, and a
  title with no match ends in about a minute and a half), and that they can watch it at
  `http://127.0.0.1:8765` (Results tab). The number of matches is not
  known beforehand: say so, and that a shorter "Posted within" or fewer
  locations makes a run shorter.
- **After each search**: how many it found and how many searches remain.
  Run the scrape one search per command so you can say this; do not
  chain all of them into one long command that stays silent until the
  end.
- **After Stage 0**: scraped, passed, and the biggest drop reasons.
- **When the Remote check starts and ends** (runs that have it): how many
  jobs in how many batches, then how many passed and failed.
- **When Stage 1 starts and ends**: how many jobs in how many batches, then
  how many passed.
- **When Stage 2 starts and ends**: how many jobs, then pass / review / fail.

Keep each to one line. This is on top of the final report in step 6, not
instead of it.

## 0. Preflight

- **Newer version?** Run `venv/bin/python -m ftja.version check` before
  anything else in this list. It asks GitHub every time (no cached
  answer), prints something and exits 0 even when offline; it never stops
  a run.
  - `up to date`, or it could not check: go on.
  - `update available`, on an **interactive** run: ask the user now, before
    the lock is taken, whether to update first — name both versions, and
    say that it takes about a minute and their own files are not touched.
    - Yes: follow the `ftja-update` skill (`.agents/skills/ftja-update/SKILL.md`)
      from its step 2. If it stops (local changes, a diverged branch),
      report why and ask whether to run on the current version instead.
      When it succeeds, this file may have changed under you: read
      `.agents/skills/ftja-run/SKILL.md` again from disk and start over
      from step 0a with what it says now. Do not ask about updating again.
    - No: go on with the installed version and repeat the `update
      available` line in your final report.
  - `update available`, on an **unattended** run: never update and never
    ask. Go on, and append the line to `run.log` so it is seen later.
  Never update once the run has started.
- Check `rubric.md` and `criteria.json` exist in the project root. If either
  is missing, STOP and tell the user to run `/ftja-setup` first — do not
  improvise a rubric yourself.
- Check the lock: `venv/bin/python -m ftja.lock check .ftja.lock`. If it
  prints `locked` (exit code 1), append one line to `run.log` ("skipped —
  already running") and STOP. Do not proceed.
- Acquire the lock: `venv/bin/python -m ftja.lock acquire .ftja.lock`.
- **Always release the lock before finishing** (`venv/bin/python -m ftja.lock release .ftja.lock`),
  including on any error path. Treat this like a try/finally.
- Count tokens as you go, not at the end: every time a Stage 1 or Stage 2
  `Agent` call returns, run `venv/bin/python -m ftja.live record-tokens
  --dir <run_dir> --tokens <that call's usage.subagent_tokens> --label
  "<stage and batch>"` (the run directory exists once `ftja.live start` has
  run). `finalize` sums what was recorded. Never keep the total in your head
  and never pass 0 for a count you did not make: a missing total shows as
  "-", a wrong one is believed.
- **Check who judges**: `venv/bin/python -m ftja.judge status`. When it
  prints `"mode": "api"` with `"ready": true`, the user chose to judge
  with their own API key from the supplier they prefer (`.env`, set on the
  Pipeline tab): wherever
  steps 2-4 below say to call `Agent` subagents for `rc/`, `s1/` or `s2/`,
  run instead

  ```
  venv/bin/python -m ftja.judge run --dir <run_dir> --stage <rc|s1|s2>
  ```

  once per stage (no batches, no waves). It judges every prompt of that
  stage without an answer, writes the same `<n>.out.json` files, and
  records the real tokens itself — do not call `record-tokens` for it. Its
  `failed` lists jobs it could not answer: run it again once (it only
  takes those); a rerun the check commands ask for is
  `--jobs <n,n> --force`. Everything else (`check-*`, `prepare-*`,
  `results`, `finalize`) is unchanged. With `"mode": "api"` but
  `"ready": false`, fall back to subagents for this run and tell the user
  what is missing: a key (Pipeline tab, or `.env` as the printed
  `key_var`, from `key_page`), the address (custom only), or the models —
  for those, offer "Choosing the judge models" at the end of this file. Never print, read
  aloud or copy the key.
- **Check the criteria list**: `venv/bin/python -m ftja.verdict status`.
  `rubric-criteria.json` is the rubric as a list of single criteria with
  stable ids; Stage 2 answers per criterion and `finalize` computes the
  verdict from those answers. The user edits this list one criterion at a
  time in the viewer's Pipeline tab, which rewrites `rubric.md` from it. If
  the command prints `ok`, continue. If it prints `missing`, `stale`
  (rubric.md was edited as text since) or `invalid: ...`, rewrite the file
  from `rubric.md` yourself before going on:

  ```json
  {"rubric_version": "<venv/bin/python -c 'from ftja.state import rubric_version; print(rubric_version())'>",
   "criteria": [
     {"id": "direct_build", "kind": "pass", "group": "builder", "label": "Builds the product personally", "text": "<the rule>"},
     {"id": "internship", "kind": "fail", "label": "Internship or trainee position", "text": "<the rule>"},
     {"id": "ownership", "kind": "preference", "label": "Hands-on, zero-to-one ownership", "text": "<the rule>"}],
   "notes": {"pass": "", "fail": "", "preference": ""}}
  ```

  - `kind` is one of the rubric's three categories. `pass`: a reason the
    role is a match. `fail`: a reason to reject it, wherever the rubric
    states it — including any "Fail when ..." line under Preferences.
    `preference`: everything else; shown to the user, never decides.
  - `group` (pass only, optional): give the same group name to pass
    criteria that only count together ("both must be evidenced"). A job
    passes on any one group, or on any one ungrouped pass criterion. Most
    rubrics need no groups.
  - `label` is what the user sees on every job, next to Met / Not met /
    Triggered. Write it so it reads on its own, in at most 6 words:
    "Requires a language the candidate doesn't speak", not "Language".
  - `text` is the rule the model applies. Carry the rubric's own wording
    over, with its examples and exceptions; do not shorten it into a
    paraphrase and do not add anything the rubric doesn't say.
  - `notes`: guidance in a section that belongs to no single criterion
    (how strict to be, a Stage 1 note). Leave out "fail if nothing passes";
    the rule already does that.
  - Keep the id of every criterion that still exists, even if its wording
    changed. The viewer stores the user's per-criterion feedback under
    these ids. New ids: short snake_case.
  - Do not rewrite `rubric.md` here. Run `ftja.verdict status` again; it
    must print `ok`.
- **Old details** (interactive runs only): `venv/bin/python -m ftja.state
  prune-preview`. It changes nothing. If `worth_asking` is false, say
  nothing and go on. If it is true, tell the user, before anything else
  runs, exactly what it reports and ask whether to remove it:
  - how many jobs, judged between which dates (`jobs`, `judged_from`,
    `judged_to`, older than `older_than_days` days), and how they break
    down (`by_status`);
  - what would be removed from each of them (`removes`) and what stays
    (`keeps`), and that jobs they marked as applied are not touched;
  - the database's size now and about how much comes back
    (`database_bytes`, `bytes_freed_estimate`, in MB).
  Only on a clear yes run `venv/bin/python -m ftja.state prune` and report
  the size before and after. It cannot be undone. On an unattended run
  never prune and never ask.
- **Check for pending review decisions**: `venv/bin/python -m ftja.state
  pending-review` and `venv/bin/python -m ftja.state pending-feedback` (the
  second lists single criteria the user disagreed with in the viewer;
  "empty" below means both are). This is what replaces a live watcher — review "just
  happens" as part of the normal run cadence instead of needing a
  background process. If it's empty, continue straight to step 1. If this
  is an **unattended invocation** (triggered by the scheduled launchd
  trigger, no one to ask) and the list is non-empty, also continue straight
  to step 1 — pending items just wait for the next interactive run, don't
  block the scrape over them. If this is an **interactive invocation** (the
  user typed something to trigger this) and the list is non-empty, pause
  here and follow `/ftja-review`'s steps 2-3 (propose concrete
  criteria.json/rubric.md changes for each pending reason, confirm before
  applying) before moving on to step 1 — this is the only place that skill's
  logic runs unless the user explicitly calls `/ftja-review` on its own.

## 1. Start the run and scrape (Stage 0a)

Do this only after the preflight above is settled (the criteria list is
`ok`, pending reviews are handled), because it copies `criteria.json`'s
search settings and `rubric-criteria.json` for this run:

```
venv/bin/python -m ftja.live start
```

It prints `{"run_id": ..., "run_dir": ".ftja-run/<id>", "stages": [...], ...}`.
`stages` is the list of judging stages this run does (see "Which stages a
run does" above); tell the user which ones in your first line. Every later
command takes that `run_dir` as `--dir`; every file of this run lives in it
(nothing goes to /tmp). From this moment the run is visible in the viewer's
Results tab, and it advances there by itself as the files below appear —
you never report progress, and you never write these files by hand.

`start` also prints `searches`: the run's searches in order, one for
every search term in every location (`criteria.json`'s `search_terms` ×
`locations`; 3 terms and 4 locations make 12). Scrape each of them by its
number in that list (0, 1, 2, ...), one after another — a separate command
per search, with a line to the user between them (see "Keep the user
informed"):

```
venv/bin/python -m ftja.live scrape --dir <run_dir> --search <number>
```

Each call reads its term, its location, the time window and the cap per
search from the run's own snapshot, scrapes in batches of 10, and updates
that search's count after every batch. Do all of them: a search you skip
is a term that was never looked for in that location.

## 2. Deterministic filter (Stage 0b)

```
venv/bin/python -m ftja.live stage0 --dir <run_dir>
```

Merges the scrapes (one entry per `job_url`), runs `ftja.filter_stage0`,
and prints `{"scraped": N, "passed": M, "dropped": {...}}`. `M` is your
coverage number for this run (compare it, over time, against what
LinkedIn's own search UI shows for the same term — that's the Acceptance
Criteria #2 check, not something to automate here). Location is not part
of Stage 0 — it's already deterministic at scrape time.

What the filter does, all in code with no LLM call (titles are already
settled: the scrape keeps only postings whose title contains the search
term that found them); drops a JD not written
in a language the candidate reads (langdetect against `criteria.json`'s
`languages`); drops a JD that plainly requires a language outside that list
("Fluent in German and English"), keeping anything ambiguous ("German is a
plus") for Stage 2; requires a tier-1 keyword (only when Stage 1 is one of
the run's stages); applies exclude keywords; when the Remote check is one
of the run's stages, drops a posting with none of the user's remote
keywords in its title or description (`no_remote_keyword`);
collapses the same JD reposted under several URLs into one job; and, last,
drops jobs an earlier run already judged (they're in `seen.db`), so no LLM
call is spent on the same posting twice. The
language-requirement drops are listed in the rejected file with the
sentence that triggered each, and are not recorded as seen.

## 2b. Remote check — cheap-model reading of the remote sentences

**Only when `remote` is in the run's `stages`.** Otherwise skip to step 3.

```
venv/bin/python -m ftja.live prepare-remote --dir <run_dir>
```

Writes one filled prompt per Stage 0 survivor that has a remote keyword to
`<run_dir>/rc/<n>.txt` (template: `remote_prompt.md`; the job's title, the
sentences around its remote keywords, and the categories of the user's
`remote-check.json` with the answers each allows). It prints `jobs`: they
are numbered `0 .. jobs-1`. (`without_remote_keywords` counts postings kept
without any remote keyword; code settles those, there is no prompt for
them.)

Call the `Agent` tool with `model: "haiku"`, in **batches of up to 10 job
numbers** per subagent, exactly as Stage 1 below does it (read all prompts
in one step, write all answers in one step, at most 20 calls per message,
record each call's tokens). Each subagent reads `<run_dir>/rc/<n>.txt` and
writes its answer to `<run_dir>/rc/<n>.out.json`. The answer is ONLY:

```json
{"verdict": "pass" | "fail", "reason": "<one sentence, at most 15 words>", "evidence_sids": ["S3"],
 "answers": [{"id": "<category id>", "answer": "<one of that category's answer ids, or ?>",
              "detail": "<12 words max>", "evidence_sids": ["S3"]}, ...]}
```

The `answers` report what the posting says per category (`?` when it does
not); an answer the user marked as ruling a posting out fails it, in code.
Otherwise the top-level `verdict`, the model's overall reading against all
of the user's answers, decides, and a pass that points at no sentence it
was shown is recorded as a fail. Do not judge,
edit or complete an answer yourself.

Then check the answers:

```
venv/bin/python -m ftja.live check-remote --dir <run_dir>
```

`rerun` lists jobs whose answer cannot be read (no file, no verdict, an
answer that is not on a category's list): rerun exactly those job numbers
once. A pass without an evidence sentence is not in this list and is not
to be rerun: it is settled as a fail.
The next step refuses while any is missing.

## 3. Stage 1 — cheap-model sentence-block judgment

**Only when `stage1` is in the run's `stages`.** Otherwise skip to step 4.

```
venv/bin/python -m ftja.live prepare-stage1 --dir <run_dir>
```

Writes one filled prompt per job Stage 1 judges to `<run_dir>/s1/<n>.txt`:
the Stage 0 survivors, or only the Remote check's passes when that stage
ran first (template: `stage1_prompt.md`; the job's keyword sentences with
their neighbours, plus `rubric.md`'s Pass/Fail sections). It prints how
many jobs there are; they are numbered `0 .. jobs-1`.
(`failed_by_code_no_keyword`, on a run continued from the Remote check,
counts postings with none of the Stage 1 keywords: code fails those, there
is no prompt for them.)

Call the `Agent` tool with `model: "haiku"`, giving **each subagent a batch
of up to 10 job numbers**: it reads `<run_dir>/s1/<n>.txt` for each, judges
each job on its own, and writes each answer to `<run_dir>/s1/<n>.out.json`.
The answer is ONLY:

```json
{"verdict": "pass" | "fail", "evidence_sids": ["S3", "S4"], "reason": "<one sentence, at most 15 words>",
 "blocks": [{"sid": "S3", "why": "<12 words max>"}, ...]}
```

`reason` is shown to the user next to every job Stage 1 turned down, so it
must say what decided it, not "no pass criterion met". `blocks` has one
entry per [T1] sentence: what the model made of that sentence. The user
sees it under each matched sentence, next to the keyword that matched.

Tell the subagent to work in as few steps as it can: read all of its
prompt files in one step (the Read calls together), decide every job, then
write all of its answers in one step (the Write calls together). Do NOT
ask it to finish one job before reading the next: every extra step is a
round trip, and in a measured run that made a batch of 7 take 262 seconds
instead of 83 for the same verdicts. The viewer's Stage 1 count therefore
moves a batch at a time.

Batching is deliberate: every subagent carries a fixed overhead of roughly
45k tokens, so one job per subagent cost about 5× more for the same verdicts
in a measured run. Stage 1 inputs are short keyword excerpts, so a batch of
10 stays small.

Run the batches in parallel by putting several `Agent` calls in one message,
but **no more than 20 per message** — that is the concurrent subagent limit,
and calls beyond it fail. Send the next wave after the previous one returns.

Ask each subagent to also reply with one line per job (`N <json>`). Writes
can fail on transient permission-check errors; when an output file is
missing, write it yourself from the reply. If neither exists, rerun that
job. Evidence is by S-id only, so there are no quotes to hallucinate. Record each call's tokens with `record-tokens`, as in the preflight.

Before Stage 2, check the answers against the sentences each prompt held:

```
venv/bin/python -m ftja.live check-stage1 --dir <run_dir>
```

`rerun` lists jobs whose answer cites a sentence the prompt never had, or
passes a job without citing any: rerun exactly those job numbers once (one
`Agent` call can take several). `prepare-stage2` and `results` already treat
them as missing. `warnings` (a keyword sentence with no reading) are fine to
leave; they show as an empty reading under that sentence.

## 4. Stage 2 — mid-model resume/portfolio judgment

**Only when `stage2` is in the run's `stages`.** When it is not (Stage 2
is switched off on the Pipeline tab), skip this whole step: do NOT run
`prepare-stage2` and do NOT call any Stage 2 subagent. Go to step 5.
`results` records what passed the run's last stage as waiting, and the run
can be continued later. Then follow "After a run that stopped early" at
the end of this file instead of ending your turn.

If `profile/summary.md` doesn't exist, STOP and tell the user to run
`/ftja-setup` — don't fall back to reading the raw CV/portfolio, that
reintroduces the token cost the summary exists to avoid.

```
venv/bin/python -m ftja.live prepare-stage2 --dir <run_dir>
```

Run it once Stage 1 is complete; Stage 2 starts only then, so the stages
run and show one after another. It refuses, naming the job numbers, while
any Stage 1 answer is missing or unreadable — fix those first. Otherwise
it writes one filled prompt per Stage 1 pass (per Remote check pass, on a
run without Stage 1) to `<run_dir>/s2/<n>.txt` (template: `stage2_prompt.md`, with
the run's criteria list and the full JD) and prints how many there are,
numbered `0 .. jobs-1`. A job whose description is empty is left out and
recorded as a Stage 1 fail with a note.

For each one, call the `Agent` tool with `model: "sonnet"` — **one job per
subagent; do not batch Stage 2.** In a measured comparison, borderline jobs
that failed in every single-job run passed when judged in a batch alongside
similar postings. Stage 2 is the final verdict, so it stays single-job. The
subagent reads `<run_dir>/s2/<n>.txt` and follows it (it reads `rubric.md`
and `profile/summary.md` itself), writes its JSON answer to
`<run_dir>/s2/<n>.out.json`, and returns the same JSON in its reply so a
failed write does not lose it.

The answer has one result per criterion and no overall verdict, plus what
the employer asks for, a one-line company description and notes:

```json
{"company_line": "...",
 "criteria": [{"id": "direct_build", "result": "met", "quote": "<verbatim from the JD>", "why": "<one short sentence>"}, ...],
 "employer_requirements": [{"kind": "must", "label": "...", "quote": "...", "candidate": "meets", "why": "..."}, ...],
 "notes": [{"text": "...", "quote": "..."}]}
```

Do not decide pass/fail from this yourself, and do not edit, drop or "fix"
any entry: copy a reply into the output file exactly as returned. Code
checks each quote against the JD and computes `passed` / `review` /
`stage2_fail` by a fixed rule (`ftja/verdict.py`): a result the model gave
without a quote that really appears in the JD is downgraded to `unclear`, a
criterion the model skipped counts as `unclear`, and an employer
requirement or note whose quote isn't in the JD is dropped. The viewer
shows each job's card the moment its file lands.

Run these calls in parallel waves of at most 20 per message, as in Stage 1.
Record each call's tokens with `record-tokens`, as in the preflight.

## 5. Finalize

```
venv/bin/python -m ftja.live results --dir <run_dir>
```

It refuses, naming the job numbers, while any answer of a stage this run
does is missing (for Stage 2: isn't valid JSON with a `criteria` list) —
rerun those jobs and call it again. Otherwise it writes the run's `results.json` and
`stats.json`. Then:

```
venv/bin/python -m ftja.finalize --run-dir <run_dir>
```

This computes each Stage 2 job's verdict against the criteria list copied
at the start of the run, records everything in `seen.db` (title/company/
location and the Stage 1 reason for every job; for jobs that reached Stage
2 also the per-criterion results, the employer's requirements, notes and
the full JD text), writes `digest-<run id>.md` (passed, then the ones to
review) and `rejected-<run id>.md` (Stage1/2 fails, with their reasoning,
so "why did X fail" stays readable after the run ends; the run id is the
run's start time, so two runs on one day keep separate files), appends `run.log`
and `runs.jsonl`, fires the notification (macOS only), and marks the run finished
so the viewer swaps the live view for the finished run — do this even if 0
jobs passed (silent failure is exactly what we're avoiding).

## 6. Release the lock and report

```
venv/bin/python -m ftja.lock release .ftja.lock
```

If this was invoked interactively (not from launchd), tell the user the
digest path, the pass and review counts (`finalize` prints both; "review"
means the posting was ambiguous on a deciding point and the user should
read it), and that the run is in the viewer's Results tab.

## After a run that stopped early

A run whose `stages` do not include `stage2` stops after its last stage.
Do steps 5 and 6 as usual (finalize, release the lock). In your report,
say that the run stopped there on purpose, how many postings passed that
stage, and that they can read them in the Results tab ("Passed N — see
why" on that stage's line; for the Remote check that popup also downloads
the table) and press **Continue to Stage 1** or **Continue to Stage 2**
there when they want another stage to run.

On an **unattended** run, stop here.

On an **interactive** run, do not end your turn yet: stay available for
those buttons, the way the setup chat waits for the web view. Tell the
user you are waiting for about nine minutes, then run (shell timeout
600000 ms):

```
venv/bin/python -m ftja.run_bridge wait --run-id <run id>
```

- `{"status": "continue", "to": "stage1" | "stage2"}`: the user pressed a
  Continue button. Go on with "Continuing a run that stopped early" below,
  for this run id and that stage (`to` missing means `stage2`).
- `{"status": "remote"}`: the user pressed the Remote check's button on
  the Pipeline tab. Follow the `ftja-remote` skill
  (`.agents/skills/ftja-remote/SKILL.md`) from its step 1, then start this
  wait again.
- `{"status": "keywords"}`: the user asked on the Pipeline tab for the
  keywords of a language they started reading. Follow the `ftja-keywords`
  skill (`.agents/skills/ftja-keywords/SKILL.md`) from its step 1, then
  start this wait again.
- `{"status": "timeout"}`: nobody pressed anything. End your turn, and say
  that the run can still be continued any time by typing
  `/ftja-run continue <run id>` in this chat (the button shows the exact
  line when no session is waiting).

If the user writes to you while you wait, answer them; the wait can be
started again afterwards.

## Continuing a run that stopped early

For "/ftja-run continue [run id] [stage1|stage2]" or "continue to Stage 1 /
Stage 2". The user stopped the run before this stage on purpose and is now
asking for it. Stage 2 is the expensive one (one `sonnet` subagent per
posting). The stage named is the one to run; with none named it is Stage 2.
Stage 1 can only be asked for on a run that stopped after the Remote check.

1. For Stage 2, check `profile/summary.md` exists, as in step 4.
2. Take the lock exactly as in the preflight (`ftja.lock check`, then
   `acquire`). If it is locked, a run is in progress: say so and stop.
3. Reopen the run:

   ```
   venv/bin/python -m ftja.live continue --run-id <run id> --to <stage1 or stage2>
   ```

   Leave `--run-id` out to take the latest run that is waiting; leave
   `--to` out for Stage 2. It prints the `run_dir` and how many postings
   are waiting. If it refuses (the run is not waiting, it cannot go on to
   that stage, or its working files are gone), release the lock, tell the
   user what it said, and stop. Before going on, tell the user how many
   postings the stage will read.
4. Do that stage's step for that `run_dir`: step 3 from `prepare-stage1`
   on, or step 4 from `prepare-stage2` on. Do only that one stage. The run
   judges against the rubric, keywords and criteria list it was started
   with, not today's.
5. Do step 5 (Finalize) and step 6 (release the lock and report). The run
   keeps its place and its id in the Results tab. After Stage 2 its
   postings carry their final verdict. After Stage 1 the run has stopped
   early again, with the Stage 1 passes waiting: follow "After a run that
   stopped early" above.

Do not scrape, do not run Stage 0 or an earlier stage again, and do not
run the version check or the pending-review preflight for a continue.

## Choosing the judge models

For "choose my FTJA judge models", or when `ftja.judge status` shows API
judging with a model missing. FTJA ships no model names: suppliers rename
and reprice models often, and a guessed name fails or costs more than it
should. So:

1. `venv/bin/python -m ftja.judge models` — the model ids the user's key
   can use, from the supplier itself. Only suggest ids from this list. (If
   it fails, the key or the address is wrong: say so and stop.)
2. Read the supplier's current prices at the `pricing_page` that
   `ftja.judge status` prints (fetch the page; do not answer from memory).
   Note anything that changes cost: thinking/reasoning modes billed as
   output, peak and off-peak rates, cached-input prices.
3. Suggest two models from the list: the cheapest one fit for short
   yes/no screening (Stage 1 and the Remote check) and a stronger one for
   Stage 2, which quotes the job description against each criterion.
   Show each one's input and output price per million tokens, and a rough
   cost per run (Stage 1 ≈ 2k input + 300 output tokens per posting,
   Stage 2 ≈ 15k input + 1.5k output per posting reaching it; use the
   counts from `runs.jsonl` when there are any).
4. Only after the user agrees:
   `venv/bin/python -m ftja.judge set-models --s1 <id> --s2 <id>`.
   The Pipeline tab shows them on its next load.

