---
name: shadcn
description: Gerencia componentes e projetos shadcn/ui, fornecendo contexto, documentação e padrões de uso para construir sistemas de design modernos.
user-invocable: false
risk: safe
source: https://github.com/shadcn-ui/ui/tree/main/skills/shadcn
date_added: "2026-03-07"
---

# shadcn/ui

Um framework para construir UI, componentes e sistemas de design. Componentes são adicionados como código-fonte ao projeto do usuário via CLI.

> **IMPORTANTE:** Execute todos os comandos da CLI usando o executor de pacotes do projeto: `npx shadcn@latest`, `pnpm dlx shadcn@latest`, ou `bunx --bun shadcn@latest` — baseado no `packageManager` do projeto. Os exemplos abaixo usam `npx shadcn@latest`, mas substitua pelo executor correto do projeto.

## Quando Usar
- Use ao adicionar novos componentes do shadcn/ui ou registros da comunidade.
- Use ao estilizar, compor ou depurar componentes shadcn/ui existentes.
- Use ao inicializar um novo projeto ou alternar presets do sistema de design.
- Use para recuperar documentação de componentes, exemplos e referências de API.

## Contexto Atual do Projeto

```json
!`npx shadcn@latest info --json 2>/dev/null || echo '{"error": "No shadcn project found. Run shadcn init first."}'`
```

O JSON acima contém a config do projeto e componentes instalados. Use `npx shadcn@latest docs <component>` para obter documentação e URLs de exemplos para qualquer componente.

## Princípios

1. **Use componentes existentes primeiro.** Use `npx shadcn@latest search` para verificar registros antes de escrever UI personalizada. Verifique registros da comunidade também.
2. **Componha, não reinvente.** Página de configurações = Tabs + Card + controles de formulário. Dashboard = Sidebar + Card + Chart + Table.
3. **Use variantes built-in antes de estilos customizados.** `variant="outline"`, `size="sm"`, etc.
4. **Use cores semânticas.** `bg-primary`, `text-muted-foreground` — nunca valores brutos como `bg-blue-500`.

## Regras Críticas

Estas regras são **sempre aplicadas**. Cada uma link para um arquivo com pares de código Incorreto/Correto.

### Estilos & Tailwind → [styling.md](./rules/styling.md)

- **`className` para layout, não para estilos.** Nunca sobrescreva cores ou tipografia de componentes.
- **Sem `space-x-*` ou `space-y-*`.** Use `flex` com `gap-*`. Para pilhas verticais, `flex flex-col gap-*`.
- **Use `size-*` quando largura e altura são iguais.** `size-10` não `w-10 h-10`.
- **Use atalho `truncate`.** Não `overflow-hidden text-ellipsis whitespace-nowrap`.
- **Sem sobrescrita manual de cores `dark:`.** Use tokens semânticos (`bg-background`, `text-muted-foreground`).
- **Use `cn()` para classes condicionais.** Não escreva ternários com template literal manual.
- **Sem `z-index` manual em componentes de sobreposição.** Dialog, Sheet, Popover, etc. tratam seu próprio empilhamento.

### Formulários & Inputs → [forms.md](./rules/forms.md)

- **Formulários usam `FieldGroup` + `Field`.** Nunca use `div` bruto com `space-y-*` ou `grid gap-*` para layout de formulário.
- **`InputGroup` usa `InputGroupInput`/`InputGroupTextarea`.** Nunca `Input`/`Textarea` bruto dentro de `InputGroup`.
- **Botões dentro de inputs usam `InputGroup` + `InputGroupAddon`.**
- **Conjuntos de opções (2–7 escolhas) usam `ToggleGroup`.** Não faça loop `Button` com estado ativo manual.
- **`FieldSet` + `FieldLegend` para agrupar checkboxes/radios relacionados.** Não use `div` com heading.
- **Validação de Field usa `data-invalid` + `aria-invalid`.** `data-invalid` em `Field`, `aria-invalid` no controle. Para desabilitado: `data-disabled` em `Field`, `disabled` no controle.

### Estrutura de Componentes → [composition.md](./rules/composition.md)

- **Items sempre dentro de seu Group.** `SelectItem` → `SelectGroup`. `DropdownMenuItem` → `DropdownMenuGroup`. `CommandItem` → `CommandGroup`.
- **Use `asChild` (radix) ou `render` (base) para triggers customizados.** Verifique campo `base` de `npx shadcn@latest info`. → [base-vs-radix.md](./rules/base-vs-radix.md)
- **Dialog, Sheet e Drawer sempre precisam de Title.** `DialogTitle`, `SheetTitle`, `DrawerTitle` obrigatórios para acessibilidade. Use `className="sr-only"` se oculto visualmente.
- **Use composição completa de Card.** `CardHeader`/`CardTitle`/`CardDescription`/`CardContent`/`CardFooter`. Não despeje tudo em `CardContent`.
- **Button não possui `isPending`/`isLoading`.** Componha com `Spinner` + `data-icon` + `disabled`.
- **`TabsTrigger` deve estar dentro de `TabsList`.** Nunca renderize triggers diretamente em `Tabs`.
- **`Avatar` sempre precisa de `AvatarFallback`.** Para quando a imagem falhar ao carregar.

### Use Componentes, Não Markup Customizado → [composition.md](./rules/composition.md)

- **Use componentes existentes antes de markup customizado.** Verifique se um componente existe antes de escrever uma `div` estilizada.
- **Callouts usam `Alert`.** Não construa divs estilizados customizados.
- **Estados vazios usam `Empty`.** Não construa markup de estado vazio customizado.
- **Toast via `sonner`.** Use `toast()` do `sonner`.
- **Use `Separator`** em vez de `<hr>` ou `<div className="border-t">`.
- **Use `Skeleton`** para placeholders de loading. Sem divs customizados `animate-pulse`.
- **Use `Badge`** em vez de spans estilizados customizados.

### Ícones → [icons.md](./rules/icons.md)

- **Ícones em `Button` usam `data-icon`.** `data-icon="inline-start"` ou `data-icon="inline-end"` no ícone.
- **Sem classes de dimensionamento em ícones dentro de componentes.** Componentes tratam dimensionamento de ícone via CSS. Sem `size-4` ou `w-4 h-4`.
- **Passe ícones como objetos, não como chaves string.** `icon={CheckIcon}`, não uma busca de string.

### CLI

- **Nunca decodifique ou busque códigos preset manualmente.** Passe-os diretamente para `npx shadcn@latest init --preset <code>`.

## Padrões-Chave

Estes são os padrões mais comuns que diferenciam código correto em shadcn/ui. Para casos extremos, veja os arquivos de regras linkados acima.

```tsx
// Layout de formulário: FieldGroup + Field, não div + Label.
<FieldGroup>
  <Field>
    <FieldLabel htmlFor="email">Email</FieldLabel>
    <Input id="email" />
  </Field>
</FieldGroup>

// Validação: data-invalid em Field, aria-invalid no controle.
<Field data-invalid>
  <FieldLabel>Email</FieldLabel>
  <Input aria-invalid />
  <FieldDescription>Email inválido.</FieldDescription>
</Field>

// Ícones em botões: data-icon, sem classes de dimensionamento.
<Button>
  <SearchIcon data-icon="inline-start" />
  Buscar
</Button>

// Espaçamento: gap-*, não space-y-*.
<div className="flex flex-col gap-4">  // correto
<div className="space-y-4">           // errado

// Dimensões iguais: size-*, não w-* h-*.
<Avatar className="size-10">   // correto
<Avatar className="w-10 h-10"> // errado

// Cores de status: variantes Badge ou tokens semânticos, não cores brutas.
<Badge variant="secondary">+20.1%</Badge>    // correto
<span className="text-emerald-600">+20.1%</span> // errado
```

## Seleção de Componentes

| Necessidade                | Use                                                                                                 |
| -------------------------- | --------------------------------------------------------------------------------------------------- |
| Botão/ação                 | `Button` com variante apropriada                                                                   |
| Inputs de formulário       | `Input`, `Select`, `Combobox`, `Switch`, `Checkbox`, `RadioGroup`, `Textarea`, `InputOTP`, `Slider` |
| Alternar entre 2–5 opções  | `ToggleGroup` + `ToggleGroupItem`                                                                  |
| Exibição de dados          | `Table`, `Card`, `Badge`, `Avatar`                                                                 |
| Navegação                  | `Sidebar`, `NavigationMenu`, `Breadcrumb`, `Tabs`, `Pagination`                                    |
| Sobreposições              | `Dialog` (modal), `Sheet` (painel lateral), `Drawer` (folha inferior), `AlertDialog` (confirmação)  |
| Feedback                   | `sonner` (toast), `Alert`, `Progress`, `Skeleton`, `Spinner`                                       |
| Paleta de comando          | `Command` dentro de `Dialog`                                                                       |
| Gráficos                   | `Chart` (encapsula Recharts)                                                                       |
| Layout                     | `Card`, `Separator`, `Resizable`, `ScrollArea`, `Accordion`, `Collapsible`                         |
| Estados vazios             | `Empty`                                                                                             |
| Menus                      | `DropdownMenu`, `ContextMenu`, `Menubar`                                                           |
| Tooltips/info              | `Tooltip`, `HoverCard`, `Popover`                                                                  |

## Campos-Chave

O contexto do projeto injetado contém estes campos-chave:

- **`aliases`** → use o prefixo de alias real para imports (ex: `@/`, `~/`), nunca codifique.
- **`isRSC`** → quando `true`, componentes usando `useState`, `useEffect`, manipuladores de eventos ou APIs do navegador precisam de `"use client"` no topo do arquivo. Sempre referencie este campo ao aconselhar sobre a diretiva.
- **`tailwindVersion`** → `"v4"` usa blocos `@theme inline`; `"v3"` usa `tailwind.config.js`.
- **`tailwindCssFile`** → o arquivo CSS global onde variáveis CSS customizadas são definidas. Sempre edite este arquivo, nunca crie um novo.
- **`style`** → tratamento visual do componente (ex: `nova`, `vega`).
- **`base`** → biblioteca primitiva (`radix` ou `base`). Afeta APIs de componentes e props disponíveis.
- **`iconLibrary`** → determina imports de ícone. Use `lucide-react` para `lucide`, `@tabler/icons-react` para `tabler`, etc. Nunca assuma `lucide-react`.
- **`resolvedPaths`** → destinos exatos no sistema de arquivos para componentes, utils, hooks, etc.
- **`framework`** → roteamento e convenções de arquivo (ex: Next.js App Router vs Vite SPA).
- **`packageManager`** → use isto para qualquer instalação de dependência não-shadcn (ex: `pnpm add date-fns` vs `npm install date-fns`).

Veja [cli.md — `info` command](./cli.md) para referência completa de campos.

## Documentação, Exemplos e Uso de Componentes

Execute `npx shadcn@latest docs <component>` para obter as URLs para documentação, exemplos e referência de API de um componente. Busque estas URLs para obter o conteúdo real.

```bash
npx shadcn@latest docs button dialog select
```

**Ao criar, corrigir, depurar ou usar um componente, sempre execute `npx shadcn@latest docs` e busque as URLs primeiro.** Isto garante que você está trabalhando com a API correta e padrões de uso em vez de adivinhar.

## Workflow

1. **Obtenha contexto do projeto** — já injetado acima. Execute `npx shadcn@latest info` novamente se precisar atualizar.
2. **Verifique componentes instalados primeiro** — antes de executar `add`, sempre verifique a lista `components` do contexto do projeto ou liste o diretório `resolvedPaths.ui`. Não importe componentes que não foram adicionados, e não re-adicione os já instalados.
3. **Encontre componentes** — `npx shadcn@latest search`.
4. **Obtenha docs e exemplos** — execute `npx shadcn@latest docs <component>` para obter URLs, depois busque-as. Use `npx shadcn@latest view` para navegar itens de registro que você não instalou. Para visualizar alterações em componentes instalados, use `npx shadcn@latest add --diff`.
5. **Instale ou atualize** — `npx shadcn@latest add`. Ao atualizar componentes existentes, use `--dry-run` e `--diff` para visualizar alterações primeiro (veja [Atualizando Componentes](#atualizando-componentes) abaixo).
6. **Corrija imports em componentes de terceiros** — Após adicionar componentes de registros da comunidade (ex: `@bundui`, `@magicui`), verifique os arquivos não-UI adicionados para caminhos de import codificados como `@/components/ui/...`. Estes não corresponderão aos aliases reais do projeto. Use `npx shadcn@latest info` para obter o alias `ui` correto (ex: `@workspace/ui/components`) e reescreva os imports accordingly. A CLI reescreve imports para seus próprios arquivos de UI, mas componentes de registro de terceiros podem usar caminhos padrão que não correspondem ao projeto.
7. **Analise componentes adicionados** — Após adicionar um componente ou bloco de qualquer registro, **sempre leia os arquivos adicionados e verifique se estão corretos**. Verifique sub-componentes faltantes (ex: `SelectItem` sem `SelectGroup`), imports faltando, composição incorreta, ou violações das [Regras Críticas](#regras-críticas). Também substitua qualquer import de ícone pela `iconLibrary` do projeto a partir do contexto do projeto (ex: se o item de registro usa `lucide-react` mas o projeto usa `hugeicons`, troque os imports e nomes de ícone accordingly). Corrija todos os problemas antes de prosseguir.
8. **Registro deve ser explícito** — Quando o usuário pedir para adicionar um bloco ou componente, **não adivinhe o registro**. Se nenhum registro for especificado (ex: usuário diz "adicione um bloco de login" sem especificar `@shadcn`, `@tailark`, etc.), pergunta qual registro usar. Nunca padrão para um registro em nome do usuário.
9. **Alternando presets** — Pergunte ao usuário primeiro: **reinstalar**, **mesclar**, ou **pular**?
   - **Reinstalar**: `npx shadcn@latest init --preset <code> --force --reinstall`. Sobrescreve todos os componentes.
   - **Mesclar**: `npx shadcn@latest init --preset <code> --force --no-reinstall`, depois execute `npx shadcn@latest info` para listar componentes instalados, depois para cada componente instalado use `--dry-run` e `--diff` para [mesclar inteligentemente](#atualizando-componentes) individualmente.
   - **Pular**: `npx shadcn@latest init --preset <code> --force --no-reinstall`. Apenas atualiza config e CSS, deixa componentes como estão.

## Atualizando Componentes

Quando o usuário pede para atualizar um componente da upstream mantendo suas alterações locais, use `--dry-run` e `--diff` para mesclar inteligentemente. **NUNCA busque arquivos brutos do GitHub manualmente — sempre use a CLI.**

1. Execute `npx shadcn@latest add <component> --dry-run` para ver todos os arquivos que seriam afetados.
2. Para cada arquivo, execute `npx shadcn@latest add <component> --diff <file>` para ver o que mudou na upstream vs local.
3. Decida por arquivo baseado no diff:
   - Sem alterações locais → seguro sobrescrever.
   - Tem alterações locais → leia o arquivo local, analise o diff, e aplique atualizações da upstream enquanto preserva modificações locais.
   - Usuário diz "apenas atualize tudo" → use `--overwrite`, mas confirme primeiro.
4. **Nunca use `--overwrite` sem aprovação explícita do usuário.**

## Referência Rápida

```bash
# Crie um novo projeto.
npx shadcn@latest init --name my-app --preset base-nova
npx shadcn@latest init --name my-app --preset a2r6bw --template vite

# Crie um projeto monorepo.
npx shadcn@latest init --name my-app --preset base-nova --monorepo
npx shadcn@latest init --name my-app --preset base-nova --template next --monorepo

# Inicialize projeto existente.
npx shadcn@latest init --preset base-nova
npx shadcn@latest init --defaults  # atalho: --template=next --preset=base-nova

# Adicione componentes.
npx shadcn@latest add button card dialog
npx shadcn@latest add @magicui/shimmer-button
npx shadcn@latest add --all

# Visualize alterações antes de adicionar/atualizar.
npx shadcn@latest add button --dry-run
npx shadcn@latest add button --diff button.tsx
npx shadcn@latest add @acme/form --view button.tsx

# Pesquise registros.
npx shadcn@latest search @shadcn -q "sidebar"
npx shadcn@latest search @tailark -q "stats"

# Obtenha docs e URLs de exemplos de componentes.
npx shadcn@latest docs button dialog select

# Veja detalhes de item de registro (para itens ainda não instalados).
npx shadcn@latest view @shadcn/button
```

**Presets nomeados:** `base-nova`, `radix-nova`
**Templates:** `next`, `vite`, `start`, `react-router`, `astro` (todos suportam `--monorepo`) e `laravel` (não suportado para monorepo)
**Códigos de preset:** Strings Base62 começando com `a` (ex: `a2r6bw`), de [ui.shadcn.com](https://ui.shadcn.com).

## Referências Detalhadas

- [rules/forms.md](./rules/forms.md) — FieldGroup, Field, InputGroup, ToggleGroup, FieldSet, validation states
- [rules/composition.md](./rules/composition.md) — Groups, overlays, Card, Tabs, Avatar, Alert, Empty, Toast, Separator, Skeleton, Badge, Button loading
- [rules/icons.md](./rules/icons.md) — data-icon, icon sizing, passing icons as objects
- [rules/styling.md](./rules/styling.md) — Semantic colors, variants, className, spacing, size, truncate, dark mode, cn(), z-index
- [rules/base-vs-radix.md](./rules/base-vs-radix.md) — asChild vs render, Select, ToggleGroup, Slider, Accordion
- [cli.md](./cli.md) — Commands, flags, presets, templates
- [customization.md](./customization.md) — Theming, CSS variables, extending components