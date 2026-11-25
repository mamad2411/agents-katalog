---
name: "hlr-43-embedded-disclosure-policies"
description: "Use when working with EUDI high-level requirements for 'Embedded disclosure policies'. Contains normative SHALL/SHOULD/MAY requirements from ARF Annex 2."
sections:
  - "A.2.3.25 Topic 43 - Embedded disclosure policies"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~1568 -->

#### A.2.3.25 Topic 43 - Embedded disclosure policies

<div class="eudi-hlr" id="EDP_01" markdown>
<div class="eudi-hlr__id">EDP_01<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL enable an Attestation Provider to optionally express an embedded disclosure policy for a QEAA, PuB-EAA, or non-qualified EAA.

*Note: The [European Digital Identity Regulation] does not contain a requirement for PIDs to be able to contain an embedded disclosure policy.*

</div>
</div>

<div class="eudi-hlr" id="EDP_02" markdown>
<div class="eudi-hlr__id">EDP_02<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL support embedded disclosure policies implementing the 'Authorised relying parties only policy' described in Annex III of Implementing Regulation (EU) 2024/2979 and as specified in [ETSI TS 119 472-3]. If present, such an embedded disclosure policy SHALL contain a list of duplets, where each duplet consists of an EU-wide unique Relying Party identifier in combination with a Service identifier, as specified in Reg_32 and Reg_33. After receiving a presentation request, the Wallet Unit SHALL retrieve the unique identifier and Service identifier of the Relying Party from the registration certificate presented by the Relying Party, and compare them to the list of authorised identifier duplets in the policy for the requested attestation. If the identifier duplet is not included in this list, the Wallet Unit SHALL consider the evaluation of the embedded disclosure policy to have failed, and inform the User.

*Note: The Wallet Unit uses the Relying Party identifier and Service identifier in the registration certificate, not the identifiers in the access certificate. This is because if the Relying Party uses the services of an intermediary, the identifiers in the access certificate refer to the intermediary rather than the intermediated Relying Party. The intermediary is not relevant for the purposes of an EDP.*

</div>
</div>

<div class="eudi-hlr" id="EDP_03" markdown>
<div class="eudi-hlr__id">EDP_03<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL support embedded disclosure policies implementing the 'Specific root of trust' policy described in Annex III of Implementing Regulation (EU) 2024/2979 and as specified in [ETSI TS 119 472-3]. If present, such an embedded disclosure policy SHALL contain a list of root or intermediate certificates used for signing Relying Party registration certificates. After receiving a presentation request, the Wallet Unit SHALL compare all certificates in the certificate chain that was used to sign the registration certificate provided by the Relying Party to the list of authorised root or intermediate certificates in the policy for the requested attestation. If none of these certificates are included in this list, the Wallet Unit SHALL consider the evaluation of the embedded disclosure policy to have failed, and inform the User.

*Note: See EDP_02 for why the Wallet Unit uses the certificate chain of the registration certificate rather than the one of the access certificate.*

</div>
</div>

<div class="eudi-hlr" id="EDP_04" markdown>
<div class="eudi-hlr__id">EDP_04</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="EDP_05" markdown>
<div class="eudi-hlr__id">EDP_05<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

An embedded disclosure policy SHOULD contain a link to a website of the Attestation Provider explaining the disclosure policy in layman's terms. If this is the case, the Wallet Unit SHALL display the link to the User and allow them to navigate to that website.

</div>
</div>

<div class="eudi-hlr" id="EDP_06" markdown>
<div class="eudi-hlr__id">EDP_06<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Wallet Unit SHALL evaluate an embedded disclosure policy in conjunction with the information received from the requesting Relying Party in the registration certificate, in order to determine if the Relying Party has permission from the Attestation Provider to access the requested attestation. The Wallet Unit SHALL perform this evaluation in compliance with the evaluation rules established in ETSI TS 119 472-3.

</div>
</div>

<div class="eudi-hlr" id="EDP_07" markdown>
<div class="eudi-hlr__id">EDP_07<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Wallet Unit SHALL enable the User, based on the outcome of the evaluation of the applicable embedded disclosure policy(s), to deny or allow the presentation of the requested attestation to the Relying Party.

</div>
</div>

<div class="eudi-hlr" id="EDP_08" markdown>
<div class="eudi-hlr__id">EDP_08<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The format of an embedded disclosure policy SHALL comply with ETSI TS 119 472-3.

</div>
</div>

<div class="eudi-hlr" id="EDP_09" markdown>
<div class="eudi-hlr__id">EDP_09<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

An Attestation Provider SHALL include an embedded disclosure policy (if any) by value in the Issuer metadata related to the attestation, in compliance with [OpenID4VCI] and [ETSI TS 119 472-3].

</div>
</div>

<div class="eudi-hlr" id="EDP_10" markdown>
<div class="eudi-hlr__id">EDP_10<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

During attestation issuance, a Wallet Unit SHALL retrieve and store the corresponding embedded disclosure policy, if any.

*Note: The intent of this requirement is that the Wallet Unit is able to evaluate an EDP during a presentation transaction, without needing to request it again from the Attestation Provider. This is necessary in particular during proximity presentations, which must be able to be done without an internet connection.*

</div>
</div>

<div class="eudi-hlr" id="EDP_11" markdown>
<div class="eudi-hlr__id">EDP_11<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

An Attestation Provider SHALL revoke an attestation if a corresponding embedded disclosure policy is added, changed, or deleted.

</div>
</div>


[](){ #topic-44 }
