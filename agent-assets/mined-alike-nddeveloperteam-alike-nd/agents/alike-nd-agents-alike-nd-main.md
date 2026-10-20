# Project Directives & Environment Protection Rules

## Critical Rule: Preserve .env and .env.example intact
- **DO NOT TOUCH, MODIFY, OR REMOVE** `MONGO_URI` or `JWT_SECRET` from `.env` or `.env.example`.
- Both `MONGO_URI` and `JWT_SECRET` are required by the backend services (`backend/store.ts`, `backend/routes/auth.ts`, `backend/routes/userAuth.ts`, `backend/routes/sellerPortal.ts`).
- Never generate any diff or change that deletes, clears, comments out, or modifies these lines. Keep the `.env` file and `.env.example` exactly intact with both keys preserved.
