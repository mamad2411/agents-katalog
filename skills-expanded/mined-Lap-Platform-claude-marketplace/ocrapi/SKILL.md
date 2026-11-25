---
name: ocrapi
description: "ocrapi API skill. Use when working with ocrapi for ocr. Covers 20 endpoints."
version: 1.0.0
generator: lapsh
---

# ocrapi
API version: v1

## Auth
ApiKey Apikey in header

## Base URL
http://localhost

## Setup
1. Set your API key in the appropriate header
2. GET /ocr/pdf/get-job-status -- verify access
3. POST /ocr/image/toText -- create first toText

## Endpoints

20 endpoints across 1 groups. See references/api-spec.lap for full details.

### ocr
| Method | Path | Description |
|--------|------|-------------|
| POST | /ocr/image/toText | Convert a scanned image into text |
| POST | /ocr/image/to/words-with-location | Convert a scanned image into words with location |
| POST | /ocr/image/to/lines-with-location | Convert a scanned image into words with location |
| POST | /ocr/photo/toText | Convert a photo of a document into text |
| POST | /ocr/photo/to/words-with-location | Convert a photo of a document or receipt into words with location |
| POST | /ocr/photo/recognize/receipt | Recognize a photo of a receipt, extract key business information |
| POST | /ocr/photo/recognize/business-card | Recognize a photo of a business card, extract key business information |
| POST | /ocr/photo/recognize/form | Recognize a photo of a form, extract key fields and business information |
| POST | /ocr/photo/recognize/form/advanced | Recognize a photo of a form, extract key fields using stored templates |
| POST | /ocr/pdf/toText | Converts an uploaded PDF file into text via Optical Character Recognition. |
| GET | /ocr/pdf/get-job-status | Returns the result of the Async Job - possible states can be STARTED or COMPLETED |
| POST | /ocr/pdf/to/words-with-location | Convert a PDF into words with location |
| POST | /ocr/pdf/to/lines-with-location | Convert a PDF into text lines with location |
| POST | /ocr/preprocessing/image/binarize | Convert an image of text into a binarized (light and dark) view |
| POST | /ocr/preprocessing/image/binarize/advanced | Convert an image of text into a binary (light and dark) view with ML |
| POST | /ocr/preprocessing/image/get-page-angle | Get the angle of the page / document / receipt |
| POST | /ocr/preprocessing/image/unrotate | Detect and unrotate a document image |
| POST | /ocr/preprocessing/image/unrotate/advanced | Detect and unrotate a document image (advanced) |
| POST | /ocr/preprocessing/image/unskew | Detect and unskew a photo of a document |
| POST | /ocr/receipts/photo/to/csv | Convert a photo of a receipt into a CSV file containing structured information from the receipt |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a toText?" -> POST /ocr/image/toText
- "Create a words-with-location?" -> POST /ocr/image/to/words-with-location
- "Create a lines-with-location?" -> POST /ocr/image/to/lines-with-location
- "Create a toText?" -> POST /ocr/photo/toText
- "Create a words-with-location?" -> POST /ocr/photo/to/words-with-location
- "Create a receipt?" -> POST /ocr/photo/recognize/receipt
- "Create a business-card?" -> POST /ocr/photo/recognize/business-card
- "Create a form?" -> POST /ocr/photo/recognize/form
- "Create a advanced?" -> POST /ocr/photo/recognize/form/advanced
- "Create a toText?" -> POST /ocr/pdf/toText
- "List all get-job-status?" -> GET /ocr/pdf/get-job-status
- "Create a words-with-location?" -> POST /ocr/pdf/to/words-with-location
- "Create a lines-with-location?" -> POST /ocr/pdf/to/lines-with-location
- "Create a binarize?" -> POST /ocr/preprocessing/image/binarize
- "Create a advanced?" -> POST /ocr/preprocessing/image/binarize/advanced
- "Create a get-page-angle?" -> POST /ocr/preprocessing/image/get-page-angle
- "Create a unrotate?" -> POST /ocr/preprocessing/image/unrotate
- "Create a advanced?" -> POST /ocr/preprocessing/image/unrotate/advanced
- "Create a unskew?" -> POST /ocr/preprocessing/image/unskew
- "Create a csv?" -> POST /ocr/receipts/photo/to/csv
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
