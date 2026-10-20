---
name: "oid4vp-authorization-request"
description: "Use when constructing or validating an OpenID4VP authorization request. Covers: request parameters (presentation_definition, dcql_query, nonce, response_type, response_mode, response_uri, client_id), client_id prefixes (pre-registered, redirect_uri, did, verifier_attestation, x509_san_dns, x509_san_uri), request_uri with GET and POST methods, JAR (RFC9101), Verifier Info and Proof of Possession."
sections:
  - "4. Scope"
---

<!-- ARF version: 1.0-final-2025-07-09 -->
<!-- Tokens: ~754 -->

## 4. Scope
OpenID for Verifiable Presentations extends existing OAuth 2.0 mechanisms in the following ways:

- A new query language, the Digital Credentials Query Language (DCQL), is defined to enable requesting Presentations in an easier and more flexible way. See [Section 6](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#dcql_query) for more details.

        - A new `dcql_query` Authorization Request parameter is defined to request Presentation of Credentials in the JSON-encoded DCQL format. See [Section 5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#vp_token_request) for more details.

        - A new `vp_token` response parameter is defined to return Presentations with or without Holder Binding to the Verifier in either Authorization or Token Response depending on the Response Type. See [Section 8](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#response) for more details.

        - New Response Types `vp_token` and `vp_token id_token` are defined to request Credentials to be returned in the Authorization Response (standalone or along with a Self-Issued ID Token [[SIOPv2](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#SIOPv2)]). See [Section 8](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#response) for more details.

        - A new OAuth 2.0 Response Mode `direct_post` is defined to support sending the response across devices, or when the size of the response exceeds the redirect URL character size limitation. See [Section 8.2](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#response_mode_post) for more details.

        - The `format` parameter is used throughout the protocol in order to enable customization according to the specific needs of a particular Credential format. Examples in [Appendix B](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#format_specific_parameters) are given for Credential formats as specified in [[VC_DATA](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#VC_DATA)], [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.18013-5)], and [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-oauth-sd-jwt-vc)].

        - The concept of a Client Identifier Prefix to enable deployments of this specification to use different mechanisms to obtain and validate metadata of the Verifier beyond the scope of [[RFC6749](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC6749)].

        - A mechanism specifying the use of OpenID4VP with the Digital Credentials API (see [Appendix A](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#dc_api)).

      
Presentation of Credentials using OpenID for Verifiable Presentations can be combined with the End-User authentication using [[SIOPv2](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#SIOPv2)], and the issuance of OAuth 2.0 Access Tokens.
