---
name: crash-triage-analyst
description: Triage Android crash reports from Crashlytics, Sentry, Play Console, or local stack traces — identifying whether it's a recent regression, a known library bug, an OEM/device-specific issue, or a real defect needing a code fix. Use whenever the user pastes a stack trace, mentions Crashlytics/Sentry/Play vitals, asks "why is this crashing", "what does this trace mean", or wants to prioritize a crash backlog. Especially useful for high-volume crashes where the dev needs to decide whether to fix, suppress, or escalate.
---

# Crash Triage Analyst

Most production crashes fall into a small number of buckets. This skill helps you place the crash in its bucket so you know whether it's a 10-minute fix, a workaround, or something to escalate.

## When to use

Triggers: pasted stack trace, "why am I seeing this crash", "Crashlytics", "Sentry", "Play vitals", "ANR" (use ANR skill instead for those), "is this a real bug".

For "fix this bug in my code", just fix it. Use this skill when triage itself is the question.

## Process

### Phase 1: Gather the evidence

Ask for or extract from the report:

- **Full stack trace** (deobfuscated if R8 was on).
- **Affected versions** — does this happen on the latest release, or only old ones?
- **Affected devices/OS** — concentrated on one OEM or Android version?
- **Frequency** — how many sessions affected, what's the trend (rising, flat, falling)?
- **First-seen version** — is there a commit range to bisect?
- **User actions before crash** — breadcrumbs/logs leading up to it.

If a critical piece is missing, ask before guessing.

### Phase 2: Classify

Walk through these in order. Stop at the first match.

**1. Recent regression**
- First-seen version is the current or last release.
- Affects many devices/OS versions broadly.
- → Bisect the commit range, find the change, fix or revert.

**2. OEM / device-specific**
- Concentrated on one manufacturer (Samsung, Xiaomi, Huawei especially) or one OS version.
- Stack trace involves framework or vendor code paths.
- → Workaround in app code (try/catch around the offending API, feature-flag off for affected devices). Don't try to "fix" the OEM bug.

**3. Known library issue**
- Stack trace bottom-frames are in a third-party library.
- → Search the library's issue tracker for the exception class + top frame. Common offenders: WorkManager, AndroidX Lifecycle, Glide, Hilt. If a fix exists, upgrade. If not, work around (downgrade, swap library, or guard the call site).

**4. Process death / restoration**
- `IllegalStateException` from a Fragment / ViewModel / SavedStateHandle on resume.
- `NullPointerException` on a field that was set in `onCreate` but the activity was recreated without the setup running.
- → Restore state via `SavedStateHandle` / `onSaveInstanceState`. Don't assume `Application.onCreate` re-ran.

**5. Lifecycle / coroutine misuse**
- `IllegalStateException: Fragment not attached to a context`.
- `CancellationException` surfacing in unexpected places.
- → Scope coroutines to `viewModelScope` or `viewLifecycleOwner.lifecycleScope`. Guard UI updates with `lifecycle.isAtLeast(STARTED)`.

**6. Background execution restrictions**
- `IllegalStateException: Not allowed to start service Intent` (Android 8+).
- `ForegroundServiceStartNotAllowedException` (Android 12+).
- → Use WorkManager or foreground service with proper trigger context.

**7. Real defect**
- None of the above. The trace points at your code and reproduces with sensible inputs.
- → Fix the bug. This is the case where you actually debug.

### Phase 3: Decide on action

For each crash, pick one:

- **Fix** — write the patch, ship in next release.
- **Workaround** — try/catch, feature flag, version gate. Document why.
- **Watch** — low volume, unclear root cause. Add breadcrumbs or extra logging in next release and revisit.
- **Won't fix** — affects deprecated flow, very old OS version below your `minSdk` target, or a third-party crash you can't influence. Suppress in the crash reporter to keep the dashboard clean.
- **Escalate** — file an issue with the library/OEM if you can repro.

### Phase 4: Prevent recurrence

For categories 4–7, add a guardrail:

- A unit test that exercises the failure path with the same inputs.
- A lint rule or detekt rule for the misuse pattern if it's project-wide.
- An assertion in debug builds (`check(...)` or `error(...)`) that fails early.

## Output

For each crash:

```
Crash: [first line of stack]
Bucket: [1–7 from Phase 2]
Evidence: [one line on what places it here]
Action: [Fix / Workaround / Watch / Won't fix / Escalate]
Fix sketch: [one paragraph or code snippet, if applicable]
```

If triaging multiple crashes at once, sort by `frequency × user impact` and call out which 2–3 to tackle first.

## Common pitfalls

- **Treating obfuscated traces as real.** Always deobfuscate first — R8 makes `a.b.c()` look unrelated to your code.
- **Fixing the most frequent crash instead of the most actionable one.** A 10k-session crash you can't reproduce is worth less than a 200-session one you can.
- **Catching `Throwable` to "make the crash go away".** Suppresses the symptom, leaves the bug. Reserve for true workarounds with a documented reason.
- **Ignoring "first seen in version X".** Often the single most useful field — narrows to a commit range immediately.
