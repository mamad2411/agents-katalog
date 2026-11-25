---
name: aws-cloud9
description: "AWS Cloud9 API skill. Use when working with AWS Cloud9 for root. Covers 13 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Cloud9
API version: 2017-09-23

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

13 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Creates an Cloud9 development environment, launches an Amazon Elastic Compute Cloud (Amazon EC2) instance, and then connects from the instance to the environment. |
| POST | / | Adds an environment member to an Cloud9 development environment. |
| POST | / | Deletes an Cloud9 development environment. If an Amazon EC2 instance is connected to the environment, also terminates the instance. |
| POST | / | Deletes an environment member from a development environment. |
| POST | / | Gets information about environment members for an Cloud9 development environment. |
| POST | / | Gets status information for an Cloud9 development environment. |
| POST | / | Gets information about Cloud9 development environments. |
| POST | / | Gets a list of Cloud9 development environment identifiers. |
| POST | / | Gets a list of the tags associated with an Cloud9 development environment. |
| POST | / | Adds tags to an Cloud9 development environment.  Tags that you add to an Cloud9 environment by using this method will NOT be automatically propagated to underlying resources. |
| POST | / | Removes tags from an Cloud9 development environment. |
| POST | / | Changes the settings of an existing Cloud9 development environment. |
| POST | / | Changes the settings of an existing environment member for an Cloud9 development environment. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
