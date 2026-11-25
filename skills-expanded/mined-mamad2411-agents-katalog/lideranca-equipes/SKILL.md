---
name: "lideranca-equipes"
description: "Skills para gestão de pessoas, feedback estruturado, desenvolvimento de times e liderança em contexto de startups e PMEs brasileiras. Use quando precisar de frameworks de feedback, estruturar 1:1s, resolver conflitos, desenvolver cultura de equipe ou fazer a transição para liderança."
version: 1.0.0
license: MIT
tags:
  - lideranca
  - equipes
  - feedback
  - delegacao
  - gestao-pessoas
  - okr
  - cultura
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read /caminho/lideranca-equipes/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no .cursorrules ou .cursor/rules/lideranca-equipes.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Liderança & Equipes (Nível PODEROSO)

Skills práticas para gestão de pessoas, feedback estruturado, desenvolvimento de times e liderança no contexto de startups e PMEs brasileiras. De conversas difíceis a PDIs, de segurança psicológica a times remotos — cobrindo os desafios reais de quem lidera no Brasil.

Este domínio é voltado para líderes de primeira viagem, gestores intermediários e founders que precisam estruturar sua liderança sem manual de RH de multinacional.

---

## Início Rápido

### Claude Code
```
/read /caminho/lideranca-equipes/SKILL.md
> Preciso estruturar um feedback difícil para um desenvolvedor sênior que está entregando abaixo do esperado há 2 sprints. Use o framework SBI.
```

### Cursor
Adicione ao `.cursor/rules/lideranca-equipes.md` e use:
```
@lideranca-equipes Crie um template de reunião 1:1 semanal para gestores de produto
```

### Codex
Inclua no `AGENTS.md`:
```
Contexto de liderança: use as diretrizes de lideranca-equipes para tarefas 
que envolvam gestão de pessoas, feedback, cultura e desenvolvimento de times.
```

### Windsurf
Em **Settings > AI Rules**, adicione o conteúdo de `SKILL.md` e então:
```
Com base nas skills de lideranca-equipes, crie um programa de reconhecimento 
para um time de 8 pessoas em startup early-stage sem budget para bônus financeiros
```

---

## Visão Geral das Skills

| Skill | Pasta | Foco |
|-------|-------|------|
| Feedback Estruturado | `feedback-estruturado/` | Feedback 1:1 com SBI, feedforward e frameworks |
| Reunião Individual | `reuniao-individual/` | Preparação e condução de reuniões 1:1 eficazes |
| Gestão de Conflitos | `gestao-conflitos/` | Resolução de conflitos e mediação em times |
| Cultura Psicológica | `cultura-psicologica/` | Segurança psicológica, diversidade e inclusão |
| Reconhecimento | `reconhecimento/` | Programas de reconhecimento e engajamento |
| Desenvolvimento de Time | `desenvolvimento-time/` | PDIs, trilhas de desenvolvimento e planos de carreira |
| Remoto e Híbrido | `remoto-hibrido/` | Gestão de times remotos e híbridos |
| Reunião Eficaz | `reuniao-eficaz/` | Facilitação de reuniões produtivas |
| Líder Técnico | `lider-tecnico/` | Transição de especialista para líder técnico/manager |
| Time Pequeno | `time-pequeno/` | Gestão de times de 2-15 pessoas em startups e PMEs BR |

---

## Exemplos de Uso

### Feedback Estruturado
```
Preciso dar feedback para minha analista de marketing que está produzindo conteúdo 
de boa qualidade mas perde prazos constantemente. Use o framework SBI 
(Situação-Comportamento-Impacto) e inclua também um feedforward 
com próximos passos concretos.
```

### One-on-One
```
Sou líder de engenharia de software e tenho 1:1s semanais com 5 devs. 
As reuniões estão se tornando status reports chatos. Crie um template 
de 1:1 de 30 minutos que realmente desenvolva as pessoas e mantenha 
o engajamento, com perguntas abertas e espaço para carreira.
```

### Gestão de Conflitos
```
Dois colaboradores da minha equipe de vendas estão em conflito aberto 
por causa de divisão de território de clientes. O clima está afetando 
o time todo. Como mediador, como devo conduzir a conversa? 
Crie um roteiro de mediação em 3 etapas.
```

### Desenvolvimento de Time
```
Tenho uma desenvolvedora pleno que quer chegar a sênior em 18 meses. 
Crie um PDI (Plano de Desenvolvimento Individual) com: competências 
a desenvolver, atividades práticas, recursos de aprendizagem e 
marcos de avaliação bimestrais.
```

### Remoto e Híbrido
```
Minha startup tem 12 pessoas: 6 no escritório em SP, 4 remote-first 
em outras cidades e 2 em fuso diferente (RJ e Recife). 
Crie um playbook de trabalho híbrido com: rituais de time, 
ferramentas, normas de comunicação e como preservar a cultura.
```

### Líder Técnico
```
Fui promovido a tech lead de uma equipe de 6 devs há 3 meses. 
Ainda codifico 60% do tempo e me sinto culpado quando não entrego código. 
Como faço essa transição? Crie um plano de 90 dias para me tornar 
um líder técnico eficaz sem abandonar minha identidade técnica.
```

---

## Contexto Brasileiro

- **CLT e vínculos empregatícios**: feedbacks negativos documentados têm relevância jurídica no Brasil — sempre orientar sobre registro e comunicação formal
- **Cultura hierárquica**: o ambiente corporativo brasileiro tende a ser mais hierárquico que o americano; feedback direto pode ser percebido como desrespeitoso — adaptar linguagem
- **Comunicação indireta**: brasileiros frequentemente comunicam insatisfação de forma indireta; líderes precisam desenvolver escuta ativa aguçada
- **Benefícios como cultura**: VR/VA, convênio médico e odontológico são partes do pacote esperado — programas de reconhecimento não financeiro têm ainda mais impacto
- **Diversidade regional**: times com pessoas de diferentes regiões têm diferenças culturais reais (ritmo de trabalho, comunicação, feriados) — abordar explicitamente
- **Mercado de trabalho tech**: alta rotatividade em tech BR; desenvolvimento de carreira e aprendizado são os principais fatores de retenção além de salário
- **Legislação trabalhista**: PLR, banco de horas, home office (Lei 14.442/2022) e férias têm regras específicas — sempre mencionar quando relevante
- **Saúde mental no trabalho**: tema crescente no Brasil pós-pandemia; síndrome de burnout é reconhecida como doença ocupacional pelo CID-11/OMS desde 2022

---

## Configuração de Harness

### Claude Code (CLAUDE.md)
```markdown
## Liderança & Equipes
Ao lidar com tarefas de gestão de pessoas:
- Use a skill lideranca-equipes para estrutura e frameworks
- Adaptar linguagem ao contexto brasileiro (hierarquia, comunicação indireta, CLT)
- Para feedbacks: sempre usar framework estruturado (SBI, STAR, etc.)
- Mencionar implicações de CLT quando relevante para decisões de gestão
```

### Cursor (.cursorrules)
```
# Liderança & Equipes Rules
- Para feedbacks: usar framework SBI ou equivalente estruturado
- Para 1:1s: perguntas abertas, foco em carreira e desenvolvimento, não apenas status
- Para conflitos: abordagem mediadora, nunca parcial
- Adaptar tudo ao contexto cultural brasileiro
```

### Codex (AGENTS.md)
```markdown
## Agente de Liderança e Equipes
Especialidade: gestão de pessoas, feedback, cultura e desenvolvimento em startups/PMEs BR.
Sempre adaptar frameworks internacionais (OKR, SBI, PDI) para o contexto brasileiro.
Mencionar implicações de CLT e cultura hierárquica brasileira quando pertinente.
```

### Windsurf (AI Rules)
```
Liderança & Equipes: use as skills deste domínio para gestão de pessoas, feedback,
desenvolvimento de times e liderança no contexto de startups e PMEs brasileiras.
Sempre considerar a cultura hierárquica BR e implicações da CLT.
```

---

## Regras

1. **Framework antes de improvisação**: todo feedback, conflito ou conversa difícil deve ter um framework estruturado (SBI, SCARF, STAR) — jamais improvisar em situações delicadas
2. **Documentar sempre**: no contexto brasileiro com CLT, conversas sobre desempenho, advertências e acordos de melhoria devem ser documentadas formalmente
3. **Adaptar ao contexto cultural**: frameworks americanos de feedback direto precisam de tradução para a cultura brasileira — suavizar sem perder a substância
4. **Separar pessoa de comportamento**: feedback é sobre comportamentos observáveis e seus impactos — nunca sobre personalidade ou caráter
5. **Desenvolvimento como retenção**: no mercado tech brasileiro, PDI e perspectiva de carreira são tão importantes quanto salário — tratar como prioridade estratégica
6. **Times remotos precisam de mais estrutura**: rituais, normas de comunicação e check-ins frequentes são mais importantes remotamente — nunca assumir que o time se organiza sozinho
7. **Escuta antes de solução**: ao lidar com conflitos ou problemas de desempenho, entender o contexto completo antes de propor qualquer solução
8. **OKRs com contexto**: ao implementar OKRs em PMEs, simplificar radicalmente — PME com 15 pessoas não precisa do mesmo rigor de OKR de uma empresa com 500
9. **Saúde mental em pauta**: normalizar conversas sobre carga de trabalho, estresse e bem-estar — líderes que ignoram este tema perdem os melhores talentos
10. **Modelo de transição para liderança**: novos líderes precisam de 90 dias de adaptação — não cobrar resultados de gestão do dia 1; criar um plano de transição explícito
