---
name: jevaluate-publish
description: Use when rating whether a project, repo, skill, workflow, plugin, agent product or post uses TypeSafe's Jev (System One) model well -- "is this a good use of Jev?", "rate this Jev integration", "jevaluate-publish https://github.com/owner/repo", or a link to something named after Jev; also when checking whether something that calls itself Jev actually uses it. The rating goes to the public ratings list. For a person's own or team's project, jevaluate-private is the one to use.
---

# Jevaluate Publish

Rates how well something uses Jev, TypeSafe's System One model (typed questions over a JSON `state`, answered in parallel with calibrated probabilities). Every rating is evidence-backed, dated, tied to a commit, and logged, so the library of past ratings anchors future ones.

## How to rate

Follow `read.md`; `scripts/step.py` serves the rubric, the fix rows and past ratings one phase at a time. Jevaluate rates projects; it doesn't run or diagnose your own pipeline. If asked for that, say so and stop.

## Model

Run on a Sonnet-class model at medium effort, the same one every time: ratings stay comparable only if the rater doesn't change. In Codex, run on `gpt-6-sol` at medium effort. In another harness, pick one model and effort and keep them. Record both in the rating (`rater`, `effort`); a rating by a different model is a different rater's.

## Verdicts

Verdicts run from 5 "Learn from it" down to the verdict-1 codes and "Can't rate yet", defined in `rubric.md` section 5. They come from the rules, never from averaging scores. Any verdict of 3 or below states its reasoning and the core fixes.

## The library

Ratings are logged outside this skill, in `$JEVALUATE_LIBRARY` if set, else `~/.claude/jevaluate-library/` if it exists (libraries made before Codex support), else `~/.jevaluate-library/`; `scripts/library.py` creates it. Never overwrite a past rating: a re-rating is a new dated entry.

## Sources

Only public sources: the docs at docs.typesafe.ai (page list: `https://docs.typesafe.ai/llms.txt`; append `.md` to any page for markdown) and the project's own public files. Credit a repo to its GitHub owner, never to its banner or branding. A project's claims about its own results are claims until the rating checks them.

## In Codex

Codex's default sandbox blocks the network and writes outside the workspace. Fetching a repo (`gh`, `git`) and `library.py add` need your approval, or run with network access and the library folder as a writable root.
