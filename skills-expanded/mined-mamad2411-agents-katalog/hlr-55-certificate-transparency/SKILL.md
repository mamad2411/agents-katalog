---
name: "hlr-55-certificate-transparency"
description: "Use when working with EUDI high-level requirements for 'Certificate Transparency'. Contains normative SHALL/SHOULD/MAY requirements from ARF Annex 2."
sections:
  - "A.2.3.33 Topic 55 - Certificate Transparency"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~585 -->

#### A.2.3.33 Topic 55 - Certificate Transparency

<div class="eudi-hlr" id="CT_01" markdown>
<div class="eudi-hlr__id">CT_01<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

An Access CA issuing access certificates SHALL register these in a CT log according to RFC 9162, if such a log is available for access certificates.

</div>
</div>

<div class="eudi-hlr" id="CT_02" markdown>
<div class="eudi-hlr__id">CT_02<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

An Access CA issuing access certificates SHALL describe in its CPS how it logs all access certificates.

</div>
</div>

<div class="eudi-hlr" id="CT_03" markdown>
<div class="eudi-hlr__id">CT_03<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

In case a CT log provider for access certificates is available, all Access CAs SHALL act as monitors in the CT ecosystem. Access CAs SHOULD still monitor the CT logs in situations of temporary unavailability.

</div>
</div>

<div class="eudi-hlr" id="CT_04" markdown>
<div class="eudi-hlr__id">CT_04<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

An Access CA SHALL include at least one Signed Certificate Timestamp (SCT) in each access certificate.

</div>
</div>

<div class="eudi-hlr" id="CT_05" markdown>
<div class="eudi-hlr__id">CT_05<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

When verifying an access certificate during PID or attestation issuance or presentation, a Wallet Unit SHALL also verify that the access certificate includes at least one valid Signed Certificate Timestamp (SCT).

</div>
</div>

<div class="eudi-hlr" id="CT_06" markdown>
<div class="eudi-hlr__id">CT_06<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If an access certificate does not include a valid SCT, a Wallet Unit SHALL handle this as a failure or Relying Party authentication, in compliance with all requirements in [Topic 6][topic-6]] and in particular requirement RPA_06a.

</div>
</div>


[](){ #topic-56 }
