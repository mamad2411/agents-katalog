---
name: amazon-elastic-block-store
description: "Amazon Elastic Block Store API skill. Use when working with Amazon Elastic Block Store for snapshots. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Elastic Block Store
API version: 2019-11-02

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /snapshots/{secondSnapshotId}/changedblocks -- verify access
3. POST /snapshots/completion/{snapshotId} -- create first completion

## Endpoints

6 endpoints across 1 groups. See references/api-spec.lap for full details.

### snapshots
| Method | Path | Description |
|--------|------|-------------|
| POST | /snapshots/completion/{snapshotId} | Seals and completes the snapshot after all of the required blocks of data have been written to it. Completing the snapshot changes the status to completed. You cannot write new blocks to a snapshot after it has been completed.  You should always retry requests that receive server (5xx) error responses, and ThrottlingException and RequestThrottledException client error responses. For more information see Error retries in the Amazon Elastic Compute Cloud User Guide. |
| GET | /snapshots/{snapshotId}/blocks/{blockIndex} | Returns the data in a block in an Amazon Elastic Block Store snapshot.  You should always retry requests that receive server (5xx) error responses, and ThrottlingException and RequestThrottledException client error responses. For more information see Error retries in the Amazon Elastic Compute Cloud User Guide. |
| GET | /snapshots/{secondSnapshotId}/changedblocks | Returns information about the blocks that are different between two Amazon Elastic Block Store snapshots of the same volume/snapshot lineage.  You should always retry requests that receive server (5xx) error responses, and ThrottlingException and RequestThrottledException client error responses. For more information see Error retries in the Amazon Elastic Compute Cloud User Guide. |
| GET | /snapshots/{snapshotId}/blocks | Returns information about the blocks in an Amazon Elastic Block Store snapshot.  You should always retry requests that receive server (5xx) error responses, and ThrottlingException and RequestThrottledException client error responses. For more information see Error retries in the Amazon Elastic Compute Cloud User Guide. |
| PUT | /snapshots/{snapshotId}/blocks/{blockIndex} | Writes a block of data to a snapshot. If the specified block contains data, the existing data is overwritten. The target snapshot must be in the pending state. Data written to a snapshot must be aligned with 512-KiB sectors.  You should always retry requests that receive server (5xx) error responses, and ThrottlingException and RequestThrottledException client error responses. For more information see Error retries in the Amazon Elastic Compute Cloud User Guide. |
| POST | /snapshots | Creates a new Amazon EBS snapshot. The new snapshot enters the pending state after the request completes.  After creating the snapshot, use  PutSnapshotBlock to write blocks of data to the snapshot.  You should always retry requests that receive server (5xx) error responses, and ThrottlingException and RequestThrottledException client error responses. For more information see Error retries in the Amazon Elastic Compute Cloud User Guide. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get block details?" -> GET /snapshots/{snapshotId}/blocks/{blockIndex}
- "List all changedblocks?" -> GET /snapshots/{secondSnapshotId}/changedblocks
- "List all blocks?" -> GET /snapshots/{snapshotId}/blocks
- "Update a block?" -> PUT /snapshots/{snapshotId}/blocks/{blockIndex}
- "Create a snapshot?" -> POST /snapshots
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
