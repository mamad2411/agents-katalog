---
name: amazon-lex-runtime-service
description: "Amazon Lex Runtime Service API skill. Use when working with Amazon Lex Runtime Service for bot. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Lex Runtime Service
API version: 2016-11-28

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /bot/{botName}/alias/{botAlias}/user/{userId}/session/ -- verify access
3. POST /bot/{botName}/alias/{botAlias}/user/{userId}/content -- create first content

## Endpoints

5 endpoints across 1 groups. See references/api-spec.lap for full details.

### bot
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /bot/{botName}/alias/{botAlias}/user/{userId}/session | Removes session information for a specified bot, alias, and user ID. |
| GET | /bot/{botName}/alias/{botAlias}/user/{userId}/session/ | Returns session information for a specified bot, alias, and user ID. |
| POST | /bot/{botName}/alias/{botAlias}/user/{userId}/content | Sends user input (text or speech) to Amazon Lex. Clients use this API to send text and audio requests to Amazon Lex at runtime. Amazon Lex interprets the user input using the machine learning model that it built for the bot.  The PostContent operation supports audio input at 8kHz and 16kHz. You can use 8kHz audio to achieve higher speech recognition accuracy in telephone audio applications.   In response, Amazon Lex returns the next message to convey to the user. Consider the following example messages:     For a user input "I would like a pizza," Amazon Lex might return a response with a message eliciting slot data (for example, PizzaSize): "What size pizza would you like?".     After the user provides all of the pizza order information, Amazon Lex might return a response with a message to get user confirmation: "Order the pizza?".     After the user replies "Yes" to the confirmation prompt, Amazon Lex might return a conclusion statement: "Thank you, your cheese pizza has been ordered.".     Not all Amazon Lex messages require a response from the user. For example, conclusion statements do not require a response. Some messages require only a yes or no response. In addition to the message, Amazon Lex provides additional context about the message in the response that you can use to enhance client behavior, such as displaying the appropriate client user interface. Consider the following examples:     If the message is to elicit slot data, Amazon Lex returns the following context information:     x-amz-lex-dialog-state header set to ElicitSlot     x-amz-lex-intent-name header set to the intent name in the current context     x-amz-lex-slot-to-elicit header set to the slot name for which the message is eliciting information     x-amz-lex-slots header set to a map of slots configured for the intent with their current values       If the message is a confirmation prompt, the x-amz-lex-dialog-state header is set to Confirmation and the x-amz-lex-slot-to-elicit header is omitted.     If the message is a clarification prompt configured for the intent, indicating that the user intent is not understood, the x-amz-dialog-state header is set to ElicitIntent and the x-amz-slot-to-elicit header is omitted.     In addition, Amazon Lex also returns your application-specific sessionAttributes. For more information, see Managing Conversation Context. |
| POST | /bot/{botName}/alias/{botAlias}/user/{userId}/text | Sends user input to Amazon Lex. Client applications can use this API to send requests to Amazon Lex at runtime. Amazon Lex then interprets the user input using the machine learning model it built for the bot.   In response, Amazon Lex returns the next message to convey to the user an optional responseCard to display. Consider the following example messages:     For a user input "I would like a pizza", Amazon Lex might return a response with a message eliciting slot data (for example, PizzaSize): "What size pizza would you like?"     After the user provides all of the pizza order information, Amazon Lex might return a response with a message to obtain user confirmation "Proceed with the pizza order?".     After the user replies to a confirmation prompt with a "yes", Amazon Lex might return a conclusion statement: "Thank you, your cheese pizza has been ordered.".     Not all Amazon Lex messages require a user response. For example, a conclusion statement does not require a response. Some messages require only a "yes" or "no" user response. In addition to the message, Amazon Lex provides additional context about the message in the response that you might use to enhance client behavior, for example, to display the appropriate client user interface. These are the slotToElicit, dialogState, intentName, and slots fields in the response. Consider the following examples:    If the message is to elicit slot data, Amazon Lex returns the following context information:    dialogState set to ElicitSlot     intentName set to the intent name in the current context     slotToElicit set to the slot name for which the message is eliciting information     slots set to a map of slots, configured for the intent, with currently known values       If the message is a confirmation prompt, the dialogState is set to ConfirmIntent and SlotToElicit is set to null.    If the message is a clarification prompt (configured for the intent) that indicates that user intent is not understood, the dialogState is set to ElicitIntent and slotToElicit is set to null.     In addition, Amazon Lex also returns your application-specific sessionAttributes. For more information, see Managing Conversation Context. |
| POST | /bot/{botName}/alias/{botAlias}/user/{userId}/session | Creates a new session or modifies an existing session with an Amazon Lex bot. Use this operation to enable your application to set the state of the bot. For more information, see Managing Sessions. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all session?" -> GET /bot/{botName}/alias/{botAlias}/user/{userId}/session/
- "Create a content?" -> POST /bot/{botName}/alias/{botAlias}/user/{userId}/content
- "Create a text?" -> POST /bot/{botName}/alias/{botAlias}/user/{userId}/text
- "Create a session?" -> POST /bot/{botName}/alias/{botAlias}/user/{userId}/session
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
