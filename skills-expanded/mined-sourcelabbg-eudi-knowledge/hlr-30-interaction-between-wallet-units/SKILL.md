---
name: "hlr-30-interaction-between-wallet-units"
description: "Use when working with EUDI high-level requirements for 'Interaction between Wallet Units'. Contains normative SHALL/SHOULD/MAY requirements from ARF Annex 2."
sections:
  - "A.2.3.19 Topic 30 - Interaction between Wallet Units"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~2878 -->

#### A.2.3.19 Topic 30 - Interaction between Wallet Units

<div class="eudi-hlr" id="W2W_01" markdown>
<div class="eudi-hlr__id">W2W_01<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL be able to act as a Holder Wallet Unit, in accordance with all requirements in this Topic.

</div>
</div>

<div class="eudi-hlr" id="W2W_02" markdown>
<div class="eudi-hlr__id">W2W_02<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

When acting as a Holder Wallet Unit, if there is a contradiction between a requirement for Holder Wallet Units in this Topic and any requirement for Wallet Units in other Topics in this document, the requirement in this Topic SHALL take precedence. However, when acting as a Holder Wallet Unit, a Wallet Unit SHALL comply with all requirements for Wallet Units in other Topics in this document that do not contradict any requirement in this Topic.

</div>
</div>

<div class="eudi-hlr" id="W2W_03" markdown>
<div class="eudi-hlr__id">W2W_03<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL be able to act as a Verifier Wallet Unit, in accordance with all requirements in this Topic.

</div>
</div>

<div class="eudi-hlr" id="W2W_04" markdown>
<div class="eudi-hlr__id">W2W_04<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

When acting as a Verifier Wallet Unit, a Wallet Unit SHALL NOT comply with any requirement for Wallet Units in other Topics in this document.

</div>
</div>

<div class="eudi-hlr" id="W2W_05" markdown>
<div class="eudi-hlr__id">W2W_05<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL act as a Holder Wallet Unit only if the User selects a 'Holder Wallet Unit mode'. If the User closes the Wallet Unit, or after a period of non-activity, the Wallet Unit SHALL return to 'normal' mode.

</div>
</div>

<div class="eudi-hlr" id="W2W_06" markdown>
<div class="eudi-hlr__id">W2W_06<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

When entering the Holder Wallet Unit mode, a Wallet Unit SHALL inform its User that this mode should only be used for interactions with natural persons using a Wallet Unit, and that the User should not proceed if they are in fact interacting with a Relying Party.

</div>
</div>

<div class="eudi-hlr" id="W2W_07" markdown>
<div class="eudi-hlr__id">W2W_07<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL act as a Verifier Wallet Unit only if the User selects a 'Verifier Wallet Unit mode'. If the User closes the Wallet Unit, or after a period of non-activity, the Wallet Unit SHALL return to 'normal' mode.

</div>
</div>

<div class="eudi-hlr" id="W2W_08" markdown>
<div class="eudi-hlr__id">W2W_08<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Verifier Wallet Unit and a Holder Wallet Unit SHALL support attestation presentation only in proximity, meaning they SHALL support only [ISO/IEC 18013-5] to communicate.

</div>
</div>

<div class="eudi-hlr" id="W2W_09" markdown>
<div class="eudi-hlr__id">W2W_09<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Holder Wallet Units SHALL comply with the requirements for mDLs and for mdocs in ISO/IEC 18013-5, unless specified differently in [Technical Specification 9](../../technical-specifications/ts9-wallet-to-wallet-interactions.md).

</div>
</div>

<div class="eudi-hlr" id="W2W_10" markdown>
<div class="eudi-hlr__id">W2W_10<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Verifier Wallet Units SHALL comply with the requirements for mDL readers and for mdoc readers in ISO/IEC 18013-5, unless specified differently in [Technical Specification 9](../../technical-specifications/ts9-wallet-to-wallet-interactions.md).

</div>
</div>

<div class="eudi-hlr" id="W2W_11" markdown>
<div class="eudi-hlr__id">W2W_11<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Holder Wallet Unit SHOULD provide the Holder, through a user-friendly UI, with the option to inform the Verifier Wallet Unit about the attributes which the Verifier should include in the presentation request, by sending a presentation offer. If the Holder creates a presentation offer, the Holder Wallet Unit SHALL transfer it to the Verifier Wallet Unit as specified in [Technical Specification 9](../../technical-specifications/ts9-wallet-to-wallet-interactions.md).

*Note: TS9 specifies an extension of the device engagement structure specified in [ISO/IEC 18013-5].*

</div>
</div>

<div class="eudi-hlr" id="W2W_12" markdown>
<div class="eudi-hlr__id">W2W_12<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Holder Wallet Unit SHALL recommend the Holder to create a presentation offer, as this will increase the chance of success of the use case.

</div>
</div>

<div class="eudi-hlr" id="W2W_13" markdown>
<div class="eudi-hlr__id">W2W_13<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Verifier Wallet Unit SHALL provide the Verifier, through a user-friendly UI, with the possibility to select the attributes that will be included in the presentation request.

</div>
</div>

<div class="eudi-hlr" id="W2W_14" markdown>
<div class="eudi-hlr__id">W2W_14<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For the purposes of W2W_13, if the Verifier Wallet Unit received a presentation offer, it SHALL present this offer to the Verifier, and enable the Verifier to include one or more of the attributes in the offer into the presentation request. However, the Verifier Wallet Unit SHALL NOT allow the Verifier to include any attribute not present in the offer.

</div>
</div>

<div class="eudi-hlr" id="W2W_15" markdown>
<div class="eudi-hlr__id">W2W_15<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For the purposes of W2W_13, if the Verifier Wallet Unit did not receive a presentation offer, it SHALL present the Verifier with a list of attributes that can be included in the presentation request. The Verifier Wallet Unit MAY ask the Verifier some questions about the purpose of the use case to narrow down the list.

</div>
</div>

<div class="eudi-hlr" id="W2W_16" markdown>
<div class="eudi-hlr__id">W2W_16<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Verifier Wallet Unit SHALL authenticate the Verifier and SHALL obtain the Verifier's approval prior to sending a presentation request to a Holder Wallet Unit.

</div>
</div>

<div class="eudi-hlr" id="W2W_17" markdown>
<div class="eudi-hlr__id">W2W_17<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Verifier Wallet Unit SHALL implement measures to limit the number of presentation requests it can send per unit of time, to prevent abuse of the Wallet-to-Wallet functionality by Relying Parties. The limitation strategy, for instance exponential backoff time between subsequent presentation requests or hard limits for the number of requests, SHALL be decided by the Wallet Provider, based on applicable requirements in [Technical Specification 9](../../technical-specifications/ts9-wallet-to-wallet-interactions.md).

</div>
</div>

<div class="eudi-hlr" id="W2W_18" markdown>
<div class="eudi-hlr__id">W2W_18</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="W2W_19" markdown>
<div class="eudi-hlr__id">W2W_19<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

When receiving a presentation response, a Verifier Wallet SHALL verify the received attestation according to requirements OIA_12 - OIA_15 in [Topic 1][topic-1].

</div>
</div>

<div class="eudi-hlr" id="W2W_20" markdown>
<div class="eudi-hlr__id">W2W_20<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Verifier Wallet Unit SHALL display all verified attributes to the Verifier.

</div>
</div>

<div class="eudi-hlr" id="W2W_21" markdown>
<div class="eudi-hlr__id">W2W_21<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Verifier Wallet Unit SHALL NOT persistently store any attestations or attributes received. A Verifier Wallet Unit SHOULD minimise the time the received presentation is stored in memory. A Verifier Wallet Unit SHALL comply with OIA_16 in [Topic 1][topic-1].

</div>
</div>

<div class="eudi-hlr" id="W2W_22" markdown>
<div class="eudi-hlr__id">W2W_22<span class="kw-should">SHOULD</span></div>
<div class="eudi-hlr__body" markdown>

Wallet Providers SHOULD take measures to prevent a User from taking screenshots while their Wallet Unit is acting as a Verifier Wallet Unit.

</div>
</div>

<div class="eudi-hlr" id="W2W_23" markdown>
<div class="eudi-hlr__id">W2W_23<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

When sending a presentation request to a Holder Wallet Unit, a Verifier Wallet Unit SHALL include in that request a cryptographic proof that it is a genuine, non-revoked EUDI Wallet Unit operated by a recognised Wallet Provider, bound to the protocol session in which the presentation request is sent, if a common method to provide such a proof is established in a technical specification.

*Note: Such a specification is being developed within ETSI.*

</div>
</div>

<div class="eudi-hlr" id="W2W_24" markdown>
<div class="eudi-hlr__id">W2W_24<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Before presenting a received presentation request to the Holder, a Holder Wallet Unit SHALL authenticate the Verifier Wallet Unit by verifying the proof meant in W2W_23, if present.

</div>
</div>

<div class="eudi-hlr" id="W2W_25" markdown>
<div class="eudi-hlr__id">W2W_25<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If the verification required by W2W_24 fails or cannot be performed, a Holder Wallet Unit SHALL notify the User. In addition, the Wallet Unit SHALL either not present the requested attributes to the Verifier Wallet Unit, or give the User the choice to present the requested attributes or not.

*Note: It is up to the Wallet Provider to make a choice for one of these two options.*

</div>
</div>


[](){ #topic-31 }
