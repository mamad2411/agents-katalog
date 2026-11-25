# Repository Guidelines

## Project Structure & Module Organization

This is a Vite + React + TypeScript app for the Seller Recovery Radar workflow. Application entry points are `src/main.tsx`, `src/App.tsx`, and `src/app/`. Reusable UI lives in `src/components/ui/`, charts in `src/components/charts/`, feature screens in `src/features/`, business rules in `src/domain/`, mock data in `src/mocks/`, and persistence/API facades in `src/services/`. Global CSS and design tokens are under `src/styles/`; static public assets are in `public/`. OpenSpec planning artifacts live in `openspec/`. Treat `dist/` and `node_modules/` as generated output.

## Build, Test, and Development Commands

- `npm install`: install dependencies from `package-lock.json`.
- `npm run dev`: start the Vite development server.
- `npm run build`: run TypeScript project builds, then produce the Vite production bundle.
- `npm run preview`: serve the built bundle locally.
- `npm run lint`: run ESLint over the repository.
- `npm run test`: run the Vitest suite once.
- `npm run test:watch`: run Vitest in watch mode.
- `npm run test:coverage`: generate V8 coverage output.

## Coding Style & Naming Conventions

Use TypeScript and React function components. Match the existing style: two-space indentation, double quotes, semicolons, `camelCase` functions and variables, `PascalCase` React components and types. Prefer `type` imports for type-only dependencies. Keep domain calculations in `src/domain/` pure and UI-free; keep form/dashboard behavior inside `src/features/`. Use `lucide-react` icons where existing UI controls need icons.

## Testing Guidelines

Tests use Vitest with `jsdom`, Testing Library, and setup from `src/test/setup.ts`. Co-locate tests near the code they cover using `*.test.ts` or `*.test.tsx`, as in `src/domain/calculations/calculations.test.ts` and `src/features/dashboard/OverviewDashboard.test.tsx`. Add focused tests for domain rules, formatters, services, and user-visible component behavior. No coverage threshold is configured, but run `npm run test` before handing off changes and use `npm run test:coverage` for larger logic changes.

## Commit & Pull Request Guidelines

This checkout does not include Git metadata, so no project-specific commit history convention is available. Use short, imperative commit subjects such as `Add recovery plan tests` or `Fix product upload parsing`. Pull requests should include a concise summary, linked issue or OpenSpec change when relevant, validation commands run, and screenshots or recordings for visible UI changes.

## Agent-Specific Instructions

Do not edit generated directories (`dist/`, `node_modules/`) unless explicitly requested. Keep changes scoped to the requested behavior, preserve existing folder boundaries, and update tests when touching shared domain logic or user-facing workflows.
