---
name: amazon-timestream-query
description: "Amazon Timestream Query API skill. Use when working with Amazon Timestream Query for root. Covers 15 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Timestream Query
API version: 2018-11-01

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

15 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Cancels a query that has been issued. Cancellation is provided only if the query has not completed running before the cancellation request was issued. Because cancellation is an idempotent operation, subsequent cancellation requests will return a CancellationMessage, indicating that the query has already been canceled. See code sample for details. |
| POST | / | Create a scheduled query that will be run on your behalf at the configured schedule. Timestream assumes the execution role provided as part of the ScheduledQueryExecutionRoleArn parameter to run the query. You can use the NotificationConfiguration parameter to configure notification for your scheduled query operations. |
| POST | / | Deletes a given scheduled query. This is an irreversible operation. |
| POST | / | Describes the settings for your account that include the query pricing model and the configured maximum TCUs the service can use for your query workload. You're charged only for the duration of compute units used for your workloads. |
| POST | / | DescribeEndpoints returns a list of available endpoints to make Timestream API calls against. This API is available through both Write and Query. Because the Timestream SDKs are designed to transparently work with the service’s architecture, including the management and mapping of the service endpoints, it is not recommended that you use this API unless:   You are using VPC endpoints (Amazon Web Services PrivateLink) with Timestream     Your application uses a programming language that does not yet have SDK support   You require better control over the client-side implementation   For detailed information on how and when to use and implement DescribeEndpoints, see The Endpoint Discovery Pattern. |
| POST | / | Provides detailed information about a scheduled query. |
| POST | / | You can use this API to run a scheduled query manually. |
| POST | / | Gets a list of all scheduled queries in the caller's Amazon account and Region. ListScheduledQueries is eventually consistent. |
| POST | / | List all tags on a Timestream query resource. |
| POST | / | A synchronous operation that allows you to submit a query with parameters to be stored by Timestream for later running. Timestream only supports using this operation with ValidateOnly set to true. |
| POST | / | Query is a synchronous operation that enables you to run a query against your Amazon Timestream data. Query will time out after 60 seconds. You must update the default timeout in the SDK to support a timeout of 60 seconds. See the code sample for details.  Your query request will fail in the following cases:    If you submit a Query request with the same client token outside of the 5-minute idempotency window.     If you submit a Query request with the same client token, but change other parameters, within the 5-minute idempotency window.     If the size of the row (including the query metadata) exceeds 1 MB, then the query will fail with the following error message:   Query aborted as max page response size has been exceeded by the output result row     If the IAM principal of the query initiator and the result reader are not the same and/or the query initiator and the result reader do not have the same query string in the query requests, the query will fail with an Invalid pagination token error. |
| POST | / | Associate a set of tags with a Timestream resource. You can then activate these user-defined tags so that they appear on the Billing and Cost Management console for cost allocation tracking. |
| POST | / | Removes the association of tags from a Timestream query resource. |
| POST | / | Transitions your account to use TCUs for query pricing and modifies the maximum query compute units that you've configured. If you reduce the value of MaxQueryTCU to a desired configuration, the new value can take up to 24 hours to be effective.  After you've transitioned your account to use TCUs for query pricing, you can't transition to using bytes scanned for query pricing. |
| POST | / | Update a scheduled query. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
