---
name: launchdarkly-rest-api
description: "LaunchDarkly REST API skill. Use when working with LaunchDarkly REST for api. Covers 349 endpoints."
version: 1.0.0
generator: lapsh
---

# LaunchDarkly REST API
API version: 2.0

## Auth
ApiKey Authorization in header

## Base URL
https://app.launchdarkly.com

## Setup
1. Set your API key in the appropriate header
2. GET /api/v2 -- verify access
3. POST /api/v2/account/relay-auto-configs -- create first relay-auto-configs

## Endpoints

349 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/v2 | Root resource |
| GET | /api/v2/account/relay-auto-configs | List Relay Proxy configs |
| POST | /api/v2/account/relay-auto-configs | Create a new Relay Proxy config |
| GET | /api/v2/account/relay-auto-configs/{id} | Get Relay Proxy config |
| PATCH | /api/v2/account/relay-auto-configs/{id} | Update a Relay Proxy config |
| DELETE | /api/v2/account/relay-auto-configs/{id} | Delete Relay Proxy config by ID |
| POST | /api/v2/account/relay-auto-configs/{id}/reset | Reset Relay Proxy configuration key |
| GET | /api/v2/applications | Get applications |
| GET | /api/v2/applications/{applicationKey} | Get application by key |
| PATCH | /api/v2/applications/{applicationKey} | Update application |
| DELETE | /api/v2/applications/{applicationKey} | Delete application |
| GET | /api/v2/applications/{applicationKey}/versions | Get application versions by application key |
| PATCH | /api/v2/applications/{applicationKey}/versions/{versionKey} | Update application version |
| DELETE | /api/v2/applications/{applicationKey}/versions/{versionKey} | Delete application version |
| GET | /api/v2/approval-requests | List approval requests |
| POST | /api/v2/approval-requests | Create approval request |
| GET | /api/v2/approval-requests/{id} | Get approval request |
| PATCH | /api/v2/approval-requests/{id} | Update approval request |
| DELETE | /api/v2/approval-requests/{id} | Delete approval request |
| POST | /api/v2/approval-requests/{id}/apply | Apply approval request |
| POST | /api/v2/approval-requests/{id}/reviews | Review approval request |
| GET | /api/v2/auditlog | List audit log entries |
| POST | /api/v2/auditlog | Search audit log entries |
| POST | /api/v2/auditlog/counts | Get audit log entry counts |
| GET | /api/v2/auditlog/{id} | Get audit log entry |
| GET | /api/v2/caller-identity | Identify the caller |
| GET | /api/v2/code-refs/extinctions | List extinctions |
| GET | /api/v2/code-refs/repositories | List repositories |
| POST | /api/v2/code-refs/repositories | Create repository |
| GET | /api/v2/code-refs/repositories/{repo} | Get repository |
| PATCH | /api/v2/code-refs/repositories/{repo} | Update repository |
| DELETE | /api/v2/code-refs/repositories/{repo} | Delete repository |
| POST | /api/v2/code-refs/repositories/{repo}/branch-delete-tasks | Delete branches |
| GET | /api/v2/code-refs/repositories/{repo}/branches | List branches |
| GET | /api/v2/code-refs/repositories/{repo}/branches/{branch} | Get branch |
| PUT | /api/v2/code-refs/repositories/{repo}/branches/{branch} | Upsert branch |
| POST | /api/v2/code-refs/repositories/{repo}/branches/{branch}/extinction-events | Create extinction |
| GET | /api/v2/code-refs/statistics | Get links to code reference repositories for each project |
| GET | /api/v2/code-refs/statistics/{projectKey} | Get code references statistics for flags |
| GET | /api/v2/destinations | List destinations |
| POST | /api/v2/destinations/generate-warehouse-destination-key-pair | Generate Snowflake destination key pair |
| POST | /api/v2/destinations/projects/{projKey}/environments/{envKey}/generate-trust-policy | Generate trust policy |
| POST | /api/v2/destinations/{projectKey}/{environmentKey} | Create Data Export destination |
| GET | /api/v2/destinations/{projectKey}/{environmentKey}/{id} | Get destination |
| PATCH | /api/v2/destinations/{projectKey}/{environmentKey}/{id} | Update Data Export destination |
| DELETE | /api/v2/destinations/{projectKey}/{environmentKey}/{id} | Delete Data Export destination |
| GET | /api/v2/flag-links/projects/{projectKey}/flags/{featureFlagKey} | List flag links |
| POST | /api/v2/flag-links/projects/{projectKey}/flags/{featureFlagKey} | Create flag link |
| PATCH | /api/v2/flag-links/projects/{projectKey}/flags/{featureFlagKey}/{id} | Update flag link |
| DELETE | /api/v2/flag-links/projects/{projectKey}/flags/{featureFlagKey}/{id} | Delete flag link |
| GET | /api/v2/flag-status/{projectKey}/{featureFlagKey} | Get flag status across environments |
| GET | /api/v2/flag-statuses/{projectKey}/{environmentKey} | List feature flag statuses |
| GET | /api/v2/flag-statuses/{projectKey}/{environmentKey}/{featureFlagKey} | Get feature flag status |
| GET | /api/v2/flags/{projectKey} | List feature flags |
| POST | /api/v2/flags/{projectKey} | Create a feature flag |
| GET | /api/v2/flags/{projectKey}/{environmentKey}/{featureFlagKey}/dependent-flags | List dependent feature flags by environment |
| GET | /api/v2/flags/{projectKey}/{featureFlagKey} | Get feature flag |
| PATCH | /api/v2/flags/{projectKey}/{featureFlagKey} | Update feature flag |
| DELETE | /api/v2/flags/{projectKey}/{featureFlagKey} | Delete feature flag |
| POST | /api/v2/flags/{projectKey}/{featureFlagKey}/copy | Copy feature flag |
| GET | /api/v2/flags/{projectKey}/{featureFlagKey}/dependent-flags | List dependent feature flags |
| GET | /api/v2/flags/{projectKey}/{featureFlagKey}/expiring-targets/{environmentKey} | Get expiring context targets for feature flag |
| PATCH | /api/v2/flags/{projectKey}/{featureFlagKey}/expiring-targets/{environmentKey} | Update expiring context targets on feature flag |
| GET | /api/v2/flags/{projectKey}/{featureFlagKey}/expiring-user-targets/{environmentKey} | Get expiring user targets for feature flag |
| PATCH | /api/v2/flags/{projectKey}/{featureFlagKey}/expiring-user-targets/{environmentKey} | Update expiring user targets on feature flag |
| GET | /api/v2/flags/{projectKey}/{featureFlagKey}/triggers/{environmentKey} | List flag triggers |
| POST | /api/v2/flags/{projectKey}/{featureFlagKey}/triggers/{environmentKey} | Create flag trigger |
| GET | /api/v2/flags/{projectKey}/{featureFlagKey}/triggers/{environmentKey}/{id} | Get flag trigger by ID |
| PATCH | /api/v2/flags/{projectKey}/{featureFlagKey}/triggers/{environmentKey}/{id} | Update flag trigger |
| DELETE | /api/v2/flags/{projectKey}/{featureFlagKey}/triggers/{environmentKey}/{id} | Delete flag trigger |
| GET | /api/v2/flags/{projectKey}/{flagKey}/release | Get release for flag |
| PATCH | /api/v2/flags/{projectKey}/{flagKey}/release | Patch release for flag |
| DELETE | /api/v2/flags/{projectKey}/{flagKey}/release | Delete a release for flag |
| GET | /api/v2/integration-capabilities/big-segment-store | List all big segment store integrations |
| POST | /api/v2/integration-capabilities/big-segment-store/{projectKey}/{environmentKey}/{integrationKey} | Create big segment store integration |
| GET | /api/v2/integration-capabilities/big-segment-store/{projectKey}/{environmentKey}/{integrationKey}/{integrationId} | Get big segment store integration by ID |
| PATCH | /api/v2/integration-capabilities/big-segment-store/{projectKey}/{environmentKey}/{integrationKey}/{integrationId} | Update big segment store integration |
| DELETE | /api/v2/integration-capabilities/big-segment-store/{projectKey}/{environmentKey}/{integrationKey}/{integrationId} | Delete big segment store integration |
| GET | /api/v2/integration-capabilities/featureStore | List all delivery configurations |
| GET | /api/v2/integration-capabilities/featureStore/{projectKey}/{environmentKey} | Get delivery configurations by environment |
| POST | /api/v2/integration-capabilities/featureStore/{projectKey}/{environmentKey}/{integrationKey} | Create delivery configuration |
| GET | /api/v2/integration-capabilities/featureStore/{projectKey}/{environmentKey}/{integrationKey}/{id} | Get delivery configuration by ID |
| PATCH | /api/v2/integration-capabilities/featureStore/{projectKey}/{environmentKey}/{integrationKey}/{id} | Update delivery configuration |
| DELETE | /api/v2/integration-capabilities/featureStore/{projectKey}/{environmentKey}/{integrationKey}/{id} | Delete delivery configuration |
| POST | /api/v2/integration-capabilities/featureStore/{projectKey}/{environmentKey}/{integrationKey}/{id}/validate | Validate delivery configuration |
| GET | /api/v2/integration-capabilities/flag-import | List all flag import configurations |
| POST | /api/v2/integration-capabilities/flag-import/{projectKey}/{integrationKey} | Create a flag import configuration |
| GET | /api/v2/integration-capabilities/flag-import/{projectKey}/{integrationKey}/{integrationId} | Get a single flag import configuration |
| PATCH | /api/v2/integration-capabilities/flag-import/{projectKey}/{integrationKey}/{integrationId} | Update a flag import configuration |
| DELETE | /api/v2/integration-capabilities/flag-import/{projectKey}/{integrationKey}/{integrationId} | Delete a flag import configuration |
| POST | /api/v2/integration-capabilities/flag-import/{projectKey}/{integrationKey}/{integrationId}/trigger | Trigger a single flag import run |
| GET | /api/v2/integration-configurations/keys/{integrationKey} | Get all configurations for the integration |
| POST | /api/v2/integration-configurations/keys/{integrationKey} | Create integration configuration |
| GET | /api/v2/integration-configurations/{integrationConfigurationId} | Get an integration configuration |
| PATCH | /api/v2/integration-configurations/{integrationConfigurationId} | Update integration configuration |
| DELETE | /api/v2/integration-configurations/{integrationConfigurationId} | Delete integration configuration |
| GET | /api/v2/integrations/{integrationKey} | Get audit log subscriptions by integration |
| POST | /api/v2/integrations/{integrationKey} | Create audit log subscription |
| GET | /api/v2/integrations/{integrationKey}/{id} | Get audit log subscription by ID |
| PATCH | /api/v2/integrations/{integrationKey}/{id} | Update audit log subscription |
| DELETE | /api/v2/integrations/{integrationKey}/{id} | Delete audit log subscription |
| GET | /api/v2/members | List account members |
| POST | /api/v2/members | Invite new members |
| PATCH | /api/v2/members | Modify account members |
| GET | /api/v2/members/{id} | Get account member |
| PATCH | /api/v2/members/{id} | Modify an account member |
| DELETE | /api/v2/members/{id} | Delete account member |
| POST | /api/v2/members/{id}/teams | Add a member to teams |
| GET | /api/v2/metrics/{projectKey} | List metrics |
| POST | /api/v2/metrics/{projectKey} | Create metric |
| GET | /api/v2/metrics/{projectKey}/{metricKey} | Get metric |
| PATCH | /api/v2/metrics/{projectKey}/{metricKey} | Update metric |
| DELETE | /api/v2/metrics/{projectKey}/{metricKey} | Delete metric |
| GET | /api/v2/oauth/clients | Get clients |
| POST | /api/v2/oauth/clients | Create a LaunchDarkly OAuth 2.0 client |
| GET | /api/v2/oauth/clients/{clientId} | Get client by ID |
| PATCH | /api/v2/oauth/clients/{clientId} | Patch client by ID |
| DELETE | /api/v2/oauth/clients/{clientId} | Delete OAuth 2.0 client |
| GET | /api/v2/openapi.json | Gets the OpenAPI spec in json |
| GET | /api/v2/projects | List projects |
| POST | /api/v2/projects | Create project |
| GET | /api/v2/projects/{projectKey} | Get project |
| PATCH | /api/v2/projects/{projectKey} | Update project |
| DELETE | /api/v2/projects/{projectKey} | Delete project |
| GET | /api/v2/projects/{projectKey}/context-kinds | Get context kinds |
| PUT | /api/v2/projects/{projectKey}/context-kinds/{key} | Create or update context kind |
| GET | /api/v2/projects/{projectKey}/environments | List environments |
| POST | /api/v2/projects/{projectKey}/environments | Create environment |
| GET | /api/v2/projects/{projectKey}/environments/{environmentKey} | Get environment |
| PATCH | /api/v2/projects/{projectKey}/environments/{environmentKey} | Update environment |
| DELETE | /api/v2/projects/{projectKey}/environments/{environmentKey} | Delete environment |
| POST | /api/v2/projects/{projectKey}/environments/{environmentKey}/apiKey | Reset environment SDK key |
| GET | /api/v2/projects/{projectKey}/environments/{environmentKey}/context-attributes | Get context attribute names |
| GET | /api/v2/projects/{projectKey}/environments/{environmentKey}/context-attributes/{attributeName} | Get context attribute values |
| POST | /api/v2/projects/{projectKey}/environments/{environmentKey}/context-instances/search | Search for context instances |
| GET | /api/v2/projects/{projectKey}/environments/{environmentKey}/context-instances/{id} | Get context instances |
| DELETE | /api/v2/projects/{projectKey}/environments/{environmentKey}/context-instances/{id} | Delete context instances |
| POST | /api/v2/projects/{projectKey}/environments/{environmentKey}/contexts/search | Search for contexts |
| PUT | /api/v2/projects/{projectKey}/environments/{environmentKey}/contexts/{contextKind}/{contextKey}/flags/{featureFlagKey} | Update flag settings for context |
| GET | /api/v2/projects/{projectKey}/environments/{environmentKey}/contexts/{kind}/{key} | Get contexts |
| GET | /api/v2/projects/{projectKey}/environments/{environmentKey}/experiments | Get experiments |
| POST | /api/v2/projects/{projectKey}/environments/{environmentKey}/experiments | Create experiment |
| GET | /api/v2/projects/{projectKey}/environments/{environmentKey}/experiments/{experimentKey} | Get experiment |
| PATCH | /api/v2/projects/{projectKey}/environments/{environmentKey}/experiments/{experimentKey} | Patch experiment |
| POST | /api/v2/projects/{projectKey}/environments/{environmentKey}/experiments/{experimentKey}/iterations | Create iteration |
| POST | /api/v2/projects/{projectKey}/environments/{environmentKey}/flags/evaluate | Evaluate flags for context instance |
| GET | /api/v2/projects/{projectKey}/environments/{environmentKey}/followers | Get followers of all flags in a given project and environment |
| GET | /api/v2/projects/{projectKey}/environments/{environmentKey}/holdouts | Get all holdouts |
| POST | /api/v2/projects/{projectKey}/environments/{environmentKey}/holdouts | Create holdout |
| GET | /api/v2/projects/{projectKey}/environments/{environmentKey}/holdouts/id/{holdoutId} | Get Holdout by Id |
| GET | /api/v2/projects/{projectKey}/environments/{environmentKey}/holdouts/{holdoutKey} | Get holdout |
| PATCH | /api/v2/projects/{projectKey}/environments/{environmentKey}/holdouts/{holdoutKey} | Patch holdout |
| POST | /api/v2/projects/{projectKey}/environments/{environmentKey}/mobileKey | Reset environment mobile SDK key |
| POST | /api/v2/projects/{projectKey}/environments/{environmentKey}/segments/evaluate | List segment memberships for context instance |
| GET | /api/v2/projects/{projectKey}/experimentation-settings | Get experimentation settings |
| PUT | /api/v2/projects/{projectKey}/experimentation-settings | Update experimentation settings |
| GET | /api/v2/projects/{projectKey}/flag-defaults | Get flag defaults for project |
| PATCH | /api/v2/projects/{projectKey}/flag-defaults | Update flag default for project |
| PUT | /api/v2/projects/{projectKey}/flag-defaults | Create or update flag defaults for project |
| GET | /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests | List approval requests for a flag |
| POST | /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests | Create approval request for a flag |
| POST | /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests-flag-copy | Create approval request to copy flag configurations across environments |
| GET | /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests/{id} | Get approval request for a flag |
| PATCH | /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests/{id} | Update flag approval request |
| DELETE | /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests/{id} | Delete approval request for a flag |
| POST | /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests/{id}/apply | Apply approval request for a flag |
| POST | /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests/{id}/reviews | Review approval request for a flag |
| GET | /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/followers | Get followers of a flag in a project and environment |
| PUT | /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/followers/{memberId} | Add a member as a follower of a flag in a project and environment |
| DELETE | /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/followers/{memberId} | Remove a member as a follower of a flag in a project and environment |
| GET | /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/scheduled-changes | List scheduled changes |
| POST | /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/scheduled-changes | Create scheduled changes workflow |
| GET | /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/scheduled-changes/{id} | Get a scheduled change |
| PATCH | /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/scheduled-changes/{id} | Update scheduled changes workflow |
| DELETE | /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/scheduled-changes/{id} | Delete scheduled changes workflow |
| GET | /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/workflows | Get workflows |
| POST | /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/workflows | Create workflow |
| GET | /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/workflows/{workflowId} | Get custom workflow |
| DELETE | /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/workflows/{workflowId} | Delete workflow |
| POST | /api/v2/projects/{projectKey}/flags/{flagKey}/environments/{environmentKey}/migration-safety-issues | Get migration safety issues |
| PUT | /api/v2/projects/{projectKey}/flags/{flagKey}/release | Create a new release for flag |
| PUT | /api/v2/projects/{projectKey}/flags/{flagKey}/release/phases/{phaseId} | Update phase status for release |
| GET | /api/v2/projects/{projectKey}/layers | Get layers |
| POST | /api/v2/projects/{projectKey}/layers | Create layer |
| PATCH | /api/v2/projects/{projectKey}/layers/{layerKey} | Update layer |
| GET | /api/v2/projects/{projectKey}/metric-groups | List metric groups |
| POST | /api/v2/projects/{projectKey}/metric-groups | Create metric group |
| GET | /api/v2/projects/{projectKey}/metric-groups/{metricGroupKey} | Get metric group |
| PATCH | /api/v2/projects/{projectKey}/metric-groups/{metricGroupKey} | Patch metric group |
| DELETE | /api/v2/projects/{projectKey}/metric-groups/{metricGroupKey} | Delete metric group |
| GET | /api/v2/projects/{projectKey}/release-pipelines | Get all release pipelines |
| POST | /api/v2/projects/{projectKey}/release-pipelines | Create a release pipeline |
| GET | /api/v2/projects/{projectKey}/release-pipelines/{pipelineKey} | Get release pipeline by key |
| PUT | /api/v2/projects/{projectKey}/release-pipelines/{pipelineKey} | Update a release pipeline |
| DELETE | /api/v2/projects/{projectKey}/release-pipelines/{pipelineKey} | Delete release pipeline |
| GET | /api/v2/projects/{projectKey}/release-pipelines/{pipelineKey}/releases | Get release progressions for release pipeline |
| GET | /api/v2/public-ip-list | Gets the public IP list |
| GET | /api/v2/roles | List custom roles |
| POST | /api/v2/roles | Create custom role |
| GET | /api/v2/roles/{customRoleKey} | Get custom role |
| PATCH | /api/v2/roles/{customRoleKey} | Update custom role |
| DELETE | /api/v2/roles/{customRoleKey} | Delete custom role |
| GET | /api/v2/segments/{projectKey}/{environmentKey} | List segments |
| POST | /api/v2/segments/{projectKey}/{environmentKey} | Create segment |
| GET | /api/v2/segments/{projectKey}/{environmentKey}/{segmentKey} | Get segment |
| PATCH | /api/v2/segments/{projectKey}/{environmentKey}/{segmentKey} | Patch segment |
| DELETE | /api/v2/segments/{projectKey}/{environmentKey}/{segmentKey} | Delete segment |
| POST | /api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/contexts | Update context targets on a big segment |
| GET | /api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/contexts/{contextKey} | Get big segment membership for context |
| POST | /api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/exports | Create big segment export |
| GET | /api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/exports/{exportID} | Get big segment export |
| POST | /api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/imports | Create big segment import |
| GET | /api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/imports/{importID} | Get big segment import |
| POST | /api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/users | Update user context targets on a big segment |
| GET | /api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/users/{userKey} | Get big segment membership for user |
| GET | /api/v2/segments/{projectKey}/{segmentKey}/expiring-targets/{environmentKey} | Get expiring targets for segment |
| PATCH | /api/v2/segments/{projectKey}/{segmentKey}/expiring-targets/{environmentKey} | Update expiring targets for segment |
| GET | /api/v2/segments/{projectKey}/{segmentKey}/expiring-user-targets/{environmentKey} | Get expiring user targets for segment |
| PATCH | /api/v2/segments/{projectKey}/{segmentKey}/expiring-user-targets/{environmentKey} | Update expiring user targets for segment |
| GET | /api/v2/teams | List teams |
| POST | /api/v2/teams | Create team |
| PATCH | /api/v2/teams | Update teams |
| GET | /api/v2/teams/{teamKey} | Get team |
| PATCH | /api/v2/teams/{teamKey} | Update team |
| DELETE | /api/v2/teams/{teamKey} | Delete team |
| GET | /api/v2/teams/{teamKey}/maintainers | Get team maintainers |
| POST | /api/v2/teams/{teamKey}/members | Add multiple members to team |
| GET | /api/v2/teams/{teamKey}/roles | Get team custom roles |
| GET | /api/v2/templates | Get workflow templates |
| POST | /api/v2/templates | Create workflow template |
| DELETE | /api/v2/templates/{templateKey} | Delete workflow template |
| GET | /api/v2/tokens | List access tokens |
| POST | /api/v2/tokens | Create access token |
| GET | /api/v2/tokens/{id} | Get access token |
| PATCH | /api/v2/tokens/{id} | Patch access token |
| DELETE | /api/v2/tokens/{id} | Delete access token |
| POST | /api/v2/tokens/{id}/reset | Reset access token |
| GET | /api/v2/usage/clientside-contexts | Get contexts clientside usage |
| GET | /api/v2/usage/clientside-mau | Get MAU clientside usage |
| GET | /api/v2/usage/data-export-events | Get data export events usage |
| GET | /api/v2/usage/evaluations/{projectKey}/{environmentKey}/{featureFlagKey} | Get evaluations usage |
| GET | /api/v2/usage/events/{type} | Get events usage |
| GET | /api/v2/usage/experimentation-events | Get experimentation events usage |
| GET | /api/v2/usage/experimentation-keys | Get experimentation keys usage |
| GET | /api/v2/usage/mau | Get MAU usage |
| GET | /api/v2/usage/mau/bycategory | Get MAU usage by category |
| GET | /api/v2/usage/mau/sdks | Get MAU SDKs by type |
| GET | /api/v2/usage/observability/errors | Get observability errors usage |
| GET | /api/v2/usage/observability/logs | Get observability logs usage |
| GET | /api/v2/usage/observability/metrics | Get observability metrics usage |
| GET | /api/v2/usage/observability/sessions | Get observability sessions usage |
| GET | /api/v2/usage/observability/traces | Get observability traces usage |
| GET | /api/v2/usage/sdk-versions/details | Get SDK versions usage details |
| GET | /api/v2/usage/serverside-contexts | Get contexts serverside usage |
| GET | /api/v2/usage/service-connections | Get service connections usage |
| GET | /api/v2/usage/streams/{source} | Get stream usage |
| GET | /api/v2/usage/streams/{source}/bysdkversion | Get stream usage by SDK version |
| GET | /api/v2/usage/streams/{source}/sdkversions | Get stream usage SDK versions |
| GET | /api/v2/usage/total-contexts | Get contexts total usage |
| GET | /api/v2/usage/total-mau | Get MAU total usage |
| GET | /api/v2/usage/vega-ai | Get Vega AI usage |
| GET | /api/v2/user-attributes/{projectKey}/{environmentKey} | Get user attribute names |
| GET | /api/v2/user-search/{projectKey}/{environmentKey} | Find users |
| GET | /api/v2/users/{projectKey}/{environmentKey} | List users |
| GET | /api/v2/users/{projectKey}/{environmentKey}/{userKey} | Get user |
| DELETE | /api/v2/users/{projectKey}/{environmentKey}/{userKey} | Delete user |
| GET | /api/v2/users/{projectKey}/{environmentKey}/{userKey}/flags | List flag settings for user |
| GET | /api/v2/users/{projectKey}/{environmentKey}/{userKey}/flags/{featureFlagKey} | Get flag setting for user |
| PUT | /api/v2/users/{projectKey}/{environmentKey}/{userKey}/flags/{featureFlagKey} | Update flag settings for user |
| GET | /api/v2/users/{projectKey}/{userKey}/expiring-user-targets/{environmentKey} | Get expiring dates on flags for user |
| PATCH | /api/v2/users/{projectKey}/{userKey}/expiring-user-targets/{environmentKey} | Update expiring user target for flags |
| GET | /api/v2/versions | Get version information |
| GET | /api/v2/webhooks | List webhooks |
| POST | /api/v2/webhooks | Creates a webhook |
| GET | /api/v2/webhooks/{id} | Get webhook |
| PATCH | /api/v2/webhooks/{id} | Update webhook |
| DELETE | /api/v2/webhooks/{id} | Delete webhook |
| GET | /api/v2/tags | List tags |
| GET | /api/v2/projects/{projectKey}/ai-configs/{configKey}/targeting | Show an AI Config's targeting |
| PATCH | /api/v2/projects/{projectKey}/ai-configs/{configKey}/targeting | Update AI Config targeting |
| GET | /api/v2/projects/{projectKey}/ai-configs | List AI Configs |
| POST | /api/v2/projects/{projectKey}/ai-configs | Create new AI Config |
| DELETE | /api/v2/projects/{projectKey}/ai-configs/{configKey} | Delete AI Config |
| GET | /api/v2/projects/{projectKey}/ai-configs/{configKey} | Get AI Config |
| PATCH | /api/v2/projects/{projectKey}/ai-configs/{configKey} | Update AI Config |
| POST | /api/v2/projects/{projectKey}/ai-configs/{configKey}/variations | Create AI Config variation |
| DELETE | /api/v2/projects/{projectKey}/ai-configs/{configKey}/variations/{variationKey} | Delete AI Config variation |
| GET | /api/v2/projects/{projectKey}/ai-configs/{configKey}/variations/{variationKey} | Get AI Config variation |
| PATCH | /api/v2/projects/{projectKey}/ai-configs/{configKey}/variations/{variationKey} | Update AI Config variation |
| GET | /api/v2/projects/{projectKey}/ai-configs/{configKey}/metrics | Get AI Config metrics |
| GET | /api/v2/projects/{projectKey}/ai-configs/{configKey}/metrics-by-variation | Get AI Config metrics by variation |
| DELETE | /api/v2/projects/{projectKey}/ai-configs/model-configs/restricted | Remove AI models from the restricted list |
| POST | /api/v2/projects/{projectKey}/ai-configs/model-configs/restricted | Add AI models to the restricted list |
| GET | /api/v2/projects/{projectKey}/ai-configs/model-configs | List AI model configs |
| POST | /api/v2/projects/{projectKey}/ai-configs/model-configs | Create an AI model config |
| DELETE | /api/v2/projects/{projectKey}/ai-configs/model-configs/{modelConfigKey} | Delete an AI model config |
| GET | /api/v2/projects/{projectKey}/ai-configs/model-configs/{modelConfigKey} | Get AI model config |
| GET | /api/v2/projects/{projectKey}/ai-tools | List AI tools |
| POST | /api/v2/projects/{projectKey}/ai-tools | Create an AI tool |
| GET | /api/v2/projects/{projectKey}/ai-tools/{toolKey}/versions | List AI tool versions |
| DELETE | /api/v2/projects/{projectKey}/ai-tools/{toolKey} | Delete AI tool |
| GET | /api/v2/projects/{projectKey}/ai-tools/{toolKey} | Get AI tool |
| PATCH | /api/v2/projects/{projectKey}/ai-tools/{toolKey} | Update AI tool |
| GET | /api/v2/projects/{projectKey}/agent-graphs | List agent graphs |
| POST | /api/v2/projects/{projectKey}/agent-graphs | Create new agent graph |
| DELETE | /api/v2/projects/{projectKey}/agent-graphs/{graphKey} | Delete agent graph |
| GET | /api/v2/projects/{projectKey}/agent-graphs/{graphKey} | Get agent graph |
| PATCH | /api/v2/projects/{projectKey}/agent-graphs/{graphKey} | Update agent graph |
| GET | /api/v2/announcements | Get announcements |
| POST | /api/v2/announcements | Create an announcement |
| DELETE | /api/v2/announcements/{announcementId} | Delete an announcement |
| PATCH | /api/v2/announcements/{announcementId} | Update an announcement |
| GET | /api/v2/approval-requests/projects/{projectKey}/settings | Get approval request settings |
| PATCH | /api/v2/approval-requests/projects/{projectKey}/settings | Update approval request settings |
| GET | /api/v2/projects/{projectKey}/views | List views |
| POST | /api/v2/projects/{projectKey}/views | Create view |
| DELETE | /api/v2/projects/{projectKey}/views/{viewKey} | Delete view |
| GET | /api/v2/projects/{projectKey}/views/{viewKey} | Get view |
| PATCH | /api/v2/projects/{projectKey}/views/{viewKey} | Update view |
| DELETE | /api/v2/projects/{projectKey}/views/{viewKey}/link/{resourceType} | Unlink resource |
| POST | /api/v2/projects/{projectKey}/views/{viewKey}/link/{resourceType} | Link resource |
| GET | /api/v2/projects/{projectKey}/views/{viewKey}/linked/{resourceType} | Get linked resources |
| GET | /api/v2/projects/{projectKey}/view-associations/{resourceType}/{resourceKey} | Get linked views for a given resource |
| GET | /api/v2/projects/{projectKey}/release-policies | List release policies |
| POST | /api/v2/projects/{projectKey}/release-policies | Create a release policy |
| POST | /api/v2/projects/{projectKey}/release-policies/order | Update the order of existing release policies |
| DELETE | /api/v2/projects/{projectKey}/release-policies/{policyKey} | Delete a release policy |
| GET | /api/v2/projects/{projectKey}/release-policies/{policyKey} | Get a release policy by key |
| PUT | /api/v2/projects/{projectKey}/release-policies/{policyKey} | Update a release policy |
| GET | /api/v2/engineering-insights/charts/deployments/frequency | Get deployment frequency chart data |
| GET | /api/v2/engineering-insights/charts/flags/stale | Get stale flags chart data |
| GET | /api/v2/engineering-insights/charts/flags/status | Get flag status chart data |
| GET | /api/v2/engineering-insights/charts/lead-time | Get lead time chart data |
| GET | /api/v2/engineering-insights/charts/releases/frequency | Get release frequency chart data |
| POST | /api/v2/engineering-insights/deployment-events | Create deployment event |
| GET | /api/v2/engineering-insights/deployments | List deployments |
| GET | /api/v2/engineering-insights/deployments/{deploymentID} | Get deployment |
| PATCH | /api/v2/engineering-insights/deployments/{deploymentID} | Update deployment |
| GET | /api/v2/engineering-insights/flag-events | List flag events |
| POST | /api/v2/engineering-insights/insights/group | Create insight group |
| GET | /api/v2/engineering-insights/insights/groups | List insight groups |
| GET | /api/v2/engineering-insights/insights/groups/{insightGroupKey} | Get insight group |
| PATCH | /api/v2/engineering-insights/insights/groups/{insightGroupKey} | Patch insight group |
| DELETE | /api/v2/engineering-insights/insights/groups/{insightGroupKey} | Delete insight group |
| GET | /api/v2/engineering-insights/insights/scores | Get insight scores |
| GET | /api/v2/engineering-insights/pull-requests | List pull requests |
| GET | /api/v2/engineering-insights/repositories | List repositories |
| PUT | /api/v2/engineering-insights/repositories/projects | Associate repositories with projects |
| DELETE | /api/v2/engineering-insights/repositories/{repositoryKey}/projects/{projectKey} | Remove repository project association |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all api?" -> GET /api/v2
- "List all relay-auto-configs?" -> GET /api/v2/account/relay-auto-configs
- "Create a relay-auto-config?" -> POST /api/v2/account/relay-auto-configs
- "Get relay-auto-config details?" -> GET /api/v2/account/relay-auto-configs/{id}
- "Partially update a relay-auto-config?" -> PATCH /api/v2/account/relay-auto-configs/{id}
- "Delete a relay-auto-config?" -> DELETE /api/v2/account/relay-auto-configs/{id}
- "Create a reset?" -> POST /api/v2/account/relay-auto-configs/{id}/reset
- "List all applications?" -> GET /api/v2/applications
- "Get application details?" -> GET /api/v2/applications/{applicationKey}
- "Partially update a application?" -> PATCH /api/v2/applications/{applicationKey}
- "Delete a application?" -> DELETE /api/v2/applications/{applicationKey}
- "List all versions?" -> GET /api/v2/applications/{applicationKey}/versions
- "Partially update a version?" -> PATCH /api/v2/applications/{applicationKey}/versions/{versionKey}
- "Delete a version?" -> DELETE /api/v2/applications/{applicationKey}/versions/{versionKey}
- "List all approval-requests?" -> GET /api/v2/approval-requests
- "Create a approval-request?" -> POST /api/v2/approval-requests
- "Get approval-request details?" -> GET /api/v2/approval-requests/{id}
- "Partially update a approval-request?" -> PATCH /api/v2/approval-requests/{id}
- "Delete a approval-request?" -> DELETE /api/v2/approval-requests/{id}
- "Create a apply?" -> POST /api/v2/approval-requests/{id}/apply
- "Create a review?" -> POST /api/v2/approval-requests/{id}/reviews
- "Search auditlog?" -> GET /api/v2/auditlog
- "Create a auditlog?" -> POST /api/v2/auditlog
- "Create a count?" -> POST /api/v2/auditlog/counts
- "Get auditlog details?" -> GET /api/v2/auditlog/{id}
- "List all caller-identity?" -> GET /api/v2/caller-identity
- "List all extinctions?" -> GET /api/v2/code-refs/extinctions
- "List all repositories?" -> GET /api/v2/code-refs/repositories
- "Create a repository?" -> POST /api/v2/code-refs/repositories
- "Get repository details?" -> GET /api/v2/code-refs/repositories/{repo}
- "Partially update a repository?" -> PATCH /api/v2/code-refs/repositories/{repo}
- "Delete a repository?" -> DELETE /api/v2/code-refs/repositories/{repo}
- "Create a branch-delete-task?" -> POST /api/v2/code-refs/repositories/{repo}/branch-delete-tasks
- "List all branches?" -> GET /api/v2/code-refs/repositories/{repo}/branches
- "Get branche details?" -> GET /api/v2/code-refs/repositories/{repo}/branches/{branch}
- "Update a branche?" -> PUT /api/v2/code-refs/repositories/{repo}/branches/{branch}
- "Create a extinction-event?" -> POST /api/v2/code-refs/repositories/{repo}/branches/{branch}/extinction-events
- "List all statistics?" -> GET /api/v2/code-refs/statistics
- "Get statistic details?" -> GET /api/v2/code-refs/statistics/{projectKey}
- "List all destinations?" -> GET /api/v2/destinations
- "Create a generate-warehouse-destination-key-pair?" -> POST /api/v2/destinations/generate-warehouse-destination-key-pair
- "Create a generate-trust-policy?" -> POST /api/v2/destinations/projects/{projKey}/environments/{envKey}/generate-trust-policy
- "Get destination details?" -> GET /api/v2/destinations/{projectKey}/{environmentKey}/{id}
- "Partially update a destination?" -> PATCH /api/v2/destinations/{projectKey}/{environmentKey}/{id}
- "Delete a destination?" -> DELETE /api/v2/destinations/{projectKey}/{environmentKey}/{id}
- "Get flag details?" -> GET /api/v2/flag-links/projects/{projectKey}/flags/{featureFlagKey}
- "Partially update a flag?" -> PATCH /api/v2/flag-links/projects/{projectKey}/flags/{featureFlagKey}/{id}
- "Delete a flag?" -> DELETE /api/v2/flag-links/projects/{projectKey}/flags/{featureFlagKey}/{id}
- "Get flag-status details?" -> GET /api/v2/flag-status/{projectKey}/{featureFlagKey}
- "Get flag-statuse details?" -> GET /api/v2/flag-statuses/{projectKey}/{environmentKey}
- "Get flag-statuse details?" -> GET /api/v2/flag-statuses/{projectKey}/{environmentKey}/{featureFlagKey}
- "Get flag details?" -> GET /api/v2/flags/{projectKey}
- "List all dependent-flags?" -> GET /api/v2/flags/{projectKey}/{environmentKey}/{featureFlagKey}/dependent-flags
- "Get flag details?" -> GET /api/v2/flags/{projectKey}/{featureFlagKey}
- "Partially update a flag?" -> PATCH /api/v2/flags/{projectKey}/{featureFlagKey}
- "Delete a flag?" -> DELETE /api/v2/flags/{projectKey}/{featureFlagKey}
- "Create a copy?" -> POST /api/v2/flags/{projectKey}/{featureFlagKey}/copy
- "List all dependent-flags?" -> GET /api/v2/flags/{projectKey}/{featureFlagKey}/dependent-flags
- "Get expiring-target details?" -> GET /api/v2/flags/{projectKey}/{featureFlagKey}/expiring-targets/{environmentKey}
- "Partially update a expiring-target?" -> PATCH /api/v2/flags/{projectKey}/{featureFlagKey}/expiring-targets/{environmentKey}
- "Get expiring-user-target details?" -> GET /api/v2/flags/{projectKey}/{featureFlagKey}/expiring-user-targets/{environmentKey}
- "Partially update a expiring-user-target?" -> PATCH /api/v2/flags/{projectKey}/{featureFlagKey}/expiring-user-targets/{environmentKey}
- "Get trigger details?" -> GET /api/v2/flags/{projectKey}/{featureFlagKey}/triggers/{environmentKey}
- "Get trigger details?" -> GET /api/v2/flags/{projectKey}/{featureFlagKey}/triggers/{environmentKey}/{id}
- "Partially update a trigger?" -> PATCH /api/v2/flags/{projectKey}/{featureFlagKey}/triggers/{environmentKey}/{id}
- "Delete a trigger?" -> DELETE /api/v2/flags/{projectKey}/{featureFlagKey}/triggers/{environmentKey}/{id}
- "List all release?" -> GET /api/v2/flags/{projectKey}/{flagKey}/release
- "List all big-segment-store?" -> GET /api/v2/integration-capabilities/big-segment-store
- "Get big-segment-store details?" -> GET /api/v2/integration-capabilities/big-segment-store/{projectKey}/{environmentKey}/{integrationKey}/{integrationId}
- "Partially update a big-segment-store?" -> PATCH /api/v2/integration-capabilities/big-segment-store/{projectKey}/{environmentKey}/{integrationKey}/{integrationId}
- "Delete a big-segment-store?" -> DELETE /api/v2/integration-capabilities/big-segment-store/{projectKey}/{environmentKey}/{integrationKey}/{integrationId}
- "List all featureStore?" -> GET /api/v2/integration-capabilities/featureStore
- "Get featureStore details?" -> GET /api/v2/integration-capabilities/featureStore/{projectKey}/{environmentKey}
- "Get featureStore details?" -> GET /api/v2/integration-capabilities/featureStore/{projectKey}/{environmentKey}/{integrationKey}/{id}
- "Partially update a featureStore?" -> PATCH /api/v2/integration-capabilities/featureStore/{projectKey}/{environmentKey}/{integrationKey}/{id}
- "Delete a featureStore?" -> DELETE /api/v2/integration-capabilities/featureStore/{projectKey}/{environmentKey}/{integrationKey}/{id}
- "Create a validate?" -> POST /api/v2/integration-capabilities/featureStore/{projectKey}/{environmentKey}/{integrationKey}/{id}/validate
- "List all flag-import?" -> GET /api/v2/integration-capabilities/flag-import
- "Get flag-import details?" -> GET /api/v2/integration-capabilities/flag-import/{projectKey}/{integrationKey}/{integrationId}
- "Partially update a flag-import?" -> PATCH /api/v2/integration-capabilities/flag-import/{projectKey}/{integrationKey}/{integrationId}
- "Delete a flag-import?" -> DELETE /api/v2/integration-capabilities/flag-import/{projectKey}/{integrationKey}/{integrationId}
- "Create a trigger?" -> POST /api/v2/integration-capabilities/flag-import/{projectKey}/{integrationKey}/{integrationId}/trigger
- "Get key details?" -> GET /api/v2/integration-configurations/keys/{integrationKey}
- "Get integration-configuration details?" -> GET /api/v2/integration-configurations/{integrationConfigurationId}
- "Partially update a integration-configuration?" -> PATCH /api/v2/integration-configurations/{integrationConfigurationId}
- "Delete a integration-configuration?" -> DELETE /api/v2/integration-configurations/{integrationConfigurationId}
- "Get integration details?" -> GET /api/v2/integrations/{integrationKey}
- "Get integration details?" -> GET /api/v2/integrations/{integrationKey}/{id}
- "Partially update a integration?" -> PATCH /api/v2/integrations/{integrationKey}/{id}
- "Delete a integration?" -> DELETE /api/v2/integrations/{integrationKey}/{id}
- "List all members?" -> GET /api/v2/members
- "Create a member?" -> POST /api/v2/members
- "Get member details?" -> GET /api/v2/members/{id}
- "Partially update a member?" -> PATCH /api/v2/members/{id}
- "Delete a member?" -> DELETE /api/v2/members/{id}
- "Create a team?" -> POST /api/v2/members/{id}/teams
- "Get metric details?" -> GET /api/v2/metrics/{projectKey}
- "Get metric details?" -> GET /api/v2/metrics/{projectKey}/{metricKey}
- "Partially update a metric?" -> PATCH /api/v2/metrics/{projectKey}/{metricKey}
- "Delete a metric?" -> DELETE /api/v2/metrics/{projectKey}/{metricKey}
- "List all clients?" -> GET /api/v2/oauth/clients
- "Create a client?" -> POST /api/v2/oauth/clients
- "Get client details?" -> GET /api/v2/oauth/clients/{clientId}
- "Partially update a client?" -> PATCH /api/v2/oauth/clients/{clientId}
- "Delete a client?" -> DELETE /api/v2/oauth/clients/{clientId}
- "List all openapi.json?" -> GET /api/v2/openapi.json
- "List all projects?" -> GET /api/v2/projects
- "Create a project?" -> POST /api/v2/projects
- "Get project details?" -> GET /api/v2/projects/{projectKey}
- "Partially update a project?" -> PATCH /api/v2/projects/{projectKey}
- "Delete a project?" -> DELETE /api/v2/projects/{projectKey}
- "List all context-kinds?" -> GET /api/v2/projects/{projectKey}/context-kinds
- "Update a context-kind?" -> PUT /api/v2/projects/{projectKey}/context-kinds/{key}
- "List all environments?" -> GET /api/v2/projects/{projectKey}/environments
- "Create a environment?" -> POST /api/v2/projects/{projectKey}/environments
- "Get environment details?" -> GET /api/v2/projects/{projectKey}/environments/{environmentKey}
- "Partially update a environment?" -> PATCH /api/v2/projects/{projectKey}/environments/{environmentKey}
- "Delete a environment?" -> DELETE /api/v2/projects/{projectKey}/environments/{environmentKey}
- "Create a apiKey?" -> POST /api/v2/projects/{projectKey}/environments/{environmentKey}/apiKey
- "List all context-attributes?" -> GET /api/v2/projects/{projectKey}/environments/{environmentKey}/context-attributes
- "Get context-attribute details?" -> GET /api/v2/projects/{projectKey}/environments/{environmentKey}/context-attributes/{attributeName}
- "Create a search?" -> POST /api/v2/projects/{projectKey}/environments/{environmentKey}/context-instances/search
- "Get context-instance details?" -> GET /api/v2/projects/{projectKey}/environments/{environmentKey}/context-instances/{id}
- "Delete a context-instance?" -> DELETE /api/v2/projects/{projectKey}/environments/{environmentKey}/context-instances/{id}
- "Create a search?" -> POST /api/v2/projects/{projectKey}/environments/{environmentKey}/contexts/search
- "Update a flag?" -> PUT /api/v2/projects/{projectKey}/environments/{environmentKey}/contexts/{contextKind}/{contextKey}/flags/{featureFlagKey}
- "Get context details?" -> GET /api/v2/projects/{projectKey}/environments/{environmentKey}/contexts/{kind}/{key}
- "List all experiments?" -> GET /api/v2/projects/{projectKey}/environments/{environmentKey}/experiments
- "Create a experiment?" -> POST /api/v2/projects/{projectKey}/environments/{environmentKey}/experiments
- "Get experiment details?" -> GET /api/v2/projects/{projectKey}/environments/{environmentKey}/experiments/{experimentKey}
- "Partially update a experiment?" -> PATCH /api/v2/projects/{projectKey}/environments/{environmentKey}/experiments/{experimentKey}
- "Create a iteration?" -> POST /api/v2/projects/{projectKey}/environments/{environmentKey}/experiments/{experimentKey}/iterations
- "Create a evaluate?" -> POST /api/v2/projects/{projectKey}/environments/{environmentKey}/flags/evaluate
- "List all followers?" -> GET /api/v2/projects/{projectKey}/environments/{environmentKey}/followers
- "List all holdouts?" -> GET /api/v2/projects/{projectKey}/environments/{environmentKey}/holdouts
- "Create a holdout?" -> POST /api/v2/projects/{projectKey}/environments/{environmentKey}/holdouts
- "Get id details?" -> GET /api/v2/projects/{projectKey}/environments/{environmentKey}/holdouts/id/{holdoutId}
- "Get holdout details?" -> GET /api/v2/projects/{projectKey}/environments/{environmentKey}/holdouts/{holdoutKey}
- "Partially update a holdout?" -> PATCH /api/v2/projects/{projectKey}/environments/{environmentKey}/holdouts/{holdoutKey}
- "Create a mobileKey?" -> POST /api/v2/projects/{projectKey}/environments/{environmentKey}/mobileKey
- "Create a evaluate?" -> POST /api/v2/projects/{projectKey}/environments/{environmentKey}/segments/evaluate
- "List all experimentation-settings?" -> GET /api/v2/projects/{projectKey}/experimentation-settings
- "List all flag-defaults?" -> GET /api/v2/projects/{projectKey}/flag-defaults
- "List all approval-requests?" -> GET /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests
- "Create a approval-request?" -> POST /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests
- "Create a approval-requests-flag-copy?" -> POST /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests-flag-copy
- "Get approval-request details?" -> GET /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests/{id}
- "Partially update a approval-request?" -> PATCH /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests/{id}
- "Delete a approval-request?" -> DELETE /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests/{id}
- "Create a apply?" -> POST /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests/{id}/apply
- "Create a review?" -> POST /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests/{id}/reviews
- "List all followers?" -> GET /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/followers
- "Update a follower?" -> PUT /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/followers/{memberId}
- "Delete a follower?" -> DELETE /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/followers/{memberId}
- "List all scheduled-changes?" -> GET /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/scheduled-changes
- "Create a scheduled-change?" -> POST /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/scheduled-changes
- "Get scheduled-change details?" -> GET /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/scheduled-changes/{id}
- "Partially update a scheduled-change?" -> PATCH /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/scheduled-changes/{id}
- "Delete a scheduled-change?" -> DELETE /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/scheduled-changes/{id}
- "List all workflows?" -> GET /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/workflows
- "Create a workflow?" -> POST /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/workflows
- "Get workflow details?" -> GET /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/workflows/{workflowId}
- "Delete a workflow?" -> DELETE /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/workflows/{workflowId}
- "Create a migration-safety-issue?" -> POST /api/v2/projects/{projectKey}/flags/{flagKey}/environments/{environmentKey}/migration-safety-issues
- "Update a phase?" -> PUT /api/v2/projects/{projectKey}/flags/{flagKey}/release/phases/{phaseId}
- "List all layers?" -> GET /api/v2/projects/{projectKey}/layers
- "Create a layer?" -> POST /api/v2/projects/{projectKey}/layers
- "Partially update a layer?" -> PATCH /api/v2/projects/{projectKey}/layers/{layerKey}
- "List all metric-groups?" -> GET /api/v2/projects/{projectKey}/metric-groups
- "Create a metric-group?" -> POST /api/v2/projects/{projectKey}/metric-groups
- "Get metric-group details?" -> GET /api/v2/projects/{projectKey}/metric-groups/{metricGroupKey}
- "Partially update a metric-group?" -> PATCH /api/v2/projects/{projectKey}/metric-groups/{metricGroupKey}
- "Delete a metric-group?" -> DELETE /api/v2/projects/{projectKey}/metric-groups/{metricGroupKey}
- "List all release-pipelines?" -> GET /api/v2/projects/{projectKey}/release-pipelines
- "Create a release-pipeline?" -> POST /api/v2/projects/{projectKey}/release-pipelines
- "Get release-pipeline details?" -> GET /api/v2/projects/{projectKey}/release-pipelines/{pipelineKey}
- "Update a release-pipeline?" -> PUT /api/v2/projects/{projectKey}/release-pipelines/{pipelineKey}
- "Delete a release-pipeline?" -> DELETE /api/v2/projects/{projectKey}/release-pipelines/{pipelineKey}
- "List all releases?" -> GET /api/v2/projects/{projectKey}/release-pipelines/{pipelineKey}/releases
- "List all public-ip-list?" -> GET /api/v2/public-ip-list
- "List all roles?" -> GET /api/v2/roles
- "Create a role?" -> POST /api/v2/roles
- "Get role details?" -> GET /api/v2/roles/{customRoleKey}
- "Partially update a role?" -> PATCH /api/v2/roles/{customRoleKey}
- "Delete a role?" -> DELETE /api/v2/roles/{customRoleKey}
- "Get segment details?" -> GET /api/v2/segments/{projectKey}/{environmentKey}
- "Get segment details?" -> GET /api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}
- "Partially update a segment?" -> PATCH /api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}
- "Delete a segment?" -> DELETE /api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}
- "Create a context?" -> POST /api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/contexts
- "Get context details?" -> GET /api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/contexts/{contextKey}
- "Create a export?" -> POST /api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/exports
- "Get export details?" -> GET /api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/exports/{exportID}
- "Create a import?" -> POST /api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/imports
- "Get import details?" -> GET /api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/imports/{importID}
- "Create a user?" -> POST /api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/users
- "Get user details?" -> GET /api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/users/{userKey}
- "Get expiring-target details?" -> GET /api/v2/segments/{projectKey}/{segmentKey}/expiring-targets/{environmentKey}
- "Partially update a expiring-target?" -> PATCH /api/v2/segments/{projectKey}/{segmentKey}/expiring-targets/{environmentKey}
- "Get expiring-user-target details?" -> GET /api/v2/segments/{projectKey}/{segmentKey}/expiring-user-targets/{environmentKey}
- "Partially update a expiring-user-target?" -> PATCH /api/v2/segments/{projectKey}/{segmentKey}/expiring-user-targets/{environmentKey}
- "List all teams?" -> GET /api/v2/teams
- "Create a team?" -> POST /api/v2/teams
- "Get team details?" -> GET /api/v2/teams/{teamKey}
- "Partially update a team?" -> PATCH /api/v2/teams/{teamKey}
- "Delete a team?" -> DELETE /api/v2/teams/{teamKey}
- "List all maintainers?" -> GET /api/v2/teams/{teamKey}/maintainers
- "Create a member?" -> POST /api/v2/teams/{teamKey}/members
- "List all roles?" -> GET /api/v2/teams/{teamKey}/roles
- "Search templates?" -> GET /api/v2/templates
- "Create a template?" -> POST /api/v2/templates
- "Delete a template?" -> DELETE /api/v2/templates/{templateKey}
- "List all tokens?" -> GET /api/v2/tokens
- "Create a token?" -> POST /api/v2/tokens
- "Get token details?" -> GET /api/v2/tokens/{id}
- "Partially update a token?" -> PATCH /api/v2/tokens/{id}
- "Delete a token?" -> DELETE /api/v2/tokens/{id}
- "Create a reset?" -> POST /api/v2/tokens/{id}/reset
- "List all clientside-contexts?" -> GET /api/v2/usage/clientside-contexts
- "List all clientside-mau?" -> GET /api/v2/usage/clientside-mau
- "List all data-export-events?" -> GET /api/v2/usage/data-export-events
- "Get evaluation details?" -> GET /api/v2/usage/evaluations/{projectKey}/{environmentKey}/{featureFlagKey}
- "Get event details?" -> GET /api/v2/usage/events/{type}
- "List all experimentation-events?" -> GET /api/v2/usage/experimentation-events
- "List all experimentation-keys?" -> GET /api/v2/usage/experimentation-keys
- "List all mau?" -> GET /api/v2/usage/mau
- "List all bycategory?" -> GET /api/v2/usage/mau/bycategory
- "List all sdks?" -> GET /api/v2/usage/mau/sdks
- "List all errors?" -> GET /api/v2/usage/observability/errors
- "List all logs?" -> GET /api/v2/usage/observability/logs
- "List all metrics?" -> GET /api/v2/usage/observability/metrics
- "List all sessions?" -> GET /api/v2/usage/observability/sessions
- "List all traces?" -> GET /api/v2/usage/observability/traces
- "List all details?" -> GET /api/v2/usage/sdk-versions/details
- "List all serverside-contexts?" -> GET /api/v2/usage/serverside-contexts
- "List all service-connections?" -> GET /api/v2/usage/service-connections
- "Get stream details?" -> GET /api/v2/usage/streams/{source}
- "List all bysdkversion?" -> GET /api/v2/usage/streams/{source}/bysdkversion
- "List all sdkversions?" -> GET /api/v2/usage/streams/{source}/sdkversions
- "List all total-contexts?" -> GET /api/v2/usage/total-contexts
- "List all total-mau?" -> GET /api/v2/usage/total-mau
- "List all vega-ai?" -> GET /api/v2/usage/vega-ai
- "Get user-attribute details?" -> GET /api/v2/user-attributes/{projectKey}/{environmentKey}
- "Search user-search?" -> GET /api/v2/user-search/{projectKey}/{environmentKey}
- "Get user details?" -> GET /api/v2/users/{projectKey}/{environmentKey}
- "Get user details?" -> GET /api/v2/users/{projectKey}/{environmentKey}/{userKey}
- "Delete a user?" -> DELETE /api/v2/users/{projectKey}/{environmentKey}/{userKey}
- "List all flags?" -> GET /api/v2/users/{projectKey}/{environmentKey}/{userKey}/flags
- "Get flag details?" -> GET /api/v2/users/{projectKey}/{environmentKey}/{userKey}/flags/{featureFlagKey}
- "Update a flag?" -> PUT /api/v2/users/{projectKey}/{environmentKey}/{userKey}/flags/{featureFlagKey}
- "Get expiring-user-target details?" -> GET /api/v2/users/{projectKey}/{userKey}/expiring-user-targets/{environmentKey}
- "Partially update a expiring-user-target?" -> PATCH /api/v2/users/{projectKey}/{userKey}/expiring-user-targets/{environmentKey}
- "List all versions?" -> GET /api/v2/versions
- "List all webhooks?" -> GET /api/v2/webhooks
- "Create a webhook?" -> POST /api/v2/webhooks
- "Get webhook details?" -> GET /api/v2/webhooks/{id}
- "Partially update a webhook?" -> PATCH /api/v2/webhooks/{id}
- "Delete a webhook?" -> DELETE /api/v2/webhooks/{id}
- "List all tags?" -> GET /api/v2/tags
- "List all targeting?" -> GET /api/v2/projects/{projectKey}/ai-configs/{configKey}/targeting
- "List all ai-configs?" -> GET /api/v2/projects/{projectKey}/ai-configs
- "Create a ai-config?" -> POST /api/v2/projects/{projectKey}/ai-configs
- "Delete a ai-config?" -> DELETE /api/v2/projects/{projectKey}/ai-configs/{configKey}
- "Get ai-config details?" -> GET /api/v2/projects/{projectKey}/ai-configs/{configKey}
- "Partially update a ai-config?" -> PATCH /api/v2/projects/{projectKey}/ai-configs/{configKey}
- "Create a variation?" -> POST /api/v2/projects/{projectKey}/ai-configs/{configKey}/variations
- "Delete a variation?" -> DELETE /api/v2/projects/{projectKey}/ai-configs/{configKey}/variations/{variationKey}
- "Get variation details?" -> GET /api/v2/projects/{projectKey}/ai-configs/{configKey}/variations/{variationKey}
- "Partially update a variation?" -> PATCH /api/v2/projects/{projectKey}/ai-configs/{configKey}/variations/{variationKey}
- "List all metrics?" -> GET /api/v2/projects/{projectKey}/ai-configs/{configKey}/metrics
- "List all metrics-by-variation?" -> GET /api/v2/projects/{projectKey}/ai-configs/{configKey}/metrics-by-variation
- "Create a restricted?" -> POST /api/v2/projects/{projectKey}/ai-configs/model-configs/restricted
- "List all model-configs?" -> GET /api/v2/projects/{projectKey}/ai-configs/model-configs
- "Create a model-config?" -> POST /api/v2/projects/{projectKey}/ai-configs/model-configs
- "Delete a model-config?" -> DELETE /api/v2/projects/{projectKey}/ai-configs/model-configs/{modelConfigKey}
- "Get model-config details?" -> GET /api/v2/projects/{projectKey}/ai-configs/model-configs/{modelConfigKey}
- "List all ai-tools?" -> GET /api/v2/projects/{projectKey}/ai-tools
- "Create a ai-tool?" -> POST /api/v2/projects/{projectKey}/ai-tools
- "List all versions?" -> GET /api/v2/projects/{projectKey}/ai-tools/{toolKey}/versions
- "Delete a ai-tool?" -> DELETE /api/v2/projects/{projectKey}/ai-tools/{toolKey}
- "Get ai-tool details?" -> GET /api/v2/projects/{projectKey}/ai-tools/{toolKey}
- "Partially update a ai-tool?" -> PATCH /api/v2/projects/{projectKey}/ai-tools/{toolKey}
- "List all agent-graphs?" -> GET /api/v2/projects/{projectKey}/agent-graphs
- "Create a agent-graph?" -> POST /api/v2/projects/{projectKey}/agent-graphs
- "Delete a agent-graph?" -> DELETE /api/v2/projects/{projectKey}/agent-graphs/{graphKey}
- "Get agent-graph details?" -> GET /api/v2/projects/{projectKey}/agent-graphs/{graphKey}
- "Partially update a agent-graph?" -> PATCH /api/v2/projects/{projectKey}/agent-graphs/{graphKey}
- "List all announcements?" -> GET /api/v2/announcements
- "Create a announcement?" -> POST /api/v2/announcements
- "Delete a announcement?" -> DELETE /api/v2/announcements/{announcementId}
- "Partially update a announcement?" -> PATCH /api/v2/announcements/{announcementId}
- "List all settings?" -> GET /api/v2/approval-requests/projects/{projectKey}/settings
- "List all views?" -> GET /api/v2/projects/{projectKey}/views
- "Create a view?" -> POST /api/v2/projects/{projectKey}/views
- "Delete a view?" -> DELETE /api/v2/projects/{projectKey}/views/{viewKey}
- "Get view details?" -> GET /api/v2/projects/{projectKey}/views/{viewKey}
- "Partially update a view?" -> PATCH /api/v2/projects/{projectKey}/views/{viewKey}
- "Delete a link?" -> DELETE /api/v2/projects/{projectKey}/views/{viewKey}/link/{resourceType}
- "Search linked?" -> GET /api/v2/projects/{projectKey}/views/{viewKey}/linked/{resourceType}
- "Get view-association details?" -> GET /api/v2/projects/{projectKey}/view-associations/{resourceType}/{resourceKey}
- "List all release-policies?" -> GET /api/v2/projects/{projectKey}/release-policies
- "Create a release-policy?" -> POST /api/v2/projects/{projectKey}/release-policies
- "Create a order?" -> POST /api/v2/projects/{projectKey}/release-policies/order
- "Delete a release-policy?" -> DELETE /api/v2/projects/{projectKey}/release-policies/{policyKey}
- "Get release-policy details?" -> GET /api/v2/projects/{projectKey}/release-policies/{policyKey}
- "Update a release-policy?" -> PUT /api/v2/projects/{projectKey}/release-policies/{policyKey}
- "List all frequency?" -> GET /api/v2/engineering-insights/charts/deployments/frequency
- "List all stale?" -> GET /api/v2/engineering-insights/charts/flags/stale
- "List all status?" -> GET /api/v2/engineering-insights/charts/flags/status
- "List all lead-time?" -> GET /api/v2/engineering-insights/charts/lead-time
- "List all frequency?" -> GET /api/v2/engineering-insights/charts/releases/frequency
- "Create a deployment-event?" -> POST /api/v2/engineering-insights/deployment-events
- "List all deployments?" -> GET /api/v2/engineering-insights/deployments
- "Get deployment details?" -> GET /api/v2/engineering-insights/deployments/{deploymentID}
- "Partially update a deployment?" -> PATCH /api/v2/engineering-insights/deployments/{deploymentID}
- "Search flag-events?" -> GET /api/v2/engineering-insights/flag-events
- "Create a group?" -> POST /api/v2/engineering-insights/insights/group
- "Search groups?" -> GET /api/v2/engineering-insights/insights/groups
- "Get group details?" -> GET /api/v2/engineering-insights/insights/groups/{insightGroupKey}
- "Partially update a group?" -> PATCH /api/v2/engineering-insights/insights/groups/{insightGroupKey}
- "Delete a group?" -> DELETE /api/v2/engineering-insights/insights/groups/{insightGroupKey}
- "List all scores?" -> GET /api/v2/engineering-insights/insights/scores
- "Search pull-requests?" -> GET /api/v2/engineering-insights/pull-requests
- "List all repositories?" -> GET /api/v2/engineering-insights/repositories
- "Delete a project?" -> DELETE /api/v2/engineering-insights/repositories/{repositoryKey}/projects/{projectKey}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
