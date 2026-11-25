---
name: aws-performance-insights
description: "AWS Performance Insights API skill. Use when working with AWS Performance Insights for root. Covers 13 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Performance Insights
API version: 2018-02-27

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

13 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Creates a new performance analysis report for a specific time period for the DB instance. |
| POST | / | Deletes a performance analysis report. |
| POST | / | For a specific time period, retrieve the top N dimension keys for a metric.   Each response element returns a maximum of 500 bytes. For larger elements, such as SQL statements, only the first 500 bytes are returned. |
| POST | / | Get the attributes of the specified dimension group for a DB instance or data source. For example, if you specify a SQL ID, GetDimensionKeyDetails retrieves the full text of the dimension db.sql.statement associated with this ID. This operation is useful because GetResourceMetrics and DescribeDimensionKeys don't support retrieval of large SQL statement text. |
| POST | / | Retrieves the report including the report ID, status, time details, and the insights with recommendations. The report status can be RUNNING, SUCCEEDED, or FAILED. The insights include the description and recommendation fields. |
| POST | / | Retrieve the metadata for different features. For example, the metadata might indicate that a feature is turned on or off on a specific DB instance. |
| POST | / | Retrieve Performance Insights metrics for a set of data sources over a time period. You can provide specific dimension groups and dimensions, and provide filtering criteria for each group. You must specify an aggregate function for each metric.  Each response element returns a maximum of 500 bytes. For larger elements, such as SQL statements, only the first 500 bytes are returned. |
| POST | / | Retrieve the dimensions that can be queried for each specified metric type on a specified DB instance. |
| POST | / | Retrieve metrics of the specified types that can be queried for a specified DB instance. |
| POST | / | Lists all the analysis reports created for the DB instance. The reports are sorted based on the start time of each report. |
| POST | / | Retrieves all the metadata tags associated with Amazon RDS Performance Insights resource. |
| POST | / | Adds metadata tags to the Amazon RDS Performance Insights resource. |
| POST | / | Deletes the metadata tags from the Amazon RDS Performance Insights resource. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
