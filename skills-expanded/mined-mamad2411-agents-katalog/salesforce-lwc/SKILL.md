---
name: salesforce-lwc
description: "Design and troubleshoot Lightning Web Components across UI architecture, LDS, UI API, Apex controllers, events, caching, accessibility, SLDS, and client-server contracts."
---

# Salesforce LWC

Design LWCs that are secure, reusable, performant, and aligned with platform-native data access patterns.

## Focus

- Component boundaries and public API
- LDS, UI API, wire adapters, and imperative Apex
- GraphQL query and mutation usage when UI API shapes are a better fit than custom Apex
- Multi-framework app decisions when React is a better fit than LWC for a sandbox or scratch-org experience
- Agentforce Experience Layer component boundaries for conversational and multi-surface UI
- Eventing, state flow, and server contract design
- Accessibility, SLDS usage, and responsive behavior
- Performance, caching, and network minimization
- Metadata configuration and page placement

## Rules

- Prefer LDS and UI API before custom Apex.
- Prefer official platform client APIs such as `lightning/graphql` and base-component type definitions before inventing custom abstractions.
- Do not treat Salesforce Multi-framework as a replacement for LWC. Use it for beta-appropriate React experiences in scratch orgs or sandboxes when the app needs open-framework UI patterns with Salesforce auth, security, governance, GraphQL, and metadata.
- For Agentforce Experience Layer work, define reusable component intent and data contracts once, then verify how each target surface renders or constrains the interaction.
- Keep data contract and presentation concerns separate.
- Make accessibility and security first-order design constraints.
- Minimize server calls and cache where appropriate.

## Required Output

1. Component structure
2. Data access strategy
3. Framework or surface choice
4. Apex contract if needed
5. UX and accessibility notes
6. Performance considerations
