# src/components/ — UI Components

Componentes React compartilhados. Usa shadcn/ui + Tailwind CSS com design mobile-first.

---

## Estrutura

```
components/
├── ui/                 # shadcn/ui primitivos (Button, Card, Dialog, Input...)
├── dashboard/          # Componentes do dashboard financeiro
├── transactions/       # Lista e itens de transações
├── chat/               # Interface de chat IA
├── import/             # Upload e progresso de importação
└── layout/             # Estrutura da app (navbar, bottom-nav, paywall)
```

---

## Design System

### shadcn/ui (`components/ui/`)
- Componentes **copiados** para o projeto (não são dependência gerenciada)
- Adicionar novos: `npx shadcn@latest add <component>`
- Customizar em `components/ui/` — sem modificar o original
- Referência: `components.json` na raiz

### Tailwind — Mobile-First
- **Breakpoints:** `sm:` (640px+), `md:` (768px+), `lg:` (1024px+)
- Escrever estilo base para mobile, adicionar breakpoints para telas maiores
- Tamanho mínimo de toque: `min-h-[44px] min-w-[44px]` (WCAG AA)
- Viewport de referência: 375px (iPhone SE) — menor alvo Android

### Paleta de Cores (a definir formalmente)
```css
/* Tokens definidos em globals.css via shadcn/ui */
--primary: azul/verde financeiro  /* tons de confiança */
--destructive: vermelho           /* gastos, erros */
--muted: cinza suave              /* texto secundário */
```

---

## Componentes por Área

### dashboard/
- `summary-cards.tsx` — Cards: Total Receitas, Total Despesas, Saldo
- `category-chart.tsx` — Gráfico pizza/donut de distribuição por categoria
- `spending-breakdown.tsx` — Cards por categoria com ícone + valor + % + contagem

### transactions/
- `transaction-list.tsx` — Lista com scroll infinito
- `transaction-item.tsx` — Item individual (data, descrição, valor, categoria)
- `category-selector.tsx` — Seletor de categoria para correção (14 opções + custom)

### chat/
- `chat-messages.tsx` — Área de mensagens com scroll automático
- `chat-input.tsx` — Input com envio por botão ou Enter
- `chat-bubble.tsx` — Bolha de mensagem (user vs assistant)

### import/
- `file-dropzone.tsx` — Área de drag-and-drop + click para selecionar OFX/CSV
- `import-progress.tsx` — Feedback visual: uploading → parsing → categorizing → done

### layout/
- `navbar.tsx` — Header com logo + menu (desktop)
- `bottom-nav.tsx` — Navegação inferior mobile (Dashboard, Transações, Import, Chat)
- `paywall-modal.tsx` — Modal de upgrade Premium com benefícios + CTA

---

## Padrões de Componentes

### Props tipadas sempre
```typescript
interface TransactionItemProps {
  transaction: Tables<'transactions'>
  onCategoryChange?: (id: string, category: string) => void
}
```

### Estados obrigatórios para qualquer lista
```typescript
// Sempre tratar os 3 estados:
if (isLoading) return <TransactionListSkeleton />
if (error) return <ErrorState message={error.message} />
if (!data?.length) return <EmptyState cta="Importar primeiro extrato" />
return <TransactionList data={data} />
```

### Formatação brasileira
```typescript
import { formatCurrency, formatDate } from '@/lib/utils/format'
// R$ 1.234,56 e DD/MM/YYYY — nunca formatos americanos
```

### Cores de categorias
Cada categoria tem cor consistente em todos os gráficos:
```typescript
const CATEGORY_COLORS: Record<string, string> = {
  alimentacao: '#16a34a',
  delivery: '#ea580c',
  transporte: '#2563eb',
  // ... definir em constants.ts
}
```

---

## Acessibilidade (WCAG AA)

- Labels em todos os form inputs
- `aria-label` em botões sem texto visível
- Contraste mínimo 4.5:1 para texto normal
- Tamanho mínimo de toque: 44x44px
- Ordem de foco lógica

---

## Regras

- **Sem lógica de negócio** em componentes — chamar `@/lib/` ou receber via props
- **Client Components** apenas quando necessário — marcar `'use client'` explicitamente
- **Skeleton loaders** para todo estado de loading (não usar spinners genéricos)
- **Textos em PT-BR** — labels, mensagens de erro, placeholders, empty states
- **Imports absolutos:** `import { Button } from '@/components/ui/button'`
