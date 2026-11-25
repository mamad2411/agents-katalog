---
name: clinpgx-database
description: "Acesse dados de farmacogenômica do ClinPGx (sucessor do PharmGKB). Consulte interações gene-medicamento, diretrizes CPIC, funções de alelos, para medicina de precisão e decisões de dosagem guiada por genótipo."
---

# Banco de Dados ClinPGx

## Visão Geral

ClinPGx (Clinical Pharmacogenomics Database) é um recurso abrangente de informações de farmacogenômica clínica, sucessor do PharmGKB. Consolida dados do PharmGKB, CPIC e PharmCAT, oferecendo informações curatoradas sobre como variações genéticas afetam a resposta aos medicamentos. Acesse pares gene-medicamento, diretrizes clínicas, funções de alelos e rótulos de medicamentos para aplicações de medicina de precisão.

## Quando Usar Esta Skill

Esta skill deve ser usada quando:

- **Interações gene-medicamento**: Consultar como variantes genéticas afetam metabolismo, eficácia ou toxicidade de medicamentos
- **Diretrizes CPIC**: Acessar diretrizes de prática clínica baseadas em evidências para farmacogenética
- **Informações de alelos**: Recuperar dados de função, frequência e fenótipo de alelos
- **Rótulos de medicamentos**: Explorar rotulagem farmacogenômica de medicamentos FDA e outros órgãos reguladores
- **Anotações farmacogenômicas**: Acessar literatura curatorada sobre relacionamentos gene-medicamento-doença
- **Suporte à decisão clínica**: Usar a ferramenta PharmDOG para conversão de fenótipo e interpretação customizada de genótipo
- **Medicina de precisão**: Implementar testes farmacogenômicos na prática clínica
- **Metabolismo de medicamentos**: Entender funções de CYP450 e outros genes farmacológicos
- **Dosagem personalizada**: Encontrar recomendações de dosagem guiada por genótipo
- **Reações adversas a medicamentos**: Identificar fatores de risco genético para toxicidade de medicamentos

## Instalação e Configuração

### Acesso via API Python

A REST API do ClinPGx fornece acesso programático a todos os recursos do banco de dados. Configuração básica:

```bash
uv pip install requests
```

### Endpoint da API

```python
BASE_URL = "https://api.clinpgx.org/v1/"
```

**Limites de Taxa**:
- Máximo de 2 requisições por segundo
- Requisições excessivas resultarão em resposta HTTP 429 (Too Many Requests)

**Autenticação**: Não obrigatória para acesso básico

**Licença de Dados**: Creative Commons Attribution-ShareAlike 4.0 International License

Para uso substancial da API, notifique o time do ClinPGx em api@clinpgx.org

## Capacidades Principais

### 1. Consultas de Gene

**Recupere informações de gene** incluindo função, anotações clínicas e significância farmacogenômica:

```python
import requests

# Obter detalhes do gene
response = requests.get("https://api.clinpgx.org/v1/gene/CYP2D6")
gene_data = response.json()

# Buscar genes por nome
response = requests.get("https://api.clinpgx.org/v1/gene",
                       params={"q": "CYP"})
genes = response.json()
```

**Principais farmacogenes**:
- **Enzimas CYP450**: CYP2D6, CYP2C19, CYP2C9, CYP3A4, CYP3A5
- **Transportadores**: SLCO1B1, ABCB1, ABCG2
- **Outros metabolizadores**: TPMT, DPYD, NUDT15, UGT1A1
- **Receptores**: OPRM1, HTR2A, ADRB1
- **Genes HLA**: HLA-B, HLA-A

### 2. Consultas de Medicamento e Substância Química

**Recupere informações de medicamento** incluindo anotações farmacogenômicas e mecanismos:

```python
# Obter detalhes do medicamento
response = requests.get("https://api.clinpgx.org/v1/chemical/PA448515")  # Varfarina
drug_data = response.json()

# Buscar medicamentos por nome
response = requests.get("https://api.clinpgx.org/v1/chemical",
                       params={"name": "warfarin"})
drugs = response.json()
```

**Categorias de medicamento com significância farmacogenômica**:
- Anticoagulantes (varfarina, clopidogrel)
- Antidepressivos (ISRSs, TCAs)
- Imunossupressores (tacrolimus, azatioprina)
- Medicamentos oncológicos (5-fluorouracila, irinotecano, tamoxifeno)
- Medicamentos cardiovasculares (estatinas, betabloqueadores)
- Medicamentos para dor (codeína, tramadol)
- Antivirais (abacavir)

### 3. Consultas de Pares Gene-Medicamento

**Acesse relacionamentos curados de gene-medicamento** com anotações clínicas:

```python
# Obter informações de par gene-medicamento
response = requests.get("https://api.clinpgx.org/v1/geneDrugPair",
                       params={"gene": "CYP2D6", "drug": "codeine"})
pair_data = response.json()

# Obter todos os pares para um gene
response = requests.get("https://api.clinpgx.org/v1/geneDrugPair",
                       params={"gene": "CYP2C19"})
all_pairs = response.json()
```

**Fontes de anotação clínica**:
- CPIC (Clinical Pharmacogenetics Implementation Consortium)
- DPWG (Dutch Pharmacogenetics Working Group)
- FDA (Food and Drug Administration)
- Anotações de resumo de literatura revisada por pares

### 4. Diretrizes CPIC

**Acesse diretrizes de prática clínica baseadas em evidências**:

```python
# Obter diretriz CPIC
response = requests.get("https://api.clinpgx.org/v1/guideline/PA166104939")
guideline = response.json()

# Listar todas as diretrizes CPIC
response = requests.get("https://api.clinpgx.org/v1/guideline",
                       params={"source": "CPIC"})
guidelines = response.json()
```

**Componentes de diretriz CPIC**:
- Pares gene-medicamento abrangidos
- Recomendações clínicas por fenótipo
- Níveis de evidência e classificações de força
- Literatura de suporte
- PDFs baixáveis e materiais suplementares
- Considerações de implementação

**Exemplo de diretrizes**:
- CYP2D6-codeína (evitar em metabolizadores ultra-rápidos)
- CYP2C19-clopidogrel (terapia alternativa para metabolizadores lentos)
- TPMT-azatioprina (redução de dose para metabolizadores intermediários/lentos)
- DPYD-fluoropirimidinas (ajuste de dose baseado em atividade)
- HLA-B*57:01-abacavir (evitar se positivo)

### 5. Informações de Alelo e Variante

**Consulte dados de função e frequência de alelo**:

```python
# Obter informações de alelo
response = requests.get("https://api.clinpgx.org/v1/allele/CYP2D6*4")
allele_data = response.json()

# Obter todos os alelos para um gene
response = requests.get("https://api.clinpgx.org/v1/allele",
                       params={"gene": "CYP2D6"})
alleles = response.json()
```

**Informações de alelo incluem**:
- Status funcional (normal, diminuído, sem função, aumentado, incerto)
- Frequências populacionais entre grupos étnicos
- Variantes definidoras (SNPs, indels, CNVs)
- Atribuição de fenótipo
- Referências a sistemas de nomenclatura PharmVar e outros

**Categorias de fenótipo**:
- **Metabolizador ultra-rápido** (UM): Atividade enzimática aumentada
- **Metabolizador normal** (NM): Atividade enzimática normal
- **Metabolizador intermediário** (IM): Atividade enzimática reduzida
- **Metabolizador lento** (PM): Atividade enzimática pouca ou nenhuma

### 6. Anotações de Variante

**Acesse anotações clínicas para variantes genéticas específicas**:

```python
# Obter informações de variante
response = requests.get("https://api.clinpgx.org/v1/variant/rs4244285")
variant_data = response.json()

# Buscar variantes por posição (se suportado)
response = requests.get("https://api.clinpgx.org/v1/variant",
                       params={"chromosome": "10", "position": "94781859"})
variants = response.json()
```

**Os dados de variante incluem**:
- rsID e coordenadas genômicas
- Gene e consequência funcional
- Associações de alelo
- Significância clínica
- Frequências populacionais
- Referências de literatura

### 7. Anotações Clínicas

**Recupere anotações de literatura curatoradas** (anteriormente anotações clínicas PharmGKB):

```python
# Obter anotações clínicas
response = requests.get("https://api.clinpgx.org/v1/clinicalAnnotation",
                       params={"gene": "CYP2D6"})
annotations = response.json()

# Filtrar por nível de evidência
response = requests.get("https://api.clinpgx.org/v1/clinicalAnnotation",
                       params={"evidenceLevel": "1A"})
high_evidence = response.json()
```

**Níveis de evidência** (do mais alto para o mais baixo):
- **Nível 1A**: Evidência de alta qualidade, diretrizes CPIC/FDA/DPWG
- **Nível 1B**: Evidência de alta qualidade, ainda não em diretriz
- **Nível 2A**: Evidência moderada de estudos bem desenhados
- **Nível 2B**: Evidência moderada com algumas limitações
- **Nível 3**: Evidência limitada ou conflitante
- **Nível 4**: Relatos de caso ou evidência fraca

### 8. Rótulos de Medicamentos

**Acesse informações farmacogenômicas de rótulos de medicamentos**:

```python
# Obter rótulos de medicamentos com informações PGx
response = requests.get("https://api.clinpgx.org/v1/drugLabel",
                       params={"drug": "warfarin"})
labels = response.json()

# Filtrar por fonte reguladora
response = requests.get("https://api.clinpgx.org/v1/drugLabel",
                       params={"source": "FDA"})
fda_labels = response.json()
```

**Informações do rótulo incluem**:
- Recomendações de teste
- Orientação de dosagem por genótipo
- Avisos e precauções
- Informações de biomarcador
- Fonte reguladora (FDA, EMA, PMDA, etc.)

### 9. Vias

**Explore vias farmacocinéticas e farmacodinâmicas**:

```python
# Obter informações de via
response = requests.get("https://api.clinpgx.org/v1/pathway/PA146123006")  # Via Varfarina
pathway_data = response.json()

# Buscar vias por medicamento
response = requests.get("https://api.clinpgx.org/v1/pathway",
                       params={"drug": "warfarin"})
pathways = response.json()
```

**Diagramas de via** mostram:
- Etapas de metabolismo do medicamento
- Enzimas e transportadores envolvidos
- Variantes genéticas afetando cada etapa
- Efeitos a jusante em eficácia/toxicidade
- Interações com outras vias

## Fluxo de Consulta

### Fluxo 1: Suporte à Decisão Clínica para Prescrição de Medicamento

1. **Identifique genótipo do paciente** para farmacogenes relevantes:
   ```python
   # Exemplo: Paciente é CYP2C19 *1/*2 (metabolizador intermediário)
   response = requests.get("https://api.clinpgx.org/v1/allele/CYP2C19*2")
   allele_function = response.json()
   ```

2. **Consulte pares gene-medicamento** para medicamento de interesse:
   ```python
   response = requests.get("https://api.clinpgx.org/v1/geneDrugPair",
                          params={"gene": "CYP2C19", "drug": "clopidogrel"})
   pair_info = response.json()
   ```

3. **Recupere diretriz CPIC** para recomendações de dosagem:
   ```python
   response = requests.get("https://api.clinpgx.org/v1/guideline",
                          params={"gene": "CYP2C19", "drug": "clopidogrel"})
   guideline = response.json()
   # Recomendação: Terapia antiagregante plaquetária alternativa para IM/PM
   ```

4. **Verifique rótulo do medicamento** para orientação reguladora:
   ```python
   response = requests.get("https://api.clinpgx.org/v1/drugLabel",
                          params={"drug": "clopidogrel"})
   label = response.json()
   ```

### Fluxo 2: Análise de Painel de Gene

1. **Obtenha lista de farmacogenes** em painel clínico:
   ```python
   pgx_panel = ["CYP2C19", "CYP2D6", "CYP2C9", "TPMT", "DPYD", "SLCO1B1"]
   ```

2. **Para cada gene, recupere todas as interações com medicamentos**:
   ```python
   all_interactions = {}
   for gene in pgx_panel:
       response = requests.get("https://api.clinpgx.org/v1/geneDrugPair",
                              params={"gene": gene})
       all_interactions[gene] = response.json()
   ```

3. **Filtre por evidência de nível diretriz CPIC**:
   ```python
   for gene, pairs in all_interactions.items():
       for pair in pairs:
           if pair.get('cpicLevel'):  # Tem diretriz CPIC
               print(f"{gene} - {pair['drug']}: {pair['cpicLevel']}")
   ```

4. **Gere relatório do paciente** com achados farmacogenômicos acionáveis.

### Fluxo 3: Avaliação de Segurança do Medicamento

1. **Consulte medicamento para associações PGx**:
   ```python
   response = requests.get("https://api.clinpgx.org/v1/chemical",
                          params={"name": "abacavir"})
   drug_id = response.json()[0]['id']
   ```

2. **Obtenha anotações clínicas**:
   ```python
   response = requests.get("https://api.clinpgx.org/v1/clinicalAnnotation",
                          params={"drug": drug_id})
   annotations = response.json()
   ```

3. **Verifique associações HLA** e risco de toxicidade:
   ```python
   for annotation in annotations:
       if 'HLA' in annotation.get('genes', []):
           print(f"Risco de toxicidade: {annotation['phenotype']}")
           print(f"Nível de evidência: {annotation['evidenceLevel']}")
   ```

4. **Recupere recomendações de rastreamento** de diretrizes e rótulos.

### Fluxo 4: Análise de Pesquisa - Farmacogenômica Populacional

1. **Obtenha frequências de alelo** para comparação populacional:
   ```python
   response = requests.get("https://api.clinpgx.org/v1/allele",
                          params={"gene": "CYP2D6"})
   alleles = response.json()
   ```

2. **Extraia frequências específicas de população**:
   ```python
   populations = ['European', 'African', 'East Asian', 'Latino']
   frequency_data = {}
   for allele in alleles:
       allele_name = allele['name']
       frequency_data[allele_name] = {
           pop: allele.get(f'{pop}_frequency', 'N/A')
           for pop in populations
       }
   ```

3. **Calcule distribuições de fenótipo** por população:
   ```python
   # Combine frequências de alelo com função para prever fenótipos
   phenotype_dist = calculate_phenotype_frequencies(frequency_data)
   ```

4. **Analise implicações** para dosagem de medicamento em populações diversas.

### Fluxo 5: Revisão de Evidência de Literatura

1. **Busque par gene-medicamento**:
   ```python
   response = requests.get("https://api.clinpgx.org/v1/geneDrugPair",
                          params={"gene": "TPMT", "drug": "azathioprine"})
   pair = response.json()
   ```

2. **Recupere todas as anotações clínicas**:
   ```python
   response = requests.get("https://api.clinpgx.org/v1/clinicalAnnotation",
                          params={"gene": "TPMT", "drug": "azathioprine"})
   annotations = response.json()
   ```

3. **Filtre por nível de evidência e data de publicação**:
   ```python
   high_quality = [a for a in annotations
                   if a['evidenceLevel'] in ['1A', '1B', '2A']]
   ```

4. **Extraia PMIDs** e recupere referências completas:
   ```python
   pmids = [a['pmid'] for a in high_quality if 'pmid' in a]
   # Use skill PubMed para recuperar citações completas
   ```

## Limite de Taxa e Melhores Práticas

### Conformidade com Limite de Taxa

```python
import time

def rate_limited_request(url, params=None, delay=0.5):
    """Faça requisição de API com limite de taxa (máximo 2 req/seg)"""
    response = requests.get(url, params=params)
    time.sleep(delay)  # Aguarde 0.5 segundo entre requisições
    return response

# Use em loops
genes = ["CYP2D6", "CYP2C19", "CYP2C9"]
for gene in genes:
    response = rate_limited_request(
        "https://api.clinpgx.org/v1/gene/" + gene
    )
    data = response.json()
```

### Tratamento de Erros

```python
def safe_api_call(url, params=None, max_retries=3):
    """Chamada de API com tratamento de erro e tentativas"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                # Limite de taxa excedido
                wait_time = 2 ** attempt  # Backoff exponencial
                print(f"Limite de taxa atingido. Aguardando {wait_time}s...")
                time.sleep(wait_time)
            else:
                response.raise_for_status()

        except requests.exceptions.RequestException as e:
            print(f"Tentativa {attempt + 1} falhou: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(1)
```

### Cache de Resultados

```python
import json
from pathlib import Path

def cached_query(cache_file, api_func, *args, **kwargs):
    """Cache resultados de API para evitar consultas repetidas"""
    cache_path = Path(cache_file)

    if cache_path.exists():
        with open(cache_path) as f:
            return json.load(f)

    result = api_func(*args, **kwargs)

    with open(cache_path, 'w') as f:
        json.dump(result, f, indent=2)

    return result

# Uso
gene_data = cached_query(
    'cyp2d6_cache.json',
    rate_limited_request,
    "https://api.clinpgx.org/v1/gene/CYP2D6"
)
```

## Ferramenta PharmDOG

PharmDOG (anteriormente DDRx) é a ferramenta de suporte à decisão clínica do ClinPGx para interpretar resultados de testes farmacogenômicos:

**Recursos principais**:
- **Calculadora de conversão de fenótipo**: Ajusta previsões de fenótipo para interações medicamentosas afetando CYP2D6
- **Genótipos customizados**: Insira genótipos de paciente para obter previsões de fenótipo
- **Compartilhamento de código QR**: Gere relatórios de paciente compartilháveis
- **Fontes de orientação flexíveis**: Selecione quais diretrizes aplicar (CPIC, DPWG, FDA)
- **Análise multi-medicamento**: Avalie múltiplos medicamentos simultaneamente

**Acesso**: Disponível em https://www.clinpgx.org/pharmacogenomic-decision-support

**Casos de uso**:
- Interpretação clínica de resultados de painel PGx
- Revisão de medicamentos para pacientes com genótipos conhecidos
- Materiais de educação do paciente
- Suporte à decisão no ponto de cuidado

## Recursos

### scripts/query_clinpgx.py

Script Python com funções prontas para uso em consultas comuns do ClinPGx:

- `get_gene_info(gene_symbol)` - Recupere detalhes do gene
- `get_drug_info(drug_name)` - Obtenha informações do medicamento
- `get_gene_drug_pairs(gene, drug)` - Consulte interações gene-medicamento
- `get_cpic_guidelines(gene, drug)` - Recupere diretrizes CPIC
- `get_alleles(gene)` - Obtenha todos os alelos para um gene
- `get_clinical_annotations(gene, drug, evidence_level)` - Consulte anotações de literatura
- `get_drug_labels(drug)` - Recupere rótulos farmacogenômicos de medicamento
- `search_variants(rsid)` - Busque por rsID de variante
- `export_to_dataframe(data)` - Converta resultados para DataFrame do pandas

Consulte este script para exemplos de implementação com limite de taxa apropriado e tratamento de erro.

### references/api_reference.md

Documentação abrangente de API incluindo:

- Listagem de endpoint completa com parâmetros
- Especificações de formato de requisição/resposta
- Consultas de exemplo para cada endpoint
- Operadores de filtro e padrões de busca
- Definições de schema de dados
- Detalhes de limite de taxa
- Requisitos de autenticação (se houver)
- Solução de problemas de erros comuns

Consulte este documento quando informações detalhadas de API forem necessárias ou ao construir consultas complexas.

## Notas Importantes

### Fontes de Dados e Integração

ClinPGx consolida múltiplas fontes autoritárias:
- **PharmGKB**: Base de conhecimento de farmacogenômica curatorada (agora parte do ClinPGx)
- **CPIC**: Diretrizes de implementação clínica baseadas em evidências
- **PharmCAT**: Ferramenta de chamada de alelo e interpretação de fenótipo
- **DPWG**: Diretrizes farmacogenéticas holandesas
- **Rótulos FDA/EMA**: Informações farmacogenômicas regulatórias

A partir de julho de 2025, todos os URLs PharmGKB redirecionam para páginas correspondentes do ClinPGx.

### Considerações de Implementação Clínica

- **Níveis de evidência**: Sempre verifique a força da evidência antes da aplicação clínica
- **Diferenças populacionais**: Frequências de alelo variam significativamente entre populações
- **Conversão de fenótipo**: Considere interações medicamentosas que afetam atividade enzimática
- **Efeitos multi-gene**: Alguns medicamentos são afetados por múltiplos farmacogenes
- **Fatores não genéticos**: Idade, função de órgão e interações medicamentosas também afetam resposta
- **Limitações de teste**: Nem todos os alelos clinicamente relevantes são detectados por todos os ensaios

### Atualizações de Dados

- ClinPGx atualiza continuamente com novas evidências e diretrizes
- Verifique datas de publicação de anotações clínicas
- Monitore Blog ClinPGx (https://blog.clinpgx.org/) para anúncios
- Diretrizes CPIC atualizadas conforme novas evidências emergem
- PharmVar fornece atualizações de nomenclatura para definições de alelo

### Estabilidade da API

- Os endpoints de API são relativamente estáveis mas podem mudar durante desenvolvimento
- Parâmetros e formatos de resposta sujeitos a modificação
- Monitore changelog de API e blog ClinPGx para atualizações
- Considere fixação de versão para aplicações de produção
- Teste mudanças de API em desenvolvimento antes de implantação em produção

## Casos de Uso Comuns

### Teste Farmacogenômico Pré-emptivo

Consulte todos os pares gene-medicamento clinicamente acionáveis para guiar seleção de painel:

```python
# Obtenha todos os pares com diretriz CPIC
response = requests.get("https://api.clinpgx.org/v1/geneDrugPair",
                       params={"cpicLevel": "A"})  # Recomendações Nível A
actionable_pairs = response.json()
```

### Gestão de Terapia Medicamentosa

Revise medicamentos de paciente contra genótipos conhecidos:

```python
patient_genes = {"CYP2C19": "*1/*2", "CYP2D6": "*1/*1", "SLCO1B1": "*1/*5"}
medications = ["clopidogrel", "simvastatin", "escitalopram"]

for med in medications:
    for gene in patient_genes:
        response = requests.get("https://api.clinpgx.org/v1/geneDrugPair",
                               params={"gene": gene, "drug": med})
        # Verifique interações e orientação de dosagem
```

### Elegibilidade para Ensaio Clínico

Rastreie contra-indicações farmacogenômicas:

```python
# Verifique HLA-B*57:01 antes do ensaio de abacavir
response = requests.get("https://api.clinpgx.org/v1/geneDrugPair",
                       params={"gene": "HLA-B", "drug": "abacavir"})
pair_info = response.json()
# CPIC: Não use se HLA-B*57:01 positivo
```

## Recursos Adicionais

- **Website ClinPGx**: https://www.clinpgx.org/
- **Blog ClinPGx**: https://blog.clinpgx.org/
- **Documentação de API**: https://api.clinpgx.org/
- **Website CPIC**: https://cpicpgx.org/
- **PharmCAT**: https://pharmcat.clinpgx.org/
- **ClinGen**: https://clinicalgenome.org/
- **Contato**: api@clinpgx.org (para uso substancial de API)