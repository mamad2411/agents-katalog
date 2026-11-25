---
name: computer-vision-api
description: "Computer Vision API skill. Use when working with Computer Vision for models, analyze, generateThumbnail. Covers 9 endpoints."
version: 1.0.0
generator: lapsh
---

# Computer Vision API
API version: 1.0

## Auth
ApiKey Ocp-Apim-Subscription-Key in header

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /models -- verify access
3. POST /analyze -- create first analyze

## Endpoints

9 endpoints across 8 groups. See references/api-spec.lap for full details.

### models
| Method | Path | Description |
|--------|------|-------------|
| GET | /models | This operation returns the list of domain-specific models that are supported by the Computer Vision API.  Currently, the API only supports one domain-specific model: a celebrity recognizer. A successful response will be returned in JSON.  If the request failed, the response will contain an error code and a message to help understand what went wrong. |
| POST | /models/{model}/analyze | This operation recognizes content within an image by applying a domain-specific model.  The list of domain-specific models that are supported by the Computer Vision API can be retrieved using the /models GET request.  Currently, the API only provides a single domain-specific model: celebrities. Two input methods are supported -- (1) Uploading an image or (2) specifying an image URL. A successful response will be returned in JSON.  If the request failed, the response will contain an error code and a message to help understand what went wrong. |

### analyze
| Method | Path | Description |
|--------|------|-------------|
| POST | /analyze | This operation extracts a rich set of visual features based on the image content. Two input methods are supported -- (1) Uploading an image or (2) specifying an image URL.  Within your request, there is an optional parameter to allow you to choose which features to return.  By default, image categories are returned in the response. |

### generateThumbnail
| Method | Path | Description |
|--------|------|-------------|
| POST | /generateThumbnail | This operation generates a thumbnail image with the user-specified width and height. By default, the service analyzes the image, identifies the region of interest (ROI), and generates smart cropping coordinates based on the ROI. Smart cropping helps when you specify an aspect ratio that differs from that of the input image. A successful response contains the thumbnail image binary. If the request failed, the response contains an error code and a message to help determine what went wrong. |

### ocr
| Method | Path | Description |
|--------|------|-------------|
| POST | /ocr | Optical Character Recognition (OCR) detects printed text in an image and extracts the recognized characters into a machine-usable character stream.   Upon success, the OCR results will be returned. Upon failure, the error code together with an error message will be returned. The error code can be one of InvalidImageUrl, InvalidImageFormat, InvalidImageSize, NotSupportedImage,  NotSupportedLanguage, or InternalServerError. |

### describe
| Method | Path | Description |
|--------|------|-------------|
| POST | /describe | This operation generates a description of an image in human readable language with complete sentences.  The description is based on a collection of content tags, which are also returned by the operation. More than one description can be generated for each image.  Descriptions are ordered by their confidence score. All descriptions are in English. Two input methods are supported -- (1) Uploading an image or (2) specifying an image URL.A successful response will be returned in JSON.  If the request failed, the response will contain an error code and a message to help understand what went wrong. |

### tag
| Method | Path | Description |
|--------|------|-------------|
| POST | /tag | This operation generates a list of words, or tags, that are relevant to the content of the supplied image. The Computer Vision API can return tags based on objects, living beings, scenery or actions found in images. Unlike categories, tags are not organized according to a hierarchical classification system, but correspond to image content. Tags may contain hints to avoid ambiguity or provide context, for example the tag 'cello' may be accompanied by the hint 'musical instrument'. All tags are in English. |

### recognizeText
| Method | Path | Description |
|--------|------|-------------|
| POST | /recognizeText | Recognize Text operation. When you use the Recognize Text interface, the response contains a field called 'Operation-Location'. The 'Operation-Location' field contains the URL that you must use for your Get Handwritten Text Operation Result operation. |

### textOperations
| Method | Path | Description |
|--------|------|-------------|
| GET | /textOperations/{operationId} | This interface is used for getting text operation result. The URL to this interface should be retrieved from 'Operation-Location' field returned from Recognize Text interface. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all models?" -> GET /models
- "Create a analyze?" -> POST /analyze
- "Create a generateThumbnail?" -> POST /generateThumbnail
- "Create a ocr?" -> POST /ocr
- "Create a describe?" -> POST /describe
- "Create a tag?" -> POST /tag
- "Create a analyze?" -> POST /models/{model}/analyze
- "Create a recognizeText?" -> POST /recognizeText
- "Get textOperation details?" -> GET /textOperations/{operationId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
