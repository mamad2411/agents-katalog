---
name: scvi-tools
description: Esta habilidade deve ser usada ao trabalhar com análise de dados de ômica de célula única usando scvi-tools, incluindo scRNA-seq, scATAC-seq, CITE-seq, transcriptômica espacial e outras modalidades de célula única. Use esta habilidade para modelagem probabilística, correção de batch, redução de dimensionalidade, expressão diferencial, anotação de tipo celular, integração multimodal e tarefas de análise espacial.
---

# scvi-tools

## Visão Geral

scvi-tools é um framework Python abrangente para modelos probabilísticos em genômica de célula única. Construído em PyTorch e PyTorch Lightning, fornece modelos generativos profundos usando inferência variacional para analisar diversas modalidades de dados de célula única.

## Quando Usar Esta Habilidade

Use esta habilidade quando:
- Analisar dados de single-cell RNA-seq (redução de dimensionalidade, correção de batch, integração)
- Trabalhar com dados de single-cell ATAC-seq ou acessibilidade de cromatina
- Integrar dados multimodais (CITE-seq, multiome, conjuntos de dados pareados/não pareados)
- Analisar dados de transcriptômica espacial (deconvolução, mapeamento espacial)
- Realizar análise de expressão diferencial em dados de célula única
- Conduzir tarefas de anotação de tipo celular ou transfer learning
- Trabalhar com modalidades especializadas de célula única (metilação, citometria, velocidade de RNA)
- Construir modelos probabilísticos customizados para análise de célula única

## Capacidades Principais

scvi-tools fornece modelos organizados por modalidade de dados:

### 1. Análise de Single-Cell RNA-seq
Modelos principais para análise de expressão, correção de batch e integração. Veja `references/models-scrna-seq.md` para:
- **scVI**: Redução de dimensionalidade não supervisionada e correção de batch
- **scANVI**: Anotação de tipo celular semi-supervisionada e integração
- **AUTOZI**: Detecção e modelagem de zero-inflação
- **VeloVI**: Análise de velocidade de RNA
- **contrastiveVI**: Isolamento de efeito de perturbação

### 2. Acessibilidade de Cromatina (ATAC-seq)
Modelos para análise de dados de cromatina de célula única. Veja `references/models-atac-seq.md` para:
- **PeakVI**: Análise e integração de ATAC-seq baseada em picos
- **PoissonVI**: Modelagem quantitativa de contagem de fragmentos
- **scBasset**: Abordagem de aprendizado profundo com análise de motivos

### 3. Integração Multimodal e Multi-ômica
Análise conjunta de múltiplos tipos de dados. Veja `references/models-multimodal.md` para:
- **totalVI**: Modelagem conjunta de proteína CITE-seq e RNA
- **MultiVI**: Integração multi-ômica pareada e não pareada
- **MrVI**: Análise multi-resolução entre amostras

### 4. Transcriptômica Espacial
Análise de transcriptômica com resolução espacial. Veja `references/models-spatial.md` para:
- **DestVI**: Deconvolução espacial multi-resolução
- **Stereoscope**: Deconvolução de tipo celular
- **Tangram**: Mapeamento espacial e integração
- **scVIVA**: Análise de relacionamento célula-ambiente

### 5. Modalidades Especializadas
Ferramentas de análise especializadas adicionais. Veja `references/models-specialized.md` para:
- **MethylVI/MethylANVI**: Análise de metilação de célula única
- **CytoVI**: Correção de batch de citometria de fluxo/massa
- **Solo**: Detecção de doublets
- **CellAssign**: Anotação de tipo celular baseada em marcadores

## Workflow Típico

Todos os modelos scvi-tools seguem um padrão de API consistente:

```python
# 1. Carregar e fazer pré-processamento de dados (formato AnnData)
import scvi
import scanpy as sc

adata = scvi.data.heart_cell_atlas_subsampled()
sc.pp.filter_genes(adata, min_counts=3)
sc.pp.highly_variable_genes(adata, n_top_genes=1200)

# 2. Registrar dados com modelo (especificar camadas, covariáveis)
scvi.model.SCVI.setup_anndata(
    adata,
    layer="counts",  # Use contagens brutas, não log-normalizadas
    batch_key="batch",
    categorical_covariate_keys=["donor"],
    continuous_covariate_keys=["percent_mito"]
)

# 3. Criar e treinar modelo
model = scvi.model.SCVI(adata)
model.train()

# 4. Extrair representações latentes e valores normalizados
latent = model.get_latent_representation()
normalized = model.get_normalized_expression(library_size=1e4)

# 5. Armazenar em AnnData para análise downstream
adata.obsm["X_scVI"] = latent
adata.layers["scvi_normalized"] = normalized

# 6. Análise downstream com scanpy
sc.pp.neighbors(adata, use_rep="X_scVI")
sc.tl.umap(adata)
sc.tl.leiden(adata)
```

**Princípios de Design Principais:**
- **Contagens brutas obrigatórias**: Modelos esperam dados de contagem não normalizados para desempenho ótimo
- **API unificada**: Interface consistente em todos os modelos (setup → train → extract)
- **Centrado em AnnData**: Integração perfeita com o ecossistema scanpy
- **Aceleração GPU**: Utilização automática de GPUs disponíveis
- **Correção de batch**: Lidar com variação técnica através do registro de covariáveis

## Tarefas de Análise Comuns

### Expressão Diferencial
Análise de DE probabilística usando os modelos generativos aprendidos:

```python
de_results = model.differential_expression(
    groupby="cell_type",
    group1="TypeA",
    group2="TypeB",
    mode="change",  # Usar teste de hipótese composto
    delta=0.25      # Limiar de tamanho de efeito mínimo
)
```

Veja `references/differential-expression.md` para metodologia detalhada e interpretação.

### Persistência de Modelo
Salvar e carregar modelos treinados:

```python
# Salvar modelo
model.save("./model_directory", overwrite=True)

# Carregar modelo
model = scvi.model.SCVI.load("./model_directory", adata=adata)
```

### Correção de Batch e Integração
Integrar conjuntos de dados entre batches ou estudos:

```python
# Registrar informações de batch
scvi.model.SCVI.setup_anndata(adata, batch_key="study")

# Modelo aprende automaticamente representações corrigidas por batch
model = scvi.model.SCVI(adata)
model.train()
latent = model.get_latent_representation()  # Corrigido por batch
```

## Fundamentos Teóricos

scvi-tools é construído em:
- **Inferência variacional**: Distribuições posteriores aproximadas para inferência Bayesiana escalável
- **Modelos generativos profundos**: Arquiteturas VAE que aprendem distribuições de dados complexas
- **Inferência amortizada**: Redes neurais compartilhadas para aprendizado eficiente entre células
- **Modelagem probabilística**: Quantificação de incerteza principiada e teste estatístico

Veja `references/theoretical-foundations.md` para contexto detalhado sobre o framework matemático.

## Recursos Adicionais

- **Workflows**: `references/workflows.md` contém workflows comuns, melhores práticas, ajuste de hiperparâmetros e otimização de GPU
- **Referências de Modelos**: Documentação detalhada para cada categoria de modelo no diretório `references/`
- **Documentação Oficial**: https://docs.scvi-tools.org/en/stable/
- **Tutoriais**: https://docs.scvi-tools.org/en/stable/tutorials/index.html
- **Referência de API**: https://docs.scvi-tools.org/en/stable/api/index.html

## Instalação

```bash
uv pip install scvi-tools
# Para suporte a GPU
uv pip install scvi-tools[cuda]
```

## Melhores Práticas

1. **Use contagens brutas**: Sempre forneça dados de contagem não normalizados aos modelos
2. **Filtre genes**: Remova genes com contagem baixa antes da análise (ex: `min_counts=3`)
3. **Registre covariáveis**: Inclua fatores técnicos conhecidos (batch, donor, etc.) em `setup_anndata`
4. **Seleção de features**: Use genes altamente variáveis para desempenho melhorado
5. **Salvamento de modelo**: Sempre salve modelos treinados para evitar retreinamento
6. **Uso de GPU**: Ative aceleração GPU para conjuntos de dados grandes (`accelerator="gpu"`)
7. **Integração Scanpy**: Armazene outputs em objetos AnnData para análise downstream