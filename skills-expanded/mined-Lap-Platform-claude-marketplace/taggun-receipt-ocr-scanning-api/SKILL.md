---
name: taggun-receipt-ocr-scanning-api
description: "TAGGUN Receipt OCR Scanning API skill. Use when working with TAGGUN Receipt OCR Scanning for api. Covers 23 endpoints."
version: 1.0.0
generator: lapsh
---

# TAGGUN Receipt OCR Scanning API
API version: 1.16.85

## Auth
ApiKey apikey in header

## Base URL
https://api.taggun.io/

## Setup
1. Set your API key in the appropriate header
2. GET /api/account/v1/known-merchants/export -- verify access
3. POST /api/account/v1/feedback -- create first feedback

## Endpoints

23 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/account/v1/known-merchants/export | Export a list of merchant names and addresses to normalise and match in CSV format |
| GET | /api/account/v1/known-product-codes/export | Export a list of product codes to normalise and match in CSV format |
| GET | /api/account/v1/product-categories/export | Export a list of product categories and descriptions to match in CSV format |
| GET | /api/validation/v1/campaign/settings/list | list all campaign setting IDs for a client |
| GET | /api/validation/v1/campaign/settings/{campaignId} | get campaign settings for a client |
| POST | /api/account/v1/feedback | Add manually verified receipt data to a given receipt for feedback and training purposes |
| POST | /api/account/v1/known-merchants/import | Import a list of merchant names and addresses to normalise and match in CSV to TSV format. |
| POST | /api/account/v1/known-product-codes/import | Import a list of product codes to normalise in and match in CSV to TSV format. |
| POST | /api/account/v1/merchantname/add | Add a keyword to your account's model to predict merchant name. Changes in your account's model are updated daily. |
| POST | /api/account/v1/product-categories/import | Import a list of product categories and descriptions to match in CSV to TSV format. |
| POST | /api/receipt/v1/simple/encoded | transcribe a receipt using base64 encoded image in json payload |
| POST | /api/receipt/v1/simple/file | transcribe a receipt by uploading an image file |
| POST | /api/receipt/v1/simple/url | transcribe a receipt from URL |
| POST | /api/receipt/v1/verbose/encoded | transcribe a receipt using base64 encoded image in json payload and return detailed result |
| POST | /api/receipt/v1/verbose/file | transcribe a receipt by uploading an image file and return detailed result |
| POST | /api/receipt/v1/verbose/url | transcribe a receipt from URL and return detailed result |
| POST | /api/validation/v1/campaign/file | validate and match a receipt against a receipt validation settings by uploading an image file |
| POST | /api/validation/v1/campaign/product-validation/file | validate if user-submitted info like serial number are detected an image file |
| POST | /api/validation/v1/campaign/receipt-validation/file | validate and match a receipt against a receipt validation settings by uploading an image file |
| POST | /api/validation/v1/campaign/receipt-validation/url | validate and match a receipt against a receipt validation settings from URL |
| POST | /api/validation/v1/campaign/settings/create/{campaignId} | create campaign settings for a client |
| PUT | /api/validation/v1/campaign/settings/update/{campaignId} | update campaign settings for a client |
| DELETE | /api/validation/v1/campaign/settings/delete/{campaignId} | delete campaign settings for a client |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all export?" -> GET /api/account/v1/known-merchants/export
- "List all export?" -> GET /api/account/v1/known-product-codes/export
- "List all export?" -> GET /api/account/v1/product-categories/export
- "List all list?" -> GET /api/validation/v1/campaign/settings/list
- "Get setting details?" -> GET /api/validation/v1/campaign/settings/{campaignId}
- "Create a feedback?" -> POST /api/account/v1/feedback
- "Create a import?" -> POST /api/account/v1/known-merchants/import
- "Create a import?" -> POST /api/account/v1/known-product-codes/import
- "Create a add?" -> POST /api/account/v1/merchantname/add
- "Create a import?" -> POST /api/account/v1/product-categories/import
- "Create a encoded?" -> POST /api/receipt/v1/simple/encoded
- "Create a file?" -> POST /api/receipt/v1/simple/file
- "Create a url?" -> POST /api/receipt/v1/simple/url
- "Create a encoded?" -> POST /api/receipt/v1/verbose/encoded
- "Create a file?" -> POST /api/receipt/v1/verbose/file
- "Create a url?" -> POST /api/receipt/v1/verbose/url
- "Create a file?" -> POST /api/validation/v1/campaign/file
- "Create a file?" -> POST /api/validation/v1/campaign/product-validation/file
- "Create a file?" -> POST /api/validation/v1/campaign/receipt-validation/file
- "Create a url?" -> POST /api/validation/v1/campaign/receipt-validation/url
- "Update a update?" -> PUT /api/validation/v1/campaign/settings/update/{campaignId}
- "Delete a delete?" -> DELETE /api/validation/v1/campaign/settings/delete/{campaignId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
