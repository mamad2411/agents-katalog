# Knicks-Knacks Development Guide

## Project Overview

Knicks-Knacks is a monorepo containing multiple web and mobile applications built with modern technologies. The repository uses **Turborepo** for build orchestration and **Yarn Berry (v4.9.1)** for package management.

## Repository Structure

```
knicks-knacks/
├── apps/                    # Full-stack applications
│   ├── bot-battle/         # LLM benchmarking web app
│   ├── calorie-cam/        # Food tracking (mobile + backend)
│   ├── leaf/               # Book tracking (mobile + backend)
│   └── regexplain/         # Regex explanation web app
├── games/                   # Web-based games (GitHub Pages)
│   ├── wordle/             # Word guessing game
│   ├── 2048/               # Number sliding puzzle
│   └── asteroids/          # Space shooter game
├── packages/               # Shared packages
│   ├── eslint-config/      # ESLint configurations
│   ├── shared/             # Shared utilities & types
│   └── ui/                 # Shared UI components
├── package.json            # Root workspace config
├── turbo.json              # Turborepo configuration
└── tsconfig.base.json      # Base TypeScript config
```

## Tech Stack

| Category | Technology |
|----------|------------|
| Monorepo | Turborepo 1.10.16 |
| Package Manager | Yarn Berry 4.9.1 |
| Language | TypeScript 5.x |
| Web Framework | Next.js 15 |
| Mobile Framework | React Native + Expo 53 |
| Styling | Tailwind CSS |
| Backend | Express.js |
| Database | Supabase (PostgreSQL) |

## Existing Apps

### BotBattle (`apps/bot-battle/web`)
- **Purpose**: LLM API benchmarking and comparison
- **Tech**: Next.js 15, React 18, Zustand, TanStack Query
- **URL**: https://www.botbattle.cc/
- **Deployment**: Vercel

### CalorieCam (`apps/calorie-cam/`)
- **Purpose**: AI-powered food photo analysis for calorie tracking
- **Tech**: React Native (Expo), Express.js, OpenAI GPT-4o, Supabase
- **Deployment**: Railway (backend), Expo EAS (mobile)

### Leaf (`apps/leaf/`)
- **Purpose**: Book tracking and discovery app
- **Tech**: React Native (Expo), Express.js, Open Library API, Supabase
- **Deployment**: Railway (backend), Expo EAS (mobile)

### RegExplain (`apps/regexplain/web`)
- **Purpose**: AI-powered regex explanation tool
- **Tech**: Next.js 15, React 19
- **URL**: https://www.regexplain.cc/
- **Deployment**: Vercel

## Games (`games/`)

Web-based games deployed to GitHub Pages at https://colorpulse6.github.io/knicks-knacks/

| Game | Description |
|------|-------------|
| Wordle | Daily word guessing game |
| 2048 | Number sliding puzzle |
| Asteroids | Space shooter with collision detection |
| Brickles | Neon brick-breaker with power-ups and combos |
| Chimera | FF6-style JRPG with ATB combat (in development) |

Games use Next.js with static export (`output: 'export'`) for GitHub Pages compatibility.

**Note:** Sector Zero (vertical space shooter) has been moved to a separate repository: https://github.com/colorpulse6/sector-zero

### Chimera (RPG)
An ambitious FF6-style JRPG with:
- ATB (Active Time Battle) combat system
- Tile-based world exploration
- Story about a reality controlled by AI (medieval facade, sci-fi truth)
- Protagonist Kai searching for his sister Elara
- Party member Lady Lyra Lumina
- Save/load system with multiple slots

See `games/chimera/docs/` for full story documentation.

## Development Workflow

### Prerequisites
- Node.js 18+
- Yarn 4.9.1 (comes with repo via corepack)

### Getting Started

```bash
# Install dependencies
yarn install

# Build shared packages first
yarn prepare

# Run all apps in development
yarn dev
```

### App-Specific Commands

```bash
# Web Apps
yarn regexplain:dev          # Start RegExplain
yarn bot-battle:dev          # Start BotBattle

# Mobile Apps (run in separate terminals)
yarn calorie-cam:backend     # CalorieCam API server
yarn calorie-cam:mobile      # CalorieCam Expo app

yarn leaf:backend            # Leaf API server
yarn leaf:mobile             # Leaf Expo app

# Games
yarn wordle:dev              # Start Wordle game
yarn 2048:dev                # Start 2048 game
yarn asteroids:dev           # Start Asteroids game
yarn brickles:dev            # Start Brickles game
yarn chimera:dev             # Start Chimera RPG
```

### Build Commands

```bash
# Build everything
yarn build

# Build specific app
yarn turbo run build --filter=@knicks-knacks/regexplain

# Build shared packages only
yarn build:packages
```

### Other Commands

```bash
yarn lint                    # Lint all projects
yarn test                    # Run all tests
yarn clean                   # Remove node_modules, dist, .next, .turbo
```

## Adding a New App

### Web App (Next.js)

1. Create directory structure:
   ```
   apps/[app-name]/web/
   ```

2. Initialize with Next.js:
   ```bash
   cd apps/[app-name]/web
   npx create-next-app@latest . --typescript --tailwind --eslint
   ```

3. Update `package.json` name to `@knicks-knacks/[app-name]`

4. Add script to root `package.json`:
   ```json
   "[app-name]:dev": "cd apps/[app-name]/web && yarn dev"
   ```

### Game (Static Export)

1. Create directory structure:
   ```
   games/[game-name]/web/
   ```

2. Configure `next.config.js` for static export:
   ```js
   const nextConfig = {
     output: 'export',
     images: { unoptimized: true },
     trailingSlash: true,
   }
   ```

3. Add script to root `package.json`:
   ```json
   "[game-name]:dev": "cd games/[game-name]/web && yarn dev"
   ```

## Deployment

### Vercel (Web Apps)
- BotBattle and RegExplain auto-deploy from `main` branch
- Configure in Vercel dashboard with root directory set to app path

### Railway (Backends)
- CalorieCam and Leaf backends deploy from `main` branch
- Configuration in `railway.json` and `nixpacks.toml`

### Expo EAS (Mobile Apps)
- Build with `eas build`
- Submit with `eas submit`

### GitHub Pages (Games)
- Automated deployment via GitHub Actions
- Push to `main` triggers build and deploy to `gh-pages` branch
- Games available at: `https://colorpulse6.github.io/knicks-knacks/[game-name]/`

## Coding Standards

### TypeScript
- Strict mode enabled
- No implicit any
- Explicit return types for functions

### React
- Functional components with hooks
- Use `"use client"` directive for client components in Next.js
- Prefer composition over inheritance

### Styling
- Tailwind CSS for all styling
- Use `cn()` utility for conditional classes
- Mobile-first responsive design

### State Management
- Zustand for global state
- TanStack Query for server state
- Local state with useState/useReducer

### File Naming
- Components: PascalCase (`GameBoard.tsx`)
- Utilities: camelCase (`useLocalStorage.ts`)
- Constants: SCREAMING_SNAKE_CASE

## Environment Variables

Each app has its own `.env.example` file. Copy to `.env.local` for development:

```bash
cp apps/[app-name]/.env.example apps/[app-name]/.env.local
```

Common variables:
- `SUPABASE_URL` / `SUPABASE_ANON_KEY` - Database access
- `OPENAI_API_KEY` - AI features
- `NODE_ENV` - Environment mode

## Troubleshooting

### Yarn/Dependency Issues
```bash
yarn clean
rm -rf .yarn/cache
yarn install
```

### Turborepo Cache Issues
```bash
yarn turbo run build --force
```

### Expo/Metro Issues
```bash
cd apps/[app]/mobile
npx expo start --clear
```
