---
name: amazon-lex-runtime-v2
description: "Amazon Lex Runtime V2 API skill. Use when working with Amazon Lex Runtime V2 for bots. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Lex Runtime V2
API version: 2020-08-07

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /bots/{botId}/botAliases/{botAliasId}/botLocales/{localeId}/sessions/{sessionId} -- verify access
3. POST /bots/{botId}/botAliases/{botAliasId}/botLocales/{localeId}/sessions/{sessionId} -- create first sessions

## Endpoints

5 endpoints across 1 groups. See references/api-spec.lap for full details.

### bots
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /bots/{botId}/botAliases/{botAliasId}/botLocales/{localeId}/sessions/{sessionId} | Removes session information for a specified bot, alias, and user ID.  You can use this operation to restart a conversation with a bot. When you remove a session, the entire history of the session is removed so that you can start again. You don't need to delete a session. Sessions have a time limit and will expire. Set the session time limit when you create the bot. The default is 5 minutes, but you can specify anything between 1 minute and 24 hours. If you specify a bot or alias ID that doesn't exist, you receive a BadRequestException.  If the locale doesn't exist in the bot, or if the locale hasn't been enables for the alias, you receive a BadRequestException. |
| GET | /bots/{botId}/botAliases/{botAliasId}/botLocales/{localeId}/sessions/{sessionId} | Returns session information for a specified bot, alias, and user. For example, you can use this operation to retrieve session information for a user that has left a long-running session in use. If the bot, alias, or session identifier doesn't exist, Amazon Lex V2 returns a BadRequestException. If the locale doesn't exist or is not enabled for the alias, you receive a BadRequestException. |
| POST | /bots/{botId}/botAliases/{botAliasId}/botLocales/{localeId}/sessions/{sessionId} | Creates a new session or modifies an existing session with an Amazon Lex V2 bot. Use this operation to enable your application to set the state of the bot. |
| POST | /bots/{botId}/botAliases/{botAliasId}/botLocales/{localeId}/sessions/{sessionId}/text | Sends user input to Amazon Lex V2. Client applications use this API to send requests to Amazon Lex V2 at runtime. Amazon Lex V2 then interprets the user input using the machine learning model that it build for the bot. In response, Amazon Lex V2 returns the next message to convey to the user and an optional response card to display. If the optional post-fulfillment response is specified, the messages are returned as follows. For more information, see PostFulfillmentStatusSpecification.    Success message - Returned if the Lambda function completes successfully and the intent state is fulfilled or ready fulfillment if the message is present.    Failed message - The failed message is returned if the Lambda function throws an exception or if the Lambda function returns a failed intent state without a message.    Timeout message - If you don't configure a timeout message and a timeout, and the Lambda function doesn't return within 30 seconds, the timeout message is returned. If you configure a timeout, the timeout message is returned when the period times out.    For more information, see Completion message. |
| POST | /bots/{botId}/botAliases/{botAliasId}/botLocales/{localeId}/sessions/{sessionId}/utterance | Sends user input to Amazon Lex V2. You can send text or speech. Clients use this API to send text and audio requests to Amazon Lex V2 at runtime. Amazon Lex V2 interprets the user input using the machine learning model built for the bot. The following request fields must be compressed with gzip and then base64 encoded before you send them to Amazon Lex V2.    requestAttributes   sessionState   The following response fields are compressed using gzip and then base64 encoded by Amazon Lex V2. Before you can use these fields, you must decode and decompress them.    inputTranscript   interpretations   messages   requestAttributes   sessionState   The example contains a Java application that compresses and encodes a Java object to send to Amazon Lex V2, and a second that decodes and decompresses a response from Amazon Lex V2. If the optional post-fulfillment response is specified, the messages are returned as follows. For more information, see PostFulfillmentStatusSpecification.    Success message - Returned if the Lambda function completes successfully and the intent state is fulfilled or ready fulfillment if the message is present.    Failed message - The failed message is returned if the Lambda function throws an exception or if the Lambda function returns a failed intent state without a message.    Timeout message - If you don't configure a timeout message and a timeout, and the Lambda function doesn't return within 30 seconds, the timeout message is returned. If you configure a timeout, the timeout message is returned when the period times out.    For more information, see Completion message. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Delete a session?" -> DELETE /bots/{botId}/botAliases/{botAliasId}/botLocales/{localeId}/sessions/{sessionId}
- "Get session details?" -> GET /bots/{botId}/botAliases/{botAliasId}/botLocales/{localeId}/sessions/{sessionId}
- "Create a text?" -> POST /bots/{botId}/botAliases/{botAliasId}/botLocales/{localeId}/sessions/{sessionId}/text
- "Create a utterance?" -> POST /bots/{botId}/botAliases/{botAliasId}/botLocales/{localeId}/sessions/{sessionId}/utterance
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
