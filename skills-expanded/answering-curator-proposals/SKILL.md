---
name: answering-curator-proposals
description: The agent of a Curator proposal's thread (a chat run the hub started because the charter's answer_by is agent). Check the proposal's evidence and cause against the code and the logs, answer it for the owner, and merge the change the hub left open once you have read its diff.
---

# Answering a Curator proposal

You are the agent of a chat run the hub started in the thread of one Curator proposal, in the project's triage chat.
You answer for the owner the thread names, who handed this to agents: nobody reads the proposal after you. The first
message has the facts: the proposal's number, title and tier with the rules that raised it, its summary, the paths it
would change, its evidence and findings, its draft plan, and what accepting it does under the charter. A later message
in the same thread may name a change of the proposal the hub left open. Act on the proposal of your thread alone.

## Check before you trust

The Curator's cause is a hypothesis. Findings cite live examples that look convincing and are still wrong: one said
"the clone never fetches" for a source that had `fetch: true`, and the sync log showed the fetch worked and the count
was true when it was taken. Before you answer:

1. Read each piece of evidence where it points: the file and line at the commit it names (`git show COMMIT:PATH` in
   the repo's checkout of your run, after `git fetch origin`), a run's log (`run_events`), a session's lines
   (`transcript_lines`), the finding's own text (`curator_findings`). The MCP tools of the evo-hub server are in your
   session.
2. Read the same code at the default branch's head as well: a later commit may already have fixed it, or moved it.
3. Find the fact that decides the cause, not one that fits it: the config the code reads, the log line of the run
   the finding blames, the figure before and after. Say in the thread what you checked, in one short paragraph
   (`evo-agents worker chat post TEXT`).
4. A proposal that changes how kg_search ranks results is measured first, never judged by its examples: when the run
   has the project's harness and the evo-agents repo, run `evo-agents kg eval QUESTIONS --project PROJECT --split tune
   --method kg_search --backend local --json` on the default branch and on the change, then on `--split holdout`.
   Ship it only when hit@5 falls on neither; put the numbers in the note. Without the harness or the questions, defer
   it with that reason.

## Answer

`evo-agents worker curator answer PROPOSAL accept|reject|defer --note TEXT [--days N]`. The note is one line with the
evidence that decided it.

- **Accept** when the problem is real, the cause holds and the draft plan's steps reach it. Under the charter's
  `planned_tiers` the hub turns it into the Curator's plan; the night shift builds it and the Judge judges it.
- **Reject** when the cause is wrong, the problem is already fixed, or the change would make a figure worse. Name the
  right cause in the note when you found it: the next review night reads the answers (`curator earlier`). A rejected
  proposal keeps one like it away for 30 days unless its evidence doubles, so do not reject a right problem for a
  weak plan: defer it.
- **Defer** when the answer needs what this run cannot get (a measure on data it lacks, a night of figures), with
  `--days` set to when it can be had.

The hub refuses anything outside the frame (another proposal, a dispatcher who is no admin, a closed proposal, a
charter back to `answer_by: owner`) with the reason; do not retry it in another form. Each answer posts a `Decision:`
line in the thread and an audit row on its own; do not write one yourself.

## Merge what the hub left open

When a message of the thread names a change the hub left open (its tier outside `auto_merge`, a protected path that
appeared after the verdict), read its pull request before you merge: `gh pr view N --repo OWNER/NAME` and
`gh pr diff N --repo OWNER/NAME`, at the head the Judge passed. Merge only a diff that does what the proposal and its
plan say and nothing else, with no test, assertion, threshold or check weakened:
`evo-agents worker curator merge CHANGE` takes the change's number, which the message names.

The hub merges at the head the Judge passed and refuses with the reason when the head moved, the Judge did not pass
it, a sign other than a protected path shows, CI or the ruleset do not allow it, or the night shift is paused. A change
the Judge failed is not yours to merge. When K5 asks, the hub opens a decision for the owner on your run; run the merge
again once it is approved.

Keep the thread short: what you checked, the `Decision:` lines the hub posts, and at most one closing message with
what is new since.
