---

name: time-series-db-visualization-pattern
description: Render time-series data as a scrolling multi-series canvas chart with downsampled LTTB buckets and a brushable overview band.
category: design
triggers:
  - time series db visualization pattern
tags: [design, time, series, visualization, canvas]
version: 1.0.0
---

# time-series-db-visualization-pattern

Time-series DB UIs (explorer, query REPL) should separate the **detail viewport** from an **overview band** rendered beneath it. The detail viewport renders only the visible time window using LTTB (Largest-Triangle-Three-Buckets) downsampling — target ~2 points per horizontal pixel, never more. Raw points only render when the zoom level drops below the native retention interval (e.g., 10s resolution); above that, stream pre-aggregated min/max/avg tuples from the DB's built-in rollup (Prometheus `rate()`/`avg_over_time`, Influx `aggregateWindow`, Timescale `time_bucket`). Draw each series on a shared Canvas2D layer, not per-series SVG — SVG collapses past ~5k nodes, and time-series explorers routinely show 50k+ points across 10 series.

Use a **dual-axis time cursor**: a vertical line that snaps to the nearest sample timestamp (not the mouse x-coordinate), with a tooltip pulling the exact stored value rather than an interpolated one. Timestamps must render in both the user's local TZ and UTC simultaneously — ambiguity around DST boundaries is the #1 support complaint for TSDB tooling. The overview band below shows the full queried range downsampled to ~200 points; dragging its brush updates the detail viewport's window without re-querying (client-side zoom within the fetched range), and only fires a new query when the brush extends past the cached range.

Support **gap rendering** explicitly: null/missing samples must draw as broken lines, not zero-interpolated, because TSDB ingestion gaps are semantically meaningful (agent down, not "value=0"). Color-code series by a hashed metric-name-to-hue function so the same metric keeps its color across tabs/sessions without a stateful legend registry.
