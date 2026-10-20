---
name: "hlr-01-accessing-online-services-with-a-wallet-"
description: "Use when working with EUDI high-level requirements for 'Accessing Online Services with a Wallet Unit'. Contains normative SHALL/SHOULD/MAY requirements from ARF Annex 2."
sections:
  - "A.2.3.1 Topic 1 - Accessing Online Services with a Wallet Unit"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~4903 -->

#### A.2.3.1 Topic 1 - Accessing Online Services with a Wallet Unit

<div class="eudi-hlr" id="OIA_01" markdown>
<div class="eudi-hlr__id">OIA_01<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For proximity presentation flows, a Wallet Unit SHALL support the transmission mechanism specified in [ISO/IEC 18013-5] to receive and respond to presentation requests for person identification data (PID) and attestations by Relying Parties.

</div>
</div>

<div class="eudi-hlr" id="OIA_01a" markdown>
<div class="eudi-hlr__id">OIA_01a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For remote presentation flows, a Wallet Unit SHALL support the following transmission mechanisms: - The API-mediated mechanisms specified in OIA_08, OIA_08a, and OIA_08b, - The mechanisms based on redirects specified in OIA_03b and OIA_03c.

</div>
</div>

<div class="eudi-hlr" id="OIA_02" markdown>
<div class="eudi-hlr__id">OIA_02<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL support proving cryptographic device binding between the WSCA/WSCD or a keystore included in the Wallet Unit and a PID or attestation, in accordance with [SD-JWT VC] or [ISO/IEC 18013-5].

*Note: Such a mechanism is called 'mdoc authentication' in [ISO/IEC 18013-5] and 'key binding' in [SD-JWT VC].*

</div>
</div>

<div class="eudi-hlr" id="OIA_03" markdown>
<div class="eudi-hlr__id">OIA_03<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

When issuing, presenting, or verifying an attestation, Wallet Units, PID Providers, Attestation Providers, and Relying Parties SHALL only use cryptographic algorithms included in the [ECCG Agreed Cryptographic Mechanisms v2.0].

</div>
</div>

<div class="eudi-hlr" id="OIA_03a" markdown>
<div class="eudi-hlr__id">OIA_03a</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="OIA_03b" markdown>
<div class="eudi-hlr__id">OIA_03b<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For remote presentation flows using redirects and [OpenID4VP], when the format of the requested attestation complies with [ISO/IEC 18013-5], Relying Parties and Wallet Units SHALL comply with the requirements in [HAIP] Sections 5, 5.1 and 5.3.1, as well as with the 'ISO mdocs' profile in Section 6 and with Sections 7 and 8.

*Note: a) '[HAIP] Section 5' refers only to the requirements directly under the Section 5 heading. This does not include sections 5.1, 5.2, and 5.3. b) For clarity: in [HAIP] v1.0, the 'ISO mdocs' profile implies that Relying Parties and Wallet Units must comply with the applicable requirements in [OpenID4VP] Annex B.2. c) This requirement and OIA_03c both correspond to the profile for transmission via redirects specified in [ETSI TS 119 472-2] Section 1, but are more specific with regard to format of the attestation.*

</div>
</div>

<div class="eudi-hlr" id="OIA_03c" markdown>
<div class="eudi-hlr__id">OIA_03c<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For remote presentation flows using redirects and [OpenID4VP], when the format of the requested attestation complies with [SD-JWT VC], Relying Parties and Wallet Units SHALL comply with the requirements in [HAIP] Sections 5, 5.1, and 5.3.2, as well as with the 'IETF SD-JWT VCs' profile in Section 6 and with Sections 7 and 8

*Note: a) '[HAIP] Section 5' refers only to the requirements directly under the Section 5 heading. This does not include sections 5.1, 5.2, and 5.3. b) For clarity: in [HAIP] v1.0 Section 6, the 'IETF SD-JWT VCs' profile implies that Relying Parties and Wallet Units must comply with the requirements in [OpenID4VP] Annex B.3, as well as with the requirements in Section 6.1.*

</div>
</div>

<div class="eudi-hlr" id="OIA_03d" markdown>
<div class="eudi-hlr__id">OIA_03d<span class="kw-may">MAY</span></div>
<div class="eudi-hlr__body" markdown>

For remote presentation flows using redirects and [ISO/IEC 18013-7], Relying Parties and Wallet Units MAY comply with the requirements in [ISO/IEC 18013-7] Annex A.

</div>
</div>

<div class="eudi-hlr" id="OIA_04" markdown>
<div class="eudi-hlr__id">OIA_04</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="OIA_05" markdown>
<div class="eudi-hlr__id">OIA_05<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

After verifying and processing a PID or attestation request, the Wallet Unit SHALL display to the User the identity of the requesting Relying Party and the requested attributes.

</div>
</div>

<div class="eudi-hlr" id="OIA_06" markdown>
<div class="eudi-hlr__id">OIA_06<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL present the requested attributes only after having received the User's approval.

*Note: See also OIA_07.*

</div>
</div>

<div class="eudi-hlr" id="OIA_07" markdown>
<div class="eudi-hlr__id">OIA_07<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL support selective disclosure of attributes from PIDs and attestations to be presented to the requesting Relying Parties.

</div>
</div>

<div class="eudi-hlr" id="OIA_08" markdown>
<div class="eudi-hlr__id">OIA_08<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For remote presentation flows using the [W3C Digital Credentials API] and [OpenID4VP], when the format of the requested attestation complies with [ISO/IEC 18013-5], Relying Parties and Wallet Units SHALL comply with the requirements in [HAIP] Sections 5, 5.2 and 5.3.1, as well as with the 'ISO mdocs' profile in Section 6 and with Sections 7 and 8. 

*Note: a) '[HAIP] Section 5' refers only to the requirements directly under the Section 5 heading. b) For clarity: in [HAIP] v1.0, the 'ISO mdocs' profile implies that Relying Parties and Wallet Units must comply with the applicable requirements in [OpenID4VP] Annex B.2. c) This requirement and OIA_08a both correspond to the profile for API-mediated transmission specified in [ETSI TS 119 472-2] Section 1, but are more specific with regard to format of the attestation.*

</div>
</div>

<div class="eudi-hlr" id="OIA_08a" markdown>
<div class="eudi-hlr__id">OIA_08a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For remote presentation flows using the [W3C Digital Credentials API] and [OpenID4VP], when the format of the requested attestation complies with [SD-JWT VC], Relying Parties and Wallet Units SHALL comply with the requirements in [HAIP] Sections 5, 5.2 and 5.3.2, as well as with the 'IETF SD-JWT VCs' profile in Section 6 and with Sections 7 and 8.

*Note: a) '[HAIP] Section 5' refers only to the requirements directly under the Section 5 heading. b) For clarity: in [HAIP] v1.0 Section 6, the 'IETF SD-JWT VCs' profile implies that Relying Parties and Wallet Units must comply with the requirements in [OpenID4VP] Annex B.3, as well as with the requirements in Section 6.1.*

</div>
</div>

<div class="eudi-hlr" id="OIA_08b" markdown>
<div class="eudi-hlr__id">OIA_08b<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For remote presentation flows using the [W3C Digital Credentials API] and [ISO/IEC 18013-7], Relying Party Instances and Wallet Units SHALL comply with the requirements in [ISO/IEC 18013-7] Annex C.

*Note: The latter restriction applies even if such disclosure would enhance the services provided by the operating system to the Wallet Unit, for example, attestation selection in the context of the Digital Credentials API.*

</div>
</div>

<div class="eudi-hlr" id="OIA_08c" markdown>
<div class="eudi-hlr__id">OIA_08c<span class="kw-should">SHOULD</span></div>
<div class="eudi-hlr__body" markdown>

Wallet Units SHOULD NOT support using a redirects-based transmission mechanism for cross-device presentation flows.

</div>
</div>

<div class="eudi-hlr" id="OIA_08d" markdown>
<div class="eudi-hlr__id">OIA_08d<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If a Relying Party uses a redirects-based transmission mechanism for cross-device presentation flows, it SHALL implement adequate mitigations for the challenges described in [Section 4.4.3.1][4431-introduction] of the ARF main document.

</div>
</div>

<div class="eudi-hlr" id="OIA_08e" markdown>
<div class="eudi-hlr__id">OIA_08e<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL, by default (see OIA_08f), disclose the presence of all stored attestations (meaning their attestation type) to the Digital Credentials API framework, but it SHALL NOT disclose the presence of attributes in these attestations, nor their values.

*Note: The latter restriction applies even if such disclosure would enhance the services provided by the operating system to the Wallet Unit, for example, attestation selection in the context of the Digital Credentials API.*

</div>
</div>

<div class="eudi-hlr" id="OIA_08f" markdown>
<div class="eudi-hlr__id">OIA_08f<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL provide a global User setting to disable the disclosure of stored attestations to the Digital Credentials API framework, as described in OIA_08e. When this setting is set to disable disclosure, the Wallet Unit SHOULD subsequently enable the User to select individual attestations to be disclosed to the DC API.

*Note: If this setting is set to disable disclosure and the User does not subsequently select any individual attestations to be disclosed, the Wallet Unit will not disclose any attributes at all. As a result, presentation requests sent using the DC API will likely fail.*

</div>
</div>

<div class="eudi-hlr" id="OIA_08g" markdown>
<div class="eudi-hlr__id">OIA_08g<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

In cross-device presentation flows using the [W3C Digital Credentials API], a Wallet Unit SHALL verify that the Relying Party Instance is in close physical proximity to the Wallet Unit. For this proximity check the Wallet Unit SHALL use a secure, direct, and user-mediated local communication channel, such as a short-range wireless communication technology.

*Note: In [CTAP] terms, this proximity check is the BLE proximity engagement, present in both the Hybrid transport specified in [CTAP] v2.2 and in [CTAP] v2.3. Where both devices support it, the underlying operating systems, browsers, mediating APIs, or any other technical layer outside the control of the Wallet Unit, should prefer performing both the proximity check and the data transfer over a local short-range channel (as enabled by [CTAP] v2.3) over the use of a Hybrid tunnel service first defined in [CTAP] v2.2.*

</div>
</div>

<div class="eudi-hlr" id="OIA_09" markdown>
<div class="eudi-hlr__id">OIA_09<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For remote presentation flows the Wallet Unit SHALL ensure that the attributes included in the presented attestation are accessible only to the Relying Party Instance, by encrypting the presentation response.

</div>
</div>

<div class="eudi-hlr" id="OIA_10" markdown>
<div class="eudi-hlr__id">OIA_10<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For both proximity and remote presentation flows, if a Wallet Unit contains multiple PIDs having the same encoding (e.g. ISO/IEC 18013-5 or SD-JWT VC-compliant) and a Relying Party requests a PID having that encoding, the Wallet Unit SHALL ask the User which of these PIDs they want to present, unless the Wallet Unit can decide from context.

*Note: This requirement is not about multiple technical PIDs corresponding to a single logical PID, but to different logical PIDs whose technical PIDs have the same encoding. Probably, these logical PIDs are issued by different PID Providers.*

</div>
</div>

<div class="eudi-hlr" id="OIA_11" markdown>
<div class="eudi-hlr__id">OIA_11<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For both proximity and remote presentation flows, if a Wallet Unit contains multiple attestations having the same encoding (e.g. ISO/IEC 18013-5 or SD-JWT VC-compliant) and the same attestation type, and a Relying Party requests an attestation having that type and encoding, the Wallet Unit SHALL ask the User which of these attestations they want to present, unless the Wallet Unit can decide from context.

*Note: a) Attestation types are explained in [Topic 12][topic-12]]. b) See note to OIA_10, which applies mutatis mutandis.*

</div>
</div>

<div class="eudi-hlr" id="OIA_12" markdown>
<div class="eudi-hlr__id">OIA_12<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For both proximity and remote presentation flows, a Relying Party SHALL validate the signature of a PID using a trust anchor provided in a PID Provider LoTE made available in accordance with [Topic 31][topic-31]].

</div>
</div>

<div class="eudi-hlr" id="OIA_13" markdown>
<div class="eudi-hlr__id">OIA_13<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For both proximity and remote presentation flows, a Relying Party SHALL validate the qualified signature of a QEAA in accordance with Art.32 of the [European Digital Identity Regulation]. For the verification, the Relying Party SHALL use a trust anchor provided in a QEAA Provider Trusted List made available in accordance with [Art. 22](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=uriserv%3AOJ.L_.2014.257.01.0073.01.ENG#d1e2162-73-1) of the [European Digital Identity Regulation].

</div>
</div>

<div class="eudi-hlr" id="OIA_14" markdown>
<div class="eudi-hlr__id">OIA_14<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For both proximity and remote presentation flows, a Relying Party SHALL validate the signature of a PuB-EAA using a trust anchor provided in a Pub-EAA Provider LoTE made available in accordance with [Topic 31][topic-31]].

</div>
</div>

<div class="eudi-hlr" id="OIA_15" markdown>
<div class="eudi-hlr__id">OIA_15<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For both proximity and remote presentation flows, a Relying Party SHALL validate the signature of a non-qualified EAA using a trust anchor provided according to the mechanism(s) specified in the applicable Attestation Rulebook, see [Topic 12][topic-12]].

*Note: a) OIA_12 - OIA_15 imply that a Relying Party Instance must know if the attestation it is requesting from a Wallet Instance is a PID, a QEAA, a PuB-EAA, or a non-qualified EAA. These requirements also imply that the Relying Party Instance must store trust anchors in such a way that, at the time of verification, it is able to distinguish between trust anchors usable either for PIDs, for QEAAs, for PuB-EAAs, or for non-qualified EAAs.*

</div>
</div>

<div class="eudi-hlr" id="OIA_15a" markdown>
<div class="eudi-hlr__id">OIA_15a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Relying Party SHALL perform regular trust anchor management, meaning it SHALL download the latest version of all applicable Trusted Lists and LoTEs. If it finds that new trusted entities have been added, or that new trust anchors have been added for existing trusted entities, it SHALL ensure that these trust anchors are properly stored in all relevant Relying Party Instances. Conversely, if the Relying Party finds that an existing trusted entity has been invalidated in the Trusted List or LoTE, or that some of the trust anchors of existing trusted entities have expired, been revoked, or otherwise been invalidated, it SHALL ensure that these trust anchors are removed from all Relying Party Instances.

</div>
</div>

<div class="eudi-hlr" id="OIA_15b" markdown>
<div class="eudi-hlr__id">OIA_15b<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For the retrieval and management of trust anchors, Relying Parties and Relying Party Instances SHALL support both Trusted Lists complying with [ETSI TS 119 612] and LoTEs complying with [ETSI TS 119 602].

*Note: Trusted Lists complying with [ETSI TS 119 612] are used for the distribution of trust anchors of QEAA Providers. LoTEs complying with [ETSI TS 119 602] are used for the distribution of trust anchors of PID Providers, PuB-EAA Providers, Access Certificate Authorities, and Providers of registration certificates.*

</div>
</div>

<div class="eudi-hlr" id="OIA_16" markdown>
<div class="eudi-hlr__id">OIA_16<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

When receiving a PID or attestation, a Relying Party Instance SHALL discard the values of all unique elements, including at least the ones mentioned in requirement ISSU_35 in [Topic 10][topic-10], as well as any timestamps, as soon as they are no longer needed. The Relying Party Instance SHALL NOT communicate these values to the Relying Party or to any other party inside or outside the EUDI Wallet ecosystem.

</div>
</div>

<div class="eudi-hlr" id="OIA_17" markdown>
<div class="eudi-hlr__id">OIA_17<span class="kw-should">SHOULD</span></div>
<div class="eudi-hlr__body" markdown>

A Relying Party Instance SHOULD verify the device-binding signature or Message Authentication Code provided in the presentation response of the Wallet Unit during the presentation of a PID or device-bound attestation, following the steps specified per [ISO/IEC 18013-5] or [SD-JWT VC], as applicable.

</div>
</div>


[](){ #topic-3 }
