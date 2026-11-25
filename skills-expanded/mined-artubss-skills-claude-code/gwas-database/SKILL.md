---
name: gwas-database
description: "Consulte o Catálogo GWAS NHGRI-EBI para associações SNP-traço. Pesquise variantes por ID rs, doença/traço, gene, recupere valores de p e estatísticas resumidas, para epidemiologia genética e escores de risco poligênico."
---

# Banco de Dados do Catálogo GWAS

## Visão Geral

O Catálogo GWAS é um repositório abrangente de estudos de associação genômica ampla publicados, mantido pelo Instituto Nacional de Pesquisa do Genoma Humano (NHGRI) e pelo Instituto Europeu de Bioinformática (EBI). O catálogo contém associações SNP-traço curadas de milhares de publicações GWAS, incluindo variantes genéticas, doenças e traços associados, valores de p, tamanhos de efeito e estatísticas resumidas completas para muitos estudos.

## Quando Usar Esta Competência

Esta competência deve ser usada quando as consultas envolvem:

- **Associações de variantes genéticas**: Encontrando SNPs associados a doenças ou traços
- **Buscas de SNP**: Recuperando informações sobre variantes genéticas específicas (IDs rs)
- **Pesquisas de traço/doença**: Descobrindo associações genéticas para fenótipos
- **Associações de genes**: Encontrando variantes em ou perto de genes específicos
- **Estatísticas resumidas de GWAS**: Acessando dados completos de associação genômica ampla
- **Metadados de estudos**: Recuperando informações de publicação e coorte
- **Genética populacional**: Explorando associações específicas de ancestralidade
- **Escores de risco poligênico**: Identificando variantes para modelos de predição de risco
- **Genômica funcional**: Entendendo efeitos de variantes e contexto genômico
- **Revisões sistemáticas**: Síntese abrangente de literatura sobre associações genéticas

## Funcionalidades Principais

### 1. Compreendendo a Estrutura de Dados do Catálogo GWAS

O Catálogo GWAS é organizado em torno de quatro entidades principais:

- **Estudos**: Publicações GWAS com metadados (PMID, autor, detalhes da coorte)
- **Associações**: Associações SNP-traço com evidência estatística (p ≤ 5×10⁻⁸)
- **Variantes**: Marcadores genéticos (SNPs) com coordenadas genômicas e alelos
- **Traços**: Fenótipos e doenças (mapeados para termos de ontologia EFO)

**Identificadores-chave:**
- Acessos de estudos: IDs `GCST` (ex: GCST001234)
- IDs de variantes: números `rs` (ex: rs7903146) ou formato `variant_id`
- IDs de traços: termos EFO (ex: EFO_0001360 para diabetes tipo 2)
- Símbolos de genes: nomes aprovados HGNC (ex: TCF7L2)

### 2. Pesquisas na Interface Web

A interface web em https://www.ebi.ac.uk/gwas/ suporta múltiplos modos de busca:

**Por Variante (ID rs):**
```
rs7903146
```
Retorna todas as associações de traço para este SNP.

**Por Doença/Traço:**
```
type 2 diabetes
Parkinson disease
body mass index
```
Retorna todas as variantes genéticas associadas.

**Por Gene:**
```
APOE
TCF7L2
```
Retorna variantes na região do gene ou próximas.

**Por Região Cromossômica:**
```
10:114000000-115000000
```
Retorna variantes no intervalo genômico especificado.

**Por Publicação:**
```
PMID:20581827
Author: McCarthy MI
GCST001234
```
Retorna detalhes do estudo e todas as associações reportadas.

### 3. Acesso via REST API

O Catálogo GWAS fornece duas APIs REST para acesso programático:

**URLs Base:**
- API do Catálogo GWAS: `https://www.ebi.ac.uk/gwas/rest/api`
- API de Estatísticas Resumidas: `https://www.ebi.ac.uk/gwas/summary-statistics/api`

**Documentação da API:**
- Documentação da API principal: https://www.ebi.ac.uk/gwas/rest/docs/api
- Documentação de estatísticas resumidas: https://www.ebi.ac.uk/gwas/summary-statistics/docs/

**Endpoints Principais:**

1. **Endpoint de estudos** - `/studies/{accessionID}`
   ```python
   import requests

   # Obter um estudo específico
   url = "https://www.ebi.ac.uk/gwas/rest/api/studies/GCST001795"
   response = requests.get(url, headers={"Content-Type": "application/json"})
   study = response.json()
   ```

2. **Endpoint de associações** - `/associations`
   ```python
   # Encontrar associações para uma variante
   variant = "rs7903146"
   url = f"https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/{variant}/associations"
   params = {"projection": "associationBySnp"}
   response = requests.get(url, params=params, headers={"Content-Type": "application/json"})
   associations = response.json()
   ```

3. **Endpoint de variantes** - `/singleNucleotidePolymorphisms/{rsID}`
   ```python
   # Obter detalhes da variante
   url = "https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/rs7903146"
   response = requests.get(url, headers={"Content-Type": "application/json"})
   variant_info = response.json()
   ```

4. **Endpoint de traços** - `/efoTraits/{efoID}`
   ```python
   # Obter informações do traço
   url = "https://www.ebi.ac.uk/gwas/rest/api/efoTraits/EFO_0001360"
   response = requests.get(url, headers={"Content-Type": "application/json"})
   trait_info = response.json()
   ```

### 4. Exemplos de Consultas e Padrões

**Exemplo 1: Encontrar todas as associações para uma doença**
```python
import requests

trait = "EFO_0001360"  # Diabetes tipo 2
base_url = "https://www.ebi.ac.uk/gwas/rest/api"

# Consultar associações para este traço
url = f"{base_url}/efoTraits/{trait}/associations"
response = requests.get(url, headers={"Content-Type": "application/json"})
associations = response.json()

# Processar resultados
for assoc in associations.get('_embedded', {}).get('associations', []):
    variant = assoc.get('rsId')
    pvalue = assoc.get('pvalue')
    risk_allele = assoc.get('strongestAllele')
    print(f"{variant}: p={pvalue}, alelo de risco={risk_allele}")
```

**Exemplo 2: Obter informações de variante e todas as associações de traço**
```python
import requests

variant = "rs7903146"
base_url = "https://www.ebi.ac.uk/gwas/rest/api"

# Obter detalhes da variante
url = f"{base_url}/singleNucleotidePolymorphisms/{variant}"
response = requests.get(url, headers={"Content-Type": "application/json"})
variant_data = response.json()

# Obter todas as associações para esta variante
url = f"{base_url}/singleNucleotidePolymorphisms/{variant}/associations"
params = {"projection": "associationBySnp"}
response = requests.get(url, params=params, headers={"Content-Type": "application/json"})
associations = response.json()

# Extrair nomes de traços e valores de p
for assoc in associations.get('_embedded', {}).get('associations', []):
    trait = assoc.get('efoTrait')
    pvalue = assoc.get('pvalue')
    print(f"Traço: {trait}, valor de p: {pvalue}")
```

**Exemplo 3: Acessar estatísticas resumidas**
```python
import requests

# Consultar API de estatísticas resumidas
base_url = "https://www.ebi.ac.uk/gwas/summary-statistics/api"

# Encontrar associações por traço com limiar de valor de p
trait = "EFO_0001360"  # Diabetes tipo 2
p_upper = "0.000000001"  # p < 1e-9
url = f"{base_url}/traits/{trait}/associations"
params = {
    "p_upper": p_upper,
    "size": 100  # Número de resultados
}
response = requests.get(url, params=params)
results = response.json()

# Processar achados genômica-ampla significantes
for hit in results.get('_embedded', {}).get('associations', []):
    variant_id = hit.get('variant_id')
    chromosome = hit.get('chromosome')
    position = hit.get('base_pair_location')
    pvalue = hit.get('p_value')
    print(f"{chromosome}:{position} ({variant_id}): p={pvalue}")
```

**Exemplo 4: Consultar por região cromossômica**
```python
import requests

# Encontrar variantes em uma região genômica específica
chromosome = "10"
start_pos = 114000000
end_pos = 115000000

base_url = "https://www.ebi.ac.uk/gwas/rest/api"
url = f"{base_url}/singleNucleotidePolymorphisms/search/findByChromBpLocationRange"
params = {
    "chrom": chromosome,
    "bpStart": start_pos,
    "bpEnd": end_pos
}
response = requests.get(url, params=params, headers={"Content-Type": "application/json"})
variants_in_region = response.json()
```

### 5. Trabalhar com Estatísticas Resumidas

O Catálogo GWAS hospeda estatísticas resumidas completas para muitos estudos, fornecendo acesso a todas as variantes testadas (não apenas achados genômica-ampla significantes).

**Métodos de Acesso:**
1. **Download FTP**: http://ftp.ebi.ac.uk/pub/databases/gwas/summary_statistics/
2. **REST API**: Acesso baseado em consulta a estatísticas resumidas
3. **Interface web**: Navegue e baixe pelo site

**Características da API de Estatísticas Resumidas:**
- Filtrar por cromossomo, posição, valor de p
- Consultar variantes específicas em estudos
- Recuperar tamanhos de efeito e frequências de alelos
- Acessar dados harmonizados e padronizados

**Exemplo: Baixar estatísticas resumidas para um estudo**
```python
import requests
import gzip

# Obter estatísticas resumidas disponíveis
base_url = "https://www.ebi.ac.uk/gwas/summary-statistics/api"
url = f"{base_url}/studies/GCST001234"
response = requests.get(url)
study_info = response.json()

# O link de download é fornecido na resposta
# Alternativamente, use FTP:
# ftp://ftp.ebi.ac.uk/pub/databases/gwas/summary_statistics/GCSTXXXXXX/
```

### 6. Integração de Dados e Referência Cruzada

O Catálogo GWAS fornece links para recursos externos:

**Bancos de Dados Genômicos:**
- Ensembl: Anotações de genes e consequências de variantes
- dbSNP: Identificadores de variantes e frequências populacionais
- gnomAD: Frequências de alelos populacionais

**Recursos Funcionais:**
- Open Targets: Associações alvo-doença
- PGS Catalog: Escores de risco poligênico
- UCSC Genome Browser: Contexto genômico

**Recursos de Fenótipo:**
- EFO (Experimental Factor Ontology): Termos de traço padronizados
- OMIM: Relações doença-gene
- Disease Ontology: Hierarquias de doenças

**Seguindo Links em Respostas da API:**
```python
import requests

# As respostas da API incluem _links para recursos relacionados
response = requests.get("https://www.ebi.ac.uk/gwas/rest/api/studies/GCST001234")
study = response.json()

# Seguir link para associações
associations_url = study['_links']['associations']['href']
associations_response = requests.get(associations_url)
```

## Fluxos de Trabalho de Consulta

### Fluxo de Trabalho 1: Explorando Associações Genéticas para uma Doença

1. **Identificar o traço** usando termos EFO ou texto livre:
   - Pesquisar na interface web por nome da doença
   - Observar o ID EFO (ex: EFO_0001360 para diabetes tipo 2)

2. **Consultar associações via API:**
   ```python
   url = f"https://www.ebi.ac.uk/gwas/rest/api/efoTraits/{efo_id}/associations"
   ```

3. **Filtrar por significância e população:**
   - Verificar valores de p (genômica-ampla significante: p ≤ 5×10⁻⁸)
   - Revisar informações de ancestralidade nos metadados de estudo
   - Filtrar por tamanho de amostra ou status descoberta/replicação

4. **Extrair detalhes de variante:**
   - IDs rs para cada associação
   - Alelos de efeito e direções
   - Tamanhos de efeito (odds ratios, coeficientes beta)
   - Frequências de alelos populacionais

5. **Referência cruzada com outros bancos de dados:**
   - Pesquisar consequências de variante em Ensembl
   - Verificar frequências populacionais em gnomAD
   - Explorar função e vias de genes

### Fluxo de Trabalho 2: Investigando uma Variante Genética Específica

1. **Consultar a variante:**
   ```python
   url = f"https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/{rs_id}"
   ```

2. **Recuperar todas as associações de traço:**
   ```python
   url = f"https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/{rs_id}/associations"
   ```

3. **Analisar pleiotropia:**
   - Identificar todos os traços associados com esta variante
   - Revisar direções de efeito em traços
   - Procurar vias biológicas compartilhadas

4. **Verificar contexto genômico:**
   - Determinar genes próximos
   - Identificar se variante está em regiões codificadoras/regulatórias
   - Revisar desequilíbrio de ligação com outras variantes

### Fluxo de Trabalho 3: Análise de Associação Centrada em Gene

1. **Pesquisar por símbolo de gene** na interface web ou:
   ```python
   url = f"https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/search/findByGene"
   params = {"geneName": gene_symbol}
   ```

2. **Recuperar variantes em região de gene:**
   - Obter coordenadas cromossômicas para gene
   - Consultar variantes em região
   - Incluir promotor e regiões regulatórias (estender limites)

3. **Analisar padrões de associação:**
   - Identificar traços associados com variantes neste gene
   - Procurar associações consistentes em estudos
   - Revisar tamanhos de efeito e direções

4. **Interpretação funcional:**
   - Determinar consequências de variante (missense, regulatória, etc)
   - Verificar dados de QTL de expressão (eQTL)
   - Revisar contexto de via e rede

### Fluxo de Trabalho 4: Revisão Sistemática de Evidência Genética

1. **Definir questão de pesquisa:**
   - Traço ou doença específica de interesse
   - Considerações populacionais
   - Requisitos de desenho de estudo

2. **Extração abrangente de variante:**
   - Consultar todas as associações para traço
   - Estabelecer limiar de significância
   - Observar estudos de descoberta e replicação

3. **Avaliação de qualidade:**
   - Revisar tamanhos de amostra de estudo
   - Verificar diversidade populacional
   - Avaliar heterogeneidade em estudos
   - Identificar potenciais vieses

4. **Síntese de dados:**
   - Agregar associações em estudos
   - Realizar meta-análise se aplicável
   - Criar tabelas resumidas
   - Gerar gráficos de Manhattan ou forest plots

5. **Exportação e documentação:**
   - Baixar dados completos de associação
   - Exportar estatísticas resumidas se necessário
   - Documentar estratégia de busca e data
   - Criar scripts de análise reproduzíveis

### Fluxo de Trabalho 5: Acessando e Analisando Estatísticas Resumidas

1. **Identificar estudos com estatísticas resumidas:**
   - Navegar pelo portal de estatísticas resumidas
   - Verificar listagens de diretório FTP
   - Consultar API para estudos disponíveis

2. **Baixar estatísticas resumidas:**
   ```bash
   # Via FTP
   wget ftp://ftp.ebi.ac.uk/pub/databases/gwas/summary_statistics/GCSTXXXXXX/harmonised/GCSTXXXXXX-harmonised.tsv.gz
   ```

3. **Consultar via API para variantes específicas:**
   ```python
   url = f"https://www.ebi.ac.uk/gwas/summary-statistics/api/chromosomes/{chrom}/associations"
   params = {"start": start_pos, "end": end_pos}
   ```

4. **Processar e analisar:**
   - Filtrar por limiares de valor de p
   - Extrair tamanhos de efeito e intervalos de confiança
   - Realizar análises posteriores (fine-mapping, colocalization, etc)

## Formatos de Resposta e Campos de Dados

**Campos-chave em Registros de Associação:**
- `rsId`: Identificador de variante (número rs)
- `strongestAllele`: Alelo de risco para a associação
- `pvalue`: Valor de p da associação
- `pvalueText`: Valor de p como texto (pode incluir desigualdade)
- `orPerCopyNum`: Odds ratio ou coeficiente beta
- `betaNum`: Tamanho de efeito (para traços quantitativos)
- `betaUnit`: Unidade de medida para beta
- `range`: Intervalo de confiança
- `efoTrait`: Nome do traço associado
- `mappedLabel`: Termo de traço mapeado em EFO

**Campos de Metadados de Estudo:**
- `accessionId`: Identificador de estudo GCST
- `pubmedId`: ID do PubMed
- `author`: Primeiro autor
- `publicationDate`: Data de publicação
- `ancestryInitial`: Ancestralidade de população de descoberta
- `ancestryReplication`: Ancestralidade de população de replicação
- `sampleSize`: Tamanho total da amostra

**Paginação:**
Os resultados são paginados (padrão 20 itens por página). Navegue usando:
- Parâmetro `size`: Número de resultados por página
- Parâmetro `page`: Número da página (indexado em 0)
- `_links` em resposta: URLs para páginas anterior/próxima

## Melhores Práticas

### Estratégia de Consulta
- Começar com interface web para identificar termos EFO relevantes e acessos de estudo
- Usar API para extração de dados em massa e análises automatizadas
- Implementar tratamento de paginação para grandes conjuntos de resultados
- Cachear respostas da API para minimizar requisições redundantes

### Interpretação de Dados
- Sempre verificar limiares de valor de p (genômica-ampla: 5×10⁻⁸)
- Revisar informações de ancestralidade para aplicabilidade populacional
- Considerar tamanho de amostra ao avaliar força de evidência
- Verificar replicação em estudos independentes
- Estar ciente de viés do vencedor em estimativas de tamanho de efeito

### Limitação de Taxa e Ética
- Respeitar diretrizes de uso de API (sem requisições excessivas)
- Usar downloads de estatísticas resumidas para análises genômica-ampla
- Implementar atrasos apropriados entre chamadas de API
- Cachear resultados localmente ao executar análises iterativas
- Citar o Catálogo GWAS em publicações

### Considerações de Qualidade de Dados
- O Catálogo GWAS cura associações publicadas (pode conter inconsistências)
- Tamanhos de efeito reportados conforme publicado (pode necessitar harmonização)
- Alguns estudos reportam associações condicionais ou conjuntas
- Verificar sobreposição de estudos ao combinar resultados
- Estar ciente de vieses de seleção e ascertainment

## Exemplo de Integração em Python

Fluxo de trabalho completo para consultar e analisar dados GWAS:

```python
import requests
import pandas as pd
from time import sleep

def query_gwas_catalog(trait_id, p_threshold=5e-8):
    """
    Consultar o Catálogo GWAS para associações de traço

    Args:
        trait_id: Identificador de traço EFO (ex: 'EFO_0001360')
        p_threshold: Limiar de valor de p para filtragem

    Returns:
        pandas DataFrame com resultados de associação
    """
    base_url = "https://www.ebi.ac.uk/gwas/rest/api"
    url = f"{base_url}/efoTraits/{trait_id}/associations"

    headers = {"Content-Type": "application/json"}
    results = []
    page = 0

    while True:
        params = {"page": page, "size": 100}
        response = requests.get(url, params=params, headers=headers)

        if response.status_code != 200:
            break

        data = response.json()
        associations = data.get('_embedded', {}).get('associations', [])

        if not associations:
            break

        for assoc in associations:
            pvalue = assoc.get('pvalue')
            if pvalue and float(pvalue) <= p_threshold:
                results.append({
                    'variant': assoc.get('rsId'),
                    'pvalue': pvalue,
                    'risk_allele': assoc.get('strongestAllele'),
                    'or_beta': assoc.get('orPerCopyNum') or assoc.get('betaNum'),
                    'trait': assoc.get('efoTrait'),
                    'pubmed_id': assoc.get('pubmedId')
                })

        page += 1
        sleep(0.1)  # Limitação de taxa

    return pd.DataFrame(results)

# Exemplo de uso
df = query_gwas_catalog('EFO_0001360')  # Diabetes tipo 2
print(df.head())
print(f"\nTotal de associações: {len(df)}")
print(f"Variantes únicas: {df['variant'].nunique()}")
```

## Recursos

### references/api_reference.md

Documentação abrangente de API incluindo:
- Especificações de endpoint detalhadas para ambas as APIs
- Lista completa de parâmetros de consulta e filtros
- Especificações de formato de resposta e descrições de campos
- Exemplos de consulta avançada e padrões
- Tratamento de erros e solução de problemas
- Integração com bancos de dados externos

Consulte esta referência quando:
- Construir consultas de API complexas
- Compreender estruturas de resposta
- Implementar paginação ou operações em lote
- Solucionar problemas de erros da API
- Explorar opções de filtragem avançada

### Materiais de Treinamento

A equipe do Catálogo GWAS fornece materiais de workshop:
- Repositório GitHub: https://github.com/EBISPOT/GWAS_Catalog-workshop
- Notebooks Jupyter com consultas de exemplo
- Integração Google Colab para execução em nuvem

## Notas Importantes

### Atualizações de Dados
- O Catálogo GWAS é atualizado regularmente com novas publicações
- Re-executar consultas periodicamente para cobertura abrangente
- Estatísticas resumidas são adicionadas conforme estudos lançam dados
- Mapeamentos de EFO podem ser atualizados ao longo do tempo

### Requisitos de Citação
Ao usar dados do Catálogo GWAS, cite:
- Sollis E, et al. (2023) The NHGRI-EBI GWAS Catalog: knowledgebase and deposition resource. Nucleic Acids Research. PMID: 37953337
- Inclua data de acesso e versão quando disponível
- Cite estudos originais ao discutir descobertas específicas

### Limitações
- Nem todas as publicações GWAS estão incluídas (critérios de curação aplicáveis)
- Estatísticas resumidas completas disponíveis para subconjunto de estudos
- Tamanhos de efeito podem exigir harmonização em estudos
- Diversidade populacional está crescendo, mas historicamente limitada
- Algumas associações representam efeitos condicionais ou conjuntos

### Acesso a Dados
- Interface web: Livre, sem registro necessário
- APIs REST: Livre, sem chave API necessária
- Downloads FTP: Acesso aberto
- Limitação de taxa aplica-se a API (seja respeitoso)

## Recursos Adicionais

- **Site do Catálogo GWAS**: https://www.ebi.ac.uk/gwas/
- **Documentação**: https://www.ebi.ac.uk/gwas/docs
- **Documentação de API**: https://www.ebi.ac.uk/gwas/rest/docs/api
- **API de Estatísticas Resumidas**: https://www.ebi.ac.uk/gwas/summary-statistics/docs/
- **Site FTP**: http://ftp.ebi.ac.uk/pub/databases/gwas/
- **Materiais de treinamento**: https://github.com/EBISPOT/GWAS_Catalog-workshop
- **PGS Catalog** (escores poligênicos): https://www.pgscatalog.org/
- **Ajuda e suporte**: gwas-info@ebi.ac.uk