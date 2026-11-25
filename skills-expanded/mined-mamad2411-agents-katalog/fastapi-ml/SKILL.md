---
name: fastapi-ml
description: Backend FastAPI del sistema SeguroData — endpoints /predict, /explain, /graphrag, /prescribe, /whoami en Railway (siempre activo). Patrones de capas, Pydantic v2 y integración Supabase/OpenRouter.
---

# FastAPI ML — SeguroData Bogotá

El backend Python es el único servicio de la Capa 4. Corre en **Railway** (siempre activo, sin cold start, ~$5/mes plan Hobby).

> El contrato completo (request/response JSON, matriz endpoint×rol, decisiones D1-D12) está en la skill `backend-segurodata` — es la fuente única de verdad.

## Estructura del backend

```
backend/
├── app/
│   ├── main.py              ← create_app() factory + lifespan + wiring
│   ├── config.py            ← Settings (pydantic-settings)
│   ├── dependencies.py      ← get_supabase, get_current_user, require_roles
│   ├── exceptions.py        ← errores de dominio + handlers centralizados
│   ├── middleware.py        ← request_id + access log con latencia
│   ├── routers/             ← health, predict, explain, graphrag, prescribe, auth (/whoami)
│   ├── schemas/             ← Pydantic v2 por endpoint
│   ├── services/            ← lógica de negocio + filtro por rol (D8)
│   ├── repositories/        ← acceso a tablas/RPC Supabase
│   ├── clients/             ← supabase_client, openrouter_client, embeddings
│   ├── core/                ← security.py (JWT), cache.py
│   └── data/                ← tabla_ontologica_seed.json
├── tests/                   ← pytest + httpx ASGITransport + token_factory
├── Dockerfile · railway.toml · requirements.txt · .env.example
```

## Endpoints principales

```python
# POST /predict — LOOKUP a tabla predicciones (pre-computado; NUNCA inferencia en runtime)
{ "upz_cod": "044", "anio": 2026, "mes": 7 }
# → { "nivel_riesgo": "ALTO", "probabilidades": {"CRITICO":0.08,"ALTO":0.62,"MEDIO":0.24,"BAJO":0.06}, "origen": "seed_dev" }

# GET /explain?upz_cod=044&anio=2026&mes=7 — SHAP pre-computado desde Supabase
# → { "shap_top3": [{"feature":"cuadrantes_por_km2","valor":-0.34}, ...] }  (+shap_completo si ANALISTA/ADMIN)

# POST /graphrag — RAG sobre corpus F10 (pgvector + OpenRouter)
{ "pregunta": "¿Por qué aumentó el hurto en Kennedy?", "upz_contexto": "044" }
# → { "respuesta": "...", "fuentes": [...], "modelo_llm": "...", "cacheado": false }

# POST /prescribe — tabla ontológica (determinista) + redacción LLM. Roles: COMANDANTE/ANALISTA/ADMIN
{ "upz_cod": "044", "shap_top": [{"feature": "cuadrantes_por_km2", "valor": -0.34}] }
# → { "diagnosticos": [...], "cai": {...}, "recomendacion_llm": "..." }

# GET /whoami — pre-mortem T5
# → { "rol": "COMANDANTE_CAI", "cuadrante_asignado": null, "cuadrante_pendiente": true }
```

## Variables de entorno (Railway)

```bash
OPENROUTER_API_KEY=sk-or-...              # OpenRouter — costo marginal (:free no confiables)
LLM_MODEL=google/gemini-2.5-flash-lite    # Modelo por defecto
LLM_MODEL_FALLBACK=anthropic/claude-3-haiku
SUPABASE_URL=https://pluxaelenhkdaakxdrpm.supabase.co
SUPABASE_SERVICE_KEY=eyJ...        # Service key — NUNCA exponer al frontend
SUPABASE_JWT_SECRET=...            # Para verificar JWTs de Supabase Auth (HS256)
CORS_ORIGINS=https://<dominio-vercel>
ENV=production
```

## Desarrollo local

```bash
cd backend
pip install -r requirements.txt -r requirements-dev.txt
uvicorn app.main:app --reload --port 8000
# API docs en: http://localhost:8000/docs
# Sin Supabase Auth configurado: ENV=development + AUTH_MODE=disabled (usuario fake ADMIN)
```

## Deploy a Railway

```bash
# Opción A: GitHub integration (recomendado) — conectar repo en railway.app, root dir backend/
# Opción B: CLI
railway login
railway link
cd backend && railway up
# Railway detecta el Dockerfile; env vars se configuran en el dashboard
```

Railway es **siempre activo** — no hay cold start ni pre-calentamiento. El healthcheck (`railway.toml` → `healthcheckPath = "/health"`) valida cada deploy.

## Integración con Supabase pgvector (GraphRAG)

```python
# El endpoint /graphrag embebe la pregunta con sentence-transformers
# (all-MiniLM-L6-v2 — 384 dims, corre local en el contenedor, horneado en la imagen Docker)
embedding = await embeddings_client.encode(pregunta)   # run_in_executor — no bloquear event loop

result = await supabase.rpc("match_documents", {
    "query_embedding": embedding,
    "match_threshold": 0.7,
    "match_count": 5,
    "filter_upz": upz_contexto,
}).execute()
# Si 0 resultados con filtro → reintentar sin filtro (nunca respuesta vacía)
```

## Notas críticas

- La `OPENROUTER_API_KEY` se configura en Railway — **NUNCA** en el frontend ni en el código
- SHAP values y predicciones se sirven desde Supabase (pre-computados en Notebook 04) — **NUNCA** calcular on-demand ni importar xgboost/shap en backend/app/
- **La service key bypasea RLS** → el filtro por rol/cuadrante se aplica explícito en la capa services (D8)
- CORS: permitir solo el dominio de Vercel en producción, localhost:5173 en desarrollo
- Datos seed: las filas sintéticas llevan `origen='seed_dev'`; el switch a artefactos reales es `scripts/load_model_artifacts.py`
