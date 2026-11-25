---

name: data-pipeline-visualization-pattern
description: Visual patterns for rendering multi-stage data pipelines with flow direction, stage health, and throughput indicators
category: design
triggers:
  - data pipeline visualization pattern
tags: [design, data, pipeline, visualization]
version: 1.0.0
---

# data-pipeline-visualization-pattern

Data pipeline visualizations benefit from a left-to-right (or top-to-bottom) directed acyclic graph layout where each node represents a processing stage (extract, transform, load, enrich, sink) and edges carry animated particles or flowing gradients proportional to current throughput. Use a three-tier color encoding: saturated green/blue for healthy flow, amber for degraded (lag building, retries climbing), and red for broken/halted stages. Each stage node should expose at-a-glance metrics — records/sec in, records/sec out, lag, error rate — as a compact badge or sparkline embedded in the node, with the full metric panel revealed on hover or click.

For pipeline-flow-visualizer-style apps, animate edge particles at a speed mapped to throughput (faster particles = higher rate) and use particle density to show backpressure buildup between stages. For etl-job-scheduler layouts, overlay a Gantt-like timeline beneath the DAG so users can see both topology and temporal execution (job X started at 02:00, took 14 min, triggered job Y). For stream-throughput-monitor views, pair the DAG with a stacked area chart of throughput per stage over time so spikes and bottlenecks align visually with the stage that caused them.

Critical affordances: make stage boundaries the primary interaction target (not edges), since users diagnose at the stage level; show the "slowest stage" as a persistent badge so bottleneck identification is zero-click; and always render the pipeline in a single viewport without horizontal scroll at typical zoom — collapse or group stages into supernodes when the DAG exceeds ~12 nodes.
