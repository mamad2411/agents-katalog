---
name: testing-patterns
description: Padrões de testes Jest, funções factory, estratégias de mocking e workflow TDD. Use ao escrever testes unitários, criar test factories ou seguir o ciclo red-green-refactor do TDD.
---

# Padrões de Testes e Utilitários

## Filosofia de Testes

**Desenvolvimento Orientado por Testes (TDD):**
- Escreva o teste FALHANDO primeiro
- Implemente código mínimo para passar
- Refatore após verde
- Nunca escreva código de produção sem um teste falhando

**Testes Orientados por Comportamento:**
- Teste comportamento, não implementação
- Foque em APIs públicas e requisitos de negócio
- Evite testar detalhes de implementação
- Use nomes descritivos que descrevam o comportamento

**Padrão Factory:**
- Crie funções `getMockX(overrides?: Partial<X>)`
- Forneça padrões sensatos
- Permita sobrescrever propriedades específicas
- Mantenha testes DRY e mantíveis

## Utilitários de Teste

### Função Render Customizada

Crie um render customizado que envolve componentes com providers obrigatórios:

```typescript
// src/utils/testUtils.tsx
import { render } from '@testing-library/react-native';
import { ThemeProvider } from './theme';

export const renderWithTheme = (ui: React.ReactElement) => {
  return render(
    <ThemeProvider>{ui}</ThemeProvider>
  );
};
```

**Uso:**
```typescript
import { renderWithTheme } from 'utils/testUtils';
import { screen } from '@testing-library/react-native';

it('should render component', () => {
  renderWithTheme(<MyComponent />);
  expect(screen.getByText('Hello')).toBeTruthy();
});
```

## Padrão Factory

### Factory de Props de Componente

```typescript
import { ComponentProps } from 'react';

const getMockMyComponentProps = (
  overrides?: Partial<ComponentProps<typeof MyComponent>>
) => {
  return {
    title: 'Default Title',
    count: 0,
    onPress: jest.fn(),
    isLoading: false,
    ...overrides,
  };
};

// Uso em testes
it('should render with custom title', () => {
  const props = getMockMyComponentProps({ title: 'Custom Title' });
  renderWithTheme(<MyComponent {...props} />);
  expect(screen.getByText('Custom Title')).toBeTruthy();
});
```

### Factory de Dados

```typescript
interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user';
}

const getMockUser = (overrides?: Partial<User>): User => {
  return {
    id: '123',
    name: 'John Doe',
    email: 'john@example.com',
    role: 'user',
    ...overrides,
  };
};

// Uso
it('should display admin badge for admin users', () => {
  const user = getMockUser({ role: 'admin' });
  renderWithTheme(<UserCard user={user} />);
  expect(screen.getByText('Admin')).toBeTruthy();
});
```

## Padrões de Mocking

### Mocking de Módulos

```typescript
// Mock de módulo inteiro
jest.mock('utils/analytics');

// Mock com função factory
jest.mock('utils/analytics', () => ({
  Analytics: {
    logEvent: jest.fn(),
  },
}));

// Acesse o mock no teste
const mockLogEvent = jest.requireMock('utils/analytics').Analytics.logEvent;
```

### Mocking de Hooks GraphQL

```typescript
jest.mock('./GetItems.generated', () => ({
  useGetItemsQuery: jest.fn(),
}));

const mockUseGetItemsQuery = jest.requireMock(
  './GetItems.generated'
).useGetItemsQuery as jest.Mock;

// No teste
mockUseGetItemsQuery.mockReturnValue({
  data: { items: [] },
  loading: false,
  error: undefined,
});
```

## Estrutura de Testes

```typescript
describe('ComponentName', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Rendering', () => {
    it('should render component with default props', () => {});
    it('should render loading state when loading', () => {});
  });

  describe('User interactions', () => {
    it('should call onPress when button is clicked', async () => {});
  });

  describe('Edge cases', () => {
    it('should handle empty data gracefully', () => {});
  });
});
```

## Padrões de Query

```typescript
// Elemento deve existir
expect(screen.getByText('Hello')).toBeTruthy();

// Elemento não deve existir
expect(screen.queryByText('Goodbye')).toBeNull();

// Elemento aparece assincronamente
await waitFor(() => {
  expect(screen.findByText('Loaded')).toBeTruthy();
});
```

## Padrões de Interação com Usuário

```typescript
import { fireEvent, screen } from '@testing-library/react-native';

it('should submit form on button click', async () => {
  const onSubmit = jest.fn();
  renderWithTheme(<LoginForm onSubmit={onSubmit} />);

  fireEvent.changeText(screen.getByLabelText('Email'), 'user@example.com');
  fireEvent.changeText(screen.getByLabelText('Password'), 'password123');
  fireEvent.press(screen.getByTestId('login-button'));

  await waitFor(() => {
    expect(onSubmit).toHaveBeenCalled();
  });
});
```

## Anti-Padrões a Evitar

### Testar Comportamento do Mock ao Invés de Comportamento Real

```typescript
// Ruim - testando o mock
expect(mockFetchData).toHaveBeenCalled();

// Bom - testando comportamento atual
expect(screen.getByText('John Doe')).toBeTruthy();
```

### Não Usar Factories

```typescript
// Ruim - dados de teste duplicados e inconsistentes
it('test 1', () => {
  const user = { id: '1', name: 'John', email: 'john@test.com', role: 'user' };
});
it('test 2', () => {
  const user = { id: '2', name: 'Jane', email: 'jane@test.com' }; // Role faltando!
});

// Bom - factory reutilizável
const user = getMockUser({ name: 'Custom Name' });
```

## Boas Práticas

1. **Sempre use funções factory** para props e dados
2. **Teste comportamento, não implementação**
3. **Use nomes descritivos para testes**
4. **Organize com describe blocks**
5. **Limpe mocks entre testes**
6. **Mantenha testes focados** - um comportamento por teste

## Executando Testes

```bash
# Executar todos os testes
npm test

# Executar com cobertura
npm run test:coverage

# Executar arquivo específico
npm test ComponentName.test.tsx
```

## Integração com Outras Skills

- **react-ui-patterns**: Teste todos os estados da UI (loading, error, empty, success)
- **systematic-debugging**: Escreva teste que reproduza o bug antes de corrigir