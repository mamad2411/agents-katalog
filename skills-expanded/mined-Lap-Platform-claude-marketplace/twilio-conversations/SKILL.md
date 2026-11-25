---
name: twilio-conversations
description: "Twilio - Conversations API skill. Use when working with Twilio - Conversations for Configuration, Conversations, ConversationWithParticipants. Covers 103 endpoints."
version: 1.0.0
generator: lapsh
---

# Twilio - Conversations
API version: 1.0.0

## Auth
Bearer basic

## Base URL
https://conversations.twilio.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /v1/Configuration -- verify access
3. POST /v1/Configuration -- create first Configuration

## Endpoints

103 endpoints across 8 groups. See references/api-spec.lap for full details.

### Configuration
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/Configuration | Fetch the global configuration of conversations on your account |
| POST | /v1/Configuration | Update the global configuration of conversations on your account |
| GET | /v1/Configuration/Addresses | Retrieve a list of address configurations for an account |
| POST | /v1/Configuration/Addresses | Create a new address configuration |
| GET | /v1/Configuration/Addresses/{Sid} | Fetch an address configuration |
| POST | /v1/Configuration/Addresses/{Sid} | Update an existing address configuration |
| DELETE | /v1/Configuration/Addresses/{Sid} | Remove an existing address configuration |
| GET | /v1/Configuration/Webhooks |  |
| POST | /v1/Configuration/Webhooks |  |

### Conversations
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/Conversations | Create a new conversation in your account's default service |
| GET | /v1/Conversations | Retrieve a list of conversations in your account's default service |
| POST | /v1/Conversations/{Sid} | Update an existing conversation in your account's default service |
| DELETE | /v1/Conversations/{Sid} | Remove a conversation from your account's default service |
| GET | /v1/Conversations/{Sid} | Fetch a conversation from your account's default service |
| POST | /v1/Conversations/{ConversationSid}/Messages | Add a new message to the conversation |
| GET | /v1/Conversations/{ConversationSid}/Messages | Retrieve a list of all messages in the conversation |
| POST | /v1/Conversations/{ConversationSid}/Messages/{Sid} | Update an existing message in the conversation |
| DELETE | /v1/Conversations/{ConversationSid}/Messages/{Sid} | Remove a message from the conversation |
| GET | /v1/Conversations/{ConversationSid}/Messages/{Sid} | Fetch a message from the conversation |
| GET | /v1/Conversations/{ConversationSid}/Messages/{MessageSid}/Receipts/{Sid} | Fetch the delivery and read receipts of the conversation message |
| GET | /v1/Conversations/{ConversationSid}/Messages/{MessageSid}/Receipts | Retrieve a list of all delivery and read receipts of the conversation message |
| POST | /v1/Conversations/{ConversationSid}/Participants | Add a new participant to the conversation |
| GET | /v1/Conversations/{ConversationSid}/Participants | Retrieve a list of all participants of the conversation |
| POST | /v1/Conversations/{ConversationSid}/Participants/{Sid} | Update an existing participant in the conversation |
| DELETE | /v1/Conversations/{ConversationSid}/Participants/{Sid} | Remove a participant from the conversation |
| GET | /v1/Conversations/{ConversationSid}/Participants/{Sid} | Fetch a participant of the conversation |
| GET | /v1/Conversations/{ConversationSid}/Webhooks | Retrieve a list of all webhooks scoped to the conversation |
| POST | /v1/Conversations/{ConversationSid}/Webhooks | Create a new webhook scoped to the conversation |
| GET | /v1/Conversations/{ConversationSid}/Webhooks/{Sid} | Fetch the configuration of a conversation-scoped webhook |
| POST | /v1/Conversations/{ConversationSid}/Webhooks/{Sid} | Update an existing conversation-scoped webhook |
| DELETE | /v1/Conversations/{ConversationSid}/Webhooks/{Sid} | Remove an existing webhook scoped to the conversation |

### ConversationWithParticipants
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/ConversationWithParticipants | Create a new conversation with the list of participants in your account's default service |

### Credentials
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/Credentials | Add a new push notification credential to your account |
| GET | /v1/Credentials | Retrieve a list of all push notification credentials on your account |
| POST | /v1/Credentials/{Sid} | Update an existing push notification credential on your account |
| DELETE | /v1/Credentials/{Sid} | Remove a push notification credential from your account |
| GET | /v1/Credentials/{Sid} | Fetch a push notification credential from your account |

### ParticipantConversations
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/ParticipantConversations | Retrieve a list of all Conversations that this Participant belongs to by identity or by address. Only one parameter should be specified. |

### Roles
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/Roles | Create a new user role in your account's default service |
| GET | /v1/Roles | Retrieve a list of all user roles in your account's default service |
| POST | /v1/Roles/{Sid} | Update an existing user role in your account's default service |
| DELETE | /v1/Roles/{Sid} | Remove a user role from your account's default service |
| GET | /v1/Roles/{Sid} | Fetch a user role from your account's default service |

### Services
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/Services | Create a new conversation service on your account |
| GET | /v1/Services | Retrieve a list of all conversation services on your account |
| DELETE | /v1/Services/{Sid} | Remove a conversation service with all its nested resources from your account |
| GET | /v1/Services/{Sid} | Fetch a conversation service from your account |
| DELETE | /v1/Services/{ChatServiceSid}/Bindings/{Sid} | Remove a push notification binding from the conversation service |
| GET | /v1/Services/{ChatServiceSid}/Bindings/{Sid} | Fetch a push notification binding from the conversation service |
| GET | /v1/Services/{ChatServiceSid}/Bindings | Retrieve a list of all push notification bindings in the conversation service |
| GET | /v1/Services/{ChatServiceSid}/Configuration | Fetch the configuration of a conversation service |
| POST | /v1/Services/{ChatServiceSid}/Configuration | Update configuration settings of a conversation service |
| POST | /v1/Services/{ChatServiceSid}/Conversations | Create a new conversation in your service |
| GET | /v1/Services/{ChatServiceSid}/Conversations | Retrieve a list of conversations in your service |
| POST | /v1/Services/{ChatServiceSid}/Conversations/{Sid} | Update an existing conversation in your service |
| DELETE | /v1/Services/{ChatServiceSid}/Conversations/{Sid} | Remove a conversation from your service |
| GET | /v1/Services/{ChatServiceSid}/Conversations/{Sid} | Fetch a conversation from your service |
| POST | /v1/Services/{ChatServiceSid}/Conversations/{ConversationSid}/Messages | Add a new message to the conversation in a specific service |
| GET | /v1/Services/{ChatServiceSid}/Conversations/{ConversationSid}/Messages | Retrieve a list of all messages in the conversation |
| POST | /v1/Services/{ChatServiceSid}/Conversations/{ConversationSid}/Messages/{Sid} | Update an existing message in the conversation |
| DELETE | /v1/Services/{ChatServiceSid}/Conversations/{ConversationSid}/Messages/{Sid} | Remove a message from the conversation |
| GET | /v1/Services/{ChatServiceSid}/Conversations/{ConversationSid}/Messages/{Sid} | Fetch a message from the conversation |
| GET | /v1/Services/{ChatServiceSid}/Conversations/{ConversationSid}/Messages/{MessageSid}/Receipts/{Sid} | Fetch the delivery and read receipts of the conversation message |
| GET | /v1/Services/{ChatServiceSid}/Conversations/{ConversationSid}/Messages/{MessageSid}/Receipts | Retrieve a list of all delivery and read receipts of the conversation message |
| POST | /v1/Services/{ChatServiceSid}/Conversations/{ConversationSid}/Participants | Add a new participant to the conversation in a specific service |
| GET | /v1/Services/{ChatServiceSid}/Conversations/{ConversationSid}/Participants | Retrieve a list of all participants of the conversation |
| POST | /v1/Services/{ChatServiceSid}/Conversations/{ConversationSid}/Participants/{Sid} | Update an existing participant in the conversation |
| DELETE | /v1/Services/{ChatServiceSid}/Conversations/{ConversationSid}/Participants/{Sid} | Remove a participant from the conversation |
| GET | /v1/Services/{ChatServiceSid}/Conversations/{ConversationSid}/Participants/{Sid} | Fetch a participant of the conversation |
| POST | /v1/Services/{ChatServiceSid}/Conversations/{ConversationSid}/Webhooks | Create a new webhook scoped to the conversation in a specific service |
| GET | /v1/Services/{ChatServiceSid}/Conversations/{ConversationSid}/Webhooks | Retrieve a list of all webhooks scoped to the conversation |
| POST | /v1/Services/{ChatServiceSid}/Conversations/{ConversationSid}/Webhooks/{Sid} | Update an existing conversation-scoped webhook |
| DELETE | /v1/Services/{ChatServiceSid}/Conversations/{ConversationSid}/Webhooks/{Sid} | Remove an existing webhook scoped to the conversation |
| GET | /v1/Services/{ChatServiceSid}/Conversations/{ConversationSid}/Webhooks/{Sid} | Fetch the configuration of a conversation-scoped webhook |
| POST | /v1/Services/{ChatServiceSid}/ConversationWithParticipants | Create a new conversation with the list of participants in your account's default service |
| POST | /v1/Services/{ChatServiceSid}/Configuration/Notifications | Update push notification service settings |
| GET | /v1/Services/{ChatServiceSid}/Configuration/Notifications | Fetch push notification service settings |
| GET | /v1/Services/{ChatServiceSid}/ParticipantConversations | Retrieve a list of all Conversations that this Participant belongs to by identity or by address. Only one parameter should be specified. |
| POST | /v1/Services/{ChatServiceSid}/Roles | Create a new user role in your service |
| GET | /v1/Services/{ChatServiceSid}/Roles | Retrieve a list of all user roles in your service |
| POST | /v1/Services/{ChatServiceSid}/Roles/{Sid} | Update an existing user role in your service |
| DELETE | /v1/Services/{ChatServiceSid}/Roles/{Sid} | Remove a user role from your service |
| GET | /v1/Services/{ChatServiceSid}/Roles/{Sid} | Fetch a user role from your service |
| POST | /v1/Services/{ChatServiceSid}/Users | Add a new conversation user to your service |
| GET | /v1/Services/{ChatServiceSid}/Users | Retrieve a list of all conversation users in your service |
| POST | /v1/Services/{ChatServiceSid}/Users/{Sid} | Update an existing conversation user in your service |
| DELETE | /v1/Services/{ChatServiceSid}/Users/{Sid} | Remove a conversation user from your service |
| GET | /v1/Services/{ChatServiceSid}/Users/{Sid} | Fetch a conversation user from your service |
| POST | /v1/Services/{ChatServiceSid}/Users/{UserSid}/Conversations/{ConversationSid} | Update a specific User Conversation. |
| DELETE | /v1/Services/{ChatServiceSid}/Users/{UserSid}/Conversations/{ConversationSid} | Delete a specific User Conversation. |
| GET | /v1/Services/{ChatServiceSid}/Users/{UserSid}/Conversations/{ConversationSid} | Fetch a specific User Conversation. |
| GET | /v1/Services/{ChatServiceSid}/Users/{UserSid}/Conversations | Retrieve a list of all User Conversations for the User. |
| POST | /v1/Services/{ChatServiceSid}/Configuration/Webhooks | Update a specific Webhook. |
| GET | /v1/Services/{ChatServiceSid}/Configuration/Webhooks | Fetch a specific service webhook configuration. |

### Users
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/Users | Add a new conversation user to your account's default service |
| GET | /v1/Users | Retrieve a list of all conversation users in your account's default service |
| POST | /v1/Users/{Sid} | Update an existing conversation user in your account's default service |
| DELETE | /v1/Users/{Sid} | Remove a conversation user from your account's default service |
| GET | /v1/Users/{Sid} | Fetch a conversation user from your account's default service |
| POST | /v1/Users/{UserSid}/Conversations/{ConversationSid} | Update a specific User Conversation. |
| DELETE | /v1/Users/{UserSid}/Conversations/{ConversationSid} | Delete a specific User Conversation. |
| GET | /v1/Users/{UserSid}/Conversations/{ConversationSid} | Fetch a specific User Conversation. |
| GET | /v1/Users/{UserSid}/Conversations | Retrieve a list of all User Conversations for the User. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all Configuration?" -> GET /v1/Configuration
- "Create a Configuration?" -> POST /v1/Configuration
- "List all Addresses?" -> GET /v1/Configuration/Addresses
- "Create a Address?" -> POST /v1/Configuration/Addresses
- "Get Address details?" -> GET /v1/Configuration/Addresses/{Sid}
- "Delete a Address?" -> DELETE /v1/Configuration/Addresses/{Sid}
- "List all Webhooks?" -> GET /v1/Configuration/Webhooks
- "Create a Webhook?" -> POST /v1/Configuration/Webhooks
- "Create a Conversation?" -> POST /v1/Conversations
- "List all Conversations?" -> GET /v1/Conversations
- "Delete a Conversation?" -> DELETE /v1/Conversations/{Sid}
- "Get Conversation details?" -> GET /v1/Conversations/{Sid}
- "Create a Message?" -> POST /v1/Conversations/{ConversationSid}/Messages
- "List all Messages?" -> GET /v1/Conversations/{ConversationSid}/Messages
- "Delete a Message?" -> DELETE /v1/Conversations/{ConversationSid}/Messages/{Sid}
- "Get Message details?" -> GET /v1/Conversations/{ConversationSid}/Messages/{Sid}
- "Get Receipt details?" -> GET /v1/Conversations/{ConversationSid}/Messages/{MessageSid}/Receipts/{Sid}
- "List all Receipts?" -> GET /v1/Conversations/{ConversationSid}/Messages/{MessageSid}/Receipts
- "Create a Participant?" -> POST /v1/Conversations/{ConversationSid}/Participants
- "List all Participants?" -> GET /v1/Conversations/{ConversationSid}/Participants
- "Delete a Participant?" -> DELETE /v1/Conversations/{ConversationSid}/Participants/{Sid}
- "Get Participant details?" -> GET /v1/Conversations/{ConversationSid}/Participants/{Sid}
- "List all Webhooks?" -> GET /v1/Conversations/{ConversationSid}/Webhooks
- "Create a Webhook?" -> POST /v1/Conversations/{ConversationSid}/Webhooks
- "Get Webhook details?" -> GET /v1/Conversations/{ConversationSid}/Webhooks/{Sid}
- "Delete a Webhook?" -> DELETE /v1/Conversations/{ConversationSid}/Webhooks/{Sid}
- "Create a ConversationWithParticipant?" -> POST /v1/ConversationWithParticipants
- "Create a Credential?" -> POST /v1/Credentials
- "List all Credentials?" -> GET /v1/Credentials
- "Delete a Credential?" -> DELETE /v1/Credentials/{Sid}
- "Get Credential details?" -> GET /v1/Credentials/{Sid}
- "List all ParticipantConversations?" -> GET /v1/ParticipantConversations
- "Create a Role?" -> POST /v1/Roles
- "List all Roles?" -> GET /v1/Roles
- "Delete a Role?" -> DELETE /v1/Roles/{Sid}
- "Get Role details?" -> GET /v1/Roles/{Sid}
- "Create a Service?" -> POST /v1/Services
- "List all Services?" -> GET /v1/Services
- "Delete a Service?" -> DELETE /v1/Services/{Sid}
- "Get Service details?" -> GET /v1/Services/{Sid}
- "Delete a Binding?" -> DELETE /v1/Services/{ChatServiceSid}/Bindings/{Sid}
- "Get Binding details?" -> GET /v1/Services/{ChatServiceSid}/Bindings/{Sid}
- "List all Bindings?" -> GET /v1/Services/{ChatServiceSid}/Bindings
- "List all Configuration?" -> GET /v1/Services/{ChatServiceSid}/Configuration
- "Create a Configuration?" -> POST /v1/Services/{ChatServiceSid}/Configuration
- "Create a Conversation?" -> POST /v1/Services/{ChatServiceSid}/Conversations
- "List all Conversations?" -> GET /v1/Services/{ChatServiceSid}/Conversations
- "Delete a Conversation?" -> DELETE /v1/Services/{ChatServiceSid}/Conversations/{Sid}
- "Get Conversation details?" -> GET /v1/Services/{ChatServiceSid}/Conversations/{Sid}
- "Create a Message?" -> POST /v1/Services/{ChatServiceSid}/Conversations/{ConversationSid}/Messages
- "List all Messages?" -> GET /v1/Services/{ChatServiceSid}/Conversations/{ConversationSid}/Messages
- "Delete a Message?" -> DELETE /v1/Services/{ChatServiceSid}/Conversations/{ConversationSid}/Messages/{Sid}
- "Get Message details?" -> GET /v1/Services/{ChatServiceSid}/Conversations/{ConversationSid}/Messages/{Sid}
- "Get Receipt details?" -> GET /v1/Services/{ChatServiceSid}/Conversations/{ConversationSid}/Messages/{MessageSid}/Receipts/{Sid}
- "List all Receipts?" -> GET /v1/Services/{ChatServiceSid}/Conversations/{ConversationSid}/Messages/{MessageSid}/Receipts
- "Create a Participant?" -> POST /v1/Services/{ChatServiceSid}/Conversations/{ConversationSid}/Participants
- "List all Participants?" -> GET /v1/Services/{ChatServiceSid}/Conversations/{ConversationSid}/Participants
- "Delete a Participant?" -> DELETE /v1/Services/{ChatServiceSid}/Conversations/{ConversationSid}/Participants/{Sid}
- "Get Participant details?" -> GET /v1/Services/{ChatServiceSid}/Conversations/{ConversationSid}/Participants/{Sid}
- "Create a Webhook?" -> POST /v1/Services/{ChatServiceSid}/Conversations/{ConversationSid}/Webhooks
- "List all Webhooks?" -> GET /v1/Services/{ChatServiceSid}/Conversations/{ConversationSid}/Webhooks
- "Delete a Webhook?" -> DELETE /v1/Services/{ChatServiceSid}/Conversations/{ConversationSid}/Webhooks/{Sid}
- "Get Webhook details?" -> GET /v1/Services/{ChatServiceSid}/Conversations/{ConversationSid}/Webhooks/{Sid}
- "Create a ConversationWithParticipant?" -> POST /v1/Services/{ChatServiceSid}/ConversationWithParticipants
- "Create a Notification?" -> POST /v1/Services/{ChatServiceSid}/Configuration/Notifications
- "List all Notifications?" -> GET /v1/Services/{ChatServiceSid}/Configuration/Notifications
- "List all ParticipantConversations?" -> GET /v1/Services/{ChatServiceSid}/ParticipantConversations
- "Create a Role?" -> POST /v1/Services/{ChatServiceSid}/Roles
- "List all Roles?" -> GET /v1/Services/{ChatServiceSid}/Roles
- "Delete a Role?" -> DELETE /v1/Services/{ChatServiceSid}/Roles/{Sid}
- "Get Role details?" -> GET /v1/Services/{ChatServiceSid}/Roles/{Sid}
- "Create a User?" -> POST /v1/Services/{ChatServiceSid}/Users
- "List all Users?" -> GET /v1/Services/{ChatServiceSid}/Users
- "Delete a User?" -> DELETE /v1/Services/{ChatServiceSid}/Users/{Sid}
- "Get User details?" -> GET /v1/Services/{ChatServiceSid}/Users/{Sid}
- "Delete a Conversation?" -> DELETE /v1/Services/{ChatServiceSid}/Users/{UserSid}/Conversations/{ConversationSid}
- "Get Conversation details?" -> GET /v1/Services/{ChatServiceSid}/Users/{UserSid}/Conversations/{ConversationSid}
- "List all Conversations?" -> GET /v1/Services/{ChatServiceSid}/Users/{UserSid}/Conversations
- "Create a Webhook?" -> POST /v1/Services/{ChatServiceSid}/Configuration/Webhooks
- "List all Webhooks?" -> GET /v1/Services/{ChatServiceSid}/Configuration/Webhooks
- "Create a User?" -> POST /v1/Users
- "List all Users?" -> GET /v1/Users
- "Delete a User?" -> DELETE /v1/Users/{Sid}
- "Get User details?" -> GET /v1/Users/{Sid}
- "Delete a Conversation?" -> DELETE /v1/Users/{UserSid}/Conversations/{ConversationSid}
- "Get Conversation details?" -> GET /v1/Users/{UserSid}/Conversations/{ConversationSid}
- "List all Conversations?" -> GET /v1/Users/{UserSid}/Conversations
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
