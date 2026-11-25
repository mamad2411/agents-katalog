---
name: it-operations
description: Gerencia infraestrutura de TI, monitoramento, resposta a incidentes e confiabilidade de serviços. Fornece frameworks para gerenciamento de serviços ITIL, estratégias de observabilidade, automação, backup/recuperação, planejamento de capacidade e práticas de excelência operacional.
---

# Especialista em Operações de TI

Uma competência abrangente para gerenciar operações de infraestrutura de TI, garantir confiabilidade de serviços, implementar estratégias de monitoramento e alertas, gerenciar incidentes e manter excelência operacional através de automação e melhores práticas.

## Princípios Fundamentais

### 1. Confiabilidade de Serviço em Primeiro Lugar
- **Monitoramento Proativo**: Implementar observabilidade abrangente antes que incidentes ocorram
- **Gerenciamento de Incidentes**: Processos de resposta estruturados com caminhos de escalação claros
- **Gerenciamento de SLA/SLO**: Definir e manter objetivos de nível de serviço alinhados com as necessidades de negócio
- **Melhoria Contínua**: Aprender com incidentes através de post-mortems isentos de culpa

### 2. Automação em Detrimento de Processos Manuais
- **Infraestrutura como Código**: Gerenciar configuração de infraestrutura através de código versionado
- **Automação de Runbooks**: Converter procedimentos manuais em workflows automatizados
- **Sistemas Auto-Recuperáveis**: Implementar remediação automatizada para problemas comuns
- **Gerenciamento de Configuração**: Manter consistência entre ambientes

### 3. Gerenciamento de Serviços ITIL
- **Estratégia de Serviço**: Alinhar serviços de TI com objetivos de negócio
- **Design de Serviço**: Projetar serviços resilientes e escaláveis
- **Transição de Serviço**: Gerenciar mudanças com disrupção mínima
- **Operação de Serviço**: Entregar e suportar serviços efetivamente
- **Melhoria Contínua de Serviço**: Aprimorar iterativamente a qualidade de serviço

### 4. Excelência Operacional
- **Documentação**: Manter runbooks atualizados, procedimentos e diagramas de arquitetura
- **Gerenciamento de Conhecimento**: Construir bases de conhecimento pesquisáveis a partir de resoluções de incidentes
- **Planejamento de Capacidade**: Prever e provisionar recursos de forma proativa
- **Otimização de Custos**: Balancear requisitos de performance com custos de infraestrutura

## Workflow Principal

### Workflow de Operações de Infraestrutura

```
1. MONITORAMENTO & OBSERVABILIDADE
   ├─ Definir SLIs/SLOs/SLAs para serviços críticos
   ├─ Implementar coleta de métricas (infraestrutura, aplicação, negócio)
   ├─ Configurar alertas com limiares apropriados e escalação
   ├─ Construir dashboards para diferentes públicos (ops, devs, executivos)
   └─ Estabelecer rotação de on-call e procedimentos de escalação

2. GERENCIAMENTO DE INCIDENTES
   ├─ Receber alerta ou relato de usuário
   ├─ Avaliar severidade e impacto (P1/P2/P3/P4)
   ├─ Engajar respondentes apropriados
   ├─ Investigar e diagnosticar causa raiz
   ├─ Implementar correção ou contorno
   ├─ Comunicar status para stakeholders
   ├─ Documentar resolução na base de conhecimento
   └─ Conduzir revisão pós-incidente

3. GERENCIAMENTO DE MUDANÇAS
   ├─ Submeter requisição de mudança com avaliação de impacto
   ├─ Revisar e aprovar através de CAB (Change Advisory Board)
   ├─ Agendar janela de mudança
   ├─ Executar mudança com plano de rollback pronto
   ├─ Validar critérios de sucesso
   ├─ Documentar resultados reais vs planejados
   └─ Fechar ticket de mudança

4. PLANEJAMENTO DE CAPACIDADE
   ├─ Coletar tendências de utilização de recursos
   ├─ Analisar padrões de crescimento
   ├─ Prever requisitos futuros
   ├─ Planejar procurement ou provisioning
   ├─ Executar adições de capacidade
   └─ Monitorar efetividade

5. AUTOMAÇÃO & OTIMIZAÇÃO
   ├─ Identificar tarefas manuais repetitivas
   ├─ Documentar processo atual
   ├─ Projetar solução automatizada
   ├─ Implementar e testar automação
   ├─ Fazer deploy em produção
   ├─ Medir economia de tempo/custo
   └─ Iterar e melhorar
```

## Frameworks de Decisão

### Matriz de Decisão de Configuração de Alertas

| Cenário | Tipo de Alerta | Limiar | Tempo de Resposta | Escalação |
|----------|-----------|-----------|---------------|------------|
| Serviço completamente indisponível | Page | Imediato | < 5 min | Imediato para on-call |
| Serviço degradado | Page | 2-3 falhas | < 15 min | Após 15 min para on-call |
| Alto uso de recursos | Aviso | > 80% sustentado | < 1 hora | Após 2 horas para líder de equipe |
| Aproximando capacidade | Info | > 70% tendência | < 24 horas | Revisão semanal de capacidade |
| Desvio de configuração | Ticket | Qualquer desvio | < 7 dias | Revisão mensal |

### Classificação de Severidade de Incidentes

**Prioridade 1 (Crítica)**
- Indisponibilidade completa de serviço afetando todos os usuários
- Perda de dados ou breach de segurança
- Impacto financeiro > R$ 50K/hora
- Resposta: Imediata, 24/7, todos disponíveis

**Prioridade 2 (Alta)**
- Indisponibilidade parcial de serviço afetando muitos usuários
- Degradação significativa de performance
- Impacto financeiro R$ 5K-R$ 50K/hora
- Resposta: < 30 minutos durante horário comercial

**Prioridade 3 (Média)**
- Degradação de serviço afetando alguns usuários
- Funcionalidade não-crítica prejudicada
- Workaround disponível
- Resposta: < 4 horas durante horário comercial

**Prioridade 4 (Baixa)**
- Problemas menores com impacto mínimo
- Problemas cosméticos
- Solicitações de melhorias
- Resposta: Próximo dia útil

### Avaliação de Risco de Gerenciamento de Mudanças

```
Nível de Risco = Impacto × Probabilidade × Complexidade

Impacto (1-5):
1 = Usuário único
2 = Equipe
3 = Departamento
4 = Empresa inteira
5 = Voltado para cliente

Probabilidade de Problemas (1-5):
1 = Rotina, testada
2 = Familiar, documentada
3 = Alguma incerteza
4 = Novo território
5 = Nunca feito antes

Complexidade (1-5):
1 = Componente único
2 = Poucos componentes
3 = Múltiplos sistemas
4 = Cross-platform
5 = Escala empresarial

Interpretação da Pontuação de Risco:
1-20: Mudança padrão (pré-aprovada)
21-50: Mudança normal (revisão CAB)
51-75: Mudança de alto risco (testes extensivos, aprovação senior)
76-125: Mudança de emergência apenas (aprovação executiva)
```

### Seleção de Ferramentas de Monitoramento

| Requisito | Prometheus + Grafana | Datadog | New Relic | ELK Stack | Splunk |
|-------------|---------------------|---------|-----------|-----------|---------|
| Custo | Grátis (auto-hospedado) | $$$$ | $$$$ | Grátis-$$ | $$$$$ |
| Métricas | Excelente | Excelente | Excelente | Bom | Bom |
| Logs | Via Loki | Excelente | Excelente | Excelente | Excelente |
| Traces | Via Tempo | Excelente | Excelente | Limitado | Bom |
| Curva de Aprendizado | Íngreme | Moderada | Moderada | Íngreme | Íngreme |
| Cloud-Native | Excelente | Excelente | Excelente | Bom | Bom |
| On-Premises | Excelente | Bom | Bom | Excelente | Excelente |
| APM | Via exporters | Excelente | Excelente | Limitado | Bom |

## Desafios Operacionais Comuns

### Desafio 1: Fadiga de Alertas
**Problema**: Muitos alertas falsos positivos causando burnout da equipe

**Solução**:
```yaml
Processo de Ajuste de Alertas:
1. Medir volume de alertas baseline e taxa de falsos positivos
2. Categorizar alertas por acionabilidade:
   - Acionável + Urgente = Manter como page
   - Acionável + Não Urgente = Ticket
   - Não Acionável = Remover ou converter para métrica de dashboard
3. Implementar agregação de alertas (agrupar alertas similares)
4. Adicionar contexto aos alertas (links para runbooks, métricas relevantes)
5. Reuniões de revisão regulares (semanais) para ajustar limiares
6. Rastrear métricas:
   - MTTA (Tempo Médio para Reconhecer): < 5 min alvo
   - Taxa de Falsos Positivos: < 20% alvo
   - Volume de Alertas por Semana: Tendência decrescente
```

### Desafio 2: Documentação de Incidentes Durante Crise
**Problema**: Equipes pulam documentação durante incidentes de alta pressão

**Solução**:
- Designar função dedicada de escrivão (não o comandante de incidente)
- Usar ferramentas de gerenciamento de incidentes (PagerDuty, Opsgenie) com timeline automática
- Relatórios de incidentes baseados em template com campos obrigatórios
- Revisão pós-incidente agendada automaticamente (dentro de 48 horas)
- Gamificar documentação (rastrear e reconhecer documentação completa)

### Desafio 3: Silos de Conhecimento
**Problema**: Conhecimento crítico preso nas cabeças de membros individuais da equipe

**Solução**:
```yaml
Estratégia de Transferência de Conhecimento:
- Pair Programming/Shadowing: 20% da capacidade de sprint
- Requisitos de Runbook: Todo sistema deve ter runbook
- Sessões Lunch & Learn: 30 min semanais de compartilhamento de conhecimento
- Matriz de Treinamento Cruzado: Rastrear quem sabe o quê, identificar gaps
- Rotação de On-Call: Todos rodam para espalhar conhecimento
- Revisões Pós-Incidente: Compartilhamento obrigatório com equipe
- Sprints de Documentação: Foco trimestral na conclusão de documentação
```

### Desafio 4: Balanceando Estabilidade vs Inovação
**Problema**: Equipe de operações resiste a mudanças para manter estabilidade

**Solução**:
- Implementar janelas de mudança (períodos de manutenção planejada)
- Usar deployments blue-green ou canary para reduzir risco
- Estabelecer "tempo de inovação" (modelo Google 20% time)
- Criar ambientes sandbox para experimentação
- Medir e recompensar tanto estabilidade quanto métricas de melhoria
- Incluir "redução de toil" como alvo de OKR

## Métricas Principais & KPIs

### Métricas de Confiabilidade de Serviço
```yaml
Disponibilidade:
  Fórmula: (Tempo Total - Downtime) / Tempo Total × 100
  Alvo: 99,9% (43,8 min/mês de downtime)
  Medição: Por serviço, mensalmente

MTTR (Tempo Médio para Recuperação):
  Fórmula: Soma dos tempos de recuperação / Número de incidentes
  Alvo: < 30 minutos para P1, < 4 horas para P2
  Medição: Por nível de severidade, mensalmente

MTBF (Tempo Médio Entre Falhas):
  Fórmula: Tempo operacional total / Número de falhas
  Alvo: > 720 horas (30 dias)
  Medição: Por serviço, trimestralmente

MTTA (Tempo Médio para Reconhecer):
  Fórmula: Soma dos tempos de reconhecimento / Número de alertas
  Alvo: < 5 minutos para pages
  Medição: Por engenheiro de on-call, semanalmente

Taxa de Sucesso de Mudança:
  Fórmula: Mudanças bem-sucedidas / Total de mudanças × 100
  Alvo: > 95%
  Medição: Mensalmente

Taxa de Recorrência de Incidentes:
  Fórmula: Incidentes repetidos / Total de incidentes × 100
  Alvo: < 10%
  Medição: Trimestral (mesma causa raiz em 90 dias)
```

### Métricas de Eficiência Operacional
```yaml
Percentual de Toil:
  Definição: Tempo gasto em tarefas manuais e repetitivas
  Alvo: < 30% da capacidade da equipe
  Medição: Rastreamento de tempo semanal

Cobertura de Automação:
  Fórmula: Tarefas automatizadas / Total de tarefas repetitivas × 100
  Alvo: > 70%
  Medição: Auditoria trimestral

Carga de On-Call:
  Fórmula: Alertas por turno de on-call
  Alvo: < 5 alertas acionáveis por turno
  Medição: Por engenheiro, semanalmente

Cobertura de Runbook:
  Fórmula: Serviços com runbooks / Total de serviços × 100
  Alvo: 100%
  Medição: Auditoria mensal

Utilização de Base de Conhecimento:
  Fórmula: Incidentes resolvidos via KB / Total de incidentes × 100
  Alvo: > 40%
  Medição: Mensalmente
```

## Pontos de Integração

### Com Times de Desenvolvimento
- Participar em revisões de design para requisitos operacionais
- Fornecer automação de deployment e suporte a pipeline CI/CD
- Compartilhar requisitos de monitoramento e logging
- Colaborar em resposta a incidentes e post-mortems
- Propriedade conjunta de SLOs e orçamentos de erro

### Com Times de Segurança
- Implementar monitoramento e alertas de segurança
- Gerenciar controles de acesso e sistemas de autenticação
- Coordenar patching de vulnerabilidades e remediação
- Conduzir resposta a incidentes de segurança
- Manter conformidade com políticas de segurança

### Com Stakeholders de Negócio
- Reportar sobre disponibilidade e performance de serviço
- Comunicar janelas de manutenção planejadas
- Fornecer previsões de planejamento de capacidade
- Traduzir métricas técnicas para impacto de negócio
- Participar no planejamento de continuidade de negócio

## Melhores Práticas

### 1. Post-Mortems Isentos de Culpa
```markdown
Template de Revisão Pós-Incidente:
- Resumo do Incidente (o que aconteceu, quando, impacto)
- Timeline de Eventos (cronologia detalhada)
- Análise de Causa Raiz (5 Porquês ou Diagrama de Ishikawa)
- O Que Correu Bem (pontos fortes durante resposta)
- O Que Poderia Melhorar (oportunidades)
- Itens de Ação (com proprietários e datas de entrega)
- Lições Aprendidas (insights compartilháveis)

Regras:
- Sem culpa ou punição
- Foco em sistemas e processos, não pessoas
- Todos podem falar livremente
- Itens de ação devem ser rastreados até conclusão
```

### 2. Padrões de Runbook
```yaml
Conteúdo de Runbook:
  - Visão Geral do Serviço: Propósito, dependências, arquitetura
  - SLIs/SLOs/SLAs: Limiares e alvos definidos
  - Problemas Comuns: Sintomas, causas, soluções
  - Passos de Troubleshooting: Procedimentos passo a passo
  - Caminhos de Escalação: Quem contatar e quando
  - Comandos Úteis: Comandos prontos para copiar/colar
  - Links de Dashboard: Links diretos para dashboards relevantes
  - Mudanças Recentes: Link para log de mudanças
  - Informações de Contato: Equipe, product owner, SMEs

Manutenção:
  - Revisar trimestralmente ou após incidentes maiores
  - Testar procedimentos durante períodos de baixo tráfego
  - Atualizar após toda mudança significativa
  - Rastrear métricas de uso (page views, ratings de utilidade)
```

### 3. Melhores Práticas de On-Call
```yaml
Preparação para On-Call:
  - Laptop com acesso VPN
  - Dispositivo móvel com apps de notificação
  - Lista de contatos (caminhos de escalação)
  - Acesso a todos os sistemas críticos
  - Runbooks marcados como favoritos
  - On-call de backup identificado

Durante On-Call:
  - Reconhecer alertas dentro de 5 minutos
  - Atualizar status do incidente regularmente
  - Seguir procedimentos de escalação
  - Documentar todas as ações no ticket de incidente
  - Fazer handoff claro para próximo on-call

Pós On-Call:
  - Completar relatórios de incidente
  - Submeter tickets de redução de toil
  - Fornecer feedback sobre runbooks
  - Atualizar documentação de on-call
```

### 4. Disciplina de Gerenciamento de Mudanças
```yaml
Processo de Mudança Padrão:
  1. Criar requisição de mudança (RFC)
  2. Documentar:
     - O Quê: Mudanças específicas sendo feitas
     - Por Quê: Justificativa de negócio
     - Quando: Data/hora proposta
     - Quem: Implementador e aprovador de mudança
     - Como: Procedimento passo a passo
     - Risco: Avaliação e mitigação
     - Rollback: Plano de rollback detalhado
     - Testes: Passos de validação
  3. Submeter para revisão CAB (aviso com 7 dias de antecedência)
  4. Implementar durante janela aprovada
  5. Validar critérios de sucesso
  6. Fechar mudança com resultados reais
  7. Revisão pós-implementação se problemas ocorreram

Processo de Mudança de Emergência:
  - Aprovação executiva necessária
  - Implementar com monitoramento aumentado
  - Notificação completa da equipe
  - Documentação completa em 24 horas
  - Revisão pós-mudança obrigatória
```

## Arquivos de Referência

Para orientação técnica detalhada, consulte:
- [reference/monitoring.md](reference/monitoring.md) - Observabilidade, métricas, alertas e design de dashboards
- [reference/incident-management.md](reference/incident-management.md) - Resposta a incidentes, análise de causa raiz, post-mortems
- [reference/infrastructure.md](reference/infrastructure.md) - Gerenciamento de servidores, operações de rede, planejamento de capacidade
- [reference/automation.md](reference/automation.md) - Scripting, gerenciamento de configuração, ferramentas de orquestração
- [reference/backup-recovery.md](reference/backup-recovery.md) - Estratégias de backup, recuperação de desastre, continuidade de negócio

## Primeiros Passos

1. **Para Nova Infraestrutura**: Comece com [reference/infrastructure.md](reference/infrastructure.md) para orientação de setup
2. **Para Setup de Monitoramento**: Revise [reference/monitoring.md](reference/monitoring.md) para estratégia de observabilidade
3. **Para Resposta a Incidentes**: Veja [reference/incident-management.md](reference/incident-management.md) para procedimentos
4. **Para Projetos de Automação**: Verifique [reference/automation.md](reference/automation.md) para recomendações de tooling
5. **Para Planejamento de DR**: Consulte [reference/backup-recovery.md](reference/backup-recovery.md) para estratégias de recuperação