---
name: sandboxed-code-execution
description: "Run generated or untrusted code safely: ephemeral sandboxes, resource and network limits, output capture and artifact handling."
type: procedural
category: execution
domain: execution
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: high
level: advanced
triggers:
  - run untrusted code safely
  - ephemeral sandbox execution
  - code interpreter limits
  - sandbox network egress
  - e2b sandbox integration
keywords:
  - sandbox
  - isolation
  - execution
  - egress
  - quotas
  - ephemeral
source: custom
enabled: true
---

# Sandboxed Code Execution

## Purpose

Run generated or untrusted code safely: ephemeral sandboxes, resource and network limits, output capture and artifact handling.

## When to Use

- An agent must execute code it generated or received.
- Analysis needs a clean environment with computed dependencies.
- Untrusted input must be evaluated without exposing the host.

## When NOT to Use

- The code is trusted, reviewed production code running in its normal pipeline.
- The task needs hardware or a network path the sandbox forbids.
- You cannot bound runtime cost; unbounded execution is not acceptable.

## Capabilities

- Provision ephemeral sandboxes with a defined expiry.
- Apply CPU, memory, disk and wall-clock limits.
- Restrict network egress to an allowlist.
- Capture stdout, stderr, exit codes and produced artifacts.

## Inputs

- The code, its language runtime and dependency manifest.
- The required network destinations and secrets, if any.
- The time and resource budget per execution.

## Workflow

1. Define the isolation boundary: filesystem, network and credentials.
2. Create the sandbox from a pinned image with only the needed runtime.
3. Stream output with a hard timeout; kill on exceed rather than truncating silently.
4. Copy out only declared artifacts by path allowlist.
5. Destroy the sandbox and record the exit code with output digests.

## Tools

- E2B or a container sandbox
- process supervision with timeouts
- artifact store

## Examples

- `allskills mcp install --harness claude --servers e2b`
- `allskills explain execution.sandboxed-code-execution --query "run generated python"`
- `allskills route "execute this code snippet safely"`

## Safety

- A sandbox with host mounts or open egress is not a sandbox.
- Never pass long-lived credentials into untrusted execution.
- Unbounded output can exhaust disk; cap and rotate.

## Source

All-Skills canonical library (`skills/execution/sandboxed-code-execution`). First-party skill, maintained in this repository.

## Notes

- Ephemeral environments make results reproducible and limits enforceable.
- Record the image digest alongside results so runs can be compared.
- Pairs with: `security/secrets-management`, `ai/tool-calling`.
