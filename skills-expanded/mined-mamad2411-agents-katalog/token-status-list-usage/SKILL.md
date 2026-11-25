---
name: "token-status-list-usage"
description: "Use when implementing Token Status List verification. Covers: referenced tokens (JOSE/COSE), status types, verification procedures, and validation rules."
sections:
  - "6. Referenced Token"
  - "6.1. Status Claim"
  - "6.2. Referenced Token in JOSE"
  - "6.3. Referenced Token in COSE"
  - "7. Status Types"
  - "7.1. Status Types Values"
---

<!-- ARF version: draft-10 -->
<!-- Tokens: ~6538 -->

## 6. Referenced Token


### 6.1. Status Claim
By including a "status" claim in a Referenced Token, the Issuer is referencing a mechanism to retrieve status information about this Referenced Token. The claim contains members used to reference to a Status List Token as defined in this specification. Other members of the "status" object may be defined by other specifications. This is analogous to "cnf" claim in Section 3.1 of [[RFC7800](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC7800)] in which different authenticity confirmation methods can be included.


### 6.2. Referenced Token in JOSE
The Referenced Token MAY be encoded as a "JSON Web Token (JWT)" according to [[RFC7519](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC7519)] or other formats based on JOSE.
The following content applies to the JWT Claims Set:

- 
            `status`: REQUIRED. The `status` (status) claim MUST specify a JSON Object that contains at least one reference to a status mechanism.

- 
                `status_list`: REQUIRED when the status mechanism defined in this specification is used. It contains a reference to a Status List Token. It MUST at least contain the following claims:

- 
                    `idx`: REQUIRED. The `idx` (index) claim MUST specify an Integer that represents the index to check for status information in the Status List for the current Referenced Token. The value of `idx` MUST be a non-negative number, containing a value of zero or greater.

                  - 
                    `uri`: REQUIRED. The `uri` (URI) claim MUST specify a String value that identifies the Status List Token containing the status information for the Referenced Token. The value of `uri` MUST be a URI conforming to [[RFC3986](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC3986)].

                

            

        
Application of additional restrictions and policies are at the discretion of the Relying Party.
The following is a non-normative example of a decoded header and payload of a Referenced Token:

```
{
  "alg": "ES256",
  "kid": "11"
}
.
{
  "status": {
    "status_list": {
      "idx": 0,
      "uri": "https://example.com/statuslists/1"
    }
  }
}
```

SD-JWT-based Verifiable Credentials [[SD-JWT.VC](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#SD-JWT.VC)] introduce the usage of a status mechanism in Section 3.2.2.2. The "status" object uses the same encoding as a JWT as defined in [Section 6.2](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#referenced-token-jose).
The following is a non-normative example of a Referenced Token in SD-JWT-VC serialized form as received from an Issuer:

```
eyJhbGciOiAiRVMyNTYiLCAidHlwIjogImV4YW1wbGUrc2Qtand0In0.eyJfc2QiOiBb
Ikh2cktYNmZQVjB2OUtfeUNWRkJpTEZIc01heGNEXzExNEVtNlZUOHgxbGciXSwgImlz
cyI6ICJodHRwczovL2V4YW1wbGUuY29tL2lzc3VlciIsICJpYXQiOiAxNjgzMDAwMDAw
LCAiZXhwIjogMTg4MzAwMDAwMCwgInN1YiI6ICI2YzVjMGE0OS1iNTg5LTQzMWQtYmFl
Ny0yMTkxMjJhOWVjMmMiLCAic3RhdHVzIjogeyJzdGF0dXNfbGlzdCI6IHsiaWR4Ijog
MCwgInVyaSI6ICJodHRwczovL2V4YW1wbGUuY29tL3N0YXR1c2xpc3RzLzEifX0sICJf
c2RfYWxnIjogInNoYS0yNTYifQ.-kgS-R-Z4DEDlqb8kb6381_gHHNatsoF1fcVKZk3M
06CrnV8F8k9d2w2V_YAOvgcb0f11FqDFezXBXH30d4vcw~WyIyR0xDNDJzS1F2ZUNmR2
ZyeU5STjl3IiwgInN0cmVldF9hZGRyZXNzIiwgIlNjaHVsc3RyLiAxMiJd~WyJlbHVWN
U9nM2dTTklJOEVZbnN4QV9BIiwgImxvY2FsaXR5IiwgIlNjaHVscGZvcnRhIl0~WyI2S
Wo3dE0tYTVpVlBHYm9TNXRtdlZBIiwgInJlZ2lvbiIsICJTYWNoc2VuLUFuaGFsdCJd~
WyJlSThaV205UW5LUHBOUGVOZW5IZGhRIiwgImNvdW50cnkiLCAiREUiXQ~WyJRZ19PN
jR6cUF4ZTQxMmExMDhpcm9BIiwgImFkZHJlc3MiLCB7Il9zZCI6IFsiNnZoOWJxLXpTN
EdLTV83R3BnZ1ZiWXp6dTZvT0dYcm1OVkdQSFA3NVVkMCIsICI5Z2pWdVh0ZEZST0NnU
nJ0TmNHVVhtRjY1cmRlemlfNkVyX2o3NmttWXlNIiwgIktVUkRQaDRaQzE5LTN0aXotR
GYzOVY4ZWlkeTFvVjNhM0gxRGEyTjBnODgiLCAiV045cjlkQ0JKOEhUQ3NTMmpLQVN4V
GpFeVc1bTV4NjVfWl8ycm8yamZYTSJdfV0~
```

The resulting payload of the example above:

```
{
  "_sd": [
    "HvrKX6fPV0v9K_yCVFBiLFHsMaxcD_114Em6VT8x1lg"
  ],
  "iss": "https://example.com/issuer",
  "iat": 1683000000,
  "exp": 1883000000,
  "sub": "6c5c0a49-b589-431d-bae7-219122a9ec2c",
  "status": {
    "status_list": {
      "idx": 0,
      "uri": "https://example.com/statuslists/1"
    }
  },
  "_sd_alg": "sha-256"
}
```


### 6.3. Referenced Token in COSE
The Referenced Token MAY be encoded as a "COSE Web Token (CWT)" object according to [[RFC8392](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC8392)] or other formats based on COSE.
The following content applies to the CWT Claims Set:

- 
            `65535` (status): REQUIRED. The status claim is encoded as a `Status` CBOR structure and MUST include at least one data item that refers to a status mechanism. Each data item in the `Status` CBOR structure comprises a key-value pair, where the key must be a CBOR text string (Major Type 3) specifying the identifier of the status mechanism and the corresponding value defines its contents. This specification defines the following data items:

- 
                `status_list` (status list): REQUIRED when the status mechanism defined in this specification is used. It has the same definition as the `status_list` claim in [Section 6.2](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#referenced-token-jose) but MUST be encoded as a `StatusListInfo` CBOR structure with the following fields:

- 
                    `idx`: REQUIRED. Unsigned integer (Major Type 0) The `idx` (index) claim MUST specify an Integer that represents the index to check for status information in the Status List for the current Referenced Token. The value of `idx` MUST be a non-negative number, containing a value of zero or greater.

                  - 
                    `uri`: REQUIRED. Text string (Major Type 3). The `uri` (URI) claim MUST specify a String value that identifies the Status List Token containing the status information for the Referenced Token. The value of `uri` MUST be a URI conforming to [[RFC3986](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC3986)].

                

            

        
Application of additional restrictions and policies are at the discretion of the Relying Party.
The following is a non-normative example of a Referenced Token in CWT format in Hex:

```
d28443a10126a1044231325866a502653132333435017368747470733a2f2f657861
6d706c652e636f6d061a648c5bea041a8898dfea19ffffa16b7374617475735f6c69
7374a2636964780063757269782168747470733a2f2f6578616d706c652e636f6d2f
7374617475736c697374732f315840362d01f477f9dab57e25d2953a3a29564936ea
a6ef9b9f197607e39e14991980a4b7d378b1ad6dc41f60c13db100a821d20054c070
38b6d15c8523af7a5b43d4
```

The following is the CBOR Annotated Hex output of the example above:

```
d2                              # tag(18)
  84                            #   array(4)
    43                          #     bytes(3)
      a10126                    #       "¡\x01&"
    a1                          #     map(1)
      04                        #       uint(4)
      42                        #       bytes(2)
        3132                    #         "12"
    58 66                       #     bytes(102)
      a50265313233343501736874  #       "¥\x02e12345\x01sht"
      7470733a2f2f6578616d706c  #       "tps://exampl"
      652e636f6d061a648c5bea04  #       "e.com\x06\x1ad\x8c[ê\x04"
      1a8898dfea19ffffa16b7374  #       "\x1a\x88\x98ßê\x19ÿÿ¡kst"
      617475735f6c697374a26369  #       "atus_list¢ci"
      647800637572697821687474  #       "dx\x00curix!htt"
      70733a2f2f6578616d706c65  #       "ps://example"
      2e636f6d2f7374617475736c  #       ".com/statusl"
      697374732f31              #       "ists/1"
    58 40                       #     bytes(64)
      362d01f477f9dab57e25d295  #       "6-\x01ôwùÚµ~%Ò\x95"
      3a3a29564936eaa6ef9b9f19  #       "::)VI6ê¦ï\x9b\x9f\x19"
      7607e39e14991980a4b7d378  #       "v\x07ã\x9e\x14\x99\x19\x80¤·Óx"
      b1ad6dc41f60c13db100a821  #       "±\xadmÄ\x1f`Á=±\x00¨!"
      d20054c07038b6d15c8523af  #       "Ò\x00TÀp8¶Ñ\\x85#¯"
      7a5b43d4                  #       "z[CÔ"
```

ISO mdoc [[ISO.mdoc](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#ISO.mdoc)] may utilize the Status List mechanism by introducing the `status` parameter in the Mobile Security Object (MSO) as specified in Section 9.1.2. The `status` parameter uses the same encoding as a CWT as defined in [Section 6.3](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#referenced-token-cose).
It is RECOMMENDED to use `status` for the label of the field that contains the `Status` CBOR structure.
Application of additional restrictions and policies are at the discretion of the Relying Party.
The following is a non-normative example of an IssuerAuth as specified in ISO mDL (also referred to as signed MSO) in Hex:

```
8443a10126a118215901f3308201ef30820195a00302010202140bfec7da97e048e
15ac3dacb9eafe82e64fd07f5300a06082a8648ce3d040302302331143012060355
04030c0b75746f7069612069616361310b3009060355040613025553301e170d323
4313030313030303030305a170d3235313030313030303030305a30213112301006
035504030c0975746f706961206473310b300906035504061302555330593013060
72a8648ce3d020106082a8648ce3d03010703420004ace7ab7340e5d9648c5a72a9
a6f56745c7aad436a03a43efea77b5fa7b88f0197d57d8983e1b37d3a539f4d5883
65e38cbbf5b94d68c547b5bc8731dcd2f146ba381a83081a5301c0603551d1f0415
30133011a00fa00d820b6578616d706c652e636f6d301e0603551d1204173015811
36578616d706c65406578616d706c652e636f6d301d0603551d0e0416041414e290
17a6c35621ffc7a686b7b72db06cd12351301f0603551d2304183016801454fa238
3a04c28e0d930792261c80c4881d2c00b300e0603551d0f0101ff04040302078030
150603551d250101ff040b3009060728818c5d050102300a06082a8648ce3d04030
20348003045022100b7103fd4b90529f50bd6f70c5ae5ce7f4f3d4d15a4e082812f
9fa1f5c2e5aa0a0220070b2822ec7ce6c56804923a85b2cfbffd054cf9a915f070c
fef7179a4bc6569590320d81859031ba766737461747573a16b7374617475735f6c
697374a26369647819019c63757269782168747470733a2f2f6578616d706c652e6
36f6d2f7374617475736c697374732f3167646f6354797065756f72672e69736f2e
31383031332e352e312e6d444c6776657273696f6e63312e306c76616c696469747
9496e666fa3667369676e6564c074323032342d31302d30315431333a33303a3032
5a6976616c696446726f6dc074323032342d31302d30315431333a33303a30325a6
a76616c6964556e74696cc074323032352d31302d30315431333a33303a30325a6c
76616c756544696765737473a1716f72672e69736f2e31383031332e352e31ac005
820a81d65ed5075fbd7ee19fa66e2bb3047ed826e2769873e7ef07c923da7a6f243
01582048701a9546492284d266ed81d439230a582d0e1f17a08ab1859a3efe98069
0a4025820d11fe48c8835b30bfb3895c3905436ddfb63f59ab9eee181b110985329
2a8f62035820a741bf05e20a8bc359e32426106ed0899b2c60262cc3acc637ddc99
41095fb7a045820ab67cb9a8f20a8572f77f02727367d08dc8e57fb89deb46b9c62
6e94457b7d8b055820bacddb4142b3842bd555206eb5acb27ded063294995c7e7fe
fbf93ece522604d065820bfd02b3aebdc05b53b5539226c38088d6d784b0ea0fab6
9eb9311650a48d325307582027dab70fe71da63e5e5d199e8ae5b79cbe8904bc30c
5b7544fb809e02ccb3e6a0858200dbd7ccc9c7727d3d17295f1b6f1914071670ee2
3d4d33530c31f1f406b8e3b7095820a5beb5efadf37f21637209abc519830681cc5
1f334818a823fec13b29552f5ba0a5820d8047c95f9272d7d07b2c13a9f5ac2ee02
380ab272a165e569391d89a2152c3c0b582004939930ffb4911ef03487a153605a3
0368b69f2437d6d21b4c90f92bc144c3e6d6465766963654b6579496e666fa16964
65766963654b6579a40102200121582096313d6c63e24e3372742bfdb1a33ba2c89
7dcd68ab8c753e4fbd48dca6b7f9a2258201fb3269edd418857de1b39a4e4a44b92
fa484caa722c228288f01d0c03a2c3d66f646967657374416c676f726974686d675
348412d3235365840b7c2d4abe85aa5ba814ef95de0385c71c802be8ac33a4a971a
85ed800ba7acb59cb21035f4a68fc0caa450cbefd3b255aec72f83595f0ae7b7d50
fe8a1c4cafe
```

The following is the CBOR Diagnostic Notation of the example above:

```
[
  << {
    1: -7
  } >>,
  {
    33: h'308201ef30820195a00302010202140bfec7da97e048e15ac3dacb9ea
    fe82e64fd07f5300a06082a8648ce3d04030230233114301206035504030c0b
    75746f7069612069616361310b3009060355040613025553301e170d3234313
    030313030303030305a170d3235313030313030303030305a30213112301006
    035504030c0975746f706961206473310b30090603550406130255533059301
    306072a8648ce3d020106082a8648ce3d03010703420004ace7ab7340e5d964
    8c5a72a9a6f56745c7aad436a03a43efea77b5fa7b88f0197d57d8983e1b37d
    3a539f4d588365e38cbbf5b94d68c547b5bc8731dcd2f146ba381a83081a530
    1c0603551d1f041530133011a00fa00d820b6578616d706c652e636f6d301e0
    603551d120417301581136578616d706c65406578616d706c652e636f6d301d
    0603551d0e0416041414e29017a6c35621ffc7a686b7b72db06cd12351301f0
    603551d2304183016801454fa2383a04c28e0d930792261c80c4881d2c00b30
    0e0603551d0f0101ff04040302078030150603551d250101ff040b300906072
    8818c5d050102300a06082a8648ce3d0403020348003045022100b7103fd4b9
    0529f50bd6f70c5ae5ce7f4f3d4d15a4e082812f9fa1f5c2e5aa0a0220070b2
    822ec7ce6c56804923a85b2cfbffd054cf9a915f070cfef7179a4bc6569'
  },
  << 24( << {
    "status": {
      "status_list": {
        "idx": 412,
        "uri": "https://example.com/statuslists/1"
      }
    },
    "docType": "org.iso.18013.5.1.mDL",
    "version": "1.0",
    "validityInfo": {
      "signed": 2024-10-01 13:30:02+00:00,
      "validFrom": 2024-10-01 13:30:02+00:00,
      "validUntil": 2025-10-01 13:30:02+00:00
    },
    "valueDigests": {
      "org.iso.18013.5.1": {
        0: h'a81d65ed5075fbd7ee19fa66e2bb3047ed826e2769873e7ef07c92
        3da7a6f243',
        1: h'48701a9546492284d266ed81d439230a582d0e1f17a08ab1859a3e
        fe980690a4',
        2: h'd11fe48c8835b30bfb3895c3905436ddfb63f59ab9eee181b11098
        53292a8f62',
        3: h'a741bf05e20a8bc359e32426106ed0899b2c60262cc3acc637ddc9
        941095fb7a',
        4: h'ab67cb9a8f20a8572f77f02727367d08dc8e57fb89deb46b9c626e
        94457b7d8b',
        5: h'bacddb4142b3842bd555206eb5acb27ded063294995c7e7fefbf93
        ece522604d',
        6: h'bfd02b3aebdc05b53b5539226c38088d6d784b0ea0fab69eb93116
        50a48d3253',
        7: h'27dab70fe71da63e5e5d199e8ae5b79cbe8904bc30c5b7544fb809
        e02ccb3e6a',
        8: h'0dbd7ccc9c7727d3d17295f1b6f1914071670ee23d4d33530c31f1
        f406b8e3b7',
        9: h'a5beb5efadf37f21637209abc519830681cc51f334818a823fec13
        b29552f5ba',
        10: h'd8047c95f9272d7d07b2c13a9f5ac2ee02380ab272a165e569391
        d89a2152c3c',
        11: h'04939930ffb4911ef03487a153605a30368b69f2437d6d21b4c90
        f92bc144c3e'
      }
    },
    "deviceKeyInfo": {
      "deviceKey": {
        1: 2,
        -1: 1,
        -2: h'96313d6c63e24e3372742bfdb1a33ba2c897dcd68ab8c753e4fbd
        48dca6b7f9a',
        -3: h'1fb3269edd418857de1b39a4e4a44b92fa484caa722c228288f01
        d0c03a2c3d6'
      }
    },
    "digestAlgorithm": "SHA-256"
  } >> ) >>,
  h'b7c2d4abe85aa5ba814ef95de0385c71c802be8ac33a4a971a85ed800ba7acb
  59cb21035f4a68fc0caa450cbefd3b255aec72f83595f0ae7b7d50fe8a1c4cafe'
]
```

---

## 7. Status Types
This document defines the statuses of Referenced Tokens as Status Type values. A status describes the state, mode, condition or stage of an entity that is represented by the Referenced Token.
A Status List can not represent multiple statuses per Referenced Token. If the Status List contains more than one bit per token (as defined by `bits` in the Status List), then the whole value of bits MUST describe one value. Status Types MUST have a numeric value between 0 and 255 for their representation in the Status List. The issuer of the Status List MUST choose an adequate `bits` value (bit size) to be able to describe the required Status Types for its application.


### 7.1. Status Types Values
This document creates a registry in [Section 14.5](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#iana-status-types) that includes the most common Status Type values. Additional values may defined for particular use cases. Status Types described by this document comprise:

- 
            0x00 - "VALID" - The status of the Referenced Token is valid, correct or legal.

          - 
            0x01 - "INVALID" - The status of the Referenced Token is revoked, annulled, taken back, recalled or cancelled.

          - 
            0x02 - "SUSPENDED" - The status of the Referenced Token is temporarily invalid, hanging, debarred from privilege. This state is reversible.

        
The Status Type value 0x03 and Status Type values in the range 0x0B until 0x0F are permanently reserved as application specific. Meaning the processing of Status Types using these values is application specific. All other Status Type values are reserved for future registration.
The processing rules for Referenced Tokens (such as JWT or CWT) precede any evaluation of a Referenced Token's status. For example, if a token is evaluated as being expired through the "exp" (Expiration Time) but also has a status of 0x00 ("VALID"), the token is considered expired.
See [Section 12.8](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#privacy-status-types) for privacy considerations on status types.
