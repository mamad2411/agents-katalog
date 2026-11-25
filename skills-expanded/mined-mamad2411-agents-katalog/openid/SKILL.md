---
name: openid
description: "OpenID Foundation specs: every spec, maturity and errata, routed to the right family reference or dedicated skill. Use when a task names any OpenID Foundation specification or working group, or asks which one fits a use case: OpenID Connect (OIDC) Core, Discovery, Dynamic Client Registration, logout, prompt=create, Native SSO, SIOPv2, Key Binding; OpenID Federation; FAPI 1.0, FAPI 2.0, JARM, Grant Management, FAPI CIBA; CIBA and MODRNA; Shared Signals (SSF), CAEP, RISC; OpenID4VCI, OpenID4VP, HAIP, DCP, DCHP; AuthZEN Authorization API; eKYC and Identity Assurance (verified_claims); iGov; IPSIE; R&E; HEART; FastFed; EAP ACR values and Token Bound Authentication; legacy OpenID 2.0, Attribute Exchange, PAPE, Simple Registration and Yadis. Also use to check whether a spec is Final, an Implementer's Draft or a Draft, to find its errata set, to upgrade from an Implementer's Draft under the OpenID Foundation Process, or to find OpenID certification and conformance tests."
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.2.0"
  kind: standard
---

# OpenID Foundation specifications

The OpenID Foundation (OIDF) publishes identity specifications through working groups: OpenID Connect, OpenID Federation, FAPI, CIBA, Shared Signals, OpenID for Verifiable Credentials, AuthZEN, Identity Assurance and others. This skill is the index. It tells the agent which family a task belongs to, how mature each specification is, which revision and errata to pin, and whether a dedicated skill covers the family in depth.

**Follow the workflow below step by step.** Every fact here comes from a page in [Sources](#sources) or from the specification document linked in a reference file. When this skill and a source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps in Inputs.

## Inputs (fill in, or ask before starting)

- What is being built or reviewed: for example a relying party (RP), an OpenID Provider (OP), an authorization server, a resource server, a wallet, a credential issuer or verifier, a policy decision point, or a signal transmitter or receiver.
- Family: the working group or specification the task names, or the use case if it names none. Pick it with [Pick a family](#pick-a-family).
- Target version: the OpenID Foundation Process (current, Process Document v1.98) defines how every specification is versioned. Per specification, default to the Final at its latest errata set, else the newest Implementer's Draft; older Implementer's Drafts are read only to upgrade. Each family's own lines, legacy versions and previews are in its dedicated skill or family reference. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in the family reference, unless the user names another.
- Sources: when refreshing this skill or when a pin looks out of date, re-read every URL in [Sources](#sources), then every specification URL in the affected reference file. Compare titles, maturity sections and dates, update the reference entries and pins, and bump the version.

## Pick a family

1. Sign-in, ID Tokens, UserInfo, discovery, client registration or logout for users of a web or native app: **OpenID Connect** ([`references/connect.md`](references/connect.md)).
2. Trust between many parties through Trust Anchors, Entity Statements and Trust Chains: **OpenID Federation** ([`references/federation.md`](references/federation.md)).
3. High-security OAuth for open banking, open data or other regulated APIs: **FAPI** ([`references/fapi.md`](references/fapi.md)).
4. Authentication on a separate device, without a browser redirect: **CIBA** ([`references/modrna.md`](references/modrna.md)); with FAPI, also the FAPI CIBA profile in `fapi.md`.
5. Session revocation, risk and account events between services: **Shared Signals** ([`references/shared-signals.md`](references/shared-signals.md)).
6. Issuing or presenting verifiable credentials, wallets, SD-JWT VC or mdoc: **OpenID4VC** ([`references/dcp-openid4vc.md`](references/dcp-openid4vc.md)); for alignment with ISO presentation protocols, also [`references/dchp.md`](references/dchp.md).
7. A policy enforcement point asking a policy decision point for an access decision: **AuthZEN** ([`references/authzen.md`](references/authzen.md)).
8. Verified identity data with evidence and assurance metadata (`verified_claims`): **eKYC & IDA** ([`references/ekyc-ida.md`](references/ekyc-ida.md)).
9. Government or public-sector deployments: **iGov** ([`references/igov.md`](references/igov.md)). Enterprise SaaS and workforce identity profiles: **IPSIE** ([`references/ipsie.md`](references/ipsie.md)). Research and education: **R&E** ([`references/rande.md`](references/rande.md)).
10. Archived groups: health data (**HEART**, [`references/heart.md`](references/heart.md)), automated federation setup (**FastFed**, [`references/fastfed.md`](references/fastfed.md)), ACR values and Token Binding (**EAP**, [`references/eap.md`](references/eap.md)).
11. Community groups such as AI Identity Management: [`references/community-groups.md`](references/community-groups.md). OpenID 2.0 and other legacy or inactive documents: [`references/inactive-and-obsolete.md`](references/inactive-and-obsolete.md).

## Invariants

1. **Three maturity levels.** OpenID specifications go through Drafts, Implementer's Drafts and Final Specifications. Final Specifications are OpenID Foundation standards (Explore All Specifications). Pin the level and the exact document URL, not just the title.
2. **IPR protection depends on the level.** Implementer's Drafts and Final Specifications provide intellectual property protections to implementers; the index page names no such protection for Drafts (Explore All Specifications). The patent promise applies only to the working groups listed in the contribution agreements, not to all Foundation work (Contribution Agreements page, March 1, 2012 board affirmation).
3. **Approval is a member vote.** An Implementer's Draft has a 45-day review period and a Final a 60-day review period, each followed by a vote that needs a simple majority representing 20% of members (Developing an OpenID Standard).
4. **Default posture by level (this skill's recommendation, not an OIDF rule).** Build against a Final Specification and its latest errata set. Build against an Implementer's Draft only at the pinned ID revision, and expect breaking changes before Final. Track Working Group Drafts and editors' copies; do not ship interoperability promises on them.
5. **Errata replace the unversioned URL.** Several unversioned URLs now serve the errata edition, for example Connect Core, Discovery and Registration "incorporating errata set 2", JARM and Identity Assurance "incorporating errata set 1". The `-final` URL, where one exists, keeps the originally approved text. Cite which one you implement.
6. **Unversioned draft URLs move.** A URL such as `openid-connect-self-issued-v2-1_0.html` can serve a newer working draft than the last Implementer's Draft. For drafts, pin the `-ID<n>` or `-<nn>` URL.
7. **Index pages can disagree with the documents.** When a working group page and the document title differ (for example in errata set numbers), state both and follow the document. The reference files record the differences found on 2026-10-02.
8. **Certification exists.** The OIDF runs a free conformance suite and a self-certification programme with the "OpenID Certified" mark; some ecosystems require certification (Certification). Test guides exist for OpenID Connect OPs and RPs (including logout), FAPI 2 and FAPI 1 Advanced OPs, FAPI-CIBA, OpenID4VP, OpenID4VCI, the Shared Signals Framework and OpenID Federation (How to Certify Your Implementation).

## Workflow

1. **Identify the family.** Use [Pick a family](#pick-a-family) and the user's role.
   ✓ You can name the working group and the specifications in scope.
2. **Load the family reference.** Read only the reference for that family, plus any family it builds on (for example FAPI builds on OpenID Connect and OAuth; CAEP and RISC build on SSF).
   -> the reference file named in the [Reference index](#reference-index)
   ✓ Each specification in scope has an exact title, URL, maturity and date from the reference.
3. **Use the dedicated skill when one exists.** OpenID Connect, OpenID Federation, FAPI, CIBA, Shared Signals, OpenID4VC and AuthZEN have dedicated skills with normative detail. Install it and follow its workflow; this skill only routes.
   ✓ The dedicated skill is installed, or the reference confirms there is none.
4. **Pick and pin the version.** Choose the Final at its latest errata set, or the newest Implementer's Draft, then record the document URL, maturity level, date and errata set, and the posture from invariant 4.
   -> [`references/versions.md`](references/versions.md)
   ✓ The design or code cites a pinned URL, not only a title.
5. **Read the specification itself for normative rules.** The reference files summarise; requirements come from the specification text.
   ✓ Every MUST you implement cites a section of the pinned document.
6. **Plan conformance.** If the family has a conformance suite, plan to run it.
   ✓ The plan names the conformance test or states that none exists.
7. **Upgrade** (only when asked). Move an implementation from an Implementer's Draft to the Final, or to a later errata set, using the dedicated skill's upgrade steps where one exists.
   -> [`references/versions.md`](references/versions.md)
   ✓ The new pin is a Final or the newest Implementer's Draft, and the conformance tests pass against it.

## Verify before done

- [ ] Every OpenID specification in the design is named by its exact title, URL, maturity level and date.
- [ ] Finals are pinned with their latest errata set, or the reason for the original text is stated.
- [ ] No Working Group Draft is presented as a standard, and Implementer's Drafts are pinned by their `-ID<n>` URL.
- [ ] Specifications from archived working groups (EAP, FastFed, HEART) or inactive and obsolete lists are flagged as such.
- [ ] Where a dedicated skill exists, it was installed and its checklist was run.
- [ ] Conformance testing is planned where the OIDF offers it.

## Reference index

- **`references/versions.md`**: the OpenID Foundation Process: the five stages, draft and Implementer's Draft numbering, errata sets, review periods and votes, how to pick and upgrade a version of any OpenID specification, and where each family's version lines live.
- **`references/connect.md`**: AB/Connect: Core, Discovery, Registration, RP Metadata Choices, response types, Form Post, Migration, logout specs, `unmet_authentication_requirements`, `prompt=create`, Native SSO, SIOPv2, Key Binding, drafts and implementer's guides.
- **`references/federation.md`**: OpenID Federation 1.0 and 1.1, Federation for OpenID Connect 1.1, extensions and drafts.
- **`references/fapi.md`**: FAPI 1.0 Baseline and Advanced, FAPI 2.0 Security Profile, Attacker Model, Message Signing, JARM, FAPI CIBA, Grant Management, HTTP Signatures.
- **`references/modrna.md`**: CIBA Core, MODRNA Authentication Profile, Account Porting, User Questioning API, MODRNA drafts.
- **`references/shared-signals.md`**: SSF, CAEP, RISC, CAEP Interoperability Profile.
- **`references/dcp-openid4vc.md`**: OpenID4VCI, OpenID4VP, HAIP, security and trust, OpenID4VP over BLE.
- **`references/dchp.md`**: Digital Credentials Harmonized Presentation working group.
- **`references/authzen.md`**: Authorization API 1.0, COAZ, Access Request and Approval, Obligations.
- **`references/ekyc-ida.md`**: Identity Assurance, Schema Definition, Claims Registration, errata, Authority, ASC, Attachments, Identity Proofing Extension.
- **`references/igov.md`**, **`references/ipsie.md`**, **`references/rande.md`**: public sector, enterprise and research and education profiles.
- **`references/heart.md`**, **`references/fastfed.md`**, **`references/eap.md`**: archived working groups.
- **`references/community-groups.md`**: active and archived community groups.
- **`references/inactive-and-obsolete.md`**: Account Chooser, Native Applications, OpenID Authentication 1.x and 2.0 and its extensions, Yadis, Contract Exchange.

## Related skills

Install the dedicated family skills by name:

- `openid-connect`: `npx skills add ScaleDockHQ/scaledock-skills --skill openid-connect`
- `openid-federation`: `npx skills add ScaleDockHQ/scaledock-skills --skill openid-federation`
- `fapi`: `npx skills add ScaleDockHQ/scaledock-skills --skill fapi`
- `ciba`: `npx skills add ScaleDockHQ/scaledock-skills --skill ciba`
- `shared-signals`: `npx skills add ScaleDockHQ/scaledock-skills --skill shared-signals`
- `openid4vc`: `npx skills add ScaleDockHQ/scaledock-skills --skill openid4vc`
- `authzen`: `npx skills add ScaleDockHQ/scaledock-skills --skill authzen`

## Sources

Status uses the publishing body's own maturity term; these are index pages, so the status is Index. Checked is the date the source was last read. Individual specification URLs, with their maturity and dates, are in the reference files.

- [Explore All Specifications](https://openid.net/developers/specs/): Index, as of 2026-10-02, checked 2026-10-02.
- [AB/Connect Working Group – Specifications](https://openid.net/wg/connect/specifications/): Index, as of 2026-10-02, checked 2026-10-02.
- [AuthZEN – Specifications](https://openid.net/wg/authzen/specifications/): Index, as of 2026-10-02, checked 2026-10-02.
- [Digital Credentials Protocols (DCP) Working Group – Specifications](https://openid.net/wg/digital-credentials-protocols/specifications/): Index, as of 2026-10-02, checked 2026-10-02.
- [Digital Credentials Harmonized Presentation Working Group – Specifications](https://openid.net/wg/digital-credentials-harmonized-presentation-working-group/specifications/): Index, as of 2026-10-02, checked 2026-10-02.
- [eKYC & IDA Working Group – Specifications](https://openid.net/wg/ekyc-ida/specifications/): Index, as of 2026-10-02, checked 2026-10-02.
- [FAPI Working Group – Specifications](https://openid.net/wg/fapi/specifications/): Index, as of 2026-10-02, checked 2026-10-02.
- [iGov Working Group – Specifications](https://openid.net/wg/igov/specifications/): Index, as of 2026-10-02, checked 2026-10-02.
- [IPSIE – Specifications](https://openid.net/wg/ipsie/specifications/): Index, as of 2026-10-02, checked 2026-10-02.
- [MODRNA Working Group – Specifications](https://openid.net/wg/modrna/specifications/): Index, as of 2026-10-02, checked 2026-10-02.
- [R&E Working Group – Specifications](https://openid.net/wg/rande/specifications/): Index, as of 2026-10-02, checked 2026-10-02.
- [Shared Signals Working Group – Specifications](https://openid.net/wg/sharedsignals/specifications/): Index, as of 2026-10-02, checked 2026-10-02.
- [EAP Working Group – Specifications](https://openid.net/wg/eap/specifications/): Index, as of 2026-10-02, checked 2026-10-02.
- [FastFed Working Group – Specifications](https://openid.net/wg/fastfed/specifications/): Index, as of 2026-10-02, checked 2026-10-02.
- [HEART Working Group – Specifications](https://openid.net/wg/heart/specifications/): Index, as of 2026-10-02, checked 2026-10-02.
- [Archived Groups](https://openid.net/wg/archived-groups/): Index, as of 2026-10-02, checked 2026-10-02.
- [Community Groups](https://openid.net/cg/): Index, as of 2026-10-02, checked 2026-10-02.
- [The OpenID Process](https://openid.net/foundation/openid-process-document/): Published, OpenID Process Document v1.98 (19 October 2024), checked 2026-10-05.
- [Developing an OpenID Standard](https://openid.net/foundation/developing-openid-standards/): Index, as of 2026-10-02, checked 2026-10-02.
- [OpenID Foundation Contribution Agreements](https://openid.net/intellectual-property/openid-foundation-contribution-agreements/): Index, as of 2026-10-02, checked 2026-10-02.
- [Certification](https://openid.net/certification/): Index, as of 2026-10-02, checked 2026-10-02.
- [How to Certify Your Implementation](https://openid.net/certification/how-to-certify-your-implementation/): Index, as of 2026-10-02, checked 2026-10-02.
