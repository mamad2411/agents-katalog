---
name: exavault-api
description: "ExaVault API skill. Use when working with ExaVault for email-lists, forms, activity. Covers 59 endpoints."
version: 1.0.0
generator: lapsh
---

# ExaVault API
API version: 2.0

## Auth
ApiKey ev-api-key in header

## Base URL
https://accountname.exavault.com/api/v2

## Setup
1. Set your API key in the appropriate header
2. GET /email-lists -- verify access
3. POST /email-lists -- create first email-lists

## Endpoints

59 endpoints across 12 groups. See references/api-spec.lap for full details.

### email-lists
| Method | Path | Description |
|--------|------|-------------|
| GET | /email-lists | Get all email groups |
| POST | /email-lists | Create new email list |
| GET | /email-lists/{id} | Get individual email group |
| PATCH | /email-lists/{id} | Update an email group |
| DELETE | /email-lists/{id} | Delete an email group with given id |

### forms
| Method | Path | Description |
|--------|------|-------------|
| GET | /forms | Get receive folder form settings |
| GET | /forms/{id} | Get receive folder form by Id |
| PATCH | /forms/{id} | Updates a form with given parameters |
| GET | /forms/entries/{id} | Get form data entries for a receive |
| DELETE | /forms/entries/{id} | Delete a receive form submission |

### activity
| Method | Path | Description |
|--------|------|-------------|
| GET | /activity/session | Get activity logs |
| GET | /activity/webhooks | Get webhook logs |

### notifications
| Method | Path | Description |
|--------|------|-------------|
| PATCH | /notifications/{id} | Update a notification |
| GET | /notifications/{id} | Get notification details |
| DELETE | /notifications/{id} | Delete a notification |
| POST | /notifications | Create a new notification |
| GET | /notifications | Get a list of notifications |

### users
| Method | Path | Description |
|--------|------|-------------|
| POST | /users | Create a user |
| GET | /users | Get a list of users |
| GET | /users/{id} | Get info for a user |
| DELETE | /users/{id} | Delete a user |
| PATCH | /users/{id} | Update a user |

### resources
| Method | Path | Description |
|--------|------|-------------|
| GET | /resources/list | Get a list of all resources |
| GET | /resources/{id} | Get resource metadata |
| PATCH | /resources/{id} | Rename a resource. |
| DELETE | /resources/{id} | Delete a Resource |
| DELETE | /resources | Delete Resources |
| POST | /resources | Create a folder |
| GET | /resources | Get Resource Properties |
| GET | /resources/list/{id} | List contents of folder |
| POST | /resources/compress | Compress resources |
| POST | /resources/extract | Extract resources |
| POST | /resources/copy | Copy resources |
| POST | /resources/move | Move resources |
| GET | /resources/preview | Preview a file |
| POST | /resources/upload | Upload a file |
| GET | /resources/download | Download a file |

### account
| Method | Path | Description |
|--------|------|-------------|
| GET | /account | Get account settings |
| PATCH | /account | Update account settings |

### email
| Method | Path | Description |
|--------|------|-------------|
| POST | /email/welcome/{username} | Resend welcome email to specific user |
| POST | /email/referral | Send referral email to a given address |

### shares
| Method | Path | Description |
|--------|------|-------------|
| POST | /shares | Creates a share |
| GET | /shares | Get a list of shares |
| GET | /shares/{id} | Get a share |
| PATCH | /shares/{id} | Update a share |
| DELETE | /shares/{id} | Deactivate a share |
| POST | /shares/complete-send/{id} | Complete send files |

### recipients
| Method | Path | Description |
|--------|------|-------------|
| POST | /recipients/shares/invites/{shareId} | Resend invitations to share recipients |

### ssh-keys
| Method | Path | Description |
|--------|------|-------------|
| GET | /ssh-keys | Get metadata for a list of SSH Keys |
| POST | /ssh-keys | Create a new SSH Key |
| GET | /ssh-keys/{id} | Get metadata for an SSH Key |
| DELETE | /ssh-keys/{id} | Delete an SSH Key |

### webhooks
| Method | Path | Description |
|--------|------|-------------|
| GET | /webhooks | Get Webhooks List |
| POST | /webhooks | Add A New Webhook |
| GET | /webhooks/{id} | Get info for a webhook |
| PATCH | /webhooks/{id} | Update a webhook |
| DELETE | /webhooks/{id} | Delete a webhook |
| POST | /webhooks/resend/{activityId} | Resend a webhook message |
| POST | /webhooks/regenerate-token/{id} | Regenerate security token |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all email-lists?" -> GET /email-lists
- "Create a email-list?" -> POST /email-lists
- "Get email-list details?" -> GET /email-lists/{id}
- "Partially update a email-list?" -> PATCH /email-lists/{id}
- "Delete a email-list?" -> DELETE /email-lists/{id}
- "List all forms?" -> GET /forms
- "Get form details?" -> GET /forms/{id}
- "Partially update a form?" -> PATCH /forms/{id}
- "Get entry details?" -> GET /forms/entries/{id}
- "Delete a entry?" -> DELETE /forms/entries/{id}
- "List all session?" -> GET /activity/session
- "List all webhooks?" -> GET /activity/webhooks
- "Partially update a notification?" -> PATCH /notifications/{id}
- "Get notification details?" -> GET /notifications/{id}
- "Delete a notification?" -> DELETE /notifications/{id}
- "Create a notification?" -> POST /notifications
- "List all notifications?" -> GET /notifications
- "Create a user?" -> POST /users
- "Search users?" -> GET /users
- "Get user details?" -> GET /users/{id}
- "Delete a user?" -> DELETE /users/{id}
- "Partially update a user?" -> PATCH /users/{id}
- "List all list?" -> GET /resources/list
- "Get resource details?" -> GET /resources/{id}
- "Partially update a resource?" -> PATCH /resources/{id}
- "Delete a resource?" -> DELETE /resources/{id}
- "Create a resource?" -> POST /resources
- "List all resources?" -> GET /resources
- "Get list details?" -> GET /resources/list/{id}
- "Create a compress?" -> POST /resources/compress
- "Create a extract?" -> POST /resources/extract
- "Create a copy?" -> POST /resources/copy
- "Create a move?" -> POST /resources/move
- "List all preview?" -> GET /resources/preview
- "Create a upload?" -> POST /resources/upload
- "List all download?" -> GET /resources/download
- "List all account?" -> GET /account
- "Create a referral?" -> POST /email/referral
- "Create a share?" -> POST /shares
- "Search shares?" -> GET /shares
- "Get share details?" -> GET /shares/{id}
- "Partially update a share?" -> PATCH /shares/{id}
- "Delete a share?" -> DELETE /shares/{id}
- "List all ssh-keys?" -> GET /ssh-keys
- "Create a ssh-key?" -> POST /ssh-keys
- "Get ssh-key details?" -> GET /ssh-keys/{id}
- "Delete a ssh-key?" -> DELETE /ssh-keys/{id}
- "List all webhooks?" -> GET /webhooks
- "Create a webhook?" -> POST /webhooks
- "Get webhook details?" -> GET /webhooks/{id}
- "Partially update a webhook?" -> PATCH /webhooks/{id}
- "Delete a webhook?" -> DELETE /webhooks/{id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
