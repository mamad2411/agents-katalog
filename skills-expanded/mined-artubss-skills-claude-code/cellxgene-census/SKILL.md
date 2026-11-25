---
name: cellxgene-census
description: "Consulte o CZ CELLxGENE Census (61M+ células). Filtre por tipo de célula/tecido/doença, recupere dados de expressão, integre com scanpy/PyTorch, para análise de célula única em escala populacional."
---

# CZ CELLxGENE Census

## Visão Geral

O CZ CELLxGENE Census oferece acesso programático a uma coleção abrangente e versionada de dados de genômica de célula única padronizados do CZ CELLxGENE Discover. Este skill permite consultas eficientes e análise de milhões de células em milhares de conjuntos de dados.

O Census inclui:
- **61+ milhões de células** de humanos e camundongos
- **Metadados padronizados** (tipos de célula, tecidos, doenças, doadores)
- **Matrizes de expressão gênica bruta**
- **Embeddings pré-calculados** e estatísticas
- **Integração com PyTorch, scanpy e outras ferramentas de análise**

## Quando Usar Este Skill

Este skill deve ser usado quando:
- Consultando dados de expressão de célula única por tipo de célula, tecido ou doença
- Explorando conjuntos de dados e metadados de célula única disponíveis
- Treinando modelos de aprendizado de máquina com dados de célula única
- Realizando análises em larga escala entre conjuntos de dados
- Integrando dados do Census com scanpy ou outros frameworks de análise
- Calculando estatísticas em milhões de células
- Acessando embeddings pré-calculados ou predições de modelos

## Instalação e Configuração

Instale a API do Census:
```bash
uv pip install cellxgene-census
```

Para workflows de aprendizado de máquina, instale dependências adicionais:
```bash
uv pip install cellxgene-census[experimental]
```

## Padrões de Workflow Principal

### 1. Abrindo o Census

Sempre use o context manager para garantir limpeza apropriada de recursos:

```python
import cellxgene_census

# Abrir versão estável mais recente
with cellxgene_census.open_soma() as census:
    # Trabalhar com dados do census

# Abrir versão específica para reprodutibilidade
with cellxgene_census.open_soma(census_version="2023-07-25") as census:
    # Trabalhar com dados do census
```

**Pontos-chave:**
- Use context manager (declaração `with`) para limpeza automática
- Especifique `census_version` para análises reprodutíveis
- Por padrão, abre a release "stable" mais recente

### 2. Explorando Informações do Census

Antes de consultar dados de expressão, explore conjuntos de dados e metadados disponíveis.

**Acesse informações resumidas:**
```python
# Obter estatísticas resumidas
summary = census["census_info"]["summary"].read().concat().to_pandas()
print(f"Total de células: {summary['total_cell_count'][0]}")

# Obter todos os conjuntos de dados
datasets = census["census_info"]["datasets"].read().concat().to_pandas()

# Filtrar conjuntos de dados por critérios
covid_datasets = datasets[datasets["disease"].str.contains("COVID", na=False)]
```

**Consulte metadados de célula para entender dados disponíveis:**
```python
# Obter tipos de célula únicos em um tecido
cell_metadata = cellxgene_census.get_obs(
    census,
    "homo_sapiens",
    value_filter="tissue_general == 'brain' and is_primary_data == True",
    column_names=["cell_type"]
)
unique_cell_types = cell_metadata["cell_type"].unique()
print(f"Encontrados {len(unique_cell_types)} tipos de célula no cérebro")

# Contar células por tecido
tissue_counts = cell_metadata.groupby("tissue_general").size()
```

**Importante:** Sempre filtre por `is_primary_data == True` para evitar contar células duplicadas, a menos que esteja analisando duplicatas especificamente.

### 3. Consultando Dados de Expressão (Pequena a Média Escala)

Para consultas retornando < 100k células que cabem na memória, use `get_anndata()`:

```python
# Consulta básica com filtros de tipo de célula e tecido
adata = cellxgene_census.get_anndata(
    census=census,
    organism="Homo sapiens",  # ou "Mus musculus"
    obs_value_filter="cell_type == 'B cell' and tissue_general == 'lung' and is_primary_data == True",
    obs_column_names=["assay", "disease", "sex", "donor_id"],
)

# Consultar genes específicos com múltiplos filtros
adata = cellxgene_census.get_anndata(
    census=census,
    organism="Homo sapiens",
    var_value_filter="feature_name in ['CD4', 'CD8A', 'CD19', 'FOXP3']",
    obs_value_filter="cell_type == 'T cell' and disease == 'COVID-19' and is_primary_data == True",
    obs_column_names=["cell_type", "tissue_general", "donor_id"],
)
```

**Sintaxe de filtro:**
- Use `obs_value_filter` para filtragem de célula
- Use `var_value_filter` para filtragem de gene
- Combine condições com `and`, `or`
- Use `in` para múltiplos valores: `tissue in ['lung', 'liver']`
- Selecione apenas colunas necessárias com `obs_column_names`

**Obtendo metadados separadamente:**
```python
# Consultar metadados de célula
cell_metadata = cellxgene_census.get_obs(
    census, "homo_sapiens",
    value_filter="disease == 'COVID-19' and is_primary_data == True",
    column_names=["cell_type", "tissue_general", "donor_id"]
)

# Consultar metadados de gene
gene_metadata = cellxgene_census.get_var(
    census, "homo_sapiens",
    value_filter="feature_name in ['CD4', 'CD8A']",
    column_names=["feature_id", "feature_name", "feature_length"]
)
```

### 4. Consultas em Larga Escala (Processamento Fora de Núcleo)

Para consultas que excedem a RAM disponível, use `axis_query()` com processamento iterativo:

```python
import tiledbsoma as soma

# Criar consulta de eixo
query = census["census_data"]["homo_sapiens"].axis_query(
    measurement_name="RNA",
    obs_query=soma.AxisQuery(
        value_filter="tissue_general == 'brain' and is_primary_data == True"
    ),
    var_query=soma.AxisQuery(
        value_filter="feature_name in ['FOXP2', 'TBR1', 'SATB2']"
    )
)

# Iterar através da matriz de expressão em chunks
iterator = query.X("raw").tables()
for batch in iterator:
    # batch é uma pyarrow.Table com colunas:
    # - soma_data: valor de expressão
    # - soma_dim_0: coordenada de célula (obs)
    # - soma_dim_1: coordenada de gene (var)
    process_batch(batch)
```

**Calculando estatísticas incrementais:**
```python
# Exemplo: Calcular expressão média
n_observations = 0
sum_values = 0.0

iterator = query.X("raw").tables()
for batch in iterator:
    values = batch["soma_data"].to_numpy()
    n_observations += len(values)
    sum_values += values.sum()

mean_expression = sum_values / n_observations
```

### 5. Aprendizado de Máquina com PyTorch

Para treinamento de modelos, use a integração experimental com PyTorch:

```python
from cellxgene_census.experimental.ml import experiment_dataloader

with cellxgene_census.open_soma() as census:
    # Criar dataloader
    dataloader = experiment_dataloader(
        census["census_data"]["homo_sapiens"],
        measurement_name="RNA",
        X_name="raw",
        obs_value_filter="tissue_general == 'liver' and is_primary_data == True",
        obs_column_names=["cell_type"],
        batch_size=128,
        shuffle=True,
    )

    # Loop de treinamento
    for epoch in range(num_epochs):
        for batch in dataloader:
            X = batch["X"]  # Tensor de expressão gênica
            labels = batch["obs"]["cell_type"]  # Labels de tipo de célula

            # Forward pass
            outputs = model(X)
            loss = criterion(outputs, labels)

            # Backward pass
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
```

**Divisão treino/teste:**
```python
from cellxgene_census.experimental.ml import ExperimentDataset

# Criar dataset a partir do experimento
dataset = ExperimentDataset(
    experiment_axis_query,
    layer_name="raw",
    obs_column_names=["cell_type"],
    batch_size=128,
)

# Dividir em treino e teste
train_dataset, test_dataset = dataset.random_split(
    split=[0.8, 0.2],
    seed=42
)
```

### 6. Integração com Scanpy

Integre perfeitamente dados do Census com workflows scanpy:

```python
import scanpy as sc

# Carregar dados do Census
adata = cellxgene_census.get_anndata(
    census=census,
    organism="Homo sapiens",
    obs_value_filter="cell_type == 'neuron' and tissue_general == 'cortex' and is_primary_data == True",
)

# Workflow scanpy padrão
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=2000)

# Redução de dimensionalidade
sc.pp.pca(adata, n_comps=50)
sc.pp.neighbors(adata)
sc.tl.umap(adata)

# Visualização
sc.pl.umap(adata, color=["cell_type", "tissue", "disease"])
```

### 7. Integração Multi-Dataset

Consulte e integre múltiplos conjuntos de dados:

```python
# Estratégia 1: Consultar múltiplos tecidos separadamente
tissues = ["lung", "liver", "kidney"]
adatas = []

for tissue in tissues:
    adata = cellxgene_census.get_anndata(
        census=census,
        organism="Homo sapiens",
        obs_value_filter=f"tissue_general == '{tissue}' and is_primary_data == True",
    )
    adata.obs["tissue"] = tissue
    adatas.append(adata)

# Concatenar
combined = adatas[0].concatenate(adatas[1:])

# Estratégia 2: Consultar múltiplos conjuntos de dados diretamente
adata = cellxgene_census.get_anndata(
    census=census,
    organism="Homo sapiens",
    obs_value_filter="tissue_general in ['lung', 'liver', 'kidney'] and is_primary_data == True",
)
```

## Conceitos-Chave e Melhores Práticas

### Sempre Filtre Dados Primários
A menos que esteja analisando duplicatas, sempre inclua `is_primary_data == True` em consultas para evitar contar células múltiplas vezes:
```python
obs_value_filter="cell_type == 'B cell' and is_primary_data == True"
```

### Especifique Versão do Census para Reprodutibilidade
Sempre especifique a versão do Census em análises de produção:
```python
census = cellxgene_census.open_soma(census_version="2023-07-25")
```

### Estime Tamanho da Consulta Antes de Carregar
Para consultas grandes, primeiro verifique o número de células para evitar problemas de memória:
```python
# Obter contagem de células
metadata = cellxgene_census.get_obs(
    census, "homo_sapiens",
    value_filter="tissue_general == 'brain' and is_primary_data == True",
    column_names=["soma_joinid"]
)
n_cells = len(metadata)
print(f"Consulta retornará {n_cells:,} células")

# Se muito grande (>100k), use processamento fora de núcleo
```

### Use tissue_general para Agrupamentos Mais Amplos
O campo `tissue_general` fornece categorias mais amplas que `tissue`, úteis para análises entre tecidos:
```python
# Agrupamento mais amplo
obs_value_filter="tissue_general == 'immune system'"

# Tecido específico
obs_value_filter="tissue == 'peripheral blood mononuclear cell'"
```

### Selecione Apenas Colunas Necessárias
Minimize transferência de dados especificando apenas colunas de metadados necessárias:
```python
obs_column_names=["cell_type", "tissue_general", "disease"]  # Não todas as colunas
```

### Verifique Presença de Dataset para Consultas Gene-Específicas
Ao analisar genes específicos, verifique quais conjuntos de dados os mediram:
```python
presence = cellxgene_census.get_presence_matrix(
    census,
    "homo_sapiens",
    var_value_filter="feature_name in ['CD4', 'CD8A']"
)
```

### Workflow em Duas Etapas: Explorar Depois Consultar
Primeiro explore metadados para entender dados disponíveis, depois consulte expressão:
```python
# Etapa 1: Explorar o que está disponível
metadata = cellxgene_census.get_obs(
    census, "homo_sapiens",
    value_filter="disease == 'COVID-19' and is_primary_data == True",
    column_names=["cell_type", "tissue_general"]
)
print(metadata.value_counts())

# Etapa 2: Consultar com base em achados
adata = cellxgene_census.get_anndata(
    census=census,
    organism="Homo sapiens",
    obs_value_filter="disease == 'COVID-19' and cell_type == 'T cell' and is_primary_data == True",
)
```

## Campos de Metadados Disponíveis

### Metadados de Célula (obs)
Campos-chave para filtragem:
- `cell_type`, `cell_type_ontology_term_id`
- `tissue`, `tissue_general`, `tissue_ontology_term_id`
- `disease`, `disease_ontology_term_id`
- `assay`, `assay_ontology_term_id`
- `donor_id`, `sex`, `self_reported_ethnicity`
- `development_stage`, `development_stage_ontology_term_id`
- `dataset_id`
- `is_primary_data` (Booleano: True = célula única)

### Metadados de Gene (var)
- `feature_id` (ID de gene Ensembl, ex.: "ENSG00000161798")
- `feature_name` (Símbolo do gene, ex.: "FOXP2")
- `feature_length` (Comprimento do gene em pares de bases)

## Documentação de Referência

Este skill inclui documentação de referência detalhada:

### references/census_schema.md
Documentação abrangente de:
- Estrutura e organização dos dados do Census
- Todos os campos de metadados disponíveis
- Sintaxe e operadores de filtro de valor
- Tipos de objeto SOMA
- Critérios de inclusão de dados

**Quando ler:** Quando você precisa de informações detalhadas de schema, lista completa de campos de metadados ou sintaxe de filtro complexa.

### references/common_patterns.md
Exemplos e padrões para:
- Consultas exploratórias (apenas metadados)
- Consultas pequenas-a-médias (AnnData)
- Consultas grandes (processamento fora de núcleo)
- Integração com PyTorch
- Workflows de integração Scanpy
- Integração multi-dataset
- Melhores práticas e armadilhas comuns

**Quando ler:** Ao implementar padrões de consulta específicos, procurar exemplos de código ou troubleshooting de problemas comuns.

## Casos de Uso Comuns

### Caso de Uso 1: Explorar Tipos de Célula em um Tecido
```python
with cellxgene_census.open_soma() as census:
    cells = cellxgene_census.get_obs(
        census, "homo_sapiens",
        value_filter="tissue_general == 'lung' and is_primary_data == True",
        column_names=["cell_type"]
    )
    print(cells["cell_type"].value_counts())
```

### Caso de Uso 2: Consultar Expressão de Gene Marcador
```python
with cellxgene_census.open_soma() as census:
    adata = cellxgene_census.get_anndata(
        census=census,
        organism="Homo sapiens",
        var_value_filter="feature_name in ['CD4', 'CD8A', 'CD19']",
        obs_value_filter="cell_type in ['T cell', 'B cell'] and is_primary_data == True",
    )
```

### Caso de Uso 3: Treinar Classificador de Tipo de Célula
```python
from cellxgene_census.experimental.ml import experiment_dataloader

with cellxgene_census.open_soma() as census:
    dataloader = experiment_dataloader(
        census["census_data"]["homo_sapiens"],
        measurement_name="RNA",
        X_name="raw",
        obs_value_filter="is_primary_data == True",
        obs_column_names=["cell_type"],
        batch_size=128,
        shuffle=True,
    )

    # Treinar modelo
    for epoch in range(epochs):
        for batch in dataloader:
            # Lógica de treinamento
            pass
```

### Caso de Uso 4: Análise Entre Tecidos
```python
with cellxgene_census.open_soma() as census:
    adata = cellxgene_census.get_anndata(
        census=census,
        organism="Homo sapiens",
        obs_value_filter="cell_type == 'macrophage' and tissue_general in ['lung', 'liver', 'brain'] and is_primary_data == True",
    )

    # Analisar diferenças de macrófago entre tecidos
    sc.tl.rank_genes_groups(adata, groupby="tissue_general")
```

## Troubleshooting

### Consulta Retorna Muitas Células
- Adicione filtros mais específicos para reduzir escopo
- Use `tissue` em vez de `tissue_general` para granularidade mais fina
- Filtre por `dataset_id` específico se conhecido
- Mude para processamento fora de núcleo para consultas grandes

### Erros de Memória
- Reduza escopo de consulta com filtros mais restritivos
- Selecione menos genes com `var_value_filter`
- Use processamento fora de núcleo com `axis_query()`
- Processe dados em lotes

### Células Duplicadas nos Resultados
- Sempre inclua `is_primary_data == True` em filtros
- Verifique se está consultando intencionalmente entre múltiplos conjuntos de dados

### Gene Não Encontrado
- Verifique ortografia do nome do gene (sensível a maiúsculas)
- Tente ID Ensembl com `feature_id` em vez de `feature_name`
- Verifique matriz de presença de dataset para ver se gene foi medido
- Alguns genes podem ter sido filtrados durante a construção do Census

### Inconsistências de Versão
- Sempre especifique `census_version` explicitamente
- Use mesma versão em todas as análises
- Verifique notas de release para mudanças específicas de versão