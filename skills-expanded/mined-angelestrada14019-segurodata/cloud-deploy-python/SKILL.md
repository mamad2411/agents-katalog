---
name: cloud-deploy-python
description: Deploy completo de SeguroData — FastAPI a Railway + React a Vercel + setup Supabase.
---

# Cloud Deploy Python — SeguroData Bogotá

Deploy del sistema completo: backend Python (FastAPI → Railway) + frontend React (→ Vercel) + base de datos (Supabase).

## Arquitectura de deploy

```
Frontend React + deck.gl  →  Vercel   (CDN global, siempre activo, gratis)
Backend FastAPI (Python)  →  Railway  (siempre activo, SIN cold start, ~$5/mes plan Hobby)
Base de datos             →  Supabase (PostgreSQL + PostGIS + pgvector, proyecto `segurodata` ref pluxaelenhkdaakxdrpm)
LLM proxy                 →  OpenRouter (server-side en Railway, NUNCA en browser)
```

## 1. Deploy Backend — Railway

```bash
# Opción A (recomendada): GitHub integration
# 1. railway.app → New Project → Deploy from GitHub repo
# 2. Root Directory: backend/  (Railway detecta el Dockerfile)
# 3. Configurar variables de entorno en el dashboard (ver abajo)
# 4. Cada push a main redeploya automáticamente

# Opción B: CLI
railway login
railway link          # vincular al proyecto Railway
cd backend
railway up            # build + deploy del Dockerfile

# URL resultante: https://<app>.up.railway.app
# Guardar esta URL para el frontend como VITE_API_URL
```

Variables de entorno en Railway (dashboard → Variables):
```bash
ENV=production
SUPABASE_URL=https://pluxaelenhkdaakxdrpm.supabase.co
SUPABASE_SERVICE_KEY=eyJ...
SUPABASE_JWT_SECRET=...
OPENROUTER_API_KEY=sk-or-...
LLM_MODEL=google/gemini-2.5-flash-lite
LLM_MODEL_FALLBACK=anthropic/claude-3-haiku
CORS_ORIGINS=https://<dominio-vercel>
```

`backend/railway.toml` define el healthcheck:
```toml
[deploy]
healthcheckPath = "/health"
healthcheckTimeout = 300     # la primera carga del modelo de embeddings tarda
restartPolicyType = "ON_FAILURE"
```

**No hay pre-calentamiento**: Railway mantiene el contenedor siempre activo — listo para demo sin warmup.

## 2. Deploy Frontend — Vercel

```bash
# Opción A: desde vercel.com (recomendado)
# 1. Conectar repositorio GitHub en vercel.com
# 2. Seleccionar carpeta /frontend — Framework preset: Vite
# 3. Agregar variables de entorno

# Opción B: CLI
cd frontend && vercel
```

Variables de entorno en Vercel:
```
VITE_SUPABASE_URL=https://pluxaelenhkdaakxdrpm.supabase.co
VITE_SUPABASE_ANON_KEY=eyJ...           (clave pública — OK exponer)
VITE_API_URL=https://<app>.up.railway.app
```

## 3. Setup Supabase

Las migraciones viven en `supabase/migrations/*.sql` (aplicadas vía MCP Supabase o SQL Editor). Scripts de datos:

```bash
# .env en raíz: SUPABASE_URL, SUPABASE_SERVICE_KEY, SUPABASE_DB_URL (para COPY bulk)
python scripts/seed_supabase.py         # silver + geometrías F2/F4 + predicciones/shap sintéticos (origen='seed_dev')
python scripts/index_corpus.py          # embeddings F10 → documents_corpus (pgvector)
python scripts/load_model_artifacts.py  # SWITCH: borra seed_dev y carga artefactos reales de Notebooks 03/04
```

Paso manual post-migración: habilitar `custom_access_token_hook` en Dashboard → Auth → Hooks.

## Checklist de entrega (agosto 2026)

- [ ] FastAPI en Railway respondiendo — URL pública activa, /health 200
- [ ] React en Vercel — URL pública, los 4 módulos funcionando
- [ ] Supabase — predicciones + SHAP reales (origen='notebook_04') + pgvector cargados
- [ ] Hook de claims habilitado y JWT e2e verificado (pre-mortem E3)
- [ ] Registro del proyecto en datos.gov.co (sección "Usos") — **OBLIGATORIO**
- [ ] README actualizado con las 3 URLs (GitHub + Vercel + Railway)

## Costos del stack (demo/concurso)

| Servicio | Costo | Límite |
|---------|-------|--------|
| Railway (plan Hobby) | ~$5/mes | 8 GB RAM, siempre activo, sin cold start |
| Vercel | $0 | Bandwidth de sobra en proyectos hobby |
| Supabase | $0 | 500 MB DB + 1 GB storage + 2 GB transfer |
| OpenRouter | <$1/mes | Gemini Flash Lite, costo marginal por consulta (`:free` no confiables, ver `docs/chatbot_test_battery.md`) |
| **Total** | **~$5-6/mes** | Suficiente para el concurso |
