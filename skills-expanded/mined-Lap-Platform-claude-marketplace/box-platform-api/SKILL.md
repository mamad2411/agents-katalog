---
name: box-platform-api
description: "Box Platform API skill. Use when working with Box Platform for authorize, oauth2, files. Covers 296 endpoints."
version: 1.0.0
generator: lapsh
---

# Box Platform API
API version: 2024.0

## Auth
OAuth2

## Base URL
https://api.box.com/2.0

## Setup
1. Configure auth: OAuth2
2. GET /authorize -- verify access
3. POST /oauth2/token -- create first token

## Endpoints

296 endpoints across 56 groups. See references/api-spec.lap for full details.

### authorize
| Method | Path | Description |
|--------|------|-------------|
| GET | /authorize | Authorize user |

### oauth2
| Method | Path | Description |
|--------|------|-------------|
| POST | /oauth2/token | Request access token |
| POST | /oauth2/token#refresh | Refresh access token |
| POST | /oauth2/revoke | Revoke access token |

### files
| Method | Path | Description |
|--------|------|-------------|
| GET | /files/{file_id} | Get file information |
| POST | /files/{file_id} | Restore file |
| PUT | /files/{file_id} | Update file |
| DELETE | /files/{file_id} | Delete file |
| GET | /files/{file_id}/app_item_associations | List file app item associations |
| GET | /files/{file_id}/content | Download file |
| POST | /files/{file_id}/content | Upload file version |
| OPTIONS | /files/content | Preflight check before upload |
| POST | /files/content | Upload file |
| POST | /files/upload_sessions | Create upload session |
| POST | /files/{file_id}/upload_sessions | Create upload session for existing file |
| GET | /files/upload_sessions/{upload_session_id} | Get upload session |
| PUT | /files/upload_sessions/{upload_session_id} | Upload part of file |
| DELETE | /files/upload_sessions/{upload_session_id} | Remove upload session |
| GET | /files/upload_sessions/{upload_session_id}/parts | List parts |
| POST | /files/upload_sessions/{upload_session_id}/commit | Commit upload session |
| POST | /files/{file_id}/copy | Copy file |
| GET | /files/{file_id}/thumbnail.{extension} | Get file thumbnail |
| GET | /files/{file_id}/collaborations | List file collaborations |
| GET | /files/{file_id}/comments | List file comments |
| GET | /files/{file_id}/tasks | List tasks on file |
| GET | /files/{file_id}/trash | Get trashed file |
| DELETE | /files/{file_id}/trash | Permanently remove file |
| GET | /files/{file_id}/versions | List all file versions |
| GET | /files/{file_id}/versions/{file_version_id} | Get file version |
| DELETE | /files/{file_id}/versions/{file_version_id} | Remove file version |
| PUT | /files/{file_id}/versions/{file_version_id} | Restore file version |
| POST | /files/{file_id}/versions/current | Promote file version |
| GET | /files/{file_id}/metadata | List metadata instances on file |
| GET | /files/{file_id}/metadata/enterprise/securityClassification-6VMVochwUWo | Get classification on file |
| POST | /files/{file_id}/metadata/enterprise/securityClassification-6VMVochwUWo | Add classification to file |
| PUT | /files/{file_id}/metadata/enterprise/securityClassification-6VMVochwUWo | Update classification on file |
| DELETE | /files/{file_id}/metadata/enterprise/securityClassification-6VMVochwUWo | Remove classification from file |
| GET | /files/{file_id}/metadata/{scope}/{template_key} | Get metadata instance on file |
| POST | /files/{file_id}/metadata/{scope}/{template_key} | Create metadata instance on file |
| PUT | /files/{file_id}/metadata/{scope}/{template_key} | Update metadata instance on file |
| DELETE | /files/{file_id}/metadata/{scope}/{template_key} | Remove metadata instance from file |
| GET | /files/{file_id}/metadata/global/boxSkillsCards | List Box Skill cards on file |
| POST | /files/{file_id}/metadata/global/boxSkillsCards | Create Box Skill cards on file |
| PUT | /files/{file_id}/metadata/global/boxSkillsCards | Update Box Skill cards on file |
| DELETE | /files/{file_id}/metadata/global/boxSkillsCards | Remove Box Skill cards from file |
| GET | /files/{file_id}/watermark | Get watermark on file |
| PUT | /files/{file_id}/watermark | Apply watermark to file |
| DELETE | /files/{file_id}/watermark | Remove watermark from file |
| GET | /files/{file_id}#get_shared_link | Get shared link for file |
| PUT | /files/{file_id}#add_shared_link | Add shared link to file |
| PUT | /files/{file_id}#update_shared_link | Update shared link on file |
| PUT | /files/{file_id}#remove_shared_link | Remove shared link from file |

### file_requests
| Method | Path | Description |
|--------|------|-------------|
| GET | /file_requests/{file_request_id} | Get file request |
| PUT | /file_requests/{file_request_id} | Update file request |
| DELETE | /file_requests/{file_request_id} | Delete file request |
| POST | /file_requests/{file_request_id}/copy | Copy file request |

### folders
| Method | Path | Description |
|--------|------|-------------|
| GET | /folders/{folder_id} | Get folder information |
| POST | /folders/{folder_id} | Restore folder |
| PUT | /folders/{folder_id} | Update folder |
| DELETE | /folders/{folder_id} | Delete folder |
| GET | /folders/{folder_id}/app_item_associations | List folder app item associations |
| GET | /folders/{folder_id}/items | List items in folder |
| POST | /folders | Create folder |
| POST | /folders/{folder_id}/copy | Copy folder |
| GET | /folders/{folder_id}/collaborations | List folder collaborations |
| GET | /folders/{folder_id}/trash | Get trashed folder |
| DELETE | /folders/{folder_id}/trash | Permanently remove folder |
| GET | /folders/{folder_id}/metadata | List metadata instances on folder |
| GET | /folders/{folder_id}/metadata/enterprise/securityClassification-6VMVochwUWo | Get classification on folder |
| POST | /folders/{folder_id}/metadata/enterprise/securityClassification-6VMVochwUWo | Add classification to folder |
| PUT | /folders/{folder_id}/metadata/enterprise/securityClassification-6VMVochwUWo | Update classification on folder |
| DELETE | /folders/{folder_id}/metadata/enterprise/securityClassification-6VMVochwUWo | Remove classification from folder |
| GET | /folders/{folder_id}/metadata/{scope}/{template_key} | Get metadata instance on folder |
| POST | /folders/{folder_id}/metadata/{scope}/{template_key} | Create metadata instance on folder |
| PUT | /folders/{folder_id}/metadata/{scope}/{template_key} | Update metadata instance on folder |
| DELETE | /folders/{folder_id}/metadata/{scope}/{template_key} | Remove metadata instance from folder |
| GET | /folders/trash/items | List trashed items |
| GET | /folders/{folder_id}/watermark | Get watermark for folder |
| PUT | /folders/{folder_id}/watermark | Apply watermark to folder |
| DELETE | /folders/{folder_id}/watermark | Remove watermark from folder |
| GET | /folders/{folder_id}#get_shared_link | Get shared link for folder |
| PUT | /folders/{folder_id}#add_shared_link | Add shared link to folder |
| PUT | /folders/{folder_id}#update_shared_link | Update shared link on folder |
| PUT | /folders/{folder_id}#remove_shared_link | Remove shared link from folder |

### folder_locks
| Method | Path | Description |
|--------|------|-------------|
| GET | /folder_locks | List folder locks |
| POST | /folder_locks | Create folder lock |
| DELETE | /folder_locks/{folder_lock_id} | Delete folder lock |

### metadata_templates
| Method | Path | Description |
|--------|------|-------------|
| GET | /metadata_templates | Find metadata template by instance ID |
| GET | /metadata_templates/enterprise/securityClassification-6VMVochwUWo/schema | List all classifications |
| PUT | /metadata_templates/enterprise/securityClassification-6VMVochwUWo/schema#add | Add classification |
| PUT | /metadata_templates/enterprise/securityClassification-6VMVochwUWo/schema#update | Update classification |
| GET | /metadata_templates/{scope}/{template_key}/schema | Get metadata template by name |
| PUT | /metadata_templates/{scope}/{template_key}/schema | Update metadata template |
| DELETE | /metadata_templates/{scope}/{template_key}/schema | Remove metadata template |
| GET | /metadata_templates/{template_id} | Get metadata template by ID |
| GET | /metadata_templates/global | List all global metadata templates |
| GET | /metadata_templates/enterprise | List all metadata templates for enterprise |
| POST | /metadata_templates/schema | Create metadata template |
| POST | /metadata_templates/schema#classifications | Add initial classifications |
| GET | /metadata_templates/{namespace}/{template_key}/fields/{field_key}/options | List metadata template's options for taxonomy field |

### metadata_cascade_policies
| Method | Path | Description |
|--------|------|-------------|
| GET | /metadata_cascade_policies | List metadata cascade policies |
| POST | /metadata_cascade_policies | Create metadata cascade policy |
| GET | /metadata_cascade_policies/{metadata_cascade_policy_id} | Get metadata cascade policy |
| DELETE | /metadata_cascade_policies/{metadata_cascade_policy_id} | Remove metadata cascade policy |
| POST | /metadata_cascade_policies/{metadata_cascade_policy_id}/apply | Force-apply metadata cascade policy to folder |

### metadata_queries
| Method | Path | Description |
|--------|------|-------------|
| POST | /metadata_queries/execute_read | Query files/folders by metadata |

### comments
| Method | Path | Description |
|--------|------|-------------|
| GET | /comments/{comment_id} | Get comment |
| PUT | /comments/{comment_id} | Update comment |
| DELETE | /comments/{comment_id} | Remove comment |
| POST | /comments | Create comment |

### collaborations
| Method | Path | Description |
|--------|------|-------------|
| GET | /collaborations/{collaboration_id} | Get collaboration |
| PUT | /collaborations/{collaboration_id} | Update collaboration |
| DELETE | /collaborations/{collaboration_id} | Remove collaboration |
| GET | /collaborations | List pending collaborations |
| POST | /collaborations | Create collaboration |

### search
| Method | Path | Description |
|--------|------|-------------|
| GET | /search | Search for content |

### tasks
| Method | Path | Description |
|--------|------|-------------|
| POST | /tasks | Create task |
| GET | /tasks/{task_id} | Get task |
| PUT | /tasks/{task_id} | Update task |
| DELETE | /tasks/{task_id} | Remove task |
| GET | /tasks/{task_id}/assignments | List task assignments |

### task_assignments
| Method | Path | Description |
|--------|------|-------------|
| POST | /task_assignments | Assign task |
| GET | /task_assignments/{task_assignment_id} | Get task assignment |
| PUT | /task_assignments/{task_assignment_id} | Update task assignment |
| DELETE | /task_assignments/{task_assignment_id} | Unassign task |

### shared_items
| Method | Path | Description |
|--------|------|-------------|
| GET | /shared_items | Find file for shared link |

### shared_items#folders
| Method | Path | Description |
|--------|------|-------------|
| GET | /shared_items#folders | Find folder for shared link |

### web_links
| Method | Path | Description |
|--------|------|-------------|
| POST | /web_links | Create web link |
| GET | /web_links/{web_link_id} | Get web link |
| POST | /web_links/{web_link_id} | Restore web link |
| PUT | /web_links/{web_link_id} | Update web link |
| DELETE | /web_links/{web_link_id} | Remove web link |
| GET | /web_links/{web_link_id}/trash | Get trashed web link |
| DELETE | /web_links/{web_link_id}/trash | Permanently remove web link |
| GET | /web_links/{web_link_id}#get_shared_link | Get shared link for web link |
| PUT | /web_links/{web_link_id}#add_shared_link | Add shared link to web link |
| PUT | /web_links/{web_link_id}#update_shared_link | Update shared link on web link |
| PUT | /web_links/{web_link_id}#remove_shared_link | Remove shared link from web link |

### shared_items#web_links
| Method | Path | Description |
|--------|------|-------------|
| GET | /shared_items#web_links | Find web link for shared link |

### shared_items#app_items
| Method | Path | Description |
|--------|------|-------------|
| GET | /shared_items#app_items | Find app item for shared link |

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /users | List enterprise users |
| POST | /users | Create user |
| GET | /users/me | Get current user |
| POST | /users/terminate_sessions | Create jobs to terminate users session |
| GET | /users/{user_id} | Get user |
| PUT | /users/{user_id} | Update user |
| DELETE | /users/{user_id} | Delete user |
| GET | /users/{user_id}/avatar | Get user avatar |
| POST | /users/{user_id}/avatar | Add or update user avatar |
| DELETE | /users/{user_id}/avatar | Delete user avatar |
| PUT | /users/{user_id}/folders/0 | Transfer owned folders |
| GET | /users/{user_id}/email_aliases | List user's email aliases |
| POST | /users/{user_id}/email_aliases | Create email alias |
| DELETE | /users/{user_id}/email_aliases/{email_alias_id} | Remove email alias |
| GET | /users/{user_id}/memberships | List user's groups |

### invites
| Method | Path | Description |
|--------|------|-------------|
| POST | /invites | Create user invite |
| GET | /invites/{invite_id} | Get user invite status |

### groups
| Method | Path | Description |
|--------|------|-------------|
| GET | /groups | List groups for enterprise |
| POST | /groups | Create group |
| POST | /groups/terminate_sessions | Create jobs to terminate user group session |
| GET | /groups/{group_id} | Get group |
| PUT | /groups/{group_id} | Update group |
| DELETE | /groups/{group_id} | Remove group |
| GET | /groups/{group_id}/memberships | List members of group |
| GET | /groups/{group_id}/collaborations | List group collaborations |

### group_memberships
| Method | Path | Description |
|--------|------|-------------|
| POST | /group_memberships | Add user to group |
| GET | /group_memberships/{group_membership_id} | Get group membership |
| PUT | /group_memberships/{group_membership_id} | Update group membership |
| DELETE | /group_memberships/{group_membership_id} | Remove user from group |

### webhooks
| Method | Path | Description |
|--------|------|-------------|
| GET | /webhooks | List all webhooks |
| POST | /webhooks | Create webhook |
| GET | /webhooks/{webhook_id} | Get webhook |
| PUT | /webhooks/{webhook_id} | Update webhook |
| DELETE | /webhooks/{webhook_id} | Remove webhook |

### skill_invocations
| Method | Path | Description |
|--------|------|-------------|
| PUT | /skill_invocations/{skill_id} | Update all Box Skill cards on file |

### events
| Method | Path | Description |
|--------|------|-------------|
| OPTIONS | /events | Get events long poll endpoint |
| GET | /events | List user and enterprise events |

### collections
| Method | Path | Description |
|--------|------|-------------|
| GET | /collections | List all collections |
| GET | /collections/{collection_id}/items | List collection items |
| GET | /collections/{collection_id} | Get collection by ID |

### recent_items
| Method | Path | Description |
|--------|------|-------------|
| GET | /recent_items | List recently accessed items |

### retention_policies
| Method | Path | Description |
|--------|------|-------------|
| GET | /retention_policies | List retention policies |
| POST | /retention_policies | Create retention policy |
| GET | /retention_policies/{retention_policy_id} | Get retention policy |
| PUT | /retention_policies/{retention_policy_id} | Update retention policy |
| DELETE | /retention_policies/{retention_policy_id} | Delete retention policy |
| GET | /retention_policies/{retention_policy_id}/assignments | List retention policy assignments |

### retention_policy_assignments
| Method | Path | Description |
|--------|------|-------------|
| POST | /retention_policy_assignments | Assign retention policy |
| GET | /retention_policy_assignments/{retention_policy_assignment_id} | Get retention policy assignment |
| DELETE | /retention_policy_assignments/{retention_policy_assignment_id} | Remove retention policy assignment |
| GET | /retention_policy_assignments/{retention_policy_assignment_id}/files_under_retention | Get files under retention |
| GET | /retention_policy_assignments/{retention_policy_assignment_id}/file_versions_under_retention | Get file versions under retention |

### legal_hold_policies
| Method | Path | Description |
|--------|------|-------------|
| GET | /legal_hold_policies | List all legal hold policies |
| POST | /legal_hold_policies | Create legal hold policy |
| GET | /legal_hold_policies/{legal_hold_policy_id} | Get legal hold policy |
| PUT | /legal_hold_policies/{legal_hold_policy_id} | Update legal hold policy |
| DELETE | /legal_hold_policies/{legal_hold_policy_id} | Remove legal hold policy |

### legal_hold_policy_assignments
| Method | Path | Description |
|--------|------|-------------|
| GET | /legal_hold_policy_assignments | List legal hold policy assignments |
| POST | /legal_hold_policy_assignments | Assign legal hold policy |
| GET | /legal_hold_policy_assignments/{legal_hold_policy_assignment_id} | Get legal hold policy assignment |
| DELETE | /legal_hold_policy_assignments/{legal_hold_policy_assignment_id} | Unassign legal hold policy |
| GET | /legal_hold_policy_assignments/{legal_hold_policy_assignment_id}/files_on_hold | List files with current file versions for legal hold policy assignment |
| GET | /legal_hold_policy_assignments/{legal_hold_policy_assignment_id}/file_versions_on_hold | List previous file versions for legal hold policy assignment |

### file_version_retentions
| Method | Path | Description |
|--------|------|-------------|
| GET | /file_version_retentions | List file version retentions |
| GET | /file_version_retentions/{file_version_retention_id} | Get retention on file |

### file_version_legal_holds
| Method | Path | Description |
|--------|------|-------------|
| GET | /file_version_legal_holds/{file_version_legal_hold_id} | Get file version legal hold |
| GET | /file_version_legal_holds | List file version legal holds |

### shield_information_barriers
| Method | Path | Description |
|--------|------|-------------|
| GET | /shield_information_barriers/{shield_information_barrier_id} | Get shield information barrier with specified ID |
| POST | /shield_information_barriers/change_status | Add changed status of shield information barrier with specified ID |
| GET | /shield_information_barriers | List shield information barriers |
| POST | /shield_information_barriers | Create shield information barrier |

### shield_information_barrier_reports
| Method | Path | Description |
|--------|------|-------------|
| GET | /shield_information_barrier_reports | List shield information barrier reports |
| POST | /shield_information_barrier_reports | Create shield information barrier report |
| GET | /shield_information_barrier_reports/{shield_information_barrier_report_id} | Get shield information barrier report by ID |

### shield_information_barrier_segments
| Method | Path | Description |
|--------|------|-------------|
| GET | /shield_information_barrier_segments/{shield_information_barrier_segment_id} | Get shield information barrier segment with specified ID |
| DELETE | /shield_information_barrier_segments/{shield_information_barrier_segment_id} | Delete shield information barrier segment |
| PUT | /shield_information_barrier_segments/{shield_information_barrier_segment_id} | Update shield information barrier segment with specified ID |
| GET | /shield_information_barrier_segments | List shield information barrier segments |
| POST | /shield_information_barrier_segments | Create shield information barrier segment |

### shield_information_barrier_segment_members
| Method | Path | Description |
|--------|------|-------------|
| GET | /shield_information_barrier_segment_members/{shield_information_barrier_segment_member_id} | Get shield information barrier segment member by ID |
| DELETE | /shield_information_barrier_segment_members/{shield_information_barrier_segment_member_id} | Delete shield information barrier segment member by ID |
| GET | /shield_information_barrier_segment_members | List shield information barrier segment members |
| POST | /shield_information_barrier_segment_members | Create shield information barrier segment member |

### shield_information_barrier_segment_restrictions
| Method | Path | Description |
|--------|------|-------------|
| GET | /shield_information_barrier_segment_restrictions/{shield_information_barrier_segment_restriction_id} | Get shield information barrier segment restriction by ID |
| DELETE | /shield_information_barrier_segment_restrictions/{shield_information_barrier_segment_restriction_id} | Delete shield information barrier segment restriction by ID |
| GET | /shield_information_barrier_segment_restrictions | List shield information barrier segment restrictions |
| POST | /shield_information_barrier_segment_restrictions | Create shield information barrier segment restriction |

### device_pinners
| Method | Path | Description |
|--------|------|-------------|
| GET | /device_pinners/{device_pinner_id} | Get device pin |
| DELETE | /device_pinners/{device_pinner_id} | Remove device pin |

### enterprises
| Method | Path | Description |
|--------|------|-------------|
| GET | /enterprises/{enterprise_id}/device_pinners | List enterprise device pins |

### terms_of_services
| Method | Path | Description |
|--------|------|-------------|
| GET | /terms_of_services | List terms of services |
| POST | /terms_of_services | Create terms of service |
| GET | /terms_of_services/{terms_of_service_id} | Get terms of service |
| PUT | /terms_of_services/{terms_of_service_id} | Update terms of service |

### terms_of_service_user_statuses
| Method | Path | Description |
|--------|------|-------------|
| GET | /terms_of_service_user_statuses | List terms of service user statuses |
| POST | /terms_of_service_user_statuses | Create terms of service status for new user |
| PUT | /terms_of_service_user_statuses/{terms_of_service_user_status_id} | Update terms of service status for existing user |

### collaboration_whitelist_entries
| Method | Path | Description |
|--------|------|-------------|
| GET | /collaboration_whitelist_entries | List allowed collaboration domains |
| POST | /collaboration_whitelist_entries | Add domain to list of allowed collaboration domains |
| GET | /collaboration_whitelist_entries/{collaboration_whitelist_entry_id} | Get allowed collaboration domain |
| DELETE | /collaboration_whitelist_entries/{collaboration_whitelist_entry_id} | Remove domain from list of allowed collaboration domains |

### collaboration_whitelist_exempt_targets
| Method | Path | Description |
|--------|------|-------------|
| GET | /collaboration_whitelist_exempt_targets | List users exempt from collaboration domain restrictions |
| POST | /collaboration_whitelist_exempt_targets | Create user exemption from collaboration domain restrictions |
| GET | /collaboration_whitelist_exempt_targets/{collaboration_whitelist_exempt_target_id} | Get user exempt from collaboration domain restrictions |
| DELETE | /collaboration_whitelist_exempt_targets/{collaboration_whitelist_exempt_target_id} | Remove user from list of users exempt from domain restrictions |

### storage_policies
| Method | Path | Description |
|--------|------|-------------|
| GET | /storage_policies | List storage policies |
| GET | /storage_policies/{storage_policy_id} | Get storage policy |

### storage_policy_assignments
| Method | Path | Description |
|--------|------|-------------|
| GET | /storage_policy_assignments | List storage policy assignments |
| POST | /storage_policy_assignments | Assign storage policy |
| GET | /storage_policy_assignments/{storage_policy_assignment_id} | Get storage policy assignment |
| PUT | /storage_policy_assignments/{storage_policy_assignment_id} | Update storage policy assignment |
| DELETE | /storage_policy_assignments/{storage_policy_assignment_id} | Unassign storage policy |

### zip_downloads
| Method | Path | Description |
|--------|------|-------------|
| POST | /zip_downloads | Create zip download |
| GET | /zip_downloads/{zip_download_id}/content | Download zip archive |
| GET | /zip_downloads/{zip_download_id}/status | Get zip download status |

### sign_requests
| Method | Path | Description |
|--------|------|-------------|
| POST | /sign_requests/{sign_request_id}/cancel | Cancel Box Sign request |
| POST | /sign_requests/{sign_request_id}/resend | Resend Box Sign request |
| GET | /sign_requests/{sign_request_id} | Get Box Sign request by ID |
| GET | /sign_requests | List Box Sign requests |
| POST | /sign_requests | Create Box Sign request |

### workflows
| Method | Path | Description |
|--------|------|-------------|
| GET | /workflows | List workflows |
| POST | /workflows/{workflow_id}/start | Starts workflow based on request body |

### sign_templates
| Method | Path | Description |
|--------|------|-------------|
| GET | /sign_templates | List Box Sign templates |
| GET | /sign_templates/{template_id} | Get Box Sign template by ID |

### integration_mappings
| Method | Path | Description |
|--------|------|-------------|
| GET | /integration_mappings/slack | List Slack integration mappings |
| POST | /integration_mappings/slack | Create Slack integration mapping |
| PUT | /integration_mappings/slack/{integration_mapping_id} | Update Slack integration mapping |
| DELETE | /integration_mappings/slack/{integration_mapping_id} | Delete Slack integration mapping |
| GET | /integration_mappings/teams | List Teams integration mappings |
| POST | /integration_mappings/teams | Create Teams integration mapping |
| PUT | /integration_mappings/teams/{integration_mapping_id} | Update Teams integration mapping |
| DELETE | /integration_mappings/teams/{integration_mapping_id} | Delete Teams integration mapping |

### ai
| Method | Path | Description |
|--------|------|-------------|
| POST | /ai/ask | Ask question |
| POST | /ai/text_gen | Generate text |
| POST | /ai/extract | Extract metadata (freeform) |
| POST | /ai/extract_structured | Extract metadata (structured) |

### ai_agent_default
| Method | Path | Description |
|--------|------|-------------|
| GET | /ai_agent_default | Get AI agent default configuration |

### ai_agents
| Method | Path | Description |
|--------|------|-------------|
| GET | /ai_agents | List AI agents |
| POST | /ai_agents | Create AI agent |
| PUT | /ai_agents/{agent_id} | Update AI agent |
| GET | /ai_agents/{agent_id} | Get AI agent by agent ID |
| DELETE | /ai_agents/{agent_id} | Delete AI agent |

### metadata_taxonomies
| Method | Path | Description |
|--------|------|-------------|
| POST | /metadata_taxonomies | Create metadata taxonomy |
| GET | /metadata_taxonomies/{namespace} | Get metadata taxonomies for namespace |
| GET | /metadata_taxonomies/{namespace}/{taxonomy_key} | Get metadata taxonomy by taxonomy key |
| PATCH | /metadata_taxonomies/{namespace}/{taxonomy_key} | Update metadata taxonomy |
| DELETE | /metadata_taxonomies/{namespace}/{taxonomy_key} | Remove metadata taxonomy |
| POST | /metadata_taxonomies/{namespace}/{taxonomy_key}/levels | Create metadata taxonomy levels |
| PATCH | /metadata_taxonomies/{namespace}/{taxonomy_key}/levels/{level_index} | Update metadata taxonomy level |
| POST | /metadata_taxonomies/{namespace}/{taxonomy_key}/levels:append | Add metadata taxonomy level |
| POST | /metadata_taxonomies/{namespace}/{taxonomy_key}/levels:trim | Delete metadata taxonomy level |
| GET | /metadata_taxonomies/{namespace}/{taxonomy_key}/nodes | List metadata taxonomy nodes |
| POST | /metadata_taxonomies/{namespace}/{taxonomy_key}/nodes | Create metadata taxonomy node |
| GET | /metadata_taxonomies/{namespace}/{taxonomy_key}/nodes/{node_id} | Get metadata taxonomy node by ID |
| PATCH | /metadata_taxonomies/{namespace}/{taxonomy_key}/nodes/{node_id} | Update metadata taxonomy node |
| DELETE | /metadata_taxonomies/{namespace}/{taxonomy_key}/nodes/{node_id} | Remove metadata taxonomy node |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all authorize?" -> GET /authorize
- "Create a token?" -> POST /oauth2/token
- "Create a token#refresh?" -> POST /oauth2/token#refresh
- "Create a revoke?" -> POST /oauth2/revoke
- "Get file details?" -> GET /files/{file_id}
- "Update a file?" -> PUT /files/{file_id}
- "Delete a file?" -> DELETE /files/{file_id}
- "List all app_item_associations?" -> GET /files/{file_id}/app_item_associations
- "List all content?" -> GET /files/{file_id}/content
- "Create a content?" -> POST /files/{file_id}/content
- "Create a content?" -> POST /files/content
- "Create a upload_session?" -> POST /files/upload_sessions
- "Create a upload_session?" -> POST /files/{file_id}/upload_sessions
- "Get upload_session details?" -> GET /files/upload_sessions/{upload_session_id}
- "Update a upload_session?" -> PUT /files/upload_sessions/{upload_session_id}
- "Delete a upload_session?" -> DELETE /files/upload_sessions/{upload_session_id}
- "List all parts?" -> GET /files/upload_sessions/{upload_session_id}/parts
- "Create a commit?" -> POST /files/upload_sessions/{upload_session_id}/commit
- "Create a copy?" -> POST /files/{file_id}/copy
- "Get thumbnail.{extension} details?" -> GET /files/{file_id}/thumbnail.{extension}
- "List all collaborations?" -> GET /files/{file_id}/collaborations
- "List all comments?" -> GET /files/{file_id}/comments
- "List all tasks?" -> GET /files/{file_id}/tasks
- "List all trash?" -> GET /files/{file_id}/trash
- "List all versions?" -> GET /files/{file_id}/versions
- "Get version details?" -> GET /files/{file_id}/versions/{file_version_id}
- "Delete a version?" -> DELETE /files/{file_id}/versions/{file_version_id}
- "Update a version?" -> PUT /files/{file_id}/versions/{file_version_id}
- "Create a current?" -> POST /files/{file_id}/versions/current
- "List all metadata?" -> GET /files/{file_id}/metadata
- "List all securityClassification-6VMVochwUWo?" -> GET /files/{file_id}/metadata/enterprise/securityClassification-6VMVochwUWo
- "Create a securityClassification-6VMVochwUWo?" -> POST /files/{file_id}/metadata/enterprise/securityClassification-6VMVochwUWo
- "Get metadata details?" -> GET /files/{file_id}/metadata/{scope}/{template_key}
- "Update a metadata?" -> PUT /files/{file_id}/metadata/{scope}/{template_key}
- "Delete a metadata?" -> DELETE /files/{file_id}/metadata/{scope}/{template_key}
- "List all boxSkillsCards?" -> GET /files/{file_id}/metadata/global/boxSkillsCards
- "Create a boxSkillsCard?" -> POST /files/{file_id}/metadata/global/boxSkillsCards
- "List all watermark?" -> GET /files/{file_id}/watermark
- "Get file_request details?" -> GET /file_requests/{file_request_id}
- "Update a file_request?" -> PUT /file_requests/{file_request_id}
- "Delete a file_request?" -> DELETE /file_requests/{file_request_id}
- "Create a copy?" -> POST /file_requests/{file_request_id}/copy
- "Get folder details?" -> GET /folders/{folder_id}
- "Update a folder?" -> PUT /folders/{folder_id}
- "Delete a folder?" -> DELETE /folders/{folder_id}
- "List all app_item_associations?" -> GET /folders/{folder_id}/app_item_associations
- "List all items?" -> GET /folders/{folder_id}/items
- "Create a folder?" -> POST /folders
- "Create a copy?" -> POST /folders/{folder_id}/copy
- "List all collaborations?" -> GET /folders/{folder_id}/collaborations
- "List all trash?" -> GET /folders/{folder_id}/trash
- "List all metadata?" -> GET /folders/{folder_id}/metadata
- "List all securityClassification-6VMVochwUWo?" -> GET /folders/{folder_id}/metadata/enterprise/securityClassification-6VMVochwUWo
- "Create a securityClassification-6VMVochwUWo?" -> POST /folders/{folder_id}/metadata/enterprise/securityClassification-6VMVochwUWo
- "Get metadata details?" -> GET /folders/{folder_id}/metadata/{scope}/{template_key}
- "Update a metadata?" -> PUT /folders/{folder_id}/metadata/{scope}/{template_key}
- "Delete a metadata?" -> DELETE /folders/{folder_id}/metadata/{scope}/{template_key}
- "List all items?" -> GET /folders/trash/items
- "List all watermark?" -> GET /folders/{folder_id}/watermark
- "List all folder_locks?" -> GET /folder_locks
- "Create a folder_lock?" -> POST /folder_locks
- "Delete a folder_lock?" -> DELETE /folder_locks/{folder_lock_id}
- "List all metadata_templates?" -> GET /metadata_templates
- "List all schema?" -> GET /metadata_templates/enterprise/securityClassification-6VMVochwUWo/schema
- "List all schema?" -> GET /metadata_templates/{scope}/{template_key}/schema
- "Get metadata_template details?" -> GET /metadata_templates/{template_id}
- "List all global?" -> GET /metadata_templates/global
- "List all enterprise?" -> GET /metadata_templates/enterprise
- "Create a schema?" -> POST /metadata_templates/schema
- "Create a schema#classification?" -> POST /metadata_templates/schema#classifications
- "List all metadata_cascade_policies?" -> GET /metadata_cascade_policies
- "Create a metadata_cascade_policy?" -> POST /metadata_cascade_policies
- "Get metadata_cascade_policy details?" -> GET /metadata_cascade_policies/{metadata_cascade_policy_id}
- "Delete a metadata_cascade_policy?" -> DELETE /metadata_cascade_policies/{metadata_cascade_policy_id}
- "Create a apply?" -> POST /metadata_cascade_policies/{metadata_cascade_policy_id}/apply
- "Create a execute_read?" -> POST /metadata_queries/execute_read
- "Get comment details?" -> GET /comments/{comment_id}
- "Update a comment?" -> PUT /comments/{comment_id}
- "Delete a comment?" -> DELETE /comments/{comment_id}
- "Create a comment?" -> POST /comments
- "Get collaboration details?" -> GET /collaborations/{collaboration_id}
- "Update a collaboration?" -> PUT /collaborations/{collaboration_id}
- "Delete a collaboration?" -> DELETE /collaborations/{collaboration_id}
- "List all collaborations?" -> GET /collaborations
- "Create a collaboration?" -> POST /collaborations
- "Search search?" -> GET /search
- "Create a task?" -> POST /tasks
- "Get task details?" -> GET /tasks/{task_id}
- "Update a task?" -> PUT /tasks/{task_id}
- "Delete a task?" -> DELETE /tasks/{task_id}
- "List all assignments?" -> GET /tasks/{task_id}/assignments
- "Create a task_assignment?" -> POST /task_assignments
- "Get task_assignment details?" -> GET /task_assignments/{task_assignment_id}
- "Update a task_assignment?" -> PUT /task_assignments/{task_assignment_id}
- "Delete a task_assignment?" -> DELETE /task_assignments/{task_assignment_id}
- "List all shared_items?" -> GET /shared_items
- "Get file details?" -> GET /files/{file_id}#get_shared_link
- "Update a file?" -> PUT /files/{file_id}#add_shared_link
- "Update a file?" -> PUT /files/{file_id}#update_shared_link
- "Update a file?" -> PUT /files/{file_id}#remove_shared_link
- "List all shared_items#folders?" -> GET /shared_items#folders
- "Get folder details?" -> GET /folders/{folder_id}#get_shared_link
- "Update a folder?" -> PUT /folders/{folder_id}#add_shared_link
- "Update a folder?" -> PUT /folders/{folder_id}#update_shared_link
- "Update a folder?" -> PUT /folders/{folder_id}#remove_shared_link
- "Create a web_link?" -> POST /web_links
- "Get web_link details?" -> GET /web_links/{web_link_id}
- "Update a web_link?" -> PUT /web_links/{web_link_id}
- "Delete a web_link?" -> DELETE /web_links/{web_link_id}
- "List all trash?" -> GET /web_links/{web_link_id}/trash
- "List all shared_items#web_links?" -> GET /shared_items#web_links
- "Get web_link details?" -> GET /web_links/{web_link_id}#get_shared_link
- "Update a web_link?" -> PUT /web_links/{web_link_id}#add_shared_link
- "Update a web_link?" -> PUT /web_links/{web_link_id}#update_shared_link
- "Update a web_link?" -> PUT /web_links/{web_link_id}#remove_shared_link
- "List all shared_items#app_items?" -> GET /shared_items#app_items
- "List all users?" -> GET /users
- "Create a user?" -> POST /users
- "List all me?" -> GET /users/me
- "Create a terminate_session?" -> POST /users/terminate_sessions
- "Get user details?" -> GET /users/{user_id}
- "Update a user?" -> PUT /users/{user_id}
- "Delete a user?" -> DELETE /users/{user_id}
- "List all avatar?" -> GET /users/{user_id}/avatar
- "Create a avatar?" -> POST /users/{user_id}/avatar
- "List all email_aliases?" -> GET /users/{user_id}/email_aliases
- "Create a email_aliase?" -> POST /users/{user_id}/email_aliases
- "Delete a email_aliase?" -> DELETE /users/{user_id}/email_aliases/{email_alias_id}
- "List all memberships?" -> GET /users/{user_id}/memberships
- "Create a invite?" -> POST /invites
- "Get invite details?" -> GET /invites/{invite_id}
- "List all groups?" -> GET /groups
- "Create a group?" -> POST /groups
- "Create a terminate_session?" -> POST /groups/terminate_sessions
- "Get group details?" -> GET /groups/{group_id}
- "Update a group?" -> PUT /groups/{group_id}
- "Delete a group?" -> DELETE /groups/{group_id}
- "List all memberships?" -> GET /groups/{group_id}/memberships
- "List all collaborations?" -> GET /groups/{group_id}/collaborations
- "Create a group_membership?" -> POST /group_memberships
- "Get group_membership details?" -> GET /group_memberships/{group_membership_id}
- "Update a group_membership?" -> PUT /group_memberships/{group_membership_id}
- "Delete a group_membership?" -> DELETE /group_memberships/{group_membership_id}
- "List all webhooks?" -> GET /webhooks
- "Create a webhook?" -> POST /webhooks
- "Get webhook details?" -> GET /webhooks/{webhook_id}
- "Update a webhook?" -> PUT /webhooks/{webhook_id}
- "Delete a webhook?" -> DELETE /webhooks/{webhook_id}
- "Update a skill_invocation?" -> PUT /skill_invocations/{skill_id}
- "List all events?" -> GET /events
- "List all collections?" -> GET /collections
- "List all items?" -> GET /collections/{collection_id}/items
- "Get collection details?" -> GET /collections/{collection_id}
- "List all recent_items?" -> GET /recent_items
- "List all retention_policies?" -> GET /retention_policies
- "Create a retention_policy?" -> POST /retention_policies
- "Get retention_policy details?" -> GET /retention_policies/{retention_policy_id}
- "Update a retention_policy?" -> PUT /retention_policies/{retention_policy_id}
- "Delete a retention_policy?" -> DELETE /retention_policies/{retention_policy_id}
- "List all assignments?" -> GET /retention_policies/{retention_policy_id}/assignments
- "Create a retention_policy_assignment?" -> POST /retention_policy_assignments
- "Get retention_policy_assignment details?" -> GET /retention_policy_assignments/{retention_policy_assignment_id}
- "Delete a retention_policy_assignment?" -> DELETE /retention_policy_assignments/{retention_policy_assignment_id}
- "List all files_under_retention?" -> GET /retention_policy_assignments/{retention_policy_assignment_id}/files_under_retention
- "List all file_versions_under_retention?" -> GET /retention_policy_assignments/{retention_policy_assignment_id}/file_versions_under_retention
- "List all legal_hold_policies?" -> GET /legal_hold_policies
- "Create a legal_hold_policy?" -> POST /legal_hold_policies
- "Get legal_hold_policy details?" -> GET /legal_hold_policies/{legal_hold_policy_id}
- "Update a legal_hold_policy?" -> PUT /legal_hold_policies/{legal_hold_policy_id}
- "Delete a legal_hold_policy?" -> DELETE /legal_hold_policies/{legal_hold_policy_id}
- "List all legal_hold_policy_assignments?" -> GET /legal_hold_policy_assignments
- "Create a legal_hold_policy_assignment?" -> POST /legal_hold_policy_assignments
- "Get legal_hold_policy_assignment details?" -> GET /legal_hold_policy_assignments/{legal_hold_policy_assignment_id}
- "Delete a legal_hold_policy_assignment?" -> DELETE /legal_hold_policy_assignments/{legal_hold_policy_assignment_id}
- "List all files_on_hold?" -> GET /legal_hold_policy_assignments/{legal_hold_policy_assignment_id}/files_on_hold
- "List all file_version_retentions?" -> GET /file_version_retentions
- "List all file_versions_on_hold?" -> GET /legal_hold_policy_assignments/{legal_hold_policy_assignment_id}/file_versions_on_hold
- "Get file_version_retention details?" -> GET /file_version_retentions/{file_version_retention_id}
- "Get file_version_legal_hold details?" -> GET /file_version_legal_holds/{file_version_legal_hold_id}
- "List all file_version_legal_holds?" -> GET /file_version_legal_holds
- "Get shield_information_barrier details?" -> GET /shield_information_barriers/{shield_information_barrier_id}
- "Create a change_status?" -> POST /shield_information_barriers/change_status
- "List all shield_information_barriers?" -> GET /shield_information_barriers
- "Create a shield_information_barrier?" -> POST /shield_information_barriers
- "List all shield_information_barrier_reports?" -> GET /shield_information_barrier_reports
- "Create a shield_information_barrier_report?" -> POST /shield_information_barrier_reports
- "Get shield_information_barrier_report details?" -> GET /shield_information_barrier_reports/{shield_information_barrier_report_id}
- "Get shield_information_barrier_segment details?" -> GET /shield_information_barrier_segments/{shield_information_barrier_segment_id}
- "Delete a shield_information_barrier_segment?" -> DELETE /shield_information_barrier_segments/{shield_information_barrier_segment_id}
- "Update a shield_information_barrier_segment?" -> PUT /shield_information_barrier_segments/{shield_information_barrier_segment_id}
- "List all shield_information_barrier_segments?" -> GET /shield_information_barrier_segments
- "Create a shield_information_barrier_segment?" -> POST /shield_information_barrier_segments
- "Get shield_information_barrier_segment_member details?" -> GET /shield_information_barrier_segment_members/{shield_information_barrier_segment_member_id}
- "Delete a shield_information_barrier_segment_member?" -> DELETE /shield_information_barrier_segment_members/{shield_information_barrier_segment_member_id}
- "List all shield_information_barrier_segment_members?" -> GET /shield_information_barrier_segment_members
- "Create a shield_information_barrier_segment_member?" -> POST /shield_information_barrier_segment_members
- "Get shield_information_barrier_segment_restriction details?" -> GET /shield_information_barrier_segment_restrictions/{shield_information_barrier_segment_restriction_id}
- "Delete a shield_information_barrier_segment_restriction?" -> DELETE /shield_information_barrier_segment_restrictions/{shield_information_barrier_segment_restriction_id}
- "List all shield_information_barrier_segment_restrictions?" -> GET /shield_information_barrier_segment_restrictions
- "Create a shield_information_barrier_segment_restriction?" -> POST /shield_information_barrier_segment_restrictions
- "Get device_pinner details?" -> GET /device_pinners/{device_pinner_id}
- "Delete a device_pinner?" -> DELETE /device_pinners/{device_pinner_id}
- "List all device_pinners?" -> GET /enterprises/{enterprise_id}/device_pinners
- "List all terms_of_services?" -> GET /terms_of_services
- "Create a terms_of_service?" -> POST /terms_of_services
- "Get terms_of_service details?" -> GET /terms_of_services/{terms_of_service_id}
- "Update a terms_of_service?" -> PUT /terms_of_services/{terms_of_service_id}
- "List all terms_of_service_user_statuses?" -> GET /terms_of_service_user_statuses
- "Create a terms_of_service_user_statuse?" -> POST /terms_of_service_user_statuses
- "Update a terms_of_service_user_statuse?" -> PUT /terms_of_service_user_statuses/{terms_of_service_user_status_id}
- "List all collaboration_whitelist_entries?" -> GET /collaboration_whitelist_entries
- "Create a collaboration_whitelist_entry?" -> POST /collaboration_whitelist_entries
- "Get collaboration_whitelist_entry details?" -> GET /collaboration_whitelist_entries/{collaboration_whitelist_entry_id}
- "Delete a collaboration_whitelist_entry?" -> DELETE /collaboration_whitelist_entries/{collaboration_whitelist_entry_id}
- "List all collaboration_whitelist_exempt_targets?" -> GET /collaboration_whitelist_exempt_targets
- "Create a collaboration_whitelist_exempt_target?" -> POST /collaboration_whitelist_exempt_targets
- "Get collaboration_whitelist_exempt_target details?" -> GET /collaboration_whitelist_exempt_targets/{collaboration_whitelist_exempt_target_id}
- "Delete a collaboration_whitelist_exempt_target?" -> DELETE /collaboration_whitelist_exempt_targets/{collaboration_whitelist_exempt_target_id}
- "List all storage_policies?" -> GET /storage_policies
- "Get storage_policy details?" -> GET /storage_policies/{storage_policy_id}
- "List all storage_policy_assignments?" -> GET /storage_policy_assignments
- "Create a storage_policy_assignment?" -> POST /storage_policy_assignments
- "Get storage_policy_assignment details?" -> GET /storage_policy_assignments/{storage_policy_assignment_id}
- "Update a storage_policy_assignment?" -> PUT /storage_policy_assignments/{storage_policy_assignment_id}
- "Delete a storage_policy_assignment?" -> DELETE /storage_policy_assignments/{storage_policy_assignment_id}
- "Create a zip_download?" -> POST /zip_downloads
- "List all content?" -> GET /zip_downloads/{zip_download_id}/content
- "List all status?" -> GET /zip_downloads/{zip_download_id}/status
- "Create a cancel?" -> POST /sign_requests/{sign_request_id}/cancel
- "Create a resend?" -> POST /sign_requests/{sign_request_id}/resend
- "Get sign_request details?" -> GET /sign_requests/{sign_request_id}
- "List all sign_requests?" -> GET /sign_requests
- "Create a sign_request?" -> POST /sign_requests
- "List all workflows?" -> GET /workflows
- "Create a start?" -> POST /workflows/{workflow_id}/start
- "List all sign_templates?" -> GET /sign_templates
- "Get sign_template details?" -> GET /sign_templates/{template_id}
- "List all slack?" -> GET /integration_mappings/slack
- "Create a slack?" -> POST /integration_mappings/slack
- "Update a slack?" -> PUT /integration_mappings/slack/{integration_mapping_id}
- "Delete a slack?" -> DELETE /integration_mappings/slack/{integration_mapping_id}
- "List all teams?" -> GET /integration_mappings/teams
- "Create a team?" -> POST /integration_mappings/teams
- "Update a team?" -> PUT /integration_mappings/teams/{integration_mapping_id}
- "Delete a team?" -> DELETE /integration_mappings/teams/{integration_mapping_id}
- "Create a ask?" -> POST /ai/ask
- "Create a text_gen?" -> POST /ai/text_gen
- "List all ai_agent_default?" -> GET /ai_agent_default
- "Create a extract?" -> POST /ai/extract
- "Create a extract_structured?" -> POST /ai/extract_structured
- "List all ai_agents?" -> GET /ai_agents
- "Create a ai_agent?" -> POST /ai_agents
- "Update a ai_agent?" -> PUT /ai_agents/{agent_id}
- "Get ai_agent details?" -> GET /ai_agents/{agent_id}
- "Delete a ai_agent?" -> DELETE /ai_agents/{agent_id}
- "Create a metadata_taxonomy?" -> POST /metadata_taxonomies
- "Get metadata_taxonomy details?" -> GET /metadata_taxonomies/{namespace}
- "Get metadata_taxonomy details?" -> GET /metadata_taxonomies/{namespace}/{taxonomy_key}
- "Partially update a metadata_taxonomy?" -> PATCH /metadata_taxonomies/{namespace}/{taxonomy_key}
- "Delete a metadata_taxonomy?" -> DELETE /metadata_taxonomies/{namespace}/{taxonomy_key}
- "Create a level?" -> POST /metadata_taxonomies/{namespace}/{taxonomy_key}/levels
- "Partially update a level?" -> PATCH /metadata_taxonomies/{namespace}/{taxonomy_key}/levels/{level_index}
- "Create a levels:append?" -> POST /metadata_taxonomies/{namespace}/{taxonomy_key}/levels:append
- "Create a levels:trim?" -> POST /metadata_taxonomies/{namespace}/{taxonomy_key}/levels:trim
- "Search nodes?" -> GET /metadata_taxonomies/{namespace}/{taxonomy_key}/nodes
- "Create a node?" -> POST /metadata_taxonomies/{namespace}/{taxonomy_key}/nodes
- "Get node details?" -> GET /metadata_taxonomies/{namespace}/{taxonomy_key}/nodes/{node_id}
- "Partially update a node?" -> PATCH /metadata_taxonomies/{namespace}/{taxonomy_key}/nodes/{node_id}
- "Delete a node?" -> DELETE /metadata_taxonomies/{namespace}/{taxonomy_key}/nodes/{node_id}
- "Search options?" -> GET /metadata_templates/{namespace}/{template_key}/fields/{field_key}/options
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object
- Error responses use types: `bad_request`, `forbidden`, `not_found`, `operation_blocked_temporary`

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
