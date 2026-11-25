---
name: amazon-sagemaker-runtime
description: "Amazon SageMaker Runtime API skill. Use when working with Amazon SageMaker Runtime for endpoints. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon SageMaker Runtime
API version: 2017-05-13

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST /endpoints/{EndpointName}/invocations -- create first invocations

## Endpoints

3 endpoints across 1 groups. See references/api-spec.lap for full details.

### endpoints
| Method | Path | Description |
|--------|------|-------------|
| POST | /endpoints/{EndpointName}/invocations | After you deploy a model into production using Amazon SageMaker hosting services, your client applications use this API to get inferences from the model hosted at the specified endpoint.  For an overview of Amazon SageMaker, see How It Works.  Amazon SageMaker strips all POST headers except those supported by the API. Amazon SageMaker might add additional headers. You should not rely on the behavior of headers outside those enumerated in the request syntax.  Calls to InvokeEndpoint are authenticated by using Amazon Web Services Signature Version 4. For information, see Authenticating Requests (Amazon Web Services Signature Version 4) in the Amazon S3 API Reference. A customer's model containers must respond to requests within 60 seconds. The model itself can have a maximum processing time of 60 seconds before responding to invocations. If your model is going to take 50-60 seconds of processing time, the SDK socket timeout should be set to be 70 seconds.  Endpoints are scoped to an individual account, and are not public. The URL does not contain the account ID, but Amazon SageMaker determines the account ID from the authentication token that is supplied by the caller. |
| POST | /endpoints/{EndpointName}/async-invocations | After you deploy a model into production using Amazon SageMaker hosting services, your client applications use this API to get inferences from the model hosted at the specified endpoint in an asynchronous manner. Inference requests sent to this API are enqueued for asynchronous processing. The processing of the inference request may or may not complete before you receive a response from this API. The response from this API will not contain the result of the inference request but contain information about where you can locate it. Amazon SageMaker strips all POST headers except those supported by the API. Amazon SageMaker might add additional headers. You should not rely on the behavior of headers outside those enumerated in the request syntax.  Calls to InvokeEndpointAsync are authenticated by using Amazon Web Services Signature Version 4. For information, see Authenticating Requests (Amazon Web Services Signature Version 4) in the Amazon S3 API Reference. |
| POST | /endpoints/{EndpointName}/invocations-response-stream | Invokes a model at the specified endpoint to return the inference response as a stream. The inference stream provides the response payload incrementally as a series of parts. Before you can get an inference stream, you must have access to a model that's deployed using Amazon SageMaker hosting services, and the container for that model must support inference streaming. For more information that can help you use this API, see the following sections in the Amazon SageMaker Developer Guide:   For information about how to add streaming support to a model, see How Containers Serve Requests.   For information about how to process the streaming response, see Invoke real-time endpoints.   Before you can use this operation, your IAM permissions must allow the sagemaker:InvokeEndpoint action. For more information about Amazon SageMaker actions for IAM policies, see Actions, resources, and condition keys for Amazon SageMaker in the IAM Service Authorization Reference. Amazon SageMaker strips all POST headers except those supported by the API. Amazon SageMaker might add additional headers. You should not rely on the behavior of headers outside those enumerated in the request syntax.  Calls to InvokeEndpointWithResponseStream are authenticated by using Amazon Web Services Signature Version 4. For information, see Authenticating Requests (Amazon Web Services Signature Version 4) in the Amazon S3 API Reference. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a invocation?" -> POST /endpoints/{EndpointName}/invocations
- "Create a async-invocation?" -> POST /endpoints/{EndpointName}/async-invocations
- "Create a invocations-response-stream?" -> POST /endpoints/{EndpointName}/invocations-response-stream
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object
- Error responses use types: InternalStreamFailure, ModelStreamError

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
