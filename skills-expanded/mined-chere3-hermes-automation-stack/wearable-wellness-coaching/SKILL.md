---
name: wearable-wellness-coaching
description: Design evidence-grounded, non-clinical, safety-bounded coaching rules and daily briefs from consumer health-device data such as sleep, activity, HRV, resting heart rate, breathing rate, SpO2, skin temperature, nutrition, hydration, weight trends, and connected oral-care/hygiene sessions.
---

# Wearable Wellness Coaching

Use this skill when designing rules, prompts, decision logic, or briefings from Fitbit, Google Health, Pixel Watch, Apple Watch, Garmin, Oura, WHOOP, or similar consumer wearables. It also covers non-wearable connected health devices that emit personal behavior metrics—smart toothbrushes (Oral-B iO), scales, blood-pressure cuffs, hydration bottles—where the same non-clinical, provenance-bounded discipline applies. The goal is practical wellness coaching—not diagnosis, treatment, triage by biomarker, or replacement of professional care.

## Core policy

1. Treat wearable outputs as noisy estimates and trends, not clinical measurements.
2. Compare physiologic signals primarily with the person's own baseline or the vendor's personal range. Do not compare HRV between people.
3. Use population guidance for behaviors (sleep duration, weekly activity, diet pattern), not to diagnose from vitals.
4. Never infer a named condition or causal explanation from a wearable pattern. Say that a signal “coincided with” or “departed from the usual pattern,” not that it was caused by illness, stress, dehydration, alcohol, or overtraining.
5. Symptoms and perceived wellbeing override the device. Normal-looking data does not rule out a problem; unusual data does not establish one.
6. Never advise medication/supplement changes, oxygen use, aggressive calorie restriction, fasting, compensatory exercise, forced hydration, or training through concerning symptoms.
7. Make one primary recommendation and at most one secondary recommendation per brief.
8. Do not suppress all recommendations merely because the data are non-clinical. When the user explicitly wants guidance, provide bounded, low-risk wellness actions from personal trends and attach an explicit disclaimer both to the overall result and to each recommendation. For this user, use the Spanish wording: “Estas recomendaciones no tienen veracidad ni validez clínica, no son un diagnóstico y no sustituyen atención médica profesional.” The disclaimer must accompany the action rather than replace or obscure it.

## Evidence workflow

1. Check current official documentation for the exact device/app and supported metrics; vendor terminology and algorithms change.
2. Ground behavioral targets in authoritative public-health guidance (for example, WHO activity, CDC sleep, WHO healthy diet).
3. Use peer-reviewed validation reviews to characterize device limitations. Prefer umbrella reviews and device-specific validation against accepted reference standards.
4. Separate three kinds of numbers in the deliverable:
   - **Evidence-based public-health targets**: cite directly.
   - **Vendor-provided personal ranges or alerts**: preserve their meaning; do not reinterpret clinically.
   - **Product heuristics** (minimum days, persistence windows, reminder intervals): label explicitly as conservative engineering choices, not validated medical thresholds.
5. Include dated links and state when legacy Fitbit pages redirect to current Google Health documentation.

## Connector authorization and production readiness

When the task involves a failed Google Health/Fitbit sync, OAuth refresh, scope selection, consent-screen publishing, or launch verification:

1. Diagnose the failing stage before reauthorizing or changing project settings: secret lookup, OAuth refresh, then individual read-only API categories.
2. Keep diagnostic output free of tokens, authorization codes, full OAuth bodies, and health payloads; status codes and safe error identifiers are sufficient.
3. Distinguish a production server from Google OAuth `In production`, and distinguish a private limited-use client from a publicly launched app.
4. Minimize scopes from the implemented data types. Do not request broad cloud, write, location, ECG, profile, or other adjacent permissions merely because a discovery method lists them.
5. Treat a roughly seven-day `invalid_grant` pattern as evidence of `External` + `Testing` token expiry only after correlating issue time, last success, and first failure.
6. For public launch or user counts beyond Google's unverified limit, prepare truthful per-scope justifications, disclosure, deletion, privacy/terms, verified-domain, and CASA materials. Do not begin a paid security assessment until Google directs it.
7. After any OAuth change, verify token refresh, every required read-only category, database freshness, tests, and absence of newly introduced scopes.
8. When a read-only category intermittently returns `429` or `5xx`, harden the connector rather than reauthorizing: use a small bounded retry budget with incremental backoff for transient HTTP and transport failures only. Fail fast on permanent `4xx` responses.
9. Wrap exhausted request failures in a secret-safe stage label such as `rollup:total-calories failed: HTTP 500`. Never include request URLs, query strings, bearer tokens, response bodies, vendor messages, or health payloads in scheduler output.
10. Add regression tests that prove transient errors retry and recover, permanent errors do not retry, and rendered failures contain the category/status but none of the upstream body. Then run a real minimal sync and verify the normalized database advanced; a green unit suite alone is insufficient.

See `references/google-health-oauth-production.md` for the safe diagnostic ladder, minimal Google Health scopes, private-production versus public-verification decision path, and verification dossier.

For expiring consent links, generate a fresh state-bound URL rather than resending the old one. A new URL supersedes the prior pending authorization. State the short validity window and any network prerequisite in the same message, and do not claim renewal succeeded until the callback and a minimal read-only sync are verified. See `references/google-health-link-renewal.md` for the proven local workflow.

## Multi-source metric reconciliation and provenance

When the same behavior is observed by more than one channel (vendor cloud, local BLE advertisements, a post-session GATT summary, manual entry), reconcile rather than pick a winner:

1. Record every metric as `{value, source, observed_at, quality}`. A brief must be able to say *where* a number came from.
2. Keep raw observations immutable in their own table. Reconciliation rewrites the normalized view only; it never deletes source evidence.
3. Match observations deterministically—device identity, start time within tolerance, duration within tolerance, matching mode. Never match on fuzzy device *names*.
4. Ambiguous matches fail closed: emit separate `partial` sessions rather than inventing one merged session.
5. Apply per-field precedence, not per-record precedence. One source can own coverage while another owns aggregate pressure and a third owns the live timeline.
6. Re-reconcile a rolling window (72 hours is a reasonable default) on every sync, because vendors frequently upload a skeleton record first and enrich it hours later. Reconciliation must be idempotent and order-independent.
7. **Absence is never zero.** A metric the device did not report is `null` / `unavailable`. Rendering it as `0%` fabricates a bad result and will produce a false coaching trigger.
8. Do not promote a vendor's internal index into an anatomical or physiological claim. If the protocol exposes a *timer interval*, it is a timer interval—not a body location—no matter how convenient the relabeling would be.

## Data-quality gate

Before firing any coaching rule:

- Missing data is unknown, never zero.
- Require a vendor-valid/non-null metric and reject known off-wrist, low-battery, incomplete-sync, or poor-signal periods.
- Prefer the vendor's personal range. If computing a baseline, use robust statistics (median/percentiles) rather than a simple mean.
- A reasonable conservative default is 21 valid nights among the previous 28 for nocturnal vitals. Label this as a product heuristic.
- Do not let the current anomalous night immediately rewrite its own baseline; lag baseline updates by 1–2 nights.
- Mark baselines provisional after device/firmware/wrist changes, long gaps, altitude changes, or major routine changes.
- A single outlier should trigger only a quality/context check. A conservative confirmation rule is outside the personal range on 2 of 3 valid nights; call this an engineering heuristic.
- Confidence rises when multiple independent signals and subjective feedback agree.

## Signal-specific rules

### Sleep

- Coach from total sleep duration, regularity, and multi-night trends.
- Do not make consequential decisions from a single night or from REM/deep-stage minutes alone; consumer devices remain limited in stage classification.
- For adults, apply age-appropriate public-health duration guidance only as a behavioral reference.
- Safe suggestions: consistent sleep/wake times, a modestly earlier wind-down, reduced late caffeine, and a dark/quiet environment.
- Never diagnose insomnia or sleep apnea.

### Activity and Active Zone Minutes

- Use flexible weekly goals, not rigid daily quotas. WHO guidance supports 150–300 minutes moderate or 75–150 vigorous aerobic activity weekly for adults, plus muscle strengthening on at least two days, where appropriate.
- For low-activity users, start small; some activity is better than none.
- If weekly activity is behind and recovery signals are stable, suggest a small achievable bout such as a 10–15 minute walk.
- If recent activity is unusually high and multiple recovery signals have shifted, suggest considering a lighter session or rest—not asserting overtraining.
- Never prescribe vigorous activity for people with relevant known conditions, pregnancy, injury, or no prior exposure without deferring to their professional plan.

### Sedentary time

- Encourage replacing sedentary time with any movement. A reminder after roughly 60 continuous minutes and a 2–5 minute movement break can be used as a product heuristic, not a medical cutoff.

### HRV and resting heart rate

- Interpret direction only relative to the person's baseline. An isolated low HRV or high/low resting heart rate is not actionable beyond checking data quality/context.
- Combined persistent drift (for example, resting heart rate above and HRV below personal range) may justify a gentle recovery suggestion if the person feels well.
- Never label tachycardia, bradycardia, infection, stress, dehydration, or overtraining from consumer data.

### Breathing rate, SpO2, and skin temperature

- Use personal-range persistence and symptoms; avoid clinical cutoffs in wellness coaching.
- For isolated SpO2 readings, check fit, position, motion, warmth, battery/signal, and altitude context. Do not prescribe oxygen or breathing interventions.
- Do not call skin-temperature variation “fever”; it is not core body temperature.
- Persistent or repeated vendor alerts should lead only to a recommendation to discuss with a professional, especially if new or accompanied by symptoms.

### Oral care and hygiene sessions

Connected toothbrushes report brushing frequency, duration, mode, pressure states, and—only sometimes—coverage and per-zone time.

- Coach from frequency, duration, and pressure trends across days; a single short session is not actionable.
- Guided/app-assisted sessions and unguided sessions are not equivalent data. Coverage and zone maps typically exist only for guided sessions. Suppress all coverage/zone advice for unguided or incomplete days, and instead suggest running one guided session to obtain a reliable map.
- "Pressure high/normal/low" is a vendor state classification, not a force measurement in newtons. Do not restate it as physical force.
- Suppress pressure advice entirely when no pressure source is present for the period.
- Safe suggestions: complete the two-minute timer, lighten grip and let the brush do the work, keep two sessions per day, spend more time on the zones the app itself flags as low coverage.
- Never infer gingivitis, caries, enamel wear, recession, or any oral disease from device metrics, and never recommend a treatment. Persistent patterns lead only to "discuss with a dental professional."
- Require a minimum history before firing any rule (3+ days is a reasonable conservative default) and require a majority of qualifying days rather than reacting to one.

### Nutrition and hydration

- Evaluate only when logs are sufficiently complete; a conservative product rule is at least 4 complete days among the last 7.
- When completeness is unknown, describe the log as partial and do not infer deficiency or excess.
- Prefer additive, low-risk actions: include fruit/vegetables, minimally processed foods, a routine protein source, or water instead of a sugary drink.
- Do not infer dehydration from HR, HRV, temperature, or a short-term weight change. Avoid universal liter targets without individual context; encourage regular access to fluids and drinking around activity according to thirst/plan.

### Weight
- Ignore daily fluctuations. Prefer a weekly median from at least three comparable weigh-ins and several weeks of trend.
- Only provide weight-loss coaching after an explicit user goal and suppress it for minors, pregnancy, early postpartum, known eating-disorder history, or other safety exclusions.
- Discuss habits and intended trajectory, never moral success/failure or compensation.
- Persistent unintentional change warrants professional consultation without speculating about cause.

## Brief state machine

- **Green — stable:** enough data, no confirmed drift, no concerning symptoms. Reinforce the existing plan.
- **Yellow — uncertain:** one outlier, incomplete data, or changed device/context. Explain uncertainty and ask to observe/recheck.
- **Orange — confirmed recovery-related pattern:** multiple signals or persistent deviation plus relevant subjective feedback. Offer an optional lighter day, regular meals/fluids, and sleep prioritization; do not name a cause.
- **Professional consultation:** persistent signals, repeated official device alerts, ongoing fatigue/palpitations/sleep difficulty, or unintentional weight trend. State only that a professional should assess it.
- **Urgent symptoms:** chest pain/tightness, substantial or worsening breathing difficulty, fainting, confusion, blue lips/face/nails, or other severe symptoms should prompt urgent/emergency services. Do not wait for wearable confirmation or provide a diagnosis.

## Output format

Keep the brief compact:

1. **Data confidence** — high/medium/low and why.
2. **What changed** — relative to the personal pattern.
3. **One concrete action** — optional and achievable.
4. **Uncertainty statement** — the data cannot determine a cause.
5. **Escalation** — only when warranted.
6. **Clinical disclaimer** — attach it to the overall coaching result and every emitted recommendation; keep it short enough that it does not bury the action.

Preferred language:

> Several signals moved away from your recent pattern. This does not identify a cause. If you feel well, consider a lighter day and an earlier sleep routine. If the pattern persists or you have symptoms, discuss it with a professional.

Avoid alarmist language, biomarker score worship, long lists of simultaneous goals, and generic legal disclaimers that obscure the actual action.

## Verification checklist

- Every public-health target has an authoritative citation.
- Every device-specific claim matches current vendor documentation.
- Product heuristics are labeled as heuristics, not evidence-derived clinical cutoffs.
- No disease, causal, medication, supplement, oxygen, calorie-deficit, or universal-hydration instruction appears.
- Missing/low-quality data suppresses coaching rather than generating a zero or negative judgment.
- Every metric carries `source`, `observed_at`, and `quality`; raw observations survive reconciliation.
- Absent metrics render as unavailable, never as `0`. Reconciliation is idempotent and order-independent.
- Vendor internal indices (timer/pacer slots) are not relabeled as anatomical or physiological facts.
- Advice requiring a data class is suppressed when that class is absent for the period (no pressure data → no pressure advice; no guided session → no coverage advice).
- Emitted suggestion text contains no disease, treatment, or diagnostic vocabulary — assert this in tests.
- The brief has no more than two actions and includes escalation only when appropriate.
- Sensitive weight coaching is gated by user intent and exclusions.
- When recommendations are emitted, the overall result and every recommendation contain the required non-clinical disclaimer, while still providing the concrete bounded action the user requested.
- Scheduled connector failures distinguish OAuth, individual API categories, and storage without exposing secrets or health payloads; transient retries are bounded and permanent failures fail fast.
- After connector hardening, both automated tests and a live minimal sync pass, and database freshness is verified read-only.

## Reference material

- See `references/evidence-and-rule-bank.md` for a condensed evidence bank, source links, observed validation limitations, and a reusable rule matrix.
- See `references/google-health-v4-readonly-expansion.md` for a Discovery-first audit workflow, exact data-type/rollup distinctions, scope-schema inconsistencies, source-code coverage checks, and privacy-preserving expansion patterns for profile, settings, ECG, IRN, location, nutrition, sleep, activity, and health metrics.
- See `references/connected-device-metric-reconciliation.md` for multi-source (cloud/BLE/GATT) reconciliation schema, per-field precedence, the pacer-vs-anatomical-zone trap, provenance-preserving storage, and the recommendation gating rules for connected oral-care devices.
