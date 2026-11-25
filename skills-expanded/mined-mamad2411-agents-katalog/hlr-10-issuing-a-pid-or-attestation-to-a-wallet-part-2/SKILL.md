---
name: "hlr-10-issuing-a-pid-or-attestation-to-a-wallet-part-2"
description: "Use when working with EUDI high-level requirements for 'Issuing a PID or attestation to a Wallet Unit' (Part 2). Contains normative requirements from ARF Annex 2."
sections:
  - "C - HLRs for Attestation Issuance <!-- omit from toc -->"
  - "D - HLRs for Privacy Risks and Mitigation <!-- omit from toc -->"
  - "Method A: Once-only attestations <!-- omit from toc -->"
  - "Method B: Limited-time attestations <!-- omit from toc -->"
  - "Method C: Rotating-batch attestations <!-- omit from toc -->"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~7461 -->

##### C - HLRs for Attestation Issuance <!-- omit from toc -->

<div class="eudi-hlr" id="ISSU_25" markdown>
<div class="eudi-hlr__id">ISSU_25<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

An Attestation Provider SHALL ensure all attestations issued to Wallet Units comply with the requirements specified in the applicable Attestation Rulebook, as described in [Topic 12][topic-12]].

</div>
</div>

<div class="eudi-hlr" id="ISSU_26" markdown>
<div class="eudi-hlr__id">ISSU_26<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

An Attestation Provider SHALL support the OpenID4VCI protocol referenced in ISSU_01 for issuing attestations.

</div>
</div>

<div class="eudi-hlr" id="ISSU_27" markdown>
<div class="eudi-hlr__id">ISSU_27<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

An Attestation Provider SHOULD implement device binding for all attestations it issues. If an issued attestation is device-bound, the Attestation Provider SHALL ensure that the attestation is cryptographically bound to a WSCA/WSCD or a keystore available to the Wallet Unit, as specified in [Topic 9][topic-9].

*Note: a) Device binding is called 'mdoc authentication' in [ISO/IEC 18013-5] and 'key binding' in [SD-JWT VC]. b) Implementing mdoc authentication is mandatory in [ISO/IEC 18013-5] and therefore, it is mandatory for attestations complying with that standard. c) See ISSU_27d.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_27a" markdown>
<div class="eudi-hlr__id">ISSU_27a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If the subject of the attestation is a natural person, an Attestation Provider SHALL verify the identity of the subject of the attestation, in compliance with applicable requirements and in accordance with relevant standards or Implementing Regulations.

*Note: Not every attestation has a natural person as its subject. For example, a holiday voucher may be valid for any User that can present it to a Relying Party and therefore has no subject. This is comparable to the concept of a 'bearer token'.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_27b" markdown>
<div class="eudi-hlr__id">ISSU_27b<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If applicable, an Attestation Provider SHALL ensure that the attributes attested in the attestation issued are valid for the identified attestation subject.

</div>
</div>

<div class="eudi-hlr" id="ISSU_27c" markdown>
<div class="eudi-hlr__id">ISSU_27c<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Attestation Provider SHALL verify that the User requesting the attestation has the right to receive it.

</div>
</div>

<div class="eudi-hlr" id="ISSU_27d" markdown>
<div class="eudi-hlr__id">ISSU_27d<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

An Attestation Provider issuing device-bound attestations SHALL indicate the desired level of security for the private key storage and for User authentication in its Credential Issuer metadata, according to [OpenID4VCI] section 12.2.4 and Appendix D.2.

*Note: See also WIAM_14b, WIAM_14c, and WUA_05 and WUA_05a.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_28" markdown>
<div class="eudi-hlr__id">ISSU_28<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For the verification of a WIA or KA, an Attestation Provider SHALL accept all Wallet Provider trust anchors published by the Commission in the relevant LoTE, and only those.

*Note: The Wallet Provider LoTE is explained in [Topic 31][topic-31].*

</div>
</div>

<div class="eudi-hlr" id="ISSU_28a" markdown>
<div class="eudi-hlr__id">ISSU_28a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For the retrieval and management of trust anchors, Attestation Providers SHALL support LoTEs complying with [ETSI TS 119 602].

*Note: LoTEs complying with [ETSI TS 119 602] are used for the distribution of trust anchors of Wallet Providers.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_29" markdown>
<div class="eudi-hlr__id">ISSU_29<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A QEAA Provider or PuB-EAA Provider SHALL support all Wallet Solutions, except in case the attestation in question is a Strong User Authentication (SUA) attestation as meant in [Topic 20][topic-20] and the Wallet Provider does not support processing of the transactional data associated with the SUA attestation. Except for such cases, a QEAA Provider or PuB-EAA Provider SHALL NOT discriminate between Wallet Solutions when processing a request for the issuance of an attestation.

*Note: This requirement is not applicable for non-qualified EAA Providers. For example, a non-qualified EAA Provider may choose to issue attestations in the format specified in [W3C VCDM v2.0], see ARB_01a. In that case, it will support only those Wallet Solutions that have implemented this attestation format.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_30" markdown>
<div class="eudi-hlr__id">ISSU_30<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Before issuing a device-bound attestation, an Attestation Provider SHALL verify the Wallet Unit's key attestation using a trust anchor registered in the Wallet Provider LoTE. Moreover, it SHALL verify that the WSCD or keystore referenced in the KA has not been revoked.

*Note: This requirement applies specifically to the KA received during device-bound attestation issuance. The corresponding requirement for verifying the WIA is ISSU_30a.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_30a" markdown>
<div class="eudi-hlr__id">ISSU_30a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Before issuing an attestation, an Attestation Provider SHALL: - verify that the Wallet Provider mentioned in the Wallet Unit's WIA is present in the Wallet Provider LoTE. - authenticate and validate the WIA using the trust anchor(s) registered for the Wallet Provider in that LoTE.

*Note: This requirement applies to both device-bound and non-device-bound attestations*

</div>
</div>

<div class="eudi-hlr" id="ISSU_31" markdown>
<div class="eudi-hlr__id">ISSU_31</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="ISSU_32" markdown>
<div class="eudi-hlr__id">ISSU_32<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

An Attestation Provider SHALL sign its Credential Issuer metadata as specified in section 12.2.3 of [OpenID4VCI]. To do so, the Attestation Provider SHALL use the private key corresponding to the public key in its access certificate. The Attestation Provider SHALL include its access certificate, as well as all intermediate certificate(s) leading up to the trust anchor of the corresponding Access Certificate Authority in the LoTE (see ISSU_33), in the `x5c` parameter in the JOSE header of the JSON Web Signature for the metadata.

</div>
</div>

<div class="eudi-hlr" id="ISSU_32a" markdown>
<div class="eudi-hlr__id">ISSU_32a</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="ISSU_33" markdown>
<div class="eudi-hlr__id">ISSU_33<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For the verification of access certificates, a Wallet Unit SHALL accept all trust anchors of Access Certificate Authorities, as published by the Commission in the relevant LoTE, and only those.

*Note: The Access Certificate Authority LoTE is explained in [[Topic 27][topic-27]].*

</div>
</div>

<div class="eudi-hlr" id="ISSU_33a" markdown>
<div class="eudi-hlr__id">ISSU_33a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For the verification of the registration certificates of Attestation Providers, a Wallet Unit SHALL accept all trust anchors of Providers of registration certificates, as published by the Commission in the relevant LoTE, and only those.

*Note: The requirement for Wallet Units to verify and validate registration certificates only applies as of 24 months after entry into force of the Regulation amending [CIR 2024/2982].*

</div>
</div>

<div class="eudi-hlr" id="ISSU_33b" markdown>
<div class="eudi-hlr__id">ISSU_33b<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Provider SHALL ensure that its Wallet Units support all attestations conforming to attestation schemes registered in the catalogue of schemes for the attestation of attributes established by the Commission pursuant to Article 8 of Commission Implementing Regulation (EU) 2025/1569, where such attestations use a format and issuance protocol supported by Wallet Units pursuant to Commission Implementing Regulations (EU) 2024/2977, 2024/2979 and 2024/2982. 

</div>
</div>

<div class="eudi-hlr" id="ISSU_34" markdown>
<div class="eudi-hlr__id">ISSU_34<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL authenticate and validate the access certificate of the Attestation Provider before requesting the issuance of an attestation. The Wallet Unit SHALL verify that the access certificate is authentic and is valid at the time of validation, and that the issuer of the access certificate is in the Access Certificate Authority LoTE, as documented in [[Topic 27][topic-27]].

</div>
</div>

<div class="eudi-hlr" id="ISSU_34a" markdown>
<div class="eudi-hlr__id">ISSU_34a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Before requesting the issuance of an attestation, the Wallet Unit SHALL verify that the Attestation Provider is a registered QEAA Provider, PuB-EAA Provider, or EAA Provider. To do so, the Wallet Unit SHALL inspect the `entitlement` member in the registration certificate of the Attestation Provider, provided in the Credential Issuer Metadata per [ETSI TS 119 472-3] section 4.2.3, and verify the authenticity of the registration certificate. If this procedure does not confirm that the Attestation Provider is indeed registered as a QEAA Provider, PuB-EAA Provider, or EAA Provider, the Wallet Unit SHALL display a warning to the User, and SHALL NOT request the issuance of an attestation.

*Note: The requirement for Wallet Units to verify and validate registration certificates only applies as of 24 months after entry into force of the Regulation amending [CIR 2024/2982].*

</div>
</div>

<div class="eudi-hlr" id="ISSU_34b" markdown>
<div class="eudi-hlr__id">ISSU_34b<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Before requesting the issuance of an attestation, the Wallet Unit SHALL verify whether the Provider properly registered for the issuance of the type of attestation that the User wants to obtain. To do so, the Wallet Unit SHALL inspect the `providesAttestations` member in the registration certificate of the Attestation Provider, provided in the Credential Issuer Metadata per [ETSI TS 119 472-3] section 4.2.3, and verify the authenticity of the registration certificate. If this procedure does not confirm that the Attestation Provider registered for the relevant type of attestation, the Wallet Unit SHALL display a warning to the User, and SHALL NOT request the issuance of an attestation. 

*Note: The requirement for Wallet Units to verify and validate registration certificates only applies as of 24 months after entry into force of the Regulation amending [CIR 2024/2982].*

</div>
</div>

##### D - HLRs for Privacy Risks and Mitigation <!-- omit from toc -->

<div class="eudi-hlr" id="ISSU_35" markdown>
<div class="eudi-hlr__id">ISSU_35<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A PID Provider or Attestation Provider SHALL ensure that all unique elements in a PID or attestation have a negligible chance of having the same value across all PIDs or attestations issued by that Provider. This SHALL include at least a) the salt used for hashing every attribute, b) the hash values of all attributes, c) the attestation identifier or index used for revocation purposes (if applicable), d) the attestation public key used for device binding (if applicable), and e) the value of the Attestation Provider signature.

*Note: a) The list of unique elements is based on [ISO/IEC 18013-5] and [SD-JWT VC]. b) This requirement can be achieved, for example, by ensuring that salt values, indexes and attestation identifiers are pseudo-random numbers generated by a cryptographically secure pseudo-random number generator (CSPRNG).*

</div>
</div>

<div class="eudi-hlr" id="ISSU_35a" markdown>
<div class="eudi-hlr__id">ISSU_35a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Provider SHALL ensure that all unique elements in a WIA or KA have a negligible chance of having the same value across all WIAs and KAs issued by that Wallet Provider and intended to be presented to different PID Providers or Attestation Providers. This SHALL include at least a) the attestation index for revocation, unless the per-KA index approach meant in WUA_28 is used, b) the WIA or KA public key, and c) the value of the Wallet Provider signature over the WIA or KA.

*Note: In other words, the following do not have to be unique: i) WIAs presented to the same PID Provider or Attestation Provider, and ii) the revocation index in a KA under the type-shared index approach (see WUA_28). However, under the per-KA index approach (see WUA_28), the KA revocation index is unique per KA or per KA-issuer pair and is subject to this requirement.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_35b" markdown>
<div class="eudi-hlr__id">ISSU_35b<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

After issuing a PID, attestation, KA, or WIA, a PID Provider, Attestation Provider or Wallet Provider SHALL discard the values of all unique elements, including at least the ones mentioned in requirement ISSU_35 or ISSU_35a (as applicable) above, as well as any timestamps, as soon as they are no longer needed. The Provider SHALL NOT communicate these values to any other party inside or outside the EUDI Wallet ecosystem.

</div>
</div>

<div class="eudi-hlr" id="ISSU_36" markdown>
<div class="eudi-hlr__id">ISSU_36<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

When issuing PIDs, attestations, or WIAs or KAs in a batch to a Wallet Unit, a PID Provider, Attestation Provider, or Wallet Provider SHALL ensure that the timestamps in these PIDs, attestations, or WIAs and KAs do not enable Relying Parties to conclude that they are part of the same batch (and therefore belong to the same User).

*Note: a) This can be done, for example, by making timestamps sufficiently imprecise that a high number of batches, each issued to a different Wallet Unit, share the same timestamp values (herd privacy). b) This requirement does not apply to timestamps included in the attestation as selectively disclosable attributes, see ISSU_36a.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_36a" markdown>
<div class="eudi-hlr__id">ISSU_36a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If the exact time of the issuance of an attestation or the beginning or end of its validity period is relevant for the use case, the applicable Attestation Rulebook SHALL specify one or more selectively disclosable attribute(s) containing a timestamp with the required precision.

*Note: a) An example of this may be a vehicle registration attestation indicating the date and time (down to the second) at which a car changed ownership and therefore legal responsibility. b) This requirement ensures that requirement ISSU_36 can be complied with without running into challenges related to the use case.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_37" markdown>
<div class="eudi-hlr__id">ISSU_37<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Provider SHALL ensure that its Wallet Solution supports the following methods for limiting the number of times a User can present the same technical PID or attestation to Relying Parties: Method A (Once-only attestations, as specified in requirement ISSU_43 - ISSU_47) and Method B (Limited-time attestations, as specified in requirement ISSU_48 - ISSU_50). In addition, a Wallet Provider MAY ensure that its Wallet Solution supports Method C (Rotating-batch attestations, as specified in requirement ISSU_51 - ISSU_54) or Method D (Per-Relying Party attestations, as specified in requirement ISSU_55 - ISSU_57).

*Note: Wallet Solutions, PID Providers, Attestation Providers, and Wallet Providers are free to define and use other methods as well. However, such other methods are out of scope of the ARF.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_38" markdown>
<div class="eudi-hlr__id">ISSU_38<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A PID Provider or Attestation Provider SHALL have a policy describing which method(s) (i.e, A, B, C, and/or D) it will use to limit the number of times a Wallet Unit may present a single technical PID or attestation. For each supported method, the policy SHALL also specify how the values for respective parameters for that method, such as technical validity period and batch size, will be chosen. The goal of the policy SHALL be to ensure that the risk of linkability is mitigated to an acceptable level, given the (expected) usage of the logical PID or attestation by the User. To determine what an acceptable level of risk is, the PID Provider or Attestation Provider SHALL carry out a risk analysis regarding linkability.

*Note: a) If an Attestation Provider issues multiple attestation types, these requirements apply for each type of attestation separately. b) [Technical Specification 3](../../technical-specifications/ts3-wallet-unit-attestation.md) specifies that WIAs and KAs shall be sent to a PID Provider or Attestation Provider only once. In other words, for WIAs and KAs, the use of Method A is mandatory.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_39" markdown>
<div class="eudi-hlr__id">ISSU_39<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

PID Providers and Attestation Providers SHALL include the `credential_reuse_policy` parameter, specified in section 4.2.4.2 of [ETSI TS 119 472-3], in their Credential Issuer Metadata to specify which of the methods A, B, C, or D the Wallet Unit must use for the logical PID or attestation issued. Indicated methods SHALL be ordered by preference.

*Note: See also ISSU_40.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_39a" markdown>
<div class="eudi-hlr__id">ISSU_39a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Wallet Units SHALL support the `credential_reuse_policy` Credential Issuer Metadata parameter specified in section 4.2.4.2 of [ETSI TS 119 472-3] and SHALL present each technical PID and attestation in accordance with the values set for this parameter by the relevant PID Provider or Attestation Provider.

</div>
</div>

<div class="eudi-hlr" id="ISSU_40" markdown>
<div class="eudi-hlr__id">ISSU_40<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A PID Provider or Attestation Provider SHALL indicate in their OpenID4VCI Issuer metadata that either method A or method B must be used for a given type of PID or attestation. In addition, a PID Provider or Attestation Provider MAY indicate that it prefers using method C and/or method D over method A or method B, by including the methods in the metadata in the appropriate order. In such a case, a Wallet Unit supporting method C and/or method D SHALL use that method, while a Wallet Unit not supporting these methods SHALL use method A or method B, as applicable.

*Note: a) This requirement implies that a PID Provider or Attestation Provider must not include both method A and method B in its metadata. b) Example: An Attestation Provider indicates methods {D, C, A} in its metadata, in that order. A Wallet Unit that supports methods C and D (as well as A and B) then uses method D for this type of attestation. A Wallet Unit supporting methods A, B and C uses method C. A Wallet Unit supporting only methods A and B uses method A.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_40a" markdown>
<div class="eudi-hlr__id">ISSU_40a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

When implementing any of the methods mentioned in ISSU_37, a Wallet Unit, PID Provider, or Attestation Provider SHALL comply with the applicable requirements in [ETSI TS 119 472-3], section 4.2.4.

</div>
</div>

<div class="eudi-hlr" id="ISSU_41" markdown>
<div class="eudi-hlr__id">ISSU_41<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

To the maximum extent possible, Wallet Providers, PID Providers, and Attestation Providers SHALL ensure that Users do not notice which of the methods A, B, C, or D is used for their PIDs and attestations.

</div>
</div>

<div class="eudi-hlr" id="ISSU_42" markdown>
<div class="eudi-hlr__id">ISSU_42<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

To the maximum extent possible, Wallet Providers, PID Providers, and Attestation Providers SHALL ensure that no User action is needed for the re-issuance of WIAs or KAs, PIDs, or attestations.

*Note: For the topic of re-issuance, see also the [Discussion Paper for Topic B](../../discussion-topics/b-re-issuance-and-batch-issuance-of-pids-and-attestations.md).*

</div>
</div>

##### Method A: Once-only attestations <!-- omit from toc -->

<div class="eudi-hlr" id="ISSU_43" markdown>
<div class="eudi-hlr__id">ISSU_43<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If Method A is used, the Wallet Unit SHALL request the PID Provider or Attestation Provider to issue technical PIDs or attestations in batches to the Wallet Unit. All PIDs or attestations in a batch SHALL have the same attribute values and the same technical validity period.

</div>
</div>

<div class="eudi-hlr" id="ISSU_44" markdown>
<div class="eudi-hlr__id">ISSU_44<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If Method A is used, the Wallet Unit SHALL present each technical PID or attestation only once to a Relying Party that requests the corresponding logical PID or attestation, except when it has fallen back to Method B as specified in ISSU_47.

</div>
</div>

<div class="eudi-hlr" id="ISSU_45" markdown>
<div class="eudi-hlr__id">ISSU_45<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If Method A is used, the Wallet Unit SHALL have a lower limit for the number of unused technical PIDs or attestations it holds for each logical PID or attestation, and SHALL request the issuance of a new batch when this limit is reached. The PID Provider or Attestation Provider SHALL inform the Wallet Unit about the value of the lower limit and the size of the batch to be requested, using the `credential_reuse_policy` Credential Issuer Metadata parameter specified in section 4.2.4.2 of [ETSI TS 119 472-3].

</div>
</div>

<div class="eudi-hlr" id="ISSU_46" markdown>
<div class="eudi-hlr__id">ISSU_46<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If Method A is used and the Wallet Unit must request a new batch of technical PIDs or attestations but is not able to do so (for instance because it is offline), the Wallet Unit SHALL warn the User that they are about to lose the possibility to present the corresponding logical PID or attestation to Relying Parties, and request them to connect their device to the internet.

</div>
</div>

<div class="eudi-hlr" id="ISSU_47" markdown>
<div class="eudi-hlr__id">ISSU_47<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If Method A is used and the Wallet Unit has run out of unused technical PIDs or attestations, but is not able to request a new batch, it SHALL fall back to method B (see ISSU_48 - ISSU_50). This means that, when requested by a Relying Party or Attestation Provider, the Wallet Unit SHALL again present one of the already used technical PIDs or attestations. The Wallet Unit SHALL return to using method A as soon as it is able to go online and request a new batch of PIDs or attestations.

</div>
</div>

##### Method B: Limited-time attestations <!-- omit from toc -->

<div class="eudi-hlr" id="ISSU_48" markdown>
<div class="eudi-hlr__id">ISSU_48<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If Method B is used, the Wallet Unit SHALL request the PID Provider or Attestation Provider to issue a single technical PID or attestation to the Wallet Unit.

</div>
</div>

<div class="eudi-hlr" id="ISSU_49" markdown>
<div class="eudi-hlr__id">ISSU_49<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If Method B is used, the Wallet Unit SHALL present a technical PID or attestation multiple times to the same Relying Party or to different Relying Parties, when a Relying Party requests the corresponding logical PID or attestation.

</div>
</div>

<div class="eudi-hlr" id="ISSU_50" markdown>
<div class="eudi-hlr__id">ISSU_50<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If Method B is used, the Wallet Unit SHALL request the PID Provider or Attestation Provider to re-issue a technical PID or attestation some time before the one existing in the Wallet Unit expires. The PID Provider or Attestation Provider SHALL inform the Wallet Unit about the moment at which the Wallet Unit must request the re-issuance of a technical PID or attestation, relative to the expiration date of the existing one. To do so, the PID Provider or Attestation Provider SHALL use the `credential_reuse_policy` Credential Issuer Metadata parameter specified in section 4.2.4.2 of [ETSI TS 119 472-3].

*Note: It is the responsibility of the Relying Party receiving a PID or attestation to validate whether a presented technical PID or attestation is temporally valid. A Wallet Unit is allowed to present a PID or attestation even if its expiration date is in the past.*

</div>
</div>

##### Method C: Rotating-batch attestations <!-- omit from toc -->

<div class="eudi-hlr" id="ISSU_51" markdown>
<div class="eudi-hlr__id">ISSU_51<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If Method C is used, the Wallet Unit SHALL request the PID Provider or Attestation Provider to issue technical PIDs or attestations in batches to the Wallet Unit. All PIDs or attestations in a batch SHALL have the same attribute values and the same technical validity period.

</div>
</div>

<div class="eudi-hlr" id="ISSU_52" markdown>
<div class="eudi-hlr__id">ISSU_52<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If Method C is used, the Wallet Unit SHALL present each technical PID or attestation in a batch once to a Relying Party that requests the corresponding logical PID or attestation, in a random order. When all PIDs or attestations in a batch have been presented once, the Wallet Unit SHALL reset the batch, and start presenting each PID or attestation in the batch again, in a random order. The Wallet Unit SHALL continue doing this until it receives a new batch, see ISSU_54.

</div>
</div>

<div class="eudi-hlr" id="ISSU_53" markdown>
<div class="eudi-hlr__id">ISSU_53</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="ISSU_54" markdown>
<div class="eudi-hlr__id">ISSU_54<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If Method C is used, the Wallet Unit SHALL request the PID Provider or Attestation Provider to re-issue a batch of technical PIDs or attestations some time before the batch in the Wallet Unit expires. The PID Provider or Attestation Provider SHALL inform the Wallet Unit about the size of the batch and about the moment at which the Wallet Unit must request the re-issuance of a batch, relative to the expiration date of the existing batch. To do so, the PID Provider or Attestation Provider SHALL use the `credential_reuse_policy` Credential Issuer Metadata parameter specified in section 4.2.4.2 of [ETSI TS 119 472-3].

</div>
</div>
