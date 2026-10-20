---
name: ios-knowledge-base
description: Versioned iOS 26 / Apple-platform knowledge base that the other ios-ops skills cite — SwiftUI, Liquid Glass, on-device AI, framework routes and deep dives, capability and code recipes, verification proof matrices, and official source registries. Use when an ios-ops skill links into it, or when you need the source-backed reference for an Apple framework, API, or release-proof requirement.
---

# iOS knowledge base

Shared reference library for the ios-ops skills. Every document lives under
`references/` in this skill's directory. Other ios-ops skills link here with
`../ios-knowledge-base/references/<path>`; if your tool installs skills under
prefixed directory names, find this skill by name and resolve the same
`references/<path>` inside it.

## Where to start

- `references/README.md` — learning paths and the route
  `idea -> capability -> framework -> state/data -> UI -> system surface -> verification`.
- `references/coverage-matrix.md` — what is covered and what is still future work.
- `references/sources/` — official source registry and freshness log. Check it before
  calling any claim current.

## Layout

| Directory | Contents |
|---|---|
| `00-foundations/` | Platform foundations and product framing |
| `10-swiftui/` | SwiftUI mental model, state, layout, navigation, accessibility |
| `20-liquid-glass/`, `21-design-deep-dives/` | Liquid Glass adoption and design recipes |
| `30-on-device-ai/`, `31-on-device-ai-recipes/`, `32-apple-intelligence-surfaces/` | Foundation Models, Core ML, Apple Intelligence surfaces |
| `40-framework-routes/` to `44-system-services/` | Framework routing and deep dives |
| `50-capability-recipes/`, `70-code-recipes/` | Capability and code recipes |
| `60-verification/` | Device-backed proof matrices |
| `90-templates/` | Briefs and target plans |

Search the tree for the framework or capability name instead of reading it front to
back. Keep the distinction the documents draw between *verified on a device* and
*only written down*.
