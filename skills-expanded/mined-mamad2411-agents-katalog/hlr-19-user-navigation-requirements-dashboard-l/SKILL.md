---
name: "hlr-19-user-navigation-requirements-dashboard-l"
description: "Use when working with EUDI high-level requirements for 'User navigation requirements (Dashboard logs for transparency)'. Contains normative SHALL/SHOULD/MAY requirements from ARF Annex 2."
sections:
  - "A.2.3.12 Topic 19 - User navigation requirements (Dashboard logs for transparency)"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~3632 -->

#### A.2.3.12 Topic 19 - User navigation requirements (Dashboard logs for transparency)

<div class="eudi-hlr" id="DASH_01" markdown>
<div class="eudi-hlr__id">DASH_01<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL provide a user-friendly dashboard functionality to its User.

</div>
</div>

<div class="eudi-hlr" id="DASH_02" markdown>
<div class="eudi-hlr__id">DASH_02<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Wallet Unit SHALL log all transactions executed through the Wallet Unit, including any transactions that were not completed successfully. This log SHALL include all types of transaction executed through the Wallet Unit: a) PID or attestation issuance and re-issuance transactions, b) PID or attestation presentation transactions, c) Wallet-to-Wallet transactions (see [Topic 30][topic-30]), d) pseudonym registration or presentation transactions, e) signature or seal creation transactions (see [Topic 16][topic-16]), f) data deletion requests sent to a Relying Party (see [Topic 48][topic-48]), g) reports sent to a Data Protection Authority (see [Topic 50][topic-50]), h) PID or attestation deletions by the User.

*Note: For the data to be logged for a data deletion request to a Relying Party or a report sent to a DPA, see Topic 48 and Topic 50, respectively. For other types of transaction, the data to be logged is specified in the requirements in this Topic.*

</div>
</div>

<div class="eudi-hlr" id="DASH_02a" markdown>
<div class="eudi-hlr__id">DASH_02a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Wallet Unit SHALL retain transactions in the log at least for the minimum retention period specified in applicable legislation. If the Wallet Unit must delete transactions from the log, for instance because of size limitations, the Wallet Unit SHALL notify the User via the dashboard before doing so, indicating the potential consequences for the User's data protection rights, and SHALL instruct the User how to export the transactions that are about to be deleted. See DASH_07.

</div>
</div>

<div class="eudi-hlr" id="DASH_02b" markdown>
<div class="eudi-hlr__id">DASH_02b<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The dashboard SHALL include a functionality to display to the User an overview of all transactions in the log.

</div>
</div>

<div class="eudi-hlr" id="DASH_02c" markdown>
<div class="eudi-hlr__id">DASH_02c<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The transaction log meant in DASH_02 SHALL comply with all relevant requirement in [Technical Specification 10](../../technical-specifications/ts10-data-portability-and-download-(export).md), including measures to ensure and/or verify its confidentiality, integrity, and authenticity.

</div>
</div>

<div class="eudi-hlr" id="DASH_03" markdown>
<div class="eudi-hlr__id">DASH_03<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For a PID or attestation presentation transaction executed through the Wallet Unit, the log SHALL contain at least: a) the date and time of the transaction, b) the trade name, unique identifier, and Service identifier of the corresponding Relying Party, and the Member State in which that Relying Party is established, c) the trade name, contact details (if available), unique identifier, and Service identifier of the intermediary, if an intermediary is involved in the transaction, d) the attestation type(s) and the identifier(s) of the attribute(s) that were requested, as well as those that were presented, e) in the case of non-completed transactions, the reason for such non-completion, f) the URL of the online service of the Relying Party's Registrar. g) the web form URL (if available), e-mail address (if available), and telephone number (if available) provided by the Relying Party for sending data deletion requests, see requirement RPRC_11 in [Topic 44][topic-44], h) the name and country of the Data Protection Authority supervising the Relying Party, as well as the web form URL (if available), e-mail address (if available), and telephone number (if available) provided by this DPA for reporting suspicious attribute presentation requests. i) information on the intended use and the URL to the applicable privacy policy.

*Note: a) If an intermediary is involved in the transaction, the Wallet Unit obtains the information under point b) from the registration certificate in the presentation request, and the information under point c) from the access certificate. In case no intermediary is involved, the Wallet Unit obtains the information under point b) from either the registration certificate or the access certificate, because it is identical in both certificates. b) The information in points g) and h) can be retrieved from the registration certificate. At least one of the options (URL, e-mail address, or telephone number) will be present. See RPRC_11 and RPRC_12.*

</div>
</div>

<div class="eudi-hlr" id="DASH_03a" markdown>
<div class="eudi-hlr__id">DASH_03a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For a PID or attestation presentation transaction or a Wallet-to-Wallet transaction executed through the Wallet Unit, the log SHALL NOT contain the value of any attributes presented to the Relying Party or the Verifier Wallet Unit.

</div>
</div>

<div class="eudi-hlr" id="DASH_03b" markdown>
<div class="eudi-hlr__id">DASH_03b<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For a Wallet-to-Wallet transaction executed through the Wallet Unit, the log SHALL contain at least: a) the date and time of the transaction, b) the role of the Wallet Unit (Holder Wallet Unit or Verifier Wallet Unit), c) the attestation type(s) and the identifier(s) of the attribute(s) that were requested, as well as those that were presented, d) in the case of non-completed transactions, the reason for such non-completion.

</div>
</div>

<div class="eudi-hlr" id="DASH_03c" markdown>
<div class="eudi-hlr__id">DASH_03c<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For a pseudonym registration or presentation transaction executed through the Wallet Unit, the log SHALL contain at least: a) the date and time of the transaction, b) identifying information about the Relying Party, if known to the Wallet Unit, c) whether it is a pseudonym registration or pseudonym presentation transaction, d) in the case of non-completed transactions, the reason for such non-completion.

*Note: Regarding point b), see PA_20 in [Topic 11][topic-11].*

</div>
</div>

<div class="eudi-hlr" id="DASH_03d" markdown>
<div class="eudi-hlr__id">DASH_03d<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If a presentation request contains transactional data, the Wallet Unit SHALL log the value of this transactional data only to the extent explicitly required by the applicable Technical Specification associated with the requested SUA attestation, and in accordance with data minimisation principles. If the applicable Technical Specification does not explicitly specify that transactional data shall be logged, the Wallet Unit SHALL NOT log the value of any transactional data.

*Note: a) For the concepts of transactional data and SUA attestations and their related Technical Specifications, see [Topic 20][topic-20]. b) For example, for PSD2 Strong Customer Authentication transactions, the scope of transactional data to be included in the transaction log is defined in [Technical Specification 12](../../technical-specifications/ts12-electronic-payments-SCA-implementation-with-wallet.md) and includes the payment transaction identifier and merchant name.*

</div>
</div>

<div class="eudi-hlr" id="DASH_04" markdown>
<div class="eudi-hlr__id">DASH_04<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For a signature or seal creation transaction executed through the Wallet Unit, the log SHALL contain at least: a) the date and time of the transaction, b) the document or data signed or sealed (if available to the Wallet Unit), c) in the case of non-completed transactions, the reason for such non-completion.

</div>
</div>

<div class="eudi-hlr" id="DASH_05" markdown>
<div class="eudi-hlr__id">DASH_05<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For a PID or attestation issuance or re-issuance transaction executed through the Wallet Unit, the log SHALL contain at least: a) the date and time of the transaction, b) the trade name, contact details (if available), unique identifier, and Service identifier of the corresponding PID Provider or Attestation Provider, c) the attestation type requested, as well as the attestation type issued, d) the number of attestations requested and issued (i.e., the size of the batch in case of batch issuance), e) in the case of non-completed transactions, the reason for such non-completion. f) for a re-issuance transaction, whether it was triggered by the User or by the Wallet Unit without involvement of the User, g) the URL of the associated Registrar's online service.

*Note: a) The Wallet Unit obtains the information under point b) from either the registration certificate or the access certificate, because it is identical in both certificates. b) Regarding point g): this URL can be retrieved from the access certificate.*

</div>
</div>

<div class="eudi-hlr" id="DASH_05a" markdown>
<div class="eudi-hlr__id">DASH_05a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For the deletion of a PID or attestation by the User, the log SHALL contain at least: a) the date and time of the deletion event, b) the attestation type of the deleted PID or attestation. c) The name and unique identifier of the corresponding PID Provider or Attestation Provider.

*Note: This requirement is not about deletion of transactions from the log, as per DASH_06a.*

</div>
</div>

<div class="eudi-hlr" id="DASH_06" markdown>
<div class="eudi-hlr__id">DASH_06<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Wallet Provider SHALL ensure the confidentiality, integrity, and authenticity of all transactions included in the log.

</div>
</div>

<div class="eudi-hlr" id="DASH_06a" markdown>
<div class="eudi-hlr__id">DASH_06a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Via the dashboard, the Wallet Unit SHALL enable the User to delete any transaction in the log. Before deleting any transactions, the Wallet Unit SHALL indicate to the User the potential consequences for the User's data protection rights.

*Note: This requirement applies even in case the minimum retention period specified in applicable legislation (see DASH_02a) is not yet over.*

</div>
</div>

<div class="eudi-hlr" id="DASH_06b" markdown>
<div class="eudi-hlr__id">DASH_06b<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Wallet Unit SHALL ensure that no entity other than the User can delete transactions from the log, except possibly for the reason mentioned in DASH_02a.

</div>
</div>

<div class="eudi-hlr" id="DASH_07" markdown>
<div class="eudi-hlr__id">DASH_07<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The dashboard SHALL allow the User to export the details of one or more transactions in the log to a file, using the common format specified according to DASH_02c, while ensuring their confidentiality, authenticity and integrity. The file SHALL be stored in an external storage or remote storage location of the User's choice, from among the storage options supported by the Wallet Unit and SHALL use the common format and security measures specified according to DASH_02c.

</div>
</div>

<div class="eudi-hlr" id="DASH_08" markdown>
<div class="eudi-hlr__id">DASH_08<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For a natural-person User, a Wallet Instance SHALL provide a User interface.

</div>
</div>

<div class="eudi-hlr" id="DASH_09" markdown>
<div class="eudi-hlr__id">DASH_09<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The User interface referred to in DASH_08 SHALL provide a view with - the EU Digital Identity Wallet Trust Mark, - accompanying general information on the certification of Wallet Solutions, - links to the certification status information as defined in the [Technical Specification 1](../../technical-specifications/ts1-eudi-wallet-trust-mark.md).

</div>
</div>

<div class="eudi-hlr" id="DASH_09a" markdown>
<div class="eudi-hlr__id">DASH_09a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Positioning of the view meant in DASH_09 in the Wallet UI navigation SHALL follow design guidelines provided by the European Commission.

</div>
</div>

<div class="eudi-hlr" id="DASH_09b" markdown>
<div class="eudi-hlr__id">DASH_09b<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Regarding the EUDI Wallet Trust Mark, Wallet Providers and Wallet Units SHALL comply with all relevant requirements in [Technical Specification 1](../../technical-specifications/ts1-eudi-wallet-trust-mark.md), as well as with the relevant requirements in Article 14a of [CIR 2024/2979] and the Annexes mentioned therein.

</div>
</div>

<div class="eudi-hlr" id="DASH_10" markdown>
<div class="eudi-hlr__id">DASH_10</div>
<div class="eudi-hlr__body" markdown>

Empty

*Note: See requirement WIAM_12a in [Topic 40][topic-40].*

</div>
</div>

<div class="eudi-hlr" id="DASH_11" markdown>
<div class="eudi-hlr__id">DASH_11</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="DASH_12" markdown>
<div class="eudi-hlr__id">DASH_12<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The User interface referred to in DASH_08 SHALL enable the User, for each presentation transaction in the log, to easily request the Relying Party to delete any or all attributes presented to it in that transaction, or to send a report about that particular transaction to a DPA.

</div>
</div>


[](){ #topic-20 }
