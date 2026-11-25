---
name: restful4up
description: "RESTful4Up API skill. Use when working with RESTful4Up for unpack, emulation-output, clean. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# RESTful4Up
API version: 1.0.0

## Auth
No authentication required.

## Base URL
/v1

## Setup
1. No auth setup needed
3. POST /unpack -- create first unpack

## Endpoints

5 endpoints across 5 groups. See references/api-spec.lap for full details.

### unpack
| Method | Path | Description |
|--------|------|-------------|
| POST | /unpack | try to unpack the given file |

### emulation-output
| Method | Path | Description |
|--------|------|-------------|
| POST | /emulation-output | try to get the emulation output after unpacking the file |

### clean
| Method | Path | Description |
|--------|------|-------------|
| HEAD | /clean | clean up the uploaded files |

### generate-partial-yara-rules
| Method | Path | Description |
|--------|------|-------------|
| POST | /generate-partial-yara-rules | generate partial YARA rules for give executable. (Rule without the condition section) |

### apply-yara-rules
| Method | Path | Description |
|--------|------|-------------|
| POST | /apply-yara-rules | apply given YARA rules to the given executable. (upto 10 rules) |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a unpack?" -> POST /unpack
- "Create a emulation-output?" -> POST /emulation-output
- "Create a generate-partial-yara-rule?" -> POST /generate-partial-yara-rules
- "Create a apply-yara-rule?" -> POST /apply-yara-rules

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
