---
name: opentargets-database
description: "Consulte a Plataforma Open Targets para associações alvo-doença, descoberta de alvo farmacológico, dados de tratabilidade/segurança, evidências genéticas/ômicas, fármacos conhecidos, para identificação de alvo terapêutico."
---

# Base de Dados Open Targets

## Visão Geral

A Plataforma Open Targets é um recurso abrangente para identificação e priorização sistemática de potenciais alvos farmacológicos terapêuticos. Integra conjuntos de dados disponíveis publicamente, incluindo genética humana, ômicas, literatura e dados químicos para construir e pontuar associações alvo-doença.

**Capacidades principais:**
- Consultar anotações de alvo (gene), incluindo tratabilidade, segurança, expressão
- Pesquisar associações doença-alvo com pontuações de evidência
- Recuperar evidências de múltiplos tipos de dados (genética, vias, literatura, etc.)
- Encontrar fármacos conhecidos para doenças e seus mecanismos
- Acessar informações de fármacos, incluindo fases de ensaios clínicos e eventos adversos
- Avaliar tratabilidade e potencial terapêutico do alvo

**Acesso aos dados:** A plataforma oferece API GraphQL, interface web, downloads de dados e acesso ao Google BigQuery. Esta habilidade se concentra na API GraphQL para acesso programático.

## Quando Usar Esta Habilidade

Esta habilidade deve ser usada quando:

- **Descoberta de alvo:** Encontrar potenciais alvos terapêuticos para uma doença
- **Avaliação de alvo:** Avaliar tratabilidade, segurança e tratabilidade de genes
- **Coleta de evidências:** Recuperar evidências de apoio para associações alvo-doença
- **Reposicionamento de fármacos:** Identificar fármacos existentes que podem ser reposicionados para novas indicações
- **Inteligência competitiva:** Entender precedência clínica e panorama de desenvolvimento de fármacos
- **Priorização de alvo:** Classificar alvos com base em evidências genéticas e outros tipos de dados
- **Pesquisa de mecanismo:** Investigar vias biológicas e funções gênicas
- **Descoberta de biomarcadores:** Encontrar genes expressos diferencialmente em doença
- **Avaliação de segurança:** Identificar possíveis preocupações de toxicidade para alvos farmacológicos

## Fluxo de Trabalho Principal

### 1. Pesquisar por Entidades

Comece encontrando os identificadores para alvos, doenças ou fármacos de interesse.

**Para alvos (genes):**
```python
from scripts.query_opentargets import search_entities

# Pesquisar por símbolo ou nome de gene
results = search_entities("BRCA1", entity_types=["target"])
# Retorna: [{"id": "ENSG00000012048", "name": "BRCA1", ...}]
```

**Para doenças:**
```python
# Pesquisar por nome de doença
results = search_entities("alzheimer", entity_types=["disease"])
# Retorna: [{"id": "EFO_0000249", "name": "Alzheimer disease", ...}]
```

**Para fármacos:**
```python
# Pesquisar por nome de fármaco
results = search_entities("aspirin", entity_types=["drug"])
# Retorna: [{"id": "CHEMBL25", "name": "ASPIRIN", ...}]
```

**Identificadores usados:**
- Alvos: IDs de gene Ensembl (ex: `ENSG00000157764`)
- Doenças: IDs EFO (Experimental Factor Ontology) (ex: `EFO_0000249`)
- Fármacos: IDs ChEMBL (ex: `CHEMBL25`)

### 2. Consultar Informações de Alvo

Recupere anotações abrangentes de alvo para avaliar tratabilidade e biologia.

```python
from scripts.query_opentargets import get_target_info

target_info = get_target_info("ENSG00000157764", include_diseases=True)

# Acesse campos principais:
# - approvedSymbol: Símbolo de gene HGNC
# - approvedName: Nome completo do gene
# - tractability: Avaliações de tratabilidade em modalidades
# - safetyLiabilities: Preocupações de segurança conhecidas
# - geneticConstraint: Scores de constraint do gnomAD
# - associatedDiseases: Principais associações de doença com scores
```

**Anotações principais para revisar:**
- **Tratabilidade:** Previsões de tratabilidade de molécula pequena, anticorpo, PROTAC
- **Segurança:** Preocupações de toxicidade conhecidas de múltiplos bancos de dados
- **Constraint genético:** Scores pLI e LOEUF indicando essencialidade
- **Associações de doença:** Doenças ligadas ao alvo com scores de evidência

Consulte `references/target_annotations.md` para informações detalhadas sobre todas as features de alvo.

### 3. Consultar Informações de Doença

Obtenha detalhes de doença e alvos/fármacos associados.

```python
from scripts.query_opentargets import get_disease_info

disease_info = get_disease_info("EFO_0000249", include_targets=True)

# Acesse campos:
# - name: Nome da doença
# - description: Descrição da doença
# - therapeuticAreas: Categorias de doença de alto nível
# - associatedTargets: Principais alvos com scores de associação
```

### 4. Recuperar Evidências Alvo-Doença

Obtenha evidências detalhadas apoiando uma associação alvo-doença.

```python
from scripts.query_opentargets import get_target_disease_evidence

# Obter todas as evidências
evidence = get_target_disease_evidence(
    ensembl_id="ENSG00000157764",
    efo_id="EFO_0000249"
)

# Filtrar por tipo de evidência
genetic_evidence = get_target_disease_evidence(
    ensembl_id="ENSG00000157764",
    efo_id="EFO_0000249",
    data_types=["genetic_association"]
)

# Cada registro de evidência contém:
# - datasourceId: Fonte de dados específica (ex: "gwas_catalog", "chembl")
# - datatypeId: Categoria de evidência (ex: "genetic_association", "known_drug")
# - score: Força da evidência (0-1)
# - studyId: Identificador do estudo original
# - literature: Publicações associadas
```

**Principais tipos de evidência:**
1. **genetic_association:** GWAS, variantes raras, ClinVar, gene burden
2. **somatic_mutation:** Cancer Gene Census, IntOGen, biomarcadores de câncer
3. **known_drug:** Precedência clínica de fármacos aprovados/clínicos
4. **affected_pathway:** Telas CRISPR, análises de via, assinaturas gênicas
5. **rna_expression:** Expressão diferencial do Expression Atlas
6. **animal_model:** Fenótipos de camundongo do IMPC
7. **literature:** Text-mining da Europe PMC

Consulte `references/evidence_types.md` para descrições detalhadas de todos os tipos de evidência e diretrizes de interpretação.

### 5. Encontrar Fármacos Conhecidos

Identifique fármacos usados para uma doença e seus alvos.

```python
from scripts.query_opentargets import get_known_drugs_for_disease

drugs = get_known_drugs_for_disease("EFO_0000249")

# drugs contém:
# - uniqueDrugs: Número total de fármacos únicos
# - uniqueTargets: Número total de alvos únicos
# - rows: Lista de registros fármaco-alvo-indicação com:
#   - drug: {name, drugType, maximumClinicalTrialPhase}
#   - targets: Genes alvo do fármaco
#   - phase: Fase de ensaio clínico para esta indicação
#   - status: Status do ensaio (ativo, concluído, etc.)
#   - mechanismOfAction: Como o fármaco funciona
```

**Fases clínicas:**
- Fase 4: Fármaco aprovado
- Fase 3: Ensaios clínicos em estágio tardio
- Fase 2: Ensaios em estágio intermediário
- Fase 1: Ensaios de segurança inicial

### 6. Obter Informações de Fármaco

Recupere informações detalhadas de fármaco, incluindo mecanismos e indicações.

```python
from scripts.query_opentargets import get_drug_info

drug_info = get_drug_info("CHEMBL25")

# Acesse:
# - name, synonyms: Identificadores de fármaco
# - drugType: Molécula pequena, anticorpo, etc.
# - maximumClinicalTrialPhase: Estágio de desenvolvimento
# - mechanismsOfAction: Alvo e tipo de ação
# - indications: Doenças com fases de ensaio
# - withdrawnNotice: Se retirado, motivos e países
```

### 7. Obter Todas as Associações para um Alvo

Encontre todas as doenças associadas a um alvo, opcionalmente filtrando por pontuação.

```python
from scripts.query_opentargets import get_target_associations

# Obter associações com pontuação >= 0,5
associations = get_target_associations(
    ensembl_id="ENSG00000157764",
    min_score=0.5
)

# Cada associação contém:
# - disease: {id, name}
# - score: Pontuação geral de associação (0-1)
# - datatypeScores: Detalhamento por tipo de evidência
```

**Pontuações de associação:**
- Intervalo: 0-1 (maior = evidência mais forte)
- Agregue evidências em todos os tipos de dados usando soma harmônica
- NÃO são scores de confiança, mas métricas de ranking relativo
- Doenças pouco estudadas podem ter scores menores apesar de boa evidência

## Detalhes da API GraphQL

**Para consultas personalizadas além das funções auxiliares fornecidas**, use a API GraphQL diretamente ou modifique `scripts/query_opentargets.py`.

Informações principais:
- **Endpoint:** `https://api.platform.opentargets.org/api/v4/graphql`
- **Browser interativo:** `https://api.platform.opentargets.org/api/v4/graphql/browser`
- **Autenticação não necessária**
- **Solicite apenas campos necessários** para minimizar tamanho de resposta
- **Use paginação** para grandes conjuntos de resultados: `page: {size: N, index: M}`

Consulte `references/api_reference.md` para:
- Documentação completa do endpoint
- Consultas de exemplo para todos os tipos de entidade
- Padrões de tratamento de erros
- Melhores práticas para uso de API

## Melhores Práticas

### Estratégia de Priorização de Alvo

Ao priorizar alvos de medicamentos:

1. **Comece com evidência genética:** Genética humana (GWAS, variantes raras) fornece relevância de doença mais forte
2. **Verifique tratabilidade:** Prefira alvos com precedência clínica ou de descoberta
3. **Avalie segurança:** Revise responsabilidades de segurança, padrões de expressão e constraint genético
4. **Avalie precedência clínica:** Fármacos conhecidos indicam tratabilidade e janela terapêutica
5. **Considere múltiplos tipos de evidência:** Evidência convergente de fontes diferentes aumenta confiança
6. **Valide mecanicamente:** Evidência de via e plausibilidade biológica
7. **Revise literatura manualmente:** Para decisões críticas, examine publicações primárias

### Interpretação de Evidências

**Indicadores de evidência forte:**
- Múltiplas fontes de evidência independentes
- Scores altos de associação genética (especialmente GWAS com L2G > 0,5)
- Precedência clínica de fármacos aprovados
- Variantes ClinVar patogênicas com concordância de doença
- Modelos de camundongo com fenótipos relevantes

**Sinais de cautela:**
- Apenas uma única fonte de evidência
- Text-mining como única evidência (requer validação manual)
- Evidência conflitante entre fontes
- Alta essencialidade + expressão onipresente (janela terapêutica ruim)
- Múltiplas responsabilidades de segurança

**Interpretação de pontuação:**
- Scores classificam força relativa, não confiança absoluta
- Doenças pouco estudadas têm scores menores apesar de alvos potencialmente válidos
- Pese fontes curadas por especialistas mais altas que predições computacionais
- Verifique detalhamento de evidências, não apenas score geral

### Fluxos de Trabalho Comuns

**Fluxo de Trabalho 1: Descoberta de Alvo para uma Doença**
1. Pesquisar doença → obter ID EFO
2. Consultar informação de doença com `include_targets=True`
3. Revisar principais alvos classificados por score de associação
4. Para alvos promissores, obter informação detalhada de alvo
5. Examinar tipos de evidência apoiando cada associação
6. Avaliar tratabilidade e segurança para alvos priorizados

**Fluxo de Trabalho 2: Validação de Alvo**
1. Pesquisar alvo → obter ID Ensembl
2. Obter informação abrangente de alvo
3. Verificar tratabilidade (especialmente precedência clínica)
4. Revisar responsabilidades de segurança e constraint genético
5. Examinar associações de doença para entender biologia
6. Procurar por chemical probes ou compostos ferramentas
7. Verificar fármacos conhecidos alvo do gene para insights de mecanismo

**Fluxo de Trabalho 3: Reposicionamento de Fármaco**
1. Pesquisar doença → obter ID EFO
2. Obter fármacos conhecidos para doença
3. Para cada fármaco, obter informação detalhada de fármaco
4. Examinar mecanismos de ação e alvos
5. Procurar por indicações de doença relacionadas
6. Avaliar fases de ensaios clínicos e status
7. Identificar oportunidades de reposicionamento com base no mecanismo

**Fluxo de Trabalho 4: Inteligência Competitiva**
1. Pesquisar alvo de interesse
2. Obter doenças associadas com evidência
3. Para cada doença, obter fármacos conhecidos
4. Revisar fases clínicas e status de desenvolvimento
5. Identificar competidores e seus mecanismos
6. Avaliar precedência clínica e panorama de mercado

## Recursos

### Scripts

**scripts/query_opentargets.py**
Funções auxiliares para operações de API comuns:
- `search_entities()` - Pesquisar alvos, doenças ou fármacos
- `get_target_info()` - Recuperar anotações de alvo
- `get_disease_info()` - Recuperar informação de doença
- `get_target_disease_evidence()` - Obter evidência de apoio
- `get_known_drugs_for_disease()` - Encontrar fármacos para doença
- `get_drug_info()` - Recuperar detalhes de fármaco
- `get_target_associations()` - Obter todas as associações para alvo
- `execute_query()` - Executar consultas GraphQL personalizadas

### Referências

**references/api_reference.md**
Documentação completa de API GraphQL incluindo:
- Detalhes de endpoint e autenticação
- Tipos de consulta disponíveis (target, disease, drug, search)
- Consultas de exemplo para todas as operações comuns
- Tratamento de erros e melhores práticas
- Requisitos de licença de dados e citação

**references/evidence_types.md**
Guia abrangente de tipos de evidência e fontes de dados:
- Descrições detalhadas de todos os 7 principais tipos de evidência
- Metodologias de pontuação para cada fonte
- Diretrizes de interpretação de evidência
- Forças e limitações de cada tipo de evidência
- Recomendações de avaliação de qualidade

**references/target_annotations.md**
Referência completa de anotação de alvo:
- 12 principais categorias de anotação explicadas
- Detalhes de avaliação de tratabilidade
- Fontes de responsabilidade de segurança
- Dados de expressão, essencialidade e constraint
- Diretrizes de interpretação para priorização de alvo
- Red flags e green flags para avaliação de alvo

## Atualizações de Dados e Controle de Versão

A Plataforma Open Targets é atualizada **trimestralmente** com novos lançamentos de dados. A versão atual (em outubro de 2025) está disponível no endpoint de API.

**Informação de lançamento:** Verifique https://platform-docs.opentargets.org/release-notes para as atualizações mais recentes.

**Citação:** Ao usar dados do Open Targets, cite:
Ochoa, D. et al. (2025) Open Targets Platform: facilitating therapeutic hypotheses building in drug discovery. Nucleic Acids Research, 53(D1):D1467-D1477.

## Limitações e Considerações

1. **API é para consultas exploratórias:** Para análises sistemáticas de muitos alvos/doenças, use downloads de dados ou BigQuery
2. **Scores são relativos, não absolutos:** Scores de associação classificam força de evidência mas não predizem sucesso clínico
3. **Doenças pouco estudadas têm scores menores:** Doenças novas ou raras podem ter forte evidência mas scores agregados menores
4. **Qualidade de evidência varia:** Pese fontes curadas por especialistas mais altas que predições computacionais
5. **Requer interpretação biológica:** Scores e evidências devem ser interpretados em contexto biológico e clínico
6. **Autenticação não necessária:** Todos os dados são livremente acessíveis, mas cite apropriadamente