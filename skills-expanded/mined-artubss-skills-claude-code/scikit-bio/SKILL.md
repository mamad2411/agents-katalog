---
name: scikit-bio
description: "Kit de ferramentas para dados biológicos. Análise de sequências, alinhamentos, árvores filogenéticas, métricas de diversidade (alfa/beta, UniFrac), ordenação (PCoA), PERMANOVA, I/O FASTA/Newick, para análise de microbioma."
---

# scikit-bio

## Visão geral

scikit-bio é uma biblioteca Python abrangente para trabalhar com dados biológicos. Use esta skill para análises bioinformáticas abrangendo manipulação de sequências, alinhamento, filogenética, ecologia microbiana e estatísticas multivariadas.

## Quando usar esta skill

Esta skill deve ser utilizada quando o usuário:
- Trabalha com sequências biológicas (DNA, RNA, proteína)
- Precisa ler/escrever formatos de arquivo biológico (FASTA, FASTQ, GenBank, Newick, BIOM, etc.)
- Realiza alinhamentos de sequências ou busca motivos
- Constrói ou analisa árvores filogenéticas
- Calcula métricas de diversidade (diversidade alfa/beta, distâncias UniFrac)
- Realiza análise de ordenação (PCoA, CCA, RDA)
- Executa testes estatísticos em dados biológicos/ecológicos (PERMANOVA, ANOSIM, Mantel)
- Analisa dados de microbioma ou ecologia de comunidades
- Trabalha com embeddings de proteína de modelos de linguagem
- Precisa manipular tabelas de dados biológicos

## Capacidades principais

### 1. Manipulação de sequências

Trabalhe com sequências biológicas usando classes especializadas para dados de DNA, RNA e proteína.

**Operações principais:**
- Ler/escrever sequências de formatos FASTA, FASTQ, GenBank, EMBL
- Fatiamento de sequências, concatenação e busca
- Complemento reverso, transcrição (DNA→RNA) e tradução (RNA→proteína)
- Encontrar motivos e padrões usando regex
- Calcular distâncias (Hamming, baseada em k-mer)
- Lidar com pontuações de qualidade e metadados de sequência

**Padrões comuns:**
```python
import skbio

# Ler sequências do arquivo
seq = skbio.DNA.read('input.fasta')

# Operações em sequências
rc = seq.reverse_complement()
rna = seq.transcribe()
protein = rna.translate()

# Encontrar motivos
motif_positions = seq.find_with_regex('ATG[ACGT]{3}')

# Verificar propriedades
has_degens = seq.has_degenerates()
seq_no_gaps = seq.degap()
```

**Notas importantes:**
- Use as classes `DNA`, `RNA`, `Protein` para sequências com validação de alfabeto
- Use a classe `Sequence` para sequências genéricas sem restrições de alfabeto
- Pontuações de qualidade carregadas automaticamente de arquivos FASTQ em metadados posicionais
- Tipos de metadados: nível de sequência (ID, descrição), posicional (por base), intervalo (regiões/features)

### 2. Alinhamento de sequências

Realize alinhamentos de sequências pareados e múltiplos usando algoritmos de programação dinâmica.

**Capacidades principais:**
- Alinhamento global (Needleman-Wunsch com variante semi-global)
- Alinhamento local (Smith-Waterman)
- Esquemas de pontuação configuráveis (match/mismatch, penalidades de gap, matrizes de substituição)
- Conversão de string CIGAR
- Armazenamento e manipulação de alinhamento múltiplo com `TabularMSA`

**Padrões comuns:**
```python
from skbio.alignment import local_pairwise_align_ssw, TabularMSA

# Alinhamento pareado
alignment = local_pairwise_align_ssw(seq1, seq2)

# Acessar sequências alinhadas
msa = alignment.aligned_sequences

# Ler alinhamento múltiplo do arquivo
msa = TabularMSA.read('alignment.fasta', constructor=skbio.DNA)

# Calcular consenso
consensus = msa.consensus()
```

**Notas importantes:**
- Use `local_pairwise_align_ssw` para alinhamentos locais (mais rápido, baseado em SSW)
- Use `StripedSmithWaterman` para alinhamentos de proteína
- Penalidades de gap afim recomendadas para sequências biológicas
- Pode converter entre formatos de alinhamento scikit-bio, BioPython e Biotite

### 3. Árvores filogenéticas

Construa, manipule e analise árvores filogenéticas que representam relações evolutivas.

**Capacidades principais:**
- Construção de árvore a partir de matrizes de distância (UPGMA, WPGMA, Neighbor Joining, GME, BME)
- Manipulação de árvore (poda, rerraizamento, travessia)
- Cálculos de distância (patística, cofenítica, Robinson-Foulds)
- Visualização ASCII
- I/O de formato Newick

**Padrões comuns:**
```python
from skbio import TreeNode
from skbio.tree import nj

# Ler árvore do arquivo
tree = TreeNode.read('tree.nwk')

# Construir árvore a partir de matriz de distância
tree = nj(distance_matrix)

# Operações em árvore
subtree = tree.shear(['taxon1', 'taxon2', 'taxon3'])
tips = [node for node in tree.tips()]
lca = tree.lowest_common_ancestor(['taxon1', 'taxon2'])

# Calcular distâncias
patristic_dist = tree.find('taxon1').distance(tree.find('taxon2'))
cophenetic_matrix = tree.cophenetic_matrix()

# Comparar árvores
rf_distance = tree.robinson_foulds(other_tree)
```

**Notas importantes:**
- Use `nj()` para neighbor joining (método filogenético clássico)
- Use `upgma()` para UPGMA (assume relógio molecular)
- GME e BME são altamente escaláveis para árvores grandes
- Árvores podem ser enraizadas ou desenraizadas; algumas métricas exigem enraizamento específico

### 4. Análise de diversidade

Calcule métricas de diversidade alfa e beta para ecologia microbiana e análise de comunidades.

**Capacidades principais:**
- Diversidade alfa: riqueza, entropia de Shannon, índice de Simpson, Faith's PD, uniformidade de Pielou
- Diversidade beta: Bray-Curtis, Jaccard, UniFrac ponderado/não ponderado, distâncias euclidianas
- Métricas de diversidade filogenética (requer entrada de árvore)
- Rarefação e subamostragem
- Integração com ordenação e testes estatísticos

**Padrões comuns:**
```python
from skbio.diversity import alpha_diversity, beta_diversity
import skbio

# Diversidade alfa
alpha = alpha_diversity('shannon', counts_matrix, ids=sample_ids)
faith_pd = alpha_diversity('faith_pd', counts_matrix, ids=sample_ids,
                          tree=tree, otu_ids=feature_ids)

# Diversidade beta
bc_dm = beta_diversity('braycurtis', counts_matrix, ids=sample_ids)
unifrac_dm = beta_diversity('unweighted_unifrac', counts_matrix,
                           ids=sample_ids, tree=tree, otu_ids=feature_ids)

# Obter métricas disponíveis
from skbio.diversity import get_alpha_diversity_metrics
print(get_alpha_diversity_metrics())
```

**Notas importantes:**
- Contagens devem ser inteiros representando abundâncias, não frequências relativas
- Métricas filogenéticas (Faith's PD, UniFrac) requerem árvore e mapeamento de ID OTU
- Use `partial_beta_diversity()` para calcular apenas pares específicos de amostras
- Diversidade alfa retorna Series, diversidade beta retorna DistanceMatrix

### 5. Métodos de ordenação

Reduza dados biológicos de alta dimensionalidade para espaços de baixa dimensionalidade visualizáveis.

**Capacidades principais:**
- PCoA (Principal Coordinate Analysis) a partir de matrizes de distância
- CA (Correspondence Analysis) para tabelas de contingência
- CCA (Canonical Correspondence Analysis) com restrições ambientais
- RDA (Redundancy Analysis) para relações lineares
- Projeção de biplot para interpretação de features

**Padrões comuns:**
```python
from skbio.stats.ordination import pcoa, cca

# PCoA a partir de matriz de distância
pcoa_results = pcoa(distance_matrix)
pc1 = pcoa_results.samples['PC1']
pc2 = pcoa_results.samples['PC2']

# CCA com variáveis ambientais
cca_results = cca(species_matrix, environmental_matrix)

# Salvar/carregar resultados de ordenação
pcoa_results.write('ordination.txt')
results = skbio.OrdinationResults.read('ordination.txt')
```

**Notas importantes:**
- PCoA funciona com qualquer matriz de distância/dissimilaridade
- CCA revela drivers ambientais da composição de comunidades
- Resultados de ordenação incluem autovalores, proporção explicada e coordenadas de amostras/features
- Resultados integram com bibliotecas de visualização (matplotlib, seaborn, plotly)

### 6. Testes estatísticos

Realize testes de hipóteses específicos para dados ecológicos e biológicos.

**Capacidades principais:**
- PERMANOVA: teste diferenças entre grupos usando matrizes de distância
- ANOSIM: teste alternativo para diferenças entre grupos
- PERMDISP: teste homogeneidade de dispersões de grupo
- Teste de Mantel: correlação entre matrizes de distância
- Bioenv: encontra variáveis ambientais correlacionadas com distâncias

**Padrões comuns:**
```python
from skbio.stats.distance import permanova, anosim, mantel

# Teste se grupos diferem significativamente
permanova_results = permanova(distance_matrix, grouping, permutations=999)
print(f"p-value: {permanova_results['p-value']}")

# Teste ANOSIM
anosim_results = anosim(distance_matrix, grouping, permutations=999)

# Teste de Mantel entre duas matrizes de distância
mantel_results = mantel(dm1, dm2, method='pearson', permutations=999)
print(f"Correlation: {mantel_results[0]}, p-value: {mantel_results[1]}")
```

**Notas importantes:**
- Testes de permutação fornecem testes de significância não paramétricos
- Use 999+ permutações para p-valores robustos
- PERMANOVA sensível a diferenças de dispersão; combine com PERMDISP
- Testes de Mantel avaliam correlação de matriz (ex: distância geográfica vs genética)

### 7. I/O de arquivo e conversão de formato

Leia e escreva mais de 19 formatos de arquivo biológico com detecção automática de formato.

**Formatos suportados:**
- Sequências: FASTA, FASTQ, GenBank, EMBL, QSeq
- Alinhamentos: Clustal, PHYLIP, Stockholm
- Árvores: Newick
- Tabelas: BIOM (HDF5 e JSON)
- Distâncias: matrizes quadradas delimitadas
- Análises: BLAST+6/7, GFF3, resultados de ordenação
- Metadados: TSV/CSV com validação

**Padrões comuns:**
```python
import skbio

# Ler com detecção automática de formato
seq = skbio.DNA.read('file.fasta', format='fasta')
tree = skbio.TreeNode.read('tree.nwk')

# Escrever em arquivo
seq.write('output.fasta', format='fasta')

# Gerador para arquivos grandes (eficiente em memória)
for seq in skbio.io.read('large.fasta', format='fasta', constructor=skbio.DNA):
    process(seq)

# Converter formatos
seqs = list(skbio.io.read('input.fastq', format='fastq', constructor=skbio.DNA))
skbio.io.write(seqs, format='fasta', into='output.fasta')
```

**Notas importantes:**
- Use geradores para arquivos grandes para evitar problemas de memória
- Formato pode ser autodetectado quando o parâmetro `into` é especificado
- Alguns objetos podem ser escritos em múltiplos formatos
- Suporte para piping stdin/stdout com `verify=False`

### 8. Matrizes de distância

Crie e manipule matrizes de distância/dissimilaridade com métodos estatísticos.

**Capacidades principais:**
- Armazenar dados simétricos (DistanceMatrix) ou assimétricos (DissimilarityMatrix)
- Indexação e fatiamento baseados em ID
- Integração com diversidade, ordenação e testes estatísticos
- Ler/escrever formato de texto delimitado

**Padrões comuns:**
```python
from skbio import DistanceMatrix
import numpy as np

# Criar a partir de array
data = np.array([[0, 1, 2], [1, 0, 3], [2, 3, 0]])
dm = DistanceMatrix(data, ids=['A', 'B', 'C'])

# Acessar distâncias
dist_ab = dm['A', 'B']
row_a = dm['A']

# Ler do arquivo
dm = DistanceMatrix.read('distances.txt')

# Usar em análises posteriores
pcoa_results = pcoa(dm)
permanova_results = permanova(dm, grouping)
```

**Notas importantes:**
- DistanceMatrix força simetria e diagonal zero
- DissimilarityMatrix permite valores assimétricos
- IDs habilitam integração com metadados e conhecimento biológico
- Compatível com pandas, numpy e scikit-learn

### 9. Tabelas biológicas

Trabalhe com tabelas de features (tabelas OTU/ASV) comuns em pesquisa de microbioma.

**Capacidades principais:**
- I/O de formato BIOM (HDF5 e JSON)
- Integração com pandas, polars, AnnData, numpy
- Técnicas de aumento de dados (phylomix, mixup, métodos composicionais)
- Filtragem e normalização de amostras/features
- Integração de metadados

**Padrões comuns:**
```python
from skbio import Table

# Ler tabela BIOM
table = Table.read('table.biom')

# Acessar dados
sample_ids = table.ids(axis='sample')
feature_ids = table.ids(axis='observation')
counts = table.matrix_data

# Filtrar
filtered = table.filter(sample_ids_to_keep, axis='sample')

# Converter para/de pandas
df = table.to_dataframe()
table = Table.from_dataframe(df)
```

**Notas importantes:**
- Tabelas BIOM são padrão em workflows QIIME 2
- Linhas normalmente representam amostras, colunas representam features (OTUs/ASVs)
- Suporta representações esparsas e densas
- Formato de saída configurável (pandas/polars/numpy)

### 10. Embeddings de proteína

Trabalhe com embeddings de modelos de linguagem de proteína para análise posterior.

**Capacidades principais:**
- Armazenar embeddings de modelos de linguagem de proteína (ESM, ProtTrans, etc.)
- Converter embeddings em matrizes de distância
- Gerar objetos de ordenação para visualização
- Exportar para numpy/pandas para workflows de ML

**Padrões comuns:**
```python
from skbio.embedding import ProteinEmbedding, ProteinVector

# Criar embedding a partir de array
embedding = ProteinEmbedding(embedding_array, sequence_ids)

# Converter em matriz de distância para análise
dm = embedding.to_distances(metric='euclidean')

# Visualização PCoA do espaço de embedding
pcoa_results = embedding.to_ordination(metric='euclidean', method='pcoa')

# Exportar para machine learning
array = embedding.to_array()
df = embedding.to_dataframe()
```

**Notas importantes:**
- Embeddings fazem ponte entre modelos de linguagem de proteína e bioinformática tradicional
- Compatíveis com o ecossistema de distância/ordenação/estatísticas do scikit-bio
- SequenceEmbedding e ProteinEmbedding fornecem funcionalidade especializada
- Útil para clustering de sequências, classificação e visualização

## Melhores práticas

### Instalação
```bash
uv pip install scikit-bio
```

### Considerações de desempenho
- Use geradores para arquivos de sequências grandes para minimizar uso de memória
- Para árvores filogenéticas massivas, prefira GME ou BME em vez de NJ
- Cálculos de diversidade beta podem ser paralelizados com `partial_beta_diversity()`
- Formato BIOM (HDF5) mais eficiente que JSON para tabelas grandes

### Integração com ecossistema
- Sequências interoperam com Biopython via formatos padrão
- Tabelas integram com pandas, polars e AnnData
- Matrizes de distância compatíveis com scikit-learn
- Resultados de ordenação visualizáveis com matplotlib/seaborn/plotly
- Funciona perfeitamente com artefatos QIIME 2 (BIOM, árvores, matrizes de distância)

### Workflows comuns
1. **Análise de diversidade de microbioma**: Ler tabela BIOM → Calcular diversidade alfa/beta → Ordenação (PCoA) → Testes estatísticos (PERMANOVA)
2. **Análise filogenética**: Ler sequências → Alinhar → Construir matriz de distância → Construir árvore → Calcular distâncias filogenéticas
3. **Processamento de sequências**: Ler FASTQ → Filtrar qualidade → Aparar/limpar → Encontrar motivos → Traduzir → Escrever FASTA
4. **Genômica comparativa**: Ler sequências → Alinhamento pareado → Calcular distâncias → Construir árvore → Analisar clados

## Documentação de referência

Para informações detalhadas da API, especificações de parâmetros e exemplos de uso avançado, consulte `references/api_reference.md` que contém documentação abrangente sobre:
- Assinaturas de métodos completas e parâmetros para todas as capacidades
- Exemplos de código estendidos para workflows complexos
- Resolução de problemas comuns
- Dicas de otimização de desempenho
- Padrões de integração com outras bibliotecas

## Recursos adicionais

- Documentação oficial: https://scikit.bio/docs/latest/
- Repositório GitHub: https://github.com/scikit-bio/scikit-bio
- Suporte em fórum: https://forum.qiime2.org (scikit-bio faz parte do ecossistema QIIME 2)