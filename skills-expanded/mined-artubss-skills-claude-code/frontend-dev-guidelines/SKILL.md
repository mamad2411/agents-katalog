---
name: frontend-dev-guidelines
description: Diretrizes de desenvolvimento frontend para aplicações React/TypeScript. Padrões modernos incluindo Suspense, lazy loading, useSuspenseQuery, organização de arquivos com diretório features, styling MUI v7, TanStack Router, otimização de performance e melhores práticas com TypeScript. Use ao criar componentes, páginas, features, buscar dados, fazer styling, rotting ou trabalhar com código frontend.
---

# Diretrizes de Desenvolvimento Frontend

## Propósito

Guia abrangente para desenvolvimento React moderno, enfatizando busca de dados baseada em Suspense, lazy loading, organização adequada de arquivos e otimização de performance.

## Quando Usar Esta Skill

- Criar novos componentes ou páginas
- Construir novas features
- Buscar dados com TanStack Query
- Configurar routing com TanStack Router
- Fazer styling de componentes com MUI v7
- Otimização de performance
- Organizar código frontend
- Melhores práticas com TypeScript

---

## Quick Start

### Checklist de Novo Componente

Criando um componente? Siga este checklist:

- [ ] Use padrão `React.FC<Props>` com TypeScript
- [ ] Lazy load se componente pesado: `React.lazy(() => import())`
- [ ] Envolver em `<SuspenseLoader>` para estados de carregamento
- [ ] Use `useSuspenseQuery` para busca de dados
- [ ] Aliases de import: `@/`, `~types`, `~components`, `~features`
- [ ] Styles: Inline se <100 linhas, arquivo separado se >100 linhas
- [ ] Use `useCallback` para event handlers passados a filhos
- [ ] Default export no final
- [ ] Sem early returns com spinners de carregamento
- [ ] Use `useMuiSnackbar` para notificações do usuário

### Checklist de Nova Feature

Criando uma feature? Configure esta estrutura:

- [ ] Criar diretório `features/{nome-da-feature}/`
- [ ] Criar subdiretórios: `api/`, `components/`, `hooks/`, `helpers/`, `types/`
- [ ] Criar arquivo de serviço API: `api/{feature}Api.ts`
- [ ] Configurar tipos TypeScript em `types/`
- [ ] Criar rota em `routes/{nome-da-feature}/index.tsx`
- [ ] Lazy load de componentes da feature
- [ ] Usar Suspense boundaries
- [ ] Exportar API pública do feature `index.ts`

---

## Quick Reference de Aliases de Import

| Alias | Resolve Para | Exemplo |
|-------|-------------|---------|
| `@/` | `src/` | `import { apiClient } from '@/lib/apiClient'` |
| `~types` | `src/types` | `import type { User } from '~types/user'` |
| `~components` | `src/components` | `import { SuspenseLoader } from '~components/SuspenseLoader'` |
| `~features` | `src/features` | `import { authApi } from '~features/auth'` |

Definido em: [vite.config.ts](../../vite.config.ts) linhas 180-185

---

## Cheatsheet de Imports Comuns

```typescript
// React & Lazy Loading
import React, { useState, useCallback, useMemo } from 'react';
const Heavy = React.lazy(() => import('./Heavy'));

// MUI Components
import { Box, Paper, Typography, Button, Grid } from '@mui/material';
import type { SxProps, Theme } from '@mui/material';

// TanStack Query (Suspense)
import { useSuspenseQuery, useQueryClient } from '@tanstack/react-query';

// TanStack Router
import { createFileRoute } from '@tanstack/react-router';

// Project Components
import { SuspenseLoader } from '~components/SuspenseLoader';

// Hooks
import { useAuth } from '@/hooks/useAuth';
import { useMuiSnackbar } from '@/hooks/useMuiSnackbar';

// Types
import type { Post } from '~types/post';
```

---

## Topic Guides

### 🎨 Padrões de Componentes

**Componentes React modernos usam:**
- `React.FC<Props>` para type safety
- `React.lazy()` para code splitting
- `SuspenseLoader` para estados de carregamento
- Padrão const nomeado + default export

**Conceitos-chave:**
- Lazy load de componentes pesados (DataGrid, gráficos, editores)
- Sempre envolver componentes lazy em Suspense
- Usar componente SuspenseLoader (com animação fade)
- Estrutura de componente: Props → Hooks → Handlers → Render → Export

**[📖 Guia Completo: resources/component-patterns.md](resources/component-patterns.md)**

---

### 📊 Busca de Dados

**PADRÃO PRIMÁRIO: useSuspenseQuery**
- Use com Suspense boundaries
- Estratégia cache-first (verificar cache do grid antes da API)
- Substitui verificações de `isLoading`
- Type-safe com generics

**Camada de Serviço API:**
- Criar `features/{feature}/api/{feature}Api.ts`
- Usar instância axios `apiClient`
- Métodos centralizados por feature
- Formato de rota: `/form/route` (NÃO `/api/form/route`)

**[📖 Guia Completo: resources/data-fetching.md](resources/data-fetching.md)**

---

### 📁 Organização de Arquivos

**features/ vs components/:**
- `features/`: Domain-specific (posts, comments, auth)
- `components/`: Verdadeiramente reutilizável (SuspenseLoader, CustomAppBar)

**Subdiretórios de Feature:**
```
features/
  my-feature/
    api/          # Camada de serviço API
    components/   # Componentes da feature
    hooks/        # Custom hooks
    helpers/      # Funções utilitárias
    types/        # Tipos TypeScript
```

**[📖 Guia Completo: resources/file-organization.md](resources/file-organization.md)**

---

### 🎨 Styling

**Inline vs Separado:**
- <100 linhas: Inline `const styles: Record<string, SxProps<Theme>>`
- >100 linhas: Arquivo separado `.styles.ts`

**Método Primário:**
- Use prop `sx` para componentes MUI
- Type-safe com `SxProps<Theme>`
- Acesso ao theme: `(theme) => theme.palette.primary.main`

**MUI v7 Grid:**
```typescript
<Grid size={{ xs: 12, md: 6 }}>  // ✅ Sintaxe v7
<Grid xs={12} md={6}>             // ❌ Sintaxe antiga
```

**[📖 Guia Completo: resources/styling-guide.md](resources/styling-guide.md)**

---

### 🛣️ Routing

**TanStack Router - Baseado em Folders:**
- Diretório: `routes/my-route/index.tsx`
- Lazy load de componentes
- Use `createFileRoute`
- Dados de breadcrumb no loader

**Exemplo:**
```typescript
import { createFileRoute } from '@tanstack/react-router';
import { lazy } from 'react';

const MyPage = lazy(() => import('@/features/my-feature/components/MyPage'));

export const Route = createFileRoute('/my-route/')({
    component: MyPage,
    loader: () => ({ crumb: 'My Route' }),
});
```

**[📖 Guia Completo: resources/routing-guide.md](resources/routing-guide.md)**

---

### ⏳ Estados de Carregamento e Erro

**REGRA CRÍTICA: Sem Early Returns**

```typescript
// ❌ NUNCA - Causa layout shift
if (isLoading) {
    return <LoadingSpinner />;
}

// ✅ SEMPRE - Layout consistente
<SuspenseLoader>
    <Content />
</SuspenseLoader>
```

**Por quê:** Previne Cumulative Layout Shift (CLS), melhor UX

**Tratamento de Erros:**
- Use `useMuiSnackbar` para feedback do usuário
- NUNCA `react-toastify`
- Callbacks `onError` do TanStack Query

**[📖 Guia Completo: resources/loading-and-error-states.md](resources/loading-and-error-states.md)**

---

### ⚡ Performance

**Padrões de Otimização:**
- `useMemo`: Computações caras (filter, sort, map)
- `useCallback`: Event handlers passados a filhos
- `React.memo`: Componentes caros
- Debounced search (300-500ms)
- Prevenção de memory leak (cleanup em useEffect)

**[📖 Guia Completo: resources/performance.md](resources/performance.md)**

---

### 📘 TypeScript

**Padrões:**
- Strict mode, sem tipo `any`
- Tipos de retorno explícitos em funções
- Type imports: `import type { User } from '~types/user'`
- Interfaces de props de componentes com JSDoc

**[📖 Guia Completo: resources/typescript-standards.md](resources/typescript-standards.md)**

---

### 🔧 Padrões Comuns

**Tópicos Cobertos:**
- React Hook Form com validação Zod
- Contratos de wrapper do DataGrid
- Padrões de componente Dialog
- Hook `useAuth` para usuário atual
- Padrões de Mutation com invalidação de cache

**[📖 Guia Completo: resources/common-patterns.md](resources/common-patterns.md)**

---

### 📚 Exemplos Completos

**Exemplos de funcionamento completo:**
- Componente moderno com todos os padrões
- Estrutura de feature completa
- Camada de serviço API
- Rota com lazy loading
- Suspense + useSuspenseQuery
- Formulário com validação

**[📖 Guia Completo: resources/complete-examples.md](resources/complete-examples.md)**

---

## Guia de Navegação

| Precisa... | Leia este recurso |
|------------|-------------------|
| Criar um componente | [component-patterns.md](resources/component-patterns.md) |
| Buscar dados | [data-fetching.md](resources/data-fetching.md) |
| Organizar arquivos/pastas | [file-organization.md](resources/file-organization.md) |
| Fazer styling de componentes | [styling-guide.md](resources/styling-guide.md) |
| Configurar routing | [routing-guide.md](resources/routing-guide.md) |
| Tratar carregamento/erros | [loading-and-error-states.md](resources/loading-and-error-states.md) |
| Otimizar performance | [performance.md](resources/performance.md) |
| Tipos TypeScript | [typescript-standards.md](resources/typescript-standards.md) |
| Formulários/Auth/DataGrid | [common-patterns.md](resources/common-patterns.md) |
| Ver exemplos completos | [complete-examples.md](resources/complete-examples.md) |

---

## Princípios Fundamentais

1. **Lazy Load Tudo o Que é Pesado**: Routes, DataGrid, gráficos, editores
2. **Suspense para Carregamento**: Use SuspenseLoader, não early returns
3. **useSuspenseQuery**: Padrão primário de busca de dados para código novo
4. **Features são Organizadas**: Subdiretórios api/, components/, hooks/, helpers/
5. **Styles Baseado em Tamanho**: <100 inline, >100 separado
6. **Aliases de Import**: Use @/, ~types, ~components, ~features
7. **Sem Early Returns**: Previne layout shift
8. **useMuiSnackbar**: Para todas as notificações do usuário

---

## Quick Reference: Estrutura de Arquivos

```
src/
  features/
    my-feature/
      api/
        myFeatureApi.ts       # Serviço API
      components/
        MyFeature.tsx         # Componente principal
        SubComponent.tsx      # Componentes relacionados
      hooks/
        useMyFeature.ts       # Custom hooks
        useSuspenseMyFeature.ts  # Hooks Suspense
      helpers/
        myFeatureHelpers.ts   # Utilitários
      types/
        index.ts              # Tipos TypeScript
      index.ts                # Exports públicos

  components/
    SuspenseLoader/
      SuspenseLoader.tsx      # Loader reutilizável
    CustomAppBar/
      CustomAppBar.tsx        # AppBar reutilizável

  routes/
    my-route/
      index.tsx               # Componente de rota
      create/
        index.tsx             # Rota aninhada
```

---

## Template Moderno de Componente (Quick Copy)

```typescript
import React, { useState, useCallback } from 'react';
import { Box, Paper } from '@mui/material';
import { useSuspenseQuery } from '@tanstack/react-query';
import { featureApi } from '../api/featureApi';
import type { FeatureData } from '~types/feature';

interface MyComponentProps {
    id: number;
    onAction?: () => void;
}

export const MyComponent: React.FC<MyComponentProps> = ({ id, onAction }) => {
    const [state, setState] = useState<string>('');

    const { data } = useSuspenseQuery({
        queryKey: ['feature', id],
        queryFn: () => featureApi.getFeature(id),
    });

    const handleAction = useCallback(() => {
        setState('updated');
        onAction?.();
    }, [onAction]);

    return (
        <Box sx={{ p: 2 }}>
            <Paper sx={{ p: 3 }}>
                {/* Conteúdo */}
            </Paper>
        </Box>
    );
};

export default MyComponent;
```

Para exemplos completos, veja [resources/complete-examples.md](resources/complete-examples.md)

---

## Skills Relacionadas

- **error-tracking**: Rastreamento de erros com Sentry (se aplica ao frontend também)
- **backend-dev-guidelines**: Padrões de API backend que o frontend consome

---

**Status da Skill**: Estrutura modular com carregamento progressivo para otimização ideal de gerenciamento de contexto