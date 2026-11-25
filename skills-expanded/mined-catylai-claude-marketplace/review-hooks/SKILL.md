---
name: review-hooks
description: "Audits hook scripts together with their settings registrations and reports costly model calls, duplicated handlers, written rules that should be hooks, and stale or mis-timed entries, each with file and line. Use when hooks are slow or fire on the wrong files, after changing hooks, or as a periodic sweep. Can execute a hook against a synthetic payload, after a permission prompt. Not for skills (use review-skills); not for permission layering (use config-audit)."
when_to_use: "audit my hooks, review hooks.json, hooks are slow, hook fires on the wrong files, should this rule be a hook, dead hook, hook timeout"
argument-hint: "[hooks directory, settings file, or pasted hook config; defaults to the repo's .claude/ and plugin hooks plus ~/.claude/]"
allowed-tools: Read, Glob, Grep, WebFetch(domain:code.claude.com), Agent, Bash(bash "${CLAUDE_PLUGIN_ROOT}/scripts/hooks/validate-hook-registration.sh" *), Bash(bash "${CLAUDE_PLUGIN_ROOT}/scripts/hooks/lint-hook-source.sh" *)
disallowed-tools: Write, Edit, NotebookEdit
context: fork
license: MIT
---

# Hook Audit

Target: $ARGUMENTS

Audit a hook system end to end: the registrations, the scripts they point at, and the written rules
the hooks are meant to enforce. This is a report; the caller applies the fixes.

## Step 1 — Resolve the target

- **A path:** audit the hook registrations and scripts under it.
- **Empty:** collect every registration:
  - the `hooks` blocks in `.claude/settings.json`, `.claude/settings.local.json`,
    `~/.claude/settings.json` and any managed settings file;
  - each plugin's `hooks/hooks.json`;
  - `hooks:` in skill and agent frontmatter.

  Then read each script those entries run, the project's `CLAUDE.md`, and the files it references.
- **Pasted hook config or scripts** (Cowork, or no checkout): audit that text and skip Step 2. This
  fork can't see the conversation, so pasted content only arrives through the argument.
- **No registrations found:** return `No hook registrations found under <target>` plus the paths you
  checked, and stop.

Fetch `https://code.claude.com/docs/en/hooks` once here and pass the relevant parts to the lenses, so
the audit tests against the current event surface. If the fetch fails, continue, and mark every
Lens 4 finding `unverified against current docs`.

## Step 2 — Mechanical checks

Three scripts ship under `${CLAUDE_PLUGIN_ROOT}/scripts/hooks/`. Run the first two before the lenses,
and hand their output to the lenses as established fact:

```bash
# Registration: event names, matcher syntax, hook type, command shape, timeouts;
# with --plugin-root, whether each registered command resolves to an existing file.
bash "${CLAUDE_PLUGIN_ROOT}/scripts/hooks/validate-hook-registration.sh" <hooks.json> --plugin-root <plugin-dir>

# Sources: fields read but never supplied, machine-local paths, eval on hook input,
# missing CLI guards, blocks with no stderr reason.
bash "${CLAUDE_PLUGIN_ROOT}/scripts/hooks/lint-hook-source.sh" --dir <hook-source-dir>
```

Both only read, and exit `0` clean (warnings allowed), `1` errors found, `2` misconfigured. Exit `2`
covers a missing `jq`. Record it as "mechanical checks unavailable" and continue with the lenses.

The third script, `run-hook-event.sh`, **executes** a hook against a synthetic payload for the named
event:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/hooks/run-hook-event.sh" --event PreToolUse --tool Bash --print-payload
bash "${CLAUDE_PLUGIN_ROOT}/scripts/hooks/run-hook-event.sh" --event PreToolUse --tool Bash -- <hook argv>
```

- `--print-payload` only prints the fixture.
- Without it, the hook runs for real and can write files or send notifications. Run it only on
  hooks whose source you have read and judged free of side effects. The call raises a permission
  prompt, because it is deliberately left out of `allowed-tools`.
- Its exit code describes the run, not the hook's verdict:
  - `0`: the hook returned a protocol-defined code (0, 1 or 2, where 2 means it blocked);
  - `1`: timeout, undefined code, or unparseable JSON;
  - `2`: bad usage.
- Quote the hook's own exit code and stderr in any finding based on a run.

## Step 3 — Four lenses

Spawn four `Agent` calls in one message, one lens each. Give every agent the Step 1 file list, the
Step 2 output, the fetched docs, and the finding schema below. If `Agent` is unavailable (the nesting
depth limit, or a surface without subagents), run the lenses inline in order.

**Lens 1: model cost inside hooks.** Grep hook sources for SDK imports or inference calls, and for
`prompt`/`agent` hook types. If none exist, check for drift: a leftover SDK dependency, docs
describing model calls that no longer happen, a stale config key. For each hook that calls a model:

- Is the model pinned?
- What bounds the prompt size?
- What gates the call (threshold, cooldown)?
- Does the matcher fire on lockfiles, generated output or docs?
- What does one invocation roughly cost?

Recommend narrowing the matcher first.

**Lens 2: process and duplicated work.** Each handler on an event is a separate process. Mark
identical entry work across handlers on the same event. Find one condition checked in two places
with different outcomes (blocks in Pre, warns in Post). Weigh consolidating into a dispatcher against
its change cost, and state which way it comes out.

**Lens 3: written rules that should be mechanical.** This lens owns the rule-to-hook question for
the whole plugin. Classify each written convention:

- **(a) enforced:** a hook or permission rule already blocks or warns;
- **(b) should be enforced:** violations are detectable from tool input;
- **(c) judgement only.**

For each (b), sketch the event, matcher, detection condition, exit behaviour and the message the
model reads.

**Lens 4: staleness and drift.** Against the fetched docs, look for:

- uncovered lifecycle events that would help;
- deprecated payload fields;
- branches unreachable under the configured matchers;
- entries pointing at a missing or always-exit-0 script;
- external CLIs invoked with no guard;
- timeouts mismatched to the workload;
- assumptions that the working directory is the repo root, which break under worktrees.

Finding schema, for every lens:

```json
{"lens": 1, "severity": "critical|warning|minor", "file": "path", "line": 0,
 "evidence": "quoted code or rule", "problem": "one sentence", "change": "concrete proposal"}
```

Severity is `critical` (blocks unrelated work, or fails open silently), `warning` (cost, duplication,
an unenforced rule that is actually violated) or `minor`.

## Step 4 — Verify

Re-open the file and line for every critical finding and confirm the quoted evidence is there. Drop
any finding whose evidence you can't reproduce.

## Report

Keep it under about 1,500 words.

```markdown
# Hook audit: <target>

Mechanical checks: registration exit <n>, source lint exit <n> (or "unavailable: <reason>")

## Findings
| # | Severity | Lens | File:line | Problem | Change |
|---|----------|------|-----------|---------|--------|

## Already correct
<up to five things done well, so they don't get "improved" later>

## Needs a decision
<up to three genuine trade-offs: the options and their costs, not decided here>

## Not checked
<unreadable paths, skipped runs, unverified lens-4 items, or "none">
```
