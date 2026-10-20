---
name: "oid4vci-credential-endpoint"
description: "Use when implementing the credential endpoint for issuing credentials. Covers: credential request format, proof of possession (key binding), credential response, error handling, and the nonce endpoint for fresh c_nonce values."
sections:
  - "9. Deferred Credential Endpoint"
  - "9.1. Deferred Credential Request"
  - "9.2. Deferred Credential Response"
  - "9.3. Deferred Credential Error Response"
  - "10. Encrypted Credential Requests and Responses"
---

<!-- ARF version: 1.0-2025-02-03 -->
<!-- Tokens: ~2144 -->

## 9. Deferred Credential Endpoint
This endpoint is used to issue one or more Credentials previously requested at the Credential Endpoint in cases where the Credential Issuer was not able to immediately issue this Credential. Support for this endpoint is OPTIONAL.
The Wallet MUST present to the Deferred Endpoint an Access Token that is valid for the issuance of the Credential(s) previously requested at the Credential Endpoint.
Communication with the Deferred Credential Endpoint MUST utilize TLS.


### 9.1. Deferred Credential Request
The Deferred Credential Request is an HTTP POST request. The Deferred Credential Request MAY be encrypted (on top of TLS) using the `credential_request_encryption` parameter in [Section 12.2](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-issuer-metadata) as specified in [Section 10](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#encrypted-messages).
The following parameters are used in the Deferred Credential Request:

- 
            `transaction_id`: REQUIRED. String identifying a Deferred Issuance transaction.

          - 
            `credential_response_encryption`: OPTIONAL. as defined in [Section 8.2](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-request).

        
The Credential Issuer MUST invalidate the `transaction_id` after the Credential for which it was meant has been obtained by the Wallet.
Additional Deferred Credential Request parameters MAY be defined and used.
The Credential Issuer MUST ignore any unrecognized parameters.
The Credential Issuer indicates support for encrypted requests by including the `credential_request_encryption` parameter in the Credential Issuer Metadata. The Client MAY encrypt the request when `encryption_required` is `false` and MUST do so when `encryption_required` is `true`.
When performing Deferred Credential Request encryption, the Client MUST encode the information in the Deferred Credential Request in a JWT as specified by [Section 10](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#encrypted-messages), using the parameters from the `credential_request_encryption` object in the Credential Issuer Metadata.
If the Deferred Credential Request is not encrypted, the media type of the request MUST be set to `application/json`.
The following is a non-normative example of a Deferred Credential Request:

```
POST /deferred_credential HTTP/1.1
Host: server.example.com
Content-Type: application/json
Authorization: Bearer czZCaGRSa3F0MzpnWDFmQmF0M2JW

{
  "transaction_id": "8xLOxBtZp8"
}
```

The Credential Issuer indicates support for encrypted responses by including the `credential_response_encryption` parameter in the Credential Issuer Metadata. The Client MAY request encrypted responses by providing its encryption parameters in the Deferred Credential Request when `encryption_required` is `false` and MUST do so when `encryption_required` is `true`. Note that this object will be used for encrypting the response, regardless of what was sent in the initial Credential Request. If it is not included encryption will not be performed. Deferred Credential Request encryption MUST but used if the `credential_response_encryption` parameter is included, to prevent it being substituted by an attacker.


### 9.2. Deferred Credential Response
A Deferred Credential Response may either contain the requested Credentials or further defer the issuance:

- If the Credential Issuer is able to issue the requested Credentials, the Deferred Credential Response MUST use the `credentials` parameter as defined in [Section 8.3](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-response) and MUST respond with the HTTP status code 200 (see Section 15.3.3 of [[RFC9110](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC9110)]).

          - If the Credential Issuer still requires more time, the Deferred Credential Response MUST use the `interval` and `transaction_id` parameters as defined in [Section 8.3](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-response) and it MUST respond with the HTTP status code 202 (see Section 15.3.3 of [[RFC9110](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC9110)]). The value of `transaction_id` MUST be same as the value of `transaction_id` in the Deferred Credential Request.

        
The Deferred Credential Response MAY use the `notification_id` parameter as defined in [Section 8.3](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-response).
Additional Deferred Credential Response parameters MAY be defined and used.
The Wallet MUST ignore any unrecognized parameters.
If the Client requested an encrypted response by including the `credential_response_encryption` object in the request, the Credential Issuer MUST encode the information in the Deferred Credential Response as specified by [Section 10](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#encrypted-messages), using the parameters from the `credential_response_encryption` object. Note that this is done regardless of the content. The `credential_response_encryption` object may be different from the one included in the initial Credential Request so the Credential Issuer MUST use the newly provided one. This is to simplify key management in the case of longer deferred issuance.
If the Deferred Credential Response is not encrypted, the media type of the response MUST be set to `application/json`.
The following is a non-normative example of a Deferred Credential Response containing Credentials:

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

The following is a non-normative example of a Deferred Credential Response, where the Credential Issuer still requires more time:

```
HTTP/1.1 202 OK
Content-Type: application/json

{
  "transaction_id": "8xLOxBtZp8",
  "interval": 86400
}
```


### 9.3. Deferred Credential Error Response
When the Deferred Credential Request is invalid, the Credential Issuer constructs the error response as defined in [Section 8.3.1](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-error-response).
The following additional error code is specified in addition to those already defined in [Section 8.3.1.2](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-request-errors):

- 
            `invalid_transaction_id`: The Deferred Credential Request contains an invalid `transaction_id`. This error occurs when the `transaction_id` was not issued by the respective Credential Issuer or it was already used to obtain a Credential.

        
This is a non-normative example of a Deferred Credential Error Response:

```
HTTP/1.1 400 Bad Request
Content-Type: application/json
Cache-Control: no-store

{
  "error": "invalid_transaction_id"
}
```

In the event the Credential Issuer can no longer issue the credential(s), the `credential_request_denied` error code as defined in [Section 8.3.1.2](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-request-errors) should be used in response to a request. A wallet upon receiving this error SHOULD stop making requests to the deferred credential endpoint for the given `transaction_id`.

---

## 10. Encrypted Credential Requests and Responses
Encryption of requests and responses for the Credential and Deferred Credential Endpoints is performed as follows:
The contents of the message MUST be encoded as a JWT as described in [[RFC7519](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC7519)]. The media type MUST be set to `application/jwt`.
The Public Key used to encrypt the message is selected based on the context. In the case where multiple public keys are available, any may be selected based on the information about each key, such as the `kty` (Key Type), `use` (Public Key Use), `alg` (Algorithm), and other JWK parameters. The `alg` parameter MUST be present. The JWE `alg` algorithm used MUST be equal to the `alg` value of the chosen JWK. If the selected public key contains a `kid` parameter, the JWE MUST include the same value in the `kid` JWE Header Parameter (as defined in [Section 4.1.6](https://rfc-editor.org/rfc/rfc7516)) of the encrypted message. This enables the easy identification of the specific public key that was used to encrypt the message. The JWE `enc` content encryption algorithm used is obtained based on context.
If a `zip` (Compression Algorithm) value is specified, then compression is performed before encryption, as specified in [[RFC7516](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC7516)]. If absent, no compression is performed.
When encryption of a message was required but the received message is unencrypted, it SHOULD be rejected.
For security considerations see [Section 13.11](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#encryption-security-considersations)
