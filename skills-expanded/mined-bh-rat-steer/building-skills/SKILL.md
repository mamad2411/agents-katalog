---
name: building-skills
description: "Builds an Agent Skill (SKILL.md) end to end with steer: design the trigger and components, scaffold with steer new, write the body, then gate on steer validate and a real run. Use when the user wants to create, write, or scaffold a skill, turn a document, API, or repeated workflow into a skill, or review, fix, or improve an existing skill. Also use when a skill needs credentials, persistent state, enforced steps, background processes, or learning wired in."
metadata:
  version: 0.1.0
---

# building-skills
Build an Agent Skill the deliberate way: design the trigger and the
components with the user, scaffold with `steer new`, write the body, and
prove the result with `steer validate` and a real run. The user gets an
installed, spec-valid skill, not a plausible-looking draft.

This skill bundles its own steer runtime at `scripts/steer.py` for its
flow and learning; authoring the new skill additionally needs the
installed `steer` CLI, checked below.

## Before you start

1. **Check steer.** Run `steer --version`. If it is missing, ask the
   user to install it (`uv tool install steer-ai` or `pip install
   steer-ai`), then continue; do not hand-roll a lookalike scaffold as a
   fallback.
2. **Set two paths.** `SKILL` is this skill's own directory (this file's
   parent); `WS` is the new skill's directory, decided during design; it
   does not need to exist yet.
3. **Apply past lessons.** Run `python3 "$SKILL/scripts/steer.py" learn
   show` and follow what it says; those lessons came from real previous
   builds.
4. **Improving rather than building?** For a review or tune-up of an
   existing skill, skip the flow and follow
   `references/improving-a-skill.md`.

## Process

This build runs behind an enforced flow: steps verify themselves against
reality, and you cannot skip ahead. The flow lives next to this file and
operates on the new skill's directory:

    python3 "$SKILL/scripts/steer.py" flow status --workspace "$WS"
    python3 "$SKILL/scripts/steer.py" flow next --workspace "$WS"
    python3 "$SKILL/scripts/steer.py" flow done <step-id> --workspace "$WS"

The steps, and what completes them:

1. **design** (mandate): triage the source material, make the four
   decisions below, and compose the exact `steer new` command. Show the
   user the command, the name, and the install scope; mark the step done
   when they agree.
2. **scaffold** (verified): run the agreed command. Completes when
   SKILL.md exists in the workspace.
3. **write** (verified): fill the scaffold with real content. Completes
   when no TODO marker is left anywhere in the workspace (the generated
   `scripts/steer.py` is exempt; you never edit it).
4. **validate** (verified): completes only while `steer validate .`
   passes in the workspace. Fix warnings and info findings too, or tell
   the user which one stays and why.
5. **exercise** (mandate): install the skill, run it once on a real
   task, and fix what the run exposes. Mark done after the run, then
   wrap up as the directive says.

Do NOT claim the build is done while the flow status shows incomplete
steps.

## The four design decisions

Ground every decision in real material: the document or API the user
pointed at, this conversation's history, or their answers, never generic
knowledge of what such a skill "usually" looks like. When the source is
a document, an API, or the current conversation, read
`references/source-material.md` first; it says what to extract and what
to leave behind.

1. **Who triggers it?** Model-invoked means the description is the
   entire trigger: what the skill does plus when to use it, in the words
   the user would actually say. Human-invoked (`--user-invoked`) trades
   auto-triggering for firing exactly when asked. Pick deliberately.
2. **What does it need at runtime?** Credentials, state between runs, an
   environment snapshot, steps that must not be skipped, a managed
   background process, lessons from its own runs: each is one steer
   component, wired in by `steer new` together with a bundled runtime
   (`scripts/steer.py`), so whoever runs the skill needs Python, not
   steer. Read `references/choosing-components.md` and take only what
   changes behavior.
3. **What loads when?** Material every run needs goes in the body;
   branch-only detail goes under `references/` (`--refs`) behind a
   one-line pointer. The budgets (under 500 lines, about 5k tokens)
   exist because the whole body enters context on every trigger.
4. **How much freedom?** Deterministic work becomes a script
   (`--scripts`, one JSON envelope on stdout); judgment stays prose; a
   required order becomes flow steps (`--steps`) with verify conditions
   instead of ALL-CAPS pleading. The more fragile the operation, the
   less freedom the skill should leave.

## Learning

This skill improves with use. As you work:

- The moment the user corrects you, or something fails and then works a
  different way, capture it:
  `python3 "$SKILL/scripts/steer.py" learn note "<one imperative rule>" --kind correction`
  Lessons are atomic rules ("Use X not Y when Z"), never secrets.
- When a lesson from the digest helped, run
  `python3 "$SKILL/scripts/steer.py" learn confirm <id>`; when one was
  wrong, `learn dispute <id>` the same way.
- Before finishing, record the outcome:
  `python3 "$SKILL/scripts/steer.py" learn run ok` (or `failed` with
  `--note`).

If a `learnings.md` exists in this skill, read it too; those are
promoted lessons that shipped with the skill.

## Gotchas

- Names bite late: lowercase kebab-case, 64 chars max, equal to the
  directory name, and the Claude API rejects names containing "claude"
  or "anthropic". `steer validate` checks all of this; run it early, not
  only at the gate.
- A component the skill does not need is context the agent pays for on
  every run. When in doubt, leave it out; `steer bundle --with ...`
  and one copied section wire one in later.
- The new skill's `scripts/steer.py` is generated code: never edit it
  (`steer validate` flags edits, packaging refuses them), and keep the
  TODO gate away from it. Running the finished skill needs Python 3.11
  or newer, not steer; the installed CLI is for authoring and for the
  optional `--auto-learn` Stop hook.
- One skill, one job. When the design produces two triggers with two
  processes, build two skills.
- The new skill only loads reference files it names. Point to each one
  ("When X, first read references/y.md") or delete it.

## References

Branch-only detail lives behind pointers and loads only when needed:

- Picking runtime components: `references/choosing-components.md`
- Descriptions, bodies, flows, and scripts:
  `references/writing-the-body.md`
- Building from a document, an API, or this conversation:
  `references/source-material.md`
- Reviewing or upgrading an existing skill:
  `references/improving-a-skill.md`
