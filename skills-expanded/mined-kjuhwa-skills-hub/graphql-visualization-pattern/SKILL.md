---

name: graphql-visualization-pattern
description: Visualizing GraphQL operations (queries, schemas, subscriptions) through interactive node-graph and live-feed UIs
category: design
triggers:
  - graphql visualization pattern
tags: [design, graphql, visualization, node, schema]
version: 1.0.0
---

# graphql-visualization-pattern

GraphQL's strength is its introspectable, typed, hierarchical nature — so visualizations should exploit that structure rather than treat operations as opaque text. For a query builder, render the schema as a collapsible tree where each field exposes its type, arguments, and nullability, and let the user toggle selection nodes that compile into a valid selection set in a live preview pane. For a schema grapher, draw types as nodes and field-references as directed edges (object→object, interface→implementer, union→member), with arrow style encoding list/non-null modifiers and edge color encoding relationship kind. For a subscription feed, render each pushed payload as a timestamped card keyed by subscription root field, with a running delta indicator showing which fields changed since the previous event.

The unifying pattern is **schema-derived layout**: never hand-author the visualization structure — derive it from an introspection result (`__schema`) or a parsed SDL AST. This lets the same component render any GraphQL endpoint and auto-adapts when the schema evolves. Use a left-rail type/field picker, a center canvas for the graph or builder, and a right-rail detail panel showing the selected node's description, directives, and deprecation reason. Force-directed layout works for schema graphs <200 types; above that, switch to a cluster-by-module or collapsible-by-namespace view to avoid hairballs.

Keep rendering concerns orthogonal to GraphQL semantics: the visualization layer should consume a normalized `{nodes, edges, metadata}` shape produced by a separate schema-parser module. That separation lets you swap the renderer (SVG, Canvas, react-flow, d3) without touching introspection code, and lets you unit-test schema parsing against fixture SDL files independently of DOM.
