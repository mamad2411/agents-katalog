---
name: hosted-onboarding-api
description: "Hosted onboarding API skill. Use when working with Hosted onboarding for getOnboardingUrl, getPciQuestionnaireUrl. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# Hosted onboarding API
API version: 6

## Auth
ApiKey X-API-Key in header | Bearer basic

## Base URL
https://cal-test.adyen.com/cal/services/Hop/v6

## Setup
1. Set Authorization header with your Bearer token
3. POST /getOnboardingUrl -- create first getOnboardingUrl

## Endpoints

2 endpoints across 2 groups. See references/api-spec.lap for full details.

### getOnboardingUrl
| Method | Path | Description |
|--------|------|-------------|
| POST | /getOnboardingUrl | Get a link to a Adyen-hosted onboarding page |

### getPciQuestionnaireUrl
| Method | Path | Description |
|--------|------|-------------|
| POST | /getPciQuestionnaireUrl | Get a link to a PCI compliance questionnaire |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a getOnboardingUrl?" -> POST /getOnboardingUrl
- "Create a getPciQuestionnaireUrl?" -> POST /getPciQuestionnaireUrl
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
