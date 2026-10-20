---
name: "w3c-vcdm-identifiers-types"
description: "Use when working with identifiers and types in W3C VCDM. Covers: identifier modeling rules and URI usage across credentials and presentations."
sections:
  - "4.4 Identifiers"
---

<!-- ARF version: 2.0-2024-12-04 -->
<!-- Tokens: ~5519 -->

### 4.4 Identifiers
        

        
When expressing statements about a specific thing, such as a person, product, or
organization, using a globally unique identifier for that thing can be useful.
Globally unique identifiers enable others to express statements
about the same thing. This specification defines the optional `id`
[property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) for such identifiers. The `id` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property)
allows for expressing statements about specific things in the
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) and is set by an [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) when expressing
objects in a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) or a [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) when expressing
objects in a [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation). The `id` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) expresses an
identifier that others are expected to use when expressing statements about the
specific thing identified by that identifier. Example `id` values
include UUIDs (`urn:uuid:0c07c1ce-57cb-41af-bef2-1b932b986873`), HTTP URLs
(`https://id.example/things#123`), and DIDs (`did:example:1234abcd`).
        

        Note: Identifiers of any kind increase correlatability
Developers are reminded that identifiers might be harmful
when pseudonymity is required. When considering such scenarios, developers are
encouraged to read Section [8.4 Identifier-Based Correlation](https://www.w3.org/TR/vc-data-model-2.0/#identifier-based-correlation) carefully
There are also other types of access and correlation mechanisms documented
in Section [8. Privacy Considerations](https://www.w3.org/TR/vc-data-model-2.0/#privacy-considerations) that create privacy concerns.
Where privacy is a vital consideration, it is permissible to omit the
`id` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property). Some use cases do not need or explicitly need to omit,
the `id` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property). Similarly, special attention is to be given to the choice
between publicly resolvable URLs and other forms of identifiers. Publicly
resolvable URLs can facilitate ease of verification and interoperability, yet
they might also inadvertently grant access to potentially sensitive information
if not used judiciously.
        
        
          id
          
The `id` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) is OPTIONAL. If present, `id` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property)'s value
MUST be a single [URL](https://www.w3.org/TR/vc-data-model-2.0/#dfn-url), which MAY be dereferenceable. It is
RECOMMENDED that the [URL](https://www.w3.org/TR/vc-data-model-2.0/#dfn-url) in the `id` be one which, if dereferenceable, results
in a document containing machine-readable information about the `id`.
          
        

        
        
    [Example 3](https://www.w3.org/TR/vc-data-model-2.0/#example-use-of-the-id-property): Use of the id property
   
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
    "proofValue": "z5WHRyhjLd2H5RFcSqW3bss39zFBvVrVuXUovBpbGX2ATL8vSxwoeoiZFb1eibsdjRQK5GS1nr76RZRKBj7iH9roE"
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
    "proofValue": "u2V0AhVhAfojGD02jMuCezr87Ra8dvWa9ruscwcjDo2jYpvNEzxQthrKO3csDTuvk2A278uD7Cot6fgfm4YXddQ3eKnF91VgjgCQCpvhiT83vvn-T-PFVSUfoo51-s11TfQ39hmlIC61wy2hYINWUMbNH3sN80JcCKn-4fcaBDpSGT7KgsL07bUWUlHrJhVhAG4V_V2OV_xGWDfKU1CH_D53kF5Hy8RBi4S0551TkpUKvouKF5s5a-b1qDh2iNK1RXQyF6vdhbt4Kjo0RfnSYplhAvBoxWd2Xmpe8ERCoO3qs3el64rEmsYuPOgMyQTacrl2tuFLs3ui23JdtCnOSxmcRzVC27r4HIpubjSug4NE261hAcb7bwdJUpxP6Bqp7hiD8O_nFIMxLdzErfU522ZVy4CqLOiEERGMT2jFlgDcxlpkk5ZrMJOl9QfQSLPtjolWIy1hAbOzFKnJtBhSu3lfzmSftTWl1-FLtWu3Lt7ePxpGPbMjr6DVfS3sZL8E6M4uETdce15BsDkThGi_1ZjJ7YG9GLFhADav02TPSZdSV73AqOyZ6ryfuz3Y7pKKuu67dnqNzzXS-H-8-39I1rA759bba_lkqeo8F0lPtT_3liNamnCd-CoFnL2lzc3Vlcg"
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
    "proofValue": "u2V0ChVhQkkdBby2GbmvVh66cM6TNzNfh0hR9ePeG7dWYbHfDxK6CcA_rVoxxsRGIoWX5Gs6ZGgQNPTBeehiEHT_cj-5fjZ6ArTluARHPbaXQzWyXKrVYQGd_DaMQQsoaryttl5TvxnFT-Vm4SkVx03K9qNJ4jhArS1r7HKFDPyyrvPGqNF8bjgNELvoomOjpbD9JEvaGI1pYYJVTGbTfcflzyx41E-f9kSqmf10xYzxJrGfC7b7GPY8X7VjMT__ZKSuwdH-5jak-5gkjocsHI6oxIKlLrhW1Wh5yrDCH-QC823TS8NE9VGBzIFAfUt5qazGEcJ8CxeSPxFgg1LgUmXHTRjMrLAeoNgJipw-F81uEwauN0JK-WcohpmWBZy9pc3N1ZXI"
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
.YEsG9at9Hnt_j-UykCrnl494fcYMTjzpgvlK0KzzjvfmZmSg-sNVJqMZWizYhWv_eRUvAoZohvSJWeagwj_Ajw


    


    
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

d28443a10128a05901be7b2240636f6e74657874223a5b2268747470733a2f2f7777772e77332e6f72672f6e732f63726564656e7469616c732f7632222c2268747470733a2f2f7777772e77332e6f72672f6e732f63726564656e7469616c732f6578616d706c65732f7632225d2c226964223a22687474703a2f2f756e69766572736974792e6578616d706c652f63726564656e7469616c732f33373332222c2274797065223a5b2256657269666961626c6543726564656e7469616c222c224578616d706c6544656772656543726564656e7469616c225d2c22697373756572223a2268747470733a2f2f756e69766572736974792e6578616d706c652f697373756572732f353635303439222c2276616c696446726f6d223a22323031302d30312d30315430303a30303a30305a222c2263726564656e7469616c5375626a656374223a7b226964223a226469643a6578616d706c653a656266656231663731326562633666316332373665313265633231222c22646567726565223a7b2274797065223a224578616d706c6542616368656c6f72446567726565222c226e616d65223a2242616368656c6f72206f6620536369656e636520616e642041727473227d7d7d584013d7bfd4a7f3c0296d67f24157e4ba5a5fedafc688c5e01bd72f23e1d419d558ec05cddf9ac477fdc9fc7a8b1325dc80968a1bbc95d2c601753693290cbff553

    


    
    
    
    
      - 
        Encoded
      
      - 
        Decoded
      
      - 
        Issuer Disclosures
      
    
    
      

eyJraWQiOiJFeEhrQk1XOWZtYmt2VjI2Nm1ScHVQMnNVWV9OX0VXSU4xbGFwVXpPOHJvIiwiYWxnIjoiRVMyNTYifQ
.eyJpYXQiOjE3NDU3NzY3MTMsImV4cCI6MTc0Njk4NjMxMywiX3NkX2FsZyI6InNoYS0yNTYiLCJAY29udGV4dCI6WyJodHRwczovL3d3dy53My5vcmcvbnMvY3JlZGVudGlhbHMvdjIiLCJodHRwczovL3d3dy53My5vcmcvbnMvY3JlZGVudGlhbHMvZXhhbXBsZXMvdjIiXSwiaXNzdWVyIjoiaHR0cHM6Ly91bml2ZXJzaXR5LmV4YW1wbGUvaXNzdWVycy81NjUwNDkiLCJ2YWxpZEZyb20iOiIyMDEwLTAxLTAxVDAwOjAwOjAwWiIsImNyZWRlbnRpYWxTdWJqZWN0Ijp7ImRlZ3JlZSI6eyJuYW1lIjoiQmFjaGVsb3Igb2YgU2NpZW5jZSBhbmQgQXJ0cyIsIl9zZCI6WyJhbDRaR3cxellsZU1BMTA2SXpiLVhlc0pBbldDZ1NpNW5QbjFKRVYxamo4Il19LCJfc2QiOlsiOC1vWU9FU1JrNjBpbVozblgzY2E5RGxIeXFJcTk4RnQzX19HMUFsYU90MCJdfSwiX3NkIjpbIk9EUGNVWENXbGQtSGlxQ1h5NEhuY1Mxb3hqaURpRE9wMTJ4YlVveEZvU2MiLCJVaGtGbUw3cXc0UVlLWDJjVDNMWFAwcDZ5VHc1UmlIRG5xWGxfMFZLZnhBIl19
.YASiTse77TXvt7jYyChZOd6x0TbbBeEVZ14pekiOWw6G6N40a3evbWFBAkuPcStVFZPshFy1GFECySRVAhcD5A
~WyIzQkdhQ3BfaTZIV0hEMm5GekZ2blN3IiwgImlkIiwgImh0dHA6Ly91bml2ZXJzaXR5LmV4YW1wbGUvY3JlZGVudGlhbHMvMzczMiJd~WyJld1p0bUpDZHA2VWFWcEVhTXZ0V0FRIiwgInR5cGUiLCBbIlZlcmlmaWFibGVDcmVkZW50aWFsIiwgIkV4YW1wbGVEZWdyZWVDcmVkZW50aWFsIl1d~WyJIdThleHpqLTBySDg0aEtwenhnS0VnIiwgImlkIiwgImRpZDpleGFtcGxlOmViZmViMWY3MTJlYmM2ZjFjMjc2ZTEyZWMyMSJd~WyJVczR2ekVuVWJuSU96OC1VVDd2OHN3IiwgInR5cGUiLCAiRXhhbXBsZUJhY2hlbG9yRGVncmVlIl0~

    
    
      ```
{  "kid": "ExHkBMW9fmbkvV266mRpuP2sUY_N_EWIN1lapUzO8ro",  "alg": "ES256"}
```
      ```
{  "iat": 1745776713,  "exp": 1746986313,  "_sd_alg": "sha-256",  "@context": [    "https://www.w3.org/ns/credentials/v2",    "https://www.w3.org/ns/credentials/examples/v2"  ],  "issuer": "https://university.example/issuers/565049",  "validFrom": "2010-01-01T00:00:00Z",  "credentialSubject": {    "degree": {      "name": "Bachelor of Science and Arts",      "_sd": [        "al4ZGw1zYleMA106Izb-XesJAnWCgSi5nPn1JEV1jj8"      ]    },    "_sd": [      "8-oYOESRk60imZ3nX3ca9DlHyqIq98Ft3__G1AlaOt0"    ]  },  "_sd": [    "ODPcUXCWld-HiqCXy4HncS1oxjiDiDOp12xbUoxFoSc",    "UhkFmL7qw4QYKX2cT3LXP0p6yTw5RiHDnqXl_0VKfxA"  ]}
```
