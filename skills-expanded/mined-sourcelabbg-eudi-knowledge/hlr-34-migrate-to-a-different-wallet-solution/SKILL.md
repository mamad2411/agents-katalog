---
name: "hlr-34-migrate-to-a-different-wallet-solution"
description: "Use when working with EUDI high-level requirements for 'Migrate to a different Wallet Solution'. Contains normative SHALL/SHOULD/MAY requirements from ARF Annex 2."
sections:
  - "A.2.3.21 Topic 34 - Migrate to a different Wallet Solution"
  - "A. Back-up requirements <!-- omit from toc -->"
  - "B. Restore Requirements <!-- omit from toc -->"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~2195 -->

#### A.2.3.21 Topic 34 - Migrate to a different Wallet Solution

##### A. Back-up requirements <!-- omit from toc -->

<div class="eudi-hlr" id="Mig_01" markdown>
<div class="eudi-hlr__id">Mig_01<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL include and keep up-to-date a Migration Object, containing the following information: - The contents of the log for all transactions executed through the Wallet Unit, as listed in requirement DASH_02. - A list of PIDs and attestations (except Key Attestations and Wallet Instance Attestations) present in the Wallet Unit, according to the requirements in this Topic.

</div>
</div>

<div class="eudi-hlr" id="Mig_02" markdown>
<div class="eudi-hlr__id">Mig_02<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Migration Object SHALL comply with all requirements in [Technical Specification 10](../../technical-specifications/ts10-data-portability-and-download-(export).md).

</div>
</div>

<div class="eudi-hlr" id="Mig_03" markdown>
<div class="eudi-hlr__id">Mig_03<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For each PID or device-bound attestation that is issued to it, a Wallet Unit SHALL add to the Migration Object all data necessary to request issuance of that PID or attestation once again. This SHALL include at least the attestation type and the PID Provider or Attestation Provider that issued the PID or attestation, as well as their service supply points. However, the Migration Object SHALL NOT contain attribute identifiers or attribute values, and SHALL NOT contain any private keys of the PID or device-bound attestation.

</div>
</div>

<div class="eudi-hlr" id="Mig_03a" markdown>
<div class="eudi-hlr__id">Mig_03a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For each non-device-bound attestation that is issued to it, a Wallet Unit SHALL add to the Migration Object one of the following: either all data necessary to request issuance of that attestation once again, as listed in Mig_03, or all data necessary to transfer the attestation to a new device without involvement of the Attestation Provider, including attribute identifiers and attribute values. The Wallet Unit SHALL enable the User to indicate if they want to store attribute identifiers and values in the Migration Object.

</div>
</div>

<div class="eudi-hlr" id="Mig_03b" markdown>
<div class="eudi-hlr__id">Mig_03b<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If the User deletes a PID or attestation from their Wallet Unit, the Wallet Unit SHALL delete the corresponding entry from the Migration Object.

</div>
</div>

<div class="eudi-hlr" id="Mig_04" markdown>
<div class="eudi-hlr__id">Mig_04<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Wallet Unit SHALL store the Migration Object in an external storage or remote storage location of the User's choice, from among the storage options supported by the Wallet Unit, in such a way that the User can still retrieve the object from a new Wallet Unit in case the existing Wallet Unit becomes unavailable.

*Note: a) It is up to the Wallet Provider to decide which external storage options or remote storage locations the Wallet Unit supports for storing the Migration Object. b) The new Wallet Unit may be either an instance of the same Wallet Solution as the old one, or an instance of a different Wallet Solution.*

</div>
</div>

<div class="eudi-hlr" id="Mig_05" markdown>
<div class="eudi-hlr__id">Mig_05<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Wallet Unit SHALL store the Migration Object in such a way that its confidentiality, integrity, and authenticity is protected and that it is protected against use by others than the User.

*Note: This could be done, for example, by using password-based cryptography to encrypt the object.*

</div>
</div>


##### B. Restore Requirements <!-- omit from toc -->

<div class="eudi-hlr" id="Mig_06" markdown>
<div class="eudi-hlr__id">Mig_06<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Directly after installation of a new Wallet Instance, the Wallet Instance SHALL enable the User to import a Migration Object from an external storage or remote storage location indicated by the User, from among the storage options supported by the Wallet Unit.

</div>
</div>

<div class="eudi-hlr" id="Mig_07" markdown>
<div class="eudi-hlr__id">Mig_07<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

When importing a Migration Object, for each PID and device-bound attestation listed in the Migration Object, the Wallet Unit SHALL enable the User to select that PID or attestation. When a PID or device-bound attestation is selected, the Wallet Unit SHALL request the respective PID Provider or Attestation Provider to issue a new PID or attestation of the same type to the new Wallet Unit. If the User selects a PID, the Wallet Unit SHALL request issuance of the PID first, before any of the other selected attestations.

*Note: a) Since no refresh tokens (see ISSU_65) will be available on the new Wallet Unit, this is a new issuance process, which will include User authentication by the PID Provider or Attestation Provider. b) The rationale for the last requirement is to ensure that if other Attestation Providers want to use a PID to do User authentication, the PID is actually available.*

</div>
</div>

<div class="eudi-hlr" id="Mig_07a" markdown>
<div class="eudi-hlr__id">Mig_07a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

When importing a Migration Object, for each non-device-bound attestation listed in the Migration Object, the Wallet Unit SHALL enable the User to select that attestation. When an attestation is selected, the Wallet Unit SHALL, depending on whether the Migration Object contains attribute identifiers and attribute values (see Mig_03a), either restore the technical attestation directly from the Object or request the respective Attestation Provider to issue a new attestation of the same type to the new Wallet Unit.

</div>
</div>

<div class="eudi-hlr" id="Mig_07b" markdown>
<div class="eudi-hlr__id">Mig_07b<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

When importing a Migration Object, the Wallet Unit SHALL ask the User whether they want to restore the log from the Migration Object. When the User agrees, the Wallet Unit SHALL restore the log, and SHALL append future transactions to this log according to the requirements in [Topic 19][topic-19].

</div>
</div>

<div class="eudi-hlr" id="Mig_08" markdown>
<div class="eudi-hlr__id">Mig_08</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="Mig_09" markdown>
<div class="eudi-hlr__id">Mig_09</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="Mig_10" markdown>
<div class="eudi-hlr__id">Mig_10</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="Mig_11" markdown>
<div class="eudi-hlr__id">Mig_11<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The processes and interfaces used for issuance of a PID or attestation as part of a migration process SHALL be the same as those used for a 'normal' issuance process, as specified in [Topic 10][topic-10].

</div>
</div>

<div class="eudi-hlr" id="Mig_12" markdown>
<div class="eudi-hlr__id">Mig_12</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="Mig_13" markdown>
<div class="eudi-hlr__id">Mig_13</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="Mig_14" markdown>
<div class="eudi-hlr__id">Mig_14</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="Mig_15" markdown>
<div class="eudi-hlr__id">Mig_15</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="Mig_16" markdown>
<div class="eudi-hlr__id">Mig_16</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>


[](){ #topic-38 }
