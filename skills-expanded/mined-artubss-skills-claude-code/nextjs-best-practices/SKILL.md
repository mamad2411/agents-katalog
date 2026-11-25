---
name: nextjs-best-practices
description: Princípios do Next.js App Router. Server Components, busca de dados, padrões de roteamento.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Melhores Práticas Next.js

> Princípios para desenvolvimento com Next.js App Router.

---

## 1. Server vs Client Components

### Árvore de Decisão

```
Precisa de...?
│
├── useState, useEffect, event handlers
│   └── Client Component ('use client')
│
├── Busca de dados direta, sem interatividade
│   └── Server Component (padrão)
│
└── Ambos? 
    └── Divida: Server pai + Client filho
```

### Por Padrão

| Tipo | Uso |
|------|-----|
| **Server** | Busca de dados, layout, conteúdo estático |
| **Client** | Formulários, botões, UI interativa |

---

## 2. Padrões de Busca de Dados

### Estratégia de Fetch

| Padrão | Uso |
|--------|-----|
| **Padrão** | Estático (em cache no build) |
| **Revalidate** | ISR (atualização por tempo) |
| **No-store** | Dinâmico (a cada requisição) |

### Fluxo de Dados

| Fonte | Padrão |
|-------|--------|
| Banco de dados | Fetch em Server Component |
| API | fetch com cache |
| Entrada de usuário | Client state + server action |

---

## 3. Princípios de Roteamento

### Convenções de Arquivo

| Arquivo | Propósito |
|---------|-----------|
| `page.tsx` | UI da rota |
| `layout.tsx` | Layout compartilhado |
| `loading.tsx` | Estado de carregamento |
| `error.tsx` | Error boundary |
| `not-found.tsx` | Página 404 |

### Organização de Rotas

| Padrão | Uso |
|--------|-----|
| Route groups `(name)` | Organizar sem afetar URL |
| Parallel routes `@slot` | Múltiplas páginas no mesmo nível |
| Intercepting `(.)` | Overlays de modal |

---

## 4. API Routes

### Route Handlers

| Método | Uso |
|--------|-----|
| GET | Ler dados |
| POST | Criar dados |
| PUT/PATCH | Atualizar dados |
| DELETE | Remover dados |

### Melhores Práticas

- Valide entrada com Zod
- Retorne status codes apropriados
- Trate erros com elegância
- Use Edge runtime quando possível

---

## 5. Princípios de Performance

### Otimização de Imagens

- Use componente next/image
- Configure priority para acima da dobra
- Forneça placeholder blur
- Use sizes responsivos

### Otimização de Bundle

- Imports dinâmicos para componentes pesados
- Code splitting baseado em rotas (automático)
- Analise com bundle analyzer

---

## 6. Metadados

### Estático vs Dinâmico

| Tipo | Uso |
|------|-----|
| Exportação estática | Metadados fixos |
| generateMetadata | Dinâmico por rota |

### Tags Essenciais

- title (50-60 caracteres)
- description (150-160 caracteres)
- Imagens Open Graph
- URL canônica

---

## 7. Estratégia de Cache

### Camadas de Cache

| Camada | Controle |
|--------|----------|
| Request | opções de fetch |
| Data | revalidate/tags |
| Rota completa | config de rota |

### Revalidação

| Método | Uso |
|--------|-----|
| Baseada em tempo | `revalidate: 60` |
| On-demand | `revalidatePath/Tag` |
| Sem cache | `no-store` |

---

## 8. Server Actions

### Casos de Uso

- Submissões de formulário
- Mutações de dados
- Triggers de revalidação

### Melhores Práticas

- Marque com 'use server'
- Valide todas as entradas
- Retorne respostas tipadas
- Trate erros

---

## 9. Anti-Padrões

| ❌ Não faça | ✅ Faça |
|----------|-------|
| 'use client' em tudo | Server por padrão |
| Fetch em client components | Fetch em server |
| Pule loading states | Use loading.tsx |
| Ignore error boundaries | Use error.tsx |
| Bundles client grandes | Imports dinâmicos |

---

## 10. Estrutura de Projeto

```
app/
├── (marketing)/     # Route group
│   └── page.tsx
├── (dashboard)/
│   ├── layout.tsx   # Dashboard layout
│   └── page.tsx
├── api/
│   └── [resource]/
│       └── route.ts
└── components/
    └── ui/
```

---

> **Lembre-se:** Server Components são o padrão por um motivo. Comece por lá e adicione client apenas quando necessário.