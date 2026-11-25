---
name: filescom-api
description: "Files.com API skill. Use when working with Files.com for sessions, action_logs, action_notification_exports. Covers 324 endpoints."
version: 1.0.0
generator: lapsh
---

# Files.com API
API version: 0.0.1

## Auth
ApiKey X-FilesAPI-Key in header

## Base URL
https://app.files.com/api/rest/v1

## Setup
1. Set your API key in the appropriate header
2. GET /action_logs -- verify access
3. POST /sessions -- create first sessions

## Endpoints

324 endpoints across 99 groups. See references/api-spec.lap for full details.

### sessions
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /sessions | Delete user session (log out) |
| POST | /sessions | Create user session (log in) |

### action_logs
| Method | Path | Description |
|--------|------|-------------|
| GET | /action_logs | List Action Logs |

### action_notification_exports
| Method | Path | Description |
|--------|------|-------------|
| POST | /action_notification_exports | Create Action Notification Export |
| GET | /action_notification_exports/{id} | Show Action Notification Export |

### action_notification_export_results
| Method | Path | Description |
|--------|------|-------------|
| GET | /action_notification_export_results | List Action Notification Export Results |

### api_key
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /api_key | Delete current API key.  (Requires current API connection to be using an API key.) |
| PATCH | /api_key | Update current API key.  (Requires current API connection to be using an API key.) |
| GET | /api_key | Show information about current API key.  (Requires current API connection to be using an API key.) |

### api_keys
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /api_keys/{id} | Delete API Key |
| PATCH | /api_keys/{id} | Update API Key |
| GET | /api_keys/{id} | Show API Key |
| POST | /api_keys | Create API Key |
| GET | /api_keys | List API Keys |

### site
| Method | Path | Description |
|--------|------|-------------|
| GET | /site/usage | Get the most recent usage snapshot (usage data for billing purposes) for a Site. |
| PATCH | /site | Update Site Settings |
| GET | /site | Show Site Settings |
| GET | /site/ip_addresses | List IP Addresses associated with the current site |
| GET | /site/dns_records | Show Site DNS Configuration |
| POST | /site/test-webhook | Test Webhook |
| POST | /site/api_keys | Create API Key |
| GET | /site/api_keys | List API Keys |

### user
| Method | Path | Description |
|--------|------|-------------|
| PATCH | /user | Update User |
| POST | /user/public_keys | Create Public Key |
| GET | /user/public_keys | List Public Keys |
| GET | /user/groups | List Group Users |
| POST | /user/api_keys | Create API Key |
| GET | /user/api_keys | List API Keys |

### users
| Method | Path | Description |
|--------|------|-------------|
| POST | /users/{id}/unlock | Unlock user who has been locked out due to failed logins. |
| POST | /users/{id}/resend_welcome_email | Resend user welcome email |
| POST | /users/{id}/2fa/reset | Trigger 2FA Reset process for user who has lost access to their existing 2FA methods. |
| DELETE | /users/{id} | Delete User |
| PATCH | /users/{id} | Update User |
| GET | /users/{id} | Show User |
| POST | /users | Create User |
| GET | /users | List Users |
| GET | /users/{user_id}/sftp_client_uses | List User SFTP Client Uses |
| GET | /users/{user_id}/cipher_uses | List User Cipher Uses |
| POST | /users/{user_id}/public_keys | Create Public Key |
| GET | /users/{user_id}/public_keys | List Public Keys |
| GET | /users/{user_id}/permissions | List Permissions |
| GET | /users/{user_id}/groups | List Group Users |
| POST | /users/{user_id}/api_keys | Create API Key |
| GET | /users/{user_id}/api_keys | List API Keys |

### api_request_logs
| Method | Path | Description |
|--------|------|-------------|
| GET | /api_request_logs | List API Request Logs |

### apps
| Method | Path | Description |
|--------|------|-------------|
| GET | /apps | List Apps |

### as2_incoming_messages
| Method | Path | Description |
|--------|------|-------------|
| GET | /as2_incoming_messages | List AS2 Incoming Messages |

### as2_outgoing_messages
| Method | Path | Description |
|--------|------|-------------|
| GET | /as2_outgoing_messages | List AS2 Outgoing Messages |

### as2_partners
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /as2_partners/{id} | Delete AS2 Partner |
| PATCH | /as2_partners/{id} | Update AS2 Partner |
| GET | /as2_partners/{id} | Show AS2 Partner |
| POST | /as2_partners | Create AS2 Partner |
| GET | /as2_partners | List AS2 Partners |

### as2_stations
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /as2_stations/{id} | Delete AS2 Station |
| PATCH | /as2_stations/{id} | Update AS2 Station |
| GET | /as2_stations/{id} | Show AS2 Station |
| POST | /as2_stations | Create AS2 Station |
| GET | /as2_stations | List AS2 Stations |

### automations
| Method | Path | Description |
|--------|------|-------------|
| POST | /automations/{id}/manual_run | Manually Run Automation |
| DELETE | /automations/{id} | Delete Automation |
| PATCH | /automations/{id} | Update Automation |
| GET | /automations/{id} | Show Automation |
| POST | /automations | Create Automation |
| GET | /automations | List Automations |

### automation_logs
| Method | Path | Description |
|--------|------|-------------|
| GET | /automation_logs | List Automation Logs |

### automation_runs
| Method | Path | Description |
|--------|------|-------------|
| GET | /automation_runs/{id} | Show Automation Run |
| GET | /automation_runs | List Automation Runs |

### bandwidth_snapshots
| Method | Path | Description |
|--------|------|-------------|
| GET | /bandwidth_snapshots | List Bandwidth Snapshots |

### behaviors
| Method | Path | Description |
|--------|------|-------------|
| POST | /behaviors/webhook/test | Test Webhook |
| DELETE | /behaviors/{id} | Delete Behavior |
| PATCH | /behaviors/{id} | Update Behavior |
| GET | /behaviors/{id} | Show Behavior |
| POST | /behaviors | Create Behavior |
| GET | /behaviors | List Behaviors |
| GET | /behaviors/folders/{path} | List Behaviors by Path |

### bundle_actions
| Method | Path | Description |
|--------|------|-------------|
| GET | /bundle_actions | List Bundle Actions |

### bundle_downloads
| Method | Path | Description |
|--------|------|-------------|
| GET | /bundle_downloads | List Share Link Downloads |

### bundle_notifications
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /bundle_notifications/{id} | Delete Share Link Notification |
| PATCH | /bundle_notifications/{id} | Update Share Link Notification |
| GET | /bundle_notifications/{id} | Show Share Link Notification |
| POST | /bundle_notifications | Create Share Link Notification |
| GET | /bundle_notifications | List Share Link Notifications |

### bundle_recipients
| Method | Path | Description |
|--------|------|-------------|
| POST | /bundle_recipients | Create Share Link Recipient |
| GET | /bundle_recipients | List Share Link Recipients |

### bundle_registrations
| Method | Path | Description |
|--------|------|-------------|
| GET | /bundle_registrations | List Share Link Registrations |

### bundles
| Method | Path | Description |
|--------|------|-------------|
| GET | /bundles/{id} | Show Share Link |
| PATCH | /bundles/{id} | Update Share Link |
| DELETE | /bundles/{id} | Delete Share Link |
| GET | /bundles | List Share Links |
| POST | /bundles | Create Share Link |
| POST | /bundles/{id}/share | Send email(s) with a link to bundle |

### child_site_management_policies
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /child_site_management_policies/{id} | Delete Child Site Management Policy |
| PATCH | /child_site_management_policies/{id} | Update Child Site Management Policy |
| GET | /child_site_management_policies/{id} | Show Child Site Management Policy |
| POST | /child_site_management_policies | Create Child Site Management Policy |
| GET | /child_site_management_policies | List Child Site Management Policies |

### clickwraps
| Method | Path | Description |
|--------|------|-------------|
| GET | /clickwraps | List Clickwraps |
| POST | /clickwraps | Create Clickwrap |
| DELETE | /clickwraps/{id} | Delete Clickwrap |
| PATCH | /clickwraps/{id} | Update Clickwrap |
| GET | /clickwraps/{id} | Show Clickwrap |

### dns_records
| Method | Path | Description |
|--------|------|-------------|
| GET | /dns_records | Show Site DNS Configuration |

### email_incoming_messages
| Method | Path | Description |
|--------|------|-------------|
| GET | /email_incoming_messages | List Email Incoming Messages |

### email_logs
| Method | Path | Description |
|--------|------|-------------|
| GET | /email_logs | List Email Logs |

### exavault_api_request_logs
| Method | Path | Description |
|--------|------|-------------|
| GET | /exavault_api_request_logs | List Exavault API Request Logs |

### external_events
| Method | Path | Description |
|--------|------|-------------|
| POST | /external_events | Create External Event |
| GET | /external_events | List External Events |
| GET | /external_events/{id} | Show External Event |

### files
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /files/{path} | Delete File/Folder |
| PATCH | /files/{path} | Update File/Folder Metadata |
| POST | /files/{path} | Upload File |
| GET | /files/{path} | Download File |

### file_actions
| Method | Path | Description |
|--------|------|-------------|
| GET | /file_actions/metadata/{path} | Find File/Folder by Path |
| POST | /file_actions/copy/{path} | Copy File/Folder |
| POST | /file_actions/move/{path} | Move File/Folder |
| POST | /file_actions/unzip | Extract a ZIP file to a destination folder. |
| GET | /file_actions/zip_list/{path} | List the contents of a ZIP file. |
| POST | /file_actions/zip | Create a ZIP from one or more paths and save it to a destination path. |
| POST | /file_actions/begin_upload/{path} | Begin File Upload |

### file_comments
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /file_comments/{id} | Delete File Comment |
| PATCH | /file_comments/{id} | Update File Comment |
| POST | /file_comments | Create File Comment |
| GET | /file_comments/files/{path} | List File Comments by Path |

### file_comment_reactions
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /file_comment_reactions/{id} | Delete File Comment Reaction |
| POST | /file_comment_reactions | Create File Comment Reaction |

### file_migrations
| Method | Path | Description |
|--------|------|-------------|
| GET | /file_migrations/{id} | Show File Migration |

### file_migration_logs
| Method | Path | Description |
|--------|------|-------------|
| GET | /file_migration_logs | List File Migration Logs |

### folders
| Method | Path | Description |
|--------|------|-------------|
| POST | /folders/{path} | Create Folder |
| GET | /folders/{path} | List Folders by Path |

### form_field_sets
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /form_field_sets/{id} | Delete Form Field Set |
| PATCH | /form_field_sets/{id} | Update Form Field Set |
| GET | /form_field_sets/{id} | Show Form Field Set |
| POST | /form_field_sets | Create Form Field Set |
| GET | /form_field_sets | List Form Field Sets |

### ftp_action_logs
| Method | Path | Description |
|--------|------|-------------|
| GET | /ftp_action_logs | List FTP Action Logs |

### groups
| Method | Path | Description |
|--------|------|-------------|
| POST | /groups/{group_id}/users | Create User |
| GET | /groups/{group_id}/users | List Group Users |
| GET | /groups/{group_id}/permissions | List Permissions |
| DELETE | /groups/{group_id}/memberships/{user_id} | Delete Group User |
| PATCH | /groups/{group_id}/memberships/{user_id} | Update Group User |
| DELETE | /groups/{id} | Delete Group |
| PATCH | /groups/{id} | Update Group |
| GET | /groups/{id} | Show Group |
| POST | /groups | Create Group |
| GET | /groups | List Groups |

### group_users
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /group_users/{id} | Delete Group User |
| PATCH | /group_users/{id} | Update Group User |
| GET | /group_users | List Group Users |
| POST | /group_users | Create Group User |

### gpg_keys
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /gpg_keys/{id} | Delete GPG Key |
| PATCH | /gpg_keys/{id} | Update GPG Key |
| GET | /gpg_keys/{id} | Show GPG Key |
| POST | /gpg_keys | Create GPG Key |
| GET | /gpg_keys | List GPG Keys |

### history
| Method | Path | Description |
|--------|------|-------------|
| GET | /history/files/{path} | List history for specific file. |
| GET | /history/folders/{path} | List history for specific folder. |
| GET | /history/users/{user_id} | List history for specific user. |
| GET | /history/login | List site login history. |
| GET | /history | List site full action history. |

### history_exports
| Method | Path | Description |
|--------|------|-------------|
| POST | /history_exports | Create History Export |
| GET | /history_exports/{id} | Show History Export |

### history_export_results
| Method | Path | Description |
|--------|------|-------------|
| GET | /history_export_results | List History Export Results |

### holiday_regions
| Method | Path | Description |
|--------|------|-------------|
| GET | /holiday_regions/supported | List all possible holiday regions |

### inbox_recipients
| Method | Path | Description |
|--------|------|-------------|
| POST | /inbox_recipients | Create Inbox Recipient |
| GET | /inbox_recipients | List Inbox Recipients |

### inbox_registrations
| Method | Path | Description |
|--------|------|-------------|
| GET | /inbox_registrations | List Inbox Registrations |

### inbox_uploads
| Method | Path | Description |
|--------|------|-------------|
| GET | /inbox_uploads | List Inbox Uploads |

### inbound_s3_logs
| Method | Path | Description |
|--------|------|-------------|
| GET | /inbound_s3_logs | List Inbound S3 Logs |

### invoices
| Method | Path | Description |
|--------|------|-------------|
| GET | /invoices/{id} | Show Invoice |
| GET | /invoices | List Invoices |

### ip_addresses
| Method | Path | Description |
|--------|------|-------------|
| GET | /ip_addresses/smartfile-reserved | List all possible public SmartFile IP addresses |
| GET | /ip_addresses/exavault-reserved | List all possible public ExaVault IP addresses |
| GET | /ip_addresses/reserved | List all possible public IP addresses |
| GET | /ip_addresses | List IP Addresses associated with the current site |

### key_lifecycle_rules
| Method | Path | Description |
|--------|------|-------------|
| PATCH | /key_lifecycle_rules/{id} | Update Key Lifecycle Rule |
| DELETE | /key_lifecycle_rules/{id} | Delete Key Lifecycle Rule |
| GET | /key_lifecycle_rules/{id} | Show Key Lifecycle Rule |
| POST | /key_lifecycle_rules | Create Key Lifecycle Rule |
| GET | /key_lifecycle_rules | List Key Lifecycle Rules |

### locks
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /locks/{path} | Delete Lock |
| POST | /locks/{path} | Create Lock |
| GET | /locks/{path} | List Locks by Path |

### messages
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /messages/{id} | Delete Message |
| PATCH | /messages/{id} | Update Message |
| GET | /messages/{id} | Show Message |
| POST | /messages | Create Message |
| GET | /messages | List Messages |

### message_comments
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /message_comments/{id} | Delete Message Comment |
| PATCH | /message_comments/{id} | Update Message Comment |
| GET | /message_comments/{id} | Show Message Comment |
| POST | /message_comments | Create Message Comment |
| GET | /message_comments | List Message Comments |

### message_comment_reactions
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /message_comment_reactions/{id} | Delete Message Comment Reaction |
| GET | /message_comment_reactions/{id} | Show Message Comment Reaction |
| POST | /message_comment_reactions | Create Message Comment Reaction |
| GET | /message_comment_reactions | List Message Comment Reactions |

### message_reactions
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /message_reactions/{id} | Delete Message Reaction |
| GET | /message_reactions/{id} | Show Message Reaction |
| POST | /message_reactions | Create Message Reaction |
| GET | /message_reactions | List Message Reactions |

### notifications
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /notifications/{id} | Delete Notification |
| PATCH | /notifications/{id} | Update Notification |
| GET | /notifications/{id} | Show Notification |
| POST | /notifications | Create Notification |
| GET | /notifications | List Notifications |

### outbound_connection_logs
| Method | Path | Description |
|--------|------|-------------|
| GET | /outbound_connection_logs | List Outbound Connection Logs |

### partners
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /partners/{id} | Delete Partner |
| PATCH | /partners/{id} | Update Partner |
| GET | /partners/{id} | Show Partner |
| GET | /partners | List Partners |
| POST | /partners | Create Partner |

### partner_sites
| Method | Path | Description |
|--------|------|-------------|
| GET | /partner_sites/linked_partner_sites | Get Partner Sites linked to the current Site |
| GET | /partner_sites | List Partner Sites |

### partner_site_requests
| Method | Path | Description |
|--------|------|-------------|
| POST | /partner_site_requests/{id}/reject | Reject partner site request |
| POST | /partner_site_requests/{id}/approve | Approve partner site request |
| GET | /partner_site_requests/find_by_pairing_key | Find partner site request by pairing key |
| DELETE | /partner_site_requests/{id} | Delete Partner Site Request |
| POST | /partner_site_requests | Create Partner Site Request |
| GET | /partner_site_requests | List Partner Site Requests |

### payments
| Method | Path | Description |
|--------|------|-------------|
| GET | /payments/{id} | Show Payment |
| GET | /payments | List Payments |

### permissions
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /permissions/{id} | Delete Permission |
| POST | /permissions | Create Permission |
| GET | /permissions | List Permissions |

### priorities
| Method | Path | Description |
|--------|------|-------------|
| GET | /priorities | List Priorities |

### projects
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /projects/{id} | Delete Project |
| PATCH | /projects/{id} | Update Project |
| GET | /projects/{id} | Show Project |
| POST | /projects | Create Project |
| GET | /projects | List Projects |

### public_hosting_request_logs
| Method | Path | Description |
|--------|------|-------------|
| GET | /public_hosting_request_logs | List Public Hosting Request Logs |

### public_keys
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /public_keys/{id} | Delete Public Key |
| PATCH | /public_keys/{id} | Update Public Key |
| GET | /public_keys/{id} | Show Public Key |
| POST | /public_keys | Create Public Key |
| GET | /public_keys | List Public Keys |

### restores
| Method | Path | Description |
|--------|------|-------------|
| POST | /restores | Create Restore |
| GET | /restores | List Restores |

### remote_bandwidth_snapshots
| Method | Path | Description |
|--------|------|-------------|
| GET | /remote_bandwidth_snapshots | List Remote Bandwidth Snapshots |

### remote_mount_backends
| Method | Path | Description |
|--------|------|-------------|
| POST | /remote_mount_backends/{id}/reset_status | Reset backend status to healthy. |
| DELETE | /remote_mount_backends/{id} | Delete Remote Mount Backend |
| PATCH | /remote_mount_backends/{id} | Update Remote Mount Backend |
| GET | /remote_mount_backends/{id} | Show Remote Mount Backend |
| GET | /remote_mount_backends | List Remote Mount Backends |
| POST | /remote_mount_backends | Create Remote Mount Backend |

### remote_servers
| Method | Path | Description |
|--------|------|-------------|
| POST | /remote_servers/{id}/agent_push_update | Push update to Files Agent |
| POST | /remote_servers/{id}/configuration_file | Post local changes, check in, and download configuration file (used by some Remote Server integrations, such as the Files.com Agent) |
| GET | /remote_servers/{id}/configuration_file | Download configuration file (required for some Remote Server integrations, such as the Files.com Agent) |
| GET | /remote_servers | List Remote Servers |
| POST | /remote_servers | Create Remote Server |
| DELETE | /remote_servers/{id} | Delete Remote Server |
| PATCH | /remote_servers/{id} | Update Remote Server |
| GET | /remote_servers/{id} | Show Remote Server |

### remote_server_credentials
| Method | Path | Description |
|--------|------|-------------|
| GET | /remote_server_credentials | List Remote Server Credentials |
| POST | /remote_server_credentials | Create Remote Server Credential |
| DELETE | /remote_server_credentials/{id} | Delete Remote Server Credential |
| PATCH | /remote_server_credentials/{id} | Update Remote Server Credential |
| GET | /remote_server_credentials/{id} | Show Remote Server Credential |

### requests
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /requests/{id} | Delete Request |
| POST | /requests | Create Request |
| GET | /requests | List Requests |
| GET | /requests/folders/{path} | List Requests |

### scim_logs
| Method | Path | Description |
|--------|------|-------------|
| GET | /scim_logs/{id} | Show Scim Log |
| GET | /scim_logs | List Scim Logs |

### settings_changes
| Method | Path | Description |
|--------|------|-------------|
| GET | /settings_changes | List Settings Changes |

### sftp_action_logs
| Method | Path | Description |
|--------|------|-------------|
| GET | /sftp_action_logs | List SFTP Action Logs |

### sftp_host_keys
| Method | Path | Description |
|--------|------|-------------|
| GET | /sftp_host_keys | List SFTP Host Keys |
| POST | /sftp_host_keys | Create SFTP Host Key |
| DELETE | /sftp_host_keys/{id} | Delete SFTP Host Key |
| PATCH | /sftp_host_keys/{id} | Update SFTP Host Key |
| GET | /sftp_host_keys/{id} | Show SFTP Host Key |

### share_groups
| Method | Path | Description |
|--------|------|-------------|
| GET | /share_groups | List Share Groups |
| POST | /share_groups | Create Share Group |
| DELETE | /share_groups/{id} | Delete Share Group |
| GET | /share_groups/{id} | Show Share Group |
| PATCH | /share_groups/{id} | Update Share Group |

### siem_http_destinations
| Method | Path | Description |
|--------|------|-------------|
| GET | /siem_http_destinations | List SIEM HTTP Destinations |
| POST | /siem_http_destinations | Create SIEM HTTP Destination |
| DELETE | /siem_http_destinations/{id} | Delete SIEM HTTP Destination |
| GET | /siem_http_destinations/{id} | Show SIEM HTTP Destination |
| PATCH | /siem_http_destinations/{id} | Update SIEM HTTP Destination |
| POST | /siem_http_destinations/send_test_entry | send_test_entry SIEM HTTP Destination |

### snapshots
| Method | Path | Description |
|--------|------|-------------|
| POST | /snapshots/{id}/finalize | Finalize Snapshot |
| DELETE | /snapshots/{id} | Delete Snapshot |
| PATCH | /snapshots/{id} | Update Snapshot |
| GET | /snapshots/{id} | Show Snapshot |
| POST | /snapshots | Create Snapshot |
| GET | /snapshots | List Snapshots |

### sso_strategies
| Method | Path | Description |
|--------|------|-------------|
| POST | /sso_strategies/{id}/sync | Synchronize provisioning data with the SSO remote server. |
| GET | /sso_strategies/{id} | Show SSO Strategy |
| GET | /sso_strategies | List SSO Strategies |

### styles
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /styles/{path} | Delete Style |
| PATCH | /styles/{path} | Update Style |
| GET | /styles/{path} | Show Style |

### syncs
| Method | Path | Description |
|--------|------|-------------|
| POST | /syncs/{id}/dry_run | Dry Run Sync |
| POST | /syncs/{id}/manual_run | Manually Run Sync |
| DELETE | /syncs/{id} | Delete Sync |
| PATCH | /syncs/{id} | Update Sync |
| GET | /syncs/{id} | Show Sync |
| GET | /syncs | List Syncs |
| POST | /syncs | Create Sync |

### sync_logs
| Method | Path | Description |
|--------|------|-------------|
| GET | /sync_logs | List Sync Logs |

### sync_runs
| Method | Path | Description |
|--------|------|-------------|
| GET | /sync_runs/{id} | Show Sync Run |
| GET | /sync_runs | List Sync Runs |

### usage_snapshots
| Method | Path | Description |
|--------|------|-------------|
| GET | /usage_snapshots | List Usage Snapshots |

### usage_daily_snapshots
| Method | Path | Description |
|--------|------|-------------|
| GET | /usage_daily_snapshots | List Usage Daily Snapshots |

### user_cipher_uses
| Method | Path | Description |
|--------|------|-------------|
| GET | /user_cipher_uses | List User Cipher Uses |

### user_lifecycle_rules
| Method | Path | Description |
|--------|------|-------------|
| PATCH | /user_lifecycle_rules/{id} | Update User Lifecycle Rule |
| DELETE | /user_lifecycle_rules/{id} | Delete User Lifecycle Rule |
| GET | /user_lifecycle_rules/{id} | Show User Lifecycle Rule |
| POST | /user_lifecycle_rules | Create User Lifecycle Rule |
| GET | /user_lifecycle_rules | List User Lifecycle Rules |

### user_requests
| Method | Path | Description |
|--------|------|-------------|
| GET | /user_requests | List User Requests |
| POST | /user_requests | Create User Request |
| DELETE | /user_requests/{id} | Delete User Request |
| GET | /user_requests/{id} | Show User Request |

### user_sftp_client_uses
| Method | Path | Description |
|--------|------|-------------|
| GET | /user_sftp_client_uses | List User SFTP Client Uses |

### web_dav_action_logs
| Method | Path | Description |
|--------|------|-------------|
| GET | /web_dav_action_logs | List WebDAV Action Logs |

### webhook_tests
| Method | Path | Description |
|--------|------|-------------|
| POST | /webhook_tests | Create Webhook Test |

### workspaces
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /workspaces/{id} | Delete Workspace |
| PATCH | /workspaces/{id} | Update Workspace |
| GET | /workspaces/{id} | Show Workspace |
| POST | /workspaces | Create Workspace |
| GET | /workspaces | List Workspaces |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a session?" -> POST /sessions
- "List all action_logs?" -> GET /action_logs
- "Create a action_notification_export?" -> POST /action_notification_exports
- "Get action_notification_export details?" -> GET /action_notification_exports/{id}
- "List all action_notification_export_results?" -> GET /action_notification_export_results
- "List all api_key?" -> GET /api_key
- "Delete a api_key?" -> DELETE /api_keys/{id}
- "Partially update a api_key?" -> PATCH /api_keys/{id}
- "Get api_key details?" -> GET /api_keys/{id}
- "Create a api_key?" -> POST /api_keys
- "List all api_keys?" -> GET /api_keys
- "List all usage?" -> GET /site/usage
- "List all site?" -> GET /site
- "List all ip_addresses?" -> GET /site/ip_addresses
- "List all dns_records?" -> GET /site/dns_records
- "Create a test-webhook?" -> POST /site/test-webhook
- "Create a api_key?" -> POST /site/api_keys
- "List all api_keys?" -> GET /site/api_keys
- "Create a public_key?" -> POST /user/public_keys
- "List all public_keys?" -> GET /user/public_keys
- "List all groups?" -> GET /user/groups
- "Create a api_key?" -> POST /user/api_keys
- "List all api_keys?" -> GET /user/api_keys
- "Create a unlock?" -> POST /users/{id}/unlock
- "Create a resend_welcome_email?" -> POST /users/{id}/resend_welcome_email
- "Create a reset?" -> POST /users/{id}/2fa/reset
- "Delete a user?" -> DELETE /users/{id}
- "Partially update a user?" -> PATCH /users/{id}
- "Get user details?" -> GET /users/{id}
- "Create a user?" -> POST /users
- "Search users?" -> GET /users
- "List all sftp_client_uses?" -> GET /users/{user_id}/sftp_client_uses
- "List all cipher_uses?" -> GET /users/{user_id}/cipher_uses
- "Create a public_key?" -> POST /users/{user_id}/public_keys
- "List all public_keys?" -> GET /users/{user_id}/public_keys
- "List all permissions?" -> GET /users/{user_id}/permissions
- "List all groups?" -> GET /users/{user_id}/groups
- "Create a api_key?" -> POST /users/{user_id}/api_keys
- "List all api_keys?" -> GET /users/{user_id}/api_keys
- "List all api_request_logs?" -> GET /api_request_logs
- "List all apps?" -> GET /apps
- "List all as2_incoming_messages?" -> GET /as2_incoming_messages
- "List all as2_outgoing_messages?" -> GET /as2_outgoing_messages
- "Delete a as2_partner?" -> DELETE /as2_partners/{id}
- "Partially update a as2_partner?" -> PATCH /as2_partners/{id}
- "Get as2_partner details?" -> GET /as2_partners/{id}
- "Create a as2_partner?" -> POST /as2_partners
- "List all as2_partners?" -> GET /as2_partners
- "Delete a as2_station?" -> DELETE /as2_stations/{id}
- "Partially update a as2_station?" -> PATCH /as2_stations/{id}
- "Get as2_station details?" -> GET /as2_stations/{id}
- "Create a as2_station?" -> POST /as2_stations
- "List all as2_stations?" -> GET /as2_stations
- "Create a manual_run?" -> POST /automations/{id}/manual_run
- "Delete a automation?" -> DELETE /automations/{id}
- "Partially update a automation?" -> PATCH /automations/{id}
- "Get automation details?" -> GET /automations/{id}
- "Create a automation?" -> POST /automations
- "List all automations?" -> GET /automations
- "List all automation_logs?" -> GET /automation_logs
- "Get automation_run details?" -> GET /automation_runs/{id}
- "List all automation_runs?" -> GET /automation_runs
- "List all bandwidth_snapshots?" -> GET /bandwidth_snapshots
- "Create a test?" -> POST /behaviors/webhook/test
- "Delete a behavior?" -> DELETE /behaviors/{id}
- "Partially update a behavior?" -> PATCH /behaviors/{id}
- "Get behavior details?" -> GET /behaviors/{id}
- "Create a behavior?" -> POST /behaviors
- "List all behaviors?" -> GET /behaviors
- "Get folder details?" -> GET /behaviors/folders/{path}
- "List all bundle_actions?" -> GET /bundle_actions
- "List all bundle_downloads?" -> GET /bundle_downloads
- "Delete a bundle_notification?" -> DELETE /bundle_notifications/{id}
- "Partially update a bundle_notification?" -> PATCH /bundle_notifications/{id}
- "Get bundle_notification details?" -> GET /bundle_notifications/{id}
- "Create a bundle_notification?" -> POST /bundle_notifications
- "List all bundle_notifications?" -> GET /bundle_notifications
- "Create a bundle_recipient?" -> POST /bundle_recipients
- "List all bundle_recipients?" -> GET /bundle_recipients
- "List all bundle_registrations?" -> GET /bundle_registrations
- "Get bundle details?" -> GET /bundles/{id}
- "Partially update a bundle?" -> PATCH /bundles/{id}
- "Delete a bundle?" -> DELETE /bundles/{id}
- "List all bundles?" -> GET /bundles
- "Create a bundle?" -> POST /bundles
- "Create a share?" -> POST /bundles/{id}/share
- "Delete a child_site_management_policy?" -> DELETE /child_site_management_policies/{id}
- "Partially update a child_site_management_policy?" -> PATCH /child_site_management_policies/{id}
- "Get child_site_management_policy details?" -> GET /child_site_management_policies/{id}
- "Create a child_site_management_policy?" -> POST /child_site_management_policies
- "List all child_site_management_policies?" -> GET /child_site_management_policies
- "List all clickwraps?" -> GET /clickwraps
- "Create a clickwrap?" -> POST /clickwraps
- "Delete a clickwrap?" -> DELETE /clickwraps/{id}
- "Partially update a clickwrap?" -> PATCH /clickwraps/{id}
- "Get clickwrap details?" -> GET /clickwraps/{id}
- "List all dns_records?" -> GET /dns_records
- "List all email_incoming_messages?" -> GET /email_incoming_messages
- "List all email_logs?" -> GET /email_logs
- "List all exavault_api_request_logs?" -> GET /exavault_api_request_logs
- "Create a external_event?" -> POST /external_events
- "List all external_events?" -> GET /external_events
- "Get external_event details?" -> GET /external_events/{id}
- "Delete a file?" -> DELETE /files/{path}
- "Partially update a file?" -> PATCH /files/{path}
- "Get file details?" -> GET /files/{path}
- "Get metadata details?" -> GET /file_actions/metadata/{path}
- "Create a unzip?" -> POST /file_actions/unzip
- "Get zip_list details?" -> GET /file_actions/zip_list/{path}
- "Create a zip?" -> POST /file_actions/zip
- "Delete a file_comment?" -> DELETE /file_comments/{id}
- "Partially update a file_comment?" -> PATCH /file_comments/{id}
- "Create a file_comment?" -> POST /file_comments
- "Get file details?" -> GET /file_comments/files/{path}
- "Delete a file_comment_reaction?" -> DELETE /file_comment_reactions/{id}
- "Create a file_comment_reaction?" -> POST /file_comment_reactions
- "Get file_migration details?" -> GET /file_migrations/{id}
- "List all file_migration_logs?" -> GET /file_migration_logs
- "Search folders?" -> GET /folders/{path}
- "Delete a form_field_set?" -> DELETE /form_field_sets/{id}
- "Partially update a form_field_set?" -> PATCH /form_field_sets/{id}
- "Get form_field_set details?" -> GET /form_field_sets/{id}
- "Create a form_field_set?" -> POST /form_field_sets
- "List all form_field_sets?" -> GET /form_field_sets
- "List all ftp_action_logs?" -> GET /ftp_action_logs
- "Create a user?" -> POST /groups/{group_id}/users
- "List all users?" -> GET /groups/{group_id}/users
- "List all permissions?" -> GET /groups/{group_id}/permissions
- "Delete a membership?" -> DELETE /groups/{group_id}/memberships/{user_id}
- "Partially update a membership?" -> PATCH /groups/{group_id}/memberships/{user_id}
- "Delete a group?" -> DELETE /groups/{id}
- "Partially update a group?" -> PATCH /groups/{id}
- "Get group details?" -> GET /groups/{id}
- "Create a group?" -> POST /groups
- "List all groups?" -> GET /groups
- "Delete a group_user?" -> DELETE /group_users/{id}
- "Partially update a group_user?" -> PATCH /group_users/{id}
- "List all group_users?" -> GET /group_users
- "Create a group_user?" -> POST /group_users
- "Delete a gpg_key?" -> DELETE /gpg_keys/{id}
- "Partially update a gpg_key?" -> PATCH /gpg_keys/{id}
- "Get gpg_key details?" -> GET /gpg_keys/{id}
- "Create a gpg_key?" -> POST /gpg_keys
- "List all gpg_keys?" -> GET /gpg_keys
- "Get file details?" -> GET /history/files/{path}
- "Get folder details?" -> GET /history/folders/{path}
- "Get user details?" -> GET /history/users/{user_id}
- "List all login?" -> GET /history/login
- "List all history?" -> GET /history
- "Create a history_export?" -> POST /history_exports
- "Get history_export details?" -> GET /history_exports/{id}
- "List all history_export_results?" -> GET /history_export_results
- "List all supported?" -> GET /holiday_regions/supported
- "Create a inbox_recipient?" -> POST /inbox_recipients
- "List all inbox_recipients?" -> GET /inbox_recipients
- "List all inbox_registrations?" -> GET /inbox_registrations
- "List all inbox_uploads?" -> GET /inbox_uploads
- "List all inbound_s3_logs?" -> GET /inbound_s3_logs
- "Get invoice details?" -> GET /invoices/{id}
- "List all invoices?" -> GET /invoices
- "List all smartfile-reserved?" -> GET /ip_addresses/smartfile-reserved
- "List all exavault-reserved?" -> GET /ip_addresses/exavault-reserved
- "List all reserved?" -> GET /ip_addresses/reserved
- "List all ip_addresses?" -> GET /ip_addresses
- "Partially update a key_lifecycle_rule?" -> PATCH /key_lifecycle_rules/{id}
- "Delete a key_lifecycle_rule?" -> DELETE /key_lifecycle_rules/{id}
- "Get key_lifecycle_rule details?" -> GET /key_lifecycle_rules/{id}
- "Create a key_lifecycle_rule?" -> POST /key_lifecycle_rules
- "List all key_lifecycle_rules?" -> GET /key_lifecycle_rules
- "Delete a lock?" -> DELETE /locks/{path}
- "Get lock details?" -> GET /locks/{path}
- "Delete a message?" -> DELETE /messages/{id}
- "Partially update a message?" -> PATCH /messages/{id}
- "Get message details?" -> GET /messages/{id}
- "Create a message?" -> POST /messages
- "List all messages?" -> GET /messages
- "Delete a message_comment?" -> DELETE /message_comments/{id}
- "Partially update a message_comment?" -> PATCH /message_comments/{id}
- "Get message_comment details?" -> GET /message_comments/{id}
- "Create a message_comment?" -> POST /message_comments
- "List all message_comments?" -> GET /message_comments
- "Delete a message_comment_reaction?" -> DELETE /message_comment_reactions/{id}
- "Get message_comment_reaction details?" -> GET /message_comment_reactions/{id}
- "Create a message_comment_reaction?" -> POST /message_comment_reactions
- "List all message_comment_reactions?" -> GET /message_comment_reactions
- "Delete a message_reaction?" -> DELETE /message_reactions/{id}
- "Get message_reaction details?" -> GET /message_reactions/{id}
- "Create a message_reaction?" -> POST /message_reactions
- "List all message_reactions?" -> GET /message_reactions
- "Delete a notification?" -> DELETE /notifications/{id}
- "Partially update a notification?" -> PATCH /notifications/{id}
- "Get notification details?" -> GET /notifications/{id}
- "Create a notification?" -> POST /notifications
- "List all notifications?" -> GET /notifications
- "List all outbound_connection_logs?" -> GET /outbound_connection_logs
- "Delete a partner?" -> DELETE /partners/{id}
- "Partially update a partner?" -> PATCH /partners/{id}
- "Get partner details?" -> GET /partners/{id}
- "List all partners?" -> GET /partners
- "Create a partner?" -> POST /partners
- "List all linked_partner_sites?" -> GET /partner_sites/linked_partner_sites
- "List all partner_sites?" -> GET /partner_sites
- "Create a reject?" -> POST /partner_site_requests/{id}/reject
- "Create a approve?" -> POST /partner_site_requests/{id}/approve
- "List all find_by_pairing_key?" -> GET /partner_site_requests/find_by_pairing_key
- "Delete a partner_site_request?" -> DELETE /partner_site_requests/{id}
- "Create a partner_site_request?" -> POST /partner_site_requests
- "List all partner_site_requests?" -> GET /partner_site_requests
- "Get payment details?" -> GET /payments/{id}
- "List all payments?" -> GET /payments
- "Delete a permission?" -> DELETE /permissions/{id}
- "Create a permission?" -> POST /permissions
- "List all permissions?" -> GET /permissions
- "List all priorities?" -> GET /priorities
- "Delete a project?" -> DELETE /projects/{id}
- "Partially update a project?" -> PATCH /projects/{id}
- "Get project details?" -> GET /projects/{id}
- "Create a project?" -> POST /projects
- "List all projects?" -> GET /projects
- "List all public_hosting_request_logs?" -> GET /public_hosting_request_logs
- "Delete a public_key?" -> DELETE /public_keys/{id}
- "Partially update a public_key?" -> PATCH /public_keys/{id}
- "Get public_key details?" -> GET /public_keys/{id}
- "Create a public_key?" -> POST /public_keys
- "List all public_keys?" -> GET /public_keys
- "Create a restore?" -> POST /restores
- "List all restores?" -> GET /restores
- "List all remote_bandwidth_snapshots?" -> GET /remote_bandwidth_snapshots
- "Create a reset_status?" -> POST /remote_mount_backends/{id}/reset_status
- "Delete a remote_mount_backend?" -> DELETE /remote_mount_backends/{id}
- "Partially update a remote_mount_backend?" -> PATCH /remote_mount_backends/{id}
- "Get remote_mount_backend details?" -> GET /remote_mount_backends/{id}
- "List all remote_mount_backends?" -> GET /remote_mount_backends
- "Create a remote_mount_backend?" -> POST /remote_mount_backends
- "Create a agent_push_update?" -> POST /remote_servers/{id}/agent_push_update
- "Create a configuration_file?" -> POST /remote_servers/{id}/configuration_file
- "List all configuration_file?" -> GET /remote_servers/{id}/configuration_file
- "List all remote_servers?" -> GET /remote_servers
- "Create a remote_server?" -> POST /remote_servers
- "Delete a remote_server?" -> DELETE /remote_servers/{id}
- "Partially update a remote_server?" -> PATCH /remote_servers/{id}
- "Get remote_server details?" -> GET /remote_servers/{id}
- "List all remote_server_credentials?" -> GET /remote_server_credentials
- "Create a remote_server_credential?" -> POST /remote_server_credentials
- "Delete a remote_server_credential?" -> DELETE /remote_server_credentials/{id}
- "Partially update a remote_server_credential?" -> PATCH /remote_server_credentials/{id}
- "Get remote_server_credential details?" -> GET /remote_server_credentials/{id}
- "Delete a request?" -> DELETE /requests/{id}
- "Create a request?" -> POST /requests
- "List all requests?" -> GET /requests
- "Get folder details?" -> GET /requests/folders/{path}
- "Get scim_log details?" -> GET /scim_logs/{id}
- "List all scim_logs?" -> GET /scim_logs
- "List all settings_changes?" -> GET /settings_changes
- "List all sftp_action_logs?" -> GET /sftp_action_logs
- "List all sftp_host_keys?" -> GET /sftp_host_keys
- "Create a sftp_host_key?" -> POST /sftp_host_keys
- "Delete a sftp_host_key?" -> DELETE /sftp_host_keys/{id}
- "Partially update a sftp_host_key?" -> PATCH /sftp_host_keys/{id}
- "Get sftp_host_key details?" -> GET /sftp_host_keys/{id}
- "List all share_groups?" -> GET /share_groups
- "Create a share_group?" -> POST /share_groups
- "Delete a share_group?" -> DELETE /share_groups/{id}
- "Get share_group details?" -> GET /share_groups/{id}
- "Partially update a share_group?" -> PATCH /share_groups/{id}
- "List all siem_http_destinations?" -> GET /siem_http_destinations
- "Create a siem_http_destination?" -> POST /siem_http_destinations
- "Delete a siem_http_destination?" -> DELETE /siem_http_destinations/{id}
- "Get siem_http_destination details?" -> GET /siem_http_destinations/{id}
- "Partially update a siem_http_destination?" -> PATCH /siem_http_destinations/{id}
- "Create a send_test_entry?" -> POST /siem_http_destinations/send_test_entry
- "Create a finalize?" -> POST /snapshots/{id}/finalize
- "Delete a snapshot?" -> DELETE /snapshots/{id}
- "Partially update a snapshot?" -> PATCH /snapshots/{id}
- "Get snapshot details?" -> GET /snapshots/{id}
- "Create a snapshot?" -> POST /snapshots
- "List all snapshots?" -> GET /snapshots
- "Create a sync?" -> POST /sso_strategies/{id}/sync
- "Get sso_strategy details?" -> GET /sso_strategies/{id}
- "List all sso_strategies?" -> GET /sso_strategies
- "Delete a style?" -> DELETE /styles/{path}
- "Partially update a style?" -> PATCH /styles/{path}
- "Get style details?" -> GET /styles/{path}
- "Create a dry_run?" -> POST /syncs/{id}/dry_run
- "Create a manual_run?" -> POST /syncs/{id}/manual_run
- "Delete a sync?" -> DELETE /syncs/{id}
- "Partially update a sync?" -> PATCH /syncs/{id}
- "Get sync details?" -> GET /syncs/{id}
- "List all syncs?" -> GET /syncs
- "Create a sync?" -> POST /syncs
- "List all sync_logs?" -> GET /sync_logs
- "Get sync_run details?" -> GET /sync_runs/{id}
- "List all sync_runs?" -> GET /sync_runs
- "List all usage_snapshots?" -> GET /usage_snapshots
- "List all usage_daily_snapshots?" -> GET /usage_daily_snapshots
- "List all user_cipher_uses?" -> GET /user_cipher_uses
- "Partially update a user_lifecycle_rule?" -> PATCH /user_lifecycle_rules/{id}
- "Delete a user_lifecycle_rule?" -> DELETE /user_lifecycle_rules/{id}
- "Get user_lifecycle_rule details?" -> GET /user_lifecycle_rules/{id}
- "Create a user_lifecycle_rule?" -> POST /user_lifecycle_rules
- "List all user_lifecycle_rules?" -> GET /user_lifecycle_rules
- "List all user_requests?" -> GET /user_requests
- "Create a user_request?" -> POST /user_requests
- "Delete a user_request?" -> DELETE /user_requests/{id}
- "Get user_request details?" -> GET /user_requests/{id}
- "List all user_sftp_client_uses?" -> GET /user_sftp_client_uses
- "List all web_dav_action_logs?" -> GET /web_dav_action_logs
- "Create a webhook_test?" -> POST /webhook_tests
- "Delete a workspace?" -> DELETE /workspaces/{id}
- "Partially update a workspace?" -> PATCH /workspaces/{id}
- "Get workspace details?" -> GET /workspaces/{id}
- "Create a workspace?" -> POST /workspaces
- "List all workspaces?" -> GET /workspaces
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
