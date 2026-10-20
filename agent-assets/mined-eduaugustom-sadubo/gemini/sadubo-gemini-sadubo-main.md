# SAD-ADUBO — Sistema Inteligente de Apoio à Decisão para Recomendação de Adubação

> **TCC — Bacharelado em Sistemas de Informação | UEG — UnU Santa Helena de Goiás | 2026**
> Autor: Eduardo Augusto de Oliveira Mendes | Orientadora: Prof.ª Me. Pollyana Queiroz

---

## Visão do Produto

Sistema web que recebe dados físico-químicos de solo, variáveis climáticas e histórico de manejo agrícola, e retorna a recomendação de fertilizante mais adequada — acompanhada de uma explicação interpretável (SHAP) acessível ao produtor rural. O MVP valida a metodologia usando o dataset público *Fertilizer Recommendation Dataset* (Kaggle, 10 000 registros, 20 features).

**O que o sistema NÃO faz no MVP:** app mobile, autenticação de usuários, banco de dados persistente, integração com API climática em tempo real, recomendação de dose quantitativa (kg/ha), SIG/mapas de variabilidade.

---

## Stack Tecnológico

| Camada | Tecnologia |
|---|---|
| Interface (Frontend) | Streamlit ≥ 1.30 |
| ML / Backend | Python 3.10+, scikit-learn ≥ 1.4, XGBoost ≥ 2.0 |
| Explicabilidade | SHAP ≥ 0.45 (TreeExplainer) |
| Visualização | Matplotlib, Seaborn, Plotly |
| Serialização | Joblib (modelos, Scaler, Encoders) |
| Dados | Pandas, NumPy |
| Versionamento | Git + GitHub |
| Deploy | Streamlit Community Cloud |

---

## Estrutura de Pastas

```
sad-adubo/
├── data/
│   └── fertilizer_recommendation.csv   # Dataset bruto (Kaggle)
├── notebooks/
│   ├── eda.ipynb                        # Análise exploratória do projeto
│   └── soil-based-fertilizer-recommendation-eda-10-ml-ref.ipynb  # Referência Kaggle
├── models/
│   ├── best_model.pkl                   # Modelo serializado (melhor F1)
│   ├── scaler.pkl                       # MinMaxScaler treinado
│   ├── encoders.pkl                     # Dict de LabelEncoders por coluna
│   ├── metrics.json                     # Métricas de todos os modelos (JSON)
│   ├── confusion_matrices.pkl           # Matrizes de confusão por modelo
│   ├── feature_names.pkl                # Ordem das features usada no treino
│   ├── label_classes.pkl                # Nomes das classes da variável-alvo
│   └── shap_global_values.pkl           # SHAP global pré-calculado (500 amostras)
├── src/
│   ├── preprocessing.py                 # Pipeline de encoding + scaling
│   ├── train.py                         # Treinamento e avaliação dos modelos
│   ├── predict.py                       # Inferência em tempo real
│   └── explainer.py                     # Cálculo e formatação do SHAP
├── app.py                               # Ponto de entrada do Streamlit
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Dataset

- **Fonte:** [Kaggle — Fertilizer Recommendation Dataset](https://www.kaggle.com/datasets/miadul/fertilizer-recommendation-dataset/data)
- **Dimensões:** 10 000 linhas × 20 colunas (19 features + 1 alvo)
- **Variável-alvo:** `Recommended_Fertilizer` (classificação multiclasse)
- **Valores nulos:** nenhum
- **Tarefa de ML:** classificação supervisionada multiclasse

### Grupos de Variáveis

| Grupo | Variáveis |
|---|---|
| **Solo** | Soil_Type, Soil_pH, Soil_Moisture, Organic_Carbon, Electrical_Conductivity, Nitrogen_Level, Phosphorus_Level, Potassium_Level |
| **Clima** | Temperature, Humidity, Rainfall |
| **Manejo / Cultivo** | Crop_Type, Crop_Growth_Stage, Season, Irrigation_Type, Previous_Crop, Region |
| **Histórico** | Fertilizer_Used_Last_Season, Yield_Last_Season |

### Insights da EDA (notebook anexo)

- Distribuição das classes-alvo **balanceada** — não requer SMOTE
- **Correlação positiva moderada** entre N, P e K (consistente com literatura agronômica)
- **Outliers preservados** em Rainfall e Temperature (valores extremos representam cenários reais)
- Features de maior importância (RF preliminar): **Soil_pH > Nitrogen_Level > Crop_Type**
- Variáveis categóricas requerem **Label Encoding** antes da modelagem

---

## Pipeline de Machine Learning

### 1. Pré-processamento

```python
# Ordem obrigatória — evitar data leakage
# 1. Fit APENAS no conjunto de treino
# 2. Transform em treino e teste

categorical_cols = ['Soil_Type', 'Crop_Type', 'Crop_Growth_Stage',
                    'Season', 'Irrigation_Type', 'Previous_Crop', 'Region']
numerical_cols   = ['Soil_pH', 'Soil_Moisture', 'Organic_Carbon',
                    'Electrical_Conductivity', 'Nitrogen_Level',
                    'Phosphorus_Level', 'Potassium_Level',
                    'Temperature', 'Humidity', 'Rainfall',
                    'Fertilizer_Used_Last_Season', 'Yield_Last_Season']
target_col       = 'Recommended_Fertilizer'

# Encoding: LabelEncoder por coluna categórica
# Scaling:  MinMaxScaler (range [0, 1]) nas colunas numéricas
# Split:    80/20, stratify=y, random_state=42
```

### 2. Modelos Comparados

| Algoritmo | Justificativa |
|---|---|
| Decision Tree | Baseline interpretável; o produtor pode ler as regras |
| Random Forest | Referência da literatura (Athayde 2023, acurácia > 99%) |
| SVM (kernel RBF) | Eficaz em espaços de alta dimensionalidade |
| **XGBoost** ⭐ | Candidato preferencial; estado da arte em dados tabulares |

### 3. Avaliação

- **Métrica primária de seleção:** F1-Score macro (k-fold, k=10)
- **Métricas secundárias:** Acurácia, Precisão, Recall, Matriz de Confusão
- **Critério:** modelo com maior F1-Score macro médio no cross-validation é serializado

### 4. Explicabilidade (SHAP)

```python
import shap

# Global: calculado offline sobre amostra do conjunto de teste
explainer    = shap.TreeExplainer(best_model)
shap_values  = explainer.shap_values(X_test_sample)

# Local: calculado em tempo real para cada predição do usuário
shap_local   = explainer.shap_values(X_user_input)
# → exibido como waterfall plot no Streamlit
```

---

## Funcionalidades do Sistema (Streamlit)

A aplicação é organizada em **4 abas**:

### Aba 1 — 🌱 Recomendação (Persona: Produtor Rural)

| ID | Funcionalidade | Prioridade |
|---|---|---|
| F01 | Formulário de dados de solo (N, P, K, pH, Umidade, C.Orgânico) | Alta |
| F02 | Formulário de dados climáticos (Temperatura, Umidade do Ar, Chuva) | Alta |
| F03 | Dropdowns de manejo (Tipo de Solo, Cultura, Irrigação, Fertilizante Anterior) | Alta |
| F04 | Validação de ranges agronômicos com mensagem de erro inline | Média |
| F05 | Card de resultado: nome do fertilizante + percentual de confiança | Alta |
| F06 | Gráfico SHAP waterfall — "Por que este fertilizante?" | Alta |
| F07 | Texto interpretativo automático em português (baseado nos top SHAP values) | Média |
| F08 | Botão: Download do resultado em CSV | Média |

### Aba 2 — 📊 Análise do Dataset (Persona: Pesquisador)

| ID | Funcionalidade | Prioridade |
|---|---|---|
| F09 | Distribuição das classes-alvo (countplot) | Média |
| F10 | Heatmap de correlação interativo (Plotly) | Média |
| F11 | Boxplots por variável numérica | Baixa |

### Aba 3 — 🤖 Desempenho dos Modelos (Persona: Pesquisador)

| ID | Funcionalidade | Prioridade |
|---|---|---|
| F12 | Tabela comparativa: F1-Score e Acurácia dos 4 modelos | Média |
| F13 | Matriz de confusão do modelo selecionado | Baixa |
| F14 | SHAP summary plot — importância global de features | Alta |

### Aba 4 — ℹ️ Sobre o Sistema

Descrição do projeto, metodologia simplificada, limitações do MVP e créditos acadêmicos.

---

## Requisitos Funcionais e Não Funcionais

### Funcionais

- `RF01` O sistema recebe dados físico-químicos do solo (N, P, K, pH, umidade, carbono orgânico)
- `RF02` O sistema recebe variáveis climáticas (temperatura, precipitação)
- `RF03` O sistema executa o modelo serializado e retorna a classe do fertilizante
- `RF04` Toda predição exibe justificativa via gráfico SHAP
- `RF05` O sistema permite exportação do resultado em `.csv`

### Não Funcionais

| ID | Categoria | Critério |
|---|---|---|
| RNF01 | Desempenho | Predição gerada em ≤ 2 segundos |
| RNF02 | Usabilidade | Usuário sem letramento técnico completa o fluxo sem ajuda |
| RNF03 | Portabilidade | Acessível via navegador, sem instalação local |
| RNF04 | Reprodutibilidade | `random_state=42` em todos os experimentos |
| RNF05 | Explicabilidade | SHAP exibido em 100% das predições |

---

## Critérios de Aceite do MVP

- [x] Acurácia ≥ 0.85 no conjunto de teste — *Decision Tree: 0.877* (verificar `models/metrics.json`)
- [x] F1-Score macro ≥ 0.74 no conjunto de teste — *Decision Tree: 0.744* (verificar `models/metrics.json`)
- [x] Predição gerada em ≤ 2 segundos (`st.cache_resource` implementado)
- [x] Gráfico SHAP renderizado para 100% das predições
- [x] Validação de inputs fora de range funcional
- [x] CSV exportado com: inputs + fertilizante recomendado + probabilidade
- [ ] URL pública no Streamlit Community Cloud (pendente deploy)
- [ ] Ao menos 2 usuários não técnicos completam o fluxo sem auxílio (pendente testes)
- [x] Repositório GitHub com README de instalação

---

## Personas

**Produtor Rural (Primária):** João, 42 anos, Goiás. Ensino médio, letramento digital básico. Quer inserir dados da análise de solo e receber a recomendação em segundos, sem depender de agrônomo para cada decisão. Conectividade rural limitada; prefere resultado visual e direto.

**Pesquisador / Técnico (Secundária):** Ana, 35 anos, agrônoma. Quer validar a recomendação de forma transparente, comparar algoritmos e entender quais variáveis mais impactam o modelo. Usa a aba de métricas e o SHAP global.

---

## Riscos e Mitigações

| Risco | Severidade | Mitigação |
|---|---|---|
| Dataset sem regionalização brasileira | Alta | Documentar claramente como limitação do protótipo; propor coleta de dados locais como trabalho futuro |
| Overfitting | Média | Cross-validation k=10; monitorar gap treino/teste |
| SHAP lento para inputs em batch | Média | SHAP global calculado offline; local apenas para 1 registro por vez |
| Confiança do técnico agrônomo no modelo | Alta | SHAP como ferramenta de transparência + referências bibliográficas na aba "Sobre" |

---

## Modelagem do Sistema

### Diagrama de Casos de Uso

#### Atores

| Ator | Tipo | Papel |
|---|---|---|
| Produtor Rural | Humano (primário) | Informa dados da propriedade, solicita recomendação e consulta resultado |
| Pesquisador / Administrador | Humano (secundário) | Treina, ajusta e valida o modelo; acompanha desempenho e atualiza a lógica do SAD |
| Base de Dados / Dataset | Sistema externo | Fornece os dados históricos usados no treinamento e validação |
| Motor de ML | Sistema interno | Responsável pela predição, avaliação e explicabilidade |

#### Casos de Uso — Produtor Rural

- Inserir dados de solo
- Inserir dados climáticos
- Inserir dados de manejo
- Solicitar recomendação de adubação
- Visualizar fertilizante recomendado
- Visualizar explicação da recomendação
- Exportar resultado em CSV

#### Casos de Uso — Pesquisador / Administrador

- Treinar modelo
- Validar modelo
- Comparar algoritmos
- Atualizar base de dados
- Consultar métricas de desempenho

#### Relações entre Casos de Uso

**"Solicitar recomendação de adubação"** `<<include>>`:
- Inserir dados de solo
- Inserir dados climáticos
- Inserir dados de manejo
- Processar dados
- Gerar predição
- Exibir recomendação

**"Gerar predição"** `<<include>>`:
- Aplicar modelo treinado

**"Visualizar explicação da recomendação"** `<<extend>>`:
- Solicitar recomendação de adubação

**"Exportar resultado em CSV"** `<<extend>>`:
- Visualizar fertilizante recomendado

---

### Diagramas de Fluxo

#### Fluxo 1 — Desenvolvimento do Sistema (Metodológico)

```
Coleta da base de dados
        ↓
Limpeza e pré-processamento
        ↓
Análise exploratória (EDA)
        ↓
Codificação de variáveis categóricas (Label Encoding)
        ↓
Normalização / escalonamento (MinMaxScaler)
        ↓
Divisão em treino e teste (80/20, stratify, random_state=42)
        ↓
Treinamento dos modelos (DT, RF, SVM, XGBoost)
        ↓
Validação cruzada (k-fold, k=10)
        ↓
Comparação das métricas (F1-Score macro, Acurácia, Matriz de Confusão)
        ↓
Seleção do melhor modelo
        ↓
Geração de explicabilidade com SHAP
        ↓
Serialização (best_model.pkl, scaler.pkl, encoders.pkl)
        ↓
Disponibilização no Streamlit
```

#### Fluxo 2 — Uso do Sistema (Produtor Rural)

```
Usuário acessa a interface web (URL pública)
        ↓
Preenche dados de solo, clima e manejo
        ↓
Sistema valida os campos
        ↓ (campos inválidos → mensagem de erro inline → retorna ao formulário)
Sistema executa o pré-processamento (encoding + scaling)
        ↓
Modelo treinado gera a recomendação (predict + predict_proba)
        ↓
Sistema exibe o fertilizante recomendado (card com % de confiança)
        ↓
Sistema exibe importância das variáveis (gráfico SHAP waterfall)
        ↓
Usuário deseja exportar?
    ├── Sim → Download do resultado em CSV
    └── Não → Fim
```

---

## Estado Atual da Implementação

Todos os módulos estão implementados e funcionais. O pipeline de treinamento foi executado e os artefatos estão serializados em `models/`. A interface Streamlit cobre as 4 abas e as 14 funcionalidades (F01–F14).

**Pendente:** deploy no Streamlit Community Cloud + testes com usuários não técnicos.

---

## Decisões de Design

### LabelEncoder fitado no dataset completo (pré-split)

Os `LabelEncoders` são ajustados no dataset **completo** antes da divisão treino/teste. Essa decisão é justificável porque o `LabelEncoder` mapeia apenas o domínio das categorias (quais valores existem), **sem vazamento de informação de valor** (média, distribuição, etc.). Caso fosse fitado apenas no treino, categorias presentes somente no teste causariam erros em produção. Esta abordagem é documentada na aba “Sobre o Sistema” da aplicação.

### SHAP global pré-calculado

O SHAP global é calculado durante o treinamento sobre uma amostra de 500 registros do conjunto de teste e salvo em `shap_global_values.pkl`. Isso evita latência na Aba 3 (Desempenho dos Modelos). O SHAP local (por predição) é calculado em tempo real para cada requisição do usuário.

### Cache com `st.cache_resource`

O modelo, encoders e scaler são carregados com `@st.cache_resource`, garantindo que o carregamento ocorra uma única vez por sessão. Isso assegura o RNF01 (predição ≤ 2 segundos).

### Persistência de resultado com `st.session_state`

O resultado da última predição é armazenado em `st.session_state` para que não seja perdido ao interagir com outros elementos da página (RNF02 — usabilidade).

### Texto interpretativo SHAP com direção de impacto

O módulo `explainer.py` gera automaticamente um texto em português descrevendo os top-3 fatores SHAP com indicação de direção (positivamente / negativamente), tornando a explicação acessível ao produtor rural sem letramento técnico em ML.
