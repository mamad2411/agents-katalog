---
name: echolot
description: The door to echolot, for Android performance regressions — from a Perfetto trace down to a place in the code. Use when cold start regressed, scrolling stutters, TTI grew, a benchmark dropped, or there is a .perfetto-trace to read; also for "why is startup slow", "where does main thread time go", "what is burning CPU". Reads where the project stands and takes the next step.
---

# echolot

echolot turns a Perfetto trace into about twenty rows of facts. **Never open
the trace yourself**: no TraceProcessor, no SQL, no reading `.perfetto-trace`.
The report is what you read.

## The tool comes first

Run `echolot --version`. If there is no such command, echolot is not
installed: it is a Python tool this plugin does not bring. Tell the human to
install it, `pipx install echolot` or `uv tool install echolot`, and stop: the
install needs the network and writes outside the project. If a command below
says a verb, flag or topic does not exist, the installed echolot is older than
this plugin: the human upgrades it, `pipx upgrade echolot` or
`uv tool upgrade echolot`.

Run every `echolot` command on its own: never chained with `&&` or `;`, and
with the trace files named rather than globbed
(`ls .echolot/traces` lists them). A host's rule that lets echolot out of its
sandbox covers a command line that is echolot alone; `git status && echolot
doctor -q`, or a `*.perfetto-trace`, keeps the whole line inside.

## Then ask the tool where things stand

```bash
echolot                 # where things stand, and what is next
```

Show the output to the human as it is, then act on its `next` line
(`echolot status --next` prints the word alone):

| `next` | what you do |
|---|---|
| `init` | `echolot init --for plugin`, then `echolot` again: the .gitignore lines, and no `.claude/`. In Codex, `echolot init --for plugin,codex`: it also writes the rule that lets echolot out of the sandbox, which Codex allows only from outside it, so ask to run it there. Never plain `echolot init`, whatever else says it: that installs `.claude/`, and the skills would load twice |
| `upgrade` | show the `layer` line as it is, it names the upgrade, and stop |
| `doctor` | `echolot doctor`: show what failed, and stop. A sandbox's refusal names its own way out |
| `setup` | the `echolot-setup` skill, or `echolot guide setup` where the host does not list it |
| `fix-config` | show the error, ask the human to fix `echolot.yml`, stop |
| `resume-or-new` | show the recap `echolot` printed and ask: carry on (`echolot hunt --resume`, then the `echolot-hunt` skill), something new (the `echolot-hunt` skill with their question), or the report alone (`echolot report`) |
| `init-force` | files in `.claude/` differ from the package: ask, then `echolot init --for plugin` (`--for plugin,codex` in Codex); `.claude/` is the human's to remove; go on as for `hunt` |
| `fix-settings` | show the `layer` line; the human fixes the file; go on as for `hunt` |
| `hunt` | the `echolot-hunt` skill, or `echolot guide hunt` where the host does not list it |

## With an argument

The argument wins over the state. `setup`, `hunt <words>` and `reflect` are
the skills of those names; `hunt <words>`, or free text about slowness, starts
a hunt with those words as the question, and the open investigation is not
asked about. `init` is `echolot init --for plugin`, and `--for plugin,codex`
in Codex. Any other word is the `echolot` command of that name: run it, show
the output.

## Asking the human

Where a step says ask, ask in plain words and wait for the answer, with your
host's question tool if it has one. Never answer for the human to move on.

## Before reading a report yourself

Read `echolot guide` once: how to read the report through `echolot report`,
what a silent detector means, and how a finding leads to a file. The
installed echolot prints it, so it matches the version you are running. A
hunt skips it: the reports are the loop's, read in its subagent.
