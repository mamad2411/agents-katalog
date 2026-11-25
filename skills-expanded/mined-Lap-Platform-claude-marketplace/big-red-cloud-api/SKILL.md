---
name: big-red-cloud-api
description: "Big Red Cloud API skill. Use when working with Big Red Cloud for accounts, analysisCategories, bankAccounts. Covers 120 endpoints."
version: 1.0.0
generator: lapsh
---

# Big Red Cloud API
API version: v1

## Auth
ApiKey (inferred from docs)

## Base URL
https://app.bigredcloud.com/api

## Setup
1. Set your API key in the appropriate header
2. GET /v1/accounts -- verify access
3. POST /v1/bankAccounts -- create first bankAccounts

## Endpoints

120 endpoints across 30 groups. See references/api-spec.lap for full details.

### accounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/accounts | Returns a list of company's Accounts. Supports OData querying protocol. |

### analysisCategories
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/analysisCategories | Returns a list of company's Analysis Categories. Supports OData querying protocol. |

### bankAccounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/bankAccounts | Returns a list of company's Bank Account. Supports OData querying protocol. |
| POST | /v1/bankAccounts | Creates a new Bank Account. |
| GET | /v1/bankAccounts/{id} | Returns information about a single Bank Account. |
| PUT | /v1/bankAccounts/{id} | Updates an existing Bank Account. |
| DELETE | /v1/bankAccounts/{id} | Removes an existing Bank Account. |
| PUT | /v1/bankAccounts/batch | Processes a batch of Bank Accounts. |

### bookTranTypes
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/bookTranTypes | Returns a list of global Book Transactions' Types. Supports OData querying protocol. |

### cashPayments
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/cashPayments | Returns a list of company's Cash Payments. Supports OData querying protocol. |
| POST | /v1/cashPayments | Creates a new Cash Payment. |
| GET | /v1/cashPayments/{id} | Returns information about a single Cash Payment. |
| PUT | /v1/cashPayments/{id} | Updates an existing Cash Payment. |
| DELETE | /v1/cashPayments/{id} | Removes an existing Cash Payment. |
| PUT | /v1/cashPayments/batch | Processes a batch of Cash Payments. |

### cashReceipts
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/cashReceipts | Returns a list of company's Cash Receipts. Supports OData querying protocol. |
| POST | /v1/cashReceipts | Creates a new Cash Receipt. |
| GET | /v1/cashReceipts/{id} | Returns information about a single Cash Receipt. |
| PUT | /v1/cashReceipts/{id} | Updates an existing Cash Receipt. |
| DELETE | /v1/cashReceipts/{id} | Removes an existing Cash Receipt. |
| PUT | /v1/cashReceipts/batch | Processes a batch of Cash Receipts. |

### categoryTypes
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/categoryTypes | Returns a list of company's Category Types. Supports OData querying protocol. |

### companySettings
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/companySettings | Returns a list of company settings. Supports OData querying protocol. |

### companySetupConfig
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/companySetupConfig | Returns the company configuration settings. |
| GET | /v1/companySetupConfig/getFinancialYear | Returns the financial year. |
| GET | /v1/companySetupConfig/getCompanyOptions | Returns the company option setting. |
| GET | /v1/companySetupConfig/getCompanyLogo | Returns the company logo. |

### customers
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/customers | Returns a list of company's Customers. Supports OData querying protocol. |
| POST | /v1/customers | Creates a new Customer. |
| GET | /v1/customers/{id} | Returns information about a single Customer. You may specify that Customer's ledger balance should be calculated. |
| PUT | /v1/customers/{id} | Updates an existing Customer. |
| DELETE | /v1/customers/{id} | Removes an existing Customer. |
| GET | /v1/customers/GetWithoutDormant | Returns a list of company's Customers without dormant records. Supports OData querying protocol. |
| PUT | /v1/customers/batch | Processes a batch of Customers. |
| GET | /v1/customers/{itemId}/openingBalance | Returns a Customer's opening balances, calculated for the next periods: current month, one month old, two months old, three and more months old. |
| GET | /v1/customers/{itemId}/openingBalanceList | Returns a list of Customer's opening balance transactions. |
| GET | /v1/customers/{itemId}/accountTrans | Returns a list of Customer's account transactions. |
| GET | /v1/customers/{itemId}/quotes | Returns a list of Customer's quotes. |

### email
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/email/sendSalesInvoice | Sends a Sales Invoice email. |
| POST | /v1/email/sendEmailStatement | Sends a Statement email. |
| POST | /v1/email/sendQuote | Sends a Quote email. |

### nominalAccounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/nominalAccounts | Returns a list of company's Nominal Accounts. Supports OData querying protocol. |
| GET | /v1/nominalAccounts/{id} | Returns information about a single Nominal Account. |
| GET | /v1/nominalAccounts/ledger | Returns information about Nominal Ledger from all Nominal accounts. |
| GET | /v1/nominalAccounts/ledger/{ids} | Returns information about Nominal Ledger from specific Nominal Accounts. |

### ownerTypeGroups
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/ownerTypeGroups | Returns a list of global Owner Type Groups. Supports OData querying protocol. |

### ownerTypes
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/ownerTypes | Returns a list of global Owner Types. Supports OData querying protocol. |

### payments
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/payments | Returns a list of company's Payments. Supports OData querying protocol. |
| POST | /v1/payments | Creates a new Payment. |
| GET | /v1/payments/{id} | Returns information about a single Payments. |
| PUT | /v1/payments/{id} | Updates an existing Payment. |
| DELETE | /v1/payments/{id} | Removes an existing Payment. |
| PUT | /v1/payments/batch | Processes a batch of Payments. |

### products
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/products | Returns a list of company's Products. Supports OData querying protocol. |
| POST | /v1/products | Creates a new Product. |
| GET | /v1/products/{id} | Returns information about a single Product. |
| PUT | /v1/products/{id} | Updates an existing Product. |
| DELETE | /v1/products/{id} | Removes an existing Product. |
| GET | /v1/products/GetWithoutDormant | Returns a list of company's Products without dormant records. Supports OData querying protocol. |
| PUT | /v1/products/batch | Processes a batch of Products. |

### productTypes
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/productTypes | Returns a list of global Product Types. Supports OData querying protocol. |

### purchases
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/purchases | Returns a list of company's Purchases. Supports OData querying protocol. |
| POST | /v1/purchases | Creates a new Purchase. |
| GET | /v1/purchases/{id} | Returns information about a single Purchases. |
| PUT | /v1/purchases/{id} | Updates an existing Purchase. |
| DELETE | /v1/purchases/{id} | Removes an existing Purchase. |
| PUT | /v1/purchases/batch | Processes a batch of Purchases. |
| POST | /v1/purchases/createPurchaseWithGeneratingReference | Creates a new Purchase with auto generating reference. |

### quotes
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/quotes | Returns a list of company's Quotes. |
| POST | /v1/quotes | Creates a new Quote. |
| GET | /v1/quotes/{id} | Returns information about a single Quote. |
| PUT | /v1/quotes/{id} | Updates an existing Quote. |
| DELETE | /v1/quotes/{id} | Removes an existing Quote. |
| PUT | /v1/quotes/batch | Processes a batch of Quote. |
| PUT | /v1/quotes/close/{id} | Close a Quote. |
| PUT | /v1/quotes/reopen/{id} | Reopen a Quote. |
| POST | /v1/quotes/generateSaleInvoice | Generate a sale invoice from a Quote. |
| POST | /v1/quotes/createQuoteWithGeneratingReference | Creates a new Quote with auto generating reference. |

### sales
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/sales | Returns a list of company's Sales Entries, Sales Invoices and Sales Credit Notes. Supports OData querying protocol. |

### salesCreditNotes
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/salesCreditNotes | Returns a list of company's Sales Credit Notes. Supports OData querying protocol. |
| POST | /v1/salesCreditNotes | Creates a new Sales Credit Note. |
| GET | /v1/salesCreditNotes/{id} | Returns information about a single Sales Credit Note. |
| PUT | /v1/salesCreditNotes/{id} | Updates an existing Sales Credit Note. |
| DELETE | /v1/salesCreditNotes/{id} | Removes an existing Sales Credit Note. |
| PUT | /v1/salesCreditNotes/batch | Processes a batch of Sales Credit Notes. |
| POST | /v1/salesCreditNotes/createCreditNoteWithGeneratingReference | Creates a new Sale Credit Note with auto generating reference. |

### salesEntries
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/salesEntries | Returns a list of company's Sales Entries. Supports OData querying protocol. |
| POST | /v1/salesEntries | Creates a new Sales Entry. |
| GET | /v1/salesEntries/{id} | Returns information about a single Sales Entry. |
| PUT | /v1/salesEntries/{id} | Updates an existing Sales Entry. |
| DELETE | /v1/salesEntries/{id} | Removes an existing Sales Entry. |
| PUT | /v1/salesEntries/batch | Processes a batch of Sales Entries. |

### salesInvoices
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/salesInvoices | Returns a list of company's Sales Invoices. Supports OData querying protocol. |
| POST | /v1/salesInvoices | Creates a new Sales Invoice. |
| GET | /v1/salesInvoices/{id} | Returns information about a single Sales Invoice. |
| PUT | /v1/salesInvoices/{id} | Updates an existing Sales Invoice. |
| DELETE | /v1/salesInvoices/{id} | Removes an existing Sales Invoice. |
| PUT | /v1/salesInvoices/batch | Processes a batch of Sales Invoices. |
| POST | /v1/salesInvoices/createSaleInvoiceWithGeneratingReference | Creates a new Sale Invoice with auto generating reference. |

### salesReps
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/salesReps | Returns a list of company's SaleRep. |
| POST | /v1/salesReps | Creates a new SaleRep. |
| GET | /v1/salesReps/{id} | Returns information about a single SaleRep. |
| PUT | /v1/salesReps/{id} | Updates an existing Sale Rep. |
| DELETE | /v1/salesReps/{id} | Removes an existing Sale Rep. |
| PUT | /v1/salesReps/batch | Processes a batch of Sale Rep. |

### suppliers
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/suppliers | Returns a list of company's Suppliers. Supports OData querying protocol. |
| POST | /v1/suppliers | Creates a new Supplier. |
| GET | /v1/suppliers/{id} | Returns information about a single Supplier. You may specify that Supplier's ledger balance should be calculated. |
| PUT | /v1/suppliers/{id} | Updates an existing Supplier. |
| DELETE | /v1/suppliers/{id} | Removes an existing Supplier. |
| PUT | /v1/suppliers/batch | Processes a batch of Suppliers. |
| GET | /v1/suppliers/{itemId}/openingBalance | Returns a Supplier's opening balances, calculated for the next periods: current month, one month old, two months old, three and more months old. |
| GET | /v1/suppliers/{itemId}/openingBalanceList | Returns a list of Supplier's opening balance transactions. |
| GET | /v1/suppliers/{itemId}/accountTrans | Returns a list of Supplier's account transactions. |

### userDefinedFields
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/userDefinedFields | Returns a list of company's User Defined Fields. Supports OData querying protocol. |

### vatAnalysisTypes
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/vatAnalysisTypes | Returns a list of global Vat Analysis Types. Supports OData querying protocol. |

### vatCategories
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/vatCategories | Returns a list of global Vat Categories. Supports OData querying protocol. |
| POST | /v1/vatCategories/vatRates | Process Vat Rates |

### vatRates
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/vatRates | Returns a list of company's Vat Rates. Supports OData querying protocol. |

### vatTypes
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/vatTypes | Returns a list of global Vat Types. Supports OData querying protocol. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all accounts?" -> GET /v1/accounts
- "List all analysisCategories?" -> GET /v1/analysisCategories
- "List all bankAccounts?" -> GET /v1/bankAccounts
- "Create a bankAccount?" -> POST /v1/bankAccounts
- "Get bankAccount details?" -> GET /v1/bankAccounts/{id}
- "Update a bankAccount?" -> PUT /v1/bankAccounts/{id}
- "Delete a bankAccount?" -> DELETE /v1/bankAccounts/{id}
- "List all bookTranTypes?" -> GET /v1/bookTranTypes
- "List all cashPayments?" -> GET /v1/cashPayments
- "Create a cashPayment?" -> POST /v1/cashPayments
- "Get cashPayment details?" -> GET /v1/cashPayments/{id}
- "Update a cashPayment?" -> PUT /v1/cashPayments/{id}
- "Delete a cashPayment?" -> DELETE /v1/cashPayments/{id}
- "List all cashReceipts?" -> GET /v1/cashReceipts
- "Create a cashReceipt?" -> POST /v1/cashReceipts
- "Get cashReceipt details?" -> GET /v1/cashReceipts/{id}
- "Update a cashReceipt?" -> PUT /v1/cashReceipts/{id}
- "Delete a cashReceipt?" -> DELETE /v1/cashReceipts/{id}
- "List all categoryTypes?" -> GET /v1/categoryTypes
- "List all companySettings?" -> GET /v1/companySettings
- "List all companySetupConfig?" -> GET /v1/companySetupConfig
- "List all getFinancialYear?" -> GET /v1/companySetupConfig/getFinancialYear
- "List all getCompanyOptions?" -> GET /v1/companySetupConfig/getCompanyOptions
- "List all getCompanyLogo?" -> GET /v1/companySetupConfig/getCompanyLogo
- "List all customers?" -> GET /v1/customers
- "Create a customer?" -> POST /v1/customers
- "Get customer details?" -> GET /v1/customers/{id}
- "Update a customer?" -> PUT /v1/customers/{id}
- "Delete a customer?" -> DELETE /v1/customers/{id}
- "List all GetWithoutDormant?" -> GET /v1/customers/GetWithoutDormant
- "List all openingBalance?" -> GET /v1/customers/{itemId}/openingBalance
- "List all openingBalanceList?" -> GET /v1/customers/{itemId}/openingBalanceList
- "List all accountTrans?" -> GET /v1/customers/{itemId}/accountTrans
- "List all quotes?" -> GET /v1/customers/{itemId}/quotes
- "Create a sendSalesInvoice?" -> POST /v1/email/sendSalesInvoice
- "Create a sendEmailStatement?" -> POST /v1/email/sendEmailStatement
- "Create a sendQuote?" -> POST /v1/email/sendQuote
- "List all nominalAccounts?" -> GET /v1/nominalAccounts
- "Get nominalAccount details?" -> GET /v1/nominalAccounts/{id}
- "List all ledger?" -> GET /v1/nominalAccounts/ledger
- "Get ledger details?" -> GET /v1/nominalAccounts/ledger/{ids}
- "List all ownerTypeGroups?" -> GET /v1/ownerTypeGroups
- "List all ownerTypes?" -> GET /v1/ownerTypes
- "List all payments?" -> GET /v1/payments
- "Create a payment?" -> POST /v1/payments
- "Get payment details?" -> GET /v1/payments/{id}
- "Update a payment?" -> PUT /v1/payments/{id}
- "Delete a payment?" -> DELETE /v1/payments/{id}
- "List all products?" -> GET /v1/products
- "Create a product?" -> POST /v1/products
- "Get product details?" -> GET /v1/products/{id}
- "Update a product?" -> PUT /v1/products/{id}
- "Delete a product?" -> DELETE /v1/products/{id}
- "List all GetWithoutDormant?" -> GET /v1/products/GetWithoutDormant
- "List all productTypes?" -> GET /v1/productTypes
- "List all purchases?" -> GET /v1/purchases
- "Create a purchase?" -> POST /v1/purchases
- "Get purchase details?" -> GET /v1/purchases/{id}
- "Update a purchase?" -> PUT /v1/purchases/{id}
- "Delete a purchase?" -> DELETE /v1/purchases/{id}
- "Create a createPurchaseWithGeneratingReference?" -> POST /v1/purchases/createPurchaseWithGeneratingReference
- "List all quotes?" -> GET /v1/quotes
- "Create a quote?" -> POST /v1/quotes
- "Get quote details?" -> GET /v1/quotes/{id}
- "Update a quote?" -> PUT /v1/quotes/{id}
- "Delete a quote?" -> DELETE /v1/quotes/{id}
- "Update a close?" -> PUT /v1/quotes/close/{id}
- "Update a reopen?" -> PUT /v1/quotes/reopen/{id}
- "Create a generateSaleInvoice?" -> POST /v1/quotes/generateSaleInvoice
- "Create a createQuoteWithGeneratingReference?" -> POST /v1/quotes/createQuoteWithGeneratingReference
- "List all sales?" -> GET /v1/sales
- "List all salesCreditNotes?" -> GET /v1/salesCreditNotes
- "Create a salesCreditNote?" -> POST /v1/salesCreditNotes
- "Get salesCreditNote details?" -> GET /v1/salesCreditNotes/{id}
- "Update a salesCreditNote?" -> PUT /v1/salesCreditNotes/{id}
- "Delete a salesCreditNote?" -> DELETE /v1/salesCreditNotes/{id}
- "Create a createCreditNoteWithGeneratingReference?" -> POST /v1/salesCreditNotes/createCreditNoteWithGeneratingReference
- "List all salesEntries?" -> GET /v1/salesEntries
- "Create a salesEntry?" -> POST /v1/salesEntries
- "Get salesEntry details?" -> GET /v1/salesEntries/{id}
- "Update a salesEntry?" -> PUT /v1/salesEntries/{id}
- "Delete a salesEntry?" -> DELETE /v1/salesEntries/{id}
- "List all salesInvoices?" -> GET /v1/salesInvoices
- "Create a salesInvoice?" -> POST /v1/salesInvoices
- "Get salesInvoice details?" -> GET /v1/salesInvoices/{id}
- "Update a salesInvoice?" -> PUT /v1/salesInvoices/{id}
- "Delete a salesInvoice?" -> DELETE /v1/salesInvoices/{id}
- "Create a createSaleInvoiceWithGeneratingReference?" -> POST /v1/salesInvoices/createSaleInvoiceWithGeneratingReference
- "List all salesReps?" -> GET /v1/salesReps
- "Create a salesRep?" -> POST /v1/salesReps
- "Get salesRep details?" -> GET /v1/salesReps/{id}
- "Update a salesRep?" -> PUT /v1/salesReps/{id}
- "Delete a salesRep?" -> DELETE /v1/salesReps/{id}
- "List all suppliers?" -> GET /v1/suppliers
- "Create a supplier?" -> POST /v1/suppliers
- "Get supplier details?" -> GET /v1/suppliers/{id}
- "Update a supplier?" -> PUT /v1/suppliers/{id}
- "Delete a supplier?" -> DELETE /v1/suppliers/{id}
- "List all openingBalance?" -> GET /v1/suppliers/{itemId}/openingBalance
- "List all openingBalanceList?" -> GET /v1/suppliers/{itemId}/openingBalanceList
- "List all accountTrans?" -> GET /v1/suppliers/{itemId}/accountTrans
- "List all userDefinedFields?" -> GET /v1/userDefinedFields
- "List all vatAnalysisTypes?" -> GET /v1/vatAnalysisTypes
- "List all vatCategories?" -> GET /v1/vatCategories
- "Create a vatRate?" -> POST /v1/vatCategories/vatRates
- "List all vatRates?" -> GET /v1/vatRates
- "List all vatTypes?" -> GET /v1/vatTypes
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
