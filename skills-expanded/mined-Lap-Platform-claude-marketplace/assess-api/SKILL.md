---
name: assess-api
description: "Assess API skill. Use when working with Assess for data, companies. Covers 20 endpoints."
version: 1.0.0
generator: lapsh
---

# Assess API
API version: 1.0

## Auth
ApiKey Authorization in header

## Base URL
https://api.codat.io

## Setup
1. Set your API key in the appropriate header
2. GET /data/companies/{companyId}/assess/dataTypes/{dataType}/dataIntegrity/status -- verify access
3. POST /data/companies/{companyId}/assess/excel -- create first excel

## Endpoints

20 endpoints across 2 groups. See references/api-spec.lap for full details.

### data
| Method | Path | Description |
|--------|------|-------------|
| GET | /data/companies/{companyId}/assess/dataTypes/{dataType}/dataIntegrity/status | Get data integrity status |
| GET | /data/companies/{companyId}/assess/dataTypes/{dataType}/dataIntegrity/summaries | Get data integrity summary |
| GET | /data/companies/{companyId}/assess/dataTypes/{dataType}/dataIntegrity/details | List data type data integrity |
| GET | /data/companies/{companyId}/connections/{connectionId}/assess/commerceMetrics/revenue | Get commerce revenue metrics |
| GET | /data/companies/{companyId}/connections/{connectionId}/assess/commerceMetrics/orders | Get orders report |
| GET | /data/companies/{companyId}/connections/{connectionId}/assess/commerceMetrics/refunds | Get refunds report |
| GET | /data/companies/{companyId}/connections/{connectionId}/assess/commerceMetrics/customerRetention | Get customer retention metrics |
| GET | /data/companies/{companyId}/connections/{connectionId}/assess/commerceMetrics/lifetimeValue | Get lifetime value metric |
| GET | /data/companies/{companyId}/connections/{connectionId}/assess/accountingMetrics/marketing | Get marketing metrics report |
| POST | /data/companies/{companyId}/assess/excel | Generate Excel report |
| GET | /data/companies/{companyId}/assess/excel | Get Excel report status |
| GET | /data/companies/{companyId}/assess/excel/download | Download Excel report |

### companies
| Method | Path | Description |
|--------|------|-------------|
| GET | /companies/{companyId}/reports/enhancedProfitAndLoss/accounts | Get enhanced profit and loss accounts |
| GET | /companies/{companyId}/reports/enhancedBalanceSheet/accounts | Get enhanced balance sheet accounts |
| GET | /companies/{companyId}/reports/enhancedCashFlow/transactions | Get enhanced cash flow report |
| GET | /companies/{companyId}/reports/enhancedInvoices | Get enhanced invoices report |
| POST | /companies/{companyId}/reports/liabilities/loans/transactions | Generate loan transactions report |
| GET | /companies/{companyId}/reports/liabilities/loans/transactions | List loan transactions |
| POST | /companies/{companyId}/reports/liabilities/loans | Generate loan summaries report |
| GET | /companies/{companyId}/reports/liabilities/loans | Get loan summaries |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all status?" -> GET /data/companies/{companyId}/assess/dataTypes/{dataType}/dataIntegrity/status
- "Search summaries?" -> GET /data/companies/{companyId}/assess/dataTypes/{dataType}/dataIntegrity/summaries
- "Search details?" -> GET /data/companies/{companyId}/assess/dataTypes/{dataType}/dataIntegrity/details
- "List all accounts?" -> GET /companies/{companyId}/reports/enhancedProfitAndLoss/accounts
- "List all accounts?" -> GET /companies/{companyId}/reports/enhancedBalanceSheet/accounts
- "Search transactions?" -> GET /companies/{companyId}/reports/enhancedCashFlow/transactions
- "Search enhancedInvoices?" -> GET /companies/{companyId}/reports/enhancedInvoices
- "List all revenue?" -> GET /data/companies/{companyId}/connections/{connectionId}/assess/commerceMetrics/revenue
- "List all orders?" -> GET /data/companies/{companyId}/connections/{connectionId}/assess/commerceMetrics/orders
- "List all refunds?" -> GET /data/companies/{companyId}/connections/{connectionId}/assess/commerceMetrics/refunds
- "List all customerRetention?" -> GET /data/companies/{companyId}/connections/{connectionId}/assess/commerceMetrics/customerRetention
- "List all lifetimeValue?" -> GET /data/companies/{companyId}/connections/{connectionId}/assess/commerceMetrics/lifetimeValue
- "List all marketing?" -> GET /data/companies/{companyId}/connections/{connectionId}/assess/accountingMetrics/marketing
- "Create a excel?" -> POST /data/companies/{companyId}/assess/excel
- "List all excel?" -> GET /data/companies/{companyId}/assess/excel
- "List all download?" -> GET /data/companies/{companyId}/assess/excel/download
- "Create a transaction?" -> POST /companies/{companyId}/reports/liabilities/loans/transactions
- "List all transactions?" -> GET /companies/{companyId}/reports/liabilities/loans/transactions
- "Create a loan?" -> POST /companies/{companyId}/reports/liabilities/loans
- "List all loans?" -> GET /companies/{companyId}/reports/liabilities/loans
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
