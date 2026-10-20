# GitHub Copilot Instructions - Análise de Consumo de Álcool

## Visão Geral do Projeto

Projeto educacional de ciência de dados sobre consumo de álcool **per capita** por país (WHO/FiveThirtyEight 2010). Notebook em **português brasileiro** cobrindo EDA completa, visualizações geográficas interativas com Plotly, testes estatísticos de hipóteses e modelagem preditiva (regressão + classificação).

## Arquitetura e Estrutura

- **Notebook único**: `alcohol_consumption.ipynb` - 10 seções numeradas, 69 células, 195 países analisados
- **Dataset**: `drinks.csv` - 5 colunas (1 categórica: country; 4 numéricas: beer/wine/spirit_servings, total_litres_of_pure_alcohol)
- **Sem valores nulos**, sem duplicatas, outliers mantidos intencionalmente (Belarus 14.4L, Czech Republic 361 beer servings)

### Fluxo de Análise (10 Seções Fixas)
1. Libs → 2. Load → 3. EDA → 4. Transform → 5. Viz Geo → 6. Hipóteses → 7. Regressão → 8. Classificação → 9. Tuning → 10. Conclusões

**⚠️ CRÍTICO**: NUNCA renumere seções principais (1-10). Adicione subseções apenas (ex: `### 7.3 Nova Análise`).

## Convenções Críticas (IMUTÁVEIS)

### Nomenclatura Global
- **DataFrame principal**: `df_drinks` (referenciado em 40+ células)
- **Coluna de categoria**: `consumption_category` (pd.Categorical criado na Seção 4)
- **Labels fixas**: `['Very Low', 'Low', 'Medium', 'High', 'Very High']` (ordem importa para Plotly)
- **Ordem de categorias**: `category_order = ['Very Low', 'Low', 'Medium', 'High', 'Very High']`

### Sistema de Bins (NÃO MODIFICAR)
```python
bins = [0, 1, 4, 7, 10, float('inf')]  # Baseado em quartis dos dados de 2010
labels = ['Very Low', 'Low', 'Medium', 'High', 'Very High']
df_drinks['consumption_category'] = pd.cut(
    df_drinks['total_litres_of_pure_alcohol'], bins=bins, labels=labels, include_lowest=True
)
```
**Razão**: Bins derivados de análise quartil específica. Alterar quebra reprodutibilidade e comparabilidade com literatura.

## Stack e Padrões de Código

### Bibliotecas (Instaladas na Célula #VSC-cb1edb4d)
```python
# Visualização: plotly (mapas), matplotlib + seaborn (gráficos)
# Estatística: scipy (ttest_ind, shapiro, levene), statsmodels (regressão, VIF)
# ML: scikit-learn (modelos, pipelines, tuning, métricas)
# Dados: pandas, numpy
```

### Divisão de Responsabilidades por Biblioteca
- **Plotly Express**: Mapas coropléticos APENAS (`px.choropleth` com `locationmode='country names'`)
- **Matplotlib/Seaborn**: Scatter plots, heatmaps, histogramas, boxplots, confusion matrix, curvas ROC
- **SciPy**: Testes de hipótese (`ttest_ind` para Welch's t-test, `shapiro` para normalidade, `levene` para variâncias)
- **Scikit-learn**: Modelos de regressão/classificação, pipelines, `RandomizedSearchCV`, métricas (MAE, RMSE, R², F1, AUC)
- **Statsmodels**: Regressão linear com estatísticas detalhadas (`sm.OLS`), VIF para multicolinearidade

## Padrões de Código Específicos

### 1. Mapas Coropléticos (Plotly - Seção 5)

**Categórico (discrete)** para `consumption_category`:
```python
category_order = ['Very Low', 'Low', 'Medium', 'High', 'Very High']
fig = px.choropleth(
    df_drinks, locations="country", locationmode='country names',
    color="consumption_category", color_discrete_sequence=px.colors.sequential.Reds,
    category_orders={'consumption_category': category_order},  # ⚠️ OBRIGATÓRIO
    hover_data={'total_litres_of_pure_alcohol': ':.2f', 'beer_servings': True, ...},
    labels={'consumption_category': 'Categoria de Consumo', ...}
)
fig.update_layout(geo=dict(projection_type='natural earth'), height=600, width=1000)
fig.show()  # Sempre usar .show() para renderizar
```

**Contínuo (continuous)** para valores numéricos:
```python
fig = px.choropleth(df_drinks, color="total_litres_of_pure_alcohol", 
                    color_continuous_scale='Reds', ...)  # Note: continuous, não discrete
```

**Debugging mapas vazios**: Verificar `locationmode='country names'` (não ISO codes) e comparar `df_drinks['country']` com nomes oficiais do Plotly (ex: "Antigua & Barbuda" com &, "DR Congo" não "Democratic Republic").

### 2. Testes de Hipótese (Seção 6)

**Padrão Welch's t-test** (variâncias desiguais):
```python
# 1. Criar flag de grupo
islamic_countries = ["Afghanistan", "Pakistan", ...]
df_drinks["is_islamic"] = df_drinks["country"].isin(islamic_countries)

# 2. Separar grupos
group1 = df_drinks[df_drinks["is_islamic"]]['total_litres_of_pure_alcohol']
group2 = df_drinks[~df_drinks["is_islamic"]]['total_litres_of_pure_alcohol']

# 3. Verificar suposições (células #VSC-10ec5980)
stat1, p1 = shapiro(group1)  # Normalidade
stat_lev, p_lev = levene(group1, group2)  # Homocedasticidade

# 4. Executar teste t
result = ttest_ind(group1, group2, equal_var=False)  # equal_var=False para Welch
t_stat, p_value = result.statistic, result.pvalue

# 5. Reportar: médias, desvios, n, t-stat, p-valor, conclusão em português
```
**Importante**: Sempre verificar normalidade (Shapiro-Wilk) e variâncias (Levene) antes de aplicar teste t. Se p < 0.05 em Levene, usar `equal_var=False`.

### 3. Funções de Avaliação de Modelos (Seções 7-8)

**Regressão** (células #VSC-7af77076 e similares):
```python
def avaliar_regressao(modelo, X_tr, X_te, y_tr, y_te, nome):
    cv_r2 = cross_val_score(modelo, X_tr, y_tr, cv=5, scoring='r2').mean()
    modelo.fit(X_tr, y_tr); pred = modelo.predict(X_te)
    return {
        'modelo': nome,
        'MAE': round(mean_absolute_error(y_te, pred), 2),
        'RMSE': round(mean_squared_error(y_te, pred, squared=False), 2),
        'R2_teste': round(r2_score(y_te, pred), 3),
        'R2_CV (média k=5)': round(cv_r2, 3)
    }
# Armazena em: resultados_reg (pd.DataFrame)
```

**Classificação** (células #VSC-e9aaf6fe e similares):
```python
def avaliar_classificacao(modelo, X_tr, X_te, y_tr, y_te, nome):
    modelo.fit(X_tr, y_tr); preds = modelo.predict(X_te)
    probas = modelo.predict_proba(X_te)[:, 1] if hasattr(modelo, "predict_proba") else None
    report = classification_report(y_te, preds, output_dict=True)['weighted avg']
    return {
        'modelo': nome, 'acuracia': round((preds == y_te).mean(), 3),
        'precisao': round(report['precision'], 3), 'recall': round(report['recall'], 3),
        'f1': round(report['f1-score'], 3),
        'auc': round(roc_auc_score(y_te, probas), 3) if probas is not None else np.nan
    }, preds, probas  # Retorna métricas + predições + probabilidades
# Armazena em: resultados_cls (lista de dicts)
```

**Preparação de dados**:
```python
# Regressão (Seção 7): features = df_drinks[['beer_servings', 'wine_servings', 'spirit_servings']]
#                      target = df_drinks['total_litres_of_pure_alcohol']
# Classificação (Seção 8): X_cls = mesmas features
#                          y_cls = (consumption_category in ['High', 'Very High']).astype(int)
# Split: test_size=0.2, random_state=42, stratify=y_cls (para classificação apenas)
```

### 4. Tuning de Hiperparâmetros (Seção 9)

**RandomizedSearchCV com Pipelines**:
```python
# Ridge (regressão)
ridge_pipe = Pipeline([('scaler', StandardScaler()), ('model', Ridge())])
ridge_param = {'model__alpha': np.logspace(-3, 3, 20)}
ridge_search = RandomizedSearchCV(ridge_pipe, ridge_param, n_iter=10, cv=5, 
                                   scoring='r2', random_state=42)
ridge_search.fit(X_train, y_train)
# Comparar ridge_search.best_estimator_ com modelos base

# Logistic (classificação)
log_pipe = Pipeline([('scaler', StandardScaler()), ('model', LogisticRegression(max_iter=1000))])
log_param = {'model__C': np.logspace(-3, 3, 20), 'model__solver': ['liblinear', 'lbfgs']}
log_search = RandomizedSearchCV(log_pipe, log_param, n_iter=10, cv=5, 
                                 scoring='f1', random_state=42)
```
**⚠️ SEMPRE**: `random_state=42` para reprodutibilidade (usado em split, tuning, etc.).

### 5. Visualizações de Classificação (Seção 8)

**Matriz de Confusão**:
```python
cm = confusion_matrix(yc_test, preds_log)
sns.heatmap(cm, annot=True, fmt='d', cmap='Reds', cbar=False)
plt.xlabel('Predito'); plt.ylabel('Real')
plt.title('Matriz de confusão - Logistic Regression'); plt.show()
```

**Curva ROC**:
```python
fpr, tpr, _ = roc_curve(yc_test, prob_log)
plt.plot(fpr, tpr, color='firebrick', label=f'AUC = {roc_auc_score(yc_test, prob_log):.2f}')
plt.plot([0,1], [0,1], color='gray', linestyle='--')  # Diagonal de referência
plt.xlabel('Falso positivo'); plt.ylabel('Verdadeiro positivo')
plt.title('Curva ROC - Logistic Regression'); plt.legend(); plt.show()
```
**Paleta de cores**: Sempre `'firebrick'` ou `'darkblue'` para consistência com paleta `Reds`.

### 6. Análise de Multicolinearidade (Seção 7)

**VIF (Variance Inflation Factor)** antes de regressão múltipla:
```python
from statsmodels.stats.outliers_influence import variance_inflation_factor
vif_df = pd.DataFrame({
    'variável': features.columns,
    'VIF': [variance_inflation_factor(features.values, i) for i in range(len(features.columns))]
})
# VIF > 10 indica multicolinearidade severa. Neste dataset: todos VIF < 3 ✓
```

## Características do Dataset

### Estrutura
- **195 países**, **5 colunas** (1 categórica: country; 4 numéricas: beer/wine/spirit_servings, total_litres_of_pure_alcohol)
- **Sem valores nulos**, sem duplicatas, outliers mantidos intencionalmente
- **Unidades**: servings = doses/pessoa/ano; total_litres = litros álcool puro/pessoa/ano
- **Fonte**: WHO/GISAH 2010 (dados estáticos, sem série temporal)

### Outliers Notáveis (NÃO REMOVER)
- **Maior consumo**: Belarus (14.4 L/ano), Lithuania, Andorra (Europa Central/Oriental)
- **Consumo zero**: Afghanistan, Bangladesh, North Korea (religião/política)
- **Servings extremos**: Cook Islands (spirit=254), Czech Republic (beer=361)
- **Decisão**: Mantidos por representarem padrões culturais reais, essenciais para políticas públicas

### Nomes de Países (Plotly Compatibility)
A coluna `country` usa nomes específicos do Plotly (`locationmode='country names'`):
- ✅ "Antigua & Barbuda" (com &)
- ✅ "DR Congo" (não "Democratic Republic of the Congo")
- ✅ "Cote d'Ivoire" (sem acento)
- ⚠️ Ao adicionar dados, verificar compatibilidade com base geográfica do Plotly

## Workflows de Desenvolvimento

### Adicionar Nova Análise
1. Identifique seção apropriada (5=Viz, 6=Hipóteses, 7=Regressão, 8=Classificação)
2. Crie subseção numerada (ex: `### 7.3 Regressão Ridge com Regularização`)
3. **Sempre** preceda código com célula markdown explicando PORQUÊ/COMO
4. Use células separadas: transformação → verificação → interpretação
5. Para modelos: armazene resultados em `resultados_reg`/`resultados_cls` para comparação

### Debugging de Mapas Plotly
**Problema**: Países aparecem vazios no mapa
- ✅ Usar `locationmode='country names'` (não ISO codes)
- ✅ Comparar nomes em `df_drinks['country']` com lista oficial Plotly
- ✅ Sempre chamar `fig.show()` para renderizar (não apenas `fig`)
- ✅ Verificar se `category_order` está definido para mapas categóricos

### Executar Notebook
```powershell
# Instalar dependências (célula #VSC-cb1edb4d)
pip install pandas seaborn matplotlib plotly numpy scipy scikit-learn statsmodels jupyterlab

# Executar células sequencialmente (1→10)
# Reiniciar kernel se modificar df_drinks ou bins globais
```

## Contexto da Análise (Seção 10 - Conclusões)

### Hipóteses Confirmadas
- **Hipótese I**: Países islâmicos consomem ~5.6 L/ano menos (p < 0.001, Welch's t-test)
- **Hipótese II**: Beer tem maior correlação (r=0.83) vs. wine (r=0.66) e spirits (r=0.65)

### Padrões Descobertos
- **Geográficos**: Europa Central/Oriental + Rússia = alto consumo; MENA (Middle East/North Africa) = muito baixo
- **Culturais**: Religião islâmica = impacto negativo forte; clima frio = destilados populares
- **Estatísticos**: Beer explica 69% da variância do consumo total (R² simples), wine é preditor mais fraco

### Modelos Implementados (Métricas na Seção 10.1)
| Tipo | Modelo | Melhor Métrica | Observação |
|------|--------|----------------|------------|
| Regressão | Linear Múltipla | R²=0.91, RMSE=1.1L | **Recomendado** (interpretável) |
| Regressão | Ridge (tunado) | R² CV=0.90 | Ganho marginal ~2% |
| Classificação | Logistic Regression | F1=0.85, AUC=0.88 | **Melhor desempenho** |
| Classificação | GaussianNB | F1=0.78 | Baseline superado |

## Variáveis Kernel Principais (Estado Global)

**DataFrames**:
- `df_drinks` (195×6): Dataset principal com `consumption_category` adicionada
- `df_class` (195×7): Cópia com flag `high_consumption` (binário 0/1)
- `df_numeric` (195×4): Apenas colunas numéricas para análise de outliers

**Features/Targets**:
- Regressão: `features` (beer/wine/spirit_servings), `target` (total_litres), splits: `X_train`, `X_test`, `y_train`, `y_test`
- Classificação: `X_cls`, `y_cls` (high_consumption), splits: `Xc_train`, `Xc_test`, `yc_train`, `yc_test`

**Modelos Treinados**:
- `reg_beer`, `reg_multi` (LinearRegression), `poly2` (PolynomialFeatures+Scaler+LR)
- `nb_model` (GaussianNB), `log_model` (LogisticRegression)
- `ridge_search`, `log_search` (RandomizedSearchCV tunados)

**Resultados**:
- `resultados_reg` (pd.DataFrame): métricas de regressão
- `resultados_cls` (list[dict]): métricas de classificação

## Regras Críticas (⚠️ NÃO VIOLAR)

1. **NUNCA** renumere seções principais (1-10) → use subseções (ex: `### 7.3`)
2. **NUNCA** modifique `bins = [0, 1, 4, 7, 10, float('inf')]` → quebra reprodutibilidade
3. **NUNCA** altere `random_state=42` → necessário para reproduzir resultados
4. **NUNCA** renomeie `df_drinks` → 40+ células dependem deste nome
5. **SEMPRE** preceda código com markdown explicativo (padrão de 3 células: explicação → código → verificação)
6. **SEMPRE** use `fig.show()` (Plotly) ou `plt.show()` (Matplotlib) para renderizar
7. **SEMPRE** armazene métricas de modelos em `resultados_reg`/`resultados_cls` para comparação
8. **SEMPRE** use `stratify=y_cls` ao dividir dados de classificação (balanceamento)

---

## Referência Rápida

### IDs de Células Importantes
- `#VSC-cb1edb4d`: Instalação de dependências (pip install)
- `#VSC-3b417920`: Imports de todas as bibliotecas
- `#VSC-ba102e30`: Carregamento do dataset (`pd.read_csv("drinks.csv")`)
- `#VSC-ce1be8f6`: Criação de `consumption_category` com bins fixos
- `#VSC-73cd03c4`: Primeiro mapa coroplético (categórico)
- `#VSC-10ec5980`: Verificação de suposições (Shapiro-Wilk + Levene)
- `#VSC-ea789984`: Teste t completo (Hipótese I)
- `#VSC-7af77076`: Preparação de features/target para regressão
- `#VSC-e9aaf6fe`: Função `avaliar_classificacao()`
- `#VSC-202b6c78`: Comparação modelos base vs. tunados

### Comandos Úteis
```powershell
# Executar notebook completo
jupyter lab alcohol_consumption.ipynb

# Verificar compatibilidade de nomes de países
df_drinks['country'].unique()

# Resetar kernel e limpar outputs
# Kernel → Restart & Clear All Outputs (no menu do Jupyter)

# Exportar análises para HTML
jupyter nbconvert --to html alcohol_consumption.ipynb
```

### Onde Encontrar
- **Bins de categorização**: Seção 4.1 (célula #VSC-ce1be8f6)
- **Funções de avaliação**: Seções 7 (regressão) e 8 (classificação)
- **VIF para multicolinearidade**: Seção 7 (antes de regressão múltipla)
- **Curvas ROC e Confusion Matrix**: Seção 8 (após modelos de classificação)
- **Comparação de modelos**: Seção 9.1 (tabelas comparativas)
- **Conclusões e métricas finais**: Seção 10.1 (tabela resumida)
