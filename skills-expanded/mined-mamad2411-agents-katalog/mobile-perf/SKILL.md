---
name: mobile-perf
description: Set mobile perf budgets — cold start (TTI), warm start, scroll FPS, memory; per audience device tier (low-end Android baseline); identify the dominant cost. Native only; not web CWV.
---

# mobile-perf

> Mobile perf is about the low-end Android in someone's hand, not the iPhone on your desk. Output is a budget per critical screen + the dominant cost.

## When to use

- A mobile app or screen is being designed/built.
- Users complain "the app is slow" but the team doesn't know which axis.

## The budget axes

For each critical screen / journey, pin all four:

- **Cold start TTI**: app launched fresh → first interactive frame. Target: < 2s on low-end Android.
- **Warm start TTI**: app foregrounded from background. Target: < 500ms.
- **Scroll FPS**: target 60 fps on lists; flag if < 55 sustained.
- **Memory ceiling**: target stays under the OS's foreground-app memory bucket for the audience device (typically 200–400 MB on low-end Android).

## Audience device tier

Pin which device represents the audience. The fastest dev phone in the office is not it.

- **Low-end Android baseline**: ~2-year-old mid-range Android. The Pixel 6a / Galaxy A series. < 6 GB RAM, mid-tier SoC.
- **Median Android**: current-year flagship Android.
- **iPhone tier**: current iPhone or 2-year-old iPhone — much smaller perf variance than Android.

For consumer apps, low-end Android is almost always the right baseline.

## Procedure

1. **Pick the screen / journey** (one at a time; multiple screens = multiple passes).
2. **Pin the 4 axes** with target values.
3. **Measure current state** with the audience device tier. Real device, not simulator.
4. **Identify the dominant cost** of any axis missing its target. Common culprits:
   - **Cold start**: too many libraries loaded synchronously, premature DB warm-up, oversized launch storyboard.
   - **Warm start**: app re-initializes state instead of restoring it.
   - **Scroll FPS**: heavy item rendering, missing recycling, layout thrash, JS thread blocking (RN/Flutter).
   - **Memory**: bitmap caching unbounded, leaks in adapter/list controllers, large hero images undowngraded.
5. **Recommend ONE fix** with expected effect.

## Output

```text
Mobile perf budget: /home screen (cold start)

Audience device: low-end Android (Pixel 6a, 6 GB RAM, Cortex-A78).

Targets:
  Cold start TTI    : < 2,000 ms
  Warm start TTI    : <   500 ms
  Scroll FPS        : ≥ 55 fps
  Memory (foreground): < 250 MB

Current (measured on Pixel 6a, low-battery mode off, release build):
  Cold start: 3,400 ms   ← over budget
  Warm start:   380 ms   ok
  Scroll FPS :  58 fps   ok
  Memory     : 210 MB    ok

Dominant cost (cold start):
  4 SDKs are initialized synchronously in onCreate (analytics, push, crash,
  feature flags). Together ~1,600 ms.

First fix:
  Move 3 of 4 SDKs to async init after the first frame. The crash SDK stays
  synchronous (must capture early crashes). Expected: cold start ~1,800 ms,
  under target. Validate on Pixel 6a release build.
```

## Quality bar

- Audience device tier pinned (real device name).
- All 4 axes have target + measured value.
- One dominant cost named for any failing axis.
- One first fix with expected effect.

## Anti-patterns to avoid

- Measuring on a Pixel 9 Pro and shipping.
- Optimizing scroll FPS when cold start is failing. Fix the failing axis first.
- "Add a splash screen" to hide cold start. Hides the symptom; doesn't fix it.
- Single-axis budget. Always pin all 4.
