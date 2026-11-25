---
name: pdfbrokerio-api
description: "PdfBroker.io API skill. Use when working with PdfBroker.io for api. Covers 16 endpoints."
version: 1.0.0
generator: lapsh
---

# PdfBroker.io API
API version: v1

## Auth
OAuth2

## Base URL
Not specified.

## Setup
1. Configure auth: OAuth2
2. GET /api/pdf -- verify access
3. POST /api/pdf/xslfo -- create first xslfo

## Endpoints

16 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/pdf | Basic method to verify api is up and running |
| GET | /api/v1/pdf | Basic method to verify api is up and running |
| POST | /api/pdf/xslfo | Create pdf-file from complete XSL-FO document. |
| POST | /api/v1/pdf/xslfo | Create pdf-file from complete XSL-FO document. |
| POST | /api/pdf/xslfowithtransform | Create pdf-file from transforming xml document with Xsl-Fo transform document. |
| POST | /api/v1/pdf/xslfowithtransform | Create pdf-file from transforming xml document with Xsl-Fo transform document. |
| POST | /api/pdf/pdftoimage | Generate an image of to provided pdf file |
| POST | /api/v1/pdf/pdftoimage | Generate an image of to provided pdf file |
| POST | /api/pdf/pdfconcat | Concatenate multiple pdf files into single pdf file.. |
| POST | /api/v1/pdf/pdfconcat | Concatenate multiple pdf files into single pdf file.. |
| POST | /api/pdf/pdfwritestring | Write text on a page in a pdf document. |
| POST | /api/v1/pdf/pdfwritestring | Write text on a page in a pdf document. |
| POST | /api/pdf/weasyprint | Generate pdf file from html/url using Weasyprint. Requires paid subscription. This is our premium pdf generator. It is the most accurate and feature rich pdf generator we have with support for pdf/a-1b, pdf/a-2b, pdf/a-3b, pdf/a-4b and pdf/ua-1. |
| POST | /api/v1/pdf/weasyprint | Generate pdf file from html/url using Weasyprint. Requires paid subscription. This is our premium pdf generator. It is the most accurate and feature rich pdf generator we have with support for pdf/a-1b, pdf/a-2b, pdf/a-3b, pdf/a-4b and pdf/ua-1. |
| POST | /api/pdf/wkhtmltopdf | Generate pdf file from url using the excellent tool wkhtmltopdf. |
| POST | /api/v1/pdf/wkhtmltopdf | Generate pdf file from url using the excellent tool wkhtmltopdf. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all pdf?" -> GET /api/pdf
- "List all pdf?" -> GET /api/v1/pdf
- "Create a xslfo?" -> POST /api/pdf/xslfo
- "Create a xslfo?" -> POST /api/v1/pdf/xslfo
- "Create a xslfowithtransform?" -> POST /api/pdf/xslfowithtransform
- "Create a xslfowithtransform?" -> POST /api/v1/pdf/xslfowithtransform
- "Create a pdftoimage?" -> POST /api/pdf/pdftoimage
- "Create a pdftoimage?" -> POST /api/v1/pdf/pdftoimage
- "Create a pdfconcat?" -> POST /api/pdf/pdfconcat
- "Create a pdfconcat?" -> POST /api/v1/pdf/pdfconcat
- "Create a pdfwritestring?" -> POST /api/pdf/pdfwritestring
- "Create a pdfwritestring?" -> POST /api/v1/pdf/pdfwritestring
- "Create a weasyprint?" -> POST /api/pdf/weasyprint
- "Create a weasyprint?" -> POST /api/v1/pdf/weasyprint
- "Create a wkhtmltopdf?" -> POST /api/pdf/wkhtmltopdf
- "Create a wkhtmltopdf?" -> POST /api/v1/pdf/wkhtmltopdf
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
