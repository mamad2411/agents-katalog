---
name: xero-accounting-api
description: "Xero Accounting API skill. Use when working with Xero Accounting for Accounts, BatchPayments, BankTransactions. Covers 237 endpoints."
version: 1.0.0
generator: lapsh
---

# Xero Accounting API
API version: 11.1.0

## Auth
OAuth2

## Base URL
https://api.xero.com/api.xro/2.0

## Setup
1. Configure auth: OAuth2
2. GET /Accounts -- verify access
3. POST /Accounts/{AccountID} -- create first Accounts

## Endpoints

237 endpoints across 32 groups. See references/api-spec.lap for full details.

### Accounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /Accounts | Retrieves the full chart of accounts |
| PUT | /Accounts | Creates a new chart of accounts |
| GET | /Accounts/{AccountID} | Retrieves a single chart of accounts by using a unique account Id |
| POST | /Accounts/{AccountID} | Updates a chart of accounts |
| DELETE | /Accounts/{AccountID} | Deletes a chart of accounts |
| GET | /Accounts/{AccountID}/Attachments | Retrieves attachments for a specific accounts by using a unique account Id |
| GET | /Accounts/{AccountID}/Attachments/{AttachmentID} | Retrieves a specific attachment from a specific account using a unique attachment Id |
| GET | /Accounts/{AccountID}/Attachments/{FileName} | Retrieves an attachment for a specific account by filename |
| POST | /Accounts/{AccountID}/Attachments/{FileName} | Updates attachment on a specific account by filename |
| PUT | /Accounts/{AccountID}/Attachments/{FileName} | Creates an attachment on a specific account |

### BatchPayments
| Method | Path | Description |
|--------|------|-------------|
| GET | /BatchPayments | Retrieves either one or many batch payments for invoices |
| PUT | /BatchPayments | Creates one or many batch payments for invoices |
| POST | /BatchPayments | Updates a specific batch payment for invoices and credit notes |
| GET | /BatchPayments/{BatchPaymentID} | Retrieves a specific batch payment using a unique batch payment Id |
| POST | /BatchPayments/{BatchPaymentID} | Updates a specific batch payment for invoices and credit notes |
| GET | /BatchPayments/{BatchPaymentID}/History | Retrieves history from a specific batch payment |
| PUT | /BatchPayments/{BatchPaymentID}/History | Creates a history record for a specific batch payment |

### BankTransactions
| Method | Path | Description |
|--------|------|-------------|
| GET | /BankTransactions | Retrieves any spent or received money transactions |
| PUT | /BankTransactions | Creates one or more spent or received money transaction |
| POST | /BankTransactions | Updates or creates one or more spent or received money transaction |
| GET | /BankTransactions/{BankTransactionID} | Retrieves a single spent or received money transaction by using a unique bank transaction Id |
| POST | /BankTransactions/{BankTransactionID} | Updates a single spent or received money transaction |
| GET | /BankTransactions/{BankTransactionID}/Attachments | Retrieves any attachments from a specific bank transactions |
| GET | /BankTransactions/{BankTransactionID}/Attachments/{AttachmentID} | Retrieves specific attachments from a specific BankTransaction using a unique attachment Id |
| GET | /BankTransactions/{BankTransactionID}/Attachments/{FileName} | Retrieves a specific attachment from a specific bank transaction by filename |
| POST | /BankTransactions/{BankTransactionID}/Attachments/{FileName} | Updates a specific attachment from a specific bank transaction by filename |
| PUT | /BankTransactions/{BankTransactionID}/Attachments/{FileName} | Creates an attachment for a specific bank transaction by filename |
| GET | /BankTransactions/{BankTransactionID}/History | Retrieves history from a specific bank transaction using a unique bank transaction Id |
| PUT | /BankTransactions/{BankTransactionID}/History | Creates a history record for a specific bank transactions |

### BankTransfers
| Method | Path | Description |
|--------|------|-------------|
| GET | /BankTransfers | Retrieves all bank transfers |
| PUT | /BankTransfers | Creates a bank transfer |
| GET | /BankTransfers/{BankTransferID} | Retrieves specific bank transfers by using a unique bank transfer Id |
| GET | /BankTransfers/{BankTransferID}/Attachments | Retrieves attachments from a specific bank transfer |
| GET | /BankTransfers/{BankTransferID}/Attachments/{AttachmentID} | Retrieves a specific attachment from a specific bank transfer using a unique attachment ID |
| GET | /BankTransfers/{BankTransferID}/Attachments/{FileName} | Retrieves a specific attachment on a specific bank transfer by file name |
| POST | /BankTransfers/{BankTransferID}/Attachments/{FileName} |  |
| PUT | /BankTransfers/{BankTransferID}/Attachments/{FileName} |  |
| GET | /BankTransfers/{BankTransferID}/History | Retrieves history from a specific bank transfer using a unique bank transfer Id |
| PUT | /BankTransfers/{BankTransferID}/History | Creates a history record for a specific bank transfer |

### BrandingThemes
| Method | Path | Description |
|--------|------|-------------|
| GET | /BrandingThemes | Retrieves all the branding themes |
| GET | /BrandingThemes/{BrandingThemeID} | Retrieves a specific branding theme using a unique branding theme Id |
| GET | /BrandingThemes/{BrandingThemeID}/PaymentServices | Retrieves the payment services for a specific branding theme |
| POST | /BrandingThemes/{BrandingThemeID}/PaymentServices | Creates a new custom payment service for a specific branding theme |

### Budgets
| Method | Path | Description |
|--------|------|-------------|
| GET | /Budgets | Retrieve a list of budgets |
| GET | /Budgets/{BudgetID} | Retrieves a specific budget, which includes budget lines |

### Contacts
| Method | Path | Description |
|--------|------|-------------|
| GET | /Contacts | Retrieves all contacts in a Xero organisation |
| PUT | /Contacts | Creates multiple contacts (bulk) in a Xero organisation |
| POST | /Contacts | Updates or creates one or more contacts in a Xero organisation |
| GET | /Contacts/{ContactNumber} | Retrieves a specific contact by contact number in a Xero organisation |
| GET | /Contacts/{ContactID} | Retrieves a specific contacts in a Xero organisation using a unique contact Id |
| POST | /Contacts/{ContactID} | Updates a specific contact in a Xero organisation |
| GET | /Contacts/{ContactID}/Attachments | Retrieves attachments for a specific contact in a Xero organisation |
| GET | /Contacts/{ContactID}/Attachments/{AttachmentID} | Retrieves a specific attachment from a specific contact using a unique attachment Id |
| GET | /Contacts/{ContactID}/Attachments/{FileName} | Retrieves a specific attachment from a specific contact by file name |
| POST | /Contacts/{ContactID}/Attachments/{FileName} |  |
| PUT | /Contacts/{ContactID}/Attachments/{FileName} |  |
| GET | /Contacts/{ContactID}/CISSettings | Retrieves CIS settings for a specific contact in a Xero organisation |
| GET | /Contacts/{ContactID}/History | Retrieves history records for a specific contact |
| PUT | /Contacts/{ContactID}/History | Creates a new history record for a specific contact |

### ContactGroups
| Method | Path | Description |
|--------|------|-------------|
| GET | /ContactGroups | Retrieves the contact Id and name of each contact group |
| PUT | /ContactGroups | Creates a contact group |
| GET | /ContactGroups/{ContactGroupID} | Retrieves a specific contact group by using a unique contact group Id |
| POST | /ContactGroups/{ContactGroupID} | Updates a specific contact group |
| PUT | /ContactGroups/{ContactGroupID}/Contacts | Creates contacts to a specific contact group |
| DELETE | /ContactGroups/{ContactGroupID}/Contacts | Deletes all contacts from a specific contact group |
| DELETE | /ContactGroups/{ContactGroupID}/Contacts/{ContactID} | Deletes a specific contact from a contact group using a unique contact Id |

### CreditNotes
| Method | Path | Description |
|--------|------|-------------|
| GET | /CreditNotes | Retrieves any credit notes |
| PUT | /CreditNotes | Creates a new credit note |
| POST | /CreditNotes | Updates or creates one or more credit notes |
| GET | /CreditNotes/{CreditNoteID} | Retrieves a specific credit note using a unique credit note Id |
| POST | /CreditNotes/{CreditNoteID} | Updates a specific credit note |
| GET | /CreditNotes/{CreditNoteID}/Attachments | Retrieves attachments for a specific credit notes |
| GET | /CreditNotes/{CreditNoteID}/Attachments/{AttachmentID} | Retrieves a specific attachment from a specific credit note using a unique attachment Id |
| GET | /CreditNotes/{CreditNoteID}/Attachments/{FileName} | Retrieves a specific attachment on a specific credit note by file name |
| POST | /CreditNotes/{CreditNoteID}/Attachments/{FileName} | Updates attachments on a specific credit note by file name |
| PUT | /CreditNotes/{CreditNoteID}/Attachments/{FileName} | Creates an attachment for a specific credit note |
| GET | /CreditNotes/{CreditNoteID}/pdf | Retrieves credit notes as PDF files |
| PUT | /CreditNotes/{CreditNoteID}/Allocations | Creates allocation for a specific credit note |
| DELETE | /CreditNotes/{CreditNoteID}/Allocations/{AllocationID} | Deletes an Allocation from a Credit Note |
| GET | /CreditNotes/{CreditNoteID}/History | Retrieves history records of a specific credit note |
| PUT | /CreditNotes/{CreditNoteID}/History | Retrieves history records of a specific credit note |

### Currencies
| Method | Path | Description |
|--------|------|-------------|
| GET | /Currencies | Retrieves currencies for your Xero organisation |
| PUT | /Currencies | Create a new currency for a Xero organisation |

### Employees
| Method | Path | Description |
|--------|------|-------------|
| GET | /Employees | Retrieves employees used in Xero payrun |
| PUT | /Employees | Creates new employees used in Xero payrun |
| POST | /Employees | Creates a single new employees used in Xero payrun |
| GET | /Employees/{EmployeeID} | Retrieves a specific employee used in Xero payrun using a unique employee Id |

### ExpenseClaims
| Method | Path | Description |
|--------|------|-------------|
| GET | /ExpenseClaims | Retrieves expense claims |
| PUT | /ExpenseClaims | Creates expense claims |
| GET | /ExpenseClaims/{ExpenseClaimID} | Retrieves a specific expense claim using a unique expense claim Id |
| POST | /ExpenseClaims/{ExpenseClaimID} | Updates a specific expense claims |
| GET | /ExpenseClaims/{ExpenseClaimID}/History | Retrieves history records of a specific expense claim |
| PUT | /ExpenseClaims/{ExpenseClaimID}/History | Creates a history record for a specific expense claim |

### Invoices
| Method | Path | Description |
|--------|------|-------------|
| GET | /Invoices | Retrieves sales invoices or purchase bills |
| PUT | /Invoices | Creates one or more sales invoices or purchase bills |
| POST | /Invoices | Updates or creates one or more sales invoices or purchase bills |
| GET | /Invoices/{InvoiceID} | Retrieves a specific sales invoice or purchase bill using a unique invoice Id |
| POST | /Invoices/{InvoiceID} | Updates a specific sales invoices or purchase bills |
| GET | /Invoices/{InvoiceID}/pdf | Retrieves invoices or purchase bills as PDF files |
| GET | /Invoices/{InvoiceID}/Attachments | Retrieves attachments for a specific invoice or purchase bill |
| GET | /Invoices/{InvoiceID}/Attachments/{AttachmentID} | Retrieves a specific attachment from a specific invoices or purchase bills by using a unique attachment Id |
| GET | /Invoices/{InvoiceID}/Attachments/{FileName} | Retrieves an attachment from a specific invoice or purchase bill by filename |
| POST | /Invoices/{InvoiceID}/Attachments/{FileName} | Updates an attachment from a specific invoices or purchase bill by filename |
| PUT | /Invoices/{InvoiceID}/Attachments/{FileName} | Creates an attachment for a specific invoice or purchase bill by filename |
| GET | /Invoices/{InvoiceID}/OnlineInvoice | Retrieves a URL to an online invoice |
| POST | /Invoices/{InvoiceID}/Email | Sends a copy of a specific invoice to related contact via email |
| GET | /Invoices/{InvoiceID}/History | Retrieves history records for a specific invoice |
| PUT | /Invoices/{InvoiceID}/History | Creates a history record for a specific invoice |

### InvoiceReminders
| Method | Path | Description |
|--------|------|-------------|
| GET | /InvoiceReminders/Settings | Retrieves invoice reminder settings |

### Items
| Method | Path | Description |
|--------|------|-------------|
| GET | /Items | Retrieves items |
| PUT | /Items | Creates one or more items |
| POST | /Items | Updates or creates one or more items |
| GET | /Items/{ItemID} | Retrieves a specific item using a unique item Id |
| POST | /Items/{ItemID} | Updates a specific item |
| DELETE | /Items/{ItemID} | Deletes a specific item |
| GET | /Items/{ItemID}/History | Retrieves history for a specific item |
| PUT | /Items/{ItemID}/History | Creates a history record for a specific item |

### Journals
| Method | Path | Description |
|--------|------|-------------|
| GET | /Journals | Retrieves journals |
| GET | /Journals/{JournalID} | Retrieves a specific journal using a unique journal Id. |
| GET | /Journals/{JournalNumber} | Retrieves a specific journal using a unique journal number. |

### LinkedTransactions
| Method | Path | Description |
|--------|------|-------------|
| GET | /LinkedTransactions | Retrieves linked transactions (billable expenses) |
| PUT | /LinkedTransactions | Creates linked transactions (billable expenses) |
| GET | /LinkedTransactions/{LinkedTransactionID} | Retrieves a specific linked transaction (billable expenses) using a unique linked transaction Id |
| POST | /LinkedTransactions/{LinkedTransactionID} | Updates a specific linked transactions (billable expenses) |
| DELETE | /LinkedTransactions/{LinkedTransactionID} | Deletes a specific linked transactions (billable expenses) |

### ManualJournals
| Method | Path | Description |
|--------|------|-------------|
| GET | /ManualJournals | Retrieves manual journals |
| PUT | /ManualJournals | Creates one or more manual journals |
| POST | /ManualJournals | Updates or creates a single manual journal |
| GET | /ManualJournals/{ManualJournalID} | Retrieves a specific manual journal |
| POST | /ManualJournals/{ManualJournalID} | Updates a specific manual journal |
| GET | /ManualJournals/{ManualJournalID}/Attachments | Retrieves attachment for a specific manual journal |
| GET | /ManualJournals/{ManualJournalID}/Attachments/{AttachmentID} | Allows you to retrieve a specific attachment from a specific manual journal using a unique attachment Id |
| GET | /ManualJournals/{ManualJournalID}/Attachments/{FileName} | Retrieves a specific attachment from a specific manual journal by file name |
| POST | /ManualJournals/{ManualJournalID}/Attachments/{FileName} | Updates a specific attachment from a specific manual journal by file name |
| PUT | /ManualJournals/{ManualJournalID}/Attachments/{FileName} | Creates a specific attachment for a specific manual journal by file name |
| GET | /ManualJournals/{ManualJournalID}/History | Retrieves history for a specific manual journal |
| PUT | /ManualJournals/{ManualJournalID}/History | Creates a history record for a specific manual journal |

### Organisation
| Method | Path | Description |
|--------|------|-------------|
| GET | /Organisation | Retrieves Xero organisation details |
| GET | /Organisation/Actions | Retrieves a list of the key actions your app has permission to perform in the connected Xero organisation. |
| GET | /Organisation/{OrganisationID}/CISSettings | Retrieves the CIS settings for the Xero organistaion. |

### Overpayments
| Method | Path | Description |
|--------|------|-------------|
| GET | /Overpayments | Retrieves overpayments |
| GET | /Overpayments/{OverpaymentID} | Retrieves a specific overpayment using a unique overpayment Id |
| PUT | /Overpayments/{OverpaymentID}/Allocations | Creates a single allocation for a specific overpayment |
| DELETE | /Overpayments/{OverpaymentID}/Allocations/{AllocationID} | Deletes an Allocation from an overpayment |
| GET | /Overpayments/{OverpaymentID}/History | Retrieves history records of a specific overpayment |
| PUT | /Overpayments/{OverpaymentID}/History | Creates a history record for a specific overpayment |

### Payments
| Method | Path | Description |
|--------|------|-------------|
| GET | /Payments | Retrieves payments for invoices and credit notes |
| PUT | /Payments | Creates multiple payments for invoices or credit notes |
| POST | /Payments | Creates a single payment for invoice or credit notes |
| GET | /Payments/{PaymentID} | Retrieves a specific payment for invoices and credit notes using a unique payment Id |
| POST | /Payments/{PaymentID} | Updates a specific payment for invoices and credit notes |
| GET | /Payments/{PaymentID}/History | Retrieves history records of a specific payment |
| PUT | /Payments/{PaymentID}/History | Creates a history record for a specific payment |

### PaymentServices
| Method | Path | Description |
|--------|------|-------------|
| GET | /PaymentServices | Retrieves payment services |
| PUT | /PaymentServices | Creates a payment service |

### Prepayments
| Method | Path | Description |
|--------|------|-------------|
| GET | /Prepayments | Retrieves prepayments |
| GET | /Prepayments/{PrepaymentID} | Allows you to retrieve a specified prepayments |
| PUT | /Prepayments/{PrepaymentID}/Allocations | Allows you to create an Allocation for prepayments |
| DELETE | /Prepayments/{PrepaymentID}/Allocations/{AllocationID} | Deletes an Allocation from a Prepayment |
| GET | /Prepayments/{PrepaymentID}/History | Retrieves history record for a specific prepayment |
| PUT | /Prepayments/{PrepaymentID}/History | Creates a history record for a specific prepayment |

### PurchaseOrders
| Method | Path | Description |
|--------|------|-------------|
| GET | /PurchaseOrders | Retrieves purchase orders |
| PUT | /PurchaseOrders | Creates one or more purchase orders |
| POST | /PurchaseOrders | Updates or creates one or more purchase orders |
| GET | /PurchaseOrders/{PurchaseOrderID}/pdf | Retrieves specific purchase order as PDF files using a unique purchase order Id |
| GET | /PurchaseOrders/{PurchaseOrderID} | Retrieves a specific purchase order using a unique purchase order Id |
| POST | /PurchaseOrders/{PurchaseOrderID} | Updates a specific purchase order |
| GET | /PurchaseOrders/{PurchaseOrderNumber} | Retrieves a specific purchase order using purchase order number |
| GET | /PurchaseOrders/{PurchaseOrderID}/History | Retrieves history for a specific purchase order |
| PUT | /PurchaseOrders/{PurchaseOrderID}/History | Creates a history record for a specific purchase orders |
| GET | /PurchaseOrders/{PurchaseOrderID}/Attachments | Retrieves attachments for a specific purchase order |
| GET | /PurchaseOrders/{PurchaseOrderID}/Attachments/{AttachmentID} | Retrieves specific attachment for a specific purchase order using a unique attachment Id |
| GET | /PurchaseOrders/{PurchaseOrderID}/Attachments/{FileName} | Retrieves a specific attachment for a specific purchase order by filename |
| POST | /PurchaseOrders/{PurchaseOrderID}/Attachments/{FileName} | Updates a specific attachment for a specific purchase order by filename |
| PUT | /PurchaseOrders/{PurchaseOrderID}/Attachments/{FileName} | Creates attachment for a specific purchase order |

### Quotes
| Method | Path | Description |
|--------|------|-------------|
| GET | /Quotes | Retrieves sales quotes |
| PUT | /Quotes | Create one or more quotes |
| POST | /Quotes | Updates or creates one or more quotes |
| GET | /Quotes/{QuoteID} | Retrieves a specific quote using a unique quote Id |
| POST | /Quotes/{QuoteID} | Updates a specific quote |
| GET | /Quotes/{QuoteID}/History | Retrieves history records of a specific quote |
| PUT | /Quotes/{QuoteID}/History | Creates a history record for a specific quote |
| GET | /Quotes/{QuoteID}/pdf | Retrieves a specific quote as a PDF file using a unique quote Id |
| GET | /Quotes/{QuoteID}/Attachments | Retrieves attachments for a specific quote |
| GET | /Quotes/{QuoteID}/Attachments/{AttachmentID} | Retrieves a specific attachment from a specific quote using a unique attachment Id |
| GET | /Quotes/{QuoteID}/Attachments/{FileName} | Retrieves a specific attachment from a specific quote by filename |
| POST | /Quotes/{QuoteID}/Attachments/{FileName} | Updates a specific attachment from a specific quote by filename |
| PUT | /Quotes/{QuoteID}/Attachments/{FileName} | Creates attachment for a specific quote |

### Receipts
| Method | Path | Description |
|--------|------|-------------|
| GET | /Receipts | Retrieves draft expense claim receipts for any user |
| PUT | /Receipts | Creates draft expense claim receipts for any user |
| GET | /Receipts/{ReceiptID} | Retrieves a specific draft expense claim receipt by using a unique receipt Id |
| POST | /Receipts/{ReceiptID} | Updates a specific draft expense claim receipts |
| GET | /Receipts/{ReceiptID}/Attachments | Retrieves attachments for a specific expense claim receipt |
| GET | /Receipts/{ReceiptID}/Attachments/{AttachmentID} | Retrieves a specific attachments from a specific expense claim receipts by using a unique attachment Id |
| GET | /Receipts/{ReceiptID}/Attachments/{FileName} | Retrieves a specific attachment from a specific expense claim receipts by file name |
| POST | /Receipts/{ReceiptID}/Attachments/{FileName} | Updates a specific attachment on a specific expense claim receipts by file name |
| PUT | /Receipts/{ReceiptID}/Attachments/{FileName} | Creates an attachment on a specific expense claim receipts by file name |
| GET | /Receipts/{ReceiptID}/History | Retrieves a history record for a specific receipt |
| PUT | /Receipts/{ReceiptID}/History | Creates a history record for a specific receipt |

### RepeatingInvoices
| Method | Path | Description |
|--------|------|-------------|
| GET | /RepeatingInvoices | Retrieves repeating invoices |
| PUT | /RepeatingInvoices | Creates one or more repeating invoice templates |
| POST | /RepeatingInvoices | Creates or deletes one or more repeating invoice templates |
| GET | /RepeatingInvoices/{RepeatingInvoiceID} | Retrieves a specific repeating invoice by using a unique repeating invoice Id |
| POST | /RepeatingInvoices/{RepeatingInvoiceID} | Deletes a specific repeating invoice template |
| GET | /RepeatingInvoices/{RepeatingInvoiceID}/Attachments | Retrieves attachments from a specific repeating invoice |
| GET | /RepeatingInvoices/{RepeatingInvoiceID}/Attachments/{AttachmentID} | Retrieves a specific attachment from a specific repeating invoice |
| GET | /RepeatingInvoices/{RepeatingInvoiceID}/Attachments/{FileName} | Retrieves a specific attachment from a specific repeating invoices by file name |
| POST | /RepeatingInvoices/{RepeatingInvoiceID}/Attachments/{FileName} | Updates a specific attachment from a specific repeating invoices by file name |
| PUT | /RepeatingInvoices/{RepeatingInvoiceID}/Attachments/{FileName} | Creates an attachment from a specific repeating invoices by file name |
| GET | /RepeatingInvoices/{RepeatingInvoiceID}/History | Retrieves history record for a specific repeating invoice |
| PUT | /RepeatingInvoices/{RepeatingInvoiceID}/History | Creates a  history record for a specific repeating invoice |

### Reports
| Method | Path | Description |
|--------|------|-------------|
| GET | /Reports/TenNinetyNine | Retrieve reports for 1099 |
| GET | /Reports/AgedPayablesByContact | Retrieves report for aged payables by contact |
| GET | /Reports/AgedReceivablesByContact | Retrieves report for aged receivables by contact |
| GET | /Reports/BalanceSheet | Retrieves report for balancesheet |
| GET | /Reports/BankSummary | Retrieves report for bank summary |
| GET | /Reports/{ReportID} | Retrieves a specific report using a unique ReportID |
| GET | /Reports/BudgetSummary | Retrieves report for budget summary |
| GET | /Reports/ExecutiveSummary | Retrieves report for executive summary |
| GET | /Reports | Retrieves a list of the organistaions unique reports that require a uuid to fetch |
| GET | /Reports/ProfitAndLoss | Retrieves report for profit and loss |
| GET | /Reports/TrialBalance | Retrieves report for trial balance |

### Setup
| Method | Path | Description |
|--------|------|-------------|
| POST | /Setup | Sets the chart of accounts, the conversion date and conversion balances |

### TaxRates
| Method | Path | Description |
|--------|------|-------------|
| GET | /TaxRates | Retrieves tax rates |
| PUT | /TaxRates | Creates one or more tax rates |
| POST | /TaxRates | Updates tax rates |
| GET | /TaxRates/{TaxType} | Retrieves a specific tax rate according to given TaxType code |

### TrackingCategories
| Method | Path | Description |
|--------|------|-------------|
| GET | /TrackingCategories | Retrieves tracking categories and options |
| PUT | /TrackingCategories | Create tracking categories |
| GET | /TrackingCategories/{TrackingCategoryID} | Retrieves specific tracking categories and options using a unique tracking category Id |
| POST | /TrackingCategories/{TrackingCategoryID} | Updates a specific tracking category |
| DELETE | /TrackingCategories/{TrackingCategoryID} | Deletes a specific tracking category |
| PUT | /TrackingCategories/{TrackingCategoryID}/Options | Creates options for a specific tracking category |
| POST | /TrackingCategories/{TrackingCategoryID}/Options/{TrackingOptionID} | Updates a specific option for a specific tracking category |
| DELETE | /TrackingCategories/{TrackingCategoryID}/Options/{TrackingOptionID} | Deletes a specific option for a specific tracking category |

### Users
| Method | Path | Description |
|--------|------|-------------|
| GET | /Users | Retrieves users |
| GET | /Users/{UserID} | Retrieves a specific user |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all Accounts?" -> GET /Accounts
- "Get Account details?" -> GET /Accounts/{AccountID}
- "Delete a Account?" -> DELETE /Accounts/{AccountID}
- "List all Attachments?" -> GET /Accounts/{AccountID}/Attachments
- "Get Attachment details?" -> GET /Accounts/{AccountID}/Attachments/{AttachmentID}
- "Get Attachment details?" -> GET /Accounts/{AccountID}/Attachments/{FileName}
- "Update a Attachment?" -> PUT /Accounts/{AccountID}/Attachments/{FileName}
- "List all BatchPayments?" -> GET /BatchPayments
- "Create a BatchPayment?" -> POST /BatchPayments
- "Get BatchPayment details?" -> GET /BatchPayments/{BatchPaymentID}
- "List all History?" -> GET /BatchPayments/{BatchPaymentID}/History
- "List all BankTransactions?" -> GET /BankTransactions
- "Create a BankTransaction?" -> POST /BankTransactions
- "Get BankTransaction details?" -> GET /BankTransactions/{BankTransactionID}
- "List all Attachments?" -> GET /BankTransactions/{BankTransactionID}/Attachments
- "Get Attachment details?" -> GET /BankTransactions/{BankTransactionID}/Attachments/{AttachmentID}
- "Get Attachment details?" -> GET /BankTransactions/{BankTransactionID}/Attachments/{FileName}
- "Update a Attachment?" -> PUT /BankTransactions/{BankTransactionID}/Attachments/{FileName}
- "List all History?" -> GET /BankTransactions/{BankTransactionID}/History
- "List all BankTransfers?" -> GET /BankTransfers
- "Get BankTransfer details?" -> GET /BankTransfers/{BankTransferID}
- "List all Attachments?" -> GET /BankTransfers/{BankTransferID}/Attachments
- "Get Attachment details?" -> GET /BankTransfers/{BankTransferID}/Attachments/{AttachmentID}
- "Get Attachment details?" -> GET /BankTransfers/{BankTransferID}/Attachments/{FileName}
- "Update a Attachment?" -> PUT /BankTransfers/{BankTransferID}/Attachments/{FileName}
- "List all History?" -> GET /BankTransfers/{BankTransferID}/History
- "List all BrandingThemes?" -> GET /BrandingThemes
- "Get BrandingTheme details?" -> GET /BrandingThemes/{BrandingThemeID}
- "List all PaymentServices?" -> GET /BrandingThemes/{BrandingThemeID}/PaymentServices
- "Create a PaymentService?" -> POST /BrandingThemes/{BrandingThemeID}/PaymentServices
- "List all Budgets?" -> GET /Budgets
- "Get Budget details?" -> GET /Budgets/{BudgetID}
- "List all Contacts?" -> GET /Contacts
- "Create a Contact?" -> POST /Contacts
- "Get Contact details?" -> GET /Contacts/{ContactNumber}
- "Get Contact details?" -> GET /Contacts/{ContactID}
- "List all Attachments?" -> GET /Contacts/{ContactID}/Attachments
- "Get Attachment details?" -> GET /Contacts/{ContactID}/Attachments/{AttachmentID}
- "Get Attachment details?" -> GET /Contacts/{ContactID}/Attachments/{FileName}
- "Update a Attachment?" -> PUT /Contacts/{ContactID}/Attachments/{FileName}
- "List all CISSettings?" -> GET /Contacts/{ContactID}/CISSettings
- "List all History?" -> GET /Contacts/{ContactID}/History
- "List all ContactGroups?" -> GET /ContactGroups
- "Get ContactGroup details?" -> GET /ContactGroups/{ContactGroupID}
- "Delete a Contact?" -> DELETE /ContactGroups/{ContactGroupID}/Contacts/{ContactID}
- "List all CreditNotes?" -> GET /CreditNotes
- "Create a CreditNote?" -> POST /CreditNotes
- "Get CreditNote details?" -> GET /CreditNotes/{CreditNoteID}
- "List all Attachments?" -> GET /CreditNotes/{CreditNoteID}/Attachments
- "Get Attachment details?" -> GET /CreditNotes/{CreditNoteID}/Attachments/{AttachmentID}
- "Get Attachment details?" -> GET /CreditNotes/{CreditNoteID}/Attachments/{FileName}
- "Update a Attachment?" -> PUT /CreditNotes/{CreditNoteID}/Attachments/{FileName}
- "List all pdf?" -> GET /CreditNotes/{CreditNoteID}/pdf
- "Delete a Allocation?" -> DELETE /CreditNotes/{CreditNoteID}/Allocations/{AllocationID}
- "List all History?" -> GET /CreditNotes/{CreditNoteID}/History
- "List all Currencies?" -> GET /Currencies
- "List all Employees?" -> GET /Employees
- "Create a Employee?" -> POST /Employees
- "Get Employee details?" -> GET /Employees/{EmployeeID}
- "List all ExpenseClaims?" -> GET /ExpenseClaims
- "Get ExpenseClaim details?" -> GET /ExpenseClaims/{ExpenseClaimID}
- "List all History?" -> GET /ExpenseClaims/{ExpenseClaimID}/History
- "List all Invoices?" -> GET /Invoices
- "Create a Invoice?" -> POST /Invoices
- "Get Invoice details?" -> GET /Invoices/{InvoiceID}
- "List all pdf?" -> GET /Invoices/{InvoiceID}/pdf
- "List all Attachments?" -> GET /Invoices/{InvoiceID}/Attachments
- "Get Attachment details?" -> GET /Invoices/{InvoiceID}/Attachments/{AttachmentID}
- "Get Attachment details?" -> GET /Invoices/{InvoiceID}/Attachments/{FileName}
- "Update a Attachment?" -> PUT /Invoices/{InvoiceID}/Attachments/{FileName}
- "List all OnlineInvoice?" -> GET /Invoices/{InvoiceID}/OnlineInvoice
- "Create a Email?" -> POST /Invoices/{InvoiceID}/Email
- "List all History?" -> GET /Invoices/{InvoiceID}/History
- "List all Settings?" -> GET /InvoiceReminders/Settings
- "List all Items?" -> GET /Items
- "Create a Item?" -> POST /Items
- "Get Item details?" -> GET /Items/{ItemID}
- "Delete a Item?" -> DELETE /Items/{ItemID}
- "List all History?" -> GET /Items/{ItemID}/History
- "List all Journals?" -> GET /Journals
- "Get Journal details?" -> GET /Journals/{JournalID}
- "Get Journal details?" -> GET /Journals/{JournalNumber}
- "List all LinkedTransactions?" -> GET /LinkedTransactions
- "Get LinkedTransaction details?" -> GET /LinkedTransactions/{LinkedTransactionID}
- "Delete a LinkedTransaction?" -> DELETE /LinkedTransactions/{LinkedTransactionID}
- "List all ManualJournals?" -> GET /ManualJournals
- "Create a ManualJournal?" -> POST /ManualJournals
- "Get ManualJournal details?" -> GET /ManualJournals/{ManualJournalID}
- "List all Attachments?" -> GET /ManualJournals/{ManualJournalID}/Attachments
- "Get Attachment details?" -> GET /ManualJournals/{ManualJournalID}/Attachments/{AttachmentID}
- "Get Attachment details?" -> GET /ManualJournals/{ManualJournalID}/Attachments/{FileName}
- "Update a Attachment?" -> PUT /ManualJournals/{ManualJournalID}/Attachments/{FileName}
- "List all History?" -> GET /ManualJournals/{ManualJournalID}/History
- "List all Organisation?" -> GET /Organisation
- "List all Actions?" -> GET /Organisation/Actions
- "List all CISSettings?" -> GET /Organisation/{OrganisationID}/CISSettings
- "List all Overpayments?" -> GET /Overpayments
- "Get Overpayment details?" -> GET /Overpayments/{OverpaymentID}
- "Delete a Allocation?" -> DELETE /Overpayments/{OverpaymentID}/Allocations/{AllocationID}
- "List all History?" -> GET /Overpayments/{OverpaymentID}/History
- "List all Payments?" -> GET /Payments
- "Create a Payment?" -> POST /Payments
- "Get Payment details?" -> GET /Payments/{PaymentID}
- "List all History?" -> GET /Payments/{PaymentID}/History
- "List all PaymentServices?" -> GET /PaymentServices
- "List all Prepayments?" -> GET /Prepayments
- "Get Prepayment details?" -> GET /Prepayments/{PrepaymentID}
- "Delete a Allocation?" -> DELETE /Prepayments/{PrepaymentID}/Allocations/{AllocationID}
- "List all History?" -> GET /Prepayments/{PrepaymentID}/History
- "List all PurchaseOrders?" -> GET /PurchaseOrders
- "Create a PurchaseOrder?" -> POST /PurchaseOrders
- "List all pdf?" -> GET /PurchaseOrders/{PurchaseOrderID}/pdf
- "Get PurchaseOrder details?" -> GET /PurchaseOrders/{PurchaseOrderID}
- "Get PurchaseOrder details?" -> GET /PurchaseOrders/{PurchaseOrderNumber}
- "List all History?" -> GET /PurchaseOrders/{PurchaseOrderID}/History
- "List all Attachments?" -> GET /PurchaseOrders/{PurchaseOrderID}/Attachments
- "Get Attachment details?" -> GET /PurchaseOrders/{PurchaseOrderID}/Attachments/{AttachmentID}
- "Get Attachment details?" -> GET /PurchaseOrders/{PurchaseOrderID}/Attachments/{FileName}
- "Update a Attachment?" -> PUT /PurchaseOrders/{PurchaseOrderID}/Attachments/{FileName}
- "List all Quotes?" -> GET /Quotes
- "Create a Quote?" -> POST /Quotes
- "Get Quote details?" -> GET /Quotes/{QuoteID}
- "List all History?" -> GET /Quotes/{QuoteID}/History
- "List all pdf?" -> GET /Quotes/{QuoteID}/pdf
- "List all Attachments?" -> GET /Quotes/{QuoteID}/Attachments
- "Get Attachment details?" -> GET /Quotes/{QuoteID}/Attachments/{AttachmentID}
- "Get Attachment details?" -> GET /Quotes/{QuoteID}/Attachments/{FileName}
- "Update a Attachment?" -> PUT /Quotes/{QuoteID}/Attachments/{FileName}
- "List all Receipts?" -> GET /Receipts
- "Get Receipt details?" -> GET /Receipts/{ReceiptID}
- "List all Attachments?" -> GET /Receipts/{ReceiptID}/Attachments
- "Get Attachment details?" -> GET /Receipts/{ReceiptID}/Attachments/{AttachmentID}
- "Get Attachment details?" -> GET /Receipts/{ReceiptID}/Attachments/{FileName}
- "Update a Attachment?" -> PUT /Receipts/{ReceiptID}/Attachments/{FileName}
- "List all History?" -> GET /Receipts/{ReceiptID}/History
- "List all RepeatingInvoices?" -> GET /RepeatingInvoices
- "Create a RepeatingInvoice?" -> POST /RepeatingInvoices
- "Get RepeatingInvoice details?" -> GET /RepeatingInvoices/{RepeatingInvoiceID}
- "List all Attachments?" -> GET /RepeatingInvoices/{RepeatingInvoiceID}/Attachments
- "Get Attachment details?" -> GET /RepeatingInvoices/{RepeatingInvoiceID}/Attachments/{AttachmentID}
- "Get Attachment details?" -> GET /RepeatingInvoices/{RepeatingInvoiceID}/Attachments/{FileName}
- "Update a Attachment?" -> PUT /RepeatingInvoices/{RepeatingInvoiceID}/Attachments/{FileName}
- "List all History?" -> GET /RepeatingInvoices/{RepeatingInvoiceID}/History
- "List all TenNinetyNine?" -> GET /Reports/TenNinetyNine
- "List all AgedPayablesByContact?" -> GET /Reports/AgedPayablesByContact
- "List all AgedReceivablesByContact?" -> GET /Reports/AgedReceivablesByContact
- "List all BalanceSheet?" -> GET /Reports/BalanceSheet
- "List all BankSummary?" -> GET /Reports/BankSummary
- "Get Report details?" -> GET /Reports/{ReportID}
- "List all BudgetSummary?" -> GET /Reports/BudgetSummary
- "List all ExecutiveSummary?" -> GET /Reports/ExecutiveSummary
- "List all Reports?" -> GET /Reports
- "List all ProfitAndLoss?" -> GET /Reports/ProfitAndLoss
- "List all TrialBalance?" -> GET /Reports/TrialBalance
- "Create a Setup?" -> POST /Setup
- "List all TaxRates?" -> GET /TaxRates
- "Create a TaxRate?" -> POST /TaxRates
- "Get TaxRate details?" -> GET /TaxRates/{TaxType}
- "List all TrackingCategories?" -> GET /TrackingCategories
- "Get TrackingCategory details?" -> GET /TrackingCategories/{TrackingCategoryID}
- "Delete a TrackingCategory?" -> DELETE /TrackingCategories/{TrackingCategoryID}
- "Delete a Option?" -> DELETE /TrackingCategories/{TrackingCategoryID}/Options/{TrackingOptionID}
- "List all Users?" -> GET /Users
- "Get User details?" -> GET /Users/{UserID}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
