---
name: "w3c-vcdm-privacy-minimization"
description: "Use when implementing data-minimization and selective disclosure privacy approaches in W3C VCDM. Covers privacy tradeoffs and mitigation patterns in mid-section privacy guidance."
sections:
  - "8.8 Favor Abstract Claims*This section is non-normative.*"
  - "8.9 The Principle of Data Minimization*This section is non-normative.*"
  - "8.10 Bearer Credentials*This section is non-normative.*"
  - "8.11 Correlation During Validation*This section is non-normative.*"
---

<!-- ARF version: 2.0-2024-12-04 -->
<!-- Tokens: ~7521 -->

### 8.8 Favor Abstract Claims*This section is non-normative.*
        

        
[Issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) are encouraged to limit the information included in a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) to the smallest set required for the intended purposes, so as to
allow recipients to use them in various situations without disclosing more
personally identifiable information (PII) than necessary. One way to avoid
placing PII in a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) is to use an abstract [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property)
that meets the needs of [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) without providing overly specific
information about a [subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects).
        
        
For example, this document uses the `ageOver` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property)
instead of a specific birthdate, which would represent more sensitive PII. If
retailers in a particular market commonly require purchasers to be older than
a certain age, an [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) trusted in that market might choose to offer
[verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) that claim that [subjects](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects) have met that
requirement rather than offering [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) that contain
[claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) about the customers' birthdays. This practice enables individual
customers to make purchases without disclosing more PII than necessary.

---

### 8.9 The Principle of Data Minimization*This section is non-normative.*
        

        
Privacy violations occur when information divulged in one context leaks into
another. One accepted best practice for preventing such a violation is for
[verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) to limit the information requested and received, to the absolute
minimum necessary for a particular transaction. Regulations in multiple
jurisdictions, including the Health Insurance Portability and Accountability
Act (HIPAA) in the United States and the General Data Protection Regulation
(GDPR) in the European Union, mandate this data minimization approach.
        
        
With [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential), data minimization for [issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) means
limiting the content of a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) to the minimum required by
potential [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) for expected use. For [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier), data minimization
means restricting the scope of information requested or required for
accessing services.
        
        
For example, a driver's license containing a driver's ID number, height, weight,
birthday, and home address expressed as a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) contains
more information than is necessary to establish that the person is above a
certain age.
        

        
It is considered best practice for [issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) to atomize information or use a
securing mechanism that allows for [selective disclosure](https://www.w3.org/TR/vc-data-model-2.0/#dfn-selective-disclosure). For example, an
[issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) of driver's licenses could issue a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential)
containing every property that appears on a driver's license, and allow the
[holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) to disclose each property selectively. It could also issue more
abstract [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) (for example, a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential)
containing only an `ageOver` property). One possible adaptation would be for
[issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) to provide secure HTTP endpoints for retrieving single-use [bearer credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-bearer-credentials) that promote the pseudonymous use of [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential).
Implementers that find this impractical or unsafe might consider using
[selective disclosure](https://www.w3.org/TR/vc-data-model-2.0/#dfn-selective-disclosure) schemes that eliminate dependence on [issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) at
proving time and reduce the risk of temporal correlation by [issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers).
        

        
[Verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) are urged to only request information that is strictly necessary
for a specific transaction to occur. This is important for at least
two reasons:
        

        
          - 
It reduces the liability on the [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) for handling highly sensitive
information that it does not need to handle.
          
          - 
It enhances the [subject's](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects) and/or [holder's](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) privacy by only asking for
information that is necessary for a specific transaction.
          
        

        
Implementers of software used by [holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) are encouraged to disclose the
information being requested by a [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier), allowing the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) to
decline to share specific information that is unnecessary for the
transaction. Implementers of software used by [holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) are also advised
to give [holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) access to logs of information shared with [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier),
enabling the [holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) to provide this information to authorities if they
believe that they have been subjected to information overreach or coerced to
share more information than necessary for a particular transaction.
        

        Note: Minimum disclosure can still lead to unique identification
While it is possible to practice the principle of minimum disclosure, it might
be impossible to avoid the strong identification of an individual for
specific use cases during a single session or over multiple sessions. The
authors of this document cannot stress how difficult it is to meet this
principle in real-world scenarios.

---

### 8.10 Bearer Credentials*This section is non-normative.*
        

        
A bearer credential is a
privacy-enhancing piece of information, such as a concert ticket, that entitles
its [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) to a specific resource without requiring the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) to
divulge sensitive information. In low-risk scenarios, entities often use bearer
credentials where multiple [holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) presenting the same [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential)
is not a concern or would not result in large economic or reputational losses.
        

        
[Verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) that are [bearer credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-bearer-credentials) are made
possible by not specifying the [subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects) identifier, expressed using the
`id` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property), which is nested in the
`credentialSubject` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property). For example, the following
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) is a [bearer credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-bearer-credentials):
        

        
        
    [Example 35](https://www.w3.org/TR/vc-data-model-2.0/#example-use-of-issuer-properties): Use of issuer properties
   
      - Credential- ecdsa- ecdsa-sd- bbs- jose- cose- sd-jwt```
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://www.w3.org/ns/credentials/examples/v2"
  ],
  "id": "http://university.example/credentials/temporary/28934792387492384",
  "type": ["VerifiableCredential", "ExampleDegreeCredential"],
  "issuer": "https://university.example/issuers/14",
  "validFrom": "2017-10-22T12:23:48Z",
  "credentialSubject": {
    // note that the 'id' property is not specified for bearer credentials
    "degree": {
      "type": "ExampleBachelorDegree",
      "name": "Bachelor of Science and Arts"
    }
  }
}
```**application/vc**
            ```
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://www.w3.org/ns/credentials/examples/v2"
  ],
  "id": "http://university.example/credentials/temporary/28934792387492384",
  "type": [
    "VerifiableCredential",
    "ExampleDegreeCredential"
  ],
  "issuer": "https://university.example/issuers/14",
  "validFrom": "2017-10-22T12:23:48Z",
  "credentialSubject": {
    "degree": {
      "type": "ExampleBachelorDegree",
      "name": "Bachelor of Science and Arts"
    }
  },
  "proof": {
    "type": "DataIntegrityProof",
    "created": "2025-04-27T17:58:34Z",
    "verificationMethod": "did:key:zDnaebSRtPnW6YCpxAhR5JPxJqt9UunCsBPhLEtUokUvp87nQ",
    "cryptosuite": "ecdsa-rdfc-2019",
    "proofPurpose": "assertionMethod",
    "proofValue": "z5gCBzvpHbsJoeuuy5Z54rKQwkGzBZkmapRZZAKKW4ervhBGGTaygnh4sBG6vV8MHGD8eKhXEmkXr487JwVhZ2WHQ"
  }
}
```**application/vc**
            ```
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://www.w3.org/ns/credentials/examples/v2"
  ],
  "id": "http://university.example/credentials/temporary/28934792387492384",
  "type": [
    "VerifiableCredential",
    "ExampleDegreeCredential"
  ],
  "issuer": "https://university.example/issuers/14",
  "validFrom": "2017-10-22T12:23:48Z",
  "credentialSubject": {
    "degree": {
      "type": "ExampleBachelorDegree",
      "name": "Bachelor of Science and Arts"
    }
  },
  "proof": {
    "type": "DataIntegrityProof",
    "created": "2025-04-27T17:58:34Z",
    "verificationMethod": "did:key:zDnaerJh8WwyBVVGcZKKkqRKK9iezje8ut6t9bnNChtxcWwNv",
    "cryptosuite": "ecdsa-sd-2023",
    "proofPurpose": "assertionMethod",
    "proofValue": "u2V0AhVhAOEMucTcwHIY19VxghifeZjhZGFI9buw5OmEiWzSpbStoG5arWcYX6NB2-ftSiNc_CMh-CemG3peCu8ZOrSCHVFgjgCQC1zlBPjThDb-LSIbpc3uzcrjmKdC3xyuQAM8DoT5zv3FYIP13m1SOplZJx47EsonA19WEGnwABCA4hlMlQS96LIQMhVhADxlyJM3iqf_jn__vvJ0KgjL5uKLmVSsOxTFUsIHJ82mS8DAo_WZUmDxMnCAjrrxPQXLaNdfcmqehQOLT4_oiiVhA74UxSBi3EedkNnN5F2WV_Hd1Pr1vPWA_Qx52meKAa0_FhKu-Gm8uk2fFxK28flIbUv5HVQgGT0nrSuSprE4JslhAGl8hwCBGr5KxrUVAcMZE3vW26KrrI6jMTDLPGb81b9-ILrXLIJKb_ZOcmLggwzgbyxE_hUDLL9b88aZ7tE4dOVhACerSusVIq25s-hjms5Ws4Uw3wmgRQp1lp228deojpcavN-n3FNe3AIBgHFbpK2SzdOzvraj-HVkMpQptXrGEhVhAujmfdq6faQbfYn4LUQCy_sDUr1WNbklcyg2XTDQKscMF0VAUU38d50UrmprSKbhrnZpgWMBFg4ibUco_HO4UToFnL2lzc3Vlcg"
  }
}
```**application/vc**
            ```
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://www.w3.org/ns/credentials/examples/v2"
  ],
  "id": "http://university.example/credentials/temporary/28934792387492384",
  "type": [
    "VerifiableCredential",
    "ExampleDegreeCredential"
  ],
  "issuer": "https://university.example/issuers/14",
  "validFrom": "2017-10-22T12:23:48Z",
  "credentialSubject": {
    "degree": {
      "type": "ExampleBachelorDegree",
      "name": "Bachelor of Science and Arts"
    }
  },
  "proof": {
    "type": "DataIntegrityProof",
    "verificationMethod": "did:key:zUC78GzFRA4TWh2mqRiKro1wwRb5KDaMJ3M1AD3qGtgEbFrwWGvWbnCzArkeTZCyzBz4Panr2hLaZxsXHiBQCwBc3fRPH6xY4u5v8ZAd3dPW1aw89Rra86CVwXr3DczANggYbMD",
    "cryptosuite": "bbs-2023",
    "proofPurpose": "assertionMethod",
    "proofValue": "u2V0ChVhQhlm-IXSzQAaXH0xW-NU1t3ikH2xt--sFY-DtoL44DiWf3qv-nuhCc36deovk3t1GLy9JeN-vdeth8XWKMGUcyA4eWD21lxYdvK5Qdzw07ytYQGd_DaMQQsoaryttl5TvxnFT-Vm4SkVx03K9qNJ4jhArdrHmhnEXifHmmlKM3zCnc0pq4l3ZkBkIESZ4DrQomVNYYJVTGbTfcflzyx41E-f9kSqmf10xYzxJrGfC7b7GPY8X7VjMT__ZKSuwdH-5jak-5gkjocsHI6oxIKlLrhW1Wh5yrDCH-QC823TS8NE9VGBzIFAfUt5qazGEcJ8CxeSPxFggOkuR5x7VvZAB-RbcqkcwxkQ7or0tsVOUTPlebfxRUQCBZy9pc3N1ZXI"
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
  "id": "http://university.example/credentials/temporary/28934792387492384",
  "type": [
    "VerifiableCredential",
    "ExampleDegreeCredential"
  ],
  "issuer": "https://university.example/issuers/14",
  "validFrom": "2017-10-22T12:23:48Z",
  "credentialSubject": {
    "degree": {
      "type": "ExampleBachelorDegree",
      "name": "Bachelor of Science and Arts"
    }
  }
}
```
**application/vc+jwt**


eyJraWQiOiJFeEhrQk1XOWZtYmt2VjI2Nm1ScHVQMnNVWV9OX0VXSU4xbGFwVXpPOHJvIiwiYWxnIjoiRVMyNTYifQ
.eyJAY29udGV4dCI6WyJodHRwczovL3d3dy53My5vcmcvbnMvY3JlZGVudGlhbHMvdjIiLCJodHRwczovL3d3dy53My5vcmcvbnMvY3JlZGVudGlhbHMvZXhhbXBsZXMvdjIiXSwiaWQiOiJodHRwOi8vdW5pdmVyc2l0eS5leGFtcGxlL2NyZWRlbnRpYWxzL3RlbXBvcmFyeS8yODkzNDc5MjM4NzQ5MjM4NCIsInR5cGUiOlsiVmVyaWZpYWJsZUNyZWRlbnRpYWwiLCJFeGFtcGxlRGVncmVlQ3JlZGVudGlhbCJdLCJpc3N1ZXIiOiJodHRwczovL3VuaXZlcnNpdHkuZXhhbXBsZS9pc3N1ZXJzLzE0IiwidmFsaWRGcm9tIjoiMjAxNy0xMC0yMlQxMjoyMzo0OFoiLCJjcmVkZW50aWFsU3ViamVjdCI6eyJkZWdyZWUiOnsidHlwZSI6IkV4YW1wbGVCYWNoZWxvckRlZ3JlZSIsIm5hbWUiOiJCYWNoZWxvciBvZiBTY2llbmNlIGFuZCBBcnRzIn19fQ
.6xC1cZL-ht0EvN7nz2Zs81htECRBp_87csS2IRyRG41wp-4zW0US8rth2KZjQMhsuPy7s0yjVIRWFGb6TQRCdg


    


    
**application/vc**
```
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://www.w3.org/ns/credentials/examples/v2"
  ],
  "id": "http://university.example/credentials/temporary/28934792387492384",
  "type": [
    "VerifiableCredential",
    "ExampleDegreeCredential"
  ],
  "issuer": "https://university.example/issuers/14",
  "validFrom": "2017-10-22T12:23:48Z",
  "credentialSubject": {
    "degree": {
      "type": "ExampleBachelorDegree",
      "name": "Bachelor of Science and Arts"
    }
  }
}
```
**application/vc+cose**

d28443a10128a05901a27b2240636f6e74657874223a5b2268747470733a2f2f7777772e77332e6f72672f6e732f63726564656e7469616c732f7632222c2268747470733a2f2f7777772e77332e6f72672f6e732f63726564656e7469616c732f6578616d706c65732f7632225d2c226964223a22687474703a2f2f756e69766572736974792e6578616d706c652f63726564656e7469616c732f74656d706f726172792f3238393334373932333837343932333834222c2274797065223a5b2256657269666961626c6543726564656e7469616c222c224578616d706c6544656772656543726564656e7469616c225d2c22697373756572223a2268747470733a2f2f756e69766572736974792e6578616d706c652f697373756572732f3134222c2276616c696446726f6d223a22323031372d31302d32325431323a32333a34385a222c2263726564656e7469616c5375626a656374223a7b22646567726565223a7b2274797065223a224578616d706c6542616368656c6f72446567726565222c226e616d65223a2242616368656c6f72206f6620536369656e636520616e642041727473227d7d7d58409ec236d42a81339288605ac9a750f8632dadc2d44bcaae49b2d1431f9d98fded1c01772494c84a0aab75b9ec527ce6dc3fbd4d7f913f6963549cb19c091be521

    


    
    
    
    
      - 
        Encoded
      
      - 
        Decoded
      
      - 
        Issuer Disclosures
      
    
    
      

eyJraWQiOiJFeEhrQk1XOWZtYmt2VjI2Nm1ScHVQMnNVWV9OX0VXSU4xbGFwVXpPOHJvIiwiYWxnIjoiRVMyNTYifQ
.eyJpYXQiOjE3NDU3NzY3MTQsImV4cCI6MTc0Njk4NjMxNCwiX3NkX2FsZyI6InNoYS0yNTYiLCJAY29udGV4dCI6WyJodHRwczovL3d3dy53My5vcmcvbnMvY3JlZGVudGlhbHMvdjIiLCJodHRwczovL3d3dy53My5vcmcvbnMvY3JlZGVudGlhbHMvZXhhbXBsZXMvdjIiXSwiaXNzdWVyIjoiaHR0cHM6Ly91bml2ZXJzaXR5LmV4YW1wbGUvaXNzdWVycy8xNCIsInZhbGlkRnJvbSI6IjIwMTctMTAtMjJUMTI6MjM6NDhaIiwiY3JlZGVudGlhbFN1YmplY3QiOnsiZGVncmVlIjp7Im5hbWUiOiJCYWNoZWxvciBvZiBTY2llbmNlIGFuZCBBcnRzIiwiX3NkIjpbIl9BT1Y2UkQwSmFobzVaaUgxSUxNd0pXSlE3cS1ueWVveVhIQWoyeVdtUlkiXX19LCJfc2QiOlsiUG9aeVBTUGtzd1AyODdsRU5ZMDJHdzg1Q2NzMjYyWU5fVkZLSEFpOGZ3byIsIlY0Y0k4aDQ5VUt6em5UdGpMQV9NZ3hBblFoeWR0ME45OWVVdjBTZXJibDQiXX0
.71495BlH0xrBlHTp-Y2JqwvTx1u3nu8dS8eiXwxSF-TukGYmbZ0y74RxVQCZ046h7YK2OZ-FZjlVUAcTN0vLvQ
~WyJqVThiaS1zWHk1dzVKNUYtdlhNaUZ3IiwgImlkIiwgImh0dHA6Ly91bml2ZXJzaXR5LmV4YW1wbGUvY3JlZGVudGlhbHMvdGVtcG9yYXJ5LzI4OTM0NzkyMzg3NDkyMzg0Il0~WyJlbXBLOFdGNDhHcW56ekVudTJNblV3IiwgInR5cGUiLCBbIlZlcmlmaWFibGVDcmVkZW50aWFsIiwgIkV4YW1wbGVEZWdyZWVDcmVkZW50aWFsIl1d~WyJnTnRsVmhfeVZyWm5aeEVXQUpyaFhRIiwgInR5cGUiLCAiRXhhbXBsZUJhY2hlbG9yRGVncmVlIl0~

    
    
      ```
{  "kid": "ExHkBMW9fmbkvV266mRpuP2sUY_N_EWIN1lapUzO8ro",  "alg": "ES256"}
```
      ```
{  "iat": 1745776714,  "exp": 1746986314,  "_sd_alg": "sha-256",  "@context": [    "https://www.w3.org/ns/credentials/v2",    "https://www.w3.org/ns/credentials/examples/v2"  ],  "issuer": "https://university.example/issuers/14",  "validFrom": "2017-10-22T12:23:48Z",  "credentialSubject": {    "degree": {      "name": "Bachelor of Science and Arts",      "_sd": [        "_AOV6RD0Jaho5ZiH1ILMwJWJQ7q-nyeoyXHAj2yWmRY"      ]    }  },  "_sd": [    "PoZyPSPkswP287lENY02Gw85Ccs262YN_VFKHAi8fwo",    "V4cI8h49UKzznTtjLA_MgxAnQhydt0N99eUv0Serbl4"  ]}
```

---

### 8.11 Correlation During Validation*This section is non-normative.*
        

        
When processing [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential), [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier)
evaluate relevant [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) before relying upon them. This
evaluation might be done in any manner desired as long as it satisfies
the requirements of the [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) doing the validation.
Many verifiers will perform the checks listed in Appendix [A. Validation](https://www.w3.org/TR/vc-data-model-2.0/#validation) as
well as a variety of specific business process checks such as:
        

        
          - 
The professional licensure status of the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders).
          
          - 
A date of license renewal or revocation.
          
          - 
The sub-qualifications of an individual.
          
          - 
If a relationship exists between the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) and the [entity](https://www.w3.org/TR/vc-data-model-2.0/#dfn-entities)
with whom the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) is attempting to interact.
          
          - 
The geolocation information associated with the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders).
          
        

        
The process of performing these checks might result in information leakage that
leads to a privacy violation of the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders). For example, a simple
operation, such as checking an improperly configured revocation list, can
notify the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) that a specific business is likely interacting
with the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders). This could
enable [issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) to collude to correlate individuals without their
knowledge.
        

        
[Issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) are urged to not use mechanisms, such as [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential)
revocation lists that are unique per [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential), during the
[verification](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verify) process, which could lead to privacy violations. Organizations
providing software to [holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) ought to warn when [credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) include
information that could lead to privacy violations during the verification
process. [Verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) are urged to consider rejecting [credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) that
produce privacy violations or that enable substandard privacy practices.
