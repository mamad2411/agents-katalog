---
name: wp-divi-5-extension-architecture
description: Plans a Divi 5 extension's WordPress bootstrap, namespaces, module registration, Visual Builder source, PHP frontend rendering, build output, tests, compatibility boundary, and package contents. Use before creating or substantially restructuring an extension.
---

# wp-divi-5-extension-architecture

Use this skill before implementation when the extension boundary, scaffold, runtime responsibilities, or package structure is not already explicit.

## Required Inputs

- Extension purpose and user-visible capabilities.
- Exact Divi, WordPress, PHP, Node.js, npm, and Composer versions.
- Existing scaffold and package manifests, when present.
- Required module types and dynamic data sources.
- Distribution target and update model.
- Divi 4 compatibility or conversion requirements.
- Security, accessibility, performance, and licensing constraints.

## Decisions to Make

- WordPress plugin bootstrap and activation behavior.
- PHP namespace, Composer autoloading, and module registration.
- JavaScript/TypeScript source and build-entry boundaries.
- `module.json` location and metadata ownership.
- Frontend render ownership and editor/frontend shared contracts.
- Styles, scripts, icons, translations, and generated artifacts.
- Testing layers and fixture strategy.
- Package allowlist and excluded development files.
- Compatibility matrix and fallback policy.

## Workflow

Use [`workflows/plan-divi-extension-workflow.md`](workflows/plan-divi-extension-workflow.md).

## Resource

Use [`resources/extension-architecture-map.md`](resources/extension-architecture-map.md).

## Completion Evidence

Record:

- Chosen architecture and why it fits.
- Every runtime entry point.
- Source versus generated files.
- Module registration and rendering ownership.
- Data and permission boundaries.
- Supported version matrix.
- Build, test, package, install, update, and rollback evidence required.
