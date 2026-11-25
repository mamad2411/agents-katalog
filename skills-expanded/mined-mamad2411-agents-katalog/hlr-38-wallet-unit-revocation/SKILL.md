---
name: "hlr-38-wallet-unit-revocation"
description: "Use when working with EUDI high-level requirements for 'Wallet Unit revocation'. Contains normative SHALL/SHOULD/MAY requirements from ARF Annex 2."
sections:
  - "A.2.3.22 Topic 38 - Wallet Unit revocation"
  - "A. Issuing a Wallet Unit Attestation <!-- omit from toc -->"
  - "B. Revoking a Wallet Unit <!-- omit from toc -->"
  - "C. Informing the User <!-- omit from toc -->"
  - "D. Verifying the revocation status of a Wallet Unit <!-- omit from toc -->"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~3667 -->

#### A.2.3.22 Topic 38 - Wallet Unit revocation

##### A. Issuing a Wallet Unit Attestation <!-- omit from toc -->

<div class="eudi-hlr" id="WURevocation_01" markdown>
<div class="eudi-hlr__id">WURevocation_01<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

To enable a PID Provider or an Attestation Provider to verify the authenticity and the revocation status of a Wallet Unit it is interacting with, a Wallet Provider SHALL issue one or more Key Attestations (KA) and Wallet Instance Attestations (WIA) to the Wallet Unit, as specified in [Topic 9][topic-9].

*Note: The first of these KAs and WIAs will be issued during the activation phase of a Wallet Unit. During the lifetime of the Wallet Unit, the Wallet Provider will re-issue KAs and WIAs as needed.*

</div>
</div>

<div class="eudi-hlr" id="WURevocation_02" markdown>
<div class="eudi-hlr__id">WURevocation_02</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="WURevocation_03" markdown>
<div class="eudi-hlr__id">WURevocation_03<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Provider SHALL have a policy governing all aspects of WIA and KA issuance and management, in line with clauses 6 and 7 of [ETSI TS 119 471], incorporating the amendments introduced by [CIR 2025/1569] and subject to the necessary adaptations to WIAs and KAs. The policy SHALL distinguish between WIAs, KAs for WSCA/WSCDs, and KAs for keystores. For KAs describing a WSCA/WSCD, the policy SHALL comply with at least the extended normalised certificate policy ('NCP+') requirements as specified in [ETSI EN 319 411-1], insofar applicable for the issuance of KAs rather than public key certificates. For KAs describing a keystore, the policy SHALL comply with at least the normalised certificate policy ('NCP') requirements as specified in [ETSI EN 319 411-1], insofar applicable for the issuance of KAs rather than public key certificates.

</div>
</div>

<div class="eudi-hlr" id="WURevocation_04" markdown>
<div class="eudi-hlr__id">WURevocation_04</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="WURevocation_05" markdown>
<div class="eudi-hlr__id">WURevocation_05</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>


##### B. Revoking a Wallet Unit <!-- omit from toc -->

<div class="eudi-hlr" id="WURevocation_06" markdown>
<div class="eudi-hlr__id">WURevocation_06</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="WURevocation_07" markdown>
<div class="eudi-hlr__id">WURevocation_07<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

To revoke the Wallet Instance of a Wallet Unit, a Wallet Provider SHALL, in the status list(s) for Wallet Instances, set the `revoked` status at all index positions mentioned in the WIAs issued to that Wallet Instance.

</div>
</div>

<div class="eudi-hlr" id="WURevocation_07a" markdown>
<div class="eudi-hlr__id">WURevocation_07a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

To revoke a WSCD or keystore of a Wallet Unit, the Wallet Provider SHALL, in the status list(s) for WSCDs and keystores, set the `revoked` status at all index positions mentioned in the KAs describing that WSCD or keystore.

*Note: For this requirement, it does not matter whether each index in the status list(s) for WSCDs and keystores refers to a type of WSCD or keystore or to an individual WSCD or keystore.*

</div>
</div>

<div class="eudi-hlr" id="WURevocation_08" markdown>
<div class="eudi-hlr__id">WURevocation_08</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="WURevocation_09" markdown>
<div class="eudi-hlr__id">WURevocation_09<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

During the lifetime of a Wallet Unit, the Wallet Provider SHALL regularly verify that the security of the Wallet Unit is not breached or compromised. If the Wallet Provider detects a security breach or compromise, the Wallet Provider SHALL analyse its cause(s) and impact(s). If the breach or compromise affects the trustworthiness or reliability of the Wallet Unit, the Wallet Provider SHALL revoke the Wallet Unit by revoking the Wallet Instance according to WURevocation_07. The Wallet Provider SHALL do so at least in the following circumstances: - If the security of the Wallet Unit, or the security of the mobile device and OS on which the corresponding Wallet Instance is installed, or the security of the WSCA/WSCD it uses for managing critical cryptographic assets, is breached or compromised in a manner that affects its trustworthiness or reliability. - If the security of the Wallet Solution is breached or compromised in a manner that affects the trustworthiness or reliability of all corresponding Wallet Units. - If the security of the common authentication and data protection mechanisms used by the Wallet Unit is breached or compromised in a manner that affects their trustworthiness or reliability. - If the security of the electronic identification scheme under which the Wallet Unit is provided is breached or compromised in a manner that affects its trustworthiness or reliability.

*Note: The first bullet corresponds to a Critical or High Risk level security posture risk status according to the table in [Section 6.5.4.2 of the ARF main document][6542-wallet-unit-revocation], as analysed or detected for a Wallet Instance due to monitoring done according to WPSM_03.*

</div>
</div>

<div class="eudi-hlr" id="WURevocation_09a" markdown>
<div class="eudi-hlr__id">WURevocation_09a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If a breach or compromise detected per WURevocation_09 affects the trustworthiness or reliability of a (type of) WSCA/WSCD or keystore, the Wallet Provider SHALL revoke the corresponding (type of) WSCA/WSCD or keystore according to WURevocation_07a.

*Note: Per WURevocation_09, a compromise of a type of WSCA/WSCD always leads to the revocation of both that type of WSCA/WSCD and of all Wallet Instances using a WSCA/WSCD of that type.*

</div>
</div>

<div class="eudi-hlr" id="WURevocation_09b" markdown>
<div class="eudi-hlr__id">WURevocation_09b</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="WURevocation_09c" markdown>
<div class="eudi-hlr__id">WURevocation_09c<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If a Wallet Provider revokes a keystore of a Wallet Unit, it SHOULD also revoke the entire Wallet Unit by revoking the Wallet Instance. If the Wallet Provider decides to not revoke the Wallet Instance, it SHALL create a risk analysis showing that this does not lead to unacceptable risks to the User, PID Providers and Attestation Providers, Relying Parties, or the Wallet Provider itself.

*Note: If the Wallet Provider does not revoke the Wallet Instance, only the attestations bound to the revoked keystore will be impacted. Other functionalities of the Wallet Unit, including the presentation of a PID, will remain available to the User.*

</div>
</div>

<div class="eudi-hlr" id="WURevocation_10" markdown>
<div class="eudi-hlr__id">WURevocation_10<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Provider SHALL revoke a Wallet Unit upon the explicit request of the User registered during the Wallet Unit activation process, see [Topic 40][topic-40]. To do so, the Wallet Provider SHALL revoke the Wallet Instance (see WURevocation_07). The Wallet Provider SHALL authenticate the User before accepting a request to revoke the Wallet Unit.

</div>
</div>

<div class="eudi-hlr" id="WURevocation_11" markdown>
<div class="eudi-hlr__id">WURevocation_11<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Provider SHALL revoke a Wallet Unit upon the explicit request of a PID Provider, in case the natural person using the Wallet Unit has died. To do so, the Wallet Provider SHALL revoke the Wallet Instance (see WURevocation_07). To identify the Wallet Unit that is to be revoked, the PID Provider SHALL use a Wallet Instance identifier provided by the Wallet Provider in the WIA during PID issuance.

*Note: Under [Technical Specification 3](../../technical-specifications/ts3-wallet-unit-attestation.md), the Wallet Instance identifier used for revocation is conveyed in the WIA (see WUA_08). See also the notes to WUA_08.*

</div>
</div>

<div class="eudi-hlr" id="WURevocation_12" markdown>
<div class="eudi-hlr__id">WURevocation_12<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Before revoking a Wallet Unit per WURevocation_11, the Wallet Provider SHALL verify that the party requesting revocation is indeed a valid PID Provider listed in the LoTE of PID Providers.

</div>
</div>

<div class="eudi-hlr" id="WURevocation_13" markdown>
<div class="eudi-hlr__id">WURevocation_13<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Before requesting a Wallet Provider to revoke a Wallet Unit per WURevocation_11, the PID Provider SHALL ensure that the revocation does not harm the interests of any of the stakeholders. The PID Provider SHALL include a documented policy ensuring that this is the case in the policy meant in WURevocation_03.

</div>
</div>


##### C. Informing the User <!-- omit from toc -->

<div class="eudi-hlr" id="WURevocation_14" markdown>
<div class="eudi-hlr__id">WURevocation_14<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Provider SHALL inform a User without delay, and within 24 hours at most, in case the Wallet Provider decided to revoke the User's Wallet Unit. The Wallet Provider SHALL also inform the User about the reason(s) for the revocation. This information SHALL be understandable for the general public. It SHALL include (a reference to) technical details about any security breach if applicable. The Wallet Provider SHALL inform the User about the function(s) of the Wallet Unit that remain available to the User, if any, and functions that will not work any more. The Wallet Provider SHALL also inform the User about measures they can take to ensure they have a fully working Wallet Unit again as soon as possible, such as migrating to a different Wallet Solution.

*Note: Functions that remain available to the User may include viewing their own attributes in their Wallet Unit and accessing their account at the Wallet Provider.*

</div>
</div>

<div class="eudi-hlr" id="WURevocation_15" markdown>
<div class="eudi-hlr__id">WURevocation_15</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="WURevocation_16" markdown>
<div class="eudi-hlr__id">WURevocation_16<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

To inform a User about the revocation of their Wallet Unit, the Wallet Provider SHALL use a communication channel that is independent of the Wallet Unit. In addition, the Wallet Provider MAY use the Wallet Unit itself to inform the User.

</div>
</div>


##### D. Verifying the revocation status of a Wallet Unit <!-- omit from toc -->

<div class="eudi-hlr" id="WURevocation_17" markdown>
<div class="eudi-hlr__id">WURevocation_17</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="WURevocation_18" markdown>
<div class="eudi-hlr__id">WURevocation_18<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A PID Provider issuing revocable PIDs SHALL, for each of its valid PIDs, regularly verify whether the Wallet Instance on which that PID is residing has been revoked and whether the associated WSCD has been revoked, using the WIA and KA received during issuance of that PID. If either the Wallet Instance or the WSCD has been revoked, the PID Provider SHALL immediately revoke the respective PID.

*Note: a) This requirement aligns with WUA_29, which requires PID Providers to check the revocation status of both the WIA and KA throughout the PID validity period. b) This is a consequence of the legal requirement in [CIR 2024/2977], Article 5, 4.(b). c) See [Technical Specification 3](../../technical-specifications/ts3-wallet-unit-attestation.md) for how the PID Provider can do this verification.*

</div>
</div>

<div class="eudi-hlr" id="WURevocation_19" markdown>
<div class="eudi-hlr__id">WURevocation_19<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

An Attestation Provider issuing revocable attestations MAY decide to revoke an attestation if the Wallet Provider revoked the Wallet Unit on which that attestation is residing, in the same manner as described in WURevocation_18. An Attestation Provider SHALL publish its policy in this regard.

*Note: Publishing its policy regarding revocation allows a Relying Party to decide if it can put sufficient trust in the attestations issued by that Attestation Provider.*

</div>
</div>

<div class="eudi-hlr" id="WURevocation_19a" markdown>
<div class="eudi-hlr__id">WURevocation_19a</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="WURevocation_19b" markdown>
<div class="eudi-hlr__id">WURevocation_19b</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="WURevocation_20" markdown>
<div class="eudi-hlr__id">WURevocation_20</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="WURevocation_21" markdown>
<div class="eudi-hlr__id">WURevocation_21</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>


[](){ #topic-40 }
