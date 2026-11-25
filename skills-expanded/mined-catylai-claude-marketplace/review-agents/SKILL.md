---
name: review-agents
description: "Audits subagent definitions and reports which agents should be skills, which descriptions an orchestrator can't route on, which rule lists should become examples, and which frontmatter fields are ignored. Use after adding or changing agents, or when an orchestrator keeps picking the wrong one. Read-only. Not for skills (use review-skills); not for hooks (use review-hooks); not for a whole-configuration sweep (use config-audit)."
when_to_use: "audit my agents, review agent definitions, should this agent be a skill, agent description rewrite, orchestrator picks the wrong agent"
argument-hint: "[agents directory, or pasted agent file content; defaults to this repo's agents plus ~/.claude/agents/]"
allowed-tools: Read, Glob, Grep
disallowed-tools: Write, Edit, NotebookEdit
context: fork
license: MIT
---

# Agent Roster Audit

Target: $ARGUMENTS

Evaluate every agent definition in scope for packaging, frontmatter, prompt quality and routability.
This is a report; the caller applies the fixes.

## Step 1 — Resolve the target and read the roster

- **A path:** read every `*.md` agent file under it.
- **Empty:** glob `agents/*.md`, `.claude/agents/*.md` and `plugins/**/agents/*.md` in the working
  directory, plus `~/.claude/agents/*.md`.
- **Pasted agent content** (Cowork, or no checkout): audit that text. This fork can't see the
  conversation, so pasted content only arrives through the argument.
- **Nothing found:** return `No agent definitions found under <target>` plus the globs you tried,
  and stop.

Read each file in full before proposing a change to it. List the skills directories too: a
"convert to skill" finding needs to know whether that skill exists, and an overlap finding needs both
sides.

## Step 2 — Packaging

For each agent, decide keep, convert to skill, or delete. The deciding question is whether it needs
its own tool set, model, turn budget and context window, or whether it is Claude following a
procedure.

- A reviewer with `tools: Read, Grep` spawned for an isolated pass → **keep**. Tool narrowing or a
  separate window each justify it.
- A list of commit conventions with no tool restriction → **convert to skill**.
- One agent analyses and another publishes → **keep both**. Flag overlap only for the same analysis.
- No inbound reference and a scope another agent covers → **delete**, naming the agent that covers it.

## Step 3 — Frontmatter

- **Ignored fields.** Agents shipped in a plugin ignore `hooks`, `mcpServers` and `permissionMode`.
  Flag any plugin agent that sets them, and name what the author expected them to do. The field
  looks active and isn't.
- **`tools`:** least privilege, plain tool names. A read-only reviewer should also set
  `disallowedTools: Write, Edit`. An agent that should not spawn subagents should leave `Agent` out
  of `tools`.
- **`maxTurns`:** present and consistent with any tool-call budget the body states. At the limit, the
  caller receives the output marked partial.
- **`model`:** set deliberately, or omitted to inherit.
- **`skills:`** entries must name skills that exist. A dangling one is dropped with no visible
  error; only the debug log records it. In a plugin agent, write another plugin's skill as
  `plugin:skill`; a bare name resolves within the agent's own plugin. To confirm, run with `--debug`
  and spawn the agent: each resolved entry logs `Preloaded skill '<entry>'`, and a dangling one logs
  `Skill '<entry>' specified in frontmatter was not found`.

## Step 4 — Rules to examples

Look for sections that enumerate "if X then Y" conditions where the underlying call is a judgement.
Replace them with two to four concrete examples that differ in situation but show one principle.
Keep explicit rule tables where the agent is a gate applying a fixed checklist. For each section you
flag, draft the replacement examples.

<example>
Rule block:
- If the branch starts with fix/, use fix as the type
- If there is no issue key, use the component as the scope
- If only tests changed, use test regardless of the branch

Replacement:
Branch feat/PROJ-123-retry-logic → feat(PROJ-123): add queue retry with backoff
Branch fix/api-null-pointer → fix(api): handle null in the stats aggregator
Branch feat/PROJ-124-dashboard, only tests changed → test(PROJ-124): cover dashboard edge cases
</example>

## Step 5 — Description as a routing signal

A strong description says when to pick the agent, what triggers it, and what it returns. It adds
"use proactively" if the agent should auto-delegate.

<example>
Weak: "Helps debug problems."
Strong: "Read-only root-cause analysis. Tests falsifiable hypotheses against evidence and returns a
ranked diagnosis. Use proactively when a test fails for an unclear reason."
</example>

Also flag names too generic to tell apart from a neighbour, two descriptions that match the same
request, and bodies long enough that detail should move into a referenced skill.

## Step 6 — Verify before reporting

For every delete or orphan claim, grep for the agent name across agents, skills, commands and
instruction files, excluding the agent's own file. Drop the claim if anything references it.

## Report

```markdown
# Agent audit: <target> (<n> agents)

## Findings
| # | Severity | Agent | Path | Problem | Fix |
|---|----------|-------|------|---------|-----|

## Example substitutions
<per flagged section: file, heading, current rule block quoted, drafted examples>

## Frontmatter rewrites
<per agent: current description, proposed description, other field changes>

## Not checked
<paths that could not be read, or "none">
```

Severity is `critical` (an ignored or dangling field the agent depends on, or write access on a
read-only role), `warning` (misclassified, weak routing signal) or `minor`. Sort by severity, with
one sentence of rationale each. A healthy roster gets a short report with an empty findings table.
