---
name: mobile-design
description: Pensamento e tomada de decisão em design mobile-first para apps iOS e Android. Interação por toque, padrões de performance, convenções de plataforma. Ensina princípios, não valores fixos. Use ao construir apps React Native, Flutter ou nativos.
allowed-tools: Read, Glob, Grep, Bash
---

# Sistema de Design Mobile

> **Filosofia:** Toque em primeiro lugar. Consciente de bateria. Respeitoso com a plataforma. Capaz offline.
> **Princípio Central:** Mobile NÃO é um desktop pequeno. PENSE em restrições mobile, PERGUNTE sobre a escolha de plataforma.

---

## 🔧 Scripts de Execução

**Execute estes para validação (não leia, apenas execute):**

| Script | Propósito | Uso |
|--------|-----------|-----|
| `scripts/mobile_audit.py` | Auditoria de UX Mobile e Toque | `python scripts/mobile_audit.py <project_path>` |

---

## 🔴 OBRIGATÓRIO: Leia os Arquivos de Referência Antes de Trabalhar!

**⛔ NÃO comece o desenvolvimento até ler os arquivos relevantes:**

### Universal (Sempre Leia)

| Arquivo | Conteúdo | Status |
|---------|----------|--------|
| **[mobile-design-thinking.md](mobile-design-thinking.md)** | **⚠️ ANTI-MEMORIZAÇÃO: Força o pensamento, previne defaults de IA** | **⬜ CRÍTICO PRIMEIRO** |
| **[touch-psychology.md](touch-psychology.md)** | **Lei de Fitts, gestos, haptics, zona de polegar** | **⬜ CRÍTICO** |
| **[mobile-performance.md](mobile-performance.md)** | **Performance RN/Flutter, 60fps, memória** | **⬜ CRÍTICO** |
| **[mobile-backend.md](mobile-backend.md)** | **Notificações push, sincronização offline, API mobile** | **⬜ CRÍTICO** |
| **[mobile-testing.md](mobile-testing.md)** | **Pirâmide de testes, E2E, específico por plataforma** | **⬜ CRÍTICO** |
| **[mobile-debugging.md](mobile-debugging.md)** | **Debugging nativo vs JS, Flipper, Logcat** | **⬜ CRÍTICO** |
| [mobile-navigation.md](mobile-navigation.md) | Tab/Stack/Drawer, deep linking | ⬜ Leia |
| [mobile-typography.md](mobile-typography.md) | Fontes do sistema, Dynamic Type, a11y | ⬜ Leia |
| [mobile-color-system.md](mobile-color-system.md) | OLED, modo escuro, ciente de bateria | ⬜ Leia |
| [decision-trees.md](decision-trees.md) | Seleção de framework/state/storage | ⬜ Leia |

> 🧠 **mobile-design-thinking.md é PRIORIDADE!** Este arquivo garante que a IA pense em vez de usar padrões memorizados.

### Específico por Plataforma (Leia Baseado no Alvo)

| Plataforma | Arquivo | Conteúdo | Quando Ler |
|-----------|---------|----------|-----------|
| **iOS** | [platform-ios.md](platform-ios.md) | Human Interface Guidelines, SF Pro, padrões SwiftUI | Construindo para iPhone/iPad |
| **Android** | [platform-android.md](platform-android.md) | Material Design 3, Roboto, padrões Compose | Construindo para Android |
| **Cross-Platform** | Ambos acima | Pontos de divergência de plataforma | React Native / Flutter |

> 🔴 **Se construir para iOS → Leia platform-ios.md PRIMEIRO!**
> 🔴 **Se construir para Android → Leia platform-android.md PRIMEIRO!**
> 🔴 **Se cross-platform → Leia AMBOS e aplique lógica condicional por plataforma!**

---

## ⚠️ CRÍTICO: PERGUNTE ANTES DE ASSUMIR (OBRIGATÓRIO)

> **PARE! Se a solicitação do usuário for aberta, NÃO padronize para seus favoritos.**

### Você DEVE Perguntar Se Não Especificado:

| Aspecto | Pergunte | Por Quê |
|--------|----------|---------|
| **Plataforma** | "iOS, Android, ou ambos?" | Afeta TODA decisão de design |
| **Framework** | "React Native, Flutter, ou nativo?" | Determina padrões e ferramentas |
| **Navegação** | "Tab bar, drawer, ou baseado em stack?" | Decisão central de UX |
| **State** | "Qual state management? (Zustand/Redux/Riverpod/BLoC?)" | Fundação da arquitetura |
| **Offline** | "Isso precisa funcionar offline?" | Afeta estratégia de dados |
| **Dispositivos alvo** | "Apenas telefone, ou suporte a tablet?" | Complexidade do layout |

### ⛔ ANTI-PADRÕES MOBILE DE IA (LISTA DE PROIBIÇÕES)

> 🚫 **Estas são tendências padrão de IA que DEVEM ser evitadas!**

#### Pecados de Performance

| ❌ NUNCA FAÇA | Por Que Está Errado | ✅ SEMPRE FAÇA |
|---------------|-------------------|-----------------|
| **ScrollView para listas longas** | Renderiza TODOS os itens, memória explode | Use `FlatList` / `FlashList` / `ListView.builder` |
| **Função renderItem inline** | Nova função a cada render, todos itens re-renderizam | `useCallback` + `React.memo` |
| **Sem keyExtractor** | Chaves baseadas em índice causam bugs ao reordenar | ID único e estável dos dados |
| **Pule getItemLayout** | Layout assíncrono = scroll tremido | Forneça quando itens têm altura fixa |
| **setState() em toda parte** | Re-renderizações desnecessárias de widgets | State direcionado, construtores `const` |
| **Native driver: false** | Animações bloqueadas pela thread JS | `useNativeDriver: true` sempre |
| **console.log em produção** | Bloqueia thread JS severamente | Remova antes de release build |
| **Pule React.memo/const** | Cada item re-renderiza em qualquer mudança | Memoize itens de lista SEMPRE |

#### Pecados de Toque/UX

| ❌ NUNCA FAÇA | Por Que Está Errado | ✅ SEMPRE FAÇA |
|---------------|-------------------|-----------------|
| **Alvo de toque < 44px** | Impossível tocar com precisão, frustrante | Mínimo 44pt (iOS) / 48dp (Android) |
| **Espaçamento < 8px entre alvos** | Toques acidentais em vizinhos | Mínimo 8-12px de lacuna |
| **Interações apenas por gesto** | Usuários com deficiência motora excluídos | Sempre forneça alternativa com botão |
| **Sem estado de carregamento** | Usuário acha que app travou | SEMPRE mostre feedback de carregamento |
| **Sem estado de erro** | Usuário travado, sem caminho de recuperação | Mostre erro com opção de retry |
| **Sem tratamento offline** | Crash/bloqueio quando rede se perde | Degradação graciosa, dados em cache |
| **Ignore convenções de plataforma** | Usuários confusos, memória muscular quebrada | iOS parece iOS, Android parece Android |

#### Pecados de Segurança

| ❌ NUNCA FAÇA | Por Que Está Errado | ✅ SEMPRE FAÇA |
|---------------|-------------------|-----------------|
| **Token em AsyncStorage** | Facilmente acessível, roubado em device rooteado | `SecureStore` / `Keychain` / `EncryptedSharedPreferences` |
| **Hardcode de chaves API** | Reverse engineered de APK/IPA | Variáveis de ambiente, armazenamento seguro |
| **Pule SSL pinning** | Ataques MITM possíveis | Pin certificados em produção |
| **Log de dados sensíveis** | Logs podem ser extraídos | Nunca faça log de tokens, senhas, PII |

#### Pecados de Arquitetura

| ❌ NUNCA FAÇA | Por Que Está Errado | ✅ SEMPRE FAÇA |
|---------------|-------------------|-----------------|
| **Lógica de negócio em UI** | Não testável, não mantível | Separação de camada de serviço |
| **State global para tudo** | Re-renderizações desnecessárias, complexidade | State local padrão, eleve quando necessário |
| **Deep linking como afterthought** | Notificações, compartilhamentos quebrados | Planeje deep links desde o dia um |
| **Pule dispose/cleanup** | Vazamentos de memória, listeners zumbis | Limpe subscrições, timers |

---

## 📱 Matriz de Decisão de Plataforma

### Quando Unificar vs Divergir

```
                    UNIFICAR (mesmo em ambas)     DIVERGIR (específico de plataforma)
                    ─────────────────────         ──────────────────────────────────
Lógica de Negócio   ✅ Sempre                     -
Camada de Dados     ✅ Sempre                     -
Funcionalidades     ✅ Sempre                     -
Principais
                    
Navegação           -                             ✅ iOS: swipe de borda, Android: botão voltar
Gestos              -                             ✅ Sensação nativa de plataforma
Ícones              -                             ✅ SF Symbols vs Material Icons
Date Pickers        -                             ✅ Pickers nativos se encaixam bem
Modals/Sheets       -                             ✅ iOS: bottom sheet vs Android: dialog
Tipografia          -                             ✅ SF Pro vs Roboto (ou customizado)
Diálogos de Erro    -                             ✅ Convenções de plataforma para alertas
```

### Referência Rápida: Padrões Padrão de Plataforma

| Elemento | iOS | Android |
|----------|-----|---------|
| **Fonte Primária** | SF Pro / SF Compact | Roboto |
| **Alvo Mín. de Toque** | 44pt × 44pt | 48dp × 48dp |
| **Navegação Voltar** | Swipe de borda esquerda | Botão/gesto de voltar do sistema |
| **Ícones da Tab Inferior** | SF Symbols | Material Symbols |
| **Action Sheet** | UIActionSheet de baixo | Bottom Sheet / Dialog |
| **Progresso** | Spinner | Progresso linear (Material) |
| **Pull to Refresh** | UIRefreshControl nativo | SwipeRefreshLayout |

---

## 🧠 Psicologia de UX Mobile (Referência Rápida)

### Lei de Fitts para Toque

```
Desktop: Cursor é preciso (1px)
Mobile:  Dedo é impreciso (~7mm de área de contato)

→ Alvos de toque DEVEM ser mínimo 44-48px
→ Ações importantes na ZONA DE POLEGAR (inferior da tela)
→ Ações destrutivas LONGE do alcance fácil
```

### Zona de Polegar (Uso com Uma Mão)

```
┌─────────────────────────────┐
│      DIFÍCIL DE ATINGIR      │ ← Navegação, menu, voltar
│        (alongar)            │
├─────────────────────────────┤
│      OK DE ATINGIR          │ ← Ações secundárias
│       (natural)             │
├─────────────────────────────┤
│      FÁCIL DE ATINGIR        │ ← CTAs primários, tab bar
│    (arco natural do polegar) │ ← Interação de conteúdo principal
└─────────────────────────────┘
        [  HOME  ]
```

### Carga Cognitiva Específica de Mobile

| Desktop | Diferença Mobile |
|---------|------------------|
| Múltiplas janelas | UMA tarefa por vez |
| Atalhos de teclado | Gestos de toque |
| Estados hover | SEM hover (toque ou nada) |
| Viewport grande | Espaço limitado, scroll vertical |
| Atenção estável | Constantemente interrompido |

Para mergulho profundo: [touch-psychology.md](touch-psychology.md)

---

## ⚡ Princípios de Performance (Referência Rápida)

### Regras Críticas React Native

```typescript
// ✅ CORRETO: renderItem memoizado + wrapper React.memo
const ListItem = React.memo(({ item }: { item: Item }) => (
  <View style={styles.item}>
    <Text>{item.title}</Text>
  </View>
));

const renderItem = useCallback(
  ({ item }: { item: Item }) => <ListItem item={item} />,
  []
);

// ✅ CORRETO: FlatList com todas otimizações
<FlatList
  data={items}
  renderItem={renderItem}
  keyExtractor={(item) => item.id}  // ID estável, NÃO índice
  getItemLayout={(data, index) => ({
    length: ITEM_HEIGHT,
    offset: ITEM_HEIGHT * index,
    index,
  })}
  removeClippedSubviews={true}
  maxToRenderPerBatch={10}
  windowSize={5}
/>
```

### Regras Críticas Flutter

```dart
// ✅ CORRETO: construtores const evitam rebuilds
class MyWidget extends StatelessWidget {
  const MyWidget({super.key}); // CONST!

  @override
  Widget build(BuildContext context) {
    return const Column( // CONST!
      children: [
        Text('Conteúdo estático'),
        MyConstantWidget(),
      ],
    );
  }
}

// ✅ CORRETO: State direcionado com ValueListenableBuilder
ValueListenableBuilder<int>(
  valueListenable: counter,
  builder: (context, value, child) => Text('$value'),
  child: const ExpensiveWidget(), // Não vai rebuildar!
)
```

### Performance de Animação

```
Acelerado por GPU (RÁPIDO):     Limitado por CPU (LENTO):
├── transform                   ├── width, height
├── opacity                     ├── top, left, right, bottom
└── (use APENAS estes)          ├── margin, padding
                                └── (EVITE animar estes)
```

Para guia completo: [mobile-performance.md](mobile-performance.md)

---

## 📝 CHECKPOINT (OBRIGATÓRIO Antes de Qualquer Trabalho Mobile)

> **Antes de escrever QUALQUER código mobile, você DEVE completar este checkpoint:**

```
🧠 CHECKPOINT:

Plataforma: [ iOS / Android / Ambas ]
Framework:  [ React Native / Flutter / SwiftUI / Kotlin ]
Arquivos Lidos: [ Liste os arquivos de skill que você leu ]

3 Princípios que Vou Aplicar:
1. _______________
2. _______________
3. _______________

Anti-Padrões que Vou Evitar:
1. _______________
2. _______________
```

**Exemplo:**
```
🧠 CHECKPOINT:

Plataforma: iOS + Android (Cross-platform)
Framework:  React Native + Expo
Arquivos Lidos: touch-psychology.md, mobile-performance.md, platform-ios.md, platform-android.md

3 Princípios que Vou Aplicar:
1. FlatList com React.memo + useCallback para todas listas
2. Alvos de toque 48px, zona de polegar para CTAs primários
3. Navegação específica por plataforma (swipe de borda iOS, botão voltar Android)

Anti-Padrões que Vou Evitar:
1. ScrollView para listas → FlatList
2. renderItem inline → Memoizado
3. AsyncStorage para tokens → SecureStore
```

> 🔴 **Não consegue preencher o checkpoint? → VOLTE E LEIA OS ARQUIVOS DE SKILL.**

---

## 🔧 Árvore de Decisão de Framework

```
O QUE VOCÊ ESTÁ CONSTRUINDO?
        │
        ├── Precisa de atualizações OTA + iteração rápida + team web
        │   └── ✅ React Native + Expo
        │
        ├── Precisa de UI pixel-perfect customizado + crítico de performance
        │   └── ✅ Flutter
        │
        ├── Funcionalidades nativas profundas + foco em plataforma única
        │   ├── Apenas iOS → SwiftUI
        │   └── Apenas Android → Kotlin + Jetpack Compose
        │
        ├── Codebase RN existente + novas funcionalidades
        │   └── ✅ React Native (bare workflow)
        │
        └── Enterprise + codebase Flutter existente
            └── ✅ Flutter
```

Para árvores de decisão completas: [decision-trees.md](decision-trees.md)

---

## 📋 Checklist Pré-Desenvolvimento

### Antes de Começar QUALQUER Projeto Mobile

- [ ] **Plataforma confirmada?** (iOS / Android / Ambas)
- [ ] **Framework escolhido?** (RN / Flutter / Nativo)
- [ ] **Padrão de navegação decidido?** (Tabs / Stack / Drawer)
- [ ] **State management selecionado?** (Zustand / Redux / Riverpod / BLoC)
- [ ] **Requisitos offline conhecidos?**
- [ ] **Deep linking planejado desde o dia um?**
- [ ] **Dispositivos alvo definidos?** (Telefone / Tablet / Ambos)

### Antes de Cada Tela

- [ ] **Alvos de toque ≥ 44-48px?**
- [ ] **CTA primária na zona de polegar?**
- [ ] **Estado de carregamento existe?**
- [ ] **Estado de erro com retry existe?**
- [ ] **Tratamento offline considerado?**
- [ ] **Convenções de plataforma seguidas?**

### Antes do Release

- [ ] **console.log removido?**
- [ ] **SecureStore para dados sensíveis?**
- [ ] **SSL pinning habilitado?**
- [ ] **Listas otimizadas (memo, keyExtractor)?**
- [ ] **Limpeza de memória no unmount?**
- [ ] **Testado em devices de baixo desempenho?**
- [ ] **Labels de acessibilidade em todos elementos interativos?**

---

## 📚 Arquivos de Referência

Para orientação mais profunda em áreas específicas:

| Arquivo | Quando Usar |
|---------|-------------|
| [mobile-design-thinking.md](mobile-design-thinking.md) | **PRIMEIRO! Anti-memorização, força pensamento baseado em contexto** |
| [touch-psychology.md](touch-psychology.md) | Entender interação por toque, Lei de Fitts, design de gestos |
| [mobile-performance.md](mobile-performance.md) | Otimizar RN/Flutter, 60fps, memória/bateria |
| [platform-ios.md](platform-ios.md) | Design específico iOS, conformidade HIG |
| [platform-android.md](platform-android.md) | Design específico Android, Material Design 3 |
| [mobile-navigation.md](mobile-navigation.md) | Padrões de navegação, deep linking |
| [mobile-typography.md](mobile-typography.md) | Escala de tipo, fontes do sistema, acessibilidade |
| [mobile-color-system.md](mobile-color-system.md) | Otimização OLED, modo escuro, consciente de bateria |
| [decision-trees.md](decision-trees.md) | Decisões de framework, state, storage |

---

> **Lembre-se:** Usuários mobile são impacientes, constantemente interrompidos, e usam dedos imprecisos em telas pequenas. Design para as PIORES condições: rede ruim, uma mão, sol brilhante, bateria baixa. Se funciona lá, funciona em qualquer lugar.