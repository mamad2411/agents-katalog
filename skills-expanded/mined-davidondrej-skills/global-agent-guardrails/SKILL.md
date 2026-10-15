---
name: global-agent-guardrails
description: "Configure a shared guard against catastrophic shell commands in local AI agents. Use when changing block patterns, adding an agent or machine, or investigating why a command was or wasn't blocked."
---

# Global Agent Guardrails

Block catastrophic shell commands before execution. One patterns file can feed a shared hook script or native adapter for each agent. This guards against accidents, not malicious agents (obfuscation like `python -c "shutil.rmtree(...)"` can slip past regex).

## File map

A typical setup has a patterns file, a shared guard, a test suite, and adapters for supported agents. Use your own documented configuration locations; avoid publishing machine-specific wiring details.

## Check installation

Confirm the guard and patterns file exist, then run the project's guard test suite. Tests should report no failures.

If missing, rebuild from the wiring table or other documentation for your setup.

## Add or tune a pattern

1. Edit the patterns file. Write POSIX ERE (`grep -E`). Use `[[:space:]]`, never `\\s` — adapters may convert `[:space:]` to `\\s` for JS/Python and compile in multiline mode.
2. Add block and allow cases to the test suite, then run it; all must pass.
3. Verify the new pattern compiles in the adapter engines using the project's documented validation method.
4. Ensure any native adapters are updated to match the shared patterns.

Block only catastrophic commands (irreversible data loss, disk wipes, repo deletion). Recoverable local commands stay allowed; avoid over-blocking.

## Per-agent wiring (user-global)

Use each agent's documented hook or native blocklist mechanism. Keep shared guard behavior consistent across adapters, and merge configuration into existing settings rather than overwriting them. Use absolute paths in configs when path expansion is inconsistent across agents.

## Gotchas

- Some agent configurations require renewed trust after hook entries change. Check the agent's documentation and verify the guard is still active.
- Fail-closed behavior can block commands in environments that cannot execute hook scripts. Consider the trade-off for background or worker agents.
- Some plugin systems require explicit enablement. Verify the plugin is enabled and keep hook code simple.
- Handle adapter errors deliberately: depending on the agent, an error may block a tool or allow it to proceed.
- Distinguish confirmation behavior from hard-block behavior in native command filters.
- Make sure the guard reads the command field used by each agent's payload format.
- **Adapter regexes require multiline mode.** Keep JavaScript's `m` flag and Python's `re.M` so `^` matches each shell line like `grep`.
- **False-positive class:** a harmless command whose argument text contains a dangerous-looking string (e.g. passing a prompt mentioning `git push --force` on a CLI) gets blocked. Workaround: put the text in a file and reference it.
- Some agents or hosted/background environments may not support local command hooks. Check current agent documentation and account for any paths that bypass the local guard.

## E2E verification

Use a safe probe in a disposable, non-git directory: ask the agent to run a command that should be blocked, and confirm the guard blocks it. A repository-related error instead of a guard block means the test did not verify the guard. Follow each agent's documented procedure and avoid bypassing permission safeguards during verification.

For a direct test, send a representative dangerous-command payload to the guard and confirm it returns the documented block result.
