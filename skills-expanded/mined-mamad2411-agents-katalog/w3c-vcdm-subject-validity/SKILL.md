---
name: "w3c-vcdm-subject-validity"
description: "Use when modeling credential subject data in W3C VCDM. Covers: credentialSubject structure and semantics."
sections:
  - "4.8 Credential Subject"
---

<!-- ARF version: 2.0-2024-12-04 -->
<!-- Tokens: ~5191 -->

### 4.8 Credential Subject
        

        
A [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) contains [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) about one or more [subjects](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects).
This specification defines a `credentialSubject` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) for the expression
of [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) about one or more [subjects](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects).
        

        
A [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) MUST contain a `credentialSubject` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property).
        

        
          credentialSubject
          
The value of the `credentialSubject` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) is a set of objects where each
object MUST be the [subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects) of one or more [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims), which MUST be
serialized inside the `credentialSubject` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property). Each object MAY also
contain an `id` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) to identify the [subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects), as described in
Section [4.4 Identifiers](https://www.w3.org/TR/vc-data-model-2.0/#identifiers).
          
        

        
        
    [Example 9](https://www.w3.org/TR/vc-data-model-2.0/#example-use-of-the-credentialsubject-property): Use of the credentialSubject property
   
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
    "created": "2025-04-27T17:58:34Z",
    "verificationMethod": "did:key:zDnaebSRtPnW6YCpxAhR5JPxJqt9UunCsBPhLEtUokUvp87nQ",
    "cryptosuite": "ecdsa-rdfc-2019",
    "proofPurpose": "assertionMethod",
    "proofValue": "z36CTYymphefPFDdFakYBe7EHHX7Upev5vtRhxG3ZtKiUPXFKknW9ZTds3wxDhTz1WFCGzFUUv6DC5vifg3VCCSFL"
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
    "created": "2025-04-27T17:58:34Z",
    "verificationMethod": "did:key:zDnaerJh8WwyBVVGcZKKkqRKK9iezje8ut6t9bnNChtxcWwNv",
    "cryptosuite": "ecdsa-sd-2023",
    "proofPurpose": "assertionMethod",
    "proofValue": "u2V0AhVhAFPsovbuHDInv8ft0M6jMPGrLrNs9j_sEfn1gdDCxFOmyjYDyblufuagmARZj9RabxfO0SkbpUi_m6dQdXIyoklgjgCQC78Ayc-2ykLAZ_NJzb5-S8dtSenHeKEHHGy469czIbhtYILJ97_OhxkzZccWMaUgCAXRO5ZCyoagriazYdV2ViFsuhVhAvGcG2tqQoB5VaC-x652sos00_94wzBOZg9wGR2mytwn_alXEbksbCMUC2lmiU_FrcFzEEAZrAdcsAfoE0J_KRlhAc71QXbdP2iKlqmgocH4qvDcv_3PT_VmSFGWISFdrQPkmv2lb2r9Mb02yZYilf20oMzCPCRsqYP--0g8ysm9doVhAIqwWkfg1pXXKaxx4_5_QpmoOoXjLPNhJ-14QSHUyxTKKCTarm33OdaIhhCjm5_e7MUCYHvA89vCSvSHMrKvKclhASFp1GivaJXYrbBcM6xNFNsXW7xBg7cZXfBeGOwcXf7fXg1GwMJILZBimOaEM5Eay38F8T6HwbeuMvBQ7b05gbFhAkLeI8-tdeQQzX6ik0xDSM4yLsHPmhG47Tu5Hm25ujoo9iVsLzskiGcIsQLsqvRK5238FvPQAeOpK04R7F2aK9IFnL2lzc3Vlcg"
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
    "proofValue": "u2V0ChVhQkkdBby2GbmvVh66cM6TNzNfh0hR9ePeG7dWYbHfDxK6CcA_rVoxxsRGIoWX5Gs6ZGgQNPTBeehiEHT_cj-5fjZ6ArTluARHPbaXQzWyXKrVYQGd_DaMQQsoaryttl5TvxnFT-Vm4SkVx03K9qNJ4jhArS1r7HKFDPyyrvPGqNF8bjgNELvoomOjpbD9JEvaGI1pYYJVTGbTfcflzyx41E-f9kSqmf10xYzxJrGfC7b7GPY8X7VjMT__ZKSuwdH-5jak-5gkjocsHI6oxIKlLrhW1Wh5yrDCH-QC823TS8NE9VGBzIFAfUt5qazGEcJ8CxeSPxFggUfIz7Xi8QhNU6pC7qIkL0HkvpKYuV2rzBuKizKrBhU6BZy9pc3N1ZXI"
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
.KJnv5DRpXi0xZ6SUSXsu30Xs5OBk8HlunnpkAitIS677TBPhwX1cgbUj9nTuLfNeLlRZnsCyua_yZZ5SooTKSw


    


    
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

d28443a10128a05901be7b2240636f6e74657874223a5b2268747470733a2f2f7777772e77332e6f72672f6e732f63726564656e7469616c732f7632222c2268747470733a2f2f7777772e77332e6f72672f6e732f63726564656e7469616c732f6578616d706c65732f7632225d2c226964223a22687474703a2f2f756e69766572736974792e6578616d706c652f63726564656e7469616c732f33373332222c2274797065223a5b2256657269666961626c6543726564656e7469616c222c224578616d706c6544656772656543726564656e7469616c225d2c22697373756572223a2268747470733a2f2f756e69766572736974792e6578616d706c652f697373756572732f353635303439222c2276616c696446726f6d223a22323031302d30312d30315430303a30303a30305a222c2263726564656e7469616c5375626a656374223a7b226964223a226469643a6578616d706c653a656266656231663731326562633666316332373665313265633231222c22646567726565223a7b2274797065223a224578616d706c6542616368656c6f72446567726565222c226e616d65223a2242616368656c6f72206f6620536369656e636520616e642041727473227d7d7d5840b1ddb83d2cc91513a6a44ae62b8c622918c9b78d1c6492afcec241b39a23cbd6f1c6efbdeeaa94e0c765b7c8b9284e2c930ae859aa0a2defc8b4d9fba132d23d

    


    
    
    
    
      - 
        Encoded
      
      - 
        Decoded
      
      - 
        Issuer Disclosures
      
    
    
      

eyJraWQiOiJFeEhrQk1XOWZtYmt2VjI2Nm1ScHVQMnNVWV9OX0VXSU4xbGFwVXpPOHJvIiwiYWxnIjoiRVMyNTYifQ
.eyJpYXQiOjE3NDU3NzY3MTQsImV4cCI6MTc0Njk4NjMxNCwiX3NkX2FsZyI6InNoYS0yNTYiLCJAY29udGV4dCI6WyJodHRwczovL3d3dy53My5vcmcvbnMvY3JlZGVudGlhbHMvdjIiLCJodHRwczovL3d3dy53My5vcmcvbnMvY3JlZGVudGlhbHMvZXhhbXBsZXMvdjIiXSwiaXNzdWVyIjoiaHR0cHM6Ly91bml2ZXJzaXR5LmV4YW1wbGUvaXNzdWVycy81NjUwNDkiLCJ2YWxpZEZyb20iOiIyMDEwLTAxLTAxVDAwOjAwOjAwWiIsImNyZWRlbnRpYWxTdWJqZWN0Ijp7ImRlZ3JlZSI6eyJuYW1lIjoiQmFjaGVsb3Igb2YgU2NpZW5jZSBhbmQgQXJ0cyIsIl9zZCI6WyJlU3NEMXVhcVNuZUdIVEVjTWxlM1ZzWlJwOHRNbmo1Q0dyN1EzandzdkZrIl19LCJfc2QiOlsiYU5MMTNnNnUtenN2VG1YVkFfOVRYdXlrSVdpRzd0djVvbExzdHNieDlkayJdfSwiX3NkIjpbIkRsMHp6eHZJcXA1TVdBNWEzSTJQRDFNQXJ3NlZBNFFMeWRscVNsSkVCeVkiLCJqVmtSaTdLMGUySTFkbFJURXREdlFVTEIxcWZaZ3NNcGlCdjVQYWsyMXlzIl19
.Yh2d9J3y-SKxa16vZzRVQKaya0V66OPIar-C9PGVzOu2Q7_0IbsYqTJxtNYsQ39fk64p1-QEgCmWPWHFRAD_qw
~WyIxTGVERC1tNlRQdlFXX1R4MU9MQVVnIiwgImlkIiwgImh0dHA6Ly91bml2ZXJzaXR5LmV4YW1wbGUvY3JlZGVudGlhbHMvMzczMiJd~WyJiU1ljSjZNVXdGZlhleWRGSl84dHlnIiwgInR5cGUiLCBbIlZlcmlmaWFibGVDcmVkZW50aWFsIiwgIkV4YW1wbGVEZWdyZWVDcmVkZW50aWFsIl1d~WyJpUGx3eUs1c01BY1BzbzZQbW1DNWl3IiwgImlkIiwgImRpZDpleGFtcGxlOmViZmViMWY3MTJlYmM2ZjFjMjc2ZTEyZWMyMSJd~WyJFaEt5VDV6ZjJuSGZUNHFnaWZtczVBIiwgInR5cGUiLCAiRXhhbXBsZUJhY2hlbG9yRGVncmVlIl0~

    
    
      ```
{  "kid": "ExHkBMW9fmbkvV266mRpuP2sUY_N_EWIN1lapUzO8ro",  "alg": "ES256"}
```
      ```
{  "iat": 1745776714,  "exp": 1746986314,  "_sd_alg": "sha-256",  "@context": [    "https://www.w3.org/ns/credentials/v2",    "https://www.w3.org/ns/credentials/examples/v2"  ],  "issuer": "https://university.example/issuers/565049",  "validFrom": "2010-01-01T00:00:00Z",  "credentialSubject": {    "degree": {      "name": "Bachelor of Science and Arts",      "_sd": [        "eSsD1uaqSneGHTEcMle3VsZRp8tMnj5CGr7Q3jwsvFk"      ]    },    "_sd": [      "aNL13g6u-zsvTmXVA_9TXuykIWiG7tv5olLstsbx9dk"    ]  },  "_sd": [    "Dl0zzxvIqp5MWA5a3I2PD1MArw6VA4QLydlqSlJEByY",    "jVkRi7K0e2I1dlRTEtDvQULB1qfZgsMpiBv5Pak21ys"  ]}
```
