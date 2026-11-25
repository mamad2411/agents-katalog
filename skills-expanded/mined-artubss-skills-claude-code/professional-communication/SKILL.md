---
name: professional-communication
description: Guia de comunicação técnica para desenvolvedores de software. Aborda estrutura de email, etiqueta de mensagens em equipe, agendas de reunião e adaptação de mensagens para públicos técnicos e não técnicos. Use ao redigir mensagens profissionais, preparar comunicações de reunião ou melhorar a comunicação escrita.
allowed-tools: Read, Glob, Grep
---

# Comunicação Profissional

## Visão Geral

Esta habilidade fornece frameworks e orientações para comunicação profissional eficaz em contextos de desenvolvimento de software. Seja escrevendo um email para stakeholders, redigindo uma mensagem de chat em equipe ou preparando agendas de reunião, esses princípios ajudam você a comunicar com clareza e construir credibilidade profissional.

**Princípio central:** Comunicação eficaz não se trata de provar quanto você sabe - trata-se de garantir que sua mensagem seja recebida e compreendida.

## Quando Usar Esta Habilidade

Use esta habilidade quando:

- Escrever emails para colegas, gerentes ou stakeholders
- Redigir mensagens de chat em equipe ou comunicações assíncronas
- Preparar agendas ou resumos de reunião
- Traduzir conceitos técnicos para públicos não técnicos
- Estruturar atualizações de status ou relatórios
- Melhorar a clareza da comunicação escrita

**Palavras-chave**: email, chat, teams, slack, discord, mensagem, escrita, comunicação, reunião, agenda, atualização de status, relatório

## Frameworks Principais

### A Estrutura O Que-Por Que-Como

Use este framework universal para organizar qualquer mensagem profissional:

| Componente | Propósito | Exemplo |
| --- | --- | --- |
| **O que** | Declare o tópico/pedido com clareza | "Precisamos atrasar o lançamento em uma semana" |
| **Por que** | Explique o raciocínio | "Bug crítico encontrado no processamento de pagamentos" |
| **Como** | Delineie próximos passos/itens de ação | "QA retestará até quinta; vou atualizar stakeholders na sexta" |

**Aplique a**: Emails, atualizações de status, pontos de discussão de reunião, explicações técnicas

### Três Regras de Ouro para Comunicação Escrita

1. **Comece com um assunto/propósito claro** - Os destinatários devem entender imediatamente do que se trata sua mensagem
2. **Use bullets, headlines e formatação navegável** - Ninguém quer um parágrafo contínuo
3. **Mensagens-chave primeiro** - Pessoas ocupadas apreciam eficiência; declare seu ponto principal de antemão

### Calibragem de Público

Antes de se comunicar, faça a si mesmo estas perguntas:

1. **Para quem** você está escrevendo? (Pares técnicos, gerentes, stakeholders, clientes)
2. **Que nível de detalhe** eles precisam? (Visão geral de alto nível vs detalhes de implementação)
3. **Qual é o valor** para eles? (Como isso afeta o trabalho/decisões deles?)

## Melhores Práticas de Email

### Fórmula para Linha de Assunto

| Em vez de | Tente |
| --- | --- |
| "Atualizações do projeto" | "Projeto X: Atualização de Status e Próximos Passos" |
| "Pergunta" | "Pergunta rápida: abordagem de rate limiting de API" |
| "FYI" | "FYI: Deployment agendado para terça 15h" |

### Template de Estrutura de Email

```markdown
**Assunto:** [Projeto/Tópico]: [Propósito Específico]

Olá [Nome],

[1-2 frases declarando o ponto-chave ou pedido de antemão]

**Contexto/Background:**
- [Bullet point 1]
- [Bullet point 2]

**O que eu preciso de você:**
- [Ação ou decisão específica necessária]
- [Prazo, se aplicável]

[Opcional: Breve próximos passos ou plano de acompanhamento]

Atenciosamente,
[Seu nome]
```

### Tipos Comuns de Email

| Tipo | Elementos-Chave |
| --- | --- |
| **Atualização de Status** | Resumo de progresso, bloqueadores, próximos passos, timeline |
| **Pedido** | Solicitação clara, contexto, prazo, por que importa |
| **Escalação** | Resumo da questão, impacto, soluções tentadas, decisão necessária |
| **FYI/Anúncio** | O que mudou, quem é afetado, qualquer ação necessária |

**Para templates**: Ver `references/email-templates.md`

## Etiqueta de Mensagens em Equipe

> **Nota:** Exemplos usam terminologia Slack, mas esses princípios se aplicam igualmente a Microsoft Teams, Discord ou qualquer plataforma de mensagens em equipe.

### Quando Usar Chat vs Email

| Use Chat | Use Email |
| --- | --- |
| Perguntas rápidas com respostas curtas | Documentação detalhada que precisa de registros |
| Coordenação em tempo real | Comunicações formais para stakeholders |
| Discussões informais em equipe | Mensagens que requerem revisão cuidadosa |
| Atualizações urgentes | Explicações complexas com múltiplas partes |

### Melhores Práticas de Mensagens em Equipe

1. **Use threads** - Mantenha canais principais navegáveis; respostas vão em threads
2. **@mention com propósito** - Não notifique pessoas desnecessariamente
3. **Organização de canais** - Canal certo para tópico certo
4. **Seja direto** - "Você pode revisar meu PR?" supera "Oi, você está ocupado?"
5. **Amigável a async** - Escreva mensagens que não requerem resposta imediata

### O Princípio "Sem Olá"

Em vez de:

```text
Você: Oi
Você: Você está aí?
Você: Posso fazer uma pergunta?
[esperando...]
```

Tente:

```text
Você: Oi Sarah - pergunta rápida sobre o script de deployment.
     Recebendo um erro de permissão na linha 42. Você já viu isso antes?
     Aqui está o erro: [colar erro]
```

## Comunicação Técnica vs Não-Técnica

### Quando Ser Técnico vs Acessível

| Público | Abordagem |
| --- | --- |
| **Pares em engenharia** | Detalhes técnicos, exemplos de código, especificidades de arquitetura |
| **Gerentes técnicos** | Equilíbrio entre detalhe e impacto de alto nível |
| **Stakeholders não técnicos** | Impacto nos negócios, analogias, resultados sobre implementação |
| **Clientes** | Linguagem clara, o que significa para eles, evitar jargão |

### Três Estratégias para Simplificação

1. **Comece com a visão geral antes dos detalhes** - As pessoas processam "por que" antes de "como"
2. **Simplifique sem perder precisão** - Use analogias; substitua jargão por linguagem clara
3. **Saiba quando mudar** - Leia o ambiente; ajuste com base em perguntas e engajamento

### Exemplos de Tradução de Jargão

| Técnico | Linguagem Clara |
| --- | --- |
| "Arquitetura de microserviços" | "Nosso sistema é dividido em peças menores e independentes que podem escalar separadamente" |
| "Processamento de mensagens assíncrono" | "Tarefas são enfileiradas e processadas em background" |
| "Pipeline de CI/CD" | "Processo automatizado que testa e faz deploy do nosso código" |
| "Migração de banco de dados" | "Atualizar como nossos dados são organizados e armazenados" |

**Para mais exemplos**: Ver `references/jargon-simplification.md`

## Princípios de Clareza na Escrita

### Voz Ativa em vez de Passiva

A voz ativa é mais clara, mais direta e transmite autoridade:

| Passiva (evite) | Ativa (prefira) |
| --- | --- |
| "Um bug foi identificado pela equipe" | "A equipe identificou um bug" |
| "A feature será implementada" | "Vamos implementar a feature" |
| "Erros foram encontrados durante testes" | "Os testes revelaram erros" |

### Elimine Palavras de Preenchimento

| Em vez de | Use |
| --- | --- |
| "Neste momento em tempo" | "Agora" |
| "No evento em que" | "Se" |
| "Devido ao fato de que" | "Porque" |
| "A fim de" | "Para" |
| "Eu apenas queria verificar se" | "Você pode" |

### O Teste "E Daí?"

Depois de escrever, pergunte: "E daí? Por que isso importa para o leitor?"

Se você não consegue responder com clareza, reestruture sua mensagem para começar com o valor/impacto.

## Comunicação de Reunião

### Antes: Melhores Práticas de Agenda

Todo convite de reunião deve incluir:

1. **Objetivo claro** - O que será realizado?
2. **Itens da agenda** - Tópicos a cobrir com estimativas de tempo
3. **Preparação necessária** - O que os participantes devem trazer/revisar?
4. **Resultado esperado** - Decisão necessária? Compartilhamento de informações? Brainstorm?

### Durante: Dicas de Facilitação

- **Time-box discussions** - "Vamos gastar 5 minutos nisso, depois movemos"
- **Capture action items live** - Quem faz o quê até quando
- **Parking lot** - Anote itens fora de tópico para depois

### Depois: Formato de Resumo

```markdown
**Reunião: [Tópico] - [Data]**

**Participantes:** [Nomes]

**Decisões-Chave:**
- [Decisão 1]
- [Decisão 2]

**Itens de Ação:**
- [ ] [Pessoa]: [Tarefa] - Vencer [Data]
- [ ] [Pessoa]: [Tarefa] - Vencer [Data]

**Próximos Passos:**
- [Reunião de acompanhamento, se necessário]
- [Documentos a compartilhar]
```

**Para estruturas por tipo de reunião**: Ver `references/meeting-structures.md`

## Referência Rápida: Checklist de Comunicação

Antes de enviar qualquer comunicação profissional:

- [ ] **Propósito claro** - O destinatário consegue entender a intenção em 5 segundos?
- [ ] **Público correto** - Esta é a pessoa/canal apropriada?
- [ ] **Mensagem-chave primeiro** - O ponto principal está à frente?
- [ ] **Navegável** - Tem bullets, headers, parágrafos curtos?
- [ ] **Ação clara** - O destinatário sabe o que (se algo) precisa fazer?
- [ ] **Verificação de jargão** - O público entenderá toda a terminologia?
- [ ] **Tom apropriado** - É profissional mas não frio?
- [ ] **Revisão** - Tem erros de digitação ou frases pouco claras?

## Ferramentas Adicionais

- `references/email-templates.md` - Templates prontos para usar por tipo
- `references/meeting-structures.md` - Estruturas para standups, retros, reviews
- `references/jargon-simplification.md` - Traduções de técnico para linguagem clara

## Habilidades Complementares

- `feedback-mastery` - Para conversas difíceis e entrega de feedback
- `/draft-email` - Gere emails usando esses frameworks

---

**Última atualização:** 2025-12-22

## Histórico de Versão

- **v1.0.0** (2025-12-26): Lançamento inicial

---