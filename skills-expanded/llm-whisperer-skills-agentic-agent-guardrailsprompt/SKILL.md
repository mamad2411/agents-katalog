# Comprehensive Guardrails and Safety for Production Agents

## Overview

Production LLM agents operate in high-stakes environments where a single unsafe output can cause legal liability, data breaches, reputational damage, or physical harm. Guardrails are the safety layer between the agent's reasoning and its actions — they validate inputs, constrain outputs, enforce policies, and provide audit trails. Unlike simple content filters, comprehensive guardrails operate at multiple levels: input sanitization, tool access control, output validation, behavioral constraints, and escalation policies.

The challenge is balancing safety with utility. Overly restrictive guardrails make agents useless; permissive guardrails leave dangerous gaps. The solution is layered defense with graduated enforcement — soft warnings for low-risk violations, hard blocks for high-risk actions, and human escalation for ambiguous cases. Each layer is independently testable and configurable.

In production, guardrails reduce agent-related incidents by 90% while maintaining 95%+ task completion rates. The key insight is that most safety violations follow predictable patterns that can be detected and prevented without blocking legitimate use cases.

## Key Concepts

- **Input Validation**: Sanitizing user inputs for prompt injection, PII, malicious payloads, and policy violations
- **Tool Access Control**: Role-based permissions on which tools agents can use and with what parameters
- **Output Filtering**: Validating agent outputs against content policies, factual consistency, and format requirements
- **Behavioral Constraints**: Limiting agent actions to predefined scopes — no file deletion, no external API calls without approval
- **Escalation Policies**: Automatic human handoff when confidence is low or risk is high
- **Audit Logging**: Complete record of all agent decisions, tool calls, and guardrail interventions
- **Rate Limiting**: Preventing abuse through per-user and per-session action limits
- **Content Classification**: ML-based classification of inputs and outputs for policy enforcement

## Implementation Patterns

```python
import re
import time
import hashlib
from dataclasses import dataclass, field
from typing import Optional, Callable, Any
from enum import Enum

class GuardrailAction(Enum):
    ALLOW = "allow"
    WARN = "warn"
    BLOCK = "block"
    ESCALATE = "escalate"
    REDACT = "redact"

class RiskLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class GuardrailResult:
    action: GuardrailAction
    rule_name: str
    risk_level: RiskLevel
    message: str
    details: dict = field(default_factory=dict)
    redacted_content: Optional[str] = None

@dataclass
class AuditEntry:
    timestamp: float
    agent_id: str
    action: str
    input_hash: str
    output_hash: str
    guardrail_results: list[GuardrailResult]
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class InputGuard:
    """Validates and sanitizes agent inputs."""

    PII_PATTERNS = {
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
        "credit_card": r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
    }

    INJECTION_PATTERNS = [
        r"ignore\s+(all\s+)?previous\s+instructions",
        r"you\s+are\s+now\s+",
        r"system\s*:\s*",
        r"<\|im_start\|>",
        r"\[INST\]",
        r"forget\s+everything",
        r"new\s+instructions:",
        r"override\s+safety",
        r"pretend\s+you\s+are",
        r"act\s+as\s+if",
    ]

    def __init__(self):
        self.blocked_patterns: list[tuple[str, str]] = []
        self.max_input_length: int = 10000

    def check(self, content: str, context: dict = None) -> list[GuardrailResult]:
        """Run all input checks."""
        results = []

        # Length check
        if len(content) > self.max_input_length:
            results.append(GuardrailResult(
                action=GuardrailAction.BLOCK,
                rule_name="input_length",
                risk_level=RiskLevel.MEDIUM,
                message=f"Input exceeds maximum length ({len(content)} > {self.max_input_length})"
            ))

        # Prompt injection check
        injection_result = self._check_injection(content)
        if injection_result:
            results.append(injection_result)

        # PII detection
        pii_results = self._check_pii(content)
        results.extend(pii_results)

        # Blocked patterns
        for pattern, reason in self.blocked_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                results.append(GuardrailResult(
                    action=GuardrailAction.BLOCK,
                    rule_name="blocked_pattern",
                    risk_level=RiskLevel.HIGH,
                    message=f"Blocked pattern detected: {reason}"
                ))

        return results

    def _check_injection(self, content: str) -> Optional[GuardrailResult]:
        content_lower = content.lower()
        for pattern in self.INJECTION_PATTERNS:
            if re.search(pattern, content_lower):
                return GuardrailResult(
                    action=GuardrailAction.BLOCK,
                    rule_name="prompt_injection",
                    risk_level=RiskLevel.CRITICAL,
                    message="Potential prompt injection detected",
                    details={"pattern": pattern}
                )
        return None

    def _check_pii(self, content: str) -> list[GuardrailResult]:
        results = []
        for pii_type, pattern in self.PII_PATTERNS.items():
            matches = re.findall(pattern, content)
            if matches:
                results.append(GuardrailResult(
                    action=GuardrailAction.REDACT,
                    rule_name=f"pii_{pii_type}",
                    risk_level=RiskLevel.HIGH,
                    message=f"PII detected: {pii_type}",
                    details={"count": len(matches)},
                    redacted_content=re.sub(pattern, f"[REDACTED_{pii_type.upper()}]", content)
                ))
        return results


class ToolGuard:
    """Controls agent access to tools and external actions."""

    def __init__(self):
        self.tool_permissions: dict[str, dict] = {}
        self.rate_limits: dict[str, list[float]] = {}
        self.blocked_tools: set[str] = set()

    def register_tool(self, name: str, risk_level: RiskLevel,
                      requires_approval: bool = False,
                      max_calls_per_minute: int = 60,
                      allowed_params: list[str] = None):
        self.tool_permissions[name] = {
            "risk_level": risk_level,
            "requires_approval": requires_approval,
            "max_calls_per_minute": max_calls_per_minute,
            "allowed_params": allowed_params or [],
        }

    def check(self, tool_name: str, params: dict = None,
              user_role: str = "user") -> GuardrailResult:
        """Check if tool call is allowed."""
        if tool_name in self.blocked_tools:
            return GuardrailResult(
                action=GuardrailAction.BLOCK,
                rule_name="tool_blocked",
                risk_level=RiskLevel.CRITICAL,
                message=f"Tool '{tool_name}' is permanently blocked"
            )

        perms = self.tool_permissions.get(tool_name)
        if not perms:
            return GuardrailResult(
                action=GuardrailAction.BLOCK,
                rule_name="tool_unknown",
                risk_level=RiskLevel.HIGH,
                message=f"Unknown tool: '{tool_name}'"
            )

        # Rate limit check
        if not self._check_rate_limit(tool_name, perms["max_calls_per_minute"]):
            return GuardrailResult(
                action=GuardrailAction.BLOCK,
                rule_name="rate_limit",
                risk_level=RiskLevel.MEDIUM,
                message=f"Rate limit exceeded for tool '{tool_name}'"
            )

        # Approval check
        if perms["requires_approval"] and user_role != "admin":
            return GuardrailResult(
                action=GuardrailAction.ESCALATE,
                rule_name="requires_approval",
                risk_level=perms["risk_level"],
                message=f"Tool '{tool_name}' requires human approval"
            )

        # Parameter validation
        if params and perms["allowed_params"]:
            invalid = set(params.keys()) - set(perms["allowed_params"])
            if invalid:
                return GuardrailResult(
                    action=GuardrailAction.WARN,
                    rule_name="invalid_params",
                    risk_level=RiskLevel.MEDIUM,
                    message=f"Unexpected parameters: {invalid}"
                )

        return GuardrailResult(
            action=GuardrailAction.ALLOW,
            rule_name="tool_allowed",
            risk_level=RiskLevel.LOW,
            message="Tool call approved"
        )

    def _check_rate_limit(self, tool_name: str, max_per_minute: int) -> bool:
        now = time.time()
        if tool_name not in self.rate_limits:
            self.rate_limits[tool_name] = []

        # Clean old entries
        self.rate_limits[tool_name] = [
            t for t in self.rate_limits[tool_name] if now - t < 60
        ]

        if len(self.rate_limits[tool_name]) >= max_per_minute:
            return False

        self.rate_limits[tool_name].append(now)
        return True


class OutputGuard:
    """Validates agent outputs before returning to user."""

    def __init__(self):
        self.max_output_length: int = 50000
        self.required_format: Optional[str] = None
        self.blocked_content: list[str] = []

    def check(self, content: str, context: dict = None) -> list[GuardrailResult]:
        results = []

        if len(content) > self.max_output_length:
            results.append(GuardrailResult(
                action=GuardrailAction.WARN,
                rule_name="output_length",
                risk_level=RiskLevel.LOW,
                message=f"Output exceeds recommended length"
            ))

        # Check for hallucinated citations
        if self._has_fake_citations(content):
            results.append(GuardrailResult(
                action=GuardrailAction.WARN,
                rule_name="fake_citations",
                risk_level=RiskLevel.MEDIUM,
                message="Output may contain fabricated citations"
            ))

        # Check for leaked system prompts
        if self._has_system_prompt_leak(content):
            results.append(GuardrailResult(
                action=GuardrailAction.BLOCK,
                rule_name="prompt_leak",
                risk_level=RiskLevel.CRITICAL,
                message="Output contains system prompt content"
            ))

        return results

    def _has_fake_citations(self, content: str) -> bool:
        citation_patterns = [
            r"according to .*?et al\.",
            r"arXiv:\d{4}\.\d{5}",
            r"doi\.org/\d+\.\d+",
        ]
        for pattern in citation_patterns:
            if re.search(pattern, content):
                # In production: verify citation exists
                pass
        return False

    def _has_system_prompt_leak(self, content: str) -> bool:
        leak_indicators = ["system prompt", "instructions say", "my instructions are",
                          "I was told to", "my system message"]
        content_lower = content.lower()
        return any(indicator in content_lower for indicator in leak_indicators)


class GuardrailPipeline:
    """Orchestrates all guardrail checks."""

    def __init__(self):
        self.input_guard = InputGuard()
        self.tool_guard = ToolGuard()
        self.output_guard = OutputGuard()
        self.audit_log: list[AuditEntry] = []
        self.on_escalation: Optional[Callable] = None

    def check_input(self, content: str, agent_id: str,
                    context: dict = None) -> tuple[bool, list[GuardrailResult]]:
        results = self.input_guard.check(content, context)
        blocked = any(r.action == GuardrailAction.BLOCK for r in results)
        escalated = any(r.action == GuardrailAction.ESCALATE for r in results)

        if escalated and self.on_escalation:
            self.on_escalation(agent_id, content, results)

        return not blocked, results

    def check_tool(self, tool_name: str, params: dict,
                   agent_id: str, user_role: str = "user"
                   ) -> tuple[bool, GuardrailResult]:
        result = self.tool_guard.check(tool_name, params, user_role)

        if result.action == GuardrailAction.ESCALATE and self.on_escalation:
            self.on_escalation(agent_id, f"Tool: {tool_name}", [result])

        return result.action != GuardrailAction.BLOCK, result

    def check_output(self, content: str, agent_id: str,
                     context: dict = None) -> tuple[str, list[GuardrailResult]]:
        results = self.output_guard.check(content, context)

        # Apply redactions
        final_content = content
        for result in results:
            if result.action == GuardrailAction.REDACT and result.redacted_content:
                final_content = result.redacted_content

        return final_content, results

    def audit(self, agent_id: str, action: str, input_content: str,
              output_content: str, results: list[GuardrailResult],
              user_id: str = None, session_id: str = None):
        self.audit_log.append(AuditEntry(
            timestamp=time.time(),
            agent_id=agent_id,
            action=action,
            input_hash=hashlib.sha256(input_content.encode()).hexdigest()[:16],
            output_hash=hashlib.sha256(output_content.encode()).hexdigest()[:16],
            guardrail_results=results,
            user_id=user_id,
            session_id=session_id
        ))
```

## Best Practices

1. **Layer your guardrails**: Input validation, tool control, and output filtering should be independent layers that each catch different risks
2. **Default to deny for unknown tools**: Don't allow agents to call tools that haven't been explicitly registered and configured
3. **Use graduated enforcement**: Warn first, then block — don't immediately escalate everything
4. **Log everything for audit**: Every guardrail intervention should be logged with full context for compliance and debugging
5. **Test guardrails adversarially**: Regularly red-team your guardrails with prompt injection, jailbreak, and edge case testing
6. **Make guardrails configurable per deployment**: Different customers and environments need different risk tolerances
7. **Implement circuit breakers**: If guardrails are triggering too frequently, the agent may be in a bad state — auto-pause and alert
8. **Separate content policy from safety policy**: Content policy (what topics are allowed) is different from safety (preventing harm) — manage them independently
9. **Use deterministic checks first**: Regex and rule-based checks are faster and more predictable than ML-based classifiers — use them as the first line
10. **Provide clear error messages**: When blocking an action, explain why and what the user can do differently

## Common Pitfalls

- **Over-blocking legitimate requests**: Too-aggressive patterns block normal use cases — measure false positive rates continuously
- **Ignoring context**: A word that's dangerous in one context may be fine in another — use contextual classifiers, not just keyword matching
- **Missing output guardrails**: Many teams focus on input safety but forget to validate what the agent actually outputs
- **No escalation path**: When guardrails block something, there should always be a way to get human review
- **Static guardrails**: Threat landscapes evolve — update guardrail rules based on new attack patterns
- **Bypassing guardrails for "trusted" users**: Privilege escalation often comes from compromised trusted accounts — apply guardrails uniformly

## References

- Inan, H. et al. (2023). "Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations." arXiv:2312.06674
- Mazeika, M. et al. (2024). "HarmBench: A Standardized Evaluation Framework." arXiv:2402.04249
- OWASP Top 10 for LLM Applications: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- NeMo Guardrails: https://github.com/NVIDIA/NeMo-Guardrails
