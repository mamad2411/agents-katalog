---
name: "oid4vp-request-uri-jar"
description: "Use when implementing request_uri or JWT-Secured Authorization Requests (JAR) for OpenID4VP. Covers: request_uri parameter, request_uri methods (GET and POST), signed request objects, and request parameter passing."
sections:
  - "5.7. Passing Authorization Request Across Devices"
  - "5.8. aud of a Request Object"
  - "5.9. Client Identifier Prefix and Verifier Metadata Management"
  - "5.9.1. Syntax"
  - "5.9.2. Fallback"
  - "5.9.3. Defined Client Identifier Prefixes"
  - "5.10. Request URI Method post"
  - "5.10.1. Request URI Response"
  - "5.10.2. Request URI Error Response"
  - "5.11. Verifier Info"
  - "5.11.1. Proof of Possession"
---

<!-- ARF version: 1.0-final-2025-07-09 -->
<!-- Tokens: ~5101 -->

### 5.7. Passing Authorization Request Across Devices
There are use-cases when the Authorization Request is being displayed on a device different from a device on which the requested Credential is stored. In those cases, an Authorization Request can be passed across devices by being rendered as a QR Code.
The usage of the Response Mode `direct_post` (see [Section 8.2](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#response_mode_post)) in conjunction with `request_uri` is RECOMMENDED, since Authorization Request size might be large and might not fit in a QR code.

---

### 5.8. aud of a Request Object
When the Verifier is sending a Request Object as defined in [[RFC9101](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC9101)], the `aud` claim value depends on whether the recipient of the request can be identified by the Verifier or not:

- the `aud` claim MUST be equal to the `iss` (issuer) claim value, when Dynamic Discovery is performed.

          - the `aud` claim MUST be "[https://self-issued.me/v2"](https://self-issued.me/v2%22), when Static Discovery metadata is used.

        
Note: "[https://self-issued.me/v2"](https://self-issued.me/v2%22) is a symbolic string and can be used as an `aud` claim value even when this specification is used standalone, without SIOPv2.

---

### 5.9. Client Identifier Prefix and Verifier Metadata Management
This specification defines the concept of a Client Identifier Prefix that dictates how the Wallet needs to interpret the Client Identifier and associated data in the process of Client identification, authentication, and authorization.
The Client Identifier Prefix enables deployments of this specification to use different mechanisms to obtain and validate metadata of the Verifier beyond the scope of [[RFC6749](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC6749)]. The term Client Identifier Prefix is used since the Verifier is acting as an OAuth 2.0 Client.
The Client Identifier Prefix is a string that MAY be communicated by the Verifier in a prefix within the `client_id` parameter in the Authorization Request. A fallback to pre-registered Clients as in [[RFC6749](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC6749)] remains in place as a default mechanism in case no Client Identifier Prefix was provided. A certain Client Identifier Prefix may require the Verifier to sign the Authorization Request as a means of authentication and/or pass additional parameters and require the Wallet to process them.


#### 5.9.1. Syntax
In the `client_id` Authorization Request parameter and other places where the Client Identifier is used, the Client Identifier Prefixes are prefixed to the usual Client Identifier, separated by a `:` (colon) character:

```
<client_id_prefix>:<orig_client_id>
```

Here, `<client_id_prefix>` is the Client Identifier Prefix and `<orig_client_id>` is an identifier for the Client within the namespace of that prefix. See [Section 5.9.3](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#client_identifier_prefixes) for Client Identifier Prefixes defined by this specification.
Wallets MUST use the presence of a `:` (colon) character and the content preceding it to determine whether a Client Identifier Prefix is used. If a `:` character is present and the content preceding it is a recognized and supported Client Identifier Prefix value, the Wallet MUST interpret the Client Identifier according to the given Client Identifier Prefix. The Client Identifier Prefix is defined as the string before the (first) `:` character. Note that implementations should not assume that the presence of a `:` character implies that the entire value can be processed as a valid URI. Instead, the specific processing rules defined for the specified Client Identifier Prefix (see [Section 5.9.3](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#client_identifier_prefixes)) should be used to parse the `client_id` value.
For example, an Authorization Request might contain `client_id=verifier_attestation:example-client` to indicate that the `verifier_attestation` Client Identifier Prefix is to be used and that within this prefix, the Verifier can be identified by the string `example-client`. The presentation would contain the full `verifier_attestation:example-client` string as the audience (intended receiver) and the same full string would be used as the Client Identifier anywhere in the OAuth flow.
Note that the Verifier needs to determine which Client Identifier Prefixes the Wallet supports prior to sending the Authorization Request in order to choose a supported prefix.
Depending on the Client Identifier Prefix, the Verifier can communicate a JSON object with its metadata using the `client_metadata` parameter which contains name/value pairs.


#### 5.9.2. Fallback
If a `:` character is not present in the Client Identifier, the Wallet MUST treat the Client Identifier as referencing a pre-registered client. This is equivalent to the [[RFC6749](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC6749)] default behavior, i.e., the Client Identifier needs to be known to the Wallet in advance of the Authorization Request. The Verifier metadata is obtained using [[RFC7591](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC7591)] or through out-of-band mechanisms.
For example, if an Authorization Request contains `client_id=example-client`, the Wallet would interpret the Client Identifier as referring to a pre-registered client.
If a `:` character is present in the Client Identifier but the value preceding it is not a recognized and supported Client Identifier Prefix value, the Wallet can treat the Client Identifier as referring to a pre-registered client or it may refuse the request.
From this definition, it follows that pre-registered clients MUST NOT contain a `:` character preceded immediately by a supported Client Identifier Prefix value in the first part of their Client Identifier.


#### 5.9.3. Defined Client Identifier Prefixes
This specification defines the following Client Identifier Prefixes, followed by the examples where applicable.
In case of using OpenID4VP over DC API, as defined in [Appendix A](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#dc_api), it is at the discretion of the Wallet whether it validates the signature on the Request Object following the processing rules defined by a relevant Client Identifier Prefix. Factors that influence the Wallet's decision include, but are not limited to, the trust framework the Wallet supports, the specific policies defined by the Issuers or ecosystem, and profiles of this specification.

- 
              `redirect_uri`: This prefix value indicates that the original Client Identifier part (without the prefix `redirect_uri:`) is the Verifier's Redirect URI (or Response URI when Response Mode `direct_post` is used). The Verifier MAY omit the `redirect_uri` Authorization Request parameter (or `response_uri` when Response Mode `direct_post` is used). All Verifier metadata parameters MUST be passed using the `client_metadata` parameter defined in [Section 5.1](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#new_parameters). An example Client Identifier value is `redirect_uri:https://client.example.org/cb`. Requests using the `redirect_uri` Client Identifier Prefix cannot be signed because there is no method for the Wallet to obtain a trusted key for verification. Therefore, implementations requiring signed requests cannot use the `redirect_uri` Client Identifier Prefix.
The following is a non-normative example of an unsigned request with the `redirect_uri` Client Identifier Prefix:

```
HTTP/1.1 302 Found
Location: https://wallet.example.org/universal-link?
  response_type=vp_token
  &client_id=redirect_uri%3Ahttps%3A%2F%2Fclient.example.org%2Fcb
  &redirect_uri=https%3A%2F%2Fclient.example.org%2Fcb
  &dcql_query=...
  &nonce=n-0S6_WzA2Mj
  &client_metadata=%7B%22vp_formats_supported%22%3A%7B%22dc%2Bsd-jwt%22%3A%7B%22sd-jwt_
  alg_values%22%3A%20%5B%22ES256%22%5D%2C%22kb-jwt_alg_values%22%3A%20%5B%22ES256%22%5D
  %7D%7D%7D
```


            - 
              `openid_federation`: This prefix value indicates that the original Client Identifier (the part without the prefix `openid_federation:`) is an Entity Identifier defined in OpenID Federation [[OpenID.Federation](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#OpenID.Federation)]. Processing rules given in [[OpenID.Federation](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#OpenID.Federation)] MUST be followed. The Authorization Request MAY also contain a `trust_chain` parameter. The final Verifier metadata is obtained from the Trust Chain after applying the policies, according to [[OpenID.Federation](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#OpenID.Federation)]. The `client_metadata` parameter, if present in the Authorization Request, MUST be ignored when this Client Identifier Prefix is used. Example Client Identifier: `openid_federation:https://federation-verifier.example.com`.

            - 
              `decentralized_identifier`: This prefix value indicates that the original Client Identifier (the part without the prefix `decentralized_identifier:`) is a Decentralized Identifier as defined in [[DID-Core](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#DID-Core)]. The request MUST be signed with a private key associated with the DID. A public key to verify the signature MUST be obtained from the `verificationMethod` property of a DID Document. Since DID Document may include multiple public keys, a particular public key used to sign the request in question MUST be identified by the `kid` in the JOSE Header. To obtain the DID Document, the Wallet MUST use DID Resolution defined by the DID method used by the Verifier. All Verifier metadata other than the public key MUST be obtained from the `client_metadata` parameter as defined in [Section 5.1](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#new_parameters). Example Client Identifier: `decentralized_identifier:did:example:123`.
The following is a non-normative example of a header and a body of a signed Request Object when the Client Identifier Prefix is `decentralized_identifier`:
Header

```
{
  "typ": "oauth-authz-req+jwt",
  "alg": "RS256",
  "kid": "did:example:123#1"
}
```

Body

```
{
  "client_id": "decentralized_identifier:did:example:123",
  "response_type": "vp_token",
  "redirect_uri": "https://client.example.org/callback",
  "nonce": "n-0S6_WzA2Mj",
  "dcql_query": { ... },
  "client_metadata": {
    "vp_formats_supported": {
      "dc+sd-jwt": {
        "sd-jwt_alg_values": ["ES256", "ES384"],
        "kb-jwt_alg_values": ["ES256", "ES384"]
      }
    }
  }
}
```


            - 
              `verifier_attestation`: This Client Identifier Prefix allows the Verifier to authenticate using a JWT that is bound to a certain public key as defined in [Section 12](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#verifier_attestation_jwt). When the Client Identifier Prefix is `verifier_attestation`, the original Client Identifier (the part without the `verifier_attestation:` prefix) MUST equal the `sub` claim value in the Verifier attestation JWT. The request MUST be signed with the private key corresponding to the public key in the `cnf` claim in the Verifier attestation JWT. This serves as proof of possession of this key. The Verifier attestation JWT MUST be added to the `jwt` JOSE Header of the request object (see [Section 12](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#verifier_attestation_jwt)). The Wallet MUST validate the signature on the Verifier attestation JWT. The `iss` claim value of the Verifier Attestation JWT MUST identify a party the Wallet trusts for issuing Verifier Attestation JWTs. If the Wallet cannot establish trust, it MUST refuse the request. If the issuer of the Verifier Attestation JWT adds a `redirect_uris` claim to the attestation, the Wallet MUST ensure the `redirect_uri` request parameter value exactly matches one of the `redirect_uris` claim entries. All Verifier metadata other than the public key MUST be obtained from the `client_metadata` parameter. Example Client Identifier: `verifier_attestation:verifier.example`.

            - 
              `x509_san_dns`: When the Client Identifier Prefix is `x509_san_dns`, the original Client Identifier (the part after the `x509_san_dns:` prefix) MUST be a DNS name and match a `dNSName` Subject Alternative Name (SAN) [[RFC5280](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC5280)] entry in the leaf certificate passed with the request. The request MUST be signed with the private key corresponding to the public key in the leaf X.509 certificate of the certificate chain added to the request in the `x5c` JOSE header [[RFC7515](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC7515)] of the signed request object. The Wallet MUST validate the signature and the trust chain of the X.509 certificate. All Verifier metadata other than the public key MUST be obtained from the `client_metadata` parameter. The following requirement applies unless the interaction is using the DC API as defined in [Appendix A](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#dc_api): If the Wallet can establish trust in the Client Identifier authenticated through the certificate, e.g. because the Client Identifier is contained in a list of trusted Client Identifiers, it may allow the client to freely choose the `redirect_uri` value. If not, the FQDN of the `redirect_uri` value MUST match the Client Identifier without the prefix `x509_san_dns:`. Example Client Identifier: `x509_san_dns:client.example.org`.

            - 
              `x509_hash`: When the Client Identifier Prefix is `x509_hash`, the original Client Identifier (the part without the `x509_hash:` prefix) MUST be a hash and match the hash of the leaf certificate passed with the request. The request MUST be signed with the private key corresponding to the public key in the leaf X.509 certificate of the certificate chain added to the request in the `x5c` JOSE header parameter [[RFC7515](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC7515)] of the signed request object. The value of `x509_hash` is the base64url-encoded value of the SHA-256 hash of the DER-encoded X.509 certificate. The Wallet MUST validate the signature and the trust chain of the X.509 leaf certificate. All Verifier metadata other than the public key MUST be obtained from the `client_metadata` parameter. Example Client Identifier: `x509_hash:Uvo3HtuIxuhC92rShpgqcT3YXwrqRxWEviRiA0OZszk`

            - 
              `origin`: This reserved Client Identifier Prefix is defined in [Appendix A.2](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#dc_api_request). The Wallet MUST NOT accept this Client Identifier Prefix in requests. In OpenID4VP over the Digital Credentials API, the audience of the Credential Presentation is always the origin value prefixed by `origin:`, for example `origin:https://verifier.example.com/`.

          
To use the Client Identifier Prefixes `openid_federation`, `decentralized_identifier`, `verifier_attestation`, `x509_san_dns` and `x509_hash`, Verifiers MUST be capable of securely storing private key material. This might require changes to the technical design of native apps as such apps are typically public clients.
Other specifications can define further Client Identifier Prefixes. It is RECOMMENDED to use collision-resistant names for such values.

---

### 5.10. Request URI Method post
This request is handled by the Request URI endpoint of the Verifier.
The request MUST use the HTTP POST method with the `https` scheme, and the content type `application/x-www-form-urlencoded` and the `Accept` header set to `application/oauth-authz-req+jwt`. The names and values in the body MUST be encoded using UTF-8.
The following parameters are defined to be included in the request to the Request URI Endpoint:

          
`wallet_metadata`:
          OPTIONAL. A string containing a JSON object containing metadata parameters as defined in [Section 10](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#as_metadata_parameters).

          

`wallet_nonce`:
          OPTIONAL. A string value used to mitigate replay attacks of the Authorization Request. When received, the Verifier MUST use it as the `wallet_nonce` value in the signed authorization request object. Value can be a base64url-encoded, fresh, cryptographically random number with sufficient entropy.

        

If the Wallet requires the Verifier to encrypt the Request Object, it SHOULD use the `jwks` parameter within the `wallet_metadata` parameter to pass public encryption keys. If the Wallet requires an encrypted Authorization Response, it SHOULD specify supported encryption algorithms using the `authorization_encryption_alg_values_supported` and `authorization_encryption_enc_values_supported` parameters.
Additionally, if the Client Identifier Prefix permits signed Request Objects, the Wallet SHOULD list supported cryptographic algorithms for securing the Request Object through the `request_object_signing_alg_values_supported` parameter. Conversely, the Wallet MUST NOT include this parameter if the Client Identifier Prefix precludes signed Request Objects.
Additional parameters MAY be defined and used in the request to the Request URI Endpoint.
The Verifier MUST ignore any unrecognized parameters.
The following is a non-normative example of a request:

```
POST /request HTTP/1.1
Host: client.example.org
Content-Type: application/x-www-form-urlencoded

wallet_metadata=%7B%22vp_formats_supported%22%3A%7B%22dc%2Bsd-jwt%22%3A%7B%22sd-jwt_a
lg_values%22%3A%20%5B%22ES256%22%5D%2C%22kb-jwt_alg_values%22%3A%20%5B%22ES256%22%5D%
7D%7D%7D&
wallet_nonce=qPmxiNFCR3QTm19POc8u
```


#### 5.10.1. Request URI Response
The Request URI response MUST be an HTTP response with the content type `application/oauth-authz-req+jwt` and the body being a signed, optionally encrypted, request object as defined in [[RFC9101](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC9101)]. The request object MUST fulfill the requirements as defined in [Section 5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#vp_token_request).
The following is a non-normative example of a payload for a request object:

```
{
  "client_id": "x509_san_dns:client.example.org",
  "response_uri": "https://client.example.org/post",
  "response_type": "vp_token",
  "response_mode": "direct_post",
  "dcql_query": {...},
  "nonce": "n-0S6_WzA2Mj",
  "wallet_nonce": "qPmxiNFCR3QTm19POc8u",
  "state" : "eyJhb...6-sVA"
}
```

The Wallet MUST process the request as defined in [[RFC9101](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC9101)]. Additionally, if the Wallet passed a `wallet_nonce` in the POST request, the Wallet MUST validate whether the request object contains the respective nonce value in a `wallet_nonce` claim. If it does not, the Wallet MUST terminate request processing.
The Wallet MUST extract the set of Authorization Request parameters from the Request Object. The Wallet MUST only use the parameters in this Request Object, even if the same parameter was provided in an Authorization Request query parameter. The Client Identifier value in the `client_id` Authorization Request parameter and the Request Object `client_id` claim value MUST be identical, including the Client Identifier Prefix. If any of these conditions are not met, the Wallet MUST terminate request processing.
The Wallet then validates the request as specified in OAuth 2.0 [[RFC6749](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC6749)].


#### 5.10.2. Request URI Error Response
If the Verifier responds with any HTTP error response, the Wallet MUST terminate the process.

---

### 5.11. Verifier Info
Verifier Info parameter allows the Verifier to provide additional context or metadata as part of the Authorization Request attested by a trusted third party. These inputs can support a variety of use cases, such as helping the Wallet apply policy decisions, validating eligibility, or presenting more meaningful information to the End-User during consent.
Each Verifier Info object contains a type identifier, associated data and optionally references to Credential identifiers. The format and semantics of these attestations are defined by ecosystems or profiles.
For example, a Verifier might include:

- A **registration certificate** issued by a trusted authority, to prove that the Verifier has publicly registered its intent to request certain credentials.

          - A **policy statement**, such as a signed document describing acceptable use, retention periods, or access rights.

          - The **confirmation of a role** of the Verifier in a certain domain, e.g. the Verifier might be a certified payment service provider under the EU's Payment Service Directive 2.

        
The Verifier Info parameter is optional. Wallets MAY use them to make authorization decisions or to enhance the user experience, but they SHOULD ignore any unrecognized or unsupported Verifier Info types.


#### 5.11.1. Proof of Possession
This specification supports two models for proof of possession:

- 
              **claim-bound attestations**: The attestation is not signed by the Verifier, but bound to it. The exact binding mechanism is defined by the type of the definition. For example for JWTs, the `sub` claim is including the distinguished name of the Certificate that was used to sign the request. The binding may also include the `client_id` parameter.

            - 
              **key-bound attestations**: The attestation's proof of possession is signed by the Verifier with a key contained or related to the attestation. To bind the signature to the presentation request, the respective signature object should include the `nonce` and `client_id` request parameters. The attestation and the proof of possession have to be passed in the attachment.

          
The Wallet MUST validate such proofs if defined by the profile and ignore or reject attachments that fail validation.
