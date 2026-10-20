---
name: apply-statistical-process-control
description: Use when monitoring a repeated process measurement over time and deciding whether a given data point warrants intervention — plot it on a control chart with limits calculated from the process's own historical common-cause variation (not from a target or specification), and only investigate and adjust when a point falls outside those limits or shows a non-random pattern, because reacting to ordinary variation within limits increases variation rather than reducing it.
source: 'Walter A. Shewhart, "Economic Control of Quality of Manufactured Product", Van Nostrand (1931); W. Edwards Deming''s funnel experiment, documented in "Out of the Crisis" (1986) — demonstrates that reacting to common-cause variation increases variation'
tags: [quality-control, spc, six-sigma, manufacturing, process-monitoring, statistics]
related: [apply-pdca, apply-goodharts-law, apply-small-sample-skepticism]
---

# Apply Statistical Process Control

Plot a repeated process measurement on a control chart with limits calculated from the process's own historical common-cause variation, and only investigate or adjust the process when a point falls outside those limits or shows a non-random pattern — because reacting to ordinary variation within calculated limits increases variation rather than reducing it.

## Why This Is Best Practice

**Why best:** SPC's specific contribution is a formal distinction between two categories of variation that look similar moment-to-moment but require opposite responses: common-cause variation is the process's normal, expected, statistically-characterized noise, and reacting to it (adjusting the process based on a single data point that is still within calculated limits) is a well-documented, measurable mistake — Deming's funnel experiment demonstrates that adjusting a stable process in response to its own normal variation increases the total variation rather than decreasing it. Special-cause variation, by contrast — a point outside the calculated control limits, or a specific non-random pattern within them — indicates a genuine, assignable change in the process that does warrant investigation. The discipline of calculating limits from the process's own actual historical behavior, rather than from a target or specification, is what makes the common-cause/special-cause distinction meaningful rather than arbitrary.

**Shewhart, "Economic Control of Quality of Manufactured Product" (1931):** Shewhart, working at Bell Labs, formalized the control chart and the underlying distinction between common-cause and special-cause variation, establishing that a process's center line and control limits (conventionally set at plus or minus three standard deviations from the mean) should be calculated from the process's own historical data, not set arbitrarily or derived from a customer specification. This distinction — statistical control (predictable, stable common-cause variation) as a property of the process itself, separate from whether that variation meets external specification requirements — is the foundational theoretical contribution SPC still rests on.

**Deming's funnel experiment (documented in "Out of the Crisis," 1986):** Deming's widely cited demonstration used a physical funnel dropping marbles toward a target, comparing a strategy of never adjusting the funnel's position against several strategies of adjusting it after each drop based on where the previous marble landed. The demonstration empirically showed that every adjustment strategy responding to normal, common-cause variation produced a wider spread of outcomes around the target than simply leaving the funnel in a fixed position — direct, reproducible evidence that "tampering" (reacting to ordinary variation as though it were meaningful signal) makes a stable process worse, not better.

**Adopted by:** Statistical process control is foundational to Six Sigma and Total Quality Management practice, standard in ISO 9001-certified manufacturing quality systems, and was central to the quality transformation of Japanese manufacturing (including Toyota) following Deming's post-WWII work there; control charts remain standard equipment on manufacturing shop floors globally.
**Impact:** Deming's funnel experiment provides direct, reproducible, quantitative evidence that reacting to common-cause variation (tampering) increases a stable process's total variation rather than reducing it — a counter-intuitive finding with broad practical consequences for any repeated-measurement process, and Shewhart's common-cause/special-cause distinction, now nearly a century old, remains the foundational logic underlying modern statistical quality control practice across manufacturing industries globally.

## Steps

1. **Collect a baseline series of process measurements over time — not a single snapshot — to characterize the process's normal variation.** A control chart's validity depends on having enough historical data to distinguish the process's actual common-cause variation from a single unrepresentative sample.

2. **Calculate the process center line (the mean) and control limits (conventionally plus or minus three standard deviations) from that baseline data.** These limits reflect what the process naturally does, not an arbitrary target or the customer's specification requirement — conflating the two is the specific mistake this technique exists to prevent.

3. **Plot each new measurement on the control chart as it becomes available, in time order.** The chart's value comes from observing variation over time, not from evaluating any single measurement in isolation.

4. **Distinguish common-cause variation (points within the calculated control limits, showing only random fluctuation) from special-cause variation (a point outside the limits, or a specific non-random pattern like a run or trend within them).** Only special-cause variation indicates a genuine, assignable change in the process worth investigating.

5. **When special-cause variation appears, investigate and address the specific assignable cause — do not adjust the process in response to ordinary variation within control limits.** Per Deming's funnel experiment, reacting to common-cause variation as though it were meaningful signal increases total variation rather than reducing it.

6. **Keep control limits (what the process naturally does) explicitly separate from specification limits (what the customer or requirement demands).** A process can be in full statistical control while its natural variation still fails to meet specification — this is a distinct capability problem requiring fundamental process redesign, not a reaction to any individual out-of-control point.

## Rules

- Calculate control limits from the process's own historical common-cause variation, never from an arbitrary target or the customer specification.
- Never adjust a process in response to a single data point that remains within its calculated control limits — this is tampering, and it measurably increases variation rather than reducing it.
- Investigate and correct the specific assignable cause when genuine special-cause variation (a point outside limits, or a specific non-random pattern) is detected.
- Treat "in statistical control" and "capable of meeting specification" as two separate questions requiring two different interventions — being in control does not guarantee meeting specification, and meeting specification once does not mean the process is in control.

## Examples

**Manufacturing dimensional control:** A production line tracks a critical part dimension on a control chart built from historical process data. When a measurement falls outside the calculated control limits, the team stops the line and investigates the specific assignable cause — a worn tool or a material batch change — rather than continuing production or reactively adjusting the machine based on that single reading.

**Avoiding tampering:** An operator watching normal, random fluctuation within control limits is tempted to adjust the machine after every reading. Recognizing this variation as common-cause — the process's expected, natural noise — the operator refrains from adjusting, consistent with Deming's funnel experiment showing that such adjustments increase variation rather than reducing it.

**Control versus capability:** A process is confirmed to be in full statistical control — every point falls within its calculated limits with no non-random patterns — but its natural variation still exceeds the customer's specification tolerance. The team recognizes this as a distinct capability gap requiring fundamental process redesign, not a special-cause investigation triggered by any specific data point, since no individual point is actually out of control.

## Common Mistakes

- **Setting control limits from a target or specification rather than from the process's own actual historical variation.** This produces limits that don't reflect what the process naturally does and undermines the entire common-cause/special-cause distinction.
- **Reacting to every individual data point (tampering) instead of distinguishing common-cause variation, which should be left alone, from special-cause variation, which should be investigated.** Deming's funnel experiment demonstrates this specific mistake increases total process variation.
- **Confusing being "in control" with being "capable."** A stable, predictable process (in control) can still fail to meet specification requirements (not capable) — these require different interventions, and treating them as the same problem misdiagnoses which fix is actually needed.
- **Failing to investigate and correct the specific assignable cause once genuine special-cause variation appears**, treating the control chart as a passive report rather than a trigger for concrete action.

## When NOT to Use

- For a one-off, non-repeating measurement with no time-series history — SPC specifically requires a process observed repeatedly over time to build meaningful control limits from.
- When the underlying process is not yet stable enough to characterize a genuine baseline of common-cause variation (a brand-new process still being tuned) — collect more baseline data before relying on calculated control limits for decision-making.
- As a substitute for addressing a known, confirmed gap between a process's natural variation and its specification requirements — a process correctly shown to be in statistical control can still require separate, fundamental redesign if it isn't capable of meeting specification.
