---
name: "arf-topic-lm-data-deletion-and-wrp-reportin-part-2"
description: "Use when implementing data deletion requests or wrongful request of personal data (WRP) reporting. Covers deletion interfaces, DPA reporting mechanisms, and compliance requirements. Part 2: covers 2. Overview, 3. Recalling the previously existing High-Level Requirements, 4. Erasure of personal data at a wallet-relying party ...."
sections:
  - "2. Overview"
  - "3. Recalling the previously existing High-Level Requirements"
  - "3.1 Existing High-Level Requirements specified in Topic 48"
  - "3.2 Existing High-Level Requirements specified in Topic 50"
  - "4. Erasure of personal data at a wallet-relying party"
  - "4.1 Discussions related to DATA_DLT_01 and DATA_DLT_02"
  - "5. Reporting a wallet-relying party to the competent data protection supervisory authority"
  - "5.1 Discussions related to RPT_DPA_01"
  - "5.2 Discussions related to RPT_DPA_02"
  - "5.3 Discussions related to RPT_DPA_03"
  - "5.4 Discussions related to RPT_DPA_04"
  - "5.5 Discussions related to RPT_DPA_05"
  - "5.6 Additional high level requirement RPT_DPA_06"
  - "6. Updated set of High Level Requirements"
  - "6.1 Update for Topic 48 (Erasure of personal data at a wallet-relying party)"
  - "6.2 Update for Topic 50 (Reporting a wallet-relying party to the competent data protection supervisory authority)"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~5157 -->

## 2. Overview

According to Article 5a (5) (a) of Regulation [(EU) No 910/2014](http://data.europa.eu/eli/reg/2014/910/oj)
a wallet solution shall support common protocols and interfaces for

* (ix) requesting a relying party to **erase the personal data** stored at a wallet-relying party pursuant to Article 17 of Regulation
  [(EU) 2016/679](http://data.europa.eu/eli/reg/2016/679/oj) and
* (x) **reporting a relying party to the competent national data protection authority** where 
an allegedly unlawful or suspicious request for data is received.

The present document discusses topics related to these protocols and interfaces, as outlined in the following figure. 

![Overview](img/Privacy-Architecture.svg)

>**Note:** The discussion with the experts from the EU Member States soon revealed, that 
> one may safely assume that there are already suitable processes in place for the process of data erasure
> requests addressed within the present document. For reports to Data Protection Authorities, there may 
> exist partially similar processes linked to handling GDPR-related complaints in spite of their different legal 
> grounds (both processes involve a user sending information to a Data Protection Authority about a third party).
> 
> Therefore, the overall strategy of the present document is to utilise the existing interfaces 
> and processes of the relying parties and supervisory authorities as much as possible and abstain from
> the creation of additional interfaces to wallet-relying parties and supervisory authorities.

## 3. Recalling the previously existing High-Level Requirements

### 3.1 Existing High-Level Requirements specified in Topic 48 

The following high-level requirements have been specified in [Topic 48][topic-48]
before starting the present discussion:

| **Index** | **Requirement specification** |
|-----------|------------------|
| DATA_DLT_01 | A Wallet Provider SHALL ensure that its Wallet Units support the technical specifications mentioned in DATA_DLT_02, allowing a User to request from a Relying Party the erasure of their attributes that were presented by that Wallet Unit to that Relying Party, in accordance with Regulation (EU) 2016/679. |
| DATA_DLT_02 | The Commission SHALL, in cooperation with the Member States, develop technical specifications for a Wallet Unit interface allowing a Wallet Unit to send attribute deletion requests to Relying Parties with whom it has interacted in the past. |
| DATA_DLT_03 | A Wallet Instance SHALL provide a function where the User may select one Relying Party or multiple Relying Parties for which an attribute deletion request must be submitted. |
| DATA_DLT_04 | A Wallet Instance SHALL be able to display the attribute deletion requests previously submitted through the Wallet Unit. |
| DATA_DLT_05 | A Wallet Unit SHALL include attribute deletion requests in a log so they can be presented to the User via the dashboard (as specified in [Topic 19][topic-19]). |
| DATA_DLT_06 | The log SHALL include as a minimum: - Date of attribute deletion request, - Relying Party to which the request was made, - Attributes requested to be removed. |

### 3.2 Existing High-Level Requirements specified in Topic 50

The following high-level requirements have been specified in [Topic 50][topic-50] before starting the discussion:

| **Index** | **Requirement specification** |
|-----------|--------------------|
| RPT_DPA_01 | A Wallet Unit SHALL provide an interface to lodge a complaint of suspicious Relying Party presentation requests to the DPA of the Member State that provided the Wallet Unit. |
| RPT_DPA_02 | The User interface enabling a User to start the process of lodging a complaint SHALL be accessible via the Wallet Instance. |
| RPT_DPA_03 | A Wallet Provider SHALL implement the interface in compliance with national procedural law and administrative practices. |
| RPT_DPA_04 | A Wallet Unit SHALL enable the lodged complaint to be substantiated, including information to identify the Relying Party, their presentation request, and the User's allegation. |
| RPT_DPA_05 | A Wallet Unit SHALL keep reports sent to the DPA in a log file so that it can be presented to the User in the dashboard (as specified in [Topic 19][topic-19]). |

## 4. Erasure of personal data at a wallet-relying party

### 4.1 Discussions related to DATA_DLT_01 and DATA_DLT_02

During the discussions with the delegated experts from the EU Member States the following
aspects related to DATA_DLT_01 and DATA_DLT_02 have been discussed:

1) The wording "in accordance with Regulation (EU) 2016/679" in DATA_DLT_01 leaves
   room for interpretation what exactly is meant here. Therefore the
   text should better be changed to "in accordance with **Article 17 of** Regulation (EU) 2016/679".

The resulting requirement **DATA_DLT_01** is hence specified as follows, whereas the changes are marked as **bold**:

> A Wallet Provider SHALL ensure that its Wallet Units support the technical specifications mentioned in 
> DATA_DLT_02, allowing a User to request from a Relying Party the erasure of their attributes that were 
> presented by that Wallet Unit to that Relying Party, in accordance with **Article 17 of** Regulation (EU) 2016/679.

2) During the discussions it was mentioned that one may assume that relying parties, which act as processors or controllers
   **already have procedures, protocols and interfaces in place to handle data deletion requests** in accordance
   with regulation (EU) 2016/679. There was a consensus among the participants in the discussion, that the wallet unit should simply
   re-use the already existing interfaces offered by the wallet-relying parties. As there are no standardised protocols
   and interfaces for this purpose (yet), this implies that the wallet unit can offer only to **open an external mail client with a suitable 
   template text** or offer only to **open a specific URL with an external browser** to ask for the deletion of data 
   in a web form provided by the wallet-relying party. It was suggested, that the registration certificate should contain 
   the necessary contact information of the wallet-relying party, including an email address or the location of a web form 
   for privacy-related enquiries.

3) It was also discussed that the details of the handling of the data deletion request is
   within the responsibility of the wallet-relying party in its role as controller, or processor
   acting on behalf of a controller. According to Article 12 (6) of Regulation (EU) 2016/679, the controller may 
   request additional information necessary to confirm the identity of the data subject. In any case Article 24 of 
   (EU) 2016/679 clarifies that the controller is responsible for the implementation of suitable technical and 
   organisational measures for the protection of personal data in line with Article 32 of (EU) 2016/679, which 
   obviously includes the requirement to **authenticate the user**, which submits a data deletion request, 
   **or the request itself** using an appropriate electronic signature. The **technical details** for this 
   authentication procedure are within the **responsibility of the wallet-relying party**, 
   acting as controller or processor, and hence there can only be a **recommendation** for the wallet-relying party 
   to utilise the strong authentication or signature facilities offered by the wallet solutions for this purpose.

This additional recommendation **DATA_DLT_07** is specified as follows: 

> While the Wallet-Relying Party is responsible for choosing appropriate authentication mechanisms before
> executing a data deletion request, it is RECOMMENDED to use the authentication and signature 
> facilities offered by the Wallet Solutions for this purpose.    

   It seems that the Commission and the EU Member States can only encourage and facilitate the development of 
   appropriate **codes of conducts** for wallet-relying parties according to Article 5f of (EU) No. 910/2014, 
   which may also address privacy-related aspects, such as the exercise of rights of data subjects according 
   to Article 40 Nr. 2 (f) of (EU) 2016/679 for example. These code of conducts could
   include the **recommendation** to utilise the strong and trustworthy **authentication, identification and 
   qualified electronic signature** capabilities of the wallet solutions for implementing the necessary 
   authentication procedure. In a similar manner, such aspects may also be addressed in certification criteria 
   according to Article 42 of (EU) 2016/679.
   

#### 4.2 Discussions related to DATA_DLT_03

During the discussions with the delegated experts from the EU Member States the following
aspect related to DATA_DLT_03 was discussed:

The possibility to send a data deletion request to more than one relying party in a single step does not seem to be appropriate
for the specific case, as requesting the data deletion is a rather sensitive process. Therefore it was agreed that the words
"**or multiple Relying Parties**" in DATA_DLT_03 should better be **deleted**.

#### 4.3 Discussions related to DATA_DLT_04

During the discussions with the delegated experts from the EU Member States the following
aspect related to DATA_DLT_04 was discussed:

It was suggested to **delete this requirement**, as the detailed requirements of the common dashboard are handled in [Topic 19][topic-19].

#### 4.4 Discussions related to DATA_DLT_05

The discussions related to DATA_DLT_05 **did not reveal any need for changes**.

#### 4.5 Discussions related to DATA_DLT_06

During the discussions with the delegated experts from the EU Member States the following
aspects related to DATA_DLT_06 were discussed:

1) The point was raised that the wallet unit is only able to initiate the process for a data
   deletion request and hence it is unclear what exactly the log according to Article 5a (4) (d) of
   the regulation (EU) No 910/2014 should contain. As the regulation speaks about a
   "log of all transactions", which contains a "list of relying parties with which the user
   has established a connection and, where applicable, all data exchanged", it seems to be appropriate
   to also **log the initiation of a data deletion request**, even if it is not clear, whether the
   partly prepared email was submitted in the end.

Therefore, it was agreed to change the text of **DATA_DLT_06** as follows:

> The log SHALL **also document the initiation of a data deletion request and** include as a minimum: 
>>- Date **and time** of attribute deletion request, 
>>- Relying Party to which the request was made, 
>>- Attributes requested to be removed.

## 5. Reporting a wallet-relying party to the competent data protection supervisory authority

### 5.1 Discussions related to RPT_DPA_01

During the discussions with the delegated experts from the EU Member States the following
aspects related to **RPT_DPA_01** have been discussed:

1) According to Article 4 (22) of the regulation (EU) 2016/679, the wallet user may, in its role of being the data subject,
   report suspicious behaviour to, or even lodge a complaint according to Article 77 of (EU) 2016/679 with, different supervisory authorities, including

   a) the supervisory authority responsible for the region in which the controller or processor is established on the territory of the Member State of that supervisory authority;

   b) data subjects residing in the Member State of that supervisory authority are substantially affected or likely to be substantially affected by the processing;

   c) or a complaint has been lodged with that supervisory authority;

2) As the regulation (EU) No. 910/2014 in its Article 5a (4) (d) (iii) and Article 5a (5) (a) (x) mentions the
   "reporting a relying party to the competent national data protection authority", it is clear that
   the wallet unit should in particular allow to get in contact with the competent national supervisory authority,
   which supervises the wallet-relying party. If the contact details of the supervisory authority for the wallet-relying
   party information is not available, the wallet unit should offer to get in contact with the supervisory authority
   of the wallet provider and it may even offer a link to the members of the European Data Protection Board at
   <https://www.edpb.europa.eu/about-edpb/about-edpb/members_en>.

Against the background of the discussion and comments received, it was agreed upon updating **RPT_DPA_01** to the following text:

> When prompted by the User, a Wallet Unit SHALL provide the contact details of the DPA, which supervises
> the Relying Party, if available, and SHALL make it easy for the User to send a report of allegedly unlawful or 
> suspicious Relying Party presentation requests to this DPA. If these are not available, the Wallet Unit SHALL 
> provide the contact details of the DPA of the region in which the Wallet Provider is residing. In addition, the Wallet Unit MAY
> also provide contact details of other DPAs taken from the "European Data Protection Board" website (<https://www.edpb.europa.eu/about-edpb/about-edpb/members_en>),
> and allow the User to choose a DPA to continue the reporting process.

### 5.2 Discussions related to RPT_DPA_02

During the discussions with the delegated experts from the EU Member States the following
aspects related to RPT_DPA_02 have been discussed:

It was discussed that there is difference between reporting suspicious
behaviour of a wallet-relying party as required by Article 5a of (EU) No. 910/2014
and lodging a complaint with a supervisory authority according to Article 77 of (EU) 2016/679.

Therefore, it was agreed to change the text of **RPT_DPA_02** as follows:

>The User interface enabling a User to start the process of **reporting a Wallet-relying Party to
> a DPA** SHALL be accessible via the log provided by the Wallet Unit.

### 5.3 Discussions related to RPT_DPA_03

During the discussions with the delegated experts from the EU Member States the following
aspect related to **RPT_DPA_03** was discussed:

It was discussed, whether mentioning the national procedural law is suitable here,
as fulfilling the requirements of the regulation (EU) 2016/679 should be
sufficient. The wallet providers should better not be obliged to take into account
requirements from national procedural law and hence it was decided to delete this requirement.

### 5.4 Discussions related to RPT_DPA_04

During the discussions with the delegated experts from the EU Member States the following
aspects related to **RPT_DPA_04** were discussed:

It was discussed, whether the text "and the User's allegation" is appropriate here, as
this does not seem to be mentioned in the regulation (EU) No. 910/2014.

However, Article 7 of the implementing act (EU) 2024/2982 mentions the possibility to "substantiate the reports, including by attaching relevant information
to identify the wallet-relying parties, and the wallet users’ claims in machine-readable format".

Furthermore, it was discussed that Article 5a (4) (d) (i) of the regulation
(EU) No. 910/2014 requires that the log allows to "view an up-to-date list of relying parties
with which the user has established a connection **and, where applicable, all data exchanged**".
The related storage requirements seem to be rather modest, as the digital signatures are usually
rather small. On the other hand, it was also argued, that it is questionable that submitting
the signatures with the initial report might not be necessary, as this kind of information could
be provided after an explicit request of the DPA in a subsequent step. In this case the wallet unit
could also be used to sign an export from the log to provide non-repudiation.

Against this background it was decided to revise the text of **RPT_DPA_04** as follows:

> Wallet providers SHALL ensure that wallet units allow wallet users to substantiate the reports,
> including by attaching relevant information to identify the wallet-relying parties, and the wallet users’
> claims in machine-readable format.
>
> Note: The log kept by the Wallet Unit will be standardized and is machine-readable
> in order to enable data portability. An excerpt from this log therefore can be used to substantiate the report.

### 5.5 Discussions related to RPT_DPA_05

During the discussions with the delegated experts from the EU Member States the following
aspects related to **RPT_DPA_05** were discussed:

Based on the discussion it was agreed, that there shall be an additional HLR in Topic 19, which
specifies the technical details and the precise data format of the log and the possibilities for
the export of the data for the purpose of reporting.

The question was raised, whether the data from the log could be inserted in an attachment of an email
and that the other option would be that the wallet unit could itself become an email client. In any case
it would be possible to export this data into a file and attach this file to an email.
In order to make it easy for the user to submit such a report, the contact information of the DPA in charge
should be part of the log, if possible.

The issue was raised that the wallet unit can not be entirely sure, that the report was indeed sent
to the DPA and hence it is not entirely clear, whether it makes sense to log it.

Against this background it was decided to slightly revise the text of **RPT_DPA_05** as follows:

> A Wallet Unit SHALL log the **initiation of a** report sent to the DPA in a log file so that it can be presented to the User in the dashboard (as specified in Topic 19).

### 5.6 Additional high level requirement RPT_DPA_06

During the discussion of [RPT_DPA_01](#51-discussions-related-to-rpt_dpa_01) it was agreed to add
the following high level requirement as **RPT_DPA_06**:

>The Wallet Unit SHALL take the contact details of the DPA, which supervises the Relying Party,
> either (in this order) from
>> a) included in  the RPRC in the log entry,
>>
>> b) included in the RPAC in the log entry,
>>
>> c) looked up by the Wallet Unit from the RP Registry, based on the Subject of the RPAC in the log entry.
>
> The contact information includes  at least one of email address, phone number, or a URL of a webform.

## 6. Updated set of High Level Requirements 

### 6.1 Update for Topic 48 (Erasure of personal data at a wallet-relying party)

The updated set of high-level requirements after the discussion will give rise to an 
update of [Topic 48][topic-48]:

| **Index**              | **Requirement specification**                                                                                                                                                                                                                                                                                                     |
|------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| DATA_DLT_01            | A Wallet Provider SHALL ensure that its Wallet Units support the technical specifications mentioned in DATA_DLT_02, allowing a User to request from a Relying Party the erasure of their attributes that were presented by that Wallet Unit to that Relying Party, in accordance with **Article 17 of** Regulation (EU) 2016/679. |
| DATA_DLT_02            | The Commission SHALL, in cooperation with the Member States, develop technical specifications for a Wallet Unit interface allowing a Wallet Unit to send attribute deletion requests to Relying Parties with whom it has interacted in the past.                                                                                  |
| DATA_DLT_03            | A Wallet Instance SHALL provide a function where the User may select one Relying Party <s>**or multiple Relying Parties**</s> for which an attribute deletion request must be submitted.                                                                                                                                          |
| <s>**DATA_DLT_04**</s> | <s>**A Wallet Instance SHALL be able to display the attribute deletion requests previously submitted through the Wallet Unit.**</s>                                                                                                                                                                                               |
| DATA_DLT_05            | A Wallet Unit SHALL include attribute deletion requests in a log so they can be presented to the User via the dashboard (as specified in [Topic 19][topic-19]).                                                                                             |
| DATA_DLT_06            | The log SHALL **also document the initiation of a data deletion request and** include as a minimum: - Date **and time** of attribute deletion request, - Relying Party to which the request was made, - Attributes requested to be removed.                                                                                       |
| **DATA_DLT_07**        | **While the Wallet-Relying Party is responsible for choosing appropriate authentication mechanisms before executing a data deletion request, it is RECOMMENDED to use the authentication and signature facilities offered by the Wallet Solutions for this purpose.**                                                             |


### 6.2 Update for Topic 50 (Reporting a wallet-relying party to the competent data protection supervisory authority)

The updated set of high-level requirements after the discussion will give rise to an update of 
[Topic 50][topic-50]:

| **Index**             | **Requirement specification**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
|-----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| RPT_DPA_01            | **When prompted by the User, a Wallet Unit SHALL provide the contact details of the DPA, which supervises the Relying Party, if available, and SHALL make it easy for the User to send a report of allegedly unlawful or suspicious Relying Party presentation requests to this DPA. If these are not available, the Wallet Unit SHALL provide the contact details of the DPA of the region in which the Wallet Provider is residing. In addition, the Wallet Unit MAY also provide contact details of other DPAs taken from the "European Data Protection Board" website (<https://www.edpb.europa.eu/about-edpb/about-edpb/members_en>), and allow the User to choose a DPA to continue the reporting process.** |
| RPT_DPA_02            | The User interface enabling a User to start the process of **reporting a Wallet-relying Party to a DPA** SHALL be accessible via the log provided by the Wallet Unit.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| <s>**RPT_DPA_03**</s> | <s>**A Wallet Provider SHALL implement the interface in compliance with national procedural law and administrative practices.**</s>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| RPT_DPA_04            | **Wallet providers SHALL ensure that wallet units allow wallet users to substantiate the reports, including by attaching relevant information to identify the wallet-relying parties, and the wallet users’ claims in machine-readable format.</br> Note: The log kept by the Wallet Unit will be standardized and is machine-readable in order to enable data portability. An excerpt from this log therefore can be used to substantiate the report.**                                                                                                                                                                                                                                                         |
| RPT_DPA_05            | A Wallet Unit SHALL log the **initiation of a** report sent to the DPA in a log file so that it can be presented to the User in the dashboard (as specified in Topic 19).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **RPT_DPA_06**        | **The Wallet Unit SHALL take the contact details of the DPA, which supervises the Relying Party, either (in this order) from a) included in  the RPRC in the log entry, b) included in the RPAC in the log entry, c) looked up by the Wallet Unit from the RP Registry, based on the Subject of the RPAC in the log entry. </br> The contact information includes  at least one of email address, phone number, or a URL of a webform.**
