# SIDEM-PAN — Guía para Claude Code

## Proyecto

Sistema de debida diligencia migratoria para Panamá. Monorepo con backend Express + TypeScript y frontend React 19 + Vite.

## Estructura clave

- `backend/src/lib/supabase.ts` — cliente Supabase admin (service key). Usar para todas las queries a la BD.
- `backend/src/services/audit.ts` — `logAction()` para auditoría WORM. Llamar siempre que se cree o modifique un expediente.
- `backend/src/services/risk-engine.ts` — `calcularRiesgo()` para scoring. Se llama al crear una application.
- `backend/src/routes/applications.ts` — endpoints CRUD de expedientes.
- `backend/src/middleware/auth.ts` — `requireAuth('AGENTE','ADMIN')` para proteger rutas.
- `frontend/src/lib/api.ts` — cliente HTTP del frontend. Agregar aquí funciones nuevas para llamar al backend.

## Base de datos

Supabase proyecto `wlzrvuwuhbtrjobcarar`. Tablas:
- `agentes` — usuarios con rol AGENTE o ADMIN
- `applications` — expedientes migratorios
- `dictamenes` — decisiones de agentes
- `control_lists` — listas INTERPOL, OFAC, países restringidos
- `audit_log` — WORM (triggers impiden DELETE y UPDATE)

Para queries usa el cliente Supabase (`supabase.from('tabla').select()`). Para funciones SQL usa `supabase.rpc('nombre_funcion')`.

## Variables de entorno

Backend (`backend/.env`):
- `SUPABASE_URL` — URL del proyecto Supabase
- `SUPABASE_SERVICE_KEY` — service_role key (nunca commitear)
- `JWT_SECRET` — secreto para firmar tokens
- `JWT_EXPIRES_IN` — duración del token (default 15m)

Frontend (`frontend/.env`):
- `VITE_API_URL` — base URL del API (default `/api`)
- `VITE_SUPABASE_URL` — URL del proyecto
- `VITE_SUPABASE_ANON_KEY` — anon key pública

## Comandos

```bash
# Backend
cd backend && npm run dev    # nodemon + ts-node, puerto 4000

# Frontend
cd frontend && npm run dev   # Vite, puerto 5173
```

## Convenciones

- El backend usa Express con rutas en `src/routes/`. Registrar rutas nuevas en `src/index.ts`.
- Toda acción sobre expedientes debe llamar `logAction()` de `src/services/audit.ts`.
- PDFs se suben a Supabase Storage bucket `documents` (máx 5MB, solo PDF).
- Para URLs de PDFs, generar signed URLs con duración de 300s (5 min).
- El frontend usa proxy Vite `/api` → `localhost:4000`. No hardcodear URLs del backend.
- Agregar endpoints nuevos en `frontend/src/lib/api.ts`.

## MCP Supabase

El MCP de Supabase está configurado en `.mcp.json`. Disponible en Claude Code con tools:
- `mcp__supabase__execute_sql` — para consultas rápidas
- `mcp__supabase__apply_migration` — para DDL (ALTER TABLE, CREATE TABLE, etc.)
- `mcp__supabase__list_tables` — para explorar el esquema

Para autenticar el MCP: abrir `/mcp` en Claude Code y conectar el servidor `supabase`.
