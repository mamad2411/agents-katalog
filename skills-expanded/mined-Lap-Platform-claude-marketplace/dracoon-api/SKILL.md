---
name: dracoon-api
description: "DRACOON API skill. Use when working with DRACOON for public, downloads, users. Covers 314 endpoints."
version: 1.0.0
generator: lapsh
---

# DRACOON API
API version: 5.47.0

## Auth
OAuth2

## Base URL
/api

## Setup
1. Configure auth: OAuth2
2. GET /v4/user/subscriptions/upload_shares -- verify access
3. POST /v4/users/{user_id}/userAttributes -- create first userAttributes

## Endpoints

314 endpoints across 17 groups. See references/api-spec.lap for full details.

### public
| Method | Path | Description |
|--------|------|-------------|
| GET | /v4/public/shares/downloads/{access_key}/{token} | Download file with token |
| HEAD | /v4/public/shares/downloads/{access_key}/{token} | Download file with token |
| GET | /v4/public/shares/uploads/{access_key}/{upload_id} | Request status of S3 file upload |
| PUT | /v4/public/shares/uploads/{access_key}/{upload_id} | Complete file upload |
| POST | /v4/public/shares/uploads/{access_key}/{upload_id} | Upload file |
| DELETE | /v4/public/shares/uploads/{access_key}/{upload_id} | Cancel file upload |
| PUT | /v4/public/shares/uploads/{access_key}/{upload_id}/s3 | Complete S3 file upload |
| GET | /v4/public/shares/uploads/{access_key} | Request public Upload Share information |
| POST | /v4/public/shares/uploads/{access_key} | Create new file upload channel |
| POST | /v4/public/shares/uploads/{access_key}/{upload_id}/s3_urls | Generate presigned URLs for S3 file upload |
| GET | /v4/public/shares/downloads/{access_key} | Request public Download Share information |
| POST | /v4/public/shares/downloads/{access_key} | Generate download URL |
| HEAD | /v4/public/shares/downloads/{access_key} | Check public Download Share password |
| GET | /v4/public/time | Request system time |
| GET | /v4/public/system/info | Request system information |
| GET | /v4/public/system/info/auth/openid | Request OpenID Connect provider authentication information |
| GET | /v4/public/system/info/auth/ad | Request Active Directory authentication information |
| GET | /v4/public/software/version | Request software version information |
| GET | /v4/public/software/third_party_dependencies | Request third-party software dependencies |

### downloads
| Method | Path | Description |
|--------|------|-------------|
| GET | /v4/downloads/{token} | Download file |
| HEAD | /v4/downloads/{token} | Download file |
| GET | /v4/downloads/zip/{token} | Download ZIP archive |
| GET | /v4/downloads/avatar/{user_id}/{uuid} | Download avatar |

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /v4/users/{user_id} | Request user |
| PUT | /v4/users/{user_id} | Update user's metadata |
| DELETE | /v4/users/{user_id} | Remove user |
| GET | /v4/users/{user_id}/userAttributes | Request custom user attributes |
| PUT | /v4/users/{user_id}/userAttributes | Add or edit custom user attributes |
| POST | /v4/users/{user_id}/userAttributes | Set custom user attributes |
| GET | /v4/users | Request users |
| POST | /v4/users | Create new user |
| POST | /v4/users/{user_id}/mfa/emergency_code | Request emergency MFA code |
| GET | /v4/users/{user_id}/rooms | Request rooms granted to the user or / and rooms that can be granted |
| GET | /v4/users/{user_id}/roles | Request user's granted roles |
| GET | /v4/users/{user_id}/last_admin_rooms | Request rooms where the user is last admin |
| GET | /v4/users/{user_id}/groups | Request groups that user is a member of or / and can become a member |
| DELETE | /v4/users/{user_id}/userAttributes/{key} | Remove custom user attribute |
| DELETE | /v4/users/{user_id}/mfa | Reset MFA for user |

### user
| Method | Path | Description |
|--------|------|-------------|
| GET | /v4/user/subscriptions/upload_shares | List Upload Share subscriptions |
| PUT | /v4/user/subscriptions/upload_shares | Subscribe or Unsubscribe a List of Upload Shares for notifications |
| GET | /v4/user/subscriptions/nodes | List node subscriptions |
| PUT | /v4/user/subscriptions/nodes | Subscribe or Unsubscribe a List of nodes for notifications |
| GET | /v4/user/subscriptions/download_shares | List Download Share subscriptions |
| PUT | /v4/user/subscriptions/download_shares | Subscribe or Unsubscribe a List of Download Shares for notifications |
| GET | /v4/user/profileAttributes | Request user profile attributes |
| PUT | /v4/user/profileAttributes | Add or edit user profile attributes |
| POST | /v4/user/profileAttributes | Set user profile attributes |
| PUT | /v4/user/notifications/config/{id} | Update notification configuration |
| GET | /v4/user/account | Request user account information |
| PUT | /v4/user/account | Update user account |
| PUT | /v4/user/account/password | Change user's password |
| GET | /v4/user/account/customer | Request customer information for user |
| PUT | /v4/user/account/customer | Activate client-side encryption for customer |
| POST | /v4/user/subscriptions/upload_shares/{share_id} | Subscribe Upload Share for notifications |
| DELETE | /v4/user/subscriptions/upload_shares/{share_id} | Unsubscribe Upload Share from notifications |
| POST | /v4/user/subscriptions/nodes/{node_id} | Subscribe node for notifications |
| DELETE | /v4/user/subscriptions/nodes/{node_id} | Unsubscribe node from notifications |
| POST | /v4/user/subscriptions/download_shares/{share_id} | Subscribe Download Share for notifications |
| DELETE | /v4/user/subscriptions/download_shares/{share_id} | Unsubscribe Download Share from notifications |
| GET | /v4/user/account/mfa/totp | Request information to setup TOTP as second authentication factor |
| POST | /v4/user/account/mfa/totp | Confirm second factor TOTP setup with a generated OTP |
| GET | /v4/user/account/keypairs | Request all user key pairs |
| POST | /v4/user/account/keypairs | Create key pair and preserve copy of old private key |
| GET | /v4/user/account/keypair | Request user's key pair |
| POST | /v4/user/account/keypair | Set user's key pair |
| DELETE | /v4/user/account/keypair | Remove user's key pair |
| GET | /v4/user/account/avatar | Request avatar |
| POST | /v4/user/account/avatar | Change avatar |
| DELETE | /v4/user/account/avatar | Reset avatar |
| GET | /v4/user/ping | (authenticated) Ping |
| GET | /v4/user/oauth/authorizations | Request list of OAuth client authorizations |
| GET | /v4/user/oauth/approvals | Request list of OAuth client approvals |
| GET | /v4/user/notifications/config | Request list of notification configurations |
| GET | /v4/user/account/mfa | Request information about the user's mfa status |
| DELETE | /v4/user/account/mfa | Using emergency-code |
| GET | /v4/user/account/customer/keypair | Request customer's key pair |
| DELETE | /v4/user/profileAttributes/{key} | Remove user profile attribute |
| DELETE | /v4/user/oauth/authorizations/{client_id} | Remove all OAuth authorizations of a client |
| DELETE | /v4/user/oauth/authorizations/{client_id}/{authorization_id} | Remove a OAuth authorization |
| DELETE | /v4/user/oauth/approvals/{client_id} | Remove OAuth client approval |
| DELETE | /v4/user/account/mfa/totp/{id} | Disable a MFA TOTP setup with generated OTP |

### uploads
| Method | Path | Description |
|--------|------|-------------|
| PUT | /v4/uploads/{token} | Complete file upload |
| POST | /v4/uploads/{token} | Upload file |
| DELETE | /v4/uploads/{token} | Cancel file upload |

### system
| Method | Path | Description |
|--------|------|-------------|
| GET | /v4/system/config/storage/s3 | Request S3 storage configuration |
| PUT | /v4/system/config/storage/s3 | Update S3 storage configuration |
| POST | /v4/system/config/storage/s3 | Create S3 storage configuration |
| GET | /v4/system/config/settings/syslog | Request syslog settings |
| PUT | /v4/system/config/settings/syslog | Update syslog settings |
| GET | /v4/system/config/settings/general | Request general settings |
| PUT | /v4/system/config/settings/general | Update general settings |
| GET | /v4/system/config/settings/eventlog | Request eventlog settings |
| PUT | /v4/system/config/settings/eventlog | Update eventlog settings |
| GET | /v4/system/config/settings/defaults | Request system defaults |
| PUT | /v4/system/config/settings/defaults | Update system defaults |
| GET | /v4/system/config/settings/auth | Request authentication settings |
| PUT | /v4/system/config/settings/auth | Update authentication settings |
| GET | /v4/system/config/policies/virus_protection | Request virus protection policies |
| PUT | /v4/system/config/policies/virus_protection | Change virus protection policies |
| GET | /v4/system/config/policies/passwords | Request password policies |
| PUT | /v4/system/config/policies/passwords | Change password policies |
| GET | /v4/system/config/policies/mfa | Request MFA policies |
| PUT | /v4/system/config/policies/mfa | Change MFA policies |
| PUT | /v4/system/config/policies/mfa/{user_type} | Change MFA policies for internal/external users |
| GET | /v4/system/config/policies/guest_users | Request guest user policies |
| PUT | /v4/system/config/policies/guest_users | Change guest user policies |
| GET | /v4/system/config/policies/classifications | Request classification policies |
| PUT | /v4/system/config/policies/classifications | Change classification policies |
| GET | /v4/system/config/oauth/clients/{client_id} | Request OAuth client |
| PUT | /v4/system/config/oauth/clients/{client_id} | Update OAuth client |
| DELETE | /v4/system/config/oauth/clients/{client_id} | Remove OAuth client |
| GET | /v4/system/config/auth/openid/idps/{idp_id} | Request OpenID Connect IDP configuration |
| PUT | /v4/system/config/auth/openid/idps/{idp_id} | Update OpenID Connect IDP configuration |
| DELETE | /v4/system/config/auth/openid/idps/{idp_id} | Remove OpenID Connect IDP configuration |
| GET | /v4/system/config/auth/ads/{ad_id} | Request Active Directory configuration |
| PUT | /v4/system/config/auth/ads/{ad_id} | Update Active Directory configuration |
| DELETE | /v4/system/config/auth/ads/{ad_id} | Remove Active Directory configuration |
| GET | /v4/system/config/storage/s3/tags | Request list of configured S3 tags |
| POST | /v4/system/config/storage/s3/tags | Create S3 tag |
| POST | /v4/system/config/policies/passwords/enforce_change | Enforce login password change for all users |
| GET | /v4/system/config/oauth/clients | Request list of OAuth clients |
| POST | /v4/system/config/oauth/clients | Create OAuth client |
| GET | /v4/system/config/auth/openid/idps | Request list of OpenID Connect IDP configurations |
| POST | /v4/system/config/auth/openid/idps | Create OpenID Connect IDP configuration |
| GET | /v4/system/config/auth/ads | Request list of Active Directory configurations |
| POST | /v4/system/config/auth/ads | Create Active Directory configuration |
| POST | /v4/system/config/actions/test/ad | Test Active Directory configuration |
| GET | /v4/system/config/storage/s3/tags/{id} | Request S3 tag |
| DELETE | /v4/system/config/storage/s3/tags/{id} | Remove S3 tag |
| GET | /v4/system/config/settings/infrastructure | Request infrastructure properties |
| GET | /v4/system/config/policies/passwords/{password_type} | Request password policies for a certain password type |

### shares
| Method | Path | Description |
|--------|------|-------------|
| GET | /v4/shares/uploads | Request list of Upload Shares |
| PUT | /v4/shares/uploads | Update List of Upload Shares |
| POST | /v4/shares/uploads | Create new Upload Share |
| DELETE | /v4/shares/uploads | Remove Upload Shares |
| GET | /v4/shares/uploads/{share_id} | Request Upload Share |
| PUT | /v4/shares/uploads/{share_id} | Update Upload Share |
| DELETE | /v4/shares/uploads/{share_id} | Remove Upload Share |
| GET | /v4/shares/downloads | Request list of Download Shares |
| PUT | /v4/shares/downloads | Update a list of Download Shares |
| POST | /v4/shares/downloads | Create new Download Share |
| DELETE | /v4/shares/downloads | Remove Download Shares |
| GET | /v4/shares/downloads/{share_id} | Request Download Share |
| PUT | /v4/shares/downloads/{share_id} | Update Download Share |
| DELETE | /v4/shares/downloads/{share_id} | Remove Download Share |
| POST | /v4/shares/uploads/{share_id}/email | Send an existing Upload Share link via email |
| POST | /v4/shares/downloads/{share_id}/email | Send an existing Download Share link via email |
| GET | /v4/shares/uploads/{share_id}/qr | Request Upload Share via QR Code |
| GET | /v4/shares/downloads/{share_id}/qr | Request Download Share via QR Code |

### settings
| Method | Path | Description |
|--------|------|-------------|
| GET | /v4/settings | Request customer settings |
| PUT | /v4/settings | Set customer settings |
| GET | /v4/settings/webhooks/{webhook_id} | Request webhook |
| PUT | /v4/settings/webhooks/{webhook_id} | Update webhook |
| DELETE | /v4/settings/webhooks/{webhook_id} | Remove webhook |
| GET | /v4/settings/notifications/channels | Request list of notification channels |
| PUT | /v4/settings/notifications/channels | Toggle notification channels |
| GET | /v4/settings/webhooks | Request list of webhooks |
| POST | /v4/settings/webhooks | Create webhook |
| POST | /v4/settings/webhooks/{webhook_id}/reset_lifetime | Reset webhook lifetime |
| GET | /v4/settings/keypairs | Request all system rescue key pairs |
| POST | /v4/settings/keypairs | Create system rescue key pair and preserve copy of old private key |
| GET | /v4/settings/keypair | Request system rescue key pair |
| POST | /v4/settings/keypair | Activate client-side encryption for customer |
| DELETE | /v4/settings/keypair | Remove system rescue key pair |
| GET | /v4/settings/webhooks/event_types | Request list of event types |

### provisioning
| Method | Path | Description |
|--------|------|-------------|
| GET | /v4/provisioning/webhooks/{webhook_id} | Request tenant webhook |
| PUT | /v4/provisioning/webhooks/{webhook_id} | Update tenant webhook |
| DELETE | /v4/provisioning/webhooks/{webhook_id} | Remove tenant webhook |
| GET | /v4/provisioning/customers/{customer_id} | Get customer |
| PUT | /v4/provisioning/customers/{customer_id} | Update customer |
| DELETE | /v4/provisioning/customers/{customer_id} | Remove customer |
| GET | /v4/provisioning/customers/{customer_id}/customerAttributes | Request customer attributes |
| PUT | /v4/provisioning/customers/{customer_id}/customerAttributes | Add or edit customer attributes |
| POST | /v4/provisioning/customers/{customer_id}/customerAttributes | Set customer attributes |
| GET | /v4/provisioning/webhooks | Request list of tenant webhooks |
| POST | /v4/provisioning/webhooks | Create tenant webhook |
| POST | /v4/provisioning/webhooks/{webhook_id}/reset_lifetime | Reset tenant webhook lifetime |
| GET | /v4/provisioning/customers | Request list of customers |
| POST | /v4/provisioning/customers | Create customer |
| GET | /v4/provisioning/webhooks/event_types | Request list of event types |
| GET | /v4/provisioning/customers/{customer_id}/users | Request list of customer users |
| DELETE | /v4/provisioning/customers/{customer_id}/customerAttributes/{key} | Remove customer attribute |

### nodes
| Method | Path | Description |
|--------|------|-------------|
| GET | /v4/nodes/{node_id}/node_attributes | Request custom node attributes |
| PUT | /v4/nodes/{node_id}/node_attributes | Add or edit custom node attributes |
| PUT | /v4/nodes/rooms/{room_id} | Updates room’s metadata |
| GET | /v4/nodes/rooms/{room_id}/webhooks | Request list of webhooks that are assigned or can be assigned to this room |
| PUT | /v4/nodes/rooms/{room_id}/webhooks | Assign or unassign webhooks to room |
| GET | /v4/nodes/rooms/{room_id}/users | Request room granted user(s) or / and user(s) that can be granted |
| PUT | /v4/nodes/rooms/{room_id}/users | Add or change room granted user(s) |
| DELETE | /v4/nodes/rooms/{room_id}/users | Revoke granted user(s) from room |
| GET | /v4/nodes/rooms/{room_id}/policies | Request Room Policies |
| PUT | /v4/nodes/rooms/{room_id}/policies | Set room policies |
| PUT | /v4/nodes/rooms/{room_id}/guest_users | Add guest users to a room |
| GET | /v4/nodes/rooms/{room_id}/groups | Request room granted group(s) or / and group(s) that can be granted |
| PUT | /v4/nodes/rooms/{room_id}/groups | Add or change room granted group(s) |
| DELETE | /v4/nodes/rooms/{room_id}/groups | Revoke granted group(s) from room |
| PUT | /v4/nodes/rooms/{room_id}/encrypt | Encrypt room |
| PUT | /v4/nodes/rooms/{room_id}/config | Configure room |
| GET | /v4/nodes/rooms/pending | Request user-room assignments per group |
| PUT | /v4/nodes/rooms/pending | Handle user-room assignments per group |
| PUT | /v4/nodes/folders/{folder_id} | Updates folder’s metadata |
| PUT | /v4/nodes/files | Updates a list of  file’s metadata |
| PUT | /v4/nodes/files/{file_id} | Updates a file’s metadata |
| GET | /v4/nodes/files/uploads/{upload_id} | Request status of S3 file upload |
| PUT | /v4/nodes/files/uploads/{upload_id} | Complete file upload |
| POST | /v4/nodes/files/uploads/{upload_id} | Upload file |
| DELETE | /v4/nodes/files/uploads/{upload_id} | Cancel file upload |
| PUT | /v4/nodes/files/uploads/{upload_id}/s3 | Complete S3 file upload |
| PUT | /v4/nodes/favorites | Mark or unmark a list of nodes (room, folder or file) as favorite |
| PUT | /v4/nodes/comments/{comment_id} | Edit node comment |
| DELETE | /v4/nodes/comments/{comment_id} | Remove node comment |
| POST | /v4/nodes/{node_id}/move_to | Move node(s) |
| POST | /v4/nodes/{node_id}/favorite | Mark a node (room, folder or file) as favorite |
| DELETE | /v4/nodes/{node_id}/favorite | Unmark a node (room, folder or file) as favorite |
| POST | /v4/nodes/{node_id}/copy_to | Copy node(s) |
| GET | /v4/nodes/{node_id}/comments | Request list of node comments |
| POST | /v4/nodes/{node_id}/comments | Create node comment |
| POST | /v4/nodes/zip | Generate download URL for ZIP download |
| POST | /v4/nodes/zip/download | Download files / folders as ZIP archive |
| POST | /v4/nodes/rooms | Create new room |
| GET | /v4/nodes/rooms/{room_id}/s3_tags | Request list of all assigned S3 tags to the room |
| POST | /v4/nodes/rooms/{room_id}/s3_tags | Set S3 tags for a room |
| GET | /v4/nodes/rooms/{room_id}/keypairs | Request all room rescue key pairs |
| POST | /v4/nodes/rooms/{room_id}/keypairs | Create key pair and preserve copy of old private key |
| GET | /v4/nodes/rooms/{room_id}/keypair | Request room rescue key |
| POST | /v4/nodes/rooms/{room_id}/keypair | Set room's rescue key pair |
| DELETE | /v4/nodes/rooms/{room_id}/keypair | Remove rooms's rescue key pair |
| POST | /v4/nodes/folders | Create new folder |
| POST | /v4/nodes/files/{file_id}/downloads | Generate download URL |
| POST | /v4/nodes/files/uploads | Create new file upload channel |
| POST | /v4/nodes/files/uploads/{upload_id}/s3_urls | Generate presigned URLs for S3 file upload |
| POST | /v4/nodes/files/keys | Set file keys for a list of users and files |
| POST | /v4/nodes/files/generate_verdict_info | Generate Virus Protection Verdict Information |
| POST | /v4/nodes/deleted_nodes/actions/restore | Restore deleted nodes |
| GET | /v4/nodes | Request list of nodes |
| DELETE | /v4/nodes | Remove nodes |
| GET | /v4/nodes/{node_id} | Request node |
| DELETE | /v4/nodes/{node_id} | Remove node |
| GET | /v4/nodes/{node_id}/parents | Request list of parent nodes |
| GET | /v4/nodes/{node_id}/deleted_nodes | Request list of deleted nodes |
| DELETE | /v4/nodes/{node_id}/deleted_nodes | Empty recycle bin |
| GET | /v4/nodes/{node_id}/deleted_nodes/versions | Request deleted versions of nodes |
| GET | /v4/nodes/search | Search nodes |
| GET | /v4/nodes/rooms/{room_id}/events | Request events of a room |
| GET | /v4/nodes/missingFileKeys | Request files without user's file key |
| GET | /v4/nodes/files/{file_id}/user_file_key | Request user's file key |
| GET | /v4/nodes/files/{file_id}/data_space_file_key | Request system rescue key |
| GET | /v4/nodes/files/{file_id}/data_room_file_key | Request room rescue key |
| GET | /v4/nodes/files/versions/{reference_id} | Request list of file versions |
| GET | /v4/nodes/deleted_nodes/{deleted_node_id} | Request deleted node |
| DELETE | /v4/nodes/{node_id}/node_attributes/{key} | Remove custom node attribute |
| DELETE | /v4/nodes/malicious_files/{malicious_file_id} | Remove malicious File |
| DELETE | /v4/nodes/deleted_nodes | Remove nodes from recycle bin |

### groups
| Method | Path | Description |
|--------|------|-------------|
| GET | /v4/groups/{group_id} | Request user group |
| PUT | /v4/groups/{group_id} | Update user group's metadata |
| DELETE | /v4/groups/{group_id} | Remove user group |
| GET | /v4/groups | Request list of user groups |
| POST | /v4/groups | Create new user group |
| GET | /v4/groups/{group_id}/users | Request group member users or / and users who can become a member |
| POST | /v4/groups/{group_id}/users | Add group members |
| DELETE | /v4/groups/{group_id}/users | Remove group members |
| GET | /v4/groups/{group_id}/rooms | Request rooms granted to the group or / and rooms that can be granted |
| GET | /v4/groups/{group_id}/roles | Request list of roles assigned to the group |
| GET | /v4/groups/{group_id}/last_admin_rooms | Request rooms where the group is defined as last admin group |

### config
| Method | Path | Description |
|--------|------|-------------|
| GET | /v4/config/settings | Request system settings |
| PUT | /v4/config/settings | Update system settings |
| GET | /v4/config/info/s3_tags | Request list of configured S3 tags |
| GET | /v4/config/info/product_packages | Request list of product packages |
| GET | /v4/config/info/product_packages/current | Request list of currently enabled product packages |
| GET | /v4/config/info/policies/virus_protection | Request virus protection |
| GET | /v4/config/info/policies/passwords | Request password policies |
| GET | /v4/config/info/policies/guest_users | Request guest users policies |
| GET | /v4/config/info/policies/classifications | Request classification policies |
| GET | /v4/config/info/policies/algorithms | Request algorithms |
| GET | /v4/config/info/notifications/channels | Request list of notification channels |
| GET | /v4/config/info/infrastructure | Request infrastructure properties |
| GET | /v4/config/info/general | Request general settings |
| GET | /v4/config/info/defaults | Request default values |

### auth
| Method | Path | Description |
|--------|------|-------------|
| GET | /v4/auth/reset_password/{token} | Validate information for password reset |
| PUT | /v4/auth/reset_password/{token} | Reset password |
| POST | /v4/auth/reset_password | Request password reset |
| POST | /v4/auth/recover_username | Recover username |

### roles
| Method | Path | Description |
|--------|------|-------------|
| GET | /v4/roles/{role_id}/users | Request users with specific role |
| POST | /v4/roles/{role_id}/users | Assign user(s) to the role |
| DELETE | /v4/roles/{role_id}/users | Revoke granted role from user(s) |
| GET | /v4/roles/{role_id}/groups | Request groups with specific role |
| POST | /v4/roles/{role_id}/groups | Assign group(s) to the role |
| DELETE | /v4/roles/{role_id}/groups | Revoke granted role from group(s) |
| GET | /v4/roles | Request all roles with assigned rights |

### datev
| Method | Path | Description |
|--------|------|-------------|
| GET | /v4/datev/mst/{config_id}/taxyears | Request all addable Datev MST tax years |
| POST | /v4/datev/mst/{config_id}/taxyears | Create new Datev MST tax year |
| POST | /v4/datev/mst/{config_id}/sync | Execute Datev MST sync |
| POST | /v4/datev/mst/authorization/start | Start Datev MST authorization |
| POST | /v4/datev/mst/authorization/complete | Complete Datev MST authorization |
| POST | /v4/datev/duo/{config_id}/sync | Execute Datev DUO sync |
| POST | /v4/datev/duo/authorization/start | Start Datev DUO authorization |
| POST | /v4/datev/duo/authorization/complete | Complete Datev DUO authorization |
| GET | /v4/datev | Request Datev sync configuration for room |
| GET | /v4/datev/mst | Request list of Datev MST sync configurations |
| GET | /v4/datev/mst/{config_id} | Request Datev MST sync configuration |
| DELETE | /v4/datev/mst/{config_id} | Remove Datev MST sync configuration |
| GET | /v4/datev/mst/{config_id}/files | Request information about Datev MST sync files |
| GET | /v4/datev/mst/{config_id}/files/{file_id} | Request information about a Datev MST sync file |
| GET | /v4/datev/duo | Request list of Datev DUO sync configurations |
| GET | /v4/datev/duo/{config_id} | Request Datev DUO sync configuration |
| DELETE | /v4/datev/duo/{config_id} | Remove Datev DUO sync configuration |
| GET | /v4/datev/duo/{config_id}/files | Request information about Datev DUO sync files |
| GET | /v4/datev/duo/{config_id}/files/{file_id} | Request information about a Datev DUO sync file |

### resources
| Method | Path | Description |
|--------|------|-------------|
| GET | /v4/resources/users/{user_id}/avatar/{uuid} | Request user avatar |
| GET | /v4/resources/user/notifications/scopes | Request list of subscription scopes |

### eventlog
| Method | Path | Description |
|--------|------|-------------|
| GET | /v4/eventlog/operations | Request allowed Log Operations |
| GET | /v4/eventlog/events | Request system events |
| GET | /v4/eventlog/audits/nodes | Request node assigned users with permissions |
| GET | /v4/eventlog/audits/node_info | Request nodes |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get download details?" -> GET /v4/public/shares/downloads/{access_key}/{token}
- "Get download details?" -> GET /v4/downloads/{token}
- "Get user details?" -> GET /v4/users/{user_id}
- "Update a user?" -> PUT /v4/users/{user_id}
- "Delete a user?" -> DELETE /v4/users/{user_id}
- "List all userAttributes?" -> GET /v4/users/{user_id}/userAttributes
- "Create a userAttribute?" -> POST /v4/users/{user_id}/userAttributes
- "List all upload_shares?" -> GET /v4/user/subscriptions/upload_shares
- "List all nodes?" -> GET /v4/user/subscriptions/nodes
- "List all download_shares?" -> GET /v4/user/subscriptions/download_shares
- "List all profileAttributes?" -> GET /v4/user/profileAttributes
- "Create a profileAttribute?" -> POST /v4/user/profileAttributes
- "Update a config?" -> PUT /v4/user/notifications/config/{id}
- "List all account?" -> GET /v4/user/account
- "List all customer?" -> GET /v4/user/account/customer
- "Update a upload?" -> PUT /v4/uploads/{token}
- "Delete a upload?" -> DELETE /v4/uploads/{token}
- "List all s3?" -> GET /v4/system/config/storage/s3
- "Create a s3?" -> POST /v4/system/config/storage/s3
- "List all syslog?" -> GET /v4/system/config/settings/syslog
- "List all general?" -> GET /v4/system/config/settings/general
- "List all eventlog?" -> GET /v4/system/config/settings/eventlog
- "List all defaults?" -> GET /v4/system/config/settings/defaults
- "List all auth?" -> GET /v4/system/config/settings/auth
- "List all virus_protection?" -> GET /v4/system/config/policies/virus_protection
- "List all passwords?" -> GET /v4/system/config/policies/passwords
- "List all mfa?" -> GET /v4/system/config/policies/mfa
- "Update a mfa?" -> PUT /v4/system/config/policies/mfa/{user_type}
- "List all guest_users?" -> GET /v4/system/config/policies/guest_users
- "List all classifications?" -> GET /v4/system/config/policies/classifications
- "Get client details?" -> GET /v4/system/config/oauth/clients/{client_id}
- "Update a client?" -> PUT /v4/system/config/oauth/clients/{client_id}
- "Delete a client?" -> DELETE /v4/system/config/oauth/clients/{client_id}
- "Get idp details?" -> GET /v4/system/config/auth/openid/idps/{idp_id}
- "Update a idp?" -> PUT /v4/system/config/auth/openid/idps/{idp_id}
- "Delete a idp?" -> DELETE /v4/system/config/auth/openid/idps/{idp_id}
- "Get ad details?" -> GET /v4/system/config/auth/ads/{ad_id}
- "Update a ad?" -> PUT /v4/system/config/auth/ads/{ad_id}
- "Delete a ad?" -> DELETE /v4/system/config/auth/ads/{ad_id}
- "List all uploads?" -> GET /v4/shares/uploads
- "Create a upload?" -> POST /v4/shares/uploads
- "Get upload details?" -> GET /v4/shares/uploads/{share_id}
- "Update a upload?" -> PUT /v4/shares/uploads/{share_id}
- "Delete a upload?" -> DELETE /v4/shares/uploads/{share_id}
- "List all downloads?" -> GET /v4/shares/downloads
- "Create a download?" -> POST /v4/shares/downloads
- "Get download details?" -> GET /v4/shares/downloads/{share_id}
- "Update a download?" -> PUT /v4/shares/downloads/{share_id}
- "Delete a download?" -> DELETE /v4/shares/downloads/{share_id}
- "List all settings?" -> GET /v4/settings
- "Get webhook details?" -> GET /v4/settings/webhooks/{webhook_id}
- "Update a webhook?" -> PUT /v4/settings/webhooks/{webhook_id}
- "Delete a webhook?" -> DELETE /v4/settings/webhooks/{webhook_id}
- "List all channels?" -> GET /v4/settings/notifications/channels
- "Get upload details?" -> GET /v4/public/shares/uploads/{access_key}/{upload_id}
- "Update a upload?" -> PUT /v4/public/shares/uploads/{access_key}/{upload_id}
- "Delete a upload?" -> DELETE /v4/public/shares/uploads/{access_key}/{upload_id}
- "Get webhook details?" -> GET /v4/provisioning/webhooks/{webhook_id}
- "Update a webhook?" -> PUT /v4/provisioning/webhooks/{webhook_id}
- "Delete a webhook?" -> DELETE /v4/provisioning/webhooks/{webhook_id}
- "Get customer details?" -> GET /v4/provisioning/customers/{customer_id}
- "Update a customer?" -> PUT /v4/provisioning/customers/{customer_id}
- "Delete a customer?" -> DELETE /v4/provisioning/customers/{customer_id}
- "List all customerAttributes?" -> GET /v4/provisioning/customers/{customer_id}/customerAttributes
- "Create a customerAttribute?" -> POST /v4/provisioning/customers/{customer_id}/customerAttributes
- "List all node_attributes?" -> GET /v4/nodes/{node_id}/node_attributes
- "Update a room?" -> PUT /v4/nodes/rooms/{room_id}
- "List all webhooks?" -> GET /v4/nodes/rooms/{room_id}/webhooks
- "List all users?" -> GET /v4/nodes/rooms/{room_id}/users
- "List all policies?" -> GET /v4/nodes/rooms/{room_id}/policies
- "List all groups?" -> GET /v4/nodes/rooms/{room_id}/groups
- "List all pending?" -> GET /v4/nodes/rooms/pending
- "Update a folder?" -> PUT /v4/nodes/folders/{folder_id}
- "Update a file?" -> PUT /v4/nodes/files/{file_id}
- "Get upload details?" -> GET /v4/nodes/files/uploads/{upload_id}
- "Update a upload?" -> PUT /v4/nodes/files/uploads/{upload_id}
- "Delete a upload?" -> DELETE /v4/nodes/files/uploads/{upload_id}
- "Update a comment?" -> PUT /v4/nodes/comments/{comment_id}
- "Delete a comment?" -> DELETE /v4/nodes/comments/{comment_id}
- "Get group details?" -> GET /v4/groups/{group_id}
- "Update a group?" -> PUT /v4/groups/{group_id}
- "Delete a group?" -> DELETE /v4/groups/{group_id}
- "List all settings?" -> GET /v4/config/settings
- "Get reset_password details?" -> GET /v4/auth/reset_password/{token}
- "Update a reset_password?" -> PUT /v4/auth/reset_password/{token}
- "List all users?" -> GET /v4/users
- "Create a user?" -> POST /v4/users
- "Create a emergency_code?" -> POST /v4/users/{user_id}/mfa/emergency_code
- "Delete a upload_share?" -> DELETE /v4/user/subscriptions/upload_shares/{share_id}
- "Delete a node?" -> DELETE /v4/user/subscriptions/nodes/{node_id}
- "Delete a download_share?" -> DELETE /v4/user/subscriptions/download_shares/{share_id}
- "List all totp?" -> GET /v4/user/account/mfa/totp
- "Create a totp?" -> POST /v4/user/account/mfa/totp
- "List all keypairs?" -> GET /v4/user/account/keypairs
- "Create a keypair?" -> POST /v4/user/account/keypairs
- "List all keypair?" -> GET /v4/user/account/keypair
- "Create a keypair?" -> POST /v4/user/account/keypair
- "List all avatar?" -> GET /v4/user/account/avatar
- "Create a avatar?" -> POST /v4/user/account/avatar
- "List all tags?" -> GET /v4/system/config/storage/s3/tags
- "Create a tag?" -> POST /v4/system/config/storage/s3/tags
- "Create a enforce_change?" -> POST /v4/system/config/policies/passwords/enforce_change
- "List all clients?" -> GET /v4/system/config/oauth/clients
- "Create a client?" -> POST /v4/system/config/oauth/clients
- "List all idps?" -> GET /v4/system/config/auth/openid/idps
- "Create a idp?" -> POST /v4/system/config/auth/openid/idps
- "List all ads?" -> GET /v4/system/config/auth/ads
- "Create a ad?" -> POST /v4/system/config/auth/ads
- "Create a ad?" -> POST /v4/system/config/actions/test/ad
- "Create a email?" -> POST /v4/shares/uploads/{share_id}/email
- "Create a email?" -> POST /v4/shares/downloads/{share_id}/email
- "List all webhooks?" -> GET /v4/settings/webhooks
- "Create a webhook?" -> POST /v4/settings/webhooks
- "Create a reset_lifetime?" -> POST /v4/settings/webhooks/{webhook_id}/reset_lifetime
- "List all keypairs?" -> GET /v4/settings/keypairs
- "Create a keypair?" -> POST /v4/settings/keypairs
- "List all keypair?" -> GET /v4/settings/keypair
- "Create a keypair?" -> POST /v4/settings/keypair
- "List all users?" -> GET /v4/roles/{role_id}/users
- "Create a user?" -> POST /v4/roles/{role_id}/users
- "List all groups?" -> GET /v4/roles/{role_id}/groups
- "Create a group?" -> POST /v4/roles/{role_id}/groups
- "Get upload details?" -> GET /v4/public/shares/uploads/{access_key}
- "Create a s3_url?" -> POST /v4/public/shares/uploads/{access_key}/{upload_id}/s3_urls
- "Get download details?" -> GET /v4/public/shares/downloads/{access_key}
- "List all webhooks?" -> GET /v4/provisioning/webhooks
- "Create a webhook?" -> POST /v4/provisioning/webhooks
- "Create a reset_lifetime?" -> POST /v4/provisioning/webhooks/{webhook_id}/reset_lifetime
- "List all customers?" -> GET /v4/provisioning/customers
- "Create a customer?" -> POST /v4/provisioning/customers
- "Create a move_to?" -> POST /v4/nodes/{node_id}/move_to
- "Create a favorite?" -> POST /v4/nodes/{node_id}/favorite
- "Create a copy_to?" -> POST /v4/nodes/{node_id}/copy_to
- "List all comments?" -> GET /v4/nodes/{node_id}/comments
- "Create a comment?" -> POST /v4/nodes/{node_id}/comments
- "Create a zip?" -> POST /v4/nodes/zip
- "Create a download?" -> POST /v4/nodes/zip/download
- "Create a room?" -> POST /v4/nodes/rooms
- "List all s3_tags?" -> GET /v4/nodes/rooms/{room_id}/s3_tags
- "Create a s3_tag?" -> POST /v4/nodes/rooms/{room_id}/s3_tags
- "List all keypairs?" -> GET /v4/nodes/rooms/{room_id}/keypairs
- "Create a keypair?" -> POST /v4/nodes/rooms/{room_id}/keypairs
- "List all keypair?" -> GET /v4/nodes/rooms/{room_id}/keypair
- "Create a keypair?" -> POST /v4/nodes/rooms/{room_id}/keypair
- "Create a folder?" -> POST /v4/nodes/folders
- "Create a download?" -> POST /v4/nodes/files/{file_id}/downloads
- "Create a upload?" -> POST /v4/nodes/files/uploads
- "Create a s3_url?" -> POST /v4/nodes/files/uploads/{upload_id}/s3_urls
- "Create a key?" -> POST /v4/nodes/files/keys
- "Create a generate_verdict_info?" -> POST /v4/nodes/files/generate_verdict_info
- "Create a restore?" -> POST /v4/nodes/deleted_nodes/actions/restore
- "List all groups?" -> GET /v4/groups
- "Create a group?" -> POST /v4/groups
- "List all users?" -> GET /v4/groups/{group_id}/users
- "Create a user?" -> POST /v4/groups/{group_id}/users
- "List all taxyears?" -> GET /v4/datev/mst/{config_id}/taxyears
- "Create a taxyear?" -> POST /v4/datev/mst/{config_id}/taxyears
- "Create a sync?" -> POST /v4/datev/mst/{config_id}/sync
- "Create a start?" -> POST /v4/datev/mst/authorization/start
- "Create a complete?" -> POST /v4/datev/mst/authorization/complete
- "Create a sync?" -> POST /v4/datev/duo/{config_id}/sync
- "Create a start?" -> POST /v4/datev/duo/authorization/start
- "Create a complete?" -> POST /v4/datev/duo/authorization/complete
- "Create a reset_password?" -> POST /v4/auth/reset_password
- "Create a recover_username?" -> POST /v4/auth/recover_username
- "List all rooms?" -> GET /v4/users/{user_id}/rooms
- "List all roles?" -> GET /v4/users/{user_id}/roles
- "List all last_admin_rooms?" -> GET /v4/users/{user_id}/last_admin_rooms
- "List all groups?" -> GET /v4/users/{user_id}/groups
- "List all ping?" -> GET /v4/user/ping
- "List all authorizations?" -> GET /v4/user/oauth/authorizations
- "List all approvals?" -> GET /v4/user/oauth/approvals
- "List all config?" -> GET /v4/user/notifications/config
- "List all mfa?" -> GET /v4/user/account/mfa
- "List all keypair?" -> GET /v4/user/account/customer/keypair
- "Get tag details?" -> GET /v4/system/config/storage/s3/tags/{id}
- "Delete a tag?" -> DELETE /v4/system/config/storage/s3/tags/{id}
- "List all infrastructure?" -> GET /v4/system/config/settings/infrastructure
- "Get password details?" -> GET /v4/system/config/policies/passwords/{password_type}
- "List all qr?" -> GET /v4/shares/uploads/{share_id}/qr
- "List all qr?" -> GET /v4/shares/downloads/{share_id}/qr
- "List all event_types?" -> GET /v4/settings/webhooks/event_types
- "List all roles?" -> GET /v4/roles
- "Get avatar details?" -> GET /v4/resources/users/{user_id}/avatar/{uuid}
- "List all scopes?" -> GET /v4/resources/user/notifications/scopes
- "List all time?" -> GET /v4/public/time
- "List all info?" -> GET /v4/public/system/info
- "List all openid?" -> GET /v4/public/system/info/auth/openid
- "List all ad?" -> GET /v4/public/system/info/auth/ad
- "List all version?" -> GET /v4/public/software/version
- "List all third_party_dependencies?" -> GET /v4/public/software/third_party_dependencies
- "List all event_types?" -> GET /v4/provisioning/webhooks/event_types
- "List all users?" -> GET /v4/provisioning/customers/{customer_id}/users
- "List all nodes?" -> GET /v4/nodes
- "Get node details?" -> GET /v4/nodes/{node_id}
- "Delete a node?" -> DELETE /v4/nodes/{node_id}
- "List all parents?" -> GET /v4/nodes/{node_id}/parents
- "List all deleted_nodes?" -> GET /v4/nodes/{node_id}/deleted_nodes
- "List all versions?" -> GET /v4/nodes/{node_id}/deleted_nodes/versions
- "List all search?" -> GET /v4/nodes/search
- "List all events?" -> GET /v4/nodes/rooms/{room_id}/events
- "List all missingFileKeys?" -> GET /v4/nodes/missingFileKeys
- "List all user_file_key?" -> GET /v4/nodes/files/{file_id}/user_file_key
- "List all data_space_file_key?" -> GET /v4/nodes/files/{file_id}/data_space_file_key
- "List all data_room_file_key?" -> GET /v4/nodes/files/{file_id}/data_room_file_key
- "Get version details?" -> GET /v4/nodes/files/versions/{reference_id}
- "Get deleted_node details?" -> GET /v4/nodes/deleted_nodes/{deleted_node_id}
- "List all rooms?" -> GET /v4/groups/{group_id}/rooms
- "List all roles?" -> GET /v4/groups/{group_id}/roles
- "List all last_admin_rooms?" -> GET /v4/groups/{group_id}/last_admin_rooms
- "List all operations?" -> GET /v4/eventlog/operations
- "List all events?" -> GET /v4/eventlog/events
- "List all nodes?" -> GET /v4/eventlog/audits/nodes
- "List all node_info?" -> GET /v4/eventlog/audits/node_info
- "Get zip details?" -> GET /v4/downloads/zip/{token}
- "Get avatar details?" -> GET /v4/downloads/avatar/{user_id}/{uuid}
- "List all datev?" -> GET /v4/datev
- "List all mst?" -> GET /v4/datev/mst
- "Get mst details?" -> GET /v4/datev/mst/{config_id}
- "Delete a mst?" -> DELETE /v4/datev/mst/{config_id}
- "List all files?" -> GET /v4/datev/mst/{config_id}/files
- "Get file details?" -> GET /v4/datev/mst/{config_id}/files/{file_id}
- "List all duo?" -> GET /v4/datev/duo
- "Get duo details?" -> GET /v4/datev/duo/{config_id}
- "Delete a duo?" -> DELETE /v4/datev/duo/{config_id}
- "List all files?" -> GET /v4/datev/duo/{config_id}/files
- "Get file details?" -> GET /v4/datev/duo/{config_id}/files/{file_id}
- "List all s3_tags?" -> GET /v4/config/info/s3_tags
- "List all product_packages?" -> GET /v4/config/info/product_packages
- "List all current?" -> GET /v4/config/info/product_packages/current
- "List all virus_protection?" -> GET /v4/config/info/policies/virus_protection
- "List all passwords?" -> GET /v4/config/info/policies/passwords
- "List all guest_users?" -> GET /v4/config/info/policies/guest_users
- "List all classifications?" -> GET /v4/config/info/policies/classifications
- "List all algorithms?" -> GET /v4/config/info/policies/algorithms
- "List all channels?" -> GET /v4/config/info/notifications/channels
- "List all infrastructure?" -> GET /v4/config/info/infrastructure
- "List all general?" -> GET /v4/config/info/general
- "List all defaults?" -> GET /v4/config/info/defaults
- "Delete a userAttribute?" -> DELETE /v4/users/{user_id}/userAttributes/{key}
- "Delete a profileAttribute?" -> DELETE /v4/user/profileAttributes/{key}
- "Delete a authorization?" -> DELETE /v4/user/oauth/authorizations/{client_id}
- "Delete a authorization?" -> DELETE /v4/user/oauth/authorizations/{client_id}/{authorization_id}
- "Delete a approval?" -> DELETE /v4/user/oauth/approvals/{client_id}
- "Delete a totp?" -> DELETE /v4/user/account/mfa/totp/{id}
- "Delete a customerAttribute?" -> DELETE /v4/provisioning/customers/{customer_id}/customerAttributes/{key}
- "Delete a node_attribute?" -> DELETE /v4/nodes/{node_id}/node_attributes/{key}
- "Delete a malicious_file?" -> DELETE /v4/nodes/malicious_files/{malicious_file_id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
