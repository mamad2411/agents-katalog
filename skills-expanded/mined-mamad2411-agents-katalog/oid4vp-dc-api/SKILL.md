---
name: "oid4vp-dc-api"
description: "Use when implementing OpenID4VP over the W3C Digital Credentials API (DC API) in a browser context. Covers: DC API protocol flow, request/response format, signed and unsigned requests, security and privacy considerations specific to the browser-based flow."
sections:
  - "Appendix A. OpenID4VP over the Digital Credentials API"
  - "A.1. Protocol"
  - "A.2. Request"
  - "A.3. Signed and Unsigned Requests"
  - "A.4. Response"
  - "A.5. Security Considerations"
  - "A.6. Privacy Considerations"
---

<!-- ARF version: 1.0-final-2025-07-09 -->
<!-- Tokens: ~4197 -->

## Appendix A. OpenID4VP over the Digital Credentials API
This section defines how to use OpenID4VP with the Digital Credentials API.
The name "Digital Credentials API" (DC API) encompasses the W3C Digital Credentials API [[W3C.Digital_Credentials_API](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#W3C.Digital_Credentials_API)]
as well as its native App Platform equivalents in operating systems (such as [Credential Manager on Android](https://developer.android.com/jetpack/androidx/releases/credentials)).
The DC API allows web sites and native apps acting as Verifiers to request the presentation of Credentials.
The API itself is agnostic to the Credential exchange protocol and can be used with different protocols.
The Web Platform, working in conjunction with other layers, such as the app platform/operating system, and based on the permission of the End-User, will send the request data along with the Origin of the Verifier to the End-User's chosen Wallet.
OpenID4VP over the DC API utilizes the mechanisms of the DC API while also allowing to leverage advanced security features of OpenID4VP, if needed.
It also defines the OpenID4VP request parameters that MAY be used with the DC API.
The DC API offers several advantages for implementers of both Verifiers and Wallets.
Firstly, the API serves as a privacy-preserving alternative to invoking Wallets via URLs, particularly custom URL schemes. The underlying app platform will only invoke a Wallet if the End-User confirms the request based on contextual information about the Credential Request and the requestor (Verifier).
Secondly, the session with the End-User will always continue in the initial context, typically a web browser tab, when the request has been fulfilled (or aborted), which results in an improved End-User experience.
Thirdly, cross-device requests benefit from the use of secure transports with proximity checks, which are handled by the OS platform, e.g., using FIDO CTAP 2.2 with hybrid transports.
And lastly, as part of the request, the Wallet is provided with information about the Verifier's Origin as authenticated by the user agent, which is important for phishing resistance.


### A.1. Protocol
To use OpenID4VP with the Digital Credentials API (DC API), the exchange protocol value has the following format: `openid4vp-v<version>-<request-type>`. The `<version>` field is a numeric value, and `<request-type>` explicitly specifies the type of request. This approach eliminates the need for Wallets to perform implicit parameter matching to accurately identify the version and the expected request and response parameters.
The value `1` MUST be used for the `<version>` field to indicate the request and response are compatible with this version of the specification. For `<request-type>`, unsigned requests, as defined in [Appendix A.3.1](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#unsigned_request), MUST use `unsigned`, signed requests, as defined in [Appendix A.3.2.1](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#single_signed_request), MUST use `signed`, and multi-signed requests, as defined in [Appendix A.3.2.2](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#multi_signed_request), MUST use `multisigned`.
The following exchange protocol values are defined by this specification:

- Unsigned requests: `openid4vp-v1-unsigned`

          - Signed requests (JWS Compact Serialization): `openid4vp-v1-signed`

          - Multi-signed requests (JWS JSON Serialization): `openid4vp-v1-multisigned`

        


### A.2. Request
The Verifier MAY send a request, as defined in [Section 5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#vp_token_request), to the DC API.
The following is a non-normative example of an unsigned OpenID4VP request (when advanced security features of OpenID4VP are not used) that can be sent over the DC API:

```
{
  response_type: "vp_token",
  response_mode: "dc_api",
  nonce: "n-0S6_WzA2Mj",
  client_metadata: {...},
  dcql_query: {...}
}
```

Out of the Authorization Request parameters defined in [[RFC6749](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC6749)] and [Section 5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#vp_token_request), the following are supported with OpenID4VP over the W3C Digital Credentials API:

- 
            `client_id`

          - 
            `response_type`

          - 
            `response_mode`

          - 
            `nonce`

          - 
            `client_metadata`

          - 
            `request`

          - 
            `transaction_data`

          - 
            `dcql_query`

          - 
            `verifier_info`

        
The `client_id` parameter MUST be omitted in unsigned requests defined in [Appendix A.3.1](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#unsigned_request). The Wallet MUST ignore any `client_id` parameter that is present in an unsigned request.
Parameters defined by a specific Client Identifier Prefix (such as the `trust_chain` parameter for the OpenID Federation Client Identifier Prefix) are also supported over the W3C Digital Credentials API.
The `client_id` parameter MUST be present in signed requests defined in [Appendix A.3.2](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#signed_request), as it communicates to the Wallet which Client Identifier Prefix and Client Identifier to use when authenticating the client through verification of the request signature or retrieving client metadata.
The value of the `response_mode` parameter MUST be `dc_api` when the response is not encrypted and `dc_api.jwt` when the response is encrypted as defined in [Section 8.3](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#response_encryption). The Response Mode `dc_api` causes the Wallet to send the Authorization Response via the DC API. For Response Mode `dc_api.jwt`, the Wallet includes the `response` parameter, which contains an encrypted JWT encapsulating the Authorization Response, as defined in [Section 8.3](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#response_encryption).
In addition to the above-mentioned parameters, a new parameter is introduced for OpenID4VP over the W3C Digital Credentials API:

- 
            `expected_origins`: REQUIRED when signed requests defined in [Appendix A.3.2](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#signed_request) are used with the Digital Credentials API (DC API). A non-empty array of strings, each string representing an Origin of the Verifier that is making the request. The Wallet MUST compare values in this parameter to the Origin to detect replay of the request from a malicious Verifier. If the Origin does not match any of the entries in `expected_origins`, the Wallet MUST return an error. This error SHOULD be an `invalid_request` error. This parameter is not for use in unsigned requests and therefore a Wallet MUST ignore this parameter if it is present in an unsigned request.

        
The transport of the request and Origin to the Wallet is platform-specific and is out of scope of OpenID4VP over the Digital Credentials API.
Additional request parameters MAY be defined and used with OpenID4VP over the DC API.
The Wallet MUST ignore any unrecognized parameters. For example, since the `state` parameter is not defined for the DC API, the Verifier cannot expect it to be included in the response.


### A.3. Signed and Unsigned Requests
Any OpenID4VP request compliant to this section of this specification can be used with the Digital Credentials API (DC API). Depending on the mechanism used to identify and authenticate the Verifier, the request can be signed or unsigned. This section defines signed and unsigned OpenID4VP requests for use with the DC API.


#### A.3.1. Unsigned Request
The Verifier MAY send all the OpenID4VP request parameters as members in the request member passed to the API.


#### A.3.2. Signed Request
The Verifier MAY send a signed request, for example, when identification and authentication of the Verifier is required.
The signed request allows the Wallet to authenticate the Verifier using one or more trust framework(s) in addition to the Web PKI utilized by the browser. An example of such a trust framework is the Verifier (RP) management infrastructure set up in the context of the eIDAS regulation in the European Union, in which case, the Wallet can no longer rely only on the web origin of the Verifier. This web origin MAY still be used to further strengthen the security of the flow. The external trust framework could, for example, map the Client Identifier to registered web origins.
The signed Request Object MAY contain all the parameters listed in [Appendix A.2](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#dc_api_request), except `request`.
Verifiers SHOULD format signed Requests using JWS Compact Serialization but MAY use JWS JSON Serialization ([[RFC7515](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC7515)]) to cater for the use cases described below.


##### A.3.2.1. JWS Compact Serialization
When the JWS Compact Serialization is used to send the request, the Verifier can convey only one Trust Framework, i.e., the Verifier knows which trust frameworks the Wallet supports. All request parameters are encoded in a request object as defined in [Section 5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#vp_token_request) and the JWS object is used as the value of the `request` claim in the `data` element of the API call.
This is illustrated in the following non-normative example.

```
{ request: "eyJhbGciOiJF..." }
```

This is an example of the payload of a signed OpenID4VP request used with the W3C Digital Credentials API in conjunction with JWS Compact Serialization:

```
{
  "expected_origins": [
    "https://origin1.example.com",
    "https://origin2.example.com"
  ],
  "client_id": "x509_san_dns:rp.example.com",
  "client_metadata": {
    "jwks": {
      "keys": [
        {
          "kty": "EC",
          "crv": "P-256",
          "x": "MKBCTNIcKUSDii11ySs3526iDZ8AiTo7Tu6KPAqv7D4",
          "y": "4Etl6SRW2YiLUrN5vfvVHuhp7x8PxltmWWlbbM4IFyM",
          "use": "enc",
          "kid": "1"
        }
      ]
    }
  },
  "response_type": "vp_token",
  "response_mode": "dc_api",
  "nonce": "n-0S6_WzA2Mj",
  "dcql_query": {...}
}
```


##### A.3.2.2. JWS JSON Serialization
The JWS JSON Serialization ([[RFC7515](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC7515)]) allows the Verifier to use multiple Client Identifiers and corresponding key material to protect the same request. This serves use cases where the Verifier requests Credentials belonging to different trust frameworks and, therefore, needs to authenticate in the context of those trust frameworks. It also allows the Verifier to add different attestations for each Client Identifier.
In this case, the following request parameters, if used, MUST be present only in the protected header of the respective `signature` object in the `signatures` array defined in [Section 7.2.1](https://rfc-editor.org/rfc/rfc7515) of [[RFC7515](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC7515)]:

- 
                `client_id`

              - 
                `verifier_info`

              - parameters that are specific to a Client Identifier Prefix, e.g., the `trust_chain` JWS header parameter for the `openid_federation` Client Identifier Prefix

            
All other request parameters MUST be present in the `payload` element of the JWS object.
Below is a non-normative example of such a request:

```
{
  "payload": "eyAiaXNzIjogImh0dHBzOi8...NzY4Mzc4MzYiIF0gfQ",
  "signatures": [
    {
      "protected": "eyJhbGciOiAiRVMyNT..MiLCJraWQiOiAiMSJ9XX19fQ",
      "signature": "PFwem0Ajp2Sag...T2z784h8TQqgTR9tXcif0jw"
    },
    {
      "protected": "eyJhbGciOiAiRVMyNTY...tpZCI6ICIxIn1dfX19",
      "signature": "irgtXbJGwE2wN4Lc...2TvUodsE0vaC-NXpB9G39cMXZ9A"
    }
  ]
}
```

Every object in the `signatures` structure contains the parameters and the signature specific to a particular Client Identifier. The signature is calculated as specified in section 5.1 of [[RFC7515](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC7515)].
The following is a non-normative example of the content of a decoded protected header:

```
{
  "alg": "ES256",
  "x5c": [
    "MIICOjCCAeG...djzH7lA==",
    "MIICLTCCAdS...koAmhWVKe"
  ],
  "client_id": "x509_san_dns:rp.example.com"
}
```

The following is a non-normative example of the payload of a signed OpenID4VP request used with the W3C Digital Credentials API in conjunction with JWS JSON Serialization:

```
{
  "expected_origins": [
    "https://origin1.example.com",
    "https://origin2.example.com"
  ],
  "response_type": "vp_token",
  "response_mode": "dc_api",
  "nonce": "n-0S6_WzA2Mj",
  "dcql_query": {...},
  "client_metadata": {
    "jwks": {
      "keys": [
        {
          "kty": "EC",
          "crv": "P-256",
          "x": "MKBCTNIcKUSDii11ySs3526iDZ8AiTo7Tu6KPAqv7D4",
          "y": "4Etl6SRW2YiLUrN5vfvVHuhp7x8PxltmWWlbbM4IFyM",
          "use": "enc",
          "kid": "1"
        }
      ]
    }
  }
}
```


### A.4. Response
Every OpenID4VP Request results in a response being provided through the Digital Credentials API (DC API), or in a canceled flow. If a response is provided, the response is an instance of the `DigitalCredential` interface, as defined in [[W3C.Digital_Credentials_API](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#W3C.Digital_Credentials_API)], and the OpenID4VP Response parameters as defined for the Response Type are represented as an object within the `data` property.
Protocol error responses are returned as an object within the `data` property. This object has a single property with the name `error` and a value containing the error response code as defined in [Section 8.5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#error-response). Note that a protocol error generated by the Wallet will still result in a fulfilled promise for the Digital Credentials API request. Privacy considerations specific to returning error responses over the Digital Credentials API can be found in [Section 15.9.2](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#privacy-dc-api-error).
The following is a non-normative example of a `data` object containing an error:

```
{
    "error": "invalid_request"
}
```

The security properties that are normally provided by the Client Identifier are achieved by binding the response to the Origin it was received from.
The audience for the response (for example, the `aud` value in a Key Binding JWT) MUST be the Origin, prefixed with `origin:`, for example `origin:https://verifier.example.com/`. This is the case even for signed requests. Therefore, when using OpenID4VP over the DC API, the Client Identifier is not used as the audience for the response.


### A.5. Security Considerations
The following security considerations from OpenID4VP apply:

- Preventing Replay of Verifiable Presentations as described in [Section 14.1](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#preventing-replay), with the difference that the origin is used instead of the Client Identifier to bind the response to the Client.

          - End-User Authentication using Credentials as described in [Section 14.4](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#end-user-authentication-using-credentials).

          - Encrypting an Unsigned Response as described in [Section 14.5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#encrypting_unsigned_response).

          - TLS Requirements as described in [Section 14.6](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#tls-requirements).

          - Always Use the Full Client Identifier as described in [Section 14.8](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#full-client-identifier) for signed requests.

          - Security Checks on the Returned Credentials and Presentations as described in [Section 14.9](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#dcql_query_security).

          - DCQL Value Matching as described in [Section 15.4.1](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#dcql-value-matching).

        


### A.6. Privacy Considerations
The following privacy considerations from OpenID4VP apply:

- Selective Disclosure as described in [Section 15.4](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#selective-disclosure).

          - Privacy implications of mechanisms to establish trust in Issuers as described in [Section 15.10](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#privacy_trusted_authorities).
