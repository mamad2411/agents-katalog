---
name: magicbell-api
description: "MagicBell API skill. Use when working with MagicBell for broadcasts, channels, events. Covers 126 endpoints."
version: 1.0.0
generator: lapsh
---

# MagicBell API
API version: 2.0.0

## Auth
Requires API key (key parameter)

## Base URL
https://api.magicbell.com/v2

## Setup
1. Include your API key via the key parameter
2. GET /broadcasts -- verify access
3. POST /broadcasts -- create first broadcasts

## Endpoints

126 endpoints across 6 groups. See references/api-spec.lap for full details.

### broadcasts
| Method | Path | Description |
|--------|------|-------------|
| GET | /broadcasts | Retrieves a paginated list of broadcasts for the project. Returns basic information about each broadcast including its creation time and status. |
| POST | /broadcasts | Creates a new broadcast message. When a broadcast is created, it generates individual notifications for relevant users within the project. Only administrators can create broadcasts. |
| GET | /broadcasts/{broadcast_id} | Retrieves detailed information about a specific broadcast by its ID. Includes the broadcast's configuration and current status. |

### channels
| Method | Path | Description |
|--------|------|-------------|
| GET | /channels/deliveryconfig |  |
| PUT | /channels/deliveryconfig |  |
| GET | /channels/mobile_push/apns/tokens | Lists all mobile_push tokens belonging to the authenticated user. Returns a paginated list of tokens, including their status, creation dates, and associated metadata. |
| POST | /channels/mobile_push/apns/tokens | Saves a mobile_push token for the authenticated user. This token serves as a credential for accessing channel-specific functionality. Each token is unique to the user and channel combination, allowing for direct communication with the user via the channel. |
| DELETE | /channels/mobile_push/apns/tokens/{token_id} | Revokes one of the authenticated user's mobile_push tokens. This permanently invalidates the specified token, preventing it from being used for future channel access. This action cannot be undone. Users can only revoke their own tokens. |
| GET | /channels/mobile_push/apns/tokens/{token_id} | Retrieves details of a specific mobile_push token belonging to the authenticated user. Returns information about the token's status, creation date, and any associated metadata. Users can only access their own tokens. |
| GET | /channels/mobile_push/expo/tokens | Lists all mobile_push tokens belonging to the authenticated user. Returns a paginated list of tokens, including their status, creation dates, and associated metadata. |
| POST | /channels/mobile_push/expo/tokens | Saves a mobile_push token for the authenticated user. This token serves as a credential for accessing channel-specific functionality. Each token is unique to the user and channel combination, allowing for direct communication with the user via the channel. |
| DELETE | /channels/mobile_push/expo/tokens/{token_id} | Revokes one of the authenticated user's mobile_push tokens. This permanently invalidates the specified token, preventing it from being used for future channel access. This action cannot be undone. Users can only revoke their own tokens. |
| GET | /channels/mobile_push/expo/tokens/{token_id} | Retrieves details of a specific mobile_push token belonging to the authenticated user. Returns information about the token's status, creation date, and any associated metadata. Users can only access their own tokens. |
| GET | /channels/mobile_push/fcm/tokens | Lists all mobile_push tokens belonging to the authenticated user. Returns a paginated list of tokens, including their status, creation dates, and associated metadata. |
| POST | /channels/mobile_push/fcm/tokens | Saves a mobile_push token for the authenticated user. This token serves as a credential for accessing channel-specific functionality. Each token is unique to the user and channel combination, allowing for direct communication with the user via the channel. |
| DELETE | /channels/mobile_push/fcm/tokens/{token_id} | Revokes one of the authenticated user's mobile_push tokens. This permanently invalidates the specified token, preventing it from being used for future channel access. This action cannot be undone. Users can only revoke their own tokens. |
| GET | /channels/mobile_push/fcm/tokens/{token_id} | Retrieves details of a specific mobile_push token belonging to the authenticated user. Returns information about the token's status, creation date, and any associated metadata. Users can only access their own tokens. |
| GET | /channels/slack/tokens | Lists all slack tokens belonging to the authenticated user. Returns a paginated list of tokens, including their status, creation dates, and associated metadata. |
| POST | /channels/slack/tokens | Saves a slack token for the authenticated user. This token serves as a credential for accessing channel-specific functionality. Each token is unique to the user and channel combination, allowing for direct communication with the user via the channel. |
| DELETE | /channels/slack/tokens/{token_id} | Revokes one of the authenticated user's slack tokens. This permanently invalidates the specified token, preventing it from being used for future channel access. This action cannot be undone. Users can only revoke their own tokens. |
| GET | /channels/slack/tokens/{token_id} | Retrieves details of a specific slack token belonging to the authenticated user. Returns information about the token's status, creation date, and any associated metadata. Users can only access their own tokens. |
| GET | /channels/teams/tokens | Lists all teams tokens belonging to the authenticated user. Returns a paginated list of tokens, including their status, creation dates, and associated metadata. |
| POST | /channels/teams/tokens | Saves a teams token for the authenticated user. This token serves as a credential for accessing channel-specific functionality. Each token is unique to the user and channel combination, allowing for direct communication with the user via the channel. |
| DELETE | /channels/teams/tokens/{token_id} | Revokes one of the authenticated user's teams tokens. This permanently invalidates the specified token, preventing it from being used for future channel access. This action cannot be undone. Users can only revoke their own tokens. |
| GET | /channels/teams/tokens/{token_id} | Retrieves details of a specific teams token belonging to the authenticated user. Returns information about the token's status, creation date, and any associated metadata. Users can only access their own tokens. |
| GET | /channels/web_push/tokens | Lists all web_push tokens belonging to the authenticated user. Returns a paginated list of tokens, including their status, creation dates, and associated metadata. |
| POST | /channels/web_push/tokens | Saves a web_push token for the authenticated user. This token serves as a credential for accessing channel-specific functionality. Each token is unique to the user and channel combination, allowing for direct communication with the user via the channel. |
| DELETE | /channels/web_push/tokens/{token_id} | Revokes one of the authenticated user's web_push tokens. This permanently invalidates the specified token, preventing it from being used for future channel access. This action cannot be undone. Users can only revoke their own tokens. |
| GET | /channels/web_push/tokens/{token_id} | Retrieves details of a specific web_push token belonging to the authenticated user. Returns information about the token's status, creation date, and any associated metadata. Users can only access their own tokens. |

### events
| Method | Path | Description |
|--------|------|-------------|
| GET | /events | Retrieves a paginated list of events for the project. |

### integrations
| Method | Path | Description |
|--------|------|-------------|
| GET | /integrations | List Integrations |
| DELETE | /integrations/apns | Removes a apns integration configuration from the project. This will disable the integration's functionality within the project. |
| GET | /integrations/apns | Retrieves the current apns integration configurations for a specific integration type in the project. Returns configuration details and status information. |
| PUT | /integrations/apns | Creates or updates a apns integration for the project. Only administrators can configure integrations. |
| DELETE | /integrations/apns/{id} | Removes a specific apns integration instance by ID from the project. |
| DELETE | /integrations/awssns | Removes a awssns integration configuration from the project. This will disable the integration's functionality within the project. |
| GET | /integrations/awssns | Retrieves the current awssns integration configurations for a specific integration type in the project. Returns configuration details and status information. |
| PUT | /integrations/awssns | Creates or updates a awssns integration for the project. Only administrators can configure integrations. |
| POST | /integrations/awssns/webhooks/incoming/{id} | Receives and processes incoming webhook events from the awssns integration. Each integration can define its own webhook payload format and handling logic. |
| DELETE | /integrations/awssns/{id} | Removes a specific awssns integration instance by ID from the project. |
| DELETE | /integrations/expo | Removes a expo integration configuration from the project. This will disable the integration's functionality within the project. |
| GET | /integrations/expo | Retrieves the current expo integration configurations for a specific integration type in the project. Returns configuration details and status information. |
| PUT | /integrations/expo | Creates or updates a expo integration for the project. Only administrators can configure integrations. |
| DELETE | /integrations/expo/{id} | Removes a specific expo integration instance by ID from the project. |
| DELETE | /integrations/fcm | Removes a fcm integration configuration from the project. This will disable the integration's functionality within the project. |
| GET | /integrations/fcm | Retrieves the current fcm integration configurations for a specific integration type in the project. Returns configuration details and status information. |
| PUT | /integrations/fcm | Creates or updates a fcm integration for the project. Only administrators can configure integrations. |
| DELETE | /integrations/fcm/{id} | Removes a specific fcm integration instance by ID from the project. |
| DELETE | /integrations/github | Removes a github integration configuration from the project. This will disable the integration's functionality within the project. |
| GET | /integrations/github | Retrieves the current github integration configurations for a specific integration type in the project. Returns configuration details and status information. |
| PUT | /integrations/github | Creates or updates a github integration for the project. Only administrators can configure integrations. |
| POST | /integrations/github/webhooks/incoming/{id} | Receives and processes incoming webhook events from the github integration. Each integration can define its own webhook payload format and handling logic. |
| DELETE | /integrations/github/{id} | Removes a specific github integration instance by ID from the project. |
| DELETE | /integrations/inbox | Removes a inbox integration configuration from the project. This will disable the integration's functionality within the project. |
| GET | /integrations/inbox | Retrieves the current inbox integration configurations for a specific integration type in the project. Returns configuration details and status information. |
| PUT | /integrations/inbox | Creates or updates a inbox integration for the project. Only administrators can configure integrations. |
| POST | /integrations/inbox/installations | Creates a new installation of a inbox integration for a user. This endpoint is used when an integration needs to be set up with user-specific credentials or configuration. |
| POST | /integrations/inbox/installations/start | Initiates the installation flow for a inbox integration. This is the first step in a multi-step installation process where user authorization or external service configuration may be required. |
| DELETE | /integrations/inbox/{id} | Removes a specific inbox integration instance by ID from the project. |
| DELETE | /integrations/mailgun | Removes a mailgun integration configuration from the project. This will disable the integration's functionality within the project. |
| GET | /integrations/mailgun | Retrieves the current mailgun integration configurations for a specific integration type in the project. Returns configuration details and status information. |
| PUT | /integrations/mailgun | Creates or updates a mailgun integration for the project. Only administrators can configure integrations. |
| DELETE | /integrations/mailgun/{id} | Removes a specific mailgun integration instance by ID from the project. |
| DELETE | /integrations/ping_email | Removes a ping_email integration configuration from the project. This will disable the integration's functionality within the project. |
| GET | /integrations/ping_email | Retrieves the current ping_email integration configurations for a specific integration type in the project. Returns configuration details and status information. |
| PUT | /integrations/ping_email | Creates or updates a ping_email integration for the project. Only administrators can configure integrations. |
| DELETE | /integrations/ping_email/{id} | Removes a specific ping_email integration instance by ID from the project. |
| DELETE | /integrations/sendgrid | Removes a sendgrid integration configuration from the project. This will disable the integration's functionality within the project. |
| GET | /integrations/sendgrid | Retrieves the current sendgrid integration configurations for a specific integration type in the project. Returns configuration details and status information. |
| PUT | /integrations/sendgrid | Creates or updates a sendgrid integration for the project. Only administrators can configure integrations. |
| DELETE | /integrations/sendgrid/{id} | Removes a specific sendgrid integration instance by ID from the project. |
| DELETE | /integrations/ses | Removes a ses integration configuration from the project. This will disable the integration's functionality within the project. |
| GET | /integrations/ses | Retrieves the current ses integration configurations for a specific integration type in the project. Returns configuration details and status information. |
| PUT | /integrations/ses | Creates or updates a ses integration for the project. Only administrators can configure integrations. |
| DELETE | /integrations/ses/{id} | Removes a specific ses integration instance by ID from the project. |
| DELETE | /integrations/slack | Removes a slack integration configuration from the project. This will disable the integration's functionality within the project. |
| GET | /integrations/slack | Retrieves the current slack integration configurations for a specific integration type in the project. Returns configuration details and status information. |
| PUT | /integrations/slack | Creates or updates a slack integration for the project. Only administrators can configure integrations. |
| POST | /integrations/slack/installations | Creates a new installation of a slack integration for a user. This endpoint is used when an integration needs to be set up with user-specific credentials or configuration. |
| POST | /integrations/slack/installations/finish | Completes the installation flow for a slack integration. This endpoint is typically called after the user has completed any required authorization steps with slack. |
| POST | /integrations/slack/installations/start | Initiates the installation flow for a slack integration. This is the first step in a multi-step installation process where user authorization or external service configuration may be required. |
| DELETE | /integrations/slack/{id} | Removes a specific slack integration instance by ID from the project. |
| DELETE | /integrations/stripe | Removes a stripe integration configuration from the project. This will disable the integration's functionality within the project. |
| GET | /integrations/stripe | Retrieves the current stripe integration configurations for a specific integration type in the project. Returns configuration details and status information. |
| PUT | /integrations/stripe | Creates or updates a stripe integration for the project. Only administrators can configure integrations. |
| POST | /integrations/stripe/webhooks/incoming/{id} | Receives and processes incoming webhook events from the stripe integration. Each integration can define its own webhook payload format and handling logic. |
| DELETE | /integrations/stripe/{id} | Removes a specific stripe integration instance by ID from the project. |
| DELETE | /integrations/templates | Removes a templates integration configuration from the project. This will disable the integration's functionality within the project. |
| GET | /integrations/templates | Retrieves the current templates integration configurations for a specific integration type in the project. Returns configuration details and status information. |
| PUT | /integrations/templates | Creates or updates a templates integration for the project. Only administrators can configure integrations. |
| POST | /integrations/templates/installations | Creates a new installation of a templates integration for a user. This endpoint is used when an integration needs to be set up with user-specific credentials or configuration. |
| DELETE | /integrations/templates/{id} | Removes a specific templates integration instance by ID from the project. |
| DELETE | /integrations/twilio | Removes a twilio integration configuration from the project. This will disable the integration's functionality within the project. |
| GET | /integrations/twilio | Retrieves the current twilio integration configurations for a specific integration type in the project. Returns configuration details and status information. |
| PUT | /integrations/twilio | Creates or updates a twilio integration for the project. Only administrators can configure integrations. |
| DELETE | /integrations/twilio/{id} | Removes a specific twilio integration instance by ID from the project. |
| DELETE | /integrations/web_push | Removes a web_push integration configuration from the project. This will disable the integration's functionality within the project. |
| GET | /integrations/web_push | Retrieves the current web_push integration configurations for a specific integration type in the project. Returns configuration details and status information. |
| PUT | /integrations/web_push | Creates or updates a web_push integration for the project. Only administrators can configure integrations. |
| POST | /integrations/web_push/installations | Creates a new installation of a web_push integration for a user. This endpoint is used when an integration needs to be set up with user-specific credentials or configuration. |
| POST | /integrations/web_push/installations/start | Initiates the installation flow for a web_push integration. This is the first step in a multi-step installation process where user authorization or external service configuration may be required. |
| DELETE | /integrations/web_push/{id} | Removes a specific web_push integration instance by ID from the project. |

### jwt
| Method | Path | Description |
|--------|------|-------------|
| GET | /jwt/project | Retrieves a list of all active project-level JWT tokens. Returns a paginated list showing token metadata including creation date, last used date, and expiration time. For security reasons, the actual token values are not included in the response. |
| POST | /jwt/project | Creates a new project-level JWT token. These tokens provide project-wide access and should be carefully managed. Only administrators can create project tokens. The returned token should be securely stored as it cannot be retrieved again after creation. |
| DELETE | /jwt/project/{token_id} | Immediately revokes a project-level JWT token. Once revoked, any requests using this token will be rejected. This action is immediate and cannot be undone. Active sessions using this token will be terminated. |
| POST | /jwt/user | Issues a new user-specific JWT token. These tokens are scoped to individual user permissions and access levels. Only administrators can create user tokens. The token is returned only once at creation time and cannot be retrieved later. |
| DELETE | /jwt/user/{token_id} | Revokes a specific user's JWT token. This immediately invalidates the token and terminates any active sessions using it. This action cannot be undone. Administrators should use this to revoke access when needed for security purposes. |
| GET | /jwt/user/{user_id} | Lists all JWT tokens associated with a specific user. Returns token metadata including creation time, last access time, and expiration date. Administrators can use this to audit user token usage and manage active sessions. Token values are not included in the response for security reasons. |

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /users/{user_id}/channels/mobile_push/apns/tokens | Lists all mobile_push tokens associated with a specific user. This endpoint is available to project administrators and returns a paginated list of tokens, including both active and revoked tokens. |
| DELETE | /users/{user_id}/channels/mobile_push/apns/tokens/{token_id} | Revokes a specific user's mobile_push token. This endpoint is available to project administrators and permanently invalidates the specified token. Once revoked, the token can no longer be used to access channel features. This action cannot be undone. |
| GET | /users/{user_id}/channels/mobile_push/apns/tokens/{token_id} | Retrieves a specific mobile_push token by its ID for a given user. This endpoint is available to project administrators and requires project-level authentication. Use this to inspect token details including its status, creation date, and associated metadata. |
| GET | /users/{user_id}/channels/mobile_push/expo/tokens | Lists all mobile_push tokens associated with a specific user. This endpoint is available to project administrators and returns a paginated list of tokens, including both active and revoked tokens. |
| DELETE | /users/{user_id}/channels/mobile_push/expo/tokens/{token_id} | Revokes a specific user's mobile_push token. This endpoint is available to project administrators and permanently invalidates the specified token. Once revoked, the token can no longer be used to access channel features. This action cannot be undone. |
| GET | /users/{user_id}/channels/mobile_push/expo/tokens/{token_id} | Retrieves a specific mobile_push token by its ID for a given user. This endpoint is available to project administrators and requires project-level authentication. Use this to inspect token details including its status, creation date, and associated metadata. |
| GET | /users/{user_id}/channels/mobile_push/fcm/tokens | Lists all mobile_push tokens associated with a specific user. This endpoint is available to project administrators and returns a paginated list of tokens, including both active and revoked tokens. |
| DELETE | /users/{user_id}/channels/mobile_push/fcm/tokens/{token_id} | Revokes a specific user's mobile_push token. This endpoint is available to project administrators and permanently invalidates the specified token. Once revoked, the token can no longer be used to access channel features. This action cannot be undone. |
| GET | /users/{user_id}/channels/mobile_push/fcm/tokens/{token_id} | Retrieves a specific mobile_push token by its ID for a given user. This endpoint is available to project administrators and requires project-level authentication. Use this to inspect token details including its status, creation date, and associated metadata. |
| GET | /users/{user_id}/channels/slack/tokens | Lists all slack tokens associated with a specific user. This endpoint is available to project administrators and returns a paginated list of tokens, including both active and revoked tokens. |
| DELETE | /users/{user_id}/channels/slack/tokens/{token_id} | Revokes a specific user's slack token. This endpoint is available to project administrators and permanently invalidates the specified token. Once revoked, the token can no longer be used to access channel features. This action cannot be undone. |
| GET | /users/{user_id}/channels/slack/tokens/{token_id} | Retrieves a specific slack token by its ID for a given user. This endpoint is available to project administrators and requires project-level authentication. Use this to inspect token details including its status, creation date, and associated metadata. |
| GET | /users/{user_id}/channels/teams/tokens | Lists all teams tokens associated with a specific user. This endpoint is available to project administrators and returns a paginated list of tokens, including both active and revoked tokens. |
| DELETE | /users/{user_id}/channels/teams/tokens/{token_id} | Revokes a specific user's teams token. This endpoint is available to project administrators and permanently invalidates the specified token. Once revoked, the token can no longer be used to access channel features. This action cannot be undone. |
| GET | /users/{user_id}/channels/teams/tokens/{token_id} | Retrieves a specific teams token by its ID for a given user. This endpoint is available to project administrators and requires project-level authentication. Use this to inspect token details including its status, creation date, and associated metadata. |
| GET | /users/{user_id}/channels/web_push/tokens | Lists all web_push tokens associated with a specific user. This endpoint is available to project administrators and returns a paginated list of tokens, including both active and revoked tokens. |
| DELETE | /users/{user_id}/channels/web_push/tokens/{token_id} | Revokes a specific user's web_push token. This endpoint is available to project administrators and permanently invalidates the specified token. Once revoked, the token can no longer be used to access channel features. This action cannot be undone. |
| GET | /users/{user_id}/channels/web_push/tokens/{token_id} | Retrieves a specific web_push token by its ID for a given user. This endpoint is available to project administrators and requires project-level authentication. Use this to inspect token details including its status, creation date, and associated metadata. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all broadcasts?" -> GET /broadcasts
- "Create a broadcast?" -> POST /broadcasts
- "Get broadcast details?" -> GET /broadcasts/{broadcast_id}
- "List all deliveryconfig?" -> GET /channels/deliveryconfig
- "List all tokens?" -> GET /channels/mobile_push/apns/tokens
- "Create a token?" -> POST /channels/mobile_push/apns/tokens
- "Delete a token?" -> DELETE /channels/mobile_push/apns/tokens/{token_id}
- "Get token details?" -> GET /channels/mobile_push/apns/tokens/{token_id}
- "List all tokens?" -> GET /channels/mobile_push/expo/tokens
- "Create a token?" -> POST /channels/mobile_push/expo/tokens
- "Delete a token?" -> DELETE /channels/mobile_push/expo/tokens/{token_id}
- "Get token details?" -> GET /channels/mobile_push/expo/tokens/{token_id}
- "List all tokens?" -> GET /channels/mobile_push/fcm/tokens
- "Create a token?" -> POST /channels/mobile_push/fcm/tokens
- "Delete a token?" -> DELETE /channels/mobile_push/fcm/tokens/{token_id}
- "Get token details?" -> GET /channels/mobile_push/fcm/tokens/{token_id}
- "List all tokens?" -> GET /channels/slack/tokens
- "Create a token?" -> POST /channels/slack/tokens
- "Delete a token?" -> DELETE /channels/slack/tokens/{token_id}
- "Get token details?" -> GET /channels/slack/tokens/{token_id}
- "List all tokens?" -> GET /channels/teams/tokens
- "Create a token?" -> POST /channels/teams/tokens
- "Delete a token?" -> DELETE /channels/teams/tokens/{token_id}
- "Get token details?" -> GET /channels/teams/tokens/{token_id}
- "List all tokens?" -> GET /channels/web_push/tokens
- "Create a token?" -> POST /channels/web_push/tokens
- "Delete a token?" -> DELETE /channels/web_push/tokens/{token_id}
- "Get token details?" -> GET /channels/web_push/tokens/{token_id}
- "List all events?" -> GET /events
- "List all integrations?" -> GET /integrations
- "List all apns?" -> GET /integrations/apns
- "Delete a apn?" -> DELETE /integrations/apns/{id}
- "List all awssns?" -> GET /integrations/awssns
- "Delete a awssn?" -> DELETE /integrations/awssns/{id}
- "List all expo?" -> GET /integrations/expo
- "Delete a expo?" -> DELETE /integrations/expo/{id}
- "List all fcm?" -> GET /integrations/fcm
- "Delete a fcm?" -> DELETE /integrations/fcm/{id}
- "List all github?" -> GET /integrations/github
- "Delete a github?" -> DELETE /integrations/github/{id}
- "List all inbox?" -> GET /integrations/inbox
- "Create a installation?" -> POST /integrations/inbox/installations
- "Create a start?" -> POST /integrations/inbox/installations/start
- "Delete a inbox?" -> DELETE /integrations/inbox/{id}
- "List all mailgun?" -> GET /integrations/mailgun
- "Delete a mailgun?" -> DELETE /integrations/mailgun/{id}
- "List all ping_email?" -> GET /integrations/ping_email
- "Delete a ping_email?" -> DELETE /integrations/ping_email/{id}
- "List all sendgrid?" -> GET /integrations/sendgrid
- "Delete a sendgrid?" -> DELETE /integrations/sendgrid/{id}
- "List all ses?" -> GET /integrations/ses
- "Delete a se?" -> DELETE /integrations/ses/{id}
- "List all slack?" -> GET /integrations/slack
- "Create a installation?" -> POST /integrations/slack/installations
- "Create a finish?" -> POST /integrations/slack/installations/finish
- "Create a start?" -> POST /integrations/slack/installations/start
- "Delete a slack?" -> DELETE /integrations/slack/{id}
- "List all stripe?" -> GET /integrations/stripe
- "Delete a stripe?" -> DELETE /integrations/stripe/{id}
- "List all templates?" -> GET /integrations/templates
- "Create a installation?" -> POST /integrations/templates/installations
- "Delete a template?" -> DELETE /integrations/templates/{id}
- "List all twilio?" -> GET /integrations/twilio
- "Delete a twilio?" -> DELETE /integrations/twilio/{id}
- "List all web_push?" -> GET /integrations/web_push
- "Create a installation?" -> POST /integrations/web_push/installations
- "Create a start?" -> POST /integrations/web_push/installations/start
- "Delete a web_push?" -> DELETE /integrations/web_push/{id}
- "List all project?" -> GET /jwt/project
- "Create a project?" -> POST /jwt/project
- "Delete a project?" -> DELETE /jwt/project/{token_id}
- "Create a user?" -> POST /jwt/user
- "Delete a user?" -> DELETE /jwt/user/{token_id}
- "Get user details?" -> GET /jwt/user/{user_id}
- "List all tokens?" -> GET /users/{user_id}/channels/mobile_push/apns/tokens
- "Delete a token?" -> DELETE /users/{user_id}/channels/mobile_push/apns/tokens/{token_id}
- "Get token details?" -> GET /users/{user_id}/channels/mobile_push/apns/tokens/{token_id}
- "List all tokens?" -> GET /users/{user_id}/channels/mobile_push/expo/tokens
- "Delete a token?" -> DELETE /users/{user_id}/channels/mobile_push/expo/tokens/{token_id}
- "Get token details?" -> GET /users/{user_id}/channels/mobile_push/expo/tokens/{token_id}
- "List all tokens?" -> GET /users/{user_id}/channels/mobile_push/fcm/tokens
- "Delete a token?" -> DELETE /users/{user_id}/channels/mobile_push/fcm/tokens/{token_id}
- "Get token details?" -> GET /users/{user_id}/channels/mobile_push/fcm/tokens/{token_id}
- "List all tokens?" -> GET /users/{user_id}/channels/slack/tokens
- "Delete a token?" -> DELETE /users/{user_id}/channels/slack/tokens/{token_id}
- "Get token details?" -> GET /users/{user_id}/channels/slack/tokens/{token_id}
- "List all tokens?" -> GET /users/{user_id}/channels/teams/tokens
- "Delete a token?" -> DELETE /users/{user_id}/channels/teams/tokens/{token_id}
- "Get token details?" -> GET /users/{user_id}/channels/teams/tokens/{token_id}
- "List all tokens?" -> GET /users/{user_id}/channels/web_push/tokens
- "Delete a token?" -> DELETE /users/{user_id}/channels/web_push/tokens/{token_id}
- "Get token details?" -> GET /users/{user_id}/channels/web_push/tokens/{token_id}

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
