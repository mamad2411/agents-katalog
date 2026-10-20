# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MCPanel is a self-hosted Minecraft server management panel that combines the simplicity of Aternos with the power of Pterodactyl. It features a marketplace integration (CurseForge, Modrinth) for one-click modpack, mod, and plugin installation.

**Architecture**: Monorepo with Next.js frontend and Fastify backend, orchestrated via Docker Compose with PostgreSQL and Redis.

## Tech Stack

### Backend
- **Runtime**: Node.js 20+ (ESM modules)
- **Framework**: Fastify 4.x with TypeScript 5.x
- **Database**: Prisma ORM with PostgreSQL 16
- **Queue**: BullMQ with Redis
- **WebSocket**: Socket.io for real-time console and stats
- **Docker**: dockerode for managing Minecraft server containers
- **Authentication**: JWT with @fastify/jwt, bcrypt password hashing, optional 2FA (OTP)

### Frontend
- **Framework**: Next.js 16.x with App Router (React 18)
- **Styling**: TailwindCSS with shadcn/ui components
- **State**: Zustand for global state, @tanstack/react-query for server state
- **WebSocket**: Socket.io client for real-time updates
- **Forms**: react-hook-form with Zod validation
- **Editor**: Monaco Editor for file editing

### Infrastructure
- **Containerization**: Docker with itzg/minecraft-server image for MC servers
- **Reverse Proxy**: Traefik via Dokploy
- **DNS**: Cloudflare (panel/api proxied, mc subdomain DNS-only for TCP)

## Common Commands

### Development

```bash
# Backend
cd backend
npm run dev              # Start backend dev server with tsx watch
npm run db:generate      # Generate Prisma client
npm run db:push          # Push schema changes to database
npm run db:migrate       # Create and run migrations

# Frontend
cd frontend
npm run dev              # Start Next.js dev server
npm run build            # Build production bundle
npm run lint             # Run ESLint

# Root (Docker)
docker compose up -d     # Start all services
docker compose logs -f   # Follow logs
docker compose down      # Stop all services
```

### Building

```bash
# Backend
cd backend
npm run build            # TypeScript compilation to dist/

# Frontend
cd frontend
npm run build            # Next.js production build
```

### Database

```bash
cd backend
npx prisma studio        # Open Prisma Studio (GUI)
npx prisma db push       # Quick schema sync (dev)
npx prisma migrate dev   # Create migration (production-ready)
npx prisma generate      # Regenerate Prisma Client
```

## Architecture Overview

### Backend Structure

```
backend/src/
├── index.ts                 # Fastify app bootstrap + plugin registration
├── config/env.ts            # Environment variable validation
├── lib/
│   ├── prisma.ts            # Prisma client singleton
│   ├── redis.ts             # Redis client
│   ├── socket.ts            # Socket.io server initialization
│   └── password.ts          # bcrypt utilities
├── routes/                  # Fastify route handlers
│   ├── auth.routes.ts       # Login, register, 2FA, email verification
│   ├── server.routes.ts     # Server CRUD, start/stop/restart
│   ├── files.routes.ts      # File manager API
│   ├── marketplace.routes.ts # CurseForge/Modrinth/Hangar search
│   ├── backup.routes.ts     # Backup management
│   ├── jobs.routes.ts       # Job status queries
│   ├── user.routes.ts       # User profile/settings
│   └── admin.routes.ts      # Admin panel endpoints
├── services/
│   ├── docker.service.ts    # Docker container lifecycle
│   ├── curseforge.service.ts # CurseForge API client
│   ├── modrinth.service.ts  # Modrinth API client
│   ├── plugins.service.ts   # Spigot/Hangar API clients
│   ├── marketplace.service.ts # Unified marketplace abstraction
│   ├── filemanager.service.ts # File operations on server volumes
│   ├── backup.service.ts    # Backup creation/restoration
│   ├── email.service.ts     # Resend email sending
│   └── two-factor.service.ts # OTP generation/verification
├── jobs/
│   ├── queue.ts             # BullMQ queue initialization
│   ├── worker.ts            # BullMQ worker startup
│   └── handlers/            # Job processors
│       ├── install-modpack.ts
│       ├── install-mod.ts
│       ├── install-plugin.ts
│       ├── backup.ts
│       └── download.service.ts
├── middleware/
│   └── auth.middleware.ts   # JWT verification decorator
└── schemas/
    ├── auth.schema.ts       # Zod schemas for auth
    └── server.schema.ts     # Zod schemas for servers
```

**Key patterns**:
- Backend uses **ESM modules** (`type: "module"` in package.json) - all imports require `.js` extension
- Routes are registered in `index.ts` via `app.register(authRoutes, { prefix: '/auth' })`
- Authentication uses `@fastify/jwt` with `@Authenticate()` decorator (see `auth.middleware.ts`)
- All async jobs (modpack install, backups) go through BullMQ and emit progress via Socket.io

### Frontend Structure

```
frontend/src/
├── app/
│   ├── layout.tsx           # Root layout with Providers
│   ├── page.tsx             # Landing page (redirects to /dashboard)
│   ├── login/page.tsx
│   ├── register/page.tsx
│   ├── verify-email/page.tsx
│   ├── forgot-password/page.tsx
│   ├── reset-password/page.tsx
│   └── dashboard/
│       ├── layout.tsx       # Dashboard shell with sidebar
│       ├── page.tsx         # Dashboard home
│       ├── servers/
│       │   ├── page.tsx     # Server list
│       │   ├── new/page.tsx # Create server wizard
│       │   └── [id]/page.tsx # Server detail (tabs: console, files, mods, plugins, backups, settings)
│       ├── marketplace/page.tsx
│       ├── settings/page.tsx
│       └── admin/page.tsx   # Admin only
├── components/
│   ├── ui/                  # shadcn/ui components
│   ├── install-button.tsx   # Marketplace install with job progress
│   ├── job-progress.tsx     # Real-time job progress bar
│   ├── file-editor.tsx      # Monaco editor wrapper
│   └── providers.tsx        # React Query + Zustand providers
├── stores/
│   └── auth.store.ts        # Zustand auth state
└── lib/
    └── utils.ts             # cn() utility for Tailwind
```

**Key patterns**:
- Uses Next.js **App Router** with Server Components (default) and Client Components (marked with `'use client'`)
- API calls via `fetch()` wrapped in React Query hooks
- Socket.io connections managed in `useEffect` hooks on dashboard pages
- Authentication token stored in httpOnly cookie (set by backend)

### Docker Orchestration

**Minecraft Server Lifecycle**:
1. User creates server via `/servers` POST → Backend allocates unique port (25565-25600 range)
2. Backend calls `docker.service.ts` → Creates container with `itzg/minecraft-server` image
3. Container mounts volume at `/data/servers/{serverId}`
4. RCON enabled on `port + 10000` for sending commands (e.g., port 25565 → RCON 35565)
5. Console logs streamed via `docker.attach()` → broadcasted to frontend via Socket.io

**Container environment variables** (see `docker.service.ts`):
- `EULA=TRUE`
- `TYPE={ServerType}` (VANILLA, PAPER, FORGE, FABRIC, etc.)
- `VERSION={minecraftVersion}`
- `MEMORY={ramMax}M`
- `ENABLE_RCON=true`
- `RCON_PASSWORD={generated}`

### Marketplace Integration

**Modpack Installation Flow** (via BullMQ):
1. User selects modpack → Frontend calls `POST /marketplace/modpacks/{id}/install`
2. Backend creates Job record in DB and queues BullMQ job
3. Worker (`jobs/handlers/install-modpack.ts`) executes:
   - Downloads modpack manifest from CurseForge/Modrinth
   - Downloads all mods in parallel (cached in `/data/cache/{source}/{projectId}/`)
   - Extracts overrides (configs, scripts, etc.) to server directory
   - Updates server type/version in DB
   - Recreates Docker container with new settings
   - Creates `InstalledMod` records with `source`, `externalId`, `projectId`, `versionId`
4. Progress emitted via `socket.emit('job:progress', { jobId, progress, message })`
5. Frontend displays real-time progress bar

**API Clients**:
- **CurseForge**: Requires API key (env: `CURSEFORGE_API_KEY`)
- **Modrinth**: No auth required
- **Hangar** (PaperMC): No auth required
- **Spiget** (SpigotMC): No auth required

### Database Schema Notes

**Important relationships**:
- `Server.userId` → Owner relationship (cascade delete)
- `InstalledMod.serverId` → Server relationship (cascade delete)
- `InstalledMod.catalogueItemId` → Optional link to `MarketplaceCatalogueItem` (for tracking global marketplace items)
- `Job.serverId` → Optional (backups reference servers, generic jobs may not)
- `Job.userId` → Required (for permission checks)

**Enums**:
- `ServerType`: VANILLA, PAPER, SPIGOT, FORGE, FABRIC, QUILT, PURPUR
- `ServerStatus`: STOPPED, STARTING, RUNNING, STOPPING, ERROR, INSTALLING
- `JobStatus`: PENDING, RUNNING, COMPLETED, FAILED, CANCELLED

### WebSocket Events

**Server → Client**:
```typescript
socket.on('console:log', { serverId, line, timestamp })      // New console line
socket.on('console:history', { serverId, lines })            // Initial history
socket.on('server:status', { serverId, status })             // Status change
socket.on('server:stats', { serverId, cpu, ram, players })   // Live stats
socket.on('job:progress', { jobId, progress, message })      // Job progress (0-100)
socket.on('job:complete', { jobId, result })                 // Job finished
socket.on('job:error', { jobId, error })                     // Job failed
```

**Client → Server**:
```typescript
socket.emit('console:join', { serverId })                    // Subscribe to server console
socket.emit('console:leave', { serverId })                   // Unsubscribe
socket.emit('console:command', { serverId, command })        // Send command to server
```

## Key Implementation Details

### Port Allocation
Ports are allocated sequentially from `MC_PORT_RANGE_START` (25565) to `MC_PORT_RANGE_END` (25600). The backend finds the first available port not in use by querying existing servers in the database.

### RCON for Server Commands
The backend uses RCON (Minecraft's remote console protocol) to send commands to running servers. RCON port is always `game_port + 10000`. The RCON password is auto-generated during container creation and stored in `Server.rconPassword`.

### File Operations
All file operations go through `filemanager.service.ts` which operates on volumes mounted at `/data/servers/{serverId}`. Files are edited via Monaco Editor in the frontend and saved via `PUT /servers/{id}/files/content`.

### Backup System
Backups are tar.gz archives created via `backup.service.ts`. The service stops the server, creates a tarball of the entire server directory, and stores it in `/data/backups/{serverId}/`. Backups can be scheduled via `backup-scheduler.service.ts` (runs on cron).

### Authentication Flow
1. User registers → Email verification token sent via Resend
2. User verifies email → Account activated
3. User logs in → JWT issued (httpOnly cookie + response body)
4. Optional: User enables 2FA → QR code generated, backup codes provided
5. All protected routes verify JWT via `@Authenticate()` decorator

### Environment Variables
Copy `.env.example` to `.env` and configure:
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `JWT_SECRET`: Random string for JWT signing
- `CURSEFORGE_API_KEY`: CurseForge API key (get from console.curseforge.com)
- `RESEND_API_KEY`: Resend API key for emails
- `EMAIL_FROM`: Sender email address
- `PANEL_URL`: Frontend URL (for CORS and email links)
- `DOMAIN`: Base domain for Traefik routing

## Development Workflow

1. **Database changes**: Modify `backend/prisma/schema.prisma` → run `npm run db:push` (dev) or `npm run db:migrate` (prod)
2. **New API endpoint**: Add route in `backend/src/routes/*.routes.ts` → register in `backend/src/index.ts`
3. **New job type**: Add handler in `backend/src/jobs/handlers/` → register in `worker.ts` → add `JobType` enum to Prisma schema
4. **Frontend state**: Use React Query for server state, Zustand for client state (auth, UI preferences)
5. **WebSocket events**: Add event handlers in `backend/src/lib/socket.ts` and corresponding listeners in frontend pages

## Deployment

The project is designed for deployment on **Dokploy** (Docker-based PaaS):
1. Connect Git repository
2. Set environment variables in Dokploy UI
3. Dokploy builds frontend/backend images and deploys via Docker Compose
4. Traefik handles SSL termination and routing (panel.domain.com → frontend, api.domain.com → backend)

**Important**: The backend container runs as root (`user: "0:0"`) to access the Docker socket at `/var/run/docker.sock`. This is required for creating/managing Minecraft server containers.
