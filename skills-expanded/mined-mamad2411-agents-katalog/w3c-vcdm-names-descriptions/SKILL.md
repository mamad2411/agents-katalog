---
name: "w3c-vcdm-names-descriptions"
description: "Use when working with human-readable labeling in W3C VCDM. Covers: names and descriptions for credentials, presentations, and related entities."
sections:
  - "4.6 Names and Descriptions"
---

<!-- ARF version: 2.0-2024-12-04 -->
<!-- Tokens: ~6468 -->

### 4.6 Names and Descriptions
        

        
When displaying a [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential), it can be helpful to have
text provided by the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) that furnishes the
[credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) with a name and a short description of its
purpose. The `name` and `description` [properties](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property)
serve these purposes.
        

        
          name
          
An OPTIONAL property that expresses the name of the [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential). If
present, the value of the `name` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) MUST be a string or
a language value object as described in
[11.1 Language and Base Direction](https://www.w3.org/TR/vc-data-model-2.0/#language-and-base-direction). Ideally, the name of a
[credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) is concise, human-readable, and could enable an individual to
quickly differentiate one [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) from any other [credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential)
they might hold.
          
          description
          
An OPTIONAL property that conveys specific details about a [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential). If
present, the value of the `description` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) MUST be a
string or a language value object as described in
[11.1 Language and Base Direction](https://www.w3.org/TR/vc-data-model-2.0/#language-and-base-direction). Ideally, the description of a
[credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) is no more than a few sentences in length and conveys enough
information about the [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) to remind an individual of its contents
without having to look through the entirety of the [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims).
          
        

        
        
    [Example 5](https://www.w3.org/TR/vc-data-model-2.0/#example-use-of-the-name-and-description-properties): Use of the name and description properties
   
      - Credential- ecdsa- ecdsa-sd- bbs- jose- cose- sd-jwt```
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://www.w3.org/ns/credentials/examples/v2"
  ],
  "id": "http://university.example/credentials/3732",
  "type": ["VerifiableCredential", "ExampleDegreeCredential"],
  "issuer": {
    "id": "https://university.example/issuers/565049",
    "name": "Example University",
    "description": "A public university focusing on teaching examples."
  },
  "validFrom": "2015-05-10T12:30:00Z",
  "name": "Example University Degree",
  "description": "2015 Bachelor of Science and Arts Degree",
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
  "issuer": {
    "id": "https://university.example/issuers/565049",
    "name": "Example University",
    "description": "A public university focusing on teaching examples."
  },
  "validFrom": "2015-05-10T12:30:00Z",
  "name": "Example University Degree",
  "description": "2015 Bachelor of Science and Arts Degree",
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
    "proofValue": "z2LeuoNi3yR1b6c3fkRsEvXJ5ex8X4RdutyK7L6HAo2bJQwr21w85Y5KWy3DptXR8ke52Assqik6wKTy9DKqkEZ2r"
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
  "issuer": {
    "id": "https://university.example/issuers/565049",
    "name": "Example University",
    "description": "A public university focusing on teaching examples."
  },
  "validFrom": "2015-05-10T12:30:00Z",
  "name": "Example University Degree",
  "description": "2015 Bachelor of Science and Arts Degree",
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
    "proofValue": "u2V0AhVhA5A-VvZ6RF2KlLjsYsx1DosYuzhbD7hn6N6gTF5yv22oTPKcqHyElGQn3TcerwktEbNrRiuWMvmfuw1XmwhCk-lgjgCQCHC44msX1XnfID2VfkUX1j1PHUzfjdORSePcGUhVB3KxYIBeo1lJt0Rp-So7_Ch6hiCE36oR-r6WyVaT6r-o0Nf1nh1hATMKDPXogkIVw6n-pqlDoJMti8cCVJvle_IWSAqv5vShtqt5E6NEJ3PTiK7NwSMSGMVE0XdJXZlEj3xck6UL0vlhAa7ltjeSjPD1TD52OkPPjuQrhADwoTsDXERr-UCuNICq-uxKiFsxebXjys1SeHIFzT0TQA5TlTl-J55vFL90q-lhAi8EKNrgQiKdl_EAlgv3aS15FLuIpUmfROB6srPRpHI4cz-kC8xlarcp9XMqHIpL5hncUJd2EoGTmMpm3nzs3PVhAr4sC2Lin-35yxMSvWXrq7cEGw4IomJnayfWsxmXencGOmXQzZxJbsUHmLCAprm51apFj19BZED6G-82Ilx0ZvlhADRiBGvSKeF3hYkihvS7kkZDnySRU4Q4yfNm_Hwe6kysHhtP5rnbu3LYfU-hI_0P6FbZJrPQ7uifIMg2QMHxARFhAxjQMayCxmcOVGlo5ICU5zQxx6qTgjgpNl1GC1dGjnA1J3xhFALceL5DHxJbSvcRsRVwRjBybMkZurUWhPgzpwVhAhbwrQWJSLLhyXqFcQef_-eKnNE3F5oBq2phORFJ16m3uRU-R-vSoXJlSpyLBZrNGU7gwCHVv0b_e2ZC13MiFR4FnL2lzc3Vlcg"
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
  "issuer": {
    "id": "https://university.example/issuers/565049",
    "name": "Example University",
    "description": "A public university focusing on teaching examples."
  },
  "validFrom": "2015-05-10T12:30:00Z",
  "name": "Example University Degree",
  "description": "2015 Bachelor of Science and Arts Degree",
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
    "proofValue": "u2V0ChVhQkS0mcHTu9KLuuY8_DlU_2lj8Su_EXxWyY0xMPZuCGQMRzah3DFaerG-CRDFWR1KBWkYUpPizkPDULYOU8XsXoC3a8_00GgHfKuoiNCLnSNBYQGd_DaMQQsoaryttl5TvxnFT-Vm4SkVx03K9qNJ4jhArXFDE8ZX70eeJX1DawHuw0sW9CBV3sa68IaRGcnZiiQpYYJVTGbTfcflzyx41E-f9kSqmf10xYzxJrGfC7b7GPY8X7VjMT__ZKSuwdH-5jak-5gkjocsHI6oxIKlLrhW1Wh5yrDCH-QC823TS8NE9VGBzIFAfUt5qazGEcJ8CxeSPxFggbCn9jbv1yUPTocre_YTgvXiebb8lJMqxhmAnw4MiFbWBZy9pc3N1ZXI"
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
  "issuer": {
    "id": "https://university.example/issuers/565049",
    "name": "Example University",
    "description": "A public university focusing on teaching examples."
  },
  "validFrom": "2015-05-10T12:30:00Z",
  "name": "Example University Degree",
  "description": "2015 Bachelor of Science and Arts Degree",
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
.eyJAY29udGV4dCI6WyJodHRwczovL3d3dy53My5vcmcvbnMvY3JlZGVudGlhbHMvdjIiLCJodHRwczovL3d3dy53My5vcmcvbnMvY3JlZGVudGlhbHMvZXhhbXBsZXMvdjIiXSwiaWQiOiJodHRwOi8vdW5pdmVyc2l0eS5leGFtcGxlL2NyZWRlbnRpYWxzLzM3MzIiLCJ0eXBlIjpbIlZlcmlmaWFibGVDcmVkZW50aWFsIiwiRXhhbXBsZURlZ3JlZUNyZWRlbnRpYWwiXSwiaXNzdWVyIjp7ImlkIjoiaHR0cHM6Ly91bml2ZXJzaXR5LmV4YW1wbGUvaXNzdWVycy81NjUwNDkiLCJuYW1lIjoiRXhhbXBsZSBVbml2ZXJzaXR5IiwiZGVzY3JpcHRpb24iOiJBIHB1YmxpYyB1bml2ZXJzaXR5IGZvY3VzaW5nIG9uIHRlYWNoaW5nIGV4YW1wbGVzLiJ9LCJ2YWxpZEZyb20iOiIyMDE1LTA1LTEwVDEyOjMwOjAwWiIsIm5hbWUiOiJFeGFtcGxlIFVuaXZlcnNpdHkgRGVncmVlIiwiZGVzY3JpcHRpb24iOiIyMDE1IEJhY2hlbG9yIG9mIFNjaWVuY2UgYW5kIEFydHMgRGVncmVlIiwiY3JlZGVudGlhbFN1YmplY3QiOnsiaWQiOiJkaWQ6ZXhhbXBsZTplYmZlYjFmNzEyZWJjNmYxYzI3NmUxMmVjMjEiLCJkZWdyZWUiOnsidHlwZSI6IkV4YW1wbGVCYWNoZWxvckRlZ3JlZSIsIm5hbWUiOiJCYWNoZWxvciBvZiBTY2llbmNlIGFuZCBBcnRzIn19fQ
.x5OQX2cmaXVU-UxScJ1KlOgR9nwpLvFO4s-fWuHvb58DDEb-xVxS8hqPIpLiNK0F3eedtoHeJ2gJ2RHVnGVSNQ


    


    
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
  "issuer": {
    "id": "https://university.example/issuers/565049",
    "name": "Example University",
    "description": "A public university focusing on teaching examples."
  },
  "validFrom": "2015-05-10T12:30:00Z",
  "name": "Example University Degree",
  "description": "2015 Bachelor of Science and Arts Degree",
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

d28443a10128a05902807b2240636f6e74657874223a5b2268747470733a2f2f7777772e77332e6f72672f6e732f63726564656e7469616c732f7632222c2268747470733a2f2f7777772e77332e6f72672f6e732f63726564656e7469616c732f6578616d706c65732f7632225d2c226964223a22687474703a2f2f756e69766572736974792e6578616d706c652f63726564656e7469616c732f33373332222c2274797065223a5b2256657269666961626c6543726564656e7469616c222c224578616d706c6544656772656543726564656e7469616c225d2c22697373756572223a7b226964223a2268747470733a2f2f756e69766572736974792e6578616d706c652f697373756572732f353635303439222c226e616d65223a224578616d706c6520556e6976657273697479222c226465736372697074696f6e223a2241207075626c696320756e697665727369747920666f637573696e67206f6e207465616368696e67206578616d706c65732e227d2c2276616c696446726f6d223a22323031352d30352d31305431323a33303a30305a222c226e616d65223a224578616d706c6520556e697665727369747920446567726565222c226465736372697074696f6e223a22323031352042616368656c6f72206f6620536369656e636520616e64204172747320446567726565222c2263726564656e7469616c5375626a656374223a7b226964223a226469643a6578616d706c653a656266656231663731326562633666316332373665313265633231222c22646567726565223a7b2274797065223a224578616d706c6542616368656c6f72446567726565222c226e616d65223a2242616368656c6f72206f6620536369656e636520616e642041727473227d7d7d5840e49e36b7cb7a12d81900a6ba0bdd26084dcb33baaf759a3a7b3eacff8af566291f6ae573ba6707b231de6f70372e4b8da88e9be12b0f7dd168d5b6f0f0044770

    


    
    
    
    
      - 
        Encoded
      
      - 
        Decoded
      
      - 
        Issuer Disclosures
      
    
    
      

eyJraWQiOiJFeEhrQk1XOWZtYmt2VjI2Nm1ScHVQMnNVWV9OX0VXSU4xbGFwVXpPOHJvIiwiYWxnIjoiRVMyNTYifQ
.eyJpYXQiOjE3NDU3NzY3MTMsImV4cCI6MTc0Njk4NjMxMywiX3NkX2FsZyI6InNoYS0yNTYiLCJAY29udGV4dCI6WyJodHRwczovL3d3dy53My5vcmcvbnMvY3JlZGVudGlhbHMvdjIiLCJodHRwczovL3d3dy53My5vcmcvbnMvY3JlZGVudGlhbHMvZXhhbXBsZXMvdjIiXSwiaXNzdWVyIjp7Im5hbWUiOiJFeGFtcGxlIFVuaXZlcnNpdHkiLCJkZXNjcmlwdGlvbiI6IkEgcHVibGljIHVuaXZlcnNpdHkgZm9jdXNpbmcgb24gdGVhY2hpbmcgZXhhbXBsZXMuIiwiX3NkIjpbIjN5U2k5WkUtdWp0RDQ4NDRacGY4V2NMY3EwQWlyajVqbFJmLTNSQVJPcmsiXX0sInZhbGlkRnJvbSI6IjIwMTUtMDUtMTBUMTI6MzA6MDBaIiwibmFtZSI6IkV4YW1wbGUgVW5pdmVyc2l0eSBEZWdyZWUiLCJkZXNjcmlwdGlvbiI6IjIwMTUgQmFjaGVsb3Igb2YgU2NpZW5jZSBhbmQgQXJ0cyBEZWdyZWUiLCJjcmVkZW50aWFsU3ViamVjdCI6eyJkZWdyZWUiOnsibmFtZSI6IkJhY2hlbG9yIG9mIFNjaWVuY2UgYW5kIEFydHMiLCJfc2QiOlsiZnRIMUtTRTVzNmZKd1cyMWY2STBlUmNtYW9SX2s5YTVBS2lTMnFidFVTNCJdfSwiX3NkIjpbIkNJaDBOYWN4ME5IWUJ5QTFoZ1NlWDdoMXF0amNvUGRIODR1NTN0a2t6R3ciXX0sIl9zZCI6WyI2UFk1X1dKU1pUaWszdG9rOHg0eEF0TWstOGpqWnpzZnV6dXhUX2JvY0wwIiwiVE9XWGhJS1dPeHBZbHgtUmtoal9kVTh3Sml2cmRuOUNrbm9fcXVvNng4YyJdfQ
.FzX3Ke7i888rlwj2XY-Xmd73hKH4oGaIp68z2xqPS1Bv17BKSaKQwfxgf22iNAguzVvlIQVXjRqpg0G-S46xDA
~WyI5MGlaMEp1a2lCUlpoa0pnajhyRDN3IiwgImlkIiwgImh0dHA6Ly91bml2ZXJzaXR5LmV4YW1wbGUvY3JlZGVudGlhbHMvMzczMiJd~WyJpbU94UllGWWVSM2VHWGdJOTUxcHVnIiwgInR5cGUiLCBbIlZlcmlmaWFibGVDcmVkZW50aWFsIiwgIkV4YW1wbGVEZWdyZWVDcmVkZW50aWFsIl1d~WyJlemF5RzgwVG1hRVhhSjRwNHlpY2xnIiwgImlkIiwgImh0dHBzOi8vdW5pdmVyc2l0eS5leGFtcGxlL2lzc3VlcnMvNTY1MDQ5Il0~WyJXT1lvak0yb2dad3pXQjJOa3FELWNBIiwgImlkIiwgImRpZDpleGFtcGxlOmViZmViMWY3MTJlYmM2ZjFjMjc2ZTEyZWMyMSJd~WyJuUG1kWEk5YWtEakd4Mk0wRTVhWUtBIiwgInR5cGUiLCAiRXhhbXBsZUJhY2hlbG9yRGVncmVlIl0~

    
    
      ```
{  "kid": "ExHkBMW9fmbkvV266mRpuP2sUY_N_EWIN1lapUzO8ro",  "alg": "ES256"}
```
      ```
{  "iat": 1745776713,  "exp": 1746986313,  "_sd_alg": "sha-256",  "@context": [    "https://www.w3.org/ns/credentials/v2",    "https://www.w3.org/ns/credentials/examples/v2"  ],  "issuer": {    "name": "Example University",    "description": "A public university focusing on teaching examples.",    "_sd": [      "3ySi9ZE-ujtD4844Zpf8WcLcq0Airj5jlRf-3RAROrk"    ]  },  "validFrom": "2015-05-10T12:30:00Z",  "name": "Example University Degree",  "description": "2015 Bachelor of Science and Arts Degree",  "credentialSubject": {    "degree": {      "name": "Bachelor of Science and Arts",      "_sd": [        "ftH1KSE5s6fJwW21f6I0eRcmaoR_k9a5AKiS2qbtUS4"      ]    },    "_sd": [      "CIh0Nacx0NHYByA1hgSeX7h1qtjcoPdH84u53tkkzGw"    ]  },  "_sd": [    "6PY5_WJSZTik3tok8x4xAtMk-8jjZzsfuzuxT_bocL0",    "TOWXhIKWOxpYlx-Rkhj_dU8wJivrdn9Ckno_quo6x8c"  ]}
```
