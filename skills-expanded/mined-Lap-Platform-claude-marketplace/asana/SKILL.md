---
name: asana
description: "Asana API skill. Use when working with Asana for access_requests, allocations, attachments. Covers 222 endpoints."
version: 1.0.0
generator: lapsh
---

# Asana
API version: 1.0

## Auth
Bearer bearer | OAuth2

## Base URL
https://app.asana.com/api/1.0

## Setup
1. Set Authorization header with your Bearer token
2. GET /access_requests -- verify access
3. POST /access_requests -- create first access_requests

## Endpoints

222 endpoints across 41 groups. See references/api-spec.lap for full details.

### access_requests
| Method | Path | Description |
|--------|------|-------------|
| GET | /access_requests | Get access requests |
| POST | /access_requests | Create an access request |
| POST | /access_requests/{access_request_gid}/approve | Approve an access request |
| POST | /access_requests/{access_request_gid}/reject | Reject an access request |

### allocations
| Method | Path | Description |
|--------|------|-------------|
| GET | /allocations/{allocation_gid} | Get an allocation |
| PUT | /allocations/{allocation_gid} | Update an allocation |
| DELETE | /allocations/{allocation_gid} | Delete an allocation |
| GET | /allocations | Get multiple allocations |
| POST | /allocations | Create an allocation |

### attachments
| Method | Path | Description |
|--------|------|-------------|
| GET | /attachments/{attachment_gid} | Get an attachment |
| DELETE | /attachments/{attachment_gid} | Delete an attachment |
| GET | /attachments | Get attachments from an object |
| POST | /attachments | Upload an attachment |

### workspaces
| Method | Path | Description |
|--------|------|-------------|
| GET | /workspaces/{workspace_gid}/audit_log_events | Get audit log events |
| GET | /workspaces/{workspace_gid}/custom_fields | Get a workspace's custom fields |
| GET | /workspaces/{workspace_gid}/projects | Get all projects in a workspace |
| POST | /workspaces/{workspace_gid}/projects | Create a project in a workspace |
| GET | /workspaces/{workspace_gid}/tags | Get tags in a workspace |
| POST | /workspaces/{workspace_gid}/tags | Create a tag in a workspace |
| GET | /workspaces/{workspace_gid}/tasks/custom_id/{custom_id} | Get a task for a given custom ID |
| GET | /workspaces/{workspace_gid}/tasks/search | Search tasks in a workspace |
| GET | /workspaces/{workspace_gid}/teams | Get teams in a workspace |
| GET | /workspaces/{workspace_gid}/typeahead | Get objects via typeahead |
| GET | /workspaces/{workspace_gid}/users | Get users in a workspace or organization |
| GET | /workspaces/{workspace_gid}/users/{user_gid} | Get a user in a workspace or organization |
| PUT | /workspaces/{workspace_gid}/users/{user_gid} | Update a user in a workspace or organization |
| GET | /workspaces/{workspace_gid}/workspace_memberships | Get the workspace memberships for a workspace |
| GET | /workspaces | Get multiple workspaces |
| GET | /workspaces/{workspace_gid} | Get a workspace |
| PUT | /workspaces/{workspace_gid} | Update a workspace |
| POST | /workspaces/{workspace_gid}/addUser | Add a user to a workspace or organization |
| POST | /workspaces/{workspace_gid}/removeUser | Remove a user from a workspace or organization |
| GET | /workspaces/{workspace_gid}/events | Get workspace events |

### batch
| Method | Path | Description |
|--------|------|-------------|
| POST | /batch | Submit parallel requests |

### budgets
| Method | Path | Description |
|--------|------|-------------|
| GET | /budgets | Get all budgets |
| POST | /budgets | Create a budget |
| GET | /budgets/{budget_gid} | Get a budget |
| PUT | /budgets/{budget_gid} | Update a budget |
| DELETE | /budgets/{budget_gid} | Delete a budget |

### projects
| Method | Path | Description |
|--------|------|-------------|
| GET | /projects/{project_gid}/custom_field_settings | Get a project's custom fields |
| POST | /projects/{project_gid}/project_briefs | Create a project brief |
| GET | /projects/{project_gid}/project_memberships | Get memberships from a project |
| GET | /projects/{project_gid}/project_statuses | Get statuses from a project |
| POST | /projects/{project_gid}/project_statuses | Create a project status |
| GET | /projects | Get multiple projects |
| POST | /projects | Create a project |
| GET | /projects/{project_gid} | Get a project |
| PUT | /projects/{project_gid} | Update a project |
| DELETE | /projects/{project_gid} | Delete a project |
| POST | /projects/{project_gid}/duplicate | Duplicate a project |
| POST | /projects/{project_gid}/addCustomFieldSetting | Add a custom field to a project |
| POST | /projects/{project_gid}/removeCustomFieldSetting | Remove a custom field from a project |
| GET | /projects/{project_gid}/task_counts | Get task count of a project |
| POST | /projects/{project_gid}/addMembers | Add users to a project |
| POST | /projects/{project_gid}/removeMembers | Remove users from a project |
| POST | /projects/{project_gid}/addFollowers | Add followers to a project |
| POST | /projects/{project_gid}/removeFollowers | Remove followers from a project |
| POST | /projects/{project_gid}/saveAsTemplate | Create a project template from a project |
| GET | /projects/{project_gid}/sections | Get sections in a project |
| POST | /projects/{project_gid}/sections | Create a section in a project |
| POST | /projects/{project_gid}/sections/insert | Move or Insert sections |
| GET | /projects/{project_gid}/tasks | Get tasks from a project |

### portfolios
| Method | Path | Description |
|--------|------|-------------|
| GET | /portfolios/{portfolio_gid}/custom_field_settings | Get a portfolio's custom fields |
| GET | /portfolios/{portfolio_gid}/portfolio_memberships | Get memberships from a portfolio |
| GET | /portfolios | Get multiple portfolios |
| POST | /portfolios | Create a portfolio |
| GET | /portfolios/{portfolio_gid} | Get a portfolio |
| PUT | /portfolios/{portfolio_gid} | Update a portfolio |
| DELETE | /portfolios/{portfolio_gid} | Delete a portfolio |
| GET | /portfolios/{portfolio_gid}/items | Get portfolio items |
| POST | /portfolios/{portfolio_gid}/addItem | Add a portfolio item |
| POST | /portfolios/{portfolio_gid}/removeItem | Remove a portfolio item |
| POST | /portfolios/{portfolio_gid}/addCustomFieldSetting | Add a custom field to a portfolio |
| POST | /portfolios/{portfolio_gid}/removeCustomFieldSetting | Remove a custom field from a portfolio |
| POST | /portfolios/{portfolio_gid}/addMembers | Add users to a portfolio |
| POST | /portfolios/{portfolio_gid}/removeMembers | Remove users from a portfolio |

### goals
| Method | Path | Description |
|--------|------|-------------|
| GET | /goals/{goal_gid}/custom_field_settings | Get a goal's custom fields |
| POST | /goals/{goal_gid}/addSupportingRelationship | Add a supporting goal relationship |
| POST | /goals/{goal_gid}/removeSupportingRelationship | Removes a supporting goal relationship |
| GET | /goals/{goal_gid} | Get a goal |
| PUT | /goals/{goal_gid} | Update a goal |
| DELETE | /goals/{goal_gid} | Delete a goal |
| GET | /goals | Get goals |
| POST | /goals | Create a goal |
| POST | /goals/{goal_gid}/setMetric | Create a goal metric |
| POST | /goals/{goal_gid}/setMetricCurrentValue | Update a goal metric |
| POST | /goals/{goal_gid}/addFollowers | Add a collaborator to a goal |
| POST | /goals/{goal_gid}/removeFollowers | Remove a collaborator from a goal |
| GET | /goals/{goal_gid}/parentGoals | Get parent goals from a goal |
| POST | /goals/{goal_gid}/addCustomFieldSetting | Add a custom field to a goal |
| POST | /goals/{goal_gid}/removeCustomFieldSetting | Remove a custom field from a goal |

### teams
| Method | Path | Description |
|--------|------|-------------|
| GET | /teams/{team_gid}/custom_field_settings | Get a team's custom fields |
| GET | /teams/{team_gid}/project_templates | Get a team's project templates |
| GET | /teams/{team_gid}/projects | Get a team's projects |
| POST | /teams/{team_gid}/projects | Create a project in a team |
| GET | /teams/{team_gid}/team_memberships | Get memberships from a team |
| POST | /teams | Create a team |
| GET | /teams/{team_gid} | Get a team |
| PUT | /teams/{team_gid} | Update a team |
| POST | /teams/{team_gid}/addUser | Add a user to a team |
| POST | /teams/{team_gid}/removeUser | Remove a user from a team |
| GET | /teams/{team_gid}/users | Get users in a team |

### custom_fields
| Method | Path | Description |
|--------|------|-------------|
| POST | /custom_fields | Create a custom field |
| GET | /custom_fields/{custom_field_gid} | Get a custom field |
| PUT | /custom_fields/{custom_field_gid} | Update a custom field |
| DELETE | /custom_fields/{custom_field_gid} | Delete a custom field |
| POST | /custom_fields/{custom_field_gid}/enum_options | Create an enum option |
| POST | /custom_fields/{custom_field_gid}/enum_options/insert | Reorder a custom field's enum |

### enum_options
| Method | Path | Description |
|--------|------|-------------|
| PUT | /enum_options/{enum_option_gid} | Update an enum option |

### custom_types
| Method | Path | Description |
|--------|------|-------------|
| GET | /custom_types | Get all custom types associated with an object |
| GET | /custom_types/{custom_type_gid} | Get a custom type |

### events
| Method | Path | Description |
|--------|------|-------------|
| GET | /events | Get events on a resource |

### exports
| Method | Path | Description |
|--------|------|-------------|
| POST | /exports/graph | Initiate a graph export |
| POST | /exports/resource | Initiate a resource export |

### goal_relationships
| Method | Path | Description |
|--------|------|-------------|
| GET | /goal_relationships/{goal_relationship_gid} | Get a goal relationship |
| PUT | /goal_relationships/{goal_relationship_gid} | Update a goal relationship |
| GET | /goal_relationships | Get goal relationships |

### jobs
| Method | Path | Description |
|--------|------|-------------|
| GET | /jobs/{job_gid} | Get a job by id |

### memberships
| Method | Path | Description |
|--------|------|-------------|
| GET | /memberships | Get multiple memberships |
| POST | /memberships | Create a membership |
| GET | /memberships/{membership_gid} | Get a membership |
| PUT | /memberships/{membership_gid} | Update a membership |
| DELETE | /memberships/{membership_gid} | Delete a membership |

### organization_exports
| Method | Path | Description |
|--------|------|-------------|
| POST | /organization_exports | Create an organization export request |
| GET | /organization_exports/{organization_export_gid} | Get details on an org export request |

### portfolio_memberships
| Method | Path | Description |
|--------|------|-------------|
| GET | /portfolio_memberships | Get multiple portfolio memberships |
| GET | /portfolio_memberships/{portfolio_membership_gid} | Get a portfolio membership |

### project_briefs
| Method | Path | Description |
|--------|------|-------------|
| GET | /project_briefs/{project_brief_gid} | Get a project brief |
| PUT | /project_briefs/{project_brief_gid} | Update a project brief |
| DELETE | /project_briefs/{project_brief_gid} | Delete a project brief |

### project_memberships
| Method | Path | Description |
|--------|------|-------------|
| GET | /project_memberships/{project_membership_gid} | Get a project membership |

### project_statuses
| Method | Path | Description |
|--------|------|-------------|
| GET | /project_statuses/{project_status_gid} | Get a project status |
| DELETE | /project_statuses/{project_status_gid} | Delete a project status |

### project_templates
| Method | Path | Description |
|--------|------|-------------|
| GET | /project_templates/{project_template_gid} | Get a project template |
| DELETE | /project_templates/{project_template_gid} | Delete a project template |
| GET | /project_templates | Get multiple project templates |
| POST | /project_templates/{project_template_gid}/instantiateProject | Instantiate a project from a project template |

### tasks
| Method | Path | Description |
|--------|------|-------------|
| GET | /tasks/{task_gid}/projects | Get projects a task is in |
| GET | /tasks/{task_gid}/stories | Get stories from a task |
| POST | /tasks/{task_gid}/stories | Create a story on a task |
| GET | /tasks/{task_gid}/tags | Get a task's tags |
| GET | /tasks | Get multiple tasks |
| POST | /tasks | Create a task |
| GET | /tasks/{task_gid} | Get a task |
| PUT | /tasks/{task_gid} | Update a task |
| DELETE | /tasks/{task_gid} | Delete a task |
| POST | /tasks/{task_gid}/duplicate | Duplicate a task |
| GET | /tasks/{task_gid}/subtasks | Get subtasks from a task |
| POST | /tasks/{task_gid}/subtasks | Create a subtask |
| POST | /tasks/{task_gid}/setParent | Set the parent of a task |
| GET | /tasks/{task_gid}/dependencies | Get dependencies from a task |
| POST | /tasks/{task_gid}/addDependencies | Set dependencies for a task |
| POST | /tasks/{task_gid}/removeDependencies | Unlink dependencies from a task |
| GET | /tasks/{task_gid}/dependents | Get dependents from a task |
| POST | /tasks/{task_gid}/addDependents | Set dependents for a task |
| POST | /tasks/{task_gid}/removeDependents | Unlink dependents from a task |
| POST | /tasks/{task_gid}/addProject | Add a project to a task |
| POST | /tasks/{task_gid}/removeProject | Remove a project from a task |
| POST | /tasks/{task_gid}/addTag | Add a tag to a task |
| POST | /tasks/{task_gid}/removeTag | Remove a tag from a task |
| POST | /tasks/{task_gid}/addFollowers | Add followers to a task |
| POST | /tasks/{task_gid}/removeFollowers | Remove followers from a task |
| GET | /tasks/{task_gid}/time_tracking_entries | Get time tracking entries for a task |
| POST | /tasks/{task_gid}/time_tracking_entries | Create a time tracking entry |

### rates
| Method | Path | Description |
|--------|------|-------------|
| GET | /rates | Get multiple rates |
| POST | /rates | Create a rate |
| GET | /rates/{rate_gid} | Get a rate |
| PUT | /rates/{rate_gid} | Update a rate |
| DELETE | /rates/{rate_gid} | Delete a rate |

### reactions
| Method | Path | Description |
|--------|------|-------------|
| GET | /reactions | Get reactions with an emoji base on an object. |

### roles
| Method | Path | Description |
|--------|------|-------------|
| GET | /roles | Get multiple roles |
| POST | /roles | Create a role |
| GET | /roles/{role_gid} | Get a role |
| PUT | /roles/{role_gid} | Update a role |
| DELETE | /roles/{role_gid} | Delete a role |

### rule_triggers
| Method | Path | Description |
|--------|------|-------------|
| POST | /rule_triggers/{rule_trigger_gid}/run | Trigger a rule |

### sections
| Method | Path | Description |
|--------|------|-------------|
| GET | /sections/{section_gid} | Get a section |
| PUT | /sections/{section_gid} | Update a section |
| DELETE | /sections/{section_gid} | Delete a section |
| POST | /sections/{section_gid}/addTask | Add task to section |
| GET | /sections/{section_gid}/tasks | Get tasks from a section |

### status_updates
| Method | Path | Description |
|--------|------|-------------|
| GET | /status_updates/{status_update_gid} | Get a status update |
| DELETE | /status_updates/{status_update_gid} | Delete a status update |
| GET | /status_updates | Get status updates from an object |
| POST | /status_updates | Create a status update |

### stories
| Method | Path | Description |
|--------|------|-------------|
| GET | /stories/{story_gid} | Get a story |
| PUT | /stories/{story_gid} | Update a story |
| DELETE | /stories/{story_gid} | Delete a story |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags | Get multiple tags |
| POST | /tags | Create a tag |
| GET | /tags/{tag_gid} | Get a tag |
| PUT | /tags/{tag_gid} | Update a tag |
| DELETE | /tags/{tag_gid} | Delete a tag |
| GET | /tags/{tag_gid}/tasks | Get tasks from a tag |

### task_templates
| Method | Path | Description |
|--------|------|-------------|
| GET | /task_templates | Get multiple task templates |
| GET | /task_templates/{task_template_gid} | Get a task template |
| DELETE | /task_templates/{task_template_gid} | Delete a task template |
| POST | /task_templates/{task_template_gid}/instantiateTask | Instantiate a task from a task template |

### user_task_lists
| Method | Path | Description |
|--------|------|-------------|
| GET | /user_task_lists/{user_task_list_gid}/tasks | Get tasks from a user task list |
| GET | /user_task_lists/{user_task_list_gid} | Get a user task list |

### team_memberships
| Method | Path | Description |
|--------|------|-------------|
| GET | /team_memberships/{team_membership_gid} | Get a team membership |
| GET | /team_memberships | Get team memberships |

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /users/{user_gid}/team_memberships | Get memberships from a user |
| GET | /users/{user_gid}/teams | Get teams for a user |
| GET | /users/{user_gid}/user_task_list | Get a user's task list |
| GET | /users | Get multiple users |
| GET | /users/{user_gid} | Get a user |
| PUT | /users/{user_gid} | Update a user |
| GET | /users/{user_gid}/favorites | Get a user's favorites |
| GET | /users/{user_gid}/workspace_memberships | Get workspace memberships for a user |

### time_periods
| Method | Path | Description |
|--------|------|-------------|
| GET | /time_periods/{time_period_gid} | Get a time period |
| GET | /time_periods | Get time periods |

### time_tracking_entries
| Method | Path | Description |
|--------|------|-------------|
| GET | /time_tracking_entries/{time_tracking_entry_gid} | Get a time tracking entry |
| PUT | /time_tracking_entries/{time_tracking_entry_gid} | Update a time tracking entry |
| DELETE | /time_tracking_entries/{time_tracking_entry_gid} | Delete a time tracking entry |
| GET | /time_tracking_entries | Get multiple time tracking entries |

### webhooks
| Method | Path | Description |
|--------|------|-------------|
| GET | /webhooks | Get multiple webhooks |
| POST | /webhooks | Establish a webhook |
| GET | /webhooks/{webhook_gid} | Get a webhook |
| PUT | /webhooks/{webhook_gid} | Update a webhook |
| DELETE | /webhooks/{webhook_gid} | Delete a webhook |

### workspace_memberships
| Method | Path | Description |
|--------|------|-------------|
| GET | /workspace_memberships/{workspace_membership_gid} | Get a workspace membership |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all access_requests?" -> GET /access_requests
- "Create a access_request?" -> POST /access_requests
- "Create a approve?" -> POST /access_requests/{access_request_gid}/approve
- "Create a reject?" -> POST /access_requests/{access_request_gid}/reject
- "Get allocation details?" -> GET /allocations/{allocation_gid}
- "Update a allocation?" -> PUT /allocations/{allocation_gid}
- "Delete a allocation?" -> DELETE /allocations/{allocation_gid}
- "List all allocations?" -> GET /allocations
- "Create a allocation?" -> POST /allocations
- "Get attachment details?" -> GET /attachments/{attachment_gid}
- "Delete a attachment?" -> DELETE /attachments/{attachment_gid}
- "List all attachments?" -> GET /attachments
- "Create a attachment?" -> POST /attachments
- "List all audit_log_events?" -> GET /workspaces/{workspace_gid}/audit_log_events
- "Create a batch?" -> POST /batch
- "List all budgets?" -> GET /budgets
- "Create a budget?" -> POST /budgets
- "Get budget details?" -> GET /budgets/{budget_gid}
- "Update a budget?" -> PUT /budgets/{budget_gid}
- "Delete a budget?" -> DELETE /budgets/{budget_gid}
- "List all custom_field_settings?" -> GET /projects/{project_gid}/custom_field_settings
- "List all custom_field_settings?" -> GET /portfolios/{portfolio_gid}/custom_field_settings
- "List all custom_field_settings?" -> GET /goals/{goal_gid}/custom_field_settings
- "List all custom_field_settings?" -> GET /teams/{team_gid}/custom_field_settings
- "Create a custom_field?" -> POST /custom_fields
- "Get custom_field details?" -> GET /custom_fields/{custom_field_gid}
- "Update a custom_field?" -> PUT /custom_fields/{custom_field_gid}
- "Delete a custom_field?" -> DELETE /custom_fields/{custom_field_gid}
- "List all custom_fields?" -> GET /workspaces/{workspace_gid}/custom_fields
- "Create a enum_option?" -> POST /custom_fields/{custom_field_gid}/enum_options
- "Create a insert?" -> POST /custom_fields/{custom_field_gid}/enum_options/insert
- "Update a enum_option?" -> PUT /enum_options/{enum_option_gid}
- "List all custom_types?" -> GET /custom_types
- "Get custom_type details?" -> GET /custom_types/{custom_type_gid}
- "List all events?" -> GET /events
- "Create a graph?" -> POST /exports/graph
- "Create a resource?" -> POST /exports/resource
- "Get goal_relationship details?" -> GET /goal_relationships/{goal_relationship_gid}
- "Update a goal_relationship?" -> PUT /goal_relationships/{goal_relationship_gid}
- "List all goal_relationships?" -> GET /goal_relationships
- "Create a addSupportingRelationship?" -> POST /goals/{goal_gid}/addSupportingRelationship
- "Create a removeSupportingRelationship?" -> POST /goals/{goal_gid}/removeSupportingRelationship
- "Get goal details?" -> GET /goals/{goal_gid}
- "Update a goal?" -> PUT /goals/{goal_gid}
- "Delete a goal?" -> DELETE /goals/{goal_gid}
- "List all goals?" -> GET /goals
- "Create a goal?" -> POST /goals
- "Create a setMetric?" -> POST /goals/{goal_gid}/setMetric
- "Create a setMetricCurrentValue?" -> POST /goals/{goal_gid}/setMetricCurrentValue
- "Create a addFollower?" -> POST /goals/{goal_gid}/addFollowers
- "Create a removeFollower?" -> POST /goals/{goal_gid}/removeFollowers
- "List all parentGoals?" -> GET /goals/{goal_gid}/parentGoals
- "Create a addCustomFieldSetting?" -> POST /goals/{goal_gid}/addCustomFieldSetting
- "Create a removeCustomFieldSetting?" -> POST /goals/{goal_gid}/removeCustomFieldSetting
- "Get job details?" -> GET /jobs/{job_gid}
- "List all memberships?" -> GET /memberships
- "Create a membership?" -> POST /memberships
- "Get membership details?" -> GET /memberships/{membership_gid}
- "Update a membership?" -> PUT /memberships/{membership_gid}
- "Delete a membership?" -> DELETE /memberships/{membership_gid}
- "Create a organization_export?" -> POST /organization_exports
- "Get organization_export details?" -> GET /organization_exports/{organization_export_gid}
- "List all portfolio_memberships?" -> GET /portfolio_memberships
- "Get portfolio_membership details?" -> GET /portfolio_memberships/{portfolio_membership_gid}
- "List all portfolio_memberships?" -> GET /portfolios/{portfolio_gid}/portfolio_memberships
- "List all portfolios?" -> GET /portfolios
- "Create a portfolio?" -> POST /portfolios
- "Get portfolio details?" -> GET /portfolios/{portfolio_gid}
- "Update a portfolio?" -> PUT /portfolios/{portfolio_gid}
- "Delete a portfolio?" -> DELETE /portfolios/{portfolio_gid}
- "List all items?" -> GET /portfolios/{portfolio_gid}/items
- "Create a addItem?" -> POST /portfolios/{portfolio_gid}/addItem
- "Create a removeItem?" -> POST /portfolios/{portfolio_gid}/removeItem
- "Create a addCustomFieldSetting?" -> POST /portfolios/{portfolio_gid}/addCustomFieldSetting
- "Create a removeCustomFieldSetting?" -> POST /portfolios/{portfolio_gid}/removeCustomFieldSetting
- "Create a addMember?" -> POST /portfolios/{portfolio_gid}/addMembers
- "Create a removeMember?" -> POST /portfolios/{portfolio_gid}/removeMembers
- "Get project_brief details?" -> GET /project_briefs/{project_brief_gid}
- "Update a project_brief?" -> PUT /project_briefs/{project_brief_gid}
- "Delete a project_brief?" -> DELETE /project_briefs/{project_brief_gid}
- "Create a project_brief?" -> POST /projects/{project_gid}/project_briefs
- "Get project_membership details?" -> GET /project_memberships/{project_membership_gid}
- "List all project_memberships?" -> GET /projects/{project_gid}/project_memberships
- "Get project_statuse details?" -> GET /project_statuses/{project_status_gid}
- "Delete a project_statuse?" -> DELETE /project_statuses/{project_status_gid}
- "List all project_statuses?" -> GET /projects/{project_gid}/project_statuses
- "Create a project_statuse?" -> POST /projects/{project_gid}/project_statuses
- "Get project_template details?" -> GET /project_templates/{project_template_gid}
- "Delete a project_template?" -> DELETE /project_templates/{project_template_gid}
- "List all project_templates?" -> GET /project_templates
- "List all project_templates?" -> GET /teams/{team_gid}/project_templates
- "Create a instantiateProject?" -> POST /project_templates/{project_template_gid}/instantiateProject
- "List all projects?" -> GET /projects
- "Create a project?" -> POST /projects
- "Get project details?" -> GET /projects/{project_gid}
- "Update a project?" -> PUT /projects/{project_gid}
- "Delete a project?" -> DELETE /projects/{project_gid}
- "Create a duplicate?" -> POST /projects/{project_gid}/duplicate
- "List all projects?" -> GET /tasks/{task_gid}/projects
- "List all projects?" -> GET /teams/{team_gid}/projects
- "Create a project?" -> POST /teams/{team_gid}/projects
- "List all projects?" -> GET /workspaces/{workspace_gid}/projects
- "Create a project?" -> POST /workspaces/{workspace_gid}/projects
- "Create a addCustomFieldSetting?" -> POST /projects/{project_gid}/addCustomFieldSetting
- "Create a removeCustomFieldSetting?" -> POST /projects/{project_gid}/removeCustomFieldSetting
- "List all task_counts?" -> GET /projects/{project_gid}/task_counts
- "Create a addMember?" -> POST /projects/{project_gid}/addMembers
- "Create a removeMember?" -> POST /projects/{project_gid}/removeMembers
- "Create a addFollower?" -> POST /projects/{project_gid}/addFollowers
- "Create a removeFollower?" -> POST /projects/{project_gid}/removeFollowers
- "Create a saveAsTemplate?" -> POST /projects/{project_gid}/saveAsTemplate
- "List all rates?" -> GET /rates
- "Create a rate?" -> POST /rates
- "Get rate details?" -> GET /rates/{rate_gid}
- "Update a rate?" -> PUT /rates/{rate_gid}
- "Delete a rate?" -> DELETE /rates/{rate_gid}
- "List all reactions?" -> GET /reactions
- "List all roles?" -> GET /roles
- "Create a role?" -> POST /roles
- "Get role details?" -> GET /roles/{role_gid}
- "Update a role?" -> PUT /roles/{role_gid}
- "Delete a role?" -> DELETE /roles/{role_gid}
- "Create a run?" -> POST /rule_triggers/{rule_trigger_gid}/run
- "Get section details?" -> GET /sections/{section_gid}
- "Update a section?" -> PUT /sections/{section_gid}
- "Delete a section?" -> DELETE /sections/{section_gid}
- "List all sections?" -> GET /projects/{project_gid}/sections
- "Create a section?" -> POST /projects/{project_gid}/sections
- "Create a addTask?" -> POST /sections/{section_gid}/addTask
- "Create a insert?" -> POST /projects/{project_gid}/sections/insert
- "Get status_update details?" -> GET /status_updates/{status_update_gid}
- "Delete a status_update?" -> DELETE /status_updates/{status_update_gid}
- "List all status_updates?" -> GET /status_updates
- "Create a status_update?" -> POST /status_updates
- "Get story details?" -> GET /stories/{story_gid}
- "Update a story?" -> PUT /stories/{story_gid}
- "Delete a story?" -> DELETE /stories/{story_gid}
- "List all stories?" -> GET /tasks/{task_gid}/stories
- "Create a story?" -> POST /tasks/{task_gid}/stories
- "List all tags?" -> GET /tags
- "Create a tag?" -> POST /tags
- "Get tag details?" -> GET /tags/{tag_gid}
- "Update a tag?" -> PUT /tags/{tag_gid}
- "Delete a tag?" -> DELETE /tags/{tag_gid}
- "List all tags?" -> GET /tasks/{task_gid}/tags
- "List all tags?" -> GET /workspaces/{workspace_gid}/tags
- "Create a tag?" -> POST /workspaces/{workspace_gid}/tags
- "List all task_templates?" -> GET /task_templates
- "Get task_template details?" -> GET /task_templates/{task_template_gid}
- "Delete a task_template?" -> DELETE /task_templates/{task_template_gid}
- "Create a instantiateTask?" -> POST /task_templates/{task_template_gid}/instantiateTask
- "List all tasks?" -> GET /tasks
- "Create a task?" -> POST /tasks
- "Get task details?" -> GET /tasks/{task_gid}
- "Update a task?" -> PUT /tasks/{task_gid}
- "Delete a task?" -> DELETE /tasks/{task_gid}
- "Create a duplicate?" -> POST /tasks/{task_gid}/duplicate
- "List all tasks?" -> GET /projects/{project_gid}/tasks
- "List all tasks?" -> GET /sections/{section_gid}/tasks
- "List all tasks?" -> GET /tags/{tag_gid}/tasks
- "List all tasks?" -> GET /user_task_lists/{user_task_list_gid}/tasks
- "List all subtasks?" -> GET /tasks/{task_gid}/subtasks
- "Create a subtask?" -> POST /tasks/{task_gid}/subtasks
- "Create a setParent?" -> POST /tasks/{task_gid}/setParent
- "List all dependencies?" -> GET /tasks/{task_gid}/dependencies
- "Create a addDependency?" -> POST /tasks/{task_gid}/addDependencies
- "Create a removeDependency?" -> POST /tasks/{task_gid}/removeDependencies
- "List all dependents?" -> GET /tasks/{task_gid}/dependents
- "Create a addDependent?" -> POST /tasks/{task_gid}/addDependents
- "Create a removeDependent?" -> POST /tasks/{task_gid}/removeDependents
- "Create a addProject?" -> POST /tasks/{task_gid}/addProject
- "Create a removeProject?" -> POST /tasks/{task_gid}/removeProject
- "Create a addTag?" -> POST /tasks/{task_gid}/addTag
- "Create a removeTag?" -> POST /tasks/{task_gid}/removeTag
- "Create a addFollower?" -> POST /tasks/{task_gid}/addFollowers
- "Create a removeFollower?" -> POST /tasks/{task_gid}/removeFollowers
- "Get custom_id details?" -> GET /workspaces/{workspace_gid}/tasks/custom_id/{custom_id}
- "List all search?" -> GET /workspaces/{workspace_gid}/tasks/search
- "Get team_membership details?" -> GET /team_memberships/{team_membership_gid}
- "List all team_memberships?" -> GET /team_memberships
- "List all team_memberships?" -> GET /teams/{team_gid}/team_memberships
- "List all team_memberships?" -> GET /users/{user_gid}/team_memberships
- "Create a team?" -> POST /teams
- "Get team details?" -> GET /teams/{team_gid}
- "Update a team?" -> PUT /teams/{team_gid}
- "List all teams?" -> GET /workspaces/{workspace_gid}/teams
- "List all teams?" -> GET /users/{user_gid}/teams
- "Create a addUser?" -> POST /teams/{team_gid}/addUser
- "Create a removeUser?" -> POST /teams/{team_gid}/removeUser
- "Get time_period details?" -> GET /time_periods/{time_period_gid}
- "List all time_periods?" -> GET /time_periods
- "List all time_tracking_entries?" -> GET /tasks/{task_gid}/time_tracking_entries
- "Create a time_tracking_entry?" -> POST /tasks/{task_gid}/time_tracking_entries
- "Get time_tracking_entry details?" -> GET /time_tracking_entries/{time_tracking_entry_gid}
- "Update a time_tracking_entry?" -> PUT /time_tracking_entries/{time_tracking_entry_gid}
- "Delete a time_tracking_entry?" -> DELETE /time_tracking_entries/{time_tracking_entry_gid}
- "List all time_tracking_entries?" -> GET /time_tracking_entries
- "List all typeahead?" -> GET /workspaces/{workspace_gid}/typeahead
- "Get user_task_list details?" -> GET /user_task_lists/{user_task_list_gid}
- "List all user_task_list?" -> GET /users/{user_gid}/user_task_list
- "List all users?" -> GET /users
- "Get user details?" -> GET /users/{user_gid}
- "Update a user?" -> PUT /users/{user_gid}
- "List all favorites?" -> GET /users/{user_gid}/favorites
- "List all users?" -> GET /teams/{team_gid}/users
- "List all users?" -> GET /workspaces/{workspace_gid}/users
- "Get user details?" -> GET /workspaces/{workspace_gid}/users/{user_gid}
- "Update a user?" -> PUT /workspaces/{workspace_gid}/users/{user_gid}
- "List all webhooks?" -> GET /webhooks
- "Create a webhook?" -> POST /webhooks
- "Get webhook details?" -> GET /webhooks/{webhook_gid}
- "Update a webhook?" -> PUT /webhooks/{webhook_gid}
- "Delete a webhook?" -> DELETE /webhooks/{webhook_gid}
- "Get workspace_membership details?" -> GET /workspace_memberships/{workspace_membership_gid}
- "List all workspace_memberships?" -> GET /users/{user_gid}/workspace_memberships
- "List all workspace_memberships?" -> GET /workspaces/{workspace_gid}/workspace_memberships
- "List all workspaces?" -> GET /workspaces
- "Get workspace details?" -> GET /workspaces/{workspace_gid}
- "Update a workspace?" -> PUT /workspaces/{workspace_gid}
- "Create a addUser?" -> POST /workspaces/{workspace_gid}/addUser
- "Create a removeUser?" -> POST /workspaces/{workspace_gid}/removeUser
- "List all events?" -> GET /workspaces/{workspace_gid}/events
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
