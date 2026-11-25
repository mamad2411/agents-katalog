---
name: design-audit
description: "Audit configured design tokens and components, 31 UX and motion laws, and task-based persona critics."
---

# Design audit

Config: `.agents/trust-before-scale.json` (else `.claude/trust-before-scale.json`), `routine.extension`,
the host instructions, and the planned base, range and changed surfaces. A missing configured input is a
gap, never a pass. Prefer the host capability in `routine.passes` (commands in `docs/harnesses.md`); this
skill is the fallback. Never invent project rules or roles. In a blind eval with config hidden, use the
routine inputs the prompt supplies and report missing source files.

Report: the command or brief, the reviewed full head SHA, scope, findings (checked file:line, severity, introduced,
worsened or pre-existing), a clean verdict or why no review happened, and limits. Route findings through
the routine. A report with no review is not clean. Never merge.

Read every `routine.designSystem` source before judging: tokens, component library, semantic
colours, typography, spacing, glyphs, states and settled rulings. Use real components and tokens,
not handwritten look-alikes. If none is configured, report “not run: no routine.designSystem
configured” and the coverage gap; do not invent a design system. Missing configured files block
conformance claims. Project rules decide thresholds and conflicts; unresolved conflicts go to the owner.

For each surface grade all 31 checks PASS / FAIL / GAP / RULING / N/A, with visible evidence or
an explicit applicability reason. A missing answer is GAP, not PASS. Numbers below identify checks,
not project decision numbers. Platform examples are guidance; configured binding requirements win.

1. Tesler: absorb complexity with defaults and clear disclosure.
2. Fitts: use reachable targets; respect the configured platform minimum (commonly 44pt or 48dp).
3. Hick and Miller: chunk choices and progressively disclose complexity.
4. Jakob: preserve familiar platform and product patterns.
5. Doherty: respond promptly or show active waiting and queued/confirmed state.
6. Aesthetic usability: use hierarchy and readable typography without hiding failures.
7. Postel: normalize reasonable input and preserve entered work on errors.
8. Peak-end: make completion specific and reassuring; avoid delight on destructive acts.
9. Proximity: group related elements with the configured spacing tokens.
10. Goal gradient: update visible progress alongside the action.
11. Native material: respect platform conventions and user control.
12. Von Restorff: one clear focal action, distinguished by more than colour.
13. Serial position: put key items where they are easiest to recall.
14. Zeigarnik: make drafts and incomplete work resumable.
15. Common region and similarity: group related content and keep equal actions consistent.
16. Prägnanz: use simple shapes and one meaning per glyph.
17. Occam and Pareto: remove complexity that earns no place in the task.
18. Parkinson: reduce effort with safe autofill and remembered details.
19. Selective attention: keep important messages out of decorative banners and fine print.
20. Norman: provide affordances, signifiers, constraints, mapping and immediate feedback.
21. Forgiveness: prevent errors, preserve drafts and offer undo for reversible acts.
22. Default effect: choose defaults serving users with clear ethical opt-in/out.
23. Inclusive design: check contrast, scaling, labels, focus order and non-colour cues.
24. Purposeful motion: show origin, state or attention; remove ornamental movement.
25. Duration/easing: use system timing and direction; keep waits and transitions legible.
26. Spatial continuity: make navigation and shared-element movement understandable.
27. Choreography: establish a lead element and a restrained stagger.
28. Animation principles: use anticipation and settling only when they explain the action.
29. Interruptibility: allow reversal and direct gesture tracking without fighting the user.
30. Reduced motion: honor the preference and avoid vestibular triggers or large autoplay motion.
31. Haptic pairing: pair meaningful feedback sparingly with supported user-controlled actions.

Run a critic panel from `routine.personas`: each role's pressure and real tasks, independently of
the designer's reading. If none is configured, report the gap and request roles rather than
fabricating them. In a running prototype count screens, clicks/taps, typed fields and hesitation;
if unavailable, label an artifact-only review and the owed walk. Findings name persona, task,
consequence and fix. Rank by frequency × consequence: task blocked, daily slowdown, friction, polish.
Review a new surface before building and again afterward. Keep the system violations, law matrix
and critic scorecard separately visible. Quote the binding rule for defects; distinguish guidance.
Route findings through routine, respect settled decisions, fix in-scope defects, and re-grade after
fixes. Record FIXED / OPEN with reason / RULING, including what already works well.
