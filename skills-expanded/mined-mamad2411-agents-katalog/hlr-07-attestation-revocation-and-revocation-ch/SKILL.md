---
name: "hlr-07-attestation-revocation-and-revocation-ch"
description: "Use when working with EUDI high-level requirements for 'Attestation revocation and revocation checking'. Contains normative SHALL/SHOULD/MAY requirements from ARF Annex 2."
sections:
  - "A.2.3.5 Topic 7 - Attestation revocation and revocation checking"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~4597 -->

#### A.2.3.5 Topic 7 - Attestation revocation and revocation checking

<div class="eudi-hlr" id="VCR_01" markdown>
<div class="eudi-hlr__id">VCR_01<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A PID Provider, QEAA Provider, or PuB-EAA Provider SHALL use one of the following methods for revocation of an [ISO/IEC 18013-5]-compliant PID, QEAA, or PuB-EAA: - Only issue short-lived attestations having a validity period of 24 hours or less, such that revocation will never be necessary, - Use an Attestation Status List mechanism specified per VCR_11, or - Use an Attestation Revocation List mechanism specified per VCR_11.

*Note: The 24-hour period originates from [ETSI EN 319 411-1] V1.4.1, requirement REV-6.2.4-03A. This requires that the process of revocation must take at most 24 hours. Consequently, revocation may make no sense if the attestation is valid for less than 24 hours, because it may reach the end of its validity period before it is revoked.*

</div>
</div>

<div class="eudi-hlr" id="VCR_01a" markdown>
<div class="eudi-hlr__id">VCR_01a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Provider SHALL use the method specified in [Technical Specification 3](../../technical-specifications/ts3-wallet-unit-attestation.md) for maintaining the revocation status of the underlying objects referenced in a WIA or key attestation.

*Note: The 'underlying object' is the object that is actually revoked by revoking the WIA or key attestation, i.e., the Wallet Instance in case of a WIA and a WSCA/WSCD or keystore in case of a key attestation.*

</div>
</div>

<div class="eudi-hlr" id="VCR_01b" markdown>
<div class="eudi-hlr__id">VCR_01b<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A PID Provider, QEAA Provider, or PuB-EAA Provider SHALL use one of the following methods for revocation of a [SD-JWT VC]-compliant PID, QEAA, or PuB-EAA: - Only issue short-lived attestations having a validity period of 24 hours or less, such that revocation will never be necessary or, - Use an Attestation Status List mechanism specified per VCR_11.

*Note: The 24-hour period originates from [ETSI EN 319 411-1] V1.4.1, requirement REV-6.2.4-03A. This requires that the process of revocation must take at most 24 hours. Consequently, revocation may make no sense if the attestation is valid for less than 24 hours, because it may reach the end of its validity period before it is revoked.*

</div>
</div>

<div class="eudi-hlr" id="VCR_02" markdown>
<div class="eudi-hlr__id">VCR_02<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For non-qualified EAAs, the relevant Rulebook SHALL specify whether that type of EAA must be revocable. If a non-qualified EAA type must be revocable, the relevant Rulebook SHALL determine which of the methods mentioned in VCR_01 or VCR_01b (as applicable) must be implemented by the relevant EAA Providers for the revocation of such an EAA.

</div>
</div>

<div class="eudi-hlr" id="VCR_03" markdown>
<div class="eudi-hlr__id">VCR_03<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If a PID or attestation is revocable, the PID Provider of a given PID, or the Attestation Provider of a given attestation, SHALL be the only party in the EUDI Wallet ecosystem responsible for executing the revocation of that PID or attestation.

*Note: A PID Provider or Attestation Provider MAY outsource the operation of the revocation process to a third party.*

</div>
</div>

<div class="eudi-hlr" id="VCR_03a" markdown>
<div class="eudi-hlr__id">VCR_03a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Wallet Provider of a given WIA or KA SHALL be the only party in the EUDI Wallet ecosystem responsible for maintaining the revocation status of the underlying object attested in that WIA or KA.

*Note: A Wallet Provider MAY outsource the operation of the revocation process to a third party.*

</div>
</div>

<div class="eudi-hlr" id="VCR_04" markdown>
<div class="eudi-hlr__id">VCR_04<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A PID Provider, Attestation Provider, or Wallet Provider that revoked a PID, attestation, WIA, or KA SHALL NOT reverse the revocation.

</div>
</div>

<div class="eudi-hlr" id="VCR_05" markdown>
<div class="eudi-hlr__id">VCR_05<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If a PID, attestation, WIA, or KA is revocable, the PID Provider, Attestation Provider, or Wallet Provider SHALL have a policy specifying under which conditions a PID, attestation, WIA, or KA it issued will be revoked.

</div>
</div>

<div class="eudi-hlr" id="VCR_06" markdown>
<div class="eudi-hlr__id">VCR_06<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If a PID or attestation is revocable, the PID Provider or Attestation Provider SHALL revoke a PID or attestation when its security has been compromised.

</div>
</div>

<div class="eudi-hlr" id="VCR_07" markdown>
<div class="eudi-hlr__id">VCR_07<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Provider SHALL revoke the Wallet Instance upon the explicit request of the User to revoke their Wallet Unit.

*Note: See also WURevocation_07 and _10.*

</div>
</div>

<div class="eudi-hlr" id="VCR_07a" markdown>
<div class="eudi-hlr__id">VCR_07a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If a PID is revocable, the PID Provider SHALL revoke that PID upon the explicit request of the User to whom the PID was issued.

</div>
</div>

<div class="eudi-hlr" id="VCR_07b" markdown>
<div class="eudi-hlr__id">VCR_07b<span class="kw-should">SHOULD</span></div>
<div class="eudi-hlr__body" markdown>

If an attestation is revocable, the Attestation Provider SHOULD revoke that attestation upon the explicit request of the User to whom the attestation was issued.

</div>
</div>

<div class="eudi-hlr" id="VCR_07c" markdown>
<div class="eudi-hlr__id">VCR_07c<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If a PID is revocable, the PID Provider SHALL revoke that PID if the Wallet Unit on which it resides is revoked, in compliance with requirement WURevocation_18 in [Topic 38][topic-38].

</div>
</div>

<div class="eudi-hlr" id="VCR_07d" markdown>
<div class="eudi-hlr__id">VCR_07d<span class="kw-may">MAY</span></div>
<div class="eudi-hlr__body" markdown>

If an attestation is revocable, the Attestation Provider MAY revoke that attestation if the Wallet Unit on which it resides is revoked, in compliance with requirement WURevocation_19 in [Topic 38][topic-38].

</div>
</div>

<div class="eudi-hlr" id="VCR_07e" markdown>
<div class="eudi-hlr__id">VCR_07e<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If a Wallet Provider uses the per-KA approach for key attestation revocation (see WUA_28), it SHALL revoke a WSCD or keystore upon the explicit request of the User to revoke their WSCD or keystore.

*Note: a) The most likely cause of such a request would be that the WSCD or keystore is a local external smart card and the User lost their WSCD or keystore. b) In contrast, under the type-shared index approach (see WUA_28), revoking the WSCD or keystore is not a per-Wallet Unit action that can be triggered by user requests. c) See also WURevocation_07a.*

</div>
</div>

<div class="eudi-hlr" id="VCR_08" markdown>
<div class="eudi-hlr__id">VCR_08<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If a PID is revocable, the PID Provider SHALL revoke a PID upon the death of the natural person who is the subject of the PID.

*Note: a) In addition, in these circumstances the PID Provider also requests the Wallet Provider to revoke the Wallet Unit, see WURevocation_11. b) The topic of Wallet Units for legal persons, possibly containing a legal-person PID, has has been removed from this ARF in view of the development of a separate business wallet.*

</div>
</div>

<div class="eudi-hlr" id="VCR_09" markdown>
<div class="eudi-hlr__id">VCR_09<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If a technical PID or attestation is revocable, the PID Provider or Attestation Provider SHALL revoke that PID or attestation if the value of one or more of the attributes in the corresponding logical PID or attestation was changed (including attributes being added or deleted) and the technical PID or attestation is still valid for at least 24 hours. Subsequently, if the User's contact details are known, the PID Provider or Attestation Provider SHOULD, via an out-of-band manner, notify the User about the revocation and ask the User to request re-issuance of the PID or attestation using their Wallet Unit.

*Note: If the value of the attributes is determined by a party different from the PID Provider or Attestation Provider, such as an Authentic Source, the Provider is responsible for ensuring that this third party notifies them about such changes.*

</div>
</div>

<div class="eudi-hlr" id="VCR_10" markdown>
<div class="eudi-hlr__id">VCR_10<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Wallet Providers SHALL implement the Attestation Status List and Attestation Revocation List mechanisms specified per VCR_11 in their Wallet Solutions.

</div>
</div>

<div class="eudi-hlr" id="VCR_11" markdown>
<div class="eudi-hlr__id">VCR_11<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For [ISO/IEC 18013-5]-compliant PIDs and attestations, the PID Provider or Attestation Provider SHALL implement the Attestation Status List or Attestation Revocation List mechanism as specified in Annex 2 of (the amended) CIR [2024/2979).

*Note: a) 'Attestation Status List' and 'Attestation Revocation List' are specific mechanisms, these terms are defined in Annex 1. b) Attestation Revocation Lists are sometimes referred to as 'Identifier Lists'. c) The relevant texts in this CIR are copied from the forthcoming 2nd edition of ISO/IEC 18013-5, available [here](https://github.com/ISOWG10/ISO-18013/tree/main/Working%20Documents).*

</div>
</div>

<div class="eudi-hlr" id="VCR_11a" markdown>
<div class="eudi-hlr__id">VCR_11a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For [SD-JWT VC]-compliant PIDs and attestations, the PID Provider or Attestation Provider SHALL implement the Attestation Status List mechanism as specified in [Token Status List].

*Note: No suitable specification of Attestation Revocation Lists in JSON format is available.*

</div>
</div>

<div class="eudi-hlr" id="VCR_12" markdown>
<div class="eudi-hlr__id">VCR_12<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If a Relying Party decides it needs to be able to verify the revocation status of PIDs or attestations, it SHALL support both the Attestation Status List mechanism and the Attestation Revocation List mechanism specified per VCR_11.

*Note: Per VCR_13, it is recommended but not mandatory for a Relying Party to verify whether a PID or attestation is revoked.*

</div>
</div>

<div class="eudi-hlr" id="VCR_12a" markdown>
<div class="eudi-hlr__id">VCR_12a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A PID Provider or Attestation Provider SHALL support the mechanism specified per VCR_01a for verifying the revocation status of a WIA or KA.

</div>
</div>

<div class="eudi-hlr" id="VCR_13" markdown>
<div class="eudi-hlr__id">VCR_13<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Relying Party Instance SHOULD verify the revocation status of a revocable PID or attestation upon obtaining it from a Wallet Unit. When a Relying Party considers deviating from this recommendation by not performing revocation checking, it SHALL perform a risk analysis considering all relevant factors for the use case, including risks to the User, the PID Provider or Attestation Provider, and risks to the Relying Party itself.

</div>
</div>

<div class="eudi-hlr" id="VCR_14" markdown>
<div class="eudi-hlr__id">VCR_14<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Relying Party SHALL perform a risk analysis considering all relevant factors for the use case, including risks to the User and risks to the Relying Party itself, to determine whether it will accept or refuse a PID or attestation in case no reliable information regarding the revocation status of that PID or attestation is available.

*Note: Examples of conditions under which no reliable revocation information is available are 1) The attestation does not contain revocation information (because it is not revocable). 2) The Relying Party Instance is offline and any cached status information is no longer valid. 3) The latest attestation status lists or attestation identifier lists provided by the PID Provider or Attestation Provider (i.e., available online) are no longer valid. 4) The Relying Party Instance is offline, but the use case requires up-to-date revocation information (instead of trusting cached information that is still valid.)*

</div>
</div>

<div class="eudi-hlr" id="VCR_15" markdown>
<div class="eudi-hlr__id">VCR_15<span class="kw-should">SHOULD</span></div>
<div class="eudi-hlr__body" markdown>

A Relying Party Instance SHOULD NOT request the relevant Attestation Status List or Attestation Revocation List each time an attestation is presented to it by a Wallet Unit. Rather, the Relying Party operating the Relying Party Instance SHOULD download each new version of the list once, at a time and from a location unrelated to the presentation of a PID or attestation by a User. The Relying Party SHOULD then distribute the list to all of its Relying Party Instances, using an Relying Party-internal distribution mechanism. Each Relying Party Instance SHOULD cache the list, so that it can perform revocation checks without making an online request. The Relying Party SHOULD perform a risk analysis to determine the frequency with which it will download the revocation lists and the maximum caching period its Relying Party Instances will use.

</div>
</div>

<div class="eudi-hlr" id="VCR_16" markdown>
<div class="eudi-hlr__id">VCR_16<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A PID Provider, Attestation Provider or Wallet Provider SHALL NOT require the Relying Party or Relying Party Instance to authenticate itself before downloading an Attestation Status List or Attestation Revocation List.

</div>
</div>

<div class="eudi-hlr" id="VCR_17" markdown>
<div class="eudi-hlr__id">VCR_17<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

When using an Attestation Status List for revocation, the PID Provider, Attestation Provider or Wallet Provider SHALL randomly assign the index for each PID or attestation, to prevent this index from becoming a correlator.

*Note: Randomly assigning indices within a bitstring or byte array is more complicated than creating random identifiers (e.g. serial numbers) for attestations, as is needed for an Attestation Revocation List. This is because duplicate indices and unnecessarily long bitstrings or byte arrays must be prevented.*

</div>
</div>

<div class="eudi-hlr" id="VCR_18" markdown>
<div class="eudi-hlr__id">VCR_18<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

When using an Attestation Status List for revocation, the PID Provider, Attestation Provider, or Wallet Provider SHALL represent a sufficiently large number of PIDs, attestations, WIAs, or KAs on each Attestation Status List to ensure herd privacy.

*Note: In this context, herd privacy means that if an entity requests a particular status list, the PID Provider, Attestation Provider, or Wallet Provider is not able to deduce which PID, attestation, WIA, or KA (likely) was presented to that entity. Complying with this requirement may be difficult in case the number of PIDs, attestations, WIAs, or KAs to be represented on the list is small. In such a case, decoy entries can be added to the list to obfuscate the real number of referenced PIDs, attestations, WIAs, or KAs.*

</div>
</div>

<div class="eudi-hlr" id="VCR_19" markdown>
<div class="eudi-hlr__id">VCR_19<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Instance SHOULD regularly check the revocation status of its PIDs and attestations. In addition, the Wallet Instance SHOULD regularly check whether itself or any WSCD or keystore it uses has been revoked. In case of any revocation, the Wallet Instance SHALL notify the User accordingly.

*Note: A Wallet Instance can check its own revocation status using its WIAs, and the revocation status of its WSCD and keystores using its key attestations.*

</div>
</div>


[](){ #topic-9 }
