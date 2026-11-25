---
name: tailwind-patterns
description: Princípios do Tailwind CSS v4. Configuração baseada em CSS, container queries, padrões modernos, arquitetura de design tokens.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Padrões Tailwind CSS (v4 - 2025)

> Utility-first CSS moderno com configuração nativa de CSS.

---

## 1. Arquitetura Tailwind v4

### O que Mudou da v3

| v3 (Legado) | v4 (Atual) |
|-------------|-----------|
| `tailwind.config.js` | Diretiva `@theme` baseada em CSS |
| Plugin PostCSS | Oxide engine (10x mais rápido) |
| Modo JIT | Nativo, sempre ativo |
| Sistema de plugins | Recursos nativos de CSS |
| Diretiva `@apply` | Ainda funciona, desaconselhado |

### Conceitos Principais v4

| Conceito | Descrição |
|----------|-----------|
| **CSS-first** | Configuração em CSS, não JavaScript |
| **Oxide Engine** | Compilador baseado em Rust, muito mais rápido |
| **Nesting Nativo** | Nesting de CSS sem PostCSS |
| **Variáveis CSS** | Todos os tokens expostos como variáveis `--*` |

---

## 2. Configuração Baseada em CSS

### Definição de Tema

```
@theme {
  /* Cores - use nomes semânticos */
  --color-primary: oklch(0.7 0.15 250);
  --color-surface: oklch(0.98 0 0);
  --color-surface-dark: oklch(0.15 0 0);
  
  /* Escala de espaçamento */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 2rem;
  
  /* Tipografia */
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}
```

### Quando Estender vs Sobrescrever

| Ação | Use Quando |
|------|-----------|
| **Estender** | Adicionar novos valores junto aos padrões |
| **Sobrescrever** | Substituir escala padrão completamente |
| **Tokens semânticos** | Nomenclatura específica do projeto (primary, surface) |

---

## 3. Container Queries (Nativo v4)

### Breakpoint vs Container

| Tipo | Responde A |
|------|-----------|
| **Breakpoint** (`md:`) | Largura do viewport |
| **Container** (`@container`) | Largura do elemento pai |

### Uso de Container Query

| Padrão | Classes |
|--------|---------|
| Definir container | `@container` no pai |
| Breakpoint de container | `@sm:`, `@md:`, `@lg:` nos filhos |
| Containers nomeados | `@container/card` para especificidade |

### Quando Usar

| Cenário | Use |
|--------|-----|
| Layouts no nível da página | Breakpoints de viewport |
| Design responsivo no nível de componente | Container queries |
| Componentes reutilizáveis | Container queries (independentes de contexto) |

---

## 4. Design Responsivo

### Sistema de Breakpoints

| Prefixo | Largura Mínima | Alvo |
|---------|---|---|
| (nenhum) | 0px | Base mobile-first |
| `sm:` | 640px | Telefone grande / tablet pequeno |
| `md:` | 768px | Tablet |
| `lg:` | 1024px | Laptop |
| `xl:` | 1280px | Desktop |
| `2xl:` | 1536px | Desktop grande |

### Princípio Mobile-First

1. Escreva estilos mobile primeiro (sem prefixo)
2. Adicione substituições para telas maiores com prefixos
3. Exemplo: `w-full md:w-1/2 lg:w-1/3`

---

## 5. Modo Escuro

### Estratégias de Configuração

| Método | Comportamento | Use Quando |
|--------|---|---|
| `class` | Classe `.dark` ativa | Alternador de tema manual |
| `media` | Segue preferência do sistema | Sem controle do usuário |
| `selector` | Seletor customizado (v4) | Temas complexos |

### Padrão de Modo Escuro

| Elemento | Claro | Escuro |
|----------|-------|--------|
| Fundo | `bg-white` | `dark:bg-zinc-900` |
| Texto | `text-zinc-900` | `dark:text-zinc-100` |
| Bordas | `border-zinc-200` | `dark:border-zinc-700` |

---

## 6. Padrões de Layout Moderno

### Padrões Flexbox

| Padrão | Classes |
|--------|---------|
| Centrar (ambos os eixos) | `flex items-center justify-center` |
| Stack vertical | `flex flex-col gap-4` |
| Linha horizontal | `flex gap-4` |
| Espaçamento entre | `flex justify-between items-center` |
| Grade com wrap | `flex flex-wrap gap-4` |

### Padrões Grid

| Padrão | Classes |
|--------|---------|
| Auto-fit responsivo | `grid grid-cols-[repeat(auto-fit,minmax(250px,1fr))]` |
| Assimétrico (Bento) | `grid grid-cols-3 grid-rows-2` com spans |
| Layout sidebar | `grid grid-cols-[auto_1fr]` |

> **Nota:** Prefira layouts assimétricos/Bento em vez de grids simétricos de 3 colunas.

---

## 7. Sistema de Cores Moderno

### OKLCH vs RGB/HSL

| Formato | Vantagem |
|---------|----------|
| **OKLCH** | Perceptualmente uniforme, melhor para design |
| **HSL** | Matiz/saturação intuitivos |
| **RGB** | Compatibilidade legada |

### Arquitetura de Token de Cor

| Camada | Exemplo | Propósito |
|--------|---------|-----------|
| **Primitiva** | `--blue-500` | Valores de cor brutos |
| **Semântica** | `--color-primary` | Nomenclatura baseada em propósito |
| **Componente** | `--button-bg` | Específico do componente |

---

## 8. Sistema de Tipografia

### Padrão de Pilha de Fontes

| Tipo | Recomendado |
|------|-------------|
| Sans | `'Inter', 'SF Pro', system-ui, sans-serif` |
| Mono | `'JetBrains Mono', 'Fira Code', monospace` |
| Display | `'Outfit', 'Poppins', sans-serif` |

### Escala de Tipos

| Classe | Tamanho | Uso |
|--------|---------|-----|
| `text-xs` | 0.75rem | Labels, captions |
| `text-sm` | 0.875rem | Texto secundário |
| `text-base` | 1rem | Texto do corpo |
| `text-lg` | 1.125rem | Texto destaque |
| `text-xl`+ | 1.25rem+ | Headings |

---

## 9. Animações e Transições

### Animações Nativas

| Classe | Efeito |
|--------|--------|
| `animate-spin` | Rotação contínua |
| `animate-ping` | Pulso de atenção |
| `animate-pulse` | Pulso sutil de opacidade |
| `animate-bounce` | Efeito de salto |

### Padrões de Transição

| Padrão | Classes |
|--------|---------|
| Todas as propriedades | `transition-all duration-200` |
| Específica | `transition-colors duration-150` |
| Com easing | `ease-out` ou `ease-in-out` |
| Efeito hover | `hover:scale-105 transition-transform` |

---

## 10. Extração de Componentes

### Quando Extrair

| Sinal | Ação |
|-------|------|
| Mesma combinação de classes 3+ vezes | Extrair componente |
| Variantes de estado complexas | Extrair componente |
| Elemento do design system | Extrair + documentar |

### Métodos de Extração

| Método | Use Quando |
|--------|-----------|
| **Componente React/Vue** | Dinâmico, JS necessário |
| **`@apply` em CSS** | Estático, JS não necessário |
| **Design tokens** | Valores reutilizáveis |

---

## 11. Anti-padrões

| Não Faça | Faça |
|----------|------|
| Valores arbitrários em toda parte | Use escala de design system |
| `!important` | Corrija especificidade propriamente |
| `style=` inline | Use utilities |
| Duplicar listas longas de classes | Extraia componente |
| Misturar config v3 com v4 | Migre completamente para CSS-first |
| Usar `@apply` pesadamente | Prefira componentes |

---

## 12. Princípios de Performance

| Princípio | Implementação |
|-----------|---|
| **Purge unused** | Automático em v4 |
| **Evite dinamismo** | Sem classes com template string |
| **Use Oxide** | Padrão em v4, 10x mais rápido |
| **Cache builds** | CI/CD caching |

---

> **Lembre-se:** Tailwind v4 é CSS-first. Abraça variáveis CSS, container queries e recursos nativos. O arquivo de config agora é opcional.