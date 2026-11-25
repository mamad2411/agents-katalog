---
name: datalakestorefilesystemmanagementclient
description: "DataLakeStoreFileSystemManagementClient API skill. Use when working with DataLakeStoreFileSystemManagementClient for WebHdfsExt, webhdfs. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# DataLakeStoreFileSystemManagementClient
API version: 2016-11-01

## Auth
No authentication required.

## Base URL
Not specified.

## Setup
1. No auth setup needed
2. GET /webhdfs/v1/{path} -- verify access
3. POST /WebHdfsExt/{path} -- create first WebHdfsExt

## Endpoints

3 endpoints across 2 groups. See references/api-spec.lap for full details.

### WebHdfsExt
| Method | Path | Description |
|--------|------|-------------|
| PUT | /WebHdfsExt/{path} | Sets or removes the expiration time on the specified file. This operation can only be executed against files. Folders are not supported. |
| POST | /WebHdfsExt/{path} | Appends to the specified file, optionally first creating the file if it does not yet exist. This method supports multiple concurrent appends to the file. NOTE: The target must not contain data added by Create or normal (serial) Append. ConcurrentAppend and Append cannot be used interchangeably; once a target file has been modified using either of these append options, the other append option cannot be used on the target file. ConcurrentAppend does not guarantee order and can result in duplicated data landing in the target file. |

### webhdfs
| Method | Path | Description |
|--------|------|-------------|
| GET | /webhdfs/v1/{path} | Checks if the specified access is available at the given path. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Update a WebHdfsExt?" -> PUT /WebHdfsExt/{path}
- "Get webhdf details?" -> GET /webhdfs/v1/{path}

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
