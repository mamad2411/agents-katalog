---
name: gene-database
description: "Consulte NCBI Gene via E-utilities/Datasets API. Pesquise por símbolo/ID, recupere informações de gene (RefSeqs, GO, localizações, fenótipos), lookups em lote, para anotação de genes e análise funcional."
---

# Gene Database

## Visão Geral

NCBI Gene é um banco de dados abrangente que integra informações de genes de diversas espécies. Fornece nomenclatura, sequências de referência (RefSeqs), mapas cromossômicos, vias biológicas, variações genéticas, fenótipos e referências cruzadas para recursos genômicos globais.

## Quando Usar Esta Skill

Esta skill deve ser usada ao trabalhar com dados de genes, incluindo pesquisa por símbolo ou ID de gene, recuperação de sequências e metadados de genes, análise de funções e vias de genes, ou realização de lookups de genes em lote.

## Início Rápido

NCBI fornece duas APIs principais para acesso a dados de genes:

1. **E-utilities** (Tradicional): API completa para todos os bancos de dados Entrez com consultas flexíveis
2. **NCBI Datasets API** (Mais nova): Otimizada para recuperação de dados de genes com fluxos de trabalho simplificados

Escolha E-utilities para consultas complexas e buscas entre bancos de dados. Escolha Datasets API para recuperação direta de dados de genes com metadados e sequências em uma única solicitação.

## Fluxos de Trabalho Comuns

### Pesquisar Genes por Símbolo ou Nome

Para pesquisar genes por símbolo ou nome entre organismos:

1. Use o script `scripts/query_gene.py` com E-utilities ESearch
2. Especifique o símbolo do gene e o organismo (ex: "BRCA1 in human")
3. O script retorna IDs de gene correspondentes

Exemplos de padrões de consulta:
- Símbolo de gene: `insulin[gene name] AND human[organism]`
- Gene com doença: `dystrophin[gene name] AND muscular dystrophy[disease]`
- Localização cromossômica: `human[organism] AND 17q21[chromosome]`

### Recuperar Informações de Gene por ID

Para buscar informações detalhadas de IDs de gene conhecidos:

1. Use `scripts/fetch_gene_data.py` com Datasets API para dados abrangentes
2. Alternativamente, use `scripts/query_gene.py` com E-utilities EFetch para formatos específicos
3. Especifique o formato de saída desejado (JSON, XML ou texto)

A Datasets API retorna:
- Nomenclatura de gene e aliases
- Sequências de referência (RefSeqs) para transcritos e proteínas
- Localização cromossômica e mapeamento
- Anotações Gene Ontology (GO)
- Publicações associadas

### Lookups de Genes em Lote

Para múltiplos genes simultaneamente:

1. Use `scripts/batch_gene_lookup.py` para processamento em lote eficiente
2. Forneça uma lista de símbolos ou IDs de genes
3. Especifique o organismo para consultas baseadas em símbolos
4. O script lida automaticamente com limite de taxa (10 requisições/segundo com chave de API)

Este fluxo de trabalho é útil para:
- Validar listas de genes
- Recuperar metadados para painéis de genes
- Referenciar cruzadamente identificadores de genes
- Construir tabelas de anotação de genes

### Pesquisar por Contexto Biológico

Para encontrar genes associados a funções biológicas ou fenótipos específicos:

1. Use E-utilities com termos Gene Ontology (GO) ou palavras-chave de fenótipo
2. Consulte por nomes de via ou associações de doenças
3. Filtre por organismo, cromossomo ou outros atributos

Exemplos de pesquisas:
- Por termo GO: `GO:0006915[biological process]` (apoptose)
- Por fenótipo: `diabetes[phenotype] AND mouse[organism]`
- Por via: `insulin signaling pathway[pathway]`

### Padrões de Acesso à API

**Limites de Taxa:**
- Sem chave de API: 3 requisições/segundo para E-utilities, 5 requisições/segundo para Datasets API
- Com chave de API: 10 requisições/segundo para ambas as APIs

**Autenticação:**
Registre-se para uma chave de API NCBI gratuita em https://www.ncbi.nlm.nih.gov/account/ para aumentar limites de taxa.

**Tratamento de Erros:**
Ambas as APIs retornam códigos de status HTTP padrão. Erros comuns incluem:
- 400: Consulta malformada ou parâmetros inválidos
- 429: Limite de taxa excedido
- 404: ID de gene não encontrado

Tente novamente requisições com falha com backoff exponencial.

## Uso de Scripts

### query_gene.py

Consulte NCBI Gene usando E-utilities (ESearch, ESummary, EFetch).

```bash
python scripts/query_gene.py --search "BRCA1" --organism "human"
python scripts/query_gene.py --id 672 --format json
python scripts/query_gene.py --search "insulin[gene] AND diabetes[disease]"
```

### fetch_gene_data.py

Busque dados abrangentes de genes usando NCBI Datasets API.

```bash
python scripts/fetch_gene_data.py --gene-id 672
python scripts/fetch_gene_data.py --symbol BRCA1 --taxon human
python scripts/fetch_gene_data.py --symbol TP53 --taxon "Homo sapiens" --output json
```

### batch_gene_lookup.py

Processe múltiplas consultas de genes de forma eficiente.

```bash
python scripts/batch_gene_lookup.py --file gene_list.txt --organism human
python scripts/batch_gene_lookup.py --ids 672,7157,5594 --output results.json
```

## Referências da API

Para documentação detalhada da API, incluindo endpoints, parâmetros, formatos de resposta e exemplos, consulte:

- `references/api_reference.md` - Documentação abrangente da API para E-utilities e Datasets API
- `references/common_workflows.md` - Exemplos adicionais e padrões de caso de uso

Pesquise estas referências quando precisar de detalhes específicos de endpoint da API, opções de parâmetros ou informações de estrutura de resposta.

## Formatos de Dados

Os dados NCBI Gene podem ser recuperados em múltiplos formatos:

- **JSON**: Dados estruturados ideais para processamento programático
- **XML**: Formato hierárquico detalhado com metadados completos
- **GenBank**: Dados de sequência com anotações
- **FASTA**: Apenas dados de sequência
- **Texto**: Resumos legíveis para humanos

Escolha JSON para aplicações modernas, XML para sistemas herdados que exigem metadados detalhados, e FASTA para fluxos de trabalho de análise de sequência.

## Melhores Práticas

1. **Sempre especifique organismo** ao pesquisar por símbolo de gene para evitar ambiguidade
2. **Use IDs de Gene** para lookups precisos quando disponível
3. **Processe requisições em lote** ao trabalhar com múltiplos genes para minimizar chamadas à API
4. **Armazene resultados em cache** localmente para reduzir consultas redundantes
5. **Inclua chave de API** em scripts para limites de taxa mais altos
6. **Trate erros graciosamente** com lógica de retry para falhas transitórias
7. **Valide símbolos de genes** antes do processamento em lote para detectar erros de digitação

## Recursos

Esta skill inclui:

### scripts/
- `query_gene.py` - Consulte genes usando E-utilities (ESearch, ESummary, EFetch)
- `fetch_gene_data.py` - Busque dados de genes usando NCBI Datasets API
- `batch_gene_lookup.py` - Trate múltiplas consultas de genes de forma eficiente

### references/
- `api_reference.md` - Documentação detalhada da API para E-utilities e Datasets API
- `common_workflows.md` - Exemplos de consultas de genes comuns e casos de uso