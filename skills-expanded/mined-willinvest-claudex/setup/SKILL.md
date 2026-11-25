---
name: setup
description: Use when the user runs /claudex:setup or asks to install/bootstrap claudex's dependencies (the Codex plugin and superpowers). Installs both plugins, then verifies the Codex CLI via codex:setup.
---

# claudex:setup — bootstrap claudex's dependencies

claudex's `/claudex:think` needs two other plugins: the **Codex** plugin
([openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc), for the Codex
runtime) and **superpowers** ([anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official),
for the brainstorming flow). This skill installs both, then runs the Codex CLI check.

This skill depends only on the `claude` CLI and Bash, so it works even before either
dependency exists. Every step is **idempotent** — re-running `/claudex:setup` is safe
and resumes cleanly.

## Order (important)

Install **both** plugins first, so the user reloads **once** — only then is
`codex:setup` invokable, and you run it last.

```
1. install codex plugin   (CLI, no reload needed yet)
2. install superpowers     (CLI, no reload needed yet)
3. ONE reload gate         (user runs /reload-plugins → both go live)
4. invoke codex:setup      (now available; verifies the Codex CLI)
```

## Steps

### 1. Install the Codex plugin

Check first, then add the marketplace and install only if missing:

```bash
claude plugin marketplace list 2>/dev/null | grep -q openai-codex \
  || claude plugin marketplace add openai/codex-plugin-cc
claude plugin list 2>/dev/null | grep -q 'codex@' \
  || claude plugin install codex@openai-codex
```

### 2. Install superpowers

```bash
claude plugin marketplace list 2>/dev/null | grep -q claude-plugins-official \
  || claude plugin marketplace add anthropics/claude-plugins-official
claude plugin list 2>/dev/null | grep -q 'superpowers@' \
  || claude plugin install superpowers@claude-plugins-official
```

If a `marketplace add` fails (e.g. no network), report it and stop — the install
in that step can't succeed. The two plugins are independent, so a failure on one
doesn't invalidate the other.

### 3. Reload gate (one time)

Plugins installed via the CLI are **not live in the running session** — their skills
(like `codex:setup`) aren't invokable until a reload. Check whether `codex:setup` is
available to you now:

- **Not available** → tell the user: *"Codex and superpowers are installed. Run
  `/reload-plugins` (or restart Claude Code) once, then re-run `/claudex:setup` to
  finish — it'll skip the already-installed plugins and run the Codex CLI check."*
  Then stop. The idempotent checks in steps 1–2 make the re-run cheap.
- **Available** → continue to step 4.

### 4. Verify the Codex CLI

Invoke `codex:setup` (via the Skill tool). It checks the local Codex CLI, offers to
`npm install -g @openai/codex` if missing, and prints `!codex login` guidance if the
CLI is installed but not authenticated. Present its output to the user.

### 5. Confirm

Run `claude plugin list` and confirm `claudex`, `codex`, and `superpowers` are all
enabled. Report the final state. `/claudex:think` is now ready to use.

## Notes

- **Scope:** installs default to `user` scope. Pass `--scope project` to the
  `install` commands if the user wants the deps tied to this project instead.
- **Already set up:** if all three plugins are enabled on the first run, skip straight
  to step 4 (the Codex CLI check) and report that nothing needed installing.
- **Don't write to `~/.claude` directly** to fake plugin state — let the CLI manage it.
