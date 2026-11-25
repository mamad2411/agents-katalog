---
name: profile
description: Interviews the user about how they work with agents, then creates a new hive profile or edits an existing one - the posture, runbook, and worker files a lead and its workers read. Use when the user says /hive:profile, "set up a hive profile", "create a profile for this project", "edit our hive profile", "make hive lead/orchestrate here", or wants a project to go from no standing process to one hive can run, globally or per project.
---

# hive profile

You are interviewing someone to produce, or change, a hive profile: the standing instructions (`posture.md`, `runbook.md`, `worker.md`) that tell a lead and its workers how this person wants work to run. Read `references/interview.md` before you ask a follow-up question or write anything - it holds the discovery map, the target-selection rules, and the `hive.yml` routing this skill depends on.

## Read before you ask anything

Run `hive profile list` and `hive doctor` (or read this project's `hive.yml` directly) before the first question. If this is an edit, also read the named profile's current, rendered behavior for each of `posture.md`, `runbook.md`, `worker.md`, and any other `.md` it carries, using "Read a rendered file in bounded sections" below, so you understand what this profile actually does today. Do not ask the user to repeat anything already answered by what you just read. This rendered read is for understanding only - `references/interview.md` covers the raw template (via `hive profile path`) you must read from, and write onto, when you actually apply an edit; a rendered copy drops any conditional section whose var is unset, so it is never a safe edit source.

## Read a rendered file in bounded sections

A harness may persist tool output over about 30KB to a file and show only a short preview, so a large rendered file read straight into a tool result is read mostly unseen. Redirect first, then look. `profile_name` is a name from `hive profile list`, `profile_file` is a filename it lists, and `profile_rendered` is a disposable file:

```sh
profile_rendered=$(mktemp)
hive profile read "$profile_file" --profile "$profile_name" > "$profile_rendered" && wc -c < "$profile_rendered"
printf '%s\n' "$profile_rendered"
```

Shell variables do not survive between tool calls. Note the path the last line printed and write that literal path into every later command and every file-reader call; do not rely on `$profile_rendered` after this call.

Use the saved content only if the read command succeeded. `wc -c` is the rendered size in bytes, the same number `hive profile list` and `hive doctor` show. If it is 25600 or less, read the whole file with your file reader. Above that, never read the whole file in one tool call; read it in sections of at most 16000 bytes each:

1. Check for long lines first: `awk 'length > 2000 {print NR; exit}' PATH`. A file reader truncates any line over 2000 characters, so if this prints a line number, read the whole file by bytes with step 3 instead of with line ranges.
2. Otherwise pick a line range with your file reader's offset and limit, and measure it first: `sed -n '1,80p' PATH | wc -c`. Shrink the range until the count is 16000 or less, then read it. Continue from the next line until you have read the last line. A scan of the headers is not a read.
3. To read by bytes: `dd if=PATH bs=1 skip=0 count=16000 2>/dev/null`. Advance `skip` by 15996 each time, which overlaps 4 bytes so text split at a section edge shows whole in the next section. Stop when a section reaches the byte count from `wc -c`.

Delete the temporary file when you are done. It is for understanding and checking only, never a source for an edit (see below).

## Discovery first, not a checklist

Start with the work, not with profile structure: ask about a recent task they did with an agent, from start to finish. Follow what they say into current agent use, handoffs, checking, review, and permissions - what already works and where they repeat themselves or correct the agent. This is adaptive: choose the next question from the last answer, not from a fixed list. `references/interview.md` has a scored map of optional follow-up questions - each tied to an answer signal that makes it worth asking - and a question budget so discovery converges instead of running forever. Most of that map goes unused in any one interview; it is there so you know what to ask *if* the signal for it shows up, not a form to complete.

For an edit, ask "what should change, and what should stay?" first, and read the current profile before asking about anything it already states.

## Both routes are equally valid

Orchestration (a lead delegating to workers) and simple (one session doing its own work) are both first-class outcomes. Recommend one from what you heard, name the one reason tied to their answer, and offer the other without calling it an upgrade or a downgrade. No stated preference means recommend simple: it is the smaller thing to start from, and delegation is available later through an edit. `references/interview.md` lists the signals for each route.

## Several profiles are fine

The user may want more than one profile - a simple one and an orchestration one, or a different profile per kind of project. Handle building several in one session: preflight every name and destination before the first write, so a bad name is caught before anything is created, and keep each profile's own differences and confirmation separate even when the discovery was shared.

## Start small; editing is how a profile grows

A first profile carries only what this interview actually surfaced. A new simple profile is `posture.md` plus a short `runbook.md` written from the confirmed answers - not a copy of anything thicker. A new orchestration profile starts from the shipped orchestration files as they are. That base already says the lead assigns todo ids, supervises and accepts, and a worker never completes its own todo. The runbook spells out lanes, the brief, scope, worktrees, shared resources, checks, review, permissions, waiting, the context checkpoint, handback and record, closing a lane and cold boot, and the posture sets the model tiers, so do not interview for any of them. The interview only fills its optional vars from confirmed answers and edits a rule the user wants changed; it does not add sections nobody asked for. Depth comes from running this skill again later to edit, not from a bigger first pass. Do not add a mandatory extra `.md` file, a review tool, or a tracking artifact that nobody's answer called for.

## Converge, then confirm once

Stop discovery when you can state: the current task flow, at least one pain or wanted change, one habit to keep, who owns which actions, how they'll know work is done, and who the profile is for (this project only, or every project on this machine). Summarise that back, offer at most three improvements each tied to something they said, and let them accept, decline, or edit each one. Before writing anything, show: profile name(s), the base each starts from, the target(s) you are about to write to (see below), and - for an edit - a concrete diff. Confirm once. Do not keep discovering after the user asks to proceed.

## Offer a flows diagram before writing

After the summary is confirmed and before any write, offer to draft a Mermaid flowchart of the proposed workflow - who does what, in what order, and where the human decides. Draw it only from the confirmed answers and the files you are about to write; never invent a step the profile itself does not contain. Iterate on it with the user until it matches what they actually agreed to. Once accepted, save it as `flows.md`, an ordinary optional extra `.md` in the profile - resolved and reported by `hive profile list`/`hive doctor` the same as any other fork-local file, never required. Tell the user plainly that Mermaid renders on GitHub or in an editor preview, not in a terminal, so they know where to look at it. On a later edit that changes the workflow, update `flows.md` in the same change, or say explicitly that it is now stale if you cannot update it in this pass - never leave it silently wrong.

## Read past sessions as evidence, with permission

For an established project - one that already has prior Claude Code or Codex sessions - ask permission before reading any of them: "Can I look at your recent sessions in this project to see how you actually work?" On a decline, or when nothing usable turns up, fall back to the ordinary discovery questions; this is a supplement to discovery, never a replacement for it.

On acceptance, read a bounded, recent first batch (for example, the ten most recent) from each harness's standard transcript location, filtered to this project. Claude Code groups its transcripts by project directory already, under its config dir's `projects/` (`$CLAUDE_CONFIG_DIR`, default `~/.claude`); Codex's rollout files live under `$CODEX_HOME/sessions/` (default `~/.codex`) and are not grouped by project, so filter by the working directory recorded inside each session instead. Do this reading in a subagent when the harness offers one, so raw transcript content never enters this interview's own context - only the findings below do.

That first batch is a starting sample, not a cap. If it leaves the evidence too thin to act on - no repeated pattern, or every session from just one kind of task - say plainly what is missing and ask the user whether to read another batch. Read more only on a yes, and you may ask again after each further batch; never extend the sample on your own judgment without asking first.

Surface what you found as observations, each with one short quoted example, covering how the user briefs work, what they correct repeatedly, and where work stalls or gets redone. Use those observations to propose a workflow, then ask "what didn't work for you here?" so the user can correct a wrong reading before you act on it. Never write transcript content - a quote, a session id, a path - into the profile itself; only the resulting workflow decisions belong there. Naming a specific harness's transcript convention here is fine (it is a documented fact about how that tool stores its own history), but do not name a skill hive does not ship as part of how you read or process them.

## Know which file you are about to write

There are two possible write targets, and they behave differently:

- **The user's own override** (their machine's copy-on-write fork, normally under their hive data directory). This always wins at read time over anything shipped.
- **The shipped source**, only when you are running inside a hive checkout (this repository, or another clone of it) - the actual template files under this checkout's `profiles/<name>/`.

`references/interview.md` has the exact detection and confirmation rules. Never guess: an unclear target is a question, not a default. If the user's own override already exists for a name whose shipped source you are about to edit, say so - the override will keep hiding your change until they deal with it - rather than silently editing both or picking one.

## Preserve what you did not ask about

An edit changes only the rule that was discussed and any dependent instruction the user explicitly approved. Everything else - unrelated sections, an optional `.md` file, `hive.yml` comments and keys, loader-owned metadata - is read fresh immediately before writing and carried through unchanged. If the file changed since you proposed the edit, re-read it, show the revised diff, and confirm again before writing.

## Route project facts into `hive.yml` `vars`, not prose

A command, a repository name, a ticket prefix: these belong in `hive.yml` `vars` and get referenced from the profile as `{{var}}`, not hard-coded into the generated `posture.md`/`runbook.md`/`worker.md` text. This is what lets one profile serve several projects. `references/interview.md` lists the `hive.yml` keys and var names this skill knows how to write. The shipped orchestration profile renders these optional vars: `check`, `install`, `repo`, `ticket_prefix`, `start_command`, `test_command`, `suite_command`, `verify_command`, `review_command` and `worker_model`. Offer one only when the interview confirmed its value, and leave the rest unset: an unset var drops its section, and nothing makes the user fill every one.

## Worked examples, only on request

`references/examples/README.md` indexes two worked examples: one orchestration profile rendered for a personal repo and a work repo, and an annotated skeleton of the three files. Open one only when the user asks to see an example or wants to adapt one. They are not part of discovery and add no interview question.

## Offer a recipe only on its own signal

`references/recipes/index.md` links a small library of optional patterns - a verification step, a shared-resource rule, a review-decision habit, and so on - each written to solve one problem an interview signal points to. Read a recipe only after discovery actually surfaces its signal; propose its benefit and cost, and apply it only if the user accepts. A recipe with no signal in this interview does not get offered, and accepting one is never required to finish a profile.

## Validate before you tell them it's done

After writing, run `hive doctor` and read each file you touched with "Read a rendered file in bounded sections" above, from the project the profile is meant to serve. Read it to the last line: a change near the end of a large file is easy to miss. Read worker text with `hive profile read worker.md`, never `hive posture`: `hive posture` prints the lead's file only. `worker.md` keeps its identity placeholders (`{{agent_name}}` and the like) in that read because they fill at spawn, so do not treat them as a defect. A profile with no readable `runbook.md` fails `hive doctor` outright; `posture.md` and `worker.md` do not, but check them anyway. Tell the user to restart any running hive session so it picks up the change, and invite one small follow-up edit once they've tried it - that is the expected way a profile keeps improving.

## After a profile edit lands, ask once about notifying leads

Do this once after the full profile edit has been reviewed and committed, not after each commit or review round. Find the changed files and the commit range for that edit, and record when both review and commit are complete; that is when the edit landed. Use `project_list` to enumerate registered projects and their paths. In each project, run `hive profile list`; its `*` marks the active profile. Keep projects whose active profile matches the one you edited.

For each matching project, call `agent_list` with `{project_id: <project id>}`. A recipient must have `kind: "lead"`, `status: "running"`, and `alive: true`, which means the row owns a live pane. Inspect its `command` for `--append-system-prompt-file <path>`. When the named file exists, compare its modification time with the edit's landed time: notify if the file is older, and exclude it if it is equal or newer. `hive lead` rewrites that file when it launches, so its modification time reflects the current session's posture render. If the command has no such flag or the file is missing, include the lead and state the reason, such as `no posture file flag` or `posture file missing`. Do not include rows with `alive: false` or `alive: null`. Ask once and show the project names, lead names, and any reason a posture age could not be checked: `N running leads use this profile: <projects and reasons>. Notify them?` If no leads qualify, report that and stop.

On no, send nothing. On yes, call `wake_set` once per qualifying lead with `delay_seconds: 1`, `project_id: <that project's integer id>`, and `deliver_to: <lead's integer agent_id>`. Do not pass an actor id such as `lead:663` as `deliver_to`. Each wake body names the changed files and commit range, then tells the lead to re-read with `hive posture`, `hive runbook`, and `hive profile read <file>`, or restart through `hive lead` to reload the posture. Do not send a wake before the human says yes.

## Without the Claude plugin

The plugin only delivers this skill and the `/hive:profile` trigger. A stock Codex user, or anyone without the plugin, follows the same steps by hand: open this file and `references/interview.md` (they ship in the npm package: for a global install the directory is `$(npm root -g)/@cmgmyr/hive/claude-plugin/skills/profile/`, and in a checkout it is `claude-plugin/skills/profile/`), then run the interview in any session. Every command here is a plain `hive` CLI call (`hive profile list`, `path`, `read`, `fork`, `hive doctor`, `hive posture`, `hive runbook`), and the profiles are ordinary markdown. Three parts are Claude-only or harness-specific: the `/hive:profile` trigger, a subagent for reading transcripts (do it inline in a harness with none, in small batches), and Claude Code's transcript location (Codex's rollout path is named above). The notify-leads step uses hive's own MCP tools, so it works wherever hive is registered.

## What this skill does not do

It does not dispatch project work, change which agent application or model a project uses beyond what was explicitly asked, install a third-party tool, or commit or publish anything. It does not choose a model name for the user: `worker_model` is written only to a value they gave. It edits `hive.yml`'s `profile`, `agents`, `vars`, `context_checkpoint_percent`, and `lead_turn_budget` keys only on an explicit ask, and only to values the user gave or confirmed.
