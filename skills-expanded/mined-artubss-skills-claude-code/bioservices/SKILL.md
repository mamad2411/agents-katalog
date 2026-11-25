---
name: bioservices
description: "Ferramenta Python primária para 40+ serviços de bioinformática. Preferida para workflows multi-banco de dados: UniProt, KEGG, ChEMBL, PubChem, Reactome, QuickGO. API unificada para queries, mapeamento de IDs, análise de pathways. Para controle REST direto, use skills individuais de banco de dados (uniprot-database, kegg-database)."
---

# BioServices

## Visão Geral

BioServices é um pacote Python que fornece acesso programático a aproximadamente 40 serviços web e bancos de dados de bioinformática. Recupere dados biológicos, execute queries cross-banco de dados, mapeie identificadores, analise sequências e integre múltiplos recursos biológicos em workflows Python. O pacote trata tanto protocolos REST quanto SOAP/WSDL de forma transparente.

## Quando Usar Esta Skill

Esta skill deve ser usada quando:
- Recuperar sequências de proteínas, anotações ou estruturas de UniProt, PDB, Pfam
- Analisar pathways metabólicos e funções gênicas via KEGG ou Reactome
- Buscar em bancos de dados de compostos (ChEBI, ChEMBL, PubChem) para informações químicas
- Converter identificadores entre diferentes bancos de dados biológicos (KEGG↔UniProt, IDs de compostos)
- Executar buscas de similaridade de sequências (BLAST, alinhamento MUSCLE)
- Consultar termos de gene ontology (QuickGO, anotações GO)
- Acessar dados de interações proteína-proteína (PSICQUIC, IntactComplex)
- Minerar dados genômicos (BioMart, ArrayExpress, ENA)
- Integrar dados de múltiplos recursos de bioinformática em um único workflow

## Capacidades Centrais

### 1. Análise de Proteínas

Recupere informações de proteínas, sequências e anotações funcionais:

```python
from bioservices import UniProt

u = UniProt(verbose=False)

# Search for protein by name
results = u.search("ZAP70_HUMAN", frmt="tab", columns="id,genes,organism")

# Retrieve FASTA sequence
sequence = u.retrieve("P43403", "fasta")

# Map identifiers between databases
kegg_ids = u.mapping(fr="UniProtKB_AC-ID", to="KEGG", query="P43403")
```

**Métodos-chave:**
- `search()`: Consulta UniProt com termos de busca flexíveis
- `retrieve()`: Obtenha entradas de proteínas em vários formatos (FASTA, XML, tab)
- `mapping()`: Converta identificadores entre bancos de dados

Referência: `references/services_reference.md` para detalhes completos da API UniProt.

### 2. Descoberta e Análise de Pathways

Acesse informações de pathways KEGG para genes e organismos:

```python
from bioservices import KEGG

k = KEGG()
k.organism = "hsa"  # Set to human

# Search for organisms
k.lookfor_organism("droso")  # Find Drosophila species

# Find pathways by name
k.lookfor_pathway("B cell")  # Returns matching pathway IDs

# Get pathways containing specific genes
pathways = k.get_pathway_by_gene("7535", "hsa")  # ZAP70 gene

# Retrieve and parse pathway data
data = k.get("hsa04660")
parsed = k.parse(data)

# Extract pathway interactions
interactions = k.parse_kgml_pathway("hsa04660")
relations = interactions['relations']  # Protein-protein interactions

# Convert to Simple Interaction Format
sif_data = k.pathway2sif("hsa04660")
```

**Métodos-chave:**
- `lookfor_organism()`, `lookfor_pathway()`: Busque por nome
- `get_pathway_by_gene()`: Encontre pathways contendo genes
- `parse_kgml_pathway()`: Extraia dados estruturados de pathway
- `pathway2sif()`: Obtenha redes de interação proteica

Referência: `references/workflow_patterns.md` para workflows completos de análise de pathways.

### 3. Buscas em Bancos de Dados de Compostos

Busque e faça referência cruzada de compostos em múltiplos bancos de dados:

```python
from bioservices import KEGG, UniChem

k = KEGG()

# Search compounds by name
results = k.find("compound", "Geldanamycin")  # Returns cpd:C11222

# Get compound information with database links
compound_info = k.get("cpd:C11222")  # Includes ChEBI links

# Cross-reference KEGG → ChEMBL using UniChem
u = UniChem()
chembl_id = u.get_compound_id_from_kegg("C11222")  # Returns CHEMBL278315
```

**Workflow comum:**
1. Busque composto por nome em KEGG
2. Extraia ID de composto KEGG
3. Use UniChem para mapeamento KEGG → ChEMBL
4. IDs ChEBI geralmente estão fornecidos em entradas KEGG

Referência: `references/identifier_mapping.md` para guia completo de mapeamento cross-banco de dados.

### 4. Análise de Sequências

Execute buscas BLAST e alinhamentos de sequências:

```python
from bioservices import NCBIblast

s = NCBIblast(verbose=False)

# Run BLASTP against UniProtKB
jobid = s.run(
    program="blastp",
    sequence=protein_sequence,
    stype="protein",
    database="uniprotkb",
    email="your.email@example.com"  # Required by NCBI
)

# Check job status and retrieve results
s.getStatus(jobid)
results = s.getResult(jobid, "out")
```

**Nota:** Tarefas BLAST são assíncronas. Verifique o status antes de recuperar resultados.

### 5. Mapeamento de Identificadores

Converta identificadores entre diferentes bancos de dados biológicos:

```python
from bioservices import UniProt, KEGG

# UniProt mapping (many database pairs supported)
u = UniProt()
results = u.mapping(
    fr="UniProtKB_AC-ID",  # Source database
    to="KEGG",              # Target database
    query="P43403"          # Identifier(s) to convert
)

# KEGG gene ID → UniProt
kegg_to_uniprot = u.mapping(fr="KEGG", to="UniProtKB_AC-ID", query="hsa:7535")

# For compounds, use UniChem
from bioservices import UniChem
u = UniChem()
chembl_from_kegg = u.get_compound_id_from_kegg("C11222")
```

**Mapeamentos suportados (UniProt):**
- UniProtKB ↔ KEGG
- UniProtKB ↔ Ensembl
- UniProtKB ↔ PDB
- UniProtKB ↔ RefSeq
- E muitos outros (veja `references/identifier_mapping.md`)

### 6. Consultas de Gene Ontology

Acesse termos GO e anotações:

```python
from bioservices import QuickGO

g = QuickGO(verbose=False)

# Retrieve GO term information
term_info = g.Term("GO:0003824", frmt="obo")

# Search annotations
annotations = g.Annotation(protein="P43403", format="tsv")
```

### 7. Interações Proteína-Proteína

Consulte bancos de dados de interação via PSICQUIC:

```python
from bioservices import PSICQUIC

s = PSICQUIC(verbose=False)

# Query specific database (e.g., MINT)
interactions = s.query("mint", "ZAP70 AND species:9606")

# List available interaction databases
databases = s.activeDBs
```

**Bancos de dados disponíveis:** MINT, IntAct, BioGRID, DIP e 30+ outros.

## Workflows de Integração Multi-Serviço

BioServices se destaca na combinação de múltiplos serviços para análise abrangente. Padrões comuns de integração:

### Pipeline Completo de Análise de Proteínas

Execute um workflow completo de caracterização de proteína:

```bash
python scripts/protein_analysis_workflow.py ZAP70_HUMAN your.email@example.com
```

Este script demonstra:
1. Busca UniProt por entrada de proteína
2. Recuperação de sequência FASTA
3. Busca de similaridade BLAST
4. Descoberta de pathway KEGG
5. Mapeamento de interações PSICQUIC

### Análise de Rede de Pathways

Analise todos os pathways de um organismo:

```bash
python scripts/pathway_analysis.py hsa output_directory/
```

Extrai e analisa:
- Todos os IDs de pathway para organismo
- Interações proteína-proteína por pathway
- Distribuições de tipo de interação
- Exporta para formatos CSV/SIF

### Busca de Composto Cross-Banco de Dados

Mapeie identificadores de compostos entre bancos de dados:

```bash
python scripts/compound_cross_reference.py Geldanamycin
```

Recupera:
- ID de composto KEGG
- Identificador ChEBI
- Identificador ChEMBL
- Propriedades básicas do composto

### Conversão em Lote de Identificadores

Converta múltiplos identificadores de uma vez:

```bash
python scripts/batch_id_converter.py input_ids.txt --from UniProtKB_AC-ID --to KEGG
```

## Melhores Práticas

### Tratamento de Formato de Saída

Diferentes serviços retornam dados em vários formatos:
- **XML**: Parse usando BeautifulSoup (maioria dos serviços SOAP)
- **Tab-separated (TSV)**: DataFrames Pandas para dados tabulares
- **Dictionary/JSON**: Manipulação Python direta
- **FASTA**: Integração BioPython para análise de sequências

### Limitação de Taxa e Verbosidade

Controle comportamento de requisições de API:

```python
from bioservices import KEGG

k = KEGG(verbose=False)  # Suppress HTTP request details
k.TIMEOUT = 30  # Adjust timeout for slow connections
```

### Tratamento de Erros

Envolva chamadas de serviço em blocos try-except:

```python
try:
    results = u.search("ambiguous_query")
    if results:
        # Process results
        pass
except Exception as e:
    print(f"Search failed: {e}")
```

### Códigos de Organismos

Use abreviações padrão de organismos:
- `hsa`: Homo sapiens (humano)
- `mmu`: Mus musculus (camundongo)
- `dme`: Drosophila melanogaster
- `sce`: Saccharomyces cerevisiae (levedura)

Liste todos os organismos: `k.list("organism")` ou `k.organismIds`

### Integração com Outras Ferramentas

BioServices funciona bem com:
- **BioPython**: Análise de sequências em dados FASTA recuperados
- **Pandas**: Manipulação de dados tabulares
- **PyMOL**: Visualização de estrutura 3D (recupere IDs PDB)
- **NetworkX**: Análise de rede de interações de pathways
- **Galaxy**: Wrappers de ferramentas customizadas para plataformas de workflow

## Recursos

### scripts/

Scripts Python executáveis demonstrando workflows completos:

- `protein_analysis_workflow.py`: Caracterização de proteína end-to-end
- `pathway_analysis.py`: Descoberta de pathway KEGG e extração de rede
- `compound_cross_reference.py`: Busca de compostos multi-banco de dados
- `batch_id_converter.py`: Utilitário de mapeamento em lote de identificadores

Scripts podem ser executados diretamente ou adaptados para casos de uso específicos.

### references/

Documentação detalhada carregada conforme necessário:

- `services_reference.md`: Lista abrangente de todos os 40+ serviços com métodos
- `workflow_patterns.md`: Workflows de análise multi-etapa detalhados
- `identifier_mapping.md`: Guia completo para conversão de IDs cross-banco de dados

Carregue referências ao trabalhar com serviços específicos ou tarefas de integração complexa.

## Instalação

```bash
uv pip install bioservices
```

Dependências são gerenciadas automaticamente. Pacote é testado em Python 3.9-3.12.

## Informações Adicionais

Para documentação de API detalhada e recursos avançados, consulte:
- Documentação oficial: https://bioservices.readthedocs.io/
- Código-fonte: https://github.com/cokelaer/bioservices
- Referências específicas do serviço em `references/services_reference.md`