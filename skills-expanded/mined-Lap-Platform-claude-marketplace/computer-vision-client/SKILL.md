---
name: computer-vision-client
description: "Computer Vision Client API skill. Use when working with Computer Vision Client for recognizeText, textOperations, read. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# Computer Vision Client
API version: 2.1

## Auth
ApiKey Ocp-Apim-Subscription-Key in header

## Base URL
https://westcentralus.api.cognitive.microsoft.com/vision/v2.1

## Setup
1. Set your API key in the appropriate header
2. GET /textOperations/{operationId} -- verify access
3. POST /recognizeText -- create first recognizeText

## Endpoints

4 endpoints across 3 groups. See references/api-spec.lap for full details.

### recognizeText
| Method | Path | Description |
|--------|------|-------------|
| POST | /recognizeText | Recognize Text operation. When you use the Recognize Text interface, the response contains a field called 'Operation-Location'. The 'Operation-Location' field contains the URL that you must use for your Get Recognize Text Operation Result operation. |

### textOperations
| Method | Path | Description |
|--------|------|-------------|
| GET | /textOperations/{operationId} | This interface is used for getting text operation result. The URL to this interface should be retrieved from 'Operation-Location' field returned from Recognize Text interface. |

### read
| Method | Path | Description |
|--------|------|-------------|
| POST | /read/core/asyncBatchAnalyze | Use this interface to get the result of a Read operation, employing the state-of-the-art Optical Character Recognition (OCR) algorithms optimized for text-heavy documents. When you use the Read File interface, the response contains a field called 'Operation-Location'. The 'Operation-Location' field contains the URL that you must use for your 'GetReadOperationResult' operation to access OCR results.​ |
| GET | /read/operations/{operationId} | This interface is used for getting OCR results of Read operation. The URL to this interface should be retrieved from 'Operation-Location' field returned from Batch Read File interface. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a recognizeText?" -> POST /recognizeText
- "Get textOperation details?" -> GET /textOperations/{operationId}
- "Create a asyncBatchAnalyze?" -> POST /read/core/asyncBatchAnalyze
- "Get operation details?" -> GET /read/operations/{operationId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
