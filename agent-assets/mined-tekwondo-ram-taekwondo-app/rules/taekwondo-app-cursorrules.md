# Cursor Rules — Taekwondo App

Eres un asistente de IA especializado en **React 19, TypeScript, Vite, Tailwind CSS y PWA development**.

---

## Contexto del Proyecto

**SIEMPRE** lee antes de responder:
- `.procontext/context.md` (arquitectura general, stack, entry points)
- `.procontext/session.md` (estado actual, TODOs, blockers)
- `.procontext/AGENTS.md` (tu rol actual: ARCHITECT, IMPLEMENTER, REVIEWER, etc.)

---

## Reglas de Código

### 1. TypeScript (Strict Mode)
- ❌ **NUNCA** usar `any` types
- ✅ Usar tipos explícitos o inferidos
- ✅ Interfaces para props de componentes
- ✅ Zod schemas para datos externos

### 2. React 19 (Functional Components)
- ✅ Functional components con hooks
- ✅ Use `use()` para async data loading (React 19 feature)
- ✅ PropTypes via TypeScript interfaces (no prop-types library)
- ❌ NO usar class components

### 3. Tailwind CSS 4 (Utility-First)
- ✅ Usar utility classes de Tailwind
- ✅ `clsx()` o `tailwind-merge()` para clases condicionales
- ❌ NO usar inline styles (`style={{}}`) excepto valores dinámicos
- ❌ NO crear CSS custom files (usar Tailwind)

### 4. Imports & Organization
```typescript
// Orden de imports:
// 1. External libraries
import { useState } from 'react'
import { Link } from '@tanstack/react-router'

// 2. Components
import { Button } from '@/components/Button'

// 3. Utils & types
import { cn } from '@/utils/cn'
import type { User } from '@/types/user'

// 4. Assets
import logo from '@/assets/logo.svg'
```

### 5. File Naming
- **Components**: PascalCase (`Button.tsx`, `Header.tsx`)
- **Utils**: camelCase (`formatDate.ts`, `cn.ts`)
- **Types**: PascalCase (`User.ts`, `Exam.ts`)
- **Hooks**: camelCase con `use` prefix (`useAuth.ts`, `useExams.ts`)

### 6. Testing
- ✅ **SIEMPRE** agregar tests Playwright para flows críticos
- ✅ Tests en `tests/` folder
- ✅ Naming: `[feature].spec.ts`

---

## Workflow RPI+ (Sigue SIEMPRE)

### 1. RESEARCH (Read-Only)
```bash
# Antes de escribir código, ANALIZA:
- Lee componentes existentes relacionados
- Revisa .procontext/knowledge/ por decisiones previas
- Grep por patterns similares en el código
```

### 2. PLAN (Design First)
```bash
# Diseña solución y pide aprobación:
- Propón estructura de componentes
- Identifica dependencias
- Estima complejidad
```

### 3. IMPLEMENT (Write Code)
```typescript
// Implementa siguiendo las reglas de código
// TypeScript strict, Tailwind CSS, componentes funcionales
```

### 4. VERIFY (Test & Lint)
```bash
# Antes de PR:
npm run lint        # Oxlint check
npm run format:check # Oxfmt check
npx playwright test  # E2E tests
```

### 5. COMPACT (Document Learnings)
```bash
# Actualiza .procontext/:
- session.md: TODOs completados, nuevos blockers
- decisions/: Si tomaste decisión importante
- knowledge/: Si aprendiste algo del dominio
```

---

## Consulta Decisiones Previas

Si encuentras código que contradice tus convenciones:
- ✅ Consulta `.procontext/planning/adrs/` primero
- ✅ Revisa `.procontext/decisions/` por contexto
- ❌ NO sobrescribas sin entender el rationale

---

## Componentes Específicos del Proyecto

### Hotspots (Modificar con cuidado)
- **src/App.tsx**: Layout principal (10 modificaciones recientes)
- **src/common/Video.tsx**: Componente crítico para videos educativos
- **src/pages/Account.tsx**: Feature de cuenta (en desarrollo activo)

### PWA Specifics
- Service worker configurado (`vite-plugin-pwa`)
- Offline-first strategy (verificar con ARCHITECT)
- Cache strategy en `workbox-window`

---

## Logging de Sesión

Al finalizar tu trabajo, actualiza `.procontext/session.md`:
- ✅ Marca [x] tareas completadas
- 📝 Agrega nuevas tareas descubiertas
- 🚧 Documenta blockers encontrados
- 💡 Nota decisiones tomadas (moverlas a `decisions/` después)

---

## Stack Reference Quick

```typescript
// React 19
import { use, useState, useEffect } from 'react'

// Routing
import { Link, useNavigate } from '@tanstack/react-router'

// State
import { create } from 'zustand'

// Validation
import { z } from 'zod'

// Styling
import { cn } from '@/utils/cn'  // tailwind-merge wrapper
import clsx from 'clsx'

// Icons
import { Menu, X, User } from 'lucide-react'

// Base UI
import { Drawer } from '@base-ui/react/drawer'
import { Select } from '@base-ui/react/select'
```

---

## Preguntas Frecuentes

### "¿Por qué `.procontext/` y no solo README.md?"

**README.md**: Para usuarios/visitantes (qué hace la app, cómo instalar)  
**`.procontext/`**: Para developers/IA (cómo está construida, por qué, estado actual)

### "¿Tengo que usar KDD/SDD?"

**NO obligatorio**. Si solo quieres codear:
- Lee `context.md` (5 min)
- Ignora el resto

KDD/SDD son **herramientas**, no burocracia. Úsalas si ayudan.

### "¿Qué es HCP?"

**HCP (Human-Code-AI Protocol)**: Estándar open source para preservar contexto en proyectos con IA.

- **Sin HCP**: IA olvida decisiones, regenera inconsistente, onboarding 3-7 días
- **Con HCP**: IA tiene memoria, código consistente, onboarding 30 min

**Más info**: https://github.com/haletheia/human-code-ai-protocol

---

**Initialized**: 2026-04-23  
**HCP Version**: 2.0.0  
**License**: AGPL-3.0  
**Maintainer**: Taekwondo App Team
