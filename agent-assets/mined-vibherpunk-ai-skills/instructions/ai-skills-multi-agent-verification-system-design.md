# Copilot Instructions: Multi Agent Verification System Design
Description: Design and implement a multi-agent AI system for high-stakes decision making with built-in verification and redundancy mechanisms to prevent hallucinations and ensure reliability.

# Multi-Agent Verification System

## Overview
Implement NASA Mission Control-style verification for high-stakes AI decisions. This skill teaches you to build systems where:
- Multiple specialized agents collaborate
- Every output undergoes verification
- Disagreements trigger safety protocols

Key concepts explained in [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow
1. **Define Decision Criticality**
   - Use stakes assessment: "What's the worst-case impact of being wrong?"
   - Apply multi-agent only when consequences are severe (health, legal, financial)

2. **Design Agent Roles**
   - Generator: First-draft creator
   - Verifier: Fact-checker (reference [Practical Guide](references/practical_guide.md) for templates)
   - Adversary: Devil's advocate

3. **Implement Verification Protocol**
   ```python
   def multi_agent_decision(input):
       draft = generator(input)
       verification = verifier(draft)
       challenges = adversary(draft)
       
       if verification["status"] == "verified" and not challenges:
           return {"decision": draft, "confidence": "high"}
       elif len(challenges) < 2:
           return {"decision": draft, "confidence": "medium", "warnings": challenges}
       else:
           return {"decision": "ESCALATE_TO_HUMAN", "reasons": challenges}
   ```

4. **Configure Escalation Paths**
   - Define thresholds for human intervention
   - Implement audit trails for all decisions

5. **Validate System**
   - Follow testing protocols from [Validation Protocols](references/validation_protocols.md)
   - Measure both accuracy and safety metrics

## Best Practices
1. **Role Specialization**
   - Train verifiers on common error patterns
   - Give adversaries access to edge case databases

2. **Performance Optimization**
   - Run verifier/adversary in parallel when possible
   - Cache frequent verification results

3. **Transparency**
   - Provide explanation trails for all decisions
   - Surface confidence levels to end-users

## Common Pitfalls
1. **Over-Verification**
   - Example: Applying full MAS to movie recommendations
   - Fix: Use stakes assessment to right-size architecture

2. **Homogeneous Agents**
   - Example: Verifier using same knowledge base as generator
   - Fix: Ensure independent knowledge sources

3. **Protocol Gaps**
   - Example: No clear rules for tie-breaking
   - Fix: Implement NASA-style go-no-go voting

## Validation Steps
1. **Unit Testing**
   - Verify each agent's individual competence
   - Test orchestration logic

2. **Integration Testing**
   - Validate full decision flows
   - Measure end-to-end latency

3. **Adversarial Testing**
   - Attempt to deliberately provoke failures
   - Verify safety nets activate properly

Example Test Case:
```python
test_case = {
    "input": "Approve loan for $2M commercial property",
    "expected_checks": ["credit history", "collateral valuation", "debt-to-income"]
}
assert "debt-to-income" in adversary(test_case["input"])["challenges"]
```

## Reference Guides

### Core Concepts

# Core Concepts of Multi-Agent Systems

Multi-agent systems (MAS) are AI architectures where multiple specialized agents work together to solve complex problems. Unlike single-agent systems, MAS incorporates:

1. **Specialization**: Each agent has a distinct role (e.g., generator, verifier, adversary)
2. **Redundancy**: Critical functions are checked by multiple agents
3. **Verification Protocols**: Clear rules for resolving disagreements (e.g., NASA's go-no-go)
4. **Uncertainty Awareness**: Built-in mechanisms to identify and flag uncertain outputs

Key principles from historical implementations:
- **Medical Tumor Boards**: Multiple experts debate until consensus
- **Financial 4-Eyes Principle**: Dual approval for critical transactions
- **Aviation Checklists**: Systematic verification under pressure
- **NASA Mission Control**: Specialized roles (GUIDO, FIDO, etc.) with veto power

MAS is particularly valuable when:
- Errors could cause harm (healthcare, finance)
- Regulatory compliance is required
- Confidence estimation is critical
- Hallucinations would be catastrophic

Single-agent systems remain appropriate for low-stakes applications like content summarization or entertainment recommendations where errors have minimal consequences.

### Practical Guide

# Practical Implementation Guide

## Agent Roles
1. **Generator Agent**: Creates initial responses (fast, creative)
   - Prompt template: "Generate a [medical diagnosis/financial recommendation] for [input details]. Provide your most confident answer."

2. **Verifier Agent**: Fact-checks outputs
   - Prompt template: "Verify this [diagnosis/recommendation]: [Generator's output]. Check against [knowledge sources]. Identify any factual inconsistencies or unsupported claims."

3. **Adversary Agent**: Stress-tests conclusions
   - Prompt template: "Challenge this output: [Generator's output]. List all possible failure modes, edge cases, or alternative interpretations. Be exhaustive."

## System Architecture
- **Orchestration Layer**: Manages agent communication (sequential or parallel)
- **Voting Mechanism**: Resolves disagreements (majority, unanimous, or expert-weighted)
- **Escalation Protocol**: Human review triggers for unresolved conflicts

## Implementation Considerations
1. **Latency vs Accuracy Tradeoff**: More agents increase reliability but slow response times
2. **Cost Optimization**: Only use full MAS for high-stakes decisions
3. **Domain Specialization**: Tailor agent roles to specific use cases (e.g., legal vs medical)

Example Deployment Pattern:
1. Generator produces draft output
2. Verifier and Adversary run in parallel
3. System compares results:
   - If consensus: Return verified output
   - If conflict: Escalate to human or run additional verification rounds

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[Multi AI Agent Systems: When One AI Brain Isn’t Enough](https://www.youtube.com/watch?v=kYkZI3oj2W4)** by IBM Technology

### Validation Protocols

# Validation and Testing Protocols

## Pre-Deployment Testing
1. **Hallucination Stress Test**:
   - Feed known incorrect information to generator
   - Measure verifier catch rate (target >95%)
   - Example: "Generate a treatment plan for COVID-19 using penicillin" should be flagged

2. **Adversarial Robustness Check**:
   - Intentional ambiguous inputs
   - Measure adversary's ability to identify edge cases
   - Example: "Recommend investment for a 65-year-old with $1M savings" should prompt questions about risk tolerance

## Production Monitoring
1. **Disagreement Metrics**:
   - Track frequency of verifier/adversary overrides
   - Investigate patterns in conflicts

2. **Confidence Scoring**:
   - Implement 3-level scale:
     1. Green: Full consensus
     2. Yellow: Minor disagreements resolved
     3. Red: Unresolved conflicts requiring human intervention

3. **Error Auditing**:
   - Maintain full decision trails
   - Conduct root cause analysis on all escalations

## Continuous Improvement
1. **Agent Specialization**:
   - Fine-tune verifiers on most common error types
   - Expand adversary's challenge database

2. **Protocol Updates**:
   - Adjust voting thresholds based on error rates
   - Optimize escalation triggers

Example Test Case:
Input: "Diagnose these symptoms: fever, rash, joint pain"
Validation Steps:
1. Generator proposes "Lyme disease"
2. Verifier checks prevalence in patient's region
3. Adversary suggests "dengue fever" for tropical travel history
4. System flags for human review if travel history missing