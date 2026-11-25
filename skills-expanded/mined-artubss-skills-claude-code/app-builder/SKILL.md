---
name: app-builder
description: Orquestrador principal de construção de aplicações. Cria aplicações full-stack a partir de requisições em linguagem natural. Determina o tipo de projeto, seleciona a tech stack e coordena agentes.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

# App Builder - Orquestrador de Construção de Aplicações

> Analisa requisições do usuário, determina tech stack, planeja estrutura e coordena agentes.

## 🎯 Regra de Leitura Seletiva

**Leia APENAS os arquivos relevantes para a requisição!** Verifique o mapa de conteúdo e encontre o que você precisa.

| Arquivo | Descrição | Quando Ler |
|---------|-----------|-----------|
| `project-detection.md` | Matriz de palavras-chave, detecção de tipo de projeto | Iniciando novo projeto |
| `tech-stack.md` | Stack padrão 2025, alternativas | Escolhendo tecnologias |
| `agent-coordination.md` | Pipeline de agentes, ordem de execução | Coordenando trabalho multi-agente |
| `scaffolding.md` | Estrutura de diretórios, arquivos principais | Criando estrutura do projeto |
| `feature-building.md` | Análise de features, tratamento de erros | Adicionando features ao projeto existente |
| `templates/SKILL.md` | **Templates de projeto** | Scaffolding de novo projeto |

---

## 📦 Templates (13)

Scaffolding rápido para novos projetos. **Leia apenas o template correspondente!**

| Template | Tech Stack | Quando Usar |
|----------|-----------|------------|
| [nextjs-fullstack](templates/nextjs-fullstack/TEMPLATE.md) | Next.js + Prisma | App web full-stack |
| [nextjs-saas](templates/nextjs-saas/TEMPLATE.md) | Next.js + Stripe | Produto SaaS |
| [nextjs-static](templates/nextjs-static/TEMPLATE.md) | Next.js + Framer | Landing page |
| [nuxt-app](templates/nuxt-app/TEMPLATE.md) | Nuxt 3 + Pinia | App full-stack Vue |
| [express-api](templates/express-api/TEMPLATE.md) | Express + JWT | API REST |
| [python-fastapi](templates/python-fastapi/TEMPLATE.md) | FastAPI | API Python |
| [react-native-app](templates/react-native-app/TEMPLATE.md) | Expo + Zustand | App mobile |
| [flutter-app](templates/flutter-app/TEMPLATE.md) | Flutter + Riverpod | Mobile multiplataforma |
| [electron-desktop](templates/electron-desktop/TEMPLATE.md) | Electron + React | App desktop |
| [chrome-extension](templates/chrome-extension/TEMPLATE.md) | Chrome MV3 | Extensão de navegador |
| [cli-tool](templates/cli-tool/TEMPLATE.md) | Node.js + Commander | App CLI |
| [monorepo-turborepo](templates/monorepo-turborepo/TEMPLATE.md) | Turborepo + pnpm | Monorepo |

---

## 🔗 Agentes Relacionados

| Agente | Papel |
|--------|-------|
| `project-planner` | Breakdown de tarefas, grafo de dependências |
| `frontend-specialist` | Componentes UI, páginas |
| `backend-specialist` | API, lógica de negócio |
| `database-architect` | Schema, migrations |
| `devops-engineer` | Deploy, preview |

---

## Exemplo de Uso

```
Usuário: "Faça um clone do Instagram com compartilhamento de fotos e likes"

Processo App Builder:
1. Tipo de projeto: Aplicação Social Media
2. Tech stack: Next.js + Prisma + Cloudinary + Clerk
3. Criar plano:
   ├─ Schema do banco (users, posts, likes, follows)
   ├─ Routes de API (12 endpoints)
   ├─ Páginas (feed, profile, upload)
   └─ Componentes (PostCard, Feed, LikeButton)
4. Coordenar agentes
5. Relatar progresso
6. Iniciar preview
```