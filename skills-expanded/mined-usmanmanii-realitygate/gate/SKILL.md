---
name: gate
description: Set up and run the RealityGate quality gate so fake code can never be merged — runs the Reality Gate check, proves every check can fail with planted canaries (selftest), installs guardrail hooks, and adds the gate to CI. Use when the user wants to stop AI-generated stubs, placeholders, hallucinated packages or leaked secrets from reaching main, asks for a pre-commit or CI quality gate, or asks to protect .env files or block force-push.
---

# RealityGate gate

Make "done" mean something, and prove the gate itself works.

## Run the gate

```bash
node "${CLAUDE_PLUGIN_ROOT}/bin/realitygate.mjs" check
node "${CLAUDE_PLUGIN_ROOT}/bin/realitygate.mjs" selftest
```

(Outside the plugin: `npx --yes realitygate check` / `npx --yes realitygate selftest`.)

- `check` exits 1 on any violation **or** when an include target scanned zero files.
- `selftest` exits 1 if any rule stays silent on its planted violation.
- To prove the project's real gate command catches fake code:
  `realitygate selftest --gate "<the project's gate command>"`. It plants a canary, runs the
  command, requires it to fail, and removes the canary.

## Set it up in a project (ask the user first)

1. Create `realitygate.config.json` if missing:
   `node "${CLAUDE_PLUGIN_ROOT}/bin/realitygate.mjs" init`. That writes the config plus the
   Build OS docs and subagents (`.claude/agents/`) and never overwrites existing files. Set `include` to the app-source globs.
2. Turn each of the project's "never break" rules into a custom rule with a `canary`
   (see the README's configuration reference). Run `selftest` to prove each one fires.
3. Guardrails:
   - A git pre-commit gate that works with every agent and every human:
     `node "${CLAUDE_PLUGIN_ROOT}/bin/realitygate.mjs" hooks install --git`.
   - Claude Code hooks (block `.env` access, destructive git, out-of-scope edits). The
     RealityGate Claude Code plugin already includes them; otherwise run
     `node "${CLAUDE_PLUGIN_ROOT}/bin/realitygate.mjs" hooks install`.
4. CI: add a workflow step using the RealityGate GitHub Action:

   ```yaml
   - uses: usmanmanii/realitygate@v0.3.0
     with:
       min-score: 80
   ```

Rules:
- Fix violations for real. A `justified: <reason>` comment is allowed only for R-006/R-007/R-008
  and only with a true reason.
- Never add `exclude` or `disable` entries just to make the gate pass. If one is truly needed,
  tell the user exactly what is being excluded and why, and get their agreement.
