---
name: think
description: Brainstorm a feature or design with an automatic Codex second opinion on every clarifying question. Use when the user runs /claudex:think, or asks for Claude+Codex collaborative brainstorming. Wraps superpowers:brainstorming.
---

# claudex:think — brainstorming with a Codex second opinion

Brainstorm normally, but every clarifying question is routed through Codex for a second opinion *before* the user sees it. Enforcement is automatic — you never call Codex yourself, and you do NOT need to run any shell command to turn it on.

## How arming works (automatic)

When the user runs `/claudex:think`, a `UserPromptExpansion` hook arms the gate for this session automatically (it runs in hook context, so it isn't subject to the permission classifier). You don't touch it.

## Steps

1. **Brainstorm.** Invoke `Skill(superpowers:brainstorming)` and follow it normally. Ask clarifying questions via `AskUserQuestion` as usual — the hook intercepts each one.
2. **Handle the Codex critique.** When you try to ask a clarifying question, the hook blocks it. The (red) denial reason is kept short on purpose — it points you to a file (`~/.claude/claudex/state/<session>-critique.md`) holding your drafted question + Codex's critique, so the critique isn't shown red and then repeated. Read that file, then in ONE message:
   - Show the question you originally drafted **verbatim** under an `**Original question:**` heading (keep your recommended option), so the user can see your framing before Codex weighed in.
   - Present Codex's critique **verbatim** under a `**Codex says:**` heading.
   - Add `**My take:**` — 1-3 sentences: do you agree? Fold any fixes you accept into the question.
   - Re-issue the `AskUserQuestion` (revised if you agreed) — the revised question is the one the user actually answers. It passes through this time (one re-issue is allowed within ~2 minutes of the block).

   So each round the user sees, in order: **Original question** (with your recommendation) → **Codex says** → **My take** → the answer window — with no red duplicate of the critique. (If the file can't be written, the hook falls back to putting the critique inline in the denial reason.)
3. **Wrap up.** When you transition to `writing-plans`, the gate auto-disarms (a `PreToolUse` Skill hook handles it); it also auto-expires after the TTL.

## Design before implementation (enforced by the hook, not just by this text)

While the gate is armed you are in **design mode**. `PreToolUse` hooks block — not just discourage — these until the design is approved:

- **Editing code.** `Edit`/`Write`/`MultiEdit`/`NotebookEdit` to any non-markdown file is denied (`.mdx` counts as code). Don't fight it: it means you skipped to implementation. Go back and brainstorm.
- **Editing instruction files.** `CLAUDE.md`, `SKILL.md`, `AGENTS.md`, `GEMINI.md` are denied even though they're markdown — changing them mid-session could weaken the gate itself.
- **Implementation skills.** `test-driven-development`, `executing-plans`, `subagent-driven-development`, `frontend-design`, `mcp-builder` are denied.
- **Shell writes.** `Bash` commands that write code (`echo >`, `sed -i`, `tee`, `node -e`, `git apply/checkout`, `cp`/`mv`, …) or that touch the gate marker are denied. Read-only exploration passes. Don't try to route around the edit gate through the shell.

What you **can** do while armed: write the design/spec/plan **markdown** doc, ask `AskUserQuestion`, and (after you've brainstormed and the user approves) invoke `writing-plans` — which disarms the gate and reopens everything for implementation. So the only sanctioned path out of design mode is: brainstorm → approved design → `writing-plans`. If the user explicitly tells you to skip the design process, that's their call — point them to the kill switch below; **don't disarm the gate yourself** (the kill switch is for the user to type with a leading `!`).

> If you never see a `Codex says:` block on your questions, the gate didn't arm (e.g. the plugin wasn't reloaded after install). Tell the user to run `/reload-plugins` and re-run `/claudex:think`, rather than trying to write the marker yourself (a model Bash write to `~/.claude` is blocked in auto mode).

## Kill switch

- **Stop early (user runs this):** `! rm -f ~/.claude/claudex/armed`
- **Globally off:** set `{"enabled": false}` in `~/.claude/claudex/config.json`.
- The gate also auto-expires after `ttlHours` (default 6).

## Behavior notes

- **Implementation gate:** on by default; set `{"enforceImplementationGate": false}` in `~/.claude/claudex/config.json` to turn off the code/skill blocking described above (the Codex question gate is unaffected). It is fail-open — a hook error never blocks an edit.
- **Read-only:** Codex cannot edit files while critiquing.
- **Fail-open by default:** if Codex is unavailable or times out, the question proceeds with a note that the second opinion was skipped — mention it to the user. Set `{"failClosed": true}` in `~/.claude/claudex/config.json` to block instead.
- This plugin's hook runs on `node`. Errors like "Bun not found" come from a different plugin, not claudex.
