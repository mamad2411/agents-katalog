---
name: chembl-database
description: "Consulte moléculas bioativas e dados de descoberta de fármacos do ChEMBL. Busque compostos por estrutura/propriedades, recupere dados de bioatividade (IC50, Ki), encontre inibidores, realize estudos de SAR, para química medicinal."
---

# Banco de Dados ChEMBL

## Visão Geral

ChEMBL é um banco de dados curado manualmente de moléculas bioativas mantido pelo European Bioinformatics Institute (EBI), contendo mais de 2 milhões de compostos, 19 milhões de medições de bioatividade, mais de 13.000 alvos de drogas, e dados sobre fármacos aprovados e candidatos em ensaios clínicos. Acesse e consulte esses dados programaticamente usando o cliente Python do ChEMBL para pesquisa em descoberta de fármacos e química medicinal.

## Quando Usar Esta Habilidade

Esta habilidade deve ser usada quando:

- **Buscas de compostos**: Encontrar moléculas por nome, estrutura ou propriedades
- **Informações de alvo**: Recuperar dados sobre proteínas, enzimas ou alvos biológicos
- **Dados de bioatividade**: Consultar medições IC50, Ki, EC50 ou outras atividades
- **Informações sobre fármacos**: Procurar fármacos aprovados, mecanismos ou indicações
- **Buscas de estrutura**: Realizar buscas de similaridade ou subestrutura
- **Quiminformática**: Analisar propriedades moleculares e aptidão para fármacos
- **Relações alvo-ligante**: Explorar interações composto-alvo
- **Descoberta de fármacos**: Identificar inibidores, agonistas ou moléculas bioativas

## Instalação e Configuração

### Cliente Python

O cliente Python do ChEMBL é necessário para acesso programático:

```bash
uv pip install chembl_webresource_client
```

### Padrão de Uso Básico

```python
from chembl_webresource_client.new_client import new_client

# Acesse diferentes endpoints
molecule = new_client.molecule
target = new_client.target
activity = new_client.activity
drug = new_client.drug
```

## Capacidades Principais

### 1. Consultas de Moléculas

**Recuperar por ID ChEMBL:**
```python
molecule = new_client.molecule
aspirin = molecule.get('CHEMBL25')
```

**Buscar por nome:**
```python
results = molecule.filter(pref_name__icontains='aspirin')
```

**Filtrar por propriedades:**
```python
# Encontre moléculas pequenas (MW <= 500) com LogP favorável
results = molecule.filter(
    molecule_properties__mw_freebase__lte=500,
    molecule_properties__alogp__lte=5
)
```

### 2. Consultas de Alvo

**Recuperar informações de alvo:**
```python
target = new_client.target
egfr = target.get('CHEMBL203')
```

**Buscar tipos de alvo específicos:**
```python
# Encontre todos os alvos de quinase
kinases = target.filter(
    target_type='SINGLE PROTEIN',
    pref_name__icontains='kinase'
)
```

### 3. Dados de Bioatividade

**Consultar atividades para um alvo:**
```python
activity = new_client.activity
# Encontre inibidores potentes de EGFR
results = activity.filter(
    target_chembl_id='CHEMBL203',
    standard_type='IC50',
    standard_value__lte=100,
    standard_units='nM'
)
```

**Obter todas as atividades para um composto:**
```python
compound_activities = activity.filter(
    molecule_chembl_id='CHEMBL25',
    pchembl_value__isnull=False
)
```

### 4. Buscas Baseadas em Estrutura

**Busca de similaridade:**
```python
similarity = new_client.similarity
# Encontre compostos semelhantes à aspirina
similar = similarity.filter(
    smiles='CC(=O)Oc1ccccc1C(=O)O',
    similarity=85  # Limiar de similaridade de 85%
)
```

**Busca de subestrutura:**
```python
substructure = new_client.substructure
# Encontre compostos contendo anel benzênico
results = substructure.filter(smiles='c1ccccc1')
```

### 5. Informações sobre Fármacos

**Recuperar dados de fármaco:**
```python
drug = new_client.drug
drug_info = drug.get('CHEMBL25')
```

**Obter mecanismos de ação:**
```python
mechanism = new_client.mechanism
mechanisms = mechanism.filter(molecule_chembl_id='CHEMBL25')
```

**Consultar indicações de fármaco:**
```python
drug_indication = new_client.drug_indication
indications = drug_indication.filter(molecule_chembl_id='CHEMBL25')
```

## Workflow de Consulta

### Workflow 1: Encontrando Inibidores para um Alvo

1. **Identifique o alvo** buscando por nome:
   ```python
   targets = new_client.target.filter(pref_name__icontains='EGFR')
   target_id = targets[0]['target_chembl_id']
   ```

2. **Consulte dados de bioatividade** para esse alvo:
   ```python
   activities = new_client.activity.filter(
       target_chembl_id=target_id,
       standard_type='IC50',
       standard_value__lte=100
   )
   ```

3. **Extraia IDs de compostos** e recupere detalhes:
   ```python
   compound_ids = [act['molecule_chembl_id'] for act in activities]
   compounds = [new_client.molecule.get(cid) for cid in compound_ids]
   ```

### Workflow 2: Analisando um Fármaco Conhecido

1. **Obtenha informações do fármaco**:
   ```python
   drug_info = new_client.drug.get('CHEMBL1234')
   ```

2. **Recupere mecanismos**:
   ```python
   mechanisms = new_client.mechanism.filter(molecule_chembl_id='CHEMBL1234')
   ```

3. **Encontre todas as bioatividades**:
   ```python
   activities = new_client.activity.filter(molecule_chembl_id='CHEMBL1234')
   ```

### Workflow 3: Estudo de Relação Estrutura-Atividade (SAR)

1. **Encontre compostos semelhantes**:
   ```python
   similar = new_client.similarity.filter(smiles='query_smiles', similarity=80)
   ```

2. **Obtenha atividades para cada composto**:
   ```python
   for compound in similar:
       activities = new_client.activity.filter(
           molecule_chembl_id=compound['molecule_chembl_id']
       )
   ```

3. **Analise relações propriedade-atividade** usando propriedades moleculares dos resultados.

## Operadores de Filtro

ChEMBL suporta filtros de consulta no estilo Django:

- `__exact` - Correspondência exata
- `__iexact` - Correspondência exata case-insensitive
- `__contains` / `__icontains` - Correspondência de substring
- `__startswith` / `__endswith` - Correspondência de prefixo/sufixo
- `__gt`, `__gte`, `__lt`, `__lte` - Comparações numéricas
- `__range` - Valor em intervalo
- `__in` - Valor em lista
- `__isnull` - Verificação nulo/não nulo

## Exportação e Análise de Dados

Converta resultados para DataFrame do pandas para análise:

```python
import pandas as pd

activities = new_client.activity.filter(target_chembl_id='CHEMBL203')
df = pd.DataFrame(list(activities))

# Analise resultados
print(df['standard_value'].describe())
print(df.groupby('standard_type').size())
```

## Otimização de Desempenho

### Cache

O cliente automaticamente armazena resultados em cache por 24 horas. Configure o cache:

```python
from chembl_webresource_client.settings import Settings

# Desabilite o cache
Settings.Instance().CACHING = False

# Ajuste expiração do cache (segundos)
Settings.Instance().CACHE_EXPIRE = 86400
```

### Avaliação Lazy

Consultas executam apenas quando os dados são acessados. Converta para lista para forçar execução:

```python
# Consulta ainda não foi executada
results = molecule.filter(pref_name__icontains='aspirin')

# Force execução
results_list = list(results)
```

### Paginação

Resultados são automaticamente paginados. Itere através de todos os resultados:

```python
for activity in new_client.activity.filter(target_chembl_id='CHEMBL203'):
    # Processe cada atividade
    print(activity['molecule_chembl_id'])
```

## Casos de Uso Comuns

### Encontrar Inibidores de Quinase

```python
# Identifique alvos de quinase
kinases = new_client.target.filter(
    target_type='SINGLE PROTEIN',
    pref_name__icontains='kinase'
)

# Obtenha inibidores potentes
for kinase in kinases[:5]:  # Primeiras 5 quinases
    activities = new_client.activity.filter(
        target_chembl_id=kinase['target_chembl_id'],
        standard_type='IC50',
        standard_value__lte=50
    )
```

### Explorar Reposicionamento de Fármacos

```python
# Obtenha fármacos aprovados
drugs = new_client.drug.filter()

# Para cada fármaco, encontre todos os alvos
for drug in drugs[:10]:
    mechanisms = new_client.mechanism.filter(
        molecule_chembl_id=drug['molecule_chembl_id']
    )
```

### Triagem Virtual

```python
# Encontre compostos com propriedades desejadas
candidates = new_client.molecule.filter(
    molecule_properties__mw_freebase__range=[300, 500],
    molecule_properties__alogp__lte=5,
    molecule_properties__hba__lte=10,
    molecule_properties__hbd__lte=5
)
```

## Recursos

### scripts/example_queries.py

Funções Python prontas para uso demonstrando padrões comuns de consulta ao ChEMBL:

- `get_molecule_info()` - Recupere detalhes de molécula por ID
- `search_molecules_by_name()` - Busca de molécula baseada em nome
- `find_molecules_by_properties()` - Filtragem baseada em propriedades
- `get_bioactivity_data()` - Consulte bioatividades para alvos
- `find_similar_compounds()` - Busca de similaridade
- `substructure_search()` - Correspondência de subestrutura
- `get_drug_info()` - Recupere informações de fármaco
- `find_kinase_inhibitors()` - Busca especializada de inibidores de quinase
- `export_to_dataframe()` - Converta resultados para DataFrame do pandas

Consulte este script para detalhes de implementação e exemplos de uso.

### references/api_reference.md

Documentação abrangente de API incluindo:

- Listagem completa de endpoints (molecule, target, activity, assay, drug, etc.)
- Todos os operadores de filtro e padrões de consulta
- Propriedades moleculares e campos de bioatividade
- Exemplos avançados de consulta
- Configuração e otimização de desempenho
- Tratamento de erros e rate limiting

Consulte este documento quando informações detalhadas de API forem necessárias ou ao solucionar problemas com consultas.

## Notas Importantes

### Confiabilidade de Dados

- Dados do ChEMBL são curados manualmente, mas podem conter inconsistências
- Sempre verifique o campo `data_validity_comment` em registros de atividade
- Esteja atento a flags `potential_duplicate`

### Unidades e Padrões

- Valores de bioatividade usam unidades padrão (nM, uM, etc.)
- `pchembl_value` fornece atividade normalizada (escala -log)
- Verifique `standard_type` para entender o tipo de medição (IC50, Ki, EC50, etc.)

### Rate Limiting

- Respeite as políticas de uso justo do ChEMBL
- Use cache para minimizar requisições repetidas
- Considere downloads em massa para grandes conjuntos de dados
- Evite sobrecarregar a API com requisições sucessivas rápidas

### Formatos de Estrutura Química

- Strings SMILES são o formato de estrutura principal
- Chaves InChI disponíveis para compostos
- Imagens SVG podem ser geradas via endpoint de imagem

## Recursos Adicionais

- Website ChEMBL: https://www.ebi.ac.uk/chembl/
- Documentação de API: https://www.ebi.ac.uk/chembl/api/data/docs
- GitHub do cliente Python: https://github.com/chembl/chembl_webresource_client
- Documentação de interface: https://chembl.gitbook.io/chembl-interface-documentation/
- Notebooks de exemplo: https://github.com/chembl/notebooks