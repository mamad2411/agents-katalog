---
name: "hlr-42-requirements-for-qtsps-to-access-authent"
description: "Use when working with EUDI high-level requirements for 'Requirements for QTSPs to access Authentic Sources'. Contains normative SHALL/SHOULD/MAY requirements from ARF Annex 2."
sections:
  - "A.2.3.24 Topic 42 - Requirements for QTSPs to access Authentic Sources"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~1215 -->

#### A.2.3.24 Topic 42 - Requirements for QTSPs to access Authentic Sources

<div class="eudi-hlr" id="QTSPAS_01" markdown>
<div class="eudi-hlr__id">QTSPAS_01<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

In accordance with [ETSI TS 119 478] and [Technical Specification 11][ts11], Member States SHALL define: - discovery mechanisms that enable QTSPs to request information about Authentic Sources or designated intermediaries recognised at the national level. This includes information regarding the attributes of a natural or legal person for which the Authentic Source or designated intermediary is considered a primary source, or for which it is recognised as authentic in accordance with Union law or national law, including administrative practices. - procedures for QTSPs to request the verification of attributes from Authentic Sources.

</div>
</div>

<div class="eudi-hlr" id="QTSPAS_02" markdown>
<div class="eudi-hlr__id">QTSPAS_02<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

An Authentic Source in the public sector, or its designated intermediary, SHALL implement an interface complying with [ETSI TS 119 478] and [Technical Specification 11][ts11] for receiving verification requests and sending responses. For each received request, the Authentic Source SHALL - identify and authenticate the requestor in such a way that it can subsequently determine whether the requestor is a QTSP issuing qualified electronic attestation of attributes, for example by means of a lookup in the QTSP Trusted List. - authenticate the User and obtain their approval, if it is legally obliged to do so, in addition to the User authentication and approval already performed by the QTSP according to QTSPAS_08. - verify whether the attribute values claimed by the QTSP match the values held by the Authentic Source and, finally, - respond with one of the following for each attribute: +'match', if the attribute value held for this User by the Authentic Source is identical to the value claimed by the QTSP, + 'no match', if the attribute value held for this User by the Authentic Source is not identical to the value claimed by the QTSP, including if the Authentic Source is the authentic source for this attribute but does not hold a value for this User, +'unknown', if the Authentic Source is not the authentic source for this attribute.

</div>
</div>

<div class="eudi-hlr" id="QTSPAS_03" markdown>
<div class="eudi-hlr__id">QTSPAS_03<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

An Authentic Source or designated intermediary SHALL respond to a verification request for attributes by any QTSP issuing qualified electronic attestation of attributes.

</div>
</div>

<div class="eudi-hlr" id="QTSPAS_04" markdown>
<div class="eudi-hlr__id">QTSPAS_04<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

An Authentic Source or designated intermediary SHALL implement the technical specifications mentioned in QTSPAS_01, so that the QTSP will receive the result of the verification of the requested attributes as described in QTSPAS_02. If the verification is deferred, the response to the QTSP SHALL include the maximum time that it will take to verify the requested attributes, and a unique identifier that the QTSP SHALL use to obtain the result of the verification.

</div>
</div>

<div class="eudi-hlr" id="QTSPAS_05" markdown>
<div class="eudi-hlr__id">QTSPAS_05<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A QTSP SHALL send an attribute verification request directly to the Authentic Source or designated intermediary recognised at national level, after discovering it using the mechanisms specified the technical specifications mentioned in QTSPAS_01.

</div>
</div>

<div class="eudi-hlr" id="QTSPAS_06" markdown>
<div class="eudi-hlr__id">QTSPAS_06<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Member States SHALL specify the processes and mechanisms to designate the Authentic Sources or intermediaries recognised at national level in accordance with Union or national law, allowing these Authentic Sources or intermediaries to verify the attributes presented to them by QTSPs.

</div>
</div>

<div class="eudi-hlr" id="QTSPAS_07" markdown>
<div class="eudi-hlr__id">QTSPAS_07</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="QTSPAS_07a" markdown>
<div class="eudi-hlr__id">QTSPAS_07a</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="QTSPAS_08" markdown>
<div class="eudi-hlr__id">QTSPAS_08<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A QTSP SHALL obtain approval from the User to verify the authenticity of the attributes, before requesting the verification of those attributes by the relevant Authentic Source or designated intermediary.

</div>
</div>


[](){ #topic-43 }
