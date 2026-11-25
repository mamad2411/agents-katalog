---
name: core-components
description: Biblioteca de componentes principais e padrões de sistema de design. Use ao construir UI, utilizar design tokens ou trabalhar com a biblioteca de componentes.
---

# Componentes Principais

## Visão Geral do Sistema de Design

Use componentes da sua biblioteca principal em vez de componentes brutos da plataforma. Isso garante estilo e comportamento consistentes.

## Design Tokens

**NUNCA hard-code valores. Sempre use design tokens.**

### Tokens de Espaçamento

```tsx
// CORRETO - Use tokens
<Box padding="$4" marginBottom="$2" />

// ERRADO - Valores hard-coded
<Box padding={16} marginBottom={8} />
```

| Token | Valor |
|-------|-------|
| `$1` | 4px |
| `$2` | 8px |
| `$3` | 12px |
| `$4` | 16px |
| `$6` | 24px |
| `$8` | 32px |

### Tokens de Cor

```tsx
// CORRETO - Tokens semânticos
<Text color="$textPrimary" />
<Box backgroundColor="$backgroundSecondary" />

// ERRADO - Cores hard-coded
<Text color="#333333" />
<Box backgroundColor="rgb(245, 245, 245)" />
```

| Token Semântico | Use Para |
|-----------------|----------|
| `$textPrimary` | Texto principal |
| `$textSecondary` | Texto de suporte |
| `$textTertiary` | Texto desabilitado/dica |
| `$primary500` | Cor da marca/destaque |
| `$statusError` | Estados de erro |
| `$statusSuccess` | Estados de sucesso |

### Tokens de Tipografia

```tsx
<Text fontSize="$lg" fontWeight="$semibold" />
```

| Token | Tamanho |
|-------|---------|
| `$xs` | 12px |
| `$sm` | 14px |
| `$md` | 16px |
| `$lg` | 18px |
| `$xl` | 20px |
| `$2xl` | 24px |

## Componentes Principais

### Box

Componente base de layout com suporte a tokens:

```tsx
<Box
  padding="$4"
  backgroundColor="$backgroundPrimary"
  borderRadius="$lg"
>
  {children}
</Box>
```

### HStack / VStack

Layouts flex horizontais e verticais:

```tsx
<HStack gap="$3" alignItems="center">
  <Icon name="user" />
  <Text>Username</Text>
</HStack>

<VStack gap="$4" padding="$4">
  <Heading>Title</Heading>
  <Text>Content</Text>
</VStack>
```

### Text

Tipografia com suporte a tokens:

```tsx
<Text
  fontSize="$lg"
  fontWeight="$semibold"
  color="$textPrimary"
>
  Hello World
</Text>
```

### Button

Botão interativo com variantes:

```tsx
<Button
  onPress={handlePress}
  variant="solid"
  size="md"
  isLoading={loading}
  isDisabled={disabled}
>
  Click Me
</Button>
```

| Variante | Use Para |
|----------|----------|
| `solid` | Ações primárias |
| `outline` | Ações secundárias |
| `ghost` | Ações terciárias/sutis |
| `link` | Ações inline |

### Input

Input de formulário com validação:

```tsx
<Input
  value={value}
  onChangeText={setValue}
  placeholder="Enter text"
  error={touched ? errors.field : undefined}
  label="Field Name"
/>
```

### Card

Contêiner de conteúdo:

```tsx
<Card padding="$4" gap="$3">
  <CardHeader>
    <Heading size="sm">Card Title</Heading>
  </CardHeader>
  <CardBody>
    <Text>Card content</Text>
  </CardBody>
</Card>
```

## Padrões de Layout

### Layout de Tela

```tsx
const MyScreen = () => (
  <Screen>
    <ScreenHeader title="Page Title" />
    <ScreenContent padding="$4">
      {/* Content */}
    </ScreenContent>
  </Screen>
);
```

### Layout de Formulário

```tsx
<VStack gap="$4" padding="$4">
  <Input label="Name" {...nameProps} />
  <Input label="Email" {...emailProps} />
  <Button isLoading={loading}>Submit</Button>
</VStack>
```

### Layout de Item de Lista

```tsx
<HStack
  padding="$4"
  gap="$3"
  alignItems="center"
  borderBottomWidth={1}
  borderColor="$borderLight"
>
  <Avatar source={{ uri: imageUrl }} size="md" />
  <VStack flex={1}>
    <Text fontWeight="$semibold">{title}</Text>
    <Text color="$textSecondary" fontSize="$sm">{subtitle}</Text>
  </VStack>
  <Icon name="chevron-right" color="$textTertiary" />
</HStack>
```

## Anti-Padrões

```tsx
// ERRADO - Valores hard-coded
<View style={{ padding: 16, backgroundColor: '#fff' }}>

// CORRETO - Design tokens
<Box padding="$4" backgroundColor="$backgroundPrimary">


// ERRADO - Componentes brutos da plataforma
import { View, Text } from 'react-native';

// CORRETO - Componentes principais
import { Box, Text } from 'components/core';


// ERRADO - Estilos inline
<Text style={{ fontSize: 18, fontWeight: '600' }}>

// CORRETO - Props com tokens
<Text fontSize="$lg" fontWeight="$semibold">
```

## Padrão de Props de Componentes

Ao criar componentes, use props baseadas em tokens:

```tsx
interface CardProps {
  padding?: '$2' | '$4' | '$6';
  variant?: 'elevated' | 'outlined' | 'filled';
  children: React.ReactNode;
}

const Card = ({ padding = '$4', variant = 'elevated', children }: CardProps) => (
  <Box
    padding={padding}
    backgroundColor="$backgroundPrimary"
    borderRadius="$lg"
    {...variantStyles[variant]}
  >
    {children}
  </Box>
);
```

## Integração com Outras Skills

- **react-ui-patterns**: Use componentes principais para estados de UI
- **testing-patterns**: Mock componentes principais em testes
- **storybook**: Documente variantes de componentes