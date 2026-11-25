---
name: codex-setup
license: Apache-2.0
description: Check whether the local Codex CLI is ready and optionally toggle the stop-time review gate
argument-hint: '[--enable-review-gate|--disable-review-gate]'
user-invocable: true
allowed-tools: Bash(node:*), Bash(npm:*), AskUserQuestion
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

<!--
SPDX-License-Identifier: Apache-2.0
Derived from openai/codex-plugin-cc v1.0.6 (db52e28), Apache-2.0. Modified for rdl-agent-extensions.
-->

## Preflight — Node.js runtime

This plugin's runtime requires Node.js >=18.18.0. Report the Node prerequisite separately from the Codex CLI prerequisite. Before running the companion, verify Node:

```bash
node -e 'const [a,b]=process.versions.node.split(".").map(Number); process.exit(a>18||(a===18&&b>=18)?0:1)'
```

Run this preflight exactly as written, as a single `Bash` command. Read the exit status and output from the Bash tool result (empty stdout on success is expected). Do not append `echo`, `;`, `&&`, pipes, or other shell separators, wrappers, or redirects; the declared grant is `Bash(node:*)`, not a general shell grant.

If that check fails (non-zero exit or `node` not found), stop and tell the user exactly: `Codex plugin requires Node.js >=18.18.0; install or upgrade Node: https://nodejs.org/en/download`. Do not surface a raw `command not found` or version error.

## Run

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-companion.mjs" setup --json $ARGUMENTS
```

If the result says Codex is unavailable and npm is available:
- Use `AskUserQuestion` exactly once to ask whether Claude should install Codex now.
- Put the install option first and suffix it with `(Recommended)`.
- Use these two options:
  - `Install Codex (Recommended)`
  - `Skip for now`
- If the user chooses install, run:

```bash
npm install -g @openai/codex
```

- Then rerun:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-companion.mjs" setup --json $ARGUMENTS
```

If Codex is already installed or npm is unavailable:
- Do not ask about installation.

Output rules:
- Present the final setup output to the user.
- If installation was skipped, present the original setup output.
- If Codex is installed but not authenticated, preserve the guidance to run `!codex login`.

## Codex packaging

For execution in a native Codex package, use the host-specific entrypoint in
[references/codex.rst](references/codex.rst). The registry selects it during packaging;
the Claude entrypoint above remains the Claude workflow.
