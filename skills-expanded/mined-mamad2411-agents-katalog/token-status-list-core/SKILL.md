---
name: "token-status-list-core"
description: "Use when understanding Token Status List fundamentals. Covers: introduction, terminology, status list representation (compressed byte array, JSON, CBOR), and status list tokens (JWT, CWT)."
sections:
  - "1. Introduction"
  - "1.1. Example Use Cases"
  - "1.2. Rationale"
  - "1.3. Design Considerations"
  - "1.4. Prior Work"
  - "1.5. Status Mechanisms Registry"
  - "2. Conventions and Definitions"
  - "3. Terminology"
  - "4. Status List"
  - "4.1. Compressed Byte Array"
  - "4.2. Status List in JSON Format"
  - "4.3. Status List in CBOR Format"
  - "5. Status List Token"
  - "5.1. Status List Token in JWT Format"
  - "5.2. Status List Token in CWT Format"
---

<!-- ARF version: draft-10 -->
<!-- Tokens: ~7289 -->

## 1. Introduction
Token formats secured by JOSE [[IANA.JOSE](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#IANA.JOSE)] or COSE [[RFC9052](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC9052)], such as JWTs [[RFC7519](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC7519)], SD-JWT VCs [[SD-JWT.VC](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#SD-JWT.VC)], CWTs [[RFC8392](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC8392)] and ISO mdoc [[ISO.mdoc](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#ISO.mdoc)], have vast possible applications. Some of these applications can involve issuing a token whereby certain semantics about the token or its validity may change over time. Communicating these changes to relying parties in an interoperable manner, such as whether the token is considered invalidated or suspended by its issuer is important for many of these applications.
This document defines a Status List data structure that describes the individual statuses of multiple Referenced Tokens. A Referenced Token may be of any format, but is most commonly a data structures secured by JOSE or COSE. The Referenced Token is referenced by the Status List, which describes the status of the Referenced Token. The statuses of all Referenced Tokens are conveyed via a bit array in the Status List. Each Referenced Token is allocated an index during issuance that represents its position within this bit array. The value of the bit(s) at this index corresponds to the Referenced Token's status. A Status List is provided within a Status List Token protected by cryptographic signature or MAC and this document defines its representations in JWT and CWT format.
The following diagram depicts the relationship between the artifacts:

```
┌────────────────┐  describes status ┌──────────────────┐
│  Status List   ├──────────────────►│ Referenced Token │
│ (JSON or CBOR) │◄──────────────────┤ (JOSE, COSE, ..) │
└─────┬──────────┘    references     └──────────────────┘
      │
      │ embedded in
      ▼
┌───────────────────┐
│ Status List Token │
│  (JWT or CWT)     │
└───────────────────┘
```

An Issuer issues Referenced Tokens to a Holder, the Holder uses and presents those Referenced Tokens to a Relying Party. The Issuer gives updated status information to the Status Issuer, who issues a Status List Token. The Status Issuer can be either the Issuer or an entity that has been authorized by the Issuer to issue Status List Tokens. The Status Issuer provides the Status List Token to the Status Provider, who serves the Status List Token on a public, resolvable endpoint. The Relying Party or the Holder may fetch the Status List Token to retrieve the status of the Referenced Token.
The roles of the Issuer (of the Referenced Token), the Status Issuer and the Status Provider may be fulfilled by the same entity. If not further specified, the term Issuer may refer to an entity acting for all three roles. This document describes how an Issuer references a Status List Token and how a Relying Party fetches and validates Status Lists.
The following diagram depicts the relationship between the involved roles (Relying Party is equivalent to Verifier of [[SD-JWT.VC](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#SD-JWT.VC)]):

```
issue                 present
           Referenced            Referenced
┌────────┐ Token      ┌────────┐ Token      ┌───────────────┐
│ Issuer ├───────────►│ Holder ├───────────►│ Relying Party │
└─┬──────┘            └───┬────┘            └──┬────────────┘
  ▼ update status         │                    │
┌───────────────┐         │                    │
│ Status Issuer │         │                    │
└─┬─────────────┘         │                    │
  ▼ provide Status List   │                    │
┌─────────────────┐       │                    │
│ Status Provider │◄──────┴────────────────────┘
└─────────────────┘     fetch Status List Token
```

Status Lists may be composed to express a range of Status Types. This document defines basic Status Types for the most common use cases as well as an extensibility mechanism for custom Status Types.
Furthermore, the document defines an extension point that enables other specifications to describe additional status mechanisms and creates an IANA registry.


### 1.1. Example Use Cases
An example of the usage of a Status List is to manage the status of issued access tokens as defined in section 1.4 of [[RFC6749](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC6749)]. Token Introspection [[RFC7662](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC7662)] defines another way to determine the status of an issued access token, but it requires the party trying to validate the state of access tokens to directly contact the token issuer, whereas the mechanism defined in this specification does not have this limitation.
Another possible use case for the Status List is to express the status of verifiable credentials (Referenced Tokens) issued by an Issuer in the Issuer-Holder-Verifier model [[SD-JWT.VC](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#SD-JWT.VC)].


### 1.2. Rationale
Revocation mechanisms are an essential part of most identity ecosystems. In the past, revocation of X.509 TLS certificates has been proven difficult. Traditional certificate revocation lists (CRLs) have limited scalability; Online Certificate Status Protocol (OCSP) has additional privacy risks, since the client is leaking the requested website to a third party. OCSP stapling is addressing some of these problems at the cost of less up-to-date data. Modern approaches use accumulator-based revocation registries and Zero-Knowledge-Proofs to accommodate for this privacy gap, but face scalability issues again. Another alternative is short-lived Referenced Tokens with regular re-issuance, but this puts additional burden on the Issuer's infrastructure.
This specification seeks to find a balance between scalability, security and privacy by minimizing the status information to mere bits (often a single bit) and compressing the resulting binary data. Thereby, a Status List may contain statuses of many thousands or millions Referenced Tokens while remaining as small as possible. Placing large amounts of Referenced Tokens into the same list also enables herd privacy relative to the Status Provider.


### 1.3. Design Considerations
The decisions taken in this specification aim to achieve the following design goals:

- 
            the specification shall favor a simple and easy-to-understand concept

          - 
            the specification shall be easy, fast and secure to implement in all major programming languages

          - 
            the specification shall be optimized to support the most common use cases and avoid unnecessary complexity of corner cases

          - 
            the Status List shall scale up to millions of tokens to support large-scale government or enterprise use cases

          - 
            the Status List shall enable caching policies and offline support

          - 
            the specification shall support JSON and CBOR based tokens

          - 
            the specification shall not specify key resolution or trust frameworks

          - 
            the specification shall define an extension point that enables other mechanisms to convey information about the status of a Referenced Token

        


### 1.4. Prior Work
Representing a status with bits in array is a rather old and well-known concept in computer science and there has been prior work to use this for revocation and status management such as a paper by Smith et al. [[smith2020let](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#smith2020let)] that proposed a mechanism called Certificate Revocation Vectors based on xz compressed bit vectors for each expiration day and the W3C bit Status List [[W3C.SL](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#W3C.SL)] that similarly uses a compressed bit representation.


### 1.5. Status Mechanisms Registry
This specification establishes the IANA "Status Mechanisms" registry for status mechanisms and registers the members defined by this specification. Other specifications can register other members used for status retrieval.
Other status mechanisms may have different tradeoffs regarding security, privacy, scalability and complexity. The privacy and security considerations in this document only represent the properties of the Status List mechanism.

---

## 2. Conventions and Definitions
The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED",
"MAY", and "OPTIONAL" in this document are to be interpreted as
described in BCP 14 [[RFC2119](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC2119)] [[RFC8174](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC8174)] when, and only when, they
appear in all capitals, as shown here.

---

## 3. Terminology

        Issuer:
        
          An entity that issues the Referenced Token.

        
Status Issuer:
        
          An entity that issues the Status List Token about the status information of the Referenced Token. This role may be fulfilled by the Issuer.

        
Status Provider:
        
          An entity that provides the Status List Token on a public endpoint. This role may be fulfilled by the Status Issuer.

        
Holder:
        
          An entity that receives Referenced Tokens from the Issuer and presents them to Relying Parties.

        
Relying Party:
        
          An entity that relies on the Referenced Token and fetches the corresponding Status List Token to validate the status of that Referenced Token. Also known as Verifier.

        
Status List:
        
          An object in JSON or CBOR representation containing a compressed byte array that represents the statuses of many Referenced Tokens.

        
Status List Token:
        
          A token in JWT (as defined in [[RFC7519](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC7519)]) or CWT (as defined in [[RFC8392](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC8392)]) representation that contains a cryptographically secured Status List.

        
Referenced Token:
        
          A cryptographically secured data structure that contains a "status" claim that is referencing a mechanism to retrieve status information about this Referenced Token. This document defines the Status List mechanism in which case the Referenced Token contains a reference to an entry in a Status List Token. It is RECOMMENDED to use JSON [[RFC8259](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC8259)] with JOSE as defined in [[RFC7515](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC7515)] or CBOR [[RFC8949](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC8949)] with COSE as defined in [[RFC9052](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC9052)]. Examples for Referenced Tokens are SD-JWT VC and ISO mdoc.

        
base64url:
        
          Denotes the URL-safe base64 encoding without padding as defined in Section 2 of [[RFC7515](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC7515)] as "Base64url Encoding".

---

## 4. Status List
A Status List is a data structure that contains the statuses of many Referenced Tokens represented by one or multiple bits. The [first section](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#status-list-byte-array) ([Section 4.1](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#status-list-byte-array)) describes how to construct a compressed byte array that is the base component for the Status List data structure. The second and third section describe how to encode such a Status List in JSON and CBOR representation.


### 4.1. Compressed Byte Array
A compressed byte array containing the status information of the Referenced Token is composed by the following algorithm:

- 
            The Status Issuer MUST define a number of bits (`bits`) of either 1,2,4 or 8, that represents the amount of bits used to describe the status of each Referenced Token within this Status List. Therefore up to 2,4,16 or 256 statuses for a Referenced Token are possible, depending on the bit size. This limitation is intended to limit bit manipulation necessary to a single byte for every operation and thus keeping implementations simpler and less error-prone.

          - 
            The Status Issuer creates a byte array of size = amount of Referenced Tokens * `bits` / 8 or greater. Depending on the `bits`, each byte in the array corresponds to 8/(`bits`) statuses (8,4,2 or 1).

          - 
            The Status Issuer sets the status values for all Referenced Tokens within the byte array. The status of each Referenced Token is identified using an index that maps to one or more specific bits within the byte array. The index starts counting at 0 and ends with amount of Referenced Tokens - 1 (being the last valid entry). The bits within an array are counted from the least significant bit ("0") to the most significant bit ("7"). All bits of the byte array at a particular index are set to a status value.

          - 
            The Status Issuer compresses the byte array using DEFLATE [[RFC1951](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC1951)] with the ZLIB [[RFC1950](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC1950)] data format. Implementations are RECOMMENDED to use the highest compression level available.

        
The following example illustrates the byte array of a Status List that represents the statuses of 16 Referenced Tokens with a `bits` of 1, requiring 2 bytes (16 bits) for the uncompressed byte array:

```
status[0] = 1
status[1] = 0
status[2] = 0
status[3] = 1
status[4] = 1
status[5] = 1
status[6] = 0
status[7] = 1
status[8] = 1
status[9] = 1
status[10] = 0
status[11] = 0
status[12] = 0
status[13] = 1
status[14] = 0
status[15] = 1
```

These bits are concatenated:

```
byte no            0                  1               2
bit no      7 6 5 4 3 2 1 0    7 6 5 4 3 2 1 0    7
           +-+-+-+-+-+-+-+-+  +-+-+-+-+-+-+-+-+  +-+...
values     |1|0|1|1|1|0|0|1|  |1|0|1|0|0|0|1|1|  |0|...
           +-+-+-+-+-+-+-+-+  +-+-+-+-+-+-+-+-+  +-+...
index       7 6 5 4 3 2 1 0   15   ...  10 9 8   23
           \_______________/  \_______________/
byte value       0xB9               0xA3
```

In the following example, the Status List additionally includes the Status Type "SUSPENDED". As the Status Type value for "SUSPENDED" is 0x02 and does not fit into 1 bit, the `bits` is required to be 2. This example illustrates the byte array of a Status List that represents the statuses of 12 Referenced Tokens with a `bits` of 2, requiring 3 bytes (24 bits) for the uncompressed byte array:

```
status[0] = 1
status[1] = 2
status[2] = 0
status[3] = 3
status[4] = 0
status[5] = 1
status[6] = 0
status[7] = 1
status[8] = 1
status[9] = 2
status[10] = 3
status[11] = 3
```

These bits are concatenated:

```
byte no            0                  1                  2
bit no      7 6 5 4 3 2 1 0    7 6 5 4 3 2 1 0    7 6 5 4 3 2 1 0
           +-+-+-+-+-+-+-+-+  +-+-+-+-+-+-+-+-+  +-+-+-+-+-+-+-+-+
values     |1|1|0|0|1|0|0|1|  |0|1|0|0|0|1|0|0|  |1|1|1|1|1|0|0|1|
           +-+-+-+-+-+-+-+-+  +-+-+-+-+-+-+-+-+  +-+-+-+-+-+-+-+-+
            \ / \ / \ / \ /    \ / \ / \ / \ /    \ / \ / \ / \ /
status       3   0   2   1      1   0   1   0      3   3   2   1
index        3   2   1   0      7   6   5   4      11  10  9   8
             \___________/      \___________/      \___________/
byte value       0xC9               0x44               0xF9
```


### 4.2. Status List in JSON Format
This section defines the data structure for a JSON-encoded Status List:

- 
            `status_list`: REQUIRED. JSON Object that contains a Status List. It MUST contain at least the following claims:

- 
                `bits`: REQUIRED. JSON Integer specifying the number of bits per Referenced Token in the compressed byte array (`lst`). The allowed values for `bits` are 1,2,4 and 8.

              - 
                `lst`: REQUIRED. JSON String that contains the status values for all the Referenced Tokens it conveys statuses for. The value MUST be the base64url-encoded compressed byte array as specified in [Section 4.1](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#status-list-byte-array).

              - 
                `aggregation_uri`: OPTIONAL. JSON String that contains a URI to retrieve the Status List Aggregation for this type of Referenced Token or Issuer. See section [Section 9](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#aggregation) for further details.

            

        
The following example illustrates the JSON representation of the Status List with `bits` 1 from the example above:

```
byte_array = [0xb9, 0xa3]
encoded:
{
  "bits": 1,
  "lst": "eNrbuRgAAhcBXQ"
}
```

The following example illustrates the JSON representation of the Status List with `bits` 2 from the example above:

```
byte_array = [0xc9, 0x44, 0xf9]
encoded:
{
  "bits": 2,
  "lst": "eNo76fITAAPfAgc"
}
```

See section [Appendix "Test vectors for Status List encoding"](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#test-vectors) for more test vectors.


### 4.3. Status List in CBOR Format
This section defines the data structure for a CBOR-encoded Status List:

- 
            The `StatusList` structure is a map (Major Type 5) and defines the following entries:

- 
                `bits`: REQUIRED. Unsigned integer (Major Type 0) that contains the number of bits per Referenced Token in the compressed byte array (`lst`). The allowed values for `bits` are 1, 2, 4 and 8.

              - 
                `lst`: REQUIRED. Byte string (Major Type 2) that contains the status values for all the Referenced Tokens it conveys statuses for. The value MUST be the compressed byte array as specified in [Section 4.1](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#status-list-byte-array).

              - 
                `aggregation_uri`: OPTIONAL. Text string (Major Type 3) that contains a URI to retrieve the Status List Aggregation for this type of Referenced Token. See section [Section 9](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#aggregation) for further detail.

            

        
The following is the CDDL definition of the StatusList structure:

```
StatusList = {
    bits: 1 / 2 / 4 / 8, ; The number of bits used per Referenced Token
    lst: bstr, ; Byte string that contains the Status List
    ? aggregation_uri: tstr, ; link to the Status List Aggregation
}
```

The following example illustrates the CBOR representation of the Status List in Hex:

```
byte_array = [0xb9, 0xa3]
encoded:
a2646269747301636c73744a78dadbb918000217015d
```

The following is the CBOR Annotated Hex output of the example above:

```
a2                              # map(2)
  64                            #   string(4)
    62697473                    #     "bits"
  01                            #   uint(1)
  63                            #   string(3)
    6c7374                      #     "lst"
  4a                            #   bytes(10)
    78dadbb918000217015d        #     "xÚÛ¹\x18\x00\x02\x17\x01]"
```

See section [Appendix "Test vectors for Status List encoding"](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#test-vectors) for more test vectors.

---

## 5. Status List Token
A Status List Token embeds the Status List into a token that is cryptographically signed and protects the integrity of the Status List. This allows for the Status List Token to be hosted by third parties or be transferred for offline use cases.
This section specifies Status List Tokens in JSON Web Token (JWT) and CBOR Web Token (CWT) format.


### 5.1. Status List Token in JWT Format
The Status List Token MUST be encoded as a "JSON Web Token (JWT)" according to [[RFC7519](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC7519)].
The following content applies to the JWT Header:

- 
            `typ`: REQUIRED. The JWT type MUST be `statuslist+jwt`.

        
The following content applies to the JWT Claims Set:

- 
            `sub`: REQUIRED. As generally defined in [[RFC7519](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC7519)]. The `sub` (subject) claim MUST specify the URI of the Status List Token. The value MUST be equal to that of the `uri` claim contained in the `status_list` claim of the Referenced Token.

          - 
            `iat`: REQUIRED. As generally defined in [[RFC7519](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC7519)]. The `iat` (issued at) claim MUST specify the time at which the Status List Token was issued.

          - 
            `exp`: OPTIONAL. As generally defined in [[RFC7519](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC7519)]. The `exp` (expiration time) claim, if present, MUST specify the time at which the Status List Token is considered expired by the Status Issuer.

          - 
            `ttl`: OPTIONAL. The `ttl` (time to live) claim, if present, MUST specify the maximum amount of time, in seconds, that the Status List Token can be cached by a consumer before a fresh copy SHOULD be retrieved. The value of the claim MUST be a positive number encoded in JSON as a number.

          - 
            `status_list`: REQUIRED. The `status_list` (status list) claim MUST specify the Status List conforming to the rules outlined in [Section 4.2](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#status-list-json).

        
The following additional rules apply:

- 
            The JWT MAY contain other claims.

          - 
            The JWT MUST be secured using a cryptographic signature or MAC algorithm. Relying Parties MUST reject JWTs with an invalid signature.

          - 
            Relying Parties MUST reject JWTs that are not valid in all other respects per "JSON Web Token (JWT)" [[RFC7519](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC7519)].

          - 
            Application of additional restrictions and policies are at the discretion of the Relying Party.

        
The following is a non-normative example of a Status List Token in JWT format:

```
{
  "alg": "ES256",
  "kid": "12",
  "typ": "statuslist+jwt"
}
.
{
  "exp": 2291720170,
  "iat": 1686920170,
  "status_list": {
    "bits": 1,
    "lst": "eNrbuRgAAhcBXQ"
  },
  "sub": "https://example.com/statuslists/1",
  "ttl": 43200
}
```


### 5.2. Status List Token in CWT Format
The Status List Token MUST be encoded as a "CBOR Web Token (CWT)" according to [[RFC8392](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC8392)].
The following content applies to the protected header of the CWT:

- 
            `16` (type): REQUIRED. The type of the CWT MUST be `application/statuslist+cwt` or the registered CoAP Content-Format ID (see [Section 14.8](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#coap-content-type)) as defined in [[RFC9596](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC9596)].

        
The following content applies to the CWT Claims Set:

- 
            `2` (subject): REQUIRED. As generally defined in [[RFC8392](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC8392)]. The subject claim MUST specify the URI of the Status List Token. The value MUST be equal to that of the `uri` claim contained in the `status_list` claim of the Referenced Token.

          - 
            `6` (issued at): REQUIRED. As generally defined in [[RFC8392](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC8392)]. The issued at claim MUST specify the time at which the Status List Token was issued.

          - 
            `4` (expiration time): OPTIONAL. As generally defined in [[RFC8392](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC8392)]. The expiration time claim, if present, MUST specify the time at which the Status List Token is considered expired by its issuer.

          - 
            `65534` (time to live): OPTIONAL. Unsigned integer (Major Type 0). The time to live claim, if present, MUST specify the maximum amount of time, in seconds, that the Status List Token can be cached by a consumer before a fresh copy SHOULD be retrieved. The value of the claim MUST be a positive number.

          - 
            `65533` (status list): REQUIRED. The status list claim MUST specify the Status List conforming to the rules outlined in [Section 4.3](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#status-list-cbor).

        
The following additional rules apply:

- 
            The CWT MAY contain other claims.

          - 
            The CWT MUST be secured using a cryptographic signature or MAC algorithm. Relying Parties MUST reject CWTs with an invalid signature.

          - 
            Relying Parties MUST reject CWTs that are not valid in all other respects per "CBOR Web Token (CWT)" [[RFC8392](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC8392)].

          - 
            Application of additional restrictions and policies are at the discretion of the Relying Party.

        
The following is a non-normative example of a Status List Token in CWT format in Hex:

```
d2845820a2012610781a6170706c69636174696f6e2f7374617475736c6973742b63
7774a1044231325850a502782168747470733a2f2f6578616d706c652e636f6d2f73
74617475736c697374732f31061a648c5bea041a8898dfea19fffe19a8c019fffda2
646269747301636c73744a78dadbb918000217015d584027d5535dfe0a33291cc9bf
b41053ad2493c49d1ee4635e12548a79bac92916845fee76799c42762f928441c5c3
44e3612381e0cf88f2f160b3e1f97728ec8403
```

The following is the CBOR Annotated Hex output of the example above:

```
d2                              # tag(18)
  84                            #   array(4)
    58 20                       #     bytes(32)
      a2012610781a6170706c6963  #       "¢\x01&\x10x\x1aapplic"
      6174696f6e2f737461747573  #       "ation/status"
      6c6973742b637774          #       "list+cwt"
    a1                          #     map(1)
      04                        #       uint(4)
      42                        #       bytes(2)
        3132                    #         "12"
    58 50                       #     bytes(80)
      a502782168747470733a2f2f  #       "¥\x02x!https://"
      6578616d706c652e636f6d2f  #       "example.com/"
      7374617475736c697374732f  #       "statuslists/"
      31061a648c5bea041a8898df  #       "1\x06\x1ad\x8c[ê\x04\x1a\x88\x98ß"
      ea19fffe19a8c019fffda264  #       "ê\x19ÿþ\x19¨À\x19ÿý¢d"
      6269747301636c73744a78da  #       "bits\x01clstJxÚ"
      dbb918000217015d          #       "Û¹\x18\x00\x02\x17\x01]"
    58 40                       #     bytes(64)
      27d5535dfe0a33291cc9bfb4  #       "'ÕS]þ\x0a3)\x1cÉ¿´"
      1053ad2493c49d1ee4635e12  #       "\x10S\xad$\x93Ä\x9d\x1eäc^\x12"
      548a79bac92916845fee7679  #       "T\x8ayºÉ)\x16\x84_îvy"
      9c42762f928441c5c344e361  #       "\x9cBv/\x92\x84AÅÃDãa"
      2381e0cf88f2f160b3e1f977  #       "#\x81àÏ\x88òñ`³áùw"
      28ec8403                  #       "(ì\x84\x03"
```
