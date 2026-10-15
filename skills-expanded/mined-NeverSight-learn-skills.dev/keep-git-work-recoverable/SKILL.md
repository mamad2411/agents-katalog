---
name: keep-git-work-recoverable
description: >-
  Establish where you are and what is safe to do when a repository operation
  refuses or the state is unclear: a switch blocked by local changes, a branch
  already checked out in another workspace, a name that will not resolve, a
  detached head, refs that may be out of date, or old workspaces to clean up.
  Nothing uncommitted is discarded and nothing is removed without positive
  evidence it landed. Use when the user says "can not switch branches", "am I
  detached", "fetch is not picking up the new branch", or pastes a git refusal.
  Not for merge-conflict content, commit messages, judging a diff, or commands
  that are already working.
---

# Keep Git Work Recoverable

**Core principle.** Nothing that cannot be recovered is destroyed to make a command succeed.

- **The refusal you are looking at is the tool protecting work that exists nowhere else.**
- **The weight sits in *Tag every claim that rests on the remote*.** Every removal downstream
  rests on whether that tag was honest.
- **You opened this in the middle of something.** This is how to do that work, not a replacement for it. Name what you were doing before you start, and return to it when this is done.

## A refused command is information

- **Retrying it unchanged is the failure this skill exists to prevent.** The second attempt fails
  for the reason the first one already gave you.
- **Classify the state, then make the one legal move from it.**
- **Where no legal move exists without discarding someone's work, the decision leaves you.** It
  goes to the human.

## What is yours to do, and what is the human's

- **You MUST NOT discard work to make an operation succeed.**
- **Each of these is the human's decision.**
  - Committing uncommitted changes.
  - Parking them.
  - Abandoning them.
  - Deleting a branch.
  - Removing a workspace holding tracked edits.
  - Rewriting history.
  - Forcing anything at a remote.
- **You MAY read state freely.** You MAY create a workspace or a branch when the task needs one.
- **Everything that destroys is proposed with what would be lost named.** It stops there.
- **Where the human approves a history rewrite, record the tree hash of the original tip first.**
  Compare it after.
  - **Same tree.** The content survived and only the history moved.
  - **A different tree.** Something was lost. It is found now rather than after the push.

## Establish before acting

**Read these from the repository rather than assuming them.**

- **Which checkout this is.** The main one, a linked workspace, or a submodule pretending to be one.
- **Whether a branch is checked out at all.** An empty branch name means a detached head.
- **Which remote is configured, and what the trunk is actually called.**
- **Whether the environment points the tools somewhere other than the current directory.**

**Get any of these wrong and every later observation describes a different repository.**

## Say which state you are in

**Report it every time.** Each state licenses only what it names, and acting from a state you
have not established is how work that existed nowhere else stops existing.

| State | Means | Licenses |
| --- | --- | --- |
| `UNLOCATED` | the checkout, the head, or the remote is still unnamed | reading, and nothing that writes |
| `LOCATED` | all four of the above are read from the repository | inspecting refs, proposing a move |
| `SECURED` | everything uncommitted is recoverable without this command succeeding | the move that was refused |
| `CONFIRMED` | the work is observed to exist somewhere it survives this checkout | removing the local copy |

- **No state is reached by assumption.** Each one names a reading you performed.
- **Removal is licensed by `CONFIRMED` alone.** The absence of a signal never reaches it.

## Which rules to read

**This table is a gate, not a checklist.** Match the left column against the refusal you got, or
against the state you cannot name.

- **One rule per row.** Enter at the matched row.
- **The match sets where to start.** The claim status sets what you may then assert.
- **Locating yourself precedes everything else.** Every other rule assumes you can name the state
  you are in.
- **Removing anything requires positive evidence**, never the absence of a signal.
- **Where the refusal could be either row, read both.** Guessing which one produces the illegal move.

| If you see... | Read |
| --- | --- |
| you cannot say which checkout you are in, whether a branch is checked out, or whether this is a linked workspace at all | `rules/locate-yourself.md` |
| the task needs a second place to work, or the environment already handed you one | `rules/isolate-or-work-in-place.md` |
| a switch refused: local changes would be overwritten, or the branch is already checked out somewhere else | `rules/switch-refused.md` |
| a name will not resolve: it may be remote-only, a tag, a commit, or a typo, and you are about to try it again | `rules/resolve-the-ref.md` |
| the sync failed, was denied, or never ran, and a claim about the remote depends on it | `rules/stale-refs.md` |
| a workspace or branch is to be removed, or is believed already merged | `rules/removing-work.md` |

**Discriminators.**

- **Locate against isolate.** Locate answers where you are. Isolate decides whether you should be
  somewhere else.
- **Refused against resolve.** Refused means the name was found and the move was blocked. Resolve
  means the name was never found.
- **Stale refs against removing work.** The first downgrades a claim. The second is where an
  unverified claim does real damage.

**Default stance.**

- **Establish where you are before acting.** Every later observation depends on it.
- **Read state freely, and change nothing that cannot be undone.**
- **Hand every destructive move to the human**, with what it would cost named.

## Tag every claim that rests on the remote

**Attach one to every statement about a branch or a remote or a merge.**

- **Observed.** A command you ran in this session produced it.
- **Unverified.** It rests on remote state you did not successfully refresh.
  - A sync that failed, was denied, or never ran leaves every remote claim unverified.
  - That covers "the branch exists" and "it is already merged" and "you are up to date".
- **Unknown.** The state could not be determined at all. Name what would determine it.
- **An unverified claim is reported as unverified.** It is not retried in a loop.
- **An unverified claim never becomes the basis for removing anything.**

## Output contract

```
State        which checkout, which branch or detached, which remote, sync status
Refusal      what was refused and the exact reason the tool gave
Options      each legal move, with what it costs and what it risks losing
Blocked on   the decision that is the human's, stated as a question
Claims       each remote-dependent statement tagged Observed or Unverified
```

- **Name the reason a command refused, in the tool's own terms.**
- **"It did not work" is not a state.** It is the one report that cannot be acted on.

## Follow the names already in use

**Take the naming from the repository, in this order.**

- The trunk's real name.
- The remote's real name.
- The pattern the existing branches and workspace directories already show.

**Where nothing is established you SHOULD ask rather than invent a scheme.** A second convention
beside the first is worse than either.

## Do not skip this when

- **A force flag would make it work.** That is the moment this skill is for.
- **The branch is obviously merged.** Squashed work is not an ancestor of the trunk.
- **You are only cleaning up.** Cleanup is where unrecoverable loss happens.
- **The workspace looks abandoned.** Provenance is what tells you, not appearance.

## Routing

- **The table above selects the rule.** Read a selected rule in full. Say which one you opened,
  in one line.
- **A direct instruction from the user outranks anything here**, including a proposal this skill
  would otherwise leave open.
- **Judging the content of a change belongs to a review of the diff.** This skill only
  establishes and repairs the state that review runs in.
