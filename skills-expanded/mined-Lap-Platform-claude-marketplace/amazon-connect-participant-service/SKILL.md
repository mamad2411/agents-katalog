---
name: amazon-connect-participant-service
description: "Amazon Connect Participant Service API skill. Use when working with Amazon Connect Participant Service for participant. Covers 9 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Connect Participant Service
API version: 2018-09-07

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /participant/views/{ViewToken} -- verify access
3. POST /participant/complete-attachment-upload -- create first complete-attachment-upload

## Endpoints

9 endpoints across 1 groups. See references/api-spec.lap for full details.

### participant
| Method | Path | Description |
|--------|------|-------------|
| POST | /participant/complete-attachment-upload | Allows you to confirm that the attachment has been uploaded using the pre-signed URL provided in StartAttachmentUpload API. A conflict exception is thrown when an attachment with that identifier is already being uploaded.   ConnectionToken is used for invoking this API instead of ParticipantToken.  The Amazon Connect Participant Service APIs do not use Signature Version 4 authentication. |
| POST | /participant/connection | Creates the participant's connection.    ParticipantToken is used for invoking this API instead of ConnectionToken.  The participant token is valid for the lifetime of the participant – until they are part of a contact. The response URL for WEBSOCKET Type has a connect expiry timeout of 100s. Clients must manually connect to the returned websocket URL and subscribe to the desired topic.  For chat, you need to publish the following on the established websocket connection:  {"topic":"aws/subscribe","content":{"topics":["aws/chat"]}}  Upon websocket URL expiry, as specified in the response ConnectionExpiry parameter, clients need to call this API again to obtain a new websocket URL and perform the same steps as before.  Message streaming support: This API can also be used together with the StartContactStreaming API to create a participant connection for chat contacts that are not using a websocket. For more information about message streaming, Enable real-time chat message streaming in the Amazon Connect Administrator Guide.  Feature specifications: For information about feature specifications, such as the allowed number of open websocket connections per participant, see Feature specifications in the Amazon Connect Administrator Guide.   The Amazon Connect Participant Service APIs do not use Signature Version 4 authentication. |
| GET | /participant/views/{ViewToken} | Retrieves the view for the specified view token. |
| POST | /participant/disconnect | Disconnects a participant.    ConnectionToken is used for invoking this API instead of ParticipantToken.  The Amazon Connect Participant Service APIs do not use Signature Version 4 authentication. |
| POST | /participant/attachment | Provides a pre-signed URL for download of a completed attachment. This is an asynchronous API for use with active contacts.   ConnectionToken is used for invoking this API instead of ParticipantToken.  The Amazon Connect Participant Service APIs do not use Signature Version 4 authentication. |
| POST | /participant/transcript | Retrieves a transcript of the session, including details about any attachments. For information about accessing past chat contact transcripts for a persistent chat, see Enable persistent chat.  If you have a process that consumes events in the transcript of an chat that has ended, note that chat transcripts contain the following event content types if the event has occurred during the chat session:    application/vnd.amazonaws.connect.event.participant.left     application/vnd.amazonaws.connect.event.participant.joined     application/vnd.amazonaws.connect.event.chat.ended     application/vnd.amazonaws.connect.event.transfer.succeeded     application/vnd.amazonaws.connect.event.transfer.failed      ConnectionToken is used for invoking this API instead of ParticipantToken.  The Amazon Connect Participant Service APIs do not use Signature Version 4 authentication. |
| POST | /participant/event | The application/vnd.amazonaws.connect.event.connection.acknowledged ContentType will no longer be supported starting December 31, 2024. This event has been migrated to the CreateParticipantConnection API using the ConnectParticipant field.  Sends an event. Message receipts are not supported when there are more than two active participants in the chat. Using the SendEvent API for message receipts when a supervisor is barged-in will result in a conflict exception.   ConnectionToken is used for invoking this API instead of ParticipantToken.  The Amazon Connect Participant Service APIs do not use Signature Version 4 authentication. |
| POST | /participant/message | Sends a message.   ConnectionToken is used for invoking this API instead of ParticipantToken.  The Amazon Connect Participant Service APIs do not use Signature Version 4 authentication. |
| POST | /participant/start-attachment-upload | Provides a pre-signed Amazon S3 URL in response for uploading the file directly to S3.   ConnectionToken is used for invoking this API instead of ParticipantToken.  The Amazon Connect Participant Service APIs do not use Signature Version 4 authentication. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a complete-attachment-upload?" -> POST /participant/complete-attachment-upload
- "Create a connection?" -> POST /participant/connection
- "Get view details?" -> GET /participant/views/{ViewToken}
- "Create a disconnect?" -> POST /participant/disconnect
- "Create a attachment?" -> POST /participant/attachment
- "Create a transcript?" -> POST /participant/transcript
- "Create a event?" -> POST /participant/event
- "Create a message?" -> POST /participant/message
- "Create a start-attachment-upload?" -> POST /participant/start-attachment-upload
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
