---
name: aws-cost-and-usage-report-service
description: "AWS Cost and Usage Report Service API skill. Use when working with AWS Cost and Usage Report Service for root. Covers 7 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Cost and Usage Report Service
API version: 2017-01-06

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

7 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Deletes the specified report. Any tags associated with the report are also deleted. |
| POST | / | Lists the Amazon Web Services Cost and Usage Report available to this account. |
| POST | / | Lists the tags associated with the specified report definition. |
| POST | / | Allows you to programmatically update your report preferences. |
| POST | / | Creates a new report using the description that you provide. |
| POST | / | Associates a set of tags with a report definition. |
| POST | / | Disassociates a set of tags from a report definition. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
