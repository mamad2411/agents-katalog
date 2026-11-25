---
name: review-skills
description: "Audits a directory of SKILL.md files and reports which skills fail to trigger, should be agents, misuse `context: fork` or invocation flags, or overlap. Use after adding or changing skills, before publishing a plugin, or when a skill never fires. Read-only. Not for agent definitions (use review-agents); not for hooks (use review-hooks); not for a whole-configuration sweep (use config-audit)."
when_to_use: "audit my skills, review SKILL.md quality, why does my skill never trigger, should this skill be an agent, rewrite a skill description, prune duplicate skills"
argument-hint: "[skills directory, or pasted SKILL.md content; defaults to this repo's skills plus ~/.claude/skills/]"
allowed-tools: Read, Glob, Grep, Agent
disallowed-tools: Write, Edit, NotebookEdit
context: fork
license: MIT
---

# Skill Authoring Audit

Target: $ARGUMENTS

Read every `SKILL.md` in scope and report on classification, context mode, invocability, frontmatter
and description quality. This is a report; the caller applies the fixes.

## Step 1 — Resolve the target

- **A path:** audit `SKILL.md` files under it.
- **Empty:** glob `skills/*/SKILL.md`, `.claude/skills/*/SKILL.md` and `plugins/**/skills/*/SKILL.md`
  in the working directory, plus `~/.claude/skills/*/SKILL.md`. The `**` matters: plugins can nest
  under category directories.
- **Pasted SKILL.md content** (Cowork, or no checkout): audit that text. This fork can't see the
  conversation, so pasted content only arrives through the argument.
- **Nothing found:** return `No SKILL.md files found under <target>` plus the globs you tried, and stop.

Also read the repo's authoring conventions (`CLAUDE.md`, any plugin standard) and list the agent
definitions beside the skills. "Should be an agent" and "duplicates an agent" need that roster.

## Step 2 — Evaluate each skill

With more than about a dozen skills, split them by name prefix or theme across three or four `Agent`
calls in one message. Give each agent its group and this step verbatim. If `Agent` is unavailable (the
nesting depth limit, or a surface without subagents), do the pass inline.

Ask six questions per skill:

1. **Type:** keep, convert to agent, merge, or delete. A skill becomes an agent when it runs in
   parallel with siblings, needs its own `model`/`maxTurns`, or is picked from a roster. Delete only an
   exact duplicate or one that nothing references and nobody invokes.
2. **Context mode:** `context: fork` runs the body as a subagent task with no conversation history.
   It suits a self-contained task that returns a result. Reference or guideline content should be
   inline, because a fork given only guidelines has nothing to do. A fork also loses
   `AskUserQuestion` and can't wait for the user, so interactive skills should run inline.
3. **Invocability:**
   - `disable-model-invocation: true` removes the description from context, so only the user can
     invoke the skill. That is right for side-effecting workflows, and it makes `when_to_use` dead
     weight.
   - `user-invocable: false` hides the skill from the `/` menu, but Claude can still invoke it.
   - Only `disable-model-invocation` stops the Skill tool.
4. **Frontmatter:**
   - `name` matches the directory, is kebab-case, and doesn't contain `claude` or `anthropic`
     (the Agent Skills spec reserves both).
   - `allowed-tools` pre-approves tools; it doesn't restrict them. Flag grants the body never uses,
     and broad ones (`Bash`, `Bash(git *)`, `Write`) on read-only skills. `disallowed-tools` is the
     field that restricts.
   - `argument-hint` without `$ARGUMENTS` in the body.
   - Unknown keys.
5. **Description:** says what the skill does and when to use it, in the user's words, with a
   "not for X (use Y)" boundary. Check four things:
   - The trigger comes first: the listing truncates `description` + `when_to_use` at a fixed cap.
   - Flag an empty, truncated, or dangling-block-scalar description as critical, since discovery
     silently breaks.
   - Flag topic-list openers.
   - Flag descriptions with no trigger phrasing.
6. **Overlap:** two skills whose descriptions both match one request. Merge them, or sharpen both
   boundaries.

<example>
Description: "Helps with testing."
Verdict: needs-rewrite (warning). It says what the skill is, gives no trigger and no boundary.
</example>

<example>
Description: "Runs the project's migration checklist before a schema change ships. Use when adding or
altering a table. Not for query tuning (use db-perf)."
Verdict: good. Trigger first, user vocabulary, one anti-trigger.
</example>

Each agent returns JSON:

```json
[{"skill": "name", "path": "skills/name/SKILL.md",
  "type": "keep|convert-to-agent|merge|delete",
  "context": "justified|should-be-inline|should-be-fork|n-a",
  "invocability": "correct|needs-change",
  "description": "good|needs-rewrite|truncated|missing",
  "severity": "critical|warning|minor|none",
  "proposed_description": "only when needs-rewrite, truncated or missing",
  "notes": "one sentence"}]
```

## Step 3 — Verify before reporting

For every `delete` or orphan claim, grep for the skill name across skills, agents, commands and
instruction files, excluding the skill's own directory. Drop the claim if anything references it. For
every flagged frontmatter key, re-read that line.

## Step 4 — Report

```markdown
# Skill audit: <target> (<n> skills)

## Findings
| # | Severity | Skill | Path | Problem | Fix |
|---|----------|-------|------|---------|-----|

## Description rewrites
<per skill: current description quoted, proposed replacement (trigger first, one anti-trigger)>

## Merge candidates
| Skill A | Skill B | Overlap | Recommendation |
|---------|---------|---------|----------------|

## Not checked
<paths that could not be read, or "none">
```

Severity is `critical` (breaks discovery or runs with the wrong privileges), `warning`
(misclassified, weak trigger, over-broad grant) or `minor`. Sort findings by severity. Each gets one
sentence of rationale. A healthy tree gets a short report with an empty findings table.
