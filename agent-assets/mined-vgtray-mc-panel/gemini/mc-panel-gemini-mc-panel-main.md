# MCPanel - Project Context

## 1. Project Overview

**MCPanel** is a self-hosted Minecraft server management panel designed to combine the simplicity of Aternos with the power of Pterodactyl. It features a modern UI, integrated marketplace for one-click modpack/plugin installations, and robust server management via Docker.

**Key Features:**
*   **Server Management:** Create, start, stop, restart, and monitor Minecraft servers.
*   **Docker Isolation:** Each server runs in its own Docker container.
*   **Marketplace:** Integrated browser for CurseForge, Modrinth, Spigot, and Hangar.
*   **File Manager:** Web-based Monaco editor, upload/download capabilities.
*   **Multi-User:** Role-based access control (Admin/User).
*   **Backups:** Automatic and manual backups.

## 2. Tech Stack

### Frontend (`/frontend`)
*   **Framework:** Next.js 14 (App Router)
*   **Language:** TypeScript
*   **Styling:** TailwindCSS, shadcn/ui
*   **State Management:** Zustand, React Query
*   **Real-time:** Socket.io Client

### Backend (`/backend`)
*   **Runtime:** Node.js 20
*   **Framework:** Fastify
*   **Language:** TypeScript
*   **Database:** PostgreSQL 16 (via Prisma ORM)
*   **Cache/Queue:** Redis 7 (BullMQ for background jobs)
*   **Docker Interface:** Dockerode
*   **Real-time:** Socket.io Server

### Infrastructure
*   **Containerization:** Docker & Docker Compose
*   **Reverse Proxy:** Traefik (recommended in production)
*   **Deployment:** Optimized for Dokploy, but works with standard Docker.

## 3. Architecture

The application is composed of three main services defined in `docker-compose.yml`:
1.  **Frontend:** Next.js application serving the UI.
2.  **Backend:** Fastify API server managing logic, DB connections, and Docker socket.
3.  **Database & Cache:** PostgreSQL for persistent data and Redis for job queues/caching.

Minecraft servers are spawned as *sibling containers* on the host Docker daemon, managed by the Backend service.

## 4. Getting Started

### Prerequisites
*   Node.js 20+
*   Docker & Docker Compose
*   PostgreSQL & Redis (or use the provided `docker-compose.yml`)

### Setup Instructions

1.  **Environment Variables:**
    *   Copy `.env.example` to `.env` in the root (if applicable) or configure `backend/.env` and `frontend/.env.local` based on the example.
    *   Critical variables: `DATABASE_URL`, `REDIS_URL`, `JWT_SECRET`.

2.  **Install Dependencies:**
    ```bash
    # Backend
    cd backend
    npm install

    # Frontend
    cd ../frontend
    npm install
    ```

3.  **Database Setup:**
    Ensure your database is running (e.g., via `docker-compose up -d mcpanel-db mcpanel-redis`).
    ```bash
    cd backend
    npm run db:generate  # Generate Prisma client
    npm run db:push      # Push schema to DB
    ```

4.  **Running in Development:**
    *   **Backend:** `cd backend && npm run dev` (Runs on port 4000)
    *   **Frontend:** `cd frontend && npm run dev` (Runs on port 3000)

## 5. Key Commands

| Scope | Command | Description |
| :--- | :--- | :--- |
| **Backend** | `npm run dev` | Start backend in watch mode |
| **Backend** | `npm run build` | Compile TypeScript to `dist/` |
| **Backend** | `npm run db:generate` | Update Prisma client type definitions |
| **Backend** | `npm run db:push` | Push schema changes to the database |
| **Frontend** | `npm run dev` | Start frontend development server |
| **Frontend** | `npm run build` | Build frontend for production |
| **Frontend** | `npm run lint` | Run ESLint |

## 6. Project Structure

*   `backend/src/jobs`: Background workers for heavy tasks (backups, downloads).
*   `backend/src/services`: Core logic (Docker management, File operations).
*   `backend/src/routes`: API endpoints definitions.
*   `backend/prisma/schema.prisma`: Database schema definition.
*   `frontend/src/app`: Next.js App Router pages.
*   `frontend/src/components`: UI components (shared and feature-specific).
*   `frontend/src/lib`: Utility functions and API clients.

## 7. Development Conventions

*   **Type Safety:** Strict TypeScript usage across full stack. Shared types should be maintained where possible.
*   **API Design:** RESTful endpoints for CRUD, WebSockets for real-time status/logs.
*   **UI/UX:** Use `shadcn/ui` components for consistency.
*   **Database:** Always use Prisma migrations/push for DB changes.
