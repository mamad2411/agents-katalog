---
name: "oid4vci-issuer-metadata"
description: "Use when configuring Credential Issuer metadata or discovering issuer capabilities. Covers: .well-known endpoints, credential_configurations_supported, display properties, proof types supported, and issuer discovery."
sections:
  - "4. Credential Offer Endpoint"
  - "4.1. Credential Offer"
  - "4.2. Credential Offer Response"
  - "5. Authorization Endpoint"
  - "5.1. Authorization Request"
  - "5.2. Successful Authorization Response"
  - "5.3. Authorization Error Response"
---

<!-- ARF version: 1.0-2025-02-03 -->
<!-- Tokens: ~5738 -->

## 4. Credential Offer Endpoint
This endpoint is used by a Credential Issuer that is already interacting with an End-User who wishes to initiate a Credential issuance. It is used to pass available information relevant for the Credential issuance to ensure a convenient and secure process.


### 4.1. Credential Offer
The Credential Issuer makes a Credential Offer by allowing the End-User to invoke the Wallet using the Wallet's Credential Offer Endpoint defined in [Section 12.1](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#client-metadata). For example, by clicking a link and/or rendering a QR code containing the Credential Offer that the End-User can scan in a wallet or an arbitrary camera application.
Credential Issuers MAY also communicate Credential Offers directly to a Wallet's backend, but any mechanism for doing so is currently outside the scope of this specification.
The Credential Offer object, which is a JSON-encoded object with the Credential Offer parameters, can be sent by value or by reference.
The Credential Offer contains a single URI query parameter, either `credential_offer` or `credential_offer_uri`:

- 
            `credential_offer`: Object with the Credential Offer parameters. This MUST NOT be present when the `credential_offer_uri` parameter is present.

          - 
            `credential_offer_uri`: String that is a URL using the `https` scheme referencing a resource containing a JSON object with the Credential Offer parameters. This MUST NOT be present when the `credential_offer` parameter is present.

        
For security considerations, see [Section 13.5](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-offer-security).


#### 4.1.1. Credential Offer Parameters
This specification defines the following parameters for the JSON-encoded Credential Offer object:

- 
              `credential_issuer`: REQUIRED. The URL of the Credential Issuer, as defined in [Section 12.2.1](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-issuer-identifier), from which the Wallet is requested to obtain one or more Credentials. The Wallet uses it to obtain the Credential Issuer's Metadata following the steps defined in [Section 12.2.2](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-issuer-wellknown).

            - 
              `credential_configuration_ids`: REQUIRED. A non-empty array of unique strings that each identify one of the keys in the name/value pairs stored in the `credential_configurations_supported` Credential Issuer metadata. The Wallet uses these string values to obtain the respective object that contains information about the Credential being offered as defined in [Section 12.2.4](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-issuer-parameters). For example, these string values can be used to obtain `scope` values to be used in the Authorization Request.

            - 
              `grants`: OPTIONAL. Object indicating to the Wallet the Grant Types the Credential Issuer's Authorization Server is prepared to process for this Credential Offer. Every grant is represented by a name/value pair. The name is the Grant Type identifier; the value is an object that contains parameters either determining the way the Wallet MUST use the particular grant and/or parameters the Wallet MUST send with the respective request(s). If `grants` is not present or is empty, the Wallet MUST determine the Grant Types the Credential Issuer's Authorization Server supports using the respective metadata. When multiple grants are present, it is at the Wallet's discretion which one to use.

          
Additional Credential Offer parameters MAY be defined and used.
The Wallet MUST ignore any unrecognized parameters.
The following values are defined by this specification:

- 
              Grant Type `authorization_code`:

- 
                  `issuer_state`: OPTIONAL. String value created by the Credential Issuer and opaque to the Wallet that is used to bind the subsequent Authorization Request with a context set up during previous process steps. If the Wallet decides to use the Authorization Code Flow and received a value for this parameter, it MUST include it in the subsequent Authorization Request to the Authorization Server as the `issuer_state` parameter value.

                - 
                  `authorization_server`: OPTIONAL string that the Wallet can use to identify the Authorization Server to use with this grant type when `authorization_servers` parameter in the Credential Issuer metadata has multiple entries. It MUST NOT be used otherwise. The value of this parameter MUST match with one of the values in the `authorization_servers` array obtained from the Credential Issuer metadata.

              

            - 
              Grant Type `urn:ietf:params:oauth:grant-type:pre-authorized_code`:

- 
                  `pre-authorized_code`: REQUIRED. The code representing the Credential Issuer's authorization for the Wallet to obtain Credentials of a certain type. This code MUST be short lived and single use. If the Wallet decides to use the Pre-Authorized Code Flow, this parameter value MUST be included in the subsequent Token Request with the Pre-Authorized Code Flow.

                - 
                  `tx_code`: OPTIONAL. Object indicating that a Transaction Code is required if present, even if empty. It describes the requirements for a Transaction Code, which the Authorization Server expects the End-User to present along with the Token Request in a Pre-Authorized Code Flow. If the Authorization Server does not expect a Transaction Code, this object is absent; this is the default. The Transaction Code is intended to bind the Pre-Authorized Code to a certain transaction to prevent replay of this code by an attacker that, for example, scanned the QR code while standing behind the legitimate End-User. It is RECOMMENDED to send the Transaction Code via a separate channel. If the Wallet decides to use the Pre-Authorized Code Flow, the Transaction Code value MUST be sent in the `tx_code` parameter with the respective Token Request as defined in [Section 6.1](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#token-request). If no `length`, `description`, or `input_mode` is given, this object MAY be empty.

- 
                      `input_mode` : OPTIONAL. String specifying the input character set. Possible values are `numeric` (only digits) and `text` (any characters). The default is `numeric`.

                    - 
                      `length`: OPTIONAL. Integer specifying the length of the Transaction Code. This helps the Wallet to render the input screen and improve the user experience.

                    - 
                      `description`: OPTIONAL. String containing guidance for the Holder of the Wallet on how to obtain the Transaction Code, e.g., describing over which communication channel it is delivered. The Wallet is RECOMMENDED to display this description next to the Transaction Code input screen to improve the user experience. The length of the string MUST NOT exceed 300 characters. The `description` does not support internationalization, however the Issuer MAY detect the Holder's language by previous communication or an HTTP Accept-Language header within an HTTP GET request for a Credential Offer URI.

                  

                - 
                  `authorization_server`: OPTIONAL string that the Wallet can use to identify the Authorization Server to use with this grant type when `authorization_servers` parameter in the Credential Issuer metadata has multiple entries. It MUST NOT be used otherwise. The value of this parameter MUST match with one of the values in the `authorization_servers` array obtained from the Credential Issuer metadata.

              

          
The following non-normative example shows a Credential Offer object where the Credential Issuer can offer the issuance of two different Credentials (which may even be of different formats):

```
{
  "credential_issuer": "https://credential-issuer.example.com",
  "credential_configuration_ids": [
    "UniversityDegreeCredential",
    "org.iso.18013.5.1.mDL"
  ],
  "grants": {
    "urn:ietf:params:oauth:grant-type:pre-authorized_code": {
      "pre-authorized_code": "oaKazRN8I0IbtZ0C7JuMn5",
      "tx_code": {
        "length": 4,
        "input_mode": "numeric",
        "description": "Please provide the one-time code that was sent via e-mail"
      }
    }
  }
}
```


#### 4.1.2. Sending Credential Offer by Value Using credential_offer Parameter
Below is a non-normative example of a Credential Offer passed by value (with line breaks within values for display purposes only):

```
GET /credential_offer?
  credential_offer=%7B%22credential_issuer%22:%22https://credential-issuer.exam
  ple.com%22,%22credential_configuration_ids%22:%5B%22UniversityDegree_JWT%22,%
  22org.iso.18013.5.1.mDL%22%5D,%22grants%22:%7B%22urn:ietf:params:oauth:grant-
  type:pre-authorized_code%22:%7B%22pre-authorized_code%22:%22oaKazRN8I0IbtZ0C7
  JuMn5%22,%22tx_code%22:%7B%7D%7D%7D%7D
```

The following is a non-normative example of a Credential Offer that can be included in a QR code or a link used to invoke a Wallet deployed as a native app (with line breaks within values for display purposes only):

```
openid-credential-offer://?
  credential_offer=%7B%22credential_issuer%22:%22https://credential-issuer.exam
  ple.com%22,%22credential_configuration_ids%22:%5B%22org.iso.18013.5.1.mDL%22%
  5D,%22grants%22:%7B%22urn:ietf:params:oauth:grant-type:pre-authorized_code%22
  :%7B%22pre-authorized_code%22:%22oaKazRN8I0IbtZ0C7JuMn5%22,%22tx_code%22:%7B%
  22input_mode%22:%22text%22,%22description%22:%22Please%20enter%20the%20serial
  %20number%20of%20your%20physical%20drivers%20license%22%7D%7D%7D%7D
```


#### 4.1.3. Sending Credential Offer by Reference Using credential_offer_uri Parameter
Upon receipt of the `credential_offer_uri`, the Wallet MUST send an HTTP GET request to the URI to retrieve the referenced Credential Offer Object, unless it is already cached, and parse it to recreate the Credential Offer parameters.
Note: The Credential Issuer SHOULD use a unique URI for each Credential Offer utilizing distinct parameters, or otherwise prevent the Credential Issuer from caching the `credential_offer_uri`.
Below is a non-normative example of this fetch process:

```
GET /credential_offer HTTP/1.1
Host: server.example.com
```

The response from the Credential Issuer that contains a Credential Offer Object MUST use the media type `application/json`.
This ability to pass the Credential Offer by reference is particularly useful for large Credential Offer objects.
When the Credential Offer is displayed as a QR code, it would usually contain the Credential Offer by reference due to the size limitations of the QR codes. Below is a non-normative example:

```
openid-credential-offer://?
  credential_offer_uri=https%3A%2F%2Fserver%2Eexample%2Ecom%2Fcredential-offer
  %2FGkurKxf5T0Y-mnPFCHqWOMiZi4VS138cQO_V7PZHAdM
```

Below is a non-normative example of a response from the Credential Issuer that contains a Credential Offer Object used to encourage the Wallet to start an Authorization Code Flow:

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "credential_issuer": "https://credential-issuer.example.com",
  "credential_configuration_ids": [
    "UniversityDegreeCredential"
  ],
  "grants": {
    "authorization_code": {
      "issuer_state": "eyJhbGciOiJSU0Et...FYUaBy"
    }
  }
}
```

Below is a non-normative example of a Credential Offer Object for a Pre-Authorized Code Flow (with a Credential type reference):

```
{
  "credential_issuer": "https://credential-issuer.example.com",
  "credential_configuration_ids": [
    "UniversityDegree_LDP_VC"
  ],
  "grants": {
    "urn:ietf:params:oauth:grant-type:pre-authorized_code": {
      "pre-authorized_code": "adhjhdjajkdkhjhdj",
      "tx_code": {}
    }
  }
}
```

When retrieving the Credential Offer from the Credential Offer URL, the `application/json` media type MUST be used. The Credential Offer cannot be signed and MUST NOT use `application/jwt` with `"alg": "none"`.


### 4.2. Credential Offer Response
The Wallet does not create a response. UX control stays with the Wallet after completion of the process.

---

## 5. Authorization Endpoint
The Authorization Endpoint is used in the same manner as defined in [[RFC6749](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC6749)]. Implementers SHOULD follow the best current practices for OAuth 2.0 Security given in [[BCP240](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#BCP240)].
When the grant type `authorization_code` is used, it is RECOMMENDED to use PKCE [[RFC7636](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC7636)] and Pushed Authorization Requests [[RFC9126](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC9126)]. PKCE prevents authorization code interception attacks. Pushed Authorization Requests ensure the integrity and authenticity of the authorization request.


### 5.1. Authorization Request
An Authorization Request is an OAuth 2.0 Authorization Request as defined in Section 4.1.1 of [[RFC6749](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC6749)], which requests that access be granted to the Credential Endpoint, as defined in [Section 8](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-endpoint).
There are two possible methods for requesting the issuance of a specific Credential type in an Authorization Request. The first method involves using the `authorization_details` request parameter, as defined in [[RFC9396](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC9396)], containing one or more authorization details of type `openid_credential`, as specified in [Section 5.1.1](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#authorization-details). The second method utilizes scopes, as outlined in [Section 5.1.2](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-request-using-type-specific-scope).
See [Section 3.3.4](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#identifying_credential) for the summary of the options how requested Credential(s) are identified throughout the Issuance flow.


#### 5.1.1. Using Authorization Details Parameter
Credential Issuers MAY support requesting authorization to issue a Credential using the `authorization_details` parameter.
The request parameter `authorization_details` defined in Section 2 of [[RFC9396](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC9396)] MUST be used to convey the details about the Credentials the Wallet wants to obtain. This specification introduces a new authorization details type `openid_credential` and defines the following parameters to be used with this authorization details type:

- 
              `type`: REQUIRED. String that determines the authorization details type. It MUST be set to `openid_credential` for the purpose of this specification.

            - 
              `credential_configuration_id`: REQUIRED. String specifying a unique identifier of the Credential being described in the `credential_configurations_supported` map in the Credential Issuer Metadata as defined in [Section 12.2.4](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-issuer-parameters). The referenced object in the `credential_configurations_supported` map conveys the details of the requested Credential, such as the format and format-specific parameters like `vct` for SD-JWT VC or `doctype` for ISO mdoc. This specification defines those Credential Format specific Issuer Metadata in [Appendix A](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#format-profiles).

            - 
              `claims`: OPTIONAL. A non-empty array of claims description objects as defined in [Appendix B.1](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#claims-description-authorization-details).

          
Additional `authorization_details` data fields MAY be defined and used when the `type` value is `openid_credential`.
Note that this effectively defines an authorization details type that is never considered invalid due to unknown fields.
The following is a non-normative example of an `authorization_details` object with a `credential_configuration_id`:

```
[
  {
    "type": "openid_credential",
    "credential_configuration_id": "UniversityDegreeCredential"
  }
]
```

If the Credential Issuer metadata contains an `authorization_servers` parameter, the authorization detail's `locations` common data field MUST be set to the Credential Issuer Identifier value. A non-normative example for a deployment where an Authorization Server protects multiple Credential Issuers would look like this:

```
[
  {
    "type": "openid_credential",
    "locations": [
      "https://credential-issuer.example.com"
    ],
    "credential_configuration_id": "UniversityDegreeCredential"
  }
]
```

Below is a non-normative example of an Authorization Request using the `authorization_details` parameter that would be sent by the User Agent to the Authorization Server in response to an HTTP 302 redirect response by the Wallet (with line breaks within values for display purposes only):

```
GET /authorize?
  response_type=code
  &client_id=s6BhdRkqt3
  &code_challenge=E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM
  &code_challenge_method=S256
  &authorization_details=%5B%7B%22type%22%3A%20%22openid_credential%22%2C%20%22
    credential_configuration_id%22%3A%20%22UniversityDegreeCredential%22%7D%5D
  &redirect_uri=https%3A%2F%2Fwallet.example.org%2Fcb

Host: server.example.com
```

This non-normative example requests authorization to issue two different Credentials:

```
[
  {
    "type": "openid_credential",
    "credential_configuration_id": "UniversityDegreeCredential"
  },
  {
    "type": "openid_credential",
    "credential_configuration_id": "org.iso.18013.5.1.mDL"
  }
]
```

Note: Applications MAY combine authorization details of type `openid_credential` with any other authorization details types in an Authorization Request.


#### 5.1.2. Using scope Parameter to Request Issuance of a Credential
Credential Issuers MAY support requesting authorization to issue a Credential using the OAuth 2.0 `scope` parameter.
When the Wallet does not know which scope value to use to request issuance of a certain Credential, it can discover it using the `scope` Credential Issuer metadata parameter defined in [Section 12.2.4](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-issuer-parameters). When the flow starts with a Credential Offer, the Wallet can use the `credential_configuration_ids` parameter values to identify object(s) in the `credential_configurations_supported` map in the Credential Issuer metadata parameter and use the `scope` parameter value from that object.
The Wallet can discover the scope values using other options such as normative text in a profile of this specification that defines scope values along with a description of their semantics.
The concrete `scope` values are out of scope of this specification.
The Wallet MAY combine scopes discovered from the Credential Issuer metadata with the scopes discovered from the Authorization Server metadata.
It is RECOMMENDED to use collision-resistant scope values.
Credential Issuers MUST interpret each scope value as a request to access the Credential Endpoint as defined in [Section 8](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-endpoint) for the issuance of a Credential type identified by that scope value. Multiple scope values MAY be present in a single request whereby each
occurrence MUST be interpreted individually.
Credential Issuers MUST ignore unknown scope values in a request.
If the Credential Issuer metadata contains an `authorization_servers` property, it is RECOMMENDED to use a `resource` parameter [[RFC8707](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC8707)] whose value is the Credential Issuer's identifier value to allow the Authorization Server to differentiate Credential Issuers.
Below is a non-normative example of an Authorization Request provided by the Wallet to the Authorization Server using the scope `UniversityDegreeCredential` and in response to an HTTP 302 redirect (with line breaks within values for display purposes only):

```
GET /authorize?
  response_type=code
  &scope=UniversityDegreeCredential
  &resource=https%3A%2F%2Fcredential-issuer.example.com
  &client_id=s6BhdRkqt3
  &code_challenge=E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM
  &code_challenge_method=S256
  &redirect_uri=https%3A%2F%2Fwallet.example.org%2Fcb
Host: server.example.com
```

If a scope value related to Credential issuance and the `authorization_details` request parameter containing objects of type `openid_credential` are both present in a single request, the Credential Issuer MUST interpret these individually. However, if both request the same Credential type, then the Credential Issuer MUST follow the request as given by the authorization details object.


#### 5.1.3. Additional Request Parameters
This specification defines the following request parameter that can be supplied in an Authorization Request:

- 
              `issuer_state`: OPTIONAL. String value identifying a certain processing context at the Credential Issuer. A value for this parameter is typically passed in a Credential Offer from the Credential Issuer to the Wallet (see [Section 4.1](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-offer)). This request parameter is used to pass the `issuer_state` value back to the Credential Issuer.

          
Note: When processing the Authorization Request, the Credential Issuer MUST take into account that the `issuer_state` is not guaranteed to originate from this Credential Issuer in all circumstances. It could have been injected by an attacker.
Additional Authorization Request parameters MAY be defined and used,
as described in [[RFC6749](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC6749)].
The Authorization Server MUST ignore any unrecognized parameters.


#### 5.1.4. Pushed Authorization Request
Use of Pushed Authorization Requests is RECOMMENDED to ensure confidentiality, integrity, and authenticity of the request data and to avoid issues caused by large requests sizes.
Below is a non-normative example of a Pushed Authorization Request:

```
POST /par HTTP/1.1
Host: server.example.com
OAuth-Client-Attestation: eyJ...
OAuth-Client-Attestation-PoP: eyJ...
Content-Type: application/x-www-form-urlencoded

response_type=code
&client_id=CLIENT1234
&code_challenge=E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM
&code_challenge_method=S256
&redirect_uri=https%3A%2F%2Fwallet.example.org%2Fcb
&authorization_details=...
```

Below is a non-normative example of a response to a successful request:

```
HTTP/1.1 201 Created
Content-Type: application/json
Cache-Control: no-cache, no-store

{
  "request_uri": "urn:ietf:params:oauth:request_uri:6esc_11ACC5bwc014ltc14eY22c",
  "expires_in": 60
}
```

Below is a non-normative example of the GET request that might subsequently be sent by the Browser:

```
GET /authorize?client_id=s6BhdRkqt3
  &request_uri=urn%3Aietf%3Aparams%3Aoauth%3Arequest_uri%3A6esc_11ACC5bwc014ltc14eY22c
Host: server.example.com
```


### 5.2. Successful Authorization Response
Authorization Responses MUST be made as defined in [[RFC6749](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC6749)].
Below is a non-normative example of a successful Authorization Response:

```
HTTP/1.1 302 Found
Location: https://wallet.example.org/cb?
  code=SplxlOBeZQQYbYS6WxSbIA
```


### 5.3. Authorization Error Response
The Authorization Error Response MUST be made as defined in [[RFC6749](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC6749)].
Below is a non-normative example of an unsuccessful Authorization Response:

```
HTTP/1.1 302 Found
Location: https://wallet.example.org/cb?
  error=invalid_request
  &error_description=Unsupported%20response_type%20value
```
