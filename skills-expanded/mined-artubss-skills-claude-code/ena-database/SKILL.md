---
name: ena-database
description: "Acesse o European Nucleotide Archive via API/FTP. Recupere sequências de DNA/RNA, leituras brutas (FASTQ), montagens de genoma por acesso, para pipelines de genômica e bioinformática. Suporta múltiplos formatos."
---

# ENA Database

## Visão Geral

O European Nucleotide Archive (ENA) é um repositório público abrangente para dados de sequências de nucleotídeos e metadados associados. Acesse e consulte sequências de DNA/RNA, leituras brutas, montagens de genomas e anotações funcionais através de REST APIs e FTP para pipelines de genômica e bioinformática.

## Quando Usar Este Skill

Este skill deve ser usado quando:

- Recuperar sequências de nucleotídeos ou leituras de sequenciamento brutas por acesso
- Pesquisar amostras, estudos ou montagens por critérios de metadados
- Baixar arquivos FASTQ ou montagens de genoma para análise
- Consultar informações taxonômicas para organismos
- Acessar anotações de sequência e dados funcionais
- Integrar dados do ENA em pipelines de bioinformática
- Realizar buscas de referência cruzada com bancos de dados relacionados
- Baixar datasets em massa via FTP ou Aspera

## Capacidades Principais

### 1. Tipos de Dados e Estrutura

O ENA organiza dados em tipos de objetos hierárquicos:

**Estudos/Projetos** - Agrupam dados relacionados e controlam datas de liberação. Estudos são a unidade principal para citar dados arquivados.

**Amostras** - Representam unidades de material biológico do qual bibliotecas de sequenciamento foram produzidas. Amostras devem ser registradas antes de submeter a maioria dos tipos de dados.

**Leituras Brutas** - Consistem em:
- **Experimentos**: Metadados sobre métodos de sequenciamento, preparação de biblioteca e detalhes do instrumento
- **Execuções**: Referências a arquivos de dados contendo leituras de sequenciamento bruto de uma única execução de sequenciamento

**Montagens** - Montagens de genoma, transcriptoma, metagenoma ou metatranscriptoma em vários níveis de conclusão.

**Sequências** - Sequências montadas e anotadas armazenadas no Banco de Dados de Sequências de Nucleotídeos EMBL, incluindo regiões codificantes/não-codificantes e anotações funcionais.

**Análises** - Resultados de análises computacionais de dados de sequência.

**Registros de Taxonomia** - Informações taxonômicas incluindo linhagem e categoria.

### 2. Acesso Programático

O ENA fornece múltiplas REST APIs para acesso a dados. Consulte `references/api_reference.md` para documentação detalhada de endpoints.

**APIs principais:**

**ENA Portal API** - Funcionalidade de busca avançada em todos os tipos de dados do ENA
- Documentação: https://www.ebi.ac.uk/ena/portal/api/doc
- Use para consultas complexas e buscas de metadados

**ENA Browser API** - Recuperação direta de registros e metadados
- Documentação: https://www.ebi.ac.uk/ena/browser/api/doc
- Use para baixar registros específicos por acesso
- Retorna dados em formato XML

**ENA Taxonomy REST API** - Consulte informações taxonômicas
- Acesse linhagem, categoria e dados taxonômicos relacionados

**ENA Cross Reference Service** - Acesse registros relacionados de bancos de dados externos
- Endpoint: https://www.ebi.ac.uk/ena/xref/rest/

**CRAM Reference Registry** - Recupere sequências de referência
- Endpoint: https://www.ebi.ac.uk/ena/cram/
- Consulte por checksums MD5 ou SHA1

**Rate Limiting**: Todas as APIs têm um limite de taxa de 50 requisições por segundo. Exceder isso retorna HTTP 429 (Too Many Requests).

### 3. Pesquisa e Recuperação de Dados

**Busca Baseada em Browser:**
- Busca de texto livre em todos os campos
- Busca de similaridade de sequência (integração BLAST)
- Busca de referência cruzada para encontrar registros relacionados
- Busca avançada com construtor de consultas Rulespace

**Consultas Programáticas:**
- Use Portal API para buscas avançadas em escala
- Filtre por tipo de dados, intervalo de datas, taxonomia ou campos de metadados
- Baixe resultados como resumos de metadados tabulados ou registros XML

**Exemplo de Padrão de Consulta API:**
```python
import requests

# Search for samples from a specific study
base_url = "https://www.ebi.ac.uk/ena/portal/api/search"
params = {
    "result": "sample",
    "query": "study_accession=PRJEB1234",
    "format": "json",
    "limit": 100
}

response = requests.get(base_url, params=params)
samples = response.json()
```

### 4. Formatos de Recuperação de Dados

**Formatos de Metadados:**
- XML (formato nativo do ENA)
- JSON (via Portal API)
- TSV/CSV (resumos tabulados)

**Dados de Sequência:**
- FASTQ (leituras brutas)
- BAM/CRAM (leituras alinhadas)
- FASTA (sequências montadas)
- Formato de arquivo simples EMBL (sequências anotadas)

**Métodos de Download:**
- Download direto via API (arquivos pequenos)
- FTP para transferência em massa
- Aspera para transferência de alta velocidade de grandes datasets
- enaBrowserTools utilitário de linha de comando para downloads em massa

### 5. Casos de Uso Comuns

**Recuperar leituras de sequenciamento bruto por acesso:**
```python
# Download run files using Browser API
accession = "ERR123456"
url = f"https://www.ebi.ac.uk/ena/browser/api/xml/{accession}"
```

**Pesquisar todas as amostras em um estudo:**
```python
# Use Portal API to list samples
study_id = "PRJNA123456"
url = f"https://www.ebi.ac.uk/ena/portal/api/search?result=sample&query=study_accession={study_id}&format=tsv"
```

**Encontrar montagens para um organismo específico:**
```python
# Search assemblies by taxonomy
organism = "Escherichia coli"
url = f"https://www.ebi.ac.uk/ena/portal/api/search?result=assembly&query=tax_tree({organism})&format=json"
```

**Obter linhagem taxonômica:**
```python
# Query taxonomy API
taxon_id = "562"  # E. coli
url = f"https://www.ebi.ac.uk/ena/taxonomy/rest/tax-id/{taxon_id}"
```

### 6. Integração com Pipelines de Análise

**Padrão de Download em Massa:**
1. Pesquise acessos correspondentes a critérios usando Portal API
2. Extraia URLs de arquivo dos resultados da busca
3. Baixe arquivos via FTP ou usando enaBrowserTools
4. Processe dados baixados no pipeline

**Integração BLAST:**
Integre com o serviço NCBI BLAST do EBI (REST/SOAP API) para buscas de similaridade de sequência contra sequências do ENA.

### 7. Melhores Práticas

**Rate Limiting:**
- Implemente backoff exponencial ao receber respostas HTTP 429
- Agrupe requisições quando possível para permanecer dentro do limite de 50 req/seg
- Use ferramentas de download em massa para datasets grandes em vez de iterar chamadas de API

**Citação de Dados:**
- Sempre cite usando acesso de Estudo/Projeto ao publicar
- Inclua números de acesso para amostras, execuções ou montagens específicas usadas

**Tratamento de Respostas API:**
- Verifique códigos de status HTTP antes de processar respostas
- Analise respostas XML usando bibliotecas XML apropriadas (não regex)
- Gerencie paginação para grandes conjuntos de resultados

**Desempenho:**
- Use FTP/Aspera para baixar arquivos grandes (>100MB)
- Prefira formatos TSV/JSON em vez de XML quando apenas metadados forem necessários
- Armazene localmente pesquisas de taxonomia ao processar muitos registros

## Recursos

Este skill inclui documentação de referência detalhada para trabalhar com ENA:

### references/

**api_reference.md** - Documentação abrangente de endpoint de API incluindo:
- Parâmetros detalhados para Portal API e Browser API
- Especificações de formato de resposta
- Sintaxe e operadores de consulta avançada
- Nomes de campos para filtragem e busca
- Padrões e exemplos de API comuns

Carregue esta referência ao construir consultas complexas de API, depurar respostas de API ou precisar de detalhes de parâmetros específicos.