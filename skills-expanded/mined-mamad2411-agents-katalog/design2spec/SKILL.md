---
name: design2spec
description: >
  Convert UI designs (screenshots, mockups, wireframes, or descriptions) into structured
  implementation-ready JSONC specification packages — before any code is written. This skill
  is especially valuable for specialized platforms where jumping straight to code causes real
  damage: Chrome extensions (CSP restrictions, manifest v3 constraints), Splunk React dashboards
  (SDK boundaries, SplunkUI component requirements), Tauri desktop apps (Rust/JS bridge, IPC
  patterns), Electron apps (process isolation, preload scripts), VS Code extensions (webview API
  restrictions), React Native (native module constraints), or any platform with non-obvious
  rules that generic code generation gets wrong. Use this skill whenever the user wants to
  analyze a design and produce a spec, says "prepare a handoff", "create a spec from this
  design", "turn this screenshot into something buildable", or provides a design for a
  specialized system. Also triggers on requests like "I need to build a Chrome extension that
  looks like this", "implement this dashboard in Splunk", or "build this UI as a Tauri app".
  This skill emits structured JSONC specs — it does NOT generate implementation code.
metadata:
  author: kundeng
  version: "1.0.0"
---

# Design-to-Spec Handoff

Convert a reference UI design into an implementation-ready specification package that a downstream coding agent or developer can implement with minimal ambiguity.

## Why this skill exists

Design-to-code is lossy, and the losses compound on specialized platforms. A coding agent looking at a mockup will reach for familiar patterns — but those patterns break when the target is a Chrome extension (CSP blocks inline scripts), a Splunk dashboard (must use SplunkUI components), or a Tauri app (UI runs in a webview with Rust IPC). This skill sits between "here's what it should look like" and "go build it." It forces a structured analysis that surfaces platform constraints, flags architectural decisions, and prevents committing to code before the constraints are understood.

The structured JSONC output works as a discipline gate: the coding agent gets a spec with explicit platform rules, component mappings, and acceptance criteria rather than improvising from a screenshot.

## Core workflow

1. **Analyze the design input** — accept images, screenshots, URLs, mockups, or natural-language descriptions. Extract layout, components, color system, typography, spacing, interaction cues, responsive assumptions, and accessibility implications.

2. **Inspect project context** — if the user provides a codebase or project, infer: framework, component library, styling system, theme/token strategy, routing, build conventions, and existing design-system patterns. Classify as greenfield, retrofit, or extension.

3. **Discover platform constraints** — this is the step generic tools skip. Identify what the target platform forbids, requires, or changes:
   - **Chrome extensions**: manifest v3 schema, CSP restrictions (no inline scripts, no eval), background service worker limitations, popup size constraints, message passing patterns
   - **Splunk dashboards**: SplunkUI component library requirements, dashboard framework SDK, search job patterns, token-based data binding
   - **Tauri apps**: webview restrictions, Rust↔JS IPC bridge (invoke/listen), allowed filesystem APIs, window management, no Node.js runtime
   - **Electron**: main/renderer process split, preload script requirements, context isolation, IPC channels
   - **VS Code extensions**: webview API (postMessage only), no direct DOM access from extension host, contribution points schema
   - **React Native**: no DOM, native module bridge, platform-specific components (iOS/Android), no CSS grid
   - **Standard web apps**: still valuable — surfaces SSR/CSR decisions, hydration boundaries, API route patterns

   If the platform has constraints, populate the `platformConstraints` section in the output. This section is what prevents the downstream coding agent from generating code that looks right but can't run.

4. **Decide starter-pack strategy** — derive from the project, not from a fixed default:
   - Existing codebase → extend current conventions
   - Codebase has design system/tokens/primitives → build spec around those
   - Codebase missing usable foundation → recommend minimum additions
   - Clean-slate → recommend starter pack appropriate to platform/goals, emitted as spec (not code)

5. **Emit the handoff spec** — produce the structured JSONC package (see schema below).

6. **Conform to downstream contracts** — if another spec-driven dev skill exists in the system, detect its schema and conform output to it instead of inventing a new one.

## Operating modes

### Mode A: Existing project / retrofit

Use when the user has an existing repo and wants to add or restyle a screen, flow, or module.

- Inspect existing conventions first
- Emit spec aligned to current architecture
- Recommend only incremental changes
- Do not propose a new stack unless the existing one is clearly unsuitable

### Mode B: Clean-slate / greenfield

Use when no codebase exists and the user wants a new project scaffold recommendation.

- Recommend an appropriate starter pack based on product/platform
- Emit the recommendation as structured spec, not code
- Do not overfit to a single framework unless the project context supports it

## Output format

Default to JSONC. The inline comments serve a specific purpose: they mark inferred decisions and rationale so the downstream agent (or human) can validate assumptions before committing to code. If a downstream skill contract exists, conform to that format instead.

## Output priority

Optimize in this order:

1. Downstream implementability — a coding agent can build from this spec without major ambiguity
2. Compatibility with existing codebase conventions
3. Platform constraint compliance — the spec must not produce code that violates platform rules
4. Design fidelity
5. Maintainability
6. Themeability
7. Verification readiness

## Default JSONC schema

Return these sections in order:

```jsonc
{
  // High-level context about the request and confidence
  "specMetadata": {
    "mode": "retrofit | greenfield",
    "platform": "web | chrome-extension | splunk-dashboard | tauri | electron | vscode-extension | react-native | other",
    "outputFormat": "jsonc",
    "confidence": "high | medium | low",
    "downstreamContract": "system-standard | custom | none",
    "notes": []
  },

  // Starter-pack choice derived from project/codebase context
  "starterPackDecision": {
    "strategy": "reuse-existing | extend-existing | recommend-new-foundation",
    "detectedStack": {
      "framework": "",
      "uiLibrary": "",
      "styling": "",
      "themeSystem": "",
      "routing": "",
      "buildSystem": ""
    },
    "recommendedFoundation": {
      "runtime": "",
      "framework": "",
      "uiSystem": "",
      "styling": "",
      "reasoning": []
    },
    "adaptationNotes": []
  },

  // Platform-specific constraints that downstream code MUST respect.
  // Omit this section entirely for standard web apps with no special constraints.
  "platformConstraints": {
    "platform": "chrome-extension | splunk-dashboard | tauri | electron | vscode-extension | react-native | other",
    "hardRules": [
      // Things that will cause build/runtime failure if violated.
      // e.g., "No inline scripts — Chrome extension CSP blocks them"
      // e.g., "Must use SplunkUI <Table> component, not custom HTML tables"
      // e.g., "No Node.js APIs — Tauri webview has no require/process"
    ],
    "sdkRequirements": [
      // Required SDK components, APIs, or patterns.
      // e.g., "Use chrome.runtime.sendMessage for background communication"
      // e.g., "Use @splunk/react-ui for all UI components"
      // e.g., "Use Tauri invoke() for all Rust backend calls"
    ],
    "manifestOrConfig": {
      // Platform-specific config the project needs.
      // e.g., Chrome: { "manifest_version": 3, "permissions": [...] }
      // e.g., Tauri: { "allowlist": { "fs": { "scope": [...] } } }
    },
    "forbiddenPatterns": [
      // Common web patterns that break on this platform.
      // e.g., "No localStorage in service workers (Chrome MV3)"
      // e.g., "No window.fetch in Electron main process"
      // e.g., "No CSS grid in React Native"
    ],
    "notes": []
  },

  // Structured design description derived from image/mockup/app context
  "designBrief": {
    "productContext": {
      "appType": "",
      "screenName": "",
      "primaryUserGoal": "",
      "primaryActions": []
    },
    "layout": {
      "shell": "",
      "regions": [],
      "hierarchy": [],
      "responsiveReflow": []
    },
    "components": [
      {
        "name": "",
        "role": "",
        "variants": [],
        "states": [],
        "notes": []
      }
    ],
    "designSystem": {
      "colorRoles": {
        "primary": "",
        "secondary": "",
        "background": "",
        "surface": "",
        "text": "",
        "muted": "",
        "success": "",
        "warning": "",
        "danger": ""
      },
      "typography": {
        "style": "",
        "scale": {}
      },
      "spacing": {},
      "radius": {},
      "shadow": {},
      "motion": []
    },
    "contentModel": {
      "dataEntities": [],
      "mockDataNeeded": true
    },
    "accessibility": {
      "contrastNotes": [],
      "keyboardNotes": [],
      "semanticNotes": []
    },
    "inferred": []
  },

  // Implementation-oriented brief for downstream coding agent
  "developerBrief": {
    "goal": "",
    "implementationConstraints": [],
    "architectureNotes": [],
    "themeNotes": [],
    "riskNotes": []
  },

  // Maps design to implementation touchpoints
  "adaptationOrFilePlan": {
    "domains": [],
    "filesOrModules": [
      {
        "pathOrArea": "",
        "purpose": "",
        "changeType": "create | update | verify"
      }
    ]
  },

  // What downstream coding agent must satisfy
  "acceptanceCriteria": [],

  // Notes for downstream implementation
  "handoffNotes": {
    "preferredNextStep": "implement-spec",
    "downstreamSkillHints": [],
    "unknowns": [],
    "assumptionsSafeToProceed": []
  },

  // Verification hooks for coding or QA skill
  "verificationChecklist": [
    {
      "name": "design-fidelity",
      "checks": []
    },
    {
      "name": "responsiveness",
      "checks": []
    },
    {
      "name": "theme-integrity",
      "checks": []
    },
    {
      "name": "platform-compliance",
      // Only when platformConstraints section is present.
      // Verify that hardRules and forbiddenPatterns are not violated.
      "checks": []
    },
    {
      "name": "maintainability",
      "checks": []
    }
  ]
}
```

## What NOT to do

- Do not generate implementation code — this skill's job is the spec, not the build. The spec is a checkpoint that prevents committing to code before constraints are understood.
- Do not force a new stack when adapting an existing codebase is more appropriate.
- Do not hide inferred decisions — mark them with JSONC comments so downstream consumers can validate or override.
- Do not skip platform constraint discovery for specialized targets. A spec that ignores Chrome CSP rules or Splunk SDK requirements will produce code that looks right but fails at runtime.
- Do not overfit to a single framework unless the project context supports it.
