# VRUM Design System — guia para agentes de IA

Aqui fica o que é deste repo. As regras de negócio do VRUM ficam em `docs/negocio.md` no `vrum-api`, no `vrum-partner` e no `vrum-driver`.

## Definição de pronto
1. Implementação completa e fiel ao Figma, quando houver.
2. `typecheck` passou **no workspace tocado** (ex.: `npm run typecheck --workspace=@x-men-evolution/native-ui`), nunca na raiz inteira sem necessidade.
3. Teste escrito quando a mudança justifica (lógica nova, variante, caso de borda).

Build, lint, typecheck e testes rodam no CI (`.github/workflows/ci.yml`).

## Pacotes e versões
- **npm** com workspaces e `package-lock.json` (`"packageManager": "npm@11.4.2"`). Nunca gerar `yarn.lock` aqui; os apps usam Yarn Classic, de propósito.
- Conflito de peer deps (reanimated × react-native): `npm install --legacy-peer-deps`.
- design-tokens, native-ui e web-ui sobem juntos na mesma versão; a tag `v*` publica no GitHub Packages. Processo na skill `release`.

## Escopo
- Componente novo vai em `packages/native-ui`. O `web-ui` está parado: a stack da vitrine web pública ainda não foi decidida.
- Skills: `component` (criar ou alterar componente) e `release` (PR, versão e publicação).

## Boas práticas (obrigatórias)
- **Tokens sempre:** cores, raios, espaçamentos e tipografia vêm de `@x-men-evolution/design-tokens/native`. Nunca hex nem valor mágico.
- **Padrão dos componentes existentes** (`FilterChip.tsx`, `Text.tsx`): função nomeada exportada, `type XProps = Omit<PressableProps, ...> & {...}`, `StyleSheet.create` no estático, dinâmico inline no array, `style` do consumidor por último.
- **Acessibilidade:** `accessibilityRole`, `accessibilityState` e alvo de toque adequado.
- **Reuso interno:** helpers em `src/internal/` (`typography`, `fieldMetrics`, `useFocusState`); conferir antes de criar.
- **Peer dependencies:** dependência de runtime do consumidor é peer, opcional só se nada do barrel principal a importa. Novas externals em `tsup.config.ts`.
- **API mínima:** só as props necessárias. Variante tipográfica nunca define cor.
- **Comentário** só para restrição que o código não expressa.

## Contratos com os apps
- `Text` resolve a fonte Inter pelo peso: o app precisa carregar `Inter_400Regular`, `Inter_500Medium`, `Inter_600SemiBold` e `Inter_700Bold` com esses nomes. Aceita `className` via `cssInterop`, por isso `nativewind` é peer obrigatório.
- `Sheet` usa `@gorhom/bottom-sheet`: o app precisa de `GestureHandlerRootView` e `BottomSheetModalProvider` na raiz. gorhom, gesture-handler e reanimated são peers opcionais (só o `Sheet` usa); `react-native-safe-area-context` é obrigatório. Para modal sem gesto, `FullScreenModal`.
- `SearchInput` tem alturas próprias (36/48/60), maiores que as dos outros campos, por decisão do Figma: não unificar.
- `TabBar`: a variante Prestador ainda tem Chat (deve virar Registros), e o componente vai se dividir em um do `vrum-driver` e um do `vrum-partner`.
