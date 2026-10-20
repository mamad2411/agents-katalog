---
name: "oid4vci-deferred-notification"
description: "Use when implementing deferred credential retrieval or notification endpoints. Covers: transaction_id for deferred issuance, deferred credential endpoint, and notification of credential acceptance or deletion."
sections:
  - "9. Deferred Credential Endpoint"
  - "9.1. Deferred Credential Request"
  - "9.2. Deferred Credential Response"
  - "9.3. Deferred Credential Error Response"
  - "11. Notification Endpoint"
  - "11.1. Notification Request"
  - "11.2. Successful Notification Response"
  - "11.3. Notification Error Response"
---

<!-- ARF version: 1.0-2025-02-03 -->
<!-- Tokens: ~2970 -->

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

## 11. Notification Endpoint
This endpoint is used by the Wallet to notify the Credential Issuer of certain events for issued Credentials. These events enable the Credential Issuer to take subsequent actions after issuance. The Credential Issuer needs to return one `notification_id` parameter per Credential Response or Deferred Credential Response for the Wallet to be able to use this endpoint. Support for this endpoint is OPTIONAL. The Issuer cannot assume that a notification will be sent for every issued Credential since the use of this Endpoint is not mandatory for the Wallet.
The Wallet MUST present to the Notification Endpoint a valid Access Token issued at the Token Endpoint as defined in [Section 6](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#token-endpoint).
A Credential Issuer that requires a request to the Notification Endpoint MUST ensure the Access Token issued by the Authorization Server is valid at the Notification Endpoint.
The notification from the Wallet is idempotent. When the Credential Issuer receives multiple identical calls from the Wallet for the same `notification_id`, it returns success. Due to the network errors, there are no guarantees that a Credential Issuer will receive a notification within a certain time period or at all.
Communication with the Notification Endpoint MUST utilize TLS.


### 11.1. Notification Request
The Wallet sends an HTTP POST request to the Notification Endpoint with the following parameters in the entity-body and using the `application/json` media type. If the Wallet supports the Notification Endpoint, the Wallet MAY send one or more Notification Requests per `notification_id` value received.

- 
            `notification_id`: REQUIRED. String received in the Credential Response or Deferred Credential Response identifying an issuance flow that contained one or more Credentials with the same Credential Configuration and Credential Dataset.

          - 
            `event`: REQUIRED. Type of the notification event. It MUST be a case sensitive string whose value is either `credential_accepted`, `credential_failure`, or `credential_deleted`. `credential_accepted` is to be used when the Credentials were successfully stored in the Wallet, with or without user action. `credential_deleted` is to be used when the unsuccessful Credential issuance was caused by a user action. In all other unsuccessful cases, `credential_failure` is to be used. Partial errors during issuance of multiple Credentials as a batch (e.g., one of the Credentials could not be stored) MUST be treated as the overall issuance flow failing.

          - 
            `event_description`: OPTIONAL. Human-readable ASCII [[USASCII](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#USASCII)] text providing additional information, used to assist the Credential Issuer developer in understanding the event that occurred. Values for the `event_description` parameter MUST NOT include characters outside the set `%x20-21 / %x23-5B / %x5D-7E`.

        
Additional Notification Request parameters MAY be defined and used.
The Credential Issuer MUST ignore any unrecognized parameters.
Below is a non-normative example of a Notification Request when a credential was successfully accepted by the End-User:

```
POST /notification HTTP/1.1
Host: server.example.com
Content-Type: application/json
Authorization: Bearer czZCaGRSa3F0MzpnWDFmQmF0M2JW

{
  "notification_id": "3fwe98js",
  "event": "credential_accepted"
}
```

Below is a non-normative example of a Notification Request when a Credential was deleted by the End-User:

```
POST /notification HTTP/1.1
Host: server.example.com
Content-Type: application/json
Authorization: Bearer czZCaGRSa3F0MzpnWDFmQmF0M2JW

{
  "notification_id": "3fwe98js",
  "event": "credential_failure",
  "event_description": "Could not store the Credential. Out of storage."
}
```


### 11.2. Successful Notification Response
When the Credential Issuer has successfully received the Notification Request from the Wallet, it MUST respond with an HTTP status code in the 2xx range. Use of the HTTP status code 204 (No Content) is RECOMMENDED.
Below is a non-normative example of a response to a successful Notification Request:

```
HTTP/1.1 204 No Content
```


### 11.3. Notification Error Response
If the Notification Request does not contain an Access Token or contains an invalid Access Token, the Notification Endpoint returns an Authorization Error Response, such as defined in Section 3 of [[RFC6750](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC6750)].
When the `notification_id` value is invalid, the HTTP response MUST use the HTTP status code 400 (Bad Request) and set the content type to `application/json` with the following parameters in the JSON-encoded response body:

- 
            `error`: REQUIRED. The value of the `error` parameter SHOULD be one of the following ASCII [[USASCII](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#USASCII)] error codes:

- 
                `invalid_notification_id`: The `notification_id` in the Notification Request was invalid.

              - 
                `invalid_notification_request`: The Notification Request is missing a required parameter, includes an unsupported parameter or parameter value, repeats the same parameter, or is otherwise malformed.

            

        
It is at the discretion of the Issuer to decide how to proceed after returning an error response.
The following is a non-normative example of a Notification Error Response when an invalid `notification_id` value was used:

```
HTTP/1.1 400 Bad Request
Content-Type: application/json
Cache-Control: no-store

{
  "error": "invalid_notification_id"
}
```
