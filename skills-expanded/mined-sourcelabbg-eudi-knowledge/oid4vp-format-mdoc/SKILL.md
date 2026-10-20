---
name: "oid4vp-format-mdoc"
description: "Use when implementing ISO mdoc (ISO 18013/23220) format in OpenID4VP. Covers: mdoc DeviceResponse, Handover, SessionTranscript computation, and mdoc-specific presentation rules."
sections:
  - "B.2. Mobile Documents or mdocs (ISO/IEC 18013 and ISO/IEC 23220 series)"
  - "B.2.1. Transaction Data"
  - "B.2.2. Metadata"
  - "B.2.3. Parameter in the meta parameter in Credential Query"
  - "B.2.4. Parameter in the Claims Query"
  - "B.2.5. Presentation Response"
  - "B.2.6. Handover and SessionTranscript Definitions"
---

<!-- ARF version: 1.0-final-2025-07-09 -->
<!-- Tokens: ~6384 -->

### B.2. Mobile Documents or mdocs (ISO/IEC 18013 and ISO/IEC 23220 series)
ISO/IEC 18013-5:2021 [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.18013-5)] defines a mobile driving license (mDL) Credential in the mobile document (mdoc) format. Although ISO/IEC 18013-5:2021 [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.18013-5)] is specific to mobile driving licenses (mDLs), the Credential format can be utilized with any type of Credential (or mdoc document types). The ISO/IEC 23220 series has extracted components from ISO/IEC 18013-5:2021 [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.18013-5)] that are common across document types to facilitate the profiling of the specification for other document types. The core data structures are shared between ISO/IEC 18013-5:2021 [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.18013-5)], ISO/IEC 23220-2 [[ISO.23220-2](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.23220-2)], ISO/IEC 23220-4 [[ISO.23220-4](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.23220-4)] which are encoded in CBOR and secured using COSE_Sign1.
The Credential Format Identifier for Credentials in the mdoc format is `mso_mdoc`.


#### B.2.1. Transaction Data
It is RECOMMENDED that each transaction data type defines a data element (`NameSpace`, `DataElementIdentifier`, `DataElementValue`) to be used to return the processed transaction data. Additionally, it is RECOMMENDED that it specifies the processing rules, potentially including any hash function to be applied, and the expected resulting structure.
Some document types support some transaction data ([Section 8.4](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#transaction_data)) to be protected using mdoc authentication, as part of the `DeviceSigned` data structure [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.18013-5)]. In those cases, the specifications of these document types include which transaction data types are supported, and the issuer includes the relevant data elements in the `KeyAuthorizations`. If a Wallet receives a request with a `transaction_data` type whose data element is unauthorized, the Wallet MUST reject the request due to an unsupported transaction data type.


#### B.2.2. Metadata
The `vp_formats_supported` parameter of the Verifier metadata or Wallet metadata MUST have the Credential Format Identifier as a key, and the value MUST be an object consisting of the following name/value pairs:

- 
              `issuerauth_alg_values`: OPTIONAL. A non-empty array containing cryptographic algorithm identifiers. The Credential MUST be considered to fulfill the requirement(s) expressed in this parameter if one of the following is true: 1) The value in the array matches the 'alg' value in the IssuerAuth COSE header. 2) The value in the array is a fully specified algorithm according to [[I-D.ietf-jose-fully-specified-algorithms](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-jose-fully-specified-algorithms)] and the combination of the `alg` value in the `IssuerAuth` COSE header and the curve used by the signing key of the COSE structure matches the combination of the algorithm and curve identified by the fully specified algorithm. As an example, if the `IssuerAuth` structure contains an `alg` header with value `-7` (which stands for ECDSA with SHA-256 in [[IANA.COSE](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#IANA.COSE)]) and is signed by a P-256 key, then it matches an `issuerauth_alg_values` element of `-7` and `-9` (which stands for ECDSA using P-256 curve and SHA-256 in [[I-D.ietf-jose-fully-specified-algorithms](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-jose-fully-specified-algorithms)]).

            - 
              `deviceauth_alg_values`: OPTIONAL. A non-empty array containing cryptographic algorithm identifiers. The Credential MUST be considered to fulfill the requirement(s) expressed in this parameter if one of the following is true: 1) The value in the array matches the 'alg' value in the `DeviceSignature` or `DeviceMac` COSE header. 2) The value in the array is a fully-specified algorithm according to [[I-D.ietf-jose-fully-specified-algorithms](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-jose-fully-specified-algorithms)] and the combination of the `alg` value in the `DeviceSignature` COSE header and the curve used by the signing key of the COSE structure matches the combination of the algorithm and curve identified by the fully-specified algorithm. 3) The `alg` of the `DeviceMac` COSE header is `HMAC 256/256` (as described in Section 9.1.3.5 of [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.18013-5)]) and the curve of the device key (from Table 22 of [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.18013-5)]) matches a value in the array using the identifiers defined in the following table:

          

            
Table 2:
Mapping of curves to `alg` identifiers used for the `HMAC 256/256` case
            

              
                Algorithm Name
                Algorithm Value
              
            
            
              
                HMAC 256/256 using ECDH with Curve P-256
                -65537
              
              
                HMAC 256/256 using ECDH with Curve P-384
                -65538
              
              
                HMAC 256/256 using ECDH with Curve P-521
                -65539
              
              
                HMAC 256/256 using ECDH with X25519
                -65540
              
              
                HMAC 256/256 using ECDH with X448
                -65541
              
              
                HMAC 256/256 using ECDH with brainpoolP256r1
                -65542
              
              
                HMAC 256/256 using ECDH with brainpoolP320r1
                -65543
              
              
                HMAC 256/256 using ECDH with brainpoolP384r1
                -65544
              
              
                HMAC 256/256 using ECDH with brainpoolP512r1
                -65545
              
            
          
Note: These are specified in OpenID4VP only for private use in this parameter in this specification, and might be superseded by a future registration in IANA.
For clarity, the following is a couple of non-normative examples of the `deviceauth_alg_values` parameter
The example below indicates the verifier supports DeviceMac with HMAC 256/256, where the MAC key is established via ECDH using keys on the P-256 curve as per Section 9.1.3.5 of [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.18013-5)].

```
{
  "deviceauth_alg_values": [ -65537 ]
}
```

The example below indicates the verifier supports DeviceMac with HMAC 256/256, where the MAC key is established via ECDH using keys on the P-256 curve as per Section 9.1.3.5 of [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.18013-5)], and DeviceSignature using ECDSA with the P-256 curve.

```
{
  "deviceauth_alg_values": [ -65537, -9 ]
}
```

The following is a non-normative example of `client_metadata` request parameter value in a request to present an ISO/IEC 18013-5 mDOC.

```
{
  "vp_formats_supported": {
    "mso_mdoc": {
      "issuerauth_alg_values": [-9, -50],

      "deviceauth_alg_values": [-9, -50]
    }
  }
}
```


#### B.2.3. Parameter in the meta parameter in Credential Query
The following is an ISO mdoc specific parameter in the `meta` parameter in a Credential Query as defined in [Section 6.1](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#credential_query).

            
`doctype_value`:
            REQUIRED. String that specifies an allowed value for the
doctype of the requested Verifiable Credential. It MUST
be a valid doctype identifier as defined in [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.18013-5)].

          


#### B.2.4. Parameter in the Claims Query
The following are ISO mdoc specific parameters to be used in a Claims Query as defined in [Section 6.3](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#claims_query).

            `intent_to_retain`
            OPTIONAL. A boolean that is equivalent to `IntentToRetain` variable defined in Section 8.3.2.1.2.1 of [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.18013-5)].

          


#### B.2.5. Presentation Response
An example DCQL query using the mdoc format is shown in [Appendix D](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#more_dcql_query_examples). The following is a non-normative example for a VP Token in the response:

```
{
  "my_credential": ["<base64url-encoded DeviceResponse>"]
}
```

The VP Token contains the base64url-encoded `DeviceResponse` CBOR structure as defined in ISO/IEC 18013-5 [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.18013-5)] or ISO/IEC 23220-4 [[ISO.23220-4](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.23220-4)]. Essentially, the `DeviceResponse` CBOR structure contains a signature or MAC over the `SessionTranscript` CBOR structure including the OpenID4VP-specific `Handover` CBOR structure.


#### B.2.6. Handover and SessionTranscript Definitions


##### B.2.6.1. Invocation via Redirects
If the presentation request is invoked using redirects, the `SessionTranscript` CBOR structure as defined in Section 9.1.5.1 in [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.18013-5)] MUST be used with the following changes:

- 
                `DeviceEngagementBytes` MUST be `null`.

              - 
                `EReaderKeyBytes` MUST be `null`.

              - 
                `Handover` MUST be the `OpenID4VPHandover` CBOR structure as defined below.

            

```
OpenID4VPHandover = [
  "OpenID4VPHandover", ; A fixed identifier for this handover type
  OpenID4VPHandoverInfoHash ; A cryptographic hash of OpenID4VPHandoverInfo
]

; Contains the sha-256 hash of OpenID4VPHandoverInfoBytes
OpenID4VPHandoverInfoHash = bstr

; Contains the bytes of OpenID4VPHandoverInfo encoded as CBOR
OpenID4VPHandoverInfoBytes = bstr .cbor OpenID4VPHandoverInfo

OpenID4VPHandoverInfo = [
  clientId,
  nonce,
  jwkThumbprint,
  responseUri
] ; Array containing handover parameters

clientId = tstr

nonce = tstr

jwkThumbprint = bstr

responseUri = tstr
```

The `OpenID4VPHandover` structure has the following elements:

- The first element MUST be the string `OpenID4VPHandover`. This serves as a unique identifier for the handover structure to prevent misinterpretation or confusion.

              - The second element MUST be a Byte String which contains the sha-256 hash of the bytes of `OpenID4VPHandoverInfo` when encoded as CBOR.

              - 
                The `OpenID4VPHandoverInfo` has the following elements:

- The first element MUST be the `client_id` request parameter. If applicable, this includes the Client Identifier Prefix.

                  - The second element MUST be the value of the `nonce` request parameter.

                  - If the response is encrypted, e.g., using `direct_post.jwt`, the third element MUST be the JWK SHA-256 Thumbprint as defined in [[RFC7638](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC7638)], encoded as a Byte String, of the Verifier's public key used to encrypt the response. Otherwise, the third element MUST be `null`. See [Appendix B.2.6.2](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#session_transcript_dc_api) for an explanation of why this is important.

                  - The fourth element MUST be either the `redirect_uri` or `response_uri` request parameter, depending on which is present, as determined by the Response Mode.

                

            
Unless otherwise stated, the values of `client_id`, `nonce`, `redirect_uri`, and `response_uri` request parameters referenced above MUST be obtained from the Authorization Request query parameters if the request is unsigned, or from the signed Request Object if the request is signed.
The following is a non-normative example of the input JWK for calculating the JWK Thumbprint in the context of `OpenID4VPHandoverInfo`:

```
{
  "kty": "EC",
  "crv": "P-256",
  "x": "DxiH5Q4Yx3UrukE2lWCErq8N8bqC9CHLLrAwLz5BmE0",
  "y": "XtLM4-3h5o3HUH0MHVJV0kyq0iBlrBwlh8qEDMZ4-Pc",
  "use": "enc",
  "alg": "ECDH-ES",
  "kid": "1"
}
```

The following is a non-normative example of the `OpenID4VPHandoverInfo` structure:

```
Hex:

847818783530395f73616e5f646e733a6578616d706c652e636f6d782b6578633767
426b786a7831726463397564527276654b7653734a4971383061766c58654c486847
7771744158204283ec927ae0f208daaa2d026a814f2b22dca52cf85ffa8f3f8626c6
bd669047781c68747470733a2f2f6578616d706c652e636f6d2f726573706f6e7365

CBOR diagnostic:

84                                 # array(4)
  78 18                            #   string(24)
    783530395f73616e5f646e733a6578 #     "x509_san_dns:ex"
    616d706c652e636f6d             #     "ample.com"
  78 2b                            #   string(43)
    6578633767426b786a783172646339 #     "exc7gBkxjx1rdc9"
    7564527276654b7653734a49713830 #     "udRrveKvSsJIq80"
    61766c58654c48684777717441     #     "avlXeLHhGwqtA"
  58 20                            #   bytes(32)
    4283ec927ae0f208daaa2d026a814f #     "B\x83ì\x92zàò\x08Úª-\x02j\x81O"
    2b22dca52cf85ffa8f3f8626c6bd66 #     "+"Ü¥,ø_ú\x8f?\x86&Æ½f"
    9047                           #     "\x90G"
  78 1c                            #   string(28)
    68747470733a2f2f6578616d706c65 #     "https://example"
    2e636f6d2f726573706f6e7365     #     ".com/response"
```

The following is a non-normative example of the `OpenID4VPHandover` structure:

```
Hex:

82714f70656e494434565048616e646f7665725820048bc053c00442af9b8eed494c
efdd9d95240d254b046b11b68013722aad38ac

CBOR diagnostic:

82                                 # array(2)
  71                               #   string(17)
    4f70656e494434565048616e646f76 #     "OpenID4VPHandov"
    6572                           #     "er"
  58 20                            #   bytes(32)
    048bc053c00442af9b8eed494cefdd #     "\x04\x8bÀSÀ\x04B¯\x9b\x8eíILïÝ"
    9d95240d254b046b11b68013722aad #     "\x9d\x95$\x0d%K\x04k\x11¶\x80\x13r*­"
    38ac                           #     "8¬"
```

The following is a non-normative example of the `SessionTranscript` structure:

```
Hex:

83f6f682714f70656e494434565048616e646f7665725820048bc053c00442af9b8e
ed494cefdd9d95240d254b046b11b68013722aad38ac

CBOR diagnostic:

83                                 # array(3)
  f6                               #   null
  f6                               #   null
  82                               #   array(2)
    71                             #     string(17)
      4f70656e494434565048616e646f #       "OpenID4VPHando"
      766572                       #       "ver"
    58 20                          #     bytes(32)
      048bc053c00442af9b8eed494cef #       "\x04\x8bÀSÀ\x04B¯\x9b\x8eíILï"
      dd9d95240d254b046b11b6801372 #       "Ý\x9d\x95$\x0d%K\x04k\x11¶\x80\x13r"
      2aad38ac                     #       "*­8¬"
```


##### B.2.6.2. Invocation via the Digital Credentials API
If the presentation request is invoked using the Digital Credentials API, the `SessionTranscript` CBOR structure as defined in Section 9.1.5.1 in [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.18013-5)] MUST be used with the following changes:

- 
                `DeviceEngagementBytes` MUST be `null`.

              - 
                `EReaderKeyBytes` MUST be `null`.

              - 
                `Handover` MUST be the `OpenID4VPDCAPIHandover` CBOR structure as defined below.

            
Note: The following section contains a definition in Concise Data Definition Language (CDDL), a language used to define data structures - see [[RFC8610](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC8610)] for more details. `bstr` refers to Byte String, defined as major type 2 in CBOR and `tstr` refers to Text String, defined as major type 3 in CBOR (encoded in utf-8) as defined in section 3.1 of [[RFC8949](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC8949)].

```
OpenID4VPDCAPIHandover = [
  "OpenID4VPDCAPIHandover", ; A fixed identifier for this handover type
  OpenID4VPDCAPIHandoverInfoHash ; A cryptographic hash of OpenID4VPDCAPIHandoverInfo
]

; Contains the sha-256 hash of OpenID4VPDCAPIHandoverInfoBytes
OpenID4VPDCAPIHandoverInfoHash = bstr

; Contains the bytes of OpenID4VPDCAPIHandoverInfo encoded as CBOR
OpenID4VPDCAPIHandoverInfoBytes = bstr .cbor OpenID4VPDCAPIHandoverInfo

OpenID4VPDCAPIHandoverInfo = [
  origin,
  nonce,
  jwkThumbprint
] ; Array containing handover parameters

origin = tstr

nonce = tstr

jwkThumbprint = bstr
```

The `OpenID4VPDCAPIHandover` structure has the following elements:

- The first element MUST be the string `OpenID4VPDCAPIHandover`. This serves as a unique identifier for the handover structure to prevent misinterpretation or confusion.

              - The second element MUST be a Byte String which contains the sha-256 hash of the bytes of `OpenID4VPDCAPIHandoverInfo` when encoded as CBOR.

              - 
                The `OpenID4VPDCAPIHandoverInfo` has the following elements:

- The first element MUST be the string representing the Origin of the request as described in [Appendix A.2](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#dc_api_request). It MUST NOT be prefixed with `origin:`.

                  - The second element MUST be the value of the `nonce` request parameter.

                  - For the Response Mode `dc_api.jwt`, the third element MUST be the JWK SHA-256 Thumbprint as defined in [[RFC7638](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC7638)], encoded as a Byte String, of the Verifier's public key used to encrypt the response. If the Response Mode is `dc_api`, the third element MUST be `null`. For unsigned requests, including the JWK Thumbprint in the `SessionTranscript` allows the Verifier to detect whether the response was re-encrypted by a third party, potentially leading to the leakage of sensitive information. While this does not prevent such an attack, it makes it detectable and helps preserve the confidentiality of the response.

                

            
The following is a non-normative example of the input JWK for calculating the JWK Thumbprint in the context of `OpenID4VPDCAPIHandoverInfo`:

```
{
  "kty": "EC",
  "crv": "P-256",
  "x": "DxiH5Q4Yx3UrukE2lWCErq8N8bqC9CHLLrAwLz5BmE0",
  "y": "XtLM4-3h5o3HUH0MHVJV0kyq0iBlrBwlh8qEDMZ4-Pc",
  "use": "enc",
  "alg": "ECDH-ES",
  "kid": "1"
}
```

The following is a non-normative example of the `OpenID4VPDCAPIHandoverInfo` structure:

```
Hex:

837368747470733a2f2f6578616d706c652e636f6d782b6578633767426b786a7831
726463397564527276654b7653734a4971383061766c58654c486847777174415820
4283ec927ae0f208daaa2d026a814f2b22dca52cf85ffa8f3f8626c6bd669047

CBOR diagnostic:

83                                 # array(3)
  73                               #   string(19)
    68747470733a2f2f6578616d706c65 #     "https://example"
    2e636f6d                       #     ".com"
  78 2b                            #   string(43)
    6578633767426b786a783172646339 #     "exc7gBkxjx1rdc9"
    7564527276654b7653734a49713830 #     "udRrveKvSsJIq80"
    61766c58654c48684777717441     #     "avlXeLHhGwqtA"
  58 20                            #   bytes(32)
    4283ec927ae0f208daaa2d026a814f #     "B\x83ì\x92zàò\x08Úª-\x02j\x81O"
    2b22dca52cf85ffa8f3f8626c6bd66 #     "+"Ü¥,ø_ú\x8f?\x86&Æ½f"
    9047                           #     "\x90G"
```

The following is a non-normative example of the `OpenID4VPDCAPIHandover` structure:

```
Hex:

82764f70656e4944345650444341504948616e646f7665725820fbece366f4212f97
62c74cfdbf83b8c69e371d5d68cea09cb4c48ca6daab761a

CBOR diagnostic:

82                                 # array(2)
  76                               #   string(22)
    4f70656e4944345650444341504948 #     "OpenID4VPDCAPIH"
    616e646f766572                 #     "andover"
  58 20                            #   bytes(32)
    fbece366f4212f9762c74cfdbf83b8 #     "ûìãfô!/\x97bÇLý¿\x83¸"
    c69e371d5d68cea09cb4c48ca6daab #     "Æ\x9e7\x1d]hÎ\xa0\x9c´Ä\x8c¦Ú«"
    761a                           #     "v\x1a"
```

The following is a non-normative example of the `SessionTranscript` structure:

```
Hex:

83f6f682764f70656e4944345650444341504948616e646f7665725820fbece366f4
212f9762c74cfdbf83b8c69e371d5d68cea09cb4c48ca6daab761a

CBOR diagnostic:

83                                 # array(3)
  f6                               #   null
  f6                               #   null
  82                               #   array(2)
    76                             #     string(22)
      4f70656e49443456504443415049 #       "OpenID4VPDCAPI"
      48616e646f766572             #       "Handover"
    58 20                          #     bytes(32)
      fbece366f4212f9762c74cfdbf83 #       "ûìãfô!/\x97bÇLý¿\x83"
      b8c69e371d5d68cea09cb4c48ca6 #       "¸Æ\x9e7\x1d]hÎ\xa0\x9c´Ä\x8c¦"
      daab761a                     #       "Ú«v\x1a"
```
