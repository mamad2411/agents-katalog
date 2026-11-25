---
name: config-audit
description: "Audits a repository's whole Claude Code configuration and reports ranked findings; with --fix, applies the ones you approve. Use for a periodic sweep, when onboarding a repo, or before handing a configuration to someone else. Covers CLAUDE.md placement and hierarchy, skills, agents, hooks, and settings precedence, including permission rules that never fire or grant too much. Not for one dimension alone (use review-skills, review-agents or review-hooks)."
argument-hint: "[--fix] [path to a repo or .claude directory; defaults to the current directory]"
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Agent, AskUserQuestion
license: MIT
---

# Configuration Audit

Arguments: $ARGUMENTS

Audit one repository's configuration across every mechanism, and report ranked findings. With
`--fix` in the arguments, present the findings for approval and apply the chosen ones. Without it,
make no edits. The skill runs inline, so the approval step can ask the user directly.

## The standard: pick the mechanism by how hard the rule must bind

| Mechanism | Binds | Right for |
| --- | --- | --- |
| `CLAUDE.md` | By being read, on every turn | Project facts, conventions, orientation |
| `SKILL.md` | When selected | A repeatable multi-step procedure |
| `settings.json` permissions | Every matching tool call | Allow, ask or deny a tool or command shape |
| Hooks | Every matching event | A condition that must be checked, or an action that must happen |

Three rules follow from it:

1. **A procedure is a skill.** Steps, an order and a finish condition belong in a `SKILL.md`, loaded
   on demand. In `CLAUDE.md` they are paid for on every turn and followed only approximately.
2. **A must-hold policy is a permission or a hook.** Written instructions hold usually. A rule
   phrased "never", "always" or "before X, do Y" is a candidate for a deny entry or a hook.
3. **Scope is a cost.** Root `CLAUDE.md` content enters every turn. Guidance for one directory or
   file type belongs in a nested `CLAUDE.md` there, or in the skill that covers that work.

## Step 1 — Map the surface

The target is the path in the arguments (ignoring `--fix`), or the current directory. Glob it for:

- `**/CLAUDE.md` and `**/CLAUDE.local.md`;
- `**/SKILL.md` and agent files (`agents/*.md`, `.claude/agents/*.md`, `plugins/**/agents/*.md`);
- `**/settings*.json` and `**/hooks.json`.

Also include `~/.claude/CLAUDE.md` and `~/.claude/settings.json` if they exist. Skip `node_modules`.

- **No readable files** (Cowork, or no checkout): ask the user to paste the `CLAUDE.md`, settings and
  hook files, and wait. Audit only what they paste, and say which mechanisms went unseen.
- **No configuration at all:** say this is a first-time setup rather than an audit. Offer to
  scaffold a project `CLAUDE.md` and one skill for the most repeated procedure, and stop.

## Step 2 — Dimension audits, in parallel

In one message, spawn three `Agent` calls. Each prompt gives the target and the file list from Step 1,
and says: "Read `<file>` and follow it as your instructions. Its `Target:` line means <target>, and
script paths in it are relative to the plugin root `${CLAUDE_PLUGIN_ROOT}`. Read-only: edit nothing.
Return its report."

- Skills: `${CLAUDE_SKILL_DIR}/../review-skills/SKILL.md`
- Agents: `${CLAUDE_SKILL_DIR}/../review-agents/SKILL.md`
- Hooks: `${CLAUDE_SKILL_DIR}/../review-hooks/SKILL.md`

In pasted mode (Step 1), there are no files to list: put the pasted text for that dimension inline
as the `Target:` in each prompt, so the subagent audits the text instead of searching a directory.
Reading the three files by path needs the plugin on disk. Where it isn't (a synced or web install,
where `${CLAUDE_SKILL_DIR}` is not expanded), invoke `review-skills`, `review-agents` and
`review-hooks` with the Skill tool instead, passing the pasted text as the argument. If neither
works, list the dimension under "Not checked".

While they run, do Steps 3 and 4 yourself. If `Agent` is unavailable (the depth limit, or a surface
without subagents), run each of those three files inline in turn after Step 4.

## Step 3 — Settings and permissions layering

Read every settings file in scope, and report each finding with the file, key path and effective
value.

1. **Precedence.** Managed settings beat command-line settings. Those beat
   `.claude/settings.local.json`, which beats `.claude/settings.json`, which beats
   `~/.claude/settings.json`. List keys like `permissions.allow` merge across files instead of
   overriding. For each scalar key set in more than one file, state which file wins and whether that
   looks intended.
2. **Dead permission rules.** Deny is checked before ask, and ask before allow. Report rules that can
   never fire because an earlier-checked rule already decides the case.
3. **Over-broad grants.** A whole-tool allow where one command shape was meant, or a wildcard that
   admits far more than its motivating example. State what the rule actually permits.
4. **Machine-specific values** in shared files: absolute home paths, local hosts.
5. **Secrets.** Any literal credential, token or key in a tracked file. This outranks everything else.

The rule-to-hook question ("this policy should be enforced") is owned by the hooks audit's Lens 3.
Here, only flag destructive operations with neither a deny rule nor a hook.

## Step 4 — Placement and hierarchy

Apply the standard above to every `CLAUDE.md`:

- **Placement:** multi-step procedures written as prose, and passive descriptions of an action the
  model is supposed to take.
- **Scope:** root-level guidance that only governs one directory or file type.
- **Hierarchy:** a nested `CLAUDE.md` that contradicts or restates its parent, machine-specific
  content in a shared file, or the same instruction in three places.

## Step 5 — Cross-cutting pass

Once the Step 2 reports arrive, look for what no single dimension can see:

- **Swapped packaging:** a skill that should be an agent, and an agent that should be a skill.
- **Orphans:** a hidden or model-disabled skill with no inbound `Skill()` call, `skills:` entry or
  mention in any instruction file.
- **Enforcement contradicted by prose:** a deny rule for an operation that a skill or `CLAUDE.md`
  tells the model to perform.
- **Duplicated guidance:** one standard inlined in several skills that should be one reference.

## Step 6 — Verify

For every orphan, delete or contradiction finding, grep for the name or rule across skills, agents
and instruction files, excluding its own file. Drop anything the grep disproves. Re-open the file and
line for every critical finding.

## Step 7 — Report

```markdown
# Configuration audit: <target>

## Per dimension
- Skills:    <n> (<critical>/<warning>/<minor>)
- Agents:    <n> (<critical>/<warning>/<minor>)
- Hooks:     <n> (<critical>/<warning>/<minor>)
- Settings:  <n> (<critical>/<warning>/<minor>)
- Placement: <n> (<critical>/<warning>/<minor>)

## Findings
| # | Severity | Dimension | File:line | Problem | Fix (target mechanism) |
|---|----------|-----------|-----------|---------|------------------------|

## Needs a decision
<genuine trade-offs, with options and costs; not decided here>

## Not checked
<dimensions or paths skipped, and why, or "none">
```

Severity is `critical` (a secret, a fail-open gate, or a must-hold policy with no enforcement),
`warning` (dead or over-broad rule, misplaced procedure, contradiction) or `minor` (scope cost,
duplication). Sort by severity. Each finding gets one sentence of rationale. A healthy configuration
gets a short report. Without `--fix`, stop here.

## Step 8 — Apply approved fixes (`--fix` only)

Ask with `AskUserQuestion` in multi-select form, one option per finding, most severe first. Batch
across several questions when there are more findings than fit in one. Write nothing before the user
answers. If `AskUserQuestion` is unavailable, list the findings by number, ask the user to reply with
the ones to apply, and wait.

Make the minimal edit for each approved finding:

- **Prose to enforcement:** write the permission entry, or wire the hook where the repo already keeps
  hooks. If the hooks belong to an installed plugin, say so and stop rather than creating a parallel
  hook surface.
- **Prose to skill:** scaffold the `SKILL.md` in the repo's frontmatter convention, move the
  procedure, and leave a one-line pointer where the prose was.
- **Unscoped instruction:** move it to the nested `CLAUDE.md` or skill it belongs in, and delete the
  original.
- **Contradiction:** amend or remove the losing statement rather than adding a third one.

Follow the repo's own change procedure (version bumps, validation) for every file you touch. Then run
the repo's validation command if it has one, and re-grep each edited file to confirm the fix landed.
End with a list of files changed and findings deferred.
