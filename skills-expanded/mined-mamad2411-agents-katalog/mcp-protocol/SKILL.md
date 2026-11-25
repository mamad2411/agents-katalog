---
name: MCP Protocol & FastMCP
description: Model Context Protocol — conceitos, FastMCP SDK, tools/resources/prompts, transporte, e patterns de servidor MCP em Python.
---

# MCP Protocol & FastMCP

## Quando Usar

- Ao criar ou modificar tools, resources ou prompts MCP
- Ao configurar o transporte do servidor
- Ao integrar o servidor MCP com hosts (Claude, Codex, etc.)

## O que é MCP

**Model Context Protocol** = padrão aberto (Anthropic, Nov/2024) para integrar LLMs com ferramentas externas. Funciona como "USB-C para IA" — resolve M×N integrações.

**Arquitetura:**
```
Host (Claude/Codex) → Client (bridge JSON-RPC) → Server (provedor de contexto)
```

**Protocolo:** JSON-RPC 2.0 sobre stdio ou Streamable HTTP.

## FastMCP — SDK Python

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("memory-server", description="Sistema de memória híbrida")
```

### Tools — Funções Executáveis

```python
@mcp.tool()
async def memory_query(project: str, query_text: str | None = None, top_k: int = 10) -> list[dict]:
    """Consulta memórias por projeto e/ou texto semântico.
    Use para buscar regras, padrões ou decisões existentes."""
    ...
```

**Regras de Tools:**
- `@mcp.tool()` registra como tool MCP
- Type hints = schema de entrada (gerado automaticamente)
- Docstring = descrição que o LLM vê (CRITICAL — seja claro e prescritivo)
- Return type = schema de saída

### Resources — Leitura Pronta

```python
@mcp.resource("mem://project/{project}/top-patterns")
async def top_patterns(project: str) -> str:
    """Retorna os top DesignPatterns do projeto.
    Consulte ANTES de iniciar qualquer tarefa."""
    ...
```

**Regras de Resources:**
- URI template com `{param}` para parametrização
- Retorno é `str` (texto formatado)
- Agente lê resources ANTES de agir (pré-task context)

### Prompts — Templates de Extração

```python
@mcp.prompt()
def summarize_work_item(task_description: str, changes: str) -> str:
    """Gera resumo estruturado para extração de conhecimento."""
    return f"""Analise a tarefa e mudanças. Extraia conhecimento durável em JSON.
    TAREFA: {task_description}
    MUDANÇAS: {changes}"""
```

**Regras de Prompts:**
- Prompts são templates, não executam lógica
- Retornam string formatada que o LLM usará
- Definem o formato esperado da resposta (JSON Schema ideal)

## Organização de Código

```python
# server/main.py — entry point
mcp = FastMCP("memory-server")
register_tools(mcp)
register_resources(mcp)
register_prompts(mcp)

# server/tools.py — tools registrados via função
def register_tools(mcp: FastMCP):
    @mcp.tool()
    async def memory_query(...):
        ...

# server/resources.py — resources registrados via função
def register_resources(mcp: FastMCP):
    @mcp.resource("mem://projects")
    async def list_projects():
        ...
```

## Transporte

| Cenário | Transporte | Comando |
|---------|-----------|---------|
| MVP local | `stdio` | `python -m server.main` |
| Serviço HTTP | `Streamable HTTP` | `mcp run server/main.py --transport http --port 8080` |

## Integração com Hosts

```json
// Configuração para Claude Desktop / Codex
{
  "mcpServers": {
    "memory": {
      "command": "python",
      "args": ["-m", "server.main"],
      "cwd": "/path/to/memory-server"
    }
  }
}
```

## Regras

- Docstrings são o contrato com o LLM — sejam descritivas e prescritivas
- Tools para ação (write), Resources para leitura (read), Prompts para extração
- Delegar lógica para services — tools são "thin controllers"
- Usar DI container em vez de instanciar services como globals
