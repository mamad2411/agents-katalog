---
name: gerar-teste-componente
description: "Escreve testes de componente com React Testing Library. Use quando o dev-frontend precisa cobrir um componente com testes."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: gerar-teste-componente

Escreve **testes de componentes e hooks React** com React Testing Library (RTL): testa comportamento visível ao usuário, estados de UI (loading, erro, vazio, sucesso) e interações, sem testar implementação interna.

**Agente:** dev-frontend  
**Guardrails aplicáveis:** `00-core.md`, `testes.md`, `frontend.md`

---

## Quando usar

- Após criar ou modificar um componente com `criar-componente`
- Após criar ou modificar um hook com `criar-hook`
- Para adicionar cobertura em componente existente sem testes
- Quando `auditar-cobertura` identifica gap em componente de risco alto

---

## Princípio fundamental

**Testar o que o usuário vê e faz — não como o componente é implementado.**

```typescript
// ⛔ testa implementação interna
expect(component.state.isOpen).toBe(true);
expect(instance.handleClick).toHaveBeenCalled();

// ✅ testa comportamento visível
expect(screen.getByRole('dialog')).toBeInTheDocument();
expect(screen.getByText('Item adicionado')).toBeVisible();
```

---

## Processo de execução

### Passo 1 — Configurar setup

```typescript
// src/setupTests.ts (configurado no jest.config.js)
import '@testing-library/jest-dom';
```

```json
// jest.config.js
{
  "setupFilesAfterFramework": ["<rootDir>/src/setupTests.ts"],
  "testEnvironment": "jsdom"
}
```

### Passo 2 — Estrutura base do teste de componente

```typescript
// src/components/UserCard/UserCard.test.tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { UserCard } from './UserCard';

describe('UserCard', () => {
  const defaultProps = {
    name: 'Ana Silva',
    email: 'ana@example.com',
  };

  it('should render user name and email', () => {
    render(<UserCard {...defaultProps} />);

    expect(screen.getByText('Ana Silva')).toBeInTheDocument();
    expect(screen.getByText('ana@example.com')).toBeInTheDocument();
  });

  it('should render avatar when avatarUrl is provided', () => {
    render(<UserCard {...defaultProps} avatarUrl="https://example.com/avatar.png" />);

    expect(screen.getByRole('img', { name: 'Foto de Ana Silva' })).toBeInTheDocument();
  });

  it('should not render avatar when avatarUrl is absent', () => {
    render(<UserCard {...defaultProps} />);

    expect(screen.queryByRole('img')).not.toBeInTheDocument();
  });

  it('should call onEdit when edit button is clicked', async () => {
    const onEdit = jest.fn();
    const user = userEvent.setup();

    render(<UserCard {...defaultProps} onEdit={onEdit} />);

    await user.click(screen.getByRole('button', { name: /editar usuário ana silva/i }));

    expect(onEdit).toHaveBeenCalledTimes(1);
  });

  it('should not render edit button when onEdit is not provided', () => {
    render(<UserCard {...defaultProps} />);

    expect(screen.queryByRole('button')).not.toBeInTheDocument();
  });
});
```

### Passo 3 — Testar componente container (com hook mockado)

Mockar o hook na fronteira — não mockar `fetch` global nem implementação interna:

```typescript
// src/pages/UserProfilePage/UserProfilePage.test.tsx
import { render, screen } from '@testing-library/react';
import { UserProfilePage } from './UserProfilePage';
import { useUser } from '../../hooks/useUser';

// Mock na fronteira do hook — testes.md §2
jest.mock('../../hooks/useUser');
const mockUseUser = useUser as jest.MockedFunction<typeof useUser>;

describe('UserProfilePage', () => {
  it('should render loading state', () => {
    mockUseUser.mockReturnValue({ user: null, isLoading: true, error: null, refetch: jest.fn() });

    render(<UserProfilePage userId="123" />);

    expect(screen.getByLabelText('Carregando perfil do usuário')).toBeInTheDocument();
  });

  it('should render error state', () => {
    mockUseUser.mockReturnValue({ user: null, isLoading: false, error: 'Falha na rede', refetch: jest.fn() });

    render(<UserProfilePage userId="123" />);

    expect(screen.getByText('Não foi possível carregar o perfil.')).toBeInTheDocument();
  });

  it('should render empty state when user is null', () => {
    mockUseUser.mockReturnValue({ user: null, isLoading: false, error: null, refetch: jest.fn() });

    render(<UserProfilePage userId="123" />);

    expect(screen.getByText('Usuário não encontrado.')).toBeInTheDocument();
  });

  it('should render user data on success', () => {
    mockUseUser.mockReturnValue({
      user: { name: 'Carlos Oliveira', email: 'carlos@example.com', avatarUrl: null },
      isLoading: false,
      error: null,
      refetch: jest.fn(),
    });

    render(<UserProfilePage userId="123" />);

    expect(screen.getByText('Carlos Oliveira')).toBeInTheDocument();
    expect(screen.getByText('carlos@example.com')).toBeInTheDocument();
  });
});
```

### Passo 4 — Testar hook customizado com `renderHook`

```typescript
// src/hooks/useUser.test.ts
import { renderHook, waitFor } from '@testing-library/react';
import { useUser } from './useUser';
import * as userService from '../services/user.service';

// Mock no service — fronteira HTTP
jest.mock('../services/user.service');
const mockFetchUser = userService.fetchUser as jest.MockedFunction<typeof userService.fetchUser>;

describe('useUser', () => {
  afterEach(() => jest.clearAllMocks());

  it('should return loading true initially', () => {
    mockFetchUser.mockResolvedValue({ id: '1', name: 'Test', email: 'test@example.com' });

    const { result } = renderHook(() => useUser('1'));

    expect(result.current.isLoading).toBe(true);
    expect(result.current.user).toBeNull();
  });

  it('should return user data on success', async () => {
    const mockUser = { id: '1', name: 'Maria Santos', email: 'maria@example.com' };
    mockFetchUser.mockResolvedValue(mockUser);

    const { result } = renderHook(() => useUser('1'));

    await waitFor(() => expect(result.current.isLoading).toBe(false));

    expect(result.current.user).toEqual(mockUser);
    expect(result.current.error).toBeNull();
  });

  it('should return error message on failure', async () => {
    mockFetchUser.mockRejectedValue(new Error('HTTP 404'));

    const { result } = renderHook(() => useUser('1'));

    await waitFor(() => expect(result.current.isLoading).toBe(false));

    expect(result.current.error).toBe('HTTP 404');
    expect(result.current.user).toBeNull();
  });

  it('should not fetch when userId is empty', () => {
    renderHook(() => useUser(''));

    expect(mockFetchUser).not.toHaveBeenCalled();
  });

  it('should refetch when refetch is called', async () => {
    mockFetchUser.mockResolvedValue({ id: '1', name: 'Test', email: 'test@example.com' });

    const { result } = renderHook(() => useUser('1'));
    await waitFor(() => expect(result.current.isLoading).toBe(false));

    result.current.refetch();

    await waitFor(() => expect(mockFetchUser).toHaveBeenCalledTimes(2));
  });
});
```

### Passo 5 — Testar formulário e interações

```typescript
// src/components/LoginForm/LoginForm.test.tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  it('should show validation error when email is empty on submit', async () => {
    const user = userEvent.setup();
    render(<LoginForm onSubmit={jest.fn()} />);

    await user.click(screen.getByRole('button', { name: /entrar/i }));

    expect(screen.getByText('Email é obrigatório')).toBeInTheDocument();
  });

  it('should call onSubmit with email and password when form is valid', async () => {
    const onSubmit = jest.fn();
    const user = userEvent.setup();
    render(<LoginForm onSubmit={onSubmit} />);

    await user.type(screen.getByLabelText('Email'), 'user@example.com');
    await user.type(screen.getByLabelText('Senha'), 'senha123');
    await user.click(screen.getByRole('button', { name: /entrar/i }));

    expect(onSubmit).toHaveBeenCalledWith({ email: 'user@example.com', password: 'senha123' });
  });

  it('should disable submit button while loading', () => {
    render(<LoginForm onSubmit={jest.fn()} isLoading />);

    expect(screen.getByRole('button', { name: /entrar/i })).toBeDisabled();
  });
});
```

### Passo 6 — Queries preferidas por prioridade (RTL)

Usar a query mais próxima de como o usuário interage (`testes.md §2`):

| Prioridade | Query | Quando usar |
|---|---|---|
| 1 | `getByRole` | Elementos com role ARIA: button, textbox, heading, img |
| 2 | `getByLabelText` | Inputs com label associado |
| 3 | `getByPlaceholderText` | Input sem label (evitar quando possível) |
| 4 | `getByText` | Texto visível estático |
| 5 | `getByDisplayValue` | Valor atual de input/select |
| 6 | `getByAltText` | Imagens com alt |
| 7 | `getByTestId` | Último recurso — preferir as anteriores |

```typescript
// ⛔ testId como primeira opção
screen.getByTestId('submit-button');

// ✅ role — mais próximo do que o usuário vê
screen.getByRole('button', { name: /salvar/i });
```

### Passo 7 — Testar lista e estados dinâmicos

```typescript
it('should render all items in the list', () => {
  const items = [
    { id: '1', name: 'Produto A', price: 99.9 },
    { id: '2', name: 'Produto B', price: 149.9 },
  ];

  render(<ProductList items={items} />);

  expect(screen.getAllByRole('listitem')).toHaveLength(2);
  expect(screen.getByText('Produto A')).toBeInTheDocument();
  expect(screen.getByText('Produto B')).toBeInTheDocument();
});

it('should render empty state when list is empty', () => {
  render(<ProductList items={[]} />);

  expect(screen.getByText('Nenhum produto encontrado.')).toBeInTheDocument();
  expect(screen.queryByRole('listitem')).not.toBeInTheDocument();
});
```

---

## Anti-padrões bloqueados

```typescript
// ⛔ testar estado interno do componente
const { container } = render(<MyComponent />);
expect(container.querySelector('.active')).toBeTruthy(); // frágil — quebra com rename de classe

// ⛔ testar detalhes de implementação do hook
expect(mockSetState).toHaveBeenCalledWith({ isOpen: true }); // não é o que o usuário percebe

// ⛔ dados pessoais reais em fixtures — testes.md §7
const user = { cpf: '123.456.789-00', name: 'João Real da Silva' };

// ✅ dados sintéticos sem relação com pessoas reais
const user = { id: 'user-test-1', name: 'Test User', email: 'test@example.com' };

// ⛔ lógica condicional no teste
if (someCondition) {
  expect(screen.getByText('A')).toBeInTheDocument();
} else {
  expect(screen.getByText('B')).toBeInTheDocument();
}
// Solução: dois testes separados, um por caso
```

---

## Checklist de conclusão

- [ ] Todos os estados tratados: loading, erro, vazio, sucesso
- [ ] Mock apenas na fronteira (hook ou service) — não em `fetch` global
- [ ] Queries por role/label/text — `getByTestId` apenas como último recurso
- [ ] Interações via `userEvent` — não via `fireEvent` diretamente
- [ ] Sem dados pessoais reais nas fixtures (`testes.md §7`)
- [ ] Nome dos testes: `should <comportamento> when <condição>` (`testes.md §1`)
- [ ] `afterEach(() => jest.clearAllMocks())` quando há mocks (`testes.md §3`)
