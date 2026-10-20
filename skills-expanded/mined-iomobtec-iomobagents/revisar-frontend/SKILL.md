---
name: revisar-frontend
description: "Revisa código React e TypeScript quanto a padrões, performance e acessibilidade. Use quando o dev-frontend vai autorrevisar o código antes do PR."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: revisar-frontend

Revisa código React/TypeScript antes de abrir PR: verifica conformidade com guardrails, qualidade de componentes, acessibilidade, gerenciamento de estado, tipagem e cobertura de testes.

**Agente:** dev-frontend  
**Guardrails aplicáveis:** `00-core.md`, `frontend.md`, `testes.md`, `seguranca.md`, `operacional.md`, `processo.md`

---

## Quando usar

- Antes de abrir PR com código frontend
- Ao revisar PR de outro desenvolvedor frontend
- Quando `auditar-cobertura` indica lacunas críticas

---

## Processo de execução

### Passo 1 — Verificar tipagem TypeScript

```typescript
// ⛔ `any` explícito ou implícito — frontend.md §4
const handleChange = (e: any) => { ... };
const data: any = await fetchData();

// ✅ tipos derivados do contrato do BFF
interface UserResponse { id: string; name: string; email: string; }
const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => { ... };
```

Checklist de tipagem:
- [ ] Sem `any` em props, retornos de função ou tipos de estado
- [ ] Tipos de props definidos em `interface` nomeada (não inline anônimo)
- [ ] Tipos de response derivados do contrato do BFF — não inventados

---

### Passo 2 — Verificar estrutura de componentes

```typescript
// ⛔ class component — frontend.md §1
class UserCard extends React.Component<Props, State> { ... }

// ⛔ lógica de negócio no componente
function OrderPage({ orderId }: { orderId: string }) {
  const [total, setTotal] = useState(0);
  // Calculando desconto diretamente no componente — lógica de negócio
  const discount = total > 1000 ? total * 0.1 : 0;
  ...
}

// ✅ componente funcional com lógica extraída para hook
function OrderPage({ orderId }: { orderId: string }) {
  const { order, isLoading, error } = useOrder(orderId);
  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message="Não foi possível carregar o pedido." />;
  if (!order) return <EmptyState message="Pedido não encontrado." />;
  return <OrderCard order={order} />;
}
```

Checklist de estrutura:
- [ ] Componente funcional — sem class component
- [ ] Lógica de dados extraída para hook
- [ ] Todos os estados assíncronos tratados: loading, erro, vazio, sucesso
- [ ] Componente não faz `fetch` diretamente — delega para hook/service
- [ ] Sem lógica de negócio no componente — apenas renderização

---

### Passo 3 — Verificar manipulação de DOM

```typescript
// ⛔ manipulação direta de DOM — frontend.md §2
document.getElementById('modal').style.display = 'block';
document.querySelector('.active').classList.remove('active');

// ✅ estado React controla o DOM
const [isModalOpen, setIsModalOpen] = useState(false);
return isModalOpen ? <Modal /> : null;
```

Checklist de DOM:
- [ ] Sem `document.getElementById` / `document.querySelector`
- [ ] Sem mutação direta de `classList` ou `style`
- [ ] `useRef` usado apenas para leitura de valor ou integração com biblioteca de terceiros

---

### Passo 4 — Verificar gerenciamento de estado

Aplicar o modelo de decisão de `organizar-estado`:

```typescript
// ⛔ estado global para dado local — frontend.md §3
const useGlobalModalStore = create(() => ({ isOpen: false }));
// → modal é UI local, usar useState no componente

// ⛔ duplicar server state localmente
const [user, setUser] = useState(null);
useEffect(() => { fetch('/api/user').then(r => r.json()).then(setUser); }, []);
// → usar React Query ou hook de dados

// ⛔ prop drilling além de 2 níveis
<Page user={user}><Section user={user}><Card user={user} />

// ✅ Context ou React Query para dado compartilhado por muitos componentes
```

Checklist de estado:
- [ ] Estado global apenas para dado genuinamente compartilhado entre árvores diferentes
- [ ] Server state gerenciado por React Query ou hook de dados — não duplicado em `useState`
- [ ] Prop drilling não ultrapassa 2 níveis
- [ ] Zustand: um store por domínio, sem lógica de negócio no store

---

### Passo 5 — Verificar acessibilidade

```typescript
// ⛔ elemento interativo não-semântico — frontend.md §5
<div onClick={handleClick}>Clique aqui</div>
<span role="button">Abrir menu</span>

// ⛔ imagem sem alt
<img src={avatarUrl} />

// ⛔ input sem label
<input type="text" placeholder="Digite seu email" />

// ✅ semântica correta
<button type="button" onClick={handleClick}>Clique aqui</button>
<img src={avatarUrl} alt={`Foto de ${name}`} />
<label htmlFor="email">Email</label>
<input id="email" type="email" />
```

Checklist de acessibilidade:
- [ ] Elementos interativos são `<button>` ou `<a>` — sem `<div onClick>`
- [ ] Imagens com `alt` descritivo ou `alt=""` se decorativa
- [ ] Inputs com `<label>` associado via `htmlFor` ou `aria-label`
- [ ] Elementos semânticos: `<article>`, `<section>`, `<nav>`, `<header>`, `<main>`
- [ ] Modais e dialogs com `role="dialog"` e foco gerenciado

---

### Passo 6 — Verificar estilo e layout

```typescript
// ⛔ estilo inline para layout/tema — frontend.md §6
<div style={{ display: 'flex', gap: '16px', color: '#333', padding: '8px' }}>

// ⛔ classe global sem namespace
<div className="container active">

// ✅ CSS Module
import styles from './UserCard.module.css';
<div className={styles.container}>

// ✅ style inline apenas para valor dinâmico computado
<div style={{ width: `${progress}%` }}>
```

Checklist de estilo:
- [ ] Sem `style={{ }}` inline para layout, espaçamento ou cor estática
- [ ] Classes CSS com namespace (CSS Modules, styled-components ou design system)
- [ ] Sem valores de cor ou espaçamento hardcoded fora de tokens

---

### Passo 7 — Verificar chaves em listas

```typescript
// ⛔ índice como key em lista mutável — frontend.md §8
{items.map((item, index) => <Item key={index} item={item} />)}

// ✅ ID estável da entidade
{items.map(item => <Item key={item.id} item={item} />)}
```

---

### Passo 8 — Verificar segurança

```typescript
// ⛔ JWT ou token em localStorage — seguranca.md §2
localStorage.setItem('token', jwtToken);
sessionStorage.setItem('authToken', token);

// ⛔ dado sensível em estado global persistido
const useAuthStore = create(persist(() => ({ cpf: '', token: '' }), { name: 'auth' }));

// ⛔ dangerouslySetInnerHTML sem sanitização — risco de XSS
<div dangerouslySetInnerHTML={{ __html: userProvidedContent }} />
```

Checklist de segurança:
- [ ] Tokens JWT não armazenados em `localStorage` ou `sessionStorage`
- [ ] Dados sensíveis (CPF, cartão, senha) não logados nem persistidos em estado global
- [ ] `dangerouslySetInnerHTML` ausente, ou conteúdo sanitizado antes do uso

---

### Passo 9 — Verificar testes

```typescript
// ⛔ teste sem cobertura de estados assíncronos
it('should render user card', () => {
  render(<UserProfilePage userId="1" />);
  expect(screen.getByText('Ana')).toBeInTheDocument();
  // Não testa loading, erro, vazio
});

// ⛔ mock de fetch global em vez de mock na fronteira
global.fetch = jest.fn().mockResolvedValue({ json: () => ({}) });
// → mockar o service ou hook, não o fetch
```

Checklist de testes:
- [ ] Testes cobrem todos os estados: loading, erro, vazio, sucesso
- [ ] Mock apenas na fronteira (hook ou service) — não `global.fetch` (`testes.md §2`)
- [ ] Queries RTL por role/label/text — `getByTestId` apenas como último recurso
- [ ] Sem dados pessoais reais nas fixtures (`testes.md §7`)

---

## Saída produzida

Lista de itens em formato:

```
✅ Aprovado
⚠️ Ressalva: <descrição do problema e sugestão de correção>
⛔ Bloqueado: <violação de guardrail — referência ao arquivo e seção>
```

Exemplo:
```
✅ Componentes funcionais — sem class components
✅ Estados assíncronos tratados: loading, erro, vazio, sucesso
⚠️ Ressalva: UserCard recebe objeto `user` inteiro mas usa apenas `name` e `email` — desestruturar no pai
⛔ Bloqueado: `localStorage.setItem('token', jwt)` — seguranca.md §2 — usar httpOnly cookie
⛔ Bloqueado: `<div onClick={handleSave}>` — frontend.md §5 — usar `<button type="button">`
```
