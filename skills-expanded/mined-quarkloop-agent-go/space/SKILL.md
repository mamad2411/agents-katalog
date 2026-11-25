# service-space

The space service owns the authoritative `space.json` configuration file,
opaque per-space record persistence, and configuration diagnostics. It does
not interpret records, plugin policy, or mutate user working directories.

Use `quark.space.v1.SpaceService` service functions for space lifecycle and
metadata operations. Space business logic lives behind this NATS
service-function contract.

## RPCs

- `CreateSpace(CreateSpaceRequest) -> Space`
  - Generated service function: `space_CreateSpace`
  - Required: `config`
  - Creates the service-owned space layout and writes its initial `space.json`.

- `UpdateConfig(UpdateConfigRequest) -> Space`
  - Generated service function: `space_UpdateConfig`
  - Required: `config`
  - Replaces `space.json`, retaining service-owned creation metadata.

- `GetSpace(GetSpaceRequest) -> Space`
  - Generated service function: `space_GetSpace`
  - Required: `name`
  - Returns metadata for one space.

- `ListSpaces(Empty) -> ListSpacesResponse`
  - Generated service function: `space_ListSpaces`
  - Lists all registered spaces.

- `DeleteSpace(DeleteSpaceRequest) -> Empty`
  - Generated service function: `space_DeleteSpace`
  - Required: `name`
  - Deletes a space and all service-owned data.

- `GetConfig(GetConfigRequest) -> ConfigResponse`
  - Generated service function: `space_GetConfig`
  - Required: `name`
  - Returns the authoritative space configuration and version.

- `PutRecord(PutRecordRequest) -> Record`
  - Generated service function: `space_PutRecord`
  - Required: `name`, `namespace`, `key`, `data`
  - Persists opaque bytes; the caller owns their meaning.

- `GetRecord(GetRecordRequest) -> Record`
  - Generated service function: `space_GetRecord`
  - Required: `name`, `namespace`, `key`
  - Reads opaque bytes without interpreting them.

- `ListRecords(ListRecordsRequest) -> ListRecordsResponse`
  - Generated service function: `space_ListRecords`
  - Required: `name`, `namespace`
  - Lists caller-owned records.

- `DeleteRecord(DeleteRecordRequest) -> Empty`
  - Generated service function: `space_DeleteRecord`
  - Required: `name`, `namespace`, `key`
  - Removes one caller-owned record.

- `Doctor(DoctorRequest) -> DoctorResponse`
  - Generated service function: `space_Doctor`
  - Required: `name`
  - Validates stored `space.json` syntax and space invariants.

## Contract Notes

- Spaces are keyed by `space.json` `name`, not by path.
- Plugin meaning, catalog resolution, and orchestration remain supervisor-owned.
- The CLI should use supervisor-owned NATS contracts for space operations.
- Runtime and supervisor callers should use service functions for space
  persistence operations.
