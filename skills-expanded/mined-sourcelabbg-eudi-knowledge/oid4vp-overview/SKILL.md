---
name: "oid4vp-overview"
description: "Use when needing an overview of OpenID4VP, its terminology, or the difference between same-device and cross-device presentation flows. Covers: Verifier, Wallet, VP Token, vp_token response type, nonce, authorization request/response model."
sections:
  - "1. Introduction"
  - "1.1. Additional Authors"
  - "1.2. Errata revisions"
  - "1.3. Requirements Notation and Conventions"
  - "2. Terminology"
  - "3. Overview"
  - "3.1. Same Device Flow"
  - "3.2. Cross Device Flow"
---

<!-- ARF version: 1.0-final-2025-07-09 -->
<!-- Tokens: ~4620 -->

## 1. Introduction
This specification defines a mechanism on top of OAuth 2.0 [[RFC6749](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC6749)] for requesting and delivering Presentations of Credentials. Credentials and Presentations can be of any format, including, but not limited to W3C Verifiable Credentials Data Model [[VC_DATA](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#VC_DATA)], ISO mdoc [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.18013-5)], and IETF SD-JWT VC [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-oauth-sd-jwt-vc)].
OAuth 2.0 [[RFC6749](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC6749)] is used as a base protocol as it provides the required rails to build a simple, secure, and developer-friendly Credential presentation layer on top of it. Moreover, implementers can, in a single interface, support Credential presentation and the issuance of Access Tokens for access to APIs based on Credentials in the Wallet. OpenID Connect [[OpenID.Core](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#OpenID.Core)] deployments can also extend their implementations using this specification with the ability to transport Credential Presentations.
This specification can also be combined with [[SIOPv2](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#SIOPv2)], if implementers require OpenID Connect features, such as the issuance of Self-Issued ID Tokens [[SIOPv2](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#SIOPv2)].
Additionally, it defines how to use OpenID4VP in conjunction with the Digital Credentials API (DC API) [[W3C.Digital_Credentials_API](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#W3C.Digital_Credentials_API)]. See section [Appendix A](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#dc_api) for all requirements applicable to implementers of OpenID4VP over the DC API. Except where it explicitly references other sections of this specification, that section is self-contained, and its implementers can ignore the rest of the specification.


### 1.1. Additional Authors

- Tobias Looker (MATTR)

          - Adam Lemmon (MATTR)

        


### 1.2. Errata revisions
The latest revision of this specification, incorporating any errata updates, is published at [openid-4-verifiable-presentations-1_0](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html). The text of the final specification as approved will always be available at [openid-4-verifiable-presentations-1_0-final](https://openid.net/specs/openid-4-verifiable-presentations-1_0-final.html). When referring to this specification from other documents, it is recommended to reference [openid-4-verifiable-presentations-1_0](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html).


### 1.3. Requirements Notation and Conventions
The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 [[RFC2119](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC2119)] [[RFC8174](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC8174)] when, and only when, they appear in all capitals, as shown here.

---

## 2. Terminology
This specification uses the terms "Access Token", "Authorization Request", "Authorization Response", "Client", "Client Authentication", "Client Identifier", "Grant Type", "Response Type", "Token Request" and "Token Response" defined by OAuth 2.0 [[RFC6749](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC6749)], the terms "End-User" and "Entity" as defined by OpenID Connect Core [[OpenID.Core](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#OpenID.Core)], the terms "Request Object" and "Request URI" as defined by [[RFC9101](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC9101)], the term "JSON Web Token (JWT)" defined by JSON Web Token (JWT) [[RFC7519](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC7519)], the term "JOSE Header" defined by JSON Web Signature (JWS) [[RFC7515](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC7515)], the term "JSON Web Encryption (JWE)" defined by [[RFC7516](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC7516)], and the term "Response Mode" defined by OAuth 2.0 Multiple Response Type Encoding Practices [[OAuth.Responses](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#OAuth.Responses)].
Base64url-encoded denotes the URL-safe base64 encoding without padding defined in Section 2 of [[RFC7515](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC7515)].
This specification also defines the following terms. In the case where a term has a definition that differs, the definition below is authoritative.

        Biometrics-based Holder Binding:
        Ability of the Holder to prove legitimate possession of a Credential by demonstrating a certain biometric trait, such as a fingerprint or face. One example of a Credential with biometric Holder Binding is a mobile driving license [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.18013-5)], which contains a portrait of the Holder.

        
Claims-based Holder Binding:
        Ability of the Holder to prove legitimate possession of a Credential by proving certain claims, e.g., name and date of birth, for example by presenting another Credential. Claims-based Holder Binding allows long-term, cross-device use of a Credential as it does not depend on cryptographic key material stored on a certain device. One example of such a Credential could be a diploma.

        
Credential:
        A set of one or more claims about a subject made by a Credential Issuer. In this specification, Credentials are usually Verifiable Credentials (defined below). Note that the definition of the term "Credential" in this specification is different from that in [[OpenID.Core](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#OpenID.Core)].

        
Credential Format Identifier:
        An identifier to denote a specific Credential Format in the context of this specification. This identifier implies the use of parameters specific to the respective Credential Format.

        
Credential Issuer:
        An entity that issues Credentials. Also called Issuer.

        
Cryptographic Holder Binding:
        Ability of the Holder to prove legitimate possession of a Credential by proving control over the same private key during the issuance and presentation. Mechanism might depend on the Credential Format. For example, in jwt_vc_json Credential Format, a Credential with Cryptographic Holder Binding contains a public key or a reference to a public key that matches to the private key controlled by the Holder.

        
Digital Credentials API:
        The Digital Credentials API (DC API) refers to the W3C Digital Credentials API [[W3C.Digital_Credentials_API](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#W3C.Digital_Credentials_API)] on the Web Platform and its equivalent native APIs on App Platforms (such as Credential Manager on Android).

        
Holder:
        An entity that receives Credentials and has control over them to present them to the Verifiers as Presentations.

        
Holder Binding or Key Binding:
        Ability of the Holder to prove legitimate possession of a Credential.

        
Issuer-Holder-Verifier Model:
        A model for exchanging claims, where claims are issued in the form of Credentials independent of the process of presenting them as Presentations to the Verifiers. An issued Credential may be used multiple times.

        
Origin:
        An identifier for the calling website or native application, asserted by the web or app platform. A web origin is the combination of a scheme/protocol, host, and port, with port being omitted when it matches the default port of the scheme. An app platform may use a linked web origin, or use a platform-specific URI for the app origin. For example, the Verifier for the organization MyExampleOrg is served from [https://verify.example.com](https://verify.example.com). The web origin is `https://verify.example.com` with `https` being the scheme, `verify.example.com` being the host, and the port is not explicitly included as `443` is the default port for the protocol `https`. The native applications origin on some platforms will also be `https://verify.example.com` and on other platforms, may be `platform:pkg-key-hash:Z4OFzVVSZrzTRa3eg79hUuHy12MVW0vzPDf4q4zaPs0`.

        
Presentation:
        Data that is presented to a specific Verifier, derived from a Credential. In this specification, Presentations are usually Verifiable Presentations including Holder Binding (as defined below), but may also be Presentations without Holder Binding (discussed in [Section 5.3](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#nkb-credentials)).

        
VP Token:
        An artifact containing one or more Presentations returned as a response to an Authorization Request. The structure of VP Tokens is defined in [Section 8.1](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#response-parameters).

        
Verifier:
        An entity that requests, receives, and validates Presentations. The Verifier is a specific case of an OAuth 2.0 Client, just like a Relying Party (RP) in [[OpenID.Core](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#OpenID.Core)].

        
Verifiable Credential (VC):
        An Issuer-signed Credential whose authenticity can be cryptographically verified. Can be of any format used in the Issuer-Holder-Verifier Model, including, but not limited to those defined in [[VC_DATA](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#VC_DATA)] (VCDM), [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.18013-5)] (mdoc), and [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-oauth-sd-jwt-vc)] (SD-JWT VC).

        
Verifiable Presentation (VP):
        A Presentation with a cryptographic proof of Holder Binding. Can be of any format used in the Issuer-Holder-Verifier Model, including, but not limited to those defined in [[VC_DATA](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#VC_DATA)] (VCDM), [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.18013-5)] (mdoc), and [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-oauth-sd-jwt-vc)] (SD-JWT VC).

        
Wallet:
        An entity used by the Holder to receive, store, present, and manage Credentials and key material. There is no single deployment model of a Wallet: Credentials and keys can both be stored/managed locally, or by using a remote self-hosted service, or a remote third-party service.

---

## 3. Overview
This specification defines a mechanism to request and present Credentials. The baseline of the protocol uses HTTPS messages and redirects as defined in OAuth 2.0. Additionally, the specification defines a separate mechanism where OpenID4VP messages are sent and received over the Digital Credentials API (DC API) [[W3C.Digital_Credentials_API](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#W3C.Digital_Credentials_API)] instead of HTTPS messages and redirects.
As the primary extension, OpenID for Verifiable Presentations introduces the new response type `vp_token`, which allows a Verifier to request and receive Verifiable Presentations and Presentations in a container designated as VP Token. A VP Token contains one or more Verifiable Presentations and/or Presentations in the same or different Credential formats. Consequently, the result of an OpenID4VP interaction is one or more Verifiable Presentations and/or Presentations instead of an Access Token.
This specification supports any Credential format used in the Issuer-Holder-Verifier Model, including, but not limited to those defined in [[VC_DATA](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#VC_DATA)] (VCDM), [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.18013-5)] (mdoc), and [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-oauth-sd-jwt-vc)] (SD-JWT VC). Credentials of multiple formats can be presented in the same transaction. The examples given in the main part of this specification use W3C Verifiable Credentials, while examples in other Credential formats are given in [Appendix B](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#format_specific_parameters).
OpenID for Verifiable Presentations supports scenarios where the Authorization Request is sent both when the Verifier is interacting with the End-User using the device that is the same or different from the device on which requested Credential(s) are stored.
This specification supports the response being sent using a redirect but also using an HTTP POST request. This enables the response to be sent across devices, or when the response size exceeds the redirect URL character size limitation.
In summary, OpenID for Verifiable Presentations is a framework that requires profiling
to achieve interoperability. Profiling means defining:

- what optional features are used or mandatory to implement, e.g., response encryption;

        - which values are permitted for parameters, e.g., Credential Format Identifiers;

        - optionally, extensions for new features.

      


### 3.1. Same Device Flow
[Figure 1](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#same_device_figure) is a diagram of a flow where the End-User presents a Credential to a Verifier interacting with the End-User on the same device that the device the Wallet resides on.
The flow utilizes simple redirects to pass Authorization Request and Response between the Verifier and the Wallet. The Presentations are returned to the Verifier in the fragment part of the redirect URI, when Response Mode is `fragment`.
Note: The diagram does not illustrate all the optional features of this specification.


          
```
+--------------+   +--------------+                                    +--------------+
|   End-User   |   |   Verifier   |                                    |    Wallet    |
+--------------+   +--------------+                                    +--------------+
        |                 |                                                   |
        |    Interacts    |                                                   |
        |---------------->|                                                   |
        |                 |  (1) Authorization Request                        |
        |                 |  (DCQL query)                                     |
        |                 |-------------------------------------------------->|
        |                 |                                                   |
        |                 |                                                   |
        |   End-User Authentication / Consent                                 |
        |                 |                                                   |
        |                 |  (2)   Authorization Response                     |
        |                 |  (VP Token with Presentation(s))                  |
        |                 |<--------------------------------------------------|
```

Figure 1:
Same Device Flow
          

(1) The Verifier sends an Authorization Request to the Wallet. It contains a Digital Credentials Query Language (DCQL, see [Section 6](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#dcql_query)) query that describes the requirements of the Credential(s) that the Verifier is requesting to be presented. Such requirements could include what type of Credential(s), in what format(s), which individual Claims within those Credential(s) (Selective Disclosure), etc. The Wallet processes the Authorization Request and determines what Credentials are available matching the Verifier's request. The Wallet also authenticates the End-User and gathers consent to present the requested Credentials.
(2) The Wallet prepares the Presentation(s) of the Credential(s) that the End-User has consented to. It then sends to the Verifier an Authorization Response where the Presentation(s) are contained in the `vp_token` parameter.


### 3.2. Cross Device Flow
[Figure 2](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#cross_device_figure) is a diagram of a flow where the End-User presents a Credential to a Verifier interacting with the End-User on a different device as the device the Wallet resides on.
In this flow, the Verifier prepares an Authorization Request and renders it as a QR Code. The End-User then uses the Wallet to scan the QR Code. The Presentations are sent to the Verifier in a direct HTTP POST request to a URL controlled by the Verifier. The flow uses the Response Type `vp_token` in conjunction with the Response Mode `direct_post`, both defined in this specification. In order to keep the size of the QR Code small and be able to sign and optionally encrypt the Request Object, the actual Authorization Request contains only the Client Identifier and Request URI (as required by [[RFC9101](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC9101)]), which the Wallet uses to retrieve the actual Authorization Request data.
Note: The diagram illustrates neither all parameters nor all optional features of this specification.
Note: The usage of the Request URI as defined in [[RFC9101](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC9101)] does not depend on any other choices made in the protocol extensibility points, i.e., it can be used in the Same Device Flow, too.


          
```
+--------------+   +--------------+                                    +--------------+
|   End-User   |   |   Verifier   |                                    |    Wallet    |
|              |   |  (device A)  |                                    |  (device B)  |
+--------------+   +--------------+                                    +--------------+
        |                 |                                                   |
        |    Interacts    |                                                   |
        |---------------->|                                                   |
        |                 |  (1) Authorization Request                        |
        |                 |      (Request URI)                                |
        |                 |-------------------------------------------------->|
        |                 |                                                   |
        |                 |  (2) Request the Request Object                   |
        |                 |<--------------------------------------------------|
        |                 |                                                   |
        |                 |  (2.5) Respond with the Request Object            |
        |                 |      (DCQL query)                                 |
        |                 |-------------------------------------------------->|
        |                 |                                                   |
        |   End-User Authentication / Consent                                 |
        |                 |                                                   |
        |                 |  (3)   Authorization Response as HTTP POST        |
        |                 |  (VP Token with Presentation(s))                  |
        |                 |<--------------------------------------------------|
```

Figure 2:
Cross Device Flow
          

(1) The Verifier sends to the Wallet an Authorization Request that contains a Request URI from where to obtain the Request Object containing Authorization Request parameters.
(2) The Wallet sends an HTTP GET request to the Request URI to retrieve the Request Object.
(2.5) The HTTP GET response returns the Request Object containing Authorization Request parameters. It contains a DCQL query that describes the requirements of the Credential(s) that the Verifier is requesting to be presented. Such requirements could include what type of Credential(s), in what format(s), which individual Claims within those Credential(s) (Selective Disclosure), etc. The Wallet processes the Request Object and determines what Credentials are available matching the Verifier's request. The Wallet also authenticates the End-User and gathers their consent to present the requested Credentials.
(3) The Wallet prepares the Presentation(s) of the Credential(s) that the End-User has consented to. It then sends to the Verifier an Authorization Response where the Presentation(s) are contained in the `vp_token` parameter.
