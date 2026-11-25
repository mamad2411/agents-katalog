---
name: github-v3-rest-api
description: "GitHub v3 REST API skill. Use when working with GitHub v3 REST for root, advisories, app. Covers 1079 endpoints."
version: 1.0.0
generator: lapsh
---

# GitHub v3 REST API
API version: 1.1.4

## Auth
ApiKey filter in query

## Base URL
https://api.github.com

## Setup
1. Set your API key in the appropriate header
2. GET / -- verify access
3. POST /app-manifests/{code}/conversions -- create first conversions

## Endpoints

1079 endpoints across 36 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| GET | / | GitHub API Root |

### advisories
| Method | Path | Description |
|--------|------|-------------|
| GET | /advisories | List global security advisories |
| GET | /advisories/{ghsa_id} | Get a global security advisory |

### app
| Method | Path | Description |
|--------|------|-------------|
| GET | /app | Get the authenticated app |
| GET | /app/hook/config | Get a webhook configuration for an app |
| PATCH | /app/hook/config | Update a webhook configuration for an app |
| GET | /app/hook/deliveries | List deliveries for an app webhook |
| GET | /app/hook/deliveries/{delivery_id} | Get a delivery for an app webhook |
| POST | /app/hook/deliveries/{delivery_id}/attempts | Redeliver a delivery for an app webhook |
| GET | /app/installation-requests | List installation requests for the authenticated app |
| GET | /app/installations | List installations for the authenticated app |
| GET | /app/installations/{installation_id} | Get an installation for the authenticated app |
| DELETE | /app/installations/{installation_id} | Delete an installation for the authenticated app |
| POST | /app/installations/{installation_id}/access_tokens | Create an installation access token for an app |
| PUT | /app/installations/{installation_id}/suspended | Suspend an app installation |
| DELETE | /app/installations/{installation_id}/suspended | Unsuspend an app installation |

### app-manifests
| Method | Path | Description |
|--------|------|-------------|
| POST | /app-manifests/{code}/conversions | Create a GitHub App from a manifest |

### applications
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /applications/{client_id}/grant | Delete an app authorization |
| POST | /applications/{client_id}/token | Check a token |
| PATCH | /applications/{client_id}/token | Reset a token |
| DELETE | /applications/{client_id}/token | Delete an app token |
| POST | /applications/{client_id}/token/scoped | Create a scoped access token |

### apps
| Method | Path | Description |
|--------|------|-------------|
| GET | /apps/{app_slug} | Get an app |

### assignments
| Method | Path | Description |
|--------|------|-------------|
| GET | /assignments/{assignment_id} | Get an assignment |
| GET | /assignments/{assignment_id}/accepted_assignments | List accepted assignments for an assignment |
| GET | /assignments/{assignment_id}/grades | Get assignment grades |

### classrooms
| Method | Path | Description |
|--------|------|-------------|
| GET | /classrooms | List classrooms |
| GET | /classrooms/{classroom_id} | Get a classroom |
| GET | /classrooms/{classroom_id}/assignments | List assignments for a classroom |

### codes_of_conduct
| Method | Path | Description |
|--------|------|-------------|
| GET | /codes_of_conduct | Get all codes of conduct |
| GET | /codes_of_conduct/{key} | Get a code of conduct |

### credentials
| Method | Path | Description |
|--------|------|-------------|
| POST | /credentials/revoke | Revoke a list of credentials |

### emojis
| Method | Path | Description |
|--------|------|-------------|
| GET | /emojis | Get emojis |

### enterprises
| Method | Path | Description |
|--------|------|-------------|
| GET | /enterprises/{enterprise}/actions/cache/retention-limit | Get GitHub Actions cache retention limit for an enterprise |
| PUT | /enterprises/{enterprise}/actions/cache/retention-limit | Set GitHub Actions cache retention limit for an enterprise |
| GET | /enterprises/{enterprise}/actions/cache/storage-limit | Get GitHub Actions cache storage limit for an enterprise |
| PUT | /enterprises/{enterprise}/actions/cache/storage-limit | Set GitHub Actions cache storage limit for an enterprise |
| GET | /enterprises/{enterprise}/code-security/configurations | Get code security configurations for an enterprise |
| POST | /enterprises/{enterprise}/code-security/configurations | Create a code security configuration for an enterprise |
| GET | /enterprises/{enterprise}/code-security/configurations/defaults | Get default code security configurations for an enterprise |
| GET | /enterprises/{enterprise}/code-security/configurations/{configuration_id} | Retrieve a code security configuration of an enterprise |
| PATCH | /enterprises/{enterprise}/code-security/configurations/{configuration_id} | Update a custom code security configuration for an enterprise |
| DELETE | /enterprises/{enterprise}/code-security/configurations/{configuration_id} | Delete a code security configuration for an enterprise |
| POST | /enterprises/{enterprise}/code-security/configurations/{configuration_id}/attach | Attach an enterprise configuration to repositories |
| PUT | /enterprises/{enterprise}/code-security/configurations/{configuration_id}/defaults | Set a code security configuration as a default for an enterprise |
| GET | /enterprises/{enterprise}/code-security/configurations/{configuration_id}/repositories | Get repositories associated with an enterprise code security configuration |
| GET | /enterprises/{enterprise}/dependabot/alerts | List Dependabot alerts for an enterprise |
| GET | /enterprises/{enterprise}/teams | List enterprise teams |
| POST | /enterprises/{enterprise}/teams | Create an enterprise team |
| GET | /enterprises/{enterprise}/teams/{enterprise-team}/memberships | List members in an enterprise team |
| POST | /enterprises/{enterprise}/teams/{enterprise-team}/memberships/add | Bulk add team members |
| POST | /enterprises/{enterprise}/teams/{enterprise-team}/memberships/remove | Bulk remove team members |
| GET | /enterprises/{enterprise}/teams/{enterprise-team}/memberships/{username} | Get enterprise team membership |
| PUT | /enterprises/{enterprise}/teams/{enterprise-team}/memberships/{username} | Add team member |
| DELETE | /enterprises/{enterprise}/teams/{enterprise-team}/memberships/{username} | Remove team membership |
| GET | /enterprises/{enterprise}/teams/{enterprise-team}/organizations | Get organization assignments |
| POST | /enterprises/{enterprise}/teams/{enterprise-team}/organizations/add | Add organization assignments |
| POST | /enterprises/{enterprise}/teams/{enterprise-team}/organizations/remove | Remove organization assignments |
| GET | /enterprises/{enterprise}/teams/{enterprise-team}/organizations/{org} | Get organization assignment |
| PUT | /enterprises/{enterprise}/teams/{enterprise-team}/organizations/{org} | Add an organization assignment |
| DELETE | /enterprises/{enterprise}/teams/{enterprise-team}/organizations/{org} | Delete an organization assignment |
| GET | /enterprises/{enterprise}/teams/{team_slug} | Get an enterprise team |
| PATCH | /enterprises/{enterprise}/teams/{team_slug} | Update an enterprise team |
| DELETE | /enterprises/{enterprise}/teams/{team_slug} | Delete an enterprise team |

### events
| Method | Path | Description |
|--------|------|-------------|
| GET | /events | List public events |

### feeds
| Method | Path | Description |
|--------|------|-------------|
| GET | /feeds | Get feeds |

### gists
| Method | Path | Description |
|--------|------|-------------|
| GET | /gists | List gists for the authenticated user |
| POST | /gists | Create a gist |
| GET | /gists/public | List public gists |
| GET | /gists/starred | List starred gists |
| GET | /gists/{gist_id} | Get a gist |
| PATCH | /gists/{gist_id} | Update a gist |
| DELETE | /gists/{gist_id} | Delete a gist |
| GET | /gists/{gist_id}/comments | List gist comments |
| POST | /gists/{gist_id}/comments | Create a gist comment |
| GET | /gists/{gist_id}/comments/{comment_id} | Get a gist comment |
| PATCH | /gists/{gist_id}/comments/{comment_id} | Update a gist comment |
| DELETE | /gists/{gist_id}/comments/{comment_id} | Delete a gist comment |
| GET | /gists/{gist_id}/commits | List gist commits |
| GET | /gists/{gist_id}/forks | List gist forks |
| POST | /gists/{gist_id}/forks | Fork a gist |
| GET | /gists/{gist_id}/star | Check if a gist is starred |
| PUT | /gists/{gist_id}/star | Star a gist |
| DELETE | /gists/{gist_id}/star | Unstar a gist |
| GET | /gists/{gist_id}/{sha} | Get a gist revision |

### gitignore
| Method | Path | Description |
|--------|------|-------------|
| GET | /gitignore/templates | Get all gitignore templates |
| GET | /gitignore/templates/{name} | Get a gitignore template |

### installation
| Method | Path | Description |
|--------|------|-------------|
| GET | /installation/repositories | List repositories accessible to the app installation |
| DELETE | /installation/token | Revoke an installation access token |

### issues
| Method | Path | Description |
|--------|------|-------------|
| GET | /issues | List issues assigned to the authenticated user |

### licenses
| Method | Path | Description |
|--------|------|-------------|
| GET | /licenses | Get all commonly used licenses |
| GET | /licenses/{license} | Get a license |

### markdown
| Method | Path | Description |
|--------|------|-------------|
| POST | /markdown | Render a Markdown document |
| POST | /markdown/raw | Render a Markdown document in raw mode |

### marketplace_listing
| Method | Path | Description |
|--------|------|-------------|
| GET | /marketplace_listing/accounts/{account_id} | Get a subscription plan for an account |
| GET | /marketplace_listing/plans | List plans |
| GET | /marketplace_listing/plans/{plan_id}/accounts | List accounts for a plan |
| GET | /marketplace_listing/stubbed/accounts/{account_id} | Get a subscription plan for an account (stubbed) |
| GET | /marketplace_listing/stubbed/plans | List plans (stubbed) |
| GET | /marketplace_listing/stubbed/plans/{plan_id}/accounts | List accounts for a plan (stubbed) |

### meta
| Method | Path | Description |
|--------|------|-------------|
| GET | /meta | Get GitHub meta information |

### networks
| Method | Path | Description |
|--------|------|-------------|
| GET | /networks/{owner}/{repo}/events | List public events for a network of repositories |

### notifications
| Method | Path | Description |
|--------|------|-------------|
| GET | /notifications | List notifications for the authenticated user |
| PUT | /notifications | Mark notifications as read |
| GET | /notifications/threads/{thread_id} | Get a thread |
| PATCH | /notifications/threads/{thread_id} | Mark a thread as read |
| DELETE | /notifications/threads/{thread_id} | Mark a thread as done |
| GET | /notifications/threads/{thread_id}/subscription | Get a thread subscription for the authenticated user |
| PUT | /notifications/threads/{thread_id}/subscription | Set a thread subscription |
| DELETE | /notifications/threads/{thread_id}/subscription | Delete a thread subscription |

### octocat
| Method | Path | Description |
|--------|------|-------------|
| GET | /octocat | Get Octocat |

### organizations
| Method | Path | Description |
|--------|------|-------------|
| GET | /organizations | List organizations |
| GET | /organizations/{org}/actions/cache/retention-limit | Get GitHub Actions cache retention limit for an organization |
| PUT | /organizations/{org}/actions/cache/retention-limit | Set GitHub Actions cache retention limit for an organization |
| GET | /organizations/{org}/actions/cache/storage-limit | Get GitHub Actions cache storage limit for an organization |
| PUT | /organizations/{org}/actions/cache/storage-limit | Set GitHub Actions cache storage limit for an organization |
| GET | /organizations/{org}/dependabot/repository-access | Lists the repositories Dependabot can access in an organization |
| PATCH | /organizations/{org}/dependabot/repository-access | Updates Dependabot's repository access list for an organization |
| PUT | /organizations/{org}/dependabot/repository-access/default-level | Set the default repository access level for Dependabot |
| GET | /organizations/{org}/settings/billing/budgets | Get all budgets for an organization |
| GET | /organizations/{org}/settings/billing/budgets/{budget_id} | Get a budget by ID for an organization |
| PATCH | /organizations/{org}/settings/billing/budgets/{budget_id} | Update a budget for an organization |
| DELETE | /organizations/{org}/settings/billing/budgets/{budget_id} | Delete a budget for an organization |
| GET | /organizations/{org}/settings/billing/premium_request/usage | Get billing premium request usage report for an organization |
| GET | /organizations/{org}/settings/billing/usage | Get billing usage report for an organization |
| GET | /organizations/{org}/settings/billing/usage/summary | Get billing usage summary for an organization |

### orgs
| Method | Path | Description |
|--------|------|-------------|
| GET | /orgs/{org} | Get an organization |
| PATCH | /orgs/{org} | Update an organization |
| DELETE | /orgs/{org} | Delete an organization |
| GET | /orgs/{org}/actions/cache/usage | Get GitHub Actions cache usage for an organization |
| GET | /orgs/{org}/actions/cache/usage-by-repository | List repositories with GitHub Actions cache usage for an organization |
| GET | /orgs/{org}/actions/hosted-runners | List GitHub-hosted runners for an organization |
| POST | /orgs/{org}/actions/hosted-runners | Create a GitHub-hosted runner for an organization |
| GET | /orgs/{org}/actions/hosted-runners/images/custom | List custom images for an organization |
| GET | /orgs/{org}/actions/hosted-runners/images/custom/{image_definition_id} | Get a custom image definition for GitHub Actions Hosted Runners |
| DELETE | /orgs/{org}/actions/hosted-runners/images/custom/{image_definition_id} | Delete a custom image from the organization |
| GET | /orgs/{org}/actions/hosted-runners/images/custom/{image_definition_id}/versions | List image versions of a custom image for an organization |
| GET | /orgs/{org}/actions/hosted-runners/images/custom/{image_definition_id}/versions/{version} | Get an image version of a custom image for GitHub Actions Hosted Runners |
| DELETE | /orgs/{org}/actions/hosted-runners/images/custom/{image_definition_id}/versions/{version} | Delete an image version of custom image from the organization |
| GET | /orgs/{org}/actions/hosted-runners/images/github-owned | Get GitHub-owned images for GitHub-hosted runners in an organization |
| GET | /orgs/{org}/actions/hosted-runners/images/partner | Get partner images for GitHub-hosted runners in an organization |
| GET | /orgs/{org}/actions/hosted-runners/limits | Get limits on GitHub-hosted runners for an organization |
| GET | /orgs/{org}/actions/hosted-runners/machine-sizes | Get GitHub-hosted runners machine specs for an organization |
| GET | /orgs/{org}/actions/hosted-runners/platforms | Get platforms for GitHub-hosted runners in an organization |
| GET | /orgs/{org}/actions/hosted-runners/{hosted_runner_id} | Get a GitHub-hosted runner for an organization |
| PATCH | /orgs/{org}/actions/hosted-runners/{hosted_runner_id} | Update a GitHub-hosted runner for an organization |
| DELETE | /orgs/{org}/actions/hosted-runners/{hosted_runner_id} | Delete a GitHub-hosted runner for an organization |
| GET | /orgs/{org}/actions/oidc/customization/sub | Get the customization template for an OIDC subject claim for an organization |
| PUT | /orgs/{org}/actions/oidc/customization/sub | Set the customization template for an OIDC subject claim for an organization |
| GET | /orgs/{org}/actions/permissions | Get GitHub Actions permissions for an organization |
| PUT | /orgs/{org}/actions/permissions | Set GitHub Actions permissions for an organization |
| GET | /orgs/{org}/actions/permissions/artifact-and-log-retention | Get artifact and log retention settings for an organization |
| PUT | /orgs/{org}/actions/permissions/artifact-and-log-retention | Set artifact and log retention settings for an organization |
| GET | /orgs/{org}/actions/permissions/fork-pr-contributor-approval | Get fork PR contributor approval permissions for an organization |
| PUT | /orgs/{org}/actions/permissions/fork-pr-contributor-approval | Set fork PR contributor approval permissions for an organization |
| GET | /orgs/{org}/actions/permissions/fork-pr-workflows-private-repos | Get private repo fork PR workflow settings for an organization |
| PUT | /orgs/{org}/actions/permissions/fork-pr-workflows-private-repos | Set private repo fork PR workflow settings for an organization |
| GET | /orgs/{org}/actions/permissions/repositories | List selected repositories enabled for GitHub Actions in an organization |
| PUT | /orgs/{org}/actions/permissions/repositories | Set selected repositories enabled for GitHub Actions in an organization |
| PUT | /orgs/{org}/actions/permissions/repositories/{repository_id} | Enable a selected repository for GitHub Actions in an organization |
| DELETE | /orgs/{org}/actions/permissions/repositories/{repository_id} | Disable a selected repository for GitHub Actions in an organization |
| GET | /orgs/{org}/actions/permissions/selected-actions | Get allowed actions and reusable workflows for an organization |
| PUT | /orgs/{org}/actions/permissions/selected-actions | Set allowed actions and reusable workflows for an organization |
| GET | /orgs/{org}/actions/permissions/self-hosted-runners | Get self-hosted runners settings for an organization |
| PUT | /orgs/{org}/actions/permissions/self-hosted-runners | Set self-hosted runners settings for an organization |
| GET | /orgs/{org}/actions/permissions/self-hosted-runners/repositories | List repositories allowed to use self-hosted runners in an organization |
| PUT | /orgs/{org}/actions/permissions/self-hosted-runners/repositories | Set repositories allowed to use self-hosted runners in an organization |
| PUT | /orgs/{org}/actions/permissions/self-hosted-runners/repositories/{repository_id} | Add a repository to the list of repositories allowed to use self-hosted runners in an organization |
| DELETE | /orgs/{org}/actions/permissions/self-hosted-runners/repositories/{repository_id} | Remove a repository from the list of repositories allowed to use self-hosted runners in an organization |
| GET | /orgs/{org}/actions/permissions/workflow | Get default workflow permissions for an organization |
| PUT | /orgs/{org}/actions/permissions/workflow | Set default workflow permissions for an organization |
| GET | /orgs/{org}/actions/runner-groups | List self-hosted runner groups for an organization |
| POST | /orgs/{org}/actions/runner-groups | Create a self-hosted runner group for an organization |
| GET | /orgs/{org}/actions/runner-groups/{runner_group_id} | Get a self-hosted runner group for an organization |
| PATCH | /orgs/{org}/actions/runner-groups/{runner_group_id} | Update a self-hosted runner group for an organization |
| DELETE | /orgs/{org}/actions/runner-groups/{runner_group_id} | Delete a self-hosted runner group from an organization |
| GET | /orgs/{org}/actions/runner-groups/{runner_group_id}/hosted-runners | List GitHub-hosted runners in a group for an organization |
| GET | /orgs/{org}/actions/runner-groups/{runner_group_id}/repositories | List repository access to a self-hosted runner group in an organization |
| PUT | /orgs/{org}/actions/runner-groups/{runner_group_id}/repositories | Set repository access for a self-hosted runner group in an organization |
| PUT | /orgs/{org}/actions/runner-groups/{runner_group_id}/repositories/{repository_id} | Add repository access to a self-hosted runner group in an organization |
| DELETE | /orgs/{org}/actions/runner-groups/{runner_group_id}/repositories/{repository_id} | Remove repository access to a self-hosted runner group in an organization |
| GET | /orgs/{org}/actions/runner-groups/{runner_group_id}/runners | List self-hosted runners in a group for an organization |
| PUT | /orgs/{org}/actions/runner-groups/{runner_group_id}/runners | Set self-hosted runners in a group for an organization |
| PUT | /orgs/{org}/actions/runner-groups/{runner_group_id}/runners/{runner_id} | Add a self-hosted runner to a group for an organization |
| DELETE | /orgs/{org}/actions/runner-groups/{runner_group_id}/runners/{runner_id} | Remove a self-hosted runner from a group for an organization |
| GET | /orgs/{org}/actions/runners | List self-hosted runners for an organization |
| GET | /orgs/{org}/actions/runners/downloads | List runner applications for an organization |
| POST | /orgs/{org}/actions/runners/generate-jitconfig | Create configuration for a just-in-time runner for an organization |
| POST | /orgs/{org}/actions/runners/registration-token | Create a registration token for an organization |
| POST | /orgs/{org}/actions/runners/remove-token | Create a remove token for an organization |
| GET | /orgs/{org}/actions/runners/{runner_id} | Get a self-hosted runner for an organization |
| DELETE | /orgs/{org}/actions/runners/{runner_id} | Delete a self-hosted runner from an organization |
| GET | /orgs/{org}/actions/runners/{runner_id}/labels | List labels for a self-hosted runner for an organization |
| POST | /orgs/{org}/actions/runners/{runner_id}/labels | Add custom labels to a self-hosted runner for an organization |
| PUT | /orgs/{org}/actions/runners/{runner_id}/labels | Set custom labels for a self-hosted runner for an organization |
| DELETE | /orgs/{org}/actions/runners/{runner_id}/labels | Remove all custom labels from a self-hosted runner for an organization |
| DELETE | /orgs/{org}/actions/runners/{runner_id}/labels/{name} | Remove a custom label from a self-hosted runner for an organization |
| GET | /orgs/{org}/actions/secrets | List organization secrets |
| GET | /orgs/{org}/actions/secrets/public-key | Get an organization public key |
| GET | /orgs/{org}/actions/secrets/{secret_name} | Get an organization secret |
| PUT | /orgs/{org}/actions/secrets/{secret_name} | Create or update an organization secret |
| DELETE | /orgs/{org}/actions/secrets/{secret_name} | Delete an organization secret |
| GET | /orgs/{org}/actions/secrets/{secret_name}/repositories | List selected repositories for an organization secret |
| PUT | /orgs/{org}/actions/secrets/{secret_name}/repositories | Set selected repositories for an organization secret |
| PUT | /orgs/{org}/actions/secrets/{secret_name}/repositories/{repository_id} | Add selected repository to an organization secret |
| DELETE | /orgs/{org}/actions/secrets/{secret_name}/repositories/{repository_id} | Remove selected repository from an organization secret |
| GET | /orgs/{org}/actions/variables | List organization variables |
| POST | /orgs/{org}/actions/variables | Create an organization variable |
| GET | /orgs/{org}/actions/variables/{name} | Get an organization variable |
| PATCH | /orgs/{org}/actions/variables/{name} | Update an organization variable |
| DELETE | /orgs/{org}/actions/variables/{name} | Delete an organization variable |
| GET | /orgs/{org}/actions/variables/{name}/repositories | List selected repositories for an organization variable |
| PUT | /orgs/{org}/actions/variables/{name}/repositories | Set selected repositories for an organization variable |
| PUT | /orgs/{org}/actions/variables/{name}/repositories/{repository_id} | Add selected repository to an organization variable |
| DELETE | /orgs/{org}/actions/variables/{name}/repositories/{repository_id} | Remove selected repository from an organization variable |
| POST | /orgs/{org}/artifacts/metadata/deployment-record | Create an artifact deployment record |
| POST | /orgs/{org}/artifacts/metadata/deployment-record/cluster/{cluster} | Set cluster deployment records |
| POST | /orgs/{org}/artifacts/metadata/storage-record | Create artifact metadata storage record |
| GET | /orgs/{org}/artifacts/{subject_digest}/metadata/deployment-records | List artifact deployment records |
| GET | /orgs/{org}/artifacts/{subject_digest}/metadata/storage-records | List artifact storage records |
| POST | /orgs/{org}/attestations/bulk-list | List attestations by bulk subject digests |
| POST | /orgs/{org}/attestations/delete-request | Delete attestations in bulk |
| DELETE | /orgs/{org}/attestations/digest/{subject_digest} | Delete attestations by subject digest |
| GET | /orgs/{org}/attestations/repositories | List attestation repositories |
| DELETE | /orgs/{org}/attestations/{attestation_id} | Delete attestations by ID |
| GET | /orgs/{org}/attestations/{subject_digest} | List attestations |
| GET | /orgs/{org}/blocks | List users blocked by an organization |
| GET | /orgs/{org}/blocks/{username} | Check if a user is blocked by an organization |
| PUT | /orgs/{org}/blocks/{username} | Block a user from an organization |
| DELETE | /orgs/{org}/blocks/{username} | Unblock a user from an organization |
| GET | /orgs/{org}/campaigns | List campaigns for an organization |
| POST | /orgs/{org}/campaigns | Create a campaign for an organization |
| GET | /orgs/{org}/campaigns/{campaign_number} | Get a campaign for an organization |
| PATCH | /orgs/{org}/campaigns/{campaign_number} | Update a campaign |
| DELETE | /orgs/{org}/campaigns/{campaign_number} | Delete a campaign for an organization |
| GET | /orgs/{org}/code-scanning/alerts | List code scanning alerts for an organization |
| GET | /orgs/{org}/code-security/configurations | Get code security configurations for an organization |
| POST | /orgs/{org}/code-security/configurations | Create a code security configuration |
| GET | /orgs/{org}/code-security/configurations/defaults | Get default code security configurations |
| DELETE | /orgs/{org}/code-security/configurations/detach | Detach configurations from repositories |
| GET | /orgs/{org}/code-security/configurations/{configuration_id} | Get a code security configuration |
| PATCH | /orgs/{org}/code-security/configurations/{configuration_id} | Update a code security configuration |
| DELETE | /orgs/{org}/code-security/configurations/{configuration_id} | Delete a code security configuration |
| POST | /orgs/{org}/code-security/configurations/{configuration_id}/attach | Attach a configuration to repositories |
| PUT | /orgs/{org}/code-security/configurations/{configuration_id}/defaults | Set a code security configuration as a default for an organization |
| GET | /orgs/{org}/code-security/configurations/{configuration_id}/repositories | Get repositories associated with a code security configuration |
| GET | /orgs/{org}/codespaces | List codespaces for the organization |
| PUT | /orgs/{org}/codespaces/access | Manage access control for organization codespaces |
| POST | /orgs/{org}/codespaces/access/selected_users | Add users to Codespaces access for an organization |
| DELETE | /orgs/{org}/codespaces/access/selected_users | Remove users from Codespaces access for an organization |
| GET | /orgs/{org}/codespaces/secrets | List organization secrets |
| GET | /orgs/{org}/codespaces/secrets/public-key | Get an organization public key |
| GET | /orgs/{org}/codespaces/secrets/{secret_name} | Get an organization secret |
| PUT | /orgs/{org}/codespaces/secrets/{secret_name} | Create or update an organization secret |
| DELETE | /orgs/{org}/codespaces/secrets/{secret_name} | Delete an organization secret |
| GET | /orgs/{org}/codespaces/secrets/{secret_name}/repositories | List selected repositories for an organization secret |
| PUT | /orgs/{org}/codespaces/secrets/{secret_name}/repositories | Set selected repositories for an organization secret |
| PUT | /orgs/{org}/codespaces/secrets/{secret_name}/repositories/{repository_id} | Add selected repository to an organization secret |
| DELETE | /orgs/{org}/codespaces/secrets/{secret_name}/repositories/{repository_id} | Remove selected repository from an organization secret |
| GET | /orgs/{org}/copilot/billing | Get Copilot seat information and settings for an organization |
| GET | /orgs/{org}/copilot/billing/seats | List all Copilot seat assignments for an organization |
| POST | /orgs/{org}/copilot/billing/selected_teams | Add teams to the Copilot subscription for an organization |
| DELETE | /orgs/{org}/copilot/billing/selected_teams | Remove teams from the Copilot subscription for an organization |
| POST | /orgs/{org}/copilot/billing/selected_users | Add users to the Copilot subscription for an organization |
| DELETE | /orgs/{org}/copilot/billing/selected_users | Remove users from the Copilot subscription for an organization |
| GET | /orgs/{org}/copilot/content_exclusion | Get Copilot content exclusion rules for an organization |
| PUT | /orgs/{org}/copilot/content_exclusion | Set Copilot content exclusion rules for an organization |
| GET | /orgs/{org}/copilot/metrics | Get Copilot metrics for an organization |
| GET | /orgs/{org}/dependabot/alerts | List Dependabot alerts for an organization |
| GET | /orgs/{org}/dependabot/secrets | List organization secrets |
| GET | /orgs/{org}/dependabot/secrets/public-key | Get an organization public key |
| GET | /orgs/{org}/dependabot/secrets/{secret_name} | Get an organization secret |
| PUT | /orgs/{org}/dependabot/secrets/{secret_name} | Create or update an organization secret |
| DELETE | /orgs/{org}/dependabot/secrets/{secret_name} | Delete an organization secret |
| GET | /orgs/{org}/dependabot/secrets/{secret_name}/repositories | List selected repositories for an organization secret |
| PUT | /orgs/{org}/dependabot/secrets/{secret_name}/repositories | Set selected repositories for an organization secret |
| PUT | /orgs/{org}/dependabot/secrets/{secret_name}/repositories/{repository_id} | Add selected repository to an organization secret |
| DELETE | /orgs/{org}/dependabot/secrets/{secret_name}/repositories/{repository_id} | Remove selected repository from an organization secret |
| GET | /orgs/{org}/docker/conflicts | Get list of conflicting packages during Docker migration for organization |
| GET | /orgs/{org}/events | List public organization events |
| GET | /orgs/{org}/failed_invitations | List failed organization invitations |
| GET | /orgs/{org}/hooks | List organization webhooks |
| POST | /orgs/{org}/hooks | Create an organization webhook |
| GET | /orgs/{org}/hooks/{hook_id} | Get an organization webhook |
| PATCH | /orgs/{org}/hooks/{hook_id} | Update an organization webhook |
| DELETE | /orgs/{org}/hooks/{hook_id} | Delete an organization webhook |
| GET | /orgs/{org}/hooks/{hook_id}/config | Get a webhook configuration for an organization |
| PATCH | /orgs/{org}/hooks/{hook_id}/config | Update a webhook configuration for an organization |
| GET | /orgs/{org}/hooks/{hook_id}/deliveries | List deliveries for an organization webhook |
| GET | /orgs/{org}/hooks/{hook_id}/deliveries/{delivery_id} | Get a webhook delivery for an organization webhook |
| POST | /orgs/{org}/hooks/{hook_id}/deliveries/{delivery_id}/attempts | Redeliver a delivery for an organization webhook |
| POST | /orgs/{org}/hooks/{hook_id}/pings | Ping an organization webhook |
| GET | /orgs/{org}/insights/api/route-stats/{actor_type}/{actor_id} | Get route stats by actor |
| GET | /orgs/{org}/insights/api/subject-stats | Get subject stats |
| GET | /orgs/{org}/insights/api/summary-stats | Get summary stats |
| GET | /orgs/{org}/insights/api/summary-stats/users/{user_id} | Get summary stats by user |
| GET | /orgs/{org}/insights/api/summary-stats/{actor_type}/{actor_id} | Get summary stats by actor |
| GET | /orgs/{org}/insights/api/time-stats | Get time stats |
| GET | /orgs/{org}/insights/api/time-stats/users/{user_id} | Get time stats by user |
| GET | /orgs/{org}/insights/api/time-stats/{actor_type}/{actor_id} | Get time stats by actor |
| GET | /orgs/{org}/insights/api/user-stats/{user_id} | Get user stats |
| GET | /orgs/{org}/installation | Get an organization installation for the authenticated app |
| GET | /orgs/{org}/installations | List app installations for an organization |
| GET | /orgs/{org}/interaction-limits | Get interaction restrictions for an organization |
| PUT | /orgs/{org}/interaction-limits | Set interaction restrictions for an organization |
| DELETE | /orgs/{org}/interaction-limits | Remove interaction restrictions for an organization |
| GET | /orgs/{org}/invitations | List pending organization invitations |
| POST | /orgs/{org}/invitations | Create an organization invitation |
| DELETE | /orgs/{org}/invitations/{invitation_id} | Cancel an organization invitation |
| GET | /orgs/{org}/invitations/{invitation_id}/teams | List organization invitation teams |
| GET | /orgs/{org}/issue-types | List issue types for an organization |
| POST | /orgs/{org}/issue-types | Create issue type for an organization |
| PUT | /orgs/{org}/issue-types/{issue_type_id} | Update issue type for an organization |
| DELETE | /orgs/{org}/issue-types/{issue_type_id} | Delete issue type for an organization |
| GET | /orgs/{org}/issues | List organization issues assigned to the authenticated user |
| GET | /orgs/{org}/members | List organization members |
| GET | /orgs/{org}/members/{username} | Check organization membership for a user |
| DELETE | /orgs/{org}/members/{username} | Remove an organization member |
| GET | /orgs/{org}/members/{username}/codespaces | List codespaces for a user in organization |
| DELETE | /orgs/{org}/members/{username}/codespaces/{codespace_name} | Delete a codespace from the organization |
| POST | /orgs/{org}/members/{username}/codespaces/{codespace_name}/stop | Stop a codespace for an organization user |
| GET | /orgs/{org}/members/{username}/copilot | Get Copilot seat assignment details for a user |
| GET | /orgs/{org}/memberships/{username} | Get organization membership for a user |
| PUT | /orgs/{org}/memberships/{username} | Set organization membership for a user |
| DELETE | /orgs/{org}/memberships/{username} | Remove organization membership for a user |
| GET | /orgs/{org}/migrations | List organization migrations |
| POST | /orgs/{org}/migrations | Start an organization migration |
| GET | /orgs/{org}/migrations/{migration_id} | Get an organization migration status |
| GET | /orgs/{org}/migrations/{migration_id}/archive | Download an organization migration archive |
| DELETE | /orgs/{org}/migrations/{migration_id}/archive | Delete an organization migration archive |
| DELETE | /orgs/{org}/migrations/{migration_id}/repos/{repo_name}/lock | Unlock an organization repository |
| GET | /orgs/{org}/migrations/{migration_id}/repositories | List repositories in an organization migration |
| GET | /orgs/{org}/organization-roles | Get all organization roles for an organization |
| DELETE | /orgs/{org}/organization-roles/teams/{team_slug} | Remove all organization roles for a team |
| PUT | /orgs/{org}/organization-roles/teams/{team_slug}/{role_id} | Assign an organization role to a team |
| DELETE | /orgs/{org}/organization-roles/teams/{team_slug}/{role_id} | Remove an organization role from a team |
| DELETE | /orgs/{org}/organization-roles/users/{username} | Remove all organization roles for a user |
| PUT | /orgs/{org}/organization-roles/users/{username}/{role_id} | Assign an organization role to a user |
| DELETE | /orgs/{org}/organization-roles/users/{username}/{role_id} | Remove an organization role from a user |
| GET | /orgs/{org}/organization-roles/{role_id} | Get an organization role |
| GET | /orgs/{org}/organization-roles/{role_id}/teams | List teams that are assigned to an organization role |
| GET | /orgs/{org}/organization-roles/{role_id}/users | List users that are assigned to an organization role |
| GET | /orgs/{org}/outside_collaborators | List outside collaborators for an organization |
| PUT | /orgs/{org}/outside_collaborators/{username} | Convert an organization member to outside collaborator |
| DELETE | /orgs/{org}/outside_collaborators/{username} | Remove outside collaborator from an organization |
| GET | /orgs/{org}/packages | List packages for an organization |
| GET | /orgs/{org}/packages/{package_type}/{package_name} | Get a package for an organization |
| DELETE | /orgs/{org}/packages/{package_type}/{package_name} | Delete a package for an organization |
| POST | /orgs/{org}/packages/{package_type}/{package_name}/restore | Restore a package for an organization |
| GET | /orgs/{org}/packages/{package_type}/{package_name}/versions | List package versions for a package owned by an organization |
| GET | /orgs/{org}/packages/{package_type}/{package_name}/versions/{package_version_id} | Get a package version for an organization |
| DELETE | /orgs/{org}/packages/{package_type}/{package_name}/versions/{package_version_id} | Delete package version for an organization |
| POST | /orgs/{org}/packages/{package_type}/{package_name}/versions/{package_version_id}/restore | Restore package version for an organization |
| GET | /orgs/{org}/personal-access-token-requests | List requests to access organization resources with fine-grained personal access tokens |
| POST | /orgs/{org}/personal-access-token-requests | Review requests to access organization resources with fine-grained personal access tokens |
| POST | /orgs/{org}/personal-access-token-requests/{pat_request_id} | Review a request to access organization resources with a fine-grained personal access token |
| GET | /orgs/{org}/personal-access-token-requests/{pat_request_id}/repositories | List repositories requested to be accessed by a fine-grained personal access token |
| GET | /orgs/{org}/personal-access-tokens | List fine-grained personal access tokens with access to organization resources |
| POST | /orgs/{org}/personal-access-tokens | Update the access to organization resources via fine-grained personal access tokens |
| POST | /orgs/{org}/personal-access-tokens/{pat_id} | Update the access a fine-grained personal access token has to organization resources |
| GET | /orgs/{org}/personal-access-tokens/{pat_id}/repositories | List repositories a fine-grained personal access token has access to |
| GET | /orgs/{org}/private-registries | List private registries for an organization |
| POST | /orgs/{org}/private-registries | Create a private registry for an organization |
| GET | /orgs/{org}/private-registries/public-key | Get private registries public key for an organization |
| GET | /orgs/{org}/private-registries/{secret_name} | Get a private registry for an organization |
| PATCH | /orgs/{org}/private-registries/{secret_name} | Update a private registry for an organization |
| DELETE | /orgs/{org}/private-registries/{secret_name} | Delete a private registry for an organization |
| GET | /orgs/{org}/projectsV2 | List projects for organization |
| GET | /orgs/{org}/projectsV2/{project_number} | Get project for organization |
| POST | /orgs/{org}/projectsV2/{project_number}/drafts | Create draft item for organization owned project |
| GET | /orgs/{org}/projectsV2/{project_number}/fields | List project fields for organization |
| POST | /orgs/{org}/projectsV2/{project_number}/fields | Add a field to an organization-owned project. |
| GET | /orgs/{org}/projectsV2/{project_number}/fields/{field_id} | Get project field for organization |
| GET | /orgs/{org}/projectsV2/{project_number}/items | List items for an organization owned project |
| POST | /orgs/{org}/projectsV2/{project_number}/items | Add item to organization owned project |
| GET | /orgs/{org}/projectsV2/{project_number}/items/{item_id} | Get an item for an organization owned project |
| PATCH | /orgs/{org}/projectsV2/{project_number}/items/{item_id} | Update project item for organization |
| DELETE | /orgs/{org}/projectsV2/{project_number}/items/{item_id} | Delete project item for organization |
| POST | /orgs/{org}/projectsV2/{project_number}/views | Create a view for an organization-owned project |
| GET | /orgs/{org}/projectsV2/{project_number}/views/{view_number}/items | List items for an organization project view |
| GET | /orgs/{org}/properties/schema | Get all custom properties for an organization |
| PATCH | /orgs/{org}/properties/schema | Create or update custom properties for an organization |
| GET | /orgs/{org}/properties/schema/{custom_property_name} | Get a custom property for an organization |
| PUT | /orgs/{org}/properties/schema/{custom_property_name} | Create or update a custom property for an organization |
| DELETE | /orgs/{org}/properties/schema/{custom_property_name} | Remove a custom property for an organization |
| GET | /orgs/{org}/properties/values | List custom property values for organization repositories |
| PATCH | /orgs/{org}/properties/values | Create or update custom property values for organization repositories |
| GET | /orgs/{org}/public_members | List public organization members |
| GET | /orgs/{org}/public_members/{username} | Check public organization membership for a user |
| PUT | /orgs/{org}/public_members/{username} | Set public organization membership for the authenticated user |
| DELETE | /orgs/{org}/public_members/{username} | Remove public organization membership for the authenticated user |
| GET | /orgs/{org}/repos | List organization repositories |
| POST | /orgs/{org}/repos | Create an organization repository |
| GET | /orgs/{org}/rulesets | Get all organization repository rulesets |
| POST | /orgs/{org}/rulesets | Create an organization repository ruleset |
| GET | /orgs/{org}/rulesets/rule-suites | List organization rule suites |
| GET | /orgs/{org}/rulesets/rule-suites/{rule_suite_id} | Get an organization rule suite |
| GET | /orgs/{org}/rulesets/{ruleset_id} | Get an organization repository ruleset |
| PUT | /orgs/{org}/rulesets/{ruleset_id} | Update an organization repository ruleset |
| DELETE | /orgs/{org}/rulesets/{ruleset_id} | Delete an organization repository ruleset |
| GET | /orgs/{org}/rulesets/{ruleset_id}/history | Get organization ruleset history |
| GET | /orgs/{org}/rulesets/{ruleset_id}/history/{version_id} | Get organization ruleset version |
| GET | /orgs/{org}/secret-scanning/alerts | List secret scanning alerts for an organization |
| GET | /orgs/{org}/secret-scanning/pattern-configurations | List organization pattern configurations |
| PATCH | /orgs/{org}/secret-scanning/pattern-configurations | Update organization pattern configurations |
| GET | /orgs/{org}/security-advisories | List repository security advisories for an organization |
| GET | /orgs/{org}/security-managers | List security manager teams |
| PUT | /orgs/{org}/security-managers/teams/{team_slug} | Add a security manager team |
| DELETE | /orgs/{org}/security-managers/teams/{team_slug} | Remove a security manager team |
| GET | /orgs/{org}/settings/immutable-releases | Get immutable releases settings for an organization |
| PUT | /orgs/{org}/settings/immutable-releases | Set immutable releases settings for an organization |
| GET | /orgs/{org}/settings/immutable-releases/repositories | List selected repositories for immutable releases enforcement |
| PUT | /orgs/{org}/settings/immutable-releases/repositories | Set selected repositories for immutable releases enforcement |
| PUT | /orgs/{org}/settings/immutable-releases/repositories/{repository_id} | Enable a selected repository for immutable releases in an organization |
| DELETE | /orgs/{org}/settings/immutable-releases/repositories/{repository_id} | Disable a selected repository for immutable releases in an organization |
| GET | /orgs/{org}/settings/network-configurations | List hosted compute network configurations for an organization |
| POST | /orgs/{org}/settings/network-configurations | Create a hosted compute network configuration for an organization |
| GET | /orgs/{org}/settings/network-configurations/{network_configuration_id} | Get a hosted compute network configuration for an organization |
| PATCH | /orgs/{org}/settings/network-configurations/{network_configuration_id} | Update a hosted compute network configuration for an organization |
| DELETE | /orgs/{org}/settings/network-configurations/{network_configuration_id} | Delete a hosted compute network configuration from an organization |
| GET | /orgs/{org}/settings/network-settings/{network_settings_id} | Get a hosted compute network settings resource for an organization |
| GET | /orgs/{org}/team/{team_slug}/copilot/metrics | Get Copilot metrics for a team |
| GET | /orgs/{org}/teams | List teams |
| POST | /orgs/{org}/teams | Create a team |
| GET | /orgs/{org}/teams/{team_slug} | Get a team by name |
| PATCH | /orgs/{org}/teams/{team_slug} | Update a team |
| DELETE | /orgs/{org}/teams/{team_slug} | Delete a team |
| GET | /orgs/{org}/teams/{team_slug}/invitations | List pending team invitations |
| GET | /orgs/{org}/teams/{team_slug}/members | List team members |
| GET | /orgs/{org}/teams/{team_slug}/memberships/{username} | Get team membership for a user |
| PUT | /orgs/{org}/teams/{team_slug}/memberships/{username} | Add or update team membership for a user |
| DELETE | /orgs/{org}/teams/{team_slug}/memberships/{username} | Remove team membership for a user |
| GET | /orgs/{org}/teams/{team_slug}/repos | List team repositories |
| GET | /orgs/{org}/teams/{team_slug}/repos/{owner}/{repo} | Check team permissions for a repository |
| PUT | /orgs/{org}/teams/{team_slug}/repos/{owner}/{repo} | Add or update team repository permissions |
| DELETE | /orgs/{org}/teams/{team_slug}/repos/{owner}/{repo} | Remove a repository from a team |
| GET | /orgs/{org}/teams/{team_slug}/teams | List child teams |
| POST | /orgs/{org}/{security_product}/{enablement} | Enable or disable a security feature for an organization |

### rate_limit
| Method | Path | Description |
|--------|------|-------------|
| GET | /rate_limit | Get rate limit status for the authenticated user |

### repos
| Method | Path | Description |
|--------|------|-------------|
| GET | /repos/{owner}/{repo} | Get a repository |
| PATCH | /repos/{owner}/{repo} | Update a repository |
| DELETE | /repos/{owner}/{repo} | Delete a repository |
| GET | /repos/{owner}/{repo}/actions/artifacts | List artifacts for a repository |
| GET | /repos/{owner}/{repo}/actions/artifacts/{artifact_id} | Get an artifact |
| DELETE | /repos/{owner}/{repo}/actions/artifacts/{artifact_id} | Delete an artifact |
| GET | /repos/{owner}/{repo}/actions/artifacts/{artifact_id}/{archive_format} | Download an artifact |
| GET | /repos/{owner}/{repo}/actions/cache/retention-limit | Get GitHub Actions cache retention limit for a repository |
| PUT | /repos/{owner}/{repo}/actions/cache/retention-limit | Set GitHub Actions cache retention limit for a repository |
| GET | /repos/{owner}/{repo}/actions/cache/storage-limit | Get GitHub Actions cache storage limit for a repository |
| PUT | /repos/{owner}/{repo}/actions/cache/storage-limit | Set GitHub Actions cache storage limit for a repository |
| GET | /repos/{owner}/{repo}/actions/cache/usage | Get GitHub Actions cache usage for a repository |
| GET | /repos/{owner}/{repo}/actions/caches | List GitHub Actions caches for a repository |
| DELETE | /repos/{owner}/{repo}/actions/caches | Delete GitHub Actions caches for a repository (using a cache key) |
| DELETE | /repos/{owner}/{repo}/actions/caches/{cache_id} | Delete a GitHub Actions cache for a repository (using a cache ID) |
| GET | /repos/{owner}/{repo}/actions/jobs/{job_id} | Get a job for a workflow run |
| GET | /repos/{owner}/{repo}/actions/jobs/{job_id}/logs | Download job logs for a workflow run |
| POST | /repos/{owner}/{repo}/actions/jobs/{job_id}/rerun | Re-run a job from a workflow run |
| GET | /repos/{owner}/{repo}/actions/oidc/customization/sub | Get the customization template for an OIDC subject claim for a repository |
| PUT | /repos/{owner}/{repo}/actions/oidc/customization/sub | Set the customization template for an OIDC subject claim for a repository |
| GET | /repos/{owner}/{repo}/actions/organization-secrets | List repository organization secrets |
| GET | /repos/{owner}/{repo}/actions/organization-variables | List repository organization variables |
| GET | /repos/{owner}/{repo}/actions/permissions | Get GitHub Actions permissions for a repository |
| PUT | /repos/{owner}/{repo}/actions/permissions | Set GitHub Actions permissions for a repository |
| GET | /repos/{owner}/{repo}/actions/permissions/access | Get the level of access for workflows outside of the repository |
| PUT | /repos/{owner}/{repo}/actions/permissions/access | Set the level of access for workflows outside of the repository |
| GET | /repos/{owner}/{repo}/actions/permissions/artifact-and-log-retention | Get artifact and log retention settings for a repository |
| PUT | /repos/{owner}/{repo}/actions/permissions/artifact-and-log-retention | Set artifact and log retention settings for a repository |
| GET | /repos/{owner}/{repo}/actions/permissions/fork-pr-contributor-approval | Get fork PR contributor approval permissions for a repository |
| PUT | /repos/{owner}/{repo}/actions/permissions/fork-pr-contributor-approval | Set fork PR contributor approval permissions for a repository |
| GET | /repos/{owner}/{repo}/actions/permissions/fork-pr-workflows-private-repos | Get private repo fork PR workflow settings for a repository |
| PUT | /repos/{owner}/{repo}/actions/permissions/fork-pr-workflows-private-repos | Set private repo fork PR workflow settings for a repository |
| GET | /repos/{owner}/{repo}/actions/permissions/selected-actions | Get allowed actions and reusable workflows for a repository |
| PUT | /repos/{owner}/{repo}/actions/permissions/selected-actions | Set allowed actions and reusable workflows for a repository |
| GET | /repos/{owner}/{repo}/actions/permissions/workflow | Get default workflow permissions for a repository |
| PUT | /repos/{owner}/{repo}/actions/permissions/workflow | Set default workflow permissions for a repository |
| GET | /repos/{owner}/{repo}/actions/runners | List self-hosted runners for a repository |
| GET | /repos/{owner}/{repo}/actions/runners/downloads | List runner applications for a repository |
| POST | /repos/{owner}/{repo}/actions/runners/generate-jitconfig | Create configuration for a just-in-time runner for a repository |
| POST | /repos/{owner}/{repo}/actions/runners/registration-token | Create a registration token for a repository |
| POST | /repos/{owner}/{repo}/actions/runners/remove-token | Create a remove token for a repository |
| GET | /repos/{owner}/{repo}/actions/runners/{runner_id} | Get a self-hosted runner for a repository |
| DELETE | /repos/{owner}/{repo}/actions/runners/{runner_id} | Delete a self-hosted runner from a repository |
| GET | /repos/{owner}/{repo}/actions/runners/{runner_id}/labels | List labels for a self-hosted runner for a repository |
| POST | /repos/{owner}/{repo}/actions/runners/{runner_id}/labels | Add custom labels to a self-hosted runner for a repository |
| PUT | /repos/{owner}/{repo}/actions/runners/{runner_id}/labels | Set custom labels for a self-hosted runner for a repository |
| DELETE | /repos/{owner}/{repo}/actions/runners/{runner_id}/labels | Remove all custom labels from a self-hosted runner for a repository |
| DELETE | /repos/{owner}/{repo}/actions/runners/{runner_id}/labels/{name} | Remove a custom label from a self-hosted runner for a repository |
| GET | /repos/{owner}/{repo}/actions/runs | List workflow runs for a repository |
| GET | /repos/{owner}/{repo}/actions/runs/{run_id} | Get a workflow run |
| DELETE | /repos/{owner}/{repo}/actions/runs/{run_id} | Delete a workflow run |
| GET | /repos/{owner}/{repo}/actions/runs/{run_id}/approvals | Get the review history for a workflow run |
| POST | /repos/{owner}/{repo}/actions/runs/{run_id}/approve | Approve a workflow run for a fork pull request |
| GET | /repos/{owner}/{repo}/actions/runs/{run_id}/artifacts | List workflow run artifacts |
| GET | /repos/{owner}/{repo}/actions/runs/{run_id}/attempts/{attempt_number} | Get a workflow run attempt |
| GET | /repos/{owner}/{repo}/actions/runs/{run_id}/attempts/{attempt_number}/jobs | List jobs for a workflow run attempt |
| GET | /repos/{owner}/{repo}/actions/runs/{run_id}/attempts/{attempt_number}/logs | Download workflow run attempt logs |
| POST | /repos/{owner}/{repo}/actions/runs/{run_id}/cancel | Cancel a workflow run |
| POST | /repos/{owner}/{repo}/actions/runs/{run_id}/deployment_protection_rule | Review custom deployment protection rules for a workflow run |
| POST | /repos/{owner}/{repo}/actions/runs/{run_id}/force-cancel | Force cancel a workflow run |
| GET | /repos/{owner}/{repo}/actions/runs/{run_id}/jobs | List jobs for a workflow run |
| GET | /repos/{owner}/{repo}/actions/runs/{run_id}/logs | Download workflow run logs |
| DELETE | /repos/{owner}/{repo}/actions/runs/{run_id}/logs | Delete workflow run logs |
| GET | /repos/{owner}/{repo}/actions/runs/{run_id}/pending_deployments | Get pending deployments for a workflow run |
| POST | /repos/{owner}/{repo}/actions/runs/{run_id}/pending_deployments | Review pending deployments for a workflow run |
| POST | /repos/{owner}/{repo}/actions/runs/{run_id}/rerun | Re-run a workflow |
| POST | /repos/{owner}/{repo}/actions/runs/{run_id}/rerun-failed-jobs | Re-run failed jobs from a workflow run |
| GET | /repos/{owner}/{repo}/actions/runs/{run_id}/timing | Get workflow run usage |
| GET | /repos/{owner}/{repo}/actions/secrets | List repository secrets |
| GET | /repos/{owner}/{repo}/actions/secrets/public-key | Get a repository public key |
| GET | /repos/{owner}/{repo}/actions/secrets/{secret_name} | Get a repository secret |
| PUT | /repos/{owner}/{repo}/actions/secrets/{secret_name} | Create or update a repository secret |
| DELETE | /repos/{owner}/{repo}/actions/secrets/{secret_name} | Delete a repository secret |
| GET | /repos/{owner}/{repo}/actions/variables | List repository variables |
| POST | /repos/{owner}/{repo}/actions/variables | Create a repository variable |
| GET | /repos/{owner}/{repo}/actions/variables/{name} | Get a repository variable |
| PATCH | /repos/{owner}/{repo}/actions/variables/{name} | Update a repository variable |
| DELETE | /repos/{owner}/{repo}/actions/variables/{name} | Delete a repository variable |
| GET | /repos/{owner}/{repo}/actions/workflows | List repository workflows |
| GET | /repos/{owner}/{repo}/actions/workflows/{workflow_id} | Get a workflow |
| PUT | /repos/{owner}/{repo}/actions/workflows/{workflow_id}/disable | Disable a workflow |
| POST | /repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches | Create a workflow dispatch event |
| PUT | /repos/{owner}/{repo}/actions/workflows/{workflow_id}/enable | Enable a workflow |
| GET | /repos/{owner}/{repo}/actions/workflows/{workflow_id}/runs | List workflow runs for a workflow |
| GET | /repos/{owner}/{repo}/actions/workflows/{workflow_id}/timing | Get workflow usage |
| GET | /repos/{owner}/{repo}/activity | List repository activities |
| GET | /repos/{owner}/{repo}/assignees | List assignees |
| GET | /repos/{owner}/{repo}/assignees/{assignee} | Check if a user can be assigned |
| POST | /repos/{owner}/{repo}/attestations | Create an attestation |
| GET | /repos/{owner}/{repo}/attestations/{subject_digest} | List attestations |
| GET | /repos/{owner}/{repo}/autolinks | Get all autolinks of a repository |
| POST | /repos/{owner}/{repo}/autolinks | Create an autolink reference for a repository |
| GET | /repos/{owner}/{repo}/autolinks/{autolink_id} | Get an autolink reference of a repository |
| DELETE | /repos/{owner}/{repo}/autolinks/{autolink_id} | Delete an autolink reference from a repository |
| GET | /repos/{owner}/{repo}/automated-security-fixes | Check if Dependabot security updates are enabled for a repository |
| PUT | /repos/{owner}/{repo}/automated-security-fixes | Enable Dependabot security updates |
| DELETE | /repos/{owner}/{repo}/automated-security-fixes | Disable Dependabot security updates |
| GET | /repos/{owner}/{repo}/branches | List branches |
| GET | /repos/{owner}/{repo}/branches/{branch} | Get a branch |
| GET | /repos/{owner}/{repo}/branches/{branch}/protection | Get branch protection |
| PUT | /repos/{owner}/{repo}/branches/{branch}/protection | Update branch protection |
| DELETE | /repos/{owner}/{repo}/branches/{branch}/protection | Delete branch protection |
| GET | /repos/{owner}/{repo}/branches/{branch}/protection/enforce_admins | Get admin branch protection |
| POST | /repos/{owner}/{repo}/branches/{branch}/protection/enforce_admins | Set admin branch protection |
| DELETE | /repos/{owner}/{repo}/branches/{branch}/protection/enforce_admins | Delete admin branch protection |
| GET | /repos/{owner}/{repo}/branches/{branch}/protection/required_pull_request_reviews | Get pull request review protection |
| PATCH | /repos/{owner}/{repo}/branches/{branch}/protection/required_pull_request_reviews | Update pull request review protection |
| DELETE | /repos/{owner}/{repo}/branches/{branch}/protection/required_pull_request_reviews | Delete pull request review protection |
| GET | /repos/{owner}/{repo}/branches/{branch}/protection/required_signatures | Get commit signature protection |
| POST | /repos/{owner}/{repo}/branches/{branch}/protection/required_signatures | Create commit signature protection |
| DELETE | /repos/{owner}/{repo}/branches/{branch}/protection/required_signatures | Delete commit signature protection |
| GET | /repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks | Get status checks protection |
| PATCH | /repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks | Update status check protection |
| DELETE | /repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks | Remove status check protection |
| GET | /repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks/contexts | Get all status check contexts |
| POST | /repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks/contexts | Add status check contexts |
| PUT | /repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks/contexts | Set status check contexts |
| DELETE | /repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks/contexts | Remove status check contexts |
| GET | /repos/{owner}/{repo}/branches/{branch}/protection/restrictions | Get access restrictions |
| DELETE | /repos/{owner}/{repo}/branches/{branch}/protection/restrictions | Delete access restrictions |
| GET | /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/apps | Get apps with access to the protected branch |
| POST | /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/apps | Add app access restrictions |
| PUT | /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/apps | Set app access restrictions |
| DELETE | /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/apps | Remove app access restrictions |
| GET | /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/teams | Get teams with access to the protected branch |
| POST | /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/teams | Add team access restrictions |
| PUT | /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/teams | Set team access restrictions |
| DELETE | /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/teams | Remove team access restrictions |
| GET | /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/users | Get users with access to the protected branch |
| POST | /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/users | Add user access restrictions |
| PUT | /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/users | Set user access restrictions |
| DELETE | /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/users | Remove user access restrictions |
| POST | /repos/{owner}/{repo}/branches/{branch}/rename | Rename a branch |
| POST | /repos/{owner}/{repo}/check-runs | Create a check run |
| GET | /repos/{owner}/{repo}/check-runs/{check_run_id} | Get a check run |
| PATCH | /repos/{owner}/{repo}/check-runs/{check_run_id} | Update a check run |
| GET | /repos/{owner}/{repo}/check-runs/{check_run_id}/annotations | List check run annotations |
| POST | /repos/{owner}/{repo}/check-runs/{check_run_id}/rerequest | Rerequest a check run |
| POST | /repos/{owner}/{repo}/check-suites | Create a check suite |
| PATCH | /repos/{owner}/{repo}/check-suites/preferences | Update repository preferences for check suites |
| GET | /repos/{owner}/{repo}/check-suites/{check_suite_id} | Get a check suite |
| GET | /repos/{owner}/{repo}/check-suites/{check_suite_id}/check-runs | List check runs in a check suite |
| POST | /repos/{owner}/{repo}/check-suites/{check_suite_id}/rerequest | Rerequest a check suite |
| GET | /repos/{owner}/{repo}/code-scanning/alerts | List code scanning alerts for a repository |
| GET | /repos/{owner}/{repo}/code-scanning/alerts/{alert_number} | Get a code scanning alert |
| PATCH | /repos/{owner}/{repo}/code-scanning/alerts/{alert_number} | Update a code scanning alert |
| GET | /repos/{owner}/{repo}/code-scanning/alerts/{alert_number}/autofix | Get the status of an autofix for a code scanning alert |
| POST | /repos/{owner}/{repo}/code-scanning/alerts/{alert_number}/autofix | Create an autofix for a code scanning alert |
| POST | /repos/{owner}/{repo}/code-scanning/alerts/{alert_number}/autofix/commits | Commit an autofix for a code scanning alert |
| GET | /repos/{owner}/{repo}/code-scanning/alerts/{alert_number}/instances | List instances of a code scanning alert |
| GET | /repos/{owner}/{repo}/code-scanning/analyses | List code scanning analyses for a repository |
| GET | /repos/{owner}/{repo}/code-scanning/analyses/{analysis_id} | Get a code scanning analysis for a repository |
| DELETE | /repos/{owner}/{repo}/code-scanning/analyses/{analysis_id} | Delete a code scanning analysis from a repository |
| GET | /repos/{owner}/{repo}/code-scanning/codeql/databases | List CodeQL databases for a repository |
| GET | /repos/{owner}/{repo}/code-scanning/codeql/databases/{language} | Get a CodeQL database for a repository |
| DELETE | /repos/{owner}/{repo}/code-scanning/codeql/databases/{language} | Delete a CodeQL database |
| POST | /repos/{owner}/{repo}/code-scanning/codeql/variant-analyses | Create a CodeQL variant analysis |
| GET | /repos/{owner}/{repo}/code-scanning/codeql/variant-analyses/{codeql_variant_analysis_id} | Get the summary of a CodeQL variant analysis |
| GET | /repos/{owner}/{repo}/code-scanning/codeql/variant-analyses/{codeql_variant_analysis_id}/repos/{repo_owner}/{repo_name} | Get the analysis status of a repository in a CodeQL variant analysis |
| GET | /repos/{owner}/{repo}/code-scanning/default-setup | Get a code scanning default setup configuration |
| PATCH | /repos/{owner}/{repo}/code-scanning/default-setup | Update a code scanning default setup configuration |
| POST | /repos/{owner}/{repo}/code-scanning/sarifs | Upload an analysis as SARIF data |
| GET | /repos/{owner}/{repo}/code-scanning/sarifs/{sarif_id} | Get information about a SARIF upload |
| GET | /repos/{owner}/{repo}/code-security-configuration | Get the code security configuration associated with a repository |
| GET | /repos/{owner}/{repo}/codeowners/errors | List CODEOWNERS errors |
| GET | /repos/{owner}/{repo}/codespaces | List codespaces in a repository for the authenticated user |
| POST | /repos/{owner}/{repo}/codespaces | Create a codespace in a repository |
| GET | /repos/{owner}/{repo}/codespaces/devcontainers | List devcontainer configurations in a repository for the authenticated user |
| GET | /repos/{owner}/{repo}/codespaces/machines | List available machine types for a repository |
| GET | /repos/{owner}/{repo}/codespaces/new | Get default attributes for a codespace |
| GET | /repos/{owner}/{repo}/codespaces/permissions_check | Check if permissions defined by a devcontainer have been accepted by the authenticated user |
| GET | /repos/{owner}/{repo}/codespaces/secrets | List repository secrets |
| GET | /repos/{owner}/{repo}/codespaces/secrets/public-key | Get a repository public key |
| GET | /repos/{owner}/{repo}/codespaces/secrets/{secret_name} | Get a repository secret |
| PUT | /repos/{owner}/{repo}/codespaces/secrets/{secret_name} | Create or update a repository secret |
| DELETE | /repos/{owner}/{repo}/codespaces/secrets/{secret_name} | Delete a repository secret |
| GET | /repos/{owner}/{repo}/collaborators | List repository collaborators |
| GET | /repos/{owner}/{repo}/collaborators/{username} | Check if a user is a repository collaborator |
| PUT | /repos/{owner}/{repo}/collaborators/{username} | Add a repository collaborator |
| DELETE | /repos/{owner}/{repo}/collaborators/{username} | Remove a repository collaborator |
| GET | /repos/{owner}/{repo}/collaborators/{username}/permission | Get repository permissions for a user |
| GET | /repos/{owner}/{repo}/comments | List commit comments for a repository |
| GET | /repos/{owner}/{repo}/comments/{comment_id} | Get a commit comment |
| PATCH | /repos/{owner}/{repo}/comments/{comment_id} | Update a commit comment |
| DELETE | /repos/{owner}/{repo}/comments/{comment_id} | Delete a commit comment |
| GET | /repos/{owner}/{repo}/comments/{comment_id}/reactions | List reactions for a commit comment |
| POST | /repos/{owner}/{repo}/comments/{comment_id}/reactions | Create reaction for a commit comment |
| DELETE | /repos/{owner}/{repo}/comments/{comment_id}/reactions/{reaction_id} | Delete a commit comment reaction |
| GET | /repos/{owner}/{repo}/commits | List commits |
| GET | /repos/{owner}/{repo}/commits/{commit_sha}/branches-where-head | List branches for HEAD commit |
| GET | /repos/{owner}/{repo}/commits/{commit_sha}/comments | List commit comments |
| POST | /repos/{owner}/{repo}/commits/{commit_sha}/comments | Create a commit comment |
| GET | /repos/{owner}/{repo}/commits/{commit_sha}/pulls | List pull requests associated with a commit |
| GET | /repos/{owner}/{repo}/commits/{ref} | Get a commit |
| GET | /repos/{owner}/{repo}/commits/{ref}/check-runs | List check runs for a Git reference |
| GET | /repos/{owner}/{repo}/commits/{ref}/check-suites | List check suites for a Git reference |
| GET | /repos/{owner}/{repo}/commits/{ref}/status | Get the combined status for a specific reference |
| GET | /repos/{owner}/{repo}/commits/{ref}/statuses | List commit statuses for a reference |
| GET | /repos/{owner}/{repo}/community/profile | Get community profile metrics |
| GET | /repos/{owner}/{repo}/compare/{basehead} | Compare two commits |
| GET | /repos/{owner}/{repo}/contents/{path} | Get repository content |
| PUT | /repos/{owner}/{repo}/contents/{path} | Create or update file contents |
| DELETE | /repos/{owner}/{repo}/contents/{path} | Delete a file |
| GET | /repos/{owner}/{repo}/contributors | List repository contributors |
| GET | /repos/{owner}/{repo}/dependabot/alerts | List Dependabot alerts for a repository |
| GET | /repos/{owner}/{repo}/dependabot/alerts/{alert_number} | Get a Dependabot alert |
| PATCH | /repos/{owner}/{repo}/dependabot/alerts/{alert_number} | Update a Dependabot alert |
| GET | /repos/{owner}/{repo}/dependabot/secrets | List repository secrets |
| GET | /repos/{owner}/{repo}/dependabot/secrets/public-key | Get a repository public key |
| GET | /repos/{owner}/{repo}/dependabot/secrets/{secret_name} | Get a repository secret |
| PUT | /repos/{owner}/{repo}/dependabot/secrets/{secret_name} | Create or update a repository secret |
| DELETE | /repos/{owner}/{repo}/dependabot/secrets/{secret_name} | Delete a repository secret |
| GET | /repos/{owner}/{repo}/dependency-graph/compare/{basehead} | Get a diff of the dependencies between commits |
| GET | /repos/{owner}/{repo}/dependency-graph/sbom | Export a software bill of materials (SBOM) for a repository. |
| POST | /repos/{owner}/{repo}/dependency-graph/snapshots | Create a snapshot of dependencies for a repository |
| GET | /repos/{owner}/{repo}/deployments | List deployments |
| POST | /repos/{owner}/{repo}/deployments | Create a deployment |
| GET | /repos/{owner}/{repo}/deployments/{deployment_id} | Get a deployment |
| DELETE | /repos/{owner}/{repo}/deployments/{deployment_id} | Delete a deployment |
| GET | /repos/{owner}/{repo}/deployments/{deployment_id}/statuses | List deployment statuses |
| POST | /repos/{owner}/{repo}/deployments/{deployment_id}/statuses | Create a deployment status |
| GET | /repos/{owner}/{repo}/deployments/{deployment_id}/statuses/{status_id} | Get a deployment status |
| POST | /repos/{owner}/{repo}/dispatches | Create a repository dispatch event |
| GET | /repos/{owner}/{repo}/environments | List environments |
| GET | /repos/{owner}/{repo}/environments/{environment_name} | Get an environment |
| PUT | /repos/{owner}/{repo}/environments/{environment_name} | Create or update an environment |
| DELETE | /repos/{owner}/{repo}/environments/{environment_name} | Delete an environment |
| GET | /repos/{owner}/{repo}/environments/{environment_name}/deployment-branch-policies | List deployment branch policies |
| POST | /repos/{owner}/{repo}/environments/{environment_name}/deployment-branch-policies | Create a deployment branch policy |
| GET | /repos/{owner}/{repo}/environments/{environment_name}/deployment-branch-policies/{branch_policy_id} | Get a deployment branch policy |
| PUT | /repos/{owner}/{repo}/environments/{environment_name}/deployment-branch-policies/{branch_policy_id} | Update a deployment branch policy |
| DELETE | /repos/{owner}/{repo}/environments/{environment_name}/deployment-branch-policies/{branch_policy_id} | Delete a deployment branch policy |
| GET | /repos/{owner}/{repo}/environments/{environment_name}/deployment_protection_rules | Get all deployment protection rules for an environment |
| POST | /repos/{owner}/{repo}/environments/{environment_name}/deployment_protection_rules | Create a custom deployment protection rule on an environment |
| GET | /repos/{owner}/{repo}/environments/{environment_name}/deployment_protection_rules/apps | List custom deployment rule integrations available for an environment |
| GET | /repos/{owner}/{repo}/environments/{environment_name}/deployment_protection_rules/{protection_rule_id} | Get a custom deployment protection rule |
| DELETE | /repos/{owner}/{repo}/environments/{environment_name}/deployment_protection_rules/{protection_rule_id} | Disable a custom protection rule for an environment |
| GET | /repos/{owner}/{repo}/environments/{environment_name}/secrets | List environment secrets |
| GET | /repos/{owner}/{repo}/environments/{environment_name}/secrets/public-key | Get an environment public key |
| GET | /repos/{owner}/{repo}/environments/{environment_name}/secrets/{secret_name} | Get an environment secret |
| PUT | /repos/{owner}/{repo}/environments/{environment_name}/secrets/{secret_name} | Create or update an environment secret |
| DELETE | /repos/{owner}/{repo}/environments/{environment_name}/secrets/{secret_name} | Delete an environment secret |
| GET | /repos/{owner}/{repo}/environments/{environment_name}/variables | List environment variables |
| POST | /repos/{owner}/{repo}/environments/{environment_name}/variables | Create an environment variable |
| GET | /repos/{owner}/{repo}/environments/{environment_name}/variables/{name} | Get an environment variable |
| PATCH | /repos/{owner}/{repo}/environments/{environment_name}/variables/{name} | Update an environment variable |
| DELETE | /repos/{owner}/{repo}/environments/{environment_name}/variables/{name} | Delete an environment variable |
| GET | /repos/{owner}/{repo}/events | List repository events |
| GET | /repos/{owner}/{repo}/forks | List forks |
| POST | /repos/{owner}/{repo}/forks | Create a fork |
| POST | /repos/{owner}/{repo}/git/blobs | Create a blob |
| GET | /repos/{owner}/{repo}/git/blobs/{file_sha} | Get a blob |
| POST | /repos/{owner}/{repo}/git/commits | Create a commit |
| GET | /repos/{owner}/{repo}/git/commits/{commit_sha} | Get a commit object |
| GET | /repos/{owner}/{repo}/git/matching-refs/{ref} | List matching references |
| GET | /repos/{owner}/{repo}/git/ref/{ref} | Get a reference |
| POST | /repos/{owner}/{repo}/git/refs | Create a reference |
| PATCH | /repos/{owner}/{repo}/git/refs/{ref} | Update a reference |
| DELETE | /repos/{owner}/{repo}/git/refs/{ref} | Delete a reference |
| POST | /repos/{owner}/{repo}/git/tags | Create a tag object |
| GET | /repos/{owner}/{repo}/git/tags/{tag_sha} | Get a tag |
| POST | /repos/{owner}/{repo}/git/trees | Create a tree |
| GET | /repos/{owner}/{repo}/git/trees/{tree_sha} | Get a tree |
| GET | /repos/{owner}/{repo}/hooks | List repository webhooks |
| POST | /repos/{owner}/{repo}/hooks | Create a repository webhook |
| GET | /repos/{owner}/{repo}/hooks/{hook_id} | Get a repository webhook |
| PATCH | /repos/{owner}/{repo}/hooks/{hook_id} | Update a repository webhook |
| DELETE | /repos/{owner}/{repo}/hooks/{hook_id} | Delete a repository webhook |
| GET | /repos/{owner}/{repo}/hooks/{hook_id}/config | Get a webhook configuration for a repository |
| PATCH | /repos/{owner}/{repo}/hooks/{hook_id}/config | Update a webhook configuration for a repository |
| GET | /repos/{owner}/{repo}/hooks/{hook_id}/deliveries | List deliveries for a repository webhook |
| GET | /repos/{owner}/{repo}/hooks/{hook_id}/deliveries/{delivery_id} | Get a delivery for a repository webhook |
| POST | /repos/{owner}/{repo}/hooks/{hook_id}/deliveries/{delivery_id}/attempts | Redeliver a delivery for a repository webhook |
| POST | /repos/{owner}/{repo}/hooks/{hook_id}/pings | Ping a repository webhook |
| POST | /repos/{owner}/{repo}/hooks/{hook_id}/tests | Test the push repository webhook |
| GET | /repos/{owner}/{repo}/immutable-releases | Check if immutable releases are enabled for a repository |
| PUT | /repos/{owner}/{repo}/immutable-releases | Enable immutable releases |
| DELETE | /repos/{owner}/{repo}/immutable-releases | Disable immutable releases |
| GET | /repos/{owner}/{repo}/import | Get an import status |
| PUT | /repos/{owner}/{repo}/import | Start an import |
| PATCH | /repos/{owner}/{repo}/import | Update an import |
| DELETE | /repos/{owner}/{repo}/import | Cancel an import |
| GET | /repos/{owner}/{repo}/import/authors | Get commit authors |
| PATCH | /repos/{owner}/{repo}/import/authors/{author_id} | Map a commit author |
| GET | /repos/{owner}/{repo}/import/large_files | Get large files |
| PATCH | /repos/{owner}/{repo}/import/lfs | Update Git LFS preference |
| GET | /repos/{owner}/{repo}/installation | Get a repository installation for the authenticated app |
| GET | /repos/{owner}/{repo}/interaction-limits | Get interaction restrictions for a repository |
| PUT | /repos/{owner}/{repo}/interaction-limits | Set interaction restrictions for a repository |
| DELETE | /repos/{owner}/{repo}/interaction-limits | Remove interaction restrictions for a repository |
| GET | /repos/{owner}/{repo}/invitations | List repository invitations |
| PATCH | /repos/{owner}/{repo}/invitations/{invitation_id} | Update a repository invitation |
| DELETE | /repos/{owner}/{repo}/invitations/{invitation_id} | Delete a repository invitation |
| GET | /repos/{owner}/{repo}/issues | List repository issues |
| POST | /repos/{owner}/{repo}/issues | Create an issue |
| GET | /repos/{owner}/{repo}/issues/comments | List issue comments for a repository |
| GET | /repos/{owner}/{repo}/issues/comments/{comment_id} | Get an issue comment |
| PATCH | /repos/{owner}/{repo}/issues/comments/{comment_id} | Update an issue comment |
| DELETE | /repos/{owner}/{repo}/issues/comments/{comment_id} | Delete an issue comment |
| PUT | /repos/{owner}/{repo}/issues/comments/{comment_id}/pin | Pin an issue comment |
| DELETE | /repos/{owner}/{repo}/issues/comments/{comment_id}/pin | Unpin an issue comment |
| GET | /repos/{owner}/{repo}/issues/comments/{comment_id}/reactions | List reactions for an issue comment |
| POST | /repos/{owner}/{repo}/issues/comments/{comment_id}/reactions | Create reaction for an issue comment |
| DELETE | /repos/{owner}/{repo}/issues/comments/{comment_id}/reactions/{reaction_id} | Delete an issue comment reaction |
| GET | /repos/{owner}/{repo}/issues/events | List issue events for a repository |
| GET | /repos/{owner}/{repo}/issues/events/{event_id} | Get an issue event |
| GET | /repos/{owner}/{repo}/issues/{issue_number} | Get an issue |
| PATCH | /repos/{owner}/{repo}/issues/{issue_number} | Update an issue |
| POST | /repos/{owner}/{repo}/issues/{issue_number}/assignees | Add assignees to an issue |
| DELETE | /repos/{owner}/{repo}/issues/{issue_number}/assignees | Remove assignees from an issue |
| GET | /repos/{owner}/{repo}/issues/{issue_number}/assignees/{assignee} | Check if a user can be assigned to a issue |
| GET | /repos/{owner}/{repo}/issues/{issue_number}/comments | List issue comments |
| POST | /repos/{owner}/{repo}/issues/{issue_number}/comments | Create an issue comment |
| GET | /repos/{owner}/{repo}/issues/{issue_number}/dependencies/blocked_by | List dependencies an issue is blocked by |
| POST | /repos/{owner}/{repo}/issues/{issue_number}/dependencies/blocked_by | Add a dependency an issue is blocked by |
| DELETE | /repos/{owner}/{repo}/issues/{issue_number}/dependencies/blocked_by/{issue_id} | Remove dependency an issue is blocked by |
| GET | /repos/{owner}/{repo}/issues/{issue_number}/dependencies/blocking | List dependencies an issue is blocking |
| GET | /repos/{owner}/{repo}/issues/{issue_number}/events | List issue events |
| GET | /repos/{owner}/{repo}/issues/{issue_number}/labels | List labels for an issue |
| POST | /repos/{owner}/{repo}/issues/{issue_number}/labels | Add labels to an issue |
| PUT | /repos/{owner}/{repo}/issues/{issue_number}/labels | Set labels for an issue |
| DELETE | /repos/{owner}/{repo}/issues/{issue_number}/labels | Remove all labels from an issue |
| DELETE | /repos/{owner}/{repo}/issues/{issue_number}/labels/{name} | Remove a label from an issue |
| PUT | /repos/{owner}/{repo}/issues/{issue_number}/lock | Lock an issue |
| DELETE | /repos/{owner}/{repo}/issues/{issue_number}/lock | Unlock an issue |
| GET | /repos/{owner}/{repo}/issues/{issue_number}/parent | Get parent issue |
| GET | /repos/{owner}/{repo}/issues/{issue_number}/reactions | List reactions for an issue |
| POST | /repos/{owner}/{repo}/issues/{issue_number}/reactions | Create reaction for an issue |
| DELETE | /repos/{owner}/{repo}/issues/{issue_number}/reactions/{reaction_id} | Delete an issue reaction |
| DELETE | /repos/{owner}/{repo}/issues/{issue_number}/sub_issue | Remove sub-issue |
| GET | /repos/{owner}/{repo}/issues/{issue_number}/sub_issues | List sub-issues |
| POST | /repos/{owner}/{repo}/issues/{issue_number}/sub_issues | Add sub-issue |
| PATCH | /repos/{owner}/{repo}/issues/{issue_number}/sub_issues/priority | Reprioritize sub-issue |
| GET | /repos/{owner}/{repo}/issues/{issue_number}/timeline | List timeline events for an issue |
| GET | /repos/{owner}/{repo}/keys | List deploy keys |
| POST | /repos/{owner}/{repo}/keys | Create a deploy key |
| GET | /repos/{owner}/{repo}/keys/{key_id} | Get a deploy key |
| DELETE | /repos/{owner}/{repo}/keys/{key_id} | Delete a deploy key |
| GET | /repos/{owner}/{repo}/labels | List labels for a repository |
| POST | /repos/{owner}/{repo}/labels | Create a label |
| GET | /repos/{owner}/{repo}/labels/{name} | Get a label |
| PATCH | /repos/{owner}/{repo}/labels/{name} | Update a label |
| DELETE | /repos/{owner}/{repo}/labels/{name} | Delete a label |
| GET | /repos/{owner}/{repo}/languages | List repository languages |
| GET | /repos/{owner}/{repo}/license | Get the license for a repository |
| POST | /repos/{owner}/{repo}/merge-upstream | Sync a fork branch with the upstream repository |
| POST | /repos/{owner}/{repo}/merges | Merge a branch |
| GET | /repos/{owner}/{repo}/milestones | List milestones |
| POST | /repos/{owner}/{repo}/milestones | Create a milestone |
| GET | /repos/{owner}/{repo}/milestones/{milestone_number} | Get a milestone |
| PATCH | /repos/{owner}/{repo}/milestones/{milestone_number} | Update a milestone |
| DELETE | /repos/{owner}/{repo}/milestones/{milestone_number} | Delete a milestone |
| GET | /repos/{owner}/{repo}/milestones/{milestone_number}/labels | List labels for issues in a milestone |
| GET | /repos/{owner}/{repo}/notifications | List repository notifications for the authenticated user |
| PUT | /repos/{owner}/{repo}/notifications | Mark repository notifications as read |
| GET | /repos/{owner}/{repo}/pages | Get a GitHub Pages site |
| POST | /repos/{owner}/{repo}/pages | Create a GitHub Pages site |
| PUT | /repos/{owner}/{repo}/pages | Update information about a GitHub Pages site |
| DELETE | /repos/{owner}/{repo}/pages | Delete a GitHub Pages site |
| GET | /repos/{owner}/{repo}/pages/builds | List GitHub Pages builds |
| POST | /repos/{owner}/{repo}/pages/builds | Request a GitHub Pages build |
| GET | /repos/{owner}/{repo}/pages/builds/latest | Get latest Pages build |
| GET | /repos/{owner}/{repo}/pages/builds/{build_id} | Get GitHub Pages build |
| POST | /repos/{owner}/{repo}/pages/deployments | Create a GitHub Pages deployment |
| GET | /repos/{owner}/{repo}/pages/deployments/{pages_deployment_id} | Get the status of a GitHub Pages deployment |
| POST | /repos/{owner}/{repo}/pages/deployments/{pages_deployment_id}/cancel | Cancel a GitHub Pages deployment |
| GET | /repos/{owner}/{repo}/pages/health | Get a DNS health check for GitHub Pages |
| GET | /repos/{owner}/{repo}/private-vulnerability-reporting | Check if private vulnerability reporting is enabled for a repository |
| PUT | /repos/{owner}/{repo}/private-vulnerability-reporting | Enable private vulnerability reporting for a repository |
| DELETE | /repos/{owner}/{repo}/private-vulnerability-reporting | Disable private vulnerability reporting for a repository |
| GET | /repos/{owner}/{repo}/properties/values | Get all custom property values for a repository |
| PATCH | /repos/{owner}/{repo}/properties/values | Create or update custom property values for a repository |
| GET | /repos/{owner}/{repo}/pulls | List pull requests |
| POST | /repos/{owner}/{repo}/pulls | Create a pull request |
| GET | /repos/{owner}/{repo}/pulls/comments | List review comments in a repository |
| GET | /repos/{owner}/{repo}/pulls/comments/{comment_id} | Get a review comment for a pull request |
| PATCH | /repos/{owner}/{repo}/pulls/comments/{comment_id} | Update a review comment for a pull request |
| DELETE | /repos/{owner}/{repo}/pulls/comments/{comment_id} | Delete a review comment for a pull request |
| GET | /repos/{owner}/{repo}/pulls/comments/{comment_id}/reactions | List reactions for a pull request review comment |
| POST | /repos/{owner}/{repo}/pulls/comments/{comment_id}/reactions | Create reaction for a pull request review comment |
| DELETE | /repos/{owner}/{repo}/pulls/comments/{comment_id}/reactions/{reaction_id} | Delete a pull request comment reaction |
| GET | /repos/{owner}/{repo}/pulls/{pull_number} | Get a pull request |
| PATCH | /repos/{owner}/{repo}/pulls/{pull_number} | Update a pull request |
| POST | /repos/{owner}/{repo}/pulls/{pull_number}/codespaces | Create a codespace from a pull request |
| GET | /repos/{owner}/{repo}/pulls/{pull_number}/comments | List review comments on a pull request |
| POST | /repos/{owner}/{repo}/pulls/{pull_number}/comments | Create a review comment for a pull request |
| POST | /repos/{owner}/{repo}/pulls/{pull_number}/comments/{comment_id}/replies | Create a reply for a review comment |
| GET | /repos/{owner}/{repo}/pulls/{pull_number}/commits | List commits on a pull request |
| GET | /repos/{owner}/{repo}/pulls/{pull_number}/files | List pull requests files |
| GET | /repos/{owner}/{repo}/pulls/{pull_number}/merge | Check if a pull request has been merged |
| PUT | /repos/{owner}/{repo}/pulls/{pull_number}/merge | Merge a pull request |
| GET | /repos/{owner}/{repo}/pulls/{pull_number}/requested_reviewers | Get all requested reviewers for a pull request |
| POST | /repos/{owner}/{repo}/pulls/{pull_number}/requested_reviewers | Request reviewers for a pull request |
| DELETE | /repos/{owner}/{repo}/pulls/{pull_number}/requested_reviewers | Remove requested reviewers from a pull request |
| GET | /repos/{owner}/{repo}/pulls/{pull_number}/reviews | List reviews for a pull request |
| POST | /repos/{owner}/{repo}/pulls/{pull_number}/reviews | Create a review for a pull request |
| GET | /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} | Get a review for a pull request |
| PUT | /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} | Update a review for a pull request |
| DELETE | /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} | Delete a pending review for a pull request |
| GET | /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}/comments | List comments for a pull request review |
| PUT | /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}/dismissals | Dismiss a review for a pull request |
| POST | /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}/events | Submit a review for a pull request |
| PUT | /repos/{owner}/{repo}/pulls/{pull_number}/update-branch | Update a pull request branch |
| GET | /repos/{owner}/{repo}/readme | Get a repository README |
| GET | /repos/{owner}/{repo}/readme/{dir} | Get a repository README for a directory |
| GET | /repos/{owner}/{repo}/releases | List releases |
| POST | /repos/{owner}/{repo}/releases | Create a release |
| GET | /repos/{owner}/{repo}/releases/assets/{asset_id} | Get a release asset |
| PATCH | /repos/{owner}/{repo}/releases/assets/{asset_id} | Update a release asset |
| DELETE | /repos/{owner}/{repo}/releases/assets/{asset_id} | Delete a release asset |
| POST | /repos/{owner}/{repo}/releases/generate-notes | Generate release notes content for a release |
| GET | /repos/{owner}/{repo}/releases/latest | Get the latest release |
| GET | /repos/{owner}/{repo}/releases/tags/{tag} | Get a release by tag name |
| GET | /repos/{owner}/{repo}/releases/{release_id} | Get a release |
| PATCH | /repos/{owner}/{repo}/releases/{release_id} | Update a release |
| DELETE | /repos/{owner}/{repo}/releases/{release_id} | Delete a release |
| GET | /repos/{owner}/{repo}/releases/{release_id}/assets | List release assets |
| POST | /repos/{owner}/{repo}/releases/{release_id}/assets | Upload a release asset |
| GET | /repos/{owner}/{repo}/releases/{release_id}/reactions | List reactions for a release |
| POST | /repos/{owner}/{repo}/releases/{release_id}/reactions | Create reaction for a release |
| DELETE | /repos/{owner}/{repo}/releases/{release_id}/reactions/{reaction_id} | Delete a release reaction |
| GET | /repos/{owner}/{repo}/rules/branches/{branch} | Get rules for a branch |
| GET | /repos/{owner}/{repo}/rulesets | Get all repository rulesets |
| POST | /repos/{owner}/{repo}/rulesets | Create a repository ruleset |
| GET | /repos/{owner}/{repo}/rulesets/rule-suites | List repository rule suites |
| GET | /repos/{owner}/{repo}/rulesets/rule-suites/{rule_suite_id} | Get a repository rule suite |
| GET | /repos/{owner}/{repo}/rulesets/{ruleset_id} | Get a repository ruleset |
| PUT | /repos/{owner}/{repo}/rulesets/{ruleset_id} | Update a repository ruleset |
| DELETE | /repos/{owner}/{repo}/rulesets/{ruleset_id} | Delete a repository ruleset |
| GET | /repos/{owner}/{repo}/rulesets/{ruleset_id}/history | Get repository ruleset history |
| GET | /repos/{owner}/{repo}/rulesets/{ruleset_id}/history/{version_id} | Get repository ruleset version |
| GET | /repos/{owner}/{repo}/secret-scanning/alerts | List secret scanning alerts for a repository |
| GET | /repos/{owner}/{repo}/secret-scanning/alerts/{alert_number} | Get a secret scanning alert |
| PATCH | /repos/{owner}/{repo}/secret-scanning/alerts/{alert_number} | Update a secret scanning alert |
| GET | /repos/{owner}/{repo}/secret-scanning/alerts/{alert_number}/locations | List locations for a secret scanning alert |
| POST | /repos/{owner}/{repo}/secret-scanning/push-protection-bypasses | Create a push protection bypass |
| GET | /repos/{owner}/{repo}/secret-scanning/scan-history | Get secret scanning scan history for a repository |
| GET | /repos/{owner}/{repo}/security-advisories | List repository security advisories |
| POST | /repos/{owner}/{repo}/security-advisories | Create a repository security advisory |
| POST | /repos/{owner}/{repo}/security-advisories/reports | Privately report a security vulnerability |
| GET | /repos/{owner}/{repo}/security-advisories/{ghsa_id} | Get a repository security advisory |
| PATCH | /repos/{owner}/{repo}/security-advisories/{ghsa_id} | Update a repository security advisory |
| POST | /repos/{owner}/{repo}/security-advisories/{ghsa_id}/cve | Request a CVE for a repository security advisory |
| POST | /repos/{owner}/{repo}/security-advisories/{ghsa_id}/forks | Create a temporary private fork |
| GET | /repos/{owner}/{repo}/stargazers | List stargazers |
| GET | /repos/{owner}/{repo}/stats/code_frequency | Get the weekly commit activity |
| GET | /repos/{owner}/{repo}/stats/commit_activity | Get the last year of commit activity |
| GET | /repos/{owner}/{repo}/stats/contributors | Get all contributor commit activity |
| GET | /repos/{owner}/{repo}/stats/participation | Get the weekly commit count |
| GET | /repos/{owner}/{repo}/stats/punch_card | Get the hourly commit count for each day |
| POST | /repos/{owner}/{repo}/statuses/{sha} | Create a commit status |
| GET | /repos/{owner}/{repo}/subscribers | List watchers |
| GET | /repos/{owner}/{repo}/subscription | Get a repository subscription |
| PUT | /repos/{owner}/{repo}/subscription | Set a repository subscription |
| DELETE | /repos/{owner}/{repo}/subscription | Delete a repository subscription |
| GET | /repos/{owner}/{repo}/tags | List repository tags |
| GET | /repos/{owner}/{repo}/tarball/{ref} | Download a repository archive (tar) |
| GET | /repos/{owner}/{repo}/teams | List repository teams |
| GET | /repos/{owner}/{repo}/topics | Get all repository topics |
| PUT | /repos/{owner}/{repo}/topics | Replace all repository topics |
| GET | /repos/{owner}/{repo}/traffic/clones | Get repository clones |
| GET | /repos/{owner}/{repo}/traffic/popular/paths | Get top referral paths |
| GET | /repos/{owner}/{repo}/traffic/popular/referrers | Get top referral sources |
| GET | /repos/{owner}/{repo}/traffic/views | Get page views |
| POST | /repos/{owner}/{repo}/transfer | Transfer a repository |
| GET | /repos/{owner}/{repo}/vulnerability-alerts | Check if vulnerability alerts are enabled for a repository |
| PUT | /repos/{owner}/{repo}/vulnerability-alerts | Enable vulnerability alerts |
| DELETE | /repos/{owner}/{repo}/vulnerability-alerts | Disable vulnerability alerts |
| GET | /repos/{owner}/{repo}/zipball/{ref} | Download a repository archive (zip) |
| POST | /repos/{template_owner}/{template_repo}/generate | Create a repository using a template |

### repositories
| Method | Path | Description |
|--------|------|-------------|
| GET | /repositories | List public repositories |

### search
| Method | Path | Description |
|--------|------|-------------|
| GET | /search/code | Search code |
| GET | /search/commits | Search commits |
| GET | /search/issues | Search issues and pull requests |
| GET | /search/labels | Search labels |
| GET | /search/repositories | Search repositories |
| GET | /search/topics | Search topics |
| GET | /search/users | Search users |

### teams
| Method | Path | Description |
|--------|------|-------------|
| GET | /teams/{team_id} | Get a team (Legacy) |
| PATCH | /teams/{team_id} | Update a team (Legacy) |
| DELETE | /teams/{team_id} | Delete a team (Legacy) |
| GET | /teams/{team_id}/invitations | List pending team invitations (Legacy) |
| GET | /teams/{team_id}/members | List team members (Legacy) |
| GET | /teams/{team_id}/members/{username} | Get team member (Legacy) |
| PUT | /teams/{team_id}/members/{username} | Add team member (Legacy) |
| DELETE | /teams/{team_id}/members/{username} | Remove team member (Legacy) |
| GET | /teams/{team_id}/memberships/{username} | Get team membership for a user (Legacy) |
| PUT | /teams/{team_id}/memberships/{username} | Add or update team membership for a user (Legacy) |
| DELETE | /teams/{team_id}/memberships/{username} | Remove team membership for a user (Legacy) |
| GET | /teams/{team_id}/repos | List team repositories (Legacy) |
| GET | /teams/{team_id}/repos/{owner}/{repo} | Check team permissions for a repository (Legacy) |
| PUT | /teams/{team_id}/repos/{owner}/{repo} | Add or update team repository permissions (Legacy) |
| DELETE | /teams/{team_id}/repos/{owner}/{repo} | Remove a repository from a team (Legacy) |
| GET | /teams/{team_id}/teams | List child teams (Legacy) |

### user
| Method | Path | Description |
|--------|------|-------------|
| GET | /user | Get the authenticated user |
| PATCH | /user | Update the authenticated user |
| GET | /user/blocks | List users blocked by the authenticated user |
| GET | /user/blocks/{username} | Check if a user is blocked by the authenticated user |
| PUT | /user/blocks/{username} | Block a user |
| DELETE | /user/blocks/{username} | Unblock a user |
| GET | /user/codespaces | List codespaces for the authenticated user |
| POST | /user/codespaces | Create a codespace for the authenticated user |
| GET | /user/codespaces/secrets | List secrets for the authenticated user |
| GET | /user/codespaces/secrets/public-key | Get public key for the authenticated user |
| GET | /user/codespaces/secrets/{secret_name} | Get a secret for the authenticated user |
| PUT | /user/codespaces/secrets/{secret_name} | Create or update a secret for the authenticated user |
| DELETE | /user/codespaces/secrets/{secret_name} | Delete a secret for the authenticated user |
| GET | /user/codespaces/secrets/{secret_name}/repositories | List selected repositories for a user secret |
| PUT | /user/codespaces/secrets/{secret_name}/repositories | Set selected repositories for a user secret |
| PUT | /user/codespaces/secrets/{secret_name}/repositories/{repository_id} | Add a selected repository to a user secret |
| DELETE | /user/codespaces/secrets/{secret_name}/repositories/{repository_id} | Remove a selected repository from a user secret |
| GET | /user/codespaces/{codespace_name} | Get a codespace for the authenticated user |
| PATCH | /user/codespaces/{codespace_name} | Update a codespace for the authenticated user |
| DELETE | /user/codespaces/{codespace_name} | Delete a codespace for the authenticated user |
| POST | /user/codespaces/{codespace_name}/exports | Export a codespace for the authenticated user |
| GET | /user/codespaces/{codespace_name}/exports/{export_id} | Get details about a codespace export |
| GET | /user/codespaces/{codespace_name}/machines | List machine types for a codespace |
| POST | /user/codespaces/{codespace_name}/publish | Create a repository from an unpublished codespace |
| POST | /user/codespaces/{codespace_name}/start | Start a codespace for the authenticated user |
| POST | /user/codespaces/{codespace_name}/stop | Stop a codespace for the authenticated user |
| GET | /user/docker/conflicts | Get list of conflicting packages during Docker migration for authenticated-user |
| PATCH | /user/email/visibility | Set primary email visibility for the authenticated user |
| GET | /user/emails | List email addresses for the authenticated user |
| POST | /user/emails | Add an email address for the authenticated user |
| DELETE | /user/emails | Delete an email address for the authenticated user |
| GET | /user/followers | List followers of the authenticated user |
| GET | /user/following | List the people the authenticated user follows |
| GET | /user/following/{username} | Check if a person is followed by the authenticated user |
| PUT | /user/following/{username} | Follow a user |
| DELETE | /user/following/{username} | Unfollow a user |
| GET | /user/gpg_keys | List GPG keys for the authenticated user |
| POST | /user/gpg_keys | Create a GPG key for the authenticated user |
| GET | /user/gpg_keys/{gpg_key_id} | Get a GPG key for the authenticated user |
| DELETE | /user/gpg_keys/{gpg_key_id} | Delete a GPG key for the authenticated user |
| GET | /user/installations | List app installations accessible to the user access token |
| GET | /user/installations/{installation_id}/repositories | List repositories accessible to the user access token |
| PUT | /user/installations/{installation_id}/repositories/{repository_id} | Add a repository to an app installation |
| DELETE | /user/installations/{installation_id}/repositories/{repository_id} | Remove a repository from an app installation |
| GET | /user/interaction-limits | Get interaction restrictions for your public repositories |
| PUT | /user/interaction-limits | Set interaction restrictions for your public repositories |
| DELETE | /user/interaction-limits | Remove interaction restrictions from your public repositories |
| GET | /user/issues | List user account issues assigned to the authenticated user |
| GET | /user/keys | List public SSH keys for the authenticated user |
| POST | /user/keys | Create a public SSH key for the authenticated user |
| GET | /user/keys/{key_id} | Get a public SSH key for the authenticated user |
| DELETE | /user/keys/{key_id} | Delete a public SSH key for the authenticated user |
| GET | /user/marketplace_purchases | List subscriptions for the authenticated user |
| GET | /user/marketplace_purchases/stubbed | List subscriptions for the authenticated user (stubbed) |
| GET | /user/memberships/orgs | List organization memberships for the authenticated user |
| GET | /user/memberships/orgs/{org} | Get an organization membership for the authenticated user |
| PATCH | /user/memberships/orgs/{org} | Update an organization membership for the authenticated user |
| GET | /user/migrations | List user migrations |
| POST | /user/migrations | Start a user migration |
| GET | /user/migrations/{migration_id} | Get a user migration status |
| GET | /user/migrations/{migration_id}/archive | Download a user migration archive |
| DELETE | /user/migrations/{migration_id}/archive | Delete a user migration archive |
| DELETE | /user/migrations/{migration_id}/repos/{repo_name}/lock | Unlock a user repository |
| GET | /user/migrations/{migration_id}/repositories | List repositories for a user migration |
| GET | /user/orgs | List organizations for the authenticated user |
| GET | /user/packages | List packages for the authenticated user's namespace |
| GET | /user/packages/{package_type}/{package_name} | Get a package for the authenticated user |
| DELETE | /user/packages/{package_type}/{package_name} | Delete a package for the authenticated user |
| POST | /user/packages/{package_type}/{package_name}/restore | Restore a package for the authenticated user |
| GET | /user/packages/{package_type}/{package_name}/versions | List package versions for a package owned by the authenticated user |
| GET | /user/packages/{package_type}/{package_name}/versions/{package_version_id} | Get a package version for the authenticated user |
| DELETE | /user/packages/{package_type}/{package_name}/versions/{package_version_id} | Delete a package version for the authenticated user |
| POST | /user/packages/{package_type}/{package_name}/versions/{package_version_id}/restore | Restore a package version for the authenticated user |
| GET | /user/public_emails | List public email addresses for the authenticated user |
| GET | /user/repos | List repositories for the authenticated user |
| POST | /user/repos | Create a repository for the authenticated user |
| GET | /user/repository_invitations | List repository invitations for the authenticated user |
| PATCH | /user/repository_invitations/{invitation_id} | Accept a repository invitation |
| DELETE | /user/repository_invitations/{invitation_id} | Decline a repository invitation |
| GET | /user/social_accounts | List social accounts for the authenticated user |
| POST | /user/social_accounts | Add social accounts for the authenticated user |
| DELETE | /user/social_accounts | Delete social accounts for the authenticated user |
| GET | /user/ssh_signing_keys | List SSH signing keys for the authenticated user |
| POST | /user/ssh_signing_keys | Create a SSH signing key for the authenticated user |
| GET | /user/ssh_signing_keys/{ssh_signing_key_id} | Get an SSH signing key for the authenticated user |
| DELETE | /user/ssh_signing_keys/{ssh_signing_key_id} | Delete an SSH signing key for the authenticated user |
| GET | /user/starred | List repositories starred by the authenticated user |
| GET | /user/starred/{owner}/{repo} | Check if a repository is starred by the authenticated user |
| PUT | /user/starred/{owner}/{repo} | Star a repository for the authenticated user |
| DELETE | /user/starred/{owner}/{repo} | Unstar a repository for the authenticated user |
| GET | /user/subscriptions | List repositories watched by the authenticated user |
| GET | /user/teams | List teams for the authenticated user |
| GET | /user/{account_id} | Get a user using their ID |
| POST | /user/{user_id}/projectsV2/{project_number}/drafts | Create draft item for user owned project |

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /users | List users |
| POST | /users/{user_id}/projectsV2/{project_number}/views | Create a view for a user-owned project |
| GET | /users/{username} | Get a user |
| POST | /users/{username}/attestations/bulk-list | List attestations by bulk subject digests |
| POST | /users/{username}/attestations/delete-request | Delete attestations in bulk |
| DELETE | /users/{username}/attestations/digest/{subject_digest} | Delete attestations by subject digest |
| DELETE | /users/{username}/attestations/{attestation_id} | Delete attestations by ID |
| GET | /users/{username}/attestations/{subject_digest} | List attestations |
| GET | /users/{username}/docker/conflicts | Get list of conflicting packages during Docker migration for user |
| GET | /users/{username}/events | List events for the authenticated user |
| GET | /users/{username}/events/orgs/{org} | List organization events for the authenticated user |
| GET | /users/{username}/events/public | List public events for a user |
| GET | /users/{username}/followers | List followers of a user |
| GET | /users/{username}/following | List the people a user follows |
| GET | /users/{username}/following/{target_user} | Check if a user follows another user |
| GET | /users/{username}/gists | List gists for a user |
| GET | /users/{username}/gpg_keys | List GPG keys for a user |
| GET | /users/{username}/hovercard | Get contextual information for a user |
| GET | /users/{username}/installation | Get a user installation for the authenticated app |
| GET | /users/{username}/keys | List public keys for a user |
| GET | /users/{username}/orgs | List organizations for a user |
| GET | /users/{username}/packages | List packages for a user |
| GET | /users/{username}/packages/{package_type}/{package_name} | Get a package for a user |
| DELETE | /users/{username}/packages/{package_type}/{package_name} | Delete a package for a user |
| POST | /users/{username}/packages/{package_type}/{package_name}/restore | Restore a package for a user |
| GET | /users/{username}/packages/{package_type}/{package_name}/versions | List package versions for a package owned by a user |
| GET | /users/{username}/packages/{package_type}/{package_name}/versions/{package_version_id} | Get a package version for a user |
| DELETE | /users/{username}/packages/{package_type}/{package_name}/versions/{package_version_id} | Delete package version for a user |
| POST | /users/{username}/packages/{package_type}/{package_name}/versions/{package_version_id}/restore | Restore package version for a user |
| GET | /users/{username}/projectsV2 | List projects for user |
| GET | /users/{username}/projectsV2/{project_number} | Get project for user |
| GET | /users/{username}/projectsV2/{project_number}/fields | List project fields for user |
| POST | /users/{username}/projectsV2/{project_number}/fields | Add field to user owned project |
| GET | /users/{username}/projectsV2/{project_number}/fields/{field_id} | Get project field for user |
| GET | /users/{username}/projectsV2/{project_number}/items | List items for a user owned project |
| POST | /users/{username}/projectsV2/{project_number}/items | Add item to user owned project |
| GET | /users/{username}/projectsV2/{project_number}/items/{item_id} | Get an item for a user owned project |
| PATCH | /users/{username}/projectsV2/{project_number}/items/{item_id} | Update project item for user |
| DELETE | /users/{username}/projectsV2/{project_number}/items/{item_id} | Delete project item for user |
| GET | /users/{username}/projectsV2/{project_number}/views/{view_number}/items | List items for a user project view |
| GET | /users/{username}/received_events | List events received by the authenticated user |
| GET | /users/{username}/received_events/public | List public events received by a user |
| GET | /users/{username}/repos | List repositories for a user |
| GET | /users/{username}/settings/billing/premium_request/usage | Get billing premium request usage report for a user |
| GET | /users/{username}/settings/billing/usage | Get billing usage report for a user |
| GET | /users/{username}/settings/billing/usage/summary | Get billing usage summary for a user |
| GET | /users/{username}/social_accounts | List social accounts for a user |
| GET | /users/{username}/ssh_signing_keys | List SSH signing keys for a user |
| GET | /users/{username}/starred | List repositories starred by a user |
| GET | /users/{username}/subscriptions | List repositories watched by a user |

### versions
| Method | Path | Description |
|--------|------|-------------|
| GET | /versions | Get all API versions |

### zen
| Method | Path | Description |
|--------|------|-------------|
| GET | /zen | Get the Zen of GitHub |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all advisories?" -> GET /advisories
- "Get advisory details?" -> GET /advisories/{ghsa_id}
- "List all app?" -> GET /app
- "Create a conversion?" -> POST /app-manifests/{code}/conversions
- "List all config?" -> GET /app/hook/config
- "List all deliveries?" -> GET /app/hook/deliveries
- "Get delivery details?" -> GET /app/hook/deliveries/{delivery_id}
- "Create a attempt?" -> POST /app/hook/deliveries/{delivery_id}/attempts
- "List all installation-requests?" -> GET /app/installation-requests
- "List all installations?" -> GET /app/installations
- "Get installation details?" -> GET /app/installations/{installation_id}
- "Delete a installation?" -> DELETE /app/installations/{installation_id}
- "Create a access_token?" -> POST /app/installations/{installation_id}/access_tokens
- "Create a token?" -> POST /applications/{client_id}/token
- "Create a scoped?" -> POST /applications/{client_id}/token/scoped
- "Get app details?" -> GET /apps/{app_slug}
- "Get assignment details?" -> GET /assignments/{assignment_id}
- "List all accepted_assignments?" -> GET /assignments/{assignment_id}/accepted_assignments
- "List all grades?" -> GET /assignments/{assignment_id}/grades
- "List all classrooms?" -> GET /classrooms
- "Get classroom details?" -> GET /classrooms/{classroom_id}
- "List all assignments?" -> GET /classrooms/{classroom_id}/assignments
- "List all codes_of_conduct?" -> GET /codes_of_conduct
- "Get codes_of_conduct details?" -> GET /codes_of_conduct/{key}
- "Create a revoke?" -> POST /credentials/revoke
- "List all emojis?" -> GET /emojis
- "List all retention-limit?" -> GET /enterprises/{enterprise}/actions/cache/retention-limit
- "List all storage-limit?" -> GET /enterprises/{enterprise}/actions/cache/storage-limit
- "List all configurations?" -> GET /enterprises/{enterprise}/code-security/configurations
- "Create a configuration?" -> POST /enterprises/{enterprise}/code-security/configurations
- "List all defaults?" -> GET /enterprises/{enterprise}/code-security/configurations/defaults
- "Get configuration details?" -> GET /enterprises/{enterprise}/code-security/configurations/{configuration_id}
- "Partially update a configuration?" -> PATCH /enterprises/{enterprise}/code-security/configurations/{configuration_id}
- "Delete a configuration?" -> DELETE /enterprises/{enterprise}/code-security/configurations/{configuration_id}
- "Create a attach?" -> POST /enterprises/{enterprise}/code-security/configurations/{configuration_id}/attach
- "List all repositories?" -> GET /enterprises/{enterprise}/code-security/configurations/{configuration_id}/repositories
- "List all alerts?" -> GET /enterprises/{enterprise}/dependabot/alerts
- "List all teams?" -> GET /enterprises/{enterprise}/teams
- "Create a team?" -> POST /enterprises/{enterprise}/teams
- "List all memberships?" -> GET /enterprises/{enterprise}/teams/{enterprise-team}/memberships
- "Create a add?" -> POST /enterprises/{enterprise}/teams/{enterprise-team}/memberships/add
- "Create a remove?" -> POST /enterprises/{enterprise}/teams/{enterprise-team}/memberships/remove
- "Get membership details?" -> GET /enterprises/{enterprise}/teams/{enterprise-team}/memberships/{username}
- "Update a membership?" -> PUT /enterprises/{enterprise}/teams/{enterprise-team}/memberships/{username}
- "Delete a membership?" -> DELETE /enterprises/{enterprise}/teams/{enterprise-team}/memberships/{username}
- "List all organizations?" -> GET /enterprises/{enterprise}/teams/{enterprise-team}/organizations
- "Create a add?" -> POST /enterprises/{enterprise}/teams/{enterprise-team}/organizations/add
- "Create a remove?" -> POST /enterprises/{enterprise}/teams/{enterprise-team}/organizations/remove
- "Get organization details?" -> GET /enterprises/{enterprise}/teams/{enterprise-team}/organizations/{org}
- "Update a organization?" -> PUT /enterprises/{enterprise}/teams/{enterprise-team}/organizations/{org}
- "Delete a organization?" -> DELETE /enterprises/{enterprise}/teams/{enterprise-team}/organizations/{org}
- "Get team details?" -> GET /enterprises/{enterprise}/teams/{team_slug}
- "Partially update a team?" -> PATCH /enterprises/{enterprise}/teams/{team_slug}
- "Delete a team?" -> DELETE /enterprises/{enterprise}/teams/{team_slug}
- "List all events?" -> GET /events
- "List all feeds?" -> GET /feeds
- "List all gists?" -> GET /gists
- "Create a gist?" -> POST /gists
- "List all public?" -> GET /gists/public
- "List all starred?" -> GET /gists/starred
- "Get gist details?" -> GET /gists/{gist_id}
- "Partially update a gist?" -> PATCH /gists/{gist_id}
- "Delete a gist?" -> DELETE /gists/{gist_id}
- "List all comments?" -> GET /gists/{gist_id}/comments
- "Create a comment?" -> POST /gists/{gist_id}/comments
- "Get comment details?" -> GET /gists/{gist_id}/comments/{comment_id}
- "Partially update a comment?" -> PATCH /gists/{gist_id}/comments/{comment_id}
- "Delete a comment?" -> DELETE /gists/{gist_id}/comments/{comment_id}
- "List all commits?" -> GET /gists/{gist_id}/commits
- "List all forks?" -> GET /gists/{gist_id}/forks
- "Create a fork?" -> POST /gists/{gist_id}/forks
- "List all star?" -> GET /gists/{gist_id}/star
- "Get gist details?" -> GET /gists/{gist_id}/{sha}
- "List all templates?" -> GET /gitignore/templates
- "Get template details?" -> GET /gitignore/templates/{name}
- "List all repositories?" -> GET /installation/repositories
- "List all issues?" -> GET /issues
- "List all licenses?" -> GET /licenses
- "Get license details?" -> GET /licenses/{license}
- "Create a markdown?" -> POST /markdown
- "Create a raw?" -> POST /markdown/raw
- "Get account details?" -> GET /marketplace_listing/accounts/{account_id}
- "List all plans?" -> GET /marketplace_listing/plans
- "List all accounts?" -> GET /marketplace_listing/plans/{plan_id}/accounts
- "Get account details?" -> GET /marketplace_listing/stubbed/accounts/{account_id}
- "List all plans?" -> GET /marketplace_listing/stubbed/plans
- "List all accounts?" -> GET /marketplace_listing/stubbed/plans/{plan_id}/accounts
- "List all meta?" -> GET /meta
- "List all events?" -> GET /networks/{owner}/{repo}/events
- "List all notifications?" -> GET /notifications
- "Get thread details?" -> GET /notifications/threads/{thread_id}
- "Partially update a thread?" -> PATCH /notifications/threads/{thread_id}
- "Delete a thread?" -> DELETE /notifications/threads/{thread_id}
- "List all subscription?" -> GET /notifications/threads/{thread_id}/subscription
- "List all octocat?" -> GET /octocat
- "List all organizations?" -> GET /organizations
- "List all retention-limit?" -> GET /organizations/{org}/actions/cache/retention-limit
- "List all storage-limit?" -> GET /organizations/{org}/actions/cache/storage-limit
- "List all repository-access?" -> GET /organizations/{org}/dependabot/repository-access
- "List all budgets?" -> GET /organizations/{org}/settings/billing/budgets
- "Get budget details?" -> GET /organizations/{org}/settings/billing/budgets/{budget_id}
- "Partially update a budget?" -> PATCH /organizations/{org}/settings/billing/budgets/{budget_id}
- "Delete a budget?" -> DELETE /organizations/{org}/settings/billing/budgets/{budget_id}
- "List all usage?" -> GET /organizations/{org}/settings/billing/premium_request/usage
- "List all usage?" -> GET /organizations/{org}/settings/billing/usage
- "List all summary?" -> GET /organizations/{org}/settings/billing/usage/summary
- "Get org details?" -> GET /orgs/{org}
- "Partially update a org?" -> PATCH /orgs/{org}
- "Delete a org?" -> DELETE /orgs/{org}
- "List all usage?" -> GET /orgs/{org}/actions/cache/usage
- "List all usage-by-repository?" -> GET /orgs/{org}/actions/cache/usage-by-repository
- "List all hosted-runners?" -> GET /orgs/{org}/actions/hosted-runners
- "Create a hosted-runner?" -> POST /orgs/{org}/actions/hosted-runners
- "List all custom?" -> GET /orgs/{org}/actions/hosted-runners/images/custom
- "Get custom details?" -> GET /orgs/{org}/actions/hosted-runners/images/custom/{image_definition_id}
- "Delete a custom?" -> DELETE /orgs/{org}/actions/hosted-runners/images/custom/{image_definition_id}
- "List all versions?" -> GET /orgs/{org}/actions/hosted-runners/images/custom/{image_definition_id}/versions
- "Get version details?" -> GET /orgs/{org}/actions/hosted-runners/images/custom/{image_definition_id}/versions/{version}
- "Delete a version?" -> DELETE /orgs/{org}/actions/hosted-runners/images/custom/{image_definition_id}/versions/{version}
- "List all github-owned?" -> GET /orgs/{org}/actions/hosted-runners/images/github-owned
- "List all partner?" -> GET /orgs/{org}/actions/hosted-runners/images/partner
- "List all limits?" -> GET /orgs/{org}/actions/hosted-runners/limits
- "List all machine-sizes?" -> GET /orgs/{org}/actions/hosted-runners/machine-sizes
- "List all platforms?" -> GET /orgs/{org}/actions/hosted-runners/platforms
- "Get hosted-runner details?" -> GET /orgs/{org}/actions/hosted-runners/{hosted_runner_id}
- "Partially update a hosted-runner?" -> PATCH /orgs/{org}/actions/hosted-runners/{hosted_runner_id}
- "Delete a hosted-runner?" -> DELETE /orgs/{org}/actions/hosted-runners/{hosted_runner_id}
- "List all sub?" -> GET /orgs/{org}/actions/oidc/customization/sub
- "List all permissions?" -> GET /orgs/{org}/actions/permissions
- "List all artifact-and-log-retention?" -> GET /orgs/{org}/actions/permissions/artifact-and-log-retention
- "List all fork-pr-contributor-approval?" -> GET /orgs/{org}/actions/permissions/fork-pr-contributor-approval
- "List all fork-pr-workflows-private-repos?" -> GET /orgs/{org}/actions/permissions/fork-pr-workflows-private-repos
- "List all repositories?" -> GET /orgs/{org}/actions/permissions/repositories
- "Update a repository?" -> PUT /orgs/{org}/actions/permissions/repositories/{repository_id}
- "Delete a repository?" -> DELETE /orgs/{org}/actions/permissions/repositories/{repository_id}
- "List all selected-actions?" -> GET /orgs/{org}/actions/permissions/selected-actions
- "List all self-hosted-runners?" -> GET /orgs/{org}/actions/permissions/self-hosted-runners
- "List all repositories?" -> GET /orgs/{org}/actions/permissions/self-hosted-runners/repositories
- "Update a repository?" -> PUT /orgs/{org}/actions/permissions/self-hosted-runners/repositories/{repository_id}
- "Delete a repository?" -> DELETE /orgs/{org}/actions/permissions/self-hosted-runners/repositories/{repository_id}
- "List all workflow?" -> GET /orgs/{org}/actions/permissions/workflow
- "List all runner-groups?" -> GET /orgs/{org}/actions/runner-groups
- "Create a runner-group?" -> POST /orgs/{org}/actions/runner-groups
- "Get runner-group details?" -> GET /orgs/{org}/actions/runner-groups/{runner_group_id}
- "Partially update a runner-group?" -> PATCH /orgs/{org}/actions/runner-groups/{runner_group_id}
- "Delete a runner-group?" -> DELETE /orgs/{org}/actions/runner-groups/{runner_group_id}
- "List all hosted-runners?" -> GET /orgs/{org}/actions/runner-groups/{runner_group_id}/hosted-runners
- "List all repositories?" -> GET /orgs/{org}/actions/runner-groups/{runner_group_id}/repositories
- "Update a repository?" -> PUT /orgs/{org}/actions/runner-groups/{runner_group_id}/repositories/{repository_id}
- "Delete a repository?" -> DELETE /orgs/{org}/actions/runner-groups/{runner_group_id}/repositories/{repository_id}
- "List all runners?" -> GET /orgs/{org}/actions/runner-groups/{runner_group_id}/runners
- "Update a runner?" -> PUT /orgs/{org}/actions/runner-groups/{runner_group_id}/runners/{runner_id}
- "Delete a runner?" -> DELETE /orgs/{org}/actions/runner-groups/{runner_group_id}/runners/{runner_id}
- "List all runners?" -> GET /orgs/{org}/actions/runners
- "List all downloads?" -> GET /orgs/{org}/actions/runners/downloads
- "Create a generate-jitconfig?" -> POST /orgs/{org}/actions/runners/generate-jitconfig
- "Create a registration-token?" -> POST /orgs/{org}/actions/runners/registration-token
- "Create a remove-token?" -> POST /orgs/{org}/actions/runners/remove-token
- "Get runner details?" -> GET /orgs/{org}/actions/runners/{runner_id}
- "Delete a runner?" -> DELETE /orgs/{org}/actions/runners/{runner_id}
- "List all labels?" -> GET /orgs/{org}/actions/runners/{runner_id}/labels
- "Create a label?" -> POST /orgs/{org}/actions/runners/{runner_id}/labels
- "Delete a label?" -> DELETE /orgs/{org}/actions/runners/{runner_id}/labels/{name}
- "List all secrets?" -> GET /orgs/{org}/actions/secrets
- "List all public-key?" -> GET /orgs/{org}/actions/secrets/public-key
- "Get secret details?" -> GET /orgs/{org}/actions/secrets/{secret_name}
- "Update a secret?" -> PUT /orgs/{org}/actions/secrets/{secret_name}
- "Delete a secret?" -> DELETE /orgs/{org}/actions/secrets/{secret_name}
- "List all repositories?" -> GET /orgs/{org}/actions/secrets/{secret_name}/repositories
- "Update a repository?" -> PUT /orgs/{org}/actions/secrets/{secret_name}/repositories/{repository_id}
- "Delete a repository?" -> DELETE /orgs/{org}/actions/secrets/{secret_name}/repositories/{repository_id}
- "List all variables?" -> GET /orgs/{org}/actions/variables
- "Create a variable?" -> POST /orgs/{org}/actions/variables
- "Get variable details?" -> GET /orgs/{org}/actions/variables/{name}
- "Partially update a variable?" -> PATCH /orgs/{org}/actions/variables/{name}
- "Delete a variable?" -> DELETE /orgs/{org}/actions/variables/{name}
- "List all repositories?" -> GET /orgs/{org}/actions/variables/{name}/repositories
- "Update a repository?" -> PUT /orgs/{org}/actions/variables/{name}/repositories/{repository_id}
- "Delete a repository?" -> DELETE /orgs/{org}/actions/variables/{name}/repositories/{repository_id}
- "Create a deployment-record?" -> POST /orgs/{org}/artifacts/metadata/deployment-record
- "Create a storage-record?" -> POST /orgs/{org}/artifacts/metadata/storage-record
- "List all deployment-records?" -> GET /orgs/{org}/artifacts/{subject_digest}/metadata/deployment-records
- "List all storage-records?" -> GET /orgs/{org}/artifacts/{subject_digest}/metadata/storage-records
- "Create a bulk-list?" -> POST /orgs/{org}/attestations/bulk-list
- "Create a delete-request?" -> POST /orgs/{org}/attestations/delete-request
- "Delete a digest?" -> DELETE /orgs/{org}/attestations/digest/{subject_digest}
- "List all repositories?" -> GET /orgs/{org}/attestations/repositories
- "Delete a attestation?" -> DELETE /orgs/{org}/attestations/{attestation_id}
- "Get attestation details?" -> GET /orgs/{org}/attestations/{subject_digest}
- "List all blocks?" -> GET /orgs/{org}/blocks
- "Get block details?" -> GET /orgs/{org}/blocks/{username}
- "Update a block?" -> PUT /orgs/{org}/blocks/{username}
- "Delete a block?" -> DELETE /orgs/{org}/blocks/{username}
- "List all campaigns?" -> GET /orgs/{org}/campaigns
- "Create a campaign?" -> POST /orgs/{org}/campaigns
- "Get campaign details?" -> GET /orgs/{org}/campaigns/{campaign_number}
- "Partially update a campaign?" -> PATCH /orgs/{org}/campaigns/{campaign_number}
- "Delete a campaign?" -> DELETE /orgs/{org}/campaigns/{campaign_number}
- "List all alerts?" -> GET /orgs/{org}/code-scanning/alerts
- "List all configurations?" -> GET /orgs/{org}/code-security/configurations
- "Create a configuration?" -> POST /orgs/{org}/code-security/configurations
- "List all defaults?" -> GET /orgs/{org}/code-security/configurations/defaults
- "Get configuration details?" -> GET /orgs/{org}/code-security/configurations/{configuration_id}
- "Partially update a configuration?" -> PATCH /orgs/{org}/code-security/configurations/{configuration_id}
- "Delete a configuration?" -> DELETE /orgs/{org}/code-security/configurations/{configuration_id}
- "Create a attach?" -> POST /orgs/{org}/code-security/configurations/{configuration_id}/attach
- "List all repositories?" -> GET /orgs/{org}/code-security/configurations/{configuration_id}/repositories
- "List all codespaces?" -> GET /orgs/{org}/codespaces
- "Create a selected_user?" -> POST /orgs/{org}/codespaces/access/selected_users
- "List all secrets?" -> GET /orgs/{org}/codespaces/secrets
- "List all public-key?" -> GET /orgs/{org}/codespaces/secrets/public-key
- "Get secret details?" -> GET /orgs/{org}/codespaces/secrets/{secret_name}
- "Update a secret?" -> PUT /orgs/{org}/codespaces/secrets/{secret_name}
- "Delete a secret?" -> DELETE /orgs/{org}/codespaces/secrets/{secret_name}
- "List all repositories?" -> GET /orgs/{org}/codespaces/secrets/{secret_name}/repositories
- "Update a repository?" -> PUT /orgs/{org}/codespaces/secrets/{secret_name}/repositories/{repository_id}
- "Delete a repository?" -> DELETE /orgs/{org}/codespaces/secrets/{secret_name}/repositories/{repository_id}
- "List all billing?" -> GET /orgs/{org}/copilot/billing
- "List all seats?" -> GET /orgs/{org}/copilot/billing/seats
- "Create a selected_team?" -> POST /orgs/{org}/copilot/billing/selected_teams
- "Create a selected_user?" -> POST /orgs/{org}/copilot/billing/selected_users
- "List all content_exclusion?" -> GET /orgs/{org}/copilot/content_exclusion
- "List all metrics?" -> GET /orgs/{org}/copilot/metrics
- "List all alerts?" -> GET /orgs/{org}/dependabot/alerts
- "List all secrets?" -> GET /orgs/{org}/dependabot/secrets
- "List all public-key?" -> GET /orgs/{org}/dependabot/secrets/public-key
- "Get secret details?" -> GET /orgs/{org}/dependabot/secrets/{secret_name}
- "Update a secret?" -> PUT /orgs/{org}/dependabot/secrets/{secret_name}
- "Delete a secret?" -> DELETE /orgs/{org}/dependabot/secrets/{secret_name}
- "List all repositories?" -> GET /orgs/{org}/dependabot/secrets/{secret_name}/repositories
- "Update a repository?" -> PUT /orgs/{org}/dependabot/secrets/{secret_name}/repositories/{repository_id}
- "Delete a repository?" -> DELETE /orgs/{org}/dependabot/secrets/{secret_name}/repositories/{repository_id}
- "List all conflicts?" -> GET /orgs/{org}/docker/conflicts
- "List all events?" -> GET /orgs/{org}/events
- "List all failed_invitations?" -> GET /orgs/{org}/failed_invitations
- "List all hooks?" -> GET /orgs/{org}/hooks
- "Create a hook?" -> POST /orgs/{org}/hooks
- "Get hook details?" -> GET /orgs/{org}/hooks/{hook_id}
- "Partially update a hook?" -> PATCH /orgs/{org}/hooks/{hook_id}
- "Delete a hook?" -> DELETE /orgs/{org}/hooks/{hook_id}
- "List all config?" -> GET /orgs/{org}/hooks/{hook_id}/config
- "List all deliveries?" -> GET /orgs/{org}/hooks/{hook_id}/deliveries
- "Get delivery details?" -> GET /orgs/{org}/hooks/{hook_id}/deliveries/{delivery_id}
- "Create a attempt?" -> POST /orgs/{org}/hooks/{hook_id}/deliveries/{delivery_id}/attempts
- "Create a ping?" -> POST /orgs/{org}/hooks/{hook_id}/pings
- "Get route-stat details?" -> GET /orgs/{org}/insights/api/route-stats/{actor_type}/{actor_id}
- "List all subject-stats?" -> GET /orgs/{org}/insights/api/subject-stats
- "List all summary-stats?" -> GET /orgs/{org}/insights/api/summary-stats
- "Get user details?" -> GET /orgs/{org}/insights/api/summary-stats/users/{user_id}
- "Get summary-stat details?" -> GET /orgs/{org}/insights/api/summary-stats/{actor_type}/{actor_id}
- "List all time-stats?" -> GET /orgs/{org}/insights/api/time-stats
- "Get user details?" -> GET /orgs/{org}/insights/api/time-stats/users/{user_id}
- "Get time-stat details?" -> GET /orgs/{org}/insights/api/time-stats/{actor_type}/{actor_id}
- "Get user-stat details?" -> GET /orgs/{org}/insights/api/user-stats/{user_id}
- "List all installation?" -> GET /orgs/{org}/installation
- "List all installations?" -> GET /orgs/{org}/installations
- "List all interaction-limits?" -> GET /orgs/{org}/interaction-limits
- "List all invitations?" -> GET /orgs/{org}/invitations
- "Create a invitation?" -> POST /orgs/{org}/invitations
- "Delete a invitation?" -> DELETE /orgs/{org}/invitations/{invitation_id}
- "List all teams?" -> GET /orgs/{org}/invitations/{invitation_id}/teams
- "List all issue-types?" -> GET /orgs/{org}/issue-types
- "Create a issue-type?" -> POST /orgs/{org}/issue-types
- "Update a issue-type?" -> PUT /orgs/{org}/issue-types/{issue_type_id}
- "Delete a issue-type?" -> DELETE /orgs/{org}/issue-types/{issue_type_id}
- "List all issues?" -> GET /orgs/{org}/issues
- "List all members?" -> GET /orgs/{org}/members
- "Get member details?" -> GET /orgs/{org}/members/{username}
- "Delete a member?" -> DELETE /orgs/{org}/members/{username}
- "List all codespaces?" -> GET /orgs/{org}/members/{username}/codespaces
- "Delete a codespace?" -> DELETE /orgs/{org}/members/{username}/codespaces/{codespace_name}
- "Create a stop?" -> POST /orgs/{org}/members/{username}/codespaces/{codespace_name}/stop
- "List all copilot?" -> GET /orgs/{org}/members/{username}/copilot
- "Get membership details?" -> GET /orgs/{org}/memberships/{username}
- "Update a membership?" -> PUT /orgs/{org}/memberships/{username}
- "Delete a membership?" -> DELETE /orgs/{org}/memberships/{username}
- "List all migrations?" -> GET /orgs/{org}/migrations
- "Create a migration?" -> POST /orgs/{org}/migrations
- "Get migration details?" -> GET /orgs/{org}/migrations/{migration_id}
- "List all archive?" -> GET /orgs/{org}/migrations/{migration_id}/archive
- "List all repositories?" -> GET /orgs/{org}/migrations/{migration_id}/repositories
- "List all organization-roles?" -> GET /orgs/{org}/organization-roles
- "Delete a team?" -> DELETE /orgs/{org}/organization-roles/teams/{team_slug}
- "Update a team?" -> PUT /orgs/{org}/organization-roles/teams/{team_slug}/{role_id}
- "Delete a team?" -> DELETE /orgs/{org}/organization-roles/teams/{team_slug}/{role_id}
- "Delete a user?" -> DELETE /orgs/{org}/organization-roles/users/{username}
- "Update a user?" -> PUT /orgs/{org}/organization-roles/users/{username}/{role_id}
- "Delete a user?" -> DELETE /orgs/{org}/organization-roles/users/{username}/{role_id}
- "Get organization-role details?" -> GET /orgs/{org}/organization-roles/{role_id}
- "List all teams?" -> GET /orgs/{org}/organization-roles/{role_id}/teams
- "List all users?" -> GET /orgs/{org}/organization-roles/{role_id}/users
- "List all outside_collaborators?" -> GET /orgs/{org}/outside_collaborators
- "Update a outside_collaborator?" -> PUT /orgs/{org}/outside_collaborators/{username}
- "Delete a outside_collaborator?" -> DELETE /orgs/{org}/outside_collaborators/{username}
- "List all packages?" -> GET /orgs/{org}/packages
- "Get package details?" -> GET /orgs/{org}/packages/{package_type}/{package_name}
- "Delete a package?" -> DELETE /orgs/{org}/packages/{package_type}/{package_name}
- "Create a restore?" -> POST /orgs/{org}/packages/{package_type}/{package_name}/restore
- "List all versions?" -> GET /orgs/{org}/packages/{package_type}/{package_name}/versions
- "Get version details?" -> GET /orgs/{org}/packages/{package_type}/{package_name}/versions/{package_version_id}
- "Delete a version?" -> DELETE /orgs/{org}/packages/{package_type}/{package_name}/versions/{package_version_id}
- "Create a restore?" -> POST /orgs/{org}/packages/{package_type}/{package_name}/versions/{package_version_id}/restore
- "List all personal-access-token-requests?" -> GET /orgs/{org}/personal-access-token-requests
- "Create a personal-access-token-request?" -> POST /orgs/{org}/personal-access-token-requests
- "List all repositories?" -> GET /orgs/{org}/personal-access-token-requests/{pat_request_id}/repositories
- "List all personal-access-tokens?" -> GET /orgs/{org}/personal-access-tokens
- "Create a personal-access-token?" -> POST /orgs/{org}/personal-access-tokens
- "List all repositories?" -> GET /orgs/{org}/personal-access-tokens/{pat_id}/repositories
- "List all private-registries?" -> GET /orgs/{org}/private-registries
- "Create a private-registry?" -> POST /orgs/{org}/private-registries
- "List all public-key?" -> GET /orgs/{org}/private-registries/public-key
- "Get private-registry details?" -> GET /orgs/{org}/private-registries/{secret_name}
- "Partially update a private-registry?" -> PATCH /orgs/{org}/private-registries/{secret_name}
- "Delete a private-registry?" -> DELETE /orgs/{org}/private-registries/{secret_name}
- "Search projectsV2?" -> GET /orgs/{org}/projectsV2
- "Get projectsV2 details?" -> GET /orgs/{org}/projectsV2/{project_number}
- "Create a draft?" -> POST /orgs/{org}/projectsV2/{project_number}/drafts
- "List all fields?" -> GET /orgs/{org}/projectsV2/{project_number}/fields
- "Create a field?" -> POST /orgs/{org}/projectsV2/{project_number}/fields
- "Get field details?" -> GET /orgs/{org}/projectsV2/{project_number}/fields/{field_id}
- "Search items?" -> GET /orgs/{org}/projectsV2/{project_number}/items
- "Create a item?" -> POST /orgs/{org}/projectsV2/{project_number}/items
- "Get item details?" -> GET /orgs/{org}/projectsV2/{project_number}/items/{item_id}
- "Partially update a item?" -> PATCH /orgs/{org}/projectsV2/{project_number}/items/{item_id}
- "Delete a item?" -> DELETE /orgs/{org}/projectsV2/{project_number}/items/{item_id}
- "Create a view?" -> POST /orgs/{org}/projectsV2/{project_number}/views
- "List all items?" -> GET /orgs/{org}/projectsV2/{project_number}/views/{view_number}/items
- "List all schema?" -> GET /orgs/{org}/properties/schema
- "Get schema details?" -> GET /orgs/{org}/properties/schema/{custom_property_name}
- "Update a schema?" -> PUT /orgs/{org}/properties/schema/{custom_property_name}
- "Delete a schema?" -> DELETE /orgs/{org}/properties/schema/{custom_property_name}
- "List all values?" -> GET /orgs/{org}/properties/values
- "List all public_members?" -> GET /orgs/{org}/public_members
- "Get public_member details?" -> GET /orgs/{org}/public_members/{username}
- "Update a public_member?" -> PUT /orgs/{org}/public_members/{username}
- "Delete a public_member?" -> DELETE /orgs/{org}/public_members/{username}
- "List all repos?" -> GET /orgs/{org}/repos
- "Create a repo?" -> POST /orgs/{org}/repos
- "List all rulesets?" -> GET /orgs/{org}/rulesets
- "Create a ruleset?" -> POST /orgs/{org}/rulesets
- "List all rule-suites?" -> GET /orgs/{org}/rulesets/rule-suites
- "Get rule-suite details?" -> GET /orgs/{org}/rulesets/rule-suites/{rule_suite_id}
- "Get ruleset details?" -> GET /orgs/{org}/rulesets/{ruleset_id}
- "Update a ruleset?" -> PUT /orgs/{org}/rulesets/{ruleset_id}
- "Delete a ruleset?" -> DELETE /orgs/{org}/rulesets/{ruleset_id}
- "List all history?" -> GET /orgs/{org}/rulesets/{ruleset_id}/history
- "Get history details?" -> GET /orgs/{org}/rulesets/{ruleset_id}/history/{version_id}
- "List all alerts?" -> GET /orgs/{org}/secret-scanning/alerts
- "List all pattern-configurations?" -> GET /orgs/{org}/secret-scanning/pattern-configurations
- "List all security-advisories?" -> GET /orgs/{org}/security-advisories
- "List all security-managers?" -> GET /orgs/{org}/security-managers
- "Update a team?" -> PUT /orgs/{org}/security-managers/teams/{team_slug}
- "Delete a team?" -> DELETE /orgs/{org}/security-managers/teams/{team_slug}
- "List all immutable-releases?" -> GET /orgs/{org}/settings/immutable-releases
- "List all repositories?" -> GET /orgs/{org}/settings/immutable-releases/repositories
- "Update a repository?" -> PUT /orgs/{org}/settings/immutable-releases/repositories/{repository_id}
- "Delete a repository?" -> DELETE /orgs/{org}/settings/immutable-releases/repositories/{repository_id}
- "List all network-configurations?" -> GET /orgs/{org}/settings/network-configurations
- "Create a network-configuration?" -> POST /orgs/{org}/settings/network-configurations
- "Get network-configuration details?" -> GET /orgs/{org}/settings/network-configurations/{network_configuration_id}
- "Partially update a network-configuration?" -> PATCH /orgs/{org}/settings/network-configurations/{network_configuration_id}
- "Delete a network-configuration?" -> DELETE /orgs/{org}/settings/network-configurations/{network_configuration_id}
- "Get network-setting details?" -> GET /orgs/{org}/settings/network-settings/{network_settings_id}
- "List all metrics?" -> GET /orgs/{org}/team/{team_slug}/copilot/metrics
- "List all teams?" -> GET /orgs/{org}/teams
- "Create a team?" -> POST /orgs/{org}/teams
- "Get team details?" -> GET /orgs/{org}/teams/{team_slug}
- "Partially update a team?" -> PATCH /orgs/{org}/teams/{team_slug}
- "Delete a team?" -> DELETE /orgs/{org}/teams/{team_slug}
- "List all invitations?" -> GET /orgs/{org}/teams/{team_slug}/invitations
- "List all members?" -> GET /orgs/{org}/teams/{team_slug}/members
- "Get membership details?" -> GET /orgs/{org}/teams/{team_slug}/memberships/{username}
- "Update a membership?" -> PUT /orgs/{org}/teams/{team_slug}/memberships/{username}
- "Delete a membership?" -> DELETE /orgs/{org}/teams/{team_slug}/memberships/{username}
- "List all repos?" -> GET /orgs/{org}/teams/{team_slug}/repos
- "Get repo details?" -> GET /orgs/{org}/teams/{team_slug}/repos/{owner}/{repo}
- "Update a repo?" -> PUT /orgs/{org}/teams/{team_slug}/repos/{owner}/{repo}
- "Delete a repo?" -> DELETE /orgs/{org}/teams/{team_slug}/repos/{owner}/{repo}
- "List all teams?" -> GET /orgs/{org}/teams/{team_slug}/teams
- "List all rate_limit?" -> GET /rate_limit
- "Get repo details?" -> GET /repos/{owner}/{repo}
- "Partially update a repo?" -> PATCH /repos/{owner}/{repo}
- "Delete a repo?" -> DELETE /repos/{owner}/{repo}
- "List all artifacts?" -> GET /repos/{owner}/{repo}/actions/artifacts
- "Get artifact details?" -> GET /repos/{owner}/{repo}/actions/artifacts/{artifact_id}
- "Delete a artifact?" -> DELETE /repos/{owner}/{repo}/actions/artifacts/{artifact_id}
- "Get artifact details?" -> GET /repos/{owner}/{repo}/actions/artifacts/{artifact_id}/{archive_format}
- "List all retention-limit?" -> GET /repos/{owner}/{repo}/actions/cache/retention-limit
- "List all storage-limit?" -> GET /repos/{owner}/{repo}/actions/cache/storage-limit
- "List all usage?" -> GET /repos/{owner}/{repo}/actions/cache/usage
- "List all caches?" -> GET /repos/{owner}/{repo}/actions/caches
- "Delete a cache?" -> DELETE /repos/{owner}/{repo}/actions/caches/{cache_id}
- "Get job details?" -> GET /repos/{owner}/{repo}/actions/jobs/{job_id}
- "List all logs?" -> GET /repos/{owner}/{repo}/actions/jobs/{job_id}/logs
- "Create a rerun?" -> POST /repos/{owner}/{repo}/actions/jobs/{job_id}/rerun
- "List all sub?" -> GET /repos/{owner}/{repo}/actions/oidc/customization/sub
- "List all organization-secrets?" -> GET /repos/{owner}/{repo}/actions/organization-secrets
- "List all organization-variables?" -> GET /repos/{owner}/{repo}/actions/organization-variables
- "List all permissions?" -> GET /repos/{owner}/{repo}/actions/permissions
- "List all access?" -> GET /repos/{owner}/{repo}/actions/permissions/access
- "List all artifact-and-log-retention?" -> GET /repos/{owner}/{repo}/actions/permissions/artifact-and-log-retention
- "List all fork-pr-contributor-approval?" -> GET /repos/{owner}/{repo}/actions/permissions/fork-pr-contributor-approval
- "List all fork-pr-workflows-private-repos?" -> GET /repos/{owner}/{repo}/actions/permissions/fork-pr-workflows-private-repos
- "List all selected-actions?" -> GET /repos/{owner}/{repo}/actions/permissions/selected-actions
- "List all workflow?" -> GET /repos/{owner}/{repo}/actions/permissions/workflow
- "List all runners?" -> GET /repos/{owner}/{repo}/actions/runners
- "List all downloads?" -> GET /repos/{owner}/{repo}/actions/runners/downloads
- "Create a generate-jitconfig?" -> POST /repos/{owner}/{repo}/actions/runners/generate-jitconfig
- "Create a registration-token?" -> POST /repos/{owner}/{repo}/actions/runners/registration-token
- "Create a remove-token?" -> POST /repos/{owner}/{repo}/actions/runners/remove-token
- "Get runner details?" -> GET /repos/{owner}/{repo}/actions/runners/{runner_id}
- "Delete a runner?" -> DELETE /repos/{owner}/{repo}/actions/runners/{runner_id}
- "List all labels?" -> GET /repos/{owner}/{repo}/actions/runners/{runner_id}/labels
- "Create a label?" -> POST /repos/{owner}/{repo}/actions/runners/{runner_id}/labels
- "Delete a label?" -> DELETE /repos/{owner}/{repo}/actions/runners/{runner_id}/labels/{name}
- "List all runs?" -> GET /repos/{owner}/{repo}/actions/runs
- "Get run details?" -> GET /repos/{owner}/{repo}/actions/runs/{run_id}
- "Delete a run?" -> DELETE /repos/{owner}/{repo}/actions/runs/{run_id}
- "List all approvals?" -> GET /repos/{owner}/{repo}/actions/runs/{run_id}/approvals
- "Create a approve?" -> POST /repos/{owner}/{repo}/actions/runs/{run_id}/approve
- "List all artifacts?" -> GET /repos/{owner}/{repo}/actions/runs/{run_id}/artifacts
- "Get attempt details?" -> GET /repos/{owner}/{repo}/actions/runs/{run_id}/attempts/{attempt_number}
- "List all jobs?" -> GET /repos/{owner}/{repo}/actions/runs/{run_id}/attempts/{attempt_number}/jobs
- "List all logs?" -> GET /repos/{owner}/{repo}/actions/runs/{run_id}/attempts/{attempt_number}/logs
- "Create a cancel?" -> POST /repos/{owner}/{repo}/actions/runs/{run_id}/cancel
- "Create a deployment_protection_rule?" -> POST /repos/{owner}/{repo}/actions/runs/{run_id}/deployment_protection_rule
- "Create a force-cancel?" -> POST /repos/{owner}/{repo}/actions/runs/{run_id}/force-cancel
- "List all jobs?" -> GET /repos/{owner}/{repo}/actions/runs/{run_id}/jobs
- "List all logs?" -> GET /repos/{owner}/{repo}/actions/runs/{run_id}/logs
- "List all pending_deployments?" -> GET /repos/{owner}/{repo}/actions/runs/{run_id}/pending_deployments
- "Create a pending_deployment?" -> POST /repos/{owner}/{repo}/actions/runs/{run_id}/pending_deployments
- "Create a rerun?" -> POST /repos/{owner}/{repo}/actions/runs/{run_id}/rerun
- "Create a rerun-failed-job?" -> POST /repos/{owner}/{repo}/actions/runs/{run_id}/rerun-failed-jobs
- "List all timing?" -> GET /repos/{owner}/{repo}/actions/runs/{run_id}/timing
- "List all secrets?" -> GET /repos/{owner}/{repo}/actions/secrets
- "List all public-key?" -> GET /repos/{owner}/{repo}/actions/secrets/public-key
- "Get secret details?" -> GET /repos/{owner}/{repo}/actions/secrets/{secret_name}
- "Update a secret?" -> PUT /repos/{owner}/{repo}/actions/secrets/{secret_name}
- "Delete a secret?" -> DELETE /repos/{owner}/{repo}/actions/secrets/{secret_name}
- "List all variables?" -> GET /repos/{owner}/{repo}/actions/variables
- "Create a variable?" -> POST /repos/{owner}/{repo}/actions/variables
- "Get variable details?" -> GET /repos/{owner}/{repo}/actions/variables/{name}
- "Partially update a variable?" -> PATCH /repos/{owner}/{repo}/actions/variables/{name}
- "Delete a variable?" -> DELETE /repos/{owner}/{repo}/actions/variables/{name}
- "List all workflows?" -> GET /repos/{owner}/{repo}/actions/workflows
- "Get workflow details?" -> GET /repos/{owner}/{repo}/actions/workflows/{workflow_id}
- "Create a dispatche?" -> POST /repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches
- "List all runs?" -> GET /repos/{owner}/{repo}/actions/workflows/{workflow_id}/runs
- "List all timing?" -> GET /repos/{owner}/{repo}/actions/workflows/{workflow_id}/timing
- "List all activity?" -> GET /repos/{owner}/{repo}/activity
- "List all assignees?" -> GET /repos/{owner}/{repo}/assignees
- "Get assignee details?" -> GET /repos/{owner}/{repo}/assignees/{assignee}
- "Create a attestation?" -> POST /repos/{owner}/{repo}/attestations
- "Get attestation details?" -> GET /repos/{owner}/{repo}/attestations/{subject_digest}
- "List all autolinks?" -> GET /repos/{owner}/{repo}/autolinks
- "Create a autolink?" -> POST /repos/{owner}/{repo}/autolinks
- "Get autolink details?" -> GET /repos/{owner}/{repo}/autolinks/{autolink_id}
- "Delete a autolink?" -> DELETE /repos/{owner}/{repo}/autolinks/{autolink_id}
- "List all automated-security-fixes?" -> GET /repos/{owner}/{repo}/automated-security-fixes
- "List all branches?" -> GET /repos/{owner}/{repo}/branches
- "Get branche details?" -> GET /repos/{owner}/{repo}/branches/{branch}
- "List all protection?" -> GET /repos/{owner}/{repo}/branches/{branch}/protection
- "List all enforce_admins?" -> GET /repos/{owner}/{repo}/branches/{branch}/protection/enforce_admins
- "Create a enforce_admin?" -> POST /repos/{owner}/{repo}/branches/{branch}/protection/enforce_admins
- "List all required_pull_request_reviews?" -> GET /repos/{owner}/{repo}/branches/{branch}/protection/required_pull_request_reviews
- "List all required_signatures?" -> GET /repos/{owner}/{repo}/branches/{branch}/protection/required_signatures
- "Create a required_signature?" -> POST /repos/{owner}/{repo}/branches/{branch}/protection/required_signatures
- "List all required_status_checks?" -> GET /repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks
- "List all contexts?" -> GET /repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks/contexts
- "Create a context?" -> POST /repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks/contexts
- "List all restrictions?" -> GET /repos/{owner}/{repo}/branches/{branch}/protection/restrictions
- "List all apps?" -> GET /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/apps
- "Create a app?" -> POST /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/apps
- "List all teams?" -> GET /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/teams
- "Create a team?" -> POST /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/teams
- "List all users?" -> GET /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/users
- "Create a user?" -> POST /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/users
- "Create a rename?" -> POST /repos/{owner}/{repo}/branches/{branch}/rename
- "Create a check-run?" -> POST /repos/{owner}/{repo}/check-runs
- "Get check-run details?" -> GET /repos/{owner}/{repo}/check-runs/{check_run_id}
- "Partially update a check-run?" -> PATCH /repos/{owner}/{repo}/check-runs/{check_run_id}
- "List all annotations?" -> GET /repos/{owner}/{repo}/check-runs/{check_run_id}/annotations
- "Create a rerequest?" -> POST /repos/{owner}/{repo}/check-runs/{check_run_id}/rerequest
- "Create a check-suite?" -> POST /repos/{owner}/{repo}/check-suites
- "Get check-suite details?" -> GET /repos/{owner}/{repo}/check-suites/{check_suite_id}
- "List all check-runs?" -> GET /repos/{owner}/{repo}/check-suites/{check_suite_id}/check-runs
- "Create a rerequest?" -> POST /repos/{owner}/{repo}/check-suites/{check_suite_id}/rerequest
- "List all alerts?" -> GET /repos/{owner}/{repo}/code-scanning/alerts
- "Get alert details?" -> GET /repos/{owner}/{repo}/code-scanning/alerts/{alert_number}
- "Partially update a alert?" -> PATCH /repos/{owner}/{repo}/code-scanning/alerts/{alert_number}
- "List all autofix?" -> GET /repos/{owner}/{repo}/code-scanning/alerts/{alert_number}/autofix
- "Create a autofix?" -> POST /repos/{owner}/{repo}/code-scanning/alerts/{alert_number}/autofix
- "Create a commit?" -> POST /repos/{owner}/{repo}/code-scanning/alerts/{alert_number}/autofix/commits
- "List all instances?" -> GET /repos/{owner}/{repo}/code-scanning/alerts/{alert_number}/instances
- "List all analyses?" -> GET /repos/{owner}/{repo}/code-scanning/analyses
- "Get analysis details?" -> GET /repos/{owner}/{repo}/code-scanning/analyses/{analysis_id}
- "Delete a analysis?" -> DELETE /repos/{owner}/{repo}/code-scanning/analyses/{analysis_id}
- "List all databases?" -> GET /repos/{owner}/{repo}/code-scanning/codeql/databases
- "Get database details?" -> GET /repos/{owner}/{repo}/code-scanning/codeql/databases/{language}
- "Delete a database?" -> DELETE /repos/{owner}/{repo}/code-scanning/codeql/databases/{language}
- "Create a variant-analys?" -> POST /repos/{owner}/{repo}/code-scanning/codeql/variant-analyses
- "Get variant-analys details?" -> GET /repos/{owner}/{repo}/code-scanning/codeql/variant-analyses/{codeql_variant_analysis_id}
- "Get repo details?" -> GET /repos/{owner}/{repo}/code-scanning/codeql/variant-analyses/{codeql_variant_analysis_id}/repos/{repo_owner}/{repo_name}
- "List all default-setup?" -> GET /repos/{owner}/{repo}/code-scanning/default-setup
- "Create a sarif?" -> POST /repos/{owner}/{repo}/code-scanning/sarifs
- "Get sarif details?" -> GET /repos/{owner}/{repo}/code-scanning/sarifs/{sarif_id}
- "List all code-security-configuration?" -> GET /repos/{owner}/{repo}/code-security-configuration
- "List all errors?" -> GET /repos/{owner}/{repo}/codeowners/errors
- "List all codespaces?" -> GET /repos/{owner}/{repo}/codespaces
- "Create a codespace?" -> POST /repos/{owner}/{repo}/codespaces
- "List all devcontainers?" -> GET /repos/{owner}/{repo}/codespaces/devcontainers
- "List all machines?" -> GET /repos/{owner}/{repo}/codespaces/machines
- "List all new?" -> GET /repos/{owner}/{repo}/codespaces/new
- "List all permissions_check?" -> GET /repos/{owner}/{repo}/codespaces/permissions_check
- "List all secrets?" -> GET /repos/{owner}/{repo}/codespaces/secrets
- "List all public-key?" -> GET /repos/{owner}/{repo}/codespaces/secrets/public-key
- "Get secret details?" -> GET /repos/{owner}/{repo}/codespaces/secrets/{secret_name}
- "Update a secret?" -> PUT /repos/{owner}/{repo}/codespaces/secrets/{secret_name}
- "Delete a secret?" -> DELETE /repos/{owner}/{repo}/codespaces/secrets/{secret_name}
- "List all collaborators?" -> GET /repos/{owner}/{repo}/collaborators
- "Get collaborator details?" -> GET /repos/{owner}/{repo}/collaborators/{username}
- "Update a collaborator?" -> PUT /repos/{owner}/{repo}/collaborators/{username}
- "Delete a collaborator?" -> DELETE /repos/{owner}/{repo}/collaborators/{username}
- "List all permission?" -> GET /repos/{owner}/{repo}/collaborators/{username}/permission
- "List all comments?" -> GET /repos/{owner}/{repo}/comments
- "Get comment details?" -> GET /repos/{owner}/{repo}/comments/{comment_id}
- "Partially update a comment?" -> PATCH /repos/{owner}/{repo}/comments/{comment_id}
- "Delete a comment?" -> DELETE /repos/{owner}/{repo}/comments/{comment_id}
- "List all reactions?" -> GET /repos/{owner}/{repo}/comments/{comment_id}/reactions
- "Create a reaction?" -> POST /repos/{owner}/{repo}/comments/{comment_id}/reactions
- "Delete a reaction?" -> DELETE /repos/{owner}/{repo}/comments/{comment_id}/reactions/{reaction_id}
- "List all commits?" -> GET /repos/{owner}/{repo}/commits
- "List all branches-where-head?" -> GET /repos/{owner}/{repo}/commits/{commit_sha}/branches-where-head
- "List all comments?" -> GET /repos/{owner}/{repo}/commits/{commit_sha}/comments
- "Create a comment?" -> POST /repos/{owner}/{repo}/commits/{commit_sha}/comments
- "List all pulls?" -> GET /repos/{owner}/{repo}/commits/{commit_sha}/pulls
- "Get commit details?" -> GET /repos/{owner}/{repo}/commits/{ref}
- "List all check-runs?" -> GET /repos/{owner}/{repo}/commits/{ref}/check-runs
- "List all check-suites?" -> GET /repos/{owner}/{repo}/commits/{ref}/check-suites
- "List all status?" -> GET /repos/{owner}/{repo}/commits/{ref}/status
- "List all statuses?" -> GET /repos/{owner}/{repo}/commits/{ref}/statuses
- "List all profile?" -> GET /repos/{owner}/{repo}/community/profile
- "Get compare details?" -> GET /repos/{owner}/{repo}/compare/{basehead}
- "Get content details?" -> GET /repos/{owner}/{repo}/contents/{path}
- "Update a content?" -> PUT /repos/{owner}/{repo}/contents/{path}
- "Delete a content?" -> DELETE /repos/{owner}/{repo}/contents/{path}
- "List all contributors?" -> GET /repos/{owner}/{repo}/contributors
- "List all alerts?" -> GET /repos/{owner}/{repo}/dependabot/alerts
- "Get alert details?" -> GET /repos/{owner}/{repo}/dependabot/alerts/{alert_number}
- "Partially update a alert?" -> PATCH /repos/{owner}/{repo}/dependabot/alerts/{alert_number}
- "List all secrets?" -> GET /repos/{owner}/{repo}/dependabot/secrets
- "List all public-key?" -> GET /repos/{owner}/{repo}/dependabot/secrets/public-key
- "Get secret details?" -> GET /repos/{owner}/{repo}/dependabot/secrets/{secret_name}
- "Update a secret?" -> PUT /repos/{owner}/{repo}/dependabot/secrets/{secret_name}
- "Delete a secret?" -> DELETE /repos/{owner}/{repo}/dependabot/secrets/{secret_name}
- "Get compare details?" -> GET /repos/{owner}/{repo}/dependency-graph/compare/{basehead}
- "List all sbom?" -> GET /repos/{owner}/{repo}/dependency-graph/sbom
- "Create a snapshot?" -> POST /repos/{owner}/{repo}/dependency-graph/snapshots
- "List all deployments?" -> GET /repos/{owner}/{repo}/deployments
- "Create a deployment?" -> POST /repos/{owner}/{repo}/deployments
- "Get deployment details?" -> GET /repos/{owner}/{repo}/deployments/{deployment_id}
- "Delete a deployment?" -> DELETE /repos/{owner}/{repo}/deployments/{deployment_id}
- "List all statuses?" -> GET /repos/{owner}/{repo}/deployments/{deployment_id}/statuses
- "Create a statuse?" -> POST /repos/{owner}/{repo}/deployments/{deployment_id}/statuses
- "Get statuse details?" -> GET /repos/{owner}/{repo}/deployments/{deployment_id}/statuses/{status_id}
- "Create a dispatche?" -> POST /repos/{owner}/{repo}/dispatches
- "List all environments?" -> GET /repos/{owner}/{repo}/environments
- "Get environment details?" -> GET /repos/{owner}/{repo}/environments/{environment_name}
- "Update a environment?" -> PUT /repos/{owner}/{repo}/environments/{environment_name}
- "Delete a environment?" -> DELETE /repos/{owner}/{repo}/environments/{environment_name}
- "List all deployment-branch-policies?" -> GET /repos/{owner}/{repo}/environments/{environment_name}/deployment-branch-policies
- "Create a deployment-branch-policy?" -> POST /repos/{owner}/{repo}/environments/{environment_name}/deployment-branch-policies
- "Get deployment-branch-policy details?" -> GET /repos/{owner}/{repo}/environments/{environment_name}/deployment-branch-policies/{branch_policy_id}
- "Update a deployment-branch-policy?" -> PUT /repos/{owner}/{repo}/environments/{environment_name}/deployment-branch-policies/{branch_policy_id}
- "Delete a deployment-branch-policy?" -> DELETE /repos/{owner}/{repo}/environments/{environment_name}/deployment-branch-policies/{branch_policy_id}
- "List all deployment_protection_rules?" -> GET /repos/{owner}/{repo}/environments/{environment_name}/deployment_protection_rules
- "Create a deployment_protection_rule?" -> POST /repos/{owner}/{repo}/environments/{environment_name}/deployment_protection_rules
- "List all apps?" -> GET /repos/{owner}/{repo}/environments/{environment_name}/deployment_protection_rules/apps
- "Get deployment_protection_rule details?" -> GET /repos/{owner}/{repo}/environments/{environment_name}/deployment_protection_rules/{protection_rule_id}
- "Delete a deployment_protection_rule?" -> DELETE /repos/{owner}/{repo}/environments/{environment_name}/deployment_protection_rules/{protection_rule_id}
- "List all secrets?" -> GET /repos/{owner}/{repo}/environments/{environment_name}/secrets
- "List all public-key?" -> GET /repos/{owner}/{repo}/environments/{environment_name}/secrets/public-key
- "Get secret details?" -> GET /repos/{owner}/{repo}/environments/{environment_name}/secrets/{secret_name}
- "Update a secret?" -> PUT /repos/{owner}/{repo}/environments/{environment_name}/secrets/{secret_name}
- "Delete a secret?" -> DELETE /repos/{owner}/{repo}/environments/{environment_name}/secrets/{secret_name}
- "List all variables?" -> GET /repos/{owner}/{repo}/environments/{environment_name}/variables
- "Create a variable?" -> POST /repos/{owner}/{repo}/environments/{environment_name}/variables
- "Get variable details?" -> GET /repos/{owner}/{repo}/environments/{environment_name}/variables/{name}
- "Partially update a variable?" -> PATCH /repos/{owner}/{repo}/environments/{environment_name}/variables/{name}
- "Delete a variable?" -> DELETE /repos/{owner}/{repo}/environments/{environment_name}/variables/{name}
- "List all events?" -> GET /repos/{owner}/{repo}/events
- "List all forks?" -> GET /repos/{owner}/{repo}/forks
- "Create a fork?" -> POST /repos/{owner}/{repo}/forks
- "Create a blob?" -> POST /repos/{owner}/{repo}/git/blobs
- "Get blob details?" -> GET /repos/{owner}/{repo}/git/blobs/{file_sha}
- "Create a commit?" -> POST /repos/{owner}/{repo}/git/commits
- "Get commit details?" -> GET /repos/{owner}/{repo}/git/commits/{commit_sha}
- "Get matching-ref details?" -> GET /repos/{owner}/{repo}/git/matching-refs/{ref}
- "Get ref details?" -> GET /repos/{owner}/{repo}/git/ref/{ref}
- "Create a ref?" -> POST /repos/{owner}/{repo}/git/refs
- "Partially update a ref?" -> PATCH /repos/{owner}/{repo}/git/refs/{ref}
- "Delete a ref?" -> DELETE /repos/{owner}/{repo}/git/refs/{ref}
- "Create a tag?" -> POST /repos/{owner}/{repo}/git/tags
- "Get tag details?" -> GET /repos/{owner}/{repo}/git/tags/{tag_sha}
- "Create a tree?" -> POST /repos/{owner}/{repo}/git/trees
- "Get tree details?" -> GET /repos/{owner}/{repo}/git/trees/{tree_sha}
- "List all hooks?" -> GET /repos/{owner}/{repo}/hooks
- "Create a hook?" -> POST /repos/{owner}/{repo}/hooks
- "Get hook details?" -> GET /repos/{owner}/{repo}/hooks/{hook_id}
- "Partially update a hook?" -> PATCH /repos/{owner}/{repo}/hooks/{hook_id}
- "Delete a hook?" -> DELETE /repos/{owner}/{repo}/hooks/{hook_id}
- "List all config?" -> GET /repos/{owner}/{repo}/hooks/{hook_id}/config
- "List all deliveries?" -> GET /repos/{owner}/{repo}/hooks/{hook_id}/deliveries
- "Get delivery details?" -> GET /repos/{owner}/{repo}/hooks/{hook_id}/deliveries/{delivery_id}
- "Create a attempt?" -> POST /repos/{owner}/{repo}/hooks/{hook_id}/deliveries/{delivery_id}/attempts
- "Create a ping?" -> POST /repos/{owner}/{repo}/hooks/{hook_id}/pings
- "Create a test?" -> POST /repos/{owner}/{repo}/hooks/{hook_id}/tests
- "List all immutable-releases?" -> GET /repos/{owner}/{repo}/immutable-releases
- "List all import?" -> GET /repos/{owner}/{repo}/import
- "List all authors?" -> GET /repos/{owner}/{repo}/import/authors
- "Partially update a author?" -> PATCH /repos/{owner}/{repo}/import/authors/{author_id}
- "List all large_files?" -> GET /repos/{owner}/{repo}/import/large_files
- "List all installation?" -> GET /repos/{owner}/{repo}/installation
- "List all interaction-limits?" -> GET /repos/{owner}/{repo}/interaction-limits
- "List all invitations?" -> GET /repos/{owner}/{repo}/invitations
- "Partially update a invitation?" -> PATCH /repos/{owner}/{repo}/invitations/{invitation_id}
- "Delete a invitation?" -> DELETE /repos/{owner}/{repo}/invitations/{invitation_id}
- "List all issues?" -> GET /repos/{owner}/{repo}/issues
- "Create a issue?" -> POST /repos/{owner}/{repo}/issues
- "List all comments?" -> GET /repos/{owner}/{repo}/issues/comments
- "Get comment details?" -> GET /repos/{owner}/{repo}/issues/comments/{comment_id}
- "Partially update a comment?" -> PATCH /repos/{owner}/{repo}/issues/comments/{comment_id}
- "Delete a comment?" -> DELETE /repos/{owner}/{repo}/issues/comments/{comment_id}
- "List all reactions?" -> GET /repos/{owner}/{repo}/issues/comments/{comment_id}/reactions
- "Create a reaction?" -> POST /repos/{owner}/{repo}/issues/comments/{comment_id}/reactions
- "Delete a reaction?" -> DELETE /repos/{owner}/{repo}/issues/comments/{comment_id}/reactions/{reaction_id}
- "List all events?" -> GET /repos/{owner}/{repo}/issues/events
- "Get event details?" -> GET /repos/{owner}/{repo}/issues/events/{event_id}
- "Get issue details?" -> GET /repos/{owner}/{repo}/issues/{issue_number}
- "Partially update a issue?" -> PATCH /repos/{owner}/{repo}/issues/{issue_number}
- "Create a assignee?" -> POST /repos/{owner}/{repo}/issues/{issue_number}/assignees
- "Get assignee details?" -> GET /repos/{owner}/{repo}/issues/{issue_number}/assignees/{assignee}
- "List all comments?" -> GET /repos/{owner}/{repo}/issues/{issue_number}/comments
- "Create a comment?" -> POST /repos/{owner}/{repo}/issues/{issue_number}/comments
- "List all blocked_by?" -> GET /repos/{owner}/{repo}/issues/{issue_number}/dependencies/blocked_by
- "Create a blocked_by?" -> POST /repos/{owner}/{repo}/issues/{issue_number}/dependencies/blocked_by
- "Delete a blocked_by?" -> DELETE /repos/{owner}/{repo}/issues/{issue_number}/dependencies/blocked_by/{issue_id}
- "List all blocking?" -> GET /repos/{owner}/{repo}/issues/{issue_number}/dependencies/blocking
- "List all events?" -> GET /repos/{owner}/{repo}/issues/{issue_number}/events
- "List all labels?" -> GET /repos/{owner}/{repo}/issues/{issue_number}/labels
- "Create a label?" -> POST /repos/{owner}/{repo}/issues/{issue_number}/labels
- "Delete a label?" -> DELETE /repos/{owner}/{repo}/issues/{issue_number}/labels/{name}
- "List all parent?" -> GET /repos/{owner}/{repo}/issues/{issue_number}/parent
- "List all reactions?" -> GET /repos/{owner}/{repo}/issues/{issue_number}/reactions
- "Create a reaction?" -> POST /repos/{owner}/{repo}/issues/{issue_number}/reactions
- "Delete a reaction?" -> DELETE /repos/{owner}/{repo}/issues/{issue_number}/reactions/{reaction_id}
- "List all sub_issues?" -> GET /repos/{owner}/{repo}/issues/{issue_number}/sub_issues
- "Create a sub_issue?" -> POST /repos/{owner}/{repo}/issues/{issue_number}/sub_issues
- "List all timeline?" -> GET /repos/{owner}/{repo}/issues/{issue_number}/timeline
- "List all keys?" -> GET /repos/{owner}/{repo}/keys
- "Create a key?" -> POST /repos/{owner}/{repo}/keys
- "Get key details?" -> GET /repos/{owner}/{repo}/keys/{key_id}
- "Delete a key?" -> DELETE /repos/{owner}/{repo}/keys/{key_id}
- "List all labels?" -> GET /repos/{owner}/{repo}/labels
- "Create a label?" -> POST /repos/{owner}/{repo}/labels
- "Get label details?" -> GET /repos/{owner}/{repo}/labels/{name}
- "Partially update a label?" -> PATCH /repos/{owner}/{repo}/labels/{name}
- "Delete a label?" -> DELETE /repos/{owner}/{repo}/labels/{name}
- "List all languages?" -> GET /repos/{owner}/{repo}/languages
- "List all license?" -> GET /repos/{owner}/{repo}/license
- "Create a merge-upstream?" -> POST /repos/{owner}/{repo}/merge-upstream
- "Create a merge?" -> POST /repos/{owner}/{repo}/merges
- "List all milestones?" -> GET /repos/{owner}/{repo}/milestones
- "Create a milestone?" -> POST /repos/{owner}/{repo}/milestones
- "Get milestone details?" -> GET /repos/{owner}/{repo}/milestones/{milestone_number}
- "Partially update a milestone?" -> PATCH /repos/{owner}/{repo}/milestones/{milestone_number}
- "Delete a milestone?" -> DELETE /repos/{owner}/{repo}/milestones/{milestone_number}
- "List all labels?" -> GET /repos/{owner}/{repo}/milestones/{milestone_number}/labels
- "List all notifications?" -> GET /repos/{owner}/{repo}/notifications
- "List all pages?" -> GET /repos/{owner}/{repo}/pages
- "Create a page?" -> POST /repos/{owner}/{repo}/pages
- "List all builds?" -> GET /repos/{owner}/{repo}/pages/builds
- "Create a build?" -> POST /repos/{owner}/{repo}/pages/builds
- "List all latest?" -> GET /repos/{owner}/{repo}/pages/builds/latest
- "Get build details?" -> GET /repos/{owner}/{repo}/pages/builds/{build_id}
- "Create a deployment?" -> POST /repos/{owner}/{repo}/pages/deployments
- "Get deployment details?" -> GET /repos/{owner}/{repo}/pages/deployments/{pages_deployment_id}
- "Create a cancel?" -> POST /repos/{owner}/{repo}/pages/deployments/{pages_deployment_id}/cancel
- "List all health?" -> GET /repos/{owner}/{repo}/pages/health
- "List all private-vulnerability-reporting?" -> GET /repos/{owner}/{repo}/private-vulnerability-reporting
- "List all values?" -> GET /repos/{owner}/{repo}/properties/values
- "List all pulls?" -> GET /repos/{owner}/{repo}/pulls
- "Create a pull?" -> POST /repos/{owner}/{repo}/pulls
- "List all comments?" -> GET /repos/{owner}/{repo}/pulls/comments
- "Get comment details?" -> GET /repos/{owner}/{repo}/pulls/comments/{comment_id}
- "Partially update a comment?" -> PATCH /repos/{owner}/{repo}/pulls/comments/{comment_id}
- "Delete a comment?" -> DELETE /repos/{owner}/{repo}/pulls/comments/{comment_id}
- "List all reactions?" -> GET /repos/{owner}/{repo}/pulls/comments/{comment_id}/reactions
- "Create a reaction?" -> POST /repos/{owner}/{repo}/pulls/comments/{comment_id}/reactions
- "Delete a reaction?" -> DELETE /repos/{owner}/{repo}/pulls/comments/{comment_id}/reactions/{reaction_id}
- "Get pull details?" -> GET /repos/{owner}/{repo}/pulls/{pull_number}
- "Partially update a pull?" -> PATCH /repos/{owner}/{repo}/pulls/{pull_number}
- "Create a codespace?" -> POST /repos/{owner}/{repo}/pulls/{pull_number}/codespaces
- "List all comments?" -> GET /repos/{owner}/{repo}/pulls/{pull_number}/comments
- "Create a comment?" -> POST /repos/{owner}/{repo}/pulls/{pull_number}/comments
- "Create a reply?" -> POST /repos/{owner}/{repo}/pulls/{pull_number}/comments/{comment_id}/replies
- "List all commits?" -> GET /repos/{owner}/{repo}/pulls/{pull_number}/commits
- "List all files?" -> GET /repos/{owner}/{repo}/pulls/{pull_number}/files
- "List all merge?" -> GET /repos/{owner}/{repo}/pulls/{pull_number}/merge
- "List all requested_reviewers?" -> GET /repos/{owner}/{repo}/pulls/{pull_number}/requested_reviewers
- "Create a requested_reviewer?" -> POST /repos/{owner}/{repo}/pulls/{pull_number}/requested_reviewers
- "List all reviews?" -> GET /repos/{owner}/{repo}/pulls/{pull_number}/reviews
- "Create a review?" -> POST /repos/{owner}/{repo}/pulls/{pull_number}/reviews
- "Get review details?" -> GET /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
- "Update a review?" -> PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
- "Delete a review?" -> DELETE /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
- "List all comments?" -> GET /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}/comments
- "Create a event?" -> POST /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}/events
- "List all readme?" -> GET /repos/{owner}/{repo}/readme
- "Get readme details?" -> GET /repos/{owner}/{repo}/readme/{dir}
- "List all releases?" -> GET /repos/{owner}/{repo}/releases
- "Create a release?" -> POST /repos/{owner}/{repo}/releases
- "Get asset details?" -> GET /repos/{owner}/{repo}/releases/assets/{asset_id}
- "Partially update a asset?" -> PATCH /repos/{owner}/{repo}/releases/assets/{asset_id}
- "Delete a asset?" -> DELETE /repos/{owner}/{repo}/releases/assets/{asset_id}
- "Create a generate-note?" -> POST /repos/{owner}/{repo}/releases/generate-notes
- "List all latest?" -> GET /repos/{owner}/{repo}/releases/latest
- "Get tag details?" -> GET /repos/{owner}/{repo}/releases/tags/{tag}
- "Get release details?" -> GET /repos/{owner}/{repo}/releases/{release_id}
- "Partially update a release?" -> PATCH /repos/{owner}/{repo}/releases/{release_id}
- "Delete a release?" -> DELETE /repos/{owner}/{repo}/releases/{release_id}
- "List all assets?" -> GET /repos/{owner}/{repo}/releases/{release_id}/assets
- "Create a asset?" -> POST /repos/{owner}/{repo}/releases/{release_id}/assets
- "List all reactions?" -> GET /repos/{owner}/{repo}/releases/{release_id}/reactions
- "Create a reaction?" -> POST /repos/{owner}/{repo}/releases/{release_id}/reactions
- "Delete a reaction?" -> DELETE /repos/{owner}/{repo}/releases/{release_id}/reactions/{reaction_id}
- "Get branche details?" -> GET /repos/{owner}/{repo}/rules/branches/{branch}
- "List all rulesets?" -> GET /repos/{owner}/{repo}/rulesets
- "Create a ruleset?" -> POST /repos/{owner}/{repo}/rulesets
- "List all rule-suites?" -> GET /repos/{owner}/{repo}/rulesets/rule-suites
- "Get rule-suite details?" -> GET /repos/{owner}/{repo}/rulesets/rule-suites/{rule_suite_id}
- "Get ruleset details?" -> GET /repos/{owner}/{repo}/rulesets/{ruleset_id}
- "Update a ruleset?" -> PUT /repos/{owner}/{repo}/rulesets/{ruleset_id}
- "Delete a ruleset?" -> DELETE /repos/{owner}/{repo}/rulesets/{ruleset_id}
- "List all history?" -> GET /repos/{owner}/{repo}/rulesets/{ruleset_id}/history
- "Get history details?" -> GET /repos/{owner}/{repo}/rulesets/{ruleset_id}/history/{version_id}
- "List all alerts?" -> GET /repos/{owner}/{repo}/secret-scanning/alerts
- "Get alert details?" -> GET /repos/{owner}/{repo}/secret-scanning/alerts/{alert_number}
- "Partially update a alert?" -> PATCH /repos/{owner}/{repo}/secret-scanning/alerts/{alert_number}
- "List all locations?" -> GET /repos/{owner}/{repo}/secret-scanning/alerts/{alert_number}/locations
- "Create a push-protection-bypass?" -> POST /repos/{owner}/{repo}/secret-scanning/push-protection-bypasses
- "List all scan-history?" -> GET /repos/{owner}/{repo}/secret-scanning/scan-history
- "List all security-advisories?" -> GET /repos/{owner}/{repo}/security-advisories
- "Create a security-advisory?" -> POST /repos/{owner}/{repo}/security-advisories
- "Create a report?" -> POST /repos/{owner}/{repo}/security-advisories/reports
- "Get security-advisory details?" -> GET /repos/{owner}/{repo}/security-advisories/{ghsa_id}
- "Partially update a security-advisory?" -> PATCH /repos/{owner}/{repo}/security-advisories/{ghsa_id}
- "Create a cve?" -> POST /repos/{owner}/{repo}/security-advisories/{ghsa_id}/cve
- "Create a fork?" -> POST /repos/{owner}/{repo}/security-advisories/{ghsa_id}/forks
- "List all stargazers?" -> GET /repos/{owner}/{repo}/stargazers
- "List all code_frequency?" -> GET /repos/{owner}/{repo}/stats/code_frequency
- "List all commit_activity?" -> GET /repos/{owner}/{repo}/stats/commit_activity
- "List all contributors?" -> GET /repos/{owner}/{repo}/stats/contributors
- "List all participation?" -> GET /repos/{owner}/{repo}/stats/participation
- "List all punch_card?" -> GET /repos/{owner}/{repo}/stats/punch_card
- "List all subscribers?" -> GET /repos/{owner}/{repo}/subscribers
- "List all subscription?" -> GET /repos/{owner}/{repo}/subscription
- "List all tags?" -> GET /repos/{owner}/{repo}/tags
- "Get tarball details?" -> GET /repos/{owner}/{repo}/tarball/{ref}
- "List all teams?" -> GET /repos/{owner}/{repo}/teams
- "List all topics?" -> GET /repos/{owner}/{repo}/topics
- "List all clones?" -> GET /repos/{owner}/{repo}/traffic/clones
- "List all paths?" -> GET /repos/{owner}/{repo}/traffic/popular/paths
- "List all referrers?" -> GET /repos/{owner}/{repo}/traffic/popular/referrers
- "List all views?" -> GET /repos/{owner}/{repo}/traffic/views
- "Create a transfer?" -> POST /repos/{owner}/{repo}/transfer
- "List all vulnerability-alerts?" -> GET /repos/{owner}/{repo}/vulnerability-alerts
- "Get zipball details?" -> GET /repos/{owner}/{repo}/zipball/{ref}
- "Create a generate?" -> POST /repos/{template_owner}/{template_repo}/generate
- "List all repositories?" -> GET /repositories
- "Search code?" -> GET /search/code
- "Search commits?" -> GET /search/commits
- "Search issues?" -> GET /search/issues
- "Search labels?" -> GET /search/labels
- "Search repositories?" -> GET /search/repositories
- "Search topics?" -> GET /search/topics
- "Search users?" -> GET /search/users
- "Get team details?" -> GET /teams/{team_id}
- "Partially update a team?" -> PATCH /teams/{team_id}
- "Delete a team?" -> DELETE /teams/{team_id}
- "List all invitations?" -> GET /teams/{team_id}/invitations
- "List all members?" -> GET /teams/{team_id}/members
- "Get member details?" -> GET /teams/{team_id}/members/{username}
- "Update a member?" -> PUT /teams/{team_id}/members/{username}
- "Delete a member?" -> DELETE /teams/{team_id}/members/{username}
- "Get membership details?" -> GET /teams/{team_id}/memberships/{username}
- "Update a membership?" -> PUT /teams/{team_id}/memberships/{username}
- "Delete a membership?" -> DELETE /teams/{team_id}/memberships/{username}
- "List all repos?" -> GET /teams/{team_id}/repos
- "Get repo details?" -> GET /teams/{team_id}/repos/{owner}/{repo}
- "Update a repo?" -> PUT /teams/{team_id}/repos/{owner}/{repo}
- "Delete a repo?" -> DELETE /teams/{team_id}/repos/{owner}/{repo}
- "List all teams?" -> GET /teams/{team_id}/teams
- "List all user?" -> GET /user
- "List all blocks?" -> GET /user/blocks
- "Get block details?" -> GET /user/blocks/{username}
- "Update a block?" -> PUT /user/blocks/{username}
- "Delete a block?" -> DELETE /user/blocks/{username}
- "List all codespaces?" -> GET /user/codespaces
- "Create a codespace?" -> POST /user/codespaces
- "List all secrets?" -> GET /user/codespaces/secrets
- "List all public-key?" -> GET /user/codespaces/secrets/public-key
- "Get secret details?" -> GET /user/codespaces/secrets/{secret_name}
- "Update a secret?" -> PUT /user/codespaces/secrets/{secret_name}
- "Delete a secret?" -> DELETE /user/codespaces/secrets/{secret_name}
- "List all repositories?" -> GET /user/codespaces/secrets/{secret_name}/repositories
- "Update a repository?" -> PUT /user/codespaces/secrets/{secret_name}/repositories/{repository_id}
- "Delete a repository?" -> DELETE /user/codespaces/secrets/{secret_name}/repositories/{repository_id}
- "Get codespace details?" -> GET /user/codespaces/{codespace_name}
- "Partially update a codespace?" -> PATCH /user/codespaces/{codespace_name}
- "Delete a codespace?" -> DELETE /user/codespaces/{codespace_name}
- "Create a export?" -> POST /user/codespaces/{codespace_name}/exports
- "Get export details?" -> GET /user/codespaces/{codespace_name}/exports/{export_id}
- "List all machines?" -> GET /user/codespaces/{codespace_name}/machines
- "Create a publish?" -> POST /user/codespaces/{codespace_name}/publish
- "Create a start?" -> POST /user/codespaces/{codespace_name}/start
- "Create a stop?" -> POST /user/codespaces/{codespace_name}/stop
- "List all conflicts?" -> GET /user/docker/conflicts
- "List all emails?" -> GET /user/emails
- "Create a email?" -> POST /user/emails
- "List all followers?" -> GET /user/followers
- "List all following?" -> GET /user/following
- "Get following details?" -> GET /user/following/{username}
- "Update a following?" -> PUT /user/following/{username}
- "Delete a following?" -> DELETE /user/following/{username}
- "List all gpg_keys?" -> GET /user/gpg_keys
- "Create a gpg_key?" -> POST /user/gpg_keys
- "Get gpg_key details?" -> GET /user/gpg_keys/{gpg_key_id}
- "Delete a gpg_key?" -> DELETE /user/gpg_keys/{gpg_key_id}
- "List all installations?" -> GET /user/installations
- "List all repositories?" -> GET /user/installations/{installation_id}/repositories
- "Update a repository?" -> PUT /user/installations/{installation_id}/repositories/{repository_id}
- "Delete a repository?" -> DELETE /user/installations/{installation_id}/repositories/{repository_id}
- "List all interaction-limits?" -> GET /user/interaction-limits
- "List all issues?" -> GET /user/issues
- "List all keys?" -> GET /user/keys
- "Create a key?" -> POST /user/keys
- "Get key details?" -> GET /user/keys/{key_id}
- "Delete a key?" -> DELETE /user/keys/{key_id}
- "List all marketplace_purchases?" -> GET /user/marketplace_purchases
- "List all stubbed?" -> GET /user/marketplace_purchases/stubbed
- "List all orgs?" -> GET /user/memberships/orgs
- "Get org details?" -> GET /user/memberships/orgs/{org}
- "Partially update a org?" -> PATCH /user/memberships/orgs/{org}
- "List all migrations?" -> GET /user/migrations
- "Create a migration?" -> POST /user/migrations
- "Get migration details?" -> GET /user/migrations/{migration_id}
- "List all archive?" -> GET /user/migrations/{migration_id}/archive
- "List all repositories?" -> GET /user/migrations/{migration_id}/repositories
- "List all orgs?" -> GET /user/orgs
- "List all packages?" -> GET /user/packages
- "Get package details?" -> GET /user/packages/{package_type}/{package_name}
- "Delete a package?" -> DELETE /user/packages/{package_type}/{package_name}
- "Create a restore?" -> POST /user/packages/{package_type}/{package_name}/restore
- "List all versions?" -> GET /user/packages/{package_type}/{package_name}/versions
- "Get version details?" -> GET /user/packages/{package_type}/{package_name}/versions/{package_version_id}
- "Delete a version?" -> DELETE /user/packages/{package_type}/{package_name}/versions/{package_version_id}
- "Create a restore?" -> POST /user/packages/{package_type}/{package_name}/versions/{package_version_id}/restore
- "List all public_emails?" -> GET /user/public_emails
- "List all repos?" -> GET /user/repos
- "Create a repo?" -> POST /user/repos
- "List all repository_invitations?" -> GET /user/repository_invitations
- "Partially update a repository_invitation?" -> PATCH /user/repository_invitations/{invitation_id}
- "Delete a repository_invitation?" -> DELETE /user/repository_invitations/{invitation_id}
- "List all social_accounts?" -> GET /user/social_accounts
- "Create a social_account?" -> POST /user/social_accounts
- "List all ssh_signing_keys?" -> GET /user/ssh_signing_keys
- "Create a ssh_signing_key?" -> POST /user/ssh_signing_keys
- "Get ssh_signing_key details?" -> GET /user/ssh_signing_keys/{ssh_signing_key_id}
- "Delete a ssh_signing_key?" -> DELETE /user/ssh_signing_keys/{ssh_signing_key_id}
- "List all starred?" -> GET /user/starred
- "Get starred details?" -> GET /user/starred/{owner}/{repo}
- "Update a starred?" -> PUT /user/starred/{owner}/{repo}
- "Delete a starred?" -> DELETE /user/starred/{owner}/{repo}
- "List all subscriptions?" -> GET /user/subscriptions
- "List all teams?" -> GET /user/teams
- "Get user details?" -> GET /user/{account_id}
- "Create a draft?" -> POST /user/{user_id}/projectsV2/{project_number}/drafts
- "List all users?" -> GET /users
- "Create a view?" -> POST /users/{user_id}/projectsV2/{project_number}/views
- "Get user details?" -> GET /users/{username}
- "Create a bulk-list?" -> POST /users/{username}/attestations/bulk-list
- "Create a delete-request?" -> POST /users/{username}/attestations/delete-request
- "Delete a digest?" -> DELETE /users/{username}/attestations/digest/{subject_digest}
- "Delete a attestation?" -> DELETE /users/{username}/attestations/{attestation_id}
- "Get attestation details?" -> GET /users/{username}/attestations/{subject_digest}
- "List all conflicts?" -> GET /users/{username}/docker/conflicts
- "List all events?" -> GET /users/{username}/events
- "Get org details?" -> GET /users/{username}/events/orgs/{org}
- "List all public?" -> GET /users/{username}/events/public
- "List all followers?" -> GET /users/{username}/followers
- "List all following?" -> GET /users/{username}/following
- "Get following details?" -> GET /users/{username}/following/{target_user}
- "List all gists?" -> GET /users/{username}/gists
- "List all gpg_keys?" -> GET /users/{username}/gpg_keys
- "List all hovercard?" -> GET /users/{username}/hovercard
- "List all installation?" -> GET /users/{username}/installation
- "List all keys?" -> GET /users/{username}/keys
- "List all orgs?" -> GET /users/{username}/orgs
- "List all packages?" -> GET /users/{username}/packages
- "Get package details?" -> GET /users/{username}/packages/{package_type}/{package_name}
- "Delete a package?" -> DELETE /users/{username}/packages/{package_type}/{package_name}
- "Create a restore?" -> POST /users/{username}/packages/{package_type}/{package_name}/restore
- "List all versions?" -> GET /users/{username}/packages/{package_type}/{package_name}/versions
- "Get version details?" -> GET /users/{username}/packages/{package_type}/{package_name}/versions/{package_version_id}
- "Delete a version?" -> DELETE /users/{username}/packages/{package_type}/{package_name}/versions/{package_version_id}
- "Create a restore?" -> POST /users/{username}/packages/{package_type}/{package_name}/versions/{package_version_id}/restore
- "Search projectsV2?" -> GET /users/{username}/projectsV2
- "Get projectsV2 details?" -> GET /users/{username}/projectsV2/{project_number}
- "List all fields?" -> GET /users/{username}/projectsV2/{project_number}/fields
- "Create a field?" -> POST /users/{username}/projectsV2/{project_number}/fields
- "Get field details?" -> GET /users/{username}/projectsV2/{project_number}/fields/{field_id}
- "Search items?" -> GET /users/{username}/projectsV2/{project_number}/items
- "Create a item?" -> POST /users/{username}/projectsV2/{project_number}/items
- "Get item details?" -> GET /users/{username}/projectsV2/{project_number}/items/{item_id}
- "Partially update a item?" -> PATCH /users/{username}/projectsV2/{project_number}/items/{item_id}
- "Delete a item?" -> DELETE /users/{username}/projectsV2/{project_number}/items/{item_id}
- "List all items?" -> GET /users/{username}/projectsV2/{project_number}/views/{view_number}/items
- "List all received_events?" -> GET /users/{username}/received_events
- "List all public?" -> GET /users/{username}/received_events/public
- "List all repos?" -> GET /users/{username}/repos
- "List all usage?" -> GET /users/{username}/settings/billing/premium_request/usage
- "List all usage?" -> GET /users/{username}/settings/billing/usage
- "List all summary?" -> GET /users/{username}/settings/billing/usage/summary
- "List all social_accounts?" -> GET /users/{username}/social_accounts
- "List all ssh_signing_keys?" -> GET /users/{username}/ssh_signing_keys
- "List all starred?" -> GET /users/{username}/starred
- "List all subscriptions?" -> GET /users/{username}/subscriptions
- "List all versions?" -> GET /versions
- "List all zen?" -> GET /zen
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
