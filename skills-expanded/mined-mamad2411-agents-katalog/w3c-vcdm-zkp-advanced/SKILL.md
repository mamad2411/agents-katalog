---
name: "w3c-vcdm-zkp-advanced"
description: "Use when implementing advanced W3C VCDM features beyond basic credential structure. Covers: zero-knowledge proofs, time, authorization, and reserved extensions."
sections:
  - "5.7 Zero-Knowledge Proofs"
  - "5.8 Representing Time"
  - "5.9 Authorization*This section is non-normative.*"
  - "5.10 Reserved Extension Points"
---

<!-- ARF version: 2.0-2024-12-04 -->
<!-- Tokens: ~6209 -->

### 5.7 Zero-Knowledge Proofs
        

        
Zero-knowledge proofs are [securing mechanisms](https://www.w3.org/TR/vc-data-model-2.0/#securing-mechanisms)
which enable a [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) to prove that they hold a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential)
containing a value without disclosing the actual value such as being able to
prove that an individual is over the age of 25 without revealing their birthday.
This data model supports being secured using zero-knowledge proofs.
        
        
Some capabilities that are compatible with [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) which are
made possible by zero-knowledge proof mechanisms include:
        
        
          - 
[Selective disclosure](https://www.w3.org/TR/vc-data-model-2.0/#dfn-selective-disclosure) of the properties in a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) by the
[holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) to a [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier). This allows a [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) to provide a [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier)
with precisely the information they need and nothing more. This also enables the
production of a derived [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) that is formatted according to
the [verifier's](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) data schema without needing to involve the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) during
presentation. This provides a great deal of flexibility for [holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) to use
their issued [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential).
          
          - 
[Unlinkable disclosure](https://www.w3.org/TR/vc-data-model-2.0/#dfn-unlinkable-disclosure) of the properties in a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) by
the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) to a [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier). Blinded signatures allow for [unlinkable disclosure](https://www.w3.org/TR/vc-data-model-2.0/#dfn-unlinkable-disclosure), which remove a common source of [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) correlation during
multiple presentations to one or more [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier). This allows a [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) to
share a different signature value with each presentation, which in turn reduces
the amount of data shared.
          
          - 
Non-correlatable identification of the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) and/or [subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects). This
allows a [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) to prove that a [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) was issued to them, or a
[subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects) to prove that a [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) was issued about them, without
sharing a correlatable identifier. This also reduces the amount of data
necessary to be shared. This capability can also be used to combine multiple
[verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) from multiple [issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) into a single [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) without revealing [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) or [subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects)
identifiers to the [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier).
          
        
        
Specification authors that create
[securing mechanisms](https://www.w3.org/TR/vc-data-model-2.0/#securing-mechanisms) MUST NOT design them in
such a way that they leak information that would enable the [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) to
correlate a [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) across multiple [verifiable presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) to different
[verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier).
        
        
Not all capabilities are supported in all zero-knowledge proof mechanisms.
Specific details about the capabilities and techniques provided by a particular
zero knowledge proof mechanism, along with any normative requirements for using
them with [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential), would be found in a specification for
securing [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) with that zero-knowledge proof mechanism.
For an example of such a specification, refer to the [Data Integrity BBS Cryptosuites v1.0](https://www.w3.org/TR/vc-di-bbs/).
        
        
We note that in most instances, for the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) to make use of zero knowledge
mechanisms with [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential), the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) is required to secure
the [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) in a manner that supports these capabilities.
        
        
The diagram below highlights how the data model might be used to issue and
present [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) in zero-knowledge.
        

        
          
          [Figure 12](https://www.w3.org/TR/vc-data-model-2.0/#fig-a-visual-example-of-the-relationship-between-credentials-and-derived-credentials-in-a-zkp-presentation) 
A visual example of the relationship between credentials and derived
credentials in a ZKP [presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-presentation).
          
        

        
An example of a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) and a [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation)
using the [Data Integrity BBS Cryptosuites v1.0](https://www.w3.org/TR/vc-di-bbs/) unlinkable selective disclosure securing mechanism is
shown below.
        

        
        
    [Example 30](https://www.w3.org/TR/vc-data-model-2.0/#example-verifiable-credential-using-the-data-integrity-bbs-cryptosuite-with-a-base-proof): Verifiable credential using the Data Integrity BBS Cryptosuite with a Base Proof
   ```
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://w3id.org/citizenship/v3"
  ],
  "type": ["VerifiableCredential", "PermanentResidentCard"],
  "issuer": {
    "id": "did:web:credentials.utopia.example",
    "image": "data:image/png;base64,iVBORw0KGgo...YII="
  },
  "identifier": "83627465",
  "name": "Permanent Resident Card",
  "description": "Government of Utopia Permanent Resident Card.",
  "validFrom": "2024-08-01T00:00:00Z",
  "validUntil": "2029-12-01T00:00:00Z",
  "credentialSubject": {
    "type": ["PermanentResident", "Person"],
    "givenName": "JANE",
    "familyName": "SMITH",
    "gender": "Female",
    "image": "data:image/png;base64,iVBORw0KGgoAA...Jggg==",
    "residentSince": "2015-01-01",
    "lprCategory": "C09",
    "lprNumber": "999-999-999",
    "commuterClassification": "C1",
    "birthCountry": "Arcadia",
    "birthDate": "1978-07-17"
  },
  "proof": {
    "type": "DataIntegrityProof",
    "verificationMethod": "did:web:playground.alpha.chapi.io#zUC75LjjCLGKRxSissX1nAebRDmY4Bv4T6MAbzgaap9Q8rAGf6SEjc2Hf4nH6bUPDwky3GWoYcUjMCcEqRRQfXEiNwfeDwNYLoeqk1J1W2Ye8vCdwv4fSd8AZ1yS6UoNzcsQoPS",
    "cryptosuite": "bbs-2023",
    "proofPurpose": "assertionMethod",
    "proofValue": "u2V0ChVhQjYs9O7wUb3KRSMaIRX7jmafVHYDPYBLD4ta85_qmuXTBU_t2Ir7pNujwRE6fERsBUEZRSjJjtI-hqOqDs3VvBvH6gd3o2KeUS2V_zpuphPpYQEkapOeQgRTak9lHKSTqEQqa4j2lyHqekEeGvzPlqcHQGFccGifvLUXtP59jCuGJ86HDA9HL5kDzUT6n4Gi50HlYYIzNqhbjIxlqOuxO2IgIppSTWjQGeer34-PmKnOzKX8m_9DHPhif7TUf5uTV4OQWdhb0SxHnJ-CPu_z9FJ5ACekBQhz6YWS0_CY6j_ibucXzeVfZwLv1W47pjbt-l1Vl5VggSn2xVt69Q0GD9mPKpOhkKV_hyOL7i6haf7bq-gOKAwWDZy9pc3N1ZXJtL2lzc3VhbmNlRGF0ZW8vZXhwaXJhdGlvbkRhdGU"
  }
}
```
      

        
The example above is a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) where the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) has
enabled a BBS-based unlinkable disclosure scheme to create a base proof that
can then be used by the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) to create a derived proof that reveals only
particular pieces of information from the original [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential).
        

        
        
    [Example 31](https://www.w3.org/TR/vc-data-model-2.0/#example-verifiable-presentation-using-the-data-integrity-bbs-cryptosuite-with-a-derived-credential-and-proof): Verifiable presentation using the Data Integrity BBS Cryptosuite with a derived credential and proof
   ```
{
  @context: "https://www.w3.org/ns/credentials/v2"
  type: "VerifiablePresentation",
  verifiableCredential: {
    "@context": [
      "https://www.w3.org/ns/credentials/v2",
      "https://w3id.org/citizenship/v3"
    ],
    "type": ["VerifiableCredential", "PermanentResidentCard"],
    "issuer": {
      "id": "did:web:issuer.utopia.example",
      "image": "data:image/png;base64,iVBORw0KGgo...YII="
    },
    "name": "Permanent Resident Card",
    "description": "Government of Utopia Permanent Resident Card.",
    "validFrom": "2024-08-01T00:00:00Z",
    "validUntil": "2029-12-01T00:00:00Z",
    "credentialSubject": {
      "type": ["PermanentResident", "Person"],
      "birthCountry": "Arcadia"
    },
    "proof": {
      type: "DataIntegrityProof",
      verificationMethod: "did:web:issuer.utopia.example#zUC75LjjCLGKRxSissX1nAebRDmY4Bv4T6MAbzgaap9Q8rAGf6SEjc2Hf4nH6bUPDwky3GWoYcUjMCcEqRRQfXEiNwfeDwNYLoeqk1J1W2Ye8vCdwv4fSd8AZ1yS6UoNzcsQoPS",
      cryptosuite: "bbs-2023",
      proofPurpose: "assertionMethod",
      proofValue: "u2V0DhVkCkLdnshxHtgeHJBBUGPBqcEooPp9ahgqs08RsoqW5EJFmsi70jqf2X368VcmfdJdYcYJwObPIg5dlyaoBm34N9BqcZ4RlTZvgwX79ivGnqLALC0EqKn2wOj5hRO76xUakfLGIcT4mE-G7CxA1FTs8sRCWy5p6FozelBYiZU2YlhUpJ7pBwelZ9wnlcbj4q-KyxAj5GU2iWp7-FxU-E624DmdT-yvCkAGRRrYej6lMwg7jB9uCHypOXXH2dVZ-jpf74YBaE4rMTxPFh60GN4o3S65F1fMsJbEMLdrXa8Vs6ZSlmveUcY1X7oPr1UIxo17ehVTCjOxWunYqrtLi9cVkYOD2s9XMk1oFVWBB3UY29axXQQXlZVfvTIUsfVc667mnlYbF7a-ko_SUfeY2n3s1DOAap5keeNU0v2KVPCbxA2WGz7UJy4xJv2a8olMOWPKjAEUruCx_dsbyicd-9KGwhYoUEO3HoAzmtI6qXVhMbJKxPrhtcp8hOdD9izVS5ed4CxHNaDGPSopF_MBwjxwPcpUufNNNdQwesrbtFJo0-P-1CrX_jSxKFMle2b3t24UbHRbZw7QnX4OG-SSVucem5jpMXTDFZ8PLFCqXX0zncJ_MQ-_u-liE-MwJu3ZemsXBp1JoB2twS0TqDVzSWR7bpFZKI9_07fKUAmQNSV_no9iAgYRLuPrnnsW1gQgCV-nNqzbcCOpzkHdCqro6nPSATq5Od3Einfc683gm5VGWxIldM0aBPytOymNz7PIZ6wkgcMABMe5Vw46B54ftW-TN5YZPDmCJ_kt7Mturn0OeQr9KJCu7S0I-SN14mL9KtGE1XDnIeR-C_YZhSA3vX4923v1l3vNFsKasqy9iEPHKM0hcogABAQCGAAECBAUGhAMJCgtYUnsiY2hhbGxlbmdlIjoiNGd2OFJyaERPdi1OSHByYlZNQlM1IiwiZG9tYWluIjoiaHR0cHM6Ly9wbGF5Z3JvdW5kLmFscGhhLmNoYXBpLmlvIn0"
    }
  }
}
```
      

        
The [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) above includes a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) that
contains an unlinkable subset of the information from the previous example and a
derived proof that the [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) can use to verify that the information
originated from the expected [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) and is bound to this particular
exchange of information.

---

### 5.8 Representing Time
        

        
Implementers are urged to understand that representing and processing time
values is not as straight-forward as it might seem and have a variety of
idiosyncrasies that are not immediately obvious nor uniformly observed in
different regions of the world. For example:
        

        
          - 
Calendaring systems other than the Gregorian calendar are actively used by
various regions.
          
          - 
When processing Daylight Saving/Summer Time, it is important to understand that
1) it is not observed in all regions, 2) it does not necessarily begin or end on
the same day or at the same time of day, and 3) the amount or direction of the
adjustment does not always match other similar regions.
          
          - 
Leap seconds might not be taken into account in all software systems, especially
for dates and times that precede the introduction of the leap second. Leap
seconds can affect highly sensitive systems that depend on the exact
millisecond offset from the epoch. However, note that for most applications the
only moment in time that is affected is the one second period of the leap second
itself. That is, the moment after the most recent leap second can always be
represented as the first moment of the next day (for example,
`2023-01-01T00:00:00Z`), regardless of whether the system in question
understands leap seconds.
          
        

        
These are just a few examples that illustrate that the actual time of day, as
would be seen on a clock on the wall, can exist in one region but not exist in
another region. For this reason, implementers are urged to use time values
that are more universal, such as values anchored to the `Z` time zone over
values that are affected by Daylight Saving/Summer Time.
        

        
This specification attempts to increase the number of universally recognized
combinations of dates and times, and reduce the potential for
misinterpretation of time values, by using the
`dateTimeStamp` construction first established by the [[XMLSCHEMA11-2](https://www.w3.org/TR/xmlschema11-2/#dateTimeStamp)] specification. In
order to reduce misinterpretations between different time zones, all time values
expressed in [conforming documents](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-document) SHOULD be specified in `dateTimeStamp`
format, either in Universal Coordinated Time (UTC), denoted by a `Z` at the end
of the value, or with a time zone offset relative to UTC. Time values that are
incorrectly serialized without an offset MUST be interpreted as UTC. Examples of
valid time zone offsets relative to UTC include `Z`, `+01:00`, `-08:00`, and
`+14:00`. See the regular expression at the end of this section for a formal
definition of all acceptable values.
        

        
Time zone definitions are occasionally changed by their governing body. When
replacing or issuing new [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential), implementers are advised
to ensure that changes to local time zone rules do not result in unexpected gaps
in validity. For example, consider the zone `America/Los_Angeles`, which has
a raw offset of UTC-8 and had voted to stop observing daylight savings time in
the year 2024. A given [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) that had a `validUtil`
value of `2024-07-12T12:00:00-07:00`, might be re-issued to have a
`validFrom` value of `2024-07-12T12:00:00-08:00`, which would create a gap of
an hour where the [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) would not be valid.
        

        
Implementers that desire to check `dateTimeStamp` values for validity
can use the regular expression provided below, which is reproduced from the [[XMLSCHEMA11-2](https://www.w3.org/TR/xmlschema11-2/#dateTimeStamp)] specification for
convenience. To avoid doubt, the regular expression in [[XMLSCHEMA11-2](https://www.w3.org/TR/vc-data-model-2.0/#bib-xmlschema11-2)] is the
normative definition. Implementers are advised that not all
`dateTimeStamp` values that pass the regular expression below are
valid moments in time. For example, the regular expression below allows for 31
days in every month, which allows for leap years, and leap seconds, as well as
days in places where they do not exist. That said, modern system libraries that
generate `dateTimeStamp` values are often error-free in their
generation of valid `dateTimeStamp` values. The regular
expression shown below (minus the whitespace included here for readability),
is often adequate when processing library-generated dates and times on
modern systems.
        

        
        
    [Example 32](https://www.w3.org/TR/vc-data-model-2.0/#example-regular-expression-to-detect-a-valid-xml-schema-1-1-part-2-datetimestamp): Regular expression to detect a valid XML Schema 1.1: Part 2 dateTimeStamp
   ```
-?([1-9][0-9]{3,}|0[0-9]{3})
-(0[1-9]|1[0-2])
-(0[1-9]|[12][0-9]|3[01])
T(([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](\.[0-9]+)?|(24:00:00(\.0+)?))
(Z|(\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00))
```

---

### 5.9 Authorization*This section is non-normative.*
        

        
[Verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) are intended as a means of reliably identifying
[subjects](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects). While it is recognized that Role Based Access Controls (RBACs)
and Attribute Based Access Controls (ABACs) rely on this identification as a
means of authorizing [subjects](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects) to access resources, this specification
does not provide a complete solution for RBAC or ABAC. Authorization is not an
appropriate use for this specification without an accompanying authorization
framework.
        

        
The Working Group did consider authorization use cases during the creation of
this specification and is pursuing that work as an architectural layer built
on top of this specification.

---

### 5.10 Reserved Extension Points
        

        
This specification reserves a number of [properties](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) to serve as possible
extension points. While some implementers signaled interest in these properties,
their inclusion in this specification was considered to be premature. It is
important to note that none of these properties are defined by this
specification. Consequently, implementers are cautioned that use of these
properties is considered experimental.
        
        
Implementers MAY use these properties, but SHOULD expect them and/or
their meanings to change during the process of normatively specifying them.
Implementers SHOULD NOT use these properties without a publicly disclosed
specification describing their implementation.
        

        
In order to avoid collisions regarding how the following properties are used,
implementations MUST specify a `type` property in the value associated with the
reserved property. For more information related to adding `type` information,
see Section [4.5 Types](https://www.w3.org/TR/vc-data-model-2.0/#types).
        

        
          
            
              Reserved Property
              Description
            
          

          
            
              `confidenceMethod`
              
A property used for specifying one or more methods that a verifier might use to
increase their confidence that the value of a property in or of a verifiable
credential or verifiable presentation is accurate. The associated vocabulary
URL MUST be `https://www.w3.org/2018/credentials#confidenceMethod`.
              
            
            
              `renderMethod`
              
A property used for specifying one or more methods to render a credential into a
visual, auditory, haptic, or other format. The associated vocabulary URL MUST be
`https://www.w3.org/2018/credentials#renderMethod`.
              
            
          
        


        
An unofficial list of specifications that are associated with the extension
points defined in this specification, as well as the reserved extension points
defined in this section, can be found in the [Verifiable Credential Extensions](https://w3c.github.io/vc-extensions/). Items in the
directory that refer to reserved extension points SHOULD be treated as
experimental.
