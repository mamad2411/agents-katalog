---
name: freeze
description: Freeze a session so a cold one can continue it — save what the work needs that the conversation alone holds, check the records with `flow state --check`, sweep what the session made stale, run the gates and commit, then report item by item. Use as `/research:freeze`, and before a session ends that changed the records or the documents. Ranks nothing; the next list is the `whatsnext` skill's. When the person says 'freeze', 'save the session' or 'park the session', they mean this skill — call it every time, even if it ran earlier in the session, and take every step.
license: Apache-2.0
compatibility: The `flow` skill beside this one, whose script it runs; git for the check, the commit and the push.
metadata:
  version: "0.12.1"
  requires: flow
---

# The freeze

A session is frozen when a clone of the repository on another computer could continue from it: could a cold session, reading only the inbox, the ranked list and the log's top State paragraph, go on without asking?
That clone test rules out whatever does not travel: the agent's memory, the scratchpad, an untracked store, a subagent still running, a local tool's state.
A freeze is a request of its own: when the person says 'freeze', 'save the session' or 'park the session', they mean this skill, called every time, even if it ran earlier in the session, with every step taken; a request ending "… and freeze" is two requests, the work and then this skill.
The one rule is to save what is important for the work, anything useful the session found and did not record.
`flow …` below is the `flow` skill's `scripts/flow.py`, run by its path from the project root as that skill says.
Where the `flow` skill is not loaded, load it before the steps: no record is minted without it.

1. **The records say what the session knows.**
   The log's top State paragraph is current and its next action names the fresh session's first move; where work happened after the entry, it is extended or a new entry added with `flow log add FILE`.
   The State paragraph says where the work stands and the next move, and never the gates' result or the push, which are facts about the commit and go in the turn's report, step 6.
   A decision that waits on the person is named there by the task in their deck that holds it (step 2), and never carried as prose alone.
   `flow touched --unnamed` lists the records changed since the newest committed entry that no entry names yet, the ids the entry is to name; `--ids` prints them on one line, and a record only re-ranked by a renumbering is left out, not to be named.
   The entry may write the ids out or name a run of them as a range, `finding-0015…0035` (an en dash or three dots for the ellipsis, written with no spaces around it), which the check reads as every id of that prefix from 0015 to 0035; `touched` lists each id on its own.
   At the month's first freeze, `flow log archive --before DATE` moves the older entries.
2. **Flush what only the context holds.**
   Inventory the conversation turn by turn, the person's messages and the replies both, under the test: if the transcript were deleted now, would anything the person said, or anything the person was told, be lost?
   Each item goes to its home by kind: an idea in the person's words, verbatim and dated (`flow idea`); a ruling where the project keeps its rules, never a card's content; a reading given in a reply into the body of the record it is about, with its standing; a correction as a dated line in the record; an unanswered question as a question or an idea; a decision that waits on the person, asked with the agent's question tool in the turn and, where it stays open, a task in their deck, `flow task "…" --summary "…" --for OWNER`, its title naming the decision, the card that waits blocked on it with `flow block ID --on TASK --reason "…"`; a preference about the process to the agent's memory.
   Then close the lifecycle of everything the session created: a task made or aborted, an idea consumed or left in the heap.
   Then the held cards: for each card the session's hand holds, the log entry says what the session did on it, and one left untouched is returned (`flow return ID --note "…"`) or passed (`flow pass ID --to OWNER --note "…"`) with a note.
   A freeze ranks nothing: a question minted is named unranked, and the list is the `whatsnext` skill's.
   A directive the next session should start from goes to the inbox, one directive, never a summary of the session.
3. **Sweep by meaning.**
   Search the surfaces a reader sees, the documents and the published pages, for the claims this session made stale, by the claims' own words, not only the files the session already touched.
   A stale claim the session may not correct, in a document the project's rules let only the person change, goes to a record — an idea (`flow idea`), or a task where the fix is work (`flow task`, `--ref` the record it is about) — with the place and the proposed edit in its body, and is named in the log entry, never left in the transcript.
4. **The checks and the gates, by exit code.**
   `flow state --check` decides what a machine can see: the log's top entry dated today where the tree changed since the newest committed entry, and every record changed since then named by an entry, a range of ids read and a record only re-ranked not asked for; it prints each held card with its drawn date and its age in days, for the State paragraph, and fails on none.
   It exits 1 on a failure, 2 where a part could not be decided, never read as clean; `flow check` and the project's other checks run beside it.
   It also prints the steps that are the session's own as a checklist — the conversation's inventory item by item, the sweep by meaning, the agent's memory checked, the gates by exit code — which the report answers.
5. **A commit with named paths, then the push as the backup.**
   The session commits at its freeze, or when the person asks before it; no transition and no ranking commits by itself.
   Before the commit, `git status --porcelain` shows whether the tree holds staged or unstaged changes outside the paths committed, another session's files in a shared tree among them: a plain commit takes what the index holds, another session's staged files among them, and the hook runner stashes the unstaged changes while the hooks run, so an edit written in that window can keep the stash from applying.
   Where there are some, commit from a `git worktree` of the freeze's own, as Install's "Several sessions in one tree" says, so that the commit holds the session's paths alone; the hooks are no reason for it, since they check the index and not the working tree.
   Or say in the turn that the runner is about to stash them.
   The flow wrote the session's own edits into the tree, uncommitted, so `git merge --ff-only` from the worktree is refused over them, and the edits travel by copy:
   - `OLD=$(git rev-parse HEAD)` and `WT=../freeze-wt`, then `git worktree add -q --detach "$WT" "$OLD"`, detached since the tree holds the branch;
   - `PATHS` is the list of paths copied and deleted in the worktree, a move's old path among them: each path the session changed is copied there with `cp -p`, the folder made first where it is new, and each path it deleted or moved, what a transition archived among them, is deleted there as `rm -f "${WT:?}/${p:?}"`, the guarded form, where `:?` stops an empty variable from reaching `rm` and which an agent's shell safety check accepts where a plain `rm -f "$WT/$p"` in a loop is refused; `git -C "$WT" add -A -- PATHS` stages them, and `git -C "$WT" status --short` shows what the commit holds, a move as a rename;
   - the commit is made there, `git -C "$WT" commit`, so it holds the session's paths alone;
   - in the tree, `NEW=$(git -C "$WT" rev-parse HEAD)`, `git update-ref refs/heads/BRANCH "$NEW" "$OLD"` and `git reset -q -- PATHS`, the paths listed from the new commit by `git show --name-only --no-renames --format= NEW` (one path to a line, a move's old path and its new path both; without `--no-renames` a move is listed by its new path only, and the old path then stays in the index): the update is refused if another commit moved the branch since `OLD`, and the reset brings the index to the new commit, the files already holding its content;
   - `git status --short -- PATHS` prints nothing, which is the check; another session's changes still show as they did;
   - `git worktree remove "$WT"`.
   Steps 2 to 5 run even on a clean tree: a clean tree says nothing about what the conversation still holds.
   A push stops on a non-fast-forward rather than forcing.
6. **Report, as the turn's final output.**
   It answers the checklist `flow state --check` printed, item by item: the inventory with where each item went, the sweep with the terms searched and the documents read, the agent's memory checked, and the gates by exit code; then the tree and the inbox directive or "none".

## The agent's memory

The agent's memory is per machine and fails the clone test, so nothing a continuation needs lives there alone.
It holds a fact about the process that no record owns — a trap paid for, a tool's behaviour, a preference of the person — and never what the repository records, and never a tree-derived figure.
An incident goes to the log, the rule it earned to the skill or the instructions that own it, the agent's own trap to its memory; a lesson that holds for every project moves from the memory into a skill.
