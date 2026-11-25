---
name: cosmic-database
description: "Acesse o banco de dados de mutações de câncer COSMIC. Consulte mutações somáticas, Cancer Gene Census, assinaturas mutacionais, fusões gênicas para pesquisa de câncer e oncologia de precisão. Requer autenticação."
---

# Banco de Dados COSMIC

## Visão Geral

COSMIC (Catalogue of Somatic Mutations in Cancer) é o maior e mais abrangente banco de dados do mundo para explorar mutações somáticas em câncer humano. Acesse a vasta coleção de dados de genômica de câncer do COSMIC, incluindo milhões de mutações em milhares de tipos de câncer, listas de genes curadas, assinaturas mutacionais e anotações clínicas de forma programática.

## Quando Usar Esta Skill

Esta skill deve ser usada quando:
- Baixar dados de mutações de câncer do COSMIC
- Acessar o Cancer Gene Census para listas de genes de câncer curadas
- Recuperar perfis de assinatura mutacional
- Consultar variantes estruturais, alterações de número de cópias ou fusões gênicas
- Analisar mutações de resistência a drogas
- Trabalhar com dados genômicos de linhagens de células cancerosas
- Integrar dados de mutações de câncer em pipelines de bioinformática
- Pesquisar genes ou mutações específicas em contextos de câncer

## Pré-requisitos

### Registro de Conta
COSMIC requer autenticação para downloads de dados:
- **Usuários acadêmicos**: Acesso gratuito com registro em https://cancer.sanger.ac.uk/cosmic/register
- **Usuários comerciais**: Licença necessária (entre em contato com QIAGEN)

### Requisitos Python
```bash
uv pip install requests pandas
```

## Início Rápido

### 1. Download Básico de Arquivo

Use o script `scripts/download_cosmic.py` para baixar arquivos de dados do COSMIC:

```python
from scripts.download_cosmic import download_cosmic_file

# Download de dados de mutação
download_cosmic_file(
    email="your_email@institution.edu",
    password="your_password",
    filepath="GRCh38/cosmic/latest/CosmicMutantExport.tsv.gz",
    output_filename="cosmic_mutations.tsv.gz"
)
```

### 2. Uso via Linha de Comando

```bash
# Download usando abreviação de tipo de dados
python scripts/download_cosmic.py user@email.com --data-type mutations

# Download de arquivo específico
python scripts/download_cosmic.py user@email.com \
    --filepath GRCh38/cosmic/latest/cancer_gene_census.csv

# Download para montagem genômica específica
python scripts/download_cosmic.py user@email.com \
    --data-type gene_census --assembly GRCh37 -o cancer_genes.csv
```

### 3. Trabalhando com Dados Baixados

```python
import pandas as pd

# Leitura de dados de mutação
mutations = pd.read_csv('cosmic_mutations.tsv.gz', sep='\t', compression='gzip')

# Leitura de Cancer Gene Census
gene_census = pd.read_csv('cancer_gene_census.csv')

# Leitura de formato VCF
import pysam
vcf = pysam.VariantFile('CosmicCodingMuts.vcf.gz')
```

## Tipos de Dados Disponíveis

### Mutações Principais
Baixe dados abrangentes de mutações, incluindo mutações pontuais, indels e anotações genômicas.

**Tipos de dados comuns**:
- `mutations` - Mutações codificantes completas (formato TSV)
- `mutations_vcf` - Mutações codificantes em formato VCF
- `sample_info` - Metadados de amostra e informações de tumor

```python
# Download de todas as mutações codificantes
download_cosmic_file(
    email="user@email.com",
    password="password",
    filepath="GRCh38/cosmic/latest/CosmicMutantExport.tsv.gz"
)
```

### Cancer Gene Census
Acesse a lista curada por especialistas de ~700+ genes de câncer com evidências substanciais de envolvimento em câncer.

```python
# Download de Cancer Gene Census
download_cosmic_file(
    email="user@email.com",
    password="password",
    filepath="GRCh38/cosmic/latest/cancer_gene_census.csv"
)
```

**Casos de uso**:
- Identificar genes de câncer conhecidos
- Filtrar variantes por relevância para câncer
- Compreender funções gênicas (oncogene vs supressor tumoral)
- Seleção de genes-alvo para pesquisa

### Assinaturas Mutacionais
Baixe perfis de assinatura para análise de assinatura mutacional.

```python
# Download de definições de assinatura
download_cosmic_file(
    email="user@email.com",
    password="password",
    filepath="signatures/signatures.tsv"
)
```

**Tipos de assinatura**:
- Assinaturas de Single Base Substitution (SBS)
- Assinaturas de Doublet Base Substitution (DBS)
- Assinaturas de Insertion/Deletion (ID)

### Variantes Estruturais e Fusões
Acesse dados de fusão gênica e rearranjos estruturais.

**Tipos de dados disponíveis**:
- `structural_variants` - Breakpoints estruturais
- `fusion_genes` - Eventos de fusão gênica

```python
# Download de fusões gênicas
download_cosmic_file(
    email="user@email.com",
    password="password",
    filepath="GRCh38/cosmic/latest/CosmicFusionExport.tsv.gz"
)
```

### Número de Cópias e Expressão
Recupere alterações de número de cópias e dados de expressão gênica.

**Tipos de dados disponíveis**:
- `copy_number` - Ganhos/perdas de número de cópias
- `gene_expression` - Dados de sobre/sub-expressão

```python
# Download de dados de número de cópias
download_cosmic_file(
    email="user@email.com",
    password="password",
    filepath="GRCh38/cosmic/latest/CosmicCompleteCNA.tsv.gz"
)
```

### Mutações de Resistência
Acesse dados de mutações de resistência a drogas com anotações clínicas.

```python
# Download de mutações de resistência
download_cosmic_file(
    email="user@email.com",
    password="password",
    filepath="GRCh38/cosmic/latest/CosmicResistanceMutations.tsv.gz"
)
```

## Trabalhando com Dados COSMIC

### Montagens Genômicas
COSMIC fornece dados para dois genomas de referência:
- **GRCh38** (recomendado, padrão atual)
- **GRCh37** (legado, para pipelines mais antigos)

Especifique a montagem em caminhos de arquivo:
```python
# GRCh38 (recomendado)
filepath="GRCh38/cosmic/latest/CosmicMutantExport.tsv.gz"

# GRCh37 (legado)
filepath="GRCh37/cosmic/latest/CosmicMutantExport.tsv.gz"
```

### Versionamento
- Use `latest` em caminhos de arquivo para sempre obter a versão mais recente
- COSMIC é atualizado trimestralmente (versão atual: v102, maio de 2025)
- Versões específicas podem ser usadas para reprodutibilidade: `v102`, `v101`, etc.

### Formatos de Arquivo
- **TSV/CSV**: Separados por tabulação/vírgula, comprimidos com gzip, leitura com pandas
- **VCF**: Formato de variante padrão, use com pysam, bcftools ou GATK
- Todos os arquivos incluem cabeçalhos descrevendo o conteúdo das colunas

### Padrões de Análise Comuns

**Filtrar mutações por gene**:
```python
import pandas as pd

mutations = pd.read_csv('cosmic_mutations.tsv.gz', sep='\t', compression='gzip')
tp53_mutations = mutations[mutations['Gene name'] == 'TP53']
```

**Identificar genes de câncer por papel**:
```python
gene_census = pd.read_csv('cancer_gene_census.csv')
oncogenes = gene_census[gene_census['Role in Cancer'].str.contains('oncogene', na=False)]
tumor_suppressors = gene_census[gene_census['Role in Cancer'].str.contains('TSG', na=False)]
```

**Extrair mutações por tipo de câncer**:
```python
mutations = pd.read_csv('cosmic_mutations.tsv.gz', sep='\t', compression='gzip')
lung_mutations = mutations[mutations['Primary site'] == 'lung']
```

**Trabalhar com arquivos VCF**:
```python
import pysam

vcf = pysam.VariantFile('CosmicCodingMuts.vcf.gz')
for record in vcf.fetch('17', 7577000, 7579000):  # TP53 region
    print(record.id, record.ref, record.alts, record.info)
```

## Referência de Dados

Para informações abrangentes sobre a estrutura de dados do COSMIC, arquivos disponíveis e descrições de campos, consulte `references/cosmic_data_reference.md`. Esta referência inclui:

- Lista completa de tipos de dados disponíveis e arquivos
- Descrições detalhadas de campo para cada tipo de arquivo
- Especificações de formato de arquivo
- Caminhos de arquivo comuns e convenções de nomenclatura
- Cronograma de atualização de dados e versionamento
- Informações de citação

Use esta referência quando:
- Explorar quais dados estão disponíveis no COSMIC
- Compreender significados de campos específicos
- Determinar o caminho de arquivo correto para um tipo de dados
- Planejar workflows de análise com dados COSMIC

## Funções Auxiliares

O script de download inclui funções auxiliares para operações comuns:

### Obter Caminhos de Arquivo Comuns
```python
from scripts.download_cosmic import get_common_file_path

# Obter caminho para arquivo de mutações
path = get_common_file_path('mutations', genome_assembly='GRCh38')
# Retorna: 'GRCh38/cosmic/latest/CosmicMutantExport.tsv.gz'

# Obter caminho para gene census
path = get_common_file_path('gene_census')
# Retorna: 'GRCh38/cosmic/latest/cancer_gene_census.csv'
```

**Abreviações disponíveis**:
- `mutations` - Mutações codificantes principais
- `mutations_vcf` - Mutações em formato VCF
- `gene_census` - Cancer Gene Census
- `resistance_mutations` - Dados de resistência a drogas
- `structural_variants` - Variantes estruturais
- `gene_expression` - Dados de expressão
- `copy_number` - Alterações de número de cópias
- `fusion_genes` - Fusões gênicas
- `signatures` - Assinaturas mutacionais
- `sample_info` - Metadados de amostra

## Resolução de Problemas

### Erros de Autenticação
- Verifique se email e senha estão corretos
- Certifique-se de que a conta está registrada em cancer.sanger.ac.uk/cosmic
- Verifique se uma licença comercial é necessária para seu caso de uso

### Arquivo Não Encontrado
- Verifique se o caminho está correto
- Verifique se a versão solicitada existe
- Use `latest` para a versão mais recente
- Confirme a montagem genômica (GRCh37 vs GRCh38) está correta

### Downloads de Arquivo Grande
- Arquivos COSMIC podem ter vários GB de tamanho
- Certifique-se de ter espaço em disco suficiente
- O download pode levar vários minutos dependendo da conexão
- O script mostra progresso de download para arquivos grandes

### Uso Comercial
- Usuários comerciais devem licenciar COSMIC através da QIAGEN
- Contato: cosmic-translation@sanger.ac.uk
- O acesso acadêmico é gratuito, mas requer registro

## Integração com Outras Ferramentas

Dados COSMIC se integram bem com:
- **Anotação de variantes**: VEP, ANNOVAR, SnpEff
- **Análise de assinatura**: SigProfiler, deconstructSigs, MuSiCa
- **Genômica de câncer**: cBioPortal, OncoKB, CIViC
- **Bioinformática**: Bioconductor, ferramentas de análise TCGA
- **Data science**: pandas, scikit-learn, PyTorch

## Recursos Adicionais

- **Site COSMIC**: https://cancer.sanger.ac.uk/cosmic
- **Documentação**: https://cancer.sanger.ac.uk/cosmic/help
- **Release Notes**: https://cancer.sanger.ac.uk/cosmic/release_notes
- **Contato**: cosmic@sanger.ac.uk

## Citação

Ao usar dados COSMIC, cite:
Tate JG, Bamford S, Jubb HC, et al. COSMIC: the Catalogue Of Somatic Mutations In Cancer. Nucleic Acids Research. 2019;47(D1):D941-D947.