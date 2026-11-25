---
name: flow
description: The typed flow of research work — ideas, tasks, questions, findings whose evidence a machine resolves, the goals the owner forms and the directions they set, one Markdown record each, linked by references and four links with a rule, moved through the `flow` CLI, with a validator, a generated index with a ranked next list, and a cold-start bundle. Use when reading a project's records to pick up work, when the person says an idea, a question or a task of their own in a session, when minting an idea, a question, a task, a finding, a goal or a direction, drawing or closing a task, answering, closing or reopening a question, removing a finding found false, adding evidence, reaching or giving up a goal, dropping a direction, parking or blocking a record, linking records, ranking the next list, or restructuring the records. The project's own instructions bind the directory, the prefixes and the gates through `flow.toml`; this skill names none of them.
license: Apache-2.0
compatibility: Python 3.11 or later, standard library only. Optional - markdownlint on PATH (a write that adds a violation is reverted), git (the log's part of the freeze check), a project reflow module (one sentence per line; built in otherwise); a resolver for the findings' formal evidence (the formal plugin's, where a formal.toml stands), a probes register and a reference library, without which formal, probe and peer-reviewed evidence is reported unchecked.
metadata:
  version: "0.12.1"
  script: scripts/flow.py
---

# The flow

Work is records: one Markdown file each, front matter plus a prose body, connected by links and moved by transitions.
The records hold data only; rules live in the project's instructions, the skills and the hooks the project runs.
`scripts/flow.py` beside this file is the CLI, the validator, the index generator and the selftest; `flow …` below is that script run by its path from the project root (`python3 ${CLAUDE_PLUGIN_ROOT}/skills/flow/scripts/flow.py …` under Claude Code), never a `flow` found on PATH, which may be another version.
`flow.toml` at the project root binds the paths and the vocabulary.

## The kinds

| Kind | What it is | States |
| --- | --- | --- |
| idea | a thought worth keeping that is not yet a question: nothing says what would answer it, no route; one thing, not a basket of several | open, consumed, removed |
| question | what we think we have to answer to move the research; its body says what counts as an answer, or points at where that is stated | open, answered, wrong, impossible, removed |
| task | a unit of work one owner can finish within its size: a design round, a prose sweep, upkeep, a community item; its body says what done means | open, done, aborted, removed |
| finding | a CHECKABLE claim: each item of its evidence names its form and its target, `formal:Lib/Foo.lean#decl`, and the forms it carries are its trust | standing, removed |
| goal | a destination the owner commits to: its title names the outcome, its body what reached means and how far out it lies | open, reached, given_up |
| direction | the owner's dated statement of where the research moves, its name the title and their words the body | open, closed |

Distinguishing tests: can one owner finish it within its size? then it is a task, not an idea.
Is it a thing you want to know rather than a thing to do? then it is a question.
Can you say what would count as an answer? then it is a question, not an idea.
Can its evidence be named in a form the project accepts and resolved by a machine where the form allows? then it is a finding; otherwise it is a claim inside a task's resolution until it earns evidence.
A conjecture is a question tagged `conjecture` (`flow question … --tag conjecture`), never a finding; a dead end is an aborted task's resolution, never a finding.

Tasks stand across the main axis, idea to question to finding: a task is a unit of work, and a question's closing is its own act, never a consequence of a task's.
A record needs nothing above it: a question may stand alone, a task may come from nothing, a finding needs no question and no goal.

## The links

Five fields connect the records, one general and four with a rule.

| Field | On | Holds | Its rule |
| --- | --- | --- | --- |
| `references` | every kind | a list of record ids | none: the general link |
| `answered_by` | question | one finding | the finding that settles it, answered or impossible |
| `blocked_by` | question, task | a map of `date`, `on` (a list) and `reason` | `draw` is refused while an item of `on` holds |
| `serves` | question | a list of goal and direction ids | biases the ranking; the index lists each goal's and direction's questions |
| `consumed_by` | idea | a list of record ids | the cards that name the idea in `references`, written with the reference |

`references` is a connection with no obligation in the flow, a clue that persists: a record names what it came from, rests on or is about.
Its target is a record of any kind in any state, a closed or a removed one included, since nothing is deleted.
It is written at any mint with `--ref ID`, repeatable, and changed afterwards with `flow ref ID +X -Y`; an entry is an id that exists, never the record's own and never one it holds already, and nothing else is refused, warned of or failed because one exists.
Where the entry is an idea, the script writes the card into the idea's `consumed_by` in the same command, whatever the idea's state, and `flow ref ID -X` takes it out again: `consumed_by` is exactly the records that name the idea in `references`, and the command reports the idea as changed beside the record.
A task and a question are connected when either references the other, and the kit reads the connection from either side: the task's `for` line, the check's warning on an open question whose tasks are all closed and not read since, and the index's section on the same questions, count a task the question names as they count one that names the question; a follow-up task that is not connected to a question does not name it, and nothing is inherited from the task it follows.
A reference says nothing of order.
Cards may be minted ahead; where they have an obvious order, the later one is blocked on the earlier, `flow block LATER --on EARLIER --reason "…"`, and cards that can be worked in parallel carry no block.

## Cards, decks and hands

An idea, a question and a task are cards, and live in decks and hands; a finding, a goal and a direction are held by nobody and stand on the board.
There is one common deck and one deck for each owner, the sense of "assigned to" in a task tracker: a card's `owner` is its deck, a name of `[hand]`, or `null` for the common one, which the commands call `common`.
A new card lands in the common deck unless it is minted `--for` an owner, and a card that leaves a hand stays in that owner's deck.
A hand is what its owner is working on now, an idea being processed, a question being answered, a task being made, within the limit `[hand]` sets, the three kinds counting alike; a card's `drawn` is the hand, the date of the present hold, `null` where the card is in no hand.
`started` is the date of the card's first draw, written by that draw and kept through a return, a pass and the closing, `null` for a card never drawn.
There are two hands: the agent's, which spans its sessions and holds what its subagents do, and the person's.
The skills write `agent` and `owner` for them, the names `[hand]` gives them by default, and the names a project's `[hand]` sets are what the commands take; `common` is no owner's name, and a `[hand]` that names one is refused when `flow.toml` is read.
A task handed to another session, a prover's, stays held in the agent's hand; the handoff's log entry says where it went.
A card that has to wait leaves the hand, since the hand holds only what is being worked: `flow block` and `flow park` on a held card return it to its owner's deck in the same command, and a card whose remaining steps are the person's is passed to the person's deck at that moment.

`state` stores a card's life only: every live card is `open`, a task as an idea and a question are, and a closed one is `done`, `aborted`, `consumed`, `answered`, `wrong`, `impossible` or `removed`.
The standing of a live card is calculated and never stored, the same four words for the three kinds:

| Standing | When |
| --- | --- |
| `held` | the card is in a hand: `drawn` is set; a held card carries no wait |
| `parked` | set down by decision |
| `blocked` | an item of its block holds today |
| `ready` | none of these: a refill may draw it now |

A card both parked and blocked reads `parked, blocked`; an idea is only ever `held` or `ready`, since an idea is never parked or blocked.
`flow show`, `flow find` and `flow state` print the standing, which the index, never reading the day, leaves to the block's items as written.

A closed card is in no deck and no hand, and in a pile read from its state, no file moving for it: the discard pile holds a task done, an idea consumed, a question answered or impossible (a finding settled it), the graveyard any card removed, a task aborted and a question wrong.
`flow find --pile discard|graveyard` lists one, and `flow show` names a closed card's pile.

## The session

A session is dedicated to its hand: it works the held cards that are its own work one by one until each is closed or walled, then freezes, reports what was done and stops; with four such cards in the hand it processes four cards.
A card handed to another session stays held and is not worked here.
Every card minted on the way goes to a deck and not to the hand, a task a question spawns in the common deck unless it is minted `--for` an owner, and ranked by no mint.
A question may be answered with no task at all.
A task it spawns may be a side story, off the list (`flow rank T --clear`); it blocks the question (`flow block Q --on T`) only where the question cannot move without it.
A design round on a question is the held question itself: its record is a dated note on the question (`flow note Q --body FILE`), its discarded options one line each inside it, and no design task is minted for the round; the round mints tasks where a piece of the work is too big.
A round on no question, on tooling or a process, is a task tagged `design`, its record the resolution.
Where the agent needs the person's answer it asks, with its question tool where it has one, in the turn it meets the decision.
Before it asks, or puts a decision to the person's deck, it applies the `method` skill's test under "Working with the owner": a choice a test settles is the agent's, run, decided and recorded, and what is correct is never put to the person as a choice.
If the person answers, the work goes on, the answer written into the card's body (`flow note`) and the log entry.
A decision still open at the turn's end, the person having postponed it or the turn having ended first, becomes a task in the person's deck whose title names the decision, `flow task "…" --summary "…" --for OWNER`, and the card that waits is blocked on it, `flow block ID --on TASK --reason "…"`, which returns it to its deck if it was held.
The log's State paragraph names that task and never carries the decision as prose alone; the task is drawn into the person's hand at their word, and made with the answer as its resolution.
A card whose remaining steps are the person's own work is passed to their deck (`flow pass ID --to owner --note "…"`, the note saying why), and leaves the agent's hand at that moment.
Parking stays for a card set down by decision, and for nothing waited on: a date and an outside event's words are items of a block.
Deviations are the person's to rule and the agent's to propose: drawing a card in the middle of a session, taking another after one that took little effort, or drawing a task straight from the deck for a prover that runs in parallel while the session works on something else.
A card drawn by a deviation counts against the hand's limit, one number and no second class of held card; a deviation that finds the hand full is the person's to settle with the ruling, a card returned or the limit raised.
A project's instructions may carry the person's standing ruling for one.
A session commits at its freeze, or when the person asks; a transition or a ranking commits nothing by itself.
In what the agent writes to the person, a record's first mention in a message carries its title, as `task-0012 (the title)`; later mentions in the same message are the id alone, however long the message; a few records are named each and never as a range of ids.

## What the person says

This part is guidance and no rule of the flow: the agent judges which card a thought of the person's is, and the script reads none of it.

The person's own word for a thing names the card's kind: an idea is minted with `flow idea`, a question with `flow question`, a task with `flow task`, and a goal or a direction is opened on their word alone, as ever.
A fresh project starts from the idea of the project, which, as it is worked, may grow into a goal, a direction and other cards, as "The mints" says: where the person names no other kind, the agent starts from an idea, and the next `whatsnext` ranks and draws it and the session works it from the hand.
Elsewhere, where they name no kind and the agent is not sure, it proposes the kind in one question and mints on the answer.
The agent writes the body from the dialog, keeping the person's words and adding context where it is needed, and the title and the summary as "Writing a title and a summary" says; the source says the record came from the person, and the day, `--source "the person, 2026-03-02"`.
The card is minted into a deck, and is drawn, `flow draw ID --owner agent`, only where the person's message asks for work on it now, as any card is.
An idea is then worked as "The mints" says: what it produces names it with `--ref`, and `flow consume IDEA` closes it once it is folded.

## The mints

Only the mints mint, one per kind, each the kind's name; every one takes the title as its one positional, `--summary "…"` (an idea, a question, a task and a finding are refused without one, a goal and a direction may have none), `--ref ID` (repeatable), `--tag T` (repeatable), `--source S` and `--body FILE`, and a card's mint (an idea, a question, a task) `--value V` and `--for OWNER`, which puts the new card in that owner's deck and the common deck without it.

| Mint | The kind's own flags |
| --- | --- |
| `flow idea "…" --summary "…"` | `--value`; `--for OWNER` |
| `flow question "…" --summary "…"` | `--serves ID` (repeatable): an open goal or direction; `--size`; `--value`; `--for OWNER` |
| `flow task "…" --summary "…"` | `--size`, `--value`, `--due YYYY-MM-DD`, `--after "…"`, `--for OWNER` |
| `flow finding "…" --summary "…"` | `--evidence FORM:TARGET…` (one or more, required, repeatable); `--answers Q`, the open question it settles, which closes answered |
| `flow goal "…"` | none |
| `flow direction "…"` | none |

A title over `[card] title_max` characters (100 where unset) and a summary over `[card] summary_max` (500) are refused, the refusal giving the length, the limit and where the rest goes, the summary for a title and the body for a summary; a summary is one paragraph on one line of the file, and a newline in one is refused.
`--value` is one of `[card] values`, `low`, `medium` and `high` in rising order where `flow.toml` binds none, and never required: a card minted without it is not judged and carries `value: null`; a word outside the list is refused, the refusal naming the list.
A question is minted with its `checked` date at today; a finding it comes from, or a wrong question it re-states, is a `--ref`, and a document it is framed from, an ADR or a report, is its `--source PATH`.
A source with a path's shape (no space, a `/` or an extension) is held to the tree; one in words takes a space.
The words that went before this model are answered with the new way: `capture` is `flow idea`, `frame` is `flow question "…" --summary "…" --ref IDEA` and `flow consume IDEA` once the idea is fully processed, and refining a question, the act of minting its first tasks, is `flow task "…" --summary "…" --ref Q` for each, `flow question "…" --summary "…" --ref Q` for a sub-question.

A minted task gets no rank by itself, whatever it references: ranks are written only by `flow rank`.
A task minted for work now is drawn with `flow draw ID` and ranked at the next ranking, the refill never drawing an unranked card; `flow ref T +Q` after the mint ranks nothing either.

An idea is worked, not only framed: drawn into a hand like any card, it produces what it holds, ideas, questions, tasks, findings, goals and directions, each naming it with `--ref` and listed in its `consumed_by` as it is minted, until everything in it is folded into them and the idea is fully processed, when `flow consume IDEA` closes it, or it is removed; an idea put back partly worked is returned, its note listing what it produced so far.
Reading an idea for a destination the person would commit to and for where their interest points is part of working it: it is done while the idea is held, before it is consumed, and never while the idea stands in a deck; the project's first ideas are the likeliest to hold them.
What it finds it puts to the person with its question tool where it has one, in the turn, the goal's title drafted from the person's words; each is minted on their answer, `flow goal "…" --ref IDEA` or `flow direction "…" --ref IDEA`, and the questions minted from the same idea are given `--serves`.
One put to the person and left unanswered is a decision open at the turn's end: a task in the person's deck whose title names the decision, minted `--ref IDEA`.
No card is blocked on it, an idea being never blocked; the decision is folded into that task, which is among what the idea produced, so the idea is consumed like any other once the rest of it is folded.
On the person's answer the task is made with it, the goal or the direction is minted `--ref IDEA`, and the idea's questions are given it with `flow serves Q +G`.
A goal and a direction stay the owner's: none is minted unasked, and an idea that holds neither produces neither.
One in an idea not yet drawn waits for that idea's working; one the agent meets in a finding or in the person's own words is put to the person in the turn in the same way, and none is minted unasked.
A fresh idea is an open one whose `consumed_by` is empty, calculated and never stored; no mint closes an idea, and `flow consume IDEA` is refused on a fresh one, since an idea that produced nothing is removed with a reason.
A thought that holds several things produces one idea per thing while it is worked; there is no split command.
An idea's size is its independence, not its length: two thoughts that can be framed, worked or dropped apart are two ideas, and a long body that gives one thought its context stays one idea.

A task is work that is big, or that must outlive the turn: a later session or the other hand needs to know it is underway or done, or its result has to be linked; either test is enough, applied with judgment rather than a limit.
Work that passes neither is done in the turn and named in the log entry, and an operation on a card is never a task.
An operation that finds a big piece of work recommends a task and does not do it: `flow task "…" --summary "…" --ref ID` mints it, its body saying what was being attempted and what done means.
Independent pieces of work are not bundled into one task, and a task whose done cannot be stated at once is split; `size` is an estimate for ordering.
A task may carry a due date (`--due YYYY-MM-DD`, `flow set T due DATE|none`), which never moves a rank: the index lists the open tasks that have one under `Due`, soonest first, `flow state` prints that list first, within `[index] due_within` days where `flow.toml` binds it (the index keeps the whole list, since it never reads the day), and names a date that has passed, and `flow check` warns on one, never fails; a not-before date is a block on the date written alone (`flow block T --on 2026-12-01 --reason "…"`), which holds until that day.
A due date is a day of the calendar: `--due 2026-13-01` is refused.
A task may carry a post-done instruction (`--after "…"`, `flow set T after "…"|none`), free text written at the open and printed by `make` and `abort` at the close for the agent to follow; a repeat is the agent minting the follow-up after the make, no interval in the script.
Tags are free words and no vocabulary is validated: `research` and `upkeep` are the usual ones, written at the mint (`--tag`) and changed after it with `flow tag ID +T -U`, a project's own words beside them; `flow tags` reports every tag in use with the records carrying it and the records carrying none, and a project's rule that rides on a tag is unchecked.
The tag `rider` marks a task riding the next piece of work handed to another session, read by `flow find --tag rider --ready`; the tag `conjecture` marks a conjecture.
The tag `revival-owner` marks a card parked until the person says so, whose park reads `--revival "on the owner's word"`; `flow find --tag revival-owner` lists the cards that wait on the person's word.
The park owns the tag: `flow unpark` removes it and says so in one line of its output, and a restate removes it too unless `--tag revival-owner` is given again; the script writes and looks for neither the tag nor the phrase on its own, so the agent passes both.

## Writing a title and a summary

A record has two fields for what it is, each written for a reader who has no other record open, the person looking at a card on a list and the agent reading one before it opens the file: the title says what the card is, and the summary explains it.
The agent writes both at the mint and changes either with `flow set` when the person says so or the work shows the card was misread.

A title is a line that says what the card is, whole, at most `[card] title_max` characters:

- a question's title is the question, asked or opening with *whether*;
- a task's is the act, its verb first;
- a finding's is the claim as one sentence;
- an idea's is the thought;
- a goal's is the outcome;
- a direction's is its name.

A title's subject is never an id, a section number or a row's code, it is never a bare label of a topic (a word or a noun phrase that names where the thing is and says nothing of what it is), and it ends with no colon.

A summary is one to four sentences in one paragraph, at most `[card] summary_max` characters: what the record states, asks or does, in which setting, and what it is for.
It names another record by what that record is, the id after it in parentheses where it helps, and it does not say where the thing is stated or what became of it: where the thing is stated, with the argument and the evidence, is the body's, and the card's history is the body's dated notes.

An invented card, to show the two together:

- title: `Does every A have the property B?`
- summary: `Asks whether every A has the property B in the finite case, the case the first draft of the argument covers; the answer decides whether the hunch from the talk (idea-0001) is worth a proof.`

A title that was the whole statement, and fits a summary, becomes the summary with `flow set ID title "NEW" --to-summary`; elsewhere the summary is written from the body.
`flow doctor` notes the live records whose title is over the limit and the live ideas, questions, tasks and findings with no summary, and fails nothing for them.

## Judging a value and a size

An idea, a question and a task carry a `value`, how much the card is worth to the project, one of `[card] values` or `null` while nobody has judged it; a question and a task carry a `size` besides, an estimate of the effort, one of `[question] sizes`.
A finding, a goal and a direction carry neither.
The agent judges the `value` at every mint of a card, and the `size` at a question's and a task's, from the card's title, its summary and the work it opens; it leaves `--value` out only where it cannot judge, and the card is judged later.
It changes either with `flow set ID value V --note "why"` or `flow set ID size S --note "why"` when the person says so or the work shows the judgment was wrong (a consequence, a discussion, a finding), the note saying what changed it; `none` clears one, and a question's `checked` stays as it was.
A value is a judgment, never a rank: it moves no card up the ranked list by itself, and a rank is still the agent's order, `whatsnext` reading the value and the size when it sets it.
`flow find --value V` lists the ideas, questions and tasks of that value, and `flow find --value none` every card not judged, the closed among them, `--state open` with it giving the live ones, which are the cards to judge.
The check fails a value outside `[card] values`, and nothing warns on a card not judged.

## The closings

| Transition | Consumes and produces | Command |
| --- | --- | --- |
| draw | a ready idea, question or task → in the owner's hand, from the common deck or the owner's own, under the owner's hand limit; it writes `owner`, `drawn` and, the first time, `started`; refused while the card is parked or its block holds, and for a card in another owner's deck, which `flow pass` moves first; `--refill` with no ID draws by rank from the top every ready card of the common deck or the owner's own until the hand's limit, and says each card it drew and each ranked card it passed over with why | `flow draw task-0001 --owner agent`; `flow draw --refill --owner agent` |
| return | a held card → out of the hand, into its owner's deck: `drawn` cleared, `owner` kept; the note is required | `flow return task-0001 --note "…"` |
| pass | a card, held or not → another owner's deck or the common one, out of the hand where it was held; the note, required, is written into the body under the date as `passed from A to B: …`; refused where the card is in that deck already and in no hand, and where it is in that owner's hand, which is a return | `flow pass question-0004 --to owner --note "…"`, `--to common` |
| make | open task, held or not → done and archived, its resolution appended under the date and its closing day stored, `closed: {date: DAY}`, with no reason; the task's `after` printed; it mints nothing | `flow make task-0001 --resolution FILE` (required, refused empty; `-` reads the standard input) |
| abort | started task, held or not → aborted and archived, with its dated reason | `flow abort task-0001 --reason "…"`; `--resolution FILE` |
| answer | open question → answered by a standing finding | `flow answer question-0001 --by finding-0002` |
| impossible | open question → impossible, by the standing finding that shows it | `flow impossible question-0001 --by finding-0002` |
| wrong | open question → wrong, with a dated reason | `flow wrong question-0001 --reason "…"` |
| reopen | any closed question (answered, impossible, wrong, removed) → open, in the common deck, its `answered_by` and its closing cleared, `checked` at today, a dated note keeping what it was; a consumed idea → open, in the common deck, its `consumed_by` kept | `flow reopen question-0001 --reason "…"`, `flow reopen idea-0001 --reason "…"` |
| remove | open idea, open question, open task never started or standing finding → removed with a dated reason; a started task is aborted instead | `flow remove idea-0001 --reason "…"` |
| consume | open idea → consumed, fully processed: its `consumed_by` lists the cards it produced and is kept, its deck, hand and rank cleared; refused where `consumed_by` is empty | `flow consume idea-0001` |
| reach, giveup | open goal → reached or given up, with a dated reason | `flow reach goal-0001 --reason "…"` (what shows it reached), `flow giveup goal-0001 --reason "…"` |
| drop | open direction → closed, with a dated reason | `flow drop direction-0001 --reason "…"` |
| evidence | a standing finding → the same finding with more evidence, its trust raised | `flow evidence finding-0001 formal:Lib/Foo.lean#decl`; `--replace OLD NEW` swaps an item and `--retire OLD --reason R` removes one, each with a dated note in the body |

Every closing clears the card's `owner` and `drawn` and keeps its `started`, and `flow reopen` brings the card back into the common deck.
A task closes one of three ways: made (state `done`), held or not, aborted when started and failed, held or not, or removed with a reason while never started.
A closed task moves to the archive at its closing transition, so the record directories show the live front of work.
A hook runner sets aside the unstaged changes to tracked files and leaves untracked files in place, a tree that never existed, so the project's hook is `flow check --staged`: the same check on a temporary checkout of the git index, which is what the commit holds, with the paths shown as the project's own and the temporary directory removed at the end.
A transition's move that is not staged, or a card minted and ranked first and not yet added, is no part of that commit and fails nothing; a path git ignores (a kept copy, a build's output an evidence line names) is read from the working tree, since the index holds none, and a tracked path from the index only.
`--staged` is refused outside a git repository, and a plain `flow check` reads the working tree.
A commit made after a transition stages the records directory whole (`git add -A` on it), and a batch of transitions is committed at once.
A session that shares a working tree with another and commits only its own paths commits from a work tree of its own, since a commit there takes the records alone and none of the files the other session has staged.
A done task with no resolution is never legitimate: the resolution says what was done, and the archived task keeps what was asked and its notes.
A residue sharp enough to name becomes a task, a question or an idea of its own, minted after the make with `--ref T`, rather than prose in the resolution or a line appended to a question's body.
A design round on no question is a task tagged `design`: drawn before the round, closed by make or abort with the round record as its resolution and its discarded options one line each inside that record; a round on a question is the held question, its record a dated note (the session, above).

A question is minted in the expectation of a finding, a part of the research and not of the conversation, and closes one of four ways:

- answered, by the one finding that settles it: `flow finding … --answers Q` mints it and closes the question in one, `flow answer Q --by F` names a finding that exists; one finding may settle several questions;
- wrong, when it is shown to be stated incorrectly, with a reason and no finding; a re-stated question references the wrong one;
- impossible, when it is shown that it cannot be answered, a paradox for one, by a finding with its evidence like any other; with no such evidence the question is not impossible but removed;
- removed, dropped with a reason, its card kept but in none of the index's lists and out of `flow find` unless asked, the findings minted under it before staying.

No closing of a question is refused for a task that names it, and no task's closing closes a question; `answer`, `impossible` and `--answers` refuse a removed finding and a question that is not open, which is reopened first.
`flow reopen` is refused on a question or an idea tagged `do-not-reopen`, the person's mark that a matter stays settled: on that refusal the agent asks the person what to do and never lifts the tag (`flow tag Q -do-not-reopen`) unasked.
Its note reads `reopened: REASON; it was STATE`, with `by F` where a finding settled it and `(DATE: its closing reason)` where it carried one; an idea takes it only consumed, a removed idea staying final and restored from git where it was removed by mistake; no other kind is reopened, redone work being a new task that references the old one.

An idea removed keeps its `consumed_by`: an idea dropped partly worked keeps what it produced.
A finding found false is removed: `flow remove F --reason R` keeps its card, out of the index's lists and counts, and the notice names everything that refers to it.
What rested on it is the session's to review by hand, case by case: a question it answered is reopened, re-answered or left, and the finding that replaces it references the removed one.
The check says nothing afterwards; the tag `refuted` keeps its meaning, a finding whose claim is a negation.

## The notice

A transition that changes a record's state, or parks, unparks, blocks or unblocks it, prints under that record's `changed` line the records that refer to it by any link, each on a line of its own with its state: `task-0002 (open) — Write up the table`, under `refers to it, may need a follow-up:`; under `--json` the list `notices`, `{"id": …, "refers": [{"id": …, "state": …}]}` for each.
A removed record is left out, and so is a record the same command minted or changed; a closed one is listed.
The link `consumed_by` is read only where the record ended badly or came back, so an idea is named for a card it produced only then: a question closed wrong, removed or reopened, a task aborted or removed, a finding removed; it is not named where a question is answered or impossible or a task done, nor on a park, an unpark, a block, an unblock, a draw or a return, and `flow consume IDEA` prints no notice.
The other links are read on every change, so `flow remove IDEA` and `flow reopen IDEA` name the cards that name the idea.
It is printed by the command that makes the change and nowhere else: `flow state --check`, `flow touched` and `flow check` repeat none of it, and `flow show ID` lists what refers to a record for whoever looks again.
It refuses nothing, fails nothing and asks for no reference to be removed: what follows is the session's to decide, record by record, the task done anyway, removed with a reason, or something else.

## The positions and the fields

| Transition | What it does | Command |
| --- | --- | --- |
| park, unpark | an open question or an open task gains or loses a parking block: the date, the reason and the revival, what would bring the card back, which every park names (a park without `--revival`, or with an empty one, is refused, the first park and a restate alike); `--tag T`, repeatable, adds a tag to the card in the same write; where the revival is the person's word the park reads `flow park ID --reason "…" --revival "on the owner's word" --tag revival-owner`, and `flow unpark` removes that tag and says so; the rank stays; on a question either sets `checked` to today; `flow park` on a card parked already restates it: the reason and the revival are replaced, the parking date is kept and one dated note, `park restated; the reason read: OLD; the revival read: OLD`, is appended (with the tags it added or dropped), a restate drops the tag `revival-owner` unless it is given again, and a restate that changes neither reason, revival nor tags is refused as nothing to change; a card parked before the revival was required stands as it is, its restate naming both; a held card is returned to its owner's deck in the same command, which says so; the command's `changed` line gives the standing as `parked since DATE`, and as `parked since DATE, blocked` where the card is blocked too | `flow park task-0001 --reason "…" --revival "…" [--tag T]`; `flow unpark task-0001 --note "…"` |
| block, unblock | an open question or an open task gains a block, `blocked_by`, or loses it or one of its items; the rank stays; on a question either sets `checked` to today; a held card is returned to its owner's deck in the same command, and stays there once the block clears, until a draw | `flow block task-0001 --on question-0002 --on 2026-12-01 --on "the vendor's reply" --reason "…"`; `flow unblock task-0001 --on "the vendor's reply" --note "…"`, or with no `--on` the whole block |
| rank | the ranked next list, one for the whole project across the decks: an open idea's, question's or task's rank, the whole order at once, or a rank cleared | `flow rank task-0001 1`, `--insert` to take a held rank and move the rest down; `flow rank --set ID…`; `flow rank task-0001 --clear` |
| checked | an open question's last-checked date refreshed: a read recorded | `flow checked question-0001 …` |
| set | `title` and `summary` on every kind, `size` on a question or a task, `value` on an idea, a question or a task (`none` clears it), `due` and `after` on a task; `--note "…"` appends why to the body under the date; `--to-summary` with a title set makes what the title read the summary; `flow set --from FILE` writes many in one run | `flow set task-0001 size small`, `flow set idea-0001 value high --note "the person says it unblocks the rest"`, `flow set goal-0001 title "…" --note "the owner: …"`, `flow set question-0001 summary "…"`, `flow set idea-0001 title "…" --to-summary` |
| ref | a record's references: `+X` adds one, `-Y` removes one, any record in any state | `flow ref task-0001 +question-0002 -idea-0004` |
| serves | an open question's goals and directions: `+G` adds an open one, `-D` removes one | `flow serves question-0001 +goal-0001 -direction-0002` |
| tag | a record's tags after its mint: `+T` adds one, `-T` removes one, the rest kept | `flow tag task-0001 +upkeep -research` |
| note | a file's text appended to a record's body under today's date, through the record's write; no field changes | `flow note task-0001 --body FILE` |

A question or a task may be parked and blocked at once: parked is by decision, a thing not worked on on purpose; blocked is by an obstacle, a thing waited on.
A card that waits on the person's decision is blocked on the task that holds the decision, and one whose remaining steps are the person's own work is passed to their deck (the session, above), never parked for either.
A decision the work needs is asked of the person, and the card is blocked on the task in their deck that holds it; a card parked with the revival `on the owner's word` and the tag `revival-owner` asks nothing and sleeps until the person brings it up.
Parking or blocking a question, propose what becomes of the tasks that reference it: those of a parked question are usually parked with it, while a blocked question may have tasks that go on.

Blocked is calculated, never marked: a record is blocked while an item of its `blocked_by.on` holds, and is not once none does, and a blocker reopened blocks again.
An item is one of three kinds, told apart exactly: a task's or a question's id, which holds until that record is settled (done, aborted, removed, answered, wrong or impossible); a date written alone, `YYYY-MM-DD`, which holds until that day; and anything else, words, which hold until removed by hand (`flow unblock T --on "…"`).
Words that mention a date are words: a date waited on is an item of its own.
`block` refuses an item that would never hold, a record already settled or a date not after today, refuses an item written as `YYYY-MM-DD` that is no day of the calendar (`2026-02-30`), which would otherwise be read as words, and refuses a second block while the first holds; a block that no longer holds is replaced.
`draw` reads the day, and clears a block none of whose items holds; a held card that becomes blocked goes to its owner's deck in the same transition, and stays there after the block clears until a refill draws it, a change of one record resolving nothing, and an idea is never blocked; `flow find --blocked` lists the records whose block holds today, `flow state` names a date waited on that has passed, and the index, which never reads the day, leaves out a record item that is settled and lists dates and words as written.
`unblock` is for words and for a mistake, never needed because a blocker closed.

`flow set` changes the fields a record's prose owner may change at any time; a `title` set appends `title set; it read:` and what the title read, in a code span (the fence one backtick longer than the longest run of backticks in it, a space inside it where it opens or ends with a backtick), to the body under the date, with `. N` after it where `--note N` says why, so what a goal or a question stated stays in the record; a `summary` set keeps nothing of what it read, `none` clears it, and on it and the other fields `--note N` appends `FIELD set: N`.
`flow set ID title "NEW" --to-summary` makes what the title read the record's summary and writes no such note: for a record whose old title was the statement itself and fits a summary, it is refused where the record has a summary and where what the title read is over the summary's limit; a title and a summary are each held to their limit and a title is never empty.
`flow set --from FILE` writes many sets in one run, where a tree has many titles and summaries to write: FILE, or `-` for the standard input, holds one JSON object a row, `{"id", "field", "value"}`, with `"note"` and, on a title's row, `"to_summary": true` where there are any, and every field `flow set` takes is taken, `none` clearing what it clears there.
`--from` takes none of ID, FIELD, VALUE, `--note` and `--to-summary` beside it: each row carries its own.
Each row is validated and applied as a single `flow set` is, its limits, the title's note and `--to-summary`'s refusals included, and the rows of one record are applied in the file's order.
A row whose value already stands is skipped and writes no note, so the same file is run again after an interruption.
A row refused never stops the run and leaves the other rows written; a line that is not JSON, a row that lacks a key and a row that names no record or no field are rows refused like any other.
Each changed record is written whole, markdownlint runs once over the written records, and a record that fails is put back as it was and all its rows are refused with the lint's line; the index is rebuilt once, at the end.
The closing line gives the rows written, unchanged and refused and the records changed, and under it each refused row with its number (its line in the file), its id, its field and why, then each record left half written, a row of it written and another refused, which is settled with a single `flow set`.
`--json` carries `written`, `unchanged`, `refused` (each `{"row", "id", "field", "msg"}`) and `half`, and the exit is 1 where a row was refused.
A field that went before this model is refused with its way: words for the body go in with `flow note`, links with `flow ref` and `flow serves`, a hand-off and a conjecture with `flow tag`.
`flow ref` and `flow serves` take `flow tag`'s refusals: no change given, one entry both added and removed, an entry removed that is not held, an entry added that is held; `flow ref` also refuses to remove the last card a consumed idea lists, the way out being `flow reopen IDEA` first.

Views: `flow find --type task --ready` (also `--form`, a finding's evidence form, repeatable, a finding listed when it carries every form given, with `--only` those whose evidence carries no other, `flow find --form stated --only` being the findings resting on `stated` alone, `--tag`, `--value V`, a card's value, `none` the cards not judged, `--owner NAME`, which reads the field, the deck and the hand together, `--deck NAME`, an owner's cards that are in no hand, `--deck common` the common deck's, `--pile discard|graveyard`, `--refers ID|PATH`, the records naming a record or a repository path by any link, an evidence item, a `source` that is a path of the tree or a body link, with `--deep` the records naming those and so on, `--ready`, the cards a refill may draw now, `--held`, `--parked` and `--blocked`, each reading the three kinds of card, `--ranked`, `--id ID`, and `--grep PATTERN`, a case-insensitive regular expression over the whole record; a removed record is left out unless asked for by `--state removed`, `--pile graveyard` or `--id`; `--state ready` and `--state active` are refused, a task's state being `open` and its standing calculated, which each row prints beside it), `flow show ID` (the record, a card's standing and place or a closed card's pile, its links by field and its back-references, `blocked_by` for the records among a block's items), `flow graph --from ID` (each link an edge labelled by its field, `consumed_by` left out as the mirror of a reference; `--dot` for Graphviz), `flow table [--top N]` (the table as it lies: each owner's hand, the goals and the directions that stand on the board, each owner's deck, the common deck, the discard pile and the graveyard, one heading a zone with its count and its note and one line a card, a hand's cards all, every open goal and every open direction, the oldest first, a deck's top `N` (five where not given) by rank and then the oldest unranked, a pile's none; under `--json` the key `zones`, each `{"kind", "owner", "title", "count", "note", "room", "find", "cards"}`, `find` being the `flow find` flags that list the whole zone), `flow state` (the cold-start bundle: the inbox, the due list, the open goals and the open directions, one line each with its id and title and none of the questions serving them, the ranked list, each owner's hand in full with its cards' ages, then each owner's deck with every card's standing, then the common deck as a count, its ranked cards being on the ranked list above; `--from N` continues it, `--budget N` bounds it; `--check` is the freeze's check, below), `flow directions` (the open directions as the owner's list), `flow tags` (every tag with its records, then the untagged; `--type` narrows), `flow artifacts` (every repository path the records refer to, by evidence, body link or a `source` that is a path, with the records naming each and whether it is in the tree), `flow touched` (below), `flow index` (`--print` to stdout, `--check` for drift), `flow check`, `flow doctor` (below).
`flow --help` lists every command, `flow <command> --help` its flags, and neither needs a bindings file.
The global flags are `--json` (any command emits one JSON object), `--root DIR` (the project, found upward from the working directory otherwise) and `--today DATE`; `flow pages` prints the page manifest the `dashboard` skill renders.
Under `--json` every record carries beside its fields what the flow calculates and never stores, for a card's face: `place`, where the card is in words (`agent, 3 days` for a held card, `agent's deck`, `common deck`, `discard pile`, `graveyard`; `null` for a finding, a goal and a direction), and `lines`, a list of `{"label", "text"}` pairs, only the ones that hold something, in this order: `waits`, `parked`, `due`, `for`, `serves`, `answered by`, `answers`, `evidence`, `fresh` or `produced`, `served by`; a record is named in them by its title.
The envelope of `--json` is `ok`, `command`, `created`, `changed`, `reranked`, `records` and `problems`, with the keys a command adds: `flow show --json` answers the record under `records[0]`, beside `body`, `links` and `backlinks`; `flow find` answers the records found under `records`, a transition the records it created or changed, and `flow table` answers `zones`, its `records` empty.
A `--body FILE` or `--resolution FILE` takes a file, never inline text (`--body "words…"` is refused as a file not found), so a long body is drafted first and checked by the project's text gates — its own checks on prose, such as a linter or a line rule; `-` reads it from the standard input, so a one-off body needs no scratch file (`printf '…\n' | flow idea TITLE --summary S --body -`), and `flow log add -` reads an entry the same way.
Every text line of a transition that names a record is `VERB ID (details) — Title`, as a mint's `created ID — Title` is, so the record is named to the person without a read: `changed ID (state, standing; path) — Title` (a parked standing reads `parked since DATE`, and `parked since DATE, blocked` where the card is blocked too), `untagged ID (revival-owner removed: the tag belongs to the parking) — Title`, `ranked ID (rank N) — Title`, `unranked ID (was N) — Title`, `re-ranked ID (N → M) — Title`, `returned ID (left OWNER's hand for OWNER's deck; why) — Title`, `passed over ID (rank N, type) — Title`, `closed ID (answered) — Title` and `after ID — Title`; the title is printed whole and is always the end of its line, and what is free text comes before it or on a line of its own beneath (the passed-over card's reason, the closed question's `by ID — Title`, the instruction after a make, each record of the follow-up notice); `--json` is unchanged.
A transition that closes a ranked record closes the ranks up, and prints each record so moved as `re-ranked ID (N → M) — Title`, never as changed; `flow rank --set` prints each record it placed as `ranked ID (rank N) — Title` and each it cleared as `unranked ID (was N) — Title`, under `--json` beside `changed` the lists `ranked` and `unranked`.
`flow rank ID N --insert` prints, after its `changed` line, `ranked ID (rank N) — Title` for the record it placed, then a `re-ranked` line for each record it moved, and under `--json` the list `ranked` beside `reranked`.

## Invariants the validator enforces

- Every id is unique and matches its filename prefix; every id in `references` and `consumed_by` exists, `answered_by` names a finding and `serves` a goal or a direction.
- State, size, value and owner (a deck or a hand) are legal values from `flow.toml`, and every field is the model's: a field of an older model fails, and `flow doctor` says what it reads now.
- Every finding standing has evidence, each item of a form `[evidence] forms` lists and resolved by that form's shape, no item twice; a removed finding's evidence is history and no longer resolved.
- Every open question has a last-checked date; an answered or impossible question names the one finding that settles it in `answered_by`, one value, never a task, one imported from before the flow excepted where it names none; no other question names one.
- An idea's `consumed_by` is exactly the records that name it in `references`, whatever the idea's state, and a consumed idea lists at least one.
- Every repository path a live record's body links is in the tree; one a closed or removed record links is warned of.
- What a hand holds stays within its limit, the three kinds of card counting alike; a held card is open, has its owner and its `started` date and carries no parking and no block (V9); a closed card has no owner and no drawn date; a closed task lives in the archive and an open one does not; a removed, aborted or wrong record, a removed finding, a reached or given-up goal and a closed direction carry their dated reason in `closed`, and no other record carries one.
- Parked and blocked sit on an open question or an open task, each with its date and reason, a block with what it waits on.
- A done task carries `closed: {date: DAY}` and no reason (V17, whose message names `flow doctor` where the day is missing); an aborted or removed task keeps its date and its reason, and a card ended any other good way carries no `closed`.
- Ranks are unique and contiguous, never on a closed record.
- Every body is one sentence per line; the committed index equals a fresh render.
- Every library key a record cites is a card the library holds, where a library is bound.

The warnings, never failures: an open question whose tasks are all closed and which was not read since (below), a due date passed, a closed record's body linking a path that is gone, evidence reported unchecked.
`flow check` prints a coverage line saying which resolvers were configured, so a green says what it did not look at; on a failure it names the command that reproduces it, for a session where no skill is loaded.
`flow.py --selftest` plants one defect per code the check reports, fails when one is planted nowhere, and must stay green.

## Reading discipline

Start with `flow state`: the inbox, the due tasks, the ranked next list, the hands, the dates that have passed and the log's top entry, every line carrying its file and line.
The log is dated entries, newest first, each a level-2 heading `## YYYY-MM-DD — headline` opening with a State paragraph; `flow state` prints the whole top entry, and its State paragraph is the one a cold session trusts.
Then the generated index, which lists the ranked list with each question's `serves`, each record's waits and, on a held card, its holder, each owner's hand and deck, the open goals and directions with the questions serving each, the open tasks in no hand (each with its deck where it is an owner's), the open, parked and blocked questions, the questions whose tasks are all closed and not read since, and the settled ones.
Locate records with `flow find` or `flow show ID`; open record files only by ID.
Never glob the record directories, and never read a record directory whole.
A session starts with `flow state` and then does what the person's message asks; where the message leaves open what to do, the agent recommends the next moves, the `whatsnext` skill among them.
The `whatsnext` skill reviews the agent's hand, reads the inbox, proposes what to make of each item, ranks under the focus the person gives, and refills the hand by rank; it runs when the person asks what is next, when the agent recommends it and the person agrees, or when the ranked list is empty.

## Writing discipline

Transitions go through `flow`.
A body is edited freely, by hand or with `flow note ID --body FILE`, which appends the file's text under today's date and needs no file name.
Every field of the front matter is written by its command — `flow set`, `flow tag`, `flow ref`, `flow serves` and the transitions — and `tags` alone also by hand.
The one record written by hand is one imported from before the flow: its whole file, with `origin: legacy`, which lets an answered question name no finding; no transition writes that value.
A body is one sentence per line, and a write that adds a markdownlint violation is reverted where markdownlint is on PATH (with the project's configuration where `flow.toml` binds one or the root keeps one, else a built-in one under which a record's `title:` is the document's title).
The refusal says that nothing was written and, on a mint, that the id it names is not taken, the next mint may get it, and adds one line with the fix where the rule that failed is MD032 (a blank line before a list and after it) or MD033 (angle brackets in prose are put in backticks).
A transition is one shell call, or `&&` stands between transitions, so a refused mint is not read past: the commands that follow it would name a record that does not exist.
A question's body says what counts as an answer, or points at where that is stated; a goal's body what reached means and how far out it lies; a task's body what done means.
The script reads none of these: they are the session's practice, and the title is the one field stating a goal or a question, the summary explaining it.
A body refers to a repository path, a document, a probe, a dataset, by a Markdown link whose target is the path from the project root (`[the theorem](<papers/alpha.md#Theorem 2.1>)`, the angle brackets where the target holds a space), an absolute path or one climbing above the root by `..` being outside the tree and failing V24 as an evidence item's fails V6; a URL, a bare `#anchor` and a path in backticks are prose, so the check never fails on a guess.
The front matter is the subset of YAML the script writes: plain scalars, single-quoted strings (a quote doubled inside), double-quoted strings with escapes, `null`, `true`/`false`, integers, block lists (`- item`) and one-level maps; a hand edit stays inside that subset, and `flow check` reads every record back.
A record points at where its subject is STATED and never restates it, because the statement moves and a copy does not.
A design record is never authority: a record points at a round for its reasoning or its history, never cites it for a rule, a criterion or a method, since the criteria a round fixed bound that round alone.
Run `flow check` before committing; the project's hook runs `flow check --staged`, the same check on the index, as well.

## An older model's records

`flow doctor` names every record and binding written in the words of a model before this one, each with what it reads now, and exits 1 where it finds one.
From v0.9: a record's `summary`, which was its title, with no `title` (renamed `title`, its words unchanged, and `summary: null` added, the explanation the project writes by hand), and an idea, a question or a task with no `value` (`value: null` added, the level the agent judges).
From v0.8.0: a task's state `ready` or `active` (now `open`: the standing is calculated), an active task's `started` and a drawn idea's (their `drawn` date, the day the present hold began, both staying held in their owner's hand), a closed task's `drawn` (moved to `started`, `drawn` cleared), and the fields the three kinds of card lack: `started` on each, `owner` and `drawn` on a question, `rank` on an idea, each `null`; a ready task had no owner and is in the common deck, and a `started` that a record cannot show stays `null`, a task returned before the upgrade having lost its date with the return.
From v0.7.0: `derived_from` (now `references`), a question's `parent`, a task's `requires` and a finding's `depends_on` (each value added to `references`, the field dropped), a question's `direction` (added to `serves`, a list now), `blocked` (now `blocked_by`), a question's or a goal's `criterion`, a task's `dod`, a goal's `horizon`, `why_now` and `first_move` (the words appended to the body as a dated line, `DATE — criterion (moved from the field): …`, nothing written lost), a question's `kind: conjecture` (the tag `conjecture`), a task's `rider: true` (the tag `rider`), and a finding with no `state` (`standing`, with `closed: null`); a block whose `on` holds words with a date inside stays words, and a line says that a date waited on is an item written alone, printed by `flow doctor` and by `flow doctor --fix`, with or without `--all`, and carried under `--json` in the list `remarks`; it is a remark, no thing for the hand.
From the models before: `abandoned` (now `closed`, the state `removed`, or `aborted` for a task that was drawn), `decomposed` (now `open`), `kill` (the body's words, as `criterion`), a task in a question's `answered_by` (a finding settles a question: mint it with `flow finding … --ref T`), `answered_by` as a list (one value now), several findings there (one answers, the others name the question in `references`), `consumed_by` as one id (a list now), a task's or a finding's `question` field (gone: the question named in `references`), a task's `kind` (a tag now), a finding's `status` (gone: the forms of its evidence stand for it; a refuted one gains the tag `refuted`) and `paper` (gone: the document is a reference `flow find --refers PATH` groups by), an evidence item with no form (the prefix read off its shape: `formal:` for a declaration, `statistical:` for a probe, `stated:` for a statement or row), a `statistical` or `reference` item whose document anchor is no row, numbered statement or heading's anchor (checked as a `stated` item's is since v0.5.0, held to the file's existence before: the hand rewrites it, the line naming the nearest heading), a finding under a shard directory (one `findings/` directory now), a question's `direction` holding a bold name (the id of a direction record, named in `serves`), the directions file and `[paths] directions` (directions are records: `flow direction NAME --body FILE` for each bullet), `[task] kinds` and `default_kind`, the `[finding]` section, a missing `[evidence] forms`, the three manifest bindings `[evidence] manifest`, `manifest_roots` and `manifest_extension` (the manifests are `formal.toml`'s alone now: delete the lines), `question_optional_kinds`, an owner `[hand]` does not list, the `decision` kind or tag on a task neither parked nor in an owner's deck, and the `decision_kinds` and `decision_owners` bindings, a third hand, the directions file's `## Inbox` section, a missing inbox, a `flow.toml` with no `[kit] release`, a done task with no `closed` day (written from the date of its first `resolution:` note; one with no such note is for the hand, which sets the day from the file's history), and the fields a record lacks.
The lines come in two classes.
The mechanical ones state the exact edit — a field the record lacks, a word renamed, a state read into this model's, a link folded into `references` or `serves`, an idea's `consumed_by` given the records that name it in `references` as the fix leaves them (the missing ones appended in the ids' order), a field's words moved to the body, a kind or a rider made a tag, `status` and `paper` deleted, an evidence item prefixed by its shape, a finding moved out of a shard, a closed task moved into the archive, `answered_by` and `consumed_by` between a list and one value, an idea's `consumed_by: null` written `[]`, a direction's name rewritten to its record's id once that record exists, an owner cleared on a ready or a closed record, a done task given `closed: {date: DAY}` from its `resolution:` note, a `summary` that was a title renamed `title` — and `flow doctor` counts them per class (`--all` lists each), while `flow doctor --fix` writes them in place, re-ordering each record's front matter to the schema, reflowing a body that gained a line, and refreshing the index, and then prints one line, the count of mechanical edits written and of records changed, above the count by class (under `--json` the same, as `written`).
Where it wrote at least one edit it also adds one dated entry at the top of the log, headed `## DAY — flow doctor --fix wrote N mechanical edits in M records`, with its State paragraph and a list of each class with the records it was written on, the ids in ranges where they run, which `flow state --check` and `flow touched --unnamed` read as naming those records; where nothing was written it adds none, and where no log is bound it says so and adds none.
The judgment ones — a task or several findings in a question's `answered_by`, an entry of an idea's `consumed_by` whose record does not name the idea (removed from the list, or the idea named in that record with `flow ref`), a decision task (passed to the person's deck with `flow pass`, or removed), the directions file's bullets, a third hand, an owner on a held record, the bindings, a missing `[kit] release` among them — are printed one per record for the hand, by `--fix` as well, and settled from their lines; `--fix` exits 1 while any is left, and no migration logic exists for them.
Then come the notes, which fail nothing: each key `flow init` writes now, set or commented, that the project's `flow.toml` has neither set nor commented (a file an earlier init wrote: `[paths] log_archive`, `[evidence] statement_words`, `[evidence] row_id`), with its default and the command that reads it, under `--json` the list `notes`, and two more that count the live records whose title is over `[card] title_max` and the live ideas, questions, tasks and findings with no summary, `--all` listing the records and `--json` carrying them as the list `card_notes`.
A question a task answered keeps one hand-write: once its finding is minted (`flow finding … --ref T`), its id is written into `answered_by`, the migration's one exception to the rule above.
The order of an upgrade: move the pins and restart, then `flow doctor --fix` first, the by-hand list, `flow check`, and only then any mint, the migration's own task among them; the script promises nothing on a tree not yet fixed but the doctor, and refuses nothing on one either (`flow state` prints its line where `[kit] release` is behind, `flow check` fails V3 on each field of an older model).
The migration lands in the commit that moves the pins, since `flow-check` at the new tag fails every record-touching commit until it is done — or the intermediate commit runs with `SKIP=flow-check` and the log entry says so.

## The log, the freeze and the project's other prose

`flow log add FILE` writes the entry FILE holds at the top of the log, under its title: reflowed to one sentence per line, a bold label of at most four words ending in a period, such as `**State.**` or `**Theorem 2.1.**`, a parenthetical allowed after its words as in `**Proposition 5.3 (Jen 1990).**`, kept with its sentence, and reverted where markdownlint reports a violation the log did not have, as a record's write is.
It refuses an entry that does not open with its `## YYYY-MM-DD — headline` and its State paragraph, labelled `**State.**` or `**State (…).**` with a parenthesis of the project's, one dated after today or before the top entry, and a file holding two entries.
`flow log archive --before DATE` moves every entry dated before DATE, verbatim and newest first, into one file per month (`2026-09.md`) in the log's archive directory, merging into a month's file that exists and keeping the link definitions closing it, and leaves one line under the log's title (under its front matter where it has no title) pointing there; the top entry always stays, and an entry whose heading carries no date is refused, since the archive files an entry by its date.
The log's entries are its level-2 headings outside its front matter and its code fences, a fence closing only on a run of its own character at least as long as the one that opened it.
A link definition closing the log goes to every file whose text uses its label: it moves to the archive files where only archived entries use it, is copied where the log uses it too, and stays in the log where nothing does.
The log and its archive files are written together or not at all, and a markdownlint violation either would gain undoes both.

`flow state --check`, at the freeze, decides what a machine can see of it and prints one line per failure:

- the log's top entry is not dated today while the tree has changed since the commit of the newest committed entry — any commit since, on a shared repository another's as well;
- a record changed since that commit, and no entry from the top down to that one names its id: written out, or within a range of the same prefix and width, `finding-0015…0035` (an en dash or three dots for the ellipsis, written with no spaces around it) naming every id from 0015 to 0035; a record whose only change is its rank, which one `flow rank … --insert` gives every record below the one inserted, is not a change the entry must name.

It prints each hand's held cards for the State paragraph, each with its drawn date and its age in days, and fails on none: each hand continues its own work.
An inbox holding items fails nothing, since the next session reads it.
Both parts need git and a committed log; where either is missing, the check says which part it did not decide.
`flow touched` lists the records the second part reads, those changed since the commit of the newest committed entry, each with its title, type and state, so today's entry names them without the ids gathered by hand: `--unnamed` only those no entry names yet, `--ids` the ids alone on one line, `--since REV` since another commit, a record then named by an entry from the top down to the newest the log held at REV.
A record whose only change is its rank is left out of the list and printed on one line at the end (`re-ranked only: id, id, …`), under `--json` as `reranked_only`, and out of `--ids`; the entry does not name it.
A question `flow rank --set` only moved is re-ranked only too: the command writes an order and refreshes no `checked` date, while `flow rank ID N`, a judgment about that one record, refreshes it, and `flow checked ID …` records a read, so a question the session reviewed is named.
It exits 1 when a part fails, else 2 when a part could not be decided, so a freeze it could not see whole is never read as clean, else 0.
What it cannot see stays the session's, and it prints those steps as a checklist the freeze's report answers (under `--json` the list `session_steps`): the conversation's inventory item by item, the sweep by meaning over the documents the session's records touch, the agent's memory checked, and the gates by exit code; the `freeze` skill is the whole of it.

`flow reflow --check PATH…` holds the project's other prose to the reflow the records get: it prints each line, as file and line, that the reflow would change, skipping a front matter block, reads the Markdown files under a directory, and exits 1 on any, or 2 on a path that is not there; the generated index (the file `flow.toml` binds as the index) is not prose under the one-sentence rule, so it is left out of the targets, a directory's among them, with one line saying so, and named alone it is refused with that reason, exit 2; it runs where no `flow.toml` stands, with the built-in reflow, which leaves a sentence unsplit after the common scholarly abbreviations (`cf.`, `e.g.`, `i.e.`, `et al.`, `Prop.`, `Thm.`, `Fig.` and their like) and not after a single capital such as `Theorem A.`, and a project with other abbreviations, a journal's names for one, binds its own reflow module.
A line the reflow does not split is left as written, so a hard break's two trailing spaces are not a change, and a line it splits keeps them on its last part; a code fence is read as the log's are.
`flow reflow --check` prints, under each line the reflow would change, the lines it would become.
`flow reflow --write TARGET…` rewrites each target, a file's path or a record's id, one sentence per line by that reflow, its front matter left as it is, and prints each file it changed, leaving the generated index out as `--check` does; markdownlint then runs as on any write, and a file that fails is put back as it was and refused with the lint's line, exit 1, the other targets of the run staying rewritten.
`flow reflow --as DEST DRAFT` checks a draft before it is placed: its lines the reflow would change, and the markdownlint violations it adds when appended to DEST (DEST a file or a record's id; a missing file named for an existing record is refused with that record's path, one named for a record not minted yet stands for a record's body under its front matter, and any other missing file for the draft alone, linted with MD041 off, since the draft is no record's body and a record's `title:` front matter, which serves as its heading, is not in it), under the configuration a record's write runs with, each at the draft's own line, and never one DEST had already; a DEST outside the project, or in a directory that cannot be written, is refused with a message, exit 2; it writes nothing.

## The next list

The ranked records are the schedule of the WORK, and the only one; the registry below orders the deliverables, not the work.
The agent's hand is filled from its top, and a session works its hand.
The list is filled or refreshed by the `whatsnext` skill, when the person asks or when it is empty, on no cadence, with no per-landing re-triage; a rank is a number alone, and why a record stands where it does goes in the log's entry for that ranking.
`flow draw --refill --owner O` is the refill: from the top of the list, every card whose standing is `ready` in the common deck or O's own is drawn, until the hand's limit, and each ranked card it passes over is printed with why (`parked`, `blocked on …`, `in owner's deck`, `held by owner`), then the hand as `3 of 4` with the room left; an unranked card is never drawn by it, a hand with no limit and an ID given with the flag are refused, a hand already full draws nothing and says so, and under `--json` the lists `drawn` and `skipped` and the hand's `count`, `limit` and `room` are its answer.
Where the hand is left under its limit, the lines say why, and the log entry for the ranking carries that explanation.
Nothing is ranked down or left off for lacking a route: finding the route is its first round's job.
A parked or blocked record keeps its rank, and the list marks what it waits for, so the order survives the wait.
Goals and directions bias the choice of the next moves and never order the list.
A done item clears its own rank through its transition, and the ranks below it close up, so the list stays 1..n without a hand on it.
`flow rank ID N` is a judgment about one record and sets a question's `checked` to today; `flow rank --set` writes an order and asserts no read.

## Evidence and trust

An evidence item is `form:target`: the form one of the words `[evidence] forms` lists, the target what the form takes, each resolved by the validator and by `flow finding`.
The kit ships five forms, words with no rank, and a project picks the ones it accepts at its setup and adds its own; what each means for the project is in its instructions as prose:

| Form | Example | Resolved against |
| --- | --- | --- |
| `formal` | `formal:Lib/Foo.lean#lemma_L`, or a whole module `formal:Lib/Foo.lean` | machine-checked, the path relative to the formal workspace, not to the project's root: asked of the resolver, `formal resolve --protocol` of the `formal` plugin, which answers from the manifests `formal.toml` binds and whose rules (the module a path names, the names a declaration answers to) are its own; the flow reads no manifest |
| `statistical` | `statistical:probes/p.py`; `statistical:results/run.md#FV-1`; `statistical:results/run.md#measured-rates` | the project's own data: a self-asserting script, named with its directory, listed in the probes register the project binds (`[evidence] probes`, a Markdown table whose first column holds the file's name in backticks); or a committed result by its path, with an anchor checked as a document's is where it has one; a result too big to commit is named by its probe alone |
| `peer-reviewed` | `peer-reviewed:jen1990`, `peer-reviewed:jen1990#lemma` | a card of the reference library the project binds, by its key, an extract after `#` |
| `stated` | `stated:papers/alpha.md#Theorem 2.1`; `stated:papers/alpha.md#FV-1`; `stated:docs/adr/0003.md#decision` | the project's own word, a document of the project and an anchor in it: a table row whose first cell is the id, two or three capitals, a hyphen, then letters and digits (`\| FV-1 \|`; `[evidence] row_id` binds another pattern); a numbered statement — Theorem, Proposition, Lemma, Corollary, Definition, Remark, Fact, Conjecture or Example, then `N` or `N.M…`, found at a line start, after `**` or in a heading (`[evidence] statement_words` binds other words, a symbol such as `§` taking its number with no space); or a heading, by the anchor GitHub gives it, a repeated one numbered `-1`, `-2` |
| `reference` | `reference:https://doi.org/…` | any other source: a link, held to its form alone, or a repository path, held to its existence, a document's anchor checked as a stated item's is |

A form the project adds (`forms = […, "benchmark"]`) is held to its path's existence where its target is one, and otherwise reported unchecked, unless the project binds a resolver to it (below); a form the project did not pick is refused, and so is an item with no form.
A form whose targets another tool owns is asked of that tool, as the library is asked `keys` and never read: the flow runs the form's resolver once with every item of the form on its standard input, one JSON object `{"protocol": 1, "form": "formal", "items": [TARGET, …]}`, and reads back one, `{"protocol": 1, "items": {TARGET: {"ok": true} | {"ok": false, "why": "…"} | {"unchecked": "…"}}}`, the exit 0 whenever it answered, whatever the items say.
The flow finds the `formal` resolver first in the binding `[evidence.resolvers] formal = […]`, with or without a `formal.toml`, the whole command as a list of strings, run at the project root with a limit of 60 seconds; else, only where a `formal.toml` stands at the root, the `formal` plugin installed beside the research one (`formal resolve --protocol`); else `formal` on PATH, the hooks' environment; `formal = []` asks none.
Another prover, or a form of the project's own, binds a command that speaks the protocol under its form's word, any form but `statistical`, `peer-reviewed`, `stated` and `reference`; the targets of such a form are the resolver's, so the flow reads no path out of them (`flow artifacts` and `flow find --refers` name none) and holds the item to `form:target` and `[evidence] forms` alone.
With no resolver found, or one turned off, the form's items are reported unchecked, as `peer-reviewed` is with no library; an answer in a protocol other than 1 leaves every item unchecked with that reason; a resolver that does not answer (a nonzero exit, the limit passed, no JSON object, a target left unanswered) leaves its items unchecked at a mint and fails the check once, V6 with no record, `the resolver for formal did not answer: …`.
A declaration resolves when it exists in the manifests, whatever its row's kind, a private declaration's included: that claim is existence (`formal resolve --public` is the plugin's command for the stricter reading, run by hand over a list of names).
Whether a document may cite it is another claim, the `formal` plugin's gates' at the document row and the citation, and a finding resting on a private declaration is one no document row can cite.
A finding's trust is the set of forms its evidence carries, read and never set: the index and `flow find` show them where a status stood, a removed finding showing `removed`, and `flow find --form F` lists the findings carrying one (`--form F --form G` those carrying both, `--only` those carrying no other).
The forms give a finding's evidence a direction to improve in: a finding resting on `stated` alone (`flow find --form stated --only`) is work waiting, a proof to formalize, a probe to run, a work to cite, and `flow evidence F ITEM…` adds the evidence that raises its trust, each item resolved as at the mint.
An item whose file a later change deleted is swapped for its successor by `flow evidence F --replace OLD NEW`, OLD matched exactly as written and NEW resolved as an added item is, or removed by `flow evidence F --retire OLD --reason R`, which is refused where it would leave the finding no evidence, the check failing a finding with none; either writes a dated note into the finding's body, as `flow note` does, so the record keeps what the evidence was.
Where no resolver, register or library is found, such evidence is reported unchecked, and the coverage line of `flow check` says so: it names, for each form asked of a resolver, the route that answered (`via the formal plugin beside the research plugin`) or why none did.
Findings live in one directory, and the document a finding belongs to is a reference `flow find --refers papers/alpha.md` groups by.

## Questions in practice

On the usual path a task is made first and its finding minted after it: `flow make T --resolution FILE`, then `flow finding … --evidence … --ref T --answers Q`.
A question is named, by `flow check`'s warning and by the index's section `Tasks all closed, not read since` alike, where it is open, not parked, not held, has tasks (those that reference it and those it references), every one of them closed, and its `checked` is absent or earlier than the latest day a task closed; a read on the day the last task closed counts as a read, and a task's closing day is the date of its `closed`, which every closed task carries.
The warning reads `` ID: its tasks are all closed and it was not read since: answer it, mint a task (`flow task TITLE --summary S --ref ID`), park it, or `flow checked ID` ``: the question is answered, a next task is minted, it is parked, or it is read and `flow checked ID` says so.
A question worked as it stands, as `whatsnext` step 7 has it, is held and so not named.
A question asks one thing, and its body says what answers it.
A question whose answer is not the person's to rule, but whose search the person may postpone, using a working value meanwhile, is real and stays open; it is set down in four steps:
the person's decision is written where the project keeps its own word, a decision file or the goal's body under a heading;
a finding is minted that says what is true, the working value and whose decision of which day it is, never the answer itself, with `stated:FILE#anchor` as its evidence and `--ref QUESTION`, no `--answers`;
the question is parked, its reason naming that finding and its revival what reopens the search;
when the answer lands, its finding answers the question (`--answers`) and the working-value finding is removed.
Such a question is never closed `wrong`, since it is not stated incorrectly, and it is never answered by the working value; `stated` is the form that holds a person's decision, so a project that wants working values lists it in `[evidence] forms`.
A question in a hand is worked where it stands: a design round on it is a dated note (`flow note Q --body FILE`), and the tasks the work needs are minted where a piece is too big.
An open end a round finds beyond that is a question of its own, referencing the finding that exposed it (`flow question "…" --summary "…" --ref finding-0001`) or minted from an idea captured first (`--ref IDEA`), and is never appended to the first question's body as what stays open: a question that gathers its residues has no answer anyone can reach, and the next list can no longer rank it by how near it is to done.
A question whose parts each carry weight alone is split: at its mint, into one question per part; at answering, the part answered closes the question, and each part still open is minted on its own with a pointer to where it is stated.
A wrong or impossible question is listed by the index under "Settled, do not re-open" with its word; so is any question but a removed one tagged `do-not-reopen` (`--tag` at its mint, or `flow tag`), the person's mark for a matter that must not be asked again; a removed record is in none of the index's lists and none of its counts, listed only by `flow find --state removed` or `--id`.
Minting a question's first tasks is the commitment point: anything ready may be drawn without further approval, so mint them with that weight.
The last cheap "no" is there; most ideas should be removed, and a removal keeps its reason.
What a question takes as its answer is fixed at its mint; the probes and criteria a round fixes bind that round alone, and the `method` skill's honest-change invariants say how a target may change.
A question's body points at where the question is STATED (a document's section, a module) and never restates it.
No question is parked, ranked down or excluded for lacking a route; parking carries a dated reason and a revival, what would bring the card back, and a park without one is refused.
A result is registered in a document as a specific numbered statement with its rows and boundary, never as a thesis rewrite, and the finding that records it is written from the landed artifact, never from the design record that commissioned it.

## Goals and directions

A goal is a destination the project commits to, formed by the owner alone, possibly after the work has started; there may be several, one may appear while the research runs, and a goal may be absent, yet to be formed.
A direction is the way the research moves, not a boundary or a gate: the owner's dated statement of what interests them; the next moves lean toward the directions without being bound by them, a goal being the stronger pull where one is set, and the list stays open to new directions.
A goal implies its own direction, towards itself, so no direction record stands behind one; a direction needs no goal, and may produce goals along the way (`flow goal "…" --ref D`), staying open.
Both are records minted and closed on the owner's word alone, which is the skill's rule and not the script's: `flow goal TITLE --body FILE`, `flow reach G --reason "…"`, `flow giveup G --reason "…"`; `flow direction NAME --body FILE`, `flow drop D --reason "…"`; a session puts one an idea holds, while it works that idea from a hand, to the person with the agent's question tool, as "The mints" says, and mints none unasked.
A question names the goals and directions it serves in `serves`, a list (`flow question … --serves ID`, `flow serves Q +G -D`), the entry added an open one, on any open question, ranked or not.
A task serves a goal only through the question it references: a task minted from no question stands alone, its link to a goal prose in its body or a reference, never read as a route.
A goal's title is the owner's words: `flow set G title "…" --note "…"` leaves what it read in the body, dated, with the owner's words for the change.
Reaching, giving up or dropping clears nothing on the questions: each keeps what it served, and the notice names them for the session to decide on by hand, re-ranked, served elsewhere, or left.
`flow directions` renders the open directions as the owner's list; the index lists the open goals under `Goals` and the open directions under `Directions`, each with the open questions serving it, and `whatsnext` reads its case off them: no goal and no direction, directions and no goal, a goal.

## What else a project keeps

- A LOG of dated entries, newest first, one per landing or decision, each `## YYYY-MM-DD — headline` opening with a State paragraph, the top one the paragraph a cold session trusts, written by `flow log add`; the commit message carries its headline and a pointer, never the entry; old entries are archived by month, verbatim, by `flow log archive`.
- An INBOX, `INBOX.md` at the root unless `[paths] inbox` names another, where the person leaves items between sessions and a freeze leaves a directive for the next one; the next session's `whatsnext` reads it and proposes what to make of each item, and no rule empties it at a freeze.
- Its ARTIFACTS — the papers, datasets, probes, figures and releases it makes — as repository paths the records refer to, by an evidence item or a body link, listed by `flow artifacts` from the records alone, no register to keep consistent; a stale artifact is a task, and the artifacts a project must name, the papers it targets, are in its instructions as prose.
- A REGISTRY of the deliverables — what the project produces (documents, a library, releases) and in what order they are read or shipped — the one place that order is stated; the ranked list orders the work, the registry the products.
- Optionally a reference library of the works it refers to, the `library` skill's, bound to the flow by one command.
- Optionally an annex for the artifacts it made that a recorded claim depends on and no other container owns, its front page carrying the test for what is admitted, a subdirectory made only when what fills it exists.

## What the project binds

`flow init` in an empty project writes `flow.toml` with the bindings filled in and the optional ones commented, the record directories under `records/` (`--records DIR` for another), the inbox, the log where `--log FILE` names one, and the index, and prints the paragraph the project's instructions should carry; `--force` overwrites a bindings file that exists.
`flow init --print-instructions` prints that paragraph for the bindings as they stand, the records directory and the log read from `flow.toml` where it exists, the defaults otherwise, and writes nothing and refuses nothing, so an existing instructions section is compared with it.
The paragraph holds the project's bindings and the rules that stand before a skill is loaded, and a project's instructions do not restate a skill's steps or a command's output, which the skills carry.

`flow init` writes `[kit] release`, the release the setup last brought the project to, at this script's version (read from this skill's `metadata.version`); the setup's verify step (`/research:research-init`) moves it once every step up to the installed release is taken, on the person's word, and a value that is no `vN.N.N` is refused when `flow.toml` is read.
Where it is newer than this script, the project was migrated on another machine or checkout and this plugin, or the hooks' pinned tag, is behind: every write (a transition, `init --force`, `doctor --fix`, `log add`, `index`) is refused and `flow check` reports the mismatch as a problem (exit 1), each naming both releases and the commands that move the plugin, `claude plugin marketplace update research-kit`, `claude plugin update research@research-kit --scope project` and a restart, or `prek autoupdate` for remote hooks; the reads answer, with a warning on the standard error first.
Where it is older, nothing refuses: `flow state` prints one line first, that the setup was last brought to that release and `/research:research-init` is to run, and `flow check` says nothing; a `flow.toml` without the line is a thing for `flow doctor`'s hand.
It writes two owners unless `--owner` names others: `agent`, with a hand limit of four, and `owner`, the person, with no limit (a limit of 0 is unlimited).
`flow.toml` names the record directory, the index, the archive, the inbox, the log and its archive directory (beside the log, `WORKLOG-archive/` for `WORKLOG.md`, where unbound), the id prefixes and width, the owners and their hand limits, the sizes, the levels of a card's value (`[card] values`), the evidence forms the project accepts (`[evidence] forms`, the five shipped ones as written; the setup asks the owner which to keep and which words of the project's to add), the evidence resolvers (the probes register, the anchors a document's items take, and `[evidence.resolvers]`, whose `formal` may stay unset), the reflow module and the markdownlint config, and the reference library's command, which may stay unset: with a `library.toml` at the root the flow asks the library skill installed beside this one, else `library` on PATH, and `flow check`'s coverage line says which.
The project's instructions name the log, the registry, the gates that cover the records and the archive rule, and what each evidence form means for the project.
The project's instructions also name where results are registered and what gates cover them.
