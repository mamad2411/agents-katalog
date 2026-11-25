---
name: pagerduty-api
description: "PagerDuty API skill. Use when working with PagerDuty for {entity_type}, abilities, addons. Covers 391 endpoints."
version: 1.0.0
generator: lapsh
---

# PagerDuty API
API version: 2.0.0

## Auth
ApiKey Authorization in header

## Base URL
https://api.pagerduty.com

## Setup
1. Set your API key in the appropriate header
2. GET /abilities -- verify access
3. POST /{entity_type}/{id}/change_tags -- create first change_tags

## Endpoints

391 endpoints across 39 groups. See references/api-spec.lap for full details.

### {entity_type}
| Method | Path | Description |
|--------|------|-------------|
| POST | /{entity_type}/{id}/change_tags | Assign tags |
| GET | /{entity_type}/{id}/tags | Get tags for entities |

### abilities
| Method | Path | Description |
|--------|------|-------------|
| GET | /abilities | List abilities |
| GET | /abilities/{id} | Test an ability |

### addons
| Method | Path | Description |
|--------|------|-------------|
| GET | /addons | List installed Add-ons |
| POST | /addons | Install an Add-on |
| GET | /addons/{id} | Get an Add-on |
| DELETE | /addons/{id} | Delete an Add-on |
| PUT | /addons/{id} | Update an Add-on |

### alert_grouping_settings
| Method | Path | Description |
|--------|------|-------------|
| GET | /alert_grouping_settings | List alert grouping settings |
| POST | /alert_grouping_settings | Create an Alert Grouping Setting |
| GET | /alert_grouping_settings/{id} | Get an Alert Grouping Setting |
| DELETE | /alert_grouping_settings/{id} | Delete an Alert Grouping Setting |
| PUT | /alert_grouping_settings/{id} | Update an Alert Grouping Setting |

### analytics
| Method | Path | Description |
|--------|------|-------------|
| POST | /analytics/metrics/incidents/all | Get aggregated incident data |
| POST | /analytics/metrics/incidents/escalation_policies | Get aggregated escalation policy data |
| POST | /analytics/metrics/incidents/escalation_policies/all | Get aggregated metrics for all escalation policies |
| POST | /analytics/metrics/incidents/services | Get aggregated service data |
| POST | /analytics/metrics/incidents/services/all | Get aggregated metrics for all services |
| POST | /analytics/metrics/incidents/teams | Get aggregated team data |
| POST | /analytics/metrics/incidents/teams/all | Get aggregated metrics for all teams |
| POST | /analytics/metrics/pd_advance_usage/features | Get aggregated PD Advance usage data |
| POST | /analytics/metrics/responders/all | Get aggregated metrics for all responders |
| POST | /analytics/metrics/responders/teams | Get responder data aggregated by team |
| POST | /analytics/metrics/users/all | Get aggregated metrics for all users |
| POST | /analytics/raw/incidents | Get raw data - multiple incidents |
| GET | /analytics/raw/incidents/{id} | Get raw data - single incident |
| GET | /analytics/raw/incidents/{id}/responses | Get raw responses from a single incident |
| POST | /analytics/raw/responders/{responder_id}/incidents | Get raw incidents for a single responder_id |
| POST | /analytics/raw/users | Get raw user analytics data |

### audit
| Method | Path | Description |
|--------|------|-------------|
| GET | /audit/records | List audit records |

### automation_actions
| Method | Path | Description |
|--------|------|-------------|
| POST | /automation_actions/actions | Create an Automation Action |
| GET | /automation_actions/actions | List Automation Actions |
| GET | /automation_actions/actions/{id} | Get an Automation Action |
| DELETE | /automation_actions/actions/{id} | Delete an Automation Action |
| PUT | /automation_actions/actions/{id} | Update an Automation Action |
| POST | /automation_actions/actions/{id}/invocations | Create an Invocation |
| GET | /automation_actions/actions/{id}/services | Get all service references associated with an Automation Action |
| POST | /automation_actions/actions/{id}/services | Associate an Automation Action with a service |
| GET | /automation_actions/actions/{id}/services/{service_id} | Get the details of an Automation Action / service relation |
| DELETE | /automation_actions/actions/{id}/services/{service_id} | Disassociate an Automation Action from a service |
| POST | /automation_actions/actions/{id}/teams | Associate an Automation Action with a team |
| GET | /automation_actions/actions/{id}/teams | Get all team references associated with an Automation Action |
| DELETE | /automation_actions/actions/{id}/teams/{team_id} | Disassociate an Automation Action from a team |
| GET | /automation_actions/actions/{id}/teams/{team_id} | Get the details of an Automation Action / team relation |
| GET | /automation_actions/invocations | List Invocations |
| GET | /automation_actions/invocations/{id} | Get an Invocation |
| POST | /automation_actions/runners | Create an Automation Action runner. |
| GET | /automation_actions/runners | List Automation Action runners |
| GET | /automation_actions/runners/{id} | Get an Automation Action runner |
| PUT | /automation_actions/runners/{id} | Update an Automation Action runner |
| DELETE | /automation_actions/runners/{id} | Delete an Automation Action runner |
| POST | /automation_actions/runners/{id}/teams | Associate a runner with a team |
| GET | /automation_actions/runners/{id}/teams | Get all team references associated with a runner |
| DELETE | /automation_actions/runners/{id}/teams/{team_id} | Disassociate a runner from a team |
| GET | /automation_actions/runners/{id}/teams/{team_id} | Get the details of a runner / team relation |

### business_services
| Method | Path | Description |
|--------|------|-------------|
| GET | /business_services | List Business Services |
| POST | /business_services | Create a Business Service |
| GET | /business_services/{id} | Get a Business Service |
| DELETE | /business_services/{id} | Delete a Business Service |
| PUT | /business_services/{id} | Update a Business Service |
| POST | /business_services/{id}/account_subscription | Create Business Service Account Subscription |
| DELETE | /business_services/{id}/account_subscription | Delete Business Service Account Subscription |
| GET | /business_services/{id}/subscribers | List Business Service Subscribers |
| POST | /business_services/{id}/subscribers | Create Business Service Subscribers |
| GET | /business_services/{id}/supporting_services/impacts | List the supporting Business Services for the given Business Service Id, sorted by impacted status. |
| POST | /business_services/{id}/unsubscribe | Remove Business Service Subscribers |
| GET | /business_services/impactors | List Impactors affecting Business Services |
| GET | /business_services/impacts | List Business Services sorted by impacted status |
| GET | /business_services/priority_thresholds | Get the global priority threshold for a Business Service to be considered impacted by an Incident |
| DELETE | /business_services/priority_thresholds | Deletes the account-level priority threshold for Business Service impact |
| PUT | /business_services/priority_thresholds | Set the Account-level priority threshold for Business Service impact. |

### change_events
| Method | Path | Description |
|--------|------|-------------|
| GET | /change_events | List Change Events |
| POST | /change_events | Create a Change Event |
| GET | /change_events/{id} | Get a Change Event |
| PUT | /change_events/{id} | Update a Change Event |

### escalation_policies
| Method | Path | Description |
|--------|------|-------------|
| GET | /escalation_policies | List escalation policies |
| POST | /escalation_policies | Create an escalation policy |
| GET | /escalation_policies/{id} | Get an escalation policy |
| DELETE | /escalation_policies/{id} | Delete an escalation policy |
| PUT | /escalation_policies/{id} | Update an escalation policy |
| GET | /escalation_policies/{id}/audit/records | List audit records for an escalation policy |

### event_orchestrations
| Method | Path | Description |
|--------|------|-------------|
| GET | /event_orchestrations | List Event Orchestrations |
| POST | /event_orchestrations | Create an Orchestration |
| GET | /event_orchestrations/{id} | Get an Orchestration |
| PUT | /event_orchestrations/{id} | Update an Orchestration |
| DELETE | /event_orchestrations/{id} | Delete an Orchestration |
| GET | /event_orchestrations/{id}/integrations | List Integrations for an Event Orchestration |
| POST | /event_orchestrations/{id}/integrations | Create an Integration for an Event Orchestration |
| GET | /event_orchestrations/{id}/integrations/{integration_id} | Get an Integration for an Event Orchestration |
| PUT | /event_orchestrations/{id}/integrations/{integration_id} | Update an Integration for an Event Orchestration |
| DELETE | /event_orchestrations/{id}/integrations/{integration_id} | Delete an Integration for an Event Orchestration |
| POST | /event_orchestrations/{id}/integrations/migration | Migrate an Integration from one Event Orchestration to another |
| GET | /event_orchestrations/{id}/global | Get the Global Orchestration for an Event Orchestration |
| PUT | /event_orchestrations/{id}/global | Update the Global Orchestration for an Event Orchestration |
| GET | /event_orchestrations/{id}/router | Get the Router for an Event Orchestration |
| PUT | /event_orchestrations/{id}/router | Update the Router for an Event Orchestration |
| GET | /event_orchestrations/{id}/unrouted | Get the Unrouted Orchestration for an Event Orchestration |
| PUT | /event_orchestrations/{id}/unrouted | Update the Unrouted Orchestration for an Event Orchestration |
| GET | /event_orchestrations/services/{service_id} | Get the Service Orchestration for a Service |
| PUT | /event_orchestrations/services/{service_id} | Update the Service Orchestration for a Service |
| GET | /event_orchestrations/services/{service_id}/active | Get the Service Orchestration active status for a Service |
| PUT | /event_orchestrations/services/{service_id}/active | Update the Service Orchestration active status for a Service |
| GET | /event_orchestrations/{id}/cache_variables | List Cache Variables for a Global Event Orchestration |
| POST | /event_orchestrations/{id}/cache_variables | Create a Cache Variable for a Global Event Orchestration |
| GET | /event_orchestrations/{id}/cache_variables/{cache_variable_id} | Get a Cache Variable for a Global Event Orchestration |
| PUT | /event_orchestrations/{id}/cache_variables/{cache_variable_id} | Update a Cache Variable for a Global Event Orchestration |
| DELETE | /event_orchestrations/{id}/cache_variables/{cache_variable_id} | Delete a Cache Variable for a Global Event Orchestration |
| GET | /event_orchestrations/{id}/cache_variables/{cache_variable_id}/data | Get Data for an External Data Cache Variable on a Global Event Orchestration |
| PUT | /event_orchestrations/{id}/cache_variables/{cache_variable_id}/data | Update Data for an External Data Cache Variable on a Global Event Orchestration |
| DELETE | /event_orchestrations/{id}/cache_variables/{cache_variable_id}/data | Delete Data for an External Data Cache Variable on a Global Event Orchestration |
| GET | /event_orchestrations/services/{service_id}/cache_variables | List Cache Variables for a Service Event Orchestration |
| POST | /event_orchestrations/services/{service_id}/cache_variables | Create a Cache Variable for a Service Event Orchestration |
| GET | /event_orchestrations/services/{service_id}/cache_variables/{cache_variable_id} | Get a Cache Variable for a Service Event Orchestration |
| PUT | /event_orchestrations/services/{service_id}/cache_variables/{cache_variable_id} | Update a Cache Variable for a Service Event Orchestration |
| DELETE | /event_orchestrations/services/{service_id}/cache_variables/{cache_variable_id} | Delete a Cache Variable for a Service Event Orchestration |
| GET | /event_orchestrations/services/{service_id}/cache_variables/{cache_variable_id}/data | Get Data for an External Data Cache Variable on a Service Event Orchestration |
| PUT | /event_orchestrations/services/{service_id}/cache_variables/{cache_variable_id}/data | Update Data for an External Data Cache Variable on a Service Event Orchestration |
| DELETE | /event_orchestrations/services/{service_id}/cache_variables/{cache_variable_id}/data | Delete Data for an External Data Cache Variable on a Service Event Orchestration |
| GET | /event_orchestrations/{id}/enablements | List Enablements for an Event Orchestration |
| PUT | /event_orchestrations/{id}/enablements/{feature_name} | Update an Enablement for an Event Orchestration |

### extension_schemas
| Method | Path | Description |
|--------|------|-------------|
| GET | /extension_schemas | List extension schemas |
| GET | /extension_schemas/{id} | Get an extension vendor |

### extensions
| Method | Path | Description |
|--------|------|-------------|
| GET | /extensions | List extensions |
| POST | /extensions | Create an extension |
| GET | /extensions/{id} | Get an extension |
| DELETE | /extensions/{id} | Delete an extension |
| PUT | /extensions/{id} | Update an extension |
| POST | /extensions/{id}/enable | Enable an extension |

### incident_workflows
| Method | Path | Description |
|--------|------|-------------|
| GET | /incident_workflows | List Incident Workflows |
| POST | /incident_workflows | Create an Incident Workflow |
| GET | /incident_workflows/{id} | Get an Incident Workflow |
| DELETE | /incident_workflows/{id} | Delete an Incident Workflow |
| PUT | /incident_workflows/{id} | Update an Incident Workflow |
| POST | /incident_workflows/{id}/instances | Start an Incident Workflow Instance |
| GET | /incident_workflows/actions | List Actions |
| GET | /incident_workflows/actions/{id} | Get an Action |
| GET | /incident_workflows/triggers | List Triggers |
| POST | /incident_workflows/triggers | Create a Trigger |
| GET | /incident_workflows/triggers/{id} | Get a Trigger |
| PUT | /incident_workflows/triggers/{id} | Update a Trigger |
| DELETE | /incident_workflows/triggers/{id} | Delete a Trigger |
| POST | /incident_workflows/triggers/{id}/services | Associate a Trigger and Service |
| DELETE | /incident_workflows/triggers/{trigger_id}/services/{service_id} | Dissociate a Trigger and Service |

### incidents
| Method | Path | Description |
|--------|------|-------------|
| GET | /incidents | List incidents |
| PUT | /incidents | Manage incidents |
| POST | /incidents | Create an Incident |
| GET | /incidents/{id} | Get an incident |
| PUT | /incidents/{id} | Update an incident |
| GET | /incidents/{id}/alerts | List alerts for an incident |
| PUT | /incidents/{id}/alerts | Manage alerts |
| GET | /incidents/{id}/alerts/{alert_id} | Get an alert |
| PUT | /incidents/{id}/alerts/{alert_id} | Update an alert |
| PUT | /incidents/{id}/business_services/{business_service_id}/impacts | Manually change an Incident's Impact on a Business Service. |
| GET | /incidents/{id}/business_services/impacts | List Business Services impacted by the given Incident |
| GET | /incidents/{id}/custom_fields/values | Get Custom Field Values |
| PUT | /incidents/{id}/custom_fields/values | Update Custom Field Values |
| GET | /incidents/{id}/log_entries | List log entries for an incident |
| PUT | /incidents/{id}/merge | Merge incidents |
| GET | /incidents/{id}/notes | List notes for an incident |
| POST | /incidents/{id}/notes | Create a note on an incident |
| PUT | /incidents/{id}/notes/{note_id} | Update a note on an incident |
| DELETE | /incidents/{id}/notes/{note_id} | Delete a note on an incident |
| GET | /incidents/{id}/outlier_incident | Get Outlier Incident |
| GET | /incidents/{id}/past_incidents | Get Past Incidents |
| GET | /incidents/{id}/related_change_events | List related Change Events for an Incident |
| GET | /incidents/{id}/related_incidents | Get Related Incidents |
| POST | /incidents/{id}/responder_requests | Create a responder request for an incident |
| PUT | /incidents/{id}/responder_requests/cancel | Cancel responder requests for an incident |
| POST | /incidents/{id}/snooze | Snooze an incident |
| POST | /incidents/{id}/status_updates | Create a status update on an incident |
| GET | /incidents/{id}/status_updates/subscribers | List Notification Subscribers |
| POST | /incidents/{id}/status_updates/subscribers | Add Notification Subscribers |
| POST | /incidents/{id}/status_updates/unsubscribe | Remove Notification Subscriber |
| GET | /incidents/types | List incident types |
| POST | /incidents/types | Create an Incident Type |
| GET | /incidents/types/{type_id_or_name} | Get an Incident Type |
| PUT | /incidents/types/{type_id_or_name} | Update an Incident Type |
| GET | /incidents/types/{type_id_or_name}/custom_fields | List Incident Type Custom Fields |
| POST | /incidents/types/{type_id_or_name}/custom_fields | Create a Custom Field for an Incident Type |
| GET | /incidents/types/{type_id_or_name}/custom_fields/{field_id} | Get an Incident Type Custom Field |
| PUT | /incidents/types/{type_id_or_name}/custom_fields/{field_id} | Update a Custom Field for an Incident Type |
| DELETE | /incidents/types/{type_id_or_name}/custom_fields/{field_id} | Delete a Custom Field for an Incident Type |
| GET | /incidents/types/{type_id_or_name}/custom_fields/{field_id}/field_options | List Field Options on a Custom Field |
| POST | /incidents/types/{type_id_or_name}/custom_fields/{field_id}/field_options | Create a Field Option for a Custom Field |
| GET | /incidents/types/{type_id_or_name}/custom_fields/{field_id}/field_options/{field_option_id} | Get a Field Option on a Custom Field |
| PUT | /incidents/types/{type_id_or_name}/custom_fields/{field_id}/field_options/{field_option_id} | Update a Field Option for a Custom Field |
| DELETE | /incidents/types/{type_id_or_name}/custom_fields/{field_id}/field_options/{field_option_id} | Delete a Field Option for a Custom Field |
| POST | /incidents/custom_fields | Create a Field |
| GET | /incidents/custom_fields | List Fields |
| GET | /incidents/custom_fields/{field_id} | Get a Field |
| PUT | /incidents/custom_fields/{field_id} | Update a Field |
| DELETE | /incidents/custom_fields/{field_id} | Delete a Field |
| POST | /incidents/custom_fields/{field_id}/field_options | Create a Field Option |
| GET | /incidents/custom_fields/{field_id}/field_options | List Field Options |
| PUT | /incidents/custom_fields/{field_id}/field_options/{field_option_id} | Update a Field Option |
| DELETE | /incidents/custom_fields/{field_id}/field_options/{field_option_id} | Delete a Field Option |

### license_allocations
| Method | Path | Description |
|--------|------|-------------|
| GET | /license_allocations | List License Allocations |

### licenses
| Method | Path | Description |
|--------|------|-------------|
| GET | /licenses | List Licenses |

### log_entries
| Method | Path | Description |
|--------|------|-------------|
| GET | /log_entries | List log entries |
| GET | /log_entries/{id} | Get a log entry |
| PUT | /log_entries/{id}/channel | Update log entry channel information. |

### maintenance_windows
| Method | Path | Description |
|--------|------|-------------|
| GET | /maintenance_windows | List maintenance windows |
| POST | /maintenance_windows | Create a maintenance window |
| GET | /maintenance_windows/{id} | Get a maintenance window |
| DELETE | /maintenance_windows/{id} | Delete or end a maintenance window |
| PUT | /maintenance_windows/{id} | Update a maintenance window |

### notifications
| Method | Path | Description |
|--------|------|-------------|
| GET | /notifications | List notifications |

### oauth_delegations
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /oauth_delegations | Delete all OAuth delegations |
| GET | /oauth_delegations/revocation_requests/status | Get OAuth delegations revocation requests status |

### oncalls
| Method | Path | Description |
|--------|------|-------------|
| GET | /oncalls | List all of the on-calls |

### paused_incident_reports
| Method | Path | Description |
|--------|------|-------------|
| GET | /paused_incident_reports/alerts | Get Paused Incident Reporting on Alerts |
| GET | /paused_incident_reports/counts | Get Paused Incident Reporting counts |

### priorities
| Method | Path | Description |
|--------|------|-------------|
| GET | /priorities | List priorities |

### rulesets
| Method | Path | Description |
|--------|------|-------------|
| GET | /rulesets | List Rulesets |
| POST | /rulesets | Create a Ruleset |
| GET | /rulesets/{id} | Get a Ruleset |
| PUT | /rulesets/{id} | Update a Ruleset |
| DELETE | /rulesets/{id} | Delete a Ruleset |
| GET | /rulesets/{id}/rules | List Event Rules |
| POST | /rulesets/{id}/rules | Create an Event Rule |
| GET | /rulesets/{id}/rules/{rule_id} | Get an Event Rule |
| PUT | /rulesets/{id}/rules/{rule_id} | Update an Event Rule |
| DELETE | /rulesets/{id}/rules/{rule_id} | Delete an Event Rule |

### schedules
| Method | Path | Description |
|--------|------|-------------|
| GET | /schedules | List schedules |
| POST | /schedules | Create a schedule |
| GET | /schedules/{id} | Get a schedule |
| DELETE | /schedules/{id} | Delete a schedule |
| PUT | /schedules/{id} | Update a schedule |
| GET | /schedules/{id}/audit/records | List audit records for a schedule |
| GET | /schedules/{id}/overrides | List overrides |
| POST | /schedules/{id}/overrides | Create one or more overrides |
| DELETE | /schedules/{id}/overrides/{override_id} | Delete an override |
| GET | /schedules/{id}/users | List users on call. |
| POST | /schedules/preview | Preview a schedule |

### service_dependencies
| Method | Path | Description |
|--------|------|-------------|
| POST | /service_dependencies/associate | Associate service dependencies |
| GET | /service_dependencies/business_services/{id} | Get Business Service dependencies |
| POST | /service_dependencies/disassociate | Disassociate service dependencies |
| GET | /service_dependencies/technical_services/{id} | Get technical service dependencies |

### services
| Method | Path | Description |
|--------|------|-------------|
| GET | /services | List services |
| POST | /services | Create a service |
| GET | /services/{id} | Get a service |
| DELETE | /services/{id} | Delete a service |
| PUT | /services/{id} | Update a service |
| GET | /services/{id}/audit/records | List audit records for a service |
| GET | /services/{id}/change_events | List Change Events for a service |
| POST | /services/{id}/integrations | Create a new integration |
| PUT | /services/{id}/integrations/{integration_id} | Update an existing integration |
| GET | /services/{id}/integrations/{integration_id} | View an integration |
| GET | /services/{id}/rules | List Service's Event Rules |
| POST | /services/{id}/rules | Create an Event Rule on a Service |
| POST | /services/{id}/rules/convert | Convert a Service's Event Rules into Event Orchestration Rules |
| GET | /services/{id}/rules/{rule_id} | Get an Event Rule from a Service |
| PUT | /services/{id}/rules/{rule_id} | Update an Event Rule on a Service |
| DELETE | /services/{id}/rules/{rule_id} | Delete an Event Rule from a Service |
| POST | /services/custom_fields | Create a Field |
| GET | /services/custom_fields | List Fields |
| GET | /services/custom_fields/{field_id} | Get a Field |
| PUT | /services/custom_fields/{field_id} | Update a Field |
| DELETE | /services/custom_fields/{field_id} | Delete a Field |
| GET | /services/custom_fields/{field_id}/field_options | List Field Options |
| POST | /services/custom_fields/{field_id}/field_options | Create a Field Option |
| GET | /services/custom_fields/{field_id}/field_options/{field_option_id} | Get a Field Option |
| PUT | /services/custom_fields/{field_id}/field_options/{field_option_id} | Update a Field Option |
| DELETE | /services/custom_fields/{field_id}/field_options/{field_option_id} | Delete a Field Option |
| GET | /services/{id}/custom_fields/values | Get Custom Field Values |
| PUT | /services/{id}/custom_fields/values | Update Custom Field Values |
| GET | /services/{id}/enablements | Get Enablements for a Service |
| PUT | /services/{id}/enablements/{feature_name} | Update an Enablement for a Service |

### session_configurations
| Method | Path | Description |
|--------|------|-------------|
| GET | /session_configurations | Get an account's session configurations |
| PUT | /session_configurations | Configure an account's session configurations |
| DELETE | /session_configurations | Delete an account's session configurations. |

### standards
| Method | Path | Description |
|--------|------|-------------|
| GET | /standards | List Standards |
| PUT | /standards/{id} | Update a standard |
| GET | /standards/scores/{resource_type} | List resources' standards scores |
| GET | /standards/scores/{resource_type}/{id} | List a resource's standards scores |

### status_dashboards
| Method | Path | Description |
|--------|------|-------------|
| GET | /status_dashboards | List Status Dashboards |
| GET | /status_dashboards/{id} | Get a single Status Dashboard by `id` |
| GET | /status_dashboards/{id}/service_impacts | Get impacted Business Services for a Status Dashboard by `id`. |
| GET | /status_dashboards/url_slugs/{url_slug} | Get a single Status Dashboard by `url_slug` |
| GET | /status_dashboards/url_slugs/{url_slug}/service_impacts | Get impacted Business Services for a  Status Dashboard by `url_slug` |

### status_pages
| Method | Path | Description |
|--------|------|-------------|
| GET | /status_pages | List Status Pages |
| GET | /status_pages/{id}/impacts | List Status Page Impacts |
| GET | /status_pages/{id}/impacts/{impact_id} | Get a Status Page Impact |
| GET | /status_pages/{id}/services | List Status Page Services |
| GET | /status_pages/{id}/services/{service_id} | Get a Status Page Service |
| GET | /status_pages/{id}/severities | List Status Page Severities |
| GET | /status_pages/{id}/severities/{severity_id} | Get a Status Page Severity |
| GET | /status_pages/{id}/statuses | List Status Page Statuses |
| GET | /status_pages/{id}/statuses/{status_id} | Get a Status Page Status |
| GET | /status_pages/{id}/posts | List Status Page Posts |
| POST | /status_pages/{id}/posts | Create a Status Page Post |
| GET | /status_pages/{id}/posts/{post_id} | Get a Status Page Post |
| PUT | /status_pages/{id}/posts/{post_id} | Update a Status Page Post |
| DELETE | /status_pages/{id}/posts/{post_id} | Delete a Status Page Post |
| GET | /status_pages/{id}/posts/{post_id}/post_updates | List Status Page Post Updates |
| POST | /status_pages/{id}/posts/{post_id}/post_updates | Create a Status Page Post Update |
| GET | /status_pages/{id}/posts/{post_id}/post_updates/{post_update_id} | Get a Status Page Post Update |
| PUT | /status_pages/{id}/posts/{post_id}/post_updates/{post_update_id} | Update a Status Page Post Update |
| DELETE | /status_pages/{id}/posts/{post_id}/post_updates/{post_update_id} | Delete a Status Page Post Update |
| GET | /status_pages/{id}/posts/{post_id}/postmortem | Get a Post Postmortem |
| POST | /status_pages/{id}/posts/{post_id}/postmortem | Create a Post Postmortem |
| PUT | /status_pages/{id}/posts/{post_id}/postmortem | Update a Post Postmortem |
| DELETE | /status_pages/{id}/posts/{post_id}/postmortem | Delete a Post Postmortem |
| GET | /status_pages/{id}/subscriptions | List Status Page Subscriptions |
| POST | /status_pages/{id}/subscriptions | Create a Status Page Subscription |
| GET | /status_pages/{id}/subscriptions/{subscription_id} | Get a Status Page Subscription |
| DELETE | /status_pages/{id}/subscriptions/{subscription_id} | Delete a Status Page Subscription |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags | List tags |
| POST | /tags | Create a tag |
| GET | /tags/{id} | Get a tag |
| DELETE | /tags/{id} | Delete a tag |
| GET | /tags/{id}/{entity_type} | Get connected entities |

### teams
| Method | Path | Description |
|--------|------|-------------|
| POST | /teams | Create a team |
| GET | /teams | List teams |
| GET | /teams/{id} | Get a team |
| DELETE | /teams/{id} | Delete a team |
| PUT | /teams/{id} | Update a team |
| GET | /teams/{id}/audit/records | List audit records for a team |
| DELETE | /teams/{id}/escalation_policies/{escalation_policy_id} | Remove an escalation policy from a team |
| PUT | /teams/{id}/escalation_policies/{escalation_policy_id} | Add an escalation policy to a team |
| GET | /teams/{id}/members | List members of a team |
| GET | /teams/{id}/notification_subscriptions | List Team Notification Subscriptions |
| POST | /teams/{id}/notification_subscriptions | Create Team Notification Subscriptions |
| POST | /teams/{id}/notification_subscriptions/unsubscribe | Unsubscribe the given Team from Notifications on the matching Subscribable entities. |
| DELETE | /teams/{id}/users/{user_id} | Remove a user from a team |
| PUT | /teams/{id}/users/{user_id} | Add a user to a team |

### templates
| Method | Path | Description |
|--------|------|-------------|
| GET | /templates | List templates |
| POST | /templates | Create a template |
| GET | /templates/{id} | Get a template |
| PUT | /templates/{id} | Update a template |
| DELETE | /templates/{id} | Delete a template |
| POST | /templates/{id}/render | Render a template |
| GET | /templates/fields | List template fields |

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /users | List users |
| POST | /users | Create a user |
| GET | /users/{id} | Get a user |
| DELETE | /users/{id} | Delete a user |
| PUT | /users/{id} | Update a user |
| GET | /users/{id}/audit/records | List audit records for a user |
| GET | /users/{id}/contact_methods | List a user's contact methods |
| POST | /users/{id}/contact_methods | Create a user contact method |
| GET | /users/{id}/contact_methods/{contact_method_id} | Get a user's contact method |
| DELETE | /users/{id}/contact_methods/{contact_method_id} | Delete a user's contact method |
| PUT | /users/{id}/contact_methods/{contact_method_id} | Update a user's contact method |
| GET | /users/{id}/license | Get the License allocated to a User |
| GET | /users/{id}/notification_rules | List a user's notification rules |
| POST | /users/{id}/notification_rules | Create a user notification rule |
| GET | /users/{id}/notification_rules/{notification_rule_id} | Get a user's notification rule |
| DELETE | /users/{id}/notification_rules/{notification_rule_id} | Delete a user's notification rule |
| PUT | /users/{id}/notification_rules/{notification_rule_id} | Update a user's notification rule |
| GET | /users/{id}/notification_subscriptions | List Notification Subscriptions |
| POST | /users/{id}/notification_subscriptions | Create Notification Subcriptions |
| POST | /users/{id}/notification_subscriptions/unsubscribe | Remove Notification Subscriptions |
| GET | /users/{id}/oncall_handoff_notification_rules | List a User's Handoff Notification Rules |
| POST | /users/{id}/oncall_handoff_notification_rules | Create a User Handoff Notification Rule |
| GET | /users/{id}/oncall_handoff_notification_rules/{oncall_handoff_notification_rule_id} | Get a user's handoff notification rule |
| DELETE | /users/{id}/oncall_handoff_notification_rules/{oncall_handoff_notification_rule_id} | Delete a User's Handoff Notification rule |
| PUT | /users/{id}/oncall_handoff_notification_rules/{oncall_handoff_notification_rule_id} | Update a User's Handoff Notification Rule |
| GET | /users/{id}/sessions | List a user's active sessions |
| DELETE | /users/{id}/sessions | Delete all user sessions |
| GET | /users/{id}/sessions/{type}/{session_id} | Get a user's session |
| DELETE | /users/{id}/sessions/{type}/{session_id} | Delete a user's session |
| GET | /users/{id}/status_update_notification_rules | List a user's status update notification rules |
| POST | /users/{id}/status_update_notification_rules | Create a user status update notification rule |
| GET | /users/{id}/status_update_notification_rules/{status_update_notification_rule_id} | Get a user's status update notification rule |
| DELETE | /users/{id}/status_update_notification_rules/{status_update_notification_rule_id} | Delete a user's status update notification rule |
| PUT | /users/{id}/status_update_notification_rules/{status_update_notification_rule_id} | Update a user's status update notification rule |
| GET | /users/me | Get the current user |

### vendors
| Method | Path | Description |
|--------|------|-------------|
| GET | /vendors | List vendors |
| GET | /vendors/{id} | Get a vendor |

### webhook_subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /webhook_subscriptions | List webhook subscriptions |
| POST | /webhook_subscriptions | Create a webhook subscription |
| GET | /webhook_subscriptions/{id} | Get a webhook subscription |
| PUT | /webhook_subscriptions/{id} | Update a webhook subscription |
| DELETE | /webhook_subscriptions/{id} | Delete a webhook subscription |
| POST | /webhook_subscriptions/{id}/enable | Enable a webhook subscription |
| POST | /webhook_subscriptions/{id}/ping | Test a webhook subscription |
| GET | /webhook_subscriptions/oauth_clients | List OAuth clients |
| POST | /webhook_subscriptions/oauth_clients | Create an OAuth client |
| GET | /webhook_subscriptions/oauth_clients/{id} | Get an OAuth client |
| PUT | /webhook_subscriptions/oauth_clients/{id} | Update an OAuth client |
| DELETE | /webhook_subscriptions/oauth_clients/{id} | Delete an OAuth client |

### workflows
| Method | Path | Description |
|--------|------|-------------|
| GET | /workflows/integrations | List Workflow Integrations |
| GET | /workflows/integrations/{id} | Get Workflow Integration |
| GET | /workflows/integrations/connections | List all Workflow Integration Connections |
| GET | /workflows/integrations/{integration_id}/connections | List Workflow Integration Connections |
| POST | /workflows/integrations/{integration_id}/connections | Create Workflow Integration Connection |
| GET | /workflows/integrations/{integration_id}/connections/{id} | Get Workflow Integration Connection |
| PATCH | /workflows/integrations/{integration_id}/connections/{id} | Update Workflow Integration Connection |
| DELETE | /workflows/integrations/{integration_id}/connections/{id} | Delete Workflow Integration Connection |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a change_tag?" -> POST /{entity_type}/{id}/change_tags
- "List all tags?" -> GET /{entity_type}/{id}/tags
- "List all abilities?" -> GET /abilities
- "Get ability details?" -> GET /abilities/{id}
- "List all addons?" -> GET /addons
- "Create a addon?" -> POST /addons
- "Get addon details?" -> GET /addons/{id}
- "Delete a addon?" -> DELETE /addons/{id}
- "Update a addon?" -> PUT /addons/{id}
- "List all alert_grouping_settings?" -> GET /alert_grouping_settings
- "Create a alert_grouping_setting?" -> POST /alert_grouping_settings
- "Get alert_grouping_setting details?" -> GET /alert_grouping_settings/{id}
- "Delete a alert_grouping_setting?" -> DELETE /alert_grouping_settings/{id}
- "Update a alert_grouping_setting?" -> PUT /alert_grouping_settings/{id}
- "Create a all?" -> POST /analytics/metrics/incidents/all
- "Create a escalation_policy?" -> POST /analytics/metrics/incidents/escalation_policies
- "Create a all?" -> POST /analytics/metrics/incidents/escalation_policies/all
- "Create a service?" -> POST /analytics/metrics/incidents/services
- "Create a all?" -> POST /analytics/metrics/incidents/services/all
- "Create a team?" -> POST /analytics/metrics/incidents/teams
- "Create a all?" -> POST /analytics/metrics/incidents/teams/all
- "Create a feature?" -> POST /analytics/metrics/pd_advance_usage/features
- "Create a all?" -> POST /analytics/metrics/responders/all
- "Create a team?" -> POST /analytics/metrics/responders/teams
- "Create a all?" -> POST /analytics/metrics/users/all
- "Create a incident?" -> POST /analytics/raw/incidents
- "Get incident details?" -> GET /analytics/raw/incidents/{id}
- "List all responses?" -> GET /analytics/raw/incidents/{id}/responses
- "Create a incident?" -> POST /analytics/raw/responders/{responder_id}/incidents
- "Create a user?" -> POST /analytics/raw/users
- "List all records?" -> GET /audit/records
- "Create a action?" -> POST /automation_actions/actions
- "List all actions?" -> GET /automation_actions/actions
- "Get action details?" -> GET /automation_actions/actions/{id}
- "Delete a action?" -> DELETE /automation_actions/actions/{id}
- "Update a action?" -> PUT /automation_actions/actions/{id}
- "Create a invocation?" -> POST /automation_actions/actions/{id}/invocations
- "List all services?" -> GET /automation_actions/actions/{id}/services
- "Create a service?" -> POST /automation_actions/actions/{id}/services
- "Get service details?" -> GET /automation_actions/actions/{id}/services/{service_id}
- "Delete a service?" -> DELETE /automation_actions/actions/{id}/services/{service_id}
- "Create a team?" -> POST /automation_actions/actions/{id}/teams
- "List all teams?" -> GET /automation_actions/actions/{id}/teams
- "Delete a team?" -> DELETE /automation_actions/actions/{id}/teams/{team_id}
- "Get team details?" -> GET /automation_actions/actions/{id}/teams/{team_id}
- "List all invocations?" -> GET /automation_actions/invocations
- "Get invocation details?" -> GET /automation_actions/invocations/{id}
- "Create a runner?" -> POST /automation_actions/runners
- "List all runners?" -> GET /automation_actions/runners
- "Get runner details?" -> GET /automation_actions/runners/{id}
- "Update a runner?" -> PUT /automation_actions/runners/{id}
- "Delete a runner?" -> DELETE /automation_actions/runners/{id}
- "Create a team?" -> POST /automation_actions/runners/{id}/teams
- "List all teams?" -> GET /automation_actions/runners/{id}/teams
- "Delete a team?" -> DELETE /automation_actions/runners/{id}/teams/{team_id}
- "Get team details?" -> GET /automation_actions/runners/{id}/teams/{team_id}
- "List all business_services?" -> GET /business_services
- "Create a business_service?" -> POST /business_services
- "Get business_service details?" -> GET /business_services/{id}
- "Delete a business_service?" -> DELETE /business_services/{id}
- "Update a business_service?" -> PUT /business_services/{id}
- "Create a account_subscription?" -> POST /business_services/{id}/account_subscription
- "List all subscribers?" -> GET /business_services/{id}/subscribers
- "Create a subscriber?" -> POST /business_services/{id}/subscribers
- "List all impacts?" -> GET /business_services/{id}/supporting_services/impacts
- "Create a unsubscribe?" -> POST /business_services/{id}/unsubscribe
- "List all impactors?" -> GET /business_services/impactors
- "List all impacts?" -> GET /business_services/impacts
- "List all priority_thresholds?" -> GET /business_services/priority_thresholds
- "List all change_events?" -> GET /change_events
- "Create a change_event?" -> POST /change_events
- "Get change_event details?" -> GET /change_events/{id}
- "Update a change_event?" -> PUT /change_events/{id}
- "Search escalation_policies?" -> GET /escalation_policies
- "Create a escalation_policy?" -> POST /escalation_policies
- "Get escalation_policy details?" -> GET /escalation_policies/{id}
- "Delete a escalation_policy?" -> DELETE /escalation_policies/{id}
- "Update a escalation_policy?" -> PUT /escalation_policies/{id}
- "List all records?" -> GET /escalation_policies/{id}/audit/records
- "List all event_orchestrations?" -> GET /event_orchestrations
- "Create a event_orchestration?" -> POST /event_orchestrations
- "Get event_orchestration details?" -> GET /event_orchestrations/{id}
- "Update a event_orchestration?" -> PUT /event_orchestrations/{id}
- "Delete a event_orchestration?" -> DELETE /event_orchestrations/{id}
- "List all integrations?" -> GET /event_orchestrations/{id}/integrations
- "Create a integration?" -> POST /event_orchestrations/{id}/integrations
- "Get integration details?" -> GET /event_orchestrations/{id}/integrations/{integration_id}
- "Update a integration?" -> PUT /event_orchestrations/{id}/integrations/{integration_id}
- "Delete a integration?" -> DELETE /event_orchestrations/{id}/integrations/{integration_id}
- "Create a migration?" -> POST /event_orchestrations/{id}/integrations/migration
- "List all global?" -> GET /event_orchestrations/{id}/global
- "List all router?" -> GET /event_orchestrations/{id}/router
- "List all unrouted?" -> GET /event_orchestrations/{id}/unrouted
- "Get service details?" -> GET /event_orchestrations/services/{service_id}
- "Update a service?" -> PUT /event_orchestrations/services/{service_id}
- "List all active?" -> GET /event_orchestrations/services/{service_id}/active
- "List all cache_variables?" -> GET /event_orchestrations/{id}/cache_variables
- "Create a cache_variable?" -> POST /event_orchestrations/{id}/cache_variables
- "Get cache_variable details?" -> GET /event_orchestrations/{id}/cache_variables/{cache_variable_id}
- "Update a cache_variable?" -> PUT /event_orchestrations/{id}/cache_variables/{cache_variable_id}
- "Delete a cache_variable?" -> DELETE /event_orchestrations/{id}/cache_variables/{cache_variable_id}
- "List all data?" -> GET /event_orchestrations/{id}/cache_variables/{cache_variable_id}/data
- "List all cache_variables?" -> GET /event_orchestrations/services/{service_id}/cache_variables
- "Create a cache_variable?" -> POST /event_orchestrations/services/{service_id}/cache_variables
- "Get cache_variable details?" -> GET /event_orchestrations/services/{service_id}/cache_variables/{cache_variable_id}
- "Update a cache_variable?" -> PUT /event_orchestrations/services/{service_id}/cache_variables/{cache_variable_id}
- "Delete a cache_variable?" -> DELETE /event_orchestrations/services/{service_id}/cache_variables/{cache_variable_id}
- "List all data?" -> GET /event_orchestrations/services/{service_id}/cache_variables/{cache_variable_id}/data
- "List all enablements?" -> GET /event_orchestrations/{id}/enablements
- "Update a enablement?" -> PUT /event_orchestrations/{id}/enablements/{feature_name}
- "List all extension_schemas?" -> GET /extension_schemas
- "Get extension_schema details?" -> GET /extension_schemas/{id}
- "Search extensions?" -> GET /extensions
- "Create a extension?" -> POST /extensions
- "Get extension details?" -> GET /extensions/{id}
- "Delete a extension?" -> DELETE /extensions/{id}
- "Update a extension?" -> PUT /extensions/{id}
- "Create a enable?" -> POST /extensions/{id}/enable
- "Search incident_workflows?" -> GET /incident_workflows
- "Create a incident_workflow?" -> POST /incident_workflows
- "Get incident_workflow details?" -> GET /incident_workflows/{id}
- "Delete a incident_workflow?" -> DELETE /incident_workflows/{id}
- "Update a incident_workflow?" -> PUT /incident_workflows/{id}
- "Create a instance?" -> POST /incident_workflows/{id}/instances
- "List all actions?" -> GET /incident_workflows/actions
- "Get action details?" -> GET /incident_workflows/actions/{id}
- "List all triggers?" -> GET /incident_workflows/triggers
- "Create a trigger?" -> POST /incident_workflows/triggers
- "Get trigger details?" -> GET /incident_workflows/triggers/{id}
- "Update a trigger?" -> PUT /incident_workflows/triggers/{id}
- "Delete a trigger?" -> DELETE /incident_workflows/triggers/{id}
- "Create a service?" -> POST /incident_workflows/triggers/{id}/services
- "Delete a service?" -> DELETE /incident_workflows/triggers/{trigger_id}/services/{service_id}
- "List all incidents?" -> GET /incidents
- "Create a incident?" -> POST /incidents
- "Get incident details?" -> GET /incidents/{id}
- "Update a incident?" -> PUT /incidents/{id}
- "List all alerts?" -> GET /incidents/{id}/alerts
- "Get alert details?" -> GET /incidents/{id}/alerts/{alert_id}
- "Update a alert?" -> PUT /incidents/{id}/alerts/{alert_id}
- "List all impacts?" -> GET /incidents/{id}/business_services/impacts
- "List all values?" -> GET /incidents/{id}/custom_fields/values
- "List all log_entries?" -> GET /incidents/{id}/log_entries
- "List all notes?" -> GET /incidents/{id}/notes
- "Create a note?" -> POST /incidents/{id}/notes
- "Update a note?" -> PUT /incidents/{id}/notes/{note_id}
- "Delete a note?" -> DELETE /incidents/{id}/notes/{note_id}
- "List all outlier_incident?" -> GET /incidents/{id}/outlier_incident
- "List all past_incidents?" -> GET /incidents/{id}/past_incidents
- "List all related_change_events?" -> GET /incidents/{id}/related_change_events
- "List all related_incidents?" -> GET /incidents/{id}/related_incidents
- "Create a responder_request?" -> POST /incidents/{id}/responder_requests
- "Create a snooze?" -> POST /incidents/{id}/snooze
- "Create a status_update?" -> POST /incidents/{id}/status_updates
- "List all subscribers?" -> GET /incidents/{id}/status_updates/subscribers
- "Create a subscriber?" -> POST /incidents/{id}/status_updates/subscribers
- "Create a unsubscribe?" -> POST /incidents/{id}/status_updates/unsubscribe
- "List all types?" -> GET /incidents/types
- "Create a type?" -> POST /incidents/types
- "Get type details?" -> GET /incidents/types/{type_id_or_name}
- "Update a type?" -> PUT /incidents/types/{type_id_or_name}
- "List all custom_fields?" -> GET /incidents/types/{type_id_or_name}/custom_fields
- "Create a custom_field?" -> POST /incidents/types/{type_id_or_name}/custom_fields
- "Get custom_field details?" -> GET /incidents/types/{type_id_or_name}/custom_fields/{field_id}
- "Update a custom_field?" -> PUT /incidents/types/{type_id_or_name}/custom_fields/{field_id}
- "Delete a custom_field?" -> DELETE /incidents/types/{type_id_or_name}/custom_fields/{field_id}
- "List all field_options?" -> GET /incidents/types/{type_id_or_name}/custom_fields/{field_id}/field_options
- "Create a field_option?" -> POST /incidents/types/{type_id_or_name}/custom_fields/{field_id}/field_options
- "Get field_option details?" -> GET /incidents/types/{type_id_or_name}/custom_fields/{field_id}/field_options/{field_option_id}
- "Update a field_option?" -> PUT /incidents/types/{type_id_or_name}/custom_fields/{field_id}/field_options/{field_option_id}
- "Delete a field_option?" -> DELETE /incidents/types/{type_id_or_name}/custom_fields/{field_id}/field_options/{field_option_id}
- "Create a custom_field?" -> POST /incidents/custom_fields
- "List all custom_fields?" -> GET /incidents/custom_fields
- "Get custom_field details?" -> GET /incidents/custom_fields/{field_id}
- "Update a custom_field?" -> PUT /incidents/custom_fields/{field_id}
- "Delete a custom_field?" -> DELETE /incidents/custom_fields/{field_id}
- "Create a field_option?" -> POST /incidents/custom_fields/{field_id}/field_options
- "List all field_options?" -> GET /incidents/custom_fields/{field_id}/field_options
- "Update a field_option?" -> PUT /incidents/custom_fields/{field_id}/field_options/{field_option_id}
- "Delete a field_option?" -> DELETE /incidents/custom_fields/{field_id}/field_options/{field_option_id}
- "List all license_allocations?" -> GET /license_allocations
- "List all licenses?" -> GET /licenses
- "List all log_entries?" -> GET /log_entries
- "Get log_entry details?" -> GET /log_entries/{id}
- "Search maintenance_windows?" -> GET /maintenance_windows
- "Create a maintenance_window?" -> POST /maintenance_windows
- "Get maintenance_window details?" -> GET /maintenance_windows/{id}
- "Delete a maintenance_window?" -> DELETE /maintenance_windows/{id}
- "Update a maintenance_window?" -> PUT /maintenance_windows/{id}
- "List all notifications?" -> GET /notifications
- "List all status?" -> GET /oauth_delegations/revocation_requests/status
- "List all oncalls?" -> GET /oncalls
- "List all alerts?" -> GET /paused_incident_reports/alerts
- "List all counts?" -> GET /paused_incident_reports/counts
- "List all priorities?" -> GET /priorities
- "List all rulesets?" -> GET /rulesets
- "Create a ruleset?" -> POST /rulesets
- "Get ruleset details?" -> GET /rulesets/{id}
- "Update a ruleset?" -> PUT /rulesets/{id}
- "Delete a ruleset?" -> DELETE /rulesets/{id}
- "List all rules?" -> GET /rulesets/{id}/rules
- "Create a rule?" -> POST /rulesets/{id}/rules
- "Get rule details?" -> GET /rulesets/{id}/rules/{rule_id}
- "Update a rule?" -> PUT /rulesets/{id}/rules/{rule_id}
- "Delete a rule?" -> DELETE /rulesets/{id}/rules/{rule_id}
- "Search schedules?" -> GET /schedules
- "Create a schedule?" -> POST /schedules
- "Get schedule details?" -> GET /schedules/{id}
- "Delete a schedule?" -> DELETE /schedules/{id}
- "Update a schedule?" -> PUT /schedules/{id}
- "List all records?" -> GET /schedules/{id}/audit/records
- "List all overrides?" -> GET /schedules/{id}/overrides
- "Create a override?" -> POST /schedules/{id}/overrides
- "Delete a override?" -> DELETE /schedules/{id}/overrides/{override_id}
- "List all users?" -> GET /schedules/{id}/users
- "Create a preview?" -> POST /schedules/preview
- "Create a associate?" -> POST /service_dependencies/associate
- "Get business_service details?" -> GET /service_dependencies/business_services/{id}
- "Create a disassociate?" -> POST /service_dependencies/disassociate
- "Get technical_service details?" -> GET /service_dependencies/technical_services/{id}
- "Search services?" -> GET /services
- "Create a service?" -> POST /services
- "Get service details?" -> GET /services/{id}
- "Delete a service?" -> DELETE /services/{id}
- "Update a service?" -> PUT /services/{id}
- "List all records?" -> GET /services/{id}/audit/records
- "List all change_events?" -> GET /services/{id}/change_events
- "Create a integration?" -> POST /services/{id}/integrations
- "Update a integration?" -> PUT /services/{id}/integrations/{integration_id}
- "Get integration details?" -> GET /services/{id}/integrations/{integration_id}
- "List all rules?" -> GET /services/{id}/rules
- "Create a rule?" -> POST /services/{id}/rules
- "Create a convert?" -> POST /services/{id}/rules/convert
- "Get rule details?" -> GET /services/{id}/rules/{rule_id}
- "Update a rule?" -> PUT /services/{id}/rules/{rule_id}
- "Delete a rule?" -> DELETE /services/{id}/rules/{rule_id}
- "Create a custom_field?" -> POST /services/custom_fields
- "List all custom_fields?" -> GET /services/custom_fields
- "Get custom_field details?" -> GET /services/custom_fields/{field_id}
- "Update a custom_field?" -> PUT /services/custom_fields/{field_id}
- "Delete a custom_field?" -> DELETE /services/custom_fields/{field_id}
- "List all field_options?" -> GET /services/custom_fields/{field_id}/field_options
- "Create a field_option?" -> POST /services/custom_fields/{field_id}/field_options
- "Get field_option details?" -> GET /services/custom_fields/{field_id}/field_options/{field_option_id}
- "Update a field_option?" -> PUT /services/custom_fields/{field_id}/field_options/{field_option_id}
- "Delete a field_option?" -> DELETE /services/custom_fields/{field_id}/field_options/{field_option_id}
- "List all values?" -> GET /services/{id}/custom_fields/values
- "List all enablements?" -> GET /services/{id}/enablements
- "Update a enablement?" -> PUT /services/{id}/enablements/{feature_name}
- "List all session_configurations?" -> GET /session_configurations
- "List all standards?" -> GET /standards
- "Update a standard?" -> PUT /standards/{id}
- "Get score details?" -> GET /standards/scores/{resource_type}
- "Get score details?" -> GET /standards/scores/{resource_type}/{id}
- "List all status_dashboards?" -> GET /status_dashboards
- "Get status_dashboard details?" -> GET /status_dashboards/{id}
- "List all service_impacts?" -> GET /status_dashboards/{id}/service_impacts
- "Get url_slug details?" -> GET /status_dashboards/url_slugs/{url_slug}
- "List all service_impacts?" -> GET /status_dashboards/url_slugs/{url_slug}/service_impacts
- "List all status_pages?" -> GET /status_pages
- "List all impacts?" -> GET /status_pages/{id}/impacts
- "Get impact details?" -> GET /status_pages/{id}/impacts/{impact_id}
- "List all services?" -> GET /status_pages/{id}/services
- "Get service details?" -> GET /status_pages/{id}/services/{service_id}
- "List all severities?" -> GET /status_pages/{id}/severities
- "Get severity details?" -> GET /status_pages/{id}/severities/{severity_id}
- "List all statuses?" -> GET /status_pages/{id}/statuses
- "Get statuse details?" -> GET /status_pages/{id}/statuses/{status_id}
- "List all posts?" -> GET /status_pages/{id}/posts
- "Create a post?" -> POST /status_pages/{id}/posts
- "Get post details?" -> GET /status_pages/{id}/posts/{post_id}
- "Update a post?" -> PUT /status_pages/{id}/posts/{post_id}
- "Delete a post?" -> DELETE /status_pages/{id}/posts/{post_id}
- "List all post_updates?" -> GET /status_pages/{id}/posts/{post_id}/post_updates
- "Create a post_update?" -> POST /status_pages/{id}/posts/{post_id}/post_updates
- "Get post_update details?" -> GET /status_pages/{id}/posts/{post_id}/post_updates/{post_update_id}
- "Update a post_update?" -> PUT /status_pages/{id}/posts/{post_id}/post_updates/{post_update_id}
- "Delete a post_update?" -> DELETE /status_pages/{id}/posts/{post_id}/post_updates/{post_update_id}
- "List all postmortem?" -> GET /status_pages/{id}/posts/{post_id}/postmortem
- "Create a postmortem?" -> POST /status_pages/{id}/posts/{post_id}/postmortem
- "List all subscriptions?" -> GET /status_pages/{id}/subscriptions
- "Create a subscription?" -> POST /status_pages/{id}/subscriptions
- "Get subscription details?" -> GET /status_pages/{id}/subscriptions/{subscription_id}
- "Delete a subscription?" -> DELETE /status_pages/{id}/subscriptions/{subscription_id}
- "Search tags?" -> GET /tags
- "Create a tag?" -> POST /tags
- "Get tag details?" -> GET /tags/{id}
- "Delete a tag?" -> DELETE /tags/{id}
- "Get tag details?" -> GET /tags/{id}/{entity_type}
- "Create a team?" -> POST /teams
- "Search teams?" -> GET /teams
- "Get team details?" -> GET /teams/{id}
- "Delete a team?" -> DELETE /teams/{id}
- "Update a team?" -> PUT /teams/{id}
- "List all records?" -> GET /teams/{id}/audit/records
- "Delete a escalation_policy?" -> DELETE /teams/{id}/escalation_policies/{escalation_policy_id}
- "Update a escalation_policy?" -> PUT /teams/{id}/escalation_policies/{escalation_policy_id}
- "List all members?" -> GET /teams/{id}/members
- "List all notification_subscriptions?" -> GET /teams/{id}/notification_subscriptions
- "Create a notification_subscription?" -> POST /teams/{id}/notification_subscriptions
- "Create a unsubscribe?" -> POST /teams/{id}/notification_subscriptions/unsubscribe
- "Delete a user?" -> DELETE /teams/{id}/users/{user_id}
- "Update a user?" -> PUT /teams/{id}/users/{user_id}
- "Search templates?" -> GET /templates
- "Create a template?" -> POST /templates
- "Get template details?" -> GET /templates/{id}
- "Update a template?" -> PUT /templates/{id}
- "Delete a template?" -> DELETE /templates/{id}
- "Create a render?" -> POST /templates/{id}/render
- "List all fields?" -> GET /templates/fields
- "Search users?" -> GET /users
- "Create a user?" -> POST /users
- "Get user details?" -> GET /users/{id}
- "Delete a user?" -> DELETE /users/{id}
- "Update a user?" -> PUT /users/{id}
- "List all records?" -> GET /users/{id}/audit/records
- "List all contact_methods?" -> GET /users/{id}/contact_methods
- "Create a contact_method?" -> POST /users/{id}/contact_methods
- "Get contact_method details?" -> GET /users/{id}/contact_methods/{contact_method_id}
- "Delete a contact_method?" -> DELETE /users/{id}/contact_methods/{contact_method_id}
- "Update a contact_method?" -> PUT /users/{id}/contact_methods/{contact_method_id}
- "List all license?" -> GET /users/{id}/license
- "List all notification_rules?" -> GET /users/{id}/notification_rules
- "Create a notification_rule?" -> POST /users/{id}/notification_rules
- "Get notification_rule details?" -> GET /users/{id}/notification_rules/{notification_rule_id}
- "Delete a notification_rule?" -> DELETE /users/{id}/notification_rules/{notification_rule_id}
- "Update a notification_rule?" -> PUT /users/{id}/notification_rules/{notification_rule_id}
- "List all notification_subscriptions?" -> GET /users/{id}/notification_subscriptions
- "Create a notification_subscription?" -> POST /users/{id}/notification_subscriptions
- "Create a unsubscribe?" -> POST /users/{id}/notification_subscriptions/unsubscribe
- "List all oncall_handoff_notification_rules?" -> GET /users/{id}/oncall_handoff_notification_rules
- "Create a oncall_handoff_notification_rule?" -> POST /users/{id}/oncall_handoff_notification_rules
- "Get oncall_handoff_notification_rule details?" -> GET /users/{id}/oncall_handoff_notification_rules/{oncall_handoff_notification_rule_id}
- "Delete a oncall_handoff_notification_rule?" -> DELETE /users/{id}/oncall_handoff_notification_rules/{oncall_handoff_notification_rule_id}
- "Update a oncall_handoff_notification_rule?" -> PUT /users/{id}/oncall_handoff_notification_rules/{oncall_handoff_notification_rule_id}
- "List all sessions?" -> GET /users/{id}/sessions
- "Get session details?" -> GET /users/{id}/sessions/{type}/{session_id}
- "Delete a session?" -> DELETE /users/{id}/sessions/{type}/{session_id}
- "List all status_update_notification_rules?" -> GET /users/{id}/status_update_notification_rules
- "Create a status_update_notification_rule?" -> POST /users/{id}/status_update_notification_rules
- "Get status_update_notification_rule details?" -> GET /users/{id}/status_update_notification_rules/{status_update_notification_rule_id}
- "Delete a status_update_notification_rule?" -> DELETE /users/{id}/status_update_notification_rules/{status_update_notification_rule_id}
- "Update a status_update_notification_rule?" -> PUT /users/{id}/status_update_notification_rules/{status_update_notification_rule_id}
- "List all me?" -> GET /users/me
- "List all vendors?" -> GET /vendors
- "Get vendor details?" -> GET /vendors/{id}
- "List all webhook_subscriptions?" -> GET /webhook_subscriptions
- "Create a webhook_subscription?" -> POST /webhook_subscriptions
- "Get webhook_subscription details?" -> GET /webhook_subscriptions/{id}
- "Update a webhook_subscription?" -> PUT /webhook_subscriptions/{id}
- "Delete a webhook_subscription?" -> DELETE /webhook_subscriptions/{id}
- "Create a enable?" -> POST /webhook_subscriptions/{id}/enable
- "Create a ping?" -> POST /webhook_subscriptions/{id}/ping
- "List all oauth_clients?" -> GET /webhook_subscriptions/oauth_clients
- "Create a oauth_client?" -> POST /webhook_subscriptions/oauth_clients
- "Get oauth_client details?" -> GET /webhook_subscriptions/oauth_clients/{id}
- "Update a oauth_client?" -> PUT /webhook_subscriptions/oauth_clients/{id}
- "Delete a oauth_client?" -> DELETE /webhook_subscriptions/oauth_clients/{id}
- "List all integrations?" -> GET /workflows/integrations
- "Get integration details?" -> GET /workflows/integrations/{id}
- "List all connections?" -> GET /workflows/integrations/connections
- "List all connections?" -> GET /workflows/integrations/{integration_id}/connections
- "Create a connection?" -> POST /workflows/integrations/{integration_id}/connections
- "Get connection details?" -> GET /workflows/integrations/{integration_id}/connections/{id}
- "Partially update a connection?" -> PATCH /workflows/integrations/{integration_id}/connections/{id}
- "Delete a connection?" -> DELETE /workflows/integrations/{integration_id}/connections/{id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
