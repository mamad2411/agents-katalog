---
name: setup
description: Use when the person asks you to set up Ork, install it, or get started with it in a repository - checking it's installed, setting up the project, making Ork's tools available to you, and a first workflow.
---

# Setting up Ork

Ork runs workflows on the person's machine with their own accounts. Setting it
up changes their machine and their repository, so say what each step does and
ask before it. Work through these in order, and stop where they say no.

## 1. Check

```sh
ork --version
ork doctor
```

- **No `ork`:** it needs Node 24.20 or later (`node --version`). The install is
  `npm install --global @krapht/ork`; show it and run it only when they say
  yes. The guide:
  https://github.com/mimshins/ork/blob/main/docs/getting-started/installation.md
- **Read `ork doctor` to them.** It needs git, a git repository with a commit,
  and one agent driver. Don't run `git init` or a commit without asking.
- **A driver not ready:** they log in themselves, with `claude auth login`, or
  by setting `ANTHROPIC_API_KEY` or a cloud provider in their own shell (either
  makes the claude-code driver ready), or with another driver's own tool
  (`opencode auth login`, `cmd login`, `codex login`). Never ask for a key,
  never take one pasted to you, and
  never write one into a file or a command. `gh` and `aws` are optional, and
  their logins are their own too (`gh auth login`, `aws sso login`).

## 2. The project

- **`ork init`** keeps Ork's files in the repository, in `.ork/`, committed with
  the code. It adds `.ork/runs/` to `.gitignore`, links `.claude/` and similar
  folders to `.ork/`, and writes a starter workflow, `hello`.
- **`ork register`** keeps them beside it, in `~/.ork/projects/<id>/`, and
  writes nothing into the repository. For a repository whose process isn't
  theirs to change, or to try Ork first.

Explain both and ask which. Skip the question when the repository decides it: a
`.ork/` folder means `ork init` has run (`ork projects` lists what's
registered). Neither overwrites a file.

## 3. Make Ork available to you

If Ork's tools (`workflows`, `check`) already answer you, skip this. Otherwise,
by where you run, and asking before each change to a config:

- **Claude Code:** Ork's plugin brings the skills and the tools. The person
  types these themselves:

  ```
  /plugin marketplace add mimshins/ork
  /plugin install ork@ork
  ```

  Or, in a project set up with `ork init`, the skills in the repository for
  everyone who clones it, then the tools:

  ```sh
  ork init --skills
  claude mcp add ork -- ork mcp
  ```

  New tools start when they restart Claude Code or reconnect `ork` in `/mcp`;
  so does the plugin's, once `ork` is installed.

- **Another MCP client:** add a server named `ork` with command `ork` and args
  `["mcp"]` to its MCP config, where its own docs say. Its tools find the
  project by its id, from `ork projects`.
- **A shell only:** use the CLI. `ork --help` and each command's `--help` say
  what it takes.

## 4. A first workflow

For workflows that fit their project, point them at `ork onboard`. It asks
questions and has no flags for the answers, so they run it in their own
terminal; don't run it for them. It shows the most it can spend and asks before
any spend, writes only on a branch, and never merges.

Or offer to write one for a task they name. Follow `/ork:write`, check each draft
(the `check` tool, or `ork validate <file>`) until it has no error, then save
it. Don't start it: a run spends their money. Start it only when they say so,
in the background with its inputs (`start_run`, or
`ork run <name> --detach --input name=value`), and follow it with `/ork:run`.

## 5. Show them `ork ui`

Tell them to run `ork ui` in their own terminal: their runs, graphs and logs in
the browser, and where they answer what a run asks.

## Never

- Ask for, store or pass on a password, key or token.
- Answer a run's decision: they answer in `ork ui` or with `ork decide` in
  their own terminal.
- Install, edit a config, or start a run without a yes.
