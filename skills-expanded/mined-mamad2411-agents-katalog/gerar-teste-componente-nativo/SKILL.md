---
name: gerar-teste-componente-nativo
description: "Escreve testes com Jest e React Native Testing Library para componentes, telas e hooks. Use quando o dev-mobile precisa cobrir código mobile com testes."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: gerar-teste-componente-nativo

Escreve **testes de componente e tela React Native** com Jest e React Native Testing Library (RNTL): render, interações do usuário, estados assíncronos e verificação de acessibilidade.

**Agente:** dev-mobile  
**Guardrails aplicáveis:** `testes.md`, `mobile.md §9`

---

## Quando usar

- Após criar um componente nativo com `criar-componente-nativo`
- Após criar uma tela com `criar-tela`
- Após criar um hook com `criar-hook-mobile`
- Para aumentar cobertura de testes em código existente

---

## Princípios de teste mobile (RNTL)

1. **Testar comportamento, não implementação** — o que o usuário vê/faz, não como o código está escrito
2. **Seletores de acessibilidade** — prioridade: `getByRole`, `getByLabelText`, `getByText`, `getByTestId` (último recurso)
3. **Mock na fronteira HTTP** — mockar o hook que chama o BFF, nunca o `fetch` ou `axios` diretamente
4. **Testes independentes** — cada teste deve funcionar isoladamente, sem depender de outro
5. **Cobrir os 4 estados** — loading, erro, vazio, sucesso

---

## Processo de execução

### Passo 1 — Criar o arquivo de teste

```
src/components/<ComponentName>/<ComponentName>.test.tsx
src/__tests__/screens/<ScreenName>.test.tsx
src/__tests__/hooks/use<HookName>.test.ts
```

### Passo 2 — Configurar utilitários de teste

```typescript
// src/utils/testUtils.tsx — criar uma vez, reutilizar em todos os testes
import React from 'react';
import { render, RenderOptions } from '@testing-library/react-native';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: { retry: false, gcTime: 0 },
      mutations: { retry: false },
    },
  });
}

interface WrapperProps {
  children: React.ReactNode;
}

export function createWrapper() {
  const queryClient = createTestQueryClient();
  return function Wrapper({ children }: WrapperProps) {
    return (
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    );
  };
}

export function renderWithProviders(
  ui: React.ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) {
  return render(ui, { wrapper: createWrapper(), ...options });
}
```

### Passo 3 — Testes de componente apresentacional

```typescript
// src/components/Button/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react-native';
import { Button } from './Button';

describe('Button', () => {
  it('renderiza o label corretamente', () => {
    render(<Button label="Confirmar" onPress={() => {}} />);
    expect(screen.getByRole('button', { name: 'Confirmar' })).toBeTruthy();
  });

  it('chama onPress quando tocado', () => {
    const handlePress = jest.fn();
    render(<Button label="Confirmar" onPress={handlePress} />);

    fireEvent.press(screen.getByRole('button', { name: 'Confirmar' }));

    expect(handlePress).toHaveBeenCalledTimes(1);
  });

  it('não chama onPress quando desabilitado', () => {
    const handlePress = jest.fn();
    render(<Button label="Confirmar" onPress={handlePress} isDisabled />);

    fireEvent.press(screen.getByRole('button', { name: 'Confirmar' }));

    expect(handlePress).not.toHaveBeenCalled();
  });

  it('exibe indicador de loading quando isLoading é true', () => {
    render(<Button label="Confirmar" onPress={() => {}} isLoading />);
    expect(screen.getByLabelText('Aguarde')).toBeTruthy();
    expect(screen.queryByText('Confirmar')).toBeNull();
  });
});
```

### Passo 4 — Testes de tela com mock de hook

```typescript
// src/__tests__/screens/OrdersScreen.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react-native';
import { renderWithProviders } from '@/utils/testUtils';

// Mock do hook na fronteira HTTP — não mockar axios ou fetch
jest.mock('@/hooks/useOrders');
import { useOrders } from '@/hooks/useOrders';
import OrdersScreen from '@/app/(tabs)/orders/index';

const mockUseOrders = useOrders as jest.MockedFunction<typeof useOrders>;

describe('OrdersScreen', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('exibe indicador de loading enquanto busca pedidos', () => {
    mockUseOrders.mockReturnValue({
      isLoading: true,
      data: undefined,
      error: null,
      refetch: jest.fn(),
      isRefetching: false,
    } as any);

    renderWithProviders(<OrdersScreen />);

    expect(screen.getByLabelText('Carregando pedidos')).toBeTruthy();
  });

  it('exibe mensagem de erro com botão de retry quando falha', async () => {
    const mockRefetch = jest.fn();
    mockUseOrders.mockReturnValue({
      isLoading: false,
      data: undefined,
      error: new Error('Network error'),
      refetch: mockRefetch,
      isRefetching: false,
    } as any);

    renderWithProviders(<OrdersScreen />);

    expect(screen.getByText('Não foi possível carregar os pedidos.')).toBeTruthy();

    fireEvent.press(screen.getByRole('button', { name: 'Tentar novamente' }));
    expect(mockRefetch).toHaveBeenCalledTimes(1);
  });

  it('exibe empty state quando não há pedidos', () => {
    mockUseOrders.mockReturnValue({
      isLoading: false,
      data: [],
      error: null,
      refetch: jest.fn(),
      isRefetching: false,
    } as any);

    renderWithProviders(<OrdersScreen />);

    expect(screen.getByText('Você ainda não tem pedidos.')).toBeTruthy();
  });

  it('exibe lista de pedidos quando carregado com sucesso', () => {
    mockUseOrders.mockReturnValue({
      isLoading: false,
      data: [
        { id: '1', number: 'PED-001', status: 'active' },
        { id: '2', number: 'PED-002', status: 'pending' },
      ],
      error: null,
      refetch: jest.fn(),
      isRefetching: false,
    } as any);

    renderWithProviders(<OrdersScreen />);

    expect(screen.getByText('PED-001')).toBeTruthy();
    expect(screen.getByText('PED-002')).toBeTruthy();
  });
});
```

### Passo 5 — Testes de formulário

```typescript
// src/__tests__/screens/LoginScreen.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react-native';
import { renderWithProviders } from '@/utils/testUtils';
import LoginScreen from '@/app/(auth)/login';

jest.mock('@/hooks/useAuth');
import { useLogin } from '@/hooks/useAuth';

describe('LoginScreen', () => {
  it('submete o formulário com os dados preenchidos', async () => {
    const mockLogin = jest.fn().mockResolvedValue(undefined);
    (useLogin as jest.Mock).mockReturnValue({ mutate: mockLogin, isPending: false });

    renderWithProviders(<LoginScreen />);

    fireEvent.changeText(screen.getByLabelText('Email'), 'user@email.com');
    fireEvent.changeText(screen.getByLabelText('Senha'), 'senha123');
    fireEvent.press(screen.getByRole('button', { name: 'Entrar' }));

    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith({
        email: 'user@email.com',
        password: 'senha123',
      });
    });
  });

  it('exibe erro de validação para email inválido', async () => {
    renderWithProviders(<LoginScreen />);

    fireEvent.changeText(screen.getByLabelText('Email'), 'email-invalido');
    fireEvent.press(screen.getByRole('button', { name: 'Entrar' }));

    await waitFor(() => {
      expect(screen.getByText('Email inválido')).toBeTruthy();
    });
  });
});
```

### Passo 6 — Testes de hook customizado

```typescript
// src/__tests__/hooks/useOrders.test.ts
import { renderHook, waitFor } from '@testing-library/react-native';
import { createWrapper } from '@/utils/testUtils';

// Mock do cliente HTTP na fronteira do módulo
jest.mock('@/services/api');
import api from '@/services/api';
import { useOrders } from '@/hooks/useOrders';

const mockApi = api as jest.Mocked<typeof api>;

describe('useOrders', () => {
  it('retorna dados do BFF quando a query é bem-sucedida', async () => {
    const mockOrders = [{ id: '1', number: 'PED-001' }];
    mockApi.get.mockResolvedValue({ data: mockOrders });

    const { result } = renderHook(() => useOrders(), { wrapper: createWrapper() });

    expect(result.current.isLoading).toBe(true);

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(result.current.data).toEqual(mockOrders);
  });

  it('retorna erro quando a API falha', async () => {
    mockApi.get.mockRejectedValue(new Error('Network error'));

    const { result } = renderHook(() => useOrders(), { wrapper: createWrapper() });

    await waitFor(() => {
      expect(result.current.error).toBeTruthy();
    });
  });
});
```

### Passo 7 — Testes de acessibilidade

```typescript
it('todos os elementos interativos têm labels acessíveis', () => {
  renderWithProviders(<OrdersScreen />);

  // Verificar que botões têm nome acessível
  const buttons = screen.getAllByRole('button');
  buttons.forEach((button) => {
    expect(button.props.accessibilityLabel || button.props.children).toBeTruthy();
  });
});

it('imagens têm texto alternativo', () => {
  render(<UserCard user={mockUser} />);
  expect(screen.getByRole('image', { name: `Foto de ${mockUser.name}` })).toBeTruthy();
});
```

### Passo 8 — Mocks de módulos nativos

```typescript
// jest.setup.js — mocks globais para módulos que não funcionam em ambiente Node
jest.mock('expo-secure-store', () => ({
  getItemAsync: jest.fn(),
  setItemAsync: jest.fn(),
  deleteItemAsync: jest.fn(),
}));

jest.mock('expo-router', () => ({
  useRouter: () => ({ push: jest.fn(), replace: jest.fn(), back: jest.fn() }),
  useLocalSearchParams: () => ({}),
  useSegments: () => [],
  Link: ({ children }: { children: React.ReactNode }) => children,
  Stack: {
    Screen: () => null,
  },
}));

jest.mock('@react-native-async-storage/async-storage', () =>
  require('@react-native-async-storage/async-storage/jest/async-storage-mock')
);
```

---

## Racionalizações bloqueadas

| Racionalização | Rebate |
|---|---|
| "Vou usar `getByTestId` para todos os seletores, é mais fácil" | `testID` é o último recurso — `getByRole` e `getByLabelText` testam comportamento real e detectam regressões de acessibilidade |
| "Não preciso testar o estado de loading, é óbvio" | Loading com `accessibilityLabel` errado é um bug de acessibilidade real — todos os 4 estados devem ser testados |
| "Vou mockar o `axios` diretamente" | Mockar na fronteira do hook garante que a lógica do hook também é testada; mockar o `axios` torna o teste um teste de implementação |

---

## Checklist de conclusão

- [ ] `testUtils.tsx` com `renderWithProviders` e `createWrapper` disponível
- [ ] Testes dos 4 estados: loading, erro, vazio, sucesso
- [ ] Seletores por role/label (`getByRole`, `getByLabelText`) — `getByTestId` apenas quando necessário
- [ ] Mocks na fronteira do hook (não no axios/fetch)
- [ ] Testes de interação do usuário com `fireEvent.press` e `fireEvent.changeText`
- [ ] Módulos nativos mockados globalmente em `jest.setup.js`
- [ ] `jest.clearAllMocks()` no `beforeEach`
- [ ] Todos os testes passam com `npx jest`
