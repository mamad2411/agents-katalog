---
name: torchdrug
description: "Kit de ferramentas para descoberta de fármacos baseado em grafos. Predição de propriedades moleculares (ADMET), modelagem de proteínas, raciocínio em grafos de conhecimento, geração molecular, retrossíntese, GNNs (GIN, GAT, SchNet), 40+ conjuntos de dados, para aprendizado de máquina baseado em PyTorch em moléculas, proteínas e grafos biomédicos."
---

# TorchDrug

## Visão Geral

TorchDrug é uma caixa de ferramentas abrangente de aprendizado de máquina baseada em PyTorch para descoberta de fármacos e ciência molecular. Aplique redes neurais de grafos, modelos pré-treinados e definições de tarefas em moléculas, proteínas e grafos de conhecimento biológico, incluindo predição de propriedades moleculares, modelagem de proteínas, raciocínio em grafos de conhecimento, geração molecular, planejamento de retrossíntese, com 40+ conjuntos de dados curados e 20+ arquiteturas de modelo.

## Quando Usar Esta Skill

Esta skill deve ser usada ao trabalhar com:

**Tipos de Dados:**
- Cadeias SMILES ou estruturas moleculares
- Sequências de proteína ou estruturas 3D (arquivos PDB)
- Reações químicas e retrossíntese
- Grafos de conhecimento biomédicos
- Conjuntos de dados de descoberta de fármacos

**Tarefas:**
- Predição de propriedades moleculares (solubilidade, toxicidade, atividade)
- Predição de função ou estrutura de proteína
- Predição de ligação alvo-fármaco
- Geração de novas estruturas moleculares
- Planejamento de rotas de síntese química
- Predição de links em bases de conhecimento biomédicas
- Treinamento de redes neurais de grafos em dados científicos

**Bibliotecas e Integração:**
- TorchDrug é a biblioteca principal
- Frequentemente usado com RDKit para quiminformática
- Compatível com PyTorch e PyTorch Lightning
- Integra-se com AlphaFold e ESM para proteínas

## Começando

### Instalação

```bash
uv pip install torchdrug
# Ou com dependências opcionais
uv pip install torchdrug[full]
```

### Exemplo Rápido

```python
from torchdrug import datasets, models, tasks
from torch.utils.data import DataLoader

# Carregar conjunto de dados molecular
dataset = datasets.BBBP("~/molecule-datasets/")
train_set, valid_set, test_set = dataset.split()

# Definir modelo GNN
model = models.GIN(
    input_dim=dataset.node_feature_dim,
    hidden_dims=[256, 256, 256],
    edge_input_dim=dataset.edge_feature_dim,
    batch_norm=True,
    readout="mean"
)

# Criar tarefa de predição de propriedade
task = tasks.PropertyPrediction(
    model,
    task=dataset.tasks,
    criterion="bce",
    metric=["auroc", "auprc"]
)

# Treinar com PyTorch
optimizer = torch.optim.Adam(task.parameters(), lr=1e-3)
train_loader = DataLoader(train_set, batch_size=32, shuffle=True)

for epoch in range(100):
    for batch in train_loader:
        loss = task(batch)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
```

## Capacidades Principais

### 1. Predição de Propriedades Moleculares

Prediga propriedades químicas, físicas e biológicas de moléculas a partir da estrutura.

**Casos de Uso:**
- Propriedades de semelhança a fármacos e ADMET
- Triagem de toxicidade
- Propriedades de química quântica
- Predição de afinidade de ligação

**Componentes Principais:**
- 20+ conjuntos de dados moleculares (BBBP, HIV, Tox21, QM9, etc.)
- Modelos GNN (GIN, GAT, SchNet)
- Tarefas PropertyPrediction e MultipleBinaryClassification

**Referência:** Consulte `references/molecular_property_prediction.md` para:
- Catálogo completo de conjuntos de dados
- Guia de seleção de modelo
- Fluxos de trabalho de treinamento e melhores práticas
- Detalhes de engenharia de atributos

### 2. Modelagem de Proteínas

Trabalhe com sequências, estruturas e propriedades de proteínas.

**Casos de Uso:**
- Predição de função enzimática
- Estabilidade e solubilidade de proteína
- Localização subcelular
- Interações proteína-proteína
- Predição de estrutura

**Componentes Principais:**
- 15+ conjuntos de dados de proteína (EnzymeCommission, GeneOntology, PDBBind, etc.)
- Modelos de sequência (ESM, ProteinBERT, ProteinLSTM)
- Modelos de estrutura (GearNet, SchNet)
- Múltiplos tipos de tarefas para diferentes níveis de predição

**Referência:** Consulte `references/protein_modeling.md` para:
- Conjuntos de dados específicos de proteína
- Modelos de sequência vs estrutura
- Estratégias de pré-treinamento
- Integração com AlphaFold e ESM

### 3. Raciocínio em Grafos de Conhecimento

Prediga elos faltantes e relações em grafos de conhecimento biológico.

**Casos de Uso:**
- Reposicionamento de fármacos
- Descoberta de mecanismos de doença
- Associações gene-doença
- Raciocínio biomédico multi-hop

**Componentes Principais:**
- KGs gerais (FB15k, WN18) e biomédicos (Hetionet)
- Modelos de embedding (TransE, RotatE, ComplEx)
- Tarefa KnowledgeGraphCompletion

**Referência:** Consulte `references/knowledge_graphs.md` para:
- Conjuntos de dados de grafo de conhecimento (incluindo Hetionet com 45k entidades biomédicas)
- Comparação de modelos de embedding
- Métricas e protocolos de avaliação
- Aplicações biomédicas

### 4. Geração Molecular

Gere novas estruturas moleculares com propriedades desejadas.

**Casos de Uso:**
- Design de novo de fármacos
- Otimização de líderes
- Exploração de espaço químico
- Geração guiada por propriedades

**Componentes Principais:**
- Geração autorregressiva
- GCPN (geração baseada em política)
- GraphAutoregressiveFlow
- Fluxos de trabalho de otimização de propriedade

**Referência:** Consulte `references/molecular_generation.md` para:
- Estratégias de geração (incondicional, condicional, baseada em scaffold)
- Otimização multi-objetivo
- Validação e filtragem
- Integração com predição de propriedade

### 5. Retrossíntese

Prediga rotas sintéticas de moléculas-alvo para materiais de partida.

**Casos de Uso:**
- Planejamento de síntese
- Otimização de rota
- Avaliação de acessibilidade sintética
- Planejamento multi-etapa

**Componentes Principais:**
- Conjunto de dados de reação USPTO-50k
- CenterIdentification (predição de centro de reação)
- SynthonCompletion (predição de reagente)
- Pipeline de Retrosynthesis ponta-a-ponta

**Referência:** Consulte `references/retrosynthesis.md` para:
- Decomposição de tarefa (ID do centro → conclusão de synthon)
- Planejamento de síntese multi-etapa
- Verificação de disponibilidade comercial
- Integração com outras ferramentas de retrossíntese

### 6. Modelos de Rede Neural de Grafos

Catálogo abrangente de arquiteturas GNN para diferentes tipos de dados e tarefas.

**Modelos Disponíveis:**
- GNNs gerais: GCN, GAT, GIN, RGCN, MPNN
- Cientes de 3D: SchNet, GearNet
- Específicos de proteína: ESM, ProteinBERT, GearNet
- Grafo de conhecimento: TransE, RotatE, ComplEx, SimplE
- Generativo: GraphAutoregressiveFlow

**Referência:** Consulte `references/models_architectures.md` para:
- Descrições detalhadas de modelo
- Guia de seleção de modelo por tarefa e conjunto de dados
- Comparações de arquitetura
- Dicas de implementação

### 7. Conjuntos de Dados

40+ conjuntos de dados curados abrangendo química, biologia e grafos de conhecimento.

**Categorias:**
- Propriedades moleculares (descoberta de fármacos, química quântica)
- Propriedades de proteína (função, estrutura, interações)
- Grafos de conhecimento (gerais e biomédicos)
- Reações de retrossíntese

**Referência:** Consulte `references/datasets.md` para:
- Catálogo completo de conjuntos de dados com tamanhos e tarefas
- Guia de seleção de conjunto de dados
- Carregamento e pré-processamento
- Estratégias de divisão (aleatória, scaffold)

## Fluxos de Trabalho Comuns

### Fluxo de Trabalho 1: Predição de Propriedades Moleculares

**Cenário:** Prediga penetração da barreira hematoencefálica para candidatos a fármacos.

**Etapas:**
1. Carregue conjunto de dados: `datasets.BBBP()`
2. Escolha modelo: GIN para grafos moleculares
3. Defina tarefa: `PropertyPrediction` com classificação binária
4. Treine com divisão de scaffold para avaliação realista
5. Avalie usando AUROC e AUPRC

**Navegação:** `references/molecular_property_prediction.md` → Seleção de conjunto de dados → Seleção de modelo → Treinamento

### Fluxo de Trabalho 2: Predição de Função de Proteína

**Cenário:** Prediga função enzimática a partir da sequência.

**Etapas:**
1. Carregue conjunto de dados: `datasets.EnzymeCommission()`
2. Escolha modelo: ESM (pré-treinado) ou GearNet (com estrutura)
3. Defina tarefa: `PropertyPrediction` com classificação multi-classe
4. Fine-tune modelo pré-treinado ou treine do zero
5. Avalie usando acurácia e métricas por classe

**Navegação:** `references/protein_modeling.md` → Seleção de modelo (sequência vs estrutura) → Estratégias de pré-treinamento

### Fluxo de Trabalho 3: Reposicionamento de Fármacos via Grafos de Conhecimento

**Cenário:** Encontre novos tratamentos de doença em Hetionet.

**Etapas:**
1. Carregue conjunto de dados: `datasets.Hetionet()`
2. Escolha modelo: RotatE ou ComplEx
3. Defina tarefa: `KnowledgeGraphCompletion`
4. Treine com amostragem negativa
5. Consulte predições "Compound-treats-Disease"
6. Filtre por plausibilidade e mecanismo

**Navegação:** `references/knowledge_graphs.md` → Conjunto de dados Hetionet → Seleção de modelo → Aplicações biomédicas

### Fluxo de Trabalho 4: Geração de Novo de Moléculas

**Cenário:** Gere moléculas semelhantes a fármacos otimizadas para ligação-alvo.

**Etapas:**
1. Treine preditor de propriedade em dados de atividade
2. Escolha abordagem de geração: GCPN para otimização baseada em RL
3. Defina função de recompensa combinando afinidade, semelhança a fármacos, sintetizabilidade
4. Gere candidatos com restrições de propriedade
5. Valide química e filtre por semelhança a fármacos
6. Classifique por pontuação multi-objetivo

**Navegação:** `references/molecular_generation.md` → Geração condicional → Otimização multi-objetivo

### Fluxo de Trabalho 5: Planejamento de Retrossíntese

**Cenário:** Planeje rota de síntese para moléculas-alvo.

**Etapas:**
1. Carregue conjunto de dados: `datasets.USPTO50k()`
2. Treine modelo de identificação de centro (RGCN)
3. Treine modelo de conclusão de synthon (GIN)
4. Combine em pipeline de retrossíntese ponta-a-ponta
5. Aplique recursivamente para planejamento multi-etapa
6. Verifique disponibilidade comercial de blocos de construção

**Navegação:** `references/retrosynthesis.md` → Tipos de tarefa → Planejamento multi-etapa

## Padrões de Integração

### Com RDKit

Converta entre moléculas TorchDrug e RDKit:
```python
from torchdrug import data
from rdkit import Chem

# SMILES → moléculas TorchDrug
smiles = "CCO"
mol = data.Molecule.from_smiles(smiles)

# TorchDrug → RDKit
rdkit_mol = mol.to_molecule()

# RDKit → TorchDrug
rdkit_mol = Chem.MolFromSmiles(smiles)
mol = data.Molecule.from_molecule(rdkit_mol)
```

### Com AlphaFold/ESM

Use estruturas previstas:
```python
from torchdrug import data

# Carregue estrutura prevista por AlphaFold
protein = data.Protein.from_pdb("AF-P12345-F1-model_v4.pdb")

# Construa grafo com arestas espaciais
graph = protein.residue_graph(
    node_position="ca",
    edge_types=["sequential", "radius"],
    radius_cutoff=10.0
)
```

### Com PyTorch Lightning

Envolva tarefas para treinamento Lightning:
```python
import pytorch_lightning as pl

class LightningTask(pl.LightningModule):
    def __init__(self, torchdrug_task):
        super().__init__()
        self.task = torchdrug_task

    def training_step(self, batch, batch_idx):
        return self.task(batch)

    def validation_step(self, batch, batch_idx):
        pred = self.task.predict(batch)
        target = self.task.target(batch)
        return {"pred": pred, "target": target}

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=1e-3)
```

## Detalhes Técnicos

Para aprofundamentos na arquitetura do TorchDrug:

**Conceitos Principais:** Consulte `references/core_concepts.md` para:
- Filosofia de arquitetura (modular, configurável)
- Estruturas de dados (Graph, Molecule, Protein, PackedGraph)
- Interface de modelo e assinatura de função forward
- Interface de tarefa (predict, target, forward, evaluate)
- Fluxos de trabalho de treinamento e melhores práticas
- Funções de perda e métricas
- Armadilhas comuns e debugging

## Folha de Referência Rápida

**Escolha Conjunto de Dados:**
- Propriedade molecular → `references/datasets.md` → Seção Molecular
- Tarefa de proteína → `references/datasets.md` → Seção Protein
- Grafo de conhecimento → `references/datasets.md` → Seção Knowledge graph

**Escolha Modelo:**
- Moléculas → `references/models_architectures.md` → Seção GNN → GIN/GAT/SchNet
- Proteínas (sequência) → `references/models_architectures.md` → Seção Protein → ESM
- Proteínas (estrutura) → `references/models_architectures.md` → Seção Protein → GearNet
- Grafo de conhecimento → `references/models_architectures.md` → Seção KG → RotatE/ComplEx

**Tarefas Comuns:**
- Predição de propriedade → `references/molecular_property_prediction.md` ou `references/protein_modeling.md`
- Geração → `references/molecular_generation.md`
- Retrossíntese → `references/retrosynthesis.md`
- Raciocínio KG → `references/knowledge_graphs.md`

**Entenda a Arquitetura:**
- Estruturas de dados → `references/core_concepts.md` → Data Structures
- Design de modelo → `references/core_concepts.md` → Model Interface
- Design de tarefa → `references/core_concepts.md` → Task Interface

## Resolução de Problemas Comuns

**Problema: Erros de incompatibilidade de dimensão**
→ Verifique se `model.input_dim` corresponde a `dataset.node_feature_dim`
→ Consulte `references/core_concepts.md` → Essential Attributes

**Problema: Desempenho ruim em tarefas moleculares**
→ Use divisão de scaffold, não aleatória
→ Tente GIN em vez de GCN
→ Consulte `references/molecular_property_prediction.md` → Best Practices

**Problema: Modelo de proteína não está aprendendo**
→ Use ESM pré-treinado para tarefas de sequência
→ Verifique construção de aresta para modelos de estrutura
→ Consulte `references/protein_modeling.md` → Training Workflows

**Problema: Erros de memória com grafos grandes**
→ Reduza tamanho do lote
→ Use acumulação de gradiente
→ Consulte `references/core_concepts.md` → Memory Efficiency

**Problema: Moléculas geradas são inválidas**
→ Adicione restrições de validade
→ Pós-processe com validação RDKit
→ Consulte `references/molecular_generation.md` → Validation and Filtering

## Recursos

**Documentação Oficial:** https://torchdrug.ai/docs/
**GitHub:** https://github.com/DeepGraphLearning/torchdrug
**Artigo:** TorchDrug: A Powerful and Flexible Machine Learning Platform for Drug Discovery

## Resumo

Navegue até o arquivo de referência apropriado com base em sua tarefa:

1. **Predição de propriedades moleculares** → `molecular_property_prediction.md`
2. **Modelagem de proteínas** → `protein_modeling.md`
3. **Grafos de conhecimento** → `knowledge_graphs.md`
4. **Geração molecular** → `molecular_generation.md`
5. **Retrossíntese** → `retrosynthesis.md`
6. **Seleção de modelo** → `models_architectures.md`
7. **Seleção de conjunto de dados** → `datasets.md`
8. **Detalhes técnicos** → `core_concepts.md`

Cada referência fornece cobertura abrangente de seu domínio com exemplos, melhores práticas e casos de uso comuns.