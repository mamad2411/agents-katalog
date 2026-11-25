---
name: httpbinorg
description: "httpbin.org API skill. Use when working with httpbin.org for absolute-redirect, anything, base64. Covers 73 endpoints."
version: 1.0.0
generator: lapsh
---

# httpbin.org
API version: 0.9.2

## Auth
ApiKey Authorization in header

## Base URL
https://httpbin.org/

## Setup
1. Set your API key in the appropriate header
2. GET /anything -- verify access
3. POST /anything -- create first anything

## Endpoints

73 endpoints across 41 groups. See references/api-spec.lap for full details.

### absolute-redirect
| Method | Path | Description |
|--------|------|-------------|
| GET | /absolute-redirect/{n} | Absolutely 302 Redirects n times. |

### anything
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /anything | Returns anything passed in request data. |
| GET | /anything | Returns anything passed in request data. |
| PATCH | /anything | Returns anything passed in request data. |
| POST | /anything | Returns anything passed in request data. |
| PUT | /anything | Returns anything passed in request data. |
| DELETE | /anything/{anything} | Returns anything passed in request data. |
| GET | /anything/{anything} | Returns anything passed in request data. |
| PATCH | /anything/{anything} | Returns anything passed in request data. |
| POST | /anything/{anything} | Returns anything passed in request data. |
| PUT | /anything/{anything} | Returns anything passed in request data. |

### base64
| Method | Path | Description |
|--------|------|-------------|
| GET | /base64/{value} | Decodes base64url-encoded string. |

### basic-auth
| Method | Path | Description |
|--------|------|-------------|
| GET | /basic-auth/{user}/{passwd} | Prompts the user for authorization using HTTP Basic Auth. |

### bearer
| Method | Path | Description |
|--------|------|-------------|
| GET | /bearer | Prompts the user for authorization using bearer authentication. |

### brotli
| Method | Path | Description |
|--------|------|-------------|
| GET | /brotli | Returns Brotli-encoded data. |

### bytes
| Method | Path | Description |
|--------|------|-------------|
| GET | /bytes/{n} | Returns n random bytes generated with given seed |

### cache
| Method | Path | Description |
|--------|------|-------------|
| GET | /cache | Returns a 304 if an If-Modified-Since header or If-None-Match is present. Returns the same as a GET otherwise. |
| GET | /cache/{value} | Sets a Cache-Control header for n seconds. |

### cookies
| Method | Path | Description |
|--------|------|-------------|
| GET | /cookies | Returns cookie data. |
| GET | /cookies/delete | Deletes cookie(s) as provided by the query string and redirects to cookie list. |
| GET | /cookies/set | Sets cookie(s) as provided by the query string and redirects to cookie list. |
| GET | /cookies/set/{name}/{value} | Sets a cookie and redirects to cookie list. |

### deflate
| Method | Path | Description |
|--------|------|-------------|
| GET | /deflate | Returns Deflate-encoded data. |

### delay
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /delay/{delay} | Returns a delayed response (max of 10 seconds). |
| GET | /delay/{delay} | Returns a delayed response (max of 10 seconds). |
| PATCH | /delay/{delay} | Returns a delayed response (max of 10 seconds). |
| POST | /delay/{delay} | Returns a delayed response (max of 10 seconds). |
| PUT | /delay/{delay} | Returns a delayed response (max of 10 seconds). |

### delete
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /delete | The request's DELETE parameters. |

### deny
| Method | Path | Description |
|--------|------|-------------|
| GET | /deny | Returns page denied by robots.txt rules. |

### digest-auth
| Method | Path | Description |
|--------|------|-------------|
| GET | /digest-auth/{qop}/{user}/{passwd} | Prompts the user for authorization using Digest Auth. |
| GET | /digest-auth/{qop}/{user}/{passwd}/{algorithm} | Prompts the user for authorization using Digest Auth + Algorithm. |
| GET | /digest-auth/{qop}/{user}/{passwd}/{algorithm}/{stale_after} | Prompts the user for authorization using Digest Auth + Algorithm. |

### drip
| Method | Path | Description |
|--------|------|-------------|
| GET | /drip | Drips data over a duration after an optional initial delay. |

### encoding
| Method | Path | Description |
|--------|------|-------------|
| GET | /encoding/utf8 | Returns a UTF-8 encoded body. |

### etag
| Method | Path | Description |
|--------|------|-------------|
| GET | /etag/{etag} | Assumes the resource has the given etag and responds to If-None-Match and If-Match headers appropriately. |

### get
| Method | Path | Description |
|--------|------|-------------|
| GET | /get | The request's query parameters. |

### gzip
| Method | Path | Description |
|--------|------|-------------|
| GET | /gzip | Returns GZip-encoded data. |

### headers
| Method | Path | Description |
|--------|------|-------------|
| GET | /headers | Return the incoming request's HTTP headers. |

### hidden-basic-auth
| Method | Path | Description |
|--------|------|-------------|
| GET | /hidden-basic-auth/{user}/{passwd} | Prompts the user for authorization using HTTP Basic Auth. |

### html
| Method | Path | Description |
|--------|------|-------------|
| GET | /html | Returns a simple HTML document. |

### image
| Method | Path | Description |
|--------|------|-------------|
| GET | /image | Returns a simple image of the type suggest by the Accept header. |
| GET | /image/jpeg | Returns a simple JPEG image. |
| GET | /image/png | Returns a simple PNG image. |
| GET | /image/svg | Returns a simple SVG image. |
| GET | /image/webp | Returns a simple WEBP image. |

### ip
| Method | Path | Description |
|--------|------|-------------|
| GET | /ip | Returns the requester's IP Address. |

### json
| Method | Path | Description |
|--------|------|-------------|
| GET | /json | Returns a simple JSON document. |

### links
| Method | Path | Description |
|--------|------|-------------|
| GET | /links/{n}/{offset} | Generate a page containing n links to other pages which do the same. |

### patch
| Method | Path | Description |
|--------|------|-------------|
| PATCH | /patch | The request's PATCH parameters. |

### post
| Method | Path | Description |
|--------|------|-------------|
| POST | /post | The request's POST parameters. |

### put
| Method | Path | Description |
|--------|------|-------------|
| PUT | /put | The request's PUT parameters. |

### range
| Method | Path | Description |
|--------|------|-------------|
| GET | /range/{numbytes} | Streams n random bytes generated with given seed, at given chunk size per packet. |

### redirect-to
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /redirect-to | 302/3XX Redirects to the given URL. |
| GET | /redirect-to | 302/3XX Redirects to the given URL. |
| PATCH | /redirect-to | 302/3XX Redirects to the given URL. |
| POST | /redirect-to | 302/3XX Redirects to the given URL. |
| PUT | /redirect-to | 302/3XX Redirects to the given URL. |

### redirect
| Method | Path | Description |
|--------|------|-------------|
| GET | /redirect/{n} | 302 Redirects n times. |

### relative-redirect
| Method | Path | Description |
|--------|------|-------------|
| GET | /relative-redirect/{n} | Relatively 302 Redirects n times. |

### response-headers
| Method | Path | Description |
|--------|------|-------------|
| GET | /response-headers | Returns a set of response headers from the query string. |
| POST | /response-headers | Returns a set of response headers from the query string. |

### robots.txt
| Method | Path | Description |
|--------|------|-------------|
| GET | /robots.txt | Returns some robots.txt rules. |

### status
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /status/{codes} | Return status code or random status code if more than one are given |
| GET | /status/{codes} | Return status code or random status code if more than one are given |
| PATCH | /status/{codes} | Return status code or random status code if more than one are given |
| POST | /status/{codes} | Return status code or random status code if more than one are given |
| PUT | /status/{codes} | Return status code or random status code if more than one are given |

### stream-bytes
| Method | Path | Description |
|--------|------|-------------|
| GET | /stream-bytes/{n} | Streams n random bytes generated with given seed, at given chunk size per packet. |

### stream
| Method | Path | Description |
|--------|------|-------------|
| GET | /stream/{n} | Stream n JSON responses |

### user-agent
| Method | Path | Description |
|--------|------|-------------|
| GET | /user-agent | Return the incoming requests's User-Agent header. |

### uuid
| Method | Path | Description |
|--------|------|-------------|
| GET | /uuid | Return a UUID4. |

### xml
| Method | Path | Description |
|--------|------|-------------|
| GET | /xml | Returns a simple XML document. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get absolute-redirect details?" -> GET /absolute-redirect/{n}
- "List all anything?" -> GET /anything
- "Create a anything?" -> POST /anything
- "Delete a anything?" -> DELETE /anything/{anything}
- "Get anything details?" -> GET /anything/{anything}
- "Partially update a anything?" -> PATCH /anything/{anything}
- "Update a anything?" -> PUT /anything/{anything}
- "Get base64 details?" -> GET /base64/{value}
- "Get basic-auth details?" -> GET /basic-auth/{user}/{passwd}
- "List all bearer?" -> GET /bearer
- "List all brotli?" -> GET /brotli
- "Get byte details?" -> GET /bytes/{n}
- "List all cache?" -> GET /cache
- "Get cache details?" -> GET /cache/{value}
- "List all cookies?" -> GET /cookies
- "List all delete?" -> GET /cookies/delete
- "List all set?" -> GET /cookies/set
- "Get set details?" -> GET /cookies/set/{name}/{value}
- "List all deflate?" -> GET /deflate
- "Delete a delay?" -> DELETE /delay/{delay}
- "Get delay details?" -> GET /delay/{delay}
- "Partially update a delay?" -> PATCH /delay/{delay}
- "Update a delay?" -> PUT /delay/{delay}
- "List all deny?" -> GET /deny
- "Get digest-auth details?" -> GET /digest-auth/{qop}/{user}/{passwd}
- "Get digest-auth details?" -> GET /digest-auth/{qop}/{user}/{passwd}/{algorithm}
- "Get digest-auth details?" -> GET /digest-auth/{qop}/{user}/{passwd}/{algorithm}/{stale_after}
- "List all drip?" -> GET /drip
- "List all utf8?" -> GET /encoding/utf8
- "Get etag details?" -> GET /etag/{etag}
- "List all get?" -> GET /get
- "List all gzip?" -> GET /gzip
- "List all headers?" -> GET /headers
- "Get hidden-basic-auth details?" -> GET /hidden-basic-auth/{user}/{passwd}
- "List all html?" -> GET /html
- "List all image?" -> GET /image
- "List all jpeg?" -> GET /image/jpeg
- "List all png?" -> GET /image/png
- "List all svg?" -> GET /image/svg
- "List all webp?" -> GET /image/webp
- "List all ip?" -> GET /ip
- "List all json?" -> GET /json
- "Get link details?" -> GET /links/{n}/{offset}
- "Create a post?" -> POST /post
- "Get range details?" -> GET /range/{numbytes}
- "List all redirect-to?" -> GET /redirect-to
- "Create a redirect-to?" -> POST /redirect-to
- "Get redirect details?" -> GET /redirect/{n}
- "Get relative-redirect details?" -> GET /relative-redirect/{n}
- "List all response-headers?" -> GET /response-headers
- "Create a response-header?" -> POST /response-headers
- "List all robots.txt?" -> GET /robots.txt
- "Delete a status?" -> DELETE /status/{codes}
- "Get status details?" -> GET /status/{codes}
- "Partially update a status?" -> PATCH /status/{codes}
- "Update a status?" -> PUT /status/{codes}
- "Get stream-byte details?" -> GET /stream-bytes/{n}
- "Get stream details?" -> GET /stream/{n}
- "List all user-agent?" -> GET /user-agent
- "List all uuid?" -> GET /uuid
- "List all xml?" -> GET /xml
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
