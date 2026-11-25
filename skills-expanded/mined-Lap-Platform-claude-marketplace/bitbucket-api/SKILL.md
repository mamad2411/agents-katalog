---
name: bitbucket-api
description: "Bitbucket API skill. Use when working with Bitbucket for addon, hook_events, repositories. Covers 335 endpoints."
version: 1.0.0
generator: lapsh
---

# Bitbucket API
API version: 2.0

## Auth
basic | OAuth2 | ApiKey Authorization in header

## Base URL
https://api.bitbucket.org/2.0

## Setup
1. Set your API key in the appropriate header
2. GET /addon/linkers -- verify access
3. POST /addon/linkers/{linker_key}/values -- create first values

## Endpoints

335 endpoints across 8 groups. See references/api-spec.lap for full details.

### addon
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /addon | Delete an app |
| PUT | /addon | Update an installed app |
| GET | /addon/linkers | List linkers for an app |
| GET | /addon/linkers/{linker_key} | Get a linker for an app |
| DELETE | /addon/linkers/{linker_key}/values | Delete all linker values |
| GET | /addon/linkers/{linker_key}/values | List linker values for a linker |
| POST | /addon/linkers/{linker_key}/values | Create a linker value |
| PUT | /addon/linkers/{linker_key}/values | Update a linker value |
| DELETE | /addon/linkers/{linker_key}/values/{value_id} | Delete a linker value |
| GET | /addon/linkers/{linker_key}/values/{value_id} | Get a linker value |

### hook_events
| Method | Path | Description |
|--------|------|-------------|
| GET | /hook_events | Get a webhook resource |
| GET | /hook_events/{subject_type} | List subscribable webhook types |

### repositories
| Method | Path | Description |
|--------|------|-------------|
| GET | /repositories | List public repositories |
| GET | /repositories/{workspace} | List repositories in a workspace |
| DELETE | /repositories/{workspace}/{repo_slug} | Delete a repository |
| GET | /repositories/{workspace}/{repo_slug} | Get a repository |
| POST | /repositories/{workspace}/{repo_slug} | Create a repository |
| PUT | /repositories/{workspace}/{repo_slug} | Update a repository |
| GET | /repositories/{workspace}/{repo_slug}/branch-restrictions | List branch restrictions |
| POST | /repositories/{workspace}/{repo_slug}/branch-restrictions | Create a branch restriction rule |
| DELETE | /repositories/{workspace}/{repo_slug}/branch-restrictions/{id} | Delete a branch restriction rule |
| GET | /repositories/{workspace}/{repo_slug}/branch-restrictions/{id} | Get a branch restriction rule |
| PUT | /repositories/{workspace}/{repo_slug}/branch-restrictions/{id} | Update a branch restriction rule |
| GET | /repositories/{workspace}/{repo_slug}/branching-model | Get the branching model for a repository |
| GET | /repositories/{workspace}/{repo_slug}/branching-model/settings | Get the branching model config for a repository |
| PUT | /repositories/{workspace}/{repo_slug}/branching-model/settings | Update the branching model config for a repository |
| GET | /repositories/{workspace}/{repo_slug}/commit/{commit} | Get a commit |
| DELETE | /repositories/{workspace}/{repo_slug}/commit/{commit}/approve | Unapprove a commit |
| POST | /repositories/{workspace}/{repo_slug}/commit/{commit}/approve | Approve a commit |
| GET | /repositories/{workspace}/{repo_slug}/commit/{commit}/comments | List a commit's comments |
| POST | /repositories/{workspace}/{repo_slug}/commit/{commit}/comments | Create comment for a commit |
| DELETE | /repositories/{workspace}/{repo_slug}/commit/{commit}/comments/{comment_id} | Delete a commit comment |
| GET | /repositories/{workspace}/{repo_slug}/commit/{commit}/comments/{comment_id} | Get a commit comment |
| PUT | /repositories/{workspace}/{repo_slug}/commit/{commit}/comments/{comment_id} | Update a commit comment |
| PUT | /repositories/{workspace}/{repo_slug}/commit/{commit}/properties/{app_key}/{property_name} | Update a commit application property |
| DELETE | /repositories/{workspace}/{repo_slug}/commit/{commit}/properties/{app_key}/{property_name} | Delete a commit application property |
| GET | /repositories/{workspace}/{repo_slug}/commit/{commit}/properties/{app_key}/{property_name} | Get a commit application property |
| GET | /repositories/{workspace}/{repo_slug}/commit/{commit}/pullrequests | List pull requests that contain a commit |
| GET | /repositories/{workspace}/{repo_slug}/commit/{commit}/reports | List reports |
| PUT | /repositories/{workspace}/{repo_slug}/commit/{commit}/reports/{reportId} | Create or update a report |
| GET | /repositories/{workspace}/{repo_slug}/commit/{commit}/reports/{reportId} | Get a report |
| DELETE | /repositories/{workspace}/{repo_slug}/commit/{commit}/reports/{reportId} | Delete a report |
| GET | /repositories/{workspace}/{repo_slug}/commit/{commit}/reports/{reportId}/annotations | List annotations |
| POST | /repositories/{workspace}/{repo_slug}/commit/{commit}/reports/{reportId}/annotations | Bulk create or update annotations |
| GET | /repositories/{workspace}/{repo_slug}/commit/{commit}/reports/{reportId}/annotations/{annotationId} | Get an annotation |
| PUT | /repositories/{workspace}/{repo_slug}/commit/{commit}/reports/{reportId}/annotations/{annotationId} | Create or update an annotation |
| DELETE | /repositories/{workspace}/{repo_slug}/commit/{commit}/reports/{reportId}/annotations/{annotationId} | Delete an annotation |
| GET | /repositories/{workspace}/{repo_slug}/commit/{commit}/statuses | List commit statuses for a commit |
| POST | /repositories/{workspace}/{repo_slug}/commit/{commit}/statuses/build | Create a build status for a commit |
| GET | /repositories/{workspace}/{repo_slug}/commit/{commit}/statuses/build/{key} | Get a build status for a commit |
| PUT | /repositories/{workspace}/{repo_slug}/commit/{commit}/statuses/build/{key} | Update a build status for a commit |
| GET | /repositories/{workspace}/{repo_slug}/commits | List commits |
| POST | /repositories/{workspace}/{repo_slug}/commits | List commits with include/exclude |
| GET | /repositories/{workspace}/{repo_slug}/commits/{revision} | List commits for revision |
| POST | /repositories/{workspace}/{repo_slug}/commits/{revision} | List commits for revision using include/exclude |
| GET | /repositories/{workspace}/{repo_slug}/components | List components |
| GET | /repositories/{workspace}/{repo_slug}/components/{component_id} | Get a component for issues |
| GET | /repositories/{workspace}/{repo_slug}/default-reviewers | List default reviewers |
| DELETE | /repositories/{workspace}/{repo_slug}/default-reviewers/{target_username} | Remove a user from the default reviewers |
| GET | /repositories/{workspace}/{repo_slug}/default-reviewers/{target_username} | Get a default reviewer |
| PUT | /repositories/{workspace}/{repo_slug}/default-reviewers/{target_username} | Add a user to the default reviewers |
| GET | /repositories/{workspace}/{repo_slug}/deploy-keys | List repository deploy keys |
| POST | /repositories/{workspace}/{repo_slug}/deploy-keys | Add a repository deploy key |
| DELETE | /repositories/{workspace}/{repo_slug}/deploy-keys/{key_id} | Delete a repository deploy key |
| GET | /repositories/{workspace}/{repo_slug}/deploy-keys/{key_id} | Get a repository deploy key |
| PUT | /repositories/{workspace}/{repo_slug}/deploy-keys/{key_id} | Update a repository deploy key |
| GET | /repositories/{workspace}/{repo_slug}/deployments | List deployments |
| GET | /repositories/{workspace}/{repo_slug}/deployments/{deployment_uuid} | Get a deployment |
| GET | /repositories/{workspace}/{repo_slug}/deployments_config/environments/{environment_uuid}/variables | List variables for an environment |
| POST | /repositories/{workspace}/{repo_slug}/deployments_config/environments/{environment_uuid}/variables | Create a variable for an environment |
| PUT | /repositories/{workspace}/{repo_slug}/deployments_config/environments/{environment_uuid}/variables/{variable_uuid} | Update a variable for an environment |
| DELETE | /repositories/{workspace}/{repo_slug}/deployments_config/environments/{environment_uuid}/variables/{variable_uuid} | Delete a variable for an environment |
| GET | /repositories/{workspace}/{repo_slug}/diff/{spec} | Compare two commits |
| GET | /repositories/{workspace}/{repo_slug}/diffstat/{spec} | Compare two commit diff stats |
| GET | /repositories/{workspace}/{repo_slug}/downloads | List download artifacts |
| POST | /repositories/{workspace}/{repo_slug}/downloads | Upload a download artifact |
| DELETE | /repositories/{workspace}/{repo_slug}/downloads/{filename} | Delete a download artifact |
| GET | /repositories/{workspace}/{repo_slug}/downloads/{filename} | Get a download artifact link |
| GET | /repositories/{workspace}/{repo_slug}/effective-branching-model | Get the effective, or currently applied, branching model for a repository |
| GET | /repositories/{workspace}/{repo_slug}/effective-default-reviewers | List effective default reviewers |
| GET | /repositories/{workspace}/{repo_slug}/environments | List environments |
| POST | /repositories/{workspace}/{repo_slug}/environments | Create an environment |
| GET | /repositories/{workspace}/{repo_slug}/environments/{environment_uuid} | Get an environment |
| DELETE | /repositories/{workspace}/{repo_slug}/environments/{environment_uuid} | Delete an environment |
| POST | /repositories/{workspace}/{repo_slug}/environments/{environment_uuid}/changes | Update an environment |
| GET | /repositories/{workspace}/{repo_slug}/filehistory/{commit}/{path} | List commits that modified a file |
| GET | /repositories/{workspace}/{repo_slug}/forks | List repository forks |
| POST | /repositories/{workspace}/{repo_slug}/forks | Fork a repository |
| GET | /repositories/{workspace}/{repo_slug}/hooks | List webhooks for a repository |
| POST | /repositories/{workspace}/{repo_slug}/hooks | Create a webhook for a repository |
| DELETE | /repositories/{workspace}/{repo_slug}/hooks/{uid} | Delete a webhook for a repository |
| GET | /repositories/{workspace}/{repo_slug}/hooks/{uid} | Get a webhook for a repository |
| PUT | /repositories/{workspace}/{repo_slug}/hooks/{uid} | Update a webhook for a repository |
| GET | /repositories/{workspace}/{repo_slug}/issues | List issues |
| POST | /repositories/{workspace}/{repo_slug}/issues | Create an issue |
| POST | /repositories/{workspace}/{repo_slug}/issues/export | Export issues |
| GET | /repositories/{workspace}/{repo_slug}/issues/export/{repo_name}-issues-{task_id}.zip | Check issue export status |
| GET | /repositories/{workspace}/{repo_slug}/issues/import | Check issue import status |
| POST | /repositories/{workspace}/{repo_slug}/issues/import | Import issues |
| DELETE | /repositories/{workspace}/{repo_slug}/issues/{issue_id} | Delete an issue |
| GET | /repositories/{workspace}/{repo_slug}/issues/{issue_id} | Get an issue |
| PUT | /repositories/{workspace}/{repo_slug}/issues/{issue_id} | Update an issue |
| GET | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/attachments | List attachments for an issue |
| POST | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/attachments | Upload an attachment to an issue |
| DELETE | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/attachments/{path} | Delete an attachment for an issue |
| GET | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/attachments/{path} | Get attachment for an issue |
| GET | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/changes | List changes on an issue |
| POST | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/changes | Modify the state of an issue |
| GET | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/changes/{change_id} | Get issue change object |
| GET | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/comments | List comments on an issue |
| POST | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/comments | Create a comment on an issue |
| DELETE | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/comments/{comment_id} | Delete a comment on an issue |
| GET | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/comments/{comment_id} | Get a comment on an issue |
| PUT | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/comments/{comment_id} | Update a comment on an issue |
| DELETE | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/vote | Remove vote for an issue |
| GET | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/vote | Check if current user voted for an issue |
| PUT | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/vote | Vote for an issue |
| DELETE | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/watch | Stop watching an issue |
| GET | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/watch | Check if current user is watching a issue |
| PUT | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/watch | Watch an issue |
| GET | /repositories/{workspace}/{repo_slug}/merge-base/{revspec} | Get the common ancestor between two commits |
| GET | /repositories/{workspace}/{repo_slug}/milestones | List milestones |
| GET | /repositories/{workspace}/{repo_slug}/milestones/{milestone_id} | Get a milestone |
| GET | /repositories/{workspace}/{repo_slug}/override-settings | Retrieve the inheritance state for repository settings |
| PUT | /repositories/{workspace}/{repo_slug}/override-settings | Set the inheritance state for repository settings |
| GET | /repositories/{workspace}/{repo_slug}/patch/{spec} | Get a patch for two commits |
| GET | /repositories/{workspace}/{repo_slug}/permissions-config/groups | List explicit group permissions for a repository |
| DELETE | /repositories/{workspace}/{repo_slug}/permissions-config/groups/{group_slug} | Delete an explicit group permission for a repository |
| GET | /repositories/{workspace}/{repo_slug}/permissions-config/groups/{group_slug} | Get an explicit group permission for a repository |
| PUT | /repositories/{workspace}/{repo_slug}/permissions-config/groups/{group_slug} | Update an explicit group permission for a repository |
| GET | /repositories/{workspace}/{repo_slug}/permissions-config/users | List explicit user permissions for a repository |
| DELETE | /repositories/{workspace}/{repo_slug}/permissions-config/users/{selected_user_id} | Delete an explicit user permission for a repository |
| GET | /repositories/{workspace}/{repo_slug}/permissions-config/users/{selected_user_id} | Get an explicit user permission for a repository |
| PUT | /repositories/{workspace}/{repo_slug}/permissions-config/users/{selected_user_id} | Update an explicit user permission for a repository |
| GET | /repositories/{workspace}/{repo_slug}/pipelines | List pipelines |
| POST | /repositories/{workspace}/{repo_slug}/pipelines | Run a pipeline |
| GET | /repositories/{workspace}/{repo_slug}/pipelines-config/caches | List caches |
| DELETE | /repositories/{workspace}/{repo_slug}/pipelines-config/caches | Delete caches |
| DELETE | /repositories/{workspace}/{repo_slug}/pipelines-config/caches/{cache_uuid} | Delete a cache |
| GET | /repositories/{workspace}/{repo_slug}/pipelines-config/caches/{cache_uuid}/content-uri | Get cache content URI |
| GET | /repositories/{workspace}/{repo_slug}/pipelines-config/runners | Get repository runners |
| POST | /repositories/{workspace}/{repo_slug}/pipelines-config/runners | Create repository runner |
| GET | /repositories/{workspace}/{repo_slug}/pipelines-config/runners/{runner_uuid} | Get repository runner |
| PUT | /repositories/{workspace}/{repo_slug}/pipelines-config/runners/{runner_uuid} | Update repository runner |
| DELETE | /repositories/{workspace}/{repo_slug}/pipelines-config/runners/{runner_uuid} | Delete repository runner |
| GET | /repositories/{workspace}/{repo_slug}/pipelines/{pipeline_uuid} | Get a pipeline |
| GET | /repositories/{workspace}/{repo_slug}/pipelines/{pipeline_uuid}/steps | List steps for a pipeline |
| GET | /repositories/{workspace}/{repo_slug}/pipelines/{pipeline_uuid}/steps/{step_uuid} | Get a step of a pipeline |
| GET | /repositories/{workspace}/{repo_slug}/pipelines/{pipeline_uuid}/steps/{step_uuid}/log | Get log file for a step |
| GET | /repositories/{workspace}/{repo_slug}/pipelines/{pipeline_uuid}/steps/{step_uuid}/logs/{log_uuid} | Get the logs for the build container or a service container for a given step of a pipeline. |
| GET | /repositories/{workspace}/{repo_slug}/pipelines/{pipeline_uuid}/steps/{step_uuid}/test_reports | Get a summary of test reports for a given step of a pipeline. |
| GET | /repositories/{workspace}/{repo_slug}/pipelines/{pipeline_uuid}/steps/{step_uuid}/test_reports/test_cases | Get test cases for a given step of a pipeline. |
| GET | /repositories/{workspace}/{repo_slug}/pipelines/{pipeline_uuid}/steps/{step_uuid}/test_reports/test_cases/{test_case_uuid}/test_case_reasons | Get test case reasons (output) for a given test case in a step of a pipeline. |
| POST | /repositories/{workspace}/{repo_slug}/pipelines/{pipeline_uuid}/stopPipeline | Stop a pipeline |
| GET | /repositories/{workspace}/{repo_slug}/pipelines_config | Get configuration |
| PUT | /repositories/{workspace}/{repo_slug}/pipelines_config | Update configuration |
| PUT | /repositories/{workspace}/{repo_slug}/pipelines_config/build_number | Update the next build number |
| POST | /repositories/{workspace}/{repo_slug}/pipelines_config/schedules | Create a schedule |
| GET | /repositories/{workspace}/{repo_slug}/pipelines_config/schedules | List schedules |
| GET | /repositories/{workspace}/{repo_slug}/pipelines_config/schedules/{schedule_uuid} | Get a schedule |
| PUT | /repositories/{workspace}/{repo_slug}/pipelines_config/schedules/{schedule_uuid} | Update a schedule |
| DELETE | /repositories/{workspace}/{repo_slug}/pipelines_config/schedules/{schedule_uuid} | Delete a schedule |
| GET | /repositories/{workspace}/{repo_slug}/pipelines_config/schedules/{schedule_uuid}/executions | List executions of a schedule |
| GET | /repositories/{workspace}/{repo_slug}/pipelines_config/ssh/key_pair | Get SSH key pair |
| PUT | /repositories/{workspace}/{repo_slug}/pipelines_config/ssh/key_pair | Update SSH key pair |
| DELETE | /repositories/{workspace}/{repo_slug}/pipelines_config/ssh/key_pair | Delete SSH key pair |
| GET | /repositories/{workspace}/{repo_slug}/pipelines_config/ssh/known_hosts | List known hosts |
| POST | /repositories/{workspace}/{repo_slug}/pipelines_config/ssh/known_hosts | Create a known host |
| GET | /repositories/{workspace}/{repo_slug}/pipelines_config/ssh/known_hosts/{known_host_uuid} | Get a known host |
| PUT | /repositories/{workspace}/{repo_slug}/pipelines_config/ssh/known_hosts/{known_host_uuid} | Update a known host |
| DELETE | /repositories/{workspace}/{repo_slug}/pipelines_config/ssh/known_hosts/{known_host_uuid} | Delete a known host |
| GET | /repositories/{workspace}/{repo_slug}/pipelines_config/variables | List variables for a repository |
| POST | /repositories/{workspace}/{repo_slug}/pipelines_config/variables | Create a variable for a repository |
| GET | /repositories/{workspace}/{repo_slug}/pipelines_config/variables/{variable_uuid} | Get a variable for a repository |
| PUT | /repositories/{workspace}/{repo_slug}/pipelines_config/variables/{variable_uuid} | Update a variable for a repository |
| DELETE | /repositories/{workspace}/{repo_slug}/pipelines_config/variables/{variable_uuid} | Delete a variable for a repository |
| PUT | /repositories/{workspace}/{repo_slug}/properties/{app_key}/{property_name} | Update a repository application property |
| DELETE | /repositories/{workspace}/{repo_slug}/properties/{app_key}/{property_name} | Delete a repository application property |
| GET | /repositories/{workspace}/{repo_slug}/properties/{app_key}/{property_name} | Get a repository application property |
| GET | /repositories/{workspace}/{repo_slug}/pullrequests | List pull requests |
| POST | /repositories/{workspace}/{repo_slug}/pullrequests | Create a pull request |
| GET | /repositories/{workspace}/{repo_slug}/pullrequests/activity | List a pull request activity log |
| GET | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id} | Get a pull request |
| PUT | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id} | Update a pull request |
| GET | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/activity | List a pull request activity log |
| DELETE | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/approve | Unapprove a pull request |
| POST | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/approve | Approve a pull request |
| GET | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/comments | List comments on a pull request |
| POST | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/comments | Create a comment on a pull request |
| DELETE | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/comments/{comment_id} | Delete a comment on a pull request |
| GET | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/comments/{comment_id} | Get a comment on a pull request |
| PUT | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/comments/{comment_id} | Update a comment on a pull request |
| DELETE | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/comments/{comment_id}/resolve | Reopen a comment thread |
| POST | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/comments/{comment_id}/resolve | Resolve a comment thread |
| GET | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/commits | List commits on a pull request |
| POST | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/decline | Decline a pull request |
| GET | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/diff | List changes in a pull request |
| GET | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/diffstat | Get the diff stat for a pull request |
| POST | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/merge | Merge a pull request |
| GET | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/merge/task-status/{task_id} | Get the merge task status for a pull request |
| GET | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/patch | Get the patch for a pull request |
| DELETE | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/request-changes | Remove change request for a pull request |
| POST | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/request-changes | Request changes for a pull request |
| GET | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/statuses | List commit statuses for a pull request |
| GET | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/tasks | List tasks on a pull request |
| POST | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/tasks | Create a task on a pull request |
| DELETE | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/tasks/{task_id} | Delete a task on a pull request |
| GET | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/tasks/{task_id} | Get a task on a pull request |
| PUT | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/tasks/{task_id} | Update a task on a pull request |
| PUT | /repositories/{workspace}/{repo_slug}/pullrequests/{pullrequest_id}/properties/{app_key}/{property_name} | Update a pull request application property |
| DELETE | /repositories/{workspace}/{repo_slug}/pullrequests/{pullrequest_id}/properties/{app_key}/{property_name} | Delete a pull request application property |
| GET | /repositories/{workspace}/{repo_slug}/pullrequests/{pullrequest_id}/properties/{app_key}/{property_name} | Get a pull request application property |
| GET | /repositories/{workspace}/{repo_slug}/refs | List branches and tags |
| GET | /repositories/{workspace}/{repo_slug}/refs/branches | List open branches |
| POST | /repositories/{workspace}/{repo_slug}/refs/branches | Create a branch |
| DELETE | /repositories/{workspace}/{repo_slug}/refs/branches/{name} | Delete a branch |
| GET | /repositories/{workspace}/{repo_slug}/refs/branches/{name} | Get a branch |
| GET | /repositories/{workspace}/{repo_slug}/refs/tags | List tags |
| POST | /repositories/{workspace}/{repo_slug}/refs/tags | Create a tag |
| DELETE | /repositories/{workspace}/{repo_slug}/refs/tags/{name} | Delete a tag |
| GET | /repositories/{workspace}/{repo_slug}/refs/tags/{name} | Get a tag |
| GET | /repositories/{workspace}/{repo_slug}/src | Get the root directory of the main branch |
| POST | /repositories/{workspace}/{repo_slug}/src | Create a commit by uploading a file |
| GET | /repositories/{workspace}/{repo_slug}/src/{commit}/{path} | Get file or directory contents |
| GET | /repositories/{workspace}/{repo_slug}/versions | List defined versions for issues |
| GET | /repositories/{workspace}/{repo_slug}/versions/{version_id} | Get a defined version for issues |
| GET | /repositories/{workspace}/{repo_slug}/watchers | List repositories watchers |

### snippets
| Method | Path | Description |
|--------|------|-------------|
| GET | /snippets | List snippets |
| POST | /snippets | Create a snippet |
| GET | /snippets/{workspace} | List snippets in a workspace |
| POST | /snippets/{workspace} | Create a snippet for a workspace |
| DELETE | /snippets/{workspace}/{encoded_id} | Delete a snippet |
| GET | /snippets/{workspace}/{encoded_id} | Get a snippet |
| PUT | /snippets/{workspace}/{encoded_id} | Update a snippet |
| GET | /snippets/{workspace}/{encoded_id}/comments | List comments on a snippet |
| POST | /snippets/{workspace}/{encoded_id}/comments | Create a comment on a snippet |
| DELETE | /snippets/{workspace}/{encoded_id}/comments/{comment_id} | Delete a comment on a snippet |
| GET | /snippets/{workspace}/{encoded_id}/comments/{comment_id} | Get a comment on a snippet |
| PUT | /snippets/{workspace}/{encoded_id}/comments/{comment_id} | Update a comment on a snippet |
| GET | /snippets/{workspace}/{encoded_id}/commits | List snippet changes |
| GET | /snippets/{workspace}/{encoded_id}/commits/{revision} | Get a previous snippet change |
| GET | /snippets/{workspace}/{encoded_id}/files/{path} | Get a snippet's raw file at HEAD |
| DELETE | /snippets/{workspace}/{encoded_id}/watch | Stop watching a snippet |
| GET | /snippets/{workspace}/{encoded_id}/watch | Check if the current user is watching a snippet |
| PUT | /snippets/{workspace}/{encoded_id}/watch | Watch a snippet |
| GET | /snippets/{workspace}/{encoded_id}/watchers | List users watching a snippet |
| DELETE | /snippets/{workspace}/{encoded_id}/{node_id} | Delete a previous revision of a snippet |
| GET | /snippets/{workspace}/{encoded_id}/{node_id} | Get a previous revision of a snippet |
| PUT | /snippets/{workspace}/{encoded_id}/{node_id} | Update a previous revision of a snippet |
| GET | /snippets/{workspace}/{encoded_id}/{node_id}/files/{path} | Get a snippet's raw file |
| GET | /snippets/{workspace}/{encoded_id}/{revision}/diff | Get snippet changes between versions |
| GET | /snippets/{workspace}/{encoded_id}/{revision}/patch | Get snippet patch between versions |

### teams
| Method | Path | Description |
|--------|------|-------------|
| GET | /teams/{username}/pipelines_config/variables | List variables for an account |
| POST | /teams/{username}/pipelines_config/variables | Create a variable for a user |
| GET | /teams/{username}/pipelines_config/variables/{variable_uuid} | Get a variable for a team |
| PUT | /teams/{username}/pipelines_config/variables/{variable_uuid} | Update a variable for a team |
| DELETE | /teams/{username}/pipelines_config/variables/{variable_uuid} | Delete a variable for a team |
| GET | /teams/{username}/search/code | Search for code in a team's repositories |

### user
| Method | Path | Description |
|--------|------|-------------|
| GET | /user | Get current user |
| GET | /user/emails | List email addresses for current user |
| GET | /user/emails/{email} | Get an email address for current user |
| GET | /user/permissions/repositories | List repository permissions for a user |
| GET | /user/permissions/workspaces | List workspaces for the current user |
| GET | /user/workspaces | List workspaces for the current user |
| GET | /user/workspaces/{workspace}/permission | Get user permission on a workspace |
| GET | /user/workspaces/{workspace}/permissions/repositories | List repository permissions in a workspace for a user |

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /users/{selected_user} | Get a user |
| GET | /users/{selected_user}/gpg-keys | List GPG keys |
| POST | /users/{selected_user}/gpg-keys | Add a new GPG key |
| DELETE | /users/{selected_user}/gpg-keys/{fingerprint} | Delete a GPG key |
| GET | /users/{selected_user}/gpg-keys/{fingerprint} | Get a GPG key |
| GET | /users/{selected_user}/pipelines_config/variables | List variables for a user |
| POST | /users/{selected_user}/pipelines_config/variables | Create a variable for a user |
| GET | /users/{selected_user}/pipelines_config/variables/{variable_uuid} | Get a variable for a user |
| PUT | /users/{selected_user}/pipelines_config/variables/{variable_uuid} | Update a variable for a user |
| DELETE | /users/{selected_user}/pipelines_config/variables/{variable_uuid} | Delete a variable for a user |
| PUT | /users/{selected_user}/properties/{app_key}/{property_name} | Update a user application property |
| DELETE | /users/{selected_user}/properties/{app_key}/{property_name} | Delete a user application property |
| GET | /users/{selected_user}/properties/{app_key}/{property_name} | Get a user application property |
| GET | /users/{selected_user}/search/code | Search for code in a user's repositories |
| GET | /users/{selected_user}/ssh-keys | List SSH keys |
| POST | /users/{selected_user}/ssh-keys | Add a new SSH key |
| DELETE | /users/{selected_user}/ssh-keys/{key_id} | Delete a SSH key |
| GET | /users/{selected_user}/ssh-keys/{key_id} | Get a SSH key |
| PUT | /users/{selected_user}/ssh-keys/{key_id} | Update a SSH key |

### workspaces
| Method | Path | Description |
|--------|------|-------------|
| GET | /workspaces | List workspaces for user |
| GET | /workspaces/{workspace} | Get a workspace |
| GET | /workspaces/{workspace}/hooks | List webhooks for a workspace |
| POST | /workspaces/{workspace}/hooks | Create a webhook for a workspace |
| DELETE | /workspaces/{workspace}/hooks/{uid} | Delete a webhook for a workspace |
| GET | /workspaces/{workspace}/hooks/{uid} | Get a webhook for a workspace |
| PUT | /workspaces/{workspace}/hooks/{uid} | Update a webhook for a workspace |
| GET | /workspaces/{workspace}/members | List users in a workspace |
| GET | /workspaces/{workspace}/members/{member} | Get user membership for a workspace |
| GET | /workspaces/{workspace}/permissions | List user permissions in a workspace |
| GET | /workspaces/{workspace}/permissions/repositories | List all repository permissions for a workspace |
| GET | /workspaces/{workspace}/permissions/repositories/{repo_slug} | List a repository permissions for a workspace |
| GET | /workspaces/{workspace}/pipelines-config/identity/oidc/.well-known/openid-configuration | Get OpenID configuration for OIDC in Pipelines |
| GET | /workspaces/{workspace}/pipelines-config/identity/oidc/keys.json | Get keys for OIDC in Pipelines |
| GET | /workspaces/{workspace}/pipelines-config/runners | Get workspace runners |
| POST | /workspaces/{workspace}/pipelines-config/runners | Create workspace runner |
| GET | /workspaces/{workspace}/pipelines-config/runners/{runner_uuid} | Get workspace runner |
| PUT | /workspaces/{workspace}/pipelines-config/runners/{runner_uuid} | Update workspace runner |
| DELETE | /workspaces/{workspace}/pipelines-config/runners/{runner_uuid} | Delete workspace runner |
| GET | /workspaces/{workspace}/pipelines-config/variables | List variables for a workspace |
| POST | /workspaces/{workspace}/pipelines-config/variables | Create a variable for a workspace |
| GET | /workspaces/{workspace}/pipelines-config/variables/{variable_uuid} | Get variable for a workspace |
| PUT | /workspaces/{workspace}/pipelines-config/variables/{variable_uuid} | Update variable for a workspace |
| DELETE | /workspaces/{workspace}/pipelines-config/variables/{variable_uuid} | Delete a variable for a workspace |
| GET | /workspaces/{workspace}/projects | List projects in a workspace |
| POST | /workspaces/{workspace}/projects | Create a project in a workspace |
| DELETE | /workspaces/{workspace}/projects/{project_key} | Delete a project for a workspace |
| GET | /workspaces/{workspace}/projects/{project_key} | Get a project for a workspace |
| PUT | /workspaces/{workspace}/projects/{project_key} | Update a project for a workspace |
| GET | /workspaces/{workspace}/projects/{project_key}/branching-model | Get the branching model for a project |
| GET | /workspaces/{workspace}/projects/{project_key}/branching-model/settings | Get the branching model config for a project |
| PUT | /workspaces/{workspace}/projects/{project_key}/branching-model/settings | Update the branching model config for a project |
| GET | /workspaces/{workspace}/projects/{project_key}/default-reviewers | List the default reviewers in a project |
| DELETE | /workspaces/{workspace}/projects/{project_key}/default-reviewers/{selected_user} | Remove the specific user from the project's default reviewers |
| GET | /workspaces/{workspace}/projects/{project_key}/default-reviewers/{selected_user} | Get a default reviewer |
| PUT | /workspaces/{workspace}/projects/{project_key}/default-reviewers/{selected_user} | Add the specific user as a default reviewer for the project |
| GET | /workspaces/{workspace}/projects/{project_key}/deploy-keys | List project deploy keys |
| POST | /workspaces/{workspace}/projects/{project_key}/deploy-keys | Create a project deploy key |
| DELETE | /workspaces/{workspace}/projects/{project_key}/deploy-keys/{key_id} | Delete a deploy key from a project |
| GET | /workspaces/{workspace}/projects/{project_key}/deploy-keys/{key_id} | Get a project deploy key |
| GET | /workspaces/{workspace}/projects/{project_key}/permissions-config/groups | List explicit group permissions for a project |
| DELETE | /workspaces/{workspace}/projects/{project_key}/permissions-config/groups/{group_slug} | Delete an explicit group permission for a project |
| GET | /workspaces/{workspace}/projects/{project_key}/permissions-config/groups/{group_slug} | Get an explicit group permission for a project |
| PUT | /workspaces/{workspace}/projects/{project_key}/permissions-config/groups/{group_slug} | Update an explicit group permission for a project |
| GET | /workspaces/{workspace}/projects/{project_key}/permissions-config/users | List explicit user permissions for a project |
| DELETE | /workspaces/{workspace}/projects/{project_key}/permissions-config/users/{selected_user_id} | Delete an explicit user permission for a project |
| GET | /workspaces/{workspace}/projects/{project_key}/permissions-config/users/{selected_user_id} | Get an explicit user permission for a project |
| PUT | /workspaces/{workspace}/projects/{project_key}/permissions-config/users/{selected_user_id} | Update an explicit user permission for a project |
| GET | /workspaces/{workspace}/pullrequests/{selected_user} | List workspace pull requests for a user |
| GET | /workspaces/{workspace}/search/code | Search for code in a workspace |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all linkers?" -> GET /addon/linkers
- "Get linker details?" -> GET /addon/linkers/{linker_key}
- "List all values?" -> GET /addon/linkers/{linker_key}/values
- "Create a value?" -> POST /addon/linkers/{linker_key}/values
- "Delete a value?" -> DELETE /addon/linkers/{linker_key}/values/{value_id}
- "Get value details?" -> GET /addon/linkers/{linker_key}/values/{value_id}
- "List all hook_events?" -> GET /hook_events
- "Get hook_event details?" -> GET /hook_events/{subject_type}
- "Search repositories?" -> GET /repositories
- "Search repositories?" -> GET /repositories/{workspace}
- "Delete a repository?" -> DELETE /repositories/{workspace}/{repo_slug}
- "Get repository details?" -> GET /repositories/{workspace}/{repo_slug}
- "Update a repository?" -> PUT /repositories/{workspace}/{repo_slug}
- "List all branch-restrictions?" -> GET /repositories/{workspace}/{repo_slug}/branch-restrictions
- "Create a branch-restriction?" -> POST /repositories/{workspace}/{repo_slug}/branch-restrictions
- "Delete a branch-restriction?" -> DELETE /repositories/{workspace}/{repo_slug}/branch-restrictions/{id}
- "Get branch-restriction details?" -> GET /repositories/{workspace}/{repo_slug}/branch-restrictions/{id}
- "Update a branch-restriction?" -> PUT /repositories/{workspace}/{repo_slug}/branch-restrictions/{id}
- "List all branching-model?" -> GET /repositories/{workspace}/{repo_slug}/branching-model
- "List all settings?" -> GET /repositories/{workspace}/{repo_slug}/branching-model/settings
- "Get commit details?" -> GET /repositories/{workspace}/{repo_slug}/commit/{commit}
- "Create a approve?" -> POST /repositories/{workspace}/{repo_slug}/commit/{commit}/approve
- "Search comments?" -> GET /repositories/{workspace}/{repo_slug}/commit/{commit}/comments
- "Create a comment?" -> POST /repositories/{workspace}/{repo_slug}/commit/{commit}/comments
- "Delete a comment?" -> DELETE /repositories/{workspace}/{repo_slug}/commit/{commit}/comments/{comment_id}
- "Get comment details?" -> GET /repositories/{workspace}/{repo_slug}/commit/{commit}/comments/{comment_id}
- "Update a comment?" -> PUT /repositories/{workspace}/{repo_slug}/commit/{commit}/comments/{comment_id}
- "Update a property?" -> PUT /repositories/{workspace}/{repo_slug}/commit/{commit}/properties/{app_key}/{property_name}
- "Delete a property?" -> DELETE /repositories/{workspace}/{repo_slug}/commit/{commit}/properties/{app_key}/{property_name}
- "Get property details?" -> GET /repositories/{workspace}/{repo_slug}/commit/{commit}/properties/{app_key}/{property_name}
- "List all pullrequests?" -> GET /repositories/{workspace}/{repo_slug}/commit/{commit}/pullrequests
- "List all reports?" -> GET /repositories/{workspace}/{repo_slug}/commit/{commit}/reports
- "Update a report?" -> PUT /repositories/{workspace}/{repo_slug}/commit/{commit}/reports/{reportId}
- "Get report details?" -> GET /repositories/{workspace}/{repo_slug}/commit/{commit}/reports/{reportId}
- "Delete a report?" -> DELETE /repositories/{workspace}/{repo_slug}/commit/{commit}/reports/{reportId}
- "List all annotations?" -> GET /repositories/{workspace}/{repo_slug}/commit/{commit}/reports/{reportId}/annotations
- "Create a annotation?" -> POST /repositories/{workspace}/{repo_slug}/commit/{commit}/reports/{reportId}/annotations
- "Get annotation details?" -> GET /repositories/{workspace}/{repo_slug}/commit/{commit}/reports/{reportId}/annotations/{annotationId}
- "Update a annotation?" -> PUT /repositories/{workspace}/{repo_slug}/commit/{commit}/reports/{reportId}/annotations/{annotationId}
- "Delete a annotation?" -> DELETE /repositories/{workspace}/{repo_slug}/commit/{commit}/reports/{reportId}/annotations/{annotationId}
- "Search statuses?" -> GET /repositories/{workspace}/{repo_slug}/commit/{commit}/statuses
- "Create a build?" -> POST /repositories/{workspace}/{repo_slug}/commit/{commit}/statuses/build
- "Get build details?" -> GET /repositories/{workspace}/{repo_slug}/commit/{commit}/statuses/build/{key}
- "Update a build?" -> PUT /repositories/{workspace}/{repo_slug}/commit/{commit}/statuses/build/{key}
- "List all commits?" -> GET /repositories/{workspace}/{repo_slug}/commits
- "Create a commit?" -> POST /repositories/{workspace}/{repo_slug}/commits
- "Get commit details?" -> GET /repositories/{workspace}/{repo_slug}/commits/{revision}
- "List all components?" -> GET /repositories/{workspace}/{repo_slug}/components
- "Get component details?" -> GET /repositories/{workspace}/{repo_slug}/components/{component_id}
- "List all default-reviewers?" -> GET /repositories/{workspace}/{repo_slug}/default-reviewers
- "Delete a default-reviewer?" -> DELETE /repositories/{workspace}/{repo_slug}/default-reviewers/{target_username}
- "Get default-reviewer details?" -> GET /repositories/{workspace}/{repo_slug}/default-reviewers/{target_username}
- "Update a default-reviewer?" -> PUT /repositories/{workspace}/{repo_slug}/default-reviewers/{target_username}
- "List all deploy-keys?" -> GET /repositories/{workspace}/{repo_slug}/deploy-keys
- "Create a deploy-key?" -> POST /repositories/{workspace}/{repo_slug}/deploy-keys
- "Delete a deploy-key?" -> DELETE /repositories/{workspace}/{repo_slug}/deploy-keys/{key_id}
- "Get deploy-key details?" -> GET /repositories/{workspace}/{repo_slug}/deploy-keys/{key_id}
- "Update a deploy-key?" -> PUT /repositories/{workspace}/{repo_slug}/deploy-keys/{key_id}
- "List all deployments?" -> GET /repositories/{workspace}/{repo_slug}/deployments
- "Get deployment details?" -> GET /repositories/{workspace}/{repo_slug}/deployments/{deployment_uuid}
- "List all variables?" -> GET /repositories/{workspace}/{repo_slug}/deployments_config/environments/{environment_uuid}/variables
- "Create a variable?" -> POST /repositories/{workspace}/{repo_slug}/deployments_config/environments/{environment_uuid}/variables
- "Update a variable?" -> PUT /repositories/{workspace}/{repo_slug}/deployments_config/environments/{environment_uuid}/variables/{variable_uuid}
- "Delete a variable?" -> DELETE /repositories/{workspace}/{repo_slug}/deployments_config/environments/{environment_uuid}/variables/{variable_uuid}
- "Get diff details?" -> GET /repositories/{workspace}/{repo_slug}/diff/{spec}
- "Get diffstat details?" -> GET /repositories/{workspace}/{repo_slug}/diffstat/{spec}
- "List all downloads?" -> GET /repositories/{workspace}/{repo_slug}/downloads
- "Create a download?" -> POST /repositories/{workspace}/{repo_slug}/downloads
- "Delete a download?" -> DELETE /repositories/{workspace}/{repo_slug}/downloads/{filename}
- "Get download details?" -> GET /repositories/{workspace}/{repo_slug}/downloads/{filename}
- "List all effective-branching-model?" -> GET /repositories/{workspace}/{repo_slug}/effective-branching-model
- "List all effective-default-reviewers?" -> GET /repositories/{workspace}/{repo_slug}/effective-default-reviewers
- "List all environments?" -> GET /repositories/{workspace}/{repo_slug}/environments
- "Create a environment?" -> POST /repositories/{workspace}/{repo_slug}/environments
- "Get environment details?" -> GET /repositories/{workspace}/{repo_slug}/environments/{environment_uuid}
- "Delete a environment?" -> DELETE /repositories/{workspace}/{repo_slug}/environments/{environment_uuid}
- "Create a change?" -> POST /repositories/{workspace}/{repo_slug}/environments/{environment_uuid}/changes
- "Search filehistory?" -> GET /repositories/{workspace}/{repo_slug}/filehistory/{commit}/{path}
- "Search forks?" -> GET /repositories/{workspace}/{repo_slug}/forks
- "Create a fork?" -> POST /repositories/{workspace}/{repo_slug}/forks
- "List all hooks?" -> GET /repositories/{workspace}/{repo_slug}/hooks
- "Create a hook?" -> POST /repositories/{workspace}/{repo_slug}/hooks
- "Delete a hook?" -> DELETE /repositories/{workspace}/{repo_slug}/hooks/{uid}
- "Get hook details?" -> GET /repositories/{workspace}/{repo_slug}/hooks/{uid}
- "Update a hook?" -> PUT /repositories/{workspace}/{repo_slug}/hooks/{uid}
- "List all issues?" -> GET /repositories/{workspace}/{repo_slug}/issues
- "Create a issue?" -> POST /repositories/{workspace}/{repo_slug}/issues
- "Create a export?" -> POST /repositories/{workspace}/{repo_slug}/issues/export
- "Get export details?" -> GET /repositories/{workspace}/{repo_slug}/issues/export/{repo_name}-issues-{task_id}.zip
- "List all import?" -> GET /repositories/{workspace}/{repo_slug}/issues/import
- "Create a import?" -> POST /repositories/{workspace}/{repo_slug}/issues/import
- "Delete a issue?" -> DELETE /repositories/{workspace}/{repo_slug}/issues/{issue_id}
- "Get issue details?" -> GET /repositories/{workspace}/{repo_slug}/issues/{issue_id}
- "Update a issue?" -> PUT /repositories/{workspace}/{repo_slug}/issues/{issue_id}
- "List all attachments?" -> GET /repositories/{workspace}/{repo_slug}/issues/{issue_id}/attachments
- "Create a attachment?" -> POST /repositories/{workspace}/{repo_slug}/issues/{issue_id}/attachments
- "Delete a attachment?" -> DELETE /repositories/{workspace}/{repo_slug}/issues/{issue_id}/attachments/{path}
- "Get attachment details?" -> GET /repositories/{workspace}/{repo_slug}/issues/{issue_id}/attachments/{path}
- "Search changes?" -> GET /repositories/{workspace}/{repo_slug}/issues/{issue_id}/changes
- "Create a change?" -> POST /repositories/{workspace}/{repo_slug}/issues/{issue_id}/changes
- "Get change details?" -> GET /repositories/{workspace}/{repo_slug}/issues/{issue_id}/changes/{change_id}
- "Search comments?" -> GET /repositories/{workspace}/{repo_slug}/issues/{issue_id}/comments
- "Create a comment?" -> POST /repositories/{workspace}/{repo_slug}/issues/{issue_id}/comments
- "Delete a comment?" -> DELETE /repositories/{workspace}/{repo_slug}/issues/{issue_id}/comments/{comment_id}
- "Get comment details?" -> GET /repositories/{workspace}/{repo_slug}/issues/{issue_id}/comments/{comment_id}
- "Update a comment?" -> PUT /repositories/{workspace}/{repo_slug}/issues/{issue_id}/comments/{comment_id}
- "List all vote?" -> GET /repositories/{workspace}/{repo_slug}/issues/{issue_id}/vote
- "List all watch?" -> GET /repositories/{workspace}/{repo_slug}/issues/{issue_id}/watch
- "Get merge-base details?" -> GET /repositories/{workspace}/{repo_slug}/merge-base/{revspec}
- "List all milestones?" -> GET /repositories/{workspace}/{repo_slug}/milestones
- "Get milestone details?" -> GET /repositories/{workspace}/{repo_slug}/milestones/{milestone_id}
- "List all override-settings?" -> GET /repositories/{workspace}/{repo_slug}/override-settings
- "Get patch details?" -> GET /repositories/{workspace}/{repo_slug}/patch/{spec}
- "List all groups?" -> GET /repositories/{workspace}/{repo_slug}/permissions-config/groups
- "Delete a group?" -> DELETE /repositories/{workspace}/{repo_slug}/permissions-config/groups/{group_slug}
- "Get group details?" -> GET /repositories/{workspace}/{repo_slug}/permissions-config/groups/{group_slug}
- "Update a group?" -> PUT /repositories/{workspace}/{repo_slug}/permissions-config/groups/{group_slug}
- "List all users?" -> GET /repositories/{workspace}/{repo_slug}/permissions-config/users
- "Delete a user?" -> DELETE /repositories/{workspace}/{repo_slug}/permissions-config/users/{selected_user_id}
- "Get user details?" -> GET /repositories/{workspace}/{repo_slug}/permissions-config/users/{selected_user_id}
- "Update a user?" -> PUT /repositories/{workspace}/{repo_slug}/permissions-config/users/{selected_user_id}
- "List all pipelines?" -> GET /repositories/{workspace}/{repo_slug}/pipelines
- "Create a pipeline?" -> POST /repositories/{workspace}/{repo_slug}/pipelines
- "List all caches?" -> GET /repositories/{workspace}/{repo_slug}/pipelines-config/caches
- "Delete a cache?" -> DELETE /repositories/{workspace}/{repo_slug}/pipelines-config/caches/{cache_uuid}
- "List all content-uri?" -> GET /repositories/{workspace}/{repo_slug}/pipelines-config/caches/{cache_uuid}/content-uri
- "List all runners?" -> GET /repositories/{workspace}/{repo_slug}/pipelines-config/runners
- "Create a runner?" -> POST /repositories/{workspace}/{repo_slug}/pipelines-config/runners
- "Get runner details?" -> GET /repositories/{workspace}/{repo_slug}/pipelines-config/runners/{runner_uuid}
- "Update a runner?" -> PUT /repositories/{workspace}/{repo_slug}/pipelines-config/runners/{runner_uuid}
- "Delete a runner?" -> DELETE /repositories/{workspace}/{repo_slug}/pipelines-config/runners/{runner_uuid}
- "Get pipeline details?" -> GET /repositories/{workspace}/{repo_slug}/pipelines/{pipeline_uuid}
- "List all steps?" -> GET /repositories/{workspace}/{repo_slug}/pipelines/{pipeline_uuid}/steps
- "Get step details?" -> GET /repositories/{workspace}/{repo_slug}/pipelines/{pipeline_uuid}/steps/{step_uuid}
- "List all log?" -> GET /repositories/{workspace}/{repo_slug}/pipelines/{pipeline_uuid}/steps/{step_uuid}/log
- "Get log details?" -> GET /repositories/{workspace}/{repo_slug}/pipelines/{pipeline_uuid}/steps/{step_uuid}/logs/{log_uuid}
- "List all test_reports?" -> GET /repositories/{workspace}/{repo_slug}/pipelines/{pipeline_uuid}/steps/{step_uuid}/test_reports
- "List all test_cases?" -> GET /repositories/{workspace}/{repo_slug}/pipelines/{pipeline_uuid}/steps/{step_uuid}/test_reports/test_cases
- "List all test_case_reasons?" -> GET /repositories/{workspace}/{repo_slug}/pipelines/{pipeline_uuid}/steps/{step_uuid}/test_reports/test_cases/{test_case_uuid}/test_case_reasons
- "Create a stopPipeline?" -> POST /repositories/{workspace}/{repo_slug}/pipelines/{pipeline_uuid}/stopPipeline
- "List all pipelines_config?" -> GET /repositories/{workspace}/{repo_slug}/pipelines_config
- "Create a schedule?" -> POST /repositories/{workspace}/{repo_slug}/pipelines_config/schedules
- "List all schedules?" -> GET /repositories/{workspace}/{repo_slug}/pipelines_config/schedules
- "Get schedule details?" -> GET /repositories/{workspace}/{repo_slug}/pipelines_config/schedules/{schedule_uuid}
- "Update a schedule?" -> PUT /repositories/{workspace}/{repo_slug}/pipelines_config/schedules/{schedule_uuid}
- "Delete a schedule?" -> DELETE /repositories/{workspace}/{repo_slug}/pipelines_config/schedules/{schedule_uuid}
- "List all executions?" -> GET /repositories/{workspace}/{repo_slug}/pipelines_config/schedules/{schedule_uuid}/executions
- "List all key_pair?" -> GET /repositories/{workspace}/{repo_slug}/pipelines_config/ssh/key_pair
- "List all known_hosts?" -> GET /repositories/{workspace}/{repo_slug}/pipelines_config/ssh/known_hosts
- "Create a known_host?" -> POST /repositories/{workspace}/{repo_slug}/pipelines_config/ssh/known_hosts
- "Get known_host details?" -> GET /repositories/{workspace}/{repo_slug}/pipelines_config/ssh/known_hosts/{known_host_uuid}
- "Update a known_host?" -> PUT /repositories/{workspace}/{repo_slug}/pipelines_config/ssh/known_hosts/{known_host_uuid}
- "Delete a known_host?" -> DELETE /repositories/{workspace}/{repo_slug}/pipelines_config/ssh/known_hosts/{known_host_uuid}
- "List all variables?" -> GET /repositories/{workspace}/{repo_slug}/pipelines_config/variables
- "Create a variable?" -> POST /repositories/{workspace}/{repo_slug}/pipelines_config/variables
- "Get variable details?" -> GET /repositories/{workspace}/{repo_slug}/pipelines_config/variables/{variable_uuid}
- "Update a variable?" -> PUT /repositories/{workspace}/{repo_slug}/pipelines_config/variables/{variable_uuid}
- "Delete a variable?" -> DELETE /repositories/{workspace}/{repo_slug}/pipelines_config/variables/{variable_uuid}
- "Update a property?" -> PUT /repositories/{workspace}/{repo_slug}/properties/{app_key}/{property_name}
- "Delete a property?" -> DELETE /repositories/{workspace}/{repo_slug}/properties/{app_key}/{property_name}
- "Get property details?" -> GET /repositories/{workspace}/{repo_slug}/properties/{app_key}/{property_name}
- "List all pullrequests?" -> GET /repositories/{workspace}/{repo_slug}/pullrequests
- "Create a pullrequest?" -> POST /repositories/{workspace}/{repo_slug}/pullrequests
- "List all activity?" -> GET /repositories/{workspace}/{repo_slug}/pullrequests/activity
- "Get pullrequest details?" -> GET /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}
- "Update a pullrequest?" -> PUT /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}
- "List all activity?" -> GET /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/activity
- "Create a approve?" -> POST /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/approve
- "List all comments?" -> GET /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/comments
- "Create a comment?" -> POST /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/comments
- "Delete a comment?" -> DELETE /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/comments/{comment_id}
- "Get comment details?" -> GET /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/comments/{comment_id}
- "Update a comment?" -> PUT /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/comments/{comment_id}
- "Create a resolve?" -> POST /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/comments/{comment_id}/resolve
- "List all commits?" -> GET /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/commits
- "Create a decline?" -> POST /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/decline
- "List all diff?" -> GET /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/diff
- "List all diffstat?" -> GET /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/diffstat
- "Create a merge?" -> POST /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/merge
- "Get task-status details?" -> GET /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/merge/task-status/{task_id}
- "List all patch?" -> GET /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/patch
- "Create a request-change?" -> POST /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/request-changes
- "Search statuses?" -> GET /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/statuses
- "Search tasks?" -> GET /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/tasks
- "Create a task?" -> POST /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/tasks
- "Delete a task?" -> DELETE /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/tasks/{task_id}
- "Get task details?" -> GET /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/tasks/{task_id}
- "Update a task?" -> PUT /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/tasks/{task_id}
- "Update a property?" -> PUT /repositories/{workspace}/{repo_slug}/pullrequests/{pullrequest_id}/properties/{app_key}/{property_name}
- "Delete a property?" -> DELETE /repositories/{workspace}/{repo_slug}/pullrequests/{pullrequest_id}/properties/{app_key}/{property_name}
- "Get property details?" -> GET /repositories/{workspace}/{repo_slug}/pullrequests/{pullrequest_id}/properties/{app_key}/{property_name}
- "Search refs?" -> GET /repositories/{workspace}/{repo_slug}/refs
- "Search branches?" -> GET /repositories/{workspace}/{repo_slug}/refs/branches
- "Create a branche?" -> POST /repositories/{workspace}/{repo_slug}/refs/branches
- "Delete a branche?" -> DELETE /repositories/{workspace}/{repo_slug}/refs/branches/{name}
- "Get branche details?" -> GET /repositories/{workspace}/{repo_slug}/refs/branches/{name}
- "Search tags?" -> GET /repositories/{workspace}/{repo_slug}/refs/tags
- "Create a tag?" -> POST /repositories/{workspace}/{repo_slug}/refs/tags
- "Delete a tag?" -> DELETE /repositories/{workspace}/{repo_slug}/refs/tags/{name}
- "Get tag details?" -> GET /repositories/{workspace}/{repo_slug}/refs/tags/{name}
- "List all src?" -> GET /repositories/{workspace}/{repo_slug}/src
- "Create a src?" -> POST /repositories/{workspace}/{repo_slug}/src
- "Search src?" -> GET /repositories/{workspace}/{repo_slug}/src/{commit}/{path}
- "List all versions?" -> GET /repositories/{workspace}/{repo_slug}/versions
- "Get version details?" -> GET /repositories/{workspace}/{repo_slug}/versions/{version_id}
- "List all watchers?" -> GET /repositories/{workspace}/{repo_slug}/watchers
- "List all snippets?" -> GET /snippets
- "Create a snippet?" -> POST /snippets
- "Get snippet details?" -> GET /snippets/{workspace}
- "Delete a snippet?" -> DELETE /snippets/{workspace}/{encoded_id}
- "Get snippet details?" -> GET /snippets/{workspace}/{encoded_id}
- "Update a snippet?" -> PUT /snippets/{workspace}/{encoded_id}
- "List all comments?" -> GET /snippets/{workspace}/{encoded_id}/comments
- "Create a comment?" -> POST /snippets/{workspace}/{encoded_id}/comments
- "Delete a comment?" -> DELETE /snippets/{workspace}/{encoded_id}/comments/{comment_id}
- "Get comment details?" -> GET /snippets/{workspace}/{encoded_id}/comments/{comment_id}
- "Update a comment?" -> PUT /snippets/{workspace}/{encoded_id}/comments/{comment_id}
- "List all commits?" -> GET /snippets/{workspace}/{encoded_id}/commits
- "Get commit details?" -> GET /snippets/{workspace}/{encoded_id}/commits/{revision}
- "Get file details?" -> GET /snippets/{workspace}/{encoded_id}/files/{path}
- "List all watch?" -> GET /snippets/{workspace}/{encoded_id}/watch
- "List all watchers?" -> GET /snippets/{workspace}/{encoded_id}/watchers
- "Delete a snippet?" -> DELETE /snippets/{workspace}/{encoded_id}/{node_id}
- "Get snippet details?" -> GET /snippets/{workspace}/{encoded_id}/{node_id}
- "Update a snippet?" -> PUT /snippets/{workspace}/{encoded_id}/{node_id}
- "Get file details?" -> GET /snippets/{workspace}/{encoded_id}/{node_id}/files/{path}
- "List all diff?" -> GET /snippets/{workspace}/{encoded_id}/{revision}/diff
- "List all patch?" -> GET /snippets/{workspace}/{encoded_id}/{revision}/patch
- "List all variables?" -> GET /teams/{username}/pipelines_config/variables
- "Create a variable?" -> POST /teams/{username}/pipelines_config/variables
- "Get variable details?" -> GET /teams/{username}/pipelines_config/variables/{variable_uuid}
- "Update a variable?" -> PUT /teams/{username}/pipelines_config/variables/{variable_uuid}
- "Delete a variable?" -> DELETE /teams/{username}/pipelines_config/variables/{variable_uuid}
- "List all code?" -> GET /teams/{username}/search/code
- "List all user?" -> GET /user
- "List all emails?" -> GET /user/emails
- "Get email details?" -> GET /user/emails/{email}
- "Search repositories?" -> GET /user/permissions/repositories
- "Search workspaces?" -> GET /user/permissions/workspaces
- "List all workspaces?" -> GET /user/workspaces
- "List all permission?" -> GET /user/workspaces/{workspace}/permission
- "Search repositories?" -> GET /user/workspaces/{workspace}/permissions/repositories
- "Get user details?" -> GET /users/{selected_user}
- "List all gpg-keys?" -> GET /users/{selected_user}/gpg-keys
- "Create a gpg-key?" -> POST /users/{selected_user}/gpg-keys
- "Delete a gpg-key?" -> DELETE /users/{selected_user}/gpg-keys/{fingerprint}
- "Get gpg-key details?" -> GET /users/{selected_user}/gpg-keys/{fingerprint}
- "List all variables?" -> GET /users/{selected_user}/pipelines_config/variables
- "Create a variable?" -> POST /users/{selected_user}/pipelines_config/variables
- "Get variable details?" -> GET /users/{selected_user}/pipelines_config/variables/{variable_uuid}
- "Update a variable?" -> PUT /users/{selected_user}/pipelines_config/variables/{variable_uuid}
- "Delete a variable?" -> DELETE /users/{selected_user}/pipelines_config/variables/{variable_uuid}
- "Update a property?" -> PUT /users/{selected_user}/properties/{app_key}/{property_name}
- "Delete a property?" -> DELETE /users/{selected_user}/properties/{app_key}/{property_name}
- "Get property details?" -> GET /users/{selected_user}/properties/{app_key}/{property_name}
- "List all code?" -> GET /users/{selected_user}/search/code
- "List all ssh-keys?" -> GET /users/{selected_user}/ssh-keys
- "Create a ssh-key?" -> POST /users/{selected_user}/ssh-keys
- "Delete a ssh-key?" -> DELETE /users/{selected_user}/ssh-keys/{key_id}
- "Get ssh-key details?" -> GET /users/{selected_user}/ssh-keys/{key_id}
- "Update a ssh-key?" -> PUT /users/{selected_user}/ssh-keys/{key_id}
- "Search workspaces?" -> GET /workspaces
- "Get workspace details?" -> GET /workspaces/{workspace}
- "List all hooks?" -> GET /workspaces/{workspace}/hooks
- "Create a hook?" -> POST /workspaces/{workspace}/hooks
- "Delete a hook?" -> DELETE /workspaces/{workspace}/hooks/{uid}
- "Get hook details?" -> GET /workspaces/{workspace}/hooks/{uid}
- "Update a hook?" -> PUT /workspaces/{workspace}/hooks/{uid}
- "List all members?" -> GET /workspaces/{workspace}/members
- "Get member details?" -> GET /workspaces/{workspace}/members/{member}
- "Search permissions?" -> GET /workspaces/{workspace}/permissions
- "Search repositories?" -> GET /workspaces/{workspace}/permissions/repositories
- "Search repositories?" -> GET /workspaces/{workspace}/permissions/repositories/{repo_slug}
- "List all openid-configuration?" -> GET /workspaces/{workspace}/pipelines-config/identity/oidc/.well-known/openid-configuration
- "List all keys.json?" -> GET /workspaces/{workspace}/pipelines-config/identity/oidc/keys.json
- "List all runners?" -> GET /workspaces/{workspace}/pipelines-config/runners
- "Create a runner?" -> POST /workspaces/{workspace}/pipelines-config/runners
- "Get runner details?" -> GET /workspaces/{workspace}/pipelines-config/runners/{runner_uuid}
- "Update a runner?" -> PUT /workspaces/{workspace}/pipelines-config/runners/{runner_uuid}
- "Delete a runner?" -> DELETE /workspaces/{workspace}/pipelines-config/runners/{runner_uuid}
- "List all variables?" -> GET /workspaces/{workspace}/pipelines-config/variables
- "Create a variable?" -> POST /workspaces/{workspace}/pipelines-config/variables
- "Get variable details?" -> GET /workspaces/{workspace}/pipelines-config/variables/{variable_uuid}
- "Update a variable?" -> PUT /workspaces/{workspace}/pipelines-config/variables/{variable_uuid}
- "Delete a variable?" -> DELETE /workspaces/{workspace}/pipelines-config/variables/{variable_uuid}
- "List all projects?" -> GET /workspaces/{workspace}/projects
- "Create a project?" -> POST /workspaces/{workspace}/projects
- "Delete a project?" -> DELETE /workspaces/{workspace}/projects/{project_key}
- "Get project details?" -> GET /workspaces/{workspace}/projects/{project_key}
- "Update a project?" -> PUT /workspaces/{workspace}/projects/{project_key}
- "List all branching-model?" -> GET /workspaces/{workspace}/projects/{project_key}/branching-model
- "List all settings?" -> GET /workspaces/{workspace}/projects/{project_key}/branching-model/settings
- "List all default-reviewers?" -> GET /workspaces/{workspace}/projects/{project_key}/default-reviewers
- "Delete a default-reviewer?" -> DELETE /workspaces/{workspace}/projects/{project_key}/default-reviewers/{selected_user}
- "Get default-reviewer details?" -> GET /workspaces/{workspace}/projects/{project_key}/default-reviewers/{selected_user}
- "Update a default-reviewer?" -> PUT /workspaces/{workspace}/projects/{project_key}/default-reviewers/{selected_user}
- "List all deploy-keys?" -> GET /workspaces/{workspace}/projects/{project_key}/deploy-keys
- "Create a deploy-key?" -> POST /workspaces/{workspace}/projects/{project_key}/deploy-keys
- "Delete a deploy-key?" -> DELETE /workspaces/{workspace}/projects/{project_key}/deploy-keys/{key_id}
- "Get deploy-key details?" -> GET /workspaces/{workspace}/projects/{project_key}/deploy-keys/{key_id}
- "List all groups?" -> GET /workspaces/{workspace}/projects/{project_key}/permissions-config/groups
- "Delete a group?" -> DELETE /workspaces/{workspace}/projects/{project_key}/permissions-config/groups/{group_slug}
- "Get group details?" -> GET /workspaces/{workspace}/projects/{project_key}/permissions-config/groups/{group_slug}
- "Update a group?" -> PUT /workspaces/{workspace}/projects/{project_key}/permissions-config/groups/{group_slug}
- "List all users?" -> GET /workspaces/{workspace}/projects/{project_key}/permissions-config/users
- "Delete a user?" -> DELETE /workspaces/{workspace}/projects/{project_key}/permissions-config/users/{selected_user_id}
- "Get user details?" -> GET /workspaces/{workspace}/projects/{project_key}/permissions-config/users/{selected_user_id}
- "Update a user?" -> PUT /workspaces/{workspace}/projects/{project_key}/permissions-config/users/{selected_user_id}
- "Get pullrequest details?" -> GET /workspaces/{workspace}/pullrequests/{selected_user}
- "List all code?" -> GET /workspaces/{workspace}/search/code
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
