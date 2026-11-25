---
name: takedown
description: >
  Draft a Copyright Ordinance (Cap 528) takedown notice under ss. 88-91
  (online service provider liability), triage one you received, or draft a
  response notice. Use when asserting copyright through a Cap 528 s. 88
  takedown with the fair-dealing and good-faith gates, when an incoming
  takedown needs triage into comply / counter / engage / ignore options,
  or when drafting a response notice under s. 91.
argument-hint: "<--send | --respond | --counter> [context or path to incoming notice]"

---
# /takedown

> **HK adaptation note:** This skill adapts the US DMCA notice-and-takedown
> framework for Hong Kong under the Copyright Ordinance (Cap 528). HK's
> framework for online service provider (OSP) liability is found in Division 5
> of Cap 528 (ss. 88-91), which provides safe harbour for OSPs that comply with
> takedown requirements. As HK does not have a US-style counter-notice mechanism
> (s. 91 merely requires OSPs to restore material if the complaining party does
> not seek a court order within 14 days of being notified), the options differ.
> Fair dealing in HK (ss. 38-44) is a closed list of specific exceptions, not
> the open-ended US fair use doctrine.

Three modes. Pick one:

- `/ip-legal:takedown --send` — draft a Cap 528 s. 88 takedown notice to an OSP.
  Fair-dealing gate (*HK Cable v OFTA* principles) + good-faith gate before delivery.
- `/ip-legal:takedown --respond` — triage a takedown you received. Options:
  comply / negotiate / seek legal advice on whether fair dealing applies.
- `/ip-legal:takedown --counter` — prepare a response to the OSP asserting that the
  material was removed by mistake or misidentification (similar to a DMCA
  counter-notice but without a formal statutory mechanism in HK; the OSP may
  restore material if the original complainant does not seek a CFI injunction
  within 14 days under s. 91).
---

# /takedown

Three modes. Pick one:



## Instructions

1. **Read the practice profile.** Load `~/.claude/plugins/config/claude-for-hk-law/ip-legal/CLAUDE.md`. If it contains `[PLACEHOLDER]` markers or does not exist, stop and say: "This plugin needs setup before it can give you useful output. Run `/ip-legal:cold-start-interview` — the takedown skill depends on your approval matrix and practice profile."

2. **Check matter workspaces.** Per `## Matter workspaces`: if `Enabled` is `✗`, skip. If enabled and there is no active matter, ask: "Which matter is this for? Run `/ip-legal:matter-workspace switch <slug>` or say `practice-level`."

3. **Dispatch on `$ARGUMENTS`:**
   - `--send` → run send mode (below). Walk identify-the-work, identify-the-infringing-material, fair-dealing gate, good-faith belief, draft the Cap 528 s. 88 notice, run the loud gate, write output.
   - `--respond` → run respond mode (below). Read the incoming notice, assess (license, fair dealing, defects, host s. 88-91 compliance, sender credibility), present the options, recommend, write the triage memo.
   - `--counter` → run counter mode (below). Confirm the predicate (taken down in response to a s. 88 notice, good-faith belief of mistake/misidentification, ready for CFI jurisdiction), prepare the response notice, run the loud gate, write output.
   - No flag → ask once: "Are we sending a Copyright Ordinance takedown, triaging one we received, or preparing a response?"

4. **Respect the gates.** In `--send` and `--counter`, the loud gate runs before any final output is written. The fair-dealing gate in `--send` is separate and runs earlier; if fair dealing applies under Cap 528 ss. 38-44, stop the draft and route to attorney review.

5. **Jurisdiction note.** Cap 588 s. 88-91 is HK law. If the service provider, content, or infringer sits outside HK, flag before drafting — you may need an EU DSA notice, UK OSA notice, DMCA notice, or local-regime instrument instead of (or in addition to) a Cap 528 notice.

6. **Hand off where appropriate.** `--respond` with a response recommendation chains into `/ip-legal:takedown --counter` — but only after the triage memo has been reviewed and the decision to counter has been made deliberately.

## Examples

```
/ip-legal:takedown --send
/ip-legal:takedown --respond ~/Downloads/takedown-notice.pdf
/ip-legal:takedown --counter
/ip-legal:takedown
```

## Notes

- The outgoing takedown notice does not carry the work-product header. Internal drafts, fair-dealing analyses, and triage memos do.
- Cap 528 ss. 88-91 set out specific requirements for OSP safe harbour — every element must be present for the notice to trigger the OSP's obligation to act.
- HK does not have statutory damages for copyright infringement. Remedies in the CFI include injunctions, damages, and account of profits.
- Non-lawyer users get a one-page brief for the attorney conversation before the gate clears.

---

## Purpose

HK's Copyright Ordinance (Cap 528) ss. 88-91 provide a safe harbour framework for online service providers (OSPs). An OSP that complies with the takedown and restoration requirements is not liable for copyright infringement by its users. A takedown notice under s. 88 is a statement made in good faith that triggers the OSP's obligation to remove or disable access to allegedly infringing material. The OSP must restore the material if, within 14 days of being notified by the OSP of the takedown, the complaining party does not seek a court order for continued removal (s. 91). This is not a counter-notice mechanism in the US DMCA sense — it rests on the complainant's failure to obtain an injunction. This skill handles the takedown, response, and legal escalation options.

Three modes:

- `--send` — draft a Cap 528 s. 88 takedown notice to an OSP
- `--respond` — triage a takedown someone sent you; produce options
- `--counter` — prepare a response asserting mistake/misidentification, with the 14-day injunction watch window under s. 91

If the user does not pass a flag, ask once: "Are we sending a Copyright Ordinance takedown, triaging one we received, or preparing a response?"

> **External deliverables (send and counter modes):** the outgoing notice goes to the OSP's designated contact. Do NOT include the `PRIVILEGED & CONFIDENTIAL — ATTORNEY WORK PRODUCT` header on the outgoing document. The notice itself is not privileged. Internal drafts, pre-send briefs, fair-dealing analyses, and triage memos keep the header per plugin config `## Outputs`.

## Jurisdiction assumption

Cap 528 ss. 88-91 are **HK law**. They apply to OSPs operating in HK, or OSPs that provide services to HK users. Other jurisdictions have their own notice-and-action regimes — US DMCA §512, EU Digital Services Act Art. 16, UK Online Safety Act, etc. — that differ materially. If the OSP, content, or infringer sits outside HK, flag it — a Cap 528 notice may be the wrong instrument. Copyright subsistence itself is Berne-multilateral, but enforcement mechanics are jurisdiction-specific.

## Load context

- `~/.claude/plugins/config/claude-for-hk-law/ip-legal/CLAUDE.md` → `## IP practice profile` (copyright registrations if any), `## Enforcement posture` → `Approval matrix → Cap 528 takedown (ordinary)` row, `## Outputs` (work-product header, role), `## Who's using this` (role — lawyer vs. non-lawyer)
- **Matter context.** Check `## Matter workspaces` in the practice-level CLAUDE.md. If `Enabled` is `✗` (in-house default), skip matter machinery. If enabled and no active matter, ask: "Which matter? Run `/ip-legal:matter-workspace switch <slug>` or say `practice-level`." Write outputs to the active matter's folder at `~/.claude/plugins/config/claude-for-hk-law/ip-legal/matters/<matter-slug>/takedown/<slug>/` (or `takedown/<slug>/` at practice level). Never read another matter's files unless `Cross-matter context` is `on`.

## Send mode — drafting a Cap 528 s. 88 takedown notice

### Step 1: Identify the copyrighted work

> What is the copyrighted work?
>
> - **Title / description** — what is the work (software, image, text, video, audio)?
> - **Registration status** — US Copyright Office registration number and date (if any). Registration is NOT required to send a takedown, but it is required to file suit on a US work and its pre-infringement timing controls statutory damages and fees.
> - **Ownership** — do we own it outright, or hold an exclusive license with takedown authority? (Non-exclusive licensees typically cannot send takedowns on the licensor's work.)
> - **Prior licensing** — have we ever licensed this use, or a broader use that might cover it?

Ownership and authority are critical. HK has no equivalent of §512(f) but bad-faith notices can still expose the sender to liability for wrongful interference or tortious misrepresentation.

### Step 2: Identify the infringing material and its location

> Where is the infringing material?
>
> - **Platform / service provider** — YouTube, Twitter/X, GitHub, Reddit, Amazon, a web host, etc.
> - **URL(s)** — specific permalinks to the infringing material. One notice can cover multiple URLs if they're all from the same service.
> - **Description** — what is the infringing material and how does it infringe (verbatim copy, substantially similar, derivative)?
> - **Screenshots / evidence** — preserved with timestamp and URL visible

Under Cap 528 s. 88(2)(b), the notice must contain sufficient information to enable the OSP to identify and locate the material. URLs alone are usually enough; be precise.

### Step 3: Fair-dealing gate

HK's Copyright Ordinance (Cap 528) has a closed list of fair dealing exceptions (ss. 38-44). Unlike the US open-ended fair use doctrine, HK's fair dealing only applies to specific purposes: research and private study (s. 38), criticism, review, and news reporting (s. 39), and education (s. 41). The factors under s. 38(3) (for research/private study) are:
1. **Purpose of the dealing** — non-commercial research, private study
2. **Nature of the work** — published or unpublished
3. **Amount and substantiality** — how much of the work is used
4. **Effect on the potential market** — does the dealing harm the copyright owner's interests

For criticism, review, and news reporting under s. 39, the dealing must be accompanied by sufficient acknowledgement.

Assess:

> Does the allegedly infringing use fall within one of the specific fair dealing categories under Cap 528 (ss. 38-44)?
> - Research or private study (s. 38)?
> - Criticism, review, or news reporting (s. 39)?
> - Educational purposes by an educational establishment (s. 41)?
> - Any other specific exception?

If the use clearly falls within a fair dealing exception, do not draft. Stop and route to attorney review: "The use appears to fall within a fair dealing exception under Cap 528 [s. X]. Sending a takedown for a use protected by fair dealing may expose the sender to liability. Route this to counsel."

Note: HK's fair dealing is narrower than US fair use. Many uses that would be "fair use" in the US (e.g., transformative or non-commercial uses that do not fit into the closed list) are not fair dealing in HK.

### Step 4: Good-faith belief

Under Cap 528 s. 88(2)(c), a takedown notice must include a statement that the complainant has a good faith belief that the use of the material is not authorised by the copyright owner, its agent, or the law.

The sender forms this belief on the record. Have they:

- Confirmed the work is theirs (or they have takedown authority via exclusive licence)?
- Confirmed the use is not licensed (no prior deal, no implied licence, no Creative Commons grant that would cover it)?
- Considered fair dealing (Step 3)?
- Reviewed the accused content directly (not just a report about it)?

If yes on all four, the good-faith belief is colour-able. If no on any, pause.

### Step 5: Accuracy and authority

Cap 528 s. 88(2)(d) requires a statement that the information in the notice is accurate and that the complainant has authority to act on behalf of the copyright owner.

While HK law does not use the same "penalty of perjury" language as the US DMCA, the statement must still be made in good faith. A false or misleading notice may expose the sender to civil liability (wrongful interference, tortious misrepresentation).

Confirm signer: who is sending this on behalf of whom, and do they have authority to do so?

### Step 6: Draft the notice

Cap 528 s. 88(2) elements — the notice must include:

1. **Identity of the copyright owner or exclusive licensee** — full legal name and contact details
2. **Identification of the copyrighted work** — "Copyrighted work: [title, description]" (no registration required in HK)
3. **Identification of the infringing material** with location information — "Infringing material: [URL(s), description, how it infringes]"
4. **Statement of good faith belief** — "I have a good faith belief that use of the material is not authorised by the copyright owner, its agent, or the law."
5. **Accuracy and authority statement** — "The information in this notice is accurate and I am authorised to act on behalf of the copyright owner."
6. **Signature** (physical or electronic)

Structure:

- Sender address block / date
- Recipient: designated contact at [service provider]
- Subject: Notice of Copyright Infringement under Cap 528 s. 88
- The elements above, numbered or clearly set apart
- Signature line

Most service providers publish a preferred form or web intake. The skill produces the notice content; the user submits through the provider's path. Note in the output which intake path is expected for the named service provider.

### Step 7: The loud gate before delivery

```
┌─────────────────────────────────────────────────────────────┐
│  BEFORE THIS TAKEDOWN GOES ANYWHERE                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  A Cap 528 s. 88 takedown notice is a legal statement that  │
│  triggers the OSP's obligation to remove or disable access  │
│  to material. Making a false or misleading statement in a   │
│  notice can expose the sender to civil liability.           │
│                                                             │
│  • Making a false or misleading notice may expose the       │
│    sender to liability for wrongful interference, tortious  │
│    misrepresentation, or abuse of process under HK common   │
│    law. HK does not have a direct equivalent of US §512(f)  │
│    but a bad-faith notice is not risk-free.                 │
│                                                             │
│  • The good faith belief and accuracy statements are        │
│    material representations. They are not formalities.      │
│                                                             │
│  • Sending a takedown on material that is in fact           │
│    licensed, owned by someone else, or protected by fair    │
│    dealing exposes the sender to counterclaims.             │
│                                                             │
│  Confirm before the notice leaves:                          │
│                                                             │
│    1. You own the copyright, or you hold an exclusive       │
│       licence with takedown authority.                      │
│    2. The accused use is not authorised — you have          │
│       checked licences, grants, and any prior consents.     │
│    3. You considered fair dealing under Cap 528 ss. 38-44   │
│       (see Step 3 of this draft); your conclusion is on     │
│       the record.                                           │
│    4. Whoever has authority to sign approves sending.       │
│                                                             │
│  Approver per your practice profile: [approver from         │
│  Enforcement posture → Approval matrix → Cap 528 takedown   │
│  (ordinary) row]                                            │
│                                                             │
│  Automatic escalations that apply here: [list any from      │
│  the practice profile that this matter triggers]            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

If the user is a non-lawyer (per `## Who's using this`), add:

> A Cap 528 s. 88 takedown notice is a legal statement that triggers removal of material. Making a false or misleading statement may expose the sender to civil liability in the CFI. Have you reviewed this with a Hong Kong solicitor or barrister? If not, here's a brief to bring to them: [generate a short summary: work, ownership, accused use, licensing check, fair-dealing analysis, signer, service provider].
>
> If you need to find a licensed HK solicitor: the Law Society of Hong Kong maintains a referral service (https://www.hklawsoc.org.hk). For barristers, the Hong Kong Bar Association (https://www.hkba.org). For individual creators and small businesses, the law clinics at HKU and CUHK may provide pro bono advice.

Do not write the final output without explicit engagement with the gate.

### Step 8: Output

**Primary:** `<matter-folder>/takedown/<slug>/notice-v<N>.md` — the notice content, ready to paste into the service provider's Cap 528 intake form or send to its designated contact.

**In-chat:** show the notice as plain text for review before writing. Iterate before committing to disk.

**Reviewer-facing closing note** (in the in-chat preview only):

> This is a draft Cap 528 s. 88 notice for attorney review, not a notice ready to send. A licensed HK solicitor or barrister reviews, edits, and takes professional responsibility before submission. Do not send this unreviewed.

**Citation verification.** Any case or statutory citation included must be verified on a legal research tool. Source-tag each — `[Westlaw Asia]`, `[HKLII]`, `[HK e-Legislation]`, `[user provided]`, `[model knowledge — verify]`, `[web search — verify]`. Citations tagged `verify` get checked first.

**Post-send record.** After submission, write `<matter-folder>/takedown/<slug>/submission.md`: service provider, designated contact used, date submitted, confirmation ID if returned, URLs targeted, 14-day injunction watch window under s. 91, legal hold refreshed.

## Respond mode — triaging a takedown you received

Your content was taken down. A service provider has notified you of a Cap 528 s. 88 notice. You have options.

### Step 1: Read the notice you received

Extract:

- **Sender** — entity, signer, address, email
- **Service provider** — who notified you (the platform)
- **Claimed work** — what they say is theirs
- **Your content alleged to infringe** — URL(s) or identifiers as they named them
- **Date of takedown / notice**
- **Whether the notice appears to meet s. 88(2) requirements** — flag missing elements; a defective notice may not trigger the OSP's obligation to act

### Step 2: Assess

- **Do we have a licence?** Negotiated, implied, Creative Commons, prior settlement, assignment — anything that authorises the use.
- **Does fair dealing apply?** Walk the Cap 528 ss. 38-44 factors. HK's fair dealing is a closed list — check if the use falls within a specific exception.
- **Is the notice defective?** Missing any s. 88(2) elements? A defective notice reduces the OSP's safe harbour obligation.
- **Did the host comply properly with s. 91?** Were we given a reasonable opportunity to respond? If not, that is a separate issue with the host.
- **Is the sender a troll?** Repeat pattern of overbroad takedowns?

### Step 3: Options

Present options with tradeoffs:

**A — Comply (let the takedown stand)**
- When: they're right, or the fight isn't worth it
- Tradeoff: content stays down; may affect SEO, accounts with strikes policies
- Next step: log the event, move on

**B — Respond to the OSP asserting mistake/misidentification** (s. 91 process)
- When: we have a good-faith belief the material was misidentified or removed by mistake — licence, fair dealing, or the sender doesn't own the work
- Tradeoff: Under s. 91, if within 14 days the OSP notifies us of the takedown and we respond asserting good faith belief of mistake/misidentification, the OSP must notify the complainant. If the complainant does not seek a CFI injunction within 14 more days, the OSP must restore the material. This is NOT a counter-notice that consents to jurisdiction — it's a statutory restoration mechanism.
- Next step: `/ip-legal:takedown --counter`

**C — Engage the sender directly**
- When: there's room for a business resolution (licence, credit, takedown of a narrower portion)
- Tradeoff: content stays down during negotiations
- Next step: outreach letter to the sender

**D — Ignore and let it stand**
- When: the harm is small and we'd rather deal with the sender separately
- Tradeoff: content stays down; consider whether the sender has made a false statement that could ground a claim

Recommend one with two sentences of rationale.

### Step 4: Write triage memo

Output: `<matter-folder>/takedown/inbound/<slug>/triage.md`.

```markdown
[WORK-PRODUCT HEADER — per plugin config ## Outputs]

> **Privilege inheritance.** This triage records our first-pass assessment of an adverse takedown. It is confidential and potentially privileged — not to be shared outside the legal review chain.

# Cap 528 Takedown Received — Triage

> **READ FOR TRIAGE, NOT OPINION.** Structured intake scan, not a legal merit opinion. Every authority flagged for SME verification; every merit call is counsel's.

**Slug:** [slug]
**Received:** [YYYY-MM-DD]
**Service provider:** [platform]
**Incoming file:** [path]

## The notice

**Sender:** [entity, signer, counsel if any]
**Claimed work:** [title, description]
**Our content targeted:** [URLs / identifiers]
**Date of takedown:** [YYYY-MM-DD]
**Notice meets Cap 528 s. 88(2) requirements:** [yes / no — list any missing elements]

## Assessment

**Licence / authorization check:** [read]
**Fair dealing assessment (Cap 528 ss. 38-44):** [read — which exception applies?]
**Notice defects:** [list or none]
**Host compliance with s. 91:** [were we given notice and opportunity to respond]
**Sender credibility:** [troll / real claimant / repeat takedown pattern]

## Options

### A. Comply
### B. Respond to OSP (s. 91 process)
### C. Engage sender
### D. Ignore

**Recommendation:** [A/B/C/D] — [two sentences why] — `[SME VERIFY: counsel to confirm before executing]`

## Deadlines

- **14-day OSP notification window:** [date by which OSP must notify complainant]
- **14-day injunction watch window:** after complainant notified — if no CFI injunction sought, content restored

## Immediate actions

- [ ] Legal hold issued on the accused work and our related content — [yes/no]
- [ ] Business impact assessed (revenue, account strikes, SEO) — [yes/no]
- [ ] Matter created in log — [yes/no/TBD]
- [ ] Counsel assigned — [who]
```

Close the in-chat presentation with:

> This is a triage memo, not advice. The assessments above are a first read from the four corners of the notice. An attorney evaluates before you respond to the OSP or decide not to act.

## Counter mode — preparing a response under Cap 528 s. 91

Under Cap 528 s. 91, if the OSP notifies you that your content was removed in response to a takedown notice, you may assert a good faith belief that the material was removed by mistake or misidentification. If you do so, the OSP must notify the original complainant. If within 14 days the complainant does not seek a CFI injunction, the OSP must restore the material.

### Step 1: Confirm the predicate

- The content was taken down in response to a Cap 528 s. 88 notice (not a terms-of-service action by the host).
- You have a good-faith belief the material was removed by mistake or misidentification.
- You understand that if the complainant seeks a CFI injunction, the content stays removed pending the court's determination.

### Step 2: Draft the response

The response should include:

1. **Your identification** — name, address, contact information
2. **Identification of the material removed** and its location before removal (URL)
3. **Statement of good faith belief** that the material was removed by mistake or misidentification
4. **Signature** (physical or electronic)

Structure:

- Your address block / date
- Recipient: designated contact at the service provider (same that received the original s. 88 notice)
- Subject: Response to Copyright Takedown pursuant to Cap 528 s. 91
- The elements above, numbered or clearly set apart
- Signature line

### Step 3: The loud gate before delivery

```
┌─────────────────────────────────────────────────────────────┐
│  BEFORE THIS RESPONSE GOES ANYWHERE                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  A Cap 528 s. 91 response asserts that the material was     │
│  removed by mistake or misidentification. It sets the       │
│  14-day clock for the complainant to seek a CFI injunction. │
│                                                             │
│  • If the complainant files for an injunction in the CFI    │
│    within 14 days, the content stays down pending the       │
│    court's decision.                                        │
│                                                             │
│  • If they do not seek an injunction within 14 days, the    │
│    OSP must restore the material.                           │
│                                                             │
│  • Making a false or misleading statement in the response   │
│    may expose you to liability.                             │
│                                                             │
│  Confirm before the response leaves:                        │
│                                                             │
│    1. The material was removed in response to a Cap 528     │
│       s. 88 notice (not a TOS action).                      │
│    2. You have a good-faith belief the removal was a        │
│       mistake or misidentification — because the use is     │
│       licensed, protected by fair dealing (Cap 528          │
│       ss. 38-44), not actually infringing, or the sender    │
│       doesn't own the work.                                 │
│    3. An attorney has reviewed this before it is sent.      │
│                                                             │
│  Approver per your practice profile: [approver from         │
│  Enforcement posture → Approval matrix]                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

If the user is a non-lawyer:

> A s. 91 response is a legal statement. Have you reviewed with a licensed HK solicitor or barrister? If not, here's a brief for the conversation: [generate a 1-page summary]. The Law Society of Hong Kong maintains a referral service (https://www.hklawsoc.org.hk).

### Step 4: Output

**Primary:** `<matter-folder>/takedown/<slug>/response-v<N>.md` — the response content, ready to submit via the service provider's intake.

**In-chat:** present as plain text for review before committing.

**Post-submission record.** After submission, write `<matter-folder>/takedown/<slug>/submission.md`: service provider, date submitted, 14-day CFI injunction watch window calendared, plan if content is restored, plan if injunction is sought.

## Decision posture

Per `## Decision posture on subjective legal calls` in the practice profile: when uncertain whether the use is fair dealing, whether the rights holder is us, whether the work is actually ours — do not silently decide. HK fair dealing is a closed list; flag for attorney review. Sending a takedown or a response on an assumption is a one-way door.

## What this skill does not do

- **Submit the notice.** Drafting only. The user submits through the service provider's designated channel.
- **Pick a service provider's intake form for the user.** Notes which path is expected; does not auto-submit.
- **Decide fair dealing.** Assesses the closed list of Cap 528 ss. 38-44; flags. An attorney decides.
- **Validate the sender's claim on the receive side.** Structured read; every authority flagged for SME verification.
- **Bypass the gate.** The gate runs every time in `--send` and `--counter` modes.
- **Invent citations.** Any cites included are source-tagged and flagged for verification.
- **Handle non-HK regimes.** Cap 528 is HK-specific. For US DMCA, EU DSA, UK OSA, and other regimes — flag and route.
