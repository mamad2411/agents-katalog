---
name: payment-initiation-api
description: "Payment Initiation API skill. Use when working with Payment Initiation for domestic-payment-consents, domestic-payments, domestic-scheduled-payment-consents. Covers 41 endpoints."
version: 1.0.0
generator: lapsh
---

# Payment Initiation API
API version: 4.0.0

## Auth
OAuth2 | OAuth2

## Base URL
/open-banking/v4.0/pisp

## Setup
1. Configure auth: OAuth2 | OAuth2
2. GET /domestic-payment-consents/{ConsentId}/funds-confirmation -- verify access
3. POST /domestic-payment-consents -- create first domestic-payment-consents

## Endpoints

41 endpoints across 14 groups. See references/api-spec.lap for full details.

### domestic-payment-consents
| Method | Path | Description |
|--------|------|-------------|
| POST | /domestic-payment-consents | Create Domestic Payment Consents |
| GET | /domestic-payment-consents/{ConsentId} | Get Domestic Payment Consents |
| GET | /domestic-payment-consents/{ConsentId}/funds-confirmation | Get Domestic Payment Consents Funds Confirmation |

### domestic-payments
| Method | Path | Description |
|--------|------|-------------|
| POST | /domestic-payments | Create Domestic Payments |
| GET | /domestic-payments/{DomesticPaymentId} | Get Domestic Payments |
| GET | /domestic-payments/{DomesticPaymentId}/payment-details | Get Payment Details |

### domestic-scheduled-payment-consents
| Method | Path | Description |
|--------|------|-------------|
| POST | /domestic-scheduled-payment-consents | Create Domestic Scheduled Payment Consents |
| GET | /domestic-scheduled-payment-consents/{ConsentId} | Get Domestic Scheduled Payment Consents |

### domestic-scheduled-payments
| Method | Path | Description |
|--------|------|-------------|
| POST | /domestic-scheduled-payments | Create Domestic Scheduled Payments |
| GET | /domestic-scheduled-payments/{DomesticScheduledPaymentId} | Get Domestic Scheduled Payments |
| GET | /domestic-scheduled-payments/{DomesticScheduledPaymentId}/payment-details | Get Payment Details |

### domestic-standing-order-consents
| Method | Path | Description |
|--------|------|-------------|
| POST | /domestic-standing-order-consents | Create Domestic Standing Order Consents |
| GET | /domestic-standing-order-consents/{ConsentId} | Get Domestic Standing Order Consents |

### domestic-standing-orders
| Method | Path | Description |
|--------|------|-------------|
| POST | /domestic-standing-orders | Create Domestic Standing Orders |
| GET | /domestic-standing-orders/{DomesticStandingOrderId} | Get Domestic Standing Orders |
| GET | /domestic-standing-orders/{DomesticStandingOrderId}/payment-details | Get Payment Details |

### file-payment-consents
| Method | Path | Description |
|--------|------|-------------|
| POST | /file-payment-consents | Create File Payment Consents |
| GET | /file-payment-consents/{ConsentId} | Get File Payment Consents |
| POST | /file-payment-consents/{ConsentId}/file | Create File Payment Consents |
| GET | /file-payment-consents/{ConsentId}/file | Get File Payment Consents |

### file-payments
| Method | Path | Description |
|--------|------|-------------|
| POST | /file-payments | Create File Payments |
| GET | /file-payments/{FilePaymentId} | Get File Payments |
| GET | /file-payments/{FilePaymentId}/payment-details | Get Payment Details |
| GET | /file-payments/{FilePaymentId}/report-file | Get File Payments |

### international-payment-consents
| Method | Path | Description |
|--------|------|-------------|
| POST | /international-payment-consents | Create International Payment Consents |
| GET | /international-payment-consents/{ConsentId} | Get International Payment Consents |
| GET | /international-payment-consents/{ConsentId}/funds-confirmation | Get International Payment Consents Funds Confirmation |

### international-payments
| Method | Path | Description |
|--------|------|-------------|
| POST | /international-payments | Create International Payments |
| GET | /international-payments/{InternationalPaymentId} | Get International Payments |
| GET | /international-payments/{InternationalPaymentId}/payment-details | Get Payment Details |

### international-scheduled-payment-consents
| Method | Path | Description |
|--------|------|-------------|
| POST | /international-scheduled-payment-consents | Create International Scheduled Payment Consents |
| GET | /international-scheduled-payment-consents/{ConsentId} | Get International Scheduled Payment Consents |
| GET | /international-scheduled-payment-consents/{ConsentId}/funds-confirmation | Get International Scheduled Payment Consents Funds Confirmation |

### international-scheduled-payments
| Method | Path | Description |
|--------|------|-------------|
| POST | /international-scheduled-payments | Create International Scheduled Payments |
| GET | /international-scheduled-payments/{InternationalScheduledPaymentId} | Get International Scheduled Payments |
| GET | /international-scheduled-payments/{InternationalScheduledPaymentId}/payment-details | Get Payment Details |

### international-standing-order-consents
| Method | Path | Description |
|--------|------|-------------|
| POST | /international-standing-order-consents | Create International Standing Order Consents |
| GET | /international-standing-order-consents/{ConsentId} | Get International Standing Order Consents |

### international-standing-orders
| Method | Path | Description |
|--------|------|-------------|
| POST | /international-standing-orders | Create International Standing Orders |
| GET | /international-standing-orders/{InternationalStandingOrderPaymentId} | Get International Standing Orders |
| GET | /international-standing-orders/{InternationalStandingOrderPaymentId}/payment-details | Get Payment Details |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a domestic-payment-consent?" -> POST /domestic-payment-consents
- "Get domestic-payment-consent details?" -> GET /domestic-payment-consents/{ConsentId}
- "List all funds-confirmation?" -> GET /domestic-payment-consents/{ConsentId}/funds-confirmation
- "Create a domestic-payment?" -> POST /domestic-payments
- "Get domestic-payment details?" -> GET /domestic-payments/{DomesticPaymentId}
- "List all payment-details?" -> GET /domestic-payments/{DomesticPaymentId}/payment-details
- "Create a domestic-scheduled-payment-consent?" -> POST /domestic-scheduled-payment-consents
- "Get domestic-scheduled-payment-consent details?" -> GET /domestic-scheduled-payment-consents/{ConsentId}
- "Create a domestic-scheduled-payment?" -> POST /domestic-scheduled-payments
- "Get domestic-scheduled-payment details?" -> GET /domestic-scheduled-payments/{DomesticScheduledPaymentId}
- "List all payment-details?" -> GET /domestic-scheduled-payments/{DomesticScheduledPaymentId}/payment-details
- "Create a domestic-standing-order-consent?" -> POST /domestic-standing-order-consents
- "Get domestic-standing-order-consent details?" -> GET /domestic-standing-order-consents/{ConsentId}
- "Create a domestic-standing-order?" -> POST /domestic-standing-orders
- "Get domestic-standing-order details?" -> GET /domestic-standing-orders/{DomesticStandingOrderId}
- "List all payment-details?" -> GET /domestic-standing-orders/{DomesticStandingOrderId}/payment-details
- "Create a file-payment-consent?" -> POST /file-payment-consents
- "Get file-payment-consent details?" -> GET /file-payment-consents/{ConsentId}
- "Create a file?" -> POST /file-payment-consents/{ConsentId}/file
- "List all file?" -> GET /file-payment-consents/{ConsentId}/file
- "Create a file-payment?" -> POST /file-payments
- "Get file-payment details?" -> GET /file-payments/{FilePaymentId}
- "List all payment-details?" -> GET /file-payments/{FilePaymentId}/payment-details
- "List all report-file?" -> GET /file-payments/{FilePaymentId}/report-file
- "Create a international-payment-consent?" -> POST /international-payment-consents
- "Get international-payment-consent details?" -> GET /international-payment-consents/{ConsentId}
- "List all funds-confirmation?" -> GET /international-payment-consents/{ConsentId}/funds-confirmation
- "Create a international-payment?" -> POST /international-payments
- "Get international-payment details?" -> GET /international-payments/{InternationalPaymentId}
- "List all payment-details?" -> GET /international-payments/{InternationalPaymentId}/payment-details
- "Create a international-scheduled-payment-consent?" -> POST /international-scheduled-payment-consents
- "Get international-scheduled-payment-consent details?" -> GET /international-scheduled-payment-consents/{ConsentId}
- "List all funds-confirmation?" -> GET /international-scheduled-payment-consents/{ConsentId}/funds-confirmation
- "Create a international-scheduled-payment?" -> POST /international-scheduled-payments
- "Get international-scheduled-payment details?" -> GET /international-scheduled-payments/{InternationalScheduledPaymentId}
- "List all payment-details?" -> GET /international-scheduled-payments/{InternationalScheduledPaymentId}/payment-details
- "Create a international-standing-order-consent?" -> POST /international-standing-order-consents
- "Get international-standing-order-consent details?" -> GET /international-standing-order-consents/{ConsentId}
- "Create a international-standing-order?" -> POST /international-standing-orders
- "Get international-standing-order details?" -> GET /international-standing-orders/{InternationalStandingOrderPaymentId}
- "List all payment-details?" -> GET /international-standing-orders/{InternationalStandingOrderPaymentId}/payment-details
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
