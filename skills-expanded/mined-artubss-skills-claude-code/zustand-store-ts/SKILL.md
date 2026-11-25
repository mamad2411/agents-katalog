---
name: zustand-store-ts
description: "Crie stores Zustand seguindo padrões estabelecidos com tipos TypeScript adequados e middleware."
risk: unknown
source: community
date_added: "2026-02-27"
---

# Zustand Store

Crie stores Zustand seguindo padrões estabelecidos com tipos TypeScript adequados e middleware.

## Início Rápido

Copie o template de assets/template.ts e substitua os placeholders:
- `{{StoreName}}` → Nome da store em PascalCase (ex: `Project`)
- `{{description}}` → Breve descrição para JSDoc

## Sempre Use subscribeWithSelector

```typescript
import { create } from 'zustand';
import { subscribeWithSelector } from 'zustand/middleware';

export const useMyStore = create<MyStore>()(
  subscribeWithSelector((set, get) => ({
    // state and actions
  }))
);
```

## Separe Estado e Ações

```typescript
export interface MyState {
  items: Item[];
  isLoading: boolean;
}

export interface MyActions {
  addItem: (item: Item) => void;
  loadItems: () => Promise<void>;
}

export type MyStore = MyState & MyActions;
```

## Use Seletores Individuais

```typescript
// Bom - só faz re-render quando `items` muda
const items = useMyStore((state) => state.items);

// Evite - faz re-render em qualquer mudança de estado
const { items, isLoading } = useMyStore();
```

## Se Inscreva Fora do React

```typescript
useMyStore.subscribe(
  (state) => state.selectedId,
  (selectedId) => console.log('Selected:', selectedId)
);
```

## Etapas de Integração

1. Crie a store em `src/frontend/src/store/`
2. Exporte a partir de `src/frontend/src/store/index.ts`
3. Adicione testes em `src/frontend/src/store/*.test.ts`

## Quando Usar
Esta skill é aplicável para executar o workflow ou as ações descritas no resumo.