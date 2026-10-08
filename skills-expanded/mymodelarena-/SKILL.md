# MyModelArena .cursorrules

## General Project Structure & Language

* **Structure**: The project is organized into two main directories: `client/` for the React frontend and `server/` for the Node.js backend. Adhere strictly to the file structure defined in the Technical Specification and Implementation Plan.
* **Language**: Use **TypeScript** for both the `client` and `server` codebases. Ensure strong typing is used wherever possible, including function parameters, return types, and component props.
* **File Naming**:
    * React Components: `PascalCase.tsx` (e.g., `ModelForm.tsx`)
    * CSS Modules: `kebab-case.module.css` (e.g., `model-form.module.css`)
    * Other TS files (hooks, utils, services, controllers, routes): `camelCase.ts` or `kebab-case.ts` (e.g., `useApiModel.ts`, `llmService.ts`, `models.routes.ts`). Be consistent within client/server conventions.
* **Code Style**: Follow standard TypeScript best practices. Use clear and descriptive variable/function names. Add comments for complex logic sections. Aim for readability and maintainability. Use Prettier for code formatting (if configured). Use ESLint for linting (if configured).
* **Implementation Flow**: Strictly follow the steps outlined in the **Implementation Plan**. Each step should be implemented atomically. Refer back to the **Technical Specification** for detailed requirements when implementing each step.

## Backend (Server - Node.js/Express/Prisma)

* **Framework**: Use Express.js for the server framework.
* **Database**: Use **Prisma** as the ORM with the **SQLite** provider. Define the schema exactly as specified in `server/prisma/schema.prisma`. Use Prisma Client for all database interactions. Use Prisma Migrate for schema changes.
* **API Design**: Implement **RESTful** API endpoints as defined in the routes (`server/src/routes/`). Use standard HTTP methods (GET, POST, PUT, DELETE).
* **Controllers**: Implement business logic within controller functions (`server/src/controllers/`). Keep controllers focused on handling requests/responses and orchestrating calls to services/database.
* **Services**: Use dedicated service modules (`server/src/services/`) for interacting with external APIs (like LLMs via `LlmService`) and complex reusable logic (like `TokenizerService`).
* **Error Handling**: Implement the centralized error handling middleware (`server/src/middleware/errorHandler.ts`). Controller actions should `try...catch` errors (especially from async operations like Prisma or LLM calls) and pass them to `next(error)`. Send standardized JSON error responses (e.g., `{ success: false, error: { message: '...' } }`).
* **Async Operations**: Use `async/await` for all asynchronous operations (Prisma calls, LLM service calls). For parallel calls to multiple LLMs (Eval Execution, Judging), use `Promise.allSettled` to handle individual successes/failures robustly.
* **LLM Interaction**:
    * Implement LLM calls within `LlmService`.
    * Use `node-fetch` or `axios` for HTTPS requests.
    * Construct request bodies according to the OpenAI API protocol specification.
    * Handle authentication using API keys retrieved securely from server environment variables (`process.env`) based on the `apiKeyEnvVar` field stored in the `Model` configuration. **Never hardcode API keys or store them directly in the database.**
    * Implement basic error handling and potentially retry logic for transient network issues.
* **Tokenization & Costing**: Use the `gpt-tokenizer` library within `TokenizerService`. Implement cost calculation logic in `utils/costUtils.ts` based on token counts and model pricing stored in the database.
* **Validation**: Implement input validation within controller functions before processing requests or interacting with the database/services.

## Frontend (Client - React/Vite/TypeScript)

* **Framework**: Use React with functional components and Hooks. The project is set up using Vite.
* **Routing**: Use `react-router-dom` for all client-side routing as defined in `client/src/App.tsx`.
* **State Management**:
    * Use `useState` for local component state (form inputs, modal visibility, etc.).
    * Use **TanStack Query (`@tanstack/react-query`)** for managing server state (fetching, caching, background updates, mutations). Utilize `useQuery` for data fetching and `useMutation` for data modification (create, update, delete). Handle `isLoading`, `isError`, `error`, and `data` states provided by TanStack Query to update the UI appropriately. Invalidate relevant queries after successful mutations.
    * Use **Zustand** for minimal shared global client state if needed (e.g., list of Models for dropdowns, theme preference).
* **Component Architecture**:
    * Organize components into `common/`, `layout/`, and feature-specific directories (`features/`).
    * Define clear `Props` interfaces using TypeScript for all components.
    * Separate concerns where possible (e.g., data fetching logic in custom hooks or page components, passing data down to presentational components).
* **Styling**: Use **CSS Modules** for component-scoped styling. Adhere to the color palette, typography, and spacing defined in the Design System section of the Tech Spec (`client/src/styles/theme.css`).
* **API Interaction**: Use the client-side API wrapper (`client/src/lib/api.ts`) which uses `Workspace` or `axios` to interact with the backend REST API. Functions in `api.ts` should handle basic request setup and response parsing.
* **Error Handling**: Display user-friendly error messages based on the `isError` and `error` states from `useQuery` and `useMutation`. Use the `ErrorMessage` common component.
* **Loading States**: Display loading indicators (e.g., `Spinner` common component) based on the `isLoading` state from `useQuery` and `useMutation`. Disable interactive elements (like submit buttons) during mutations.
* **Async UI**: Ensure the UI remains responsive during background operations (API calls, processing). Provide clear visual feedback for async task progress (e.g., "Running Eval...", "Scoring Responses...").

## Testing

* **Backend Unit Tests**: Use Jest or Vitest. Write tests for utility functions, services (mocking external calls/DB), and controllers (mocking services/DB). Focus on testing business logic and validation. Place tests in `*.test.ts` files alongside the code being tested.
* **Frontend Unit/Integration Tests**: Use Jest or Vitest with React Testing Library. Test component rendering based on props, basic user interactions (`fireEvent`, `userEvent`), and custom hooks. Mock API calls (`msw` or jest mocks). Place tests in `*.test.ts` or `*.test.tsx` files.
* **E2E Tests**: Use Playwright or Cypress. Implement tests covering the key user workflows defined in the Implementation Plan. Tests should interact with the UI via selectors and perform assertions on the application's state.