---
name: "hlr-10-issuing-a-pid-or-attestation-to-a-wallet-part-3"
description: "Use when working with EUDI high-level requirements for 'Issuing a PID or attestation to a Wallet Unit' (Part 3). Contains normative requirements from ARF Annex 2."
sections:
  - "Method D: Per-Relying Party attestations <!-- omit from toc -->"
  - "E - HLRs for re-issuance and batch issuance of PIDs and attestations <!-- omit from toc -->"
  - "F - HLRs for attestation-signing certificate profiles and certificate policies <!-- omit from toc -->"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~3131 -->

##### Method D: Per-Relying Party attestations <!-- omit from toc -->

<div class="eudi-hlr" id="ISSU_55" markdown>
<div class="eudi-hlr__id">ISSU_55<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If Method D is used, the Wallet Unit SHALL present a different technical PID or attestation to each different Relying Party that requests the corresponding logical PID or attestation. This means that it SHALL comply with all requirements for Method A for such Relying Parties.

*Note: This means the Wallet Unit presents an unused technical attestation to each new Relying Party that request the logical attestation, and it requests a new batch of technical attestations if the number of remaining unused attestations goes below the lower limit. If for some reason requesting a new batch is not successful and the Wallet Unit runs out of unused technical attestations, it re-uses one of the already used technical attestations.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_56" markdown>
<div class="eudi-hlr__id">ISSU_56<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If Method D is used and a given Relying Party requests attributes from a given logical PID or attestation multiple times, the Wallet Unit MAY present the same technical PID or attestation to this Relying Party each time. If it does, it SHALL comply with all requirements for Method B for such a Relying Party.

</div>
</div>

<div class="eudi-hlr" id="ISSU_56a" markdown>
<div class="eudi-hlr__id">ISSU_56a</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="ISSU_57" markdown>
<div class="eudi-hlr__id">ISSU_57<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If Method D is used, the Wallet Unit SHALL keep track of which technical PID or attestation it has presented to which Relying Party.

*Note: To do so, the Wallet Unit can use the unique RP identifier contained in the registration certificate of the presentation requests it receives.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_57a" markdown>
<div class="eudi-hlr__id">ISSU_57a</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

##### E - HLRs for re-issuance and batch issuance of PIDs and attestations <!-- omit from toc -->

<div class="eudi-hlr" id="ISSU_58" markdown>
<div class="eudi-hlr__id">ISSU_58<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL give its User the option to manually initiate a re-issuance process for any of the logical PIDs or attestations in their Wallet Unit. If the User uses this option, the Wallet Unit SHALL attempt to start the re-issuance process immediately, and SHALL notify the User if it did not succeed in requesting re-issuance.

*Note: a) This requirement does not apply for KAs or WIAs, since Users must not be involved in their management. b) In the case of a PID or an attestation bound to the WSCA/WSCD, the Wallet Unit will request the User to authenticate to the WSCA/WSCD (see WIAM_14). In case of an attestation bound to a keystore, no additional User authentication is needed, see WIAM_15c.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_59" markdown>
<div class="eudi-hlr__id">ISSU_59<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

After a successful re-issuance, a Wallet Unit SHALL compare the attribute values of the re-issued technical PID or attestation with those of the existing technical PID or attestation, and SHALL notify the User in case of any differences.

*Note: a) This requirement does not apply for KAs or WIAs, since Users must not be involved in their management. b) The point of this requirement is to allow the User to detect errors in the attribute values in the new attestation. The follow-up process in case of errors is not defined. Presumably, the User can contact the Attestation Provider to discuss the fact that it apparently holds false attribute values for the User, and as a result, the Attestation Provider may decide to revoke the attestation.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_60" markdown>
<div class="eudi-hlr__id">ISSU_60<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL gracefully handle situations in which re-issuance of a PID, attestation, KA, or WIA fails or is refused by the PID Provider, Attestation Provider, or Wallet Provider, for example by attempting a retry after an appropriate delay.

</div>
</div>

<div class="eudi-hlr" id="ISSU_61" markdown>
<div class="eudi-hlr__id">ISSU_61<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL support PID or attestation first-time batch issuance with a single User authentication, regardless of the size of the batch.

*Note: See also requirement WIAM_14.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_62" markdown>
<div class="eudi-hlr__id">ISSU_62<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If a technical PID or attestation was successfully re-issued because the value of one or more of its attributes was changed (including attributes being added or deleted), a Wallet Unit SHALL no longer present the (now obsolete) pre-existing technical PID or attestation, and SHOULD delete it.

*Note: a) It is up to the Wallet Unit, possibly using metadata provided by the PID Provider or Attestation Provider using the [OpenID4VCI] protocol, to determine the technical PID or attestation to be deleted. b) Additionally, per requirement VCR_09, the PID Provider or Attestation Provider revokes the pre-existing technical PID or attestation.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_63" markdown>
<div class="eudi-hlr__id">ISSU_63<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

PID Providers and Attestation Providers, and Wallet Units SHALL support the features of [OpenID4VCI] enabling the re-issuance of PIDs and attestations.

</div>
</div>

<div class="eudi-hlr" id="ISSU_64" markdown>
<div class="eudi-hlr__id">ISSU_64<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

PID Providers, Attestation Providers, and Wallet Units SHALL support the features of [OpenID4VCI] enabling the batch issuance of technical PIDs or attestations.

</div>
</div>

<div class="eudi-hlr" id="ISSU_65" markdown>
<div class="eudi-hlr__id">ISSU_65<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A PID Provider or an Attestation Provider of device-bound attestations SHALL verify that a re-issued technical PID or device-bound attestation is issued to the same Wallet Unit as the existing PID or attestation.

*Note: A PID Provider or Attestation Provider can do so by issuing a device-bound refresh token to the Wallet Instance during the original issuance of the PID or attestation, and requiring that the Wallet Instance uses it to obtain a fresh access token during re-issuance. See [OpenID4VCI] section 14.5. The PID Provider or Attestation Provider needs to be able to trust that the Wallet Instance handles the refresh tokens in a secure way, so that an attacker cannot use them from another Wallet Instance. This requires trust in the (continued) security and integrity of both the original Wallet Instance and the other Wallet Instance. This trust is provided by providing the PID Provider or Attestation Provider with a valid KA for the new Wallet Unit during re-issuance, and by enabling the PID Provider or Attestation Provider to verify that the original Wallet Unit has not been revoked.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_66" markdown>
<div class="eudi-hlr__id">ISSU_66</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

##### F - HLRs for attestation-signing certificate profiles and certificate policies <!-- omit from toc -->

<div class="eudi-hlr" id="ISSU_67" markdown>
<div class="eudi-hlr__id">ISSU_67<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A PID Provider SHALL have a policy governing all aspects of PID issuance and management, in line with clauses 6 and 7 of [ETSI TS 119 471], incorporating the amendments introduced by [CIR 2025/1569] and subject to the necessary adaptations to a PID. The policy SHALL comply with at least the extended normalised certificate policy ('NCP+') requirements as specified in [ETSI EN 319 411-1], insofar applicable for the issuance of PIDs rather than public key certificates.

*Note: A common dedicated policy for issuing PIDs may be developed in the future. If so, this requirement will be changed to refer to it.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_68" markdown>
<div class="eudi-hlr__id">ISSU_68<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

PID Providers SHALL ensure that the certificates they use for signing PIDs comply with all applicable requirements in [ETSI TS 119 412-6], in particular Clause 4.

</div>
</div>

<div class="eudi-hlr" id="ISSU_69" markdown>
<div class="eudi-hlr__id">ISSU_69<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A QEAA Provider SHALL have a policy governing all aspects of QEAA issuance and management, in line with clauses 6 and 7 of [ETSI TS 119 471], incorporating the amendments introduced by [CIR 2025/1569]. The policy SHALL comply with at least the policy for qualified certificates issued to a natural person where the private key and the related certificate reside on a QSCD ('QCP-n-qscd') or qualified certificates issued to a legal person where the private key and the related certificate reside on a QSCD ('QCP-l-qscd') requirements as specified in [ETSI EN 319 411-2], insofar applicable for the issuance of QEAAs rather than public key certificates.

*Note: A common dedicated policy for issuing QEAAs may be developed in the future. If so, this requirement will be changed to refer to it.*

</div>
</div>

<div class="eudi-hlr" id="ISSU_70" markdown>
<div class="eudi-hlr__id">ISSU_70<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

QEAA Providers SHALL ensure that the certificates they use for signing QEAAs comply with all applicable requirements in [ETSI TS 119 412-6], in particular Clause 7.

</div>
</div>

<div class="eudi-hlr" id="ISSU_71" markdown>
<div class="eudi-hlr__id">ISSU_71<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Providers of non-qualified EAAs SHALL ensure that the certificates they use for signing EAAs comply with all applicable requirements in [ETSI TS 119 412-6], in particular Clause 6.

</div>
</div>

<div class="eudi-hlr" id="ISSU_72" markdown>
<div class="eudi-hlr__id">ISSU_72<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A PuB-EAA Provider SHALL have a policy governing all aspects of PuB-EAA issuance and management, in line with clauses 6 and 7 of [ETSI TS 119 471], incorporating the amendments introduced by [CIR 2025/1569] and subject to the necessary adaptations to a PuB-EAA. The policy SHALL comply with at least the extended normalised certificate policy ('NCP+') requirements as specified in [ETSI EN 319 411-1], insofar applicable for the issuance of PuB-EAAs rather than public key certificates.

*Note: A common dedicated policy for issuing PuB-EAAs may be developed in the future. If so, this requirement will be changed to refer to it*

</div>
</div>

<div class="eudi-hlr" id="ISSU_73" markdown>
<div class="eudi-hlr__id">ISSU_73<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

PuB-EAAs Providers SHALL ensure that the certificates they use for signing PuB-EAAs comply with all applicable requirements in [ETSI TS 119 412-6], in particular Clause 8.

</div>
</div>


[](){ #topic-11 }
