---
name: amazon-cognito-sync
description: "Amazon Cognito Sync API skill. Use when working with Amazon Cognito Sync for identitypools. Covers 17 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Cognito Sync
API version: 2014-06-30

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /identitypools -- verify access
3. POST /identitypools/{IdentityPoolId}/bulkpublish -- create first bulkpublish

## Endpoints

17 endpoints across 1 groups. See references/api-spec.lap for full details.

### identitypools
| Method | Path | Description |
|--------|------|-------------|
| POST | /identitypools/{IdentityPoolId}/bulkpublish | Initiates a bulk publish of all existing datasets for an Identity Pool to the configured stream. Customers are limited to one successful bulk publish per 24 hours. Bulk publish is an asynchronous request, customers can see the status of the request via the GetBulkPublishDetails operation.This API can only be called with developer credentials. You cannot call this API with the temporary user credentials provided by Cognito Identity. |
| DELETE | /identitypools/{IdentityPoolId}/identities/{IdentityId}/datasets/{DatasetName} | Deletes the specific dataset. The dataset will be deleted permanently, and the action can't be undone. Datasets that this dataset was merged with will no longer report the merge. Any subsequent operation on this dataset will result in a ResourceNotFoundException. This API can be called with temporary user credentials provided by Cognito Identity or with developer credentials. |
| GET | /identitypools/{IdentityPoolId}/identities/{IdentityId}/datasets/{DatasetName} | Gets meta data about a dataset by identity and dataset name. With Amazon Cognito Sync, each identity has access only to its own data. Thus, the credentials used to make this API call need to have access to the identity data. This API can be called with temporary user credentials provided by Cognito Identity or with developer credentials. You should use Cognito Identity credentials to make this API call. |
| GET | /identitypools/{IdentityPoolId} | Gets usage details (for example, data storage) about a particular identity pool. This API can only be called with developer credentials. You cannot call this API with the temporary user credentials provided by Cognito Identity. |
| GET | /identitypools/{IdentityPoolId}/identities/{IdentityId} | Gets usage information for an identity, including number of datasets and data usage. This API can be called with temporary user credentials provided by Cognito Identity or with developer credentials. |
| POST | /identitypools/{IdentityPoolId}/getBulkPublishDetails | Get the status of the last BulkPublish operation for an identity pool.This API can only be called with developer credentials. You cannot call this API with the temporary user credentials provided by Cognito Identity. |
| GET | /identitypools/{IdentityPoolId}/events | Gets the events and the corresponding Lambda functions associated with an identity pool.This API can only be called with developer credentials. You cannot call this API with the temporary user credentials provided by Cognito Identity. |
| GET | /identitypools/{IdentityPoolId}/configuration | Gets the configuration settings of an identity pool.This API can only be called with developer credentials. You cannot call this API with the temporary user credentials provided by Cognito Identity. |
| GET | /identitypools/{IdentityPoolId}/identities/{IdentityId}/datasets | Lists datasets for an identity. With Amazon Cognito Sync, each identity has access only to its own data. Thus, the credentials used to make this API call need to have access to the identity data. ListDatasets can be called with temporary user credentials provided by Cognito Identity or with developer credentials. You should use the Cognito Identity credentials to make this API call. |
| GET | /identitypools | Gets a list of identity pools registered with Cognito. ListIdentityPoolUsage can only be called with developer credentials. You cannot make this API call with the temporary user credentials provided by Cognito Identity. |
| GET | /identitypools/{IdentityPoolId}/identities/{IdentityId}/datasets/{DatasetName}/records | Gets paginated records, optionally changed after a particular sync count for a dataset and identity. With Amazon Cognito Sync, each identity has access only to its own data. Thus, the credentials used to make this API call need to have access to the identity data. ListRecords can be called with temporary user credentials provided by Cognito Identity or with developer credentials. You should use Cognito Identity credentials to make this API call. |
| POST | /identitypools/{IdentityPoolId}/identity/{IdentityId}/device | Registers a device to receive push sync notifications.This API can only be called with temporary credentials provided by Cognito Identity. You cannot call this API with developer credentials. |
| POST | /identitypools/{IdentityPoolId}/events | Sets the AWS Lambda function for a given event type for an identity pool. This request only updates the key/value pair specified. Other key/values pairs are not updated. To remove a key value pair, pass a empty value for the particular key.This API can only be called with developer credentials. You cannot call this API with the temporary user credentials provided by Cognito Identity. |
| POST | /identitypools/{IdentityPoolId}/configuration | Sets the necessary configuration for push sync.This API can only be called with developer credentials. You cannot call this API with the temporary user credentials provided by Cognito Identity. |
| POST | /identitypools/{IdentityPoolId}/identities/{IdentityId}/datasets/{DatasetName}/subscriptions/{DeviceId} | Subscribes to receive notifications when a dataset is modified by another device.This API can only be called with temporary credentials provided by Cognito Identity. You cannot call this API with developer credentials. |
| DELETE | /identitypools/{IdentityPoolId}/identities/{IdentityId}/datasets/{DatasetName}/subscriptions/{DeviceId} | Unsubscribes from receiving notifications when a dataset is modified by another device.This API can only be called with temporary credentials provided by Cognito Identity. You cannot call this API with developer credentials. |
| POST | /identitypools/{IdentityPoolId}/identities/{IdentityId}/datasets/{DatasetName} | Posts updates to records and adds and deletes records for a dataset and user. The sync count in the record patch is your last known sync count for that record. The server will reject an UpdateRecords request with a ResourceConflictException if you try to patch a record with a new value but a stale sync count.For example, if the sync count on the server is 5 for a key called highScore and you try and submit a new highScore with sync count of 4, the request will be rejected. To obtain the current sync count for a record, call ListRecords. On a successful update of the record, the response returns the new sync count for that record. You should present that sync count the next time you try to update that same record. When the record does not exist, specify the sync count as 0. This API can be called with temporary user credentials provided by Cognito Identity or with developer credentials. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a bulkpublish?" -> POST /identitypools/{IdentityPoolId}/bulkpublish
- "Delete a dataset?" -> DELETE /identitypools/{IdentityPoolId}/identities/{IdentityId}/datasets/{DatasetName}
- "Get dataset details?" -> GET /identitypools/{IdentityPoolId}/identities/{IdentityId}/datasets/{DatasetName}
- "Get identitypool details?" -> GET /identitypools/{IdentityPoolId}
- "Get identity details?" -> GET /identitypools/{IdentityPoolId}/identities/{IdentityId}
- "Create a getBulkPublishDetail?" -> POST /identitypools/{IdentityPoolId}/getBulkPublishDetails
- "List all events?" -> GET /identitypools/{IdentityPoolId}/events
- "List all configuration?" -> GET /identitypools/{IdentityPoolId}/configuration
- "List all datasets?" -> GET /identitypools/{IdentityPoolId}/identities/{IdentityId}/datasets
- "List all identitypools?" -> GET /identitypools
- "List all records?" -> GET /identitypools/{IdentityPoolId}/identities/{IdentityId}/datasets/{DatasetName}/records
- "Create a device?" -> POST /identitypools/{IdentityPoolId}/identity/{IdentityId}/device
- "Create a event?" -> POST /identitypools/{IdentityPoolId}/events
- "Create a configuration?" -> POST /identitypools/{IdentityPoolId}/configuration
- "Delete a subscription?" -> DELETE /identitypools/{IdentityPoolId}/identities/{IdentityId}/datasets/{DatasetName}/subscriptions/{DeviceId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
