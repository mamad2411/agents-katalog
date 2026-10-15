---
name: openeditor-project-setup
description: Inspect an existing repo and generate OpenEditor onboarding config for it. Use when Codex needs to make a project OpenEditor-compatible by inferring framework or platform from the file tree, creating or updating `.logic-editor.json`, creating `oe-swift.json` for iOS or SwiftUI projects, or explaining which config fields still need manual confirmation.
---

# OpenEditor Project Setup

## Quick Start

Use this skill to onboard an arbitrary repo into OpenEditor. The output is usually:

- `.logic-editor.json`
- `oe-swift.json` for iOS or SwiftUI repos
- a short explanation of what was inferred vs. what still needs confirmation

When the repo signals are sufficient, generate the file contents directly.
Do not ask the user for the `.logic-editor.json` or `oe-swift.json` schema when the references in this skill already cover it.

Read only the references you need:

- Always read [references/project-config.md](references/project-config.md)
- Read [references/project-detection.md](references/project-detection.md) when inferring framework, port, or run command
- Read [references/ios-config.md](references/ios-config.md) only for iOS or SwiftUI projects

## Workflow

### 1. Inspect the repo first

Look for the smallest high-signal set of inputs:

- `package.json`
- lockfiles such as `bun.lockb`, `bun.lock`, `package-lock.json`, or `pnpm-lock.yaml`
- framework folders such as `app/`, `pages/`, `src/`, `templates/`, `layout/`
- iOS signals such as `*.xcodeproj`, `*.xcworkspace`, and `*.swift`
- any existing `.logic-editor.json` or `oe-swift.json`

Do not invent support for frameworks that the references do not cover.

### 2. Infer the project type conservatively

Prefer the real parser defaults from the references over generic assumptions.

- `next` -> port `3000`, run command `npm run dev` or `bun dev` when Bun lockfiles are present
- `astro` -> port `4321`
- `expo` -> port `8081`, run command `npx expo start`
- `react-native` -> port `8081`, run command `npm start` or `bun start`
- Vite React -> port `5173`
- Shopify theme -> port `9292`, run command `shopify theme dev`
- iOS -> port `0`, empty `runCommand`, plus `oe-swift.json`
- Unknown web repo -> default to `type: "unknown"`, port `5173`, run command `npm run dev`

If the evidence is mixed, explain that uncertainty instead of pretending confidence.

### 3. Generate the smallest correct config

Rules:

- Keep `.logic-editor.json` minimal unless the repo clearly supports more
- Do not add speculative routes or URL-state variants just to look smart
- If route discovery is weak, emit a single home route:
  - `{ "path": "/", "label": "Home" }`
- Preserve existing config when updating; merge carefully instead of replacing unrelated fields
- Do not invent unsupported keys

### 4. Only generate `oe-swift.json` for real iOS projects

When the repo is SwiftUI or Xcode-based:

- infer `scheme` from the `.xcodeproj` or `.xcworkspace` name when possible
- default simulator to `iPhone 16 Pro`
- infer views from obvious `*View.swift` files
- keep view entries simple unless the repo provides stronger signals
- do not fabricate bundle IDs, deep links, or accessibility tap metadata unless the repo exposes them

### 5. Explain assumptions explicitly

After the config output, include a short explanation covering:

- detected framework or platform
- chosen port and run command
- whether routes were inferred or defaulted
- whether `oe-swift.json` was generated and why
- which fields should be manually confirmed

### 6. Prefer generation over schema questions

If the repo is a supported type and the references here cover the config format:

- generate the file contents directly
- use conservative defaults when some fields are weakly signaled
- ask follow-up questions only when a missing field would make the config invalid or misleading

Do not stop with "I need the schema" for normal React, Next, Astro, Expo, React Native, Shopify, or iOS repos.

## Output Rules

When the user asks for file contents, prefer this structure:

```text
.logic-editor.json
```json
{ ... }
```

oe-swift.json
```json
{ ... }
```

Notes
- ...
```

If the project is not iOS, omit `oe-swift.json`.

If there is already a config file, show the updated file content instead of a from-scratch template.
