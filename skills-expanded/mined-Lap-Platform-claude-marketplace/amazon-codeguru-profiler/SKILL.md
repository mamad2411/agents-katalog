---
name: amazon-codeguru-profiler
description: "Amazon CodeGuru Profiler API skill. Use when working with Amazon CodeGuru Profiler for profilingGroups, internal, tags. Covers 23 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon CodeGuru Profiler
API version: 2019-07-18

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /internal/findingsReports -- verify access
3. POST /profilingGroups/{profilingGroupName}/notificationConfiguration -- create first notificationConfiguration

## Endpoints

23 endpoints across 3 groups. See references/api-spec.lap for full details.

### profilingGroups
| Method | Path | Description |
|--------|------|-------------|
| POST | /profilingGroups/{profilingGroupName}/notificationConfiguration | Add up to 2 anomaly notifications channels for a profiling group. |
| POST | /profilingGroups/{profilingGroupName}/frames/-/metrics | Returns the time series of values for a requested list of frame metrics from a time period. |
| POST | /profilingGroups/{profilingGroupName}/configureAgent | Used by profiler agents to report their current state and to receive remote configuration updates. For example, ConfigureAgent can be used to tell an agent whether to profile or not and for how long to return profiling data. |
| POST | /profilingGroups | Creates a profiling group. |
| DELETE | /profilingGroups/{profilingGroupName} | Deletes a profiling group. |
| GET | /profilingGroups/{profilingGroupName} | Returns a  ProfilingGroupDescription  object that contains information about the requested profiling group. |
| GET | /profilingGroups/{profilingGroupName}/notificationConfiguration | Get the current configuration for anomaly notifications for a profiling group. |
| GET | /profilingGroups/{profilingGroupName}/policy | Returns the JSON-formatted resource-based policy on a profiling group. |
| GET | /profilingGroups/{profilingGroupName}/profile | Gets the aggregated profile of a profiling group for a specified time range. Amazon CodeGuru Profiler collects posted agent profiles for a profiling group into aggregated profiles.   &lt;note&gt; &lt;p&gt; Because aggregated profiles expire over time &lt;code&gt;GetProfile&lt;/code&gt; is not idempotent. &lt;/p&gt; &lt;/note&gt; &lt;p&gt; Specify the time range for the requested aggregated profile using 1 or 2 of the following parameters: &lt;code&gt;startTime&lt;/code&gt;, &lt;code&gt;endTime&lt;/code&gt;, &lt;code&gt;period&lt;/code&gt;. The maximum time range allowed is 7 days. If you specify all 3 parameters, an exception is thrown. If you specify only &lt;code&gt;period&lt;/code&gt;, the latest aggregated profile is returned. &lt;/p&gt; &lt;p&gt; Aggregated profiles are available with aggregation periods of 5 minutes, 1 hour, and 1 day, aligned to UTC. The aggregation period of an aggregated profile determines how long it is retained. For more information, see &lt;a href=&quot;https://docs.aws.amazon.com/codeguru/latest/profiler-api/API_AggregatedProfileTime.html&quot;&gt; &lt;code&gt;AggregatedProfileTime&lt;/code&gt; &lt;/a&gt;. The aggregated profile's aggregation period determines how long it is retained by CodeGuru Profiler. &lt;/p&gt; &lt;ul&gt; &lt;li&gt; &lt;p&gt; If the aggregation period is 5 minutes, the aggregated profile is retained for 15 days. &lt;/p&gt; &lt;/li&gt; &lt;li&gt; &lt;p&gt; If the aggregation period is 1 hour, the aggregated profile is retained for 60 days. &lt;/p&gt; &lt;/li&gt; &lt;li&gt; &lt;p&gt; If the aggregation period is 1 day, the aggregated profile is retained for 3 years. &lt;/p&gt; &lt;/li&gt; &lt;/ul&gt; &lt;p&gt;There are two use cases for calling &lt;code&gt;GetProfile&lt;/code&gt;.&lt;/p&gt; &lt;ol&gt; &lt;li&gt; &lt;p&gt; If you want to return an aggregated profile that already exists, use &lt;a href=&quot;https://docs.aws.amazon.com/codeguru/latest/profiler-api/API_ListProfileTimes.html&quot;&gt; &lt;code&gt;ListProfileTimes&lt;/code&gt; &lt;/a&gt; to view the time ranges of existing aggregated profiles. Use them in a &lt;code&gt;GetProfile&lt;/code&gt; request to return a specific, existing aggregated profile. &lt;/p&gt; &lt;/li&gt; &lt;li&gt; &lt;p&gt; If you want to return an aggregated profile for a time range that doesn't align with an existing aggregated profile, then CodeGuru Profiler makes a best effort to combine existing aggregated profiles from the requested time range and return them as one aggregated profile. &lt;/p&gt; &lt;p&gt; If aggregated profiles do not exist for the full time range requested, then aggregated profiles for a smaller time range are returned. For example, if the requested time range is from 00:00 to 00:20, and the existing aggregated profiles are from 00:15 and 00:25, then the aggregated profiles from 00:15 to 00:20 are returned. &lt;/p&gt; &lt;/li&gt; &lt;/ol&gt; |
| GET | /profilingGroups/{profilingGroupName}/profileTimes | Lists the start times of the available aggregated profiles of a profiling group for an aggregation period within the specified time range. |
| GET | /profilingGroups | Returns a list of profiling groups. The profiling groups are returned as  ProfilingGroupDescription  objects. |
| POST | /profilingGroups/{profilingGroupName}/agentProfile | Submits profiling data to an aggregated profile of a profiling group. To get an aggregated profile that is created with this profiling data, use  GetProfile . |
| PUT | /profilingGroups/{profilingGroupName}/policy/{actionGroup} | Adds permissions to a profiling group's resource-based policy that are provided using an action group. If a profiling group doesn't have a resource-based policy, one is created for it using the permissions in the action group and the roles and users in the principals parameter.   &lt;p&gt; The one supported action group that can be added is &lt;code&gt;agentPermission&lt;/code&gt; which grants &lt;code&gt;ConfigureAgent&lt;/code&gt; and &lt;code&gt;PostAgent&lt;/code&gt; permissions. For more information, see &lt;a href=&quot;https://docs.aws.amazon.com/codeguru/latest/profiler-ug/resource-based-policies.html&quot;&gt;Resource-based policies in CodeGuru Profiler&lt;/a&gt; in the &lt;i&gt;Amazon CodeGuru Profiler User Guide&lt;/i&gt;, &lt;a href=&quot;https://docs.aws.amazon.com/codeguru/latest/profiler-api/API_ConfigureAgent.html&quot;&gt; &lt;code&gt;ConfigureAgent&lt;/code&gt; &lt;/a&gt;, and &lt;a href=&quot;https://docs.aws.amazon.com/codeguru/latest/profiler-api/API_PostAgentProfile.html&quot;&gt; &lt;code&gt;PostAgentProfile&lt;/code&gt; &lt;/a&gt;. &lt;/p&gt; &lt;p&gt; The first time you call &lt;code&gt;PutPermission&lt;/code&gt; on a profiling group, do not specify a &lt;code&gt;revisionId&lt;/code&gt; because it doesn't have a resource-based policy. Subsequent calls must provide a &lt;code&gt;revisionId&lt;/code&gt; to specify which revision of the resource-based policy to add the permissions to. &lt;/p&gt; &lt;p&gt; The response contains the profiling group's JSON-formatted resource policy. &lt;/p&gt; |
| DELETE | /profilingGroups/{profilingGroupName}/notificationConfiguration/{channelId} | Remove one anomaly notifications channel for a profiling group. |
| DELETE | /profilingGroups/{profilingGroupName}/policy/{actionGroup} | Removes permissions from a profiling group's resource-based policy that are provided using an action group. The one supported action group that can be removed is agentPermission which grants ConfigureAgent and PostAgent permissions. For more information, see Resource-based policies in CodeGuru Profiler in the Amazon CodeGuru Profiler User Guide,  ConfigureAgent , and  PostAgentProfile . |
| PUT | /profilingGroups/{profilingGroupName} | Updates a profiling group. |

### internal
| Method | Path | Description |
|--------|------|-------------|
| GET | /internal/findingsReports | Returns a list of  FindingsReportSummary  objects that contain analysis results for all profiling groups in your AWS account. |
| GET | /internal/profilingGroups/{profilingGroupName}/recommendations | Returns a list of  Recommendation  objects that contain recommendations for a profiling group for a given time period. A list of  Anomaly  objects that contains details about anomalies detected in the profiling group for the same time period is also returned. |
| GET | /internal/profilingGroups/{profilingGroupName}/findingsReports | List the available reports for a given profiling group and time range. |
| POST | /internal/profilingGroups/{profilingGroupName}/anomalies/{anomalyInstanceId}/feedback | Sends feedback to CodeGuru Profiler about whether the anomaly detected by the analysis is useful or not. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | Returns a list of the tags that are assigned to a specified resource. |
| POST | /tags/{resourceArn} | Use to assign one or more tags to a resource. |
| DELETE | /tags/{resourceArn} | Use to remove one or more tags from a resource. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a notificationConfiguration?" -> POST /profilingGroups/{profilingGroupName}/notificationConfiguration
- "Create a metric?" -> POST /profilingGroups/{profilingGroupName}/frames/-/metrics
- "Create a configureAgent?" -> POST /profilingGroups/{profilingGroupName}/configureAgent
- "Create a profilingGroup?" -> POST /profilingGroups
- "Delete a profilingGroup?" -> DELETE /profilingGroups/{profilingGroupName}
- "Get profilingGroup details?" -> GET /profilingGroups/{profilingGroupName}
- "List all findingsReports?" -> GET /internal/findingsReports
- "List all notificationConfiguration?" -> GET /profilingGroups/{profilingGroupName}/notificationConfiguration
- "List all policy?" -> GET /profilingGroups/{profilingGroupName}/policy
- "List all profile?" -> GET /profilingGroups/{profilingGroupName}/profile
- "List all recommendations?" -> GET /internal/profilingGroups/{profilingGroupName}/recommendations
- "List all findingsReports?" -> GET /internal/profilingGroups/{profilingGroupName}/findingsReports
- "List all profileTimes?" -> GET /profilingGroups/{profilingGroupName}/profileTimes
- "List all profilingGroups?" -> GET /profilingGroups
- "Get tag details?" -> GET /tags/{resourceArn}
- "Create a agentProfile?" -> POST /profilingGroups/{profilingGroupName}/agentProfile
- "Update a policy?" -> PUT /profilingGroups/{profilingGroupName}/policy/{actionGroup}
- "Delete a notificationConfiguration?" -> DELETE /profilingGroups/{profilingGroupName}/notificationConfiguration/{channelId}
- "Delete a policy?" -> DELETE /profilingGroups/{profilingGroupName}/policy/{actionGroup}
- "Create a feedback?" -> POST /internal/profilingGroups/{profilingGroupName}/anomalies/{anomalyInstanceId}/feedback
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "Update a profilingGroup?" -> PUT /profilingGroups/{profilingGroupName}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
