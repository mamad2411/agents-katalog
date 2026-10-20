---
name: "hlr-24-user-identification-in-proximity-scenari"
description: "Use when working with EUDI high-level requirements for 'User identification in proximity scenarios'. Contains normative SHALL/SHOULD/MAY requirements from ARF Annex 2."
sections:
  - "A.2.3.14 Topic 24 - User identification in proximity scenarios"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~953 -->

#### A.2.3.14 Topic 24 - User identification in proximity scenarios

<div class="eudi-hlr" id="ProxId_01" markdown>
<div class="eudi-hlr__id">ProxId_01<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

To enable identification using proximity flows, Wallet Units SHALL support device retrieval as specified in ISO/IEC 18013-5 for presenting PID or attestation attributes. Wallet Units SHALL comply with the requirements for mDLs and mdocs ISO/IEC 18013-5.

*Note: Nominally, ISO/IEC 18013-5 is intended only for mDLs and mDL readers. The corresponding standard for mobile documents in general (including Wallet Units with the EUDI Wallet ecosystem) will be ISO/IEC 23220-4, which is based on ISO/IEC 18013-5. However, the latter standard is not finished yet and therefore cannot be referenced at the moment. To guarantee interoperability between Wallet Units and Relying Party Instances in proximity scenarios, it is necessary to make choices from among the possibilities specified in ISO/IEC 18013-5. Making the same choices as for mDLs ensure this.*

</div>
</div>

<div class="eudi-hlr" id="ProxId_01a" markdown>
<div class="eudi-hlr__id">ProxId_01a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If a Relying Party supports using proximity flows, its Relying Party Instances SHALL support device retrieval as specified in ISO/IEC 18013-5 for requesting PID or attestation attributes. Such Relying Party Instances SHALL comply with the requirements for mDL readers and mdoc readers in ISO/IEC 18013-5.

*Note: See note to ProxId_01. Support for proximity flows by Relying Parties is not mandatory.*

</div>
</div>

<div class="eudi-hlr" id="ProxId_02" markdown>
<div class="eudi-hlr__id">ProxId_02<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Wallet Units, PID Providers, Attestation Providers, Wallet Providers, and Relying Parties SHALL NOT support server retrieval as specified in ISO/IEC 18013-5 for requesting and presenting PID or attestation attributes.

*Note: Using server retrieval, a Relying Party would request User attributes directly from a PID Provider or Attestation Provider, after having received an authentication and/or authorisation token from the User's Wallet Unit.*

</div>
</div>

<div class="eudi-hlr" id="ProxId_03" markdown>
<div class="eudi-hlr__id">ProxId_03<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL present the presentation request and the identity of the Relying Party to the User when processing the request.

</div>
</div>

<div class="eudi-hlr" id="ProxId_04" markdown>
<div class="eudi-hlr__id">ProxId_04<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL request its User to approve the presentation of attributes from their Wallet Unit for proximity identification before presenting them to the Relying Party or Verifier Wallet Unit.

</div>
</div>

<div class="eudi-hlr" id="ProxId_05" markdown>
<div class="eudi-hlr__id">ProxId_05<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL transmit the requested User attributes to the requesting Relying Party Instance securely in accordance with ISO/IEC 18013-5 for proximity flows.

</div>
</div>

<div class="eudi-hlr" id="ProxId_06" markdown>
<div class="eudi-hlr__id">ProxId_06</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>


[](){ #topic-25 }
