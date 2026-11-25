---
name: coding-agent-hardening
description: >-
  Review the configuration of a coding agent — its skills, tools, hooks, MCP
  servers and autorun rules — for ways a repository can turn the agent against
  its operator. Use when asked to audit agent configuration, review a SKILL.md
  or AGENTS.md, assess MCP server risk, check tool allowlists, or secure
  developer AI tooling.
allowed-tools: Read, Grep, Glob
---

# Securing the developers' coding agents

A coding agent reads the repository it is working in. That makes every file in
the repository an input to a system that can run commands — and the agent's own
configuration is the control surface.

The threat is not that the agent is malicious. It is that instructions in a
repository are indistinguishable, at the token level, from instructions from
the operator.

## When to use this

Auditing `.claude/`, `AGENTS.md`, `.github/`, MCP configuration, CI that
invokes an agent, or any repository that a coding agent will open.

## Procedure

**1 — Inventory the surface.** List every file that reaches the agent's context
automatically: skill files, agent instruction files, hooks, MCP server
definitions, settings with tool allowlists, and any file the agent is told to
read on startup. Record which are **operator-controlled** (a maintainer wrote
them) and which are **content** (a contributor, a dependency, or a fetched
document can influence them).

**2 — Find the confusion.** For every content-controlled input, ask: if this
file contained an instruction, would the agent follow it? Grade each:

| Grade | Meaning |
|---|---|
| `isolated` | content is quoted as data and never read as instruction |
| `advisory` | content can influence phrasing but not tool calls |
| `directive` | content can cause a tool call |

Any `directive` path from unreviewed content is a finding, and its severity is
whatever the agent's most powerful allowed tool can do.

**3 — Check the allowlist against the blast radius.** For each pre-approved
tool, state the worst outcome of one call with attacker-chosen arguments. A
pre-approved `Bash` with unrestricted arguments is equivalent to pre-approving
everything else; note it as such rather than listing it as one item.

**4 — Check the hooks.** Hooks run without the model's judgement. A hook that
executes repository-supplied code (a script path from a config file, a test
command from `package.json`) runs attacker-supplied code the moment the agent
opens the repository. This is the highest-value finding in most reviews.

**5 — Check the MCP servers.** For each: who operates it, what it can reach,
whether its tool descriptions are trusted input (they are model-visible text
from a third party), and whether its credentials exceed the task.

**6 — Check the escape hatches.** Can a human stop it? Is there an audit trail
that survives the agent's own actions? An agent that can edit its own logs has
no logs.

## Example

**Input** — the fixture committed at the top of [`scripts/coding_agent_hardening.py`](scripts/coding_agent_hardening.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
tool          writes  scope    reversible  inner loop?
----------------------------------------------------------
read_file     False   self     True        True
write_file    True    project  True        True
run_tests     True    self     True        True
run_shell     True    tenant   False       True
git_commit    True    project  True        True
git_push      True    project  False       False
```

The run continues past this. `test_skills.py` executes the script on every
build, **with no model configured** — so what CI proves is that it runs and
refuses legibly, not that it prints these lines. The output above is a recorded
run against a real model, and nothing re-diffs it: a model's answer is not
reproducible, and this repository does not claim otherwise anywhere it can be
checked.

## Output contract

```json
{
  "surface": [{"path": "str", "control": "operator|content", "auto_loaded": true}],
  "findings": [
    {"kind": "prompt_injection|overbroad_tool|unsafe_hook|mcp_trust|no_audit",
     "path": "str", "grade": "isolated|advisory|directive",
     "worst_case": "str", "severity": "critical|high|medium|low",
     "fix": "str"}
  ],
  "allowlist_review": [{"tool": "str", "worst_single_call": "str", "bounded": true}]
}
```

## Failure modes

- **Reviewing the agent's instructions and not its inputs.** The instructions
  are the part you control; the inputs are the part an attacker controls.
- **Treating tool descriptions as trusted.** They are third-party text placed
  directly in the model's context.
- **Assuming a human reviews every action.** Check whether the mode in use
  actually prompts, and audit the configuration that decides that.
- **Rating an injection finding by the text of the injection.** Rate it by what
  the allowlist permits.
