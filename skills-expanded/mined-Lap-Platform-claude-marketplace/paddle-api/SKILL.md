---
name: paddle-api
description: "Paddle API skill. Use when working with Paddle for customers, adjustments, client-tokens. Covers 87 endpoints."
version: 1.0.0
generator: lapsh
---

# Paddle API
API version: 1.0

## Auth
Bearer Bearer

## Base URL
https://sandbox-api.paddle.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /adjustments -- verify access
3. POST /customers/{customer_id}/addresses -- create first addresses

## Endpoints

87 endpoints across 18 groups. See references/api-spec.lap for full details.

### customers
| Method | Path | Description |
|--------|------|-------------|
| GET | /customers/{customer_id}/addresses | List addresses for a customer |
| POST | /customers/{customer_id}/addresses | Create an address for a customer |
| GET | /customers/{customer_id}/addresses/{address_id} | Get an address for a customer |
| PATCH | /customers/{customer_id}/addresses/{address_id} | Update an address for a customer |
| GET | /customers/{customer_id}/businesses | List businesses for a customer |
| POST | /customers/{customer_id}/businesses | Create a business for a customer |
| GET | /customers/{customer_id}/businesses/{business_id} | Get a business for a customer |
| PATCH | /customers/{customer_id}/businesses/{business_id} | Update a business for a customer |
| GET | /customers | List customers |
| POST | /customers | Create a customer |
| GET | /customers/{customer_id} | Get a customer |
| PATCH | /customers/{customer_id} | Update a customer |
| GET | /customers/{customer_id}/credit-balances | List credit balances for a customer |
| POST | /customers/{customer_id}/auth-token | Generate an authentication token for a customer |
| POST | /customers/{customer_id}/portal-sessions | Create a customer portal session |
| GET | /customers/{customer_id}/payment-methods | List payment methods for a customer |
| GET | /customers/{customer_id}/payment-methods/{payment_method_id} | Get a payment method for a customer |
| DELETE | /customers/{customer_id}/payment-methods/{payment_method_id} | Delete a payment method for a customer |

### adjustments
| Method | Path | Description |
|--------|------|-------------|
| GET | /adjustments | List adjustments |
| POST | /adjustments | Create an adjustment |
| GET | /adjustments/{adjustment_id}/credit-note | Get a PDF credit note for an adjustment |

### client-tokens
| Method | Path | Description |
|--------|------|-------------|
| GET | /client-tokens | List client-side tokens |
| POST | /client-tokens | Create a client-side token |
| GET | /client-tokens/{client_token_id} | Get a client-side token |
| PATCH | /client-tokens/{client_token_id} | Update a client-side token |

### discount-groups
| Method | Path | Description |
|--------|------|-------------|
| GET | /discount-groups | List discount groups |
| POST | /discount-groups | Create a discount group |
| GET | /discount-groups/{discount_group_id} | Get a discount group |
| PATCH | /discount-groups/{discount_group_id} | Update a discount group |

### discounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /discounts | List discounts |
| POST | /discounts | Create a discount |
| GET | /discounts/{discount_id} | Get a discount |
| PATCH | /discounts/{discount_id} | Update a discount |

### event-types
| Method | Path | Description |
|--------|------|-------------|
| GET | /event-types | List events types |

### events
| Method | Path | Description |
|--------|------|-------------|
| GET | /events | List events |

### ips
| Method | Path | Description |
|--------|------|-------------|
| GET | /ips | Get Paddle IP addresses |

### notification-settings
| Method | Path | Description |
|--------|------|-------------|
| GET | /notification-settings | List notification settings |
| POST | /notification-settings | Create a notification setting |
| GET | /notification-settings/{notification_setting_id} | Get a notification setting |
| PATCH | /notification-settings/{notification_setting_id} | Update a notification setting |
| DELETE | /notification-settings/{notification_setting_id} | Delete a notification setting |

### notifications
| Method | Path | Description |
|--------|------|-------------|
| GET | /notifications | List notifications |
| GET | /notifications/{notification_id} | Get a notification |
| GET | /notifications/{notification_id}/logs | List logs for a notification |
| POST | /notifications/{notification_id}/replay | Replay a notification |

### prices
| Method | Path | Description |
|--------|------|-------------|
| GET | /prices | List prices |
| POST | /prices | Create a price |
| GET | /prices/{price_id} | Get a price |
| PATCH | /prices/{price_id} | Update a price |

### pricing-preview
| Method | Path | Description |
|--------|------|-------------|
| POST | /pricing-preview | Preview prices |

### products
| Method | Path | Description |
|--------|------|-------------|
| GET | /products | List products |
| POST | /products | Create a product |
| GET | /products/{product_id} | Get a product |
| PATCH | /products/{product_id} | Update a product |

### reports
| Method | Path | Description |
|--------|------|-------------|
| GET | /reports | List reports |
| POST | /reports | Create a report |
| GET | /reports/{report_id} | Get a report |
| GET | /reports/{report_id}/download-url | Get a CSV file for a report |

### simulation-types
| Method | Path | Description |
|--------|------|-------------|
| GET | /simulation-types | List simulation types |

### simulations
| Method | Path | Description |
|--------|------|-------------|
| GET | /simulations | List simulations |
| POST | /simulations | Create a simulation |
| GET | /simulations/{simulation_id} | Get a simulation |
| PATCH | /simulations/{simulation_id} | Update a simulation |
| GET | /simulations/{simulation_id}/runs | List runs for a simulation |
| POST | /simulations/{simulation_id}/runs | Create a run for a simulation |
| GET | /simulations/{simulation_id}/runs/{simulation_run_id} | Get a run for a simulation |
| GET | /simulations/{simulation_id}/runs/{simulation_run_id}/events | List events for a simulation run |
| GET | /simulations/{simulation_id}/runs/{simulation_run_id}/events/{simulation_event_id} | Get an event for a simulation run |
| POST | /simulations/{simulation_id}/runs/{simulation_run_id}/events/{simulation_event_id}/replay | Replay an event for a simulation run |

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions | List subscriptions |
| GET | /subscriptions/{subscription_id} | Get a subscription |
| PATCH | /subscriptions/{subscription_id} | Update a subscription |
| POST | /subscriptions/{subscription_id}/cancel | Cancel a subscription |
| POST | /subscriptions/{subscription_id}/pause | Pause a subscription |
| POST | /subscriptions/{subscription_id}/resume | Resume a paused subscription |
| POST | /subscriptions/{subscription_id}/activate | Activate a trialing subscription |
| GET | /subscriptions/{subscription_id}/update-payment-method-transaction | Get a transaction to update payment method |
| PATCH | /subscriptions/{subscription_id}/preview | Preview an update to a subscription |
| POST | /subscriptions/{subscription_id}/charge | Create a one-time charge for a subscription |
| POST | /subscriptions/{subscription_id}/charge/preview | Preview a one-time charge for a subscription |

### transactions
| Method | Path | Description |
|--------|------|-------------|
| GET | /transactions | List transactions |
| POST | /transactions | Create a transaction |
| GET | /transactions/{transaction_id} | Get a transaction |
| PATCH | /transactions/{transaction_id} | Update a transaction |
| POST | /transactions/preview | Preview a transaction |
| POST | /transactions/{transaction_id}/revise | Revise customer information on a billed or completed transaction |
| GET | /transactions/{transaction_id}/invoice | Get a PDF invoice for a transaction |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search addresses?" -> GET /customers/{customer_id}/addresses
- "Create a address?" -> POST /customers/{customer_id}/addresses
- "Get address details?" -> GET /customers/{customer_id}/addresses/{address_id}
- "Partially update a address?" -> PATCH /customers/{customer_id}/addresses/{address_id}
- "List all adjustments?" -> GET /adjustments
- "Create a adjustment?" -> POST /adjustments
- "List all credit-note?" -> GET /adjustments/{adjustment_id}/credit-note
- "Search businesses?" -> GET /customers/{customer_id}/businesses
- "Create a business?" -> POST /customers/{customer_id}/businesses
- "Get business details?" -> GET /customers/{customer_id}/businesses/{business_id}
- "Partially update a business?" -> PATCH /customers/{customer_id}/businesses/{business_id}
- "List all client-tokens?" -> GET /client-tokens
- "Create a client-token?" -> POST /client-tokens
- "Get client-token details?" -> GET /client-tokens/{client_token_id}
- "Partially update a client-token?" -> PATCH /client-tokens/{client_token_id}
- "Search customers?" -> GET /customers
- "Create a customer?" -> POST /customers
- "Get customer details?" -> GET /customers/{customer_id}
- "Partially update a customer?" -> PATCH /customers/{customer_id}
- "List all credit-balances?" -> GET /customers/{customer_id}/credit-balances
- "Create a auth-token?" -> POST /customers/{customer_id}/auth-token
- "Create a portal-session?" -> POST /customers/{customer_id}/portal-sessions
- "List all discount-groups?" -> GET /discount-groups
- "Create a discount-group?" -> POST /discount-groups
- "Get discount-group details?" -> GET /discount-groups/{discount_group_id}
- "Partially update a discount-group?" -> PATCH /discount-groups/{discount_group_id}
- "List all discounts?" -> GET /discounts
- "Create a discount?" -> POST /discounts
- "Get discount details?" -> GET /discounts/{discount_id}
- "Partially update a discount?" -> PATCH /discounts/{discount_id}
- "List all event-types?" -> GET /event-types
- "List all events?" -> GET /events
- "List all ips?" -> GET /ips
- "List all notification-settings?" -> GET /notification-settings
- "Create a notification-setting?" -> POST /notification-settings
- "Get notification-setting details?" -> GET /notification-settings/{notification_setting_id}
- "Partially update a notification-setting?" -> PATCH /notification-settings/{notification_setting_id}
- "Delete a notification-setting?" -> DELETE /notification-settings/{notification_setting_id}
- "Search notifications?" -> GET /notifications
- "Get notification details?" -> GET /notifications/{notification_id}
- "List all logs?" -> GET /notifications/{notification_id}/logs
- "Create a replay?" -> POST /notifications/{notification_id}/replay
- "List all payment-methods?" -> GET /customers/{customer_id}/payment-methods
- "Get payment-method details?" -> GET /customers/{customer_id}/payment-methods/{payment_method_id}
- "Delete a payment-method?" -> DELETE /customers/{customer_id}/payment-methods/{payment_method_id}
- "List all prices?" -> GET /prices
- "Create a price?" -> POST /prices
- "Get price details?" -> GET /prices/{price_id}
- "Partially update a price?" -> PATCH /prices/{price_id}
- "Create a pricing-preview?" -> POST /pricing-preview
- "List all products?" -> GET /products
- "Create a product?" -> POST /products
- "Get product details?" -> GET /products/{product_id}
- "Partially update a product?" -> PATCH /products/{product_id}
- "List all reports?" -> GET /reports
- "Create a report?" -> POST /reports
- "Get report details?" -> GET /reports/{report_id}
- "List all download-url?" -> GET /reports/{report_id}/download-url
- "List all simulation-types?" -> GET /simulation-types
- "List all simulations?" -> GET /simulations
- "Create a simulation?" -> POST /simulations
- "Get simulation details?" -> GET /simulations/{simulation_id}
- "Partially update a simulation?" -> PATCH /simulations/{simulation_id}
- "List all runs?" -> GET /simulations/{simulation_id}/runs
- "Create a run?" -> POST /simulations/{simulation_id}/runs
- "Get run details?" -> GET /simulations/{simulation_id}/runs/{simulation_run_id}
- "List all events?" -> GET /simulations/{simulation_id}/runs/{simulation_run_id}/events
- "Get event details?" -> GET /simulations/{simulation_id}/runs/{simulation_run_id}/events/{simulation_event_id}
- "Create a replay?" -> POST /simulations/{simulation_id}/runs/{simulation_run_id}/events/{simulation_event_id}/replay
- "List all subscriptions?" -> GET /subscriptions
- "Get subscription details?" -> GET /subscriptions/{subscription_id}
- "Partially update a subscription?" -> PATCH /subscriptions/{subscription_id}
- "Create a cancel?" -> POST /subscriptions/{subscription_id}/cancel
- "Create a pause?" -> POST /subscriptions/{subscription_id}/pause
- "Create a resume?" -> POST /subscriptions/{subscription_id}/resume
- "Create a activate?" -> POST /subscriptions/{subscription_id}/activate
- "List all update-payment-method-transaction?" -> GET /subscriptions/{subscription_id}/update-payment-method-transaction
- "Create a charge?" -> POST /subscriptions/{subscription_id}/charge
- "Create a preview?" -> POST /subscriptions/{subscription_id}/charge/preview
- "List all transactions?" -> GET /transactions
- "Create a transaction?" -> POST /transactions
- "Get transaction details?" -> GET /transactions/{transaction_id}
- "Partially update a transaction?" -> PATCH /transactions/{transaction_id}
- "Create a preview?" -> POST /transactions/preview
- "Create a revise?" -> POST /transactions/{transaction_id}/revise
- "List all invoice?" -> GET /transactions/{transaction_id}/invoice
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
