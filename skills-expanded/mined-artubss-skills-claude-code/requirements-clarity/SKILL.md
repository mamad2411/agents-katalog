---
name: requirements-clarity
description: Esclareça requisitos ambíguos através de diálogo focado antes da implementação. Use quando requisitos forem pouco claros, features forem complexas (>2 dias) ou envolverem coordenação entre times. Faça duas perguntas essenciais - Por quê? (verificação YAGNI) e Mais simples? (verificação KISS) - para garantir clareza antes de codificar.
---

# Skill de Clareza de Requisitos

## Descrição

Transforma automaticamente requisitos vagos em PRDs acionáveis através de clarificação sistemática com um sistema de pontuação de 100 pontos.


## Instruções

Quando ativado, detecte requisitos vagos:

1. **Solicitações de Feature Vagas**
   - Usuário diz: "adicionar login", "implementar pagamento", "criar dashboard"
   - Faltam: Como, com qual tecnologia, quais restrições?

2. **Contexto Técnico Faltando**
   - Nenhuma pilha de tecnologia mencionada
   - Nenhum ponto de integração identificado
   - Nenhuma restrição de performance/segurança

3. **Especificações Incompletas**
   - Nenhum critério de aceitação
   - Nenhuma métrica de sucesso
   - Nenhum caso extremo considerado
   - Nenhum tratamento de erro mencionado

4. **Escopo Ambíguo**
   - Limites pouco claros ("user management" - exatamente o quê?)
   - Sem distinção entre MVP e melhorias futuras
   - Falta o "o que NÃO está incluído"

**NÃO ative quando**:
- Caminhos de arquivo específicos mencionados (ex: "auth.go:45")
- Snippets de código incluídos
- Funções/classes existentes referenciadas
- Correções de bugs com passos de reprodução claros

## Princípios Centrais

1. **Questionamento Sistemático**
   - Faça perguntas focadas e específicas
   - Uma categoria por vez (2-3 perguntas por rodada)
   - Construa sobre respostas anteriores
   - Evite sobrecarregar usuários

2. **Iteração Orientada à Qualidade**
   - Avalie continuamente pontuação de clareza (0-100)
   - Identifique lacunas sistematicamente
   - Itere até ≥ 90 pontos
   - Documente todas as rodadas de clarificação

3. **Output Acionável**
   - Gere especificações concretas
   - Inclua critérios de aceitação mensuráveis
   - Forneça fases executáveis
   - Permita implementação direta

## Processo de Clarificação

### Etapa 1: Análise Inicial do Requisito

**Input**: Descrição do requisito do usuário

**Tarefas**:
1. Analise e compreenda o requisito central
2. Gere nome da feature (formato kebab-case)
3. Determine versão do documento (padrão `1.0` salvo especificação do usuário)
4. Garanta que `./docs/prds/` exista para output do PRD
5. Realize avaliação inicial de clareza (0-100)

**Rubrica de Avaliação**:
```
Clareza Funcional: /30 pontos
- Inputs/outputs claros: 10 pts
- Interação do usuário definida: 10 pts
- Critérios de sucesso declarados: 10 pts

Especificidade Técnica: /25 pontos
- Pilha de tecnologia mencionada: 8 pts
- Pontos de integração identificados: 8 pts
- Restrições especificadas: 9 pts

Completude da Implementação: /25 pontos
- Casos extremos considerados: 8 pts
- Tratamento de erro mencionado: 9 pts
- Validação de dados especificada: 8 pts

Contexto de Negócio: /20 pontos
- Declaração de problema clara: 7 pts
- Usuários-alvo identificados: 7 pts
- Métricas de sucesso definidas: 6 pts
```

**Formato de Resposta Inicial**:
```markdown
Entendi seu requisito. Deixe-me ajudar você a refinar essa especificação.

**Pontuação de Clareza Atual**: X/100

**Aspectos Claros**:
- [Liste o que está claro]

**Precisa de Clarificação**:
- [Liste lacunas]

Vou esclarecer esses pontos sistematicamente...
```

### Etapa 2: Análise de Lacunas

Identifique informações faltando em quatro dimensões:

**1. Escopo Funcional**
- Qual é a funcionalidade central?
- Quais são os limites?
- O que está fora do escopo?
- Quais são os casos extremos?

**2. Interação do Usuário**
- Como os usuários interagem?
- Quais são os inputs?
- Quais são os outputs?
- Quais são cenários de sucesso/falha?

**3. Restrições Técnicas**
- Requisitos de performance?
- Requisitos de compatibilidade?
- Considerações de segurança?
- Necessidades de escalabilidade?

**4. Valor de Negócio**
- Qual problema isso resolve?
- Quem são os usuários-alvo?
- Quais são as métricas de sucesso?
- Qual é a prioridade?

### Etapa 3: Clarificação Interativa

**Estratégia de Perguntas**:
1. Comece com lacunas de maior impacto
2. Faça 2-3 perguntas por rodada
3. Construa contexto progressivamente
4. Use a linguagem do usuário
5. Forneça exemplos quando útil

**Formato de Pergunta**:
```markdown
Preciso esclarecer os seguintes pontos para completar o documento de requisitos:

1. **[Categoria]**: [Pergunta específica]?
   - Por exemplo: [Exemplo se útil]

2. **[Categoria]**: [Pergunta específica]?

3. **[Categoria]**: [Pergunta específica]?

Favor fornecer suas respostas, e continuarei refinando o PRD.
```

**Após Cada Resposta do Usuário**:
1. Atualize pontuação de clareza
2. Capture novas informações no esboço do PRD em trabalho
3. Identifique lacunas restantes
4. Se pontuação < 90: Continue com próxima rodada de perguntas
5. Se pontuação ≥ 90: Prossiga para geração do PRD

**Formato de Atualização de Pontuação**:
```markdown
Obrigado pelas informações adicionais!

**Atualização de Pontuação de Clareza**: X/100 → Y/100

**Conteúdo Recém Clarificado**:
- [Resuma novas informações]

**Pontos Restantes a Esclarecer**:
- [Liste lacunas restantes se pontuação < 90]

[Se pontuação < 90: Continue com próxima rodada de perguntas]
[Se pontuação ≥ 90: "Perfeito! Vou agora gerar o documento PRD completo..."]
```

### Etapa 4: Geração do PRD

Após pontuação de clareza ≥ 90, gere PRD abrangente.

**Arquivo de Output**:

1. **PRD Final**: `./docs/prds/{feature_name}-v{version}-prd.md`

Use a ferramenta `Write` para criar ou atualizar este arquivo. Derive `{version}` da versão do documento registrada no PRD (padrão `1.0`).

## Estrutura do Documento PRD

```markdown
# {Nome da Feature} - Documento de Requisitos do Produto (PRD)

## Descrição de Requisitos

### Contexto
- **Problema de Negócio**: [Descreva o problema de negócio a ser resolvido]
- **Usuários-Alvo**: [Grupos de usuários-alvo]
- **Proposta de Valor**: [Valor que essa feature traz]

### Visão Geral da Feature
- **Features Centrais**: [Lista de features principais]
- **Limites da Feature**: [O que está e não está incluído]
- **Cenários de Usuário**: [Cenários típicos de uso]

### Requisitos Detalhados
- **Input/Output**: [Especificações específicas de input/output]
- **Interação do Usuário**: [Fluxo de operação do usuário]
- **Requisitos de Dados**: [Estruturas de dados e regras de validação]
- **Casos Extremos**: [Tratamento de casos extremos]

## Decisões de Design

### Abordagem Técnica
- **Escolha de Arquitetura**: [Decisões de arquitetura técnica e fundamentação]
- **Componentes-Chave**: [Lista de componentes técnicos principais]
- **Armazenamento de Dados**: [Modelos de dados e soluções de armazenamento]
- **Especificação de Interface**: [Especificações de API/interface]

### Restrições
- **Requisitos de Performance**: [Tempo de resposta, throughput, etc.]
- **Compatibilidade**: [Requisitos de compatibilidade de sistema]
- **Segurança**: [Considerações de segurança]
- **Escalabilidade**: [Considerações de expansão futura]

### Avaliação de Risco
- **Riscos Técnicos**: [Riscos técnicos potenciais e planos de mitigação]
- **Riscos de Dependência**: [Dependências externas e alternativas]
- **Riscos de Cronograma**: [Riscos de cronograma e estratégias de resposta]

## Critérios de Aceitação

### Aceitação Funcional
- [ ] Feature 1: [Condições de aceitação específicas]
- [ ] Feature 2: [Condições de aceitação específicas]
- [ ] Feature 3: [Condições de aceitação específicas]

### Padrões de Qualidade
- [ ] Qualidade de Código: [Padrões de código e requisitos de revisão]
- [ ] Cobertura de Testes: [Requisitos de teste e cobertura]
- [ ] Métricas de Performance: [Critérios de aprovação em testes de performance]
- [ ] Revisão de Segurança: [Requisitos de revisão de segurança]

### Aceitação do Usuário
- [ ] Experiência do Usuário: [Critérios de aceitação de UX]
- [ ] Documentação: [Requisitos de entrega de documentação]
- [ ] Materiais de Treinamento: [Se necessário, requisitos de material de treinamento]

## Fases de Execução

### Fase 1: Preparação
**Objetivo**: Preparação do ambiente e validação técnica
- [ ] Tarefa 1: [Descrição específica da tarefa]
- [ ] Tarefa 2: [Descrição específica da tarefa]
- **Entregáveis**: [Entregáveis da fase]
- **Tempo**: [Tempo estimado]

### Fase 2: Desenvolvimento Central
**Objetivo**: Implementar funcionalidade central
- [ ] Tarefa 1: [Descrição específica da tarefa]
- [ ] Tarefa 2: [Descrição específica da tarefa]
- **Entregáveis**: [Entregáveis da fase]
- **Tempo**: [Tempo estimado]

### Fase 3: Integração & Testes
**Objetivo**: Integração e garantia de qualidade
- [ ] Tarefa 1: [Descrição específica da tarefa]
- [ ] Tarefa 2: [Descrição específica da tarefa]
- **Entregáveis**: [Entregáveis da fase]
- **Tempo**: [Tempo estimado]

### Fase 4: Deployment
**Objetivo**: Release e monitoramento
- [ ] Tarefa 1: [Descrição específica da tarefa]
- [ ] Tarefa 2: [Descrição específica da tarefa]
- **Entregáveis**: [Entregáveis da fase]
- **Tempo**: [Tempo estimado]

---

**Versão do Documento**: 1.0
**Criado**: {timestamp}
**Rodadas de Clarificação**: {clarification_rounds}
**Pontuação de Qualidade**: {quality_score}/100
```

## Diretrizes de Comportamento

### FAÇA
- Faça perguntas específicas e focadas
- Construa sobre respostas anteriores
- Forneça exemplos para orientar usuários
- Mantenha tom conversacional
- Resuma rodadas de clarificação dentro do PRD
- Use inglês claro e profissional
- Gere especificações concretas
- Permaneça em modo de clarificação até pontuação ≥ 90

### NÃO FAÇA
- Faça todas as perguntas de uma vez
- Faça suposições sem confirmação
- Gere PRD antes de pontuação 90+
- Pule nenhuma seção obrigatória
- Use linguagem vaga ou abstrata
- Prossiga sem respostas do usuário
- Saia do modo skill prematuramente

## Critérios de Sucesso

- Pontuação de clareza ≥ 90/100
- Todas as seções do PRD completas com substância
- Critérios de aceitação verificáveis (usando formato `- [ ]`)
- Fases de execução acionáveis com tarefas concretas
- Usuário aprova PRD final
- Pronto para handoff de desenvolvimento