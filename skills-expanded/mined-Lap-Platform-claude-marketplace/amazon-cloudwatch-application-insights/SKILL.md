---
name: amazon-cloudwatch-application-insights
description: "Amazon CloudWatch Application Insights API skill. Use when working with Amazon CloudWatch Application Insights for root. Covers 33 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon CloudWatch Application Insights
API version: 2018-11-25

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

33 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Adds a workload to a component. Each component can have at most five workloads. |
| POST | / | Adds an application that is created from a resource group. |
| POST | / | Creates a custom component by grouping similar standalone instances to monitor. |
| POST | / | Adds an log pattern to a LogPatternSet. |
| POST | / | Removes the specified application from monitoring. Does not delete the application. |
| POST | / | Ungroups a custom component. When you ungroup custom components, all applicable monitors that are set up for the component are removed and the instances revert to their standalone status. |
| POST | / | Removes the specified log pattern from a LogPatternSet. |
| POST | / | Describes the application. |
| POST | / | Describes a component and lists the resources that are grouped together in a component. |
| POST | / | Describes the monitoring configuration of the component. |
| POST | / | Describes the recommended monitoring configuration of the component. |
| POST | / | Describe a specific log pattern from a LogPatternSet. |
| POST | / | Describes an anomaly or error with the application. |
| POST | / | Describes an application problem. |
| POST | / | Describes the anomalies or errors associated with the problem. |
| POST | / | Describes a workload and its configuration. |
| POST | / | Lists the IDs of the applications that you are monitoring. |
| POST | / | Lists the auto-grouped, standalone, and custom components of the application. |
| POST | / | Lists the INFO, WARN, and ERROR events for periodic configuration updates performed by Application Insights. Examples of events represented are:    INFO: creating a new alarm or updating an alarm threshold.   WARN: alarm not created due to insufficient data points used to predict thresholds.   ERROR: alarm not created due to permission errors or exceeding quotas. |
| POST | / | Lists the log pattern sets in the specific application. |
| POST | / | Lists the log patterns in the specific log LogPatternSet. |
| POST | / | Lists the problems with your application. |
| POST | / | Retrieve a list of the tags (keys and values) that are associated with a specified application. A tag is a label that you optionally define and associate with an application. Each tag consists of a required tag key and an optional associated tag value. A tag key is a general label that acts as a category for more specific tag values. A tag value acts as a descriptor within a tag key. |
| POST | / | Lists the workloads that are configured on a given component. |
| POST | / | Remove workload from a component. |
| POST | / | Add one or more tags (keys and values) to a specified application. A tag is a label that you optionally define and associate with an application. Tags can help you categorize and manage application in different ways, such as by purpose, owner, environment, or other criteria.  Each tag consists of a required tag key and an associated tag value, both of which you define. A tag key is a general label that acts as a category for more specific tag values. A tag value acts as a descriptor within a tag key. |
| POST | / | Remove one or more tags (keys and values) from a specified application. |
| POST | / | Updates the application. |
| POST | / | Updates the custom component name and/or the list of resources that make up the component. |
| POST | / | Updates the monitoring configurations for the component. The configuration input parameter is an escaped JSON of the configuration and should match the schema of what is returned by DescribeComponentConfigurationRecommendation. |
| POST | / | Adds a log pattern to a LogPatternSet. |
| POST | / | Updates the visibility of the problem or specifies the problem as RESOLVED. |
| POST | / | Adds a workload to a component. Each component can have at most five workloads. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
