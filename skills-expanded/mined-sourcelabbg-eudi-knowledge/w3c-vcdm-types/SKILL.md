---
name: "w3c-vcdm-types"
description: "Use when implementing type constraints in W3C VCDM. Covers: type processing and type requirements for credentials and presentations."
sections:
  - "4.5 Types"
---

<!-- ARF version: 2.0-2024-12-04 -->
<!-- Tokens: ~5094 -->

### 4.5 Types
        

        
Software systems that process the kinds of objects specified in this document
use type information to determine whether or not a provided
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) or [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) is appropriate
for the intended use-case. This specification defines a `type`
[property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) for expressing object type information. This type
information can be used during [validation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claim-validation) processes, as described in Appendix
[A. Validation](https://www.w3.org/TR/vc-data-model-2.0/#validation).
        

        
[Verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) and [verifiable presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) MUST contain a
`type` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) with an associated value.
        

        
          type
          
The value of the `type` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) MUST be one or more
[terms](https://www.w3.org/TR/json-ld11/#dfn-term) and
[absolute URL strings](https://url.spec.whatwg.org/#absolute-url-string). If more than
one value is provided, the order does not matter.
          
        

        
        
    [Example 4](https://www.w3.org/TR/vc-data-model-2.0/#example-use-of-the-type-property): Use of the type property
   
      - Credential- ecdsa- ecdsa-sd- bbs- jose- cose- sd-jwt```
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://www.w3.org/ns/credentials/examples/v2"
  ],
  "id": "http://university.example/credentials/3732",
  "type": ["VerifiableCredential", "ExampleDegreeCredential"],
  "issuer": "https://university.example/issuers/565049",
  "validFrom": "2010-01-01T00:00:00Z",
  "credentialSubject": {
    "id": "did:example:ebfeb1f712ebc6f1c276e12ec21",
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
  "id": "http://university.example/credentials/3732",
  "type": [
    "VerifiableCredential",
    "ExampleDegreeCredential"
  ],
  "issuer": "https://university.example/issuers/565049",
  "validFrom": "2010-01-01T00:00:00Z",
  "credentialSubject": {
    "id": "did:example:ebfeb1f712ebc6f1c276e12ec21",
    "degree": {
      "type": "ExampleBachelorDegree",
      "name": "Bachelor of Science and Arts"
    }
  },
  "proof": {
    "type": "DataIntegrityProof",
    "created": "2025-04-27T17:58:33Z",
    "verificationMethod": "did:key:zDnaebSRtPnW6YCpxAhR5JPxJqt9UunCsBPhLEtUokUvp87nQ",
    "cryptosuite": "ecdsa-rdfc-2019",
    "proofPurpose": "assertionMethod",
    "proofValue": "z2F16goBUjRsg2ieNiojpaz313CN98DU4APFiokAUkUvEYESSDmokg1omwvcK7EFqLgYpdyekEoxnVHwuxt8Webwa"
  }
}
```**application/vc**
            ```
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://www.w3.org/ns/credentials/examples/v2"
  ],
  "id": "http://university.example/credentials/3732",
  "type": [
    "VerifiableCredential",
    "ExampleDegreeCredential"
  ],
  "issuer": "https://university.example/issuers/565049",
  "validFrom": "2010-01-01T00:00:00Z",
  "credentialSubject": {
    "id": "did:example:ebfeb1f712ebc6f1c276e12ec21",
    "degree": {
      "type": "ExampleBachelorDegree",
      "name": "Bachelor of Science and Arts"
    }
  },
  "proof": {
    "type": "DataIntegrityProof",
    "created": "2025-04-27T17:58:33Z",
    "verificationMethod": "did:key:zDnaerJh8WwyBVVGcZKKkqRKK9iezje8ut6t9bnNChtxcWwNv",
    "cryptosuite": "ecdsa-sd-2023",
    "proofPurpose": "assertionMethod",
    "proofValue": "u2V0AhVhAIC9hFSOtM2k0lFFuKclfp_cYTO5YWhZIYaMEPMcz1jloqTS0Zkww-Lc1U6FP15vJBaIa5ICMknDv16H8r0eh8VgjgCQDJUVkvejrCod7srzLsvKZEVUqzPULOZlb5-cwYdz0K8NYIJNls-gfevdbPuoczDW5TuctpSXJ7V9anf9MrkmJYP7ehVhARNoIdk_H3oT_8HxLP5Fo38e9blzlzSBmFswtxQUPzERVBXcgCU9k6c8pJz_RmjL0Y1eaW50Gl_qs_olK0u7NKlhAD3n7fkV5E-YF4KlodM7PhHP8_kB9you9XtTDVif3tyYsfWewmRysEN0A-EdLZ0WRwSwyJGBaBgGPb5erVUT-ElhAmLyoxIvE3GPC9rTc8tpfNEmTvcwBlpDGMlYkKb52XQeQeQFQwzgCPhpJowOomdMfPUq_xsHih8NsnDN0LXJtVFhArdqKKbPA-tMtA0mMQn1vIZ6mVjeTeJTsdxwZze2EspERwrMcgS25V-fVtjdEXCmNKyL7giUGy4eixjRGYowzpFhADobyi3ucf61IGgBM8_Vy1b8JkaiISFoy_i8ZldQfiqIoG00zU4-jEFuLWvsW7FGfPo0jq-2ZZBvS5H4SjaETJIFnL2lzc3Vlcg"
  }
}
```**application/vc**
            ```
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://www.w3.org/ns/credentials/examples/v2"
  ],
  "id": "http://university.example/credentials/3732",
  "type": [
    "VerifiableCredential",
    "ExampleDegreeCredential"
  ],
  "issuer": "https://university.example/issuers/565049",
  "validFrom": "2010-01-01T00:00:00Z",
  "credentialSubject": {
    "id": "did:example:ebfeb1f712ebc6f1c276e12ec21",
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
    "proofValue": "u2V0ChVhQkkdBby2GbmvVh66cM6TNzNfh0hR9ePeG7dWYbHfDxK6CcA_rVoxxsRGIoWX5Gs6ZGgQNPTBeehiEHT_cj-5fjZ6ArTluARHPbaXQzWyXKrVYQGd_DaMQQsoaryttl5TvxnFT-Vm4SkVx03K9qNJ4jhArS1r7HKFDPyyrvPGqNF8bjgNELvoomOjpbD9JEvaGI1pYYJVTGbTfcflzyx41E-f9kSqmf10xYzxJrGfC7b7GPY8X7VjMT__ZKSuwdH-5jak-5gkjocsHI6oxIKlLrhW1Wh5yrDCH-QC823TS8NE9VGBzIFAfUt5qazGEcJ8CxeSPxFgg_vwNGMCz741AWQhjph2NJJcybTTnmtmN1AZd15PefM6BZy9pc3N1ZXI"
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
  "id": "http://university.example/credentials/3732",
  "type": [
    "VerifiableCredential",
    "ExampleDegreeCredential"
  ],
  "issuer": "https://university.example/issuers/565049",
  "validFrom": "2010-01-01T00:00:00Z",
  "credentialSubject": {
    "id": "did:example:ebfeb1f712ebc6f1c276e12ec21",
    "degree": {
      "type": "ExampleBachelorDegree",
      "name": "Bachelor of Science and Arts"
    }
  }
}
```
**application/vc+jwt**


eyJraWQiOiJFeEhrQk1XOWZtYmt2VjI2Nm1ScHVQMnNVWV9OX0VXSU4xbGFwVXpPOHJvIiwiYWxnIjoiRVMyNTYifQ
.eyJAY29udGV4dCI6WyJodHRwczovL3d3dy53My5vcmcvbnMvY3JlZGVudGlhbHMvdjIiLCJodHRwczovL3d3dy53My5vcmcvbnMvY3JlZGVudGlhbHMvZXhhbXBsZXMvdjIiXSwiaWQiOiJodHRwOi8vdW5pdmVyc2l0eS5leGFtcGxlL2NyZWRlbnRpYWxzLzM3MzIiLCJ0eXBlIjpbIlZlcmlmaWFibGVDcmVkZW50aWFsIiwiRXhhbXBsZURlZ3JlZUNyZWRlbnRpYWwiXSwiaXNzdWVyIjoiaHR0cHM6Ly91bml2ZXJzaXR5LmV4YW1wbGUvaXNzdWVycy81NjUwNDkiLCJ2YWxpZEZyb20iOiIyMDEwLTAxLTAxVDAwOjAwOjAwWiIsImNyZWRlbnRpYWxTdWJqZWN0Ijp7ImlkIjoiZGlkOmV4YW1wbGU6ZWJmZWIxZjcxMmViYzZmMWMyNzZlMTJlYzIxIiwiZGVncmVlIjp7InR5cGUiOiJFeGFtcGxlQmFjaGVsb3JEZWdyZWUiLCJuYW1lIjoiQmFjaGVsb3Igb2YgU2NpZW5jZSBhbmQgQXJ0cyJ9fX0
.yLIZkNIu3N3b2JNM69FVtAD9C5iaw7qMRc5TG6Yl8yWUu9ql9cO2sUBzNSSSz7MfqW_PMXxpbqplMKsuheroaA


    


    
**application/vc**
```
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://www.w3.org/ns/credentials/examples/v2"
  ],
  "id": "http://university.example/credentials/3732",
  "type": [
    "VerifiableCredential",
    "ExampleDegreeCredential"
  ],
  "issuer": "https://university.example/issuers/565049",
  "validFrom": "2010-01-01T00:00:00Z",
  "credentialSubject": {
    "id": "did:example:ebfeb1f712ebc6f1c276e12ec21",
    "degree": {
      "type": "ExampleBachelorDegree",
      "name": "Bachelor of Science and Arts"
    }
  }
}
```
**application/vc+cose**

d28443a10128a05901be7b2240636f6e74657874223a5b2268747470733a2f2f7777772e77332e6f72672f6e732f63726564656e7469616c732f7632222c2268747470733a2f2f7777772e77332e6f72672f6e732f63726564656e7469616c732f6578616d706c65732f7632225d2c226964223a22687474703a2f2f756e69766572736974792e6578616d706c652f63726564656e7469616c732f33373332222c2274797065223a5b2256657269666961626c6543726564656e7469616c222c224578616d706c6544656772656543726564656e7469616c225d2c22697373756572223a2268747470733a2f2f756e69766572736974792e6578616d706c652f697373756572732f353635303439222c2276616c696446726f6d223a22323031302d30312d30315430303a30303a30305a222c2263726564656e7469616c5375626a656374223a7b226964223a226469643a6578616d706c653a656266656231663731326562633666316332373665313265633231222c22646567726565223a7b2274797065223a224578616d706c6542616368656c6f72446567726565222c226e616d65223a2242616368656c6f72206f6620536369656e636520616e642041727473227d7d7d58402c8dcd949c0418cf1b489b94632ccaea624331ad4881b15e5c3fddb34d86a5128f5442cd5603f3a0a8d8282ac7b13090c79249b048e3433e9eebfed1d0407adf

    


    
    
    
    
      - 
        Encoded
      
      - 
        Decoded
      
      - 
        Issuer Disclosures
      
    
    
      

eyJraWQiOiJFeEhrQk1XOWZtYmt2VjI2Nm1ScHVQMnNVWV9OX0VXSU4xbGFwVXpPOHJvIiwiYWxnIjoiRVMyNTYifQ
.eyJpYXQiOjE3NDU3NzY3MTMsImV4cCI6MTc0Njk4NjMxMywiX3NkX2FsZyI6InNoYS0yNTYiLCJAY29udGV4dCI6WyJodHRwczovL3d3dy53My5vcmcvbnMvY3JlZGVudGlhbHMvdjIiLCJodHRwczovL3d3dy53My5vcmcvbnMvY3JlZGVudGlhbHMvZXhhbXBsZXMvdjIiXSwiaXNzdWVyIjoiaHR0cHM6Ly91bml2ZXJzaXR5LmV4YW1wbGUvaXNzdWVycy81NjUwNDkiLCJ2YWxpZEZyb20iOiIyMDEwLTAxLTAxVDAwOjAwOjAwWiIsImNyZWRlbnRpYWxTdWJqZWN0Ijp7ImRlZ3JlZSI6eyJuYW1lIjoiQmFjaGVsb3Igb2YgU2NpZW5jZSBhbmQgQXJ0cyIsIl9zZCI6WyJEUkg1aWVsZHdHNXJPMlVQNXlYYlBXWHNTaFFNSmxESlJfZlFVbmhZVDNFIl19LCJfc2QiOlsiUzRvTGpDb0dNckpuMnFFR2lXY1JNNmdFNGZ6cVVFcVIzNC1FOWdjZzIyWSJdfSwiX3NkIjpbIlZtWnFMMkpKUFB0RDk2TmxwNE43TzFRMXhFRmNMZ1hCVzVfQWFGQXp4Sm8iLCJaYTdxRkpZSnRSTExSOFNRT1VUYUxwaDZBY21QSGlYVkc5Ni03Wnp3MEtJIl19
.ypl46Q1EqUERV-IUUS_-qGoAESfv_WdXwtHOk2vX7QTZNFf0NNfg-w2OR8JPRe97kZBDQLuBZKPJhBXdFjbSwg
~WyIxeDVielRkZXhsLW4zWVVIQXF5ZUxBIiwgImlkIiwgImh0dHA6Ly91bml2ZXJzaXR5LmV4YW1wbGUvY3JlZGVudGlhbHMvMzczMiJd~WyJablVReVZXRmo0UlFfTHFmOVBkbmN3IiwgInR5cGUiLCBbIlZlcmlmaWFibGVDcmVkZW50aWFsIiwgIkV4YW1wbGVEZWdyZWVDcmVkZW50aWFsIl1d~WyI5TG1nOHhaUVJxWEZZaVRlV0hRZjV3IiwgImlkIiwgImRpZDpleGFtcGxlOmViZmViMWY3MTJlYmM2ZjFjMjc2ZTEyZWMyMSJd~WyJZMVBDaVA3YnJ3TjFHMEVMWmJXRlZRIiwgInR5cGUiLCAiRXhhbXBsZUJhY2hlbG9yRGVncmVlIl0~

    
    
      ```
{  "kid": "ExHkBMW9fmbkvV266mRpuP2sUY_N_EWIN1lapUzO8ro",  "alg": "ES256"}
```
      ```
{  "iat": 1745776713,  "exp": 1746986313,  "_sd_alg": "sha-256",  "@context": [    "https://www.w3.org/ns/credentials/v2",    "https://www.w3.org/ns/credentials/examples/v2"  ],  "issuer": "https://university.example/issuers/565049",  "validFrom": "2010-01-01T00:00:00Z",  "credentialSubject": {    "degree": {      "name": "Bachelor of Science and Arts",      "_sd": [        "DRH5ieldwG5rO2UP5yXbPWXsShQMJlDJR_fQUnhYT3E"      ]    },    "_sd": [      "S4oLjCoGMrJn2qEGiWcRM6gE4fzqUEqR34-E9gcg22Y"    ]  },  "_sd": [    "VmZqL2JJPPtD96Nlp4N7O1Q1xEFcLgXBW5_AaFAzxJo",    "Za7qFJYJtRLLR8SQOUTaLph6AcmPHiXVG96-7Zzw0KI"  ]}
```
