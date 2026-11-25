---
name: openmetrics
description: >-
  OpenMetrics: expose metrics in the OpenMetrics text format for scraping. Covers OpenMetrics. Use when exposing metrics in the OpenMetrics format. Triggers: OpenMetrics.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# OpenMetrics

OpenMetrics 1.0, the metrics exposition format now maintained by the Prometheus project, read from `specification/OpenMetrics.md` in the prometheus/OpenMetrics repository (the Internet-Draft source, draft-richih-opsawg-openmetrics-01). The OpenMetrics 2.0 draft published in the prometheus/docs repository is tracked as a preview.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Exposer (client library, exporter or instrumented service) producing OpenMetrics, or ingestor (scraper or agent) parsing it.
- Target version: OpenMetrics 1.0 (current); OpenMetrics 2.0 (preview, posture: track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **Overview.** "Implementers MUST expose metrics in the OpenMetrics text format in response to a simple HTTP GET request to a documented URL for a given process or device."
2. **Data Model § Strings.** "Strings MUST only consist of valid UTF-8 characters and MAY be zero length."
3. **Data Model § MetricFamily.** "Every Metric within a MetricFamily MUST have a unique LabelSet."
4. **Data Model § Unit.** "If non-empty, it MUST be a suffix of the MetricFamily name separated by an underscore."
5. **Metric Types § Counter.** "A Total is a non-NaN and MUST be monotonically non-decreasing over time, starting from 0."
6. **Metric Types § Histogram.** "Histogram MetricPoints MUST have one bucket with an +Inf threshold."
7. **Data transmission & wire formats.** "Partial or invalid expositions MUST be considered erroneous in their entirety."
8. **Protocol Negotiation.** "Producers MUST use the oldest version of the standard (i.e. 1.0.0) unless requested otherwise by the ingestor."
9. **Text format § Overall Structure.** "The content type MUST be: application/openmetrics-text; version=1.0.0; charset=utf-8"
10. **Text format § Overall Structure.** "Expositions MUST end with EOF and SHOULD end with 'EOF\n'."
11. **Text format § Counter.** "The MetricPoint's Total Value Sample MetricName MUST have the suffix "_total"."
12. **Design Considerations § Statelessness.** "A core design choice is that exposers MUST NOT exclude a metric merely because it has had no recent changes, or observations."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the section it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `prometheus`, `opentelemetry`, `protobuf`, `http-semantics`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [OpenMetrics 1.0 specification](https://raw.githubusercontent.com/prometheus/OpenMetrics/42cbeb674d91064a1ca5cab72741d87159064550/specification/OpenMetrics.md): Internet-Draft source (OpenMetrics 1.0), 1.0 (draft-richih-opsawg-openmetrics-01), main at commit 42cbeb6, checked 2026-10-06.
- [OpenMetrics 2.0 specification (draft)](https://raw.githubusercontent.com/prometheus/docs/605cf81fefc2e8e91f8ba89bb1555ae52a43a318/docs/specs/om/open_metrics_spec_2_0.md): Experimental, 2.0.0-rc0 (Experimental, March 2026), prometheus/docs main at commit 605cf81, checked 2026-10-06.
