---
name: citation-management
description: Gestão abrangente de citações para pesquisa acadêmica. Pesquise Google Scholar e PubMed por artigos, extraia metadados precisos, valide citações e gere entradas BibTeX corretamente formatadas. Esta habilidade deve ser usada quando você precisar encontrar artigos, verificar informações de citação, converter DOIs para BibTeX ou garantir a precisão de referências em redação científica.
allowed-tools: [Read, Write, Edit, Bash]
---

# Gestão de Citações

## Visão Geral

Gerencie citações sistematicamente ao longo do processo de pesquisa e escrita. Esta habilidade fornece ferramentas e estratégias para buscar em bancos de dados acadêmicos (Google Scholar, PubMed), extrair metadados precisos de múltiplas fontes (CrossRef, PubMed, arXiv), validar informações de citação e gerar entradas BibTeX corretamente formatadas.

Crítico para manter a precisão de citações, evitar erros de referência e garantir pesquisa reproduzível. Integra-se perfeitamente com a habilidade de revisão de literatura para fluxos de trabalho de pesquisa abrangentes.

## Quando Usar Esta Habilidade

Use esta habilidade quando:
- Pesquisar artigos específicos no Google Scholar ou PubMed
- Converter DOIs, PMIDs ou IDs do arXiv para BibTeX corretamente formatado
- Extrair metadados completos para citações (autores, título, periódico, ano, etc.)
- Validar citações existentes quanto à precisão
- Limpar e formatar arquivos BibTeX
- Encontrar artigos altamente citados em um campo específico
- Verificar se as informações de citação correspondem à publicação real
- Construir uma bibliografia para um manuscrito ou tese
- Verificar citações duplicadas
- Garantir formatação consistente de citações

## Aprimoramento Visual com Esquemas Científicos

**Ao criar documentos com esta habilidade, sempre considere adicionar diagramas e esquemas científicos para aprimorar a comunicação visual.**

Se o seu documento ainda não contiver esquemas ou diagramas:
- Use a habilidade **scientific-schematics** para gerar diagramas de qualidade para publicação com IA
- Simplesmente descreva seu diagrama desejado em linguagem natural
- Nano Banana Pro gerará, revisará e refinará automaticamente o esquema

**Para novos documentos:** Os esquemas científicos devem ser gerados por padrão para representar visualmente conceitos-chave, fluxos de trabalho, arquiteturas ou relações descritas no texto.

**Como gerar esquemas:**
```bash
python scripts/generate_schematic.py "sua descrição do diagrama" -o figures/output.png
```

A IA gerará automaticamente:
- Imagens de qualidade para publicação com formatação apropriada
- Revisão e refinamento através de múltiplas iterações
- Garantia de acessibilidade (amigável para daltônicos, alto contraste)
- Salvamento de outputs no diretório figures/

**Quando adicionar esquemas:**
- Diagramas de fluxo de trabalho de citação
- Fluxogramas de metodologia de busca de literatura
- Arquiteturas de sistema de gerenciamento de referências
- Árvores de decisão de estilo de citação
- Diagramas de integração de banco de dados
- Qualquer conceito complexo que se beneficie de visualização

Para orientação detalhada sobre como criar esquemas, consulte a documentação da habilidade scientific-schematics.

---

## Fluxo de Trabalho Principal

A gestão de citações segue um processo sistemático:

### Fase 1: Descoberta e Busca de Artigos

**Objetivo**: Encontrar artigos relevantes usando mecanismos de busca acadêmica.

#### Busca no Google Scholar

Google Scholar oferece cobertura mais abrangente entre disciplinas.

**Busca Básica**:
```bash
# Pesquisar artigos sobre um tópico
python scripts/search_google_scholar.py "edição de genes CRISPR" \
  --limit 50 \
  --output results.json

# Pesquisar com filtro de ano
python scripts/search_google_scholar.py "aprendizado de máquina dobramento de proteínas" \
  --year-start 2020 \
  --year-end 2024 \
  --limit 100 \
  --output ml_proteins.json
```

**Estratégias de Busca Avançada** (ver `references/google_scholar_search.md`):
- Use aspas para frases exatas: `"aprendizado profundo"`
- Pesquise por autor: `author:LeCun`
- Pesquise no título: `intitle:"redes neurais"`
- Exclua termos: `aprendizado de máquina -survey`
- Encontre artigos altamente citados usando opções de classificação
- Filtre por intervalo de datas para obter trabalhos recentes

**Melhores Práticas**:
- Use termos de busca específicos e direcionados
- Inclua termos técnicos e siglas principais
- Filtre por anos recentes para campos em movimento rápido
- Verifique "Citado por" para encontrar artigos seminais
- Exporte resultados principais para análise adicional

#### Busca no PubMed

PubMed especializa-se em literatura biomédica e ciências da vida (35+ milhões de citações).

**Busca Básica**:
```bash
# Pesquisar PubMed
python scripts/search_pubmed.py "tratamento da doença de Alzheimer" \
  --limit 100 \
  --output alzheimers.json

# Pesquisar com termos MeSH e filtros
python scripts/search_pubmed.py \
  --query '"Doença de Alzheimer"[MeSH] AND "Terapia Medicamentosa"[MeSH]' \
  --date-start 2020 \
  --date-end 2024 \
  --publication-types "Clinical Trial,Review" \
  --output alzheimers_trials.json
```

**Consultas Avançadas do PubMed** (ver `references/pubmed_search.md`):
- Use termos MeSH: `"Diabetes Mellitus"[MeSH]`
- Tags de campo: `"câncer"[Title]`, `"Smith J"[Author]`
- Operadores booleanos: `AND`, `OR`, `NOT`
- Filtros de data: `2020:2024[Publication Date]`
- Tipos de publicação: `"Review"[Publication Type]`
- Combine com API E-utilities para automação

**Melhores Práticas**:
- Use o Navegador MeSH para encontrar vocabulário controlado correto
- Construa consultas complexas no Construtor de Busca Avançada do PubMed primeiro
- Inclua múltiplos sinônimos com OR
- Recupere PMIDs para fácil extração de metadados
- Exporte para JSON ou diretamente para BibTeX

### Fase 2: Extração de Metadados

**Objetivo**: Converter identificadores de artigos (DOI, PMID, ID arXiv) em metadados completos e precisos.

#### Conversão Rápida de DOI para BibTeX

Para DOIs únicos, use a ferramenta de conversão rápida:

```bash
# Converter DOI único
python scripts/doi_to_bibtex.py 10.1038/s41586-021-03819-2

# Converter múltiplos DOIs de um arquivo
python scripts/doi_to_bibtex.py --input dois.txt --output references.bib

# Diferentes formatos de output
python scripts/doi_to_bibtex.py 10.1038/nature12345 --format json
```

#### Extração Abrangente de Metadados

Para DOIs, PMIDs, IDs do arXiv ou URLs:

```bash
# Extrair de DOI
python scripts/extract_metadata.py --doi 10.1038/s41586-021-03819-2

# Extrair de PMID
python scripts/extract_metadata.py --pmid 34265844

# Extrair de ID arXiv
python scripts/extract_metadata.py --arxiv 2103.14030

# Extrair de URL
python scripts/extract_metadata.py --url "https://www.nature.com/articles/s41586-021-03819-2"

# Extração em lote de arquivo (identificadores mistos)
python scripts/extract_metadata.py --input identifiers.txt --output citations.bib
```

**Fontes de Metadados** (ver `references/metadata_extraction.md`):

1. **API CrossRef**: Fonte primária para DOIs
   - Metadados abrangentes para artigos de periódicos
   - Informações fornecidas pelo editor
   - Inclui autores, título, periódico, volume, páginas, datas
   - Gratuito, sem chave de API necessária

2. **E-utilities do PubMed**: Literatura biomédica
   - Metadados oficiais do NCBI
   - Inclui termos MeSH, resumos
   - Identificadores PMID e PMCID
   - Gratuito, chave de API recomendada para alto volume

3. **API do arXiv**: Pré-impressões em física, matemática, CI, q-bio
   - Metadados completos para pré-impressões
   - Rastreamento de versão
   - Afiliações de autores
   - Acesso gratuito e aberto

4. **API DataCite**: Conjuntos de dados de pesquisa, software, outros recursos
   - Metadados para outputs acadêmicos não-tradicionais
   - DOIs para conjuntos de dados e código
   - Acesso gratuito

**O que é Extraído**:
- **Campos obrigatórios**: autor, título, ano
- **Artigos de periódicos**: periódico, volume, número, páginas, DOI
- **Livros**: editora, ISBN, edição
- **Artigos de conferência**: nome da conferência, local, páginas
- **Pré-impressões**: repositório (arXiv, bioRxiv), ID de pré-impressão
- **Adicional**: resumo, palavras-chave, URL

### Fase 3: Formatação BibTeX

**Objetivo**: Gerar entradas BibTeX limpas e corretamente formatadas.

#### Compreendendo Tipos de Entradas BibTeX

Ver `references/bibtex_formatting.md` para guia completo.

**Tipos de Entrada Comuns**:
- `@article`: Artigos de periódicos (mais comum)
- `@book`: Livros
- `@inproceedings`: Artigos de conferência
- `@incollection`: Capítulos de livros
- `@phdthesis`: Dissertações
- `@misc`: Pré-impressões, software, conjuntos de dados

**Campos Obrigatórios por Tipo**:

```bibtex
@article{citationkey,
  author  = {Last1, First1 and Last2, First2},
  title   = {Article Title},
  journal = {Journal Name},
  year    = {2024},
  volume  = {10},
  number  = {3},
  pages   = {123--145},
  doi     = {10.1234/example}
}

@inproceedings{citationkey,
  author    = {Last, First},
  title     = {Paper Title},
  booktitle = {Conference Name},
  year      = {2024},
  pages     = {1--10}
}

@book{citationkey,
  author    = {Last, First},
  title     = {Book Title},
  publisher = {Publisher Name},
  year      = {2024}
}
```

#### Formatação e Limpeza

Use o formatador para padronizar arquivos BibTeX:

```bash
# Formatar e limpar arquivo BibTeX
python scripts/format_bibtex.py references.bib \
  --output formatted_references.bib

# Classificar entradas por chave de citação
python scripts/format_bibtex.py references.bib \
  --sort key \
  --output sorted_references.bib

# Classificar por ano (mais recentes primeiro)
python scripts/format_bibtex.py references.bib \
  --sort year \
  --descending \
  --output sorted_references.bib

# Remover duplicatas
python scripts/format_bibtex.py references.bib \
  --deduplicate \
  --output clean_references.bib

# Validar e gerar relatório
python scripts/format_bibtex.py references.bib \
  --validate \
  --report validation_report.txt
```

**Operações de Formatação**:
- Padronizar ordem de campos
- Indentação e espaçamento consistentes
- Capitalização apropriada em títulos (protegida com {})
- Formato de nome de autor padronizado
- Formato de chave de citação consistente
- Remover campos desnecessários
- Corrigir erros comuns (vírgulas, chaves ausentes)

### Fase 4: Validação de Citações

**Objetivo**: Verificar se todas as citações são precisas e completas.

#### Validação Abrangente

```bash
# Validar arquivo BibTeX
python scripts/validate_citations.py references.bib

# Validar e corrigir problemas comuns
python scripts/validate_citations.py references.bib \
  --auto-fix \
  --output validated_references.bib

# Gerar relatório de validação detalhado
python scripts/validate_citations.py references.bib \
  --report validation_report.json \
  --verbose
```

**Verificações de Validação** (ver `references/citation_validation.md`):

1. **Verificação de DOI**:
   - DOI resolve corretamente via doi.org
   - Metadados correspondem entre BibTeX e CrossRef
   - Sem DOIs quebrados ou inválidos

2. **Campos Obrigatórios**:
   - Todos os campos obrigatórios presentes para tipo de entrada
   - Nenhuma informação vazia ou crítica ausente
   - Nomes de autores corretamente formatados

3. **Consistência de Dados**:
   - Ano é válido (4 dígitos, intervalo razoável)
   - Volume/número são numéricos
   - Páginas formatadas corretamente (ex: 123--145)
   - URLs são acessíveis

4. **Detecção de Duplicatas**:
   - Mesmo DOI usado múltiplas vezes
   - Títulos similares (possíveis duplicatas)
   - Combinações de autor/ano/título idênticas

5. **Conformidade de Formato**:
   - Sintaxe BibTeX válida
   - Chaves e aspas apropriadas
   - Chaves de citação únicas
   - Caracteres especiais tratados corretamente

**Output de Validação**:
```json
{
  "total_entries": 150,
  "valid_entries": 145,
  "errors": [
    {
      "citation_key": "Smith2023",
      "error_type": "missing_field",
      "field": "journal",
      "severity": "high"
    },
    {
      "citation_key": "Jones2022",
      "error_type": "invalid_doi",
      "doi": "10.1234/broken",
      "severity": "high"
    }
  ],
  "warnings": [
    {
      "citation_key": "Brown2021",
      "warning_type": "possible_duplicate",
      "duplicate_of": "Brown2021a",
      "severity": "medium"
    }
  ]
}
```

### Fase 5: Integração com Fluxo de Trabalho de Escrita

#### Construindo Referências para Manuscritos

Fluxo de trabalho completo para criar uma bibliografia:

```bash
# 1. Pesquisar artigos sobre seu tópico
python scripts/search_pubmed.py \
  '"Sistemas CRISPR-Cas"[MeSH] AND "Edição de Genes"[MeSH]' \
  --date-start 2020 \
  --limit 200 \
  --output crispr_papers.json

# 2. Extrair DOIs dos resultados de busca e converter para BibTeX
python scripts/extract_metadata.py \
  --input crispr_papers.json \
  --output crispr_refs.bib

# 3. Adicionar artigos específicos por DOI
python scripts/doi_to_bibtex.py 10.1038/nature12345 >> crispr_refs.bib
python scripts/doi_to_bibtex.py 10.1126/science.abcd1234 >> crispr_refs.bib

# 4. Formatar e limpar arquivo BibTeX
python scripts/format_bibtex.py crispr_refs.bib \
  --deduplicate \
  --sort year \
  --descending \
  --output references.bib

# 5. Validar todas as citações
python scripts/validate_citations.py references.bib \
  --auto-fix \
  --report validation.json \
  --output final_references.bib

# 6. Revisar relatório de validação e corrigir problemas restantes
cat validation.json

# 7. Usar em seu documento LaTeX
# \bibliography{final_references}
```

#### Integração com Habilidade de Revisão de Literatura

Esta habilidade complementa a habilidade `literature-review`:

**Habilidade de Revisão de Literatura** → Busca e síntese sistemáticas
**Habilidade de Gestão de Citações** → Tratamento técnico de citações

**Fluxo de Trabalho Combinado**:
1. Use `literature-review` para busca abrangente em múltiplos bancos de dados
2. Use `citation-management` para extrair e validar todas as citações
3. Use `literature-review` para sintetizar achados tematicamente
4. Use `citation-management` para verificar precisão final da bibliografia

```bash
# Após completar revisão de literatura
# Verificar todas as citações no documento de revisão
python scripts/validate_citations.py my_review_references.bib --report review_validation.json

# Formatar para estilo de citação específico, se necessário
python scripts/format_bibtex.py my_review_references.bib \
  --style nature \
  --output formatted_refs.bib
```

## Estratégias de Busca

### Melhores Práticas no Google Scholar

**Encontrando Artigos Seminais**:
- Classifique por contagem de citações (mais citados primeiro)
- Procure por artigos de revisão para visão geral
- Verifique "Citado por" para avaliação de impacto
- Use alertas de citação para rastrear novas citações

**Operadores Avançados** (lista completa em `references/google_scholar_search.md`):
```
"frase exata"           # Correspondência de frase exata
author:sobrenome        # Pesquisa por autor
intitle:palavra-chave   # Pesquisa apenas no título
source:periódico        # Pesquisa periódico específico
-excluir               # Excluir termos
OR                     # Termos alternativos
2020..2024            # Intervalo de ano
```

**Buscas de Exemplo**:
```
# Encontrar revisões recentes sobre um tópico
"CRISPR" intitle:review 2023..2024

# Encontrar artigos de autor específico sobre tópico
author:Church "biologia sintética"

# Encontrar trabalho fundamental altamente citado
"aprendizado profundo" 2012..2015 sort:citations

# Excluir surveys e focar em métodos
"dobramento de proteínas" -survey -review intitle:method
```

### Melhores Práticas no PubMed

**Usando Termos MeSH**:
MeSH (Medical Subject Headings) oferece vocabulário controlado para buscas precisas.

1. **Encontre termos MeSH** em https://meshb.nlm.nih.gov/search
2. **Use em consultas**: `"Diabetes Mellitus, Type 2"[MeSH]`
3. **Combine com palavras-chave** para cobertura abrangente

**Tags de Campo**:
```
[Title]              # Pesquisa apenas no título
[Title/Abstract]     # Pesquisa no título ou resumo
[Author]             # Pesquisa por nome de autor
[Journal]            # Pesquisa periódico específico
[Publication Date]   # Intervalo de data
[Publication Type]   # Tipo de artigo
[MeSH]              # Termo MeSH
```

**Construindo Consultas Complexas**:
```bash
# Ensaios clínicos sobre tratamento de diabetes publicados recentemente
"Diabetes Mellitus, Type 2"[MeSH] AND "Terapia Medicamentosa"[MeSH] 
AND "Clinical Trial"[Publication Type] AND 2020:2024[Publication Date]

# Revisões sobre CRISPR em periódico específico
"Sistemas CRISPR-Cas"[MeSH] AND "Nature"[Journal] AND "Review"[Publication Type]

# Trabalho recente de autor específico
"Smith AB"[Author] AND câncer[Title/Abstract] AND 2022:2024[Publication Date]
```

**E-utilities para Automação**:
Os scripts usam API E-utilities do NCBI para acesso programático:
- **ESearch**: Pesquisar e recuperar PMIDs
- **EFetch**: Recuperar metadados completos
- **ESummary**: Obter informações de resumo
- **ELink**: Encontrar artigos relacionados

Ver `references/pubmed_search.md` para documentação completa da API.

## Ferramentas e Scripts

### search_google_scholar.py

Pesquisar Google Scholar e exportar resultados.

**Características**:
- Busca automatizada com limitação de taxa
- Suporte a paginação
- Filtragem por intervalo de ano
- Exportação para JSON ou BibTeX
- Informações de contagem de citações

**Uso**:
```bash
# Busca básica
python scripts/search_google_scholar.py "computação quântica"

# Busca avançada com filtros
python scripts/search_google_scholar.py "computação quântica" \
  --year-start 2020 \
  --year-end 2024 \
  --limit 100 \
  --sort-by citations \
  --output quantum_papers.json

# Exportar diretamente para BibTeX
python scripts/search_google_scholar.py "aprendizado de máquina" \
  --limit 50 \
  --format bibtex \
  --output ml_papers.bib
```

### search_pubmed.py

Pesquisar PubMed usando API E-utilities.

**Características**:
- Suporte a consulta complexa (MeSH, tags de campo, Booleano)
- Filtragem por intervalo de data
- Filtragem por tipo de publicação
- Recuperação em lote com metadados
- Exportação para JSON ou BibTeX

**Uso**:
```bash
# Busca simples por palavra-chave
python scripts/search_pubmed.py "edição de genes CRISPR"

# Consulta complexa com filtros
python scripts/search_pubmed.py \
  --query '"Sistemas CRISPR-Cas"[MeSH] AND "terapêutico"[Title/Abstract]' \
  --date-start 2020-01-01 \
  --date-end 2024-12-31 \
  --publication-types "Clinical Trial,Review" \
  --limit 200 \
  --output crispr_therapeutic.json

# Exportar para BibTeX
python scripts/search_pubmed.py "doença de Alzheimer" \
  --limit 100 \
  --format bibtex \
  --output alzheimers.bib
```

### extract_metadata.py

Extrair metadados completos de identificadores de artigos.

**Características**:
- Suporta DOI, PMID, ID arXiv, URL
- Consulta APIs CrossRef, PubMed, arXiv
- Trata múltiplos tipos de identificador
- Processamento em lote
- Múltiplos formatos de output

**Uso**:
```bash
# DOI único
python scripts/extract_metadata.py --doi 10.1038/s41586-021-03819-2

# PMID único
python scripts/extract_metadata.py --pmid 34265844

# ID arXiv único
python scripts/extract_metadata.py --arxiv 2103.14030

# De URL
python scripts/extract_metadata.py \
  --url "https://www.nature.com/articles/s41586-021-03819-2"

# Processamento em lote (arquivo com um identificador por linha)
python scripts/extract_metadata.py \
  --input paper_ids.txt \
  --output references.bib

# Diferentes formatos de output
python scripts/extract_metadata.py \
  --doi 10.1038/nature12345 \
  --format json  # ou bibtex, yaml
```

### validate_citations.py

Validar entradas BibTeX quanto à precisão e completude.

**Características**:
- Verificação de DOI via doi.org e CrossRef
- Verificação de campo obrigatório
- Detecção de duplicata
- Validação de formato
- Correção automática de problemas comuns
- Relatório detalhado

**Uso**:
```bash
# Validação básica
python scripts/validate_citations.py references.bib

# Com correção automática
python scripts/validate_citations.py references.bib \
  --auto-fix \
  --output fixed_references.bib

# Relatório de validação detalhado
python scripts/validate_citations.py references.bib \
  --report validation_report.json \
  --verbose

# Verificar apenas DOIs
python scripts/validate_citations.py references.bib \
  --check-dois-only
```

### format_bibtex.py

Formatar e limpar arquivos BibTeX.

**Características**:
- Padronizar formatação
- Classificar entradas (por chave, ano, autor)
- Remover duplicatas
- Validar sintaxe
- Corrigir erros comuns
- Impor convenções de chave de citação

**Uso**:
```bash
# Formatação básica
python scripts/format_bibtex.py references.bib

# Classificar por ano (mais recentes primeiro)
python scripts/format_bibtex.py references.bib \
  --sort year \
  --descending \
  --output sorted_refs.bib

# Remover duplicatas
python scripts/format_bibtex.py references.bib \
  --deduplicate \
  --output clean_refs.bib

# Limpeza completa
python scripts/format_bibtex.py references.bib \
  --deduplicate \
  --sort year \
  --validate \
  --auto-fix \
  --output final_refs.bib
```

### doi_to_bibtex.py

Conversão rápida de DOI para BibTeX.

**Características**:
- Conversão rápida de DOI único
- Processamento em lote
- Múltiplos formatos de output
- Suporte à área de transferência

**Uso**:
```bash
# DOI único
python scripts/doi_to_bibtex.py 10.1038/s41586-021-03819-2

# Múltiplos DOIs
python scripts/doi_to_bibtex.py \
  10.1038/nature12345 \
  10.1126/science.abc1234 \
  10.1016/j.cell.2023.01.001

# De arquivo (um DOI por linha)
python scripts/doi_to_bibtex.py --input dois.txt --output references.bib

# Copiar para área de transferência
python scripts/doi_to_bibtex.py 10.1038/nature12345 --clipboard
```

## Melhores Práticas

### Estratégia de Busca

1. **Comece amplo, depois restrinja**:
   - Comece com termos gerais para entender o campo
   - Refine com palavras-chave específicas e filtros
   - Use sinônimos e termos relacionados

2. **Use múltiplas fontes**:
   - Google Scholar para cobertura abrangente
   - PubMed para foco biomédico
   - arXiv para pré-impressões
   - Combine resultados para completude

3. **Aproveite citações**:
   - Verifique "Citado por" para artigos seminais
   - Revise referências de artigos principais
   - Use redes de citação para descobrir trabalho relacionado

4. **Documente suas buscas**:
   - Salve consultas de busca e datas
   - Registre número de resultados
   - Anote filtros ou restrições aplicadas

### Extração de Metadados

1. **Sempre use DOIs quando disponíveis**:
   - Identificador mais confiável
   - Link permanente para publicação
   - Melhor fonte de metadados via CrossRef

2. **Verifique metadados extraídos**:
   - Verifique se os nomes de autores estão corretos
   - Verifique nomes de periódico/conferência
   - Confirme ano de publicação
   - Valide números de página e volume

3. **Trate casos especiais**:
   - Pré-impressões: Inclua repositório e ID
   - Pré-impressões depois publicadas: Use versão publicada
   - Artigos de conferência: Inclua nome e local da conferência
   - Capítulos de livros: Inclua título do livro e editores

4. **Mantenha consistência**:
   - Use formato de nome de autor consistente
   - Padronize abreviações de periódicos
   - Use mesmo formato de DOI (URL preferido)

### Qualidade BibTeX

1. **Siga convenções**:
   - Use chaves de citação significativas (FirstAutor2024palavra-chave)
   - Proteja capitalização em títulos com {}
   - Use -- para intervalos de páginas (não hífen único)
   - Inclua campo DOI para todas as publicações modernas

2. **Mantenha lim