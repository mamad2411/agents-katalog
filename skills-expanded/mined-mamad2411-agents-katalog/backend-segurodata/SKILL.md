---
name: backend-segurodata
description: Contrato completo del backend FastAPI de SeguroData — endpoints, schemas JSON, matriz endpoint×rol, claims JWT, env vars, árbol de backend/app/ y decisiones de arquitectura D1-D12. Fuente única de verdad para implementar o revisar código en backend/.
---

# Backend SeguroData — Contrato y Arquitectura

Backend FastAPI en Railway (siempre activo). Supabase = datos + auth + pgvector. OpenRouter = proxy LLM. Proyecto Supabase: `segurodata` (ref `pluxaelenhkdaakxdrpm`, us-east-1).

## Los 7 endpoints

### POST /predict — nivel de riesgo por UPZ×mes (lookup, NO inferencia)

```json
// Request
{ "upz_cod": "044", "anio": 2026, "mes": 7 }
// Response 200
{
  "upz_cod": "044", "anio": 2026, "mes": 7,
  "nivel_riesgo": "ALTO",
  "probabilidades": { "CRITICO": 0.08, "ALTO": 0.62, "MEDIO": 0.24, "BAJO": 0.06 },
  "origen": "seed_dev"
}
```
Lookup a tabla `predicciones` por PK (upz_cod, anio, mes). 404 si no existe la fila.

### GET /explain?upz_cod=044&anio=2026&mes=7 — SHAP pre-computado

```json
// Response 200 (CIUDADANO / COMANDANTE_CAI)
{
  "upz_cod": "044", "anio": 2026, "mes": 7, "nivel_riesgo": "ALTO",
  "shap_top3": [
    { "feature": "cuadrantes_por_km2", "valor": -0.34 },
    { "feature": "n_delitos_upz_4sem", "valor": 0.28 },
    { "feature": "luminarias_led_upz", "valor": -0.19 }
  ]
}
// ANALISTA_SDSCJ / ADMIN reciben además: "shap_completo": [ ...las 18 features ]
```

### POST /graphrag — chatbot causal con citas

```json
// Request
{ "pregunta": "¿Por qué aumentó el hurto en Kennedy?", "upz_contexto": "044" }
// Response 200
{
  "respuesta": "Según el Boletín SCJ de noviembre 2025...",
  "fuentes": [
    { "tipo": "RSS_ELTIEMPO", "titulo": "El Tiempo — ...", "fecha": "2026-06-11", "url": "https://..." },
    { "tipo": "RSS_INFORMANTE", "titulo": "El Informante Soy Yo — ...", "fecha": "2026-04-29", "url": "https://..." }
  ],
  "modelo_llm": "google/gemini-2.5-flash-lite", "cacheado": false
}
```
Flujo: embed pregunta (MiniLM local) → RPC `match_documents(threshold=0.7, count=5, filter_upz)` → si 0 con filtro, retry sin filtro → prompt con chunks → OpenRouter (caché TTL 24h).

### POST /prescribe — recomendación operacional (roles: COMANDANTE_CAI, ANALISTA_SDSCJ, ADMIN)

```json
// Request
{ "upz_cod": "044", "shap_top": [{ "feature": "cuadrantes_por_km2", "valor": -0.34 }] }
// Response 200
{
  "upz_cod": "044",
  "diagnosticos": [{
    "feature": "cuadrantes_por_km2", "diagnostico": "Baja cobertura policial",
    "tipo_intervencion": "Seguridad", "entidad_responsable": "MEBOG / SIJIN",
    "accion": "Reforzar cuadrante + CAI"
  }],
  "cai": { "nombre": "CAI Américas", "cuadrante_id": "...", "telefono": null },
  "recomendacion_llm": "UPZ 44 — Américas: ...(máx 200 palabras, lenguaje operacional)"
}
```
Mapeo feature→diagnóstico→entidad es DETERMINISTA (tabla ontológica 17 filas, `app/data/tabla_ontologica_seed.json`, override env `TABLA_ONTOLOGICA_PATH`). El LLM solo redacta.

### GET /whoami — pre-mortem T5

```json
// Response 200
{ "rol": "COMANDANTE_CAI", "cuadrante_asignado": null, "cuadrante_pendiente": true }
```
`cuadrante_pendiente = (rol == COMANDANTE_CAI && cuadrante_asignado == null)` — el frontend muestra aviso en vez de mapa vacío.

### GET /health — sin auth, sin rate limit

```json
{ "status": "ok", "version": "0.1.0", "env": "production" }
```

### PATCH /admin/usuarios/{user_id}/cuadrante — asignar cuadrante (solo ADMIN, pre-mortem T5)

```json
// Request
{ "cuadrante_id": "E12C02013" }
// Response 200
{ "user_id": "c6967b12-...", "cuadrante_asignado": "E12C02013" }
```
404 si `cuadrante_id` no existe en `cuadrantes_geom` o si `user_id` no existe en `user_profiles`.
Antes de este endpoint, `cuadrante_asignado` solo se podía tocar por SQL/Dashboard manual — cierra
el flujo de `/whoami.cuadrante_pendiente` de punta a punta.

## Matriz endpoint × rol

| Endpoint | Sin token | CIUDADANO | COMANDANTE_CAI | ANALISTA_SDSCJ | ADMIN |
|---|---|---|---|---|---|
| GET /health | ✅ | ✅ | ✅ | ✅ | ✅ |
| POST /predict | 401 | ✅ todas las UPZ | ✅ solo UPZs de su cuadrante (403 fuera) | ✅ | ✅ |
| GET /explain | 401 | ✅ top-3 | ✅ top-3 (su cuadrante) | ✅ completo | ✅ completo |
| POST /graphrag | 401 | ✅ | ✅ | ✅ | ✅ |
| POST /prescribe | 401 | **403** | ✅ | ✅ | ✅ |
| GET /whoami | 401 | ✅ | ✅ | ✅ | ✅ |
| PATCH /admin/usuarios/{id}/cuadrante | 401 | 403 | 403 | 403 | ✅ |

Rate limits (slowapi, por IP): /graphrag y /prescribe **10/min**; demás autenticados 60/min; /health sin límite.

## JWT y claims

- El proyecto real firma con **ES256/JWKS** (verificado en vivo, pre-mortem E3: `SUPABASE_JWKS_URL` →
  `<url>/auth/v1/.well-known/jwks.json`). `decode_supabase_jwt` soporta ambas ramas — ES256/RS256 vía
  `SUPABASE_JWKS_URL` (escape hatch real, usar esta), o HS256 legacy vía `SUPABASE_JWT_SECRET` (solo
  para tests unitarios con secret falso, ver `backend/tests/conftest.py`); audience `authenticated`.
- Claims custom inyectados por `public.custom_access_token_hook`: `rol` (CIUDADANO|COMANDANTE_CAI|ANALISTA_SDSCJ|ADMIN) y `cuadrante_asignado` (str|null). El hook NO filtra por `user_profiles.aprobado` — inyecta el `rol` tal cual esté en la fila.
- El hook se habilita manualmente: Dashboard → Auth → Hooks → Custom Access Token.
- Dev local: `AUTH_MODE=disabled` inyecta usuario fake ADMIN — SOLO si `ENV=development` (guard en config).

## Decisiones de arquitectura (cerradas — no reabrir)

| # | Decisión |
|---|---|
| D1 | supabase-py v2 async envuelto en repositories. Bulk offline: psycopg + COPY |
| D2 | /predict = lookup puro a `predicciones`. PROHIBIDO importar xgboost/shap en backend/app/ |
| D3 | Seed sintético `origen='seed_dev'`; switch a real con `scripts/load_model_artifacts.py` |
| D4 | Embeddings: sentence-transformers all-MiniLM-L6-v2 (384d) en el backend, torch CPU-only, modelo horneado en Docker. Plan B: fastembed (solo tocar clients/embeddings.py) |
| D5 | slowapi in-memory (1 instancia Railway) |
| D6 | TTLCache(256, 24h) para OpenRouter, key sha256(model+prompt) |
| D7 | PyJWT HS256 + SUPABASE_JWT_SECRET; SUPABASE_JWKS_URL opcional como escape |
| D8 | **La service key bypasea RLS** → filtro rol/cuadrante EXPLÍCITO en services. RLS protege solo al frontend |
| D9 | pgvector HNSW (m=16, ef_construction=64), cosine |
| D10 | Tabla ontológica = JSON estático bundleado, 17 filas |
| D11 | structlog JSON + middleware request_id/timing |
| D12 | ruff lint+format |

## Árbol backend/

```
backend/app/
├── main.py config.py dependencies.py exceptions.py middleware.py logging_config.py
├── routers/    health predict explain graphrag prescribe auth admin
├── schemas/    common predict explain graphrag prescribe auth admin
├── services/   prediction_service explain_service graphrag_service prescribe_service admin_service
├── repositories/ predictions_repo shap_repo documents_repo cuadrantes_repo ontology_repo user_profiles_repo
├── clients/    supabase_client openrouter_client embeddings
├── core/       security.py cache.py
└── data/       tabla_ontologica_seed.json
backend/tests/  conftest + test por router + test_admin + test_jwt_e2e (integration, verde con
                credenciales reales) + test_whoami (T5, verificado también en vivo)
```

## Env vars (backend/.env.example)

```bash
ENV=development                      # development | production
AUTH_MODE=enabled                    # disabled solo permitido si ENV=development
SUPABASE_URL=https://pluxaelenhkdaakxdrpm.supabase.co
SUPABASE_SERVICE_KEY=                # service_role — NUNCA al frontend
SUPABASE_JWT_SECRET=                 # dejar vacío si el proyecto usa ES256 (ver SUPABASE_JWKS_URL)
SUPABASE_JWKS_URL=                   # <SUPABASE_URL>/auth/v1/.well-known/jwks.json — proyecto real usa ES256
SUPABASE_DB_URL=                     # solo scripts offline (COPY bulk), no el backend
OPENROUTER_API_KEY=
LLM_MODEL=google/gemini-2.5-flash-lite
LLM_MODEL_FALLBACK=anthropic/claude-3-haiku
LLM_MAX_TOKENS=600
LLM_CACHE_TTL_SECONDS=86400
LLM_CACHE_MAXSIZE=256
EMBEDDINGS_MODEL=sentence-transformers/all-MiniLM-L6-v2
CORS_ORIGINS=http://localhost:5173   # prod: dominio Vercel exacto, sin *
RATE_LIMIT_DEFAULT=60/minute
RATE_LIMIT_LLM=10/minute             # /graphrag y /prescribe
TABLA_ONTOLOGICA_PATH=               # opcional: override del JSON bundleado
```

## Presupuestos de latencia

- /predict, /explain, /whoami: **<500ms** (lookup por PK + 1 query opcional de cuadrante)
- /graphrag: **<2s** (embed ~50ms + RPC ~150ms + Gemini Flash ~1.5s; cacheado <100ms)
- Si un cambio agrega un round-trip a Supabase, debe justificarse contra estos presupuestos.

## Comandos de verificación

```bash
cd backend
uvicorn app.main:app --reload                          # local
ruff check . && ruff format --check .
python -m pytest tests/ -m "not integration" -q       # suite unit
python -m pytest tests/test_jwt_e2e.py -m integration  # E3, requiere credenciales reales
```
