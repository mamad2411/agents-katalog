---
name: fleet-agent-inspection
description: "Use when checking, briefing, or retiring another fleet agent."
version: 2.0.0
author: coordinator role of hermes-fleet-apps
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [fleet, multi-agent, profiles, inspection, delegation, handoff]
    related_skills: [agent-fleet-design, hermes-agent-factory, fleet-project-pipeline]
---

# Fleet agent inspection

The owner runs several agents on separate profiles, each with its own context.
When they ask "what is <agent> doing on <project>?" you have no handoff and no
shared history. Reconstruct it from that profile's directory, then verify every
claim against the work product itself.

The same skill covers the other directions: **handing work to** a sibling,
**propagating a changed convention** to every agent, and **retiring** one.

**Read-only by default.** Inspecting a sibling's profile is fine; editing its
skills, memories, config or crons is not, unless the owner says so explicitly.
The exception is a standing rule that directly governs the projects that agent
works on — propagate that, and nothing else.

## Procedure

### 1. Search profile CONTENT, never filenames

```
search_files(pattern="(?i)<project>", target="content",
             path="$HERMES_HOME/profiles", output_mode="files_only")
```

A project name typically appears in zero filenames and dozens of files, so a
filename search reads as "that agent never touched it" — the opposite of the
truth. Keep `cache/` out, and never grep `$HERMES_HOME` wholesale by extension:
`*.json` pulls in the model-catalogue cache (one huge line matching anything)
and `*.db` pulls in `state.db`. Name the small files you want.

### 2. Read the highest-signal artifacts

| artifact | what it gives you |
|---|---|
| `profiles/<name>/pastes/paste_*.txt` | its own handoff prompts: state, closed decisions, traps |
| `profiles/<name>/pending/memory/*.json` | proposed memory operations — what it believes |
| `profiles/<name>/logs/agent.log` mtime | working now, or idle since when |
| `profiles/<name>/processes.json` | background jobs still in flight; `[]` = nothing running |
| `profiles/<name>/state.db` | the conversation — what it last told the user |

The newest paste is usually the richest file: a handoff prompt already contains
the summary you are trying to produce.

**"What did it last tell me?" is answered from `state.db`, not `sessions/`**
(often months stale). Open it read-only so the sibling keeps its WAL:

```bash
python scripts/last_message.py <profile>              # its last reply
python scripts/last_message.py <profile> --sessions   # recent sessions
```

By hand: connect via URI (`file:<posix path>?mode=ro`; backslashes break the URI
on Windows), the column is `messages.timestamp`, and `sessions.message_count`
lags — pick the newest session by `max(messages.timestamp)`.

- **Read the last message before calling an agent idle.** One whose final line
  asks for approval ("tell me ok and I'll commit") looks idle in every liveness
  signal and is unblocked by one word. Quote the request verbatim.
- **"I left it running" is a liveness question — answer it in the first line.**
  Log mtime = when the session last thought; `processes.json` = whether a job is
  still executing. `Turn ended: reason=text_response` is a finished turn, not a
  crash.
- **Away from the machine and wondering about a restart?** Check host uptime
  first (`uptime -s`; Windows `systeminfo | grep -i "boot time"`): a reboot
  killed every session and flips the whole report.

### 3. Verify against the work product, not the agent's notes

A handoff states what was true when that session stopped. Re-derive live facts
from the repo; when they disagree, call the note **stale** (work continued), not
wrong (a mistake).

```
git log --oneline -12 ; git status -sb ; git worktree list ; git branch -vv
```

- List worktrees and branches, not just the log: an extra worktree or side
  branch in no handoff is *undocumented state* — ask what it is.
- Cross-check the plan's tick marks against commits and changelog; a done step
  with an unticked box is a stale plan, worth naming.
- When a path you were told to check does not exist, list its parent or `find`
  it by name before concluding it is missing.

### 4. Read the project's own rules before judging

What looks like a mistake is usually a settled decision recorded in `AGENTS.md`,
`CONTRIBUTING.md` or a private notes file. Read it before criticising.

### 5. Report the phase map, not the narrative

Closed / in flight / next, as a checklist; then the one or two items at risk.
Lead with anything that can lose work (many commits, no backup).

- **Name every open item by what it is and where it lives, never by its
  label** — a handoff's labels mean nothing to the owner a day later.
- When the owner drops an item, grep the plan files before saying it is gone:
  an item in a file must be ticked or removed there.
- **"What first?"**: rank by one rule each — what they see every time they open
  the app > small bugs already located > research-only items > scale work
  needing data not on disk — and propose the shape of item one.

## Deciding who owns a capability

Audit what the fleet already has before proposing a new agent or moving a
capability:

```
find $HERMES_HOME/profiles/<name>/skills -name SKILL.md | sed 's|/SKILL.md||'
grep -m3 -E '^(name|description):' <each candidate>/SKILL.md
```

- **A sibling's skills hold the owner's taste**, accrued over months of
  corrections; moving the capability to a fresh agent restarts that at zero.
- **Judge scope by the artifact's toolchain**: when the deliverable is code
  (SVG, CSS, render scripts), the coding agent owns it.
- **List what the sibling already shipped** (`git ls-files <assets-dir>`)
  before offering to produce an asset; a "missing" capability is often committed.
- **A distribution profile is not over-provisioned**: a profile shipped to end
  users legitimately carries skills inert on this host.
- **A coordination mechanism nobody uses is not a saving**: check the board is
  actually used before adding bookkeeping there, and name when it would pay off.
- **The handoff artifact between agents is a file in the project repo**, on
  the branch the consumer checks out.
- **A gitignored coordination file lives in exactly one worktree**: sibling
  worktrees do not have it (`git check-ignore -q <dir>`); say which directory a
  session must be opened in.
- **A long-lived side worktree holds stale copies of shared assets**: compare
  with `md5sum`, and make `git merge main` the first step of a brief that
  consumes them.

## Delegating work TO a fleet agent

Default: you do the whole loop — write a numbered `JOB-NNN/BRIEF.md` in the
sibling's workspace, dispatch it headless, verify, deliver the artifact. "Ask
<agent> to make X" is a request for the finished X, not for a brief.

**Briefs and every committed artifact are in English**; reply to the owner in
the language they write in.

A brief that survives contact contains, in order:

1. **The skill or rules file to read first**, and for a multi-phase build each
   skill named **at the step it applies**.
2. The concrete state: absolute path, branch, HEAD, clean/dirty, what exists.
3. Numbered steps with exact commands and the check after each.
4. **Stop conditions** for what it must not resolve alone (credentials,
   publishing, the owner's decisions) — never for ordinary gaps in the inputs:
   for those, name the fallback source, require it marked at each use, and ask
   for the gap list.
5. **Do-nots**, including not redoing finished work and not disabling a guard.
6. **A "work clean" section as its own heading**: one job folder, which repos
   and profiles are read-only, install nothing, what to delete at the end
   (scratch, temp renders, caches, today's Temp entries), and "list what you
   removed, with paths, in REPORT.md".
7. What to report: the values of each check, not the word "done".

- **Steps needing a password, token or one-time code are the owner's**, listed
  separately and first.
- **Every path in the brief must survive until it is read**: never cite a
  profile's `cache/` or scratch (swept on a timer); cite the repo copy.
- **Read the sibling's SOUL against the real project before its first job
  there.** A precondition naming a folder convention refuses a project that
  keeps the file elsewhere; when the artifact truly does not exist (no brand),
  have it write a job-local file in its job folder instead of inventing one in
  the project.
- **After several compactions, start the next job in a fresh session and write
  the handoff yourself** (project in two lines, HEAD + test command, what closed,
  hard rules verbatim, ONE job). Grep the plan files first for facts the sibling
  holds only in its head.
- **An analysis job** demands "measure on a copy, do not estimate; label every
  projection", a fixed output file and no code. When it returns, check its
  numbers against older plan files and have the stale lines swept.
- **A job needing a public dataset gets a shape first**: folder outside repo,
  backup and scratch; MB at peak; retention decided in the approval.
- **A one-word reply ("hi") means the brief never reached it** — re-send.

**Dispatching headless** when the agent's gateway is stopped:

```bash
cd <project-root> && hermes -p <name> chat -Q --max-turns 600 \
  -q "You are <NAME>. The owner asked for this job (relayed by the coordinator). Read and execute, end to end, the brief at <abs path>. Read it completely first. The owner is away: follow its stop conditions." \
  2>&1 | tee <project>/<JOB>/session-stdout.log
```

Run it in a background terminal with `notify=true`, raise `--max-turns` for a
multi-hour job, and confirm the start ~90 s later from `logs/agent.log` and its
first files (`-Q` keeps stdout empty until the end). Before dispatch, state in
the brief that the owner's request IS the say-so for anything its own rules
gate, and write a baseline file next to the brief (real-data size/mtime, repo
HEAD + `git status --porcelain | md5sum`, cache sizes, Temp entry count) so the
after-check is a diff. Tool evaluations: `references/tool-evaluation-brief.md`.
Supervising the job (watchdog, resume after a cut, sweep):
`references/headless-job-supervision.md`. Facts check:
`scripts/verify_facts_ledger.py`.

### Relaying between the owner and a sibling

- **Relay the owner's decision, not your paraphrase.** Copy names and numbers
  from the canonical source; mark example values as examples and state the rule
  they illustrate. Name the actor of every check ("the coordinator checked",
  "the owner confirmed"), never "I" — the sibling reads the message as the
  owner's voice. Correct a slip at once with a one-line steer.
- **Relay a sweeping principle as a plan with a guard**, not a build order:
  write it into the plan as a phase, audit the gaps, propose a guard test, build
  nothing yet. Tell the owner where you narrowed "everything".
- **Re-read your relay for contradictions** before sending, and **check a new
  instruction against earlier decisions** — a sweeping phrase can overturn a
  specific choice.
- **A filler "okay" is not approval of a pending commit.** Ask for the explicit
  word; an ambiguous destructive word gets numbered readings, not action.
- **An "ok commit" relay carries the whole close-out**: checks by actor, one
  commit message, tick the item, cleanup in order, then the next item or "stop
  and wait". Write a backup step as "sync the backup clone by fetch +
  fast-forward from its side", never a push onto its checked-out branch.
- **Answer a pending approval in the same message as any new instruction.** A
  tweak folds into one commit; a different kind of job gets "commit what you
  have first".
- **A sibling that breaks a brief rule, discloses it, and names a legitimate
  source is reporting a bad rule** — fix the rule. Approve a parameter changed to
  pass a required case, and ask for the reason in the project log.
- **A question the owner's recorded spec already answers is yours to answer.**
  Low-stakes reversible choices: take a sound recommendation, tell the owner the
  alternative in one line. Ask first only when irreversible.
- **"Remembered the same way as <setting>" is a claim to grep**, not a feature.
- **A sibling that stops at a blocker did the right thing** — say so.
- **A constraint it cannot meet, measured and costed, asks for a decision**:
  measure the one variable it did not, and decide.
- **Before "ok commit?", check whether the fix overturns a rule the owner
  settled earlier** (grep the plan files); put both sides in two lines.
- **Verify the result yourself before saying it worked**, and name what the
  agent did well — the owner is deciding how much to trust it next time.

### Briefing an agent to produce a public-facing asset

Write the facts section yourself from the tool's SOUL, skills, README and
schema, and name one real record for the example ("leave a line out rather than
invent a value"). Narrow every safety constraint to the actual risk and name the
permitted substitute. Full procedure: `references/asset-brief-writing.md`.

## Skills by step in the SOUL

A skill in the index is a suggestion the model may skip, and the owner never
names skills. Name each agent's 2-7 must-load skills **in its SOUL at the method
step where each applies** — names only, the SOUL is paid every turn:

```
Skills by step, load each when you reach it, the owner never has to name them:
Research `research`; Spec `to-spec`; Tickets `to-tickets`.
```

- Pick by reading every skill's `description` against the SOUL's METHOD line,
  plus the irreversible gates (first push, publishing).
- A rule that must hold on every turn goes in the SOUL as text, not a name.
- One agent at a time with the owner's ok; prune off-role bundled skills in the
  same pass. Test: `grep -rhoE '\`[a-z-]+\`'` over its own skills and memories —
  a name referenced there must stay.

## Propagating standing rules across the fleet

When a convention changes, each agent reads a different channel: a skill in its
own profile, `~/.claude/CLAUDE.md` for Claude Code, and a machine-enforced guard
for anything a script can break. Channel table and the rule that every later
change must re-reach every channel: `references/fleet-rule-propagation.md`;
the guard recipe: `references/machine-enforced-guards.md`.

### Timing: do not interrupt a sibling mid-task

Decide by intersection: does any changed capability touch the step it is on?
Prove the change is invisible with greps over its SOUL, memories and the
project's docs, then deliver the news as a line in the plan file at the step
where it matters.

- **Already running the job? Queue the correction** as the next numbered brief,
  stating what carries over.
- **Three rejected passes on one deliverable** means the question is wrong:
  ask what already covers the need; stopping is often cheapest.
- **"I don't get how the UI works" after a build is a shape failure**: stop
  dispatching, agree a mockup with the owner, then one brief.
- **A running session's skill index is frozen at session start**: have the
  one-line explanation ready if it reaches for a removed skill.

### "Does agent A know what agent B did?"

Answer from the channels: (1) the project's log or roadmap — quote the entry;
(2) the sibling's own words that could only come from that file; (3) the files
themselves (`md5sum` on both worktrees). A project's identity absent from a
sibling's memory is the design working: it belongs in the repo.

## Judging a sibling's proposed next step

A sibling's "next" comes from the plan, which knows the order but not the
moment — judge it.

- **Do not freeze surface area before anyone used it** (translations, docs,
  assets from wording in flux); let the owner use the thing first.
- **Before "go use it for a few days", check how they launch it.** No launcher
  means give the exact two working lines, offer a removable shortcut, and plan a
  packaging phase.
- **A step that mixes categories** (UI + product logic) gets two commits.
- **New UI feature: shape before code** — a mockup in the real style showing
  where it lives, what you click, how it is undone. Check: placement where the
  need is seen; no jargon in UI copy; any action that cannot be undone is
  labelled and cheap to recover; the product's core promise (if everything
  previews, so does this); parity with the path it duplicates (same caps, same
  eligibility filter — a justified exception is the owner's pick, costs stated);
  state that survives closing the window.
- **A changed default of an existing command is a behaviour change**: flag it.
- **When a feature returns, grep the whole UI for the jargon just removed**;
  other hits go to the plan, not into the commit under review.
- **"I expect" in a shape note is a test to request**, with both outcomes
  pre-decided.
- **A speed-up is a go with three conditions**: same answers proven old-vs-new,
  before/after times at small and large scale on a copy, every caller named.
- **Check the feature against the case that motivated it**, and **judge a
  detector by what it does NOT fire on**; a group check needs a minimum group
  size; a threshold tuned on synthetic fixtures proves the mechanism only.
- **"Does it hold at scale?"**: split into engine, interface and accuracy, check
  each in code, recommend a measured phase.
- **Fence the real data.** Find every store and let the owner name the real
  one; record size, mtime and row counts of every learned table before dispatch
  and re-check after each report. For SQLite, note your own read-only queries
  (they touch `-shm`); a size jump with no new rows is the WAL folding in. The
  owner's app launched from the repo runs the sibling's uncommitted code: keep it
  closed while the sibling works.
- **Never forward screenshots of the owner's personal data**; describe in words,
  require fake fixtures.
- **"Does the tool already do X?"**: grep the code before relaying.
- **A request that breaks a project hard rule** goes as a shape with the
  conflict named (opt-in, plan-first, undo), plus which irreversible step to
  hold until it exists.
- **Losing track? Freeze new work and switch to a use-driven loop**: the owner
  uses the tool for a week or two, each blocker becomes one numbered line in a
  dated private fixes file (with the real-data baseline at the top), items go one
  at a time (shape → code → your check → commit on their ok). Put the cause with
  file:line in each item; a pre-existing bug found along the way is the next
  item, written at once with its repro.
- **Widening a fix into shared logic is a todo, not a yes.**
- **Hold a dependent agent until its input is on main**; one agent at a time on
  the same file.
- **Parallel worktrees**: decide by file overlap and by who reviews; a second
  lane doubles the owner's review load.

## Retiring a fleet agent

- **Separate retiring the CAPABILITY from cancelling the DELIVERABLE**, in
  writing, before anything irreversible. "Close" can mean a terminal, a session
  or the profile — ask.
- **A deleted profile is often recoverable**: a live session holds file locks,
  so the directory survives; removing the tombstone re-registers it:

  ```bash
  rm $HERMES_HOME/profiles/.deleted/<name>
  hermes profile list | grep <name>
  ```

  Never report a profile gone from the list alone — `du -sh` must say "No such
  file". After a restore, re-run `prompt-size` and recount its skills.
- **Archive what it learned, not what it rendered**: skills, SOUL, briefs, the
  approved artifacts; never caches or frames.
- **Carry its findings about OTHER projects** into their owners' plan files first.
- **A capability proven to work and then dismissed is a finished experiment** —
  say so in the archive note.
- **Its own open terminal blocks deletion**: ask the owner to close it, then
  verify the directory is gone.

### Winding down a cancelled job (the agent stays)

One closing message: the cancellation is about the deliverable, not the work
(name one thing done well); what you already cleaned, with paths, "do not
recreate it"; exactly three tasks (sweep its own leftovers from its working
window only, add missing lessons to its skill one line each, do not touch the
repo); a fixed-length report. Verify from disk before closing the session.

### Reporting on the sibling that stays

Re-derive from commits, plan phase headings and `git status`. Lead with the
commits the owner remembers approving. Surface uncommitted edits to a generator
whose output was not re-run — but read its last message first: work held back
for approval is closed by the owner's yes or no. A deliberately paused step is
not an open task; say why it is paused.

## Pitfalls

- **Do not repeat a sibling's claim as your own finding**; say what you re-ran.
- **A passing test count is not proof the tests ran** — check for skips.
- **Re-run a pipeline fresh in a scratch store** (data-dir env var or flag);
  cached stages prove nothing, and an edge flag against the real output dir
  overwrites real output.
- **Sabotage a guard yourself** and match each claimed failure mode to a proof.
- **Look at screenshots yourself**, and say in the go message that the shots
  stay until you have looked. A half-transparent panel was captured mid
  fade-in. For video, extract boundary frames; `md5sum` a loop's seam frames.
- **Prove a generated asset was derived, not retyped**: no hex literals in the
  generator source, `md5sum` of the token file copy matches the repo's.
- **When docs move between files, prove nothing was lost**: every non-blank line
  of `git show HEAD:<file>` present in the union of the new files, anchors
  resolve.
- **Check a completion report for what it did NOT commit**: ignored drafts and
  generators are in no backup (`git check-ignore -q <dir>`).
- **A blocker in another agent's plan, or stated from memory, may be stale**:
  re-derive from the tick marks; a closed prerequisite frees a waiting worker.
- **Offer the handoff, do not assume it.**
- **What a sibling uses or knows is on disk**: read its profile instead of
  relaying the question, and grep for an existing rule before asking the owner.
- **A short tool name may be a small local utility**, not the famous product.
- **Editing a sibling's skills needs the owner's say-so — then do the whole
  job**: `references/skill-consolidation.md`. `skill_manage` addresses only the
  active profile; use file tools for a sibling's files.
- **Pruning bundled skills: delete, then `hermes -p <name> skills opt-out`**, or
  an update re-seeds them; then grep its SOUL and skills for the deleted names.
- **Adding a capability is the same conversation as removing one**: consolidate
  superseded skills in the same pass.
