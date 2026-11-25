---
name: api-reference
description: "API Reference API skill. Use when working with API Reference for api. Covers 215 endpoints."
version: 1.0.0
generator: lapsh
---

# API Reference
API version: v0

## Auth
Bearer bearer | Bearer DSN

## Base URL
https://us.sentry.io

## Setup
1. Set Authorization header with your Bearer token
2. GET /api/0/organizations/ -- verify access
3. POST /api/0/organizations/{organization_id_or_slug}/alert-rules/ -- create first alert-rules

## Endpoints

215 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/0/organizations/ | Return a list of organizations available to the authenticated session in a region. |
| GET | /api/0/organizations/{organization_id_or_slug}/ | Return details on an individual organization, including various details |
| PUT | /api/0/organizations/{organization_id_or_slug}/ | Update various attributes and configurable settings for the given organization. |
| GET | /api/0/organizations/{organization_id_or_slug}/alert-rules/ | ## Deprecated |
| POST | /api/0/organizations/{organization_id_or_slug}/alert-rules/ | ## Deprecated |
| GET | /api/0/organizations/{organization_id_or_slug}/alert-rules/{alert_rule_id}/ | ## Deprecated |
| PUT | /api/0/organizations/{organization_id_or_slug}/alert-rules/{alert_rule_id}/ | ## Deprecated |
| DELETE | /api/0/organizations/{organization_id_or_slug}/alert-rules/{alert_rule_id}/ | ## Deprecated |
| GET | /api/0/organizations/{organization_id_or_slug}/config/integrations/ | Get integration provider information about all available integrations for an organization. |
| GET | /api/0/organizations/{organization_id_or_slug}/dashboards/ | Retrieve a list of custom dashboards that are associated with the given organization. |
| POST | /api/0/organizations/{organization_id_or_slug}/dashboards/ | Create a new dashboard for the given Organization |
| GET | /api/0/organizations/{organization_id_or_slug}/dashboards/{dashboard_id}/ | Return details about an organization's custom dashboard. |
| PUT | /api/0/organizations/{organization_id_or_slug}/dashboards/{dashboard_id}/ | Edit an organization's custom dashboard as well as any bulk |
| DELETE | /api/0/organizations/{organization_id_or_slug}/dashboards/{dashboard_id}/ | Delete an organization's custom dashboard, or tombstone |
| GET | /api/0/organizations/{organization_id_or_slug}/detectors/ | ⚠️ This endpoint is currently in **beta** and may be subject to change. It is supported by [New Monitors and Alerts](/product/new-monitors-and-alerts/) and may not be viewable in the UI today. |
| POST | /api/0/organizations/{organization_id_or_slug}/detectors/ | ⚠️ This endpoint is currently in **beta** and may be subject to change. It is supported by [New Monitors and Alerts](/product/new-monitors-and-alerts/) and may not be viewable in the UI today. |
| PUT | /api/0/organizations/{organization_id_or_slug}/detectors/ | ⚠️ This endpoint is currently in **beta** and may be subject to change. It is supported by [New Monitors and Alerts](/product/new-monitors-and-alerts/) and may not be viewable in the UI today. |
| DELETE | /api/0/organizations/{organization_id_or_slug}/detectors/ | ⚠️ This endpoint is currently in **beta** and may be subject to change. It is supported by [New Monitors and Alerts](/product/new-monitors-and-alerts/) and may not be viewable in the UI today. |
| GET | /api/0/organizations/{organization_id_or_slug}/detectors/{detector_id}/ | ⚠️ This endpoint is currently in **beta** and may be subject to change. It is supported by [New Monitors and Alerts](/product/new-monitors-and-alerts/) and may not be viewable in the UI today. |
| PUT | /api/0/organizations/{organization_id_or_slug}/detectors/{detector_id}/ | ⚠️ This endpoint is currently in **beta** and may be subject to change. It is supported by [New Monitors and Alerts](/product/new-monitors-and-alerts/) and may not be viewable in the UI today. |
| DELETE | /api/0/organizations/{organization_id_or_slug}/detectors/{detector_id}/ | ⚠️ This endpoint is currently in **beta** and may be subject to change. It is supported by [New Monitors and Alerts](/product/new-monitors-and-alerts/) and may not be viewable in the UI today. |
| GET | /api/0/organizations/{organization_id_or_slug}/discover/saved/ | Retrieve a list of saved queries that are associated with the given organization. |
| POST | /api/0/organizations/{organization_id_or_slug}/discover/saved/ | Create a new saved query for the given organization. |
| GET | /api/0/organizations/{organization_id_or_slug}/discover/saved/{query_id}/ | Retrieve a saved query. |
| PUT | /api/0/organizations/{organization_id_or_slug}/discover/saved/{query_id}/ | Modify a saved query. |
| DELETE | /api/0/organizations/{organization_id_or_slug}/discover/saved/{query_id}/ | Delete a saved query. |
| GET | /api/0/organizations/{organization_id_or_slug}/environments/ | Lists an organization's environments. |
| GET | /api/0/organizations/{organization_id_or_slug}/eventids/{event_id}/ | This resolves an event ID to the project slug and internal issue ID and internal event ID. |
| GET | /api/0/organizations/{organization_id_or_slug}/events/ | Retrieves explore data for a given organization. |
| GET | /api/0/organizations/{organization_id_or_slug}/events-timeseries/ | Retrieves explore data for a given organization as a timeseries. |
| POST | /api/0/organizations/{organization_id_or_slug}/external-users/ | Link a user from an external provider to a Sentry user. |
| PUT | /api/0/organizations/{organization_id_or_slug}/external-users/{external_user_id}/ | Update a user in an external provider that is currently linked to a Sentry user. |
| DELETE | /api/0/organizations/{organization_id_or_slug}/external-users/{external_user_id}/ | Delete the link between a user from an external provider and a Sentry user. |
| GET | /api/0/organizations/{organization_id_or_slug}/forwarding/ | Returns a list of data forwarders for an organization. |
| POST | /api/0/organizations/{organization_id_or_slug}/forwarding/ | Creates a new data forwarder for an organization. |
| PUT | /api/0/organizations/{organization_id_or_slug}/forwarding/{data_forwarder_id}/ | Updates a data forwarder for an organization or update a project-specific override. |
| DELETE | /api/0/organizations/{organization_id_or_slug}/forwarding/{data_forwarder_id}/ | Deletes a data forwarder for an organization. All project-specific overrides will be deleted as well. |
| GET | /api/0/organizations/{organization_id_or_slug}/integrations/ | Lists all the available Integrations for an Organization. |
| GET | /api/0/organizations/{organization_id_or_slug}/integrations/{integration_id}/ | OrganizationIntegrationBaseEndpoints expect both Integration and |
| DELETE | /api/0/organizations/{organization_id_or_slug}/integrations/{integration_id}/ | OrganizationIntegrationBaseEndpoints expect both Integration and |
| GET | /api/0/organizations/{organization_id_or_slug}/issues/ | Return a list of issues for an organization. All parameters are supplied as query string parameters. A default query of `is:unresolved` is applied. To return all results, use an empty query value (i.e. ``?query=`). |
| PUT | /api/0/organizations/{organization_id_or_slug}/issues/ | Bulk mutate various attributes on a maxmimum of 1000 issues. |
| DELETE | /api/0/organizations/{organization_id_or_slug}/issues/ | Permanently remove the given issues. If IDs are provided, queries and filtering will be ignored. If any IDs are out of scope, the data won't be mutated but the endpoint will still produce a successful response. For example, if no issues were found matching the criteria, a HTTP 204 is returned. |
| GET | /api/0/organizations/{organization_id_or_slug}/members/ | List all organization members. |
| POST | /api/0/organizations/{organization_id_or_slug}/members/ | Add or invite a member to an organization. |
| GET | /api/0/organizations/{organization_id_or_slug}/members/{member_id}/ | Retrieve an organization member's details. |
| PUT | /api/0/organizations/{organization_id_or_slug}/members/{member_id}/ | Update a member's [organization-level](https://docs.sentry.io/organization/membership/#organization-level-roles) and [team-level](https://docs.sentry.io/organization/membership/#team-level-roles) roles. |
| DELETE | /api/0/organizations/{organization_id_or_slug}/members/{member_id}/ | Remove an organization member. |
| POST | /api/0/organizations/{organization_id_or_slug}/members/{member_id}/teams/{team_id_or_slug}/ | This request can return various success codes depending on the context of the team: |
| PUT | /api/0/organizations/{organization_id_or_slug}/members/{member_id}/teams/{team_id_or_slug}/ | The relevant organization member must already be a part of the team. |
| DELETE | /api/0/organizations/{organization_id_or_slug}/members/{member_id}/teams/{team_id_or_slug}/ | Delete an organization member from a team. |
| GET | /api/0/organizations/{organization_id_or_slug}/monitors/ | Lists monitors, including nested monitor environments. May be filtered to a project or environment. |
| POST | /api/0/organizations/{organization_id_or_slug}/monitors/ | Create a new monitor. |
| GET | /api/0/organizations/{organization_id_or_slug}/monitors/{monitor_id_or_slug}/ | Retrieves details for a monitor. |
| PUT | /api/0/organizations/{organization_id_or_slug}/monitors/{monitor_id_or_slug}/ | Update a monitor. |
| DELETE | /api/0/organizations/{organization_id_or_slug}/monitors/{monitor_id_or_slug}/ | Delete a monitor or monitor environments. |
| GET | /api/0/organizations/{organization_id_or_slug}/monitors/{monitor_id_or_slug}/checkins/ | Retrieve a list of check-ins for a monitor |
| GET | /api/0/organizations/{organization_id_or_slug}/notifications/actions/ | Returns all Spike Protection Notification Actions for an organization. |
| POST | /api/0/organizations/{organization_id_or_slug}/notifications/actions/ | Creates a new Notification Action for Spike Protection. |
| GET | /api/0/organizations/{organization_id_or_slug}/notifications/actions/{action_id}/ | Returns a serialized Spike Protection Notification Action object. |
| PUT | /api/0/organizations/{organization_id_or_slug}/notifications/actions/{action_id}/ | Updates a Spike Protection Notification Action. |
| DELETE | /api/0/organizations/{organization_id_or_slug}/notifications/actions/{action_id}/ | Deletes a Spike Protection Notification Action. |
| GET | /api/0/organizations/{organization_id_or_slug}/preprodartifacts/{artifact_id}/install-details/ | Retrieve install info for a given artifact. |
| GET | /api/0/organizations/{organization_id_or_slug}/preprodartifacts/{artifact_id}/size-analysis/ | Retrieve size analysis results for a given artifact. |
| GET | /api/0/organizations/{organization_id_or_slug}/prevent/owner/{owner}/repositories/ | Retrieves repository data for a given owner. |
| GET | /api/0/organizations/{organization_id_or_slug}/prevent/owner/{owner}/repositories/sync/ | Gets syncing status for repositories for an integrated organization. |
| POST | /api/0/organizations/{organization_id_or_slug}/prevent/owner/{owner}/repositories/sync/ | Syncs repositories for an integrated organization with GitHub. |
| GET | /api/0/organizations/{organization_id_or_slug}/prevent/owner/{owner}/repositories/tokens/ | Retrieves a paginated list of repository tokens for a given owner. |
| GET | /api/0/organizations/{organization_id_or_slug}/prevent/owner/{owner}/repository/{repository}/ | Retrieves repository data for a single repository. |
| GET | /api/0/organizations/{organization_id_or_slug}/prevent/owner/{owner}/repository/{repository}/branches/ | Retrieves branch data for a given owner and repository. |
| GET | /api/0/organizations/{organization_id_or_slug}/prevent/owner/{owner}/repository/{repository}/test-results/ | Retrieves the list of test results for a given repository and owner. Also accepts a number of query parameters to filter the results. |
| GET | /api/0/organizations/{organization_id_or_slug}/prevent/owner/{owner}/repository/{repository}/test-results-aggregates/ | Retrieves aggregated test result metrics for a given repository and owner. |
| GET | /api/0/organizations/{organization_id_or_slug}/prevent/owner/{owner}/repository/{repository}/test-suites/ | Retrieves test suites belonging to a repository's test results. |
| POST | /api/0/organizations/{organization_id_or_slug}/prevent/owner/{owner}/repository/{repository}/token/regenerate/ | Regenerates a repository upload token and returns the new token. |
| GET | /api/0/organizations/{organization_id_or_slug}/project-keys/ | Return a list of client keys (DSNs) for all projects in an organization. |
| GET | /api/0/organizations/{organization_id_or_slug}/projects/ | Return a list of projects bound to a organization. |
| GET | /api/0/organizations/{organization_id_or_slug}/relay_usage/ | Return a list of trusted relays bound to an organization. |
| GET | /api/0/organizations/{organization_id_or_slug}/release-threshold-statuses/ | **`[WARNING]`**: This API is an experimental Alpha feature and is subject to change! |
| GET | /api/0/organizations/{organization_id_or_slug}/releases/{version}/ | Return details on an individual release. |
| PUT | /api/0/organizations/{organization_id_or_slug}/releases/{version}/ | Update a release. This can change some metadata associated with |
| DELETE | /api/0/organizations/{organization_id_or_slug}/releases/{version}/ | Permanently remove a release and all of its files. |
| GET | /api/0/organizations/{organization_id_or_slug}/releases/{version}/deploys/ | Returns a list of deploys based on the organization, version, and project. |
| POST | /api/0/organizations/{organization_id_or_slug}/releases/{version}/deploys/ | Create a deploy for a given release. |
| GET | /api/0/organizations/{organization_id_or_slug}/replay-count/ | Return a count of replays for a list of issue or transaction IDs. |
| GET | /api/0/organizations/{organization_id_or_slug}/replay-selectors/ | Return a list of selectors for a given organization. |
| GET | /api/0/organizations/{organization_id_or_slug}/replays/ | Return a list of replays belonging to an organization. |
| GET | /api/0/organizations/{organization_id_or_slug}/replays/{replay_id}/ | Return details on an individual replay. |
| GET | /api/0/organizations/{organization_id_or_slug}/repos/{repo_id}/commits/ | List a Repository's Commits |
| GET | /api/0/organizations/{organization_id_or_slug}/scim/v2/Groups | Returns a paginated list of teams bound to a organization with a SCIM Groups GET Request. |
| POST | /api/0/organizations/{organization_id_or_slug}/scim/v2/Groups | Create a new team bound to an organization via a SCIM Groups POST |
| GET | /api/0/organizations/{organization_id_or_slug}/scim/v2/Groups/{team_id_or_slug} | Query an individual team with a SCIM Group GET Request. |
| PATCH | /api/0/organizations/{organization_id_or_slug}/scim/v2/Groups/{team_id_or_slug} | Update a team's attributes with a SCIM Group PATCH Request. |
| DELETE | /api/0/organizations/{organization_id_or_slug}/scim/v2/Groups/{team_id_or_slug} | Delete a team with a SCIM Group DELETE Request. |
| GET | /api/0/organizations/{organization_id_or_slug}/scim/v2/Users | Returns a paginated list of members bound to a organization with a SCIM Users GET Request. |
| POST | /api/0/organizations/{organization_id_or_slug}/scim/v2/Users | Create a new Organization Member via a SCIM Users POST Request. |
| GET | /api/0/organizations/{organization_id_or_slug}/scim/v2/Users/{member_id} | Query an individual organization member with a SCIM User GET Request. |
| PATCH | /api/0/organizations/{organization_id_or_slug}/scim/v2/Users/{member_id} | Update an organization member's attributes with a SCIM PATCH Request. |
| DELETE | /api/0/organizations/{organization_id_or_slug}/scim/v2/Users/{member_id} | Delete an organization member with a SCIM User DELETE Request. |
| GET | /api/0/organizations/{organization_id_or_slug}/sentry-apps/ | Retrieve the custom integrations for an organization |
| GET | /api/0/organizations/{organization_id_or_slug}/sessions/ | Returns a time series of release health session statistics for projects bound to an organization. |
| GET | /api/0/organizations/{organization_id_or_slug}/shortids/{issue_id}/ | Resolve a short ID to the project slug and group details. |
| GET | /api/0/organizations/{organization_id_or_slug}/stats-summary/ | Query summarized event counts by project for your Organization. Also see https://docs.sentry.io/api/organizations/retrieve-event-counts-for-an-organization-v2/ for reference. |
| GET | /api/0/organizations/{organization_id_or_slug}/stats_v2/ | Query event counts for your Organization. |
| GET | /api/0/organizations/{organization_id_or_slug}/teams/ | Returns a list of teams bound to a organization. |
| POST | /api/0/organizations/{organization_id_or_slug}/teams/ | Create a new team bound to an organization. Requires at least one of the `name` |
| GET | /api/0/organizations/{organization_id_or_slug}/user-teams/ | Returns a list of teams the user has access to in the specified organization. |
| GET | /api/0/organizations/{organization_id_or_slug}/workflows/ | ⚠️ This endpoint is currently in **beta** and may be subject to change. It is supported by [New Monitors and Alerts](/product/new-monitors-and-alerts/) and may not be viewable in the UI today. |
| POST | /api/0/organizations/{organization_id_or_slug}/workflows/ | ⚠️ This endpoint is currently in **beta** and may be subject to change. It is supported by [New Monitors and Alerts](/product/new-monitors-and-alerts/) and may not be viewable in the UI today. |
| PUT | /api/0/organizations/{organization_id_or_slug}/workflows/ | ⚠️ This endpoint is currently in **beta** and may be subject to change. It is supported by [New Monitors and Alerts](/product/new-monitors-and-alerts/) and may not be viewable in the UI today. |
| DELETE | /api/0/organizations/{organization_id_or_slug}/workflows/ | ⚠️ This endpoint is currently in **beta** and may be subject to change. It is supported by [New Monitors and Alerts](/product/new-monitors-and-alerts/) and may not be viewable in the UI today. |
| GET | /api/0/organizations/{organization_id_or_slug}/workflows/{workflow_id}/ | ⚠️ This endpoint is currently in **beta** and may be subject to change. It is supported by [New Monitors and Alerts](/product/new-monitors-and-alerts/) and may not be viewable in the UI today. |
| PUT | /api/0/organizations/{organization_id_or_slug}/workflows/{workflow_id}/ | ⚠️ This endpoint is currently in **beta** and may be subject to change. It is supported by [New Monitors and Alerts](/product/new-monitors-and-alerts/) and may not be viewable in the UI today. |
| DELETE | /api/0/organizations/{organization_id_or_slug}/workflows/{workflow_id}/ | ⚠️ This endpoint is currently in **beta** and may be subject to change. It is supported by [New Monitors and Alerts](/product/new-monitors-and-alerts/) and may not be viewable in the UI today. |
| GET | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/ | Return details on an individual project. |
| PUT | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/ | Update various attributes and configurable settings for the given project. |
| DELETE | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/ | Schedules a project for deletion. |
| GET | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/environments/ | Lists a project's environments. |
| GET | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/environments/{environment}/ | Return details on a project environment. |
| PUT | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/environments/{environment}/ | Update the visibility for a project environment. |
| GET | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/events/ | Return a list of events bound to a project. |
| GET | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/events/{event_id}/source-map-debug/ | Return a list of source map errors for a given event. |
| GET | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/filters/ | Retrieve a list of filters for a given project. |
| PUT | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/filters/{filter_id}/ | Update various inbound data filters for a project. |
| GET | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/keys/ | Return a list of client keys bound to a project. |
| POST | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/keys/ | Create a new client key bound to a project.  The key's secret and public key |
| GET | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/keys/{key_id}/ | Return a client key bound to a project. |
| PUT | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/keys/{key_id}/ | Update various settings for a client key. |
| DELETE | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/keys/{key_id}/ | Delete a client key for a given project. |
| GET | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/members/ | Returns a list of active organization members that belong to any team assigned to the project. |
| GET | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/monitors/{monitor_id_or_slug}/ | Retrieves details for a monitor. |
| PUT | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/monitors/{monitor_id_or_slug}/ | Update a monitor. |
| DELETE | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/monitors/{monitor_id_or_slug}/ | Delete a monitor or monitor environments. |
| GET | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/monitors/{monitor_id_or_slug}/checkins/ | Retrieve a list of check-ins for a monitor |
| GET | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/ownership/ | Returns details on a project's ownership configuration. |
| PUT | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/ownership/ | Updates ownership configurations for a project. Note that only the |
| GET | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/preprodartifacts/build-distribution/latest/ | Get the latest installable build for a project. |
| DELETE | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/replays/{replay_id}/ | Delete a replay. |
| GET | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/replays/{replay_id}/clicks/ | Retrieve a collection of RRWeb DOM node-ids and the timestamp they were clicked. |
| GET | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/replays/{replay_id}/recording-segments/ | Return a collection of replay recording segments. |
| GET | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/replays/{replay_id}/recording-segments/{segment_id}/ | Return a replay recording segment. |
| GET | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/replays/{replay_id}/viewed-by/ | Return a list of users who have viewed a replay. |
| GET | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/rules/ | ## Deprecated |
| POST | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/rules/ | ## Deprecated |
| GET | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/rules/{rule_id}/ | ## Deprecated |
| PUT | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/rules/{rule_id}/ | ## Deprecated |
| DELETE | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/rules/{rule_id}/ | ## Deprecated |
| GET | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/symbol-sources/ | List custom symbol sources configured for a project. |
| POST | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/symbol-sources/ | Add a custom symbol source to a project. |
| PUT | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/symbol-sources/ | Update a custom symbol source in a project. |
| DELETE | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/symbol-sources/ | Delete a custom symbol source from a project. |
| GET | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/teams/ | Return a list of teams that have access to this project. |
| POST | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/teams/{team_id_or_slug}/ | Give a team access to a project. |
| DELETE | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/teams/{team_id_or_slug}/ | Revoke a team's access to a project. |
| GET | /api/0/seer/models/ | Get list of actively used LLM model names from Seer. |
| GET | /api/0/sentry-apps/{sentry_app_id_or_slug}/ | Retrieve a custom integration. |
| PUT | /api/0/sentry-apps/{sentry_app_id_or_slug}/ | Update an existing custom integration. |
| DELETE | /api/0/sentry-apps/{sentry_app_id_or_slug}/ | Delete a custom integration. |
| GET | /api/0/teams/{organization_id_or_slug}/{team_id_or_slug}/ | Return details on an individual team. |
| PUT | /api/0/teams/{organization_id_or_slug}/{team_id_or_slug}/ | Update various attributes and configurable settings for the given |
| DELETE | /api/0/teams/{organization_id_or_slug}/{team_id_or_slug}/ | Schedules a team for deletion. |
| POST | /api/0/teams/{organization_id_or_slug}/{team_id_or_slug}/external-teams/ | Link a team from an external provider to a Sentry team. |
| PUT | /api/0/teams/{organization_id_or_slug}/{team_id_or_slug}/external-teams/{external_team_id}/ | Update a team in an external provider that is currently linked to a Sentry team. |
| DELETE | /api/0/teams/{organization_id_or_slug}/{team_id_or_slug}/external-teams/{external_team_id}/ | Delete the link between a team from an external provider and a Sentry team. |
| GET | /api/0/teams/{organization_id_or_slug}/{team_id_or_slug}/members/ | List all members on a team. |
| GET | /api/0/teams/{organization_id_or_slug}/{team_id_or_slug}/projects/ | Return a list of projects bound to a team. |
| POST | /api/0/teams/{organization_id_or_slug}/{team_id_or_slug}/projects/ | Create a new project bound to a team. |
| GET | /api/0/organizations/{organization_id_or_slug}/repos/ | Return a list of version control repositories for a given organization. |
| GET | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/files/dsyms/ | Retrieve a list of debug information files for a given project. |
| POST | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/files/dsyms/ | Upload a new debug information file for the given release. |
| DELETE | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/files/dsyms/ | Delete a debug information file for a given project. |
| GET | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/users/ | Return a list of users seen within this project. |
| GET | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/tags/{key}/values/ | Return a list of values associated with this key.  The `query` |
| GET | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/stats/ | Caution |
| GET | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/user-feedback/ | Return a list of user feedback items within this project. |
| POST | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/user-feedback/ | *This endpoint is DEPRECATED. We document it here for older SDKs and users who are still migrating to the [User Feedback Widget](https://docs.sentry.io/product/user-feedback/#user-feedback-widget) or [API](https://docs.sentry.io/platforms/javascript/user-feedback/#user-feedback-api)(multi-platform). If you are a new user, do not use this endpoint - unless you don't have a JS frontend, and your platform's SDK does not offer a feedback API.* |
| GET | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/hooks/ | Return a list of service hooks bound to a project. |
| POST | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/hooks/ | Register a new service hook on a project. |
| GET | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/hooks/{hook_id}/ | Return a service hook bound to a project. |
| PUT | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/hooks/{hook_id}/ | Update a service hook. |
| DELETE | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/hooks/{hook_id}/ | Remove a service hook. |
| GET | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/events/{event_id}/ | Return details on an individual event. |
| GET | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/issues/ | **Deprecated**: This endpoint has been replaced with the [Organization Issues endpoint](/api/events/list-an-organizations-issues/) which |
| PUT | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/issues/ | Bulk mutate various attributes on issues.  The list of issues to modify is given through the `id` query parameter.  It is repeated for each issue that should be modified. |
| DELETE | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/issues/ | Permanently remove the given issues. The list of issues to modify is given through the `id` query parameter.  It is repeated for each issue that should be removed. |
| GET | /api/0/organizations/{organization_id_or_slug}/issues/{issue_id}/tags/{key}/values/ | Returns a list of values associated with this key for an issue. |
| GET | /api/0/organizations/{organization_id_or_slug}/issues/{issue_id}/hashes/ | This endpoint lists an issue's hashes, which are the generated checksums used to aggregate individual events. |
| GET | /api/0/organizations/{organization_id_or_slug}/issues/{issue_id}/ | Return details on an individual issue. This returns the basic stats for the issue (title, last seen, first seen), some overall numbers (number of comments, user reports) as well as the summarized event data. |
| PUT | /api/0/organizations/{organization_id_or_slug}/issues/{issue_id}/ | Updates an individual issue's attributes.  Only the attributes submitted are modified. |
| DELETE | /api/0/organizations/{organization_id_or_slug}/issues/{issue_id}/ | Removes an individual issue. |
| GET | /api/0/organizations/{organization_id_or_slug}/releases/ | Return a list of releases for a given organization. |
| POST | /api/0/organizations/{organization_id_or_slug}/releases/ | Create a new release for the given organization.  Releases are used by |
| GET | /api/0/organizations/{organization_id_or_slug}/releases/{version}/files/ | Return a list of files for a given release. |
| POST | /api/0/organizations/{organization_id_or_slug}/releases/{version}/files/ | Upload a new file for the given release. |
| GET | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/releases/{version}/files/ | Return a list of files for a given release. |
| POST | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/releases/{version}/files/ | Upload a new file for the given release. |
| GET | /api/0/organizations/{organization_id_or_slug}/releases/{version}/files/{file_id}/ | Retrieve a file for a given release. |
| PUT | /api/0/organizations/{organization_id_or_slug}/releases/{version}/files/{file_id}/ | Update an organization release file. |
| DELETE | /api/0/organizations/{organization_id_or_slug}/releases/{version}/files/{file_id}/ | Delete a file for a given release. |
| GET | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/releases/{version}/files/{file_id}/ | Retrieve a file for a given release. |
| PUT | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/releases/{version}/files/{file_id}/ | Update a project release file. |
| DELETE | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/releases/{version}/files/{file_id}/ | Delete a file for a given release. |
| GET | /api/0/organizations/{organization_id_or_slug}/releases/{version}/commits/ | List an organization release's commits. |
| GET | /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/releases/{version}/commits/ | List a project release's commits. |
| GET | /api/0/organizations/{organization_id_or_slug}/releases/{version}/commitfiles/ | Retrieve files changed in a release's commits |
| GET | /api/0/organizations/{organization_id_or_slug}/sentry-app-installations/ | Return a list of integration platform installations for a given organization. |
| POST | /api/0/sentry-app-installations/{uuid}/external-issues/ | Create or update an external issue from an integration platform integration. |
| DELETE | /api/0/sentry-app-installations/{uuid}/external-issues/{external_issue_id}/ | Delete an external issue. |
| POST | /api/0/organizations/{organization_id_or_slug}/spike-protections/ | Enables Spike Protection feature for some of the projects within the organization. |
| DELETE | /api/0/organizations/{organization_id_or_slug}/spike-protections/ | Disables Spike Protection feature for some of the projects within the organization. |
| GET | /api/0/organizations/{organization_id_or_slug}/issues/{issue_id}/autofix/ | Retrieve the current detailed state of an issue fix process for a specific issue including: |
| POST | /api/0/organizations/{organization_id_or_slug}/issues/{issue_id}/autofix/ | Trigger a Seer Issue Fix run for a specific issue. |
| GET | /api/0/organizations/{organization_id_or_slug}/issues/{issue_id}/events/ | Return a list of error events bound to an issue |
| GET | /api/0/organizations/{organization_id_or_slug}/issues/{issue_id}/events/{event_id}/ | Retrieves the details of an issue event. |
| GET | /api/0/organizations/{organization_id_or_slug}/issues/{issue_id}/external-issues/ | Retrieve custom integration issue links for the given Sentry issue |
| GET | /api/0/organizations/{organization_id_or_slug}/issues/{issue_id}/tags/{key}/ | Return a list of values associated with this key for an issue. When paginated can return at most 1000 values. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search organizations?" -> GET /api/0/organizations/
- "Get organization details?" -> GET /api/0/organizations/{organization_id_or_slug}/
- "Update a organization?" -> PUT /api/0/organizations/{organization_id_or_slug}/
- "List all alert-rules?" -> GET /api/0/organizations/{organization_id_or_slug}/alert-rules/
- "Create a alert-rule?" -> POST /api/0/organizations/{organization_id_or_slug}/alert-rules/
- "Get alert-rule details?" -> GET /api/0/organizations/{organization_id_or_slug}/alert-rules/{alert_rule_id}/
- "Update a alert-rule?" -> PUT /api/0/organizations/{organization_id_or_slug}/alert-rules/{alert_rule_id}/
- "Delete a alert-rule?" -> DELETE /api/0/organizations/{organization_id_or_slug}/alert-rules/{alert_rule_id}/
- "List all integrations?" -> GET /api/0/organizations/{organization_id_or_slug}/config/integrations/
- "List all dashboards?" -> GET /api/0/organizations/{organization_id_or_slug}/dashboards/
- "Create a dashboard?" -> POST /api/0/organizations/{organization_id_or_slug}/dashboards/
- "Get dashboard details?" -> GET /api/0/organizations/{organization_id_or_slug}/dashboards/{dashboard_id}/
- "Update a dashboard?" -> PUT /api/0/organizations/{organization_id_or_slug}/dashboards/{dashboard_id}/
- "Delete a dashboard?" -> DELETE /api/0/organizations/{organization_id_or_slug}/dashboards/{dashboard_id}/
- "Search detectors?" -> GET /api/0/organizations/{organization_id_or_slug}/detectors/
- "Create a detector?" -> POST /api/0/organizations/{organization_id_or_slug}/detectors/
- "Get detector details?" -> GET /api/0/organizations/{organization_id_or_slug}/detectors/{detector_id}/
- "Update a detector?" -> PUT /api/0/organizations/{organization_id_or_slug}/detectors/{detector_id}/
- "Delete a detector?" -> DELETE /api/0/organizations/{organization_id_or_slug}/detectors/{detector_id}/
- "Search saved?" -> GET /api/0/organizations/{organization_id_or_slug}/discover/saved/
- "Create a saved?" -> POST /api/0/organizations/{organization_id_or_slug}/discover/saved/
- "Get saved details?" -> GET /api/0/organizations/{organization_id_or_slug}/discover/saved/{query_id}/
- "Update a saved?" -> PUT /api/0/organizations/{organization_id_or_slug}/discover/saved/{query_id}/
- "Delete a saved?" -> DELETE /api/0/organizations/{organization_id_or_slug}/discover/saved/{query_id}/
- "List all environments?" -> GET /api/0/organizations/{organization_id_or_slug}/environments/
- "Get eventid details?" -> GET /api/0/organizations/{organization_id_or_slug}/eventids/{event_id}/
- "Search events?" -> GET /api/0/organizations/{organization_id_or_slug}/events/
- "Search events-timeseries?" -> GET /api/0/organizations/{organization_id_or_slug}/events-timeseries/
- "Create a external-user?" -> POST /api/0/organizations/{organization_id_or_slug}/external-users/
- "Update a external-user?" -> PUT /api/0/organizations/{organization_id_or_slug}/external-users/{external_user_id}/
- "Delete a external-user?" -> DELETE /api/0/organizations/{organization_id_or_slug}/external-users/{external_user_id}/
- "List all forwarding?" -> GET /api/0/organizations/{organization_id_or_slug}/forwarding/
- "Create a forwarding?" -> POST /api/0/organizations/{organization_id_or_slug}/forwarding/
- "Update a forwarding?" -> PUT /api/0/organizations/{organization_id_or_slug}/forwarding/{data_forwarder_id}/
- "Delete a forwarding?" -> DELETE /api/0/organizations/{organization_id_or_slug}/forwarding/{data_forwarder_id}/
- "List all integrations?" -> GET /api/0/organizations/{organization_id_or_slug}/integrations/
- "Get integration details?" -> GET /api/0/organizations/{organization_id_or_slug}/integrations/{integration_id}/
- "Delete a integration?" -> DELETE /api/0/organizations/{organization_id_or_slug}/integrations/{integration_id}/
- "Search issues?" -> GET /api/0/organizations/{organization_id_or_slug}/issues/
- "List all members?" -> GET /api/0/organizations/{organization_id_or_slug}/members/
- "Create a member?" -> POST /api/0/organizations/{organization_id_or_slug}/members/
- "Get member details?" -> GET /api/0/organizations/{organization_id_or_slug}/members/{member_id}/
- "Update a member?" -> PUT /api/0/organizations/{organization_id_or_slug}/members/{member_id}/
- "Delete a member?" -> DELETE /api/0/organizations/{organization_id_or_slug}/members/{member_id}/
- "Update a team?" -> PUT /api/0/organizations/{organization_id_or_slug}/members/{member_id}/teams/{team_id_or_slug}/
- "Delete a team?" -> DELETE /api/0/organizations/{organization_id_or_slug}/members/{member_id}/teams/{team_id_or_slug}/
- "List all monitors?" -> GET /api/0/organizations/{organization_id_or_slug}/monitors/
- "Create a monitor?" -> POST /api/0/organizations/{organization_id_or_slug}/monitors/
- "Get monitor details?" -> GET /api/0/organizations/{organization_id_or_slug}/monitors/{monitor_id_or_slug}/
- "Update a monitor?" -> PUT /api/0/organizations/{organization_id_or_slug}/monitors/{monitor_id_or_slug}/
- "Delete a monitor?" -> DELETE /api/0/organizations/{organization_id_or_slug}/monitors/{monitor_id_or_slug}/
- "List all checkins?" -> GET /api/0/organizations/{organization_id_or_slug}/monitors/{monitor_id_or_slug}/checkins/
- "List all actions?" -> GET /api/0/organizations/{organization_id_or_slug}/notifications/actions/
- "Create a action?" -> POST /api/0/organizations/{organization_id_or_slug}/notifications/actions/
- "Get action details?" -> GET /api/0/organizations/{organization_id_or_slug}/notifications/actions/{action_id}/
- "Update a action?" -> PUT /api/0/organizations/{organization_id_or_slug}/notifications/actions/{action_id}/
- "Delete a action?" -> DELETE /api/0/organizations/{organization_id_or_slug}/notifications/actions/{action_id}/
- "List all install-details?" -> GET /api/0/organizations/{organization_id_or_slug}/preprodartifacts/{artifact_id}/install-details/
- "List all size-analysis?" -> GET /api/0/organizations/{organization_id_or_slug}/preprodartifacts/{artifact_id}/size-analysis/
- "List all repositories?" -> GET /api/0/organizations/{organization_id_or_slug}/prevent/owner/{owner}/repositories/
- "List all sync?" -> GET /api/0/organizations/{organization_id_or_slug}/prevent/owner/{owner}/repositories/sync/
- "Create a sync?" -> POST /api/0/organizations/{organization_id_or_slug}/prevent/owner/{owner}/repositories/sync/
- "List all tokens?" -> GET /api/0/organizations/{organization_id_or_slug}/prevent/owner/{owner}/repositories/tokens/
- "Get repository details?" -> GET /api/0/organizations/{organization_id_or_slug}/prevent/owner/{owner}/repository/{repository}/
- "List all branches?" -> GET /api/0/organizations/{organization_id_or_slug}/prevent/owner/{owner}/repository/{repository}/branches/
- "List all test-results?" -> GET /api/0/organizations/{organization_id_or_slug}/prevent/owner/{owner}/repository/{repository}/test-results/
- "List all test-results-aggregates?" -> GET /api/0/organizations/{organization_id_or_slug}/prevent/owner/{owner}/repository/{repository}/test-results-aggregates/
- "List all test-suites?" -> GET /api/0/organizations/{organization_id_or_slug}/prevent/owner/{owner}/repository/{repository}/test-suites/
- "Create a regenerate?" -> POST /api/0/organizations/{organization_id_or_slug}/prevent/owner/{owner}/repository/{repository}/token/regenerate/
- "List all project-keys?" -> GET /api/0/organizations/{organization_id_or_slug}/project-keys/
- "List all projects?" -> GET /api/0/organizations/{organization_id_or_slug}/projects/
- "List all relay_usage?" -> GET /api/0/organizations/{organization_id_or_slug}/relay_usage/
- "List all release-threshold-statuses?" -> GET /api/0/organizations/{organization_id_or_slug}/release-threshold-statuses/
- "Search releases?" -> GET /api/0/organizations/{organization_id_or_slug}/releases/{version}/
- "Update a release?" -> PUT /api/0/organizations/{organization_id_or_slug}/releases/{version}/
- "Delete a release?" -> DELETE /api/0/organizations/{organization_id_or_slug}/releases/{version}/
- "List all deploys?" -> GET /api/0/organizations/{organization_id_or_slug}/releases/{version}/deploys/
- "Create a deploy?" -> POST /api/0/organizations/{organization_id_or_slug}/releases/{version}/deploys/
- "Search replay-count?" -> GET /api/0/organizations/{organization_id_or_slug}/replay-count/
- "Search replay-selectors?" -> GET /api/0/organizations/{organization_id_or_slug}/replay-selectors/
- "Search replays?" -> GET /api/0/organizations/{organization_id_or_slug}/replays/
- "Search replays?" -> GET /api/0/organizations/{organization_id_or_slug}/replays/{replay_id}/
- "List all commits?" -> GET /api/0/organizations/{organization_id_or_slug}/repos/{repo_id}/commits/
- "List all Groups?" -> GET /api/0/organizations/{organization_id_or_slug}/scim/v2/Groups
- "Create a Group?" -> POST /api/0/organizations/{organization_id_or_slug}/scim/v2/Groups
- "Get Group details?" -> GET /api/0/organizations/{organization_id_or_slug}/scim/v2/Groups/{team_id_or_slug}
- "Partially update a Group?" -> PATCH /api/0/organizations/{organization_id_or_slug}/scim/v2/Groups/{team_id_or_slug}
- "Delete a Group?" -> DELETE /api/0/organizations/{organization_id_or_slug}/scim/v2/Groups/{team_id_or_slug}
- "List all Users?" -> GET /api/0/organizations/{organization_id_or_slug}/scim/v2/Users
- "Create a User?" -> POST /api/0/organizations/{organization_id_or_slug}/scim/v2/Users
- "Get User details?" -> GET /api/0/organizations/{organization_id_or_slug}/scim/v2/Users/{member_id}
- "Partially update a User?" -> PATCH /api/0/organizations/{organization_id_or_slug}/scim/v2/Users/{member_id}
- "Delete a User?" -> DELETE /api/0/organizations/{organization_id_or_slug}/scim/v2/Users/{member_id}
- "List all sentry-apps?" -> GET /api/0/organizations/{organization_id_or_slug}/sentry-apps/
- "Search sessions?" -> GET /api/0/organizations/{organization_id_or_slug}/sessions/
- "Get shortid details?" -> GET /api/0/organizations/{organization_id_or_slug}/shortids/{issue_id}/
- "List all stats-summary?" -> GET /api/0/organizations/{organization_id_or_slug}/stats-summary/
- "List all stats_v2?" -> GET /api/0/organizations/{organization_id_or_slug}/stats_v2/
- "List all teams?" -> GET /api/0/organizations/{organization_id_or_slug}/teams/
- "Create a team?" -> POST /api/0/organizations/{organization_id_or_slug}/teams/
- "List all user-teams?" -> GET /api/0/organizations/{organization_id_or_slug}/user-teams/
- "Search workflows?" -> GET /api/0/organizations/{organization_id_or_slug}/workflows/
- "Create a workflow?" -> POST /api/0/organizations/{organization_id_or_slug}/workflows/
- "Get workflow details?" -> GET /api/0/organizations/{organization_id_or_slug}/workflows/{workflow_id}/
- "Update a workflow?" -> PUT /api/0/organizations/{organization_id_or_slug}/workflows/{workflow_id}/
- "Delete a workflow?" -> DELETE /api/0/organizations/{organization_id_or_slug}/workflows/{workflow_id}/
- "Get project details?" -> GET /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/
- "Update a project?" -> PUT /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/
- "Delete a project?" -> DELETE /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/
- "List all environments?" -> GET /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/environments/
- "Get environment details?" -> GET /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/environments/{environment}/
- "Update a environment?" -> PUT /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/environments/{environment}/
- "List all events?" -> GET /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/events/
- "List all source-map-debug?" -> GET /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/events/{event_id}/source-map-debug/
- "List all filters?" -> GET /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/filters/
- "Update a filter?" -> PUT /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/filters/{filter_id}/
- "List all keys?" -> GET /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/keys/
- "Create a key?" -> POST /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/keys/
- "Get key details?" -> GET /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/keys/{key_id}/
- "Update a key?" -> PUT /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/keys/{key_id}/
- "Delete a key?" -> DELETE /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/keys/{key_id}/
- "List all members?" -> GET /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/members/
- "Get monitor details?" -> GET /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/monitors/{monitor_id_or_slug}/
- "Update a monitor?" -> PUT /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/monitors/{monitor_id_or_slug}/
- "Delete a monitor?" -> DELETE /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/monitors/{monitor_id_or_slug}/
- "List all checkins?" -> GET /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/monitors/{monitor_id_or_slug}/checkins/
- "List all ownership?" -> GET /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/ownership/
- "List all latest?" -> GET /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/preprodartifacts/build-distribution/latest/
- "Delete a replay?" -> DELETE /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/replays/{replay_id}/
- "Search clicks?" -> GET /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/replays/{replay_id}/clicks/
- "List all recording-segments?" -> GET /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/replays/{replay_id}/recording-segments/
- "Get recording-segment details?" -> GET /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/replays/{replay_id}/recording-segments/{segment_id}/
- "List all viewed-by?" -> GET /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/replays/{replay_id}/viewed-by/
- "List all rules?" -> GET /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/rules/
- "Create a rule?" -> POST /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/rules/
- "Get rule details?" -> GET /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/rules/{rule_id}/
- "Update a rule?" -> PUT /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/rules/{rule_id}/
- "Delete a rule?" -> DELETE /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/rules/{rule_id}/
- "List all symbol-sources?" -> GET /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/symbol-sources/
- "Create a symbol-source?" -> POST /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/symbol-sources/
- "List all teams?" -> GET /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/teams/
- "Delete a team?" -> DELETE /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/teams/{team_id_or_slug}/
- "List all models?" -> GET /api/0/seer/models/
- "Get sentry-app details?" -> GET /api/0/sentry-apps/{sentry_app_id_or_slug}/
- "Update a sentry-app?" -> PUT /api/0/sentry-apps/{sentry_app_id_or_slug}/
- "Delete a sentry-app?" -> DELETE /api/0/sentry-apps/{sentry_app_id_or_slug}/
- "Get team details?" -> GET /api/0/teams/{organization_id_or_slug}/{team_id_or_slug}/
- "Update a team?" -> PUT /api/0/teams/{organization_id_or_slug}/{team_id_or_slug}/
- "Delete a team?" -> DELETE /api/0/teams/{organization_id_or_slug}/{team_id_or_slug}/
- "Create a external-team?" -> POST /api/0/teams/{organization_id_or_slug}/{team_id_or_slug}/external-teams/
- "Update a external-team?" -> PUT /api/0/teams/{organization_id_or_slug}/{team_id_or_slug}/external-teams/{external_team_id}/
- "Delete a external-team?" -> DELETE /api/0/teams/{organization_id_or_slug}/{team_id_or_slug}/external-teams/{external_team_id}/
- "List all members?" -> GET /api/0/teams/{organization_id_or_slug}/{team_id_or_slug}/members/
- "List all projects?" -> GET /api/0/teams/{organization_id_or_slug}/{team_id_or_slug}/projects/
- "Create a project?" -> POST /api/0/teams/{organization_id_or_slug}/{team_id_or_slug}/projects/
- "List all repos?" -> GET /api/0/organizations/{organization_id_or_slug}/repos/
- "List all dsyms?" -> GET /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/files/dsyms/
- "Create a dsym?" -> POST /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/files/dsyms/
- "Search users?" -> GET /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/users/
- "List all values?" -> GET /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/tags/{key}/values/
- "List all stats?" -> GET /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/stats/
- "List all user-feedback?" -> GET /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/user-feedback/
- "Create a user-feedback?" -> POST /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/user-feedback/
- "List all hooks?" -> GET /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/hooks/
- "Create a hook?" -> POST /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/hooks/
- "Get hook details?" -> GET /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/hooks/{hook_id}/
- "Update a hook?" -> PUT /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/hooks/{hook_id}/
- "Delete a hook?" -> DELETE /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/hooks/{hook_id}/
- "Get event details?" -> GET /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/events/{event_id}/
- "Search issues?" -> GET /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/issues/
- "List all values?" -> GET /api/0/organizations/{organization_id_or_slug}/issues/{issue_id}/tags/{key}/values/
- "List all hashes?" -> GET /api/0/organizations/{organization_id_or_slug}/issues/{issue_id}/hashes/
- "Get issue details?" -> GET /api/0/organizations/{organization_id_or_slug}/issues/{issue_id}/
- "Update a issue?" -> PUT /api/0/organizations/{organization_id_or_slug}/issues/{issue_id}/
- "Delete a issue?" -> DELETE /api/0/organizations/{organization_id_or_slug}/issues/{issue_id}/
- "Search releases?" -> GET /api/0/organizations/{organization_id_or_slug}/releases/
- "Create a release?" -> POST /api/0/organizations/{organization_id_or_slug}/releases/
- "List all files?" -> GET /api/0/organizations/{organization_id_or_slug}/releases/{version}/files/
- "Create a file?" -> POST /api/0/organizations/{organization_id_or_slug}/releases/{version}/files/
- "List all files?" -> GET /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/releases/{version}/files/
- "Create a file?" -> POST /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/releases/{version}/files/
- "Get file details?" -> GET /api/0/organizations/{organization_id_or_slug}/releases/{version}/files/{file_id}/
- "Update a file?" -> PUT /api/0/organizations/{organization_id_or_slug}/releases/{version}/files/{file_id}/
- "Delete a file?" -> DELETE /api/0/organizations/{organization_id_or_slug}/releases/{version}/files/{file_id}/
- "Get file details?" -> GET /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/releases/{version}/files/{file_id}/
- "Update a file?" -> PUT /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/releases/{version}/files/{file_id}/
- "Delete a file?" -> DELETE /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/releases/{version}/files/{file_id}/
- "List all commits?" -> GET /api/0/organizations/{organization_id_or_slug}/releases/{version}/commits/
- "List all commits?" -> GET /api/0/projects/{organization_id_or_slug}/{project_id_or_slug}/releases/{version}/commits/
- "List all commitfiles?" -> GET /api/0/organizations/{organization_id_or_slug}/releases/{version}/commitfiles/
- "List all sentry-app-installations?" -> GET /api/0/organizations/{organization_id_or_slug}/sentry-app-installations/
- "Create a external-issue?" -> POST /api/0/sentry-app-installations/{uuid}/external-issues/
- "Delete a external-issue?" -> DELETE /api/0/sentry-app-installations/{uuid}/external-issues/{external_issue_id}/
- "Create a spike-protection?" -> POST /api/0/organizations/{organization_id_or_slug}/spike-protections/
- "List all autofix?" -> GET /api/0/organizations/{organization_id_or_slug}/issues/{issue_id}/autofix/
- "Create a autofix?" -> POST /api/0/organizations/{organization_id_or_slug}/issues/{issue_id}/autofix/
- "Search events?" -> GET /api/0/organizations/{organization_id_or_slug}/issues/{issue_id}/events/
- "Get event details?" -> GET /api/0/organizations/{organization_id_or_slug}/issues/{issue_id}/events/{event_id}/
- "List all external-issues?" -> GET /api/0/organizations/{organization_id_or_slug}/issues/{issue_id}/external-issues/
- "Get tag details?" -> GET /api/0/organizations/{organization_id_or_slug}/issues/{issue_id}/tags/{key}/
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
