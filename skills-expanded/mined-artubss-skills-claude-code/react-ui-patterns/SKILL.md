---
name: react-ui-patterns
description: Padrões modernos de UI em React para estados de carregamento, tratamento de erros e busca de dados. Use ao construir componentes de UI, lidar com dados assíncronos ou gerenciar estados de UI.
---

# Padrões de UI React

## Princípios Fundamentais

1. **Nunca mostrar UI obsoleta** - Spinners apenas quando realmente carregando
2. **Sempre expor erros** - Usuários devem saber quando algo falha
3. **Atualizações otimistas** - Fazer a UI parecer instantânea
4. **Divulgação progressiva** - Mostrar conteúdo conforme fica disponível
5. **Degradação graciosa** - Dados parciais são melhores que nenhum dado

## Padrões de Estado de Carregamento

### A Regra de Ouro

**Mostrar indicador de carregamento APENAS quando não há dados para exibir.**

```typescript
// CORRETO - Mostrar carregamento apenas quando não há dados
const { data, loading, error } = useGetItemsQuery();

if (error) return <ErrorState error={error} onRetry={refetch} />;
if (loading && !data) return <LoadingState />;
if (!data?.items.length) return <EmptyState />;

return <ItemList items={data.items} />;
```

```typescript
// ERRADO - Mostra spinner mesmo com dados em cache
if (loading) return <LoadingState />; // Pisca ao fazer refetch!
```

### Árvore de Decisão de Estado de Carregamento

```
Há um erro?
  → Sim: Mostrar estado de erro com opção de tentar novamente
  → Não: Continuar

Está carregando E não temos dados?
  → Sim: Mostrar indicador de carregamento (spinner/skeleton)
  → Não: Continuar

Temos dados?
  → Sim, com itens: Mostrar os dados
  → Sim, mas vazio: Mostrar estado vazio
  → Não: Mostrar carregamento (fallback)
```

### Skeleton vs Spinner

| Use Skeleton Quando | Use Spinner Quando |
|-------------------|------------------|
| Forma de conteúdo conhecida | Forma de conteúdo desconhecida |
| Layouts de lista/card | Ações em modal |
| Carregamento inicial da página | Envios de botão |
| Placeholders de conteúdo | Operações inline |

## Padrões de Tratamento de Erros

### A Hierarquia de Tratamento de Erros

```
1. Erro inline (nível de campo) → Erros de validação de formulário
2. Notificação toast → Erros recuperáveis, usuário pode tentar novamente
3. Banner de erro → Erros em nível de página, dados ainda parcialmente usáveis
4. Tela de erro completa → Irrecuperável, precisa de ação do usuário
```

### Sempre Mostrar Erros

**CRÍTICO: Nunca engula erros silenciosamente.**

```typescript
// CORRETO - Erro sempre exposto ao usuário
const [createItem, { loading }] = useCreateItemMutation({
  onCompleted: () => {
    toast.success({ title: 'Item criado' });
  },
  onError: (error) => {
    console.error('createItem falhou:', error);
    toast.error({ title: 'Falha ao criar item' });
  },
});

// ERRADO - Erro silenciosamente capturado, usuário não tem ideia
const [createItem] = useCreateItemMutation({
  onError: (error) => {
    console.error(error); // Usuário não vê nada!
  },
});
```

### Padrão de Componente Estado de Erro

```typescript
interface ErrorStateProps {
  error: Error;
  onRetry?: () => void;
  title?: string;
}

const ErrorState = ({ error, onRetry, title }: ErrorStateProps) => (
  <div className="error-state">
    <Icon name="exclamation-circle" />
    <h3>{title ?? 'Algo deu errado'}</h3>
    <p>{error.message}</p>
    {onRetry && (
      <Button onClick={onRetry}>Tentar Novamente</Button>
    )}
  </div>
);
```

## Padrões de Estado de Botão

### Estado de Carregamento do Botão

```tsx
<Button
  onClick={handleSubmit}
  isLoading={isSubmitting}
  disabled={!isValid || isSubmitting}
>
  Enviar
</Button>
```

### Desabilitar Durante Operações

**CRÍTICO: Sempre desabilitar gatilhos durante operações assíncronos.**

```tsx
// CORRETO - Botão desabilitado enquanto carrega
<Button
  disabled={isSubmitting}
  isLoading={isSubmitting}
  onClick={handleSubmit}
>
  Enviar
</Button>

// ERRADO - Usuário pode clicar múltiplas vezes
<Button onClick={handleSubmit}>
  {isSubmitting ? 'Enviando...' : 'Enviar'}
</Button>
```

## Estados Vazios

### Requisitos de Estado Vazio

Toda lista/coleção DEVE ter um estado vazio:

```tsx
// ERRADO - Sem estado vazio
return <FlatList data={items} />;

// CORRETO - Estado vazio explícito
return (
  <FlatList
    data={items}
    ListEmptyComponent={<EmptyState />}
  />
);
```

### Estados Vazios Contextuais

```tsx
// Busca sem resultados
<EmptyState
  icon="search"
  title="Nenhum resultado encontrado"
  description="Tente termos de busca diferentes"
/>

// Lista sem itens ainda
<EmptyState
  icon="plus-circle"
  title="Nenhum item ainda"
  description="Crie seu primeiro item"
  action={{ label: 'Criar Item', onClick: handleCreate }}
/>
```

## Padrão de Envio de Formulário

```tsx
const MyForm = () => {
  const [submit, { loading }] = useSubmitMutation({
    onCompleted: handleSuccess,
    onError: handleError,
  });

  const handleSubmit = async () => {
    if (!isValid) {
      toast.error({ title: 'Por favor, corrija os erros' });
      return;
    }
    await submit({ variables: { input: values } });
  };

  return (
    <form>
      <Input
        value={values.name}
        onChange={handleChange('name')}
        error={touched.name ? errors.name : undefined}
      />
      <Button
        type="submit"
        onClick={handleSubmit}
        disabled={!isValid || loading}
        isLoading={loading}
      >
        Enviar
      </Button>
    </form>
  );
};
```

## Anti-Padrões

### Estados de Carregamento

```typescript
// ERRADO - Spinner quando dados existem (causa fluxo)
if (loading) return <Spinner />;

// CORRETO - Mostrar carregamento apenas sem dados
if (loading && !data) return <Spinner />;
```

### Tratamento de Erros

```typescript
// ERRADO - Erro engolido
try {
  await mutation();
} catch (e) {
  console.log(e); // Usuário não tem ideia!
}

// CORRETO - Erro exposto
onError: (error) => {
  console.error('operação falhou:', error);
  toast.error({ title: 'Operação falhou' });
}
```

### Estados de Botão

```typescript
// ERRADO - Botão não desabilitado durante envio
<Button onClick={submit}>Enviar</Button>

// CORRETO - Desabilitado e mostra carregamento
<Button onClick={submit} disabled={loading} isLoading={loading}>
  Enviar
</Button>
```

## Checklist

Antes de completar qualquer componente de UI:

**Estados de UI:**
- [ ] Estado de erro tratado e mostrado ao usuário
- [ ] Estado de carregamento mostrado apenas quando não há dados
- [ ] Estado vazio fornecido para coleções
- [ ] Botões desabilitados durante operações assíncronos
- [ ] Botões mostram indicador de carregamento quando apropriado

**Dados e Mutations:**
- [ ] Mutations têm handler onError
- [ ] Todas as ações do usuário têm feedback (toast/visual)

## Integração com Outras Skills

- **graphql-schema**: Use padrões de mutation com tratamento de erro apropriado
- **testing-patterns**: Teste todos os estados de UI (carregamento, erro, vazio, sucesso)
- **formik-patterns**: Aplique padrões de envio de formulário