---
name: "hlr-18-combined-presentations-of-attributes"
description: "Use when working with EUDI high-level requirements for 'Combined presentations of attributes'. Contains normative SHALL/SHOULD/MAY requirements from ARF Annex 2."
sections:
  - "A.2.3.11 Topic 18 - Combined presentations of attributes"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~863 -->

#### A.2.3.11 Topic 18 - Combined presentations of attributes

<div class="eudi-hlr" id="ACP_01" markdown>
<div class="eudi-hlr__id">ACP_01<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Cryptographic Binding of Attestations scheme SHALL enable a WSCA/WSCD or keystore to prove that it manages two or more private keys, paired with two or more public keys provided to it by the Wallet Unit.

*Note: a)These public keys may be included in WIAs and KAs, PIDs, attestations, or pseudonyms. b) The proof may be transitive, so a proof that two keys are stored/managed in the same WSCA/WSCD or keystore may be done by proving these keys relate to each other via a third key (also stored in the WSCA/WSCD or keystore).*

</div>
</div>

<div class="eudi-hlr" id="ACP_02" markdown>
<div class="eudi-hlr__id">ACP_02<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Cryptographic Binding of Attestations scheme SHALL rely solely on algorithms included in the [ECCG Agreed Cryptographic Mechanisms v2.0].

</div>
</div>

<div class="eudi-hlr" id="ACP_03" markdown>
<div class="eudi-hlr__id">ACP_03<span class="kw-should">SHOULD</span></div>
<div class="eudi-hlr__body" markdown>

A Cryptographic Binding of Attestations scheme SHOULD be implemented using a Zero-Knowledge Proof mechanism that satisfies the requirements specified in [Topic 53][topic-53].

</div>
</div>

<div class="eudi-hlr" id="ACP_04" markdown>
<div class="eudi-hlr__id">ACP_04<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Cryptographic Binding of Attestations scheme SHALL be compatible with the requirements for attestation issuance in this document, in particular [Topic 10][topic-10], as well as with requirements for both remote and proximity presentation flows in this document, in particular [Topic 1][topic-1] and [Topic 24][topic-24].

</div>
</div>

<div class="eudi-hlr" id="ACP_05" markdown>
<div class="eudi-hlr__id">ACP_05<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Cryptographic Binding of Attestations scheme SHALL enable an Attestation Provider, during the issuance of an attestation, to request and obtain proof that the private key for the new attestation is managed by the same WSCA/WSCD or keystore as the private key of a PID or another attestation already existing on the Wallet Unit.

*Note: ACP_05 and ACP_06 may require an addition to the common OpenID4VCI protocol referenced in requirement ISSU_01, or an extension or profile thereof.*

</div>
</div>

<div class="eudi-hlr" id="ACP_06" markdown>
<div class="eudi-hlr__id">ACP_06</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="ACP_07" markdown>
<div class="eudi-hlr__id">ACP_07<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Before making a request according to ACP_05, an Attestation Provider SHALL verify that the new attestation indeed belongs to the User of the existing PID or attestation.

</div>
</div>


[](){ #topic-19 }
