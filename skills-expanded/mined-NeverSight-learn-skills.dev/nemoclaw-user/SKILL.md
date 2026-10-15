---
name: nemoclaw-user
description: >
  User-facing NemoClaw guidance for installing, configuring, operating, securing,
  monitoring, and troubleshooting NemoClaw sandboxes. Use when users ask about
  NemoClaw quickstarts, OpenClaw and OpenShell relationships, local inference,
  remote GPU deployment, sandbox lifecycle, network policy, security posture,
  agent skills, command reference, or issue triage instructions.
---

# NemoClaw User

Use this skill as the top-level entrypoint for user-facing NemoClaw workflows.
The detailed workflow prompts are bundled under `references/` and indexed in
[`skills.md`](skills.md).

## Routing

Read the relevant referenced skill prompt before answering:

- Quickstart, prerequisites, Windows setup, first sandbox: `references/nemoclaw-user-get-started/SKILL.md`
- Overview, ecosystem, release notes, OpenClaw/OpenShell/NemoClaw relationship: `references/nemoclaw-user-overview/SKILL.md`
- Architecture, CLI selection, command reference, troubleshooting: `references/nemoclaw-user-reference/SKILL.md`
- Local inference, Ollama, vLLM, TensorRT-LLM, NIM, OpenAI-compatible endpoints: `references/nemoclaw-user-configure-inference/SKILL.md`
- Security posture, sandbox controls, credential storage, OpenClaw controls: `references/nemoclaw-user-configure-security/SKILL.md`
- Remote GPU or Brev deployment: `references/nemoclaw-user-deploy-remote/SKILL.md`
- Sandbox lifecycle, status, logs, rebuilds, upgrades, uninstall, messaging, persistence: `references/nemoclaw-user-manage-sandboxes/SKILL.md`
- Network policy, egress rules, endpoint access, approval workflow: `references/nemoclaw-user-manage-policy/SKILL.md`
- Monitoring, logs, health checks, debugging agent behavior: `references/nemoclaw-user-monitor-sandbox/SKILL.md`
- NemoClaw agent skills and coding assistant integration: `references/nemoclaw-user-agent-skills/SKILL.md`
- AI-assisted issue and PR triage instructions: `references/nemoclaw-user-triage-instructions/SKILL.md`

If multiple areas apply, start with the highest-level overview or reference
skill, then load more specific prompts as needed. Preserve the source skill's
commands, cautions, and prerequisites when composing the final guidance.
