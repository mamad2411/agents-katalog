---
name: github-actions-data
description: GitHub Actions para el pipeline ETL semanal de SeguroData — activación, secrets y ejecución manual.
---

# GitHub Actions Data — SeguroData Bogotá

El workflow `.github/workflows/etl-semanal.yml` automatiza la descarga incremental de las 12 fuentes de datos.

## Estado actual

El workflow está **DESACTIVADO**. La carga de datos se hace manualmente durante el concurso.

Para activarlo manualmente en cualquier momento:
**GitHub → Actions → ETL semanal → Run workflow**

## Activar el cron automático

```yaml
# En .github/workflows/etl-semanal.yml
# Descomentar el bloque schedule para activar el cron:
on:
  schedule:
    - cron: '0 6 * * 1'  # Cada lunes a las 6am UTC (1am Bogotá)
  workflow_dispatch:       # También permite ejecución manual
```

Después de descomentar, hacer commit → GitHub activa el cron automáticamente.

## Secrets requeridos en GitHub

Agregar en: **GitHub → Settings → Secrets and variables → Actions**

| Secret | Valor | Para qué |
|--------|-------|---------|
| `SOCRATA_APP_TOKEN` | Token gratuito de dev.socrata.com | F5 NUSE, F6 Hurto PN |
| `SUPABASE_URL` | URL del proyecto Supabase | Carga de datos a BD |
| `SUPABASE_SERVICE_KEY` | Service key de Supabase | Escritura en tablas |

## Estructura del workflow

```yaml
# .github/workflows/etl-semanal.yml
name: ETL semanal
on:
  workflow_dispatch:
  # schedule: - cron: '0 6 * * 1'  # ← descomentar para activar

jobs:
  etl:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with: { python-version: '3.11' }
      - run: pip install -r requirements.txt -q
      - run: python src/pipeline.py
        env:
          SOCRATA_APP_TOKEN: ${{ secrets.SOCRATA_APP_TOKEN }}
          SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          SUPABASE_SERVICE_KEY: ${{ secrets.SUPABASE_SERVICE_KEY }}
```

## Advertencias

- **No activar el cron antes del concurso** — ejecutar el pipeline manualmente es suficiente y más controlado
- Si el workflow falla: revisar en la tab "Actions" de GitHub para ver el log completo
- F7 (estratificación) tarda varios minutos y puede fallar en el runner gratuito — ejecutar localmente en su lugar

## Ejecutar localmente (equivalente al workflow)

```bash
export SOCRATA_APP_TOKEN=<tu_token>
python src/pipeline.py --status          # verificar estado
python src/pipeline.py                   # ejecutar descarga incremental
python src/transform.py                  # Bronze → Silver
```
