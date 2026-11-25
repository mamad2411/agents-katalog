---
name: "oid4vci-batch-issuance"
description: "Use when implementing batch credential issuance. Covers: batch credential request format, batch credential response, and handling multiple credentials in a single issuance flow."
sections:
  - "11. Notification Endpoint"
  - "11.1. Notification Request"
  - "11.2. Successful Notification Response"
  - "11.3. Notification Error Response"
---

<!-- ARF version: 1.0-2025-02-03 -->
<!-- Tokens: ~1231 -->

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
