---
name: metabolomics-workbench-database
description: "Acesso à Metabolomics Workbench do NIH via REST API (4.200+ estudos). Consulte metabolitos, nomenclatura RefMet, dados MS/NMR, buscas m/z, metadados de estudos, para descoberta de metabolômica e biomarcadores."
---

# Banco de Dados Metabolomics Workbench

## Visão Geral

A Metabolomics Workbench é uma plataforma abrangente patrocinada pelo NIH Common Fund hospedada na UCSD que funciona como o repositório primário para dados de pesquisa em metabolômica. Ela oferece acesso programático a mais de 4.200 estudos processados (3.790+ disponíveis publicamente), nomenclatura de metabolitos padronizada através da RefMet, e poderosas capacidades de busca em múltiplas plataformas analíticas (GC-MS, LC-MS, NMR).

## Quando Usar Esta Habilidade

Esta habilidade deve ser usada ao consultar estruturas de metabolitos, acessar dados de estudos, padronizar nomenclatura, realizar buscas de espectrometria de massa, ou recuperar associações gene/proteína-metabolito através da REST API da Metabolomics Workbench.

## Capacidades Principais

### 1. Consultando Estruturas e Dados de Metabolitos

Acesse informações abrangentes de metabolitos, incluindo estruturas, identificadores e referências cruzadas para bancos de dados externos.

**Operações principais:**
- Recupere dados de compostos por vários identificadores (PubChem CID, InChI Key, KEGG ID, HMDB ID, etc.)
- Baixe estruturas moleculares como arquivos MOL ou imagens PNG
- Acesse classificações de compostos padronizadas
- Faça referências cruzadas entre diferentes bancos de dados de metabolitos

**Exemplos de consultas:**
```python
import requests

# Obter informações de compostos por PubChem CID
response = requests.get('https://www.metabolomicsworkbench.org/rest/compound/pubchem_cid/5281365/all/json')

# Baixar estrutura molecular como PNG
response = requests.get('https://www.metabolomicsworkbench.org/rest/compound/regno/11/png')

# Obter nome do composto por número de registro
response = requests.get('https://www.metabolomicsworkbench.org/rest/compound/regno/11/name/json')
```

### 2. Acessando Metadados de Estudos e Resultados Experimentais

Consulte estudos de metabolômica por vários critérios e recupere conjuntos de dados experimentais completos.

**Operações principais:**
- Busque estudos por metabolito, instituto, investigador ou título
- Acesse resumos de estudos, fatores experimentais e detalhes de análise
- Recupere dados experimentais completos em vários formatos
- Baixe arquivos no formato mwTab para informações completas do estudo
- Consulte dados de metabolômica não direcionada

**Exemplos de consultas:**
```python
# Listar todos os estudos públicos disponíveis
response = requests.get('https://www.metabolomicsworkbench.org/rest/study/study_id/ST/available/json')

# Obter resumo do estudo
response = requests.get('https://www.metabolomicsworkbench.org/rest/study/study_id/ST000001/summary/json')

# Recuperar dados experimentais
response = requests.get('https://www.metabolomicsworkbench.org/rest/study/study_id/ST000001/data/json')

# Encontrar estudos contendo um metabolito específico
response = requests.get('https://www.metabolomicsworkbench.org/rest/study/refmet_name/Tyrosine/summary/json')
```

### 3. Padronizando Nomenclatura de Metabolitos com RefMet

Use o banco de dados RefMet para padronizar nomes de metabolitos e acessar classificação sistemática em quatro níveis de resolução estrutural.

**Operações principais:**
- Associe nomes comuns de metabolitos a nomes RefMet padronizados
- Consulte por fórmula química, massa exata ou InChI Key
- Acesse classificação hierárquica (superclasse, classe principal, subclasse)
- Recupere todas as entradas RefMet ou filtre por classificação

**Exemplos de consultas:**
```python
# Padronizar um nome de metabolito
response = requests.get('https://www.metabolomicsworkbench.org/rest/refmet/match/citrate/name/json')

# Consultar por fórmula molecular
response = requests.get('https://www.metabolomicsworkbench.org/rest/refmet/formula/C12H24O2/all/json')

# Obter todos os metabolitos em uma classe específica
response = requests.get('https://www.metabolomicsworkbench.org/rest/refmet/main_class/Fatty%20Acids/all/json')

# Recuperar banco de dados RefMet completo
response = requests.get('https://www.metabolomicsworkbench.org/rest/refmet/all/json')
```

### 4. Realizando Buscas de Espectrometria de Massa

Busque compostos por razão massa-carga (m/z) com tipos de íons aduto e níveis de tolerância especificados.

**Operações principais:**
- Busque massas de íons precursores em múltiplos bancos de dados (Metabolomics Workbench, LIPIDS, RefMet)
- Especifique tipos de íons aduto (M+H, M-H, M+Na, M+NH4, M+2H, etc.)
- Calcule massas exatas para metabolitos conhecidos com adutos específicos
- Defina tolerância de massa para correspondência flexível

**Exemplos de consultas:**
```python
# Buscar por valor de m/z com aduto M+H
response = requests.get('https://www.metabolomicsworkbench.org/rest/moverz/MB/635.52/M+H/0.5/json')

# Calcular massa exata para um metabolito com aduto específico
response = requests.get('https://www.metabolomicsworkbench.org/rest/moverz/exactmass/PC(34:1)/M+H/json')

# Buscar no banco de dados RefMet
response = requests.get('https://www.metabolomicsworkbench.org/rest/moverz/REFMET/200.15/M-H/0.3/json')
```

### 5. Filtrando Estudos por Parâmetros Analíticos e Biológicos

Use o contexto MetStat para encontrar estudos que correspondam a condições experimentais específicas.

**Operações principais:**
- Filtre por método analítico (LCMS, GCMS, NMR)
- Especifique polaridade de ionização (POSITIVE, NEGATIVE)
- Filtre por tipo de cromatografia (HILIC, RP, GC)
- Direcione espécies específicas, fontes de amostra ou doenças
- Combine múltiplos filtros usando formato delimitado por ponto-e-vírgula

**Exemplos de consultas:**
```python
# Encontrar estudos de sangue humano em diabetes usando LC-MS
response = requests.get('https://www.metabolomicsworkbench.org/rest/metstat/LCMS;POSITIVE;HILIC;Human;Blood;Diabetes/json')

# Encontrar todos os estudos de sangue humano contendo tirosina
response = requests.get('https://www.metabolomicsworkbench.org/rest/metstat/;;;Human;Blood;;;Tyrosine/json')

# Filtrar apenas por método analítico
response = requests.get('https://www.metabolomicsworkbench.org/rest/metstat/GCMS;;;;;;/json')
```

### 6. Acessando Informações de Gene e Proteína

Recupere dados de gene e proteína associados a vias metabólicas e metabolismo de metabolitos.

**Operações principais:**
- Consulte genes por símbolo, nome ou ID
- Acesse sequências de proteína e anotações
- Faça referências cruzadas entre IDs de genes, IDs RefSeq e IDs UniProt
- Recupere associações gene-metabolito

**Exemplos de consultas:**
```python
# Obter informações de gene por símbolo
response = requests.get('https://www.metabolomicsworkbench.org/rest/gene/gene_symbol/ACACA/all/json')

# Recuperar dados de proteína por ID UniProt
response = requests.get('https://www.metabolomicsworkbench.org/rest/protein/uniprot_id/Q13085/all/json')
```

## Fluxos de Trabalho Comuns

### Fluxo de Trabalho 1: Encontrando Estudos para um Metabolito Específico

Para encontrar todos os estudos contendo medições de um metabolito específico:

1. Primeiro, padronize o nome do metabolito usando RefMet:
   ```python
   response = requests.get('https://www.metabolomicsworkbench.org/rest/refmet/match/glucose/name/json')
   ```

2. Use o nome padronizado para buscar estudos:
   ```python
   response = requests.get('https://www.metabolomicsworkbench.org/rest/study/refmet_name/Glucose/summary/json')
   ```

3. Recupere dados experimentais de estudos específicos:
   ```python
   response = requests.get('https://www.metabolomicsworkbench.org/rest/study/study_id/ST000001/data/json')
   ```

### Fluxo de Trabalho 2: Identificando Compostos a partir de Dados MS

Para identificar compostos potenciais a partir de valores de m/z de espectrometria de massa:

1. Realize busca m/z com aduto apropriado e tolerância:
   ```python
   response = requests.get('https://www.metabolomicsworkbench.org/rest/moverz/MB/180.06/M+H/0.5/json')
   ```

2. Revise compostos candidatos dos resultados

3. Recupere informações detalhadas para compostos candidatos:
   ```python
   response = requests.get('https://www.metabolomicsworkbench.org/rest/compound/regno/{regno}/all/json')
   ```

4. Baixe estruturas para confirmação:
   ```python
   response = requests.get('https://www.metabolomicsworkbench.org/rest/compound/regno/{regno}/png')
   ```

### Fluxo de Trabalho 3: Explorando Metabolômica Específica de Doença

Para encontrar estudos de metabolômica para uma doença específica e plataforma analítica:

1. Use MetStat para filtrar estudos:
   ```python
   response = requests.get('https://www.metabolomicsworkbench.org/rest/metstat/LCMS;POSITIVE;;Human;;Cancer/json')
   ```

2. Revise IDs de estudos dos resultados

3. Acesse informações detalhadas do estudo:
   ```python
   response = requests.get('https://www.metabolomicsworkbench.org/rest/study/study_id/ST{ID}/summary/json')
   ```

4. Recupere dados experimentais completos:
   ```python
   response = requests.get('https://www.metabolomicsworkbench.org/rest/study/study_id/ST{ID}/data/json')
   ```

## Formatos de Saída

A API suporta dois formatos de saída primários:
- **JSON** (padrão): Formato legível por máquina, ideal para acesso programático
- **TXT**: Formato de texto com valores separados por tabulação, legível por humanos

Especifique o formato anexando `/json` ou `/txt` às URLs da API. Quando o formato é omitido, JSON é retornado por padrão.

## Melhores Práticas

1. **Use RefMet para padronização**: Sempre padronize nomes de metabolitos através da RefMet antes de buscar estudos para garantir nomenclatura consistente

2. **Especifique adutos apropriados**: Ao realizar buscas m/z, use o tipo de íon aduto correto para seu método analítico (ex: M+H para modo positivo ESI)

3. **Defina tolerâncias razoáveis**: Use valores de tolerância de massa apropriados (tipicamente 0,5 Da para MS de baixa resolução, 0,01 Da para MS de alta resolução)

4. **Cache de dados de referência**: Considere fazer cache de dados de referência frequentemente usados (banco de dados RefMet, informações de compostos) para minimizar chamadas de API

5. **Manipule paginação**: Para grandes conjuntos de resultados, esteja preparado para manipular múltiplas estruturas de dados nas respostas

6. **Valide identificadores**: Faça referências cruzadas de identificadores de metabolitos entre múltiplos bancos de dados quando possível para garantir identificação correta de compostos

## Recursos

### references/

Documentação detalhada de referência de API está disponível em `references/api_reference.md`, incluindo:
- Especificações completas de endpoints REST API
- Todos os contextos disponíveis (compound, study, refmet, metstat, gene, protein, moverz)
- Detalhes de parâmetros de entrada/saída
- Tipos de íons aduto para espectrometria de massa
- Exemplos adicionais de consultas

Carregue este arquivo de referência quando especificações de API detalhadas forem necessárias ou ao trabalhar com endpoints menos comuns.