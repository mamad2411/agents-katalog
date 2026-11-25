---
name: n8n-workflow-patterns
description: Padrões arquiteturais comprovados de workflows reais n8n. Use ao construir novos workflows, projetar estrutura de workflow, escolher padrões de workflow, planejar arquitetura de workflow, ou ao fazer perguntas sobre processamento de webhook, integração HTTP API, operações de banco de dados, workflows de agente IA, ou tarefas agendadas.
---

# Padrões de Workflow n8n

Padrões arquiteturais comprovados para construir workflows n8n.

---

## Os 5 Padrões Centrais

Com base em análise de uso real de workflow:

1. **[Processamento de Webhook](webhook_processing.md)** (Mais Comum)
   - Receber requisições HTTP → Processar → Saída
   - Padrão: Webhook → Validar → Transformar → Responder/Notificar

2. **[Integração HTTP API](http_api_integration.md)**
   - Buscar dados de APIs REST → Transformar → Armazenar/Usar
   - Padrão: Trigger → HTTP Request → Transformar → Ação → Tratador de Erro

3. **[Operações de Banco de Dados](database_operations.md)**
   - Ler/Escrever/Sincronizar dados de banco de dados
   - Padrão: Agendamento → Query → Transformar → Escrever → Verificar

4. **[Workflow de Agente IA](ai_agent_workflow.md)**
   - Agentes IA com ferramentas e memória
   - Padrão: Trigger → Agente IA (Modelo + Ferramentas + Memória) → Saída

5. **[Tarefas Agendadas](scheduled_tasks.md)**
   - Workflows de automação recorrentes
   - Padrão: Agendamento → Buscar → Processar → Entregar → Registrar

---

## Guia de Seleção de Padrão

### Quando usar cada padrão:

**Processamento de Webhook** - Use quando:
- Receber dados de sistemas externos
- Construir integrações (comandos Slack, envios de formulários, webhooks GitHub)
- Precisa de resposta instantânea a eventos
- Exemplo: "Receber webhook de pagamento Stripe → Atualizar banco de dados → Enviar confirmação"

**Integração HTTP API** - Use quando:
- Buscar dados de APIs externas
- Sincronizar com serviços de terceiros
- Construir pipelines de dados
- Exemplo: "Buscar issues GitHub → Transformar → Criar tickets Jira"

**Operações de Banco de Dados** - Use quando:
- Sincronizar entre bancos de dados
- Executar queries de banco de dados agendadas
- Workflows ETL
- Exemplo: "Ler registros Postgres → Transformar → Escrever em MySQL"

**Workflow de Agente IA** - Use quando:
- Construir IA conversacional
- Precisa de IA com acesso a ferramentas
- Tarefas de raciocínio multi-etapas
- Exemplo: "Chat com IA que pode pesquisar docs, consultar banco de dados, enviar emails"

**Tarefas Agendadas** - Use quando:
- Relatórios ou resumos recorrentes
- Busca periódica de dados
- Tarefas de manutenção
- Exemplo: "Diariamente: Buscar analytics → Gerar relatório → Email para time"

---

## Componentes Comuns de Workflow

Todos os padrões compartilham estes blocos de construção:

### 1. Triggers
- **Webhook** - Endpoint HTTP (instantâneo)
- **Schedule** - Timing baseado em Cron (periódico)
- **Manual** - Clicar para executar (teste)
- **Polling** - Verificar mudanças (intervalos)

### 2. Fontes de Dados
- **HTTP Request** - APIs REST
- **Nós de banco de dados** - Postgres, MySQL, MongoDB
- **Nós de serviço** - Slack, Google Sheets, etc.
- **Code** - JavaScript/Python customizado

### 3. Transformação
- **Set** - Mapear/transformar campos
- **Code** - Lógica complexa
- **IF/Switch** - Roteamento condicional
- **Merge** - Combinar fluxos de dados

### 4. Saídas
- **HTTP Request** - Chamar APIs
- **Database** - Escrever dados
- **Communication** - Email, Slack, Discord
- **Storage** - Arquivos, armazenamento em nuvem

### 5. Tratamento de Erros
- **Error Trigger** - Capturar erros de workflow
- **IF** - Verificar condições de erro
- **Stop and Error** - Falha explícita
- **Continue On Fail** - Configuração por nó

---

## Checklist de Criação de Workflow

Ao construir QUALQUER workflow, siga este checklist:

### Fase de Planejamento
- [ ] Identificar o padrão (webhook, API, banco de dados, IA, agendado)
- [ ] Listar nós necessários (usar search_nodes)
- [ ] Entender fluxo de dados (entrada → transformar → saída)
- [ ] Planejar estratégia de tratamento de erros

### Fase de Implementação
- [ ] Criar workflow com trigger apropriado
- [ ] Adicionar nós de fonte de dados
- [ ] Configurar autenticação/credenciais
- [ ] Adicionar nós de transformação (Set, Code, IF)
- [ ] Adicionar nós de saída/ação
- [ ] Configurar tratamento de erros

### Fase de Validação
- [ ] Validar cada configuração de nó (validate_node_operation)
- [ ] Validar workflow completo (validate_workflow)
- [ ] Testar com dados de amostra
- [ ] Tratar casos extremos (dados vazios, erros)

### Fase de Implantação
- [ ] Revisar configurações de workflow (ordem de execução, timeout, tratamento de erros)
- [ ] Ativar workflow ⚠️ **Ativação manual necessária na interface n8n** (API/MCP não conseguem ativar)
- [ ] Monitorar primeiras execuções
- [ ] Documentar propósito do workflow e fluxo de dados

---

## Padrões de Fluxo de Dados

### Fluxo Linear
```
Trigger → Transformar → Ação → Fim
```
**Use quando**: Workflows simples com caminho único

### Fluxo com Ramificação
```
Trigger → IF → [Caminho Verdadeiro]
            └→ [Caminho Falso]
```
**Use quando**: Ações diferentes baseadas em condições

### Processamento Paralelo
```
Trigger → [Branch 1] → Merge
       └→ [Branch 2] ↗
```
**Use quando**: Operações independentes que podem rodar simultaneamente

### Padrão de Loop
```
Trigger → Split in Batches → Processar → Loop (até acabar)
```
**Use quando**: Processar grandes conjuntos de dados em chunks

### Padrão de Tratador de Erro
```
Fluxo Principal → [Caminho de Sucesso]
              └→ [Error Trigger → Tratador de Erro]
```
**Use quando**: Precisar de workflow de tratamento de erro separado

---

## Problemas Comuns

### 1. Estrutura de Dados de Webhook
**Problema**: Não consegue acessar dados de payload de webhook

**Solução**: Dados estão aninhados sob `$json.body`
```javascript
❌ {{$json.email}}
✅ {{$json.body.email}}
```
Veja: skill n8n Expression Syntax

### 2. Múltiplos Itens de Entrada
**Problema**: Nó processa todos os itens de entrada, mas quero apenas um

**Solução**: Use modo "Execute Once" ou processe apenas o primeiro item
```javascript
{{$json[0].field}}  // Apenas primeiro item
```

### 3. Problemas de Autenticação
**Problema**: Chamadas de API falhando com 401/403

**Solução**:
- Configurar credenciais apropriadamente
- Usar a seção "Credentials", não parâmetros
- Testar credenciais antes de ativar workflow

### 4. Ordem de Execução de Nó
**Problema**: Nós executando em ordem inesperada

**Solução**: Verificar configurações de workflow → Execution Order
- v0: De cima para baixo (legado)
- v1: Baseado em conexão (recomendado)

### 5. Erros de Expressão
**Problema**: Expressões aparecendo como texto literal

**Solução**: Use {{}} ao redor de expressões
- Veja skill n8n Expression Syntax para detalhes

---

## Integração com Outras Skills

Essas skills funcionam juntas com Padrões de Workflow:

**n8n MCP Tools Expert** - Use para:
- Encontrar nós para seu padrão (search_nodes)
- Entender operações de nó (get_node_essentials)
- Criar workflows (n8n_create_workflow)

**n8n Expression Syntax** - Use para:
- Escrever expressões em nós de transformação
- Acessar dados de webhook corretamente ({{$json.body.field}})
- Referenciar nós anteriores ({{$node["Node Name"].json.field}})

**n8n Node Configuration** - Use para:
- Configurar operações específicas para nós de padrão
- Entender requisitos específicos de nó

**n8n Validation Expert** - Use para:
- Validar estrutura de workflow
- Corrigir erros de validação
- Garantir correção de workflow antes da implantação

---

## Estatísticas de Padrão

Padrões comuns de workflow:

**Triggers Mais Comuns**:
1. Webhook - 35%
2. Schedule (tarefas periódicas) - 28%
3. Manual (teste/admin) - 22%
4. Service triggers (Slack, email, etc.) - 15%

**Transformações Mais Comuns**:
1. Set (mapeamento de campo) - 68%
2. Code (lógica customizada) - 42%
3. IF (roteamento condicional) - 38%
4. Switch (multi-condição) - 18%

**Saídas Mais Comuns**:
1. HTTP Request (APIs) - 45%
2. Slack - 32%
3. Escritas em banco de dados - 28%
4. Email - 24%

**Complexidade Média de Workflow**:
- Simples (3-5 nós): 42%
- Médio (6-10 nós): 38%
- Complexo (11+ nós): 20%

---

## Exemplos de Início Rápido

### Exemplo 1: Webhook Simples → Slack
```
1. Webhook (path: "form-submit", POST)
2. Set (mapear campos de formulário)
3. Slack (postar mensagem em #notifications)
```

### Exemplo 2: Relatório Agendado
```
1. Schedule (diariamente às 9 AM)
2. HTTP Request (buscar analytics)
3. Code (agregar dados)
4. Email (enviar relatório formatado)
5. Error Trigger → Slack (notificar em caso de falha)
```

### Exemplo 3: Sincronização de Banco de Dados
```
1. Schedule (a cada 15 minutos)
2. Postgres (consultar novos registros)
3. IF (verificar se registros existem)
4. MySQL (inserir registros)
5. Postgres (atualizar timestamp de sincronização)
```

### Exemplo 4: Assistente IA
```
1. Webhook (receber mensagem de chat)
2. AI Agent
   ├─ OpenAI Chat Model (ai_languageModel)
   ├─ HTTP Request Tool (ai_tool)
   ├─ Database Tool (ai_tool)
   └─ Window Buffer Memory (ai_memory)
3. Webhook Response (enviar resposta IA)
```

### Exemplo 5: Integração de API
```
1. Manual Trigger (para teste)
2. HTTP Request (GET /api/users)
3. Split In Batches (processar 100 por vez)
4. Set (transformar dados de usuário)
5. Postgres (upsert usuários)
6. Loop (voltar ao passo 3 até acabar)
```

---

## Arquivos de Padrão Detalhado

Para orientação abrangente sobre cada padrão:

- **[webhook_processing.md](webhook_processing.md)** - Padrões webhook, estrutura de dados, tratamento de resposta
- **[http_api_integration.md](http_api_integration.md)** - APIs REST, autenticação, paginação, tentativas
- **[database_operations.md](database_operations.md)** - Queries, sincronização, transações, processamento em lote
- **[ai_agent_workflow.md](ai_agent_workflow.md)** - Agentes IA, ferramentas, memória, nós langchain
- **[scheduled_tasks.md](scheduled_tasks.md)** - Agendamentos Cron, relatórios, tarefas de manutenção

---

## Exemplos de Template Real

Da biblioteca de templates n8n:

**Template #2947**: Clima para Slack
- Padrão: Tarefa Agendada
- Nós: Schedule → HTTP Request (API de clima) → Set → Slack
- Complexidade: Simples (4 nós)

**Processamento de Webhook**: Padrão mais comum
- Mais comum: Envios de formulário, webhooks de pagamento, integrações de chat

**HTTP API**: Padrão comum
- Mais comum: Busca de dados, integrações de terceiros

**Operações de Banco de Dados**: Padrão comum
- Mais comum: ETL, sincronização de dados, workflows de backup

**Agentes IA**: Crescente em uso
- Mais comum: Chatbots, geração de conteúdo, análise de dados

Use `search_templates` e `get_template` de n8n-mcp tools para encontrar exemplos!

---

## Melhores Práticas

### ✅ Faça

- Comece com o padrão mais simples que resolve seu problema
- Planeje a estrutura do workflow antes de construir
- Use tratamento de erros em todos os workflows
- Teste com dados de amostra antes de ativar
- Siga o checklist de criação de workflow
- Use nomes descritivos para nós
- Documente workflows complexos (campo de notas)
- Monitore execuções de workflow após a implantação

### ❌ Não Faça

- Construir workflows de uma vez (itere! média 56s entre edições)
- Pular validação antes de ativar
- Ignorar cenários de erro
- Usar padrões complexos quando padrões simples servem
- Codificar credenciais em parâmetros
- Esquecer de lidar com casos de dados vazios
- Misturar múltiplos padrões sem limites claros
- Implantar sem testar

---

## Resumo

**Pontos-Chave**:
1. **5 padrões centrais** cobrem 90%+ dos casos de uso de workflow
2. **Processamento de webhook** é o padrão mais comum
3. Use o **checklist de criação de workflow** para cada workflow
4. **Planejar padrão** → **Selecionar nós** → **Construir** → **Validar** → **Implantar**
5. Integre com outras skills para desenvolvimento completo de workflow

**Próximos Passos**:
1. Identificar seu padrão de caso de uso
2. Ler arquivo de padrão detalhado
3. Usar n8n MCP Tools Expert para encontrar nós
4. Seguir o checklist de criação de workflow
5. Usar n8n Validation Expert para validar

**Skills Relacionadas**:
- n8n MCP Tools Expert - Encontrar e configurar nós
- n8n Expression Syntax - Escrever expressões corretamente
- n8n Validation Expert - Validar e corrigir erros
- n8n Node Configuration - Configurar operações específicas