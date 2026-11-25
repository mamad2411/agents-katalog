---
name: autogpt-agents
description: Plataforma autônoma de agentes de IA para construir e implantar agentes contínuos. Use ao criar agentes de workflow visual, implantar agentes autônomos persistentes ou construir sistemas complexos de automação de IA com múltiplas etapas.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Agents, AutoGPT, Autonomous Agents, Workflow Automation, Visual Builder, AI Platform]
dependencies: [autogpt-platform>=0.4.0]
---

# AutoGPT - Plataforma de Agentes de IA Autônomos

Plataforma abrangente para construir, implantar e gerenciar agentes de IA contínuos através de uma interface visual ou kit de desenvolvimento.

## Quando usar AutoGPT

**Use AutoGPT quando:**
- Construindo agentes autônomos que rodam continuamente
- Criando agentes de IA baseados em workflow visual
- Implantando agentes com triggers externos (webhooks, agendamentos)
- Construindo pipelines complexos de automação com múltiplas etapas
- Necessitando de um agent builder sem código/baixo código

**Principais características:**
- **Visual Agent Builder**: Editor de workflow baseado em nós com drag-and-drop
- **Execução Contínua**: Agentes rodam persistentemente com triggers
- **Marketplace**: Agentes pré-construídos e blocos para compartilhar/reutilizar
- **Sistema de Blocos**: Componentes modulares para LLM, ferramentas, integrações
- **Forge Toolkit**: Ferramentas de desenvolvimento para criação customizada de agentes
- **Sistema de Benchmark**: Testes padronizados de desempenho de agentes

**Use alternativas em vez disso:**
- **LangChain/LlamaIndex**: Se você precisa de mais controle sobre a lógica do agente
- **CrewAI**: Para colaboração multi-agente baseada em papéis
- **OpenAI Assistants**: Para implantações simples de agentes hospedados
- **Semantic Kernel**: Para integração com ecossistema Microsoft

## Início rápido

### Instalação (Docker)

```bash
# Clone repositório
git clone https://github.com/Significant-Gravitas/AutoGPT.git
cd AutoGPT/autogpt_platform

# Copie arquivo de ambiente
cp .env.example .env

# Inicie serviços backend
docker compose up -d --build

# Inicie frontend (em terminal separado)
cd frontend
cp .env.example .env
npm install
npm run dev
```

### Acesse a plataforma

- **Interface Frontend**: http://localhost:3000
- **API Backend**: http://localhost:8006/api
- **WebSocket**: ws://localhost:8001/ws

## Visão geral da arquitetura

AutoGPT possui dois sistemas principais:

### AutoGPT Platform (Produção)
- Agent builder visual com frontend React
- Backend FastAPI com execution engine
- Infraestrutura PostgreSQL + Redis + RabbitMQ

### AutoGPT Classic (Desenvolvimento)
- **Forge**: Kit de desenvolvimento de agentes
- **Benchmark**: Framework de testes de desempenho
- **CLI**: Interface de linha de comando para desenvolvimento

## Conceitos principais

### Graphs e nodes

Agentes são representados como **graphs** contendo **nodes** conectados por **links**:

```
Graph (Agent)
  ├── Node (Input)
  │   └── Block (AgentInputBlock)
  ├── Node (Process)
  │   └── Block (LLMBlock)
  ├── Node (Decision)
  │   └── Block (SmartDecisionMaker)
  └── Node (Output)
      └── Block (AgentOutputBlock)
```

### Blocos

Blocos são componentes funcionais reutilizáveis:

| Tipo de Bloco | Propósito |
|------------|---------|
| `INPUT` | Pontos de entrada do agente |
| `OUTPUT` | Saídas do agente |
| `AI` | Chamadas de LLM, geração de texto |
| `WEBHOOK` | Triggers externos |
| `STANDARD` | Operações gerais |
| `AGENT` | Execução de agente aninhado |

### Fluxo de execução

```
User/Trigger → Graph Execution → Node Execution → Block.execute()
     ↓              ↓                 ↓
  Inputs      Queue System      Output Yields
```

## Construindo agentes

### Usando o agent builder visual

1. **Abra Agent Builder** em http://localhost:3000
2. **Adicione blocos** do painel BlocksControl
3. **Conecte nodes** arrastando entre handles
4. **Configure inputs** em cada node
5. **Execute agente** usando PrimaryActionBar

### Blocos disponíveis

**Blocos de IA:**
- `AITextGeneratorBlock` - Gere texto com LLMs
- `AIConversationBlock` - Conversas multi-turno
- `SmartDecisionMakerBlock` - Lógica condicional

**Blocos de Integração:**
- Conectores GitHub, Google, Discord, Notion
- Triggers webhook e handlers
- Blocos de requisição HTTP

**Blocos de Controle:**
- Blocos de Input/Output
- Nós de branching e decisão
- Blocos de loop e iteração

## Execução do agente

### Tipos de trigger

**Execução manual:**
```http
POST /api/v1/graphs/{graph_id}/execute
Content-Type: application/json

{
  "inputs": {
    "input_name": "value"
  }
}
```

**Trigger webhook:**
```http
POST /api/v1/webhooks/{webhook_id}
Content-Type: application/json

{
  "data": "webhook payload"
}
```

**Execução agendada:**
```json
{
  "schedule": "0 */2 * * *",
  "graph_id": "graph-uuid",
  "inputs": {}
}
```

### Monitorando execução

**Atualizações WebSocket:**
```javascript
const ws = new WebSocket('ws://localhost:8001/ws');

ws.onmessage = (event) => {
  const update = JSON.parse(event.data);
  console.log(`Node ${update.node_id}: ${update.status}`);
};
```

**REST API polling:**
```http
GET /api/v1/executions/{execution_id}
```

## Usando Forge (Desenvolvimento)

### Crie agente customizado

```bash
# Configure ambiente forge
cd classic
./run setup

# Crie novo agente a partir de template
./run forge create my-agent

# Inicie servidor do agente
./run forge start my-agent
```

### Estrutura do agente

```
my-agent/
├── agent.py          # Lógica principal do agente
├── abilities/        # Habilidades customizadas
│   ├── __init__.py
│   └── custom.py
├── prompts/          # Templates de prompt
└── config.yaml       # Configuração do agente
```

### Implemente habilidade customizada

```python
from forge import Ability, ability

@ability(
    name="custom_search",
    description="Search for information",
    parameters={
        "query": {"type": "string", "description": "Search query"}
    }
)
def custom_search(query: str) -> str:
    """Custom search ability."""
    # Implemente lógica de busca
    result = perform_search(query)
    return result
```

## Benchmarking de agentes

### Execute benchmarks

```bash
# Execute todos os benchmarks
./run benchmark

# Execute categoria específica
./run benchmark --category coding

# Execute com agente específico
./run benchmark --agent my-agent
```

### Categorias de benchmark

- **Coding**: Geração e debug de código
- **Retrieval**: Busca de informações
- **Web**: Navegação e interação na web
- **Writing**: Tarefas de geração de texto

### VCR cassettes

Benchmarks usam respostas HTTP gravadas para reprodutibilidade:

```bash
# Grave cassettes novos
./run benchmark --record

# Execute com cassettes existentes
./run benchmark --playback
```

## Integrações

### Adicionando credenciais

1. Navegue para Profile > Integrations
2. Selecione provider (OpenAI, GitHub, Google, etc.)
3. Digite chaves de API ou autorize OAuth
4. Credenciais são criptografadas e armazenadas com segurança

### Usando credenciais em blocos

Blocos acessam automaticamente credenciais do usuário:

```python
class MyLLMBlock(Block):
    def execute(self, inputs):
        # Credenciais são injetadas pelo sistema
        credentials = self.get_credentials("openai")
        client = OpenAI(api_key=credentials.api_key)
        # ...
```

### Providers suportados

| Provider | Tipo de Auth | Casos de Uso |
|----------|-----------|-----------|
| OpenAI | API Key | LLM, embeddings |
| Anthropic | API Key | Modelos Claude |
| GitHub | OAuth | Código, repos |
| Google | OAuth | Drive, Gmail, Calendar |
| Discord | Bot Token | Mensagens |
| Notion | OAuth | Documentos |

## Implantação

### Setup Docker para produção

```yaml
# docker-compose.prod.yml
services:
  rest_server:
    image: autogpt/platform-backend
    environment:
      - DATABASE_URL=postgresql://...
      - REDIS_URL=redis://redis:6379
    ports:
      - "8006:8006"

  executor:
    image: autogpt/platform-backend
    command: poetry run executor

  frontend:
    image: autogpt/platform-frontend
    ports:
      - "3000:3000"
```

### Variáveis de ambiente

| Variável | Propósito |
|----------|---------|
| `DATABASE_URL` | Conexão PostgreSQL |
| `REDIS_URL` | Conexão Redis |
| `RABBITMQ_URL` | Conexão RabbitMQ |
| `ENCRYPTION_KEY` | Criptografia de credenciais |
| `SUPABASE_URL` | Autenticação |

### Gere chave de criptografia

```bash
cd autogpt_platform/backend
poetry run cli gen-encrypt-key
```

## Melhores práticas

1. **Comece simples**: Comece com agentes de 3-5 nodes
2. **Teste incrementalmente**: Execute e teste após cada mudança
3. **Use webhooks**: Triggers externos para agentes orientados a eventos
4. **Monitore custos**: Rastreie uso de API de LLM via sistema de créditos
5. **Versione agentes**: Salve versões funcionando antes de mudanças
6. **Benchmark**: Use agbenchmark para validar qualidade do agente

## Problemas comuns

**Serviços não iniciando:**
```bash
# Verifique status dos containers
docker compose ps

# Veja logs
docker compose logs rest_server

# Reinicie serviços
docker compose restart
```

**Problemas de conexão com banco de dados:**
```bash
# Execute migrações
cd backend
poetry run prisma migrate deploy
```

**Execução do agente travada:**
```bash
# Verifique fila RabbitMQ
# Visite http://localhost:15672 (guest/guest)

# Limpe execuções travadas
docker compose restart executor
```

## Referências

- **[Advanced Usage](references/advanced-usage.md)** - Blocos customizados, implantação, escalabilidade
- **[Troubleshooting](references/troubleshooting.md)** - Problemas comuns, debug

## Recursos

- **Documentação**: https://docs.agpt.co
- **Repositório**: https://github.com/Significant-Gravitas/AutoGPT
- **Discord**: https://discord.gg/autogpt
- **License**: MIT (Classic) / Polyform Shield (Platform)