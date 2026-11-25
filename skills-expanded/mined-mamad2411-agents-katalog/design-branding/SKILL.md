---
name: "design-branding"
description: "Skills para identidade visual, criação de materiais de vendas, decks executivos e assets B2B com briefing para designers. Use quando precisar criar, revisar ou orientar projetos de design, branding, apresentações e materiais visuais para o mercado brasileiro."
version: 1.0.0
license: MIT
tags:
  - design
  - branding
  - identidade-visual
  - deck
  - materiais-vendas
  - figma
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read /caminho/design-branding/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no .cursorrules ou .cursor/rules/design-branding.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Design & Branding (Nível PODEROSO)

Skills para identidade visual, materiais de vendas, decks executivos e assets B2B voltados ao mercado brasileiro. Cobrindo desde o briefing inicial para designers e agências até a produção de apresentações estratégicas, brandbooks e orientações para Figma.

Este domínio transforma ideias de negócio em direção criativa estruturada, com linguagem acessível para fundadores, gestores de marketing e profissionais de design no Brasil.

---

## Início Rápido

### Claude Code
```
/read /caminho/design-branding/SKILL.md
> Crie um briefing completo de identidade visual para uma startup de saúde mental B2C
```

### Cursor
Adicione ao `.cursor/rules/design-branding.md` e use:
```
@design-branding Preciso de um one-pager para apresentar nossa solução SaaS para RH
```

### Codex
Inclua no `AGENTS.md`:
```
Contexto de design: use as diretrizes de design-branding para qualquer tarefa de materiais visuais, apresentações e identidade.
```

### Windsurf
Em **Settings > AI Rules**, adicione o conteúdo de `SKILL.md` e então:
```
Com base nas skills de design-branding, estruture um deck para captação de investimento Série A
```

---

## Visão Geral das Skills

| Skill | Pasta | Foco |
|-------|-------|------|
| Identidade Visual | `identidade-visual/` | Brand guidelines, paleta, tipografia, logo |
| Design de Pitch | `design-de-pitch/` | Estrutura e visual de pitch decks e apresentações executivas |
| Materiais de Vendas | `materiais-vendas/` | One-pager, proposta visual, folder e materiais B2B |
| Assets Redes Sociais | `assets-redes-sociais/` | Templates feed, stories, banners para redes sociais |
| Feedback de Design | `feedback-de-design/` | Feedback e direção em projetos de UI/UX e protótipos |
| Briefing de Logo | `briefing-de-logo/` | Briefing de logo e identidade para designers e agências |
| Manual de Marca | `manual-de-marca/` | Brandbook: aplicações de marca, tipografia, cores, restrições |
| Produção no Figma | `producao-no-figma/` | Organização e produção em Figma: componentes, auto-layout |
| Apresentação Slides | `apresentacao-slides/` | Slides executivos: estrutura, narrativa e visual |
| Briefing de Vídeo | `briefing-de-video/` | Briefing para vídeos institucionais e de produto |

---

## Exemplos de Uso

### Identidade Visual
```
Crie um briefing completo de identidade visual para uma fintech B2B chamada "VaultBR"
que atende pequenas empresas. Inclua: posicionamento, personalidade da marca,
diretrizes de cor, tipografia sugerida e exemplos de aplicação.
```

### Pitch Design
```
Preciso estruturar um pitch deck de 12 slides para captar R$ 2M em seed round.
A empresa é um marketplace de servicos para condomínios.
Dê a estrutura, o que vai em cada slide e dicas visuais.
```

### Materiais de Vendas
```
Crie um one-pager para nossa plataforma de gestão de frotas.
Público: gestores de logística de empresas com 10+ veículos.
Tom: profissional e direto. Formato: A4 para envio digital.
```

### Social Assets
```
Preciso de um plano de templates para Instagram de uma clínica odontológica premium.
Crie especificações para: post feed quadrado, stories e destaque de capa.
Inclua estrutura, hierarquia visual e paleta sugerida.
```

### Brand Book
```
Nossa startup tem logo e cores definidas. Crie a estrutura de um brandbook
completo com: usos corretos e incorretos do logo, variações, paleta com
códigos HEX/RGB/CMYK, tipografia principal e secundária, e tom de voz.
```

### Video Briefing
```
Crie um briefing para vídeo institucional de 90 segundos de uma escola de
programação para mulheres. Inclua: objetivo, público, mensagem central,
tom, referências de estilo e roteiro em cenas.
```

---

## Contexto Brasileiro

- **Mercado local**: referências visuais do mercado brasileiro — cores vibrantes são bem aceitas em B2C, mas B2B tende ao conservador
- **Plataformas dominantes**: Instagram, LinkedIn, WhatsApp; priorize formatos 1:1 (feed), 9:16 (stories/reels) e 16:9 (apresentações)
- **Ferramentas populares**: Figma (design colaborativo), Canva (PMEs), PowerPoint/Google Slides (apresentações corporativas)
- **LGPD**: impacta uso de imagens de pessoas; sempre orientar sobre direitos de uso de fotos e ilustrações
- **Impressão**: quando indicar cores, sempre incluir CMYK para materiais impressos — o mercado gráfico BR ainda usa muito offset
- **Concorrência regional**: benchmarks devem incluir players nacionais além dos internacionais

---

## Configuração de Harness

### Claude Code (CLAUDE.md)
```markdown
## Design & Branding
Ao criar materiais visuais, briefings ou apresentações:
- Use a skill design-branding como referência de estrutura
- Adapte para o contexto B2B ou B2C conforme o projeto
- Inclua sempre especificações técnicas (dimensões, formatos, resoluções)
- Considere o mercado brasileiro nas sugestões de cor e tipografia
```

### Cursor (.cursorrules)
```
# Design & Branding Rules
- Para briefings de design: siga a estrutura da skill design-branding
- Sempre perguntar: público, plataforma, tom, referências
- Entregar especificações técnicas completas
- Adaptar ao nível de maturidade de design do cliente
```

### Codex (AGENTS.md)
```markdown
## Agente de Design & Branding
Especialidade: materiais visuais, identidade, apresentações e briefings para o mercado BR.
Ao receber tarefas de design: estruture primeiro o briefing, depois a entrega.
```

### Windsurf (AI Rules)
```
Design & Branding: use as skills deste domínio para estruturar briefings,
criar especificações visuais e orientar produções criativas no contexto brasileiro.
```

---

## Regras

1. **Sempre perguntar o contexto** antes de criar: público-alvo, plataforma de uso, tom da marca e concorrentes de referência
2. **Especificações técnicas primeiro**: dimensões, resolução, formato de arquivo são obrigatórios em qualquer entrega
3. **Separar briefing de execução**: o agente orienta e especifica; a execução pixel a pixel é do designer humano ou ferramenta dedicada
4. **Tom adaptado ao cliente**: agências recebem briefings técnicos; fundadores recebem linguagem acessível com exemplos visuais referenciados
5. **Incluir referências nacionais**: sempre misturar referências BR com internacionais para ancoragem de mercado
6. **Validar contra o negócio**: qualquer decisão visual deve ter justificativa de negócio, não apenas estética
7. **LGPD em imagens**: orientar sobre direitos de uso de fotos e ilustrações de pessoas em materiais comerciais
8. **Versões por canal**: materiais precisam de adaptações específicas para cada canal — nunca usar o mesmo arquivo em todos os lugares
9. **Acessibilidade**: mencionar contraste mínimo (WCAG AA: 4.5:1) em materiais digitais
10. **Iteração rápida**: entregar uma versão enxuta primeiro, depois expandir — evitar paralisia por excesso de opções
