---
name: "oid4vp-security"
description: "Use when reviewing security or privacy requirements for an OpenID4VP implementation. Covers: replay prevention, nonce binding, session fixation, direct_post response URI validation, TLS requirements, selective disclosure privacy, verifier-to-verifier unlinkability, and conformance testing guidance."
sections:
  - "13. Implementation Considerations"
  - "13.1. Static Configuration Values of the Wallets"
  - "13.2. Nested Presentations"
  - "13.3. Response Mode direct_post"
  - "13.4. Pre-Final Specifications"
  - "14. Security Considerations"
  - "14.1. Preventing Replay of Verifiable Presentations"
  - "14.2. Session Fixation"
  - "14.3. Response Mode \"direct_post\""
  - "14.4. End-User Authentication using Credentials"
  - "14.5. Encrypting an Unsigned Response"
  - "14.6. TLS Requirements"
  - "14.7. Incomplete or Incorrect Implementations of the Specifications and Conformance Testing"
  - "14.8. Always Use the Full Client Identifier"
  - "14.9. Security Checks on the Returned Credentials and Presentations"
  - "15. Privacy Considerations"
  - "15.1. User Consent"
  - "15.2. Privacy Notice"
  - "15.3. Purpose Legitimacy"
  - "15.4. Selective Disclosure"
  - "15.5. Verifier-to-Verifier Unlinkable Presentations"
  - "15.6. No Fingerprinting of the End-User"
  - "15.7. Information Security"
  - "15.8. Wallet to Verifier Communication"
  - "15.9. Error Responses"
  - "15.10. Establishing Trust in the Issuers"
---

<!-- ARF version: 1.0-final-2025-07-09 -->
<!-- Tokens: ~7038 -->

## 13. Implementation Considerations


### 13.1. Static Configuration Values of the Wallets
This section lists profiles of this specification that define static configuration values for Wallets and defines one set of static configuration values that can be used by the Verifier when it is unable to perform Dynamic Discovery.


#### 13.1.1. Profiles that Define Static Configuration Values
The following is a list of profiles that define static configuration values of Wallets:

- 
              [OpenID4VC High Assurance Interoperability Profile 1.0](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html)

            - 
              [JWT VC Presentation Profile](https://identity.foundation/jwt-vc-presentation-profile/)

          


#### 13.1.2. A Set of Static Configuration Values bound to openid4vp://
The following is a non-normative example of a set of static configuration values that can be used with `vp_token` parameter as a supported Response Type, bound to a custom URL scheme `openid4vp://` as an Authorization Endpoint:

```
{
  "authorization_endpoint": "openid4vp:",
  "response_types_supported": [
    "vp_token"
  ],
  "vp_formats_supported": {
    "dc+sd-jwt": {
      "sd-jwt_alg_values": [
        "ES256"
      ],
      "kb-jwt_alg_values": [
        "ES256"
      ]
    },
    "mso_mdoc": {}
  },
  "request_object_signing_alg_values_supported": [
    "ES256"
  ]
}
```


### 13.2. Nested Presentations
This specification does not support presentation of a Presentation nested inside another Presentation.


### 13.3. Response Mode direct_post
The design of the interactions between the different components of the Verifier (especially Frontend and Response URI) when using Response Mode `direct_post` is at the discretion of the Verifier since it does not affect the interface between the Verifier and the Wallet.
In order to support implementers, this section outlines a possible design that fulfills the Security Considerations given in [Section 14](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#security_considerations).
[Figure 3](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#direct_post_reference_design) illustrates a sequence diagram of the design:


          
```
+--------+   +------------+           +---------------------+                 +----------+
|End-User|   |  Verifier  |           |  Verifier           |                 |  Wallet  |
|        |   |            |           |  Response Endpoint  |                 |          |
+--------+   +------------+           +---------------------+                 +----------+
    |              |                            |                                  |
    |   interacts  |                            |                                  |
    |------------->|                            |                                  |
    |              |  (1) create nonce          |                                  |
    |              |-----------+                |                                  |
    |              |           |                |                                  |
    |              |<----------+                |                                  |
    |              |                            |                                  |
    |              |  (2) initiate transaction  |                                  |
    |              |--------------------------->|                                  |
    |              |                            |                                  |
    |              |  (3) return transaction-id & request-id                       |
    |              |<---------------------------|                                  |
    |              |                            |                                  |
    |              |  (4) Authorization Request                                    |
    |              |      (response_uri, nonce, state, dcql_query)                 |
    |              |-------------------------------------------------------------->|
    |              |                            |                                  |
    |              End-User Authentication / Consent                               |
    |              |                            |                                  |
    |              |                            | (5) Authorization Response       |
    |              |                            |     (VP Token, state)            |
    |              |                            |<---------------------------------|
    |              |                            |                                  |
    |              |                            | (6) Response                     |
    |              |                            | (redirect_uri with response_code)|
    |              |                            |--------------------------------->|
    |              |                            |                                  |
    |              |  (7) Redirect to the redirect URI (response_code)             |
    |              |<--------------------------------------------------------------|
    |              |                            |                                  |
    |              |  (8) fetch response data   |                                  |
    |              |     (transaction-id, response_code)                           |
    |              |--------------------------->|                                  |
    |              |                            |                                  |
    |              |                            |                                  |
    |              |  (9) response data         |                                  |
    |              |     (VP Token)             |                                  |
    |              |<---------------------------|                                  |
    |              |                            |                                  |
    |              |  (10) check nonce          |                                  |
    |              |-----------+                |                                  |
    |              |           |                |                                  |
    |              |<----------+                |                                  |
```

Figure 3:
Reference Design for Response Mode `direct_post`
          

(1) The Verifier produces a `nonce` value by generating at least 16 fresh, cryptographically random bytes with sufficient entropy, associates it with the session and base64url encodes it.
(2) The Verifier initiates a new transaction at its Response URI.
(3) The Response URI will set up the transaction and respond with two fresh, cryptographically random numbers with sufficient entropy designated as `transaction-id` and `request-id`. Those values are used in the process to identify the authorization response (`request-id`) and to ensure only the Verifier can obtain the Authorization Response data (`transaction-id`).
(4) The Verifier then sends the Authorization Request with the `request-id` as `state` and the `nonce` value created in step (1) to the Wallet.
(5) After authenticating the End-User and getting their consent to share the request Credentials, the Wallet sends the Authorization Response with the parameters `vp_token` and `state` to the `response_uri` of the Verifier.
(6) The Verifier's Response URI checks whether the `state` value is a valid `request-id`. If so, it stores the Authorization Response data linked to the respective `transaction-id`. It then creates a `response_code` as fresh, cryptographically random number with sufficient entropy that it also links with the respective Authorization Response data. It then returns the `redirect_uri`, which includes the `response_code` to the Wallet.
Note: If the Verifier's Response URI does not return a `redirect_uri`, processing at the Wallet stops at that step. The Verifier is supposed to fetch the Authorization Response without waiting for a redirect (see step 8).
(7) The Wallet sends the user agent to the Verifier (`redirect_uri`). The Verifier receives the Request and extracts the `response_code` parameter.
(8) The Verifier sends the `response_code` and the `transaction-id` from its session to the Response URI.

- The Response URI uses the `transaction-id` to look the matching Authorization Response data up, which implicitly validates the `transaction-id` associated with the Verifier's session.

          - If an Authorization Response is found, the Response URI checks whether the `response_code` was associated with this Authorization Response in step (6).

        
Note: If the Verifier's Response URI did not return a `redirect_uri` in step (6), the Verifier will periodically query the Response URI with the `transaction-id` to obtain the Authorization Response once it becomes available.
(9) The Response URI returns the VP Token for further processing to the Verifier.
(10) The Verifier checks whether the `nonce` received in the Credential(s) in the VP Token in step (9) corresponds to the `nonce` value from the session. The Verifier then consumes the VP Token and invalidates the `transaction-id`, `request-id` and `nonce` in the session.


### 13.4. Pre-Final Specifications
Implementers should be aware that this specification uses several specifications that are not yet final specifications. Those specifications are:

- OpenID Federation 1.0 draft -43 [[OpenID.Federation](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#OpenID.Federation)]

          - SIOPv2 draft -13 [[SIOPv2](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#SIOPv2)]

          - Selective Disclosure for JWTs (SD-JWT) draft -22 [[I-D.ietf-oauth-selective-disclosure-jwt](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-oauth-selective-disclosure-jwt)]

          - SD-JWT-based Verifiable Credentials (SD-JWT VC) draft -09 [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-oauth-sd-jwt-vc)]

          - Fully-Specified Algorithms for JOSE and COSE draft -13 [[I-D.ietf-jose-fully-specified-algorithms](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-jose-fully-specified-algorithms)]

        
While breaking changes to the specifications referenced in this specification are not expected, should they occur, OpenID4VP implementations should continue to use the specifically referenced versions above in preference to the final versions, unless updated by a profile or new version of this specification.

---

## 14. Security Considerations


### 14.1. Preventing Replay of Verifiable Presentations
An attacker could try to inject Presentations obtained from (for example) a previous Authorization Response into another Authorization Response, thus impersonating the End-User that originally presented the respective Verifiable Presentation. Holder Binding aims to prevent such attacks.


#### 14.1.1. Presentations without Holder Binding Proofs
By definition, Presentations without Holder Binding (see [Section 5.3](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#nkb-credentials)) do
not provide protection against replay. A Verifier that consumes Presentations without Holder Binding
accepts the risk that the Holder may have obtained the Credential from a third
party (e.g., by playing the role of a Verifier) and that the Holder may not be
the subject of the Credential.
Depending on the use case, the risk assessment of the Verifier, and external
validation measures that can be taken, this risk may be acceptable.


#### 14.1.2. Verifiable Presentations
For Verifiable Presentations, implementers of this specification MUST implement the controls as defined in this section to detect and prevent replay attacks.
The cryptographic proof of possession in a Verifiable Presentation MUST be bound by the Wallet to the intended audience (the Client Identifier of the Verifier) and the respective transaction (identified by the `nonce` parameter in the Authorization Request, as defined in [Section 5.2](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#existing_parameters)). The Verifier MUST verify this binding.
The Wallet MUST link every Verifiable Presentation returned to the Verifier in the VP Token to the `client_id` and the `nonce` values of the respective Authentication Request.
The Verifier MUST validate every individual Verifiable Presentation in an Authorization Response and ensure that it is linked to the values of the `client_id` and the `nonce` parameter it had used for the respective Authorization Request. If any Verifiable Presentation in the response does not contain the correct `nonce` value, the response MUST be rejected.
The `client_id` is used to detect the replay of Verifiable Presentations to a party other than the one intended. This allows Verifiers to reject the Verifiable Presentation. The `nonce` value binds the Verifiable Presentation to a certain authentication transaction and allows the Verifier to detect injection of a Presentation in the flow, which is especially important in the flows where the Presentation is passed through the front-channel.
Note: Different formats for Verifiable Presentations and signature/proof schemes use different ways to represent the intended audience and the session binding. Some use claims to directly represent those values, others include the values into the calculation of cryptographic proofs. There are also different naming conventions across the different formats. The format of the respective presentation is defined by the Verifier in the request.
The following is a non-normative example of the payload of a Verifiable Presentation following a request with the Credential Format Identifier `jwt_vc_json`:

```
{
  "iss": "did:example:ebfeb1f712ebc6f1c276e12ec21",
  "jti": "urn:uuid:3978344f-8596-4c3a-a978-8fcaba3903c5",
  "aud": "s6BhdRkqt3",
  "nonce": "343s$FSFDa-",
  "nbf": 1541493724,
  "iat": 1541493724,
  "exp": 1573029723,
  "vp": {
    "@context": [
      "https://www.w3.org/2018/credentials/v1",
      "https://www.w3.org/2018/credentials/examples/v1"
    ],
    "type": ["VerifiablePresentation"],

    "verifiableCredential": [""]
  }
}
```

In the example above, the requested `nonce` value is included as the `nonce` and `client_id` as the `aud` value in the proof of the Verifiable Presentation.
The following is a non-normative example of a Verifiable Presentation following a request with the Credential Format Identifier `ldp_vc` without a `proof` property:

```
{
  "@context": [ ... ],
  "type": "VerifiablePresentation",
  "verifiableCredential": [ ... ],
  "proof": {
    "type": "DataIntegrityProof",
    "cryptosuite": "ecdsa-rdfc-2019",
    "created": "2018-09-14T21:19:10Z",
    "proofPurpose": "authentication",
    "verificationMethod": "did:example:ebfeb1f712ebc6f1c276e12ec21#keys-1",
    "challenge": "343s$FSFDa-",
    "domain": "x509_san_dns:client.example.org",
    "proofValue": "z2iAR...3oj9Q8"
  }
}
```

In the example above, the requested `nonce` value is included as the `challenge` and `client_id` as the `domain` value in the proof of the Verifiable Presentation.


### 14.2. Session Fixation
To perform a session fixation attack, an attacker would start the process using a Verifier on a device under their control, capture the Authorization Request, and relay it to the device of a victim. The attacker would then periodically try to conclude the process in their Verifier, which would cause the Verifier on their device to try to fetch and verify the Authorization Response.
Such an attack is impossible against flows implemented with the Response Mode `fragment` as the Wallet will always send the VP Token to the redirect endpoint on the same device where it resides. This means an attacker could extract a valid Authorization Request from a Verifier on their device and trick a Victim into performing the same Authorization Request on the victim's device. But there is usually no way for an attacker to get hold of the resulting VP Token.
However, the Response Mode `direct_post` is susceptible to such an attack as the result is sent from the Wallet out-of-band to the Verifier's Response URI.
This kind of attack can be detected if the Response Mode `direct_post` is used in conjunction with the redirect URI, which causes the Wallet to redirect the flow to the Verifier's frontend at the device where the transaction was concluded. The Verifier's Response URI MUST include a fresh secret (Response Code) into the redirect URI returned to the Wallet and the Verifier's Response URI MUST require the frontend to pass the respective Response Code when fetching the Authorization Response. That stops session fixation attacks as long as the attacker is unable to get access to the Response Code.
Note that this protection technique is not applicable to cross-device scenarios because the browser used by the Wallet will not have the original session.
It is also not applicable in same-device scenarios if the Wallet uses a browser different from the one used on the presentation request (e.g. device with multiple installed browsers), because the original session will also not be available there. [Appendix A](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#dc_api) provides an alternative Wallet invocation method using web/app platform APIs that avoids many of these issues.
See [Section 13.3](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#implementation_considerations_direct_post) for more implementation considerations.
When using the Response Mode `direct_post` without the further protection provided by the redirect URI, there is no session context for the Verifier to detect session fixation attempts. It is RECOMMENDED for the Verifiers to implement mechanisms to strengthen the security of the flow. For more details on possible attacks and mitigations see [[I-D.ietf-oauth-cross-device-security](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-oauth-cross-device-security)].


### 14.3. Response Mode "direct_post"


#### 14.3.1. Validation of the Response URI
The Wallet MUST ensure the data in the Authorization Response cannot leak through Response URIs. When using pre-registered Response URIs, the Wallet MUST comply with best practices for redirect URI validation as defined in [[RFC9700](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC9700)]. The Wallet MAY also rely on a Client Identifier Prefix in conjunction with Client Authentication and integrity protection of the request to establish trust in the Response URI provided by a certain Verifier.


#### 14.3.2. Protection of the Response URI
The Verifier SHOULD protect its Response URI from inadvertent requests by checking that the value of the received `state` parameter corresponds to a recent Authorization Request.


#### 14.3.3. Protection of the Authorization Response Data
This specification assumes that the Verifier's Response URI offers an internal interface to other components of the Verifier to obtain (and subsequently process) Authorization Response data. An attacker could try to obtain Authorization Response Data from a Verifier's Response URI by looking up this data through the internal interface. This could lead to leakage of valid Presentations containing personally identifiable information.
Implementations of this specification MUST have security mechanisms in place to prevent inadvertent requests against this internal interface. Implementation options to fulfill this requirement include:

- Authentication between the different parts within the Verifier

            - Two cryptographically random numbers.  The first being used to manage state between the Wallet and Verifier. The second being used to ensure that only a legitimate component of the Verifier can obtain the Authorization Response data.

          


### 14.4. End-User Authentication using Credentials
Clients intending to authenticate the End-User utilizing a claim in a Credential MUST ensure this claim is stable for the End-User as well as locally unique and never reassigned within the Credential Issuer to another End-User. Such a claim MUST also only be used in combination with the Credential Issuer identifier to ensure global uniqueness and to prevent attacks where an attacker obtains the same claim from a different Credential Issuer and tries to impersonate the legitimate End-User.


### 14.5. Encrypting an Unsigned Response
Because an encrypted Authorization Response has no additional integrity protection, an attacker might be able to alter Authorization Response parameters and generate a new encrypted Authorization Response for the Verifier, as encryption is performed using the public key of the Verifier (which is likely to be widely known when not ephemeral to the request/response). Note this includes injecting a new VP Token. Since the contents of the VP Token are integrity protected, tampering with the VP Token is detectable by the Verifier. For details, see [Section 14.1](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#preventing-replay).


### 14.6. TLS Requirements
Implementations MUST follow [[BCP195](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#BCP195)].
Whenever TLS is used, a TLS server certificate check MUST be performed, per [[RFC6125](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC6125)].


### 14.7. Incomplete or Incorrect Implementations of the Specifications and Conformance Testing
To achieve the full security benefits, it is important that the implementation of this specification, and the underlying specifications, are both complete and correct.
The OpenID Foundation provides tools that can be used to confirm that an implementation is correct and conformant:
[https://openid.net/certification/conformance-testing-for-openid-for-verifiable-presentations/](https://openid.net/certification/conformance-testing-for-openid-for-verifiable-presentations/)


### 14.8. Always Use the Full Client Identifier
Confusing Verifiers using a Client Identifier Prefix with those using none can lead to attacks. Therefore, Wallets MUST always use the full Client Identifier, including the prefix if provided, within the context of the Wallet or its responses to identify the client. This refers in particular to places where the Client Identifier is used in [[RFC6749](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC6749)] and in the presentation returned to the Verifier.


### 14.9. Security Checks on the Returned Credentials and Presentations
While the Verifier can specify various constraints both on the claims level and
the Credential level as shown in [Section 6.4](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#dcql_query_lang_processing_rules), it MUST NOT rely on the Wallet to enforce
these constraints. The Wallet is not controlled by the Verifier and the Verifier
MUST perform its own security checks on the returned Credentials and
Presentations.

---

## 15. Privacy Considerations
Many privacy considerations are specific to the Credential format and associated proof type used in a particular Presentation.
This section focuses on privacy considerations specific to the presentation protocol while also addressing cross-cutting concerns related to credential formats, Wallet behavior, and Verifier practices.
Wallet providers and Verifiers need to take into account privacy considerations in this section to mitigate the risks of
data leakage, user tracking, and other privacy harms.


### 15.1. User Consent
Wallets SHOULD obtain explicit, informed consent from the End-User before releasing any Verifiable Credential or Presentation to a Verifier, or returning an error.
Transaction history and data within the Wallet SHOULD NOT be accessible to anyone other than the End-User, unless the End-User has given consent or there is another legal basis to do so.


### 15.2. Privacy Notice
Wallets SHOULD make their privacy notices readily available to the End-User.


### 15.3. Purpose Legitimacy
The Verifier SHOULD ensure that the purpose for collecting the information it is requesting is sufficiently specific and communicated before collection. For example, the purpose is shown to the End-User before or within the presentation request that is sent to the Wallet.
If the Wallet has indications that the Verifier is requesting data that it is not entitled to, the Wallet SHOULD warn the End-User or potentially stop processing.


### 15.4. Selective Disclosure
Selective disclosure is a data minimization technique that allows for sharing only the specific information needed from
a Credential without revealing all of the claims contained in that Credential.
The DCQL helps facilitate selective disclosure by allowing the Verifier to specify the claims it is interested in,
allowing the Wallet to disclose only the claims that are relevant to the Verifier's request.
Some Credential formats support selective disclosure and a salted-hash based approach is one common approach.


#### 15.4.1. DCQL Value Matching
When using DCQL `values` to match the expected values of claims, the fact that a
claim within a certain Credential matched a value or did not match a value might
already leak information about the claim value. Therefore, Wallets MUST take
precautions against leaking information about the claim value when processing
`values`. This SHOULD include, in particular:

- ensuring that a Verifier, in the response, cannot distinguish between the case where an End-User did
not consent to releasing the Credential and the case where the claim value did
not match the expected value, and

            - preventing repeated or "silent" requests leaking data to the Verifier without
the user's consent by ensuring that all requests, even if no response can be
sent by the Wallet due to a `values` mismatch, require some form of End-User
interaction before a response is sent.

          
In both cases listed here, it needs to be considered that returning an error
response can also leak information about the processing outcome of `values`.


#### 15.4.2. Strictly Necessary Claims
Verifiers SHOULD use DCQL queries that request only the minimal set of claims and Credentials needed to fulfill the specified purposes.


### 15.5. Verifier-to-Verifier Unlinkable Presentations
Even when using selective disclosure to reveal limited claims from a Credential to a Verifier, there are ways in which a Presentation could be linked to another Presentation in another session or a Presentation to another Verifier. For example, with Credential formats such as SD-JWT and mdoc, the Issuer signature on a Credential or the public key a Credential is bound to, can provide a Verifier with a way to link the Credential across different Presentations or sessions. In order to avoid such linking, a Wallet can use multiple instances of a Credential, each with unique Issuer signatures and associated public keys to limit this:

- a Wallet can use an issued Credential instance only once in a Presentation to a specific Verifier, before discarding the Credential, thus avoiding linking on the above basis ever occurring

          - a Wallet can apply a limited use policy for a specific instance of a Credential, perhaps only allowing it to be presented to the same Verifier to avoid Verifier to Verifier linkability

        
Considerable discourse regarding unlinkability in salted-hash based selective disclosure mechanisms is provided in Section 10.1 of [[I-D.ietf-oauth-selective-disclosure-jwt](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-oauth-selective-disclosure-jwt)]. One technique mentioned to achieve some important unlinkability properties is the use of batch issuance, which is supported in [[OpenID4VCI](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#OpenID4VCI)], with individual Credentials being presented only once.


### 15.6. No Fingerprinting of the End-User
A Verifier SHOULD NOT attempt to fingerprint the End-User based on metadata that may be available in the interaction with the End-User's wallet.
A Wallet SHOULD implement measures that prevent fingerprinting of the End-Users during the request to resolve the Request Object URI.
A Wallet SHOULD implement measures that limit unintended additional information being disclosed through the Response URI. For example, disclosing Wallet-related information through the HTTP user agent header.


### 15.7. Information Security
Both Wallet providers and Verifiers SHOULD apply suitable security controls at the operational, functional, and strategic level to ensure the integrity, confidentiality and general handling of PII. Furthermore, they should consider protections against risks such as unauthorized access, destruction, use, modification, disclosure or loss throughout the whole of its life cycle.


### 15.8. Wallet to Verifier Communication
Wallets SHOULD only send the minimal amount of information possible, and in particular, avoid sending any additional HTTP headers identifying the software used for the request (e.g., HTTP libraries or their versions) when retrieving a `request_uri` or sending to `response_uri` to reduce the risk of fingerprinting and End-User tracking.
Wallets MUST NOT include any personally identifiable information (PII) in HTTP requests to Verifiers unless explicitly required for the flow and authorized by the End-User.


#### 15.8.1. Establishing Trust in the Request URI
Wallets operating within a trust framework SHOULD validate that the Request URI is properly associated with the Client Identifier and authorized for the request.
Untrusted or unrecognized Request URI endpoints SHOULD be rejected or require End-User confirmation before proceeding.


#### 15.8.2. Authorization Requests with Request URI
If the Wallet is acting within a trust framework that allows the Wallet to determine whether a Request URI belongs to a certain Client Identifier, the Wallet is RECOMMENDED to validate the Verifier's authenticity and authorization given by the Client Identifier and that the Request URI corresponds to this Verifier. If the link cannot be established in those cases, the Wallet MUST refuse the request.


### 15.9. Error Responses
Error responses SHOULD avoid including sensitive or detailed contextual information that could be used to infer the End-User's data.


#### 15.9.1. wallet_unavailable Authorization Error Response
In the event that another component is invoked instead of the Wallet, the End-User SHOULD be informed and give consent before the invoked component returns the `wallet_unavailable` Authorization Error Response to the Verifier.


#### 15.9.2. Digital Credential API Error Responses
Returning any OpenID4VP protocol error, regardless of content, can reveal additional information about the End-User’s underlying Credentials or Wallet in a way that is unique to the Digital Credentials API since reaching the Wallet can be dependent on a Wallet's ability to satisfy the request. For example, platform implementations could only allow Wallets to be selected that satisfy the request. In this case, OpenID4VP protocol error responses can only be returned by a selected Wallet and would therefore reveal that the End-User is in possession of Credentials that satisfy the request. This is in contrast to other engagement methods, in which the Wallet receives the request before learning if it can be fulfilled. What is revealed by a Wallet in those cases depends on how each individual Wallet processes the request.
The narrower a request is, the more information is revealed:

- A request that can be fulfilled by a broad range of documents will only reveal that the End-User has a Credential from a large set of documents.

            - A request for a single document type will reveal the End-User is in possession of that Credential. How sensitive this is would depend on the particular Credential.

            - A request with which can only be satisfied by a single trusted authority will reveal that the End-User has a Credential from a particular authority, from which other attributes may be inferred.

            - A request with value matching (as defined in [Section 6.4.1](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#selecting_claims)) will reveal the specific value of that claim/attribute.

          
Wallet implementations need to balance the value of error detection to the maintenance and scaling of the Verifier ecosystem with the information that is revealed.
A Wallet SHOULD NOT return any OpenID4VP protocol errors without End-User interaction either with the platform or the Wallet. When handling errors, implementations can opt to cancel the flow (the details of which are platform specific) rather than return an OpenID4VP protocol-specific error. This will make the result indistinguishable from other platform aborts, preventing any information from being revealed.
A Wallet SHOULD NOT return any OpenID4VP protocol errors before obtaining End-User consent, when processing a request containing value matching (to avoid revealing values of claims without consent), or issuer selection (to avoid revealing that the End-User has a Credential from a particular authority). Additionally, the End-User consent protects against undetected, repeated requests to the Wallet.


### 15.10. Establishing Trust in the Issuers
This specification introduces an extension point that allows for a Verifier to express expected Issuers or trust frameworks that certify Issuers. It is important to understand the implications of these trust establishment mechanisms on the privacy of the overall system.
In general, two types of mechanisms can be distinguished: those that are self-contained, where the Wallet and Verifier already have all the information needed to check if a Credential satisfies the request, and those that depend on online resolution to obtain additional data.
Mechanisms that require online resolution can leak information that could be used to profile the usage of the Credentials.
In particular, situations where the Wallet must fetch data before it can generate a matching presentation may expose information about individual End-Users to external parties.
Wallets SHOULD NOT access URLs included in a request from the Verifier if those URLs are unfamiliar or hosted by untrusted third parties. Privacy risks can be reduced if such URLs are treated purely as identifiers and not actually retrieved by the Wallet upon receiving the request.
Ecosystems intending to use trusted authority mechanisms SHOULD ensure that the privacy characteristics of their chosen mechanisms align with the overall privacy goals of the ecosystem.
