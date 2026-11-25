---
name: neutrino-api
description: "Neutrino API skill. Use when working with Neutrino for html-render, image-watermark, qr-code. Covers 28 endpoints."
version: 1.0.0
generator: lapsh
---

# Neutrino API
API version: 3.7.2

## Auth
ApiKey user-id in header | ApiKey api-key in header

## Base URL
https://neutrinoapi.net/

## Setup
1. Set your API key in the appropriate header
2. GET /hlr-lookup -- verify access
3. POST /html-render -- create first html-render

## Endpoints

28 endpoints across 28 groups. See references/api-spec.lap for full details.

### html-render
| Method | Path | Description |
|--------|------|-------------|
| POST | /html-render | HTML Render |

### image-watermark
| Method | Path | Description |
|--------|------|-------------|
| POST | /image-watermark | Image Watermark |

### qr-code
| Method | Path | Description |
|--------|------|-------------|
| POST | /qr-code | QR Code |

### image-resize
| Method | Path | Description |
|--------|------|-------------|
| POST | /image-resize | Image Resize |

### sms-verify
| Method | Path | Description |
|--------|------|-------------|
| POST | /sms-verify | SMS Verify |

### phone-playback
| Method | Path | Description |
|--------|------|-------------|
| POST | /phone-playback | Phone Playback |

### hlr-lookup
| Method | Path | Description |
|--------|------|-------------|
| GET | /hlr-lookup | HLR Lookup |

### verify-security-code
| Method | Path | Description |
|--------|------|-------------|
| GET | /verify-security-code | Verify Security Code |

### phone-verify
| Method | Path | Description |
|--------|------|-------------|
| POST | /phone-verify | Phone Verify |

### email-validate
| Method | Path | Description |
|--------|------|-------------|
| GET | /email-validate | Email Validate |

### bad-word-filter
| Method | Path | Description |
|--------|------|-------------|
| POST | /bad-word-filter | Bad Word Filter |

### ua-lookup
| Method | Path | Description |
|--------|------|-------------|
| GET | /ua-lookup | UA Lookup |

### phone-validate
| Method | Path | Description |
|--------|------|-------------|
| GET | /phone-validate | Phone Validate |

### ip-blocklist-download
| Method | Path | Description |
|--------|------|-------------|
| GET | /ip-blocklist-download | IP Blocklist Download |

### ip-probe
| Method | Path | Description |
|--------|------|-------------|
| GET | /ip-probe | IP Probe |

### host-reputation
| Method | Path | Description |
|--------|------|-------------|
| GET | /host-reputation | Host Reputation |

### email-verify
| Method | Path | Description |
|--------|------|-------------|
| GET | /email-verify | Email Verify |

### domain-lookup
| Method | Path | Description |
|--------|------|-------------|
| GET | /domain-lookup | Domain Lookup |

### ip-blocklist
| Method | Path | Description |
|--------|------|-------------|
| GET | /ip-blocklist | IP Blocklist |

### ip-info
| Method | Path | Description |
|--------|------|-------------|
| GET | /ip-info | IP Info |

### geocode-reverse
| Method | Path | Description |
|--------|------|-------------|
| GET | /geocode-reverse | Geocode Reverse |

### geocode-address
| Method | Path | Description |
|--------|------|-------------|
| GET | /geocode-address | Geocode Address |

### bin-list-download
| Method | Path | Description |
|--------|------|-------------|
| GET | /bin-list-download | BIN List Download |

### convert
| Method | Path | Description |
|--------|------|-------------|
| GET | /convert | Convert |

### bin-lookup
| Method | Path | Description |
|--------|------|-------------|
| GET | /bin-lookup | BIN Lookup |

### html-clean
| Method | Path | Description |
|--------|------|-------------|
| POST | /html-clean | HTML Clean |

### url-info
| Method | Path | Description |
|--------|------|-------------|
| GET | /url-info | URL Info |

### browser-bot
| Method | Path | Description |
|--------|------|-------------|
| POST | /browser-bot | Browser Bot |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a html-render?" -> POST /html-render
- "Create a image-watermark?" -> POST /image-watermark
- "Create a qr-code?" -> POST /qr-code
- "Create a image-resize?" -> POST /image-resize
- "Create a sms-verify?" -> POST /sms-verify
- "Create a phone-playback?" -> POST /phone-playback
- "List all hlr-lookup?" -> GET /hlr-lookup
- "List all verify-security-code?" -> GET /verify-security-code
- "Create a phone-verify?" -> POST /phone-verify
- "List all email-validate?" -> GET /email-validate
- "Create a bad-word-filter?" -> POST /bad-word-filter
- "List all ua-lookup?" -> GET /ua-lookup
- "List all phone-validate?" -> GET /phone-validate
- "List all ip-blocklist-download?" -> GET /ip-blocklist-download
- "List all ip-probe?" -> GET /ip-probe
- "List all host-reputation?" -> GET /host-reputation
- "List all email-verify?" -> GET /email-verify
- "List all domain-lookup?" -> GET /domain-lookup
- "List all ip-blocklist?" -> GET /ip-blocklist
- "List all ip-info?" -> GET /ip-info
- "List all geocode-reverse?" -> GET /geocode-reverse
- "List all geocode-address?" -> GET /geocode-address
- "List all bin-list-download?" -> GET /bin-list-download
- "List all convert?" -> GET /convert
- "List all bin-lookup?" -> GET /bin-lookup
- "Create a html-clean?" -> POST /html-clean
- "List all url-info?" -> GET /url-info
- "Create a browser-bot?" -> POST /browser-bot
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
