---
name: "hlr-53-zero-knowledge-proofs"
description: "Use when working with EUDI high-level requirements for 'Zero-Knowledge Proofs'. Contains normative SHALL/SHOULD/MAY requirements from ARF Annex 2."
sections:
  - "A.2.3.31 Topic 53 - Zero-Knowledge Proofs"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~1313 -->

#### A.2.3.31 Topic 53 - Zero-Knowledge Proofs

<div class="eudi-hlr" id="ZKP_01" markdown>
<div class="eudi-hlr__id">ZKP_01<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A ZKP scheme SHALL provide support for the following generic functions, while hiding all attributes of PIDs or attestations: (i) generation of a proof that an (some) attribute(s) having a specific value is (are) included in a PID or attestation, (ii) generation of a proof that a PID or attestation is within its validity period, (iii) generation of a proof that a PID or attestation has not been revoked, and (iv) generation of a proof that a PID or device-bound attestation is bound to a key stored in the WSCA/WSCD or in a keystore of the Wallet Unit. Additionally, a ZKP scheme SHOULD provide support for the following function, which SHOULD be used only when hiding the PID Provider or Attestation Provider is necessary: (v) generation of a proof that a PID or attestation has been issued by a trusted PID Provider or Attestation Provider, without revealing the PID Provider or Attestation Provider.

*Note: See section 4.1.1 of the Discussion Paper for Topic G.*

</div>
</div>

<div class="eudi-hlr" id="ZKP_02" markdown>
<div class="eudi-hlr__id">ZKP_02<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A ZKP scheme SHALL support proving possession of attestation of a given type.

*Note: See section 4.1.2 and 4.1.3 of the Discussion Paper for Topic G.*

</div>
</div>

<div class="eudi-hlr" id="ZKP_03" markdown>
<div class="eudi-hlr__id">ZKP_03<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A ZKP scheme SHOULD support the privacy-preserving binding of an attestation to a PID. In addition to the generic functions defined in ZKP_01, for this use case, a ZKP scheme SHALL provide support for the following functions: (i) generation of a proof that the Wallet Unit stores an attestation and a PID and that the attestation includes a specific attribute, having a specific value, which is also present in the PID.

*Note: See section 4.1.4 of the Discussion Paper for Topic G.*

</div>
</div>

<div class="eudi-hlr" id="ZKP_04" markdown>
<div class="eudi-hlr__id">ZKP_04<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A ZKP scheme SHOULD support the derivation of a verifiable User pseudonym, by combining an attribute value that is unique for the User with Relying Party-specific context (e.g., the Relying Party identifier) In addition to the generic functions defined in ZKP_01, for this use case, a ZKP scheme SHALL provide support for the following functions: (i) generation of a request for the issuance of an attestation that includes a secret attribute unique to the User, without revealing this attribute to the Attestation Provider, (ii) generation of an attestation presentation that includes a verifiable pseudonym derived from the secret attribute, a Relying Party identifier, and context-related information.

*Note: See section 4.1.5 of the Discussion Paper for Topic G.*

</div>
</div>

<div class="eudi-hlr" id="ZKP_05" markdown>
<div class="eudi-hlr__id">ZKP_05<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A ZKP scheme SHALL be usable in both remote and proximity presentation flows. While the inclusion of ZKP will introduce computational and verification delays, these delays SHALL NOT critically undermine or defeat the purpose of the Relying Party service (e.g. because of a critical impact on the User experience of the Wallet Unit).

</div>
</div>

<div class="eudi-hlr" id="ZKP_06" markdown>
<div class="eudi-hlr__id">ZKP_06<span class="kw-should">SHOULD</span></div>
<div class="eudi-hlr__body" markdown>

A ZKP scheme SHOULD be able to generate proofs for already issued PIDs and attestations in the formats specified in [ISO/IEC 18013-5] or [SD-JWT VC].

</div>
</div>

<div class="eudi-hlr" id="ZKP_07" markdown>
<div class="eudi-hlr__id">ZKP_07<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A ZKP scheme SHALL NOT introduce any additional communication or information that could be used to track or link User activity during, before, or after proof generation.

</div>
</div>

<div class="eudi-hlr" id="ZKP_08" markdown>
<div class="eudi-hlr__id">ZKP_08<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A ZKP scheme SHALL rely solely on algorithms included in the [ECCG Agreed Cryptographic Mechanisms v2.0].

</div>
</div>

<div class="eudi-hlr" id="ZKP_09" markdown>
<div class="eudi-hlr__id">ZKP_09<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Use of a ZKP scheme SHALL NOT prevent the Wallet Unit's ability to provide User authentication with Level of Assurance High.

</div>
</div>


[](){ #topic-54 }
