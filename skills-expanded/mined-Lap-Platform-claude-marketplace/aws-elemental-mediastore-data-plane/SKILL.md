---
name: aws-elemental-mediastore-data-plane
description: "AWS Elemental MediaStore Data Plane API skill. Use when working with AWS Elemental MediaStore Data Plane for {Path+}, root. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Elemental MediaStore Data Plane
API version: 2017-09-01

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET / -- verify access

## Endpoints

5 endpoints across 2 groups. See references/api-spec.lap for full details.

### {Path+}
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /{Path+} | Deletes an object at the specified path. |
| HEAD | /{Path+} | Gets the headers for an object at the specified path. |
| GET | /{Path+} | Downloads the object at the specified path. If the object’s upload availability is set to streaming, AWS Elemental MediaStore downloads the object even if it’s still uploading the object. |
| PUT | /{Path+} | Uploads an object to the specified path. Object sizes are limited to 25 MB for standard upload availability and 10 MB for streaming upload availability. |

### root
| Method | Path | Description |
|--------|------|-------------|
| GET | / | Provides a list of metadata entries about folders and objects in the specified folder. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
