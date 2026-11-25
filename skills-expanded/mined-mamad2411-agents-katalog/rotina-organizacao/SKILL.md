---
name: "rotina-organizacao"
description: "Skills de produtividade pessoal com metodologias GTD, time blocking, gestão de energia e organização de projetos pessoais. Use quando precisar implementar sistema de tarefas, planejar agenda, criar checklists reutilizáveis, delegar eficazmente ou construir hábitos sustentáveis."
version: 1.0.0
license: MIT
tags:
  - produtividade
  - gtd
  - time-blocking
  - checklists
  - delegacao
  - organizacao
  - habitos
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read rotina-organizacao/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/rotina-organizacao.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Rotina, Tarefas & Organização (Nível PODEROSO)

Skills de produtividade pessoal e profissional para quem quer sair do caos e entrar num sistema que funciona. Metodologias GTD, time blocking, Pomodoro, Atomic Habits e frameworks de delegação — tudo adaptado à realidade brasileira: interrupções constantes, WhatsApp 24h, cultura de urgência e jornadas de trabalho que invadem a vida pessoal.

## Início Rápido

### Claude Code
```
/read rotina-organizacao/sistema-gtd/SKILL.md
/read rotina-organizacao/bloqueio-de-tempo/SKILL.md
/read rotina-organizacao/criador-de-checklists/SKILL.md
/read rotina-organizacao/delegacao/SKILL.md
/read rotina-organizacao/revisao-semanal/SKILL.md
/read rotina-organizacao/prioridades/SKILL.md
/read rotina-organizacao/caixa-de-entrada-zero/SKILL.md
/read rotina-organizacao/habitos/SKILL.md
/read rotina-organizacao/foco-e-trabalho-profundo/SKILL.md
/read rotina-organizacao/equilibrio-vida/SKILL.md
```

### Cursor
Adicione em `.cursor/rules/rotina-organizacao.md`:
```
Você é um coach de produtividade especializado no contexto brasileiro.
Metodologias: GTD, time blocking, Atomic Habits, princípio 80/20.
Considere realidade BR: WhatsApp sempre ligado, cultura de urgência, reuniões improdutivas.
Foco em sistemas simples e sustentáveis, não perfeccionismo.
```

### Codex
Inclua no `AGENTS.md`:
```
## Coach de Produtividade BR
Consulte rotina-organizacao/ para sistemas de tarefas, agenda, hábitos e delegação.
Priorize simplicidade e sustentabilidade. Considere a realidade da cultura BR.
```

## Visão Geral das Skills

| Skill | Pasta | Foco |
|-------|-------|------|
| Sistema GTD | `sistema-gtd/` | Getting Things Done adaptado ao Brasil |
| Bloqueio de Tempo | `bloqueio-de-tempo/` | Agenda com deep work e temas do dia |
| Criador de Checklists | `criador-de-checklists/` | Checklists, SOPs e rotinas repetíveis |
| Delegação | `delegacao/` | Frameworks de delegação para líderes |
| Revisão Semanal | `revisao-semanal/` | Revisão semanal completa |
| Prioridades | `prioridades/` | Eisenhower, RICE pessoal, 80/20 |
| Caixa de Entrada Zero | `caixa-de-entrada-zero/` | Gestão de email e notificações |
| Hábitos | `habitos/` | Atomic habits e habit stacking |
| Foco e Trabalho Profundo | `foco-e-trabalho-profundo/` | Pomodoro, deep work, sem distrações |
| Equilíbrio de Vida | `equilibrio-vida/` | Work-life balance e prevenção de burnout |

## Exemplos de Uso

### GTD System
```
Use gtd-system para implementar GTD na minha vida. Sou gestor de produto
em startup, tenho 3 projetos simultâneos e sinto que estou perdendo coisas
importantes. Me dê a configuração completa: caixas de coleta, listas, revisão
semanal e ferramentas para usar no Notion ou papel.
```

### Time Blocking
```
Use time-blocking para reorganizar minha agenda. Trabalho como dev freelancer,
tenho 3 clientes, reuniões espalhadas e nenhum tempo para deep work.
Meu horário: 9h às 18h. Me crie um modelo de semana com blocos de foco,
reuniões agrupadas e tempo de buffer para imprevistos.
```

### Checklist Builder
```
Use checklist-builder para criar meu SOP de onboarding de novos clientes
como consultor de marketing. Processo atual: 2 semanas de caos toda vez.
Quero um checklist completo do contrato assinado até o primeiro relatório
entregue, com responsável e prazo em cada etapa.
```

### Delegação
```
Use delegacao. Sou dono de uma agência com 8 pessoas mas faço tudo sozinho.
Me dê o framework Delegation Poker ou equivalente para mapear o que delegar,
como treinar a equipe e como criar sistemas de acompanhamento sem microgerenciar.
```

### Hábitos
```
Use habitos para criar minha rotina matinal. Quero implementar: exercício 30min,
leitura 20min e revisão de metas 10min. Já tentei 3 vezes e falho sempre
na segunda semana. Me dê estratégia de habit stacking, gatilhos e como
tornar esses hábitos a resistência mínima.
```

### Equilíbrio de Vida
```
Use equilibrio-vida. Trabalho 12h por dia, finais de semana incluídos,
nunca me desconecto do WhatsApp de trabalho e estou começando a ter
problemas de saúde. Me ajude a criar limites saudáveis sem prejudicar
meu negócio que fatura R$ 50k/mês.
```

## Contexto Brasileiro

### Desafios Únicos da Produtividade no Brasil

#### WhatsApp como Ferramenta de Trabalho
- Brasil é o país com maior uso de WhatsApp para trabalho no mundo
- Expectativa de resposta imediata cria ansiedade e interrupção constante
- Solução: status de ocupado, horários de resposta, separar grupos pessoais e profissionais
- Ferramentas: WhatsApp Business com horário de funcionamento, resposta automática

#### Cultura de Urgência Falsa
- "Para ontem" é expressão comum no ambiente corporativo BR
- Tudo parece urgente mas poucos itens são realmente importantes
- Matriz de Eisenhower + protocolo de triagem é essencial no contexto BR
- Estabelecer SLAs internos: o que respondo em 1h, 4h, 1 dia útil

#### Reuniões no Brasil
- Cultura de reunião longa sem pauta nem decisão é muito comum
- Reuniões começam tarde e excedem o tempo previsto
- Solução: agenda escrita antes, decisão documentada depois, blocos de reunião agrupados

#### Fuso Horário e Trabalho Remoto
- Brasil tem 4 fusos horários: UTC-5, UTC-4, UTC-3, UTC-2
- Equipes distribuídas: definir horário de sobreposição para sincronia
- Trabalho assíncrono por padrão, sincrônico apenas para decisões complexas

### Ferramentas de Produtividade Populares no Brasil
| Categoria | Ferramenta | Uso no BR |
|-----------|-----------|-----------|
| Tarefas/Projetos | Notion, Trello, Asana | Amplo uso |
| Tempo | Toggl, Clockify | Dev e freelancers |
| E-mail | Gmail (domina), Outlook | Corporativo |
| Comunicação | WhatsApp Business, Slack | Essencial |
| Notas | Notion, Obsidian, Evernote | Crescendo |
| Calendário | Google Calendar | Padrão de fato |
| Pomodoro | Forest App, Be Focused | Mobile |

### Legislação e Direitos Trabalhistas
- CLT limita jornada a 8h/dia e 44h/semana (horas extras regulamentadas)
- Trabalho remoto: direito à desconexão é tema crescente no Brasil
- LGPD: monitoramento de produtividade em home office tem restrições

## Configuração de Harness

### Claude Code — CLAUDE.md Global
Adicione ao seu `~/.claude/CLAUDE.md`:
```markdown
## Coach de Produtividade & Organização
Quando trabalhar em rotina, produtividade ou organização pessoal:
- Contexto BR: WhatsApp como ferramenta de trabalho, cultura de urgência, reuniões longas
- Metodologias: GTD, time blocking, Atomic Habits, Eisenhower, 80/20
- Priorizar simplicidade: sistemas que falham são os complexos demais
- Ferramentas: Google Calendar, Notion, Trello, WhatsApp Business como base BR
- Equilíbrio: CLT e direitos trabalhistas BR, direito à desconexão
```

### Cursor — .cursorrules
```
# Rotina & Produtividade BR
- Coach de produtividade com foco no contexto brasileiro
- Metodologias: GTD, time blocking, Atomic Habits, princípio 80/20
- Desafios BR: WhatsApp 24h, urgência cultural, reuniões sem pauta
- Ferramentas padrão BR: Google Calendar, Notion, WhatsApp Business
- Foco em sistemas simples e sustentáveis, resistentes a falhas humanas
- Hábitos: habit stacking, menor resistência possível, celebração de pequenas vitórias
```

### Codex — AGENTS.md
```markdown
## Produtividade & Organização Brasil

Especialização:
- Sistemas de gestão pessoal (GTD, time blocking, Eisenhower)
- Criação de hábitos sustentáveis (Atomic Habits, habit stacking)
- Frameworks de delegação para líderes e donos de negócio BR
- Gestão de comunicação digital (email, WhatsApp, notificações)

Contexto cultural BR:
- WhatsApp é ferramenta de trabalho principal — estratégia de gestão necessária
- Cultura de urgência falsa — triagem e SLAs internos são essenciais
- Reuniões: pauta obrigatória, decisão documentada, tempo cronometrado
```

## Regras

1. **Simplicidade primeiro:** Sistemas complexos não são mantidos. Sempre escolher a versão mais simples que funcione
2. **Contexto BR obrigatório:** Nunca ignorar o WhatsApp, a cultura de urgência e as reuniões longas ao criar sistemas
3. **GTD adaptado:** O GTD original foi criado para e-mail. Adaptar para WhatsApp, Slack e notificações móveis
4. **Hábitos progressivos:** Começar com versão mínima viável do hábito. Não otimizar prematuramente
5. **Delegação com sistema:** Nunca apenas "delegar". Sempre: responsável + prazo + critério de sucesso + checkin
6. **Revisão semanal não negociável:** É o coração de qualquer sistema de produtividade. Blocar na agenda
7. **Deep work protegido:** No mínimo 2h de foco ininterrupto por dia. Reuniões e notificações nesse período são proibidas
8. **Inbox Zero com triagem:** Email tratado como inbox, não arquivo. Ação imediata ou agendamento no mesmo momento
9. **Equilíbrio mensurável:** Work-life balance sem métricas não funciona. Definir indicadores concretos de saúde
10. **Carregue apenas o SKILL.md específico** da área que precisar para manter contexto focado e relevante
