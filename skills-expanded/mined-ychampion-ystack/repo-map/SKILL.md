---
name: repo-map
description: >-
  Map an unfamiliar codebase onto one page: what it is, how to install, run and test it (each command
  actually run), the entry points, the main data flow traced through real files, where things live,
  and the traps. Use for "explain this repo", "onboard me", "how is this codebase organized", "where
  do I start", "map this project", or before your first change in a repo you haven't worked in.
---

# Repo map

A newcomer, human or agent, needs four answers before changing anything: what this is, how to run it,
where a request goes, and what will bite. This skill answers them on one page, and every command on
it has been run.

## When it applies

- First work in a repo you don't know.
- Someone asks how a project is put together.
- A handoff where the next agent starts cold.

## Procedure

### 1. Skim the surface (5 minutes, no deep reading)

README, the manifest files (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, ...), the
top-level folders, CI config, Dockerfiles, `.env.example`, any `AGENTS.md` / `CLAUDE.md` /
`CONTRIBUTING.md`. `git log --oneline -20` and the most-changed files
(`git log --name-only --since=6.months --format= | sort | uniq -c | sort -rn | head -20`) show where
the live work is.

### 2. Run it

Find and run install, build, test and start. Record the exact commands that worked, how long they
took, and anything you had to fix or set (env vars, services, versions). A command you didn't run
goes on the map marked "not run".

### 3. Find the entry points

Where execution starts: `main` functions, server route tables, CLI command definitions, job and queue
handlers, exported library API, scheduled tasks. List them with file paths.

### 4. Trace one real flow end to end

Pick the most important user action (a request, a command, a job). Follow it from entry point to
storage and back, naming each file and function it passes through. One traced flow teaches more than
a list of every folder. For a large repo, trace a second flow in parallel with a subagent if your
host has them.

### 5. Note the traps

Generated code not to edit by hand, surprising conventions, slow or flaky tests, required services,
environment differences, things that look dead but are loaded by name.

### 6. Write the page

```
# <project>: map   (as of <commit>, <date>)
What it is: <two sentences>
Run:  install <cmd> | build <cmd> | test <cmd> (<time>) | start <cmd>
Needs: <services, env vars, versions>
Entry points: <path - what starts here>
Flow: <action>: <file:function> -> <file:function> -> ... -> <storage>
Layout: <folder - what lives there>, only folders that matter
Traps: <one line each>
Live areas: <most-changed files lately>
```

Keep it to one screen. Save it where the user asks, or in the session's scratch space.

## Rules

- Every command on the map was run, or is marked "not run".
- Paths and function names, not descriptions like "the auth layer".
- Date the map with the commit; it goes stale.
