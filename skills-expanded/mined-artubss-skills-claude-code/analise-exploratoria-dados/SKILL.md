---
name: analise-exploratoria-dados
description: Realize análise exploratória abrangente em arquivos de dados científicos em mais de 200 formatos de arquivo. Esta habilidade deve ser usada ao analisar qualquer arquivo de dados científico para compreender sua estrutura, conteúdo, qualidade e características. Detecta automaticamente o tipo de arquivo e gera relatórios detalhados em markdown com análise específica do formato, métricas de qualidade e recomendações de análise posterior. Cobre química, bioinformática, microscopia, espectroscopia, proteômica, metabolômica e formatos gerais de dados científicos.
---

# Análise Exploratória de Dados

## Visão Geral

Realize análise exploratória de dados (EDA) abrangente em arquivos de dados científicos em múltiplos domínios. Esta habilidade fornece detecção automática de tipo de arquivo, análise específica do formato, avaliação da qualidade dos dados e gera relatórios detalhados em markdown adequados para documentação e planejamento de análises posteriores.

**Capacidades principais:**
- Detecção automática e análise de 200+ formatos de arquivo científico
- Extração abrangente de metadados específica do formato
- Avaliação de qualidade e integridade dos dados
- Resumos estatísticos e distribuições
- Recomendações de visualização
- Sugestões de análise posterior
- Geração de relatórios em markdown

## Quando Usar Esta Habilidade

Use esta habilidade quando:
- O usuário fornece um caminho para um arquivo de dados científico para análise
- O usuário pede para "explorar", "analisar" ou "resumir" um arquivo de dados
- O usuário quer entender a estrutura e o conteúdo de dados científicos
- O usuário precisa de um relatório abrangente de um dataset antes da análise
- O usuário quer avaliar a qualidade ou completude dos dados
- O usuário pergunta que tipo de análise é apropriado para um arquivo

## Categorias de Arquivo Suportadas

A habilidade possui cobertura abrangente de formatos de arquivo científico organizados em seis categorias principais:

### 1. Formatos de Química e Moléculas (60+ extensões)
Arquivos de estrutura, saídas de química computacional, trajetórias de dinâmica molecular e bancos de dados químicos.

**Tipos de arquivo incluem:** `.pdb`, `.cif`, `.mol`, `.mol2`, `.sdf`, `.xyz`, `.smi`, `.gro`, `.log`, `.fchk`, `.cube`, `.dcd`, `.xtc`, `.trr`, `.prmtop`, `.psf` e muitos mais.

**Arquivo de referência:** `references/chemistry_molecular_formats.md`

### 2. Formatos de Bioinformática e Genômica (50+ extensões)
Dados de sequências, alinhamentos, anotações, variantes e dados de expressão.

**Tipos de arquivo incluem:** `.fasta`, `.fastq`, `.sam`, `.bam`, `.vcf`, `.bed`, `.gff`, `.gtf`, `.bigwig`, `.h5ad`, `.loom`, `.counts`, `.mtx` e muitos mais.

**Arquivo de referência:** `references/bioinformatics_genomics_formats.md`

### 3. Formatos de Microscopia e Imagem (45+ extensões)
Imagens de microscopia, imagens médicas, imagens de lâminas inteiras e microscopia eletrônica.

**Tipos de arquivo incluem:** `.tif`, `.nd2`, `.lif`, `.czi`, `.ims`, `.dcm`, `.nii`, `.mrc`, `.dm3`, `.vsi`, `.svs`, `.ome.tiff` e muitos mais.

**Arquivo de referência:** `references/microscopy_imaging_formats.md`

### 4. Formatos de Espectroscopia e Química Analítica (35+ extensões)
RMN, espectrometria de massa, IR/Raman, UV-Vis, raio-X, cromatografia e outras técnicas analíticas.

**Tipos de arquivo incluem:** `.fid`, `.mzML`, `.mzXML`, `.raw`, `.mgf`, `.spc`, `.jdx`, `.xy`, `.cif` (cristalografia), `.wdf` e muitos mais.

**Arquivo de referência:** `references/spectroscopy_analytical_formats.md`

### 5. Formatos de Proteômica e Metabolômica (30+ extensões)
Proteômica de espectrometria de massa, metabolômica, lipidomia e dados multi-omics.

**Tipos de arquivo incluem:** `.mzML`, `.pepXML`, `.protXML`, `.mzid`, `.mzTab`, `.sky`, `.mgf`, `.msp`, `.h5ad` e muitos mais.

**Arquivo de referência:** `references/proteomics_metabolomics_formats.md`

### 6. Formatos Gerais de Dados Científicos (30+ extensões)
Arrays, tabelas, dados hierárquicos, arquivos compactados e formatos científicos comuns.

**Tipos de arquivo incluem:** `.npy`, `.npz`, `.csv`, `.xlsx`, `.json`, `.hdf5`, `.zarr`, `.parquet`, `.mat`, `.fits`, `.nc`, `.xml` e muitos mais.

**Arquivo de referência:** `references/general_scientific_formats.md`

## Fluxo de Trabalho

### Etapa 1: Detecção de Tipo de Arquivo

Quando um usuário fornece um caminho de arquivo, primeiro identifique o tipo de arquivo:

1. Extraia a extensão do arquivo
2. Procure a extensão no arquivo de referência apropriado
3. Identifique a categoria e descrição do formato
4. Carregue as informações específicas do formato

**Exemplo:**
```
Usuário: "Analize data.fastq"
→ Extensão: .fastq
→ Categoria: bioinformatics_genomics
→ Formato: Formato FASTQ (dados de sequência com scores de qualidade)
→ Referência: references/bioinformatics_genomics_formats.md
```

### Etapa 2: Carregue Informações Específicas do Formato

Com base no tipo de arquivo, leia o arquivo de referência correspondente para entender:
- **Dados Típicos:** Que tipo de dados este formato contém
- **Casos de Uso:** Aplicações comuns para este formato
- **Bibliotecas Python:** Como ler o arquivo em Python
- **Abordagem EDA:** Que análises são apropriadas para este tipo de dados

Procure no arquivo de referência a extensão específica (ex: procure por "### .fastq" em `bioinformatics_genomics_formats.md`).

### Etapa 3: Realize Análise de Dados

Use o script `scripts/eda_analyzer.py` OU implemente análise customizada:

**Opção A: Use o script analisador**
```python
# O script automaticamente:
# 1. Detecta tipo de arquivo
# 2. Carrega informações de referência
# 3. Realiza análise específica do formato
# 4. Gera relatório em markdown

python scripts/eda_analyzer.py <filepath> [output.md]
```

**Opção B: Análise customizada na conversa**
Com base na informação de formato do arquivo de referência, realize análise apropriada:

Para dados tabulares (CSV, TSV, Excel):
- Carregue com pandas
- Verifique dimensões, tipos de dados
- Analise valores ausentes
- Calcule estatísticas resumidas
- Identifique outliers
- Verifique duplicatas

Para dados de sequência (FASTA, FASTQ):
- Conte sequências
- Analise distribuições de comprimento
- Calcule conteúdo GC
- Avalie scores de qualidade (FASTQ)

Para imagens (TIFF, ND2, CZI):
- Verifique dimensões (X, Y, Z, C, T)
- Analise profundidade de bits e intervalo de valores
- Extraia metadados (canais, timestamps, calibração espacial)
- Calcule estatísticas de intensidade

Para arrays (NPY, HDF5):
- Verifique forma e dimensões
- Analise tipo de dados
- Calcule resumos estatísticos
- Verifique valores ausentes/inválidos

### Etapa 4: Gere Relatório Abrangente

Crie um relatório em markdown com as seguintes seções:

#### Seções Obrigatórias:
1. **Título e Metadados**
   - Nome do arquivo e timestamp
   - Tamanho do arquivo e localização

2. **Informações Básicas**
   - Propriedades do arquivo
   - Identificação do formato

3. **Detalhes do Tipo de Arquivo**
   - Descrição do formato da referência
   - Conteúdo de dados típico
   - Casos de uso comuns
   - Bibliotecas Python para leitura

4. **Análise de Dados**
   - Estrutura e dimensões
   - Resumos estatísticos
   - Avaliação de qualidade
   - Características dos dados

5. **Descobertas Principais**
   - Padrões notáveis
   - Problemas potenciais
   - Métricas de qualidade

6. **Recomendações**
   - Etapas de pré-processamento
   - Análises apropriadas
   - Ferramentas e métodos
   - Abordagens de visualização

#### Localização do Template
Use `assets/report_template.md` como guia para a estrutura do relatório.

### Etapa 5: Salve Relatório

Salve o relatório em markdown com um nome descritivo:
- Padrão: `{nome_arquivo_original}_eda_report.md`
- Exemplo: `experiment_data.fastq` → `experiment_data_eda_report.md`

## Referências Detalhadas de Formato

Cada arquivo de referência contém informações abrangentes para dezenas de tipos de arquivo. Para encontrar informações sobre um formato específico:

1. Identifique a categoria pela extensão
2. Leia o arquivo de referência apropriado
3. Procure pelo heading da seção correspondente à extensão (ex: "### .pdb")
4. Extraia a informação do formato

### Estrutura do Arquivo de Referência

Cada entrada de formato inclui:
- **Descrição:** O que é o formato
- **Dados Típicos:** O que contém
- **Casos de Uso:** Aplicações comuns
- **Bibliotecas Python:** Como lê-lo (com exemplos de código)
- **Abordagem EDA:** Análises específicas a realizar

**Exemplo de busca:**
```markdown
### .pdb - Protein Data Bank
**Descrição:** Formato padrão para estruturas 3D de macromoléculas biológicas
**Dados Típicos:** Coordenadas atômicas, informações de resíduos, estrutura secundária
**Casos de Uso:** Análise de estrutura de proteína, visualização molecular, docking
**Bibliotecas Python:**
- `Biopython`: `Bio.PDB`
- `MDAnalysis`: `MDAnalysis.Universe('file.pdb')`
**Abordagem EDA:**
- Validação de estrutura (comprimentos de ligação, ângulos)
- Distribuição de fator B
- Detecção de resíduos ausentes
- Gráficos de Ramachandran
```

## Boas Práticas

### Leitura de Arquivos de Referência

Arquivos de referência são grandes (10.000+ palavras cada). Para usá-los de forma eficiente:

1. **Procure por extensão:** Use grep para encontrar o formato específico
   ```python
   import re
   with open('references/chemistry_molecular_formats.md', 'r') as f:
       content = f.read()
       pattern = r'### \.pdb[^#]*?(?=###|\Z)'
       match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
   ```

2. **Extraia seções relevantes:** Não carregue arquivos de referência inteiros desnecessariamente no contexto

3. **Armazene informações de formato em cache:** Se analisar múltiplos arquivos do mesmo tipo, reutilize a informação de formato

### Análise de Dados

1. **Procure amostras em arquivos grandes:** Para arquivos com milhões de registros, analise uma amostra representativa
2. **Trate erros com elegância:** Muitos formatos científicos requerem bibliotecas específicas; forneça instruções claras de instalação
3. **Valide metadados:** Verifique consistência de metadados (ex: dimensões informadas vs dados reais)
4. **Considere proveniência dos dados:** Observe instrumento, versões de software, etapas de processamento

### Geração de Relatório

1. **Seja abrangente:** Inclua todas as informações relevantes para análise posterior
2. **Seja específico:** Forneça recomendações concretas baseadas no tipo de arquivo
3. **Seja acionável:** Sugira próximos passos e ferramentas específicas
4. **Inclua exemplos de código:** Mostre como carregar e trabalhar com os dados

## Exemplos

### Exemplo 1: Analisando um arquivo FASTQ

```python
# Usuário fornece: "Analize reads.fastq"

# 1. Detecte tipo de arquivo
extension = '.fastq'
category = 'bioinformatics_genomics'

# 2. Leia informação de referência
# Procure em references/bioinformatics_genomics_formats.md por "### .fastq"

# 3. Realize análise
from Bio import SeqIO
sequences = list(SeqIO.parse('reads.fastq', 'fastq'))
# Calcule: contagem de leitura, distribuição de comprimento, scores de qualidade, conteúdo GC

# 4. Gere relatório
# Inclua: descrição do formato, resultados de análise, recomendações de QC

# 5. Salve como: reads_eda_report.md
```

### Exemplo 2: Analisando um dataset CSV

```python
# Usuário fornece: "Explore experiment_results.csv"

# 1. Detecte: .csv → general_scientific

# 2. Carregue referência para formato CSV

# 3. Analise
import pandas as pd
df = pd.read_csv('experiment_results.csv')
# Dimensões, dtypes, valores ausentes, estatísticas, correlações

# 4. Gere relatório com:
# - Estrutura de dados
# - Padrões de valores ausentes
# - Resumos estatísticos
# - Matriz de correlação
# - Resultados de detecção de outliers

# 5. Salve relatório
```

### Exemplo 3: Analisando dados de microscopia

```python
# Usuário fornece: "Analize cells.nd2"

# 1. Detecte: .nd2 → microscopy_imaging (formato Nikon)

# 2. Leia referência para formato ND2
# Aprenda: multi-dimensional (XYZCT), requer nd2reader

# 3. Analise
from nd2reader import ND2Reader
with ND2Reader('cells.nd2') as images:
    # Extraia: dimensões, canais, pontos de tempo, metadados
    # Calcule: estatísticas de intensidade, informação de frame

# 4. Gere relatório com:
# - Dimensões de imagem (XY, Z-stacks, tempo, canais)
# - Comprimentos de onda de canal
# - Tamanho de pixel e calibração
# - Recomendações para análise de imagem

# 5. Salve relatório
```

## Solução de Problemas

### Bibliotecas Ausentes

Muitos formatos científicos requerem bibliotecas especializadas:

**Problema:** Erro de importação ao tentar ler um arquivo

**Solução:** Forneça instruções claras de instalação
```python
try:
    from Bio import SeqIO
except ImportError:
    print("Instale Biopython: uv pip install biopython")
```

Requisitos comuns por categoria:
- **Bioinformática:** `biopython`, `pysam`, `pyBigWig`
- **Química:** `rdkit`, `mdanalysis`, `cclib`
- **Microscopia:** `tifffile`, `nd2reader`, `aicsimageio`, `pydicom`
- **Espectroscopia:** `nmrglue`, `pymzml`, `pyteomics`
- **Geral:** `pandas`, `numpy`, `h5py`, `scipy`

### Tipos de Arquivo Desconhecidos

Se uma extensão de arquivo não estiver nas referências:

1. Pergunte ao usuário sobre o formato do arquivo
2. Verifique se é uma variante específica do fabricante
3. Tente análise genérica baseada na estrutura do arquivo (texto vs binário)
4. Forneça recomendações gerais

### Arquivos Grandes

Para arquivos muito grandes:

1. Use estratégias de amostragem (primeiros N registros)
2. Use acesso mapeado em memória (para HDF5, NPY)
3. Processe em chunks (para CSV, FASTQ)
4. Forneça estimativas baseadas em amostras

## Uso de Script

O `scripts/eda_analyzer.py` pode ser usado diretamente:

```bash
# Uso básico
python scripts/eda_analyzer.py data.csv

# Especifique arquivo de saída
python scripts/eda_analyzer.py data.csv output_report.md

# O script irá:
# 1. Detectar tipo de arquivo automaticamente
# 2. Carregar referências de formato
# 3. Realizar análise apropriada
# 4. Gerar relatório em markdown
```

O script suporta análise automática para muitos formatos comuns, mas análise customizada na conversa fornece mais flexibilidade e insights específicos do domínio.

## Uso Avançado

### Análise de Múltiplos Arquivos

Ao analisar múltiplos arquivos relacionados:
1. Realize EDA individual em cada arquivo
2. Crie um relatório de comparação resumido
3. Identifique relacionamentos e dependências
4. Sugira estratégias de integração

### Controle de Qualidade

Para avaliação de qualidade de dados:
1. Verifique conformidade de formato
2. Valide consistência de metadados
3. Avalie completude
4. Identifique outliers e anomalias
5. Compare com intervalos/distribuições esperadas

### Recomendações de Pré-processamento

Com base em características dos dados, recomende:
1. Estratégias de normalização
2. Imputação de valores ausentes
3. Tratamento de outliers
4. Correção de batch
5. Conversões de formato

## Recursos

### scripts/
- `eda_analyzer.py`: Script de análise abrangente que pode ser executado diretamente ou importado

### references/
- `chemistry_molecular_formats.md`: 60+ formatos de arquivo química/moléculas
- `bioinformatics_genomics_formats.md`: 50+ formatos bioinformática
- `microscopy_imaging_formats.md`: 45+ formatos imagem
- `spectroscopy_analytical_formats.md`: 35+ formatos espectroscopia
- `proteomics_metabolomics_formats.md`: 30+ formatos omics
- `general_scientific_formats.md`: 30+ formatos gerais

### assets/
- `report_template.md`: Template markdown abrangente para relatórios EDA