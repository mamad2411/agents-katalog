---
name: string-database
description: "Consulta a API STRING para interações proteína-proteína (59M proteínas, 20B interações). Análise de redes, enriquecimento GO/KEGG, descoberta de interações, 5000+ espécies, para biologia de sistemas."
---

# Banco de Dados STRING

## Visão Geral

STRING é um banco de dados abrangente de interações proteína-proteína conhecidas e preditas, cobrindo 59M proteínas e 20B+ interações em 5000+ organismos. Consulte redes de interação, execute análise de enriquecimento funcional, descubra parceiros via REST API para biologia de sistemas e análise de vias.

## Quando Usar Esta Habilidade

Esta habilidade deve ser usada quando:
- Recuperar redes de interação proteína-proteína para uma ou múltiplas proteínas
- Executar análise de enriquecimento funcional (GO, KEGG, Pfam) em listas de proteínas
- Descobrir parceiros de interação e expandir redes de proteínas
- Testar se proteínas formam módulos funcionais significativamente enriquecidos
- Gerar visualizações de rede com coloração baseada em evidência
- Analisar homologia e relações de família de proteínas
- Conduzir comparações de interação proteína entre espécies
- Identificar proteínas hub e padrões de conectividade de rede

## Início Rápido

A habilidade fornece:
1. Funções auxiliares Python (`scripts/string_api.py`) para todas as operações REST API do STRING
2. Documentação de referência abrangente (`references/string_reference.md`) com especificações detalhadas de API

Quando usuários solicitarem dados STRING, determine qual operação é necessária e use a função apropriada de `scripts/string_api.py`.

## Operações Principais

### 1. Mapeamento de Identificadores (`string_map_ids`)

Converta nomes de genes, nomes de proteínas e IDs externos para identificadores STRING.

**Quando usar**: Iniciando qualquer análise STRING, validando nomes de proteínas, encontrando identificadores canônicos.

**Uso**:
```python
from scripts.string_api import string_map_ids

# Mapear proteína única
result = string_map_ids('TP53', species=9606)

# Mapear múltiplas proteínas
result = string_map_ids(['TP53', 'BRCA1', 'EGFR', 'MDM2'], species=9606)

# Mapear com múltiplas correspondências por consulta
result = string_map_ids('p53', species=9606, limit=5)
```

**Parâmetros**:
- `species`: ID de táxon NCBI (9606 = humano, 10090 = camundongo, 7227 = mosca)
- `limit`: Número de correspondências por identificador (padrão: 1)
- `echo_query`: Incluir termo de consulta na saída (padrão: 1)

**Melhor prática**: Sempre mapeie identificadores primeiro para consultas subsequentes mais rápidas.

### 2. Recuperação de Rede (`string_network`)

Obtenha dados de rede de interação proteína-proteína em formato tabular.

**Quando usar**: Construindo redes de interação, analisando conectividade, recuperando evidência de interação.

**Uso**:
```python
from scripts.string_api import string_network

# Obter rede para proteína única
network = string_network('9606.ENSP00000269305', species=9606)

# Obter rede com múltiplas proteínas
proteins = ['9606.ENSP00000269305', '9606.ENSP00000275493']
network = string_network(proteins, required_score=700)

# Expandir rede com interatores adicionais
network = string_network('TP53', species=9606, add_nodes=10, required_score=400)

# Apenas interações físicas
network = string_network('TP53', species=9606, network_type='physical')
```

**Parâmetros**:
- `required_score`: Limiar de confiança (0-1000)
  - 150: confiança baixa (exploratória)
  - 400: confiança média (padrão, análise padrão)
  - 700: confiança alta (conservadora)
  - 900: confiança mais alta (muito rigorosa)
- `network_type`: `'functional'` (todas as evidências, padrão) ou `'physical'` (apenas ligação direta)
- `add_nodes`: Adicionar N proteínas mais conectadas (0-10)

**Colunas de saída**: Pares de interação, pontuações de confiança e pontuações de evidência individual (vizinhança, fusão, coexpressão, experimental, banco de dados, mineração de texto).

### 3. Visualização de Rede (`string_network_image`)

Gere visualização de rede como imagem PNG.

**Quando usar**: Criando figuras, exploração visual, apresentações.

**Uso**:
```python
from scripts.string_api import string_network_image

# Obter imagem de rede
proteins = ['TP53', 'MDM2', 'ATM', 'CHEK2', 'BRCA1']
img_data = string_network_image(proteins, species=9606, required_score=700)

# Salvar imagem
with open('network.png', 'wb') as f:
    f.write(img_data)

# Rede colorida por evidência
img = string_network_image(proteins, species=9606, network_flavor='evidence')

# Visualização baseada em confiança
img = string_network_image(proteins, species=9606, network_flavor='confidence')

# Rede de ações (ativação/inibição)
img = string_network_image(proteins, species=9606, network_flavor='actions')
```

**Sabores de rede**:
- `'evidence'`: Linhas coloridas mostram tipos de evidência (padrão)
- `'confidence'`: A espessura da linha representa confiança
- `'actions'`: Mostra relações de ativação/inibição

### 4. Parceiros de Interação (`string_interaction_partners`)

Encontre todas as proteínas que interagem com proteína(s) fornecida(s).

**Quando usar**: Descobrindo novas interações, encontrando proteínas hub, expandindo redes.

**Uso**:
```python
from scripts.string_api import string_interaction_partners

# Obter top 10 interatores de TP53
partners = string_interaction_partners('TP53', species=9606, limit=10)

# Obter interatores de alta confiança
partners = string_interaction_partners('TP53', species=9606,
                                      limit=20, required_score=700)

# Encontrar interatores para múltiplas proteínas
partners = string_interaction_partners(['TP53', 'MDM2'],
                                      species=9606, limit=15)
```

**Parâmetros**:
- `limit`: Número máximo de parceiros a retornar (padrão: 10)
- `required_score`: Limiar de confiança (0-1000)

**Casos de uso**:
- Identificação de proteína hub
- Expansão de rede a partir de proteínas sementes
- Descoberta de conexões indiretas

### 5. Enriquecimento Funcional (`string_enrichment`)

Execute análise de enriquecimento em Gene Ontology, vias KEGG, domínios Pfam e mais.

**Quando usar**: Interpretando listas de proteínas, análise de vias, caracterização funcional, entendendo processos biológicos.

**Uso**:
```python
from scripts.string_enrichment import string_enrichment

# Enriquecimento para lista de proteínas
proteins = ['TP53', 'MDM2', 'ATM', 'CHEK2', 'BRCA1', 'ATR', 'TP73']
enrichment = string_enrichment(proteins, species=9606)

# Analisar resultados para encontrar termos significativos
import pandas as pd
df = pd.read_csv(io.StringIO(enrichment), sep='\t')
significant = df[df['fdr'] < 0.05]
```

**Categorias de enriquecimento**:
- **Gene Ontology**: Processo Biológico, Função Molecular, Componente Celular
- **Vias KEGG**: Vias metabólicas e de sinalização
- **Pfam**: Domínios de proteína
- **InterPro**: Famílias e domínios de proteína
- **SMART**: Arquitetura de domínio
- **Palavras-chave UniProt**: Palavras-chave funcionais curadas

**Colunas de saída**:
- `category`: Banco de dados de anotação (ex.: "KEGG Pathways", "GO Biological Process")
- `term`: Identificador de termo
- `description`: Descrição legível do termo
- `number_of_genes`: Proteínas de entrada com esta anotação
- `p_value`: Valor p de enriquecimento não corrigido
- `fdr`: Taxa de descoberta falsa (valor p corrigido)

**Método estatístico**: Teste exato de Fisher com correção FDR de Benjamini-Hochberg.

**Interpretação**: FDR < 0,05 indica enriquecimento estatisticamente significativo.

### 6. Enriquecimento de PPI (`string_ppi_enrichment`)

Teste se uma rede de proteína tem significativamente mais interações do que o esperado pelo acaso.

**Quando usar**: Validando se proteínas formam módulo funcional, testando conectividade de rede.

**Uso**:
```python
from scripts.string_api import string_ppi_enrichment
import json

# Testar conectividade de rede
proteins = ['TP53', 'MDM2', 'ATM', 'CHEK2', 'BRCA1']
result = string_ppi_enrichment(proteins, species=9606, required_score=400)

# Analisar resultado JSON
data = json.loads(result)
print(f"Arestas observadas: {data['number_of_edges']}")
print(f"Arestas esperadas: {data['expected_number_of_edges']}")
print(f"Valor p: {data['p_value']}")
```

**Campos de saída**:
- `number_of_nodes`: Proteínas na rede
- `number_of_edges`: Interações observadas
- `expected_number_of_edges`: Esperadas em rede aleatória
- `p_value`: Significância estatística

**Interpretação**:
- valor p < 0,05: Rede é significativamente enriquecida (proteínas provavelmente formam módulo funcional)
- valor p ≥ 0,05: Sem enriquecimento significativo (proteínas podem ser não relacionadas)

### 7. Pontuações de Homologia (`string_homology`)

Recupere informações de similaridade de proteína e homologia.

**Quando usar**: Identificando famílias de proteínas, análise de paráloga, comparações entre espécies.

**Uso**:
```python
from scripts.string_api import string_homology

# Obter homologia entre proteínas
proteins = ['TP53', 'TP63', 'TP73']  # família p53
homology = string_homology(proteins, species=9606)
```

**Casos de uso**:
- Identificação de família de proteína
- Descoberta de paráloga
- Análise evolutiva

### 8. Informações de Versão (`string_version`)

Obtenha versão atual do banco de dados STRING.

**Quando usar**: Garantindo reprodutibilidade, documentando métodos.

**Uso**:
```python
from scripts.string_api import string_version

version = string_version()
print(f"Versão STRING: {version}")
```

## Fluxos de Trabalho Comuns

### Fluxo de Trabalho 1: Análise de Lista de Proteínas (Fluxo de Trabalho Padrão)

**Caso de uso**: Analisar lista de proteínas de experimento (ex.: expressão diferencial, proteômica).

```python
from scripts.string_api import (string_map_ids, string_network,
                                string_enrichment, string_ppi_enrichment,
                                string_network_image)

# Etapa 1: Mapear nomes de genes para IDs STRING
gene_list = ['TP53', 'BRCA1', 'ATM', 'CHEK2', 'MDM2', 'ATR', 'BRCA2']
mapping = string_map_ids(gene_list, species=9606)

# Etapa 2: Obter rede de interação
network = string_network(gene_list, species=9606, required_score=400)

# Etapa 3: Testar se rede é enriquecida
ppi_result = string_ppi_enrichment(gene_list, species=9606)

# Etapa 4: Executar enriquecimento funcional
enrichment = string_enrichment(gene_list, species=9606)

# Etapa 5: Gerar visualização de rede
img = string_network_image(gene_list, species=9606,
                          network_flavor='evidence', required_score=400)
with open('protein_network.png', 'wb') as f:
    f.write(img)

# Etapa 6: Analisar e interpretar resultados
```

### Fluxo de Trabalho 2: Investigação de Proteína Única

**Caso de uso**: Investigação profunda nas interações e parceiros de uma proteína.

```python
from scripts.string_api import (string_map_ids, string_interaction_partners,
                                string_network_image)

# Etapa 1: Mapear nome de proteína
protein = 'TP53'
mapping = string_map_ids(protein, species=9606)

# Etapa 2: Obter todos os parceiros de interação
partners = string_interaction_partners(protein, species=9606,
                                      limit=20, required_score=700)

# Etapa 3: Visualizar rede expandida
img = string_network_image(protein, species=9606, add_nodes=15,
                          network_flavor='confidence', required_score=700)
with open('tp53_network.png', 'wb') as f:
    f.write(img)
```

### Fluxo de Trabalho 3: Análise Centrada em Vias

**Caso de uso**: Identificar e visualizar proteínas em uma via biológica específica.

```python
from scripts.string_api import string_enrichment, string_network

# Etapa 1: Começar com proteínas conhecidas de via
dna_repair_proteins = ['TP53', 'ATM', 'ATR', 'CHEK1', 'CHEK2',
                       'BRCA1', 'BRCA2', 'RAD51', 'XRCC1']

# Etapa 2: Obter rede
network = string_network(dna_repair_proteins, species=9606,
                        required_score=700, add_nodes=5)

# Etapa 3: Enriquecimento para confirmar anotação de via
enrichment = string_enrichment(dna_repair_proteins, species=9606)

# Etapa 4: Analisar enriquecimento para vias de reparo de DNA
import pandas as pd
import io
df = pd.read_csv(io.StringIO(enrichment), sep='\t')
dna_repair = df[df['description'].str.contains('DNA repair', case=False)]
```

### Fluxo de Trabalho 4: Análise Entre Espécies

**Caso de uso**: Comparar interações de proteína entre diferentes organismos.

```python
from scripts.string_api import string_network

# Rede humana
human_network = string_network('TP53', species=9606, required_score=700)

# Rede de camundongo
mouse_network = string_network('Trp53', species=10090, required_score=700)

# Rede de levedura (se ortólogo existir)
yeast_network = string_network('gene_name', species=4932, required_score=700)
```

### Fluxo de Trabalho 5: Expansão de Rede e Descoberta

**Caso de uso**: Começar com proteínas sementes e descobrir módulos funcionais conectados.

```python
from scripts.string_api import (string_interaction_partners, string_network,
                                string_enrichment)

# Etapa 1: Começar com proteína(s) semente
seed_proteins = ['TP53']

# Etapa 2: Obter interatores de primeiro grau
partners = string_interaction_partners(seed_proteins, species=9606,
                                      limit=30, required_score=700)

# Etapa 3: Analisar parceiros para obter lista de proteína
import pandas as pd
import io
df = pd.read_csv(io.StringIO(partners), sep='\t')
all_proteins = list(set(df['preferredName_A'].tolist() +
                       df['preferredName_B'].tolist()))

# Etapa 4: Executar enriquecimento em rede expandida
enrichment = string_enrichment(all_proteins[:50], species=9606)

# Etapa 5: Filtrar para módulos funcionais interessantes
enrichment_df = pd.read_csv(io.StringIO(enrichment), sep='\t')
modules = enrichment_df[enrichment_df['fdr'] < 0.001]
```

## Espécies Comuns

Ao especificar espécies, use IDs de táxon NCBI:

| Organismo | Nome Comum | ID Táxon |
|----------|-------------|----------|
| Homo sapiens | Humano | 9606 |
| Mus musculus | Camundongo | 10090 |
| Rattus norvegicus | Rato | 10116 |
| Drosophila melanogaster | Mosca-da-fruta | 7227 |
| Caenorhabditis elegans | C. elegans | 6239 |
| Saccharomyces cerevisiae | Levedura | 4932 |
| Arabidopsis thaliana | Arabidopsis | 3702 |
| Escherichia coli | E. coli | 511145 |
| Danio rerio | Peixe-zebra | 7955 |

Lista completa disponível em: https://string-db.org/cgi/input?input_page_active_form=organisms

## Entendendo Pontuações de Confiança

STRING fornece pontuações de confiança combinadas (0-1000) integrando múltiplos tipos de evidência:

### Canais de Evidência

1. **Vizinhança (nscore)**: Vizinhança genômica conservada entre espécies
2. **Fusão (fscore)**: Eventos de fusão gênica
3. **Perfil Filogenético (pscore)**: Padrões de co-ocorrência entre espécies
4. **Coexpressão (ascore)**: Expressão de RNA correlacionada
5. **Experimental (escore)**: Experimentos bioquímicos e genéticos
6. **Banco de Dados (dscore)**: Vias curadas e bancos de dados de complexos
7. **Mineração de Texto (tscore)**: Co-ocorrência em literatura e extração por PNL

### Limiares Recomendados

Escolha limiar baseado nos objetivos de análise:

- **150 (confiança baixa)**: Análise exploratória, geração de hipóteses
- **400 (confiança média)**: Análise padrão, sensibilidade/especificidade equilibrada
- **700 (confiança alta)**: Análise conservadora, interações de alta confiança
- **900 (confiança mais alta)**: Muito rigoroso, evidência experimental preferida

**Compensações**:
- Limiares mais baixos: Mais interações (recall mais alto, mais falsos positivos)
- Limiares mais altos: Menos interações (precisão mais alta, mais falsos negativos)

## Tipos de Rede

### Redes Funcionais (Padrão)

Inclui todos os tipos de evidência (experimental, computacional, mineração de texto). Representa proteínas que são funcionalmente associadas, mesmo sem ligação física direta.

**Quando usar**:
- Análise de vias
- Estudos de enriquecimento funcional
- Biologia de sistemas
- Maioria das análises gerais

### Redes Físicas

Inclui apenas evidência de ligação física direta (dados experimentais e anotações de banco de dados para interações físicas).

**Quando usar**:
- Estudos de biologia estrutural
- Análise de complexo de proteína
- Validação de ligação direta
- Quando contato físico é necessário

## Melhores Práticas de API

1. **Sempre mapeie identificadores primeiro**: Use `string_map_ids()` antes de outras operações para consultas mais rápidas
2. **Use IDs STRING quando possível**: Use formato `9606.ENSP00000269305` em vez de nomes de genes
3. **Especifique espécie para redes >10 proteínas**: Obrigatório para resultados precisos
4. **Respeite limites de taxa**: Aguarde 1 segundo entre chamadas de API
5. **Use URLs versionadas para reprodutibilidade**: Disponível na documentação de referência
6. **Trate erros com elegância**: Verifique prefixo "Error:" em strings retornadas
7. **Escolha limiares de confiança apropriados**: Combine limiar com objetivos de análise

## Referência Detalhada

Para documentação abrangente de API, listas completas de parâmetros, formatos de saída e uso avançado, consulte `references/string_reference.md`. Isso inclui:

- Especificações completas de endpoint de API
- Todos os formatos de saída suportados (TSV, JSON, XML, PSI-MI)
- Recursos avançados (upload em massa, enriquecimento de valores/ranks)
- Tratamento de erros e troubleshooting
- Integração com outras ferramentas (Cytoscape, R, bibliotecas Python)
- Licença de dados e informações de citação

## Troubleshooting

**Nenhuma proteína encontrada**:
- Verifique se parâmetro species corresponde aos identificadores
- Tente mapear identificadores primeiro com `string_map_ids()`
- Verifique erros de digitação em nomes de proteínas

**Resultados de rede vazios**:
- Diminua limiar de confiança (`required_score`)
- Verifique se proteínas realmente interagem
- Verifique se species está correto

**Timeout ou consultas lentas**:
- Reduza número de proteínas de entrada
- Use IDs STRING em vez de nomes de genes
- Divida consultas grandes em lotes

**Erro "Species required"**:
- Adicione parâmetro `species` para redes com >10 proteínas
- Sempre inclua species para consistência

**Resultados parecem inesperados**:
- Verifique versão STRING com `string_version()`
- Verifique se network_type é apropriado (funcional vs físico)
- Revise seleção de limiar de confiança

## Recursos Adicionais

Para análise em escala de proteoma ou upload completo de rede de espécie:
- Visite https://string-db.org
- Use recurso "Upload proteome"
- STRING gerará rede de interação completa e preverá funções

Para downloads em massa de conjuntos de dados completos:
- Página de download: https://string-db.org/cgi/download
- Inclui arquivos de interação completos, anotações de proteína e mapeamentos de vias

## Licença de Dados

Os dados STRING estão livremente disponíveis sob licença **Creative Commons BY 4.0**:
- Livre para uso acadêmico e comercial
- Atribuição necessária ao publicar
- Cite publicação STRING mais recente

## Citação

Ao usar STRING em publicações, cite a publicação mais recente em: https://string-db.org/cgi/about