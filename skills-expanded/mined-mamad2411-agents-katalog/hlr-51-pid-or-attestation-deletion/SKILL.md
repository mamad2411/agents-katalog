---
name: "hlr-51-pid-or-attestation-deletion"
description: "Use when working with EUDI high-level requirements for 'PID or attestation deletion'. Contains normative SHALL/SHOULD/MAY requirements from ARF Annex 2."
sections:
  - "A.2.3.29 Topic 51 - PID or attestation deletion"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~745 -->

#### A.2.3.29 Topic 51 - PID or attestation deletion

<div class="eudi-hlr" id="PAD_01" markdown>
<div class="eudi-hlr__id">PAD_01<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL at any time enable the User to delete any PID or attestation from their Wallet Unit.

</div>
</div>

<div class="eudi-hlr" id="PAD_02" markdown>
<div class="eudi-hlr__id">PAD_02<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If the User indicates that a logical PID or attestation must be deleted, and the Wallet Unit contains multiple physical PIDs or attestations corresponding to that logical PID or attestation, a Wallet Unit SHALL delete all of these physical PIDs and attestations simultaneously.

*Note: a) This situation may occur if the PID Provider or Attestation Provider issued a batch of physical PIDs or attestations to the Wallet Unit, rather than a single one. b) Physical PIDs or attestations correspond to a logical one if they have not only the same attestation type and Provider, but also the same attribute values. In principle, the same Provider can issue two attestations of the same type to the same Wallet Unit, for example two diplomas from the same university. This corresponds to the notion of a Credential Dataset in OpenID4VCI.*

</div>
</div>

<div class="eudi-hlr" id="PAD_03" markdown>
<div class="eudi-hlr__id">PAD_03<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If the Wallet Unit deletes a PID or attestation on the User's request, the Wallet Unit SHALL NOT notify the respective PID Provider or Attestation Provider.

*Note: This is a matter of User privacy.*

</div>
</div>

<div class="eudi-hlr" id="PAD_04" markdown>
<div class="eudi-hlr__id">PAD_04<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If the Wallet Unit deletes a PID or device-bound attestation on the User's request, the Wallet Unit SHALL ensure that all cryptographic assets in the WSCA/WSCD or keystores related to this PID or attestation are securely destroyed.

*Note: Key deletion for a PID key is a cryptographic key operation and requires User authentication, as specified in requirement WIAM_14.*

</div>
</div>

<div class="eudi-hlr" id="PAD_05" markdown>
<div class="eudi-hlr__id">PAD_05<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If a Wallet Unit deletes, on the User's request, a PID or attestation previously disclosed to the Digital Credentials API framework, the Wallet Instance SHALL disclose the fact that it no longer stores this PID or attestation to the Digital Credentials API framework.

</div>
</div>

<div class="eudi-hlr" id="PAD_06" markdown>
<div class="eudi-hlr__id">PAD_06</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>


[](){ #topic-52 }
