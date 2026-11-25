---
name: the-plaid-api
description: "The Plaid API skill. Use when working with The Plaid for asset_report, cra, credit. Covers 325 endpoints."
version: 1.0.0
generator: lapsh
---

# The Plaid API
API version: 2020-09-14_1.681.5

## Auth
ApiKey PLAID-CLIENT-ID in header | ApiKey PLAID-SECRET in header | ApiKey Plaid-Version in header

## Base URL
https://production.plaid.com

## Setup
1. Set your API key in the appropriate header
2. GET /fdx/recipients -- verify access
3. POST /asset_report/create -- create first create

## Endpoints

325 endpoints across 48 groups. See references/api-spec.lap for full details.

### asset_report
| Method | Path | Description |
|--------|------|-------------|
| POST | /asset_report/create | Create an Asset Report |
| POST | /asset_report/get | Retrieve an Asset Report |
| POST | /asset_report/pdf/get | Retrieve a PDF Asset Report |
| POST | /asset_report/refresh | Refresh an Asset Report |
| POST | /asset_report/filter | Filter Asset Report |
| POST | /asset_report/remove | Delete an Asset Report |
| POST | /asset_report/audit_copy/create | Create Asset Report Audit Copy |
| POST | /asset_report/audit_copy/get | Retrieve an Asset Report Audit Copy |
| POST | /asset_report/audit_copy/pdf/get | Retrieve a PDF Asset Report Audit Copy |
| POST | /asset_report/audit_copy/remove | Remove Asset Report Audit Copy |

### cra
| Method | Path | Description |
|--------|------|-------------|
| POST | /cra/monitoring_insights/subscribe | Subscribe to Monitoring Insights |
| POST | /cra/monitoring_insights/unsubscribe | Unsubscribe from Monitoring Insights |
| POST | /cra/monitoring_insights/get | Retrieve a Monitoring Insights Report |
| POST | /cra/partner_insights/get | Retrieve cash flow insights from the bank accounts used for income verification |
| POST | /cra/check_report/income_insights/get | Retrieve cash flow information from your user's banks |
| POST | /cra/check_report/base_report/get | Retrieve a Base Report |
| POST | /cra/check_report/pdf/get | Retrieve Consumer Reports as a PDF |
| POST | /cra/check_report/create | Refresh or create a Consumer Report |
| POST | /cra/check_report/partner_insights/get | Retrieve cash flow insights from partners |
| POST | /cra/check_report/cashflow_insights/get | Retrieve cash flow insights from your user's banking data |
| POST | /cra/check_report/lend_score/get | Retrieve the LendScore from your user's banking data |
| POST | /cra/check_report/network_insights/get | Retrieve network attributes for the user |
| POST | /cra/check_report/verification/get | Retrieve various home lending reports for a user. |
| POST | /cra/check_report/verification/pdf/get | Retrieve Consumer Reports as a Verification PDF |
| POST | /cra/loans/applications/register | Register loan applications and decisions. |
| POST | /cra/loans/register | Register a list of loans to their applicants. |
| POST | /cra/loans/update | Updates loan data. |
| POST | /cra/loans/unregister | Unregister a list of loans. |

### credit
| Method | Path | Description |
|--------|------|-------------|
| POST | /credit/audit_copy_token/update | Update an Audit Copy Token |
| POST | /credit/sessions/get | Retrieve Link sessions for your user |
| POST | /credit/audit_copy_token/create | Create Asset or Income Report Audit Copy Token |
| POST | /credit/audit_copy_token/remove | Remove an Audit Copy token |
| POST | /credit/asset_report/freddie_mac/get | Retrieve an Asset Report with Freddie Mac format. Only Freddie Mac can use this endpoint. |
| POST | /credit/freddie_mac/reports/get | Retrieve an Asset Report with Freddie Mac format (aka VOA - Verification Of Assets), and a Verification Of Employment (VOE) report if this one is available. Only Freddie Mac can use this endpoint. |
| POST | /credit/bank_income/get | Retrieve information from the bank accounts used for income verification |
| POST | /credit/bank_income/pdf/get | Retrieve information from the bank accounts used for income verification in PDF format |
| POST | /credit/bank_income/refresh | Refresh a user's bank income information |
| POST | /credit/bank_income/webhook/update | Subscribe and unsubscribe to proactive notifications for a user's income profile |
| POST | /credit/payroll_income/parsing_config/update | Update the parsing configuration for a document income verification |
| POST | /credit/bank_statements/uploads/get | Retrieve data for a user's uploaded bank statements |
| POST | /credit/payroll_income/get | Retrieve a user's payroll information |
| POST | /credit/payroll_income/risk_signals/get | Retrieve fraud insights for a user's manually uploaded document(s). |
| POST | /credit/payroll_income/precheck | Check income verification eligibility and optimize conversion |
| POST | /credit/employment/get | Retrieve a summary of an individual's employment information |
| POST | /credit/payroll_income/refresh | Refresh a digital payroll income verification |
| POST | /credit/relay/create | Create a relay token to share an Asset Report with a partner client |
| POST | /credit/relay/get | Retrieve the reports associated with a relay token that was shared with you |
| POST | /credit/relay/pdf/get | Retrieve the pdf reports associated with a relay token that was shared with you (beta) |
| POST | /credit/relay/refresh | Refresh a report of a relay token |
| POST | /credit/relay/remove | Remove relay token |

### consumer_report
| Method | Path | Description |
|--------|------|-------------|
| POST | /consumer_report/pdf/get | Retrieve a PDF Reports |

### oauth
| Method | Path | Description |
|--------|------|-------------|
| POST | /oauth/token | Create or refresh an OAuth access token |
| POST | /oauth/introspect | Get metadata about an OAuth token |
| POST | /oauth/revoke | Revoke an OAuth token |

### statements
| Method | Path | Description |
|--------|------|-------------|
| POST | /statements/list | Retrieve a list of all statements associated with an item. |
| POST | /statements/download | Retrieve a single statement. |
| POST | /statements/refresh | Refresh statements data. |

### consent
| Method | Path | Description |
|--------|------|-------------|
| POST | /consent/events/get | List a historical log of item consent events |

### item
| Method | Path | Description |
|--------|------|-------------|
| POST | /item/activity/list | List a historical log of user consent events |
| POST | /item/application/list | List a user’s connected applications |
| POST | /item/application/unlink | Unlink a user’s connected application |
| POST | /item/application/scopes/update | Update the scopes of access for a particular application |
| POST | /item/get | Retrieve an Item |
| POST | /item/remove | Remove an Item |
| POST | /item/webhook/update | Update Webhook URL |
| POST | /item/access_token/invalidate | Invalidate access_token |
| POST | /item/public_token/exchange | Exchange public token for an access token |
| POST | /item/public_token/create | Create public token |
| POST | /item/import | Import Item |

### application
| Method | Path | Description |
|--------|------|-------------|
| POST | /application/get | Retrieve information about a Plaid application |

### user_account
| Method | Path | Description |
|--------|------|-------------|
| POST | /user_account/session/get | Retrieve User Account |
| POST | /user_account/session/event/send | Send User Account Session Event |

### profile
| Method | Path | Description |
|--------|------|-------------|
| POST | /profile/network_status/get | Check a user's Plaid Network status |

### network
| Method | Path | Description |
|--------|------|-------------|
| POST | /network/status/get | Check a user's Plaid Network status |

### auth
| Method | Path | Description |
|--------|------|-------------|
| POST | /auth/get | Retrieve auth data |
| POST | /auth/verify | Verify auth data |

### transactions
| Method | Path | Description |
|--------|------|-------------|
| POST | /transactions/get | Get transaction data |
| POST | /transactions/refresh | Refresh transaction data |
| POST | /transactions/recurring/get | Fetch recurring transaction streams |
| POST | /transactions/sync | Get incremental transaction updates on an Item |
| POST | /transactions/enrich | Enrich locally-held transaction data |

### sandbox
| Method | Path | Description |
|--------|------|-------------|
| POST | /sandbox/transactions/create | Create sandbox transactions |
| POST | /sandbox/processor_token/create | Create a test Item and processor token |
| POST | /sandbox/public_token/create | Create a test Item |
| POST | /sandbox/item/fire_webhook | Fire a test webhook |
| POST | /sandbox/item/reset_login | Force a Sandbox Item into an error state |
| POST | /sandbox/item/set_verification_status | Set verification status for Sandbox account |
| POST | /sandbox/user/reset_login | Force item(s) for a Sandbox User into an error state |
| POST | /sandbox/bank_transfer/simulate | Simulate a bank transfer event in Sandbox |
| POST | /sandbox/transfer/sweep/simulate | Simulate creating a sweep |
| POST | /sandbox/transfer/simulate | Simulate a transfer event in Sandbox |
| POST | /sandbox/transfer/refund/simulate | Simulate a refund event in Sandbox |
| POST | /sandbox/transfer/ledger/simulate_available | Simulate converting pending balance to available balance |
| POST | /sandbox/transfer/ledger/deposit/simulate | Simulate a ledger deposit event in Sandbox |
| POST | /sandbox/transfer/ledger/withdraw/simulate | Simulate a ledger withdraw event in Sandbox |
| POST | /sandbox/transfer/repayment/simulate | Trigger the creation of a repayment |
| POST | /sandbox/transfer/fire_webhook | Manually fire a Transfer webhook |
| POST | /sandbox/transfer/test_clock/create | Create a test clock |
| POST | /sandbox/transfer/test_clock/advance | Advance a test clock |
| POST | /sandbox/transfer/test_clock/get | Get a test clock |
| POST | /sandbox/transfer/test_clock/list | List test clocks |
| POST | /sandbox/payment_profile/reset_login | Reset the login of a Payment Profile |
| POST | /sandbox/payment/simulate | Simulate a payment event in Sandbox |
| POST | /sandbox/bank_transfer/fire_webhook | Manually fire a Bank Transfer webhook |
| POST | /sandbox/income/fire_webhook | Manually fire an Income webhook |
| POST | /sandbox/bank_income/fire_webhook | Manually fire a bank income webhook in sandbox |
| POST | /sandbox/cra/cashflow_updates/update | Trigger an update for Cash Flow Updates |
| POST | /sandbox/oauth/select_accounts | Save the selected accounts when connecting to the Platypus Oauth institution |

### cashflow_report
| Method | Path | Description |
|--------|------|-------------|
| POST | /cashflow_report/refresh | Refresh transaction data in `cashflow_report` |
| POST | /cashflow_report/get | Gets transaction data in `cashflow_report` |
| POST | /cashflow_report/transactions/get | Gets transaction data in cashflow_report |
| POST | /cashflow_report/insights/get | Gets insights data in Cashflow Report |

### user
| Method | Path | Description |
|--------|------|-------------|
| POST | /user/transactions/refresh | Refresh user items for Transactions bundle |
| POST | /user/financial_data/refresh | Refresh user items for Financial-Insights bundle |
| POST | /user/create | Create user |
| POST | /user/get | Retrieve user identity and information |
| POST | /user/identity/remove | Remove user identity data |
| POST | /user/update | Update user information |
| POST | /user/remove | Remove user |
| POST | /user/products/terminate | Terminate user-based products |
| POST | /user/items/get | Get Items associated with a User |
| POST | /user/items/associate | Associate Items to a User |
| POST | /user/items/remove | Remove Items from a User |
| POST | /user/third_party_token/create | Create a third-party user token |
| POST | /user/third_party_token/remove | Remove a third-party user token |

### institutions
| Method | Path | Description |
|--------|------|-------------|
| POST | /institutions/get | Get details of all supported institutions |
| POST | /institutions/search | Search institutions |
| POST | /institutions/get_by_id | Get details of an institution |

### accounts
| Method | Path | Description |
|--------|------|-------------|
| POST | /accounts/get | Retrieve accounts |
| POST | /accounts/balance/get | Retrieve real-time balance data |

### categories
| Method | Path | Description |
|--------|------|-------------|
| POST | /categories/get | (Deprecated) Get legacy categories |

### identity
| Method | Path | Description |
|--------|------|-------------|
| POST | /identity/get | Retrieve identity data |
| POST | /identity/documents/uploads/get | Returns uploaded document identity |
| POST | /identity/match | Retrieve identity match score |
| POST | /identity/refresh | Refresh identity data |

### dashboard_user
| Method | Path | Description |
|--------|------|-------------|
| POST | /dashboard_user/get | Retrieve a dashboard user |
| POST | /dashboard_user/list | List dashboard users |

### identity_verification
| Method | Path | Description |
|--------|------|-------------|
| POST | /identity_verification/create | Create a new Identity Verification |
| POST | /identity_verification/get | Retrieve Identity Verification |
| POST | /identity_verification/list | List Identity Verifications |
| POST | /identity_verification/retry | Retry an Identity Verification |
| POST | /identity_verification/autofill/create | Create autofill for an Identity Verification |

### watchlist_screening
| Method | Path | Description |
|--------|------|-------------|
| POST | /watchlist_screening/entity/create | Create a watchlist screening for an entity |
| POST | /watchlist_screening/entity/get | Get an entity screening |
| POST | /watchlist_screening/entity/history/list | List history for entity watchlist screenings |
| POST | /watchlist_screening/entity/hit/list | List hits for entity watchlist screenings |
| POST | /watchlist_screening/entity/list | List entity watchlist screenings |
| POST | /watchlist_screening/entity/program/get | Get entity watchlist screening program |
| POST | /watchlist_screening/entity/program/list | List entity watchlist screening programs |
| POST | /watchlist_screening/entity/review/create | Create a review for an entity watchlist screening |
| POST | /watchlist_screening/entity/review/list | List reviews for entity watchlist screenings |
| POST | /watchlist_screening/entity/update | Update an entity screening |
| POST | /watchlist_screening/individual/create | Create a watchlist screening for a person |
| POST | /watchlist_screening/individual/get | Retrieve an individual watchlist screening |
| POST | /watchlist_screening/individual/history/list | List history for individual watchlist screenings |
| POST | /watchlist_screening/individual/hit/list | List hits for individual watchlist screening |
| POST | /watchlist_screening/individual/list | List Individual Watchlist Screenings |
| POST | /watchlist_screening/individual/program/get | Get individual watchlist screening program |
| POST | /watchlist_screening/individual/program/list | List individual watchlist screening programs |
| POST | /watchlist_screening/individual/review/create | Create a review for an individual watchlist screening |
| POST | /watchlist_screening/individual/review/list | List reviews for individual watchlist screenings |
| POST | /watchlist_screening/individual/update | Update individual watchlist screening |

### beacon
| Method | Path | Description |
|--------|------|-------------|
| POST | /beacon/account_risk/v1/evaluate | Evaluate risk of a bank account |
| POST | /beacon/user/create | Create a Beacon User |
| POST | /beacon/user/get | Get a Beacon User |
| POST | /beacon/user/review | Review a Beacon User |
| POST | /beacon/report/create | Create a Beacon Report |
| POST | /beacon/report/list | List Beacon Reports for a Beacon User |
| POST | /beacon/report_syndication/list | List Beacon Report Syndications for a Beacon User |
| POST | /beacon/report/get | Get a Beacon Report |
| POST | /beacon/report_syndication/get | Get a Beacon Report Syndication |
| POST | /beacon/user/update | Update the identity data of a Beacon User |
| POST | /beacon/duplicate/get | Get a Beacon Duplicate |
| POST | /beacon/user/history/list | List a Beacon User's history |
| POST | /beacon/user/account_insights/get | Get Account Insights for a Beacon User |

### protect
| Method | Path | Description |
|--------|------|-------------|
| POST | /protect/user/insights/get | Get Protect user insights |
| POST | /protect/report/create | Create a Protect report |
| POST | /protect/compute | Compute Protect Trust Index Score |
| POST | /protect/event/send | Send a new event to enrich user data |
| POST | /protect/event/get | Get information about a user event |

### business_verification
| Method | Path | Description |
|--------|------|-------------|
| POST | /business_verification/get | Get a business verification |
| POST | /business_verification/create | Create a business verification |

### processor
| Method | Path | Description |
|--------|------|-------------|
| POST | /processor/auth/get | Retrieve Auth data |
| POST | /processor/account/get | Retrieve the account associated with a processor token |
| POST | /processor/investments/holdings/get | Retrieve Investment Holdings |
| POST | /processor/investments/transactions/get | Get investment transactions data |
| POST | /processor/transactions/get | Get transaction data |
| POST | /processor/transactions/sync | Get incremental transaction updates on a processor token |
| POST | /processor/transactions/refresh | Refresh transaction data |
| POST | /processor/transactions/recurring/get | Fetch recurring transaction streams |
| POST | /processor/signal/evaluate | Evaluate a planned ACH transaction |
| POST | /processor/signal/decision/report | Report whether you initiated an ACH transaction |
| POST | /processor/signal/return/report | Report a return for an ACH transaction |
| POST | /processor/signal/prepare | Opt-in a processor token to Signal |
| POST | /processor/bank_transfer/create | Create a bank transfer as a processor |
| POST | /processor/liabilities/get | Retrieve Liabilities data |
| POST | /processor/identity/get | Retrieve Identity data |
| POST | /processor/identity/match | Retrieve identity match score |
| POST | /processor/balance/get | Retrieve Balance data |
| POST | /processor/token/create | Create processor token |
| POST | /processor/token/permissions/set | Control a processor's access to products |
| POST | /processor/token/permissions/get | Get a processor token's product permissions |
| POST | /processor/token/webhook/update | Update a processor token's webhook URL |
| POST | /processor/stripe/bank_account_token/create | Create Stripe bank account token |
| POST | /processor/apex/processor_token/create | Create Apex bank account token |

### webhook_verification_key
| Method | Path | Description |
|--------|------|-------------|
| POST | /webhook_verification_key/get | Get webhook verification key |

### liabilities
| Method | Path | Description |
|--------|------|-------------|
| POST | /liabilities/get | Retrieve Liabilities data |

### payment_initiation
| Method | Path | Description |
|--------|------|-------------|
| POST | /payment_initiation/recipient/create | Create payment recipient |
| POST | /payment_initiation/payment/reverse | Reverse an existing payment |
| POST | /payment_initiation/recipient/get | Get payment recipient |
| POST | /payment_initiation/recipient/list | List payment recipients |
| POST | /payment_initiation/payment/create | Create a payment |
| POST | /payment_initiation/payment/token/create | Create payment token |
| POST | /payment_initiation/consent/create | Create payment consent |
| POST | /payment_initiation/consent/get | Get payment consent |
| POST | /payment_initiation/consent/revoke | Revoke payment consent |
| POST | /payment_initiation/consent/payment/execute | Execute a single payment using consent |
| POST | /payment_initiation/payment/get | Get payment details |
| POST | /payment_initiation/payment/list | List payments |

### investments
| Method | Path | Description |
|--------|------|-------------|
| POST | /investments/holdings/get | Get Investment holdings |
| POST | /investments/transactions/get | Get investment transactions |
| POST | /investments/refresh | Refresh investment data |
| POST | /investments/auth/get | Get data needed to authorize an investments transfer |

### link
| Method | Path | Description |
|--------|------|-------------|
| POST | /link/token/create | Create Link Token |
| POST | /link/token/get | Get Link Token |
| POST | /link/oauth/correlation_id/exchange | Exchange the Link Correlation Id for a Link Token |

### session
| Method | Path | Description |
|--------|------|-------------|
| POST | /session/token/create | Create a Link token for Layer |

### transfer
| Method | Path | Description |
|--------|------|-------------|
| POST | /transfer/get | Retrieve a transfer |
| POST | /transfer/recurring/get | Retrieve a recurring transfer |
| POST | /transfer/authorization/create | Create a transfer authorization |
| POST | /transfer/authorization/cancel | Cancel a transfer authorization |
| POST | /transfer/balance/get | (Deprecated) Retrieve a balance held with Plaid |
| POST | /transfer/capabilities/get | Get RTP eligibility information of a transfer |
| POST | /transfer/configuration/get | Get transfer product configuration |
| POST | /transfer/ledger/get | Retrieve Plaid Ledger balance |
| POST | /transfer/ledger/distribute | Move available balance between ledgers |
| POST | /transfer/ledger/deposit | Deposit funds into a Plaid Ledger balance |
| POST | /transfer/ledger/withdraw | Withdraw funds from a Plaid Ledger balance |
| POST | /transfer/originator/funding_account/update | Update the funding account associated with the originator |
| POST | /transfer/originator/funding_account/create | Create a new funding account for an originator |
| POST | /transfer/metrics/get | Get transfer product usage metrics |
| POST | /transfer/create | Create a transfer |
| POST | /transfer/recurring/create | Create a recurring transfer |
| POST | /transfer/list | List transfers |
| POST | /transfer/recurring/list | List recurring transfers |
| POST | /transfer/cancel | Cancel a transfer |
| POST | /transfer/recurring/cancel | Cancel a recurring transfer. |
| POST | /transfer/event/list | List transfer events |
| POST | /transfer/ledger/event/list | List transfer ledger events |
| POST | /transfer/event/sync | Sync transfer events |
| POST | /transfer/sweep/get | Retrieve a sweep |
| POST | /transfer/sweep/list | List sweeps |
| POST | /transfer/migrate_account | Migrate account into Transfers |
| POST | /transfer/intent/create | Create a transfer intent object to invoke the Transfer UI |
| POST | /transfer/intent/get | Retrieve more information about a transfer intent |
| POST | /transfer/repayment/list | Lists historical repayments |
| POST | /transfer/repayment/return/list | List the returns included in a repayment |
| POST | /transfer/platform/requirement/submit | Submit additional onboarding information on behalf of an originator |
| POST | /transfer/originator/create | Create a new originator |
| POST | /transfer/questionnaire/create | Generate a Plaid-hosted onboarding UI URL. |
| POST | /transfer/diligence/submit | Submit transfer diligence on behalf of the originator |
| POST | /transfer/diligence/document/upload | Upload transfer diligence document on behalf of the originator |
| POST | /transfer/originator/get | Get status of an originator's onboarding |
| POST | /transfer/originator/list | Get status of all originators' onboarding |
| POST | /transfer/refund/create | Create a refund |
| POST | /transfer/refund/get | Retrieve a refund |
| POST | /transfer/refund/cancel | Cancel a refund |
| POST | /transfer/platform/originator/create | Create an originator for Transfer for Platforms customers |
| POST | /transfer/platform/person/create | Create a person associated with an originator |

### bank_transfer
| Method | Path | Description |
|--------|------|-------------|
| POST | /bank_transfer/get | Retrieve a bank transfer |
| POST | /bank_transfer/create | Create a bank transfer |
| POST | /bank_transfer/list | List bank transfers |
| POST | /bank_transfer/cancel | Cancel a bank transfer |
| POST | /bank_transfer/event/list | List bank transfer events |
| POST | /bank_transfer/event/sync | Sync bank transfer events |
| POST | /bank_transfer/sweep/get | Retrieve a sweep |
| POST | /bank_transfer/sweep/list | List sweeps |
| POST | /bank_transfer/balance/get | Get balance of your Bank Transfer account |
| POST | /bank_transfer/migrate_account | Migrate account into Bank Transfers |

### employers
| Method | Path | Description |
|--------|------|-------------|
| POST | /employers/search | Search employer database |

### income
| Method | Path | Description |
|--------|------|-------------|
| POST | /income/verification/create | (Deprecated) Create an income verification instance |
| POST | /income/verification/paystubs/get | (Deprecated) Retrieve information from the paystubs used for income verification |
| POST | /income/verification/documents/download | (Deprecated) Download the original documents used for income verification |
| POST | /income/verification/taxforms/get | (Deprecated) Retrieve information from the tax documents used for income verification |
| POST | /income/verification/precheck | (Deprecated) Check digital income verification eligibility and optimize conversion |

### employment
| Method | Path | Description |
|--------|------|-------------|
| POST | /employment/verification/get | (Deprecated) Retrieve a summary of an individual's employment information |

### beta
| Method | Path | Description |
|--------|------|-------------|
| POST | /beta/credit/v1/bank_employment/get | Retrieve information from the bank accounts used for employment verification |
| POST | /beta/transactions/v1/enhance | enhance locally-held transaction data |
| POST | /beta/transactions/rules/v1/create | Create transaction category rule |
| POST | /beta/transactions/rules/v1/list | Return a list of rules created for the Item associated with the access token. |
| POST | /beta/transactions/rules/v1/remove | Remove transaction rule |
| POST | /beta/transactions/user_insights/v1/get | Obtain user insights based on transactions sent through /transactions/enrich |
| POST | /beta/ewa_report/v1/get | Get EWA Score Report |
| POST | /beta/partner/customer/v1/create | Creates a new end customer for a Plaid reseller. |
| POST | /beta/partner/customer/v1/get | Retrieves the details of a Plaid reseller's end customer. |
| POST | /beta/partner/customer/v1/update | Updates an existing end customer. |
| POST | /beta/partner/customer/v1/enable | Enables a Plaid reseller's end customer in the Production environment. |

### signal
| Method | Path | Description |
|--------|------|-------------|
| POST | /signal/evaluate | Evaluate a planned ACH transaction |
| POST | /signal/schedule | Schedule a planned ACH transaction |
| POST | /signal/decision/report | Report whether you initiated an ACH transaction |
| POST | /signal/return/report | Report a return for an ACH transaction |
| POST | /signal/prepare | Opt-in an Item to Signal Transaction Scores |

### wallet
| Method | Path | Description |
|--------|------|-------------|
| POST | /wallet/create | Create an e-wallet |
| POST | /wallet/get | Fetch an e-wallet |
| POST | /wallet/list | Fetch a list of e-wallets |
| POST | /wallet/transaction/execute | Execute a transaction using an e-wallet |
| POST | /wallet/transaction/get | Fetch an e-wallet transaction |
| POST | /wallet/transaction/list | List e-wallet transactions |

### issues
| Method | Path | Description |
|--------|------|-------------|
| POST | /issues/search | Search for an Issue |
| POST | /issues/get | Get an Issue |
| POST | /issues/subscribe | Subscribe to an Issue |

### payment_profile
| Method | Path | Description |
|--------|------|-------------|
| POST | /payment_profile/create | Create payment profile |
| POST | /payment_profile/get | Get payment profile |
| POST | /payment_profile/remove | Remove payment profile |

### partner
| Method | Path | Description |
|--------|------|-------------|
| POST | /partner/customer/create | Creates a new end customer for a Plaid reseller. |
| POST | /partner/customer/get | Returns a Plaid reseller's end customer. |
| POST | /partner/customer/enable | Enables a Plaid reseller's end customer in the Production environment. |
| POST | /partner/customer/remove | Removes a Plaid reseller's end customer. |
| POST | /partner/customer/oauth_institutions/get | Returns OAuth-institution registration information for a given end customer. |

### link_delivery
| Method | Path | Description |
|--------|------|-------------|
| POST | /link_delivery/create | Create Hosted Link session |
| POST | /link_delivery/get | Get Hosted Link session |

### fdx
| Method | Path | Description |
|--------|------|-------------|
| POST | /fdx/notifications | Webhook receiver for fdx notifications |
| GET | /fdx/recipients | Get Recipients |
| GET | /fdx/recipient/{recipientId} | Get Recipient |

### network_insights
| Method | Path | Description |
|--------|------|-------------|
| POST | /network_insights/report/get | Retrieve network insights for the provided `access_tokens` |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a create?" -> POST /asset_report/create
- "Create a get?" -> POST /asset_report/get
- "Create a get?" -> POST /asset_report/pdf/get
- "Create a refresh?" -> POST /asset_report/refresh
- "Create a filter?" -> POST /asset_report/filter
- "Create a remove?" -> POST /asset_report/remove
- "Create a create?" -> POST /asset_report/audit_copy/create
- "Create a get?" -> POST /asset_report/audit_copy/get
- "Create a get?" -> POST /asset_report/audit_copy/pdf/get
- "Create a remove?" -> POST /asset_report/audit_copy/remove
- "Create a subscribe?" -> POST /cra/monitoring_insights/subscribe
- "Create a unsubscribe?" -> POST /cra/monitoring_insights/unsubscribe
- "Create a get?" -> POST /cra/monitoring_insights/get
- "Create a update?" -> POST /credit/audit_copy_token/update
- "Create a get?" -> POST /cra/partner_insights/get
- "Create a get?" -> POST /cra/check_report/income_insights/get
- "Create a get?" -> POST /cra/check_report/base_report/get
- "Create a get?" -> POST /cra/check_report/pdf/get
- "Create a create?" -> POST /cra/check_report/create
- "Create a get?" -> POST /cra/check_report/partner_insights/get
- "Create a get?" -> POST /cra/check_report/cashflow_insights/get
- "Create a get?" -> POST /cra/check_report/lend_score/get
- "Create a get?" -> POST /cra/check_report/network_insights/get
- "Create a get?" -> POST /cra/check_report/verification/get
- "Create a get?" -> POST /cra/check_report/verification/pdf/get
- "Create a register?" -> POST /cra/loans/applications/register
- "Create a register?" -> POST /cra/loans/register
- "Create a update?" -> POST /cra/loans/update
- "Create a unregister?" -> POST /cra/loans/unregister
- "Create a get?" -> POST /consumer_report/pdf/get
- "Create a token?" -> POST /oauth/token
- "Create a introspect?" -> POST /oauth/introspect
- "Create a revoke?" -> POST /oauth/revoke
- "Create a list?" -> POST /statements/list
- "Create a download?" -> POST /statements/download
- "Create a refresh?" -> POST /statements/refresh
- "Create a get?" -> POST /consent/events/get
- "Create a list?" -> POST /item/activity/list
- "Create a list?" -> POST /item/application/list
- "Create a unlink?" -> POST /item/application/unlink
- "Create a update?" -> POST /item/application/scopes/update
- "Create a get?" -> POST /application/get
- "Create a get?" -> POST /item/get
- "Create a get?" -> POST /user_account/session/get
- "Create a send?" -> POST /user_account/session/event/send
- "Create a get?" -> POST /profile/network_status/get
- "Create a get?" -> POST /network/status/get
- "Create a get?" -> POST /auth/get
- "Create a verify?" -> POST /auth/verify
- "Create a get?" -> POST /transactions/get
- "Create a refresh?" -> POST /transactions/refresh
- "Create a create?" -> POST /sandbox/transactions/create
- "Create a refresh?" -> POST /cashflow_report/refresh
- "Create a get?" -> POST /cashflow_report/get
- "Create a get?" -> POST /cashflow_report/transactions/get
- "Create a get?" -> POST /cashflow_report/insights/get
- "Create a get?" -> POST /transactions/recurring/get
- "Create a sync?" -> POST /transactions/sync
- "Create a enrich?" -> POST /transactions/enrich
- "Create a refresh?" -> POST /user/transactions/refresh
- "Create a refresh?" -> POST /user/financial_data/refresh
- "Create a get?" -> POST /institutions/get
- "Create a search?" -> POST /institutions/search
- "Create a get_by_id?" -> POST /institutions/get_by_id
- "Create a remove?" -> POST /item/remove
- "Create a get?" -> POST /accounts/get
- "Create a get?" -> POST /categories/get
- "Create a create?" -> POST /sandbox/processor_token/create
- "Create a create?" -> POST /sandbox/public_token/create
- "Create a fire_webhook?" -> POST /sandbox/item/fire_webhook
- "Create a get?" -> POST /accounts/balance/get
- "Create a get?" -> POST /identity/get
- "Create a get?" -> POST /identity/documents/uploads/get
- "Create a match?" -> POST /identity/match
- "Create a refresh?" -> POST /identity/refresh
- "Create a get?" -> POST /dashboard_user/get
- "Create a list?" -> POST /dashboard_user/list
- "Create a create?" -> POST /identity_verification/create
- "Create a get?" -> POST /identity_verification/get
- "Create a list?" -> POST /identity_verification/list
- "Create a retry?" -> POST /identity_verification/retry
- "Create a create?" -> POST /watchlist_screening/entity/create
- "Create a get?" -> POST /watchlist_screening/entity/get
- "Create a list?" -> POST /watchlist_screening/entity/history/list
- "Create a list?" -> POST /watchlist_screening/entity/hit/list
- "Create a list?" -> POST /watchlist_screening/entity/list
- "Create a get?" -> POST /watchlist_screening/entity/program/get
- "Create a list?" -> POST /watchlist_screening/entity/program/list
- "Create a create?" -> POST /watchlist_screening/entity/review/create
- "Create a list?" -> POST /watchlist_screening/entity/review/list
- "Create a update?" -> POST /watchlist_screening/entity/update
- "Create a create?" -> POST /watchlist_screening/individual/create
- "Create a get?" -> POST /watchlist_screening/individual/get
- "Create a list?" -> POST /watchlist_screening/individual/history/list
- "Create a list?" -> POST /watchlist_screening/individual/hit/list
- "Create a list?" -> POST /watchlist_screening/individual/list
- "Create a get?" -> POST /watchlist_screening/individual/program/get
- "Create a list?" -> POST /watchlist_screening/individual/program/list
- "Create a create?" -> POST /watchlist_screening/individual/review/create
- "Create a list?" -> POST /watchlist_screening/individual/review/list
- "Create a update?" -> POST /watchlist_screening/individual/update
- "Create a evaluate?" -> POST /beacon/account_risk/v1/evaluate
- "Create a create?" -> POST /beacon/user/create
- "Create a get?" -> POST /beacon/user/get
- "Create a review?" -> POST /beacon/user/review
- "Create a create?" -> POST /beacon/report/create
- "Create a list?" -> POST /beacon/report/list
- "Create a list?" -> POST /beacon/report_syndication/list
- "Create a get?" -> POST /beacon/report/get
- "Create a get?" -> POST /beacon/report_syndication/get
- "Create a update?" -> POST /beacon/user/update
- "Create a get?" -> POST /beacon/duplicate/get
- "Create a create?" -> POST /identity_verification/autofill/create
- "Create a list?" -> POST /beacon/user/history/list
- "Create a get?" -> POST /beacon/user/account_insights/get
- "Create a get?" -> POST /protect/user/insights/get
- "Create a create?" -> POST /protect/report/create
- "Create a compute?" -> POST /protect/compute
- "Create a send?" -> POST /protect/event/send
- "Create a get?" -> POST /protect/event/get
- "Create a get?" -> POST /business_verification/get
- "Create a create?" -> POST /business_verification/create
- "Create a get?" -> POST /processor/auth/get
- "Create a get?" -> POST /processor/account/get
- "Create a get?" -> POST /processor/investments/holdings/get
- "Create a get?" -> POST /processor/investments/transactions/get
- "Create a get?" -> POST /processor/transactions/get
- "Create a sync?" -> POST /processor/transactions/sync
- "Create a refresh?" -> POST /processor/transactions/refresh
- "Create a get?" -> POST /processor/transactions/recurring/get
- "Create a evaluate?" -> POST /processor/signal/evaluate
- "Create a report?" -> POST /processor/signal/decision/report
- "Create a report?" -> POST /processor/signal/return/report
- "Create a prepare?" -> POST /processor/signal/prepare
- "Create a create?" -> POST /processor/bank_transfer/create
- "Create a get?" -> POST /processor/liabilities/get
- "Create a get?" -> POST /processor/identity/get
- "Create a match?" -> POST /processor/identity/match
- "Create a get?" -> POST /processor/balance/get
- "Create a update?" -> POST /item/webhook/update
- "Create a invalidate?" -> POST /item/access_token/invalidate
- "Create a get?" -> POST /webhook_verification_key/get
- "Create a get?" -> POST /liabilities/get
- "Create a create?" -> POST /payment_initiation/recipient/create
- "Create a reverse?" -> POST /payment_initiation/payment/reverse
- "Create a get?" -> POST /payment_initiation/recipient/get
- "Create a list?" -> POST /payment_initiation/recipient/list
- "Create a create?" -> POST /payment_initiation/payment/create
- "Create a create?" -> POST /payment_initiation/payment/token/create
- "Create a create?" -> POST /payment_initiation/consent/create
- "Create a get?" -> POST /payment_initiation/consent/get
- "Create a revoke?" -> POST /payment_initiation/consent/revoke
- "Create a execute?" -> POST /payment_initiation/consent/payment/execute
- "Create a reset_login?" -> POST /sandbox/item/reset_login
- "Create a set_verification_status?" -> POST /sandbox/item/set_verification_status
- "Create a reset_login?" -> POST /sandbox/user/reset_login
- "Create a exchange?" -> POST /item/public_token/exchange
- "Create a create?" -> POST /item/public_token/create
- "Create a create?" -> POST /user/create
- "Create a get?" -> POST /user/get
- "Create a remove?" -> POST /user/identity/remove
- "Create a update?" -> POST /user/update
- "Create a remove?" -> POST /user/remove
- "Create a terminate?" -> POST /user/products/terminate
- "Create a get?" -> POST /user/items/get
- "Create a associate?" -> POST /user/items/associate
- "Create a remove?" -> POST /user/items/remove
- "Create a create?" -> POST /user/third_party_token/create
- "Create a remove?" -> POST /user/third_party_token/remove
- "Create a get?" -> POST /credit/sessions/get
- "Create a get?" -> POST /payment_initiation/payment/get
- "Create a list?" -> POST /payment_initiation/payment/list
- "Create a get?" -> POST /investments/holdings/get
- "Create a get?" -> POST /investments/transactions/get
- "Create a refresh?" -> POST /investments/refresh
- "Create a get?" -> POST /investments/auth/get
- "Create a create?" -> POST /processor/token/create
- "Create a set?" -> POST /processor/token/permissions/set
- "Create a get?" -> POST /processor/token/permissions/get
- "Create a update?" -> POST /processor/token/webhook/update
- "Create a create?" -> POST /processor/stripe/bank_account_token/create
- "Create a create?" -> POST /processor/apex/processor_token/create
- "Create a import?" -> POST /item/import
- "Create a create?" -> POST /link/token/create
- "Create a get?" -> POST /link/token/get
- "Create a exchange?" -> POST /link/oauth/correlation_id/exchange
- "Create a create?" -> POST /session/token/create
- "Create a get?" -> POST /transfer/get
- "Create a get?" -> POST /transfer/recurring/get
- "Create a get?" -> POST /bank_transfer/get
- "Create a create?" -> POST /transfer/authorization/create
- "Create a cancel?" -> POST /transfer/authorization/cancel
- "Create a get?" -> POST /transfer/balance/get
- "Create a get?" -> POST /transfer/capabilities/get
- "Create a get?" -> POST /transfer/configuration/get
- "Create a get?" -> POST /transfer/ledger/get
- "Create a distribute?" -> POST /transfer/ledger/distribute
- "Create a deposit?" -> POST /transfer/ledger/deposit
- "Create a withdraw?" -> POST /transfer/ledger/withdraw
- "Create a update?" -> POST /transfer/originator/funding_account/update
- "Create a create?" -> POST /transfer/originator/funding_account/create
- "Create a get?" -> POST /transfer/metrics/get
- "Create a create?" -> POST /transfer/create
- "Create a create?" -> POST /transfer/recurring/create
- "Create a create?" -> POST /bank_transfer/create
- "Create a list?" -> POST /transfer/list
- "Create a list?" -> POST /transfer/recurring/list
- "Create a list?" -> POST /bank_transfer/list
- "Create a cancel?" -> POST /transfer/cancel
- "Create a cancel?" -> POST /transfer/recurring/cancel
- "Create a cancel?" -> POST /bank_transfer/cancel
- "Create a list?" -> POST /transfer/event/list
- "Create a list?" -> POST /transfer/ledger/event/list
- "Create a list?" -> POST /bank_transfer/event/list
- "Create a sync?" -> POST /transfer/event/sync
- "Create a sync?" -> POST /bank_transfer/event/sync
- "Create a get?" -> POST /transfer/sweep/get
- "Create a get?" -> POST /bank_transfer/sweep/get
- "Create a list?" -> POST /transfer/sweep/list
- "Create a list?" -> POST /bank_transfer/sweep/list
- "Create a get?" -> POST /bank_transfer/balance/get
- "Create a migrate_account?" -> POST /bank_transfer/migrate_account
- "Create a migrate_account?" -> POST /transfer/migrate_account
- "Create a create?" -> POST /transfer/intent/create
- "Create a get?" -> POST /transfer/intent/get
- "Create a list?" -> POST /transfer/repayment/list
- "Create a list?" -> POST /transfer/repayment/return/list
- "Create a submit?" -> POST /transfer/platform/requirement/submit
- "Create a create?" -> POST /transfer/originator/create
- "Create a create?" -> POST /transfer/questionnaire/create
- "Create a submit?" -> POST /transfer/diligence/submit
- "Create a upload?" -> POST /transfer/diligence/document/upload
- "Create a get?" -> POST /transfer/originator/get
- "Create a list?" -> POST /transfer/originator/list
- "Create a create?" -> POST /transfer/refund/create
- "Create a get?" -> POST /transfer/refund/get
- "Create a cancel?" -> POST /transfer/refund/cancel
- "Create a create?" -> POST /transfer/platform/originator/create
- "Create a create?" -> POST /transfer/platform/person/create
- "Create a simulate?" -> POST /sandbox/bank_transfer/simulate
- "Create a simulate?" -> POST /sandbox/transfer/sweep/simulate
- "Create a simulate?" -> POST /sandbox/transfer/simulate
- "Create a simulate?" -> POST /sandbox/transfer/refund/simulate
- "Create a simulate_available?" -> POST /sandbox/transfer/ledger/simulate_available
- "Create a simulate?" -> POST /sandbox/transfer/ledger/deposit/simulate
- "Create a simulate?" -> POST /sandbox/transfer/ledger/withdraw/simulate
- "Create a simulate?" -> POST /sandbox/transfer/repayment/simulate
- "Create a fire_webhook?" -> POST /sandbox/transfer/fire_webhook
- "Create a create?" -> POST /sandbox/transfer/test_clock/create
- "Create a advance?" -> POST /sandbox/transfer/test_clock/advance
- "Create a get?" -> POST /sandbox/transfer/test_clock/get
- "Create a list?" -> POST /sandbox/transfer/test_clock/list
- "Create a reset_login?" -> POST /sandbox/payment_profile/reset_login
- "Create a simulate?" -> POST /sandbox/payment/simulate
- "Create a search?" -> POST /employers/search
- "Create a create?" -> POST /income/verification/create
- "Create a get?" -> POST /income/verification/paystubs/get
- "Create a download?" -> POST /income/verification/documents/download
- "Create a get?" -> POST /income/verification/taxforms/get
- "Create a precheck?" -> POST /income/verification/precheck
- "Create a get?" -> POST /employment/verification/get
- "Create a create?" -> POST /credit/audit_copy_token/create
- "Create a remove?" -> POST /credit/audit_copy_token/remove
- "Create a get?" -> POST /credit/asset_report/freddie_mac/get
- "Create a get?" -> POST /credit/freddie_mac/reports/get
- "Create a get?" -> POST /beta/credit/v1/bank_employment/get
- "Create a get?" -> POST /credit/bank_income/get
- "Create a get?" -> POST /credit/bank_income/pdf/get
- "Create a refresh?" -> POST /credit/bank_income/refresh
- "Create a update?" -> POST /credit/bank_income/webhook/update
- "Create a update?" -> POST /credit/payroll_income/parsing_config/update
- "Create a get?" -> POST /credit/bank_statements/uploads/get
- "Create a get?" -> POST /credit/payroll_income/get
- "Create a get?" -> POST /credit/payroll_income/risk_signals/get
- "Create a precheck?" -> POST /credit/payroll_income/precheck
- "Create a get?" -> POST /credit/employment/get
- "Create a refresh?" -> POST /credit/payroll_income/refresh
- "Create a create?" -> POST /credit/relay/create
- "Create a get?" -> POST /credit/relay/get
- "Create a get?" -> POST /credit/relay/pdf/get
- "Create a refresh?" -> POST /credit/relay/refresh
- "Create a remove?" -> POST /credit/relay/remove
- "Create a fire_webhook?" -> POST /sandbox/bank_transfer/fire_webhook
- "Create a fire_webhook?" -> POST /sandbox/income/fire_webhook
- "Create a fire_webhook?" -> POST /sandbox/bank_income/fire_webhook
- "Create a update?" -> POST /sandbox/cra/cashflow_updates/update
- "Create a select_account?" -> POST /sandbox/oauth/select_accounts
- "Create a evaluate?" -> POST /signal/evaluate
- "Create a schedule?" -> POST /signal/schedule
- "Create a report?" -> POST /signal/decision/report
- "Create a report?" -> POST /signal/return/report
- "Create a prepare?" -> POST /signal/prepare
- "Create a create?" -> POST /wallet/create
- "Create a get?" -> POST /wallet/get
- "Create a list?" -> POST /wallet/list
- "Create a execute?" -> POST /wallet/transaction/execute
- "Create a get?" -> POST /wallet/transaction/get
- "Create a list?" -> POST /wallet/transaction/list
- "Create a enhance?" -> POST /beta/transactions/v1/enhance
- "Create a create?" -> POST /beta/transactions/rules/v1/create
- "Create a list?" -> POST /beta/transactions/rules/v1/list
- "Create a remove?" -> POST /beta/transactions/rules/v1/remove
- "Create a get?" -> POST /beta/transactions/user_insights/v1/get
- "Create a get?" -> POST /beta/ewa_report/v1/get
- "Create a search?" -> POST /issues/search
- "Create a get?" -> POST /issues/get
- "Create a subscribe?" -> POST /issues/subscribe
- "Create a create?" -> POST /payment_profile/create
- "Create a get?" -> POST /payment_profile/get
- "Create a remove?" -> POST /payment_profile/remove
- "Create a create?" -> POST /partner/customer/create
- "Create a get?" -> POST /partner/customer/get
- "Create a enable?" -> POST /partner/customer/enable
- "Create a remove?" -> POST /partner/customer/remove
- "Create a get?" -> POST /partner/customer/oauth_institutions/get
- "Create a create?" -> POST /beta/partner/customer/v1/create
- "Create a get?" -> POST /beta/partner/customer/v1/get
- "Create a update?" -> POST /beta/partner/customer/v1/update
- "Create a enable?" -> POST /beta/partner/customer/v1/enable
- "Create a create?" -> POST /link_delivery/create
- "Create a get?" -> POST /link_delivery/get
- "Create a notification?" -> POST /fdx/notifications
- "List all recipients?" -> GET /fdx/recipients
- "Get recipient details?" -> GET /fdx/recipient/{recipientId}
- "Create a get?" -> POST /network_insights/report/get
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
