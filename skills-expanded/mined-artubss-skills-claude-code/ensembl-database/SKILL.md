---
name: ensembl-database
description: "Consulte a API REST do banco de dados de genoma Ensembl para 250+ espécies. Buscas de genes, recuperação de sequências, análise de variantes, genômica comparativa, ortólogos, previsões VEP, para pesquisa genômica."
---

# Banco de Dados Ensembl

## Visão Geral

Acesse e consulte o banco de dados de genoma Ensembl, um recurso abrangente de dados genômicos de vertebrados mantido pelo EMBL-EBI. O banco de dados fornece anotações de genes, sequências, variantes, informações regulatórias e dados de genômica comparativa para mais de 250 espécies. A versão atual é 115 (setembro de 2025).

## Quando Usar esta Habilidade

Esta habilidade deve ser usada quando:

- Consultar informações de genes por símbolo ou ID Ensembl
- Recuperar sequências de DNA, transcrito ou proteína
- Analisar variantes genéticas usando o Variant Effect Predictor (VEP)
- Encontrar ortólogos e parálogos entre espécies
- Acessar features regulatórios e anotações genômicas
- Converter coordenadas entre montagens de genoma (ex.: GRCh37 para GRCh38)
- Realizar análises de genômica comparativa
- Integrar dados Ensembl em pipelines de pesquisa genômica

## Capacidades Principais

### 1. Recuperação de Informações de Genes

Consulte dados de genes por símbolo, ID Ensembl ou identificadores de bancos de dados externos.

**Operações comuns:**
- Procurar informações de genes por símbolo (ex.: "BRCA2", "TP53")
- Recuperar informações de transcrito e proteína
- Obter coordenadas de genes e localizações cromossômicas
- Acessar referências cruzadas a bancos de dados externos (UniProt, RefSeq, etc.)

**Usando o pacote ensembl_rest:**
```python
from ensembl_rest import EnsemblClient

client = EnsemblClient()

# Procurar gene por símbolo
gene_data = client.symbol_lookup(
    species='human',
    symbol='BRCA2'
)

# Obter informações detalhadas do gene
gene_info = client.lookup_id(
    id='ENSG00000139618',  # ID Ensembl BRCA2
    expand=True
)
```

**API REST direta (sem pacote):**
```python
import requests

server = "https://rest.ensembl.org"

# Busca por símbolo
response = requests.get(
    f"{server}/lookup/symbol/homo_sapiens/BRCA2",
    headers={"Content-Type": "application/json"}
)
gene_data = response.json()
```

### 2. Recuperação de Sequências

Busque sequências genômicas, de transcrito ou proteína em vários formatos (JSON, FASTA, texto simples).

**Operações:**
- Obter sequências de DNA para genes ou regiões genômicas
- Recuperar sequências de transcrito (cDNA)
- Acessar sequências de proteína
- Extrair sequências com regiões flanqueadoras ou modificações

**Exemplo:**
```python
# Usando o pacote ensembl_rest
sequence = client.sequence_id(
    id='ENSG00000139618',  # ID do gene
    content_type='application/json'
)

# Obter sequência para uma região genômica
region_seq = client.sequence_region(
    species='human',
    region='7:140424943-140624564'  # cromossomo:início-fim
)
```

### 3. Análise de Variantes

Consulte dados de variação genética e preveja consequências de variantes usando o Variant Effect Predictor (VEP).

**Capacidades:**
- Procurar variantes por rsID ou coordenadas genômicas
- Prever consequências funcionais de variantes
- Acessar dados de frequência populacional
- Recuperar associações de fenótipo

**Exemplo VEP:**
```python
# Prever consequências de variantes
vep_result = client.vep_hgvs(
    species='human',
    hgvs_notation='ENST00000380152.7:c.803C>T'
)

# Consultar variante por rsID
variant = client.variation_id(
    species='human',
    id='rs699'
)
```

### 4. Genômica Comparativa

Realize comparações entre espécies para identificar ortólogos, parálogos e relações evolutivas.

**Operações:**
- Encontrar ortólogos (mesmo gene em diferentes espécies)
- Identificar parálogos (genes relacionados na mesma espécie)
- Acessar árvores de genes mostrando relações evolutivas
- Recuperar informações de famílias de genes

**Exemplo:**
```python
# Encontrar ortólogos para um gene humano
orthologs = client.homology_ensemblgene(
    id='ENSG00000139618',  # BRCA2 humano
    target_species='mouse'
)

# Obter árvore de genes
gene_tree = client.genetree_member_symbol(
    species='human',
    symbol='BRCA2'
)
```

### 5. Análise de Região Genômica

Encontre todos os features genômicos (genes, transcritos, elementos regulatórios) em uma região específica.

**Casos de uso:**
- Identificar todos os genes em uma região cromossômica
- Encontrar features regulatórios (promotores, enhancers)
- Localizar variantes dentro de uma região
- Recuperar features estruturais

**Exemplo:**
```python
# Encontrar todos os features em uma região
features = client.overlap_region(
    species='human',
    region='7:140424943-140624564',
    feature='gene'
)
```

### 6. Mapeamento de Montagem

Converta coordenadas entre diferentes montagens de genoma (ex.: GRCh37 para GRCh38).

**Importante:** Use `https://grch37.rest.ensembl.org` para consultas GRCh37/hg19 e `https://rest.ensembl.org` para montagens atuais.

**Exemplo:**
```python
from ensembl_rest import AssemblyMapper

# Mapear coordenadas de GRCh37 para GRCh38
mapper = AssemblyMapper(
    species='human',
    asm_from='GRCh37',
    asm_to='GRCh38'
)

mapped = mapper.map(chrom='7', start=140453136, end=140453136)
```

## Práticas Recomendadas da API

### Limite de Taxa

A API REST Ensembl tem limites de taxa. Siga estas práticas:

1. **Respeite os limites de taxa:** Máximo de 15 requisições por segundo para usuários anônimos
2. **Manipule respostas 429:** Quando limitado por taxa, verifique o header `Retry-After` e aguarde
3. **Use endpoints em lote:** Ao consultar vários itens, use endpoints em lote quando disponível
4. **Armazene em cache:** Armazene dados frequentemente acessados para reduzir chamadas de API

### Tratamento de Erros

Sempre implemente tratamento de erros apropriado:

```python
import requests
import time

def query_ensembl(endpoint, params=None, max_retries=3):
    server = "https://rest.ensembl.org"
    headers = {"Content-Type": "application/json"}

    for attempt in range(max_retries):
        response = requests.get(
            f"{server}{endpoint}",
            headers=headers,
            params=params
        )

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            # Limitado por taxa - aguarde e tente novamente
            retry_after = int(response.headers.get('Retry-After', 1))
            time.sleep(retry_after)
        else:
            response.raise_for_status()

    raise Exception(f"Falhou após {max_retries} tentativas")
```

## Instalação

### Pacote Python (Recomendado)

```bash
uv pip install ensembl_rest
```

O pacote `ensembl_rest` fornece uma interface Pythônica para todos os endpoints da API REST Ensembl.

### API REST Direta

Nenhuma instalação necessária - use bibliotecas HTTP padrão como `requests`:

```bash
uv pip install requests
```

## Recursos

### references/

- `api_endpoints.md`: Documentação abrangente de todas as 17 categorias de endpoints da API com exemplos e parâmetros

### scripts/

- `ensembl_query.py`: Script Python reutilizável para consultas Ensembl comuns com limite de taxa e tratamento de erros integrados

## Fluxos de Trabalho Comuns

### Fluxo de Trabalho 1: Pipeline de Anotação de Genes

1. Procurar gene por símbolo para obter ID Ensembl
2. Recuperar informações de transcrito
3. Obter sequências de proteína para todos os transcritos
4. Encontrar ortólogos em outras espécies
5. Exportar resultados

### Fluxo de Trabalho 2: Análise de Variantes

1. Consultar variante por rsID ou coordenadas
2. Usar VEP para prever consequências funcionais
3. Verificar frequências populacionais
4. Recuperar associações de fenótipo
5. Gerar relatório

### Fluxo de Trabalho 3: Análise Comparativa

1. Começar com gene de interesse em espécie de referência
2. Encontrar ortólogos em espécie alvo
3. Recuperar sequências para todos os ortólogos
4. Comparar estruturas e features de genes
5. Analisar conservação evolutiva

## Informações de Espécies e Montagem

Para consultar espécies e montagens disponíveis:

```python
# Listar todas as espécies disponíveis
species_list = client.info_species()

# Obter informações de montagem para uma espécie
assembly_info = client.info_assembly(species='human')
```

Identificadores de espécies comuns:
- Humano: `homo_sapiens` ou `human`
- Camundongo: `mus_musculus` ou `mouse`
- Peixe-zebra: `danio_rerio` ou `zebrafish`
- Mosca-da-fruta: `drosophila_melanogaster`

## Recursos Adicionais

- **Documentação Oficial:** https://rest.ensembl.org/documentation
- **Documentação do Pacote Python:** https://ensemblrest.readthedocs.io
- **Treinamento EBI:** https://www.ebi.ac.uk/training/online/courses/ensembl-rest-api/
- **Navegador Ensembl:** https://useast.ensembl.org
- **Exemplos no GitHub:** https://github.com/Ensembl/ensembl-rest/wiki