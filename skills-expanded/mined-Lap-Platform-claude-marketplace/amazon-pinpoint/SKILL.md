---
name: amazon-pinpoint
description: "Amazon Pinpoint API skill. Use when working with Amazon Pinpoint for apps, templates, recommenders. Covers 122 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Pinpoint
API version: 2016-12-01

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /v1/apps -- verify access
3. POST /v1/apps -- create first apps

## Endpoints

122 endpoints across 5 groups. See references/api-spec.lap for full details.

### apps
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/apps | Creates an application. |
| POST | /v1/apps/{application-id}/campaigns | Creates a new campaign for an application or updates the settings of an existing campaign for an application. |
| POST | /v1/apps/{application-id}/jobs/export | Creates an export job for an application. |
| POST | /v1/apps/{application-id}/jobs/import | Creates an import job for an application. |
| POST | /v1/apps/{application-id}/journeys | Creates a journey for an application. |
| POST | /v1/apps/{application-id}/segments | Creates a new segment for an application or updates the configuration, dimension, and other settings for an existing segment that's associated with an application. |
| DELETE | /v1/apps/{application-id}/channels/adm | Disables the ADM channel for an application and deletes any existing settings for the channel. |
| DELETE | /v1/apps/{application-id}/channels/apns | Disables the APNs channel for an application and deletes any existing settings for the channel. |
| DELETE | /v1/apps/{application-id}/channels/apns_sandbox | Disables the APNs sandbox channel for an application and deletes any existing settings for the channel. |
| DELETE | /v1/apps/{application-id}/channels/apns_voip | Disables the APNs VoIP channel for an application and deletes any existing settings for the channel. |
| DELETE | /v1/apps/{application-id}/channels/apns_voip_sandbox | Disables the APNs VoIP sandbox channel for an application and deletes any existing settings for the channel. |
| DELETE | /v1/apps/{application-id} | Deletes an application. |
| DELETE | /v1/apps/{application-id}/channels/baidu | Disables the Baidu channel for an application and deletes any existing settings for the channel. |
| DELETE | /v1/apps/{application-id}/campaigns/{campaign-id} | Deletes a campaign from an application. |
| DELETE | /v1/apps/{application-id}/channels/email | Disables the email channel for an application and deletes any existing settings for the channel. |
| DELETE | /v1/apps/{application-id}/endpoints/{endpoint-id} | Deletes an endpoint from an application. |
| DELETE | /v1/apps/{application-id}/eventstream | Deletes the event stream for an application. |
| DELETE | /v1/apps/{application-id}/channels/gcm | Disables the GCM channel for an application and deletes any existing settings for the channel. |
| DELETE | /v1/apps/{application-id}/journeys/{journey-id} | Deletes a journey from an application. |
| DELETE | /v1/apps/{application-id}/segments/{segment-id} | Deletes a segment from an application. |
| DELETE | /v1/apps/{application-id}/channels/sms | Disables the SMS channel for an application and deletes any existing settings for the channel. |
| DELETE | /v1/apps/{application-id}/users/{user-id} | Deletes all the endpoints that are associated with a specific user ID. |
| DELETE | /v1/apps/{application-id}/channels/voice | Disables the voice channel for an application and deletes any existing settings for the channel. |
| GET | /v1/apps/{application-id}/channels/adm | Retrieves information about the status and settings of the ADM channel for an application. |
| GET | /v1/apps/{application-id}/channels/apns | Retrieves information about the status and settings of the APNs channel for an application. |
| GET | /v1/apps/{application-id}/channels/apns_sandbox | Retrieves information about the status and settings of the APNs sandbox channel for an application. |
| GET | /v1/apps/{application-id}/channels/apns_voip | Retrieves information about the status and settings of the APNs VoIP channel for an application. |
| GET | /v1/apps/{application-id}/channels/apns_voip_sandbox | Retrieves information about the status and settings of the APNs VoIP sandbox channel for an application. |
| GET | /v1/apps/{application-id} | Retrieves information about an application. |
| GET | /v1/apps/{application-id}/kpis/daterange/{kpi-name} | Retrieves (queries) pre-aggregated data for a standard metric that applies to an application. |
| GET | /v1/apps/{application-id}/settings | Retrieves information about the settings for an application. |
| GET | /v1/apps | Retrieves information about all the applications that are associated with your Amazon Pinpoint account. |
| GET | /v1/apps/{application-id}/channels/baidu | Retrieves information about the status and settings of the Baidu channel for an application. |
| GET | /v1/apps/{application-id}/campaigns/{campaign-id} | Retrieves information about the status, configuration, and other settings for a campaign. |
| GET | /v1/apps/{application-id}/campaigns/{campaign-id}/activities | Retrieves information about all the activities for a campaign. |
| GET | /v1/apps/{application-id}/campaigns/{campaign-id}/kpis/daterange/{kpi-name} | Retrieves (queries) pre-aggregated data for a standard metric that applies to a campaign. |
| GET | /v1/apps/{application-id}/campaigns/{campaign-id}/versions/{version} | Retrieves information about the status, configuration, and other settings for a specific version of a campaign. |
| GET | /v1/apps/{application-id}/campaigns/{campaign-id}/versions | Retrieves information about the status, configuration, and other settings for all versions of a campaign. |
| GET | /v1/apps/{application-id}/campaigns | Retrieves information about the status, configuration, and other settings for all the campaigns that are associated with an application. |
| GET | /v1/apps/{application-id}/channels | Retrieves information about the history and status of each channel for an application. |
| GET | /v1/apps/{application-id}/channels/email | Retrieves information about the status and settings of the email channel for an application. |
| GET | /v1/apps/{application-id}/endpoints/{endpoint-id} | Retrieves information about the settings and attributes of a specific endpoint for an application. |
| GET | /v1/apps/{application-id}/eventstream | Retrieves information about the event stream settings for an application. |
| GET | /v1/apps/{application-id}/jobs/export/{job-id} | Retrieves information about the status and settings of a specific export job for an application. |
| GET | /v1/apps/{application-id}/jobs/export | Retrieves information about the status and settings of all the export jobs for an application. |
| GET | /v1/apps/{application-id}/channels/gcm | Retrieves information about the status and settings of the GCM channel for an application. |
| GET | /v1/apps/{application-id}/jobs/import/{job-id} | Retrieves information about the status and settings of a specific import job for an application. |
| GET | /v1/apps/{application-id}/jobs/import | Retrieves information about the status and settings of all the import jobs for an application. |
| GET | /v1/apps/{application-id}/endpoints/{endpoint-id}/inappmessages | Retrieves the in-app messages targeted for the provided endpoint ID. |
| GET | /v1/apps/{application-id}/journeys/{journey-id} | Retrieves information about the status, configuration, and other settings for a journey. |
| GET | /v1/apps/{application-id}/journeys/{journey-id}/kpis/daterange/{kpi-name} | Retrieves (queries) pre-aggregated data for a standard engagement metric that applies to a journey. |
| GET | /v1/apps/{application-id}/journeys/{journey-id}/activities/{journey-activity-id}/execution-metrics | Retrieves (queries) pre-aggregated data for a standard execution metric that applies to a journey activity. |
| GET | /v1/apps/{application-id}/journeys/{journey-id}/execution-metrics | Retrieves (queries) pre-aggregated data for a standard execution metric that applies to a journey. |
| GET | /v1/apps/{application-id}/journeys/{journey-id}/runs/{run-id}/activities/{journey-activity-id}/execution-metrics | Retrieves (queries) pre-aggregated data for a standard run execution metric that applies to a journey activity. |
| GET | /v1/apps/{application-id}/journeys/{journey-id}/runs/{run-id}/execution-metrics | Retrieves (queries) pre-aggregated data for a standard run execution metric that applies to a journey. |
| GET | /v1/apps/{application-id}/journeys/{journey-id}/runs | Provides information about the runs of a journey. |
| GET | /v1/apps/{application-id}/segments/{segment-id} | Retrieves information about the configuration, dimension, and other settings for a specific segment that's associated with an application. |
| GET | /v1/apps/{application-id}/segments/{segment-id}/jobs/export | Retrieves information about the status and settings of the export jobs for a segment. |
| GET | /v1/apps/{application-id}/segments/{segment-id}/jobs/import | Retrieves information about the status and settings of the import jobs for a segment. |
| GET | /v1/apps/{application-id}/segments/{segment-id}/versions/{version} | Retrieves information about the configuration, dimension, and other settings for a specific version of a segment that's associated with an application. |
| GET | /v1/apps/{application-id}/segments/{segment-id}/versions | Retrieves information about the configuration, dimension, and other settings for all the versions of a specific segment that's associated with an application. |
| GET | /v1/apps/{application-id}/segments | Retrieves information about the configuration, dimension, and other settings for all the segments that are associated with an application. |
| GET | /v1/apps/{application-id}/channels/sms | Retrieves information about the status and settings of the SMS channel for an application. |
| GET | /v1/apps/{application-id}/users/{user-id} | Retrieves information about all the endpoints that are associated with a specific user ID. |
| GET | /v1/apps/{application-id}/channels/voice | Retrieves information about the status and settings of the voice channel for an application. |
| GET | /v1/apps/{application-id}/journeys | Retrieves information about the status, configuration, and other settings for all the journeys that are associated with an application. |
| POST | /v1/apps/{application-id}/eventstream | Creates a new event stream for an application or updates the settings of an existing event stream for an application. |
| POST | /v1/apps/{application-id}/events | Creates a new event to record for endpoints, or creates or updates endpoint data that existing events are associated with. |
| PUT | /v1/apps/{application-id}/attributes/{attribute-type} | Removes one or more custom attributes, of the same attribute type, from the application. Existing endpoints still have the attributes but Amazon Pinpoint will stop capturing new or changed values for these attributes. |
| POST | /v1/apps/{application-id}/messages | Creates and sends a direct message. |
| POST | /v1/apps/{application-id}/otp | Send an OTP message |
| POST | /v1/apps/{application-id}/users-messages | Creates and sends a message to a list of users. |
| PUT | /v1/apps/{application-id}/channels/adm | Enables the ADM channel for an application or updates the status and settings of the ADM channel for an application. |
| PUT | /v1/apps/{application-id}/channels/apns | Enables the APNs channel for an application or updates the status and settings of the APNs channel for an application. |
| PUT | /v1/apps/{application-id}/channels/apns_sandbox | Enables the APNs sandbox channel for an application or updates the status and settings of the APNs sandbox channel for an application. |
| PUT | /v1/apps/{application-id}/channels/apns_voip | Enables the APNs VoIP channel for an application or updates the status and settings of the APNs VoIP channel for an application. |
| PUT | /v1/apps/{application-id}/channels/apns_voip_sandbox | Enables the APNs VoIP sandbox channel for an application or updates the status and settings of the APNs VoIP sandbox channel for an application. |
| PUT | /v1/apps/{application-id}/settings | Updates the settings for an application. |
| PUT | /v1/apps/{application-id}/channels/baidu | Enables the Baidu channel for an application or updates the status and settings of the Baidu channel for an application. |
| PUT | /v1/apps/{application-id}/campaigns/{campaign-id} | Updates the configuration and other settings for a campaign. |
| PUT | /v1/apps/{application-id}/channels/email | Enables the email channel for an application or updates the status and settings of the email channel for an application. |
| PUT | /v1/apps/{application-id}/endpoints/{endpoint-id} | Creates a new endpoint for an application or updates the settings and attributes of an existing endpoint for an application. You can also use this operation to define custom attributes for an endpoint. If an update includes one or more values for a custom attribute, Amazon Pinpoint replaces (overwrites) any existing values with the new values. |
| PUT | /v1/apps/{application-id}/endpoints | Creates a new batch of endpoints for an application or updates the settings and attributes of a batch of existing endpoints for an application. You can also use this operation to define custom attributes for a batch of endpoints. If an update includes one or more values for a custom attribute, Amazon Pinpoint replaces (overwrites) any existing values with the new values. |
| PUT | /v1/apps/{application-id}/channels/gcm | Enables the GCM channel for an application or updates the status and settings of the GCM channel for an application. |
| PUT | /v1/apps/{application-id}/journeys/{journey-id} | Updates the configuration and other settings for a journey. |
| PUT | /v1/apps/{application-id}/journeys/{journey-id}/state | Cancels (stops) an active journey. |
| PUT | /v1/apps/{application-id}/segments/{segment-id} | Creates a new segment for an application or updates the configuration, dimension, and other settings for an existing segment that's associated with an application. |
| PUT | /v1/apps/{application-id}/channels/sms | Enables the SMS channel for an application or updates the status and settings of the SMS channel for an application. |
| PUT | /v1/apps/{application-id}/channels/voice | Enables the voice channel for an application or updates the status and settings of the voice channel for an application. |
| POST | /v1/apps/{application-id}/verify-otp | Verify an OTP |

### templates
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/templates/{template-name}/email | Creates a message template for messages that are sent through the email channel. |
| POST | /v1/templates/{template-name}/inapp | Creates a new message template for messages using the in-app message channel. |
| POST | /v1/templates/{template-name}/push | Creates a message template for messages that are sent through a push notification channel. |
| POST | /v1/templates/{template-name}/sms | Creates a message template for messages that are sent through the SMS channel. |
| POST | /v1/templates/{template-name}/voice | Creates a message template for messages that are sent through the voice channel. |
| DELETE | /v1/templates/{template-name}/email | Deletes a message template for messages that were sent through the email channel. |
| DELETE | /v1/templates/{template-name}/inapp | Deletes a message template for messages sent using the in-app message channel. |
| DELETE | /v1/templates/{template-name}/push | Deletes a message template for messages that were sent through a push notification channel. |
| DELETE | /v1/templates/{template-name}/sms | Deletes a message template for messages that were sent through the SMS channel. |
| DELETE | /v1/templates/{template-name}/voice | Deletes a message template for messages that were sent through the voice channel. |
| GET | /v1/templates/{template-name}/email | Retrieves the content and settings of a message template for messages that are sent through the email channel. |
| GET | /v1/templates/{template-name}/inapp | Retrieves the content and settings of a message template for messages sent through the in-app channel. |
| GET | /v1/templates/{template-name}/push | Retrieves the content and settings of a message template for messages that are sent through a push notification channel. |
| GET | /v1/templates/{template-name}/sms | Retrieves the content and settings of a message template for messages that are sent through the SMS channel. |
| GET | /v1/templates/{template-name}/voice | Retrieves the content and settings of a message template for messages that are sent through the voice channel. |
| GET | /v1/templates/{template-name}/{template-type}/versions | Retrieves information about all the versions of a specific message template. |
| GET | /v1/templates | Retrieves information about all the message templates that are associated with your Amazon Pinpoint account. |
| PUT | /v1/templates/{template-name}/email | Updates an existing message template for messages that are sent through the email channel. |
| PUT | /v1/templates/{template-name}/inapp | Updates an existing message template for messages sent through the in-app message channel. |
| PUT | /v1/templates/{template-name}/push | Updates an existing message template for messages that are sent through a push notification channel. |
| PUT | /v1/templates/{template-name}/sms | Updates an existing message template for messages that are sent through the SMS channel. |
| PUT | /v1/templates/{template-name}/{template-type}/active-version | Changes the status of a specific version of a message template to active. |
| PUT | /v1/templates/{template-name}/voice | Updates an existing message template for messages that are sent through the voice channel. |

### recommenders
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/recommenders | Creates an Amazon Pinpoint configuration for a recommender model. |
| DELETE | /v1/recommenders/{recommender-id} | Deletes an Amazon Pinpoint configuration for a recommender model. |
| GET | /v1/recommenders/{recommender-id} | Retrieves information about an Amazon Pinpoint configuration for a recommender model. |
| GET | /v1/recommenders | Retrieves information about all the recommender model configurations that are associated with your Amazon Pinpoint account. |
| PUT | /v1/recommenders/{recommender-id} | Updates an Amazon Pinpoint configuration for a recommender model. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/tags/{resource-arn} | Retrieves all the tags (keys and values) that are associated with an application, campaign, message template, or segment. |
| POST | /v1/tags/{resource-arn} | Adds one or more tags (keys and values) to an application, campaign, message template, or segment. |
| DELETE | /v1/tags/{resource-arn} | Removes one or more tags (keys and values) from an application, campaign, message template, or segment. |

### phone
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/phone/number/validate | Retrieves information about a phone number. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a app?" -> POST /v1/apps
- "Create a campaign?" -> POST /v1/apps/{application-id}/campaigns
- "Create a email?" -> POST /v1/templates/{template-name}/email
- "Create a export?" -> POST /v1/apps/{application-id}/jobs/export
- "Create a import?" -> POST /v1/apps/{application-id}/jobs/import
- "Create a inapp?" -> POST /v1/templates/{template-name}/inapp
- "Create a journey?" -> POST /v1/apps/{application-id}/journeys
- "Create a push?" -> POST /v1/templates/{template-name}/push
- "Create a recommender?" -> POST /v1/recommenders
- "Create a segment?" -> POST /v1/apps/{application-id}/segments
- "Create a sm?" -> POST /v1/templates/{template-name}/sms
- "Create a voice?" -> POST /v1/templates/{template-name}/voice
- "Delete a app?" -> DELETE /v1/apps/{application-id}
- "Delete a campaign?" -> DELETE /v1/apps/{application-id}/campaigns/{campaign-id}
- "Delete a endpoint?" -> DELETE /v1/apps/{application-id}/endpoints/{endpoint-id}
- "Delete a journey?" -> DELETE /v1/apps/{application-id}/journeys/{journey-id}
- "Delete a recommender?" -> DELETE /v1/recommenders/{recommender-id}
- "Delete a segment?" -> DELETE /v1/apps/{application-id}/segments/{segment-id}
- "Delete a user?" -> DELETE /v1/apps/{application-id}/users/{user-id}
- "List all adm?" -> GET /v1/apps/{application-id}/channels/adm
- "List all apns?" -> GET /v1/apps/{application-id}/channels/apns
- "List all apns_sandbox?" -> GET /v1/apps/{application-id}/channels/apns_sandbox
- "List all apns_voip?" -> GET /v1/apps/{application-id}/channels/apns_voip
- "List all apns_voip_sandbox?" -> GET /v1/apps/{application-id}/channels/apns_voip_sandbox
- "Get app details?" -> GET /v1/apps/{application-id}
- "Get daterange details?" -> GET /v1/apps/{application-id}/kpis/daterange/{kpi-name}
- "List all settings?" -> GET /v1/apps/{application-id}/settings
- "List all apps?" -> GET /v1/apps
- "List all baidu?" -> GET /v1/apps/{application-id}/channels/baidu
- "Get campaign details?" -> GET /v1/apps/{application-id}/campaigns/{campaign-id}
- "List all activities?" -> GET /v1/apps/{application-id}/campaigns/{campaign-id}/activities
- "Get daterange details?" -> GET /v1/apps/{application-id}/campaigns/{campaign-id}/kpis/daterange/{kpi-name}
- "Get version details?" -> GET /v1/apps/{application-id}/campaigns/{campaign-id}/versions/{version}
- "List all versions?" -> GET /v1/apps/{application-id}/campaigns/{campaign-id}/versions
- "List all campaigns?" -> GET /v1/apps/{application-id}/campaigns
- "List all channels?" -> GET /v1/apps/{application-id}/channels
- "List all email?" -> GET /v1/apps/{application-id}/channels/email
- "List all email?" -> GET /v1/templates/{template-name}/email
- "Get endpoint details?" -> GET /v1/apps/{application-id}/endpoints/{endpoint-id}
- "List all eventstream?" -> GET /v1/apps/{application-id}/eventstream
- "Get export details?" -> GET /v1/apps/{application-id}/jobs/export/{job-id}
- "List all export?" -> GET /v1/apps/{application-id}/jobs/export
- "List all gcm?" -> GET /v1/apps/{application-id}/channels/gcm
- "Get import details?" -> GET /v1/apps/{application-id}/jobs/import/{job-id}
- "List all import?" -> GET /v1/apps/{application-id}/jobs/import
- "List all inappmessages?" -> GET /v1/apps/{application-id}/endpoints/{endpoint-id}/inappmessages
- "List all inapp?" -> GET /v1/templates/{template-name}/inapp
- "Get journey details?" -> GET /v1/apps/{application-id}/journeys/{journey-id}
- "Get daterange details?" -> GET /v1/apps/{application-id}/journeys/{journey-id}/kpis/daterange/{kpi-name}
- "List all execution-metrics?" -> GET /v1/apps/{application-id}/journeys/{journey-id}/activities/{journey-activity-id}/execution-metrics
- "List all execution-metrics?" -> GET /v1/apps/{application-id}/journeys/{journey-id}/execution-metrics
- "List all execution-metrics?" -> GET /v1/apps/{application-id}/journeys/{journey-id}/runs/{run-id}/activities/{journey-activity-id}/execution-metrics
- "List all execution-metrics?" -> GET /v1/apps/{application-id}/journeys/{journey-id}/runs/{run-id}/execution-metrics
- "List all runs?" -> GET /v1/apps/{application-id}/journeys/{journey-id}/runs
- "List all push?" -> GET /v1/templates/{template-name}/push
- "Get recommender details?" -> GET /v1/recommenders/{recommender-id}
- "List all recommenders?" -> GET /v1/recommenders
- "Get segment details?" -> GET /v1/apps/{application-id}/segments/{segment-id}
- "List all export?" -> GET /v1/apps/{application-id}/segments/{segment-id}/jobs/export
- "List all import?" -> GET /v1/apps/{application-id}/segments/{segment-id}/jobs/import
- "Get version details?" -> GET /v1/apps/{application-id}/segments/{segment-id}/versions/{version}
- "List all versions?" -> GET /v1/apps/{application-id}/segments/{segment-id}/versions
- "List all segments?" -> GET /v1/apps/{application-id}/segments
- "List all sms?" -> GET /v1/apps/{application-id}/channels/sms
- "List all sms?" -> GET /v1/templates/{template-name}/sms
- "Get user details?" -> GET /v1/apps/{application-id}/users/{user-id}
- "List all voice?" -> GET /v1/apps/{application-id}/channels/voice
- "List all voice?" -> GET /v1/templates/{template-name}/voice
- "List all journeys?" -> GET /v1/apps/{application-id}/journeys
- "Get tag details?" -> GET /v1/tags/{resource-arn}
- "List all versions?" -> GET /v1/templates/{template-name}/{template-type}/versions
- "List all templates?" -> GET /v1/templates
- "Create a validate?" -> POST /v1/phone/number/validate
- "Create a eventstream?" -> POST /v1/apps/{application-id}/eventstream
- "Create a event?" -> POST /v1/apps/{application-id}/events
- "Update a attribute?" -> PUT /v1/apps/{application-id}/attributes/{attribute-type}
- "Create a message?" -> POST /v1/apps/{application-id}/messages
- "Create a otp?" -> POST /v1/apps/{application-id}/otp
- "Create a users-message?" -> POST /v1/apps/{application-id}/users-messages
- "Delete a tag?" -> DELETE /v1/tags/{resource-arn}
- "Update a campaign?" -> PUT /v1/apps/{application-id}/campaigns/{campaign-id}
- "Update a endpoint?" -> PUT /v1/apps/{application-id}/endpoints/{endpoint-id}
- "Update a journey?" -> PUT /v1/apps/{application-id}/journeys/{journey-id}
- "Update a recommender?" -> PUT /v1/recommenders/{recommender-id}
- "Update a segment?" -> PUT /v1/apps/{application-id}/segments/{segment-id}
- "Create a verify-otp?" -> POST /v1/apps/{application-id}/verify-otp
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
