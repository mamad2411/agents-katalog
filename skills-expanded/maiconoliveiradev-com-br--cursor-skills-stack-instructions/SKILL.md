# Stack — Instruções

## Domínios

| App | URL |
|-----|-----|
| Site público | `https://maiconoliveiradev.com.br` |
| API + Admin | `https://admin.maiconoliveiradev.com.br` |

## Arquitetura

```
┌─────────────────────────┐         ┌────────────────────────────────────┐
│  Vercel                 │  HTTP   │  Hostinger Premium                 │
│  maiconoliveiradev.com  │ ──────► │  admin.maiconoliveiradev.com.br    │
│  Next.js 15             │         │  Laravel 12 + MySQL                │
└─────────────────────────┘         └────────────────────────────────────┘
```

## Versões (v1)

| Tecnologia | Versão |
|------------|--------|
| Laravel | **12** |
| PHP | **8.3+** |
| Next.js | **15** (App Router) |
| Node.js | **20 LTS** |
| MySQL | **8.x** |
| React | 19 (via Next / Inertia) |
| Tailwind CSS | 4.x (web) / 3.x (admin) |
| Framer Motion | latest |
| next-intl | 4.x |

## Monorepo

```
/
├── apps/web/          # Next.js → Vercel
├── apps/api/          # Laravel → Hostinger
├── packages/types/    # contratos API TypeScript
├── docker/            # Dockerfiles (api, web)
├── docker-compose.yml
├── .cursor/
├── portfolio-data.md
└── README.md
```

## Stack por camada

| Camada | Tecnologia | Onde |
|--------|------------|------|
| Site público | Next.js 15 + next-intl | Vercel |
| UI site | Tailwind + componentes custom | `apps/web` |
| Animações | Framer Motion | `apps/web` |
| API REST | Laravel 12 `/api/v1` | Hostinger |
| Painel admin | Inertia.js + React + Vite | `apps/api` |
| Auth admin | Breeze-style (sessão) | `apps/api` |
| Banco | MySQL + Eloquent | Hostinger |
| i18n conteúdo | JSON `{pt,en}` + DeepL | Laravel |
| Mídia | `storage/app/public` | Laravel |

## Comunicação

- `NEXT_PUBLIC_API_URL=https://admin.maiconoliveiradev.com.br`
- `API_INTERNAL_URL=http://api:8000` (SSR no Docker)
- CORS: `maiconoliveiradev.com.br` + `www` + `*.vercel.app` (staging)
- API: [api-conventions.md](../docs/api-conventions.md)

## Fora do escopo v1

- PostgreSQL / Prisma / Sanctum
- Docker em produção (só dev local)
- Filtro projetos por stack

## Status (2026-07-03)

- [x] Arquitetura, domínios, versões
- [x] Monorepo, i18n, DeepL, design
- [x] API conventions documentadas
- [x] Scaffold `apps/web` + `apps/api` gerado
- [x] `packages/types` implementado
- [x] API v1 + admin 8 módulos
- [x] Site público 5 rotas
- [x] Docker Compose local
- [x] Deploy produção (Vercel + Hostinger)
- [x] Deploy contínuo (Vercel auto + Hostinger Git)
- [x] Vercel Analytics
- [ ] GitHub Actions lint/test em PR (opcional)
