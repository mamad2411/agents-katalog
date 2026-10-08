---
name: agent-control-plane-review
description: Review agent orchestration and operator control-plane repos in the lab (cooperations, recon-ops) as products — sandbox posture, capability scoping, persistence provenance, task and artifact visibility, and operator safety boundaries. Use whenever the user asks to review an agent runtime, orchestration workflow, MCP surface scope, operator UI truthfulness, or whether an automation is bounded enough to trust, even if they only name the repo.
allowed-tools: Read, Grep, Glob, Bash
---

# Agent Control Plane Review

## Overview

This skill reviews orchestration and operator-control-plane repos as products, not just codebases. Use it for `cooperations` and `recon-ops` when the question is about workflow truthfulness, safety, visibility, or operator usefulness.

The lab root is `${LAB_ROOT}/`; all `workspace/` paths in this skill and its references are relative to it.

## Review Workflow

1. Identify the execution contract first: sandbox, capabilities, approvals, persistence.
2. Check whether CLI, UI, and MCP surfaces describe one coherent runtime model.
3. Check whether task history, artifacts, and failure visibility are inspectable.
4. Check whether automation is bounded enough for a human operator to trust.
5. Distinguish product usefulness from autonomy overreach.

## What To Flag

- invisible side effects
- loose or underspecified MCP tool scope
- persistence without clear provenance
- operator UI that hides the real execution contract
- safety posture that exists only in docs, not in runtime surfaces

## References

- [control-plane-targets.md](references/control-plane-targets.md)

## Related

- Lab-local skills `mcp-stdio-schema-lint` and `mcp-tool-authority-boundary`
  (in the lab's `.claude/skills/`) go deeper on individual MCP tool schemas
  and per-tool blast radius; use them when the finding narrows to one MCP
  server or tool.
