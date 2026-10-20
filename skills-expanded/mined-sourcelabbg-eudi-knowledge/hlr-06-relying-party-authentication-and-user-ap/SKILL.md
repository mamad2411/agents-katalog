---
name: "hlr-06-relying-party-authentication-and-user-ap"
description: "Use when working with EUDI high-level requirements for 'Relying Party authentication and User approval'. Contains normative SHALL/SHOULD/MAY requirements from ARF Annex 2."
sections:
  - "A.2.3.4 Topic 6 - Relying Party authentication and User approval"
  - "A. Relying Party authentication <!-- omit from toc -->"
  - "B. User approval <!-- omit from toc -->"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~2624 -->

#### A.2.3.4 Topic 6 - Relying Party authentication and User approval

##### A. Relying Party authentication <!-- omit from toc -->

<div class="eudi-hlr" id="RPA_01" markdown>
<div class="eudi-hlr__id">RPA_01<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Wallet Unit used by a User, as well as the Relying Party Instance used by the Relying Party, SHALL implement a mechanism for Relying Party authentication in PID or attestation presentation transactions. This mechanism SHALL: - enable the Wallet Unit to identify and authenticate the Relying Party, - enable the Wallet Unit to verify that the request from the Relying Party was not copied and replayed, - use an access certificate issued in accordance with [Topic 27][topic-27]].

*Note: Wallet Units and Relying Parties comply with this requirement if they comply with the requirements in this Topic.*

</div>
</div>

<div class="eudi-hlr" id="RPA_01a" markdown>
<div class="eudi-hlr__id">RPA_01a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL retain full authority over the process meant in RPA_01. In particular, this process SHALL NOT be handled by a third party, including the browser and the operating system.

*Note: This requirement applies, in particular, in the context of the [W3C Digital Credentials API].*

</div>
</div>

<div class="eudi-hlr" id="RPA_02" markdown>
<div class="eudi-hlr__id">RPA_02<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For performing Relying Party authentication, Wallet Units and Relying Party Instances SHALL support access certificates as specified in [ETSI TS 119 475] and [ETSI TS 119 411-8].

*Note: In [ISO/IEC 18013-5], the Relying Party authentication mechanism is called mdoc reader authentication and uses an X.509 certificate. For [OpenID4VP], [HAIP] specifies that Client Identifier Prefix `x509_hash` must be used to authenticate the Relying Party. This mechanism also uses an X.509 certificate.*

</div>
</div>

<div class="eudi-hlr" id="RPA_02a" markdown>
<div class="eudi-hlr__id">RPA_02a</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="RPA_03" markdown>
<div class="eudi-hlr__id">RPA_03<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit and a Relying Party Instance SHALL perform Relying Party authentication in all PID or attestation presentation transactions to Relying Parties, whether proximity or remote, using an access certificate.

*Note: The actions both entities perform differ. For example, while the Relying Party creates a signature over some data in the request, the Wallet Unit validates that signature.*

</div>
</div>

<div class="eudi-hlr" id="RPA_04" markdown>
<div class="eudi-hlr__id">RPA_04<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For the verification of access certificates, a Wallet Unit SHALL accept only the trust anchors in the LoTE(s) of all Access Certificate Authorities notified by Member States.

*Note: For more information about Access Certificate Authorities, please see [Topic 31][topic-31]].*

</div>
</div>

<div class="eudi-hlr" id="RPA_05" markdown>
<div class="eudi-hlr__id">RPA_05<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If Relying Party authentication fails for any reason, the Wallet Instance SHALL inform the User that the identity of the Relying Party could not be verified and that therefore the request is not trustworthy.

</div>
</div>

<div class="eudi-hlr" id="RPA_06" markdown>
<div class="eudi-hlr__id">RPA_06<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If Relying Party authentication succeeds, the Wallet Instance SHALL display to the User the trade names of the Relying Party and its Service, as included in the access certificate received from the Relying Party Instance, together with the attributes requested by the Relying Party. The Wallet Instance SHALL do so when asking the User for approval according to RPA_07.

*Note: a) A Relying Party Instance may be used for multiple Relying Party Services, provided it has received a separate access certificate for each, see Reg_10a. b) If the authenticated Relying Party is an intermediary acting on behalf of an intermediated Relying Party, the Wallet Instance does not display the trade names of the intermediary and its Service, but only those of the intermediated Relying Party; see RPI_07.*

</div>
</div>

<div class="eudi-hlr" id="RPA_06a" markdown>
<div class="eudi-hlr__id">RPA_06a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If Relying Party authentication fails for any reason, the Wallet Unit SHALL notify the User. In addition, the Wallet Unit SHALL either not present the requested attributes to the Relying Party, or give the User the choice to present the requested attributes or not.

*Note: It is up to the Wallet Provider to make a choice for one of these two options.*

</div>
</div>


##### B. User approval <!-- omit from toc -->

<div class="eudi-hlr" id="RPA_07" markdown>
<div class="eudi-hlr__id">RPA_07<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL ensure the User approved the presentation of any attribute(s) in the Wallet Unit to a Relying Party or Verifier Wallet Unit, prior to presenting these attributes. A Wallet Unit SHALL always allow the User to refuse presenting an attribute requested by the Relying Party or Verifier Wallet Unit.

</div>
</div>

<div class="eudi-hlr" id="RPA_07a" markdown>
<div class="eudi-hlr__id">RPA_07a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL retain full authority over the process meant in RPA_07, RPA_07b, and RPA_07c. In particular, this process SHALL NOT be handled by a third party, including the browser and the operating system.

*Note: This requirement applies, in particular, in the context of the [W3C Digital Credentials API].*

</div>
</div>

<div class="eudi-hlr" id="RPA_07b" markdown>
<div class="eudi-hlr__id">RPA_07b<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

In addition to RPA_07, in case the Wallet Unit warns the User about failed verifications regarding the Relying Party's access certificate or registration certificate, the Wallet Unit SHALL ensure that User approval is explicit. Silence or pre-ticked boxes SHALL NOT suffice.

</div>
</div>

<div class="eudi-hlr" id="RPA_07c" markdown>
<div class="eudi-hlr__id">RPA_07c<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

In addition to RPA_07, in case a Relying Party requests the presentation of the portrait in a PID (see PID Rulebook), the Wallet Unit SHALL warn the User that the request involves the presentation of biometric data. The Wallet Unit SHALL ensure that User approval for presenting the portrait is explicit. Silence or a pre-ticked box SHALL NOT suffice.

</div>
</div>

<div class="eudi-hlr" id="RPA_08" markdown>
<div class="eudi-hlr__id">RPA_08<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL authenticate the User before allowing the User to give or refuse approval for releasing any attributes, in accordance with WIAM_14 or WIAM_15, as applicable.

</div>
</div>

<div class="eudi-hlr" id="RPA_09" markdown>
<div class="eudi-hlr__id">RPA_09</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="RPA_10" markdown>
<div class="eudi-hlr__id">RPA_10<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

When asking for User approval, the Wallet Unit SHALL show to the User the User-friendly description of the Relying Party's intended use and the link to the applicable privacy policy.

*Note: The User-friendly description of the Relying Party's intended use is included in the registration certificate. The link to the privacy policy is also included in the registration certificate. See [Topic 44][topic-44] for details.*

</div>
</div>

<div class="eudi-hlr" id="RPA_10a" markdown>
<div class="eudi-hlr__id">RPA_10a<span class="kw-should">SHOULD</span></div>
<div class="eudi-hlr__body" markdown>

The Wallet Unit SHOULD ensure that the User gives approval either to present all attributes requested in a presentation request, or none of them.

*Note: This means that a User should be asked either to approve the presentation of all requested attributes or to deny all of them. The Wallet Unit should not allow partial approval, since this would mean that the Relying Party cannot deliver the service, but nevertheless receives some User attributes. This would be a violation of the User's privacy. Note that a Relying Party is not allowed to request more data than is justified for the intended use. So if the User feels that the Relying Party is actually requesting more data than needed, that implies that the Relying Party is not trustworthy and should not receive any data.*

</div>
</div>

<div class="eudi-hlr" id="RPA_11" markdown>
<div class="eudi-hlr__id">RPA_11<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

When the presentation of an attestation or a PID is denied by the User, the Wallet Unit SHALL behave towards the Relying Party as if the attestation or PID did not exist.

</div>
</div>

<div class="eudi-hlr" id="RPA_12" markdown>
<div class="eudi-hlr__id">RPA_12<span class="kw-may">MAY</span></div>
<div class="eudi-hlr__body" markdown>

When asking for User approval, the Wallet Unit MAY indicate to the User whether the attestation requested by a Relying Party is device-bound or not.

*Note: The intent of this indication is to warn the User that a non-device-bound attestation may be copied by the Relying Party and presented to a third party.*

</div>
</div>


[](){ #topic-7 }
