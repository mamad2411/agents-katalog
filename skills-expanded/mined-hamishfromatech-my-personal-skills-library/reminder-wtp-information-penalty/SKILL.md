---
name: reminder-wtp-information-penalty
description: Applies the Barron, Damgaard & Gravert field experiment (Journal of Economic Behavior & Organization 241, 2026; 4,009 pregnant women in South Africa via a national mobile-health platform) showing that demand for reminders is substantial and that reminders themselves create demand — exposure to reminders increases BOTH adherence AND willingness to pay for MORE reminders, while adding health information to a reminder reduces both. Use when [designing notification or reminder systems for behavior-change apps, pricing any reminder/subscription/nudge product (including AI assistant nudges), deciding whether to attach content to a reminder, or forecasting engagement vs monetization tradeoffs in nudging]. NOT for [spam-optimization or engagement-maximization dark patterns, medical advice or clinical dosing decisions, or one-shot advertising copy design].
---

# Reminder WTP & the Information Penalty

## Overview
The first field experiment to measure both the behavioral and monetary value of reminders in a real public-health deployment at scale: >4,000 women via South Africa's national MomConnect platform, randomized across purely attentional, informational, and morally persuasive reminder types. The headline: **people value reminders enough to pay for them, receiving reminders increases that valuation, and adding information to a reminder destroys value on both margins.** This is the cheapest, cleanest evidence base for any A-Tech conversation about notification design or nudge pricing.

## The Evidence Base
- **Barron, Kai; Damgaard, Mette Trier; Gravert, Christina** — "Nudge Me! A field experiment on reminders for medication adherence," *Journal of Economic Behavior & Organization*, vol. 241 (2026), DOI 10.1016/j.jebo.2025.107368.
- Field experiment with **over 4,000 pregnant women** delivered via the **national mobile health platform** (South Africa).
- Reminder arms: purely **attentional** (nudge-to-action only), **informational** (adds health information), and **morally persuasive** framing.
- Two outcome families: (1) **adherence to iron supplementation**, (2) **willingness to pay (WTP)** for future reminders (revealed-preference, not stated).
- See `references/barron-damgaard-gravert-evidence-base.md` for the full extraction and design caveats.

## Core Findings (the four laws)
1. **Demand is high.** Despite high self-reported adherence, **>80% of participants chose additional reminders when free**, and many were willing to pay for them. Self-report overstates adherence AND understates demand for support — the gap between the two is the product opportunity.
2. **Reminders create their own demand.** Exposure to reminders **increases both adherence and WTP**. Reminding is a habit loop with a positive feedback property: using the feature makes people value more of it. This is the rare nudge with a *compounding* rather than decaying effect (contrast with the nudge-wear-off literature the library already tracks).
3. **The information penalty.** Reminders that include additional health information **significantly reduce BOTH adherence and WTP** relative to simple reminders. Well-intended content is not neutral: it converts a frictionless attentional cue into a cognitive task.
4. **The mechanism is effort, not distrust.** An information-bearing reminder asks the recipient to read, process, and decide — reintroducing the exact friction the reminder exists to remove. (See A-Tech's `engagement-gated-nudge-effectiveness-2026`: engagement is the gate; here content itself gates engagement.)

## When to Use
- Designing any reminder/notification product (health, finance, learning, AI assistants).
- Pricing nudges: the WTP data justifies subscription tiers for reminder *quality* (frequency control, no-info mode).
- Deciding whether to attach educational content to a behavioral prompt.
- Arguing against "make notifications richer/more personal" without evidence.

## NOT For
- Engagement-farming: maximizing notifications without regard to user welfare inverts the finding.
- Clinical decisions: the domain is iron-supplementation reminders; generalize the mechanism, not the medical content.
- Stated-preference surveys: use revealed WTP designs.

## Core Process / Workflow
1. **Audit the reminder payload.** List every element of your notification: salience cue, link, text, images, personalization. Classify each as attentional vs informational.
2. **Apply the information-penalty test.** Ask: does this element require reading/processing before action? If yes, it is a candidate for removal or deferral (move content to a tap-through, never into the notification).
3. **Keep the reminder dumb.** Default: cue + link + action. If information must be delivered, send it as a *separate, opt-in* message — never bundled with the nudge.
4. **Design the WTP hook, not just the hook.** Because reminders increase their own demand, the premium tier is frequency/quiet-hours control and "no-education mode" — sell the cleaner cue, not more content.
5. **Measure both outcomes.** Track adherence/completion AND opt-in-to-more-reminders (revealed demand proxy). A drop in the second after adding content is your information-penalty signal.
6. **Pre-commit against scope creep.** Write the "no content in nudges" rule into the notification design system so A/B tests don't silently reintroduce the penalty.

### Template: Reminder Payload Audit
| Element | Type (attentional/informational) | Processing required | Keep / defer / cut |
|---|---|---|---|
| Title cue | attentional | none | keep |
| "Learn more" body text | informational | reading | defer to tap-through |
| Emoji/mascot | attentional | none | keep (test) |
| Multi-line health explainer | informational | reading + judgment | cut (penalty applies) |

## A-Tech Alignment
- **Open source:** replicable via SMS/push A/B tooling; MomConnect is a public-sector deployment pattern.
- **Privacy:** reminders carry no behavioral profiling requirement — a low-surveillance nudge class.
- **Financial freedom:** quantified WTP for reminders = defensible pricing for behavior-change products; the premium is *less* content, not more.
- **Practical:** the information-penalty test is a one-page rule any product team can run Monday morning.

## References
- See [references/barron-damgaard-gravert-evidence-base.md](references/barron-damgaard-gravert-evidence-base.md) for study details, arm design, limitations (single country, single supplement, adherence partly self-reported), and the A/B template.
- Pairs with: `engagement-gated-nudge-effectiveness-2026` (engagement gates nudge effects), `nudge-effectiveness-reality-check` (small-effects calibration), `boosting-empowering-behavior-change` (reminders as the simplest boost), `digital-addiction-economics-2026` (WTP-for-commitment precedent), `intent-assistant-attention-steering` (gentle-notification design pattern).