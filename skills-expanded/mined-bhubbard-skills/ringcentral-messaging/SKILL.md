---
name: ringcentral-messaging
description: "Sending SMS, Fax, and interacting with Team Messaging via the RingCentral API"
---

# RingCentral Messaging Skill

This skill covers the capabilities of the RingCentral API related to asynchronous communication, including SMS, MMS, Fax, and Team Messaging.

## SMS and MMS API
RingCentral allows you to send and receive text and multimedia messages.
- **Endpoint**: `POST /restapi/v1.0/account/~/extension/~/sms`
- **Payload**: Requires `from` (a valid RingCentral phone number assigned to the extension), `to` (array of recipients), and `text`.
- **MMS**: To send media, use `multipart/form-data` encoding and attach files along with the JSON payload.
- **Compliance**: Be aware of A2P 10DLC compliance rules when sending SMS programmatically.

## Fax API
Send and receive faxes purely via the REST API without physical hardware.
- **Endpoint**: `POST /restapi/v1.0/account/~/extension/~/fax`
- **Payload**: Sent as `multipart/form-data`. Provide `to` (fax number) and the document as an attachment (e.g., PDF, DOCX).
- **Status Checking**: Use the Message Store API (`GET /restapi/v1.0/account/~/extension/~/message-store/{messageId}`) to check if a fax was sent successfully.

## Team Messaging (Glip)
Integrate with RingCentral's Team Messaging platform to send notifications, create teams, and interact with chat via bots.
- **Endpoints**: Base path is typically `/restapi/v1.0/glip/`.
- **Posting Messages**: `POST /restapi/v1.0/glip/chats/{chatId}/posts`. You can send plain text or structured cards.
- **Webhooks**: Use Glip webhooks to receive real-time notifications about new posts or events in a team.

## Best Practices
- Respect rate limits. The Messaging APIs have specific tier limits (e.g., Heavy vs. Light API calls).
- For inbound SMS/Fax, set up Webhooks instead of polling the Message Store.
