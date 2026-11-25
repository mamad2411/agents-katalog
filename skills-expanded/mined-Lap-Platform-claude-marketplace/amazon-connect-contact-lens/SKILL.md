---
name: amazon-connect-contact-lens
description: "Amazon Connect Contact Lens API skill. Use when working with Amazon Connect Contact Lens for realtime-contact-analysis. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Amazon Connect Contact Lens
API version: 2020-08-21

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST /realtime-contact-analysis/analysis-segments -- create first analysis-segments

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### realtime-contact-analysis
| Method | Path | Description |
|--------|------|-------------|
| POST | /realtime-contact-analysis/analysis-segments | Provides a list of analysis segments for a real-time analysis session. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a analysis-segment?" -> POST /realtime-contact-analysis/analysis-segments
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
