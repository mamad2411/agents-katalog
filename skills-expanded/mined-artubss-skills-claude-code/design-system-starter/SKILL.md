---
name: design-system-starter
description: Crie e evolua sistemas de design com design tokens, arquitetura de componentes, diretrizes de acessibilidade e templates de documentação. Garante UI consistente, escalável e acessível em todos os produtos.
license: MIT
metadata:
  version: 1.0.0
  tags: [design-system, ui, components, design-tokens, accessibility, frontend]
---

# Design System Starter

Construa sistemas de design robustos e escaláveis que garantem consistência visual e experiências de usuário excepcionais.

---

## Início Rápido

Basta descrever o que você precisa:

```
Create a design system for my React app with dark mode support
```

É só isso. A skill fornece tokens, componentes e diretrizes de acessibilidade.

---

## Gatilhos

| Gatilho | Exemplo |
|---------|---------|
| Criar sistema de design | "Create a design system for my app" |
| Design tokens | "Set up design tokens for colors and spacing" |
| Arquitetura de componentes | "Design component structure using atomic design" |
| Acessibilidade | "Ensure WCAG 2.1 compliance for my components" |
| Dark mode | "Implement theming with dark mode support" |

---

## Referência Rápida

| Tarefa | Saída |
|------|--------|
| Design tokens | JSON de cores, tipografia, espaçamento, sombras |
| Estrutura de componentes | Hierarquia de design atômico (átomos, moléculas, organismos) |
| Temas | CSS variables ou setup de ThemeProvider |
| Acessibilidade | Padrões compatíveis com WCAG 2.1 AA |
| Documentação | Docs de componentes com props, exemplos, notas de a11y |

---

## Recursos Inclusos

- `references/component-examples.md` - Implementações completas de componentes
- `templates/design-tokens-template.json` - Formato W3C para design tokens
- `templates/component-template.tsx` - Template de componente React
- `checklists/design-system-checklist.md` - Checklist de auditoria do sistema de design

---

## Filosofia do Sistema de Design

### O que é um Sistema de Design?

Um sistema de design é mais do que uma biblioteca de componentes—é uma coleção de:

1. **Design Tokens**: Decisões de design fundamentais (cores, espaçamento, tipografia)
2. **Componentes**: Blocos de construção reutilizáveis de UI
3. **Padrões**: Soluções e composições comuns de UX
4. **Diretrizes**: Regras, princípios e boas práticas
5. **Documentação**: Como usar tudo de forma eficaz

### Princípios Fundamentais

**1. Consistência Acima de Criatividade**
- Padrões previsíveis reduzem carga cognitiva
- Usuários aprendem uma vez, aplicam em todos os lugares
- Designers e desenvolvedores falam a mesma linguagem

**2. Acessibilidade por Padrão**
- Conformidade WCAG 2.1 Nível AA mínimo
- Navegação por teclado integrada
- Suporte a leitura de tela desde o início

**3. Escalável e Mantível**
- Design tokens permitem mudanças globais
- Composição de componentes reduz duplicação
- Estratégias de versionamento e descontinuação

**4. Amigável a Desenvolvedores**
- Contratos de API claros
- Documentação abrangente
- Fácil de integrar e personalizar

---

## Design Tokens

Design tokens são as decisões de design atômicas que definem a linguagem visual do seu sistema.

### Categorias de Tokens

#### 1. Tokens de Cor

**Cores Primitivas** (Valores brutos):
```json
{
  "color": {
    "primitive": {
      "blue": {
        "50": "#eff6ff",
        "100": "#dbeafe",
        "200": "#bfdbfe",
        "300": "#93c5fd",
        "400": "#60a5fa",
        "500": "#3b82f6",
        "600": "#2563eb",
        "700": "#1d4ed8",
        "800": "#1e40af",
        "900": "#1e3a8a",
        "950": "#172554"
      }
    }
  }
}
```

**Cores Semânticas** (Significado contextual):
```json
{
  "color": {
    "semantic": {
      "brand": {
        "primary": "{color.primitive.blue.600}",
        "primary-hover": "{color.primitive.blue.700}",
        "primary-active": "{color.primitive.blue.800}"
      },
      "text": {
        "primary": "{color.primitive.gray.900}",
        "secondary": "{color.primitive.gray.600}",
        "tertiary": "{color.primitive.gray.500}",
        "disabled": "{color.primitive.gray.400}",
        "inverse": "{color.primitive.white}"
      },
      "background": {
        "primary": "{color.primitive.white}",
        "secondary": "{color.primitive.gray.50}",
        "tertiary": "{color.primitive.gray.100}"
      },
      "feedback": {
        "success": "{color.primitive.green.600}",
        "warning": "{color.primitive.yellow.600}",
        "error": "{color.primitive.red.600}",
        "info": "{color.primitive.blue.600}"
      }
    }
  }
}
```

**Acessibilidade**: Garanta que as proporções de contraste de cor atendam ao WCAG 2.1 Nível AA:
- Texto normal: mínimo 4.5:1
- Texto grande (18pt+ ou 14pt+ negrito): mínimo 3:1
- Componentes UI e gráficos: mínimo 3:1

#### 2. Tokens de Tipografia

```json
{
  "typography": {
    "fontFamily": {
      "sans": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
      "serif": "'Georgia', 'Times New Roman', serif",
      "mono": "'Fira Code', 'Courier New', monospace"
    },
    "fontSize": {
      "xs": "0.75rem",     // 12px
      "sm": "0.875rem",    // 14px
      "base": "1rem",      // 16px
      "lg": "1.125rem",    // 18px
      "xl": "1.25rem",     // 20px
      "2xl": "1.5rem",     // 24px
      "3xl": "1.875rem",   // 30px
      "4xl": "2.25rem",    // 36px
      "5xl": "3rem"        // 48px
    },
    "fontWeight": {
      "normal": 400,
      "medium": 500,
      "semibold": 600,
      "bold": 700
    },
    "lineHeight": {
      "tight": 1.25,
      "normal": 1.5,
      "relaxed": 1.75,
      "loose": 2
    },
    "letterSpacing": {
      "tight": "-0.025em",
      "normal": "0",
      "wide": "0.025em"
    }
  }
}
```

#### 3. Tokens de Espaçamento

**Escala**: Use uma escala de espaçamento consistente (geralmente base de 4px ou 8px)

```json
{
  "spacing": {
    "0": "0",
    "1": "0.25rem",   // 4px
    "2": "0.5rem",    // 8px
    "3": "0.75rem",   // 12px
    "4": "1rem",      // 16px
    "5": "1.25rem",   // 20px
    "6": "1.5rem",    // 24px
    "8": "2rem",      // 32px
    "10": "2.5rem",   // 40px
    "12": "3rem",     // 48px
    "16": "4rem",     // 64px
    "20": "5rem",     // 80px
    "24": "6rem"      // 96px
  }
}
```

**Espaçamento Específico de Componentes**:
```json
{
  "component": {
    "button": {
      "padding-x": "{spacing.4}",
      "padding-y": "{spacing.2}",
      "gap": "{spacing.2}"
    },
    "card": {
      "padding": "{spacing.6}",
      "gap": "{spacing.4}"
    }
  }
}
```

#### 4. Tokens de Border Radius

```json
{
  "borderRadius": {
    "none": "0",
    "sm": "0.125rem",   // 2px
    "base": "0.25rem",  // 4px
    "md": "0.375rem",   // 6px
    "lg": "0.5rem",     // 8px
    "xl": "0.75rem",    // 12px
    "2xl": "1rem",      // 16px
    "full": "9999px"
  }
}
```

#### 5. Tokens de Sombra

```json
{
  "shadow": {
    "xs": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
    "sm": "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1)",
    "base": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1)",
    "md": "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1)",
    "lg": "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1)",
    "xl": "0 25px 50px -12px rgba(0, 0, 0, 0.25)"
  }
}
```

---

## Arquitetura de Componentes

### Metodologia de Design Atômico

**Átomos** → **Moléculas** → **Organismos** → **Templates** → **Páginas**

#### Átomos (Componentes Primitivos)
Blocos de construção básicos que não podem ser decompostos.

**Exemplos:**
- Button
- Input
- Label
- Icon
- Badge
- Avatar

**Componente Button:**
```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  icon?: React.ReactNode;
  children: React.ReactNode;
}
```

Veja `references/component-examples.md` para implementação completa do Button com variantes, tamanhos e padrões de estilo.

#### Moléculas (Composições Simples)
Grupos de átomos que funcionam juntos.

**Exemplos:**
- SearchBar (Input + Button)
- FormField (Label + Input + ErrorMessage)
- Card (Container + Title + Content + Actions)

**Molécula FormField:**
```typescript
interface FormFieldProps {
  label: string;
  name: string;
  error?: string;
  hint?: string;
  required?: boolean;
  children: React.ReactNode;
}
```

Veja `references/component-examples.md` para FormField, Card (padrão de componente composto), Input com variantes, Modal e mais exemplos de composição.

#### Organismos (Composições Complexas)
Componentes UI complexos compostos por moléculas e átomos.

**Exemplos:**
- Navigation Bar
- Product Card Grid
- User Profile Section
- Modal Dialog

#### Templates (Layouts de Página)
Estruturas no nível da página que definem a colocação de conteúdo.

**Exemplos:**
- Dashboard Layout (Sidebar + Header + Main Content)
- Marketing Page Layout (Hero + Features + Footer)
- Settings Page Layout (Tabs + Content Panels)

#### Páginas (Instâncias Específicas)
Páginas reais com conteúdo real.

---

## Design de API de Componentes

### Boas Práticas de Props

**1. Nomes de Props Previsíveis**
```typescript
// ✅ Bom: Nomenclatura consistente
<Button variant="primary" size="md" />
<Input variant="outlined" size="md" />

// ❌ Ruim: Inconsistente
<Button type="primary" sizeMode="md" />
<Input style="outlined" inputSize="md" />
```

**2. Defaults Sensatos**
```typescript
// ✅ Bom: Fornece defaults
interface ButtonProps {
  variant?: 'primary' | 'secondary';  // Default: primary
  size?: 'sm' | 'md' | 'lg';          // Default: md
}

// ❌ Ruim: Tudo obrigatório
interface ButtonProps {
  variant: 'primary' | 'secondary';
  size: 'sm' | 'md' | 'lg';
  color: string;
  padding: string;
}
```

**3. Composição Sobre Configuração**
```typescript
// ✅ Bom: Componível
<Card>
  <Card.Header>
    <Card.Title>Title</Card.Title>
  </Card.Header>
  <Card.Body>Content</Card.Body>
  <Card.Footer>Actions</Card.Footer>
</Card>

// ❌ Ruim: Props demais
<Card
  title="Title"
  content="Content"
  footerContent="Actions"
  hasHeader={true}
  hasFooter={true}
/>
```

**4. Componentes Polimórficos**
Permita que componentes sejam renderizados como diferentes elementos HTML:
```typescript
<Button as="a" href="/login">Login</Button>
<Button as="button" onClick={handleClick}>Click Me</Button>
```

Veja `references/component-examples.md` para padrões completos de componentes polimórficos em TypeScript.

---

## Temas e Dark Mode

### Estrutura de Tema

```typescript
interface Theme {
  colors: {
    brand: {
      primary: string;
      secondary: string;
    };
    text: {
      primary: string;
      secondary: string;
    };
    background: {
      primary: string;
      secondary: string;
    };
    feedback: {
      success: string;
      warning: string;
      error: string;
      info: string;
    };
  };
  typography: {
    fontFamily: {
      sans: string;
      mono: string;
    };
    fontSize: Record<string, string>;
  };
  spacing: Record<string, string>;
  borderRadius: Record<string, string>;
  shadow: Record<string, string>;
}
```

### Implementação de Dark Mode

**Abordagem 1: CSS Variables**
```css
:root {
  --color-bg-primary: #ffffff;
  --color-text-primary: #000000;
}

[data-theme="dark"] {
  --color-bg-primary: #1a1a1a;
  --color-text-primary: #ffffff;
}
```

**Abordagem 2: Tailwind CSS Dark Mode**
```tsx
<div className="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
  Content
</div>
```

**Abordagem 3: Styled Components ThemeProvider**
```typescript
const lightTheme = { background: '#fff', text: '#000' };
const darkTheme = { background: '#000', text: '#fff' };

<ThemeProvider theme={isDark ? darkTheme : lightTheme}>
  <App />
</ThemeProvider>
```

---

## Diretrizes de Acessibilidade

### Conformidade WCAG 2.1 Nível AA

#### Contraste de Cor
- **Texto normal** (< 18pt): mínimo 4.5:1
- **Texto grande** (≥ 18pt ou ≥ 14pt negrito): mínimo 3:1
- **Componentes UI**: mínimo 3:1

**Ferramentas**: Use verificadores de contraste como [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)

#### Navegação por Teclado
```typescript
// ✅ Todos os elementos interativos devem ser acessíveis por teclado
<button
  onClick={handleClick}
  onKeyDown={(e) => e.key === 'Enter' && handleClick()}
>
  Click me
</button>

// ✅ Gerenciamento de foco
<Modal>
  <FocusTrap>
    {/* Modal content */}
  </FocusTrap>
</Modal>
```

#### Atributos ARIA
Padrões ARIA essenciais:
- `aria-label`: Forneça nomes acessíveis
- `aria-expanded`: Comunique estado expandido/recolhido
- `aria-controls`: Associe controles com conteúdo
- `aria-live`: Anuncie mudanças de conteúdo dinâmico

#### Suporte a Leitor de Tela
- Use elementos HTML semânticos (`<button>`, `<nav>`, `<main>`)
- Evite div/span sem semântica para elementos interativos
- Forneça labels significativos para todos os controles

Veja `references/component-examples.md` para exemplos completos de acessibilidade incluindo Skip Links, focus traps e padrões ARIA.

---

## Padrões de Documentação

### Template de Documentação de Componente

Cada componente deve documentar:
- **Propósito**: O que o componente faz
- **Uso**: Instrução de importação e exemplo básico
- **Variantes**: Estilos visuais disponíveis
- **Props**: Tabela completa de props com tipos, defaults, descrições
- **Acessibilidade**: Suporte a teclado, atributos ARIA, comportamento de leitor de tela
- **Exemplos**: Casos de uso comuns com código

Use Storybook, Docusaurus ou ferramentas similares para documentação interativa.

Veja `templates/component-template.tsx` para a estrutura padrão de componente.

---

## Workflow do Sistema de Design

### 1. Fase de Design
- **Auditoria de padrões existentes**: Identifique inconsistências
- **Defina design tokens**: Cores, tipografia, espaçamento
- **Crie inventário de componentes**: Liste todos os componentes necessários
- **Design no Figma**: Crie biblioteca de componentes

### 2. Fase de Desenvolvimento
- **Configure ferramentas**: Storybook, TypeScript, testes
- **Implemente tokens**: CSS variables ou configuração de tema
- **Construa átomos primeiro**: Comece com primitivos
- **Compose para cima**: Construa moléculas, organismos
- **Documente conforme avança**: Escreva docs junto com código

### 3. Fase de Adoção
- **Crie guia de migração**: Ajude times a adotar
- **Forneça codemods**: Automatize migrações quando possível
- **Execute workshops**: Treine times sobre uso
- **Colete feedback**: Itere com base em uso real

### 4. Fase de Manutenção
- **Versionamento semântico**: Releases major/minor/patch
- **Estratégia de descontinuação**: Descontinue componentes antigos com elegância
- **Changelog**: Documente todas as mudanças
- **Monitore adoção**: Acompanhe uso em todos os produtos

---

## Checklist de Início Rápido

Ao criar um novo sistema de design:

- [ ] Defina princípios e valores de design
- [ ] Estabeleça estrutura de design tokens (cores, tipografia, espaçamento)
- [ ] Crie paleta de cor primitiva (escala 50-950)
- [ ] Defina tokens de cor semântica (brand, text, background, feedback)
- [ ] Estabeleça escala de tipografia e famílias de fontes
- [ ] Estabeleça escala de espaçamento (base 4px ou 8px)
- [ ] Design de componentes atômicos (Button, Input, Label, etc.)
- [ ] Implemente sistema de tema (light/dark mode)
- [ ] Garanta conformidade WCAG 2.1 Nível AA
- [ ] Configure documentação (Storybook ou similar)
- [ ] Crie exemplos de uso para cada componente
- [ ] Estabeleça estratégia de versionamento e release
- [ ] Crie guias de migração para times que adotam