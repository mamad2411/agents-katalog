---
name: pdb-database
description: "Acesso ao RCSB PDB para estruturas 3D de proteínas/ácidos nucléicos. Busque por texto/sequência/estrutura, baixe coordenadas (PDB/mmCIF), recupere metadados, para biologia estrutural e descoberta de fármacos."
---

# Banco de Dados PDB

## Visão Geral

RCSB PDB é o repositório mundial de dados estruturais 3D de macromoléculas biológicas. Busque estruturas, recupere coordenadas e metadados, realize buscas de similaridade por sequência e estrutura em mais de 200.000 estruturas determinadas experimentalmente e modelos computacionais.

## Quando Usar Este Skill

Este skill deve ser usado quando:
- Buscar estruturas 3D de proteínas ou ácidos nucléicos por texto, sequência ou similaridade estrutural
- Baixar arquivos de coordenadas nos formatos PDB, mmCIF ou BinaryCIF
- Recuperar metadados estruturais, métodos experimentais ou métricas de qualidade
- Realizar operações em lote em múltiplas estruturas
- Integrar dados PDB em workflows computacionais para descoberta de fármacos, engenharia de proteínas ou pesquisa em biologia estrutural

## Capacidades Principais

### 1. Buscando Estruturas

Encontre entradas PDB usando vários critérios de busca:

**Busca por Texto:** Busque por nome de proteína, palavras-chave ou descrições
```python
from rcsbapi.search import TextQuery
query = TextQuery("hemoglobin")
results = list(query())
print(f"Found {len(results)} structures")
```

**Busca por Atributo:** Consulte propriedades específicas (organismo, resolução, método, etc.)
```python
from rcsbapi.search import AttributeQuery
from rcsbapi.search.attrs import rcsb_entity_source_organism

# Find human protein structures
query = AttributeQuery(
    attribute=rcsb_entity_source_organism.scientific_name,
    operator="exact_match",
    value="Homo sapiens"
)
results = list(query())
```

**Similaridade de Sequência:** Encontre estruturas semelhantes a uma sequência dada
```python
from rcsbapi.search import SequenceQuery

query = SequenceQuery(
    value="MTEYKLVVVGAGGVGKSALTIQLIQNHFVDEYDPTIEDSYRKQVVIDGETCLLDILDTAGQEEYSAMRDQYMRTGEGFLCVFAINNTKSFEDIHHYREQIKRVKDSEDVPMVLVGNKCDLPSRTVDTKQAQDLARSYGIPFIETSAKTRQGVDDAFYTLVREIRKHKEKMSKDGKKKKKKSKTKCVIM",
    evalue_cutoff=0.1,
    identity_cutoff=0.9
)
results = list(query())
```

**Similaridade Estrutural:** Encontre estruturas com geometria 3D similar
```python
from rcsbapi.search import StructSimilarityQuery

query = StructSimilarityQuery(
    structure_search_type="entry",
    entry_id="4HHB"  # Hemoglobin
)
results = list(query())
```

**Combinando Consultas:** Use operadores lógicos para construir buscas complexas
```python
from rcsbapi.search import TextQuery, AttributeQuery
from rcsbapi.search.attrs import rcsb_entry_info

# High-resolution human proteins
query1 = AttributeQuery(
    attribute=rcsb_entity_source_organism.scientific_name,
    operator="exact_match",
    value="Homo sapiens"
)
query2 = AttributeQuery(
    attribute=rcsb_entry_info.resolution_combined,
    operator="less",
    value=2.0
)
combined_query = query1 & query2  # AND operation
results = list(combined_query())
```

### 2. Recuperando Dados de Estrutura

Acesse informações detalhadas sobre entradas PDB específicas:

**Informações Básicas da Entrada:**
```python
from rcsbapi.data import Schema, fetch

# Get entry-level data
entry_data = fetch("4HHB", schema=Schema.ENTRY)
print(entry_data["struct"]["title"])
print(entry_data["exptl"][0]["method"])
```

**Informações de Entidade Polimérica:**
```python
# Get protein/nucleic acid information
entity_data = fetch("4HHB_1", schema=Schema.POLYMER_ENTITY)
print(entity_data["entity_poly"]["pdbx_seq_one_letter_code"])
```

**Usando GraphQL para Consultas Flexíveis:**
```python
from rcsbapi.data import fetch

# Custom GraphQL query
query = """
{
  entry(entry_id: "4HHB") {
    struct {
      title
    }
    exptl {
      method
    }
    rcsb_entry_info {
      resolution_combined
      deposited_atom_count
    }
  }
}
"""
data = fetch(query_type="graphql", query=query)
```

### 3. Baixando Arquivos de Estrutura

Recupere arquivos de coordenadas em vários formatos:

**Métodos de Download:**
- **Formato PDB** (formato texto legado): `https://files.rcsb.org/download/{PDB_ID}.pdb`
- **Formato mmCIF** (padrão moderno): `https://files.rcsb.org/download/{PDB_ID}.cif`
- **BinaryCIF** (binário comprimido): Use a API ModelServer para acesso eficiente
- **Montagem biológica**: `https://files.rcsb.org/download/{PDB_ID}.pdb1` (para a montagem 1)

**Exemplo de Download:**
```python
import requests

pdb_id = "4HHB"

# Download PDB format
pdb_url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
response = requests.get(pdb_url)
with open(f"{pdb_id}.pdb", "w") as f:
    f.write(response.text)

# Download mmCIF format
cif_url = f"https://files.rcsb.org/download/{pdb_id}.cif"
response = requests.get(cif_url)
with open(f"{pdb_id}.cif", "w") as f:
    f.write(response.text)
```

### 4. Trabalhando com Dados de Estrutura

Operações comuns com arquivos recuperados:

**Analisar e Processar Coordenadas:**
Use BioPython ou outras bibliotecas de biologia estrutural para trabalhar com arquivos baixados:
```python
from Bio.PDB import PDBParser

parser = PDBParser()
structure = parser.get_structure("protein", "4HHB.pdb")

# Iterate through atoms
for model in structure:
    for chain in model:
        for residue in chain:
            for atom in residue:
                print(atom.get_coord())
```

**Extrair Metadados:**
```python
from rcsbapi.data import fetch, Schema

# Get experimental details
data = fetch("4HHB", schema=Schema.ENTRY)

resolution = data.get("rcsb_entry_info", {}).get("resolution_combined")
method = data.get("exptl", [{}])[0].get("method")
deposition_date = data.get("rcsb_accession_info", {}).get("deposit_date")

print(f"Resolution: {resolution} Å")
print(f"Method: {method}")
print(f"Deposited: {deposition_date}")
```

### 5. Operações em Lote

Processe múltiplas estruturas com eficiência:

```python
from rcsbapi.data import fetch, Schema

pdb_ids = ["4HHB", "1MBN", "1GZX"]  # Hemoglobin, myoglobin, etc.

results = {}
for pdb_id in pdb_ids:
    try:
        data = fetch(pdb_id, schema=Schema.ENTRY)
        results[pdb_id] = {
            "title": data["struct"]["title"],
            "resolution": data.get("rcsb_entry_info", {}).get("resolution_combined"),
            "organism": data.get("rcsb_entity_source_organism", [{}])[0].get("scientific_name")
        }
    except Exception as e:
        print(f"Error fetching {pdb_id}: {e}")

# Display results
for pdb_id, info in results.items():
    print(f"\n{pdb_id}: {info['title']}")
    print(f"  Resolution: {info['resolution']} Å")
    print(f"  Organism: {info['organism']}")
```

## Instalação do Pacote Python

Instale o cliente da API Python oficial do RCSB PDB:

```bash
# Current recommended package
uv pip install rcsb-api

# For legacy code (deprecated, use rcsb-api instead)
uv pip install rcsbsearchapi
```

O pacote `rcsb-api` fornece acesso unificado às APIs Search e Data através dos módulos `rcsbapi.search` e `rcsbapi.data`.

## Casos de Uso Comuns

### Descoberta de Fármacos
- Busque estruturas de alvos para medicamentos
- Analise sítios de ligação de ligantes
- Compare complexos proteína-ligante
- Identifique bolsas de ligação similares

### Engenharia de Proteínas
- Encontre estruturas homólogas para modelagem
- Analise relações sequência-estrutura
- Compare estruturas mutantes
- Estude estabilidade e dinâmica de proteínas

### Pesquisa em Biologia Estrutural
- Baixe estruturas para análise computacional
- Construa alinhamentos baseados em estrutura
- Analise recursos estruturais (estrutura secundária, domínios)
- Compare métodos experimentais e métricas de qualidade

### Educação e Visualização
- Recupere estruturas para ensino
- Gere visualizações moleculares
- Explore relações estrutura-função
- Estude conservação evolutiva

## Conceitos-Chave

**ID PDB:** Identificador único de 4 caracteres (ex: "4HHB") para cada entrada de estrutura. Entradas de AlphaFold e ModelArchive começam com prefixos "AF_" ou "MA_".

**mmCIF/PDBx:** Formato de arquivo moderno que usa estrutura chave-valor, substituindo o formato PDB legado para estruturas grandes.

**Montagem Biológica:** A forma funcional de uma macromolécule, que pode conter múltiplas cópias de cadeias da unidade assimétrica.

**Resolução:** Medida de detalhe em estruturas cristalográficas (valores menores = maior detalhe). Intervalo típico: 1,5-3,5 Å para estruturas de alta qualidade.

**Entidade:** Um componente molecular único em uma estrutura (cadeia de proteína, DNA, ligante, etc.).

## Recursos

Este skill inclui documentação de referência no diretório `references/`:

### references/api_reference.md
Documentação abrangente da API cobrindo:
- Especificações detalhadas de endpoints da API
- Padrões de consulta avançados e exemplos
- Referência de schema de dados
- Rate limiting e melhores práticas
- Solução de problemas para problemas comuns

Use esta referência quando você precisar de informações aprofundadas sobre recursos da API, construção de consultas complexas ou informações detalhadas sobre schema de dados.

## Recursos Adicionais

- **Site RCSB PDB:** https://www.rcsb.org
- **Portal Educacional PDB-101:** https://pdb101.rcsb.org
- **Documentação da API:** https://www.rcsb.org/docs/programmatic-access/web-apis-overview
- **Docs do Pacote Python:** https://rcsbapi.readthedocs.io/
- **Documentação da Data API:** https://data.rcsb.org/
- **Repositório GitHub:** https://github.com/rcsb/py-rcsb-api