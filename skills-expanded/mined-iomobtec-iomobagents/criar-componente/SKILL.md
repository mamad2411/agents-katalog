---
name: criar-componente
description: "Cria componentes React reutilizáveis com props, tipagem e stories. Use quando o dev-frontend vai adicionar um componente à UI."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: criar-componente

Cria um **componente React funcional em TypeScript**: definição de props tipadas, implementação com hooks adequados, estilos via design system, estados de loading/erro/vazio e acessibilidade básica.

**Agente:** dev-frontend  
**Guardrails aplicáveis:** `00-core.md`, `frontend.md`, `seguranca.md`

---

## Quando usar

- Para criar novo componente reutilizável (botão, card, form, modal)
- Para criar componente de tela (page-level component que agrega outros)
- Para extrair parte de um componente existente que cresceu demais

---

## Classificação de componentes

Identificar o tipo antes de implementar:

| Tipo | Responsabilidade | Exemplo |
|---|---|---|
| **Apresentacional** | Recebe dados via props, renderiza, não busca dados | `UserCard`, `OrderRow`, `StatusBadge` |
| **Container / Smart** | Busca dados (via hook), gerencia estado, compõe apresentacionais | `UserProfilePage`, `OrderListContainer` |
| **Layout** | Estrutura visual reutilizável, sem lógica de dados | `PageShell`, `SidebarLayout`, `Grid` |
| **Formulário** | Captura entrada do usuário, valida, submete | `LoginForm`, `AddressForm` |

---

## Pré-requisitos

- Contrato de props definido (o que o componente recebe)
- Shape dos dados do BFF (se componente container)
- Componentes do design system disponíveis para uso

---

## Processo de execução

### Passo 1 — Definir a interface de props

Sempre começar pela interface de props — define o contrato público do componente:

```typescript
// Props explícitas e tipadas — nunca `any` (frontend.md §4)
interface UserCardProps {
  userId: string;
  name: string;
  email: string;
  avatarUrl?: string;           // opcional — usar `?`
  onEdit?: () => void;          // callback opcional
  className?: string;           // escape hatch para estilo externo
}
```

Convenções de props:
- Callbacks nomeados com prefixo `on`: `onClick`, `onSubmit`, `onChange`
- Props booleanas com prefixo `is`/`has`/`should`: `isLoading`, `hasError`, `isDisabled`
- Nunca passar objeto inteiro quando só alguns campos são usados — desestruturar no pai

### Passo 2 — Implementar o componente

**Componente apresentacional:**
```typescript
// Sempre componente funcional — nunca class component (frontend.md §1)
export function UserCard({ name, email, avatarUrl, onEdit, className }: UserCardProps) {
  return (
    <article className={`user-card ${className ?? ''}`}>
      {avatarUrl && (
        <img src={avatarUrl} alt={`Foto de ${name}`} className="user-card__avatar" />
      )}
      <div className="user-card__info">
        <h2 className="user-card__name">{name}</h2>
        <p className="user-card__email">{email}</p>
      </div>
      {onEdit && (
        // Elemento interativo com label acessível (frontend.md §5)
        <button
          type="button"
          onClick={onEdit}
          aria-label={`Editar usuário ${name}`}
          className="user-card__edit-btn"
        >
          Editar
        </button>
      )}
    </article>
  );
}
```

**Componente container (busca dados via hook):**
```typescript
export function UserProfilePage({ userId }: { userId: string }) {
  // Lógica de dados no hook — componente só renderiza
  const { user, isLoading, error } = useUser(userId);

  if (isLoading) return <LoadingSpinner aria-label="Carregando perfil do usuário" />;
  if (error) return <ErrorMessage message="Não foi possível carregar o perfil." />;
  if (!user) return <EmptyState message="Usuário não encontrado." />;

  return <UserCard name={user.name} email={user.email} avatarUrl={user.avatarUrl} />;
}
```

### Passo 3 — Tratar todos os estados possíveis

Todo componente que depende de dados assíncronos deve tratar:

| Estado | O que renderizar |
|---|---|
| Loading | Skeleton ou spinner com `aria-label` descritivo |
| Erro | Mensagem de erro com opção de retry quando possível |
| Vazio | Empty state com orientação ao usuário |
| Sucesso | Conteúdo principal |

Nunca deixar estado não tratado — tela em branco não é empty state.

### Passo 4 — Aplicar acessibilidade

Checklist mínimo (`frontend.md §5`):
- [ ] Imagens com `alt` descritivo (ou `alt=""` se decorativa)
- [ ] Botões com texto visível ou `aria-label`
- [ ] Inputs com `<label>` associado via `htmlFor` ou `aria-label`
- [ ] Elementos interativos são `<button>` ou `<a>` — nunca `<div onClick>`
- [ ] Uso de elementos semânticos: `<article>`, `<section>`, `<nav>`, `<header>`, `<main>`

### Passo 5 — Estrutura de arquivos

```
src/components/<ComponentName>/
├── index.ts                        # re-export público
├── <ComponentName>.tsx             # implementação
├── <ComponentName>.test.tsx        # testes com RTL
└── <ComponentName>.module.css      # estilos (se usar CSS Modules)
```

Ou, para componente de tela:
```
src/pages/<PageName>/
├── index.ts
├── <PageName>.tsx
├── <PageName>.test.tsx
└── components/                     # sub-componentes locais desta tela
    └── <SubComponent>/
```

### Passo 6 — Regras de estilo

- Usar CSS Modules, styled-components ou tokens do design system (`frontend.md §6`)
- Sem `style={{ }}` inline para layout, espaçamento ou cor
- Sem classes globais sem namespace

```typescript
// ⛔ style inline para layout
<div style={{ display: 'flex', gap: '16px', color: '#333' }}>

// ✅ CSS Module
import styles from './UserCard.module.css';
<div className={styles.container}>

// ✅ style inline apenas para valor dinâmico computado
<div style={{ width: `${progressPercent}%` }}>  // valor dinâmico — aceitável
```

### Passo 7 — Chaves únicas em listas

`frontend.md §8` — nunca usar índice como key em lista mutável:

```typescript
// ⛔ índice como key
{orders.map((order, index) => <OrderRow key={index} order={order} />)}

// ✅ ID estável da entidade
{orders.map(order => <OrderRow key={order.id} order={order} />)}
```

---

## Checklist de conclusão

- [ ] Props tipadas — sem `any` (`frontend.md §4`)
- [ ] Componente funcional — sem class component (`frontend.md §1`)
- [ ] Todos os estados tratados: loading, erro, vazio, sucesso
- [ ] Elementos interativos acessíveis (button, label, aria) (`frontend.md §5`)
- [ ] Sem manipulação direta de DOM (`frontend.md §2`)
- [ ] Sem `style` inline para layout/tema (`frontend.md §6`)
- [ ] Chaves estáveis em listas (`frontend.md §8`)
- [ ] Testes escritos com `gerar-teste-componente`
