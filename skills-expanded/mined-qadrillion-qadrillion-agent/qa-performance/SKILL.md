---
name: qa-performance
description: Author and execute bounded performance checks with an explicit workload, baseline, thresholds and diagnosis. Apply when latency, throughput, capacity or resource regressions are in scope.
---

# Performance execution

Use through `qa` as a risk overlay; read `.agent/rules/test-automation.md`.
Use an existing team harness when present. A timing assertion, a browser audit
and a load test answer different questions; choose the one the decision needs.

## Define the experiment

Write the performance question before generating traffic. Record operation mix,
dataset, arrival/concurrency model, connection behavior, cache state, warmup,
measurement duration, sample count and observation boundary. Identify client,
network and target/build/configuration; compare equivalent environments.

Choose thresholds from requirements or an explicitly declared diagnostic budget,
never from whichever measurement just passed. Define successful-content checks,
latency percentiles, error/timeout limits and required completed work. Separate
threshold failure from an emergency stop. A baseline supports relative change;
it does not establish that the baseline itself is acceptable.

Set maximum request count, concurrency/rate, duration, per-request timeout and
permitted resource footprint. Define stop signals and who/what observes them:
unexpected identity, sustained error rise, saturation, fixture growth or loss of
telemetry needed for safe execution. Use only the task's authorized isolated
target; a production-like label is not target verification.

## Author and run

Verify a single request's business result and cleanup before scaling. Make the
harness fail when a threshold fails; logging a check failure while exiting zero
is insufficient. Record scheduled, attempted, completed, errored and interrupted
work; generator inability to achieve the intended workload is a coverage gap.

For a closed workload, fixed workers wait for responses before sending more;
latency growth therefore reduces offered traffic. Use an open arrival model when
the question requires arrivals independent of response time, and observe dropped
work. A sequential probe is useful for local response regressions but cannot
establish capacity or behavior under sustained arrivals.

Execute the declared warmup and measured phase, keeping their samples distinct.
Collect individual samples or suitable histograms, error details, throughput and
tail latency. Include timeout/error counts even when percentiles describe only
successful responses. Explain the population and quantile method. Small samples
and short runs limit tail and stability claims; a p99 from a handful of requests
does not provide a stable estimate. Retain the first failing experiment.

## Diagnose against the baseline

Compare the same workload on baseline and candidate, separating cold/warm cache
and successful/error latency. Check achieved workload and generator resource
limits before blaming the target. Correlate timestamps with utilization,
saturation, errors and traces for the critical path where available.

Form one bottleneck hypothesis, change one relevant factor and measure its
predicted effect. Report unavailable telemetry as unknown. A fix needs a new
linked measurement with unchanged acceptance thresholds, not an assertion that
the code looks faster. Broader experiments need a revised workload and limits.

## Maintain

Version the workload, dataset seed and thresholds together; retain comparable
baseline artifacts with build/config identity. Change thresholds for an approved
requirement or experimental design change, not to hide a regression. Keep short
regression probes separate from sustained load/soak exercises and document what
CI hardware variance prevents them from deciding.

For this repository's bounded local HTTP helper, read
[the measurement recipe](references/local-http.md). For an existing k6 project,
read [workload and threshold adaptation](references/k6.md); no tool migration is
required. Browser rendering and mobile startup/frame/resource checks use their
native measurement boundaries rather than treating HTTP time as total UX time.
