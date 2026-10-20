---
name: ai-suggestion-micro-interruption-eye-tracking
description: Quantifies the hidden cognitive cost of AI code suggestions using eye-tracking evidence. Use when evaluating AI coding assistant UX, designing suggestion delivery systems, analyzing developer flow disruption, or optimizing AI suggestion timing/presentation. NOT for general productivity metrics without cognitive load context.
---

# AI Suggestion Micro-Interruption Eye-Tracking

## Overview
Eye-tracking evidence reveals that generative AI code suggestions introduce cumulative micro-interruptions that disrupt developer flow, with over half of suggestions never looked at and over 75% of looked-at suggestions rejected.

## When to Use
- Designing AI code suggestion delivery systems and UX
- Evaluating cognitive cost of AI coding assistants
- Optimizing suggestion timing and presentation format
- Analyzing developer flow disruption from AI suggestions
- Building attention-aware AI suggestion systems
- NOT for general productivity measurement without cognitive load context
- NOT for non-coding AI interaction contexts

## Core Process / Workflow

1. **Measure suggestion engagement**: Track fixation rate, dwell time, acceptance/rejection ratios
2. **Quantify micro-interruption cost**: Calculate cumulative cognitive overhead from suggestion volume
3. **Analyze deletion patterns**: Monitor deletion rate spikes around rejected suggestions
4. **Optimize suggestion delivery**:
   - Reduce suggestion volume for lower cognitive overhead
   - Prioritize quality and completeness over frequency
   - Implement temporal awareness (workflow-phase-aware timing)
   - Consider alternative presentation formats (collapsible previews, overlays, side panels)
5. **Design attention-aware systems**: Use developer attention state to inform when to generate

### Key Metrics
- Fixation rate: % of suggestions actually looked at (baseline: 49.5%)
- Acceptance rate: % of looked-at suggestions accepted (baseline: 23.3%)
- Dwell time: avg time looking at suggestion (baseline: 0.9s)
- Micro-interruption frequency: interruptions per session (baseline: ~51 per 45min)
- Deletion rate ratio: deletion rate during vs. outside interruption windows (baseline: 5.8x)
- Startup cost: fixed time to begin reading any suggestion (baseline: 256ms)

### Suggestion Delivery Design Principles
1. **Volume reduction**: Current systems present as uninterrupted stream; reduce frequency
2. **Temporal awareness**: Modulate based on workflow position (more receptive at task boundaries)
3. **Length optimization**: Longer complete suggestions amortize startup cost when correct
4. **Format innovation**: Explore overlays, collapsible previews, side panels vs. inline ghost text
5. **Attention modeling**: Use developer cognitive state to decide whether/when to generate

## References
- See [references/alakmeh-2026-eye-tracking-study.md](references/alakmeh-2026-eye-tracking-study.md) for full study details, methodology, and statistical results.