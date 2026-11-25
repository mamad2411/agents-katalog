---
name: domain-frontend
description: Apply web scenario, interface and accessibility guidance to frontend work in the current action scope.
---

# Implement the user's web scenario

- Identify route, user action, reused components/tokens, data contract and state owner. Preserve agreed visual direction/design system. Explore visual choices for a new or explicitly redesigned surface; bug fixes do not authorize a palette, font dependency or layout replacement.
- Cover relevant loading, empty, error, success, stale-response and repeated-submit states. Trace request identity/order to the rendered result: late responses must not overwrite newer intent. Show success/proven outcomes only from corresponding runtime state. A disabled button alone does not establish server idempotency.
- Use semantic controls: buttons for actions, links for navigation, named icon controls and labeled fields. Keep keyboard access/visible focus; overlays must not hide focus, and dragging needs accessible alternatives when applicable. Announce important async results without flooding assistive technology.
- Verify relevant viewports, long content, overflow and zoom. Honor reduced motion; ongoing decorative motion needs appropriate stopping controls. Give typography/layout hierarchy tied to real content. Decoration/game animation must not obscure controls or invent activity. Match action names and result messages; error/empty copy explains the next useful step.
- Keep secrets out of bundles and untrusted text out of executable HTML. Measure the relevant bottleneck before cache/memoization, virtualization or bundle changes. Preserve framework/component contracts; this method installs no tools and fetches no floating rules.
- Propose real browser scenarios when allowed. Build/unit/mock success or a component quote cannot establish interaction, visual quality, persistence or subjective acceptance. Use suitable registered verification or contract human acceptance. Missing verifiers leave requirements unverified; never invoke forbidden tools in a read-only AI action.

Modified adaptation of anthropics/skills frontend-design and selected vercel-labs/web-interface-guidelines rules: project direction wins; auto-memory, universal aesthetics and extra lifecycle removed. [Anthropic Apache-2.0](../licenses/anthropics-frontend-design-Apache-2.0.txt); Copyright (c) 2025 Vercel Labs, [MIT](../licenses/vercel-web-interface-guidelines-MIT.txt). Sources/changes: [PROVENANCE](../PROVENANCE.json). No vercel-labs/agent-skills React/composition text imported.
