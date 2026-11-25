# AGENTS.md

Orienting doc for any AI coding agent landing in this repository.
Format: [agents.md](https://agents.md/).

_Everything this repository documents lives in [`handbook/`](/handbook/README.md), the single source of truth.
This page only routes there._

## What this repository is

<!-- One paragraph: what the repository is for, and the one thing to know before touching it.
     Link the handbook leaf that owns the detail rather than restating it. -->

## The first five minutes

- where a fact lives, and how the tree grows: [`handbook/meta/handbook/`](/handbook/meta/handbook/README.md)
- how a sentence is written here, before you write one: [`handbook/meta/authoring/`](/handbook/meta/authoring/README.md)
- what this repository decides for itself, and the rules it adopts beyond the shared ones:
  [`handbook/meta/local/`](/handbook/meta/local/README.md)
- the vocabulary this repository uses: [`handbook/meta/glossary/`](/handbook/meta/glossary/README.md)
<!-- Add the leaves a session needs before its first edit: how to build, how to test, how a change is proposed and lands. -->

## Behaviour

- Every document outside `handbook/` either derives from it or backreferences it, and this page's italic line is its own.
  In Claude Code the prose rules load on their own when you touch a file carrying prose;
  run `/docs:check` after touching documentation.
<!-- Add the standing prohibitions of this repository, each linking the leaf that says why. -->

---

_The shared pages under `handbook/meta/` point to their home, [`cynkra/handbook-tools`](https://github.com/cynkra/handbook-tools);
the rule file and the skills are carried from there unchanged,
and `.handbook-source` names the files and the state of the source this handbook was last checked against._
