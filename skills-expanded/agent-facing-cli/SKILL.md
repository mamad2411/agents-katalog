---
name: agent-facing-cli
description: "Use when an agent will drive a CLI. Contract test first."
version: 1.1.0
author: coder role of hermes-fleet-apps
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [cli, json, contract, agent, skill-pack, testing]
    related_skills: [build-method]
---

# Agent-facing CLI

When an assistant (or any script) is to operate a CLI, the machine-readable
output IS the product. The assistant never reads prose. So the output gets a
contract before anything is built on top of it, and the instruction sheet is
written FROM that contract, never the other way round.

## Order

1. **Inventory the real shapes.** Read every `--json` (or equivalent) emit
   site in the source and list keys per command. Measured, not remembered:
   the prose form and the JSON form drift independently.
2. **Contract test, before the skill.** One test file that:
   - runs every command through the REAL entry point (`main(argv)`), not the
     command functions — the argument parser is part of the contract;
   - `json.loads` the WHOLE of stdout: one document, nothing before or after.
     A progress line printed under `--json` is then a red test instead of an
     agent that silently misreads a run;
   - asserts the keys the sheet will name (`{...} <= doc.keys()`) and the
     type it assumes: list-when-empty, bool flags, the undo handle;
   - drives the whole autonomous loop end to end on a temp fixture.
   Stub the expensive engine (model, network) with a stand-in keyed by
   filename so the fixture is milliseconds and deterministic. Never let a test
   fall back to the real data dir: make the data-dir argument mandatory in the
   test helper and assert it.
3. **The instruction sheet (SKILL.md)**, from the contract. Two columns: what
   the agent may do on its own vs. what it only relays from an explicit human
   instruction — anything that names a person, anything with no undo. Say what
   to READ from each response, not only what to run. Destructive commands:
   plan, show the human what the id resolved to, `--apply` only after they
   confirm and never in the same turn.
4. **Sheet and parser agree both ways.** A test collects every
   `<tool> <command>` the sheet names and asserts `named <= real` AND
   `real <= named`. A ghost command fails the agent on its first message; an
   unnamed command is a capability it will never use. Assert the collected
   set is non-empty first — a regex that matches nothing passes both
   containment checks vacuously.
5. **Shipped agent material is public; it gets a leak check.** Anything in the
   pack directory is copied onto strangers' machines. Ban by SHAPE (home
   paths, key prefixes, `key=` followed by a value, model-family names), never
   by a list of real values — the list would be the leak. Plant each shape in
   the sabotage pass (see the qa role's `guard-verification`), including alphanumeric
   suffixes like `gpt-4o` that `\d\b` misses.
6. Only then the profile/install packaging, and only after that any intake
   parser for free-text replies.

## Giving a UI-only action a CLI door

When an action is reachable only from a page, server or window (answer a queued
question, confirm a match), an agent cannot do it. Add a command; do not embed the
page.

1. **Find the one function that already performs the action and call THAT.** Lift it
   into a named factory first if it is a closure inside the server. The command is
   a second door into the same write path, never a second copy: the meaning of each
   answer, the journal and the side-records stay decided in one place.
2. **Address the target by a stable handle, never by list position.** Each CLI run
   rebuilds the queue, so "item 3" can name a different item between the `--json`
   read and the answer. Take the path or id. Then confine it: `resolve()` first, then
   `relative_to(<allowed dir>)`, so `allowed/../x` is refused as well. A position
   could only name a queued item, and the handle has to keep that promise.
3. **Rebuild the item with the SAME builder the queue uses**, so the question being
   answered is exactly the one `--json` showed.
4. **Validate the flag grammar before opening any store:** exactly one answer kind
   (the kind is its own flag, a name is data and never a command), sub-flags only
   with their owner (`--note` only with `--accept`), answer flags refused without the
   door flag, and the door refused next to the long-running mode (`--serve`). Exit 2
   for grammar, exit 1 for an action that ran and failed, with the reason on stderr.
5. **Plan by default, `--apply` to act**, and make the plan report the destination
   the apply would use.
6. **Under `--json`, wrap the reused function in `contextlib.redirect_stdout`** when
   it narrates to a terminal. Then put everything it narrated into the document:
   undo id, created record id, any remembered rule. If the function's collector does
   not carry an id you need to report, widen the collector, not the output parsing.
7. **Before adding flags to an existing command, grep the tests for hand-built
   argument objects** (`SimpleNamespace(` / `_args(` helpers). They skip argparse
   defaults, so every new `args.<flag>` read raises `AttributeError` in tests that
   never touched the feature. Backfill the missing attributes at the top of the
   command with `hasattr` defaults. Grep the same way before widening a shared tuple
   or return shape, and change any test that pins the old shape on purpose, making
   it stronger (for example, check the new id against the stored row).
   **Widening an option from one value to many** (`type=int` -> `nargs="+"`) is the
   same trap: hand-built callers keep passing the scalar and crash on iteration.
   Accept both shapes at the top of the handler, keep the one-value output document
   unchanged, and put the many-value case in its own function with its own document.
   Existing callers (window, agents) then need no change in the same commit.
   **A batch version of a destructive command refuses the WHOLE set** if any one item
   would be refused alone (an unknown id, a set that leaves an owner empty). One
   plan lists every item with what it resolved to, and one `--apply` runs everything in
   one transaction. Removing the valid rest would remove a set nobody reviewed as a whole.
8. **Prove it end to end with the real executable in a subprocess**, the way the
   window or agent will call it: plan, apply, the side-record, `undo`, and a refused
   path, on a throwaway world.

## Renaming what a human reads

When a label shown to a person is wrong but its value is also a machine key (a
`--json` field, an enum written into journals), split the two instead of renaming:

- Keep the enum value and the JSON key exactly as they are. Agents, journals and old
  runs read them, so a rename breaks every consumer without any error.
- Put the human word in ONE shared constant, and have every surface (CLI summary, web
  page, per-file lines) read that constant, so no two surfaces spell it differently.
- In the agent's instruction sheet, explain what the key MEANS. Otherwise the agent
  will relay the old wrong meaning to the human.
- Grep every place that prints the old word, and decide for each one whether it has
  the same meaning. The same word often covers two different facts ("file failed to
  decode" vs "item too unclear to classify"). Give each fact its own word; leave alone a line that
  already describes a real failure correctly.
- Test the human output for the new word AND for the absence of the old one, and assert
  in the same test that the JSON key is unchanged.
- Prove it on a real dry run: same input, same count, new word.

## Rules

- No agent loop inside the CLI. The CLI stays a CLI; the agent is a separate
  pack that calls it. Adding it to the repo means a real commit, a README
  section, and the leak check reading the pack directory.
- The pack carries no path, key, model name or real name; the user brings
  their own LLM.
- **A long `--json` run must still show it is alive.** Stdout holds one JSON document,
  so a 45-minute scan prints nothing, and a working run looks exactly like a hung one.
  Send progress lines to STDERR (for example `scanned 40/95 files`), keep stdout
  clean, and add a test that stdout stays a single document while stderr receives
  progress.
- Verify any external link the README gains (`curl -o /dev/null -w '%{http_code}'`)
  before it ships.
