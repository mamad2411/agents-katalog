---
name: revisar-mobile
description: "Revisa código React Native antes do PR quanto a performance, acessibilidade, padrões e comportamento cross-platform. Use quando o dev-mobile ou o tech-lead vai revisar um PR mobile."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: revisar-mobile

Revisa código **React Native + Expo** antes de abrir PR: performance, acessibilidade, padrões de navegação, estado, segurança de storage e conformidade com `mobile.md`.

**Agente:** `dev-mobile`, `tech-lead`  
**Guardrails aplicáveis:** `mobile.md`, `testes.md`, `operacional.md`, `processo.md`

---

## Quando usar

- Antes de abrir qualquer PR de código mobile
- Ao revisar código de outro desenvolvedor mobile como par
- Para auditar uma tela ou componente existente antes de reutilizá-lo

---

## Processo de execução

Executar os checklists na ordem abaixo. Cada item reprovado deve ser **corrigido antes de abrir o PR**.

---

### Checklist 1 — Estrutura e padrões de código

- [ ] Todos os componentes são funcionais — sem class components (`mobile.md §1`)
- [ ] Sem `any` em TypeScript — tipos derivados dos contratos do BFF (`mobile.md §9`)
- [ ] Estilos via `StyleSheet.create()` ou NativeWind — sem inline para layout/tema (`mobile.md §2`)
- [ ] Nenhuma chamada HTTP direta ao backend — apenas via hook → BFF (`mobile.md §4`)
- [ ] Props bem tipadas e com convenções corretas (`onPress`, `isLoading`, `hasError`)
- [ ] Componentes com responsabilidade única — tela compõe, componente apresenta

---

### Checklist 2 — Acessibilidade (`mobile.md §5`)

- [ ] Todo elemento interativo (`TouchableOpacity`, `Pressable`, `TextInput`) tem `accessibilityLabel`
- [ ] `accessibilityRole` definido em elementos interativos e informativos relevantes
- [ ] `accessibilityState` definido para estados dinâmicos (`{ disabled: true }`, `{ busy: true }`, `{ selected: true }`)
- [ ] `accessibilityHint` em ações não óbvias
- [ ] Imagens com `alt` via `accessibilityLabel` ou `accessible={false}` se decorativas
- [ ] Nenhum `allowFontScaling={false}` — Dynamic Type obrigatório
- [ ] Área de toque mínima de 44pt (verificar `minHeight` ou `padding`)
- [ ] Estados de loading com `accessibilityLabel` descritivo no `ActivityIndicator`

---

### Checklist 3 — Performance

- [ ] `FlashList` (não `FlatList`) para listas com mais de 20 itens (`mobile.md §6`)
- [ ] `keyExtractor` retorna ID estável da entidade — nunca índice do array
- [ ] `estimatedItemSize` definido no `FlashList`
- [ ] `useCallback` em callbacks passados para listas e componentes filhos que não renderizam com frequência
- [ ] `useMemo` apenas quando o custo computacional é real e mensurável
- [ ] Sem `console.log` deixados em código de produção (além do impacto de performance, vaza dados)
- [ ] Imagens carregadas com tamanho adequado ao dispositivo (sem imagens 4K em thumbnails)
- [ ] `keyboardShouldPersistTaps="handled"` em `ScrollView` com formulários

---

### Checklist 4 — Navegação (`mobile.md §3`)

- [ ] Toda navegação via Expo Router (`router.push`, `<Link>`) — sem configuração manual de `NavigationContainer`
- [ ] Parâmetros de rota tipados com `useLocalSearchParams<{ id: string }>()`
- [ ] `enabled: !!id` em queries que dependem de parâmetro de rota
- [ ] Redirect de autenticação centralizado em `useAuthRedirect` — não disperso nas telas
- [ ] Deep link testado para rotas dinâmicas

---

### Checklist 5 — Estado (`mobile.md §4`, `mobile.md §7`)

- [ ] Dados do servidor em TanStack Query — sem `useEffect` + `fetch` manual
- [ ] Query keys centralizadas em objeto exportado — sem magic strings espalhadas
- [ ] Tokens e credenciais em `expo-secure-store` — nunca em `AsyncStorage` ou `useState`
- [ ] Zustand com seletores granulares — não o store inteiro
- [ ] `initialize()` do AuthStore chamado no RootLayout
- [ ] `refetchOnWindowFocus: false` no QueryClient (mobile não tem foco de janela)

---

### Checklist 6 — Testes

- [ ] Todos os 4 estados cobertos: loading, erro, vazio, sucesso
- [ ] Seletores por `getByRole` / `getByLabelText` — `getByTestId` apenas como último recurso
- [ ] Mocks na fronteira do hook (não no `axios`/`fetch`)
- [ ] `jest.clearAllMocks()` no `beforeEach`
- [ ] `npx jest` passa sem erros ou warnings
- [ ] Cobertura de branches (estados condicionais)

---

### Checklist 7 — Comportamento cross-platform

- [ ] Testado em iOS (Simulator) e Android (Emulator)
- [ ] Diferenças de plataforma explícitas com `Platform.select` ou arquivos `.ios.tsx`/`.android.tsx`
- [ ] Sombras tratadas corretamente: `shadowColor/shadowOffset` (iOS) e `elevation` (Android)
- [ ] Inputs de texto sem comportamento inesperado em um dos sistemas
- [ ] Safe area respeitada com `SafeAreaView` ou `useSafeAreaInsets`

---

### Checklist 8 — Qualidade operacional

- [ ] Branch criada conforme convenção: `feat/<ticket>-<descrição>`
- [ ] Commits convencionais: `feat:`, `fix:`, `refactor:`, `test:`
- [ ] Nenhum arquivo `.env` commitado
- [ ] Nenhum secret, token ou chave hardcoded no código
- [ ] `npx tsc --noEmit` passa sem erros
- [ ] PR com descrição preenchida

---

## Formato de saída da revisão

Ao concluir a revisão, emitir relatório no formato:

```
## Revisão de código mobile — <nome da feature/PR>

**Status:** ✅ Aprovado | ⚠️ Aprovado com ressalvas | ⛔ Reprovado

### Itens aprovados
- [lista dos checklists que passaram]

### Itens a corrigir antes do PR
| # | Arquivo/Componente | Problema | Regra |
|---|---|---|---|
| 1 | OrdersScreen.tsx:42 | FlatList com 50 itens — usar FlashList | mobile.md §6 |
| 2 | useOrders.ts:18 | any no tipo de retorno | mobile.md §9 |

### Sugestões (não bloqueantes)
- [melhorias de legibilidade, performance opcional, etc.]
```

---

## Checklist de conclusão da skill

- [ ] Todos os 8 checklists executados
- [ ] Itens reprovados corrigidos antes de considerar pronto
- [ ] Relatório emitido
- [ ] `npx jest` e `npx tsc --noEmit` passando após correções
