---
name: "oid4vp-format-sd-jwt-vc"
description: "Use when implementing IETF SD-JWT VC format in OpenID4VP. Covers: SD-JWT VC format identifier, presentation response structure, key binding JWT, and transaction data for SD-JWT VCs."
sections:
  - "B.3. IETF SD-JWT VC"
  - "B.3.1. Format Identifier"
  - "B.3.2. Example Credential"
  - "B.3.3. Transaction Data"
  - "B.3.4. Metadata"
  - "B.3.5. Parameter in the meta parameter in Credential Query"
  - "B.3.6. Presentation Response"
  - "B.3.7. SD-JWT VCLD"
---

<!-- ARF version: 1.0-final-2025-07-09 -->
<!-- Tokens: ~4357 -->

### B.3. IETF SD-JWT VC
This section defines how Credentials complying with [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-oauth-sd-jwt-vc)] can be presented to the Verifier using this specification.
If `require_cryptographic_holder_binding` is set to `true` in the Credential Query, the Wallet MUST return an SD-JWT [[I-D.ietf-oauth-selective-disclosure-jwt](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-oauth-selective-disclosure-jwt)] with a Key Binding JWT (SD-JWT+KB) as the Verifiable Presentation. SD-JWTs that do not support Holder Binding (i.e., do not have a `cnf` Claim) cannot be returned in this case.
If `require_cryptographic_holder_binding` is set to `false`, an SD-JWT without the Key Binding JWT MAY be returned.


#### B.3.1. Format Identifier
The Credential Format Identifier is `dc+sd-jwt`.


#### B.3.2. Example Credential
The following is a non-normative example of the unsecured payload of an IETF SD-JWT VC that will be used throughout this section:

```
{
  "vct": "https://credentials.example.com/identity_credential",
  "given_name": "John",
  "family_name": "Doe",
  "birthdate": "1940-01-01"
}
```

The following is a non-normative example of an IETF SD-JWT VC using the unsecured payload above, containing claims that are selectively disclosable.

```
{
  "_sd": [
    "3oUCnaKt7wqDKuyh-LgQozzfhgb8gO5Ni-RCWsWW2vA",
    "8z8z9X9jUtb99gjejCwFAGz4aqlHf-sCqQ6eM_qmpUQ",
    "Cxq4872UXXngGULT_kl8fdwVFkyK6AJfPZLy7L5_0kI",
    "TGf4oLbgwd5JQaHyKVQZU9UdGE0w5rtDsrZzfUaomLo",
    "jsu9yVulwQQlhFlM_3JlzMaSFzglhQG0DpfayQwLUK4",
    "sFcViHN-JG3eTUyBmU4fkwusy5I1SLBhe1jNvKxP5xM",
    "tiTngp9_jhC389UP8_k67MXqoSfiHq3iK6o9un4we_Y",
    "xsKkGJXD1-e3I9zj0YyKNv-lU5YqhsEAF9NhOr8xga4"
  ],
  "iss": "https://example.com/issuer",
  "iat": 1683000000,
  "exp": 1883000000,
  "vct": "https://credentials.example.com/identity_credential",
  "_sd_alg": "sha-256",
  "cnf": {
    "jwk": {
      "kty": "EC",
      "crv": "P-256",
      "x": "TCAER19Zvu3OHF4j4W4vfSVoHIP1ILilDls7vCeGemc",
      "y": "ZxjiWWbZMQGHVWKVQ4hbSIirsVfuecCE6t4jT9F2HZQ"
    }
  }
}
```

The following are disclosures belonging to the claims from the example above.
**Claim `given_name`**:

- SHA-256 Hash: `jsu9yVulwQQlhFlM_3JlzMaSFzglhQG0DpfayQwLUK4`

            - Disclosure:
              `WyIyR0xDNDJzS1F2ZUNmR2ZyeU5STjl3IiwgImdpdmVuX25hbWUiLCAiSm9o`
              `biJd`

            - Contents:
`["2GLC42sKQveCfGfryNRN9w", "given_name", "John"]`

          
**Claim `family_name`**:

- SHA-256 Hash: `TGf4oLbgwd5JQaHyKVQZU9UdGE0w5rtDsrZzfUaomLo`

            - Disclosure:
              `WyJlbHVWNU9nM2dTTklJOEVZbnN4QV9BIiwgImZhbWlseV9uYW1lIiwgIkRv`
              `ZSJd`

            - Contents:
`["eluV5Og3gSNII8EYnsxA_A", "family_name", "Doe"]`

          
**Claim `birthdate`**:

- SHA-256 Hash: `tiTngp9_jhC389UP8_k67MXqoSfiHq3iK6o9un4we_Y`

            - Disclosure:
              `WyI2SWo3dE0tYTVpVlBHYm9TNXRtdlZBIiwgImJpcnRoZGF0ZSIsICIxOTQw`
              `LTAxLTAxIl0`

            - Contents:
`["6Ij7tM-a5iVPGboS5tmvVA", "birthdate", "1940-01-01"]`

          


#### B.3.3. Transaction Data
It is RECOMMENDED that each transaction data type defines a top-level claim parameter to be used in the Key Binding JWT to return the processed transaction data. Additionally, it is RECOMMENDED that it specifies the processing rules, potentially including any hash function to be applied, and the expected resulting structure.
The transaction data mechanism requires the use of an SD-JWT VC with Cryptographic Holder Binding. Wallets MUST reject requests with transaction data types that have the `require_cryptographic_holder_binding` parameter set to `false`.


##### B.3.3.1. A Profile of Transaction Data in SD-JWT VC
The following is one profile that can be included in a transaction data type specification:

- 
                The `transaction_data` request parameter includes the following parameter, in addition to `type` and `credential_ids` from [Section 5.1](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#new_parameters):

- 
                    `transaction_data_hashes_alg`: OPTIONAL. Non-empty array of strings each representing a hash algorithm identifier, one of which MUST be used to calculate hashes in `transaction_data_hashes` response parameter. The value of the identifier MUST be a hash algorithm value from the "Hash Name String" column in the IANA "Named Information Hash Algorithm" registry [[IANA.Hash.Algorithms](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#IANA.Hash.Algorithms)] or a value defined in another specification and/or profile of this specification. If this parameter is not present, a default value of `sha-256` MUST be used. To promote interoperability, implementations MUST support the sha-256 hash algorithm.

                

              - 
                The Key Binding JWT in the response includes the following top-level parameters:

- 
                    `transaction_data_hashes`: A non-empty array of strings where each element is a base64url-encoded hash. Each of these hashes is calculated using a hash function over the string received in the `transaction_data` request parameter (base64url decoding is not performed before hashing). Each hash value ensures the integrity of, and maps to, the respective transaction data object. If `transaction_data_hashes_alg` was specified in the request, the hash function MUST be one of its values. If `transaction_data_hashes_alg` was not specified in the request, the hash function MUST be `sha-256`.

                  - 
                    `transaction_data_hashes_alg`: REQUIRED when this parameter was present in the `transaction_data` request parameter. String representing the hash algorithm identifier used to calculate hashes in `transaction_data_hashes` response parameter.

                

            


#### B.3.4. Metadata
The `vp_formats_supported` parameter of the Verifier metadata or Wallet metadata MUST have the Credential Format Identifier as a key, and the value MUST be an object consisting of the following name/value pairs:

- 
              `sd-jwt_alg_values`: OPTIONAL. A non-empty array containing fully-specified identifiers of cryptographic algorithms (as defined in [[I-D.ietf-jose-fully-specified-algorithms](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-jose-fully-specified-algorithms)]) supported for an Issuer-signed JWT of an SD-JWT.

            - 
              `kb-jwt_alg_values`: OPTIONAL. A non-empty array containing fully-specified identifiers of cryptographic algorithms (as defined in [[I-D.ietf-jose-fully-specified-algorithms](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-jose-fully-specified-algorithms)]) supported for a Key Binding JWT (KB-JWT).

          
The following is a non-normative example of `client_metadata` request parameter value in a request to present an IETF SD-JWT VC.

```
{
  "vp_formats_supported": {
    "dc+sd-jwt": {
      "sd-jwt_alg_values": ["ES256", "ES384"],
      "kb-jwt_alg_values": ["ES256", "ES384"]
    }
  }
}
```


#### B.3.5. Parameter in the meta parameter in Credential Query
The following is an SD-JWT VC specific parameter in the `meta` parameter in a Credential Query as defined in [Section 6.1](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#credential_query).

            
`vct_values`:
            REQUIRED. A non-empty array of strings that specifies allowed values for
the type of the requested Verifiable Credential. All elements in the array MUST
be valid type identifiers as defined in [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-oauth-sd-jwt-vc)]. The Wallet
MAY return Credentials that inherit from any of the specified types, following
the inheritance logic defined in [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-oauth-sd-jwt-vc)].

          


#### B.3.6. Presentation Response
A non-normative example DCQL query using the SD-JWT VC format is shown in [Section 7.4](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#dcql_query_example).
The respective response is shown in [Section 8.1.1](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#response_dcql_query).
Additional examples are shown in [Appendix D](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#more_dcql_query_examples).
The following requirements apply to the `nonce` and `aud` claims in the Key Binding JWT:

- the `nonce` claim MUST be the value of `nonce` from the Authorization Request;

            - the `aud` claim MUST be the value of the Client Identifier, except for requests over the DC API where it MUST be the Origin prefixed with `origin:`, as described in [Appendix A.4](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#dc_api_response).

          
The following is a non-normative example of the unsecured payload of the Key Binding JWT of a Verifiable Presentation.

```
{
  "nonce": "n-0S6_WzA2Mj",
  "aud": "x509_san_dns:client.example.org",
  "iat": 1709838604,
  "sd_hash": "Dy-RYwZfaaoC3inJbLslgPvMp09bH-clYP_3qbRqtW4",
  "transaction_data_hashes": [ "fOBUSQvo46yQO-wRwXBcGqvnbKIueISEL961_Sjd4do" ]
}
```


#### B.3.7. SD-JWT VCLD
SD-JWT VCLD (SD-JWT Verifiable Credentials with JSON-LD) extends the IETF SD-JWT VC [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-oauth-sd-jwt-vc)] Credential format and allows to incorporate existing data models that use Linked Data, e.g., W3C VCDM [[VC_DATA](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#VC_DATA)], while enabling a consistent and uncomplicated approach to selective disclosure.
Information contained in SD-JWT VCLD Credentials can be processed using a JSON-LD [[JSON-LD](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#JSON-LD)] processor after the SD-JWT VC processing.
When IETF SD-JWT VC is mentioned in this specification, SD-JWT VCLD defined in this section MAY be used.


##### B.3.7.1. Format
SD-JWT VCLD Credentials are valid SD-JWT VCs and all requirements from [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-oauth-sd-jwt-vc)] apply. Additionally, the requirements listed in this section apply.
For compatibility with JWT processors, the following registered Claims from [[RFC7519](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC7519)] and [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-oauth-sd-jwt-vc)] MUST be used instead of any respective counterpart properties from W3C VCDM or elsewhere:

- 
                `vct` to represent the type of the Credential.

              - 
                `exp` and `nbf` to represent the validity period of SD-JWT VCLD (i.e., cryptographic signature).

              - 
                `iss` to represent the Credential Issuer.

              - 
                `status` to represent the information to obtain the status of the Credential.

            
IETF SD-JWT VC is extended with the following claim:

- 
                `ld`: OPTIONAL. Contains a JSON-LD [[JSON-LD](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#JSON-LD)] object in compact form, e.g., [[VC_DATA](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#VC_DATA)].

            


##### B.3.7.2. Processing
The following outlines a suggested non-normative set of processing steps for SD-JWT VCLD:


###### B.3.7.2.1. Step 1: SD-JWT VC Processing

- A receiver (holder or verifier) of an SD-JWT VCLD applies the processing rules outlined in Section 4 of [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-oauth-sd-jwt-vc)], including verifying signatures, validity periods, status information, etc.

                - If the `vct` value is associated with any SD-JWT VC Type Metadata, schema validation of the entire SD-JWT VCLD is performed, including the nested `ld` claim.

                - Additionally, trust framework rules are applied, such as ensuring the Credential Issuer is authorized to issue SD-JWT VCLDs for the specified `vct` value.

              


###### B.3.7.2.2. Step 2: Business Logic Processing

- Once the SD-JWT VC is verified and trusted by the SD-JWT VC processor, and if the `ld` claim is present, the receiver extracts the JSON-LD object from the `ld` claim and uses this for the business logic object. If the `ld` claim is not present, the entire SD-JWT VC is considered to represent the business logic object.

                - The business logic object is then passed on for further use case-specific processing and validation. The business logic assumes that all security-critical functions (e.g., signature verification, trusted issuer) have already been performed during the previous step. Additional schema validation is applied if provided in the `ld` claim, e.g., to support SHACL schemas. Note that while a `vct` claim is required, SD-JWT VC type metadata resolution and related schema validation is optional in certain cases.

              


##### B.3.7.3. Examples
The following is a non-normative example of an unsecured payload of an SD-JWT VCLD (i.e., before applying the modifications to enable selective disclosure and before adding validity claims).

```
{
  "vct": "https://credentials.example.com/example_credential",
  "ld": {
    "@context": [
      "https://www.w3.org/ns/credentials/v2",
      "https://w3id.org/citizenship/v3"
    ],
    "credentialSubject": {
      "givenName": "John",
      "familyName": "Doe",
      "birthDate": "1978-07-17"
    }
  }
}
```

The following payload would be used in the SD-JWT after encoding the payload above and enabling selective disclosure on the End-User specific claims within `credentialSubject`:

```
{
  "iss": "https://issuer.example.com",
  "iat": 1683000000,
  "exp": 1883000000,
  "vct": "https://credentials.example.com/example_credential",
  "ld": {
    "@context": [
      "https://www.w3.org/ns/credentials/v2",
      "https://w3id.org/citizenship/v3"
    ],
    "credentialSubject": {
      "_sd": [
        "6BJdQrO24ejTTMsFI-wGiJJmGrbseWc5IwCCp4NAJ0k",
        "NTDVsbVAwS9AnUVq-_YG_wv0yGD0bv2JstX-AmvN65I",
        "ts0pyPntLjD0_NcgNOI3hd_2WjbZw21p2LfqhOC0b-U"
      ]
    }
  },
  "_sd_alg": "sha-256",
  "cnf": {
    "jwk": {
      "kty": "EC",
      "crv": "P-256",
      "x": "TCAER19Zvu3OHF4j4W4vfSVoHIP1ILilDls7vCeGemc",
      "y": "ZxjiWWbZMQGHVWKVQ4hbSIirsVfuecCE6t4jT9F2HZQ"
    }
  }
}
```

Note: The decision which claims to make selectively disclosable is up to the Issuer of the Credential. Considerations can be found in Section 6 and Section 9.7 of [[I-D.ietf-oauth-selective-disclosure-jwt](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-oauth-selective-disclosure-jwt)].
