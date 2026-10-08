---
description:
globs:
alwaysApply: true
---
---
description: Guides GPT-4o and Hume AI integration
globs: backend/services/{gpt4o,hume}.js, backend/prompts/*.js
alwaysApply: false
---

# CanAI LLM Guidelines

## Purpose
Guide the deployment of Large Language Models (LLMs) to deliver safe, efficient, and emotionally resonant outputs across the 9-stage user journey (F1-F9), aligning with PRD Sections 6, 8.4, 12, and 17 to support user trust and platform reliability.

## Scope
Provide flexible, high-level guidance for deploying LLMs, ensuring PRD alignment, emotional resonance, and adaptability to project needs while prioritizing safety and performance.

## Guiding Principles

### Safety
- Protect users from harmful or biased outputs through robust filtering and validation.
- Secure data handling to comply with privacy standards.

### Emotional Resonance
- Deliver outputs that align with user emotional drivers and PRD-defined metrics.
- Validate resonance to enhance user engagement and trust.

### Efficiency
- Optimize resource usage for performance and cost-effectiveness.
- Implement fallbacks to maintain functionality under constraints.

### PRD Alignment
- Ensure LLM deployments support PRD objectives for each journey stage.
- Adapt to evolving PRD requirements and user feedback.

## LLM Deployment Approach

### Input Handling
- Validate inputs for completeness and appropriateness before processing.
- Optimize token usage, prioritizing essential user data within model limits.
- Filter inappropriate content and prevent prompt injection attacks.

### Privacy & Security
- Redact sensitive information and enforce strict access controls.
- Define retention periods for LLM interactions per PRD.
- Log access attempts securely for compliance.

### Cost & Rate Limits
- Monitor API usage to stay within rate limits and budgets.
- Set alerts for cost thresholds and implement circuit breakers for external services.
- Use cost-efficient models or fallbacks when appropriate.

### Configuration
- Use balanced model settings (e.g., moderate temperature) for consistency, adjusting for creative tasks.
- Set timeouts with retries to ensure reliability.
- Support fallback models to maintain quality during failures.

### Safety & Bias
- Validate outputs for harmful or biased content using detection tools.
- Mitigate bias through flagging and correction, logging incidents for review.
- Ensure compliance with PRD safety standards before delivery.

### Emotional Resonance
- Confirm outputs meet resonance goals using validation tools (e.g., Hume AI).
- Target high trust and confidence scores per PRD metrics.
- Trigger human review for low-confidence outputs in critical stages.

### Fallback & Recovery
- Provide partial outputs or cached responses during failures.
- Communicate errors empathetically with clear retry options.
- Use alternative models or data to maintain functionality.

### Output Standards
- Ensure outputs match PRD-specified formats, lengths, and tones.
- Validate structure and consistency before delivery.
- Support dynamic user preferences (e.g., tone, style).

## Stage-Specific Guidance
Apply LLM deployments thoughtfully across the 9-stage journey, guided by PRD:
- **F1: Discovery Hook**: Generate trust-building content with high resonance.
- **F2: Discovery Funnel**: Validate inputs with emotionally supportive feedback.
- **F3: Spark Layer**: Create engaging spark concepts tailored to user inputs.
- **F4: Purchase Flow**: Provide clear, reassuring payment guidance.
- **F5: Input Collection**: Offer context-aware input assistance.
- **F6: Intent Mirror**: Summarize inputs with high confidence and empathy.
- **F7: Deliverable**: Generate high-quality, resonant outputs.
- **F8: SparkSplit**: Produce comparable outputs for trust evaluation.
- **F9: Feedback**: Analyze feedback for sentiment and actionable insights.

## Implementation Guidance

### Integration
- Ensure compatibility with project services (e.g., Supabase, Make.com).
- Track LLM interactions via analytics for performance insights.

### Code Generation
- Include clear comments and documentation for generated code.
- Adhere to project coding standards (e.g., TypeScript, React).
- Validate functionality and integration before deployment.

### Performance
- Optimize for fast response times per PRD targets.
- Cache frequent responses to reduce latency.
- Support streaming for long-running tasks to improve user experience.

### Monitoring & Logging
- Log interactions, including tokens, costs, and errors.
- Track metrics like success rates, fallbacks, and resonance scores.
- Use tools (e.g., Sentry) for real-time error detection.

### Testing
- Achieve high test coverage for LLM-related code.
- Validate fallback scenarios and safety checks.
- Test output quality and resonance alignment.

### CI/CD
- Automate input validation, safety, and performance tests in pipelines.
- Validate schema compliance and resource usage.
- Monitor deployment health and rollback readiness.

## Documentation
- Document LLM configurations, safety measures, and fallback strategies.
- Maintain a log of prompt changes and performance metrics.
- Update documentation with PRD or project evolution.

## Ownership
- **AI Team**: Configures and maintains LLM deployments.
- **Product Team**: Defines output goals and metrics.
- **QA Team**: Validates safety, quality, and resonance.
- **DevOps Team**: Monitors performance and cost.

## References
- **PRD Sections**: 6 (Requirements), 8.4 (AI Integration), 12 (Metrics), 17 (Enhancements).
- **Standards**: Prioritize safety, resonance, and PRD alignment.

---

**Created**: June 19, 2025
**Version**: 1.0.0
