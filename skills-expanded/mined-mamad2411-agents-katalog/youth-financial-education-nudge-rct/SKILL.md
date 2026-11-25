---
name: youth-financial-education-nudge-rct
description: Applies the Levy, Howard & Lukas (2026) large-scale preregistered field experiment (approximately 425,000 children and parents) testing behavioral nudges to increase youth participation in voluntary financial skills training. Covers the targeting decision framework (nudge the child, not the parent), the message-content optimization guidance (sending a message matters more than optimizing its content), the persistence and downstream-behavior findings, and the factorial experimental design template. Use when designing nudges to increase engagement with voluntary educational or training content, deciding whether to target parents or children (or end-users vs gatekeepers), optimizing reminder or invitation message content, evaluating whether nudge-induced engagement will persist or translate to behavior change, designing factorial nudge experiments, or building financial-literacy or skills-training engagement features for Be Practical, A-Coder, or Builder's Club. NOT for high-stakes financial decisions where nudges are weakest, NOT for assuming engagement nudges will produce durable behavior change, and NOT for message-content optimization when the evidence says content optimization yields no marginal gain over simply sending a message.
---

# Youth Financial Education Nudge RCT

## Overview

A large-scale preregistered field experiment by Levy, Howard & Lukas (Stanford, University of Virginia, University of St. Andrews; January 31, 2026) tested behavioral nudges designed to increase youth participation in voluntary financial skills training. The study randomized approximately 425,000 children and their parents across a 3 × 10 (parent × child) factorial design — 3 parent conditions (control + 2 parent nudge arms) crossed with 10 child conditions (control + 9 distinct child nudge types) — within a mobile app context featuring 25 financial-skills questions.

The results deliver four counterintuitive lessons that should reshape how product teams design engagement nudges:

1. **Nudge the child, not the parent.** Child-directed nudges raised training uptake from 2.70% to 3.13% (ATE = 0.43 percentage points, p < 0.001) — a 16% relative increase. Parent-directed nudges had no detectable effect on child outcomes. Nudging both parents and children simultaneously offered no advantage over nudging children alone (interaction term effectively zero, p = 0.92).

2. **Sending a message matters more than optimizing its content.** All 9 child nudge types — spanning identity priming, future payoff, attention, and endorsement categories — significantly outperformed control. But none was significantly superior to another (all pairwise p > 0.75). The dominant effect is the act of outreach, not the psychological framing.

3. **Engagement effects do not persist.** Difference-in-differences analysis showed nudge-induced engagement was a timing shift, not a durable change. Users engaged earlier but not more in total over the observation window.

4. **Engagement does not translate to behavior change.** Despite increasing training uptake, the nudges produced no detectable downstream effects on savings behavior. Getting people into the training did not change their financial actions.

For A-Tech, this study is a direct evidence base for the Be Practical financial freedom curriculum — it tells us what nudges can and cannot do when the goal is getting learners into voluntary financial education, and it sets honest expectations about whether that engagement will persist or change behavior.

## When to Use

- Designing nudges, reminders, or invitations to increase engagement with voluntary educational or training content
- Deciding whether to target end-users directly or to target gatekeepers (parents, managers, admins) who influence end-user behavior
- Optimizing reminder or invitation message content and wondering whether A/B testing message variants is worth the effort
- Evaluating whether nudge-induced engagement will persist over time or translate to downstream behavior change
- Designing factorial nudge experiments (multi-arm, multi-dimensional designs testing multiple nudge types simultaneously)
- Building financial-literacy or skills-training engagement features for Be Practical, A-Coder onboarding, or Builder's Club participation
- Setting realistic expectations for engagement-nudge effect sizes in voluntary-learning contexts (baseline uptake ~2.7%, nudge lift ~16% relative)

### NOT for...

- High-stakes financial decisions (savings, investment, debt) where the goal is behavior change, not engagement — this study found no downstream behavior effect
- Assuming engagement nudges will produce durable behavior change — they produced a timing shift, not persistent engagement
- Message-content optimization exercises when the evidence indicates content optimization yields no marginal gain over simply sending a message
- Assuming parent/gatekeeper nudges will influence child/end-user outcomes — they did not

## Core Process / Workflow

### Step 1: Apply the Targeting Decision Framework

The single most actionable finding: **nudge the end-user directly, not the gatekeeper.** Before designing any engagement nudge, run through this decision tree:

```
WHO IS THE DECISION-MAKER?
│
├── The end-user performs the target behavior themselves
│   → Nudge the end-user directly.
│   → Do NOT spend resources nudging the gatekeeper.
│   → Do NOT assume nudging both is better than nudging one.
│
├── A gatekeeper (parent, manager, admin) controls access or approval
│   → First, test whether the gatekeeper nudge moves the end-user outcome.
│   → In this study, the parent nudge had ZERO detectable effect.
│   → If the gatekeeper nudge shows no effect, redirect all resources
│     to the end-user nudge.
│
└── Both end-user and gatekeeper are involved
    → Default to the end-user nudge.
    → Only add the gatekeeper nudge if a pilot shows a nonzero
      interaction effect (this study found p = 0.92 — effectively
      zero additive value).
```

**Why gatekeeper nudges failed here:** The child was the one who had to open the app and answer the questions. The parent nudge may have been delivered to a channel the parent did not check, or the parent may have lacked the leverage or motivation to direct the child's behavior in this context. The general lesson: when the end-user holds the action lever, target the end-user.

### Step 2: Apply the Message Content Optimization Guidance

When designing the message itself, follow the evidence-based priority order:

| Priority | Action | Evidence |
|---|---|---|
| **1 (highest)** | Send a message at all | Control (no message) vs. any nudge: significant lift (p < 0.001) |
| **2** | Ensure the message reaches the end-user's active channel | The parent-channel message had no effect; the child-channel message did |
| **3 (lowest)** | Optimize the psychological framing of the message | All 9 nudge types performed equivalently (all pairwise p > 0.75) |

**The 9 child nudge types tested (all equivalent in effect):**

- **Identity priming:** Messages that frame the child as someone who is financially savvy or responsible
- **Future payoff:** Messages that emphasize the long-term benefit of financial skills
- **Attention:** Messages that simply raise the salience of the available training
- **Endorsement:** Messages that leverage social endorsement or authority signals

**Practical implication:** Do not over-invest in message-copy A/B testing for engagement nudges. Pick any well-formed message from the four categories above, send it through the end-user's active channel, and redirect your optimization budget to higher-leverage decisions (targeting, timing, channel, and what happens after engagement).

### Step 3: Set Persistence Expectations

Use the difference-in-differences finding to calibrate persistence expectations:

- **Short-term:** Expect a timing shift — nudge recipients engage earlier than non-recipients.
- **Total engagement:** Do not expect the nudge to increase cumulative engagement over a longer window. The earlier engagement may come at the expense of later engagement.
- **Design implication:** If the goal is cumulative engagement (not just timely engagement), a single nudge is insufficient. Plan for repeated nudges, structural reminders, or a curriculum design that creates its own re-engagement pull (progress, streaks, social accountability).

This aligns with the `nudge-persistence-technology-adoption` skill: pure attention nudges produce timing shifts, not durable change. Persistence requires either a technology-adoption channel (a durable configuration change) or a habit-formation channel (repeated cue-response). A one-time message nudge provides neither.

### Step 4: Set Downstream-Behavior Expectations

The most sobering finding: **training uptake did not translate to savings behavior change.** Getting children into the financial skills training did not change whether they saved money.

Apply this expectation to any engagement-nudge design:

```
ENGAGEMENT ≠ BEHAVIOR CHANGE

Nudge → Engagement (training uptake) → [GAP] → Behavior change (savings)

The [GAP] is real and was not closed by the training in this study.
```

**Design implications:**
- Measure the downstream behavior, not just the engagement metric. An engagement lift that does not move the behavior metric is a partial result.
- If the goal is behavior change, the intervention must include more than an engagement nudge. It likely needs a boost (competence-building), a structural change (default enrollment, auto-save), or an incentive — not just an invitation to learn.
- This connects to the `boosting-empowering-behavior-change` skill: nudges clear the path to learning; boosts build the competence that learning is supposed to deliver. The Levy et al. finding suggests that the nudge-to-learning link is working, but the learning-to-behavior link needs a different intervention.

### Step 5: Use the Factorial Design Template

The study used a 3 × 10 factorial design (3 parent conditions × 10 child conditions = 30 cells). This is a powerful template for testing multiple nudge dimensions simultaneously without running separate experiments for each.

**Factorial nudge experiment template:**

1. **Identify the dimensions** you want to test (e.g., target audience × message type × timing)
2. **Define the levels** within each dimension (e.g., 3 audience levels × 4 message types × 2 timing windows = 24 cells)
3. **Randomize participants across all cells** (balanced assignment)
4. **Include a pure control** in each dimension (no message, no timing nudge)
5. **Pre-register the hypotheses and analysis plan** — this study was preregistered, which is what makes the null findings (parent nudge no effect, no content difference, no persistence, no downstream behavior) credible rather than suspicious
6. **Power for the interaction tests**, not just the main effects — the key finding that parent + child nudging is no better than child alone (p = 0.92) required sufficient power to detect (or rule out) an interaction
7. **Report all pairwise comparisons** with adjusted p-values — the "all nudge types are equivalent" finding rests on 36 pairwise comparisons all exceeding p > 0.75

### Step 6: Interpret Homogeneous Effects Correctly

The study found effects were homogeneous across age and gender subgroups — no significant heterogeneity. This is informative but should be interpreted carefully:

- **Homogeneity does not mean the nudge works equally for everyone in absolute terms.** It means the *treatment effect* (the lift from the nudge) was the same across subgroups. Baseline engagement rates may still differ.
- **Do not over-segment.** If a well-powered study finds no heterogeneity across age and gender, do not assume your smaller-scale deployment will find meaningful segment differences. Spend the segmentation budget on channel and timing instead.
- **This contrasts with the `scaled-behavioral-measurement-targeting` skill**, where a latent behavioral moderator (loss aversion) drove real heterogeneity. The difference: in Levy et al., the nudge was a simple attention/identity message with no theory-predicted moderator. When theory identifies a moderator, test for heterogeneity; when it does not, expect homogeneity and save the segmentation cost.

## A-Tech Application Matrix

### Be Practical (Financial Freedom Curriculum) — PRIMARY APPLICATION

This study is the most directly relevant evidence base in the entire skill library for Be Practical's financial education mission.

| Be Practical Decision | Levy et al. Guidance | Action |
|---|---|---|
| **How to increase voluntary module completion** | Child-directed nudges increased training uptake 16% | Send direct nudges to the learner (not to a spouse, manager, or parent) via the learner's active channel |
| **Whether to A/B test module invitation copy** | All 9 nudge types performed equivalently (p > 0.75) | Do not over-invest in copy optimization. Pick any well-formed invitation and ship it. Reallocate the A/B testing budget to channel and timing |
| **Whether to nudge both the learner and an accountability partner** | Parent + child nudging was no better than child alone (p = 0.92) | Default to learner-only nudging. Only add an accountability-partner nudge if a pilot shows a nonzero interaction |
| **Whether engagement nudges will produce lasting learning habits** | DiD showed a timing shift, not durable engagement | Do not expect a single invitation nudge to create a lasting learning habit. Build re-engagement into the curriculum (progress, streaks, checkpoints — see `zeigarnik-onboarding-architecture` and `behavioral-design-practical-playbooks`) |
| **Whether getting learners into the training will change their financial behavior** | No downstream effect on savings behavior | Measure downstream financial behavior, not just module completion. If the goal is behavior change, pair the engagement nudge with a boost (competence-building) and a structural change (auto-save, default enrollment) — see `boosting-empowering-behavior-change` and `nudge-persistence-technology-adoption` |
| **What effect size to expect** | Baseline 2.70%, lift to 3.13% (16% relative) | Set realistic targets: a 10-20% relative lift in voluntary engagement is a good outcome. A 50%+ lift is likely inflated |

**Curriculum design implication:** Be Practical should be designed as a two-stage intervention:
1. **Stage 1 (Engagement):** A direct, simple nudge to the learner via their active channel. Any well-formed message works. Do not over-engineer the copy.
2. **Stage 2 (Behavior change):** The curriculum itself must be a boost — it must build the competence and provide the structural tools (calculators, auto-enrollment templates, implementation intentions) that convert learning into action. The Levy et al. finding tells us Stage 1 alone does not produce Stage 2.

### A-Coder (Developer Onboarding & Engagement)

| A-Coder Decision | Levy et al. Guidance |
|---|---|
| Nudging new developers to complete onboarding | Send the nudge to the developer directly, not to their team lead. The end-user holds the action lever. |
| A/B testing onboarding invitation messages | All message variants performed equivalently. Ship one good message; spend the optimization budget on the onboarding flow itself. |
| Whether onboarding nudges create lasting habits | Expect a timing shift, not durable engagement. Build re-engagement into the IDE (progress, unlockable features — see `zeigarnik-onboarding-architecture`). |
| Whether onboarding completion changes coding behavior | Engagement ≠ behavior change. Measure downstream coding metrics (PR rate, test coverage), not just onboarding completion. |

### Builder's Club (Community Participation)

| Builder's Club Decision | Levy et al. Guidance |
|---|---|
| Nudging members to participate in community challenges | Nudge the member directly, not via a group admin or moderator. |
| Optimizing challenge invitation language | Content optimization yields no marginal gain. Send a clear, well-formed invitation and focus on the challenge design instead. |
| Whether participation nudges create lasting contributors | Expect a timing shift. Build structural re-engagement (contribution streaks, milestone badges, peer pairing — see `behavioral-design-practical-playbooks`). |
| Whether challenge participation leads to ongoing open-source contribution | Measure downstream contribution behavior (PRs, issues, reviews), not just challenge participation. Pair the engagement nudge with competence-building boosts. |

## Cross-References to Existing Nudging Skills

- **`nudge-persistence-technology-adoption`** — The Levy et al. timing-shift finding is a direct instance of the "pure attention" pathway in the persistence framework. A one-time message nudge produces no durable artifact and no habit loop, so it does not persist. Use the persistence framework to design a follow-on intervention that does persist (technology adoption or habit formation).
- **`nudge-effectiveness-reality-check`** — The 16% relative lift (0.43pp on a 2.70% baseline) is consistent with the bias-corrected nudge effect-size range (d ≈ 0.004 to d = 0.27). Finance is the lowest-receptivity domain in the Mertens hierarchy (d = 0.25), and this study confirms that even a well-powered, preregistered nudge in the financial domain produces a small absolute effect. Use this skill to calibrate expectations.
- **`boosting-empowering-behavior-change`** — The "no downstream behavior change" finding is the core argument for boosting. The nudge got learners into the training (engagement), but the training alone did not build the competence needed to change behavior. Pair engagement nudges with competence-building boosts.
- **`boosts-vs-nudges-public-preference`** — When communicating the Be Practical intervention strategy to learners, frame the nudge (invitation) and the boost (curriculum) as complementary. The nudge removes friction to starting; the boost builds the capability that makes starting worthwhile.
- **`scaled-behavioral-measurement-targeting`** — Levy et al. found homogeneous effects across age and gender. This contrasts with the Bauer et al. finding that a theory-identified latent moderator (loss aversion) drove real heterogeneity. The lesson: when theory identifies a moderator, test for heterogeneity and target; when it does not, expect homogeneity and save the segmentation cost.
- **`nudge-second-order-meta-analysis-publication-bias`** — This study is preregistered and high-powered (N ≈ 425,000), which is exactly the evidence-quality standard the meta-analysis skill recommends. Its null findings (no parent effect, no content difference, no persistence, no downstream behavior) are credible precisely because the study meets that standard.
- **`behavioral-design-practical-playbooks`** — The playbook design principles (implementation intentions, progressive commitment, social proof, variable rewards) are the Stage 2 boost that the Levy et al. finding says is necessary. The nudge gets learners in; the playbook design is what should produce behavior change.
- **`zeigarnik-onboarding-architecture`** — The Zeigarnik-based re-engagement design (incomplete tasks pull learners back) is a structural solution to the persistence gap that Levy et al. identified. A one-time nudge produces a timing shift; Zeigarnik architecture produces re-engagement pull.
- **`hyperbolic-discounting-reversal`** — The "future payoff" nudge type in Levy et al. is conceptually related to hyperbolic discounting interventions. The finding that future-payoff framing was no more effective than simple attention nudges suggests that future-payoff framing alone is insufficient to overcome present bias — consistent with the hyperbolic discounting skill's recommendation to combine reframing with structural commitment devices.
- **`llm-iterative-personalized-nudging`** — The Li et al. study found that LLM-personalized nudges produced large effects (32.4% vs 14.1% saving rate) in a low-friction domain (electricity). Levy et al. found no content-optimization benefit in a financial-education context. The contrast suggests that personalization may matter more in some domains than others — and that in voluntary financial education, the bottleneck is not message content but the decision to engage at all.

## References

- See [references/evidence-base.md](references/evidence-base.md) for the full study details, experimental design, all results (main effects, interactions, subgroup analyses, difference-in-differences, downstream behavior), implications, limitations, and A-Tech alignment.