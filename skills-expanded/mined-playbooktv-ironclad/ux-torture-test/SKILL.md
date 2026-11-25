---
name: ux-torture-test
description: Break a user interface under real-world conditions across responsiveness, hostile content, interaction states, accessibility, network failure, interruption, and complete user journeys, reporting observable user harm with evidence rather than aesthetic opinion. Use whenever the user wants to stress-test a UI, verify responsive and edge-case behaviour, inspect loading/error/empty/recovery states, review a flow for friction, or find where an interface fails under reality. Part of the audit suite; inherits the shared constitution while its own job is proving observable user harm.
---

# UX Torture Test

**Epistemology: prove observable user harm, not aesthetic opinion.**

An agent turned loose on a UI can generate infinite "this could be cleaner" commentary. This skill reports defects and friction only when tied to a real user goal and evidence.

Read `references/CONSTITUTION.md` first.

## The evidence gate

A defect or friction finding requires:

1. **User goal** — what the user is trying to accomplish.
2. **Observed obstruction** — the exact thing that blocks, confuses, misleads, or increases error risk.
3. **Consequence** — abandonment, lost work, wrong action, repeated effort, uncertainty, exclusion, or recovery cost.
4. **Evidence** — concrete viewport, zoom, content, state, input method, network condition, sequence, or runtime observation.
5. **Reproduction path** — precise steps and environment.

If all five cannot be supplied, classify it as a **research hypothesis** or discard it. Do not soften opinion into a defect.

## Phase 0: Define user objectives and critical journeys

Identify:

- primary user roles;
- first-time and returning-user goals;
- top critical journeys;
- irreversible/destructive actions;
- financially or operationally sensitive steps;
- important recovery paths;
- known analytics/drop-off evidence if available.

Define success for each journey before judging friction.

## Phase 1: Reconnaissance

Map:

- routes/screens and journey transitions;
- responsive primitives and breakpoints;
- shared components and tokens;
- forms and mutations;
- state/data ownership;
- overlays, navigation, menus, focus behaviour;
- loading/error/empty patterns;
- localisation and RTL support;
- browser/runtime test setup;
- known accessibility utilities and automated checks.

Inspect implementation and run the interface where possible.

## Phase 2: Journey friction pass

Trace critical objectives end to end as a first-time user and, where relevant, a returning user.

Hunt for:

- unnecessary decisions;
- premature information requests;
- repeated entry;
- unclear next action;
- terminology drift;
- weak system status;
- hidden prerequisites;
- dead ends;
- forced context switching;
- destructive ambiguity;
- lost work;
- recovery requiring refresh or restart;
- success states that fail to establish what happened next.

A friction finding must pass the evidence gate. If the consequence depends on user preference or behaviour that has not been observed, mark it `RESEARCH HYPOTHESIS`.

## Phase 3: State completeness and transition integrity

Inventory meaningful user actions and data views. Map only applicable states:

- idle;
- hover/focus/active;
- pending;
- success;
- failure;
- partial success;
- retry/recovery;
- disabled and reason;
- first-use empty;
- filtered empty;
- no-permission;
- failed-to-load;
- stale;
- offline;
- interrupted;
- conflict.

Do not merely check that states exist. Test transitions:

`ready → action → pending → acknowledgement → persistence → reconciliation → feedback → recovery`

Ask:

- Can repeat action duplicate effects?
- Can success appear before durable success?
- Can failure lose user input?
- Can retry duplicate work?
- Can partial success be distinguished from total failure?
- Can stale/conflicting data be recognised?
- Does navigation interruption leave ambiguous outcome?
- Is disabled state explained when action is expected?

## Phase 4: Environmental torture pass

Test strategically across combinations, not only isolated dimensions.

Conditions include, where applicable:

- 320px narrow viewport;
- mobile landscape;
- tablet;
- common desktop;
- ultrawide;
- 200% and 400% zoom;
- OS/browser large text;
- long names, emails, URLs, and unbroken strings;
- localisation expansion;
- Unicode, emoji, and non-Latin scripts;
- RTL;
- empty, one-item, many-item, and huge datasets;
- zero and extreme numeric values;
- slow, failed, and missing images;
- dynamic mobile viewport and on-screen keyboard;
- safe areas/notches;
- orientation change;
- reduced motion;
- slow network;
- timeout;
- offline;
- interrupted mutation;
- back/forward navigation;
- refresh during pending action;
- stale tab;
- multiple tabs;
- expired session;
- downgraded permission where relevant.

Prioritise combinations likely to compound harm, such as narrow viewport + large text + long localisation, or slow network + repeated submit + navigation away.

## Phase 5: Accessibility interaction pass

At minimum, where tooling permits:

- complete critical journeys keyboard-only;
- verify logical focus order and visible focus;
- test modal/menu focus containment and restoration;
- inspect accessible names and semantics;
- test form validation announcement and recovery;
- test zoom and reflow;
- inspect target sizes;
- verify meaning is not communicated by colour alone;
- test reduced-motion behaviour;
- inspect dynamic status/error announcement where relevant.

Automated scanners are supporting evidence, not a substitute for interaction testing.

Do not claim WCAG conformance from this skill. Use `PASS WITHIN TESTED SCOPE`.

## Phase 6: Visual and behavioural consistency

Report consistency issues only when they create expectation mismatch or task harm.

Look for:

- same appearance, different behaviour;
- same behaviour, materially different presentation;
- inconsistent save models;
- inconsistent Enter/Escape/Back behaviour;
- token drift that causes hierarchy or affordance confusion;
- inconsistent pending/disabled/error treatment;
- responsive divergence without product reason;
- terminology inconsistency affecting comprehension.

Distinguish intentional variation from drift.

## Phase 7: Browser/runtime orchestration

For each critical journey, build a small torture matrix combining:

- viewport;
- content extreme;
- network state;
- session/permission state;
- input method;
- interruption/navigation condition.

Record exact environment and result.

Use browser developer tools where available to inspect:

- console errors;
- network requests and retries;
- duplicate requests;
- response timing;
- storage/session state;
- layout shifts;
- accessibility tree;
- focus order.

Static review should generate hypotheses. Runtime testing should prove or disprove them.

## Phase 8: Verification and prioritisation

Re-run High-impact findings from a clean state. Preserve screenshots, recordings, traces, or exact steps where possible.

Prioritise using:

- user harm;
- frequency/reach;
- journey criticality;
- recoverability;
- exclusion/accessibility impact;
- business consequence.

Separate:

- `CONFIRMED DEFECT`
- `HIGH CONFIDENCE`
- `RESEARCH HYPOTHESIS`
- `NOT TESTED`

## Report format

```markdown
# UX Torture Report — [surface/flow]

**Status:** WITHSTANDS WITHIN TESTED SCOPE | HARM FOUND | PARTIAL
**Declared scope:** [...]
**Critical journeys tested:** [...]

## Torture matrix
| Journey | Environment/state combination | Result | Evidence |

## Findings

### [Severity] · [Journey / State / Environmental / Accessibility / Consistency] · [title]
- **User goal:** [...]
- **Obstruction:** [...]
- **Consequence:** [...]
- **Evidence:** [...]
- **Reproduction:** [...]
- **Fix:** [...]
- **Confidence:** Confirmed | High Confidence | Research Hypothesis

## State coverage gaps
[...]

## Research hypotheses
[...]

## Not tested
[...]

## Retest plan
[Exact journeys and conditions to repeat after remediation.]
```

## Anti-patterns

- The opinion generator.
- Aesthetic drift disguised as user harm.
- Happy-path-only testing.
- Checking states without testing transitions.
- Testing dimensions individually when the failure comes from combinations.
- Vague reproduction such as "mobile is bad."
- Claiming accessibility conformance from a limited pass.
- Treating a research hypothesis as a confirmed defect.
