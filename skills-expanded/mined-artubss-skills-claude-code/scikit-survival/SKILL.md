---
name: scikit-survival
description: Kit de ferramentas abrangente para análise de sobrevivência e modelagem de tempo até evento em Python usando scikit-survival. Use essa competência ao trabalhar com dados de sobrevivência censurados, realizar análise tempo-até-evento, ajustar modelos Cox, Florestas de Sobrevivência Aleatória, modelos de Gradient Boosting, ou SVMs de Sobrevivência, avaliar predições de sobrevivência com índice de concordância ou Brier score, lidar com riscos competitivos, ou implementar qualquer workflow de análise de sobrevivência com a biblioteca scikit-survival.
---

# scikit-survival: Análise de Sobrevivência em Python

## Visão Geral

scikit-survival é uma biblioteca Python para análise de sobrevivência construída sobre scikit-learn. Ela fornece ferramentas especializadas para análise tempo-até-evento, lidando com o desafio único de dados censurados, onde algumas observações são apenas parcialmente conhecidas.

A análise de sobrevivência visa estabelecer conexões entre covariáveis e o tempo de um evento, levando em conta registros censurados (particularmente dados censurados à direita de estudos onde participantes não experimentam eventos durante períodos de observação).

## Quando Usar Essa Competência

Use essa competência quando:
- Executar análise de sobrevivência ou modelagem tempo-até-evento
- Trabalhar com dados censurados (censurados à direita, à esquerda ou por intervalo)
- Ajustar modelos de riscos proporcionais de Cox (padrão ou penalizados)
- Construir modelos ensemble de sobrevivência (Florestas de Sobrevivência Aleatória, Gradient Boosting)
- Treinar Máquinas de Vetores de Suporte de Sobrevivência
- Avaliar desempenho de modelos de sobrevivência (índice de concordância, Brier score, AUC dependente do tempo)
- Estimar curvas de Kaplan-Meier ou Nelson-Aalen
- Analisar riscos competitivos
- Pré-processar dados de sobrevivência ou lidar com valores ausentes em datasets de sobrevivência
- Realizar qualquer análise usando a biblioteca scikit-survival

## Capacidades Principais

### 1. Tipos de Modelos e Seleção

scikit-survival fornece múltiplas famílias de modelos, cada uma adequada para cenários diferentes:

#### Modelos de Riscos Proporcionais de Cox
**Use para**: Análise de sobrevivência padrão com coeficientes interpretáveis
- `CoxPHSurvivalAnalysis`: Modelo Cox básico
- `CoxnetSurvivalAnalysis`: Cox penalizado com elastic net para dados de alta dimensionalidade
- `IPCRidge`: Regressão ridge para modelos de tempo de falha acelerado

**Veja**: `references/cox-models.md` para orientação detalhada sobre modelos Cox, regularização e interpretação

#### Métodos Ensemble
**Use para**: Alto desempenho preditivo com relações não-lineares complexas
- `RandomSurvivalForest`: Método ensemble robusto e não-paramétrico
- `GradientBoostingSurvivalAnalysis`: Boosting baseado em árvores para máximo desempenho
- `ComponentwiseGradientBoostingSurvivalAnalysis`: Boosting linear com seleção de features
- `ExtraSurvivalTrees`: Árvores extremamente aleatorizadas para regularização adicional

**Veja**: `references/ensemble-models.md` para orientação abrangente sobre métodos ensemble, sintonia de hiperparâmetros e quando usar cada modelo

#### Máquinas de Vetores de Suporte de Sobrevivência
**Use para**: Datasets de médio porte com aprendizado baseado em margem
- `FastSurvivalSVM`: SVM linear otimizado para velocidade
- `FastKernelSurvivalSVM`: SVM com kernel para relações não-lineares
- `HingeLossSurvivalSVM`: SVM com hinge loss
- `ClinicalKernelTransform`: Kernel especializado para dados clínicos + moleculares

**Veja**: `references/svm-models.md` para orientação detalhada sobre SVM, seleção de kernel e sintonia de hiperparâmetros

#### Árvore de Decisão de Seleção de Modelo

```
Início
├─ Dados de alta dimensionalidade (p > n)?
│  ├─ Sim → CoxnetSurvivalAnalysis (elastic net)
│  └─ Não → Continuar
│
├─ Precisa de coeficientes interpretáveis?
│  ├─ Sim → CoxPHSurvivalAnalysis ou ComponentwiseGradientBoostingSurvivalAnalysis
│  └─ Não → Continuar
│
├─ Relações não-lineares complexas esperadas?
│  ├─ Sim
│  │  ├─ Dataset grande (n > 1000) → GradientBoostingSurvivalAnalysis
│  │  ├─ Dataset médio → RandomSurvivalForest ou FastKernelSurvivalSVM
│  │  └─ Dataset pequeno → RandomSurvivalForest
│  └─ Não → CoxPHSurvivalAnalysis ou FastSurvivalSVM
│
└─ Para máximo desempenho → Tente múltiplos modelos e compare
```

### 2. Preparação de Dados e Pré-processamento

Antes de modelar, prepare adequadamente dados de sobrevivência:

#### Criando Resultados de Sobrevivência
```python
from sksurv.util import Surv

# A partir de arrays separados
y = Surv.from_arrays(event=event_array, time=time_array)

# A partir de DataFrame
y = Surv.from_dataframe('event', 'time', df)
```

#### Etapas Essenciais de Pré-processamento
1. **Lidar com valores ausentes**: Estratégias de imputação para features
2. **Codificar variáveis categóricas**: One-hot encoding ou label encoding
3. **Padronizar features**: Crítico para SVMs e modelos Cox regularizados
4. **Validar qualidade dos dados**: Verificar tempos negativos, eventos suficientes por feature
5. **Divisão treino-teste**: Manter taxas de censura semelhantes entre divisões

**Veja**: `references/data-handling.md` para workflows completos de pré-processamento, validação de dados e melhores práticas

### 3. Avaliação de Modelos

Avaliação apropriada é crítica para modelos de sobrevivência. Use métricas adequadas que levem em conta censura:

#### Índice de Concordância (C-index)
Métrica primária para ranking/discriminação:
- **C-index de Harrell**: Use para censura baixa (<40%)
- **C-index de Uno**: Use para censura moderada a alta (>40%) - mais robusto

```python
from sksurv.metrics import concordance_index_censored, concordance_index_ipcw

# C-index de Harrell
c_harrell = concordance_index_censored(y_test['event'], y_test['time'], risk_scores)[0]

# C-index de Uno (recomendado)
c_uno = concordance_index_ipcw(y_train, y_test, risk_scores)[0]
```

#### AUC Dependente do Tempo
Avaliar discriminação em pontos de tempo específicos:

```python
from sksurv.metrics import cumulative_dynamic_auc

times = [365, 730, 1095]  # 1, 2, 3 anos
auc, mean_auc = cumulative_dynamic_auc(y_train, y_test, risk_scores, times)
```

#### Brier Score
Avaliar tanto discriminação quanto calibração:

```python
from sksurv.metrics import integrated_brier_score

ibs = integrated_brier_score(y_train, y_test, survival_functions, times)
```

**Veja**: `references/evaluation-metrics.md` para orientação abrangente sobre avaliação, seleção de métricas e uso de scorers com validação cruzada

### 4. Análise de Riscos Competitivos

Lidar com situações com múltiplos tipos de eventos mutuamente excludentes:

```python
from sksurv.nonparametric import cumulative_incidence_competing_risks

# Estimar incidência cumulativa para cada tipo de evento
time_points, cif_event1, cif_event2 = cumulative_incidence_competing_risks(y)
```

**Use riscos competitivos quando**:
- Múltiplos tipos de eventos mutuamente excludentes existem (ex: morte por diferentes causas)
- Ocorrência de um evento impede outros
- Necessário estimativas de probabilidade para tipos de evento específicos

**Veja**: `references/competing-risks.md` para métodos detalhados de riscos competitivos, modelos de hazard causa-específico e interpretação

### 5. Estimação Não-paramétrica

Estimar funções de sobrevivência sem suposições paramétricas:

#### Estimador de Kaplan-Meier
```python
from sksurv.nonparametric import kaplan_meier_estimator

time, survival_prob = kaplan_meier_estimator(y['event'], y['time'])
```

#### Estimador de Nelson-Aalen
```python
from sksurv.nonparametric import nelson_aalen_estimator

time, cumulative_hazard = nelson_aalen_estimator(y['event'], y['time'])
```

## Workflows Típicos

### Workflow 1: Análise de Sobrevivência Padrão

```python
from sksurv.datasets import load_breast_cancer
from sksurv.linear_model import CoxPHSurvivalAnalysis
from sksurv.metrics import concordance_index_ipcw
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 1. Carregar e preparar dados
X, y = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. Pré-processar
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 3. Ajustar modelo
estimator = CoxPHSurvivalAnalysis()
estimator.fit(X_train_scaled, y_train)

# 4. Fazer predições
risk_scores = estimator.predict(X_test_scaled)

# 5. Avaliar
c_index = concordance_index_ipcw(y_train, y_test, risk_scores)[0]
print(f"C-index: {c_index:.3f}")
```

### Workflow 2: Dados de Alta Dimensionalidade com Seleção de Features

```python
from sksurv.linear_model import CoxnetSurvivalAnalysis
from sklearn.model_selection import GridSearchCV
from sksurv.metrics import as_concordance_index_ipcw_scorer

# 1. Usar Cox penalizado para seleção de features
estimator = CoxnetSurvivalAnalysis(l1_ratio=0.9)  # Similar a Lasso

# 2. Sintonizar regularização com validação cruzada
param_grid = {'alpha_min_ratio': [0.01, 0.001]}
cv = GridSearchCV(estimator, param_grid,
                  scoring=as_concordance_index_ipcw_scorer(), cv=5)
cv.fit(X, y)

# 3. Identificar features selecionadas
best_model = cv.best_estimator_
selected_features = np.where(best_model.coef_ != 0)[0]
```

### Workflow 3: Método Ensemble para Máximo Desempenho

```python
from sksurv.ensemble import GradientBoostingSurvivalAnalysis
from sklearn.model_selection import GridSearchCV

# 1. Definir grid de parâmetros
param_grid = {
    'learning_rate': [0.01, 0.05, 0.1],
    'n_estimators': [100, 200, 300],
    'max_depth': [3, 5, 7]
}

# 2. Grid search
gbs = GradientBoostingSurvivalAnalysis()
cv = GridSearchCV(gbs, param_grid, cv=5,
                  scoring=as_concordance_index_ipcw_scorer(), n_jobs=-1)
cv.fit(X_train, y_train)

# 3. Avaliar melhor modelo
best_model = cv.best_estimator_
risk_scores = best_model.predict(X_test)
c_index = concordance_index_ipcw(y_train, y_test, risk_scores)[0]
```

### Workflow 4: Comparação Abrangente de Modelos

```python
from sksurv.linear_model import CoxPHSurvivalAnalysis
from sksurv.ensemble import RandomSurvivalForest, GradientBoostingSurvivalAnalysis
from sksurv.svm import FastSurvivalSVM
from sksurv.metrics import concordance_index_ipcw, integrated_brier_score

# Definir modelos
models = {
    'Cox': CoxPHSurvivalAnalysis(),
    'RSF': RandomSurvivalForest(n_estimators=100, random_state=42),
    'GBS': GradientBoostingSurvivalAnalysis(random_state=42),
    'SVM': FastSurvivalSVM(random_state=42)
}

# Avaliar cada modelo
results = {}
for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    risk_scores = model.predict(X_test_scaled)
    c_index = concordance_index_ipcw(y_train, y_test, risk_scores)[0]
    results[name] = c_index
    print(f"{name}: C-index = {c_index:.3f}")

# Selecionar melhor modelo
best_model_name = max(results, key=results.get)
print(f"\nMelhor modelo: {best_model_name}")
```

## Integração com scikit-learn

scikit-survival integra completamente com o ecossistema scikit-learn:

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score, GridSearchCV

# Usar pipelines
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', CoxPHSurvivalAnalysis())
])

# Usar validação cruzada
scores = cross_val_score(pipeline, X, y, cv=5,
                         scoring=as_concordance_index_ipcw_scorer())

# Usar grid search
param_grid = {'model__alpha': [0.1, 1.0, 10.0]}
cv = GridSearchCV(pipeline, param_grid, cv=5)
cv.fit(X, y)
```

## Melhores Práticas

1. **Sempre padronizar features** para SVMs e modelos Cox regularizados
2. **Usar C-index de Uno** em vez de Harrell quando censura > 40%
3. **Relatar múltiplas métricas de avaliação** (C-index, Brier score integrado, AUC dependente do tempo)
4. **Verificar suposição de riscos proporcionais** para modelos Cox
5. **Usar validação cruzada** para sintonia de hiperparâmetros com scorers apropriados
6. **Validar qualidade dos dados** antes de modelar (verificar tempos negativos, eventos suficientes por feature)
7. **Comparar múltiplos tipos de modelos** para encontrar melhor desempenho
8. **Usar importância de permutação** para Florestas de Sobrevivência Aleatória (importância built-in não está disponível)
9. **Considerar riscos competitivos** quando múltiplos tipos de eventos existem
10. **Documentar mecanismo de censura** e taxas na análise

## Armadilhas Comuns a Evitar

1. **Usar C-index de Harrell com censura alta** → Use C-index de Uno
2. **Não padronizar features para SVMs** → Sempre padronize
3. **Esquecer de passar y_train para concordance_index_ipcw** → Necessário para cálculo IPCW
4. **Tratar eventos competitivos como censurados** → Use métodos de riscos competitivos
5. **Não verificar eventos suficientes por feature** → Regra de ouro: 10+ eventos por feature
6. **Usar importância built-in para RSF** → Use importância de permutação
7. **Ignorar suposição de riscos proporcionais** → Validar ou usar modelos alternativos
8. **Não usar scorers apropriados em validação cruzada** → Use as_concordance_index_ipcw_scorer()

## Arquivos de Referência

Essa competência inclui arquivos de referência detalhados para tópicos específicos:

- **`references/cox-models.md`**: Guia completo para modelos de riscos proporcionais de Cox, Cox penalizado (CoxNet), IPCRidge, estratégias de regularização e interpretação
- **`references/ensemble-models.md`**: Florestas de Sobrevivência Aleatória, Gradient Boosting, sintonia de hiperparâmetros, importância de features e seleção de modelos
- **`references/evaluation-metrics.md`**: Índice de concordância (Harrell vs Uno), AUC dependente do tempo, Brier score, pipelines abrangentes de avaliação
- **`references/data-handling.md`**: Carregamento de dados, workflows de pré-processamento, tratamento de dados faltantes, codificação de features, verificações de validação
- **`references/svm-models.md`**: Máquinas de Vetores de Suporte de Sobrevivência, seleção de kernel, clinical kernel transform, sintonia de hiperparâmetros
- **`references/competing-risks.md`**: Análise de riscos competitivos, funções de incidência cumulativa, modelos de hazard causa-específico

Carregue esses arquivos de referência quando informações detalhadas forem necessárias para tarefas específicas.

## Recursos Adicionais

- **Documentação Oficial**: https://scikit-survival.readthedocs.io/
- **Repositório GitHub**: https://github.com/sebp/scikit-survival
- **Datasets Built-in**: Use `sksurv.datasets` para datasets de prática (GBSG2, WHAS500, câncer de pulmão de veteranos, etc.)
- **Referência de API**: Lista completa de classes e funções em https://scikit-survival.readthedocs.io/en/stable/api/index.html

## Referência Rápida: Imports Principais

```python
# Modelos
from sksurv.linear_model import CoxPHSurvivalAnalysis, CoxnetSurvivalAnalysis, IPCRidge
from sksurv.ensemble import RandomSurvivalForest, GradientBoostingSurvivalAnalysis
from sksurv.svm import FastSurvivalSVM, FastKernelSurvivalSVM
from sksurv.tree import SurvivalTree

# Métricas de avaliação
from sksurv.metrics import (
    concordance_index_censored,
    concordance_index_ipcw,
    cumulative_dynamic_auc,
    brier_score,
    integrated_brier_score,
    as_concordance_index_ipcw_scorer,
    as_integrated_brier_score_scorer
)

# Estimação não-paramétrica
from sksurv.nonparametric import (
    kaplan_meier_estimator,
    nelson_aalen_estimator,
    cumulative_incidence_competing_risks
)

# Tratamento de dados
from sksurv.util import Surv
from sksurv.preprocessing import OneHotEncoder, encode_categorical
from sksurv.datasets import load_gbsg2, load_breast_cancer, load_veterans_lung_cancer

# Kernels
from sksurv.kernels import ClinicalKernelTransform
```