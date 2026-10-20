---
name: "hlr-20-strong-user-authentication-for-electroni"
description: "Use when working with EUDI high-level requirements for 'Strong User authentication for electronic payments'. Contains normative SHALL/SHOULD/MAY requirements from ARF Annex 2."
sections:
  - "A.2.3.13 Topic 20 - Strong User authentication for electronic payments"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~1365 -->

#### A.2.3.13 Topic 20 - Strong User authentication for electronic payments

<div class="eudi-hlr" id="SUA_01" markdown>
<div class="eudi-hlr__id">SUA_01<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL be able to process the transactional data included in a presentation request for the SUA attestation(s) specified in [Technical Specification 12](../../technical-specifications/ts12-electronic-payments-SCA-implementation-with-wallet.md), according to all requirements in that Technical Specification.

*Note: Technical Specification 12 specifies a SUA attestation intended for performing SCA as specified in the PSD2 Regulation. The related Rulebook is called "SCA Attestation Rulebook".*

</div>
</div>

<div class="eudi-hlr" id="SUA_02" markdown>
<div class="eudi-hlr__id">SUA_02<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Scheme Providers MAY specify Attestation Rulebooks (see [Topic 12][topic-12]) and associated technical specifications for SUA attestations other that the ones specified in [Technical Specification 12](../../technical-specifications/ts12-electronic-payments-SCA-implementation-with-wallet.md)). The Attestation Rulebook or the technical specification of such of a SUA attestation SHALL specify the syntax and semantics of the transactional data associated with that attestation.

</div>
</div>

<div class="eudi-hlr" id="SUA_02a" markdown>
<div class="eudi-hlr__id">SUA_02a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Technical Specification associated with a given SUA attestation SHALL specify all necessary requirements for Wallet Units to process transactional data intended for this SUA attestation, at least regarding a) rendering and displaying the data to the User when obtaining approval for presentation, b) processing (e.g., hashing) the data for inclusion in the device binding signature, and c) the scope of information to be logged about a SUA attestation presentation transaction by a Wallet Unit.

</div>
</div>

<div class="eudi-hlr" id="SUA_03" markdown>
<div class="eudi-hlr__id">SUA_03<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Attestation Provider of a SUA attestation other than the one(s) specified in [Technical Specification 12](../../technical-specifications/ts12-electronic-payments-SCA-implementation-with-wallet.md) SHALL NOT issue such an attestation to a Wallet Unit that does not comply with all relevant requirements in the SUA Attestation Rulebook and the technical specification for that attestation.

</div>
</div>

<div class="eudi-hlr" id="SUA_04" markdown>
<div class="eudi-hlr__id">SUA_04<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

In the response to a presentation request for a SUA attestation that includes transactional data, a Wallet Unit SHALL include (a representation of) that data, according to requirements included in the associated technical specification or Attestation Rulebook or in information provided to the Wallet Unit in the presentation request. In the latter case, the rules to interpret such information SHALL be included in the associated technical specification or Attestation Rulebook.

*Note: This requirement, as well as SUA_05, only applies if the requested SUA attestation is present on the Wallet Unit and if the User consents to signing the transactional data and presenting the requested attributes.*

</div>
</div>

<div class="eudi-hlr" id="SUA_05" markdown>
<div class="eudi-hlr__id">SUA_05<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Wallet Unit SHALL include (a representation of) the transactional data received in a presentation request in the signature creation process used for device binding, using the private key of the requested SUA attestation and the mechanisms specified for key binding in [SD-JWT VC] or mdoc authentication in [ISO/IEC 18013-5], as applicable. For this process, the Wallet Unit SHALL comply with the applicable requirements in the technical specification and the Attestation Rulebook for the requested SUA attestation, see SUA_01 or SUA_02.

*Note: a) The resulting signature value constitutes a proof of transaction. This signature value, possibly in combination with other protocols items, fulfils the requirements for the authentication code required in [PSD2]. b) See also requirement OIA_02 in [Topic 1][topic-1].*

</div>
</div>

<div class="eudi-hlr" id="SUA_06" markdown>
<div class="eudi-hlr__id">SUA_06<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Wallet Unit SHALL render or adapt the dialogue message(s) displayed to the User (like font size and colour, background colour, text position, labels in the buttons to 'approve' or 'reject' a transaction), according to requirements in [Technical Specification 12](../../technical-specifications/ts12-electronic-payments-SCA-implementation-with-wallet.md).

</div>
</div>

<div class="eudi-hlr" id="SUA_07" markdown>
<div class="eudi-hlr__id">SUA_07<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Upon receiving a presentation request with transactional data, the Wallet Unit SHALL validate if the transactional data is intended for the given attestation and that the transactional data conforms to the related technical specification and/or Attestation Rulebook. In case the validation result is positive, the Wallet Unit SHALL process the transactional data in compliance with the related technical specification.

</div>
</div>


[](){ #topic-24 }
