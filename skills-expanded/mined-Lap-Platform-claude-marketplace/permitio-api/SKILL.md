---
name: permitio-api
description: "Permit.io API skill. Use when working with Permit.io for members, api-key, orgs. Covers 258 endpoints."
version: 1.0.0
generator: lapsh
---

# Permit.io API
API version: 2.0.0

## Auth
Bearer bearer

## Base URL
Not specified.

## Setup
1. Set Authorization header with your Bearer token
2. GET /v2/members/me -- verify access
3. POST /v2/members -- create first members

## Endpoints

258 endpoints across 14 groups. See references/api-spec.lap for full details.

### members
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/members/me | Get the authenticated account member |
| GET | /v2/members | List Organization Members |
| POST | /v2/members | Invite new members |
| DELETE | /v2/members | Remove permission |
| GET | /v2/members/{member_id} | Get Organization Member |
| DELETE | /v2/members/{member_id} | Remove member |
| PATCH | /v2/members/{member_id} | Edit members |

### api-key
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/api-key/{proj_id}/{env_id} | Get Environment Api Key |
| GET | /v2/api-key/scope | Get Api Key Scope |
| GET | /v2/api-key | List Api Keys |
| POST | /v2/api-key | Create Api Key |
| GET | /v2/api-key/{api_key_id} | Get Api Key |
| DELETE | /v2/api-key/{api_key_id} | Delete Api Key |
| POST | /v2/api-key/{api_key_id}/rotate-secret | Rotate API Key |

### orgs
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/orgs | List Organizations |
| POST | /v2/orgs | Create Organization |
| GET | /v2/orgs/{org_id} | Get Organization |
| DELETE | /v2/orgs/{org_id} | Delete Organization |
| PATCH | /v2/orgs/{org_id} | Update Organization |
| GET | /v2/orgs/active/org | Get Active Organization |
| GET | /v2/orgs/{org_id}/stats | Stats Organization |
| GET | /v2/orgs/{org_id}/invites | List Organization Invites |
| POST | /v2/orgs/{org_id}/invites | Invite Members To Organization |
| DELETE | /v2/orgs/{org_id}/invites/{invite_id} | Cancel Invite |

### projects
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/projects | List Projects |
| POST | /v2/projects | Create Project |
| GET | /v2/projects/{proj_id} | Get Project |
| DELETE | /v2/projects/{proj_id} | Delete Project |
| PATCH | /v2/projects/{proj_id} | Update Project |
| GET | /v2/projects/{proj_id}/envs/{env_id}/stats | Stats Environments |
| GET | /v2/projects/{proj_id}/envs | List Environments |
| POST | /v2/projects/{proj_id}/envs | Create Environment |
| GET | /v2/projects/{proj_id}/envs/{env_id} | Get Environment |
| DELETE | /v2/projects/{proj_id}/envs/{env_id} | Delete Environment |
| PATCH | /v2/projects/{proj_id}/envs/{env_id} | Update Environment |
| POST | /v2/projects/{proj_id}/envs/{env_id}/copy | Copy Environment |
| POST | /v2/projects/{proj_id}/envs/{env_id}/copy/async | Copy Environment Async |
| GET | /v2/projects/{proj_id}/envs/{env_id}/copy/async/{task_id}/result | Get Copy Environment Task Result |
| POST | /v2/projects/{proj_id}/envs/{env_id}/test_jwks | Test Jwks By Url |
| GET | /v2/projects/{proj_id}/repos | List Policy Repos |
| POST | /v2/projects/{proj_id}/repos | Create Policy Repo |
| GET | /v2/projects/{proj_id}/repos/active | Get Active Policy Repo |
| PUT | /v2/projects/{proj_id}/repos/disable | Disable Active Policy Repo |
| PUT | /v2/projects/{proj_id}/repos/{repo_id}/activate | Activate Policy Repo |
| GET | /v2/projects/{proj_id}/repos/{repo_id} | Get Policy Repo |
| DELETE | /v2/projects/{proj_id}/repos/{repo_id} | Delete Policy Repo |
| GET | /v2/projects/{proj_id}/{env_id}/opal_scope | Get Scope Config |
| PUT | /v2/projects/{proj_id}/{env_id}/opal_scope | Set Scope Config |
| DELETE | /v2/projects/{proj_id}/{env_id}/opal_scope | Reset Scope Config |

### schema
| Method | Path | Description |
|--------|------|-------------|
| PUT | /v2/schema/{proj_id}/{env_id}/bulk/roles | Bulk Create Or Replace Roles |
| GET | /v2/schema/{proj_id}/{env_id}/condition_sets | List Condition Sets |
| POST | /v2/schema/{proj_id}/{env_id}/condition_sets | Create Condition Set |
| GET | /v2/schema/{proj_id}/{env_id}/condition_sets/{condition_set_id} | Get Condition Set |
| DELETE | /v2/schema/{proj_id}/{env_id}/condition_sets/{condition_set_id} | Delete Condition Set |
| PATCH | /v2/schema/{proj_id}/{env_id}/condition_sets/{condition_set_id} | Update Condition Set |
| GET | /v2/schema/{proj_id}/{env_id}/condition_sets/{condition_set_id}/ancestors | Get Condition Set Ancestors |
| GET | /v2/schema/{proj_id}/{env_id}/condition_sets/{condition_set_id}/descendants | Get Condition Set Descendants |
| POST | /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/roles/{role_id}/implicit_grants | Create Implicit Grant |
| DELETE | /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/roles/{role_id}/implicit_grants | Delete Implicit Grant |
| PUT | /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/roles/{role_id}/implicit_grants/conditions | Update Implicit Grants Conditions |
| GET | /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/action_groups | List Resource Action Groups |
| POST | /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/action_groups | Create Resource Action Group |
| GET | /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/action_groups/{action_group_id} | Get Resource Action Group |
| DELETE | /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/action_groups/{action_group_id} | Delete Resource Action Group |
| PATCH | /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/action_groups/{action_group_id} | Update Resource Action Group |
| GET | /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/actions | List Resource Actions |
| POST | /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/actions | Create Resource Action |
| GET | /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/actions/{action_id} | Get Resource Action |
| DELETE | /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/actions/{action_id} | Delete Resource Action |
| PATCH | /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/actions/{action_id} | Update Resource Action |
| GET | /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/attributes | List Resource Attributes |
| POST | /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/attributes | Create Resource Attribute |
| GET | /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/attributes/{attribute_id} | Get Resource Attribute |
| DELETE | /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/attributes/{attribute_id} | Delete Resource Attribute |
| PATCH | /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/attributes/{attribute_id} | Update Resource Attribute |
| GET | /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/relations | List Resource Relations |
| POST | /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/relations | Create Resource Relation |
| GET | /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/relations/{relation_id} | Get Resource Relation |
| DELETE | /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/relations/{relation_id} | Delete Resource Relation |
| GET | /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/roles | List Resource Roles |
| POST | /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/roles | Create Resource Role |
| GET | /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/roles/{role_id} | Get Resource Role |
| DELETE | /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/roles/{role_id} | Delete Resource Role |
| PATCH | /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/roles/{role_id} | Update Resource Role |
| POST | /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/roles/{role_id}/permissions | Assign Permissions to Role |
| DELETE | /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/roles/{role_id}/permissions | Remove Permissions from Role |
| GET | /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/roles/{role_id}/ancestors | Get Resource Role Ancestors |
| GET | /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/roles/{role_id}/descendants | Get Resource Role Descendants |
| GET | /v2/schema/{proj_id}/{env_id}/resources | List Resources |
| POST | /v2/schema/{proj_id}/{env_id}/resources | Create Resource |
| GET | /v2/schema/{proj_id}/{env_id}/resources/{resource_id} | Get Resource |
| PUT | /v2/schema/{proj_id}/{env_id}/resources/{resource_id} | Replace Resource |
| DELETE | /v2/schema/{proj_id}/{env_id}/resources/{resource_id} | Delete Resource |
| PATCH | /v2/schema/{proj_id}/{env_id}/resources/{resource_id} | Update Resource |
| GET | /v2/schema/{proj_id}/{env_id}/roles | List Roles |
| POST | /v2/schema/{proj_id}/{env_id}/roles | Create Role |
| GET | /v2/schema/{proj_id}/{env_id}/roles/{role_id} | Get Role |
| DELETE | /v2/schema/{proj_id}/{env_id}/roles/{role_id} | Delete Role |
| PATCH | /v2/schema/{proj_id}/{env_id}/roles/{role_id} | Update Role |
| POST | /v2/schema/{proj_id}/{env_id}/roles/{role_id}/permissions | Assign Permissions To Role |
| DELETE | /v2/schema/{proj_id}/{env_id}/roles/{role_id}/permissions | Remove Permissions From Role |
| GET | /v2/schema/{proj_id}/{env_id}/roles/{role_id}/ancestors | Get Role Ancestors |
| GET | /v2/schema/{proj_id}/{env_id}/roles/{role_id}/descendants | Get Role Descendants |
| GET | /v2/schema/{proj_id}/{env_id}/users/attributes | List User Attributes |
| POST | /v2/schema/{proj_id}/{env_id}/users/attributes | Create User Attribute |
| GET | /v2/schema/{proj_id}/{env_id}/users/attributes/{attribute_id} | Get User Attribute |
| DELETE | /v2/schema/{proj_id}/{env_id}/users/attributes/{attribute_id} | Delete User Attribute |
| PATCH | /v2/schema/{proj_id}/{env_id}/users/attributes/{attribute_id} | Update User Attribute |
| GET | /v2/schema/{proj_id}/{env_id}/groups/direct | List Direct Group |
| GET | /v2/schema/{proj_id}/{env_id}/groups/direct/{group_instance_key} | Get Direct Group |
| GET | /v2/schema/{proj_id}/{env_id}/groups/{group_instance_key}/children | List group children (EAP) |
| GET | /v2/schema/{proj_id}/{env_id}/groups/{group_instance_key}/parents | List group parents (EAP) |
| GET | /v2/schema/{proj_id}/{env_id}/groups/{group_instance_key}/users | List group users (EAP) |
| GET | /v2/schema/{proj_id}/{env_id}/groups/{group_instance_key}/roles | List group roles (EAP) |
| POST | /v2/schema/{proj_id}/{env_id}/groups/{group_instance_key}/roles | Assign Role To Group |
| DELETE | /v2/schema/{proj_id}/{env_id}/groups/{group_instance_key}/roles | Remove Role From Group |
| GET | /v2/schema/{proj_id}/{env_id}/groups/{group_instance_key} | Get Group |
| DELETE | /v2/schema/{proj_id}/{env_id}/groups/{group_instance_key} | Delete Group |
| GET | /v2/schema/{proj_id}/{env_id}/groups | List Group |
| POST | /v2/schema/{proj_id}/{env_id}/groups | Create Group |
| PUT | /v2/schema/{proj_id}/{env_id}/groups/{group_instance_key}/users/{user_id} | Assign User To Group |
| DELETE | /v2/schema/{proj_id}/{env_id}/groups/{group_instance_key}/users/{user_id} | Remove User From Group |
| PUT | /v2/schema/{proj_id}/{env_id}/groups/{group_instance_key}/assign_group | Assign Group To Group |
| DELETE | /v2/schema/{proj_id}/{env_id}/groups/{group_instance_key}/assign_group | Remove Group From Group |

### facts
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/facts/{proj_id}/{env_id}/users | List Users |
| POST | /v2/facts/{proj_id}/{env_id}/users | Create User |
| GET | /v2/facts/{proj_id}/{env_id}/users/{user_id} | Get User |
| PUT | /v2/facts/{proj_id}/{env_id}/users/{user_id} | Replace User |
| DELETE | /v2/facts/{proj_id}/{env_id}/users/{user_id} | Delete User |
| PATCH | /v2/facts/{proj_id}/{env_id}/users/{user_id} | Update User |
| POST | /v2/facts/{proj_id}/{env_id}/users/{user_id}/roles | Assign Role To User |
| DELETE | /v2/facts/{proj_id}/{env_id}/users/{user_id}/roles | Unassign Role From User |
| GET | /v2/facts/{proj_id}/{env_id}/tenants/{tenant_id}/users | List Tenant Users |
| POST | /v2/facts/{proj_id}/{env_id}/tenants/{tenant_id}/users | Add User To Tenant |
| GET | /v2/facts/{proj_id}/{env_id}/tenants | List Tenants |
| POST | /v2/facts/{proj_id}/{env_id}/tenants | Create Tenant |
| GET | /v2/facts/{proj_id}/{env_id}/tenants/{tenant_id} | Get Tenant |
| DELETE | /v2/facts/{proj_id}/{env_id}/tenants/{tenant_id} | Delete Tenant |
| PATCH | /v2/facts/{proj_id}/{env_id}/tenants/{tenant_id} | Update Tenant |
| DELETE | /v2/facts/{proj_id}/{env_id}/tenants/{tenant_id}/users/{user_id} | Delete Tenant User |
| GET | /v2/facts/{proj_id}/{env_id}/role_assignments/detailed | List Role Assignments Detailed |
| GET | /v2/facts/{proj_id}/{env_id}/role_assignments | List Role Assignments |
| POST | /v2/facts/{proj_id}/{env_id}/role_assignments | Assign Role |
| DELETE | /v2/facts/{proj_id}/{env_id}/role_assignments | Unassign Role |
| POST | /v2/facts/{proj_id}/{env_id}/role_assignments/bulk | Bulk create role assignments |
| DELETE | /v2/facts/{proj_id}/{env_id}/role_assignments/bulk | Bulk Unassign Role |
| GET | /v2/facts/{proj_id}/{env_id}/set_rules | List Set Permissions |
| POST | /v2/facts/{proj_id}/{env_id}/set_rules | Assign Set Permissions |
| DELETE | /v2/facts/{proj_id}/{env_id}/set_rules | Unassign Set Permissions |
| GET | /v2/facts/{proj_id}/{env_id}/resource_instances/detailed | List Resource Instances Detailed |
| GET | /v2/facts/{proj_id}/{env_id}/resource_instances | List Resource Instances |
| POST | /v2/facts/{proj_id}/{env_id}/resource_instances | Create Resource Instance |
| GET | /v2/facts/{proj_id}/{env_id}/resource_instances/{instance_id} | Get Resource Instance |
| DELETE | /v2/facts/{proj_id}/{env_id}/resource_instances/{instance_id} | Delete Resource Instance |
| PATCH | /v2/facts/{proj_id}/{env_id}/resource_instances/{instance_id} | Update Resource Instance |
| GET | /v2/facts/{proj_id}/{env_id}/proxy_configs | List Proxy Configs |
| POST | /v2/facts/{proj_id}/{env_id}/proxy_configs | Create Proxy Config |
| GET | /v2/facts/{proj_id}/{env_id}/proxy_configs/{proxy_config_id} | Get Proxy Config |
| DELETE | /v2/facts/{proj_id}/{env_id}/proxy_configs/{proxy_config_id} | Delete Proxy Config |
| PATCH | /v2/facts/{proj_id}/{env_id}/proxy_configs/{proxy_config_id} | Update Proxy Config |
| PUT | /v2/facts/{proj_id}/{env_id}/bulk/users | Bulk Replace Users |
| POST | /v2/facts/{proj_id}/{env_id}/bulk/users | Bulk Create Users |
| DELETE | /v2/facts/{proj_id}/{env_id}/bulk/users | Bulk Delete Users |
| POST | /v2/facts/{proj_id}/{env_id}/bulk/tenants | Bulk Create Tenants |
| DELETE | /v2/facts/{proj_id}/{env_id}/bulk/tenants | Bulk Delete Tenants |
| PUT | /v2/facts/{proj_id}/{env_id}/bulk/resource_instances | Bulk Replace Resource Instances |
| DELETE | /v2/facts/{proj_id}/{env_id}/bulk/resource_instances | Bulk Delete Resource Instances |
| GET | /v2/facts/{proj_id}/{env_id}/email_configurations | Get Email Configuration |
| POST | /v2/facts/{proj_id}/{env_id}/email_configurations | Create Or Update Email Configuration |
| POST | /v2/facts/{proj_id}/{env_id}/email_configurations/send_test_email | Send Test Email |
| GET | /v2/facts/{proj_id}/{env_id}/email_templates/ | List Templates |
| GET | /v2/facts/{proj_id}/{env_id}/email_templates/{template_type} | Get Template By Type |
| POST | /v2/facts/{proj_id}/{env_id}/email_templates/{template_type} | Update Template By Type |
| POST | /v2/facts/{proj_id}/{env_id}/email_templates/{template_type}/send_test_email | Send Test Email By Type |
| GET | /v2/facts/{proj_id}/{env_id}/relationship_tuples/detailed | List Relationship Tuples Detailed |
| GET | /v2/facts/{proj_id}/{env_id}/relationship_tuples | List Relationship Tuples |
| POST | /v2/facts/{proj_id}/{env_id}/relationship_tuples | Create Relationship Tuple |
| DELETE | /v2/facts/{proj_id}/{env_id}/relationship_tuples | Delete Relationship Tuple |
| POST | /v2/facts/{proj_id}/{env_id}/relationship_tuples/bulk | Bulk create relationship tuples |
| DELETE | /v2/facts/{proj_id}/{env_id}/relationship_tuples/bulk | Bulk Delete Relationship Tuples |
| GET | /v2/facts/{proj_id}/{env_id}/user_invites | List User Invites |
| POST | /v2/facts/{proj_id}/{env_id}/user_invites | Create User Invite |
| GET | /v2/facts/{proj_id}/{env_id}/user_invites/{user_invite_id} | Get User Invite |
| DELETE | /v2/facts/{proj_id}/{env_id}/user_invites/{user_invite_id} | Delete User Invite |
| PATCH | /v2/facts/{proj_id}/{env_id}/user_invites/{user_invite_id} | Update User Invite |
| POST | /v2/facts/{proj_id}/{env_id}/user_invites/{user_invite_id}/approve | Approve User Invite |
| GET | /v2/facts/{proj_id}/{env_id}/access_requests/{elements_config_id}/user/{user_id}/tenant/{tenant_id} | List Access Requests |
| POST | /v2/facts/{proj_id}/{env_id}/access_requests/{elements_config_id}/user/{user_id}/tenant/{tenant_id} | Create Access Request |
| GET | /v2/facts/{proj_id}/{env_id}/access_requests/{elements_config_id}/user/{user_id}/tenant/{tenant_id}/{access_request_id} | Get Access Request |
| PATCH | /v2/facts/{proj_id}/{env_id}/access_requests/{elements_config_id}/user/{user_id}/tenant/{tenant_id}/{access_request_id}/reviewer | Update Access Request Reviewer |
| PUT | /v2/facts/{proj_id}/{env_id}/access_requests/{elements_config_id}/user/{user_id}/tenant/{tenant_id}/{access_request_id}/approve | Approve Access Request |
| PUT | /v2/facts/{proj_id}/{env_id}/access_requests/{elements_config_id}/user/{user_id}/tenant/{tenant_id}/{access_request_id}/deny | Deny Access Request |
| PUT | /v2/facts/{proj_id}/{env_id}/access_requests/{elements_config_id}/user/{user_id}/tenant/{tenant_id}/{access_request_id}/cancel | Cancel Access Request |

### pdps
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/pdps/{proj_id}/{env_id}/configs | List PDP configurations |
| GET | /v2/pdps/{proj_id}/{env_id}/configs/{pdp_id}/values | Get PDP configuration |
| PUT | /v2/pdps/{proj_id}/{env_id}/configs/{pdp_id}/debug-audit-logs/enable | Enable debug audit logs |
| PUT | /v2/pdps/{proj_id}/{env_id}/configs/{pdp_id}/debug-audit-logs/disable | Disable debug audit logs |
| POST | /v2/pdps/{proj_id}/{env_id}/configs/{pdp_id}/rotate-api-key | Rotate PDP API Key |
| POST | /v2/pdps/{proj_id}/{env_id}/configs/migrate-shards | Migrate PDP Config number of shards |
| GET | /v2/pdps/{proj_id}/{env_id}/audit_logs | List Audit Logs |
| GET | /v2/pdps/{proj_id}/{env_id}/audit_logs/{log_id} | Get detailed audit log |

### elements
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/elements/{proj_id}/{env_id}/config | List Elements Configs |
| POST | /v2/elements/{proj_id}/{env_id}/config | Create Elements Config |
| GET | /v2/elements/{proj_id}/{env_id}/config/{elements_config_id} | Get Elements Config |
| PATCH | /v2/elements/{proj_id}/{env_id}/config/{elements_config_id} | Update Elements Config |
| GET | /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/runtime | Get Elements Config Runtime |
| DELETE | /v2/elements/{proj_id}/{env_id}/{elements_config_id} | Delete Elements Config |
| GET | /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/data/users | List users |
| POST | /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/data/users | Create user |
| DELETE | /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/data/users/{user_id} | Delete user |
| GET | /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/data/user-invites | List all Elements User Invites |
| GET | /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/data/roles | List roles |
| POST | /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/data/users/{user_id}/roles | Assign role to user |
| DELETE | /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/data/users/{user_id}/roles | Unassign role from user |
| POST | /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/data/active | Set Config Active |
| GET | /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/data/audit_logs | List audit logs |
| GET | /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/access_requests | List Access Requests |
| POST | /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/access_requests | Create Access Request |
| GET | /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/access_requests/{access_request_id} | Get Access Request |
| PATCH | /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/access_requests/{access_request_id}/reviewer | Update Access Request Reviewer |
| PUT | /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/access_requests/{access_request_id}/approve | Approve Access Request |
| PUT | /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/access_requests/{access_request_id}/deny | Deny Access Request |
| PUT | /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/access_requests/{access_request_id}/cancel | Cancel Access Request |
| GET | /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/operation_approval | List Operation Approvals |
| POST | /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/operation_approval | Create Operation Approval |
| GET | /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/operation_approval/{operation_approval_id} | Get Operation Approval |
| PATCH | /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/operation_approval/{operation_approval_id}/reviewer | Update Operation Approval Reviewer |
| PUT | /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/operation_approval/{operation_approval_id}/approve | Approve Operation Approval |
| PUT | /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/operation_approval/{operation_approval_id}/deny | Deny Operation Approval |
| PUT | /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/operation_approval/{operation_approval_id}/cancel | Cancel Operation Approval |

### deprecated
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/deprecated/history | List Api Events |
| GET | /v2/deprecated/history/{event_id} | Get Api Event |
| GET | /v2/deprecated/history/{event_id}/request | Get Request Body |
| GET | /v2/deprecated/history/{event_id}/response | Get Response Body |
| GET | /v2/deprecated/activity | List Activity Events |
| GET | /v2/deprecated/activity/types | List Activity Types |

### history
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/history | List Api Events |
| GET | /v2/history/{event_id} | Get Api Event |
| GET | /v2/history/{event_id}/request | Get Request Body |
| GET | /v2/history/{event_id}/response | Get Response Body |

### activity
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/activity | List Activity Events |
| GET | /v2/activity/types | List Activity Types |

### policy_guards
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/policy_guards/scopes | List Policy Guard Scopes |
| POST | /v2/policy_guards/scopes | Create Policy Guard Scope |
| GET | /v2/policy_guards/scopes/{policy_guard_scope_id} | Get Policy Guard Scope |
| DELETE | /v2/policy_guards/scopes/{policy_guard_scope_id} | Delete Policy Guard Scope |
| POST | /v2/policy_guards/scopes/{policy_guard_scope_id}/associate | Associate Policy Guard Scope |
| DELETE | /v2/policy_guards/scopes/{policy_guard_scope_id}/disassociate | Disassociate Policy Guard Scope |
| GET | /v2/policy_guards/scopes/{policy_guard_scope_id}/rules | List Policy Guard Rules |
| POST | /v2/policy_guards/scopes/{policy_guard_scope_id}/rules | Create Policy Guard Rule |
| DELETE | /v2/policy_guards/scopes/{policy_guard_scope_id}/rules | Delete Policy Guard Rule |

### audit-log-replay
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/audit-log-replay | Run the audit log replay |

### internal
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/internal/opal_data/{org_id}/{proj_id}/{env_id}/optimized | Get All Data Optimized |
| GET | /v2/internal/opal_data/{org_id}/{proj_id}/{env_id} | Get All Data |
| GET | /v2/internal/opal_data/{org_id}/{proj_id}/{env_id}/users | Get All Users Data |
| GET | /v2/internal/opal_data/{org_id}/{proj_id}/{env_id}/role_assignments | Get All Role Assignments Data |
| GET | /v2/internal/opal_data/{org_id}/{proj_id}/{env_id}/resource_instances | Get All Resource Instances Data |
| GET | /v2/internal/opal_data/{org_id}/{proj_id}/{env_id}/relationships | Get All Relationships Data |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all me?" -> GET /v2/members/me
- "List all members?" -> GET /v2/members
- "Create a member?" -> POST /v2/members
- "Get member details?" -> GET /v2/members/{member_id}
- "Delete a member?" -> DELETE /v2/members/{member_id}
- "Partially update a member?" -> PATCH /v2/members/{member_id}
- "Get api-key details?" -> GET /v2/api-key/{proj_id}/{env_id}
- "List all scope?" -> GET /v2/api-key/scope
- "List all api-key?" -> GET /v2/api-key
- "Create a api-key?" -> POST /v2/api-key
- "Get api-key details?" -> GET /v2/api-key/{api_key_id}
- "Delete a api-key?" -> DELETE /v2/api-key/{api_key_id}
- "Create a rotate-secret?" -> POST /v2/api-key/{api_key_id}/rotate-secret
- "Search orgs?" -> GET /v2/orgs
- "Create a org?" -> POST /v2/orgs
- "Get org details?" -> GET /v2/orgs/{org_id}
- "Delete a org?" -> DELETE /v2/orgs/{org_id}
- "Partially update a org?" -> PATCH /v2/orgs/{org_id}
- "List all org?" -> GET /v2/orgs/active/org
- "List all stats?" -> GET /v2/orgs/{org_id}/stats
- "List all invites?" -> GET /v2/orgs/{org_id}/invites
- "Create a invite?" -> POST /v2/orgs/{org_id}/invites
- "Delete a invite?" -> DELETE /v2/orgs/{org_id}/invites/{invite_id}
- "List all projects?" -> GET /v2/projects
- "Create a project?" -> POST /v2/projects
- "Get project details?" -> GET /v2/projects/{proj_id}
- "Delete a project?" -> DELETE /v2/projects/{proj_id}
- "Partially update a project?" -> PATCH /v2/projects/{proj_id}
- "List all stats?" -> GET /v2/projects/{proj_id}/envs/{env_id}/stats
- "List all envs?" -> GET /v2/projects/{proj_id}/envs
- "Create a env?" -> POST /v2/projects/{proj_id}/envs
- "Get env details?" -> GET /v2/projects/{proj_id}/envs/{env_id}
- "Delete a env?" -> DELETE /v2/projects/{proj_id}/envs/{env_id}
- "Partially update a env?" -> PATCH /v2/projects/{proj_id}/envs/{env_id}
- "Create a copy?" -> POST /v2/projects/{proj_id}/envs/{env_id}/copy
- "Create a async?" -> POST /v2/projects/{proj_id}/envs/{env_id}/copy/async
- "List all result?" -> GET /v2/projects/{proj_id}/envs/{env_id}/copy/async/{task_id}/result
- "Create a test_jwk?" -> POST /v2/projects/{proj_id}/envs/{env_id}/test_jwks
- "Search condition_sets?" -> GET /v2/schema/{proj_id}/{env_id}/condition_sets
- "Create a condition_set?" -> POST /v2/schema/{proj_id}/{env_id}/condition_sets
- "Get condition_set details?" -> GET /v2/schema/{proj_id}/{env_id}/condition_sets/{condition_set_id}
- "Delete a condition_set?" -> DELETE /v2/schema/{proj_id}/{env_id}/condition_sets/{condition_set_id}
- "Partially update a condition_set?" -> PATCH /v2/schema/{proj_id}/{env_id}/condition_sets/{condition_set_id}
- "List all ancestors?" -> GET /v2/schema/{proj_id}/{env_id}/condition_sets/{condition_set_id}/ancestors
- "List all descendants?" -> GET /v2/schema/{proj_id}/{env_id}/condition_sets/{condition_set_id}/descendants
- "Create a implicit_grant?" -> POST /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/roles/{role_id}/implicit_grants
- "List all action_groups?" -> GET /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/action_groups
- "Create a action_group?" -> POST /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/action_groups
- "Get action_group details?" -> GET /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/action_groups/{action_group_id}
- "Delete a action_group?" -> DELETE /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/action_groups/{action_group_id}
- "Partially update a action_group?" -> PATCH /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/action_groups/{action_group_id}
- "List all actions?" -> GET /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/actions
- "Create a action?" -> POST /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/actions
- "Get action details?" -> GET /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/actions/{action_id}
- "Delete a action?" -> DELETE /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/actions/{action_id}
- "Partially update a action?" -> PATCH /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/actions/{action_id}
- "List all attributes?" -> GET /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/attributes
- "Create a attribute?" -> POST /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/attributes
- "Get attribute details?" -> GET /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/attributes/{attribute_id}
- "Delete a attribute?" -> DELETE /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/attributes/{attribute_id}
- "Partially update a attribute?" -> PATCH /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/attributes/{attribute_id}
- "List all relations?" -> GET /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/relations
- "Create a relation?" -> POST /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/relations
- "Get relation details?" -> GET /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/relations/{relation_id}
- "Delete a relation?" -> DELETE /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/relations/{relation_id}
- "List all roles?" -> GET /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/roles
- "Create a role?" -> POST /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/roles
- "Get role details?" -> GET /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/roles/{role_id}
- "Delete a role?" -> DELETE /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/roles/{role_id}
- "Partially update a role?" -> PATCH /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/roles/{role_id}
- "Create a permission?" -> POST /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/roles/{role_id}/permissions
- "List all ancestors?" -> GET /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/roles/{role_id}/ancestors
- "List all descendants?" -> GET /v2/schema/{proj_id}/{env_id}/resources/{resource_id}/roles/{role_id}/descendants
- "Search resources?" -> GET /v2/schema/{proj_id}/{env_id}/resources
- "Create a resource?" -> POST /v2/schema/{proj_id}/{env_id}/resources
- "Get resource details?" -> GET /v2/schema/{proj_id}/{env_id}/resources/{resource_id}
- "Update a resource?" -> PUT /v2/schema/{proj_id}/{env_id}/resources/{resource_id}
- "Delete a resource?" -> DELETE /v2/schema/{proj_id}/{env_id}/resources/{resource_id}
- "Partially update a resource?" -> PATCH /v2/schema/{proj_id}/{env_id}/resources/{resource_id}
- "Search roles?" -> GET /v2/schema/{proj_id}/{env_id}/roles
- "Create a role?" -> POST /v2/schema/{proj_id}/{env_id}/roles
- "Get role details?" -> GET /v2/schema/{proj_id}/{env_id}/roles/{role_id}
- "Delete a role?" -> DELETE /v2/schema/{proj_id}/{env_id}/roles/{role_id}
- "Partially update a role?" -> PATCH /v2/schema/{proj_id}/{env_id}/roles/{role_id}
- "Create a permission?" -> POST /v2/schema/{proj_id}/{env_id}/roles/{role_id}/permissions
- "List all ancestors?" -> GET /v2/schema/{proj_id}/{env_id}/roles/{role_id}/ancestors
- "List all descendants?" -> GET /v2/schema/{proj_id}/{env_id}/roles/{role_id}/descendants
- "List all attributes?" -> GET /v2/schema/{proj_id}/{env_id}/users/attributes
- "Create a attribute?" -> POST /v2/schema/{proj_id}/{env_id}/users/attributes
- "Get attribute details?" -> GET /v2/schema/{proj_id}/{env_id}/users/attributes/{attribute_id}
- "Delete a attribute?" -> DELETE /v2/schema/{proj_id}/{env_id}/users/attributes/{attribute_id}
- "Partially update a attribute?" -> PATCH /v2/schema/{proj_id}/{env_id}/users/attributes/{attribute_id}
- "Search direct?" -> GET /v2/schema/{proj_id}/{env_id}/groups/direct
- "Get direct details?" -> GET /v2/schema/{proj_id}/{env_id}/groups/direct/{group_instance_key}
- "List all children?" -> GET /v2/schema/{proj_id}/{env_id}/groups/{group_instance_key}/children
- "List all parents?" -> GET /v2/schema/{proj_id}/{env_id}/groups/{group_instance_key}/parents
- "List all users?" -> GET /v2/schema/{proj_id}/{env_id}/groups/{group_instance_key}/users
- "List all roles?" -> GET /v2/schema/{proj_id}/{env_id}/groups/{group_instance_key}/roles
- "Create a role?" -> POST /v2/schema/{proj_id}/{env_id}/groups/{group_instance_key}/roles
- "Get group details?" -> GET /v2/schema/{proj_id}/{env_id}/groups/{group_instance_key}
- "Delete a group?" -> DELETE /v2/schema/{proj_id}/{env_id}/groups/{group_instance_key}
- "Search groups?" -> GET /v2/schema/{proj_id}/{env_id}/groups
- "Create a group?" -> POST /v2/schema/{proj_id}/{env_id}/groups
- "Update a user?" -> PUT /v2/schema/{proj_id}/{env_id}/groups/{group_instance_key}/users/{user_id}
- "Delete a user?" -> DELETE /v2/schema/{proj_id}/{env_id}/groups/{group_instance_key}/users/{user_id}
- "Search users?" -> GET /v2/facts/{proj_id}/{env_id}/users
- "Create a user?" -> POST /v2/facts/{proj_id}/{env_id}/users
- "Get user details?" -> GET /v2/facts/{proj_id}/{env_id}/users/{user_id}
- "Update a user?" -> PUT /v2/facts/{proj_id}/{env_id}/users/{user_id}
- "Delete a user?" -> DELETE /v2/facts/{proj_id}/{env_id}/users/{user_id}
- "Partially update a user?" -> PATCH /v2/facts/{proj_id}/{env_id}/users/{user_id}
- "Create a role?" -> POST /v2/facts/{proj_id}/{env_id}/users/{user_id}/roles
- "Search users?" -> GET /v2/facts/{proj_id}/{env_id}/tenants/{tenant_id}/users
- "Create a user?" -> POST /v2/facts/{proj_id}/{env_id}/tenants/{tenant_id}/users
- "Search tenants?" -> GET /v2/facts/{proj_id}/{env_id}/tenants
- "Create a tenant?" -> POST /v2/facts/{proj_id}/{env_id}/tenants
- "Get tenant details?" -> GET /v2/facts/{proj_id}/{env_id}/tenants/{tenant_id}
- "Delete a tenant?" -> DELETE /v2/facts/{proj_id}/{env_id}/tenants/{tenant_id}
- "Partially update a tenant?" -> PATCH /v2/facts/{proj_id}/{env_id}/tenants/{tenant_id}
- "Delete a user?" -> DELETE /v2/facts/{proj_id}/{env_id}/tenants/{tenant_id}/users/{user_id}
- "List all detailed?" -> GET /v2/facts/{proj_id}/{env_id}/role_assignments/detailed
- "List all role_assignments?" -> GET /v2/facts/{proj_id}/{env_id}/role_assignments
- "Create a role_assignment?" -> POST /v2/facts/{proj_id}/{env_id}/role_assignments
- "Create a bulk?" -> POST /v2/facts/{proj_id}/{env_id}/role_assignments/bulk
- "List all set_rules?" -> GET /v2/facts/{proj_id}/{env_id}/set_rules
- "Create a set_rule?" -> POST /v2/facts/{proj_id}/{env_id}/set_rules
- "Search detailed?" -> GET /v2/facts/{proj_id}/{env_id}/resource_instances/detailed
- "Search resource_instances?" -> GET /v2/facts/{proj_id}/{env_id}/resource_instances
- "Create a resource_instance?" -> POST /v2/facts/{proj_id}/{env_id}/resource_instances
- "Get resource_instance details?" -> GET /v2/facts/{proj_id}/{env_id}/resource_instances/{instance_id}
- "Delete a resource_instance?" -> DELETE /v2/facts/{proj_id}/{env_id}/resource_instances/{instance_id}
- "Partially update a resource_instance?" -> PATCH /v2/facts/{proj_id}/{env_id}/resource_instances/{instance_id}
- "List all proxy_configs?" -> GET /v2/facts/{proj_id}/{env_id}/proxy_configs
- "Create a proxy_config?" -> POST /v2/facts/{proj_id}/{env_id}/proxy_configs
- "Get proxy_config details?" -> GET /v2/facts/{proj_id}/{env_id}/proxy_configs/{proxy_config_id}
- "Delete a proxy_config?" -> DELETE /v2/facts/{proj_id}/{env_id}/proxy_configs/{proxy_config_id}
- "Partially update a proxy_config?" -> PATCH /v2/facts/{proj_id}/{env_id}/proxy_configs/{proxy_config_id}
- "Create a user?" -> POST /v2/facts/{proj_id}/{env_id}/bulk/users
- "Create a tenant?" -> POST /v2/facts/{proj_id}/{env_id}/bulk/tenants
- "List all email_configurations?" -> GET /v2/facts/{proj_id}/{env_id}/email_configurations
- "Create a email_configuration?" -> POST /v2/facts/{proj_id}/{env_id}/email_configurations
- "Create a send_test_email?" -> POST /v2/facts/{proj_id}/{env_id}/email_configurations/send_test_email
- "List all email_templates?" -> GET /v2/facts/{proj_id}/{env_id}/email_templates/
- "Get email_template details?" -> GET /v2/facts/{proj_id}/{env_id}/email_templates/{template_type}
- "Create a send_test_email?" -> POST /v2/facts/{proj_id}/{env_id}/email_templates/{template_type}/send_test_email
- "List all detailed?" -> GET /v2/facts/{proj_id}/{env_id}/relationship_tuples/detailed
- "List all relationship_tuples?" -> GET /v2/facts/{proj_id}/{env_id}/relationship_tuples
- "Create a relationship_tuple?" -> POST /v2/facts/{proj_id}/{env_id}/relationship_tuples
- "Create a bulk?" -> POST /v2/facts/{proj_id}/{env_id}/relationship_tuples/bulk
- "Search user_invites?" -> GET /v2/facts/{proj_id}/{env_id}/user_invites
- "Create a user_invite?" -> POST /v2/facts/{proj_id}/{env_id}/user_invites
- "Get user_invite details?" -> GET /v2/facts/{proj_id}/{env_id}/user_invites/{user_invite_id}
- "Delete a user_invite?" -> DELETE /v2/facts/{proj_id}/{env_id}/user_invites/{user_invite_id}
- "Partially update a user_invite?" -> PATCH /v2/facts/{proj_id}/{env_id}/user_invites/{user_invite_id}
- "Create a approve?" -> POST /v2/facts/{proj_id}/{env_id}/user_invites/{user_invite_id}/approve
- "Get tenant details?" -> GET /v2/facts/{proj_id}/{env_id}/access_requests/{elements_config_id}/user/{user_id}/tenant/{tenant_id}
- "Get tenant details?" -> GET /v2/facts/{proj_id}/{env_id}/access_requests/{elements_config_id}/user/{user_id}/tenant/{tenant_id}/{access_request_id}
- "List all configs?" -> GET /v2/pdps/{proj_id}/{env_id}/configs
- "List all values?" -> GET /v2/pdps/{proj_id}/{env_id}/configs/{pdp_id}/values
- "Create a rotate-api-key?" -> POST /v2/pdps/{proj_id}/{env_id}/configs/{pdp_id}/rotate-api-key
- "Create a migrate-shard?" -> POST /v2/pdps/{proj_id}/{env_id}/configs/migrate-shards
- "Search audit_logs?" -> GET /v2/pdps/{proj_id}/{env_id}/audit_logs
- "Get audit_log details?" -> GET /v2/pdps/{proj_id}/{env_id}/audit_logs/{log_id}
- "List all repos?" -> GET /v2/projects/{proj_id}/repos
- "Create a repo?" -> POST /v2/projects/{proj_id}/repos
- "List all active?" -> GET /v2/projects/{proj_id}/repos/active
- "Get repo details?" -> GET /v2/projects/{proj_id}/repos/{repo_id}
- "Delete a repo?" -> DELETE /v2/projects/{proj_id}/repos/{repo_id}
- "List all config?" -> GET /v2/elements/{proj_id}/{env_id}/config
- "Create a config?" -> POST /v2/elements/{proj_id}/{env_id}/config
- "Get config details?" -> GET /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}
- "Partially update a config?" -> PATCH /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}
- "List all runtime?" -> GET /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/runtime
- "Delete a element?" -> DELETE /v2/elements/{proj_id}/{env_id}/{elements_config_id}
- "Search users?" -> GET /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/data/users
- "Create a user?" -> POST /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/data/users
- "Delete a user?" -> DELETE /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/data/users/{user_id}
- "Search user-invites?" -> GET /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/data/user-invites
- "Search roles?" -> GET /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/data/roles
- "Create a role?" -> POST /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/data/users/{user_id}/roles
- "Create a active?" -> POST /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/data/active
- "Search audit_logs?" -> GET /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/data/audit_logs
- "List all access_requests?" -> GET /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/access_requests
- "Create a access_request?" -> POST /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/access_requests
- "Get access_request details?" -> GET /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/access_requests/{access_request_id}
- "List all operation_approval?" -> GET /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/operation_approval
- "Create a operation_approval?" -> POST /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/operation_approval
- "Get operation_approval details?" -> GET /v2/elements/{proj_id}/{env_id}/config/{elements_config_id}/operation_approval/{operation_approval_id}
- "List all history?" -> GET /v2/deprecated/history
- "Get history details?" -> GET /v2/deprecated/history/{event_id}
- "List all request?" -> GET /v2/deprecated/history/{event_id}/request
- "List all response?" -> GET /v2/deprecated/history/{event_id}/response
- "List all history?" -> GET /v2/history
- "Get history details?" -> GET /v2/history/{event_id}
- "List all request?" -> GET /v2/history/{event_id}/request
- "List all response?" -> GET /v2/history/{event_id}/response
- "List all activity?" -> GET /v2/activity
- "List all types?" -> GET /v2/activity/types
- "List all activity?" -> GET /v2/deprecated/activity
- "List all types?" -> GET /v2/deprecated/activity/types
- "List all scopes?" -> GET /v2/policy_guards/scopes
- "Create a scope?" -> POST /v2/policy_guards/scopes
- "Get scope details?" -> GET /v2/policy_guards/scopes/{policy_guard_scope_id}
- "Delete a scope?" -> DELETE /v2/policy_guards/scopes/{policy_guard_scope_id}
- "Create a associate?" -> POST /v2/policy_guards/scopes/{policy_guard_scope_id}/associate
- "List all rules?" -> GET /v2/policy_guards/scopes/{policy_guard_scope_id}/rules
- "Create a rule?" -> POST /v2/policy_guards/scopes/{policy_guard_scope_id}/rules
- "List all opal_scope?" -> GET /v2/projects/{proj_id}/{env_id}/opal_scope
- "Create a audit-log-replay?" -> POST /v2/audit-log-replay
- "List all optimized?" -> GET /v2/internal/opal_data/{org_id}/{proj_id}/{env_id}/optimized
- "Get opal_data details?" -> GET /v2/internal/opal_data/{org_id}/{proj_id}/{env_id}
- "List all users?" -> GET /v2/internal/opal_data/{org_id}/{proj_id}/{env_id}/users
- "List all role_assignments?" -> GET /v2/internal/opal_data/{org_id}/{proj_id}/{env_id}/role_assignments
- "List all resource_instances?" -> GET /v2/internal/opal_data/{org_id}/{proj_id}/{env_id}/resource_instances
- "List all relationships?" -> GET /v2/internal/opal_data/{org_id}/{proj_id}/{env_id}/relationships
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
