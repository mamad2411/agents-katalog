---
name: reactome-database
description: "Consultar REST API do Reactome para análise de vias, enriquecimento, mapeamento gene-via, vias de doença, interações moleculares, análise de expressão, para estudos de biologia de sistemas."
---

# Banco de Dados Reactome

## Visão Geral

Reactome é um banco de dados de vias livre, de código aberto e curado com mais de 2.825 vias humanas. Consulte vias biológicas, realize análise de sobre-representação e expressão, mapeie genes para vias, explore interações moleculares via REST API e cliente Python para pesquisa em biologia de sistemas.

## Quando Usar Esta Competência

Esta competência deve ser usada quando:
- Realizar análise de enriquecimento de vias em listas de genes ou proteínas
- Analisar dados de expressão gênica para identificar vias biológicas relevantes
- Consultar informações específicas de vias, reações ou interações moleculares
- Mapear genes ou proteínas para vias e processos biológicos
- Explorar vias relacionadas a doenças e mecanismos biológicos
- Visualizar resultados de análise no Reactome Pathway Browser
- Conduzir análise comparativa de vias entre espécies

## Capacidades Principais

Reactome fornece dois serviços de API principais e uma biblioteca cliente Python:

### 1. Content Service - Recuperação de Dados

Consulte e recupere dados de vias biológicas, interações moleculares e informações de entidades.

**Operações comuns:**
- Recuperar informações e hierarquias de vias
- Consultar entidades específicas (proteínas, reações, complexos)
- Obter moléculas participantes em vias
- Acessar versão do banco de dados e metadados
- Explorar compartimentos de vias e localizações

**URL Base da API:** `https://reactome.org/ContentService`

### 2. Analysis Service - Análise de Vias

Execute análise computacional em listas de genes e dados de expressão.

**Tipos de análise:**
- **Análise de Sobre-representação**: Identifique vias estatisticamente significativas de listas de genes/proteínas
- **Análise de Dados de Expressão**: Analise datasets de expressão gênica para encontrar vias relevantes
- **Comparação entre Espécies**: Compare dados de vias entre organismos diferentes

**URL Base da API:** `https://reactome.org/AnalysisService`

### 3. Pacote Python reactome2py

Biblioteca cliente Python que encapsula chamadas da API Reactome para acesso programático mais fácil.

**Instalação:**
```bash
uv pip install reactome2py
```

**Nota:** O pacote reactome2py (versão 3.0.0, lançado em janeiro de 2021) é funcional mas não está em manutenção ativa. Para a funcionalidade mais atualizada, considere usar chamadas diretas da REST API.

## Consultando Dados de Vias

### Usando Content Service REST API

O Content Service usa protocolo REST e retorna dados em formatos JSON ou texto simples.

**Obter versão do banco de dados:**
```python
import requests

response = requests.get("https://reactome.org/ContentService/data/database/version")
version = response.text
print(f"Versão do Reactome: {version}")
```

**Consultar uma entidade específica:**
```python
import requests

entity_id = "R-HSA-69278"  # ID de via de exemplo
response = requests.get(f"https://reactome.org/ContentService/data/query/{entity_id}")
data = response.json()
```

**Obter moléculas participantes em uma via:**
```python
import requests

event_id = "R-HSA-69278"
response = requests.get(
    f"https://reactome.org/ContentService/data/event/{event_id}/participatingPhysicalEntities"
)
molecules = response.json()
```

### Usando Pacote reactome2py

```python
import reactome2py
from reactome2py import content

# Consultar informações de via
pathway_info = content.query_by_id("R-HSA-69278")

# Obter versão do banco de dados
version = content.get_database_version()
```

**Para endpoints de API detalhados e parâmetros**, consulte `references/api_reference.md` nesta competência.

## Realizando Análise de Vias

### Análise de Sobre-representação

Envie uma lista de identificadores de gene/proteína para encontrar vias enriquecidas.

**Usando REST API:**
```python
import requests

# Preparar lista de identificadores
identifiers = ["TP53", "BRCA1", "EGFR", "MYC"]
data = "\n".join(identifiers)

# Enviar análise
response = requests.post(
    "https://reactome.org/AnalysisService/identifiers/",
    headers={"Content-Type": "text/plain"},
    data=data
)

result = response.json()
token = result["summary"]["token"]  # Salvar token para recuperar resultados depois

# Acessar vias
for pathway in result["pathways"]:
    print(f"{pathway['stId']}: {pathway['name']} (p-value: {pathway['entities']['pValue']})")
```

**Recuperar análise por token:**
```python
# Token é válido por 7 dias
response = requests.get(f"https://reactome.org/AnalysisService/token/{token}")
results = response.json()
```

### Análise de Dados de Expressão

Analise datasets de expressão gênica com valores quantitativos.

**Formato de entrada (TSV com cabeçalho começando com #):**
```
#Gene	Sample1	Sample2	Sample3
TP53	2.5	3.1	2.8
BRCA1	1.2	1.5	1.3
EGFR	4.5	4.2	4.8
```

**Enviar dados de expressão:**
```python
import requests

# Ler arquivo TSV
with open("expression_data.tsv", "r") as f:
    data = f.read()

response = requests.post(
    "https://reactome.org/AnalysisService/identifiers/",
    headers={"Content-Type": "text/plain"},
    data=data
)

result = response.json()
```

### Projeção entre Espécies

Mapeie identificadores para vias humanas exclusivamente usando o endpoint `/projection/`:

```python
response = requests.post(
    "https://reactome.org/AnalysisService/identifiers/projection/",
    headers={"Content-Type": "text/plain"},
    data=data
)
```

## Visualizando Resultados

Resultados de análise podem ser visualizados no Reactome Pathway Browser construindo URLs com o token de análise:

```python
token = result["summary"]["token"]
pathway_id = "R-HSA-69278"
url = f"https://reactome.org/PathwayBrowser/#{pathway_id}&DTAB=AN&ANALYSIS={token}"
print(f"Ver resultados: {url}")
```

## Trabalhando com Tokens de Análise

- Tokens de análise são válidos por **7 dias**
- Tokens permitem recuperação de resultados previamente calculados sem reenviamento
- Armazene tokens para acessar resultados entre sessões
- Use endpoint `GET /token/{TOKEN}` para recuperar resultados

## Formatos de Dados e Identificadores

### Tipos de Identificador Suportados

Reactome aceita vários formatos de identificador:
- Acessões UniProt (ex: P04637)
- Símbolos de gene (ex: TP53)
- IDs Ensembl (ex: ENSG00000141510)
- IDs EntrezGene (ex: 7157)
- IDs ChEBI para moléculas pequenas

O sistema detecta automaticamente os tipos de identificador.

### Requisitos de Formato de Entrada

**Para análise de sobre-representação:**
- Lista de texto simples de identificadores (um por linha)
- OU coluna única em formato TSV

**Para análise de expressão:**
- Formato TSV com linha de cabeçalho obrigatória começando com "#"
- Coluna 1: identificadores
- Colunas 2+: valores numéricos de expressão
- Use ponto (.) como separador decimal

### Formato de Saída

Todas as respostas da API retornam JSON contendo:
- `pathways`: Array de vias enriquecidas com métricas estatísticas
- `summary`: Metadados de análise e token
- `entities`: Identificadores correspondidos e não mapeados
- Valores estatísticos: pValue, FDR (taxa de falsa descoberta)

## Scripts Auxiliares

Esta competência inclui `scripts/reactome_query.py`, um script auxiliar para operações comuns do Reactome:

```bash
# Consultar informações de via
python scripts/reactome_query.py query R-HSA-69278

# Realizar análise de sobre-representação
python scripts/reactome_query.py analyze gene_list.txt

# Obter versão do banco de dados
python scripts/reactome_query.py version
```

## Recursos Adicionais

- **Documentação da API**: https://reactome.org/dev
- **Guia do Usuário**: https://reactome.org/userguide
- **Portal de Documentação**: https://reactome.org/documentation
- **Downloads de Dados**: https://reactome.org/download-data
- **Documentação reactome2py**: https://reactome.github.io/reactome2py/

Para documentação abrangente de endpoints da API, consulte `references/api_reference.md` nesta competência.

## Estatísticas Atuais do Banco de Dados (Versão 94, Setembro de 2025)

- 2.825 vias humanas
- 16.002 reações
- 11.630 proteínas
- 2.176 moléculas pequenas
- 1.070 fármacos
- 41.373 referências bibliográficas