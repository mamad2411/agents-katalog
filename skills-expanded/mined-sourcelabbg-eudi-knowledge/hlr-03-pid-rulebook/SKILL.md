---
name: "hlr-03-pid-rulebook"
description: "Use when working with EUDI high-level requirements for 'PID Rulebook'. Contains normative SHALL/SHOULD/MAY requirements from ARF Annex 2."
sections:
  - "A.2.3.2 Topic 3 - PID Rulebook"
  - "A. Generic HLRs <!-- omit from toc -->"
  - "B. HLRs for ISO/IEC 18013-5-compliant PIDs <!-- omit from toc -->"
  - "C. HLRs for SD-JWT VC-compliant PIDs <!-- omit from toc -->"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~3832 -->

#### A.2.3.2 Topic 3 - PID Rulebook

##### A. Generic HLRs <!-- omit from toc -->

<div class="eudi-hlr" id="PID_01" markdown>
<div class="eudi-hlr__id">PID_01<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

PIDs and PID Providers SHALL comply with all requirements in [PID Rulebook][pid-rulebook].

</div>
</div>

<div class="eudi-hlr" id="PID_02" markdown>
<div class="eudi-hlr__id">PID_02<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A PID Provider SHALL issue any PID in both the format specified in ISO/IEC 18013-5 [ISO/IEC 18013-5] and the format specified in [SD-JWT VC].

</div>
</div>

<div class="eudi-hlr" id="PID_03" markdown>
<div class="eudi-hlr__id">PID_03<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

During issuance of a PID, the PID Provider MAY enable the User to opt out from receiving a portrait attribute in their PID. If the User opts out, the PID Provider SHALL include the `portrait` attribute in the PID as an empty JSON `string` or CBOR `bstr`, as applicable given the format of the PID.

*Note: As described in the PID Rulebook and in the Regulation amending [CIR 2024/2977], inclusion of the `portrait` attribute in the PID is mandatory only from 24 months after the entry into force of that Regulation. *

</div>
</div>

<div class="eudi-hlr" id="PID_03a" markdown>
<div class="eudi-hlr__id">PID_03a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If a Relying Party obtains the `portrait` attribute from a User's PID, it SHALL NOT retain the portrait, unless its processing is necessary for the purposes of identification and authentication in compliance with Union data protection law or where this is provided for by Union or national law, in compliance with Union data protection law. The Relying Party SHALL NOT transfer the portrait to third countries or international organisations unless permitted by Union data protection law.

*Note: See [CIR 2024/2977].*

</div>
</div>


##### B. HLRs for ISO/IEC 18013-5-compliant PIDs <!-- omit from toc -->

<div class="eudi-hlr" id="PID_04" markdown>
<div class="eudi-hlr__id">PID_04<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

PID Providers SHALL use "eu.europa.ec.eudi.pid.1" as the attestation type for ISO/IEC 18013-5-compliant PIDs.

*Note: a) This identifier uses the general format [Reverse Domain].[Domain Specific Extension]. Since the European Commission controls the domain ec.europa.eu, this attestation type identifier will not collide with any attestation type identifiers defined by other organisations in other Attestation Rulebooks. b) The version number 1 in this identifier is used to distinguish between the first version of the PID, defined in the [PID Rulebook](../annex-3/annex-3.01-pid-rulebook.md), and any future version, which will then have an incremented version number.*

</div>
</div>

<div class="eudi-hlr" id="PID_05" markdown>
<div class="eudi-hlr__id">PID_05<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

When issuing a PID compliant with [ISO/IEC 18013-5], a PID Provider SHALL use the value "eu.europa.ec.eudi.pid.1" for the identifier of the namespace for the PID attributes specified in [Section 4.2 of the PID Rulebook](../annex-3/annex-3.01-pid-rulebook.md).

*Note: a) The version number 1 allows for future extension(s) or change(s) of the ISO/IEC 18013-5-compliant PID attributes. b) This namespace has the same value as the attestation type specified in requirement PID_04. This is allowed according to ISO/IEC 18013-5.*

</div>
</div>

<div class="eudi-hlr" id="PID_06" markdown>
<div class="eudi-hlr__id">PID_06<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

When issuing a PID compliant with [ISO/IEC 18013-5], a PID Provider MAY include attributes that are not defined in the [PID Rulebook](../annex-3/annex-3.01-pid-rulebook.md). If so, these attributes SHALL be defined within a domestic PID namespace as meant in requirement ARB_10 in [Topic 12][topic-12]. The PID Provider SHALL generate the identifier for this domestic PID namespace by appending the applicable ISO 3166-1 alpha-2 country code or the ISO 3166-2 region code, separated by a period, to the PID namespace identifier specified in PID_05, excluding the version number. The PID Provider MAY include a version number in the domestic PID namespace identifier.

*Note: For example, the identifier of the first domestic PID namespace for Germany could be "eu.europa.ec.eudi.pid.de.1".*

</div>
</div>

<div class="eudi-hlr" id="PID_07" markdown>
<div class="eudi-hlr__id">PID_07<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A PID Provider that defines a domestic namespace SHALL publish the namespace, including all attribute identifiers, their definition, presence and encoding format, in an Attestation Rulebook complying with all applicable requirements in [Topic 12][topic-12].

</div>
</div>

<div class="eudi-hlr" id="PID_08" markdown>
<div class="eudi-hlr__id">PID_08<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

When issuing a PID compliant with [ISO/IEC 18013-5], a PID Provider SHALL include both the attributes and the metadata specified in [CIR 2024/2977] in the PID as issuer-signed data elements.

*Note: This implies that technically speaking, there is no difference between these attributes and metadata.*

</div>
</div>

<div class="eudi-hlr" id="PID_09" markdown>
<div class="eudi-hlr__id">PID_09<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

When issuing a PID compliant with [ISO/IEC 18013-5], a PID Provider SHALL encode each attribute or metadata in the PID as specified in the third column of the tables in [Section 4.2.1 of the PID Rulebook](../annex-3/annex-3.01-pid-rulebook.md).

</div>
</div>

<div class="eudi-hlr" id="PID_10" markdown>
<div class="eudi-hlr__id">PID_10<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

When issuing a PID compliant with [ISO/IEC 18013-5], a PID Provider SHALL encode each attribute or metadata in the PID in Concise Binary Object Representation (CBOR) according to [RFC 8949].

</div>
</div>

<div class="eudi-hlr" id="PID_11" markdown>
<div class="eudi-hlr__id">PID_11<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

When issuing a PID compliant with [ISO/IEC 18013-5], a PID Provider SHALL ensure that each PID contains at most one attribute with the same attribute identifier.

</div>
</div>

<div class="eudi-hlr" id="PID_12" markdown>
<div class="eudi-hlr__id">PID_12<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

When issuing a PID compliant with [ISO/IEC 18013-5], a PID Provider SHALL ensure that the value of all attributes and metadata in the PID is valid at the value of the timestamp in the validFrom element in the MSO, see [ISO/IEC 18013-5] clause 9.1.2.4.

*Note: The value of the age_over_18, age_over_NN, or age_in_years attributes, if present, changes whenever the User to whom the person identification data relates has a relevant birthday. The value of many other attributes will also change over time.*

</div>
</div>

<div class="eudi-hlr" id="PID_13" markdown>
<div class="eudi-hlr__id">PID_13<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If a PID Provider issues PIDs compliant with [ISO/IEC 18013-5] and containing the `issuance_date` or `expiry_date` attributes, the PID Provider SHALL have a policy for determining the value of these attributes relative to the `validFrom` and `validUntil` elements in the MSO, see [ISO/IEC 18013-5] clause 9.1.2.4.

*Note: See the notes to the `issuance_date` and `expiry_date` attributes in [PID Rulebook][pid-rulebook]. Examples of aspects to be considered in the policy may include (but are not limited to) the following:  1)  If an `issuance_date` or `expiry_date` is encoded as a `full-date` (rather than a `tdate`), it has no time element. However, `validFrom` and `validUntil` contain a time element, which is expressed in UTC. Therefore, comparing `expiry_date` to `validUntil`, for instance, may give ambiguous results in case the local time is not equal to UTC. The policy should ensure that situations are avoided where the User can legitimately expect (based on the values of `issuance_date` and `expiry_date` shown by the Wallet Unit when displaying the PID) that they can use their PID, while in reality its technical validity period (as determined by `validFrom` and `validUntil`) has not yet begun or has ended. 2) The exact meaning of `issuance_date` and `expiry_date` depends on local law and regulations. For example, in some jurisdictions an identity document whose `expiry_date` is in the past may by law still be used for identification for some purposes. However, this requires that the PID is still valid according to the `validFrom` and `validUntil` timestamps in the MSO. 3) A local requirement may exist stating that `issuance_date` and `expiry_date` must be identical to the dates on an existing physical document of the User.*

</div>
</div>


##### C. HLRs for SD-JWT VC-compliant PIDs <!-- omit from toc -->

<div class="eudi-hlr" id="PID_14" markdown>
<div class="eudi-hlr__id">PID_14<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A PID Provider issuing [SD-JWT VC]-compliant PIDs SHALL include the vct claim in their PIDs, where the vct claim SHALL be a URN within the `urn:eudi:pid:` namespace. The type indicated by the vct claim SHALL be `urn:eudi:pid:1` for the type defined in this document or a domestic type that extends it.

</div>
</div>

<div class="eudi-hlr" id="PID_15" markdown>
<div class="eudi-hlr__id">PID_15</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="PID_16" markdown>
<div class="eudi-hlr__id">PID_16<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A PID Provider that defines a domestic type SHALL publish information about the type, including all claim identifiers, their definition, presence and encoding format, in an Attestation Rulebook complying with all applicable requirements in [Topic 12][topic-12].

</div>
</div>

<div class="eudi-hlr" id="PID_17" markdown>
<div class="eudi-hlr__id">PID_17<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

When issuing a PID compliant with [SD-JWT VC], a PID Provider SHALL include both the attributes and the metadata specified in [CIR 2024/2977] in the PID as claims.

*Note: This implies that technically speaking, there is no difference between these attributes and metadata.*

</div>
</div>

<div class="eudi-hlr" id="PID_18" markdown>
<div class="eudi-hlr__id">PID_18<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

When issuing a PID compliant with [SD-JWT VC], a PID Provider SHALL encode each attribute or metadata in the PID as specified in the tables in [Section 5.2 of the PID Rulebook](../annex-3/annex-3.01-pid-rulebook.md).

</div>
</div>

<div class="eudi-hlr" id="PID_19" markdown>
<div class="eudi-hlr__id">PID_19<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

When issuing a PID compliant with [SD-JWT VC], a PID Provider SHALL ensure that the value of all attributes and metadata in the PID is valid at the value of the timestamp in the nbf claim, if present.

*Note: The value of the age-related claims, if present, changes whenever the User to whom the person identification data relates has a relevant birthday. The value of many other attributes will also change over time.*

</div>
</div>

<div class="eudi-hlr" id="PID_20" markdown>
<div class="eudi-hlr__id">PID_20<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If a PID Provider issues PIDs compliant with [SD-JWT VC] and containing the `date_of_issuance` or `date_of_expiry` claims, the PID Provider SHALL have a policy for determining the value of these claims relative to the `nbf` and `exp` claims in the SD-JWT VC, see [SD-JWT VC] section 3.2.2.2.

*Note: See the notes to the `date_of_issuance` and `date_of_expiry` attributes in [PID Rulebook][pid-rulebook]. Examples of aspects to be considered in the policy may include (but are not limited to) the following: 1) `date_of_issuance` and `date_of_expiry` claims do not have a time element. However, `nbf` and `exp` express a time relative to UTC. Therefore, comparing `date_of_expiry` to `exp`, for instance, may give ambiguous results in case the local time is not equal to UTC. The policy should ensure that situations are avoided where the User can legitimately expect (based on the value of `date_of_issuance` and `date_of_expiry` shown by the Wallet Unit when displaying the PID) that they can use their PID, while in reality its technical validity period (as determined by `nbf` and `exp`) has not yet begun or has ended. 2) The exact meaning of `date_of_issuance` and `date_of_expiry` depends on local law and regulations. For example, in some jurisdictions an identity document whose `date_of_expiry` is in the past may by law still be used for identification for some purposes. However, this requires that the PID is still valid according to the `nbf` and `exp` timestamps in the SD_JWT VC. 3) A local requirement may exist stating that `date_of_issuance` and `date_of_expiry` must be identical to the dates on an existing physical document of the User.*

</div>
</div>

<div class="eudi-hlr" id="PID_21" markdown>
<div class="eudi-hlr__id">PID_21<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

When issuing a PID compliant with [SD-JWT VC], a PID Provider SHALL make all claims (i.e., all top-level properties, all nested properties, and all array entries) selectively disclosable individually, except those claims defined as non-selectively disclosable in [SD-JWT VC].

</div>
</div>


[](){ #topic-4 }
