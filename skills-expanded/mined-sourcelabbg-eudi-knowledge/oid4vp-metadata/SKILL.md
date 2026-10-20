---
name: "oid4vp-metadata"
description: "Use when configuring wallet or verifier metadata, wallet invocation schemes (openid4vp://, universal links, DC API), or implementing Verifier Attestation JWTs. Covers: authorization_server metadata, vp_formats_supported, client_metadata parameters, and verifier_attestation JWT format."
sections:
  - "9. Wallet Invocation"
  - "10. Wallet Metadata (Authorization Server Metadata)"
  - "10.1. Additional Wallet Metadata Parameters"
  - "10.2. Obtaining Wallet's Metadata"
  - "11. Verifier Metadata (Client Metadata)"
  - "11.1. Additional Verifier Metadata Parameters"
  - "12. Verifier Attestation JWT"
---

<!-- ARF version: 1.0-final-2025-07-09 -->
<!-- Tokens: ~1990 -->

## 9. Wallet Invocation
The Verifier can use one of the following mechanisms to invoke a Wallet:

- Custom URL scheme as an `authorization_endpoint` (for example, `openid4vp://` as defined in [Section 13.1.2](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#openid4vp-scheme))

        - URL (including Domain-bound Universal Links/App link) as an `authorization_endpoint`

      
For a cross device flow, either of the above options MAY be presented as a QR code for the End-User to scan using a Wallet or an arbitrary camera application on a user-device.
The Wallet can also be invoked from the web or a native app using the Digital Credentials API as described in [Appendix A](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#dc_api). As described in detail in [Appendix A](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#dc_api), DC API provides privacy, security (see [Section 14.2](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#session_fixation)), and user experience benefits (particularly in the cases where an End-User has multiple Wallets).

---

## 10. Wallet Metadata (Authorization Server Metadata)
This specification defines how the Verifier can determine Credential formats, proof types and algorithms supported by the Wallet to be used in a protocol exchange.


### 10.1. Additional Wallet Metadata Parameters
This specification defines new metadata parameters according to [[RFC8414](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC8414)].

          
`vp_formats_supported`:
          
            REQUIRED. An object containing a list of name/value pairs, where the name is a Credential Format Identifier and the value defines format-specific parameters that a Wallet supports. For specific values that can be used, see [Appendix B](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#format_specific_parameters).
Deployments can extend the formats supported, provided Issuers, Holders and Verifiers all understand the new format.
The following is a non-normative example of a `vp_formats_supported` parameter:

```
"vp_formats_supported": {
  "jwt_vc_json": {
    "alg_values": [
      "ES256K",
      "ES384"
    ]
  }
}
```


          

`client_id_prefixes_supported`:
          
            OPTIONAL. A non-empty array of strings containing the values of the Client Identifier Prefixes that the Wallet supports. The values defined by this specification are `pre-registered` (which represents the behavior when no Client Identifier Prefix is used), `redirect_uri`, `openid_federation`, `verifier_attestation`, `decentralized_identifier`, `x509_san_dns` and `x509_hash`. If omitted, the default value is `pre-registered`. Other values may be used when defined in the profiles or extensions of this specification.

        

Additional Wallet metadata parameters MAY be defined and used,
as described in [[RFC8414](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC8414)].
The Verifier MUST ignore any unrecognized parameters.


### 10.2. Obtaining Wallet's Metadata
A Verifier utilizing this specification has multiple options to obtain the Wallet's metadata:

- Verifier obtains the Wallet's metadata dynamically, e.g., using [[RFC8414](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC8414)] or out-of-band mechanisms. See [Section 10](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#as_metadata_parameters) for the details.

          - Verifier has pre-obtained a static set of the Wallet's metadata. See [Section 13.1.2](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#openid4vp-scheme) for the example.

---

## 11. Verifier Metadata (Client Metadata)
To convey Verifier metadata, Client metadata defined in Section 2 of [[RFC7591](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC7591)] is used.
This specification defines how the Wallet can determine Credential formats, proof types and algorithms supported by the Verifier to be used in a protocol exchange.


### 11.1. Additional Verifier Metadata Parameters
This specification defines the following new Client metadata parameters according to [[RFC7591](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC7591)], to be used by the Verifier:

          
`vp_formats_supported`:
          REQUIRED. An object containing a list of name/value pairs, where the name is a Credential Format Identifier and the value defines format-specific parameters that a Verifier supports. For specific values that can be used, see [Appendix B](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#format_specific_parameters).
Deployments can extend the formats supported, provided Issuers, Holders and Verifiers all understand the new format.

        

Additional Verifier metadata parameters MAY be defined and used,
as described in [[RFC7591](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC7591)].
The Wallet MUST ignore any unrecognized parameters.

---

## 12. Verifier Attestation JWT
The Verifier Attestation JWT is a JWT especially designed to allow a Wallet to authenticate a Verifier in a secure and flexible manner. A Verifier Attestation JWT is issued to the Verifier by a party that Wallets trust for the purpose of authentication and authorization of Verifiers. The way this trust is established is out of scope of this specification. Every Verifier is bound to a public key, the Verifier MUST always present a Verifier Attestation JWT along with the proof of possession for this key. In the case of the Client Identifier Prefix `verifier_attestation`, the authorization request is signed with this key, which serves as proof of possession.
A Verifier Attestation JWT MUST contain the following claims:

- 
          `iss`: REQUIRED. This claim identifies the issuer of the Verifier Attestation JWT. The `iss` value MAY be used to retrieve the issuer's public key. How the trust is established between Wallet and Issuer and how the public key is obtained for validating the attestation's signature is out of scope of this specification.

        - 
          `sub`: REQUIRED. The value of this claim MUST be the `client_id` of the client making the Credential request.

        - 
          `iat`: OPTIONAL. A number representing the time at which the Verifier Attestation JWT was issued using the syntax defined in [RFC7519].

        - 
          `exp`: REQUIRED. A number representing the time at which the Verifier Attestation JWT expires using the syntax defined in [RFC7519]. The Wallet MUST reject any Verifier Attestation JWT with an expiration time that has passed, subject to allowable clock skew between systems.

        - 
          `nbf`: OPTIONAL. A number representing the time before which the token MUST NOT be accepted for processing.

        - 
          `cnf`: REQUIRED. This claim contains the confirmation method as defined in [[RFC7800](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC7800)]. It MUST contain a JSON Web Key [[RFC7517](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC7517)] as defined in Section 3.2 of [[RFC7800](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC7800)]. This claim determines the public key that the Verifier MUST prove possession of the corresponding private key for when presenting the Verifier Attestation JWT. This additional security measure allows the Verifier to obtain a Verifier Attestation JWT from a trusted issuer and use it for a long time independent of that issuer without the risk of an adversary impersonating the Verifier by replaying a captured attestation.

      
Additional claims MAY be defined and used in the Verifier Attestation JWT,
as described in [[RFC7519](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC7519)].
The Wallet MUST ignore any unrecognized claims.
Verifier Attestation JWTs compliant with this specification MUST use the media type `application/verifier-attestation+jwt` as defined in [Appendix E.6.1](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#va_media_type).
A Verifier Attestation JWT MUST set the `typ` JOSE header to `verifier-attestation+jwt`.
The Verifier Attestation JWT MAY be conveyed in the header of a JWS signed object (JOSE header).
This specification introduces a JOSE header, which can be used to add a JWT to such a header as follows:

- 
          `jwt`: This JOSE header MUST contain a JWT.

      
In the context of this specification, such a JWT MUST set the `typ` JOSE header to `verifier-attestation+jwt`.
