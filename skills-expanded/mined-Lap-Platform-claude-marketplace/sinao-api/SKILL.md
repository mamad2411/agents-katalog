---
name: sinao-api
description: "Sinao API skill. Use when working with Sinao for login, sendpassword, changepassword. Covers 383 endpoints."
version: 1.0.0
generator: lapsh
---

# Sinao API
API version: 1.1.0

## Auth
Bearer bearer | Bearer basic | Bearer basic

## Base URL
https://api.sinao.app/v1

## Setup
1. Set Authorization header with your Bearer token
2. GET /refresh -- verify access
3. POST /login -- create first login

## Endpoints

383 endpoints across 12 groups. See references/api-spec.lap for full details.

### login
| Method | Path | Description |
|--------|------|-------------|
| POST | /login | Login |
| POST | /login/send/2fa | Send 2FA code |

### sendpassword
| Method | Path | Description |
|--------|------|-------------|
| POST | /sendpassword | Password recover by email |

### changepassword
| Method | Path | Description |
|--------|------|-------------|
| POST | /changepassword | Change password |

### logout
| Method | Path | Description |
|--------|------|-------------|
| POST | /logout | Logout |

### refresh
| Method | Path | Description |
|--------|------|-------------|
| GET | /refresh | Refresh a token |

### me
| Method | Path | Description |
|--------|------|-------------|
| GET | /me | Get current user |
| POST | /me | Update current user |

### register
| Method | Path | Description |
|--------|------|-------------|
| POST | /register | Create an User |

### apps
| Method | Path | Description |
|--------|------|-------------|
| POST | /apps | Create an app |
| GET | /apps | List apps |
| GET | /apps/{appId} | Get an app |
| GET | /apps/{appId}/ping | Ping app web hostname |
| POST | /apps/{appId}/reset | Reset all data |
| GET | /apps/{appId}/apikeys | Get all api keys |
| POST | /apps/{appId}/apikeys | Create new API key |
| DELETE | /apps/{appId}/apikeys/{id} | Remove an api key |
| GET | /apps/{appId}/apipartners | Get all api partners |
| GET | /apps/{appId}/settings | Get app config |
| POST | /apps/{appId}/settings | Update app config |
| GET | /apps/{appId}/jobs/{job} | Get app job |
| GET | /apps/{appId}/templates | Get templates |
| POST | /apps/{appId}/templates | Create a template |
| GET | /apps/{appId}/document-langs | Get document (invoice or quote) available printable langs |
| POST | /apps/{appId}/templates/batch | Create multiple templates |
| GET | /apps/{appId}/templates/default | Get default template |
| GET | /apps/{appId}/templates/{id} | Get a template |
| POST | /apps/{appId}/templates/{id} | Update a template |
| GET | /apps/{appId}/subscription/plan/extra | Get current plan |
| GET | /apps/{appId}/subscription/customer | Stripe Customer object |
| POST | /apps/{appId}/subscription/customer | Stripe Customer object |
| GET | /apps/{appId}/subscription/plan | Get current plan |
| DELETE | /apps/{appId}/subscription/plan | End current plan |
| GET | /apps/{appId}/subscription/plans | Get plans |
| GET | /apps/{appId}/subscription/invoices | See all invoices |
| GET | /apps/{appId}/subscription/payment_methods | See all payment methods |
| GET | /apps/{appId}/subscription/extra/count | Count extra usage |
| POST | /apps/{appId}/subscription/extra/{stripe_plan} | Enable plan |
| GET | /apps/{appId}/subscription/plans/{stripe_plan} | Simulate a plan |
| POST | /apps/{appId}/subscription/plans/{stripe_plan} | Change plan |
| GET | /apps/{appId}/subscription/plans/{stripe_plan}/checkout | Get payment link to Stripe Checkout |
| GET | /apps/{appId}/subscription/checkout_session | Get Stripe Checkout Session id |
| GET | /apps/{appId}/subscription/checkout_add_source | Get payment link to Stripe Checkout |
| POST | /apps/{appId}/subscription/source | Add creditcard or sepadebit |
| DELETE | /apps/{appId}/subscription/source | Remove creditcard or sepadebit |
| POST | /apps/{appId}/subscription/source/default | Change default source |
| POST | /apps/{appId}/subscription/pay_all | Pay all due invoices |
| POST | /apps/{appId}/subscription/cancel | Cancel the subscription now |
| POST | /apps/{appId}/subscription/extend_trial | Extend trial period |
| POST | /apps/{appId}/subscription/coupon | Add coupon |
| GET | /apps/{appId}/subscription/coupon | See coupon |
| POST | /apps/{appId}/subscription/anchordate | Update anchor date |
| GET | /apps/{appId}/access/profiles | Get profiles |
| POST | /apps/{appId}/access/invite | Invite an user |
| GET | /apps/{appId}/access/invite | List invitations |
| DELETE | /apps/{appId}/access/invite/{id} | Delete an invitation |
| GET | /apps/{appId}/pennylane/refresh-token | endpoint for Pennylane fesh bearer token |
| POST | /apps/access/invite/{accessToken}/register | Create an User by invitation |
| GET | /apps/access/invite/{accessToken} | Get invitation informations |
| DELETE | /apps/access/invite/{accessToken} | Delete an invitation from token |
| POST | /apps/access/accounting/policies/accounting/batch | Create/update policies for a user |
| GET | /apps/{appId}/access | Get policies for an app |
| GET | /apps/{appId}/access/{userId} | Get police for an user |
| POST | /apps/{appId}/access/{userId} | Update police for an user |
| DELETE | /apps/{appId}/access/{userId} | Delete police for an user |
| GET | /apps/{appId}/organization | Get organization profile for current app |
| POST | /apps/{appId}/organization | Update organization profile for current app |
| GET | /apps/{appId}/organizations | List organizations |
| POST | /apps/{appId}/organizations | Create an organization |
| POST | /apps/{appId}/organizations/batch | Create multiple organizations |
| DELETE | /apps/{appId}/organizations/batch | Remove multiple organizations |
| POST | /apps/{appId}/organizations/chorus-search | Search organizations in Chorus Pro |
| GET | /apps/{appId}/organizations/{id} | Get an organization |
| POST | /apps/{appId}/organizations/{id} | Update an organization |
| DELETE | /apps/{appId}/organizations/{id} | Remove an organization |
| GET | /apps/{appId}/organizations/{id}/restore | Restore an organization |
| GET | /apps/{appId}/organizations/{id}/sepa/mandate | Get sepa_mandate of a organizations |
| DELETE | /apps/{appId}/organizations/delete/all | Remove all organizations |
| GET | /apps/{appId}/persons | List persons |
| POST | /apps/{appId}/persons | Create a person |
| POST | /apps/{appId}/persons/batch | Create multiple persons |
| DELETE | /apps/{appId}/persons/batch | Delete many persons |
| GET | /apps/{appId}/persons/{id} | Get a person |
| POST | /apps/{appId}/persons/{id} | Update a person |
| DELETE | /apps/{appId}/persons/{id} | Remove a person |
| GET | /apps/{appId}/persons/{id}/restore | Restore a person |
| GET | /apps/{appId}/persons/{id}/sepa/mandate | Get sepa_mandate of a person |
| DELETE | /apps/{appId}/persons/delete/all | Remove all persons |
| GET | /apps/{appId}/establishments/{id} | Get an establishment |
| POST | /apps/{appId}/establishments/{id} | Update an establishment |
| DELETE | /apps/{appId}/establishments/{id} | Remove an establishment |
| POST | /apps/{appId}/establishments/{establishment_id}/contact/{contact_id} | Update an establishment contact |
| DELETE | /apps/{appId}/establishments/{establishment_id}/contact/{contact_id} | Remove an establishment contact |
| GET | /apps/{appId}/relationships | List relationships |
| POST | /apps/{appId}/relationships/{id}/attach | Attach a file |
| DELETE | /apps/{appId}/relationships/{id}/attach | Detach a file |
| GET | /apps/{appId}/relationships/{id} | Get a relationship |
| POST | /apps/{appId}/relationships/{id} | Update a relationship |
| POST | /apps/{appId}/relationships/{id}/tag | Add a tag on a relationship |
| DELETE | /apps/{appId}/relationships/{id}/tag | Delete a tag on a relationship |
| POST | /apps/{appId}/contacts/merge | Merge many contacts |
| GET | /apps/{appId}/invoices | List invoices |
| POST | /apps/{appId}/invoices | Create an invoice |
| POST | /apps/{appId}/invoices/batch | Create or update many invoices |
| DELETE | /apps/{appId}/invoices/batch | Delete many invoices |
| GET | /apps/{appId}/invoices/nextnumber | Get the next invoice number for preview |
| GET | /apps/{appId}/invoices/download | Download a list of invoices in pdf into a .zip file |
| GET | /apps/{appId}/invoices/statistics | Obtain statistics about invoices |
| POST | /apps/{appId}/invoices/fresh | Regenerate pdf and recalcul amounts of invoice |
| POST | /apps/{appId}/invoices/chorus-pro | Send selected invoices to Chorus-Pro |
| GET | /apps/{appId}/invoices/{id} | Get an invoice |
| POST | /apps/{appId}/invoices/{id} | Update an invoice |
| DELETE | /apps/{appId}/invoices/{id} | Remove an invoice |
| POST | /apps/{appId}/invoices/{id}/duplicate | Duplicate an invoice |
| POST | /apps/{appId}/invoices/{id}/avoid | Create a creditnote on an invoice |
| POST | /apps/{appId}/invoices/{id}/finalize | Finalize an invoice |
| POST | /apps/{appId}/invoices/{id}/updatestatus | Update the status of an invoice |
| POST | /apps/{appId}/invoices/{id}/attach | Attach a file at an invoice |
| DELETE | /apps/{appId}/invoices/{id}/attach | Detach a file at an invoice |
| POST | /apps/{appId}/invoices/{id}/tag | Add a tag on an invoice |
| DELETE | /apps/{appId}/invoices/{id}/tag | Delete a tag on an invoice |
| GET | /apps/{appId}/invoices/{id}/pdf | Download the invoice as pdf |
| GET | /apps/{appId}/invoices/{id}/preview.jpg | Download invoice as jpeg |
| GET | /apps/{appId}/invoice/{id}/link | Generate an invoice link |
| POST | /apps/{appId}/invoices/batch/breakdown | Update the breakdown of an invoice |
| DELETE | /apps/{appId}/invoices/delete/all | Remove all purchases |
| GET | /apps/{appId}/quotes | List quotes |
| POST | /apps/{appId}/quotes | Create a quote |
| POST | /apps/{appId}/quotes/batch | Create or update many quotes |
| DELETE | /apps/{appId}/quotes/batch | Delete many quotes |
| POST | /apps/{appId}/quotes/invoice | Create or update many quotes |
| GET | /apps/{appId}/quotes/nextnumber | Get the next quote number for preview |
| GET | /apps/{appId}/quotes/download | Download a list of quotes in pdf into a .zip file |
| GET | /apps/{appId}/quotes/statistics | Obtain statistics about quotes |
| POST | /apps/{appId}/quotes/fresh | Regenerate pdf and recalcul amounts of quote |
| GET | /apps/{appId}/quotes/{id} | Get a quote |
| POST | /apps/{appId}/quotes/{id} | Update a quote |
| DELETE | /apps/{appId}/quotes/{id} | Remove a quote |
| POST | /apps/{appId}/quotes/{id}/finalize | Finalize a quote |
| POST | /apps/{appId}/quotes/{id}/duplicate | Duplicate a quote |
| POST | /apps/{appId}/quotes/{id}/invoice | Transform the quote in invoice |
| POST | /apps/{appId}/quotes/{id}/situation_invoice | Transform the quote into a situation invoice |
| POST | /apps/{appId}/quotes/{id}/downpayment | Transform the quote in a downpayment invoice |
| POST | /apps/{appId}/quotes/{id}/updatestatus | Update the status of a quote |
| POST | /apps/{appId}/quotes/{id}/attach | Attach a file at a quote |
| DELETE | /apps/{appId}/quotes/{id}/attach | Detach a file at a quote |
| POST | /apps/{appId}/quotes/{id}/tag | Add a tag on an quote |
| DELETE | /apps/{appId}/quotes/{id}/tag | Delete a tag on a quote |
| GET | /apps/{appId}/quotes/{id}/pdf | Download the quote as pdf |
| GET | /apps/{appId}/quotes/{id}/preview.jpg | Download quote as jpeg |
| GET | /apps/{appId}/quotes/{id}/yousign/preview.jpg | Download quote as jpeg |
| DELETE | /apps/{appId}/quotes/delete/all | Remove all quotes |
| POST | /apps/{appId}/quotes/batch/breakdown | Update the breakdown of an quote |
| GET | /apps/{appId}/salesdocumentmodels | List sales documents models |
| POST | /apps/{appId}/salesdocumentmodels | Create a sales document model |
| GET | /apps/{appId}/salesdocumentmodels/{id} | Get a sales document model |
| POST | /apps/{appId}/salesdocumentmodels/{id} | Update a sales document model |
| DELETE | /apps/{appId}/salesdocumentmodels/{id} | Remove a sales document model |
| GET | /apps/{appId}/recurringinvoices | List RecurringInvoice |
| POST | /apps/{appId}/recurringinvoices | Create a RecurringInvoice |
| POST | /apps/{appId}/recurringinvoices/batch | Create or update many RecurringInvoice |
| DELETE | /apps/{appId}/recurringinvoices/batch | Delete many RecurringInvoice |
| GET | /apps/{appId}/recurringinvoices/periods | Get json of periods_formats for a date. |
| GET | /apps/{appId}/recurringinvoices/{id} | Get a RecurringInvoice |
| POST | /apps/{appId}/recurringinvoices/{id} | Update a RecurringInvoice |
| DELETE | /apps/{appId}/recurringinvoices/{id} | Remove a RecurringInvoice |
| GET | /apps/{appId}/recurringinvoices/{id}/plan | Preview next invoices generations |
| GET | /apps/{appId}/bankdetails | List BankDetails |
| POST | /apps/{appId}/bankdetails | Create a BankDetails |
| GET | /apps/{appId}/bankdetails/{id} | Get a BankDetails |
| POST | /apps/{appId}/bankdetails/{id} | Update a BankDetails |
| DELETE | /apps/{appId}/bankdetails/{id} | Remove a BankDetails |
| POST | /apps/{appId}/email/document | Send an email |
| POST | /apps/{appId}/email/batch | Send emails |
| GET | /apps/{appId}/email/document/{id} | Get all emails assign to a document |
| GET | /apps/{appId}/purchases | List purchases |
| POST | /apps/{appId}/purchases | Create a purchase |
| GET | /apps/{appId}/purchases/statistics | Obtain statistics about purchases |
| POST | /apps/{appId}/purchases/batch | Create or update many purchases |
| DELETE | /apps/{appId}/purchases/batch | Delete many purchases |
| GET | /apps/{appId}/purchases/download | Download a list of purchases in pdf into a .zip file |
| GET | /apps/{appId}/purchases/{id} | Get a purchase |
| POST | /apps/{appId}/purchases/{id} | Update a purchase |
| DELETE | /apps/{appId}/purchases/{id} | Remove a purchase |
| POST | /apps/{appId}/purchases/{id}/updatestatus | Update the status of an invoice |
| POST | /apps/{appId}/purchases/{id}/attach | Attach a file at a purchase |
| DELETE | /apps/{appId}/purchases/{id}/attach | Detach a file at a purchase |
| POST | /apps/{appId}/purchases/{id}/tag | Add a tag on a purchase |
| DELETE | /apps/{appId}/purchases/{id}/tag | Delete a tag on a purchase |
| GET | /apps/{appId}/purchases/{id}/original | Download the purchase as pdf |
| GET | /apps/{appId}/purchases/{id}/preview.jpg | Download purchase as jpeg |
| GET | /apps/{appId}/purchases/{id}/thumbnail.jpg | Show purchase thumbnail as jpeg |
| DELETE | /apps/{appId}/purchases/delete/all | Remove all purchases |
| POST | /apps/{appId}/purchases/mileage_allowances/create | Create a mileage allowance |
| POST | /apps/{appId}/purchases/mileage_allowances/{id}/duplicate | Duplicate an mileage allowance |
| GET | /apps/{appId}/purchases/mileage_allowances/resume | Resume of all mileage allowances for the current year + employee |
| POST | /apps/{appId}/purchases/mileage_allowances/{id} | Update a mileage allowance |
| POST | /apps/{appId}/purchases/create/demo | Create a fake purchase for test purpose |
| GET | /apps/{appId}/accounts/employees | Get accounting for all employees |
| POST | /apps/{appId}/accounts/employees | Create accounting for an employee |
| GET | /apps/{appId}/accounts/employees/{id} | Get account for an employee |
| POST | /apps/{appId}/accounts/employees/{id} | Update account for an employee |
| DELETE | /apps/{appId}/accounts/employees/{id} | Delete account for an employee |
| GET | /apps/{appId}/attachments | List attachments |
| POST | /apps/{appId}/attachments | Attach a file on an object |
| PUT | /apps/{appId}/attachments | Recreate S.A.P attestations |
| GET | /apps/{appId}/attachments/download | Download a list of attachments in pdf into a .zip file |
| GET | /apps/{appId}/attachments/sap-download | Download a list of SAP attestations in pdf into a .zip file |
| GET | /apps/{appId}/attachments/{id} | Get attachment by id |
| DELETE | /apps/{appId}/attachments/{id} | Detach a file from id |
| GET | /apps/{appId}/attachments/{id}/pdf | Download the attachment as pdf |
| GET | /apps/{appId}/products | List products |
| POST | /apps/{appId}/products | Create a product |
| POST | /apps/{appId}/products/batch | Create multiple products |
| DELETE | /apps/{appId}/products/batch | Delete many products |
| POST | /apps/{appId}/products/{id}/attach | Attach a file |
| DELETE | /apps/{appId}/products/{id}/attach | Detach a file |
| GET | /apps/{appId}/products/{id} | Get a product |
| POST | /apps/{appId}/products/{id} | Update a product |
| DELETE | /apps/{appId}/products/{id} | Remove a product |
| POST | /apps/{appId}/products/{id}/tag | Add a tag on a product |
| DELETE | /apps/{appId}/products/{id}/tag | Delete a tag on a product |
| DELETE | /apps/{appId}/products/delete/all | Remove all products |
| GET | /apps/{appId}/productstocks | List stocks |
| POST | /apps/{appId}/productstocks | Create a stocks |
| GET | /apps/{appId}/productstocks/{id} | Get a stocks |
| POST | /apps/{appId}/productstocks/{id} | Update a stocks |
| DELETE | /apps/{appId}/productstocks/{id} | Remove a stocks |
| POST | /apps/{appId}/productstocks/{id}/destruct | Destruct a quantity of stock (forgotten, destructed, expirated stock...) |
| POST | /apps/{appId}/productstocks/{id}/rental/exit | Consider part of the stock as rented |
| POST | /apps/{appId}/productstocks/{id}/rental/back | Consider part of the stock as back |
| GET | /apps/{appId}/productcategory | List product categories |
| POST | /apps/{appId}/productcategory | Create a product category |
| GET | /apps/{appId}/productcategory/{id} | Get a product category |
| POST | /apps/{appId}/productcategory/{id} | Update a product category |
| DELETE | /apps/{appId}/productcategory/{id} | Remove a product category |
| POST | /apps/{appId}/reconcile | Reconcile a transaction or a document |
| DELETE | /apps/{appId}/reconcile | Remove payments by an object |
| POST | /apps/{appId}/reconcile/batch | Reconcile several transactions |
| GET | /apps/{appId}/payments | List payments |
| GET | /apps/{appId}/payments/recipe_book | Get the recipe book |
| GET | /apps/{appId}/payments/{id} | Get a payment |
| DELETE | /apps/{appId}/payments/{id} | Remove a payment |
| GET | /apps/{appId}/sepamandates/directdebit | Preview sepa direct debit file |
| POST | /apps/{appId}/sepamandates/directdebit | Download sepa direct debit file |
| GET | /apps/{appId}/sepamandates/credittransfer | Preview sepa credit transfer file |
| POST | /apps/{appId}/sepamandates/credittransfer | Preview sepa credit transfer file |
| GET | /apps/{appId}/sepamandates/ | List SEPAMandate |
| POST | /apps/{appId}/sepamandates/ | Create a SEPAMandate |
| GET | /apps/{appId}/sepamandates/{id} | Get a SEPAMandate |
| POST | /apps/{appId}/sepamandates/{id} | Update a SEPAMandate |
| DELETE | /apps/{appId}/sepamandates/{id} | Remove a SEPAMandate |
| GET | /apps/{appId}/urssaf/preview | Preview URSSAF request payment |
| POST | /apps/{appId}/urssaf/auth | Login URSSAF |
| POST | /apps/{appId}/urssaf/register_customer | Register a person to URSSAF and create him a mandate |
| POST | /apps/{appId}/urssaf/customer | Get person informations |
| GET | /apps/{appId}/urssaf/payment | Get status of a payment |
| POST | /apps/{appId}/urssaf/payment | Send URSSAF request payment |
| GET | /apps/{appId}/banks/ | List banks connected to bankin |
| DELETE | /apps/{appId}/banks/ | Remove a Bankin synchronization |
| GET | /apps/{appId}/banks/connect | Get the link to the funnel to connect a bank with Sinao |
| POST | /apps/{appId}/banks/synchronize | Triggers synchronization at Bankin then synchronizes transactions with Sinao |
| GET | /apps/{appId}/banks/{id}/funnel/sync | Get the link to the funnel to start manually a synchronization (SCA) |
| GET | /apps/{appId}/banks/{id}/funnel/edit | Get the link to the funnel to edit password |
| GET | /apps/{appId}/banks/{id}/funnel/validate | Get the link to the funnel to validate a pro item (SCA) |
| POST | /apps/{appId}/banks/{id}/select_accounts | Select accounts to synchronize |
| GET | /apps/{appId}/cashflowsources/ | List CashflowSource |
| POST | /apps/{appId}/cashflowsources/ | Create a CashflowSource |
| GET | /apps/{appId}/cashflowsources/{id} | Get a CashflowSource |
| POST | /apps/{appId}/cashflowsources/{id} | Update a CashflowSource |
| DELETE | /apps/{appId}/cashflowsources/{id} | Remove a CashflowSource |
| GET | /apps/{appId}/logs/autoreconcile/ | List autoreconciliation logs |
| POST | /apps/{appId}/logs/autoreconcile/ | Start force autoreconciliation |
| DELETE | /apps/{appId}/logs/autoreconcile/ | Clear autoreconciliation logs |
| GET | /apps/{appId}/transactions/ | List Transaction |
| POST | /apps/{appId}/transactions/ | Create a Transaction |
| POST | /apps/{appId}/transactions/batch | Create multiple transactions |
| DELETE | /apps/{appId}/transactions/batch | Delete many transactions |
| POST | /apps/{appId}/transactions/{id}/attach | Attach a file |
| DELETE | /apps/{appId}/transactions/{id}/attach | Detach a file |
| GET | /apps/{appId}/transactions/{id} | Get a Transaction |
| POST | /apps/{appId}/transactions/{id} | Update a Transaction |
| DELETE | /apps/{appId}/transactions/{id} | Remove a Transaction |
| POST | /apps/{appId}/transactions/{id}/tag | Add a tag on a transaction |
| DELETE | /apps/{appId}/transactions/{id}/tag | Delete a tag on a transaction |
| GET | /apps/{appId}/rules/ | List rules |
| POST | /apps/{appId}/rules/ | Create a rule |
| POST | /apps/{appId}/rules/execute_on | Execute all rules |
| GET | /apps/{appId}/rules/{id} | Get a rule |
| POST | /apps/{appId}/rules/{id} | Update a rule |
| DELETE | /apps/{appId}/rules/{id} | Remove a rule |
| GET | /apps/{appId}/accounts/ | List Account |
| POST | /apps/{appId}/accounts/ | Create a Account |
| POST | /apps/{appId}/accounts/batch | Create many accounts |
| DELETE | /apps/{appId}/accounts/batch | Remove multiple accounting accounts |
| GET | /apps/{appId}/accounts/{id} | Get a Account |
| POST | /apps/{appId}/accounts/{id} | Update a Account |
| DELETE | /apps/{appId}/accounts/{id} | Remove a Account |
| POST | /apps/{appId}/accounts/{delete_account_id}/replace | Delete an account and replace relatives by replacement account id |
| GET | /apps/{appId}/forecast/elements | Get all forecast elements |
| POST | /apps/{appId}/forecast/elements | Create a forecast element |
| DELETE | /apps/{appId}/forecast/elements | Remove a forecast element |
| POST | /apps/{appId}/forecast/elements/{id} | Create a forecast element |
| DELETE | /apps/{appId}/forecast/elements/{id} | Remove a forecast element |
| GET | /apps/{appId}/forecast/turnover | Get all sales_lines grouped by account |
| GET | /apps/{appId}/forecast/expenditures | Get all sales_lines grouped by account |
| GET | /apps/{appId}/forecast/payments | Get all sales_lines grouped by account |
| GET | /apps/{appId}/forecast/average/payment | Get supplier and customer average payment period |
| GET | /apps/{appId}/forecast/transactions | Get all transactions grouped by account |
| GET | /apps/{appId}/forecast/pourcentages/budgets | Calculate pourcentages budgets for all categories |
| GET | /apps/{appId}/forecast/invoices/unpaid | Calculate pourcentages budgets for all categories |
| GET | /apps/{appId}/forecast/purchases/unpaid | Calculate pourcentages budgets for all categories |
| GET | /apps/{appId}/accountcategories/ | List categories |
| POST | /apps/{appId}/accountcategories/ | Create a category |
| GET | /apps/{appId}/accountcategories/{id} | Get a category |
| POST | /apps/{appId}/accountcategories/{id} | Update a category |
| DELETE | /apps/{appId}/accountcategories/{id} | Remove a category |
| GET | /apps/{appId}/exports | List ExportEntity |
| POST | /apps/{appId}/exports | Create a ExportEntity |
| GET | /apps/{appId}/exports/months | List ExportEntity |
| GET | /apps/{appId}/exports/acd_compta | Get the ACD UUID for authentification |
| POST | /apps/{appId}/exports/acd_compta | Register ACD identifiants |
| POST | /apps/{appId}/exports/acd_compta/filenumber | Set ACD file number |
| GET | /apps/{appId}/exports/agiris | Get your Agiris file code |
| POST | /apps/{appId}/exports/agiris | Register Agiris file code |
| GET | /apps/{appId}/exports/download | Download the export entity as zip |
| GET | /apps/{appId}/exports/download/{export_id} | Download the export entity as zip |
| GET | /apps/{appId}/exports/{id} | Get a ExportEntity |
| DELETE | /apps/{appId}/exports/{id} | Remove a ExportEntity |
| GET | /apps/{appId}/accounting_entries/ | List accounting entries |
| GET | /apps/{appId}/statistics/vat | Obtain statistics about vat |
| GET | /apps/{appId}/statistics/timetable/sales | Obtain statistics about sales |
| GET | /apps/{appId}/statistics/timetable/purchases | Obtain statistics about timetable purchases |
| GET | /apps/{appId}/statistics/charts/{type} | Obtain statistics about everything |
| GET | /apps/{appId}/declare/vat | Obtain the url of Teledec declaration page redirection |
| POST | /apps/{appId}/declare/vat | register Vat declaration settings |
| GET | /apps/{appId}/tags | Get all existants tags |
| POST | /apps/{appId}/supplier/accepted | Accept a supplier |
| POST | /apps/{appId}/supplier/accepted/invoice | Accepted to add only this invoice |
| POST | /apps/{appId}/signature | Create a signature |
| GET | /apps/{appId}/services/stripe/webhook | Ping Stripe webhook endpoint |
| POST | /apps/{appId}/services/stripe/webhook | Webhook for Stripe |
| POST | /apps/{appId}/services/yousign/webhook | Webhook for Yousign |
| POST | /apps/{appId}/sponsorship/invite | Send an email |
| POST | /apps/{appId}/sponsorship/activate | Activate the invitation for sponsorship |
| GET | /apps/{appId}/sponsorship/list/referrals | Get all referrals for a referrer |
| GET | /apps/{appId}/sponsorship/referrer | Get the referrer information for my app |
| GET | /apps/{appId}/sponsorship/referrer/url | Get the referrer url for my app |
| POST | /apps/{appId}/sponsorship/accept/referrer | Verify if the referrer code is valid |
| GET | /apps/{appId}/sponsorship/credit | Get the credit for my app |
| POST | /apps/{appId}/stripe/import/launch | Launch the import of Stripe data |
| GET | /apps/{appId}/stripe/import/status | Get the import status of Stripe data |
| GET | /apps/{appId}/stripe/import/state | Get the import state of Stripe data |
| GET | /apps/{appId}/openai/billing/estimate | Get the import state of Stripe data |
| GET | /apps/{appId}/openai/billing/reformulate | Get the reformulate for a designation |
| GET | /apps/{appId}/openai/billing/corrector | Get the smart corrector for a designation |
| POST | /apps/{appId}/openai/accounting/suggest | Suggest an accounting account from a free-text description using AI |
| POST | /apps/{appId}/paypal/connect/{clientId} | Connect to Paypal |
| GET | /apps/{appId}/paypal/connect/state | Get if app is connect to Paypal |
| GET | /apps/{appId}/paypal/connect/delete | Delete synchronisation paypal |
| GET | /apps/{appId}/webhooks/events | Get all events |

### invoice
| Method | Path | Description |
|--------|------|-------------|
| GET | /invoice/token-validation/ | Validate an invoice token |
| GET | /invoice/download/fec/{token} | Download .fec invoice |
| GET | /invoice/download/pdf/{token} | Download pdf invoice |

### ping
| Method | Path | Description |
|--------|------|-------------|
| GET | /ping | Ping server |

### services
| Method | Path | Description |
|--------|------|-------------|
| POST | /services/collector | Push to purchase collector |
| GET | /services/vies/{siren} | Get VIES database informations from SIREN |

### partners
| Method | Path | Description |
|--------|------|-------------|
| POST | /partners/{partnerId}/clients/login | Login a client |
| GET | /partners/{partnerId} | Get partner information |
| GET | /partners/{partnerId}/cases | Get all cases for a partner |
| GET | /partners/{partnerId}/apps/{app_id}/apikey | Get or create a apikey for a app inside partner case |
| GET | /partners/{partnerId}/plans | Get all plans for a partner |
| POST | /partners/{partnerId}/subscriptions/{app_id}/update | Update a subscription |
| POST | /partners/{partnerId}/subscriptions/{app_id}/cancel | Cancel a subscription |
| DELETE | /partners/{partnerId}/delete/cases | Delete apps inside a partner scope |
| POST | /partners/{partnerId}/dissociate/cases | Dissociate apps from a partner |
| POST | /partners/{partnerId}/add/collaborator | Add a collaborator to an app |
| GET | /partners/{partnerId}/collaborators | Get all collaborators for a partner |
| DELETE | /partners/{partnerId}/collaborators/{id} | Delete a collaborator for a partner |
| POST | /partners/{partnerId}/assign/collaborators/{id} | Affecter un collaborateur à un partenaire |
| POST | /partners/{partnerId}/collaborators/{id}/update | Update a collaborator profile for a partner |
| POST | /partners/{partnerId}/user/accept/invite | User accept an invite 'Support Technique' on this app |
| POST | /partners/{partnerId}/add/policy | Add a user policy to an app (make by partner) |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a login?" -> POST /login
- "Create a sendpassword?" -> POST /sendpassword
- "Create a changepassword?" -> POST /changepassword
- "Create a logout?" -> POST /logout
- "Create a 2fa?" -> POST /login/send/2fa
- "List all refresh?" -> GET /refresh
- "List all me?" -> GET /me
- "Create a me?" -> POST /me
- "Create a register?" -> POST /register
- "Create a app?" -> POST /apps
- "Search apps?" -> GET /apps
- "Get app details?" -> GET /apps/{appId}
- "List all ping?" -> GET /apps/{appId}/ping
- "Create a reset?" -> POST /apps/{appId}/reset
- "Search apikeys?" -> GET /apps/{appId}/apikeys
- "Create a apikey?" -> POST /apps/{appId}/apikeys
- "Delete a apikey?" -> DELETE /apps/{appId}/apikeys/{id}
- "Search apipartners?" -> GET /apps/{appId}/apipartners
- "List all settings?" -> GET /apps/{appId}/settings
- "Create a setting?" -> POST /apps/{appId}/settings
- "Get job details?" -> GET /apps/{appId}/jobs/{job}
- "List all templates?" -> GET /apps/{appId}/templates
- "Create a template?" -> POST /apps/{appId}/templates
- "List all document-langs?" -> GET /apps/{appId}/document-langs
- "Create a batch?" -> POST /apps/{appId}/templates/batch
- "List all default?" -> GET /apps/{appId}/templates/default
- "Get template details?" -> GET /apps/{appId}/templates/{id}
- "List all extra?" -> GET /apps/{appId}/subscription/plan/extra
- "List all customer?" -> GET /apps/{appId}/subscription/customer
- "Create a customer?" -> POST /apps/{appId}/subscription/customer
- "List all plan?" -> GET /apps/{appId}/subscription/plan
- "List all plans?" -> GET /apps/{appId}/subscription/plans
- "List all invoices?" -> GET /apps/{appId}/subscription/invoices
- "List all payment_methods?" -> GET /apps/{appId}/subscription/payment_methods
- "List all count?" -> GET /apps/{appId}/subscription/extra/count
- "Get plan details?" -> GET /apps/{appId}/subscription/plans/{stripe_plan}
- "List all checkout?" -> GET /apps/{appId}/subscription/plans/{stripe_plan}/checkout
- "List all checkout_session?" -> GET /apps/{appId}/subscription/checkout_session
- "List all checkout_add_source?" -> GET /apps/{appId}/subscription/checkout_add_source
- "Create a source?" -> POST /apps/{appId}/subscription/source
- "Create a default?" -> POST /apps/{appId}/subscription/source/default
- "Create a pay_all?" -> POST /apps/{appId}/subscription/pay_all
- "Create a cancel?" -> POST /apps/{appId}/subscription/cancel
- "Create a extend_trial?" -> POST /apps/{appId}/subscription/extend_trial
- "Create a coupon?" -> POST /apps/{appId}/subscription/coupon
- "List all coupon?" -> GET /apps/{appId}/subscription/coupon
- "Create a anchordate?" -> POST /apps/{appId}/subscription/anchordate
- "List all profiles?" -> GET /apps/{appId}/access/profiles
- "Create a invite?" -> POST /apps/{appId}/access/invite
- "Search invite?" -> GET /apps/{appId}/access/invite
- "Delete a invite?" -> DELETE /apps/{appId}/access/invite/{id}
- "List all refresh-token?" -> GET /apps/{appId}/pennylane/refresh-token
- "Create a register?" -> POST /apps/access/invite/{accessToken}/register
- "Get invite details?" -> GET /apps/access/invite/{accessToken}
- "Delete a invite?" -> DELETE /apps/access/invite/{accessToken}
- "Create a batch?" -> POST /apps/access/accounting/policies/accounting/batch
- "Search access?" -> GET /apps/{appId}/access
- "Get access details?" -> GET /apps/{appId}/access/{userId}
- "Delete a access?" -> DELETE /apps/{appId}/access/{userId}
- "List all organization?" -> GET /apps/{appId}/organization
- "Create a organization?" -> POST /apps/{appId}/organization
- "Search organizations?" -> GET /apps/{appId}/organizations
- "Create a organization?" -> POST /apps/{appId}/organizations
- "Create a batch?" -> POST /apps/{appId}/organizations/batch
- "Create a chorus-search?" -> POST /apps/{appId}/organizations/chorus-search
- "Get organization details?" -> GET /apps/{appId}/organizations/{id}
- "Delete a organization?" -> DELETE /apps/{appId}/organizations/{id}
- "List all restore?" -> GET /apps/{appId}/organizations/{id}/restore
- "List all mandate?" -> GET /apps/{appId}/organizations/{id}/sepa/mandate
- "Search persons?" -> GET /apps/{appId}/persons
- "Create a person?" -> POST /apps/{appId}/persons
- "Create a batch?" -> POST /apps/{appId}/persons/batch
- "Get person details?" -> GET /apps/{appId}/persons/{id}
- "Delete a person?" -> DELETE /apps/{appId}/persons/{id}
- "List all restore?" -> GET /apps/{appId}/persons/{id}/restore
- "List all mandate?" -> GET /apps/{appId}/persons/{id}/sepa/mandate
- "Get establishment details?" -> GET /apps/{appId}/establishments/{id}
- "Delete a establishment?" -> DELETE /apps/{appId}/establishments/{id}
- "Delete a contact?" -> DELETE /apps/{appId}/establishments/{establishment_id}/contact/{contact_id}
- "Search relationships?" -> GET /apps/{appId}/relationships
- "Create a attach?" -> POST /apps/{appId}/relationships/{id}/attach
- "Get relationship details?" -> GET /apps/{appId}/relationships/{id}
- "Create a tag?" -> POST /apps/{appId}/relationships/{id}/tag
- "Create a merge?" -> POST /apps/{appId}/contacts/merge
- "Search invoices?" -> GET /apps/{appId}/invoices
- "Create a invoice?" -> POST /apps/{appId}/invoices
- "Create a batch?" -> POST /apps/{appId}/invoices/batch
- "List all nextnumber?" -> GET /apps/{appId}/invoices/nextnumber
- "List all download?" -> GET /apps/{appId}/invoices/download
- "Search statistics?" -> GET /apps/{appId}/invoices/statistics
- "Create a fresh?" -> POST /apps/{appId}/invoices/fresh
- "Create a chorus-pro?" -> POST /apps/{appId}/invoices/chorus-pro
- "Get invoice details?" -> GET /apps/{appId}/invoices/{id}
- "Delete a invoice?" -> DELETE /apps/{appId}/invoices/{id}
- "Create a duplicate?" -> POST /apps/{appId}/invoices/{id}/duplicate
- "Create a avoid?" -> POST /apps/{appId}/invoices/{id}/avoid
- "Create a finalize?" -> POST /apps/{appId}/invoices/{id}/finalize
- "Create a updatestatus?" -> POST /apps/{appId}/invoices/{id}/updatestatus
- "Create a attach?" -> POST /apps/{appId}/invoices/{id}/attach
- "Create a tag?" -> POST /apps/{appId}/invoices/{id}/tag
- "List all pdf?" -> GET /apps/{appId}/invoices/{id}/pdf
- "List all preview.jpg?" -> GET /apps/{appId}/invoices/{id}/preview.jpg
- "List all link?" -> GET /apps/{appId}/invoice/{id}/link
- "Create a breakdown?" -> POST /apps/{appId}/invoices/batch/breakdown
- "List all token-validation?" -> GET /invoice/token-validation/
- "Get fec details?" -> GET /invoice/download/fec/{token}
- "Get pdf details?" -> GET /invoice/download/pdf/{token}
- "Search quotes?" -> GET /apps/{appId}/quotes
- "Create a quote?" -> POST /apps/{appId}/quotes
- "Create a batch?" -> POST /apps/{appId}/quotes/batch
- "Create a invoice?" -> POST /apps/{appId}/quotes/invoice
- "List all nextnumber?" -> GET /apps/{appId}/quotes/nextnumber
- "List all download?" -> GET /apps/{appId}/quotes/download
- "Search statistics?" -> GET /apps/{appId}/quotes/statistics
- "Create a fresh?" -> POST /apps/{appId}/quotes/fresh
- "Get quote details?" -> GET /apps/{appId}/quotes/{id}
- "Delete a quote?" -> DELETE /apps/{appId}/quotes/{id}
- "Create a finalize?" -> POST /apps/{appId}/quotes/{id}/finalize
- "Create a duplicate?" -> POST /apps/{appId}/quotes/{id}/duplicate
- "Create a invoice?" -> POST /apps/{appId}/quotes/{id}/invoice
- "Create a situation_invoice?" -> POST /apps/{appId}/quotes/{id}/situation_invoice
- "Create a downpayment?" -> POST /apps/{appId}/quotes/{id}/downpayment
- "Create a updatestatus?" -> POST /apps/{appId}/quotes/{id}/updatestatus
- "Create a attach?" -> POST /apps/{appId}/quotes/{id}/attach
- "Create a tag?" -> POST /apps/{appId}/quotes/{id}/tag
- "List all pdf?" -> GET /apps/{appId}/quotes/{id}/pdf
- "List all preview.jpg?" -> GET /apps/{appId}/quotes/{id}/preview.jpg
- "List all preview.jpg?" -> GET /apps/{appId}/quotes/{id}/yousign/preview.jpg
- "Create a breakdown?" -> POST /apps/{appId}/quotes/batch/breakdown
- "Search salesdocumentmodels?" -> GET /apps/{appId}/salesdocumentmodels
- "Create a salesdocumentmodel?" -> POST /apps/{appId}/salesdocumentmodels
- "Get salesdocumentmodel details?" -> GET /apps/{appId}/salesdocumentmodels/{id}
- "Delete a salesdocumentmodel?" -> DELETE /apps/{appId}/salesdocumentmodels/{id}
- "Search recurringinvoices?" -> GET /apps/{appId}/recurringinvoices
- "Create a recurringinvoice?" -> POST /apps/{appId}/recurringinvoices
- "Create a batch?" -> POST /apps/{appId}/recurringinvoices/batch
- "List all periods?" -> GET /apps/{appId}/recurringinvoices/periods
- "Get recurringinvoice details?" -> GET /apps/{appId}/recurringinvoices/{id}
- "Delete a recurringinvoice?" -> DELETE /apps/{appId}/recurringinvoices/{id}
- "List all plan?" -> GET /apps/{appId}/recurringinvoices/{id}/plan
- "Search bankdetails?" -> GET /apps/{appId}/bankdetails
- "Create a bankdetail?" -> POST /apps/{appId}/bankdetails
- "Get bankdetail details?" -> GET /apps/{appId}/bankdetails/{id}
- "Delete a bankdetail?" -> DELETE /apps/{appId}/bankdetails/{id}
- "Create a document?" -> POST /apps/{appId}/email/document
- "Create a batch?" -> POST /apps/{appId}/email/batch
- "Get document details?" -> GET /apps/{appId}/email/document/{id}
- "Search purchases?" -> GET /apps/{appId}/purchases
- "Create a purchase?" -> POST /apps/{appId}/purchases
- "Search statistics?" -> GET /apps/{appId}/purchases/statistics
- "Create a batch?" -> POST /apps/{appId}/purchases/batch
- "List all download?" -> GET /apps/{appId}/purchases/download
- "Get purchase details?" -> GET /apps/{appId}/purchases/{id}
- "Delete a purchase?" -> DELETE /apps/{appId}/purchases/{id}
- "Create a updatestatus?" -> POST /apps/{appId}/purchases/{id}/updatestatus
- "Create a attach?" -> POST /apps/{appId}/purchases/{id}/attach
- "Create a tag?" -> POST /apps/{appId}/purchases/{id}/tag
- "List all original?" -> GET /apps/{appId}/purchases/{id}/original
- "List all preview.jpg?" -> GET /apps/{appId}/purchases/{id}/preview.jpg
- "List all thumbnail.jpg?" -> GET /apps/{appId}/purchases/{id}/thumbnail.jpg
- "Create a create?" -> POST /apps/{appId}/purchases/mileage_allowances/create
- "Create a duplicate?" -> POST /apps/{appId}/purchases/mileage_allowances/{id}/duplicate
- "List all resume?" -> GET /apps/{appId}/purchases/mileage_allowances/resume
- "Create a demo?" -> POST /apps/{appId}/purchases/create/demo
- "Search employees?" -> GET /apps/{appId}/accounts/employees
- "Create a employee?" -> POST /apps/{appId}/accounts/employees
- "Get employee details?" -> GET /apps/{appId}/accounts/employees/{id}
- "Delete a employee?" -> DELETE /apps/{appId}/accounts/employees/{id}
- "Search attachments?" -> GET /apps/{appId}/attachments
- "Create a attachment?" -> POST /apps/{appId}/attachments
- "List all download?" -> GET /apps/{appId}/attachments/download
- "List all sap-download?" -> GET /apps/{appId}/attachments/sap-download
- "Get attachment details?" -> GET /apps/{appId}/attachments/{id}
- "Delete a attachment?" -> DELETE /apps/{appId}/attachments/{id}
- "List all pdf?" -> GET /apps/{appId}/attachments/{id}/pdf
- "Search products?" -> GET /apps/{appId}/products
- "Create a product?" -> POST /apps/{appId}/products
- "Create a batch?" -> POST /apps/{appId}/products/batch
- "Create a attach?" -> POST /apps/{appId}/products/{id}/attach
- "Get product details?" -> GET /apps/{appId}/products/{id}
- "Delete a product?" -> DELETE /apps/{appId}/products/{id}
- "Create a tag?" -> POST /apps/{appId}/products/{id}/tag
- "Search productstocks?" -> GET /apps/{appId}/productstocks
- "Create a productstock?" -> POST /apps/{appId}/productstocks
- "Get productstock details?" -> GET /apps/{appId}/productstocks/{id}
- "Delete a productstock?" -> DELETE /apps/{appId}/productstocks/{id}
- "Create a destruct?" -> POST /apps/{appId}/productstocks/{id}/destruct
- "Create a exit?" -> POST /apps/{appId}/productstocks/{id}/rental/exit
- "Create a back?" -> POST /apps/{appId}/productstocks/{id}/rental/back
- "Search productcategory?" -> GET /apps/{appId}/productcategory
- "Create a productcategory?" -> POST /apps/{appId}/productcategory
- "Get productcategory details?" -> GET /apps/{appId}/productcategory/{id}
- "Delete a productcategory?" -> DELETE /apps/{appId}/productcategory/{id}
- "Create a reconcile?" -> POST /apps/{appId}/reconcile
- "Create a batch?" -> POST /apps/{appId}/reconcile/batch
- "Search payments?" -> GET /apps/{appId}/payments
- "List all recipe_book?" -> GET /apps/{appId}/payments/recipe_book
- "Get payment details?" -> GET /apps/{appId}/payments/{id}
- "Delete a payment?" -> DELETE /apps/{appId}/payments/{id}
- "List all directdebit?" -> GET /apps/{appId}/sepamandates/directdebit
- "Create a directdebit?" -> POST /apps/{appId}/sepamandates/directdebit
- "List all credittransfer?" -> GET /apps/{appId}/sepamandates/credittransfer
- "Create a credittransfer?" -> POST /apps/{appId}/sepamandates/credittransfer
- "Search sepamandates?" -> GET /apps/{appId}/sepamandates/
- "Create a sepamandate?" -> POST /apps/{appId}/sepamandates/
- "Get sepamandate details?" -> GET /apps/{appId}/sepamandates/{id}
- "Delete a sepamandate?" -> DELETE /apps/{appId}/sepamandates/{id}
- "List all preview?" -> GET /apps/{appId}/urssaf/preview
- "Create a auth?" -> POST /apps/{appId}/urssaf/auth
- "Create a register_customer?" -> POST /apps/{appId}/urssaf/register_customer
- "Create a customer?" -> POST /apps/{appId}/urssaf/customer
- "List all payment?" -> GET /apps/{appId}/urssaf/payment
- "Create a payment?" -> POST /apps/{appId}/urssaf/payment
- "List all banks?" -> GET /apps/{appId}/banks/
- "List all connect?" -> GET /apps/{appId}/banks/connect
- "Create a synchronize?" -> POST /apps/{appId}/banks/synchronize
- "List all sync?" -> GET /apps/{appId}/banks/{id}/funnel/sync
- "List all edit?" -> GET /apps/{appId}/banks/{id}/funnel/edit
- "List all validate?" -> GET /apps/{appId}/banks/{id}/funnel/validate
- "Create a select_account?" -> POST /apps/{appId}/banks/{id}/select_accounts
- "Search cashflowsources?" -> GET /apps/{appId}/cashflowsources/
- "Create a cashflowsource?" -> POST /apps/{appId}/cashflowsources/
- "Get cashflowsource details?" -> GET /apps/{appId}/cashflowsources/{id}
- "Delete a cashflowsource?" -> DELETE /apps/{appId}/cashflowsources/{id}
- "Search autoreconcile?" -> GET /apps/{appId}/logs/autoreconcile/
- "Create a autoreconcile?" -> POST /apps/{appId}/logs/autoreconcile/
- "Search transactions?" -> GET /apps/{appId}/transactions/
- "Create a transaction?" -> POST /apps/{appId}/transactions/
- "Create a batch?" -> POST /apps/{appId}/transactions/batch
- "Create a attach?" -> POST /apps/{appId}/transactions/{id}/attach
- "Get transaction details?" -> GET /apps/{appId}/transactions/{id}
- "Delete a transaction?" -> DELETE /apps/{appId}/transactions/{id}
- "Create a tag?" -> POST /apps/{appId}/transactions/{id}/tag
- "Search rules?" -> GET /apps/{appId}/rules/
- "Create a rule?" -> POST /apps/{appId}/rules/
- "Create a execute_on?" -> POST /apps/{appId}/rules/execute_on
- "Get rule details?" -> GET /apps/{appId}/rules/{id}
- "Delete a rule?" -> DELETE /apps/{appId}/rules/{id}
- "Search accounts?" -> GET /apps/{appId}/accounts/
- "Create a account?" -> POST /apps/{appId}/accounts/
- "Create a batch?" -> POST /apps/{appId}/accounts/batch
- "Get account details?" -> GET /apps/{appId}/accounts/{id}
- "Delete a account?" -> DELETE /apps/{appId}/accounts/{id}
- "Create a replace?" -> POST /apps/{appId}/accounts/{delete_account_id}/replace
- "Search elements?" -> GET /apps/{appId}/forecast/elements
- "Create a element?" -> POST /apps/{appId}/forecast/elements
- "Delete a element?" -> DELETE /apps/{appId}/forecast/elements/{id}
- "List all turnover?" -> GET /apps/{appId}/forecast/turnover
- "List all expenditures?" -> GET /apps/{appId}/forecast/expenditures
- "List all payments?" -> GET /apps/{appId}/forecast/payments
- "List all payment?" -> GET /apps/{appId}/forecast/average/payment
- "List all transactions?" -> GET /apps/{appId}/forecast/transactions
- "List all budgets?" -> GET /apps/{appId}/forecast/pourcentages/budgets
- "List all unpaid?" -> GET /apps/{appId}/forecast/invoices/unpaid
- "List all unpaid?" -> GET /apps/{appId}/forecast/purchases/unpaid
- "Search accountcategories?" -> GET /apps/{appId}/accountcategories/
- "Create a accountcategory?" -> POST /apps/{appId}/accountcategories/
- "Get accountcategory details?" -> GET /apps/{appId}/accountcategories/{id}
- "Delete a accountcategory?" -> DELETE /apps/{appId}/accountcategories/{id}
- "Search exports?" -> GET /apps/{appId}/exports
- "Create a export?" -> POST /apps/{appId}/exports
- "List all months?" -> GET /apps/{appId}/exports/months
- "List all acd_compta?" -> GET /apps/{appId}/exports/acd_compta
- "Create a acd_compta?" -> POST /apps/{appId}/exports/acd_compta
- "Create a filenumber?" -> POST /apps/{appId}/exports/acd_compta/filenumber
- "List all agiris?" -> GET /apps/{appId}/exports/agiris
- "Create a agiris?" -> POST /apps/{appId}/exports/agiris
- "List all download?" -> GET /apps/{appId}/exports/download
- "Get download details?" -> GET /apps/{appId}/exports/download/{export_id}
- "Get export details?" -> GET /apps/{appId}/exports/{id}
- "Delete a export?" -> DELETE /apps/{appId}/exports/{id}
- "Search accounting_entries?" -> GET /apps/{appId}/accounting_entries/
- "List all vat?" -> GET /apps/{appId}/statistics/vat
- "List all sales?" -> GET /apps/{appId}/statistics/timetable/sales
- "List all purchases?" -> GET /apps/{appId}/statistics/timetable/purchases
- "Search charts?" -> GET /apps/{appId}/statistics/charts/{type}
- "List all vat?" -> GET /apps/{appId}/declare/vat
- "Create a vat?" -> POST /apps/{appId}/declare/vat
- "List all tags?" -> GET /apps/{appId}/tags
- "Create a accepted?" -> POST /apps/{appId}/supplier/accepted
- "Create a invoice?" -> POST /apps/{appId}/supplier/accepted/invoice
- "Create a signature?" -> POST /apps/{appId}/signature
- "List all ping?" -> GET /ping
- "List all webhook?" -> GET /apps/{appId}/services/stripe/webhook
- "Create a webhook?" -> POST /apps/{appId}/services/stripe/webhook
- "Create a collector?" -> POST /services/collector
- "Get vy details?" -> GET /services/vies/{siren}
- "Create a webhook?" -> POST /apps/{appId}/services/yousign/webhook
- "Create a invite?" -> POST /apps/{appId}/sponsorship/invite
- "Create a activate?" -> POST /apps/{appId}/sponsorship/activate
- "List all referrals?" -> GET /apps/{appId}/sponsorship/list/referrals
- "List all referrer?" -> GET /apps/{appId}/sponsorship/referrer
- "List all url?" -> GET /apps/{appId}/sponsorship/referrer/url
- "Create a referrer?" -> POST /apps/{appId}/sponsorship/accept/referrer
- "List all credit?" -> GET /apps/{appId}/sponsorship/credit
- "Create a launch?" -> POST /apps/{appId}/stripe/import/launch
- "List all status?" -> GET /apps/{appId}/stripe/import/status
- "List all state?" -> GET /apps/{appId}/stripe/import/state
- "List all estimate?" -> GET /apps/{appId}/openai/billing/estimate
- "List all reformulate?" -> GET /apps/{appId}/openai/billing/reformulate
- "List all corrector?" -> GET /apps/{appId}/openai/billing/corrector
- "Create a suggest?" -> POST /apps/{appId}/openai/accounting/suggest
- "List all state?" -> GET /apps/{appId}/paypal/connect/state
- "List all delete?" -> GET /apps/{appId}/paypal/connect/delete
- "Search events?" -> GET /apps/{appId}/webhooks/events
- "Create a login?" -> POST /partners/{partnerId}/clients/login
- "Get partner details?" -> GET /partners/{partnerId}
- "Search cases?" -> GET /partners/{partnerId}/cases
- "List all apikey?" -> GET /partners/{partnerId}/apps/{app_id}/apikey
- "List all plans?" -> GET /partners/{partnerId}/plans
- "Create a update?" -> POST /partners/{partnerId}/subscriptions/{app_id}/update
- "Create a cancel?" -> POST /partners/{partnerId}/subscriptions/{app_id}/cancel
- "Create a case?" -> POST /partners/{partnerId}/dissociate/cases
- "Create a collaborator?" -> POST /partners/{partnerId}/add/collaborator
- "Search collaborators?" -> GET /partners/{partnerId}/collaborators
- "Delete a collaborator?" -> DELETE /partners/{partnerId}/collaborators/{id}
- "Create a update?" -> POST /partners/{partnerId}/collaborators/{id}/update
- "Create a invite?" -> POST /partners/{partnerId}/user/accept/invite
- "Create a policy?" -> POST /partners/{partnerId}/add/policy
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
