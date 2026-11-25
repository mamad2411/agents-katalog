---
name: proactive-ai-intervention-timing
description: Time AI coding assistant interventions based on empirical field-study data to maximize engagement and minimize flow disruption. Covers workflow-boundary targeting, mid-task avoidance, interpretation-time reduction, and the four-phase receptivity model. Use when designing proactive IDE features, calibrating agent interruption policies, or building coding assistants where timing quality determines adoption. NOT for always-on reactive assistants or batch automation.
---

# Proactive AI Intervention Timing

## Overview

Timing is the single largest determinant of whether a proactive AI coding suggestion is engaged or dismissed. A five-day field study of 15 professional developers and 229 AI interventions found that boundary-targeted suggestions achieved 52% engagement, while mid-task interruptions were dismissed 62% of the time. Well-timed proactive suggestions reduced developer interpretation time by 55% compared to reactive requests (45.4s vs. 101.4s, p = 0.0016).

This skill translates those findings into concrete design rules for A-Coder and any IDE building ambient intelligence. The core principle: proactive agents should surface insights when the developer is already transitioning, not when they are immersed.

## When to Use

- Designing proactive IDE features that suggest code quality improvements, security fixes, or refactoring opportunities
- Calibrating when an AI assistant should interrupt vs. stay silent
- Building coding assistants where timing mistakes destroy trust faster than content mistakes
- Evaluating vendor claims about "proactive" coding features against empirical engagement benchmarks
- NOT for always-on reactive chatbots, inline completion, or batch CI jobs

## Core Finding: Boundary vs. Immersion

| Intervention Timing | Engagement Rate | Dismissal Rate | Interpretation Time | Cognitive State |
|---------------------|-----------------|----------------|---------------------|-----------------|
| **Workflow boundaries** (post-commit, pre-push, after test run) | 52% | Low | 45.4s (fast) | Transitioning, reflective |
| **Mid-task** (during edit, on declined suggestion, while debugging) | Low | 62% | 101.4s (slow) | Immersed, high load |

**Interpretation:** Developers are receptive when they are between tasks and cognitively available. They reject intrusions when they are in flow. The 55% interpretation-time reduction at boundaries means boundary-targeted suggestions are not just more accepted — they are faster to process.

## The Four Workflow Boundaries for Proactive Intervention

### 1. Post-Commit (Highest Engagement)
The developer has just finished a unit of work and is mentally switching context. This is the ideal moment for:
- Code quality suggestions (refactoring opportunities introduced by the commit)
- Security scan results affecting the committed files
- Dependency drift alerts (new advisories since last commit)
- Test coverage gaps introduced by the commit

**Implementation rule:** Monitor git commit hooks. Queue insights for the 30-second window after commit completion. Do not show if the developer immediately begins typing in a new file.

### 2. Pre-Push / Pre-PR (High Engagement)
The developer is preparing to share work. Receptivity is high for:
- Lint or style violations that will fail CI
- Merge conflict previews
- Reviewer-impact predictions ("this change affects 3 services — consider adding tests")
- Documentation gap alerts

**Implementation rule:** Trigger when the push/PR creation gesture begins (clicking "Publish Branch" or "Create Pull Request"), not after. Offer a summary, not a blocking gate.

### 3. Post-Test-Run (Medium-High Engagement)
Tests have completed; the developer is evaluating outcomes. Ideal for:
- Flaky test pattern detection
- Regression root-cause hypotheses
- Snapshot drift explanations
- Coverage gap identification

**Implementation rule:** Wait for the full test suite to finish (not during intermediate failures). Summarize in 1–2 sentences with an expandable detail panel.

### 4. Idle / Break Detection (Medium Engagement)
The developer has paused typing for an extended period. Suitable for:
- Long-running background analysis results (architecture drift, security scan)
- Gentle reminders of deferred insights ("You postponed this yesterday — still relevant?")
- Learning nuggets tied to recent code patterns

**Implementation rule:** Require ≥90 seconds of no keyboard activity AND no active debugger session. Never interrupt during compilation or package installation.

## The Mid-Task Danger Zone

**Never proactively interrupt when:**
- The developer is actively typing (keystroke cadence > 1 per 2 seconds)
- A suggestion was just declined (dismissal signals lowered receptivity)
- The debugger is paused on a breakpoint
- A file was modified in the last 10 seconds
- An autocomplete menu is open
- The developer is in a diff/review view

These conditions correlate with the 62% dismissal rate. Violating them trains the developer to distrust the agent entirely.

## The Interpretation-Time Metric

Well-timed proactive suggestions were processed in 45.4 seconds vs. 101.4 seconds for reactive suggestions. The 55% reduction is a proxy for cognitive alignment: the developer already has the relevant context loaded because they are at a boundary, whereas reactive suggestions require reconstructing context from scratch.

**Design implication:** Proactive suggestions at boundaries should be concise (≤3 sentences). The developer is not asking for help — you are offering a timely nudge. Respect their momentum.

## The Cognitive Alignment Hypothesis

The study's statistical finding (r = 0.533, p = 0.0016) suggests that timing quality explains a substantial portion of variance in how quickly developers understand AI suggestions. Cognitive alignment means:
- The suggestion references code the developer was just working on
- The suggestion arrives when the developer is reflecting, not executing
- The suggestion format matches the developer's current mental model (code review vs. inline hint)

**Implementation:** Match insight format to boundary type:
- Post-commit → summary panel with file list and severity badges
- Pre-push → inline diff preview with toggle to accept
- Post-test → collapsible error explanation with stack trace linkage
- Idle → subtle toast with link to detailed report

## Insight Priority Matrix

Not all insights are equal. Use this matrix to decide whether to queue for the next boundary or suppress entirely:

| Severity | Relevance to Current File | Timing Rule |
|----------|---------------------------|-------------|
| Critical (security, data loss) | Directly related | Interrupt even mid-task with modal + escape hatch |
| High (breaking change, test failure) | Same module | Queue for next boundary; notify immediately if boundary > 5 min away |
| Medium (refactor opportunity, style) | Same project | Queue for next boundary; suppress if 2+ queued |
| Low (general tip, learning) | Unrelated | Suppress unless idle > 5 minutes |

## The Dismissal Signal Protocol

When a developer dismisses a proactive suggestion, that is behavioral data. Use it:
- **First dismissal in a session:** Reduce insight frequency by 50% for the next 10 minutes
- **Two dismissals in 15 minutes:** Switch to silent queue only (no notifications; badge only)
- **Three dismissals in a session:** Pause proactive surfacing entirely until the next natural boundary (post-commit or idle > 5 min)
- **Dismissal of a specific insight type:** Down-rank that category for this developer for 24 hours

This prevents the death spiral where untimely suggestions train the developer to ignore all agent output.

## A-Tech Application: A-Coder Boundary Mode

### Current State
A-Coder operates reactively (Level 1) and via spec-driven execution (Level 2). The missing layer is boundary-targeted proactive suggestions.

### Implementation Target
1. **Boundary detector:** Lightweight local parser of git state, test status, and keyboard idle time
2. **Insight queue:** Hold non-critical insights until the next detected boundary
3. **Dismissal tracker:** Per-session behavioral model with backoff rules
4. **Cognitive alignment formatter:** Auto-select format (summary panel, inline diff, toast) based on boundary type
5. **Privacy boundary:** All telemetry (keystrokes, idle time) stays local; only project-level evidence enters sync

### Measurement
- Target engagement rate: ≥ 40% at workflow boundaries
- Target dismissal rate: < 30% overall
- Target interpretation time: < 60 seconds for proactive suggestions
- Developer satisfaction score (1–5): ≥ 4.0 for "timing of suggestions"

## Anti-Patterns

- **Immediate surfacing** — Showing insights the moment they are generated, regardless of developer state. This ignores the 62% dismissal rate.
- **Persistence without adaptation** — Continuing to interrupt mid-task after repeated dismissals. This erodes trust permanently.
- **One-format-fits-all** — Using the same inline popup for post-commit summaries and idle tips. Format mismatch increases cognitive load.
- **Boundary spamming** — Queuing 5+ insights for a single boundary. Overwhelmed developers dismiss everything.
- **Ignoring the pre-push moment** — Waiting until after push to surface CI-likely failures. The developer has already committed to sharing.

## Cross-References
- `developer-experience-and-flow/proactive-agent-design-taxonomy` — The three-level taxonomy and IDQ/CGS/LL evaluation framework
- `developer-experience-and-flow/flow-state-engineering-for-coding-tools` — Neuroscience of flow and interruption recovery costs
- `cognitive-science-and-ux/context-switching-taxonomy-ai-assisted-work` — Measuring context-switch costs that timing must respect
- `developer-experience-and-flow/ai-assisted-engineering-discipline-2026` — Spec-before-code planning that proactive agents monitor
- `developer-experience-and-flow/ai-brain-fry-defense` — Preventing cognitive overload from poorly timed AI output

## References
- See [references/five-day-field-study-summary.md](references/five-day-field-study-summary.md) for the full arXiv paper summary, methodology, and statistical results.
