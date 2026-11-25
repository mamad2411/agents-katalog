---
name: client-intake
description: >
  Structured intake — practice-area templates, cross-area issue spotting,
  conflict flags, and triage classification. Produces a formatted case summary
  the student analyzes and the professor reviews. Does NOT decide case
  acceptance. Use when starting a new client intake, running an intake
  interview, or writing up a new client's situation.
argument-hint: "[optional: practice area hint]"
---

# /client-intake

1. Load `~/.claude/plugins/config/claude-for-hk-law/legal-clinic/CLAUDE.md` → practice areas, intake templates, supervision style, flag triggers.
2. Use the workflow below.
3. Route to practice-area template. Listen for cross-area issues throughout.
4. Conflict check flags. Triage classification.
5. Output formatted case summary with AI-assisted label, verification prompts, supervision routing.

```
/legal-clinic:client-intake
```

---

# Client Intake

## Purpose

Intake is one of the biggest bottlenecks in clinics. A student might spend 45 minutes interviewing, another hour writing it up, more time spotting the issues. Meanwhile the waitlist grows.

This skill structures the conversation, produces the write-up, spots issues across practice areas, and flags conflicts — so the student's time goes to analysis, not transcription.

**What it doesn't do:** decide whether to take the case. That's the student's analysis and the professor's judgment. Claude accelerates the information-gathering and structuring, not the lawyering.

## Load context

`~/.claude/plugins/config/claude-for-hk-law/legal-clinic/CLAUDE.md` → practice areas, intake templates (per practice area if multiple), supervision style, jurisdiction, flag triggers.

## Read the supervisor guide

Check for a practice-area guide at `~/.claude/plugins/config/claude-for-hk-law/legal-clinic/guides/<practice-area>.md`. If one exists, use its intake questions, red flags, and good-fit criteria instead of the generic defaults below. If one doesn't exist, use the generic intake and note at the end of the intake summary: "This was a generic intake — your supervisor can tailor the questions for your clinic type with `/legal-clinic:build-guide`."

When the intake starts before the practice area is routed (Step 1 of the workflow below), re-check for the guide after routing — the guide path depends on which practice area the intake landed in.

## Workflow

### Step 1: Practice area routing

Which practice area does this intake start in? The client may not know — they know their problem, not the legal category.

> "Tell me what's going on — what brought you to the clinic today?"

From the answer, route to the appropriate intake template. If the clinic handles multiple areas and the problem spans them (housing client mentions immigration status, family client mentions domestic violence), note all relevant areas — cross-area issue spotting is a feature, not a bug.

### Step 2: Practice-area-specific intake

Each practice area asks different questions. Use the template from `~/.claude/plugins/config/claude-for-hk-law/legal-clinic/CLAUDE.md` for this area. Defaults if none provided:

**Immigration (HK context — non-refoulement, overstayer, torture claims):**
- Current immigration status and how entered HK
- Any prior applications, removals, encounters with the Immigration Department
- Country conditions relevant to any non-refoulement/torture claim
- Family members in HK and their statuses
- Criminal history (sensitive — explain why asking)
- Timeline urgency: any pending hearings, appeal deadlines, removal directions
- Relevant: Immigration Ordinance (Cap 115), Torture Claim framework

**Housing (HK context):**
- Type of housing (private, public housing / HA, subdivided flat, HOS)
- What happened: notice to quit, distraint, conditions problem, deposit dispute
- Lease terms and payment history — is the property subject to the Landlord and Tenant (Consolidation) Ordinance (Cap 7)?
- Habitability issues (repairs requested, landlord response, documentation — note the Maintenance Order regime under Cap 7)
- If public housing: any Housing Authority notice issues
- Timeline urgency: notice date, court date if any (Lands Tribunal, District Court)
- Refer to CLIC (www.clic.org.hk) for tenant rights information

**Family (HK context):**
- Relationship and what's at issue (custody, access, maintenance, divorce, protection)
- Children involved — ages, current arrangement
- Safety: any domestic violence (Domestic and Cohabitation Relationships Violence Ordinance Cap 189), threats, fear (handle carefully — see cross-area flags)
- Existing court orders (Matrimonial Causes Ordinance Cap 179, Separation and Maintenance Orders Ordinance Cap 16)
- Timeline urgency: any hearings scheduled, urgent protection order needed

**Consumer (HK context):**
- Type of debt or dispute
- Who's contacting them and how
- Documentation: contracts, statements, demand letters, credit card agreements
- Has anything been filed against them (Small Claims Tribunal, District Court)
- Timeline urgency: answer deadlines, judgment enforcement
- Relevant: Control of Exemption Clauses Ordinance (Cap 71), Unconscionable Contracts Ordinance (Cap 458), Money Lenders Ordinance (Cap 163)

### Step 3: Cross-practice-area issue spotting

While running the practice-area template, listen for issues outside that area:

| Client says | Also flags |
|---|---|
| "I'm worried about my immigration status" | Immigration issue — even in a housing intake |
| "My partner [threatening behavior]" | DV / family law / protection order (Cap 189) — even in a consumer intake |
| "I can't work because of my injury" | Possible employee's compensation claim / disability benefit |
| "They're taking money from my wages" | Garnishment — consumer/employment overlap |
| "The landlord said he'd report me to Immigration" | Housing + immigration + possible unlawful eviction under Cap 7 |

Note every cross-area issue in the summary. The clinic may handle it, refer it, or both — that's the professor's call. The student should see it.

### Step 4: Conflict check flags

Per whatever conflict-check process `~/.claude/plugins/config/claude-for-hk-law/legal-clinic/CLAUDE.md` describes. At minimum:

- Opposing party name(s) — does the clinic represent or have represented them?
- Related parties — anyone else the student or clinic might have a conflict with?
- Positional conflicts — is this case asking for something that would hurt another clinic client?

Flag for professor review. Don't resolve the conflict — surface it.

### Step 5: Triage classification

Not a case-acceptance decision — a triage input:

| Classification | Means |
|---|---|
| **Urgent** | Deadline in days, safety issue (e.g., risk of domestic violence under Cap 189), irreversible harm imminent, removal directions imminent |
| **Time-sensitive** | Deadline in weeks, harm ongoing but not immediately irreversible |
| **Standard** | No immediate deadline, can queue normally |
| **May be out of scope** | Issue is outside clinic's practice areas — flag for referral assessment (e.g., CLIC, Duty Lawyer Service, Free Legal Advice Scheme) |

### Step 6: Supervision flag check

Per `~/.claude/plugins/config/claude-for-hk-law/legal-clinic/CLAUDE.md` supervision style and flag triggers. If formal queue or configurable flags are enabled, and a trigger is present (deadline mentioned, DV indicator, immigration status at issue, etc.), note the flag.

### Step 7: Deadline handoff — required deliverable

If the intake surfaces any timeline deadline (answer due, hearing, statute-of-limitations cutoff, cure period, filing window, notice window, ICE check-in, removal hearing, eviction court date, protective order renewal), **emit a copy-paste-ready `/legal-clinic:deadlines --add ...` block as part of the intake output**. This is a required deliverable, not a suggestion — the intake identifies deadlines, and the student shouldn't have to re-transcribe them into the deadline skill.

Format each deadline as a fenced code block the student can copy, with every field pre-populated from the intake:

```
/legal-clinic:deadlines --add
  case=[case slug or client-last-name-keyword]
  type=[response|hearing|statute-of-limitations|discovery|cure-period|filing-window|notice|other]
  description="[one-line description of what is due]"
  due=[VERIFY — student + supervisor compute from triggering event]
  source="[triggering event + ordinance/rule cite, e.g., 'Notice to Quit served 2026-05-04, Cap 7 § 4']"
  owner=[student name]
  warnings=[14,7,3,1]
```

Rules:
- One block per deadline surfaced. Do not combine. Each one will route through the deadlines skill's pre-add duplicate check.
- Leave the `due=` value as `[VERIFY — student + supervisor compute]` when the deadline is jurisdictional (response deadline, SOL, notice window under a specific rule). The deadlines skill will not compute for you; the student + supervisor do the math and update the entry.
- When a date is given in the triggering document (a hearing date on a summons, an Immigration Department check-in date, a renewal deadline on a protection order under Cap 189), put that date in `due=`. When the date is computed (count N days from triggering event), leave the `[VERIFY]` marker.
- If no deadline is surfaced in the intake, omit this section — don't fabricate one.

## Output

```markdown
# Intake Summary: [Client name or ID]

---
[AI-ASSISTED DRAFT — requires student analysis and attorney review]

**Privilege and confidentiality.** This summary is derived from client communications that may be privileged, confidential, or both. It inherits the source's privilege status. Distributing it beyond the privilege circle (including outside the clinic) can waive privilege. Keep it in the clinic's privileged file store, mark it appropriately, and make distribution decisions with your supervisor.
---

**Date:** [date] | **Intake by:** [student] | **Practice area:** [primary + any cross-area]

## Bottom line

[Take the case / Decline because X / Need more info on Y — next step is Z]

## Client's situation (in their words)

[The narrative the client gave, before legal categorization. This is the human story.]

## Legal issues identified

*Every statutory, ordinance, regulatory, rule, or case citation in this section carries a provenance tag (see plugin CLAUDE.md `## Shared guardrails` for the tag vocabulary). `[user provided]` if the supervisor uploaded the text, `[statute / regulator site]` if you fetched it this session from an official source (e.g., HK e-Legislation), a research-connector tag (`[HKLII]`, etc.) if it came from a tool result in this conversation, `[model knowledge — verify]` otherwise. The default is `[model knowledge — verify]`. A supervising attorney who cannot verify a cite against a connector needs to see the tag to know what to check first.*

### Primary ([practice area])
- [Issue 1]: [one line with any cite tagged, e.g., "Cap 7 § 5 `[model knowledge — verify]`"]
- [Issue 2]: [one line]

### Cross-practice-area flags
- [Other area]: [what the client said that raised it]
  [UNCERTAIN: whether clinic handles this or refers — professor call]

## Key facts

| Fact | Source | Documentation |
|---|---|---|
| [fact] | [client statement / document provided] | [have it / need it] |

## Conflict check

**Opposing party:** [name(s)]
**Related parties:** [any]
**Flag:** [clear / needs conflict check against clinic database]

## Triage

**Classification:** [Urgent / Time-sensitive / Standard / May be out of scope]
**Driving deadline:** [if any — date and what it is]

## Deadlines to log

[One `/legal-clinic:deadlines --add ...` block per surfaced deadline — Step 7.
If none, omit this section.]

## Jurisdictional notes

*Every statute, ordinance, rule, or case citation in this section carries a provenance tag — same vocabulary as `## Legal issues identified`. Default `[model knowledge — verify]`. When no research connector is reachable for this session, record it in the **Sources:** line of the reviewer note (see plugin CLAUDE.md `## Outputs`) — do not emit a standalone banner.*

[State-specific or local-rule-specific issues relevant to this case type, per
CLAUDE.md jurisdiction, with each cite tagged]

## Supervision flags

[If supervision style includes flags: which fired and why. If formal queue:
"QUEUED for [professor]."]

---

## Verification prompts for the student

Before analysis, verify:
- [ ] [Specific fact the intake relies on — confirm with client or documents]
- [ ] [Deadline date — confirm from the actual notice/court document, not client's memory]
- [ ] [Any legal conclusion above is a starting hypothesis — research before relying on it]

## What this summary does NOT do

This summary does not decide whether the clinic takes this case. That's your
analysis and [Professor]'s judgment. It structures what the client told you
so you can spend your time on the analysis instead of the write-up.
```

## Practice-area intake template references

Store practice-area-specific question sets at `references/intake-templates/[area].md`. Cold-start populates these from the professor's intake form(s); if none provided, use the defaults above.

## What this skill does NOT do

- **Decide case acceptance.** Student analyzes, professor decides.
- **Resolve conflicts.** Flags them for the professor.
- **Give advice during intake.** Intake is gathering; advice comes after analysis and professor review.
- **Produce a final document.** The summary is a starting point — the student reads it, corrects anything mischaracterized, and builds the analysis from it.

## Close with the next-steps decision tree

End with the next-steps decision tree per CLAUDE.md `## Outputs`. Customize the options to what this skill just produced — the five default branches (draft the X, escalate, get more facts, watch and wait, something else) are a starting point, not a lock-in. The tree is the output; the lawyer picks.

## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```

