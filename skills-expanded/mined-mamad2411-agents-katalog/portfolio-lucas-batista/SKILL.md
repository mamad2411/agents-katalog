# Cursor Rules — Portfólio Lucas Batista

## Entrada obrigatória

Leia, nesta ordem: `AGENTS.md`, `docs/CANON.md`, `docs/ARQUITETURA.md` e o
documento específico da tarefa no índice `docs/README.md`.

## Norte do produto

O projeto é um _Executive Proof System_ para headhunters e lideranças de
operações/dados. Não o transforme em landing SaaS, currículo genérico ou
dashboard decorativo.

Ordem canônica: `Header → ExecutiveHero → EvidenceStrip → ProfileBrief →
SignatureCases → TrajectoryBoard → ContactPanel → Footer`.

## Arquitetura e fontes da verdade

- O repositório é único; o Streamlit vive em `apps/demos/`.
- Copy, cases, CTAs e links: `data/content.ts`.
- Slugs, tiers, pages e publicação: `contracts/demo-catalog.json`.
- Cálculos exibidos nas âncoras: `contracts/demo-snapshots/*.json`, exportados
  pelo Python.
- Tokens editáveis: `design/tokens.json`.
- Fila: `docs/ROADMAP.md`.
- Operação e deploy: `docs/OPERACAO.md`.

Não editar manualmente `app/design-tokens.css`,
`apps/demos/presentation/tokens.py`, `.streamlit/config.toml` ou snapshots.
Use `npm run tokens:sync` e `npm run demos:export`.

Não recriar `demos-logistica/`, clones de deploy, sincronização por `robocopy`
ou pastas históricas na árvore ativa.

## Código e design

- Next.js 16, React 19, TypeScript, Tailwind CSS v4 e Node 24.x.
- Não criar `tailwind.config.ts`.
- Server Components por padrão; `'use client'` apenas para interação real.
- Props tipadas, sem `any`, copy narrativa hardcoded ou `console.log` em
  produção.
- Lucide é a única biblioteca de ícones React.
- ECharts, MapLibre, modal e Analytics permanecem lazy.
- Mobile-first em 375 px; validar também 768 e 1440 px.
- Tipografia Source Serif 4 + Inter; cores somente via tokens.
- Evitar cards, badges, sombras, gradientes e animações sem função.
- Garantir foco visível, `ESC`, reduced motion, semântica e touch targets de
  pelo menos 44 px.

## Gate antes de commit

```powershell
npm run format
npm run verify
npm run demos:smoke
npm run test:e2e
npm audit --audit-level=moderate
```

Mudança visual também exige `npm run qa:visual`, `npm run qa:streamlit` e
`npm run lighthouse:all` com os servidores locais ativos. Lighthouse deve ficar
em pelo menos 90 nas quatro categorias.

Não publicar, fazer push ou alterar serviços externos sem autorização
explícita.
