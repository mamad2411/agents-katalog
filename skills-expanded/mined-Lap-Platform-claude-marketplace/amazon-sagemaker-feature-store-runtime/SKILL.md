---
name: amazon-sagemaker-feature-store-runtime
description: "Amazon SageMaker Feature Store Runtime API skill. Use when working with Amazon SageMaker Feature Store Runtime for BatchGetRecord, FeatureGroup. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon SageMaker Feature Store Runtime
API version: 2020-07-01

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /FeatureGroup/{FeatureGroupName} -- verify access
3. POST /BatchGetRecord -- create first BatchGetRecord

## Endpoints

4 endpoints across 2 groups. See references/api-spec.lap for full details.

### BatchGetRecord
| Method | Path | Description |
|--------|------|-------------|
| POST | /BatchGetRecord | Retrieves a batch of Records from a FeatureGroup. |

### FeatureGroup
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /FeatureGroup/{FeatureGroupName} | Deletes a Record from a FeatureGroup in the OnlineStore. Feature Store supports both SoftDelete and HardDelete. For SoftDelete (default), feature columns are set to null and the record is no longer retrievable by GetRecord or BatchGetRecord. For HardDelete, the complete Record is removed from the OnlineStore. In both cases, Feature Store appends the deleted record marker to the OfflineStore. The deleted record marker is a record with the same RecordIdentifer as the original, but with is_deleted value set to True, EventTime set to the delete input EventTime, and other feature values set to null. Note that the EventTime specified in DeleteRecord should be set later than the EventTime of the existing record in the OnlineStore for that RecordIdentifer. If it is not, the deletion does not occur:   For SoftDelete, the existing (not deleted) record remains in the OnlineStore, though the delete record marker is still written to the OfflineStore.    HardDelete returns EventTime: 400 ValidationException to indicate that the delete operation failed. No delete record marker is written to the OfflineStore.   When a record is deleted from the OnlineStore, the deleted record marker is appended to the OfflineStore. If you have the Iceberg table format enabled for your OfflineStore, you can remove all history of a record from the OfflineStore using Amazon Athena or Apache Spark. For information on how to hard delete a record from the OfflineStore with the Iceberg table format enabled, see Delete records from the offline store. |
| GET | /FeatureGroup/{FeatureGroupName} | Use for OnlineStore serving from a FeatureStore. Only the latest records stored in the OnlineStore can be retrieved. If no Record with RecordIdentifierValue is found, then an empty result is returned. |
| PUT | /FeatureGroup/{FeatureGroupName} | The PutRecord API is used to ingest a list of Records into your feature group.  If a new record’s EventTime is greater, the new record is written to both the OnlineStore and OfflineStore. Otherwise, the record is a historic record and it is written only to the OfflineStore.  You can specify the ingestion to be applied to the OnlineStore, OfflineStore, or both by using the TargetStores request parameter.  You can set the ingested record to expire at a given time to live (TTL) duration after the record’s event time, ExpiresAt = EventTime + TtlDuration, by specifying the TtlDuration parameter. A record level TtlDuration is set when specifying the TtlDuration parameter using the PutRecord API call. If the input TtlDuration is null or unspecified, TtlDuration is set to the default feature group level TtlDuration. A record level TtlDuration supersedes the group level TtlDuration. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a BatchGetRecord?" -> POST /BatchGetRecord
- "Delete a FeatureGroup?" -> DELETE /FeatureGroup/{FeatureGroupName}
- "Get FeatureGroup details?" -> GET /FeatureGroup/{FeatureGroupName}
- "Update a FeatureGroup?" -> PUT /FeatureGroup/{FeatureGroupName}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
