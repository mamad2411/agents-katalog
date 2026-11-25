---
name: pydeseq2
description: "Análise de expressão gênica diferencial (Python DESeq2). Identifique genes DE a partir de contagens de RNA-seq em massa, testes de Wald, correção de FDR, gráficos volcano/MA, para análise de RNA-seq."
---

# PyDESeq2

## Visão Geral

PyDESeq2 é uma implementação em Python do DESeq2 para análise de expressão diferencial com dados de RNA-seq em massa. Projete e execute fluxos de trabalho completos do carregamento de dados até a interpretação de resultados, incluindo designs de fator único e multifatorial, testes de Wald com correção de testes múltiplos, encolhimento apeGLM opcional e integração com pandas e AnnData.

## Quando Usar Esta Skill

Esta skill deve ser usada quando:
- Analisar dados de contagem de RNA-seq em massa para expressão diferencial
- Comparar expressão gênica entre condições experimentais (ex: tratado vs controle)
- Executar designs multifatoriais considerando efeitos de batch ou covariáveis
- Converter fluxos de trabalho DESeq2 baseados em R para Python
- Integrar análise de expressão diferencial em pipelines baseados em Python
- Usuários mencionam "DESeq2", "expressão diferencial", "análise de RNA-seq" ou "PyDESeq2"

## Fluxo de Trabalho Rápido

Para usuários que desejam executar uma análise padrão de expressão diferencial:

```python
import pandas as pd
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats

# 1. Carregar dados
counts_df = pd.read_csv("counts.csv", index_col=0).T  # Transpor para amostras × genes
metadata = pd.read_csv("metadata.csv", index_col=0)

# 2. Filtrar genes com contagem baixa
genes_to_keep = counts_df.columns[counts_df.sum(axis=0) >= 10]
counts_df = counts_df[genes_to_keep]

# 3. Inicializar e ajustar DESeq2
dds = DeseqDataSet(
    counts=counts_df,
    metadata=metadata,
    design="~condition",
    refit_cooks=True
)
dds.deseq2()

# 4. Executar testes estatísticos
ds = DeseqStats(dds, contrast=["condition", "treated", "control"])
ds.summary()

# 5. Acessar resultados
results = ds.results_df
significant = results[results.padj < 0.05]
print(f"Found {len(significant)} significant genes")
```

## Etapas Principais do Fluxo de Trabalho

### Etapa 1: Preparação de Dados

**Requisitos de entrada:**
- **Matriz de contagem:** DataFrame de amostras × genes com contagens de leitura inteiras não-negativas
- **Metadados:** DataFrame de amostras × variáveis com fatores experimentais

**Padrões comuns de carregamento de dados:**

```python
# De CSV (formato típico: genes × amostras, precisa de transposição)
counts_df = pd.read_csv("counts.csv", index_col=0).T
metadata = pd.read_csv("metadata.csv", index_col=0)

# De TSV
counts_df = pd.read_csv("counts.tsv", sep="\t", index_col=0).T

# De AnnData
import anndata as ad
adata = ad.read_h5ad("data.h5ad")
counts_df = pd.DataFrame(adata.X, index=adata.obs_names, columns=adata.var_names)
metadata = adata.obs
```

**Filtragem de dados:**

```python
# Remover genes com contagem baixa
genes_to_keep = counts_df.columns[counts_df.sum(axis=0) >= 10]
counts_df = counts_df[genes_to_keep]

# Remover amostras com metadados faltantes
samples_to_keep = ~metadata.condition.isna()
counts_df = counts_df.loc[samples_to_keep]
metadata = metadata.loc[samples_to_keep]
```

### Etapa 2: Especificação de Design

A fórmula de design especifica como a expressão gênica é modelada.

**Designs de fator único:**
```python
design = "~condition"  # Comparação simples de dois grupos
```

**Designs multifatoriais:**
```python
design = "~batch + condition"  # Controlar efeitos de batch
design = "~age + condition"     # Incluir covariável contínua
design = "~group + condition + group:condition"  # Efeitos de interação
```

**Diretrizes de fórmula de design:**
- Use notação de fórmula Wilkinson (estilo R)
- Coloque variáveis de ajuste (ex: batch) antes da variável de interesse principal
- Garanta que variáveis existem como colunas no DataFrame de metadados
- Use tipos de dados apropriados (categórico para variáveis discretas)

### Etapa 3: Ajuste de DESeq2

Inicialize DeseqDataSet e execute o pipeline completo:

```python
from pydeseq2.dds import DeseqDataSet

dds = DeseqDataSet(
    counts=counts_df,
    metadata=metadata,
    design="~condition",
    refit_cooks=True,  # Reajustar após remover outliers
    n_cpus=1           # Processamento paralelo (ajuste conforme necessário)
)

# Executar o pipeline DESeq2 completo
dds.deseq2()
```

**O que `deseq2()` faz:**
1. Calcula fatores de tamanho (normalização)
2. Ajusta dispersões por gene
3. Ajusta curva de tendência de dispersão
4. Calcula priores de dispersão
5. Ajusta dispersões MAP (encolhimento)
6. Ajusta mudanças de dobra logarítmica
7. Calcula distâncias de Cook (detecção de outliers)
8. Reajusta se outliers detectados (opcional)

### Etapa 4: Testes Estatísticos

Execute testes de Wald para identificar genes diferentemente expressos:

```python
from pydeseq2.ds import DeseqStats

ds = DeseqStats(
    dds,
    contrast=["condition", "treated", "control"],  # Teste tratado vs controle
    alpha=0.05,                # Limiar de significância
    cooks_filter=True,         # Filtrar outliers
    independent_filter=True    # Filtrar testes com baixo poder
)

ds.summary()
```

**Especificação de contraste:**
- Formato: `[variable, test_level, reference_level]`
- Exemplo: `["condition", "treated", "control"]` testa tratado vs controle
- Se `None`, usa o último coeficiente no design

**Colunas do DataFrame de resultados:**
- `baseMean`: Contagem normalizada média em amostras
- `log2FoldChange`: Mudança de dobra log2 entre condições
- `lfcSE`: Erro padrão de LFC
- `stat`: Estatística do teste de Wald
- `pvalue`: Valor p bruto
- `padj`: Valor p ajustado (corrigido por FDR via Benjamini-Hochberg)

### Etapa 5: Encolhimento Opcional de LFC

Aplique encolhimento para reduzir ruído nas estimativas de mudança de dobra:

```python
ds.lfc_shrink()  # Aplica encolhimento apeGLM
```

**Quando usar encolhimento de LFC:**
- Para visualização (gráficos volcano, mapas de calor)
- Para classificar genes por tamanho de efeito
- Ao priorizar genes para experimentos de acompanhamento

**Importante:** Encolhimento afeta apenas os valores log2FoldChange, não os resultados do teste estatístico (valores p permanecem inalterados). Use valores encolhidos para visualização, mas reporte valores p não-encolhidos para significância.

### Etapa 6: Exportação de Resultados

Salve resultados e objetos intermediários:

```python
import pickle

# Exportar resultados como CSV
ds.results_df.to_csv("deseq2_results.csv")

# Salvar apenas genes significativos
significant = ds.results_df[ds.results_df.padj < 0.05]
significant.to_csv("significant_genes.csv")

# Salvar DeseqDataSet para uso posterior
with open("dds_result.pkl", "wb") as f:
    pickle.dump(dds.to_picklable_anndata(), f)
```

## Padrões de Análise Comuns

### Comparação de Dois Grupos

Comparação padrão caso-controle:

```python
dds = DeseqDataSet(counts=counts_df, metadata=metadata, design="~condition")
dds.deseq2()

ds = DeseqStats(dds, contrast=["condition", "treated", "control"])
ds.summary()

results = ds.results_df
significant = results[results.padj < 0.05]
```

### Comparações Múltiplas

Testando múltiplos grupos de tratamento contra controle:

```python
dds = DeseqDataSet(counts=counts_df, metadata=metadata, design="~condition")
dds.deseq2()

treatments = ["treatment_A", "treatment_B", "treatment_C"]
all_results = {}

for treatment in treatments:
    ds = DeseqStats(dds, contrast=["condition", treatment, "control"])
    ds.summary()
    all_results[treatment] = ds.results_df

    sig_count = len(ds.results_df[ds.results_df.padj < 0.05])
    print(f"{treatment}: {sig_count} significant genes")
```

### Considerando Efeitos de Batch

Controlar variação técnica:

```python
# Incluir batch no design
dds = DeseqDataSet(counts=counts_df, metadata=metadata, design="~batch + condition")
dds.deseq2()

# Testar condição controlando batch
ds = DeseqStats(dds, contrast=["condition", "treated", "control"])
ds.summary()
```

### Covariáveis Contínuas

Incluir variáveis contínuas como idade ou dosagem:

```python
# Garantir que variável contínua é numérica
metadata["age"] = pd.to_numeric(metadata["age"])

dds = DeseqDataSet(counts=counts_df, metadata=metadata, design="~age + condition")
dds.deseq2()

ds = DeseqStats(dds, contrast=["condition", "treated", "control"])
ds.summary()
```

## Usando o Script de Análise

Esta skill inclui um script completo de linha de comando para análises padrão:

```bash
# Uso básico
python scripts/run_deseq2_analysis.py \
  --counts counts.csv \
  --metadata metadata.csv \
  --design "~condition" \
  --contrast condition treated control \
  --output results/

# Com opções adicionais
python scripts/run_deseq2_analysis.py \
  --counts counts.csv \
  --metadata metadata.csv \
  --design "~batch + condition" \
  --contrast condition treated control \
  --output results/ \
  --min-counts 10 \
  --alpha 0.05 \
  --n-cpus 4 \
  --plots
```

**Características do script:**
- Carregamento de dados automático e validação
- Filtragem de genes e amostras
- Execução completa do pipeline DESeq2
- Testes estatísticos com parâmetros personalizáveis
- Exportação de resultados (CSV, pickle)
- Visualização opcional (gráficos volcano e MA)

Direcione usuários para `scripts/run_deseq2_analysis.py` quando precisarem de ferramenta independente ou desejarem processar múltiplos conjuntos de dados em lote.

## Interpretação de Resultados

### Identificando Genes Significativos

```python
# Filtrar por valor p ajustado
significant = ds.results_df[ds.results_df.padj < 0.05]

# Filtrar por significância e tamanho de efeito
sig_and_large = ds.results_df[
    (ds.results_df.padj < 0.05) &
    (abs(ds.results_df.log2FoldChange) > 1)
]

# Separar genes super e subexpressos
upregulated = significant[significant.log2FoldChange > 0]
downregulated = significant[significant.log2FoldChange < 0]

print(f"Upregulated: {len(upregulated)}")
print(f"Downregulated: {len(downregulated)}")
```

### Classificação e Ordenação

```python
# Ordenar por valor p ajustado
top_by_padj = ds.results_df.sort_values("padj").head(20)

# Ordenar por valor absoluto de mudança de dobra (usar valores encolhidos)
ds.lfc_shrink()
ds.results_df["abs_lfc"] = abs(ds.results_df.log2FoldChange)
top_by_lfc = ds.results_df.sort_values("abs_lfc", ascending=False).head(20)

# Ordenar por métrica combinada
ds.results_df["score"] = -np.log10(ds.results_df.padj) * abs(ds.results_df.log2FoldChange)
top_combined = ds.results_df.sort_values("score", ascending=False).head(20)
```

### Métricas de Qualidade

```python
# Verificar normalização (fatores de tamanho devem estar próximos a 1)
print("Size factors:", dds.obsm["size_factors"])

# Examinar estimativas de dispersão
import matplotlib.pyplot as plt
plt.hist(dds.varm["dispersions"], bins=50)
plt.xlabel("Dispersion")
plt.ylabel("Frequency")
plt.title("Dispersion Distribution")
plt.show()

# Verificar distribuição de valor p (deve ser principalmente plana com pico próximo a 0)
plt.hist(ds.results_df.pvalue.dropna(), bins=50)
plt.xlabel("P-value")
plt.ylabel("Frequency")
plt.title("P-value Distribution")
plt.show()
```

## Diretrizes de Visualização

### Gráfico Volcano

Visualize significância vs tamanho de efeito:

```python
import matplotlib.pyplot as plt
import numpy as np

results = ds.results_df.copy()
results["-log10(padj)"] = -np.log10(results.padj)

plt.figure(figsize=(10, 6))
significant = results.padj < 0.05

plt.scatter(
    results.loc[~significant, "log2FoldChange"],
    results.loc[~significant, "-log10(padj)"],
    alpha=0.3, s=10, c='gray', label='Not significant'
)
plt.scatter(
    results.loc[significant, "log2FoldChange"],
    results.loc[significant, "-log10(padj)"],
    alpha=0.6, s=10, c='red', label='padj < 0.05'
)

plt.axhline(-np.log10(0.05), color='blue', linestyle='--', alpha=0.5)
plt.xlabel("Log2 Fold Change")
plt.ylabel("-Log10(Adjusted P-value)")
plt.title("Volcano Plot")
plt.legend()
plt.savefig("volcano_plot.png", dpi=300)
```

### Gráfico MA

Mostre mudança de dobra vs expressão média:

```python
plt.figure(figsize=(10, 6))

plt.scatter(
    np.log10(results.loc[~significant, "baseMean"] + 1),
    results.loc[~significant, "log2FoldChange"],
    alpha=0.3, s=10, c='gray'
)
plt.scatter(
    np.log10(results.loc[significant, "baseMean"] + 1),
    results.loc[significant, "log2FoldChange"],
    alpha=0.6, s=10, c='red'
)

plt.axhline(0, color='blue', linestyle='--', alpha=0.5)
plt.xlabel("Log10(Base Mean + 1)")
plt.ylabel("Log2 Fold Change")
plt.title("MA Plot")
plt.savefig("ma_plot.png", dpi=300)
```

## Solução de Problemas Comuns

### Problemas de Formato de Dados

**Problema:** "Index mismatch between counts and metadata"

**Solução:** Garanta que nomes de amostra correspondem exatamente
```python
print("Counts samples:", counts_df.index.tolist())
print("Metadata samples:", metadata.index.tolist())

# Tomar intersecção se necessário
common = counts_df.index.intersection(metadata.index)
counts_df = counts_df.loc[common]
metadata = metadata.loc[common]
```

**Problema:** "All genes have zero counts"

**Solução:** Verificar se dados precisam ser transpostos
```python
print(f"Counts shape: {counts_df.shape}")
# Se genes > amostras, transposição é necessária
if counts_df.shape[1] < counts_df.shape[0]:
    counts_df = counts_df.T
```

### Problemas de Matriz de Design

**Problema:** "Design matrix is not full rank"

**Causa:** Variáveis confundidas (ex: todas as amostras tratadas em um batch)

**Solução:** Remover variável confundida ou adicionar termo de interação
```python
# Verificar confundimento
print(pd.crosstab(metadata.condition, metadata.batch))

# Simplificar design ou adicionar interação
design = "~condition"  # Remover batch
# OU
design = "~condition + batch + condition:batch"  # Modelar interação
```

### Sem Genes Significativos

**Diagnósticos:**
```python
# Verificar distribuição de dispersão
plt.hist(dds.varm["dispersions"], bins=50)
plt.show()

# Verificar fatores de tamanho
print(dds.obsm["size_factors"])

# Observar genes principais por valor p bruto
print(ds.results_df.nsmallest(20, "pvalue"))
```

**Possíveis causas:**
- Tamanhos de efeito pequenos
- Variabilidade biológica alta
- Tamanho de amostra insuficiente
- Problemas técnicos (efeitos de batch, outliers)

## Documentação de Referência

Para detalhes abrangentes além deste guia orientado por fluxo de trabalho:

- **Referência de API** (`references/api_reference.md`): Documentação completa de classes, métodos e estruturas de dados de PyDESeq2. Use quando precisar de informações detalhadas de parâmetros ou entender atributos de objeto.

- **Guia de Fluxo de Trabalho** (`references/workflow_guide.md`): Guia aprofundado cobrindo fluxos de trabalho de análise completos, padrões de carregamento de dados, designs multifatoriais, solução de problemas e melhores práticas. Use ao lidar com designs experimentais complexos ou encontrar problemas.

Carregue essas referências no contexto quando usuários precisarem de:
- Documentação detalhada de API: `Read references/api_reference.md`
- Exemplos de fluxo de trabalho abrangentes: `Read references/workflow_guide.md`
- Orientação de solução de problemas: `Read references/workflow_guide.md` (veja seção Troubleshooting)

## Lembretes Importantes

1. **Orientação de dados é importante:** Matrizes de contagem geralmente carregam como genes × amostras, mas precisam ser amostras × genes. Sempre transponha com `.T` se necessário.

2. **Filtragem de amostra:** Remova amostras com metadados faltantes antes da análise para evitar erros.

3. **Filtragem de gene:** Filtre genes com contagem baixa (ex: < 10 leituras totais) para melhorar poder e reduzir tempo computacional.

4. **Ordem de fórmula de design:** Coloque variáveis de ajuste antes da variável de interesse (ex: `"~batch + condition"` não `"~condition + batch"`).

5. **Timing de encolhimento de LFC:** Aplique encolhimento após testes estatísticos e apenas para propósitos de visualização/classificação. Valores p permanecem baseados em estimativas não-encolhidas.

6. **Interpretação de resultado:** Use `padj < 0.05` para significância, não valores p brutos. O procedimento Benjamini-Hochberg controla taxa de descoberta falsa.

7. **Especificação de contraste:** O formato é `[variable, test_level, reference_level]` onde test_level é comparado contra reference_level.

8. **Salvar objetos intermediários:** Use pickle para salvar objetos DeseqDataSet para uso posterior ou análises adicionais sem re-executar a etapa de ajuste cara.

## Instalação e Requisitos

```bash
uv pip install pydeseq2
```

**Requisitos do sistema:**
- Python 3.10-3.11
- pandas 1.4.3+
- numpy 1.23.0+
- scipy 1.11.0+
- scikit-learn 1.1.1+
- anndata 0.8.0+

**Opcional para visualização:**
- matplotlib
- seaborn

## Recursos Adicionais

- **Documentação Oficial:** https://pydeseq2.readthedocs.io
- **Repositório GitHub:** https://github.com/owkin/PyDESeq2
- **Publicação:** Muzellec et al. (2023) Bioinformatics, DOI: 10.1093/bioinformatics/btad547
- **DESeq2 Original (R):** Love et al. (2014) Genome Biology, DOI: 10.1186/s13059-014-0550-8