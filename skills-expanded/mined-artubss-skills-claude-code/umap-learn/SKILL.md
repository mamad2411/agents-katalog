---
name: umap-learn
description: "Redução de dimensionalidade com UMAP. Aprendizado rápido e não-linear de variedades para visualização 2D/3D, pré-processamento de clustering (HDBSCAN), UMAP supervisionado/paramétrico, para dados de alta dimensionalidade."
---

# UMAP-Learn

## Visão Geral

UMAP (Uniform Manifold Approximation and Projection) é uma técnica de redução de dimensionalidade para visualização e redução de dimensionalidade não-linear geral. Aplique essa habilidade para embeddings rápidos e escaláveis que preservam estrutura local e global, aprendizado supervisionado e pré-processamento de clustering.

## Quick Start

### Instalação

```bash
uv pip install umap-learn
```

### Uso Básico

UMAP segue as convenções do scikit-learn e pode ser usado como um substituto direto para t-SNE ou PCA.

```python
import umap
from sklearn.preprocessing import StandardScaler

# Preparar dados (padronização é essencial)
scaled_data = StandardScaler().fit_transform(data)

# Método 1: Passo único (fit e transform)
embedding = umap.UMAP().fit_transform(scaled_data)

# Método 2: Passos separados (para reutilizar modelo treinado)
reducer = umap.UMAP(random_state=42)
reducer.fit(scaled_data)
embedding = reducer.embedding_  # Acessar o embedding treinado
```

**Requisito crítico de pré-processamento:** Sempre padronize as features para escalas comparáveis antes de aplicar UMAP, garantindo ponderação igual entre dimensões.

### Fluxo de Trabalho Típico

```python
import umap
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# 1. Pré-processar dados
scaler = StandardScaler()
scaled_data = scaler.fit_transform(raw_data)

# 2. Criar e ajustar UMAP
reducer = umap.UMAP(
    n_neighbors=15,
    min_dist=0.1,
    n_components=2,
    metric='euclidean',
    random_state=42
)
embedding = reducer.fit_transform(scaled_data)

# 3. Visualizar
plt.scatter(embedding[:, 0], embedding[:, 1], c=labels, cmap='Spectral', s=5)
plt.colorbar()
plt.title('UMAP Embedding')
plt.show()
```

## Guia de Ajuste de Parâmetros

UMAP possui quatro parâmetros primários que controlam o comportamento do embedding. Compreender esses é crucial para uso eficaz.

### n_neighbors (padrão: 15)

**Propósito:** Equilibra estrutura local versus global no embedding.

**Como funciona:** Controla o tamanho da vizinhança local que UMAP examina ao aprender a estrutura da variedade.

**Efeitos por valor:**
- **Valores baixos (2-5):** Enfatiza detalhe local fino, mas pode fragmentar dados em componentes desconectados
- **Valores médios (15-20):** Visão equilibrada de estrutura local e relacionamentos globais (ponto de partida recomendado)
- **Valores altos (50-200):** Prioriza estrutura topológica ampla em detrimento de detalhes refinados

**Recomendação:** Comece com 15 e ajuste com base nos resultados. Aumente para mais estrutura global, diminua para mais detalhe local.

### min_dist (padrão: 0.1)

**Propósito:** Controla como os pontos se agrupam no espaço de baixa dimensionalidade.

**Como funciona:** Define a distância mínima que os pontos precisam manter na representação de saída.

**Efeitos por valor:**
- **Valores baixos (0.0-0.1):** Cria embeddings aglomerados úteis para clustering; revela detalhes topológicos finos
- **Valores altos (0.5-0.99):** Impede compactação apertada; enfatiza preservação topológica ampla sobre estrutura local

**Recomendação:** Use 0.0 para aplicações de clustering, 0.1-0.3 para visualização, 0.5+ para estrutura solta.

### n_components (padrão: 2)

**Propósito:** Determina a dimensionalidade do espaço de saída incorporado.

**Recurso-chave:** Diferente de t-SNE, UMAP dimensiona bem na dimensão de embedding, permitindo uso além de visualização.

**Usos comuns:**
- **2-3 dimensões:** Visualização
- **5-10 dimensões:** Pré-processamento de clustering (melhor preserva densidade que 2D)
- **10-50 dimensões:** Feature engineering para modelos de ML downstream

**Recomendação:** Use 2 para visualização, 5-10 para clustering, superior para pipelines de ML.

### metric (padrão: 'euclidean')

**Propósito:** Especifica como a distância é calculada entre pontos de dados de entrada.

**Métricas suportadas:**
- **Variantes Minkowski:** euclidean, manhattan, chebyshev
- **Métricas espaciais:** canberra, braycurtis, haversine
- **Métricas de correlação:** cosine, correlation (boas para embeddings de texto/documentos)
- **Métricas para dados binários:** hamming, jaccard, dice, russellrao, kulsinski, rogerstanimoto, sokalmichener, sokalsneath, yule
- **Métricas customizadas:** Funções de distância definidas pelo usuário via Numba

**Recomendação:** Use euclidean para dados numéricos, cosine para vetores de texto/documentos, hamming para dados binários.

### Exemplo de Ajuste de Parâmetros

```python
# Para visualização com ênfase em estrutura local
umap.UMAP(n_neighbors=15, min_dist=0.1, n_components=2, metric='euclidean')

# Para pré-processamento de clustering
umap.UMAP(n_neighbors=30, min_dist=0.0, n_components=10, metric='euclidean')

# Para embeddings de documentos
umap.UMAP(n_neighbors=15, min_dist=0.1, n_components=2, metric='cosine')

# Para preservar estrutura global
umap.UMAP(n_neighbors=100, min_dist=0.5, n_components=2, metric='euclidean')
```

## Redução de Dimensionalidade Supervisionada e Semi-Supervisionada

UMAP oferece suporte à incorporação de informação de rótulos para guiar o processo de embedding, permitindo separação de classes enquanto preserva a estrutura interna.

### UMAP Supervisionado

Passe rótulos-alvo via parâmetro `y` ao fazer fit:

```python
# Redução de dimensionalidade supervisionada
embedding = umap.UMAP().fit_transform(data, y=labels)
```

**Benefícios-chave:**
- Alcança classes claramente separadas
- Preserva estrutura interna dentro de cada classe
- Mantém relacionamentos globais entre classes

**Quando usar:** Quando você tem dados rotulados e quer separar classes conhecidas enquanto mantém embeddings significativos de pontos.

### UMAP Semi-Supervisionado

Para rótulos parciais, marque pontos não rotulados com `-1` seguindo a convenção do scikit-learn:

```python
# Criar rótulos semi-supervisionados
semi_labels = labels.copy()
semi_labels[unlabeled_indices] = -1

# Fazer fit com rótulos parciais
embedding = umap.UMAP().fit_transform(data, y=semi_labels)
```

**Quando usar:** Quando a rotulação é cara ou você tem mais dados do que rótulos disponíveis.

### Aprendizado de Métrica com UMAP

Treine um embedding supervisionado em dados rotulados, depois aplique a dados não rotulados novos:

```python
# Treinar em dados rotulados
mapper = umap.UMAP().fit(train_data, train_labels)

# Transformar dados de teste não rotulados
test_embedding = mapper.transform(test_data)

# Usar como feature engineering para classificador downstream
from sklearn.svm import SVC
clf = SVC().fit(mapper.embedding_, train_labels)
predictions = clf.predict(test_embedding)
```

**Quando usar:** Para feature engineering supervisionado em pipelines de machine learning.

## UMAP para Clustering

UMAP serve como pré-processamento eficaz para algoritmos de clustering baseados em densidade como HDBSCAN, superando a maldição da dimensionalidade.

### Melhores Práticas para Clustering

**Princípio-chave:** Configure UMAP diferentemente para clustering do que para visualização.

**Parâmetros recomendados:**
- **n_neighbors:** Aumente para ~30 (padrão 15 é muito local e pode criar clusters artificialmente refinados)
- **min_dist:** Defina para 0.0 (empacote pontos densamente dentro de clusters para limites mais claros)
- **n_components:** Use 5-10 dimensões (mantém performance enquanto melhora preservação de densidade vs. 2D)

### Fluxo de Trabalho de Clustering

```python
import umap
import hdbscan
from sklearn.preprocessing import StandardScaler

# 1. Pré-processar dados
scaled_data = StandardScaler().fit_transform(data)

# 2. UMAP com parâmetros otimizados para clustering
reducer = umap.UMAP(
    n_neighbors=30,
    min_dist=0.0,
    n_components=10,  # Superior a 2 para melhor preservação de densidade
    metric='euclidean',
    random_state=42
)
embedding = reducer.fit_transform(scaled_data)

# 3. Aplicar clustering HDBSCAN
clusterer = hdbscan.HDBSCAN(
    min_cluster_size=15,
    min_samples=5,
    metric='euclidean'
)
labels = clusterer.fit_predict(embedding)

# 4. Avaliar
from sklearn.metrics import adjusted_rand_score
score = adjusted_rand_score(true_labels, labels)
print(f"Adjusted Rand Score: {score:.3f}")
print(f"Number of clusters: {len(set(labels)) - (1 if -1 in labels else 0)}")
print(f"Noise points: {sum(labels == -1)}")
```

### Visualização Após Clustering

```python
# Criar embedding 2D para visualização (separado de clustering)
vis_reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, n_components=2, random_state=42)
vis_embedding = vis_reducer.fit_transform(scaled_data)

# Plotar com rótulos de cluster
import matplotlib.pyplot as plt
plt.scatter(vis_embedding[:, 0], vis_embedding[:, 1], c=labels, cmap='Spectral', s=5)
plt.colorbar()
plt.title('UMAP Visualization with HDBSCAN Clusters')
plt.show()
```

**Ressalva importante:** UMAP não preserva completamente a densidade e pode criar divisões de clusters artificiais. Sempre valide e explore os clusters resultantes.

## Transformando Dados Novos

UMAP permite pré-processamento de dados novos através de seu método `transform()`, permitindo que modelos treinados projetem dados invistos no espaço de embedding aprendido.

### Uso Básico de Transform

```python
# Treinar em dados de treinamento
trans = umap.UMAP(n_neighbors=15, random_state=42).fit(X_train)

# Transformar dados de teste
test_embedding = trans.transform(X_test)
```

### Integração com Pipelines de Machine Learning

```python
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import umap

# Dividir dados
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2)

# Pré-processar
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Treinar UMAP
reducer = umap.UMAP(n_components=10, random_state=42)
X_train_embedded = reducer.fit_transform(X_train_scaled)
X_test_embedded = reducer.transform(X_test_scaled)

# Treinar classificador nos embeddings
clf = SVC()
clf.fit(X_train_embedded, y_train)
accuracy = clf.score(X_test_embedded, y_test)
print(f"Test accuracy: {accuracy:.3f}")
```

### Considerações Importantes

**Consistência de dados:** O método transform assume que a distribuição geral no espaço de dimensionalidade superior é consistente entre dados de treinamento e teste. Quando essa suposição falha, considere usar Parametric UMAP.

**Performance:** Operações de transform são eficientes (tipicamente <1 segundo), embora chamadas iniciais possam ser mais lentas devido à compilação JIT do Numba.

**Compatibilidade com scikit-learn:** UMAP segue convenções padrão do sklearn e funciona perfeitamente em pipelines:

```python
from sklearn.pipeline import Pipeline

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('umap', umap.UMAP(n_components=10)),
    ('classifier', SVC())
])

pipeline.fit(X_train, y_train)
predictions = pipeline.predict(X_test)
```

## Recursos Avançados

### Parametric UMAP

Parametric UMAP substitui otimização direta de embedding com uma função de mapeamento de rede neural aprendida.

**Diferenças-chave de UMAP padrão:**
- Usa TensorFlow/Keras para treinar redes codificadoras
- Permite transformação eficiente de dados novos
- Oferece suporte a reconstrução via redes decodificadoras (inverse transform)
- Permite arquiteturas customizadas (CNNs para imagens, RNNs para sequências)

**Instalação:**
```bash
uv pip install umap-learn[parametric_umap]
# Requer TensorFlow 2.x
```

**Uso básico:**
```python
from umap.parametric_umap import ParametricUMAP

# Arquitetura padrão (rede totalmente conectada de 3 camadas com 100 neurônios)
embedder = ParametricUMAP()
embedding = embedder.fit_transform(data)

# Transformar dados novos eficientemente
new_embedding = embedder.transform(new_data)
```

**Arquitetura customizada:**
```python
import tensorflow as tf

# Definir codificador customizado
encoder = tf.keras.Sequential([
    tf.keras.layers.InputLayer(input_shape=(input_dim,)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(2)  # Dimensão de saída
])

embedder = ParametricUMAP(encoder=encoder, dims=(input_dim,))
embedding = embedder.fit_transform(data)
```

**Quando usar Parametric UMAP:**
- Precisa de transformação eficiente de dados novos após treinamento
- Requer capacidades de reconstrução (inverse transforms)
- Quer combinar UMAP com autoencoders
- Trabalha com tipos de dados complexos (imagens, sequências) que se beneficiam de arquiteturas especializadas

**Quando usar UMAP padrão:**
- Precisa de simplicidade e prototipagem rápida
- Dataset é pequeno e eficiência computacional não é crítica
- Não requer transformações aprendidas para dados futuros

### Inverse Transforms

Inverse transforms permitem reconstrução de dados de alta dimensionalidade a partir de embeddings de baixa dimensionalidade.

**Uso básico:**
```python
reducer = umap.UMAP()
embedding = reducer.fit_transform(data)

# Reconstruir dados de alta dimensionalidade a partir de coordenadas de embedding
reconstructed = reducer.inverse_transform(embedding)
```

**Limitações importantes:**
- Operação computacionalmente cara
- Funciona mal fora do convex hull do embedding
- Precisão diminui em regiões com lacunas entre clusters

**Casos de uso:**
- Compreender estrutura de dados incorporados
- Visualizar transições suaves entre clusters
- Explorar interpolações entre pontos de dados
- Gerar amostras sintéticas no espaço de embedding

**Exemplo: Explorando espaço de embedding:**
```python
import numpy as np

# Criar grade de pontos no espaço de embedding
x = np.linspace(embedding[:, 0].min(), embedding[:, 0].max(), 10)
y = np.linspace(embedding[:, 1].min(), embedding[:, 1].max(), 10)
xx, yy = np.meshgrid(x, y)
grid_points = np.c_[xx.ravel(), yy.ravel()]

# Reconstruir amostras da grade
reconstructed_samples = reducer.inverse_transform(grid_points)
```

### AlignedUMAP

Para analisar datasets temporais ou relacionados (ex: experimentos de série temporal, dados de lote):

```python
from umap import AlignedUMAP

# Lista de datasets relacionados
datasets = [day1_data, day2_data, day3_data]

# Criar embeddings alinhados
mapper = AlignedUMAP().fit(datasets)
aligned_embeddings = mapper.embeddings_  # Lista de embeddings
```

**Quando usar:** Comparar embeddings entre datasets relacionados mantendo sistemas de coordenadas consistentes.

## Reprodutibilidade

Para garantir resultados reproduzíveis, sempre defina o parâmetro `random_state`:

```python
reducer = umap.UMAP(random_state=42)
```

UMAP usa otimização estocástica, então resultados variarão ligeiramente entre execuções sem um estado aleatório fixo.

## Problemas Comuns e Soluções

**Problema:** Componentes desconectados ou clusters fragmentados
- **Solução:** Aumente `n_neighbors` para enfatizar mais estrutura global

**Problema:** Clusters muito espalhados ou não bem separados
- **Solução:** Diminua `min_dist` para permitir empacotamento mais apertado

**Problema:** Resultados ruins de clustering
- **Solução:** Use parâmetros específicos para clustering (n_neighbors=30, min_dist=0.0, n_components=5-10)

**Problema:** Resultados de transform diferem significativamente do treinamento
- **Solução:** Garanta que a distribuição de dados de teste corresponda ao treinamento, ou use Parametric UMAP

**Problema:** Performance lenta em datasets grandes
- **Solução:** Defina `low_memory=True` (padrão), ou considere redução de dimensionalidade com PCA primeiro

**Problema:** Todos os pontos colapsados em um único cluster
- **Solução:** Verifique pré-processamento de dados (garanta escalonamento apropriado), aumente `min_dist`

## Recursos

### references/

Contém documentação detalhada da API:
- `api_reference.md`: Parâmetros e métodos completos da classe UMAP

Carregue essas referências quando informação detalhada de parâmetros ou uso avançado de métodos for necessário.