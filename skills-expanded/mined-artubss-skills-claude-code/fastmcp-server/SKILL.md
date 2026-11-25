---
name: fastmcp-server
description: Guia completo para construir servidores MCP com FastMCP 3.0 - tools, resources, autenticação, providers, middleware e deploy. Use ao criar servidores MCP em Python ou integrar modelos de IA com ferramentas e dados externos.
version: 1.0.0
author: FastMCP Community
license: MIT
tags: [FastMCP, MCP, Python, AI, Tools, Server, Authentication, Providers]
dependencies: []
---

# Desenvolvimento de Servidores FastMCP 3.0

Referência completa para construir servidores MCP (Model Context Protocol) prontos para produção com FastMCP 3.0 - o framework Pythônico rápido para conectar LLMs a ferramentas e dados.

## Quando usar esta skill

**Use FastMCP Server quando:**
- Criar um novo servidor MCP em Python
- Adicionar tools, resources ou prompts a um servidor MCP
- Implementar autenticação (OAuth, OIDC, verificação de token)
- Configurar middleware para logging, rate limiting ou autorização
- Configurar providers (local, filesystem, skills, customizado)
- Construir servidores MCP para produção com telemetria e storage
- Fazer upgrade de FastMCP 2.x para 3.0

**Áreas-chave cobertas:**
- **Tools & Resources** (CORE): Decoradores, validação, tipos de retorno, templates
- **Context & DI** (CORE): Contexto MCP, injeção de dependência, background tasks
- **Autenticação** (SECURITY): OAuth, OIDC, verificação de token, padrões de proxy
- **Autorização** (SECURITY): Controle de acesso baseado em escopo e role
- **Middleware** (ADVANCED): Pipeline de request/response, middleware integrado
- **Providers** (ADVANCED): Local, filesystem, skills e providers customizados
- **Features** (ADVANCED): Paginação, sampling, storage, OpenTelemetry, versionamento

## Referência rápida

### Padrões principais

**Criar um servidor com tools:**
```python
from fastmcp import FastMCP

mcp = FastMCP("MyServer")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b
```

**Criar um resource:**
```python
@mcp.resource("data://config")
def get_config() -> dict:
    """Return server configuration"""
    return {"version": "1.0", "debug": False}
```

**Criar um template de resource:**
```python
@mcp.resource("users://{user_id}/profile")
def get_user_profile(user_id: str) -> dict:
    """Get a user's profile by ID"""
    return fetch_user(user_id)
```

**Criar um prompt:**
```python
@mcp.prompt
def review_code(code: str, language: str = "python") -> str:
    """Review code for best practices"""
    return f"Review this {language} code:\n\n{code}"
```

**Executar o servidor:**
```python
if __name__ == "__main__":
    mcp.run()

# Or with transport options:
# mcp.run(transport="sse", host="0.0.0.0", port=8000)
```

### Usar context em tools

```python
from fastmcp import FastMCP, Context

mcp = FastMCP("MyServer")

@mcp.tool
def process_data(uri: str, ctx: Context) -> str:
    """Process data with logging and progress"""
    ctx.info(f"Processing {uri}")
    ctx.report_progress(0, 100)
    data = ctx.read_resource(uri)
    ctx.report_progress(100, 100)
    return f"Processed: {data}"
```

### Configuração de autenticação

```python
from fastmcp import FastMCP
from fastmcp.server.auth import BearerAuthProvider

auth = BearerAuthProvider(
    jwks_uri="https://your-provider/.well-known/jwks.json",
    audience="your-api",
    issuer="https://your-provider/"
)

mcp = FastMCP("SecureServer", auth=auth)
```

## Conceitos-chave

### Tools
Funções expostas como capacidades executáveis para LLMs. Decoradas com `@mcp.tool`. Suportam validação Pydantic, async, tipos de retorno customizados e anotações (readOnlyHint, destructiveHint).

### Resources & Templates
Fontes de dados estáticas ou dinâmicas identificadas por URIs. Resources usam URIs fixos (`data://config`), templates usam URIs parametrizados (`users://{id}/profile`). Suportam tipos MIME, anotações e parâmetros com wildcard.

### Context
O objeto `Context` fornece acesso a recursos MCP dentro de tools/resources: logging, report de progresso, acesso a resources, sampling de LLM, elicitação de usuário e estado de sessão.

### Injeção de Dependência
Injete valores em funções de tool/resource usando `Depends()`. Suporta requisições HTTP, access tokens, dependências customizadas e padrões baseados em gerador para limpeza.

### Providers
Controle de onde os componentes vêm. `LocalProvider` (padrão, baseado em decorador), `FileSystemProvider` (carrega de arquivos Python em disco), `SkillsProvider` (bundles empacotados) ou providers customizados.

### Autenticação & Autorização
Múltiplos padrões de autenticação: verificação de token (JWT, JWKS), proxy OAuth, proxy OIDC, OAuth remoto e servidor OAuth completo. Autorização via escopos em componentes e middleware.

### Middleware
Intercepte e modifique requests/responses. Middleware integrado para rate limiting, tratamento de erros, logging e limites de tamanho de response. Middleware customizado via `@mcp.middleware`.

## Usando as referências

A documentação detalhada está organizada na pasta `references/`:

### Primeiros Passos
- **getting-started/installation.md** - Instale FastMCP, dependências opcionais, verifique setup
- **getting-started/upgrade-guide.md** - Migre de FastMCP 2.x para 3.0
- **getting-started/quickstart.md** - Primeiro servidor, tools, resources, prompts, executar

### Server
- **server/server-class.md** - Configuração do servidor FastMCP, opções de transport, filtro de tags
- **server/tools.md** - Decorador tool, parâmetros, validação, tipos de retorno, anotações
- **server/resources-and-templates.md** - Resources, templates, URIs, wildcards, tipos MIME

### Context
- **context/mcp-context.md** - Objeto Context, logging, progresso, acesso a resources, sampling
- **context/background-tasks.md** - Operações de longa duração com suporte a tasks
- **context/dependency-injection.md** - Depends(), deps customizadas, requisição HTTP, access tokens
- **context/user-elicitation.md** - Solicite entrada estruturada de usuários durante execução

### Features
- **features/icons.md** - Ícones customizados para tools, resources, prompts e servidores
- **features/lifespans.md** - Gerenciamento de ciclo de vida do servidor e hooks de startup/shutdown
- **features/client-logging.md** - Envie mensagens de log para clientes MCP
- **features/middleware.md** - Pipeline de request/response, middleware integrado e customizado
- **features/pagination.md** - Paginação de listas grandes de componentes
- **features/progress-reporting.md** - Reporte progresso para operações de longa duração
- **features/sampling.md** - Solicite conclusões de LLM do cliente
- **features/storage-backends.md** - Storage em memória, arquivo e Redis para cache e tokens
- **features/opentelemetry.md** - Rastreamento distribuído e observabilidade
- **features/versioning.md** - Versione componentes e filtre por intervalos de versão

### Autenticação
- **authentication/token-verification.md** - JWT, JWKS, introspection, chaves estáticas, customizado
- **authentication/remote-oauth.md** - Delegue autenticação ao provider OAuth upstream
- **authentication/oauth-proxy.md** - Proxy OAuth completo com PKCE, gerenciamento de clientes
- **authentication/oidc-proxy.md** - Proxy OpenID Connect com auto-discovery
- **authentication/full-oauth-server.md** - Servidor OAuth completo integrado

### Autorização
- **authorization.md** - Controle de acesso baseado em escopo, autorização em middleware, padrões

### Providers
- **providers/local.md** - Provider padrão, registro de componentes baseado em decorador
- **providers/filesystem.md** - Carregue componentes de arquivos Python em disco
- **providers/skills.md** - Empacote e distribua bundles de componentes
- **providers/custom.md** - Construa providers customizados para qualquer fonte de componente

## Histórico de versões

**v1.0.0** (Fevereiro de 2026)
- Lançamento inicial cobrindo FastMCP 3.0 (release candidate)
- 30 arquivos de referência em 7 categorias
- Cobertura completa de tools, resources, context, autenticação, providers e features