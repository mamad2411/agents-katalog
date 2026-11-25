---
name: mols-mermaid-chart
description: "Use for Mermaid bar, line, XY, pie, Sankey, treemap, radar, or quadrant requests when the reader must compare numeric categories, inspect an ordered or time-based trend, explain part-to-whole composition, trace quantified flow, compare weighted hierarchy, evaluate same-scale profiles, or position items on normalized axes. Preserve source values, units, order, population, and time basis. Do not use for procedures, handoffs, states, architecture, schema, unweighted hierarchy, or event order; route those to mols-mermaid-diagram. Route whole-dashboard design to mols-markdown-dashboard."
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
  - agentsskills
---

# Mermaid Chart

## Purpose

Mermaid로 **수치 구조를 빠르고 쉽게 읽을 수 있는 chart-as-code**를 생성하거나 개선한다.

Category 비교, 시간 추세, 구성비, 양적 이동, 계층 규모, multidimensional profile과 two-axis positioning에 사용한다. Histogram, box plot, scatter처럼 Mermaid가 직접 지원하지 않는 chart는 table이나 전문 chart 도구로 보낸다.

## References

- 새 chart를 만들거나 type·구조를 바꿀 때 [Mermaid Chart Reference](references/mermaid-charts.md)를 읽는다.
- theme, palette, 강조 또는 기존 chart의 visual language를 다룰 때만 [Style Policy](references/style-policy.md)를 읽는다.
- 문법이 필요하면 [Examples](references/examples/README.md)에서 선택한 type의 문서만 읽는다.
- render, export, syntax error 또는 compatibility 확인이 필요할 때 [Verification](references/mermaid-chart-verification.md)을 읽는다.

## Workflow

1. 독자가 chart로 답해야 하는 **수치 질문**을 한 문장으로 정의한다.
1. source, 단위, 기준 시점, 모집단, 순서와 누락값을 확인한다.
1. 질문에 가장 직접적인 chart type과 target renderer 지원 여부를 확인한다.
1. 값·sign·scale·order를 보존하고 축, label, series를 최소한으로 설계한다.
1. 정확한 값이 중요하면 source table을 함께 제공한다.
1. inline Markdown, `.mmd` 또는 rendered artifact 중 필요한 output만 만든다.
1. 필요한 수준까지 검증하고 data caveat와 renderer 제약을 보고한다.

## Editing Rules

- 기존 chart는 요청 범위만 수정하고 theme, series order, label convention과 visual language를 불필요하게 바꾸지 않는다.
- 원문에 없는 값·순위·추세·상관관계를 만들지 않는다.
- 하나의 chart에는 하나의 핵심 수치 질문만 둔다.
- 같은 정보를 chart와 table로 반복하지 않는다. 정확한 값 보존이 필요할 때만 table을 병기한다.
- 복잡도를 style로 덮지 말고 chart를 분리하거나 더 단순한 표현으로 전환한다.
