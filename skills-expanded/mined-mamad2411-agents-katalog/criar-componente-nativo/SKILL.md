---
name: criar-componente-nativo
description: "Cria um componente React Native reutilizável com props tipadas, StyleSheet ou NativeWind e acessibilidade. Use quando o dev-mobile vai adicionar um componente à UI mobile."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: criar-componente-nativo

Cria um **componente React Native reutilizável**: props tipadas, StyleSheet ou NativeWind, acessibilidade mobile e testes com RNTL.

**Agente:** dev-mobile  
**Guardrails aplicáveis:** `mobile.md §1`, `mobile.md §2`, `mobile.md §5`, `mobile.md §8`, `mobile.md §9`

---

## Quando usar

- Para criar componente apresentacional reutilizável (botão, card, badge, input, modal)
- Para extrair parte de uma tela que cresceu demais em um componente isolado
- Para criar componente de layout (container, spacer, divider)

---

## Classificação de componentes

Identificar o tipo antes de implementar:

| Tipo | Responsabilidade | Exemplo |
|---|---|---|
| **Apresentacional** | Recebe dados via props, renderiza sem buscar dados | `UserCard`, `OrderRow`, `StatusBadge` |
| **Interativo** | Recebe callbacks, gerencia estado de UI interno | `Button`, `TextInput`, `Checkbox` |
| **Layout** | Estrutura visual reutilizável, sem dados | `Container`, `Spacer`, `Divider`, `Section` |
| **Feedback** | Comunica estado ao usuário | `LoadingScreen`, `ErrorScreen`, `EmptyState`, `Toast` |

---

## Processo de execução

### Passo 1 — Definir a interface de props

```typescript
// Sempre começar pelo contrato público do componente
interface OrderRowProps {
  order: Order;                          // tipo derivado do contrato do BFF
  onPress?: (orderId: string) => void;   // callback opcional — prefixo 'on'
  isSelected?: boolean;                  // booleano — prefixo 'is', 'has', 'should'
  testID?: string;                       // escape hatch para testes
}
```

Convenções de props mobile:
- `onPress` para toque, `onChange` para mudança de valor
- `isLoading`, `isDisabled`, `hasError` para estados booleanos
- `testID` sempre suportado para seletores em testes
- `accessibilityLabel` quando o componente agrega semântica especial

### Passo 2 — Implementar o componente

**Componente apresentacional com StyleSheet:**

```tsx
// src/components/OrderRow/OrderRow.tsx
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import type { Order } from '@/types/api';

interface OrderRowProps {
  order: Order;
  onPress?: (orderId: string) => void;
  testID?: string;
}

export function OrderRow({ order, onPress, testID }: OrderRowProps) {
  return (
    <TouchableOpacity
      style={styles.container}
      onPress={() => onPress?.(order.id)}
      disabled={!onPress}
      accessibilityLabel={`Pedido ${order.number}, status ${order.status}`}
      accessibilityRole="button"
      accessibilityHint={onPress ? 'Toque duas vezes para ver detalhes' : undefined}
      testID={testID ?? `order-row-${order.id}`}
    >
      <View style={styles.info}>
        <Text style={styles.number}>{order.number}</Text>
        <Text style={styles.date}>{formatDate(order.createdAt)}</Text>
      </View>
      <StatusBadge status={order.status} />
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    backgroundColor: '#fff',
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: '#e2e8f0',
  },
  info: { flex: 1 },
  number: { fontSize: 16, fontWeight: '600', color: '#1e293b' },
  date: { fontSize: 14, color: '#64748b', marginTop: 2 },
});
```

**Componente com NativeWind:**

```tsx
import { View, Text, TouchableOpacity } from 'react-native';

export function StatusBadge({ status }: { status: Order['status'] }) {
  const colorClass = {
    pending: 'bg-yellow-100 text-yellow-800',
    active: 'bg-green-100 text-green-800',
    cancelled: 'bg-red-100 text-red-800',
  }[status] ?? 'bg-gray-100 text-gray-800';

  const label = {
    pending: 'Pendente',
    active: 'Ativo',
    cancelled: 'Cancelado',
  }[status] ?? status;

  return (
    <View className={`px-2 py-1 rounded-full ${colorClass}`}>
      <Text className="text-xs font-medium">{label}</Text>
    </View>
  );
}
```

**Componente interativo (Button):**

```tsx
// src/components/Button/Button.tsx
import { TouchableOpacity, Text, ActivityIndicator, StyleSheet } from 'react-native';

interface ButtonProps {
  label: string;
  onPress: () => void;
  variant?: 'primary' | 'secondary' | 'danger';
  isLoading?: boolean;
  isDisabled?: boolean;
  testID?: string;
}

export function Button({
  label,
  onPress,
  variant = 'primary',
  isLoading = false,
  isDisabled = false,
  testID,
}: ButtonProps) {
  return (
    <TouchableOpacity
      style={[styles.base, styles[variant], (isDisabled || isLoading) && styles.disabled]}
      onPress={onPress}
      disabled={isDisabled || isLoading}
      accessibilityLabel={label}
      accessibilityRole="button"
      accessibilityState={{ disabled: isDisabled || isLoading, busy: isLoading }}
      testID={testID}
    >
      {isLoading ? (
        <ActivityIndicator
          color={variant === 'primary' ? '#fff' : '#6366f1'}
          accessibilityLabel="Aguarde"
        />
      ) : (
        <Text style={[styles.label, styles[`${variant}Label`]]}>{label}</Text>
      )}
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  base: {
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: 48,           // target mínimo de toque (mobile.md §5)
  },
  primary: { backgroundColor: '#6366f1' },
  secondary: { backgroundColor: '#fff', borderWidth: 1, borderColor: '#6366f1' },
  danger: { backgroundColor: '#ef4444' },
  disabled: { opacity: 0.5 },
  label: { fontSize: 16, fontWeight: '600' },
  primaryLabel: { color: '#fff' },
  secondaryLabel: { color: '#6366f1' },
  dangerLabel: { color: '#fff' },
});
```

### Passo 3 — Diferenças de plataforma

```tsx
// Diferença simples — Platform.select inline (mobile.md §8)
const shadowStyle = Platform.select({
  ios: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.08,
    shadowRadius: 4,
  },
  android: { elevation: 3 },
});

// Diferença estrutural — arquivos separados
// Header.ios.tsx    — usa BlurView do sistema iOS
// Header.android.tsx — usa View com elevation
```

### Passo 4 — Estrutura de arquivos

```
src/components/<ComponentName>/
├── index.ts                     ← re-export: export { ComponentName } from './ComponentName'
├── <ComponentName>.tsx          ← implementação
└── <ComponentName>.test.tsx     ← testes RNTL
```

Para componente com variações de plataforma:
```
src/components/<ComponentName>/
├── index.ts
├── <ComponentName>.tsx          ← lógica compartilhada
├── <ComponentName>.ios.tsx      ← variação iOS (quando estrutural)
├── <ComponentName>.android.tsx  ← variação Android (quando estrutural)
└── <ComponentName>.test.tsx
```

### Passo 5 — Componentes de feedback (obrigatórios no projeto)

Criar os componentes base de feedback se ainda não existirem:

```tsx
// src/components/LoadingScreen/LoadingScreen.tsx
import { View, ActivityIndicator, StyleSheet } from 'react-native';

interface LoadingScreenProps {
  accessibilityLabel?: string;
}

export function LoadingScreen({ accessibilityLabel = 'Carregando' }: LoadingScreenProps) {
  return (
    <View style={styles.container} accessibilityRole="progressbar">
      <ActivityIndicator size="large" color="#6366f1" accessibilityLabel={accessibilityLabel} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, alignItems: 'center', justifyContent: 'center' },
});
```

```tsx
// src/components/EmptyState/EmptyState.tsx
import { View, Text, StyleSheet } from 'react-native';

interface EmptyStateProps {
  message: string;
  action?: React.ReactNode;
}

export function EmptyState({ message, action }: EmptyStateProps) {
  return (
    <View style={styles.container} accessibilityRole="none">
      <Text style={styles.message}>{message}</Text>
      {action}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, alignItems: 'center', justifyContent: 'center', padding: 24 },
  message: { fontSize: 16, color: '#64748b', textAlign: 'center' },
});
```

---

## Anti-padrões bloqueados

```tsx
// ⛔ elementos não acessíveis para interação
<View onTouchEnd={handlePress}>   // use TouchableOpacity ou Pressable
<Text onPress={handlePress}>      // texto não é elemento interativo

// ⛔ tamanho mínimo de toque abaixo de 44pt
<TouchableOpacity style={{ padding: 4 }}>  // toque muito pequeno para dedos

// ⛔ inline styles para tema/layout fixo
<View style={{ flex: 1, padding: 16, backgroundColor: '#fff' }}>

// ⛔ any em props
interface Props { data: any }
```

---

## Checklist de conclusão

- [ ] Props tipadas sem `any`
- [ ] Componente funcional (sem class component)
- [ ] `accessibilityLabel`, `accessibilityRole` em elementos interativos
- [ ] `accessibilityState` para estados dinâmicos (disabled, loading, selected)
- [ ] Área de toque mínima de 44pt (`minHeight: 44` ou `padding` adequado)
- [ ] Estilos via `StyleSheet.create()` ou NativeWind (sem inline para layout)
- [ ] Diferenças de plataforma explícitas com `Platform.select` ou arquivos separados
- [ ] `testID` suportado para seletores em testes
- [ ] Arquivo `index.ts` com re-export
- [ ] Testes escritos com `gerar-teste-componente-nativo`
