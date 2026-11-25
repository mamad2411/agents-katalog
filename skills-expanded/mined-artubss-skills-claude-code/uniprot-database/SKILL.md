---
name: uniprot-database
description: "Acesso direto à API REST do UniProt. Buscas de proteínas, recuperação FASTA, mapeamento de IDs, Swiss-Prot/TrEMBL. Para workflows Python com múltiplos bancos de dados, prefira bioservices (interface unificada para 40+ serviços). Use isto para trabalho HTTP/REST direto ou controle específico do UniProt."
---

# Banco de Dados UniProt

## Visão Geral

UniProt é o principal recurso abrangente do mundo para sequências de proteínas e informações funcionais. Busque proteínas por nome, gene ou acesso, recupere sequências em formato FASTA, execute mapeamento de IDs entre bancos de dados, acesse anotações Swiss-Prot/TrEMBL via API REST para análise de proteínas.

## Quando Usar Esta Skill

Esta skill deve ser usada quando:
- Procurar por entradas de proteínas por nome, símbolo de gene, acesso ou organismo
- Recuperar sequências de proteínas em FASTA ou outros formatos
- Mapear identificadores entre UniProt e bancos de dados externos (Ensembl, RefSeq, PDB, etc.)
- Acessar anotações de proteínas incluindo termos GO, domínios e descrições funcionais
- Recuperar em lote múltiplas entradas de proteínas eficientemente
- Consultar dados de proteínas revisadas (Swiss-Prot) versus não revisadas (TrEMBL)
- Fazer streaming de grandes conjuntos de dados de proteínas
- Construir consultas personalizadas com sintaxe de busca específica por campo

## Capacidades Principais

### 1. Buscar Proteínas

Busque no UniProt usando consultas em linguagem natural ou sintaxe de busca estruturada.

**Padrões de busca comuns:**
```python
# Buscar por nome de proteína
query = "insulin AND organism_name:\"Homo sapiens\""

# Buscar por nome de gene
query = "gene:BRCA1 AND reviewed:true"

# Buscar por acesso
query = "accession:P12345"

# Buscar por comprimento de sequência
query = "length:[100 TO 500]"

# Buscar por taxonomia
query = "taxonomy_id:9606"  # Proteínas humanas

# Buscar por termo GO
query = "go:0005515"  # Ligação de proteína
```

Use o endpoint de busca da API: `https://rest.uniprot.org/uniprotkb/search?query={query}&format={format}`

**Formatos suportados:** JSON, TSV, Excel, XML, FASTA, RDF, TXT

### 2. Recuperar Entradas Individuais de Proteínas

Recupere entradas de proteínas específicas pelo número de acesso.

**Formatos de número de acesso:**
- Clássico: P12345, Q1AAA9, O15530 (6 caracteres: letra + 5 alfanuméricos)
- Estendido: A0A022YWF9 (10 caracteres para entradas mais recentes)

**Endpoint de recuperação:** `https://rest.uniprot.org/uniprotkb/{accession}.{format}`

Exemplo: `https://rest.uniprot.org/uniprotkb/P12345.fasta`

### 3. Recuperação em Lote e Mapeamento de IDs

Mapeie identificadores de proteínas entre diferentes sistemas de banco de dados e recupere múltiplas entradas eficientemente.

**Workflow de mapeamento de IDs:**
1. Envie trabalho de mapeamento para: `https://rest.uniprot.org/idmapping/run`
2. Verifique status do trabalho: `https://rest.uniprot.org/idmapping/status/{jobId}`
3. Recupere resultados: `https://rest.uniprot.org/idmapping/results/{jobId}`

**Bancos de dados suportados para mapeamento:**
- UniProtKB AC/ID
- Nomes de genes
- Ensembl, RefSeq, EMBL
- PDB, AlphaFoldDB
- KEGG, termos GO
- E muitos mais (veja `/references/id_mapping_databases.md`)

**Limitações:**
- Máximo de 100.000 IDs por trabalho
- Resultados armazenados por 7 dias

### 4. Fazer Streaming de Grandes Conjuntos de Resultados

Para consultas grandes que excedem limites de paginação, use o endpoint de stream:

`https://rest.uniprot.org/uniprotkb/stream?query={query}&format={format}`

O endpoint de stream retorna todos os resultados sem paginação, apropriado para baixar conjuntos de dados completos.

### 5. Personalizar Campos Recuperados

Especifique exatamente quais campos recuperar para transferência de dados eficiente.

**Campos comuns:**
- `accession` - Número de acesso UniProt
- `id` - Nome da entrada
- `gene_names` - Nome(s) do gene
- `organism_name` - Organismo
- `protein_name` - Nomes de proteína
- `sequence` - Sequência de aminoácidos
- `length` - Comprimento da sequência
- `go_*` - Anotações de Gene Ontology
- `cc_*` - Campos de comentário (função, interação, etc.)
- `ft_*` - Anotações de recursos (domínios, sítios, etc.)

**Exemplo:** `https://rest.uniprot.org/uniprotkb/search?query=insulin&fields=accession,gene_names,organism_name,length,sequence&format=tsv`

Veja `/references/api_fields.md` para lista completa de campos.

## Implementação em Python

Para acesso programático, use o script auxiliar fornecido `scripts/uniprot_client.py` que implementa:

- `search_proteins(query, format)` - Buscar no UniProt com qualquer consulta
- `get_protein(accession, format)` - Recuperar entrada de proteína única
- `map_ids(ids, from_db, to_db)` - Mapear entre tipos de identificador
- `batch_retrieve(accessions, format)` - Recuperar múltiplas entradas
- `stream_results(query, format)` - Fazer stream de grandes conjuntos de resultados

**Pacotes Python alternativos:**
- **Unipressed**: Cliente Python moderno e tipado para API REST do UniProt
- **bioservices**: Cliente abrangente de serviços web de bioinformática

## Exemplos de Sintaxe de Consulta

**Operadores booleanos:**
```
kinase AND organism_name:human
(diabetes OR insulin) AND reviewed:true
cancer NOT lung
```

**Buscas específicas por campo:**
```
gene:BRCA1
accession:P12345
organism_id:9606
taxonomy_name:"Homo sapiens"
annotation:(type:signal)
```

**Consultas de intervalo:**
```
length:[100 TO 500]
mass:[50000 TO 100000]
```

**Caracteres curinga:**
```
gene:BRCA*
protein_name:kinase*
```

Veja `/references/query_syntax.md` para documentação abrangente de sintaxe.

## Melhores Práticas

1. **Use entradas revisadas quando possível**: Filtre com `reviewed:true` para entradas Swiss-Prot (manualmente curadas)
2. **Especifique formato explicitamente**: Escolha o formato mais apropriado (FASTA para sequências, TSV para dados tabulares, JSON para análise programática)
3. **Use seleção de campo**: Solicite apenas campos que você precisa para reduzir largura de banda e tempo de processamento
4. **Trate paginação**: Para grandes conjuntos de resultados, implemente paginação apropriada ou use o endpoint de stream
5. **Cache de resultados**: Armazene dados frequentemente acessados localmente para minimizar chamadas à API
6. **Rate limiting**: Seja respeitoso com os recursos da API; implemente atrasos para operações em lote grandes
7. **Verifique qualidade de dados**: Entradas TrEMBL são previsões computacionais; entradas Swiss-Prot são revisadas manualmente

## Recursos

### scripts/
`uniprot_client.py` - Cliente Python com funções auxiliares para operações comuns do UniProt incluindo busca, recuperação, mapeamento de IDs e streaming.

### references/
- `api_fields.md` - Lista completa de campos disponíveis para personalizar consultas
- `id_mapping_databases.md` - Bancos de dados suportados para operações de mapeamento de IDs
- `query_syntax.md` - Sintaxe de consulta abrangente com exemplos avançados
- `api_examples.md` - Exemplos de código em múltiplas linguagens (Python, curl, R)

## Recursos Adicionais

- **Documentação da API**: https://www.uniprot.org/help/api
- **Explorador de API Interativo**: https://www.uniprot.org/api-documentation
- **Tutorial REST**: https://www.uniprot.org/help/uniprot_rest_tutorial
- **Ajuda de Sintaxe de Consulta**: https://www.uniprot.org/help/query-fields
- **Endpoint SPARQL**: https://sparql.uniprot.org/ (para consultas de gráficos avançadas)