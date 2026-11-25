---
name: brainbi
description: "brainbi API skill. Use when working with brainbi for {{server}}. Covers 33 endpoints."
version: 1.0.0
generator: lapsh
---

# brainbi

## Auth
ApiKey Authorization in header

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /{{server}}/api/rule -- verify access
3. POST /{{server}}/api/rule -- create first rule

## Endpoints

33 endpoints across 1 groups. See references/api-spec.lap for full details.

### {{server}}
| Method | Path | Description |
|--------|------|-------------|
| GET | /{{server}}/api/rule | Rules |
| GET | /{{server}}/api/rule/1 | Rule {id} |
| POST | /{{server}}/api/rule | Rule |
| GET | /{{server}}/api/rule/ruleData/1 | Rule Data |
| GET | /{{server}}/api/rule/ruleData/1/latest | Rule Data Latest |
| GET | /{{server}}/api/products | Products |
| GET | /{{server}}/api/products/1 | Products {id} |
| GET | /{{server}}/api/products/23767/rules | Products {id} Get Rules |
| POST | /{{server}}/api/products | Products |
| GET | /{{server}}/api/analyze/pricing | [BETA] Scrape Product |
| GET | /{{server}}/api/analyze/pricing | [BETA] Scrape Product Copy |
| PUT | /{{server}}/api/products | Products |
| DELETE | /{{server}}/api/products/1137 | Products |
| GET | /{{server}}/api/customers | Customers |
| GET | /{{server}}/api/customers/1 | Customers {id} |
| POST | /{{server}}/api/customers | Customers |
| PUT | /{{server}}/api/customers/1137 | Customers |
| DELETE | /{{server}}/api/customers/1137 | Customers |
| GET | /{{server}}/api/orders | Orders |
| GET | /{{server}}/api/orders/12 | Orders {id} |
| POST | /{{server}}/api/orders | Orders |
| PUT | /{{server}}/api/orders/1137 | Orders |
| DELETE | /{{server}}/api/orders/1137 | Orders |
| GET | /{{server}}/api/orderlines | OrderLines |
| GET | /{{server}}/api/orderlines/123 | OrderLines {id} |
| POST | /{{server}}/api/orderlines | OrderLine |
| PUT | /{{server}}/api/orderlines/1137 | OrderLines |
| DELETE | /{{server}}/api/orderlines/1137 | OrderLines |
| GET | /{{server}}/api/seo/ranking/latest | SEO Latest Rankings |
| POST | /{{server}}/api/login | Login and get bearer token |
| POST | /{{server}}/api/register | Register |
| POST | /{{server}}/api/register_woocommerce | Register and Create Store Connection for WooCommerce |
| POST | /{{server}}/api/logout | Logout |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all rule?" -> GET /{{server}}/api/rule
- "List all 1?" -> GET /{{server}}/api/rule/1
- "Create a rule?" -> POST /{{server}}/api/rule
- "List all 1?" -> GET /{{server}}/api/rule/ruleData/1
- "List all latest?" -> GET /{{server}}/api/rule/ruleData/1/latest
- "List all products?" -> GET /{{server}}/api/products
- "List all 1?" -> GET /{{server}}/api/products/1
- "List all rules?" -> GET /{{server}}/api/products/23767/rules
- "Create a product?" -> POST /{{server}}/api/products
- "List all pricing?" -> GET /{{server}}/api/analyze/pricing
- "List all customers?" -> GET /{{server}}/api/customers
- "List all 1?" -> GET /{{server}}/api/customers/1
- "Create a customer?" -> POST /{{server}}/api/customers
- "List all orders?" -> GET /{{server}}/api/orders
- "List all 12?" -> GET /{{server}}/api/orders/12
- "Create a order?" -> POST /{{server}}/api/orders
- "List all orderlines?" -> GET /{{server}}/api/orderlines
- "List all 123?" -> GET /{{server}}/api/orderlines/123
- "Create a orderline?" -> POST /{{server}}/api/orderlines
- "List all latest?" -> GET /{{server}}/api/seo/ranking/latest
- "Create a login?" -> POST /{{server}}/api/login
- "Create a register?" -> POST /{{server}}/api/register
- "Create a register_woocommerce?" -> POST /{{server}}/api/register_woocommerce
- "Create a logout?" -> POST /{{server}}/api/logout
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
