---
name: the-jira-cloud-platform-rest-api
description: "The Jira Cloud platform REST API skill. Use when working with The Jira Cloud platform REST for rest. Covers 619 endpoints."
version: 1.0.0
generator: lapsh
---

# The Jira Cloud platform REST API
API version: 1001.0.0-SNAPSHOT-2e55eec067fba5cfeec4fef1856e5d704bf42094

## Auth
OAuth2 | Bearer basic

## Base URL
https://your-domain.atlassian.net

## Setup
1. Set Authorization header with your Bearer token
2. GET /rest/api/3/announcementBanner -- verify access
3. POST /rest/api/3/app/field/context/configuration/list -- create first list

## Endpoints

619 endpoints across 1 groups. See references/api-spec.lap for full details.

### rest
| Method | Path | Description |
|--------|------|-------------|
| GET | /rest/api/3/announcementBanner | Get announcement banner configuration |
| PUT | /rest/api/3/announcementBanner | Update announcement banner configuration |
| POST | /rest/api/3/app/field/context/configuration/list | Bulk get custom field configurations |
| POST | /rest/api/3/app/field/value | Update custom fields |
| GET | /rest/api/3/app/field/{fieldIdOrKey}/context/configuration | Get custom field configurations |
| PUT | /rest/api/3/app/field/{fieldIdOrKey}/context/configuration | Update custom field configurations |
| PUT | /rest/api/3/app/field/{fieldIdOrKey}/value | Update custom field value |
| GET | /rest/api/3/application-properties | Get application property |
| GET | /rest/api/3/application-properties/advanced-settings | Get advanced settings |
| PUT | /rest/api/3/application-properties/{id} | Set application property |
| GET | /rest/api/3/applicationrole | Get all application roles |
| GET | /rest/api/3/applicationrole/{key} | Get application role |
| GET | /rest/api/3/attachment/content/{id} | Get attachment content |
| GET | /rest/api/3/attachment/meta | Get Jira attachment settings |
| GET | /rest/api/3/attachment/thumbnail/{id} | Get attachment thumbnail |
| DELETE | /rest/api/3/attachment/{id} | Delete attachment |
| GET | /rest/api/3/attachment/{id} | Get attachment metadata |
| GET | /rest/api/3/attachment/{id}/expand/human | Get all metadata for an expanded attachment |
| GET | /rest/api/3/attachment/{id}/expand/raw | Get contents metadata for an expanded attachment |
| GET | /rest/api/3/auditing/record | Get audit records |
| GET | /rest/api/3/avatar/{type}/system | Get system avatars by type |
| POST | /rest/api/3/bulk/issues/delete | Bulk delete issues |
| GET | /rest/api/3/bulk/issues/fields | Get bulk editable fields |
| POST | /rest/api/3/bulk/issues/fields | Bulk edit issues |
| POST | /rest/api/3/bulk/issues/move | Bulk move issues |
| GET | /rest/api/3/bulk/issues/transition | Get available transitions |
| POST | /rest/api/3/bulk/issues/transition | Bulk transition issue statuses |
| POST | /rest/api/3/bulk/issues/unwatch | Bulk unwatch issues |
| POST | /rest/api/3/bulk/issues/watch | Bulk watch issues |
| GET | /rest/api/3/bulk/queue/{taskId} | Get bulk issue operation progress |
| POST | /rest/api/3/changelog/bulkfetch | Bulk fetch changelogs |
| GET | /rest/api/3/classification-levels | Get all classification levels |
| POST | /rest/api/3/comment/list | Get comments by IDs |
| GET | /rest/api/3/comment/{commentId}/properties | Get comment property keys |
| DELETE | /rest/api/3/comment/{commentId}/properties/{propertyKey} | Delete comment property |
| GET | /rest/api/3/comment/{commentId}/properties/{propertyKey} | Get comment property |
| PUT | /rest/api/3/comment/{commentId}/properties/{propertyKey} | Set comment property |
| GET | /rest/api/3/component | Find components for projects |
| POST | /rest/api/3/component | Create component |
| DELETE | /rest/api/3/component/{id} | Delete component |
| GET | /rest/api/3/component/{id} | Get component |
| PUT | /rest/api/3/component/{id} | Update component |
| GET | /rest/api/3/component/{id}/relatedIssueCounts | Get component issues count |
| GET | /rest/api/3/config/fieldschemes | Get field schemes |
| POST | /rest/api/3/config/fieldschemes | Create field scheme |
| DELETE | /rest/api/3/config/fieldschemes/fields | Remove fields associated with field schemes |
| PUT | /rest/api/3/config/fieldschemes/fields | Update fields associated with field schemes |
| DELETE | /rest/api/3/config/fieldschemes/fields/parameters | Remove field parameters |
| PUT | /rest/api/3/config/fieldschemes/fields/parameters | Update field parameters |
| GET | /rest/api/3/config/fieldschemes/projects | Get projects with field schemes |
| PUT | /rest/api/3/config/fieldschemes/projects | Associate projects to field schemes |
| DELETE | /rest/api/3/config/fieldschemes/{id} | Delete a field scheme |
| GET | /rest/api/3/config/fieldschemes/{id} | Get field scheme |
| PUT | /rest/api/3/config/fieldschemes/{id} | Update field scheme |
| POST | /rest/api/3/config/fieldschemes/{id}/clone | Clone field scheme |
| GET | /rest/api/3/config/fieldschemes/{id}/fields | Search field scheme fields |
| GET | /rest/api/3/config/fieldschemes/{id}/fields/{fieldId}/parameters | Get field parameters |
| GET | /rest/api/3/config/fieldschemes/{id}/projects | Search field scheme projects |
| GET | /rest/api/3/configuration | Get global settings |
| GET | /rest/api/3/configuration/timetracking | Get selected time tracking provider |
| PUT | /rest/api/3/configuration/timetracking | Select time tracking provider |
| GET | /rest/api/3/configuration/timetracking/list | Get all time tracking providers |
| GET | /rest/api/3/configuration/timetracking/options | Get time tracking settings |
| PUT | /rest/api/3/configuration/timetracking/options | Set time tracking settings |
| GET | /rest/api/3/customFieldOption/{id} | Get custom field option |
| GET | /rest/api/3/dashboard | Get all dashboards |
| POST | /rest/api/3/dashboard | Create dashboard |
| PUT | /rest/api/3/dashboard/bulk/edit | Bulk edit dashboards |
| GET | /rest/api/3/dashboard/gadgets | Get available gadgets |
| GET | /rest/api/3/dashboard/search | Search for dashboards |
| GET | /rest/api/3/dashboard/{dashboardId}/gadget | Get gadgets |
| POST | /rest/api/3/dashboard/{dashboardId}/gadget | Add gadget to dashboard |
| DELETE | /rest/api/3/dashboard/{dashboardId}/gadget/{gadgetId} | Remove gadget from dashboard |
| PUT | /rest/api/3/dashboard/{dashboardId}/gadget/{gadgetId} | Update gadget on dashboard |
| GET | /rest/api/3/dashboard/{dashboardId}/items/{itemId}/properties | Get dashboard item property keys |
| DELETE | /rest/api/3/dashboard/{dashboardId}/items/{itemId}/properties/{propertyKey} | Delete dashboard item property |
| GET | /rest/api/3/dashboard/{dashboardId}/items/{itemId}/properties/{propertyKey} | Get dashboard item property |
| PUT | /rest/api/3/dashboard/{dashboardId}/items/{itemId}/properties/{propertyKey} | Set dashboard item property |
| DELETE | /rest/api/3/dashboard/{id} | Delete dashboard |
| GET | /rest/api/3/dashboard/{id} | Get dashboard |
| PUT | /rest/api/3/dashboard/{id} | Update dashboard |
| POST | /rest/api/3/dashboard/{id}/copy | Copy dashboard |
| GET | /rest/api/3/data-policy | Get data policy for the workspace |
| GET | /rest/api/3/data-policy/project | Get data policy for projects |
| GET | /rest/api/3/events | Get events |
| POST | /rest/api/3/expression/analyse | Analyse Jira expression |
| POST | /rest/api/3/expression/eval | Currently being removed. Evaluate Jira expression |
| POST | /rest/api/3/expression/evaluate | Evaluate Jira expression using enhanced search API |
| GET | /rest/api/3/field | Get fields |
| POST | /rest/api/3/field | Create custom field |
| DELETE | /rest/api/3/field/association | Remove associations |
| PUT | /rest/api/3/field/association | Create associations |
| GET | /rest/api/3/field/search | Get fields paginated |
| GET | /rest/api/3/field/search/trashed | Get fields in trash paginated |
| PUT | /rest/api/3/field/{fieldId} | Update custom field |
| GET | /rest/api/3/field/{fieldId}/context | Get custom field contexts |
| POST | /rest/api/3/field/{fieldId}/context | Create custom field context |
| GET | /rest/api/3/field/{fieldId}/context/defaultValue | Get custom field contexts default values |
| PUT | /rest/api/3/field/{fieldId}/context/defaultValue | Set custom field contexts default values |
| GET | /rest/api/3/field/{fieldId}/context/issuetypemapping | Get issue types for custom field context |
| POST | /rest/api/3/field/{fieldId}/context/mapping | Get custom field contexts for projects and issue types |
| GET | /rest/api/3/field/{fieldId}/context/projectmapping | Get project mappings for custom field context |
| DELETE | /rest/api/3/field/{fieldId}/context/{contextId} | Delete custom field context |
| PUT | /rest/api/3/field/{fieldId}/context/{contextId} | Update custom field context |
| PUT | /rest/api/3/field/{fieldId}/context/{contextId}/issuetype | Add issue types to context |
| POST | /rest/api/3/field/{fieldId}/context/{contextId}/issuetype/remove | Remove issue types from context |
| GET | /rest/api/3/field/{fieldId}/context/{contextId}/option | Get custom field options (context) |
| POST | /rest/api/3/field/{fieldId}/context/{contextId}/option | Create custom field options (context) |
| PUT | /rest/api/3/field/{fieldId}/context/{contextId}/option | Update custom field options (context) |
| PUT | /rest/api/3/field/{fieldId}/context/{contextId}/option/move | Reorder custom field options (context) |
| DELETE | /rest/api/3/field/{fieldId}/context/{contextId}/option/{optionId} | Delete custom field options (context) |
| DELETE | /rest/api/3/field/{fieldId}/context/{contextId}/option/{optionId}/issue | Replace custom field options |
| PUT | /rest/api/3/field/{fieldId}/context/{contextId}/project | Assign custom field context to projects |
| POST | /rest/api/3/field/{fieldId}/context/{contextId}/project/remove | Remove custom field context from projects |
| GET | /rest/api/3/field/{fieldId}/contexts | Get contexts for a field |
| GET | /rest/api/3/field/{fieldId}/screens | Get screens for a field |
| GET | /rest/api/3/field/{fieldKey}/option | Get all issue field options |
| POST | /rest/api/3/field/{fieldKey}/option | Create issue field option |
| GET | /rest/api/3/field/{fieldKey}/option/suggestions/edit | Get selectable issue field options |
| GET | /rest/api/3/field/{fieldKey}/option/suggestions/search | Get visible issue field options |
| DELETE | /rest/api/3/field/{fieldKey}/option/{optionId} | Delete issue field option |
| GET | /rest/api/3/field/{fieldKey}/option/{optionId} | Get issue field option |
| PUT | /rest/api/3/field/{fieldKey}/option/{optionId} | Update issue field option |
| DELETE | /rest/api/3/field/{fieldKey}/option/{optionId}/issue | Replace issue field option |
| DELETE | /rest/api/3/field/{id} | Delete custom field |
| POST | /rest/api/3/field/{id}/restore | Restore custom field from trash |
| POST | /rest/api/3/field/{id}/trash | Move custom field to trash |
| GET | /rest/api/3/fieldconfiguration | Get all field configurations |
| POST | /rest/api/3/fieldconfiguration | Create field configuration |
| DELETE | /rest/api/3/fieldconfiguration/{id} | Delete field configuration |
| PUT | /rest/api/3/fieldconfiguration/{id} | Update field configuration |
| GET | /rest/api/3/fieldconfiguration/{id}/fields | Get field configuration items |
| PUT | /rest/api/3/fieldconfiguration/{id}/fields | Update field configuration items |
| GET | /rest/api/3/fieldconfigurationscheme | Get all field configuration schemes |
| POST | /rest/api/3/fieldconfigurationscheme | Create field configuration scheme |
| GET | /rest/api/3/fieldconfigurationscheme/mapping | Get field configuration issue type items |
| GET | /rest/api/3/fieldconfigurationscheme/project | Get field configuration schemes for projects |
| PUT | /rest/api/3/fieldconfigurationscheme/project | Assign field configuration scheme to project |
| DELETE | /rest/api/3/fieldconfigurationscheme/{id} | Delete field configuration scheme |
| PUT | /rest/api/3/fieldconfigurationscheme/{id} | Update field configuration scheme |
| PUT | /rest/api/3/fieldconfigurationscheme/{id}/mapping | Assign issue types to field configurations |
| POST | /rest/api/3/fieldconfigurationscheme/{id}/mapping/delete | Remove issue types from field configuration scheme |
| POST | /rest/api/3/filter | Create filter |
| GET | /rest/api/3/filter/defaultShareScope | Get default share scope |
| PUT | /rest/api/3/filter/defaultShareScope | Set default share scope |
| GET | /rest/api/3/filter/favourite | Get favorite filters |
| GET | /rest/api/3/filter/my | Get my filters |
| GET | /rest/api/3/filter/search | Search for filters |
| DELETE | /rest/api/3/filter/{id} | Delete filter |
| GET | /rest/api/3/filter/{id} | Get filter |
| PUT | /rest/api/3/filter/{id} | Update filter |
| DELETE | /rest/api/3/filter/{id}/columns | Reset columns |
| GET | /rest/api/3/filter/{id}/columns | Get columns |
| PUT | /rest/api/3/filter/{id}/columns | Set columns |
| DELETE | /rest/api/3/filter/{id}/favourite | Remove filter as favorite |
| PUT | /rest/api/3/filter/{id}/favourite | Add filter as favorite |
| PUT | /rest/api/3/filter/{id}/owner | Change filter owner |
| GET | /rest/api/3/filter/{id}/permission | Get share permissions |
| POST | /rest/api/3/filter/{id}/permission | Add share permission |
| DELETE | /rest/api/3/filter/{id}/permission/{permissionId} | Delete share permission |
| GET | /rest/api/3/filter/{id}/permission/{permissionId} | Get share permission |
| POST | /rest/api/3/forge/panel/action/bulk/async | Bulk pin or unpin issue panel to projects |
| DELETE | /rest/api/3/group | Remove group |
| GET | /rest/api/3/group | Get group |
| POST | /rest/api/3/group | Create group |
| GET | /rest/api/3/group/bulk | Bulk get groups |
| GET | /rest/api/3/group/member | Get users from group |
| DELETE | /rest/api/3/group/user | Remove user from group |
| POST | /rest/api/3/group/user | Add user to group |
| GET | /rest/api/3/groups/picker | Find groups |
| GET | /rest/api/3/groupuserpicker | Find users and groups |
| GET | /rest/api/3/instance/license | Get license |
| POST | /rest/api/3/issue | Create issue |
| POST | /rest/api/3/issue/archive | Archive issue(s) by JQL |
| PUT | /rest/api/3/issue/archive | Archive issue(s) by issue ID/key |
| POST | /rest/api/3/issue/bulk | Bulk create issue |
| POST | /rest/api/3/issue/bulkfetch | Bulk fetch issues |
| GET | /rest/api/3/issue/createmeta | Get create issue metadata |
| GET | /rest/api/3/issue/createmeta/{projectIdOrKey}/issuetypes | Get create metadata issue types for a project |
| GET | /rest/api/3/issue/createmeta/{projectIdOrKey}/issuetypes/{issueTypeId} | Get create field metadata for a project and issue type id |
| GET | /rest/api/3/issue/limit/report | Get issue limit report |
| GET | /rest/api/3/issue/picker | Get issue picker suggestions |
| POST | /rest/api/3/issue/properties | Bulk set issues properties by list |
| POST | /rest/api/3/issue/properties/multi | Bulk set issue properties by issue |
| DELETE | /rest/api/3/issue/properties/{propertyKey} | Bulk delete issue property |
| PUT | /rest/api/3/issue/properties/{propertyKey} | Bulk set issue property |
| PUT | /rest/api/3/issue/unarchive | Unarchive issue(s) by issue keys/ID |
| POST | /rest/api/3/issue/watching | Get is watching issue bulk |
| DELETE | /rest/api/3/issue/{issueIdOrKey} | Delete issue |
| GET | /rest/api/3/issue/{issueIdOrKey} | Get issue |
| PUT | /rest/api/3/issue/{issueIdOrKey} | Edit issue |
| PUT | /rest/api/3/issue/{issueIdOrKey}/assignee | Assign issue |
| POST | /rest/api/3/issue/{issueIdOrKey}/attachments | Add attachment |
| GET | /rest/api/3/issue/{issueIdOrKey}/changelog | Get changelogs |
| POST | /rest/api/3/issue/{issueIdOrKey}/changelog/list | Get changelogs by IDs |
| GET | /rest/api/3/issue/{issueIdOrKey}/comment | Get comments |
| POST | /rest/api/3/issue/{issueIdOrKey}/comment | Add comment |
| DELETE | /rest/api/3/issue/{issueIdOrKey}/comment/{id} | Delete comment |
| GET | /rest/api/3/issue/{issueIdOrKey}/comment/{id} | Get comment |
| PUT | /rest/api/3/issue/{issueIdOrKey}/comment/{id} | Update comment |
| GET | /rest/api/3/issue/{issueIdOrKey}/editmeta | Get edit issue metadata |
| POST | /rest/api/3/issue/{issueIdOrKey}/notify | Send notification for issue |
| GET | /rest/api/3/issue/{issueIdOrKey}/properties | Get issue property keys |
| DELETE | /rest/api/3/issue/{issueIdOrKey}/properties/{propertyKey} | Delete issue property |
| GET | /rest/api/3/issue/{issueIdOrKey}/properties/{propertyKey} | Get issue property |
| PUT | /rest/api/3/issue/{issueIdOrKey}/properties/{propertyKey} | Set issue property |
| DELETE | /rest/api/3/issue/{issueIdOrKey}/remotelink | Delete remote issue link by global ID |
| GET | /rest/api/3/issue/{issueIdOrKey}/remotelink | Get remote issue links |
| POST | /rest/api/3/issue/{issueIdOrKey}/remotelink | Create or update remote issue link |
| DELETE | /rest/api/3/issue/{issueIdOrKey}/remotelink/{linkId} | Delete remote issue link by ID |
| GET | /rest/api/3/issue/{issueIdOrKey}/remotelink/{linkId} | Get remote issue link by ID |
| PUT | /rest/api/3/issue/{issueIdOrKey}/remotelink/{linkId} | Update remote issue link by ID |
| GET | /rest/api/3/issue/{issueIdOrKey}/transitions | Get transitions |
| POST | /rest/api/3/issue/{issueIdOrKey}/transitions | Transition issue |
| DELETE | /rest/api/3/issue/{issueIdOrKey}/votes | Delete vote |
| GET | /rest/api/3/issue/{issueIdOrKey}/votes | Get votes |
| POST | /rest/api/3/issue/{issueIdOrKey}/votes | Add vote |
| DELETE | /rest/api/3/issue/{issueIdOrKey}/watchers | Delete watcher |
| GET | /rest/api/3/issue/{issueIdOrKey}/watchers | Get issue watchers |
| POST | /rest/api/3/issue/{issueIdOrKey}/watchers | Add watcher |
| DELETE | /rest/api/3/issue/{issueIdOrKey}/worklog | Bulk delete worklogs |
| GET | /rest/api/3/issue/{issueIdOrKey}/worklog | Get issue worklogs |
| POST | /rest/api/3/issue/{issueIdOrKey}/worklog | Add worklog |
| POST | /rest/api/3/issue/{issueIdOrKey}/worklog/move | Bulk move worklogs |
| DELETE | /rest/api/3/issue/{issueIdOrKey}/worklog/{id} | Delete worklog |
| GET | /rest/api/3/issue/{issueIdOrKey}/worklog/{id} | Get worklog |
| PUT | /rest/api/3/issue/{issueIdOrKey}/worklog/{id} | Update worklog |
| GET | /rest/api/3/issue/{issueIdOrKey}/worklog/{worklogId}/properties | Get worklog property keys |
| DELETE | /rest/api/3/issue/{issueIdOrKey}/worklog/{worklogId}/properties/{propertyKey} | Delete worklog property |
| GET | /rest/api/3/issue/{issueIdOrKey}/worklog/{worklogId}/properties/{propertyKey} | Get worklog property |
| PUT | /rest/api/3/issue/{issueIdOrKey}/worklog/{worklogId}/properties/{propertyKey} | Set worklog property |
| POST | /rest/api/3/issueLink | Create issue link |
| DELETE | /rest/api/3/issueLink/{linkId} | Delete issue link |
| GET | /rest/api/3/issueLink/{linkId} | Get issue link |
| GET | /rest/api/3/issueLinkType | Get issue link types |
| POST | /rest/api/3/issueLinkType | Create issue link type |
| DELETE | /rest/api/3/issueLinkType/{issueLinkTypeId} | Delete issue link type |
| GET | /rest/api/3/issueLinkType/{issueLinkTypeId} | Get issue link type |
| PUT | /rest/api/3/issueLinkType/{issueLinkTypeId} | Update issue link type |
| PUT | /rest/api/3/issues/archive/export | Export archived issue(s) |
| GET | /rest/api/3/issuesecurityschemes | Get issue security schemes |
| POST | /rest/api/3/issuesecurityschemes | Create issue security scheme |
| GET | /rest/api/3/issuesecurityschemes/level | Get issue security levels |
| PUT | /rest/api/3/issuesecurityschemes/level/default | Set default issue security levels |
| GET | /rest/api/3/issuesecurityschemes/level/member | Get issue security level members |
| GET | /rest/api/3/issuesecurityschemes/project | Get projects using issue security schemes |
| PUT | /rest/api/3/issuesecurityschemes/project | Associate security scheme to project |
| GET | /rest/api/3/issuesecurityschemes/search | Search issue security schemes |
| GET | /rest/api/3/issuesecurityschemes/{id} | Get issue security scheme |
| PUT | /rest/api/3/issuesecurityschemes/{id} | Update issue security scheme |
| GET | /rest/api/3/issuesecurityschemes/{issueSecuritySchemeId}/members | Get issue security level members by issue security scheme |
| DELETE | /rest/api/3/issuesecurityschemes/{schemeId} | Delete issue security scheme |
| PUT | /rest/api/3/issuesecurityschemes/{schemeId}/level | Add issue security levels |
| DELETE | /rest/api/3/issuesecurityschemes/{schemeId}/level/{levelId} | Remove issue security level |
| PUT | /rest/api/3/issuesecurityschemes/{schemeId}/level/{levelId} | Update issue security level |
| PUT | /rest/api/3/issuesecurityschemes/{schemeId}/level/{levelId}/member | Add issue security level members |
| DELETE | /rest/api/3/issuesecurityschemes/{schemeId}/level/{levelId}/member/{memberId} | Remove member from issue security level |
| GET | /rest/api/3/issuetype | Get all issue types for user |
| POST | /rest/api/3/issuetype | Create issue type |
| GET | /rest/api/3/issuetype/project | Get issue types for project |
| DELETE | /rest/api/3/issuetype/{id} | Delete issue type |
| GET | /rest/api/3/issuetype/{id} | Get issue type |
| PUT | /rest/api/3/issuetype/{id} | Update issue type |
| GET | /rest/api/3/issuetype/{id}/alternatives | Get alternative issue types |
| POST | /rest/api/3/issuetype/{id}/avatar2 | Load issue type avatar |
| GET | /rest/api/3/issuetype/{issueTypeId}/properties | Get issue type property keys |
| DELETE | /rest/api/3/issuetype/{issueTypeId}/properties/{propertyKey} | Delete issue type property |
| GET | /rest/api/3/issuetype/{issueTypeId}/properties/{propertyKey} | Get issue type property |
| PUT | /rest/api/3/issuetype/{issueTypeId}/properties/{propertyKey} | Set issue type property |
| GET | /rest/api/3/issuetypescheme | Get all issue type schemes |
| POST | /rest/api/3/issuetypescheme | Create issue type scheme |
| GET | /rest/api/3/issuetypescheme/mapping | Get issue type scheme items |
| GET | /rest/api/3/issuetypescheme/project | Get issue type schemes for projects |
| PUT | /rest/api/3/issuetypescheme/project | Assign issue type scheme to project |
| DELETE | /rest/api/3/issuetypescheme/{issueTypeSchemeId} | Delete issue type scheme |
| PUT | /rest/api/3/issuetypescheme/{issueTypeSchemeId} | Update issue type scheme |
| PUT | /rest/api/3/issuetypescheme/{issueTypeSchemeId}/issuetype | Add issue types to issue type scheme |
| PUT | /rest/api/3/issuetypescheme/{issueTypeSchemeId}/issuetype/move | Change order of issue types |
| DELETE | /rest/api/3/issuetypescheme/{issueTypeSchemeId}/issuetype/{issueTypeId} | Remove issue type from issue type scheme |
| GET | /rest/api/3/issuetypescreenscheme | Get issue type screen schemes |
| POST | /rest/api/3/issuetypescreenscheme | Create issue type screen scheme |
| GET | /rest/api/3/issuetypescreenscheme/mapping | Get issue type screen scheme items |
| GET | /rest/api/3/issuetypescreenscheme/project | Get issue type screen schemes for projects |
| PUT | /rest/api/3/issuetypescreenscheme/project | Assign issue type screen scheme to project |
| DELETE | /rest/api/3/issuetypescreenscheme/{issueTypeScreenSchemeId} | Delete issue type screen scheme |
| PUT | /rest/api/3/issuetypescreenscheme/{issueTypeScreenSchemeId} | Update issue type screen scheme |
| PUT | /rest/api/3/issuetypescreenscheme/{issueTypeScreenSchemeId}/mapping | Append mappings to issue type screen scheme |
| PUT | /rest/api/3/issuetypescreenscheme/{issueTypeScreenSchemeId}/mapping/default | Update issue type screen scheme default screen scheme |
| POST | /rest/api/3/issuetypescreenscheme/{issueTypeScreenSchemeId}/mapping/remove | Remove mappings from issue type screen scheme |
| GET | /rest/api/3/issuetypescreenscheme/{issueTypeScreenSchemeId}/project | Get issue type screen scheme projects |
| GET | /rest/api/3/jql/autocompletedata | Get field reference data (GET) |
| POST | /rest/api/3/jql/autocompletedata | Get field reference data (POST) |
| GET | /rest/api/3/jql/autocompletedata/suggestions | Get field auto complete suggestions |
| GET | /rest/api/3/jql/function/computation | Get precomputations (apps) |
| POST | /rest/api/3/jql/function/computation | Update precomputations (apps) |
| POST | /rest/api/3/jql/function/computation/search | Get precomputations by ID (apps) |
| POST | /rest/api/3/jql/match | Check issues against JQL |
| POST | /rest/api/3/jql/parse | Parse JQL query |
| POST | /rest/api/3/jql/pdcleaner | Convert user identifiers to account IDs in JQL queries |
| POST | /rest/api/3/jql/sanitize | Sanitize JQL queries |
| GET | /rest/api/3/label | Get all labels |
| GET | /rest/api/3/license/approximateLicenseCount | Get approximate license count |
| GET | /rest/api/3/license/approximateLicenseCount/product/{applicationKey} | Get approximate application license count |
| GET | /rest/api/3/mypermissions | Get my permissions |
| DELETE | /rest/api/3/mypreferences | Delete preference |
| GET | /rest/api/3/mypreferences | Get preference |
| PUT | /rest/api/3/mypreferences | Set preference |
| GET | /rest/api/3/mypreferences/locale | Get locale |
| PUT | /rest/api/3/mypreferences/locale | Set locale |
| GET | /rest/api/3/myself | Get current user |
| GET | /rest/api/3/notificationscheme | Get notification schemes paginated |
| POST | /rest/api/3/notificationscheme | Create notification scheme |
| GET | /rest/api/3/notificationscheme/project | Get projects using notification schemes paginated |
| GET | /rest/api/3/notificationscheme/{id} | Get notification scheme |
| PUT | /rest/api/3/notificationscheme/{id} | Update notification scheme |
| PUT | /rest/api/3/notificationscheme/{id}/notification | Add notifications to notification scheme |
| DELETE | /rest/api/3/notificationscheme/{notificationSchemeId} | Delete notification scheme |
| DELETE | /rest/api/3/notificationscheme/{notificationSchemeId}/notification/{notificationId} | Remove notification from notification scheme |
| GET | /rest/api/3/permissions | Get all permissions |
| POST | /rest/api/3/permissions/check | Get bulk permissions |
| POST | /rest/api/3/permissions/project | Get permitted projects |
| GET | /rest/api/3/permissionscheme | Get all permission schemes |
| POST | /rest/api/3/permissionscheme | Create permission scheme |
| DELETE | /rest/api/3/permissionscheme/{schemeId} | Delete permission scheme |
| GET | /rest/api/3/permissionscheme/{schemeId} | Get permission scheme |
| PUT | /rest/api/3/permissionscheme/{schemeId} | Update permission scheme |
| GET | /rest/api/3/permissionscheme/{schemeId}/permission | Get permission scheme grants |
| POST | /rest/api/3/permissionscheme/{schemeId}/permission | Create permission grant |
| DELETE | /rest/api/3/permissionscheme/{schemeId}/permission/{permissionId} | Delete permission scheme grant |
| GET | /rest/api/3/permissionscheme/{schemeId}/permission/{permissionId} | Get permission scheme grant |
| GET | /rest/api/3/plans/plan | Get plans paginated |
| POST | /rest/api/3/plans/plan | Create plan |
| GET | /rest/api/3/plans/plan/{planId} | Get plan |
| PUT | /rest/api/3/plans/plan/{planId} | Update plan |
| PUT | /rest/api/3/plans/plan/{planId}/archive | Archive plan |
| POST | /rest/api/3/plans/plan/{planId}/duplicate | Duplicate plan |
| GET | /rest/api/3/plans/plan/{planId}/team | Get teams in plan paginated |
| POST | /rest/api/3/plans/plan/{planId}/team/atlassian | Add Atlassian team to plan |
| DELETE | /rest/api/3/plans/plan/{planId}/team/atlassian/{atlassianTeamId} | Remove Atlassian team from plan |
| GET | /rest/api/3/plans/plan/{planId}/team/atlassian/{atlassianTeamId} | Get Atlassian team in plan |
| PUT | /rest/api/3/plans/plan/{planId}/team/atlassian/{atlassianTeamId} | Update Atlassian team in plan |
| POST | /rest/api/3/plans/plan/{planId}/team/planonly | Create plan-only team |
| DELETE | /rest/api/3/plans/plan/{planId}/team/planonly/{planOnlyTeamId} | Delete plan-only team |
| GET | /rest/api/3/plans/plan/{planId}/team/planonly/{planOnlyTeamId} | Get plan-only team |
| PUT | /rest/api/3/plans/plan/{planId}/team/planonly/{planOnlyTeamId} | Update plan-only team |
| PUT | /rest/api/3/plans/plan/{planId}/trash | Trash plan |
| GET | /rest/api/3/priority | Get priorities |
| POST | /rest/api/3/priority | Create priority |
| PUT | /rest/api/3/priority/default | Set default priority |
| PUT | /rest/api/3/priority/move | Move priorities |
| GET | /rest/api/3/priority/search | Search priorities |
| DELETE | /rest/api/3/priority/{id} | Delete priority |
| GET | /rest/api/3/priority/{id} | Get priority |
| PUT | /rest/api/3/priority/{id} | Update priority |
| GET | /rest/api/3/priorityscheme | Get priority schemes |
| POST | /rest/api/3/priorityscheme | Create priority scheme |
| POST | /rest/api/3/priorityscheme/mappings | Suggested priorities for mappings |
| GET | /rest/api/3/priorityscheme/priorities/available | Get available priorities by priority scheme |
| DELETE | /rest/api/3/priorityscheme/{schemeId} | Delete priority scheme |
| PUT | /rest/api/3/priorityscheme/{schemeId} | Update priority scheme |
| GET | /rest/api/3/priorityscheme/{schemeId}/priorities | Get priorities by priority scheme |
| GET | /rest/api/3/priorityscheme/{schemeId}/projects | Get projects by priority scheme |
| GET | /rest/api/3/project | Get all projects |
| POST | /rest/api/3/project | Create project |
| POST | /rest/api/3/project-template | Create custom project |
| PUT | /rest/api/3/project-template/edit-template | Edit a custom project template |
| GET | /rest/api/3/project-template/live-template | Gets a custom project template |
| DELETE | /rest/api/3/project-template/remove-template | Deletes a custom project template |
| POST | /rest/api/3/project-template/save-template | Save a custom project template |
| GET | /rest/api/3/project/recent | Get recent projects |
| GET | /rest/api/3/project/search | Get projects paginated |
| GET | /rest/api/3/project/type | Get all project types |
| GET | /rest/api/3/project/type/accessible | Get licensed project types |
| GET | /rest/api/3/project/type/{projectTypeKey} | Get project type by key |
| GET | /rest/api/3/project/type/{projectTypeKey}/accessible | Get accessible project type by key |
| DELETE | /rest/api/3/project/{projectIdOrKey} | Delete project |
| GET | /rest/api/3/project/{projectIdOrKey} | Get project |
| PUT | /rest/api/3/project/{projectIdOrKey} | Update project |
| POST | /rest/api/3/project/{projectIdOrKey}/archive | Archive project |
| PUT | /rest/api/3/project/{projectIdOrKey}/avatar | Set project avatar |
| DELETE | /rest/api/3/project/{projectIdOrKey}/avatar/{id} | Delete project avatar |
| POST | /rest/api/3/project/{projectIdOrKey}/avatar2 | Load project avatar |
| GET | /rest/api/3/project/{projectIdOrKey}/avatars | Get all project avatars |
| GET | /rest/api/3/project/{projectIdOrKey}/classification-config | Get the classification configuration for a project |
| DELETE | /rest/api/3/project/{projectIdOrKey}/classification-level/default | Remove the default data classification level from a project |
| GET | /rest/api/3/project/{projectIdOrKey}/classification-level/default | Get the default data classification level of a project |
| PUT | /rest/api/3/project/{projectIdOrKey}/classification-level/default | Update the default data classification level of a project |
| GET | /rest/api/3/project/{projectIdOrKey}/component | Get project components paginated |
| GET | /rest/api/3/project/{projectIdOrKey}/components | Get project components |
| POST | /rest/api/3/project/{projectIdOrKey}/delete | Delete project asynchronously |
| GET | /rest/api/3/project/{projectIdOrKey}/features | Get project features |
| PUT | /rest/api/3/project/{projectIdOrKey}/features/{featureKey} | Set project feature state |
| GET | /rest/api/3/project/{projectIdOrKey}/properties | Get project property keys |
| DELETE | /rest/api/3/project/{projectIdOrKey}/properties/{propertyKey} | Delete project property |
| GET | /rest/api/3/project/{projectIdOrKey}/properties/{propertyKey} | Get project property |
| PUT | /rest/api/3/project/{projectIdOrKey}/properties/{propertyKey} | Set project property |
| POST | /rest/api/3/project/{projectIdOrKey}/restore | Restore deleted or archived project |
| GET | /rest/api/3/project/{projectIdOrKey}/role | Get project roles for project |
| DELETE | /rest/api/3/project/{projectIdOrKey}/role/{id} | Delete actors from project role |
| GET | /rest/api/3/project/{projectIdOrKey}/role/{id} | Get project role for project |
| POST | /rest/api/3/project/{projectIdOrKey}/role/{id} | Add actors to project role |
| PUT | /rest/api/3/project/{projectIdOrKey}/role/{id} | Set actors for project role |
| GET | /rest/api/3/project/{projectIdOrKey}/roledetails | Get project role details |
| GET | /rest/api/3/project/{projectIdOrKey}/statuses | Get all statuses for project |
| GET | /rest/api/3/project/{projectIdOrKey}/version | Get project versions paginated |
| GET | /rest/api/3/project/{projectIdOrKey}/versions | Get project versions |
| GET | /rest/api/3/project/{projectId}/email | Get project's sender email |
| PUT | /rest/api/3/project/{projectId}/email | Set project's sender email |
| GET | /rest/api/3/project/{projectId}/hierarchy | Get project issue type hierarchy |
| GET | /rest/api/3/project/{projectKeyOrId}/issuesecuritylevelscheme | Get project issue security scheme |
| GET | /rest/api/3/project/{projectKeyOrId}/notificationscheme | Get project notification scheme |
| GET | /rest/api/3/project/{projectKeyOrId}/permissionscheme | Get assigned permission scheme |
| PUT | /rest/api/3/project/{projectKeyOrId}/permissionscheme | Assign permission scheme |
| GET | /rest/api/3/project/{projectKeyOrId}/securitylevel | Get project issue security levels |
| GET | /rest/api/3/projectCategory | Get all project categories |
| POST | /rest/api/3/projectCategory | Create project category |
| DELETE | /rest/api/3/projectCategory/{id} | Delete project category |
| GET | /rest/api/3/projectCategory/{id} | Get project category by ID |
| PUT | /rest/api/3/projectCategory/{id} | Update project category |
| GET | /rest/api/3/projects/fields | Get fields for projects |
| GET | /rest/api/3/projectvalidate/key | Validate project key |
| GET | /rest/api/3/projectvalidate/validProjectKey | Get valid project key |
| GET | /rest/api/3/projectvalidate/validProjectName | Get valid project name |
| POST | /rest/api/3/redact | Redact |
| GET | /rest/api/3/redact/status/{jobId} | Get redaction status |
| GET | /rest/api/3/resolution | Get resolutions |
| POST | /rest/api/3/resolution | Create resolution |
| PUT | /rest/api/3/resolution/default | Set default resolution |
| PUT | /rest/api/3/resolution/move | Move resolutions |
| GET | /rest/api/3/resolution/search | Search resolutions |
| DELETE | /rest/api/3/resolution/{id} | Delete resolution |
| GET | /rest/api/3/resolution/{id} | Get resolution |
| PUT | /rest/api/3/resolution/{id} | Update resolution |
| GET | /rest/api/3/role | Get all project roles |
| POST | /rest/api/3/role | Create project role |
| DELETE | /rest/api/3/role/{id} | Delete project role |
| GET | /rest/api/3/role/{id} | Get project role by ID |
| POST | /rest/api/3/role/{id} | Partial update project role |
| PUT | /rest/api/3/role/{id} | Fully update project role |
| DELETE | /rest/api/3/role/{id}/actors | Delete default actors from project role |
| GET | /rest/api/3/role/{id}/actors | Get default actors for project role |
| POST | /rest/api/3/role/{id}/actors | Add default actors to project role |
| GET | /rest/api/3/screens | Get screens |
| POST | /rest/api/3/screens | Create screen |
| POST | /rest/api/3/screens/addToDefault/{fieldId} | Add field to default screen |
| GET | /rest/api/3/screens/tabs | Get bulk screen tabs |
| DELETE | /rest/api/3/screens/{screenId} | Delete screen |
| PUT | /rest/api/3/screens/{screenId} | Update screen |
| GET | /rest/api/3/screens/{screenId}/availableFields | Get available screen fields |
| GET | /rest/api/3/screens/{screenId}/tabs | Get all screen tabs |
| POST | /rest/api/3/screens/{screenId}/tabs | Create screen tab |
| DELETE | /rest/api/3/screens/{screenId}/tabs/{tabId} | Delete screen tab |
| PUT | /rest/api/3/screens/{screenId}/tabs/{tabId} | Update screen tab |
| GET | /rest/api/3/screens/{screenId}/tabs/{tabId}/fields | Get all screen tab fields |
| POST | /rest/api/3/screens/{screenId}/tabs/{tabId}/fields | Add screen tab field |
| DELETE | /rest/api/3/screens/{screenId}/tabs/{tabId}/fields/{id} | Remove screen tab field |
| POST | /rest/api/3/screens/{screenId}/tabs/{tabId}/fields/{id}/move | Move screen tab field |
| POST | /rest/api/3/screens/{screenId}/tabs/{tabId}/move/{pos} | Move screen tab |
| GET | /rest/api/3/screenscheme | Get screen schemes |
| POST | /rest/api/3/screenscheme | Create screen scheme |
| DELETE | /rest/api/3/screenscheme/{screenSchemeId} | Delete screen scheme |
| PUT | /rest/api/3/screenscheme/{screenSchemeId} | Update screen scheme |
| GET | /rest/api/3/search | Currently being removed. Search for issues using JQL (GET) |
| POST | /rest/api/3/search | Currently being removed. Search for issues using JQL (POST) |
| POST | /rest/api/3/search/approximate-count | Count issues using JQL |
| GET | /rest/api/3/search/jql | Search for issues using JQL enhanced search (GET) |
| POST | /rest/api/3/search/jql | Search for issues using JQL enhanced search (POST) |
| GET | /rest/api/3/securitylevel/{id} | Get issue security level |
| GET | /rest/api/3/serverInfo | Get Jira instance info |
| GET | /rest/api/3/settings/columns | Get issue navigator default columns |
| PUT | /rest/api/3/settings/columns | Set issue navigator default columns |
| GET | /rest/api/3/status | Get all statuses |
| GET | /rest/api/3/status/{idOrName} | Get status |
| GET | /rest/api/3/statuscategory | Get all status categories |
| GET | /rest/api/3/statuscategory/{idOrKey} | Get status category |
| DELETE | /rest/api/3/statuses | Bulk delete Statuses |
| GET | /rest/api/3/statuses | Bulk get statuses |
| POST | /rest/api/3/statuses | Bulk create statuses |
| PUT | /rest/api/3/statuses | Bulk update statuses |
| GET | /rest/api/3/statuses/byNames | Bulk get statuses by name |
| GET | /rest/api/3/statuses/search | Search statuses paginated |
| GET | /rest/api/3/statuses/{statusId}/project/{projectId}/issueTypeUsages | Get issue type usages by status and project |
| GET | /rest/api/3/statuses/{statusId}/projectUsages | Get project usages by status |
| GET | /rest/api/3/statuses/{statusId}/workflowUsages | Get workflow usages by status |
| GET | /rest/api/3/task/{taskId} | Get task |
| POST | /rest/api/3/task/{taskId}/cancel | Cancel task |
| GET | /rest/api/3/uiModifications | Get UI modifications |
| POST | /rest/api/3/uiModifications | Create UI modification |
| DELETE | /rest/api/3/uiModifications/{uiModificationId} | Delete UI modification |
| PUT | /rest/api/3/uiModifications/{uiModificationId} | Update UI modification |
| GET | /rest/api/3/universal_avatar/type/{type}/owner/{entityId} | Get avatars |
| POST | /rest/api/3/universal_avatar/type/{type}/owner/{entityId} | Load avatar |
| DELETE | /rest/api/3/universal_avatar/type/{type}/owner/{owningObjectId}/avatar/{id} | Delete avatar |
| GET | /rest/api/3/universal_avatar/view/type/{type} | Get avatar image by type |
| GET | /rest/api/3/universal_avatar/view/type/{type}/avatar/{id} | Get avatar image by ID |
| GET | /rest/api/3/universal_avatar/view/type/{type}/owner/{entityId} | Get avatar image by owner |
| DELETE | /rest/api/3/user | Delete user |
| GET | /rest/api/3/user | Get user |
| POST | /rest/api/3/user | Create user |
| GET | /rest/api/3/user/assignable/multiProjectSearch | Find users assignable to projects |
| GET | /rest/api/3/user/assignable/search | Find users assignable to issues |
| GET | /rest/api/3/user/bulk | Bulk get users |
| GET | /rest/api/3/user/bulk/migration | Get account IDs for users |
| DELETE | /rest/api/3/user/columns | Reset user default columns |
| GET | /rest/api/3/user/columns | Get user default columns |
| PUT | /rest/api/3/user/columns | Set user default columns |
| GET | /rest/api/3/user/email | Get user email |
| GET | /rest/api/3/user/email/bulk | Get user email bulk |
| GET | /rest/api/3/user/groups | Get user groups |
| GET | /rest/api/3/user/permission/search | Find users with permissions |
| GET | /rest/api/3/user/picker | Find users for picker |
| GET | /rest/api/3/user/properties | Get user property keys |
| DELETE | /rest/api/3/user/properties/{propertyKey} | Delete user property |
| GET | /rest/api/3/user/properties/{propertyKey} | Get user property |
| PUT | /rest/api/3/user/properties/{propertyKey} | Set user property |
| GET | /rest/api/3/user/search | Find users |
| GET | /rest/api/3/user/search/query | Find users by query |
| GET | /rest/api/3/user/search/query/key | Find user keys by query |
| GET | /rest/api/3/user/viewissue/search | Find users with browse permission |
| GET | /rest/api/3/users | Get all users default |
| GET | /rest/api/3/users/search | Get all users |
| POST | /rest/api/3/version | Create version |
| DELETE | /rest/api/3/version/{id} | Delete version |
| GET | /rest/api/3/version/{id} | Get version |
| PUT | /rest/api/3/version/{id} | Update version |
| PUT | /rest/api/3/version/{id}/mergeto/{moveIssuesTo} | Merge versions |
| POST | /rest/api/3/version/{id}/move | Move version |
| GET | /rest/api/3/version/{id}/relatedIssueCounts | Get version's related issues count |
| GET | /rest/api/3/version/{id}/relatedwork | Get related work |
| POST | /rest/api/3/version/{id}/relatedwork | Create related work |
| PUT | /rest/api/3/version/{id}/relatedwork | Update related work |
| POST | /rest/api/3/version/{id}/removeAndSwap | Delete and replace version |
| GET | /rest/api/3/version/{id}/unresolvedIssueCount | Get version's unresolved issues count |
| DELETE | /rest/api/3/version/{versionId}/relatedwork/{relatedWorkId} | Delete related work |
| DELETE | /rest/api/3/webhook | Delete webhooks by ID |
| GET | /rest/api/3/webhook | Get dynamic webhooks for app |
| POST | /rest/api/3/webhook | Register dynamic webhooks |
| GET | /rest/api/3/webhook/failed | Get failed webhooks |
| PUT | /rest/api/3/webhook/refresh | Extend webhook life |
| GET | /rest/api/3/workflow | Get all workflows |
| POST | /rest/api/3/workflow | Create workflow |
| POST | /rest/api/3/workflow/history | Read workflow version from history |
| POST | /rest/api/3/workflow/history/list | List workflow history entries |
| GET | /rest/api/3/workflow/rule/config | Get workflow transition rule configurations |
| PUT | /rest/api/3/workflow/rule/config | Update workflow transition rule configurations |
| PUT | /rest/api/3/workflow/rule/config/delete | Delete workflow transition rule configurations |
| GET | /rest/api/3/workflow/search | Get workflows paginated |
| DELETE | /rest/api/3/workflow/transitions/{transitionId}/properties | Delete workflow transition property |
| GET | /rest/api/3/workflow/transitions/{transitionId}/properties | Get workflow transition properties |
| POST | /rest/api/3/workflow/transitions/{transitionId}/properties | Create workflow transition property |
| PUT | /rest/api/3/workflow/transitions/{transitionId}/properties | Update workflow transition property |
| DELETE | /rest/api/3/workflow/{entityId} | Delete inactive workflow |
| GET | /rest/api/3/workflow/{workflowId}/project/{projectId}/issueTypeUsages | Get issue types in a project that are using a given workflow |
| GET | /rest/api/3/workflow/{workflowId}/projectUsages | Get projects using a given workflow |
| GET | /rest/api/3/workflow/{workflowId}/workflowSchemes | Get workflow schemes which are using a given workflow |
| POST | /rest/api/3/workflows | Bulk get workflows |
| GET | /rest/api/3/workflows/capabilities | Get available workflow capabilities |
| POST | /rest/api/3/workflows/create | Bulk create workflows |
| POST | /rest/api/3/workflows/create/validation | Validate create workflows |
| GET | /rest/api/3/workflows/defaultEditor | Get the user's default workflow editor |
| POST | /rest/api/3/workflows/preview | Preview workflow |
| GET | /rest/api/3/workflows/search | Search workflows |
| POST | /rest/api/3/workflows/update | Bulk update workflows |
| POST | /rest/api/3/workflows/update/validation | Validate update workflows |
| GET | /rest/api/3/workflowscheme | Get all workflow schemes |
| POST | /rest/api/3/workflowscheme | Create workflow scheme |
| GET | /rest/api/3/workflowscheme/project | Get workflow scheme project associations |
| PUT | /rest/api/3/workflowscheme/project | Assign workflow scheme to project |
| POST | /rest/api/3/workflowscheme/project/switch | Switch workflow scheme for project |
| POST | /rest/api/3/workflowscheme/read | Bulk get workflow schemes |
| POST | /rest/api/3/workflowscheme/update | Update workflow scheme |
| POST | /rest/api/3/workflowscheme/update/mappings | Get required status mappings for workflow scheme update |
| DELETE | /rest/api/3/workflowscheme/{id} | Delete workflow scheme |
| GET | /rest/api/3/workflowscheme/{id} | Get workflow scheme |
| PUT | /rest/api/3/workflowscheme/{id} | Classic update workflow scheme |
| POST | /rest/api/3/workflowscheme/{id}/createdraft | Create draft workflow scheme |
| DELETE | /rest/api/3/workflowscheme/{id}/default | Delete default workflow |
| GET | /rest/api/3/workflowscheme/{id}/default | Get default workflow |
| PUT | /rest/api/3/workflowscheme/{id}/default | Update default workflow |
| DELETE | /rest/api/3/workflowscheme/{id}/draft | Delete draft workflow scheme |
| GET | /rest/api/3/workflowscheme/{id}/draft | Get draft workflow scheme |
| PUT | /rest/api/3/workflowscheme/{id}/draft | Update draft workflow scheme |
| DELETE | /rest/api/3/workflowscheme/{id}/draft/default | Delete draft default workflow |
| GET | /rest/api/3/workflowscheme/{id}/draft/default | Get draft default workflow |
| PUT | /rest/api/3/workflowscheme/{id}/draft/default | Update draft default workflow |
| DELETE | /rest/api/3/workflowscheme/{id}/draft/issuetype/{issueType} | Delete workflow for issue type in draft workflow scheme |
| GET | /rest/api/3/workflowscheme/{id}/draft/issuetype/{issueType} | Get workflow for issue type in draft workflow scheme |
| PUT | /rest/api/3/workflowscheme/{id}/draft/issuetype/{issueType} | Set workflow for issue type in draft workflow scheme |
| POST | /rest/api/3/workflowscheme/{id}/draft/publish | Publish draft workflow scheme |
| DELETE | /rest/api/3/workflowscheme/{id}/draft/workflow | Delete issue types for workflow in draft workflow scheme |
| GET | /rest/api/3/workflowscheme/{id}/draft/workflow | Get issue types for workflows in draft workflow scheme |
| PUT | /rest/api/3/workflowscheme/{id}/draft/workflow | Set issue types for workflow in workflow scheme |
| DELETE | /rest/api/3/workflowscheme/{id}/issuetype/{issueType} | Delete workflow for issue type in workflow scheme |
| GET | /rest/api/3/workflowscheme/{id}/issuetype/{issueType} | Get workflow for issue type in workflow scheme |
| PUT | /rest/api/3/workflowscheme/{id}/issuetype/{issueType} | Set workflow for issue type in workflow scheme |
| DELETE | /rest/api/3/workflowscheme/{id}/workflow | Delete issue types for workflow in workflow scheme |
| GET | /rest/api/3/workflowscheme/{id}/workflow | Get issue types for workflows in workflow scheme |
| PUT | /rest/api/3/workflowscheme/{id}/workflow | Set issue types for workflow in workflow scheme |
| GET | /rest/api/3/workflowscheme/{workflowSchemeId}/projectUsages | Get projects which are using a given workflow scheme |
| GET | /rest/api/3/worklog/deleted | Get IDs of deleted worklogs |
| POST | /rest/api/3/worklog/list | Get worklogs |
| GET | /rest/api/3/worklog/updated | Get IDs of updated worklogs |
| GET | /rest/atlassian-connect/1/addons/{addonKey}/properties | Get app properties |
| DELETE | /rest/atlassian-connect/1/addons/{addonKey}/properties/{propertyKey} | Delete app property |
| GET | /rest/atlassian-connect/1/addons/{addonKey}/properties/{propertyKey} | Get app property |
| PUT | /rest/atlassian-connect/1/addons/{addonKey}/properties/{propertyKey} | Set app property |
| DELETE | /rest/atlassian-connect/1/app/module/dynamic | Remove modules |
| GET | /rest/atlassian-connect/1/app/module/dynamic | Get modules |
| POST | /rest/atlassian-connect/1/app/module/dynamic | Register modules |
| PUT | /rest/atlassian-connect/1/migration/field | Bulk update custom field value |
| PUT | /rest/atlassian-connect/1/migration/properties/{entityType} | Bulk update entity properties |
| POST | /rest/atlassian-connect/1/migration/workflow/rule/search | Get workflow transition rule configurations |
| GET | /rest/atlassian-connect/1/migration/{connectKey}/{jiraIssueFieldsKey}/task | Get Connect issue field migration task |
| GET | /rest/atlassian-connect/1/service-registry | Retrieve the attributes of service registries |
| GET | /rest/forge/1/app/properties | Get app property keys (Forge) |
| DELETE | /rest/forge/1/app/properties/{propertyKey} | Delete app property (Forge) |
| GET | /rest/forge/1/app/properties/{propertyKey} | Get app property (Forge) |
| PUT | /rest/forge/1/app/properties/{propertyKey} | Set app property (Forge) |
| POST | /rest/internal/api/latest/worklog/bulk | Get worklogs by issue id and worklog id |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all announcementBanner?" -> GET /rest/api/3/announcementBanner
- "Create a list?" -> POST /rest/api/3/app/field/context/configuration/list
- "Create a value?" -> POST /rest/api/3/app/field/value
- "List all configuration?" -> GET /rest/api/3/app/field/{fieldIdOrKey}/context/configuration
- "List all application-properties?" -> GET /rest/api/3/application-properties
- "List all advanced-settings?" -> GET /rest/api/3/application-properties/advanced-settings
- "Update a application-property?" -> PUT /rest/api/3/application-properties/{id}
- "List all applicationrole?" -> GET /rest/api/3/applicationrole
- "Get applicationrole details?" -> GET /rest/api/3/applicationrole/{key}
- "Get content details?" -> GET /rest/api/3/attachment/content/{id}
- "List all meta?" -> GET /rest/api/3/attachment/meta
- "Get thumbnail details?" -> GET /rest/api/3/attachment/thumbnail/{id}
- "Delete a attachment?" -> DELETE /rest/api/3/attachment/{id}
- "Get attachment details?" -> GET /rest/api/3/attachment/{id}
- "List all human?" -> GET /rest/api/3/attachment/{id}/expand/human
- "List all raw?" -> GET /rest/api/3/attachment/{id}/expand/raw
- "List all record?" -> GET /rest/api/3/auditing/record
- "List all system?" -> GET /rest/api/3/avatar/{type}/system
- "Create a delete?" -> POST /rest/api/3/bulk/issues/delete
- "List all fields?" -> GET /rest/api/3/bulk/issues/fields
- "Create a field?" -> POST /rest/api/3/bulk/issues/fields
- "Create a move?" -> POST /rest/api/3/bulk/issues/move
- "List all transition?" -> GET /rest/api/3/bulk/issues/transition
- "Create a transition?" -> POST /rest/api/3/bulk/issues/transition
- "Create a unwatch?" -> POST /rest/api/3/bulk/issues/unwatch
- "Create a watch?" -> POST /rest/api/3/bulk/issues/watch
- "Get queue details?" -> GET /rest/api/3/bulk/queue/{taskId}
- "Create a bulkfetch?" -> POST /rest/api/3/changelog/bulkfetch
- "List all classification-levels?" -> GET /rest/api/3/classification-levels
- "Create a list?" -> POST /rest/api/3/comment/list
- "List all properties?" -> GET /rest/api/3/comment/{commentId}/properties
- "Delete a property?" -> DELETE /rest/api/3/comment/{commentId}/properties/{propertyKey}
- "Get property details?" -> GET /rest/api/3/comment/{commentId}/properties/{propertyKey}
- "Update a property?" -> PUT /rest/api/3/comment/{commentId}/properties/{propertyKey}
- "Search component?" -> GET /rest/api/3/component
- "Create a component?" -> POST /rest/api/3/component
- "Delete a component?" -> DELETE /rest/api/3/component/{id}
- "Get component details?" -> GET /rest/api/3/component/{id}
- "Update a component?" -> PUT /rest/api/3/component/{id}
- "List all relatedIssueCounts?" -> GET /rest/api/3/component/{id}/relatedIssueCounts
- "Search fieldschemes?" -> GET /rest/api/3/config/fieldschemes
- "Create a fieldscheme?" -> POST /rest/api/3/config/fieldschemes
- "List all projects?" -> GET /rest/api/3/config/fieldschemes/projects
- "Delete a fieldscheme?" -> DELETE /rest/api/3/config/fieldschemes/{id}
- "Get fieldscheme details?" -> GET /rest/api/3/config/fieldschemes/{id}
- "Update a fieldscheme?" -> PUT /rest/api/3/config/fieldschemes/{id}
- "Create a clone?" -> POST /rest/api/3/config/fieldschemes/{id}/clone
- "List all fields?" -> GET /rest/api/3/config/fieldschemes/{id}/fields
- "List all parameters?" -> GET /rest/api/3/config/fieldschemes/{id}/fields/{fieldId}/parameters
- "List all projects?" -> GET /rest/api/3/config/fieldschemes/{id}/projects
- "List all configuration?" -> GET /rest/api/3/configuration
- "List all timetracking?" -> GET /rest/api/3/configuration/timetracking
- "List all list?" -> GET /rest/api/3/configuration/timetracking/list
- "List all options?" -> GET /rest/api/3/configuration/timetracking/options
- "Get customFieldOption details?" -> GET /rest/api/3/customFieldOption/{id}
- "List all dashboard?" -> GET /rest/api/3/dashboard
- "Create a dashboard?" -> POST /rest/api/3/dashboard
- "List all gadgets?" -> GET /rest/api/3/dashboard/gadgets
- "List all search?" -> GET /rest/api/3/dashboard/search
- "List all gadget?" -> GET /rest/api/3/dashboard/{dashboardId}/gadget
- "Create a gadget?" -> POST /rest/api/3/dashboard/{dashboardId}/gadget
- "Delete a gadget?" -> DELETE /rest/api/3/dashboard/{dashboardId}/gadget/{gadgetId}
- "Update a gadget?" -> PUT /rest/api/3/dashboard/{dashboardId}/gadget/{gadgetId}
- "List all properties?" -> GET /rest/api/3/dashboard/{dashboardId}/items/{itemId}/properties
- "Delete a property?" -> DELETE /rest/api/3/dashboard/{dashboardId}/items/{itemId}/properties/{propertyKey}
- "Get property details?" -> GET /rest/api/3/dashboard/{dashboardId}/items/{itemId}/properties/{propertyKey}
- "Update a property?" -> PUT /rest/api/3/dashboard/{dashboardId}/items/{itemId}/properties/{propertyKey}
- "Delete a dashboard?" -> DELETE /rest/api/3/dashboard/{id}
- "Get dashboard details?" -> GET /rest/api/3/dashboard/{id}
- "Update a dashboard?" -> PUT /rest/api/3/dashboard/{id}
- "Create a copy?" -> POST /rest/api/3/dashboard/{id}/copy
- "List all data-policy?" -> GET /rest/api/3/data-policy
- "List all project?" -> GET /rest/api/3/data-policy/project
- "List all events?" -> GET /rest/api/3/events
- "Create a analyse?" -> POST /rest/api/3/expression/analyse
- "Create a eval?" -> POST /rest/api/3/expression/eval
- "Create a evaluate?" -> POST /rest/api/3/expression/evaluate
- "List all field?" -> GET /rest/api/3/field
- "Create a field?" -> POST /rest/api/3/field
- "Search search?" -> GET /rest/api/3/field/search
- "Search trashed?" -> GET /rest/api/3/field/search/trashed
- "Update a field?" -> PUT /rest/api/3/field/{fieldId}
- "List all context?" -> GET /rest/api/3/field/{fieldId}/context
- "Create a context?" -> POST /rest/api/3/field/{fieldId}/context
- "List all defaultValue?" -> GET /rest/api/3/field/{fieldId}/context/defaultValue
- "List all issuetypemapping?" -> GET /rest/api/3/field/{fieldId}/context/issuetypemapping
- "Create a mapping?" -> POST /rest/api/3/field/{fieldId}/context/mapping
- "List all projectmapping?" -> GET /rest/api/3/field/{fieldId}/context/projectmapping
- "Delete a context?" -> DELETE /rest/api/3/field/{fieldId}/context/{contextId}
- "Update a context?" -> PUT /rest/api/3/field/{fieldId}/context/{contextId}
- "Create a remove?" -> POST /rest/api/3/field/{fieldId}/context/{contextId}/issuetype/remove
- "List all option?" -> GET /rest/api/3/field/{fieldId}/context/{contextId}/option
- "Create a option?" -> POST /rest/api/3/field/{fieldId}/context/{contextId}/option
- "Delete a option?" -> DELETE /rest/api/3/field/{fieldId}/context/{contextId}/option/{optionId}
- "Create a remove?" -> POST /rest/api/3/field/{fieldId}/context/{contextId}/project/remove
- "List all contexts?" -> GET /rest/api/3/field/{fieldId}/contexts
- "List all screens?" -> GET /rest/api/3/field/{fieldId}/screens
- "List all option?" -> GET /rest/api/3/field/{fieldKey}/option
- "Create a option?" -> POST /rest/api/3/field/{fieldKey}/option
- "List all edit?" -> GET /rest/api/3/field/{fieldKey}/option/suggestions/edit
- "List all search?" -> GET /rest/api/3/field/{fieldKey}/option/suggestions/search
- "Delete a option?" -> DELETE /rest/api/3/field/{fieldKey}/option/{optionId}
- "Get option details?" -> GET /rest/api/3/field/{fieldKey}/option/{optionId}
- "Update a option?" -> PUT /rest/api/3/field/{fieldKey}/option/{optionId}
- "Delete a field?" -> DELETE /rest/api/3/field/{id}
- "Create a restore?" -> POST /rest/api/3/field/{id}/restore
- "Create a trash?" -> POST /rest/api/3/field/{id}/trash
- "Search fieldconfiguration?" -> GET /rest/api/3/fieldconfiguration
- "Create a fieldconfiguration?" -> POST /rest/api/3/fieldconfiguration
- "Delete a fieldconfiguration?" -> DELETE /rest/api/3/fieldconfiguration/{id}
- "Update a fieldconfiguration?" -> PUT /rest/api/3/fieldconfiguration/{id}
- "List all fields?" -> GET /rest/api/3/fieldconfiguration/{id}/fields
- "List all fieldconfigurationscheme?" -> GET /rest/api/3/fieldconfigurationscheme
- "Create a fieldconfigurationscheme?" -> POST /rest/api/3/fieldconfigurationscheme
- "List all mapping?" -> GET /rest/api/3/fieldconfigurationscheme/mapping
- "List all project?" -> GET /rest/api/3/fieldconfigurationscheme/project
- "Delete a fieldconfigurationscheme?" -> DELETE /rest/api/3/fieldconfigurationscheme/{id}
- "Update a fieldconfigurationscheme?" -> PUT /rest/api/3/fieldconfigurationscheme/{id}
- "Create a delete?" -> POST /rest/api/3/fieldconfigurationscheme/{id}/mapping/delete
- "Create a filter?" -> POST /rest/api/3/filter
- "List all defaultShareScope?" -> GET /rest/api/3/filter/defaultShareScope
- "List all favourite?" -> GET /rest/api/3/filter/favourite
- "List all my?" -> GET /rest/api/3/filter/my
- "List all search?" -> GET /rest/api/3/filter/search
- "Delete a filter?" -> DELETE /rest/api/3/filter/{id}
- "Get filter details?" -> GET /rest/api/3/filter/{id}
- "Update a filter?" -> PUT /rest/api/3/filter/{id}
- "List all columns?" -> GET /rest/api/3/filter/{id}/columns
- "List all permission?" -> GET /rest/api/3/filter/{id}/permission
- "Create a permission?" -> POST /rest/api/3/filter/{id}/permission
- "Delete a permission?" -> DELETE /rest/api/3/filter/{id}/permission/{permissionId}
- "Get permission details?" -> GET /rest/api/3/filter/{id}/permission/{permissionId}
- "Create a async?" -> POST /rest/api/3/forge/panel/action/bulk/async
- "List all group?" -> GET /rest/api/3/group
- "Create a group?" -> POST /rest/api/3/group
- "List all bulk?" -> GET /rest/api/3/group/bulk
- "List all member?" -> GET /rest/api/3/group/member
- "Create a user?" -> POST /rest/api/3/group/user
- "Search picker?" -> GET /rest/api/3/groups/picker
- "Search groupuserpicker?" -> GET /rest/api/3/groupuserpicker
- "List all license?" -> GET /rest/api/3/instance/license
- "Create a issue?" -> POST /rest/api/3/issue
- "Create a archive?" -> POST /rest/api/3/issue/archive
- "Create a bulk?" -> POST /rest/api/3/issue/bulk
- "Create a bulkfetch?" -> POST /rest/api/3/issue/bulkfetch
- "List all createmeta?" -> GET /rest/api/3/issue/createmeta
- "List all issuetypes?" -> GET /rest/api/3/issue/createmeta/{projectIdOrKey}/issuetypes
- "Get issuetype details?" -> GET /rest/api/3/issue/createmeta/{projectIdOrKey}/issuetypes/{issueTypeId}
- "List all report?" -> GET /rest/api/3/issue/limit/report
- "Search picker?" -> GET /rest/api/3/issue/picker
- "Create a property?" -> POST /rest/api/3/issue/properties
- "Create a multi?" -> POST /rest/api/3/issue/properties/multi
- "Delete a property?" -> DELETE /rest/api/3/issue/properties/{propertyKey}
- "Update a property?" -> PUT /rest/api/3/issue/properties/{propertyKey}
- "Create a watching?" -> POST /rest/api/3/issue/watching
- "Delete a issue?" -> DELETE /rest/api/3/issue/{issueIdOrKey}
- "Get issue details?" -> GET /rest/api/3/issue/{issueIdOrKey}
- "Update a issue?" -> PUT /rest/api/3/issue/{issueIdOrKey}
- "Create a attachment?" -> POST /rest/api/3/issue/{issueIdOrKey}/attachments
- "List all changelog?" -> GET /rest/api/3/issue/{issueIdOrKey}/changelog
- "Create a list?" -> POST /rest/api/3/issue/{issueIdOrKey}/changelog/list
- "List all comment?" -> GET /rest/api/3/issue/{issueIdOrKey}/comment
- "Create a comment?" -> POST /rest/api/3/issue/{issueIdOrKey}/comment
- "Delete a comment?" -> DELETE /rest/api/3/issue/{issueIdOrKey}/comment/{id}
- "Get comment details?" -> GET /rest/api/3/issue/{issueIdOrKey}/comment/{id}
- "Update a comment?" -> PUT /rest/api/3/issue/{issueIdOrKey}/comment/{id}
- "List all editmeta?" -> GET /rest/api/3/issue/{issueIdOrKey}/editmeta
- "Create a notify?" -> POST /rest/api/3/issue/{issueIdOrKey}/notify
- "List all properties?" -> GET /rest/api/3/issue/{issueIdOrKey}/properties
- "Delete a property?" -> DELETE /rest/api/3/issue/{issueIdOrKey}/properties/{propertyKey}
- "Get property details?" -> GET /rest/api/3/issue/{issueIdOrKey}/properties/{propertyKey}
- "Update a property?" -> PUT /rest/api/3/issue/{issueIdOrKey}/properties/{propertyKey}
- "List all remotelink?" -> GET /rest/api/3/issue/{issueIdOrKey}/remotelink
- "Create a remotelink?" -> POST /rest/api/3/issue/{issueIdOrKey}/remotelink
- "Delete a remotelink?" -> DELETE /rest/api/3/issue/{issueIdOrKey}/remotelink/{linkId}
- "Get remotelink details?" -> GET /rest/api/3/issue/{issueIdOrKey}/remotelink/{linkId}
- "Update a remotelink?" -> PUT /rest/api/3/issue/{issueIdOrKey}/remotelink/{linkId}
- "List all transitions?" -> GET /rest/api/3/issue/{issueIdOrKey}/transitions
- "Create a transition?" -> POST /rest/api/3/issue/{issueIdOrKey}/transitions
- "List all votes?" -> GET /rest/api/3/issue/{issueIdOrKey}/votes
- "Create a vote?" -> POST /rest/api/3/issue/{issueIdOrKey}/votes
- "List all watchers?" -> GET /rest/api/3/issue/{issueIdOrKey}/watchers
- "Create a watcher?" -> POST /rest/api/3/issue/{issueIdOrKey}/watchers
- "List all worklog?" -> GET /rest/api/3/issue/{issueIdOrKey}/worklog
- "Create a worklog?" -> POST /rest/api/3/issue/{issueIdOrKey}/worklog
- "Create a move?" -> POST /rest/api/3/issue/{issueIdOrKey}/worklog/move
- "Delete a worklog?" -> DELETE /rest/api/3/issue/{issueIdOrKey}/worklog/{id}
- "Get worklog details?" -> GET /rest/api/3/issue/{issueIdOrKey}/worklog/{id}
- "Update a worklog?" -> PUT /rest/api/3/issue/{issueIdOrKey}/worklog/{id}
- "List all properties?" -> GET /rest/api/3/issue/{issueIdOrKey}/worklog/{worklogId}/properties
- "Delete a property?" -> DELETE /rest/api/3/issue/{issueIdOrKey}/worklog/{worklogId}/properties/{propertyKey}
- "Get property details?" -> GET /rest/api/3/issue/{issueIdOrKey}/worklog/{worklogId}/properties/{propertyKey}
- "Update a property?" -> PUT /rest/api/3/issue/{issueIdOrKey}/worklog/{worklogId}/properties/{propertyKey}
- "Create a issueLink?" -> POST /rest/api/3/issueLink
- "Delete a issueLink?" -> DELETE /rest/api/3/issueLink/{linkId}
- "Get issueLink details?" -> GET /rest/api/3/issueLink/{linkId}
- "List all issueLinkType?" -> GET /rest/api/3/issueLinkType
- "Create a issueLinkType?" -> POST /rest/api/3/issueLinkType
- "Delete a issueLinkType?" -> DELETE /rest/api/3/issueLinkType/{issueLinkTypeId}
- "Get issueLinkType details?" -> GET /rest/api/3/issueLinkType/{issueLinkTypeId}
- "Update a issueLinkType?" -> PUT /rest/api/3/issueLinkType/{issueLinkTypeId}
- "List all issuesecurityschemes?" -> GET /rest/api/3/issuesecurityschemes
- "Create a issuesecurityscheme?" -> POST /rest/api/3/issuesecurityschemes
- "List all level?" -> GET /rest/api/3/issuesecurityschemes/level
- "List all member?" -> GET /rest/api/3/issuesecurityschemes/level/member
- "List all project?" -> GET /rest/api/3/issuesecurityschemes/project
- "List all search?" -> GET /rest/api/3/issuesecurityschemes/search
- "Get issuesecurityscheme details?" -> GET /rest/api/3/issuesecurityschemes/{id}
- "Update a issuesecurityscheme?" -> PUT /rest/api/3/issuesecurityschemes/{id}
- "List all members?" -> GET /rest/api/3/issuesecurityschemes/{issueSecuritySchemeId}/members
- "Delete a issuesecurityscheme?" -> DELETE /rest/api/3/issuesecurityschemes/{schemeId}
- "Delete a level?" -> DELETE /rest/api/3/issuesecurityschemes/{schemeId}/level/{levelId}
- "Update a level?" -> PUT /rest/api/3/issuesecurityschemes/{schemeId}/level/{levelId}
- "Delete a member?" -> DELETE /rest/api/3/issuesecurityschemes/{schemeId}/level/{levelId}/member/{memberId}
- "List all issuetype?" -> GET /rest/api/3/issuetype
- "Create a issuetype?" -> POST /rest/api/3/issuetype
- "List all project?" -> GET /rest/api/3/issuetype/project
- "Delete a issuetype?" -> DELETE /rest/api/3/issuetype/{id}
- "Get issuetype details?" -> GET /rest/api/3/issuetype/{id}
- "Update a issuetype?" -> PUT /rest/api/3/issuetype/{id}
- "List all alternatives?" -> GET /rest/api/3/issuetype/{id}/alternatives
- "Create a avatar2?" -> POST /rest/api/3/issuetype/{id}/avatar2
- "List all properties?" -> GET /rest/api/3/issuetype/{issueTypeId}/properties
- "Delete a property?" -> DELETE /rest/api/3/issuetype/{issueTypeId}/properties/{propertyKey}
- "Get property details?" -> GET /rest/api/3/issuetype/{issueTypeId}/properties/{propertyKey}
- "Update a property?" -> PUT /rest/api/3/issuetype/{issueTypeId}/properties/{propertyKey}
- "List all issuetypescheme?" -> GET /rest/api/3/issuetypescheme
- "Create a issuetypescheme?" -> POST /rest/api/3/issuetypescheme
- "List all mapping?" -> GET /rest/api/3/issuetypescheme/mapping
- "List all project?" -> GET /rest/api/3/issuetypescheme/project
- "Delete a issuetypescheme?" -> DELETE /rest/api/3/issuetypescheme/{issueTypeSchemeId}
- "Update a issuetypescheme?" -> PUT /rest/api/3/issuetypescheme/{issueTypeSchemeId}
- "Delete a issuetype?" -> DELETE /rest/api/3/issuetypescheme/{issueTypeSchemeId}/issuetype/{issueTypeId}
- "List all issuetypescreenscheme?" -> GET /rest/api/3/issuetypescreenscheme
- "Create a issuetypescreenscheme?" -> POST /rest/api/3/issuetypescreenscheme
- "List all mapping?" -> GET /rest/api/3/issuetypescreenscheme/mapping
- "List all project?" -> GET /rest/api/3/issuetypescreenscheme/project
- "Delete a issuetypescreenscheme?" -> DELETE /rest/api/3/issuetypescreenscheme/{issueTypeScreenSchemeId}
- "Update a issuetypescreenscheme?" -> PUT /rest/api/3/issuetypescreenscheme/{issueTypeScreenSchemeId}
- "Create a remove?" -> POST /rest/api/3/issuetypescreenscheme/{issueTypeScreenSchemeId}/mapping/remove
- "Search project?" -> GET /rest/api/3/issuetypescreenscheme/{issueTypeScreenSchemeId}/project
- "List all autocompletedata?" -> GET /rest/api/3/jql/autocompletedata
- "Create a autocompletedata?" -> POST /rest/api/3/jql/autocompletedata
- "List all suggestions?" -> GET /rest/api/3/jql/autocompletedata/suggestions
- "List all computation?" -> GET /rest/api/3/jql/function/computation
- "Create a computation?" -> POST /rest/api/3/jql/function/computation
- "Create a search?" -> POST /rest/api/3/jql/function/computation/search
- "Create a match?" -> POST /rest/api/3/jql/match
- "Create a parse?" -> POST /rest/api/3/jql/parse
- "Create a pdcleaner?" -> POST /rest/api/3/jql/pdcleaner
- "Create a sanitize?" -> POST /rest/api/3/jql/sanitize
- "List all label?" -> GET /rest/api/3/label
- "List all approximateLicenseCount?" -> GET /rest/api/3/license/approximateLicenseCount
- "Get product details?" -> GET /rest/api/3/license/approximateLicenseCount/product/{applicationKey}
- "List all mypermissions?" -> GET /rest/api/3/mypermissions
- "List all mypreferences?" -> GET /rest/api/3/mypreferences
- "List all locale?" -> GET /rest/api/3/mypreferences/locale
- "List all myself?" -> GET /rest/api/3/myself
- "List all notificationscheme?" -> GET /rest/api/3/notificationscheme
- "Create a notificationscheme?" -> POST /rest/api/3/notificationscheme
- "List all project?" -> GET /rest/api/3/notificationscheme/project
- "Get notificationscheme details?" -> GET /rest/api/3/notificationscheme/{id}
- "Update a notificationscheme?" -> PUT /rest/api/3/notificationscheme/{id}
- "Delete a notificationscheme?" -> DELETE /rest/api/3/notificationscheme/{notificationSchemeId}
- "Delete a notification?" -> DELETE /rest/api/3/notificationscheme/{notificationSchemeId}/notification/{notificationId}
- "List all permissions?" -> GET /rest/api/3/permissions
- "Create a check?" -> POST /rest/api/3/permissions/check
- "Create a project?" -> POST /rest/api/3/permissions/project
- "List all permissionscheme?" -> GET /rest/api/3/permissionscheme
- "Create a permissionscheme?" -> POST /rest/api/3/permissionscheme
- "Delete a permissionscheme?" -> DELETE /rest/api/3/permissionscheme/{schemeId}
- "Get permissionscheme details?" -> GET /rest/api/3/permissionscheme/{schemeId}
- "Update a permissionscheme?" -> PUT /rest/api/3/permissionscheme/{schemeId}
- "List all permission?" -> GET /rest/api/3/permissionscheme/{schemeId}/permission
- "Create a permission?" -> POST /rest/api/3/permissionscheme/{schemeId}/permission
- "Delete a permission?" -> DELETE /rest/api/3/permissionscheme/{schemeId}/permission/{permissionId}
- "Get permission details?" -> GET /rest/api/3/permissionscheme/{schemeId}/permission/{permissionId}
- "List all plan?" -> GET /rest/api/3/plans/plan
- "Create a plan?" -> POST /rest/api/3/plans/plan
- "Get plan details?" -> GET /rest/api/3/plans/plan/{planId}
- "Update a plan?" -> PUT /rest/api/3/plans/plan/{planId}
- "Create a duplicate?" -> POST /rest/api/3/plans/plan/{planId}/duplicate
- "List all team?" -> GET /rest/api/3/plans/plan/{planId}/team
- "Create a atlassian?" -> POST /rest/api/3/plans/plan/{planId}/team/atlassian
- "Delete a atlassian?" -> DELETE /rest/api/3/plans/plan/{planId}/team/atlassian/{atlassianTeamId}
- "Get atlassian details?" -> GET /rest/api/3/plans/plan/{planId}/team/atlassian/{atlassianTeamId}
- "Update a atlassian?" -> PUT /rest/api/3/plans/plan/{planId}/team/atlassian/{atlassianTeamId}
- "Create a planonly?" -> POST /rest/api/3/plans/plan/{planId}/team/planonly
- "Delete a planonly?" -> DELETE /rest/api/3/plans/plan/{planId}/team/planonly/{planOnlyTeamId}
- "Get planonly details?" -> GET /rest/api/3/plans/plan/{planId}/team/planonly/{planOnlyTeamId}
- "Update a planonly?" -> PUT /rest/api/3/plans/plan/{planId}/team/planonly/{planOnlyTeamId}
- "List all priority?" -> GET /rest/api/3/priority
- "Create a priority?" -> POST /rest/api/3/priority
- "List all search?" -> GET /rest/api/3/priority/search
- "Delete a priority?" -> DELETE /rest/api/3/priority/{id}
- "Get priority details?" -> GET /rest/api/3/priority/{id}
- "Update a priority?" -> PUT /rest/api/3/priority/{id}
- "List all priorityscheme?" -> GET /rest/api/3/priorityscheme
- "Create a priorityscheme?" -> POST /rest/api/3/priorityscheme
- "Create a mapping?" -> POST /rest/api/3/priorityscheme/mappings
- "Search available?" -> GET /rest/api/3/priorityscheme/priorities/available
- "Delete a priorityscheme?" -> DELETE /rest/api/3/priorityscheme/{schemeId}
- "Update a priorityscheme?" -> PUT /rest/api/3/priorityscheme/{schemeId}
- "List all priorities?" -> GET /rest/api/3/priorityscheme/{schemeId}/priorities
- "Search projects?" -> GET /rest/api/3/priorityscheme/{schemeId}/projects
- "List all project?" -> GET /rest/api/3/project
- "Create a project?" -> POST /rest/api/3/project
- "Create a project-template?" -> POST /rest/api/3/project-template
- "List all live-template?" -> GET /rest/api/3/project-template/live-template
- "Create a save-template?" -> POST /rest/api/3/project-template/save-template
- "List all recent?" -> GET /rest/api/3/project/recent
- "Search search?" -> GET /rest/api/3/project/search
- "List all type?" -> GET /rest/api/3/project/type
- "List all accessible?" -> GET /rest/api/3/project/type/accessible
- "Get type details?" -> GET /rest/api/3/project/type/{projectTypeKey}
- "List all accessible?" -> GET /rest/api/3/project/type/{projectTypeKey}/accessible
- "Delete a project?" -> DELETE /rest/api/3/project/{projectIdOrKey}
- "Get project details?" -> GET /rest/api/3/project/{projectIdOrKey}
- "Update a project?" -> PUT /rest/api/3/project/{projectIdOrKey}
- "Create a archive?" -> POST /rest/api/3/project/{projectIdOrKey}/archive
- "Delete a avatar?" -> DELETE /rest/api/3/project/{projectIdOrKey}/avatar/{id}
- "Create a avatar2?" -> POST /rest/api/3/project/{projectIdOrKey}/avatar2
- "List all avatars?" -> GET /rest/api/3/project/{projectIdOrKey}/avatars
- "List all classification-config?" -> GET /rest/api/3/project/{projectIdOrKey}/classification-config
- "List all default?" -> GET /rest/api/3/project/{projectIdOrKey}/classification-level/default
- "Search component?" -> GET /rest/api/3/project/{projectIdOrKey}/component
- "List all components?" -> GET /rest/api/3/project/{projectIdOrKey}/components
- "Create a delete?" -> POST /rest/api/3/project/{projectIdOrKey}/delete
- "List all features?" -> GET /rest/api/3/project/{projectIdOrKey}/features
- "Update a feature?" -> PUT /rest/api/3/project/{projectIdOrKey}/features/{featureKey}
- "List all properties?" -> GET /rest/api/3/project/{projectIdOrKey}/properties
- "Delete a property?" -> DELETE /rest/api/3/project/{projectIdOrKey}/properties/{propertyKey}
- "Get property details?" -> GET /rest/api/3/project/{projectIdOrKey}/properties/{propertyKey}
- "Update a property?" -> PUT /rest/api/3/project/{projectIdOrKey}/properties/{propertyKey}
- "Create a restore?" -> POST /rest/api/3/project/{projectIdOrKey}/restore
- "List all role?" -> GET /rest/api/3/project/{projectIdOrKey}/role
- "Delete a role?" -> DELETE /rest/api/3/project/{projectIdOrKey}/role/{id}
- "Get role details?" -> GET /rest/api/3/project/{projectIdOrKey}/role/{id}
- "Update a role?" -> PUT /rest/api/3/project/{projectIdOrKey}/role/{id}
- "List all roledetails?" -> GET /rest/api/3/project/{projectIdOrKey}/roledetails
- "List all statuses?" -> GET /rest/api/3/project/{projectIdOrKey}/statuses
- "Search version?" -> GET /rest/api/3/project/{projectIdOrKey}/version
- "List all versions?" -> GET /rest/api/3/project/{projectIdOrKey}/versions
- "List all email?" -> GET /rest/api/3/project/{projectId}/email
- "List all hierarchy?" -> GET /rest/api/3/project/{projectId}/hierarchy
- "List all issuesecuritylevelscheme?" -> GET /rest/api/3/project/{projectKeyOrId}/issuesecuritylevelscheme
- "List all notificationscheme?" -> GET /rest/api/3/project/{projectKeyOrId}/notificationscheme
- "List all permissionscheme?" -> GET /rest/api/3/project/{projectKeyOrId}/permissionscheme
- "List all securitylevel?" -> GET /rest/api/3/project/{projectKeyOrId}/securitylevel
- "List all projectCategory?" -> GET /rest/api/3/projectCategory
- "Create a projectCategory?" -> POST /rest/api/3/projectCategory
- "Delete a projectCategory?" -> DELETE /rest/api/3/projectCategory/{id}
- "Get projectCategory details?" -> GET /rest/api/3/projectCategory/{id}
- "Update a projectCategory?" -> PUT /rest/api/3/projectCategory/{id}
- "List all fields?" -> GET /rest/api/3/projects/fields
- "List all key?" -> GET /rest/api/3/projectvalidate/key
- "List all validProjectKey?" -> GET /rest/api/3/projectvalidate/validProjectKey
- "List all validProjectName?" -> GET /rest/api/3/projectvalidate/validProjectName
- "Create a redact?" -> POST /rest/api/3/redact
- "Get status details?" -> GET /rest/api/3/redact/status/{jobId}
- "List all resolution?" -> GET /rest/api/3/resolution
- "Create a resolution?" -> POST /rest/api/3/resolution
- "List all search?" -> GET /rest/api/3/resolution/search
- "Delete a resolution?" -> DELETE /rest/api/3/resolution/{id}
- "Get resolution details?" -> GET /rest/api/3/resolution/{id}
- "Update a resolution?" -> PUT /rest/api/3/resolution/{id}
- "List all role?" -> GET /rest/api/3/role
- "Create a role?" -> POST /rest/api/3/role
- "Delete a role?" -> DELETE /rest/api/3/role/{id}
- "Get role details?" -> GET /rest/api/3/role/{id}
- "Update a role?" -> PUT /rest/api/3/role/{id}
- "List all actors?" -> GET /rest/api/3/role/{id}/actors
- "Create a actor?" -> POST /rest/api/3/role/{id}/actors
- "List all screens?" -> GET /rest/api/3/screens
- "Create a screen?" -> POST /rest/api/3/screens
- "List all tabs?" -> GET /rest/api/3/screens/tabs
- "Delete a screen?" -> DELETE /rest/api/3/screens/{screenId}
- "Update a screen?" -> PUT /rest/api/3/screens/{screenId}
- "List all availableFields?" -> GET /rest/api/3/screens/{screenId}/availableFields
- "List all tabs?" -> GET /rest/api/3/screens/{screenId}/tabs
- "Create a tab?" -> POST /rest/api/3/screens/{screenId}/tabs
- "Delete a tab?" -> DELETE /rest/api/3/screens/{screenId}/tabs/{tabId}
- "Update a tab?" -> PUT /rest/api/3/screens/{screenId}/tabs/{tabId}
- "List all fields?" -> GET /rest/api/3/screens/{screenId}/tabs/{tabId}/fields
- "Create a field?" -> POST /rest/api/3/screens/{screenId}/tabs/{tabId}/fields
- "Delete a field?" -> DELETE /rest/api/3/screens/{screenId}/tabs/{tabId}/fields/{id}
- "Create a move?" -> POST /rest/api/3/screens/{screenId}/tabs/{tabId}/fields/{id}/move
- "List all screenscheme?" -> GET /rest/api/3/screenscheme
- "Create a screenscheme?" -> POST /rest/api/3/screenscheme
- "Delete a screenscheme?" -> DELETE /rest/api/3/screenscheme/{screenSchemeId}
- "Update a screenscheme?" -> PUT /rest/api/3/screenscheme/{screenSchemeId}
- "List all search?" -> GET /rest/api/3/search
- "Create a search?" -> POST /rest/api/3/search
- "Create a approximate-count?" -> POST /rest/api/3/search/approximate-count
- "List all jql?" -> GET /rest/api/3/search/jql
- "Create a jql?" -> POST /rest/api/3/search/jql
- "Get securitylevel details?" -> GET /rest/api/3/securitylevel/{id}
- "List all serverInfo?" -> GET /rest/api/3/serverInfo
- "List all columns?" -> GET /rest/api/3/settings/columns
- "List all status?" -> GET /rest/api/3/status
- "Get status details?" -> GET /rest/api/3/status/{idOrName}
- "List all statuscategory?" -> GET /rest/api/3/statuscategory
- "Get statuscategory details?" -> GET /rest/api/3/statuscategory/{idOrKey}
- "List all statuses?" -> GET /rest/api/3/statuses
- "Create a statuse?" -> POST /rest/api/3/statuses
- "List all byNames?" -> GET /rest/api/3/statuses/byNames
- "List all search?" -> GET /rest/api/3/statuses/search
- "List all issueTypeUsages?" -> GET /rest/api/3/statuses/{statusId}/project/{projectId}/issueTypeUsages
- "List all projectUsages?" -> GET /rest/api/3/statuses/{statusId}/projectUsages
- "List all workflowUsages?" -> GET /rest/api/3/statuses/{statusId}/workflowUsages
- "Get task details?" -> GET /rest/api/3/task/{taskId}
- "Create a cancel?" -> POST /rest/api/3/task/{taskId}/cancel
- "List all uiModifications?" -> GET /rest/api/3/uiModifications
- "Create a uiModification?" -> POST /rest/api/3/uiModifications
- "Delete a uiModification?" -> DELETE /rest/api/3/uiModifications/{uiModificationId}
- "Update a uiModification?" -> PUT /rest/api/3/uiModifications/{uiModificationId}
- "Get owner details?" -> GET /rest/api/3/universal_avatar/type/{type}/owner/{entityId}
- "Delete a avatar?" -> DELETE /rest/api/3/universal_avatar/type/{type}/owner/{owningObjectId}/avatar/{id}
- "Get type details?" -> GET /rest/api/3/universal_avatar/view/type/{type}
- "Get avatar details?" -> GET /rest/api/3/universal_avatar/view/type/{type}/avatar/{id}
- "Get owner details?" -> GET /rest/api/3/universal_avatar/view/type/{type}/owner/{entityId}
- "List all user?" -> GET /rest/api/3/user
- "Create a user?" -> POST /rest/api/3/user
- "Search multiProjectSearch?" -> GET /rest/api/3/user/assignable/multiProjectSearch
- "Search search?" -> GET /rest/api/3/user/assignable/search
- "List all bulk?" -> GET /rest/api/3/user/bulk
- "List all migration?" -> GET /rest/api/3/user/bulk/migration
- "List all columns?" -> GET /rest/api/3/user/columns
- "List all email?" -> GET /rest/api/3/user/email
- "List all bulk?" -> GET /rest/api/3/user/email/bulk
- "List all groups?" -> GET /rest/api/3/user/groups
- "Search search?" -> GET /rest/api/3/user/permission/search
- "Search picker?" -> GET /rest/api/3/user/picker
- "List all properties?" -> GET /rest/api/3/user/properties
- "Delete a property?" -> DELETE /rest/api/3/user/properties/{propertyKey}
- "Get property details?" -> GET /rest/api/3/user/properties/{propertyKey}
- "Update a property?" -> PUT /rest/api/3/user/properties/{propertyKey}
- "Search search?" -> GET /rest/api/3/user/search
- "Search query?" -> GET /rest/api/3/user/search/query
- "Search key?" -> GET /rest/api/3/user/search/query/key
- "Search search?" -> GET /rest/api/3/user/viewissue/search
- "List all users?" -> GET /rest/api/3/users
- "List all search?" -> GET /rest/api/3/users/search
- "Create a version?" -> POST /rest/api/3/version
- "Delete a version?" -> DELETE /rest/api/3/version/{id}
- "Get version details?" -> GET /rest/api/3/version/{id}
- "Update a version?" -> PUT /rest/api/3/version/{id}
- "Update a mergeto?" -> PUT /rest/api/3/version/{id}/mergeto/{moveIssuesTo}
- "Create a move?" -> POST /rest/api/3/version/{id}/move
- "List all relatedIssueCounts?" -> GET /rest/api/3/version/{id}/relatedIssueCounts
- "List all relatedwork?" -> GET /rest/api/3/version/{id}/relatedwork
- "Create a relatedwork?" -> POST /rest/api/3/version/{id}/relatedwork
- "Create a removeAndSwap?" -> POST /rest/api/3/version/{id}/removeAndSwap
- "List all unresolvedIssueCount?" -> GET /rest/api/3/version/{id}/unresolvedIssueCount
- "Delete a relatedwork?" -> DELETE /rest/api/3/version/{versionId}/relatedwork/{relatedWorkId}
- "List all webhook?" -> GET /rest/api/3/webhook
- "Create a webhook?" -> POST /rest/api/3/webhook
- "List all failed?" -> GET /rest/api/3/webhook/failed
- "List all workflow?" -> GET /rest/api/3/workflow
- "Create a workflow?" -> POST /rest/api/3/workflow
- "Create a history?" -> POST /rest/api/3/workflow/history
- "Create a list?" -> POST /rest/api/3/workflow/history/list
- "List all config?" -> GET /rest/api/3/workflow/rule/config
- "List all search?" -> GET /rest/api/3/workflow/search
- "List all properties?" -> GET /rest/api/3/workflow/transitions/{transitionId}/properties
- "Create a property?" -> POST /rest/api/3/workflow/transitions/{transitionId}/properties
- "Delete a workflow?" -> DELETE /rest/api/3/workflow/{entityId}
- "List all issueTypeUsages?" -> GET /rest/api/3/workflow/{workflowId}/project/{projectId}/issueTypeUsages
- "List all projectUsages?" -> GET /rest/api/3/workflow/{workflowId}/projectUsages
- "List all workflowSchemes?" -> GET /rest/api/3/workflow/{workflowId}/workflowSchemes
- "Create a workflow?" -> POST /rest/api/3/workflows
- "List all capabilities?" -> GET /rest/api/3/workflows/capabilities
- "Create a create?" -> POST /rest/api/3/workflows/create
- "Create a validation?" -> POST /rest/api/3/workflows/create/validation
- "List all defaultEditor?" -> GET /rest/api/3/workflows/defaultEditor
- "Create a preview?" -> POST /rest/api/3/workflows/preview
- "List all search?" -> GET /rest/api/3/workflows/search
- "Create a update?" -> POST /rest/api/3/workflows/update
- "Create a validation?" -> POST /rest/api/3/workflows/update/validation
- "List all workflowscheme?" -> GET /rest/api/3/workflowscheme
- "Create a workflowscheme?" -> POST /rest/api/3/workflowscheme
- "List all project?" -> GET /rest/api/3/workflowscheme/project
- "Create a switch?" -> POST /rest/api/3/workflowscheme/project/switch
- "Create a read?" -> POST /rest/api/3/workflowscheme/read
- "Create a update?" -> POST /rest/api/3/workflowscheme/update
- "Create a mapping?" -> POST /rest/api/3/workflowscheme/update/mappings
- "Delete a workflowscheme?" -> DELETE /rest/api/3/workflowscheme/{id}
- "Get workflowscheme details?" -> GET /rest/api/3/workflowscheme/{id}
- "Update a workflowscheme?" -> PUT /rest/api/3/workflowscheme/{id}
- "Create a createdraft?" -> POST /rest/api/3/workflowscheme/{id}/createdraft
- "List all default?" -> GET /rest/api/3/workflowscheme/{id}/default
- "List all draft?" -> GET /rest/api/3/workflowscheme/{id}/draft
- "List all default?" -> GET /rest/api/3/workflowscheme/{id}/draft/default
- "Delete a issuetype?" -> DELETE /rest/api/3/workflowscheme/{id}/draft/issuetype/{issueType}
- "Get issuetype details?" -> GET /rest/api/3/workflowscheme/{id}/draft/issuetype/{issueType}
- "Update a issuetype?" -> PUT /rest/api/3/workflowscheme/{id}/draft/issuetype/{issueType}
- "Create a publish?" -> POST /rest/api/3/workflowscheme/{id}/draft/publish
- "List all workflow?" -> GET /rest/api/3/workflowscheme/{id}/draft/workflow
- "Delete a issuetype?" -> DELETE /rest/api/3/workflowscheme/{id}/issuetype/{issueType}
- "Get issuetype details?" -> GET /rest/api/3/workflowscheme/{id}/issuetype/{issueType}
- "Update a issuetype?" -> PUT /rest/api/3/workflowscheme/{id}/issuetype/{issueType}
- "List all workflow?" -> GET /rest/api/3/workflowscheme/{id}/workflow
- "List all projectUsages?" -> GET /rest/api/3/workflowscheme/{workflowSchemeId}/projectUsages
- "List all deleted?" -> GET /rest/api/3/worklog/deleted
- "Create a list?" -> POST /rest/api/3/worklog/list
- "List all updated?" -> GET /rest/api/3/worklog/updated
- "List all properties?" -> GET /rest/atlassian-connect/1/addons/{addonKey}/properties
- "Delete a property?" -> DELETE /rest/atlassian-connect/1/addons/{addonKey}/properties/{propertyKey}
- "Get property details?" -> GET /rest/atlassian-connect/1/addons/{addonKey}/properties/{propertyKey}
- "Update a property?" -> PUT /rest/atlassian-connect/1/addons/{addonKey}/properties/{propertyKey}
- "List all dynamic?" -> GET /rest/atlassian-connect/1/app/module/dynamic
- "Create a dynamic?" -> POST /rest/atlassian-connect/1/app/module/dynamic
- "Update a property?" -> PUT /rest/atlassian-connect/1/migration/properties/{entityType}
- "Create a search?" -> POST /rest/atlassian-connect/1/migration/workflow/rule/search
- "List all task?" -> GET /rest/atlassian-connect/1/migration/{connectKey}/{jiraIssueFieldsKey}/task
- "List all service-registry?" -> GET /rest/atlassian-connect/1/service-registry
- "List all properties?" -> GET /rest/forge/1/app/properties
- "Delete a property?" -> DELETE /rest/forge/1/app/properties/{propertyKey}
- "Get property details?" -> GET /rest/forge/1/app/properties/{propertyKey}
- "Update a property?" -> PUT /rest/forge/1/app/properties/{propertyKey}
- "Create a bulk?" -> POST /rest/internal/api/latest/worklog/bulk
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
