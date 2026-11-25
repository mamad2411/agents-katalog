---
name: agent-resilience-testing
description: Orchestrates end-to-end resilience testing for LLM agents with AgentBreak, including LLM infrastructure failures, prompt injection, agent skill supply-chain risk, guardrail verification, and MCP server/tool failures. Use when the user asks to "test my agent for resilience", "chaos test this agent", "find failure modes in my LLM app", "red-team my MCP tools", or assess agent reliability, fault tolerance, safety, or recovery behavior.
metadata:
  short-description: Test agents for resilience with AgentBreak
---

# Agent Resilience Testing

This skill is the orchestrator. AgentBreak is the deterministic engine for live fault injection; static checks and guardrail probes fill the gaps that a proxy cannot observe directly.

## Core Rules

- Run the real `agentbreak` CLI for initialization, validation, inspection, proxying, scorecards, and history.
- Cover all four lanes: LLM failure modes, agent skill supply chain, guardrails, and MCP server/tool behavior.
- Treat mock-mode direct requests as endpoint smoke tests, not full agent resilience evidence.
- Treat proxy-mode traffic through the user's actual agent as the primary resilience signal.
- If MCP is enabled, run `agentbreak inspect` before testing. If inspect fails, stop and ask whether to fix MCP config or disable MCP testing.
- If proxy auth or connection validation fails, stop and fix that first. Do not run chaos tests against broken upstream auth.
- Always clean up local processes and restore temporary `.env` changes after a run.
- Ask before changing project config files unless the user has already explicitly asked you to perform setup.

## Orchestrator Workflow

1. **Check AgentBreak**
   - Run `agentbreak --help`.
   - If missing, detect `uv` or an active virtualenv and install with the least invasive command.

2. **Map The System**
   - Inspect the repo for provider, framework, MCP usage, agent skills/capabilities, guardrails, tool calls, base URLs, retry logic, timeout handling, and error paths.
   - Read `references/detection.md` for scan patterns and what to report.
   - Present concise findings and choose mock or proxy mode.

3. **Build The Four-Lane Test Plan**
   - Read `references/coverage.md`.
   - Lane 1: LLM failures: outages, brownouts, rate limits, context/token failures, malformed outputs, prompt injection, and streaming failures.
   - Lane 2: Agent skills: scan installed/local skills for unsafe instructions, secret access, network exfiltration, downloads, dangerous commands, and hidden prompt injection.
   - Lane 3: Guardrails: verify input, output, tool-argument, tool-result, PII/secrets, policy, and human-approval checks.
   - Lane 4: MCP: test server failures, tool failures, bad schemas, bad results, registry drift, rug pulls, poisoning, and cross-tool attacks.

4. **Configure AgentBreak**
   - If `.agentbreak/application.yaml` or `.agentbreak/scenarios.yaml` is missing, run `agentbreak init`.
   - Choose one LLM provider unless the user explicitly wants multiple separate runs.
   - Use port `5005` by default.
   - Use mock mode for demos, CI, and low-risk setup. Use proxy mode when the goal is real agent resilience.
   - Validate with `agentbreak validate`; use `agentbreak validate --test-connection` in proxy mode.

5. **Create Scenarios And Probes**
   - Keep existing presets and append project-specific scenarios below them.
   - Read `references/scenarios.md` before writing scenario YAML.
   - Read `references/skill-supply-chain.md` before auditing agent skills.
   - Read `references/guardrails.md` before guardrail probes.
   - Generate `.agentbreak/queries.yaml` when useful so tests exercise realistic prompts and tool calls for this specific agent.
   - Re-run `agentbreak validate` after every scenario edit.

6. **Run Tests**
   - Start `agentbreak serve -v` and wait for `/healthz`.
   - In mock mode, send contextual requests directly to AgentBreak and label the result as a smoke test.
   - In proxy mode, route the actual agent's LLM and MCP traffic through AgentBreak, run realistic tasks, then read `/_agentbreak/scorecard`.
   - Run static skill checks and guardrail probes even when proxy traffic is unavailable.
   - If history is enabled, compare against prior runs.

7. **Report Results**
   - Use `references/report.md` for the output structure.
   - Report each lane as `tested`, `partial`, `not present`, or `blocked`.
   - Include traffic summary, static scan results, guardrail results, scenario coverage, score/outcome, observed failures, evidence, likely code fixes, and caveats.
   - For mock smoke tests, explicitly say that SDK retry logic and agent behavior were not exercised.

## User-Facing Flow

The user should only need to ask:

```text
Test my agent for resilience.
```

Keep the interaction simple. Explain what you found, ask only when a safety or validity choice is required, run the AgentBreak CLI for durable checks, and return one clear report.
