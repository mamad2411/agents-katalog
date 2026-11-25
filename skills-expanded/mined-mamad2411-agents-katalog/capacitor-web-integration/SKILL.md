---
name: capacitor-web-integration
description: Use when integrating CapacitorJS into a web framework (React, Vue, Angular, SvelteKit) including platform detection, build pipeline alignment, PWA hybrid patterns, and live-reload configuration.
---

# Capacitor Web Integration

## Specialization

Integrate CapacitorJS cleanly into a web framework project with deterministic build pipeline alignment, platform-conditional code patterns, PWA hybrid awareness, and safe live-reload configuration.

## Scope Boundaries

In scope:

- Framework-specific integration for React, Vue, Angular, and SvelteKit.
- Platform detection using `Capacitor.isNativePlatform()` and `Capacitor.getPlatform()`.
- Build pipeline output alignment (`webDir`, Vite/Webpack config, output adapter).
- PWA + Capacitor hybrid coexistence rules.
- Live-reload development server configuration and security limits.
- Tree-shaking and bundle size impact of Capacitor imports.

Out of scope:

- Initial Capacitor project creation (see `capacitor-setup`).
- Native plugin authoring (see `capacitor-plugin-authoring`).
- Native API usage patterns (see `capacitor-native-apis`).
- Release signing and store submission (see `capacitor-release-readiness`).

## Trigger Conditions

- A web framework project is being configured for Capacitor for the first time.
- Platform-specific behavior differs from expectations in native builds.
- A PWA is being extended to also run as a native Capacitor app.
- Live-reload is needed during development without exposing the dev server to production.
- Build output mismatches are causing `cap sync` to miss assets or produce stale builds.

## Inputs

- Web framework and version (React, Vue, Angular, SvelteKit).
- Build tool and output directory configuration.
- Target platforms: iOS, Android, or both.
- PWA service worker presence and caching strategy.
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

- Framework-specific integration guidance with concrete configuration snippets.
- Platform detection pattern for conditional native and web behavior.
- Build pipeline alignment verification steps.
- PWA + Capacitor coexistence rules when a service worker is present.
- Live-reload configuration with explicit security constraints.
- Residual risks and known framework-specific quirks.

## Framework-Specific Patterns

### React (Vite)
```typescript
// vite.config.ts — align build.outDir with capacitor.config.ts webDir
export default defineConfig({
  build: { outDir: 'dist' }
});
// capacitor.config.ts
const config: CapacitorConfig = { webDir: 'dist' };
```

### SvelteKit
```typescript
// svelte.config.js — use static adapter for Capacitor builds
import adapter from '@sveltejs/adapter-static';
export default { kit: { adapter: adapter({ fallback: 'index.html' }) } };
// capacitor.config.ts
const config: CapacitorConfig = { webDir: 'build' };
```

### Angular
```typescript
// angular.json — set outputPath to match webDir
"outputPath": "www"
// capacitor.config.ts
const config: CapacitorConfig = { webDir: 'www' };
```

### Vue (Vite)
```typescript
// vite.config.ts
export default defineConfig({ build: { outDir: 'dist' } });
// capacitor.config.ts
const config: CapacitorConfig = { webDir: 'dist' };
```

## Platform Detection Rules

```typescript
import { Capacitor } from '@capacitor/core';

// Prefer isNativePlatform() for native vs. web branching
if (Capacitor.isNativePlatform()) {
  // Use native APIs
} else {
  // Use web APIs or graceful degradation
}

// Use getPlatform() only when iOS and Android require distinct behavior
const platform = Capacitor.getPlatform(); // 'ios' | 'android' | 'web'
```

- Never use `navigator.userAgent` sniffing to detect Capacitor context.
- Never use platform-specific code at module scope; isolate it behind a detection guard.
- Web fallback paths must be functional; do not assume native context is always available.

## PWA Coexistence Rules

- Disable service worker caching for routes that depend on Capacitor native plugins.
- Do not register a service worker inside a Capacitor native build; use `Capacitor.isNativePlatform()` to gate registration.
- Ensure the service worker's `scope` does not intercept Capacitor's bridge communication.
- Pre-caching static assets is safe; intercepting all network requests breaks native plugin calls.

## Live-Reload Configuration

```typescript
// capacitor.config.ts — development only, never commit
const config: CapacitorConfig = {
  server: {
    url: 'http://192.168.1.x:5173', // local network IP of dev machine
    cleartext: true                  // required for Android HTTP
  }
};
```

- The `server.url` override must never be present in committed production configuration.
- Use environment-based config loading (`process.env.NODE_ENV`) to prevent accidental production commits.
- `cleartext: true` is required for Android HTTP but only valid in development.

## Build Pipeline Checklist

- Framework build output directory matches `webDir` in `capacitor.config.ts`.
- `npm run build` (or equivalent) executes before every `cap sync`.
- SvelteKit uses the static adapter; a server-side adapter will not work with Capacitor.
- Angular projects use the `browser` output target, not `server`.
- No dynamic route-based rendering that requires a Node.js server; Capacitor serves static files only.

## Quality Gates

- `cap sync` completes cleanly after a fresh framework build.
- Platform detection uses only `Capacitor.isNativePlatform()` or `Capacitor.getPlatform()`.
- No `server.url` override is present in committed configuration.
- PWA service worker registration is gated behind `!Capacitor.isNativePlatform()`.
- Web fallbacks exist for all native API call sites.

## Done Criteria

- Framework builds and syncs to native projects without errors.
- Platform detection pattern is applied consistently across the codebase.
- PWA and Capacitor coexistence rules are documented and enforced.
- Live-reload works in development and does not affect production builds.
- Residual integration risks are explicit and owner-assigned.
