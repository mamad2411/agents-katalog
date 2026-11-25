---
name: arboreto
description: Inferir redes regulatórias de genes (GRNs) a partir de dados de expressão gênica usando algoritmos escaláveis (GRNBoost2, GENIE3). Use ao analisar dados de transcriptômica (RNA-seq em bulk, RNA-seq de célula única) para identificar relações fator de transcrição-gene alvo e interações regulatórias. Suporta computação distribuída para conjuntos de dados em larga escala.
---

# Arboreto

## Visão Geral

Arboreto é uma biblioteca computacional para inferir redes regulatórias de genes (GRNs) a partir de dados de expressão gênica usando algoritmos paralelizados que escalam de máquinas individuais para clusters multi-nó.

**Capacidade principal**: Identificar quais fatores de transcrição (TFs) regulam quais genes alvo com base em padrões de expressão em observações (células, amostras, condições).

## Início Rápido

Instale arboreto:
```bash
uv pip install arboreto
```

Inferência básica de GRN:
```python
import pandas as pd
from arboreto.algo import grnboost2

if __name__ == '__main__':
    # Carregar dados de expressão (genes como colunas)
    expression_matrix = pd.read_csv('expression_data.tsv', sep='\t')

    # Inferir rede regulatória
    network = grnboost2(expression_data=expression_matrix)

    # Salvar resultados (TF, alvo, importância)
    network.to_csv('network.tsv', sep='\t', index=False, header=False)
```

**Crítico**: Sempre use o guard `if __name__ == '__main__':` porque Dask cria novos processos.

## Capacidades Principais

### 1. Inferência Básica de GRN

Para fluxos de trabalho padrão de inferência de GRN incluindo:
- Preparação de dados de entrada (Pandas DataFrame ou array NumPy)
- Execução de inferência com GRNBoost2 ou GENIE3
- Filtragem por fatores de transcrição
- Formato de saída e interpretação

**Veja**: `references/basic_inference.md`

**Use o script pronto para execução**: `scripts/basic_grn_inference.py` para tarefas padrão de inferência:
```bash
python scripts/basic_grn_inference.py expression_data.tsv output_network.tsv --tf-file tfs.txt --seed 777
```

### 2. Seleção de Algoritmo

Arboreto fornece dois algoritmos:

**GRNBoost2 (Recomendado)**:
- Inferência rápida baseada em gradient boosting
- Otimizado para conjuntos de dados grandes (10k+ observações)
- Escolha padrão para a maioria das análises

**GENIE3**:
- Inferência baseada em Random Forest
- Abordagem original de regressão múltipla
- Use para comparação ou validação

Comparação rápida:
```python
from arboreto.algo import grnboost2, genie3

# Rápido, recomendado
network_grnboost = grnboost2(expression_data=matrix)

# Algoritmo clássico
network_genie3 = genie3(expression_data=matrix)
```

**Para comparação detalhada de algoritmos, parâmetros e orientação de seleção**: `references/algorithms.md`

### 3. Computação Distribuída

Escale inferência de multi-núcleo local para ambientes em cluster:

**Local (padrão)** - Usa todos os núcleos disponíveis automaticamente:
```python
network = grnboost2(expression_data=matrix)
```

**Cliente local customizado** - Controle recursos:
```python
from distributed import LocalCluster, Client

local_cluster = LocalCluster(n_workers=10, memory_limit='8GB')
client = Client(local_cluster)

network = grnboost2(expression_data=matrix, client_or_address=client)

client.close()
local_cluster.close()
```

**Computação em cluster** - Conecte ao scheduler Dask remoto:
```python
from distributed import Client

client = Client('tcp://scheduler:8786')
network = grnboost2(expression_data=matrix, client_or_address=client)
```

**Para configuração de cluster, otimização de performance e fluxos de trabalho em larga escala**: `references/distributed_computing.md`

## Instalação

```bash
uv pip install arboreto
```

**Dependências**: scipy, scikit-learn, numpy, pandas, dask, distributed

## Casos de Uso Comuns

### Análise de RNA-seq de Célula Única
```python
import pandas as pd
from arboreto.algo import grnboost2

if __name__ == '__main__':
    # Carregar matriz de expressão de célula única (células x genes)
    sc_data = pd.read_csv('scrna_counts.tsv', sep='\t')

    # Inferir rede regulatória específica do tipo celular
    network = grnboost2(expression_data=sc_data, seed=42)

    # Filtrar links de alta confiança
    high_confidence = network[network['importance'] > 0.5]
    high_confidence.to_csv('grn_high_confidence.tsv', sep='\t', index=False)
```

### RNA-seq em Bulk com Filtragem de TF
```python
from arboreto.utils import load_tf_names
from arboreto.algo import grnboost2

if __name__ == '__main__':
    # Carregar dados
    expression_data = pd.read_csv('rnaseq_tpm.tsv', sep='\t')
    tf_names = load_tf_names('human_tfs.txt')

    # Inferir com restrição de TF
    network = grnboost2(
        expression_data=expression_data,
        tf_names=tf_names,
        seed=123
    )

    network.to_csv('tf_target_network.tsv', sep='\t', index=False)
```

### Análise Comparativa (Múltiplas Condições)
```python
from arboreto.algo import grnboost2

if __name__ == '__main__':
    # Inferir redes para diferentes condições
    conditions = ['control', 'treatment_24h', 'treatment_48h']

    for condition in conditions:
        data = pd.read_csv(f'{condition}_expression.tsv', sep='\t')
        network = grnboost2(expression_data=data, seed=42)
        network.to_csv(f'{condition}_network.tsv', sep='\t', index=False)
```

## Interpretação de Saída

Arboreto retorna um DataFrame com links regulatórios:

| Coluna | Descrição |
|--------|-----------|
| `TF` | Fator de transcrição (regulador) |
| `target` | Gene alvo |
| `importance` | Pontuação de importância regulatória (maior = mais forte) |

**Estratégia de filtragem**:
- Top N links por gene alvo
- Limiar de importância (ex: > 0.5)
- Testes de significância estatística (testes de permutação)

## Integração com pySCENIC

Arboreto é um componente principal do pipeline SCENIC para análise de rede regulatória de célula única:

```python
# Etapa 1: Use arboreto para inferência de GRN
from arboreto.algo import grnboost2
network = grnboost2(expression_data=sc_data, tf_names=tf_list)

# Etapa 2: Use pySCENIC para identificação de regulon e pontuação de atividade
# (Veja documentação do pySCENIC para análise downstream)
```

## Reprodutibilidade

Sempre defina uma seed para resultados reproduzíveis:
```python
network = grnboost2(expression_data=matrix, seed=777)
```

Execute múltiplas seeds para análise de robustez:
```python
from distributed import LocalCluster, Client

if __name__ == '__main__':
    client = Client(LocalCluster())

    seeds = [42, 123, 777]
    networks = []

    for seed in seeds:
        net = grnboost2(expression_data=matrix, client_or_address=client, seed=seed)
        networks.append(net)

    # Combinar redes e filtrar links de consenso
    consensus = analyze_consensus(networks)
```

## Solução de Problemas

**Erros de memória**: Reduza o tamanho do conjunto de dados filtrando genes de baixa variância ou use computação distribuída

**Performance lenta**: Use GRNBoost2 em vez de GENIE3, ative cliente distribuído, filtre lista de TF

**Erros de Dask**: Garanta que o guard `if __name__ == '__main__':` esteja presente em scripts

**Resultados vazios**: Verifique formato de dados (genes como colunas), confirme que nomes de TF correspondem aos nomes de genes