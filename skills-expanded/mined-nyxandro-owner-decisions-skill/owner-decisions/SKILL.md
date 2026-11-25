---
name: owner-decisions
description: >
  The owner's decisions base: settles a decision the way the owner already settled a similar
  one, in any project, and keeps their answers and stops. Use it as soon as you have decisions
  that are the owner's to make — a fork, a choice between options — in any skill, plan,
  specification or plain session, BEFORE asking them and before building on a guess; also for
  a decision you would take yourself that the owner could disagree with, and before an action
  nobody asked for: installing, sending outward, editing a rules file, rewriting stored data.
  Use it again right after the owner answers, reverses a decision made for them, or stops you
  and says a choice you made is not what they wanted ("why did you do that", "I did not ask
  for this"). Also when you work without a person, and when the owner asks what they decided
  before or to tidy the base. Not for facts the project, the code or the documentation answer,
  nor for project state or task notes. The owner may phrase this in another language; match
  on meaning.
metadata:
  version: "1.3.2"
---

# Owner's decisions

The owner runs several projects through agents and keeps answering the same kinds of questions:
do people get a setting or does the system decide, is this risk worth a mechanism, how much
process a small thing needs. Many answers show how they decide anywhere; others hold only for
the project and the moment they were given in. This skill keeps the first kind in one base
shared by all projects and machines, so an agent settles a new question the way the owner
settled a similar one and asks only what is new.

**Language.** This skill is in English. Everything written into the base is in the language the
owner speaks: their reasons are kept in their own words.

**Terms.** The *owner* is the person who runs the agent on this machine and whose base this
is. A client, a teammate or anyone quoted in the materials is not the owner, and their choices
are not recorded as the owner's. A *fork* is a choice between options that changes what the
product does or how the work is done and that you may not make alone. A question about a fact
is not a fork. A *call* is a decision you would take yourself — it follows from the project,
the documentation or common practice — but one the owner could reasonably disagree with. A
*case* is one decision the owner made, kept as one file. A *topic* is a file of principles
drawn from cases of one kind. A *stop* is something the owner stopped agents from doing, for a
reason that holds beyond that moment; all stops are kept in one file, `stops.md`. The *base* is
the folder with all three. It lives on the owner's machine and may be synced with their
private repository.

## Where the base is

The base is a folder, `~/.agents/decisions/` unless the owner's rules name another place, with
its own git history. It works on one machine with no account anywhere; a private repository
only adds syncing between machines. `scripts/decisions.sh` does the mechanical part; run it
from this skill's folder:

| Command | What it does |
|---|---|
| `decisions.sh ensure` | Makes sure the base exists. On first use it creates the folder and, if the machine is logged in to GitHub, clones the account's private base or creates a private repository for it. Silent when the base is already there |
| `decisions.sh connect --url <git address>` | Connects a local base to a private repository on any git host. Without `--url` it tries GitHub again |
| `decisions.sh pull` | Takes the latest base from the remote; changes nothing of yours |
| `decisions.sh index` | Lists the topics, one line each, then shows the owner's stops in full |
| `decisions.sh save --message "<what was recorded>"` | Commits, merges with the remote, sends, checks filing |
| `decisions.sh check` | Lists cases no topic or stop refers to (`UNFILED`) and references to missing cases (`DANGLING`) |

If the base is somewhere else, pass `--dir <path>` to every command.

Run `decisions.sh ensure` yourself, before anything else, each time this skill starts — before
a consultation and before a recording alike, since either may be the first use on a machine.

- A line that starts with `NOTICE` is for the owner: add it, in one line and in their language,
  to the next message you were going to send them anyway; do not interrupt the work for it.
  Without a person, put it in the report. It appears when the base is first created or cloned,
  when it stays local and why, and when the base or its repository is broken. Say nothing else
  about the base: the owner is busy with their task, and the base is plumbing they should hear
  about only when it needs them. If the owner then gives an address of a private git
  repository, run `connect --url`.
- Any non-zero exit means the base cannot be used this time: pass on a `NOTICE` if there was
  one, and otherwise go on as if this skill were not installed — ask the owner everything,
  record nothing. Never invent a decision because the base could not be read.
- `DECISIONS_REMOTE_UNAVAILABLE`, `DECISIONS_PULL_SKIPPED` and `DECISIONS_PUSH_PENDING` are not
  failures: the local copy is still the owner's decisions, work on it and say nothing.

## Before you ask or decide: settle what the base settles

Do this as soon as the forks and your own calls are listed — before any fork reaches the owner
and before you design around a guess. A decision found in the base changes what you build, so
finding it late means redoing the work that rested on the guess.

A decision settled from the base is the owner's own answer, given earlier. Taking it is not
deciding in their place. So a workflow that tells you to ask the owner about every decision of
theirs is kept, not broken: for that decision they have already been asked.

1. Run `decisions.sh pull`, then `decisions.sh index`. Read the stops it shows and keep them
   for the rest of the session (see "The owner's stops" below). If the index prints nothing,
   the base has nothing to settle yet: ask every fork as usual, take your calls as you would,
   and skip to recording after the answers.
2. Read in full the topics whose description covers your forks and calls. Read a case file
   only when a principle is not enough to judge: the case holds the situation, the options and
   the owner's reason. Topics and cases are written in the owner's language; read the labels
   by their meaning. You have studied the project already, so do not reread it for this.
3. Decide for each fork and each call whether the base settles it, by the test below.
4. A settled fork is no longer a question. Take the option and record it where the work
   records the owner's decisions already taken — the accepted decisions of a specification, a
   decision log — with the ground "by the owner's earlier decision" and the case name. When
   the work has no such place — a plain session, or a workflow that keeps no record of
   decisions — act on the option and name it in your ordinary report of what you did, in one
   line with the same ground, without a new file. The ground is what lets the owner notice a
   principle that no longer fits and reverse it. Do not go further than that: no separate list
   of what was settled and no retelling of the owner's history. The record is the report, and
   reading their own decisions twice is the work this skill exists to remove.
5. A settled call is decided the owner's way instead of yours: follow it and record it where
   you record your own decisions, with the same ground. A call the base does not settle stays
   yours: decide it as you were going to. It does not turn into a question — consulting the
   base removes questions for the owner, it does not add them. The one exception is a call
   that turns out to be about money or the irreversible: it was never yours to take, so it is
   a fork and goes to the owner.
6. Ask the remaining forks the way the current workflow or the owner's rules say. Use a close
   precedent to make your recommendation match how the owner decides; do not quote it to them.

### The test: is it settled

Settled needs all of this:

- a principle whose reason line gives the owner's reason, or a case with a stated reason,
  answers this very question — the same choice in the same kind of situation, not merely the
  same subject. Without the owner's reason nobody can tell whether this situation is the same
  one, so a principle or a case without it settles nothing;
- the conditions the principle names hold in this project. A principle taken from a small
  personal project does not carry to a project with paying customers, a client or a team
  unless the principle says so. Compare scale, who the users are, whose data it is and what a
  mistake costs;
- the principle has no entry in the topic's unresolved list and no boundary that puts this
  project on the other side. A boundary marked as an agent's reading, not the owner's word,
  counts as unresolved for any project near it;
- no standing rule of the owner and no decision this project has already written down says
  otherwise: both outrank a precedent from another project;
- no stop forbids the action the option leads to;
- it is not about money and not about the irreversible (below).

Everything else is not settled. The principle may point to an option nobody offered — for
example "no setting at all"; that is still settled, with that option. A principle gives the
direction, not the details, which stay yours to design.

You come to this test with a recommendation of your own, and a precedent that agrees with it
will look closer than it is. The question is whether the owner decided this, not whether their
decision supports you. When in doubt, it is not settled: a wrong settled decision costs the
owner more than one extra question.

### Never settled, whatever the precedent

- **money** — spending the owner's or a client's money, prices, paid services, anything that
  changes a bill. A fork where even one option costs money is a money fork, including when the
  precedent is a refusal to spend;
- **the irreversible** — a decision that, once acted on, cannot be taken back by the next
  change: deleting or rewriting stored data, sending or publishing something outward, a legal
  commitment, releasing to real users, granting access. What counts is the act the decision
  triggers, not the subject of the feature. How a feature that sends messages or deletes
  records should behave is an ordinary design fork, because the design can be changed
  tomorrow; whether to run a migration over live data, or to publish a repository now, is
  irreversible.

These always go to the owner as ordinary questions.

Without a person (a task the owner set and left), consult the base for every decision you
take in their place. A settled fork is taken as above. A fork the base does not settle cannot
be asked, so it is decided by the rules you were given for working alone; if there are none,
take the option that is easiest to undo and write it down as awaiting the owner. Money and
the irreversible stay off limits: leave them undone and name them in the report.

### The owner's stops

A stop is not waiting for a fork: it is about an action you could take without seeing any
decision in it — installing something, editing a project's rules file, fixing right after a
diagnosis. That is why `index` shows every stop each time, whatever question brought you here,
and why this skill also starts before an action nobody asked for: run `ensure`, `pull` and
`index` and read the stops, even with no fork in sight.

- Before an action a stop names, follow the stop, for the rest of the session.
- If this project gives a concrete reason to act otherwise — a fact of the project, not your
  preference — ask the owner once before acting, and name that reason. Never break a stop
  silently. Without a person, do not break it at all: leave the action undone and name it in
  the report.
- A stop's own "unless" line says where it does not hold; inside that, it is not a stop.
- The owner letting you this once changes nothing: the stop stays as it was.

## After the answer: record it

Do this in the same turn in which the owner answered, before you go on with the work. The
answer is in the conversation now and will not be there after the session ends.

Record a decision when all hold:

- the owner said or chose it themselves: an answer to a fork, an explicit instruction, a
  reversal of what you or the base decided, or a correction of what you did. Silence, "ok" to
  something else and your own unconfirmed recommendation are not decisions;
- it carries to other projects, and the owner's reason or their own words are what make it
  carry. A reason about how things should be — "people should not manage settings, the bot is
  there to be smart" — holds in any project. A reason that is a trait other projects share —
  a personal project, no paying users, a client's data — carries to projects of that kind:
  record it with that condition. A fact of this one project — "in this project we keep no
  specs" — or of this moment — "I will look at it myself" — does not, and the decision is
  narrow. Without a reason it is narrow too, unless the owner's words set it for everywhere:
  "always", "in every project", "this is how I work". A name, a date, a number or a text that
  matters to this feature only is narrow. Decide this yourself; do not ask the owner whether
  to record;
- it says something the base does not hold yet. An answer that exactly repeats a principle —
  the same choice, for the same reason, in a project of the same kind — is not recorded at
  all: no case, no change to the topic. A new kind of project, a new reason, a reason where the
  principle had none, or a sharper condition is something new;
- it holds no secrets, credentials, personal data of third parties or anything a client would
  call confidential. Describe a client's project by its kind when its name should not travel.

A reversal of anything taken from the base — a settled fork or a settled call — is the most
valuable record: it shows where a principle ends. It is recorded whatever its reason: a reason
that belongs to this project is the principle's boundary, and a reversal with no reason goes
to the unresolved list, as `references/record.md` says. Record money and irreversible
decisions that carry too — they are never settled from the base, but they tune your
recommendations.

A correction — the owner stopping you or telling you after the fact, often sharply, that a
choice you made is not what they wanted: "I did not ask for this", "why did you do that" —
shows a decision you took without seeing one. When that choice came from the base, it is a
reversal, above. Otherwise weigh it by the same test:

- about this task or this moment — "do not open the browser, I will look myself" is how the
  owner wants this result checked now — it is kept nowhere;
- about this project only, it stays with the project, below;
- when what the owner objects to is a kind of action you took unasked — installing, sending
  outward, editing a rules file, rewriting data, putting your own scheme in place of theirs —
  and nothing in their words ties it to this project or this moment, it is a stop: "I did not
  ask you to install it" holds anywhere. Words like "again", "I told you", "never" make it
  plain. Write the case with `source: reversal` and add the stop to `stops.md` under the
  subject it belongs to, as `references/record.md` shows. A stop lives there only; no topic
  repeats it. If a stop already covers the same action, an exact repeat writes nothing, and a
  new reason or a sharper "unless" updates its line.

When you are not sure the objection is to a kind of action rather than to this moment, it is
not a stop: a false stop holds agents back in every project. When the owner objects to the same
kind of action again — "again", "I told you" — it is. Do not ask the owner to explain a
correction or to confirm it as a stop; the one question `references/record.md` allows for a
reversal nothing explains still stands.

When you asked before breaking a stop and the owner let you only this time, nothing is
recorded. When their answer gives a reason that holds for projects of a kind — a trait such
projects share, not a fact of this one — it becomes the stop's "unless" line in their words; a
reason you named and they only accepted is marked as your reading. When they say the stop no
longer holds, remove it from `stops.md`; the case that records this goes to the topic its
subject belongs to, as a principle that names the stop's cases as replaced, and those cases get
`superseded_by` it — so every case stays filed.

A decision about the moment — how the owner wants this result checked now, what to skip this
time — is kept nowhere: it was for that moment. A decision about this project stays out of the
base and is kept only when a later session in this project would otherwise get it wrong; most
need no record at all. Keep it in a place that this project alone reads: where the project
already keeps the truth about itself and its decisions — a specification, a decision log,
other documents it maintains as that — or in a memory that belongs to this project only, if
you have one. Add it the way that place takes entries. Do not write it into the agent's rules
files (`AGENTS.md`, `CLAUDE.md` and the like), even where your tools call them memory, nor
into a memory shared by all projects: everything there reaches every project as a rule. Do
not start a new document or a new kind of record for it; when there is no such place, the
decision stays in the work itself.

Right before you write, run `decisions.sh pull`, `decisions.sh index` and `decisions.sh check`
again and reread the topic you will write into, even if you read them earlier in this session. Another session or
machine may have written since, and if this conversation was rolled back or a message was sent
again, what you read earlier may predate your own earlier write: a rollback undoes the
conversation, not the files already in the base.

Then follow `references/record.md`: write the case, file it under a topic or a stop, merge or
mark the boundary, and run `decisions.sh save`. Several answers from one message go in one
save.

## Keeping the base true

The base is worth what its principles are worth, so it is merged, not appended: a new decision
joins the principle it confirms, becomes a boundary of the one it goes against, or — when
nothing explains the difference — becomes one short question to the owner. `references/record.md`
has the steps. Two things hold throughout:

- A reason or a boundary you worked out yourself is never written as the owner's. Until the
  owner confirms it, forks that depend on it are not settled.
- Cases are not deleted: they are the record the principles are rebuilt from. A decision the
  owner replaced stays, marked with `superseded_by`.

When the owner asks to tidy the base, or `check` reports `UNFILED` or `DANGLING`, repair the
filing first, then merge duplicates and resolve boundaries topic by topic.

## Typical failures

| Thought | Reality |
|---|---|
| "The precedent is about something similar, I will settle it" | Similar wording is not the same decision. Settle only when the principle's conditions hold in this project; otherwise ask |
| "The owner once chose the cheap option, so this spending is settled" | Money and the irreversible are never settled from the base |
| "I will list for the owner what I settled and why" | The document that records the decision is the report. A second list makes the owner read their own decisions twice, which is the work this skill exists to remove |
| "I will record the answers at the end of the session" | The session may end first. Record in the turn the answer arrives |
| "I read the base earlier in this session, I know what is in it" | Pull and index again right before writing. Another session may have written since, and a rollback of the conversation does not roll back files you already wrote |
| "The owner decided it, so it goes into the base" | Only what carries to other projects goes there. A decision about this project or this moment stays with the project, or nowhere |
| "The owner was sharp about it, so it must be a rule" | A sharp correction is usually about this result now. It becomes a stop only when the reason or the owner's words make it hold elsewhere |
| "I will add the stop at the end of its topic" | A topic is read only when its question comes up. Stops live in `stops.md`, which every index shows |
| "This stop does not fit here; I will quietly do otherwise" | Ask the owner once, naming the project's reason. A stop is never broken silently |
| "I will put this project's decision into `AGENTS.md`, my shared memory, or a new notes file" | Rules files and memory shared by all projects reach everywhere as rules. A project's decision goes only where this project alone reads it, and no new document is started for it |
| "The base is unavailable, I will decide by my own taste" | Then nothing is settled: ask the owner as usual |
| "Two cases disagree, I will keep the newer one" | First look for what differs between the situations. Replace only when the owner said the old one no longer holds |
