---
name: intent-assistant-attention-steering
description: Applies the Intent Assistant (INA) pattern — an LLM vision agent that continuously scores screen content against a user's stated intention and intervenes with gentle, dismissible nudges (accuracy 0.878, 22-participant field study) — to design attention-steering assistants that preserve autonomy instead of blocking. Use when designing AI-assisted focus/digital-wellbeing features, evaluating context-aware proactive assistants, building screenshot-understanding nudges, writing about intention-based vs rule-based self-control tools, or studying trust and privacy concerns in screen-monitoring agents.
---

# Intent Assistant (INA): Attention-Steering Agents

## Overview

INA (Choi, Lee, Kim, C. Kim, Min, Knox, M.K. Lee & K. Lee — KAIST/UT Austin/Univ. of Seoul/Yonsei, arXiv:2510.14513, system paper 2026) is the cleanest documented pattern for **LLM-based steering of human attention** across arbitrary screen tasks. The system has four loops:

1. **Intention elicitation** — user states an intention; the LLM runs a brief clarification dialogue to disambiguate ("study" → "study HCI via YouTube lectures using these resources"). Clarification alone raises distraction detection accuracy from 0.805 to 0.871.
2. **Continuous scoring** — every ~2s, a Gemini 2.0-Flash call scores the current screenshot + app metadata against the clarified intention on a 0–1 distractibility rubric. Full system accuracy 0.878, F1 0.845 (IntentionBench, 77h of natural workflow); 0.899 on real deployment data.
3. **Gentle intervention** — on sustained on-task→off-task transition (4s dwell), a *dismissible* notification: soft question + re-entry suggestion ("Shall we restart with X?"); polite P20-style phrasing, no command. On return, praise. Repeat at 30s max while off-task.
4. **Feedback refinement** — user one-click marks nudges right/wrong; the LLM generates a reflection that edits scoring policy in the prompt (validated by marked cases later). Detection + clarification + feedback together: 0.878.

Three-week in-the-wild comparison (N=22, within-subject vs. simple reminder and logging-only): LLM-estimated off-task ratio 0.104 INA vs. 0.166 simple reminder (p<.001); intention-alignment 4.44 vs. 4.23 (p<.001); focused immersion 3.74 vs. 2.90 logging-only (p=.0003).

## When to Use

- Designing AI-assisted focus, digital-wellbeing, or proactive-assistant products (distraction nudge + praise pattern)
- Evaluating screenshot/vision-context agents for user-behavior assistance
- Reasoning about the safety trap of intention-steering systems (guardrail bypass)
- Deciding between rule-based blocking vs. semantic-intention steering in a product
- NOT for: clinical addiction treatment; employee monitoring; covert steering (fails the INA autonomy condition)

## Core Pattern

```
loop (every 2s):
  screenshot → VisionLLM → distract_score 0..1 (rubric-anchored, chain-of-thought first)
  if score crosses 0.5 sustained ≥4s:
    if transition to off-task → gentle dismissible nudge (LLM-written, references intention)
    if transition to on-task → short praise
    sustained off-task → re-nudge at max 30s intervals
  on user "incorrect" feedback → LLM reflection → append policy adjustment to prompt
```

**Prompt-structure constants (from the paper):** 6-band rubric (0.0 "perfectly relevant" → 1.0 "completely irrelevant") with worked examples per band; "Be certain for scores" extreme-score-only-with-evidence rule; warm supportive tone; always mention front-most app/URL; JSON-only schema (score field).

**State-transition mechanics:** trigger on *state transition + dwell*, not raw threshold, to avoid notification storms. Message generation is a separate prompt pass from detection.

**Benchmarks/metrics to copy:** distraction score 0–1; sustained-transition trigger; F1 target ≥0.85 pre-launch (INA's 0.845/0.878); IntentionBench (50 tasks × 14 apps × 32 sites; on-task/off-task synthesis) as public benchmark design reference.

## Evidence & Field-Study Mechanics

- Within-subjects, 1 week per condition, randomized order, blind names ("Purple/Blue/Orange"). 1,786 sessions / 1,360h / ~2.45M logs.
- Users reported INA felt *supportive/companionalbe* (praise was a meaningful positive mechanism), not surveillance-like — in contrast to logging-only condition which felt surveilling and passive.
- **Negative findings that transfer:** ~half of participants raised data-privacy concerns despite on-device masking; notification fatigue (27% "excessive notifications", 27% "misclassified notifications"); forced per-session Q&A caused frustration; negative feedback only persisted within a session ("Why am I inputting this again?").

## The INA Safety Trap (novel failure mode — treat as a design invariant)

INA *encourages* the user's stated intention. Nothing stops a user from stating an unsafe intention; once stated, the system works *against* it. Paper's observed failure: user states "hack into hospital server", browses phishing tutorials → INA praises; user then shifts to an ethics lesson → INA nudges them *back to the harmful intent*. The authors' proposed mitigations (guardrail model gating of nudges/praise WildGuard-style, harm-classification on clarified intentions, refuse-and-safe-alternative path) should be treated as **mandatory, not optional** in any real deployment.

## A-Tech Alignment

- **Open source**: IntentionBench released publicly; architecture replicable with open-weights (vision LLM + prompt engineering, no proprietary lock-in — a genuinely open-source-buildable pattern).
- **Data privacy**: the central design tension, addressed explicitly by the authors: screenshot → temp server for scoring → encrypted storage, with stated goal of eventual fully-local processing; ~50% of participants still raised privacy concerns even under the lab-masking protocol. Design implications: prefer local vision-LLM scoring; never store raw screenshots; feedback-only persistent state. The privacy concern is intrinsic to *screen understanding* — treat on-device as an architecture requirement, not an optimization.
- **Financial freedom**: a practical pattern for a privacy-preserving, on-device digital-wellbeing product (opportunity cost: ~1.7 h/day of reclaimable focus in the study population); pairs with `digital-addiction-economics-2026`'s $4.20 WTP finding for committed self-control.
- **Practical implementation**: explicit loop + rubric + state machine above is implementable today as an open-source local screencast agent.
- **Community/ethical stance**: INA only nudges toward goals the user *typed themselves* — the antithesis of engagement-optimizing dark patterns; use as the ethical contrast case in attention-economy content, together with `digital-addiction-economics-2026`'s litigation exposure side.

## References

- arXiv:2510.14513 (2026): "State Your Intention to Steer Your Attention: An AI Assistant for Intentional Digital Living" — full system, prompts, ablations, benchmark, field protocol.
- Related skills: `digital-addiction-economics-2026` (the behavioral-economics foundation: habits ~31% of social-media use, commitment WTP) · `neuroadaptive-attention-engineering` · `proactive-agent-design-taxonomy` · `attention-sovereignty-architecture` · `adaptive-digital-nudging-llm-architecture`.