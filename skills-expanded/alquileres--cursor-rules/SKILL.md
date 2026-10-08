# 🚀 REGLAS ESPECÍFICAS PARA AI ASSISTANT

## 🎯 OBJETIVO DEL PROYECTO
- **Dominio**: Gestión de alquileres de inquilinos
- **Usuario**: Administrador que gestiona inquilinos, pagos y propiedades
- **Stack**: Elysia + Prisma + React + Eden Treaty (Type-Safe end-to-end)

## 🚫 PROHIBICIONES CRÍTICAS
### Backend
- ❌ **NUNCA** usar Express, NestJS, Fastify
- ❌ **NUNCA** usar TypeORM, MikroORM, Sequelize
- ❌ **NUNCA** usar Joi, Yup, Zod para validación
- ❌ **NUNCA** usar Axios o Fetch nativo
- ❌ **NUNCA** crear implementaciones sin interfaces

### Frontend
- ❌ **NUNCA** usar Axios, Fetch, o librerías HTTP externas
- ❌ **NUNCA** crear carpeta `/src/types/` (usar `shared/types/`)
- ❌ **NUNCA** usar Redux, Zustand, Jotai
- ❌ **NUNCA** usar CSS Modules o styled-components

## ✅ PATRONES OBLIGATORIOS
### Arquitectura
- **Backend**: Routes → Controllers → Services → Repositories → Entities
- **Interfaces**: `I{Nombre}Service`, `I{Nombre}Repository`
- **Entities**: `toDTO()`, `fromPrisma()`, `toPrisma()`
- **Type-Safety**: Eden Treaty para comunicación frontend-backend

### Estructura de Archivos
```
server/src/
├── routes/         # Endpoints Elysia
├── controllers/    # Lógica HTTP
├── services/       # Reglas de negocio
├── repositories/   # Acceso a datos
├── entities/       # Modelos de dominio
├── interfaces/     # Contratos TypeScript
└── plugins/        # Middleware Elysia

web/src/
├── contexts/       # ApiContext con Eden Treaty
├── components/     # Componentes React
├── hooks/          # Custom hooks
└── pages/          # Páginas/rutas
```

## 🔄 VERIFICACIÓN OBLIGATORIA DESPUÉS DE CADA CAMBIO

**ANTES de continuar programando, ejecutar:**
```bash
# Backend
cd server && npm run type-check && npm run build

# Frontend
cd web && npm run type-check && npm run build
```

## 📋 CHECKLIST ANTES DE CADA CAMBIO
### Backend
- [ ] `export type App = typeof app` en `src/index.ts`
- [ ] Interfaces existen: `grep -r "interface I.*Service"`
- [ ] Entities tienen métodos: `toDTO()`, `fromPrisma()`, `toPrisma()`
- [ ] **Controllers usan contexto de Elysia correctamente** (NO `userId` como parámetro directo)
- [ ] **Auth plugin expone `getCurrentUserId()` en contexto**
- [ ] **✅ `npm run type-check` pasa sin errores**
- [ ] **✅ `npm run build` compila exitosamente**
- [ ] `npm run dev:full` funciona (dev + type-check)

### Frontend
- [ ] `treaty<App>` import correcto
- [ ] `import type { App }` desde server
- [ ] NO carpeta `src/types/`
- [ ] **✅ `npm run type-check` pasa sin errores**
- [ ] **✅ `npm run build` compila exitosamente**
- [ ] `npm run dev:full` funciona

## 🚨 ERRORES COMUNES A EVITAR

### Controllers en Elysia
❌ **MALO:** `({ userId }: { userId: number }) =>`
✅ **BUENO:** `({ getCurrentUserId }: { getCurrentUserId: () => number }) =>`

### Auth Context
❌ **MALO:** Esperar `userId` directamente en parámetros
✅ **BUENO:** Usar `getCurrentUserId()` del auth plugin

### Tipos de Contexto
❌ **MALO:** Definir tipos manuales que no coinciden con Elysia
✅ **BUENO:** Dejar que Elysia infiera los tipos automáticamente

## 🔄 WORKFLOW RECOMENDADO
1. **Planificar** la funcionalidad según dominio (inquilinos, pagos, propiedades)
2. **Crear interfaces** primero (contracts)
3. **Implementar entities** con métodos DTO
4. **Crear repositories** con Prisma
5. **Implementar services** con lógica de negocio
6. **Crear controllers** para endpoints
7. **Definir routes** en Elysia
8. **Probar** con `npm run dev:full`
9. **Commit** siguiendo conventional commits

## ⚠️ SI VIOLAS ESTAS REGLAS
**DETENTE INMEDIATAMENTE Y PREGUNTA**

Este estándar es estricto porque garantiza type-safety end-to-end y mantenibilidad a largo plazo.
