---
name: component-library-discovery
description: Descoberta de componentes UI de bibliotecas externas (badtz-ui, uselayouts, lucide-animated). Tabelas por contexto + perguntas interativas.
---

# Component Library Discovery

Skill para descobrir e selecionar componentes de bibliotecas UI externas compatíveis com shadcn/React projects.

## 📚 Bibliotecas Suportadas

| Biblioteca | Foco | Instalação |
|------------|------|------------|
| **badtz-ui** | Landing Pages, conversão | `npx shadcn@latest add https://badtz-ui.com/r/<comp>.json` |
| **uselayouts** | Micro-interações, animações | `npx shadcn@latest add https://uselayouts.com/r/<comp>` |
| **lucide-animated** | Ícones animados (350+) | Copy-paste |

---

## 🎯 PASSO 1: Tabela por Contexto

### Landing Pages (badtz-ui)

| Seção | Componente | Comando |
|-------|------------|---------|
| Hero | `hero-section` | `npx shadcn@latest add https://badtz-ui.com/r/hero-section.json` |
| CTA Button | `glowing-button` | `npx shadcn@latest add https://badtz-ui.com/r/glowing-button.json` |
| Pricing | `pricing-card` | `npx shadcn@latest add https://badtz-ui.com/r/pricing-card.json` |
| Testimonials | `testimonial-card` | `npx shadcn@latest add https://badtz-ui.com/r/testimonial-card.json` |
| Features | `feature-card` | `npx shadcn@latest add https://badtz-ui.com/r/feature-card.json` |
| FAQ | `accordion-faq` | `npx shadcn@latest add https://badtz-ui.com/r/accordion-faq.json` |
| Footer | `footer-section` | `npx shadcn@latest add https://badtz-ui.com/r/footer-section.json` |
| Logo Cloud | `logo-cloud` | `npx shadcn@latest add https://badtz-ui.com/r/logo-cloud.json` |
| Stats | `stats-section` | `npx shadcn@latest add https://badtz-ui.com/r/stats-section.json` |

### Micro-interações (uselayouts)

| Efeito | Componente | Comando |
|--------|------------|---------|
| Card 3D | `3d-book` | `npx shadcn@latest add https://uselayouts.com/r/3d-book` |
| Card Flip | `flip-card` | `npx shadcn@latest add https://uselayouts.com/r/flip-card` |
| Magnetic Button | `magnetic-button` | `npx shadcn@latest add https://uselayouts.com/r/magnetic-button` |
| Stagger List | `stagger-list` | `npx shadcn@latest add https://uselayouts.com/r/stagger-list` |
| Text Reveal | `text-reveal` | `npx shadcn@latest add https://uselayouts.com/r/text-reveal` |
| Blur Fade | `blur-fade` | `npx shadcn@latest add https://uselayouts.com/r/blur-fade` |

### Ícones Animados (lucide-animated)

| Contexto | Ícones Recomendados |
|----------|---------------------|
| **Loading** | `loader-pinwheel`, `refresh-cw`, `hourglass`, `loader` |
| **Success** | `check`, `check-check`, `circle-check`, `badge-check` |
| **Error** | `x`, `circle-x`, `ban`, `alert-triangle` |
| **Notifications** | `bell`, `mail-check`, `message-circle`, `inbox` |
| **User Actions** | `heart`, `bookmark`, `star`, `thumbs-up` |
| **Navigation** | `arrow-right`, `chevron-down`, `menu`, `search` |
| **Media** | `play`, `pause`, `volume`, `mic` |
| **Settings** | `settings`, `cog`, `sliders-horizontal` |

**Como usar lucide-animated:**
1. Acesse https://lucide-animated.com/
2. Pesquise o ícone desejado
3. Clique no ícone para ver código
4. Copie e cole no seu componente

---

## 🤔 PASSO 2: Perguntas Interativas

**Se o usuário não souber qual componente usar, fazer estas perguntas:**

```markdown
## 🔍 Descoberta de Componente

Para recomendar o melhor componente, preciso saber:

1. **Qual é o contexto?**
   - [ ] Landing Page (hero, pricing, testimonials)
   - [ ] Dashboard (cards, charts, stats)
   - [ ] Formulários (inputs, selects, validation)
   - [ ] Navegação (menu, sidebar, tabs)
   - [ ] Feedback (loading, success, error)
   - [ ] Outro: _________

2. **Precisa de animação?**
   - [ ] Sim, animação suave (micro-interações)
   - [ ] Sim, atenção especial (destaque)
   - [ ] Não, estático está ok

3. **É um ícone ou componente completo?**
   - [ ] Ícone
   - [ ] Componente/Seção
```

**Após respostas, retornar:**

```markdown
## 💡 Recomendação

Para **[contexto]** com **[animação]**, recomendo:

| Opção | Biblioteca | Componente | Motivo |
|-------|------------|------------|--------|
| A | [lib] | [comp] | [porque] |
| B | [lib] | [comp] | [alternativa] |

**Comando para instalar opção A:**
\`\`\`bash
npx shadcn@latest add [url]
\`\`\`
```

---

## 🔗 PASSO 3: Catálogos Completos

Se as tabelas acima não tiverem o que o usuário precisa:

> **📚 Catálogos Completos:**
> - [badtz-ui.com/docs](https://badtz-ui.com/docs) - Todos os componentes para LPs
> - [uselayouts.com/docs](https://uselayouts.com/docs/introduction) - Todas as micro-interações
> - [lucide-animated.com](https://lucide-animated.com) - Todos os 350+ ícones animados

---

## 🔄 Uso em Workflows

Esta skill pode ser invocada em:

| Workflow | Quando |
|----------|--------|
| `/new-project` | Phase 5.3 (UI Styling) - PASSO 4.6 |
| `/new-task` | Quando adicionar componentes UI |
| `/legacy-project` | Ao modernizar UI existente |
| `/ui-ux-pro-max` | Após gerar Design System |

**Invocação:**
```markdown
> [!TIP]
> **Skill:** `component-library-discovery`
> Consultar para encontrar componentes premium de bibliotecas externas.
```

---

## ⚠️ Pré-requisitos

1. **shadcn/ui inicializado** - As bibliotecas usam o registry do shadcn
2. **Tailwind CSS** - Todas dependem de Tailwind
3. **React 18+** - Compatibilidade com hooks modernos
4. **Framer Motion** (para uselayouts) - Instalar se usar micro-interações:
   ```bash
   npm install framer-motion
   ```
