# CLAUDE.md — Client Workspace

React 19 SPA built with Vite 8 and TypeScript.

## Key Details

- Entry point: `src/main.tsx`
- Main component: `src/App.tsx`
- Build output: `../server/public/` (Vite config)
- TypeScript config: `tsconfig.app.json` (app code), `tsconfig.node.json` (Vite config)
- Module resolution: `bundler` — no file extensions needed in imports
- Strict mode enabled: no unused locals/params, no unchecked side-effect imports

## Dependencies

- React 19, React DOM
- TanStack React Query (data fetching via `/api/*`)
- Firebase (auth)
- react-gtm-module (Google Tag Manager analytics)
- OpenTelemetry SDK for web tracing

## Testing

- Tests live alongside source: `src/**/*.test.{ts,tsx}`
- Environment: `jsdom`
- Libraries: `@testing-library/react`, `@testing-library/user-event`, `@testing-library/jest-dom`
- Run: `npm run test:client` from repo root

## Conventions

- JSX uses `react-jsx` transform (no `import React` needed)
- Use functional components with hooks
- Data fetching via TanStack Query hooks pointed at `/api/*` endpoints
- CSS files co-located with components
