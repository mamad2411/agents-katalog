---
name: "hlr-50-blueprint-to-report-unlawful-or-suspicio"
description: "Use when working with EUDI high-level requirements for 'Blueprint to report unlawful or suspicious request of data'. Contains normative SHALL/SHOULD/MAY requirements from ARF Annex 2."
sections:
  - "A.2.3.28 Topic 50 - Blueprint to report unlawful or suspicious request of data"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~1110 -->

#### A.2.3.28 Topic 50 - Blueprint to report unlawful or suspicious request of data

<div class="eudi-hlr" id="RPT_DPA_01" markdown>
<div class="eudi-hlr__id">RPT_DPA_01<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL enable the User to start the process of reporting a suspicious presentation request to a DPA. When prompted by the User, a Wallet Unit SHALL provide the contact details of the DPA which supervises the Relying Party that made the suspicious request, available in the log for that request (see DASH_03). In addition, the Wallet Unit MAY also provide the contact details of the DPA of the region in which the Wallet Provider is residing, or of other DPAs, taken from the European Data Protection Board website (<https://www.edpb.europa.eu/about-edpb/about-edpb/members_en>).

</div>
</div>

<div class="eudi-hlr" id="RPT_DPA_02" markdown>
<div class="eudi-hlr__id">RPT_DPA_02<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Wallet Unit SHALL offer the User the option to report a suspicious request to a DPA via the transaction log presented in the dashboard, see [Topic 19][topic-19].

</div>
</div>

<div class="eudi-hlr" id="RPT_DPA_02a" markdown>
<div class="eudi-hlr__id">RPT_DPA_02a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL support at least the following possibilities to report a suspicious presentation request to a DPA, depending on what contact details are available for the DPA: a) Open a URL in an external browser to report the request in a web form provided by the DPA. b) Open an external e-mail client and start a draft e-mail to the DPA, with a suitable template text, c) open an external phone client and start a phone call.

</div>
</div>

<div class="eudi-hlr" id="RPT_DPA_03" markdown>
<div class="eudi-hlr__id">RPT_DPA_03</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="RPT_DPA_04" markdown>
<div class="eudi-hlr__id">RPT_DPA_04<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Provider SHALL ensure that a Wallet Unit allows its User to substantiate a report sent to a DPA, including by attaching relevant information to identify the Relying Party and the Users' claims in a machine-readable format.

*Note: The log kept by the Wallet Unit is standardised in [Technical Specification 10](https://github.com/eu-digital-identity-wallet/eudi-doc-standards-and-technical-specifications/blob/main/docs/technical-specifications/ts10-data-portability-and-download-(export).md) and is machine-readable in order to enable data portability. An excerpt from this log therefore can be used to substantiate the report.*

</div>
</div>

<div class="eudi-hlr" id="RPT_DPA_05" markdown>
<div class="eudi-hlr__id">RPT_DPA_05<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL log the fact that it initiated the sending of a report to a DPA (see RPT_DPA_02a), as specified in [Topic 19][topic-19].

</div>
</div>

<div class="eudi-hlr" id="RPT_DPA_05a" markdown>
<div class="eudi-hlr__id">RPT_DPA_05a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For a report sent to a DPA, the log SHALL contain at least: a) the date and time when the report was sent, b) the name and country of the DPA, and c) the channel and contact information used for initiating sending the report, i.e., the URL, e-mail address, or phone number of the DPA.

</div>
</div>

<div class="eudi-hlr" id="RPT_DPA_06" markdown>
<div class="eudi-hlr__id">RPT_DPA_06<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Wallet Units, Data Protection Authorities, and Registrars SHALL comply with the relevant requirements in [Technical Specification 8](../../technical-specifications/ts8-common-interface-for-reporting-of-wrp-to-dpa.md).

</div>
</div>


[](){ #topic-51 }
