---
name: pubchem-database
description: "Consultar PubChem via API PUG-REST/PubChemPy (110M+ compostos). Buscar por nome/CID/SMILES, recuperar propriedades, buscas de similaridade/subestrutura, bioatividade, para quiminformática."
---

# Banco de Dados PubChem

## Visão Geral

PubChem é o maior banco de dados químico gratuito do mundo com 110M+ compostos e 270M+ bioatividades. Consulte estruturas químicas por nome, CID ou SMILES, recupere propriedades moleculares, execute buscas de similaridade e subestrutura, acesse dados de bioatividade usando API PUG-REST e PubChemPy.

## Quando Usar Esta Skill

Esta skill deve ser usada quando:
- Buscar compostos químicos por nome, estrutura (SMILES/InChI) ou fórmula molecular
- Recuperar propriedades moleculares (MW, LogP, TPSA, descritores de ligações de hidrogênio)
- Executar buscas de similaridade para encontrar compostos estruturalmente relacionados
- Conduzir buscas de subestrutura para motivos químicos específicos
- Acessar dados de bioatividade de ensaios de triagem
- Converter entre formatos de identificador químico (CID, SMILES, InChI)
- Processar em lote múltiplos compostos para triagem de similaridade com fármacos ou análise de propriedades

## Capacidades Principais

### 1. Busca de Estrutura Química

Busque compostos usando múltiplos tipos de identificadores:

**Por Nome Químico**:
```python
import pubchempy as pcp
compounds = pcp.get_compounds('aspirin', 'name')
compound = compounds[0]
```

**Por CID (ID de Composto)**:
```python
compound = pcp.Compound.from_cid(2244)  # Aspirin
```

**Por SMILES**:
```python
compound = pcp.get_compounds('CC(=O)OC1=CC=CC=C1C(=O)O', 'smiles')[0]
```

**Por InChI**:
```python
compound = pcp.get_compounds('InChI=1S/C9H8O4/...', 'inchi')[0]
```

**Por Fórmula Molecular**:
```python
compounds = pcp.get_compounds('C9H8O4', 'formula')
# Retorna todos os compostos correspondentes a esta fórmula
```

### 2. Recuperação de Propriedades

Recupere propriedades moleculares para compostos usando abordagens de alto ou baixo nível:

**Usando PubChemPy (Recomendado)**:
```python
import pubchempy as pcp

# Obtenha objeto composto com todas as propriedades
compound = pcp.get_compounds('caffeine', 'name')[0]

# Acesse propriedades individuais
molecular_formula = compound.molecular_formula
molecular_weight = compound.molecular_weight
iupac_name = compound.iupac_name
smiles = compound.canonical_smiles
inchi = compound.inchi
xlogp = compound.xlogp  # Coeficiente de partição
tpsa = compound.tpsa    # Área de superfície polar topológica
```

**Obter Propriedades Específicas**:
```python
# Solicitar apenas propriedades específicas
properties = pcp.get_properties(
    ['MolecularFormula', 'MolecularWeight', 'CanonicalSMILES', 'XLogP'],
    'aspirin',
    'name'
)
# Retorna lista de dicionários
```

**Recuperação em Lote de Propriedades**:
```python
import pandas as pd

compound_names = ['aspirin', 'ibuprofen', 'paracetamol']
all_properties = []

for name in compound_names:
    props = pcp.get_properties(
        ['MolecularFormula', 'MolecularWeight', 'XLogP'],
        name,
        'name'
    )
    all_properties.extend(props)

df = pd.DataFrame(all_properties)
```

**Propriedades Disponíveis**: MolecularFormula, MolecularWeight, CanonicalSMILES, IsomericSMILES, InChI, InChIKey, IUPACName, XLogP, TPSA, HBondDonorCount, HBondAcceptorCount, RotatableBondCount, Complexity, Charge, e muitas mais (veja `references/api_reference.md` para lista completa).

### 3. Busca de Similaridade

Encontre compostos estruturalmente similares usando similaridade Tanimoto:

```python
import pubchempy as pcp

# Comece com um composto de consulta
query_compound = pcp.get_compounds('gefitinib', 'name')[0]
query_smiles = query_compound.canonical_smiles

# Execute busca de similaridade
similar_compounds = pcp.get_compounds(
    query_smiles,
    'smiles',
    searchtype='similarity',
    Threshold=85,  # Limite de similaridade (0-100)
    MaxRecords=50
)

# Processe resultados
for compound in similar_compounds[:10]:
    print(f"CID {compound.cid}: {compound.iupac_name}")
    print(f"  MW: {compound.molecular_weight}")
```

**Nota**: Buscas de similaridade são assíncronas para consultas grandes e podem levar 15-30 segundos para serem concluídas. PubChemPy lida com o padrão assíncrono automaticamente.

### 4. Busca de Subestrutura

Encontre compostos contendo um motivo estrutural específico:

```python
import pubchempy as pcp

# Busque compostos contendo anel de piridina
pyridine_smiles = 'c1ccncc1'

matches = pcp.get_compounds(
    pyridine_smiles,
    'smiles',
    searchtype='substructure',
    MaxRecords=100
)

print(f"Encontrados {len(matches)} compostos contendo piridina")
```

**Subestruturas Comuns**:
- Anel de benzeno: `c1ccccc1`
- Piridina: `c1ccncc1`
- Fenol: `c1ccc(O)cc1`
- Ácido carboxílico: `C(=O)O`

### 5. Conversão de Formato

Converta entre diferentes formatos de estrutura química:

```python
import pubchempy as pcp

compound = pcp.get_compounds('aspirin', 'name')[0]

# Converta para diferentes formatos
smiles = compound.canonical_smiles
inchi = compound.inchi
inchikey = compound.inchikey
cid = compound.cid

# Baixe arquivos de estrutura
pcp.download('SDF', 'aspirin', 'name', 'aspirin.sdf', overwrite=True)
pcp.download('JSON', '2244', 'cid', 'aspirin.json', overwrite=True)
```

### 6. Visualização de Estrutura

Gere imagens de estrutura 2D:

```python
import pubchempy as pcp

# Baixe estrutura do composto como PNG
pcp.download('PNG', 'caffeine', 'name', 'caffeine.png', overwrite=True)

# Usando URL direto (via requests)
import requests

cid = 2244  # Aspirin
url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/PNG?image_size=large"
response = requests.get(url)

with open('structure.png', 'wb') as f:
    f.write(response.content)
```

### 7. Recuperação de Sinônimos

Obtenha todos os nomes conhecidos e sinônimos para um composto:

```python
import pubchempy as pcp

synonyms_data = pcp.get_synonyms('aspirin', 'name')

if synonyms_data:
    cid = synonyms_data[0]['CID']
    synonyms = synonyms_data[0]['Synonym']

    print(f"CID {cid} tem {len(synonyms)} sinônimos:")
    for syn in synonyms[:10]:  # Primeiros 10
        print(f"  - {syn}")
```

### 8. Acesso a Dados de Bioatividade

Recupere dados de atividade biológica de ensaios:

```python
import requests
import json

# Obtenha resumo de bioensaio para um composto
cid = 2244  # Aspirin
url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/assaysummary/JSON"

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    # Processe informações de bioensaio
    table = data.get('Table', {})
    rows = table.get('Row', [])
    print(f"Encontrados {len(rows)} registros de bioensaio")
```

**Para consultas de bioatividade mais complexas**, use o script auxiliar `scripts/bioactivity_query.py` que fornece:
- Resumos de bioensaio com filtragem de resultado de atividade
- Identificação de alvo de ensaio
- Busca de compostos por alvo biológico
- Listas de compostos ativos para ensaios específicos

### 9. Anotações Abrangentes de Composto

Acesse informações detalhadas de composto através de PUG-View:

```python
import requests

cid = 2244
url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON"

response = requests.get(url)
if response.status_code == 200:
    annotations = response.json()
    # Contém dados extensivos incluindo:
    # - Propriedades Químicas e Físicas
    # - Informações de Medicamento e Medicação
    # - Farmacologia e Bioquímica
    # - Segurança e Perigos
    # - Toxicidade
    # - Referências de literatura
    # - Patentes
```

**Obter Seção Específica**:
```python
# Obtenha apenas informações de medicamento
url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON?heading=Drug and Medication Information"
```

## Requisitos de Instalação

Instale PubChemPy para acesso baseado em Python:

```bash
uv pip install pubchempy
```

Para acesso direto de API e consultas de bioatividade:

```bash
uv pip install requests
```

Opcional para análise de dados:

```bash
uv pip install pandas
```

## Scripts Auxiliares

Esta skill inclui scripts Python para tarefas comuns do PubChem:

### scripts/compound_search.py

Fornece funções utilitárias para buscar e recuperar informações de compostos:

**Funções-Chave**:
- `search_by_name(name, max_results=10)`: Busque compostos por nome
- `search_by_smiles(smiles)`: Busque por string SMILES
- `get_compound_by_cid(cid)`: Recupere composto por CID
- `get_compound_properties(identifier, namespace, properties)`: Obtenha propriedades específicas
- `similarity_search(smiles, threshold, max_records)`: Execute busca de similaridade
- `substructure_search(smiles, max_records)`: Execute busca de subestrutura
- `get_synonyms(identifier, namespace)`: Obtenha todos os sinônimos
- `batch_search(identifiers, namespace, properties)`: Busca em lote de múltiplos compostos
- `download_structure(identifier, namespace, format, filename)`: Baixe estruturas
- `print_compound_info(compound)`: Imprima informações formatadas de composto

**Uso**:
```python
from scripts.compound_search import search_by_name, get_compound_properties

# Busque um composto
compounds = search_by_name('ibuprofen')

# Obtenha propriedades específicas
props = get_compound_properties('aspirin', 'name', ['MolecularWeight', 'XLogP'])
```

### scripts/bioactivity_query.py

Fornece funções para recuperação de dados de atividade biológica:

**Funções-Chave**:
- `get_bioassay_summary(cid)`: Obtenha resumo de bioensaio para composto
- `get_compound_bioactivities(cid, activity_outcome)`: Obtenha bioatividades filtradas
- `get_assay_description(aid)`: Obtenha informações detalhadas de ensaio
- `get_assay_targets(aid)`: Obtenha alvos biológicos para ensaio
- `search_assays_by_target(target_name, max_results)`: Encontre ensaios por alvo
- `get_active_compounds_in_assay(aid, max_results)`: Obtenha compostos ativos
- `get_compound_annotations(cid, section)`: Obtenha anotações de PUG-View
- `summarize_bioactivities(cid)`: Gere estatísticas de resumo de bioatividade
- `find_compounds_by_bioactivity(target, threshold, max_compounds)`: Encontre compostos por alvo

**Uso**:
```python
from scripts.bioactivity_query import get_bioassay_summary, summarize_bioactivities

# Obtenha resumo de bioatividade
summary = summarize_bioactivities(2244)  # Aspirin
print(f"Total de ensaios: {summary['total_assays']}")
print(f"Ativos: {summary['active']}, Inativos: {summary['inactive']}")
```

## Limites de Taxa de API e Melhores Práticas

**Limites de Taxa**:
- Máximo 5 requisições por segundo
- Máximo 400 requisições por minuto
- Máximo 300 segundos de tempo de execução por minuto

**Melhores Práticas**:
1. **Use CIDs para consultas repetidas**: CIDs são mais eficientes que nomes ou estruturas
2. **Cache de resultados localmente**: Armazene dados acessados frequentemente
3. **Batch de requisições**: Combine múltiplas consultas quando possível
4. **Implemente atrasos**: Adicione atrasos de 0,2-0,3 segundo entre requisições
5. **Trate erros graciosamente**: Verifique erros HTTP e dados ausentes
6. **Use PubChemPy**: Abstração de nível superior lida com muitos casos extremos
7. **Aproveite padrão assíncrono**: Para buscas grandes de similaridade/subestrutura
8. **Especifique MaxRecords**: Limite resultados para evitar timeouts

**Tratamento de Erros**:
```python
from pubchempy import BadRequestError, NotFoundError, TimeoutError

try:
    compound = pcp.get_compounds('query', 'name')[0]
except NotFoundError:
    print("Composto não encontrado")
except BadRequestError:
    print("Formato de requisição inválido")
except TimeoutError:
    print("Requisição expirou - tente reduzir escopo")
except IndexError:
    print("Nenhum resultado retornado")
```

## Workflows Comuns

### Workflow 1: Pipeline de Conversão de Identificador Químico

Converta entre diferentes identificadores químicos:

```python
import pubchempy as pcp

# Comece com qualquer tipo de identificador
compound = pcp.get_compounds('caffeine', 'name')[0]

# Extraia todos os formatos de identificador
identifiers = {
    'CID': compound.cid,
    'Name': compound.iupac_name,
    'SMILES': compound.canonical_smiles,
    'InChI': compound.inchi,
    'InChIKey': compound.inchikey,
    'Formula': compound.molecular_formula
}
```

### Workflow 2: Triagem de Propriedade Similar a Fármaco

Triagem de compostos usando Regra dos Cinco de Lipinski:

```python
import pubchempy as pcp

def check_drug_likeness(compound_name):
    compound = pcp.get_compounds(compound_name, 'name')[0]

    # Regra dos Cinco de Lipinski
    rules = {
        'MW <= 500': compound.molecular_weight <= 500,
        'LogP <= 5': compound.xlogp <= 5 if compound.xlogp else None,
        'HBD <= 5': compound.h_bond_donor_count <= 5,
        'HBA <= 10': compound.h_bond_acceptor_count <= 10
    }

    violations = sum(1 for v in rules.values() if v is False)
    return rules, violations

rules, violations = check_drug_likeness('aspirin')
print(f"Violações de Lipinski: {violations}")
```

### Workflow 3: Encontrando Candidatos de Fármaco Similares

Identifique compostos estruturalmente similares a um fármaco conhecido:

```python
import pubchempy as pcp

# Comece com fármaco conhecido
reference_drug = pcp.get_compounds('imatinib', 'name')[0]
reference_smiles = reference_drug.canonical_smiles

# Encontre compostos similares
similar = pcp.get_compounds(
    reference_smiles,
    'smiles',
    searchtype='similarity',
    Threshold=85,
    MaxRecords=20
)

# Filtre por propriedades similares a fármacos
candidates = []
for comp in similar:
    if comp.molecular_weight and 200 <= comp.molecular_weight <= 600:
        if comp.xlogp and -1 <= comp.xlogp <= 5:
            candidates.append(comp)

print(f"Encontrados {len(candidates)} candidatos similares a fármacos")
```

### Workflow 4: Comparação em Lote de Propriedade de Composto

Compare propriedades entre múltiplos compostos:

```python
import pubchempy as pcp
import pandas as pd

compound_list = ['aspirin', 'ibuprofen', 'naproxen', 'celecoxib']

properties_list = []
for name in compound_list:
    try:
        compound = pcp.get_compounds(name, 'name')[0]
        properties_list.append({
            'Name': name,
            'CID': compound.cid,
            'Formula': compound.molecular_formula,
            'MW': compound.molecular_weight,
            'LogP': compound.xlogp,
            'TPSA': compound.tpsa,
            'HBD': compound.h_bond_donor_count,
            'HBA': compound.h_bond_acceptor_count
        })
    except Exception as e:
        print(f"Erro ao processar {name}: {e}")

df = pd.DataFrame(properties_list)
print(df.to_string(index=False))
```

### Workflow 5: Triagem Virtual Baseada em Subestrutura

Triagem de compostos contendo farmaçóforos específicos:

```python
import pubchempy as pcp

# Defina farmaçóforo (ex: grupo sulfonamida)
pharmacophore_smiles = 'S(=O)(=O)N'

# Busque compostos contendo essa subestrutura
hits = pcp.get_compounds(
    pharmacophore_smiles,
    'smiles',
    searchtype='substructure',
    MaxRecords=100
)

# Filtre ainda mais por propriedades
filtered_hits = [
    comp for comp in hits
    if comp.molecular_weight and comp.molecular_weight < 500
]

print(f"Encontrados {len(filtered_hits)} compostos com subestrutura desejada")
```

## Documentação de Referência

Para documentação detalhada de API, incluindo listas completas de propriedades, padrões de URL, opções de consulta avançada e mais exemplos, consulte `references/api_reference.md`. Esta referência abrangente inclui:

- Documentação completa de endpoint da API PUG-REST
- Lista completa de propriedades moleculares disponíveis
- Padrões de tratamento de requisição assíncrona
- Referência da API PubChemPy
- API PUG-View para anotações
- Workflows comuns e casos de uso
- Links para documentação oficial do PubChem

## Troubleshooting

**Composto Não Encontrado**:
- Tente nomes alternativos ou sinônimos
- Use CID se conhecido
- Verifique ortografia e formato de nome químico

**Erros de Timeout**:
- Reduza parâmetro MaxRecords
- Adicione atrasos entre requisições
- Use CIDs em vez de nomes para consultas mais rápidas

**Valores de Propriedade Vazios**:
- Nem todas as propriedades estão disponíveis para todos os compostos
- Verifique se propriedade existe antes de acessar: `if compound.xlogp:`
- Algumas propriedades só disponíveis para certos tipos de compostos

**Taxa Limite Excedida**:
- Implemente atrasos (0,2-0,3 segundos) entre requisições
- Use operações em lote quando possível
- Considere fazer cache de resultados localmente

**Busca de Similaridade/Subestrutura Trava**:
- Estas são operações assíncronas que podem levar 15-30 segundos
- PubChemPy lida com polling automaticamente
- Reduza MaxRecords se expirar timeout

## Recursos Adicionais

- PubChem Home: https://pubchem.ncbi.nlm.nih.gov/
- Documentação PUG-REST: https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest
- Tutorial PUG-REST: https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest-tutorial
- Documentação PubChemPy: https://pubchempy.readthedocs.io/
- GitHub PubChemPy: https://github.com/mcs07/PubChemPy