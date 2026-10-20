# Avocado App - Gemini CLI Context

This project is a Next.js + TypeScript demo application for an avocado-themed e-commerce site. It serves as a learning project for building React components, managing state with Context, and utilizing Next.js features like API routes and Static Site Generation (SSG).

## Project Overview

- **Framework:** [Next.js](https://nextjs.org/) (v13.4.19)
- **Language:** [TypeScript](https://www.typescriptlang.org/)
- **UI Framework:** [Semantic UI React](https://react.semantic-ui.com/)
- **State Management:** React Context API with `useReducer` (see `src/store/Cart.tsx`)
- **Data Source:** A local mock database (see `src/database/db.ts`) serving static data from `src/database/data.ts`.
- **Styling:** Semantic UI CSS and global styles in `src/global.css`.

### Architecture

- `src/pages/`: Next.js file-based routing, including API routes (`src/pages/api/avo`).
- `src/components/`: Modular UI components organized by feature (e.g., `CartItemList`, `KawaiiHeader`, `ProductSummary`).
- `src/database/`: Mock database implementation for local data handling.
- `src/store/`: Shopping cart state management using React Context.
- `public/`: Static assets including product images.

## Building and Running

### Prerequisites
- Node.js and npm installed.

### Commands
- **Install dependencies:** `npm install`
- **Start development server:** `npm run dev` (runs at `http://localhost:3000`)
- **Build for production:** `npm run build`
- **Start production server:** `npm run start`
- **Lint the project:** `npm run lint`

## Development Conventions

### Path Aliases
The project uses TypeScript path aliases for cleaner imports (configured in `tsconfig.json`):
- `@database`: Maps to `src/database/db.ts`
- `@components/*`: Maps to `src/components/*`
- `@store/*`: Maps to `src/store/*`

### Coding Style
- **Functional Components:** Prefer functional components with Hooks.
- **TypeScript:** Use strict typing where possible. Custom types are defined in `src/index.d.ts` and component-specific files.
- **State Management:** Use the `useCart` and `useCartMutations` hooks from `@store/Cart` for interacting with the shopping cart.
- **API Calls:** API routes are used to expose data from the local mock DB. The frontend fetches data from these routes (e.g., `/api/avo`).

### Component Structure
Components are typically structured as:
```tsx
import React from 'react'
// Imports...

const MyComponent = () => {
  return (
    // JSX using Semantic UI...
  )
}

export default MyComponent
```
