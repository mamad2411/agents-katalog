---
name: app-center-client
description: "App Center Client API skill. Use when working with App Center Client for v0.1. Covers 265 endpoints."
version: 1.0.0
generator: lapsh
---

# App Center Client
API version: v0.1

## Auth
ApiKey X-API-Token in header | basic

## Base URL
https://api.appcenter.ms/

## Setup
1. Set your API key in the appropriate header
2. GET /v0.1/user/notifications/emailSettings -- verify access
3. POST /v0.1/users/{user_id}/devices/register -- create first register

## Endpoints

265 endpoints across 1 groups. See references/api-spec.lap for full details.

### v0.1
| Method | Path | Description |
|--------|------|-------------|
| POST | /v0.1/users/{user_id}/devices/register | Registers a user for an existing device |
| GET | /v0.1/user/notifications/emailSettings | Get Default email notification settings for the user |
| GET | /v0.1/user/metadata/optimizely |  |
| POST | /v0.1/user/invitations/orgs/{invitation_token}/reject | Rejects a pending organization invitation |
| POST | /v0.1/user/invitations/orgs/{invitation_token}/accept | Accepts a pending organization invitation for the specified user |
| POST | /v0.1/user/invitations/distribution_groups/accept | Accepts all pending invitations to distribution groups for the specified user |
| POST | /v0.1/user/invitations/apps/{invitation_token}/reject | Rejects a pending invitation for the specified user |
| POST | /v0.1/user/invitations/apps/{invitation_token}/accept | Accepts a pending invitation for the specified user |
| GET | /v0.1/user/export/serviceConnections | Gets all service connections of the service type for GDPR export. |
| POST | /v0.1/user/dsr/export/{token}/cancel |  |
| GET | /v0.1/user/dsr/export/{token} |  |
| POST | /v0.1/user/dsr/export |  |
| POST | /v0.1/user/dsr/delete/{token}/cancel |  |
| GET | /v0.1/user/dsr/delete/{token} |  |
| POST | /v0.1/user/dsr/delete |  |
| GET | /v0.1/user/devices/{device_udid} | Returns the device details. |
| DELETE | /v0.1/user/devices/{device_udid} | Removes an existing device from a user |
| GET | /v0.1/user/devices | Returns all devices associated with the given user. |
| GET | /v0.1/user | Returns the user profile data |
| PATCH | /v0.1/user | Updates the user profile and returns the updated user data |
| GET | /v0.1/sdk/apps/{app_secret}/releases/{release_hash} | If 'latest' is not specified then it will return the specified release if it's enabled. If 'latest' is specified, regardless of whether a release hash is provided, the latest enabled release is returned. |
| GET | /v0.1/sdk/apps/{app_secret}/releases/private/latest | Get the latest release distributed to a private group the given user is a member of for the given app. |
| GET | /v0.1/public/sparkle/apps/{app_secret} | Gets the sparkle feed of the releases that are distributed to all the public distribution groups. |
| GET | /v0.1/public/sdk/apps/{app_secret}/releases/{release_hash}/public_distribution_groups | Get all public distribution groups that a given release has been distributed to |
| GET | /v0.1/public/sdk/apps/{app_secret}/releases/latest | Get the latest public release for the given app. |
| GET | /v0.1/public/sdk/apps/{app_secret}/distribution_groups/{distribution_group_id}/releases/latest | Get a release with 'latest' for the given public group. |
| POST | /v0.1/public/apps/{owner_name}/{app_name}/install_analytics | Notify download(s) for the provided distribution release(s). |
| GET | /v0.1/public/apps/{app_id}/releases/{release_id}/ios_manifest | Returns the manifest.plist in XML format for installing the release on a device. Only available for iOS. |
| GET | /v0.1/orgs/{org_name}/users/{user_name}/apps | Get a user apps information from an organization by name |
| PATCH | /v0.1/orgs/{org_name}/users/{user_name} | Updates the given organization user |
| DELETE | /v0.1/orgs/{org_name}/users/{user_name} | Removes a user from an organization. |
| GET | /v0.1/orgs/{org_name}/users/{user_name} | Get a user information from an organization by name - if there is explicit permission return it, if not if not return highest implicit permission |
| GET | /v0.1/orgs/{org_name}/users | Returns a list of users that belong to an organization |
| GET | /v0.1/orgs/{org_name}/testers | Returns a unique list of users including the whole organization members plus testers in any shared group of that org |
| DELETE | /v0.1/orgs/{org_name}/teams/{team_name}/users/{user_name} | Removes a user from a team that is owned by an organization |
| GET | /v0.1/orgs/{org_name}/teams/{team_name}/users | Returns the users of a team which is owned by an organization |
| POST | /v0.1/orgs/{org_name}/teams/{team_name}/users | Adds a new user to a team that is owned by an organization |
| PATCH | /v0.1/orgs/{org_name}/teams/{team_name}/apps/{app_name} | Updates the permissions the team has to the app |
| DELETE | /v0.1/orgs/{org_name}/teams/{team_name}/apps/{app_name} | Removes an app from a team |
| POST | /v0.1/orgs/{org_name}/teams/{team_name}/apps | Adds an app to a team |
| GET | /v0.1/orgs/{org_name}/teams/{team_name}/apps | Returns the apps a team has access to |
| GET | /v0.1/orgs/{org_name}/teams/{team_name} | Returns the details of a single team |
| DELETE | /v0.1/orgs/{org_name}/teams/{team_name} | Deletes a single team |
| PATCH | /v0.1/orgs/{org_name}/teams/{team_name} | Updates a single team |
| GET | /v0.1/orgs/{org_name}/teams | Returns the list of all teams in this org |
| POST | /v0.1/orgs/{org_name}/teams | Creates a team and returns it |
| POST | /v0.1/orgs/{org_name}/invitations/{email}/revoke | Removes a user's invitation to an organization |
| POST | /v0.1/orgs/{org_name}/invitations/{email}/resend | Cancels an existing organization invitation for the user and sends a new one |
| PATCH | /v0.1/orgs/{org_name}/invitations/{email} | Allows the role of an invited user to be changed |
| POST | /v0.1/orgs/{org_name}/invitations | Invites a new or existing user to an organization |
| DELETE | /v0.1/orgs/{org_name}/invitations | Removes a user's invitation to an organization |
| GET | /v0.1/orgs/{org_name}/invitations | Gets the pending invitations for the organization |
| GET | /v0.1/orgs/{org_name}/distribution_groups_details | Returns a list of distribution groups with details for an organization |
| POST | /v0.1/orgs/{org_name}/distribution_groups/{distribution_group_name}/resend_invite | Resend shared distribution group invite notification to previously invited testers |
| POST | /v0.1/orgs/{org_name}/distribution_groups/{distribution_group_name}/members/bulk_delete | Delete testers from distribution group in an org |
| GET | /v0.1/orgs/{org_name}/distribution_groups/{distribution_group_name}/members | Returns a list of member in the distribution group specified |
| POST | /v0.1/orgs/{org_name}/distribution_groups/{distribution_group_name}/members | Accepts an array of user email addresses to get added to the specified group |
| POST | /v0.1/orgs/{org_name}/distribution_groups/{distribution_group_name}/apps/bulk_delete | Delete apps from distribution group in an org |
| GET | /v0.1/orgs/{org_name}/distribution_groups/{distribution_group_name}/apps | Get apps from a distribution group in an org |
| POST | /v0.1/orgs/{org_name}/distribution_groups/{distribution_group_name}/apps | Add apps to distribution group in an org |
| GET | /v0.1/orgs/{org_name}/distribution_groups/{distribution_group_name} | Returns a single distribution group in org for a given distribution group name |
| PATCH | /v0.1/orgs/{org_name}/distribution_groups/{distribution_group_name} | Update one given distribution group name in an org |
| DELETE | /v0.1/orgs/{org_name}/distribution_groups/{distribution_group_name} | Deletes a single distribution group from an org with a given distribution group name |
| POST | /v0.1/orgs/{org_name}/distribution_groups | Creates a disribution goup which can be shared across apps under an organization |
| GET | /v0.1/orgs/{org_name}/distribution_groups | Returns a list of distribution groups in the org specified |
| GET | /v0.1/orgs/{org_name}/azure_subscriptions | Returns a list of azure subscriptions for the organization |
| POST | /v0.1/orgs/{org_name}/avatar | Sets the organization avatar |
| DELETE | /v0.1/orgs/{org_name}/avatar | Deletes the uploaded organization avatar |
| POST | /v0.1/orgs/{org_name}/apps | Creates a new app for the organization and returns it to the caller |
| GET | /v0.1/orgs/{org_name}/apps | Returns a list of apps for the organization |
| GET | /v0.1/orgs/{org_name} | Returns the details of a single organization |
| PATCH | /v0.1/orgs/{org_name} | Returns a list of organizations the requesting user has access to |
| DELETE | /v0.1/orgs/{org_name} | Deletes a single organization |
| POST | /v0.1/orgs | Creates a new organization and returns it to the caller |
| GET | /v0.1/orgs | Returns a list of organizations the requesting user has access to |
| GET | /v0.1/invitations/sent | Returns all invitations sent by the caller |
| GET | /v0.1/azure_subscriptions | Returns a list of azure subscriptions for the user |
| GET | /v0.1/apps/{owner_name}/{app_name}/webhooks | Get web hooks configured for a particular app |
| GET | /v0.1/apps/{owner_name}/{app_name}/versions | Gets a list of application versions. |
| DELETE | /v0.1/apps/{owner_name}/{app_name}/users/{user_email} | Removes the user from the app |
| PATCH | /v0.1/apps/{owner_name}/{app_name}/users/{user_email} | Update user permission for the app |
| GET | /v0.1/apps/{owner_name}/{app_name}/users | Returns the users associated with the app specified with the given app name which belongs to the given owner. |
| GET | /v0.1/apps/{owner_name}/{app_name}/uploads/releases/{upload_id} | Get the current status of the release upload. |
| PATCH | /v0.1/apps/{owner_name}/{app_name}/uploads/releases/{upload_id} | Update the current status of the release upload. |
| POST | /v0.1/apps/{owner_name}/{app_name}/uploads/releases | Initiate a new release upload. This API is part of multi-step upload process. |
| POST | /v0.1/apps/{owner_name}/{app_name}/transfer_to_org | Transfers ownership of an app to a new organization |
| POST | /v0.1/apps/{owner_name}/{app_name}/transfer/{destination_owner_name} | Transfers ownership of an app to a different user or organization |
| DELETE | /v0.1/apps/{owner_name}/{app_name}/testers/{tester_id} | Delete the given tester from the all releases |
| GET | /v0.1/apps/{owner_name}/{app_name}/testers | Returns the testers associated with the app specified with the given app name which belongs to the given owner. |
| GET | /v0.1/apps/{owner_name}/{app_name}/teams | Returns the details of all teams that have access to the app. |
| GET | /v0.1/apps/{owner_name}/{app_name}/symbols/{symbol_id}/status | Returns a particular symbol by id (uuid) for the provided application |
| GET | /v0.1/apps/{owner_name}/{app_name}/symbols/{symbol_id}/location | Gets the URL to download the symbol |
| POST | /v0.1/apps/{owner_name}/{app_name}/symbols/{symbol_id}/ignore | Marks a symbol by id (uuid) as ignored |
| GET | /v0.1/apps/{owner_name}/{app_name}/symbols/{symbol_id} | Returns a particular symbol by id (uuid) for the provided application |
| GET | /v0.1/apps/{owner_name}/{app_name}/symbols | Returns the list of all symbols for the provided application |
| GET | /v0.1/apps/{owner_name}/{app_name}/symbol_uploads/{symbol_upload_id}/location | Gets the URL to download the symbol upload |
| GET | /v0.1/apps/{owner_name}/{app_name}/symbol_uploads/{symbol_upload_id} | Gets a symbol upload by id for the specified application |
| PATCH | /v0.1/apps/{owner_name}/{app_name}/symbol_uploads/{symbol_upload_id} | Commits or aborts the symbol upload process for a new set of symbols for the specified application |
| DELETE | /v0.1/apps/{owner_name}/{app_name}/symbol_uploads/{symbol_upload_id} | Deletes a symbol upload by id for the specified application |
| GET | /v0.1/apps/{owner_name}/{app_name}/symbol_uploads | Gets a list of all uploads for the specified application |
| POST | /v0.1/apps/{owner_name}/{app_name}/symbol_uploads | Begins the symbol upload process for a new set of symbols for the specified application |
| GET | /v0.1/apps/{owner_name}/{app_name}/store_service_status | Application specific store service status |
| GET | /v0.1/apps/{owner_name}/{app_name}/releases/{release_id}/update_devices/{resign_id} | Returns the resign status to the caller |
| PUT | /v0.1/apps/{owner_name}/{app_name}/releases/{release_id}/testers/{tester_id} | Update details about the specified tester associated with the release |
| DELETE | /v0.1/apps/{owner_name}/{app_name}/releases/{release_id}/testers/{tester_id} | Delete the given tester from the release |
| POST | /v0.1/apps/{owner_name}/{app_name}/releases/{release_id}/testers | Distributes a release to a user |
| DELETE | /v0.1/apps/{owner_name}/{app_name}/releases/{release_id}/stores/{store_id} | Delete the given distribution store from the release |
| POST | /v0.1/apps/{owner_name}/{app_name}/releases/{release_id}/stores | Distributes a release to a store |
| GET | /v0.1/apps/{owner_name}/{app_name}/releases/{release_id}/provisioning_profile | Return information about the provisioning profile. Only available for iOS. |
| PUT | /v0.1/apps/{owner_name}/{app_name}/releases/{release_id}/groups/{group_id} | Update details about the specified distribution group associated with the release |
| DELETE | /v0.1/apps/{owner_name}/{app_name}/releases/{release_id}/groups/{group_id} | Delete the given distribution group from the release |
| POST | /v0.1/apps/{owner_name}/{app_name}/releases/{release_id}/groups | Distributes a release to a group |
| GET | /v0.1/apps/{owner_name}/{app_name}/releases/{release_id} | Get a release with id `release_id`. If `release_id` is `latest`, return the latest release that was distributed to the current user (from all the distribution groups). |
| PUT | /v0.1/apps/{owner_name}/{app_name}/releases/{release_id} | Update details of a release. |
| PATCH | /v0.1/apps/{owner_name}/{app_name}/releases/{release_id} | Updates a release. |
| DELETE | /v0.1/apps/{owner_name}/{app_name}/releases/{release_id} | Deletes a release. |
| GET | /v0.1/apps/{owner_name}/{app_name}/releases/filter_by_tester | Return detailed information about releases avaiable to a tester. |
| GET | /v0.1/apps/{owner_name}/{app_name}/releases | Return basic information about releases. |
| GET | /v0.1/apps/{owner_name}/{app_name}/recent_releases | Get the latest release from every distribution group associated with an application. |
| GET | /v0.1/apps/{owner_name}/{app_name}/notifications/emailSettings | Get Email notification settings of user for a particular app |
| POST | /v0.1/apps/{owner_name}/{app_name}/invitations/{user_email} | Invites a new or existing user to an app |
| PATCH | /v0.1/apps/{owner_name}/{app_name}/invitations/{user_email} | Update pending invitation permission |
| DELETE | /v0.1/apps/{owner_name}/{app_name}/invitations/{user_email} | Removes a user's invitation to an app |
| POST | /v0.1/apps/{owner_name}/{app_name}/invitations | Invites a new or existing user to an app |
| GET | /v0.1/apps/{owner_name}/{app_name}/invitations | Gets the pending invitations for the app |
| POST | /v0.1/apps/{owner_name}/{app_name}/export_configurations_aks/{export_configuration_id}/enable | Enable export configuration. |
| POST | /v0.1/apps/{owner_name}/{app_name}/export_configurations_aks/{export_configuration_id}/disable | Disable export configuration. |
| GET | /v0.1/apps/{owner_name}/{app_name}/export_configurations_aks/{export_configuration_id} | Get export configuration. |
| PATCH | /v0.1/apps/{owner_name}/{app_name}/export_configurations_aks/{export_configuration_id} | Partially update export configuration. |
| DELETE | /v0.1/apps/{owner_name}/{app_name}/export_configurations_aks/{export_configuration_id} | Delete export configuration. |
| GET | /v0.1/apps/{owner_name}/{app_name}/export_configurations_aks | List export configurations. |
| POST | /v0.1/apps/{owner_name}/{app_name}/export_configurations_aks | Create new export configuration |
| GET | /v0.1/apps/{owner_name}/{app_name}/errors/{errorId}/sessionLogs | Get session logs by error ID |
| GET | /v0.1/apps/{owner_name}/{app_name}/errors/{errorId}/attachments/{attachmentId}/text | Error attachment text. |
| GET | /v0.1/apps/{owner_name}/{app_name}/errors/{errorId}/attachments/{attachmentId}/location | Error attachment location. |
| GET | /v0.1/apps/{owner_name}/{app_name}/errors/{errorId}/attachments | List error attachments. |
| GET | /v0.1/apps/{owner_name}/{app_name}/errors/search | Errors list based on search parameters |
| GET | /v0.1/apps/{owner_name}/{app_name}/errors/retention_settings | gets the retention settings in days |
| GET | /v0.1/apps/{owner_name}/{app_name}/errors/errorfreeDevicePercentages | Percentage of error-free devices by day in the time range based on the selected versions. If SingleErrorTypeParameter is not provided, defaults to handlederror. API will return -1 if crash devices is greater than active devices |
| GET | /v0.1/apps/{owner_name}/{app_name}/errors/errorGroups/{errorGroupId}/stacktrace | Gets the stack trace for the error group. |
| GET | /v0.1/apps/{owner_name}/{app_name}/errors/errorGroups/{errorGroupId}/operatingSystems | Top OSes of the selected error group. |
| GET | /v0.1/apps/{owner_name}/{app_name}/errors/errorGroups/{errorGroupId}/models | Top models of the selected error group. |
| GET | /v0.1/apps/{owner_name}/{app_name}/errors/errorGroups/{errorGroupId}/errors/{errorId}/stacktrace | Error Stacktrace details. |
| GET | /v0.1/apps/{owner_name}/{app_name}/errors/errorGroups/{errorGroupId}/errors/{errorId}/location | Error location. |
| GET | /v0.1/apps/{owner_name}/{app_name}/errors/errorGroups/{errorGroupId}/errors/{errorId}/download | Download details for a specific error. |
| GET | /v0.1/apps/{owner_name}/{app_name}/errors/errorGroups/{errorGroupId}/errors/{errorId} | Error details. |
| DELETE | /v0.1/apps/{owner_name}/{app_name}/errors/errorGroups/{errorGroupId}/errors/{errorId} | Delete a specific error and related attachments and blobs for an app. Searchable data will not be deleted immediately and may take up to 30 days. |
| GET | /v0.1/apps/{owner_name}/{app_name}/errors/errorGroups/{errorGroupId}/errors/latest | Latest error details. |
| GET | /v0.1/apps/{owner_name}/{app_name}/errors/errorGroups/{errorGroupId}/errors | Get all errors for group |
| GET | /v0.1/apps/{owner_name}/{app_name}/errors/errorGroups/{errorGroupId}/errorfreeDevicePercentages | Percentage of error-free devices by day in the time range. Api will return -1 if crash devices is greater than active devices |
| GET | /v0.1/apps/{owner_name}/{app_name}/errors/errorGroups/{errorGroupId}/errorCountsPerDay | Count of errors by day in the time range of the selected error group with selected version |
| GET | /v0.1/apps/{owner_name}/{app_name}/errors/errorGroups/{errorGroupId} | Error group details |
| PATCH | /v0.1/apps/{owner_name}/{app_name}/errors/errorGroups/{errorGroupId} | Update error group state |
| GET | /v0.1/apps/{owner_name}/{app_name}/errors/errorGroups/search | Error groups list based on search parameters |
| GET | /v0.1/apps/{owner_name}/{app_name}/errors/errorGroups | List of error groups |
| GET | /v0.1/apps/{owner_name}/{app_name}/errors/errorCountsPerDay | Count of crashes or errors by day in the time range based the selected versions. If SingleErrorTypeParameter is not provided, defaults to handlederror. |
| GET | /v0.1/apps/{owner_name}/{app_name}/errors/available_versions | Get all available versions in the time range. |
| GET | /v0.1/apps/{owner_name}/{app_name}/errors/availableAppBuilds | List of app builds |
| GET | /v0.1/apps/{owner_name}/{app_name}/distribution_stores/{store_name}/releases/{release_id}/realtimestatus | Return the Real time Status publishing of release from store. |
| GET | /v0.1/apps/{owner_name}/{app_name}/distribution_stores/{store_name}/releases/{release_id}/publish_logs | Returns publish logs for a particular release published to a particular store |
| GET | /v0.1/apps/{owner_name}/{app_name}/distribution_stores/{store_name}/releases/{release_id}/publish_error_details | Return the Error Details of release which failed in publishing. |
| GET | /v0.1/apps/{owner_name}/{app_name}/distribution_stores/{store_name}/releases/{release_id} | Return releases published in a store for releaseId and storeId |
| DELETE | /v0.1/apps/{owner_name}/{app_name}/distribution_stores/{store_name}/releases/{release_id} | delete the release with release Id |
| GET | /v0.1/apps/{owner_name}/{app_name}/distribution_stores/{store_name}/releases | Return all releases published  in a store |
| GET | /v0.1/apps/{owner_name}/{app_name}/distribution_stores/{store_name}/latest_release | Returns the latest release published in a store. |
| GET | /v0.1/apps/{owner_name}/{app_name}/distribution_stores/{store_name} | Return the store details for specified store name. |
| PATCH | /v0.1/apps/{owner_name}/{app_name}/distribution_stores/{store_name} | Update the store. |
| DELETE | /v0.1/apps/{owner_name}/{app_name}/distribution_stores/{store_name} | delete the store based on specific store name. |
| POST | /v0.1/apps/{owner_name}/{app_name}/distribution_stores | Create a new external store for the specified application. |
| GET | /v0.1/apps/{owner_name}/{app_name}/distribution_stores | Get all the store details from Storage store table for a particular application. |
| POST | /v0.1/apps/{owner_name}/{app_name}/distribution_groups/{distribution_group_name}/resend_invite | Resend distribution group app invite notification to previously invited testers |
| GET | /v0.1/apps/{owner_name}/{app_name}/distribution_groups/{distribution_group_name}/releases/{release_id} | Return detailed information about a distributed release in a given distribution group. |
| DELETE | /v0.1/apps/{owner_name}/{app_name}/distribution_groups/{distribution_group_name}/releases/{release_id} | Deletes a release with id 'release_id' in a given distribution group. |
| GET | /v0.1/apps/{owner_name}/{app_name}/distribution_groups/{distribution_group_name}/releases | Return basic information about distributed releases in a given distribution group. |
| POST | /v0.1/apps/{owner_name}/{app_name}/distribution_groups/{distribution_group_name}/members/bulk_delete | Remove the users from the distribution group |
| GET | /v0.1/apps/{owner_name}/{app_name}/distribution_groups/{distribution_group_name}/members | Returns a list of member details in the distribution group specified |
| POST | /v0.1/apps/{owner_name}/{app_name}/distribution_groups/{distribution_group_name}/members | Adds the members to the specified distribution group |
| GET | /v0.1/apps/{owner_name}/{app_name}/distribution_groups/{distribution_group_name}/devices/download_devices_list | Returns all devices associated with the given distribution group. |
| GET | /v0.1/apps/{owner_name}/{app_name}/distribution_groups/{distribution_group_name}/devices | Returns all devices associated with the given distribution group |
| GET | /v0.1/apps/{owner_name}/{app_name}/distribution_groups/{distribution_group_name} | Returns a single distribution group for a given distribution group name |
| PATCH | /v0.1/apps/{owner_name}/{app_name}/distribution_groups/{distribution_group_name} | Updates the attributes of distribution group |
| DELETE | /v0.1/apps/{owner_name}/{app_name}/distribution_groups/{distribution_group_name} | Deletes a distribution group |
| GET | /v0.1/apps/{owner_name}/{app_name}/distribution_groups | Returns a list of distribution groups in the app specified |
| POST | /v0.1/apps/{owner_name}/{app_name}/distribution_groups | Creates a new distribution group and returns it to the caller |
| GET | /v0.1/apps/{owner_name}/{app_name}/diagnostics/symbol_groups_info | Gets application level statistics for all missing symbol groups |
| GET | /v0.1/apps/{owner_name}/{app_name}/diagnostics/symbol_groups/{symbol_group_id} | Gets missing symbol crash group by its id |
| GET | /v0.1/apps/{owner_name}/{app_name}/diagnostics/symbol_groups | Gets top N (ordered by crash count) of crash groups by missing symbol |
| PUT | /v0.1/apps/{owner_name}/{app_name}/devices/block_logs/{install_id} | **Warning, this operation is not reversible.** |
| PUT | /v0.1/apps/{owner_name}/{app_name}/devices/block_logs | **Warning, this operation is not reversible.** |
| GET | /v0.1/apps/{owner_name}/{app_name}/crashes_info | Gets whether the application has any crashes. |
| GET | /v0.1/apps/{owner_name}/{app_name}/crashes/{crash_id}/session_logs | Get session logs by crash ID |
| GET | /v0.1/apps/{owner_name}/{app_name}/crashes/{crash_id}/attachments/{attachment_id}/text | Gets content of the text attachment. |
| GET | /v0.1/apps/{owner_name}/{app_name}/crashes/{crash_id}/attachments/{attachment_id}/location | Gets the URI location to download crash attachment. |
| GET | /v0.1/apps/{owner_name}/{app_name}/crashes/{crash_id}/attachments | Gets all attachments for a specific crash. |
| GET | /v0.1/apps/{owner_name}/{app_name}/crash_groups/{crash_group_id}/stacktrace | Gets a stacktrace for a specific crash. |
| GET | /v0.1/apps/{owner_name}/{app_name}/crash_groups/{crash_group_id}/crashes/{crash_id}/stacktrace | Gets a stacktrace for a specific crash. |
| GET | /v0.1/apps/{owner_name}/{app_name}/crash_groups/{crash_group_id}/crashes/{crash_id}/raw/location | Gets the URI location to download json of a specific crash. |
| GET | /v0.1/apps/{owner_name}/{app_name}/crash_groups/{crash_group_id}/crashes/{crash_id}/native/download | Gets the native log of a specific crash as a text attachment. |
| GET | /v0.1/apps/{owner_name}/{app_name}/crash_groups/{crash_group_id}/crashes/{crash_id}/native | Gets the native log of a specific crash. |
| GET | /v0.1/apps/{owner_name}/{app_name}/crash_groups/{crash_group_id}/crashes/{crash_id} | Gets a specific crash for an app. |
| DELETE | /v0.1/apps/{owner_name}/{app_name}/crash_groups/{crash_group_id}/crashes/{crash_id} | Delete a specific crash and related attachments and blobs for an app. |
| GET | /v0.1/apps/{owner_name}/{app_name}/crash_groups/{crash_group_id}/crashes | Gets all crashes of a group. |
| GET | /v0.1/apps/{owner_name}/{app_name}/crash_groups/{crash_group_id} | Gets a specific group. |
| PATCH | /v0.1/apps/{owner_name}/{app_name}/crash_groups/{crash_group_id} | Updates a group. |
| GET | /v0.1/apps/{owner_name}/{app_name}/crash_groups | Gets a list of crash groups and whether the list contains all available groups. |
| GET | /v0.1/apps/{owner_name}/{app_name}/bugtracker/crashGroup/{crash_group_id} | Get project issue related to a crash group |
| GET | /v0.1/apps/{owner_name}/{app_name}/bugtracker | Get bug tracker settings for a particular app |
| DELETE | /v0.1/apps/{owner_name}/{app_name}/azure_subscriptions/{azure_subscription_id} | Delete the azure subscriptions for the app |
| GET | /v0.1/apps/{owner_name}/{app_name}/azure_subscriptions | Returns a list of azure subscriptions for the app |
| POST | /v0.1/apps/{owner_name}/{app_name}/azure_subscriptions | Link azure subscription to an app |
| POST | /v0.1/apps/{owner_name}/{app_name}/avatar | Sets the app avatar |
| DELETE | /v0.1/apps/{owner_name}/{app_name}/avatar | Deletes the uploaded app avatar |
| GET | /v0.1/apps/{owner_name}/{app_name}/apple_test_flight_groups | Fetch all apple test flight groups |
| GET | /v0.1/apps/{owner_name}/{app_name}/apple_mapping | Get mapping of apple app to an existing app in apple store. |
| DELETE | /v0.1/apps/{owner_name}/{app_name}/apple_mapping | Delete mapping of apple app to an existing app in apple store. |
| POST | /v0.1/apps/{owner_name}/{app_name}/apple_mapping | Create a mapping for an existing app in apple store for the specified application. |
| DELETE | /v0.1/apps/{owner_name}/{app_name}/api_tokens/{api_token_id} | Delete the App Api Token object with the specific ID |
| GET | /v0.1/apps/{owner_name}/{app_name}/api_tokens | Returns App API tokens for the app |
| POST | /v0.1/apps/{owner_name}/{app_name}/api_tokens | Creates a new App API token |
| GET | /v0.1/apps/{owner_name}/{app_name}/analytics/versions | Count of active versions in the time range ordered by version. |
| GET | /v0.1/apps/{owner_name}/{app_name}/analytics/sessions_per_device | Count of sessions per device in the time range. |
| GET | /v0.1/apps/{owner_name}/{app_name}/analytics/session_durations_distribution | Gets session duration. |
| GET | /v0.1/apps/{owner_name}/{app_name}/analytics/session_counts | Count of sessions in the time range. |
| GET | /v0.1/apps/{owner_name}/{app_name}/analytics/places | Places in the time range. |
| GET | /v0.1/apps/{owner_name}/{app_name}/analytics/oses | OSes in the time range. |
| GET | /v0.1/apps/{owner_name}/{app_name}/analytics/models | Models in the time range. |
| GET | /v0.1/apps/{owner_name}/{app_name}/analytics/log_flow | Logs received between the specified start time and the current time. The API will return a maximum of 100 logs per call. |
| GET | /v0.1/apps/{owner_name}/{app_name}/analytics/languages | Languages in the time range. |
| GET | /v0.1/apps/{owner_name}/{app_name}/analytics/generic_log_flow | Logs received between the specified start time and the current time. The API will return a maximum of 100 logs per call. |
| GET | /v0.1/apps/{owner_name}/{app_name}/analytics/events/{event_name}/properties/{event_property_name}/counts | Event properties value counts during the time range in descending order. |
| GET | /v0.1/apps/{owner_name}/{app_name}/analytics/events/{event_name}/properties | Event properties. |
| GET | /v0.1/apps/{owner_name}/{app_name}/analytics/events/{event_name}/event_count | Count of events by interval in the time range. |
| GET | /v0.1/apps/{owner_name}/{app_name}/analytics/events/{event_name}/device_count | Count of devices for an event by interval in the time range. |
| GET | /v0.1/apps/{owner_name}/{app_name}/analytics/events/{event_name}/count_per_session | Count of events per session by interval in the time range. |
| GET | /v0.1/apps/{owner_name}/{app_name}/analytics/events/{event_name}/count_per_device | Count of events per device by interval in the time range. |
| DELETE | /v0.1/apps/{owner_name}/{app_name}/analytics/events/{event_name} | Delete the set of Events with the specified event names. |
| GET | /v0.1/apps/{owner_name}/{app_name}/analytics/events | Count of active events in the time range ordered by event. |
| DELETE | /v0.1/apps/{owner_name}/{app_name}/analytics/event_logs/{event_name} | Delete the set of Events with the specified event names. |
| POST | /v0.1/apps/{owner_name}/{app_name}/analytics/distribution/release_counts | Count of total downloads for the provided distribution releases. |
| GET | /v0.1/apps/{owner_name}/{app_name}/analytics/crashfree_device_percentages | Percentage of crash-free device by day in the time range based on the selected versions. Api will return -1 if crash devices is greater than active devices. |
| GET | /v0.1/apps/{owner_name}/{app_name}/analytics/crash_groups/{crash_group_id}/overall | Available for UWP apps only. |
| GET | /v0.1/apps/{owner_name}/{app_name}/analytics/crash_groups/{crash_group_id}/operating_systems | Available for UWP apps only. |
| GET | /v0.1/apps/{owner_name}/{app_name}/analytics/crash_groups/{crash_group_id}/models | Available for UWP apps only. |
| GET | /v0.1/apps/{owner_name}/{app_name}/analytics/crash_groups/{crash_group_id}/crash_counts | Available for UWP apps only. |
| POST | /v0.1/apps/{owner_name}/{app_name}/analytics/crash_groups | Overall crashes and affected users count of the selected crash groups with selected versions. |
| GET | /v0.1/apps/{owner_name}/{app_name}/analytics/crash_counts | Available for UWP apps only. |
| HEAD | /v0.1/apps/{owner_name}/{app_name}/analytics/audiences/{audience_name} | Returns whether audience definition exists. |
| DELETE | /v0.1/apps/{owner_name}/{app_name}/analytics/audiences/{audience_name} | Deletes audience definition. |
| GET | /v0.1/apps/{owner_name}/{app_name}/analytics/audiences/{audience_name} | Gets audience definition. |
| PUT | /v0.1/apps/{owner_name}/{app_name}/analytics/audiences/{audience_name} | Creates or updates audience definition. |
| GET | /v0.1/apps/{owner_name}/{app_name}/analytics/audiences/metadata/device_properties/{property_name}/values | Get list of device property values. |
| GET | /v0.1/apps/{owner_name}/{app_name}/analytics/audiences/metadata/device_properties | Get list of device properties. |
| GET | /v0.1/apps/{owner_name}/{app_name}/analytics/audiences/metadata/custom_properties | Get list of custom properties. |
| POST | /v0.1/apps/{owner_name}/{app_name}/analytics/audiences/definition/test | Tests audience definition. |
| GET | /v0.1/apps/{owner_name}/{app_name}/analytics/audiences | Get list of audiences. |
| GET | /v0.1/apps/{owner_name}/{app_name}/analytics/active_device_counts | Count of active devices by interval in the time range. |
| GET | /v0.1/apps/{owner_name}/{app_name} | Return a specific app with the given app name which belongs to the given owner. |
| PATCH | /v0.1/apps/{owner_name}/{app_name} | Partially updates a single app |
| DELETE | /v0.1/apps/{owner_name}/{app_name} | Delete an app |
| POST | /v0.1/apps | Creates a new app and returns it to the caller |
| GET | /v0.1/apps | Returns a list of apps |
| DELETE | /v0.1/api_tokens/{api_token_id} | Delete the user api_token object with the specific id |
| GET | /v0.1/api_tokens | Returns api tokens for the authenticated user |
| POST | /v0.1/api_tokens | Creates a new User API token |
| GET | /v0.1/administeredOrgs | Returns a list organizations in which the requesting user is an admin |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a register?" -> POST /v0.1/users/{user_id}/devices/register
- "List all emailSettings?" -> GET /v0.1/user/notifications/emailSettings
- "List all optimizely?" -> GET /v0.1/user/metadata/optimizely
- "Create a reject?" -> POST /v0.1/user/invitations/orgs/{invitation_token}/reject
- "Create a accept?" -> POST /v0.1/user/invitations/orgs/{invitation_token}/accept
- "Create a accept?" -> POST /v0.1/user/invitations/distribution_groups/accept
- "Create a reject?" -> POST /v0.1/user/invitations/apps/{invitation_token}/reject
- "Create a accept?" -> POST /v0.1/user/invitations/apps/{invitation_token}/accept
- "List all serviceConnections?" -> GET /v0.1/user/export/serviceConnections
- "Create a cancel?" -> POST /v0.1/user/dsr/export/{token}/cancel
- "Get export details?" -> GET /v0.1/user/dsr/export/{token}
- "Create a export?" -> POST /v0.1/user/dsr/export
- "Create a cancel?" -> POST /v0.1/user/dsr/delete/{token}/cancel
- "Get delete details?" -> GET /v0.1/user/dsr/delete/{token}
- "Create a delete?" -> POST /v0.1/user/dsr/delete
- "Get device details?" -> GET /v0.1/user/devices/{device_udid}
- "Delete a device?" -> DELETE /v0.1/user/devices/{device_udid}
- "List all devices?" -> GET /v0.1/user/devices
- "List all user?" -> GET /v0.1/user
- "Get release details?" -> GET /v0.1/sdk/apps/{app_secret}/releases/{release_hash}
- "List all latest?" -> GET /v0.1/sdk/apps/{app_secret}/releases/private/latest
- "Get app details?" -> GET /v0.1/public/sparkle/apps/{app_secret}
- "List all public_distribution_groups?" -> GET /v0.1/public/sdk/apps/{app_secret}/releases/{release_hash}/public_distribution_groups
- "List all latest?" -> GET /v0.1/public/sdk/apps/{app_secret}/releases/latest
- "List all latest?" -> GET /v0.1/public/sdk/apps/{app_secret}/distribution_groups/{distribution_group_id}/releases/latest
- "Create a install_analytic?" -> POST /v0.1/public/apps/{owner_name}/{app_name}/install_analytics
- "List all ios_manifest?" -> GET /v0.1/public/apps/{app_id}/releases/{release_id}/ios_manifest
- "List all apps?" -> GET /v0.1/orgs/{org_name}/users/{user_name}/apps
- "Partially update a user?" -> PATCH /v0.1/orgs/{org_name}/users/{user_name}
- "Delete a user?" -> DELETE /v0.1/orgs/{org_name}/users/{user_name}
- "Get user details?" -> GET /v0.1/orgs/{org_name}/users/{user_name}
- "List all users?" -> GET /v0.1/orgs/{org_name}/users
- "List all testers?" -> GET /v0.1/orgs/{org_name}/testers
- "Delete a user?" -> DELETE /v0.1/orgs/{org_name}/teams/{team_name}/users/{user_name}
- "List all users?" -> GET /v0.1/orgs/{org_name}/teams/{team_name}/users
- "Create a user?" -> POST /v0.1/orgs/{org_name}/teams/{team_name}/users
- "Partially update a app?" -> PATCH /v0.1/orgs/{org_name}/teams/{team_name}/apps/{app_name}
- "Delete a app?" -> DELETE /v0.1/orgs/{org_name}/teams/{team_name}/apps/{app_name}
- "Create a app?" -> POST /v0.1/orgs/{org_name}/teams/{team_name}/apps
- "List all apps?" -> GET /v0.1/orgs/{org_name}/teams/{team_name}/apps
- "Get team details?" -> GET /v0.1/orgs/{org_name}/teams/{team_name}
- "Delete a team?" -> DELETE /v0.1/orgs/{org_name}/teams/{team_name}
- "Partially update a team?" -> PATCH /v0.1/orgs/{org_name}/teams/{team_name}
- "List all teams?" -> GET /v0.1/orgs/{org_name}/teams
- "Create a team?" -> POST /v0.1/orgs/{org_name}/teams
- "Create a revoke?" -> POST /v0.1/orgs/{org_name}/invitations/{email}/revoke
- "Create a resend?" -> POST /v0.1/orgs/{org_name}/invitations/{email}/resend
- "Partially update a invitation?" -> PATCH /v0.1/orgs/{org_name}/invitations/{email}
- "Create a invitation?" -> POST /v0.1/orgs/{org_name}/invitations
- "List all invitations?" -> GET /v0.1/orgs/{org_name}/invitations
- "List all distribution_groups_details?" -> GET /v0.1/orgs/{org_name}/distribution_groups_details
- "Create a resend_invite?" -> POST /v0.1/orgs/{org_name}/distribution_groups/{distribution_group_name}/resend_invite
- "Create a bulk_delete?" -> POST /v0.1/orgs/{org_name}/distribution_groups/{distribution_group_name}/members/bulk_delete
- "List all members?" -> GET /v0.1/orgs/{org_name}/distribution_groups/{distribution_group_name}/members
- "Create a member?" -> POST /v0.1/orgs/{org_name}/distribution_groups/{distribution_group_name}/members
- "Create a bulk_delete?" -> POST /v0.1/orgs/{org_name}/distribution_groups/{distribution_group_name}/apps/bulk_delete
- "List all apps?" -> GET /v0.1/orgs/{org_name}/distribution_groups/{distribution_group_name}/apps
- "Create a app?" -> POST /v0.1/orgs/{org_name}/distribution_groups/{distribution_group_name}/apps
- "Get distribution_group details?" -> GET /v0.1/orgs/{org_name}/distribution_groups/{distribution_group_name}
- "Partially update a distribution_group?" -> PATCH /v0.1/orgs/{org_name}/distribution_groups/{distribution_group_name}
- "Delete a distribution_group?" -> DELETE /v0.1/orgs/{org_name}/distribution_groups/{distribution_group_name}
- "Create a distribution_group?" -> POST /v0.1/orgs/{org_name}/distribution_groups
- "List all distribution_groups?" -> GET /v0.1/orgs/{org_name}/distribution_groups
- "List all azure_subscriptions?" -> GET /v0.1/orgs/{org_name}/azure_subscriptions
- "Create a avatar?" -> POST /v0.1/orgs/{org_name}/avatar
- "Create a app?" -> POST /v0.1/orgs/{org_name}/apps
- "List all apps?" -> GET /v0.1/orgs/{org_name}/apps
- "Get org details?" -> GET /v0.1/orgs/{org_name}
- "Partially update a org?" -> PATCH /v0.1/orgs/{org_name}
- "Delete a org?" -> DELETE /v0.1/orgs/{org_name}
- "Create a org?" -> POST /v0.1/orgs
- "List all orgs?" -> GET /v0.1/orgs
- "List all sent?" -> GET /v0.1/invitations/sent
- "List all azure_subscriptions?" -> GET /v0.1/azure_subscriptions
- "List all webhooks?" -> GET /v0.1/apps/{owner_name}/{app_name}/webhooks
- "List all versions?" -> GET /v0.1/apps/{owner_name}/{app_name}/versions
- "Delete a user?" -> DELETE /v0.1/apps/{owner_name}/{app_name}/users/{user_email}
- "Partially update a user?" -> PATCH /v0.1/apps/{owner_name}/{app_name}/users/{user_email}
- "List all users?" -> GET /v0.1/apps/{owner_name}/{app_name}/users
- "Get release details?" -> GET /v0.1/apps/{owner_name}/{app_name}/uploads/releases/{upload_id}
- "Partially update a release?" -> PATCH /v0.1/apps/{owner_name}/{app_name}/uploads/releases/{upload_id}
- "Create a release?" -> POST /v0.1/apps/{owner_name}/{app_name}/uploads/releases
- "Create a transfer_to_org?" -> POST /v0.1/apps/{owner_name}/{app_name}/transfer_to_org
- "Delete a tester?" -> DELETE /v0.1/apps/{owner_name}/{app_name}/testers/{tester_id}
- "List all testers?" -> GET /v0.1/apps/{owner_name}/{app_name}/testers
- "List all teams?" -> GET /v0.1/apps/{owner_name}/{app_name}/teams
- "List all status?" -> GET /v0.1/apps/{owner_name}/{app_name}/symbols/{symbol_id}/status
- "List all location?" -> GET /v0.1/apps/{owner_name}/{app_name}/symbols/{symbol_id}/location
- "Create a ignore?" -> POST /v0.1/apps/{owner_name}/{app_name}/symbols/{symbol_id}/ignore
- "Get symbol details?" -> GET /v0.1/apps/{owner_name}/{app_name}/symbols/{symbol_id}
- "List all symbols?" -> GET /v0.1/apps/{owner_name}/{app_name}/symbols
- "List all location?" -> GET /v0.1/apps/{owner_name}/{app_name}/symbol_uploads/{symbol_upload_id}/location
- "Get symbol_upload details?" -> GET /v0.1/apps/{owner_name}/{app_name}/symbol_uploads/{symbol_upload_id}
- "Partially update a symbol_upload?" -> PATCH /v0.1/apps/{owner_name}/{app_name}/symbol_uploads/{symbol_upload_id}
- "Delete a symbol_upload?" -> DELETE /v0.1/apps/{owner_name}/{app_name}/symbol_uploads/{symbol_upload_id}
- "List all symbol_uploads?" -> GET /v0.1/apps/{owner_name}/{app_name}/symbol_uploads
- "Create a symbol_upload?" -> POST /v0.1/apps/{owner_name}/{app_name}/symbol_uploads
- "List all store_service_status?" -> GET /v0.1/apps/{owner_name}/{app_name}/store_service_status
- "Get update_device details?" -> GET /v0.1/apps/{owner_name}/{app_name}/releases/{release_id}/update_devices/{resign_id}
- "Update a tester?" -> PUT /v0.1/apps/{owner_name}/{app_name}/releases/{release_id}/testers/{tester_id}
- "Delete a tester?" -> DELETE /v0.1/apps/{owner_name}/{app_name}/releases/{release_id}/testers/{tester_id}
- "Create a tester?" -> POST /v0.1/apps/{owner_name}/{app_name}/releases/{release_id}/testers
- "Delete a store?" -> DELETE /v0.1/apps/{owner_name}/{app_name}/releases/{release_id}/stores/{store_id}
- "Create a store?" -> POST /v0.1/apps/{owner_name}/{app_name}/releases/{release_id}/stores
- "List all provisioning_profile?" -> GET /v0.1/apps/{owner_name}/{app_name}/releases/{release_id}/provisioning_profile
- "Update a group?" -> PUT /v0.1/apps/{owner_name}/{app_name}/releases/{release_id}/groups/{group_id}
- "Delete a group?" -> DELETE /v0.1/apps/{owner_name}/{app_name}/releases/{release_id}/groups/{group_id}
- "Create a group?" -> POST /v0.1/apps/{owner_name}/{app_name}/releases/{release_id}/groups
- "Get release details?" -> GET /v0.1/apps/{owner_name}/{app_name}/releases/{release_id}
- "Update a release?" -> PUT /v0.1/apps/{owner_name}/{app_name}/releases/{release_id}
- "Partially update a release?" -> PATCH /v0.1/apps/{owner_name}/{app_name}/releases/{release_id}
- "Delete a release?" -> DELETE /v0.1/apps/{owner_name}/{app_name}/releases/{release_id}
- "List all filter_by_tester?" -> GET /v0.1/apps/{owner_name}/{app_name}/releases/filter_by_tester
- "List all releases?" -> GET /v0.1/apps/{owner_name}/{app_name}/releases
- "List all recent_releases?" -> GET /v0.1/apps/{owner_name}/{app_name}/recent_releases
- "List all emailSettings?" -> GET /v0.1/apps/{owner_name}/{app_name}/notifications/emailSettings
- "Partially update a invitation?" -> PATCH /v0.1/apps/{owner_name}/{app_name}/invitations/{user_email}
- "Delete a invitation?" -> DELETE /v0.1/apps/{owner_name}/{app_name}/invitations/{user_email}
- "Create a invitation?" -> POST /v0.1/apps/{owner_name}/{app_name}/invitations
- "List all invitations?" -> GET /v0.1/apps/{owner_name}/{app_name}/invitations
- "Create a enable?" -> POST /v0.1/apps/{owner_name}/{app_name}/export_configurations_aks/{export_configuration_id}/enable
- "Create a disable?" -> POST /v0.1/apps/{owner_name}/{app_name}/export_configurations_aks/{export_configuration_id}/disable
- "Get export_configurations_ak details?" -> GET /v0.1/apps/{owner_name}/{app_name}/export_configurations_aks/{export_configuration_id}
- "Partially update a export_configurations_ak?" -> PATCH /v0.1/apps/{owner_name}/{app_name}/export_configurations_aks/{export_configuration_id}
- "Delete a export_configurations_ak?" -> DELETE /v0.1/apps/{owner_name}/{app_name}/export_configurations_aks/{export_configuration_id}
- "List all export_configurations_aks?" -> GET /v0.1/apps/{owner_name}/{app_name}/export_configurations_aks
- "Create a export_configurations_ak?" -> POST /v0.1/apps/{owner_name}/{app_name}/export_configurations_aks
- "List all sessionLogs?" -> GET /v0.1/apps/{owner_name}/{app_name}/errors/{errorId}/sessionLogs
- "List all text?" -> GET /v0.1/apps/{owner_name}/{app_name}/errors/{errorId}/attachments/{attachmentId}/text
- "List all location?" -> GET /v0.1/apps/{owner_name}/{app_name}/errors/{errorId}/attachments/{attachmentId}/location
- "List all attachments?" -> GET /v0.1/apps/{owner_name}/{app_name}/errors/{errorId}/attachments
- "Search search?" -> GET /v0.1/apps/{owner_name}/{app_name}/errors/search
- "List all retention_settings?" -> GET /v0.1/apps/{owner_name}/{app_name}/errors/retention_settings
- "List all errorfreeDevicePercentages?" -> GET /v0.1/apps/{owner_name}/{app_name}/errors/errorfreeDevicePercentages
- "List all stacktrace?" -> GET /v0.1/apps/{owner_name}/{app_name}/errors/errorGroups/{errorGroupId}/stacktrace
- "List all operatingSystems?" -> GET /v0.1/apps/{owner_name}/{app_name}/errors/errorGroups/{errorGroupId}/operatingSystems
- "List all models?" -> GET /v0.1/apps/{owner_name}/{app_name}/errors/errorGroups/{errorGroupId}/models
- "List all stacktrace?" -> GET /v0.1/apps/{owner_name}/{app_name}/errors/errorGroups/{errorGroupId}/errors/{errorId}/stacktrace
- "List all location?" -> GET /v0.1/apps/{owner_name}/{app_name}/errors/errorGroups/{errorGroupId}/errors/{errorId}/location
- "List all download?" -> GET /v0.1/apps/{owner_name}/{app_name}/errors/errorGroups/{errorGroupId}/errors/{errorId}/download
- "Get error details?" -> GET /v0.1/apps/{owner_name}/{app_name}/errors/errorGroups/{errorGroupId}/errors/{errorId}
- "Delete a error?" -> DELETE /v0.1/apps/{owner_name}/{app_name}/errors/errorGroups/{errorGroupId}/errors/{errorId}
- "List all latest?" -> GET /v0.1/apps/{owner_name}/{app_name}/errors/errorGroups/{errorGroupId}/errors/latest
- "List all errors?" -> GET /v0.1/apps/{owner_name}/{app_name}/errors/errorGroups/{errorGroupId}/errors
- "List all errorfreeDevicePercentages?" -> GET /v0.1/apps/{owner_name}/{app_name}/errors/errorGroups/{errorGroupId}/errorfreeDevicePercentages
- "List all errorCountsPerDay?" -> GET /v0.1/apps/{owner_name}/{app_name}/errors/errorGroups/{errorGroupId}/errorCountsPerDay
- "Get errorGroup details?" -> GET /v0.1/apps/{owner_name}/{app_name}/errors/errorGroups/{errorGroupId}
- "Partially update a errorGroup?" -> PATCH /v0.1/apps/{owner_name}/{app_name}/errors/errorGroups/{errorGroupId}
- "Search search?" -> GET /v0.1/apps/{owner_name}/{app_name}/errors/errorGroups/search
- "List all errorGroups?" -> GET /v0.1/apps/{owner_name}/{app_name}/errors/errorGroups
- "List all errorCountsPerDay?" -> GET /v0.1/apps/{owner_name}/{app_name}/errors/errorCountsPerDay
- "List all available_versions?" -> GET /v0.1/apps/{owner_name}/{app_name}/errors/available_versions
- "List all availableAppBuilds?" -> GET /v0.1/apps/{owner_name}/{app_name}/errors/availableAppBuilds
- "List all realtimestatus?" -> GET /v0.1/apps/{owner_name}/{app_name}/distribution_stores/{store_name}/releases/{release_id}/realtimestatus
- "List all publish_logs?" -> GET /v0.1/apps/{owner_name}/{app_name}/distribution_stores/{store_name}/releases/{release_id}/publish_logs
- "List all publish_error_details?" -> GET /v0.1/apps/{owner_name}/{app_name}/distribution_stores/{store_name}/releases/{release_id}/publish_error_details
- "Get release details?" -> GET /v0.1/apps/{owner_name}/{app_name}/distribution_stores/{store_name}/releases/{release_id}
- "Delete a release?" -> DELETE /v0.1/apps/{owner_name}/{app_name}/distribution_stores/{store_name}/releases/{release_id}
- "List all releases?" -> GET /v0.1/apps/{owner_name}/{app_name}/distribution_stores/{store_name}/releases
- "List all latest_release?" -> GET /v0.1/apps/{owner_name}/{app_name}/distribution_stores/{store_name}/latest_release
- "Get distribution_store details?" -> GET /v0.1/apps/{owner_name}/{app_name}/distribution_stores/{store_name}
- "Partially update a distribution_store?" -> PATCH /v0.1/apps/{owner_name}/{app_name}/distribution_stores/{store_name}
- "Delete a distribution_store?" -> DELETE /v0.1/apps/{owner_name}/{app_name}/distribution_stores/{store_name}
- "Create a distribution_store?" -> POST /v0.1/apps/{owner_name}/{app_name}/distribution_stores
- "List all distribution_stores?" -> GET /v0.1/apps/{owner_name}/{app_name}/distribution_stores
- "Create a resend_invite?" -> POST /v0.1/apps/{owner_name}/{app_name}/distribution_groups/{distribution_group_name}/resend_invite
- "Get release details?" -> GET /v0.1/apps/{owner_name}/{app_name}/distribution_groups/{distribution_group_name}/releases/{release_id}
- "Delete a release?" -> DELETE /v0.1/apps/{owner_name}/{app_name}/distribution_groups/{distribution_group_name}/releases/{release_id}
- "List all releases?" -> GET /v0.1/apps/{owner_name}/{app_name}/distribution_groups/{distribution_group_name}/releases
- "Create a bulk_delete?" -> POST /v0.1/apps/{owner_name}/{app_name}/distribution_groups/{distribution_group_name}/members/bulk_delete
- "List all members?" -> GET /v0.1/apps/{owner_name}/{app_name}/distribution_groups/{distribution_group_name}/members
- "Create a member?" -> POST /v0.1/apps/{owner_name}/{app_name}/distribution_groups/{distribution_group_name}/members
- "List all download_devices_list?" -> GET /v0.1/apps/{owner_name}/{app_name}/distribution_groups/{distribution_group_name}/devices/download_devices_list
- "List all devices?" -> GET /v0.1/apps/{owner_name}/{app_name}/distribution_groups/{distribution_group_name}/devices
- "Get distribution_group details?" -> GET /v0.1/apps/{owner_name}/{app_name}/distribution_groups/{distribution_group_name}
- "Partially update a distribution_group?" -> PATCH /v0.1/apps/{owner_name}/{app_name}/distribution_groups/{distribution_group_name}
- "Delete a distribution_group?" -> DELETE /v0.1/apps/{owner_name}/{app_name}/distribution_groups/{distribution_group_name}
- "List all distribution_groups?" -> GET /v0.1/apps/{owner_name}/{app_name}/distribution_groups
- "Create a distribution_group?" -> POST /v0.1/apps/{owner_name}/{app_name}/distribution_groups
- "List all symbol_groups_info?" -> GET /v0.1/apps/{owner_name}/{app_name}/diagnostics/symbol_groups_info
- "Get symbol_group details?" -> GET /v0.1/apps/{owner_name}/{app_name}/diagnostics/symbol_groups/{symbol_group_id}
- "List all symbol_groups?" -> GET /v0.1/apps/{owner_name}/{app_name}/diagnostics/symbol_groups
- "Update a block_log?" -> PUT /v0.1/apps/{owner_name}/{app_name}/devices/block_logs/{install_id}
- "List all crashes_info?" -> GET /v0.1/apps/{owner_name}/{app_name}/crashes_info
- "List all session_logs?" -> GET /v0.1/apps/{owner_name}/{app_name}/crashes/{crash_id}/session_logs
- "List all text?" -> GET /v0.1/apps/{owner_name}/{app_name}/crashes/{crash_id}/attachments/{attachment_id}/text
- "List all location?" -> GET /v0.1/apps/{owner_name}/{app_name}/crashes/{crash_id}/attachments/{attachment_id}/location
- "List all attachments?" -> GET /v0.1/apps/{owner_name}/{app_name}/crashes/{crash_id}/attachments
- "List all stacktrace?" -> GET /v0.1/apps/{owner_name}/{app_name}/crash_groups/{crash_group_id}/stacktrace
- "List all stacktrace?" -> GET /v0.1/apps/{owner_name}/{app_name}/crash_groups/{crash_group_id}/crashes/{crash_id}/stacktrace
- "List all location?" -> GET /v0.1/apps/{owner_name}/{app_name}/crash_groups/{crash_group_id}/crashes/{crash_id}/raw/location
- "List all download?" -> GET /v0.1/apps/{owner_name}/{app_name}/crash_groups/{crash_group_id}/crashes/{crash_id}/native/download
- "List all native?" -> GET /v0.1/apps/{owner_name}/{app_name}/crash_groups/{crash_group_id}/crashes/{crash_id}/native
- "Get crashe details?" -> GET /v0.1/apps/{owner_name}/{app_name}/crash_groups/{crash_group_id}/crashes/{crash_id}
- "Delete a crashe?" -> DELETE /v0.1/apps/{owner_name}/{app_name}/crash_groups/{crash_group_id}/crashes/{crash_id}
- "List all crashes?" -> GET /v0.1/apps/{owner_name}/{app_name}/crash_groups/{crash_group_id}/crashes
- "Get crash_group details?" -> GET /v0.1/apps/{owner_name}/{app_name}/crash_groups/{crash_group_id}
- "Partially update a crash_group?" -> PATCH /v0.1/apps/{owner_name}/{app_name}/crash_groups/{crash_group_id}
- "List all crash_groups?" -> GET /v0.1/apps/{owner_name}/{app_name}/crash_groups
- "Get crashGroup details?" -> GET /v0.1/apps/{owner_name}/{app_name}/bugtracker/crashGroup/{crash_group_id}
- "List all bugtracker?" -> GET /v0.1/apps/{owner_name}/{app_name}/bugtracker
- "Delete a azure_subscription?" -> DELETE /v0.1/apps/{owner_name}/{app_name}/azure_subscriptions/{azure_subscription_id}
- "List all azure_subscriptions?" -> GET /v0.1/apps/{owner_name}/{app_name}/azure_subscriptions
- "Create a azure_subscription?" -> POST /v0.1/apps/{owner_name}/{app_name}/azure_subscriptions
- "Create a avatar?" -> POST /v0.1/apps/{owner_name}/{app_name}/avatar
- "List all apple_test_flight_groups?" -> GET /v0.1/apps/{owner_name}/{app_name}/apple_test_flight_groups
- "List all apple_mapping?" -> GET /v0.1/apps/{owner_name}/{app_name}/apple_mapping
- "Create a apple_mapping?" -> POST /v0.1/apps/{owner_name}/{app_name}/apple_mapping
- "Delete a api_token?" -> DELETE /v0.1/apps/{owner_name}/{app_name}/api_tokens/{api_token_id}
- "List all api_tokens?" -> GET /v0.1/apps/{owner_name}/{app_name}/api_tokens
- "Create a api_token?" -> POST /v0.1/apps/{owner_name}/{app_name}/api_tokens
- "List all versions?" -> GET /v0.1/apps/{owner_name}/{app_name}/analytics/versions
- "List all sessions_per_device?" -> GET /v0.1/apps/{owner_name}/{app_name}/analytics/sessions_per_device
- "List all session_durations_distribution?" -> GET /v0.1/apps/{owner_name}/{app_name}/analytics/session_durations_distribution
- "List all session_counts?" -> GET /v0.1/apps/{owner_name}/{app_name}/analytics/session_counts
- "List all places?" -> GET /v0.1/apps/{owner_name}/{app_name}/analytics/places
- "List all oses?" -> GET /v0.1/apps/{owner_name}/{app_name}/analytics/oses
- "List all models?" -> GET /v0.1/apps/{owner_name}/{app_name}/analytics/models
- "List all log_flow?" -> GET /v0.1/apps/{owner_name}/{app_name}/analytics/log_flow
- "List all languages?" -> GET /v0.1/apps/{owner_name}/{app_name}/analytics/languages
- "List all generic_log_flow?" -> GET /v0.1/apps/{owner_name}/{app_name}/analytics/generic_log_flow
- "List all counts?" -> GET /v0.1/apps/{owner_name}/{app_name}/analytics/events/{event_name}/properties/{event_property_name}/counts
- "List all properties?" -> GET /v0.1/apps/{owner_name}/{app_name}/analytics/events/{event_name}/properties
- "List all event_count?" -> GET /v0.1/apps/{owner_name}/{app_name}/analytics/events/{event_name}/event_count
- "List all device_count?" -> GET /v0.1/apps/{owner_name}/{app_name}/analytics/events/{event_name}/device_count
- "List all count_per_session?" -> GET /v0.1/apps/{owner_name}/{app_name}/analytics/events/{event_name}/count_per_session
- "List all count_per_device?" -> GET /v0.1/apps/{owner_name}/{app_name}/analytics/events/{event_name}/count_per_device
- "Delete a event?" -> DELETE /v0.1/apps/{owner_name}/{app_name}/analytics/events/{event_name}
- "List all events?" -> GET /v0.1/apps/{owner_name}/{app_name}/analytics/events
- "Delete a event_log?" -> DELETE /v0.1/apps/{owner_name}/{app_name}/analytics/event_logs/{event_name}
- "Create a release_count?" -> POST /v0.1/apps/{owner_name}/{app_name}/analytics/distribution/release_counts
- "List all crashfree_device_percentages?" -> GET /v0.1/apps/{owner_name}/{app_name}/analytics/crashfree_device_percentages
- "List all overall?" -> GET /v0.1/apps/{owner_name}/{app_name}/analytics/crash_groups/{crash_group_id}/overall
- "List all operating_systems?" -> GET /v0.1/apps/{owner_name}/{app_name}/analytics/crash_groups/{crash_group_id}/operating_systems
- "List all models?" -> GET /v0.1/apps/{owner_name}/{app_name}/analytics/crash_groups/{crash_group_id}/models
- "List all crash_counts?" -> GET /v0.1/apps/{owner_name}/{app_name}/analytics/crash_groups/{crash_group_id}/crash_counts
- "Create a crash_group?" -> POST /v0.1/apps/{owner_name}/{app_name}/analytics/crash_groups
- "List all crash_counts?" -> GET /v0.1/apps/{owner_name}/{app_name}/analytics/crash_counts
- "Delete a audience?" -> DELETE /v0.1/apps/{owner_name}/{app_name}/analytics/audiences/{audience_name}
- "Get audience details?" -> GET /v0.1/apps/{owner_name}/{app_name}/analytics/audiences/{audience_name}
- "Update a audience?" -> PUT /v0.1/apps/{owner_name}/{app_name}/analytics/audiences/{audience_name}
- "List all values?" -> GET /v0.1/apps/{owner_name}/{app_name}/analytics/audiences/metadata/device_properties/{property_name}/values
- "List all device_properties?" -> GET /v0.1/apps/{owner_name}/{app_name}/analytics/audiences/metadata/device_properties
- "List all custom_properties?" -> GET /v0.1/apps/{owner_name}/{app_name}/analytics/audiences/metadata/custom_properties
- "Create a test?" -> POST /v0.1/apps/{owner_name}/{app_name}/analytics/audiences/definition/test
- "List all audiences?" -> GET /v0.1/apps/{owner_name}/{app_name}/analytics/audiences
- "List all active_device_counts?" -> GET /v0.1/apps/{owner_name}/{app_name}/analytics/active_device_counts
- "Get app details?" -> GET /v0.1/apps/{owner_name}/{app_name}
- "Partially update a app?" -> PATCH /v0.1/apps/{owner_name}/{app_name}
- "Delete a app?" -> DELETE /v0.1/apps/{owner_name}/{app_name}
- "Create a app?" -> POST /v0.1/apps
- "List all apps?" -> GET /v0.1/apps
- "Delete a api_token?" -> DELETE /v0.1/api_tokens/{api_token_id}
- "List all api_tokens?" -> GET /v0.1/api_tokens
- "Create a api_token?" -> POST /v0.1/api_tokens
- "List all administeredOrgs?" -> GET /v0.1/administeredOrgs
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object
- Error responses use types: <b>bad_request</b>, <b>forbidden</b>, <b>not_found</b>

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
