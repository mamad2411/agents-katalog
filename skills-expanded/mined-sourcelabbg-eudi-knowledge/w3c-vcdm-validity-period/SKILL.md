---
name: "w3c-vcdm-validity-period"
description: "Use when implementing temporal validity in W3C VCDM. Covers: validity period semantics and related processing rules."
sections:
  - "4.9 Validity Period"
---

<!-- ARF version: 2.0-2024-12-04 -->
<!-- Tokens: ~5685 -->

### 4.9 Validity Period
        

        
This specification defines the `validFrom` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) to help an
issuer to express the date and time when a [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) becomes valid and
the `validUntil` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) to express the date and time
when a [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) ceases to be valid.
        

        
When comparing dates and times, the calculation is done "temporally",
meaning that the string value is converted to a "temporal value" which exists
as a point on a timeline. Temporal comparisons are then performed by checking
to see where the date and time being compared are in relation to
a particular point on the timeline.
        

        
          validFrom
          
If present, the value of the `validFrom` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) MUST be a
[[XMLSCHEMA11-2](https://www.w3.org/TR/xmlschema11-2/#dateTime)]
`dateTimeStamp` string value representing the date and time the
[credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) becomes valid, which could be a date and time in the future or
the past. Note that this value represents the earliest point in time at which
the information associated with the `credentialSubject`
[property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) becomes valid. If a `validUntil` value also exists, the
`validFrom` value MUST express a point in time that is temporally the same or
earlier than the point in time expressed by the `validUntil` value.
          
          validUntil
          
If present, the value of the `validUntil` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) MUST be a
[[XMLSCHEMA11-2](https://www.w3.org/TR/xmlschema11-2/#dateTimeStamp)]
`dateTimeStamp` string value representing the date and time the
[credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) ceases to be valid, which could be a date and time in the past
or the future. Note that this value represents the latest point in time at
which the information associated with the `credentialSubject`
[property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) is valid. If a `validFrom` value also exists, the `validUntil`
value MUST express a point in time that is temporally the same or later than the
point in time expressed by the `validFrom` value.
          
        

        
        
    [Example 11](https://www.w3.org/TR/vc-data-model-2.0/#example-use-of-the-validfrom-and-validuntil-properties): Use of the validFrom and validUntil properties
   
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
  "validUntil": "2020-01-01T19:23:24Z",
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
  "validUntil": "2020-01-01T19:23:24Z",
  "credentialSubject": {
    "id": "did:example:ebfeb1f712ebc6f1c276e12ec21",
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
    "proofValue": "z65sN9W58eruTDUUXYxxwhG4cQ73zQkQuhMYvUVipeM4oEUBPbCxd3oTQTJhnfHN9juyZSzYpERYFjZcfpb2xgeto"
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
  "validUntil": "2020-01-01T19:23:24Z",
  "credentialSubject": {
    "id": "did:example:ebfeb1f712ebc6f1c276e12ec21",
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
    "proofValue": "u2V0AhVhAxWvPP0HD9usaRDFthqpz1zXbWtTpNr_1pRFMKY9wbt7RAh0kwkoqR9cFHY0PdBj0cPo9BXd_54Z9iLl7GsmAjlgjgCQCJ0FUx3YRbBxybCrTEtFINFNKD7UC2j8tjmvYa6EQKlNYIL-KVtIrAWQi98Ng86FB4giy2xKCqn_kNOmO75D7AQfEhlhA5pKNMOahYQbk8obEMFyLgAsmd3FGqf3FoDTojybRWUPf7F3A22Kl1822zW093-XtKum7Nfe3q16norHXUnhkWVhAvNR9By8I5ISJtylSp1fkzurbIvSXVhkaj4wsUpbTy1GnYHzeS7qhAyUoO4GkIMUfP3yLS0BIGBbJR7de1s5G4lhATnwFdztYAEXk6z93jJot3TPhlnOYk10G0e7u3uyJJF-ZrAsctOYbjF3ZcNZu3UXJZRe4_ytxr5OqwIVLnUfDqFhAkff2_b4hqpz0uK0kDHjkpMun4mAhuxVCjcmyIlJnaaTdFc2RovLnKiPx4Xnd9P_lOd3ZQoz5ThPWzMS7r_43M1hAmVVtNJ7-lpJdlc9tg5e3GpAhnXzYHpiv3WRRT3F4tH8B_zkHnyeNBT61d16TTnvlFn5mFXJ99FD4abIcQkyP_lhA8IS9pAGKqVgTDzxXSvGcGWMXQ4LEy3jfywyDpdiZodvttNhuZVBMkGKhNBo94oGjIHRfoeAFvQfZQo8_ENtBEYFnL2lzc3Vlcg"
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
  "validUntil": "2020-01-01T19:23:24Z",
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
    "proofValue": "u2V0ChVhQjBPG4AXIRGKu6h5awRiAZHSrx5gfUdbWc2rAxdsfIzSIywzsphRnlb5rPDWwdJlBF5krx4JRYNtT7exHHAw_aZtO6AARXGfbz0eHNrcTKL5YQGd_DaMQQsoaryttl5TvxnFT-Vm4SkVx03K9qNJ4jhArKnv3N5iX7nvZR0OCXS-uXH4QQ9mW65QM5qlHOfE4GQVYYJVTGbTfcflzyx41E-f9kSqmf10xYzxJrGfC7b7GPY8X7VjMT__ZKSuwdH-5jak-5gkjocsHI6oxIKlLrhW1Wh5yrDCH-QC823TS8NE9VGBzIFAfUt5qazGEcJ8CxeSPxFggWjulaLj5whA4VZOvBqHQbwhSW7Ph0eZ2bxz7ota_qnCBZy9pc3N1ZXI"
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
  "validUntil": "2020-01-01T19:23:24Z",
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
.eyJAY29udGV4dCI6WyJodHRwczovL3d3dy53My5vcmcvbnMvY3JlZGVudGlhbHMvdjIiLCJodHRwczovL3d3dy53My5vcmcvbnMvY3JlZGVudGlhbHMvZXhhbXBsZXMvdjIiXSwiaWQiOiJodHRwOi8vdW5pdmVyc2l0eS5leGFtcGxlL2NyZWRlbnRpYWxzLzM3MzIiLCJ0eXBlIjpbIlZlcmlmaWFibGVDcmVkZW50aWFsIiwiRXhhbXBsZURlZ3JlZUNyZWRlbnRpYWwiXSwiaXNzdWVyIjoiaHR0cHM6Ly91bml2ZXJzaXR5LmV4YW1wbGUvaXNzdWVycy8xNCIsInZhbGlkRnJvbSI6IjIwMTAtMDEtMDFUMTk6MjM6MjRaIiwidmFsaWRVbnRpbCI6IjIwMjAtMDEtMDFUMTk6MjM6MjRaIiwiY3JlZGVudGlhbFN1YmplY3QiOnsiaWQiOiJkaWQ6ZXhhbXBsZTplYmZlYjFmNzEyZWJjNmYxYzI3NmUxMmVjMjEiLCJkZWdyZWUiOnsidHlwZSI6IkV4YW1wbGVCYWNoZWxvckRlZ3JlZSIsIm5hbWUiOiJCYWNoZWxvciBvZiBTY2llbmNlIGFuZCBBcnRzIn19fQ
.UGJHic3E0XIwnJnzsQPF49ZMJsJtVhQSYTk7m8uvpbQWQPIttHiQo8k2qVhNZiRtMDLuIYAdTjim8rhGZbCJ2A


    


    
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
  "validUntil": "2020-01-01T19:23:24Z",
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

d28443a10128a05901de7b2240636f6e74657874223a5b2268747470733a2f2f7777772e77332e6f72672f6e732f63726564656e7469616c732f7632222c2268747470733a2f2f7777772e77332e6f72672f6e732f63726564656e7469616c732f6578616d706c65732f7632225d2c226964223a22687474703a2f2f756e69766572736974792e6578616d706c652f63726564656e7469616c732f33373332222c2274797065223a5b2256657269666961626c6543726564656e7469616c222c224578616d706c6544656772656543726564656e7469616c225d2c22697373756572223a2268747470733a2f2f756e69766572736974792e6578616d706c652f697373756572732f3134222c2276616c696446726f6d223a22323031302d30312d30315431393a32333a32345a222c2276616c6964556e74696c223a22323032302d30312d30315431393a32333a32345a222c2263726564656e7469616c5375626a656374223a7b226964223a226469643a6578616d706c653a656266656231663731326562633666316332373665313265633231222c22646567726565223a7b2274797065223a224578616d706c6542616368656c6f72446567726565222c226e616d65223a2242616368656c6f72206f6620536369656e636520616e642041727473227d7d7d584076a5f6a774019f85df7b204233f02dcd34fcaa896191e0c41cc6e78f2c4c7d9456daf472970ee8bd3993474bc31f975df3278e844ed6707486b77e928fbd7231

    


    
    
    
    
      - 
        Encoded
      
      - 
        Decoded
      
      - 
        Issuer Disclosures
      
    
    
      

eyJraWQiOiJFeEhrQk1XOWZtYmt2VjI2Nm1ScHVQMnNVWV9OX0VXSU4xbGFwVXpPOHJvIiwiYWxnIjoiRVMyNTYifQ
.eyJpYXQiOjE3NDU3NzY3MTQsImV4cCI6MTc0Njk4NjMxNCwiX3NkX2FsZyI6InNoYS0yNTYiLCJAY29udGV4dCI6WyJodHRwczovL3d3dy53My5vcmcvbnMvY3JlZGVudGlhbHMvdjIiLCJodHRwczovL3d3dy53My5vcmcvbnMvY3JlZGVudGlhbHMvZXhhbXBsZXMvdjIiXSwiaXNzdWVyIjoiaHR0cHM6Ly91bml2ZXJzaXR5LmV4YW1wbGUvaXNzdWVycy8xNCIsInZhbGlkRnJvbSI6IjIwMTAtMDEtMDFUMTk6MjM6MjRaIiwidmFsaWRVbnRpbCI6IjIwMjAtMDEtMDFUMTk6MjM6MjRaIiwiY3JlZGVudGlhbFN1YmplY3QiOnsiZGVncmVlIjp7Im5hbWUiOiJCYWNoZWxvciBvZiBTY2llbmNlIGFuZCBBcnRzIiwiX3NkIjpbInRreDZVVzN3VF9OcVRpeHZWR2tzd2RaRi1rQkE0TmhBV1pHSmxhUURpREkiXX0sIl9zZCI6WyJmTmpEU0RIbDNIQkNTQ1hSRzh0OWJud1RIMUpTT0JQOE0wWmFaQlpQTmNJIl19LCJfc2QiOlsiUHhTdmNMelpvam1Lck5qMWVKWDNxVjZKcVoxdFBVV1dYMFo5Q2dLRTlEVSIsInRTSThIellYN2RYdHhpMVc3UHUxckg4S3ZFNUxBRkNEVVNxcHpsbmdzRDgiXX0
.4gc3oF3a-OHOSwVC1eiCZP-ureWU-bdPdjBlL-xBjUsE5qL2sBQbg5PP_CO6JgZiBONpr3iU6cL0MF9iPpu9Eg
~WyJ3SzVZQTBEZzRoc18wdmtFZk1ENG93IiwgImlkIiwgImh0dHA6Ly91bml2ZXJzaXR5LmV4YW1wbGUvY3JlZGVudGlhbHMvMzczMiJd~WyJ1T0podHZvMEJ0cm1YbWxIeUVKUTdRIiwgInR5cGUiLCBbIlZlcmlmaWFibGVDcmVkZW50aWFsIiwgIkV4YW1wbGVEZWdyZWVDcmVkZW50aWFsIl1d~WyJjTzBQZjZxM1MweHp2dmRwS25aWlpnIiwgImlkIiwgImRpZDpleGFtcGxlOmViZmViMWY3MTJlYmM2ZjFjMjc2ZTEyZWMyMSJd~WyI0N0FDOWhlLTRCNW4xV1N0dFJRYXRBIiwgInR5cGUiLCAiRXhhbXBsZUJhY2hlbG9yRGVncmVlIl0~

    
    
      ```
{  "kid": "ExHkBMW9fmbkvV266mRpuP2sUY_N_EWIN1lapUzO8ro",  "alg": "ES256"}
```
      ```
{  "iat": 1745776714,  "exp": 1746986314,  "_sd_alg": "sha-256",  "@context": [    "https://www.w3.org/ns/credentials/v2",    "https://www.w3.org/ns/credentials/examples/v2"  ],  "issuer": "https://university.example/issuers/14",  "validFrom": "2010-01-01T19:23:24Z",  "validUntil": "2020-01-01T19:23:24Z",  "credentialSubject": {    "degree": {      "name": "Bachelor of Science and Arts",      "_sd": [        "tkx6UW3wT_NqTixvVGkswdZF-kBA4NhAWZGJlaQDiDI"      ]    },    "_sd": [      "fNjDSDHl3HBCSCXRG8t9bnwTH1JSOBP8M0ZaZBZPNcI"    ]  },  "_sd": [    "PxSvcLzZojmKrNj1eJX3qV6JqZ1tPUWWX0Z9CgKE9DU",    "tSI8HzYX7dXtxi1W7Pu1rH8KvE5LAFCDUSqpzlngsD8"  ]}
```
