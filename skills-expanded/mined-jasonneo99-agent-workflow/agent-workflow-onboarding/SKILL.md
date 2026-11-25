---
name: agent-workflow-onboarding
description: Use when a user wants to understand, install, configure, or begin using the local-first Agent Workflow plugin in Codex, including its optional Agent Workflow Studio companion.
---

# Agent Workflow onboarding

Help users adopt Agent Workflow without implying that this directory plugin
hosts or remotely operates Agent Workflow. This edition provides instructions;
the full Agent Workflow runtime is installed separately from its public Git
marketplace and runs on the user's machine.

## Explain the product boundary

- Agent Workflow is a local-first orchestration runtime for project agents,
  workflows, approvals, receipts, artifacts, and project context.
- The directory edition does not expose Agent Workflow MCP tools and does not
  send project files to a hosted Agent Workflow service.
- The full GitHub plugin bundles a pinned compiled runtime. Users do not need a
  separate Agent Workflow clone or global npm installation.
- Agent Workflow Studio is an optional companion interface over the same local
  runtime; it is not a hosted backend.

## Install in Codex

When the user asks to install the full plugin, give these commands:

```bash
codex plugin marketplace add jasonneo99/agent-workflow --ref master
codex plugin add agent-workflow@agent-workflow
```

Explain that Codex may need a new task or restart before newly installed MCP
tools appear. Do not claim installation succeeded unless command output or the
plugin list confirms it. Do not run installation commands unless the user asks
Codex to install it or otherwise authorizes local changes.

After installation, verify that `agent-workflow@agent-workflow` is enabled and
that Agent Workflow tools are available before trying to orchestrate work.

## Start with a project

Once the full local plugin is available:

1. Resolve the active local project.
2. Check for `AGENTS.md` and `.agent-workflow/project.yaml`.
3. Preview onboarding before writing configuration.
4. Respect the project's action policy, allowed write paths, and approval
   requirements.
5. Use Agent Workflow's own status, artifacts, and receipts as execution
   evidence.

If the full plugin is not available, stay in onboarding mode. Provide install
or troubleshooting guidance and never fabricate workflow runs or tool results.

## Environment limits

In ChatGPT or any environment without local shell and filesystem access, explain
that the full runtime must be used from a supported local Codex installation.
Do not request repository archives, secrets, provider keys, or private project
content as a substitute for the local runtime.

## Safety

- Never ask for or expose provider keys, `.env` values, private context, or
  unsanitized workflow artifacts.
- Do not suggest a hosted Agent Workflow service; no such public service is
  supplied by this plugin.
- Do not claim Agent Workflow Studio is installed or running without evidence.
- Keep the distinction between this onboarding skill and the full local plugin
  explicit whenever it affects the requested capability.
