---
name: "oid4vci-overview"
description: "Use when needing an overview of OpenID4VCI, its terminology, or the credential issuance flow. Covers: Credential Issuer, Wallet, authorization code flow, pre-authorized code flow, and the relationship between OID4VCI and OAuth 2.0."
sections:
  - "1. Introduction"
  - "1.1. Errata revisions"
  - "1.2. Requirements Notation and Conventions"
  - "2. Terminology"
  - "3. Overview"
  - "3.1. Credential Issuer"
  - "3.2. OAuth 2.0"
  - "3.3. Core Concepts"
  - "3.4. Authorization Code Flow"
  - "3.5. Pre-Authorized Code Flow"
---

<!-- ARF version: 1.0-2025-02-03 -->
<!-- Tokens: ~7744 -->

## 1. Introduction
This specification defines an OAuth-protected API for the issuance of Verifiable Credentials. Credentials can be of any format, including, but not limited to, IETF SD-JWT VC [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#I-D.ietf-oauth-sd-jwt-vc)], ISO mdoc [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#ISO.18013-5)], and W3C VCDM [[VC_DATA](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#VC_DATA)].
Verifiable Credentials are very similar to identity assertions, like ID Tokens in OpenID Connect [[OpenID.Core](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#OpenID.Core)], in that they allow a Credential Issuer to assert End-User claims. A Verifiable Credential follows a pre-defined schema (the Credential type) and MAY be bound to a certain Holder, e.g., through Cryptographic Key Binding. Verifiable Credentials can be securely presented for the End-User to the RP, without the involvement of the Credential Issuer.
Access to this API is authorized using OAuth 2.0 [[RFC6749](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC6749)], i.e., the Wallet uses OAuth 2.0 to obtain authorization to receive Verifiable Credentials. This way the issuance process can benefit from the proven security, simplicity, and flexibility of OAuth 2.0 and existing OAuth 2.0 deployments and OpenID Connect OPs (see [[OpenID.Core](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#OpenID.Core)]) can be extended to become Credential Issuers.


### 1.1. Errata revisions
The latest revision of this specification, incorporating any errata updates, is published at [openid-4-verifiable-credential-issuance-1_0](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html). The text of the final specification as approved will always be available at [openid-4-verifiable-credential-issuance-1_0-final](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0-final.html). When referring to this specification from other documents, it is recommended to reference [openid-4-verifiable-credential-issuance-1_0](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html).


### 1.2. Requirements Notation and Conventions
The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 [[RFC2119](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC2119)] [[RFC8174](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC8174)] when, and only when, they appear in all capitals, as shown here.

---

## 2. Terminology
This specification uses the terms "Access Token", "Authorization Endpoint", "Authorization Request", "Authorization Response", "Authorization Code Grant", "Authorization Server", "Client", "Client Authentication", "Client Identifier", "Grant Type", "Refresh Token", "Token Endpoint", "Token Request" and "Token Response" defined by OAuth 2.0 [[RFC6749](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC6749)], the terms "End-User", "Entity", and "Request Object" as defined by OpenID Connect Core [[OpenID.Core](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#OpenID.Core)], the term "JSON Web Token (JWT)" defined by JSON Web Token (JWT) [[RFC7519](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC7519)], the term "JOSE Header" defined by JSON Web Signature (JWS) [[RFC7515](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC7515)].
Base64url-encoded denotes the URL-safe base64 encoding without padding defined in Section 2 of [[RFC7515](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC7515)].
This specification also defines the following terms. In the case where a term has a definition that differs, the definition below is authoritative for this specification.

        Credential Dataset:
        A set of one or more claims about a subject, provided by a Credential Issuer.

        
Credential (or Verifiable Credential (VC)):
        An instance of a Credential Configuration with a particular Credential Dataset, that is signed by an Issuer and can be cryptographically verified. An Issuer may provide multiple Credentials as separate instances of the same Credential Configuration and Credential Dataset but with different cryptographic values. In this specification, the term "Verifiable Credential" is also referred to as "Credential". It's important to note that the use of the term "Credential" here differs from its usage in [[OpenID.Core](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#OpenID.Core)] and [[RFC6749](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC6749)]. In this context, "Credential" specifically does not encompass other meanings such as passwords used for login credentials.

        
Credential Format:
        Data Model used to create and represent Credential information. This format defines how various pieces of data within a Verifiable Credential are organized and encoded, ensuring that the Verifiable Credential can be consistently understood, processed, and verified by different systems. The exact parameters required to use a Credential Format in the context of this specification are defined in the Credential Format Profile. Definitions of Credential Formats is out of scope for this specification. Examples for Credential Formats are IETF SD-JWT VC [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#I-D.ietf-oauth-sd-jwt-vc)], ISO mdoc [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#ISO.18013-5)], and W3C VCDM [[VC_DATA](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#VC_DATA)].

        
Credential Format Profile:
        Set of parameters specific to individual Credential Formats. This specification provides Credential Format Profiles for IETF SD-JWT VC [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#I-D.ietf-oauth-sd-jwt-vc)], ISO mdoc [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#ISO.18013-5)], and W3C VCDM [[VC_DATA](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#VC_DATA)], which can be found in the section [Appendix A](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#format-profiles). Additionally, other specifications or deployments can define their own Credential Format Profiles by utilizing the extension points defined in this specification.

        
Credential Format Identifier:
        An identifier to denote a specific Credential Format in the context of this specification. This identifier implies the use of parameters specific to the respective Credential Format Profile.

        
Credential Configuration:
        Credential Issuer's description of a particular kind of Credential that the Credential Issuer is offering to issue, along with metadata pertaining to the issuance process and the issued Credentials. Each Credential Configuration references a Credential Format and specifies the corresponding parameters given in the Credential Format Profile. It also includes information about how issuance of a described Credential be requested, information on cryptographic methods and algorithms supported for issuance, and display information to be used by the Wallet. A Credential Configuration is identified by a Credential Configuration Identifier string that is unique to an Issuer. Credential Issuer metadata includes one or more Credential Configurations.

        
Presentation:
        Data that is presented to a specific Verifier, derived from one or more Verifiable Credentials that can be from the same or different Credential Issuers. It can be of any Credential Format.

        
Credential Issuer (or Issuer):
        An entity that issues Verifiable Credentials. In the context of this specification, the Credential Issuer acts as an OAuth 2.0 Resource Server (see [[RFC6749](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC6749)]). The Credential Issuer might also act as an Authorization Server.

        
Holder:
        An entity that receives Verifiable Credentials and has control over them to present them to the Verifiers as Presentations.

        
Verifier:
        An entity that requests, receives, and validates Presentations.

        
Issuer-Holder-Verifier Model:
        Model that facilitates the exchange of claims, where claims are issued as Verifiable Credentials independently of the process of presenting them to Verifiers in the form of Presentations. An issued Verifiable Credential may be used multiple times, although this is not a requirement.

        
Holder Binding:
        Ability of the Holder to prove legitimate possession of a Verifiable Credential.

        
Cryptographic Holder Binding or Cryptographic Key Binding:
        Ability of the Holder to prove legitimate possession of a Verifiable Credential by proving control over the same private key during the issuance and presentation. The concrete mechanism depends on the Credential Format. For example, in IETF SD-JWT VC [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#I-D.ietf-oauth-sd-jwt-vc)], the Issuer can enable this binding by including a public key or a reference to a public key that matches to the private key controlled by the Holder.

        
Claims-based Holder Binding:
        Ability of the Holder to prove legitimate possession of a Credential by proving certain claims, e.g., name and date of birth, for example by presenting another Credential. Claims-based Holder Binding allows long-term, cross-device use of a Credential as it does not depend on cryptographic key material stored on a certain device. One example of such a Credential could be a diploma.

        
Wallet:
        An entity used by the Holder to request, receive, store, present, and manage Verifiable Credentials and cryptographic key material. There is no single deployment model of a Wallet: Credentials and keys can be stored and managed either locally, through a remote self-hosted service, or via a remote third-party service. In the context of this specification, the Wallet acts as an OAuth 2.0 Client (see [[RFC6749](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC6749)]) and obtains an Access Token to access an OAuth 2.0 Resource Server (Credential Endpoint).

        
Deferred Credential Issuance:
        Issuance of Credentials not directly in the response to a Credential issuance request but following a period of time that can be used to perform certain offline business processes.

---

## 3. Overview


### 3.1. Credential Issuer
This specification defines an API for Credential issuance provided by a Credential Issuer. The API is comprised of the following endpoints:

- A mandatory Credential Endpoint from which Credentials can be issued (see [Section 8](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-endpoint)). From this endpoint, one Credential, or multiple Credentials with the same Credential Format and Credential Dataset can be issued in one request.

          - An optional Nonce Endpoint from which a fresh `c_nonce` value can be obtained to be used in proof of possession of key material in a subsequent request to the Credential Endpoint (see [Section 7](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#nonce-endpoint)).

          - An optional Deferred Credential Endpoint to allow for the deferred delivery of Credentials (see [Section 9](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#deferred-credential-issuance)).

          - An optional mechanism for the Credential Issuer to make a Credential Offer to the Wallet to encourage the Wallet to start the issuance flow (see [Section 4](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-offer-endpoint)).

          - An optional mechanism for the Credential Issuer to receive notification(s) from the Wallet about the status of the Credential(s) that have been issued (see [Section 11](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#notification-endpoint)).

          - A mechanism for the Credential Issuer to publish metadata about the Credentials it is capable of issuing (see [Section 12.2](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-issuer-metadata)).

        
The Credential Endpoint may bind an issued Credential to specific cryptographic key material, in which case Credential requests include proof(s) of possession or attestations for the key material. Multiple key proof types are supported.


### 3.2. OAuth 2.0
According to the OAuth 2.0 framework, each Credential Issuer acts as a Resource Server that is protected by an Access Token issued by an Authorization Server, as defined in OAuth 2.0 [[RFC6749](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC6749)]. The same Authorization Server can protect one or more Credential Issuers. Wallets identify the Authorization Server for a Credential Issuer by referring to the Credential Issuer's metadata (see [Section 12.2](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-issuer-metadata)).
All OAuth 2.0 Grant Types and extensions mechanisms can be used in conjunction with the Credential issuance API. Aspects not defined in this specification are expected to follow [[RFC6749](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC6749)].
Existing OAuth 2.0 mechanisms are extended as follows:

- A new Grant Type "Pre-Authorized Code" is defined to facilitate flows where the preparation of the Credential issuance is conducted before the actual OAuth flow starts (see [Section 3.5](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#pre-authz-code-flow)).

          - A new authorization details [[RFC9396](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC9396)] type `openid_credential` is defined to convey the details about the Credentials (including Credential Dataset, Credential Formats, and Credential types) the Wallet wants to obtain (see [Section 5.1.1](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#authorization-details)).

          - Client metadata is used to convey the Wallet's metadata. The new Client metadata parameter `credential_offer_endpoint` is added to allow a Wallet (acting as OAuth 2.0 client) to publish its Credential Offer Endpoint (see [Section 12.1](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#client-metadata)).

          - Authorization Endpoint: The additional parameter `issuer_state` is added to convey state in the context of processing an issuer-initiated Credential Offer (see [Section 5.1](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-authz-request)).

        


### 3.3. Core Concepts
In the context of this specification, Credential Datasets, Credential Format and Credential Format Profile are defined in [Section 2](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#terminology).
While in principle independent of each other, the Credential Dataset and the Credential Format can have a relationship in the sense that an Issuer may only offer certain Credential Formats for certain Credential Datasets.
An End-User typically authorizes the issuance of Credentials with a specific Credential Dataset, but does not usually care about the Credential Format. The same Credential Dataset may even be issued in different Credential Formats or with multiple Credential instances.


#### 3.3.1. Credential Formats and Credential Format Profiles
This specification is Credential Format agnostic and allows implementers to leverage specific capabilities of Credential Formats of their choice.
To this end, extension points to add Credential Format specific parameters in the Credential Issuer metadata, Credential Offer, Authorization Request, and Credential Request are defined.
Credential Format Profiles for IETF SD-JWT VC [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#I-D.ietf-oauth-sd-jwt-vc)], ISO mdoc [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#ISO.18013-5)], and W3C VCDM [[VC_DATA](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#VC_DATA)] are specified in [Appendix A](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#format-profiles).
Other specifications or deployments can define their own Credential Format Profiles using the above-mentioned extension points.


#### 3.3.2. Batch Credential Issuance
This specification enables the issuance of Verifiable Credentials through the Credential Endpoint.
A single request to this endpoint may request the issuance of a batch of one or more Verifiable Credentials.
Credentials can vary in their format, including Credential Format Profile-specific parameters, in their contents known as the Credential Dataset, and in the cryptographic data such as Issuer signatures, hashes, and keys used for Cryptographic Key Binding.
Credentials can therefore vary in the following dimensions:

- Credential Format

            - Credential Dataset

            - Cryptographic Data

          
In the context of a single request, the batch of issued Credentials sent in response MUST share the same Credential Format and Credential Dataset, but SHOULD contain different Cryptographic Data. For example to achieve unlinkability between the Credentials, each credential should be bound to different cryptographic keys.
To issue multiple Verifiable Credentials with differing Credential Formats or Credential Datasets, multiple requests MUST be sent to the Credential Endpoint.


#### 3.3.3. Issuance Flow Variations
The issuance can have multiple characteristics that can be combined depending on the use cases:

- Authorization Code Flow or Pre-Authorized Code Flow: The Credential Issuer can obtain End-User information to turn into a Verifiable Credential using End-User authentication and consent at the Credential Issuer's Authorization Endpoint (Authorization Code Flow) or using out-of-band mechanisms outside of the issuance flow (Pre-Authorized Code Flow).

            - Wallet initiated or Issuer initiated: The request from the Wallet can be sent to the Credential Issuer without any gesture from the Credential Issuer (Wallet Initiated) or following the communication from the Credential Issuer (Issuer Initiated).

            - Same-device or Cross-device Credential Offer: The End-User may receive the Credential Offer from the Credential Issuer either on the same device as the device the Wallet resides on, or through any other means, such as another device or postal mail, so that the Credential Offer can be communicated to the Wallet.

            - Immediate or Deferred: The Credential Issuer can issue the Credential directly in response to the Credential Request (immediate) or requires time and needs the Wallet to come back to retrieve Credential (deferred).

          
The following subsections illustrate some of the authorization flows supported by this specification.


#### 3.3.4. Identifying Credentials Being Issued Throughout the Issuance Flow
Below is the summary of how Credential(s) that are being issued are identified throughout the issuance flow:

- In the Credential Offer, the Credential Issuer identifies offered Credential Configurations
using the `credential_configuration_ids` parameter.

            - When the Wallet uses Authorization Details in the Authorization Request, the Wallet uses
the `credential_configuration_id` parameter to identify the requested Credential Configurations.
The Authorization Server returns an `authorization_details` parameter containing
the `credential_identifiers` parameter in the Token Response,
and the Wallet uses those `credential_identifier` values in the Credential Request.

            - When the Wallet uses `scope` parameter in the Authorization Request, the `scope` value(s)
are used to identify requested Credential Configurations. In this case, the Authorization Server has two options.
If the Authorization Server supports returning `credential_identifiers` parameter
in the Token Response, it MAY do so, in which case the Wallet uses those `credential_identifier` values
in the Credential Request. If the Authorization Server does not support returning an `authorization_details` parameter containing the
`credential_identifiers` parameter in the Token Response, the Wallet uses `credential_configuration_id` parameter
in the Credential Request.

          


### 3.4. Authorization Code Flow
The Authorization Code Flow uses the grant type `authorization_code` as defined in [[RFC6749](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC6749)] to issue Access Tokens.
Figure 1 shows the Authorization Code Flows with the two variations that can be implemented for the issuance of Credentials, as outlined in this specification:

- 
            **Wallet-initiated variation**, described in [Appendix H.4](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#use-case-4) or [Appendix H.6](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#use-case-6);

          - 
            **Issuer-initiated variation**, described in [Appendix H.1](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#use-case-1).

        
Please note that the diagram does not illustrate all the optional features defined in this specification.

          
```
+----------+    +-----------+        +----------------------+   +-------------------+
| End-User |    |   Wallet  |        | Authorization Server |   | Credential Issuer |
+----------+    +-----------+        +----------------------+   +-------------------+
      |               |                           |                        |
      | (1a) End-User |                           |                        |
      |  selects      |  (1b) Credential Offer    |                        |
      |  Credential-->|  (credential type)        |                        |
      |               |<---------------------------------------------------|
      |               |                           |                        |
      |               |  (2) Obtains Issuer's     |                        |
      |               |      Credential Issuer    |                        |
      |               |      metadata             |                        |
      |               |--------------------------------------------------->|
      |               |                           |                        |
      |               |                           |  (3) Authorization     |
      |               |                           |      Request           |
      |               |                           |      (type(s) of       |
      |               |                           |      Credentials to    |
      |               |                           |      be issued)        |
      |               |-------------------------->|                        |
      |               |                           |                        |
      |  End-User Authentication / Consent        |                        |
      |               |                           |  (4) Authorization     |
      |               |                           |      Response (code)   |
      |               |<--------------------------|                        |
      |               |                           |                        |
      |               |                           |  (5) Token Request     |
      |               |                           |      (code)            |
      |               |-------------------------->|      Token Response    |
      |               |                           |      (Access Token)    |
      |               |<--------------------------|                        |
      |               |                           |                        |
      |               |  (6) Credential Request   |                        |
      |               |      (Access Token,       |                        |
      |               |       proof(s))           |                        |
      |               |--------------------------------------------------->|
      |               |                           |                        |
      |               |      Credential Response  |                        |
      |               |      with Credential(s)   |                        |
      |               |      OR Transaction ID    |                        |
      |               |<---------------------------------------------------|
```

Figure 1:
Issuance using Authorization Code Flow
          
(1a) The Wallet-initiated flow begins as the End-User requests a Credential via the Wallet from the Credential Issuer. The End-User either selects a Credential from a pre-configured list of Credentials ready to be issued, or alternatively, the Wallet gives guidance to the End-User to select a Credential from a Credential Issuer based on the information it received in the presentation request from a Verifier.
(1b) The Issuer-initiated flow begins as the Credential Issuer generates a Credential Offer for certain Credential(s) that it communicates to the Wallet, for example, as a QR code or as a URI. The Credential Offer contains the Credential Issuer's URL and the information about the Credential(s) being offered. This step is defined in [Section 4.1](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-offer).
(2) The Wallet uses the Credential Issuer's URL to fetch the Credential Issuer metadata, as described in [Section 12.2](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-issuer-metadata). The Wallet needs the metadata to learn the Credential types and formats that the Credential Issuer supports and to determine the Authorization Endpoint (OAuth 2.0 Authorization Server) as well as Credential Endpoint required to start the request. This specification supports configurations where the Credential Endpoint and the Authorization Endpoint are managed by either separate entities or a single entity.
(3) The Wallet sends an Authorization Request to the Authorization Endpoint. The Authorization Endpoint processes the Authorization Request, which typically includes authenticating the End-User and gathering End-User consent. Note: The Authorization Request may be sent as a Pushed Authorization Request.
(4) The Authorization Endpoint returns the Authorization Response with the Authorization Code upon successfully processing the Authorization Request.
Note: Steps (3) and (4) happen in the front channel, by redirecting the End-User via the User Agent. Those steps are defined in [Section 5](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#authorization-endpoint). The Authorization Server and the User Agent may exchange any further messages between the steps if required by the Authorization Server to authenticate the End-User. For example, the Authorization Server may request Credential presentation as a means to authenticate or identify the End-User during the issuance flow, as described in [Appendix H.5](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#use-case-5).
(5) The Wallet sends a Token Request to the Token Endpoint with the Authorization Code obtained in Step (4). The Token Endpoint returns an Access Token in the Token Response upon successfully validating the Authorization Code. This step happens in the back-channel communication (direct communication between two systems using HTTP requests and responses without using redirects through an intermediary such as a browser). This step is defined in [Section 6](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#token-endpoint).
(6) The Wallet sends a Credential Request to the Credential Issuer's Credential Endpoint with the Access Token and (optionally) the proof(s) of possession of the private key of a key pair to which the Credential Issuer should bind the issued Credential to. Upon successfully validating Access Token and proof(s), the Credential Issuer returns a Credential in the Credential Response. This step is defined in [Section 8](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-endpoint).
If the Credential Issuer requires more time to issue a Credential, the Credential Issuer may return a Transaction ID and a time interval in the Credential Response. The Wallet may send a Deferred Credential Request with the Transaction ID to obtain a Credential after the specified time interval has passed, as defined in [Section 9](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#deferred-credential-issuance).
Note: This flow is based on OAuth 2.0 and the Authorization Code Grant type, but this specification can be used with other OAuth 2.0 grant types as well.


### 3.5. Pre-Authorized Code Flow
Figure 2 is a diagram of a Credential issuance using the Pre-Authorized Code Flow. In this flow, before initiating the flow with the Wallet, the Credential Issuer first conducts the steps required to prepare for Credential issuance, e.g., End-User authentication and authorization. Consequently, the Pre-Authorized Code is sent by the Credential Issuer to the Wallet. This flow does not use the Authorization Endpoint, and the Wallet exchanges the Pre-Authorized Code for the Access Token directly at the Token Endpoint. The Access Token is then used to request Credential issuance at the Credential Endpoint. See [Appendix H.2](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#use-case-2) for the description of such a use case.
How the End-User provides information required for the issuance of a requested Credential to the Credential Issuer and the business processes conducted by the Credential Issuer to prepare a Credential are out of scope of this specification.
This flow uses the OAuth 2.0 Grant Type `urn:ietf:params:oauth:grant-type:pre-authorized_code`, which is defined in [Section 4.1.1](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-offer-parameters).
The following diagram is based on the Credential Issuer-initiated flow, as described in the use case in [Appendix H.2](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#use-case-2). Please note that it does not illustrate all the optional features outlined in this specification.

          
```
+----------+   +-----------+           +----------------------+   +-------------------+
| End-User |   |   Wallet  |           | Authorization Server |   | Credential Issuer |
+----------+   +-----------+           +----------------------+   +-------------------+
      |              |                              |                       |
      |              |  (1) End-User provides       |                       |
      |              |      information required    |                       |
      |              |      for the issuance of     |                       |
      |              |      a certain Credential    |                       |
      |              |----------------------------------------------------->|
      |              |                              |                       |
      |              |  (2) Credential Offer        |                       |
      |              |      (Pre-Authorized Code)   |                       |
      |              |<-----------------------------------------------------|
      |              |  (3) Obtains Issuer's        |                       |
      |              |      Credential Issuer       |                       |
      |              |      metadata                |                       |
      |              |----------------------------------------------------->|
      |   interacts  |                              |                       |
      |------------->|                              |                       |
      |              |                              |                       |
      |              |  (4) Token Request           |                       |
      |              |      (Pre-Authorized Code,   |                       |
      |              |       tx_code)               |                       |
      |              |----------------------------->|                       |
      |              |      Token Response          |                       |
      |              |      (access_token)          |                       |
      |              |<-----------------------------|                       |
      |              |                              |                       |
      |              |  (5) Credential Request      |                       |
      |              |      (access_token, proof(s))|                       |
      |              |----------------------------------------------------->|
      |              |      Credential Response     |                       |
      |              |      (Credential(s))         |                       |
      |              |<-----------------------------------------------------|
```

Figure 2:
Issuance using Pre-Authorized Code Flow
          
(1) The Credential Issuer successfully obtains consent and End-User data required for the issuance of a requested Credential from the End-User using an Issuer-specific business process.
(2) The flow defined in this specification begins as the Credential Issuer generates a Credential Offer for certain Credential(s) and communicates it to the Wallet, for example, as a QR code or as a URI. The Credential Offer contains the Credential Issuer's URL, the information about the Credential(s) being offered, and the Pre-Authorized Code. This step is defined in [Section 4.1](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-offer).
(3) The Wallet uses the Credential Issuer's URL to fetch its metadata, as described in [Section 12.2](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-issuer-metadata). The Wallet needs the metadata to learn the Credential types and formats that the Credential Issuer supports, and to determine the Token Endpoint (at the OAuth 2.0 Authorization Server) as well as the Credential Endpoint required to start the request.
(4) The Wallet sends the Pre-Authorized Code obtained in Step (2) in the Token Request to the Token Endpoint. The Wallet will additionally send a Transaction Code provided by the End-User, if it was required by the Credential Issuer. This step is defined in [Section 6](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#token-endpoint).
(5) This step is the same as Step (6) in the Authorization Code Flow.
It is important to note that anyone who possesses a valid Pre-Authorized Code, without further security measures, would be able to receive a VC from the Credential Issuer. Implementers MUST implement mitigations most suitable to the use case.
One such mechanism defined in this specification is the usage of Transaction Codes. The Credential Issuer indicates the usage of Transaction Codes in the Credential Offer and sends the Transaction Code to the End-User via a second channel different than the issuance flow. After the End-User provides the Transaction Code, the Wallet sends the Transaction Code within the Token Request, and the Authorization Server verifies the Transaction Code.
For more details and concrete mitigations, see [Section 13.6](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#security-considerations-pre-authz-code).
