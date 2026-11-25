---
name: fda-database
description: "Consultar API openFDA para medicamentos, dispositivos, eventos adversos, recalls, submissões regulatórias (510k, PMA), identificação de substâncias (UNII), para análise de dados regulatórios da FDA e pesquisa de segurança."
---

# Acesso ao Banco de Dados da FDA

## Visão Geral

Acesse dados regulatórios abrangentes da FDA por meio do openFDA, a iniciativa da FDA de fornecer APIs abertas para conjuntos de dados públicos. Consulte informações sobre medicamentos, dispositivos médicos, alimentos, produtos animais/veterinários e substâncias usando Python com interfaces padronizadas.

**Principais capacidades:**
- Consultar eventos adversos para medicamentos, dispositivos, alimentos e produtos veterinários
- Acessar rotulagem de produtos, aprovações e submissões regulatórias
- Monitorar recalls e ações de execução
- Procurar Códigos de Medicamento Nacional (NDC) e identificadores de substâncias (UNII)
- Analisar classificações de dispositivos e autorizações (510k, PMA)
- Rastrear escassez de medicamentos e problemas de suprimento
- Pesquisar estruturas químicas e relacionamentos de substâncias

## Quando Usar Esta Habilidade

Esta habilidade deve ser usada ao trabalhar com:
- **Pesquisa de medicamentos**: Perfis de segurança, eventos adversos, rotulagem, aprovações, escassez
- **Vigilância de dispositivos médicos**: Eventos adversos, recalls, autorizações 510(k), aprovações PMA
- **Segurança alimentar**: Recalls, rastreamento de alérgenos, eventos adversos, suplementos dietéticos
- **Medicina veterinária**: Eventos adversos de medicamentos para animais por espécie e raça
- **Dados químicos/de substâncias**: Busca UNII, mapeamento de número CAS, estruturas moleculares
- **Análise regulatória**: Caminhos de aprovação, ações de execução, rastreamento de conformidade
- **Farmacovigilância**: Vigilância pós-comercialização, detecção de sinais de segurança
- **Pesquisa científica**: Interações de medicamentos, segurança comparativa, estudos epidemiológicos

## Início Rápido

### 1. Configuração Básica

```python
from scripts.fda_query import FDAQuery

# Inicializar (chave de API opcional, mas recomendada)
fda = FDAQuery(api_key="YOUR_API_KEY")

# Consultar eventos adversos de medicamentos
events = fda.query_drug_events("aspirin", limit=100)

# Obter rotulagem de medicamento
label = fda.query_drug_label("Lipitor", brand=True)

# Buscar recalls de dispositivos
recalls = fda.query("device", "enforcement",
                   search="classification:Class+I",
                   limit=50)
```

### 2. Configuração de Chave de API

Embora a API funcione sem chave, o registro fornece limites de taxa mais altos:
- **Sem chave**: 240 requisições/min, 1.000/dia
- **Com chave**: 240 requisições/min, 120.000/dia

Registre-se em: https://open.fda.gov/apis/authentication/

Defina como variável de ambiente:
```bash
export FDA_API_KEY="your_key_here"
```

### 3. Executando Exemplos

```bash
# Executar exemplos abrangentes
python scripts/fda_examples.py

# Isto demonstra:
# - Perfis de segurança de medicamentos
# - Vigilância de dispositivos
# - Monitoramento de recalls de alimentos
# - Busca de substâncias
# - Análise comparativa de medicamentos
# - Análise de medicamentos veterinários
```

## Categorias do Banco de Dados FDA

### Medicamentos

Acesse 6 endpoints relacionados a medicamentos cobrindo todo o ciclo de vida do medicamento, desde aprovação até vigilância pós-comercialização.

**Endpoints:**
1. **Eventos Adversos** - Relatórios de efeitos colaterais, erros e falhas terapêuticas
2. **Rotulagem de Produtos** - Informações de prescrição, avisos, indicações
3. **Diretório NDC** - Informações de produtos com Código Nacional de Medicamento
4. **Relatórios de Execução** - Recalls de medicamentos e ações de segurança
5. **Drugs@FDA** - Dados de aprovação histórica desde 1939
6. **Escassez de Medicamentos** - Problemas de suprimento atuais e resolvidos

**Casos de uso comuns:**
```python
# Detecção de sinais de segurança
fda.count_by_field("drug", "event",
                  search="patient.drug.medicinalproduct:metformin",
                  field="patient.reaction.reactionmeddrapt")

# Obter informações de prescrição
label = fda.query_drug_label("Keytruda", brand=True)

# Verificar recalls
recalls = fda.query_drug_recalls(drug_name="metformin")

# Monitorar escassez
shortages = fda.query("drug", "drugshortages",
                     search="status:Currently+in+Shortage")
```

**Referência:** Veja `references/drugs.md` para documentação detalhada

### Dispositivos

Acesse 9 endpoints relacionados a dispositivos cobrindo segurança, aprovações e registros de dispositivos médicos.

**Endpoints:**
1. **Eventos Adversos** - Mau funcionamento, lesões e mortes de dispositivos
2. **Autorizações 510(k)** - Notificações de pré-comercialização
3. **Classificação** - Categorias de dispositivos e classes de risco
4. **Relatórios de Execução** - Recalls de dispositivos
5. **Recalls** - Informações detalhadas de recalls
6. **PMA** - Dados de aprovação pré-comercialização para dispositivos Classe III
7. **Registros e Listagens** - Dados de estabelecimentos de fabricação
8. **UDI** - Banco de dados de Identificação Única de Dispositivos
9. **Sorologia COVID-19** - Dados de desempenho de testes de anticorpos

**Casos de uso comuns:**
```python
# Monitorar segurança de dispositivos
events = fda.query_device_events("pacemaker", limit=100)

# Procurar classificação de dispositivo
classification = fda.query_device_classification("DQY")

# Encontrar autorizações 510(k)
clearances = fda.query_device_510k(applicant="Medtronic")

# Pesquisar por UDI
device_info = fda.query("device", "udi",
                       search="identifiers.id:00884838003019")
```

**Referência:** Veja `references/devices.md` para documentação detalhada

### Alimentos

Acesse 2 endpoints relacionados a alimentos para monitoramento de segurança e recalls.

**Endpoints:**
1. **Eventos Adversos** - Alimentos, suplementos dietéticos e eventos cosméticos
2. **Relatórios de Execução** - Recalls de produtos alimentares

**Casos de uso comuns:**
```python
# Monitorar recalls de alérgenos
recalls = fda.query_food_recalls(reason="undeclared peanut")

# Rastrear eventos de suplementos dietéticos
events = fda.query_food_events(
    industry="Dietary Supplements")

# Encontrar recalls de contaminação
listeria = fda.query_food_recalls(
    reason="listeria",
    classification="I")
```

**Referência:** Veja `references/foods.md` para documentação detalhada

### Animal e Veterinária

Acesse dados de eventos adversos de medicamentos veterinários com informações específicas de espécie.

**Endpoint:**
1. **Eventos Adversos** - Efeitos colaterais de medicamentos para animais por espécie, raça e produto

**Casos de uso comuns:**
```python
# Eventos específicos por espécie
dog_events = fda.query_animal_events(
    species="Dog",
    drug_name="flea collar")

# Análise de predisposição por raça
breed_query = fda.query("animalandveterinary", "event",
    search="reaction.veddra_term_name:*seizure*+AND+"
           "animal.breed.breed_component:*Labrador*")
```

**Referência:** Veja `references/animal_veterinary.md` para documentação detalhada

### Substâncias e Outros

Acesse dados de substâncias em nível molecular com códigos UNII, estruturas químicas e relacionamentos.

**Endpoints:**
1. **Dados de Substâncias** - UNII, CAS, estruturas químicas, relacionamentos
2. **NSDE** - Dados de substâncias históricos (legado)

**Casos de uso comuns:**
```python
# Mapeamento UNII para CAS
substance = fda.query_substance_by_unii("R16CO5Y76E")

# Pesquisar por nome
results = fda.query_substance_by_name("acetaminophen")

# Obter estrutura química
structure = fda.query("other", "substance",
    search="names.name:ibuprofen+AND+substanceClass:chemical")
```

**Referência:** Veja `references/other.md` para documentação detalhada

## Padrões Comuns de Consulta

### Padrão 1: Análise de Perfil de Segurança

Crie perfis de segurança abrangentes combinando múltiplas fontes de dados:

```python
def drug_safety_profile(fda, drug_name):
    """Gerar perfil de segurança completo."""

    # 1. Total de eventos adversos
    events = fda.query_drug_events(drug_name, limit=1)
    total = events["meta"]["results"]["total"]

    # 2. Reações mais comuns
    reactions = fda.count_by_field(
        "drug", "event",
        search=f"patient.drug.medicinalproduct:*{drug_name}*",
        field="patient.reaction.reactionmeddrapt",
        exact=True
    )

    # 3. Eventos graves
    serious = fda.query("drug", "event",
        search=f"patient.drug.medicinalproduct:*{drug_name}*+AND+serious:1",
        limit=1)

    # 4. Recalls recentes
    recalls = fda.query_drug_recalls(drug_name=drug_name)

    return {
        "total_events": total,
        "top_reactions": reactions["results"][:10],
        "serious_events": serious["meta"]["results"]["total"],
        "recalls": recalls["results"]
    }
```

### Padrão 2: Análise de Tendências Temporais

Analise tendências ao longo do tempo usando intervalos de datas:

```python
from datetime import datetime, timedelta

def get_monthly_trends(fda, drug_name, months=12):
    """Obter tendências mensais de eventos adversos."""
    trends = []

    for i in range(months):
        end = datetime.now() - timedelta(days=30*i)
        start = end - timedelta(days=30)

        date_range = f"[{start.strftime('%Y%m%d')}+TO+{end.strftime('%Y%m%d')}]"
        search = f"patient.drug.medicinalproduct:*{drug_name}*+AND+receivedate:{date_range}"

        result = fda.query("drug", "event", search=search, limit=1)
        count = result["meta"]["results"]["total"] if "meta" in result else 0

        trends.append({
            "month": start.strftime("%Y-%m"),
            "events": count
        })

    return trends
```

### Padrão 3: Análise Comparativa

Compare múltiplos produtos lado a lado:

```python
def compare_drugs(fda, drug_list):
    """Comparar perfis de segurança de múltiplos medicamentos."""
    comparison = {}

    for drug in drug_list:
        # Total de eventos
        events = fda.query_drug_events(drug, limit=1)
        total = events["meta"]["results"]["total"] if "meta" in events else 0

        # Eventos graves
        serious = fda.query("drug", "event",
            search=f"patient.drug.medicinalproduct:*{drug}*+AND+serious:1",
            limit=1)
        serious_count = serious["meta"]["results"]["total"] if "meta" in serious else 0

        comparison[drug] = {
            "total_events": total,
            "serious_events": serious_count,
            "serious_rate": (serious_count/total*100) if total > 0 else 0
        }

    return comparison
```

### Padrão 4: Busca em Múltiplos Bancos de Dados

Vincule dados em múltiplos endpoints:

```python
def comprehensive_device_lookup(fda, device_name):
    """Procurar dispositivo em todos os bancos de dados relevantes."""

    return {
        "adverse_events": fda.query_device_events(device_name, limit=10),
        "510k_clearances": fda.query_device_510k(device_name=device_name),
        "recalls": fda.query("device", "enforcement",
                           search=f"product_description:*{device_name}*"),
        "udi_info": fda.query("device", "udi",
                            search=f"brand_name:*{device_name}*")
    }
```

## Trabalhando com Resultados

### Estrutura de Resposta

Todas as respostas da API seguem esta estrutura:

```python
{
    "meta": {
        "disclaimer": "...",
        "results": {
            "skip": 0,
            "limit": 100,
            "total": 15234
        }
    },
    "results": [
        # Array de objetos de resultado
    ]
}
```

### Tratamento de Erros

Sempre trate erros potenciais:

```python
result = fda.query_drug_events("aspirin", limit=10)

if "error" in result:
    print(f"Erro: {result['error']}")
elif "results" not in result or len(result["results"]) == 0:
    print("Nenhum resultado encontrado")
else:
    # Processar resultados
    for event in result["results"]:
        # Tratar dados de evento
        pass
```

### Paginação

Para grandes conjuntos de resultados, use paginação:

```python
# Paginação automática
all_results = fda.query_all(
    "drug", "event",
    search="patient.drug.medicinalproduct:aspirin",
    max_results=5000
)

# Paginação manual
for skip in range(0, 1000, 100):
    batch = fda.query("drug", "event",
                     search="...",
                     limit=100,
                     skip=skip)
    # Processar lote
```

## Melhores Práticas

### 1. Use Buscas Específicas

**FAÇA:**
```python
# Busca de campo específico
search="patient.drug.medicinalproduct:aspirin"
```

**NÃO FAÇA:**
```python
# Wildcard muito amplo
search="*aspirin*"
```

### 2. Implemente Limitação de Taxa

A classe `FDAQuery` lida com limitação de taxa automaticamente, mas esteja ciente dos limites:
- 240 requisições por minuto
- 120.000 requisições por dia (com chave de API)

### 3. Cache de Dados Acessados Frequentemente

A classe `FDAQuery` inclui cache integrado (habilitado por padrão):

```python
# Cache é automático
fda = FDAQuery(api_key=api_key, use_cache=True, cache_ttl=3600)
```

### 4. Use Correspondência Exata para Contagem

Ao contar/agregar, use o sufixo `.exact`:

```python
# Contar frases exatas
fda.count_by_field("drug", "event",
                  search="...",
                  field="patient.reaction.reactionmeddrapt",
                  exact=True)  # Adiciona .exact automaticamente
```

### 5. Valide Dados de Entrada

Limpe e valide termos de busca:

```python
def clean_drug_name(name):
    """Limpar nome de medicamento para consulta."""
    return name.strip().replace('"', '\\"')

drug_name = clean_drug_name(user_input)
```

## Referência de API

Para informações detalhadas sobre:
- **Autenticação e limites de taxa** → Veja `references/api_basics.md`
- **Bancos de dados de medicamentos** → Veja `references/drugs.md`
- **Bancos de dados de dispositivos** → Veja `references/devices.md`
- **Bancos de dados de alimentos** → Veja `references/foods.md`
- **Bancos de dados animais/veterinários** → Veja `references/animal_veterinary.md`
- **Bancos de dados de substâncias** → Veja `references/other.md`

## Scripts

### `scripts/fda_query.py`

Módulo de consulta principal com classe `FDAQuery` fornecendo:
- Interface unificada para todos os endpoints FDA
- Limitação de taxa automática e cache
- Tratamento de erros e lógica de retry
- Padrões de consulta comuns

### `scripts/fda_examples.py`

Exemplos abrangentes demonstrando:
- Análise de perfil de segurança de medicamentos
- Monitoramento de vigilância de dispositivos
- Rastreamento de recalls de alimentos
- Busca de substâncias
- Análise comparativa de medicamentos
- Análise de medicamentos veterinários

Execute exemplos:
```bash
python scripts/fda_examples.py
```

## Recursos Adicionais

- **Homepage openFDA**: https://open.fda.gov/
- **Documentação de API**: https://open.fda.gov/apis/
- **Explorador de API Interativo**: https://open.fda.gov/apis/try-the-api/
- **Repositório GitHub**: https://github.com/FDA/openfda
- **Termos de Serviço**: https://open.fda.gov/terms/

## Suporte e Resolução de Problemas

### Problemas Comuns

**Problema**: Limite de taxa excedido
- **Solução**: Use chave de API, implemente atrasos ou reduza frequência de requisições

**Problema**: Nenhum resultado encontrado
- **Solução**: Tente termos de busca mais amplos, verifique ortografia, use wildcards

**Problema**: Sintaxe de consulta inválida
- **Solução**: Revise sintaxe de consulta em `references/api_basics.md`

**Problema**: Campos ausentes nos resultados
- **Solução**: Nem todos os registros contêm todos os campos; sempre verifique existência de campo

### Obter Ajuda

- **Problemas GitHub**: https://github.com/FDA/openfda/issues
- **Email**: open-fda@fda.hhs.gov