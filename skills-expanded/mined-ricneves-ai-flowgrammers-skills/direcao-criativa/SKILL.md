---
name: "direcao-criativa"
description: "Skills para desenvolvimento de conceito criativo, direção de arte, naming, campanhas 360° e storytelling visual para marcas brasileiras. Use quando precisar criar conceitos de campanha, nomear produtos, estruturar narrativas de marca ou orientar produções criativas."
version: 1.0.0
license: MIT
tags:
  - criatividade
  - direcao-arte
  - campanha
  - storytelling
  - naming
  - conceito-criativo
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read /caminho/direcao-criativa/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no .cursorrules ou .cursor/rules/direcao-criativa.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Direção Criativa (Nível PODEROSO)

Skills para o desenvolvimento de conceito criativo, direção de arte, naming, campanhas integradas e storytelling visual voltados para o mercado brasileiro. De grandes ideias estratégicas até moodboards e roteiros, este domínio transforma posicionamento de marca em criatividade executável.

Ideal para diretores criativos, gerentes de marketing, fundadores e agências que precisam de estrutura para dar vida a campanhas com propósito e impacto no público brasileiro.

---

## Início Rápido

### Claude Code
```
/read /caminho/direcao-criativa/SKILL.md
> Desenvolva o conceito criativo de uma campanha de lançamento para um aplicativo de finanças pessoais voltado à Geração Z brasileira
```

### Cursor
Adicione ao `.cursor/rules/direcao-criativa.md` e use:
```
@direcao-criativa Preciso de 5 opções de naming para uma marca de cosméticos naturais focada no público afro-brasileiro
```

### Codex
Inclua no `AGENTS.md`:
```
Contexto criativo: use as diretrizes de direcao-criativa para tarefas que envolvam 
conceito de campanha, naming, storytelling visual e direção de arte.
```

### Windsurf
Em **Settings > AI Rules**, adicione o conteúdo de `SKILL.md` e então:
```
Com base nas skills de direcao-criativa, crie um moodboard textual e referências 
para uma campanha de Dia das Mães para varejo de moda feminina
```

---

## Visão Geral das Skills

| Skill | Pasta | Foco |
|-------|-------|------|
| Conceito Criativo | `conceito-criativo/` | Big idea e conceito central de campanha |
| Direção de Arte | `direcao-arte/` | Briefing e referências para direção de arte e produção visual |
| Naming | `naming/` | Naming de produtos, marcas e campanhas |
| Tagline | `tagline/` | Taglines, slogans e brand promises memoráveis |
| Campanha 360° | `campanha-360/` | Planejamento de campanha integrada multi-canal |
| Narrativa Visual | `narrativa-visual/` | Narrativa visual para marcas: arco, personagens, emoção |
| Moodboard | `moodboard/` | Criação de moodboards e referências para produções |
| Roteiro de Vídeo | `roteiro-video/` | Roteiro para vídeos publicitários, institucionais e de produto |
| Ideação | `ideacao/` | Facilitação de brainstorming e sessões criativas |
| Ativação de Marca | `ativacao-de-marca/` | Ativações de marca, experiências e eventos criativos |

---

## Exemplos de Uso

### Conceito Criativo
```
Nossa marca de cerveja artesanal "Raiz" quer uma campanha para o Dia do Trabalhador. 
Público: homens e mulheres de 28-45 anos, classe C/B, que valorizam autenticidade. 
Crie o conceito criativo com: big idea, território criativo, manifesto de 
100 palavras e exemplos de execução em 3 peças.
```

### Naming
```
Preciso de 10 opções de nome para uma startup de logística reversa sustentável 
(coleta e reciclagem de embalagens). Público B2B, grandes redes de varejo. 
Para cada nome: origem, significado, disponibilidade de .com.br e fit com o setor.
```

### Tagline
```
Nossa empresa de consultoria de RH se posiciona como "parceira estratégica de 
transformação cultural". Crie 8 opções de tagline: 4 racionais/diretas e 
4 emocionais/aspiracionais. Inclua uma análise do por que cada uma funciona.
```

### Campanha 360°
```
Planeje uma campanha de 60 dias para o lançamento de um plano odontológico 
para MEIs e autônomos. Budget estimado: R$ 150k. Canais disponíveis: 
digital, WhatsApp, rádio AM/FM. Inclua: conceito, cronograma, 
distribuição de budget e KPIs por canal.
```

### Roteiro de Vídeo
```
Crie o roteiro de um vídeo de 60 segundos para Instagram Reels de uma 
escola de inglês para adultos profissionais. Tom: inspirador, sem clichê 
de "fale inglês em 30 dias". Inclua: cenas, texto de locução, 
música sugerida e chamada para ação.
```

### Ideação
```
Facilite uma sessão de brainstorming para gerar 20 ideias de ativação de marca 
para uma empresa de alimentos saudáveis no evento Rock in Rio. 
Público: jovens 18-35 anos. Budget por ativação: R$ 30-80k. 
Use a técnica SCAMPER para expandir as ideias.
```

---

## Contexto Brasileiro

- **Sazonalidade BR**: Carnaval, Copa do Mundo, Dia das Mães (maior data do varejo), Dia dos Namorados, Dia dos Pais, Dia das Crianças, Black Friday e Natal — calendário criativo deve considerar estas datas
- **Diversidade e representatividade**: o público brasileiro é diverso; campanhas inclusivas performam melhor e evitam crises de reputação
- **Regionalismo**: linguagem e referências culturais variam muito entre Norte/Nordeste e Sul/Sudeste — considerar dialetos, expressões e referências locais
- **Conar**: Conselho Nacional de Autorregulamentação Publicitária estabelece limites para publicidade — sempre mencionar restrições para bebidas alcoólicas, alimentos ultraprocessados e publicidade infantil
- **Mídias locais**: rádio ainda é forte no interior BR; WhatsApp é canal de marketing relevante; TikTok cresceu aceleradamente em todas as faixas etárias
- **Referências visuais**: humor, afeto e família ressoam fortemente no imaginário brasileiro — explorar estes territórios com autenticidade
- **Orçamento real de mercado**: custos de produção BR variam muito; sempre orientar com faixas realistas (vídeo institucional: R$ 15k-150k; campanha digital: R$ 5k-500k/mês)

---

## Configuração de Harness

### Claude Code (CLAUDE.md)
```markdown
## Direção Criativa
Ao criar conceitos, campanhas ou naming:
- Use a skill direcao-criativa como estrutura de briefing
- Sempre perguntar: público, território emocional, orçamento e canais disponíveis
- Entregar múltiplas opções (mínimo 3) antes de aprofundar em uma direção
- Considerar contexto cultural brasileiro nas referências e linguagem
```

### Cursor (.cursorrules)
```
# Direção Criativa Rules
- Para naming: mínimo 5 opções com análise de cada uma
- Para conceitos: sempre incluir big idea + manifesto + execuções de exemplo
- Para roteiros: formato cena-por-cena com tempo estimado
- Adaptar todas as referências para o contexto cultural brasileiro
```

### Codex (AGENTS.md)
```markdown
## Agente de Direção Criativa
Especialidade: conceito criativo, naming, campanhas e storytelling para o mercado BR.
Entregar sempre múltiplas opções. Referenciar contexto cultural, datas comemorativas 
e regulamentações do CONAR quando relevante.
```

### Windsurf (AI Rules)
```
Direção Criativa: use as skills deste domínio para desenvolver conceitos de campanha,
naming, storytelling e direção de arte. Sempre adaptar para o contexto cultural 
e mercadológico brasileiro, considerando diversidade e regionalismo.
```

---

## Regras

1. **Big idea primeiro**: antes de qualquer execução, o conceito central (big idea) deve estar claro e aprovado — nunca pular para peças sem ancoragem conceitual
2. **Múltiplas opções**: entregar sempre no mínimo 3 opções de conceito, naming ou tagline — evitar a armadilha da primeira ideia
3. **Briefing antes de criar**: perguntar sempre: quem é o público? qual é a emoção central? quais canais? qual o orçamento? qual o prazo?
4. **Território emocional**: todo conceito precisa habitar um território emocional claro — não misturar humor com drama sem intenção estratégica
5. **Verificar disponibilidade de naming**: ao sugerir nomes, sempre incluir checklist de disponibilidade (.com.br, Instagram, INPI para marcas)
6. **CONAR em mente**: campanhas para bebidas alcoólicas, alimentos, produtos financeiros e público infantil têm restrições específicas — mencionar sempre
7. **Representatividade**: campanhas que excluem ou estereotipam grupos causam crises — orientar sobre diversidade e inclusão como padrão, não exceção
8. **Orçamento realista**: sempre ancoras sugestões criativas em orçamentos reais do mercado brasileiro
9. **Roteiros com tempo**: todo roteiro deve ter tempo estimado por cena e duração total — cena de 5 segundos é diferente de 15 segundos em produção
10. **Mensurabilidade**: toda campanha precisa de KPIs definidos antes da execução — criatividade sem métricas é arte, não negócio
