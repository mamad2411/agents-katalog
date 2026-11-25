---
license: Apache-2.0
description: Cancel an active background Codex job in this repository
argument-hint: '[job-id]'
user-invocable: true
disable-model-invocation: true
allowed-tools: Bash(node:*)
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

<!--
SPDX-License-Identifier: Apache-2.0
Derived from openai/codex-plugin-cc v1.0.6 (db52e28), Apache-2.0. Modified for rdl-agent-extensions.
-->

## Preflight — Node.js runtime

Before running the companion, verify Node >=18.18.0:

```bash
node -e 'const [a,b]=process.versions.node.split(".").map(Number); process.exit(a>18||(a===18&&b>=18)?0:1)'
```

Run this preflight exactly as written, as a single `Bash` command. Read the exit status and output from the Bash tool result (empty stdout on success is expected). Do not append `echo`, `;`, `&&`, pipes, or other shell separators, wrappers, or redirects; the declared grant is `Bash(node:*)`, not a general shell grant.

If that check fails (non-zero exit or `node` not found), stop and tell the user exactly: `Codex plugin requires Node.js >=18.18.0; install or upgrade Node: https://nodejs.org/en/download`. Do not surface a raw `command not found` or version error.

## Run

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-companion.mjs" cancel "$ARGUMENTS"
```

Present the command output to the user exactly as returned, including the cancelled job ID and status.

## Codex packaging

For execution in a native Codex package, use the host-specific entrypoint in
[references/codex.rst](references/codex.rst). The registry selects it during packaging;
the Claude entrypoint above remains the Claude workflow.
