---
name: statsmodels
description: "Kit de ferramentas de modelagem estatística. OLS, GLM, logística, ARIMA, séries temporais, testes de hipóteses, diagnósticos, AIC/BIC, para inferência estatística rigorosa e análise econométrica."
---

# Statsmodels: Modelagem Estatística e Econometria

## Visão Geral

Statsmodels é a principal biblioteca Python para modelagem estatística, fornecendo ferramentas para estimação, inferência e diagnósticos em uma ampla gama de métodos estatísticos. Aplique essa competência para análise estatística rigorosa, de regressão linear simples a modelos de séries temporais complexos e análises econométricas.

## Quando Usar Esta Competência

Esta competência deve ser usada quando:
- Ajustar modelos de regressão (OLS, WLS, GLS, regressão quantílica)
- Realizar modelagem linear generalizada (logística, Poisson, Gamma, etc.)
- Analisar resultados discretos (binário, multinomial, contagem, ordinal)
- Conduzir análise de séries temporais (ARIMA, SARIMAX, VAR, previsão)
- Executar testes estatísticos e diagnósticos
- Testar pressupostos do modelo (heterocedasticidade, autocorrelação, normalidade)
- Detectar outliers e observações influentes
- Comparar modelos (AIC/BIC, testes de razão de verossimilhança)
- Estimar efeitos causais
- Produzir tabelas estatísticas prontas para publicação e inferência

## Guia de Início Rápido

### Regressão Linear (OLS)

```python
import statsmodels.api as sm
import numpy as np
import pandas as pd

# Preparar dados - SEMPRE adicione constante para intercepto
X = sm.add_constant(X_data)

# Ajustar modelo OLS
model = sm.OLS(y, X)
results = model.fit()

# Ver resultados abrangentes
print(results.summary())

# Resultados principais
print(f"R-squared: {results.rsquared:.4f}")
print(f"Coeficientes:\\n{results.params}")
print(f"P-values:\\n{results.pvalues}")

# Previsões com intervalos de confiança
predictions = results.get_prediction(X_new)
pred_summary = predictions.summary_frame()
print(pred_summary)  # inclui média, IC, intervalos de previsão

# Diagnósticos
from statsmodels.stats.diagnostic import het_breuschpagan
bp_test = het_breuschpagan(results.resid, X)
print(f"P-value Breusch-Pagan: {bp_test[1]:.4f}")

# Visualizar resíduos
import matplotlib.pyplot as plt
plt.scatter(results.fittedvalues, results.resid)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Valores ajustados')
plt.ylabel('Resíduos')
plt.show()
```

### Regressão Logística (Resultados Binários)

```python
from statsmodels.discrete.discrete_model import Logit

# Adicionar constante
X = sm.add_constant(X_data)

# Ajustar modelo logit
model = Logit(y_binary, X)
results = model.fit()

print(results.summary())

# Razões de chance
odds_ratios = np.exp(results.params)
print("Razões de chance:\\n", odds_ratios)

# Probabilidades preditas
probs = results.predict(X)

# Previsões binárias (limiar 0.5)
predictions = (probs > 0.5).astype(int)

# Avaliação do modelo
from sklearn.metrics import classification_report, roc_auc_score

print(classification_report(y_binary, predictions))
print(f"AUC: {roc_auc_score(y_binary, probs):.4f}")

# Efeitos marginais
marginal = results.get_margeff()
print(marginal.summary())
```

### Séries Temporais (ARIMA)

```python
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# Verificar estacionariedade
from statsmodels.tsa.stattools import adfuller

adf_result = adfuller(y_series)
print(f"P-value ADF: {adf_result[1]:.4f}")

if adf_result[1] > 0.05:
    # Série não-estacionária, diferenciar
    y_diff = y_series.diff().dropna()

# Plotar ACF/PACF para identificar p, q
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
plot_acf(y_diff, lags=40, ax=ax1)
plot_pacf(y_diff, lags=40, ax=ax2)
plt.show()

# Ajustar ARIMA(p,d,q)
model = ARIMA(y_series, order=(1, 1, 1))
results = model.fit()

print(results.summary())

# Previsão
forecast = results.forecast(steps=10)
forecast_obj = results.get_forecast(steps=10)
forecast_df = forecast_obj.summary_frame()

print(forecast_df)  # inclui média e intervalos de confiança

# Diagnósticos residuais
results.plot_diagnostics(figsize=(12, 8))
plt.show()
```

### Modelos Lineares Generalizados (GLM)

```python
import statsmodels.api as sm

# Regressão Poisson para dados de contagem
X = sm.add_constant(X_data)
model = sm.GLM(y_counts, X, family=sm.families.Poisson())
results = model.fit()

print(results.summary())

# Razões de taxa (para Poisson com link log)
rate_ratios = np.exp(results.params)
print("Razões de taxa:\\n", rate_ratios)

# Verificar superdispersão
overdispersion = results.pearson_chi2 / results.df_resid
print(f"Superdispersão: {overdispersion:.2f}")

if overdispersion > 1.5:
    # Usar Binomial Negativo em vez disso
    from statsmodels.discrete.count_model import NegativeBinomial
    nb_model = NegativeBinomial(y_counts, X)
    nb_results = nb_model.fit()
    print(nb_results.summary())
```

## Capacidades Principais de Modelagem Estatística

### 1. Modelos de Regressão Linear

Suite abrangente de modelos lineares para resultados contínuos com várias estruturas de erro.

**Modelos disponíveis:**
- **OLS**: Regressão linear padrão com erros i.i.d.
- **WLS**: Mínimos quadrados ponderados para erros heterocedásticos
- **GLS**: Mínimos quadrados generalizados para estrutura de covariância arbitrária
- **GLSAR**: GLS com erros autorregressivos para séries temporais
- **Regressão Quantílica**: Quantis condicionais (robusto a outliers)
- **Efeitos Mistos**: Modelos hierárquicos/multinível com efeitos aleatórios
- **Recursiva/Móvel**: Estimação de parâmetros variantes no tempo

**Características principais:**
- Testes diagnósticos abrangentes
- Erros padrão robustos (HC, HAC, cluster-robusto)
- Estatísticas de influência (distância de Cook, alavancagem, DFFITS)
- Testes de hipóteses (testes F, testes de Wald)
- Comparação de modelos (AIC, BIC, testes de razão de verossimilhança)
- Previsão com intervalos de confiança e previsão

**Quando usar:** Variável de resultado contínua, deseja inferência sobre coeficientes, necessita diagnósticos

**Referência:** Veja `references/linear_models.md` para orientação detalhada sobre seleção de modelo, diagnósticos e melhores práticas.

### 2. Modelos Lineares Generalizados (GLM)

Framework flexível que estende modelos lineares para distribuições não-normais.

**Famílias de distribuição:**
- **Binomial**: Resultados binários ou proporções (regressão logística)
- **Poisson**: Dados de contagem
- **Binomial Negativo**: Contagens superdispersas
- **Gamma**: Dados contínuos positivos, com distribuição assimétrica à direita
- **Gaussiana Inversa**: Contínua positiva com estrutura de variância específica
- **Gaussiana**: Equivalente a OLS
- **Tweedie**: Família flexível para dados semicontínuos

**Funções de ligação:**
- Logit, Probit, Log, Identidade, Inversa, Sqrt, CLogLog, Power
- Escolha baseada em necessidades de interpretação e ajuste do modelo

**Características principais:**
- Estimação de máxima verossimilhança via IRLS
- Resíduos de desvio e Pearson
- Estatísticas de bondade do ajuste
- Medidas de pseudo R-quadrado
- Erros padrão robustos

**Quando usar:** Resultados não-normais, necessita especificações flexíveis de variância e ligação

**Referência:** Veja `references/glm.md` para seleção de família, funções de ligação, interpretação e diagnósticos.

### 3. Modelos de Escolha Discreta

Modelos para resultados categóricos e de contagem.

**Modelos binários:**
- **Logit**: Regressão logística (razões de chance)
- **Probit**: Regressão probit (distribuição normal)

**Modelos multinomiais:**
- **MNLogit**: Categorias desordenadas (3+ níveis)
- **Logit Condicional**: Modelos de escolha com variáveis específicas de alternativa
- **Modelo Ordenado**: Resultados ordinais (categorias ordenadas)

**Modelos de contagem:**
- **Poisson**: Modelo padrão de contagem
- **Binomial Negativo**: Contagens superdispersas
- **Zero-Inflado**: Zeros em excesso (ZIP, ZINB)
- **Modelos Hurdle**: Modelos em dois estágios para dados com muitos zeros

**Características principais:**
- Estimação de máxima verossimilhança
- Efeitos marginais na média ou efeitos marginais médios
- Comparação de modelos via AIC/BIC
- Probabilidades preditas e classificação
- Testes de bondade do ajuste

**Quando usar:** Resultados binários, categóricos ou de contagem

**Referência:** Veja `references/discrete_choice.md` para seleção de modelo, interpretação e avaliação.

### 4. Análise de Séries Temporais

Capacidades abrangentes de modelagem e previsão de séries temporais.

**Modelos univariados:**
- **AutoReg (AR)**: Modelos autorregressivos
- **ARIMA**: Média móvel integrada autorregressiva
- **SARIMAX**: ARIMA sazonal com variáveis exógenas
- **Suavização Exponencial**: Simples, Holt, Holt-Winters
- **ETS**: Modelos no espaço de estados de inovações

**Modelos multivariados:**
- **VAR**: Autorregressão vetorial
- **VARMAX**: VAR com MA e variáveis exógenas
- **Modelos de Fator Dinâmico**: Extrair fatores comuns
- **VECM**: Modelos de correção de erro vetorial (cointegração)

**Modelos avançados:**
- **Espaço de Estados**: Filtro de Kalman, especificações personalizadas
- **Mudança de Regime**: Modelos de switching de Markov
- **ARDL**: Autorregressão distribuída com defasagem

**Características principais:**
- Análise ACF/PACF para identificação de modelo
- Testes de estacionariedade (ADF, KPSS)
- Previsão com intervalos de previsão
- Diagnósticos de resíduos (Ljung-Box, heterocedasticidade)
- Teste de causalidade de Granger
- Funções de resposta ao impulso (IRF)
- Decomposição de variância do erro de previsão (FEVD)

**Quando usar:** Dados ordenados no tempo, previsão, compreensão da dinâmica temporal

**Referência:** Veja `references/time_series.md` para seleção de modelo, diagnósticos e métodos de previsão.

### 5. Testes Estatísticos e Diagnósticos

Capacidades extensivas de teste e diagnóstico para validação de modelo.

**Diagnósticos de resíduos:**
- Testes de autocorrelação (Ljung-Box, Durbin-Watson, Breusch-Godfrey)
- Testes de heterocedasticidade (Breusch-Pagan, White, ARCH)
- Testes de normalidade (Jarque-Bera, Omnibus, Anderson-Darling, Lilliefors)
- Testes de especificação (RESET, Harvey-Collier)

**Influência e outliers:**
- Alavancagem (valores de chapéu)
- Distância de Cook
- DFFITs e DFBETAs
- Resíduos estudentizados
- Gráficos de influência

**Teste de hipóteses:**
- Testes t (uma amostra, duas amostras, pareados)
- Testes de proporção
- Testes qui-quadrado
- Testes não-paramétricos (Mann-Whitney, Wilcoxon, Kruskal-Wallis)
- ANOVA (um fator, dois fatores, medidas repetidas)

**Comparações múltiplas:**
- HSD de Tukey
- Correção de Bonferroni
- Taxa de Descoberta Falsa (FDR)

**Tamanhos de efeito e poder:**
- d de Cohen, eta-quadrado
- Análise de poder para testes t, proporções
- Cálculos de tamanho de amostra

**Inferência robusta:**
- Erros padrão consistentes com heterocedasticidade (HC0-HC3)
- Erros padrão HAC (Newey-West)
- Erros padrão cluster-robustos

**Quando usar:** Validando pressupostos, detectando problemas, garantindo inferência robusta

**Referência:** Veja `references/stats_diagnostics.md` para procedimentos abrangentes de teste e diagnóstico.

## API de Fórmula (Estilo R)

Statsmodels suporta fórmulas estilo R para especificação intuitiva de modelo:

```python
import statsmodels.formula.api as smf

# OLS com fórmula
results = smf.ols('y ~ x1 + x2 + x1:x2', data=df).fit()

# Variáveis categóricas (dummy coding automático)
results = smf.ols('y ~ x1 + C(category)', data=df).fit()

# Interações
results = smf.ols('y ~ x1 * x2', data=df).fit()  # x1 + x2 + x1:x2

# Termos polinomiais
results = smf.ols('y ~ x + I(x**2)', data=df).fit()

# Logit
results = smf.logit('y ~ x1 + x2 + C(group)', data=df).fit()

# Poisson
results = smf.poisson('count ~ x1 + x2', data=df).fit()

# ARIMA (não disponível via fórmula, use API regular)
```

## Seleção e Comparação de Modelos

### Critérios de Informação

```python
# Comparar modelos usando AIC/BIC
models = {
    'Modelo 1': model1_results,
    'Modelo 2': model2_results,
    'Modelo 3': model3_results
}

comparison = pd.DataFrame({
    'AIC': {name: res.aic for name, res in models.items()},
    'BIC': {name: res.bic for name, res in models.items()},
    'Log-Likelihood': {name: res.llf for name, res in models.items()}
})

print(comparison.sort_values('AIC'))
# Valores mais baixos de AIC/BIC indicam melhor modelo
```

### Teste de Razão de Verossimilhança (Modelos Aninhados)

```python
# Para modelos aninhados (um é subconjunto do outro)
from scipy import stats

lr_stat = 2 * (full_model.llf - reduced_model.llf)
df = full_model.df_model - reduced_model.df_model
p_value = 1 - stats.chi2.cdf(lr_stat, df)

print(f"Estatística LR: {lr_stat:.4f}")
print(f"P-value: {p_value:.4f}")

if p_value < 0.05:
    print("Modelo completo significativamente melhor")
else:
    print("Modelo reduzido preferido (parcimônia)")
```

### Validação Cruzada

```python
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error

kf = KFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = []

for train_idx, val_idx in kf.split(X):
    X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
    y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

    # Ajustar modelo
    model = sm.OLS(y_train, X_train).fit()

    # Prever
    y_pred = model.predict(X_val)

    # Pontuar
    rmse = np.sqrt(mean_squared_error(y_val, y_pred))
    cv_scores.append(rmse)

print(f"CV RMSE: {np.mean(cv_scores):.4f} ± {np.std(cv_scores):.4f}")
```

## Melhores Práticas

### Preparação de Dados

1. **Sempre adicione constante**: Use `sm.add_constant()` a menos que exclua o intercepto
2. **Verificar valores ausentes**: Tratar ou imputar antes de ajustar
3. **Escalar se necessário**: Melhora convergência, interpretação (mas não necessário para modelos de árvore)
4. **Codificar categóricas**: Use API de fórmula ou dummy coding manual

### Construção de Modelo

1. **Começar simples**: Inicie com modelo básico, adicione complexidade conforme necessário
2. **Verificar pressupostos**: Testar resíduos, heterocedasticidade, autocorrelação
3. **Usar modelo apropriado**: Compatibilizar modelo com tipo de resultado (binário→Logit, contagem→Poisson)
4. **Considerar alternativas**: Se pressupostos violados, usar métodos robustos ou modelo diferente

### Inferência

1. **Reportar tamanhos de efeito**: Não apenas p-values
2. **Usar erros padrão robustos**: Quando heterocedasticidade ou clustering presente
3. **Comparações múltiplas**: Corrigir quando testando muitas hipóteses
4. **Intervalos de confiança**: Sempre reportar junto com estimativas pontuais

### Avaliação de Modelo

1. **Verificar resíduos**: Plotar resíduos vs ajustados, gráfico Q-Q
2. **Diagnósticos de influência**: Identificar e investigar observações influentes
3. **Validação fora da amostra**: Testar em conjunto de retenção ou validação cruzada
4. **Comparar modelos**: Usar AIC/BIC para não-aninhados, teste LR para aninhados

### Relatório

1. **Resumo abrangente**: Use `.summary()` para saída detalhada
2. **Documentar decisões**: Anotar transformações, observações excluídas
3. **Interpretar cuidadosamente**: Levar em conta funções de ligação (ex: exp(β) para link log)
4. **Visualizar**: Plotar previsões, intervalos de confiança, diagnósticos

## Fluxos de Trabalho Comuns

### Fluxo de Trabalho 1: Análise de Regressão Linear

1. Explorar dados (gráficos, descritivos)
2. Ajustar modelo OLS inicial
3. Verificar diagnósticos de resíduos
4. Testar heterocedasticidade, autocorrelação
5. Verificar multicolinearidade (VIF)
6. Identificar observações influentes
7. Reajustar com erros padrão robustos se necessário
8. Interpretar coeficientes e inferência
9. Validar em retenção ou via CV

### Fluxo de Trabalho 2: Classificação Binária

1. Ajustar regressão logística (Logit)
2. Verificar problemas de convergência
3. Interpretar razões de chance
4. Calcular efeitos marginais
5. Avaliar desempenho de classificação (AUC, matriz de confusão)
6. Verificar observações influentes
7. Comparar com modelos alternativos (Probit)
8. Validar previsões em conjunto de teste

### Fluxo de Trabalho 3: Análise de Dados de Contagem

1. Ajustar regressão Poisson
2. Verificar superdispersão
3. Se superdisperso, ajustar Binomial Negativo
4. Verificar zeros em excesso (considerar ZIP/ZINB)
5. Interpretar razões de taxa
6. Avaliar bondade do ajuste
7. Comparar modelos via AIC
8. Validar previsões

### Fluxo de Trabalho 4: Previsão de Série Temporal

1. Plotar série, verificar tendência/sazonalidade
2. Testar estacionariedade (ADF, KPSS)
3. Diferenciar se não-estacionária
4. Identificar p, q de ACF/PACF
5. Ajustar ARIMA ou SARIMAX
6. Verificar diagnósticos de resíduos (Ljung-Box)
7. Gerar previsões com intervalos de confiança
8. Avaliar acurácia de previsão em conjunto de teste

## Documentação de Referência

Esta competência inclui arquivos de referência abrangentes para orientação detalhada:

### references/linear_models.md
Cobertura detalhada de modelos de regressão linear incluindo:
- OLS, WLS, GLS, GLSAR, Regressão Quantílica
- Modelos de efeitos mistos
- Regressão recursiva e móvel
- Diagnósticos abrangentes (heterocedasticidade, autocorrelação, multicolinearidade)
- Estatísticas de influência e detecção de outliers
- Erros padrão robustos (HC, HAC, cluster)
- Testes de hipóteses e comparação de modelos

### references/glm.md
Guia completo para modelos lineares generalizados:
- Todas as famílias de distribuição (Binomial, Poisson, Gamma, etc.)
- Funções de ligação e quando usar cada uma
- Ajuste e interpretação de modelo
- Pseudo R-quadrado e bondade do ajuste
- Diagnósticos e análise de resíduos
- Aplicações (regressão logística, Poisson, Gamma)

### references/discrete_choice.md
Guia abrangente para modelos de resultado discreto:
- Modelos binários (Logit, Probit)
- Modelos multinomiais (MNLogit, Logit Condicional)
- Modelos de contagem (Poisson, Binomial Negativo, Zero-Inflado, Hurdle)
- Modelos ordinais
- Efeitos marginais e interpretação
- Diagnósticos e comparação de modelos

### references/time_series.md
Orientação detalhada para análise de série temporal:
- Modelos univariados (AR, ARIMA, SARIMAX, Suavização Exponencial)
- Modelos multivariados (VAR, VARMAX, Fator Dinâmico)
- Modelos no espaço de estados
- Testes de estacionariedade e diagnósticos
- Métodos e avaliação de previsão
- Causalidade de Granger, IRF, FEVD

### references/stats_diagnostics.md
Testes estatísticos e diagnósticos abrangentes:
- Diagnósticos de resíduos (autocorrelação, heterocedasticidade, normalidade)
- Detecção de influência e outliers
- Testes de hipóteses (paramétricos e não-paramétricos)
- ANOVA e testes pós-hoc
- Correção de comparações múltiplas
- Matrizes de covariância robusta
- Análise de poder e tamanhos de efeito

**Quando referenciar:**
- Necessita explicações detalhadas de parâmetros
- Escolher entre modelos similares
- Solucionar problemas de convergência ou diagnósticos
- Compreender estatísticas de teste específicas
- Procurar exemplos de código para recursos avançados

**Padrões de busca:**
```bash
# Encontrar informações sobre modelos específicos
grep -r "Regressão Quantílica" references/

# Encontrar testes de diagnóstico
grep -r "Breusch-Pagan" references/stats_diagnostics.md

# Encontrar orientação de série temporal
grep -r "SARIMAX" references/time_series.md
```

## Armadilhas Comuns a Evitar

1. **Esquecer termo de constante**: Sempre use `sm.add_constant()` a menos que nenhum intercepto desejado
2. **Ignorar pressupostos**: Verificar resíduos, heterocedasticidade, autocorrelação
3. **Modelo errado para tipo de resultado**: Binário→Logit/Probit, Contagem→Poisson/NB, não OLS
4. **Não verificar convergência**: Procurar avisos de otimização
5. **Mal interpretar coeficientes**: Lembrar de funções de ligação (log, logit, etc.)
6. **Usar Poisson com superdispersão**: Verificar dispersão, usar Binomial Negativo se necessário
7. **Não usar erros padrão robustos**: Quando heterocedasticidade ou clustering presentes
8. **Sobreajuste**: Muitos parâmetros em relação ao tamanho da amostra
9. **Vazamento de dados**: Ajustar em dados de teste ou usar informações futuras
10. **Não validar previsões**: Sempre verificar desempenho fora da amostra
11. **Comparar modelos não-aninhados**: Usar AIC/BIC, não teste LR
12. **Ignorar observações influentes**: Verificar distância de Cook e alavancagem
13. **Teste múltiplo**: Corrigir p-values ao testar muitas hipóteses
14. **Não diferenciar série temporal**: Ajustar ARIMA em dados não-estacionários
15. **Confundir intervalos de previsão vs confiança**: Intervalos de previsão são mais amplos

## Obtendo Ajuda

Para documentação detalhada e exemplos:
- Documentação oficial: https://www.statsmodels.org/stable/
- Guia do usuário: https://www.statsmodels.org/stable/user-guide.html
- Exemplos: https://www.statsmodels.org/stable/examples/index.html
- Referência da API: https://www.statsmodels.org/stable/api.html