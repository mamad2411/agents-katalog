---
name: scikit-learn
description: Aprendizado de máquina em Python com scikit-learn. Use ao trabalhar com aprendizado supervisionado (classificação, regressão), aprendizado não supervisionado (clustering, redução de dimensionalidade), avaliação de modelos, ajuste de hiperparâmetros, pré-processamento ou construção de pipelines de ML. Fornece documentação de referência abrangente para algoritmos, técnicas de pré-processamento, pipelines e melhores práticas.
---

# Scikit-learn

## Visão Geral

Esta skill fornece orientação abrangente para tarefas de aprendizado de máquina usando scikit-learn, a biblioteca Python padrão da indústria para aprendizado de máquina clássico. Use esta skill para classificação, regressão, clustering, redução de dimensionalidade, pré-processamento, avaliação de modelos e construção de pipelines de ML prontos para produção.

## Instalação

```bash
# Instale scikit-learn usando uv
uv pip install scikit-learn

# Opcional: Instale dependências de visualização
uv pip install matplotlib seaborn

# Comumente usado com
uv pip install pandas numpy
```

## Quando Usar Esta Skill

Use a skill scikit-learn quando:

- Construir modelos de classificação ou regressão
- Realizar clustering ou redução de dimensionalidade
- Pré-processar e transformar dados para aprendizado de máquina
- Avaliar performance do modelo com validação cruzada
- Ajustar hiperparâmetros com busca em grid ou aleatória
- Criar pipelines de ML para workflows de produção
- Comparar diferentes algoritmos para uma tarefa
- Trabalhar com dados estruturados (tabulares) e textuais
- Precisar de abordagens de aprendizado de máquina interpretáveis e clássicas

## Início Rápido

### Exemplo de Classificação

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Dividir dados
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Pré-processar
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Treinar modelo
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Avaliar
y_pred = model.predict(X_test_scaled)
print(classification_report(y_test, y_pred))
```

### Pipeline Completo com Dados Mistos

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import GradientBoostingClassifier

# Definir tipos de features
numeric_features = ['age', 'income']
categorical_features = ['gender', 'occupation']

# Criar pipelines de pré-processamento
numeric_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Combinar transformadores
preprocessor = ColumnTransformer([
    ('num', numeric_transformer, numeric_features),
    ('cat', categorical_transformer, categorical_features)
])

# Pipeline completo
model = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', GradientBoostingClassifier(random_state=42))
])

# Ajustar e prever
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
```

## Capacidades Principais

### 1. Aprendizado Supervisionado

Algoritmos abrangentes para tarefas de classificação e regressão.

**Principais algoritmos:**
- **Modelos lineares**: Logistic Regression, Linear Regression, Ridge, Lasso, ElasticNet
- **Baseados em árvores**: Decision Trees, Random Forest, Gradient Boosting
- **Máquinas de Vetores de Suporte**: SVC, SVR com vários kernels
- **Métodos ensemble**: AdaBoost, Voting, Stacking
- **Redes Neurais**: MLPClassifier, MLPRegressor
- **Outros**: Naive Bayes, K-Nearest Neighbors

**Quando usar:**
- Classificação: Prever categorias discretas (detecção de spam, classificação de imagens, detecção de fraude)
- Regressão: Prever valores contínuos (previsão de preço, previsão de demanda)

**Veja:** `references/supervised_learning.md` para documentação detalhada de algoritmos, parâmetros e exemplos de uso.

### 2. Aprendizado Não Supervisionado

Descobrir padrões em dados não rotulados através de clustering e redução de dimensionalidade.

**Algoritmos de clustering:**
- **Baseado em partição**: K-Means, MiniBatchKMeans
- **Baseado em densidade**: DBSCAN, HDBSCAN, OPTICS
- **Hierárquico**: AgglomerativeClustering
- **Probabilístico**: Gaussian Mixture Models
- **Outros**: MeanShift, SpectralClustering, BIRCH

**Redução de dimensionalidade:**
- **Linear**: PCA, TruncatedSVD, NMF
- **Aprendizado de manifold**: t-SNE, UMAP, Isomap, LLE
- **Extração de features**: FastICA, LatentDirichletAllocation

**Quando usar:**
- Segmentação de clientes, detecção de anomalias, visualização de dados
- Reduzir dimensões de features, análise exploratória de dados
- Modelagem de tópicos, compressão de imagens

**Veja:** `references/unsupervised_learning.md` para documentação detalhada.

### 3. Avaliação e Seleção de Modelos

Ferramentas para avaliação robusta de modelos, validação cruzada e ajuste de hiperparâmetros.

**Estratégias de validação cruzada:**
- KFold, StratifiedKFold (classificação)
- TimeSeriesSplit (dados temporais)
- GroupKFold (amostras agrupadas)

**Ajuste de hiperparâmetros:**
- GridSearchCV (busca exaustiva)
- RandomizedSearchCV (amostragem aleatória)
- HalvingGridSearchCV (halving sucessivo)

**Métricas:**
- **Classificação**: acurácia, precisão, recall, F1-score, ROC AUC, matriz de confusão
- **Regressão**: MSE, RMSE, MAE, R², MAPE
- **Clustering**: silhueta, Calinski-Harabasz, Davies-Bouldin

**Quando usar:**
- Comparar performance do modelo objetivamente
- Encontrar hiperparâmetros ótimos
- Prevenir overfitting através de validação cruzada
- Compreender comportamento do modelo com curvas de aprendizado

**Veja:** `references/model_evaluation.md` para métricas abrangentes e estratégias de ajuste.

### 4. Pré-processamento de Dados

Transformar dados brutos em formatos adequados para aprendizado de máquina.

**Escalonamento e normalização:**
- StandardScaler (média zero, variância unitária)
- MinMaxScaler (intervalo limitado)
- RobustScaler (robusto para outliers)
- Normalizer (normalização amostra-a-amostra)

**Codificação de variáveis categóricas:**
- OneHotEncoder (categorias nominais)
- OrdinalEncoder (categorias ordenadas)
- LabelEncoder (codificação de alvo)

**Manipulação de valores ausentes:**
- SimpleImputer (média, mediana, mais frequente)
- KNNImputer (k-vizinhos mais próximos)
- IterativeImputer (imputação multivariada)

**Engenharia de features:**
- PolynomialFeatures (termos de interação)
- KBinsDiscretizer (binning)
- Seleção de features (RFE, SelectKBest, SelectFromModel)

**Quando usar:**
- Antes de treinar qualquer algoritmo que requeira features escalonadas (SVM, KNN, Redes Neurais)
- Converter variáveis categóricas para formato numérico
- Manipular dados ausentes sistematicamente
- Criar features não-lineares para modelos lineares

**Veja:** `references/preprocessing.md` para técnicas detalhadas de pré-processamento.

### 5. Pipelines e Composição

Construir workflows de ML reproduzíveis e prontos para produção.

**Componentes principais:**
- **Pipeline**: Encadear transformadores e estimadores sequencialmente
- **ColumnTransformer**: Aplicar pré-processamento diferente a colunas diferentes
- **FeatureUnion**: Combinar múltiplos transformadores em paralelo
- **TransformedTargetRegressor**: Transformar variável alvo

**Benefícios:**
- Previne vazamento de dados em validação cruzada
- Simplifica código e melhora manutenibilidade
- Permite ajuste de hiperparâmetros conjunto
- Garante consistência entre treinamento e predição

**Quando usar:**
- Sempre use Pipelines para workflows de produção
- Ao misturar features numéricas e categóricas (use ColumnTransformer)
- Ao realizar validação cruzada com etapas de pré-processamento
- Ao ajustar hiperparâmetros incluindo parâmetros de pré-processamento

**Veja:** `references/pipelines_and_composition.md` para padrões abrangentes de pipeline.

## Scripts de Exemplo

### Pipeline de Classificação

Execute um workflow completo de classificação com pré-processamento, comparação de modelos, ajuste de hiperparâmetros e avaliação:

```bash
python scripts/classification_pipeline.py
```

Este script demonstra:
- Manipulação de tipos de dados mistos (numéricos e categóricos)
- Comparação de modelos usando validação cruzada
- Ajuste de hiperparâmetros com GridSearchCV
- Avaliação abrangente com múltiplas métricas
- Análise de importância de features

### Análise de Clustering

Realize análise de clustering com comparação de algoritmos e visualização:

```bash
python scripts/clustering_analysis.py
```

Este script demonstra:
- Encontrar número ótimo de clusters (método do cotovelo, análise de silhueta)
- Comparar múltiplos algoritmos de clustering (K-Means, DBSCAN, Agglomerative, Gaussian Mixture)
- Avaliar qualidade do clustering sem verdade fundamental
- Visualizar resultados com projeção PCA

## Documentação de Referência

Esta skill inclui arquivos de referência abrangentes para aprofundamento em tópicos específicos:

### Referência Rápida
**Arquivo:** `references/quick_reference.md`
- Padrões comuns de importação e instruções de instalação
- Templates de workflow rápido para tarefas comuns
- Cheat sheets de seleção de algoritmo
- Padrões comuns e armadilhas
- Dicas de otimização de performance

### Aprendizado Supervisionado
**Arquivo:** `references/supervised_learning.md`
- Modelos lineares (regressão e classificação)
- Máquinas de Vetores de Suporte
- Árvores de Decisão e métodos ensemble
- K-Nearest Neighbors, Naive Bayes, Redes Neurais
- Guia de seleção de algoritmo

### Aprendizado Não Supervisionado
**Arquivo:** `references/unsupervised_learning.md`
- Todos os algoritmos de clustering com parâmetros e casos de uso
- Técnicas de redução de dimensionalidade
- Detecção de outlier e novidade
- Gaussian Mixture Models
- Guia de seleção de método

### Avaliação de Modelos
**Arquivo:** `references/model_evaluation.md`
- Estratégias de validação cruzada
- Métodos de ajuste de hiperparâmetros
- Métricas de classificação, regressão e clustering
- Curvas de aprendizado e validação
- Melhores práticas para seleção de modelo

### Pré-processamento
**Arquivo:** `references/preprocessing.md`
- Escalonamento e normalização de features
- Codificação de variáveis categóricas
- Imputação de valores ausentes
- Técnicas de engenharia de features
- Transformadores personalizados

### Pipelines e Composição
**Arquivo:** `references/pipelines_and_composition.md`
- Construção e uso de pipelines
- ColumnTransformer para tipos de dados mistos
- FeatureUnion para transformações paralelas
- Exemplos completos de ponta a ponta
- Melhores práticas

## Workflows Comuns

### Construir um Modelo de Classificação

1. **Carregar e explorar dados**
   ```python
   import pandas as pd
   df = pd.read_csv('data.csv')
   X = df.drop('target', axis=1)
   y = df['target']
   ```

2. **Dividir dados com estratificação**
   ```python
   from sklearn.model_selection import train_test_split
   X_train, X_test, y_train, y_test = train_test_split(
       X, y, test_size=0.2, stratify=y, random_state=42
   )
   ```

3. **Criar pipeline de pré-processamento**
   ```python
   from sklearn.pipeline import Pipeline
   from sklearn.preprocessing import StandardScaler
   from sklearn.compose import ColumnTransformer

   # Manipular features numéricas e categóricas separadamente
   preprocessor = ColumnTransformer([
       ('num', StandardScaler(), numeric_features),
       ('cat', OneHotEncoder(), categorical_features)
   ])
   ```

4. **Construir pipeline completo**
   ```python
   model = Pipeline([
       ('preprocessor', preprocessor),
       ('classifier', RandomForestClassifier(random_state=42))
   ])
   ```

5. **Ajustar hiperparâmetros**
   ```python
   from sklearn.model_selection import GridSearchCV

   param_grid = {
       'classifier__n_estimators': [100, 200],
       'classifier__max_depth': [10, 20, None]
   }

   grid_search = GridSearchCV(model, param_grid, cv=5)
   grid_search.fit(X_train, y_train)
   ```

6. **Avaliar no conjunto de teste**
   ```python
   from sklearn.metrics import classification_report

   best_model = grid_search.best_estimator_
   y_pred = best_model.predict(X_test)
   print(classification_report(y_test, y_pred))
   ```

### Realizar Análise de Clustering

1. **Pré-processar dados**
   ```python
   from sklearn.preprocessing import StandardScaler

   scaler = StandardScaler()
   X_scaled = scaler.fit_transform(X)
   ```

2. **Encontrar número ótimo de clusters**
   ```python
   from sklearn.cluster import KMeans
   from sklearn.metrics import silhouette_score

   scores = []
   for k in range(2, 11):
       kmeans = KMeans(n_clusters=k, random_state=42)
       labels = kmeans.fit_predict(X_scaled)
       scores.append(silhouette_score(X_scaled, labels))

   optimal_k = range(2, 11)[np.argmax(scores)]
   ```

3. **Aplicar clustering**
   ```python
   model = KMeans(n_clusters=optimal_k, random_state=42)
   labels = model.fit_predict(X_scaled)
   ```

4. **Visualizar com redução de dimensionalidade**
   ```python
   from sklearn.decomposition import PCA

   pca = PCA(n_components=2)
   X_2d = pca.fit_transform(X_scaled)

   plt.scatter(X_2d[:, 0], X_2d[:, 1], c=labels, cmap='viridis')
   ```

## Melhores Práticas

### Sempre Use Pipelines
Pipelines previnem vazamento de dados e garantem consistência:
```python
# Bom: Pré-processamento no pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LogisticRegression())
])

# Ruim: Pré-processamento fora (pode vazar informação)
X_scaled = StandardScaler().fit_transform(X)
```

### Ajuste nos Dados de Treinamento Apenas
Nunca ajuste nos dados de teste:
```python
# Bom
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # Apenas transformar

# Ruim
scaler = StandardScaler()
X_all_scaled = scaler.fit_transform(np.vstack([X_train, X_test]))
```

### Use Divisão Estratificada para Classificação
Preserve distribuição de classes:
```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
```

### Defina Random State para Reproduzibilidade
```python
model = RandomForestClassifier(n_estimators=100, random_state=42)
```

### Escolha Métricas Apropriadas
- Dados balanceados: Acurácia, F1-score
- Dados desbalanceados: Precisão, Recall, ROC AUC, Acurácia Balanceada
- Sensível ao custo: Definir scorer personalizado

### Escalone Features Quando Necessário
Algoritmos que requerem escalonamento de features:
- SVM, KNN, Redes Neurais
- PCA, Regressão Linear/Logística com regularização
- K-Means clustering

Algoritmos que não requerem escalonamento:
- Modelos baseados em árvores (Decision Trees, Random Forest, Gradient Boosting)
- Naive Bayes

## Resolvendo Problemas Comuns

### ConvergenceWarning
**Problema:** Modelo não convergiu
**Solução:** Aumente `max_iter` ou escalone features
```python
model = LogisticRegression(max_iter=1000)
```

### Performance Ruim no Conjunto de Teste
**Problema:** Overfitting
**Solução:** Use regularização, validação cruzada ou modelo mais simples
```python
# Adicionar regularização
model = Ridge(alpha=1.0)

# Usar validação cruzada
scores = cross_val_score(model, X, y, cv=5)
```

### Erro de Memória com Datasets Grandes
**Solução:** Use algoritmos projetados para dados grandes
```python
# Use SGD para datasets grandes
from sklearn.linear_model import SGDClassifier
model = SGDClassifier()

# Ou MiniBatchKMeans para clustering
from sklearn.cluster import MiniBatchKMeans
model = MiniBatchKMeans(n_clusters=8, batch_size=100)
```

## Recursos Adicionais

- Documentação Oficial: https://scikit-learn.org/stable/
- Guia do Usuário: https://scikit-learn.org/stable/user_guide.html
- Referência de API: https://scikit-learn.org/stable/api/index.html
- Galeria de Exemplos: https://scikit-learn.org/stable/auto_examples/index.html