---
name: mailchimp-transactional-api
description: "Mailchimp Transactional API skill. Use when working with Mailchimp Transactional for allowlists, exports, ips. Covers 102 endpoints."
version: 1.0.0
generator: lapsh
---

# Mailchimp Transactional API
API version: 1.3.3

## Auth
Requires API key (key parameter)

## Base URL
https://mandrillapp.com/api/1.3

## Setup
1. Include your API key via the key parameter
3. POST /allowlists/add -- create first add

## Endpoints

102 endpoints across 16 groups. See references/api-spec.lap for full details.

### allowlists
| Method | Path | Description |
|--------|------|-------------|
| POST | /allowlists/add | Add email to allowlist |
| POST | /allowlists/list | List allowlist entries |
| POST | /allowlists/delete | Remove email from allowlist |

### exports
| Method | Path | Description |
|--------|------|-------------|
| POST | /exports/info | Get export job information |
| POST | /exports/list | List export jobs |
| POST | /exports/rejects | Export rejection blacklist |
| POST | /exports/whitelist | Export rejection allowlist (legacy) |
| POST | /exports/allowlist | Export rejection allowlist |
| POST | /exports/activity | Export activity history |

### ips
| Method | Path | Description |
|--------|------|-------------|
| POST | /ips/list | List dedicated IPs |
| POST | /ips/info | Get dedicated IP information |
| POST | /ips/provision | Request dedicated IP provisioning |
| POST | /ips/start-warmup | Start IP warmup process |
| POST | /ips/cancel-warmup | Cancel IP warmup process |
| POST | /ips/set-pool | Move IP to different pool |
| POST | /ips/delete | Delete dedicated IP |
| POST | /ips/list-pools | List dedicated IP pools |
| POST | /ips/pool-info | Get pool information |
| POST | /ips/create-pool | Create dedicated IP pool |
| POST | /ips/delete-pool | Delete dedicated IP pool |
| POST | /ips/check-custom-dns | Test custom DNS configuration |
| POST | /ips/set-custom-dns | Configure custom DNS for IP |

### metadata
| Method | Path | Description |
|--------|------|-------------|
| POST | /metadata/list | List custom metadata fields |
| POST | /metadata/add | Add custom metadata field |
| POST | /metadata/update | Update custom metadata field |
| POST | /metadata/delete | Delete custom metadata field |

### rejects
| Method | Path | Description |
|--------|------|-------------|
| POST | /rejects/add | Add email to rejection blacklist |
| POST | /rejects/list | List rejection blacklist entries |
| POST | /rejects/delete | Delete email from rejection blacklist |

### senders
| Method | Path | Description |
|--------|------|-------------|
| POST | /senders/list | List senders used by this account |
| POST | /senders/domains | List sender domains |
| POST | /senders/add-domain | Add a sender domain |
| POST | /senders/check-domain | Check domain SPF and DKIM |
| POST | /senders/verify-domain | Verify a sender domain by email |
| POST | /senders/info | Get detailed information for a sender |
| POST | /senders/time-series | Get hourly stats for a sender |
| POST | /senders/delete-domain | Delete a sender domain |

### subaccounts
| Method | Path | Description |
|--------|------|-------------|
| POST | /subaccounts/list | List subaccounts |
| POST | /subaccounts/add | Add a new subaccount |
| POST | /subaccounts/info | Get subaccount information |
| POST | /subaccounts/update | Update an existing subaccount |
| POST | /subaccounts/delete | Delete a subaccount |
| POST | /subaccounts/pause | Pause a subaccount |
| POST | /subaccounts/resume | Resume a paused subaccount |

### tags
| Method | Path | Description |
|--------|------|-------------|
| POST | /tags/list | List all user-defined tags |
| POST | /tags/delete | Delete a tag permanently |
| POST | /tags/info | Get detailed information about a tag |
| POST | /tags/time-series | Get time series data for a specific tag |
| POST | /tags/all-time-series | Get time series data for all tags |

### templates
| Method | Path | Description |
|--------|------|-------------|
| POST | /templates/add | Add a new template |
| POST | /templates/info | Get template information |
| POST | /templates/update | Update an existing template |
| POST | /templates/publish | Publish a template |
| POST | /templates/delete | Delete a template |
| POST | /templates/list | List all templates |
| POST | /templates/time-series | Get template time series data |
| POST | /templates/render | Render a template |

### urls
| Method | Path | Description |
|--------|------|-------------|
| POST | /urls/list | Get most clicked URLs (DEPRECATED) |
| POST | /urls/search | Search clicked URLs (DEPRECATED) |
| POST | /urls/time-series | Get URL time series (DEPRECATED) |
| POST | /urls/tracking-domains | Get tracking domains |
| POST | /urls/add-tracking-domain | Add tracking domain |
| POST | /urls/check-tracking-domain | Check tracking domain |
| POST | /urls/delete-tracking-domain | Delete a tracking domain |

### users
| Method | Path | Description |
|--------|------|-------------|
| POST | /users/info | Return the information about the API-connected user |
| POST | /users/ping | Validate an API key and respond to a ping |
| POST | /users/ping2 | Validate an API key and respond to a ping (strict JSON parser version) |
| POST | /users/senders | Return the senders that have tried to use this account |

### webhooks
| Method | Path | Description |
|--------|------|-------------|
| POST | /webhooks/list | Get the list of all webhooks |
| POST | /webhooks/add | Add a new webhook |
| POST | /webhooks/info | Get webhook information |
| POST | /webhooks/update | Update an existing webhook |
| POST | /webhooks/delete | Delete an existing webhook |

### whitelists
| Method | Path | Description |
|--------|------|-------------|
| POST | /whitelists/add | Add email to whitelist |
| POST | /whitelists/list | List whitelist entries |
| POST | /whitelists/delete | Remove email from whitelist |

### inbound
| Method | Path | Description |
|--------|------|-------------|
| POST | /inbound/domains | List inbound domains |
| POST | /inbound/add-domain | Add inbound domain |
| POST | /inbound/check-domain | Check domain settings |
| POST | /inbound/delete-domain | Delete inbound domain |
| POST | /inbound/routes | List routes |
| POST | /inbound/add-route | Add route |
| POST | /inbound/update-route | Update mailbox route |
| POST | /inbound/delete-route | Delete mailbox route |
| POST | /inbound/send-raw | Send mime document |

### mctemplates
| Method | Path | Description |
|--------|------|-------------|
| POST | /mctemplates/info | Get Mailchimp Transactional template information |
| POST | /mctemplates/list | List Mailchimp Transactional templates |
| POST | /mctemplates/render | Render a Mailchimp Transactional template |
| POST | /mctemplates/time-series | Get Mailchimp Transactional template time series |

### messages
| Method | Path | Description |
|--------|------|-------------|
| POST | /messages/send | Send a new transactional message through the Transactional API. |
| POST | /messages/send-template | Send a new transactional message using a template |
| POST | /messages/send-mc-template | Send a new transactional message using a Mailchimp Transactional template |
| POST | /messages/search | Search recently sent messages |
| POST | /messages/search-time-series | Get time series data for message search |
| POST | /messages/info | Get information about a single sent message |
| POST | /messages/content | Get the full content of a sent message |
| POST | /messages/parse | Parse a MIME message |
| POST | /messages/send-raw | Send a raw MIME message through Mandrill |
| POST | /messages/list-scheduled | Get scheduled emails |
| POST | /messages/cancel-scheduled | Cancel a scheduled email |
| POST | /messages/reschedule | Reschedule a scheduled email |
| POST | /messages/send-sms | Send SMS message |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a add?" -> POST /allowlists/add
- "Create a list?" -> POST /allowlists/list
- "Create a delete?" -> POST /allowlists/delete
- "Create a info?" -> POST /exports/info
- "Create a list?" -> POST /exports/list
- "Create a reject?" -> POST /exports/rejects
- "Create a whitelist?" -> POST /exports/whitelist
- "Create a allowlist?" -> POST /exports/allowlist
- "Create a activity?" -> POST /exports/activity
- "Create a list?" -> POST /ips/list
- "Create a info?" -> POST /ips/info
- "Create a provision?" -> POST /ips/provision
- "Create a start-warmup?" -> POST /ips/start-warmup
- "Create a cancel-warmup?" -> POST /ips/cancel-warmup
- "Create a set-pool?" -> POST /ips/set-pool
- "Create a delete?" -> POST /ips/delete
- "Create a list-pool?" -> POST /ips/list-pools
- "Create a pool-info?" -> POST /ips/pool-info
- "Create a create-pool?" -> POST /ips/create-pool
- "Create a delete-pool?" -> POST /ips/delete-pool
- "Create a check-custom-dn?" -> POST /ips/check-custom-dns
- "Create a set-custom-dn?" -> POST /ips/set-custom-dns
- "Create a list?" -> POST /metadata/list
- "Create a add?" -> POST /metadata/add
- "Create a update?" -> POST /metadata/update
- "Create a delete?" -> POST /metadata/delete
- "Create a add?" -> POST /rejects/add
- "Create a list?" -> POST /rejects/list
- "Create a delete?" -> POST /rejects/delete
- "Create a list?" -> POST /senders/list
- "Create a domain?" -> POST /senders/domains
- "Create a add-domain?" -> POST /senders/add-domain
- "Create a check-domain?" -> POST /senders/check-domain
- "Create a verify-domain?" -> POST /senders/verify-domain
- "Create a info?" -> POST /senders/info
- "Create a time-sery?" -> POST /senders/time-series
- "Create a list?" -> POST /subaccounts/list
- "Create a add?" -> POST /subaccounts/add
- "Create a info?" -> POST /subaccounts/info
- "Create a update?" -> POST /subaccounts/update
- "Create a delete?" -> POST /subaccounts/delete
- "Create a pause?" -> POST /subaccounts/pause
- "Create a resume?" -> POST /subaccounts/resume
- "Create a list?" -> POST /tags/list
- "Create a delete?" -> POST /tags/delete
- "Create a info?" -> POST /tags/info
- "Create a time-sery?" -> POST /tags/time-series
- "Create a all-time-sery?" -> POST /tags/all-time-series
- "Create a add?" -> POST /templates/add
- "Create a info?" -> POST /templates/info
- "Create a update?" -> POST /templates/update
- "Create a publish?" -> POST /templates/publish
- "Create a delete?" -> POST /templates/delete
- "Create a list?" -> POST /templates/list
- "Create a time-sery?" -> POST /templates/time-series
- "Create a render?" -> POST /templates/render
- "Create a list?" -> POST /urls/list
- "Create a search?" -> POST /urls/search
- "Create a time-sery?" -> POST /urls/time-series
- "Create a tracking-domain?" -> POST /urls/tracking-domains
- "Create a add-tracking-domain?" -> POST /urls/add-tracking-domain
- "Create a check-tracking-domain?" -> POST /urls/check-tracking-domain
- "Create a info?" -> POST /users/info
- "Create a ping?" -> POST /users/ping
- "Create a ping2?" -> POST /users/ping2
- "Create a sender?" -> POST /users/senders
- "Create a list?" -> POST /webhooks/list
- "Create a add?" -> POST /webhooks/add
- "Create a info?" -> POST /webhooks/info
- "Create a update?" -> POST /webhooks/update
- "Create a delete?" -> POST /webhooks/delete
- "Create a add?" -> POST /whitelists/add
- "Create a list?" -> POST /whitelists/list
- "Create a delete?" -> POST /whitelists/delete
- "Create a domain?" -> POST /inbound/domains
- "Create a add-domain?" -> POST /inbound/add-domain
- "Create a check-domain?" -> POST /inbound/check-domain
- "Create a delete-domain?" -> POST /inbound/delete-domain
- "Create a route?" -> POST /inbound/routes
- "Create a add-route?" -> POST /inbound/add-route
- "Create a update-route?" -> POST /inbound/update-route
- "Create a delete-route?" -> POST /inbound/delete-route
- "Create a send-raw?" -> POST /inbound/send-raw
- "Create a info?" -> POST /mctemplates/info
- "Create a list?" -> POST /mctemplates/list
- "Create a render?" -> POST /mctemplates/render
- "Create a time-sery?" -> POST /mctemplates/time-series
- "Create a send?" -> POST /messages/send
- "Create a send-template?" -> POST /messages/send-template
- "Create a send-mc-template?" -> POST /messages/send-mc-template
- "Create a search?" -> POST /messages/search
- "Create a search-time-sery?" -> POST /messages/search-time-series
- "Create a info?" -> POST /messages/info
- "Create a content?" -> POST /messages/content
- "Create a parse?" -> POST /messages/parse
- "Create a send-raw?" -> POST /messages/send-raw
- "Create a list-scheduled?" -> POST /messages/list-scheduled
- "Create a cancel-scheduled?" -> POST /messages/cancel-scheduled
- "Create a reschedule?" -> POST /messages/reschedule
- "Create a send-sm?" -> POST /messages/send-sms
- "Create a delete-domain?" -> POST /senders/delete-domain
- "Create a delete-tracking-domain?" -> POST /urls/delete-tracking-domain

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object
- Error responses use types: Invalid_Key, MC_Exception_PaymentRequired, MC_Exception_ValidationError, Unknown_Message, Unknown_Subaccount, Unknown_Template

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
