---
name: "w3c-vcdm-status-schemas-securing"
description: "Use when implementing status, schema, and securing features in W3C VCDM. Covers: status information, data schemas, and securing mechanisms."
sections:
  - "4.10 Status"
  - "4.11 Data Schemas"
  - "4.12 Securing Mechanisms"
---

<!-- ARF version: 2.0-2024-12-04 -->
<!-- Tokens: ~5303 -->

### 4.10 Status
        

        
This specification defines the
credentialStatus [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) for
discovering information related to the status of a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential), such as whether it is suspended or revoked.
        

        
If present, the value associated with the `credentialStatus` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) is a
single object or a set of one or more objects. The following [properties](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property)
are defined for every object:
        

        
          id
          
The `id` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) is OPTIONAL. It MAY be used to provide a
unique identifier for the credential status object. If present, the
normative guidance in Section [4.4 Identifiers](https://www.w3.org/TR/vc-data-model-2.0/#identifiers) MUST be followed.
          
          type
          
The `type` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) is REQUIRED. It is used to express the
type of status information expressed by the object. The related normative
guidance in Section [4.5 Types](https://www.w3.org/TR/vc-data-model-2.0/#types) MUST be followed.
          
        

        
The precise content of the [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) status information is determined by
the specific `credentialStatus` [type](https://www.w3.org/TR/vc-data-model-2.0/#dfn-type) definition and varies
depending on factors such as whether it is simple to implement or if it is
privacy-enhancing. The value will provide enough information to determine the
current status of the [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) and whether machine-readable information will
be retrievable from the URL. For example, the object could contain a link to an
external document that notes whether the [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) is suspended or revoked.
        

        
        
    [Example 12](https://www.w3.org/TR/vc-data-model-2.0/#example-use-of-the-status-property): Use of the status property
   ```
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://www.w3.org/ns/credentials/examples/v2"
  ],
  "id": "http://university.example/credentials/3732",
  "type": ["VerifiableCredential", "ExampleDegreeCredential"],
  "issuer": "https://university.example/issuers/14",
  "validFrom": "2010-01-01T19:23:24Z",
  "credentialSubject": {
    "id": "did:example:ebfeb1f712ebc6f1c276e12ec21",
    "degree": {
      "type": "ExampleBachelorDegree",
      "name": "Bachelor of Science and Arts"
    }
  },
  "credentialStatus": {
    "id": "https://university.example/credentials/status/3#94567",
    "type": "BitstringStatusListEntry",
    "statusPurpose": "revocation",
    "statusListIndex": "94567",
    "statusListCredential": "https://university.example/credentials/status/3"
  }
}
```
      

        
A [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) can have more than one status associated
with it, such as whether it has been revoked or suspended.
        

        
        
    [Example 13](https://www.w3.org/TR/vc-data-model-2.0/#example-use-of-multiple-entries-for-the-status-property): Use of multiple entries for the status property
   ```
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://www.w3.org/ns/credentials/examples/v2"
  ],
  "id": "http://license.example/credentials/9837",
  "type": ["VerifiableCredential", "ExampleDrivingLicenseCredential"],
  "issuer": "https://license.example/issuers/48",
  "validFrom": "2020-03-14T12:10:42Z",
  "credentialSubject": {
    "id": "did:example:f1c276e12ec21ebfeb1f712ebc6",
    "license": {
      "type": "ExampleDrivingLicense",
      "name": "License to Drive a Car"
    }
  },
  "credentialStatus": [{
    "id": "https://license.example/credentials/status/84#14278",
    "type": "BitstringStatusListEntry",
    "statusPurpose": "revocation",
    "statusListIndex": "14278",
    "statusListCredential": "https://license.example/credentials/status/84"
  }, {
    "id": "https://license.example/credentials/status/84#82938",
    "type": "BitstringStatusListEntry",
    "statusPurpose": "suspension",
    "statusListIndex": "82938",
    "statusListCredential": "https://license.example/credentials/status/84"
  }]
}
```
      

        
Implementers are cautioned that [credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) with multiple status entries
might contain conflicting information. Reconciling such conflicts is a part of
the [validation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claim-validation) process, hence part of the verifier's business logic, and
therefore out of scope for this specification.
        

        
Defining the data model, formats, and protocols for status schemes is out of the
scope of this specification. The [Verifiable Credential Extensions](https://w3c.github.io/vc-extensions/) document contains
available status schemes for implementers who want to implement [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) status checking.
        

        
Credential status specifications MUST NOT enable tracking of individuals, such
as an [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) being notified (either directly or indirectly) when a
[verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) is interested in a specific [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) or [subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects). Unacceptable
approaches include "phoning home," such that every use of a credential contacts
the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) of the credential to check the status for a specific individual,
or "pseudonymity reduction," such that every use of the credential causes a
request for information from the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) that the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) can use
to deduce [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) interest in a specific individual.

---

### 4.11 Data Schemas
        

        
Data schemas are useful when enforcing a specific structure on a given
data collection. There are at least two types of data schemas that this
specification considers:
        

        
          - 
Data verification schemas, which are used to establish that the structure
and contents of a [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) or [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) conform to a
published schema.
          
          - 
Data encoding schemas, which are used to map the contents of a
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) to an alternative representation format, such as a
format used in a zero-knowledge proof.
          
        

        
It is important to understand that data schemas serve a different purpose from
the `@context` property, which neither enforces data structure or
data syntax nor enables the definition of arbitrary encodings to alternate
representation formats.
        
        
This specification defines the following [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) for expressing a
data schema, which an [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) can include in the [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential)
that it issues:
        

        
          credentialSchema
          
            
The value of the `credentialSchema` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) MUST be one or
more data schemas that provide [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) with enough information to
determine whether the provided data conforms to the provided schema(s). Each
`credentialSchema` MUST specify its `type` (for example,
`JsonSchema`) and an `id` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property)
that MUST be a [URL](https://www.w3.org/TR/vc-data-model-2.0/#dfn-url) identifying the schema file. The specific type
definition determines the precise contents of each data schema.
            
            
If multiple schemas are present, validity is determined according to the
processing rules outlined by each associated `type` property.
            
          
        

        Note: Credential type-specific syntax checking is possible
The `credentialSchema` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) allows one to
annotate type definitions or lock them to specific versions of the vocabulary.
Authors of [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) can include a static version of their
vocabulary using `credentialSchema` that is secured by some content
integrity protection mechanism. The `credentialSchema`
[property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) also makes it possible to perform syntactic checking on the
[credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) and to use [verification](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verify) mechanisms such as JSON Schema
[[VC-JSON-SCHEMA](https://www.w3.org/TR/vc-data-model-2.0/#bib-vc-json-schema)] validation.
        

        
        
    [Example 14](https://www.w3.org/TR/vc-data-model-2.0/#example-using-the-credentialschema-property-to-perform-json-schema-validation): Using the credentialSchema property to perform JSON schema validation
   ```
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://www.w3.org/ns/credentials/examples/v2"
  ],
  "id": "http://university.example/credentials/3732",
  "type": ["VerifiableCredential", "ExampleDegreeCredential", "ExamplePersonCredential"],
  "issuer": "https://university.example/issuers/14",
  "validFrom": "2010-01-01T19:23:24Z",
  "credentialSubject": {
    "id": "did:example:ebfeb1f712ebc6f1c276e12ec21",
    "degree": {
      "type": "ExampleBachelorDegree",
      "name": "Bachelor of Science and Arts"
    },
    "alumniOf": {
      "name": "Example University"
    }
  },
  "credentialSchema": [{
    "id": "https://example.org/examples/degree.json",
    "type": "JsonSchema"
  },
  {
    "id": "https://example.org/examples/alumni.json",
    "type": "JsonSchema"
  }]
}
```
      

        
In the example above, the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) is specifying two `credentialSchema`
objects, each of which point to a JSON Schema [[VC-JSON-SCHEMA](https://www.w3.org/TR/vc-data-model-2.0/#bib-vc-json-schema)] file that a
[verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) can use to determine whether the [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) is
well-formed.

---

### 4.12 Securing Mechanisms
        

        
This specification recognizes two classes of
securing mechanisms:
those that use enveloping proofs and those that use embedded proofs.
        

        
An enveloping proof wraps a serialization
of this data model. One such RECOMMENDED enveloping proof mechanism is defined
in [Securing Verifiable Credentials using JOSE and COSE](https://www.w3.org/TR/vc-jose-cose/) [[VC-JOSE-COSE](https://www.w3.org/TR/vc-data-model-2.0/#bib-vc-jose-cose)].
        

        
An embedded proof is a mechanism where the proof is
included in the serialization of the data model. One such RECOMMENDED embedded
proof mechanism is defined in [Verifiable Credential Data Integrity 1.0](https://www.w3.org/TR/vc-data-integrity/) [[VC-DATA-INTEGRITY](https://www.w3.org/TR/vc-data-model-2.0/#bib-vc-data-integrity)].
        

        
These two classes of securing mechanisms are not mutually exclusive. Additional
securing mechanism specifications might also be defined according to the rules
in Section [5.13 Securing Mechanism Specifications](https://www.w3.org/TR/vc-data-model-2.0/#securing-mechanism-specifications).
        

        
        
    [Example 15](https://www.w3.org/TR/vc-data-model-2.0/#example-a-verifiable-credential-using-an-embedded-proof): A verifiable credential using an embedded proof
   ```
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://www.w3.org/ns/credentials/examples/v2"
  ],
  "id": "http://example.gov/credentials/3732",
  "type": ["VerifiableCredential", "ExampleDegreeCredential"],
  "issuer": "did:example:6fb1f712ebe12c27cc26eebfe11",
  "validFrom": "2010-01-01T19:23:24Z",
  "credentialSubject": {
    "id": "https://subject.example/subject/3921",
    "degree": {
      "type": "ExampleBachelorDegree",
      "name": "Bachelor of Science and Arts"
    }
  },
  "proof": {
    "type": "DataIntegrityProof",
    "cryptosuite": "eddsa-rdfc-2022",
    "created": "2021-11-13T18:19:39Z",
    "verificationMethod": "https://university.example/issuers/14#key-1",
    "proofPurpose": "assertionMethod",
    "proofValue": "z58DAdFfa9SkqZMVPxAQp...jQCrfFPP2oumHKtz"
  }
}
```
      

        
The [embedded proof](https://www.w3.org/TR/vc-data-model-2.0/#dfn-embedded-proof) above secures the original [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) by decorating
the original data with a digital signature via the `proof` property. This
results in a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) that is easy to manage in modern
programming environments and database systems.
        

        
        
    [Example 16](https://www.w3.org/TR/vc-data-model-2.0/#example-a-verifiable-credential-that-uses-an-enveloping-proof-in-sd-jwt-format): A verifiable credential that uses an enveloping proof in SD-JWT format
   ```
eyJhbGciOiJFUzM4NCIsImtpZCI6IkdOV2FBTDJQVlVVMkpJVDg5bTZxMGM3U3ZjNDBTLWJ2UjFTT0
Q3REZCb1UiLCJ0eXAiOiJ2YytsZCtqc29uK3NkLWp3dCIsImN0eSI6InZjK2xkK2pzb24ifQ
.
eyJAY29udGV4dCI6WyJodHRwczovL3d3dy53My5vcmcvbnMvY3JlZGVudGlhbHMvdjIiLCJodHRwcz
ovL3d3dy53My5vcmcvbnMvY3JlZGVudGlhbHMvZXhhbXBsZXMvdjIiXSwiaXNzdWVyIjoiaHR0cHM6
Ly91bml2ZXJzaXR5LmV4YW1wbGUvaXNzdWVycy81NjUwNDkiLCJ2YWxpZEZyb20iOiIyMDEwLTAxLT
AxVDE5OjIzOjI0WiIsImNyZWRlbnRpYWxTY2hlbWEiOnsiX3NkIjpbIlNFOHp4bmduZTNNbWEwLUNm
S2dlYW1rNUVqU1NfOXRaNlN5NDdBdTdxRWMiLCJjT3lySEVrSlZwdEtSdURtNkNZVTREajJvRkExd0
JQRjFHcTJnWEo1NXpzIl19LCJjcmVkZW50aWFsU3ViamVjdCI6eyJkZWdyZWUiOnsibmFtZSI6IkJh
Y2hlbG9yIG9mIFNjaWVuY2UgYW5kIEFydHMiLCJfc2QiOlsibVNfSVBMa0JHcTIxbVA3Z0VRaHhOck
E0ZXNMc1ZKQ1E5QUpZNDFLLVRQSSJdfSwiX3NkIjpbIlhTSG9iU05Md01PVl9QNkhQMHNvMnZ1clNy
VXZ3UURYREJHQWtyTXk3TjgiXX0sIl9zZCI6WyJQNE5qWHFXa2JOc1NfRzdvdmlLdm1NOG0yckhDTm
5XVVV2SXZBbW9jb2RZIiwieFNvSHBKUXlCNGV1dmg4SkFJdDFCd1pjNFVEOHY5S3ZOTmVLMk9OSjFC
QSJdLCJfc2RfYWxnIjoic2hhLTI1NiIsImlzcyI6Imh0dHBzOi8vdW5pdmVyc2l0eS5leGFtcGxlL2
lzc3VlcnMvNTY1MDQ5IiwiaWF0IjoxNzAzNjI1OTAxLCJleHAiOjE3MzUyNDgzMDEsImNuZiI6eyJq
d2siOnsia3R5IjoiRUMiLCJjcnYiOiJQLTM4NCIsImFsZyI6IkVTMzg0IiwieCI6Inl1Zlo1SFUzcU
NfOTRMbkI3Zklzd0hmT0swQlJra0Z5bzVhd1QyX21ld0tJWUpLMVNfR0QySVB3UjRYUTZpdFEiLCJ5
IjoiRmEtV2pOd2NLQ1RWWHVDU2tCY3RkdHJOYzh6bXdBTTZWOWxudmxxd1QyQnRlQ0ZHNmR6ZDJoMF
VjeXluTDg0dCJ9fX0
.
M7BFJB9LEV_xEylSJpP00fd_4WjrOlXshh0dUv3QgOzw2MEGIfSfi9PoCkHJH7TI0InsqkD6XZVz38
MpeDKekgBW-RoDdJmxnifYOEJhKpJ5EN9PvA007UPi9QCaiEzX
~
WyJFX3F2V09NWVQ1Z3JNTkprOHNXN3BBIiwgImlkIiwgImh0dHA6Ly91bml2ZXJzaXR5LmV4YW1wbG
UvY3JlZGVudGlhbHMvMTg3MiJd
~
WyJTSEc4WnpfRDVRbFMwU0ZrZFUzNXlRIiwgInR5cGUiLCBbIlZlcmlmaWFibGVDcmVkZW50aWFsIi
wgIkV4YW1wbGVBbHVtbmlDcmVkZW50aWFsIl1d
~
WyJqZzJLRno5bTFVaGFiUGtIaHV4cXRRIiwgImlkIiwgImh0dHBzOi8vZXhhbXBsZS5vcmcvZXhhbX
BsZXMvZGVncmVlLmpzb24iXQ
~
WyItQmhzaE10UnlNNUVFbGt4WGVXVm5nIiwgInR5cGUiLCAiSnNvblNjaGVtYSJd~WyJ0SEFxMEUwN
nY2ckRuUlNtSjlSUWRBIiwgImlkIiwgImRpZDpleGFtcGxlOjEyMyJd
~
WyJ1Ynd6bi1kS19tMzRSMGI0SG84QTBBIiwgInR5cGUiLCAiQmFjaGVsb3JEZWdyZWUiXQ
```
      

        
The [enveloping proof](https://www.w3.org/TR/vc-data-model-2.0/#dfn-enveloping-proof) above secures the original [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) by
encapsulating the original data in a digital signature envelope, resulting in a
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) that can be processed using tooling that understands
the SD-JWT format.
