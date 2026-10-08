---
title: "pi: prompt template or skill?"
date: 2026-08-25T01:13:46+02:00
tags:
  - ai
  - dev
  - pi
---

**Problem statement**: I often type `commit (only) what you changed` in coding
agent harnesses. Can I make an abbreviation out of it?

[Pi](https://pi.dev/) turns a Markdown file in `~/.pi/agent/prompts/` into a
/slash command. This one gives me `/commit`:

```markdown {filename="~/.pi/agent/prompts/commit.md"}
---
description: Commit files changed in this turn without pushing
---
Commit what you changed (only). DO NOT push.
```

```shell
% find ~/.pi/agent/prompts -maxdepth 1 -type f -print -exec sh -c 'printf "%s\n" "--- $1"; cat "$1"' _ {} \;
/Users/thiago.perrotta/.pi/agent/prompts/commit.md
--- /Users/thiago.perrotta/.pi/agent/prompts/commit.md
---
description: Commit files changed in this turn without pushing
---
Commit what you changed (only). DO NOT push.
```

In Pi, a [prompt template](https://pi.dev/docs/latest/prompt-templates) is fixed
prompt expansion. It is right for a short, stable request:

> Prompt templates are Markdown snippets that expand into full prompts. Type
> /name in the editor to invoke a template, where name is the filename without
> .md.

A [skill](https://agentskills.io/home) is a capability package. Its description
is available at startup, but Pi loads its
[`SKILL.md`](https://pi.dev/docs/latest/skills) only when task matches or I run
`/skill:name`. A skill can carry scripts, references, setup, and a workflow that
branches on state:

> Skills are self-contained capability packages that the agent loads on-demand.
> A skill provides specialized workflows, setup instructions, helper scripts,
> and reference documentation for specific tasks.

A commit flow with checks, generated files, partial staging rules, or project
specific policy deserves a skill. This one is a couple of words and one
constraint, so I choose to keep it simple.
