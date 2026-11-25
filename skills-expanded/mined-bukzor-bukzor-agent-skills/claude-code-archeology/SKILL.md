---
name: claude-code-archeology
description: "Agent MUST load on /claude-code-archeology, when a question is about what happened in a past Claude Code session (what was tried, decided, or lost), when recovering sessions after a crash or freeze, or before parsing anything under ~/.claude/projects."
---

# Claude Code archeology

`~/.claude/projects/*/*.jsonl` is the only durable record of most work
done here. It answers questions nothing else can -- what was tried and
abandoned, what a command printed before the machine froze, what was
decided in a conversation that ended without a commit. Treat it as a
primary source.

Never `grep` the raw JSONL. It matches JSON-escaped text, misses
anything split across content blocks, and prints a 4000-column line on a
hit. Use the tools below; they decode first.

## The tools

| command                                     | answers                                                     |
| ------------------------------------------- | ----------------------------------------------------------- |
| `claude-search PATTERN [--role talk] [--all]` | which session discussed this, with snippets                  |
| `claude-inventory [--days N] [--sh]`          | what was I working on; `--sh` emits resume commands          |
| `claude-branch-list FILE [--branches-only]`   | the file's tree, marking real rewind points                  |
| `claude-branch-extract [--as-session CWD]`    | linearize one branch into a new resumable JSONL              |
| `claude-jsonl-cwd FILE`                       | the directory a session ran in (needed to resume it)         |
| `claude-jsonl-path DIR`                       | the projects/ dir holding a cwd's sessions                   |
| `claude-jsonl-display < FILE`                 | render a transcript readably -- **on stderr**; stdout carries only a machine-oriented `result.result` line, if any, so `\| tail`/`\| grep` on stdout alone will not see it |
| `claude-jsonl-to-log < FILE`                   | same rendering, captured to a `.log` file beside it           |

## What it cost

> [!DRAFT] agent-authored 2026-09-16, vetoable.

`claude-tokens | claude-tokens-cost` writes one costed row per API
request. `claude-tokens-wire` reads the same calls off a mitmproxy
capture instead -- same schema, and it sees ~11% more requests than any
transcript does. `-histogram` groups them; `-params` fits the estimator
constants.

Dedupe on `(requestId, message.id)` is load-bearing, and is why these
totals can be added up at all: the CLI writes one record per content
block, each repeating that response's whole `usage`.

What the numbers mean -- the pricing multipliers, what the corpus cost,
how to estimate a task before running it -- is a body of findings with
its own standing, kept as a claim ledger rather than restated here:
`~/.claude/docs/dev/claims.kb/attention-costs.md`.

Library behind them: `claude_code_archeology.{session,search,inventory,
tree,format_short,branch_extract}` -- import it rather than re-parsing
when a question needs custom analysis:

```sh
uv run --project ~/repo/github.com/bukzor/bukzor-tools python - <<'PY'
from claude_code_archeology import session
PY
```

Every module is doctested; `uv run pytest` in that repo runs them.

## Format facts that bite

- **The file is a forest, not a log.** Records carry `uuid` and
  `parentUuid`; a rewind writes new records as *siblings* of the old
  continuation, and each compaction starts a new root. `--resume` and the
  rewind picker walk back from the newest record only, so abandoned
  branches and every pre-compaction era are unreachable in the UI --
  extraction is the only way back -- but fully present in the file.
  That's where "we tried that and it didn't work" lives.
- **A compaction root's parent is in a second field.** Its
  `compact_boundary` record has a null `parentUuid` and names the era it
  summarised in **`logicalParentUuid`**. Walk `parentUuid` alone and every
  pre-compaction era reads as abandoned -- which is right for the rewind
  picker and wrong for anything measuring what was thrown away. All 294
  boundaries here carry the field; missing it overstated abandoned-branch
  spend sevenfold, reporting 7.3% as 54%
  (`~/.claude/docs/dev/claims.kb/`, COMPACT_PARENT).
- **The `projects/<slug>/` name is not invertible.** The slug maps both
  `/` and `.` to `-`, so `prototype.chatfs/docs` and
  `prototype-chatfs-docs` collide. Read `cwd` from the records
  (`claude-jsonl-cwd`); never decode the directory name. Last value
  wins, since resuming from elsewhere rewrites it.
- **`type: user` is not "the user typed this".** Tool results are stored
  as user records. Distinguishing them (`role_of`, `is_user_text`) is
  what makes "what did I actually ask for" answerable.
- **Subagent transcripts live under the parent session**, in
  `projects/<slug>/<session-id>/subagents/agent-<id>.jsonl`, with every
  record marked `isSidechain: true`. Nothing globbing `projects/*/*.jsonl`
  sees them -- not `--resume`, not the tools above unless pointed at the
  file. They are shaped like sessions otherwise, so
  `claude-branch-extract --as-session CWD` re-homes one as a session of
  its own: the marks come off, `cwd` moves to the directory the work
  belongs in, and it resumes like anything else. What does not come
  back is the agent definition it ran under -- the promoted session
  gets the plain system prompt and the session's own model.
- **User-role text is often harness-injected**: compaction summaries,
  skill preambles, command wrappers, `[Request interrupted...]`. Filter
  it before drawing conclusions about what a person said.
- Files are append-only, so a frozen or killed session loses nothing but
  the in-flight turn. A crashed write can leave one malformed line;
  parse defensively rather than failing the whole file.

## Rewinding to a state the picker will not offer

Extraction hands you a whole branch and `/rewind` cuts it back, and
between them that is the whole recipe:

1. `claude-branch-list FILE` (or a `claude-search` hit) names any record
   on the branch you want -- a locator, not a boundary.
2. `claude-branch-extract FILE <uuid>` writes a new session holding that
   branch through its tip; add `--as-session <cwd>` when the source is a
   subagent's.
3. `cd <cwd> && claude --resume <new-id>`, `/rewind` to the prompt of
   yours the state sits behind, then send the turn again.

**Extraction running forward to the tip is wanted, not a gap.** Naming
the record and stopping there is `/rewind`'s job, done later and better:
the picker offers every prompt of yours, and taking one drops the later
era from context. An extraction-time cut was tried and removed for
duplicating it. The residue -- dropping a tail mid-turn, where no prompt
of yours precedes the cut -- is `claude-jsonl-truncate`'s job, in place
or to a fresh id (`Skill(claude-code-surgery)`), not a second flag
here. Do not re-add one.

Two things do not come back with it: the repo state the dropped turn
worked against -- version control is the only rewind for that, so commit
each step of anything you may want to re-run -- and, for a promoted
subagent, its agent definition. Re-asking without rewinding is not the
same experiment: the first answer stays in context, and what comes back
is a revision of it.

**A subagent is not rewound by rewinding its caller.** Its transcript is
a separate append-only file, bound to the spawning tool-use by
`subagents/agent-<id>.meta.json` and resumed through its `agentId`, and
the file-history records backing `/rewind` cover the repo only, never
`~/.claude/projects`. So a caller cut plus a re-sent turn reaches a
subagent that remembers everything. Cut both files, or -- better for
anything you may want to replay -- run the other side as its own session
and drive it with `SendMessage`.

In-place surgery -- cutting a poisoned tail so the *same* agent id
resumes, clearing a `stoppedByUser` refusal in the meta.json -- is
`Skill(claude-code-surgery)`.

## Recovery after a crash or freeze

`bin/dead-sessions` (beside this file; stdlib only, read-only) lists what
the crash killed. `~/.claude/sessions/<pid>.json` is the live-session
registry: an entry outlives a crash, and pid plus `procStart` tell a dead
session from a reused pid. For each dead session it prints the cwd, the
resume command, the last prompt and reply, tool calls that never got a
result, and sub-agents whose `meta.json` lacks `finished`.
`claude-inventory --days 2 --sh` casts a wider net: every recent session,
registered or not.

1. Sort the sessions into three kinds:
   - *interrupted*: `busy`, a tool call with no result, or an unfinished
     sub-agent;
   - *idle with uncommitted work*: its last reply says so;
   - *clean*.

   Run `git status` and `git log` in each cwd: a dead sub-agent may have
   left partial edits, or none.
2. Resume the interrupted ones in new tmux windows, sending no prompt:
   `tmux new-window -d -n NAME -c CWD`, then
   `tmux send-keys -t NAME 'claude --resume ID' Enter`. Check that each one
   came up with `tmux capture-pane -p -t NAME`. Never send a message to a
   resumed session: a coordinator may relaunch sub-agents that have side
   effects. Give the user a suggested message instead, saying what died,
   when, and the state of the tree.
3. A dead sub-agent's result never reaches its parent, so the parent has to
   relaunch it. The CLI says so on resume ("didn't finish before the
   previous session ended").
4. The crash time is the newest write across the transcripts and
   `~/.claude/backups/`, not the boot time (`/proc/uptime`).
5. When a session's useful work is on an abandoned branch,
   `claude-branch-list` it and extract the branch rather than hunting
   through the live chain.

## Mining a session for evidence

When the transcript is evidence about an incident rather than work to
resume, file it like any other perishable source -- capture the extract
into the investigation's `evidence.kb/`, don't re-read the JSONL at
every question. See `Skill(incident-forensics)`.

Two habits keep this honest:

- Quote what the record says, and cite `file:line` (the tools print line
  numbers for exactly this). A transcript is a record of what was
  *claimed* at the time, which is not the same as what was true.
- A session's own summary of itself -- compaction summaries, `ai-title`
  records -- is a lossy secondary source. Check it against the records
  it summarizes before repeating it.
