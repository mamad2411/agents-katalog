# AGENTS.md

## Project Goal

The purpose of this directory is to investigate and mitigate cases where Stillcolor on macOS does not reliably keep temporal dithering disabled.

This is not meant to be theoretical research. The goal is to find a practical and reliable approach that reduces or eliminates situations where dithering silently turns back on.

## What Stillcolor Does

Stillcolor is a macOS app intended to disable GPU/DCP-side temporal dithering on Apple Silicon Macs.

For this project, treat temporal dithering as a real accessibility problem whose presence or absence directly affects usability.

## How To Verify Dithering State

The current verification command is:

```bash
ioreg -lw0 | grep -i enableDither
```

Interpretation:

- `enableDither = No` means dithering is disabled
- `enableDither = Yes` means dithering is enabled

Important notes:

- the output may contain multiple lines
- if all lines are `Yes`, Stillcolor did not actually apply the change at that moment
- if the lines are `No`, Stillcolor has applied the change at least at that moment

## Observed Problem

Stillcolor's menu bar UI may show settings such as:

- `Disable Dithering`
- `Disable uniformity2D`

but that does not always mean dithering is actually disabled.

Observed failure mode:

- Stillcolor appears to be configured to disable dithering
- `ioreg -lw0 | grep -i enableDither` still shows `Yes`
- restarting Stillcolor has been observed to change `enableDither` from `Yes` back to `No`

That suggests one or more of the following:

1. Stillcolor sometimes fails to apply its change
2. Stillcolor applies the change, but later loses effect
3. a system event restores dithering
4. the Stillcolor UI does not always reflect the real system state

## Working Assumptions

Use these assumptions as the starting point:

- restarting Stillcolor can sometimes change `enableDither` from `Yes` to `No`
- the main question is not whether Stillcolor can work at all
- the main question is why the effect does not always remain active

## What This Directory Should Contain

The work in this directory should focus on practical mitigation and diagnostics.

Preferred directions:

### 1. Reproduce The Problem

Identify which events can flip `enableDither` back to `Yes`, including at least:

- Stillcolor launch
- Stillcolor restart
- login
- logout/login
- sleep/wake
- display lock/unlock
- external monitor attach/detach
- resolution or scaling changes
- refresh rate changes
- True Tone on/off
- Night Shift on/off
- HDR on/off

### 2. Automate State Checking

Create small utilities or scripts that:

- check `enableDither` regularly
- log state transitions
- clearly distinguish `Yes` from `No`

### 3. Add Recovery

Find a way to automatically disable dithering again when it turns back on.

Examples:

- watchdog script
- `launchd` agent
- wake hook
- menu bar helper
- combined logging and recovery

### 4. Root Cause Analysis

If possible, determine:

- what Stillcolor changes internally
- why the change does not always persist
- whether the issue is tied to a specific macOS version, Apple Silicon generation, or display state change
- whether the UI reflects desired state instead of actual state

## Do Not Assume

Do not assume:

- the problem is imaginary or purely subjective
- the UI checkmark always reflects the real state
- a running app automatically means the effect is still active
- the issue is irrelevant just because other display variables may also affect comfort

The focus of this project is specific:

**Stillcolor does not always remain effectively applied.**

## Desired Outcome

Good outcomes would include one of the following:

1. a confirmed explanation of which event turns dithering back on
2. a reliable automatic workaround that restores Stillcolor's effect quickly
3. a patch that improves Stillcolor's reliability
4. a diagnostic toolkit that captures precise evidence for later fixes

The most valuable outcome is something that is actually usable in day-to-day work.

## Practical Rules

- prefer small, testable steps
- every hypothesis should be testable
- every test should include before/after verification with:

```bash
ioreg -lw0 | grep -i enableDither
```

- prefer simple and robust scripts
- if you build a watchdog, log:
  - check time
  - observed state
  - action taken
  - result after action

## Suggested First Steps

1. map the events that may change `enableDither`
2. create a minimal state-check script that clearly returns `Yes` or `No`
3. create a minimal watchdog prototype that restarts Stillcolor when the state returns to `Yes`
4. add logging so later analysis can correlate state changes with context
