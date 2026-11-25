---
name: "style-guide-frameworks"
description: "Style guide foundations: a comparison of industry style guides, style guide architecture, voice vs tone, automated style checking, and reading level assessment. Use when choosing a base guide or setting up enforcement."
---

# Style Guide Frameworks

> Frameworks and reference patterns for building effective writing style guides.

## Knowledge Base

### Industry Style Guide Comparison

| Style Guide | Best For | Key Stance |
|------------|----------|------------|
| Google Developer Style Guide | Developer documentation | Present tense, active voice, second person |
| Microsoft Writing Style Guide | Product documentation | Conversational, task-oriented, accessible |
| Apple Style Guide | Consumer-facing docs | Minimal, precise, design-aware |
| Stripe Documentation Style | API documentation | Direct, example-heavy, technically precise |
| Chicago Manual of Style | Long-form content | Comprehensive grammar reference |

### Style Guide Architecture

A complete style guide covers these areas:

```
Voice & Tone
  ├── Brand voice definition
  ├── Tone variations by context
  └── Persona description

Language Rules
  ├── Grammar (tense, voice, person)
  ├── Capitalization
  ├── Punctuation
  ├── Numbers and dates
  └── Abbreviations and acronyms

Formatting
  ├── Heading hierarchy
  ├── Lists (bulleted vs numbered)
  ├── Tables
  ├── Code blocks and inline code
  ├── Images and diagrams
  └── Callouts and admonitions

Terminology
  ├── Preferred terms glossary
  ├── Terms to avoid
  ├── Product-specific vocabulary
  └── Domain-specific definitions

Accessibility & Inclusion
  ├── Plain language guidelines
  ├── Inclusive language rules
  ├── Alt text standards
  └── Reading level targets

Content Types
  ├── Per-type guidelines (tutorial, reference, etc.)
  ├── Template for each type
  └── Examples for each type
```

### Voice vs Tone

**Voice** is constant. It is who you are. Like a person's personality.
**Tone** varies by situation. Like how a person adapts to different conversations.

Example voice: "Clear, confident, helpful."

| Situation | Tone Adjustment |
|-----------|----------------|
| Error message | Empathetic, solution-oriented |
| Tutorial | Patient, encouraging |
| API reference | Precise, neutral |
| Release announcement | Enthusiastic, grateful |
| Security advisory | Urgent, serious |

### Automated Style Checking

**Vale** is the standard linter for prose. Configuration structure:

```ini
# .vale.ini
StylesPath = .vale/styles
MinAlertLevel = suggestion

[*.md]
BasedOnStyles = Vale, Google, Project
```

Custom rule types:
- **Substitution**: Replace one term with another
- **Existence**: Flag terms that should never appear
- **Occurrence**: Limit how often a term appears
- **Conditional**: If X appears, Y must also appear
- **Consistency**: If you use "color" once, do not use "colour"

### Reading Level Assessment

| Audience | Target Grade Level | Test |
|----------|--------------------|------|
| General public | Grade 6-8 | Flesch-Kincaid |
| Business users | Grade 8-10 | Flesch-Kincaid |
| Developers | Grade 10-12 | Coleman-Liau |
| Academics | Grade 12+ | Gunning Fog |

## Patterns

1. **Start with a Base**: Extend Google or Microsoft's guide rather than starting from zero. Override only what needs to differ.
2. **Examples Over Rules**: For every rule, provide a "do this / not this" example. Developers learn faster from examples.
3. **Progressive Adoption**: Start with 10-15 high-impact rules. Add more as the team builds the habit.
4. **Tooling from Day One**: If a rule cannot be checked by Vale or textlint, it will be ignored. Automate what you can.
5. **Versioned Glossary**: Treat the terminology glossary like a contract. Changes need review and communication.

## Anti-Patterns

1. **The 100-Page Guide**: No one reads it. Keep it under 10 pages. Link to the base guide for comprehensive rules.
2. **Rules Without Examples**: "Use active voice" without showing what active voice looks like in technical documentation.
3. **Unenforced Rules**: Style guides that exist in a wiki but are never checked or referenced in code review.
4. **One Voice for Everything**: Using the same chatty tone in error messages and security advisories.
5. **Prescriptive Grammar Pedantry**: Debating Oxford commas instead of addressing real consistency issues like term usage.

## References

- [Google Developer Documentation Style Guide](https://developers.google.com/style)
- [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/)
- [Stripe Documentation Style](https://docs.stripe.com/)
- [Vale - Prose Linter](https://vale.sh/)
- [Readability Formulas](https://readabilityformulas.com/)
