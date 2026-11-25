---
name: agent-hook-guard
description: Turns one problem that the reviews found into one hook of the agent. A hook is a check that the agent tool runs by itself before or after a tool call or at the end of a turn. The skill shows the hook first with a diagram, writes it only after a yes, tests it by forcing the error and then shows it in a real run. Use it whenever the user asks for a hook, an automatic guard, "something that stops this from happening again" while the agent works, or wants a red team, verification or retrospective finding enforced by the machine instead of by a rule the model must remember.
---

# Agent hook guard

A rule in AGENTS.md works only when the model remembers it. A hook runs every time. This skill adds one hook for one problem.

An agent hook runs inside the agent tool, for example a Claude Code hook in its settings file, or an OpenCode plugin that listens to tool events. A git hook is not an agent hook. Use a git hook or CI only when the user asks for one. If the project's agent has no hooks, say so and propose a test or a command instead (`session-retrospective-rules`).

## 1. Choose one problem

Read the findings: `.scratchpad/<slug>/redteam-report.md`, `verification-report.md`, `browser-test-report.md`, or the moments of a retrospective. Choose the one problem that a hook would have stopped and that is easiest to explain. A good candidate:

- A program can check it, without judgment: a file in the wrong folder, a commit with failing tests, an edit to a generated file, a forbidden command.
- Happened, or can happen again, in this project.
- Has a check that runs in a few seconds.

If the first candidate needs a long explanation, pick a simpler one. The user must understand the hook from one sentence.

## 2. Show it before you write it

In the chat, give:

- The problem, with its finding id and evidence.
- When the hook runs (before a tool call, after an edit, at the end of a turn) and what it checks.
- What the agent sees when the check fails: blocked, or a warning it must act on.
- One diagram:

```text
agent edits a file
      │
      ▼
hook: after edit ── file is an order fixture? ── no ──▶ continue
                              │ yes
                              ▼
                   run the fixture check ── fails ──▶ block, show the error
```

Then ask. Do not write the hook without a yes.

## 3. Write it and force the error

1. Write the hook in the project's agent configuration, not in the user's personal settings, unless the user asks. Keep the logic in a small script in the repository, so that a person can read, test and run it by hand.
2. Run the script by hand with an input that must fail, and with one that must pass.
3. Look for false positives: run it on inputs that are close to the bad case but correct. Users switch off a hook that blocks good work.
4. Commit the hook and its script (`git-commit-organizer`).

## 4. See it in a real run

The hook works only when the agent tool runs it. Start a short session of the agent (in a new session, or a headless run if the agent has one) and ask it for the action that the hook must stop. Show the output. If the agent tool does not call the hook, fix the configuration and try again.

## 5. Report

Write it in `.scratchpad/<slug>/hook-report.md`: the problem and its source, the diagram, the files, the forced-error results, the real-run output, and the cases the hook does not cover.
