---
name: "arf-topic-h-transaction-logs-part-2"
description: "Use when implementing transaction logging in the Wallet Unit. Covers log content, retention, access control, and privacy requirements for wallet transaction records. Part 2: covers 4.7 Topic 30 - Interaction between Wallet Units, 4.8 Topic 40 - Wallet Instance installation and Wallet Unit activation and management, 5 Relation to Other Topics ...."
sections:
  - "4.7 Topic 30 - Interaction between Wallet Units"
  - "4.8 Topic 40 - Wallet Instance installation and Wallet Unit activation and management"
  - "5 Relation to Other Topics"
  - "5.1 Changes to other topics"
  - "5.2 Relation to Risk Register (tbd)"
  - "6 Additions and Changes to the ARF"
  - "7 References"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~1195 -->

## 4.7 Topic 30 - Interaction between Wallet Units

| **Index** | **Requirement specification** | **Proposal** |
|-----------|-------------------------------|--------------|
|  W2W_08   | Wallet Providers SHALL ensure that a Wallet Unit provides a log of transactions related to Wallet-to-Wallet transactions, allowing the User to view the history of the presentation requests and responses (sent or received respectively, depending on the role of a Wallet Unit in a transaction). |   New requirement  |

## 4.8 Topic 40 - Wallet Instance installation and Wallet Unit activation and management

| **Index** | **Requirement specification** | **Proposal** |
|-----------|-------------------------------|--------------|
|  WIAM_12a   | The Wallet Unit SHALL ensure that the Wallet Provider cannot access the contents of the Wallet Unit, in particular to learn a) which attestations are present on the Wallet Unit, b) the status of these attestations, c) the value of attributes in these attestations, and d) the contents of the Wallet Unit log meant in DASH_02. |   New requirement  |

## 5 Relation to Other Topics

### 5.1 Changes to other topics

This topic is related to Topic N - Export and Data Portability. Some further changes to DASH_02 have been proposed, on top of the proposal resulting from the discussion on Topic N. The final wording of the DASH_02 will be thus as proposed in this paper.

Other changes to HLRs related to transaction logs topic proposed in the Topic N Discussion Paper, are valid and remain unchanged.

### 5.2 Relation to Risk Register (tbd)

The risk register for European Digital Identity Wallets \[RiskRegister\]
contains the following risks that are related to the Relying Party registration:

|Risk type | Risk id | Related risk titles|
|-------------|-------|-------------------|

More specifically, \[RiskRegister\]  describes the following threats to a Wallet:

|ID | Threat description | Related risks |
|---------|-------|-------------------|

## 6 Additions and Changes to the ARF

See sections 4 and 5 above. In addition, transactional data related aspects in the main text of the ARF will be updated accordingly.

## 7 References

| Reference                              | Description                                                  |
|----------------------------------------|--------------------------------------------------------------|
| [ARF_DevPlan]                          | Architecture and Reference Framework Development plan 2025, European Commission, v1.0 |
| [RiskRegister]                         | Annex 1 to the Commission Implementing Regulation laying down rules for the application of Regulation (EU) No 910/2014 of the European Parliament and of the Council as regards the certification of the European Digital Identity Wallets, European Commission, October 2024, draft |
| [Topic 11][topic-11]                             | Topic 11 - Pseudonyms  |
| [Topic 16][topic-16]                             | Topic 16 - Signing documents with a Wallet Unit |
| [Topic 19][topic-19]                             | Topic 19 - User navigation requirements (Dashboard logs for transparency)  |
| [Topic 34][topic-34]                             | Topic 34 - Migrate to a different Wallet Solution  |
| [Topic 48][topic-48]                             | Topic 48 - Blueprint for requesting data deletion to Relying Parties |
| [Topic 50][topic-50]                             | Topic 50 - Blueprint to report unlawful or suspicious request of data |
| [RiskRegister]                         | [Annex 1 to the Commission Implementing Regulation laying down rules for the application of Regulation (EU) No 910/2014 of the European Parliament and of the Council as regards the certification of the European Digital Identity Wallets, European Commission, October 2024, draft](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402981#anx_I) |
| [European Digital Identity Regulation] | [Regulation (EU) 2024/1183 of the European Parliament and of the Council of 11 April 2024 amending Regulation (EU) No 910/2014 as regards establishing the European Digital Identity Framework](https://eur-lex.europa.eu/eli/reg/2024/1183/oj/eng) |
| [CIR 2024/2979]                      | [Commission Implementing Regulation (EU) 2024/2979 of 28 November 2024 laying down rules for the application of Regulation (EU) No 910/2014 of the European Parliament and of the Council as regards the integrity and core functionalities of European Digital Identity Wallets](https://eur-lex.europa.eu/eli/reg_impl/2024/2979/oj/eng)) |
|  [GDPR]                              | [Regulation (EU) 2016/679 of the European Parliament and of the Council of 27 April 2016 on the protection of natural persons with regard to the processing of personal data and on the free movement of such data, and repealing Directive 95/46/EC (General Data Protection Regulation)](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng) |
| [OID4VP] | [OpenID for Verifiable Presentations](https://github.com/eu-digital-identity-wallet/eudi-doc-standards-and-technical-specifications/issues/2) |
| [ISO/IEC - 18013-5]   |  [Mobile driving licence (mDL) application](https://github.com/eu-digital-identity-wallet/eudi-doc-standards-and-technical-specifications/issues/84) |
