---
name: aws-mediatailor
description: "AWS MediaTailor API skill. Use when working with AWS MediaTailor for configureLogs, channel, sourceLocation. Covers 44 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS MediaTailor
API version: 2018-04-23

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /alerts -- verify access
3. POST /channel/{ChannelName} -- create first channel

## Endpoints

44 endpoints across 10 groups. See references/api-spec.lap for full details.

### configureLogs
| Method | Path | Description |
|--------|------|-------------|
| PUT | /configureLogs/channel | Configures Amazon CloudWatch log settings for a channel. |
| PUT | /configureLogs/playbackConfiguration | Amazon CloudWatch log settings for a playback configuration. |

### channel
| Method | Path | Description |
|--------|------|-------------|
| POST | /channel/{ChannelName} | Creates a channel. For information about MediaTailor channels, see Working with channels in the MediaTailor User Guide. |
| POST | /channel/{ChannelName}/program/{ProgramName} | Creates a program within a channel. For information about programs, see Working with programs in the MediaTailor User Guide. |
| DELETE | /channel/{ChannelName} | Deletes a channel. For information about MediaTailor channels, see Working with channels in the MediaTailor User Guide. |
| DELETE | /channel/{ChannelName}/policy | The channel policy to delete. |
| DELETE | /channel/{ChannelName}/program/{ProgramName} | Deletes a program within a channel. For information about programs, see Working with programs in the MediaTailor User Guide. |
| GET | /channel/{ChannelName} | Describes a channel. For information about MediaTailor channels, see Working with channels in the MediaTailor User Guide. |
| GET | /channel/{ChannelName}/program/{ProgramName} | Describes a program within a channel. For information about programs, see Working with programs in the MediaTailor User Guide. |
| GET | /channel/{ChannelName}/policy | Returns the channel's IAM policy. IAM policies are used to control access to your channel. |
| GET | /channel/{ChannelName}/schedule | Retrieves information about your channel's schedule. |
| PUT | /channel/{ChannelName}/policy | Creates an IAM policy for the channel. IAM policies are used to control access to your channel. |
| PUT | /channel/{ChannelName}/start | Starts a channel. For information about MediaTailor channels, see Working with channels in the MediaTailor User Guide. |
| PUT | /channel/{ChannelName}/stop | Stops a channel. For information about MediaTailor channels, see Working with channels in the MediaTailor User Guide. |
| PUT | /channel/{ChannelName} | Updates a channel. For information about MediaTailor channels, see Working with channels in the MediaTailor User Guide. |
| PUT | /channel/{ChannelName}/program/{ProgramName} | Updates a program within a channel. |

### sourceLocation
| Method | Path | Description |
|--------|------|-------------|
| POST | /sourceLocation/{SourceLocationName}/liveSource/{LiveSourceName} | The live source configuration. |
| POST | /sourceLocation/{SourceLocationName} | Creates a source location. A source location is a container for sources. For more information about source locations, see Working with source locations in the MediaTailor User Guide. |
| POST | /sourceLocation/{SourceLocationName}/vodSource/{VodSourceName} | The VOD source configuration parameters. |
| DELETE | /sourceLocation/{SourceLocationName}/liveSource/{LiveSourceName} | The live source to delete. |
| DELETE | /sourceLocation/{SourceLocationName} | Deletes a source location. A source location is a container for sources. For more information about source locations, see Working with source locations in the MediaTailor User Guide. |
| DELETE | /sourceLocation/{SourceLocationName}/vodSource/{VodSourceName} | The video on demand (VOD) source to delete. |
| GET | /sourceLocation/{SourceLocationName}/liveSource/{LiveSourceName} | The live source to describe. |
| GET | /sourceLocation/{SourceLocationName} | Describes a source location. A source location is a container for sources. For more information about source locations, see Working with source locations in the MediaTailor User Guide. |
| GET | /sourceLocation/{SourceLocationName}/vodSource/{VodSourceName} | Provides details about a specific video on demand (VOD) source in a specific source location. |
| GET | /sourceLocation/{SourceLocationName}/liveSources | Lists the live sources contained in a source location. A source represents a piece of content. |
| GET | /sourceLocation/{SourceLocationName}/vodSources | Lists the VOD sources contained in a source location. A source represents a piece of content. |
| PUT | /sourceLocation/{SourceLocationName}/liveSource/{LiveSourceName} | Updates a live source's configuration. |
| PUT | /sourceLocation/{SourceLocationName} | Updates a source location. A source location is a container for sources. For more information about source locations, see Working with source locations in the MediaTailor User Guide. |
| PUT | /sourceLocation/{SourceLocationName}/vodSource/{VodSourceName} | Updates a VOD source's configuration. |

### prefetchSchedule
| Method | Path | Description |
|--------|------|-------------|
| POST | /prefetchSchedule/{PlaybackConfigurationName}/{Name} | Creates a prefetch schedule for a playback configuration. A prefetch schedule allows you to tell MediaTailor to fetch and prepare certain ads before an ad break happens. For more information about ad prefetching, see Using ad prefetching in the MediaTailor User Guide. |
| DELETE | /prefetchSchedule/{PlaybackConfigurationName}/{Name} | Deletes a prefetch schedule for a specific playback configuration. If you call DeletePrefetchSchedule on an expired prefetch schedule, MediaTailor returns an HTTP 404 status code. For more information about ad prefetching, see Using ad prefetching in the MediaTailor User Guide. |
| GET | /prefetchSchedule/{PlaybackConfigurationName}/{Name} | Retrieves a prefetch schedule for a playback configuration. A prefetch schedule allows you to tell MediaTailor to fetch and prepare certain ads before an ad break happens. For more information about ad prefetching, see Using ad prefetching in the MediaTailor User Guide. |
| POST | /prefetchSchedule/{PlaybackConfigurationName} | Lists the prefetch schedules for a playback configuration. |

### playbackConfiguration
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /playbackConfiguration/{Name} | Deletes a playback configuration. For information about MediaTailor configurations, see Working with configurations in AWS Elemental MediaTailor. |
| GET | /playbackConfiguration/{Name} | Retrieves a playback configuration. For information about MediaTailor configurations, see Working with configurations in AWS Elemental MediaTailor. |
| PUT | /playbackConfiguration | Creates a playback configuration. For information about MediaTailor configurations, see Working with configurations in AWS Elemental MediaTailor. |

### alerts
| Method | Path | Description |
|--------|------|-------------|
| GET | /alerts | Lists the alerts that are associated with a MediaTailor channel assembly resource. |

### channels
| Method | Path | Description |
|--------|------|-------------|
| GET | /channels | Retrieves information about the channels that are associated with the current AWS account. |

### playbackConfigurations
| Method | Path | Description |
|--------|------|-------------|
| GET | /playbackConfigurations | Retrieves existing playback configurations. For information about MediaTailor configurations, see Working with Configurations in AWS Elemental MediaTailor. |

### sourceLocations
| Method | Path | Description |
|--------|------|-------------|
| GET | /sourceLocations | Lists the source locations for a channel. A source location defines the host server URL, and contains a list of sources. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{ResourceArn} | A list of tags that are associated with this resource. Tags are key-value pairs that you can associate with Amazon resources to help with organization, access control, and cost tracking. For more information, see Tagging AWS Elemental MediaTailor Resources. |
| POST | /tags/{ResourceArn} | The resource to tag. Tags are key-value pairs that you can associate with Amazon resources to help with organization, access control, and cost tracking. For more information, see Tagging AWS Elemental MediaTailor Resources. |
| DELETE | /tags/{ResourceArn} | The resource to untag. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Delete a channel?" -> DELETE /channel/{ChannelName}
- "Delete a liveSource?" -> DELETE /sourceLocation/{SourceLocationName}/liveSource/{LiveSourceName}
- "Delete a playbackConfiguration?" -> DELETE /playbackConfiguration/{Name}
- "Delete a prefetchSchedule?" -> DELETE /prefetchSchedule/{PlaybackConfigurationName}/{Name}
- "Delete a program?" -> DELETE /channel/{ChannelName}/program/{ProgramName}
- "Delete a sourceLocation?" -> DELETE /sourceLocation/{SourceLocationName}
- "Delete a vodSource?" -> DELETE /sourceLocation/{SourceLocationName}/vodSource/{VodSourceName}
- "Get channel details?" -> GET /channel/{ChannelName}
- "Get liveSource details?" -> GET /sourceLocation/{SourceLocationName}/liveSource/{LiveSourceName}
- "Get program details?" -> GET /channel/{ChannelName}/program/{ProgramName}
- "Get sourceLocation details?" -> GET /sourceLocation/{SourceLocationName}
- "Get vodSource details?" -> GET /sourceLocation/{SourceLocationName}/vodSource/{VodSourceName}
- "List all policy?" -> GET /channel/{ChannelName}/policy
- "List all schedule?" -> GET /channel/{ChannelName}/schedule
- "Get playbackConfiguration details?" -> GET /playbackConfiguration/{Name}
- "Get prefetchSchedule details?" -> GET /prefetchSchedule/{PlaybackConfigurationName}/{Name}
- "List all alerts?" -> GET /alerts
- "List all channels?" -> GET /channels
- "List all liveSources?" -> GET /sourceLocation/{SourceLocationName}/liveSources
- "List all playbackConfigurations?" -> GET /playbackConfigurations
- "List all sourceLocations?" -> GET /sourceLocations
- "Get tag details?" -> GET /tags/{ResourceArn}
- "List all vodSources?" -> GET /sourceLocation/{SourceLocationName}/vodSources
- "Delete a tag?" -> DELETE /tags/{ResourceArn}
- "Update a channel?" -> PUT /channel/{ChannelName}
- "Update a liveSource?" -> PUT /sourceLocation/{SourceLocationName}/liveSource/{LiveSourceName}
- "Update a program?" -> PUT /channel/{ChannelName}/program/{ProgramName}
- "Update a sourceLocation?" -> PUT /sourceLocation/{SourceLocationName}
- "Update a vodSource?" -> PUT /sourceLocation/{SourceLocationName}/vodSource/{VodSourceName}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
