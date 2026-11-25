---
name: n8n-code-python
description: Escrever código Python em nós Code do n8n. Use quando estiver escrevendo Python no n8n, usando sintaxe _input/_json/_node, trabalhando com biblioteca padrão, ou precisar compreender limitações de Python em nós Code do n8n.
---

# Nó Code Python (Beta)

Orientação especializada para escrever código Python em nós Code do n8n.

---

## ⚠️ Importante: JavaScript Primeiro

**Recomendação**: Use **JavaScript para 95% dos casos**. Use Python apenas quando:
- Você precisa de funções específicas da biblioteca padrão do Python
- Você é significativamente mais confortável com sintaxe Python
- Você está fazendo transformações de dados melhor adequadas ao Python

**Por que JavaScript é preferido:**
- Funções auxiliares completas do n8n ($helpers.httpRequest, etc.)
- Biblioteca DateTime Luxon para operações avançadas de data/hora
- Sem limitações de bibliotecas externas
- Melhor documentação do n8n e suporte da comunidade

---

## Início Rápido

```python
# Template básico para nós Code Python
items = _input.all()

# Processar dados
processed = []
for item in items:
    processed.append({
        "json": {
            **item["json"],
            "processed": True,
            "timestamp": datetime.now().isoformat()
        }
    })

return processed
```

### Regras Essenciais

1. **Considere JavaScript primeiro** - Use Python apenas quando necessário
2. **Acessar dados**: `_input.all()`, `_input.first()`, ou `_input.item`
3. **CRÍTICO**: Deve retornar no formato `[{"json": {...}}]`
4. **CRÍTICO**: Dados de webhook estão sob `_json["body"]` (não `_json` diretamente)
5. **LIMITAÇÃO CRÍTICA**: **Sem bibliotecas externas** (sem requests, pandas, numpy)
6. **Apenas biblioteca padrão**: json, datetime, re, base64, hashlib, urllib.parse, math, random, statistics

---

## Guia de Seleção de Modo

Igual ao JavaScript - escolha baseado no seu caso de uso:

### Executar Uma Vez para Todos os Itens (Recomendado - Padrão)

**Use este modo para:** 95% dos casos

- **Como funciona**: Código executa **uma vez** independente da contagem de entrada
- **Acesso aos dados**: `_input.all()` ou array `_items` (modo Native)
- **Melhor para**: Agregação, filtragem, processamento em lote, transformações
- **Desempenho**: Mais rápido para múltiplos itens (execução única)

```python
# Exemplo: Calcular total de todos os itens
all_items = _input.all()
total = sum(item["json"].get("amount", 0) for item in all_items)

return [{
    "json": {
        "total": total,
        "count": len(all_items),
        "average": total / len(all_items) if all_items else 0
    }
}]
```

### Executar Uma Vez para Cada Item

**Use este modo para:** Apenas casos especializados

- **Como funciona**: Código executa **separadamente** para cada item de entrada
- **Acesso aos dados**: `_input.item` ou `_item` (modo Native)
- **Melhor para**: Lógica específica do item, operações independentes, validação por item
- **Desempenho**: Mais lento para grandes volumes (múltiplas execuções)

```python
# Exemplo: Adicionar timestamp de processamento a cada item
item = _input.item

return [{
    "json": {
        **item["json"],
        "processed": True,
        "processed_at": datetime.now().isoformat()
    }
}]
```

---

## Modos Python: Beta vs Native

O n8n oferece dois modos de execução Python:

### Python (Beta) - Recomendado
- **Use**: Sintaxe auxiliar `_input`, `_json`, `_node`
- **Melhor para**: Maioria dos casos de uso Python
- **Auxiliares disponíveis**: `_now`, `_today`, `_jmespath()`
- **Importar**: `from datetime import datetime`

```python
# Exemplo Python (Beta)
items = _input.all()
now = _now  # Objeto datetime incorporado

return [{
    "json": {
        "count": len(items),
        "timestamp": now.isoformat()
    }
}]
```

### Python (Native) (Beta)
- **Use**: Apenas variáveis `_items`, `_item`
- **Sem auxiliares**: Sem `_input`, `_now`, etc.
- **Mais limitado**: Apenas Python padrão
- **Use quando**: Precisa de Python puro sem auxiliares do n8n

```python
# Exemplo Python (Native)
processed = []

for item in _items:
    processed.append({
        "json": {
            "id": item["json"].get("id"),
            "processed": True
        }
    })

return processed
```

**Recomendação**: Use **Python (Beta)** para melhor integração com n8n.

---

## Padrões de Acesso aos Dados

### Padrão 1: _input.all() - Mais Comum

**Use quando**: Processando arrays, operações em lote, agregações

```python
# Obter todos os itens do nó anterior
all_items = _input.all()

# Filtrar, transformar conforme necessário
valid = [item for item in all_items if item["json"].get("status") == "active"]

processed = []
for item in valid:
    processed.append({
        "json": {
            "id": item["json"]["id"],
            "name": item["json"]["name"]
        }
    })

return processed
```

### Padrão 2: _input.first() - Muito Comum

**Use quando**: Trabalhando com objetos únicos, respostas de API

```python
# Obter apenas o primeiro item
first_item = _input.first()
data = first_item["json"]

return [{
    "json": {
        "result": process_data(data),
        "processed_at": datetime.now().isoformat()
    }
}]
```

### Padrão 3: _input.item - Apenas Modo Cada Item

**Use quando**: Em modo "Executar Uma Vez para Cada Item"

```python
# Item atual em loop (apenas modo Cada Item)
current_item = _input.item

return [{
    "json": {
        **current_item["json"],
        "item_processed": True
    }
}]
```

### Padrão 4: _node - Referenciar Outros Nós

**Use quando**: Precisa de dados de nós específicos no workflow

```python
# Obter saída de nó específico
webhook_data = _node["Webhook"]["json"]
http_data = _node["HTTP Request"]["json"]

return [{
    "json": {
        "combined": {
            "webhook": webhook_data,
            "api": http_data
        }
    }
}]
```

**Veja**: [DATA_ACCESS.md](DATA_ACCESS.md) para guia completo

---

## Crítico: Estrutura de Dados de Webhook

**ERRO MAIS COMUM**: Dados de webhook estão aninhados sob `["body"]`

```python
# ❌ ERRADO - Levantará KeyError
name = _json["name"]
email = _json["email"]

# ✅ CORRETO - Dados de webhook estão sob ["body"]
name = _json["body"]["name"]
email = _json["body"]["email"]

# ✅ MAIS SEGURO - Use .get() para acesso seguro
webhook_data = _json.get("body", {})
name = webhook_data.get("name")
```

**Por quê**: O nó Webhook envolve todos os dados de requisição sob propriedade `body`. Isso inclui dados POST, parâmetros de query, e payloads JSON.

**Veja**: [DATA_ACCESS.md](DATA_ACCESS.md) para detalhes completos da estrutura de webhook

---

## Requisitos de Formato de Retorno

**REGRA CRÍTICA**: Sempre retornar lista de dicionários com chave `"json"`

### Formatos de Retorno Corretos

```python
# ✅ Resultado único
return [{
    "json": {
        "field1": value1,
        "field2": value2
    }
}]

# ✅ Múltiplos resultados
return [
    {"json": {"id": 1, "data": "first"}},
    {"json": {"id": 2, "data": "second"}}
]

# ✅ List comprehension
transformed = [
    {"json": {"id": item["json"]["id"], "processed": True}}
    for item in _input.all()
    if item["json"].get("valid")
]
return transformed

# ✅ Resultado vazio (quando sem dados para retornar)
return []

# ✅ Retorno condicional
if should_process:
    return [{"json": processed_data}]
else:
    return []
```

### Formatos de Retorno Incorretos

```python
# ❌ ERRADO: Dicionário sem wrapper de lista
return {
    "json": {"field": value}
}

# ❌ ERRADO: Lista sem wrapper json
return [{"field": value}]

# ❌ ERRADO: String pura
return "processed"

# ❌ ERRADO: Estrutura incompleta
return [{"data": value}]  # Deveria ser {"json": value}
```

**Por que importa**: Nós seguintes esperam formato de lista. Formato incorreto causa falha na execução do workflow.

**Veja**: [ERROR_PATTERNS.md](ERROR_PATTERNS.md) #2 para soluções de erros detalhadas

---

## Limitação Crítica: Sem Bibliotecas Externas

**LIMITAÇÃO PYTHON MAIS IMPORTANTE**: Não é possível importar pacotes externos

### O Que NÃO Está Disponível

```python
# ❌ NÃO DISPONÍVEL - Levantará ModuleNotFoundError
import requests  # ❌ Não
import pandas  # ❌ Não
import numpy  # ❌ Não
import scipy  # ❌ Não
from bs4 import BeautifulSoup  # ❌ Não
import lxml  # ❌ Não
```

### O Que Está Disponível (Biblioteca Padrão)

```python
# ✅ DISPONÍVEL - Apenas biblioteca padrão
import json  # ✅ Análise JSON
import datetime  # ✅ Operações de data/hora
import re  # ✅ Expressões regulares
import base64  # ✅ Codificação Base64
import hashlib  # ✅ Funções hash
import urllib.parse  # ✅ Análise de URL
import math  # ✅ Funções matemáticas
import random  # ✅ Números aleatórios
import statistics  # ✅ Funções estatísticas
```

### Soluções Alternativas

**Precisa de requisições HTTP?**
- ✅ Use nó **HTTP Request** antes do nó Code
- ✅ Ou mude para **JavaScript** e use `$helpers.httpRequest()`

**Precisa de análise de dados (pandas/numpy)?**
- ✅ Use módulo **statistics** do Python para estatísticas básicas
- ✅ Ou mude para **JavaScript** para maioria das operações
- ✅ Cálculos manuais com listas e dicionários

**Precisa de web scraping (BeautifulSoup)?**
- ✅ Use nó **HTTP Request** + nó **HTML Extract**
- ✅ Ou mude para **JavaScript** com regex/métodos de string

**Veja**: [STANDARD_LIBRARY.md](STANDARD_LIBRARY.md) para referência completa

---

## Visão Geral de Padrões Comuns

Baseado em workflows de produção, aqui estão os padrões Python mais úteis:

### 1. Transformação de Dados
Transformar todos os itens com list comprehensions

```python
items = _input.all()

return [
    {
        "json": {
            "id": item["json"].get("id"),
            "name": item["json"].get("name", "Unknown").upper(),
            "processed": True
        }
    }
    for item in items
]
```

### 2. Filtragem e Agregação
Somar, filtrar, contar com funções incorporadas

```python
items = _input.all()
total = sum(item["json"].get("amount", 0) for item in items)
valid_items = [item for item in items if item["json"].get("amount", 0) > 0]

return [{
    "json": {
        "total": total,
        "count": len(valid_items)
    }
}]
```

### 3. Processamento de String com Regex
Extrair padrões de texto

```python
import re

items = _input.all()
email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

all_emails = []
for item in items:
    text = item["json"].get("text", "")
    emails = re.findall(email_pattern, text)
    all_emails.extend(emails)

# Remover duplicatas
unique_emails = list(set(all_emails))

return [{
    "json": {
        "emails": unique_emails,
        "count": len(unique_emails)
    }
}]
```

### 4. Validação de Dados
Validar e limpar dados

```python
items = _input.all()
validated = []

for item in items:
    data = item["json"]
    errors = []

    # Validar campos
    if not data.get("email"):
        errors.append("Email obrigatório")
    if not data.get("name"):
        errors.append("Nome obrigatório")

    validated.append({
        "json": {
            **data,
            "valid": len(errors) == 0,
            "errors": errors if errors else None
        }
    })

return validated
```

### 5. Análise Estatística
Calcular estatísticas com módulo statistics

```python
from statistics import mean, median, stdev

items = _input.all()
values = [item["json"].get("value", 0) for item in items if "value" in item["json"]]

if values:
    return [{
        "json": {
            "mean": mean(values),
            "median": median(values),
            "stdev": stdev(values) if len(values) > 1 else 0,
            "min": min(values),
            "max": max(values),
            "count": len(values)
        }
    }]
else:
    return [{"json": {"error": "Nenhum valor encontrado"}}]
```

**Veja**: [COMMON_PATTERNS.md](COMMON_PATTERNS.md) para 10 padrões Python detalhados

---

## Prevenção de Erros - Top 5 Erros

### #1: Importar Bibliotecas Externas (Python-Específico!)

```python
# ❌ ERRADO: Tentando importar biblioteca externa
import requests  # ModuleNotFoundError!

# ✅ CORRETO: Use nó HTTP Request ou JavaScript
# Adicione nó HTTP Request antes do nó Code
# OU mude para JavaScript e use $helpers.httpRequest()
```

### #2: Código Vazio ou Sem Retorno

```python
# ❌ ERRADO: Sem instrução return
items = _input.all()
# Processamento...
# Esqueceu de retornar!

# ✅ CORRETO: Sempre retornar dados
items = _input.all()
# Processamento...
return [{"json": item["json"]} for item in items]
```

### #3: Formato de Retorno Incorreto

```python
# ❌ ERRADO: Retornando dict em vez de lista
return {"json": {"result": "success"}}

# ✅ CORRETO: Wrapper de lista obrigatório
return [{"json": {"result": "success"}}]
```

### #4: KeyError no Acesso a Dicionário

```python
# ❌ ERRADO: Acesso direto falha se faltando
name = _json["user"]["name"]  # KeyError!

# ✅ CORRETO: Use .get() para acesso seguro
name = _json.get("user", {}).get("name", "Unknown")
```

### #5: Aninhamento de Body de Webhook

```python
# ❌ ERRADO: Acesso direto aos dados de webhook
email = _json["email"]  # KeyError!

# ✅ CORRETO: Dados de webhook sob ["body"]
email = _json["body"]["email"]

# ✅ MELHOR: Acesso seguro com .get()
email = _json.get("body", {}).get("email", "sem-email")
```

**Veja**: [ERROR_PATTERNS.md](ERROR_PATTERNS.md) para guia completo de erros

---

## Referência da Biblioteca Padrão

### Módulos Mais Úteis

```python
# Operações JSON
import json
data = json.loads(json_string)
json_output = json.dumps({"key": "value"})

# Data/hora
from datetime import datetime, timedelta
now = datetime.now()
tomorrow = now + timedelta(days=1)
formatted = now.strftime("%Y-%m-%d")

# Expressões regulares
import re
matches = re.findall(r'\d+', text)
cleaned = re.sub(r'[^\w\s]', '', text)

# Codificação Base64
import base64
encoded = base64.b64encode(data).decode()
decoded = base64.b64decode(encoded)

# Hashing
import hashlib
hash_value = hashlib.sha256(text.encode()).hexdigest()

# Análise de URL
import urllib.parse
params = urllib.parse.urlencode({"key": "value"})
parsed = urllib.parse.urlparse(url)

# Estatísticas
from statistics import mean, median, stdev
average = mean([1, 2, 3, 4, 5])
```

**Veja**: [STANDARD_LIBRARY.md](STANDARD_LIBRARY.md) para referência completa

---

## Melhores Práticas

### 1. Sempre Use .get() para Acesso a Dicionário

```python
# ✅ SEGURO: Não falha se campo faltando
value = item["json"].get("field", "default")

# ❌ ARRISCADO: Falha se campo não existe
value = item["json"]["field"]
```

### 2. Tratar Explicitamente Valores None/Null

```python
# ✅ BOM: Padrão 0 se None
amount = item["json"].get("amount") or 0

# ✅ BOM: Verificar None explicitamente
text = item["json"].get("text")
if text is None:
    text = ""
```

### 3. Use List Comprehensions para Filtragem

```python
# ✅ PYTHÔNICO: List comprehension
valid = [item for item in items if item["json"].get("active")]

# ❌ VERBOSO: Loop manual
valid = []
for item in items:
    if item["json"].get("active"):
        valid.append(item)
```

### 4. Retornar Estrutura Consistente

```python
# ✅ CONSISTENTE: Sempre lista com chave "json"
return [{"json": result}]  # Resultado único
return results  # Múltiplos resultados (já formatados)
return []  # Sem resultados
```

### 5. Debugar com Instruções print()

```python
# Instruções de debug aparecem no console do navegador (F12)
items = _input.all()
print(f"Processando {len(items)} itens")
print(f"Primeiro item: {items[0] if items else 'None'}")
```

---

## Quando Usar Python vs JavaScript

### Use Python Quando:
- ✅ Você precisa do módulo `statistics` para operações estatísticas
- ✅ Você é significativamente mais confortável com sintaxe Python
- ✅ Sua lógica mapeia bem para list comprehensions
- ✅ Você precisa de funções específicas da biblioteca padrão

### Use JavaScript Quando:
- ✅ Você precisa de requisições HTTP ($helpers.httpRequest())
- ✅ Você precisa de data/hora avançadas (DateTime/Luxon)
- ✅ Você quer melhor integração com n8n
- ✅ **Para 95% dos casos** (recomendado)

### Considere Outros Nós Quando:
- ❌ Mapeamento simples de campos → Use nó **Set**
- ❌ Filtragem básica → Use nó **Filter**
- ❌ Condicionais simples → Use nó **IF** ou **Switch**
- ❌ Apenas requisições HTTP → Use nó **HTTP Request**

---

## Integração com Outras Skills

### Funciona Com:

**Sintaxe de Expressão n8n**:
- Expressões usam sintaxe `{{ }}` em outros nós
- Nós Code usam Python diretamente (sem `{{ }}`)
- Quando usar expressões vs code

**Especialista n8n MCP Tools**:
- Como encontrar nó Code: `search_nodes({query: "code"})`
- Obter ajuda de configuração: `get_node_essentials("nodes-base.code")`
- Validar code: `validate_node_operation()`

**Configuração de Nó n8n**:
- Seleção de modo (Todos os Itens vs Cada Item)
- Seleção de linguagem (Python vs JavaScript)
- Compreender dependências de propriedade

**Padrões de Workflow n8n**:
- Nós Code em etapa de transformação
- Quando usar Python vs JavaScript em padrões

**Especialista em Validação n8n**:
- Validar configuração de nó Code
- Tratar erros de validação
- Auto-corrigir problemas comuns

**Código n8n JavaScript**:
- Quando usar JavaScript ao invés
- Comparação de recursos JavaScript vs Python
- Migração de Python para JavaScript

---

## Lista de Verificação de Referência Rápida

Antes de fazer deploy de nós Code Python, verifique:

- [ ] **Considerou JavaScript primeiro** - Usando Python apenas quando necessário
- [ ] **Código não está vazio** - Deve ter lógica significativa
- [ ] **Instrução return existe** - Deve retornar lista de dicionários
- [ ] **Formato de retorno correto** - Cada item: `{"json": {...}}`
- [ ] **Acesso aos dados correto** - Usando `_input.all()`, `_input.first()`, ou `_input.item`
- [ ] **Sem imports externos** - Apenas biblioteca padrão (json, datetime, re, etc.)
- [ ] **Acesso seguro a dicionário** - Usando `.get()` para evitar KeyError
- [ ] **Dados de webhook** - Acessar via `["body"]` se vindo de webhook
- [ ] **Seleção de modo** - "Todos os Itens" para maioria dos casos
- [ ] **Saída consistente** - Todos caminhos de código retornam mesma estrutura

---

## Recursos Adicionais

### Arquivos Relacionados
- [DATA_ACCESS.md](DATA_ACCESS.md) - Padrões abrangentes de acesso aos dados Python
- [COMMON_PATTERNS.md](COMMON_PATTERNS.md) - 10 padrões Python para n8n
- [ERROR_PATTERNS.md](ERROR_PATTERNS.md) - Top 5 erros e soluções
- [STANDARD_LIBRARY.md](STANDARD_LIBRARY.md) - Referência completa da biblioteca padrão

### Documentação n8n
- Guia do Nó Code: https://docs.n8n.io/code/code-node/
- Python no n8n: https://docs.n8n.io/code/builtin/python-modules/

---

**Pronto para escrever Python em nós Code do n8n - mas considere JavaScript primeiro!** Use Python para necessidades específicas, consulte o guia de padrões de erro para evitar erros comuns, e aproveite a biblioteca padrão efetivamente.