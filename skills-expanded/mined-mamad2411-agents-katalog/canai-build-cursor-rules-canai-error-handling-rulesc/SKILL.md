---
description:
globs: backend/middleware/{error,retry}.js, backend/routes/*.js, frontend/src/components/*/ErrorBoundary.tsx
alwaysApply: false
---
---
description: Guides robust error handling practices
globs: backend/middleware/{error,retry}.js, backend/routes/*.js, frontend/src/components/*/ErrorBoundary.tsx
alwaysApply: false
---

# CanAI Error Handling Guidelines

## Purpose
Enable empathetic, user-focused error handling across the 9-stage user journey (F1-F9) of the CanAI Emotional Sovereignty Platform, aligning with PRD Sections 7, 9, and 12 to maintain trust, ensure responsiveness, and support platform availability.

## Scope
Provide flexible, high-level guidance for error handling across frontend, backend, APIs, databases, webhooks, and AI integrations, prioritizing PRD alignment, user experience, and adaptability.

## Guiding Principles

### Empathy
- Deliver clear, supportive error messages that guide users to resolution.
- Maintain a positive tone to preserve trust and emotional engagement.

### Responsiveness
- Detect and display errors quickly to minimize user disruption.
- Provide fallback options or retries for seamless recovery.

### Accessibility
- Ensure error messages meet WCAG 2.2 AA standards (e.g., ARIA labels, contrast).
- Make feedback inclusive for all users.

### Reliability
- Log errors securely for debugging and analytics.
- Implement robust recovery mechanisms for transient issues.

## Error Handling Approach

### Error Types
Address common issues, adapting as needed per PRD:
- API timeouts, validation failures, payment errors, low AI confidence, input conflicts, inappropriate content, rate limits, network issues, authentication failures, AI output errors, service quotas, webhook failures.

### User-Facing Responses
- Use concise, empathetic messages tailored to the context.
- Display errors rapidly, leveraging cached responses where possible.
- Provide actionable next steps (e.g., retry, clarify input).

### Logging
- Capture errors with relevant details (e.g., type, user ID, timestamp, correlation ID).
- Store logs securely with access controls, adhering to PRD retention policies.

## Stage-Specific Guidance
Apply error handling thoughtfully across the 9-stage journey, guided by PRD:

- **F1: Discovery Hook**: Use cached content for loading failures; show fallback pricing or samples.
- **F2: Discovery Funnel**: Offer tooltips for validation errors; save progress locally if autosave fails.
- **F3: Spark Layer**: Display cached outputs for generation issues; prompt upgrades for rate limits.
- **F4: Purchase Flow**: Retry payments with backoff; suggest alternative methods for failures.
- **F5: Input Collection**: Persist inputs locally for save errors; highlight invalid fields clearly.
- **F6: Intent Mirror**: Provide basic summaries for low-confidence outputs; request clarifications.
- **F7: Deliverable**: Return partial outputs for timeouts with resume options; offer text fallbacks for PDFs.
- **F8: SparkSplit**: Show single outputs for comparison failures; use backup analysis for scoring issues.
- **F9: Feedback**: Queue feedback locally for submission errors; retry email sends as needed.

## Implementation Guidance

### Frontend
- Use error boundaries and fallbacks to maintain UI stability.
- Provide accessible, real-time notifications for errors.
- Cache fallback content for offline or timeout scenarios.

### Backend
- Implement middleware for consistent error detection and response formatting.
- Standardize API error responses with user-friendly messages and metadata.
- Retry transient errors with configurable backoff strategies.

### AI Integrations
- Offer fallbacks for AI timeouts or quotas (e.g., simplified prompts, alternative models).
- Log AI errors for monitoring and refinement.
- Apply trust penalties for fallback outputs per PRD.

### Webhooks
- Queue failed webhooks for retries with exponential backoff.
- Escalate persistent failures to support for review.

### Database & Logging
- Store error logs in a secure, queryable database with fields for type, action, and metadata.
- Apply retention policies and access controls per PRD.

### Monitoring
- Integrate tools (e.g., Sentry) for real-time error tracking.
- Analyze error patterns to improve handling and prevent recurrence.
- Track retries and recovery success for performance insights.

## Validation & Testing
- Test error detection, logging, and recovery in CI/CD pipelines.
- Verify alignment with PRD requirements and accessibility standards.
- Review error handling periodically to adapt to user feedback.

## Documentation
- Document common errors, their causes, and recovery steps.
- Maintain a log of error trends and resolutions.
- Update error messages based on user experience insights.

## Success Metrics
- **User Trust**: Positive feedback on error handling clarity and empathy.
- **Recovery**: High success rate for retries and fallbacks.
- **Performance**: Fast error detection and response times.
- **Compliance**: Secure logging with no privacy violations.

## Ownership
- **Frontend Team**: Manages UI error handling and accessibility.
- **Backend Team**: Implements API and webhook error logic.
- **QA Team**: Validates error flows and compliance.
- **DevOps Team**: Monitors errors and performance.

## References
- **PRD Sections**: 7 (Non-Functional Requirements), 9 (Error Handling), 12 (Metrics).
- **Standards**: Emphasize PRD precedence, accessibility, and user trust.

---

**Created**: June 19, 2025
**Version**: 1.0.0
**Alignment**: PRD Sections 7, 9, 12
