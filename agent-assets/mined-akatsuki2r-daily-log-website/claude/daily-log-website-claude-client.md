# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a React + TypeScript + Vite frontend application that serves as a client for a daily log/tracking system. It communicates with a Python FastAPI backend running at `http://127.0.0.1:8000`.

## Common Commands

```bash
npm run dev       # Start development server
npm run build     # Build for production (TypeScript check + Vite build)
npm run lint      # Run ESLint
npm run preview   # Preview production build
```

## Architecture

- **Routing**: React Router v6 with `createBrowserRouter` in `src/main.tsx`
- **API Client**: Axios instance in `src/API.ts` with automatic Bearer token injection from localStorage
- **Styling**: Tailwind CSS v4 (configured via `@tailwindcss/vite` plugin in `vite.config.ts`)
- **State**: React hooks (useState) for local component state

### Key Routes

| Path | Component |
|------|-----------|
| `/` | App (WelcomePage) |
| `/SignUpPage` | RegisterPage |
| `/Login` | LoginBox |
| `/Home` | Home (authenticated) |
| `/Nodes` | (placeholder) |
| `/Sessions` | (placeholder) |
| `/Decision_Log` | (placeholder) |
| `/Dashboard` | (placeholder) |

### Auth Flow

- Signup: POST to `/v1/authentication/SignUp` with `{username, email, password}`
- Login: POST to `/v1/authentication/Login` with `{username, password}`
- Token stored in `localStorage` under `access_token`
- API interceptor in `src/API.ts` automatically attaches `Authorization: Bearer <token>` to requests

### Component Structure

- `src/Pages/` - Page-level components
- `src/components/` - Reusable UI components (Navbar variants, Sections, RegistrationBoxes)
- `src/api/` - API call utilities (currently empty, add endpoint functions here)
- `src/API.ts` - Axios configuration with interceptors