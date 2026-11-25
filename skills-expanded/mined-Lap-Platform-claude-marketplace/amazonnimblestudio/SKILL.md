---
name: amazonnimblestudio
description: "AmazonNimbleStudio API skill. Use when working with AmazonNimbleStudio for 2020-08-01. Covers 49 endpoints."
version: 1.0.0
generator: lapsh
---

# AmazonNimbleStudio
API version: 2020-08-01

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /2020-08-01/eulas -- verify access
3. POST /2020-08-01/studios/{studioId}/eula-acceptances -- create first eula-acceptances

## Endpoints

49 endpoints across 1 groups. See references/api-spec.lap for full details.

### 2020-08-01
| Method | Path | Description |
|--------|------|-------------|
| POST | /2020-08-01/studios/{studioId}/eula-acceptances | Accept EULAs. |
| POST | /2020-08-01/studios/{studioId}/launch-profiles | Create a launch profile. |
| POST | /2020-08-01/studios/{studioId}/streaming-images | Creates a streaming image resource in a studio. |
| POST | /2020-08-01/studios/{studioId}/streaming-sessions | Creates a streaming session in a studio. After invoking this operation, you must poll GetStreamingSession until the streaming session is in the READY state. |
| POST | /2020-08-01/studios/{studioId}/streaming-sessions/{sessionId}/streams | Creates a streaming session stream for a streaming session. After invoking this API, invoke GetStreamingSessionStream with the returned streamId to poll the resource until it is in the READY state. |
| POST | /2020-08-01/studios | Create a new studio. When creating a studio, two IAM roles must be provided: the admin role and the user role. These roles are assumed by your users when they log in to the Nimble Studio portal. The user role must have the AmazonNimbleStudio-StudioUser managed policy attached for the portal to function properly. The admin role must have the AmazonNimbleStudio-StudioAdmin managed policy attached for the portal to function properly. You may optionally specify a KMS key in the StudioEncryptionConfiguration. In Nimble Studio, resource names, descriptions, initialization scripts, and other data you provide are always encrypted at rest using an KMS key. By default, this key is owned by Amazon Web Services and managed on your behalf. You may provide your own KMS key when calling CreateStudio to encrypt this data using a key you own and manage. When providing an KMS key during studio creation, Nimble Studio creates KMS grants in your account to provide your studio user and admin roles access to these KMS keys. If you delete this grant, the studio will no longer be accessible to your portal users. If you delete the studio KMS key, your studio will no longer be accessible. |
| POST | /2020-08-01/studios/{studioId}/studio-components | Creates a studio component resource. |
| DELETE | /2020-08-01/studios/{studioId}/launch-profiles/{launchProfileId} | Permanently delete a launch profile. |
| DELETE | /2020-08-01/studios/{studioId}/launch-profiles/{launchProfileId}/membership/{principalId} | Delete a user from launch profile membership. |
| DELETE | /2020-08-01/studios/{studioId}/streaming-images/{streamingImageId} | Delete streaming image. |
| DELETE | /2020-08-01/studios/{studioId}/streaming-sessions/{sessionId} | Deletes streaming session resource. After invoking this operation, use GetStreamingSession to poll the resource until it transitions to a DELETED state. A streaming session will count against your streaming session quota until it is marked DELETED. |
| DELETE | /2020-08-01/studios/{studioId} | Delete a studio resource. |
| DELETE | /2020-08-01/studios/{studioId}/studio-components/{studioComponentId} | Deletes a studio component resource. |
| DELETE | /2020-08-01/studios/{studioId}/membership/{principalId} | Delete a user from studio membership. |
| GET | /2020-08-01/eulas/{eulaId} | Get EULA. |
| GET | /2020-08-01/studios/{studioId}/launch-profiles/{launchProfileId} | Get a launch profile. |
| GET | /2020-08-01/studios/{studioId}/launch-profiles/{launchProfileId}/details | Launch profile details include the launch profile resource and summary information of resources that are used by, or available to, the launch profile. This includes the name and description of all studio components used by the launch profiles, and the name and description of streaming images that can be used with this launch profile. |
| GET | /2020-08-01/studios/{studioId}/launch-profiles/{launchProfileId}/init | Get a launch profile initialization. |
| GET | /2020-08-01/studios/{studioId}/launch-profiles/{launchProfileId}/membership/{principalId} | Get a user persona in launch profile membership. |
| GET | /2020-08-01/studios/{studioId}/streaming-images/{streamingImageId} | Get streaming image. |
| GET | /2020-08-01/studios/{studioId}/streaming-sessions/{sessionId} | Gets StreamingSession resource. Invoke this operation to poll for a streaming session state while creating or deleting a session. |
| GET | /2020-08-01/studios/{studioId}/streaming-session-backups/{backupId} | Gets StreamingSessionBackup resource. Invoke this operation to poll for a streaming session backup while stopping a streaming session. |
| GET | /2020-08-01/studios/{studioId}/streaming-sessions/{sessionId}/streams/{streamId} | Gets a StreamingSessionStream for a streaming session. Invoke this operation to poll the resource after invoking CreateStreamingSessionStream. After the StreamingSessionStream changes to the READY state, the url property will contain a stream to be used with the DCV streaming client. |
| GET | /2020-08-01/studios/{studioId} | Get a studio resource. |
| GET | /2020-08-01/studios/{studioId}/studio-components/{studioComponentId} | Gets a studio component resource. |
| GET | /2020-08-01/studios/{studioId}/membership/{principalId} | Get a user's membership in a studio. |
| GET | /2020-08-01/studios/{studioId}/eula-acceptances | List EULA acceptances. |
| GET | /2020-08-01/eulas | List EULAs. |
| GET | /2020-08-01/studios/{studioId}/launch-profiles/{launchProfileId}/membership | Get all users in a given launch profile membership. |
| GET | /2020-08-01/studios/{studioId}/launch-profiles | List all the launch profiles a studio. |
| GET | /2020-08-01/studios/{studioId}/streaming-images | List the streaming image resources available to this studio. This list will contain both images provided by Amazon Web Services, as well as streaming images that you have created in your studio. |
| GET | /2020-08-01/studios/{studioId}/streaming-session-backups | Lists the backups of a streaming session in a studio. |
| GET | /2020-08-01/studios/{studioId}/streaming-sessions | Lists the streaming sessions in a studio. |
| GET | /2020-08-01/studios/{studioId}/studio-components | Lists the StudioComponents in a studio. |
| GET | /2020-08-01/studios/{studioId}/membership | Get all users in a given studio membership.   ListStudioMembers only returns admin members. |
| GET | /2020-08-01/studios | List studios in your Amazon Web Services accounts in the requested Amazon Web Services Region. |
| GET | /2020-08-01/tags/{resourceArn} | Gets the tags for a resource, given its Amazon Resource Names (ARN). This operation supports ARNs for all resource types in Nimble Studio that support tags, including studio, studio component, launch profile, streaming image, and streaming session. All resources that can be tagged will contain an ARN property, so you do not have to create this ARN yourself. |
| POST | /2020-08-01/studios/{studioId}/launch-profiles/{launchProfileId}/membership | Add/update users with given persona to launch profile membership. |
| POST | /2020-08-01/studios/{studioId}/membership | Add/update users with given persona to studio membership. |
| POST | /2020-08-01/studios/{studioId}/streaming-sessions/{sessionId}/start | Transitions sessions from the STOPPED state into the READY state. The START_IN_PROGRESS state is the intermediate state between the STOPPED and READY states. |
| PUT | /2020-08-01/studios/{studioId}/sso-configuration | Repairs the IAM Identity Center configuration for a given studio. If the studio has a valid IAM Identity Center configuration currently associated with it, this operation will fail with a validation error. If the studio does not have a valid IAM Identity Center configuration currently associated with it, then a new IAM Identity Center application is created for the studio and the studio is changed to the READY state. After the IAM Identity Center application is repaired, you must use the Amazon Nimble Studio console to add administrators and users to your studio. |
| POST | /2020-08-01/studios/{studioId}/streaming-sessions/{sessionId}/stop | Transitions sessions from the READY state into the STOPPED state. The STOP_IN_PROGRESS state is the intermediate state between the READY and STOPPED states. |
| POST | /2020-08-01/tags/{resourceArn} | Creates tags for a resource, given its ARN. |
| DELETE | /2020-08-01/tags/{resourceArn} | Deletes the tags for a resource. |
| PATCH | /2020-08-01/studios/{studioId}/launch-profiles/{launchProfileId} | Update a launch profile. |
| PATCH | /2020-08-01/studios/{studioId}/launch-profiles/{launchProfileId}/membership/{principalId} | Update a user persona in launch profile membership. |
| PATCH | /2020-08-01/studios/{studioId}/streaming-images/{streamingImageId} | Update streaming image. |
| PATCH | /2020-08-01/studios/{studioId} | Update a Studio resource. Currently, this operation only supports updating the displayName of your studio. |
| PATCH | /2020-08-01/studios/{studioId}/studio-components/{studioComponentId} | Updates a studio component resource. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a eula-acceptance?" -> POST /2020-08-01/studios/{studioId}/eula-acceptances
- "Create a launch-profile?" -> POST /2020-08-01/studios/{studioId}/launch-profiles
- "Create a streaming-image?" -> POST /2020-08-01/studios/{studioId}/streaming-images
- "Create a streaming-session?" -> POST /2020-08-01/studios/{studioId}/streaming-sessions
- "Create a stream?" -> POST /2020-08-01/studios/{studioId}/streaming-sessions/{sessionId}/streams
- "Create a studio?" -> POST /2020-08-01/studios
- "Create a studio-component?" -> POST /2020-08-01/studios/{studioId}/studio-components
- "Delete a launch-profile?" -> DELETE /2020-08-01/studios/{studioId}/launch-profiles/{launchProfileId}
- "Delete a membership?" -> DELETE /2020-08-01/studios/{studioId}/launch-profiles/{launchProfileId}/membership/{principalId}
- "Delete a streaming-image?" -> DELETE /2020-08-01/studios/{studioId}/streaming-images/{streamingImageId}
- "Delete a streaming-session?" -> DELETE /2020-08-01/studios/{studioId}/streaming-sessions/{sessionId}
- "Delete a studio?" -> DELETE /2020-08-01/studios/{studioId}
- "Delete a studio-component?" -> DELETE /2020-08-01/studios/{studioId}/studio-components/{studioComponentId}
- "Delete a membership?" -> DELETE /2020-08-01/studios/{studioId}/membership/{principalId}
- "Get eula details?" -> GET /2020-08-01/eulas/{eulaId}
- "Get launch-profile details?" -> GET /2020-08-01/studios/{studioId}/launch-profiles/{launchProfileId}
- "List all details?" -> GET /2020-08-01/studios/{studioId}/launch-profiles/{launchProfileId}/details
- "List all init?" -> GET /2020-08-01/studios/{studioId}/launch-profiles/{launchProfileId}/init
- "Get membership details?" -> GET /2020-08-01/studios/{studioId}/launch-profiles/{launchProfileId}/membership/{principalId}
- "Get streaming-image details?" -> GET /2020-08-01/studios/{studioId}/streaming-images/{streamingImageId}
- "Get streaming-session details?" -> GET /2020-08-01/studios/{studioId}/streaming-sessions/{sessionId}
- "Get streaming-session-backup details?" -> GET /2020-08-01/studios/{studioId}/streaming-session-backups/{backupId}
- "Get stream details?" -> GET /2020-08-01/studios/{studioId}/streaming-sessions/{sessionId}/streams/{streamId}
- "Get studio details?" -> GET /2020-08-01/studios/{studioId}
- "Get studio-component details?" -> GET /2020-08-01/studios/{studioId}/studio-components/{studioComponentId}
- "Get membership details?" -> GET /2020-08-01/studios/{studioId}/membership/{principalId}
- "List all eula-acceptances?" -> GET /2020-08-01/studios/{studioId}/eula-acceptances
- "List all eulas?" -> GET /2020-08-01/eulas
- "List all membership?" -> GET /2020-08-01/studios/{studioId}/launch-profiles/{launchProfileId}/membership
- "List all launch-profiles?" -> GET /2020-08-01/studios/{studioId}/launch-profiles
- "List all streaming-images?" -> GET /2020-08-01/studios/{studioId}/streaming-images
- "List all streaming-session-backups?" -> GET /2020-08-01/studios/{studioId}/streaming-session-backups
- "List all streaming-sessions?" -> GET /2020-08-01/studios/{studioId}/streaming-sessions
- "List all studio-components?" -> GET /2020-08-01/studios/{studioId}/studio-components
- "List all membership?" -> GET /2020-08-01/studios/{studioId}/membership
- "List all studios?" -> GET /2020-08-01/studios
- "Get tag details?" -> GET /2020-08-01/tags/{resourceArn}
- "Create a membership?" -> POST /2020-08-01/studios/{studioId}/launch-profiles/{launchProfileId}/membership
- "Create a membership?" -> POST /2020-08-01/studios/{studioId}/membership
- "Create a start?" -> POST /2020-08-01/studios/{studioId}/streaming-sessions/{sessionId}/start
- "Create a stop?" -> POST /2020-08-01/studios/{studioId}/streaming-sessions/{sessionId}/stop
- "Delete a tag?" -> DELETE /2020-08-01/tags/{resourceArn}
- "Partially update a launch-profile?" -> PATCH /2020-08-01/studios/{studioId}/launch-profiles/{launchProfileId}
- "Partially update a membership?" -> PATCH /2020-08-01/studios/{studioId}/launch-profiles/{launchProfileId}/membership/{principalId}
- "Partially update a streaming-image?" -> PATCH /2020-08-01/studios/{studioId}/streaming-images/{streamingImageId}
- "Partially update a studio?" -> PATCH /2020-08-01/studios/{studioId}
- "Partially update a studio-component?" -> PATCH /2020-08-01/studios/{studioId}/studio-components/{studioComponentId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
