---
name: adyen-checkout-api
description: "Adyen Checkout API skill. Use when working with Adyen Checkout for applePay, cancels, cardDetails. Covers 28 endpoints."
version: 1.0.0
generator: lapsh
---

# Adyen Checkout API
API version: 70

## Auth
ApiKey X-API-Key in header | Bearer basic

## Base URL
https://checkout-test.adyen.com/v70

## Setup
1. Set Authorization header with your Bearer token
2. GET /storedPaymentMethods -- verify access
3. POST /applePay/sessions -- create first sessions

## Endpoints

28 endpoints across 15 groups. See references/api-spec.lap for full details.

### applePay
| Method | Path | Description |
|--------|------|-------------|
| POST | /applePay/sessions | Get an Apple Pay session |

### cancels
| Method | Path | Description |
|--------|------|-------------|
| POST | /cancels | Cancel an authorised payment |

### cardDetails
| Method | Path | Description |
|--------|------|-------------|
| POST | /cardDetails | Get the brands and other details of a card |

### donationCampaigns
| Method | Path | Description |
|--------|------|-------------|
| POST | /donationCampaigns | Get a list of donation campaigns. |

### donations
| Method | Path | Description |
|--------|------|-------------|
| POST | /donations | Make a donation |

### forward
| Method | Path | Description |
|--------|------|-------------|
| POST | /forward | Forward stored payment details |

### orders
| Method | Path | Description |
|--------|------|-------------|
| POST | /orders | Create an order |
| POST | /orders/cancel | Cancel an order |

### originKeys
| Method | Path | Description |
|--------|------|-------------|
| POST | /originKeys | Create originKey values for domains |

### paymentLinks
| Method | Path | Description |
|--------|------|-------------|
| POST | /paymentLinks | Create a payment link |
| GET | /paymentLinks/{linkId} | Get a payment link |
| PATCH | /paymentLinks/{linkId} | Update the status of a payment link |

### paymentMethods
| Method | Path | Description |
|--------|------|-------------|
| POST | /paymentMethods | Get a list of available payment methods |
| POST | /paymentMethods/balance | Get the balance of a gift card |

### payments
| Method | Path | Description |
|--------|------|-------------|
| POST | /payments | Start a transaction |
| POST | /payments/details | Submit details for a payment |
| POST | /payments/{paymentPspReference}/amountUpdates | Update an authorised amount |
| POST | /payments/{paymentPspReference}/cancels | Cancel an authorised payment |
| POST | /payments/{paymentPspReference}/captures | Capture an authorised payment |
| POST | /payments/{paymentPspReference}/refunds | Refund a captured payment |
| POST | /payments/{paymentPspReference}/reversals | Refund or cancel a payment |

### paypal
| Method | Path | Description |
|--------|------|-------------|
| POST | /paypal/updateOrder | Updates the order for PayPal Express Checkout |

### sessions
| Method | Path | Description |
|--------|------|-------------|
| POST | /sessions | Create a payment session |
| GET | /sessions/{sessionId} | Get the result of a payment session |

### storedPaymentMethods
| Method | Path | Description |
|--------|------|-------------|
| GET | /storedPaymentMethods | Get tokens for stored payment details |
| POST | /storedPaymentMethods | Create a token to store payment details |
| DELETE | /storedPaymentMethods/{storedPaymentMethodId} | Delete a token for stored payment details |

### validateShopperId
| Method | Path | Description |
|--------|------|-------------|
| POST | /validateShopperId | Validates shopper Id |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a session?" -> POST /applePay/sessions
- "Create a cancel?" -> POST /cancels
- "Create a cardDetail?" -> POST /cardDetails
- "Create a donationCampaign?" -> POST /donationCampaigns
- "Create a donation?" -> POST /donations
- "Create a forward?" -> POST /forward
- "Create a order?" -> POST /orders
- "Create a cancel?" -> POST /orders/cancel
- "Create a originKey?" -> POST /originKeys
- "Create a paymentLink?" -> POST /paymentLinks
- "Get paymentLink details?" -> GET /paymentLinks/{linkId}
- "Partially update a paymentLink?" -> PATCH /paymentLinks/{linkId}
- "Create a paymentMethod?" -> POST /paymentMethods
- "Create a balance?" -> POST /paymentMethods/balance
- "Create a payment?" -> POST /payments
- "Create a detail?" -> POST /payments/details
- "Create a amountUpdate?" -> POST /payments/{paymentPspReference}/amountUpdates
- "Create a cancel?" -> POST /payments/{paymentPspReference}/cancels
- "Create a capture?" -> POST /payments/{paymentPspReference}/captures
- "Create a refund?" -> POST /payments/{paymentPspReference}/refunds
- "Create a reversal?" -> POST /payments/{paymentPspReference}/reversals
- "Create a updateOrder?" -> POST /paypal/updateOrder
- "Create a session?" -> POST /sessions
- "Get session details?" -> GET /sessions/{sessionId}
- "List all storedPaymentMethods?" -> GET /storedPaymentMethods
- "Create a storedPaymentMethod?" -> POST /storedPaymentMethods
- "Delete a storedPaymentMethod?" -> DELETE /storedPaymentMethods/{storedPaymentMethodId}
- "Create a validateShopperId?" -> POST /validateShopperId
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
