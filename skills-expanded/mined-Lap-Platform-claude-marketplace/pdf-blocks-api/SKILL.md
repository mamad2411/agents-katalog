---
name: pdf-blocks-api
description: "PDF Blocks API skill. Use when working with PDF Blocks for add_password, add_watermark, merge_documents. Covers 12 endpoints."
version: 1.0.0
generator: lapsh
---

# PDF Blocks API
API version: 1.5.0

## Auth
ApiKey X-Api-Key in header

## Base URL
https://api.pdfblocks.com

## Setup
1. Set your API key in the appropriate header
3. POST /v1/add_password -- create first add_password

## Endpoints

12 endpoints across 11 groups. See references/api-spec.lap for full details.

### add_password
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/add_password | Add a password to a PDF |

### add_watermark
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/add_watermark/text | Add a text watermark to a PDF |
| POST | /v1/add_watermark/image | Add an image watermark to a PDF |

### merge_documents
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/merge_documents | Merge PDF documents |

### extract_pages
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/extract_pages | Extract pages from a PDF |

### remove_pages
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/remove_pages | Remove pages from a PDF |

### rotate_pages
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/rotate_pages | Rotate pages in a PDF |

### add_restrictions
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/add_restrictions | Add restrictions to a PDF |

### remove_password
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/remove_password | Remove the password from a PDF |

### remove_restrictions
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/remove_restrictions | Remove the restrictions from a PDF |

### remove_signatures
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/remove_signatures | Remove the signatures from a PDF |

### reverse_pages
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/reverse_pages | Reverse the pages of a PDF |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a add_password?" -> POST /v1/add_password
- "Create a text?" -> POST /v1/add_watermark/text
- "Create a image?" -> POST /v1/add_watermark/image
- "Create a merge_document?" -> POST /v1/merge_documents
- "Create a extract_page?" -> POST /v1/extract_pages
- "Create a remove_page?" -> POST /v1/remove_pages
- "Create a rotate_page?" -> POST /v1/rotate_pages
- "Create a add_restriction?" -> POST /v1/add_restrictions
- "Create a remove_password?" -> POST /v1/remove_password
- "Create a remove_restriction?" -> POST /v1/remove_restrictions
- "Create a remove_signature?" -> POST /v1/remove_signatures
- "Create a reverse_page?" -> POST /v1/reverse_pages
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
