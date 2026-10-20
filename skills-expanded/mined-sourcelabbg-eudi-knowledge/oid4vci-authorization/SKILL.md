---
name: "oid4vci-authorization"
description: "Use when implementing the authorization flow for credential issuance. Covers: authorization request with issuer_state, authorization_details, scope-based requests, pushed authorization requests (PAR), and token endpoint extensions."
sections:
  - "7. Nonce Endpoint"
  - "7.1. Nonce Request"
  - "7.2. Nonce Response"
  - "8. Credential Endpoint"
  - "8.1. Binding the Issued Credential to the Identifier of the End-User Possessing that Credential"
  - "8.2. Credential Request"
  - "8.3. Credential Response"
---

<!-- ARF version: 1.0-2025-02-03 -->
<!-- Tokens: ~5611 -->

## 7. Nonce Endpoint
This endpoint allows a Client to acquire a fresh `c_nonce` value. A Credential Issuer that requires `c_nonce` values to be incorporated into proofs in the Credential Request (see [Section 8.2](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-request)) MUST offer a Nonce Endpoint.
The `nonce_endpoint` Credential Issuer Metadata parameter, as defined in [Section 12.2.4](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-issuer-parameters), contains the URL of the Credential Issuer's Nonce Endpoint.


### 7.1. Nonce Request
A request for a nonce is made by sending an HTTP POST request to the URL provided in the `nonce_endpoint` Credential Issuer Metadata parameter. The Nonce Endpoint is not a protected resource, meaning the Wallet does not need to supply an access token to access it.
Below is a non-normative example of a Nonce Request:

```
POST /nonce HTTP/1.1
Host: credential-issuer.example.com
Content-Length: 0
```


### 7.2. Nonce Response
The Credential Issuer provides a nonce value in an HTTP response with a 2xx status code and the following parameters included as top-level members in the message body of the HTTP response using the application/json media type:

- 
            `c_nonce`: REQUIRED. String containing a challenge to be used when creating a proof of possession of the key (see [Section 8.2](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-request)). It is at the discretion of the Credential Issuer when to return a new challenge value as opposed to the one returned in the previous request. New challenge values MUST be unpredictable.

        
Due to the temporal nature of the `c_nonce` value, the Credential Issuer MUST make the response uncacheable by adding a `Cache-Control` header field including the value `no-store`.
The Credential Issuer MAY provide a DPoP nonce in an HTTP header as defined in Section 8.2 of [[RFC9449](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC9449)]. In this case, the Wallet uses the new nonce value in the DPoP proof when presenting an access token at the Credential Endpoint.
Below is a non-normative example of a Nonce Response:

```
HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: no-store
DPoP-Nonce: eyJ7S_zG.eyJH0-Z.HX4w-7v

{
  "c_nonce": "wKI4LT17ac15ES9bw8ac4"
}
```

---

## 8. Credential Endpoint
The Credential Endpoint issues one or more Credentials of the same Credential Configuration and Credential Dataset (as approved by the End-User) upon presentation of a valid Access Token representing this approval. Support for this endpoint is REQUIRED.
Communication with the Credential Endpoint MUST utilize TLS.
The Client sends a Credential Request to obtain:

- one Credential; or

        - multiple Credential instances of the same Credential Configuration and Credential Dataset, each with distinct cryptographic material.

      
If the Issuer supports the issuance of multiple Credentials, the Client can send several consecutive Credential Requests to obtain multiple Credentials in a chosen sequence.


### 8.1. Binding the Issued Credential to the Identifier of the End-User Possessing that Credential
The issued Credential SHOULD be cryptographically bound to the identifier of the End-User who possesses the Credential. Cryptographic Key Binding allows the Verifier to verify during the presentation of a Credential that the End-User presenting a Credential is the same End-User to whom that Credential was issued. For non-cryptographic types of binding and Credentials issued without any binding, see the Implementation Considerations in [Section 14.1](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#claims-based-binding) and [Section 14.2](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#no-binding).
Note: Claims in the Credential are about the subject of the Credential, which is often the End-User who possesses it.
For Cryptographic Key Binding, the Client has different options to provide Cryptographic Key Binding material for a requested Credential within a proof of a certain proof type. A proof type may provide the cryptographic public key(s) either with corresponding proof(s) of possession of the private key(s) or with key attestation(s). Proof types are defined in [Appendix F](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#proof-types).


### 8.2. Credential Request
A Client makes a Credential Request to the Credential Endpoint by sending the following parameters in the entity-body of an HTTP POST request. The Credential Request MAY be encrypted (on top of TLS) using the `credential_request_encryption` parameter in [Section 12.2](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-issuer-metadata) as specified in [Section 10](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#encrypted-messages).

- 
            `credential_identifier`: REQUIRED when an Authorization Details of type `openid_credential` was returned from the Token Response. It MUST NOT be used otherwise. A string that identifies a Credential Dataset that is requested for issuance. When this parameter is used, the `credential_configuration_id` MUST NOT be present.

          - 
            `credential_configuration_id`: REQUIRED if a `credential_identifiers` parameter was not returned from the Token Response as part of the `authorization_details` parameter. It MUST NOT be used otherwise. String that uniquely identifies one of the keys in the name/value pairs stored in the `credential_configurations_supported` Credential Issuer metadata. The corresponding object in the `credential_configurations_supported` map MUST contain one of the value(s) used in the `scope` parameter in the Authorization Request. When this parameter is used, the `credential_identifier` MUST NOT be present.

          - 
            `proofs`: OPTIONAL. Object providing one or more proof of possessions of the cryptographic key material to which the issued Credential instances will be bound to. The `proofs` parameter contains exactly one parameter named as the proof type in [Appendix F](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#proof-types), the value set for this parameter is a non-empty array containing parameters as defined by the corresponding proof type.

          - 
            `credential_response_encryption`: OPTIONAL. Object containing information for encrypting the Credential Response. If this request element is not present, the corresponding credential response returned is not encrypted.

- 
                `jwk`: REQUIRED. Object containing a single public key as a JWK used for encrypting the Credential Response.

              - 
                `enc`: REQUIRED. JWE [[RFC7516](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC7516)] `enc` algorithm [[RFC7518](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC7518)] for encrypting Credential Responses.

              - 
                `zip`: OPTIONAL. JWE [[RFC7516](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC7516)] `zip` algorithm [[RFC7518](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC7518)] for compressing Credential Responses prior to encryption. If absent then compression MUST not be used.

            

        
See [Section 3.3.4](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#identifying_credential) for the summary of the options how requested Credential(s) are identified throughout the Issuance flow.
The proof type contained in the `proofs` parameter is an extension point that enables the use of different types of proofs for different cryptographic schemes.
The proof(s) in the `proofs` parameter MUST incorporate the Credential Issuer Identifier (audience) and, if the Credential Issuer has a Nonce Endpoint, a `c_nonce` value to allow the Credential Issuer to detect freshness. The way that data is incorporated depends on the key proof type. In a JWT, for example, the `c_nonce` value is conveyed in the `nonce` claim, whereas the audience is conveyed in the `aud` claim. In a Linked Data proof, for example, the `c_nonce` is included as the `challenge` element in the key proof object and the Credential Issuer (the intended audience) is included as the `domain` element.
The `proofs` parameter MUST be present if the `proof_types_supported` parameter is present in the `credential_configurations_supported` parameter of the Issuer metadata for the requested Credential.
The `c_nonce` value is retrieved from the Nonce Endpoint as defined in [Section 7](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#nonce-endpoint).
Additional Credential Request parameters MAY be defined and used.
The Credential Issuer MUST ignore any unrecognized parameters.
The Credential Issuer indicates support for encrypted requests by including the `credential_request_encryption` parameter in the Credential Issuer Metadata. The Client MAY encrypt the request when `encryption_required` is `false` and MUST do so when `encryption_required` is `true`.
When performing Credential Request encryption, the Client MUST encode the information in the Credential Request in a JWT as specified by [Section 10](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#encrypted-messages), using the parameters from the `credential_request_encryption` object in the Credential Issuer Metadata.
If the Credential Request is not encrypted, the media type of the request MUST be set to `application/json`.
Below is a non-normative example of a Credential Request for a Credential in [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#ISO.18013-5)] format using the Credential configuration identifier and a key proof type `jwt` (with line breaks within values for display purposes only):

```
POST /credential HTTP/1.1
Host: server.example.com
Content-Type: application/json
Authorization: Bearer czZCaGRSa3F0MzpnWDFmQmF0M2JW

{
  "credential_configuration_id": "org.iso.18013.5.1.mDL",
  "proofs": {
    "jwt": [
      "eyJraWQiOiJkaWQ6ZXhhbXBsZTplYmZlYjFmNzEyZWJjNmYxYzI3NmUxMmVjMjEva2V5cy8x
       IiwiYWxnIjoiRVMyNTYiLCJ0eXAiOiJKV1QifQ"
    ]
  }
}
```

Below is a non-normative example of a Credential Request for two Credential instances in an IETF SD-JWT VC [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#I-D.ietf-oauth-sd-jwt-vc)] format using a Credential identifier from the Token Response and key proof type `jwt` (with line breaks within values for display purposes only):

```
POST /credential HTTP/1.1
Host: server.example.com
Content-Type: application/json
Authorization: Bearer czZCaGRSa3F0MzpnWDFmQmF0M2JW

{
  "credential_identifier": "CivilEngineeringDegree-2023",
  "proofs": {
    "jwt": [
      "eyJ0eXAiOiJvcGVuaWQ0dmNpLXByb29mK2p3dCIsImFsZyI6IkVTMjU2IiwiandrIjp7Imt0
       eSI6IkVDIiwiY3J2IjoiUC0yNTYiLCJ4IjoiblVXQW9BdjNYWml0aDhFN2kxOU9kYXhPTFlG
       T3dNLVoyRXVNMDJUaXJUNCIsInkiOiJIc2tIVThCalVpMVU5WHFpN1N3bWo4Z3dBS18weGtj
       RGpFV183MVNvc0VZIn19",
      "eyJraWQiOiJkaWQ6ZXhhbXBsZTplYmZlYjFmNzEyZWJjNmYxYzI3NmUxMmVjMjEva2V5cy8x
       IiwiYWxnIjoiRVMyNTYiLCJ0eXAiOiJKV1QifQ"
    ]
  }
}
```

Below is a non-normative example of a Credential Request for one Credential in W3C VCDM format using a Credential identifier from the Token Response and key proof type `di_vp` (with line breaks within values for display purposes only):

```
POST /credential HTTP/1.1
Host: server.example.com
Content-Type: application/json
Authorization: BEARER czZCaGRSa3F0MzpnWDFmQmF0M2JW

{
  "credential_identifier": "CivilEngineeringDegree-2023",
  "proofs": {
    "di_vp": [
      {
        "@context": [
          "https://www.w3.org/ns/credentials/v2",
          "https://www.w3.org/ns/credentials/examples/v2"
        ],
        "type": [
          "VerifiablePresentation"
        ],
        "holder": "did:key:z6MkvrFpBNCoYewiaeBLgjUDvLxUtnK5R6mqh5XPvLsrPsro",
        "proof": [
          {
            "type": "DataIntegrityProof",
            "cryptosuite": "eddsa-2022",
            "proofPurpose": "authentication",
            "verificationMethod": "did:key:z6MkvrFpBNCoYewiaeBLgjUDvLxUtnK5R6mq
             h5XPvLsrPsro#z6MkvrFpBNCoYewiaeBLgjUDvLxUtnK5R6mqh5XPvLsrPsro",
            "created": "2023-03-01T14:56:29.280619Z",
            "challenge": "82d4cb36-11f6-4273-b9c6-df1ac0ff17e9",
            "domain": "did:web:audience.company.com",
            "proofValue": "z5hrbHzZiqXHNpLq6i7zePEUcUzEbZKmWfNQzXcUXUrqF7bykQ7A
             CiWFyZdT2HcptF1zd1t7NhfQSdqrbPEjZceg7"
          }
        ]
      }
    ]
  }
}
```

The Credential Issuer indicates support for encrypted responses by including the `credential_response_encryption` parameter in the Credential Issuer Metadata. The Client MAY request encrypted responses by providing its encryption parameters in the Credential Request when `encryption_required` is `false` and MUST do so when `encryption_required` is `true`. Credential Request encryption MUST be used if the `credential_response_encryption` parameter is included, to prevent it being substituted by an attacker.


### 8.3. Credential Response
The Credential Response can either be returned immediately or in a deferred manner. The response can contain one or more Credentials with the same Credential Configuration and Credential Dataset depending on the Credential Request:

- If the Credential Issuer is able to immediately issue the requested Credentials, it MUST respond with the HTTP status code 200 (see Section 15.3.3 of [[RFC9110](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC9110)]).

          - If the Credential Issuer is not able to immediately issue the requested credentials (e.g., due to a manual review process being required or the data used to issue the credential is not ready yet), the Credential Issuer MUST return a response with a `transaction_id` parameter. In this case, the Credential Issuer MUST also use the HTTP status code 202 for the response. The `transaction_id` MAY be used by the Client at a later time at the Deferred Credential endpoint.

        
If the Client requested an encrypted response by including the `credential_response_encryption` object in the request, the Credential Issuer MUST encode the information in the Credential Response as specified by [Section 10](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#encrypted-messages), using the parameters from the `credential_response_encryption` object. Note that this is done regardless of the content.
If the Credential Response is not encrypted, the media type of the response MUST be set to `application/json`.
The following parameters are used in the JSON-encoded Credential Response body:

- 
            `credentials`: OPTIONAL. Contains an array of one or more issued Credentials. It MUST NOT be used if the `transaction_id` parameter is present. The elements of the array MUST be objects. The number of elements in the `credentials` array matches the number of keys that the Wallet has provided via the `proofs` parameter of the Credential Request, unless the Issuer decides to issue fewer Credentials. Each key provided by the Wallet is used to bind to, at most, one Credential. This specification defines the following parameters to be used inside this object:

- 
                `credential`: REQUIRED. Contains one issued Credential. The encoding of the Credential depends on the Credential Format and MAY be a string or an object. Credential Formats expressed as binary data MUST be base64url-encoded and returned as a string. More details are defined in the Credential Format Profiles in [Appendix A](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#format-profiles).

            

          - 
            `transaction_id`: OPTIONAL. String identifying a Deferred Issuance transaction. This parameter is contained in the response if the Credential Issuer cannot immediately issue the Credential. The value is subsequently used to obtain the respective Credential with the Deferred Credential Endpoint (see [Section 9](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#deferred-credential-issuance)). It MUST not be used if the `credentials` parameter is present. It MUST be invalidated after the Credential for which it was meant has been obtained by the Wallet.

          - 
            `interval`: REQUIRED if `transaction_id` is present. Contains a positive number that represents the minimum amount of time in seconds that the Wallet SHOULD wait after receiving the response before sending a new request to the Deferred Credential Endpoint. It MUST NOT be used if the `credentials` parameter is present.

          - 
            `notification_id`: OPTIONAL. String identifying one or more Credentials issued in one Credential Response. It MUST be included in the Notification Request as defined in [Section 11.1](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#notification). It MUST not be used if the `credentials` parameter is not present.

        
Additional Credential Response parameters MAY be defined and used. The Wallet MUST ignore any unrecognized parameters.
Below is a non-normative example of a Credential Response in an immediate issuance flow for a Credential in JWT VC format (JSON encoded):

```
HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: no-store

{
  "credentials": [
    {
      "credential": "LUpixVCWJk0eOt4CXQe1NXK....WZwmhmn9OQp6YxX0a2L"
    }
  ]
}
```

Below is a non-normative example of a Credential Response in an immediate issuance flow for multiple Credential instances in JWT VC format (JSON encoded) with an additional `notification_id` parameter:

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "credentials": [
    {
      "credential": "LUpixVCWJk0eOt4CXQe1NXK....WZwmhmn9OQp6YxX0a2L"
    },
    {
      "credential": "YXNkZnNhZGZkamZqZGFza23....29tZTIzMjMyMzIzMjMy"
    }
  ],
  "notification_id": "3fwe98js"
}
```

Below is a non-normative example of a Credential Response in a deferred flow:

```
HTTP/1.1 202 Accepted
Content-Type: application/json
Cache-Control: no-store

{
  "transaction_id": "8xLOxBtZp8",
  "interval" : 3600
}
```


#### 8.3.1. Credential Error Response
When the Credential Request is invalid or unauthorized, the Credential Issuer constructs the error response as defined in this section.


##### 8.3.1.1. Authorization Errors
If the Credential Request does not contain an Access Token that enables issuance of a requested Credential, the Credential Endpoint returns an authorization error response such as defined in Section 3 of [[RFC6750](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC6750)].


##### 8.3.1.2. Credential Request Errors
For errors related to the Credential Request's payload, such as issues with `type`, `format`, `proofs`, encryption parameters, or if the request is denied, the specific error codes from this section MUST be used instead of the generic `invalid_request` parameter defined in Section 3.1 of [[RFC6750](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC6750)].
If the Wallet is requesting the issuance of a Credential that is not supported by the Credential Endpoint, the HTTP response MUST use the HTTP status code 400 (Bad Request) and set the content type to `application/json` with the following parameters in the JSON-encoded response body:

- 
                `error`: REQUIRED. The `error` parameter SHOULD be a single ASCII [[USASCII](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#USASCII)] error code from the following:

- 
                    `invalid_credential_request`: The Credential Request is missing a required parameter, includes an unsupported parameter or parameter value, repeats the same parameter, or is otherwise malformed.

                  - 
                    `unknown_credential_configuration`: Requested Credential Configuration is unknown.

                  - 
                    `unknown_credential_identifier`: Requested Credential identifier is unknown.

                  - 
                    `invalid_proof`: The `proofs` parameter in the Credential Request is invalid: (1) if the field is missing, or (2) one of the provided key proofs is invalid, or (3) if at least one of the key proofs does not contain a `c_nonce` value (refer to [Section 7.2](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#nonce-response)).

                  - 
                    `invalid_nonce`: The `proofs` parameter in the Credential Request uses an invalid nonce: at least one of the key proofs contains an invalid `c_nonce` value. The wallet should retrieve a new `c_nonce` value (refer to [Section 7](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#nonce-endpoint)).

                  - 
                    `invalid_encryption_parameters`: This error occurs when the encryption parameters in the Credential Request are either invalid or missing. In the latter case, it indicates that the Credential Issuer requires the Credential Response to be sent encrypted, but the Credential Request does not contain the necessary encryption parameters.

                  - 
                    `credential_request_denied`: The Credential Request has not been accepted by the Credential Issuer. The Wallet SHOULD treat this error as unrecoverable, meaning if received from a Credential Issuer the Credential cannot be issued.

                

              - 
                `error_description`: OPTIONAL. The `error_description` parameter MUST be a human-readable ASCII [[USASCII](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#USASCII)] text, providing any additional information used to assist the Client implementers in understanding the occurred error. The values for the `error_description` parameter MUST NOT include characters outside the set `%x20-21 / %x23-5B / %x5D-7E`.

            
The usage of these parameters takes precedence over the `invalid_request` parameter defined in [Section 8.3.1.1](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#authorization-errors), since they provide more details about the errors.
Note that Credential Error Responses are never encrypted, even if a valid Credential Response would have been.
The following is a non-normative example of a Credential Error Response where an unsupported Credential Format was requested:

```
HTTP/1.1 400 Bad Request
Content-Type: application/json
Cache-Control: no-store

{
  "error": "unknown_credential_configuration"
}
```
