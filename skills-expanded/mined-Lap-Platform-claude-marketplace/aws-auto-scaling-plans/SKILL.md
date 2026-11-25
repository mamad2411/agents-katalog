---
name: aws-auto-scaling-plans
description: "AWS Auto Scaling Plans API skill. Use when working with AWS Auto Scaling Plans for root. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Auto Scaling Plans
API version: 2018-01-06

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

6 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Creates a scaling plan. |
| POST | / | Deletes the specified scaling plan. Deleting a scaling plan deletes the underlying ScalingInstruction for all of the scalable resources that are covered by the plan. If the plan has launched resources or has scaling activities in progress, you must delete those resources separately. |
| POST | / | Describes the scalable resources in the specified scaling plan. |
| POST | / | Describes one or more of your scaling plans. |
| POST | / | Retrieves the forecast data for a scalable resource. Capacity forecasts are represented as predicted values, or data points, that are calculated using historical data points from a specified CloudWatch load metric. Data points are available for up to 56 days. |
| POST | / | Updates the specified scaling plan. You cannot update a scaling plan if it is in the process of being created, updated, or deleted. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
