---
name: "w3c-vcdm-trust-extensibility"
description: "Use when working with W3C VCDM trust and extensibility features. Covers: trust model and extensibility."
sections:
  - "5.1 Trust Model*This section is non-normative.*"
  - "5.2 Extensibility"
---

<!-- ARF version: 2.0-2024-12-04 -->
<!-- Tokens: ~7000 -->

### 5.1 Trust Model*This section is non-normative.*
        

        
The [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) trust model is based on the following
expectations:
        

        
          - 
The [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) expects the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) to verifiably issue the
[credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) that it receives. This can be established by satisfying
either of the following:
            
              - 
An [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) secures a [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) with a
[securing mechanism](https://www.w3.org/TR/vc-data-model-2.0/#securing-mechanisms) which establishes that the
[issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) generated the [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential). In other words, an [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) issues a
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential).
              
              - 
A [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) is transmitted in a way that clearly establishes that the
[issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) generated the [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential), and that the [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) was not
tampered with in transit nor storage. This expectation could be weakened,
depending on the risk assessment by the [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier).
              
            
          
          - 
All [entities](https://www.w3.org/TR/vc-data-model-2.0/#dfn-entities) expect the [verifiable data registry](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-data-registries) to be tamper-evident
and to be a correct record of which data is controlled by which [entities](https://www.w3.org/TR/vc-data-model-2.0/#dfn-entities).
This is typically achieved by the method of its publication. This could be via a
peer-to-peer protocol from a trusted publisher, a publicly accessible and well
known web site (with a content hash), a blockchain, etc. When entities publish
metadata about themselves, the publication can be integrity-protected by being
secured using with the entity's private key.
          
          - 
The [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) and [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) expect the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) to stand by [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims)
it makes in [credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) about the [subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects), and to revoke [credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential)
quickly if and when they no longer stand by those [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims).
          
          - 
The [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) might trust the [issuer's](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) because the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders)
has a pre-existing trust relationship with the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers). For example, an
employer might provide an employee with an employment [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential),
or a government might issue an electronic passport to a citizen.
        
Where no pre-existing trust relationship exists, the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) might
have some out-of-band means of determining whether the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) is
qualified to issue the [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) being provided.
        
        
Note: It is not always necessary for the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) to trust the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers),
since the issued [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) might be an assertion about
a [subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects) who is not the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders), or about no-one, and the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders)
might be willing to relay this information to a [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) without
being held accountable for its veracity.
        
        
          - 
The [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) expects the [credential repository](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential-repositories) to store [credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential)
securely, to not release [credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) to anyone other than the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders)
(which may subsequently present them to a [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier)), and to not corrupt nor
lose [credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) while they are in its care.
          
        

        
This trust model differentiates itself from other trust models by ensuring
the following:
        

        
          - 
The [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) and [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) do not need to know anything about the
[credential repository](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential-repositories).
          
          - 
The [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) does not need to know anything about the [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier).
          
        

       
How [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) decide which [issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) to trust, and for what data or
purposes, is out of scope for this recommendation. Some [issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers), such as
well-known organizations, might be trusted by many [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) simply because
of their reputation. Some [issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) and [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) might be members of a
community in which all members trust each other due to the rules of membership.
Some [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) might trust a specific trust-service provider whose
responsibility is to vet [issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) and list them in a trust list such as those
specified in [Electronic Signatures and Infrastructures (ESI); Trusted Lists](https://www.etsi.org/deliver/etsi_ts/119600_119699/119612/02.01.01_60/ts_119612v020101p.pdf) [[ETSI-TRUST-LISTS](https://www.w3.org/TR/vc-data-model-2.0/#bib-etsi-trust-lists)] or the
[Adobe
Approved Trust List](https://helpx.adobe.com/acrobat/kb/approved-trust-list1.html).
        

        
By decoupling the expectations between the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) and the [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier),
a more flexible and dynamic trust model is created, such that market
competition and customer choice is increased.
        

        
For more information about how this trust model interacts with various threat
models studied by the Working Group, see the [Verifiable Credentials Use Cases](https://www.w3.org/TR/vc-use-cases/) [[VC-USE-CASES](https://www.w3.org/TR/vc-data-model-2.0/#bib-vc-use-cases)].
        

        Note: Trust model differs from the traditional Certificate Authority system
The data model detailed in this specification does not imply a transitive trust
model, such as that provided by more traditional Certificate Authority trust
models. In the Verifiable Credentials Data Model, a [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) either
directly trusts or does not trust an [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers). While it is possible to
build transitive trust models using the Verifiable Credentials Data Model,
implementers are urged to
[learn
about the security weaknesses](https://datatracker.ietf.org/doc/draft-iab-web-pki-problems/) introduced by
[broadly delegating trust](https://www.usenix.org/conference/imc-05/perils-transitive-trust-domain-name-system) in the manner adopted by Certificate Authority
systems.

---

### 5.2 Extensibility
        

        
One of the goals of the Verifiable Credentials Data Model is to enable
permissionless innovation. To achieve this, the data model needs to be
extensible in a number of different ways. The data model is required to:
        

        
          - 
Model complex multi-entity relationships through the use of a [graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-graphs)-based
data model.
          
          - 
Extend the machine-readable vocabularies used to describe information in the
data model, without the use of a centralized system for doing so, through the
use of Linked Data [[LINKED-DATA](https://www.w3.org/TR/vc-data-model-2.0/#bib-linked-data)].
          
          - 
Support multiple types of cryptographic proof formats through the use of
[Securing Verifiable Credentials using JOSE and COSE](https://www.w3.org/TR/vc-jose-cose/), [Verifiable Credential Data Integrity 1.0](https://www.w3.org/TR/vc-data-integrity/), and a variety of cryptographic
suites listed in the [Verifiable Credential Extensions](https://w3c.github.io/vc-extensions/) document.
          
          - 
Provide all of the extensibility mechanisms outlined above in a data format that
is popular with software developers and web page authors, and is enabled through
the use of [JSON-LD 1.1](https://www.w3.org/TR/json-ld11/).
          
        

        
This approach to data modeling is often called an
*open world assumption*, meaning that any entity can say anything about
any other entity. While this approach seems to conflict with building simple and
predictable software systems, balancing extensibility with program correctness
is always more challenging with an open world assumption than with closed
software systems.
        

        
The rest of this section describes, through a series of examples, how both
extensibility and program correctness are achieved.
        

        
Let us assume we start with the [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) shown below.
        

        
        
    [Example 22](https://www.w3.org/TR/vc-data-model-2.0/#example-a-simple-credential): A simple credential
   
      - Credential- ecdsa- ecdsa-sd- bbs- jose- cose- sd-jwt```
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://www.w3.org/ns/credentials/examples/v2"
  ],
  "id": "http://vc.example/credentials/4643",
  "type": ["VerifiableCredential"],
  "issuer": "https://issuer.example/issuers/14",
  "validFrom": "2018-02-24T05:28:04Z",
  "credentialSubject": {
    "id": "did:example:abcdef1234567",
    "name": "Jane Doe"
  }
}
```**application/vc**
            ```
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://www.w3.org/ns/credentials/examples/v2"
  ],
  "id": "http://vc.example/credentials/4643",
  "type": [
    "VerifiableCredential"
  ],
  "issuer": "https://issuer.example/issuers/14",
  "validFrom": "2018-02-24T05:28:04Z",
  "credentialSubject": {
    "id": "did:example:abcdef1234567",
    "name": "Jane Doe"
  },
  "proof": {
    "type": "DataIntegrityProof",
    "created": "2025-04-27T17:58:34Z",
    "verificationMethod": "did:key:zDnaebSRtPnW6YCpxAhR5JPxJqt9UunCsBPhLEtUokUvp87nQ",
    "cryptosuite": "ecdsa-rdfc-2019",
    "proofPurpose": "assertionMethod",
    "proofValue": "z3FfiNeGUGhy8ApiRsv42y5VUPFgbieFbUJebkKhkZ6tNASNv6MkiJwNGWczfmrdYdmLZa6r3rtJ4BSF9BjnwrSo8"
  }
}
```**application/vc**
            ```
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://www.w3.org/ns/credentials/examples/v2"
  ],
  "id": "http://vc.example/credentials/4643",
  "type": [
    "VerifiableCredential"
  ],
  "issuer": "https://issuer.example/issuers/14",
  "validFrom": "2018-02-24T05:28:04Z",
  "credentialSubject": {
    "id": "did:example:abcdef1234567",
    "name": "Jane Doe"
  },
  "proof": {
    "type": "DataIntegrityProof",
    "created": "2025-04-27T17:58:34Z",
    "verificationMethod": "did:key:zDnaerJh8WwyBVVGcZKKkqRKK9iezje8ut6t9bnNChtxcWwNv",
    "cryptosuite": "ecdsa-sd-2023",
    "proofPurpose": "assertionMethod",
    "proofValue": "u2V0AhVhA8DUmqMDGQOAZ8hIuyi_X-LbT_fD_guDAKeRkRbAwk8aXyQeTRQErpRbOMQiYhWHKelW9XSZSIU3_dk8s-SLLIVgjgCQCEJqTiBGYPxkutgRjtMH-_iViqDBvJl4I9XVBXrsRRBhYIC2fjWyVwswq0oXkkyYFTxwdT5k-XZWMJx7JdwFPfALfg1hApuvVmqTlFFKpI79s8M8CND3arkiGE6talSgE8n2iT9NxbWYgiqH0s3Zxo_eXGCbBoxibB3_VMt9huvsz51yhxVhAj55Js6Ka1i7-mfjrszFmD1W0Lc81XKCtAqHvF-qY2XWd6cpHIwWlSvU3NxSoYpcAdxUrgAu17iEmHMLvpdyllFhAo4kADpzjQ_AeB0nvp-IzeawelLeusg8t2M2yZLPzcN3R4alEKnbWofwSflHD2Yx_QQW3U9Ck9YALaKZbO_KIRYFnL2lzc3Vlcg"
  }
}
```**application/vc**
            ```
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://www.w3.org/ns/credentials/examples/v2"
  ],
  "id": "http://vc.example/credentials/4643",
  "type": [
    "VerifiableCredential"
  ],
  "issuer": "https://issuer.example/issuers/14",
  "validFrom": "2018-02-24T05:28:04Z",
  "credentialSubject": {
    "id": "did:example:abcdef1234567",
    "name": "Jane Doe"
  },
  "proof": {
    "type": "DataIntegrityProof",
    "verificationMethod": "did:key:zUC78GzFRA4TWh2mqRiKro1wwRb5KDaMJ3M1AD3qGtgEbFrwWGvWbnCzArkeTZCyzBz4Panr2hLaZxsXHiBQCwBc3fRPH6xY4u5v8ZAd3dPW1aw89Rra86CVwXr3DczANggYbMD",
    "cryptosuite": "bbs-2023",
    "proofPurpose": "assertionMethod",
    "proofValue": "u2V0ChVhQtDW_taTeCBSwoqWX3rzUAFmrR8_TAfE8027nlDX8x4Eiquv_i6S7XU_4mnGV-ODaZYnVuh47RBcLtkevGmEDr_0aXc7ujmM6icKfQgg88cRYQGd_DaMQQsoaryttl5TvxnFT-Vm4SkVx03K9qNJ4jhArvqENcCm8D2khyMGr7-FGFdx818_ufbFmo8hKn_2FgMpYYJVTGbTfcflzyx41E-f9kSqmf10xYzxJrGfC7b7GPY8X7VjMT__ZKSuwdH-5jak-5gkjocsHI6oxIKlLrhW1Wh5yrDCH-QC823TS8NE9VGBzIFAfUt5qazGEcJ8CxeSPxFggPmXI3YCyx-_cwMML4xSJvv9xy0Xvrw9Qb6s21_i5rHiBZy9pc3N1ZXI"
  }
}
```

    
**Protected Headers**
```
{
  "kid": "ExHkBMW9fmbkvV266mRpuP2sUY_N_EWIN1lapUzO8ro",
  "alg": "ES256"
}
```
**application/vc**
```
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://www.w3.org/ns/credentials/examples/v2"
  ],
  "id": "http://vc.example/credentials/4643",
  "type": [
    "VerifiableCredential"
  ],
  "issuer": "https://issuer.example/issuers/14",
  "validFrom": "2018-02-24T05:28:04Z",
  "credentialSubject": {
    "id": "did:example:abcdef1234567",
    "name": "Jane Doe"
  }
}
```
**application/vc+jwt**


eyJraWQiOiJFeEhrQk1XOWZtYmt2VjI2Nm1ScHVQMnNVWV9OX0VXSU4xbGFwVXpPOHJvIiwiYWxnIjoiRVMyNTYifQ
.eyJAY29udGV4dCI6WyJodHRwczovL3d3dy53My5vcmcvbnMvY3JlZGVudGlhbHMvdjIiLCJodHRwczovL3d3dy53My5vcmcvbnMvY3JlZGVudGlhbHMvZXhhbXBsZXMvdjIiXSwiaWQiOiJodHRwOi8vdmMuZXhhbXBsZS9jcmVkZW50aWFscy80NjQzIiwidHlwZSI6WyJWZXJpZmlhYmxlQ3JlZGVudGlhbCJdLCJpc3N1ZXIiOiJodHRwczovL2lzc3Vlci5leGFtcGxlL2lzc3VlcnMvMTQiLCJ2YWxpZEZyb20iOiIyMDE4LTAyLTI0VDA1OjI4OjA0WiIsImNyZWRlbnRpYWxTdWJqZWN0Ijp7ImlkIjoiZGlkOmV4YW1wbGU6YWJjZGVmMTIzNDU2NyIsIm5hbWUiOiJKYW5lIERvZSJ9fQ
.p2BTVD1miV8CyTx1ivkbBmBo_LzoMNyQbDPP1_bxRMov_umGGpsw9ngQ5bF245MAbtH-yJw7L0wx14KKQC1gvw


    


    
**application/vc**
```
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://www.w3.org/ns/credentials/examples/v2"
  ],
  "id": "http://vc.example/credentials/4643",
  "type": [
    "VerifiableCredential"
  ],
  "issuer": "https://issuer.example/issuers/14",
  "validFrom": "2018-02-24T05:28:04Z",
  "credentialSubject": {
    "id": "did:example:abcdef1234567",
    "name": "Jane Doe"
  }
}
```
**application/vc+cose**

d28443a10128a05901487b2240636f6e74657874223a5b2268747470733a2f2f7777772e77332e6f72672f6e732f63726564656e7469616c732f7632222c2268747470733a2f2f7777772e77332e6f72672f6e732f63726564656e7469616c732f6578616d706c65732f7632225d2c226964223a22687474703a2f2f76632e6578616d706c652f63726564656e7469616c732f34363433222c2274797065223a5b2256657269666961626c6543726564656e7469616c225d2c22697373756572223a2268747470733a2f2f6973737565722e6578616d706c652f697373756572732f3134222c2276616c696446726f6d223a22323031382d30322d32345430353a32383a30345a222c2263726564656e7469616c5375626a656374223a7b226964223a226469643a6578616d706c653a61626364656631323334353637222c226e616d65223a224a616e6520446f65227d7d5840eeb9cf85c67689580f3f73aef32e28e495412ab15f694bec8522b52153966a32c16dace5627374f50fef36b7df36415b2a79e652fa87598940e83d0ff972a167

    


    
    
    
    
      - 
        Encoded
      
      - 
        Decoded
      
      - 
        Issuer Disclosures
      
    
    
      

eyJraWQiOiJFeEhrQk1XOWZtYmt2VjI2Nm1ScHVQMnNVWV9OX0VXSU4xbGFwVXpPOHJvIiwiYWxnIjoiRVMyNTYifQ
.eyJpYXQiOjE3NDU3NzY3MTQsImV4cCI6MTc0Njk4NjMxNCwiX3NkX2FsZyI6InNoYS0yNTYiLCJAY29udGV4dCI6WyJodHRwczovL3d3dy53My5vcmcvbnMvY3JlZGVudGlhbHMvdjIiLCJodHRwczovL3d3dy53My5vcmcvbnMvY3JlZGVudGlhbHMvZXhhbXBsZXMvdjIiXSwiaXNzdWVyIjoiaHR0cHM6Ly9pc3N1ZXIuZXhhbXBsZS9pc3N1ZXJzLzE0IiwidmFsaWRGcm9tIjoiMjAxOC0wMi0yNFQwNToyODowNFoiLCJjcmVkZW50aWFsU3ViamVjdCI6eyJuYW1lIjoiSmFuZSBEb2UiLCJfc2QiOlsidVE2NkFmZXF3dWY0Y2s5NXI2cTFWZVZEM3FVYjU0VTJtUmdZdGRWQVpkbyJdfSwiX3NkIjpbIktwdURNMGVHaWtoNXBiVjhUR1lrYjZTdDNaLUZadkNtWmxkeGl1NmwydzgiLCJiUzFQMVNOc2tUb2h1QlRCeE8tNHF4bThRT21sQmlDTXhnVXJnYkNpWHM4Il19
.NUK9XkgPZ46Zc_3urENrSvkN0RRkNUw31ki9YFAJVhggzxBJhYHNBWK1NtFhu6cQU1o0XqKjaYVMXHsCB4SGGQ
~WyJTZDNNNUZ1LTl3dnRaZU85RTE2dEx3IiwgImlkIiwgImh0dHA6Ly92Yy5leGFtcGxlL2NyZWRlbnRpYWxzLzQ2NDMiXQ~WyJKeHpWdGlUWjE3UVBpRDZpdVJIZDh3IiwgInR5cGUiLCBbIlZlcmlmaWFibGVDcmVkZW50aWFsIl1d~WyJwUEY1VG95bFhTa19FeU8zUmhJT2RRIiwgImlkIiwgImRpZDpleGFtcGxlOmFiY2RlZjEyMzQ1NjciXQ~

    
    
      ```
{  "kid": "ExHkBMW9fmbkvV266mRpuP2sUY_N_EWIN1lapUzO8ro",  "alg": "ES256"}
```
      ```
{  "iat": 1745776714,  "exp": 1746986314,  "_sd_alg": "sha-256",  "@context": [    "https://www.w3.org/ns/credentials/v2",    "https://www.w3.org/ns/credentials/examples/v2"  ],  "issuer": "https://issuer.example/issuers/14",  "validFrom": "2018-02-24T05:28:04Z",  "credentialSubject": {    "name": "Jane Doe",    "_sd": [      "uQ66Afeqwuf4ck95r6q1VeVD3qUb54U2mRgYtdVAZdo"    ]  },  "_sd": [    "KpuDM0eGikh5pbV8TGYkb6St3Z-FZvCmZldxiu6l2w8",    "bS1P1SNskTohuBTBxO-4qxm8QOmlBiCMxgUrgbCiXs8"  ]}
```
