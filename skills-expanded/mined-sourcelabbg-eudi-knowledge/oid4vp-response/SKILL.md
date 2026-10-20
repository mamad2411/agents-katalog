---
name: "oid4vp-response"
description: "Use when handling or validating an OpenID4VP response. Covers: vp_token structure, presentation_submission, response modes (fragment, direct_post, direct_post.jwt), encrypted responses, transaction data, error responses, and VP Token validation rules."
sections:
  - "8. Response"
  - "8.1. Response Parameters"
  - "8.2. Response Mode \"direct_post\""
  - "8.3. Encrypted Responses"
  - "8.4. Transaction Data"
  - "8.5. Error Response"
  - "8.6. VP Token Validation"
---

<!-- ARF version: 1.0-final-2025-07-09 -->
<!-- Tokens: ~6328 -->

## 8. Response
A VP Token is only returned if the corresponding Authorization Request contained a `dcql_query` parameter or a `scope` parameter representing a DCQL Query [Section 5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#vp_token_request).
A VP Token can be returned in the Authorization Response or the Token Response depending on the Response Type used. See [Section 5.6](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#response_type_vp_token) for more details.
If the Response Type value is `vp_token`, the VP Token is returned in the Authorization Response. When the Response Type value is `vp_token id_token` and the `scope` parameter contains `openid`, the VP Token is returned in the Authorization Response alongside a Self-Issued ID Token as defined in [[SIOPv2](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#SIOPv2)].
If the Response Type value is `code` (Authorization Code Grant Type), the VP Token is provided in the Token Response.
The expected behavior is summarized in the following table:

        
Table 1:
OpenID for Verifiable Presentations `response_type` values
        

          
            
              `response_type` parameter value
            Response containing the VP Token
          
        
        
          
            
              `vp_token`

            Authorization Response
          
          
            
              `vp_token id_token`

            Authorization Response
          
          
            
              `code`

            Token Response
          
        
      
The behavior with respect to the VP Token is unspecified for any other individual Response Type value, or a combination of Response Type values.


### 8.1. Response Parameters
When a VP Token is returned, the respective response includes the following parameters:

          
`vp_token`:
          REQUIRED. This is a JSON-encoded object containing entries where the key is the `id` value used for a Credential Query in the DCQL query and the value is an array of one or more Presentations that match the respective Credential Query. When `multiple` is omitted, or set to `false`, the array MUST contain only one Presentation. There MUST NOT be any entry in the JSON-encoded object for optional Credential Queries when there are no matching Credentials for the respective Credential Query. Each Presentation is represented as a string or object, depending on the format as defined in [Appendix B](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#format_specific_parameters). The same rules as above apply for encoding the Presentations.

        

Other parameters, such as `code` (from [[RFC6749](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC6749)]), or `id_token` (from [[OpenID.Core](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#OpenID.Core)]), and `iss` (from [[RFC9207](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC9207)]) can be included in the response as defined in the respective specifications.
Additional response parameters MAY be defined and used,
as described in [[RFC6749](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC6749)].
The Client MUST ignore any unrecognized parameters.
The following is a non-normative example of an Authorization Response when the Response Type value in the Authorization Request was `vp_token`:

```
HTTP/1.1 302 Found
Location: https://client.example.org/cb#
  vp_token=...
```


#### 8.1.1. Examples
The following is a non-normative example of the contents of a VP Token
containing a single Verifiable Presentation in the SD-JWT VC format after a
request using DCQL like the one shown in [Section 7.4](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#dcql_query_example) (shortened for
brevity):

```
{
  "my_credential": ["eyJhbGci...QMA"]
}
```

The following is a non-normative example of the contents of a VP Token
containing multiple Verifiable Presentations in the SD-JWT VC format when the
Credential Query has `multiple` set to `true` (shortened for brevity):

```
{
  "my_credential": ["eyJhbGci...QMA", "eyJhbGci...QMA", ...]
}
```


### 8.2. Response Mode "direct_post"
The Response Mode `direct_post` allows the Wallet to send the Authorization Response to an endpoint controlled by the Verifier via an HTTP POST request.
It has been defined to address the following use cases:

- Verifier and Wallet are located on different devices; thus, the Wallet cannot send the Authorization Response to the Verifier using a redirect.

          - The Authorization Response size exceeds the URL length limits of user agents, so flows relying only on redirects (such as Response Mode `fragment`) cannot be used. In those cases, the Response Mode `direct_post` is the way to convey the Presentations to the Verifier without the need for the Wallet to have a backend.

        
The Response Mode is defined in accordance with [[OAuth.Responses](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#OAuth.Responses)] as follows:

          
`direct_post`:
          In this mode, the Authorization Response is sent to the Verifier using an HTTP POST request to an endpoint controlled by the Verifier. The Authorization Response MUST be encoded in the request body using the format defined by the `application/x-www-form-urlencoded` HTTP content type. The parameters in the request body MUST all be encoded using UTF-8. The Verifier can request that the Wallet redirects the End-User to the Verifier using the response as defined below.

        

The following new Authorization Request parameter is defined to be used in conjunction with Response Mode `direct_post`:

          
`response_uri`:
          REQUIRED when the Response Mode `direct_post` is used. The URL to which the Wallet MUST send the Authorization Response using an HTTP POST request as defined by the Response Mode `direct_post`. The Response URI receives all Authorization Response parameters as defined by the respective Response Type. When the `response_uri` parameter is present, the `redirect_uri` Authorization Request parameter MUST NOT be present. If the `redirect_uri` Authorization Request parameter is present when the Response Mode is `direct_post`, the Wallet MUST return an `invalid_request` Authorization Response error. The `response_uri` value MUST be a value that the client would be permitted to use as `redirect_uri` when following the rules defined in [Section 5.9](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#client_metadata_management).

        

Note: When the specification text refers to the usage of Redirect URI in the Authorization Request, that part of the text also applies when Response URI is used in the Authorization Request with Response Mode `direct_post`.
Note: The Verifier's component providing the user interface (Frontend) and the Verifier's component providing the Response URI need to be able to map authorization requests to the respective authorization responses. The Verifier MAY use the `state` Authorization Request parameter to add appropriate data to the Authorization Response for that purpose, for details see [Section 13.3](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#implementation_considerations_direct_post).
Additional request parameters MAY be defined and used with the Response Mode `direct_post`.
The Wallet MUST ignore any unrecognized parameters.
The following is a non-normative example of the payload of a Request Object with Response Mode `direct_post`:

```
{
  "client_id": "redirect_uri:https://client.example.org/post",
  "response_uri": "https://client.example.org/post",
  "response_type": "vp_token",
  "response_mode": "direct_post",
  "dcql_query": {...},
  "nonce": "n-0S6_WzA2Mj",
  "state": "eyJhb...6-sVA"
}
```

The following non-normative example of an Authorization Request refers to the Authorization Request Object from above through the `request_uri` parameter. The Authorization Request can be displayed to the End-User either directly (as a link) or as a QR Code:

```
https://wallet.example.com?
  client_id=https%3A%2F%2Fclient.example.org%2Fcb
  &request_uri=https%3A%2F%2Fclient.example.org%2F567545564
```

The following is a non-normative example of the Authorization Response that is sent via an HTTP POST request to the Verifier's Response URI:

```
POST /post HTTP/1.1
Host: client.example.org
Content-Type: application/x-www-form-urlencoded

  vp_token=...&
  state=eyJhb...6-sVA
```

The following is a non-normative example of an Authorization Error Response that is sent as an HTTP POST request to the Verifier's Response URI:

```
POST /post HTTP/1.1
Host: client.example.org
Content-Type: application/x-www-form-urlencoded

  error=invalid_request&
  error_description=unsupported%20client_id_prefix&
  state=eyJhb...6-sVA
```

If the Response URI has successfully processed the Authorization Response or Authorization Error Response, it MUST respond with an HTTP status code of 200 with `Content-Type` of `application/json` and a JSON object in the response body.
The following new parameter is defined for use in the JSON object returned from the Response Endpoint to the Wallet:

          
`redirect_uri`:
          OPTIONAL. String containing a URI. When this parameter is present the Wallet MUST redirect the user agent to this URI. This allows the Verifier to continue the interaction with the End-User on the device where the Wallet resides after the Wallet has sent the Authorization Response to the Response URI. It can be used by the Verifier to prevent session fixation ([Section 14.2](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#session_fixation)) attacks. The Response URI MAY return the `redirect_uri` parameter in response to successful Authorization Responses or for Error Responses.

        

Additional response parameters MAY be defined and used. The Wallet MUST ignore any unrecognized parameters.
Note: Response Mode `direct_post` without the `redirect_uri` could be less secure than Response Modes with redirects. For details, see ([Section 14.2](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#session_fixation)).
The value of the redirect URI is an absolute URI as defined by [[RFC3986](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC3986)] Section 4.3 and is chosen by the Verifier. The Verifier MUST include a fresh, cryptographically random value in the URL. This value is used to ensure only the receiver of the redirect can fetch and process the Authorization Response. The value can be added as a path component, as a fragment or as a parameter to the URL. It is RECOMMENDED to use a cryptographic random value of 128 bits or more. For implementation considerations see [Section 13.3](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#implementation_considerations_direct_post).
The following is a non-normative example of the response from the Verifier to the Wallet upon receiving the Authorization Response at the Response URI (using a `response_code` parameter from [Section 13.3](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#implementation_considerations_direct_post)):

```
HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: no-store

{
  "redirect_uri": "https://client.example.org/cb#response_code=091535f699ea575c7937fa5f0f454aee"
}
```

If the response does not contain the `redirect_uri` parameter, the Wallet is not required to perform any further steps.
Note: In the Response Mode `direct_post` or `direct_post.jwt`, the Wallet can change the UI based on the Verifier's callback to the Wallet following the submission of the Authorization Response.
Additional parameters MAY be defined and used in the response from the Response Endpoint to the Wallet.
The Wallet MUST ignore any unrecognized parameters.


### 8.3. Encrypted Responses
This section defines how an Authorization Response containing a VP Token (such as when the Response Type value is `vp_token` or `vp_token id_token`) can be encrypted at the application level using [[RFC7518](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC7518)] where the payload of the JWE is a JSON object containing the Authorization Response parameters. Encrypting the Authorization Response can, for example, prevent personal data in the Authorization Response from leaking, when the Authorization Response is returned through the front channel (e.g., the browser).
To encrypt the Authorization Response, implementations MUST use an unsigned, encrypted JWT as described in [[RFC7519](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC7519)].
To obtain the Verifier's public key to which to encrypt the Authorization Response, the Wallet uses JWKs from client metadata (such as the `jwks` member within the `client_metadata` request parameter or other mechanisms as allowed by the given Client Identifier Prefix).
Using what it supports and its preferences, the Wallet selects the public key to encrypt the Authorization Response based on information about each key, such as the `kty` (Key Type), `use` (Public Key Use), `alg` (Algorithm), and other JWK parameters.
The `alg` parameter MUST be present in the JWKs.
The JWE `alg` algorithm used MUST be equal to the `alg` value of the chosen `jwk`.
If the selected public key contains a `kid` parameter, the JWE MUST include the same value in the `kid` JWE Header Parameter (as defined in [Section 4.1.6](https://rfc-editor.org/rfc/rfc7516)) of the encrypted response. This enables the Verifier to easily identify the specific public key that was used to encrypt the response.
The JWE `enc` content encryption algorithm used is obtained from the `encrypted_response_enc_values_supported` parameter of client metadata, such as the `client_metadata` request parameter, allowing for the default value of `A128GCM` when not explicitly set.
The payload of the encrypted JWT response MUST include the contents of the response as defined in [Section 8.1](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#response-parameters) as top-level JSON members.
The following shows a non-normative example of the content of a request that is asking for an encrypted response while providing
a few public keys for encryption in the `jwks` member of the `client_metadata` request parameter:

```
{
 "response_type": "vp_token",
 "response_mode": "dc_api.jwt",
 "nonce": "xyz123ltcaccescbwc777",
 "dcql_query": {
  "credentials": [
   {
    "id": "my_credential",
    "format": "dc+sd-jwt",
    "meta": {
      "vct_values": ["https://credentials.example.com/identity_credential"]
    },
    "claims": [
      {"path": ["last_name"]},
      {"path": ["first_name"]},
      {"path": ["address", "postal_code"]}
     ]
    }
   ]
 },
 "client_metadata": {
   "jwks": {
    "keys": [
    {
     "kty":"EC", "kid":"ac", "use":"enc", "crv":"P-256","alg":"ECDH-ES",
     "x":"YO4epjifD-KWeq1sL2tNmm36BhXnkJ0He-WqMYrp9Fk",
     "y":"Hekpm0zfK7C-YccH5iBjcIXgf6YdUvNUac_0At55Okk"
    },
    {
     "kty":"OKP","kid":"jc","use":"enc","crv":"X25519","alg":"ECDH-ES",
     "x":"WPX7wnwq10hFNK9aDSyG1QlLswE_CJY14LdhcFUIVVc"
    },
    {
     "kty":"EC","kid":"lc","use":"enc","crv":"P-384","alg":"ECDH-ES",
     "x":"iHytgLNtXjEyYMAIGwfgjINZRmLfObYbmjPhkaPD8OiTkJtRHjegTNdH31Mxg4nV",
     "y":"MizXWSqNB7sSt_SNjg3spvaJnmjB-LpxsPpLUaea33rvINL3Mq-gEaANErRQpbLx"
    },
    {
     "kty":"OKP","kid":"bc","use":"enc","crv":"X448","alg":"ECDH-ES",
     "x":"pK5IRpLlX-8XcsRYWHejpzkfsHoDOmAYuBzAC7aTpewWOw_QFHSa64t9p2kuommI8JQQLohS2AIA"
    }
   ]
  },
  "encrypted_response_enc_values_supported": ["A128GCM", "A128CBC-HS256"]
 }
}
```

A non-normative example response to the above request, having been encrypted to the first key, might look like the following
(with added line breaks for display purposes only):

```
{
 "response" : "eyJhbGciOiJFQ0RILUVTIiwiZW5jIjoiQTEyOEdDTSIsImtpZCI6ImFjIiwiZXBrIjp7Imt
    0eSI6IkVDIiwieCI6Im5ubVZwbTNWM2piaGNhZlFhUkJrU1ZOSGx3Wkh3dC05ck9wSnVmeVlJdWsiLCJ5I
    joicjRmakRxd0p5czlxVU9QLV9iM21SNVNaRy0tQ3dPMm1pYzVWU05UWU45ZyIsImNydiI6IlAtMjU2In1
    9..uAYcHRUSSn2X0WPX.yVzlGSYG4qbg0bq18JcUiDRw56yVnbKR8E7S7YlEtzT00RqE3Pw5oTpUG3hdLN
    4taHZ9gC1kwak8JOnJgQ.1wR024_3-qtAlx1oFIUpQQ"
}
```

For illustrative purposes, the following JWK includes the private key `d` parameter value and can be used to decrypt the above encrypted Authorization Response example.

```
{
  "kty":"EC", "kid":"ac", "use":"enc", "crv":"P-256","alg":"ECDH-ES",
  "x":"YO4epjifD-KWeq1sL2tNmm36BhXnkJ0He-WqMYrp9Fk",
  "y":"Hekpm0zfK7C-YccH5iBjcIXgf6YdUvNUac_0At55Okk",
  "d":"Et-3ce0omz8_TuZ96Df9lp0GAaaDoUnDe6X-CRO7Aww"
}
```

The following shows the decoded header of the above encrypted Authorization Response example:

```
{
  "alg": "ECDH-ES",
  "enc": "A128GCM",
  "kid": "ac",
  "epk": {
    "kty": "EC",
    "x": "nnmVpm3V3jbhcafQaRBkSVNHlwZHwt-9rOpJufyYIuk",
    "y": "r4fjDqwJys9qUOP-_b3mR5SZG--CwO2mic5VSNTYN9g",
    "crv": "P-256"
  }
}
```

While this shows the payload of the above encrypted Authorization Response example:

```
{
 "vp_token": {"example_credential_id": ["eyJhb...YMetA"]}
}
```

Note that for the ECDH JWE algorithms (from Section 4.6 of [[RFC7518](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC7518)]), the `apu` and `apv` values are inputs
into the key derivation process that is used to derive the content encryption key. Regardless of the algorithm used, the values are always part of the AEAD tag computation so will still be bound to the encrypted response.
Note: For encryption, implementers have a variety of options available through JOSE, including the use of Hybrid Public Key Encryption (HPKE) as detailed in [[I-D.ietf-jose-hpke-encrypt](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-jose-hpke-encrypt)].


#### 8.3.1. Response Mode "direct_post.jwt"
This specification also defines a new Response Mode `direct_post.jwt`, which allows for encryption to be used on top of the Response Mode `direct_post` defined in [Section 8.2](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#response_mode_post). The mechanisms described in [Section 8.2](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#response_mode_post) apply unless specified otherwise in this section.
The Response Mode `direct_post.jwt` causes the Wallet to send the Authorization Response using an HTTP POST request instead of redirecting back to the Verifier as defined in [Section 8.2](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#response_mode_post). The Wallet adds the `response` parameter containing the JWT as defined in [Section 8.3](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#response_encryption) in the body of an HTTP POST request using the `application/x-www-form-urlencoded` content type. The names and values in the body MUST be encoded using UTF-8.
If a Wallet is unable to generate an encrypted response, it MAY send an error response without encryption as per [Section 8.2](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#response_mode_post).
The following is a non-normative example of a response (omitted content shown with ellipses for display purposes only):

```
POST /post HTTP/1.1
Host: client.example.org
Content-Type: application/x-www-form-urlencoded

response=eyJra...9t2LQ
```

The following is a non-normative example of the payload of the JWT used in the example above before encrypting and base64url encoding (omitted content shown with ellipses for display purposes only):

```
{
  "vp_token": {"example_jwt_vc": ["eY...QMA"]}
}
```


### 8.4. Transaction Data
The transaction data mechanism enables a binding between the user's identification/authentication and the user’s authorization, for example to complete a payment transaction, or to sign specific document(s) using QES (Qualified Electronic Signatures). This is achieved by signing the transaction data used for user authorization with the user-controlled key used for proof of possession of the Credential being presented as a means for user identification/authentication.
The Wallet that received the `transaction_data` parameter in the request MUST include a representation or reference to the data in the respective Credential presentation. How this is done is transaction data type specific. Credential Formats can give recommendations of how to handle transaction data, such as those in [Appendix B](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#format_specific_parameters).
If the Wallet does not support `transaction_data` parameter, it MUST return an error upon receiving a request that includes it.


### 8.5. Error Response
The error response follows the rules as defined in [[RFC6749](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC6749)], with the following additional clarifications:
`invalid_scope`:

- Requested scope value is invalid, unknown, or malformed.

        
`invalid_request`:

- The request contains both a `dcql_query` parameter and a `scope` parameter referencing a DCQL query.

          - The request uses the `vp_token` Response Type but does not include a `dcql_query` parameter nor a `scope` parameter referencing a DCQL query.

          - The Wallet does not support the Client Identifier Prefix passed in the Authorization Request.

          - The Client Identifier passed in the request did not belong to its Client Identifier Prefix, or requirements of a certain prefix were violated, for example an unsigned request was sent with Client Identifier Prefix `https`.

        
`invalid_client`:

- 
            `client_metadata` parameter defined in [Section 5.1](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#new_parameters) is present, but the Wallet recognizes Client Identifier and knows metadata associated with it.

          - Verifier's pre-registered metadata has been found based on the Client Identifier, but `client_metadata` parameter is also present.

        
`access_denied`:

- The Wallet did not have the requested Credentials to satisfy the Authorization Request.

          - The End-User did not give consent to share the requested Credentials with the Verifier.

          - The Wallet failed to authenticate the End-User.

        
This document also defines the following additional error codes and error descriptions:
`vp_formats_not_supported`:

- The Wallet does not support any of the formats requested by the Verifier, such as those included in the `vp_formats_supported` registration parameter.

        
`invalid_request_uri_method`:

- The value of the `request_uri_method` request parameter is neither `get` nor `post` (case-sensitive).

        
`invalid_transaction_data`:

- 
            any of the following is true for at least one object in the `transaction_data` structure:

- contains an unknown or unsupported transaction data type value,

              - is an object of a known type but containing unknown fields,

              - contains fields of the wrong type for the transaction data type,

              - contains fields with invalid values for the transaction data type,

              - is missing required fields for the transaction data type,

              - the credential_ids does not match, or

              - the referenced Credential(s) are not available in the Wallet.

            

        
`wallet_unavailable`:

- The Wallet appears to be unavailable and therefore unable to respond to the request. It can be useful in situations where the user agent cannot invoke the Wallet and another component receives the request while the End-User wishes to continue the journey on the Verifier website. For example, this applies when using claimed HTTPS URIs handled by the Wallet provider in case the platform cannot or does not translate the URI into a platform intent to invoke the Wallet. In this case, the Wallet provider would return the Authorization Error Response to the Verifier and might redirect the user agent back to the Verifier website.

        


### 8.6. VP Token Validation
Verifiers MUST validate the VP Token in the following manner:

- Validate the format of the VP Token as defined in [Section 8.1](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#response-parameters).

          - 
            Check the individual Presentations according to the specific Credential Format requested:

- Validate the integrity and authenticity of the Presentation and Credential.

              - Validate that the returned Credential(s) meet all criteria defined in the query in the Authorization Request (e.g., Claims included in the presentation).

              - Validate that all Presentations contain a cryptographic proof of Holder Binding (i.e., that they are Verifiable Presentations), unless specifically requested otherwise.

              - For Verifiable Presentations, validate the Holder Binding, including the checks required to prevent replay described in [Section 14.1](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#preventing-replay).

              - Perform the checks required by the Verifier's policy based on the set of trust requirements such as trust frameworks it belongs to (e.g., revocation checks), if applicable.

            

          - Check that the set of Presentations returned satisfies all requirements defined in the Verifier's request as described in [Section 6.4](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#dcql_query_lang_processing_rules).

        
If any of the checks related to an individual Presentation fail, the effected Presentation MUST be discarded. If any of the checks pertaining to the VP Token or the overall response fails, the VP Token MUST be rejected.
