---
name: openalex-database
description: Consulte e analise literatura acadêmica usando o banco de dados OpenAlex. Esta skill deve ser usada ao pesquisar artigos acadêmicos, analisar tendências de pesquisa, encontrar obras de autores ou instituições, rastrear citações, descobrir publicações de acesso aberto ou conduzir análise bibliométrica em 240M+ obras acadêmicas. Use para buscas de literatura, análise de produção de pesquisa, análise de citações e consultas em banco de dados acadêmico.
---

# Banco de Dados OpenAlex

## Visão Geral

OpenAlex é um catálogo abrangente com 240M+ obras acadêmicas, autores, instituições, tópicos, fontes, editoras e financiadores. Esta skill fornece ferramentas e workflows para consultar a API OpenAlex, pesquisar literatura, analisar produção de pesquisa, rastrear citações e conduzir estudos bibliométricos.

## Início Rápido

### Configuração Básica

Sempre inicialize o cliente com um endereço de e-mail para acessar o pool educado (aumento de taxa de limite 10x):

```python
from scripts.openalex_client import OpenAlexClient

client = OpenAlexClient(email="seu-email@example.edu")
```

### Requisitos de Instalação

Instale o pacote necessário usando uv:

```bash
uv pip install requests
```

Nenhuma chave de API necessária - OpenAlex é completamente aberto.

## Capacidades Principais

### 1. Pesquisar Artigos

**Use para**: Encontrar artigos por título, resumo ou tópico

```python
# Busca simples
results = client.search_works(
    search="machine learning",
    per_page=100
)

# Busca com filtros
results = client.search_works(
    search="CRISPR gene editing",
    filter_params={
        "publication_year": ">2020",
        "is_oa": "true"
    },
    sort="cited_by_count:desc"
)
```

### 2. Encontrar Obras de um Autor

**Use para**: Obter todas as publicações de um pesquisador específico

Use o padrão de dois passos (nome da entidade → ID → obras):

```python
from scripts.query_helpers import find_author_works

works = find_author_works(
    author_name="Jennifer Doudna",
    client=client,
    limit=100
)
```

**Abordagem manual de dois passos**:
```python
# Passo 1: Obter ID do autor
author_response = client._make_request(
    '/authors',
    params={'search': 'Jennifer Doudna', 'per-page': 1}
)
author_id = author_response['results'][0]['id'].split('/')[-1]

# Passo 2: Obter obras
works = client.search_works(
    filter_params={"authorships.author.id": author_id}
)
```

### 3. Encontrar Obras de uma Instituição

**Use para**: Analisar produção de pesquisa de universidades ou organizações

```python
from scripts.query_helpers import find_institution_works

works = find_institution_works(
    institution_name="Stanford University",
    client=client,
    limit=200
)
```

### 4. Artigos Altamente Citados

**Use para**: Encontrar artigos influentes em um campo

```python
from scripts.query_helpers import find_highly_cited_recent_papers

papers = find_highly_cited_recent_papers(
    topic="quantum computing",
    years=">2020",
    client=client,
    limit=100
)
```

### 5. Artigos de Acesso Aberto

**Use para**: Encontrar pesquisa disponível gratuitamente

```python
from scripts.query_helpers import get_open_access_papers

papers = get_open_access_papers(
    search_term="climate change",
    client=client,
    oa_status="any",  # ou "gold", "green", "hybrid", "bronze"
    limit=200
)
```

### 6. Análise de Tendências de Publicação

**Use para**: Rastrear produção de pesquisa ao longo do tempo

```python
from scripts.query_helpers import get_publication_trends

trends = get_publication_trends(
    search_term="artificial intelligence",
    filter_params={"is_oa": "true"},
    client=client
)

# Classificar e exibir
for trend in sorted(trends, key=lambda x: x['key'])[-10:]:
    print(f"{trend['key']}: {trend['count']} publications")
```

### 7. Análise de Produção de Pesquisa

**Use para**: Análise abrangente de pesquisa de autor ou instituição

```python
from scripts.query_helpers import analyze_research_output

analysis = analyze_research_output(
    entity_type='institution',  # ou 'author'
    entity_name='MIT',
    client=client,
    years='>2020'
)

print(f"Total de obras: {analysis['total_works']}")
print(f"Acesso aberto: {analysis['open_access_percentage']}%")
print(f"Tópicos principais: {analysis['top_topics'][:5]}")
```

### 8. Buscas em Lote

**Use para**: Obter informações de múltiplos DOIs, ORCIDs ou IDs de forma eficiente

```python
dois = [
    "https://doi.org/10.1038/s41586-021-03819-2",
    "https://doi.org/10.1126/science.abc1234",
    # ... até 50 DOIs
]

works = client.batch_lookup(
    entity_type='works',
    ids=dois,
    id_field='doi'
)
```

### 9. Amostragem Aleatória

**Use para**: Obter amostras representativas para análise

```python
# Amostra pequena
works = client.sample_works(
    sample_size=100,
    seed=42,  # Para reprodutibilidade
    filter_params={"publication_year": "2023"}
)

# Amostra grande (>10k) - trata automaticamente múltiplas requisições
works = client.sample_works(
    sample_size=25000,
    seed=42,
    filter_params={"is_oa": "true"}
)
```

### 10. Análise de Citações

**Use para**: Encontrar artigos que citam um trabalho específico

```python
# Obter a obra
work = client.get_entity('works', 'https://doi.org/10.1038/s41586-021-03819-2')

# Obter artigos que citam usando cited_by_api_url
import requests
citing_response = requests.get(
    work['cited_by_api_url'],
    params={'mailto': client.email, 'per-page': 200}
)
citing_works = citing_response.json()['results']
```

### 11. Análise de Tópicos e Disciplinas

**Use para**: Compreender áreas de foco de pesquisa

```python
# Obter tópicos principais para uma instituição
topics = client.group_by(
    entity_type='works',
    group_field='topics.id',
    filter_params={
        "authorships.institutions.id": "I136199984",  # MIT
        "publication_year": ">2020"
    }
)

for topic in topics[:10]:
    print(f"{topic['key_display_name']}: {topic['count']} works")
```

### 12. Extração de Dados em Larga Escala

**Use para**: Baixar grandes conjuntos de dados para análise

```python
# Paginar por todos os resultados
all_papers = client.paginate_all(
    endpoint='/works',
    params={
        'search': 'synthetic biology',
        'filter': 'publication_year:2020-2024'
    },
    max_results=10000
)

# Exportar para CSV
import csv
with open('papers.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Title', 'Year', 'Citations', 'DOI', 'OA Status'])

    for paper in all_papers:
        writer.writerow([
            paper.get('title', 'N/A'),
            paper.get('publication_year', 'N/A'),
            paper.get('cited_by_count', 0),
            paper.get('doi', 'N/A'),
            paper.get('open_access', {}).get('oa_status', 'closed')
        ])
```

## Melhores Práticas Críticas

### Sempre Use E-mail para o Pool Educado
Adicione e-mail para obter limite 10x (1 req/s → 10 req/s):
```python
client = OpenAlexClient(email="seu-email@example.edu")
```

### Use Padrão de Dois Passos para Buscas de Entidade
Nunca filtre por nomes de entidade diretamente - sempre obtenha o ID primeiro:
```python
# ✅ Correto
# 1. Pesquisar entidade → obter ID
# 2. Filtrar por ID

# ❌ Errado
# filter=author_name:Einstein  # Isso não funciona!
```

### Use Tamanho Máximo de Página
Sempre use `per-page=200` para recuperação de dados eficiente:
```python
results = client.search_works(search="topic", per_page=200)
```

### Agrupar Múltiplos IDs
Use `batch_lookup()` para múltiplos IDs em vez de requisições individuais:
```python
# ✅ Correto - 1 requisição para 50 DOIs
works = client.batch_lookup('works', doi_list, 'doi')

# ❌ Errado - 50 requisições separadas
for doi in doi_list:
    work = client.get_entity('works', doi)
```

### Use Parâmetro Sample para Dados Aleatórios
Use `sample_works()` com seed para amostragem aleatória reprodutível:
```python
# ✅ Correto
works = client.sample_works(sample_size=100, seed=42)

# ❌ Errado - números de página aleatória tendem a viesar resultados
# Usar números de página aleatória não fornece verdadeira amostra aleatória
```

### Selecione Apenas Campos Necessários
Reduza tamanho de resposta selecionando campos específicos:
```python
results = client.search_works(
    search="topic",
    select=['id', 'title', 'publication_year', 'cited_by_count']
)
```

## Padrões Comuns de Filtro

### Intervalos de Datas
```python
# Ano único
filter_params={"publication_year": "2023"}

# Após ano
filter_params={"publication_year": ">2020"}

# Intervalo
filter_params={"publication_year": "2020-2024"}
```

### Múltiplos Filtros (E)
```python
# Todas as condições devem corresponder
filter_params={
    "publication_year": ">2020",
    "is_oa": "true",
    "cited_by_count": ">100"
}
```

### Múltiplos Valores (OU)
```python
# Qualquer instituição corresponde
filter_params={
    "authorships.institutions.id": "I136199984|I27837315"  # MIT ou Harvard
}
```

### Colaboração (E dentro do atributo)
```python
# Artigos com autores de AMBAS as instituições
filter_params={
    "authorships.institutions.id": "I136199984+I27837315"  # MIT E Harvard
}
```

### Negação
```python
# Excluir tipo
filter_params={
    "type": "!paratext"
}
```

## Tipos de Entidade

OpenAlex fornece estes tipos de entidade:
- **works** - Documentos acadêmicos (artigos, livros, conjuntos de dados)
- **authors** - Pesquisadores com identidades desambiguadas
- **institutions** - Universidades e organizações de pesquisa
- **sources** - Periódicos, repositórios, conferências
- **topics** - Classificações de disciplina
- **publishers** - Organizações editoras
- **funders** - Agências de financiamento

Acesse qualquer tipo de entidade usando padrões consistentes:
```python
client.search_works(...)
client.get_entity('authors', author_id)
client.group_by('works', 'topics.id', filter_params={...})
```

## IDs Externos

Use identificadores externos diretamente:
```python
# DOI para obras
work = client.get_entity('works', 'https://doi.org/10.7717/peerj.4375')

# ORCID para autores
author = client.get_entity('authors', 'https://orcid.org/0000-0003-1613-5981')

# ROR para instituições
institution = client.get_entity('institutions', 'https://ror.org/02y3ad647')

# ISSN para fontes
source = client.get_entity('sources', 'issn:0028-0836')
```

## Documentação de Referência

### Referência de API Detalhada
Veja `references/api_guide.md` para:
- Sintaxe de filtro completa
- Todos os endpoints disponíveis
- Estruturas de resposta
- Tratamento de erros
- Otimização de desempenho
- Detalhes de limite de taxa

### Exemplos Comuns de Consulta
Veja `references/common_queries.md` para:
- Exemplos funcionais completos
- Casos de uso do mundo real
- Padrões de consulta complexa
- Workflows de exportação de dados
- Procedimentos de análise multi-etapa

## Scripts

### openalex_client.py
Cliente principal de API com:
- Limite de taxa automático
- Lógica de retry com backoff exponencial
- Suporte a paginação
- Operações em lote
- Tratamento de erros

Use para acesso direto à API com controle total.

### query_helpers.py
Funções auxiliares de alto nível para operações comuns:
- `find_author_works()` - Obter artigos por autor
- `find_institution_works()` - Obter artigos de instituição
- `find_highly_cited_recent_papers()` - Obter artigos influentes
- `get_open_access_papers()` - Encontrar publicações OA
- `get_publication_trends()` - Analisar tendências ao longo do tempo
- `analyze_research_output()` - Análise abrangente

Use para consultas comuns de pesquisa com interfaces simplificadas.

## Solução de Problemas

### Limite de Taxa
Se encontrar erros 403:
1. Certifique-se de que o e-mail foi adicionado às requisições
2. Verifique se não excede 10 req/s
3. Cliente implementa automaticamente backoff exponencial

### Resultados Vazios
Se as buscas não retornarem resultados:
1. Verifique sintaxe de filtro (veja `references/api_guide.md`)
2. Use padrão de dois passos para buscas de entidade (não filtre por nomes)
3. Verifique se os IDs de entidade estão em formato correto

### Erros de Timeout
Para consultas grandes:
1. Use paginação com `per-page=200`
2. Use `select=` para limitar campos retornados
3. Divida em consultas menores se necessário

## Limites de Taxa

- **Padrão**: 1 requisição/segundo, 100k requisições/dia
- **Pool educado (com e-mail)**: 10 requisições/segundo, 100k requisições/dia

Sempre use pool educado para workflows em produção fornecendo e-mail ao cliente.

## Observações

- Nenhuma autenticação necessária
- Todos os dados são abertos e gratuitos
- Limites de taxa se aplicam globalmente, não por IP
- Use LitLLM com OpenRouter se análise baseada em LLM for necessária (não use Perplexity API diretamente)
- Cliente trata automaticamente paginação, retries e limite de taxa