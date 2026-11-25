---
name: biorxiv-database
description: Ferramenta eficiente de busca em banco de dados para o servidor de pré-prints bioRxiv. Use essa competência ao pesquisar pré-prints de ciências da vida por palavras-chave, autores, intervalos de datas ou categorias, recuperando metadados de artigos, baixando PDFs ou conduzindo revisões de literatura.
---

# Banco de Dados bioRxiv

## Visão Geral

Essa competência fornece ferramentas baseadas em Python para busca e recuperação eficiente de pré-prints do banco de dados bioRxiv. Ela permite buscas abrangentes por palavras-chave, autores, intervalos de datas e categorias, retornando metadados estruturados em JSON que incluem títulos, resumos, DOIs e informações de citação. A competência também oferece suporte para downloads de PDF com análise de texto completo.

## Quando Usar Essa Competência

Use essa competência quando:
- Buscar pré-prints recentes em áreas de pesquisa específicas
- Rastrear publicações de autores particulares
- Conduzir revisões sistemáticas de literatura
- Analisar tendências de pesquisa ao longo do tempo
- Recuperar metadados para gerenciamento de citações
- Baixar PDFs de pré-prints para análise
- Filtrar artigos por categorias de assunto do bioRxiv

## Capacidades Principais de Busca

### 1. Busca por Palavras-Chave

Pesquise pré-prints contendo palavras-chave específicas em títulos, resumos ou listas de autores.

**Uso Básico:**
```python
python scripts/biorxiv_search.py \
  --keywords "CRISPR" "gene editing" \
  --start-date 2024-01-01 \
  --end-date 2024-12-31 \
  --output results.json
```

**Com Filtro de Categoria:**
```python
python scripts/biorxiv_search.py \
  --keywords "neural networks" "deep learning" \
  --days-back 180 \
  --category neuroscience \
  --output recent_neuroscience.json
```

**Campos de Busca:**
Por padrão, palavras-chave são pesquisadas em título e resumo. Customize com `--search-fields`:
```python
python scripts/biorxiv_search.py \
  --keywords "AlphaFold" \
  --search-fields title \
  --days-back 365
```

### 2. Busca por Autor

Encontre todos os artigos de um autor específico dentro de um intervalo de datas.

**Uso Básico:**
```python
python scripts/biorxiv_search.py \
  --author "Smith" \
  --start-date 2023-01-01 \
  --end-date 2024-12-31 \
  --output smith_papers.json
```

**Publicações Recentes:**
```python
# Último ano por padrão se nenhuma data for especificada
python scripts/biorxiv_search.py \
  --author "Johnson" \
  --output johnson_recent.json
```

### 3. Busca por Intervalo de Datas

Recupere todos os pré-prints postados em um intervalo de datas específico.

**Uso Básico:**
```python
python scripts/biorxiv_search.py \
  --start-date 2024-01-01 \
  --end-date 2024-01-31 \
  --output january_2024.json
```

**Com Filtro de Categoria:**
```python
python scripts/biorxiv_search.py \
  --start-date 2024-06-01 \
  --end-date 2024-06-30 \
  --category genomics \
  --output genomics_june.json
```

**Atalho Dias Atrás:**
```python
# Últimos 30 dias
python scripts/biorxiv_search.py \
  --days-back 30 \
  --output last_month.json
```

### 4. Detalhes do Artigo por DOI

Recupere metadados detalhados para um pré-print específico.

**Uso Básico:**
```python
python scripts/biorxiv_search.py \
  --doi "10.1101/2024.01.15.123456" \
  --output paper_details.json
```

**URLs de DOI Completas Aceitas:**
```python
python scripts/biorxiv_search.py \
  --doi "https://doi.org/10.1101/2024.01.15.123456"
```

### 5. Downloads de PDF

Baixe o PDF de texto completo de qualquer pré-print.

**Uso Básico:**
```python
python scripts/biorxiv_search.py \
  --doi "10.1101/2024.01.15.123456" \
  --download-pdf paper.pdf
```

**Processamento em Lote:**
Para vários PDFs, extraia DOIs de um JSON de resultado de busca e baixe cada artigo:
```python
import json
from biorxiv_search import BioRxivSearcher

# Carregue os resultados da busca
with open('results.json') as f:
    data = json.load(f)

searcher = BioRxivSearcher(verbose=True)

# Baixe cada artigo
for i, paper in enumerate(data['results'][:10]):  # Primeiros 10 artigos
    doi = paper['doi']
    searcher.download_pdf(doi, f"papers/paper_{i+1}.pdf")
```

## Categorias Válidas

Filtre buscas por categorias de assunto do bioRxiv:

- `animal-behavior-and-cognition`
- `biochemistry`
- `bioengineering`
- `bioinformatics`
- `biophysics`
- `cancer-biology`
- `cell-biology`
- `clinical-trials`
- `developmental-biology`
- `ecology`
- `epidemiology`
- `evolutionary-biology`
- `genetics`
- `genomics`
- `immunology`
- `microbiology`
- `molecular-biology`
- `neuroscience`
- `paleontology`
- `pathology`
- `pharmacology-and-toxicology`
- `physiology`
- `plant-biology`
- `scientific-communication-and-education`
- `synthetic-biology`
- `systems-biology`
- `zoology`

## Formato de Saída

Todas as buscas retornam JSON estruturado com o seguinte formato:

```json
{
  "query": {
    "keywords": ["CRISPR"],
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "category": "genomics"
  },
  "result_count": 42,
  "results": [
    {
      "doi": "10.1101/2024.01.15.123456",
      "title": "Título do Artigo Aqui",
      "authors": "Smith J, Doe J, Johnson A",
      "author_corresponding": "Smith J",
      "author_corresponding_institution": "Universidade Exemplo",
      "date": "2024-01-15",
      "version": "1",
      "type": "new results",
      "license": "cc_by",
      "category": "genomics",
      "abstract": "Texto do resumo completo...",
      "pdf_url": "https://www.biorxiv.org/content/10.1101/2024.01.15.123456v1.full.pdf",
      "html_url": "https://www.biorxiv.org/content/10.1101/2024.01.15.123456v1",
      "jatsxml": "https://www.biorxiv.org/content/...",
      "published": ""
    }
  ]
}
```

## Padrões Comuns de Uso

### Fluxo de Trabalho de Revisão de Literatura

1. **Busca ampla por palavras-chave:**
```python
python scripts/biorxiv_search.py \
  --keywords "organoids" "tissue engineering" \
  --start-date 2023-01-01 \
  --end-date 2024-12-31 \
  --category bioengineering \
  --output organoid_papers.json
```

2. **Extrair e revisar resultados:**
```python
import json

with open('organoid_papers.json') as f:
    data = json.load(f)

print(f"Encontrados {data['result_count']} artigos")

for paper in data['results'][:5]:
    print(f"\nTítulo: {paper['title']}")
    print(f"Autores: {paper['authors']}")
    print(f"Data: {paper['date']}")
    print(f"DOI: {paper['doi']}")
```

3. **Baixar artigos selecionados:**
```python
from biorxiv_search import BioRxivSearcher

searcher = BioRxivSearcher()
selected_dois = ["10.1101/2024.01.15.123456", "10.1101/2024.02.20.789012"]

for doi in selected_dois:
    filename = doi.replace("/", "_").replace(".", "_") + ".pdf"
    searcher.download_pdf(doi, f"papers/{filename}")
```

### Análise de Tendências

Rastreie tendências de pesquisa analisando frequências de publicação ao longo do tempo:

```python
python scripts/biorxiv_search.py \
  --keywords "machine learning" \
  --start-date 2020-01-01 \
  --end-date 2024-12-31 \
  --category bioinformatics \
  --output ml_trends.json
```

Em seguida, analise a distribuição temporal nos resultados.

### Rastreamento de Autores

Monitore pré-prints de pesquisadores específicos:

```python
# Rastreie múltiplos autores
authors = ["Smith", "Johnson", "Williams"]

for author in authors:
    python scripts/biorxiv_search.py \
      --author "{author}" \
      --days-back 365 \
      --output "{author}_papers.json"
```

## Uso da API Python

Para fluxos de trabalho mais complexos, importe e use a classe `BioRxivSearcher` diretamente:

```python
from scripts.biorxiv_search import BioRxivSearcher

# Inicialize
searcher = BioRxivSearcher(verbose=True)

# Múltiplas operações de busca
keywords_papers = searcher.search_by_keywords(
    keywords=["CRISPR", "gene editing"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    category="genomics"
)

author_papers = searcher.search_by_author(
    author_name="Smith",
    start_date="2023-01-01",
    end_date="2024-12-31"
)

# Obtenha detalhes de artigo específico
paper = searcher.get_paper_details("10.1101/2024.01.15.123456")

# Baixe PDF
success = searcher.download_pdf(
    doi="10.1101/2024.01.15.123456",
    output_path="paper.pdf"
)

# Formate resultados consistentemente
formatted = searcher.format_result(paper, include_abstract=True)
```

## Boas Práticas

1. **Use intervalos de datas apropriados**: Intervalos de datas menores retornam mais rapidamente. Para buscas por palavras-chave em longos períodos, considere dividir em múltiplas consultas.

2. **Filtre por categoria**: Quando possível, use `--category` para reduzir transferência de dados e melhorar precisão da busca.

3. **Respeite limites de taxa**: O script inclui atrasos automáticos (0,5s entre requisições). Para coleta de dados em larga escala, adicione atrasos adicionais.

4. **Armazene em cache resultados**: Salve resultados de busca em arquivos JSON para evitar chamadas repetidas à API.

5. **Rastreamento de versão**: Pré-prints podem ter múltiplas versões. O campo `version` indica qual versão é retornada. URLs de PDF incluem o número da versão.

6. **Trate erros elegantemente**: Verifique o `result_count` no JSON de saída. Resultados vazios podem indicar problemas com intervalo de datas ou conectividade da API.

7. **Modo verboso para depuração**: Use a flag `--verbose` para ver logging detalhado de requisições e respostas da API.

## Funcionalidades Avançadas

### Lógica Personalizada de Intervalo de Datas

```python
from datetime import datetime, timedelta

# Último trimestre
end_date = datetime.now()
start_date = end_date - timedelta(days=90)

python scripts/biorxiv_search.py \
  --start-date {start_date.strftime('%Y-%m-%d')} \
  --end-date {end_date.strftime('%Y-%m-%d')}
```

### Limitação de Resultados

Limite o número de resultados retornados:

```python
python scripts/biorxiv_search.py \
  --keywords "COVID-19" \
  --days-back 30 \
  --limit 50 \
  --output covid_top50.json
```

### Excluir Resumos para Maior Velocidade

Quando apenas metadados são necessários:

```python
# Nota: Inclusão de resumo é controlada na API Python
from scripts.biorxiv_search import BioRxivSearcher

searcher = BioRxivSearcher()
papers = searcher.search_by_keywords(keywords=["AI"], days_back=30)
formatted = [searcher.format_result(p, include_abstract=False) for p in papers]
```

## Integração Programática

Integre resultados de busca em pipelines de análise downstream:

```python
import json
import pandas as pd

# Carregue resultados
with open('results.json') as f:
    data = json.load(f)

# Converta para DataFrame para análise
df = pd.DataFrame(data['results'])

# Analise
print(f"Total de artigos: {len(df)}")
print(f"Intervalo de datas: {df['date'].min()} a {df['date'].max()}")
print(f"\nPrincipais autores por contagem de artigos:")
print(df['authors'].str.split(',').explode().str.strip().value_counts().head(10))

# Filtre e exporte
recent = df[df['date'] >= '2024-06-01']
recent.to_csv('recent_papers.csv', index=False)
```

## Testando a Competência

Para verificar se a competência do banco de dados bioRxiv está funcionando corretamente, execute a suíte de testes abrangente.

**Pré-requisitos:**
```bash
uv pip install requests
```

**Execute testes:**
```bash
python tests/test_biorxiv_search.py
```

A suíte de testes valida:
- **Inicialização**: Instanciação da classe BioRxivSearcher
- **Busca por Intervalo de Datas**: Recuperar artigos dentro de intervalos de datas específicos
- **Filtragem por Categoria**: Filtrar artigos por categorias do bioRxiv
- **Busca por Palavras-Chave**: Encontrar artigos contendo palavras-chave específicas
- **Busca por DOI**: Recuperar artigos específicos por DOI
- **Formatação de Resultados**: Formatação apropriada de metadados de artigos
- **Busca por Intervalo**: Buscar artigos recentes por intervalos de tempo

**Saída Esperada:**
```
🧬 Suíte de Testes de Busca do Banco de Dados bioRxiv
======================================================================

🧪 Teste 1: Inicialização
✅ BioRxivSearcher inicializado com sucesso

🧪 Teste 2: Busca por Intervalo de Datas
✅ Encontrados 150 artigos entre 2024-01-01 e 2024-01-07
   Primeiro artigo: Abordagem inovadora baseada em CRISPR para edição de genoma...

[... testes adicionais ...]

======================================================================
📊 Resumo de Testes
======================================================================
✅ APROVADO: Inicialização
✅ APROVADO: Busca por Intervalo de Datas
✅ APROVADO: Filtragem por Categoria
✅ APROVADO: Busca por Palavras-Chave
✅ APROVADO: Busca por DOI
✅ APROVADO: Formatação de Resultados
✅ APROVADO: Busca por Intervalo
======================================================================
Resultados: 7 de 7 testes aprovados (100%)
======================================================================

🎉 Todos os testes foram aprovados! A competência do banco de dados bioRxiv está funcionando corretamente.
```

**Nota:** Alguns testes podem mostrar avisos se nenhum artigo for encontrado em intervalos de datas ou categorias específicas. Isso é normal e não indica uma falha.

## Documentação de Referência

Para especificações completas da API, documentação de endpoints e schemas de resposta, consulte:
- `references/api_reference.md` - Documentação completa da API bioRxiv

O arquivo de referência inclui:
- Especificações completas de endpoint da API
- Detalhes de formato de resposta
- Padrões de tratamento de erros
- Diretrizes de limite de taxa
- Padrões avançados de busca