---
name: "sd-jwt-examples-nested"
description: "Use when implementing nested SD-JWT data handling. Covers: flat, structured, and recursive disclosure examples for complex claim sets."
sections:
  - "6. Considerations on Nested Data in SD-JWTs"
  - "6.1. Example: Flat SD-JWT"
  - "6.2. Example: Structured SD-JWT"
  - "6.3. Example: SD-JWT with Recursive Disclosures"
---

<!-- ARF version: RFC-9901 -->
<!-- Tokens: ~3228 -->

## 6. Considerations on Nested Data in SD-JWTs
Being JSON, an object in an SD-JWT payload MAY contain name/value pairs where the value is another object or objects MAY be elements in arrays. In SD-JWT, the Issuer decides for each claim individually, on each level of the JSON, whether or not the claim should be selectively disclosable. This choice can be made on each level independent of whether keys higher in the hierarchy are selectively disclosable.
From this it follows that the `_sd` key containing digests MAY appear multiple
times in an SD-JWT, and likewise, there MAY be multiple arrays within the
hierarchy with each having selectively disclosable elements. Digests of
selectively disclosable claims MAY even appear within other Disclosures.
The following examples illustrate some of the options an Issuer has. It is up to the Issuer to decide which structure to use, depending on, for example, the expected use cases for the SD-JWT, requirements for privacy, size considerations, or operating environment requirements. For more examples with nested structures, see Appendices [A.1](https://www.rfc-editor.org/rfc/rfc9901.html#example-simple_structured) and [A.2](https://www.rfc-editor.org/rfc/rfc9901.html#example-complex-structured-sd-jwt).
The following input JWT Claims Set is used as an example throughout this section:

```
{
  "sub": "6c5c0a49-b589-431d-bae7-219122a9ec2c",
  "address": {
    "street_address": "Schulstr. 12",
    "locality": "Schulpforta",
    "region": "Sachsen-Anhalt",
    "country": "DE"
  }
}
```


        Note: The following examples of the structures are non-normative and are not intended to
represent all possible options. They are also not meant to define or restrict
how `address` claim can be represented in an SD-JWT.


### 6.1. Example: Flat SD-JWT
The Issuer can decide to treat the `address` claim as a block that can either be disclosed completely or not at all. The following example shows that in this case, the entire `address` claim is treated as an object in the Disclosure.

```
{
  "_sd": [
    "fOBUSQvo46yQO-wRwXBcGqvnbKIueISEL961_Sjd4do"
  ],
  "iss": "https://issuer.example.com",
  "iat": 1683000000,
  "exp": 1883000000,
  "sub": "6c5c0a49-b589-431d-bae7-219122a9ec2c",
  "_sd_alg": "sha-256"
}
```

The Issuer would create the following Disclosure referenced by the one hash in the SD-JWT:

- 
            Claim `address`:

- 
                SHA-256 Hash:
`fOBUSQvo46yQO-wRwXBcGqvnbKIueISEL961_Sjd4do`

              - 
                Disclosure:
`WyIyR0xDNDJzS1F2ZUNmR2ZyeU5STjl3IiwgImFkZHJlc3MiLCB7InN0cmVldF9hZGRyZXNzIjogIlNjaHVsc3RyLiAxMiIsICJsb2NhbGl0eSI6ICJTY2h1bHBmb3J0YSIsICJyZWdpb24iOiAiU2FjaHNlbi1BbmhhbHQiLCAiY291bnRyeSI6ICJERSJ9XQ`

              - 
                Contents:
`["2GLC42sKQveCfGfryNRN9w", "address", {"street_address": "Schulstr. 12", "locality": "Schulpforta", "region": "Sachsen-Anhalt", "country": "DE"}]`

            

        


### 6.2. Example: Structured SD-JWT
The Issuer may instead decide to make the `address` claim contents selectively disclosable individually:

```
{
  "iss": "https://issuer.example.com",
  "iat": 1683000000,
  "exp": 1883000000,
  "sub": "6c5c0a49-b589-431d-bae7-219122a9ec2c",
  "address": {
    "_sd": [
      "6vh9bq-zS4GKM_7GpggVbYzzu6oOGXrmNVGPHP75Ud0",
      "9gjVuXtdFROCgRrtNcGUXmF65rdezi_6Er_j76kmYyM",
      "KURDPh4ZC19-3tiz-Df39V8eidy1oV3a3H1Da2N0g88",
      "WN9r9dCBJ8HTCsS2jKASxTjEyW5m5x65_Z_2ro2jfXM"
    ]
  },
  "_sd_alg": "sha-256"
}
```

In this case, the Issuer would use the following data in the Disclosures for the `address` sub-claims:

- 
            Claim `street_address`:

- 
                SHA-256 Hash:
`9gjVuXtdFROCgRrtNcGUXmF65rdezi_6Er_j76kmYyM`

              - 
                Disclosure:
`WyIyR0xDNDJzS1F2ZUNmR2ZyeU5STjl3IiwgInN0cmVldF9hZGRyZXNzIiwgIlNjaHVsc3RyLiAxMiJd`

              - 
                Contents:
`["2GLC42sKQveCfGfryNRN9w", "street_address", "Schulstr. 12"]`

            

          - 
            Claim `locality`:

- 
                SHA-256 Hash:
`6vh9bq-zS4GKM_7GpggVbYzzu6oOGXrmNVGPHP75Ud0`

              - 
                Disclosure:
`WyJlbHVWNU9nM2dTTklJOEVZbnN4QV9BIiwgImxvY2FsaXR5IiwgIlNjaHVscGZvcnRhIl0`

              - 
                Contents:
`["eluV5Og3gSNII8EYnsxA_A", "locality", "Schulpforta"]`

            

          - 
            Claim `region`:

- 
                SHA-256 Hash:
`KURDPh4ZC19-3tiz-Df39V8eidy1oV3a3H1Da2N0g88`

              - 
                Disclosure:
`WyI2SWo3dE0tYTVpVlBHYm9TNXRtdlZBIiwgInJlZ2lvbiIsICJTYWNoc2VuLUFuaGFsdCJd`

              - 
                Contents:
`["6Ij7tM-a5iVPGboS5tmvVA", "region", "Sachsen-Anhalt"]`

            

          - 
            Claim `country`:

- 
                SHA-256 Hash:
`WN9r9dCBJ8HTCsS2jKASxTjEyW5m5x65_Z_2ro2jfXM`

              - 
                Disclosure:
`WyJlSThaV205UW5LUHBOUGVOZW5IZGhRIiwgImNvdW50cnkiLCAiREUiXQ`

              - 
                Contents:
`["eI8ZWm9QnKPpNPeNenHdhQ", "country", "DE"]`

            

        
The Issuer may also make one sub-claim of `address` permanently disclosed and hide only the other sub-claims:

```
{
  "iss": "https://issuer.example.com",
  "iat": 1683000000,
  "exp": 1883000000,
  "sub": "6c5c0a49-b589-431d-bae7-219122a9ec2c",
  "address": {
    "_sd": [
      "6vh9bq-zS4GKM_7GpggVbYzzu6oOGXrmNVGPHP75Ud0",
      "9gjVuXtdFROCgRrtNcGUXmF65rdezi_6Er_j76kmYyM",
      "KURDPh4ZC19-3tiz-Df39V8eidy1oV3a3H1Da2N0g88"
    ],
    "country": "DE"
  },
  "_sd_alg": "sha-256"
}
```

In this case, there would be no Disclosure for `country`, since it is provided in the clear.


### 6.3. Example: SD-JWT with Recursive Disclosures
The Issuer may also decide to make the `address` claim contents selectively disclosable recursively, i.e., the `address` claim is made selectively disclosable as well as its sub-claims:

```
{
  "_sd": [
    "HvrKX6fPV0v9K_yCVFBiLFHsMaxcD_114Em6VT8x1lg"
  ],
  "iss": "https://issuer.example.com",
  "iat": 1683000000,
  "exp": 1883000000,
  "sub": "6c5c0a49-b589-431d-bae7-219122a9ec2c",
  "_sd_alg": "sha-256"
}
```

The Issuer first creates Disclosures for the sub-claims and then includes their digests in the Disclosure for the `address` claim:

- 
            Claim `street_address`:

- 
                SHA-256 Hash:
`9gjVuXtdFROCgRrtNcGUXmF65rdezi_6Er_j76kmYyM`

              - 
                Disclosure:
`WyIyR0xDNDJzS1F2ZUNmR2ZyeU5STjl3IiwgInN0cmVldF9hZGRyZXNzIiwgIlNjaHVsc3RyLiAxMiJd`

              - 
                Contents:
`["2GLC42sKQveCfGfryNRN9w", "street_address", "Schulstr. 12"]`

            

          - 
            Claim `locality`:

- 
                SHA-256 Hash:
`6vh9bq-zS4GKM_7GpggVbYzzu6oOGXrmNVGPHP75Ud0`

              - 
                Disclosure:
`WyJlbHVWNU9nM2dTTklJOEVZbnN4QV9BIiwgImxvY2FsaXR5IiwgIlNjaHVscGZvcnRhIl0`

              - 
                Contents:
`["eluV5Og3gSNII8EYnsxA_A", "locality", "Schulpforta"]`

            

          - 
            Claim `region`:

- 
                SHA-256 Hash:
`KURDPh4ZC19-3tiz-Df39V8eidy1oV3a3H1Da2N0g88`

              - 
                Disclosure:
`WyI2SWo3dE0tYTVpVlBHYm9TNXRtdlZBIiwgInJlZ2lvbiIsICJTYWNoc2VuLUFuaGFsdCJd`

              - 
                Contents:
`["6Ij7tM-a5iVPGboS5tmvVA", "region", "Sachsen-Anhalt"]`

            

          - 
            Claim `country`:

- 
                SHA-256 Hash:
`WN9r9dCBJ8HTCsS2jKASxTjEyW5m5x65_Z_2ro2jfXM`

              - 
                Disclosure:
`WyJlSThaV205UW5LUHBOUGVOZW5IZGhRIiwgImNvdW50cnkiLCAiREUiXQ`

              - 
                Contents:
`["eI8ZWm9QnKPpNPeNenHdhQ", "country", "DE"]`

            

          - 
            Claim `address`:

- 
                SHA-256 Hash:
`HvrKX6fPV0v9K_yCVFBiLFHsMaxcD_114Em6VT8x1lg`

              - 
                Disclosure:
`WyJRZ19PNjR6cUF4ZTQxMmExMDhpcm9BIiwgImFkZHJlc3MiLCB7Il9zZCI6IFsiNnZoOWJxLXpTNEdLTV83R3BnZ1ZiWXp6dTZvT0dYcm1OVkdQSFA3NVVkMCIsICI5Z2pWdVh0ZEZST0NnUnJ0TmNHVVhtRjY1cmRlemlfNkVyX2o3NmttWXlNIiwgIktVUkRQaDRaQzE5LTN0aXotRGYzOVY4ZWlkeTFvVjNhM0gxRGEyTjBnODgiLCAiV045cjlkQ0JKOEhUQ3NTMmpLQVN4VGpFeVc1bTV4NjVfWl8ycm8yamZYTSJdfV0`

              - 
                Contents:
`["Qg_O64zqAxe412a108iroA", "address", {"_sd": ["6vh9bq-zS4GKM_7GpggVbYzzu6oOGXrmNVGPHP75Ud0", "9gjVuXtdFROCgRrtNcGUXmF65rdezi_6Er_j76kmYyM", "KURDPh4ZC19-3tiz-Df39V8eidy1oV3a3H1Da2N0g88", "WN9r9dCBJ8HTCsS2jKASxTjEyW5m5x65_Z_2ro2jfXM"]}]`
