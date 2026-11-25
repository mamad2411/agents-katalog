---
name: frontend-design
description: "Design intencional para CRIAR HTML, dashboards, relatórios e páginas visuais que fujam do genérico. Use ao gerar qualquer artefato visual (export_html, save_html) que precise parecer profissional e memorável, não um template padrão."
when_to_use: "Sempre que o turno for CRIAR um artefato HTML/dashboard/relatório visual e a aparência importar (evitar o genérico que só copia o CSS da interface)."
version: 1.0.0
author: Sentury
license: MIT
category: creative
family: artifacts
priority: 70
tags: [design, UI, UX, HTML, frontend, layout, tipografia, cores, responsivo]
tools_used: [executar_python, generate_chart]
related_skills: [concept-diagrams]
platforms: [linux, macos, windows]
dependencies: []
---

# Frontend Design — Guia para o Sentury

Use esta skill quando o usuário pedir exports HTML, dashboards visuais, relatórios formatados ou qualquer artefato visual que precise ter aparência profissional e intencional.

## NO SENTURY: ESCREVA o HTML você mesmo (não use o template)

> **CRÍTICO:** gere o HTML via `executar_python` (`save_html('nome.html', '''<html>...</html>''')`),
> aplicando estes princípios. **NÃO use `export_html`** — é um template FIXO que ignora
> este design e devolve um dashboard genérico. HTML auto-contido (CSS inline), com os
> NÚMEROS REAIS da análise. Siga as diretrizes abaixo pra não ficar genérico.

---

## Princípios de Design

### 0. Comprometa-se com UMA direção
Antes de qualquer coisa, escolha **uma** direção estética coerente com o assunto (ex.: "editorial sóbrio", "dashboard denso e técnico", "one-pager executivo de alto contraste") e **execute-a com precisão**. Metade de um estilo + metade de outro = genérico. Decida a direção, declare-a numa frase, e derive cada escolha (tipografia, cor, espaçamento, motion) dela.

### 1. Fundamente no assunto
Antes de estilizar, identifique:
- **O que** é o conteúdo (relatório, dashboard de indicadores, plano de ação, página de produto)
- **Quem** vai ler (quem executa, quem decide, quem só consulta)
- **Qual** é o objetivo da página (informar, convencer, alertar)

O assunto dita as escolhas visuais. Um relatório de risco usa cores sóbrias e hierarquia clara. Um dashboard de conquistas usa contraste e destaque positivo.

### 2. Tipografia carrega personalidade
- **Títulos:** Use fontes display com personalidade (não sempre Inter/Arial)
- **Corpo:** Use fontes legíveis e complementares ao display
- **Escala:** Defina uma escala clara de tamanhos com pesos intencionais
- **Google Fonts recomendadas para relatórios e produtos:**
  - Display: `Outfit`, `DM Sans`, `Plus Jakarta Sans`
  - Corpo: `Inter`, `Source Sans 3`, `Nunito Sans`

### 3. Estrutura é informação
- Dispositivos estruturais (numeração, separadores, labels) devem **codificar algo real** sobre o conteúdo, não decorar
- Números sequenciais (01/02/03) só fazem sentido se o conteúdo é uma sequência real
- Seções devem ter hierarquia visual clara: título → subtítulo → dado → detalhe

### 4. Cor com propósito
- **Nunca use cor sem significado.** Cada cor deve comunicar algo: categoria, direção (positivo/negativo), intensidade
- **Paleta limitada:** 4-6 cores nomeadas por função
  - `--cor-positivo`: verde (#10B981)
  - `--cor-negativo`: vermelho (#EF4444)
  - `--cor-neutro`: cinza (#6B7280)
  - `--cor-destaque`: azul (#3B82F6)
  - `--cor-alerta`: âmbar (#F59E0B)
  - `--cor-fundo`: branco (#FFFFFF) ou escuro (#1F2937)
- **Acessibilidade:** Nunca use vermelho/verde sozinhos para codificar bom/ruim (8% dos homens são daltônicos). Use azul/laranja como par seguro

### 5. Motion com intenção
- Animações servem para **guiar o olhar**, não para decorar
- Uma animação orquestrada (fade-in sequencial das seções) é melhor que efeitos espalhados
- Respeite `prefers-reduced-motion`

### 6. Restraint — menos é mais
- Gaste a ousadia em **um elemento memorável** e mantenha o resto disciplinado
- Antes de finalizar: remova um elemento decorativo. Se o design sobrevive, ele era desnecessário
- Responsivo: 375px, 768px, 1024px, 1440px

---

## Anti-Padrões a Evitar

| Evitar | Preferir |
|---|---|
| Fundo creme genérico (#F4F1EA) com serif | Paleta específica ao assunto |
| Fundo preto com acento verde-ácido | Contraste calculado por contexto |
| Layout broadsheet com regras hairline | Hierarquia clara com whitespace |
| Gradiente roxo/rosa "AI slop" | Cores semânticas com propósito |
| Inter em tudo | Tipografia pareada e intencional |
| Emojis como ícones | SVG icons (Lucide, Heroicons) |

---

## Checklist Pré-Entrega

- [ ] Contraste de texto ≥ 4.5:1 (WCAG AA)
- [ ] `cursor: pointer` em todos os elementos clicáveis
- [ ] Hover states com transição suave (150-300ms)
- [ ] Focus states visíveis para navegação por teclado
- [ ] `prefers-reduced-motion` respeitado
- [ ] Responsivo: testado em 375px, 768px, 1024px, 1440px
- [ ] Sem emojis como ícones (use SVG)
- [ ] Título diz o **achado**, não o nome da variável

---

## Processo de Criação

1. **Antes de codificar:** Defina paleta (4-6 hex), tipografia (display + corpo), layout concept, e o elemento-assinatura
2. **Auto-critique:** Revise se suas escolhas são específicas para este briefing ou genéricas
3. **Codifique:** Seguindo o plano, derivando cada decisão dele
4. **Valide:** Teste do 5 segundos — alguém entende o ponto principal em 5 segundos?
