---
name: precedent
description: Remember and reuse the user's architectural, business, and tooling decisions across every project, in a queryable graph. Use whenever the user settles a non-trivial choice (database, framework, auth, deployment, pricing, process) so it gets recorded; starts work in a project you have not briefed on, including one whose decisions are only visible in its manifests, CI and docs; weighs options or asks "which should I use" or "what did I do last time"; says a past choice was a mistake, bit them, or they would not repeat it; knowingly departs from how they usually do it; or asks what they already decided, whether a choice is consistent with their other projects, or what decisions they still owe this project. Trigger it even when the user does not mention decisions or the graph. If no PRECEDENT block is in context, run uv run <this skill's directory>/scripts/precedent.py standing-orders before your first shell command and follow what it prints.
---

# Decision graph

This is Claude Code's adapter onto `precedent`, a decision graph that also
reaches Codex and Cursor (see the repo's top-level README for the other
install channels). The user's decisions are scattered across dozens of repos
and two years of conversations they no longer remember. The graph keeps them
in one place, so a choice made in one project informs the next one, from
whichever agent looks it up.

Everything goes through one script, shared by every adapter. It handles
locking, the append-only journal, project typing, and the inference queries,
so you write no Cypher for normal work.

`<skill>` below is this file's own directory (`adapters/claude/skills/precedent/`
in the repository, or wherever it was installed: `~/.claude/skills/precedent`,
or an ACR `acr__…__precedent` directory). The script ships inside it:

```bash
uv run <skill>/scripts/precedent.py <command> [flags]
```

The session brief prints the resolved path — prefer that over recomputing it.

`uv` fetches the dependency on first run — there is no install step. If `uv` is
missing, run it with a Python 3.12+ that has `graphdblite` (a venv:
`python -m pip install graphdblite`), or `pipx run` — the README's "Without uv"
lists both. Keep the script beside its `precedent_cli/` directory.

## The task skills beside this one

Nine skills cover the daily paths without going through this document. They are
directories beside this one, so every install channel ships them: a plugin
install discovers them by convention, and `acr realize` writes each into the
agent's own skills directory.

| Skill | Does |
|---|---|
| `precedent-prime` | Load this project's decisions and precedent into context |
| `precedent-record` | Record a decision that was just settled |
| `precedent-check` | Prior decisions on a topic, plus a conflict verdict |
| `precedent-tag` | Show or set this project's tags |
| `precedent-analyze` | Read an existing project and record the decisions visible in it |
| `precedent-diverge` | Record that this project departs from precedent, and why |
| `precedent-suggest` | Decisions this project still owes |
| `precedent-regret` | Mark a repeated choice as a mistake, inverting its precedent |
| `precedent-maintain` | Contradictions, tag drift, dead projects |

They are entry points, not a replacement for the judgment below — each one
points back here. `precedent-prime` overlaps with the `SessionStart` hook and is
worth running by hand after changing directory, or after recording something
that should now inform the rest of the session.

Each fires on its own description, so the user does not have to name it. Claude
Code also takes them as slash commands; Codex takes them with a `$` prefix.

## Standing orders

The session-start hook prints the standing orders automatically, in every
directory, empty ones included. To see them without a hook, or from another
agent:

    uv run <skill>/scripts/precedent.py standing-orders

Every active principle prints as part of them, after the fixed orders. Follow
those as orders, not context.

You are reading this once, and then the conversation continues for another hour.
Everything below has to survive that. Treat these as active for the rest of the
session, not as a script you run now and forget:

- **Test the rationale against the case in front of you.** A recorded
  decision is an answer plus the conditions that produced it. Read the
  `--rationale`, name the condition it depends on, and say whether that condition
  holds here. Reporting precedent without doing this is the most common way to
  be confidently wrong — it launders a past judgment into a present one.
- **When a choice gets settled** — offer to record it, in the same message it was
  settled. Not at the end of the session, which never arrives.
- **When you notice yourself saying "I'd suggest X"** — that is the trigger. Check
  first, then suggest.
- **When a project you are working in has nothing recorded** — offer to backfill
  it once (`precedent-analyze`), then drop it. An empty project is why precedent
  is thin everywhere else; nagging about it is why the user turns the skill off.

Nothing here is reached by the user typing a command. They will say an ordinary
sentence and move on, and you are the one who has to notice:

| What the user says | What it is | What you run |
|---|---|---|
| "let's go with X", "we'll use X", the argument stops | a decision | `record` |
| "what did I use last time", "which should I use" | a question for the graph | `check` |
| "X was a mistake", "X bit us", "never again", "I regret X" | a lesson, not a new decision | `regret` |
| "I know I usually do X, but here…" | a knowing exception | `record --despite` |
| "actually, for this project, X now" | a replacement in one project | `record --supersedes` |
| "that's not what I meant", "the title is too narrow", "reword that" | a rewording, not a new decision | `amend` |
| "none of this repo's decisions are in there" | a backfill | `precedent-analyze` |

Three of these get confused. Changing your mind in one project is `--supersedes`:
the old choice stays a norm everywhere else. Deciding the *pattern* was wrong is
`regret`: it marks every project that made that choice and stops the graph
arguing for it again. Deciding the *words* were wrong is `amend`: nothing about
the choice changed, so nothing is superseded and no second entry appears. Ask
which one they mean when the sentence is ambiguous — "we're moving off mongo" is
either of the first two, and "that's not really what I decided" is usually the
third rather than a new decision.

Offer, do not act. Draft the command, show the one-line summary, run it when
they confirm. The one exception is an explicit settlement, covered under
"A decision just got made": "decided", "settled", "let's go with X" is the
confirmation.

The failure mode this guards against is not refusing to use the graph; it is
using it once, at the start, and then spending the rest of the session
confidently recommending things the user rejected two years ago.

If a `SessionStart` hook is installed (see *Priming*, below), the project brief
is already in your context and you can skip the `brief` step — but the check-
before-you-recommend and record-when-settled orders still apply, because no hook
can know when a decision happens mid-conversation.

## The moments this skill exists for

### 1. Starting work in a project

Run this before your first substantive answer in a project you have not seen
this session. It costs one command and tells you what the user already settled
here and in projects like this one.

```bash
uv run <skill>/scripts/precedent.py brief --project .
```

Lead with what's relevant, not the whole dump. If the brief shows precedent that
contradicts what the user is about to do, say so now rather than after they've
written the code.

### 1a. The project has history, but the graph does not

A repo older than this skill has its decisions in the manifests, the CI config
and the README, and none of them are queryable. The brief says as much: in a git
repo with no recorded decisions it prints *nothing recorded here yet* instead of
staying silent.

Offer `precedent-analyze` — once, in one sentence, with the two or three
decisions you can already see named so the offer is concrete. If the user says
no, or ignores it, it does not come up again this session. The backfill itself
is the command's job, and its one hard rule is worth repeating here: a rationale
you inferred is quoted back to the user in two years as their own reasoning, so
it comes from evidence (cited) or from them, never from you.

### 2. The user is choosing something

When they weigh options — a database, a queue, an auth provider, a pricing
model — check before you recommend. Your own opinion is worth less than what
they already decided and lived with.

```bash
uv run <skill>/scripts/precedent.py check --topic persistence --chose postgres
```

Two verdicts are worth interrupting for: `CONFLICT` (they rejected this exact
option before — quote the recorded reason) and `DIVERGENCE` (they chose
differently in two or more comparable projects).

Neither is a verdict on *this* case. Every rationale carries a condition, and
your job is to check whether it still holds:

> Recorded: *"SQLite locks up once webhook handlers run concurrently"* — chose
> Postgres, rejected SQLite, in three bots.
>
> This project: a single-user gym tracker.
>
> The condition is concurrent writers. A single-user bot does not have them, so
> the reason that produced the precedent does not reach this case. The
> precedent is still worth knowing — it says you will want Postgres the moment
> this stops being single-user — but it does not decide today.

That is the whole job. An answer that surfaces the precedent, quotes the
rationale, and then endorses it without asking whether the condition applies has
done the lookup and skipped the thinking. Consistency is usually right and
sometimes exactly wrong; say which you think it is, and why, then leave the
decision with them.

Where a precedent is weak — one project rather than three — say so. Three bots
agreeing is a pattern; one bot is a data point, and presenting them with equal
weight overstates what the graph actually knows.

### 3. A decision just got made

When the conversation settles something that will still matter in six months,
record it. Draft the command, show the user the one-line summary, and write it
once they confirm. Do not narrate the graph mechanics.

```bash
uv run <skill>/scripts/precedent.py record \
  --title "Postgres for the bot's state" \
  --rationale "Already run it for two other services; SQLite loses on concurrent writers" \
  --scope architecture --topic persistence \
  --chose postgres --rejected sqlite,mongo --project .
```

`--rationale` is the field that matters. In two years the *what* is recoverable
from the code and the *why* is not. `--rejected` is what powers the CONFLICT
verdict later, so record the alternatives they actually turned down.

**`--topic` names the question, never the project.** A tag says what kind of
project this is (`java`, `telegram-bot`, `frontend`); a topic says which
question the decision answers (`persistence`, `backend-framework`). Topics
match one by one, so a tag added as a second topic narrows nothing — it opens
a bucket where Quarkus, a Java formatter and an import style all "answer" the
same question, and `check` reports a false DIVERGENCE between them. Test it
before writing: *would this project hold a second live decision under the same
topic without contradicting the first?* If yes, the topic is an area, not a
question — make it specific. When a qualifier is needed, put it inside one
topic (`frontend-framework`, `java-formatting`), never beside a bare noun
(`framework` + `frontend`). Prefer a topic already in use for the same
question; `record` prints a note when a topic is also a tag.

Ask before writing, not after. A wrong entry is worse than a missing one,
because it will be quoted back as precedent. **An explicit settlement is the
answer to that question:** when the user says "decided", "settled", "going with
X", record it in the same turn and report it in one line. Do not draft and wait.
If one piece is missing (no stated reason for a `--despite`, say), record what
they gave and ask for the missing piece at the end. Asking again only when
nothing was settled is what keeps a question from turning into a record.

**Recording is a side effect, never the reply.** People settle a decision and
move on in the same breath — *"ok, SQLite with litestream, now let's talk about
the handler structure"*. The handler structure is the deliverable. Recording is
a line of admin that happens on the way past:

> Recorded: SQLite + Litestream for state, systemd for deploy. Worth knowing
> that SQLite was rejected in the other three bots over concurrent handlers —
> single-instance here, so it likely does not bite.
>
> On handler structure: *[the actual answer]*

One or two lines of bookkeeping, then the answer. If your reply is mostly graph
mechanics, or if it ends by asking a question back instead of answering theirs,
you have inverted the job. Where a real ambiguity blocks recording, record what
is unambiguous, answer the question, and raise the ambiguity at the end.

**What is worth recording:** anything they would have to re-derive later — a
technology choice, an architectural boundary, a business or pricing rule, a
convention they intend to keep, a deliberate rejection. Include the ones they
argued themselves out of; a rejection with a reason is a first-class decision.

**What is not:** anything the code already states plainly, one-off fixes,
choices with no alternative, and preferences that will not outlive the session.

### 3a. When precedent does not simply apply

Four different things get confused with each other, and they want different
records. Pick by what is actually true:

| The situation | What to run | What it changes |
|---|---|---|
| The precedent is sound, but **this project is genuinely different** | `record --despite "<why this project differs>"` | Warning is answered here, and only here |
| The choice was right then and is **wrong now, in this project** | `record --supersedes <id>` | Old decision marked superseded, reasoning kept |
| The choice was **wrong everywhere**, and you repeated it | `regret --topic … --chose … --because "<lesson>"` | Every instance marked regretted; the verdict inverts |
| The choice was right — the **record of it reads wrong** | `amend --id <id> --title "<better words>"` (or `--topic` to refile it) | Only the wording or filing; no second decision, no supersession, id unchanged |

The first is the one people skip, and skipping it is expensive. Diverge without
recording why and the graph reports `DIVERGENCE` in that project forever — a
warning that is correct, unanswerable and permanent, which is exactly how a
useful signal becomes noise the user learns to scroll past.

The fourth is the one to reach for whenever the correction is to a description
rather than to a choice, and the cheap mistake is superseding instead. A
supersession writes a second decision and makes `check` carry both — an
assertion that the call was revisited. For a rewording that history never
happened, and it is asserted in the line `check` quotes first. Amend takes
`--title`, `--statement`, `--rationale` and `--topic`. `--topic` replaces the
whole topic set and is for a decision filed under the wrong question, such as a
project tag used as a topic. A different option is a different decision, so
that really is `--supersedes`.

```bash
uv run <skill>/scripts/precedent.py record --project . \
  --title "SQLite for the CLI" --topic persistence --chose sqlite \
  --rationale "embedded in the binary; there is no server to run one against" \
  --despite "this ships as a single-file CLI, so the operational argument for Postgres does not exist here"
```

Afterwards `check` in that project reports *"DIVERGENCE from 'postgres'
(3 projects) — acknowledged here: …"* and leaves it at that. Everywhere else the
plain warning still fires, because the exception was about this project, not
about the precedent.

### 3b. A choice you repeated turns out to have been wrong

Repetition is what gives precedent its weight, which is exactly the problem when
the repeated thing was a mistake. Without saying so, `check` reports *"you chose
mongo in eight projects"* as a strong norm — and argues for a ninth.

```bash
uv run <skill>/scripts/precedent.py regret --topic persistence --chose mongo \
  --because "schema drift made every migration a manual rewrite; we spent more on backfills than the schema-free start ever saved" \
  --instead postgres
```

Every active decision that made that choice is marked `regretted` in one command,
and the verdict inverts:

```
REGRET: you chose this in 8 project(s) and later concluded it was a mistake —
   "schema drift made every migration a manual rewrite ..."
   you now prefer: postgres
```

Nothing is deleted. The eight decisions keep their original rationales, because
the fact that a reason looked good eight separate times is the most valuable
thing in the record — it is what tells you the lesson was expensive and the trap
convincing. They simply stop counting as a norm, so `brief` and `suggest` no
longer offer that option, and the lesson shows up in every project's brief.

Reach for this when the user says a past choice was a mistake, or when they are
undoing one in the current project and the same reasoning applies elsewhere. Ask
first — the scope is every project at once, and a regret recorded in irritation
is hard to distinguish later from one recorded in judgment.

### 4. Which decisions are still missing

```bash
uv run <skill>/scripts/precedent.py suggest --project .
```

Two inferences, both grounded in what the user actually did:

- **Coverage gaps** — topics settled in two or more projects of this type but
  open here. These are decisions they owe this project and have not made yet,
  which is exactly the kind of thing nobody notices until it bites.
- **Principle candidates** — the same answer reached in three or more projects.
  That is no longer a per-project decision; offer to promote it.

```bash
uv run <skill>/scripts/precedent.py principle --id persistence-postgres \
  --statement "For persistence, use Postgres unless the workload is single-writer."
```

A principle is a claim about the future, so ask before creating one. Repetition
is evidence, not consent.

A principle with no `--topic` is a global instruction about how the agent
works, such as "never wait on a process with `pgrep -f`; it matches its own
poller". The user adds these when they see an agent fail the same way
repeatedly: when they ask, draft the command, show it, and run it once they
confirm. Never offer one unprompted.

When a principle stops holding, retire it with the reason. It stops printing
and stops reaching `check`, and stays in the graph so `suggest` does not offer
it again. Re-recording the same id brings it back.

```bash
uv run <skill>/scripts/precedent.py principle --id persistence-postgres \
  --retire --because "we moved state to the managed KV store"
```

## Tagging a project — your job, not a lookup table

Precedent is found by **tag overlap**, so tags are what make "what did I do in
my other backend services" work at all. A project carries a set of them:

```bash
uv run <skill>/scripts/precedent.py tag --project .                       # see the vocabulary
uv run <skill>/scripts/precedent.py tag --project . --add backend,java,distributed
```

A single type would force a false choice. A service is not `backend-api` OR
`java` OR `distributed` — it is all three, and which of them a past decision
rhymes with depends on the decision. Persistence choices travel along `backend`;
build and dependency choices travel along `java`; consistency and retry choices
travel along `distributed`. Overlap also gives you a gradient instead of a
binary: `brief` lists the closest projects with the count of shared tags, so a
sibling sharing four tags outranks one sharing a single generic tag, and you can
see which tags did the matching.

Nothing is inferred from the project's contents. An earlier version tried, and
keyword matching cannot be made correct: a Rust CLI named `nextgen` was typed
`web-frontend` because "next" appeared in its description, and `react-native`
matched `react` before it could match itself.

There is no list of known build files either — `brief` and `tag` just show the
directory's top-level contents, so `build.zig`, `shard.yml`, `BUILD.bazel` or
whatever appears next year is as visible as `package.json`. You are already
reading the project; classify it from what is actually there.

### Reuse tags; the graph will stop you if you don't

Matching is exact string equality, so `tgbot` beside an existing `telegram-bot`
hides half the history from the other half — silently, at the moment it happens.
Different agents in different sessions reach for different words for the same
thing, so this is the normal case, not an edge case. `tag --add` therefore
**refuses** a tag resembling one already in use, exits non-zero, writes nothing,
and prints the vocabulary so you can choose:

```
refusing to create the tag 'tgbot': it looks like 'telegram-bot', already in use.
  tags in use: backend, java, telegram-bot, distributed
  reuse one:   precedent.py tag --project . --add telegram-bot
  or if it really means something different:
               precedent.py tag --project . --add tgbot --new-tag
```

It catches both shapes drift takes: spelling variants (`data_pipeline` /
`data-pipeline`) and abbreviations (`tgbot` / `telegram-bot`), which share no
word at all. `--new-tag` records the pair as deliberately distinct so the
maintenance report stops proposing a merge that was already considered.

Prefer several small orthogonal tags to one compound name. `backend` + `java` +
`distributed` is better than `distributed-java-backend`: each part is reused by
other projects, which is what makes overlap meaningful, and short common words
are ones every agent spells the same way.

### Monorepos: tag the module, not the repo

A repository holding a Java backend and a Python Slack bot is two projects, and
they should not lend each other precedent. They already are two projects: the
key is the absolute path, so `/repo/backend` and `/repo/slackbot` are distinct
entries with their own tags. Containment falls out of the path — no extra
schema, nothing to keep in sync.

```bash
uv run <skill>/scripts/precedent.py tag --project ./backend  --add backend,java
uv run <skill>/scripts/precedent.py tag --project ./slackbot --add bot,slack,python
uv run <skill>/scripts/precedent.py tag --project .          --add monorepo,internal
```

Three consequences worth knowing:

- **Record against the narrowest directory the decision is about.** A choice
  about the bot's storage belongs to `./slackbot`, not the repo root. `brief` at
  the root lists the modules and reminds you.
- **Repo-level decisions reach every module.** CI, branching, release process and
  licensing are recorded once at the root and show up in each module's brief
  under *inherited from enclosing projects*. This is the reason to tag the root
  at all.
- **Modules inherit the root's tags, marked with `*`,** and those tags help a
  module find kin in other repos of the same shape. They do not make sibling
  modules kin with each other: a Java backend and a Python bot share only
  `monorepo` and `internal`, which say nothing about the work, so neither
  appears in the other's precedent. Two genuinely similar modules still match,
  because they share real tags.

Enclosing and contained projects are shown as structure rather than precedent —
they are the same codebase, and counting them as "closest projects" would crowd
out comparable work elsewhere.

### Repairing drift that already happened

`maintain` reports suspected pairs, and one command repairs them:

```bash
uv run <skill>/scripts/precedent.py tag --merge tg-bot --into telegram-bot
```

Every project carrying the old tag is retagged, the merge is journalled, and
`rebuild` replays it.

A project that split in two — a ghost from a mistyped `--project`, or an old
node `maintain` reports — is joined the same way, once the user agrees they
are one project:

```bash
uv run <skill>/scripts/precedent.py merge-project --from "<id from maintain>" --into .
```

Decisions, tags and paths move; decision ids do not change; the merge is
journalled. Any contradiction it creates is printed — drive it to a supersede
or a `--despite`. `--project` must be a directory: pass `.`, never a name.

An untagged project still records decisions perfectly well; it just never
surfaces as precedent anywhere, and `brief` says so and lists the tags on offer.
Tag it when you know what it is — guessing early is worse than waiting.

## Keeping it healthy

```bash
uv run <skill>/scripts/precedent.py maintain          # report only
uv run <skill>/scripts/precedent.py maintain --apply  # also delete orphan nodes
```

Reports contradictions (one project, one topic, two live answers), projects
whose path no longer exists, and orphan nodes. Contradictions are for the user
to resolve — record a new decision with `--supersedes <old-id>` rather than
editing history. Superseded decisions stay in the graph; they are the record of
what the user used to think, which is the part that explains the current design.

Run this when the user asks for a cleanup, or when a `check` result looks
self-contradictory.

## Priming

Prose can be forgotten by turn 40; a hook cannot. `hooks/session-start.sh` is a
`SessionStart` hook that runs `brief` for the working directory and injects the
result, so every session opens already knowing what the user decided here and in
comparable projects. It stays silent when the graph has nothing to say about the
directory, so it costs nothing in projects with no history.

Wire it in `~/.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      { "hooks": [ { "type": "command",
                     "command": "$HOME/.claude/skills/precedent/hooks/session-start.sh" } ] }
    ]
  }
}
```

Subagents do not see a SessionStart hook's output. The Claude Code plugin also
runs the hook as `session-start.sh --subagent` on `SubagentStart`, so each
subagent gets the brief for its own working directory and the standing orders
(see docs/setup.md to wire it by hand). Where that hook is not installed, run
`standing-orders` and `brief` before delegating and copy every precedent that
binds the task into each subagent prompt.

The hook covers recall. It cannot cover capture — nothing outside the
conversation can tell when a decision was made — so the standing orders above
remain the only mechanism for recording.

## Where it lives, and why it is safe

```
~/.local/share/precedent/
├── journal.jsonl   append-only, fsync'd, one line per decision — source of truth
└── graph.db        graphdblite graph — a queryable index
```

To keep it somewhere else — a synced folder, an encrypted volume, a private git
checkout — point `init` at that directory. It moves an existing store there and
leaves a pointer file at the default path naming it, so the hook and every
slash command keep working unchanged:

```bash
uv run <skill>/scripts/precedent.py init ~/Sync/precedent
uv run <skill>/scripts/precedent.py init          # where does it live right now?
```

Prefer this over `PRECEDENT_HOME`: the env var is not set in the SessionStart
hook's environment, so exporting it hides the store from priming. It refuses to
merge two populated stores — concatenating the journals and running `rebuild` is
a deliberate act, not something a path flag should do behind your back.

The journal exists because the graph engine is young (0.1.x) and because it
keeps the engine replaceable. If the graph is ever corrupted or the engine is
abandoned, `precedent.py rebuild` replays the journal into a fresh graph and
nothing is lost — that is how the store moved off Grafeo, a rebuild rather than
a migration. The journal is plain text, so it also diffs and belongs in a
private git repo if the user wants history.

Concurrent sessions are not coordinated by this tool and do not need to be.
There is no lock: graphdblite serialises writers through SQLite, waiting 5
seconds before failing loudly rather than dropping a write. Claude Code, Codex
and Cursor may all be recording at once. `selftest` measures that on Linux,
macOS and Windows rather than assuming it, because the previous engine lost
half of 120 concurrent writes in silence.

A store written before that change keeps `graph.db` as a directory; the first
command that records replays the journal into the new engine and then deletes
the old graph, so an install that predates the swap cannot keep writing to a
store nothing else reads. It is kept only when the replay could not read every
journal entry. Never bypass the script to open the graph directly.

```bash
uv run <skill>/scripts/precedent.py rebuild    # replay journal into a fresh graph
uv run <skill>/scripts/precedent.py --home /tmp/precedent-selftest selftest   # verify the install still works
```

`--home` is not optional on `selftest`: without it, the check enumerates every
real Project node in the live store and shells out to `git` in each one's
directory — expensive and, on a store with stale or removed project paths,
liable to fail outright. Point it at a scratch directory.

## Escape hatch

For a question the subcommands do not answer, query the graph directly. The
schema is in `references/schema.md` — read it before writing Cypher.

```bash
uv run <skill>/scripts/precedent.py cypher "MATCH (d:Decision)-[:CHOSE]->(o:Option {name:'postgres'}) RETURN d.title AS t"
```

Prefer a subcommand where one fits. Ad-hoc Cypher is easy to get subtly wrong,
and a wrong answer here is quoted back to the user as their own history.
