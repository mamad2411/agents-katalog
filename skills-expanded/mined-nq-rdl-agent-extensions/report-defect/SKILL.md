---
license: Apache-2.0
description: Review a recorded Codex plugin defect marker and decide whether to file it against nq-rdl/agent-extensions
argument-hint: '[defect-id]'
user-invocable: true
disable-model-invocation: true
allowed-tools: Bash(node:*), Bash(gh:*), AskUserQuestion
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

<!--
SPDX-License-Identifier: Apache-2.0
SPDX-FileCopyrightText: 2026 nq-rdl
-->

## Preflight — Node.js runtime

Before running the defect CLI, verify Node >=18.18.0:

```bash
node -e 'const [a,b]=process.versions.node.split(".").map(Number); process.exit(a>18||(a===18&&b>=18)?0:1)'
```

Run this preflight exactly as written, as a single `Bash` command. Read the exit status and output from the Bash tool result (empty stdout on success is expected). Do not append `echo`, `;`, `&&`, pipes, or other shell separators, wrappers, or redirects; the declared grant is `Bash(node:*)`, not a general shell grant.

If that check fails (non-zero exit or `node` not found), stop and tell the user exactly: `Codex plugin requires Node.js >=18.18.0; install or upgrade Node: https://nodejs.org/en/download`. Do not surface a raw `command not found` or version error.

## Reporting procedure

Set `PLUGIN_ROOT` to the installed `${CLAUDE_PLUGIN_ROOT}` directory for the
commands in [references/reporting.rst](references/reporting.rst). Read and follow
that shared procedure before inspecting, drafting, filing, or marking a defect.
Pass the user-supplied defect ID literally; use the latest marker only when no ID
was supplied. The procedure owns verdict, privacy, draft-approval, and outcome gates.

## Codex packaging

For execution in a native Codex package, use the host-specific entrypoint in
[references/codex.rst](references/codex.rst). The registry selects it during packaging;
the Claude entrypoint above remains the Claude workflow.
