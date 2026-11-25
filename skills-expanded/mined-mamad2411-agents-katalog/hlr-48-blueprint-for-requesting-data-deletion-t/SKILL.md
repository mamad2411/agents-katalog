---
name: "hlr-48-blueprint-for-requesting-data-deletion-t"
description: "Use when working with EUDI high-level requirements for 'Blueprint for requesting data deletion to Relying Parties'. Contains normative SHALL/SHOULD/MAY requirements from ARF Annex 2."
sections:
  - "A.2.3.27 Topic 48 - Blueprint for requesting data deletion to Relying Parties"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~1066 -->

#### A.2.3.27 Topic 48 - Blueprint for requesting data deletion to Relying Parties

<div class="eudi-hlr" id="DATA_DLT_01" markdown>
<div class="eudi-hlr__id">DATA_DLT_01<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL support the possibilities mentioned in DATA_DLT_02, allowing a User to request from a Relying Party the erasure of their attributes that were presented by that Wallet Unit to that Relying Party, in accordance with Article 17 of Regulation (EU) 2016/679.

</div>
</div>

<div class="eudi-hlr" id="DATA_DLT_02" markdown>
<div class="eudi-hlr__id">DATA_DLT_02<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL support at least the following possibilities to send a data erasure request to a Relying Party: a) Open a URL in an external browser to ask for the deletion of data in a web form provided by the Relying Party, b) Open an external mail client and start a draft e-mail to the Relying Party, with a suitable template text, c) open an external phone client and start a phone call. Depending on whether a Relying Party URL, e-mail address, and/or phone number was logged for the relevant attestation presentation transaction (see requirement DASH_03 in [Topic 19][topic-19]), the Wallet Unit SHALL offer the User to use one or more of these possibilities.

</div>
</div>

<div class="eudi-hlr" id="DATA_DLT_02a" markdown>
<div class="eudi-hlr__id">DATA_DLT_02a</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="DATA_DLT_03" markdown>
<div class="eudi-hlr__id">DATA_DLT_03<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Instance SHALL provide a function where the User may select one Relying Party to which a data deletion request must be submitted.

</div>
</div>

<div class="eudi-hlr" id="DATA_DLT_04" markdown>
<div class="eudi-hlr__id">DATA_DLT_04</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="DATA_DLT_05" markdown>
<div class="eudi-hlr__id">DATA_DLT_05<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL include the initiation of a data deletion request in a log, so it can be displayed to the User via the dashboard as specified in [Topic 19][topic-19].

*Note: Because the request is sent by an external web browser, e-mail client, or phone client (see DATA_DLT_02), the Wallet Unit can only log the initiation of the request.*

</div>
</div>

<div class="eudi-hlr" id="DATA_DLT_06" markdown>
<div class="eudi-hlr__id">DATA_DLT_06<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For the initiation of a data deletion request, the log SHALL contain at least: - Date and time of the initiation of the request, - Name and unique identifier of the Relying Party to which the request was made, - Attributes requested to be deleted.

</div>
</div>

<div class="eudi-hlr" id="DATA_DLT_07" markdown>
<div class="eudi-hlr__id">DATA_DLT_07<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Before executing a data deletion request, a Relying Party SHALL authenticate the requesting User (or the request itself), using appropriate authentication mechanisms of its own choosing. The Relying Party SHOULD use the authentication or signature facilities offered by the User's Wallet Unit for this purpose.

</div>
</div>

<div class="eudi-hlr" id="DATA_DLT_08" markdown>
<div class="eudi-hlr__id">DATA_DLT_08<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Wallet Units, Relying Parties, and Registrars SHALL comply with the relevant requirements in [Technical Specification 7](../../technical-specifications/ts7-common-interface-for-data-deletion-request.md).

</div>
</div>


[](){ #topic-50 }
