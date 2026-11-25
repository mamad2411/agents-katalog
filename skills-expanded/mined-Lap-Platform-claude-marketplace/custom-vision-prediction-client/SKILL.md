---
name: custom-vision-prediction-client
description: "Custom Vision Prediction Client API skill. Use when working with Custom Vision Prediction Client for {projectId}. Covers 8 endpoints."
version: 1.0.0
generator: lapsh
---

# Custom Vision Prediction Client
API version: 3.0

## Auth
ApiKey Prediction-Key in header

## Base URL
https://southcentralus.api.cognitive.microsoft.com/customvision/v3.0/prediction

## Setup
1. Set your API key in the appropriate header
3. POST /{projectId}/classify/iterations/{publishedName}/url -- create first url

## Endpoints

8 endpoints across 1 groups. See references/api-spec.lap for full details.

### {projectId}
| Method | Path | Description |
|--------|------|-------------|
| POST | /{projectId}/classify/iterations/{publishedName}/url | Classify an image url and saves the result. |
| POST | /{projectId}/classify/iterations/{publishedName}/image | Classify an image and saves the result. |
| POST | /{projectId}/classify/iterations/{publishedName}/url/nostore | Classify an image url without saving the result. |
| POST | /{projectId}/classify/iterations/{publishedName}/image/nostore | Classify an image without saving the result. |
| POST | /{projectId}/detect/iterations/{publishedName}/url | Detect objects in an image url and saves the result. |
| POST | /{projectId}/detect/iterations/{publishedName}/image | Detect objects in an image and saves the result. |
| POST | /{projectId}/detect/iterations/{publishedName}/url/nostore | Detect objects in an image url without saving the result. |
| POST | /{projectId}/detect/iterations/{publishedName}/image/nostore | Detect objects in an image without saving the result. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a url?" -> POST /{projectId}/classify/iterations/{publishedName}/url
- "Create a image?" -> POST /{projectId}/classify/iterations/{publishedName}/image
- "Create a nostore?" -> POST /{projectId}/classify/iterations/{publishedName}/url/nostore
- "Create a nostore?" -> POST /{projectId}/classify/iterations/{publishedName}/image/nostore
- "Create a url?" -> POST /{projectId}/detect/iterations/{publishedName}/url
- "Create a image?" -> POST /{projectId}/detect/iterations/{publishedName}/image
- "Create a nostore?" -> POST /{projectId}/detect/iterations/{publishedName}/url/nostore
- "Create a nostore?" -> POST /{projectId}/detect/iterations/{publishedName}/image/nostore
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
