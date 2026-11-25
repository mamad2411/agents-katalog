---
name: programacao
description: >
  Skill especializada em programação full stack, cobrindo JavaScript/TypeScript (web, Node.js, Foundry VTT), Python (IA, automação, agentes LLM), arquitetura de sistemas, bancos de dados relacionais e NoSQL, e boas práticas de engenharia. Use esta skill sempre que o usuário pedir para escrever código, revisar bugs, projetar arquitetura, criar agentes de IA, configurar backends, estruturar bancos de dados, ou otimizar performance. Também acione quando o usuário mencionar: React, Next.js, Express, FastAPI, LangChain, Foundry VTT, módulos JS, hooks, WebSocket, Docker, API REST, testes, refatoração, ou qualquer linguagem de programação — mesmo que a pergunta pareça simples como "como faço X em Python?".
---

# Skill de Programação Full Stack

Esta skill cobre o espectro completo de desenvolvimento moderno (2025/2026):

- **JavaScript / TypeScript**: Frontend (React, Next.js), Backend (Node.js, Express), Foundry VTT (módulos, macros, hooks)
- **Python**: Backend (FastAPI, Django), IA/ML (PyTorch, Transformers), Agentes LLM (LangChain, AutoGPT)
- **Full Stack**: Arquitetura de sistemas, APIs REST/GraphQL, WebSockets, autenticação
- **Bancos de dados**: SQL (PostgreSQL, SQLite), NoSQL (MongoDB, Redis, Neo4j, Cassandra)
- **Agentes de IA**: Orquestração com LangChain/LangGraph, RAG, ferramentas, memória persistente
- **DevOps light**: Docker, CI/CD, serverless (AWS Lambda)

---

## Fluxo de Trabalho

Ao receber uma tarefa de programação, siga esta sequência mental:

1. **Classificar** — É escrita de código novo, debug, arquitetura ou revisão?
2. **Calibrar estilo** — O usuário quer uma resposta direta com código (estilo Sinon) ou uma explicação didática (estilo Cardinal)? Se não for óbvio, entregue código + explicação concisa.
3. **Identificar contexto** — Qual é a stack? Há constraints de performance, escala ou compatibilidade?
4. **Entregar** — Código funcional primeiro, explicação depois. Nunca explicação sem código quando código é pedido.

---

## Princípios de Engenharia (Base Teórica)

Esta skill é fundamentada nas referências abaixo. Consulte-as ao raciocinar sobre decisões técnicas:

### Confiabilidade, Escalabilidade, Manutenibilidade
*(Designing Data-Intensive Applications — Kleppmann)*
- **Confiabilidade**: o sistema deve funcionar corretamente mesmo com falhas de hardware, software ou humanas
- **Escalabilidade**: capacidade de lidar com crescimento de carga sem reescrever tudo
- **Manutenibilidade**: código que outros (e você no futuro) conseguem entender e modificar
- Prefira **replicação** para leitura, **particionamento** para escala horizontal
- Cuidado com **consistência eventual** em sistemas distribuídos — documente as garantias

### Abstração e Composição
*(SICP — Abelson & Sussman)*
- Programe para **interfaces, não implementações**
- Decomponha problemas em funções puras e composíveis
- Dados + procedimentos que operam sobre eles = abstração bem feita
- Evite efeitos colaterais desnecessários; prefira funções que retornam valores

### Bancos de Dados: Escolha a Ferramenta Certa
*(Seven Databases in Seven Weeks — Perkins, Redmond, Wilson)*
- **PostgreSQL**: padrão para dados relacionais, ACID, consultas complexas
- **Redis**: cache, sessões, filas leves, pub/sub
- **MongoDB**: documentos semi-estruturados, prototipação rápida
- **Neo4j**: grafos, relações complexas (ex: facções de RPG, redes sociais)
- **Cassandra**: séries temporais, alta escrita distribuída
- Use `JOIN` quando os dados são naturalmente relacionais; use documento/grafo quando não são

### Conceitos de Banco de Dados
*(Database System Concepts — Silberschatz, Korth)*
- Sempre defina **transações** quando múltiplas escritas devem ser atômicas
- Entenda os níveis de isolamento: READ COMMITTED como padrão seguro
- Índices aceleram leituras, custam escritas — não indexe tudo
- Normalize até 3NF por padrão; desnormalize com propósito e documentação

### Serverless e Arquitetura Event-Driven
*(Serverless Architectures on AWS — Sbarski)*
- AWS Lambda: ideal para tarefas curtas (<15min), sem estado, event-driven
- Use **SQS** para desacoplar produtores de consumidores
- **API Gateway + Lambda** = backend sem servidor a gerir
- Cold starts são reais — warm-up strategies para funções críticas
- Custos: cobrança por invocação e duração, não por servidor ocioso

### UX e Usabilidade no Código
*(Don't Make Me Think — Krug)*
- APIs devem ser **óbvias**: nomes de funções que descrevem o que fazem
- Convenção > configuração: siga padrões da linguagem/framework
- Se o usuário da API precisar ler a documentação para entender o nome de uma função, renomeie a função
- Erros devem ser **acionáveis**: `"email inválido"` > `"erro 422"`

---

## JavaScript / TypeScript

### Padrões de Código

```typescript
// ✅ Preferido: tipagem explícita, funções puras, nomes descritivos
async function fetchUserById(id: string): Promise<User | null> {
  const user = await db.users.findUnique({ where: { id } });
  return user ?? null;
}

// ❌ Evitar: any, callbacks aninhados, efeitos colaterais ocultos
function getUser(id: any, cb: any) {
  db.query(`SELECT * FROM users WHERE id = ${id}`, cb); // SQL injection!
}
```

### Node.js / Express — Estrutura de Projeto

```
src/
├── routes/         # definição das rotas HTTP
├── controllers/    # lógica de request/response
├── services/       # regras de negócio (sem HTTP)
├── repositories/   # acesso ao banco de dados
├── middlewares/    # auth, validação, logging
├── models/         # tipos e schemas
└── utils/          # helpers puros
```

### Foundry VTT — Padrões Específicos

```javascript
// Hook correto com debounce para evitar firing excessivo
let _debounceTimer;
Hooks.on('updateToken', (token, changes, options, userId) => {
  clearTimeout(_debounceTimer);
  _debounceTimer = setTimeout(() => {
    if (!changes.x && !changes.y) return; // early return se não é movimento
    handleTokenMovement(token, changes);
  }, 50);
});

// Estrutura de módulo moderno (manifest v10+)
export class MeuModulo {
  static ID = 'meu-modulo';

  static init() {
    Hooks.once('init', () => {
      this.registerSettings();
      this.registerHandlebarsHelpers();
    });
  }

  static registerSettings() {
    game.settings.register(this.ID, 'minhaConfig', {
      name: 'Minha Configuração',
      scope: 'world',
      config: true,
      type: Boolean,
      default: false,
    });
  }
}
```

### React / Next.js — Boas Práticas

```tsx
// ✅ Componente bem estruturado
interface CharacterCardProps {
  character: Character;
  onSelect: (id: string) => void;
}

export function CharacterCard({ character, onSelect }: CharacterCardProps) {
  return (
    <div onClick={() => onSelect(character.id)} role="button" tabIndex={0}>
      <h3>{character.name}</h3>
      <span>{character.class} — Nível {character.level}</span>
    </div>
  );
}

// Server Action (Next.js 14+) — sem API route necessária
'use server';
export async function saveCharacter(data: FormData) {
  const name = data.get('name') as string;
  await db.characters.create({ data: { name } });
  revalidatePath('/characters');
}
```

---

## Python

### Estrutura de Projeto FastAPI

```
app/
├── main.py           # entry point, criação do app
├── routers/          # APIRouter por domínio
├── schemas/          # Pydantic models (request/response)
├── models/           # SQLAlchemy models (banco)
├── services/         # lógica de negócio
├── dependencies/     # injeção de dependências (auth, db session)
└── core/
    ├── config.py     # variáveis de ambiente
    └── security.py   # JWT, hashing
```

```python
# Exemplo: endpoint bem estruturado
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.schemas import CharacterCreate, CharacterResponse
from app.services import character_service

router = APIRouter(prefix="/characters", tags=["characters"])

@router.post("/", response_model=CharacterResponse, status_code=201)
async def create_character(
    data: CharacterCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    return character_service.create(db, data, owner_id=current_user.id)
```

### Agentes de IA com LangChain / LangGraph

```python
from langchain_anthropic import ChatAnthropic
from langchain.tools import tool
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

# Definir ferramentas
@tool
def search_lore(query: str) -> str:
    """Busca informações de lore no banco de dados do mundo."""
    return lore_db.search(query)

@tool  
def create_npc(name: str, role: str, faction: str) -> dict:
    """Cria um novo NPC com os atributos fornecidos."""
    return npc_service.create(name=name, role=role, faction=faction)

# Estado do agente
class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    context: dict

# Construir grafo
llm = ChatAnthropic(model="claude-sonnet-4-20250514")
llm_with_tools = llm.bind_tools([search_lore, create_npc])

def call_llm(state: AgentState):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

graph = StateGraph(AgentState)
graph.add_node("agent", call_llm)
graph.set_entry_point("agent")
graph.add_edge("agent", END)
app = graph.compile()
```

### RAG (Retrieval-Augmented Generation)

```python
from langchain_community.vectorstores import Chroma
from langchain_anthropic import AnthropicEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Indexar documentos de lore
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(lore_documents)

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=AnthropicEmbeddings(),
    persist_directory="./lore_db"
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
```

---

## Bancos de Dados

### PostgreSQL — Padrões

```sql
-- Sempre use transações para operações múltiplas
BEGIN;
  INSERT INTO characters (name, class, level) VALUES ($1, $2, $3);
  INSERT INTO character_stats (character_id, hp, mp) VALUES (lastval(), $4, $5);
COMMIT;

-- Índices estratégicos (não indexe tudo)
CREATE INDEX idx_characters_campaign_id ON characters(campaign_id);
CREATE INDEX idx_events_created_at ON events(created_at DESC);

-- JSONB para dados semi-estruturados (atributos variáveis de personagem)
ALTER TABLE characters ADD COLUMN attributes JSONB DEFAULT '{}';
CREATE INDEX idx_characters_attributes ON characters USING GIN(attributes);
-- Query: SELECT * FROM characters WHERE attributes->>'class' = 'Guerreiro';
```

### Redis — Cache e Sessões

```typescript
import { createClient } from 'redis';

const redis = createClient({ url: process.env.REDIS_URL });

// Cache com TTL
async function getCachedUser(id: string): Promise<User | null> {
  const cached = await redis.get(`user:${id}`);
  if (cached) return JSON.parse(cached);

  const user = await db.users.findUnique({ where: { id } });
  if (user) await redis.setEx(`user:${id}`, 3600, JSON.stringify(user)); // 1h TTL
  return user;
}

// Invalidar cache ao atualizar
async function updateUser(id: string, data: Partial<User>) {
  await db.users.update({ where: { id }, data });
  await redis.del(`user:${id}`); // invalida cache
}
```

---

## Debug e Revisão de Código

Quando receber código para revisar ou debugar, analise nesta ordem:

1. **Segurança**: SQL injection, XSS, secrets expostos, inputs não validados
2. **Corretude**: lógica errada, edge cases não tratados, erros silenciosos
3. **Performance**: N+1 queries, loops desnecessários, falta de índices, memory leaks
4. **Manutenibilidade**: nomes confusos, funções longas demais (>50 linhas = suspeito), código duplicado
5. **Testes**: há testes? Os casos críticos estão cobertos?

### Checklist de Code Review

```
□ Inputs validados antes de usar?
□ Erros tratados (try/catch, .catch(), Result types)?
□ Sem secrets hardcoded (use env vars)?
□ Queries parametrizadas (sem concatenação de string em SQL)?
□ Operações assíncronas com await/Promise corretos?
□ Sem console.log esquecidos em produção?
□ Funções têm responsabilidade única?
□ Tipos explícitos (TypeScript) ou type hints (Python)?
```

---

## Arquitetura de Sistemas

### Quando usar o quê

| Necessidade | Solução |
|---|---|
| API simples, time pequeno | Express/FastAPI monolito modular |
| Alta escala, times independentes | Microsserviços (mas cuidado com complexidade) |
| Tarefas assíncronas / background | Filas (BullMQ, SQS, Celery) |
| Eventos em tempo real | WebSocket (Socket.io) ou SSE |
| Funções esporádicas, sem servidor | AWS Lambda / Vercel Functions |
| Dados relacionais estruturados | PostgreSQL |
| Cache / sessões / pub-sub | Redis |
| Documentos flexíveis | MongoDB |
| Grafos e relações complexas | Neo4j |
| Busca full-text | Elasticsearch / pgvector (com embeddings) |

### Serverless (AWS Lambda) — Quando faz sentido

✅ Use quando: processamento event-driven, tarefas curtas (<15min), carga imprevisível, sem estado
❌ Evite quando: latência consistente é crítica (cold starts), processamento longo, WebSockets persistentes

```python
# Lambda handler bem estruturado
import json
import logging
from typing import Any

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event: dict, context: Any) -> dict:
    try:
        body = json.loads(event.get('body', '{}'))
        # lógica aqui
        result = process(body)
        return {'statusCode': 200, 'body': json.dumps(result)}
    except ValueError as e:
        logger.warning(f"Input inválido: {e}")
        return {'statusCode': 400, 'body': json.dumps({'error': str(e)})}
    except Exception as e:
        logger.error(f"Erro interno: {e}", exc_info=True)
        return {'statusCode': 500, 'body': json.dumps({'error': 'Erro interno'})}
```

---

## Testes

```typescript
// Jest — estrutura de teste clara
describe('CharacterService', () => {
  describe('create', () => {
    it('deve criar personagem com atributos válidos', async () => {
      const data = { name: 'Aragorn', class: 'Ranger', level: 1 };
      const result = await characterService.create(data);
      expect(result).toMatchObject({ name: 'Aragorn', class: 'Ranger' });
      expect(result.id).toBeDefined();
    });

    it('deve lançar erro para nome vazio', async () => {
      await expect(characterService.create({ name: '' }))
        .rejects.toThrow('Nome é obrigatório');
    });
  });
});
```

```python
# pytest — testes com fixtures
import pytest
from app.services import character_service

@pytest.fixture
def sample_character():
    return {"name": "Legolas", "class": "Ranger", "level": 5}

def test_create_character(db_session, sample_character):
    result = character_service.create(db_session, sample_character)
    assert result.name == "Legolas"
    assert result.id is not None

def test_create_character_empty_name(db_session):
    with pytest.raises(ValueError, match="Nome é obrigatório"):
        character_service.create(db_session, {"name": ""})
```

---

## Referências dos Livros Disponíveis

Ao raciocinar sobre problemas complexos, consulte mentalmente:

- **Kleppmann (DDIA)**: decisões sobre consistência, replicação, encodings de dados
- **SICP**: problemas de abstração, recursão, design de linguagens/interpreters
- **Silberschatz (DB Concepts)**: normalização, transações, controle de concorrência
- **Seven Databases**: escolha de banco de dados, trade-offs NoSQL vs SQL
- **Sbarski (Serverless AWS)**: arquitetura event-driven, Lambda, SQS, API Gateway
- **Krug (Don't Make Me Think)**: usabilidade de APIs, naming, experiência do desenvolvedor
