---
name: uspto-database
description: "Acesse APIs do USPTO para buscas de patentes/marcas, histórico de exame (PEDS), cessões, citações, office actions, TSDR, para análise de PI e buscas de anterioridade."
---

# Banco de Dados USPTO

## Visão Geral

O USPTO fornece APIs especializadas para dados de patentes e marcas. Busque patentes por palavras-chave/inventores/cessionários, recupere histórico de exame via PEDS, rastreie cessões, analise citações e office actions, acesse TSDR para marcas, para análise de PI e buscas de anterioridade.

## Quando Usar Esta Habilidade

Esta habilidade deve ser usada quando:

- **Busca de Patentes**: Encontrar patentes por palavras-chave, inventores, cessionários, classificações ou datas
- **Detalhes da Patente**: Recuperar dados completos de patentes incluindo reivindicações, resumos, citações
- **Busca de Marcas**: Consultar marcas por número de série ou número de registro
- **Status de Marca**: Verificar status da marca, propriedade e histórico de processamento
- **Histórico de Exame**: Acessar dados de processamento de patentes do PEDS (Patent Examination Data System)
- **Office Actions**: Recuperar texto de office action, citações e rejeições
- **Cessões**: Rastrear transferências de propriedade de patentes/marcas
- **Citações**: Analisar citações de patentes (diretas e reversas)
- **Litigação**: Acessar registros de litígios de patentes
- **Análise de Portfólio**: Analisar portfólios de patentes/marcas para empresas ou inventores

## Ecossistema de APIs do USPTO

O USPTO fornece múltiplas APIs especializadas para diferentes necessidades de dados:

### APIs Principais

1. **PatentSearch API** - Busca de patentes moderna baseada em ElasticSearch (substituiu PatentsView herdado em maio de 2025)
   - Busque patentes por palavras-chave, inventores, cessionários, classificações, datas
   - Acesso a dados de patentes até 30 de junho de 2025
   - Limite de taxa de 45 requisições/minuto
   - **URL Base**: `https://search.patentsview.org/api/v1/`

2. **PEDS (Patent Examination Data System)** - Histórico de exame de patentes
   - Status da aplicação e histórico de transações de 1981-presente
   - Datas de office action e eventos de exame
   - Use a biblioteca Python `uspto-opendata-python`
   - **Substitui**: PAIR Bulk Data (PBD) - descontinuado

3. **TSDR (Trademark Status & Document Retrieval)** - Dados de marcas
   - Status de marca, propriedade, histórico de processamento
   - Busque por número de série ou número de registro
   - **URL Base**: `https://tsdrapi.uspto.gov/ts/cd/`

### APIs Adicionais

4. **Patent Assignment Search** - Registros de propriedade e transferências
5. **Trademark Assignment Search** - Alterações de propriedade de marcas
6. **Enriched Citation API** - Análise de citações de patentes
7. **Office Action Text Retrieval** - Texto completo de office actions
8. **Office Action Citations** - Citações de office actions
9. **Office Action Rejection** - Motivos e tipos de rejeição
10. **PTAB API** - Procedimentos do Patent Trial and Appeal Board
11. **Patent Litigation Cases** - Dados de litígios em cortes federais de distrito
12. **Cancer Moonshot Data Set** - Conjunto de dados de patentes relacionadas a câncer

## Início Rápido

### Registro de Chave de API

Todas as APIs do USPTO requerem uma chave de API. Registre-se em:
**https://account.uspto.gov/api-manager/**

Defina a chave de API como uma variável de ambiente:
```bash
export USPTO_API_KEY="sua_chave_api_aqui"
```

### Scripts Auxiliares

Esta habilidade inclui scripts Python para operações comuns:

- **`scripts/patent_search.py`** - Cliente da PatentSearch API para buscar patentes
- **`scripts/peds_client.py`** - Cliente PEDS para histórico de exame
- **`scripts/trademark_client.py`** - Cliente TSDR para dados de marcas

## Tarefa 1: Buscando Patentes

### Usando a PatentSearch API

A PatentSearch API usa uma linguagem de consulta JSON com vários operadores para buscas flexíveis.

#### Exemplos Básicos de Busca de Patentes

**Busque por palavras-chave no resumo:**
```python
from scripts.patent_search import PatentSearchClient

client = PatentSearchClient()

# Busque patentes de aprendizado de máquina
results = client.search_patents({
    "patent_abstract": {"_text_all": ["machine", "learning"]}
})

for patent in results['patents']:
    print(f"{patent['patent_number']}: {patent['patent_title']}")
```

**Busque por inventor:**
```python
results = client.search_by_inventor("John Smith")
```

**Busque por cessionário/empresa:**
```python
results = client.search_by_assignee("Google")
```

**Busque por intervalo de datas:**
```python
results = client.search_by_date_range("2024-01-01", "2024-12-31")
```

**Busque por classificação CPC:**
```python
results = client.search_by_classification("H04N")  # Tecnologia de vídeo/imagem
```

#### Busca Avançada de Patentes

Combine múltiplos critérios com operadores lógicos:

```python
results = client.advanced_search(
    keywords=["artificial", "intelligence"],
    assignee="Microsoft",
    start_date="2023-01-01",
    end_date="2024-12-31",
    cpc_codes=["G06N", "G06F"]  # Classificações de IA e computação
)
```

#### Uso Direto da API

Para consultas complexas, use a API diretamente:

```python
import requests

url = "https://search.patentsview.org/api/v1/patent"
headers = {
    "X-Api-Key": "YOUR_API_KEY",
    "Content-Type": "application/json"
}

query = {
    "q": {
        "_and": [
            {"patent_date": {"_gte": "2024-01-01"}},
            {"assignee_organization": {"_text_any": ["Google", "Alphabet"]}},
            {"cpc_subclass_id": ["G06N", "H04N"]}
        ]
    },
    "f": ["patent_number", "patent_title", "patent_date", "inventor_name"],
    "s": [{"patent_date": "desc"}],
    "o": {"per_page": 100, "page": 1}
}

response = requests.post(url, headers=headers, json=query)
results = response.json()
```

### Operadores de Consulta

- **Igualdade**: `{"field": "value"}` ou `{"field": {"_eq": "value"}}`
- **Comparação**: `_gt`, `_gte`, `_lt`, `_lte`, `_neq`
- **Busca de texto**: `_text_all`, `_text_any`, `_text_phrase`
- **Correspondência de string**: `_begins`, `_contains`
- **Lógica**: `_and`, `_or`, `_not`

**Melhor Prática**: Use operadores `_text_*` para campos de texto (mais eficiente que `_contains` ou `_begins`)

### Endpoints Disponíveis de Patentes

- `/patent` - Patentes concedidas
- `/publication` - Publicações de pré-concessão
- `/inventor` - Informações de inventor
- `/assignee` - Informações de cessionário
- `/cpc_subclass`, `/cpc_at_issue` - Classificações CPC
- `/uspc` - Classificação de Patentes dos EUA
- `/ipc` - Classificação de Patentes Internacional
- `/claims`, `/brief_summary_text`, `/detail_description_text` - Dados textuais (beta)

### Documentação de Referência

Consulte `references/patentsearch_api.md` para documentação completa da PatentSearch API incluindo:
- Todos os endpoints disponíveis
- Referência completa de campos
- Sintaxe de consulta e exemplos
- Formatos de resposta
- Limites de taxa e melhores práticas

## Tarefa 2: Recuperando Dados de Exame de Patentes

### Usando PEDS (Patent Examination Data System)

PEDS fornece histórico abrangente de processamento incluindo eventos de transação, mudanças de status e linha do tempo de exame.

#### Instalação

```bash
uv pip install uspto-opendata-python
```

#### Uso Básico de PEDS

**Obtenha dados da aplicação:**
```python
from scripts.peds_client import PEDSHelper

helper = PEDSHelper()

# Por número de aplicação
app_data = helper.get_application("16123456")
print(f"Título: {app_data['title']}")
print(f"Status: {app_data['app_status']}")

# Por número de patente
patent_data = helper.get_patent("11234567")
```

**Obtenha histórico de transações:**
```python
transactions = helper.get_transaction_history("16123456")

for trans in transactions:
    print(f"{trans['date']}: {trans['code']} - {trans['description']}")
```

**Obtenha office actions:**
```python
office_actions = helper.get_office_actions("16123456")

for oa in office_actions:
    if oa['code'] == 'CTNF':
        print(f"Rejeição não-final: {oa['date']}")
    elif oa['code'] == 'CTFR':
        print(f"Rejeição final: {oa['date']}")
    elif oa['code'] == 'NOA':
        print(f"Aviso de permitimento: {oa['date']}")
```

**Obtenha resumo de status:**
```python
summary = helper.get_status_summary("16123456")

print(f"Status atual: {summary['current_status']}")
print(f"Data de depósito: {summary['filing_date']}")
print(f"Pendência: {summary['pendency_days']} dias")

if summary['is_patented']:
    print(f"Número de patente: {summary['patent_number']}")
    print(f"Data de concessão: {summary['issue_date']}")
```

#### Análise de Processamento

Analise padrões de processamento:

```python
analysis = helper.analyze_prosecution("16123456")

print(f"Total de office actions: {analysis['total_office_actions']}")
print(f"Rejeições não-finais: {analysis['non_final_rejections']}")
print(f"Rejeições finais: {analysis['final_rejections']}")
print(f"Permitida: {analysis['allowance']}")
print(f"Respostas enviadas: {analysis['responses']}")
```

### Códigos Comuns de Transação

- **CTNF** - Rejeição não-final enviada
- **CTFR** - Rejeição final enviada
- **NOA** - Aviso de permitimento enviado
- **WRIT** - Resposta enviada
- **ISS.FEE** - Pagamento de taxa de concessão
- **ABND** - Aplicação abandonada
- **AOPF** - Office action enviado

### Documentação de Referência

Consulte `references/peds_api.md` para documentação completa de PEDS incluindo:
- Todos os campos de dados disponíveis
- Referência de códigos de transação
- Uso de biblioteca Python
- Exemplos de análise de portfólio

## Tarefa 3: Buscando e Monitorando Marcas

### Usando TSDR (Trademark Status & Document Retrieval)

Acesse status de marca, propriedade e histórico de processamento.

#### Uso Básico de Marca

**Obtenha marca por número de série:**
```python
from scripts.trademark_client import TrademarkClient

client = TrademarkClient()

# Por número de série
tm_data = client.get_trademark_by_serial("87654321")

# Por número de registro
tm_data = client.get_trademark_by_registration("5678901")
```

**Obtenha status de marca:**
```python
status = client.get_trademark_status("87654321")

print(f"Marca: {status['mark_text']}")
print(f"Status: {status['status']}")
print(f"Data de depósito: {status['filing_date']}")

if status['is_registered']:
    print(f"Número de registro: {status['registration_number']}")
    print(f"Data de registro: {status['registration_date']}")
```

**Verifique saúde da marca:**
```python
health = client.check_trademark_health("87654321")

print(f"Marca: {health['mark']}")
print(f"Status: {health['status']}")

for alert in health['alerts']:
    print(alert)

if health['needs_attention']:
    print("⚠️  Esta marca precisa de atenção!")
```

#### Monitoramento de Portfólio de Marcas

Monitore múltiplas marcas:

```python
def monitor_portfolio(serial_numbers, api_key):
    """Monitore a saúde do portfólio de marcas."""
    client = TrademarkClient(api_key)

    results = {
        'active': [],
        'pending': [],
        'problems': []
    }

    for sn in serial_numbers:
        health = client.check_trademark_health(sn)

        if 'REGISTERED' in health['status']:
            results['active'].append(health)
        elif 'PENDING' in health['status'] or 'PUBLISHED' in health['status']:
            results['pending'].append(health)
        elif health['needs_attention']:
            results['problems'].append(health)

    return results
```

### Status Comuns de Marca

- **REGISTERED** - Marca registrada ativa
- **PENDING** - Em exame
- **PUBLISHED FOR OPPOSITION** - Em período de oposição
- **ABANDONED** - Aplicação abandonada
- **CANCELLED** - Registro cancelado
- **SUSPENDED** - Exame suspenso
- **REGISTERED AND RENEWED** - Registro renovado

### Documentação de Referência

Consulte `references/trademark_api.md` para documentação completa de APIs de marca incluindo:
- Referência da API TSDR
- API de Busca de Cessão de Marca
- Todos os códigos de status
- Acesso ao histórico de processamento
- Rastreamento de propriedade

## Tarefa 4: Rastreando Cessões e Propriedade

### Cessões de Patentes e Marcas

Tanto patentes quanto marcas têm APIs de Busca de Cessão para rastrear mudanças de propriedade.

#### API de Cessão de Patente

**URL Base**: `https://assignment-api.uspto.gov/patent/v1.4/`

**Busque por número de patente:**
```python
import requests
import xml.etree.ElementTree as ET

def get_patent_assignments(patent_number, api_key):
    url = f"https://assignment-api.uspto.gov/patent/v1.4/assignment/patent/{patent_number}"
    headers = {"X-Api-Key": api_key}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text  # Retorna XML

assignments_xml = get_patent_assignments("11234567", api_key)
root = ET.fromstring(assignments_xml)

for assignment in root.findall('.//assignment'):
    recorded_date = assignment.find('recordedDate').text
    assignor = assignment.find('.//assignor/name').text
    assignee = assignment.find('.//assignee/name').text
    conveyance = assignment.find('conveyanceText').text

    print(f"{recorded_date}: {assignor} → {assignee}")
    print(f"  Tipo: {conveyance}\n")
```

**Busque por nome de empresa:**
```python
def find_company_patents(company_name, api_key):
    url = "https://assignment-api.uspto.gov/patent/v1.4/assignment/search"
    headers = {"X-Api-Key": api_key}
    data = {"criteria": {"assigneeName": company_name}}

    response = requests.post(url, headers=headers, json=data)
    return response.text
```

### Tipos Comuns de Cessão

- **ASSIGNMENT OF ASSIGNORS INTEREST** - Transferência de propriedade
- **SECURITY AGREEMENT** - Interesse de garantia/segurança
- **MERGER** - Fusão corporativa
- **CHANGE OF NAME** - Alteração de nome
- **ASSIGNMENT OF PARTIAL INTEREST** - Propriedade parcial

## Tarefa 5: Acessando Dados Adicionais do USPTO

### Office Actions, Citações e Litigação

Múltiplas APIs especializadas fornecem dados adicionais de patentes.

#### Recuperação de Texto de Office Action

Recupere o texto completo de office actions usando número de aplicação. Integre com PEDS para identificar quais office actions existem, depois recupere o texto completo.

#### API de Citação Enriquecida

Analise citações de patentes:
- Citações diretas (patentes que citam esta patente)
- Citações reversas (anterioridade citada)
- Citações do examinador vs. do solicitante
- Contexto de citação

#### API de Casos de Litigação de Patentes

Acesse registros de litigação de patentes em cortes federais de distrito:
- 74.623+ registros de litigação
- Patentes questionadas
- Partes e foros
- Resultados de casos

#### API PTAB

Procedimentos do Patent Trial and Appeal Board:
- Revisão inter partes (IPR)
- Revisão pós-concessão (PGR)
- Decisões de apelação

### Documentação de Referência

Consulte `references/additional_apis.md` para documentação abrangente sobre:
- API de Citação Enriquecida
- APIs de Office Action (Texto, Citações, Rejeições)
- API de Casos de Litigação de Patentes
- API PTAB
- Conjunto de Dados Cancer Moonshot
- Códigos de Status/Evento do OCE

## Exemplo de Análise Completa

### Análise Abrangente de Patente

Combine múltiplas APIs para inteligência de patentes completa:

```python
def comprehensive_patent_analysis(patent_number, api_key):
    """
    Análise completa de patente usando múltiplas APIs do USPTO.
    """
    from scripts.patent_search import PatentSearchClient
    from scripts.peds_client import PEDSHelper

    results = {}

    # 1. Obtenha detalhes da patente
    patent_client = PatentSearchClient(api_key)
    patent_data = patent_client.get_patent(patent_number)
    results['patent'] = patent_data

    # 2. Obtenha histórico de exame
    peds = PEDSHelper()
    results['prosecution'] = peds.analyze_prosecution(patent_number)
    results['status'] = peds.get_status_summary(patent_number)

    # 3. Obtenha histórico de cessão
    import requests
    assign_url = f"https://assignment-api.uspto.gov/patent/v1.4/assignment/patent/{patent_number}"
    assign_resp = requests.get(assign_url, headers={"X-Api-Key": api_key})
    results['assignments'] = assign_resp.text if assign_resp.status_code == 200 else None

    # 4. Analise resultados
    print(f"\n=== Análise da Patente {patent_number} ===\n")
    print(f"Título: {patent_data['patent_title']}")
    print(f"Cessionário: {', '.join(patent_data.get('assignee_organization', []))}")
    print(f"Data de Concessão: {patent_data['patent_date']}")

    print(f"\nProcessamento:")
    print(f"  Office Actions: {results['prosecution']['total_office_actions']}")
    print(f"  Rejeições: {results['prosecution']['non_final_rejections']} não-finais, {results['prosecution']['final_rejections']} finais")
    print(f"  Pendência: {results['prosecution']['pendency_days']} dias")

    # Analise citações
    if 'cited_patent_number' in patent_data:
        print(f"\nCitações:")
        print(f"  Cita: {len(patent_data['cited_patent_number'])} patentes")
    if 'citedby_patent_number' in patent_data:
        print(f"  Citada por: {len(patent_data['citedby_patent_number'])} patentes")

    return results
```

## Melhores Práticas

1. **Gerenciamento de Chave de API**
   - Armazene chave de API em variáveis de ambiente
   - Nunca faça commit de chaves no controle de versão
   - Use a mesma chave em todas as APIs do USPTO

2. **Limite de Taxa**
   - PatentSearch: 45 requisições/minuto
   - Implemente backoff exponencial para erros de limite de taxa
   - Cache respostas quando possível

3. **Otimização de Consulta**
   - Use operadores `_text_*` para campos de texto (mais eficiente)
   - Solicite apenas campos necessários para reduzir tamanho de resposta
   - Use intervalos de datas para estreitar buscas

4. **Manipulação de Dados**
   - Nem todos os campos são preenchidos para todas as patentes/marcas
   - Trate dados ausentes adequadamente
   - Analise datas consistentemente

5. **Combinando APIs**
   - Use PatentSearch para descoberta
   - Use PEDS para detalhes de processamento
   - Use APIs de Cessão para rastreamento de propriedade
   - Combine dados para análise abrangente

## Observações Importantes

- **Sunset de API Herdada**: API herdada PatentsView descontinuada em 1º de maio de 2025 - use PatentSearch API
- **PAIR Bulk Data Descontinuado**: Use PEDS no lugar
- **Cobertura de Dados**: PatentSearch tem dados até 30 de junho de 2025; PEDS de 1981-presente
- **Endpoints de Texto**: Endpoints de reivindicações e descrição estão em beta com preenchimento contínuo
- **Limites de Taxa**: Respeite limites de taxa para evitar interrupções de serviço

## Recursos

### Documentação de API
- **PatentSearch API**: https://search.patentsview.org/docs/
- **Portal de Desenvolvedores USPTO**: https://developer.uspto.gov/
- **Portal de Dados Abertos USPTO**: https://data.uspto.gov/
- **Registro de Chave de API**: https://account.uspto.gov/api-manager/

### Bibliotecas Python
- **uspto-opendata-python**: https://pypi.org/project/uspto-opendata-python/
- **Docs USPTO**: https://docs.ip-tools.org/uspto-opendata-python/

### Arquivos de Referência
- `references/patentsearch_api.md` - Referência completa da PatentSearch API
- `references/peds_api.md` - Documentação de API e biblioteca PEDS
- `references/trademark_api.md` - APIs de Marca (TSDR e Cessão)
- `references/additional_apis.md` - Citações, Office Actions, Litigação, PTAB

### Scripts
- `scripts/patent_search.py` - Cliente da PatentSearch API
- `scripts/peds_client.py` - Cliente de dados de exame PEDS
- `scripts/trademark_client.py` - Cliente de busca de marca