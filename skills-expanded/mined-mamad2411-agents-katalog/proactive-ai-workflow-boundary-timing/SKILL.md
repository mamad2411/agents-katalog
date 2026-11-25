---
name: proactive-ai-workflow-boundary-timing
description: Evidence-based framework for timing proactive AI interventions at natural workflow boundaries in IDEs. Use when designing proactive AI coding assistants, determining when to surface AI suggestions, or building context-aware developer support systems. NOT for reactive/prompt-based AI assistants or non-IDE contexts.
---

# Proactive AI Workflow Boundary Timing

## Overview
Field study evidence shows that proactive AI suggestions at natural workflow boundaries (post-commit) achieve 52% engagement, while mid-task interventions are dismissed 62% of the time. Well-timed proactive suggestions are interpreted 2x faster than reactive ones.

## When to Use
- Designing proactive AI coding assistants in IDEs
- Determining optimal timing for surfacing AI suggestions
- Building context-aware developer support systems
- Evaluating proactive AI intervention effectiveness
- NOT for reactive/prompt-based AI assistants
- NOT for non-IDE or non-coding contexts

## Core Process / Workflow

### 1. Map Workflow Boundaries
Identify natural task boundaries in the developer workflow:
- **Post-commit**: Highest receptivity (52% engagement) — developer has externalized working memory
- **Post-build/test**: Potential receptive moments
- **Post-task-completion**: Natural evaluative mindset
- **Avoid mid-task**: Low receptivity (31% engagement, 62% dismissal)

### 2. Apply the Index of Opportunity Framework
- Mental workload decreases at task boundaries → natural windows for interruption
- Post-commit: working memory externalized into commit, attentional resources freed
- Mid-task: cognitive resources engaged in active implementation, interventions compete for resources

### 3. Design Intervention Triggers
Rank by receptivity:
1. **Post-commit** (52% engagement): Review changes with AI, code quality suggestions
2. **Ambiguous prompt detection** (46% engagement): Offer guidance when prompt lacks context
3. **Declined AI edit follow-up** (31% engagement): Use sparingly; often perceived as intrusive

### 4. Implement Four Design Principles
1. **Timely**: Anchor interventions to task boundaries; tune down prominence mid-task
2. **Contextually relevant**: Augment context with IDE signals (language servers, git diffs, open tabs)
3. **Explainable**: Clear rationales, previewable changes, confidence indicators
4. **User-controlled**: Lightweight pop-ups before chat invocation; configurable timing/frequency

### 5. Measure Effectiveness
- Engagement rate by trigger type
- Interpretation time (proactive vs. reactive baseline: 45.4s vs 101.4s)
- Dismissal vs. ignore vs. engage rates
- Sustained usage beyond novelty period

## References
- See [references/kuo-2026-proactive-ai-field-study.md](references/kuo-2026-proactive-ai-field-study.md) for full study details.