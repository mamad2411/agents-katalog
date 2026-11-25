---
name: react-dev
version: 1.0.0
description: Esta skill deve ser usada ao construir componentes React com TypeScript, tipificar hooks, lidar com eventos, ou quando React TypeScript, React 19, Server Components são mencionados. Cobre padrões type-safe para React 18-19 incluindo componentes genéricos, tipificação apropriada de eventos e integração de roteamento (TanStack Router, React Router).
---

# React TypeScript

React type-safe = garantias em tempo de compilação = refatoração confiante.

<when_to_use>

- Construindo componentes React tipificados
- Implementando componentes genéricos
- Tipificando manipuladores de eventos, formulários, refs
- Usando recursos do React 19 (Actions, Server Components, use())
- Integração de roteador (TanStack Router, React Router)
- Custom hooks com tipificação apropriada

NÃO para: TypeScript não-React, React vanilla JS

</when_to_use>

<react_19_changes>

Mudanças em quebra do React 19 exigem migração. Padrões-chave:

**ref como prop** - forwardRef descontinuado:

```typescript
// React 19 - ref como prop regular
type ButtonProps = {
  ref?: React.Ref<HTMLButtonElement>;
} & React.ComponentPropsWithoutRef<'button'>;

function Button({ ref, children, ...props }: ButtonProps) {
  return <button ref={ref} {...props}>{children}</button>;
}
```

**useActionState** - substitui useFormState:

```typescript
import { useActionState } from 'react';

type FormState = { errors?: string[]; success?: boolean };

function Form() {
  const [state, formAction, isPending] = useActionState(submitAction, {});
  return <form action={formAction}>...</form>;
}
```

**use()** - desembrulha promises/context:

```typescript
function UserProfile({ userPromise }: { userPromise: Promise<User> }) {
  const user = use(userPromise); // Suspende até resolver
  return <div>{user.name}</div>;
}
```

Veja [react-19-patterns.md](references/react-19-patterns.md) para useOptimistic, useTransition, checklist de migração.

</react_19_changes>

<component_patterns>

**Props** - estender elementos nativos:

```typescript
type ButtonProps = {
  variant: 'primary' | 'secondary';
} & React.ComponentPropsWithoutRef<'button'>;

function Button({ variant, children, ...props }: ButtonProps) {
  return <button className={variant} {...props}>{children}</button>;
}
```

**Tipificação de Children**:

```typescript
type Props = {
  children: React.ReactNode;          // Qualquer coisa renderizável
  icon: React.ReactElement;           // Um único elemento
  render: (data: T) => React.ReactNode;  // Render prop
};
```

**Discriminated unions** para props de variante:

```typescript
type ButtonProps =
  | { variant: 'link'; href: string }
  | { variant: 'button'; onClick: () => void };

function Button(props: ButtonProps) {
  if (props.variant === 'link') {
    return <a href={props.href}>Link</a>;
  }
  return <button onClick={props.onClick}>Button</button>;
}
```

</component_patterns>

<event_handlers>

Use tipos de evento específicos para tipificação precisa de target:

```typescript
// Mouse
function handleClick(e: React.MouseEvent<HTMLButtonElement>) {
  e.currentTarget.disabled = true;
}

// Form
function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
  e.preventDefault();
  const formData = new FormData(e.currentTarget);
}

// Input
function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
  console.log(e.target.value);
}

// Keyboard
function handleKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
  if (e.key === 'Enter') e.currentTarget.blur();
}
```

Veja [event-handlers.md](references/event-handlers.md) para focus, drag, clipboard, touch, wheel events.

</event_handlers>

<hooks_typing>

**useState** - explícito para unions/null:

```typescript
const [user, setUser] = useState<User | null>(null);
const [status, setStatus] = useState<'idle' | 'loading'>('idle');
```

**useRef** - null para DOM, value para mutável:

```typescript
const inputRef = useRef<HTMLInputElement>(null);  // DOM - usar ?.
const countRef = useRef<number>(0);               // Mutável - acesso direto
```

**useReducer** - discriminated unions para actions:

```typescript
type Action =
  | { type: 'increment' }
  | { type: 'set'; payload: number };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'set': return { ...state, count: action.payload };
    default: return state;
  }
}
```

**Custom hooks** - tuple returns com as const:

```typescript
function useToggle(initial = false) {
  const [value, setValue] = useState(initial);
  const toggle = () => setValue(v => !v);
  return [value, toggle] as const;
}
```

**useContext** - padrão de proteção null:

```typescript
const UserContext = createContext<User | null>(null);

function useUser() {
  const user = useContext(UserContext);
  if (!user) throw new Error('useUser fora de UserProvider');
  return user;
}
```

Veja [hooks.md](references/hooks.md) para useCallback, useMemo, useImperativeHandle, useSyncExternalStore.

</hooks_typing>

<generic_components>

Componentes genéricos inferem tipos das props - sem anotações manuais no site de chamada.

**Padrão** - keyof T para chaves de coluna, render props para renderização customizada:

```typescript
type Column<T> = {
  key: keyof T;
  header: string;
  render?: (value: T[keyof T], item: T) => React.ReactNode;
};

type TableProps<T> = {
  data: T[];
  columns: Column<T>[];
  keyExtractor: (item: T) => string | number;
};

function Table<T>({ data, columns, keyExtractor }: TableProps<T>) {
  return (
    <table>
      <thead>
        <tr>{columns.map(col => <th key={String(col.key)}>{col.header}</th>)}</tr>
      </thead>
      <tbody>
        {data.map(item => (
          <tr key={keyExtractor(item)}>
            {columns.map(col => (
              <td key={String(col.key)}>
                {col.render ? col.render(item[col.key], item) : String(item[col.key])}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

**Genéricos constrangidos** para propriedades obrigatórias:

```typescript
type HasId = { id: string | number };

function List<T extends HasId>({ items }: { items: T[] }) {
  return <ul>{items.map(item => <li key={item.id}>...</li>)}</ul>;
}
```

Veja [generic-components.md](examples/generic-components.md) para padrões Select, List, Modal, FormField.

</generic_components>

<server_components>

Server Components do React 19 executam no servidor e podem ser async.

**Busca assíncrona de dados**:

```typescript
export default async function UserPage({ params }: { params: { id: string } }) {
  const user = await fetchUser(params.id);
  return <div>{user.name}</div>;
}
```

**Server Actions** - 'use server' para mutações:

```typescript
'use server';

export async function updateUser(userId: string, formData: FormData) {
  await db.user.update({ where: { id: userId }, data: { ... } });
  revalidatePath(`/users/${userId}`);
}
```

**Client + Server Action**:

```typescript
'use client';

import { useActionState } from 'react';
import { updateUser } from '@/actions/user';

function UserForm({ userId }: { userId: string }) {
  const [state, formAction, isPending] = useActionState(
    (prev, formData) => updateUser(userId, formData), {}
  );
  return <form action={formAction}>...</form>;
}
```

**use() para handoff de promise**:

```typescript
// Server: passar promise sem await
async function Page() {
  const userPromise = fetchUser('123');
  return <UserProfile userPromise={userPromise} />;
}

// Client: desembrulhar com use()
'use client';
function UserProfile({ userPromise }: { userPromise: Promise<User> }) {
  const user = use(userPromise);
  return <div>{user.name}</div>;
}
```

Veja [server-components.md](examples/server-components.md) para busca paralela, streaming, error boundaries.

</server_components>

<routing>

Tanto TanStack Router quanto React Router v7 fornecem soluções de roteamento type-safe.

**TanStack Router** - Type safety em tempo de compilação com validação Zod:

```typescript
import { createRoute } from '@tanstack/react-router';
import { z } from 'zod';

const userRoute = createRoute({
  path: '/users/$userId',
  component: UserPage,
  loader: async ({ params }) => ({ user: await fetchUser(params.userId) }),
  validateSearch: z.object({
    tab: z.enum(['profile', 'settings']).optional(),
    page: z.number().int().positive().default(1),
  }),
});

function UserPage() {
  const { user } = useLoaderData({ from: userRoute.id });
  const { tab, page } = useSearch({ from: userRoute.id });
  const { userId } = useParams({ from: userRoute.id });
}
```

**React Router v7** - Geração automática de tipos com Framework Mode:

```typescript
import type { Route } from "./+types/user";

export async function loader({ params }: Route.LoaderArgs) {
  return { user: await fetchUser(params.userId) };
}

export default function UserPage({ loaderData }: Route.ComponentProps) {
  const { user } = loaderData; // Tipificado do loader
  return <h1>{user.name}</h1>;
}
```

Veja [tanstack-router.md](references/tanstack-router.md) para padrões TanStack e [react-router.md](references/react-router.md) para padrões React Router.

</routing>

<rules>

SEMPRE:
- Tipos de evento específicos (MouseEvent, ChangeEvent, etc)
- useState explícito para unions/null
- ComponentPropsWithoutRef para extensão de elemento nativo
- Discriminated unions para props de variante
- as const para retornos de tuple
- ref como prop no React 19 (sem forwardRef)
- useActionState para form actions
- Padrões de roteamento type-safe (veja seção routing)

NUNCA:
- any para manipuladores de eventos
- JSX.Element para children (usar ReactNode)
- forwardRef no React 19+
- useFormState (descontinuado)
- Esquecer null handling para DOM refs
- Misturar componentes Server/Client no mesmo arquivo
- Await promises ao passar para use()

</rules>

<references>

- [hooks.md](references/hooks.md) - useState, useRef, useReducer, useContext, custom hooks
- [event-handlers.md](references/event-handlers.md) - todos os tipos de evento, manipuladores genéricos
- [react-19-patterns.md](references/react-19-patterns.md) - useActionState, use(), useOptimistic, migração
- [generic-components.md](examples/generic-components.md) - padrões Table, Select, List, Modal
- [server-components.md](examples/server-components.md) - componentes async, Server Actions, streaming
- [tanstack-router.md](references/tanstack-router.md) - rotas TanStack Router tipificadas, search params, navegação
- [react-router.md](references/react-router.md) - React Router v7 loaders, actions, geração de tipos, formulários

</references>