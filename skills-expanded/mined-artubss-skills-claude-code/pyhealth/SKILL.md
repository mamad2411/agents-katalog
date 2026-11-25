---
name: pyhealth
description: Kit de ferramentas abrangente de IA em saúde para desenvolver, testar e implantar modelos de machine learning com dados clínicos. Esta habilidade deve ser usada ao trabalhar com registros eletrônicos de saúde (EHR), tarefas de previsão clínica (mortalidade, readmissão, recomendação de medicamentos), sistemas de codificação médica (ICD, NDC, ATC), sinais fisiológicos (EEG, ECG), conjuntos de dados de saúde (MIMIC-III/IV, eICU, OMOP), ou implementar modelos de deep learning para aplicações de saúde (RETAIN, SafeDrug, Transformer, GNN).
---

# PyHealth: Kit de Ferramentas de IA em Saúde

## Visão Geral

PyHealth é uma biblioteca Python abrangente para IA em saúde que oferece ferramentas especializadas, modelos e conjuntos de dados para machine learning clínico. Use esta habilidade ao desenvolver modelos de previsão em saúde, processar dados clínicos, trabalhar com sistemas de codificação médica ou implantar soluções de IA em ambientes de saúde.

## Quando Usar Esta Habilidade

Invoque esta habilidade quando:

- **Trabalhar com conjuntos de dados de saúde**: MIMIC-III, MIMIC-IV, eICU, OMOP, dados EEG de sono, imagens médicas
- **Tarefas de previsão clínica**: Previsão de mortalidade, readmissão hospitalar, tempo de permanência, recomendação de medicamentos
- **Codificação médica**: Tradução entre sistemas de códigos ICD-9/10, NDC, RxNorm, ATC
- **Processamento de dados clínicos**: Eventos sequenciais, sinais fisiológicos, texto clínico, imagens médicas
- **Implementar modelos de saúde**: RETAIN, SafeDrug, GAMENet, StageNet, Transformer para EHR
- **Avaliar modelos clínicos**: Métricas de justiça, calibração, interpretabilidade, quantificação de incerteza

## Capacidades Principais

PyHealth opera por meio de um pipeline modular de 5 etapas otimizado para IA em saúde:

1. **Carregamento de Dados**: Acesso a 10+ conjuntos de dados de saúde com interfaces padronizadas
2. **Definição de Tarefas**: Aplicar 20+ tarefas de previsão clínica predefinidas ou criar tarefas personalizadas
3. **Seleção de Modelo**: Escolher entre 33+ modelos (baselines, deep learning, específicos de saúde)
4. **Treinamento**: Treinar com checkpoint automático, monitoramento e avaliação
5. **Implantação**: Calibrar, interpretar e validar para uso clínico

**Desempenho**: 3x mais rápido que pandas para processamento de dados de saúde

## Fluxo de Trabalho de Início Rápido

```python
from pyhealth.datasets import MIMIC4Dataset
from pyhealth.tasks import mortality_prediction_mimic4_fn
from pyhealth.datasets import split_by_patient, get_dataloader
from pyhealth.models import Transformer
from pyhealth.trainer import Trainer

# 1. Carregar dataset e definir tarefa
dataset = MIMIC4Dataset(root="/path/to/data")
sample_dataset = dataset.set_task(mortality_prediction_mimic4_fn)

# 2. Dividir dados
train, val, test = split_by_patient(sample_dataset, [0.7, 0.1, 0.2])

# 3. Criar data loaders
train_loader = get_dataloader(train, batch_size=64, shuffle=True)
val_loader = get_dataloader(val, batch_size=64, shuffle=False)
test_loader = get_dataloader(test, batch_size=64, shuffle=False)

# 4. Inicializar e treinar modelo
model = Transformer(
    dataset=sample_dataset,
    feature_keys=["diagnoses", "medications"],
    mode="binary",
    embedding_dim=128
)

trainer = Trainer(model=model, device="cuda")
trainer.train(
    train_dataloader=train_loader,
    val_dataloader=val_loader,
    epochs=50,
    monitor="pr_auc_score"
)

# 5. Avaliar
results = trainer.evaluate(test_loader)
```

## Documentação Detalhada

Esta habilidade inclui documentação de referência abrangente organizada por funcionalidade. Leia arquivos de referência específicos conforme necessário:

### 1. Conjuntos de Dados e Estruturas de Dados

**Arquivo**: `references/datasets.md`

**Leia quando:**
- Carregar conjuntos de dados de saúde (MIMIC, eICU, OMOP, EEG de sono, etc.)
- Compreender estruturas de dados Event, Patient, Visit
- Processar diferentes tipos de dados (EHR, sinais, imagens, texto)
- Dividir dados para treinamento/validação/teste
- Trabalhar com SampleDataset para formatação específica de tarefa

**Tópicos-chave:**
- Estruturas de dados principais (Event, Patient, Visit)
- 10+ conjuntos de dados disponíveis (EHR, sinais fisiológicos, imagem, texto)
- Carregamento e iteração de dados
- Estratégias de divisão treino/validação/teste
- Otimização de desempenho para grandes conjuntos de dados

### 2. Tradução de Codificação Médica

**Arquivo**: `references/medical_coding.md`

**Leia quando:**
- Traduzir entre sistemas de codificação médica
- Trabalhar com códigos de diagnóstico (ICD-9-CM, ICD-10-CM, CCS)
- Processar códigos de medicamentos (NDC, RxNorm, ATC)
- Padronizar códigos de procedimento (ICD-9-PROC, ICD-10-PROC)
- Agrupar códigos em categorias clínicas
- Lidar com classificações hierárquicas de medicamentos

**Tópicos-chave:**
- InnerMap para pesquisas dentro do sistema
- CrossMap para tradução entre sistemas
- Sistemas de codificação suportados (ICD, NDC, ATC, CCS, RxNorm)
- Padronização de códigos e travessia de hierarquia
- Classificação de medicamentos por classe terapêutica
- Integração com conjuntos de dados

### 3. Tarefas de Previsão Clínica

**Arquivo**: `references/tasks.md`

**Leia quando:**
- Definir objetivos de previsão clínica
- Usar tarefas predefinidas (mortalidade, readmissão, recomendação de medicamentos)
- Trabalhar com tarefas baseadas em EHR, sinais, imagem ou texto
- Criar tarefas de previsão personalizadas
- Configurar esquemas de entrada/saída para modelos
- Aplicar lógica de filtragem específica de tarefa

**Tópicos-chave:**
- 20+ tarefas clínicas predefinidas
- Tarefas EHR (mortalidade, readmissão, tempo de permanência, recomendação de medicamentos)
- Tarefas de sinais (estágio de sono, análise EEG, detecção de convulsões)
- Tarefas de imagem (classificação COVID-19 raio-X do tórax)
- Tarefas de texto (codificação médica, classificação de especialidade)
- Padrões de criação de tarefa personalizada

### 4. Modelos e Arquiteturas

**Arquivo**: `references/models.md`

**Leia quando:**
- Selecionar modelos para previsão clínica
- Compreender arquiteturas e capacidades de modelos
- Escolher entre modelos de propósito geral e específicos de saúde
- Implementar modelos interpretáveis (RETAIN, AdaCare)
- Trabalhar com recomendação de medicamentos (SafeDrug, GAMENet)
- Usar redes neurais gráficas para saúde
- Configurar hiperparâmetros de modelo

**Tópicos-chave:**
- 33+ modelos disponíveis
- Propósito geral: Logistic Regression, MLP, CNN, RNN, Transformer, GNN
- Específicos de saúde: RETAIN, SafeDrug, GAMENet, StageNet, AdaCare
- Seleção de modelo por tipo de tarefa e tipo de dados
- Considerações de interpretabilidade
- Requisitos computacionais
- Diretrizes de sintonização de hiperparâmetros

### 5. Pré-processamento de Dados

**Arquivo**: `references/preprocessing.md`

**Leia quando:**
- Pré-processar dados clínicos para modelos
- Lidar com eventos sequenciais e dados de séries temporais
- Processar sinais fisiológicos (EEG, ECG)
- Normalizar valores de laboratório e sinais vitais
- Preparar rótulos para diferentes tipos de tarefas
- Construir vocabulários de recursos
- Gerenciar dados ausentes e outliers

**Tópicos-chave:**
- 15+ tipos de processador
- Processamento de sequências (padding, truncação)
- Processamento de sinais (filtragem, segmentação)
- Extração e codificação de características
- Processadores de rótulo (binário, multi-classe, multi-label, regressão)
- Pré-processamento de texto e imagem
- Fluxos de trabalho de pré-processamento comuns

### 6. Treinamento e Avaliação

**Arquivo**: `references/training_evaluation.md`

**Leia quando:**
- Treinar modelos com a classe Trainer
- Avaliar desempenho de modelo
- Calcular métricas clínicas
- Avaliar justiça de modelo entre grupos demográficos
- Calibrar previsões para confiabilidade
- Quantificar incerteza de previsão
- Interpretar previsões de modelo
- Preparar modelos para implantação clínica

**Tópicos-chave:**
- Classe Trainer (train, evaluate, inference)
- Métricas para tarefas binária, multi-classe, multi-label, regressão
- Métricas de justiça para avaliação de viés
- Métodos de calibração (Platt scaling, temperature scaling)
- Quantificação de incerteza (conformal prediction, MC dropout)
- Ferramentas de interpretabilidade (visualização de atenção, SHAP, ChEFER)
- Exemplo de pipeline de treinamento completo

## Instalação

```bash
uv pip install pyhealth
```

**Requisitos:**
- Python ≥ 3.7
- PyTorch ≥ 1.8
- NumPy, pandas, scikit-learn

## Casos de Uso Comuns

### Caso de Uso 1: Previsão de Mortalidade em UTI

**Objetivo**: Prever mortalidade de pacientes em unidade de terapia intensiva

**Abordagem:**
1. Carregar dataset MIMIC-IV → Leia `references/datasets.md`
2. Aplicar tarefa de previsão de mortalidade → Leia `references/tasks.md`
3. Selecionar modelo interpretável (RETAIN) → Leia `references/models.md`
4. Treinar e avaliar → Leia `references/training_evaluation.md`
5. Interpretar previsões para uso clínico → Leia `references/training_evaluation.md`

### Caso de Uso 2: Recomendação Segura de Medicamentos

**Objetivo**: Recomendar medicamentos evitando interações medicamentosas

**Abordagem:**
1. Carregar dataset EHR (MIMIC-IV ou OMOP) → Leia `references/datasets.md`
2. Aplicar tarefa de recomendação de medicamentos → Leia `references/tasks.md`
3. Usar modelo SafeDrug com restrições DDI → Leia `references/models.md`
4. Pré-processar códigos de medicamentos → Leia `references/medical_coding.md`
5. Avaliar com métricas multi-label → Leia `references/training_evaluation.md`

### Caso de Uso 3: Previsão de Readmissão Hospitalar

**Objetivo**: Identificar pacientes em risco de readmissão em 30 dias

**Abordagem:**
1. Carregar dados EHR multi-site (eICU ou OMOP) → Leia `references/datasets.md`
2. Aplicar tarefa de previsão de readmissão → Leia `references/tasks.md`
3. Lidar com desbalanceamento de classes no pré-processamento → Leia `references/preprocessing.md`
4. Treinar modelo Transformer → Leia `references/models.md`
5. Calibrar previsões e avaliar justiça → Leia `references/training_evaluation.md`

### Caso de Uso 4: Diagnóstico de Distúrbio do Sono

**Objetivo**: Classificar estágios do sono a partir de sinais EEG

**Abordagem:**
1. Carregar dataset de EEG de sono (SleepEDF, SHHS) → Leia `references/datasets.md`
2. Aplicar tarefa de estágio de sono → Leia `references/tasks.md`
3. Pré-processar sinais EEG (filtragem, segmentação) → Leia `references/preprocessing.md`
4. Treinar modelo CNN ou RNN → Leia `references/models.md`
5. Avaliar desempenho por estágio → Leia `references/training_evaluation.md`

### Caso de Uso 5: Tradução de Código Médico

**Objetivo**: Padronizar diagnósticos entre diferentes sistemas de codificação

**Abordagem:**
1. Leia `references/medical_coding.md` para orientação abrangente
2. Use CrossMap para traduzir entre ICD-9, ICD-10, CCS
3. Agrupe códigos em categorias clinicamente significativas
4. Integre com processamento de conjunto de dados

### Caso de Uso 6: Codificação ICD de Texto Clínico

**Objetivo**: Atribuir automaticamente códigos ICD a partir de notas clínicas

**Abordagem:**
1. Carregar MIMIC-III com texto clínico → Leia `references/datasets.md`
2. Aplicar tarefa de codificação ICD → Leia `references/tasks.md`
3. Pré-processar texto clínico → Leia `references/preprocessing.md`
4. Usar TransformersModel (ClinicalBERT) → Leia `references/models.md`
5. Avaliar com métricas multi-label → Leia `references/training_evaluation.md`

## Melhores Práticas

### Manipulação de Dados

1. **Sempre divida por paciente**: Previne vazamento de dados garantindo que nenhum paciente apareça em múltiplas divisões
   ```python
   from pyhealth.datasets import split_by_patient
   train, val, test = split_by_patient(dataset, [0.7, 0.1, 0.2])
   ```

2. **Verifique estatísticas do dataset**: Compreenda seus dados antes de modelar
   ```python
   print(dataset.stats())  # Pacientes, visitas, eventos, distribuições de códigos
   ```

3. **Use pré-processamento apropriado**: Combine processadores com tipos de dados (veja `references/preprocessing.md`)

### Desenvolvimento de Modelo

1. **Comece com baselines**: Estabeleça desempenho baseline com modelos simples
   - Logistic Regression para tarefas binárias/multi-classe
   - MLP para baseline inicial de deep learning

2. **Escolha modelos apropriados para tarefa**:
   - Interpretabilidade necessária → RETAIN, AdaCare
   - Recomendação de medicamentos → SafeDrug, GAMENet
   - Sequências longas → Transformer
   - Relações gráficas → GNN

3. **Monitore métricas de validação**: Use métricas apropriadas para tarefa e lide com desbalanceamento de classe
   - Classificação binária: AUROC, AUPRC (especialmente para eventos raros)
   - Multi-classe: macro-F1 (para desbalanceado), weighted-F1
   - Multi-label: Jaccard, example-F1
   - Regressão: MAE, RMSE

### Implantação Clínica

1. **Calibre previsões**: Garanta que probabilidades sejam confiáveis (veja `references/training_evaluation.md`)

2. **Avalie justiça**: Avalie entre grupos demográficos para detectar viés

3. **Quantifique incerteza**: Forneça estimativas de confiança para previsões

4. **Interprete previsões**: Use pesos de atenção, SHAP ou ChEFER para confiança clínica

5. **Valide minuciosamente**: Use conjuntos de teste isolados de diferentes períodos de tempo ou locais

## Limitações e Considerações

### Requisitos de Dados

- **Grandes conjuntos de dados**: Modelos de deep learning exigem dados suficientes (milhares de pacientes)
- **Qualidade dos dados**: Dados ausentes e erros de codificação impactam desempenho
- **Consistência temporal**: Garanta que divisão treino/teste respeite ordenação temporal quando necessário

### Validação Clínica

- **Validação externa**: Teste em dados de diferentes hospitais/sistemas
- **Avaliação prospectiva**: Valide em configurações clínicas reais antes da implantação
- **Revisão clínica**: Tenha clínicos revisando previsões e interpretações
- **Considerações éticas**: Aborde privacidade (HIPAA/GDPR), justiça e segurança

### Recursos Computacionais

- **GPU recomendada**: Para treinar modelos de deep learning eficientemente
- **Requisitos de memória**: Grandes conjuntos de dados podem exigir 16GB+ RAM
- **Armazenamento**: Conjuntos de dados de saúde podem ter 10s-100s de GB

## Resolução de Problemas

### Problemas Comuns

**ImportError para dataset**:
- Garanta que arquivos de dataset sejam baixados e caminho esteja correto
- Verifique compatibilidade de versão de PyHealth

**Falta de memória**:
- Reduza tamanho do batch
- Reduza comprimento da sequência (`max_seq_length`)
- Use acumulação de gradiente
- Processe dados em pedaços

**Desempenho ruim**:
- Verifique desbalanceamento de classe e use métricas apropriadas (AUPRC vs AUROC)
- Verifique pré-processamento (normalização, manipulação de dados ausentes)
- Aumente capacidade de modelo ou épocas de treinamento
- Verifique vazamento de dados em divisão treino/teste

**Treinamento lento**:
- Use GPU (`device="cuda"`)
- Aumente tamanho do batch (se memória permitir)
- Reduza comprimento da sequência
- Use modelo mais eficiente (CNN vs Transformer)

### Obtendo Ajuda

- **Documentação**: https://pyhealth.readthedocs.io/
- **GitHub Issues**: https://github.com/sunlabuiuc/PyHealth/issues
- **Tutoriais**: 7 tutoriais principais + 5 pipelines práticos disponíveis online

## Exemplo: Fluxo de Trabalho Completo

```python
# Pipeline completo de previsão de mortalidade
from pyhealth.datasets import MIMIC4Dataset
from pyhealth.tasks import mortality_prediction_mimic4_fn
from pyhealth.datasets import split_by_patient, get_dataloader
from pyhealth.models import RETAIN
from pyhealth.trainer import Trainer

# 1. Carregar dataset
print("Carregando dataset MIMIC-IV...")
dataset = MIMIC4Dataset(root="/data/mimic4")
print(dataset.stats())

# 2. Definir tarefa
print("Configurando tarefa de previsão de mortalidade...")
sample_dataset = dataset.set_task(mortality_prediction_mimic4_fn)
print(f"Geradas {len(sample_dataset)} amostras")

# 3. Dividir dados (por paciente para prevenir vazamento)
print("Dividindo dados...")
train_ds, val_ds, test_ds = split_by_patient(
    sample_dataset, ratios=[0.7, 0.1, 0.2], seed=42
)

# 4. Criar data loaders
train_loader = get_dataloader(train_ds, batch_size=64, shuffle=True)
val_loader = get_dataloader(val_ds, batch_size=64)
test_loader = get_dataloader(test_ds, batch_size=64)

# 5. Inicializar modelo interpretável
print("Inicializando modelo RETAIN...")
model = RETAIN(
    dataset=sample_dataset,
    feature_keys=["diagnoses", "procedures", "medications"],
    mode="binary",
    embedding_dim=128,
    hidden_dim=128
)

# 6. Treinar modelo
print("Treinando modelo...")
trainer = Trainer(model=model, device="cuda")
trainer.train(
    train_dataloader=train_loader,
    val_dataloader=val_loader,
    epochs=50,
    optimizer="Adam",
    learning_rate=1e-3,
    weight_decay=1e-5,
    monitor="pr_auc_score",  # Use AUPRC para dados desbalanceados
    monitor_criterion="max",
    save_path="./checkpoints/mortality_retain"
)

# 7. Avaliar no conjunto de teste
print("Avaliando no conjunto de teste...")
test_results = trainer.evaluate(
    test_loader,
    metrics=["accuracy", "precision", "recall", "f1_score",
             "roc_auc_score", "pr_auc_score"]
)

print("\nResultados do Teste:")
for metric, value in test_results.items():
    print(f"  {metric}: {value:.4f}")

# 8. Obter previsões com atenção para interpretação
predictions = trainer.inference(
    test_loader,
    additional_outputs=["visit_attention", "feature_attention"],
    return_patient_ids=True
)

# 9. Analisar paciente de alto risco
high_risk_idx = predictions["y_pred"].argmax()
patient_id = predictions["patient_ids"][high_risk_idx]
visit_attn = predictions["visit_attention"][high_risk_idx]
feature_attn = predictions["feature_attention"][high_risk_idx]

print(f"\nPaciente de alto risco: {patient_id}")
print(f"Escore de risco: {predictions['y_pred'][high_risk_idx]:.3f}")
print(f"Visita mais influente: {visit_attn.argmax()}")
print(f"Características mais importantes: {feature_attn[visit_attn.argmax()].argsort()[-5:]}")

# 10. Salvar modelo para implantação
trainer.save("./models/mortality_retain_final.pt")
print("\nModelo salvo com sucesso!")
```

## Recursos

Para informações detalhadas sobre cada componente, consulte os arquivos de referência abrangentes no diretório `references/`:

- **datasets.md**: Estruturas de dados, carregamento e divisão (4.500 palavras)
- **medical_coding.md**: Tradução de códigos e padronização (3.800 palavras)
- **tasks.md**: Tarefas de previsão clínica e criação de tarefa personalizada (4.200 palavras)
- **models.md**: Arquiteturas de modelo e diretrizes de seleção (5.100 palavras)
- **preprocessing.md**: Processadores de dados e fluxos de trabalho de pré-processamento (4.600 palavras)
- **training_evaluation.md**: Treinamento, métricas, calibração, interpretabilidade (5.900 palavras)

**Documentação abrangente total**: ~28.000 palavras em arquivos de referência modulares.