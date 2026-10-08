name: arbx-g-g005-advanced-react-19-usetransitionuseoptimistic
description: "Post-Doc skill alineada al monorepo hefarica/arbitragex-v2 (Frontend Doctrinal (Next.js + Playwright)). Se activa cuando: server actions form state. Doctrina OMEGA Zero-Mocks · Fail-Closed · El Remoto Manda."
---

# G005 — Advanced React 19 useTransition/useOptimistic

> **Dominio:** Frontend Doctrinal (Next.js + Playwright)
> **Nivel:** Post-Doc
> **Trigger:** server actions form state
> **Repos de referencia:** vercel/next.js · facebook/react · microsoft/playwright · TanStack/query · shadcn-ui/ui · radix-ui/primitives · wevm/viem · wagmi-dev/wagmi
> **Archivos del repo:** frontend/app/* · frontend/components/* · frontend/tests/e2e/* · packages/schemas/*

## Quick Start

```bash
ARBX_BUILD_FOR_LOCAL_E2E=1 ARBX_ASSUME_NO_RPC=1 pnpm playwright test --reporter=list,html
```

## Core Workflow

1. Cargar contexto del repo `hefarica/arbitragex-v2` (rama actual, último PR, estado de CI).
2. Identificar el subsistema impactado dentro de los archivos del repo listados arriba.
3. Aplicar la doctrina del nivel **Post-Doc** sin desviaciones.
4. Validar contra: `lint → typecheck → build → tests → audit → E2E → deploy`.
5. Reportar evidencia en formato Markdown forense (logs, traces, métricas, hash de commit).

## Doctrina del Nivel

- Aporte de investigación: paper o RFC referenciado.
- Benchmarks reproducibles con criterio estadístico (95% CI).
- Comparativa contra estado del arte público.

## Reglas de Ejecución

| Condición | Acción |
|-----------|--------|
| CI rojo en `main` | ABORT — fix-forward, nunca skip |
| Drift schema producer↔consumer | ABORT — restaurar isomorfismo Zod/struct |
| Cobertura E2E < contrato iter 18 | ABORT — añadir testid + assertion DEGRADED/UP/DOWN |
| Secret en plaintext fuera de Vault/age | ABORT — rotar y reportar |
| Profit neto ≤ gas + flashloan_fee | ABORT (skill C/E) |
| Slippage > banda RiskGate | RESIZE o ABORT (skill C/E) |

## Activation Triggers (regex parciales)

- `server actions form state`
- `advanced react 19 usetransition/useoptimistic`
- `arbitragex-v2 g`

## Output Esperado

- Diff atómico (rustfmt aparte de semántica).
- Evidencia: `gh pr checks <N>`, `cargo nextest`, traces OTel, screenshots Playwright.
- ADR si la decisión cambia contrato (`docs/adr/NNNN-*.md`).


---