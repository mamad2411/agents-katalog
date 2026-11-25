---
name: implement-ai-disclosure
description: Implement EU AI Act Article 50 transparency components - AIDisclosureBanner, data-ai-generated attributes, C2PA metadata embedding for AI media, and DOMPurify sanitization. Use when deploying user-facing AI features, chatbots, generative content requiring EU AI Act compliance (effective 2 August 2026).
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Implement AI Disclosure

Implement EU AI Act Article 50 transparency components for legal compliance in EU market.

## When to Use

- deploying chatbots, virtual assistants, conversational AI
- implementing generative AI content (text, image, audio, video)
- building AI-enhanced UIs requiring transparency disclosure
- adding AI disclosure to existing features

## Core Rules

### EU AI Act Article 50 - Four Obligations (effective 2 Aug 2026)

| Obligation | Article | Description |
|------------|---------|-------------|
| AI Interaction Disclosure | 50(1) | Inform users they interact with AI (unless obvious) |
| AI Content Marking | 50(2) | Mark AI content in machine-readable format |
| Biometric Notification | 50(3) | Notify individuals of emotion/biometric systems |
| Deepfake Disclosure | 50(4) | Disclose deepfakes depicting real persons/places |

### C2PA Metadata (deadline 2 Dec 2026)

- Apply to AI-generated image, audio, video content
- Requires cryptographic metadata embedding
- Enables machine-readable AI detection

### Disclosure Components

1. **AIDisclosureBanner**: Display before first meaningful interaction, accessible (ARIA, screen reader)
2. **data-ai-generated attribute**: Apply to AI-generated content elements
3. **DOMPurify + Trusted Types**: Sanitize AI content before DOM insertion

## Implementation Patterns

```tsx
import DOMPurify from 'dompurify';

// Persistent, accessible EU AI Act Article 50 disclosure before first interaction
export function ChatInterface({ aiOutputHtml }: { aiOutputHtml: string }) {
  // Always keep an accessible AI label visible; allow collapsing details, never erasing AI identity
  const sanitized = DOMPurify.sanitize(aiOutputHtml, {
    RETURN_TRUSTED_TYPE: typeof window !== 'undefined' && 'trustedTypes' in window,
  });

  return (
    <section aria-label="AI Assistant Workspace">
      <AIDisclosureBanner
        role="status"
        message="You are interacting with an AI system. Outputs may be inaccurate."
      />
      <article
        data-ai-generated="true"
        dangerouslySetInnerHTML={{ __html: sanitized as unknown as string }}
      />
    </section>
  );
}
```

## Compliance Matrix

| Feature | 50(1) | 50(2) | 50(3) | 50(4) |
|---------|-------|-------|-------|-------|
| Chatbot | Required | - | - | - |
| AI text | - | Required | - | - |
| AI image/video | - | Required | - | If deepfake |
| Emotion recognition | - | - | Required | - |

## Suggested Process

1. **Classify AI Feature**: Identify applicable Article 50 obligations
2. **Design Components**: Create AIDisclosureBanner, content marking strategy
3. **Implement**: Add banner before interaction, apply data attributes, sanitize
4. **Test**: Verify banner appears, marks present, accessibility works
5. **Document**: Record compliance for audit

## Checklist

- [ ] Article 50 obligations identified
- [ ] AIDisclosureBanner component created
- [ ] Banner appears before first interaction
- [ ] Banner is accessible (ARIA, screen reader)
- [ ] data-ai-generated attribute applied
- [ ] DOMPurify sanitization implemented
- [ ] C2PA planned for media (Dec 2026)
- [ ] Compliance documented

## Output Contracts

- **`contracts/schemas/implementation-result.json`** — Emit implementation summary, touched files, and verification evidence when delivering Article 50 disclosure components across roles.

## Failure Modes

- Missing disclosure: Add CI/CD gate, verify before release
- XSS from AI content: Always sanitize with DOMPurify
- C2PA deadline miss: Track as separate work item

## Security Guardrails (OWASP ASI)

- ASI05: AI content is untrusted, always sanitize before DOM insertion
- ASI07: AI outputs from external services require validation

## Related Skills

- **add-ui-component**: Build accessible reusable disclosure banners and content wrappers
- **accessibility-review**: Verify ARIA live regions, focus behavior, and banner accessibility
- **frontend-testing**: Test disclosure rendering before interaction and DOMPurify sanitization
- **design-ux-flow**: Design transparent AI states and Article 50 user flows around disclosure

Last updated: 2026-11-16