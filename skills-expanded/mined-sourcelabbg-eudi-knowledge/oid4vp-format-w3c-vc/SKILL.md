---
name: "oid4vp-format-w3c-vc"
description: "Use when implementing W3C Verifiable Credentials format in OpenID4VP. Covers: W3C VC format params, claims matching, presentation response structure, and transaction data for W3C VCs."
sections:
  - "B.1. W3C Verifiable Credentials"
  - "B.1.1. Parameters in the meta parameter in Credential Query"
  - "B.1.2. Claims Matching"
  - "B.1.3. Formats and Examples"
---

<!-- ARF version: 1.0-final-2025-07-09 -->
<!-- Tokens: ~3966 -->

### B.1. W3C Verifiable Credentials
The following sections define the Credential Format specific parameters and rules for W3C Verifiable Credentials compliant to the [[VC_DATA](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#VC_DATA)] specification and for W3C Verifiable Presentations of such Credentials.
If `require_cryptographic_holder_binding` is set to `true` in the Credential Query, the Wallet MUST return a Verifiable Presentation of a Verifiable Credential. Otherwise, a Verifiable Credential without Holder Binding MUST be returned.


#### B.1.1. Parameters in the meta parameter in Credential Query
The following is a W3C Verifiable Credentials specific parameter in the `meta` parameter in a Credential Query as defined in [Section 6.1](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#credential_query):

            
`type_values`:
            REQUIRED. A non-empty array of string arrays. The value of each element in the `type_values` array is a non-empty array specifying the fully expanded types (IRIs) that the Verifier accepts in a Presentation, after applying the `@context` to the Verifiable Credential. If a `type` value in a Verifiable Credential is not defined in any `@context`, it remains unchanged, i.e., remains a relative IRI after JSON-LD processing. For this reason, JSON-LD processing MAY be skipped in such cases and the relative IRI is considered to be the fully expanded type, as applying the `@context` would not alter the value. Implementations MAY use alternative mechanisms to obtain the fully expanded types, as long as the results are equivalent to those produced by JSON-LD processing. Each of the top-level arrays specifies one alternative to match the fully expanded `type` values of the Verifiable Credential against. Each inner array specifies a set of fully expanded types that MUST be present in the fully expanded types in the `type` property of the Verifiable Credential, regardless of order or the presence of additional types.

          

The following is a non-normative example of `type_values` within a DCQL query:

```
"type_values":[
  [
      "https://www.w3.org/2018/credentials#VerifiableCredential",
      "https://example.org/examples#AlumniCredential",
      "https://example.org/examples#BachelorDegree"
  ],
  [
      "https://www.w3.org/2018/credentials#VerifiableCredential",
      "https://example.org/examples#UniversityDegreeCredential"
  ],
  [
      "IdentityCredential"
  ]
]
```

The following is a non-normative example of a W3C Verifiable Credential that would match the `type_values` DCQL query above (other claims omitted for readability):

```
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "https://www.w3.org/2018/credentials/examples/v1"
  ],
  "type": ["VerifiableCredential", "UniversityDegreeCredential"]
}
```

The following is another non-normative example of a W3C Verifiable Credential that would match the `type_values` DCQL query above (other claims omitted for readability):

```
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "https://www.w3.org/2018/credentials/examples/v1"
  ],
  "type": ["VerifiableCredential", "BachelorDegree", "AlumniCredential"]
}
```

The following is another non-normative example of a W3C Verifiable Credential that would match the `type_values` DCQL query above (other claims omitted for readability):

```
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1"
  ],
  "type": ["VerifiableCredential", "IdentityCredential"]
}
```


#### B.1.2. Claims Matching
The `claims_path` parameter in the Credential Query as defined in [Section 6.1](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#credential_query) is used to specify the claims that the Verifier wants to receive in the Presentation. When used in the context of W3C Verifiable Credentials, the `claims_path` parameter always matches on the root of Verifiable Credential (not the Verifiable Presentation). Examples are shown in the following subsections.


#### B.1.3. Formats and Examples


##### B.1.3.1. VC signed as a JWT, not using JSON-LD
This section illustrates the presentation of a Credential conformant to [[VC_DATA](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#VC_DATA)] that is signed using JWS, and does not use JSON-LD.


###### B.1.3.1.1. Format Identifier and Cipher Suites
The Credential Format Identifier is `jwt_vc_json` to request a W3C Verifiable Credential compliant to the [[VC_DATA](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#VC_DATA)] specification or a Verifiable Presentation of such a Credential.
Cipher suites should use algorithm names defined in [IANA JOSE Algorithms Registry](https://www.iana.org/assignments/jose/jose.xhtml#web-signature-encryption-algorithms).


###### B.1.3.1.2. Example Credential
The following is a non-normative example of the payload of a JWT-based W3C Verifiable Credential that will be used throughout this section:

```
{
  "iss": "https://example.gov/issuers/565049",
  "nbf": 1262304000,
  "jti": "http://example.gov/credentials/3732",
  "sub": "did:example:ebfeb1f712ebc6f1c276e12ec21",
  "vc": {
    "@context": [
      "https://www.w3.org/2018/credentials/v1",
      "https://www.w3.org/2018/credentials/examples/v1"
    ],
    "type": [
      "VerifiableCredential",
      "IDCredential"
    ],
    "credentialSubject": {
      "given_name": "Max",
      "family_name": "Mustermann",
      "birthdate": "1998-01-11",
      "address": {
        "street_address": "Sandanger 25",
        "locality": "Musterstadt",
        "postal_code": "123456",
        "country": "DE"
      }
    }
  }
}
```


###### B.1.3.1.3. Metadata
The `vp_formats_supported` parameter of the Verifier metadata or Wallet metadata MUST have the Credential Format Identifier as a key, and the value MUST be an object consisting of the following name/value pair:

- 
                  `alg_values`: OPTIONAL. A non-empty array containing identifiers of cryptographic algorithms supported for a JWT-secured W3C Verifiable Credential or W3C Verifiable Presentation. If present, the `alg` JOSE header (as defined in [[RFC7515](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC7515)]) of the presented Verifiable Credential or Verifiable Presentation MUST match one of the array values.

              
The following is a non-normative example of `client_metadata` request parameter value in a request to present an W3C Verifiable Presentation.

```
{
  "vp_formats_supported": {
    "jwt_vc_json": {
      "alg_values": ["ES256", "ES384"]
    }
  }
}
```


###### B.1.3.1.4. Presentation Request
The requirements regarding the Credential to be presented are conveyed in the `dcql_query` parameter.
The following is a non-normative example of the contents of this parameter:

```
{
  "credentials": [
    {
      "id": "example_jwt_vc",
      "format": "jwt_vc_json",
      "meta": {
        "type_values": [["IDCredential"]]
      },
      "claims": [
        {"path": ["credentialSubject", "family_name"]},
        {"path": ["credentialSubject", "given_name"]}
      ]
    }
  ]
}
```


###### B.1.3.1.5. Presentation Response
The following requirements apply to the `nonce` and `aud` claims of the Verifiable Presentation:

- the `nonce` claim MUST be the value of `nonce` from the Authorization Request;

                - the `aud` claim MUST be the value of the Client Identifier, except for requests over the DC API where it MUST be the Origin prefixed with `origin:`, as described in [Appendix A.4](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#dc_api_response).

              
The following is a non-normative example of the VP Token provided in the response (shortened for presentation):

```
{
  "example_jwt_vc": ["eY...QMA"]
}
```

The following is a non-normative example of the payload of the Verifiable Presentation in the VP Token in the last example:

```
{
  "iss": "did:example:ebfeb1f712ebc6f1c276e12ec21",
  "jti": "urn:uuid:3978344f-8596-4c3a-a978-8fcaba3903c5",
  "aud": "x509_san_dns:client.example.org",
  "nbf": 1541493724,
  "iat": 1541493724,
  "exp": 1573029723,
  "nonce": "n-0S6_WzA2Mj",
  "vp": {
    "@context": [
      "https://www.w3.org/2018/credentials/v1"
    ],
    "type": [
      "VerifiablePresentation"
    ],
    "verifiableCredential": [
      "eyJhb...ssw5c"
    ]
  }
}
```


##### B.1.3.2. LDP VCs
This section illustrates presentation of a Credential conformant to [[VC_DATA](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#VC_DATA)] that is secured using Data Integrity, using JSON-LD.


###### B.1.3.2.1. Format Identifier and Cipher Suites
The Credential Format Identifier is `ldp_vc` to request a W3C Verifiable Credential compliant to the [[VC_DATA](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#VC_DATA)] specification or a Verifiable Presentation of such a Credential.
Cipher suites should use Data Integrity compatible securing mechanisms defined in [Verifiable Credential Extensions](https://www.w3.org/TR/vc-extensions/#securing-mechanisms).


###### B.1.3.2.2. Example Credential
The following is a non-normative example of the payload of a Verifiable Credential that will be used throughout this section:

```
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "https://www.w3.org/2018/credentials/examples/v1",
    "https://w3id.org/security/data-integrity/v2"
  ],
  "id": "https://example.com/credentials/1872",
  "type": [
    "VerifiableCredential",
    "IDCredential"
  ],
  "issuer": {
    "id": "did:example:issuer"
  },
  "issuanceDate": "2025-03-19T00:00:00Z",
  "credentialSubject": {
    "given_name": "Max",
    "family_name": "Mustermann",
    "birthdate": "1998-01-11",
    "address": {
      "street_address": "Sandanger 25",
      "locality": "Musterstadt",
      "postal_code": "123456",
      "country": "DE"
    }
  },
  "proof": {
    "type": "DataIntegrityProof",
    "cryptosuite": "eddsa-rdfc-2022",
    "created": "2025-03-19T15:30:15Z",
    "proofValue": "z5C5b...EtszK",
    "proofPurpose": "assertionMethod",
    "verificationMethod": "did:example:issuer#keys-1"
  }
}
```


###### B.1.3.2.3. Metadata
The `vp_formats_supported` parameter of the Verifier metadata or Wallet metadata MUST have the Credential Format Identifier as a key, and the value MUST be an object consisting of the following name/value pairs:

- 
                  `proof_type_values`: OPTIONAL. A non-empty array containing identifiers of proof types supported for a Data Integrity secured W3C Verifiable Presentation or W3C Verifiable Credential. If present, the proof `type` parameter (as defined in [[VC_DATA](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#VC_DATA)]) of the presented Verifiable Credential or Verifiable Presentation MUST match one of the array values.

                - 
                  `cryptosuite_values`: OPTIONAL. A non-empty array containing identifiers of crypto suites supported with one of the algorithms listed in `proof_type_values` for a Data Integrity secured W3C Verifiable Presentation or W3C Verifiable Credential. Note that `cryptosuite_values` MAY be used if one of the algorithms in `proof_type_values` supports multiple crypto suites. If present, the proof `cryptosuite` parameter (as defined in [[VC_DATA_INTEGRITY](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#VC_DATA_INTEGRITY)]) of the presented Verifiable Credential or Verifiable Presentation MUST match one of the array values.

              
The following is a non-normative example of `client_metadata` request parameter value in a request to present an W3C Verifiable Presentation.

```
{
  "vp_formats_supported": {
    "ldp_vc": {
      "proof_type_values": [
        "DataIntegrityProof",
        "Ed25519Signature2020"
      ],
      "cryptosuite_values": [
        "ecdsa-rdfc-2019",
        "ecdsa-sd-2023",
        "ecdsa-jcs-2019",
        "bbs-2023"
      ]
    }
  }
}
```


###### B.1.3.2.4. Presentation Request
The requirements regarding the Credential to be presented are conveyed in the `dcql_query` parameter.
The following is a non-normative example of the contents of this parameter:

```
{
  "credentials": [
    {
      "id": "example_ldp_vc",
      "format": "ldp_vc",
      "meta": {
        "type_values": [["IDCredential"]]
      },
      "claims": [
        {"path": ["credentialSubject", "family_name"]},
        {"path": ["credentialSubject", "given_name"]},
        {"path": ["credentialSubject", "birthdate"]},
        {"path": ["credentialSubject", "address", "street_address"]},
        {"path": ["credentialSubject", "address", "locality"]},
        {"path": ["credentialSubject", "address", "postal_code"]},
        {"path": ["credentialSubject", "address", "country"]}
      ]
    }
  ]
}
```


###### B.1.3.2.5. Presentation Response
The following requirements apply to the `challenge` and `domain` claims within the `proof` object in the Verifiable Presentation:

- the `challenge` claim MUST be the value of `nonce` from the Authorization Request;

                - the `domain` claim MUST be the value of the Client Identifier, except for requests over the DC API where it MUST be the Origin prefixed with `origin:`, as described in [Appendix A.4](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#dc_api_response).

              
The following is a non-normative example of the Verifiable Presentation in the `vp_token` parameter:

```
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "https://w3id.org/security/data-integrity/v2"
  ],
  "type": [
    "VerifiablePresentation"
  ],
  "verifiableCredential": [
    {
      "@context": [
        "https://www.w3.org/2018/credentials/v1",
        "https://www.w3.org/2018/credentials/examples/v1",
        "https://w3id.org/security/data-integrity/v2"
      ],
      "id": "https://example.com/credentials/1872",
      "type": [
        "VerifiableCredential",
        "IDCredential"
      ],
      "issuer": {
        "id": "did:example:issuer"
      },
      "issuanceDate": "2025-03-19T00:00:00Z",
      "credentialSubject": {
        "given_name": "Max",
        "family_name": "Mustermann",
        "birthdate": "1998-01-11",
        "address": {
          "street_address": "Sandanger 25",
          "locality": "Musterstadt",
          "postal_code": "123456",
          "country": "DE"
        }
      },
      "proof": {
        "type": "DataIntegrityProof",
        "cryptosuite": "eddsa-rdfc-2022",
        "created": "2025-03-19T15:30:15Z",
        "proofValue": "z5C5b...EtszK",
        "proofPurpose": "assertionMethod",
        "verificationMethod": "did:example:issuer#keys-1"
      }
    }
  ],
  "id": "ebc6f1c2",
  "holder": "did:example:holder",
  "proof": {
    "type": "DataIntegrityProof",
    "cryptosuite": "eddsa-rdfc-2022",
    "created": "2025-04-04T10:12:15Z",
    "challenge": "n-0S6_WzA2Mj",
    "domain": "x509_san_dns:client.example.org",
    "proofValue": "z5s8c...AD3a9d",
    "proofPurpose": "authentication",
    "verificationMethod": "did:example:holder#key-1"
  }
}
```
