---
name: to-launch
description: Hand one or more specs to the factory (the `to-launch` label) instead of building them in this session.
disable-model-invocation: true
---

The counterpart of `implement` when a spec is built **by the factory**: this
session writes no code, it puts specs in tracerworks' queue. A worker takes
each one, implements its tickets and opens the pull request; the merge queue
tests it and tracerworks merges it. Your only material here is **GitHub
labels**: no branch, no worktree, no file of the repository.

The mechanism: every minute, `tracerworks start-next` launches the oldest
open **spec** carrying both the ready label and the launch label (by default
`ready-for-agent` and `to-launch`; `priority` first), provided it has a
**free head ticket**. The label lives on the **spec**: on a ticket it does
nothing. The labels' names are your project file's (`[github]`).

## 1. The specs

Take the numbers given as arguments, else the specs published in this
conversation. A ticket's number leads to its spec: the first `#n` of its
`## Parent` section, or of a line starting with `Parent:` ("Parent" inside a
sentence does not count).

**Done when** every target is a spec's number.

## 2. The checks

Exactly those of `start-next`, for each spec:

1. **It is a spec**: open, labelled `spec` (or titled "Spec — …"), and its
   body names no parent. A body that names one is a ticket: back to step 1.
2. **It is ready**: it carries the ready label.
3. **It has at least one open ticket**: an issue whose parent is this spec.
4. **One of its tickets is free**: unassigned, and every blocker it names is
   closed (`gh issue view <b> --json state`). A blocker is written on one
   line (`Blocked by: #a, #b`) or listed under a `## Blocked by` heading
   (`- #n`, one reference at the head of each item).

A spec that fails is not launched: say which check fails and its remedy. No
ticket: `/to-tickets`. No free ticket: name the blocker still open. A closed
spec with a ticket left: reopen it — the worker starts from a new branch.

**Done when** every spec is either launchable, with its head ticket, or
refused, with the check that fails.

## 3. The label

`gh issue edit <spec> --add-label to-launch` on each launchable spec, and
nothing else: `priority` only if the operator said so in this conversation.

**The model and the effort**, only on the operator's word ("launch it in
xhigh", "in sonnet"): one label per dimension on the **spec**, with your
project file's prefixes (`effort-high`, `model-sonnet`). Remove the opposite
label of the same dimension first: two labels of one dimension start the
worker at the default. Without a word, touch nothing: the worker starts at
the project file's default. They are read again at each start of the worker.

Then read the labels back (`gh issue view <spec> --json labels`).

**Done when** the reading shows the launch label on each launchable spec and
on no ticket, and at most one label per dimension on each spec.

## 4. Report

One line per spec: its number, its head ticket, its level (the default, or
the labels), its place in the queue (`gh issue list --label to-launch --label
ready-for-agent --state open`: `priority` first, then the oldest). Recall that
a worker never deploys, and that its pull request merges through the queue
once green. For the workers' state: `tracerworks status`.
