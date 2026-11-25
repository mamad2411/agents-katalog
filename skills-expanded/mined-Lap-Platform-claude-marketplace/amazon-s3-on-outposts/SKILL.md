---
name: amazon-s3-on-outposts
description: "Amazon S3 on Outposts API skill. Use when working with Amazon S3 on Outposts for S3Outposts. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon S3 on Outposts
API version: 2017-07-25

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /S3Outposts/ListEndpoints -- verify access
3. POST /S3Outposts/CreateEndpoint -- create first CreateEndpoint

## Endpoints

5 endpoints across 1 groups. See references/api-spec.lap for full details.

### S3Outposts
| Method | Path | Description |
|--------|------|-------------|
| POST | /S3Outposts/CreateEndpoint | Creates an endpoint and associates it with the specified Outpost.  It can take up to 5 minutes for this action to finish.   Related actions include:    DeleteEndpoint     ListEndpoints |
| DELETE | /S3Outposts/DeleteEndpoint | Deletes an endpoint.  It can take up to 5 minutes for this action to finish.   Related actions include:    CreateEndpoint     ListEndpoints |
| GET | /S3Outposts/ListEndpoints | Lists endpoints associated with the specified Outpost.  Related actions include:    CreateEndpoint     DeleteEndpoint |
| GET | /S3Outposts/ListOutpostsWithS3 | Lists the Outposts with S3 on Outposts capacity for your Amazon Web Services account. Includes S3 on Outposts that you have access to as the Outposts owner, or as a shared user from Resource Access Manager (RAM). |
| GET | /S3Outposts/ListSharedEndpoints | Lists all endpoints associated with an Outpost that has been shared by Amazon Web Services Resource Access Manager (RAM). Related actions include:    CreateEndpoint     DeleteEndpoint |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a CreateEndpoint?" -> POST /S3Outposts/CreateEndpoint
- "List all ListEndpoints?" -> GET /S3Outposts/ListEndpoints
- "List all ListOutpostsWithS3?" -> GET /S3Outposts/ListOutpostsWithS3
- "List all ListSharedEndpoints?" -> GET /S3Outposts/ListSharedEndpoints
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
