---
name: kegg-database
description: "Acesso direto REST API ao KEGG (apenas uso acadêmico). Análise de vias metabólicas, mapeamento gene-vias, vias metabólicas, interações de drogas, conversão de IDs. Para workflows Python com múltiplos bancos de dados, prefira bioservices. Use isto para trabalho HTTP/REST direto ou controle específico de KEGG."
---

# KEGG Database

## Visão Geral

KEGG (Kyoto Encyclopedia of Genes and Genomes) é um recurso bioinformático abrangente para análise de vias biológicas e redes de interações moleculares.

**Importante**: A API KEGG está disponível apenas para uso acadêmico por usuários acadêmicos.

## Quando Usar Esta Skill

Esta skill deve ser usada ao consultar vias metabólicas, genes, compostos, enzimas, doenças e drogas em múltiplos organismos usando a REST API do KEGG.

## Início Rápido

A skill fornece:
1. Funções auxiliares em Python (`scripts/kegg_api.py`) para todas as operações da REST API do KEGG
2. Documentação de referência abrangente (`references/kegg_reference.md`) com especificações detalhadas da API

Quando usuários solicitam dados do KEGG, determine qual operação é necessária e use a função apropriada de `scripts/kegg_api.py`.

## Operações Principais

### 1. Informações do Banco de Dados (`kegg_info`)

Recupera metadados e estatísticas sobre bancos de dados KEGG.

**Quando usar**: Entender a estrutura do banco de dados, verificar dados disponíveis, obter informações de release.

**Uso**:
```python
from scripts.kegg_api import kegg_info

# Obter informações sobre banco de dados de vias
info = kegg_info('pathway')

# Obter informações específicas de organismo
hsa_info = kegg_info('hsa')  # Genoma humano
```

**Bancos de dados comuns**: `kegg`, `pathway`, `module`, `brite`, `genes`, `genome`, `compound`, `glycan`, `reaction`, `enzyme`, `disease`, `drug`

### 2. Listando Entradas (`kegg_list`)

Lista identificadores de entrada e nomes dos bancos de dados KEGG.

**Quando usar**: Obter todas as vias para um organismo, listar genes, recuperar catálogos de compostos.

**Uso**:
```python
from scripts.kegg_api import kegg_list

# Listar todas as vias de referência
pathways = kegg_list('pathway')

# Listar vias específicas de humanos
hsa_pathways = kegg_list('pathway', 'hsa')

# Listar genes específicos (máx. 10)
genes = kegg_list('hsa:10458+hsa:10459')
```

**Códigos de organismo comuns**: `hsa` (humano), `mmu` (camundongo), `dme` (mosca-da-fruta), `sce` (levedura), `eco` (E. coli)

### 3. Pesquisando (`kegg_find`)

Pesquisa bancos de dados KEGG por palavras-chave ou propriedades moleculares.

**Quando usar**: Encontrar genes por nome/descrição, pesquisar compostos por fórmula ou massa, descobrir entradas por palavras-chave.

**Uso**:
```python
from scripts.kegg_api import kegg_find

# Pesquisa por palavra-chave
results = kegg_find('genes', 'p53')
shiga_toxin = kegg_find('genes', 'shiga toxin')

# Pesquisa por fórmula química (correspondência exata)
compounds = kegg_find('compound', 'C7H10N4O2', 'formula')

# Pesquisa por intervalo de peso molecular
drugs = kegg_find('drug', '300-310', 'exact_mass')
```

**Opções de pesquisa**: `formula` (correspondência exata), `exact_mass` (intervalo), `mol_weight` (intervalo)

### 4. Recuperando Entradas (`kegg_get`)

Obtém entradas completas do banco de dados ou formatos de dados específicos.

**Quando usar**: Recuperar detalhes de vias, obter sequências de genes/proteínas, baixar mapas de vias, acessar estruturas de compostos.

**Uso**:
```python
from scripts.kegg_api import kegg_get

# Obter entrada de via
pathway = kegg_get('hsa00010')  # Via da glicólise

# Obter múltiplas entradas (máx. 10)
genes = kegg_get(['hsa:10458', 'hsa:10459'])

# Obter sequência de proteína (FASTA)
sequence = kegg_get('hsa:10458', 'aaseq')

# Obter sequência de nucleotídeo
nt_seq = kegg_get('hsa:10458', 'ntseq')

# Obter estrutura de composto
mol_file = kegg_get('cpd:C00002', 'mol')  # ATP em formato MOL

# Obter via como JSON (apenas uma entrada)
pathway_json = kegg_get('hsa05130', 'json')

# Obter imagem de via (apenas uma entrada)
pathway_img = kegg_get('hsa05130', 'image')
```

**Formatos de saída**: `aaseq` (FASTA de proteína), `ntseq` (FASTA de nucleotídeo), `mol` (formato MOL), `kcf` (formato KCF), `image` (PNG), `kgml` (XML), `json` (JSON de via)

**Importante**: Formatos de imagem, KGML e JSON permitem apenas uma entrada por vez.

### 5. Conversão de IDs (`kegg_conv`)

Converte identificadores entre KEGG e bancos de dados externos.

**Quando usar**: Integrar dados KEGG com outros bancos de dados, mapear IDs de genes, converter identificadores de compostos.

**Uso**:
```python
from scripts.kegg_api import kegg_conv

# Converter todos os genes humanos para IDs NCBI Gene
conversions = kegg_conv('ncbi-geneid', 'hsa')

# Converter gene específico
gene_id = kegg_conv('ncbi-geneid', 'hsa:10458')

# Converter para UniProt
uniprot_id = kegg_conv('uniprot', 'hsa:10458')

# Converter compostos para PubChem
pubchem_ids = kegg_conv('pubchem', 'compound')

# Conversão reversa (NCBI Gene ID para KEGG)
kegg_id = kegg_conv('hsa', 'ncbi-geneid')
```

**Conversões suportadas**: `ncbi-geneid`, `ncbi-proteinid`, `uniprot`, `pubchem`, `chebi`

### 6. Referência Cruzada (`kegg_link`)

Encontra entradas relacionadas dentro e entre bancos de dados KEGG.

**Quando usar**: Encontrar vias contendo genes, obter genes em uma via, mapear genes para grupos KO, encontrar compostos em vias.

**Uso**:
```python
from scripts.kegg_api import kegg_link

# Encontrar vias vinculadas a genes humanos
pathways = kegg_link('pathway', 'hsa')

# Obter genes em uma via específica
genes = kegg_link('genes', 'hsa00010')  # Genes da glicólise

# Encontrar vias contendo um gene específico
gene_pathways = kegg_link('pathway', 'hsa:10458')

# Encontrar compostos em uma via
compounds = kegg_link('compound', 'hsa00010')

# Mapear genes para grupos KO (ortologia)
ko_groups = kegg_link('ko', 'hsa:10458')
```

**Links comuns**: genes ↔ pathway, pathway ↔ compound, pathway ↔ enzyme, genes ↔ ko (ortologia)

### 7. Interações Droga-Droga (`kegg_ddi`)

Verifica interações entre drogas.

**Quando usar**: Analisar combinações de drogas, verificar contraindicações, pesquisa farmacológica.

**Uso**:
```python
from scripts.kegg_api import kegg_ddi

# Verificar uma droga
interactions = kegg_ddi('D00001')

# Verificar múltiplas drogas (máx. 10)
interactions = kegg_ddi(['D00001', 'D00002', 'D00003'])
```

## Workflows de Análise Comuns

### Workflow 1: Mapeamento Gene para Via

**Caso de uso**: Encontrar vias associadas a genes de interesse (ex: para análise de enriquecimento de vias).

```python
from scripts.kegg_api import kegg_find, kegg_link, kegg_get

# Etapa 1: Encontrar ID de gene pelo nome
gene_results = kegg_find('genes', 'p53')

# Etapa 2: Vincular gene a vias
pathways = kegg_link('pathway', 'hsa:7157')  # Gene TP53

# Etapa 3: Obter informações detalhadas de via
for pathway_line in pathways.split('\n'):
    if pathway_line:
        pathway_id = pathway_line.split('\t')[1].replace('path:', '')
        pathway_info = kegg_get(pathway_id)
        # Processar informações de via
```

### Workflow 2: Contexto de Enriquecimento de Via

**Caso de uso**: Obter todos os genes em vias de organismo para análise de enriquecimento.

```python
from scripts.kegg_api import kegg_list, kegg_link

# Etapa 1: Listar todas as vias humanas
pathways = kegg_list('pathway', 'hsa')

# Etapa 2: Para cada via, obter genes associados
for pathway_line in pathways.split('\n'):
    if pathway_line:
        pathway_id = pathway_line.split('\t')[0]
        genes = kegg_link('genes', pathway_id)
        # Processar genes para análise de enriquecimento
```

### Workflow 3: Análise de Composto para Via

**Caso de uso**: Encontrar vias metabólicas contendo compostos de interesse.

```python
from scripts.kegg_api import kegg_find, kegg_link, kegg_get

# Etapa 1: Pesquisar composto
compound_results = kegg_find('compound', 'glucose')

# Etapa 2: Vincular composto a reações
reactions = kegg_link('reaction', 'cpd:C00031')  # Glicose

# Etapa 3: Vincular reações a vias
pathways = kegg_link('pathway', 'rn:R00299')  # Reação específica

# Etapa 4: Obter detalhes de via
pathway_info = kegg_get('map00010')  # Glicólise
```

### Workflow 4: Integração entre Bancos de Dados

**Caso de uso**: Integrar dados KEGG com UniProt, NCBI ou PubChem.

```python
from scripts.kegg_api import kegg_conv, kegg_get

# Etapa 1: Converter IDs de genes KEGG para IDs de banco de dados externo
uniprot_map = kegg_conv('uniprot', 'hsa')
ncbi_map = kegg_conv('ncbi-geneid', 'hsa')

# Etapa 2: Analisar resultados de conversão
for line in uniprot_map.split('\n'):
    if line:
        kegg_id, uniprot_id = line.split('\t')
        # Usar IDs externos para integração

# Etapa 3: Obter sequências usando KEGG
sequence = kegg_get('hsa:10458', 'aaseq')
```

### Workflow 5: Análise de Via Específica de Organismo

**Caso de uso**: Comparar vias em diferentes organismos.

```python
from scripts.kegg_api import kegg_list, kegg_get

# Etapa 1: Listar vias para múltiplos organismos
human_pathways = kegg_list('pathway', 'hsa')
mouse_pathways = kegg_list('pathway', 'mmu')
yeast_pathways = kegg_list('pathway', 'sce')

# Etapa 2: Obter via de referência para comparação
ref_pathway = kegg_get('map00010')  # Glicólise de referência

# Etapa 3: Obter versões específicas de organismo
hsa_glycolysis = kegg_get('hsa00010')
mmu_glycolysis = kegg_get('mmu00010')
```

## Categorias de Vias

KEGG organiza vias em sete categorias principais. Ao interpretar IDs de vias ou recomendar vias a usuários:

1. **Metabolismo** (ex: `map00010` - Glicólise, `map00190` - Fosforilação oxidativa)
2. **Processamento de Informação Genética** (ex: `map03010` - Ribossoma, `map03040` - Spliceossoma)
3. **Processamento de Informação Ambiental** (ex: `map04010` - Sinalização MAPK, `map02010` - Transportadores ABC)
4. **Processos Celulares** (ex: `map04140` - Autofagia, `map04210` - Apoptose)
5. **Sistemas Organismos** (ex: `map04610` - Cascata do complemento, `map04910` - Sinalização de insulina)
6. **Doenças Humanas** (ex: `map05200` - Vias em câncer, `map05010` - Doença de Alzheimer)
7. **Desenvolvimento de Drogas** (classificações cronológicas e baseadas em alvo)

Consulte `references/kegg_reference.md` para listas detalhadas de vias e classificações.

## Identificadores e Formatos Importantes

### IDs de Vias
- `map#####` - Via de referência (genérica, não específica de organismo)
- `hsa#####` - Via humana
- `mmu#####` - Via de camundongo

### IDs de Genes
- Formato: `organismo:numero_gene` (ex: `hsa:10458`)

### IDs de Compostos
- Formato: `cpd:C#####` (ex: `cpd:C00002` para ATP)

### IDs de Drogas
- Formato: `dr:D#####` (ex: `dr:D00001`)

### IDs de Enzima
- Formato: `ec:EC_number` (ex: `ec:1.1.1.1`)

### IDs KO (KEGG Ortologia)
- Formato: `ko:K#####` (ex: `ko:K00001`)

## Limitações da API

Respeite estas restrições ao usar a API KEGG:

1. **Limites de entrada**: Máximo 10 entradas por operação (exceto imagem/kgml/json: apenas 1 entrada)
2. **Uso acadêmico**: API é apenas para uso acadêmico; uso comercial requer licença
3. **Códigos de status HTTP**: Verifique 200 (sucesso), 400 (requisição inválida), 404 (não encontrado)
4. **Rate limiting**: Sem limite explícito, mas evite requisições em rápida sequência

## Referência Detalhada

Para documentação abrangente de API, especificações de banco de dados, códigos de organismo e uso avançado, consulte `references/kegg_reference.md`. Isto inclui:

- Lista completa de bancos de dados KEGG
- Sintaxe detalhada de operação de API
- Todos os códigos de organismo
- Códigos de status HTTP e tratamento de erros
- Integração com Biopython e R/Bioconductor
- Melhores práticas para uso de API

## Resolução de Problemas

**404 Not Found**: Entrada ou banco de dados não existe; verifique IDs e códigos de organismo
**400 Bad Request**: Erro de sintaxe na chamada de API; verifique formatação de parâmetros
**Resultados vazios**: Termo de pesquisa pode não corresponder a entradas; tente palavras-chave mais amplas
**Erros de imagem/KGML**: Estes formatos funcionam apenas com uma única entrada; remova processamento em lote

## Ferramentas Adicionais

Para visualização interativa de vias e anotação:
- **KEGG Mapper**: https://www.kegg.jp/kegg/mapper/
- **BlastKOALA**: Anotação automática de genoma
- **GhostKOALA**: Anotação de metagenoma/metatranscriptoma