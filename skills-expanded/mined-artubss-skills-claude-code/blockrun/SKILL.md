---
name: blockrun
description: Use quando o usuário precisar de capacidades que Claude não tem (geração de imagens, dados em tempo real do X/Twitter) ou solicitar explicitamente modelos externos ("blockrun", "use grok", "use gpt", "dall-e", "deepseek")
allowed-tools: Read, Bash(python:*), Bash(python3:*), Bash(pip:*), Bash(source:*)
---

# BlockRun

**BlockRun funciona com Claude Code e Google Antigravity.**

Você não consegue gerar imagens. Você não tem acesso em tempo real ao X/Twitter. BlockRun oferece essas capacidades.

## Filosofia

Você tem uma carteira. Quando precisa de uma capacidade que não tem, você a paga autonomamente.

| Você Precisa | Você Chama | Preço |
|----------|----------|---------|
| Geração de imagens | DALL-E | $0.04/imagem |
| Dados em tempo real do X | Grok + Live Search | $0.025/fonte |
| Segunda opinião | GPT-5.2 | $1.75/M entrada, $14/M saída |
| Processamento mais barato | DeepSeek | $0.14/M entrada, $0.28/M saída |

**Como funciona:** BlockRun usa micropagamentos x402 para rotear suas solicitações para OpenAI, xAI, Google e outros provedores. Sem necessidade de chaves de API - sua carteira paga por token.

## Controle de Orçamento (Opcional)

Se o usuário especificar um orçamento (ex: "use no máximo $1"), rastreie os gastos e pare quando o orçamento for atingido:

```python
from blockrun_llm import setup_agent_wallet

client = setup_agent_wallet()
budget = 1.0  # Orçamento do usuário

# Antes de cada chamada, verifique se está dentro do orçamento
spending = client.get_spending()
if spending['total_usd'] >= budget:
    print(f"Orçamento atingido: ${spending['total_usd']:.4f} gastos")
    # Pare de fazer chamadas
else:
    response = client.chat("openai/gpt-5.2", "Olá!")

# No final, relatar gastos
spending = client.get_spending()
print(f"💰 Total gasto: ${spending['total_usd']:.4f} em {spending['calls']} chamadas")
```

## Quando Usar

| Gatilho | Sua Ação |
|---------|-------------|
| Usuário solicita explicitamente ("blockrun segunda opinião com GPT em...", "use grok para verificar...", "gerar imagem com dall-e") | Execute via BlockRun |
| Usuário precisa de algo que você não consegue fazer (imagens, dados em tempo real do X) | Sugira BlockRun, aguarde confirmação |
| Você consegue lidar com a tarefa normalmente | Faça você mesmo, não mencione BlockRun |

## Exemplos de Prompts de Usuário

Usuários dirão coisas como:

| Usuário Diz | O que Você Faz |
|-----------|-------------|
| "blockrun gerar uma imagem de um pôr do sol" | Chame DALL-E via ImageClient |
| "use grok para verificar o que está em tendência no X" | Chame Grok com `search=True` |
| "blockrun GPT revise este código" | Chame GPT-5.2 via LLMClient |
| "qual é a notícia mais recente sobre agentes de IA?" | Sugira Grok (você não tem dados em tempo real) |
| "gerar um logo para minha startup" | Sugira DALL-E (você não consegue gerar imagens) |
| "blockrun verificar meu saldo" | Mostre saldo da carteira via `get_balance()` |
| "blockrun deepseek resumir este arquivo" | Chame DeepSeek para economizar custos |

## Carteira e Saldo

Use `setup_agent_wallet()` para criar automaticamente uma carteira e obter um cliente. Mostra o código QR e mensagem de boas-vindas no primeiro uso.

**Inicializar cliente (sempre comece com isso):**
```python
from blockrun_llm import setup_agent_wallet

client = setup_agent_wallet()  # Cria carteira automaticamente, mostra QR se novo
```

**Verificar saldo (quando usuário pede "mostrar saldo", "verificar carteira", etc.):**
```python
balance = client.get_balance()  # Saldo USDC on-chain
print(f"Saldo: ${balance:.2f} USDC")
print(f"Carteira: {client.get_wallet_address()}")
```

**Mostrar código QR para financiamento:**
```python
from blockrun_llm import generate_wallet_qr_ascii, get_wallet_address

# QR ASCII para exibição em terminal
print(generate_wallet_qr_ascii(get_wallet_address()))
```

## Uso do SDK

**Pré-requisito:** Instale o SDK com `pip install blockrun-llm`

### Chat Básico
```python
from blockrun_llm import setup_agent_wallet

client = setup_agent_wallet()  # Cria carteira automaticamente se necessário
response = client.chat("openai/gpt-5.2", "Quanto é 2+2?")
print(response)

# Verificar gastos
spending = client.get_spending()
print(f"Gasto ${spending['total_usd']:.4f}")
```

### Busca em Tempo Real do X/Twitter (xAI Live Search)

**IMPORTANTE:** Para dados em tempo real do X/Twitter, você DEVE ativar Live Search com `search=True` ou `search_parameters`.

```python
from blockrun_llm import setup_agent_wallet

client = setup_agent_wallet()

# Simples: Ativar busca em tempo real com search=True
response = client.chat(
    "xai/grok-3",
    "Quais são as postagens mais recentes de @blockrunai no X?",
    search=True  # Ativa busca em tempo real do X/Twitter
)
print(response)
```

### Busca Avançada no X com Filtros

```python
from blockrun_llm import setup_agent_wallet

client = setup_agent_wallet()

response = client.chat(
    "xai/grok-3",
    "Analise o conteúdo recente e engajamento de @blockrunai",
    search_parameters={
        "mode": "on",
        "sources": [
            {
                "type": "x",
                "included_x_handles": ["blockrunai"],
                "post_favorite_count": 5
            }
        ],
        "max_search_results": 20,
        "return_citations": True
    }
)
print(response)
```

### Geração de Imagens
```python
from blockrun_llm import ImageClient

client = ImageClient()
result = client.generate("Um gato fofo usando um capacete de astronauta")
print(result.data[0].url)
```

## Referência xAI Live Search

Live Search é a API de dados em tempo real da xAI. Custo: **$0.025 por fonte** (padrão 10 fontes = ~$0.26).

Para reduzir custos, defina `max_search_results` para um valor menor:
```python
# Use apenas 5 fontes (~$0.13)
response = client.chat("xai/grok-3", "O que está em tendência?",
    search_parameters={"mode": "on", "max_search_results": 5})
```

### Parâmetros de Busca

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|---------|-------------|
| `mode` | string | "auto" | "off", "auto" ou "on" |
| `sources` | array | web,news,x | Fontes de dados para consultar |
| `return_citations` | bool | true | Incluir URLs de fontes |
| `from_date` | string | - | Data de início (YYYY-MM-DD) |
| `to_date` | string | - | Data de término (YYYY-MM-DD) |
| `max_search_results` | int | 10 | Máx de fontes a retornar (customize para controlar custo) |

### Tipos de Fonte

**Fonte X/Twitter:**
```python
{
    "type": "x",
    "included_x_handles": ["handle1", "handle2"],  # Máx 10
    "excluded_x_handles": ["spam_account"],        # Máx 10
    "post_favorite_count": 100,  # Limiar mín de curtidas
    "post_view_count": 1000      # Limiar mín de visualizações
}
```

**Fonte Web:**
```python
{
    "type": "web",
    "country": "US",  # Código alpha-2 ISO
    "allowed_websites": ["example.com"],  # Máx 5
    "safe_search": True
}
```

**Fonte de Notícias:**
```python
{
    "type": "news",
    "country": "US",
    "excluded_websites": ["tabloid.com"]  # Máx 5
}
```

## Modelos Disponíveis

| Modelo | Melhor Para | Preço |
|-------|----------|---------|
| `openai/gpt-5.2` | Segundas opiniões, code review, geral | $1.75/M entrada, $14/M saída |
| `openai/gpt-5-mini` | Raciocínio otimizado para custo | $0.30/M entrada, $1.20/M saída |
| `openai/o4-mini` | Raciocínio eficiente mais recente | $1.10/M entrada, $4.40/M saída |
| `openai/o3` | Raciocínio avançado, problemas complexos | $10/M entrada, $40/M saída |
| `xai/grok-3` | Dados em tempo real do X/Twitter | $3/M + $0.025/fonte |
| `deepseek/deepseek-chat` | Tarefas simples, processamento em massa | $0.14/M entrada, $0.28/M saída |
| `google/gemini-2.5-flash` | Documentos muito longos, rápido | $0.15/M entrada, $0.60/M saída |
| `openai/dall-e-3` | Imagens fotorrealistas | $0.04/imagem |
| `google/nano-banana` | Imagens rápidas, artísticas | $0.01/imagem |

*M = milhão de tokens. O custo real depende do comprimento do seu prompt e resposta.*

## Referência de Custo

Todos os custos de LLM são por milhão de tokens (M = 1.000.000 tokens).

| Modelo | Entrada | Saída |
|-------|-------|--------|
| GPT-5.2 | $1.75/M | $14.00/M |
| GPT-5-mini | $0.30/M | $1.20/M |
| Grok-3 (sem busca) | $3.00/M | $15.00/M |
| DeepSeek | $0.14/M | $0.28/M |

| Ações de Custo Fixo | |
|-------|--------|
| Grok Live Search | $0.025/fonte (padrão 10 = $0.25) |
| Imagem DALL-E | $0.04/imagem |
| Imagem Nano Banana | $0.01/imagem |

**Custos típicos:** Um prompt de 500 palavras (~750 tokens) para GPT-5.2 custa ~$0.001 entrada. Uma resposta de 1000 palavras (~1500 tokens) custa ~$0.02 saída.

## Setup e Financiamento

**Localização da carteira:** `$HOME/.blockrun/.session` (ex: `/Users/username/.blockrun/.session`)

**Setup pela primeira vez:**
1. Carteira se cria automaticamente quando `setup_agent_wallet()` é chamado
2. Verifique carteira e saldo:
```python
from blockrun_llm import setup_agent_wallet
client = setup_agent_wallet()
print(f"Carteira: {client.get_wallet_address()}")
print(f"Saldo: ${client.get_balance():.2f} USDC")
```
3. Financie a carteira com $1-5 USDC na rede Base

**Mostrar código QR para financiamento (ASCII para terminal):**
```python
from blockrun_llm import generate_wallet_qr_ascii, get_wallet_address
print(generate_wallet_qr_ascii(get_wallet_address()))
```

## Solução de Problemas

**"Grok diz que não tem acesso em tempo real"**
→ Você esqueceu de ativar Live Search. Adicione `search=True`:
```python
response = client.chat("xai/grok-3", "O que está em tendência?", search=True)
```

**Módulo não encontrado**
→ Instale o SDK: `pip install blockrun-llm`

## Atualizações

```bash
pip install --upgrade blockrun-llm
```