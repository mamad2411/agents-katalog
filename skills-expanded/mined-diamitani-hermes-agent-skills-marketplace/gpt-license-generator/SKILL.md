---
name: gpt-license-generator
description: "Use when generating tailored software licenses and terms for GPT-based solutions and AI applications."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [licensing, legal, gpt, ai-applications, terms-of-service, compliance]
---

# GPT License Generator

## Overview

Generate tailored software licenses, terms of service, and usage policies for GPT-based applications, AI agents, and machine learning tools. Produces clear, readable legal documents that address AI-specific concerns: data usage, model outputs, liability for AI-generated content, user responsibilities, and intellectual property rights. Templates adapt to different deployment models (SaaS, downloadable, API service, open source).

## When to Use

- "I need a license for my GPT app" — creating a custom license
- "Write terms of service for my AI tool" — SaaS terms generation
- "What license should I use for my open-source AI project?" — open-source licensing guidance
- "Generate a privacy policy that covers AI data usage" — privacy compliance
- "I need an API usage agreement for my AI service" — API terms

**Don't use for:** binding legal advice (always recommend attorney review), trademark registration, or patent applications.

## How It Works

**Gather Requirements → Select Template → Customize for AI → Add Platform-Specific Clauses → Format for Delivery**

## Steps

### 1. Gather Requirements
Ask the user:
- **Product type:** SaaS web app, downloadable software, API service, open-source library, custom GPT/Agent
- **AI capabilities:** text generation, image generation, code generation, data analysis, autonomous actions
- **Data handling:** Does it store user inputs? Train on user data? Share with third parties?
- **Monetization:** Free, paid, freemium, enterprise
- **Jurisdiction:** Which country/state laws apply?

### 2. License Type Selection

| Product Type | Recommended License |
|-------------|-------------------|
| Open-source AI library | MIT, Apache 2.0, or RAIL (Responsible AI License) |
| SaaS AI app | Custom Terms of Service + Privacy Policy |
| Downloadable AI tool | EULA (End User License Agreement) |
| API service | API Terms of Use + Acceptable Use Policy |
| Custom GPT / Agent | Usage Policy + Content Guidelines |

### 3. AI-Specific Clauses

Always include these sections for AI products:

**Output Disclaimer:**
> "The AI-generated content is provided 'as is' without warranty of any kind. [Product Name] does not guarantee the accuracy, completeness, or appropriateness of AI-generated outputs. Users are responsible for reviewing and validating all AI-generated content before use."

**Data Usage Policy:**
> "User inputs are [stored/not stored] and [are/are not] used to improve the AI model. [Describe retention period and data handling practices.]"

**Acceptable Use Restrictions:**
- No generation of illegal, harmful, or deceptive content
- No automated scraping or abuse of the service
- No use that violates third-party rights
- No circumvention of safety features or content filters

**Intellectual Property:**
> "Users retain ownership of their inputs. [Product Name] [does/does not] claim ownership of AI-generated outputs. [Clarify if outputs may be similar across users.]"

**Liability Limitation:**
> "To the maximum extent permitted by law, [Company] shall not be liable for any damages arising from the use of or inability to use the AI service, including damages resulting from inaccurate, inappropriate, or offensive AI-generated content."

### 4. Platform-Specific Additions

**For Custom GPTs (OpenAI GPT Store):**
- Reference OpenAI's usage policies as a baseline
- Add GPT-specific content guidelines
- Specify whether the GPT uses external APIs/actions

**For Mobile Apps:**
- Include app store compliance (Apple App Store / Google Play requirements)
- Add notification/permission language for data collection

**For Enterprise:**
- Add SLA (Service Level Agreement) terms
- Include data processing addendum (DPA) for GDPR compliance
- Specify support response times and escalation procedures

### 5. Format for Delivery
- Deliver as clean markdown or plain text, ready to copy into the platform
- Use clear section headers with anchor-style navigation
- Include placeholder markers `[COMPANY_NAME]`, `[DATE]`, `[CONTACT_EMAIL]`
- Add a prominent disclaimer: "This document is a template. Consult a qualified attorney to ensure it meets your specific legal requirements."

## Common Pitfalls

1. **Copying a generic license without AI clauses.** Standard MIT/GPL licenses don't address AI-specific issues like output ownership, training data rights, or model bias liability. Always add AI-specific terms.

2. **Over-promising on accuracy.** Never warrant that AI outputs are error-free. AI hallucination is a known limitation — your license must disclaim liability for incorrect outputs.

3. **Ignoring data privacy laws.** If your AI app processes user data and has EU users, GDPR applies. If it has California users, CCPA applies. Include relevant privacy clauses.

4. **Vague acceptable use policies.** "Don't do bad things" is unenforceable. Be specific: prohibited content categories, rate limits, and consequences for violations.

5. **Claiming ownership of AI outputs without clarity.** Copyright law for AI-generated content is unsettled. Be transparent about your position rather than making absolute claims that may not hold up.
