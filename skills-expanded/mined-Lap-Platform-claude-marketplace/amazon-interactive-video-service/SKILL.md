---
name: amazon-interactive-video-service
description: "Amazon Interactive Video Service API skill. Use when working with Amazon Interactive Video Service for BatchGetChannel, BatchGetStreamKey, BatchStartViewerSessionRevocation. Covers 35 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Interactive Video Service
API version: 2020-07-14

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /tags/{resourceArn} -- verify access
3. POST /BatchGetChannel -- create first BatchGetChannel

## Endpoints

35 endpoints across 33 groups. See references/api-spec.lap for full details.

### BatchGetChannel
| Method | Path | Description |
|--------|------|-------------|
| POST | /BatchGetChannel | Performs GetChannel on multiple ARNs simultaneously. |

### BatchGetStreamKey
| Method | Path | Description |
|--------|------|-------------|
| POST | /BatchGetStreamKey | Performs GetStreamKey on multiple ARNs simultaneously. |

### BatchStartViewerSessionRevocation
| Method | Path | Description |
|--------|------|-------------|
| POST | /BatchStartViewerSessionRevocation | Performs StartViewerSessionRevocation on multiple channel ARN and viewer ID pairs simultaneously. |

### CreateChannel
| Method | Path | Description |
|--------|------|-------------|
| POST | /CreateChannel | Creates a new channel and an associated stream key to start streaming. |

### CreatePlaybackRestrictionPolicy
| Method | Path | Description |
|--------|------|-------------|
| POST | /CreatePlaybackRestrictionPolicy | Creates a new playback restriction policy, for constraining playback by countries and/or origins. |

### CreateRecordingConfiguration
| Method | Path | Description |
|--------|------|-------------|
| POST | /CreateRecordingConfiguration | Creates a new recording configuration, used to enable recording to Amazon S3.  Known issue: In the us-east-1 region, if you use the Amazon Web Services CLI to create a recording configuration, it returns success even if the S3 bucket is in a different region. In this case, the state of the recording configuration is CREATE_FAILED (instead of ACTIVE). (In other regions, the CLI correctly returns failure if the bucket is in a different region.)  Workaround: Ensure that your S3 bucket is in the same region as the recording configuration. If you create a recording configuration in a different region as your S3 bucket, delete that recording configuration and create a new one with an S3 bucket from the correct region. |

### CreateStreamKey
| Method | Path | Description |
|--------|------|-------------|
| POST | /CreateStreamKey | Creates a stream key, used to initiate a stream, for the specified channel ARN. Note that CreateChannel creates a stream key. If you subsequently use CreateStreamKey on the same channel, it will fail because a stream key already exists and there is a limit of 1 stream key per channel. To reset the stream key on a channel, use DeleteStreamKey and then CreateStreamKey. |

### DeleteChannel
| Method | Path | Description |
|--------|------|-------------|
| POST | /DeleteChannel | Deletes the specified channel and its associated stream keys. If you try to delete a live channel, you will get an error (409 ConflictException). To delete a channel that is live, call StopStream, wait for the Amazon EventBridge "Stream End" event (to verify that the stream's state is no longer Live), then call DeleteChannel. (See  Using EventBridge with Amazon IVS.) |

### DeletePlaybackKeyPair
| Method | Path | Description |
|--------|------|-------------|
| POST | /DeletePlaybackKeyPair | Deletes a specified authorization key pair. This invalidates future viewer tokens generated using the key pair’s privateKey. For more information, see Setting Up Private Channels in the Amazon IVS User Guide. |

### DeletePlaybackRestrictionPolicy
| Method | Path | Description |
|--------|------|-------------|
| POST | /DeletePlaybackRestrictionPolicy | Deletes the specified playback restriction policy. |

### DeleteRecordingConfiguration
| Method | Path | Description |
|--------|------|-------------|
| POST | /DeleteRecordingConfiguration | Deletes the recording configuration for the specified ARN. If you try to delete a recording configuration that is associated with a channel, you will get an error (409 ConflictException). To avoid this, for all channels that reference the recording configuration, first use UpdateChannel to set the recordingConfigurationArn field to an empty string, then use DeleteRecordingConfiguration. |

### DeleteStreamKey
| Method | Path | Description |
|--------|------|-------------|
| POST | /DeleteStreamKey | Deletes the stream key for the specified ARN, so it can no longer be used to stream. |

### GetChannel
| Method | Path | Description |
|--------|------|-------------|
| POST | /GetChannel | Gets the channel configuration for the specified channel ARN. See also BatchGetChannel. |

### GetPlaybackKeyPair
| Method | Path | Description |
|--------|------|-------------|
| POST | /GetPlaybackKeyPair | Gets a specified playback authorization key pair and returns the arn and fingerprint. The privateKey held by the caller can be used to generate viewer authorization tokens, to grant viewers access to private channels. For more information, see Setting Up Private Channels in the Amazon IVS User Guide. |

### GetPlaybackRestrictionPolicy
| Method | Path | Description |
|--------|------|-------------|
| POST | /GetPlaybackRestrictionPolicy | Gets the specified playback restriction policy. |

### GetRecordingConfiguration
| Method | Path | Description |
|--------|------|-------------|
| POST | /GetRecordingConfiguration | Gets the recording configuration for the specified ARN. |

### GetStream
| Method | Path | Description |
|--------|------|-------------|
| POST | /GetStream | Gets information about the active (live) stream on a specified channel. |

### GetStreamKey
| Method | Path | Description |
|--------|------|-------------|
| POST | /GetStreamKey | Gets stream-key information for a specified ARN. |

### GetStreamSession
| Method | Path | Description |
|--------|------|-------------|
| POST | /GetStreamSession | Gets metadata on a specified stream. |

### ImportPlaybackKeyPair
| Method | Path | Description |
|--------|------|-------------|
| POST | /ImportPlaybackKeyPair | Imports the public portion of a new key pair and returns its arn and fingerprint. The privateKey can then be used to generate viewer authorization tokens, to grant viewers access to private channels. For more information, see Setting Up Private Channels in the Amazon IVS User Guide. |

### ListChannels
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListChannels | Gets summary information about all channels in your account, in the Amazon Web Services region where the API request is processed. This list can be filtered to match a specified name or recording-configuration ARN. Filters are mutually exclusive and cannot be used together. If you try to use both filters, you will get an error (409 ConflictException). |

### ListPlaybackKeyPairs
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListPlaybackKeyPairs | Gets summary information about playback key pairs. For more information, see Setting Up Private Channels in the Amazon IVS User Guide. |

### ListPlaybackRestrictionPolicies
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListPlaybackRestrictionPolicies | Gets summary information about playback restriction policies. |

### ListRecordingConfigurations
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListRecordingConfigurations | Gets summary information about all recording configurations in your account, in the Amazon Web Services region where the API request is processed. |

### ListStreamKeys
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListStreamKeys | Gets summary information about stream keys for the specified channel. |

### ListStreamSessions
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListStreamSessions | Gets a summary of current and previous streams for a specified channel in your account, in the AWS region where the API request is processed. |

### ListStreams
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListStreams | Gets summary information about live streams in your account, in the Amazon Web Services region where the API request is processed. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | Gets information about Amazon Web Services tags for the specified ARN. |
| POST | /tags/{resourceArn} | Adds or updates tags for the Amazon Web Services resource with the specified ARN. |
| DELETE | /tags/{resourceArn} | Removes tags from the resource with the specified ARN. |

### PutMetadata
| Method | Path | Description |
|--------|------|-------------|
| POST | /PutMetadata | Inserts metadata into the active stream of the specified channel. At most 5 requests per second per channel are allowed, each with a maximum 1 KB payload. (If 5 TPS is not sufficient for your needs, we recommend batching your data into a single PutMetadata call.) At most 155 requests per second per account are allowed. Also see Embedding Metadata within a Video Stream in the Amazon IVS User Guide. |

### StartViewerSessionRevocation
| Method | Path | Description |
|--------|------|-------------|
| POST | /StartViewerSessionRevocation | Starts the process of revoking the viewer session associated with a specified channel ARN and viewer ID. Optionally, you can provide a version to revoke viewer sessions less than and including that version. For instructions on associating a viewer ID with a viewer session, see Setting Up Private Channels. |

### StopStream
| Method | Path | Description |
|--------|------|-------------|
| POST | /StopStream | Disconnects the incoming RTMPS stream for the specified channel. Can be used in conjunction with DeleteStreamKey to prevent further streaming to a channel.  Many streaming client-software libraries automatically reconnect a dropped RTMPS session, so to stop the stream permanently, you may want to first revoke the streamKey attached to the channel. |

### UpdateChannel
| Method | Path | Description |
|--------|------|-------------|
| POST | /UpdateChannel | Updates a channel's configuration. Live channels cannot be updated. You must stop the ongoing stream, update the channel, and restart the stream for the changes to take effect. |

### UpdatePlaybackRestrictionPolicy
| Method | Path | Description |
|--------|------|-------------|
| POST | /UpdatePlaybackRestrictionPolicy | Updates a specified playback restriction policy. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a BatchGetChannel?" -> POST /BatchGetChannel
- "Create a BatchGetStreamKey?" -> POST /BatchGetStreamKey
- "Create a BatchStartViewerSessionRevocation?" -> POST /BatchStartViewerSessionRevocation
- "Create a CreateChannel?" -> POST /CreateChannel
- "Create a CreatePlaybackRestrictionPolicy?" -> POST /CreatePlaybackRestrictionPolicy
- "Create a CreateRecordingConfiguration?" -> POST /CreateRecordingConfiguration
- "Create a CreateStreamKey?" -> POST /CreateStreamKey
- "Create a DeleteChannel?" -> POST /DeleteChannel
- "Create a DeletePlaybackKeyPair?" -> POST /DeletePlaybackKeyPair
- "Create a DeletePlaybackRestrictionPolicy?" -> POST /DeletePlaybackRestrictionPolicy
- "Create a DeleteRecordingConfiguration?" -> POST /DeleteRecordingConfiguration
- "Create a DeleteStreamKey?" -> POST /DeleteStreamKey
- "Create a GetChannel?" -> POST /GetChannel
- "Create a GetPlaybackKeyPair?" -> POST /GetPlaybackKeyPair
- "Create a GetPlaybackRestrictionPolicy?" -> POST /GetPlaybackRestrictionPolicy
- "Create a GetRecordingConfiguration?" -> POST /GetRecordingConfiguration
- "Create a GetStream?" -> POST /GetStream
- "Create a GetStreamKey?" -> POST /GetStreamKey
- "Create a GetStreamSession?" -> POST /GetStreamSession
- "Create a ImportPlaybackKeyPair?" -> POST /ImportPlaybackKeyPair
- "Create a ListChannel?" -> POST /ListChannels
- "Create a ListPlaybackKeyPair?" -> POST /ListPlaybackKeyPairs
- "Create a ListPlaybackRestrictionPolicy?" -> POST /ListPlaybackRestrictionPolicies
- "Create a ListRecordingConfiguration?" -> POST /ListRecordingConfigurations
- "Create a ListStreamKey?" -> POST /ListStreamKeys
- "Create a ListStreamSession?" -> POST /ListStreamSessions
- "Create a ListStream?" -> POST /ListStreams
- "Get tag details?" -> GET /tags/{resourceArn}
- "Create a PutMetadata?" -> POST /PutMetadata
- "Create a StartViewerSessionRevocation?" -> POST /StartViewerSessionRevocation
- "Create a StopStream?" -> POST /StopStream
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "Create a UpdateChannel?" -> POST /UpdateChannel
- "Create a UpdatePlaybackRestrictionPolicy?" -> POST /UpdatePlaybackRestrictionPolicy
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
