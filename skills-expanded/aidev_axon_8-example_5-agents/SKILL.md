# Project Structure

- Frontend: `frontend/`
- Backend: `backend/`

## Code Standards

All contributors and agents must follow the project code standards in `.codex/rules/code-standards.md` when writing or updating code.

## Test Standards

All contributors and agents must follow the test standards in `.codex/rules/test.md` when writing or updating automated tests.

## React Standards

All contributors and agents must follow the React standards in `.codex/rules/react.md` when writing or updating frontend React code.

## Design System

All contributors and agents must read `DESIGN.md` and follow its design direction when creating or updating UI, styling, frontend layouts, components, and visual assets.

## API Design

All contributors and agents must follow the HTTP API standards in `.codex/rules/http.md` when defining or updating backend API endpoints.

## Folder Structure

All contributors and agents must follow the project folder structure rules in `.codex/rules/folder-structure.md` when creating or moving files.

## Frontend

The frontend is a Vite React application.

```bash
cd frontend
npm install
npm run dev
```

- Development server: `http://localhost:5173`
- Preview server: `http://localhost:4173` after running:

```bash
npm run build
npm run preview
```

## Backend

The backend is an Express API.

```bash
cd backend
npm install
npm run dev
```

- Development/API server: `http://localhost:3000`
- The backend reads `PORT` from the environment and falls back to `3000`.
- Health check endpoint: `http://localhost:3000/health`

For a production-style build and start:

```bash
npm run build
npm start
```
