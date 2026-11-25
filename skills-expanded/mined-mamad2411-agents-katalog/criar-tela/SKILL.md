---
name: criar-tela
description: "Cria uma tela (Screen) com layout, hook de dados, todos os estados e testes. Use quando o dev-mobile vai adicionar uma tela ao app."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: criar-tela

Cria uma **tela (Screen) React Native** no Expo Router: layout, hook de dados via TanStack Query, todos os estados (loading, erro, vazio, sucesso), acessibilidade e testes.

**Agente:** dev-mobile  
**Guardrails aplicáveis:** `mobile.md §1`, `mobile.md §2`, `mobile.md §4`, `mobile.md §5`, `mobile.md §6`, `mobile.md §9`

---

## Quando usar

- Para criar uma nova tela do app (equivale a uma `page` no Expo Router)
- Para telas que buscam dados do BFF e compõem componentes apresentacionais
- Para substituir um componente que cresceu e se tornou uma tela

---

## Classificação de telas

Identificar o tipo antes de implementar:

| Tipo | Responsabilidade | Exemplo |
|---|---|---|
| **Lista** | Busca coleção do BFF, renderiza com FlashList | `OrdersScreen`, `ProductListScreen` |
| **Detalhe** | Busca item único por ID do BFF | `OrderDetailScreen`, `ProductDetailScreen` |
| **Formulário** | Captura entrada do usuário e submete via mutation | `CreateOrderScreen`, `EditProfileScreen` |
| **Informativa** | Composição estática ou de dados locais | `SettingsScreen`, `AboutScreen` |

---

## Pré-requisitos

- Contrato do BFF definido (shape de request/response)
- Especificação do dev-ui-ux disponível (`plans/dev-mobile/<ticket>-<tela>-spec.md`)
- Cenários Gherkin escritos pelo dev-qa

---

## Processo de execução

### Passo 1 — Identificar o tipo e os dados necessários

```
Tipo: Lista | Detalhe | Formulário | Informativa
Endpoint do BFF: GET /orders
Response shape: Order[]
Parâmetros de rota: nenhum | { id: string }
Estado necessário: TanStack Query (dados do servidor)
```

### Passo 2 — Criar o arquivo de rota

```tsx
// app/(tabs)/orders/index.tsx  ← lista
// app/(tabs)/orders/[id].tsx   ← detalhe dinâmico
// app/(tabs)/orders/create.tsx ← formulário
```

### Passo 3 — Implementar tela de lista

```tsx
// app/(tabs)/orders/index.tsx
import { View, Text, StyleSheet } from 'react-native';
import { FlashList } from '@shopify/flash-list';
import { useOrders } from '@/hooks/useOrders';
import { OrderRow } from '@/components/OrderRow';
import { LoadingScreen } from '@/components/LoadingScreen';
import { ErrorScreen } from '@/components/ErrorScreen';
import { EmptyState } from '@/components/EmptyState';

export default function OrdersScreen() {
  const { data: orders, isLoading, error, refetch, isRefetching } = useOrders();

  if (isLoading) {
    return <LoadingScreen accessibilityLabel="Carregando pedidos" />;
  }

  if (error) {
    return (
      <ErrorScreen
        message="Não foi possível carregar os pedidos."
        onRetry={refetch}
      />
    );
  }

  if (!orders?.length) {
    return <EmptyState message="Você ainda não tem pedidos." />;
  }

  return (
    <View style={styles.container} accessibilityRole="main">
      <FlashList
        data={orders}
        renderItem={({ item }) => <OrderRow order={item} />}
        keyExtractor={(item) => item.id}
        estimatedItemSize={72}                          // mobile.md §6
        onRefresh={refetch}
        refreshing={isRefetching}
        contentContainerStyle={styles.listContent}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff' },
  listContent: { paddingVertical: 8 },
});
```

### Passo 4 — Implementar tela de detalhe

```tsx
// app/(tabs)/orders/[id].tsx
import { View, ScrollView, Text, StyleSheet } from 'react-native';
import { useLocalSearchParams, Stack } from 'expo-router';
import { useOrder } from '@/hooks/useOrder';
import { LoadingScreen } from '@/components/LoadingScreen';
import { ErrorScreen } from '@/components/ErrorScreen';

export default function OrderDetailScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const { data: order, isLoading, error, refetch } = useOrder(id);

  if (isLoading) return <LoadingScreen accessibilityLabel="Carregando detalhes do pedido" />;
  if (error) return <ErrorScreen message="Não foi possível carregar o pedido." onRetry={refetch} />;
  if (!order) return <ErrorScreen message="Pedido não encontrado." />;

  return (
    <>
      <Stack.Screen options={{ title: `Pedido ${order.number}` }} />
      <ScrollView
        style={styles.container}
        contentContainerStyle={styles.content}
        accessibilityRole="main"
      >
        {/* Compor com componentes apresentacionais */}
        <OrderHeader order={order} />
        <OrderItemsList items={order.items} />
        <OrderSummary order={order} />
      </ScrollView>
    </>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff' },
  content: { padding: 16 },
});
```

### Passo 5 — Implementar tela de formulário

```tsx
// app/(tabs)/orders/create.tsx
import { View, ScrollView, StyleSheet } from 'react-native';
import { router } from 'expo-router';
import { useCreateOrder } from '@/hooks/useOrders';
import { CreateOrderForm } from '@/components/CreateOrderForm';
import type { CreateOrderDto } from '@/types/api';

export default function CreateOrderScreen() {
  const { mutate: createOrder, isPending, error } = useCreateOrder();

  function handleSubmit(data: CreateOrderDto) {
    createOrder(data, {
      onSuccess: (order) => {
        router.replace(`/(tabs)/orders/${order.id}`);
      },
    });
  }

  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={styles.content}
      keyboardShouldPersistTaps="handled"     // evita fechar teclado ao tocar fora do input
      accessibilityRole="main"
    >
      <CreateOrderForm
        onSubmit={handleSubmit}
        isLoading={isPending}
        error={error?.message}
      />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff' },
  content: { padding: 16, paddingBottom: 40 },
});
```

### Passo 6 — Tratar todos os estados

Todo tela que depende de dados assíncronos deve tratar:

| Estado | O que renderizar |
|---|---|
| `isLoading` | `<LoadingScreen>` com `accessibilityLabel` descritivo |
| `error` | `<ErrorScreen>` com mensagem + botão de retry |
| Dados vazios | `<EmptyState>` com orientação ao usuário |
| Sucesso | Conteúdo principal da tela |

**Nunca** deixar tela em branco ou com `undefined` não tratado.

### Passo 7 — Garantir acessibilidade da tela

```tsx
// Container principal com role semântico
<View accessibilityRole="main">

// Título da tela acessível via Stack.Screen options
<Stack.Screen options={{ title: 'Meus Pedidos' }} />

// Loading com label descritivo
<ActivityIndicator accessibilityLabel="Carregando, aguarde" />

// Botões de ação com label
<TouchableOpacity
  accessibilityLabel="Criar novo pedido"
  accessibilityRole="button"
>
```

### Passo 8 — Escrever testes

Após implementar a tela, usar a skill `gerar-teste-componente-nativo` para escrever os testes:

```typescript
// src/__tests__/screens/OrdersScreen.test.tsx
import { render, screen, waitFor } from '@testing-library/react-native';
import { createWrapper } from '@/utils/testUtils';
import OrdersScreen from '@/app/(tabs)/orders/index';

// Mock do hook que chama o BFF (fronteira HTTP — não mockar abaixo disso)
jest.mock('@/hooks/useOrders');

describe('OrdersScreen', () => {
  it('exibe loading enquanto busca pedidos', () => {
    (useOrders as jest.Mock).mockReturnValue({ isLoading: true });
    render(<OrdersScreen />, { wrapper: createWrapper() });
    expect(screen.getByLabelText('Carregando pedidos')).toBeTruthy();
  });

  it('exibe mensagem de erro quando falha', async () => {
    (useOrders as jest.Mock).mockReturnValue({
      isLoading: false,
      error: new Error('Network error'),
    });
    render(<OrdersScreen />, { wrapper: createWrapper() });
    expect(screen.getByText('Não foi possível carregar os pedidos.')).toBeTruthy();
  });

  it('exibe empty state quando não há pedidos', () => {
    (useOrders as jest.Mock).mockReturnValue({ isLoading: false, data: [] });
    render(<OrdersScreen />, { wrapper: createWrapper() });
    expect(screen.getByText('Você ainda não tem pedidos.')).toBeTruthy();
  });

  it('exibe lista de pedidos quando carregado com sucesso', () => {
    (useOrders as jest.Mock).mockReturnValue({
      isLoading: false,
      data: [{ id: '1', number: 'PED-001' }],
    });
    render(<OrdersScreen />, { wrapper: createWrapper() });
    expect(screen.getByText('PED-001')).toBeTruthy();
  });
});
```

---

## Racionalizações bloqueadas

| Racionalização | Rebate |
|---|---|
| "Não preciso tratar o estado de erro, o usuário pode puxar para recarregar" | Pull-to-refresh não é descobrível para usuários de leitores de tela — a mensagem de erro com botão de retry é obrigatória |
| "Vou buscar os dados direto na tela com useEffect + fetch" | Toda busca de dados do servidor usa TanStack Query via hook customizado (`mobile.md §4`); fetch manual duplica lógica de cache, retry e loading |
| "FlashList é complicado, vou usar FlatList mesmo" | FlashList tem API compatível e é obrigatório para listas com mais de 20 itens (`mobile.md §6`); a configuração extra é `estimatedItemSize` apenas |

---

## Checklist de conclusão

- [ ] Arquivo de rota criado no local correto em `app/`
- [ ] Hook de dados via TanStack Query (nunca fetch manual)
- [ ] Estado de loading com `accessibilityLabel` descritivo
- [ ] Estado de erro com mensagem e botão de retry
- [ ] Estado vazio com `EmptyState` orientativo
- [ ] Estado de sucesso com conteúdo principal
- [ ] `FlashList` com `keyExtractor` e `estimatedItemSize` em listas
- [ ] `accessibilityRole="main"` no container principal
- [ ] Sem `any` em TypeScript
- [ ] Testes escritos cobrindo os 4 estados
