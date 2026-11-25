---
name: nudge-disclosure-transparency-effectiveness
description: Apply the evidence base that transparent nudges can be as effective — or more effective — than covert ones, resolving the ethics-effectiveness tension in behavioral design. Use when designing nudges that must be ethical AND effective, when deciding whether to disclose a nudge to users, when choosing between disclosure content types (presence, purpose, mechanism, combined), or when building trust-preserving behavioral interventions for A-Coder, Be Practical, or Builder's Club.
---

# Nudge Disclosure Transparency Effectiveness

## Overview
Two converging 2025-2026 evidence streams — the Bruns et al. (2025) meta-analysis of 23 studies (117 effect sizes) and the Cuypers, Raymaekers & Van de Walle (2026) vignette experiment (N=1,916) — demonstrate that disclosing a nudge to users does not reduce its effectiveness and may even enhance it. This resolves the long-standing tension between the ethical imperative for transparency and the practitioner fear that "if people know they're being nudged, it won't work." The practical takeaway: ethical nudging and effective nudging are not in conflict — they are complementary.

## When to Use
- Designing nudges that must be both ethical (transparent) AND effective
- Deciding whether and how to disclose a behavioral intervention to users
- Choosing between disclosure content types (presence, purpose, mechanism, combined)
- Building trust-preserving behavioral design for A-Coder, Be Practical, or Builder's Club
- Reviewing existing covert nudges for conversion to transparent versions
- Responding to regulatory or community pressure for behavioral transparency
- Designing disclosure messages that minimize cognitive load while maximizing comprehension
- NOT for: situations requiring covert influence for safety-critical defaults (e.g., emergency opt-out), or where disclosure would itself cause harm

## Core Process / Workflow

### Step 1: Understand the Evidence Base

**The Bruns et al. (2025) meta-analysis** pooled 23 publications comparing transparent to covert nudges (117 effect sizes). Key findings:
- Disclosed nudges have a **positive overall effect** on behavioral outcomes vs. covert nudges
- For non-behavioral outcomes (perceptions, intentions), disclosure makes no significant difference
- 17 of 23 studies used default nudges — generalizability beyond defaults is limited but growing
- Publication bias risk exists; the positive effect should be treated as encouraging, not definitive

**The Cuypers et al. (2026) experiment** tested four disclosure types on a salience nudge (sustainable food menu, N=1,916, preregistered, KU Leuven):
- The salience nudge increased sustainable choices by **10.4 percentage points** (33.0% → 43.4%)
- **No disclosure type significantly reduced or enhanced nudge effectiveness** vs. the covert nudge
- The **combined disclosure** (presence + purpose + mechanism) produced the highest sustainable choice rate (46.4%, +13.4 pp vs. control)
- The nudge caused a **small but significant decrease in perceived autonomy** (0.09 on a 5-point scale)
- **No disclosure type offset the autonomy decrease** — disclosures neither enhanced nor reduced perceived autonomy
- Three of four disclosures were **statistically equivalent** to the covert nudge on both effectiveness and autonomy

### Step 2: Select a Disclosure Content Type

Use de Ridder et al.'s (2022) four-element framework (Lasswell's communication model):

| Element | What it communicates | Example disclosure copy | Risk profile |
|---------|---------------------|------------------------|--------------|
| **Presence** | That behavioral techniques are being used (what/where/when) | "Behavioral insights are used to make certain options more visible" | Highest risk of suspicion if used alone (type interference); safer with specific reference (token interference) |
| **Purpose** | The policy goal / desired outcome (why) | "This menu highlights sustainable dishes to help reduce climate impact" | Low risk; can sometimes act as a nudge itself (goal alignment) |
| **Mechanism** | How the nudge works (how) | "Placing dishes at the top and using color makes them more noticeable" | Low risk; meta-analysis shows slight positive effect on effectiveness |
| **Combined** | All three elements | Presence + purpose + mechanism in one message | Highest comprehension potential; watch cognitive load if too long |

**Decision rules:**
1. If the nudge is already relatively overt (e.g., salience, framing): a presence disclosure alone adds little; prefer purpose or mechanism
2. If the nudge is relatively covert (e.g., defaults): mechanism disclosure has the strongest evidence base for positive effect
3. If cognitive load is a concern (crowded interface): prefer the single most informative element (usually purpose) over a long combined message
4. If maximum transparency is the goal and interface space allows: use the combined disclosure

### Step 3: Design for Comprehension, Not Just Presence

The Cuypers et al. study revealed a critical practical problem: **~40% of participants failed the disclosure awareness check.** Disclosures that go unnoticed fail to increase transparency. Design for noticeability:

- **Visual anchoring:** Link the disclosure to the nudged element with arrows, color, or placement (the experiment used a large arrow from the 'chef's choice' section to the disclosure)
- **Embedded, not separate:** Place disclosures within the choice environment (on the menu, in the interface), not as a separate notification
- **Brevity:** Keep mechanism disclosures brief to simulate real-life conditions where the information environment is crowded
- **Repeated exposure:** If the nudge is recurring, the disclosure should be persistent or re-shown at intervals

### Step 4: Apply the Autonomy Reality Check

The evidence delivers a sobering finding for autonomy-focused practitioners: **disclosures alone do not restore perceived autonomy.** The nudge itself caused a small autonomy decrease, and no disclosure type offset it.

**Implications for design:**
- Do NOT rely on disclosure as your primary autonomy-preservation strategy
- Pair disclosure with **structural autonomy safeguards**: preserve all choice options (freedom of choice), enable easy reversal, provide genuine alternatives
- The autonomy decrease observed was small (0.09/5.0) — not a serious threat — but it was real and consistent
- Perceived autonomy is a **heterogeneous construct** (freedom of choice, agency, self-constitution); measure all three, not just one
- If autonomy is a primary concern, consider nudge+ (reflection prompts) or boosts (capability building) instead of disclosure alone

### Step 5: Convert Covert Nudges to Transparent Versions

Audit existing behavioral interventions using this checklist:

```
For each existing nudge:
[ ] What type is it? (default / salience / framing / social proof / anchoring / other)
[ ] Is it currently disclosed to users? (covert / partially / fully transparent)
[ ] What is the ethical risk level? (low / medium / high)
[ ] Which disclosure element is most appropriate? (presence / purpose / mechanism / combined)
[ ] Where should the disclosure be placed for maximum noticeability?
[ ] Is the disclosure brief enough to avoid cognitive overload?
[ ] What structural autonomy safeguards accompany it? (reversibility, alternatives, exit)
[ ] How will disclosure comprehension be measured? (awareness check, survey, behavioral)
```

### Step 6: A-Tech Application Matrix

**A-Coder (developer IDE):**
- **Flow-state nudges:** If A-Coder nudges developers toward focused work patterns (e.g., reducing notifications during flow), disclose the mechanism: "A-Coder silences non-critical notifications when you're in a detected flow state to protect your focus."
- **Privacy defaults:** If privacy-preserving settings are the default, disclose: "A-Coder defaults to local processing because your code never leaving your machine is our core promise." (purpose + mechanism)
- **Progress architecture:** If the onboarding progress bar uses the endowed progress effect, disclose: "We've pre-filled the first steps of your setup because completing them signals your commitment." (mechanism)
- **Autonomy safeguard:** Always provide a one-click "show all notifications" override and a "disable flow detection" toggle

**Be Practical (learning platform):**
- **Chapter ordering nudges:** If chapters are ordered to leverage the goal gradient, disclose: "Chapters are sequenced so your motivation builds as you near each milestone." (mechanism)
- **Streak design:** If streak mechanics use variable rewards (motivating-uncertainty effect), disclose the structure without revealing the specific reward: "Completing daily practice unlocks surprise bonuses — the reward varies to keep motivation high." (purpose + partial mechanism)
- **Positive framing:** The mental health nudging evidence confirms positive-framing advantage — always frame disclosures positively
- **Autonomy safeguard:** Allow learners to set their own pace, skip chapters, and disable streaks entirely

**Builder's Club (community):**
- **Social proof nudges:** If contribution thermometers or "X members contributed this week" displays are used, disclose: "We show community contribution levels because seeing others participate makes contribution feel normal." (mechanism)
- **Contribution defaults:** If the community defaults to opt-in for certain features, disclose the default and the reason
- **Recognition design:** If variable contribution rewards are used, disclose the variability as a feature, not a trick
- **Autonomy safeguard:** Always allow members to hide social proof displays, set their own contribution goals, and exit any nudge-driven mechanic

## Key Evidence Summary

| Question | Answer | Evidence strength |
|----------|--------|-------------------|
| Do transparent nudges work? | Yes — as well as or better than covert nudges | Meta-analysis of 23 studies, positive overall effect |
| Which disclosure type is best? | No significant differences between types; combined disclosure shows highest descriptive effect | Direct comparison experiment, N=1,916 |
| Does disclosure restore autonomy? | No — disclosures do not offset the small autonomy decrease from nudging | Direct test, three autonomy operationalizations |
| What is the main practical risk? | Disclosures go unnoticed (~40% failure rate in the study) | Manipulation check data |
| Does this generalize beyond defaults? | Growing but still limited — salience nudges now tested, more nudge types needed | One salience study + meta-analysis |

## Anti-Patterns
- **The "ethics tax" assumption:** Believing transparency costs effectiveness — the evidence contradicts this
- **Disclosure-as-autonomy-fix:** Relying on disclosure alone to preserve perceived autonomy — it doesn't
- **The invisible disclosure:** Placing a disclosure where users won't see it, then claiming transparency
- **The maximalist disclosure:** A long, complex combined disclosure that overwhelms cognitive capacity
- **Type-interference-only:** Disclosing only "behavioral techniques are used" without context — highest risk of suspicion

## References
- See [references/bruns-meta-analysis-and-cuypers-extraction.md](references/bruns-meta-analysis-and-cuypers-extraction.md) for full study detail, methodology, all results tables, and theoretical framework.