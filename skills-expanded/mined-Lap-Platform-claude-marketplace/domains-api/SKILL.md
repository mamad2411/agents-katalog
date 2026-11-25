---
name: domains-api
description: "Domains API skill. Use when working with Domains for domains, customers. Covers 65 endpoints."
version: 1.0.0
generator: lapsh
---

# Domains API

## Auth
No authentication required.

## Base URL
https://api.ote-godaddy.com

## Setup
1. No auth setup needed
2. GET /v1/domains -- verify access
3. POST /v1/domains/available -- create first available

## Endpoints

65 endpoints across 2 groups. See references/api-spec.lap for full details.

### domains
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/domains | Retrieve a list of Domains for the specified Shopper |
| GET | /v1/domains/agreements | Retrieve the legal agreement(s) required to purchase the specified TLD and add-ons |
| GET | /v1/domains/available | Determine whether or not the specified domain is available for purchase |
| POST | /v1/domains/available | Determine whether or not the specified domains are available for purchase |
| POST | /v1/domains/contacts/validate | Validate the request body using the Domain Contact Validation Schema for specified domains. |
| POST | /v1/domains/purchase | Purchase and register the specified Domain |
| GET | /v1/domains/purchase/schema/{tld} | Retrieve the schema to be submitted when registering a Domain for the specified TLD |
| POST | /v1/domains/purchase/validate | Validate the request body using the Domain Purchase Schema for the specified TLD |
| GET | /v1/domains/suggest | Suggest alternate Domain names based on a seed Domain, a set of keywords, or the shopper's purchase history |
| GET | /v1/domains/tlds | Retrieves a list of TLDs supported and enabled for sale |
| DELETE | /v1/domains/{domain} | Cancel a purchased domain |
| GET | /v1/domains/{domain} | Retrieve details for the specified Domain |
| PATCH | /v1/domains/{domain} | Update details for the specified Domain |
| PATCH | /v1/domains/{domain}/contacts | Update domain |
| DELETE | /v1/domains/{domain}/privacy | Submit a privacy cancellation request for the given domain |
| POST | /v1/domains/{domain}/privacy/purchase | Purchase privacy for a specified domain |
| PATCH | /v1/domains/{domain}/records | Add the specified DNS Records to the specified Domain |
| PUT | /v1/domains/{domain}/records | Replace all DNS Records for the specified Domain |
| GET | /v1/domains/{domain}/records/{type}/{name} | Retrieve DNS Records for the specified Domain, optionally with the specified Type and/or Name |
| PUT | /v1/domains/{domain}/records/{type}/{name} | Replace all DNS Records for the specified Domain with the specified Type and Name |
| DELETE | /v1/domains/{domain}/records/{type}/{name} | Delete all DNS Records for the specified Domain with the specified Type and Name |
| PUT | /v1/domains/{domain}/records/{type} | Replace all DNS Records for the specified Domain with the specified Type |
| POST | /v1/domains/{domain}/renew | Renew the specified Domain |
| POST | /v1/domains/{domain}/transfer | Purchase and start or restart transfer process |
| POST | /v1/domains/{domain}/verifyRegistrantEmail | Re-send Contact E-mail Verification for specified Domain |
| GET | /v2/domains/maintenances | Retrieve a list of upcoming system Maintenances |
| GET | /v2/domains/maintenances/{maintenanceId} | Retrieve the details for an upcoming system Maintenances |
| GET | /v2/domains/usage/{yyyymm} | Retrieve api usage request counts for a specific year/month.  The data is retained for a period of three months. |

### customers
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/customers/{customerId}/domains/{domain} | Retrieve details for the specified Domain |
| DELETE | /v2/customers/{customerId}/domains/{domain}/changeOfRegistrant | Cancels a pending change of registrant request for a given domain |
| GET | /v2/customers/{customerId}/domains/{domain}/changeOfRegistrant | Retrieve change of registrant information |
| PATCH | /v2/customers/{customerId}/domains/{domain}/dnssecRecords | Add the specifed DNSSEC records to the domain |
| DELETE | /v2/customers/{customerId}/domains/{domain}/dnssecRecords | Remove the specifed DNSSEC record from the domain |
| PUT | /v2/customers/{customerId}/domains/{domain}/nameServers | Replaces the existing name servers on the domain. |
| GET | /v2/customers/{customerId}/domains/{domain}/privacy/forwarding | Retrieve privacy email forwarding settings showing where emails are delivered |
| PATCH | /v2/customers/{customerId}/domains/{domain}/privacy/forwarding | Update privacy email forwarding settings to determine how emails are delivered |
| POST | /v2/customers/{customerId}/domains/{domain}/redeem | Purchase a restore for the given domain to bring it out of redemption |
| POST | /v2/customers/{customerId}/domains/{domain}/renew | Renew the specified Domain |
| POST | /v2/customers/{customerId}/domains/{domain}/transfer | Purchase and start or restart transfer process |
| GET | /v2/customers/{customerId}/domains/{domain}/transfer | Query the current transfer status |
| POST | /v2/customers/{customerId}/domains/{domain}/transfer/validate | Validate the request body using the Domain Transfer Schema for the specified TLD |
| POST | /v2/customers/{customerId}/domains/{domain}/transferInAccept | Accepts the transfer in |
| POST | /v2/customers/{customerId}/domains/{domain}/transferInCancel | Cancels the transfer in |
| POST | /v2/customers/{customerId}/domains/{domain}/transferInRestart | Restarts transfer in request from the beginning |
| POST | /v2/customers/{customerId}/domains/{domain}/transferInRetry | Retries the current transfer in request with supplied Authorization code |
| POST | /v2/customers/{customerId}/domains/{domain}/transferOut | Initiate transfer out to another registrar for a .uk domain. |
| POST | /v2/customers/{customerId}/domains/{domain}/transferOutAccept | Accept transfer out |
| POST | /v2/customers/{customerId}/domains/{domain}/transferOutReject | Reject transfer out |
| DELETE | /v2/customers/{customerId}/domains/forwards/{fqdn} | Submit a forwarding cancellation request for the given fqdn |
| GET | /v2/customers/{customerId}/domains/forwards/{fqdn} | Retrieve the forwarding information for the given fqdn |
| PUT | /v2/customers/{customerId}/domains/forwards/{fqdn} | Modify the forwarding information for the given fqdn |
| POST | /v2/customers/{customerId}/domains/forwards/{fqdn} | Create a new forwarding configuration for the given FQDN |
| GET | /v2/customers/{customerId}/domains/{domain}/actions | Retrieves a list of the most recent actions for the specified domain |
| DELETE | /v2/customers/{customerId}/domains/{domain}/actions/{type} | Cancel the most recent user action for the specified domain |
| GET | /v2/customers/{customerId}/domains/{domain}/actions/{type} | Retrieves the most recent action for the specified domain |
| GET | /v2/customers/{customerId}/domains/notifications | Retrieve the next domain notification |
| GET | /v2/customers/{customerId}/domains/notifications/optIn | Retrieve a list of notification types that are opted in |
| PUT | /v2/customers/{customerId}/domains/notifications/optIn | Opt in to recieve notifications for the submitted notification types |
| GET | /v2/customers/{customerId}/domains/notifications/schemas/{type} | Retrieve the schema for the notification data for the specified notification type |
| POST | /v2/customers/{customerId}/domains/notifications/{notificationId}/acknowledge | Acknowledge a domain notification |
| POST | /v2/customers/{customerId}/domains/register | Purchase and register the specified Domain |
| GET | /v2/customers/{customerId}/domains/register/schema/{tld} | Retrieve the schema to be submitted when registering a Domain for the specified TLD |
| POST | /v2/customers/{customerId}/domains/register/validate | Validate the request body using the Domain Registration Schema for the specified TLD |
| PATCH | /v2/customers/{customerId}/domains/{domain}/contacts | Update domain contacts |
| POST | /v2/customers/{customerId}/domains/{domain}/regenerateAuthCode | Regenerate the auth code for the given domain |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all domains?" -> GET /v1/domains
- "List all agreements?" -> GET /v1/domains/agreements
- "List all available?" -> GET /v1/domains/available
- "Create a available?" -> POST /v1/domains/available
- "Create a validate?" -> POST /v1/domains/contacts/validate
- "Create a purchase?" -> POST /v1/domains/purchase
- "Get schema details?" -> GET /v1/domains/purchase/schema/{tld}
- "Create a validate?" -> POST /v1/domains/purchase/validate
- "Search suggest?" -> GET /v1/domains/suggest
- "List all tlds?" -> GET /v1/domains/tlds
- "Delete a domain?" -> DELETE /v1/domains/{domain}
- "Get domain details?" -> GET /v1/domains/{domain}
- "Partially update a domain?" -> PATCH /v1/domains/{domain}
- "Create a purchase?" -> POST /v1/domains/{domain}/privacy/purchase
- "Get record details?" -> GET /v1/domains/{domain}/records/{type}/{name}
- "Update a record?" -> PUT /v1/domains/{domain}/records/{type}/{name}
- "Delete a record?" -> DELETE /v1/domains/{domain}/records/{type}/{name}
- "Update a record?" -> PUT /v1/domains/{domain}/records/{type}
- "Create a renew?" -> POST /v1/domains/{domain}/renew
- "Create a transfer?" -> POST /v1/domains/{domain}/transfer
- "Create a verifyRegistrantEmail?" -> POST /v1/domains/{domain}/verifyRegistrantEmail
- "Get domain details?" -> GET /v2/customers/{customerId}/domains/{domain}
- "List all changeOfRegistrant?" -> GET /v2/customers/{customerId}/domains/{domain}/changeOfRegistrant
- "List all forwarding?" -> GET /v2/customers/{customerId}/domains/{domain}/privacy/forwarding
- "Create a redeem?" -> POST /v2/customers/{customerId}/domains/{domain}/redeem
- "Create a renew?" -> POST /v2/customers/{customerId}/domains/{domain}/renew
- "Create a transfer?" -> POST /v2/customers/{customerId}/domains/{domain}/transfer
- "List all transfer?" -> GET /v2/customers/{customerId}/domains/{domain}/transfer
- "Create a validate?" -> POST /v2/customers/{customerId}/domains/{domain}/transfer/validate
- "Create a transferInAccept?" -> POST /v2/customers/{customerId}/domains/{domain}/transferInAccept
- "Create a transferInCancel?" -> POST /v2/customers/{customerId}/domains/{domain}/transferInCancel
- "Create a transferInRestart?" -> POST /v2/customers/{customerId}/domains/{domain}/transferInRestart
- "Create a transferInRetry?" -> POST /v2/customers/{customerId}/domains/{domain}/transferInRetry
- "Create a transferOut?" -> POST /v2/customers/{customerId}/domains/{domain}/transferOut
- "Create a transferOutAccept?" -> POST /v2/customers/{customerId}/domains/{domain}/transferOutAccept
- "Create a transferOutReject?" -> POST /v2/customers/{customerId}/domains/{domain}/transferOutReject
- "Delete a forward?" -> DELETE /v2/customers/{customerId}/domains/forwards/{fqdn}
- "Get forward details?" -> GET /v2/customers/{customerId}/domains/forwards/{fqdn}
- "Update a forward?" -> PUT /v2/customers/{customerId}/domains/forwards/{fqdn}
- "List all actions?" -> GET /v2/customers/{customerId}/domains/{domain}/actions
- "Delete a action?" -> DELETE /v2/customers/{customerId}/domains/{domain}/actions/{type}
- "Get action details?" -> GET /v2/customers/{customerId}/domains/{domain}/actions/{type}
- "List all notifications?" -> GET /v2/customers/{customerId}/domains/notifications
- "List all optIn?" -> GET /v2/customers/{customerId}/domains/notifications/optIn
- "Get schema details?" -> GET /v2/customers/{customerId}/domains/notifications/schemas/{type}
- "Create a acknowledge?" -> POST /v2/customers/{customerId}/domains/notifications/{notificationId}/acknowledge
- "Create a register?" -> POST /v2/customers/{customerId}/domains/register
- "Get schema details?" -> GET /v2/customers/{customerId}/domains/register/schema/{tld}
- "Create a validate?" -> POST /v2/customers/{customerId}/domains/register/validate
- "List all maintenances?" -> GET /v2/domains/maintenances
- "Get maintenance details?" -> GET /v2/domains/maintenances/{maintenanceId}
- "Get usage details?" -> GET /v2/domains/usage/{yyyymm}
- "Create a regenerateAuthCode?" -> POST /v2/customers/{customerId}/domains/{domain}/regenerateAuthCode

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
