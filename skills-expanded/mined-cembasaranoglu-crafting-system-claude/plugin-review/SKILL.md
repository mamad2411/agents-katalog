---
name: plugin-review
description: Reviews Claude Code plugins for manifest structure, skill design, agents, hooks, MCP, LSP, monitors, permissions, security, documentation, and packaging readiness. Use when reviewing a plugin or plugin plan.
---
# Plugin Review

Review this Claude Code plugin or plugin plan: `$ARGUMENTS`

## Instructions

Check:

1. `.claude-plugin/plugin.json` identity and versioning.
2. Directory layout: only `plugin.json` under `.claude-plugin/`; other component directories at plugin root.
3. Skill boundaries and descriptions.
4. Manual-only vs model-invoked settings.
5. `allowed-tools` least privilege.
6. Dynamic shell injection risk.
7. Subagent boundaries.
8. Hooks safety.
9. MCP trust and prompt-injection risk.
10. LSP and monitor requirements.
11. README, install, usage, limitations, and security notes.
12. Local test plan.

## Output

```yaml
plugin_review:
 status: "pass | pass_with_notes | needs_changes | unsafe | blocked"
 findings:
 - severity: "critical | high | medium | low | info"
 area: "manifest | skills | agents | hooks | mcp | lsp | monitors | docs | security | packaging"
 evidence: ""
 impact: ""
 recommendation: ""
 release_blockers: []
 safe_next_steps: []
```
