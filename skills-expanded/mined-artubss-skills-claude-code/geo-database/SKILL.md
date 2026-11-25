---
name: geo-database
description: "Acesse NCBI GEO para dados de expressão gênica e genômica. Pesquise/baixe datasets de microarray e RNA-seq (GSE, GSM, GPL), recupere arquivos SOFT/Matrix, para análise de transcriptômica e expressão."
---

# Banco de Dados GEO

## Visão Geral

O Gene Expression Omnibus (GEO) é o repositório público do NCBI para dados de expressão gênica de alta largura de banda e genômica funcional. O GEO contém mais de 264.000 estudos com mais de 8 milhões de amostras de experimentos baseados em array e sequenciamento.

## Quando Usar Esta Skill

Esta skill deve ser usada ao pesquisar datasets de expressão gênica, recuperar dados experimentais, baixar arquivos brutos e processados, consultar perfis de expressão ou integrar dados de GEO em fluxos de trabalho de análise computacional.

## Capacidades Principais

### 1. Entendendo a Organização de Dados do GEO

O GEO organiza dados hierarquicamente usando diferentes tipos de acesso:

**Series (GSE):** Um experimento completo com um conjunto de amostras relacionadas
- Exemplo: GSE123456
- Contém desenho experimental, amostras e informações gerais do estudo
- Maior unidade organizacional do GEO
- Contagem atual: 264.928+ series

**Sample (GSM):** Uma única amostra experimental ou réplica biológica
- Exemplo: GSM987654
- Contém dados de amostra individual, protocolos e metadados
- Vinculado a plataformas e series
- Contagem atual: 8.068.632+ amostras

**Platform (GPL):** A plataforma de microarray ou sequenciamento usada
- Exemplo: GPL570 (Affymetrix Human Genome U133 Plus 2.0 Array)
- Descreve a tecnologia e anotações de probe/feature
- Compartilhada entre múltiplos experimentos
- Contagem atual: 27.739+ plataformas

**DataSet (GDS):** Coleções curadas com formatação consistente
- Exemplo: GDS5678
- Amostras experimentalmente comparáveis organizadas por desenho de estudo
- Processadas para análise diferencial
- Subconjunto de dados do GEO (4.348 datasets curados)
- Ideal para análises comparativas rápidas

**Profiles:** Dados de expressão específicos de genes vinculados a features de sequência
- Pesquisáveis por nome de gene ou anotação
- Referências cruzadas para Entrez Gene
- Ativa pesquisas centradas em genes em todos os estudos

### 2. Pesquisando Dados do GEO

**Pesquisa de GEO DataSets:**

Pesquise estudos por palavras-chave, organismo ou condições experimentais:

```python
from Bio import Entrez

# Configure Entrez (obrigatório)
Entrez.email = "seu.email@exemplo.com"

# Pesquise datasets
def search_geo_datasets(query, retmax=20):
    """Pesquisa banco de dados GEO DataSets"""
    handle = Entrez.esearch(
        db="gds",
        term=query,
        retmax=retmax,
        usehistory="y"
    )
    results = Entrez.read(handle)
    handle.close()
    return results

# Exemplos de pesquisa
results = search_geo_datasets("breast cancer[MeSH] AND Homo sapiens[Organism]")
print(f"Encontrados {results['Count']} datasets")

# Pesquisa por plataforma específica
results = search_geo_datasets("GPL570[Accession]")

# Pesquisa por tipo de estudo
results = search_geo_datasets("expression profiling by array[DataSet Type]")
```

**Pesquisa de GEO Profiles:**

Encontre padrões de expressão específicos de genes:

```python
# Pesquise perfis de expressão gênica
def search_geo_profiles(gene_name, organism="Homo sapiens", retmax=100):
    """Pesquisa GEO Profiles para um gene específico"""
    query = f"{gene_name}[Gene Name] AND {organism}[Organism]"
    handle = Entrez.esearch(
        db="geoprofiles",
        term=query,
        retmax=retmax
    )
    results = Entrez.read(handle)
    handle.close()
    return results

# Encontre expressão de TP53 em estudos
tp53_results = search_geo_profiles("TP53", organism="Homo sapiens")
print(f"Encontrados {tp53_results['Count']} perfis de expressão para TP53")
```

**Padrões de Pesquisa Avançada:**

```python
# Combine múltiplos termos de pesquisa
def advanced_geo_search(terms, operator="AND"):
    """Construa queries de pesquisa complexas"""
    query = f" {operator} ".join(terms)
    return search_geo_datasets(query)

# Encontre estudos recentes de alta largura de banda
search_terms = [
    "RNA-seq[DataSet Type]",
    "Homo sapiens[Organism]",
    "2024[Publication Date]"
]
results = advanced_geo_search(search_terms)

# Pesquise por autor e condição
search_terms = [
    "Smith[Author]",
    "diabetes[Disease]"
]
results = advanced_geo_search(search_terms)
```

### 3. Recuperando Dados do GEO com GEOparse (Recomendado)

**GEOparse** é a biblioteca Python primária para acessar dados do GEO:

**Instalação:**
```bash
uv pip install GEOparse
```

**Uso Básico:**

```python
import GEOparse

# Baixe e analise uma Series do GEO
gse = GEOparse.get_GEO(geo="GSE123456", destdir="./data")

# Acesse metadados da series
print(gse.metadata['title'])
print(gse.metadata['summary'])
print(gse.metadata['overall_design'])

# Acesse informações de amostra
for gsm_name, gsm in gse.gsms.items():
    print(f"Amostra: {gsm_name}")
    print(f"  Título: {gsm.metadata['title'][0]}")
    print(f"  Fonte: {gsm.metadata['source_name_ch1'][0]}")
    print(f"  Características: {gsm.metadata.get('characteristics_ch1', [])}")

# Acesse informações de plataforma
for gpl_name, gpl in gse.gpls.items():
    print(f"Plataforma: {gpl_name}")
    print(f"  Título: {gpl.metadata['title'][0]}")
    print(f"  Organismo: {gpl.metadata['organism'][0]}")
```

**Trabalhando com Dados de Expressão:**

```python
import GEOparse
import pandas as pd

# Obtenha dados de expressão da series
gse = GEOparse.get_GEO(geo="GSE123456", destdir="./data")

# Extraia matriz de expressão
# Método 1: Do arquivo series matrix (mais rápido)
if hasattr(gse, 'pivot_samples'):
    expression_df = gse.pivot_samples('VALUE')
    print(expression_df.shape)  # genes x amostras

# Método 2: De amostras individuais
expression_data = {}
for gsm_name, gsm in gse.gsms.items():
    if hasattr(gsm, 'table'):
        expression_data[gsm_name] = gsm.table['VALUE']

expression_df = pd.DataFrame(expression_data)
print(f"Matriz de expressão: {expression_df.shape}")
```

**Acessando Arquivos Suplementares:**

```python
import GEOparse

gse = GEOparse.get_GEO(geo="GSE123456", destdir="./data")

# Baixe arquivos suplementares
gse.download_supplementary_files(
    directory="./data/GSE123456_suppl",
    download_sra=False  # Defina como True para baixar arquivos SRA
)

# Liste arquivos suplementares disponíveis
for gsm_name, gsm in gse.gsms.items():
    if hasattr(gsm, 'supplementary_files'):
        print(f"Amostra {gsm_name}:")
        for file_url in gsm.metadata.get('supplementary_file', []):
            print(f"  {file_url}")
```

**Filtrando e Subconjuntos de Dados:**

```python
import GEOparse

gse = GEOparse.get_GEO(geo="GSE123456", destdir="./data")

# Filtre amostras por metadados
control_samples = [
    gsm_name for gsm_name, gsm in gse.gsms.items()
    if 'control' in gsm.metadata.get('title', [''])[0].lower()
]

treatment_samples = [
    gsm_name for gsm_name, gsm in gse.gsms.items()
    if 'treatment' in gsm.metadata.get('title', [''])[0].lower()
]

print(f"Amostras controle: {len(control_samples)}")
print(f"Amostras de tratamento: {len(treatment_samples)}")

# Extraia matriz de expressão de subconjunto
expression_df = gse.pivot_samples('VALUE')
control_expr = expression_df[control_samples]
treatment_expr = expression_df[treatment_samples]
```

### 4. Usando E-utilities do NCBI para Acesso ao GEO

**E-utilities** fornecem acesso programático de nível inferior aos metadados do GEO:

**Fluxo de Trabalho Básico com E-utilities:**

```python
from Bio import Entrez
import time

Entrez.email = "seu.email@exemplo.com"

# Etapa 1: Pesquise entradas do GEO
def search_geo(query, db="gds", retmax=100):
    """Pesquise GEO usando E-utilities"""
    handle = Entrez.esearch(
        db=db,
        term=query,
        retmax=retmax,
        usehistory="y"
    )
    results = Entrez.read(handle)
    handle.close()
    return results

# Etapa 2: Busque sumários
def fetch_geo_summaries(id_list, db="gds"):
    """Busque sumários de documentos para entradas do GEO"""
    ids = ",".join(id_list)
    handle = Entrez.esummary(db=db, id=ids)
    summaries = Entrez.read(handle)
    handle.close()
    return summaries

# Etapa 3: Busque registros completos
def fetch_geo_records(id_list, db="gds"):
    """Busque registros GEO completos"""
    ids = ",".join(id_list)
    handle = Entrez.efetch(db=db, id=ids, retmode="xml")
    records = Entrez.read(handle)
    handle.close()
    return records

# Exemplo de fluxo de trabalho
search_results = search_geo("breast cancer AND Homo sapiens")
id_list = search_results['IdList'][:5]

summaries = fetch_geo_summaries(id_list)
for summary in summaries:
    print(f"GDS: {summary.get('Accession', 'N/A')}")
    print(f"Título: {summary.get('title', 'N/A')}")
    print(f"Amostras: {summary.get('n_samples', 'N/A')}")
    print()
```

**Processamento em Lote com E-utilities:**

```python
from Bio import Entrez
import time

Entrez.email = "seu.email@exemplo.com"

def batch_fetch_geo_metadata(accessions, batch_size=100):
    """Busque metadados para múltiplos acessos do GEO"""
    results = {}

    for i in range(0, len(accessions), batch_size):
        batch = accessions[i:i + batch_size]

        # Pesquise cada acesso
        for accession in batch:
            try:
                query = f"{accession}[Accession]"
                search_handle = Entrez.esearch(db="gds", term=query)
                search_results = Entrez.read(search_handle)
                search_handle.close()

                if search_results['IdList']:
                    # Busque sumário
                    summary_handle = Entrez.esummary(
                        db="gds",
                        id=search_results['IdList'][0]
                    )
                    summary = Entrez.read(summary_handle)
                    summary_handle.close()
                    results[accession] = summary[0]

                # Seja educado com os servidores do NCBI
                time.sleep(0.34)  # Máximo 3 requisições por segundo

            except Exception as e:
                print(f"Erro ao buscar {accession}: {e}")

    return results

# Busque metadados para múltiplos datasets
gse_list = ["GSE100001", "GSE100002", "GSE100003"]
metadata = batch_fetch_geo_metadata(gse_list)
```

### 5. Acesso Direto via FTP para Arquivos de Dados

**URLs de FTP para Dados do GEO:**

Dados do GEO podem ser baixados diretamente via FTP:

```python
import ftplib
import os

def download_geo_ftp(accession, file_type="matrix", dest_dir="./data"):
    """Baixe arquivos do GEO via FTP"""
    # Construa caminho de FTP baseado no tipo de acesso
    if accession.startswith("GSE"):
        # Arquivos de series
        gse_num = accession[3:]
        base_num = gse_num[:-3] + "nnn"
        ftp_path = f"/geo/series/GSE{base_num}/{accession}/"

        if file_type == "matrix":
            filename = f"{accession}_series_matrix.txt.gz"
        elif file_type == "soft":
            filename = f"{accession}_family.soft.gz"
        elif file_type == "miniml":
            filename = f"{accession}_family.xml.tgz"

    # Conecte ao servidor FTP
    ftp = ftplib.FTP("ftp.ncbi.nlm.nih.gov")
    ftp.login()
    ftp.cwd(ftp_path)

    # Baixe arquivo
    os.makedirs(dest_dir, exist_ok=True)
    local_file = os.path.join(dest_dir, filename)

    with open(local_file, 'wb') as f:
        ftp.retrbinary(f'RETR {filename}', f.write)

    ftp.quit()
    print(f"Baixado: {local_file}")
    return local_file

# Baixe arquivo series matrix
download_geo_ftp("GSE123456", file_type="matrix")

# Baixe arquivo formato SOFT
download_geo_ftp("GSE123456", file_type="soft")
```

**Usando wget ou curl para Downloads:**

```bash
# Baixe arquivo series matrix
wget ftp://ftp.ncbi.nlm.nih.gov/geo/series/GSE123nnn/GSE123456/matrix/GSE123456_series_matrix.txt.gz

# Baixe todos os arquivos suplementares para uma series
wget -r -np -nd ftp://ftp.ncbi.nlm.nih.gov/geo/series/GSE123nnn/GSE123456/suppl/

# Baixe arquivo família em formato SOFT
wget ftp://ftp.ncbi.nlm.nih.gov/geo/series/GSE123nnn/GSE123456/soft/GSE123456_family.soft.gz
```

### 6. Analisando Dados do GEO

**Controle de Qualidade e Pré-processamento:**

```python
import GEOparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Carregue dataset
gse = GEOparse.get_GEO(geo="GSE123456", destdir="./data")
expression_df = gse.pivot_samples('VALUE')

# Verifique valores ausentes
print(f"Valores ausentes: {expression_df.isnull().sum().sum()}")

# Transformação logarítmica (se necessário)
if expression_df.min().min() > 0:  # Verifique se já está log-transformado
    if expression_df.max().max() > 100:
        expression_df = np.log2(expression_df + 1)
        print("Aplicada transformação log2")

# Gráficos de distribuição
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
expression_df.plot.box(ax=plt.gca())
plt.title("Distribuição de Expressão por Amostra")
plt.xticks(rotation=90)

plt.subplot(1, 2, 2)
expression_df.mean(axis=1).hist(bins=50)
plt.title("Distribuição de Expressão de Gene")
plt.xlabel("Expressão Média")

plt.tight_layout()
plt.savefig("geo_qc.png", dpi=300, bbox_inches='tight')
```

**Análise de Expressão Diferencial:**

```python
import GEOparse
import pandas as pd
import numpy as np
from scipy import stats

gse = GEOparse.get_GEO(geo="GSE123456", destdir="./data")
expression_df = gse.pivot_samples('VALUE')

# Defina grupos de amostras
control_samples = ["GSM1", "GSM2", "GSM3"]
treatment_samples = ["GSM4", "GSM5", "GSM6"]

# Calcule fold changes e p-values
results = []
for gene in expression_df.index:
    control_expr = expression_df.loc[gene, control_samples]
    treatment_expr = expression_df.loc[gene, treatment_samples]

    # Calcule estatísticas
    fold_change = treatment_expr.mean() - control_expr.mean()
    t_stat, p_value = stats.ttest_ind(treatment_expr, control_expr)

    results.append({
        'gene': gene,
        'log2_fold_change': fold_change,
        'p_value': p_value,
        'control_mean': control_expr.mean(),
        'treatment_mean': treatment_expr.mean()
    })

# Crie DataFrame de resultados
de_results = pd.DataFrame(results)

# Correção de testes múltiplos (Benjamini-Hochberg)
from statsmodels.stats.multitest import multipletests
_, de_results['q_value'], _, _ = multipletests(
    de_results['p_value'],
    method='fdr_bh'
)

# Filtre genes significativos
significant_genes = de_results[
    (de_results['q_value'] < 0.05) &
    (abs(de_results['log2_fold_change']) > 1)
]

print(f"Genes significativos: {len(significant_genes)}")
significant_genes.to_csv("de_results.csv", index=False)
```

**Análise de Correlação e Clustering:**

```python
import GEOparse
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy
from scipy.spatial.distance import pdist

gse = GEOparse.get_GEO(geo="GSE123456", destdir="./data")
expression_df = gse.pivot_samples('VALUE')

# Heatmap de correlação de amostras
sample_corr = expression_df.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(sample_corr, cmap='coolwarm', center=0,
            square=True, linewidths=0.5)
plt.title("Matriz de Correlação de Amostras")
plt.tight_layout()
plt.savefig("sample_correlation.png", dpi=300, bbox_inches='tight')

# Clustering hierárquico
distances = pdist(expression_df.T, metric='correlation')
linkage = hierarchy.linkage(distances, method='average')

plt.figure(figsize=(12, 6))
hierarchy.dendrogram(linkage, labels=expression_df.columns)
plt.title("Clustering Hierárquico de Amostras")
plt.xlabel("Amostras")
plt.ylabel("Distância")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("sample_clustering.png", dpi=300, bbox_inches='tight')
```

### 7. Processamento em Lote de Múltiplos Datasets

**Baixe e Processe Múltiplas Series:**

```python
import GEOparse
import pandas as pd
import os

def batch_download_geo(gse_list, destdir="./geo_data"):
    """Baixe múltiplas series do GEO"""
    results = {}

    for gse_id in gse_list:
        try:
            print(f"Processando {gse_id}...")
            gse = GEOparse.get_GEO(geo=gse_id, destdir=destdir)

            # Extraia informações-chave
            results[gse_id] = {
                'title': gse.metadata.get('title', ['N/A'])[0],
                'organism': gse.metadata.get('organism', ['N/A'])[0],
                'platform': list(gse.gpls.keys())[0] if gse.gpls else 'N/A',
                'num_samples': len(gse.gsms),
                'submission_date': gse.metadata.get('submission_date', ['N/A'])[0]
            }

            # Salve dados de expressão
            if hasattr(gse, 'pivot_samples'):
                expr_df = gse.pivot_samples('VALUE')
                expr_df.to_csv(f"{destdir}/{gse_id}_expression.csv")
                results[gse_id]['num_genes'] = len(expr_df)

        except Exception as e:
            print(f"Erro ao processar {gse_id}: {e}")
            results[gse_id] = {'error': str(e)}

    # Salve sumário
    summary_df = pd.DataFrame(results).T
    summary_df.to_csv(f"{destdir}/batch_summary.csv")

    return results

# Processe múltiplos datasets
gse_list = ["GSE100001", "GSE100002", "GSE100003"]
results = batch_download_geo(gse_list)
```

**Meta-Análise Entre Estudos:**

```python
import GEOparse
import pandas as pd
import numpy as np

def meta_analysis_geo(gse_list, gene_of_interest):
    """Execute meta-análise de expressão gênica entre estudos"""
    results = []

    for gse_id in gse_list:
        try:
            gse = GEOparse.get_GEO(geo=gse_id, destdir="./data")

            # Obtenha anotação de plataforma
            gpl = list(gse.gpls.values())[0]

            # Encontre gene na plataforma
            if hasattr(gpl, 'table'):
                gene_probes = gpl.table[
                    gpl.table['Gene Symbol'].str.contains(
                        gene_of_interest,
                        case=False,
                        na=False
                    )
                ]

                if not gene_probes.empty:
                    expr_df = gse.pivot_samples('VALUE')

                    for probe_id in gene_probes['ID']:
                        if probe_id in expr_df.index:
                            expr_values = expr_df.loc[probe_id]

                            results.append({
                                'study': gse_id,
                                'probe': probe_id,
                                'mean_expression': expr_values.mean(),
                                'std_expression': expr_values.std(),
                                'num_samples': len(expr_values)
                            })

        except Exception as e:
            print(f"Erro em {gse_id}: {e}")

    return pd.DataFrame(results)

# Meta-análise para TP53
gse_studies = ["GSE100001", "GSE100002", "GSE100003"]
meta_results = meta_analysis_geo(gse_studies, "TP53")
print(meta_results)
```

## Instalação e Configuração

### Bibliotecas Python

```bash
# Biblioteca de acesso ao GEO primária (recomendada)
uv pip install GEOparse

# Para E-utilities e acesso programático ao NCBI
uv pip install biopython

# Para análise de dados
uv pip install pandas numpy scipy

# Para visualização
uv pip install matplotlib seaborn

# Para análise estatística
uv pip install statsmodels scikit-learn
```

### Configuração

Configure o acesso aos E-utilities do NCBI:

```python
from Bio import Entrez

# Sempre defina seu email (obrigatório pelo NCBI)
Entrez.email = "seu.email@exemplo.com"

# Opcional: Defina chave de API para limites de taxa aumentados
# Obtenha sua chave de API em: https://www.ncbi.nlm.nih.gov/account/
Entrez.api_key = "sua_chave_api_aqui"

# Com chave de API: 10 requisições/segundo
# Sem chave de API: 3 requisições/segundo
```

## Casos de Uso Comuns

### Pesquisa em Transcriptômica
- Baixe dados de expressão gênica para condições específicas
- Compare perfis de expressão entre estudos
- Identifique genes expressos diferencialmente
- Execute meta-análises entre múltiplos datasets

### Estudos de Resposta a Medicamentos
- Analise mudanças de expressão gênica após tratamento com fármaco
- Identifique biomarcadores para resposta a fármaco
- Compare efeitos de fármacos entre linhagens celulares ou pacientes
- Construa modelos preditivos para sensibilidade a fármaco

### Biologia de Doenças
- Estude expressão gênica em tecidos com doença vs. normal
- Identifique assinaturas de expressão associadas a doença
- Compare subgrupos de pacientes e estágios de doença
- Correlacione expressão com desfechos clínicos

### Descoberta de Biomarcadores
- Selecione marcadores diagnósticos ou prognósticos
- Valide biomarcadores entre coortes independentes
- Compare desempenho de marcadores entre plataformas
- Integre expressão com dados clínicos

## Conceitos-Chave

**SOFT (Simple Omnibus Format in Text):** Formato baseado em texto primário do GEO contendo metadados e tabelas de dados. Facilmente analisado por GEOparse.

**MINiML (MIAME Notation in Markup Language):** Formato XML para dados do GEO, usado para acesso programático e troca de dados.

**Series Matrix:** Matriz de expressão separada por tabulações com amostras como colunas e genes/probes como linhas. Formato mais rápido para obter dados de expressão.

**Conformidade MIAME:** Minimum Information About a Microarray Experiment - anotação padronizada que o GEO impõe para todos os envios.

**Tipos de Valor de Expressão:** Diferentes tipos de medidas de expressão (sinal bruto, normalizado, log-transformado). Sempre verifique plataforma e métodos de processamento.

**Anotação de Plataforma:** Mapeia IDs de probe/feature para genes. Essencial para interpretação biológica de dados de expressão.

## Ferramenta Web GEO2R

Para análise rápida sem programação, use GEO2R:

- Ferramenta de análise estatística baseada em web integrada ao GEO
- Acessível em: https://www.ncbi.nlm.nih.gov/geo/geo2r/?acc=GSExxxxx
- Realiza análise de expressão diferencial
- Gera scripts R para reprodutibilidade
- Útil para análise exploratória antes de baixar dados

## Limitação de Taxa e Boas Práticas

**Limites de Taxa do NCBI E-utilities:**
- Sem chave de API: 3 requisições por segundo
- Com chave de API: 10 requisições por segundo
- Implemente atrasos entre requisições: `time.sleep(0.34)` (sem chave de API) ou `time.sleep(0.1)` (com chave de API)

**Acesso FTP:**
- Sem limites de taxa para downloads via FTP
- Método preferido para downloads em massa
- Pode baixar diretórios inteiros com wget -r

**Cache do GEOparse:**
- GEOparse armazena automaticamente em cache arquivos baixados em destdir
- Chamadas subsequentes usam dados em cache
- Limpe o cache periodicamente para economizar espaço em disco

**Práticas Ideais:**
- Use GEOparse para acesso em nível de series (mais fácil)
- Use E-utilities para pesquisa de metadados e queries em lote
- Use FTP para downloads diretos de arquivos e operações em massa
- Armazene dados localmente em cache para evitar downloads repetidos
- Sempre defina Entrez.email ao usar Biopython

## Recursos

### references/geo_reference.md

Documentação de referência abrangente cobrindo:
- Especificações detalhadas de API E-utilities e endpoints
- Documentação completa de formato de arquivo SOFT e MINiML
- Padrões avançados de uso de GEOparse e exemplos
- Estrutura de diretório de FTP e convenções de nomenclatura de arquivo
- Pipelines de processamento de dados e métodos de normalização
- Troubleshooting de problemas comuns e tratamento de erros
- Considerações específicas de plataforma e particularidades

Consulte esta referência para detalhes técnicos aprofundados, padrões de query complexos ou ao trabalhar com formatos de dados incomuns.

## Notas