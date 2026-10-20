---
name: "w3c-vcdm-issuer"
description: "Use when implementing issuer representation in W3C VCDM. Covers: issuer property requirements, syntax options, and issuer-related processing expectations."
sections:
  - "4.7 Issuer"
---

<!-- ARF version: 2.0-2024-12-04 -->
<!-- Tokens: ~5157 -->

### 4.7 Issuer
        

        
This specification defines a property for expressing the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) of
a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential).
        

        
A [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) MUST have an `issuer` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property).
        

        
          issuer
          
The value of the `issuer` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) MUST be either a [URL](https://www.w3.org/TR/vc-data-model-2.0/#dfn-url) or an object
containing an `id` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) whose value is a [URL](https://www.w3.org/TR/vc-data-model-2.0/#dfn-url); in either case, the
issuer selects this [URL](https://www.w3.org/TR/vc-data-model-2.0/#dfn-url) to identify itself in a globally unambiguous way. It
is RECOMMENDED that the [URL](https://www.w3.org/TR/vc-data-model-2.0/#dfn-url) be one which, if dereferenced, results in a
controlled identifier document, as defined in the [Controlled Identifiers v1.0](https://www.w3.org/TR/cid-1.0/) specification,
about the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) that can be used to [verify](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verify) the information expressed
in the [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential).
          
        

        
        
    [Example 7](https://www.w3.org/TR/vc-data-model-2.0/#example-use-of-the-issuer-property): Use of the issuer property
   
      - Credential- ecdsa- ecdsa-sd- bbs- jose- cose- sd-jwt```
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
  "issuer": "https://university.example/issuers/14",
  "validFrom": "2010-01-01T19:23:24Z",
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
    "proofValue": "z3sXkg3PHbK2YpbhQajunUvReW3Qn66mPsQQKvn4hwEG1DohgUqvXBF2oKT5Qb8tKSKjewNhsJCCcBoY6Rfye4ipw"
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
  "issuer": "https://university.example/issuers/14",
  "validFrom": "2010-01-01T19:23:24Z",
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
    "proofValue": "u2V0AhVhA91jcz-MSzf_Z-fw6VM-YN1ijTr26VBTz9H14dMiv6t5vRaGC1IKHvDtY0ZJup1pnliukZBHEXgM46Bf4EjdyIFgjgCQDMIFZRjI7aJUGGsbDYML33eEwJuub6dIF5agqeB4sTdJYIAhgKXoAudJOwmVRpO2Ab5sNIirjQdArIjp8ygMx2S5ihVhASWfZk4fYqoICvoaokYzsABtmDzpgTe8ZkI2z4MDKt1wcp0T9tBx30mk1V20Qhy2PT15nrPygrxpn8_h2Z1Jo7FhAXNmEd28tsb_VkmqckvjVBet7p8Hhq7d8DziDldJRri8-cygIdcaX0MsitDRMsclHCsO25UKSjCX96dSto_Y3FVhAeYhHIz52Lw3Fd8tO7rdPOjILauPLHFkRnmHbd8ixxKwb62gTqchavN3rv8GtKxQL9o-cLCKFm-mpQDUABuYxMVhA-vKFPcx_bNem4ufrFDr-cyjUa3r-zjLJwp9xss7XZikI3PLiiMGIBnhhGs3zCsQXvSZMX6ScPOpog6Kzl-YSj1hA7xtSv3lNDKhPKKQ-7F4WHhmfwj0F1PN_mj5jDkJcdw19eYTux4wRXgehBXRtvkuMw9iG6UFyurMFeyb-EkmQPIFnL2lzc3Vlcg"
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
  "issuer": "https://university.example/issuers/14",
  "validFrom": "2010-01-01T19:23:24Z",
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
    "proofValue": "u2V0ChVhQs4LnYe9N1n9fBW8t7tgXy8gZA1WksN76TfdxHLUW0cJlImiaNZZbbNwAaL86-8xnTgMJgpwaMchm_8VepMSYZKjfQReWnOfwRfwz8grbaNNYQGd_DaMQQsoaryttl5TvxnFT-Vm4SkVx03K9qNJ4jhArKnv3N5iX7nvZR0OCXS-uXH4QQ9mW65QM5qlHOfE4GQVYYJVTGbTfcflzyx41E-f9kSqmf10xYzxJrGfC7b7GPY8X7VjMT__ZKSuwdH-5jak-5gkjocsHI6oxIKlLrhW1Wh5yrDCH-QC823TS8NE9VGBzIFAfUt5qazGEcJ8CxeSPxFggO3rpYlZcra0jsUsWXIoCAXrkmj3mb1o1k8CYE2Wx9d6BZy9pc3N1ZXI"
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
  "issuer": "https://university.example/issuers/14",
  "validFrom": "2010-01-01T19:23:24Z",
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
.eyJAY29udGV4dCI6WyJodHRwczovL3d3dy53My5vcmcvbnMvY3JlZGVudGlhbHMvdjIiLCJodHRwczovL3d3dy53My5vcmcvbnMvY3JlZGVudGlhbHMvZXhhbXBsZXMvdjIiXSwiaWQiOiJodHRwOi8vdW5pdmVyc2l0eS5leGFtcGxlL2NyZWRlbnRpYWxzLzM3MzIiLCJ0eXBlIjpbIlZlcmlmaWFibGVDcmVkZW50aWFsIiwiRXhhbXBsZURlZ3JlZUNyZWRlbnRpYWwiXSwiaXNzdWVyIjoiaHR0cHM6Ly91bml2ZXJzaXR5LmV4YW1wbGUvaXNzdWVycy8xNCIsInZhbGlkRnJvbSI6IjIwMTAtMDEtMDFUMTk6MjM6MjRaIiwiY3JlZGVudGlhbFN1YmplY3QiOnsiaWQiOiJkaWQ6ZXhhbXBsZTplYmZlYjFmNzEyZWJjNmYxYzI3NmUxMmVjMjEiLCJkZWdyZWUiOnsidHlwZSI6IkV4YW1wbGVCYWNoZWxvckRlZ3JlZSIsIm5hbWUiOiJCYWNoZWxvciBvZiBTY2llbmNlIGFuZCBBcnRzIn19fQ
.lTz4nWXqYIiQ0bm_t26FD3GHibp2HVinvyPI6wezRaPURX2KaGSas2v4yaRFhpEyni3hLFc_L2ZhWJXcDWnyUQ


    


    
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
  "issuer": "https://university.example/issuers/14",
  "validFrom": "2010-01-01T19:23:24Z",
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

d28443a10128a05901ba7b2240636f6e74657874223a5b2268747470733a2f2f7777772e77332e6f72672f6e732f63726564656e7469616c732f7632222c2268747470733a2f2f7777772e77332e6f72672f6e732f63726564656e7469616c732f6578616d706c65732f7632225d2c226964223a22687474703a2f2f756e69766572736974792e6578616d706c652f63726564656e7469616c732f33373332222c2274797065223a5b2256657269666961626c6543726564656e7469616c222c224578616d706c6544656772656543726564656e7469616c225d2c22697373756572223a2268747470733a2f2f756e69766572736974792e6578616d706c652f697373756572732f3134222c2276616c696446726f6d223a22323031302d30312d30315431393a32333a32345a222c2263726564656e7469616c5375626a656374223a7b226964223a226469643a6578616d706c653a656266656231663731326562633666316332373665313265633231222c22646567726565223a7b2274797065223a224578616d706c6542616368656c6f72446567726565222c226e616d65223a2242616368656c6f72206f6620536369656e636520616e642041727473227d7d7d58405ecf7be0f23f3ed8bf173e4895c70f7dad9fb36628730d78a37aa499cbf1ef8263a4def9303e5de3783c7ae69884fcdafc924ee676ec232d8f51488fee4cdbc5

    


    
    
    
    
      - 
        Encoded
      
      - 
        Decoded
      
      - 
        Issuer Disclosures
      
    
    
      

eyJraWQiOiJFeEhrQk1XOWZtYmt2VjI2Nm1ScHVQMnNVWV9OX0VXSU4xbGFwVXpPOHJvIiwiYWxnIjoiRVMyNTYifQ
.eyJpYXQiOjE3NDU3NzY3MTMsImV4cCI6MTc0Njk4NjMxMywiX3NkX2FsZyI6InNoYS0yNTYiLCJAY29udGV4dCI6WyJodHRwczovL3d3dy53My5vcmcvbnMvY3JlZGVudGlhbHMvdjIiLCJodHRwczovL3d3dy53My5vcmcvbnMvY3JlZGVudGlhbHMvZXhhbXBsZXMvdjIiXSwiaXNzdWVyIjoiaHR0cHM6Ly91bml2ZXJzaXR5LmV4YW1wbGUvaXNzdWVycy8xNCIsInZhbGlkRnJvbSI6IjIwMTAtMDEtMDFUMTk6MjM6MjRaIiwiY3JlZGVudGlhbFN1YmplY3QiOnsiZGVncmVlIjp7Im5hbWUiOiJCYWNoZWxvciBvZiBTY2llbmNlIGFuZCBBcnRzIiwiX3NkIjpbImN4X0JsU2pRSVp6bjN5aFRhc0pEeGhLZVlrcndLc25fLXc1RGFKVVdNYmMiXX0sIl9zZCI6WyJOcm96NFFQRHFTOGZkdVI0bDFQaFZwS3l6aFJzN2xha3VlQUZDMmhNa2hzIl19LCJfc2QiOlsiSk84RmdIYmVuLVdlOHJvUDBiM09uV1hrVHZSMlYzOXRTSllzdmpiTy12cyIsImhvckxSUTVqbHpNcFktWDdKMXA1Wmh4UXNNNmMyaHhoZXNjUnF0RnRQSDgiXX0
.DVnk8KsBnPp-Z9vnpReTasbST4ENcNjOwn9qxCgDx7H33VsJaFi0DyCa2auVKb1oSL0IilelgxsEVs27fMClSA
~WyJoSEtXaHpnQ1k0VUJ0Z1F1V2ZWQjNBIiwgImlkIiwgImh0dHA6Ly91bml2ZXJzaXR5LmV4YW1wbGUvY3JlZGVudGlhbHMvMzczMiJd~WyJUeHZFNURzNU5OT190S0VnMUsyZnlBIiwgInR5cGUiLCBbIlZlcmlmaWFibGVDcmVkZW50aWFsIiwgIkV4YW1wbGVEZWdyZWVDcmVkZW50aWFsIl1d~WyJlUkpwYkw3WHZ2SVVwVnVGLWlLUWNnIiwgImlkIiwgImRpZDpleGFtcGxlOmViZmViMWY3MTJlYmM2ZjFjMjc2ZTEyZWMyMSJd~WyJwb2o5UDctRG5MYzF3VVBSbHpkXy1nIiwgInR5cGUiLCAiRXhhbXBsZUJhY2hlbG9yRGVncmVlIl0~

    
    
      ```
{  "kid": "ExHkBMW9fmbkvV266mRpuP2sUY_N_EWIN1lapUzO8ro",  "alg": "ES256"}
```
      ```
{  "iat": 1745776713,  "exp": 1746986313,  "_sd_alg": "sha-256",  "@context": [    "https://www.w3.org/ns/credentials/v2",    "https://www.w3.org/ns/credentials/examples/v2"  ],  "issuer": "https://university.example/issuers/14",  "validFrom": "2010-01-01T19:23:24Z",  "credentialSubject": {    "degree": {      "name": "Bachelor of Science and Arts",      "_sd": [        "cx_BlSjQIZzn3yhTasJDxhKeYkrwKsn_-w5DaJUWMbc"      ]    },    "_sd": [      "Nroz4QPDqS8fduR4l1PhVpKyzhRs7lakueAFC2hMkhs"    ]  },  "_sd": [    "JO8FgHben-We8roP0b3OnWXkTvR2V39tSJYsvjbO-vs",    "horLRQ5jlzMpY-X7J1p5ZhxQsM6c2hxhescRqtFtPH8"  ]}
```
