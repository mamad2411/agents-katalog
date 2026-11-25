---
name: bunq-api
description: "bunq API skill. Use when working with bunq for user, attachment-public, avatar. Covers 480 endpoints."
version: 1.0.0
generator: lapsh
---

# bunq API
API version: 1.0

## Auth
ApiKey X-Bunq-Client-Authentication in header

## Base URL
https://public-api.sandbox.bunq.com/v1

## Setup
1. Set your API key in the appropriate header
2. GET /device -- verify access
3. POST /user/{userID}/additional-transaction-information-category-user-defined -- create first additional-transaction-information-category-user-defined

## Endpoints

480 endpoints across 16 groups. See references/api-spec.lap for full details.

### user
| Method | Path | Description |
|--------|------|-------------|
| GET | /user/{userID}/additional-transaction-information-category | Get the available categories. |
| POST | /user/{userID}/additional-transaction-information-category-user-defined | Manage user-defined categories. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/attachment | Create a new monetary account attachment. Create a POST request with a payload that contains the binary representation of the file, without any JSON wrapping. Make sure you define the MIME type (i.e. image/jpeg) in the Content-Type header. You are required to provide a description of the attachment using the X-Bunq-Attachment-Description header. |
| GET | /user/{userID}/attachment/{itemId} | Get a specific attachment. The header of the response contains the content-type of the attachment. |
| GET | /user/{userID}/billing-contract-subscription | Get all subscription billing contract for the authenticated user. |
| GET | /user/{userID}/bunqme-fundraiser-profile/{itemId} | bunq.me public profile of the user. |
| GET | /user/{userID}/bunqme-fundraiser-profile | bunq.me public profile of the user. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/bunqme-fundraiser-result/{itemId} | bunq.me fundraiser result containing all payments. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/bunqme-tab | bunq.me tabs allows you to create a payment request and share the link through e-mail, chat, etc. Multiple persons are able to respond to the payment request and pay through bunq, iDeal or SOFORT. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/bunqme-tab | bunq.me tabs allows you to create a payment request and share the link through e-mail, chat, etc. Multiple persons are able to respond to the payment request and pay through bunq, iDeal or SOFORT. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/bunqme-tab/{itemId} | bunq.me tabs allows you to create a payment request and share the link through e-mail, chat, etc. Multiple persons are able to respond to the payment request and pay through bunq, iDeal or SOFORT. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/bunqme-tab/{itemId} | bunq.me tabs allows you to create a payment request and share the link through e-mail, chat, etc. Multiple persons are able to respond to the payment request and pay through bunq, iDeal or SOFORT. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/bunqme-tab-result-response/{itemId} | Used to view bunq.me TabResultResponse objects belonging to a tab. A TabResultResponse is an object that holds details on a tab which has been paid from the provided monetary account. |
| GET | /user/{userID}/oauth-client/{oauth-clientID}/callback-url/{itemId} | Used for managing OAuth Client Callback URLs. |
| PUT | /user/{userID}/oauth-client/{oauth-clientID}/callback-url/{itemId} | Used for managing OAuth Client Callback URLs. |
| DELETE | /user/{userID}/oauth-client/{oauth-clientID}/callback-url/{itemId} | Used for managing OAuth Client Callback URLs. |
| POST | /user/{userID}/oauth-client/{oauth-clientID}/callback-url | Used for managing OAuth Client Callback URLs. |
| GET | /user/{userID}/oauth-client/{oauth-clientID}/callback-url | Used for managing OAuth Client Callback URLs. |
| PUT | /user/{userID}/card/{itemId} | Update the card details. Allow to change pin code, status, limits, country permissions and the monetary account connected to the card. When the card has been received, it can be also activated through this endpoint. |
| GET | /user/{userID}/card/{itemId} | Return the details of a specific card. |
| GET | /user/{userID}/card | Return all the cards available to the user. |
| POST | /user/{userID}/card-batch | Used to update multiple cards in a batch. |
| POST | /user/{userID}/card-batch-replace | Used to replace multiple cards in a batch. |
| POST | /user/{userID}/card-credit | Create a new credit card request. |
| POST | /user/{userID}/card-debit | Create a new debit card request. |
| GET | /user/{userID}/card-name | Return all the accepted card names for a specific user. |
| POST | /user/{userID}/certificate-pinned | Pin the certificate chain. |
| GET | /user/{userID}/certificate-pinned | List all the pinned certificate chain for the given user. |
| DELETE | /user/{userID}/certificate-pinned/{itemId} | Remove the pinned certificate chain with the specific ID. |
| GET | /user/{userID}/certificate-pinned/{itemId} | Get the pinned certificate chain with the specified ID. |
| GET | /user/{userID}/challenge-request/{itemId} | Endpoint for apps to fetch a challenge request. |
| PUT | /user/{userID}/challenge-request/{itemId} | Endpoint for apps to fetch a challenge request. |
| POST | /user/{userID}/company | Create and manage companies. |
| GET | /user/{userID}/company | Create and manage companies. |
| GET | /user/{userID}/company/{itemId} | Create and manage companies. |
| PUT | /user/{userID}/company/{itemId} | Create and manage companies. |
| POST | /user/{userID}/confirmation-of-funds | Used to confirm availability of funds on an account. |
| GET | /user/{userID}/chat-conversation/{chat-conversationID}/attachment/{attachmentID}/content | Get the raw content of a specific attachment. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/attachment/{attachmentID}/content | Get the raw content of a specific attachment. |
| GET | /user/{userID}/attachment/{attachmentID}/content | Get the raw content of a specific attachment. |
| GET | /user/{userID}/export-annual-overview/{export-annual-overviewID}/content | Used to retrieve the raw content of an annual overview. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/export-rib/{export-ribID}/content | Used to retrieve the raw content of an RIB. |
| GET | /user/{userID}/card/{cardID}/export-statement-card/{export-statement-cardID}/content | Fetch the raw content of a card statement export. The returned file format could be CSV or PDF depending on the statement format specified during the statement creation. The doc won't display the response of a request to get the content of a statement export. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/customer-statement/{customer-statementID}/content | Fetch the raw content of a statement export. The returned file format could be MT940, CSV or PDF depending on the statement format specified during the statement creation. The doc won't display the response of a request to get the content of a statement export. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/event/{eventID}/statement/{statementID}/content | Fetch the raw content of a payment statement export. |
| GET | /user/{userID}/credential-password-ip/{itemId} | Create a credential of a user for server authentication, or delete the credential of a user for server authentication. |
| GET | /user/{userID}/credential-password-ip | Create a credential of a user for server authentication, or delete the credential of a user for server authentication. |
| POST | /user/{userID}/currency-cloud-beneficiary | Endpoint to manage CurrencyCloud beneficiaries. |
| GET | /user/{userID}/currency-cloud-beneficiary | Endpoint to manage CurrencyCloud beneficiaries. |
| GET | /user/{userID}/currency-cloud-beneficiary/{itemId} | Endpoint to manage CurrencyCloud beneficiaries. |
| GET | /user/{userID}/currency-cloud-beneficiary-requirement | Endpoint to list requirements for CurrencyCloud beneficiaries. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/currency-cloud-payment-quote | Endpoint for managing currency conversions. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/currency-conversion | Endpoint for managing currency conversions. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/currency-conversion/{itemId} | Endpoint for managing currency conversions. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/currency-conversion-quote | Endpoint to create a quote for currency conversions. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/currency-conversion-quote/{itemId} | Endpoint to create a quote for currency conversions. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/currency-conversion-quote/{itemId} | Endpoint to create a quote for currency conversions. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/customer-statement | Used to create new and read existing statement exports. Statement exports can be created in either CSV, MT940 or PDF file format. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/customer-statement | Used to create new and read existing statement exports. Statement exports can be created in either CSV, MT940 or PDF file format. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/customer-statement/{itemId} | Used to create new and read existing statement exports. Statement exports can be created in either CSV, MT940 or PDF file format. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/customer-statement/{itemId} | Used to create new and read existing statement exports. Statement exports can be created in either CSV, MT940 or PDF file format. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/payment-auto-allocate/{payment-auto-allocateID}/definition | List all the definitions in a payment auto allocate. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/draft-payment | Create a new DraftPayment. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/draft-payment | Get a listing of all DraftPayments from a given MonetaryAccount. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/draft-payment/{itemId} | Update a DraftPayment. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/draft-payment/{itemId} | Get a specific DraftPayment. |
| GET | /user/{userID}/event/{itemId} | Get a specific event for a given user. |
| GET | /user/{userID}/event | Get a collection of events for a given user. You can add query the parameters monetary_account_id, status and/or display_user_event to filter the response. When monetary_account_id={id,id} is provided only events that relate to these monetary account ids are returned. When status={AWAITING_REPLY/FINALIZED} is provided the response only contains events with the status AWAITING_REPLY or FINALIZED. When display_user_event={true/false} is set to false user events are excluded from the response, when not provided user events are displayed. User events are events that are not related to a monetary account (for example: connect invites). |
| POST | /user/{userID}/export-annual-overview | Create a new annual overview for a specific year. An overview can be generated only for a past year. |
| GET | /user/{userID}/export-annual-overview | List all the annual overviews for a user. |
| GET | /user/{userID}/export-annual-overview/{itemId} | Get an annual overview for a user by its id. |
| DELETE | /user/{userID}/export-annual-overview/{itemId} | Used to create new and read existing annual overviews of all the user's monetary accounts. Once created, annual overviews can be downloaded in PDF format via the 'export-annual-overview/{id}/content' endpoint. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/export-rib | Create a new RIB. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/export-rib | List all the RIBs for a monetary account. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/export-rib/{itemId} | Get a RIB for a monetary account by its id. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/export-rib/{itemId} | Used to create new and read existing RIBs of a monetary account |
| GET | /user/{userID}/card/{cardID}/export-statement-card/{itemId} | Used to create new and read existing card statement exports. Statement exports can be created in either CSV or PDF file format. |
| GET | /user/{userID}/card/{cardID}/export-statement-card | Used to create new and read existing card statement exports. Statement exports can be created in either CSV or PDF file format. |
| POST | /user/{userID}/card/{cardID}/export-statement-card-csv | Used to serialize ExportStatementCardCsv |
| GET | /user/{userID}/card/{cardID}/export-statement-card-csv | Used to serialize ExportStatementCardCsv |
| GET | /user/{userID}/card/{cardID}/export-statement-card-csv/{itemId} | Used to serialize ExportStatementCardCsv |
| DELETE | /user/{userID}/card/{cardID}/export-statement-card-csv/{itemId} | Used to serialize ExportStatementCardCsv |
| POST | /user/{userID}/card/{cardID}/export-statement-card-pdf | Used to serialize ExportStatementCardPdf |
| GET | /user/{userID}/card/{cardID}/export-statement-card-pdf | Used to serialize ExportStatementCardPdf |
| GET | /user/{userID}/card/{cardID}/export-statement-card-pdf/{itemId} | Used to serialize ExportStatementCardPdf |
| DELETE | /user/{userID}/card/{cardID}/export-statement-card-pdf/{itemId} | Used to serialize ExportStatementCardPdf |
| GET | /user/{userID}/feature-announcement/{itemId} | view for updating the feature display. |
| POST | /user/{userID}/card/{cardID}/generated-cvc2 | Generate a new CVC2 code for a card. |
| GET | /user/{userID}/card/{cardID}/generated-cvc2 | Get all generated CVC2 codes for a card. |
| GET | /user/{userID}/card/{cardID}/generated-cvc2/{itemId} | Get the details for a specific generated CVC2 code. |
| PUT | /user/{userID}/card/{cardID}/generated-cvc2/{itemId} | Endpoint for generating and retrieving a new CVC2 code. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/ideal-merchant-transaction | View for requesting iDEAL transactions and polling their status. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/ideal-merchant-transaction | View for requesting iDEAL transactions and polling their status. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/ideal-merchant-transaction/{itemId} | View for requesting iDEAL transactions and polling their status. |
| GET | /user/{userID}/insight-preference-date | Used to allow users to set insight/budget preferences. |
| GET | /user/{userID}/insights | Used to get insights about transactions between given time range. |
| GET | /user/{userID}/insights-search | Used to get events based on time and insight category. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/payment-auto-allocate/{payment-auto-allocateID}/instance | List all the times a users payment was automatically allocated. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/payment-auto-allocate/{payment-auto-allocateID}/instance/{itemId} | List all the times a users payment was automatically allocated. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/invoice | Used to view a bunq invoice. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/invoice/{itemId} | Used to view a bunq invoice. |
| GET | /user/{userID}/invoice | Used to list bunq invoices by user. |
| GET | /user/{userID}/invoice/{itemId} | Used to list bunq invoices by user. |
| GET | /user/{userID}/invoice/{invoiceID}/invoice-export/{itemId} | Get a PDF export of an invoice. |
| PUT | /user/{userID}/invoice/{invoiceID}/invoice-export/{itemId} | Get a PDF export of an invoice. |
| DELETE | /user/{userID}/invoice/{invoiceID}/invoice-export/{itemId} | Get a PDF export of an invoice. |
| POST | /user/{userID}/invoice/{invoiceID}/invoice-export | Get a PDF export of an invoice. |
| GET | /user/{userID}/credential-password-ip/{credential-password-ipID}/ip/{itemId} | Manage the IPs which may be used for a credential of a user for server authentication. |
| PUT | /user/{userID}/credential-password-ip/{credential-password-ipID}/ip/{itemId} | Manage the IPs which may be used for a credential of a user for server authentication. |
| POST | /user/{userID}/credential-password-ip/{credential-password-ipID}/ip | Manage the IPs which may be used for a credential of a user for server authentication. |
| GET | /user/{userID}/credential-password-ip/{credential-password-ipID}/ip | Manage the IPs which may be used for a credential of a user for server authentication. |
| GET | /user/{userID}/legal-name | Endpoint for getting available legal names that can be used by the user. |
| GET | /user/{userID}/limit | Get all limits for the authenticated user. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/mastercard-action/{itemId} | MasterCard transaction view. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/mastercard-action | MasterCard transaction view. |
| GET | /user/{userID}/monetary-account/{itemId} | Get a specific MonetaryAccount. |
| GET | /user/{userID}/monetary-account | Get a collection of all your MonetaryAccounts. |
| POST | /user/{userID}/monetary-account-bank | Create new MonetaryAccountBank. |
| GET | /user/{userID}/monetary-account-bank | Gets a listing of all MonetaryAccountBanks of a given user. |
| GET | /user/{userID}/monetary-account-bank/{itemId} | Get a specific MonetaryAccountBank. |
| PUT | /user/{userID}/monetary-account-bank/{itemId} | Update a specific existing MonetaryAccountBank. |
| GET | /user/{userID}/monetary-account-card/{itemId} | Get a specific MonetaryAccountCard. |
| PUT | /user/{userID}/monetary-account-card/{itemId} | Update a specific existing MonetaryAccountCard. |
| GET | /user/{userID}/monetary-account-card | Gets a listing of all MonetaryAccountCard of a given user. |
| POST | /user/{userID}/monetary-account-external | Endpoint for managing monetary accounts which are connected to external services. |
| GET | /user/{userID}/monetary-account-external | Endpoint for managing monetary accounts which are connected to external services. |
| GET | /user/{userID}/monetary-account-external/{itemId} | Endpoint for managing monetary accounts which are connected to external services. |
| PUT | /user/{userID}/monetary-account-external/{itemId} | Endpoint for managing monetary accounts which are connected to external services. |
| POST | /user/{userID}/monetary-account-external-savings | Endpoint for managing monetary account savings which are connected to external services. |
| GET | /user/{userID}/monetary-account-external-savings | Endpoint for managing monetary account savings which are connected to external services. |
| GET | /user/{userID}/monetary-account-external-savings/{itemId} | Endpoint for managing monetary account savings which are connected to external services. |
| PUT | /user/{userID}/monetary-account-external-savings/{itemId} | Endpoint for managing monetary account savings which are connected to external services. |
| POST | /user/{userID}/monetary-account-joint | The endpoint for joint monetary accounts. |
| GET | /user/{userID}/monetary-account-joint | The endpoint for joint monetary accounts. |
| GET | /user/{userID}/monetary-account-joint/{itemId} | The endpoint for joint monetary accounts. |
| PUT | /user/{userID}/monetary-account-joint/{itemId} | The endpoint for joint monetary accounts. |
| POST | /user/{userID}/monetary-account-savings | Create new MonetaryAccountSavings. |
| GET | /user/{userID}/monetary-account-savings | Gets a listing of all MonetaryAccountSavingss of a given user. |
| GET | /user/{userID}/monetary-account-savings/{itemId} | Get a specific MonetaryAccountSavings. |
| PUT | /user/{userID}/monetary-account-savings/{itemId} | Update a specific existing MonetaryAccountSavings. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/adyen-card-transaction/{adyen-card-transactionID}/note-attachment | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/adyen-card-transaction/{adyen-card-transactionID}/note-attachment | Used to manage attachment notes. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/adyen-card-transaction/{adyen-card-transactionID}/note-attachment/{itemId} | Used to manage attachment notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/adyen-card-transaction/{adyen-card-transactionID}/note-attachment/{itemId} | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/adyen-card-transaction/{adyen-card-transactionID}/note-attachment/{itemId} | Used to manage attachment notes. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/switch-service-payment/{switch-service-paymentID}/note-attachment | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/switch-service-payment/{switch-service-paymentID}/note-attachment | Manage the notes for a given user. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/switch-service-payment/{switch-service-paymentID}/note-attachment/{itemId} | Used to manage attachment notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/switch-service-payment/{switch-service-paymentID}/note-attachment/{itemId} | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/switch-service-payment/{switch-service-paymentID}/note-attachment/{itemId} | Used to manage attachment notes. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/bunqme-fundraiser-result/{bunqme-fundraiser-resultID}/note-attachment | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/bunqme-fundraiser-result/{bunqme-fundraiser-resultID}/note-attachment | Manage the notes for a given user. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/bunqme-fundraiser-result/{bunqme-fundraiser-resultID}/note-attachment/{itemId} | Used to manage attachment notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/bunqme-fundraiser-result/{bunqme-fundraiser-resultID}/note-attachment/{itemId} | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/bunqme-fundraiser-result/{bunqme-fundraiser-resultID}/note-attachment/{itemId} | Used to manage attachment notes. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/draft-payment/{draft-paymentID}/note-attachment | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/draft-payment/{draft-paymentID}/note-attachment | Manage the notes for a given user. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/draft-payment/{draft-paymentID}/note-attachment/{itemId} | Used to manage attachment notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/draft-payment/{draft-paymentID}/note-attachment/{itemId} | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/draft-payment/{draft-paymentID}/note-attachment/{itemId} | Used to manage attachment notes. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/ideal-merchant-transaction/{ideal-merchant-transactionID}/note-attachment | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/ideal-merchant-transaction/{ideal-merchant-transactionID}/note-attachment | Manage the notes for a given user. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/ideal-merchant-transaction/{ideal-merchant-transactionID}/note-attachment/{itemId} | Used to manage attachment notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/ideal-merchant-transaction/{ideal-merchant-transactionID}/note-attachment/{itemId} | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/ideal-merchant-transaction/{ideal-merchant-transactionID}/note-attachment/{itemId} | Used to manage attachment notes. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/mastercard-action/{mastercard-actionID}/note-attachment | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/mastercard-action/{mastercard-actionID}/note-attachment | Manage the notes for a given user. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/mastercard-action/{mastercard-actionID}/note-attachment/{itemId} | Used to manage attachment notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/mastercard-action/{mastercard-actionID}/note-attachment/{itemId} | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/mastercard-action/{mastercard-actionID}/note-attachment/{itemId} | Used to manage attachment notes. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/open-banking-merchant-transaction/{open-banking-merchant-transactionID}/note-attachment | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/open-banking-merchant-transaction/{open-banking-merchant-transactionID}/note-attachment | Used to manage attachment notes. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/open-banking-merchant-transaction/{open-banking-merchant-transactionID}/note-attachment/{itemId} | Used to manage attachment notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/open-banking-merchant-transaction/{open-banking-merchant-transactionID}/note-attachment/{itemId} | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/open-banking-merchant-transaction/{open-banking-merchant-transactionID}/note-attachment/{itemId} | Used to manage attachment notes. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/payment-batch/{payment-batchID}/note-attachment | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/payment-batch/{payment-batchID}/note-attachment | Manage the notes for a given user. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/payment-batch/{payment-batchID}/note-attachment/{itemId} | Used to manage attachment notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/payment-batch/{payment-batchID}/note-attachment/{itemId} | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/payment-batch/{payment-batchID}/note-attachment/{itemId} | Used to manage attachment notes. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/payment-delayed/{payment-delayedID}/note-attachment | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/payment-delayed/{payment-delayedID}/note-attachment | Used to manage attachment notes. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/payment-delayed/{payment-delayedID}/note-attachment/{itemId} | Used to manage attachment notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/payment-delayed/{payment-delayedID}/note-attachment/{itemId} | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/payment-delayed/{payment-delayedID}/note-attachment/{itemId} | Used to manage attachment notes. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/payment/{paymentID}/note-attachment | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/payment/{paymentID}/note-attachment | Manage the notes for a given user. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/payment/{paymentID}/note-attachment/{itemId} | Used to manage attachment notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/payment/{paymentID}/note-attachment/{itemId} | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/payment/{paymentID}/note-attachment/{itemId} | Used to manage attachment notes. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry-batch/{request-inquiry-batchID}/note-attachment | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry-batch/{request-inquiry-batchID}/note-attachment | Manage the notes for a given user. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry-batch/{request-inquiry-batchID}/note-attachment/{itemId} | Used to manage attachment notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry-batch/{request-inquiry-batchID}/note-attachment/{itemId} | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry-batch/{request-inquiry-batchID}/note-attachment/{itemId} | Used to manage attachment notes. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry/{request-inquiryID}/note-attachment | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry/{request-inquiryID}/note-attachment | Manage the notes for a given user. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry/{request-inquiryID}/note-attachment/{itemId} | Used to manage attachment notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry/{request-inquiryID}/note-attachment/{itemId} | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry/{request-inquiryID}/note-attachment/{itemId} | Used to manage attachment notes. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/request-response/{request-responseID}/note-attachment | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/request-response/{request-responseID}/note-attachment | Manage the notes for a given user. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/request-response/{request-responseID}/note-attachment/{itemId} | Used to manage attachment notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/request-response/{request-responseID}/note-attachment/{itemId} | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/request-response/{request-responseID}/note-attachment/{itemId} | Used to manage attachment notes. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/schedule/{scheduleID}/schedule-instance/{schedule-instanceID}/note-attachment | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/schedule/{scheduleID}/schedule-instance/{schedule-instanceID}/note-attachment | Manage the notes for a given user. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/schedule/{scheduleID}/schedule-instance/{schedule-instanceID}/note-attachment/{itemId} | Used to manage attachment notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/schedule/{scheduleID}/schedule-instance/{schedule-instanceID}/note-attachment/{itemId} | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/schedule/{scheduleID}/schedule-instance/{schedule-instanceID}/note-attachment/{itemId} | Used to manage attachment notes. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment-batch/{schedule-payment-batchID}/note-attachment | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment-batch/{schedule-payment-batchID}/note-attachment | Manage the notes for a given user. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment-batch/{schedule-payment-batchID}/note-attachment/{itemId} | Used to manage attachment notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment-batch/{schedule-payment-batchID}/note-attachment/{itemId} | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment-batch/{schedule-payment-batchID}/note-attachment/{itemId} | Used to manage attachment notes. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment/{schedule-paymentID}/note-attachment | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment/{schedule-paymentID}/note-attachment | Manage the notes for a given user. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment/{schedule-paymentID}/note-attachment/{itemId} | Used to manage attachment notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment/{schedule-paymentID}/note-attachment/{itemId} | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment/{schedule-paymentID}/note-attachment/{itemId} | Used to manage attachment notes. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry-batch/{schedule-request-inquiry-batchID}/note-attachment | Used to manage attachment notes for a scheduled request. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry-batch/{schedule-request-inquiry-batchID}/note-attachment | Manage the notes for a scheduled request. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry-batch/{schedule-request-inquiry-batchID}/note-attachment/{itemId} | Used to manage attachment notes for a scheduled request. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry-batch/{schedule-request-inquiry-batchID}/note-attachment/{itemId} | Used to manage attachment notes for a scheduled request. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry-batch/{schedule-request-inquiry-batchID}/note-attachment/{itemId} | Used to manage attachment notes for a scheduled request. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry/{schedule-request-inquiryID}/note-attachment | Used to manage attachment notes for a scheduled request. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry/{schedule-request-inquiryID}/note-attachment | Manage the notes for a scheduled request. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry/{schedule-request-inquiryID}/note-attachment/{itemId} | Used to manage attachment notes for a scheduled request. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry/{schedule-request-inquiryID}/note-attachment/{itemId} | Used to manage attachment notes for a scheduled request. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry/{schedule-request-inquiryID}/note-attachment/{itemId} | Used to manage attachment notes for a scheduled request. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/sofort-merchant-transaction/{sofort-merchant-transactionID}/note-attachment | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/sofort-merchant-transaction/{sofort-merchant-transactionID}/note-attachment | Manage the notes for a given user. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/sofort-merchant-transaction/{sofort-merchant-transactionID}/note-attachment/{itemId} | Used to manage attachment notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/sofort-merchant-transaction/{sofort-merchant-transactionID}/note-attachment/{itemId} | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/sofort-merchant-transaction/{sofort-merchant-transactionID}/note-attachment/{itemId} | Used to manage attachment notes. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/whitelist/{whitelistID}/whitelist-result/{whitelist-resultID}/note-attachment | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/whitelist/{whitelistID}/whitelist-result/{whitelist-resultID}/note-attachment | Manage the notes for a given user. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/whitelist/{whitelistID}/whitelist-result/{whitelist-resultID}/note-attachment/{itemId} | Used to manage attachment notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/whitelist/{whitelistID}/whitelist-result/{whitelist-resultID}/note-attachment/{itemId} | Used to manage attachment notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/whitelist/{whitelistID}/whitelist-result/{whitelist-resultID}/note-attachment/{itemId} | Used to manage attachment notes. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/adyen-card-transaction/{adyen-card-transactionID}/note-text | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/adyen-card-transaction/{adyen-card-transactionID}/note-text | Used to manage text notes. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/adyen-card-transaction/{adyen-card-transactionID}/note-text/{itemId} | Used to manage text notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/adyen-card-transaction/{adyen-card-transactionID}/note-text/{itemId} | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/adyen-card-transaction/{adyen-card-transactionID}/note-text/{itemId} | Used to manage text notes. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/switch-service-payment/{switch-service-paymentID}/note-text | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/switch-service-payment/{switch-service-paymentID}/note-text | Manage the notes for a given user. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/switch-service-payment/{switch-service-paymentID}/note-text/{itemId} | Used to manage text notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/switch-service-payment/{switch-service-paymentID}/note-text/{itemId} | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/switch-service-payment/{switch-service-paymentID}/note-text/{itemId} | Used to manage text notes. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/bunqme-fundraiser-result/{bunqme-fundraiser-resultID}/note-text | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/bunqme-fundraiser-result/{bunqme-fundraiser-resultID}/note-text | Manage the notes for a given user. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/bunqme-fundraiser-result/{bunqme-fundraiser-resultID}/note-text/{itemId} | Used to manage text notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/bunqme-fundraiser-result/{bunqme-fundraiser-resultID}/note-text/{itemId} | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/bunqme-fundraiser-result/{bunqme-fundraiser-resultID}/note-text/{itemId} | Used to manage text notes. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/draft-payment/{draft-paymentID}/note-text | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/draft-payment/{draft-paymentID}/note-text | Manage the notes for a given user. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/draft-payment/{draft-paymentID}/note-text/{itemId} | Used to manage text notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/draft-payment/{draft-paymentID}/note-text/{itemId} | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/draft-payment/{draft-paymentID}/note-text/{itemId} | Used to manage text notes. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/ideal-merchant-transaction/{ideal-merchant-transactionID}/note-text | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/ideal-merchant-transaction/{ideal-merchant-transactionID}/note-text | Manage the notes for a given user. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/ideal-merchant-transaction/{ideal-merchant-transactionID}/note-text/{itemId} | Used to manage text notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/ideal-merchant-transaction/{ideal-merchant-transactionID}/note-text/{itemId} | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/ideal-merchant-transaction/{ideal-merchant-transactionID}/note-text/{itemId} | Used to manage text notes. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/mastercard-action/{mastercard-actionID}/note-text | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/mastercard-action/{mastercard-actionID}/note-text | Manage the notes for a given user. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/mastercard-action/{mastercard-actionID}/note-text/{itemId} | Used to manage text notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/mastercard-action/{mastercard-actionID}/note-text/{itemId} | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/mastercard-action/{mastercard-actionID}/note-text/{itemId} | Used to manage text notes. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/open-banking-merchant-transaction/{open-banking-merchant-transactionID}/note-text | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/open-banking-merchant-transaction/{open-banking-merchant-transactionID}/note-text | Used to manage text notes. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/open-banking-merchant-transaction/{open-banking-merchant-transactionID}/note-text/{itemId} | Used to manage text notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/open-banking-merchant-transaction/{open-banking-merchant-transactionID}/note-text/{itemId} | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/open-banking-merchant-transaction/{open-banking-merchant-transactionID}/note-text/{itemId} | Used to manage text notes. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/payment-batch/{payment-batchID}/note-text | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/payment-batch/{payment-batchID}/note-text | Manage the notes for a given user. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/payment-batch/{payment-batchID}/note-text/{itemId} | Used to manage text notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/payment-batch/{payment-batchID}/note-text/{itemId} | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/payment-batch/{payment-batchID}/note-text/{itemId} | Used to manage text notes. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/payment-delayed/{payment-delayedID}/note-text | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/payment-delayed/{payment-delayedID}/note-text | Used to manage text notes. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/payment-delayed/{payment-delayedID}/note-text/{itemId} | Used to manage text notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/payment-delayed/{payment-delayedID}/note-text/{itemId} | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/payment-delayed/{payment-delayedID}/note-text/{itemId} | Used to manage text notes. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/payment/{paymentID}/note-text | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/payment/{paymentID}/note-text | Manage the notes for a given user. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/payment/{paymentID}/note-text/{itemId} | Used to manage text notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/payment/{paymentID}/note-text/{itemId} | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/payment/{paymentID}/note-text/{itemId} | Used to manage text notes. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry-batch/{request-inquiry-batchID}/note-text | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry-batch/{request-inquiry-batchID}/note-text | Manage the notes for a given user. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry-batch/{request-inquiry-batchID}/note-text/{itemId} | Used to manage text notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry-batch/{request-inquiry-batchID}/note-text/{itemId} | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry-batch/{request-inquiry-batchID}/note-text/{itemId} | Used to manage text notes. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry/{request-inquiryID}/note-text | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry/{request-inquiryID}/note-text | Manage the notes for a given user. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry/{request-inquiryID}/note-text/{itemId} | Used to manage text notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry/{request-inquiryID}/note-text/{itemId} | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry/{request-inquiryID}/note-text/{itemId} | Used to manage text notes. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/request-response/{request-responseID}/note-text | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/request-response/{request-responseID}/note-text | Manage the notes for a given user. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/request-response/{request-responseID}/note-text/{itemId} | Used to manage text notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/request-response/{request-responseID}/note-text/{itemId} | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/request-response/{request-responseID}/note-text/{itemId} | Used to manage text notes. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/schedule/{scheduleID}/schedule-instance/{schedule-instanceID}/note-text | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/schedule/{scheduleID}/schedule-instance/{schedule-instanceID}/note-text | Manage the notes for a given user. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/schedule/{scheduleID}/schedule-instance/{schedule-instanceID}/note-text/{itemId} | Used to manage text notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/schedule/{scheduleID}/schedule-instance/{schedule-instanceID}/note-text/{itemId} | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/schedule/{scheduleID}/schedule-instance/{schedule-instanceID}/note-text/{itemId} | Used to manage text notes. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment-batch/{schedule-payment-batchID}/note-text | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment-batch/{schedule-payment-batchID}/note-text | Manage the notes for a given user. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment-batch/{schedule-payment-batchID}/note-text/{itemId} | Used to manage text notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment-batch/{schedule-payment-batchID}/note-text/{itemId} | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment-batch/{schedule-payment-batchID}/note-text/{itemId} | Used to manage text notes. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment/{schedule-paymentID}/note-text | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment/{schedule-paymentID}/note-text | Manage the notes for a given user. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment/{schedule-paymentID}/note-text/{itemId} | Used to manage text notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment/{schedule-paymentID}/note-text/{itemId} | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment/{schedule-paymentID}/note-text/{itemId} | Used to manage text notes. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry-batch/{schedule-request-inquiry-batchID}/note-text | Used to manage text notes for a scheduled request. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry-batch/{schedule-request-inquiry-batchID}/note-text | Manage the notes for a given schedule request. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry-batch/{schedule-request-inquiry-batchID}/note-text/{itemId} | Used to manage text notes for a scheduled request. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry-batch/{schedule-request-inquiry-batchID}/note-text/{itemId} | Used to manage text notes for a scheduled request. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry-batch/{schedule-request-inquiry-batchID}/note-text/{itemId} | Used to manage text notes for a scheduled request. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry/{schedule-request-inquiryID}/note-text | Used to manage text notes for a scheduled request. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry/{schedule-request-inquiryID}/note-text | Manage the notes for a given schedule request. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry/{schedule-request-inquiryID}/note-text/{itemId} | Used to manage text notes for a scheduled request. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry/{schedule-request-inquiryID}/note-text/{itemId} | Used to manage text notes for a scheduled request. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry/{schedule-request-inquiryID}/note-text/{itemId} | Used to manage text notes for a scheduled request. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/sofort-merchant-transaction/{sofort-merchant-transactionID}/note-text | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/sofort-merchant-transaction/{sofort-merchant-transactionID}/note-text | Manage the notes for a given user. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/sofort-merchant-transaction/{sofort-merchant-transactionID}/note-text/{itemId} | Used to manage text notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/sofort-merchant-transaction/{sofort-merchant-transactionID}/note-text/{itemId} | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/sofort-merchant-transaction/{sofort-merchant-transactionID}/note-text/{itemId} | Used to manage text notes. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/whitelist/{whitelistID}/whitelist-result/{whitelist-resultID}/note-text | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/whitelist/{whitelistID}/whitelist-result/{whitelist-resultID}/note-text | Manage the notes for a given user. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/whitelist/{whitelistID}/whitelist-result/{whitelist-resultID}/note-text/{itemId} | Used to manage text notes. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/whitelist/{whitelistID}/whitelist-result/{whitelist-resultID}/note-text/{itemId} | Used to manage text notes. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/whitelist/{whitelistID}/whitelist-result/{whitelist-resultID}/note-text/{itemId} | Used to manage text notes. |
| POST | /user/{userID}/notification-filter-email | Manage the email notification filters for a user. |
| GET | /user/{userID}/notification-filter-email | Manage the email notification filters for a user. |
| POST | /user/{userID}/notification-filter-failure | Manage the url notification filters for a user. |
| GET | /user/{userID}/notification-filter-failure | Manage the url notification filters for a user. |
| POST | /user/{userID}/notification-filter-push | Manage the push notification filters for a user. |
| GET | /user/{userID}/notification-filter-push | Manage the push notification filters for a user. |
| POST | /user/{userID}/notification-filter-url | Manage the url notification filters for a user. |
| GET | /user/{userID}/notification-filter-url | Manage the url notification filters for a user. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/notification-filter-url | Manage the url notification filters for a user. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/notification-filter-url | Manage the url notification filters for a user. |
| GET | /user/{userID}/oauth-client/{itemId} | Used for managing OAuth Clients. |
| PUT | /user/{userID}/oauth-client/{itemId} | Used for managing OAuth Clients. |
| POST | /user/{userID}/oauth-client | Used for managing OAuth Clients. |
| GET | /user/{userID}/oauth-client | Used for managing OAuth Clients. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/payment | Create a new Payment. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/payment | Get a listing of all Payments performed on a given MonetaryAccount (incoming and outgoing). |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/payment/{itemId} | Get a specific previous Payment. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/mastercard-action/{mastercard-actionID}/payment | MasterCard transaction view. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/payment-auto-allocate | Manage a users automatic payment auto allocated settings. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/payment-auto-allocate | Manage a users automatic payment auto allocated settings. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/payment-auto-allocate/{itemId} | Manage a users automatic payment auto allocated settings. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/payment-auto-allocate/{itemId} | Manage a users automatic payment auto allocated settings. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/payment-auto-allocate/{itemId} | Manage a users automatic payment auto allocated settings. |
| GET | /user/{userID}/payment-auto-allocate | List a users automatic payment auto allocated settings. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/payment-batch | Create a payment batch by sending an array of single payment objects, that will become part of the batch. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/payment-batch | Return all the payment batches for a monetary account. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/payment-batch/{itemId} | Revoke a bunq.to payment batch. The status of all the payments will be set to REVOKED. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/payment-batch/{itemId} | Return the details of a specific payment batch. |
| POST | /user/{userID}/payment-service-provider-draft-payment | Manage the PaymentServiceProviderDraftPayment's for a PISP. |
| GET | /user/{userID}/payment-service-provider-draft-payment | Manage the PaymentServiceProviderDraftPayment's for a PISP. |
| PUT | /user/{userID}/payment-service-provider-draft-payment/{itemId} | Manage the PaymentServiceProviderDraftPayment's for a PISP. |
| GET | /user/{userID}/payment-service-provider-draft-payment/{itemId} | Manage the PaymentServiceProviderDraftPayment's for a PISP. |
| POST | /user/{userID}/payment-service-provider-issuer-transaction | The endpoint for payment service provider issuer transactions |
| GET | /user/{userID}/payment-service-provider-issuer-transaction | The endpoint for payment service provider issuer transactions |
| GET | /user/{userID}/payment-service-provider-issuer-transaction/{itemId} | The endpoint for payment service provider issuer transactions |
| PUT | /user/{userID}/payment-service-provider-issuer-transaction/{itemId} | The endpoint for payment service provider issuer transactions |
| GET | /user/{userID}/invoice/{invoiceID}/pdf-content | Get a PDF export of an invoice. |
| POST | /user/{userID}/card/{cardID}/replace | Request a card replacement. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry | Create a new payment request. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry | Get all payment requests for a user's monetary account. bunqme_share_url is always null if the counterparty is a bunq user. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry/{itemId} | Revoke a request for payment, by updating the status to REVOKED. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry/{itemId} | Get the details of a specific payment request, including its status. bunqme_share_url is always null if the counterparty is a bunq user. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry-batch | Create a request batch by sending an array of single request objects, that will become part of the batch. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry-batch | Return all the request batches for a monetary account. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry-batch/{itemId} | Revoke a request batch. The status of all the requests will be set to REVOKED. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry-batch/{itemId} | Return the details of a specific request batch. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/request-response/{itemId} | Update the status to accept or reject the RequestResponse. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/request-response/{itemId} | Get the details for a specific existing RequestResponse. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/request-response | Get all RequestResponses for a MonetaryAccount. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/schedule/{itemId} | Get a specific schedule definition for a given monetary account. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/schedule | Get a collection of scheduled definition for a given monetary account. You can add the parameter type to filter the response. When type={SCHEDULE_DEFINITION_PAYMENT,SCHEDULE_DEFINITION_PAYMENT_BATCH} is provided only schedule definition object that relate to these definitions are returned. |
| GET | /user/{userID}/schedule | Get a collection of scheduled definition for all accessible monetary accounts of the user. You can add the parameter type to filter the response. When type={SCHEDULE_DEFINITION_PAYMENT,SCHEDULE_DEFINITION_PAYMENT_BATCH} is provided only schedule definition object that relate to these definitions are returned. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/schedule/{scheduleID}/schedule-instance/{itemId} | view for reading, updating and listing the scheduled instance. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/schedule/{scheduleID}/schedule-instance/{itemId} | view for reading, updating and listing the scheduled instance. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/schedule/{scheduleID}/schedule-instance | view for reading, updating and listing the scheduled instance. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment | Endpoint for schedule payments. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment | Endpoint for schedule payments. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment/{itemId} | Endpoint for schedule payments. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment/{itemId} | Endpoint for schedule payments. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment/{itemId} | Endpoint for schedule payments. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment-batch/{itemId} | Endpoint for schedule payment batches. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment-batch/{itemId} | Endpoint for schedule payment batches. |
| DELETE | /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment-batch/{itemId} | Endpoint for schedule payment batches. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment-batch | Endpoint for schedule payment batches. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/share-invite-monetary-account-inquiry | [DEPRECATED - use /share-invite-monetary-account-response] Create a new share inquiry for a monetary account, specifying the permission the other bunq user will have on it. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/share-invite-monetary-account-inquiry | [DEPRECATED - use /share-invite-monetary-account-response] Get a list with all the share inquiries for a monetary account, only if the requesting user has permission to change the details of the various ones. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/share-invite-monetary-account-inquiry/{itemId} | [DEPRECATED - use /share-invite-monetary-account-response] Get the details of a specific share inquiry. |
| PUT | /user/{userID}/monetary-account/{monetary-accountID}/share-invite-monetary-account-inquiry/{itemId} | [DEPRECATED - use /share-invite-monetary-account-response] Update the details of a share. This includes updating status (revoking or cancelling it), granted permission and validity period of this share. |
| GET | /user/{userID}/share-invite-monetary-account-response/{itemId} | Return the details of a specific share a user was invited to. |
| PUT | /user/{userID}/share-invite-monetary-account-response/{itemId} | Accept or reject a share a user was invited to. |
| GET | /user/{userID}/share-invite-monetary-account-response | Return all the shares a user was invited to. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/sofort-merchant-transaction/{itemId} | View for requesting Sofort transactions and polling their status. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/sofort-merchant-transaction | View for requesting Sofort transactions and polling their status. |
| POST | /user/{userID}/monetary-account/{monetary-accountID}/event/{eventID}/statement | Used to create a statement export of a single payment. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/event/{eventID}/statement/{itemId} | Used to create a statement export of a single payment. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/switch-service-payment/{itemId} | An incoming payment made towards an account of an external bank and redirected to a bunq account via switch service. |
| POST | /user/{userID}/token-qr-request-ideal | Create a request from an ideal transaction. |
| POST | /user/{userID}/token-qr-request-sofort | Create a request from an SOFORT transaction. |
| GET | /user/{userID}/transferwise-currency | Used to get a list of supported currencies for Transferwise. |
| POST | /user/{userID}/transferwise-quote | Used to get quotes from Transferwise. These can be used to initiate payments. |
| GET | /user/{userID}/transferwise-quote/{itemId} | Used to get quotes from Transferwise. These can be used to initiate payments. |
| POST | /user/{userID}/transferwise-quote-temporary | Used to get temporary quotes from Transferwise. These cannot be used to initiate payments |
| GET | /user/{userID}/transferwise-quote-temporary/{itemId} | Used to get temporary quotes from Transferwise. These cannot be used to initiate payments |
| POST | /user/{userID}/transferwise-quote/{transferwise-quoteID}/transferwise-recipient | Used to manage recipient accounts with Transferwise. |
| GET | /user/{userID}/transferwise-quote/{transferwise-quoteID}/transferwise-recipient | Used to manage recipient accounts with Transferwise. |
| GET | /user/{userID}/transferwise-quote/{transferwise-quoteID}/transferwise-recipient/{itemId} | Used to manage recipient accounts with Transferwise. |
| DELETE | /user/{userID}/transferwise-quote/{transferwise-quoteID}/transferwise-recipient/{itemId} | Used to manage recipient accounts with Transferwise. |
| POST | /user/{userID}/transferwise-quote/{transferwise-quoteID}/transferwise-recipient-requirement | Used to determine the recipient account requirements for Transferwise transfers. |
| GET | /user/{userID}/transferwise-quote/{transferwise-quoteID}/transferwise-recipient-requirement | Used to determine the recipient account requirements for Transferwise transfers. |
| POST | /user/{userID}/transferwise-quote/{transferwise-quoteID}/transferwise-transfer | Used to create Transferwise payments. |
| GET | /user/{userID}/transferwise-quote/{transferwise-quoteID}/transferwise-transfer | Used to create Transferwise payments. |
| GET | /user/{userID}/transferwise-quote/{transferwise-quoteID}/transferwise-transfer/{itemId} | Used to create Transferwise payments. |
| POST | /user/{userID}/transferwise-quote/{transferwise-quoteID}/transferwise-transfer-requirement | Used to determine the account requirements for Transferwise transfers. |
| POST | /user/{userID}/transferwise-user | Used to manage Transferwise users. |
| GET | /user/{userID}/transferwise-user | Used to manage Transferwise users. |
| GET | /user/{userID}/tree-progress | See how many trees this user has planted. |
| GET | /user/{itemId} | Get a specific user. |
| GET | /user | Get a collection of all available users. |
| GET | /user/{userID}/whitelist-sdd/{itemId} | Get a specific recurring SDD whitelist entry. |
| GET | /user/{userID}/whitelist-sdd | Get a listing of all recurring SDD whitelist entries for a target monetary account. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/whitelist-sdd/{itemId} | Get a specific SDD whitelist entry. |
| GET | /user/{userID}/monetary-account/{monetary-accountID}/whitelist-sdd | Get a listing of all SDD whitelist entries for a target monetary account. |
| GET | /user/{userID}/whitelist-sdd-one-off/{itemId} | Get a specific one off SDD whitelist entry. |
| PUT | /user/{userID}/whitelist-sdd-one-off/{itemId} | Whitelist an one off SDD so that when another one off SDD from the creditor comes in, it is automatically accepted. |
| DELETE | /user/{userID}/whitelist-sdd-one-off/{itemId} | Whitelist an one off SDD so that when another one off SDD from the creditor comes in, it is automatically accepted. |
| POST | /user/{userID}/whitelist-sdd-one-off | Create a new one off SDD whitelist entry. |
| GET | /user/{userID}/whitelist-sdd-one-off | Get a listing of all one off SDD whitelist entries for a target monetary account. |
| GET | /user/{userID}/whitelist-sdd-recurring/{itemId} | Get a specific recurring SDD whitelist entry. |
| PUT | /user/{userID}/whitelist-sdd-recurring/{itemId} | Whitelist a recurring SDD so that when another recurrence comes in, it is automatically accepted. |
| DELETE | /user/{userID}/whitelist-sdd-recurring/{itemId} | Whitelist a recurring SDD so that when another recurrence comes in, it is automatically accepted. |
| POST | /user/{userID}/whitelist-sdd-recurring | Create a new recurring SDD whitelist entry. |
| GET | /user/{userID}/whitelist-sdd-recurring | Get a listing of all recurring SDD whitelist entries for a target monetary account. |

### attachment-public
| Method | Path | Description |
|--------|------|-------------|
| POST | /attachment-public | Create a new public attachment. Create a POST request with a payload that contains a binary representation of the file, without any JSON wrapping. Make sure you define the MIME type (i.e. image/jpeg, or image/png) in the Content-Type header. You are required to provide a description of the attachment using the X-Bunq-Attachment-Description header. |
| GET | /attachment-public/{itemId} | Get a specific attachment's metadata through its UUID. The Content-Type header of the response will describe the MIME type of the attachment file. |
| GET | /attachment-public/{attachment-publicUUID}/content | Get the raw content of a specific attachment. |

### avatar
| Method | Path | Description |
|--------|------|-------------|
| POST | /avatar | Avatars are public images used to represent you or your company. Avatars are used to represent users, monetary accounts and cash registers. Avatars cannot be deleted, only replaced. Avatars can be updated after uploading the image you would like to use through AttachmentPublic. Using the attachment_public_uuid which is returned you can update your Avatar. Avatars used for cash registers and company accounts will be reviewed by bunq. |
| GET | /avatar/{itemId} | Avatars are public images used to represent you or your company. Avatars are used to represent users, monetary accounts and cash registers. Avatars cannot be deleted, only replaced. Avatars can be updated after uploading the image you would like to use through AttachmentPublic. Using the attachment_public_uuid which is returned you can update your Avatar. Avatars used for cash registers and company accounts will be reviewed by bunq. |

### device
| Method | Path | Description |
|--------|------|-------------|
| GET | /device/{itemId} | Get a single Device. A Device is either a DevicePhone or a DeviceServer. |
| GET | /device | Get a collection of Devices. A Device is either a DevicePhone or a DeviceServer. |

### device-server
| Method | Path | Description |
|--------|------|-------------|
| POST | /device-server | Create a new DeviceServer providing the installation token in the header and signing the request with the private part of the key you used to create the installation. The API Key that you are using will be bound to the IP address of the DeviceServer which you have created.<br/><br/>Using a Wildcard API Key gives you the freedom to make API calls even if the IP address has changed after the POST device-server.<br/><br/>Find out more at this link <a href="https:/bunq.com/en/apikey-dynamic-ip" target="_blank">https:/bunq.com/en/apikey-dynamic-ip</a>. |
| GET | /device-server | Get a collection of all the DeviceServers you have created. |
| GET | /device-server/{itemId} | Get one of your DeviceServers. |

### health-check
| Method | Path | Description |
|--------|------|-------------|
| GET | /health-check | Basic health check for uptime and instance health monitoring. |

### installation
| Method | Path | Description |
|--------|------|-------------|
| POST | /installation | This is the only API call that does not require you to use the "X-Bunq-Client-Authentication" and "X-Bunq-Client-Signature" headers. |
| GET | /installation | You must have an active session to make this call. This call returns the Id of the the Installation you are using in your session. |
| GET | /installation/{itemId} | You must have an active session to make this call. This call is used to check whether the Id you provide is the Id of your current installation or not. |
| GET | /installation/{installationID}/server-public-key | Show the ServerPublicKey for this Installation. |

### user-company
| Method | Path | Description |
|--------|------|-------------|
| GET | /user-company/{user-companyID}/name | Return all the known (trade) names for a specific user company. |
| GET | /user-company/{itemId} | Get a specific company. |
| PUT | /user-company/{itemId} | Modify a specific company's data. |

### payment-service-provider-credential
| Method | Path | Description |
|--------|------|-------------|
| GET | /payment-service-provider-credential/{itemId} | Register a Payment Service Provider and provide credentials |
| POST | /payment-service-provider-credential | Register a Payment Service Provider and provide credentials |

### sandbox-user-company
| Method | Path | Description |
|--------|------|-------------|
| POST | /sandbox-user-company | Used to create a sandbox userCompany. |

### sandbox-user-person
| Method | Path | Description |
|--------|------|-------------|
| POST | /sandbox-user-person | Used to create a sandbox userPerson. |

### server-error
| Method | Path | Description |
|--------|------|-------------|
| POST | /server-error | An endpoint that will always throw an error. |

### session
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /session/{itemId} | Deletes the current session. |

### session-server
| Method | Path | Description |
|--------|------|-------------|
| POST | /session-server | Create a new session for a DeviceServer. Provide the Installation token in the "X-Bunq-Client-Authentication" header. And don't forget to create the "X-Bunq-Client-Signature" header. The response contains a Session token that should be used for as the "X-Bunq-Client-Authentication" header for all future API calls. The ip address making this call needs to match the ip address bound to your API key. |

### user-payment-service-provider
| Method | Path | Description |
|--------|------|-------------|
| GET | /user-payment-service-provider/{itemId} | Used to view UserPaymentServiceProvider for session creation. |

### user-person
| Method | Path | Description |
|--------|------|-------------|
| GET | /user-person/{itemId} | Get a specific person. |
| PUT | /user-person/{itemId} | Modify a specific person object's data. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all additional-transaction-information-category?" -> GET /user/{userID}/additional-transaction-information-category
- "Create a additional-transaction-information-category-user-defined?" -> POST /user/{userID}/additional-transaction-information-category-user-defined
- "Create a attachment?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/attachment
- "Get attachment details?" -> GET /user/{userID}/attachment/{itemId}
- "Create a attachment-public?" -> POST /attachment-public
- "Get attachment-public details?" -> GET /attachment-public/{itemId}
- "Create a avatar?" -> POST /avatar
- "Get avatar details?" -> GET /avatar/{itemId}
- "List all billing-contract-subscription?" -> GET /user/{userID}/billing-contract-subscription
- "Get bunqme-fundraiser-profile details?" -> GET /user/{userID}/bunqme-fundraiser-profile/{itemId}
- "List all bunqme-fundraiser-profile?" -> GET /user/{userID}/bunqme-fundraiser-profile
- "Get bunqme-fundraiser-result details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/bunqme-fundraiser-result/{itemId}
- "Create a bunqme-tab?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/bunqme-tab
- "List all bunqme-tab?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/bunqme-tab
- "Update a bunqme-tab?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/bunqme-tab/{itemId}
- "Get bunqme-tab details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/bunqme-tab/{itemId}
- "Get bunqme-tab-result-response details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/bunqme-tab-result-response/{itemId}
- "Get callback-url details?" -> GET /user/{userID}/oauth-client/{oauth-clientID}/callback-url/{itemId}
- "Update a callback-url?" -> PUT /user/{userID}/oauth-client/{oauth-clientID}/callback-url/{itemId}
- "Delete a callback-url?" -> DELETE /user/{userID}/oauth-client/{oauth-clientID}/callback-url/{itemId}
- "Create a callback-url?" -> POST /user/{userID}/oauth-client/{oauth-clientID}/callback-url
- "List all callback-url?" -> GET /user/{userID}/oauth-client/{oauth-clientID}/callback-url
- "Update a card?" -> PUT /user/{userID}/card/{itemId}
- "Get card details?" -> GET /user/{userID}/card/{itemId}
- "List all card?" -> GET /user/{userID}/card
- "Create a card-batch?" -> POST /user/{userID}/card-batch
- "Create a card-batch-replace?" -> POST /user/{userID}/card-batch-replace
- "Create a card-credit?" -> POST /user/{userID}/card-credit
- "Create a card-debit?" -> POST /user/{userID}/card-debit
- "List all card-name?" -> GET /user/{userID}/card-name
- "Create a certificate-pinned?" -> POST /user/{userID}/certificate-pinned
- "List all certificate-pinned?" -> GET /user/{userID}/certificate-pinned
- "Delete a certificate-pinned?" -> DELETE /user/{userID}/certificate-pinned/{itemId}
- "Get certificate-pinned details?" -> GET /user/{userID}/certificate-pinned/{itemId}
- "Get challenge-request details?" -> GET /user/{userID}/challenge-request/{itemId}
- "Update a challenge-request?" -> PUT /user/{userID}/challenge-request/{itemId}
- "Create a company?" -> POST /user/{userID}/company
- "List all company?" -> GET /user/{userID}/company
- "Get company details?" -> GET /user/{userID}/company/{itemId}
- "Update a company?" -> PUT /user/{userID}/company/{itemId}
- "Create a confirmation-of-fund?" -> POST /user/{userID}/confirmation-of-funds
- "List all content?" -> GET /user/{userID}/chat-conversation/{chat-conversationID}/attachment/{attachmentID}/content
- "List all content?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/attachment/{attachmentID}/content
- "List all content?" -> GET /attachment-public/{attachment-publicUUID}/content
- "List all content?" -> GET /user/{userID}/attachment/{attachmentID}/content
- "List all content?" -> GET /user/{userID}/export-annual-overview/{export-annual-overviewID}/content
- "List all content?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/export-rib/{export-ribID}/content
- "List all content?" -> GET /user/{userID}/card/{cardID}/export-statement-card/{export-statement-cardID}/content
- "List all content?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/customer-statement/{customer-statementID}/content
- "List all content?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/event/{eventID}/statement/{statementID}/content
- "Get credential-password-ip details?" -> GET /user/{userID}/credential-password-ip/{itemId}
- "List all credential-password-ip?" -> GET /user/{userID}/credential-password-ip
- "Create a currency-cloud-beneficiary?" -> POST /user/{userID}/currency-cloud-beneficiary
- "List all currency-cloud-beneficiary?" -> GET /user/{userID}/currency-cloud-beneficiary
- "Get currency-cloud-beneficiary details?" -> GET /user/{userID}/currency-cloud-beneficiary/{itemId}
- "List all currency-cloud-beneficiary-requirement?" -> GET /user/{userID}/currency-cloud-beneficiary-requirement
- "Create a currency-cloud-payment-quote?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/currency-cloud-payment-quote
- "List all currency-conversion?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/currency-conversion
- "Get currency-conversion details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/currency-conversion/{itemId}
- "Create a currency-conversion-quote?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/currency-conversion-quote
- "Get currency-conversion-quote details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/currency-conversion-quote/{itemId}
- "Update a currency-conversion-quote?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/currency-conversion-quote/{itemId}
- "Create a customer-statement?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/customer-statement
- "List all customer-statement?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/customer-statement
- "Get customer-statement details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/customer-statement/{itemId}
- "Delete a customer-statement?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/customer-statement/{itemId}
- "List all definition?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/payment-auto-allocate/{payment-auto-allocateID}/definition
- "Get device details?" -> GET /device/{itemId}
- "List all device?" -> GET /device
- "Create a device-server?" -> POST /device-server
- "List all device-server?" -> GET /device-server
- "Get device-server details?" -> GET /device-server/{itemId}
- "Create a draft-payment?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/draft-payment
- "List all draft-payment?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/draft-payment
- "Update a draft-payment?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/draft-payment/{itemId}
- "Get draft-payment details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/draft-payment/{itemId}
- "Get event details?" -> GET /user/{userID}/event/{itemId}
- "List all event?" -> GET /user/{userID}/event
- "Create a export-annual-overview?" -> POST /user/{userID}/export-annual-overview
- "List all export-annual-overview?" -> GET /user/{userID}/export-annual-overview
- "Get export-annual-overview details?" -> GET /user/{userID}/export-annual-overview/{itemId}
- "Delete a export-annual-overview?" -> DELETE /user/{userID}/export-annual-overview/{itemId}
- "Create a export-rib?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/export-rib
- "List all export-rib?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/export-rib
- "Get export-rib details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/export-rib/{itemId}
- "Delete a export-rib?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/export-rib/{itemId}
- "Get export-statement-card details?" -> GET /user/{userID}/card/{cardID}/export-statement-card/{itemId}
- "List all export-statement-card?" -> GET /user/{userID}/card/{cardID}/export-statement-card
- "Create a export-statement-card-csv?" -> POST /user/{userID}/card/{cardID}/export-statement-card-csv
- "List all export-statement-card-csv?" -> GET /user/{userID}/card/{cardID}/export-statement-card-csv
- "Get export-statement-card-csv details?" -> GET /user/{userID}/card/{cardID}/export-statement-card-csv/{itemId}
- "Delete a export-statement-card-csv?" -> DELETE /user/{userID}/card/{cardID}/export-statement-card-csv/{itemId}
- "Create a export-statement-card-pdf?" -> POST /user/{userID}/card/{cardID}/export-statement-card-pdf
- "List all export-statement-card-pdf?" -> GET /user/{userID}/card/{cardID}/export-statement-card-pdf
- "Get export-statement-card-pdf details?" -> GET /user/{userID}/card/{cardID}/export-statement-card-pdf/{itemId}
- "Delete a export-statement-card-pdf?" -> DELETE /user/{userID}/card/{cardID}/export-statement-card-pdf/{itemId}
- "Get feature-announcement details?" -> GET /user/{userID}/feature-announcement/{itemId}
- "Create a generated-cvc2?" -> POST /user/{userID}/card/{cardID}/generated-cvc2
- "List all generated-cvc2?" -> GET /user/{userID}/card/{cardID}/generated-cvc2
- "Get generated-cvc2 details?" -> GET /user/{userID}/card/{cardID}/generated-cvc2/{itemId}
- "Update a generated-cvc2?" -> PUT /user/{userID}/card/{cardID}/generated-cvc2/{itemId}
- "List all health-check?" -> GET /health-check
- "Create a ideal-merchant-transaction?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/ideal-merchant-transaction
- "List all ideal-merchant-transaction?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/ideal-merchant-transaction
- "Get ideal-merchant-transaction details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/ideal-merchant-transaction/{itemId}
- "List all insight-preference-date?" -> GET /user/{userID}/insight-preference-date
- "List all insights?" -> GET /user/{userID}/insights
- "List all insights-search?" -> GET /user/{userID}/insights-search
- "Create a installation?" -> POST /installation
- "List all installation?" -> GET /installation
- "Get installation details?" -> GET /installation/{itemId}
- "List all instance?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/payment-auto-allocate/{payment-auto-allocateID}/instance
- "Get instance details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/payment-auto-allocate/{payment-auto-allocateID}/instance/{itemId}
- "List all invoice?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/invoice
- "Get invoice details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/invoice/{itemId}
- "List all invoice?" -> GET /user/{userID}/invoice
- "Get invoice details?" -> GET /user/{userID}/invoice/{itemId}
- "Get invoice-export details?" -> GET /user/{userID}/invoice/{invoiceID}/invoice-export/{itemId}
- "Update a invoice-export?" -> PUT /user/{userID}/invoice/{invoiceID}/invoice-export/{itemId}
- "Delete a invoice-export?" -> DELETE /user/{userID}/invoice/{invoiceID}/invoice-export/{itemId}
- "Create a invoice-export?" -> POST /user/{userID}/invoice/{invoiceID}/invoice-export
- "Get ip details?" -> GET /user/{userID}/credential-password-ip/{credential-password-ipID}/ip/{itemId}
- "Update a ip?" -> PUT /user/{userID}/credential-password-ip/{credential-password-ipID}/ip/{itemId}
- "Create a ip?" -> POST /user/{userID}/credential-password-ip/{credential-password-ipID}/ip
- "List all ip?" -> GET /user/{userID}/credential-password-ip/{credential-password-ipID}/ip
- "List all legal-name?" -> GET /user/{userID}/legal-name
- "List all limit?" -> GET /user/{userID}/limit
- "Get mastercard-action details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/mastercard-action/{itemId}
- "List all mastercard-action?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/mastercard-action
- "Get monetary-account details?" -> GET /user/{userID}/monetary-account/{itemId}
- "List all monetary-account?" -> GET /user/{userID}/monetary-account
- "Create a monetary-account-bank?" -> POST /user/{userID}/monetary-account-bank
- "List all monetary-account-bank?" -> GET /user/{userID}/monetary-account-bank
- "Get monetary-account-bank details?" -> GET /user/{userID}/monetary-account-bank/{itemId}
- "Update a monetary-account-bank?" -> PUT /user/{userID}/monetary-account-bank/{itemId}
- "Get monetary-account-card details?" -> GET /user/{userID}/monetary-account-card/{itemId}
- "Update a monetary-account-card?" -> PUT /user/{userID}/monetary-account-card/{itemId}
- "List all monetary-account-card?" -> GET /user/{userID}/monetary-account-card
- "Create a monetary-account-external?" -> POST /user/{userID}/monetary-account-external
- "List all monetary-account-external?" -> GET /user/{userID}/monetary-account-external
- "Get monetary-account-external details?" -> GET /user/{userID}/monetary-account-external/{itemId}
- "Update a monetary-account-external?" -> PUT /user/{userID}/monetary-account-external/{itemId}
- "Create a monetary-account-external-saving?" -> POST /user/{userID}/monetary-account-external-savings
- "List all monetary-account-external-savings?" -> GET /user/{userID}/monetary-account-external-savings
- "Get monetary-account-external-saving details?" -> GET /user/{userID}/monetary-account-external-savings/{itemId}
- "Update a monetary-account-external-saving?" -> PUT /user/{userID}/monetary-account-external-savings/{itemId}
- "Create a monetary-account-joint?" -> POST /user/{userID}/monetary-account-joint
- "List all monetary-account-joint?" -> GET /user/{userID}/monetary-account-joint
- "Get monetary-account-joint details?" -> GET /user/{userID}/monetary-account-joint/{itemId}
- "Update a monetary-account-joint?" -> PUT /user/{userID}/monetary-account-joint/{itemId}
- "Create a monetary-account-saving?" -> POST /user/{userID}/monetary-account-savings
- "List all monetary-account-savings?" -> GET /user/{userID}/monetary-account-savings
- "Get monetary-account-saving details?" -> GET /user/{userID}/monetary-account-savings/{itemId}
- "Update a monetary-account-saving?" -> PUT /user/{userID}/monetary-account-savings/{itemId}
- "List all name?" -> GET /user-company/{user-companyID}/name
- "Create a note-attachment?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/adyen-card-transaction/{adyen-card-transactionID}/note-attachment
- "List all note-attachment?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/adyen-card-transaction/{adyen-card-transactionID}/note-attachment
- "Update a note-attachment?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/adyen-card-transaction/{adyen-card-transactionID}/note-attachment/{itemId}
- "Delete a note-attachment?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/adyen-card-transaction/{adyen-card-transactionID}/note-attachment/{itemId}
- "Get note-attachment details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/adyen-card-transaction/{adyen-card-transactionID}/note-attachment/{itemId}
- "Create a note-attachment?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/switch-service-payment/{switch-service-paymentID}/note-attachment
- "List all note-attachment?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/switch-service-payment/{switch-service-paymentID}/note-attachment
- "Update a note-attachment?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/switch-service-payment/{switch-service-paymentID}/note-attachment/{itemId}
- "Delete a note-attachment?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/switch-service-payment/{switch-service-paymentID}/note-attachment/{itemId}
- "Get note-attachment details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/switch-service-payment/{switch-service-paymentID}/note-attachment/{itemId}
- "Create a note-attachment?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/bunqme-fundraiser-result/{bunqme-fundraiser-resultID}/note-attachment
- "List all note-attachment?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/bunqme-fundraiser-result/{bunqme-fundraiser-resultID}/note-attachment
- "Update a note-attachment?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/bunqme-fundraiser-result/{bunqme-fundraiser-resultID}/note-attachment/{itemId}
- "Delete a note-attachment?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/bunqme-fundraiser-result/{bunqme-fundraiser-resultID}/note-attachment/{itemId}
- "Get note-attachment details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/bunqme-fundraiser-result/{bunqme-fundraiser-resultID}/note-attachment/{itemId}
- "Create a note-attachment?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/draft-payment/{draft-paymentID}/note-attachment
- "List all note-attachment?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/draft-payment/{draft-paymentID}/note-attachment
- "Update a note-attachment?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/draft-payment/{draft-paymentID}/note-attachment/{itemId}
- "Delete a note-attachment?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/draft-payment/{draft-paymentID}/note-attachment/{itemId}
- "Get note-attachment details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/draft-payment/{draft-paymentID}/note-attachment/{itemId}
- "Create a note-attachment?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/ideal-merchant-transaction/{ideal-merchant-transactionID}/note-attachment
- "List all note-attachment?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/ideal-merchant-transaction/{ideal-merchant-transactionID}/note-attachment
- "Update a note-attachment?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/ideal-merchant-transaction/{ideal-merchant-transactionID}/note-attachment/{itemId}
- "Delete a note-attachment?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/ideal-merchant-transaction/{ideal-merchant-transactionID}/note-attachment/{itemId}
- "Get note-attachment details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/ideal-merchant-transaction/{ideal-merchant-transactionID}/note-attachment/{itemId}
- "Create a note-attachment?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/mastercard-action/{mastercard-actionID}/note-attachment
- "List all note-attachment?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/mastercard-action/{mastercard-actionID}/note-attachment
- "Update a note-attachment?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/mastercard-action/{mastercard-actionID}/note-attachment/{itemId}
- "Delete a note-attachment?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/mastercard-action/{mastercard-actionID}/note-attachment/{itemId}
- "Get note-attachment details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/mastercard-action/{mastercard-actionID}/note-attachment/{itemId}
- "Create a note-attachment?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/open-banking-merchant-transaction/{open-banking-merchant-transactionID}/note-attachment
- "List all note-attachment?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/open-banking-merchant-transaction/{open-banking-merchant-transactionID}/note-attachment
- "Update a note-attachment?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/open-banking-merchant-transaction/{open-banking-merchant-transactionID}/note-attachment/{itemId}
- "Delete a note-attachment?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/open-banking-merchant-transaction/{open-banking-merchant-transactionID}/note-attachment/{itemId}
- "Get note-attachment details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/open-banking-merchant-transaction/{open-banking-merchant-transactionID}/note-attachment/{itemId}
- "Create a note-attachment?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/payment-batch/{payment-batchID}/note-attachment
- "List all note-attachment?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/payment-batch/{payment-batchID}/note-attachment
- "Update a note-attachment?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/payment-batch/{payment-batchID}/note-attachment/{itemId}
- "Delete a note-attachment?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/payment-batch/{payment-batchID}/note-attachment/{itemId}
- "Get note-attachment details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/payment-batch/{payment-batchID}/note-attachment/{itemId}
- "Create a note-attachment?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/payment-delayed/{payment-delayedID}/note-attachment
- "List all note-attachment?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/payment-delayed/{payment-delayedID}/note-attachment
- "Update a note-attachment?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/payment-delayed/{payment-delayedID}/note-attachment/{itemId}
- "Delete a note-attachment?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/payment-delayed/{payment-delayedID}/note-attachment/{itemId}
- "Get note-attachment details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/payment-delayed/{payment-delayedID}/note-attachment/{itemId}
- "Create a note-attachment?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/payment/{paymentID}/note-attachment
- "List all note-attachment?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/payment/{paymentID}/note-attachment
- "Update a note-attachment?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/payment/{paymentID}/note-attachment/{itemId}
- "Delete a note-attachment?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/payment/{paymentID}/note-attachment/{itemId}
- "Get note-attachment details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/payment/{paymentID}/note-attachment/{itemId}
- "Create a note-attachment?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry-batch/{request-inquiry-batchID}/note-attachment
- "List all note-attachment?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry-batch/{request-inquiry-batchID}/note-attachment
- "Update a note-attachment?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry-batch/{request-inquiry-batchID}/note-attachment/{itemId}
- "Delete a note-attachment?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry-batch/{request-inquiry-batchID}/note-attachment/{itemId}
- "Get note-attachment details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry-batch/{request-inquiry-batchID}/note-attachment/{itemId}
- "Create a note-attachment?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry/{request-inquiryID}/note-attachment
- "List all note-attachment?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry/{request-inquiryID}/note-attachment
- "Update a note-attachment?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry/{request-inquiryID}/note-attachment/{itemId}
- "Delete a note-attachment?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry/{request-inquiryID}/note-attachment/{itemId}
- "Get note-attachment details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry/{request-inquiryID}/note-attachment/{itemId}
- "Create a note-attachment?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/request-response/{request-responseID}/note-attachment
- "List all note-attachment?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/request-response/{request-responseID}/note-attachment
- "Update a note-attachment?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/request-response/{request-responseID}/note-attachment/{itemId}
- "Delete a note-attachment?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/request-response/{request-responseID}/note-attachment/{itemId}
- "Get note-attachment details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/request-response/{request-responseID}/note-attachment/{itemId}
- "Create a note-attachment?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/schedule/{scheduleID}/schedule-instance/{schedule-instanceID}/note-attachment
- "List all note-attachment?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/schedule/{scheduleID}/schedule-instance/{schedule-instanceID}/note-attachment
- "Update a note-attachment?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/schedule/{scheduleID}/schedule-instance/{schedule-instanceID}/note-attachment/{itemId}
- "Delete a note-attachment?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/schedule/{scheduleID}/schedule-instance/{schedule-instanceID}/note-attachment/{itemId}
- "Get note-attachment details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/schedule/{scheduleID}/schedule-instance/{schedule-instanceID}/note-attachment/{itemId}
- "Create a note-attachment?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment-batch/{schedule-payment-batchID}/note-attachment
- "List all note-attachment?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment-batch/{schedule-payment-batchID}/note-attachment
- "Update a note-attachment?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment-batch/{schedule-payment-batchID}/note-attachment/{itemId}
- "Delete a note-attachment?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment-batch/{schedule-payment-batchID}/note-attachment/{itemId}
- "Get note-attachment details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment-batch/{schedule-payment-batchID}/note-attachment/{itemId}
- "Create a note-attachment?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment/{schedule-paymentID}/note-attachment
- "List all note-attachment?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment/{schedule-paymentID}/note-attachment
- "Update a note-attachment?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment/{schedule-paymentID}/note-attachment/{itemId}
- "Delete a note-attachment?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment/{schedule-paymentID}/note-attachment/{itemId}
- "Get note-attachment details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment/{schedule-paymentID}/note-attachment/{itemId}
- "Create a note-attachment?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry-batch/{schedule-request-inquiry-batchID}/note-attachment
- "List all note-attachment?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry-batch/{schedule-request-inquiry-batchID}/note-attachment
- "Update a note-attachment?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry-batch/{schedule-request-inquiry-batchID}/note-attachment/{itemId}
- "Delete a note-attachment?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry-batch/{schedule-request-inquiry-batchID}/note-attachment/{itemId}
- "Get note-attachment details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry-batch/{schedule-request-inquiry-batchID}/note-attachment/{itemId}
- "Create a note-attachment?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry/{schedule-request-inquiryID}/note-attachment
- "List all note-attachment?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry/{schedule-request-inquiryID}/note-attachment
- "Update a note-attachment?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry/{schedule-request-inquiryID}/note-attachment/{itemId}
- "Delete a note-attachment?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry/{schedule-request-inquiryID}/note-attachment/{itemId}
- "Get note-attachment details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry/{schedule-request-inquiryID}/note-attachment/{itemId}
- "Create a note-attachment?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/sofort-merchant-transaction/{sofort-merchant-transactionID}/note-attachment
- "List all note-attachment?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/sofort-merchant-transaction/{sofort-merchant-transactionID}/note-attachment
- "Update a note-attachment?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/sofort-merchant-transaction/{sofort-merchant-transactionID}/note-attachment/{itemId}
- "Delete a note-attachment?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/sofort-merchant-transaction/{sofort-merchant-transactionID}/note-attachment/{itemId}
- "Get note-attachment details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/sofort-merchant-transaction/{sofort-merchant-transactionID}/note-attachment/{itemId}
- "Create a note-attachment?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/whitelist/{whitelistID}/whitelist-result/{whitelist-resultID}/note-attachment
- "List all note-attachment?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/whitelist/{whitelistID}/whitelist-result/{whitelist-resultID}/note-attachment
- "Update a note-attachment?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/whitelist/{whitelistID}/whitelist-result/{whitelist-resultID}/note-attachment/{itemId}
- "Delete a note-attachment?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/whitelist/{whitelistID}/whitelist-result/{whitelist-resultID}/note-attachment/{itemId}
- "Get note-attachment details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/whitelist/{whitelistID}/whitelist-result/{whitelist-resultID}/note-attachment/{itemId}
- "Create a note-text?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/adyen-card-transaction/{adyen-card-transactionID}/note-text
- "List all note-text?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/adyen-card-transaction/{adyen-card-transactionID}/note-text
- "Update a note-text?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/adyen-card-transaction/{adyen-card-transactionID}/note-text/{itemId}
- "Delete a note-text?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/adyen-card-transaction/{adyen-card-transactionID}/note-text/{itemId}
- "Get note-text details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/adyen-card-transaction/{adyen-card-transactionID}/note-text/{itemId}
- "Create a note-text?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/switch-service-payment/{switch-service-paymentID}/note-text
- "List all note-text?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/switch-service-payment/{switch-service-paymentID}/note-text
- "Update a note-text?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/switch-service-payment/{switch-service-paymentID}/note-text/{itemId}
- "Delete a note-text?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/switch-service-payment/{switch-service-paymentID}/note-text/{itemId}
- "Get note-text details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/switch-service-payment/{switch-service-paymentID}/note-text/{itemId}
- "Create a note-text?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/bunqme-fundraiser-result/{bunqme-fundraiser-resultID}/note-text
- "List all note-text?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/bunqme-fundraiser-result/{bunqme-fundraiser-resultID}/note-text
- "Update a note-text?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/bunqme-fundraiser-result/{bunqme-fundraiser-resultID}/note-text/{itemId}
- "Delete a note-text?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/bunqme-fundraiser-result/{bunqme-fundraiser-resultID}/note-text/{itemId}
- "Get note-text details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/bunqme-fundraiser-result/{bunqme-fundraiser-resultID}/note-text/{itemId}
- "Create a note-text?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/draft-payment/{draft-paymentID}/note-text
- "List all note-text?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/draft-payment/{draft-paymentID}/note-text
- "Update a note-text?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/draft-payment/{draft-paymentID}/note-text/{itemId}
- "Delete a note-text?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/draft-payment/{draft-paymentID}/note-text/{itemId}
- "Get note-text details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/draft-payment/{draft-paymentID}/note-text/{itemId}
- "Create a note-text?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/ideal-merchant-transaction/{ideal-merchant-transactionID}/note-text
- "List all note-text?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/ideal-merchant-transaction/{ideal-merchant-transactionID}/note-text
- "Update a note-text?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/ideal-merchant-transaction/{ideal-merchant-transactionID}/note-text/{itemId}
- "Delete a note-text?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/ideal-merchant-transaction/{ideal-merchant-transactionID}/note-text/{itemId}
- "Get note-text details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/ideal-merchant-transaction/{ideal-merchant-transactionID}/note-text/{itemId}
- "Create a note-text?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/mastercard-action/{mastercard-actionID}/note-text
- "List all note-text?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/mastercard-action/{mastercard-actionID}/note-text
- "Update a note-text?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/mastercard-action/{mastercard-actionID}/note-text/{itemId}
- "Delete a note-text?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/mastercard-action/{mastercard-actionID}/note-text/{itemId}
- "Get note-text details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/mastercard-action/{mastercard-actionID}/note-text/{itemId}
- "Create a note-text?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/open-banking-merchant-transaction/{open-banking-merchant-transactionID}/note-text
- "List all note-text?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/open-banking-merchant-transaction/{open-banking-merchant-transactionID}/note-text
- "Update a note-text?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/open-banking-merchant-transaction/{open-banking-merchant-transactionID}/note-text/{itemId}
- "Delete a note-text?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/open-banking-merchant-transaction/{open-banking-merchant-transactionID}/note-text/{itemId}
- "Get note-text details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/open-banking-merchant-transaction/{open-banking-merchant-transactionID}/note-text/{itemId}
- "Create a note-text?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/payment-batch/{payment-batchID}/note-text
- "List all note-text?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/payment-batch/{payment-batchID}/note-text
- "Update a note-text?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/payment-batch/{payment-batchID}/note-text/{itemId}
- "Delete a note-text?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/payment-batch/{payment-batchID}/note-text/{itemId}
- "Get note-text details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/payment-batch/{payment-batchID}/note-text/{itemId}
- "Create a note-text?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/payment-delayed/{payment-delayedID}/note-text
- "List all note-text?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/payment-delayed/{payment-delayedID}/note-text
- "Update a note-text?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/payment-delayed/{payment-delayedID}/note-text/{itemId}
- "Delete a note-text?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/payment-delayed/{payment-delayedID}/note-text/{itemId}
- "Get note-text details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/payment-delayed/{payment-delayedID}/note-text/{itemId}
- "Create a note-text?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/payment/{paymentID}/note-text
- "List all note-text?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/payment/{paymentID}/note-text
- "Update a note-text?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/payment/{paymentID}/note-text/{itemId}
- "Delete a note-text?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/payment/{paymentID}/note-text/{itemId}
- "Get note-text details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/payment/{paymentID}/note-text/{itemId}
- "Create a note-text?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry-batch/{request-inquiry-batchID}/note-text
- "List all note-text?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry-batch/{request-inquiry-batchID}/note-text
- "Update a note-text?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry-batch/{request-inquiry-batchID}/note-text/{itemId}
- "Delete a note-text?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry-batch/{request-inquiry-batchID}/note-text/{itemId}
- "Get note-text details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry-batch/{request-inquiry-batchID}/note-text/{itemId}
- "Create a note-text?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry/{request-inquiryID}/note-text
- "List all note-text?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry/{request-inquiryID}/note-text
- "Update a note-text?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry/{request-inquiryID}/note-text/{itemId}
- "Delete a note-text?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry/{request-inquiryID}/note-text/{itemId}
- "Get note-text details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry/{request-inquiryID}/note-text/{itemId}
- "Create a note-text?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/request-response/{request-responseID}/note-text
- "List all note-text?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/request-response/{request-responseID}/note-text
- "Update a note-text?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/request-response/{request-responseID}/note-text/{itemId}
- "Delete a note-text?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/request-response/{request-responseID}/note-text/{itemId}
- "Get note-text details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/request-response/{request-responseID}/note-text/{itemId}
- "Create a note-text?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/schedule/{scheduleID}/schedule-instance/{schedule-instanceID}/note-text
- "List all note-text?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/schedule/{scheduleID}/schedule-instance/{schedule-instanceID}/note-text
- "Update a note-text?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/schedule/{scheduleID}/schedule-instance/{schedule-instanceID}/note-text/{itemId}
- "Delete a note-text?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/schedule/{scheduleID}/schedule-instance/{schedule-instanceID}/note-text/{itemId}
- "Get note-text details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/schedule/{scheduleID}/schedule-instance/{schedule-instanceID}/note-text/{itemId}
- "Create a note-text?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment-batch/{schedule-payment-batchID}/note-text
- "List all note-text?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment-batch/{schedule-payment-batchID}/note-text
- "Update a note-text?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment-batch/{schedule-payment-batchID}/note-text/{itemId}
- "Delete a note-text?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment-batch/{schedule-payment-batchID}/note-text/{itemId}
- "Get note-text details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment-batch/{schedule-payment-batchID}/note-text/{itemId}
- "Create a note-text?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment/{schedule-paymentID}/note-text
- "List all note-text?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment/{schedule-paymentID}/note-text
- "Update a note-text?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment/{schedule-paymentID}/note-text/{itemId}
- "Delete a note-text?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment/{schedule-paymentID}/note-text/{itemId}
- "Get note-text details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment/{schedule-paymentID}/note-text/{itemId}
- "Create a note-text?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry-batch/{schedule-request-inquiry-batchID}/note-text
- "List all note-text?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry-batch/{schedule-request-inquiry-batchID}/note-text
- "Update a note-text?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry-batch/{schedule-request-inquiry-batchID}/note-text/{itemId}
- "Delete a note-text?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry-batch/{schedule-request-inquiry-batchID}/note-text/{itemId}
- "Get note-text details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry-batch/{schedule-request-inquiry-batchID}/note-text/{itemId}
- "Create a note-text?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry/{schedule-request-inquiryID}/note-text
- "List all note-text?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry/{schedule-request-inquiryID}/note-text
- "Update a note-text?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry/{schedule-request-inquiryID}/note-text/{itemId}
- "Delete a note-text?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry/{schedule-request-inquiryID}/note-text/{itemId}
- "Get note-text details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/schedule-request-inquiry/{schedule-request-inquiryID}/note-text/{itemId}
- "Create a note-text?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/sofort-merchant-transaction/{sofort-merchant-transactionID}/note-text
- "List all note-text?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/sofort-merchant-transaction/{sofort-merchant-transactionID}/note-text
- "Update a note-text?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/sofort-merchant-transaction/{sofort-merchant-transactionID}/note-text/{itemId}
- "Delete a note-text?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/sofort-merchant-transaction/{sofort-merchant-transactionID}/note-text/{itemId}
- "Get note-text details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/sofort-merchant-transaction/{sofort-merchant-transactionID}/note-text/{itemId}
- "Create a note-text?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/whitelist/{whitelistID}/whitelist-result/{whitelist-resultID}/note-text
- "List all note-text?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/whitelist/{whitelistID}/whitelist-result/{whitelist-resultID}/note-text
- "Update a note-text?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/whitelist/{whitelistID}/whitelist-result/{whitelist-resultID}/note-text/{itemId}
- "Delete a note-text?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/whitelist/{whitelistID}/whitelist-result/{whitelist-resultID}/note-text/{itemId}
- "Get note-text details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/whitelist/{whitelistID}/whitelist-result/{whitelist-resultID}/note-text/{itemId}
- "Create a notification-filter-email?" -> POST /user/{userID}/notification-filter-email
- "List all notification-filter-email?" -> GET /user/{userID}/notification-filter-email
- "Create a notification-filter-failure?" -> POST /user/{userID}/notification-filter-failure
- "List all notification-filter-failure?" -> GET /user/{userID}/notification-filter-failure
- "Create a notification-filter-push?" -> POST /user/{userID}/notification-filter-push
- "List all notification-filter-push?" -> GET /user/{userID}/notification-filter-push
- "Create a notification-filter-url?" -> POST /user/{userID}/notification-filter-url
- "List all notification-filter-url?" -> GET /user/{userID}/notification-filter-url
- "Create a notification-filter-url?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/notification-filter-url
- "List all notification-filter-url?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/notification-filter-url
- "Get oauth-client details?" -> GET /user/{userID}/oauth-client/{itemId}
- "Update a oauth-client?" -> PUT /user/{userID}/oauth-client/{itemId}
- "Create a oauth-client?" -> POST /user/{userID}/oauth-client
- "List all oauth-client?" -> GET /user/{userID}/oauth-client
- "Create a payment?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/payment
- "List all payment?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/payment
- "Get payment details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/payment/{itemId}
- "List all payment?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/mastercard-action/{mastercard-actionID}/payment
- "Create a payment-auto-allocate?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/payment-auto-allocate
- "List all payment-auto-allocate?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/payment-auto-allocate
- "Get payment-auto-allocate details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/payment-auto-allocate/{itemId}
- "Update a payment-auto-allocate?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/payment-auto-allocate/{itemId}
- "Delete a payment-auto-allocate?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/payment-auto-allocate/{itemId}
- "List all payment-auto-allocate?" -> GET /user/{userID}/payment-auto-allocate
- "Create a payment-batch?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/payment-batch
- "List all payment-batch?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/payment-batch
- "Update a payment-batch?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/payment-batch/{itemId}
- "Get payment-batch details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/payment-batch/{itemId}
- "Get payment-service-provider-credential details?" -> GET /payment-service-provider-credential/{itemId}
- "Create a payment-service-provider-credential?" -> POST /payment-service-provider-credential
- "Create a payment-service-provider-draft-payment?" -> POST /user/{userID}/payment-service-provider-draft-payment
- "List all payment-service-provider-draft-payment?" -> GET /user/{userID}/payment-service-provider-draft-payment
- "Update a payment-service-provider-draft-payment?" -> PUT /user/{userID}/payment-service-provider-draft-payment/{itemId}
- "Get payment-service-provider-draft-payment details?" -> GET /user/{userID}/payment-service-provider-draft-payment/{itemId}
- "Create a payment-service-provider-issuer-transaction?" -> POST /user/{userID}/payment-service-provider-issuer-transaction
- "List all payment-service-provider-issuer-transaction?" -> GET /user/{userID}/payment-service-provider-issuer-transaction
- "Get payment-service-provider-issuer-transaction details?" -> GET /user/{userID}/payment-service-provider-issuer-transaction/{itemId}
- "Update a payment-service-provider-issuer-transaction?" -> PUT /user/{userID}/payment-service-provider-issuer-transaction/{itemId}
- "List all pdf-content?" -> GET /user/{userID}/invoice/{invoiceID}/pdf-content
- "Create a replace?" -> POST /user/{userID}/card/{cardID}/replace
- "Create a request-inquiry?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry
- "List all request-inquiry?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry
- "Update a request-inquiry?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry/{itemId}
- "Get request-inquiry details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry/{itemId}
- "Create a request-inquiry-batch?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry-batch
- "List all request-inquiry-batch?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry-batch
- "Update a request-inquiry-batch?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry-batch/{itemId}
- "Get request-inquiry-batch details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/request-inquiry-batch/{itemId}
- "Update a request-response?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/request-response/{itemId}
- "Get request-response details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/request-response/{itemId}
- "List all request-response?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/request-response
- "Create a sandbox-user-company?" -> POST /sandbox-user-company
- "Create a sandbox-user-person?" -> POST /sandbox-user-person
- "Get schedule details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/schedule/{itemId}
- "List all schedule?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/schedule
- "List all schedule?" -> GET /user/{userID}/schedule
- "Get schedule-instance details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/schedule/{scheduleID}/schedule-instance/{itemId}
- "Update a schedule-instance?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/schedule/{scheduleID}/schedule-instance/{itemId}
- "List all schedule-instance?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/schedule/{scheduleID}/schedule-instance
- "Create a schedule-payment?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment
- "List all schedule-payment?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment
- "Delete a schedule-payment?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment/{itemId}
- "Get schedule-payment details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment/{itemId}
- "Update a schedule-payment?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment/{itemId}
- "Get schedule-payment-batch details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment-batch/{itemId}
- "Update a schedule-payment-batch?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment-batch/{itemId}
- "Delete a schedule-payment-batch?" -> DELETE /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment-batch/{itemId}
- "Create a schedule-payment-batch?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/schedule-payment-batch
- "Create a server-error?" -> POST /server-error
- "List all server-public-key?" -> GET /installation/{installationID}/server-public-key
- "Delete a session?" -> DELETE /session/{itemId}
- "Create a session-server?" -> POST /session-server
- "Create a share-invite-monetary-account-inquiry?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/share-invite-monetary-account-inquiry
- "List all share-invite-monetary-account-inquiry?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/share-invite-monetary-account-inquiry
- "Get share-invite-monetary-account-inquiry details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/share-invite-monetary-account-inquiry/{itemId}
- "Update a share-invite-monetary-account-inquiry?" -> PUT /user/{userID}/monetary-account/{monetary-accountID}/share-invite-monetary-account-inquiry/{itemId}
- "Get share-invite-monetary-account-response details?" -> GET /user/{userID}/share-invite-monetary-account-response/{itemId}
- "Update a share-invite-monetary-account-response?" -> PUT /user/{userID}/share-invite-monetary-account-response/{itemId}
- "List all share-invite-monetary-account-response?" -> GET /user/{userID}/share-invite-monetary-account-response
- "Get sofort-merchant-transaction details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/sofort-merchant-transaction/{itemId}
- "List all sofort-merchant-transaction?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/sofort-merchant-transaction
- "Create a statement?" -> POST /user/{userID}/monetary-account/{monetary-accountID}/event/{eventID}/statement
- "Get statement details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/event/{eventID}/statement/{itemId}
- "Get switch-service-payment details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/switch-service-payment/{itemId}
- "Create a token-qr-request-ideal?" -> POST /user/{userID}/token-qr-request-ideal
- "Create a token-qr-request-sofort?" -> POST /user/{userID}/token-qr-request-sofort
- "List all transferwise-currency?" -> GET /user/{userID}/transferwise-currency
- "Create a transferwise-quote?" -> POST /user/{userID}/transferwise-quote
- "Get transferwise-quote details?" -> GET /user/{userID}/transferwise-quote/{itemId}
- "Create a transferwise-quote-temporary?" -> POST /user/{userID}/transferwise-quote-temporary
- "Get transferwise-quote-temporary details?" -> GET /user/{userID}/transferwise-quote-temporary/{itemId}
- "Create a transferwise-recipient?" -> POST /user/{userID}/transferwise-quote/{transferwise-quoteID}/transferwise-recipient
- "List all transferwise-recipient?" -> GET /user/{userID}/transferwise-quote/{transferwise-quoteID}/transferwise-recipient
- "Get transferwise-recipient details?" -> GET /user/{userID}/transferwise-quote/{transferwise-quoteID}/transferwise-recipient/{itemId}
- "Delete a transferwise-recipient?" -> DELETE /user/{userID}/transferwise-quote/{transferwise-quoteID}/transferwise-recipient/{itemId}
- "Create a transferwise-recipient-requirement?" -> POST /user/{userID}/transferwise-quote/{transferwise-quoteID}/transferwise-recipient-requirement
- "List all transferwise-recipient-requirement?" -> GET /user/{userID}/transferwise-quote/{transferwise-quoteID}/transferwise-recipient-requirement
- "Create a transferwise-transfer?" -> POST /user/{userID}/transferwise-quote/{transferwise-quoteID}/transferwise-transfer
- "List all transferwise-transfer?" -> GET /user/{userID}/transferwise-quote/{transferwise-quoteID}/transferwise-transfer
- "Get transferwise-transfer details?" -> GET /user/{userID}/transferwise-quote/{transferwise-quoteID}/transferwise-transfer/{itemId}
- "Create a transferwise-transfer-requirement?" -> POST /user/{userID}/transferwise-quote/{transferwise-quoteID}/transferwise-transfer-requirement
- "Create a transferwise-user?" -> POST /user/{userID}/transferwise-user
- "List all transferwise-user?" -> GET /user/{userID}/transferwise-user
- "List all tree-progress?" -> GET /user/{userID}/tree-progress
- "Get user details?" -> GET /user/{itemId}
- "List all user?" -> GET /user
- "Get user-company details?" -> GET /user-company/{itemId}
- "Update a user-company?" -> PUT /user-company/{itemId}
- "Get user-payment-service-provider details?" -> GET /user-payment-service-provider/{itemId}
- "Get user-person details?" -> GET /user-person/{itemId}
- "Update a user-person?" -> PUT /user-person/{itemId}
- "Get whitelist-sdd details?" -> GET /user/{userID}/whitelist-sdd/{itemId}
- "List all whitelist-sdd?" -> GET /user/{userID}/whitelist-sdd
- "Get whitelist-sdd details?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/whitelist-sdd/{itemId}
- "List all whitelist-sdd?" -> GET /user/{userID}/monetary-account/{monetary-accountID}/whitelist-sdd
- "Get whitelist-sdd-one-off details?" -> GET /user/{userID}/whitelist-sdd-one-off/{itemId}
- "Update a whitelist-sdd-one-off?" -> PUT /user/{userID}/whitelist-sdd-one-off/{itemId}
- "Delete a whitelist-sdd-one-off?" -> DELETE /user/{userID}/whitelist-sdd-one-off/{itemId}
- "Create a whitelist-sdd-one-off?" -> POST /user/{userID}/whitelist-sdd-one-off
- "List all whitelist-sdd-one-off?" -> GET /user/{userID}/whitelist-sdd-one-off
- "Get whitelist-sdd-recurring details?" -> GET /user/{userID}/whitelist-sdd-recurring/{itemId}
- "Update a whitelist-sdd-recurring?" -> PUT /user/{userID}/whitelist-sdd-recurring/{itemId}
- "Delete a whitelist-sdd-recurring?" -> DELETE /user/{userID}/whitelist-sdd-recurring/{itemId}
- "Create a whitelist-sdd-recurring?" -> POST /user/{userID}/whitelist-sdd-recurring
- "List all whitelist-sdd-recurring?" -> GET /user/{userID}/whitelist-sdd-recurring
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
