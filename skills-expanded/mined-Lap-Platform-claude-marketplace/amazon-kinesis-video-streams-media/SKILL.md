---
name: amazon-kinesis-video-streams-media
description: "Amazon Kinesis Video Streams Media API skill. Use when working with Amazon Kinesis Video Streams Media for getMedia. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Amazon Kinesis Video Streams Media
API version: 2017-09-30

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST /getMedia -- create first getMedia

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### getMedia
| Method | Path | Description |
|--------|------|-------------|
| POST | /getMedia | Use this API to retrieve media content from a Kinesis video stream. In the request, you identify the stream name or stream Amazon Resource Name (ARN), and the starting chunk. Kinesis Video Streams then returns a stream of chunks in order by fragment number.  You must first call the GetDataEndpoint API to get an endpoint. Then send the GetMedia requests to this endpoint using the --endpoint-url parameter.   When you put media data (fragments) on a stream, Kinesis Video Streams stores each incoming fragment and related metadata in what is called a "chunk." For more information, see PutMedia. The GetMedia API returns a stream of these chunks starting from the chunk that you specify in the request.  The following limits apply when using the GetMedia API:   A client can call GetMedia up to five times per second per stream.    Kinesis Video Streams sends media data at a rate of up to 25 megabytes per second (or 200 megabits per second) during a GetMedia session.     If an error is thrown after invoking a Kinesis Video Streams media API, in addition to the HTTP status code and the response body, it includes the following pieces of information:     x-amz-ErrorType HTTP header – contains a more specific error type in addition to what the HTTP status code provides.     x-amz-RequestId HTTP header – if you want to report an issue to AWS, the support team can better diagnose the problem if given the Request Id.   Both the HTTP status code and the ErrorType header can be utilized to make programmatic decisions about whether errors are retry-able and under what conditions, as well as provide information on what actions the client programmer might need to take in order to successfully try again. For more information, see the Errors section at the bottom of this topic, as well as Common Errors. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a getMedia?" -> POST /getMedia
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
