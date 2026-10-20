---
name: "hlr-10-issuing-a-pid-or-attestation-to-a-wallet-part-1"
description: "Use when working with EUDI high-level requirements for 'Issuing a PID or attestation to a Wallet Unit' (Part 1). Contains normative requirements from ARF Annex 2."
sections:
  - "A.2.3.7 Topic 10 - Issuing a PID or attestation to a Wallet Unit"
  - "A - Generic HLRs <!-- omit from toc -->"
  - "B - HLRs for PID issuance <!-- omit from toc -->"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~6841 -->

#### A.2.3.7 Topic 10 - Issuing a PID or attestation to a Wallet Unit

##### A - Generic HLRs <!-- omit from toc -->

<div class="eudi-hlr" id="ISSU_01" markdown>
<div class="eudi-hlr__id">ISSU_01<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Wallet Providers SHALL ensure that their Wallet Solution supports the OpenID4VCI protocol specified in [OpenID4VCI], as profiled in Sections 4 and 6 of [HAIP], and with additions and changes as documented in this Annex (see e.g. this Topic and [Topic 9][topic-9]) and in [Technical Specification 3](../../technical-specifications/ts3-wallet-unit-attestation.md).

*Note: For clarity: in [HAIP] v1.0, Section 6 implies that Wallet Units must comply with the applicable requirements in [OpenID4VCI] Annex A.2 when requesting the issuance of an attestation in ISO/IEC 18013-5-compliant format, and with the applicable requirements in [OpenID4VCI] Annex A.3 when requesting the issuance of an attestation in SD-JWT VC format.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_01a" markdown>
<div class="eudi-hlr__id">ISSU_01a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

PID Providers and Attestation Providers SHALL support the OpenID4VCI protocol specified in [OpenID4VCI], as profiled in Sections 4 and 6 of [HAIP], and with additions and changes as documented in this Annex (see e.g. this Topic and [Topic 9][topic-9]) and in [Technical Specification 3](../../technical-specifications/ts3-wallet-unit-attestation.md).

*Note: a) For clarity: in [HAIP] v1.0, Section 6 implies that PID Providers and Attestation Providers must comply with the applicable requirements in [OpenID4VCI] Annex A.2 when issuing an attestation in ISO/IEC 18013-5-compliant format, and with the applicable requirements in [OpenID4VCI] Annex A.3 when issuing an attestation in SD-JWT VC format. b) In addition to supporting [OpenID4VCI], PID Providers are allowed to support other protocols for issuing PIDs to (national) Wallet Units, provided these protocols comply with all relevant requirements in the Implementing Acts and the standards referenced therein. In many Member States, the PID Provider and the Wallet Provider are closely related, and can therefore bilaterally agree to support a different protocol for PID issuance. *

</div>
</div>

<div class="eudi-hlr" id="ISSU_02" markdown>
<div class="eudi-hlr__id">ISSU_02<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Wallet Providers SHALL ensure that their Wallet Solution supports the attestation formats specified in ISO/IEC 18013-5, see [ISO/IEC 18013-5], and in SD-JWT-based Verifiable Credentials (SD-JWT VC), see [SD-JWT VC], with additions and changes as documented in this Annex and in [ETSI TS 119 472-1].

</div>
</div>

<div class="eudi-hlr" id="ISSU_03" markdown>
<div class="eudi-hlr__id">ISSU_03<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Wallet Units, PID Providers, and Attestation Providers SHALL support the [W3C Digital Credentials API](https://wicg.github.io/digital-credentials/) for the issuance of PIDs and attestations.

*Note: This requirement implies that the following conditions will be satisfied: a) the DC API specification will become a W3C Recommendation, b) this specification will comply with the principles outlined in [Section 4.4.3.1][4431-introduction] of the ARF main document, c) this specification will be broadly supported by relevant browsers and operating systems, and d) the [OpenID4VCI] standard will specify how to use OpenID4VCI with the DC API.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_04" markdown>
<div class="eudi-hlr__id">ISSU_04</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="ISSU_05" markdown>
<div class="eudi-hlr__id">ISSU_05<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL support a process to activate a newly issued PID, in accordance with the requirements for LoA High in [Commission Implementing Regulation (EU) 2015/1502](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32015R1502) Section 2.2.2. The Wallet Unit SHALL NOT allow a User to use a non-activated PID.

*Note: a) The goal of the activation process is to verify that the PID was delivered into the Wallet Unit and WSCA/WSCD of the User who is the subject of the PID. b) This requirement is not applicable for QEAAs, PuB-EAAs or non-qualified EAAs, since these are not identity means in the sense of Commission Implementing Regulation (EU) 2015/1502.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_06" markdown>
<div class="eudi-hlr__id">ISSU_06<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

After a Wallet Unit receives a PID or an attestation from a PID Provider or Attestation Provider, it SHALL verify that the PID or attestation it received matches the PID or attestation requested by the Wallet Unit.

</div>
</div>

<div class="eudi-hlr" id="ISSU_07" markdown>
<div class="eudi-hlr__id">ISSU_07<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

After a Wallet Unit receives a PID from a PID Provider, it SHALL validate the signature of the PID using a trust anchor of the PID Provider provided in a LoTE made available in accordance with [Topic 31][topic-31]].

*Note: The Wallet Provider and PID Provider may be the same entity. In such a case, the remote WSCD used by the Wallet Provider may be the same hardware HSM that is also used by the PID Provider to sign PIDs. In such a situation, this requirement may look superfluous, since the same HSM would generate the signature and verify it. However, this is not true, since for security reasons the PID Provider and Wallet Provider must use proper partitioning and logical key segregation within the HSM. Therefore, this requirement also applies in such a situation.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_08" markdown>
<div class="eudi-hlr__id">ISSU_08<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

After a Wallet Unit receives a QEAA from a QEAA Provider, it SHALL validate the qualified signature of the QEAA in accordance with Art. 32 of the [European Digital Identity Regulation]. For the verification, the Wallet Unit SHALL use a trust anchor provided in a QEAA Provider Trusted List made available in accordance with [Art. 22](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=uriserv%3AOJ.L_.2014.257.01.0073.01.ENG#d1e2162-73-1) of the [European Digital Identity Regulation].

*Note: a) Requirements ISSU_07 to ISSU_10 are equivalent to requirements OIA_12 to OIA_15 in [Topic 1][topic-1]. b) These requirements imply that a Wallet Unit must be aware whether the attestation it is requesting from an issuer is a PID, a QEAA, a PuB-EAA, or a non-qualified EAA. These requirements also imply that the Wallet Unit must store trust anchors in such a way that, when it receives an issued attestation, it is able to distinguish between trust anchors usable either for PIDs, for QEAAs, for PuB-EAAs, or for non-qualified EAAs.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_09" markdown>
<div class="eudi-hlr__id">ISSU_09<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

After a Wallet Unit receives a PuB-EAA from a PUB-EAA Provider, it SHALL validate the signature of a PuB-EAA using a trust anchor provided in a Pub-EAA Provider LoTE made available in accordance with [[Topic 31][topic-31]].

</div>
</div>

<div class="eudi-hlr" id="ISSU_10" markdown>
<div class="eudi-hlr__id">ISSU_10<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

After a Wallet Unit receives a non-qualified EAA from an EAA Provider, it SHALL validate the signature of the EAA if it has access to the trust anchors of the EAA Provider.

*Note: For a non-qualified EAA, an Attestation Rulebook may be available, see [[Topic 12][topic-12]], explaining how EAA Providers distribute their trust anchors. However, it is not required for Wallet Units to be in possession of the trust anchors of all non-qualified EAA Providers, even when an Attestation Rulebook is available.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_10a" markdown>
<div class="eudi-hlr__id">ISSU_10a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Provider SHALL perform regular trust anchor management, meaning it SHALL download the latest version of all applicable Trusted Lists and LoTEs. If it finds that new trusted entities have been added, or that new trust anchors have been added for existing trusted entities, it SHALL ensure that these trust anchors are properly stored in all relevant Wallet Units. Conversely, if the Wallet Provider finds that an existing trusted entity has been invalidated in the Trusted List or LoTE, or that some of the trust anchors of existing trusted entities have expired, been revoked, or otherwise been invalidated, it SHALL ensure that these trust anchors are removed from all Wallet Units.

</div>
</div>

<div class="eudi-hlr" id="ISSU_10b" markdown>
<div class="eudi-hlr__id">ISSU_10b<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For the retrieval and management of trust anchors, Wallet Providers and Wallet Units SHALL support both Trusted Lists complying with [ETSI TS 119 612] and LoTEs complying with [ETSI TS 119 602].

*Note: Trusted Lists complying with [ETSI TS 119 612] are used for the distribution of trust anchors of QEAA Providers. LoTEs complying with [ETSI TS 119 602] are used for the distribution of trust anchors of PID Providers, PuB-EAA Providers, Access Certificate Authorities, and Providers of registration certificates.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_11" markdown>
<div class="eudi-hlr__id">ISSU_11<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL request the User's approval before storing a PID or attestation obtained from a PID Provider or Attestation Provider. When requesting approval, the Wallet Instance SHALL display the contents of the PID or attestation to the User. The Wallet Instance SHALL also inform the User about the identity of the PID Provider or Attestation Provider, using the subject information in the PID Provider's or Attestation Provider's access certificate.

</div>
</div>

<div class="eudi-hlr" id="ISSU_11a" markdown>
<div class="eudi-hlr__id">ISSU_11a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

In case a PID or attestation is issued in batches, the Wallet Unit SHALL verify that all PIDs and attestations in a batch have the same attribute values and the same technical validity period.

*Note: PIDs and attestations are issued in batches when Method A, Method B, or Method D is used, see ISSU_37, ISSU_43, ISSU_51.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_11b" markdown>
<div class="eudi-hlr__id">ISSU_11b<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

In case one or more of the verifications in ISSU_06 - ISSU_11a fail, the Wallet Unit SHALL immediately delete the PID or attestation it received. The Wallet Instance SHALL notify the User about the fact that issuance of the PID or attestation was not successful, including the reason for this failure.

</div>
</div>

<div class="eudi-hlr" id="ISSU_12" markdown>
<div class="eudi-hlr__id">ISSU_12<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A PID Provider or Attestation Provider SHALL offer its PIDs or attestations in all formats required in the PID Rulebook or the applicable Attestation Rulebook, see [Topic 12][topic-12]].

*Note: Examples include the mdoc format specified in [ISO/IEC 18013-5] and the SD-JWT VC-format specified in [SD-JWT VC].*

</div>
</div>

<div class="eudi-hlr" id="ISSU_12a" markdown>
<div class="eudi-hlr__id">ISSU_12a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

When a User instructs their Wallet Unit to request a PID or attestation from a PID Provider or Attestation Provider, the Wallet Unit SHALL request that PID or attestation in all formats offered by the PID Provider or Attestation Provider.

*Note: Examples include the mdoc format specified in [ISO/IEC 18013-5] and the SD-JWT VC-format specified in [SD-JWT VC].*

</div>
</div>

<div class="eudi-hlr" id="ISSU_12b" markdown>
<div class="eudi-hlr__id">ISSU_12b<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The WSCA/WSCD or a keystore SHALL generate a new key pair for a new PID or attestation on request of the Wallet Instance, unless that PID or attestation is issued synchronously in a remote HSM architecture. This generation request MAY be done either prior to the issuance of any PID or attestation, or during the issuance process.

*Note: a) See also WUA_05 and WUA_05a. b) In case of synchronous issuing in a remote HSM architecture, re-use of an existing key pair within a limited period of time can be acceptable, based on the PID Provider's or Attestation Provider's issuance security policy. This is similar to a choice between Method A or Method B (see ISSU_37 and ISSU_38) when issuing PIDs or attestations non-synchronously.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_12c" markdown>
<div class="eudi-hlr__id">ISSU_12c<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The expiration date of a PID SHALL be no later than the end of the revocation maintenance periods of the WIA and the KA presented as part of the PID issuance process.

*Note: This requirement is an implication of WURevocation_18 in [Topic 38][topic-38] and WUA_29 - WUA_31. If the PID would be valid beyond the period for which the Wallet Provider has committed to maintaining the revocation status of the Wallet Instance and the WSCD, the PID Provider would not be able to fulfil its obligation to regularly check whether the Wallet Instance and WSCD have been revoked for the full PID validity period.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_12d" markdown>
<div class="eudi-hlr__id">ISSU_12d<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If an Attestation Provider supports revocation chaining for its attestations per WURevocation_19 in [Topic 38][topic-38], the expiration date of an attestation SHALL be no later than the end of the revocation maintenance periods of the WIA and the KA (if applicable) presented as part of the attestation issuance process.

*Note: See note in ISSU_12c.*

</div>
</div>

##### B - HLRs for PID issuance <!-- omit from toc -->

<div class="eudi-hlr" id="ISSU_13" markdown>
<div class="eudi-hlr__id">ISSU_13<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Provider SHALL ensure that at least one PID Provider is willing to issue a PID complying with [PID Rulebook][pid-rulebook] to Users of the Wallet Units it provides.

</div>
</div>

<div class="eudi-hlr" id="ISSU_14" markdown>
<div class="eudi-hlr__id">ISSU_14<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A PID Provider SHALL ensure that all PIDs it issues to Wallet Units comply with the requirements specified in [PID Rulebook][pid-rulebook].

</div>
</div>

<div class="eudi-hlr" id="ISSU_15" markdown>
<div class="eudi-hlr__id">ISSU_15<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A PID Provider SHALL support the OpenID4VCI protocol referenced in ISSU_01 for issuing PIDs.

</div>
</div>

<div class="eudi-hlr" id="ISSU_16" markdown>
<div class="eudi-hlr__id">ISSU_16</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="ISSU_17" markdown>
<div class="eudi-hlr__id">ISSU_17<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A PID Provider SHALL implement device binding for all PIDs it issues, meaning it SHALL ensure that a PID is cryptographically bound to the WSCA/WSCD included in the Wallet Unit, as specified in [Topic 9][topic-9].

*Note: Device binding is called 'mdoc authentication' in [ISO/IEC 18013-5] and 'key binding' in [SD-JWT VC].*

</div>
</div>

<div class="eudi-hlr" id="ISSU_18" markdown>
<div class="eudi-hlr__id">ISSU_18<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A PID Provider SHALL verify the identity of the subject of the PID in compliance with Level of Assurance (LoA) High requirements.

*Note: These requirements will be determined by the relevant eID scheme.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_18a" markdown>
<div class="eudi-hlr__id">ISSU_18a</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="ISSU_19" markdown>
<div class="eudi-hlr__id">ISSU_19<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For the verification of a WIA or KA, a PID Provider SHALL accept the Wallet Provider trust anchors it needs, as published by the Commission in the Wallet Provider LoTE.

*Note: a) The Wallet Provider LoTE is explained in [Topic 31][topic-31]. b) It is not mandatory for a PID Provider to store all Wallet Provider trust anchors. This is because it is not mandatory for a PID Provider to accept all certified Wallet Solutions in the EUDI Wallet ecosystem. Each PID Provider will choose which trust anchors they need to use.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_19a" markdown>
<div class="eudi-hlr__id">ISSU_19a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A PID Provider SHALL support all Wallet Solutions recognised under the corresponding notified eID scheme, meaning that it is willing and able to issue a PID to a Wallet Unit on request of the User.

</div>
</div>

<div class="eudi-hlr" id="ISSU_19b" markdown>
<div class="eudi-hlr__id">ISSU_19b<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For the retrieval and management of trust anchors, PID Providers SHALL support LoTEs complying with [ETSI TS 119 602].

*Note: LoTEs complying with [ETSI TS 119 602] are used for the distribution of trust anchors of Wallet Providers.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_20" markdown>
<div class="eudi-hlr__id">ISSU_20<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

To inform its potential PID subjects about the Wallet Solution(s) they can use for requesting a PID, a PID Provider SHALL publish a list of supported Wallet Solutions in such a way that it can be easily found, for example on the PID Provider's website.

*Note: This a policy requirement rather than a technical requirement.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_21" markdown>
<div class="eudi-hlr__id">ISSU_21<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Before issuing a PID, a PID Provider SHALL verify the Wallet Unit's WIA and KA using a trust anchor registered in the Wallet Provider LoTE. Moreover, it SHALL verify that the Wallet Instance referenced in the WIA has not been revoked, and that the WSCD referenced in the KA has not been revoked.

*Note: a) For WIAs and KAs, see [Topic 9][topic-9] and [Topic 38][topic-38]. b) [CIR 2024/2977], Article 3 (9), also allows another authentication mechanism in accordance with an electronic identity scheme notified at assurance level high. However, the ARF does not further specify such other authentication mechanisms, which means that in general they will not be interoperable.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_22" markdown>
<div class="eudi-hlr__id">ISSU_22<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A PID Provider SHALL sign its Credential Issuer metadata as specified in section 12.2.3 of [OpenID4VCI]. To do so, the PID Provider SHALL use the private key corresponding to the public key in its access certificate. The PID Provider SHALL include its access certificate, as well as all intermediate certificate(s) leading up to the trust anchor of the corresponding Access Certificate Authority (see ISSU_33) in the LoTE, in the `x5c` parameter in the JOSE header of the JSON Web Signature for the metadata.

</div>
</div>

<div class="eudi-hlr" id="ISSU_22a" markdown>
<div class="eudi-hlr__id">ISSU_22a</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="ISSU_22b" markdown>
<div class="eudi-hlr__id">ISSU_22b</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="ISSU_23" markdown>
<div class="eudi-hlr__id">ISSU_23<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For the verification of a PID Provider's access certificates, a Wallet Unit SHALL accept all Access Certificate Authorities trust anchors published by the Commission in the relevant LoTE, and only those.

*Note: a) Access Certificate Authority LoTEs are explained in [[Topic 27][topic-27]]. b) A Wallet Unit does not have to be able to request a PID from all PID Providers in the ecosystem. It is up to each Wallet Provider to decide which PID Providers its Wallet Units will support.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_23a" markdown>
<div class="eudi-hlr__id">ISSU_23a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Provider SHALL support at least one PID Provider, meaning that its Wallet Units SHALL be capable of requesting the issuance of a PID from these PID Provider(s), and that the Wallet Provider has agreed with the PID Provider(s) that the PID Provider(s) will process such a request according to the agreed rules and procedures.

</div>
</div>

<div class="eudi-hlr" id="ISSU_23b" markdown>
<div class="eudi-hlr__id">ISSU_23b<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Prior to or during installation of a Wallet Instance, the Wallet Provider SHALL notify the User about the PID Provider(s) that are supported by the Wallet Unit.

</div>
</div>

<div class="eudi-hlr" id="ISSU_23c" markdown>
<div class="eudi-hlr__id">ISSU_23c<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For the verification of a PID Provider's registration certificates, a Wallet Unit SHALL accept the trust anchors of all Providers of registration certificates published by the Commission in the relevant LoTE, and only those.

*Note: The requirement for Wallet Units to verify and validate registration certificates only applies as of 24 months after entry into force of the Regulation amending [CIR 2024/2982].*

</div>
</div>

<div class="eudi-hlr" id="ISSU_24" markdown>
<div class="eudi-hlr__id">ISSU_24<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL authenticate and validate the access certificate of the PID Provider before requesting the issuance of a PID. The Wallet Unit SHALL verify that the access certificate is authentic and is valid at the time of validation, and that the issuer of the access certificate is included in an Access Certificate Authority LoTE.

</div>
</div>

<div class="eudi-hlr" id="ISSU_24a" markdown>
<div class="eudi-hlr__id">ISSU_24a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Before requesting the issuance of a PID, the Wallet Unit SHALL verify that the PID Provider is indeed a registered PID Provider. To do so, the Wallet Unit SHALL inspect the `entitlement` member in the registration certificate of the PID Provider, provided in the Credential Issuer Metadata per [ETSI TS 119 472-3] section 4.2.3, and verify the authenticity of the registration certificate. If this procedure does not confirm that the PID Provider is indeed registered as a PID Provider, the Wallet Unit SHALL display a warning to the User, and SHALL NOT request the issuance of a PID.

*Note: The requirement for Wallet Units to verify and validate registration certificates only applies as of 24 months after entry into force of the Regulation amending [CIR 2024/2982].*

</div>
</div>

<div class="eudi-hlr" id="ISSU_24b" markdown>
<div class="eudi-hlr__id">ISSU_24b<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Before requesting the issuance of a PID, the Wallet Unit SHALL verify whether the PID Provider properly registered for the issuance of PIDs. To do so, the Wallet Unit SHALL inspect the `providesAttestations` member in the registration certificate of the PID Provider, provided in the Credential Issuer Metadata per [ETSI TS 119 472-3] section 4.2.3, and verify the authenticity of the registration certificate. If this procedure does not confirm that the PID Provider registered for the issuance of PIDs, the Wallet Unit SHALL display a warning to the User, and SHALL NOT request the issuance of a PID.

*Note: a) It may be argued that this verification is superfluous, since an entity registered as a PID Provider (ISSU_24a) by definition is registered for issuing PIDs. However, this verification was added to ensure that Wallet Unit can use the same verification process for PIDs as for other attestations (see ISSU_34b), as well as to ensure that in the future, it is possible to distinguish between different types of PID if needed, where not all PID Providers are registered to issue all types of PID. b) The requirement for Wallet Units to verify and validate registration certificates only applies as of 24 months after entry into force of the Regulation amending [CIR 2024/2982].*

</div>
</div>
