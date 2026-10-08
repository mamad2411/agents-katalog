# MicroFarm Development Instructions

## 🏗️ Architecture
- **Monorepo**: `packages/shared` (types/utils), `packages/backend` (API), `packages/frontend` (UI)
- **Dependencies**: Frontend/Backend depend on `@microfarm/shared`, no circular deps
- **Build Order**: Always build shared package first

## 📝 TypeScript Rules
- **Strict Mode**: Always use strict TypeScript config
- **Types**: Define explicit types, prefer interfaces over types, avoid `any`
- **Naming**: PascalCase for classes/interfaces, camelCase for functions/vars
- **Files**: One class per file, kebab-case filenames

## 🎯 Code Quality
- **Simplicity**: Choose readable over clever, max 20 lines per function
- **Separation**: Keep UI, logic, and data separate
- **Error Handling**: Always use try-catch for async operations
- **Validation**: Validate all inputs and API responses

## 🔧 Development Patterns
- **Imports**: Use named exports, import from specific files
- **State**: Keep game state centralized and immutable
- **API**: RESTful endpoints, consistent error responses
- **Rendering**: Separate rendering from game logic

## 🚀 Performance
- **Frontend**: Use requestAnimationFrame, minimize DOM manipulation
- **Backend**: Validate requests, implement proper logging
- **Memory**: Clean up intervals/timeouts, avoid memory leaks

## 📦 Package Management
- **Dependencies**: Keep minimal, use exact versions
- **Scripts**: Use pnpm workspace filters (`pnpm --filter=@microfarm/backend run dev`)
- **Build**: `pnpm run build:shared` → `pnpm run build:backend` → `pnpm run build:frontend`

## 🎮 Game-Specific
- **State Sync**: Update game state through API calls
- **Tools**: Validate tool usage on tiles before applying
- **Rendering**: Use canvas for game, optimize for 60fps
- **Crops**: Implement real-time growth updates

## 🚨 Avoid
- `any` type, circular dependencies, deep nesting (>3 levels)
- Mixing concerns, ignoring TypeScript errors
- Blocking main thread, memory leaks
- Duplicating code across packages

**Core Principle**: Simplicity, Readability, Maintainability. Choose simpler solutions.
