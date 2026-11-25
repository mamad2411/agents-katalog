---
name: avaza-api-documentation
description: "Avaza API Documentation API skill. Use when working with Avaza API Documentation for api, ScheduleSeries. Covers 94 endpoints."
version: 1.0.0
generator: lapsh
---

# Avaza API Documentation
API version: v1

## Auth
OAuth2

## Base URL
https://api.avaza.com

## Setup
1. Configure auth: OAuth2
2. GET /api/Account -- verify access
3. POST /api/Bill -- create first Bill

## Endpoints

94 endpoints across 2 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/Account | Account Details |
| GET | /api/Bill | Gets list of Bills |
| POST | /api/Bill | Create a new draft Bill |
| GET | /api/Bill/{id} | Gets a Bill by Bill ID |
| GET | /api/BillPayment | Gets list of Bill Payments |
| POST | /api/BillPayment | Create new Bill Payment and optionally assign payment allocations to Bills |
| GET | /api/BillPayment/{id} | Gets a Bill Payment by Payment Transaction ID |
| GET | /api/Company/Lookup | Gets minimal list of Companies. |
| GET | /api/Company | Gets list of Companies |
| PUT | /api/Company | Update a Company record. |
| POST | /api/Company | Create a Company |
| GET | /api/Company/{id} | Gets Company by Company ID |
| GET | /api/Contact | Gets list of Contacts |
| POST | /api/Contact | Create a Contact |
| GET | /api/Contact/{id} | Gets Contact by Contact ID |
| GET | /api/CreditNote | Gets list of CreditNotes |
| GET | /api/CreditNote/{id} | Gets Credit Note by CreditNoteID |
| GET | /api/Currency | Gets list of Currencies |
| GET | /api/Estimate | Gets list of Estimates |
| POST | /api/Estimate | Create a new draft Estimate |
| GET | /api/Estimate/{id} | Gets Estimate by Estimate ID |
| POST | /api/Expense/Attachment |  |
| POST | /api/ExpenseApproval/Submit | Submit Expenses for Approval. |
| GET | /api/Expense | Gets list of Expenses |
| PUT | /api/Expense | Update an Expense |
| POST | /api/Expense | Create an Expense |
| DELETE | /api/Expense | Delete Expense Entries |
| GET | /api/Expense/{id} | Gets an Expense Entry by Expense ID |
| GET | /api/ExpenseCategory | Gets list of Expense Categories |
| GET | /api/ExpenseGroup/Lookup | Gets minimal list of Expense Groups. |
| GET | /api/ExpenseMerchant/Lookup | Gets minimal list of Expense Merchants. |
| GET | /api/ExpensePaymentMethod/Lookup | Gets minimal list of Expense Payment Methods. |
| GET | /api/ExpenseSummary | Gets Basic Summary of Expense Statistics |
| GET | /api/FixedAmount | Gets list of Fixed Amounts |
| GET | /api/Inventory | Gets list of Inventory |
| GET | /api/Inventory/{id} | Gets InventoryItem by InventoryItem ID |
| GET | /api/Invoice | Gets list of Invoices |
| PUT | /api/Invoice | Update an Invoice |
| POST | /api/Invoice | Create a new draft invoice |
| GET | /api/Invoice/{id} | Gets Invoice by Invoice ID |
| GET | /api/Payment | Gets list of Payments |
| POST | /api/Payment | Create new Payment and optionally assign payment allocations to Invoices |
| GET | /api/Payment/{id} | Gets Payment by Payment Transaction ID |
| GET | /api/Project/Lookup | Gets minimal list of active Projects for the current user |
| GET | /api/Project | Gets list of Projects |
| PUT | /api/Project | Update an Project |
| POST | /api/Project | Create a Project |
| GET | /api/Project/{id} | Gets Project by Project ID |
| GET | /api/ProjectMember | Gets list of Project Members |
| PUT | /api/ProjectMember | Update a Member of a Project |
| POST | /api/ProjectMember | Assign a user as a Member of a Project |
| GET | /api/ProjectTimesheetCategory | Gets list of Project Timesheet Categories |
| PUT | /api/ProjectTimesheetCategory | Update a TimeSheetCategory on a Project. |
| POST | /api/ProjectTimesheetCategory | Assign a TimeSheetCategory to a Project. |
| GET | /api/RecurringInvoice | Gets list of Recurring Invoices |
| GET | /api/RecurringInvoice/{id} | Gets RecurringInvoice by ID |
| GET | /api/ScheduleAssignment | Gets list of Schedule Assignments. |
| GET | /api/ScheduleSeries | Gets list of Schedule Series |
| POST | /api/ScheduleSeries | Retrieves a list of Schedule Series. This Http Post version adds a ScheduleSeriesIDs collection filter. |
| DELETE | /api/ScheduleSeries/{id} | Delete a Schedule Series entry |
| GET | /api/Section | Gets list of Sections |
| POST | /api/Section | Create a Section |
| DELETE | /api/Section | Delete a Section |
| GET | /api/Task/Lookup | Gets minimal list of Tasks for the current user |
| GET | /api/Task | Gets list of Tasks |
| PUT | /api/Task | Update a Task. |
| POST | /api/Task | Create a Task |
| DELETE | /api/Task | Delete a Task |
| GET | /api/Task/{id} | Gets Task by Task ID |
| GET | /api/TaskDiscussion | Gets list of Task Discussion Messages |
| GET | /api/TaskStatus | Gets list of Task Statuses |
| GET | /api/TaskType | Gets list of Task Types |
| GET | /api/Tax | Get List of Taxes configured in the Avaza account. |
| GET | /api/Timesheet/deleted | Retrieves deleted (tombstone) timesheet entries. Admin access only. |
| GET | /api/Timesheet | Gets list of Timsheets |
| PUT | /api/Timesheet | Update a Timesheet |
| POST | /api/Timesheet | Create a new Timesheet Entry |
| GET | /api/Timesheet/{id} | Gets a Timesheet Entry by Timesheet ID |
| DELETE | /api/Timesheet/{id} | Delete a Timesheet Entry |
| POST | /api/TimesheetSubmission | Submit Timesheets for Approval. |
| GET | /api/TimesheetSummary | Gets Basic Summary of Timesheet Statistics |
| GET | /api/TimesheetTimer | Gets the  Running Timer if there is one for a user. |
| POST | /api/TimesheetTimer/{id} | Starts a Timer running on an existing Timesheet Entry |
| DELETE | /api/TimesheetTimer/{id} | Stop the timer running on an existing Timesheet Entry |
| GET | /api/UserProfile | Get Collection of Users who have roles in the current Avaza account. |
| GET | /api/Webhook | Get list of Webhook Subscriptions |
| POST | /api/Webhook | Subscribe to Webhook. On success, returns ID of webhook subscription. |
| DELETE | /api/Webhook | Delete webhook subscription by URL |
| GET | /api/Webhook/{id} | Get Webhook Subscription by SubscriptionID |
| DELETE | /api/Webhook/{id} | Delete Webhook Subscription by ID |

### ScheduleSeries
| Method | Path | Description |
|--------|------|-------------|
| POST | /ScheduleSeries/AddBooking | Create new Schedule Booking |
| POST | /ScheduleSeries/AddLeave | Create new Leave Booking |
| PUT | /ScheduleSeries/EditLeave | Edit Leave Booking |
| PUT | /ScheduleSeries/EditBooking | Edit Booking |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all Account?" -> GET /api/Account
- "List all Bill?" -> GET /api/Bill
- "Create a Bill?" -> POST /api/Bill
- "Get Bill details?" -> GET /api/Bill/{id}
- "List all BillPayment?" -> GET /api/BillPayment
- "Create a BillPayment?" -> POST /api/BillPayment
- "Get BillPayment details?" -> GET /api/BillPayment/{id}
- "Search Lookup?" -> GET /api/Company/Lookup
- "List all Company?" -> GET /api/Company
- "Create a Company?" -> POST /api/Company
- "Get Company details?" -> GET /api/Company/{id}
- "List all Contact?" -> GET /api/Contact
- "Create a Contact?" -> POST /api/Contact
- "Get Contact details?" -> GET /api/Contact/{id}
- "List all CreditNote?" -> GET /api/CreditNote
- "Get CreditNote details?" -> GET /api/CreditNote/{id}
- "List all Currency?" -> GET /api/Currency
- "List all Estimate?" -> GET /api/Estimate
- "Create a Estimate?" -> POST /api/Estimate
- "Get Estimate details?" -> GET /api/Estimate/{id}
- "Create a Attachment?" -> POST /api/Expense/Attachment
- "Create a Submit?" -> POST /api/ExpenseApproval/Submit
- "Search Expense?" -> GET /api/Expense
- "Create a Expense?" -> POST /api/Expense
- "Get Expense details?" -> GET /api/Expense/{id}
- "List all ExpenseCategory?" -> GET /api/ExpenseCategory
- "Search Lookup?" -> GET /api/ExpenseGroup/Lookup
- "Search Lookup?" -> GET /api/ExpenseMerchant/Lookup
- "List all Lookup?" -> GET /api/ExpensePaymentMethod/Lookup
- "List all ExpenseSummary?" -> GET /api/ExpenseSummary
- "List all FixedAmount?" -> GET /api/FixedAmount
- "List all Inventory?" -> GET /api/Inventory
- "Get Inventory details?" -> GET /api/Inventory/{id}
- "List all Invoice?" -> GET /api/Invoice
- "Create a Invoice?" -> POST /api/Invoice
- "Get Invoice details?" -> GET /api/Invoice/{id}
- "List all Payment?" -> GET /api/Payment
- "Create a Payment?" -> POST /api/Payment
- "Get Payment details?" -> GET /api/Payment/{id}
- "Search Lookup?" -> GET /api/Project/Lookup
- "List all Project?" -> GET /api/Project
- "Create a Project?" -> POST /api/Project
- "Get Project details?" -> GET /api/Project/{id}
- "List all ProjectMember?" -> GET /api/ProjectMember
- "Create a ProjectMember?" -> POST /api/ProjectMember
- "List all ProjectTimesheetCategory?" -> GET /api/ProjectTimesheetCategory
- "Create a ProjectTimesheetCategory?" -> POST /api/ProjectTimesheetCategory
- "List all RecurringInvoice?" -> GET /api/RecurringInvoice
- "Get RecurringInvoice details?" -> GET /api/RecurringInvoice/{id}
- "List all ScheduleAssignment?" -> GET /api/ScheduleAssignment
- "Create a AddBooking?" -> POST /ScheduleSeries/AddBooking
- "Create a AddLeave?" -> POST /ScheduleSeries/AddLeave
- "List all ScheduleSeries?" -> GET /api/ScheduleSeries
- "Create a ScheduleSery?" -> POST /api/ScheduleSeries
- "Delete a ScheduleSery?" -> DELETE /api/ScheduleSeries/{id}
- "List all Section?" -> GET /api/Section
- "Create a Section?" -> POST /api/Section
- "Search Lookup?" -> GET /api/Task/Lookup
- "List all Task?" -> GET /api/Task
- "Create a Task?" -> POST /api/Task
- "Get Task details?" -> GET /api/Task/{id}
- "List all TaskDiscussion?" -> GET /api/TaskDiscussion
- "List all TaskStatus?" -> GET /api/TaskStatus
- "List all TaskType?" -> GET /api/TaskType
- "List all Tax?" -> GET /api/Tax
- "List all deleted?" -> GET /api/Timesheet/deleted
- "List all Timesheet?" -> GET /api/Timesheet
- "Create a Timesheet?" -> POST /api/Timesheet
- "Get Timesheet details?" -> GET /api/Timesheet/{id}
- "Delete a Timesheet?" -> DELETE /api/Timesheet/{id}
- "Create a TimesheetSubmission?" -> POST /api/TimesheetSubmission
- "List all TimesheetSummary?" -> GET /api/TimesheetSummary
- "List all TimesheetTimer?" -> GET /api/TimesheetTimer
- "Delete a TimesheetTimer?" -> DELETE /api/TimesheetTimer/{id}
- "List all UserProfile?" -> GET /api/UserProfile
- "List all Webhook?" -> GET /api/Webhook
- "Create a Webhook?" -> POST /api/Webhook
- "Get Webhook details?" -> GET /api/Webhook/{id}
- "Delete a Webhook?" -> DELETE /api/Webhook/{id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
