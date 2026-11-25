---
name: amazon-polly
description: "Amazon Polly API skill. Use when working with Amazon Polly for lexicons, voices, synthesisTasks. Covers 9 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Polly
API version: 2016-06-10

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /v1/voices -- verify access
3. POST /v1/synthesisTasks -- create first synthesisTasks

## Endpoints

9 endpoints across 4 groups. See references/api-spec.lap for full details.

### lexicons
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /v1/lexicons/{LexiconName} | Deletes the specified pronunciation lexicon stored in an Amazon Web Services Region. A lexicon which has been deleted is not available for speech synthesis, nor is it possible to retrieve it using either the GetLexicon or ListLexicon APIs. For more information, see Managing Lexicons. |
| GET | /v1/lexicons/{LexiconName} | Returns the content of the specified pronunciation lexicon stored in an Amazon Web Services Region. For more information, see Managing Lexicons. |
| GET | /v1/lexicons | Returns a list of pronunciation lexicons stored in an Amazon Web Services Region. For more information, see Managing Lexicons. |
| PUT | /v1/lexicons/{LexiconName} | Stores a pronunciation lexicon in an Amazon Web Services Region. If a lexicon with the same name already exists in the region, it is overwritten by the new lexicon. Lexicon operations have eventual consistency, therefore, it might take some time before the lexicon is available to the SynthesizeSpeech operation. For more information, see Managing Lexicons. |

### voices
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/voices | Returns the list of voices that are available for use when requesting speech synthesis. Each voice speaks a specified language, is either male or female, and is identified by an ID, which is the ASCII version of the voice name.  When synthesizing speech ( SynthesizeSpeech ), you provide the voice ID for the voice you want from the list of voices returned by DescribeVoices. For example, you want your news reader application to read news in a specific language, but giving a user the option to choose the voice. Using the DescribeVoices operation you can provide the user with a list of available voices to select from.  You can optionally specify a language code to filter the available voices. For example, if you specify en-US, the operation returns a list of all available US English voices.  This operation requires permissions to perform the polly:DescribeVoices action. |

### synthesisTasks
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/synthesisTasks/{TaskId} | Retrieves a specific SpeechSynthesisTask object based on its TaskID. This object contains information about the given speech synthesis task, including the status of the task, and a link to the S3 bucket containing the output of the task. |
| GET | /v1/synthesisTasks | Returns a list of SpeechSynthesisTask objects ordered by their creation date. This operation can filter the tasks by their status, for example, allowing users to list only tasks that are completed. |
| POST | /v1/synthesisTasks | Allows the creation of an asynchronous synthesis task, by starting a new SpeechSynthesisTask. This operation requires all the standard information needed for speech synthesis, plus the name of an Amazon S3 bucket for the service to store the output of the synthesis task and two optional parameters (OutputS3KeyPrefix and SnsTopicArn). Once the synthesis task is created, this operation will return a SpeechSynthesisTask object, which will include an identifier of this task as well as the current status. The SpeechSynthesisTask object is available for 72 hours after starting the asynchronous synthesis task. |

### speech
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/speech | Synthesizes UTF-8 input, plain text or SSML, to a stream of bytes. SSML input must be valid, well-formed SSML. Some alphabets might not be available with all the voices (for example, Cyrillic might not be read at all by English voices) unless phoneme mapping is used. For more information, see How it Works. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Delete a lexicon?" -> DELETE /v1/lexicons/{LexiconName}
- "List all voices?" -> GET /v1/voices
- "Get lexicon details?" -> GET /v1/lexicons/{LexiconName}
- "Get synthesisTask details?" -> GET /v1/synthesisTasks/{TaskId}
- "List all lexicons?" -> GET /v1/lexicons
- "List all synthesisTasks?" -> GET /v1/synthesisTasks
- "Update a lexicon?" -> PUT /v1/lexicons/{LexiconName}
- "Create a synthesisTask?" -> POST /v1/synthesisTasks
- "Create a speech?" -> POST /v1/speech
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
