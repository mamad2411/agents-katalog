---
name: follow-tool-react-scan
description: Detect and fix React performance issues with react-scan
argument-hint: "[scope]"
related:
  - check-reference
  - learn
  - run-scan
---

## Goal

Detect performance issues in a React application and optimize with react-scan

## Scope

Use `follow-tool-react-scan` for React projects or workflows

- Use this skill only for React render performance — for general profiling (server, bundle, runtime) use `/run-profiler` or `/run-scan` per context
- If there's no codebase access and you must scan a deployed site → use the CLI URL scan or the browser extension, no package install needed

- Latest: `react-scan@0.5.7` (verified 2026-09-13)

## Execute

### 1. Prepare

> Goal: prepare references and understand react-scan APIs

1. Run `/check-reference` to verify references from sources
2. Run `/learn` (web) to learn react-scan APIs and integration methods
3. Review workflows and patterns per conventions

### 2. Select Integration Method

> Goal: pick how to integrate react-scan into the project

1. CLI auto-setup: `bunx -y react-scan@latest init` detects the framework and installs automatically
2. CLI URL scan: `bunx react-scan@latest <url>` to scan any site without changing code
3. Script tag for quick testing or legacy apps without a build
4. NPM package for production apps needing control and TypeScript
5. Build tool plugin for Vite, Webpack, esbuild, Rollup, Rspack, Rolldown, Astro
6. Browser extension for analyzing apps without changing code

### 3. Install React Scan

> Goal: install react-scan per the chosen method

1. Script tag: add the script in `index.html` before React
   ```html
   <script src="https://unpkg.com/react-scan/dist/auto.global.js"></script>
   ```

2. NPM: run `bun add react-scan` then import before React
   ```typescript
   import { scan } from 'react-scan';
   import React from 'react';
   scan({ enabled: true });
   ```

3. Vite plugin: use the plugin in `vite.config.ts`
   ```typescript
   import reactScan from 'react-scan/react-component-name/vite';
   export default defineConfig({
     plugins: [reactScan()]
   });
   ```

4. Browser extension: install on Chrome/Firefox/Brave then activate on the target site

### 4. Configure Options

> Goal: set options for scanning behavior

1. Set `enabled` per environment (`process.env.NODE_ENV === 'development'`)
2. Turn on `trackUnnecessaryRenders` to find renders that don't change the DOM
3. Adjust `showToolbar`, `showFPS`, `animationSpeed` for convenience
4. Use callbacks (`onRender`, `onCommitStart`, `onCommitFinish`) for extra logic
5. Use `setOptions()` to change the config at runtime

### 5. Initialize Scanning

> Goal: start scanning for client-side and SSR apps

1. Import `scan` or `useScan` before React and React DOM
2. Call `scan(options)` for client-side apps
3. Use the `useScan` hook in `useEffect` for SSR apps after hydration
4. Verify the toolbar shows scanning has started

### 6. Interpret Visual Cues

> Goal: read react-scan's visual cues

1. A component with an outline = a render happened
2. Outline color and thickness = severity of the problem
3. The render count number = how many times it rendered
4. Unnecessary renders are highlighted when `trackUnnecessaryRenders` is on

### 7. Analyze Performance Data

> Goal: analyze performance data from reports and callbacks

1. Watch the FPS meter (`showFPS: true`) to check overall performance
2. Watch the notification count (`showNotificationCount: true`) for slowdown alerts
3. Call `getReport()` for a detailed render report
4. Use the `onRender` callback to collect metrics or log yourself

### 8. Optimize Components

> Goal: fix components that re-render too much or unnecessarily

1. Find components that re-render often or unnecessarily
2. Use `React.memo` for components whose props rarely change
3. Use `useMemo`/`useCallback` for expensive computations and callbacks
4. Split context to reduce app-wide re-renders
5. Measure before and after optimizing to confirm unnecessary renders dropped

### 9. Disable in Production

> Goal: turn off react-scan in production builds

1. Set `enabled: false` in production builds
2. Avoid `dangerouslyForceRunInProduction` except emergency debugging
3. Use build tool plugins to strip the code out of production
4. Check bundle size hasn't grown from react-scan code

## Rules

### 1. Integration Standards

- Always import `react-scan` before React and React DOM
- Enable only in development by default
- Use `useScan` in `useEffect` for SSR applications

### 2. Performance Guidelines

- `trackUnnecessaryRenders` and `log` add overhead — use with caution
- Use build tool plugins to preserve component names for production analysis
- Find and prioritize the components highlighted most often first
- Don't optimize every component without measuring real impact
- Verify you're not optimizing renders that don't affect UX
- Remove `react-scan` before deploying to production

- Use /check-reference if needed
- Use /learn if needed
- Use /run-scan if needed

## References

- [CLI reference](references/cli.md)

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- The React app surfaces performance issues clearly
- Unnecessary renders are highlighted with easy-to-understand visual cues
- Performance data is collected and analyzed to fix the right points
- Problem components are optimized appropriately
- Production builds contain no react-scan code or overhead
- The developer sees app performance immediately

