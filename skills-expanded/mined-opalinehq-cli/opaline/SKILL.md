---
name: opaline
description: "Analyse the user's own Claude Code and Codex sessions on this Mac with the Opaline app. Use for any question about their coding-agent sessions or runs: analyse, review or retro my agent sessions; what did my agent do, where did it get stuck, loop or fail; why was that run slow or expensive; compare Claude Code and Codex runs; what my sessions cost by day, repository or model; which mistakes keep coming back; what to change in CLAUDE.md, AGENTS.md, skills, hooks, scripts or CI from what the sessions show; reopen earlier saved answers; or show the Opaline dashboard. Nothing leaves this Mac."
---

# Opaline

Opaline on this Mac holds the user's own Claude Code and Codex sessions, imported by the Opaline app, and its tools talk to the Opaline server the app runs here. Nothing leaves this Mac. A retro finds where the agents lost the most, reads the runs that show why, and fixes the setup that let it happen: instructions, skills, docs, scripts, hooks, lint and CI config.

## Ground rules

- **Facts come from Opaline.** Use the Opaline tools for every fact. The shell is for the parsing scripts in `large-results.md` on a result Opaline returned. Take repository names from the `repository` column or the dashboard, and ask the user when it is still ambiguous.
- **Read selectively.** Opaline counts, ranks and finds; you open only the runs that decide the question.
- **One person's sessions.** Every session here is the user's own. Findings name the setup and the habits that cost time, and the fix for each.
- **Out of scope** (deleting or editing sessions, choosing which agents or folders Opaline imports, Opaline support): say so plainly and point to the Opaline app.
- **Drafts.** No tool changes or deletes sessions. `sql`, `find` and `read` record their calls in a private draft that only `save_answer` publishes. Hosts may ask the user once to allow these; "always allow" is fine.
- **The app must be running.** When the Opaline tools are missing or cannot connect, the Opaline server on this Mac is not running: ask the user to open the Opaline app, then try again.

## Start

**Call `schema` first.** Call it once with no arguments, before any other analysis tool. When `schema` is not among your tools, or it answers that the retro tools are not enabled for this workspace yet, work with `find` and `read` as `classic.md` describes and leave `sql`, `measures`, `patterns`, `checks`, `search`, `run`, `estimate_questions` and `run_questions` unused in this conversation. Otherwise follow the playbook below; for a retro, `retro.md`.

## Which tool for what

Each tool's own description has its arguments, output and limits.

- `answers`: earlier saved analyses (`search`, `open`, `result`).
- `schema`: views, approved measures and run questions; `view=` for a view's columns and traps, `view=` + `column=` for common values. Call it with `view=` for each view you query.
- `measures`: one approved measure per call (`list`, `describe`, `run`); pass the same cohort to each.
- `patterns`: `digest` (the whole retro picture), `list`, `drill`, `verify`.
- `sql`: anything no measure or pattern answers; conventions below.
- `run`: one run, compact, expandable to exact records (`r<record_idx>`).
- `search`: runs by meaning, exact string or regex; to keep matches as evidence, use `search('…')` inside sql.
- `checks`: save a recurring failure as a check (`test` first, then `create`); `run` sees whether a fix held.
- `run_answers` (a view), `estimate_questions`, `run_questions`: yes/no questions answered per run; a run without a row is unanswered, not "no".
- `find`, `read`: the classic tools, and the fallback when `run` says a run's requests are not indexed yet.
- `get_dashboard`, `save_answer`, and `list_workspaces` to check that sessions have arrived.
- `share_answer` has no use here: answers stay in the Opaline app on this Mac. When the user asks to share one, say so and give the answer's link.

## On this Mac

`large-results.md` is written for Opaline Cloud as well; on this Mac three things differ:
- Links in results are `opaline://` links: they open in the Opaline app, never in a browser, so never suggest a browser or rewrite them to `http://`. Surface them as they are. A link the user pastes from the app (`opaline://…`) goes to `run` as `url`.
- A `too large to page through here … run: opaline pull …` or `opaline sql … --out` line does not apply here: the `opaline` CLI is not connected to this Mac's Opaline. Aggregate, narrow from/to or the filters, and say what the answer covers.
- `agent_feedback` reaches nobody at Opaline from here; leave it unused.

## sql conventions

These are the gotchas no tool description carries.
- `calls`, `events` and `prompts` keep their time range in their own `WHERE` (`started_at >= …` for calls, `at >= …` for events and prompts). About a week of busy command text fits the limits; a month may not.
- Alias results with new names (`sum(cost_usd) AS total_cost`). An alias that reuses a column's name is read wherever the query names that column.
- `search('text'[, 'hybrid'|'meaning'|'exact'|'regex'[, days]])` is a table: join it to `runs USING (run_id)` to rank matches by impact; at most 3 per query.
- Rank with the approved measures (`active_time`, `cost`, `tokens`, `runs`, `re_asks`, `frustration`, `group_run_time`, `group_call_time`).
- `source` is `claude_code` or `codex`: group or filter by it to compare the two agents, over the same window and repositories.
- A result marked `refused, do not retry` stays refused: narrow the query. Every result is stored as `sr_…`; its rows say where to look, and the runs you read say why.
- `session_links` follows a task across sessions; `setup_snapshots` dates setup changes, and `effective` says which settings apply. `schema view=` explains both.

## The playbook

Every analysis question runs these steps in order; dashboard requests skip them. A retro, or "how do I improve my agents", runs `retro.md` in place of steps 2-6. A question about one run or session ("what did my agent do", "why was that run slow") starts at step 5 with that run, after step 1.

1. **Earlier analysis.** `answers action=search` with the question's words. If one covers it, `answers action=open` and say its findings and cutoff in one sentence; this analysis updates it.
2. **Rank where the sessions lost the most.** Run the query measures that fit the question (`measures action=run`, one call each, one cohort for all); write `sql` only for what no measure answers. State the impact order you picked (active time, cost, frustration, re-asks or runs). Show a group of calls' time both ways, `group_run_time` and `group_call_time`; neither is time lost until those runs are read. The window the user asked for wins (default: the last 30 days); compute every total over the whole window, updates included.
3. **Find by topic.** When the question names a topic, flag, file or error, use `search` or `search('…')` in sql.
4. **Run questions.** For meaning facts cannot give ("did the agent struggle to find the file?"), rank with sql over `run_answers` (one `provider`). For runs without answers, `estimate_questions` over a SQL-selected set, state the cost and runs, then `run_questions` when it is worth it. A probability says where to read.
5. **Read the top 10-15 runs** with `run`, expanding only the phases, requests and records that decide the question, and quote exact records (`r…`). Done when you can say "read N of M" and every unread run is "not attributed".
6. **Propose a fix** in the setup that let each problem happen, quoting the setup text the run received where it matters (`prompts` with `kind = 'injected_context'`). Name the fix type: navigation pointer, automated check, reviewer standard, slim the instructions, streamline a tool, delete no-op steering, widen access, or skill / skill update. Name the channel: instructions and skills reduce a problem; a check, hook, script, doc or config is a mechanism; taste and model limits stay. Say how to re-check each finding, and offer a check for a failure that keeps happening.
7. **Save**, then answer ("Save and answer"). A later update recomputes the same measures over the new window and sums the earlier findings' runs from `finding_runs`.

Ask once, after the first `sql` and before reading, when the window, the order or the scope is ambiguous: offer options with real counts and mark a default. When the user said "just do it" or nobody can answer (a scheduled run), use the defaults and state them on the first line.

**Conclusions** rest on runs you read. Counts, probabilities and search hits say where to look. A rate before and after a fix, over the runs that record the fact, is a trend; numbers come from the tools, and savings stay unestimated. **Unknown is not zero**: name what is unknown (NULL facts, `unrecorded_facts`, `coverage_gaps`, unpriced runs, unindexed sessions, cut results) and the coverage behind each number.

**Evidence** the reader can find without Opaline: the session id, the time the tool printed with it (`started …`, `at …`, the transcript's own UTC timestamp) and a short exact quote. Opaline ids (`sr_…`, pattern ids, `q`/`r`/`c` handles, run ids) come second, never alone.

## Save and answer

- The first `sql` leaves out `analysis` and starts a draft; pass `analysis` from the trace line to every later `sql`.
- Before saving, give each finding a `sql` step whose rows are exactly the runs it rests on, with `session_id, agent_id, turn_idx`: `finding_runs` then records their cost, tokens and active time for later updates.
- `save_answer` once: `analysis`; `question`, a short title (up to 120 characters, such as "Where my agents lost time"); `finalAnswer`, complete; `findings`, one `{step, finding}` per step or query id from a trace line; up to 8 `topics`. To update an earlier answer, add `updates` = its id and `changes`: one `{step, change, evidence}` per finding saved now (`confirmed`, `strengthened`, `weakened`, `new`), plus a `dropped` item, with the earlier step id, for each earlier finding that no longer holds. A refused save saves nothing: fix it and save again. A saved answer is final; a revision is a new draft saved with `updates`. Reuse an earlier finding's runs once `answers action=result` shows its stored result available and fresh; read new runs only after its cutoff.
- Your last message is the saved final answer, complete, since callers often see only the last message. Lead with the answer and its evidence (run ids, short quotes), the window, the impact order and the coverage. End with the link the `save_answer` result gives: it opens the answer in the Opaline app. For an update add "updated from the earlier answer '<title>' (data up to <cutoff>)".

## More in this folder

- `retro.md`: read it for a retro, or any "improve my agents / setup" question.
- `classic.md`: read it when `schema` says the retro tools are off.
- `examples.md`: read it before writing sql for a question shaped like one of its examples (time lost, failing commands, could-be-a-skill, outdated skill, file finding, did a fix work).
- `large-results.md`: read it whenever a result shows a `url:` link, `[cut]` or another omission marker, or is saved to a file, with "On this Mac" above.

## Conventions

- Dates are UTC `YYYY-MM-DD`. Resolve "this month" and "last week" to explicit dates and say which range you used.
- The tools answer from this Mac's Opaline workspace; leave `workspace` out.
- Cost is estimated API cost in USD; NULL cost is unpriced or unknown: say how many runs.
- Subagent runs (`agent_id` not empty, or a Codex thread with `thread_source = 'subagent'`) belong to their parent's work.
- To ask whether an agent saw, read or ran something, count every stream: subagents read files and run commands too, so leave out `agent_id = ''` there. Match a path by its end (`match(file_path, '(^|/)AGENTS\\.md$')`), since a path after `cd ~/…` can be relative.
- A claim that something never happened, or that none or only N of M did, needs a broader check (every stream, or `search('…', 'exact')`) and a run you read that should show it. `sql` notes such traps under the result, and `save_answer` warns when an answer has neither.
- When a tool refuses a read or says the quota is used, say so and stop that line of work.

## When there is no data

When `list_workspaces` shows `sessionsLast365Days: 0` or the views hold no runs, nothing has been imported yet. Tell the user to open the Opaline app and connect their agents there (Claude Code and Codex); the app imports the sessions already on this Mac and every new one. Then check again with `list_workspaces`.
