---
name: amazon-qldb
description: "Amazon QLDB API skill. Use when working with Amazon QLDB for ledgers, journal-s3-exports, tags. Covers 20 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon QLDB
API version: 2019-01-02

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /journal-s3-exports -- verify access
3. POST /ledgers -- create first ledgers

## Endpoints

20 endpoints across 3 groups. See references/api-spec.lap for full details.

### ledgers
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /ledgers/{name}/journal-kinesis-streams/{streamId} | Ends a given Amazon QLDB journal stream. Before a stream can be canceled, its current status must be ACTIVE. You can't restart a stream after you cancel it. Canceled QLDB stream resources are subject to a 7-day retention period, so they are automatically deleted after this limit expires. |
| POST | /ledgers | Creates a new ledger in your Amazon Web Services account in the current Region. |
| DELETE | /ledgers/{name} | Deletes a ledger and all of its contents. This action is irreversible. If deletion protection is enabled, you must first disable it before you can delete the ledger. You can disable it by calling the UpdateLedger operation to set this parameter to false. |
| GET | /ledgers/{name}/journal-kinesis-streams/{streamId} | Returns detailed information about a given Amazon QLDB journal stream. The output includes the Amazon Resource Name (ARN), stream name, current status, creation time, and the parameters of the original stream creation request. This action does not return any expired journal streams. For more information, see Expiration for terminal streams in the Amazon QLDB Developer Guide. |
| GET | /ledgers/{name}/journal-s3-exports/{exportId} | Returns information about a journal export job, including the ledger name, export ID, creation time, current status, and the parameters of the original export creation request. This action does not return any expired export jobs. For more information, see Export job expiration in the Amazon QLDB Developer Guide. If the export job with the given ExportId doesn't exist, then throws ResourceNotFoundException. If the ledger with the given Name doesn't exist, then throws ResourceNotFoundException. |
| GET | /ledgers/{name} | Returns information about a ledger, including its state, permissions mode, encryption at rest settings, and when it was created. |
| POST | /ledgers/{name}/journal-s3-exports | Exports journal contents within a date and time range from a ledger into a specified Amazon Simple Storage Service (Amazon S3) bucket. A journal export job can write the data objects in either the text or binary representation of Amazon Ion format, or in JSON Lines text format. If the ledger with the given Name doesn't exist, then throws ResourceNotFoundException. If the ledger with the given Name is in CREATING status, then throws ResourcePreconditionNotMetException. You can initiate up to two concurrent journal export requests for each ledger. Beyond this limit, journal export requests throw LimitExceededException. |
| POST | /ledgers/{name}/block | Returns a block object at a specified address in a journal. Also returns a proof of the specified block for verification if DigestTipAddress is provided. For information about the data contents in a block, see Journal contents in the Amazon QLDB Developer Guide. If the specified ledger doesn't exist or is in DELETING status, then throws ResourceNotFoundException. If the specified ledger is in CREATING status, then throws ResourcePreconditionNotMetException. If no block exists with the specified address, then throws InvalidParameterException. |
| POST | /ledgers/{name}/digest | Returns the digest of a ledger at the latest committed block in the journal. The response includes a 256-bit hash value and a block address. |
| POST | /ledgers/{name}/revision | Returns a revision data object for a specified document ID and block address. Also returns a proof of the specified revision for verification if DigestTipAddress is provided. |
| GET | /ledgers/{name}/journal-kinesis-streams | Returns all Amazon QLDB journal streams for a given ledger. This action does not return any expired journal streams. For more information, see Expiration for terminal streams in the Amazon QLDB Developer Guide. This action returns a maximum of MaxResults items. It is paginated so that you can retrieve all the items by calling ListJournalKinesisStreamsForLedger multiple times. |
| GET | /ledgers/{name}/journal-s3-exports | Returns all journal export jobs for a specified ledger. This action returns a maximum of MaxResults items, and is paginated so that you can retrieve all the items by calling ListJournalS3ExportsForLedger multiple times. This action does not return any expired export jobs. For more information, see Export job expiration in the Amazon QLDB Developer Guide. |
| GET | /ledgers | Returns all ledgers that are associated with the current Amazon Web Services account and Region. This action returns a maximum of MaxResults items and is paginated so that you can retrieve all the items by calling ListLedgers multiple times. |
| POST | /ledgers/{name}/journal-kinesis-streams | Creates a journal stream for a given Amazon QLDB ledger. The stream captures every document revision that is committed to the ledger's journal and delivers the data to a specified Amazon Kinesis Data Streams resource. |
| PATCH | /ledgers/{name} | Updates properties on a ledger. |
| PATCH | /ledgers/{name}/permissions-mode | Updates the permissions mode of a ledger.  Before you switch to the STANDARD permissions mode, you must first create all required IAM policies and table tags to avoid disruption to your users. To learn more, see Migrating to the standard permissions mode in the Amazon QLDB Developer Guide. |

### journal-s3-exports
| Method | Path | Description |
|--------|------|-------------|
| GET | /journal-s3-exports | Returns all journal export jobs for all ledgers that are associated with the current Amazon Web Services account and Region. This action returns a maximum of MaxResults items, and is paginated so that you can retrieve all the items by calling ListJournalS3Exports multiple times. This action does not return any expired export jobs. For more information, see Export job expiration in the Amazon QLDB Developer Guide. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | Returns all tags for a specified Amazon QLDB resource. |
| POST | /tags/{resourceArn} | Adds one or more tags to a specified Amazon QLDB resource. A resource can have up to 50 tags. If you try to create more than 50 tags for a resource, your request fails and returns an error. |
| DELETE | /tags/{resourceArn} | Removes one or more tags from a specified Amazon QLDB resource. You can specify up to 50 tag keys to remove. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Delete a journal-kinesis-stream?" -> DELETE /ledgers/{name}/journal-kinesis-streams/{streamId}
- "Create a ledger?" -> POST /ledgers
- "Delete a ledger?" -> DELETE /ledgers/{name}
- "Get journal-kinesis-stream details?" -> GET /ledgers/{name}/journal-kinesis-streams/{streamId}
- "Get journal-s3-export details?" -> GET /ledgers/{name}/journal-s3-exports/{exportId}
- "Get ledger details?" -> GET /ledgers/{name}
- "Create a journal-s3-export?" -> POST /ledgers/{name}/journal-s3-exports
- "Create a block?" -> POST /ledgers/{name}/block
- "Create a digest?" -> POST /ledgers/{name}/digest
- "Create a revision?" -> POST /ledgers/{name}/revision
- "List all journal-kinesis-streams?" -> GET /ledgers/{name}/journal-kinesis-streams
- "List all journal-s3-exports?" -> GET /journal-s3-exports
- "List all journal-s3-exports?" -> GET /ledgers/{name}/journal-s3-exports
- "List all ledgers?" -> GET /ledgers
- "Get tag details?" -> GET /tags/{resourceArn}
- "Create a journal-kinesis-stream?" -> POST /ledgers/{name}/journal-kinesis-streams
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "Partially update a ledger?" -> PATCH /ledgers/{name}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
