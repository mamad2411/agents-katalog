---
name: arbx-i-i034-on-call-rotations-escalation
description: "PhD/Master skill alineada al monorepo hefarica/arbitragex-v2 (Observability & SRE). Se activa cuando: paging policy. Doctrina OMEGA Zero-Mocks · Fail-Closed · El Remoto Manda."
---

# I034 — On-Call Rotations & Escalation

> **Dominio:** Observability & SRE
> **Nivel:** PhD/Master
> **Trigger:** paging policy
> **Repos de referencia:** open-telemetry/opentelemetry-rust · prometheus/prometheus · grafana/{grafana,loki,tempo,mimir} · vectordotdev/vector · fluent/fluent-bit · cilium/cilium
> **Archivos del repo:** ops/grafana/dashboards/* · ops/prometheus/rules/* · services/*/src/observability/*

## Quick Start

```bash
docker compose -f ops/observability/compose.yml up -d && curl -s :9090/-/ready
```

## Core Workflow

1. Cargar contexto del repo `hefarica/arbitragex-v2` (rama actual, último PR, estado de CI).
2. Identificar el subsistema impactado dentro de los archivos del repo listados arriba.
3. Aplicar la doctrina del nivel **PhD/Master** sin desviaciones.
4. Validar contra: `lint → typecheck → build → tests → audit → E2E → deploy`.
5. Reportar evidencia en formato Markdown forense (logs, traces, métricas, hash de commit).

## Doctrina del Nivel

- Zero mocks, zero hardcode, zero `.unwrap()` en hot-path.
- Toda función pura testeada con property tests.
- Spec antes que código (RFC interno).

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

- `paging policy`
- `on-call rotations & escalation`
- `arbitragex-v2 i`

## Output Esperado

- Diff atómico (rustfmt aparte de semántica).
- Evidencia: `gh pr checks <N>`, `cargo nextest`, traces OTel, screenshots Playwright.
- ADR si la decisión cambia contrato (`docs/adr/NNNN-*.md`).


---