---
name: page-specifications
description: Detalhamento granular de cada página do projeto. Cria PAGE-SPEC-*.md com layout, seções, componentes, estados, responsividade e integração com Design System.
---

# Page Specifications Skill

> **Objetivo:** Detalhar CADA página do projeto antes do Breakdown.
> Garante que implementação tenha blueprint completo, não apenas copy genérico.

---

## 🎯 PROPÓSITO

Esta skill resolve a lacuna entre:
- **Content Strategy** (O QUE dizer) → Copy, tom, mensagens
- **Breakdown** (O QUE fazer) → Tasks de desenvolvimento

**Adiciona o COMO:** Layout, componentes, estados, responsividade.

---

## 🔗 QUANDO USAR

| Workflow | Fase | Trigger |
|----------|------|---------|
| `/new-project` | Phase 2.8 | Após Content Strategy aprovado |
| `/legacy-project` | Phase 5.8 | Após Content Strategy |
| `/new-task` | Opcional | Quando adiciona novas páginas |

---

## 📁 ESTRUTURA DE SAÍDA

```
design-system/{projeto}/
├── MASTER.md              ← Design System global
├── layout/
│   └── SHARED-LAYOUT.md   ← Header, Footer, Mobile Menu
└── pages/
    ├── PAGE-SPEC-Landing.md
    ├── PAGE-SPEC-Pricing.md
    ├── PAGE-SPEC-Start.md       (Wizard)
    ├── PAGE-SPEC-Dashboard.md   (Área logada)
    ├── PAGE-SPEC-Admin.md       (Gestão interna)
    └── PAGE-SPEC-{Página}.md
```

---

## 📊 PROCESSO (5 Passos)

### PASSO 1: Identificar Páginas

Listar todas as páginas do projeto baseado em:
- PRD (requisitos)
- TDD (fluxos técnicos)
- Content Strategy (páginas já mapeadas)

**Categorização:**

| Prioridade | Tipo | Exemplos |
|------------|------|----------|
| **Alta** | Core do produto | Landing, Pricing, Start/Wizard, Dashboard |
| **Média** | Suporte ao produto | How it Works, Workflows Library, Videos |
| **Baixa** | Complementar | Community, Blog, About |
| **Interna** | Gestão | Admin, Moderação |

---

### PASSO 2: Criar SHARED-LAYOUT.md

> [!IMPORTANT]
> **OBRIGATÓRIO:** Criar ANTES dos PAGE-SPECs individuais.
> Define elementos compartilhados para evitar duplicação.

**Template:**

```markdown
# Shared Layout Specs - Header & Footer

> **Status:** ⏳ Proposal
> **Aplicação:** Todas as páginas públicas
> **Exceção:** {páginas com layout próprio, ex: Dashboard}

---

## 1. Standard Header (Navbar)

### Visual Spec
| Elemento | Especificação |
|----------|---------------|
| **Position** | Sticky Top |
| **Height** | 64px (h-16) |
| **Background** | Glassmorphism |
| **Border** | border-b border-border |

### Conteúdo
| Elemento | Detalhes |
|----------|----------|
| **Logo** | Logo + Wordmark, link para `/` |
| **Nav Links** | Como Funciona, Workflows, Pricing, Community |
| **CTA** | "Iniciar Projeto" (button primary) |
| **Auth** | Login (ghost) - se não logado |

### Estados
- **Scroll State:** Adiciona shadow ao scrollar
- **Mobile:** Hamburger menu (sheet overlay)

---

## 2. Standard Footer

### Estrutura
| Coluna | Links |
|--------|-------|
| **Produto** | Features, Pricing, Roadmap |
| **Recursos** | Docs, Videos, Community |
| **Empresa** | About, Blog, Contact |
| **Legal** | Terms, Privacy |

### Visual
| Elemento | Especificação |
|----------|---------------|
| **Background** | bg-background |
| **Border** | border-t border-border |
| **Social** | Twitter, LinkedIn, GitHub, YouTube |

---

## 3. Mobile Menu Overlay

- **Trigger:** Hamburger icon (Menu)
- **Style:** Sheet from right
- **Conteúdo:** Nav links + Auth buttons
```

---

### PASSO 3: Criar PAGE-SPEC para cada página

> [!CAUTION]
> **BLOQUEADOR:** Perguntar ao usuário sobre priorização antes de criar todos.
> Podem existir páginas que serão implementadas em V2.

**Pergunta ao Usuário:**

```markdown
## 📄 Páginas Identificadas

Baseado no PRD/TDD/Content Strategy, estas são as páginas do projeto:

### Alta Prioridade (MVP)
- [ ] Landing Page (/)
- [ ] Pricing (/pricing)
- [ ] Start/Wizard (/start)
- [ ] Dashboard (/dashboard)

### Média Prioridade
- [ ] How it Works (/how-it-works)
- [ ] Workflows Library (/workflows)
- [ ] Video Pages (/videos/[slug])

### Baixa Prioridade (V2)
- [ ] Community (/community)
- [ ] Blog (/blog)

### Interna
- [ ] Admin (/admin)

**Quais páginas detalhar agora?**
- A) Todas
- B) Apenas Alta Prioridade (MVP)
- C) Alta + Média
- D) Definir manualmente (liste quais)
```

---

### PASSO 4: Gerar PAGE-SPEC para cada página selecionada

**Template de PAGE-SPEC:**

```markdown
# Page Spec - {Nome da Página} ({rota})

> **Objetivo:** {objetivo da página em 1 linha}
> **Referências:** MASTER.md, SHARED-LAYOUT.md, CONTENT-STRATEGY
> **Status:** ⏳ Proposal | **Data:** {data}

---

## 1. Layout & Estrutura

### Header
> Usar: `SHARED-LAYOUT.md → Standard Header`
> Exceções: {se houver}

### Spatial Anatomy (OBRIGATÓRIO para Dashboard/Admin)

> [!CAUTION]
> **FALHA QUE GEROU ESTA SEÇÃO:** Sidebar e TopBar do Dashboard foram implementados
> como "floating pills" quando a referência mostrava edge-to-edge. Sem esta seção,
> o agente faz suposições sobre posicionamento e arredondamento.

| Elemento | Ancoragem | Border-radius | Altura | Span |
|----------|-----------|---------------|--------|------|
| **Sidebar** | {edge-to-edge left | floating} | {nenhum viewport-side | 16px interno | 32px todos} | {100vh | auto} | {coluna independente | dentro do main} |
| **TopBar** | {top do conteúdo | top total da viewport} | {nenhum | pill} | {64px fixa} | {só conteúdo | full-width incluindo sidebar} |
| **Toggle** | {header da sidebar | topbar | inline} | - | - | - |
| **Content** | {scroll interno | page scroll} | - | {flex-grow} | {restante} |

### Sections
| # | Seção | Objetivo | Componentes |
|---|-------|----------|-------------|
| 1 | Hero | {objetivo} | {componentes principais} |
| 2 | {Seção} | {objetivo} | {componentes} |
| 3 | {Seção} | {objetivo} | {componentes} |

### Footer
> Usar: `SHARED-LAYOUT.md → Standard Footer`

---

## 2. Conteúdo por Seção

### 2.1 {Nome da Seção}

#### Copy
| Elemento | Conteúdo |
|----------|----------|
| **Headline** | {texto} |
| **Subheadline** | {texto} |
| **CTA** | {texto do botão} |

#### Visual
| Elemento | Especificação |
|----------|---------------|
| **Background** | {cor/gradient} |
| **Layout** | {grid, flex, etc} |
| **Componentes** | {lista de componentes} |

#### Estados
- **Default:** {descrição}
- **Loading:** {skeleton/spinner}
- **Empty:** {mensagem + CTA}
- **Error:** {mensagem + retry}

---

## 3. Responsividade

| Breakpoint | Adaptação |
|------------|-----------|
| **Desktop (≥1024px)** | {layout desktop} |
| **Tablet (768-1023px)** | {adaptações} |
| **Mobile (<768px)** | {layout mobile} |

---

## 4. Integrações

| Sistema | Uso nesta página |
|---------|------------------|
| **Auth** | {Supabase - estados logado/não logado} |
| **CMS** | {Sanity - conteúdo dinâmico} |
| **Analytics** | {PostHog - eventos a rastrear} |
| **Payments** | {Stripe - se aplicável} |

---

## 5. SEO & Performance

| Aspecto | Especificação |
|---------|---------------|
| **Title** | {max 60 chars} |
| **Meta Description** | {max 155 chars} |
| **OG Image** | {se aplicável} |
| **Loading** | {lazy load, suspense} |

---

## 6. Analytics (PostHog)

> **Nota:** Eventos customizados requerem implementação explícita.
> Pageviews e autocapture são automáticos após SDK init.

### Eventos Customizados
| Evento | Trigger | Properties |
|--------|---------|------------|
| `{page}_viewed` | Pageview (auto) | - |
| `{page}_cta_clicked` | Clique no CTA principal | `button_text`, `location` |
| `{ação_específica}` | {quando ocorre} | {dados relevantes} |

### Funis a Medir
- {Descrever funil se aplicável, ex: Wizard steps}

### Feature Flags (A/B)
- {Se houver variantes a testar}
```

---

### PASSO 5: Validar e Aprovar

**Gate de Saída:**

```
[ ] SHARED-LAYOUT.md criado (Header, Footer, Mobile Menu)
[ ] Priorização de páginas confirmada com usuário
[ ] PAGE-SPEC criado para cada página priorizada
[ ] Cada PAGE-SPEC referencia MASTER.md e CONTENT-STRATEGY
[ ] Estados (loading, empty, error) documentados onde aplicável
[ ] Responsividade descrita para cada página
[ ] **Analytics (PostHog) especificado para cada página**
[ ] Todas as PAGE-SPECs aprovadas pelo humano
```

> [!CAUTION]
> **BLOQUEADOR:** Não prosseguir para Breakdown sem PAGE-SPECs aprovados.

---

## 📋 CHECKLISTS POR TIPO DE PÁGINA

### Landing Page
- [ ] Hero Section (headline, subheadline, CTAs)
- [ ] Features/Benefits (cards ou grid)
- [ ] How it Works (steps)
- [ ] Social Proof (testimonials, logos, metrics)
- [ ] Pricing Preview (redirect para /pricing)
- [ ] FAQ Preview
- [ ] Final CTA

### Dashboard (Área Logada)
- [ ] Sidebar Navigation
- [ ] Top Bar (search, notifications, profile)
- [ ] Empty States para cada módulo
- [ ] Cards de resumo (KPIs)
- [ ] Actions disponíveis
- [ ] Mobile: Bottom nav ou drawer

### Wizard/Onboarding
- [ ] Progress indicator
- [ ] Each step layout
- [ ] Validação por step
- [ ] Navegação (back, next, skip)
- [ ] Final state (success)
- [ ] Exit points (onde usuário pode sair)

### Admin
- [ ] Sidebar diferenciada (badge "Admin")
- [ ] Módulos (Users, Billing, Content, Analytics)
- [ ] Tables com ações (view, edit, delete)
- [ ] Filtros e busca
- [ ] External links (Stripe, PostHog, Sanity)

---

## 🔴 REGRAS CRÍTICAS

1. **SEMPRE** criar SHARED-LAYOUT.md primeiro
2. **PERGUNTAR** priorização antes de criar todos os specs
3. **REFERENCIAR** MASTER.md e CONTENT-STRATEGY em cada spec
4. **DOCUMENTAR** todos os estados (loading, empty, error)
5. **VALIDAR** com usuário antes de prosseguir
6. **NÃO** duplicar copy - referenciar CONTENT-STRATEGY
