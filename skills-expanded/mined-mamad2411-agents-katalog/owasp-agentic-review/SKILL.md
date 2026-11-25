---
name: owasp-agentic-review
description: "Reviews AI agent systems for OWASP Agentic Security Top 10 vulnerabilities. USE FOR: reviewing multi-agent systems, checking agent tool permissions, validating agent-to-agent communication, auditing agent autonomy controls. DO NOT USE FOR: non-agent LLM code (use llm-security-review), general API security (use api-security-review). Inspired by microsoft/hve-core owasp-agentic skill."
---

# OWASP Agentic Security Review Skill

You are an AI agent security specialist. When invoked, review AI agent system code against the **OWASP Agentic Security Top 10** vulnerability knowledge base.

## Review Checklist

### AG01: Excessive Agent Autonomy
- [ ] Agents have clearly defined scope boundaries and capability limits
- [ ] High-impact actions require explicit human approval (human-in-the-loop)
- [ ] Agent decision-making is bounded by policy constraints
- [ ] Autonomy levels are configurable and default to conservative settings
- [ ] Kill switches or circuit breakers exist for runaway agent behavior

### AG02: Unvalidated Tool/Function Calls
- [ ] All tool calls from agents are validated against an allowlist
- [ ] Tool input parameters are validated and sanitized before execution
- [ ] Tool output is treated as untrusted and validated before further use
- [ ] Dangerous tools (file system, network, shell) have additional authorization gates
- [ ] Tool call rate limits prevent resource exhaustion

### AG03: Agent Identity Spoofing
- [ ] Agents authenticate their identity when communicating with other agents
- [ ] Multi-agent systems use signed messages or mutual TLS
- [ ] Agent impersonation is detected and blocked
- [ ] Agent capabilities are tied to verified identity, not self-declared

### AG04: Missing Audit Trail
- [ ] All agent-initiated actions are logged with timestamps and context
- [ ] Audit logs include agent identity, tool calls, inputs, and outputs
- [ ] Logs are tamper-resistant and stored securely
- [ ] Audit trail supports post-incident forensic analysis
- [ ] Sensitive data is redacted from audit logs

### AG05: Privilege Escalation via Tool Chains
- [ ] Agent permissions do not escalate through chained tool calls
- [ ] Each tool call is authorized independently, not inherited from the calling agent
- [ ] Privilege boundaries are enforced at each hop in multi-agent workflows
- [ ] Tools cannot grant the calling agent additional permissions

### AG06: Insecure Agent Communication
- [ ] Agent-to-agent messages are encrypted in transit (TLS/mTLS)
- [ ] Message integrity is verified (signatures or HMACs)
- [ ] Communication channels are authenticated (not open to arbitrary senders)
- [ ] Shared context between agents is sanitized to prevent injection

### AG07: Uncontrolled Resource Consumption
- [ ] Per-agent resource quotas (tokens, API calls, compute time) are enforced
- [ ] Recursive or looping agent behavior is detected and terminated
- [ ] Concurrent agent invocations are limited
- [ ] Cost controls and budget limits are configured for agent operations

### AG08: Inadequate Error Handling in Agents
- [ ] Agent failures are handled gracefully without exposing system internals
- [ ] Failed tool calls are retried with backoff, not infinite loops
- [ ] Error states do not leave the system in an insecure configuration
- [ ] Partial failures in multi-agent workflows are handled safely

### AG09: Unsafe Output Propagation
- [ ] Output from one agent is validated before being used as input to another
- [ ] Agent outputs are not blindly executed as code or system commands
- [ ] Cross-agent prompt injection is mitigated through output sanitization
- [ ] Agent-generated content is marked as AI-generated where appropriate

### AG10: Insufficient Monitoring and Observability
- [ ] Agent behavior is monitored in real-time for anomalies
- [ ] Alerts are configured for unusual patterns (high tool call rates, unexpected targets)
- [ ] Agent performance metrics are tracked (latency, error rates, cost)
- [ ] Dashboards provide visibility into multi-agent system health

## Output

For each finding:
- **OWASP Agentic ID**: AG01–AG10
- **Severity**: Critical / High / Medium / Low
- **Location**: File, line, or architectural component
- **Issue**: Description of the vulnerability
- **Fix**: Specific code or architectural recommendation
