---
name: ui-ux-pro-max
description: "Inteligência de design UI/UX. 50 estilos, 21 paletas, 50 combinações de fontes, 20 gráficos, 9 stacks (React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind, shadcn/ui). Ações: plan, build, create, design, implement, review, fix, improve, optimize, enhance, refactor, check UI/UX code. Projetos: website, landing page, dashboard, admin panel, e-commerce, SaaS, portfolio, blog, mobile app, .html, .tsx, .vue, .svelte. Elementos: button, modal, navbar, sidebar, card, table, form, chart. Estilos: glassmorphism, claymorphism, minimalism, brutalism, neumorphism, bento grid, dark mode, responsive, skeuomorphism, flat design. Tópicos: color palette, accessibility, animation, layout, typography, font pairing, spacing, hover, shadow, gradient. Integrações: shadcn/ui MCP para busca de componentes e exemplos."
---

# UI/UX Pro Max - Design Intelligence

Guia de design abrangente para aplicações web e mobile. Contém 50+ estilos, 97 paletas de cores, 57 combinações de fontes, 99 diretrizes UX e 25 tipos de gráficos em 9 stacks de tecnologia. Banco de dados pesquisável com recomendações baseadas em prioridades.

## Quando Aplicar

Consulte estas diretrizes quando:
- Projetando novos componentes ou páginas de UI
- Escolhendo paletas de cores e tipografia
- Revisando código para problemas de UX
- Construindo landing pages ou dashboards
- Implementando requisitos de acessibilidade

## Categorias de Regras por Prioridade

| Prioridade | Categoria | Impacto | Domínio |
|----------|----------|--------|--------|
| 1 | Acessibilidade | CRÍTICA | `ux` |
| 2 | Toque e Interação | CRÍTICA | `ux` |
| 3 | Performance | ALTA | `ux` |
| 4 | Layout e Responsivo | ALTA | `ux` |
| 5 | Tipografia e Cor | MÉDIA | `typography`, `color` |
| 6 | Animação | MÉDIA | `ux` |
| 7 | Seleção de Estilo | MÉDIA | `style`, `product` |
| 8 | Gráficos e Dados | BAIXA | `chart` |

## Referência Rápida

### 1. Acessibilidade (CRÍTICA)

- `color-contrast` - Razão mínima de 4.5:1 para texto normal
- `focus-states` - Anéis de foco visíveis em elementos interativos
- `alt-text` - Texto alternativo descritivo para imagens relevantes
- `aria-labels` - aria-label para botões apenas com ícone
- `keyboard-nav` - Ordem de tabulação corresponde à ordem visual
- `form-labels` - Use label com atributo for

### 2. Toque e Interação (CRÍTICA)

- `touch-target-size` - Alvo de toque mínimo de 44x44px
- `hover-vs-tap` - Use clique/tap para interações primárias
- `loading-buttons` - Desabilite botão durante operações assíncronas
- `error-feedback` - Mensagens de erro claras próximo ao problema
- `cursor-pointer` - Adicione cursor-pointer a elementos clicáveis

### 3. Performance (ALTA)

- `image-optimization` - Use WebP, srcset, lazy loading
- `reduced-motion` - Verifique prefers-reduced-motion
- `content-jumping` - Reserve espaço para conteúdo assíncrono

### 4. Layout e Responsivo (ALTA)

- `viewport-meta` - width=device-width initial-scale=1
- `readable-font-size` - Mínimo 16px para texto do corpo em mobile
- `horizontal-scroll` - Garanta que o conteúdo se ajuste à largura da viewport
- `z-index-management` - Defina escala de z-index (10, 20, 30, 50)

### 5. Tipografia e Cor (MÉDIA)

- `line-height` - Use 1.5-1.75 para texto do corpo
- `line-length` - Limite a 65-75 caracteres por linha
- `font-pairing` - Combine fontes de heading e corpo por personalidade

### 6. Animação (MÉDIA)

- `duration-timing` - Use 150-300ms para micro-interações
- `transform-performance` - Use transform/opacity, não width/height
- `loading-states` - Skeleton screens ou spinners

### 7. Seleção de Estilo (MÉDIA)

- `style-match` - Compatibilize estilo com tipo de produto
- `consistency` - Use o mesmo estilo em todas as páginas
- `no-emoji-icons` - Use ícones SVG, não emojis

### 8. Gráficos e Dados (BAIXA)

- `chart-type` - Compatibilize tipo de gráfico com tipo de dados
- `color-guidance` - Use paletas de cores acessíveis
- `data-table` - Forneça alternativa de tabela para acessibilidade

## Como Usar

Pesquise domínios específicos usando a ferramenta CLI abaixo.

---

## Pré-requisitos

Verifique se Python está instalado:

```bash
python3 --version || python --version
```

Se Python não está instalado, instale-o conforme o SO do usuário:

**macOS:**
```bash
brew install python3
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install python3
```

**Windows:**
```powershell
winget install Python.Python.3.12
```

---

## Como Usar Esta Skill

Quando o usuário solicita trabalho de UI/UX (design, build, create, implement, review, fix, improve), siga este fluxo de trabalho:

### Passo 1: Analise os Requisitos do Usuário

Extraia informações-chave da solicitação do usuário:
- **Tipo de produto**: SaaS, e-commerce, portfolio, dashboard, landing page, etc.
- **Palavras-chave de estilo**: minimal, playful, professional, elegant, dark mode, etc.
- **Indústria**: healthcare, fintech, gaming, education, etc.
- **Stack**: React, Vue, Next.js, ou padrão `html-tailwind`

### Passo 2: Gere o Design System (OBRIGATÓRIO)

**Sempre comece com `--design-system`** para obter recomendações abrangentes com raciocínio:

```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<tipo_produto> <indústria> <palavras-chave>" --design-system [-p "Nome do Projeto"]
```

Este comando:
1. Pesquisa 5 domínios em paralelo (product, style, color, landing, typography)
2. Aplica regras de raciocínio de `ui-reasoning.csv` para selecionar as melhores correspondências
3. Retorna design system completo: pattern, style, colors, typography, effects
4. Inclui anti-patterns a evitar

**Exemplo:**
```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness service" --design-system -p "Serenity Spa"
```

### Passo 3: Complemente com Pesquisas Detalhadas (conforme necessário)

Após obter o design system, use pesquisas por domínio para obter detalhes adicionais:

```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<palavra-chave>" --domain <domínio> [-n <máx_resultados>]
```

**Quando usar pesquisas detalhadas:**

| Necessidade | Domínio | Exemplo |
|------|--------|---------|
| Mais opções de estilo | `style` | `--domain style "glassmorphism dark"` |
| Recomendações de gráfico | `chart` | `--domain chart "real-time dashboard"` |
| Melhores práticas de UX | `ux` | `--domain ux "animation accessibility"` |
| Fontes alternativas | `typography` | `--domain typography "elegant luxury"` |
| Estrutura de landing | `landing` | `--domain landing "hero social-proof"` |

### Passo 4: Diretrizes de Stack (Padrão: html-tailwind)

Obtenha melhores práticas específicas da implementação. Se o usuário não especificar um stack, **padrão para `html-tailwind`**.

```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<palavra-chave>" --stack html-tailwind
```

Stacks disponíveis: `html-tailwind`, `react`, `nextjs`, `vue`, `svelte`, `swiftui`, `react-native`, `flutter`, `shadcn`

---

## Referência de Pesquisa

### Domínios Disponíveis

| Domínio | Use Para | Exemplos de Palavras-chave |
|--------|---------|------------------|
| `product` | Recomendações de tipo de produto | SaaS, e-commerce, portfolio, healthcare, beauty, service |
| `style` | Estilos de UI, cores, efeitos | glassmorphism, minimalism, dark mode, brutalism |
| `typography` | Combinações de fontes, Google Fonts | elegant, playful, professional, modern |
| `color` | Paletas de cores por tipo de produto | saas, ecommerce, healthcare, beauty, fintech, service |
| `landing` | Estrutura de página, estratégias de CTA | hero, hero-centric, testimonial, pricing, social-proof |
| `chart` | Tipos de gráfico, recomendações de biblioteca | trend, comparison, timeline, funnel, pie |
| `ux` | Melhores práticas, anti-patterns | animation, accessibility, z-index, loading |
| `react` | Performance de React/Next.js | waterfall, bundle, suspense, memo, rerender, cache |
| `web` | Diretrizes de interface web | aria, focus, keyboard, semantic, virtualize |
| `prompt` | Prompts de IA, palavras-chave CSS | (nome do estilo) |

### Stacks Disponíveis

| Stack | Foco |
|-------|-------|
| `html-tailwind` | Utilitários Tailwind, responsivo, a11y (PADRÃO) |
| `react` | State, hooks, performance, patterns |
| `nextjs` | SSR, routing, images, API routes |
| `vue` | Composition API, Pinia, Vue Router |
| `svelte` | Runes, stores, SvelteKit |
| `swiftui` | Views, State, Navigation, Animation |
| `react-native` | Components, Navigation, Lists |
| `flutter` | Widgets, State, Layout, Theming |
| `shadcn` | Componentes shadcn/ui, theming, forms, patterns |

---

## Fluxo de Trabalho de Exemplo

**Solicitação do usuário:** "Criar landing page para serviço profissional de cuidados com a pele"

### Passo 1: Analise os Requisitos
- Tipo de produto: Beauty/Spa service
- Palavras-chave de estilo: elegant, professional, soft
- Indústria: Beauty/Wellness
- Stack: html-tailwind (padrão)

### Passo 2: Gere o Design System (OBRIGATÓRIO)

```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness service elegant" --design-system -p "Serenity Spa"
```

**Saída:** Design system completo com pattern, style, colors, typography, effects e anti-patterns.

### Passo 3: Complemente com Pesquisas Detalhadas (conforme necessário)

```bash
# Obtenha diretrizes de UX para animação e acessibilidade
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "animation accessibility" --domain ux

# Obtenha opções de tipografia alternativas, se necessário
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "elegant luxury serif" --domain typography
```

### Passo 4: Diretrizes de Stack

```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "layout responsive form" --stack html-tailwind
```

**Depois:** Sintetize o design system + pesquisas detalhadas e implemente o design.

---

## Formatos de Saída

A flag `--design-system` suporta dois formatos de saída:

```bash
# Caixa ASCII (padrão) - melhor para exibição em terminal
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system

# Markdown - melhor para documentação
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system -f markdown
```

---

## Dicas para Melhores Resultados

1. **Seja específico com palavras-chave** - "healthcare SaaS dashboard" > "app"
2. **Pesquise múltiplas vezes** - Palavras-chave diferentes revelam insights diferentes
3. **Combine domínios** - Style + Typography + Color = Design system completo
4. **Sempre verifique UX** - Pesquise "animation", "z-index", "accessibility" para problemas comuns
5. **Use a flag de stack** - Obtenha melhores práticas específicas da implementação
6. **Itere** - Se a primeira pesquisa não corresponder, tente palavras-chave diferentes

---

## Regras Comuns para UI Profissional

Estes são problemas frequentemente ignorados que fazem a UI parecer não profissional:

### Ícones e Elementos Visuais

| Regra | Faça | Não Faça |
|------|----|----- |
| **Sem ícones emoji** | Use ícones SVG (Heroicons, Lucide, Simple Icons) | Use emojis como 🎨 🚀 ⚙️ como ícones de UI |
| **Estados de hover estáveis** | Use transições de cor/opacidade no hover | Use scale transforms que deslocam o layout |
| **Logos de marca corretos** | Pesquise SVG oficial em Simple Icons | Adivinhe ou use caminhos de logo incorretos |
| **Tamanho de ícone consistente** | Use viewBox fixo (24x24) com w-6 h-6 | Misture tamanhos de ícone aleatoriamente |

### Interação e Cursor

| Regra | Faça | Não Faça |
|------|----|----- |
| **Cursor pointer** | Adicione `cursor-pointer` a todos os cards clicáveis/hover | Deixe cursor padrão em elementos interativos |
| **Feedback de hover** | Forneça feedback visual (cor, shadow, border) | Sem indicação de que elemento é interativo |
| **Transições suaves** | Use `transition-colors duration-200` | Mudanças de estado instantâneas ou muito lentas (>500ms) |

### Contraste Light/Dark Mode

| Regra | Faça | Não Faça |
|------|----|----- |
| **Glass card light mode** | Use `bg-white/80` ou opacidade maior | Use `bg-white/10` (muito transparente) |
| **Contraste de texto light** | Use `#0F172A` (slate-900) para texto | Use `#94A3B8` (slate-400) para texto do corpo |
| **Texto atenuado light** | Use `#475569` (slate-600) mínimo | Use gray-400 ou mais claro |
| **Visibilidade de border** | Use `border-gray-200` em light mode | Use `border-white/10` (invisível) |

### Layout e Espaçamento

| Regra | Faça | Não Faça |
|------|----|----- |
| **Navbar flutuante** | Adicione `top-4 left-4 right-4` de espaçamento | Cole navbar a `top-0 left-0 right-0` |
| **Padding de conteúdo** | Considere a altura da navbar fixa | Deixe conteúdo escondido atrás de elementos fixos |
| **Max-width consistente** | Use o mesmo `max-w-6xl` ou `max-w-7xl` | Misture larguras diferentes de container |

---

## Checklist Pré-entrega

Antes de entregar código de UI, verifique estes itens:

### Qualidade Visual
- [ ] Sem emojis usados como ícones (use SVG em vez disso)
- [ ] Todos os ícones de conjunto de ícones consistente (Heroicons/Lucide)
- [ ] Logos de marca corretos (verificados em Simple Icons)
- [ ] Estados de hover não causam deslocamento de layout
- [ ] Use cores de tema diretamente (bg-primary) não wrapper var()

### Interação
- [ ] Todos os elementos clicáveis têm `cursor-pointer`
- [ ] Estados de hover fornecem feedback visual claro
- [ ] Transições são suaves (150-300ms)
- [ ] Estados de foco visíveis para navegação por teclado

### Light/Dark Mode
- [ ] Texto em light mode tem contraste suficiente (4.5:1 mínimo)
- [ ] Elementos glass/transparentes visíveis em light mode
- [ ] Borders visíveis em ambos os modos
- [ ] Teste ambos os modos antes da entrega

### Layout
- [ ] Elementos flutuantes têm espaçamento apropriado das bordas
- [ ] Nenhum conteúdo escondido atrás de navbars fixas
- [ ] Responsivo em 375px, 768px, 1024px, 1440px
- [ ] Sem scroll horizontal em mobile

### Acessibilidade
- [ ] Todas as imagens têm alt text
- [ ] Inputs de formulário têm labels
- [ ] Cor não é o único indicador
- [ ] `prefers-reduced-motion` respeitado