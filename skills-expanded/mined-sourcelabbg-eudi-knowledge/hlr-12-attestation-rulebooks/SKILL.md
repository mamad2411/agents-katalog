---
name: "hlr-12-attestation-rulebooks"
description: "Use when working with EUDI high-level requirements for 'Attestation Rulebooks'. Contains normative SHALL/SHOULD/MAY requirements from ARF Annex 2."
sections:
  - "A.2.3.9 Topic 12 - Attestation Rulebooks"
  - "A. Requirements regarding attestation formats <!-- omit from toc -->"
  - "B. Requirements regarding attestation types <!-- omit from toc -->"
  - "C. Requirements regarding attestation schemes <!-- omit from toc -->"
  - "D. Miscellaneous requirements <!-- omit from toc -->"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~6530 -->

#### A.2.3.9 Topic 12 - Attestation Rulebooks

##### A. Requirements regarding attestation formats <!-- omit from toc -->

<div class="eudi-hlr" id="ARB_01" markdown>
<div class="eudi-hlr__id">ARB_01<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Scheme Provider for an Attestation Rulebook describing a type of attestation that is a QEAA or a PuB-EAA SHALL specify that one or more of the following two common format(s) must be used for these attestations: - The format specified in ISO/IEC 18013-5, see [ISO/IEC 18013-5]. - The format specified in SD-JWT-based Verifiable Credentials (SD-JWT VC), see [SD-JWT VC].

</div>
</div>

<div class="eudi-hlr" id="ARB_01a" markdown>
<div class="eudi-hlr__id">ARB_01a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Scheme Provider for an Attestation Rulebook describing a type of attestation that is a non-qualified EAA SHALL specify that one or more of the following three common format(s) must be used for these attestations: - The format specified in ISO/IEC 18013-5, see [ISO/IEC 18013-5]. - The format specified in SD-JWT-based Verifiable Credentials (SD-JWT VC), see [SD-JWT VC]. - The format specified in W3C Verifiable Credentials Data Model, see [W3C VCDM v2.0].

</div>
</div>

<div class="eudi-hlr" id="ARB_01b" markdown>
<div class="eudi-hlr__id">ARB_01b<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Scheme Provider for an Attestation Rulebook describing attestations using the format specified in [SD-JWT VC] SHALL ensure that these attestations comply with the 'IETF SD-JWT VC Profile' specified in [HAIP] Section 6.1.

</div>
</div>

<div class="eudi-hlr" id="ARB_02" markdown>
<div class="eudi-hlr__id">ARB_02<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Scheme Provider for an Attestation Rulebook SHALL analyse whether it must be possible for a User to present that type of attestation when the Wallet Unit and the Relying Party are in proximity and attestations are presented without using the internet. If so, the Attestation Rulebook SHALL specify that the attestations must be issued in the ISO/IEC 18013-5-compliant mdoc format.

*Note: In theory, it is possible to use SD-JWT VC-compliant attestations in proximity use cases. In practice, however, the only protocol available to request and present SD-JWT VC-compliant attestations between a Wallet Unit and a Relying Party Instance is OpenID4VP. That protocol cannot be used without internet connectivity.*

</div>
</div>

<div class="eudi-hlr" id="ARB_03" markdown>
<div class="eudi-hlr__id">ARB_03<span class="kw-may">MAY</span></div>
<div class="eudi-hlr__body" markdown>

The Scheme Provider for an Attestation Rulebook MAY specify in the Attestation Rulebook that that type of attestation must be issued in the [SD-JWT VC]-compliant format, provided the [SD-JWT VC] specification has been approved by an EU standardisation body or by the European Digital Identity Cooperation Group established pursuant to [Article 46e](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32024R1183#d1e4536-1-1)(1) of the [European Digital Identity Regulation].

</div>
</div>

<div class="eudi-hlr" id="ARB_04" markdown>
<div class="eudi-hlr__id">ARB_04<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If an Attestation Rulebook specifies that a type of attestation can be issued in a format compliant with [W3C VCDM v2.0], the Scheme Provider for that Attestation Rulebook SHALL ensure the Rulebook references one or more documents specifying in detail how a Relying Party can request attributes from a such an attestation, and how a User can selectively disclose attributes from such an attestation. Moreover, these referenced documents SHALL be approved by an EU standardisation body or by the European Digital Identity Cooperation Group established pursuant to [Article 46e](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32024R1183#d1e4536-1-1)(1) of the [European Digital Identity Regulation].

</div>
</div>


##### B. Requirements regarding attestation types <!-- omit from toc -->

<div class="eudi-hlr" id="ARB_05" markdown>
<div class="eudi-hlr__id">ARB_05<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Scheme Provider for an Attestation Rulebook SHALL specify a value for the attestation type, which SHALL be unique within the scope of the EUDI Wallet ecosystem.

*Note: In ISO/IEC 18013-5, the attestation type is called 'document type' and is included as a `docType` key-value pair in both the mdoc request and the mdoc response. Also, a method for generating unique attestation type values is recommended. In OpenID4VP, the attestation type is included in the `meta` property of a Credential Query in a presentation request. In [SD-JWT VC], the attestation type is called 'SD-JWT VC type' and is included as a `vct` claim in the SD-JWT VC.*

</div>
</div>


##### C. Requirements regarding attestation schemes <!-- omit from toc -->

<div class="eudi-hlr" id="ARB_06" markdown>
<div class="eudi-hlr__id">ARB_06<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Scheme Provider for an Attestation Rulebook SHALL define all attributes that an attestation of that type may contain. This definition SHALL first describe the semantics of each attribute in an encoding-independent manner and SHALL subsequently for each attribute specify an ISO/IEC 18013-5-compliant format, an SD-JWT VC-compliant format, or both, as needed given the choices made according to ARB_01 - ARB_04.

</div>
</div>

<div class="eudi-hlr" id="ARB_06a" markdown>
<div class="eudi-hlr__id">ARB_06a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For ISO/IEC 18013-5-compliant attestations, the Attestation Rulebook SHALL define each attribute within an attribute namespace. An attribute namespace SHALL fully define the identifier, the syntax, and the semantics of each attribute within that namespace. An attribute namespace SHALL have an identifier that is unique within the scope of the EUDI Wallet ecosystem, and each attribute identifier SHALL be unique within that namespace.

*Note: In ISO/IEC 18013-5, namespaces are discussed and a method for generating unique namespace identifiers is recommended.*

</div>
</div>

<div class="eudi-hlr" id="ARB_06b" markdown>
<div class="eudi-hlr__id">ARB_06b<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For [SD-JWT VC]-compliant attestations, the Scheme Provider for the Attestation Rulebook SHALL ensure that each claim name is either: - included in the IANA registry for JWT claims, - is a Public Name as defined in [RFC 7519], or is a Private Name specific to the attestation type.

*Note: [SD-JWT VC] does not discuss how to avoid conflicting claim names. Since SD-JWTs are a special kind of JWTs, the methods specified in RFC 7519 are applicable.*

</div>
</div>

<div class="eudi-hlr" id="ARB_07" markdown>
<div class="eudi-hlr__id">ARB_07<span class="kw-should">SHOULD</span></div>
<div class="eudi-hlr__body" markdown>

When determining the attributes to be included in a new attestation type, the Scheme Provider for the applicable Attestation Rulebook SHOULD consider referring to attributes that are already included in the catalogue of attributes specified in [Topic 25][topic-25] or specified in an attestation scheme included in the catalogue of attestation schemes specified in [Commission Implementing Regulation 2025/1569](http://data.europa.eu/eli/reg_impl/2025/1569/oj), rather than unnecessarily re-defining all attributes.

</div>
</div>

<div class="eudi-hlr" id="ARB_08" markdown>
<div class="eudi-hlr__id">ARB_08<span class="kw-should">SHOULD</span></div>
<div class="eudi-hlr__body" markdown>

The Scheme Provider for an Attestation Rulebook SHOULD, when specifying a new attribute, take into consideration existing conventions for attribute identifier values and attribute syntaxes.

*Note: These conventions may depend on the format of the attestation, i.e., CBOR for ISO/IEC 18013-5-compliant attestations or JSON for SD-JWT VC-compliant attestations.*

</div>
</div>

<div class="eudi-hlr" id="ARB_09" markdown>
<div class="eudi-hlr__id">ARB_09<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Scheme Provider for an Attestation Rulebook SHALL specify, for each attribute in the attestation, whether the presence of that attribute is mandatory, optional, or conditional.

</div>
</div>

<div class="eudi-hlr" id="ARB_10" markdown>
<div class="eudi-hlr__id">ARB_10<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Scheme Provider for an Attestation Rulebook for an ISO/IEC 18013-5 compliant attestation MAY define a domestic namespace to specify attributes that are specific to that Rulebook and are not included in the applicable EU-wide or sectoral namespace. All requirements for namespaces in this Topic SHALL also apply for domestic namespaces.

</div>
</div>

<div class="eudi-hlr" id="ARB_11" markdown>
<div class="eudi-hlr__id">ARB_11<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Scheme Provider for an Attestation Rulebook describing a type of attestation that is a QEAA or a PuB-EAA SHALL include in the Rulebook an attribute as meant in [Annex V](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32024R1183#d1e40-54-1) point a) and [Annex VII](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32024R1183#d1e40-56-1) point a) of the [European Digital Identity Regulation]. This attribute SHALL reference the technical specification meant in ARB_25.

</div>
</div>

<div class="eudi-hlr" id="ARB_12" markdown>
<div class="eudi-hlr__id">ARB_12<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Scheme Provider for an Attestation Rulebook describing a type of attestation that is a non-qualified EAA SHOULD include an attribute in the Rulebook indicating that the attestation is an EAA. This attribute SHALL reference the technical specification meant in ARB_25.

</div>
</div>

<div class="eudi-hlr" id="ARB_13" markdown>
<div class="eudi-hlr__id">ARB_13<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Scheme Provider for an Attestation Rulebook describing a type of attestation that is a QEAA SHALL include in the Rulebook one or more attributes or metadata representing the set of data meant in [Annex V](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32024R1183#d1e40-54-1) point b) of the [European Digital Identity Regulation].

</div>
</div>

<div class="eudi-hlr" id="ARB_14" markdown>
<div class="eudi-hlr__id">ARB_14<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Scheme Provider for an attestation Rulebook describing a type of attestation that is a PuB-EAA SHALL include in the Rulebook one or more attributes or metadata representing the set of data meant in [Annex VII](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32024R1183#d1e40-56-1) point b) of the [European Digital Identity Regulation].

</div>
</div>

<div class="eudi-hlr" id="ARB_15" markdown>
<div class="eudi-hlr__id">ARB_15<span class="kw-should">SHOULD</span></div>
<div class="eudi-hlr__body" markdown>

The Scheme Provider for an Attestation Rulebook describing a type of attestation that is a non-qualified EAA SHOULD include in the Rulebook one or more attributes or metadata representing the set of data meant in [Annex V](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32024R1183#d1e40-54-1) point b) of the [European Digital Identity Regulation].

</div>
</div>

<div class="eudi-hlr" id="ARB_16" markdown>
<div class="eudi-hlr__id">ARB_16<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Scheme Provider for an Attestation Rulebook describing a type of attestation that is a QEAA or a PuB-EAA SHALL include in the Rulebook one or more attributes representing the set of data meant in [Annex V](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32024R1183#d1e40-54-1) point c) or [Annex VII](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32024R1183#d1e46-55-1) point c) of the [European Digital Identity Regulation].

</div>
</div>

<div class="eudi-hlr" id="ARB_17" markdown>
<div class="eudi-hlr__id">ARB_17<span class="kw-should">SHOULD</span></div>
<div class="eudi-hlr__body" markdown>

The Scheme Provider for an Attestation Rulebook describing a type of attestation that is a non-qualified EAA SHOULD include in the Rulebook one or more attributes representing the set of data meant in [Annex V](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32024R1183#d1e40-54-1) point c) of the [European Digital Identity Regulation].

</div>
</div>

<div class="eudi-hlr" id="ARB_18" markdown>
<div class="eudi-hlr__id">ARB_18<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Scheme Provider for an Attestation Rulebook describing a type of attestation that is a QEAA or a PuB-EAA SHALL include in the Rulebook one or more attributes or metadata representing the set of data meant in [Annex V](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32024R1183#d1e40-54-1) point e) or [Annex VII](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32024R1183#d1e40-56-1) point e) of the [European Digital Identity Regulation].

</div>
</div>

<div class="eudi-hlr" id="ARB_19" markdown>
<div class="eudi-hlr__id">ARB_19<span class="kw-should">SHOULD</span></div>
<div class="eudi-hlr__body" markdown>

The Scheme Provider for an Attestation Rulebook describing a type of attestation that is a non-qualified EAA SHOULD include in the Rulebook one or more attributes representing the set of data meant in [Annex V](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32024R1183#d1e40-54-1) point e) of the [European Digital Identity Regulation].

</div>
</div>

<div class="eudi-hlr" id="ARB_20" markdown>
<div class="eudi-hlr__id">ARB_20<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Scheme Provider for an Attestation Rulebook describing a type of attestation that is a QEAA or a PuB-EAA SHALL include in the Rulebook one or more attributes or metadata representing the location meant in [Annex V](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32024R1183#d1e40-54-1) point h) or [Annex VII](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32024R1183#d1e40-56-1) point h) of the [European Digital Identity Regulation]. This location SHALL indicate at least the URL at which a machine-readable version of the trust anchor to be used for verifying the QEAA or PuB-EAA can be found or looked up.

</div>
</div>

<div class="eudi-hlr" id="ARB_21" markdown>
<div class="eudi-hlr__id">ARB_21<span class="kw-should">SHOULD</span></div>
<div class="eudi-hlr__body" markdown>

The Scheme Provider for an Attestation Rulebook describing a type of attestation that is a non-qualified EAA SHOULD include in the Rulebook one or more attributes or metadata representing the location at which a machine-readable version of the trust anchor to be used for verifying the EAA can be found or looked up.

*Note: What this location indicates precisely is dependent on the nature of the mechanism used for distributing trust anchors - see requirement ARB_26.*

</div>
</div>


##### D. Miscellaneous requirements <!-- omit from toc -->

<div class="eudi-hlr" id="ARB_22" markdown>
<div class="eudi-hlr__id">ARB_22<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Scheme Provider for an Attestation Rulebook SHALL specify all technical details necessary to ensure interoperability, security, and privacy of that attestation.

*Note: An Attestation Rulebook may also specify requirements regarding how the Wallet Unit must display the attestation and the attributes in it to the User.*

</div>
</div>

<div class="eudi-hlr" id="ARB_23" markdown>
<div class="eudi-hlr__id">ARB_23<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Scheme Provider for an Attestation Rulebook describing a type of attestation that is a QEAA or a PuB-EAA SHALL specify which of the revocation mechanisms specified in [Topic 7][topic-7] SHALL be supported by that attestation.

</div>
</div>

<div class="eudi-hlr" id="ARB_24" markdown>
<div class="eudi-hlr__id">ARB_24<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Scheme Provider for an Attestation Rulebook describing a type of attestation that is a non-qualified EAA SHALL specify whether that type of EAA must be revocable. If an EAA type must be revocable, the relevant Rulebook SHALL determine which of the revocation mechanisms specified in [Topic 7][topic-7] SHALL be supported by that attestation.

</div>
</div>

<div class="eudi-hlr" id="ARB_24a" markdown>
<div class="eudi-hlr__id">ARB_24a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If an attestation is revocable, the relevant Attestation Rulebook SHALL specify the URL at which Relying Parties and other entities can retrieve the relevant Attestation Status Lists or Attestation Revocation Lists. 

*Note: This could be the domain name only, as the full URL containing the ASL or ARL relevant for an individual attestation will anyway be included in that attestation.*

</div>
</div>

<div class="eudi-hlr" id="ARB_25" markdown>
<div class="eudi-hlr__id">ARB_25<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

An Attribute Schema Provider SHALL include in its Attestation Rulebook the attribute `attestation_legal_category`, specified in the [Attestation Rulebook Template](https://github.com/eu-digital-identity-wallet/eudi-doc-attestation-rulebooks-catalog/blob/main/template/attestation-rulebook-template.md), with the appropriate value as specified in the Template.

*Note: This attribute contains the indication meant in [Annex V](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32024R1183#d1e40-54-1) point a) and [Annex VII](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32024R1183#d1e40-56-1) point a).*

</div>
</div>

<div class="eudi-hlr" id="ARB_26" markdown>
<div class="eudi-hlr__id">ARB_26<span class="kw-should">SHOULD</span></div>
<div class="eudi-hlr__body" markdown>

The Scheme Provider for an Attestation Rulebook describing a type of attestation that is a non-qualified EAA SHOULD define in the Rulebook the mechanism(s) allowing a Relying Party to obtain, in a trustworthy manner, the trust anchor(s) of the EAA Providers issuing this type of EAA.

*Note: [Technical Specification 11][ts11], section 4.3.1, recommends the use of the List of trusted entities (LoTE) data model as defined in [ETSI TS 119 602] for non-qualified EAAs.*

</div>
</div>

<div class="eudi-hlr" id="ARB_27" markdown>
<div class="eudi-hlr__id">ARB_27</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="ARB_28" markdown>
<div class="eudi-hlr__id">ARB_28<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

An Attribute Scheme Provider MAY specify an attribute in an Attestation Rulebook that indicates whether the Attestation Provider during attestation issuance requested a cryptographic binding (as specified in [Topic 18][topic-18]) between the new attestation and an existing PID or attestation. If present in a Rulebook, the identifier for this attribute SHALL be `cryptographically_bound_to`, and its contents SHALL be an attestation type or vct (see ARB_05).

*Note: The meaning of this attribute, if present, is that this attestation is cryptographically bound to one or more attestations of the given attestation type or vct on this Wallet Unit. If a Relying Party receives this attribute from a Wallet Unit, it can subsequently request the Wallet Unit to send a proof of cryptographic binding between the attestation and an attestation indicated in the `cryptographically_bound_to` attribute.*

</div>
</div>

<div class="eudi-hlr" id="ARB_29" markdown>
<div class="eudi-hlr__id">ARB_29<span class="kw-should">SHOULD</span></div>
<div class="eudi-hlr__body" markdown>

The Scheme Provider for an Attestation Rulebook describing a type of attestation that is a QEAA, PuB-EAA, or non-qualified EAA SHOULD ensure that the structure and contents of the Attestation Rulebook follow the descriptions in the [Attestation Rulebook template](https://github.com/eu-digital-identity-wallet/eudi-doc-attestation-rulebooks-catalog/blob/main/template/attestation-rulebook-template.md).

</div>
</div>

<div class="eudi-hlr" id="ARB_30" markdown>
<div class="eudi-hlr__id">ARB_30<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If an Attestation Rulebook specifies a [SD-JWT VC]-compliant attestation, the Scheme Provider for that Attestation Rulebook SHALL specify for all claims (i.e., all top-level properties, all nested properties, and all array entries) whether an Attestation Provider MUST, MAY, or MUST NOT make that claim selectively disclosable.

*Note: a) This requirement does not apply to claims defined as non-selectively disclosable in [SD-JWT VC]. b) There will be use cases where a specific claim must not be disclosed without simultaneously disclosing one or more other claims. Such cases should be solved by making all of these claims members of the same JSON object (or elements of the same JSON array). That JSON object (or array) is then the claim that must be selectively disclosable, while the nested properties (or individual array elements) must not be selectively disclosable. c) This requirement does not apply to [ISO/IEC 18013-5]-compliant attestations, since in such attestations, by definition all data elements are selectively disclosable, while none of the key-value pairs or array elements inside a data element (if any) are selectively disclosable.*

</div>
</div>

<div class="eudi-hlr" id="ARB_31" markdown>
<div class="eudi-hlr__id">ARB_31<span class="kw-should">SHOULD</span></div>
<div class="eudi-hlr__body" markdown>

If an Attestation Rulebook specifies a [SD-JWT VC]-compliant attestation, the Scheme Provider for that Attestation Rulebook SHOULD consider defining a Type Metadata Document for it, as defined in Chapter 6 of [SD-JWT VC]. If the Scheme Provider defines such a document, it SHOULD contain the Claim Selective Disclosure Metadata (defined in Section 9.3 of [SD-JWT VC]) for each of the claims, in order to specify if that claim is selectively disclosable (see requirement ARB_30).

*Note: Although a Type Metadata Document is a highly technical document, defining it has a number of advantages for developers, Attestation Providers, Relying Parties, and Wallet Units, as spelled out in Chapter 6 of [SD-JWT VC].*

</div>
</div>

<div class="eudi-hlr" id="ARB_32" markdown>
<div class="eudi-hlr__id">ARB_32</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="ARB_33" markdown>
<div class="eudi-hlr__id">ARB_33<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If a Scheme Provider for an Attestation Rulebook registers an attestation scheme in the catalogue of attestation schemes meant in [Commission Implementing Regulation 2025/1569](http://data.europa.eu/eli/reg_impl/2025/1569/oj), Article 8, the registration SHALL include a reference to the corresponding Attestation Rulebook.

*Note: By definition, an attestation scheme is machine-readable, whereas an Attestation Rulebook is human-readable.*

</div>
</div>

<div class="eudi-hlr" id="ARB_34" markdown>
<div class="eudi-hlr__id">ARB_34<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Scheme Provider for an Attestation Rulebook SHALL specify whether that attestation is device-bound or not.

</div>
</div>


[](){ #topic-16 }
