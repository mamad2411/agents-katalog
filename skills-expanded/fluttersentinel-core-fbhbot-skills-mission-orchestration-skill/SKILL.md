# Skill: Mission Orchestration & Strategic Planning

This skill guides the agent in managing complex, long-term penetration testing campaigns.

## 1. Multi-Stage Planning
A full pentest is not a single tool call. It is a sequence of dependent operations:
- **Stage 1: Recon**: Broad discovery of assets (Shodan, CT Logs, Google).
- **Stage 2: Scan**: Deep analysis of identified assets (FBH, MobSF).
- **Stage 3: Research**: Intelligent mapping of findings to 0-day disclosures.
- **Stage 4: Exploit**: Generation and execution of Proof of Concepts.
- **Stage 5: Verify**: Confirmation of impact via autonomous verification.
- **Stage 6: Report**: Synthesis of the entire campaign into a bounty-ready report.

## 2. Global State Awareness
- **Context Preservation**: Use the Global Brain (\`memory_search\`) to recall what has been tried in previous stages.
- **Adaptive Execution**: If a scan fails, the agent should transition to a "Research" mission to find alternative entry points.
- **Success Chaining**: A successful exploit in Stage 4 should lead to a deeper "Post-Exploitation Recon" to find lateral movement opportunities.

## 3. Mission Status Reporting
- Keep the operator informed about the progress of each stage.
- Flag "Critical Blockers" (e.g., "Full WAF protection detected, research required").
- Provide a clear "End-of-Mission" summary with verified impacts.
