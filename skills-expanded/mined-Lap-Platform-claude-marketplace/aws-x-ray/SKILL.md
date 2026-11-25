---
name: aws-x-ray
description: "AWS X-Ray API skill. Use when working with AWS X-Ray for Traces, CreateGroup, CreateSamplingRule. Covers 30 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS X-Ray
API version: 2016-04-12

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST /Traces -- create first Traces

## Endpoints

30 endpoints across 30 groups. See references/api-spec.lap for full details.

### Traces
| Method | Path | Description |
|--------|------|-------------|
| POST | /Traces | Retrieves a list of traces specified by ID. Each trace is a collection of segment documents that originates from a single request. Use GetTraceSummaries to get a list of trace IDs. |

### CreateGroup
| Method | Path | Description |
|--------|------|-------------|
| POST | /CreateGroup | Creates a group resource with a name and a filter expression. |

### CreateSamplingRule
| Method | Path | Description |
|--------|------|-------------|
| POST | /CreateSamplingRule | Creates a rule to control sampling behavior for instrumented applications. Services retrieve rules with GetSamplingRules, and evaluate each rule in ascending order of priority for each request. If a rule matches, the service records a trace, borrowing it from the reservoir size. After 10 seconds, the service reports back to X-Ray with GetSamplingTargets to get updated versions of each in-use rule. The updated rule contains a trace quota that the service can use instead of borrowing from the reservoir. |

### DeleteGroup
| Method | Path | Description |
|--------|------|-------------|
| POST | /DeleteGroup | Deletes a group resource. |

### DeleteResourcePolicy
| Method | Path | Description |
|--------|------|-------------|
| POST | /DeleteResourcePolicy | Deletes a resource policy from the target Amazon Web Services account. |

### DeleteSamplingRule
| Method | Path | Description |
|--------|------|-------------|
| POST | /DeleteSamplingRule | Deletes a sampling rule. |

### EncryptionConfig
| Method | Path | Description |
|--------|------|-------------|
| POST | /EncryptionConfig | Retrieves the current encryption configuration for X-Ray data. |

### GetGroup
| Method | Path | Description |
|--------|------|-------------|
| POST | /GetGroup | Retrieves group resource details. |

### Groups
| Method | Path | Description |
|--------|------|-------------|
| POST | /Groups | Retrieves all active group details. |

### Insight
| Method | Path | Description |
|--------|------|-------------|
| POST | /Insight | Retrieves the summary information of an insight. This includes impact to clients and root cause services, the top anomalous services, the category, the state of the insight, and the start and end time of the insight. |

### InsightEvents
| Method | Path | Description |
|--------|------|-------------|
| POST | /InsightEvents | X-Ray reevaluates insights periodically until they're resolved, and records each intermediate state as an event. You can review an insight's events in the Impact Timeline on the Inspect page in the X-Ray console. |

### InsightImpactGraph
| Method | Path | Description |
|--------|------|-------------|
| POST | /InsightImpactGraph | Retrieves a service graph structure filtered by the specified insight. The service graph is limited to only structural information. For a complete service graph, use this API with the GetServiceGraph API. |

### InsightSummaries
| Method | Path | Description |
|--------|------|-------------|
| POST | /InsightSummaries | Retrieves the summaries of all insights in the specified group matching the provided filter values. |

### GetSamplingRules
| Method | Path | Description |
|--------|------|-------------|
| POST | /GetSamplingRules | Retrieves all sampling rules. |

### SamplingStatisticSummaries
| Method | Path | Description |
|--------|------|-------------|
| POST | /SamplingStatisticSummaries | Retrieves information about recent sampling results for all sampling rules. |

### SamplingTargets
| Method | Path | Description |
|--------|------|-------------|
| POST | /SamplingTargets | Requests a sampling quota for rules that the service is using to sample requests. |

### ServiceGraph
| Method | Path | Description |
|--------|------|-------------|
| POST | /ServiceGraph | Retrieves a document that describes services that process incoming requests, and downstream services that they call as a result. Root services process incoming requests and make calls to downstream services. Root services are applications that use the Amazon Web Services X-Ray SDK. Downstream services can be other applications, Amazon Web Services resources, HTTP web APIs, or SQL databases. |

### TimeSeriesServiceStatistics
| Method | Path | Description |
|--------|------|-------------|
| POST | /TimeSeriesServiceStatistics | Get an aggregation of service statistics defined by a specific time range. |

### TraceGraph
| Method | Path | Description |
|--------|------|-------------|
| POST | /TraceGraph | Retrieves a service graph for one or more specific trace IDs. |

### TraceSummaries
| Method | Path | Description |
|--------|------|-------------|
| POST | /TraceSummaries | Retrieves IDs and annotations for traces available for a specified time frame using an optional filter. To get the full traces, pass the trace IDs to BatchGetTraces. A filter expression can target traced requests that hit specific service nodes or edges, have errors, or come from a known user. For example, the following filter expression targets traces that pass through api.example.com:  service("api.example.com")  This filter expression finds traces that have an annotation named account with the value 12345:  annotation.account = "12345"  For a full list of indexed fields and keywords that you can use in filter expressions, see Using Filter Expressions in the Amazon Web Services X-Ray Developer Guide. |

### ListResourcePolicies
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListResourcePolicies | Returns the list of resource policies in the target Amazon Web Services account. |

### ListTagsForResource
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListTagsForResource | Returns a list of tags that are applied to the specified Amazon Web Services X-Ray group or sampling rule. |

### PutEncryptionConfig
| Method | Path | Description |
|--------|------|-------------|
| POST | /PutEncryptionConfig | Updates the encryption configuration for X-Ray data. |

### PutResourcePolicy
| Method | Path | Description |
|--------|------|-------------|
| POST | /PutResourcePolicy | Sets the resource policy to grant one or more Amazon Web Services services and accounts permissions to access X-Ray. Each resource policy will be associated with a specific Amazon Web Services account. Each Amazon Web Services account can have a maximum of 5 resource policies, and each policy name must be unique within that account. The maximum size of each resource policy is 5KB. |

### TelemetryRecords
| Method | Path | Description |
|--------|------|-------------|
| POST | /TelemetryRecords | Used by the Amazon Web Services X-Ray daemon to upload telemetry. |

### TraceSegments
| Method | Path | Description |
|--------|------|-------------|
| POST | /TraceSegments | Uploads segment documents to Amazon Web Services X-Ray. The X-Ray SDK generates segment documents and sends them to the X-Ray daemon, which uploads them in batches. A segment document can be a completed segment, an in-progress segment, or an array of subsegments. Segments must include the following fields. For the full segment document schema, see Amazon Web Services X-Ray Segment Documents in the Amazon Web Services X-Ray Developer Guide.  Required segment document fields     name - The name of the service that handled the request.    id - A 64-bit identifier for the segment, unique among segments in the same trace, in 16 hexadecimal digits.    trace_id - A unique identifier that connects all segments and subsegments originating from a single client request.    start_time - Time the segment or subsegment was created, in floating point seconds in epoch time, accurate to milliseconds. For example, 1480615200.010 or 1.480615200010E9.    end_time - Time the segment or subsegment was closed. For example, 1480615200.090 or 1.480615200090E9. Specify either an end_time or in_progress.    in_progress - Set to true instead of specifying an end_time to record that a segment has been started, but is not complete. Send an in-progress segment when your application receives a request that will take a long time to serve, to trace that the request was received. When the response is sent, send the complete segment to overwrite the in-progress segment.   A trace_id consists of three numbers separated by hyphens. For example, 1-58406520-a006649127e371903a2de979. This includes:  Trace ID Format    The version number, for instance, 1.   The time of the original request, in Unix epoch time, in 8 hexadecimal digits. For example, 10:00AM December 2nd, 2016 PST in epoch time is 1480615200 seconds, or 58406520 in hexadecimal.   A 96-bit identifier for the trace, globally unique, in 24 hexadecimal digits. |

### TagResource
| Method | Path | Description |
|--------|------|-------------|
| POST | /TagResource | Applies tags to an existing Amazon Web Services X-Ray group or sampling rule. |

### UntagResource
| Method | Path | Description |
|--------|------|-------------|
| POST | /UntagResource | Removes tags from an Amazon Web Services X-Ray group or sampling rule. You cannot edit or delete system tags (those with an aws: prefix). |

### UpdateGroup
| Method | Path | Description |
|--------|------|-------------|
| POST | /UpdateGroup | Updates a group resource. |

### UpdateSamplingRule
| Method | Path | Description |
|--------|------|-------------|
| POST | /UpdateSamplingRule | Modifies a sampling rule's configuration. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a Trace?" -> POST /Traces
- "Create a CreateGroup?" -> POST /CreateGroup
- "Create a CreateSamplingRule?" -> POST /CreateSamplingRule
- "Create a DeleteGroup?" -> POST /DeleteGroup
- "Create a DeleteResourcePolicy?" -> POST /DeleteResourcePolicy
- "Create a DeleteSamplingRule?" -> POST /DeleteSamplingRule
- "Create a EncryptionConfig?" -> POST /EncryptionConfig
- "Create a GetGroup?" -> POST /GetGroup
- "Create a Group?" -> POST /Groups
- "Create a Insight?" -> POST /Insight
- "Create a InsightEvent?" -> POST /InsightEvents
- "Create a InsightImpactGraph?" -> POST /InsightImpactGraph
- "Create a InsightSummary?" -> POST /InsightSummaries
- "Create a GetSamplingRule?" -> POST /GetSamplingRules
- "Create a SamplingStatisticSummary?" -> POST /SamplingStatisticSummaries
- "Create a SamplingTarget?" -> POST /SamplingTargets
- "Create a ServiceGraph?" -> POST /ServiceGraph
- "Create a TimeSeriesServiceStatistic?" -> POST /TimeSeriesServiceStatistics
- "Create a TraceGraph?" -> POST /TraceGraph
- "Create a TraceSummary?" -> POST /TraceSummaries
- "Create a ListResourcePolicy?" -> POST /ListResourcePolicies
- "Create a ListTagsForResource?" -> POST /ListTagsForResource
- "Create a PutEncryptionConfig?" -> POST /PutEncryptionConfig
- "Create a PutResourcePolicy?" -> POST /PutResourcePolicy
- "Create a TelemetryRecord?" -> POST /TelemetryRecords
- "Create a TraceSegment?" -> POST /TraceSegments
- "Create a TagResource?" -> POST /TagResource
- "Create a UntagResource?" -> POST /UntagResource
- "Create a UpdateGroup?" -> POST /UpdateGroup
- "Create a UpdateSamplingRule?" -> POST /UpdateSamplingRule
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
