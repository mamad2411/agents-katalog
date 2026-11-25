---
name: adyen-payment-api
description: "Adyen Payment API skill. Use when working with Adyen Payment for adjustAuthorisation, authorise, authorise3d. Covers 13 endpoints."
version: 1.0.0
generator: lapsh
---

# Adyen Payment API
API version: 68

## Auth
ApiKey X-API-Key in header | Bearer basic

## Base URL
https://pal-test.adyen.com/pal/servlet/Payment/v68

## Setup
1. Set Authorization header with your Bearer token
3. POST /adjustAuthorisation -- create first adjustAuthorisation

## Endpoints

13 endpoints across 13 groups. See references/api-spec.lap for full details.

### adjustAuthorisation
| Method | Path | Description |
|--------|------|-------------|
| POST | /adjustAuthorisation | Change the authorised amount |

### authorise
| Method | Path | Description |
|--------|------|-------------|
| POST | /authorise | Create an authorisation |

### authorise3d
| Method | Path | Description |
|--------|------|-------------|
| POST | /authorise3d | Complete a 3DS authorisation |

### authorise3ds2
| Method | Path | Description |
|--------|------|-------------|
| POST | /authorise3ds2 | Complete a 3DS2 authorisation |

### cancel
| Method | Path | Description |
|--------|------|-------------|
| POST | /cancel | Cancel an authorisation |

### cancelOrRefund
| Method | Path | Description |
|--------|------|-------------|
| POST | /cancelOrRefund | Cancel or refund a payment |

### capture
| Method | Path | Description |
|--------|------|-------------|
| POST | /capture | Capture an authorisation |

### donate
| Method | Path | Description |
|--------|------|-------------|
| POST | /donate | Create a donation |

### getAuthenticationResult
| Method | Path | Description |
|--------|------|-------------|
| POST | /getAuthenticationResult | Get the 3DS authentication result |

### refund
| Method | Path | Description |
|--------|------|-------------|
| POST | /refund | Refund a captured payment |

### retrieve3ds2Result
| Method | Path | Description |
|--------|------|-------------|
| POST | /retrieve3ds2Result | Get the 3DS2 authentication result |

### technicalCancel
| Method | Path | Description |
|--------|------|-------------|
| POST | /technicalCancel | Cancel an authorisation using your reference |

### voidPendingRefund
| Method | Path | Description |
|--------|------|-------------|
| POST | /voidPendingRefund | Cancel an in-person refund |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a adjustAuthorisation?" -> POST /adjustAuthorisation
- "Create a authorise?" -> POST /authorise
- "Create a authorise3d?" -> POST /authorise3d
- "Create a authorise3ds2?" -> POST /authorise3ds2
- "Create a cancel?" -> POST /cancel
- "Create a cancelOrRefund?" -> POST /cancelOrRefund
- "Create a capture?" -> POST /capture
- "Create a donate?" -> POST /donate
- "Create a getAuthenticationResult?" -> POST /getAuthenticationResult
- "Create a refund?" -> POST /refund
- "Create a retrieve3ds2Result?" -> POST /retrieve3ds2Result
- "Create a technicalCancel?" -> POST /technicalCancel
- "Create a voidPendingRefund?" -> POST /voidPendingRefund
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
