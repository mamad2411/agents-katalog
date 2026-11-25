---
name: increase-api
description: "Increase API skill. Use when working with Increase for account_numbers, account_statements, account_transfers. Covers 232 endpoints."
version: 1.0.0
generator: lapsh
---

# Increase API
API version: 0.0.1

## Auth
Bearer bearer

## Base URL
https://api.increase.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /account_numbers -- verify access
3. POST /account_numbers -- create first account_numbers

## Endpoints

232 endpoints across 56 groups. See references/api-spec.lap for full details.

### account_numbers
| Method | Path | Description |
|--------|------|-------------|
| GET | /account_numbers | List Account Numbers |
| POST | /account_numbers | Create an Account Number |
| GET | /account_numbers/{account_number_id} | Retrieve an Account Number |
| PATCH | /account_numbers/{account_number_id} | Update an Account Number |

### account_statements
| Method | Path | Description |
|--------|------|-------------|
| GET | /account_statements | List Account Statements |
| GET | /account_statements/{account_statement_id} | Retrieve an Account Statement |

### account_transfers
| Method | Path | Description |
|--------|------|-------------|
| GET | /account_transfers | List Account Transfers |
| POST | /account_transfers | Create an Account Transfer |
| GET | /account_transfers/{account_transfer_id} | Retrieve an Account Transfer |
| POST | /account_transfers/{account_transfer_id}/approve | Approve an Account Transfer |
| POST | /account_transfers/{account_transfer_id}/cancel | Cancel an Account Transfer |

### accounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /accounts | List Accounts |
| POST | /accounts | Create an Account |
| GET | /accounts/{account_id} | Retrieve an Account |
| PATCH | /accounts/{account_id} | Update an Account |
| GET | /accounts/{account_id}/balance | Retrieve an Account Balance |
| POST | /accounts/{account_id}/close | Close an Account |
| GET | /accounts/{account_id}/intrafi_balance | Get IntraFi balance |

### ach_prenotifications
| Method | Path | Description |
|--------|------|-------------|
| GET | /ach_prenotifications | List ACH Prenotifications |
| POST | /ach_prenotifications | Create an ACH Prenotification |
| GET | /ach_prenotifications/{ach_prenotification_id} | Retrieve an ACH Prenotification |

### ach_transfers
| Method | Path | Description |
|--------|------|-------------|
| GET | /ach_transfers | List ACH Transfers |
| POST | /ach_transfers | Create an ACH Transfer |
| GET | /ach_transfers/{ach_transfer_id} | Retrieve an ACH Transfer |
| POST | /ach_transfers/{ach_transfer_id}/approve | Approve an ACH Transfer |
| POST | /ach_transfers/{ach_transfer_id}/cancel | Cancel a pending ACH Transfer |

### bookkeeping_accounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /bookkeeping_accounts | List Bookkeeping Accounts |
| POST | /bookkeeping_accounts | Create a Bookkeeping Account |
| PATCH | /bookkeeping_accounts/{bookkeeping_account_id} | Update a Bookkeeping Account |
| GET | /bookkeeping_accounts/{bookkeeping_account_id}/balance | Retrieve a Bookkeeping Account Balance |

### bookkeeping_entries
| Method | Path | Description |
|--------|------|-------------|
| GET | /bookkeeping_entries | List Bookkeeping Entries |
| GET | /bookkeeping_entries/{bookkeeping_entry_id} | Retrieve a Bookkeeping Entry |

### bookkeeping_entry_sets
| Method | Path | Description |
|--------|------|-------------|
| GET | /bookkeeping_entry_sets | List Bookkeeping Entry Sets |
| POST | /bookkeeping_entry_sets | Create a Bookkeeping Entry Set |
| GET | /bookkeeping_entry_sets/{bookkeeping_entry_set_id} | Retrieve a Bookkeeping Entry Set |

### card_disputes
| Method | Path | Description |
|--------|------|-------------|
| GET | /card_disputes | List Card Disputes |
| POST | /card_disputes | Create a Card Dispute |
| GET | /card_disputes/{card_dispute_id} | Retrieve a Card Dispute |
| POST | /card_disputes/{card_dispute_id}/submit_user_submission | Submit a User Submission for a Card Dispute |
| POST | /card_disputes/{card_dispute_id}/withdraw | Withdraw a Card Dispute |

### card_payments
| Method | Path | Description |
|--------|------|-------------|
| GET | /card_payments | List Card Payments |
| GET | /card_payments/{card_payment_id} | Retrieve a Card Payment |

### card_purchase_supplements
| Method | Path | Description |
|--------|------|-------------|
| GET | /card_purchase_supplements | List Card Purchase Supplements |
| GET | /card_purchase_supplements/{card_purchase_supplement_id} | Retrieve a Card Purchase Supplement |

### card_push_transfers
| Method | Path | Description |
|--------|------|-------------|
| GET | /card_push_transfers | List Card Push Transfers |
| POST | /card_push_transfers | Create a Card Push Transfer |
| GET | /card_push_transfers/{card_push_transfer_id} | Retrieve a Card Push Transfer |
| POST | /card_push_transfers/{card_push_transfer_id}/approve | Approve a Card Push Transfer |
| POST | /card_push_transfers/{card_push_transfer_id}/cancel | Cancel a pending Card Push Transfer |

### card_tokens
| Method | Path | Description |
|--------|------|-------------|
| GET | /card_tokens | List Card Tokens |
| GET | /card_tokens/{card_token_id} | Retrieve a Card Token |
| GET | /card_tokens/{card_token_id}/capabilities | Retrieve the capabilities of a Card Token |

### card_validations
| Method | Path | Description |
|--------|------|-------------|
| GET | /card_validations | List Card Validations |
| POST | /card_validations | Create a Card Validation |
| GET | /card_validations/{card_validation_id} | Retrieve a Card Validation |

### cards
| Method | Path | Description |
|--------|------|-------------|
| GET | /cards | List Cards |
| POST | /cards | Create a Card |
| GET | /cards/{card_id} | Retrieve a Card |
| PATCH | /cards/{card_id} | Update a Card |
| POST | /cards/{card_id}/create_details_iframe | Create a Card details iframe |
| GET | /cards/{card_id}/details | Retrieve sensitive details for a Card |
| POST | /cards/{card_id}/update_pin | Update a Card's PIN |

### check_deposits
| Method | Path | Description |
|--------|------|-------------|
| GET | /check_deposits | List Check Deposits |
| POST | /check_deposits | Create a Check Deposit |
| GET | /check_deposits/{check_deposit_id} | Retrieve a Check Deposit |

### check_transfers
| Method | Path | Description |
|--------|------|-------------|
| GET | /check_transfers | List Check Transfers |
| POST | /check_transfers | Create a Check Transfer |
| GET | /check_transfers/{check_transfer_id} | Retrieve a Check Transfer |
| POST | /check_transfers/{check_transfer_id}/approve | Approve a Check Transfer |
| POST | /check_transfers/{check_transfer_id}/cancel | Cancel a pending Check Transfer |
| POST | /check_transfers/{check_transfer_id}/stop_payment | Stop payment on a Check Transfer |

### declined_transactions
| Method | Path | Description |
|--------|------|-------------|
| GET | /declined_transactions | List Declined Transactions |
| GET | /declined_transactions/{declined_transaction_id} | Retrieve a Declined Transaction |

### digital_card_profiles
| Method | Path | Description |
|--------|------|-------------|
| GET | /digital_card_profiles | List Card Profiles |
| POST | /digital_card_profiles | Create a Digital Card Profile |
| GET | /digital_card_profiles/{digital_card_profile_id} | Retrieve a Digital Card Profile |
| POST | /digital_card_profiles/{digital_card_profile_id}/archive | Archive a Digital Card Profile |
| POST | /digital_card_profiles/{digital_card_profile_id}/clone | Clones a Digital Card Profile |

### digital_wallet_tokens
| Method | Path | Description |
|--------|------|-------------|
| GET | /digital_wallet_tokens | List Digital Wallet Tokens |
| GET | /digital_wallet_tokens/{digital_wallet_token_id} | Retrieve a Digital Wallet Token |

### entities
| Method | Path | Description |
|--------|------|-------------|
| GET | /entities | List Entities |
| POST | /entities | Create an Entity |
| GET | /entities/{entity_id} | Retrieve an Entity |
| PATCH | /entities/{entity_id} | Update an Entity |
| POST | /entities/{entity_id}/archive | Archive an Entity |
| POST | /entities/{entity_id}/archive_beneficial_owner | Archive a beneficial owner for a corporate Entity |
| POST | /entities/{entity_id}/confirm | Confirm an Entity's details are correct |
| POST | /entities/{entity_id}/create_beneficial_owner | Create a beneficial owner for a corporate Entity |
| POST | /entities/{entity_id}/update_address | Update a Natural Person or Corporation's address |
| POST | /entities/{entity_id}/update_beneficial_owner_address | Update the address for a beneficial owner belonging to a corporate Entity |
| POST | /entities/{entity_id}/update_industry_code | Update the industry code for a corporate Entity |

### entity_supplemental_documents
| Method | Path | Description |
|--------|------|-------------|
| GET | /entity_supplemental_documents | List Entity Supplemental Document Submissions |
| POST | /entity_supplemental_documents | Create a supplemental document for an Entity |

### event_subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /event_subscriptions | List Event Subscriptions |
| POST | /event_subscriptions | Create an Event Subscription |
| GET | /event_subscriptions/{event_subscription_id} | Retrieve an Event Subscription |
| PATCH | /event_subscriptions/{event_subscription_id} | Update an Event Subscription |

### events
| Method | Path | Description |
|--------|------|-------------|
| GET | /events | List Events |
| GET | /events/{event_id} | Retrieve an Event |

### exports
| Method | Path | Description |
|--------|------|-------------|
| GET | /exports | List Exports |
| POST | /exports | Create an Export |
| GET | /exports/{export_id} | Retrieve an Export |

### external_accounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /external_accounts | List External Accounts |
| POST | /external_accounts | Create an External Account |
| GET | /external_accounts/{external_account_id} | Retrieve an External Account |
| PATCH | /external_accounts/{external_account_id} | Update an External Account |

### fednow_transfers
| Method | Path | Description |
|--------|------|-------------|
| GET | /fednow_transfers | List FedNow Transfers |
| POST | /fednow_transfers | Create a FedNow Transfer |
| GET | /fednow_transfers/{fednow_transfer_id} | Retrieve a FedNow Transfer |
| POST | /fednow_transfers/{fednow_transfer_id}/approve | Approve a FedNow Transfer |
| POST | /fednow_transfers/{fednow_transfer_id}/cancel | Cancel a pending FedNow Transfer |

### file_links
| Method | Path | Description |
|--------|------|-------------|
| POST | /file_links | Create a File Link |

### files
| Method | Path | Description |
|--------|------|-------------|
| GET | /files | List Files |
| POST | /files | Create a File |
| GET | /files/{file_id} | Retrieve a File |

### groups
| Method | Path | Description |
|--------|------|-------------|
| GET | /groups/current | Retrieve Group details |

### inbound_ach_transfers
| Method | Path | Description |
|--------|------|-------------|
| GET | /inbound_ach_transfers | List Inbound ACH Transfers |
| GET | /inbound_ach_transfers/{inbound_ach_transfer_id} | Retrieve an Inbound ACH Transfer |
| POST | /inbound_ach_transfers/{inbound_ach_transfer_id}/create_notification_of_change | Create a notification of change for an Inbound ACH Transfer |
| POST | /inbound_ach_transfers/{inbound_ach_transfer_id}/decline | Decline an Inbound ACH Transfer |
| POST | /inbound_ach_transfers/{inbound_ach_transfer_id}/transfer_return | Return an Inbound ACH Transfer |

### inbound_check_deposits
| Method | Path | Description |
|--------|------|-------------|
| GET | /inbound_check_deposits | List Inbound Check Deposits |
| GET | /inbound_check_deposits/{inbound_check_deposit_id} | Retrieve an Inbound Check Deposit |
| POST | /inbound_check_deposits/{inbound_check_deposit_id}/decline | Decline an Inbound Check Deposit |
| POST | /inbound_check_deposits/{inbound_check_deposit_id}/return | Return an Inbound Check Deposit |

### inbound_fednow_transfers
| Method | Path | Description |
|--------|------|-------------|
| GET | /inbound_fednow_transfers | List Inbound FedNow Transfers |
| GET | /inbound_fednow_transfers/{inbound_fednow_transfer_id} | Retrieve an Inbound FedNow Transfer |

### inbound_mail_items
| Method | Path | Description |
|--------|------|-------------|
| GET | /inbound_mail_items | List Inbound Mail Items |
| GET | /inbound_mail_items/{inbound_mail_item_id} | Retrieve an Inbound Mail Item |
| POST | /inbound_mail_items/{inbound_mail_item_id}/action | Action an Inbound Mail Item |

### inbound_real_time_payments_transfers
| Method | Path | Description |
|--------|------|-------------|
| GET | /inbound_real_time_payments_transfers | List Inbound Real-Time Payments Transfers |
| GET | /inbound_real_time_payments_transfers/{inbound_real_time_payments_transfer_id} | Retrieve an Inbound Real-Time Payments Transfer |

### inbound_wire_drawdown_requests
| Method | Path | Description |
|--------|------|-------------|
| GET | /inbound_wire_drawdown_requests | List Inbound Wire Drawdown Requests |
| GET | /inbound_wire_drawdown_requests/{inbound_wire_drawdown_request_id} | Retrieve an Inbound Wire Drawdown Request |

### inbound_wire_transfers
| Method | Path | Description |
|--------|------|-------------|
| GET | /inbound_wire_transfers | List Inbound Wire Transfers |
| GET | /inbound_wire_transfers/{inbound_wire_transfer_id} | Retrieve an Inbound Wire Transfer |
| POST | /inbound_wire_transfers/{inbound_wire_transfer_id}/reverse | Reverse an Inbound Wire Transfer |

### intrafi_account_enrollments
| Method | Path | Description |
|--------|------|-------------|
| GET | /intrafi_account_enrollments | List IntraFi Account Enrollments |
| POST | /intrafi_account_enrollments | Enroll an account in the IntraFi deposit sweep network |
| GET | /intrafi_account_enrollments/{intrafi_account_enrollment_id} | Get an IntraFi Account Enrollment |
| POST | /intrafi_account_enrollments/{intrafi_account_enrollment_id}/unenroll | Unenroll an account from IntraFi |

### intrafi_exclusions
| Method | Path | Description |
|--------|------|-------------|
| GET | /intrafi_exclusions | List IntraFi Exclusions |
| POST | /intrafi_exclusions | Create an IntraFi Exclusion |
| GET | /intrafi_exclusions/{intrafi_exclusion_id} | Get an IntraFi Exclusion |
| POST | /intrafi_exclusions/{intrafi_exclusion_id}/archive | Archive an IntraFi Exclusion |

### lockboxes
| Method | Path | Description |
|--------|------|-------------|
| GET | /lockboxes | List Lockboxes |
| POST | /lockboxes | Create a Lockbox |
| GET | /lockboxes/{lockbox_id} | Retrieve a Lockbox |
| PATCH | /lockboxes/{lockbox_id} | Update a Lockbox |

### oauth
| Method | Path | Description |
|--------|------|-------------|
| POST | /oauth/tokens | Create an OAuth Token |

### oauth_applications
| Method | Path | Description |
|--------|------|-------------|
| GET | /oauth_applications | List OAuth Applications |
| GET | /oauth_applications/{oauth_application_id} | Retrieve an OAuth Application |

### oauth_connections
| Method | Path | Description |
|--------|------|-------------|
| GET | /oauth_connections | List OAuth Connections |
| GET | /oauth_connections/{oauth_connection_id} | Retrieve an OAuth Connection |

### pending_transactions
| Method | Path | Description |
|--------|------|-------------|
| GET | /pending_transactions | List Pending Transactions |
| POST | /pending_transactions | Create a Pending Transaction |
| GET | /pending_transactions/{pending_transaction_id} | Retrieve a Pending Transaction |
| POST | /pending_transactions/{pending_transaction_id}/release | Release a user-initiated Pending Transaction |

### physical_card_profiles
| Method | Path | Description |
|--------|------|-------------|
| GET | /physical_card_profiles | List Physical Card Profiles |
| POST | /physical_card_profiles | Create a Physical Card Profile |
| GET | /physical_card_profiles/{physical_card_profile_id} | Retrieve a Card Profile |
| POST | /physical_card_profiles/{physical_card_profile_id}/archive | Archive a Physical Card Profile |
| POST | /physical_card_profiles/{physical_card_profile_id}/clone | Clone a Physical Card Profile |

### physical_cards
| Method | Path | Description |
|--------|------|-------------|
| GET | /physical_cards | List Physical Cards |
| POST | /physical_cards | Create a Physical Card |
| GET | /physical_cards/{physical_card_id} | Retrieve a Physical Card |
| PATCH | /physical_cards/{physical_card_id} | Update a Physical Card |

### programs
| Method | Path | Description |
|--------|------|-------------|
| GET | /programs | List Programs |
| GET | /programs/{program_id} | Retrieve a Program |

### real_time_decisions
| Method | Path | Description |
|--------|------|-------------|
| GET | /real_time_decisions/{real_time_decision_id} | Retrieve a Real-Time Decision |
| POST | /real_time_decisions/{real_time_decision_id}/action | Action a Real-Time Decision |

### real_time_payments_transfers
| Method | Path | Description |
|--------|------|-------------|
| GET | /real_time_payments_transfers | List Real-Time Payments Transfers |
| POST | /real_time_payments_transfers | Create a Real-Time Payments Transfer |
| GET | /real_time_payments_transfers/{real_time_payments_transfer_id} | Retrieve a Real-Time Payments Transfer |
| POST | /real_time_payments_transfers/{real_time_payments_transfer_id}/approve | Approve a Real-Time Payments Transfer |
| POST | /real_time_payments_transfers/{real_time_payments_transfer_id}/cancel | Cancel a pending Real-Time Payments Transfer |

### routing_numbers
| Method | Path | Description |
|--------|------|-------------|
| GET | /routing_numbers | List Routing Numbers |

### simulations
| Method | Path | Description |
|--------|------|-------------|
| POST | /simulations/account_statements | Sandbox: Create an Account Statement |
| POST | /simulations/account_transfers/{account_transfer_id}/complete | Sandbox: Approve an Account Transfer |
| POST | /simulations/ach_transfers/{ach_transfer_id}/acknowledge | Sandbox: Acknowledge an ACH Transfer |
| POST | /simulations/ach_transfers/{ach_transfer_id}/create_notification_of_change | Sandbox: Create a Notification of Change for an ACH Transfer |
| POST | /simulations/ach_transfers/{ach_transfer_id}/return | Sandbox: Return an ACH Transfer |
| POST | /simulations/ach_transfers/{ach_transfer_id}/settle | Sandbox: Settle an ACH Transfer |
| POST | /simulations/ach_transfers/{ach_transfer_id}/submit | Sandbox: Submit an ACH Transfer |
| POST | /simulations/card_authorization_expirations | Sandbox: Expire a Card Authorization |
| POST | /simulations/card_authorizations | Sandbox: Create a Card Authorization |
| POST | /simulations/card_balance_inquiries | Sandbox: Create a Card Balance Inquiry |
| POST | /simulations/card_disputes/{card_dispute_id}/action | Sandbox: Advance the state of a Card Dispute |
| POST | /simulations/card_fuel_confirmations | Sandbox: Confirm the fuel pump amount for a Card Authorization |
| POST | /simulations/card_increments | Sandbox: Increment a Card Authorization |
| POST | /simulations/card_refunds | Sandbox: Refund a card transaction |
| POST | /simulations/card_reversals | Sandbox: Reverse a Card Authorization |
| POST | /simulations/card_settlements | Sandbox: Settle a Card Authorization |
| POST | /simulations/card_tokens | Sandbox: Create a Card Token |
| POST | /simulations/check_deposits/{check_deposit_id}/reject | Sandbox: Reject a Check Deposit |
| POST | /simulations/check_deposits/{check_deposit_id}/return | Sandbox: Return a Check Deposit |
| POST | /simulations/check_deposits/{check_deposit_id}/submit | Sandbox: Submit a Check Deposit |
| POST | /simulations/check_transfers/{check_transfer_id}/mail | Sandbox: Mail a Check Transfer |
| POST | /simulations/digital_wallet_token_requests | Sandbox: Create a digital wallet token request |
| POST | /simulations/exports | Sandbox: Generate a Tax Form Export |
| POST | /simulations/inbound_ach_transfers | Sandbox: Create an Inbound ACH Transfer |
| POST | /simulations/inbound_check_deposits | Sandbox: Create an Inbound Check Deposit |
| POST | /simulations/inbound_fednow_transfers | Sandbox: Create an Inbound FedNow Transfer |
| POST | /simulations/inbound_mail_items | Sandbox: Create an Inbound Mail Item |
| POST | /simulations/inbound_real_time_payments_transfers | Sandbox: Create an Inbound Real-Time Payments Transfer |
| POST | /simulations/inbound_wire_drawdown_requests | Sandbox: Create an Inbound Wire Drawdown request |
| POST | /simulations/inbound_wire_transfers | Sandbox: Create an Inbound Wire Transfer |
| POST | /simulations/interest_payments | Sandbox: Create an interest payment |
| POST | /simulations/pending_transactions/{pending_transaction_id}/release_inbound_funds_hold | Sandbox: Release an Inbound Funds Hold |
| POST | /simulations/physical_cards/{physical_card_id}/advance_shipment | Sandbox: Advance the shipment status of a Physical Card |
| POST | /simulations/physical_cards/{physical_card_id}/tracking_updates | Sandbox: Create a Physical Card Shipment Tracking Update |
| POST | /simulations/programs | Sandbox: Create a Program |
| POST | /simulations/real_time_payments_transfers/{real_time_payments_transfer_id}/complete | Sandbox: Complete a Real-Time Payments Transfer |
| POST | /simulations/wire_drawdown_requests/{wire_drawdown_request_id}/refuse | Sandbox: Refuse a Wire Drawdown Request |
| POST | /simulations/wire_drawdown_requests/{wire_drawdown_request_id}/submit | Sandbox: Submit a Wire Drawdown Request |
| POST | /simulations/wire_transfers/{wire_transfer_id}/reverse | Sandbox: Reverse a Wire Transfer |
| POST | /simulations/wire_transfers/{wire_transfer_id}/submit | Sandbox: Submit a Wire Transfer |

### swift_transfers
| Method | Path | Description |
|--------|------|-------------|
| GET | /swift_transfers | List Swift Transfers |
| POST | /swift_transfers | Create a Swift Transfer |
| GET | /swift_transfers/{swift_transfer_id} | Retrieve a Swift Transfer |
| POST | /swift_transfers/{swift_transfer_id}/approve | Approve a Swift Transfer |
| POST | /swift_transfers/{swift_transfer_id}/cancel | Cancel a pending Swift Transfer |

### transactions
| Method | Path | Description |
|--------|------|-------------|
| GET | /transactions | List Transactions |
| GET | /transactions/{transaction_id} | Retrieve a Transaction |

### wire_drawdown_requests
| Method | Path | Description |
|--------|------|-------------|
| GET | /wire_drawdown_requests | List Wire Drawdown Requests |
| POST | /wire_drawdown_requests | Create a Wire Drawdown Request |
| GET | /wire_drawdown_requests/{wire_drawdown_request_id} | Retrieve a Wire Drawdown Request |

### wire_transfers
| Method | Path | Description |
|--------|------|-------------|
| GET | /wire_transfers | List Wire Transfers |
| POST | /wire_transfers | Create a Wire Transfer |
| GET | /wire_transfers/{wire_transfer_id} | Retrieve a Wire Transfer |
| POST | /wire_transfers/{wire_transfer_id}/approve | Approve a Wire Transfer |
| POST | /wire_transfers/{wire_transfer_id}/cancel | Cancel a pending Wire Transfer |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all account_numbers?" -> GET /account_numbers
- "Create a account_number?" -> POST /account_numbers
- "Get account_number details?" -> GET /account_numbers/{account_number_id}
- "Partially update a account_number?" -> PATCH /account_numbers/{account_number_id}
- "List all account_statements?" -> GET /account_statements
- "Get account_statement details?" -> GET /account_statements/{account_statement_id}
- "List all account_transfers?" -> GET /account_transfers
- "Create a account_transfer?" -> POST /account_transfers
- "Get account_transfer details?" -> GET /account_transfers/{account_transfer_id}
- "Create a approve?" -> POST /account_transfers/{account_transfer_id}/approve
- "Create a cancel?" -> POST /account_transfers/{account_transfer_id}/cancel
- "List all accounts?" -> GET /accounts
- "Create a account?" -> POST /accounts
- "Get account details?" -> GET /accounts/{account_id}
- "Partially update a account?" -> PATCH /accounts/{account_id}
- "List all balance?" -> GET /accounts/{account_id}/balance
- "Create a close?" -> POST /accounts/{account_id}/close
- "List all intrafi_balance?" -> GET /accounts/{account_id}/intrafi_balance
- "List all ach_prenotifications?" -> GET /ach_prenotifications
- "Create a ach_prenotification?" -> POST /ach_prenotifications
- "Get ach_prenotification details?" -> GET /ach_prenotifications/{ach_prenotification_id}
- "List all ach_transfers?" -> GET /ach_transfers
- "Create a ach_transfer?" -> POST /ach_transfers
- "Get ach_transfer details?" -> GET /ach_transfers/{ach_transfer_id}
- "Create a approve?" -> POST /ach_transfers/{ach_transfer_id}/approve
- "Create a cancel?" -> POST /ach_transfers/{ach_transfer_id}/cancel
- "List all bookkeeping_accounts?" -> GET /bookkeeping_accounts
- "Create a bookkeeping_account?" -> POST /bookkeeping_accounts
- "Partially update a bookkeeping_account?" -> PATCH /bookkeeping_accounts/{bookkeeping_account_id}
- "List all balance?" -> GET /bookkeeping_accounts/{bookkeeping_account_id}/balance
- "List all bookkeeping_entries?" -> GET /bookkeeping_entries
- "Get bookkeeping_entry details?" -> GET /bookkeeping_entries/{bookkeeping_entry_id}
- "List all bookkeeping_entry_sets?" -> GET /bookkeeping_entry_sets
- "Create a bookkeeping_entry_set?" -> POST /bookkeeping_entry_sets
- "Get bookkeeping_entry_set details?" -> GET /bookkeeping_entry_sets/{bookkeeping_entry_set_id}
- "List all card_disputes?" -> GET /card_disputes
- "Create a card_dispute?" -> POST /card_disputes
- "Get card_dispute details?" -> GET /card_disputes/{card_dispute_id}
- "Create a submit_user_submission?" -> POST /card_disputes/{card_dispute_id}/submit_user_submission
- "Create a withdraw?" -> POST /card_disputes/{card_dispute_id}/withdraw
- "List all card_payments?" -> GET /card_payments
- "Get card_payment details?" -> GET /card_payments/{card_payment_id}
- "List all card_purchase_supplements?" -> GET /card_purchase_supplements
- "Get card_purchase_supplement details?" -> GET /card_purchase_supplements/{card_purchase_supplement_id}
- "List all card_push_transfers?" -> GET /card_push_transfers
- "Create a card_push_transfer?" -> POST /card_push_transfers
- "Get card_push_transfer details?" -> GET /card_push_transfers/{card_push_transfer_id}
- "Create a approve?" -> POST /card_push_transfers/{card_push_transfer_id}/approve
- "Create a cancel?" -> POST /card_push_transfers/{card_push_transfer_id}/cancel
- "List all card_tokens?" -> GET /card_tokens
- "Get card_token details?" -> GET /card_tokens/{card_token_id}
- "List all capabilities?" -> GET /card_tokens/{card_token_id}/capabilities
- "List all card_validations?" -> GET /card_validations
- "Create a card_validation?" -> POST /card_validations
- "Get card_validation details?" -> GET /card_validations/{card_validation_id}
- "List all cards?" -> GET /cards
- "Create a card?" -> POST /cards
- "Get card details?" -> GET /cards/{card_id}
- "Partially update a card?" -> PATCH /cards/{card_id}
- "Create a create_details_iframe?" -> POST /cards/{card_id}/create_details_iframe
- "List all details?" -> GET /cards/{card_id}/details
- "Create a update_pin?" -> POST /cards/{card_id}/update_pin
- "List all check_deposits?" -> GET /check_deposits
- "Create a check_deposit?" -> POST /check_deposits
- "Get check_deposit details?" -> GET /check_deposits/{check_deposit_id}
- "List all check_transfers?" -> GET /check_transfers
- "Create a check_transfer?" -> POST /check_transfers
- "Get check_transfer details?" -> GET /check_transfers/{check_transfer_id}
- "Create a approve?" -> POST /check_transfers/{check_transfer_id}/approve
- "Create a cancel?" -> POST /check_transfers/{check_transfer_id}/cancel
- "Create a stop_payment?" -> POST /check_transfers/{check_transfer_id}/stop_payment
- "List all declined_transactions?" -> GET /declined_transactions
- "Get declined_transaction details?" -> GET /declined_transactions/{declined_transaction_id}
- "List all digital_card_profiles?" -> GET /digital_card_profiles
- "Create a digital_card_profile?" -> POST /digital_card_profiles
- "Get digital_card_profile details?" -> GET /digital_card_profiles/{digital_card_profile_id}
- "Create a archive?" -> POST /digital_card_profiles/{digital_card_profile_id}/archive
- "Create a clone?" -> POST /digital_card_profiles/{digital_card_profile_id}/clone
- "List all digital_wallet_tokens?" -> GET /digital_wallet_tokens
- "Get digital_wallet_token details?" -> GET /digital_wallet_tokens/{digital_wallet_token_id}
- "List all entities?" -> GET /entities
- "Create a entity?" -> POST /entities
- "Get entity details?" -> GET /entities/{entity_id}
- "Partially update a entity?" -> PATCH /entities/{entity_id}
- "Create a archive?" -> POST /entities/{entity_id}/archive
- "Create a archive_beneficial_owner?" -> POST /entities/{entity_id}/archive_beneficial_owner
- "Create a confirm?" -> POST /entities/{entity_id}/confirm
- "Create a create_beneficial_owner?" -> POST /entities/{entity_id}/create_beneficial_owner
- "Create a update_address?" -> POST /entities/{entity_id}/update_address
- "Create a update_beneficial_owner_address?" -> POST /entities/{entity_id}/update_beneficial_owner_address
- "Create a update_industry_code?" -> POST /entities/{entity_id}/update_industry_code
- "List all entity_supplemental_documents?" -> GET /entity_supplemental_documents
- "Create a entity_supplemental_document?" -> POST /entity_supplemental_documents
- "List all event_subscriptions?" -> GET /event_subscriptions
- "Create a event_subscription?" -> POST /event_subscriptions
- "Get event_subscription details?" -> GET /event_subscriptions/{event_subscription_id}
- "Partially update a event_subscription?" -> PATCH /event_subscriptions/{event_subscription_id}
- "List all events?" -> GET /events
- "Get event details?" -> GET /events/{event_id}
- "List all exports?" -> GET /exports
- "Create a export?" -> POST /exports
- "Get export details?" -> GET /exports/{export_id}
- "List all external_accounts?" -> GET /external_accounts
- "Create a external_account?" -> POST /external_accounts
- "Get external_account details?" -> GET /external_accounts/{external_account_id}
- "Partially update a external_account?" -> PATCH /external_accounts/{external_account_id}
- "List all fednow_transfers?" -> GET /fednow_transfers
- "Create a fednow_transfer?" -> POST /fednow_transfers
- "Get fednow_transfer details?" -> GET /fednow_transfers/{fednow_transfer_id}
- "Create a approve?" -> POST /fednow_transfers/{fednow_transfer_id}/approve
- "Create a cancel?" -> POST /fednow_transfers/{fednow_transfer_id}/cancel
- "Create a file_link?" -> POST /file_links
- "List all files?" -> GET /files
- "Create a file?" -> POST /files
- "Get file details?" -> GET /files/{file_id}
- "List all current?" -> GET /groups/current
- "List all inbound_ach_transfers?" -> GET /inbound_ach_transfers
- "Get inbound_ach_transfer details?" -> GET /inbound_ach_transfers/{inbound_ach_transfer_id}
- "Create a create_notification_of_change?" -> POST /inbound_ach_transfers/{inbound_ach_transfer_id}/create_notification_of_change
- "Create a decline?" -> POST /inbound_ach_transfers/{inbound_ach_transfer_id}/decline
- "Create a transfer_return?" -> POST /inbound_ach_transfers/{inbound_ach_transfer_id}/transfer_return
- "List all inbound_check_deposits?" -> GET /inbound_check_deposits
- "Get inbound_check_deposit details?" -> GET /inbound_check_deposits/{inbound_check_deposit_id}
- "Create a decline?" -> POST /inbound_check_deposits/{inbound_check_deposit_id}/decline
- "Create a return?" -> POST /inbound_check_deposits/{inbound_check_deposit_id}/return
- "List all inbound_fednow_transfers?" -> GET /inbound_fednow_transfers
- "Get inbound_fednow_transfer details?" -> GET /inbound_fednow_transfers/{inbound_fednow_transfer_id}
- "List all inbound_mail_items?" -> GET /inbound_mail_items
- "Get inbound_mail_item details?" -> GET /inbound_mail_items/{inbound_mail_item_id}
- "Create a action?" -> POST /inbound_mail_items/{inbound_mail_item_id}/action
- "List all inbound_real_time_payments_transfers?" -> GET /inbound_real_time_payments_transfers
- "Get inbound_real_time_payments_transfer details?" -> GET /inbound_real_time_payments_transfers/{inbound_real_time_payments_transfer_id}
- "List all inbound_wire_drawdown_requests?" -> GET /inbound_wire_drawdown_requests
- "Get inbound_wire_drawdown_request details?" -> GET /inbound_wire_drawdown_requests/{inbound_wire_drawdown_request_id}
- "List all inbound_wire_transfers?" -> GET /inbound_wire_transfers
- "Get inbound_wire_transfer details?" -> GET /inbound_wire_transfers/{inbound_wire_transfer_id}
- "Create a reverse?" -> POST /inbound_wire_transfers/{inbound_wire_transfer_id}/reverse
- "List all intrafi_account_enrollments?" -> GET /intrafi_account_enrollments
- "Create a intrafi_account_enrollment?" -> POST /intrafi_account_enrollments
- "Get intrafi_account_enrollment details?" -> GET /intrafi_account_enrollments/{intrafi_account_enrollment_id}
- "Create a unenroll?" -> POST /intrafi_account_enrollments/{intrafi_account_enrollment_id}/unenroll
- "List all intrafi_exclusions?" -> GET /intrafi_exclusions
- "Create a intrafi_exclusion?" -> POST /intrafi_exclusions
- "Get intrafi_exclusion details?" -> GET /intrafi_exclusions/{intrafi_exclusion_id}
- "Create a archive?" -> POST /intrafi_exclusions/{intrafi_exclusion_id}/archive
- "List all lockboxes?" -> GET /lockboxes
- "Create a lockboxe?" -> POST /lockboxes
- "Get lockboxe details?" -> GET /lockboxes/{lockbox_id}
- "Partially update a lockboxe?" -> PATCH /lockboxes/{lockbox_id}
- "Create a token?" -> POST /oauth/tokens
- "List all oauth_applications?" -> GET /oauth_applications
- "Get oauth_application details?" -> GET /oauth_applications/{oauth_application_id}
- "List all oauth_connections?" -> GET /oauth_connections
- "Get oauth_connection details?" -> GET /oauth_connections/{oauth_connection_id}
- "List all pending_transactions?" -> GET /pending_transactions
- "Create a pending_transaction?" -> POST /pending_transactions
- "Get pending_transaction details?" -> GET /pending_transactions/{pending_transaction_id}
- "Create a release?" -> POST /pending_transactions/{pending_transaction_id}/release
- "List all physical_card_profiles?" -> GET /physical_card_profiles
- "Create a physical_card_profile?" -> POST /physical_card_profiles
- "Get physical_card_profile details?" -> GET /physical_card_profiles/{physical_card_profile_id}
- "Create a archive?" -> POST /physical_card_profiles/{physical_card_profile_id}/archive
- "Create a clone?" -> POST /physical_card_profiles/{physical_card_profile_id}/clone
- "List all physical_cards?" -> GET /physical_cards
- "Create a physical_card?" -> POST /physical_cards
- "Get physical_card details?" -> GET /physical_cards/{physical_card_id}
- "Partially update a physical_card?" -> PATCH /physical_cards/{physical_card_id}
- "List all programs?" -> GET /programs
- "Get program details?" -> GET /programs/{program_id}
- "Get real_time_decision details?" -> GET /real_time_decisions/{real_time_decision_id}
- "Create a action?" -> POST /real_time_decisions/{real_time_decision_id}/action
- "List all real_time_payments_transfers?" -> GET /real_time_payments_transfers
- "Create a real_time_payments_transfer?" -> POST /real_time_payments_transfers
- "Get real_time_payments_transfer details?" -> GET /real_time_payments_transfers/{real_time_payments_transfer_id}
- "Create a approve?" -> POST /real_time_payments_transfers/{real_time_payments_transfer_id}/approve
- "Create a cancel?" -> POST /real_time_payments_transfers/{real_time_payments_transfer_id}/cancel
- "List all routing_numbers?" -> GET /routing_numbers
- "Create a account_statement?" -> POST /simulations/account_statements
- "Create a complete?" -> POST /simulations/account_transfers/{account_transfer_id}/complete
- "Create a acknowledge?" -> POST /simulations/ach_transfers/{ach_transfer_id}/acknowledge
- "Create a create_notification_of_change?" -> POST /simulations/ach_transfers/{ach_transfer_id}/create_notification_of_change
- "Create a return?" -> POST /simulations/ach_transfers/{ach_transfer_id}/return
- "Create a settle?" -> POST /simulations/ach_transfers/{ach_transfer_id}/settle
- "Create a submit?" -> POST /simulations/ach_transfers/{ach_transfer_id}/submit
- "Create a card_authorization_expiration?" -> POST /simulations/card_authorization_expirations
- "Create a card_authorization?" -> POST /simulations/card_authorizations
- "Create a card_balance_inquiry?" -> POST /simulations/card_balance_inquiries
- "Create a action?" -> POST /simulations/card_disputes/{card_dispute_id}/action
- "Create a card_fuel_confirmation?" -> POST /simulations/card_fuel_confirmations
- "Create a card_increment?" -> POST /simulations/card_increments
- "Create a card_refund?" -> POST /simulations/card_refunds
- "Create a card_reversal?" -> POST /simulations/card_reversals
- "Create a card_settlement?" -> POST /simulations/card_settlements
- "Create a card_token?" -> POST /simulations/card_tokens
- "Create a reject?" -> POST /simulations/check_deposits/{check_deposit_id}/reject
- "Create a return?" -> POST /simulations/check_deposits/{check_deposit_id}/return
- "Create a submit?" -> POST /simulations/check_deposits/{check_deposit_id}/submit
- "Create a mail?" -> POST /simulations/check_transfers/{check_transfer_id}/mail
- "Create a digital_wallet_token_request?" -> POST /simulations/digital_wallet_token_requests
- "Create a export?" -> POST /simulations/exports
- "Create a inbound_ach_transfer?" -> POST /simulations/inbound_ach_transfers
- "Create a inbound_check_deposit?" -> POST /simulations/inbound_check_deposits
- "Create a inbound_fednow_transfer?" -> POST /simulations/inbound_fednow_transfers
- "Create a inbound_mail_item?" -> POST /simulations/inbound_mail_items
- "Create a inbound_real_time_payments_transfer?" -> POST /simulations/inbound_real_time_payments_transfers
- "Create a inbound_wire_drawdown_request?" -> POST /simulations/inbound_wire_drawdown_requests
- "Create a inbound_wire_transfer?" -> POST /simulations/inbound_wire_transfers
- "Create a interest_payment?" -> POST /simulations/interest_payments
- "Create a release_inbound_funds_hold?" -> POST /simulations/pending_transactions/{pending_transaction_id}/release_inbound_funds_hold
- "Create a advance_shipment?" -> POST /simulations/physical_cards/{physical_card_id}/advance_shipment
- "Create a tracking_update?" -> POST /simulations/physical_cards/{physical_card_id}/tracking_updates
- "Create a program?" -> POST /simulations/programs
- "Create a complete?" -> POST /simulations/real_time_payments_transfers/{real_time_payments_transfer_id}/complete
- "Create a refuse?" -> POST /simulations/wire_drawdown_requests/{wire_drawdown_request_id}/refuse
- "Create a submit?" -> POST /simulations/wire_drawdown_requests/{wire_drawdown_request_id}/submit
- "Create a reverse?" -> POST /simulations/wire_transfers/{wire_transfer_id}/reverse
- "Create a submit?" -> POST /simulations/wire_transfers/{wire_transfer_id}/submit
- "List all swift_transfers?" -> GET /swift_transfers
- "Create a swift_transfer?" -> POST /swift_transfers
- "Get swift_transfer details?" -> GET /swift_transfers/{swift_transfer_id}
- "Create a approve?" -> POST /swift_transfers/{swift_transfer_id}/approve
- "Create a cancel?" -> POST /swift_transfers/{swift_transfer_id}/cancel
- "List all transactions?" -> GET /transactions
- "Get transaction details?" -> GET /transactions/{transaction_id}
- "List all wire_drawdown_requests?" -> GET /wire_drawdown_requests
- "Create a wire_drawdown_request?" -> POST /wire_drawdown_requests
- "Get wire_drawdown_request details?" -> GET /wire_drawdown_requests/{wire_drawdown_request_id}
- "List all wire_transfers?" -> GET /wire_transfers
- "Create a wire_transfer?" -> POST /wire_transfers
- "Get wire_transfer details?" -> GET /wire_transfers/{wire_transfer_id}
- "Create a approve?" -> POST /wire_transfers/{wire_transfer_id}/approve
- "Create a cancel?" -> POST /wire_transfers/{wire_transfer_id}/cancel
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
