# Global Agent Rules

1. **Long-running Commands**: When executing commands that typically take a significant amount of time (such as `npm run build`, `npm run lint`, or test suites), you MUST wait for user input or confirmation before proceeding to the next step. Do not auto-run subsequent steps assuming the command has finished immediately.

2. **Update Tests**: If adding or changing any code, you MUST also update the related tests in the `tests` folder to ensure they pass and cover the changes.

3. **Tech Stack Standards**:
   - **Styling**: Use Tailwind CSS. Do not introduce new CSS libraries.
   - **Linting**: Use `npm run lint` (Biome). Do not use ESLint or Prettier unless specifically asked.
   - **Framework**: Follow Next.js App Router conventions. Default to Server Components; use `'use client'` only when needed.
   - **Imports**: Use `@/` alias for imports (e.g., `import { Button } from '@/components/ui/button'`).

4. **Code Quality**:
   - **Types**: Strictly avoid `any` types. Define proper interfaces.
   - **Verification**: Run `npm run lint` (Biome) before marking tasks as complete to ensure no linting errors were introduced.

5. **Project Specifics**:
   - **Real-time**: Be aware that Socket.io logic is in `scripts/start-socket-server.ts`. Changes to real-time features may require updating this script.
   - **Testing**: Use Jest for unit tests (`npm run test:unit`) and Playwright for E2E (`npm run test:e2e`).
