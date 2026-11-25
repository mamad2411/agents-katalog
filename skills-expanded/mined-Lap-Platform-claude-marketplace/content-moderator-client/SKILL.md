---
name: content-moderator-client
description: "Content Moderator Client API skill. Use when working with Content Moderator Client for contentmoderator. Covers 35 endpoints."
version: 1.0.0
generator: lapsh
---

# Content Moderator Client
API version: 1.0

## Auth
ApiKey Ocp-Apim-Subscription-Key in header

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /contentmoderator/lists/v1.0/imagelists -- verify access
3. POST /contentmoderator/moderate/v1.0/ProcessImage/FindFaces -- create first FindFaces

## Endpoints

35 endpoints across 1 groups. See references/api-spec.lap for full details.

### contentmoderator
| Method | Path | Description |
|--------|------|-------------|
| POST | /contentmoderator/moderate/v1.0/ProcessImage/FindFaces | Returns the list of faces found. |
| POST | /contentmoderator/moderate/v1.0/ProcessImage/OCR | Returns any text found in the image for the specified language. If no language is specified in the input, the detection defaults to English. |
| POST | /contentmoderator/moderate/v1.0/ProcessImage/Evaluate | Returns probabilities of the image containing racy or adult content. |
| POST | /contentmoderator/moderate/v1.0/ProcessImage/Match | Fuzzily match an image against one of your custom image lists. You can create and manage your custom image lists by using <a href="/docs/services/578ff44d2703741568569ab9/operations/578ff7b12703741568569abe">this API</a>. |
| POST | /contentmoderator/moderate/v1.0/ProcessText/Screen/ | Detect profanity and match against custom and shared blocklists |
| POST | /contentmoderator/moderate/v1.0/ProcessText/DetectLanguage | This operation detects the language of input content. It returns the <a href="http://www-01.sil.org/iso639-3/codes.asp">ISO 639-3 code</a> for the predominant language in the submitted text. More than 110 languages are supported. |
| GET | /contentmoderator/lists/v1.0/imagelists/{listId} | Returns the details of the image list with listId equal to the passed list ID. |
| DELETE | /contentmoderator/lists/v1.0/imagelists/{listId} | Deletes the image list with listId equal to the passed list ID. |
| PUT | /contentmoderator/lists/v1.0/imagelists/{listId} | Updates an image list with listId equal to the passed list ID. |
| POST | /contentmoderator/lists/v1.0/imagelists | Creates an image list. |
| GET | /contentmoderator/lists/v1.0/imagelists | Gets all the image lists. |
| POST | /contentmoderator/lists/v1.0/imagelists/{listId}/RefreshIndex | Refreshes the index of the list with listId equal to the passed list ID. |
| GET | /contentmoderator/lists/v1.0/termlists/{listId} | Returns list ID details of the term list with listId equal to the passed list ID. |
| DELETE | /contentmoderator/lists/v1.0/termlists/{listId} | Deletes the term list with listId equal to the passed list ID. |
| PUT | /contentmoderator/lists/v1.0/termlists/{listId} | Updates a term list. |
| POST | /contentmoderator/lists/v1.0/termlists | Creates a term list. |
| GET | /contentmoderator/lists/v1.0/termlists | Gets all the term lists. |
| POST | /contentmoderator/lists/v1.0/termlists/{listId}/RefreshIndex | Refreshes the index of the list with listId equal to the passed list ID. |
| POST | /contentmoderator/lists/v1.0/imagelists/{listId}/images | Add an image to the list with listId equal to the passed list ID. |
| DELETE | /contentmoderator/lists/v1.0/imagelists/{listId}/images | Deletes all images from the list with listId equal to the passed list ID. |
| GET | /contentmoderator/lists/v1.0/imagelists/{listId}/images | Gets all image IDs from the list with listId equal to the passed list ID. |
| DELETE | /contentmoderator/lists/v1.0/imagelists/{listId}/images/{ImageId} | Deletes an image from the list with the passed list ID and image ID. |
| POST | /contentmoderator/lists/v1.0/termlists/{listId}/terms/{term} | Adds a term to the term list with listId equal to the passed list ID. |
| DELETE | /contentmoderator/lists/v1.0/termlists/{listId}/terms/{term} | Deletes a term from the list with listId equal to the passed list ID. |
| GET | /contentmoderator/lists/v1.0/termlists/{listId}/terms | Gets all terms from the list with listId equal to the passed list ID. |
| DELETE | /contentmoderator/lists/v1.0/termlists/{listId}/terms | Deletes all terms from the list with listId equal to the passed list ID. |
| GET | /contentmoderator/review/v1.0/teams/{teamName}/reviews/{reviewId} | Returns review details for the passed review ID. |
| GET | /contentmoderator/review/v1.0/teams/{teamName}/jobs/{JobId} | Get the job details for a job ID. |
| POST | /contentmoderator/review/v1.0/teams/{teamName}/reviews | The created reviews appear for reviewers on your team. As reviewers finish reviewing, results of the reviews are posted (that is, HTTP POST) on the specified CallBackEndpoint value. |
| POST | /contentmoderator/review/v1.0/teams/{teamName}/jobs | A job ID will be returned for the content posted on this endpoint. |
| POST | /contentmoderator/review/v1.0/teams/{teamName}/reviews/{reviewId}/frames | The created reviews appear for reviewers on your team. As reviewers finish reviewing, results of the reviews are posted (that is, HTTP POST) on the specified CallBackEndpoint value. |
| GET | /contentmoderator/review/v1.0/teams/{teamName}/reviews/{reviewId}/frames | The created reviews appear for reviewers on your team. As reviewers finish reviewing, results of the reviews are posted (that is, HTTP POST) on the specified CallBackEndpoint value. |
| POST | /contentmoderator/review/v1.0/teams/{teamName}/reviews/{reviewId}/publish | Publish a video review. |
| PUT | /contentmoderator/review/v1.0/teams/{teamName}/reviews/{reviewId}/transcriptmoderationresult | This API adds a transcript screen text result file for a video review. The transcript screen text result file is a result of the Screen Text API. To generate a transcript screen text result file, you must screen a transcript file for profanity by using the Screen Text API. |
| PUT | /contentmoderator/review/v1.0/teams/{teamName}/reviews/{reviewId}/transcript | This API adds a transcript file (text version of all the words spoken in a video) to a video review. The file should be in a valid WebVTT format. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a FindFace?" -> POST /contentmoderator/moderate/v1.0/ProcessImage/FindFaces
- "Create a OCR?" -> POST /contentmoderator/moderate/v1.0/ProcessImage/OCR
- "Create a Evaluate?" -> POST /contentmoderator/moderate/v1.0/ProcessImage/Evaluate
- "Create a Match?" -> POST /contentmoderator/moderate/v1.0/ProcessImage/Match
- "Create a Screen?" -> POST /contentmoderator/moderate/v1.0/ProcessText/Screen/
- "Create a DetectLanguage?" -> POST /contentmoderator/moderate/v1.0/ProcessText/DetectLanguage
- "Get imagelist details?" -> GET /contentmoderator/lists/v1.0/imagelists/{listId}
- "Delete a imagelist?" -> DELETE /contentmoderator/lists/v1.0/imagelists/{listId}
- "Update a imagelist?" -> PUT /contentmoderator/lists/v1.0/imagelists/{listId}
- "Create a imagelist?" -> POST /contentmoderator/lists/v1.0/imagelists
- "List all imagelists?" -> GET /contentmoderator/lists/v1.0/imagelists
- "Create a RefreshIndex?" -> POST /contentmoderator/lists/v1.0/imagelists/{listId}/RefreshIndex
- "Get termlist details?" -> GET /contentmoderator/lists/v1.0/termlists/{listId}
- "Delete a termlist?" -> DELETE /contentmoderator/lists/v1.0/termlists/{listId}
- "Update a termlist?" -> PUT /contentmoderator/lists/v1.0/termlists/{listId}
- "Create a termlist?" -> POST /contentmoderator/lists/v1.0/termlists
- "List all termlists?" -> GET /contentmoderator/lists/v1.0/termlists
- "Create a RefreshIndex?" -> POST /contentmoderator/lists/v1.0/termlists/{listId}/RefreshIndex
- "Create a image?" -> POST /contentmoderator/lists/v1.0/imagelists/{listId}/images
- "List all images?" -> GET /contentmoderator/lists/v1.0/imagelists/{listId}/images
- "Delete a image?" -> DELETE /contentmoderator/lists/v1.0/imagelists/{listId}/images/{ImageId}
- "Delete a term?" -> DELETE /contentmoderator/lists/v1.0/termlists/{listId}/terms/{term}
- "List all terms?" -> GET /contentmoderator/lists/v1.0/termlists/{listId}/terms
- "Get review details?" -> GET /contentmoderator/review/v1.0/teams/{teamName}/reviews/{reviewId}
- "Get job details?" -> GET /contentmoderator/review/v1.0/teams/{teamName}/jobs/{JobId}
- "Create a review?" -> POST /contentmoderator/review/v1.0/teams/{teamName}/reviews
- "Create a job?" -> POST /contentmoderator/review/v1.0/teams/{teamName}/jobs
- "Create a frame?" -> POST /contentmoderator/review/v1.0/teams/{teamName}/reviews/{reviewId}/frames
- "List all frames?" -> GET /contentmoderator/review/v1.0/teams/{teamName}/reviews/{reviewId}/frames
- "Create a publish?" -> POST /contentmoderator/review/v1.0/teams/{teamName}/reviews/{reviewId}/publish
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
