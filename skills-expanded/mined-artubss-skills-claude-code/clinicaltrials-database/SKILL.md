---
name: clinicaltrials-database
description: "Consulte ClinicalTrials.gov via API v2. Pesquise ensaios por condição, fármaco, localização, status ou fase. Recupere detalhes de ensaios por NCT ID, exporte dados, para pesquisa clínica e compatibilidade de pacientes."
---

# Banco de Dados ClinicalTrials.gov

## Visão Geral

ClinicalTrials.gov é um registro abrangente de estudos clínicos realizados em todo o mundo, mantido pela Biblioteca Nacional de Medicina dos EUA. Acesse API v2 para pesquisar ensaios, recuperar informações detalhadas de estudos, filtrar por vários critérios e exportar dados para análise. A API é pública (sem autenticação necessária) com limite de ~50 requisições por minuto, oferecendo suporte aos formatos JSON e CSV.

## Quando Usar Esta Habilidade

Esta habilidade deve ser usada ao trabalhar com dados de ensaios clínicos em cenários como:

- **Compatibilidade de pacientes** - Encontrar ensaios recrutando para condições específicas ou populações de pacientes
- **Análise de pesquisa** - Analisar tendências de ensaios clínicos, resultados ou desenhos de estudo
- **Pesquisa de fármaco/intervenção** - Identificar ensaios testando fármacos ou intervenções específicas
- **Pesquisas geográficas** - Localizar ensaios em locais ou regiões específicas
- **Rastreamento de patrocinador/organização** - Encontrar ensaios conduzidos por instituições específicas
- **Exportação de dados** - Extrair dados de ensaios clínicos para análise ou relatório adicional
- **Monitoramento de ensaios** - Rastrear atualizações de status ou resultados para ensaios específicos
- **Triagem de elegibilidade** - Revisar critérios de inclusão/exclusão para ensaios

## Início Rápido

### Consulta de Pesquisa Básica

Pesquise ensaios clínicos usando o script auxiliar:

```bash
cd scientific-databases/clinicaltrials-database/scripts
python3 query_clinicaltrials.py
```

Ou use Python diretamente com a biblioteca `requests`:

```python
import requests

url = "https://clinicaltrials.gov/api/v2/studies"
params = {
    "query.cond": "breast cancer",
    "filter.overallStatus": "RECRUITING",
    "pageSize": 10
}

response = requests.get(url, params=params)
data = response.json()

print(f"Found {data['totalCount']} trials")
```

### Recuperar Ensaio Específico

Obtenha informações detalhadas sobre um ensaio usando seu NCT ID:

```python
import requests

nct_id = "NCT04852770"
url = f"https://clinicaltrials.gov/api/v2/studies/{nct_id}"

response = requests.get(url)
study = response.json()

# Access specific modules
title = study['protocolSection']['identificationModule']['briefTitle']
status = study['protocolSection']['statusModule']['overallStatus']
```

## Capacidades Principais

### 1. Pesquisa por Condição/Doença

Encontre ensaios estudando condições médicas ou doenças específicas usando o parâmetro `query.cond`.

**Exemplo: Encontrar ensaios recrutando para diabetes**

```python
from scripts.query_clinicaltrials import search_studies

results = search_studies(
    condition="type 2 diabetes",
    status="RECRUITING",
    page_size=20,
    sort="LastUpdatePostDate:desc"
)

print(f"Found {results['totalCount']} recruiting diabetes trials")
for study in results['studies']:
    protocol = study['protocolSection']
    nct_id = protocol['identificationModule']['nctId']
    title = protocol['identificationModule']['briefTitle']
    print(f"{nct_id}: {title}")
```

**Casos de uso comuns:**
- Encontrar ensaios para doenças raras
- Identificar ensaios para condições comórbidas
- Rastrear disponibilidade de ensaios para diagnósticos específicos

### 2. Pesquisa por Intervenção/Fármaco

Pesquise ensaios testando intervenções, fármacos, dispositivos ou procedimentos específicos usando o parâmetro `query.intr`.

**Exemplo: Encontrar ensaios Fase 3 testando Pembrolizumab**

```python
from scripts.query_clinicaltrials import search_studies

results = search_studies(
    intervention="Pembrolizumab",
    status=["RECRUITING", "ACTIVE_NOT_RECRUITING"],
    page_size=50
)

# Filter by phase in results
phase3_trials = [
    study for study in results['studies']
    if 'PHASE3' in study['protocolSection'].get('designModule', {}).get('phases', [])
]
```

**Casos de uso comuns:**
- Rastreamento de desenvolvimento de fármacos
- Inteligência competitiva para empresas farmacêuticas
- Pesquisa de opções de tratamento para clínicos

### 3. Pesquisa Geográfica

Encontre ensaios em locais específicos usando o parâmetro `query.locn`.

**Exemplo: Encontrar ensaios de câncer em Nova York**

```python
from scripts.query_clinicaltrials import search_studies

results = search_studies(
    condition="cancer",
    location="New York",
    status="RECRUITING",
    page_size=100
)

# Extract location details
for study in results['studies']:
    locations_module = study['protocolSection'].get('contactsLocationsModule', {})
    locations = locations_module.get('locations', [])
    for loc in locations:
        if 'New York' in loc.get('city', ''):
            print(f"{loc['facility']}: {loc['city']}, {loc.get('state', '')}")
```

**Casos de uso comuns:**
- Referência de pacientes para ensaios locais
- Análise de distribuição geográfica de ensaios
- Seleção de sites para novos ensaios

### 4. Pesquisa por Patrocinador/Organização

Encontre ensaios conduzidos por organizações específicas usando o parâmetro `query.spons`.

**Exemplo: Encontrar ensaios patrocinados pelo NCI**

```python
from scripts.query_clinicaltrials import search_studies

results = search_studies(
    sponsor="National Cancer Institute",
    page_size=100
)

# Extract sponsor information
for study in results['studies']:
    sponsor_module = study['protocolSection']['sponsorCollaboratorsModule']
    lead_sponsor = sponsor_module['leadSponsor']['name']
    collaborators = sponsor_module.get('collaborators', [])
    print(f"Lead: {lead_sponsor}")
    if collaborators:
        print(f"  Collaborators: {', '.join([c['name'] for c in collaborators])}")
```

**Casos de uso comuns:**
- Rastreamento de portfólios de pesquisa institucional
- Análise de prioridades de organizações de financiamento
- Identificação de oportunidades de colaboração

### 5. Filtrar por Status do Estudo

Filtre ensaios por status de recrutamento ou conclusão usando o parâmetro `filter.overallStatus`.

**Valores de status válidos:**
- `RECRUITING` - Atualmente recrutando participantes
- `NOT_YET_RECRUITING` - Ainda não aberto para recrutamento
- `ENROLLING_BY_INVITATION` - Apenas recrutando por convite
- `ACTIVE_NOT_RECRUITING` - Ativo mas não recrutando mais
- `SUSPENDED` - Temporariamente suspenso
- `TERMINATED` - Parado prematuramente
- `COMPLETED` - Estudo foi concluído
- `WITHDRAWN` - Retirado antes do recrutamento

**Exemplo: Encontrar ensaios completados recentemente com resultados**

```python
from scripts.query_clinicaltrials import search_studies

results = search_studies(
    condition="alzheimer disease",
    status="COMPLETED",
    sort="LastUpdatePostDate:desc",
    page_size=50
)

# Filter for trials with results
trials_with_results = [
    study for study in results['studies']
    if study.get('hasResults', False)
]

print(f"Found {len(trials_with_results)} completed trials with results")
```

### 6. Recuperar Informações Detalhadas do Estudo

Obtenha informações abrangentes sobre ensaios específicos, incluindo critérios de elegibilidade, desfechos, contatos e locais.

**Exemplo: Extrair critérios de elegibilidade**

```python
from scripts.query_clinicaltrials import get_study_details

study = get_study_details("NCT04852770")
eligibility = study['protocolSection']['eligibilityModule']

print(f"Eligible Ages: {eligibility.get('minimumAge')} - {eligibility.get('maximumAge')}")
print(f"Eligible Sex: {eligibility.get('sex')}")
print(f"\nInclusion Criteria:")
print(eligibility.get('eligibilityCriteria'))
```

**Exemplo: Extrair informações de contato**

```python
from scripts.query_clinicaltrials import get_study_details

study = get_study_details("NCT04852770")
contacts_module = study['protocolSection']['contactsLocationsModule']

# Overall contacts
if 'centralContacts' in contacts_module:
    for contact in contacts_module['centralContacts']:
        print(f"Contact: {contact.get('name')}")
        print(f"Phone: {contact.get('phone')}")
        print(f"Email: {contact.get('email')}")

# Study locations
if 'locations' in contacts_module:
    for location in contacts_module['locations']:
        print(f"\nFacility: {location.get('facility')}")
        print(f"City: {location.get('city')}, {location.get('state')}")
        if location.get('status'):
            print(f"Status: {location['status']}")
```

### 7. Paginação e Recuperação de Dados em Massa

Manipule grandes conjuntos de resultados com eficiência usando paginação.

**Exemplo: Recuperar todos os ensaios correspondentes**

```python
from scripts.query_clinicaltrials import search_with_all_results

# Get all trials (automatically handles pagination)
all_trials = search_with_all_results(
    condition="rare disease",
    status="RECRUITING"
)

print(f"Retrieved {len(all_trials)} total trials")
```

**Exemplo: Paginação manual com controle**

```python
from scripts.query_clinicaltrials import search_studies

all_studies = []
page_token = None
max_pages = 10  # Limit to avoid excessive requests

for page in range(max_pages):
    results = search_studies(
        condition="cancer",
        page_size=1000,  # Max page size
        page_token=page_token
    )

    all_studies.extend(results['studies'])

    # Check for next page
    page_token = results.get('pageToken')
    if not page_token:
        break

print(f"Retrieved {len(all_studies)} studies across {page + 1} pages")
```

### 8. Exportar Dados para CSV

Exporte dados de ensaios para formato CSV para análise em software de planilha ou ferramentas de análise de dados.

**Exemplo: Exportar para arquivo CSV**

```python
from scripts.query_clinicaltrials import search_studies

# Request CSV format
results = search_studies(
    condition="heart disease",
    status="RECRUITING",
    format="csv",
    page_size=1000
)

# Save to file
with open("heart_disease_trials.csv", "w") as f:
    f.write(results)

print("Data exported to heart_disease_trials.csv")
```

**Nota:** Formato CSV retorna uma string em vez de dicionário JSON.

### 9. Extrair e Resumir Informações do Estudo

Extraia informações-chave para visão geral rápida ou relatório.

**Exemplo: Criar resumo de ensaio**

```python
from scripts.query_clinicaltrials import get_study_details, extract_study_summary

# Get details and extract summary
study = get_study_details("NCT04852770")
summary = extract_study_summary(study)

print(f"NCT ID: {summary['nct_id']}")
print(f"Title: {summary['title']}")
print(f"Status: {summary['status']}")
print(f"Phase: {', '.join(summary['phase'])}")
print(f"Enrollment: {summary['enrollment']}")
print(f"Last Update: {summary['last_update']}")
print(f"\nBrief Summary:\n{summary['brief_summary']}")
```

### 10. Estratégias de Consulta Combinada

Combine múltiplos filtros para pesquisas direcionadas.

**Exemplo: Pesquisa com múltiplos critérios**

```python
from scripts.query_clinicaltrials import search_studies

# Find Phase 2/3 immunotherapy trials for lung cancer in California
results = search_studies(
    condition="lung cancer",
    intervention="immunotherapy",
    location="California",
    status=["RECRUITING", "NOT_YET_RECRUITING"],
    page_size=100
)

# Further filter by phase
phase2_3_trials = [
    study for study in results['studies']
    if any(phase in ['PHASE2', 'PHASE3']
           for phase in study['protocolSection'].get('designModule', {}).get('phases', []))
]

print(f"Found {len(phase2_3_trials)} Phase 2/3 immunotherapy trials")
```

## Recursos

### scripts/query_clinicaltrials.py

Script Python abrangente fornecendo funções auxiliares para padrões de consulta comuns:

- `search_studies()` - Pesquise ensaios com vários filtros
- `get_study_details()` - Recupere informações completas para um ensaio específico
- `search_with_all_results()` - Pagine automaticamente através de todos os resultados
- `extract_study_summary()` - Extraia informações-chave para visão geral rápida

Execute o script diretamente para exemplo de uso:

```bash
python3 scripts/query_clinicaltrials.py
```

### references/api_reference.md

Documentação detalhada da API incluindo:

- Especificações completas de endpoint
- Todos os parâmetros de consulta e valores válidos
- Estrutura de dados de resposta e módulos
- Casos de uso comuns com exemplos de código
- Manipulação de erros e melhores práticas
- Padrões de dados (datas ISO 8601, markdown CommonMark)

Carregue esta referência ao trabalhar com recursos de API desconhecidos ou solucionar problemas.

## Melhores Práticas

### Gerenciamento de Limite de Taxa

A API tem um limite de taxa de aproximadamente 50 requisições por minuto. Para recuperação de dados em massa:

1. Use o tamanho máximo de página (1000) para minimizar requisições
2. Implemente backoff exponencial em erros de limite de taxa (status 429)
3. Adicione atrasos entre requisições para coleta de dados em larga escala

```python
import time
import requests

def search_with_rate_limit(params):
    try:
        response = requests.get("https://clinicaltrials.gov/api/v2/studies", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            print("Rate limited. Waiting 60 seconds...")
            time.sleep(60)
            return search_with_rate_limit(params)  # Retry
        raise
```

### Navegação de Estrutura de Dados

A resposta da API tem uma estrutura aninhada. Caminhos-chave para informações comuns:

- **NCT ID**: `study['protocolSection']['identificationModule']['nctId']`
- **Título**: `study['protocolSection']['identificationModule']['briefTitle']`
- **Status**: `study['protocolSection']['statusModule']['overallStatus']`
- **Fase**: `study['protocolSection']['designModule']['phases']`
- **Elegibilidade**: `study['protocolSection']['eligibilityModule']`
- **Locais**: `study['protocolSection']['contactsLocationsModule']['locations']`
- **Intervenções**: `study['protocolSection']['armsInterventionsModule']['interventions']`

### Manipulação de Erros

Sempre implemente manipulação apropriada de erros para requisições de rede:

```python
import requests

try:
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e.response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
except ValueError as e:
    print(f"JSON decode error: {e}")
```

### Manipulação de Dados Faltantes

Nem todos os ensaios têm informações completas. Sempre verifique a existência de campo:

```python
# Safe navigation with .get()
phases = study['protocolSection'].get('designModule', {}).get('phases', [])
enrollment = study['protocolSection'].get('designModule', {}).get('enrollmentInfo', {}).get('count', 'N/A')

# Check before accessing
if 'resultsSection' in study:
    # Process results
    pass
```

## Especificações Técnicas

- **URL Base**: `https://clinicaltrials.gov/api/v2`
- **Autenticação**: Não necessária (API pública)
- **Limite de Taxa**: ~50 requisições/minuto por IP
- **Formatos de Resposta**: JSON (padrão), CSV
- **Tamanho Máximo de Página**: 1000 estudos por requisição
- **Formato de Data**: ISO 8601
- **Formato de Texto**: Markdown CommonMark para campos de texto rico
- **Versão da API**: 2.0 (lançada em março de 2024)
- **Especificação da API**: OpenAPI 3.0

Para detalhes técnicos completos, consulte `references/api_reference.md`.