---
name: pubmed-database
description: "Acesso direto via API REST ao PubMed. Consultas avançadas com Boolean/MeSH, API E-utilities, processamento em lote, gestão de citações. Para workflows em Python, prefira biopython (Bio.Entrez). Use isso para trabalho HTTP/REST direto ou implementações de API customizadas."
---

# Base de Dados PubMed

## Visão Geral

PubMed é o banco de dados abrangente da Biblioteca Nacional de Medicina dos EUA, oferecendo acesso gratuito ao MEDLINE e literatura de ciências da vida. Construa consultas avançadas com operadores Boolean, termos MeSH e tags de campo, acesse dados programaticamente via API E-utilities para revisões sistemáticas e análise de literatura.

## Quando Usar Esta Habilidade

Esta habilidade deve ser usada quando:
- Procurar artigos de pesquisa biomédica ou de ciências da vida
- Construir consultas complexas com operadores Boolean, tags de campo ou termos MeSH
- Conduzir revisões sistemáticas de literatura ou meta-análises
- Acessar dados do PubMed programaticamente via API E-utilities
- Encontrar artigos por critérios específicos (autor, periódico, data de publicação, tipo de artigo)
- Recuperar informações de citação, abstratos ou artigos em texto completo
- Trabalhar com PMIDs (IDs PubMed) ou DOIs
- Criar workflows automatizados para monitoramento de literatura ou extração de dados

## Capacidades Principais

### 1. Construção Avançada de Consultas

Construa consultas sofisticadas no PubMed usando operadores Boolean, tags de campo e sintaxe especializada.

**Estratégias Básicas de Busca**:
- Combine conceitos com operadores Boolean (AND, OR, NOT)
- Use tags de campo para limitar buscas a partes específicas do registro
- Empregue busca por frase com aspas duplas para correspondências exatas
- Aplique wildcards para variações de termos
- Use busca por proximidade para termos dentro de distâncias especificadas

**Consultas de Exemplo**:
```
# Revisões sistemáticas recentes sobre tratamento de diabetes
diabetes mellitus[mh] AND treatment[tiab] AND systematic review[pt] AND 2023:2024[dp]

# Ensaios clínicos comparando dois medicamentos
(metformin[nm] OR insulin[nm]) AND diabetes mellitus, type 2[mh] AND randomized controlled trial[pt]

# Pesquisa específica de autor
smith ja[au] AND cancer[tiab] AND 2023[dp] AND english[la]
```

**Quando consultar search_syntax.md**:
- Necessário lista abrangente de tags de campo disponíveis
- Requer explicação detalhada de operadores de busca
- Construção de buscas por proximidade complexas
- Compreensão do comportamento de mapeamento automático de termos
- Necessário sintaxe específica para intervalos de data, wildcards ou caracteres especiais

Padrão grep para tags de campo: `\[au\]|\[ti\]|\[ab\]|\[mh\]|\[pt\]|\[dp\]`

### 2. Termos MeSH e Vocabulário Controlado

Use Medical Subject Headings (MeSH) para buscas precisas e consistentes em toda a literatura biomédica.

**Busca com MeSH**:
- Tag [mh] busca termos MeSH com inclusão automática de termos mais específicos
- Tag [majr] limita a artigos onde o tópico é o foco principal
- Combine termos MeSH com subheadings para especificidade (ex: diabetes mellitus/therapy[mh])

**Subheadings MeSH Comuns**:
- /diagnosis - Métodos diagnósticos
- /drug therapy - Tratamento farmacêutico
- /epidemiology - Padrões e prevalência da doença
- /etiology - Causas da doença
- /prevention & control - Medidas preventivas
- /therapy - Abordagens de tratamento

**Exemplo**:
```
# Terapia de diabetes com foco específico
diabetes mellitus, type 2[mh]/drug therapy AND cardiovascular diseases[mh]/prevention & control
```

### 3. Filtragem por Tipo de Artigo e Publicação

Filtre resultados por tipo de publicação, data, disponibilidade de texto e outros atributos.

**Tipos de Publicação** (use tag de campo [pt]):
- Clinical Trial
- Meta-Analysis
- Randomized Controlled Trial
- Review
- Systematic Review
- Case Reports
- Guideline

**Filtragem por Data**:
- Ano único: `2024[dp]`
- Intervalo de data: `2020:2024[dp]`
- Data específica: `2024/03/15[dp]`

**Disponibilidade de Texto**:
- Texto completo gratuito: Adicione `AND free full text[sb]` à consulta
- Tem resumo: Adicione `AND hasabstract[text]` à consulta

**Exemplo**:
```
# RCTs recentes em texto completo gratuito sobre hipertensão
hypertension[mh] AND randomized controlled trial[pt] AND 2023:2024[dp] AND free full text[sb]
```

### 4. Acesso Programático via API E-utilities

Acesse dados do PubMed programaticamente usando a API REST NCBI E-utilities para automação e operações em massa.

**Endpoints API Principais**:
1. **ESearch** - Pesquise banco de dados e recupere PMIDs
2. **EFetch** - Baixe registros completos em vários formatos
3. **ESummary** - Obtenha resumos de documentos
4. **EPost** - Carregue UIDs para processamento em lote
5. **ELink** - Encontre artigos relacionados e dados vinculados

**Workflow Básico**:
```python
import requests

# Passo 1: Pesquise artigos
base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
search_url = f"{base_url}esearch.fcgi"
params = {
    "db": "pubmed",
    "term": "diabetes[tiab] AND 2024[dp]",
    "retmax": 100,
    "retmode": "json",
    "api_key": "YOUR_API_KEY"  # Opcional mas recomendado
}
response = requests.get(search_url, params=params)
pmids = response.json()["esearchresult"]["idlist"]

# Passo 2: Recupere detalhes de artigos
fetch_url = f"{base_url}efetch.fcgi"
params = {
    "db": "pubmed",
    "id": ",".join(pmids),
    "rettype": "abstract",
    "retmode": "text",
    "api_key": "YOUR_API_KEY"
}
response = requests.get(fetch_url, params=params)
abstracts = response.text
```

**Limites de Taxa**:
- Sem chave API: 3 requisições/segundo
- Com chave API: 10 requisições/segundo
- Sempre inclua header User-Agent

**Melhores Práticas**:
- Use servidor de histórico (usehistory=y) para grandes conjuntos de resultados
- Implemente operações em lote via EPost para múltiplos UIDs
- Cache resultados localmente para minimizar chamadas redundantes
- Respeite limites de taxa para evitar interrupção de serviço

**Quando consultar api_reference.md**:
- Necessária documentação detalhada de endpoints
- Requer especificações de parâmetros para cada E-utility
- Construção de operações em lote ou workflows de servidor de histórico
- Compreensão de formatos de resposta (XML, JSON, texto)
- Resolução de problemas de API ou questões de limite de taxa

Padrão grep para endpoints API: `esearch|efetch|esummary|epost|elink|einfo`

### 5. Correspondência de Citações e Recuperação de Artigos

Encontre artigos usando informações parciais de citação ou identificadores específicos.

**Por Identificador**:
```
# Por PMID
12345678[pmid]

# Por DOI
10.1056/NEJMoa123456[doi]

# Por ID PMC
PMC123456[pmc]
```

**Correspondência de Citações** (via API ECitMatch):
Use nome do periódico, ano, volume, página e autor para encontrar PMIDs:
```
Formato: journal|year|volume|page|author|key|
Exemplo: Science|2008|320|5880|1185|key1|
```

**Por Autor e Metadados**:
```
# Primeiro autor com ano e tópico
smith ja[1au] AND 2023[dp] AND cancer[tiab]

# Periódico, volume e página
nature[ta] AND 2024[dp] AND 456[vi] AND 123-130[pg]
```

### 6. Revisões Sistemáticas de Literatura

Conduza buscas abrangentes de literatura para revisões sistemáticas e meta-análises.

**Framework PICO** (População, Intervenção, Comparação, Desfecho):
Estruture questões de pesquisa clínica sistematicamente:
```
# Exemplo: Efetividade do tratamento de diabetes
# P: diabetes mellitus, type 2[mh]
# I: metformin[nm]
# C: lifestyle modification[tiab]
# O: glycemic control[tiab]

diabetes mellitus, type 2[mh] AND
(metformin[nm] OR lifestyle modification[tiab]) AND
glycemic control[tiab] AND
randomized controlled trial[pt]
```

**Estratégia de Busca Abrangente**:
```
# Inclua múltiplos sinônimos e termos MeSH
(disease name[tiab] OR disease name[mh] OR synonym[tiab]) AND
(treatment[tiab] OR therapy[tiab] OR intervention[tiab]) AND
(systematic review[pt] OR meta-analysis[pt] OR randomized controlled trial[pt]) AND
2020:2024[dp] AND
english[la]
```

**Refinamento de Busca**:
1. Comece amplo, revise resultados
2. Adicione especificidade com tags de campo
3. Aplique filtros de data e tipo de publicação
4. Use Busca Avançada para visualizar tradução da consulta
5. Combine histórico de busca para consultas complexas

**Quando consultar common_queries.md**:
- Necessário consultas de exemplo para tipos de doença ou áreas de pesquisa específicas
- Requer templates para diferentes desenhos de estudo
- Procurando padrões de consulta específicos de população (pediátrica, geriátrica, etc.)
- Construção de buscas específicas de metodologia
- Necessário filtros de qualidade ou padrões de melhores práticas

Padrão grep para exemplos de consulta: `diabetes|cancer|cardiovascular|clinical trial|systematic review`

### 7. Histórico de Busca e Buscas Salvas

Use recursos de histórico de busca e My NCBI do PubMed para workflows de pesquisa eficientes.

**Histórico de Busca** (via Busca Avançada):
- Mantém até 100 buscas
- Expira após 8 horas de inatividade
- Combine buscas anteriores usando referências com #
- Visualize contagens de resultados antes de executar

**Exemplo**:
```
#1: diabetes mellitus[mh]
#2: cardiovascular diseases[mh]
#3: #1 AND #2 AND risk factors[tiab]
```

**Recursos My NCBI**:
- Salve buscas indefinidamente
- Configure alertas por email para novos artigos correspondentes
- Crie coleções de artigos salvos
- Organize pesquisa por projeto ou tópico

**Feeds RSS**:
Crie feeds RSS para qualquer busca para monitorar novas publicações em sua área de interesse.

### 8. Artigos Relacionados e Descoberta de Citações

Encontre pesquisas relacionadas e explore redes de citação.

**Recurso de Artigos Similares**:
Cada artigo PubMed inclui artigos relacionados pré-calculados baseados em:
- Semelhança de título e resumo
- Sobreposição de termos MeSH
- Correspondência algorítmica ponderada

**ELink para Dados Relacionados**:
```
# Encontre artigos relacionados programaticamente
elink.fcgi?dbfrom=pubmed&db=pubmed&id=PMID&cmd=neighbor
```

**Links de Citação**:
- LinkOut para texto completo de editoras
- Links para artigos gratuitos do PubMed Central
- Conexões a entradas de bancos de dados NCBI relacionados (GenBank, ClinicalTrials.gov, etc.)

### 9. Exportação e Gestão de Citações

Exporte resultados de busca em vários formatos para gestão de citações e análise posterior.

**Formatos de Exportação**:
- Arquivos .nbib para gerenciadores de referências (Zotero, Mendeley, EndNote)
- Estilos de citação AMA, MLA, APA, NLM
- CSV para análise de dados
- XML para processamento programático

**Clipboard e Coleções**:
- Clipboard: Armazenamento temporário para até 500 itens (expiração em 8 horas)
- Coleções: Armazenamento permanente via conta My NCBI

**Exportação em Lote via API**:
```python
# Exporte citações em formato MEDLINE
efetch.fcgi?db=pubmed&id=PMID1,PMID2&rettype=medline&retmode=text
```

## Trabalhando com Arquivos de Referência

Esta habilidade inclui três arquivos de referência abrangentes no diretório `references/`:

### references/api_reference.md
Documentação completa da API E-utilities incluindo todos os nove endpoints, parâmetros, formatos de resposta e melhores práticas. Consulte quando:
- Implementar acesso programático ao PubMed
- Construir solicitações de API
- Compreender limites de taxa e autenticação
- Trabalhar com grandes conjuntos de dados via servidor de histórico
- Resolver problemas de API

### references/search_syntax.md
Guia detalhado da sintaxe de busca do PubMed incluindo tags de campo, operadores Boolean, wildcards e caracteres especiais. Consulte quando:
- Construir consultas de busca complexas
- Compreender mapeamento automático de termos
- Usar recursos de busca avançada (proximidade, wildcards)
- Aplicar filtros e limites
- Resolver problemas de resultados inesperados de busca

### references/common_queries.md
Coleção extensa de consultas de exemplo para vários cenários de pesquisa, tipos de doença e metodologias. Consulte quando:
- Iniciar uma nova busca de literatura
- Necessário templates para áreas de pesquisa específicas
- Procurando padrões de consultas de melhores práticas
- Conduzindo revisões sistemáticas
- Buscando por desenhos de estudo específicos ou populações

**Estratégia de Carregamento de Referência**:
Carregue arquivos de referência no contexto conforme necessário com base na tarefa específica. Para consultas breves ou buscas básicas, as informações neste SKILL.md podem ser suficientes. Para operações complexas, consulte o arquivo de referência apropriado.

## Workflows Comuns

### Workflow 1: Busca Básica de Literatura

1. Identifique conceitos-chave e sinônimos
2. Construa consulta com operadores Boolean e tags de campo
3. Revise resultados iniciais e refine consulta
4. Aplique filtros (data, tipo de artigo, idioma)
5. Exporte resultados para análise

### Workflow 2: Busca de Revisão Sistemática

1. Defina questão de pesquisa usando framework PICO
2. Identifique todos os termos MeSH relevantes e sinônimos
3. Construa estratégia de busca abrangente
4. Pesquise múltiplos bancos de dados (inclua PubMed)
5. Documente estratégia de busca e data
6. Exporte resultados para triagem e revisão

### Workflow 3: Extração Programática de Dados

1. Projete consulta de busca e teste na interface web
2. Implemente busca usando API ESearch
3. Use servidor de histórico para grandes conjuntos de resultados
4. Recupere registros detalhados com EFetch
5. Analise respostas XML/JSON
6. Armazene dados localmente com caching
7. Implemente limitação de taxa e tratamento de erros

### Workflow 4: Descoberta de Citações

1. Comece com artigo conhecido relevante
2. Use Artigos Similares para encontrar trabalho relacionado
3. Verifique artigos que citam (quando disponível)
4. Explore termos MeSH de artigos relevantes
5. Construa novas buscas baseadas em descobertas
6. Use ELink para encontrar entradas de banco de dados relacionadas

### Workflow 5: Monitoramento Contínuo de Literatura

1. Construa consulta de busca abrangente
2. Teste e refine consulta para precisão
3. Salve busca na conta My NCBI
4. Configure alertas por email para novas correspondências
5. Crie feed RSS para monitoramento em leitor de feeds
6. Revise artigos novos regularmente

## Dicas e Melhores Práticas

### Estratégia de Busca
- Comece amplo, depois estreite com tags de campo e filtros
- Inclua sinônimos e termos MeSH para cobertura abrangente
- Use aspas para frases exatas
- Verifique Detalhes de Busca na Busca Avançada para verificar tradução da consulta
- Combine múltiplas buscas usando histórico de busca

### Uso de API
- Obtenha chave API para limites de taxa mais altos (10 req/seg vs 3 req/seg)
- Use servidor de histórico para conjuntos de resultados > 500 artigos
- Implemente backoff exponencial para tratamento de limite de taxa
- Cache resultados localmente para minimizar requisições redundantes
- Sempre inclua header User-Agent descritivo

### Filtragem de Qualidade
- Prefira revisões sistemáticas e meta-análises para evidência sintetizada
- Use filtros de tipo de publicação para encontrar desenhos de estudo específicos
- Filtre por data para pesquisa mais recente
- Aplique filtros de idioma conforme apropriado
- Use filtro de texto completo gratuito para acesso imediato

### Gestão de Citações
- Exporte cedo e frequentemente para evitar perder resultados de busca
- Use formato .nbib para compatibilidade com a maioria dos gerenciadores de referências
- Crie conta My NCBI para coleções permanentes
- Documente estratégias de busca para reprodutibilidade
- Use Coleções para organizar pesquisa por projeto

## Limitações e Considerações

### Cobertura de Banco de Dados
- Principalmente literatura biomédica e de ciências da vida
- Artigos anteriores a 1975 frequentemente carecem de resumos
- Nomes completos de autores disponíveis a partir de 2002
- Resumos em não-inglês disponíveis mas podem exibir padrão em inglês

### Limitações de Busca
- Exibição limitada a máximo 10.000 resultados
- Histórico de busca expira após 8 horas de inatividade
- Clipboard mantém máximo 500 itens com expiração em 8 horas
- Mapeamento automático de termos pode produzir resultados inesperados

### Considerações de API
- Limites de taxa aplicáveis (3-10 requisições/segundo)
- Consultas grandes podem fazer timeout (use servidor de histórico)
- Análise XML necessária para extração de dados detalhados
- Chave API recomendada para uso em produção

### Limitações de Acesso
- PubMed fornece citações e resumos (nem sempre texto completo)
- Acesso a texto completo depende de editora, acesso institucional ou status de acesso aberto
- Disponibilidade de LinkOut varia por periódico e instituição
- Alguns conteúdos requerem assinatura ou pagamento

## Recursos de Suporte

- **Ajuda do PubMed**: https://pubmed.ncbi.nlm.nih.gov/help/
- **Documentação E-utilities**: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- **NLM Help Desk**: 1-888-FIND-NLM (1-888-346-3656)
- **Suporte Técnico**: vog.hin.mln.ibcn@seitilitue
- **Lista de Discussão**: utilities-announce@ncbi.nlm.nih.gov