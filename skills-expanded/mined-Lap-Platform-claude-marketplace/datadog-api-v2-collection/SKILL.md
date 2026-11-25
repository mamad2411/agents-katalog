---
name: datadog-api-v2-collection
description: "Datadog API V2 Collection API skill. Use when working with Datadog API V2 Collection for api. Covers 892 endpoints."
version: 1.0.0
generator: lapsh
---

# Datadog API V2 Collection
API version: 1.0

## Auth
OAuth2 | ApiKey DD-API-KEY in header | ApiKey DD-APPLICATION-KEY in header | Bearer bearer

## Base URL
https://api.datadoghq.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /api/unstable/fleet/agent_versions -- verify access
3. POST /api/unstable/fleet/deployments/configure -- create first configure

## Endpoints

892 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/unstable/fleet/agent_versions | List all available Agent versions |
| GET | /api/unstable/fleet/agents | List all Datadog Agents |
| GET | /api/unstable/fleet/agents/{agent_key} | Get detailed information about an agent |
| GET | /api/unstable/fleet/deployments | List all deployments |
| POST | /api/unstable/fleet/deployments/configure | Create a configuration deployment |
| POST | /api/unstable/fleet/deployments/upgrade | Upgrade hosts |
| GET | /api/unstable/fleet/deployments/{deployment_id} | Get a configuration deployment by ID |
| POST | /api/unstable/fleet/deployments/{deployment_id}/cancel | Cancel a deployment |
| GET | /api/unstable/fleet/schedules | List all schedules |
| POST | /api/unstable/fleet/schedules | Create a schedule |
| DELETE | /api/unstable/fleet/schedules/{id} | Delete a schedule |
| GET | /api/unstable/fleet/schedules/{id} | Get a schedule by ID |
| PATCH | /api/unstable/fleet/schedules/{id} | Update a schedule |
| POST | /api/unstable/fleet/schedules/{id}/trigger | Trigger a schedule deployment |
| GET | /api/v2/actions-datastores | List datastores |
| POST | /api/v2/actions-datastores | Create datastore |
| DELETE | /api/v2/actions-datastores/{datastore_id} | Delete datastore |
| GET | /api/v2/actions-datastores/{datastore_id} | Get datastore |
| PATCH | /api/v2/actions-datastores/{datastore_id} | Update datastore |
| DELETE | /api/v2/actions-datastores/{datastore_id}/items | Delete datastore item |
| GET | /api/v2/actions-datastores/{datastore_id}/items | List datastore items |
| PATCH | /api/v2/actions-datastores/{datastore_id}/items | Update datastore item |
| DELETE | /api/v2/actions-datastores/{datastore_id}/items/bulk | Bulk delete datastore items |
| POST | /api/v2/actions-datastores/{datastore_id}/items/bulk | Bulk write datastore items |
| GET | /api/v2/actions/app_key_registrations | List App Key Registrations |
| DELETE | /api/v2/actions/app_key_registrations/{app_key_id} | Unregister an App Key |
| GET | /api/v2/actions/app_key_registrations/{app_key_id} | Get an existing App Key Registration |
| PUT | /api/v2/actions/app_key_registrations/{app_key_id} | Register a new App Key |
| POST | /api/v2/actions/connections | Create a new Action Connection |
| DELETE | /api/v2/actions/connections/{connection_id} | Delete an existing Action Connection |
| GET | /api/v2/actions/connections/{connection_id} | Get an existing Action Connection |
| PATCH | /api/v2/actions/connections/{connection_id} | Update an existing Action Connection |
| GET | /api/v2/agentless_scanning/accounts/aws | List AWS scan options |
| POST | /api/v2/agentless_scanning/accounts/aws | Create AWS scan options |
| DELETE | /api/v2/agentless_scanning/accounts/aws/{account_id} | Delete AWS scan options |
| GET | /api/v2/agentless_scanning/accounts/aws/{account_id} | Get AWS scan options |
| PATCH | /api/v2/agentless_scanning/accounts/aws/{account_id} | Update AWS scan options |
| GET | /api/v2/agentless_scanning/accounts/azure | List Azure scan options |
| POST | /api/v2/agentless_scanning/accounts/azure | Create Azure scan options |
| DELETE | /api/v2/agentless_scanning/accounts/azure/{subscription_id} | Delete Azure scan options |
| GET | /api/v2/agentless_scanning/accounts/azure/{subscription_id} | Get Azure scan options |
| PATCH | /api/v2/agentless_scanning/accounts/azure/{subscription_id} | Update Azure scan options |
| GET | /api/v2/agentless_scanning/accounts/gcp | List GCP scan options |
| POST | /api/v2/agentless_scanning/accounts/gcp | Create GCP scan options |
| DELETE | /api/v2/agentless_scanning/accounts/gcp/{project_id} | Delete GCP scan options |
| GET | /api/v2/agentless_scanning/accounts/gcp/{project_id} | Get GCP scan options |
| PATCH | /api/v2/agentless_scanning/accounts/gcp/{project_id} | Update GCP scan options |
| GET | /api/v2/agentless_scanning/ondemand/aws | List AWS on demand tasks |
| POST | /api/v2/agentless_scanning/ondemand/aws | Create AWS on demand task |
| GET | /api/v2/agentless_scanning/ondemand/aws/{task_id} | Get AWS on demand task |
| GET | /api/v2/api_keys | Get all API keys |
| POST | /api/v2/api_keys | Create an API key |
| DELETE | /api/v2/api_keys/{api_key_id} | Delete an API key |
| GET | /api/v2/api_keys/{api_key_id} | Get API key |
| PATCH | /api/v2/api_keys/{api_key_id} | Edit an API key |
| GET | /api/v2/apicatalog/api | List APIs |
| DELETE | /api/v2/apicatalog/api/{id} | Delete an API |
| GET | /api/v2/apicatalog/api/{id}/openapi | Get an API |
| PUT | /api/v2/apicatalog/api/{id}/openapi | Update an API |
| POST | /api/v2/apicatalog/openapi | Create a new API |
| GET | /api/v2/apm/config/metrics | Get all span-based metrics |
| POST | /api/v2/apm/config/metrics | Create a span-based metric |
| DELETE | /api/v2/apm/config/metrics/{metric_id} | Delete a span-based metric |
| GET | /api/v2/apm/config/metrics/{metric_id} | Get a span-based metric |
| PATCH | /api/v2/apm/config/metrics/{metric_id} | Update a span-based metric |
| GET | /api/v2/apm/config/retention-filters | List all APM retention filters |
| POST | /api/v2/apm/config/retention-filters | Create a retention filter |
| PUT | /api/v2/apm/config/retention-filters-execution-order | Re-order retention filters |
| DELETE | /api/v2/apm/config/retention-filters/{filter_id} | Delete a retention filter |
| GET | /api/v2/apm/config/retention-filters/{filter_id} | Get a given APM retention filter |
| PUT | /api/v2/apm/config/retention-filters/{filter_id} | Update a retention filter |
| GET | /api/v2/apm/services | Get service list |
| DELETE | /api/v2/app-builder/apps | Delete Multiple Apps |
| GET | /api/v2/app-builder/apps | List Apps |
| POST | /api/v2/app-builder/apps | Create App |
| DELETE | /api/v2/app-builder/apps/{app_id} | Delete App |
| GET | /api/v2/app-builder/apps/{app_id} | Get App |
| PATCH | /api/v2/app-builder/apps/{app_id} | Update App |
| DELETE | /api/v2/app-builder/apps/{app_id}/deployment | Unpublish App |
| POST | /api/v2/app-builder/apps/{app_id}/deployment | Publish App |
| GET | /api/v2/application_keys | Get all application keys |
| DELETE | /api/v2/application_keys/{app_key_id} | Delete an application key |
| GET | /api/v2/application_keys/{app_key_id} | Get an application key |
| PATCH | /api/v2/application_keys/{app_key_id} | Edit an application key |
| GET | /api/v2/audit/events | Get a list of Audit Logs events |
| POST | /api/v2/audit/events/search | Search Audit Logs events |
| GET | /api/v2/authn_mappings | List all AuthN Mappings |
| POST | /api/v2/authn_mappings | Create an AuthN Mapping |
| DELETE | /api/v2/authn_mappings/{authn_mapping_id} | Delete an AuthN Mapping |
| GET | /api/v2/authn_mappings/{authn_mapping_id} | Get an AuthN Mapping by UUID |
| PATCH | /api/v2/authn_mappings/{authn_mapping_id} | Edit an AuthN Mapping |
| GET | /api/v2/cases | Search cases |
| POST | /api/v2/cases | Create a case |
| GET | /api/v2/cases/projects | Get all projects |
| POST | /api/v2/cases/projects | Create a project |
| DELETE | /api/v2/cases/projects/{project_id} | Remove a project |
| GET | /api/v2/cases/projects/{project_id} | Get the details of a project |
| PATCH | /api/v2/cases/projects/{project_id} | Update a project |
| GET | /api/v2/cases/projects/{project_id}/notification_rules | Get notification rules |
| POST | /api/v2/cases/projects/{project_id}/notification_rules | Create a notification rule |
| DELETE | /api/v2/cases/projects/{project_id}/notification_rules/{notification_rule_id} | Delete a notification rule |
| PUT | /api/v2/cases/projects/{project_id}/notification_rules/{notification_rule_id} | Update a notification rule |
| GET | /api/v2/cases/types | Get all case types |
| POST | /api/v2/cases/types | Create a case type |
| GET | /api/v2/cases/types/custom_attributes | Get all custom attributes |
| DELETE | /api/v2/cases/types/{case_type_id} | Delete a case type |
| GET | /api/v2/cases/types/{case_type_id}/custom_attributes | Get all custom attributes config of case type |
| POST | /api/v2/cases/types/{case_type_id}/custom_attributes | Create custom attribute config for a case type |
| DELETE | /api/v2/cases/types/{case_type_id}/custom_attributes/{custom_attribute_id} | Delete custom attributes config |
| GET | /api/v2/cases/{case_id} | Get the details of a case |
| POST | /api/v2/cases/{case_id}/archive | Archive case |
| POST | /api/v2/cases/{case_id}/assign | Assign case |
| POST | /api/v2/cases/{case_id}/attributes | Update case attributes |
| POST | /api/v2/cases/{case_id}/comment | Comment case |
| DELETE | /api/v2/cases/{case_id}/comment/{cell_id} | Delete case comment |
| DELETE | /api/v2/cases/{case_id}/custom_attributes/{custom_attribute_key} | Delete custom attribute from case |
| POST | /api/v2/cases/{case_id}/custom_attributes/{custom_attribute_key} | Update case custom attribute |
| POST | /api/v2/cases/{case_id}/description | Update case description |
| POST | /api/v2/cases/{case_id}/priority | Update case priority |
| POST | /api/v2/cases/{case_id}/relationships/incidents | Link incident to case |
| DELETE | /api/v2/cases/{case_id}/relationships/jira_issues | Remove Jira issue link from case |
| PATCH | /api/v2/cases/{case_id}/relationships/jira_issues | Link existing Jira issue to case |
| POST | /api/v2/cases/{case_id}/relationships/jira_issues | Create Jira issue for case |
| POST | /api/v2/cases/{case_id}/relationships/notebook | Create investigation notebook for case |
| PATCH | /api/v2/cases/{case_id}/relationships/project | Update case project |
| POST | /api/v2/cases/{case_id}/relationships/servicenow_tickets | Create ServiceNow ticket for case |
| POST | /api/v2/cases/{case_id}/status | Update case status |
| POST | /api/v2/cases/{case_id}/title | Update case title |
| POST | /api/v2/cases/{case_id}/unarchive | Unarchive case |
| POST | /api/v2/cases/{case_id}/unassign | Unassign case |
| GET | /api/v2/catalog/entity | Get a list of entities |
| POST | /api/v2/catalog/entity | Create or update entities |
| POST | /api/v2/catalog/entity/preview | Preview catalog entities |
| DELETE | /api/v2/catalog/entity/{entity_id} | Delete a single entity |
| GET | /api/v2/catalog/kind | Get a list of entity kinds |
| POST | /api/v2/catalog/kind | Create or update kinds |
| DELETE | /api/v2/catalog/kind/{kind_id} | Delete a single kind |
| GET | /api/v2/catalog/relation | Get a list of entity relations |
| POST | /api/v2/change-management/change-request | Create a change request |
| GET | /api/v2/change-management/change-request/{change_request_id} | Get a change request |
| PATCH | /api/v2/change-management/change-request/{change_request_id} | Update a change request |
| POST | /api/v2/change-management/change-request/{change_request_id}/branch | Create a change request branch |
| DELETE | /api/v2/change-management/change-request/{change_request_id}/decisions/{decision_id} | Delete a change request decision |
| PATCH | /api/v2/change-management/change-request/{change_request_id}/decisions/{decision_id} | Update a change request decision |
| POST | /api/v2/ci/pipeline | Send pipeline event |
| POST | /api/v2/ci/pipelines/analytics/aggregate | Aggregate pipelines events |
| GET | /api/v2/ci/pipelines/events | Get a list of pipelines events |
| POST | /api/v2/ci/pipelines/events/search | Search pipelines events |
| POST | /api/v2/ci/tests/analytics/aggregate | Aggregate tests events |
| GET | /api/v2/ci/tests/events | Get a list of tests events |
| POST | /api/v2/ci/tests/events/search | Search tests events |
| GET | /api/v2/cloud_auth/aws/persona_mapping | List AWS cloud authentication persona mappings |
| POST | /api/v2/cloud_auth/aws/persona_mapping | Create an AWS cloud authentication persona mapping |
| DELETE | /api/v2/cloud_auth/aws/persona_mapping/{persona_mapping_id} | Delete an AWS cloud authentication persona mapping |
| GET | /api/v2/cloud_auth/aws/persona_mapping/{persona_mapping_id} | Get an AWS cloud authentication persona mapping |
| POST | /api/v2/cloud_security_management/custom_frameworks | Create a custom framework |
| DELETE | /api/v2/cloud_security_management/custom_frameworks/{handle}/{version} | Delete a custom framework |
| GET | /api/v2/cloud_security_management/custom_frameworks/{handle}/{version} | Get a custom framework |
| PUT | /api/v2/cloud_security_management/custom_frameworks/{handle}/{version} | Update a custom framework |
| GET | /api/v2/cloud_security_management/resource_filters | List resource filters |
| PUT | /api/v2/cloud_security_management/resource_filters | Update resource filters |
| POST | /api/v2/code-coverage/branch/summary | Get code coverage summary for a branch |
| POST | /api/v2/code-coverage/commit/summary | Get code coverage summary for a commit |
| GET | /api/v2/container_images | Get all Container Images |
| GET | /api/v2/containers | Get All Containers |
| GET | /api/v2/cost/arbitrary_rule | List custom allocation rules |
| POST | /api/v2/cost/arbitrary_rule | Create custom allocation rule |
| POST | /api/v2/cost/arbitrary_rule/reorder | Reorder custom allocation rules |
| DELETE | /api/v2/cost/arbitrary_rule/{rule_id} | Delete custom allocation rule |
| GET | /api/v2/cost/arbitrary_rule/{rule_id} | Get custom allocation rule |
| PATCH | /api/v2/cost/arbitrary_rule/{rule_id} | Update custom allocation rule |
| GET | /api/v2/cost/aws_cur_config | List Cloud Cost Management AWS CUR configs |
| POST | /api/v2/cost/aws_cur_config | Create Cloud Cost Management AWS CUR config |
| DELETE | /api/v2/cost/aws_cur_config/{cloud_account_id} | Delete Cloud Cost Management AWS CUR config |
| GET | /api/v2/cost/aws_cur_config/{cloud_account_id} | Get cost AWS CUR config |
| PATCH | /api/v2/cost/aws_cur_config/{cloud_account_id} | Update Cloud Cost Management AWS CUR config |
| GET | /api/v2/cost/azure_uc_config | List Cloud Cost Management Azure configs |
| POST | /api/v2/cost/azure_uc_config | Create Cloud Cost Management Azure configs |
| DELETE | /api/v2/cost/azure_uc_config/{cloud_account_id} | Delete Cloud Cost Management Azure config |
| GET | /api/v2/cost/azure_uc_config/{cloud_account_id} | Get cost Azure UC config |
| PATCH | /api/v2/cost/azure_uc_config/{cloud_account_id} | Update Cloud Cost Management Azure config |
| PUT | /api/v2/cost/budget | Create or update a budget |
| POST | /api/v2/cost/budget/csv/validate | Validate CSV budget |
| POST | /api/v2/cost/budget/validate | Validate budget |
| DELETE | /api/v2/cost/budget/{budget_id} | Delete budget |
| GET | /api/v2/cost/budget/{budget_id} | Get budget |
| GET | /api/v2/cost/budgets | List budgets |
| GET | /api/v2/cost/custom_costs | List Custom Costs files |
| PUT | /api/v2/cost/custom_costs | Upload Custom Costs file |
| DELETE | /api/v2/cost/custom_costs/{file_id} | Delete Custom Costs file |
| GET | /api/v2/cost/custom_costs/{file_id} | Get Custom Costs file |
| GET | /api/v2/cost/gcp_uc_config | List Google Cloud Usage Cost configs |
| POST | /api/v2/cost/gcp_uc_config | Create Google Cloud Usage Cost config |
| DELETE | /api/v2/cost/gcp_uc_config/{cloud_account_id} | Delete Google Cloud Usage Cost config |
| GET | /api/v2/cost/gcp_uc_config/{cloud_account_id} | Get Google Cloud Usage Cost config |
| PATCH | /api/v2/cost/gcp_uc_config/{cloud_account_id} | Update Google Cloud Usage Cost config |
| GET | /api/v2/cost_by_tag/active_billing_dimensions | Get active billing dimensions for cost attribution |
| GET | /api/v2/cost_by_tag/monthly_cost_attribution | Get Monthly Cost Attribution |
| GET | /api/v2/csm/onboarding/agents | Get all CSM Agents |
| GET | /api/v2/csm/onboarding/coverage_analysis/cloud_accounts | Get the CSM Cloud Accounts Coverage Analysis |
| GET | /api/v2/csm/onboarding/coverage_analysis/hosts_and_containers | Get the CSM Hosts and Containers Coverage Analysis |
| GET | /api/v2/csm/onboarding/coverage_analysis/serverless | Get the CSM Serverless Coverage Analysis |
| GET | /api/v2/csm/onboarding/serverless/agents | Get all CSM Serverless Agents |
| GET | /api/v2/current_user/application_keys | Get all application keys owned by current user |
| POST | /api/v2/current_user/application_keys | Create an application key for current user |
| DELETE | /api/v2/current_user/application_keys/{app_key_id} | Delete an application key owned by current user |
| GET | /api/v2/current_user/application_keys/{app_key_id} | Get one application key owned by current user |
| PATCH | /api/v2/current_user/application_keys/{app_key_id} | Edit an application key owned by current user |
| DELETE | /api/v2/dashboard/lists/manual/{dashboard_list_id}/dashboards | Delete items from a dashboard list |
| GET | /api/v2/dashboard/lists/manual/{dashboard_list_id}/dashboards | Get items of a Dashboard List |
| POST | /api/v2/dashboard/lists/manual/{dashboard_list_id}/dashboards | Add Items to a Dashboard List |
| PUT | /api/v2/dashboard/lists/manual/{dashboard_list_id}/dashboards | Update items of a dashboard list |
| GET | /api/v2/datasets | Get all datasets |
| POST | /api/v2/datasets | Create a dataset |
| DELETE | /api/v2/datasets/{dataset_id} | Delete a dataset |
| GET | /api/v2/datasets/{dataset_id} | Get a single dataset by ID |
| PUT | /api/v2/datasets/{dataset_id} | Edit a dataset |
| POST | /api/v2/deletion/data/{product} | Creates a data deletion request |
| GET | /api/v2/deletion/requests | Gets a list of data deletion requests |
| PUT | /api/v2/deletion/requests/{id}/cancel | Cancels a data deletion request |
| POST | /api/v2/deployment_gates | Create deployment gate |
| GET | /api/v2/deployment_gates/{gate_id}/rules | Get rules for a deployment gate |
| POST | /api/v2/deployment_gates/{gate_id}/rules | Create deployment rule |
| DELETE | /api/v2/deployment_gates/{gate_id}/rules/{id} | Delete deployment rule |
| GET | /api/v2/deployment_gates/{gate_id}/rules/{id} | Get deployment rule |
| PUT | /api/v2/deployment_gates/{gate_id}/rules/{id} | Update deployment rule |
| DELETE | /api/v2/deployment_gates/{id} | Delete deployment gate |
| GET | /api/v2/deployment_gates/{id} | Get deployment gate |
| PUT | /api/v2/deployment_gates/{id} | Update deployment gate |
| GET | /api/v2/domain_allowlist | Get Domain Allowlist |
| PATCH | /api/v2/domain_allowlist | Sets Domain Allowlist |
| POST | /api/v2/dora/deployment | Send a deployment event |
| DELETE | /api/v2/dora/deployment/{deployment_id} | Delete a deployment event |
| POST | /api/v2/dora/deployments | Get a list of deployment events |
| GET | /api/v2/dora/deployments/{deployment_id} | Get a deployment event |
| PATCH | /api/v2/dora/deployments/{deployment_id} | Patch a deployment event |
| POST | /api/v2/dora/failure | Send an incident event |
| DELETE | /api/v2/dora/failure/{failure_id} | Delete an incident event |
| POST | /api/v2/dora/failures | Get a list of incident events |
| GET | /api/v2/dora/failures/{failure_id} | Get an incident event |
| POST | /api/v2/dora/incident | Send an incident event (legacy) |
| GET | /api/v2/downtime | Get all downtimes |
| POST | /api/v2/downtime | Schedule a downtime |
| DELETE | /api/v2/downtime/{downtime_id} | Cancel a downtime |
| GET | /api/v2/downtime/{downtime_id} | Get a downtime |
| PATCH | /api/v2/downtime/{downtime_id} | Update a downtime |
| POST | /api/v2/error-tracking/issues/search | Search error tracking issues |
| GET | /api/v2/error-tracking/issues/{issue_id} | Get the details of an error tracking issue |
| DELETE | /api/v2/error-tracking/issues/{issue_id}/assignee | Remove the assignee of an issue |
| PUT | /api/v2/error-tracking/issues/{issue_id}/assignee | Update the assignee of an issue |
| PUT | /api/v2/error-tracking/issues/{issue_id}/state | Update the state of an issue |
| GET | /api/v2/events | Get a list of events |
| POST | /api/v2/events | Post an event |
| POST | /api/v2/events/search | Search events |
| GET | /api/v2/events/{event_id} | Get an event |
| GET | /api/v2/hamr | Get HAMR organization connection |
| POST | /api/v2/hamr | Create or update HAMR organization connection |
| GET | /api/v2/incidents | Get a list of incidents |
| POST | /api/v2/incidents | Create an incident |
| DELETE | /api/v2/incidents/config/global/incident-handles | Delete global incident handle |
| GET | /api/v2/incidents/config/global/incident-handles | List global incident handles |
| POST | /api/v2/incidents/config/global/incident-handles | Create global incident handle |
| PUT | /api/v2/incidents/config/global/incident-handles | Update global incident handle |
| GET | /api/v2/incidents/config/global/settings | Get global incident settings |
| PATCH | /api/v2/incidents/config/global/settings | Update global incident settings |
| GET | /api/v2/incidents/config/notification-rules | List incident notification rules |
| POST | /api/v2/incidents/config/notification-rules | Create an incident notification rule |
| DELETE | /api/v2/incidents/config/notification-rules/{id} | Delete an incident notification rule |
| GET | /api/v2/incidents/config/notification-rules/{id} | Get an incident notification rule |
| PUT | /api/v2/incidents/config/notification-rules/{id} | Update an incident notification rule |
| GET | /api/v2/incidents/config/notification-templates | List incident notification templates |
| POST | /api/v2/incidents/config/notification-templates | Create incident notification template |
| DELETE | /api/v2/incidents/config/notification-templates/{id} | Delete a notification template |
| GET | /api/v2/incidents/config/notification-templates/{id} | Get incident notification template |
| PATCH | /api/v2/incidents/config/notification-templates/{id} | Update incident notification template |
| GET | /api/v2/incidents/config/postmortem-templates | List postmortem templates |
| POST | /api/v2/incidents/config/postmortem-templates | Create postmortem template |
| DELETE | /api/v2/incidents/config/postmortem-templates/{template_id} | Delete postmortem template |
| GET | /api/v2/incidents/config/postmortem-templates/{template_id} | Get postmortem template |
| PATCH | /api/v2/incidents/config/postmortem-templates/{template_id} | Update postmortem template |
| GET | /api/v2/incidents/config/types | Get a list of incident types |
| POST | /api/v2/incidents/config/types | Create an incident type |
| DELETE | /api/v2/incidents/config/types/{incident_type_id} | Delete an incident type |
| GET | /api/v2/incidents/config/types/{incident_type_id} | Get incident type details |
| PATCH | /api/v2/incidents/config/types/{incident_type_id} | Update an incident type |
| POST | /api/v2/incidents/import | Import an incident |
| GET | /api/v2/incidents/search | Search for incidents |
| DELETE | /api/v2/incidents/{incident_id} | Delete an existing incident |
| GET | /api/v2/incidents/{incident_id} | Get the details of an incident |
| PATCH | /api/v2/incidents/{incident_id} | Update an existing incident |
| GET | /api/v2/incidents/{incident_id}/attachments | List incident attachments |
| POST | /api/v2/incidents/{incident_id}/attachments | Create incident attachment |
| POST | /api/v2/incidents/{incident_id}/attachments/postmortems | Create postmortem attachment |
| DELETE | /api/v2/incidents/{incident_id}/attachments/{attachment_id} | Delete incident attachment |
| PATCH | /api/v2/incidents/{incident_id}/attachments/{attachment_id} | Update incident attachment |
| GET | /api/v2/incidents/{incident_id}/impacts | List an incident's impacts |
| POST | /api/v2/incidents/{incident_id}/impacts | Create an incident impact |
| DELETE | /api/v2/incidents/{incident_id}/impacts/{impact_id} | Delete an incident impact |
| GET | /api/v2/incidents/{incident_id}/relationships/integrations | Get a list of an incident's integration metadata |
| POST | /api/v2/incidents/{incident_id}/relationships/integrations | Create an incident integration metadata |
| DELETE | /api/v2/incidents/{incident_id}/relationships/integrations/{integration_metadata_id} | Delete an incident integration metadata |
| GET | /api/v2/incidents/{incident_id}/relationships/integrations/{integration_metadata_id} | Get incident integration metadata details |
| PATCH | /api/v2/incidents/{incident_id}/relationships/integrations/{integration_metadata_id} | Update an existing incident integration metadata |
| GET | /api/v2/incidents/{incident_id}/relationships/todos | Get a list of an incident's todos |
| POST | /api/v2/incidents/{incident_id}/relationships/todos | Create an incident todo |
| DELETE | /api/v2/incidents/{incident_id}/relationships/todos/{todo_id} | Delete an incident todo |
| GET | /api/v2/incidents/{incident_id}/relationships/todos/{todo_id} | Get incident todo details |
| PATCH | /api/v2/incidents/{incident_id}/relationships/todos/{todo_id} | Update an incident todo |
| GET | /api/v2/integration/aws/accounts | List all AWS integrations |
| POST | /api/v2/integration/aws/accounts | Create an AWS integration |
| DELETE | /api/v2/integration/aws/accounts/{aws_account_config_id} | Delete an AWS integration |
| GET | /api/v2/integration/aws/accounts/{aws_account_config_id} | Get an AWS integration by config ID |
| PATCH | /api/v2/integration/aws/accounts/{aws_account_config_id} | Update an AWS integration |
| DELETE | /api/v2/integration/aws/accounts/{aws_account_config_id}/ccm_config | Delete AWS CCM config |
| GET | /api/v2/integration/aws/accounts/{aws_account_config_id}/ccm_config | Get AWS CCM config |
| PATCH | /api/v2/integration/aws/accounts/{aws_account_config_id}/ccm_config | Update AWS CCM config |
| POST | /api/v2/integration/aws/accounts/{aws_account_config_id}/ccm_config | Create AWS CCM config |
| GET | /api/v2/integration/aws/available_namespaces | List available namespaces |
| DELETE | /api/v2/integration/aws/event_bridge | Delete an Amazon EventBridge source |
| GET | /api/v2/integration/aws/event_bridge | Get all Amazon EventBridge sources |
| POST | /api/v2/integration/aws/event_bridge | Create an Amazon EventBridge source |
| POST | /api/v2/integration/aws/generate_new_external_id | Generate a new external ID |
| GET | /api/v2/integration/aws/iam_permissions | Get AWS integration IAM permissions |
| GET | /api/v2/integration/aws/iam_permissions/resource_collection | Get resource collection IAM permissions |
| GET | /api/v2/integration/aws/iam_permissions/standard | Get AWS integration standard IAM permissions |
| GET | /api/v2/integration/aws/logs/services | Get list of AWS log ready services |
| GET | /api/v2/integration/gcp/accounts | List all GCP STS-enabled service accounts |
| POST | /api/v2/integration/gcp/accounts | Create a new entry for your service account |
| DELETE | /api/v2/integration/gcp/accounts/{account_id} | Delete an STS enabled GCP Account |
| PATCH | /api/v2/integration/gcp/accounts/{account_id} | Update STS Service Account |
| GET | /api/v2/integration/gcp/sts_delegate | List delegate account |
| POST | /api/v2/integration/gcp/sts_delegate | Create a Datadog GCP principal |
| GET | /api/v2/integration/google-chat/organizations/app/named-spaces/{domain_name}/{space_display_name} | Get space information by display name |
| GET | /api/v2/integration/google-chat/organizations/{organization_binding_id}/organization-handles | Get all organization handles |
| POST | /api/v2/integration/google-chat/organizations/{organization_binding_id}/organization-handles | Create organization handle |
| DELETE | /api/v2/integration/google-chat/organizations/{organization_binding_id}/organization-handles/{handle_id} | Delete organization handle |
| GET | /api/v2/integration/google-chat/organizations/{organization_binding_id}/organization-handles/{handle_id} | Get organization handle |
| PATCH | /api/v2/integration/google-chat/organizations/{organization_binding_id}/organization-handles/{handle_id} | Update organization handle |
| GET | /api/v2/integration/jira/accounts | List Jira accounts |
| DELETE | /api/v2/integration/jira/accounts/{account_id} | Delete Jira account |
| GET | /api/v2/integration/jira/issue-templates | List Jira issue templates |
| POST | /api/v2/integration/jira/issue-templates | Create Jira issue template |
| DELETE | /api/v2/integration/jira/issue-templates/{issue_template_id} | Delete Jira issue template |
| GET | /api/v2/integration/jira/issue-templates/{issue_template_id} | Get Jira issue template |
| PATCH | /api/v2/integration/jira/issue-templates/{issue_template_id} | Update Jira issue template |
| GET | /api/v2/integration/ms-teams/configuration/channel/{tenant_name}/{team_name}/{channel_name} | Get channel information by name |
| GET | /api/v2/integration/ms-teams/configuration/tenant-based-handles | Get all tenant-based handles |
| POST | /api/v2/integration/ms-teams/configuration/tenant-based-handles | Create tenant-based handle |
| DELETE | /api/v2/integration/ms-teams/configuration/tenant-based-handles/{handle_id} | Delete tenant-based handle |
| GET | /api/v2/integration/ms-teams/configuration/tenant-based-handles/{handle_id} | Get tenant-based handle information |
| PATCH | /api/v2/integration/ms-teams/configuration/tenant-based-handles/{handle_id} | Update tenant-based handle |
| GET | /api/v2/integration/ms-teams/configuration/workflows-webhook-handles | Get all Workflows webhook handles |
| POST | /api/v2/integration/ms-teams/configuration/workflows-webhook-handles | Create Workflows webhook handle |
| DELETE | /api/v2/integration/ms-teams/configuration/workflows-webhook-handles/{handle_id} | Delete Workflows webhook handle |
| GET | /api/v2/integration/ms-teams/configuration/workflows-webhook-handles/{handle_id} | Get Workflows webhook handle information |
| PATCH | /api/v2/integration/ms-teams/configuration/workflows-webhook-handles/{handle_id} | Update Workflows webhook handle |
| GET | /api/v2/integration/oci/products | List tenancy products |
| GET | /api/v2/integration/oci/tenancies | Get tenancy configs |
| POST | /api/v2/integration/oci/tenancies | Create tenancy config |
| DELETE | /api/v2/integration/oci/tenancies/{tenancy_ocid} | Delete tenancy config |
| GET | /api/v2/integration/oci/tenancies/{tenancy_ocid} | Get tenancy config |
| PATCH | /api/v2/integration/oci/tenancies/{tenancy_ocid} | Update tenancy config |
| GET | /api/v2/integration/opsgenie/services | Get all service objects |
| POST | /api/v2/integration/opsgenie/services | Create a new service object |
| DELETE | /api/v2/integration/opsgenie/services/{integration_service_id} | Delete a single service object |
| GET | /api/v2/integration/opsgenie/services/{integration_service_id} | Get a single service object |
| PATCH | /api/v2/integration/opsgenie/services/{integration_service_id} | Update a single service object |
| GET | /api/v2/integration/servicenow/assignment_groups/{instance_id} | List ServiceNow assignment groups |
| GET | /api/v2/integration/servicenow/business_services/{instance_id} | List ServiceNow business services |
| GET | /api/v2/integration/servicenow/handles | List ServiceNow templates |
| POST | /api/v2/integration/servicenow/handles | Create ServiceNow template |
| DELETE | /api/v2/integration/servicenow/handles/{template_id} | Delete ServiceNow template |
| GET | /api/v2/integration/servicenow/handles/{template_id} | Get ServiceNow template |
| PUT | /api/v2/integration/servicenow/handles/{template_id} | Update ServiceNow template |
| GET | /api/v2/integration/servicenow/instances | List ServiceNow instances |
| GET | /api/v2/integration/servicenow/users/{instance_id} | List ServiceNow users |
| GET | /api/v2/integrations | List Integrations |
| GET | /api/v2/integrations/cloudflare/accounts | List Cloudflare accounts |
| POST | /api/v2/integrations/cloudflare/accounts | Add Cloudflare account |
| DELETE | /api/v2/integrations/cloudflare/accounts/{account_id} | Delete Cloudflare account |
| GET | /api/v2/integrations/cloudflare/accounts/{account_id} | Get Cloudflare account |
| PATCH | /api/v2/integrations/cloudflare/accounts/{account_id} | Update Cloudflare account |
| GET | /api/v2/integrations/confluent-cloud/accounts | List Confluent accounts |
| POST | /api/v2/integrations/confluent-cloud/accounts | Add Confluent account |
| DELETE | /api/v2/integrations/confluent-cloud/accounts/{account_id} | Delete Confluent account |
| GET | /api/v2/integrations/confluent-cloud/accounts/{account_id} | Get Confluent account |
| PATCH | /api/v2/integrations/confluent-cloud/accounts/{account_id} | Update Confluent account |
| GET | /api/v2/integrations/confluent-cloud/accounts/{account_id}/resources | List Confluent Account resources |
| POST | /api/v2/integrations/confluent-cloud/accounts/{account_id}/resources | Add resource to Confluent account |
| DELETE | /api/v2/integrations/confluent-cloud/accounts/{account_id}/resources/{resource_id} | Delete resource from Confluent account |
| GET | /api/v2/integrations/confluent-cloud/accounts/{account_id}/resources/{resource_id} | Get resource from Confluent account |
| PATCH | /api/v2/integrations/confluent-cloud/accounts/{account_id}/resources/{resource_id} | Update resource in Confluent account |
| GET | /api/v2/integrations/fastly/accounts | List Fastly accounts |
| POST | /api/v2/integrations/fastly/accounts | Add Fastly account |
| DELETE | /api/v2/integrations/fastly/accounts/{account_id} | Delete Fastly account |
| GET | /api/v2/integrations/fastly/accounts/{account_id} | Get Fastly account |
| PATCH | /api/v2/integrations/fastly/accounts/{account_id} | Update Fastly account |
| GET | /api/v2/integrations/fastly/accounts/{account_id}/services | List Fastly services |
| POST | /api/v2/integrations/fastly/accounts/{account_id}/services | Add Fastly service |
| DELETE | /api/v2/integrations/fastly/accounts/{account_id}/services/{service_id} | Delete Fastly service |
| GET | /api/v2/integrations/fastly/accounts/{account_id}/services/{service_id} | Get Fastly service |
| PATCH | /api/v2/integrations/fastly/accounts/{account_id}/services/{service_id} | Update Fastly service |
| GET | /api/v2/integrations/okta/accounts | List Okta accounts |
| POST | /api/v2/integrations/okta/accounts | Add Okta account |
| DELETE | /api/v2/integrations/okta/accounts/{account_id} | Delete Okta account |
| GET | /api/v2/integrations/okta/accounts/{account_id} | Get Okta account |
| PATCH | /api/v2/integrations/okta/accounts/{account_id} | Update Okta account |
| GET | /api/v2/ip_allowlist | Get IP Allowlist |
| PATCH | /api/v2/ip_allowlist | Update IP Allowlist |
| GET | /api/v2/llm-obs/v1/experiments | List LLM Observability experiments |
| POST | /api/v2/llm-obs/v1/experiments | Create an LLM Observability experiment |
| POST | /api/v2/llm-obs/v1/experiments/delete | Delete LLM Observability experiments |
| PATCH | /api/v2/llm-obs/v1/experiments/{experiment_id} | Update an LLM Observability experiment |
| POST | /api/v2/llm-obs/v1/experiments/{experiment_id}/events | Push events for an LLM Observability experiment |
| GET | /api/v2/llm-obs/v1/projects | List LLM Observability projects |
| POST | /api/v2/llm-obs/v1/projects | Create an LLM Observability project |
| POST | /api/v2/llm-obs/v1/projects/delete | Delete LLM Observability projects |
| PATCH | /api/v2/llm-obs/v1/projects/{project_id} | Update an LLM Observability project |
| GET | /api/v2/llm-obs/v1/{project_id}/datasets | List LLM Observability datasets |
| POST | /api/v2/llm-obs/v1/{project_id}/datasets | Create an LLM Observability dataset |
| POST | /api/v2/llm-obs/v1/{project_id}/datasets/delete | Delete LLM Observability datasets |
| PATCH | /api/v2/llm-obs/v1/{project_id}/datasets/{dataset_id} | Update an LLM Observability dataset |
| GET | /api/v2/llm-obs/v1/{project_id}/datasets/{dataset_id}/records | List LLM Observability dataset records |
| PATCH | /api/v2/llm-obs/v1/{project_id}/datasets/{dataset_id}/records | Update LLM Observability dataset records |
| POST | /api/v2/llm-obs/v1/{project_id}/datasets/{dataset_id}/records | Append records to an LLM Observability dataset |
| POST | /api/v2/llm-obs/v1/{project_id}/datasets/{dataset_id}/records/delete | Delete LLM Observability dataset records |
| POST | /api/v2/logs | Send logs |
| POST | /api/v2/logs/analytics/aggregate | Aggregate events |
| GET | /api/v2/logs/config/archive-order | Get archive order |
| PUT | /api/v2/logs/config/archive-order | Update archive order |
| GET | /api/v2/logs/config/archives | Get all archives |
| POST | /api/v2/logs/config/archives | Create an archive |
| DELETE | /api/v2/logs/config/archives/{archive_id} | Delete an archive |
| GET | /api/v2/logs/config/archives/{archive_id} | Get an archive |
| PUT | /api/v2/logs/config/archives/{archive_id} | Update an archive |
| DELETE | /api/v2/logs/config/archives/{archive_id}/readers | Revoke role from an archive |
| GET | /api/v2/logs/config/archives/{archive_id}/readers | List read roles for an archive |
| POST | /api/v2/logs/config/archives/{archive_id}/readers | Grant role to an archive |
| GET | /api/v2/logs/config/custom-destinations | Get all custom destinations |
| POST | /api/v2/logs/config/custom-destinations | Create a custom destination |
| DELETE | /api/v2/logs/config/custom-destinations/{custom_destination_id} | Delete a custom destination |
| GET | /api/v2/logs/config/custom-destinations/{custom_destination_id} | Get a custom destination |
| PATCH | /api/v2/logs/config/custom-destinations/{custom_destination_id} | Update a custom destination |
| GET | /api/v2/logs/config/metrics | Get all log-based metrics |
| POST | /api/v2/logs/config/metrics | Create a log-based metric |
| DELETE | /api/v2/logs/config/metrics/{metric_id} | Delete a log-based metric |
| GET | /api/v2/logs/config/metrics/{metric_id} | Get a log-based metric |
| PATCH | /api/v2/logs/config/metrics/{metric_id} | Update a log-based metric |
| GET | /api/v2/logs/config/restriction_queries | List restriction queries |
| POST | /api/v2/logs/config/restriction_queries | Create a restriction query |
| GET | /api/v2/logs/config/restriction_queries/role/{role_id} | Get restriction query for a given role |
| GET | /api/v2/logs/config/restriction_queries/user/{user_id} | Get all restriction queries for a given user |
| DELETE | /api/v2/logs/config/restriction_queries/{restriction_query_id} | Delete a restriction query |
| GET | /api/v2/logs/config/restriction_queries/{restriction_query_id} | Get a restriction query |
| PATCH | /api/v2/logs/config/restriction_queries/{restriction_query_id} | Update a restriction query |
| PUT | /api/v2/logs/config/restriction_queries/{restriction_query_id} | Replace a restriction query |
| DELETE | /api/v2/logs/config/restriction_queries/{restriction_query_id}/roles | Revoke role from a restriction query |
| GET | /api/v2/logs/config/restriction_queries/{restriction_query_id}/roles | List roles for a restriction query |
| POST | /api/v2/logs/config/restriction_queries/{restriction_query_id}/roles | Grant role to a restriction query |
| GET | /api/v2/logs/events | Search logs (GET) |
| POST | /api/v2/logs/events/search | Search logs (POST) |
| GET | /api/v2/metrics | Get a list of metrics |
| DELETE | /api/v2/metrics/config/bulk-tags | Delete tags for multiple metrics |
| POST | /api/v2/metrics/config/bulk-tags | Configure tags for multiple metrics |
| GET | /api/v2/metrics/{metric_name}/active-configurations | List active tags and aggregations |
| GET | /api/v2/metrics/{metric_name}/all-tags | List tags by metric name |
| GET | /api/v2/metrics/{metric_name}/assets | Related Assets to a Metric |
| GET | /api/v2/metrics/{metric_name}/estimate | Tag Configuration Cardinality Estimator |
| GET | /api/v2/metrics/{metric_name}/tag-cardinalities | Get tag key cardinality details |
| DELETE | /api/v2/metrics/{metric_name}/tags | Delete a tag configuration |
| GET | /api/v2/metrics/{metric_name}/tags | List tag configuration by name |
| PATCH | /api/v2/metrics/{metric_name}/tags | Update a tag configuration |
| POST | /api/v2/metrics/{metric_name}/tags | Create a tag configuration |
| GET | /api/v2/metrics/{metric_name}/volumes | List distinct metric volumes by metric name |
| GET | /api/v2/monitor/notification_rule | Get all monitor notification rules |
| POST | /api/v2/monitor/notification_rule | Create a monitor notification rule |
| DELETE | /api/v2/monitor/notification_rule/{rule_id} | Delete a monitor notification rule |
| GET | /api/v2/monitor/notification_rule/{rule_id} | Get a monitor notification rule |
| PATCH | /api/v2/monitor/notification_rule/{rule_id} | Update a monitor notification rule |
| GET | /api/v2/monitor/policy | Get all monitor configuration policies |
| POST | /api/v2/monitor/policy | Create a monitor configuration policy |
| DELETE | /api/v2/monitor/policy/{policy_id} | Delete a monitor configuration policy |
| GET | /api/v2/monitor/policy/{policy_id} | Get a monitor configuration policy |
| PATCH | /api/v2/monitor/policy/{policy_id} | Edit a monitor configuration policy |
| GET | /api/v2/monitor/template | Get all monitor user templates |
| POST | /api/v2/monitor/template | Create a monitor user template |
| POST | /api/v2/monitor/template/validate | Validate a monitor user template |
| DELETE | /api/v2/monitor/template/{template_id} | Delete a monitor user template |
| GET | /api/v2/monitor/template/{template_id} | Get a monitor user template |
| PUT | /api/v2/monitor/template/{template_id} | Update a monitor user template to a new version |
| POST | /api/v2/monitor/template/{template_id}/validate | Validate an existing monitor user template |
| GET | /api/v2/monitor/{monitor_id}/downtime_matches | Get active downtimes for a monitor |
| GET | /api/v2/ndm/devices | Get the list of devices |
| GET | /api/v2/ndm/devices/{device_id} | Get the device details |
| GET | /api/v2/ndm/interfaces | Get the list of interfaces of the device |
| GET | /api/v2/ndm/tags/devices/{device_id} | Get the list of tags for a device |
| PATCH | /api/v2/ndm/tags/devices/{device_id} | Update the tags for a device |
| GET | /api/v2/ndm/tags/interfaces/{interface_id} | List tags for an interface |
| PATCH | /api/v2/ndm/tags/interfaces/{interface_id} | Update the tags for an interface |
| GET | /api/v2/network/connections/aggregate | Get all aggregated connections |
| GET | /api/v2/network/dns/aggregate | Get all aggregated DNS traffic |
| GET | /api/v2/obs-pipelines/pipelines | List pipelines |
| POST | /api/v2/obs-pipelines/pipelines | Create a new pipeline |
| POST | /api/v2/obs-pipelines/pipelines/validate | Validate an observability pipeline |
| DELETE | /api/v2/obs-pipelines/pipelines/{pipeline_id} | Delete a pipeline |
| GET | /api/v2/obs-pipelines/pipelines/{pipeline_id} | Get a specific pipeline |
| PUT | /api/v2/obs-pipelines/pipelines/{pipeline_id} | Update a pipeline |
| POST | /api/v2/on-call/escalation-policies | Create On-Call escalation policy |
| DELETE | /api/v2/on-call/escalation-policies/{policy_id} | Delete On-Call escalation policy |
| GET | /api/v2/on-call/escalation-policies/{policy_id} | Get On-Call escalation policy |
| PUT | /api/v2/on-call/escalation-policies/{policy_id} | Update On-Call escalation policy |
| POST | /api/v2/on-call/pages | Create On-Call Page |
| POST | /api/v2/on-call/pages/{page_id}/acknowledge | Acknowledge On-Call Page |
| POST | /api/v2/on-call/pages/{page_id}/escalate | Escalate On-Call Page |
| POST | /api/v2/on-call/pages/{page_id}/resolve | Resolve On-Call Page |
| POST | /api/v2/on-call/schedules | Create On-Call schedule |
| DELETE | /api/v2/on-call/schedules/{schedule_id} | Delete On-Call schedule |
| GET | /api/v2/on-call/schedules/{schedule_id} | Get On-Call schedule |
| PUT | /api/v2/on-call/schedules/{schedule_id} | Update On-Call schedule |
| GET | /api/v2/on-call/schedules/{schedule_id}/on-call | Get scheduled on-call user |
| GET | /api/v2/on-call/teams/{team_id}/on-call | Get team on-call users |
| GET | /api/v2/on-call/teams/{team_id}/routing-rules | Get On-Call team routing rules |
| PUT | /api/v2/on-call/teams/{team_id}/routing-rules | Set On-Call team routing rules |
| GET | /api/v2/on-call/users/{user_id}/notification-channels | List On-Call notification channels for a user |
| POST | /api/v2/on-call/users/{user_id}/notification-channels | Create an On-Call notification channel for a user |
| DELETE | /api/v2/on-call/users/{user_id}/notification-channels/{channel_id} | Delete an On-Call notification channel for a user |
| GET | /api/v2/on-call/users/{user_id}/notification-channels/{channel_id} | Get an On-Call notification channel for a user |
| GET | /api/v2/on-call/users/{user_id}/notification-rules | List On-Call notification rules for a user |
| POST | /api/v2/on-call/users/{user_id}/notification-rules | Create an On-Call notification rule for a user |
| DELETE | /api/v2/on-call/users/{user_id}/notification-rules/{rule_id} | Delete an On-Call notification rule for a user |
| GET | /api/v2/on-call/users/{user_id}/notification-rules/{rule_id} | Get an On-Call notification rule for a user |
| PUT | /api/v2/on-call/users/{user_id}/notification-rules/{rule_id} | Update an On-Call notification rule for a user |
| GET | /api/v2/org_configs | List Org Configs |
| GET | /api/v2/org_configs/{org_config_name} | Get a specific Org Config value |
| PATCH | /api/v2/org_configs/{org_config_name} | Update a specific Org Config |
| GET | /api/v2/org_connections | List Org Connections |
| POST | /api/v2/org_connections | Create Org Connection |
| DELETE | /api/v2/org_connections/{connection_id} | Delete Org Connection |
| PATCH | /api/v2/org_connections/{connection_id} | Update Org Connection |
| GET | /api/v2/permissions | List permissions |
| GET | /api/v2/posture_management/findings | List findings |
| PATCH | /api/v2/posture_management/findings | Mute or unmute a batch of findings |
| GET | /api/v2/posture_management/findings/{finding_id} | Get a finding |
| GET | /api/v2/powerpacks | Get all powerpacks |
| POST | /api/v2/powerpacks | Create a new powerpack |
| DELETE | /api/v2/powerpacks/{powerpack_id} | Delete a powerpack |
| GET | /api/v2/powerpacks/{powerpack_id} | Get a Powerpack |
| PATCH | /api/v2/powerpacks/{powerpack_id} | Update a powerpack |
| GET | /api/v2/processes | Get all processes |
| POST | /api/v2/prodlytics | Send server-side events |
| POST | /api/v2/product-analytics/accounts/facet_info | Get account facet info |
| POST | /api/v2/product-analytics/accounts/query | Query accounts |
| POST | /api/v2/product-analytics/analytics/scalar | Compute scalar analytics |
| POST | /api/v2/product-analytics/analytics/timeseries | Compute timeseries analytics |
| POST | /api/v2/product-analytics/users/event_filtered_query | Query event filtered users |
| POST | /api/v2/product-analytics/users/facet_info | Get user facet info |
| POST | /api/v2/product-analytics/users/query | Query users |
| GET | /api/v2/product-analytics/{entity}/mapping | Get mapping |
| POST | /api/v2/product-analytics/{entity}/mapping/connection | Create connection |
| PUT | /api/v2/product-analytics/{entity}/mapping/connection | Update connection |
| DELETE | /api/v2/product-analytics/{entity}/mapping/connection/{id} | Delete connection |
| GET | /api/v2/product-analytics/{entity}/mapping/connections | List connections |
| POST | /api/v2/query/scalar | Query scalar data across multiple products |
| POST | /api/v2/query/timeseries | Query timeseries data across multiple products |
| GET | /api/v2/reference-tables/tables | List tables |
| POST | /api/v2/reference-tables/tables | Create reference table |
| DELETE | /api/v2/reference-tables/tables/{id} | Delete table |
| GET | /api/v2/reference-tables/tables/{id} | Get table |
| PATCH | /api/v2/reference-tables/tables/{id} | Update reference table |
| DELETE | /api/v2/reference-tables/tables/{id}/rows | Delete rows |
| GET | /api/v2/reference-tables/tables/{id}/rows | Get rows by id |
| POST | /api/v2/reference-tables/tables/{id}/rows | Upsert rows |
| POST | /api/v2/reference-tables/uploads | Create reference table upload |
| GET | /api/v2/remote_config/products/asm/waf/custom_rules | List all WAF custom rules |
| POST | /api/v2/remote_config/products/asm/waf/custom_rules | Create a WAF custom rule |
| DELETE | /api/v2/remote_config/products/asm/waf/custom_rules/{custom_rule_id} | Delete a WAF Custom Rule |
| GET | /api/v2/remote_config/products/asm/waf/custom_rules/{custom_rule_id} | Get a WAF custom rule |
| PUT | /api/v2/remote_config/products/asm/waf/custom_rules/{custom_rule_id} | Update a WAF Custom Rule |
| GET | /api/v2/remote_config/products/asm/waf/exclusion_filters | List all WAF exclusion filters |
| POST | /api/v2/remote_config/products/asm/waf/exclusion_filters | Create a WAF exclusion filter |
| DELETE | /api/v2/remote_config/products/asm/waf/exclusion_filters/{exclusion_filter_id} | Delete a WAF exclusion filter |
| GET | /api/v2/remote_config/products/asm/waf/exclusion_filters/{exclusion_filter_id} | Get a WAF exclusion filter |
| PUT | /api/v2/remote_config/products/asm/waf/exclusion_filters/{exclusion_filter_id} | Update a WAF exclusion filter |
| GET | /api/v2/remote_config/products/cws/agent_rules | Get all Workload Protection agent rules |
| POST | /api/v2/remote_config/products/cws/agent_rules | Create a Workload Protection agent rule |
| DELETE | /api/v2/remote_config/products/cws/agent_rules/{agent_rule_id} | Delete a Workload Protection agent rule |
| GET | /api/v2/remote_config/products/cws/agent_rules/{agent_rule_id} | Get a Workload Protection agent rule |
| PATCH | /api/v2/remote_config/products/cws/agent_rules/{agent_rule_id} | Update a Workload Protection agent rule |
| GET | /api/v2/remote_config/products/cws/policy | Get all Workload Protection policies |
| POST | /api/v2/remote_config/products/cws/policy | Create a Workload Protection policy |
| GET | /api/v2/remote_config/products/cws/policy/download | Download the Workload Protection policy |
| DELETE | /api/v2/remote_config/products/cws/policy/{policy_id} | Delete a Workload Protection policy |
| GET | /api/v2/remote_config/products/cws/policy/{policy_id} | Get a Workload Protection policy |
| PATCH | /api/v2/remote_config/products/cws/policy/{policy_id} | Update a Workload Protection policy |
| GET | /api/v2/replay/heatmap/snapshots | List replay heatmap snapshots |
| POST | /api/v2/replay/heatmap/snapshots | Create replay heatmap snapshot |
| DELETE | /api/v2/replay/heatmap/snapshots/{snapshot_id} | Delete replay heatmap snapshot |
| PATCH | /api/v2/replay/heatmap/snapshots/{snapshot_id} | Update replay heatmap snapshot |
| DELETE | /api/v2/restriction_policy/{resource_id} | Delete a restriction policy |
| GET | /api/v2/restriction_policy/{resource_id} | Get a restriction policy |
| POST | /api/v2/restriction_policy/{resource_id} | Update a restriction policy |
| GET | /api/v2/roles | List roles |
| POST | /api/v2/roles | Create role |
| GET | /api/v2/roles/templates | List role templates |
| DELETE | /api/v2/roles/{role_id} | Delete role |
| GET | /api/v2/roles/{role_id} | Get a role |
| PATCH | /api/v2/roles/{role_id} | Update a role |
| POST | /api/v2/roles/{role_id}/clone | Create a new role by cloning an existing role |
| DELETE | /api/v2/roles/{role_id}/permissions | Revoke permission |
| GET | /api/v2/roles/{role_id}/permissions | List permissions for a role |
| POST | /api/v2/roles/{role_id}/permissions | Grant permission to a role |
| DELETE | /api/v2/roles/{role_id}/users | Remove a user from a role |
| GET | /api/v2/roles/{role_id}/users | Get all users of a role |
| POST | /api/v2/roles/{role_id}/users | Add a user to a role |
| POST | /api/v2/rum/analytics/aggregate | Aggregate RUM events |
| GET | /api/v2/rum/applications | List all the RUM applications |
| POST | /api/v2/rum/applications | Create a new RUM application |
| PATCH | /api/v2/rum/applications/{app_id}/relationships/retention_filters | Order RUM retention filters |
| GET | /api/v2/rum/applications/{app_id}/retention_filters | Get all RUM retention filters |
| POST | /api/v2/rum/applications/{app_id}/retention_filters | Create a RUM retention filter |
| DELETE | /api/v2/rum/applications/{app_id}/retention_filters/{rf_id} | Delete a RUM retention filter |
| GET | /api/v2/rum/applications/{app_id}/retention_filters/{rf_id} | Get a RUM retention filter |
| PATCH | /api/v2/rum/applications/{app_id}/retention_filters/{rf_id} | Update a RUM retention filter |
| DELETE | /api/v2/rum/applications/{id} | Delete a RUM application |
| GET | /api/v2/rum/applications/{id} | Get a RUM application |
| PATCH | /api/v2/rum/applications/{id} | Update a RUM application |
| GET | /api/v2/rum/config/metrics | Get all rum-based metrics |
| POST | /api/v2/rum/config/metrics | Create a rum-based metric |
| DELETE | /api/v2/rum/config/metrics/{metric_id} | Delete a rum-based metric |
| GET | /api/v2/rum/config/metrics/{metric_id} | Get a rum-based metric |
| PATCH | /api/v2/rum/config/metrics/{metric_id} | Update a rum-based metric |
| GET | /api/v2/rum/events | Get a list of RUM events |
| POST | /api/v2/rum/events/search | Search RUM events |
| GET | /api/v2/rum/replay/playlists | List rum replay playlists |
| POST | /api/v2/rum/replay/playlists | Create rum replay playlist |
| DELETE | /api/v2/rum/replay/playlists/{playlist_id} | Delete rum replay playlist |
| GET | /api/v2/rum/replay/playlists/{playlist_id} | Get rum replay playlist |
| PUT | /api/v2/rum/replay/playlists/{playlist_id} | Update rum replay playlist |
| DELETE | /api/v2/rum/replay/playlists/{playlist_id}/sessions | Bulk remove rum replay playlist sessions |
| GET | /api/v2/rum/replay/playlists/{playlist_id}/sessions | List rum replay playlist sessions |
| DELETE | /api/v2/rum/replay/playlists/{playlist_id}/sessions/{session_id} | Remove rum replay session from playlist |
| PUT | /api/v2/rum/replay/playlists/{playlist_id}/sessions/{session_id} | Add rum replay session to playlist |
| GET | /api/v2/rum/replay/sessions/{session_id}/views/{view_id}/segments | Get segments |
| GET | /api/v2/rum/replay/sessions/{session_id}/watchers | List rum replay session watchers |
| DELETE | /api/v2/rum/replay/sessions/{session_id}/watches | Delete rum replay session watch |
| POST | /api/v2/rum/replay/sessions/{session_id}/watches | Create rum replay session watch |
| GET | /api/v2/rum/replay/viewership-history/sessions | List rum replay viewership history sessions |
| POST | /api/v2/saml_configurations/idp_metadata | Upload IdP metadata |
| GET | /api/v2/scorecard/outcomes | List all rule outcomes |
| POST | /api/v2/scorecard/outcomes | Update Scorecard outcomes asynchronously |
| POST | /api/v2/scorecard/outcomes/batch | Create outcomes batch |
| GET | /api/v2/scorecard/rules | List all rules |
| POST | /api/v2/scorecard/rules | Create a new rule |
| DELETE | /api/v2/scorecard/rules/{rule_id} | Delete a rule |
| PUT | /api/v2/scorecard/rules/{rule_id} | Update an existing rule |
| DELETE | /api/v2/seats/users | Unassign seats from users |
| GET | /api/v2/seats/users | Get users with seats |
| POST | /api/v2/seats/users | Assign seats to users |
| GET | /api/v2/security-entities/risk-scores | List Entity Risk Scores |
| GET | /api/v2/security/cloud_workload/policy/download | Download the Workload Protection policy (US1-FED) |
| GET | /api/v2/security/findings | List security findings |
| DELETE | /api/v2/security/findings/cases | Detach security findings from their case |
| POST | /api/v2/security/findings/cases | Create cases for security findings |
| PATCH | /api/v2/security/findings/cases/{case_id} | Attach security findings to a case |
| PATCH | /api/v2/security/findings/jira_issues | Attach security findings to a Jira issue |
| POST | /api/v2/security/findings/jira_issues | Create Jira issues for security findings |
| POST | /api/v2/security/findings/search | Search security findings |
| GET | /api/v2/security/sboms | List assets SBOMs |
| GET | /api/v2/security/sboms/{asset_type} | Get SBOM |
| GET | /api/v2/security/scanned-assets-metadata | List scanned assets metadata |
| GET | /api/v2/security/signals/notification_rules | Get the list of signal-based notification rules |
| POST | /api/v2/security/signals/notification_rules | Create a new signal-based notification rule |
| DELETE | /api/v2/security/signals/notification_rules/{id} | Delete a signal-based notification rule |
| GET | /api/v2/security/signals/notification_rules/{id} | Get details of a signal-based notification rule |
| PATCH | /api/v2/security/signals/notification_rules/{id} | Patch a signal-based notification rule |
| GET | /api/v2/security/vulnerabilities | List vulnerabilities |
| GET | /api/v2/security/vulnerabilities/notification_rules | Get the list of vulnerability notification rules |
| POST | /api/v2/security/vulnerabilities/notification_rules | Create a new vulnerability-based notification rule |
| DELETE | /api/v2/security/vulnerabilities/notification_rules/{id} | Delete a vulnerability-based notification rule |
| GET | /api/v2/security/vulnerabilities/notification_rules/{id} | Get details of a vulnerability notification rule |
| PATCH | /api/v2/security/vulnerabilities/notification_rules/{id} | Patch a vulnerability-based notification rule |
| GET | /api/v2/security/vulnerable-assets | List vulnerable assets |
| GET | /api/v2/security_monitoring/cloud_workload_security/agent_rules | Get all Workload Protection agent rules (US1-FED) |
| POST | /api/v2/security_monitoring/cloud_workload_security/agent_rules | Create a Workload Protection agent rule (US1-FED) |
| DELETE | /api/v2/security_monitoring/cloud_workload_security/agent_rules/{agent_rule_id} | Delete a Workload Protection agent rule (US1-FED) |
| GET | /api/v2/security_monitoring/cloud_workload_security/agent_rules/{agent_rule_id} | Get a Workload Protection agent rule (US1-FED) |
| PATCH | /api/v2/security_monitoring/cloud_workload_security/agent_rules/{agent_rule_id} | Update a Workload Protection agent rule (US1-FED) |
| GET | /api/v2/security_monitoring/configuration/critical_assets | Get all critical assets |
| POST | /api/v2/security_monitoring/configuration/critical_assets | Create a critical asset |
| GET | /api/v2/security_monitoring/configuration/critical_assets/rules/{rule_id} | Get critical assets affecting a specific rule |
| DELETE | /api/v2/security_monitoring/configuration/critical_assets/{critical_asset_id} | Delete a critical asset |
| GET | /api/v2/security_monitoring/configuration/critical_assets/{critical_asset_id} | Get a critical asset |
| PATCH | /api/v2/security_monitoring/configuration/critical_assets/{critical_asset_id} | Update a critical asset |
| GET | /api/v2/security_monitoring/configuration/security_filters | Get all security filters |
| POST | /api/v2/security_monitoring/configuration/security_filters | Create a security filter |
| DELETE | /api/v2/security_monitoring/configuration/security_filters/{security_filter_id} | Delete a security filter |
| GET | /api/v2/security_monitoring/configuration/security_filters/{security_filter_id} | Get a security filter |
| PATCH | /api/v2/security_monitoring/configuration/security_filters/{security_filter_id} | Update a security filter |
| GET | /api/v2/security_monitoring/configuration/suppressions | Get all suppression rules |
| POST | /api/v2/security_monitoring/configuration/suppressions | Create a suppression rule |
| POST | /api/v2/security_monitoring/configuration/suppressions/rules | Get suppressions affecting future rule |
| GET | /api/v2/security_monitoring/configuration/suppressions/rules/{rule_id} | Get suppressions affecting a specific rule |
| POST | /api/v2/security_monitoring/configuration/suppressions/validation | Validate a suppression rule |
| DELETE | /api/v2/security_monitoring/configuration/suppressions/{suppression_id} | Delete a suppression rule |
| GET | /api/v2/security_monitoring/configuration/suppressions/{suppression_id} | Get a suppression rule |
| PATCH | /api/v2/security_monitoring/configuration/suppressions/{suppression_id} | Update a suppression rule |
| GET | /api/v2/security_monitoring/configuration/suppressions/{suppression_id}/version_history | Get a suppression's version history |
| GET | /api/v2/security_monitoring/content_packs/states | Get content pack states |
| PUT | /api/v2/security_monitoring/content_packs/{content_pack_id}/activate | Activate content pack |
| PUT | /api/v2/security_monitoring/content_packs/{content_pack_id}/deactivate | Deactivate content pack |
| GET | /api/v2/security_monitoring/rules | List rules |
| POST | /api/v2/security_monitoring/rules | Create a detection rule |
| POST | /api/v2/security_monitoring/rules/bulk_export | Bulk export security monitoring rules |
| POST | /api/v2/security_monitoring/rules/convert | Convert a rule from JSON to Terraform |
| POST | /api/v2/security_monitoring/rules/test | Test a rule |
| POST | /api/v2/security_monitoring/rules/validation | Validate a detection rule |
| DELETE | /api/v2/security_monitoring/rules/{rule_id} | Delete an existing rule |
| GET | /api/v2/security_monitoring/rules/{rule_id} | Get a rule's details |
| PUT | /api/v2/security_monitoring/rules/{rule_id} | Update an existing rule |
| GET | /api/v2/security_monitoring/rules/{rule_id}/convert | Convert an existing rule from JSON to Terraform |
| POST | /api/v2/security_monitoring/rules/{rule_id}/test | Test an existing rule |
| GET | /api/v2/security_monitoring/rules/{rule_id}/version_history | Get a rule's version history |
| GET | /api/v2/security_monitoring/signals | Get a quick list of security signals |
| POST | /api/v2/security_monitoring/signals/search | Get a list of security signals |
| GET | /api/v2/security_monitoring/signals/{signal_id} | Get a signal's details |
| PATCH | /api/v2/security_monitoring/signals/{signal_id}/assignee | Modify the triage assignee of a security signal |
| PATCH | /api/v2/security_monitoring/signals/{signal_id}/incidents | Change the related incidents of a security signal |
| PATCH | /api/v2/security_monitoring/signals/{signal_id}/state | Change the triage state of a security signal |
| GET | /api/v2/sensitive-data-scanner/config | List Scanning Groups |
| PATCH | /api/v2/sensitive-data-scanner/config | Reorder Groups |
| POST | /api/v2/sensitive-data-scanner/config/groups | Create Scanning Group |
| DELETE | /api/v2/sensitive-data-scanner/config/groups/{group_id} | Delete Scanning Group |
| PATCH | /api/v2/sensitive-data-scanner/config/groups/{group_id} | Update Scanning Group |
| POST | /api/v2/sensitive-data-scanner/config/rules | Create Scanning Rule |
| DELETE | /api/v2/sensitive-data-scanner/config/rules/{rule_id} | Delete Scanning Rule |
| PATCH | /api/v2/sensitive-data-scanner/config/rules/{rule_id} | Update Scanning Rule |
| GET | /api/v2/sensitive-data-scanner/config/standard-patterns | List standard patterns |
| POST | /api/v2/series | Submit metrics |
| POST | /api/v2/service_accounts | Create a service account |
| GET | /api/v2/service_accounts/{service_account_id}/application_keys | List application keys for this service account |
| POST | /api/v2/service_accounts/{service_account_id}/application_keys | Create an application key for this service account |
| DELETE | /api/v2/service_accounts/{service_account_id}/application_keys/{app_key_id} | Delete an application key for this service account |
| GET | /api/v2/service_accounts/{service_account_id}/application_keys/{app_key_id} | Get one application key for this service account |
| PATCH | /api/v2/service_accounts/{service_account_id}/application_keys/{app_key_id} | Edit an application key for this service account |
| GET | /api/v2/services | Get a list of all incident services |
| POST | /api/v2/services | Create a new incident service |
| GET | /api/v2/services/definitions | Get all service definitions |
| POST | /api/v2/services/definitions | Create or update service definition |
| DELETE | /api/v2/services/definitions/{service_name} | Delete a single service definition |
| GET | /api/v2/services/definitions/{service_name} | Get a single service definition |
| DELETE | /api/v2/services/{service_id} | Delete an existing incident service |
| GET | /api/v2/services/{service_id} | Get details of an incident service |
| PATCH | /api/v2/services/{service_id} | Update an existing incident service |
| GET | /api/v2/siem-threat-hunting/histsignals | List hist signals |
| GET | /api/v2/siem-threat-hunting/histsignals/search | Search hist signals |
| GET | /api/v2/siem-threat-hunting/histsignals/{histsignal_id} | Get a hist signal's details |
| GET | /api/v2/siem-threat-hunting/jobs | List threat hunting jobs |
| POST | /api/v2/siem-threat-hunting/jobs | Run a threat hunting job |
| POST | /api/v2/siem-threat-hunting/jobs/signal_convert | Convert a job result to a signal |
| DELETE | /api/v2/siem-threat-hunting/jobs/{job_id} | Delete an existing job |
| GET | /api/v2/siem-threat-hunting/jobs/{job_id} | Get a job's details |
| PATCH | /api/v2/siem-threat-hunting/jobs/{job_id}/cancel | Cancel a threat hunting job |
| GET | /api/v2/siem-threat-hunting/jobs/{job_id}/histsignals | Get a job's hist signals |
| POST | /api/v2/slo/report | Create a new SLO report |
| GET | /api/v2/slo/report/{report_id}/download | Get SLO report |
| GET | /api/v2/slo/report/{report_id}/status | Get SLO report status |
| GET | /api/v2/slo/{slo_id}/status | Get SLO status |
| GET | /api/v2/spa/recommendations/{service} | Get SPA Recommendations |
| GET | /api/v2/spa/recommendations/{service}/{shard} | Get SPA Recommendations with a shard parameter |
| POST | /api/v2/spans/analytics/aggregate | Aggregate spans |
| GET | /api/v2/spans/events | Get a list of spans |
| POST | /api/v2/spans/events/search | Search spans |
| POST | /api/v2/static-analysis-sca/dependencies | Post dependencies for analysis |
| POST | /api/v2/static-analysis-sca/vulnerabilities/resolve-vulnerable-symbols | POST request to resolve vulnerable symbols |
| DELETE | /api/v2/static-analysis/custom/rulesets/{ruleset_name} | Delete Custom Ruleset |
| GET | /api/v2/static-analysis/custom/rulesets/{ruleset_name} | Show Custom Ruleset |
| PATCH | /api/v2/static-analysis/custom/rulesets/{ruleset_name} | Update Custom Ruleset |
| PUT | /api/v2/static-analysis/custom/rulesets/{ruleset_name}/rules | Create Custom Rule |
| DELETE | /api/v2/static-analysis/custom/rulesets/{ruleset_name}/rules/{rule_name} | Delete Custom Rule |
| GET | /api/v2/static-analysis/custom/rulesets/{ruleset_name}/rules/{rule_name} | Show Custom Rule |
| GET | /api/v2/static-analysis/custom/rulesets/{ruleset_name}/rules/{rule_name}/revisions | List Custom Rule Revisions |
| PUT | /api/v2/static-analysis/custom/rulesets/{ruleset_name}/rules/{rule_name}/revisions | Create Custom Rule Revision |
| POST | /api/v2/static-analysis/custom/rulesets/{ruleset_name}/rules/{rule_name}/revisions/revert | Revert Custom Rule Revision |
| GET | /api/v2/static-analysis/custom/rulesets/{ruleset_name}/rules/{rule_name}/revisions/{id} | Show Custom Rule Revision |
| POST | /api/v2/static-analysis/rulesets | Ruleset get multiple |
| GET | /api/v2/static-analysis/secrets/rules | Returns a list of Secrets rules |
| GET | /api/v2/statuspages | List status pages |
| POST | /api/v2/statuspages | Create status page |
| GET | /api/v2/statuspages/degradations | List degradations |
| GET | /api/v2/statuspages/maintenances | List maintenances |
| DELETE | /api/v2/statuspages/{page_id} | Delete status page |
| GET | /api/v2/statuspages/{page_id} | Get status page |
| PATCH | /api/v2/statuspages/{page_id} | Update status page |
| GET | /api/v2/statuspages/{page_id}/components | List components |
| POST | /api/v2/statuspages/{page_id}/components | Create component |
| DELETE | /api/v2/statuspages/{page_id}/components/{component_id} | Delete component |
| GET | /api/v2/statuspages/{page_id}/components/{component_id} | Get component |
| PATCH | /api/v2/statuspages/{page_id}/components/{component_id} | Update component |
| POST | /api/v2/statuspages/{page_id}/degradations | Create degradation |
| DELETE | /api/v2/statuspages/{page_id}/degradations/{degradation_id} | Delete degradation |
| GET | /api/v2/statuspages/{page_id}/degradations/{degradation_id} | Get degradation |
| PATCH | /api/v2/statuspages/{page_id}/degradations/{degradation_id} | Update degradation |
| POST | /api/v2/statuspages/{page_id}/maintenances | Schedule maintenance |
| GET | /api/v2/statuspages/{page_id}/maintenances/{maintenance_id} | Get maintenance |
| PATCH | /api/v2/statuspages/{page_id}/maintenances/{maintenance_id} | Update maintenance |
| GET | /api/v2/synthetics/settings/on_demand_concurrency_cap | Get the on-demand concurrency cap |
| POST | /api/v2/synthetics/settings/on_demand_concurrency_cap | Save new value for on-demand concurrency cap |
| POST | /api/v2/synthetics/suites | Create a test suite |
| POST | /api/v2/synthetics/suites/bulk-delete | Bulk delete suites |
| GET | /api/v2/synthetics/suites/search | Search test suites |
| GET | /api/v2/synthetics/suites/{public_id} | Get a suite |
| PUT | /api/v2/synthetics/suites/{public_id} | Edit a test suite |
| POST | /api/v2/synthetics/tests/bulk-delete | Bulk delete tests |
| POST | /api/v2/synthetics/tests/network | Create a Network Path test |
| GET | /api/v2/synthetics/tests/network/{public_id} | Get a Network Path test |
| PUT | /api/v2/synthetics/tests/network/{public_id} | Edit a Network Path test |
| PATCH | /api/v2/synthetics/variables/{variable_id}/jsonpatch | Patch a global variable |
| GET | /api/v2/tags/enrichment | List tag pipeline rulesets |
| POST | /api/v2/tags/enrichment | Create tag pipeline ruleset |
| POST | /api/v2/tags/enrichment/reorder | Reorder tag pipeline rulesets |
| POST | /api/v2/tags/enrichment/validate-query | Validate query |
| DELETE | /api/v2/tags/enrichment/{ruleset_id} | Delete tag pipeline ruleset |
| GET | /api/v2/tags/enrichment/{ruleset_id} | Get a tag pipeline ruleset |
| PATCH | /api/v2/tags/enrichment/{ruleset_id} | Update tag pipeline ruleset |
| GET | /api/v2/team | Get all teams |
| POST | /api/v2/team | Create a team |
| GET | /api/v2/team-hierarchy-links | Get team hierarchy links |
| POST | /api/v2/team-hierarchy-links | Create a team hierarchy link |
| DELETE | /api/v2/team-hierarchy-links/{link_id} | Remove a team hierarchy link |
| GET | /api/v2/team-hierarchy-links/{link_id} | Get a team hierarchy link |
| DELETE | /api/v2/team/connections | Delete team connections |
| GET | /api/v2/team/connections | List team connections |
| POST | /api/v2/team/connections | Create team connections |
| GET | /api/v2/team/sync | Get team sync configurations |
| POST | /api/v2/team/sync | Link Teams with GitHub Teams |
| GET | /api/v2/team/{super_team_id}/member_teams | Get all member teams |
| POST | /api/v2/team/{super_team_id}/member_teams | Add a member team |
| DELETE | /api/v2/team/{super_team_id}/member_teams/{member_team_id} | Remove a member team |
| DELETE | /api/v2/team/{team_id} | Remove a team |
| GET | /api/v2/team/{team_id} | Get a team |
| PATCH | /api/v2/team/{team_id} | Update a team |
| GET | /api/v2/team/{team_id}/links | Get links for a team |
| POST | /api/v2/team/{team_id}/links | Create a team link |
| DELETE | /api/v2/team/{team_id}/links/{link_id} | Remove a team link |
| GET | /api/v2/team/{team_id}/links/{link_id} | Get a team link |
| PATCH | /api/v2/team/{team_id}/links/{link_id} | Update a team link |
| GET | /api/v2/team/{team_id}/memberships | Get team memberships |
| POST | /api/v2/team/{team_id}/memberships | Add a user to a team |
| DELETE | /api/v2/team/{team_id}/memberships/{user_id} | Remove a user from a team |
| PATCH | /api/v2/team/{team_id}/memberships/{user_id} | Update a user's membership attributes on a team |
| GET | /api/v2/team/{team_id}/notification-rules | Get team notification rules |
| POST | /api/v2/team/{team_id}/notification-rules | Create team notification rule |
| DELETE | /api/v2/team/{team_id}/notification-rules/{rule_id} | Delete team notification rule |
| GET | /api/v2/team/{team_id}/notification-rules/{rule_id} | Get team notification rule |
| PUT | /api/v2/team/{team_id}/notification-rules/{rule_id} | Update team notification rule |
| GET | /api/v2/team/{team_id}/permission-settings | Get permission settings for a team |
| PUT | /api/v2/team/{team_id}/permission-settings/{action} | Update permission setting for team |
| GET | /api/v2/teams | Get a list of all incident teams |
| POST | /api/v2/teams | Create a new incident team |
| DELETE | /api/v2/teams/{team_id} | Delete an existing incident team |
| GET | /api/v2/teams/{team_id} | Get details of an incident team |
| PATCH | /api/v2/teams/{team_id} | Update an existing incident team |
| PATCH | /api/v2/test/flaky-test-management/tests | Update flaky test states |
| POST | /api/v2/test/flaky-test-management/tests | Search flaky tests |
| GET | /api/v2/usage/application_security | Get hourly usage for application security |
| GET | /api/v2/usage/billing_dimension_mapping | Get billing dimension mapping for usage endpoints |
| GET | /api/v2/usage/cost_by_org | Get cost across multi-org account |
| GET | /api/v2/usage/estimated_cost | Get estimated cost across your account |
| GET | /api/v2/usage/historical_cost | Get historical cost across your account |
| GET | /api/v2/usage/hourly_usage | Get hourly usage by product family |
| GET | /api/v2/usage/lambda_traced_invocations | Get hourly usage for Lambda traced invocations |
| GET | /api/v2/usage/observability_pipelines | Get hourly usage for observability pipelines |
| GET | /api/v2/usage/projected_cost | Get projected cost across your account |
| GET | /api/v2/usage/usage-attribution-types | Get usage attribution types |
| POST | /api/v2/user_invitations | Send invitation emails |
| GET | /api/v2/user_invitations/{user_invitation_uuid} | Get a user invitation |
| GET | /api/v2/users | List all users |
| POST | /api/v2/users | Create a user |
| DELETE | /api/v2/users/{user_id} | Disable a user |
| GET | /api/v2/users/{user_id} | Get user details |
| PATCH | /api/v2/users/{user_id} | Update a user |
| GET | /api/v2/users/{user_id}/orgs | Get a user organization |
| GET | /api/v2/users/{user_id}/permissions | Get a user permissions |
| GET | /api/v2/users/{user_uuid}/memberships | Get user memberships |
| POST | /api/v2/workflows | Create a Workflow |
| DELETE | /api/v2/workflows/{workflow_id} | Delete an existing Workflow |
| GET | /api/v2/workflows/{workflow_id} | Get an existing Workflow |
| PATCH | /api/v2/workflows/{workflow_id} | Update an existing Workflow |
| GET | /api/v2/workflows/{workflow_id}/instances | List workflow instances |
| POST | /api/v2/workflows/{workflow_id}/instances | Execute a workflow |
| GET | /api/v2/workflows/{workflow_id}/instances/{instance_id} | Get a workflow instance |
| PUT | /api/v2/workflows/{workflow_id}/instances/{instance_id}/cancel | Cancel a workflow instance |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all agent_versions?" -> GET /api/unstable/fleet/agent_versions
- "List all agents?" -> GET /api/unstable/fleet/agents
- "Get agent details?" -> GET /api/unstable/fleet/agents/{agent_key}
- "List all deployments?" -> GET /api/unstable/fleet/deployments
- "Create a configure?" -> POST /api/unstable/fleet/deployments/configure
- "Create a upgrade?" -> POST /api/unstable/fleet/deployments/upgrade
- "Get deployment details?" -> GET /api/unstable/fleet/deployments/{deployment_id}
- "Create a cancel?" -> POST /api/unstable/fleet/deployments/{deployment_id}/cancel
- "List all schedules?" -> GET /api/unstable/fleet/schedules
- "Create a schedule?" -> POST /api/unstable/fleet/schedules
- "Delete a schedule?" -> DELETE /api/unstable/fleet/schedules/{id}
- "Get schedule details?" -> GET /api/unstable/fleet/schedules/{id}
- "Partially update a schedule?" -> PATCH /api/unstable/fleet/schedules/{id}
- "Create a trigger?" -> POST /api/unstable/fleet/schedules/{id}/trigger
- "List all actions-datastores?" -> GET /api/v2/actions-datastores
- "Create a actions-datastore?" -> POST /api/v2/actions-datastores
- "Delete a actions-datastore?" -> DELETE /api/v2/actions-datastores/{datastore_id}
- "Get actions-datastore details?" -> GET /api/v2/actions-datastores/{datastore_id}
- "Partially update a actions-datastore?" -> PATCH /api/v2/actions-datastores/{datastore_id}
- "List all items?" -> GET /api/v2/actions-datastores/{datastore_id}/items
- "Create a bulk?" -> POST /api/v2/actions-datastores/{datastore_id}/items/bulk
- "List all app_key_registrations?" -> GET /api/v2/actions/app_key_registrations
- "Delete a app_key_registration?" -> DELETE /api/v2/actions/app_key_registrations/{app_key_id}
- "Get app_key_registration details?" -> GET /api/v2/actions/app_key_registrations/{app_key_id}
- "Update a app_key_registration?" -> PUT /api/v2/actions/app_key_registrations/{app_key_id}
- "Create a connection?" -> POST /api/v2/actions/connections
- "Delete a connection?" -> DELETE /api/v2/actions/connections/{connection_id}
- "Get connection details?" -> GET /api/v2/actions/connections/{connection_id}
- "Partially update a connection?" -> PATCH /api/v2/actions/connections/{connection_id}
- "List all aws?" -> GET /api/v2/agentless_scanning/accounts/aws
- "Create a aw?" -> POST /api/v2/agentless_scanning/accounts/aws
- "Delete a aw?" -> DELETE /api/v2/agentless_scanning/accounts/aws/{account_id}
- "Get aw details?" -> GET /api/v2/agentless_scanning/accounts/aws/{account_id}
- "Partially update a aw?" -> PATCH /api/v2/agentless_scanning/accounts/aws/{account_id}
- "List all azure?" -> GET /api/v2/agentless_scanning/accounts/azure
- "Create a azure?" -> POST /api/v2/agentless_scanning/accounts/azure
- "Delete a azure?" -> DELETE /api/v2/agentless_scanning/accounts/azure/{subscription_id}
- "Get azure details?" -> GET /api/v2/agentless_scanning/accounts/azure/{subscription_id}
- "Partially update a azure?" -> PATCH /api/v2/agentless_scanning/accounts/azure/{subscription_id}
- "List all gcp?" -> GET /api/v2/agentless_scanning/accounts/gcp
- "Create a gcp?" -> POST /api/v2/agentless_scanning/accounts/gcp
- "Delete a gcp?" -> DELETE /api/v2/agentless_scanning/accounts/gcp/{project_id}
- "Get gcp details?" -> GET /api/v2/agentless_scanning/accounts/gcp/{project_id}
- "Partially update a gcp?" -> PATCH /api/v2/agentless_scanning/accounts/gcp/{project_id}
- "List all aws?" -> GET /api/v2/agentless_scanning/ondemand/aws
- "Create a aw?" -> POST /api/v2/agentless_scanning/ondemand/aws
- "Get aw details?" -> GET /api/v2/agentless_scanning/ondemand/aws/{task_id}
- "List all api_keys?" -> GET /api/v2/api_keys
- "Create a api_key?" -> POST /api/v2/api_keys
- "Delete a api_key?" -> DELETE /api/v2/api_keys/{api_key_id}
- "Get api_key details?" -> GET /api/v2/api_keys/{api_key_id}
- "Partially update a api_key?" -> PATCH /api/v2/api_keys/{api_key_id}
- "Search api?" -> GET /api/v2/apicatalog/api
- "Delete a api?" -> DELETE /api/v2/apicatalog/api/{id}
- "List all openapi?" -> GET /api/v2/apicatalog/api/{id}/openapi
- "Create a openapi?" -> POST /api/v2/apicatalog/openapi
- "List all metrics?" -> GET /api/v2/apm/config/metrics
- "Create a metric?" -> POST /api/v2/apm/config/metrics
- "Delete a metric?" -> DELETE /api/v2/apm/config/metrics/{metric_id}
- "Get metric details?" -> GET /api/v2/apm/config/metrics/{metric_id}
- "Partially update a metric?" -> PATCH /api/v2/apm/config/metrics/{metric_id}
- "List all retention-filters?" -> GET /api/v2/apm/config/retention-filters
- "Create a retention-filter?" -> POST /api/v2/apm/config/retention-filters
- "Delete a retention-filter?" -> DELETE /api/v2/apm/config/retention-filters/{filter_id}
- "Get retention-filter details?" -> GET /api/v2/apm/config/retention-filters/{filter_id}
- "Update a retention-filter?" -> PUT /api/v2/apm/config/retention-filters/{filter_id}
- "List all services?" -> GET /api/v2/apm/services
- "List all apps?" -> GET /api/v2/app-builder/apps
- "Create a app?" -> POST /api/v2/app-builder/apps
- "Delete a app?" -> DELETE /api/v2/app-builder/apps/{app_id}
- "Get app details?" -> GET /api/v2/app-builder/apps/{app_id}
- "Partially update a app?" -> PATCH /api/v2/app-builder/apps/{app_id}
- "Create a deployment?" -> POST /api/v2/app-builder/apps/{app_id}/deployment
- "List all application_keys?" -> GET /api/v2/application_keys
- "Delete a application_key?" -> DELETE /api/v2/application_keys/{app_key_id}
- "Get application_key details?" -> GET /api/v2/application_keys/{app_key_id}
- "Partially update a application_key?" -> PATCH /api/v2/application_keys/{app_key_id}
- "List all events?" -> GET /api/v2/audit/events
- "Create a search?" -> POST /api/v2/audit/events/search
- "List all authn_mappings?" -> GET /api/v2/authn_mappings
- "Create a authn_mapping?" -> POST /api/v2/authn_mappings
- "Delete a authn_mapping?" -> DELETE /api/v2/authn_mappings/{authn_mapping_id}
- "Get authn_mapping details?" -> GET /api/v2/authn_mappings/{authn_mapping_id}
- "Partially update a authn_mapping?" -> PATCH /api/v2/authn_mappings/{authn_mapping_id}
- "List all cases?" -> GET /api/v2/cases
- "Create a case?" -> POST /api/v2/cases
- "List all projects?" -> GET /api/v2/cases/projects
- "Create a project?" -> POST /api/v2/cases/projects
- "Delete a project?" -> DELETE /api/v2/cases/projects/{project_id}
- "Get project details?" -> GET /api/v2/cases/projects/{project_id}
- "Partially update a project?" -> PATCH /api/v2/cases/projects/{project_id}
- "List all notification_rules?" -> GET /api/v2/cases/projects/{project_id}/notification_rules
- "Create a notification_rule?" -> POST /api/v2/cases/projects/{project_id}/notification_rules
- "Delete a notification_rule?" -> DELETE /api/v2/cases/projects/{project_id}/notification_rules/{notification_rule_id}
- "Update a notification_rule?" -> PUT /api/v2/cases/projects/{project_id}/notification_rules/{notification_rule_id}
- "List all types?" -> GET /api/v2/cases/types
- "Create a type?" -> POST /api/v2/cases/types
- "List all custom_attributes?" -> GET /api/v2/cases/types/custom_attributes
- "Delete a type?" -> DELETE /api/v2/cases/types/{case_type_id}
- "List all custom_attributes?" -> GET /api/v2/cases/types/{case_type_id}/custom_attributes
- "Create a custom_attribute?" -> POST /api/v2/cases/types/{case_type_id}/custom_attributes
- "Delete a custom_attribute?" -> DELETE /api/v2/cases/types/{case_type_id}/custom_attributes/{custom_attribute_id}
- "Get case details?" -> GET /api/v2/cases/{case_id}
- "Create a archive?" -> POST /api/v2/cases/{case_id}/archive
- "Create a assign?" -> POST /api/v2/cases/{case_id}/assign
- "Create a attribute?" -> POST /api/v2/cases/{case_id}/attributes
- "Create a comment?" -> POST /api/v2/cases/{case_id}/comment
- "Delete a comment?" -> DELETE /api/v2/cases/{case_id}/comment/{cell_id}
- "Delete a custom_attribute?" -> DELETE /api/v2/cases/{case_id}/custom_attributes/{custom_attribute_key}
- "Create a description?" -> POST /api/v2/cases/{case_id}/description
- "Create a priority?" -> POST /api/v2/cases/{case_id}/priority
- "Create a incident?" -> POST /api/v2/cases/{case_id}/relationships/incidents
- "Create a jira_issue?" -> POST /api/v2/cases/{case_id}/relationships/jira_issues
- "Create a notebook?" -> POST /api/v2/cases/{case_id}/relationships/notebook
- "Create a servicenow_ticket?" -> POST /api/v2/cases/{case_id}/relationships/servicenow_tickets
- "Create a status?" -> POST /api/v2/cases/{case_id}/status
- "Create a title?" -> POST /api/v2/cases/{case_id}/title
- "Create a unarchive?" -> POST /api/v2/cases/{case_id}/unarchive
- "Create a unassign?" -> POST /api/v2/cases/{case_id}/unassign
- "List all entity?" -> GET /api/v2/catalog/entity
- "Create a entity?" -> POST /api/v2/catalog/entity
- "Create a preview?" -> POST /api/v2/catalog/entity/preview
- "Delete a entity?" -> DELETE /api/v2/catalog/entity/{entity_id}
- "List all kind?" -> GET /api/v2/catalog/kind
- "Create a kind?" -> POST /api/v2/catalog/kind
- "Delete a kind?" -> DELETE /api/v2/catalog/kind/{kind_id}
- "List all relation?" -> GET /api/v2/catalog/relation
- "Create a change-request?" -> POST /api/v2/change-management/change-request
- "Get change-request details?" -> GET /api/v2/change-management/change-request/{change_request_id}
- "Partially update a change-request?" -> PATCH /api/v2/change-management/change-request/{change_request_id}
- "Create a branch?" -> POST /api/v2/change-management/change-request/{change_request_id}/branch
- "Delete a decision?" -> DELETE /api/v2/change-management/change-request/{change_request_id}/decisions/{decision_id}
- "Partially update a decision?" -> PATCH /api/v2/change-management/change-request/{change_request_id}/decisions/{decision_id}
- "Create a pipeline?" -> POST /api/v2/ci/pipeline
- "Create a aggregate?" -> POST /api/v2/ci/pipelines/analytics/aggregate
- "List all events?" -> GET /api/v2/ci/pipelines/events
- "Create a search?" -> POST /api/v2/ci/pipelines/events/search
- "Create a aggregate?" -> POST /api/v2/ci/tests/analytics/aggregate
- "List all events?" -> GET /api/v2/ci/tests/events
- "Create a search?" -> POST /api/v2/ci/tests/events/search
- "List all persona_mapping?" -> GET /api/v2/cloud_auth/aws/persona_mapping
- "Create a persona_mapping?" -> POST /api/v2/cloud_auth/aws/persona_mapping
- "Delete a persona_mapping?" -> DELETE /api/v2/cloud_auth/aws/persona_mapping/{persona_mapping_id}
- "Get persona_mapping details?" -> GET /api/v2/cloud_auth/aws/persona_mapping/{persona_mapping_id}
- "Create a custom_framework?" -> POST /api/v2/cloud_security_management/custom_frameworks
- "Delete a custom_framework?" -> DELETE /api/v2/cloud_security_management/custom_frameworks/{handle}/{version}
- "Get custom_framework details?" -> GET /api/v2/cloud_security_management/custom_frameworks/{handle}/{version}
- "Update a custom_framework?" -> PUT /api/v2/cloud_security_management/custom_frameworks/{handle}/{version}
- "List all resource_filters?" -> GET /api/v2/cloud_security_management/resource_filters
- "Create a summary?" -> POST /api/v2/code-coverage/branch/summary
- "Create a summary?" -> POST /api/v2/code-coverage/commit/summary
- "List all container_images?" -> GET /api/v2/container_images
- "List all containers?" -> GET /api/v2/containers
- "List all arbitrary_rule?" -> GET /api/v2/cost/arbitrary_rule
- "Create a arbitrary_rule?" -> POST /api/v2/cost/arbitrary_rule
- "Create a reorder?" -> POST /api/v2/cost/arbitrary_rule/reorder
- "Delete a arbitrary_rule?" -> DELETE /api/v2/cost/arbitrary_rule/{rule_id}
- "Get arbitrary_rule details?" -> GET /api/v2/cost/arbitrary_rule/{rule_id}
- "Partially update a arbitrary_rule?" -> PATCH /api/v2/cost/arbitrary_rule/{rule_id}
- "List all aws_cur_config?" -> GET /api/v2/cost/aws_cur_config
- "Create a aws_cur_config?" -> POST /api/v2/cost/aws_cur_config
- "Delete a aws_cur_config?" -> DELETE /api/v2/cost/aws_cur_config/{cloud_account_id}
- "Get aws_cur_config details?" -> GET /api/v2/cost/aws_cur_config/{cloud_account_id}
- "Partially update a aws_cur_config?" -> PATCH /api/v2/cost/aws_cur_config/{cloud_account_id}
- "List all azure_uc_config?" -> GET /api/v2/cost/azure_uc_config
- "Create a azure_uc_config?" -> POST /api/v2/cost/azure_uc_config
- "Delete a azure_uc_config?" -> DELETE /api/v2/cost/azure_uc_config/{cloud_account_id}
- "Get azure_uc_config details?" -> GET /api/v2/cost/azure_uc_config/{cloud_account_id}
- "Partially update a azure_uc_config?" -> PATCH /api/v2/cost/azure_uc_config/{cloud_account_id}
- "Create a validate?" -> POST /api/v2/cost/budget/csv/validate
- "Create a validate?" -> POST /api/v2/cost/budget/validate
- "Delete a budget?" -> DELETE /api/v2/cost/budget/{budget_id}
- "Get budget details?" -> GET /api/v2/cost/budget/{budget_id}
- "List all budgets?" -> GET /api/v2/cost/budgets
- "List all custom_costs?" -> GET /api/v2/cost/custom_costs
- "Delete a custom_cost?" -> DELETE /api/v2/cost/custom_costs/{file_id}
- "Get custom_cost details?" -> GET /api/v2/cost/custom_costs/{file_id}
- "List all gcp_uc_config?" -> GET /api/v2/cost/gcp_uc_config
- "Create a gcp_uc_config?" -> POST /api/v2/cost/gcp_uc_config
- "Delete a gcp_uc_config?" -> DELETE /api/v2/cost/gcp_uc_config/{cloud_account_id}
- "Get gcp_uc_config details?" -> GET /api/v2/cost/gcp_uc_config/{cloud_account_id}
- "Partially update a gcp_uc_config?" -> PATCH /api/v2/cost/gcp_uc_config/{cloud_account_id}
- "List all active_billing_dimensions?" -> GET /api/v2/cost_by_tag/active_billing_dimensions
- "List all monthly_cost_attribution?" -> GET /api/v2/cost_by_tag/monthly_cost_attribution
- "Search agents?" -> GET /api/v2/csm/onboarding/agents
- "List all cloud_accounts?" -> GET /api/v2/csm/onboarding/coverage_analysis/cloud_accounts
- "List all hosts_and_containers?" -> GET /api/v2/csm/onboarding/coverage_analysis/hosts_and_containers
- "List all serverless?" -> GET /api/v2/csm/onboarding/coverage_analysis/serverless
- "Search agents?" -> GET /api/v2/csm/onboarding/serverless/agents
- "List all application_keys?" -> GET /api/v2/current_user/application_keys
- "Create a application_key?" -> POST /api/v2/current_user/application_keys
- "Delete a application_key?" -> DELETE /api/v2/current_user/application_keys/{app_key_id}
- "Get application_key details?" -> GET /api/v2/current_user/application_keys/{app_key_id}
- "Partially update a application_key?" -> PATCH /api/v2/current_user/application_keys/{app_key_id}
- "List all dashboards?" -> GET /api/v2/dashboard/lists/manual/{dashboard_list_id}/dashboards
- "Create a dashboard?" -> POST /api/v2/dashboard/lists/manual/{dashboard_list_id}/dashboards
- "List all datasets?" -> GET /api/v2/datasets
- "Create a dataset?" -> POST /api/v2/datasets
- "Delete a dataset?" -> DELETE /api/v2/datasets/{dataset_id}
- "Get dataset details?" -> GET /api/v2/datasets/{dataset_id}
- "Update a dataset?" -> PUT /api/v2/datasets/{dataset_id}
- "Search requests?" -> GET /api/v2/deletion/requests
- "Create a deployment_gate?" -> POST /api/v2/deployment_gates
- "List all rules?" -> GET /api/v2/deployment_gates/{gate_id}/rules
- "Create a rule?" -> POST /api/v2/deployment_gates/{gate_id}/rules
- "Delete a rule?" -> DELETE /api/v2/deployment_gates/{gate_id}/rules/{id}
- "Get rule details?" -> GET /api/v2/deployment_gates/{gate_id}/rules/{id}
- "Update a rule?" -> PUT /api/v2/deployment_gates/{gate_id}/rules/{id}
- "Delete a deployment_gate?" -> DELETE /api/v2/deployment_gates/{id}
- "Get deployment_gate details?" -> GET /api/v2/deployment_gates/{id}
- "Update a deployment_gate?" -> PUT /api/v2/deployment_gates/{id}
- "List all domain_allowlist?" -> GET /api/v2/domain_allowlist
- "Create a deployment?" -> POST /api/v2/dora/deployment
- "Delete a deployment?" -> DELETE /api/v2/dora/deployment/{deployment_id}
- "Create a deployment?" -> POST /api/v2/dora/deployments
- "Get deployment details?" -> GET /api/v2/dora/deployments/{deployment_id}
- "Partially update a deployment?" -> PATCH /api/v2/dora/deployments/{deployment_id}
- "Create a failure?" -> POST /api/v2/dora/failure
- "Delete a failure?" -> DELETE /api/v2/dora/failure/{failure_id}
- "Create a failure?" -> POST /api/v2/dora/failures
- "Get failure details?" -> GET /api/v2/dora/failures/{failure_id}
- "Create a incident?" -> POST /api/v2/dora/incident
- "List all downtime?" -> GET /api/v2/downtime
- "Create a downtime?" -> POST /api/v2/downtime
- "Delete a downtime?" -> DELETE /api/v2/downtime/{downtime_id}
- "Get downtime details?" -> GET /api/v2/downtime/{downtime_id}
- "Partially update a downtime?" -> PATCH /api/v2/downtime/{downtime_id}
- "Create a search?" -> POST /api/v2/error-tracking/issues/search
- "Get issue details?" -> GET /api/v2/error-tracking/issues/{issue_id}
- "List all events?" -> GET /api/v2/events
- "Create a event?" -> POST /api/v2/events
- "Create a search?" -> POST /api/v2/events/search
- "Get event details?" -> GET /api/v2/events/{event_id}
- "List all hamr?" -> GET /api/v2/hamr
- "Create a hamr?" -> POST /api/v2/hamr
- "List all incidents?" -> GET /api/v2/incidents
- "Create a incident?" -> POST /api/v2/incidents
- "List all incident-handles?" -> GET /api/v2/incidents/config/global/incident-handles
- "Create a incident-handle?" -> POST /api/v2/incidents/config/global/incident-handles
- "List all settings?" -> GET /api/v2/incidents/config/global/settings
- "List all notification-rules?" -> GET /api/v2/incidents/config/notification-rules
- "Create a notification-rule?" -> POST /api/v2/incidents/config/notification-rules
- "Delete a notification-rule?" -> DELETE /api/v2/incidents/config/notification-rules/{id}
- "Get notification-rule details?" -> GET /api/v2/incidents/config/notification-rules/{id}
- "Update a notification-rule?" -> PUT /api/v2/incidents/config/notification-rules/{id}
- "List all notification-templates?" -> GET /api/v2/incidents/config/notification-templates
- "Create a notification-template?" -> POST /api/v2/incidents/config/notification-templates
- "Delete a notification-template?" -> DELETE /api/v2/incidents/config/notification-templates/{id}
- "Get notification-template details?" -> GET /api/v2/incidents/config/notification-templates/{id}
- "Partially update a notification-template?" -> PATCH /api/v2/incidents/config/notification-templates/{id}
- "List all postmortem-templates?" -> GET /api/v2/incidents/config/postmortem-templates
- "Create a postmortem-template?" -> POST /api/v2/incidents/config/postmortem-templates
- "Delete a postmortem-template?" -> DELETE /api/v2/incidents/config/postmortem-templates/{template_id}
- "Get postmortem-template details?" -> GET /api/v2/incidents/config/postmortem-templates/{template_id}
- "Partially update a postmortem-template?" -> PATCH /api/v2/incidents/config/postmortem-templates/{template_id}
- "List all types?" -> GET /api/v2/incidents/config/types
- "Create a type?" -> POST /api/v2/incidents/config/types
- "Delete a type?" -> DELETE /api/v2/incidents/config/types/{incident_type_id}
- "Get type details?" -> GET /api/v2/incidents/config/types/{incident_type_id}
- "Partially update a type?" -> PATCH /api/v2/incidents/config/types/{incident_type_id}
- "Create a import?" -> POST /api/v2/incidents/import
- "Search search?" -> GET /api/v2/incidents/search
- "Delete a incident?" -> DELETE /api/v2/incidents/{incident_id}
- "Get incident details?" -> GET /api/v2/incidents/{incident_id}
- "Partially update a incident?" -> PATCH /api/v2/incidents/{incident_id}
- "List all attachments?" -> GET /api/v2/incidents/{incident_id}/attachments
- "Create a attachment?" -> POST /api/v2/incidents/{incident_id}/attachments
- "Create a postmortem?" -> POST /api/v2/incidents/{incident_id}/attachments/postmortems
- "Delete a attachment?" -> DELETE /api/v2/incidents/{incident_id}/attachments/{attachment_id}
- "Partially update a attachment?" -> PATCH /api/v2/incidents/{incident_id}/attachments/{attachment_id}
- "List all impacts?" -> GET /api/v2/incidents/{incident_id}/impacts
- "Create a impact?" -> POST /api/v2/incidents/{incident_id}/impacts
- "Delete a impact?" -> DELETE /api/v2/incidents/{incident_id}/impacts/{impact_id}
- "List all integrations?" -> GET /api/v2/incidents/{incident_id}/relationships/integrations
- "Create a integration?" -> POST /api/v2/incidents/{incident_id}/relationships/integrations
- "Delete a integration?" -> DELETE /api/v2/incidents/{incident_id}/relationships/integrations/{integration_metadata_id}
- "Get integration details?" -> GET /api/v2/incidents/{incident_id}/relationships/integrations/{integration_metadata_id}
- "Partially update a integration?" -> PATCH /api/v2/incidents/{incident_id}/relationships/integrations/{integration_metadata_id}
- "List all todos?" -> GET /api/v2/incidents/{incident_id}/relationships/todos
- "Create a todo?" -> POST /api/v2/incidents/{incident_id}/relationships/todos
- "Delete a todo?" -> DELETE /api/v2/incidents/{incident_id}/relationships/todos/{todo_id}
- "Get todo details?" -> GET /api/v2/incidents/{incident_id}/relationships/todos/{todo_id}
- "Partially update a todo?" -> PATCH /api/v2/incidents/{incident_id}/relationships/todos/{todo_id}
- "List all accounts?" -> GET /api/v2/integration/aws/accounts
- "Create a account?" -> POST /api/v2/integration/aws/accounts
- "Delete a account?" -> DELETE /api/v2/integration/aws/accounts/{aws_account_config_id}
- "Get account details?" -> GET /api/v2/integration/aws/accounts/{aws_account_config_id}
- "Partially update a account?" -> PATCH /api/v2/integration/aws/accounts/{aws_account_config_id}
- "List all ccm_config?" -> GET /api/v2/integration/aws/accounts/{aws_account_config_id}/ccm_config
- "Create a ccm_config?" -> POST /api/v2/integration/aws/accounts/{aws_account_config_id}/ccm_config
- "List all available_namespaces?" -> GET /api/v2/integration/aws/available_namespaces
- "List all event_bridge?" -> GET /api/v2/integration/aws/event_bridge
- "Create a event_bridge?" -> POST /api/v2/integration/aws/event_bridge
- "Create a generate_new_external_id?" -> POST /api/v2/integration/aws/generate_new_external_id
- "List all iam_permissions?" -> GET /api/v2/integration/aws/iam_permissions
- "List all resource_collection?" -> GET /api/v2/integration/aws/iam_permissions/resource_collection
- "List all standard?" -> GET /api/v2/integration/aws/iam_permissions/standard
- "List all services?" -> GET /api/v2/integration/aws/logs/services
- "List all accounts?" -> GET /api/v2/integration/gcp/accounts
- "Create a account?" -> POST /api/v2/integration/gcp/accounts
- "Delete a account?" -> DELETE /api/v2/integration/gcp/accounts/{account_id}
- "Partially update a account?" -> PATCH /api/v2/integration/gcp/accounts/{account_id}
- "List all sts_delegate?" -> GET /api/v2/integration/gcp/sts_delegate
- "Create a sts_delegate?" -> POST /api/v2/integration/gcp/sts_delegate
- "Get named-space details?" -> GET /api/v2/integration/google-chat/organizations/app/named-spaces/{domain_name}/{space_display_name}
- "List all organization-handles?" -> GET /api/v2/integration/google-chat/organizations/{organization_binding_id}/organization-handles
- "Create a organization-handle?" -> POST /api/v2/integration/google-chat/organizations/{organization_binding_id}/organization-handles
- "Delete a organization-handle?" -> DELETE /api/v2/integration/google-chat/organizations/{organization_binding_id}/organization-handles/{handle_id}
- "Get organization-handle details?" -> GET /api/v2/integration/google-chat/organizations/{organization_binding_id}/organization-handles/{handle_id}
- "Partially update a organization-handle?" -> PATCH /api/v2/integration/google-chat/organizations/{organization_binding_id}/organization-handles/{handle_id}
- "List all accounts?" -> GET /api/v2/integration/jira/accounts
- "Delete a account?" -> DELETE /api/v2/integration/jira/accounts/{account_id}
- "List all issue-templates?" -> GET /api/v2/integration/jira/issue-templates
- "Create a issue-template?" -> POST /api/v2/integration/jira/issue-templates
- "Delete a issue-template?" -> DELETE /api/v2/integration/jira/issue-templates/{issue_template_id}
- "Get issue-template details?" -> GET /api/v2/integration/jira/issue-templates/{issue_template_id}
- "Partially update a issue-template?" -> PATCH /api/v2/integration/jira/issue-templates/{issue_template_id}
- "Get channel details?" -> GET /api/v2/integration/ms-teams/configuration/channel/{tenant_name}/{team_name}/{channel_name}
- "List all tenant-based-handles?" -> GET /api/v2/integration/ms-teams/configuration/tenant-based-handles
- "Create a tenant-based-handle?" -> POST /api/v2/integration/ms-teams/configuration/tenant-based-handles
- "Delete a tenant-based-handle?" -> DELETE /api/v2/integration/ms-teams/configuration/tenant-based-handles/{handle_id}
- "Get tenant-based-handle details?" -> GET /api/v2/integration/ms-teams/configuration/tenant-based-handles/{handle_id}
- "Partially update a tenant-based-handle?" -> PATCH /api/v2/integration/ms-teams/configuration/tenant-based-handles/{handle_id}
- "List all workflows-webhook-handles?" -> GET /api/v2/integration/ms-teams/configuration/workflows-webhook-handles
- "Create a workflows-webhook-handle?" -> POST /api/v2/integration/ms-teams/configuration/workflows-webhook-handles
- "Delete a workflows-webhook-handle?" -> DELETE /api/v2/integration/ms-teams/configuration/workflows-webhook-handles/{handle_id}
- "Get workflows-webhook-handle details?" -> GET /api/v2/integration/ms-teams/configuration/workflows-webhook-handles/{handle_id}
- "Partially update a workflows-webhook-handle?" -> PATCH /api/v2/integration/ms-teams/configuration/workflows-webhook-handles/{handle_id}
- "List all products?" -> GET /api/v2/integration/oci/products
- "List all tenancies?" -> GET /api/v2/integration/oci/tenancies
- "Create a tenancy?" -> POST /api/v2/integration/oci/tenancies
- "Delete a tenancy?" -> DELETE /api/v2/integration/oci/tenancies/{tenancy_ocid}
- "Get tenancy details?" -> GET /api/v2/integration/oci/tenancies/{tenancy_ocid}
- "Partially update a tenancy?" -> PATCH /api/v2/integration/oci/tenancies/{tenancy_ocid}
- "List all services?" -> GET /api/v2/integration/opsgenie/services
- "Create a service?" -> POST /api/v2/integration/opsgenie/services
- "Delete a service?" -> DELETE /api/v2/integration/opsgenie/services/{integration_service_id}
- "Get service details?" -> GET /api/v2/integration/opsgenie/services/{integration_service_id}
- "Partially update a service?" -> PATCH /api/v2/integration/opsgenie/services/{integration_service_id}
- "Get assignment_group details?" -> GET /api/v2/integration/servicenow/assignment_groups/{instance_id}
- "Get business_service details?" -> GET /api/v2/integration/servicenow/business_services/{instance_id}
- "List all handles?" -> GET /api/v2/integration/servicenow/handles
- "Create a handle?" -> POST /api/v2/integration/servicenow/handles
- "Delete a handle?" -> DELETE /api/v2/integration/servicenow/handles/{template_id}
- "Get handle details?" -> GET /api/v2/integration/servicenow/handles/{template_id}
- "Update a handle?" -> PUT /api/v2/integration/servicenow/handles/{template_id}
- "List all instances?" -> GET /api/v2/integration/servicenow/instances
- "Get user details?" -> GET /api/v2/integration/servicenow/users/{instance_id}
- "List all integrations?" -> GET /api/v2/integrations
- "List all accounts?" -> GET /api/v2/integrations/cloudflare/accounts
- "Create a account?" -> POST /api/v2/integrations/cloudflare/accounts
- "Delete a account?" -> DELETE /api/v2/integrations/cloudflare/accounts/{account_id}
- "Get account details?" -> GET /api/v2/integrations/cloudflare/accounts/{account_id}
- "Partially update a account?" -> PATCH /api/v2/integrations/cloudflare/accounts/{account_id}
- "List all accounts?" -> GET /api/v2/integrations/confluent-cloud/accounts
- "Create a account?" -> POST /api/v2/integrations/confluent-cloud/accounts
- "Delete a account?" -> DELETE /api/v2/integrations/confluent-cloud/accounts/{account_id}
- "Get account details?" -> GET /api/v2/integrations/confluent-cloud/accounts/{account_id}
- "Partially update a account?" -> PATCH /api/v2/integrations/confluent-cloud/accounts/{account_id}
- "List all resources?" -> GET /api/v2/integrations/confluent-cloud/accounts/{account_id}/resources
- "Create a resource?" -> POST /api/v2/integrations/confluent-cloud/accounts/{account_id}/resources
- "Delete a resource?" -> DELETE /api/v2/integrations/confluent-cloud/accounts/{account_id}/resources/{resource_id}
- "Get resource details?" -> GET /api/v2/integrations/confluent-cloud/accounts/{account_id}/resources/{resource_id}
- "Partially update a resource?" -> PATCH /api/v2/integrations/confluent-cloud/accounts/{account_id}/resources/{resource_id}
- "List all accounts?" -> GET /api/v2/integrations/fastly/accounts
- "Create a account?" -> POST /api/v2/integrations/fastly/accounts
- "Delete a account?" -> DELETE /api/v2/integrations/fastly/accounts/{account_id}
- "Get account details?" -> GET /api/v2/integrations/fastly/accounts/{account_id}
- "Partially update a account?" -> PATCH /api/v2/integrations/fastly/accounts/{account_id}
- "List all services?" -> GET /api/v2/integrations/fastly/accounts/{account_id}/services
- "Create a service?" -> POST /api/v2/integrations/fastly/accounts/{account_id}/services
- "Delete a service?" -> DELETE /api/v2/integrations/fastly/accounts/{account_id}/services/{service_id}
- "Get service details?" -> GET /api/v2/integrations/fastly/accounts/{account_id}/services/{service_id}
- "Partially update a service?" -> PATCH /api/v2/integrations/fastly/accounts/{account_id}/services/{service_id}
- "List all accounts?" -> GET /api/v2/integrations/okta/accounts
- "Create a account?" -> POST /api/v2/integrations/okta/accounts
- "Delete a account?" -> DELETE /api/v2/integrations/okta/accounts/{account_id}
- "Get account details?" -> GET /api/v2/integrations/okta/accounts/{account_id}
- "Partially update a account?" -> PATCH /api/v2/integrations/okta/accounts/{account_id}
- "List all ip_allowlist?" -> GET /api/v2/ip_allowlist
- "List all experiments?" -> GET /api/v2/llm-obs/v1/experiments
- "Create a experiment?" -> POST /api/v2/llm-obs/v1/experiments
- "Create a delete?" -> POST /api/v2/llm-obs/v1/experiments/delete
- "Partially update a experiment?" -> PATCH /api/v2/llm-obs/v1/experiments/{experiment_id}
- "Create a event?" -> POST /api/v2/llm-obs/v1/experiments/{experiment_id}/events
- "List all projects?" -> GET /api/v2/llm-obs/v1/projects
- "Create a project?" -> POST /api/v2/llm-obs/v1/projects
- "Create a delete?" -> POST /api/v2/llm-obs/v1/projects/delete
- "Partially update a project?" -> PATCH /api/v2/llm-obs/v1/projects/{project_id}
- "List all datasets?" -> GET /api/v2/llm-obs/v1/{project_id}/datasets
- "Create a dataset?" -> POST /api/v2/llm-obs/v1/{project_id}/datasets
- "Create a delete?" -> POST /api/v2/llm-obs/v1/{project_id}/datasets/delete
- "Partially update a dataset?" -> PATCH /api/v2/llm-obs/v1/{project_id}/datasets/{dataset_id}
- "List all records?" -> GET /api/v2/llm-obs/v1/{project_id}/datasets/{dataset_id}/records
- "Create a record?" -> POST /api/v2/llm-obs/v1/{project_id}/datasets/{dataset_id}/records
- "Create a delete?" -> POST /api/v2/llm-obs/v1/{project_id}/datasets/{dataset_id}/records/delete
- "Create a log?" -> POST /api/v2/logs
- "Create a aggregate?" -> POST /api/v2/logs/analytics/aggregate
- "List all archive-order?" -> GET /api/v2/logs/config/archive-order
- "List all archives?" -> GET /api/v2/logs/config/archives
- "Create a archive?" -> POST /api/v2/logs/config/archives
- "Delete a archive?" -> DELETE /api/v2/logs/config/archives/{archive_id}
- "Get archive details?" -> GET /api/v2/logs/config/archives/{archive_id}
- "Update a archive?" -> PUT /api/v2/logs/config/archives/{archive_id}
- "List all readers?" -> GET /api/v2/logs/config/archives/{archive_id}/readers
- "Create a reader?" -> POST /api/v2/logs/config/archives/{archive_id}/readers
- "List all custom-destinations?" -> GET /api/v2/logs/config/custom-destinations
- "Create a custom-destination?" -> POST /api/v2/logs/config/custom-destinations
- "Delete a custom-destination?" -> DELETE /api/v2/logs/config/custom-destinations/{custom_destination_id}
- "Get custom-destination details?" -> GET /api/v2/logs/config/custom-destinations/{custom_destination_id}
- "Partially update a custom-destination?" -> PATCH /api/v2/logs/config/custom-destinations/{custom_destination_id}
- "List all metrics?" -> GET /api/v2/logs/config/metrics
- "Create a metric?" -> POST /api/v2/logs/config/metrics
- "Delete a metric?" -> DELETE /api/v2/logs/config/metrics/{metric_id}
- "Get metric details?" -> GET /api/v2/logs/config/metrics/{metric_id}
- "Partially update a metric?" -> PATCH /api/v2/logs/config/metrics/{metric_id}
- "List all restriction_queries?" -> GET /api/v2/logs/config/restriction_queries
- "Create a restriction_query?" -> POST /api/v2/logs/config/restriction_queries
- "Get role details?" -> GET /api/v2/logs/config/restriction_queries/role/{role_id}
- "Get user details?" -> GET /api/v2/logs/config/restriction_queries/user/{user_id}
- "Delete a restriction_query?" -> DELETE /api/v2/logs/config/restriction_queries/{restriction_query_id}
- "Get restriction_query details?" -> GET /api/v2/logs/config/restriction_queries/{restriction_query_id}
- "Partially update a restriction_query?" -> PATCH /api/v2/logs/config/restriction_queries/{restriction_query_id}
- "Update a restriction_query?" -> PUT /api/v2/logs/config/restriction_queries/{restriction_query_id}
- "List all roles?" -> GET /api/v2/logs/config/restriction_queries/{restriction_query_id}/roles
- "Create a role?" -> POST /api/v2/logs/config/restriction_queries/{restriction_query_id}/roles
- "List all events?" -> GET /api/v2/logs/events
- "Create a search?" -> POST /api/v2/logs/events/search
- "List all metrics?" -> GET /api/v2/metrics
- "Create a bulk-tag?" -> POST /api/v2/metrics/config/bulk-tags
- "List all active-configurations?" -> GET /api/v2/metrics/{metric_name}/active-configurations
- "List all all-tags?" -> GET /api/v2/metrics/{metric_name}/all-tags
- "List all assets?" -> GET /api/v2/metrics/{metric_name}/assets
- "List all estimate?" -> GET /api/v2/metrics/{metric_name}/estimate
- "List all tag-cardinalities?" -> GET /api/v2/metrics/{metric_name}/tag-cardinalities
- "List all tags?" -> GET /api/v2/metrics/{metric_name}/tags
- "Create a tag?" -> POST /api/v2/metrics/{metric_name}/tags
- "List all volumes?" -> GET /api/v2/metrics/{metric_name}/volumes
- "List all notification_rule?" -> GET /api/v2/monitor/notification_rule
- "Create a notification_rule?" -> POST /api/v2/monitor/notification_rule
- "Delete a notification_rule?" -> DELETE /api/v2/monitor/notification_rule/{rule_id}
- "Get notification_rule details?" -> GET /api/v2/monitor/notification_rule/{rule_id}
- "Partially update a notification_rule?" -> PATCH /api/v2/monitor/notification_rule/{rule_id}
- "List all policy?" -> GET /api/v2/monitor/policy
- "Create a policy?" -> POST /api/v2/monitor/policy
- "Delete a policy?" -> DELETE /api/v2/monitor/policy/{policy_id}
- "Get policy details?" -> GET /api/v2/monitor/policy/{policy_id}
- "Partially update a policy?" -> PATCH /api/v2/monitor/policy/{policy_id}
- "List all template?" -> GET /api/v2/monitor/template
- "Create a template?" -> POST /api/v2/monitor/template
- "Create a validate?" -> POST /api/v2/monitor/template/validate
- "Delete a template?" -> DELETE /api/v2/monitor/template/{template_id}
- "Get template details?" -> GET /api/v2/monitor/template/{template_id}
- "Update a template?" -> PUT /api/v2/monitor/template/{template_id}
- "Create a validate?" -> POST /api/v2/monitor/template/{template_id}/validate
- "List all downtime_matches?" -> GET /api/v2/monitor/{monitor_id}/downtime_matches
- "List all devices?" -> GET /api/v2/ndm/devices
- "Get device details?" -> GET /api/v2/ndm/devices/{device_id}
- "List all interfaces?" -> GET /api/v2/ndm/interfaces
- "Get device details?" -> GET /api/v2/ndm/tags/devices/{device_id}
- "Partially update a device?" -> PATCH /api/v2/ndm/tags/devices/{device_id}
- "Get interface details?" -> GET /api/v2/ndm/tags/interfaces/{interface_id}
- "Partially update a interface?" -> PATCH /api/v2/ndm/tags/interfaces/{interface_id}
- "List all aggregate?" -> GET /api/v2/network/connections/aggregate
- "List all aggregate?" -> GET /api/v2/network/dns/aggregate
- "List all pipelines?" -> GET /api/v2/obs-pipelines/pipelines
- "Create a pipeline?" -> POST /api/v2/obs-pipelines/pipelines
- "Create a validate?" -> POST /api/v2/obs-pipelines/pipelines/validate
- "Delete a pipeline?" -> DELETE /api/v2/obs-pipelines/pipelines/{pipeline_id}
- "Get pipeline details?" -> GET /api/v2/obs-pipelines/pipelines/{pipeline_id}
- "Update a pipeline?" -> PUT /api/v2/obs-pipelines/pipelines/{pipeline_id}
- "Create a escalation-policy?" -> POST /api/v2/on-call/escalation-policies
- "Delete a escalation-policy?" -> DELETE /api/v2/on-call/escalation-policies/{policy_id}
- "Get escalation-policy details?" -> GET /api/v2/on-call/escalation-policies/{policy_id}
- "Update a escalation-policy?" -> PUT /api/v2/on-call/escalation-policies/{policy_id}
- "Create a page?" -> POST /api/v2/on-call/pages
- "Create a acknowledge?" -> POST /api/v2/on-call/pages/{page_id}/acknowledge
- "Create a escalate?" -> POST /api/v2/on-call/pages/{page_id}/escalate
- "Create a resolve?" -> POST /api/v2/on-call/pages/{page_id}/resolve
- "Create a schedule?" -> POST /api/v2/on-call/schedules
- "Delete a schedule?" -> DELETE /api/v2/on-call/schedules/{schedule_id}
- "Get schedule details?" -> GET /api/v2/on-call/schedules/{schedule_id}
- "Update a schedule?" -> PUT /api/v2/on-call/schedules/{schedule_id}
- "List all on-call?" -> GET /api/v2/on-call/schedules/{schedule_id}/on-call
- "List all on-call?" -> GET /api/v2/on-call/teams/{team_id}/on-call
- "List all routing-rules?" -> GET /api/v2/on-call/teams/{team_id}/routing-rules
- "List all notification-channels?" -> GET /api/v2/on-call/users/{user_id}/notification-channels
- "Create a notification-channel?" -> POST /api/v2/on-call/users/{user_id}/notification-channels
- "Delete a notification-channel?" -> DELETE /api/v2/on-call/users/{user_id}/notification-channels/{channel_id}
- "Get notification-channel details?" -> GET /api/v2/on-call/users/{user_id}/notification-channels/{channel_id}
- "List all notification-rules?" -> GET /api/v2/on-call/users/{user_id}/notification-rules
- "Create a notification-rule?" -> POST /api/v2/on-call/users/{user_id}/notification-rules
- "Delete a notification-rule?" -> DELETE /api/v2/on-call/users/{user_id}/notification-rules/{rule_id}
- "Get notification-rule details?" -> GET /api/v2/on-call/users/{user_id}/notification-rules/{rule_id}
- "Update a notification-rule?" -> PUT /api/v2/on-call/users/{user_id}/notification-rules/{rule_id}
- "List all org_configs?" -> GET /api/v2/org_configs
- "Get org_config details?" -> GET /api/v2/org_configs/{org_config_name}
- "Partially update a org_config?" -> PATCH /api/v2/org_configs/{org_config_name}
- "List all org_connections?" -> GET /api/v2/org_connections
- "Create a org_connection?" -> POST /api/v2/org_connections
- "Delete a org_connection?" -> DELETE /api/v2/org_connections/{connection_id}
- "Partially update a org_connection?" -> PATCH /api/v2/org_connections/{connection_id}
- "List all permissions?" -> GET /api/v2/permissions
- "List all findings?" -> GET /api/v2/posture_management/findings
- "Get finding details?" -> GET /api/v2/posture_management/findings/{finding_id}
- "List all powerpacks?" -> GET /api/v2/powerpacks
- "Create a powerpack?" -> POST /api/v2/powerpacks
- "Delete a powerpack?" -> DELETE /api/v2/powerpacks/{powerpack_id}
- "Get powerpack details?" -> GET /api/v2/powerpacks/{powerpack_id}
- "Partially update a powerpack?" -> PATCH /api/v2/powerpacks/{powerpack_id}
- "Search processes?" -> GET /api/v2/processes
- "Create a prodlytic?" -> POST /api/v2/prodlytics
- "Create a facet_info?" -> POST /api/v2/product-analytics/accounts/facet_info
- "Create a query?" -> POST /api/v2/product-analytics/accounts/query
- "Create a scalar?" -> POST /api/v2/product-analytics/analytics/scalar
- "Create a timesery?" -> POST /api/v2/product-analytics/analytics/timeseries
- "Create a event_filtered_query?" -> POST /api/v2/product-analytics/users/event_filtered_query
- "Create a facet_info?" -> POST /api/v2/product-analytics/users/facet_info
- "Create a query?" -> POST /api/v2/product-analytics/users/query
- "List all mapping?" -> GET /api/v2/product-analytics/{entity}/mapping
- "Create a connection?" -> POST /api/v2/product-analytics/{entity}/mapping/connection
- "Delete a connection?" -> DELETE /api/v2/product-analytics/{entity}/mapping/connection/{id}
- "List all connections?" -> GET /api/v2/product-analytics/{entity}/mapping/connections
- "Create a scalar?" -> POST /api/v2/query/scalar
- "Create a timesery?" -> POST /api/v2/query/timeseries
- "List all tables?" -> GET /api/v2/reference-tables/tables
- "Create a table?" -> POST /api/v2/reference-tables/tables
- "Delete a table?" -> DELETE /api/v2/reference-tables/tables/{id}
- "Get table details?" -> GET /api/v2/reference-tables/tables/{id}
- "Partially update a table?" -> PATCH /api/v2/reference-tables/tables/{id}
- "List all rows?" -> GET /api/v2/reference-tables/tables/{id}/rows
- "Create a row?" -> POST /api/v2/reference-tables/tables/{id}/rows
- "Create a upload?" -> POST /api/v2/reference-tables/uploads
- "List all custom_rules?" -> GET /api/v2/remote_config/products/asm/waf/custom_rules
- "Create a custom_rule?" -> POST /api/v2/remote_config/products/asm/waf/custom_rules
- "Delete a custom_rule?" -> DELETE /api/v2/remote_config/products/asm/waf/custom_rules/{custom_rule_id}
- "Get custom_rule details?" -> GET /api/v2/remote_config/products/asm/waf/custom_rules/{custom_rule_id}
- "Update a custom_rule?" -> PUT /api/v2/remote_config/products/asm/waf/custom_rules/{custom_rule_id}
- "List all exclusion_filters?" -> GET /api/v2/remote_config/products/asm/waf/exclusion_filters
- "Create a exclusion_filter?" -> POST /api/v2/remote_config/products/asm/waf/exclusion_filters
- "Delete a exclusion_filter?" -> DELETE /api/v2/remote_config/products/asm/waf/exclusion_filters/{exclusion_filter_id}
- "Get exclusion_filter details?" -> GET /api/v2/remote_config/products/asm/waf/exclusion_filters/{exclusion_filter_id}
- "Update a exclusion_filter?" -> PUT /api/v2/remote_config/products/asm/waf/exclusion_filters/{exclusion_filter_id}
- "List all agent_rules?" -> GET /api/v2/remote_config/products/cws/agent_rules
- "Create a agent_rule?" -> POST /api/v2/remote_config/products/cws/agent_rules
- "Delete a agent_rule?" -> DELETE /api/v2/remote_config/products/cws/agent_rules/{agent_rule_id}
- "Get agent_rule details?" -> GET /api/v2/remote_config/products/cws/agent_rules/{agent_rule_id}
- "Partially update a agent_rule?" -> PATCH /api/v2/remote_config/products/cws/agent_rules/{agent_rule_id}
- "List all policy?" -> GET /api/v2/remote_config/products/cws/policy
- "Create a policy?" -> POST /api/v2/remote_config/products/cws/policy
- "List all download?" -> GET /api/v2/remote_config/products/cws/policy/download
- "Delete a policy?" -> DELETE /api/v2/remote_config/products/cws/policy/{policy_id}
- "Get policy details?" -> GET /api/v2/remote_config/products/cws/policy/{policy_id}
- "Partially update a policy?" -> PATCH /api/v2/remote_config/products/cws/policy/{policy_id}
- "List all snapshots?" -> GET /api/v2/replay/heatmap/snapshots
- "Create a snapshot?" -> POST /api/v2/replay/heatmap/snapshots
- "Delete a snapshot?" -> DELETE /api/v2/replay/heatmap/snapshots/{snapshot_id}
- "Partially update a snapshot?" -> PATCH /api/v2/replay/heatmap/snapshots/{snapshot_id}
- "Delete a restriction_policy?" -> DELETE /api/v2/restriction_policy/{resource_id}
- "Get restriction_policy details?" -> GET /api/v2/restriction_policy/{resource_id}
- "List all roles?" -> GET /api/v2/roles
- "Create a role?" -> POST /api/v2/roles
- "List all templates?" -> GET /api/v2/roles/templates
- "Delete a role?" -> DELETE /api/v2/roles/{role_id}
- "Get role details?" -> GET /api/v2/roles/{role_id}
- "Partially update a role?" -> PATCH /api/v2/roles/{role_id}
- "Create a clone?" -> POST /api/v2/roles/{role_id}/clone
- "List all permissions?" -> GET /api/v2/roles/{role_id}/permissions
- "Create a permission?" -> POST /api/v2/roles/{role_id}/permissions
- "List all users?" -> GET /api/v2/roles/{role_id}/users
- "Create a user?" -> POST /api/v2/roles/{role_id}/users
- "Create a aggregate?" -> POST /api/v2/rum/analytics/aggregate
- "List all applications?" -> GET /api/v2/rum/applications
- "Create a application?" -> POST /api/v2/rum/applications
- "List all retention_filters?" -> GET /api/v2/rum/applications/{app_id}/retention_filters
- "Create a retention_filter?" -> POST /api/v2/rum/applications/{app_id}/retention_filters
- "Delete a retention_filter?" -> DELETE /api/v2/rum/applications/{app_id}/retention_filters/{rf_id}
- "Get retention_filter details?" -> GET /api/v2/rum/applications/{app_id}/retention_filters/{rf_id}
- "Partially update a retention_filter?" -> PATCH /api/v2/rum/applications/{app_id}/retention_filters/{rf_id}
- "Delete a application?" -> DELETE /api/v2/rum/applications/{id}
- "Get application details?" -> GET /api/v2/rum/applications/{id}
- "Partially update a application?" -> PATCH /api/v2/rum/applications/{id}
- "List all metrics?" -> GET /api/v2/rum/config/metrics
- "Create a metric?" -> POST /api/v2/rum/config/metrics
- "Delete a metric?" -> DELETE /api/v2/rum/config/metrics/{metric_id}
- "Get metric details?" -> GET /api/v2/rum/config/metrics/{metric_id}
- "Partially update a metric?" -> PATCH /api/v2/rum/config/metrics/{metric_id}
- "List all events?" -> GET /api/v2/rum/events
- "Create a search?" -> POST /api/v2/rum/events/search
- "List all playlists?" -> GET /api/v2/rum/replay/playlists
- "Create a playlist?" -> POST /api/v2/rum/replay/playlists
- "Delete a playlist?" -> DELETE /api/v2/rum/replay/playlists/{playlist_id}
- "Get playlist details?" -> GET /api/v2/rum/replay/playlists/{playlist_id}
- "Update a playlist?" -> PUT /api/v2/rum/replay/playlists/{playlist_id}
- "List all sessions?" -> GET /api/v2/rum/replay/playlists/{playlist_id}/sessions
- "Delete a session?" -> DELETE /api/v2/rum/replay/playlists/{playlist_id}/sessions/{session_id}
- "Update a session?" -> PUT /api/v2/rum/replay/playlists/{playlist_id}/sessions/{session_id}
- "List all segments?" -> GET /api/v2/rum/replay/sessions/{session_id}/views/{view_id}/segments
- "List all watchers?" -> GET /api/v2/rum/replay/sessions/{session_id}/watchers
- "Create a watche?" -> POST /api/v2/rum/replay/sessions/{session_id}/watches
- "List all sessions?" -> GET /api/v2/rum/replay/viewership-history/sessions
- "Create a idp_metadata?" -> POST /api/v2/saml_configurations/idp_metadata
- "List all outcomes?" -> GET /api/v2/scorecard/outcomes
- "Create a outcome?" -> POST /api/v2/scorecard/outcomes
- "Create a batch?" -> POST /api/v2/scorecard/outcomes/batch
- "List all rules?" -> GET /api/v2/scorecard/rules
- "Create a rule?" -> POST /api/v2/scorecard/rules
- "Delete a rule?" -> DELETE /api/v2/scorecard/rules/{rule_id}
- "Update a rule?" -> PUT /api/v2/scorecard/rules/{rule_id}
- "List all users?" -> GET /api/v2/seats/users
- "Create a user?" -> POST /api/v2/seats/users
- "List all risk-scores?" -> GET /api/v2/security-entities/risk-scores
- "List all download?" -> GET /api/v2/security/cloud_workload/policy/download
- "List all findings?" -> GET /api/v2/security/findings
- "Create a case?" -> POST /api/v2/security/findings/cases
- "Partially update a case?" -> PATCH /api/v2/security/findings/cases/{case_id}
- "Create a jira_issue?" -> POST /api/v2/security/findings/jira_issues
- "Create a search?" -> POST /api/v2/security/findings/search
- "List all sboms?" -> GET /api/v2/security/sboms
- "Get sbom details?" -> GET /api/v2/security/sboms/{asset_type}
- "List all scanned-assets-metadata?" -> GET /api/v2/security/scanned-assets-metadata
- "List all notification_rules?" -> GET /api/v2/security/signals/notification_rules
- "Create a notification_rule?" -> POST /api/v2/security/signals/notification_rules
- "Delete a notification_rule?" -> DELETE /api/v2/security/signals/notification_rules/{id}
- "Get notification_rule details?" -> GET /api/v2/security/signals/notification_rules/{id}
- "Partially update a notification_rule?" -> PATCH /api/v2/security/signals/notification_rules/{id}
- "List all vulnerabilities?" -> GET /api/v2/security/vulnerabilities
- "List all notification_rules?" -> GET /api/v2/security/vulnerabilities/notification_rules
- "Create a notification_rule?" -> POST /api/v2/security/vulnerabilities/notification_rules
- "Delete a notification_rule?" -> DELETE /api/v2/security/vulnerabilities/notification_rules/{id}
- "Get notification_rule details?" -> GET /api/v2/security/vulnerabilities/notification_rules/{id}
- "Partially update a notification_rule?" -> PATCH /api/v2/security/vulnerabilities/notification_rules/{id}
- "List all vulnerable-assets?" -> GET /api/v2/security/vulnerable-assets
- "List all agent_rules?" -> GET /api/v2/security_monitoring/cloud_workload_security/agent_rules
- "Create a agent_rule?" -> POST /api/v2/security_monitoring/cloud_workload_security/agent_rules
- "Delete a agent_rule?" -> DELETE /api/v2/security_monitoring/cloud_workload_security/agent_rules/{agent_rule_id}
- "Get agent_rule details?" -> GET /api/v2/security_monitoring/cloud_workload_security/agent_rules/{agent_rule_id}
- "Partially update a agent_rule?" -> PATCH /api/v2/security_monitoring/cloud_workload_security/agent_rules/{agent_rule_id}
- "Search critical_assets?" -> GET /api/v2/security_monitoring/configuration/critical_assets
- "Create a critical_asset?" -> POST /api/v2/security_monitoring/configuration/critical_assets
- "Get rule details?" -> GET /api/v2/security_monitoring/configuration/critical_assets/rules/{rule_id}
- "Delete a critical_asset?" -> DELETE /api/v2/security_monitoring/configuration/critical_assets/{critical_asset_id}
- "Get critical_asset details?" -> GET /api/v2/security_monitoring/configuration/critical_assets/{critical_asset_id}
- "Partially update a critical_asset?" -> PATCH /api/v2/security_monitoring/configuration/critical_assets/{critical_asset_id}
- "List all security_filters?" -> GET /api/v2/security_monitoring/configuration/security_filters
- "Create a security_filter?" -> POST /api/v2/security_monitoring/configuration/security_filters
- "Delete a security_filter?" -> DELETE /api/v2/security_monitoring/configuration/security_filters/{security_filter_id}
- "Get security_filter details?" -> GET /api/v2/security_monitoring/configuration/security_filters/{security_filter_id}
- "Partially update a security_filter?" -> PATCH /api/v2/security_monitoring/configuration/security_filters/{security_filter_id}
- "Search suppressions?" -> GET /api/v2/security_monitoring/configuration/suppressions
- "Create a suppression?" -> POST /api/v2/security_monitoring/configuration/suppressions
- "Create a rule?" -> POST /api/v2/security_monitoring/configuration/suppressions/rules
- "Get rule details?" -> GET /api/v2/security_monitoring/configuration/suppressions/rules/{rule_id}
- "Create a validation?" -> POST /api/v2/security_monitoring/configuration/suppressions/validation
- "Delete a suppression?" -> DELETE /api/v2/security_monitoring/configuration/suppressions/{suppression_id}
- "Get suppression details?" -> GET /api/v2/security_monitoring/configuration/suppressions/{suppression_id}
- "Partially update a suppression?" -> PATCH /api/v2/security_monitoring/configuration/suppressions/{suppression_id}
- "List all version_history?" -> GET /api/v2/security_monitoring/configuration/suppressions/{suppression_id}/version_history
- "List all states?" -> GET /api/v2/security_monitoring/content_packs/states
- "Search rules?" -> GET /api/v2/security_monitoring/rules
- "Create a rule?" -> POST /api/v2/security_monitoring/rules
- "Create a bulk_export?" -> POST /api/v2/security_monitoring/rules/bulk_export
- "Create a convert?" -> POST /api/v2/security_monitoring/rules/convert
- "Create a test?" -> POST /api/v2/security_monitoring/rules/test
- "Create a validation?" -> POST /api/v2/security_monitoring/rules/validation
- "Delete a rule?" -> DELETE /api/v2/security_monitoring/rules/{rule_id}
- "Get rule details?" -> GET /api/v2/security_monitoring/rules/{rule_id}
- "Update a rule?" -> PUT /api/v2/security_monitoring/rules/{rule_id}
- "List all convert?" -> GET /api/v2/security_monitoring/rules/{rule_id}/convert
- "Create a test?" -> POST /api/v2/security_monitoring/rules/{rule_id}/test
- "List all version_history?" -> GET /api/v2/security_monitoring/rules/{rule_id}/version_history
- "List all signals?" -> GET /api/v2/security_monitoring/signals
- "Create a search?" -> POST /api/v2/security_monitoring/signals/search
- "Get signal details?" -> GET /api/v2/security_monitoring/signals/{signal_id}
- "List all config?" -> GET /api/v2/sensitive-data-scanner/config
- "Create a group?" -> POST /api/v2/sensitive-data-scanner/config/groups
- "Delete a group?" -> DELETE /api/v2/sensitive-data-scanner/config/groups/{group_id}
- "Partially update a group?" -> PATCH /api/v2/sensitive-data-scanner/config/groups/{group_id}
- "Create a rule?" -> POST /api/v2/sensitive-data-scanner/config/rules
- "Delete a rule?" -> DELETE /api/v2/sensitive-data-scanner/config/rules/{rule_id}
- "Partially update a rule?" -> PATCH /api/v2/sensitive-data-scanner/config/rules/{rule_id}
- "List all standard-patterns?" -> GET /api/v2/sensitive-data-scanner/config/standard-patterns
- "Create a sery?" -> POST /api/v2/series
- "Create a service_account?" -> POST /api/v2/service_accounts
- "List all application_keys?" -> GET /api/v2/service_accounts/{service_account_id}/application_keys
- "Create a application_key?" -> POST /api/v2/service_accounts/{service_account_id}/application_keys
- "Delete a application_key?" -> DELETE /api/v2/service_accounts/{service_account_id}/application_keys/{app_key_id}
- "Get application_key details?" -> GET /api/v2/service_accounts/{service_account_id}/application_keys/{app_key_id}
- "Partially update a application_key?" -> PATCH /api/v2/service_accounts/{service_account_id}/application_keys/{app_key_id}
- "List all services?" -> GET /api/v2/services
- "Create a service?" -> POST /api/v2/services
- "List all definitions?" -> GET /api/v2/services/definitions
- "Create a definition?" -> POST /api/v2/services/definitions
- "Delete a definition?" -> DELETE /api/v2/services/definitions/{service_name}
- "Get definition details?" -> GET /api/v2/services/definitions/{service_name}
- "Delete a service?" -> DELETE /api/v2/services/{service_id}
- "Get service details?" -> GET /api/v2/services/{service_id}
- "Partially update a service?" -> PATCH /api/v2/services/{service_id}
- "List all histsignals?" -> GET /api/v2/siem-threat-hunting/histsignals
- "List all search?" -> GET /api/v2/siem-threat-hunting/histsignals/search
- "Get histsignal details?" -> GET /api/v2/siem-threat-hunting/histsignals/{histsignal_id}
- "List all jobs?" -> GET /api/v2/siem-threat-hunting/jobs
- "Create a job?" -> POST /api/v2/siem-threat-hunting/jobs
- "Create a signal_convert?" -> POST /api/v2/siem-threat-hunting/jobs/signal_convert
- "Delete a job?" -> DELETE /api/v2/siem-threat-hunting/jobs/{job_id}
- "Get job details?" -> GET /api/v2/siem-threat-hunting/jobs/{job_id}
- "List all histsignals?" -> GET /api/v2/siem-threat-hunting/jobs/{job_id}/histsignals
- "Create a report?" -> POST /api/v2/slo/report
- "List all download?" -> GET /api/v2/slo/report/{report_id}/download
- "List all status?" -> GET /api/v2/slo/report/{report_id}/status
- "List all status?" -> GET /api/v2/slo/{slo_id}/status
- "Get recommendation details?" -> GET /api/v2/spa/recommendations/{service}
- "Get recommendation details?" -> GET /api/v2/spa/recommendations/{service}/{shard}
- "Create a aggregate?" -> POST /api/v2/spans/analytics/aggregate
- "List all events?" -> GET /api/v2/spans/events
- "Create a search?" -> POST /api/v2/spans/events/search
- "Create a dependency?" -> POST /api/v2/static-analysis-sca/dependencies
- "Create a resolve-vulnerable-symbol?" -> POST /api/v2/static-analysis-sca/vulnerabilities/resolve-vulnerable-symbols
- "Delete a ruleset?" -> DELETE /api/v2/static-analysis/custom/rulesets/{ruleset_name}
- "Get ruleset details?" -> GET /api/v2/static-analysis/custom/rulesets/{ruleset_name}
- "Partially update a ruleset?" -> PATCH /api/v2/static-analysis/custom/rulesets/{ruleset_name}
- "Delete a rule?" -> DELETE /api/v2/static-analysis/custom/rulesets/{ruleset_name}/rules/{rule_name}
- "Get rule details?" -> GET /api/v2/static-analysis/custom/rulesets/{ruleset_name}/rules/{rule_name}
- "List all revisions?" -> GET /api/v2/static-analysis/custom/rulesets/{ruleset_name}/rules/{rule_name}/revisions
- "Create a revert?" -> POST /api/v2/static-analysis/custom/rulesets/{ruleset_name}/rules/{rule_name}/revisions/revert
- "Get revision details?" -> GET /api/v2/static-analysis/custom/rulesets/{ruleset_name}/rules/{rule_name}/revisions/{id}
- "Create a ruleset?" -> POST /api/v2/static-analysis/rulesets
- "List all rules?" -> GET /api/v2/static-analysis/secrets/rules
- "List all statuspages?" -> GET /api/v2/statuspages
- "Create a statuspage?" -> POST /api/v2/statuspages
- "List all degradations?" -> GET /api/v2/statuspages/degradations
- "List all maintenances?" -> GET /api/v2/statuspages/maintenances
- "Delete a statuspage?" -> DELETE /api/v2/statuspages/{page_id}
- "Get statuspage details?" -> GET /api/v2/statuspages/{page_id}
- "Partially update a statuspage?" -> PATCH /api/v2/statuspages/{page_id}
- "List all components?" -> GET /api/v2/statuspages/{page_id}/components
- "Create a component?" -> POST /api/v2/statuspages/{page_id}/components
- "Delete a component?" -> DELETE /api/v2/statuspages/{page_id}/components/{component_id}
- "Get component details?" -> GET /api/v2/statuspages/{page_id}/components/{component_id}
- "Partially update a component?" -> PATCH /api/v2/statuspages/{page_id}/components/{component_id}
- "Create a degradation?" -> POST /api/v2/statuspages/{page_id}/degradations
- "Delete a degradation?" -> DELETE /api/v2/statuspages/{page_id}/degradations/{degradation_id}
- "Get degradation details?" -> GET /api/v2/statuspages/{page_id}/degradations/{degradation_id}
- "Partially update a degradation?" -> PATCH /api/v2/statuspages/{page_id}/degradations/{degradation_id}
- "Create a maintenance?" -> POST /api/v2/statuspages/{page_id}/maintenances
- "Get maintenance details?" -> GET /api/v2/statuspages/{page_id}/maintenances/{maintenance_id}
- "Partially update a maintenance?" -> PATCH /api/v2/statuspages/{page_id}/maintenances/{maintenance_id}
- "List all on_demand_concurrency_cap?" -> GET /api/v2/synthetics/settings/on_demand_concurrency_cap
- "Create a on_demand_concurrency_cap?" -> POST /api/v2/synthetics/settings/on_demand_concurrency_cap
- "Create a suite?" -> POST /api/v2/synthetics/suites
- "Create a bulk-delete?" -> POST /api/v2/synthetics/suites/bulk-delete
- "Search search?" -> GET /api/v2/synthetics/suites/search
- "Get suite details?" -> GET /api/v2/synthetics/suites/{public_id}
- "Update a suite?" -> PUT /api/v2/synthetics/suites/{public_id}
- "Create a bulk-delete?" -> POST /api/v2/synthetics/tests/bulk-delete
- "Create a network?" -> POST /api/v2/synthetics/tests/network
- "Get network details?" -> GET /api/v2/synthetics/tests/network/{public_id}
- "Update a network?" -> PUT /api/v2/synthetics/tests/network/{public_id}
- "List all enrichment?" -> GET /api/v2/tags/enrichment
- "Create a enrichment?" -> POST /api/v2/tags/enrichment
- "Create a reorder?" -> POST /api/v2/tags/enrichment/reorder
- "Create a validate-query?" -> POST /api/v2/tags/enrichment/validate-query
- "Delete a enrichment?" -> DELETE /api/v2/tags/enrichment/{ruleset_id}
- "Get enrichment details?" -> GET /api/v2/tags/enrichment/{ruleset_id}
- "Partially update a enrichment?" -> PATCH /api/v2/tags/enrichment/{ruleset_id}
- "List all team?" -> GET /api/v2/team
- "Create a team?" -> POST /api/v2/team
- "List all team-hierarchy-links?" -> GET /api/v2/team-hierarchy-links
- "Create a team-hierarchy-link?" -> POST /api/v2/team-hierarchy-links
- "Delete a team-hierarchy-link?" -> DELETE /api/v2/team-hierarchy-links/{link_id}
- "Get team-hierarchy-link details?" -> GET /api/v2/team-hierarchy-links/{link_id}
- "List all connections?" -> GET /api/v2/team/connections
- "Create a connection?" -> POST /api/v2/team/connections
- "List all sync?" -> GET /api/v2/team/sync
- "Create a sync?" -> POST /api/v2/team/sync
- "List all member_teams?" -> GET /api/v2/team/{super_team_id}/member_teams
- "Create a member_team?" -> POST /api/v2/team/{super_team_id}/member_teams
- "Delete a member_team?" -> DELETE /api/v2/team/{super_team_id}/member_teams/{member_team_id}
- "Delete a team?" -> DELETE /api/v2/team/{team_id}
- "Get team details?" -> GET /api/v2/team/{team_id}
- "Partially update a team?" -> PATCH /api/v2/team/{team_id}
- "List all links?" -> GET /api/v2/team/{team_id}/links
- "Create a link?" -> POST /api/v2/team/{team_id}/links
- "Delete a link?" -> DELETE /api/v2/team/{team_id}/links/{link_id}
- "Get link details?" -> GET /api/v2/team/{team_id}/links/{link_id}
- "Partially update a link?" -> PATCH /api/v2/team/{team_id}/links/{link_id}
- "List all memberships?" -> GET /api/v2/team/{team_id}/memberships
- "Create a membership?" -> POST /api/v2/team/{team_id}/memberships
- "Delete a membership?" -> DELETE /api/v2/team/{team_id}/memberships/{user_id}
- "Partially update a membership?" -> PATCH /api/v2/team/{team_id}/memberships/{user_id}
- "List all notification-rules?" -> GET /api/v2/team/{team_id}/notification-rules
- "Create a notification-rule?" -> POST /api/v2/team/{team_id}/notification-rules
- "Delete a notification-rule?" -> DELETE /api/v2/team/{team_id}/notification-rules/{rule_id}
- "Get notification-rule details?" -> GET /api/v2/team/{team_id}/notification-rules/{rule_id}
- "Update a notification-rule?" -> PUT /api/v2/team/{team_id}/notification-rules/{rule_id}
- "List all permission-settings?" -> GET /api/v2/team/{team_id}/permission-settings
- "Update a permission-setting?" -> PUT /api/v2/team/{team_id}/permission-settings/{action}
- "List all teams?" -> GET /api/v2/teams
- "Create a team?" -> POST /api/v2/teams
- "Delete a team?" -> DELETE /api/v2/teams/{team_id}
- "Get team details?" -> GET /api/v2/teams/{team_id}
- "Partially update a team?" -> PATCH /api/v2/teams/{team_id}
- "Create a test?" -> POST /api/v2/test/flaky-test-management/tests
- "List all application_security?" -> GET /api/v2/usage/application_security
- "List all billing_dimension_mapping?" -> GET /api/v2/usage/billing_dimension_mapping
- "List all cost_by_org?" -> GET /api/v2/usage/cost_by_org
- "List all estimated_cost?" -> GET /api/v2/usage/estimated_cost
- "List all historical_cost?" -> GET /api/v2/usage/historical_cost
- "List all hourly_usage?" -> GET /api/v2/usage/hourly_usage
- "List all lambda_traced_invocations?" -> GET /api/v2/usage/lambda_traced_invocations
- "List all observability_pipelines?" -> GET /api/v2/usage/observability_pipelines
- "List all projected_cost?" -> GET /api/v2/usage/projected_cost
- "List all usage-attribution-types?" -> GET /api/v2/usage/usage-attribution-types
- "Create a user_invitation?" -> POST /api/v2/user_invitations
- "Get user_invitation details?" -> GET /api/v2/user_invitations/{user_invitation_uuid}
- "List all users?" -> GET /api/v2/users
- "Create a user?" -> POST /api/v2/users
- "Delete a user?" -> DELETE /api/v2/users/{user_id}
- "Get user details?" -> GET /api/v2/users/{user_id}
- "Partially update a user?" -> PATCH /api/v2/users/{user_id}
- "List all orgs?" -> GET /api/v2/users/{user_id}/orgs
- "List all permissions?" -> GET /api/v2/users/{user_id}/permissions
- "List all memberships?" -> GET /api/v2/users/{user_uuid}/memberships
- "Create a workflow?" -> POST /api/v2/workflows
- "Delete a workflow?" -> DELETE /api/v2/workflows/{workflow_id}
- "Get workflow details?" -> GET /api/v2/workflows/{workflow_id}
- "Partially update a workflow?" -> PATCH /api/v2/workflows/{workflow_id}
- "List all instances?" -> GET /api/v2/workflows/{workflow_id}/instances
- "Create a instance?" -> POST /api/v2/workflows/{workflow_id}/instances
- "Get instance details?" -> GET /api/v2/workflows/{workflow_id}/instances/{instance_id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object
- Error responses use types: Forbidden

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
