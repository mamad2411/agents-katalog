---
name: architecture-decision-records
description: "Padrões abrangentes para criar, manter e gerenciar Registros de Decisões de Arquitetura (ADRs) que capturam o contexto e a lógica por trás de decisões técnicas significativas."
risk: unknown
source: community
date_added: "2026-02-27"
---

# Registros de Decisões de Arquitetura

Padrões abrangentes para criar, manter e gerenciar Registros de Decisões de Arquitetura (ADRs) que capturam o contexto e a lógica por trás de decisões técnicas significativas.

## Use esta habilidade quando

- Estiver tomando decisões arquiteturais significativas
- Documentar escolhas de tecnologia
- Registrar trade-offs de design
- Integrar novos membros da equipe
- Revisar decisões históricas
- Estabelecer processos de tomada de decisão

## Não use esta habilidade quando

- Você precisa apenas documentar pequenos detalhes de implementação
- A mudança é uma correção menor ou manutenção rotineira
- Não há decisão arquitetural a ser capturada

## Instruções

1. Capture o contexto de decisão, restrições e fatores impulsionadores.
2. Documente as opções consideradas com trade-offs.
3. Registre a decisão, a lógica e as consequências.
4. Vincule ADRs relacionados e atualize o status ao longo do tempo.

## Conceitos Principais

### 1. O que é um ADR?

Um Registro de Decisão de Arquitetura captura:
- **Contexto**: Por que precisávamos tomar uma decisão
- **Decisão**: O que decidimos
- **Consequências**: O que acontece como resultado

### 2. Quando Escrever um ADR

| Escrever ADR | Pular ADR |
|--------------|-----------|
| Adoção de novo framework | Atualizações de versão menor |
| Escolha de tecnologia de banco de dados | Correções de bugs |
| Padrões de design de API | Detalhes de implementação |
| Arquitetura de segurança | Manutenção rotineira |
| Padrões de integração | Mudanças de configuração |

### 3. Ciclo de Vida do ADR

```
Proposto → Aceito → Deprecado → Superado
             ↓
          Rejeitado
```

## Templates

### Template 1: ADR Padrão (Formato MADR)

```markdown
# ADR-0001: Usar PostgreSQL como Banco de Dados Principal

## Status

Aceito

## Contexto

Precisamos selecionar um banco de dados principal para nossa nova plataforma
de e-commerce. O sistema irá lidar com:
- ~10.000 usuários simultâneos
- Catálogo de produtos complexo com categorias hierárquicas
- Processamento de transações para pedidos e pagamentos
- Busca de texto completo para produtos
- Consultas geoespaciais para localizador de lojas

A equipe tem experiência com MySQL, PostgreSQL e MongoDB. Precisamos de
conformidade ACID para transações financeiras.

## Fatores de Decisão

* **Deve ter conformidade ACID** para processamento de pagamentos
* **Deve suportar consultas complexas** para relatórios
* **Deve suportar busca de texto completo** para reduzir complexidade de infraestrutura
* **Deve ter bom suporte a JSON** para atributos flexíveis de produtos
* **Familiaridade da equipe** reduz tempo de integração

## Opções Consideradas

### Opção 1: PostgreSQL
- **Prós**: Compatível com ACID, excelente suporte a JSON (JSONB), busca de
  texto completo integrada, PostGIS para geoespacial, a equipe tem experiência
- **Contras**: Replicação ligeiramente mais complexa que MySQL

### Opção 2: MySQL
- **Prós**: Muito familiar para a equipe, replicação simples, grande comunidade
- **Contras**: Suporte a JSON mais fraco, sem busca de texto completo integrada
  (precisa de Elasticsearch), sem geoespacial sem extensões

### Opção 3: MongoDB
- **Prós**: Schema flexível, JSON nativo, escalabilidade horizontal
- **Contras**: Sem ACID para transações multi-documento (no momento da decisão),
  equipe tem experiência limitada, requer disciplina de design de schema

## Decisão

Usaremos **PostgreSQL 15** como nosso banco de dados principal.

## Lógica

PostgreSQL oferece o melhor equilíbrio de:
1. **Conformidade ACID** essencial para transações de e-commerce
2. **Capacidades integradas** (busca de texto completo, JSONB, PostGIS) reduzem
   complexidade de infraestrutura
3. **Familiaridade da equipe** com bancos de dados SQL reduz curva de aprendizado
4. **Ecossistema maduro** com excelente ferramental e suporte comunitário

A complexidade ligeira na replicação é superada pela redução em serviços
adicionais (sem Elasticsearch separado necessário).

## Consequências

### Positivas
- Banco de dados único lida com transações, busca e consultas geoespaciais
- Complexidade operacional reduzida (menos serviços a gerenciar)
- Garantias de consistência forte para dados financeiros
- Equipe pode aproveitar expertise SQL existente

### Negativas
- Precisa aprender recursos específicos do PostgreSQL (JSONB, sintaxe de busca
  de texto completo)
- Limites de escalabilidade vertical podem exigir réplicas de leitura mais cedo
- Alguns membros da equipe precisam de treinamento específico em PostgreSQL

### Riscos
- Busca de texto completo pode não escalar tão bem quanto mecanismos de busca
  dedicados
- Mitigação: Projetar para possível adição de Elasticsearch se necessário

## Notas de Implementação

- Use JSONB para atributos de produtos flexíveis
- Implemente pooling de conexão com PgBouncer
- Configure replicação em fluxo contínuo para réplicas de leitura
- Use extensão pg_trgm para busca difusa

## Decisões Relacionadas

- ADR-0002: Estratégia de Cache (Redis) - complementa escolha de banco de dados
- ADR-0005: Arquitetura de Busca - pode superado se Elasticsearch for necessário

## Referências

- [Documentação PostgreSQL JSON](https://www.postgresql.org/docs/current/datatype-json.html)
- [Busca de Texto Completo PostgreSQL](https://www.postgresql.org/docs/current/textsearch.html)
- Interno: Benchmarks de desempenho em `/docs/benchmarks/database-comparison.md`
```

### Template 2: ADR Simplificado

```markdown
# ADR-0012: Adotar TypeScript para Desenvolvimento Frontend

**Status**: Aceito
**Data**: 2024-01-15
**Decisores**: @alice, @bob, @charlie

## Contexto

Nossa base de código React cresceu para mais de 50 componentes com crescentes
relatórios de bugs relacionados a desconexões de tipo de prop e erros undefined.
PropTypes fornecem verificação apenas em tempo de execução.

## Decisão

Adotar TypeScript para todo código frontend novo. Migrar código existente
incrementalmente.

## Consequências

**Positivo**: Capturar erros de tipo no tempo de compilação, melhor suporte de
IDE, código auto-documentado.

**Negativo**: Curva de aprendizado para equipe, desaceleração inicial, aumento
de complexidade de build.

**Mitigações**: Sessões de treinamento em TypeScript, permitir adoção gradual
com `allowJs: true`.
```

### Template 3: Formato Y-Statement

```markdown
# ADR-0015: Seleção de API Gateway

No contexto de **construir uma arquitetura de microsserviços**,
enfrentando **a necessidade de gerenciamento centralizado de API,
autenticação e rate limiting**,
decidimos por **Kong Gateway**
e contra **AWS API Gateway e solução Nginx customizada**,
para alcançar **independência de fornecedor, extensibilidade de plugins
e familiaridade da equipe com Lua**,
aceitando que **precisamos gerenciar infraestrutura Kong nós mesmos**.
```

### Template 4: ADR para Deprecação

```markdown
# ADR-0020: Deprecar MongoDB em Favor do PostgreSQL

## Status

Aceito (Supersede ADR-0003)

## Contexto

ADR-0003 (2021) escolheu MongoDB para armazenamento de perfil de usuário devido
à necessidade de flexibilidade de schema. Desde então:
- Transações multi-documento do MongoDB continuam problemáticas para nosso caso
  de uso
- Nosso schema se estabilizou e raramente muda
- Agora temos expertise em PostgreSQL de outros serviços
- Manter dois bancos de dados aumenta a carga operacional

## Decisão

Deprecar MongoDB e migrar perfis de usuário para PostgreSQL.

## Plano de Migração

1. **Fase 1** (Semana 1-2): Criar schema PostgreSQL, dual-write ativado
2. **Fase 2** (Semana 3-4): Preencher dados históricos, validar consistência
3. **Fase 3** (Semana 5): Trocar leituras para PostgreSQL, monitorar
4. **Fase 4** (Semana 6): Remover escritas MongoDB, desativar

## Consequências

### Positivas
- Tecnologia de banco de dados único reduz complexidade operacional
- Transações ACID para dados de usuário
- Equipe pode focar expertise PostgreSQL

### Negativas
- Esforço de migração (~4 semanas)
- Risco de problemas de dados durante migração
- Perder alguma flexibilidade de schema

## Lições Aprendidas

Documentar da experiência ADR-0003:
- Benefícios de flexibilidade de schema foram superestimados
- Custo operacional de múltiplos bancos de dados foi subestimado
- Considerar manutenção de longo prazo em decisões de tecnologia
```

### Template 5: Estilo Request for Comments (RFC)

```markdown
# RFC-0025: Adotar Event Sourcing para Gerenciamento de Pedidos

## Resumo

Propor a adoção do padrão event sourcing para o domínio de gerenciamento de
pedidos para melhorar auditabilidade, permitir consultas temporais e suportar
análise de negócios.

## Motivação

Desafios atuais:
1. Requisitos de auditoria precisam de histórico completo de pedidos
2. Consultas "Qual era o estado do pedido no momento X?" são impossíveis
3. Equipe de análise precisa de fluxo de eventos para dashboards em tempo real
4. Reconstrução de estado de pedido para suporte ao cliente é manual

## Design Detalhado

### Event Store

```
OrderCreated { orderId, customerId, items[], timestamp }
OrderItemAdded { orderId, item, timestamp }
OrderItemRemoved { orderId, itemId, timestamp }
PaymentReceived { orderId, amount, paymentId, timestamp }
OrderShipped { orderId, trackingNumber, timestamp }
```

### Projeções

- **CurrentOrderState**: Visualização materializada para consultas
- **OrderHistory**: Cronograma completo para auditoria
- **DailyOrderMetrics**: Agregação de análise

### Tecnologia

- Event Store: EventStoreDB (construído com propósito, lida com projeções)
- Alternativa considerada: Kafka + serviço de projeção customizado

## Desvantagens

- Curva de aprendizado para equipe
- Complexidade aumentada vs. CRUD
- Precisa projetar eventos cuidadosamente (imutáveis uma vez armazenados)
- Crescimento de armazenamento (eventos nunca deletados)

## Alternativas

1. **Tabelas de auditoria**: Mais simples mas não permite consultas temporais
2. **CDC do BD existente**: Complexo, não altera modelo de dados
3. **Híbrido**: Event source apenas para mudanças de estado de pedido

## Questões Não Resolvidas

- [ ] Estratégia de versionamento de schema de evento
- [ ] Política de retenção para eventos
- [ ] Frequência de snapshot para desempenho

## Plano de Implementação

1. Protótipo com tipo único de pedido (2 semanas)
2. Treinamento de equipe em event sourcing (1 semana)
3. Implementação completa e migração (4 semanas)
4. Monitoramento e otimização (contínuo)

## Referências

- [Event Sourcing por Martin Fowler](https://martinfowler.com/eaaDev/EventSourcing.html)
- [Documentação EventStoreDB](https://www.eventstore.com/docs)
```

## Gerenciamento de ADR

### Estrutura de Diretório

```
docs/
├── adr/
│   ├── README.md           # Índice e diretrizes
│   ├── template.md         # Template ADR da equipe
│   ├── 0001-use-postgresql.md
│   ├── 0002-caching-strategy.md
│   ├── 0003-mongodb-user-profiles.md  # [DEPRECADO]
│   └── 0020-deprecate-mongodb.md      # Supersede 0003
```

### Índice de ADR (README.md)

```markdown
# Registros de Decisões de Arquitetura

Este diretório contém Registros de Decisões de Arquitetura (ADRs) para
[Nome do Projeto].

## Índice

| ADR | Título | Status | Data |
|-----|--------|--------|------|
| 0001 | Usar PostgreSQL como Banco de Dados Principal | Aceito | 2024-01-10 |
| 0002 | Estratégia de Cache com Redis | Aceito | 2024-01-12 |
| 0003 | MongoDB para Perfis de Usuário | Deprecado | 2023-06-15 |
| 0020 | Deprecar MongoDB | Aceito | 2024-01-15 |

## Criando um Novo ADR

1. Copie `template.md` para `NNNN-title-with-dashes.md`
2. Preencha o template
3. Submeta PR para revisão
4. Atualize este índice após aprovação

## Status do ADR

- **Proposto**: Em discussão
- **Aceito**: Decisão tomada, implementando
- **Deprecado**: Não mais relevante
- **Superado**: Substituído por outro ADR
- **Rejeitado**: Considerado mas não adotado
```

### Automação (adr-tools)

```bash
# Instalar adr-tools
brew install adr-tools

# Inicializar diretório ADR
adr init docs/adr

# Criar novo ADR
adr new "Usar PostgreSQL como Banco de Dados Principal"

# Superar um ADR
adr new -s 3 "Deprecar MongoDB em Favor do PostgreSQL"

# Gerar table of contents
adr generate toc > docs/adr/README.md

# Vincular ADRs relacionados
adr link 2 "Complementa" 1 "É complementado por"
```

## Processo de Revisão

```markdown
## Checklist de Revisão de ADR

### Antes da Submissão
- [ ] Contexto explica claramente o problema
- [ ] Todas as opções viáveis consideradas
- [ ] Prós/contras balanceados e honestos
- [ ] Consequências (positivas e negativas) documentadas
- [ ] ADRs relacionados vinculados

### Durante Revisão
- [ ] Pelo menos 2 engenheiros sênior revisaram
- [ ] Equipes afetadas consultadas
- [ ] Implicações de segurança consideradas
- [ ] Implicações de custo documentadas
- [ ] Reversibilidade avaliada

### Após Aceitação
- [ ] Índice de ADR atualizado
- [ ] Equipe notificada
- [ ] Tickets de implementação criados
- [ ] Documentação relacionada atualizada
```

## Melhores Práticas

### Faça
- **Escreva ADRs cedo** - Antes da implementação começar
- **Mantenha-os curtos** - 1-2 páginas no máximo
- **Seja honesto sobre trade-offs** - Inclua contras reais
- **Vincule decisões relacionadas** - Construa grafo de decisão
- **Atualize status** - Deprecie quando superado

### Não Faça
- **Não mude ADRs aceitos** - Escreva novos para superá-los
- **Não pule contexto** - Leitores futuros precisam de background
- **Não esconda falhas** - Decisões rejeitadas são valiosas
- **Não seja vago** - Decisões específicas, consequências específicas
- **Não esqueça implementação** - ADR sem ação é desperdício

## Recursos

- [Documenting Architecture Decisions (Michael Nygard)](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [Template MADR](https://adr.github.io/madr/)
- [Organização ADR GitHub](https://adr.github.io/)
- [adr-tools](https://github.com/npryce/adr-tools)