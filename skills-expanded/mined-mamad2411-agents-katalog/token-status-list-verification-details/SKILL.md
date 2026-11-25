---
name: "token-status-list-verification-details"
description: "Use when implementing detailed Token Status List verification behavior. Covers section-specific verification rules and processing details."
sections:
  - "8. Verification and Processing"
  - "8.1. Status List Request"
  - "8.2. Status List Response"
  - "8.3. Validation Rules"
  - "8.4. Historical resolution"
---

<!-- ARF version: draft-10 -->
<!-- Tokens: ~2701 -->

## 8. Verification and Processing
The fetching, processing and verifying of a Status List Token may be done by either the Holder or the Relying Party. In the following section is described from the role of the Relying Party, however the same rules would also apply for the Holder.


### 8.1. Status List Request
To obtain the Status List Token, the Relying Party MUST send an HTTP GET request to the URI provided in the Referenced Token.
The HTTP endpoint SHOULD support the use of Cross-Origin Resource Sharing (CORS) [[CORS](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#CORS)] and/or other methods as appropriate to enable Browser-based clients to access it.
The Relying Party SHOULD send the following Accept-Header to indicate the requested response type:

- 
            "application/statuslist+jwt" for Status List Token in JWT format

          - 
            "application/statuslist+cwt" for Status List Token in CWT format

        
If the Relying Party does not send an Accept Header, the response type is assumed to be known implicitly or out-of-band.
A successful response that contains a Status List Token MUST use an HTTP status code in the 2xx range.
A response MAY also choose to redirect the client to another URI using an HTTP status code in the 3xx range, which clients SHOULD follow. A client SHOULD detect and intervene in cyclical redirections (i.e., "infinite" redirection loops).
The following are non-normative examples of a request and response for a Status List Token with type `application/statuslist+jwt`:

```
GET /statuslists/1 HTTP/1.1
Host: example.com
Accept: application/statuslist+jwt
```


```
HTTP/1.1 200 OK
Content-Type: application/statuslist+jwt

eyJhbGciOiJFUzI1NiIsImtpZCI6IjEyIiwidHlwIjoic3RhdHVzbGlzdCtqd3QifQ.e
yJleHAiOjIyOTE3MjAxNzAsImlhdCI6MTY4NjkyMDE3MCwiaXNzIjoiaHR0cHM6Ly9le
GFtcGxlLmNvbSIsInN0YXR1c19saXN0Ijp7ImJpdHMiOjEsImxzdCI6ImVOcmJ1UmdBQ
WhjQlhRIn0sInN1YiI6Imh0dHBzOi8vZXhhbXBsZS5jb20vc3RhdHVzbGlzdHMvMSIsI
nR0bCI6NDMyMDB9.2RSRdUce0QmRvsbJkt0Hr0Ny5c9Tim2yj43wMFU76xjv9TClW5-B
65b9pZSraeoPv6OxTULb4dHiWK0O8oLi6g
```


### 8.2. Status List Response
In the successful response, the Status Provider MUST use the following content-type:

- 
            "application/statuslist+jwt" for Status List Token in JWT format

          - 
            "application/statuslist+cwt" for Status List Token in CWT format

        
In the case of "application/statuslist+jwt", the response MUST be of type JWT and follow the rules of [Section 5.1](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#status-list-token-jwt).
In the case of "application/statuslist+cwt", the response MUST be of type CWT and follow the rules of [Section 5.2](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#status-list-token-cwt).
The HTTP response SHOULD use gzip Content-Encoding as defined in [[RFC9110](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC9110)].
If caching-related HTTP headers are present in the HTTP response, Relying Parties SHOULD prioritize the exp and ttl claims within the Status List Token over the HTTP headers for determining caching behavior.


### 8.3. Validation Rules
Upon receiving a Referenced Token, a Relying Party MUST first perform the validation of the Referenced Token - e.g., checking for expected attributes, valid signature and expiration time. The processing rules for Referenced Tokens (such as JWT or CWT) precede any evaluation of a Referenced Token's status. For example, if a token is evaluated as being expired through the "exp" (Expiration Time) but also has a status of 0x00 ("VALID"), the token is considered expired. As this is out of scope for this document, this validation is not described here, but is expected to be done according to the format of the Referenced Token.
If this validation is not successful, the Referenced Token MUST be rejected. If the validation was successful, the Relying Party MUST perform the following validation steps to evaluate the status of the reference token:

- 
            Check for the existence of a `status` claim, check for the existence of a `status_list` claim within the `status` claim and validate that the content of `status_list` adheres to the rules defined in [Section 6.2](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#referenced-token-jose) for JOSE-based Referenced Tokens and [Section 6.3](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#referenced-token-cose) for COSE-based Referenced Tokens. Other formats of Referenced Tokens may define other encoding of the URI and index.

          - 
            Resolve the Status List Token from the provided URI

          - 
            Validate the Status List Token:

- 
                Validate the Status List Token by following the rules defined in section 7.2 of [[RFC7519](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC7519)] for JWTs and section 7.2 of [[RFC8392](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC8392)] for CWTs. This step might require the resolution of a public key as described in [Section 11.3](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#key-management).

              - 
                Check for the existence of the required claims as defined in [Section 5.1](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#status-list-token-jwt) and [Section 5.2](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#status-list-token-cwt) depending on the token type

            

          - 
            All existing claims in the Status List Token MUST be checked according to the rules in [Section 5.1](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#status-list-token-jwt) and [Section 5.2](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#status-list-token-cwt)

- 
                The subject claim (`sub` or `2`) of the Status List Token MUST be equal to the `uri` claim in the `status_list` object of the Referenced Token

              - 
                If the Relying Party has custom policies regarding the freshness of the Status List Token, it SHOULD check the issued at claim (`iat` or `6`)

              - 
                If the expiration time is defined (`exp` or `4`), it MUST be checked if the Status List Token is expired

              - 
                If the Relying Party is using a system for caching the Status List Token, it SHOULD check the `ttl` claim of the Status List Token and retrieve a fresh copy if (time status was resolved + ttl < current time)

            

          - 
            Decompress the Status List with a decompressor that is compatible with DEFLATE [[RFC1951](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC1951)] and ZLIB [[RFC1950](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC1950)]

          - 
            Retrieve the status value of the index specified in the Referenced Token as described in [Section 4](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#status-list). Fail if the provided index is out of bounds of the Status List

          - 
            Check the status value as described in [Section 7](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#status-types)

        
If any of these checks fails, no statement about the status of the Referenced Token can be made and the Referenced Token SHOULD be rejected.


### 8.4. Historical resolution
By default, the status mechanism defined in this specification only conveys information about the state of Reference Tokens at the time the Status List Token was issued. The validity period for this information, as defined by the issuer, is explicitly stated by the `iat` (issued at) and `exp` (expiration time) claims for JWT and their corresponding ones for the CWT representation. If support for historical status information is required, this can be achieved by extending the request for the Status List Token as defined in [Section 8.1](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#status-list-request) with a timestamp. This feature has additional privacy implications as described in [Section 12.7](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#privacy-historical).
To obtain the Status List Token, the Relying Party MUST send an HTTP GET request to the URI provided in the Referenced Token with the additional query parameter `time` and its value being a unix timestamp. The response for a valid request SHOULD contain a Status List Token that was valid for that specified time or an error.
If the Server does not support the additional query parameter, it SHOULD return a status code of 501 (Not Implemented) or if the requested time is not supported it SHOULD return a status code of 406 (Not Acceptable). A Status List Token might be served via static file hosting (e.g., leveraging a Content Delivery Network), which would result in the client not being able to retrieve those status codes. Thus, the client MUST verify support for this feature by verifying that the requested timestamp is within the valid time of the returned token signaled via `iat` (`6` for CWT) and `exp` (`4` for CWT).
The following is a non-normative example of a GET request using the `time` query parameter:

```
GET /statuslists/1?time=1686925000 HTTP/1.1
Host: example.com
Accept: application/statuslist+jwt
```

The following is a non-normative example of a response for the above Request:

```
HTTP/1.1 200 OK
Content-Type: application/statuslist+jwt

eyJhbGciOiJFUzI1NiIsImtpZCI6IjEyIiwidHlwIjoic3RhdHVzbGlzdCtqd3QifQ.e
yJleHAiOjIyOTE3MjAxNzAsImlhdCI6MTY4NjkyMDE3MCwiaXNzIjoiaHR0cHM6Ly9le
GFtcGxlLmNvbSIsInN0YXR1c19saXN0Ijp7ImJpdHMiOjEsImxzdCI6ImVOcmJ1UmdBQ
WhjQlhRIn0sInN1YiI6Imh0dHBzOi8vZXhhbXBsZS5jb20vc3RhdHVzbGlzdHMvMSIsI
nR0bCI6NDMyMDB9.2RSRdUce0QmRvsbJkt0Hr0Ny5c9Tim2yj43wMFU76xjv9TClW5-B
65b9pZSraeoPv6OxTULb4dHiWK0O8oLi6g
```
