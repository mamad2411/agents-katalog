---
name: statistical-analysis
description: "Kit de ferramentas de análise estatística. Testes de hipótese (teste t, ANOVA, qui-quadrado), regressão, correlação, estatística Bayesiana, análise de poder, verificação de pressupostos, relatórios em formato APA, para pesquisa acadêmica."
---

# Análise Estatística

## Visão Geral

Análise estatística é um processo sistemático para testar hipóteses e quantificar relações. Conduza testes de hipótese (teste t, ANOVA, qui-quadrado), regressão, correlação e análises Bayesianas com verificação de pressupostos e relatórios em formato APA. Aplique essa habilidade em pesquisa acadêmica.

## Quando Usar Esta Habilidade

Esta habilidade deve ser usada quando:
- Conduzindo testes de hipótese estatística (testes t, ANOVA, qui-quadrado)
- Realizando análises de regressão ou correlação
- Executando análises estatísticas Bayesianas
- Verificando pressupostos estatísticos e diagnósticos
- Calculando tamanhos de efeito e conduzindo análises de poder
- Relatando resultados estatísticos em formato APA
- Analisando dados experimentais ou observacionais para pesquisa

---

## Capacidades Principais

### 1. Seleção e Planejamento de Testes
- Escolher testes estatísticos apropriados com base em questões de pesquisa e características dos dados
- Conduzir análises de poder a priori para determinar tamanhos de amostra necessários
- Planejar estratégias de análise incluindo correções para comparações múltiplas

### 2. Verificação de Pressupostos
- Verificar automaticamente todos os pressupostos relevantes antes de executar testes
- Fornecer visualizações diagnósticas (gráficos Q-Q, gráficos de resíduos, box plots)
- Recomendar ações corretivas quando pressupostos são violados

### 3. Testes Estatísticos
- Testes de hipótese: testes t, ANOVA, qui-quadrado, alternativas não-paramétricas
- Regressão: linear, múltipla, logística, com diagnósticos
- Correlações: Pearson, Spearman, com intervalos de confiança
- Alternativas Bayesianas: testes t Bayesianos, ANOVA, regressão com Fatores de Bayes

### 4. Tamanhos de Efeito e Interpretação
- Calcular e interpretar tamanhos de efeito apropriados para todas as análises
- Fornecer intervalos de confiança para estimativas de efeito
- Distinguir significância estatística de significância prática

### 5. Relatórios Profissionais
- Gerar relatórios estatísticos em estilo APA
- Criar figuras e tabelas prontas para publicação
- Fornecer interpretação completa com todas as estatísticas necessárias

---

## Árvore de Decisão do Fluxo de Trabalho

Use esta árvore de decisão para determinar seu caminho de análise:

```
INÍCIO
│
├─ Precisa SELECIONAR um teste estatístico?
│  └─ SIM → Veja "Guia de Seleção de Testes"
│  └─ NÃO → Continue
│
├─ Pronto para verificar PRESSUPOSTOS?
│  └─ SIM → Veja "Verificação de Pressupostos"
│  └─ NÃO → Continue
│
├─ Pronto para executar ANÁLISE?
│  └─ SIM → Veja "Executando Testes Estatísticos"
│  └─ NÃO → Continue
│
└─ Precisa RELATAR resultados?
   └─ SIM → Veja "Relatando Resultados"
```

---

## Guia de Seleção de Testes

### Referência Rápida: Escolhendo o Teste Correto

Use `references/test_selection_guide.md` para orientação abrangente. Referência rápida:

**Comparando Dois Grupos:**
- Independente, contínuo, normal → Teste t independente
- Independente, contínuo, não-normal → Teste U de Mann-Whitney
- Pareado, contínuo, normal → Teste t pareado
- Pareado, contínuo, não-normal → Teste de postos com sinais de Wilcoxon
- Resultado binário → Qui-quadrado ou teste exato de Fisher

**Comparando 3+ Grupos:**
- Independente, contínuo, normal → ANOVA unidirecional
- Independente, contínuo, não-normal → Teste de Kruskal-Wallis
- Pareado, contínuo, normal → ANOVA de medidas repetidas
- Pareado, contínuo, não-normal → Teste de Friedman

**Relações:**
- Duas variáveis contínuas → Correlação de Pearson (normal) ou Spearman (não-normal)
- Resultado contínuo com preditor(es) → Regressão linear
- Resultado binário com preditor(es) → Regressão logística

**Alternativas Bayesianas:**
Todos os testes têm versões Bayesianas que fornecem:
- Afirmações de probabilidade diretas sobre hipóteses
- Fatores de Bayes quantificando evidência
- Capacidade de apoiar a hipótese nula
- Veja `references/bayesian_statistics.md`

---

## Verificação de Pressupostos

### Verificação Sistemática de Pressupostos

**SEMPRE verifique pressupostos antes de interpretar resultados de testes.**

Use o módulo `scripts/assumption_checks.py` fornecido para verificação automatizada:

```python
from scripts.assumption_checks import comprehensive_assumption_check

# Verificação abrangente com visualizações
results = comprehensive_assumption_check(
    data=df,
    value_col='score',
    group_col='group',  # Opcional: para comparações entre grupos
    alpha=0.05
)
```

Isso executa:
1. **Detecção de outliers** (métodos IQR e z-score)
2. **Testes de normalidade** (teste de Shapiro-Wilk + gráficos Q-Q)
3. **Homogeneidade de variância** (teste de Levene + box plots)
4. **Interpretação e recomendações**

### Verificações Individuais de Pressupostos

Para verificações direcionadas, use funções individuais:

```python
from scripts.assumption_checks import (
    check_normality,
    check_normality_per_group,
    check_homogeneity_of_variance,
    check_linearity,
    detect_outliers
)

# Exemplo: Verificar normalidade com visualização
result = check_normality(
    data=df['score'],
    name='Pontuação do Teste',
    alpha=0.05,
    plot=True
)
print(result['interpretation'])
print(result['recommendation'])
```

### O Que Fazer Quando Pressupostos São Violados

**Normalidade violada:**
- Violação leve + n > 30 por grupo → Prossiga com teste paramétrico (robusto)
- Violação moderada → Use alternativa não-paramétrica
- Violação severa → Transforme dados ou use teste não-paramétrico

**Homogeneidade de variância violada:**
- Para teste t → Use teste t de Welch
- Para ANOVA → Use ANOVA de Welch ou ANOVA de Brown-Forsythe
- Para regressão → Use erros padrão robustos ou mínimos quadrados ponderados

**Linearidade violada (regressão):**
- Adicione termos polinomiais
- Transforme variáveis
- Use modelos não-lineares ou GAM

Veja `references/assumptions_and_diagnostics.md` para orientação abrangente.

---

## Executando Testes Estatísticos

### Bibliotecas Python

Bibliotecas principais para análise estatística:
- **scipy.stats**: Testes estatísticos principais
- **statsmodels**: Regressão avançada e diagnósticos
- **pingouin**: Testes estatísticos fáceis de usar com tamanhos de efeito
- **pymc**: Modelagem estatística Bayesiana
- **arviz**: Visualização Bayesiana e diagnósticos

### Exemplos de Análises

#### Teste t com Relatório Completo

```python
import pingouin as pg
import numpy as np

# Executar teste t independente
result = pg.ttest(group_a, group_b, correction='auto')

# Extrair resultados
t_stat = result['T'].values[0]
df = result['dof'].values[0]
p_value = result['p-val'].values[0]
cohens_d = result['cohen-d'].values[0]
ci_lower = result['CI95%'].values[0][0]
ci_upper = result['CI95%'].values[0][1]

# Relatar
print(f"t({df:.0f}) = {t_stat:.2f}, p = {p_value:.3f}")
print(f"d de Cohen = {cohens_d:.2f}, IC 95% [{ci_lower:.2f}, {ci_upper:.2f}]")
```

#### ANOVA com Testes Pós-Hoc

```python
import pingouin as pg

# ANOVA unidirecional
aov = pg.anova(dv='score', between='group', data=df, detailed=True)
print(aov)

# Se significativo, conduza testes pós-hoc
if aov['p-unc'].values[0] < 0.05:
    posthoc = pg.pairwise_tukey(dv='score', between='group', data=df)
    print(posthoc)

# Tamanho de efeito
eta_squared = aov['np2'].values[0]  # Eta-quadrado parcial
print(f"η² parcial = {eta_squared:.3f}")
```

#### Regressão Linear com Diagnósticos

```python
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Ajustar modelo
X = sm.add_constant(X_predictors)  # Adicionar intercepto
model = sm.OLS(y, X).fit()

# Resumo
print(model.summary())

# Verificar multicolinearidade (VIF)
vif_data = pd.DataFrame()
vif_data["Variable"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
print(vif_data)

# Verificar pressupostos
residuals = model.resid
fitted = model.fittedvalues

# Gráficos de resíduos
import matplotlib.pyplot as plt
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Resíduos vs ajustados
axes[0, 0].scatter(fitted, residuals, alpha=0.6)
axes[0, 0].axhline(y=0, color='r', linestyle='--')
axes[0, 0].set_xlabel('Valores ajustados')
axes[0, 0].set_ylabel('Resíduos')
axes[0, 0].set_title('Resíduos vs Ajustados')

# Gráfico Q-Q
from scipy import stats
stats.probplot(residuals, dist="norm", plot=axes[0, 1])
axes[0, 1].set_title('Q-Q Normal')

# Scale-Location
axes[1, 0].scatter(fitted, np.sqrt(np.abs(residuals / residuals.std())), alpha=0.6)
axes[1, 0].set_xlabel('Valores ajustados')
axes[1, 0].set_ylabel('√|Resíduos padronizados|')
axes[1, 0].set_title('Scale-Location')

# Histograma de resíduos
axes[1, 1].hist(residuals, bins=20, edgecolor='black', alpha=0.7)
axes[1, 1].set_xlabel('Resíduos')
axes[1, 1].set_ylabel('Frequência')
axes[1, 1].set_title('Histograma de Resíduos')

plt.tight_layout()
plt.show()
```

#### Teste t Bayesiano

```python
import pymc as pm
import arviz as az
import numpy as np

with pm.Model() as model:
    # Priors
    mu1 = pm.Normal('mu_group1', mu=0, sigma=10)
    mu2 = pm.Normal('mu_group2', mu=0, sigma=10)
    sigma = pm.HalfNormal('sigma', sigma=10)

    # Likelihood
    y1 = pm.Normal('y1', mu=mu1, sigma=sigma, observed=group_a)
    y2 = pm.Normal('y2', mu=mu2, sigma=sigma, observed=group_b)

    # Quantidade derivada
    diff = pm.Deterministic('difference', mu1 - mu2)

    # Amostra
    trace = pm.sample(2000, tune=1000, return_inferencedata=True)

# Resumir
print(az.summary(trace, var_names=['difference']))

# Probabilidade de que grupo1 > grupo2
prob_greater = np.mean(trace.posterior['difference'].values > 0)
print(f"P(μ₁ > μ₂ | dados) = {prob_greater:.3f}")

# Plotar posterior
az.plot_posterior(trace, var_names=['difference'], ref_val=0)
```

---

## Tamanhos de Efeito

### Sempre Calcule Tamanhos de Efeito

**Tamanhos de efeito quantificam magnitude, enquanto valores p apenas indicam existência de um efeito.**

Veja `references/effect_sizes_and_power.md` para orientação abrangente.

### Referência Rápida: Tamanhos de Efeito Comuns

| Teste | Tamanho de Efeito | Pequeno | Médio | Grande |
|------|-------------|-------|--------|-------|
| Teste t | d de Cohen | 0,20 | 0,50 | 0,80 |
| ANOVA | η²_p | 0,01 | 0,06 | 0,14 |
| Correlação | r | 0,10 | 0,30 | 0,50 |
| Regressão | R² | 0,02 | 0,13 | 0,26 |
| Qui-quadrado | V de Cramér | 0,07 | 0,21 | 0,35 |

**Importante**: Os benchmarks são diretrizes. O contexto importa!

### Calculando Tamanhos de Efeito

A maioria dos tamanhos de efeito são calculados automaticamente por pingouin:

```python
# Teste t retorna d de Cohen
result = pg.ttest(x, y)
d = result['cohen-d'].values[0]

# ANOVA retorna eta-quadrado parcial
aov = pg.anova(dv='score', between='group', data=df)
eta_p2 = aov['np2'].values[0]

# Correlação: r é já um tamanho de efeito
corr = pg.corr(x, y)
r = corr['r'].values[0]
```

### Intervalos de Confiança para Tamanhos de Efeito

Sempre relatar ICs para mostrar precisão:

```python
from pingouin import compute_effsize_from_t

# Para teste t
d, ci = compute_effsize_from_t(
    t_statistic,
    nx=len(group1),
    ny=len(group2),
    eftype='cohen'
)
print(f"d = {d:.2f}, IC 95% [{ci[0]:.2f}, {ci[1]:.2f}]")
```

---

## Análise de Poder

### Análise de Poder A Priori (Planejamento de Estudo)

Determinar tamanho de amostra necessário antes da coleta de dados:

```python
from statsmodels.stats.power import (
    tt_ind_solve_power,
    FTestAnovaPower
)

# Teste t: Qual n é necessário para detectar d = 0,5?
n_required = tt_ind_solve_power(
    effect_size=0.5,
    alpha=0.05,
    power=0.80,
    ratio=1.0,
    alternative='two-sided'
)
print(f"n necessário por grupo: {n_required:.0f}")

# ANOVA: Qual n é necessário para detectar f = 0,25?
anova_power = FTestAnovaPower()
n_per_group = anova_power.solve_power(
    effect_size=0.25,
    ngroups=3,
    alpha=0.05,
    power=0.80
)
print(f"n necessário por grupo: {n_per_group:.0f}")
```

### Análise de Sensibilidade (Pós-Estudo)

Determinar qual tamanho de efeito você poderia detectar:

```python
# Com n=50 por grupo, qual efeito poderíamos detectar?
detectable_d = tt_ind_solve_power(
    effect_size=None,  # Resolver para isso
    nobs1=50,
    alpha=0.05,
    power=0.80,
    ratio=1.0,
    alternative='two-sided'
)
print(f"Estudo poderia detectar d ≥ {detectable_d:.2f}")
```

**Nota**: Análise de poder pós-hoc (calculando poder depois do estudo) geralmente não é recomendada. Use análise de sensibilidade.

Veja `references/effect_sizes_and_power.md` para orientação detalhada.

---

## Relatando Resultados

### Relatório Estatístico em Estilo APA

Siga as diretrizes em `references/reporting_standards.md`.

### Elementos Essenciais do Relatório

1. **Estatísticas descritivas**: M, DP, n para todos os grupos/variáveis
2. **Estatísticas de teste**: Nome do teste, estatística, gl, valor p exato
3. **Tamanhos de efeito**: Com intervalos de confiança
4. **Verificação de pressupostos**: Quais testes foram feitos, resultados, ações tomadas
5. **Todas as análises planejadas**: Incluindo achados não-significativos

### Exemplos de Templates de Relatório

#### Teste t Independente

```
O Grupo A (n = 48, M = 75,2, DP = 8,5) teve uma pontuação significativamente
mais alta do que o Grupo B (n = 52, M = 68,3, DP = 9,2), t(98) = 3,82, p < ,001,
d = 0,77, IC 95% [0,36, 1,18], bicaudal. Os pressupostos de normalidade
(Shapiro-Wilk: Grupo A W = 0,97, p = ,18; Grupo B W = 0,96, p = ,12) e
homogeneidade de variância (F de Levene (1, 98) = 1,23, p = ,27) foram
satisfeitos.
```

#### ANOVA Unidirecional

```
Uma ANOVA unidirecional revelou um efeito principal significativo da condição
de tratamento na pontuação do teste, F(2, 147) = 8,45, p < ,001, η²_p = ,10.
Comparações pós-hoc usando HSD de Tukey indicaram que a Condição A (M = 78,2,
DP = 7,3) teve uma pontuação significativamente mais alta do que a Condição B
(M = 71,5, DP = 8,1, p = ,002, d = 0,87) e Condição C (M = 70,1, DP = 7,9,
p < ,001, d = 1,07). As Condições B e C não diferiram significativamente
(p = ,52, d = 0,18).
```

#### Regressão Múltipla

```
Regressão linear múltipla foi conduzida para predizer pontuações de exame
a partir de horas de estudo, GPA anterior e frequência. O modelo geral foi
significativo, F(3, 146) = 45,2, p < ,001, R² = ,48, R² ajustado = ,47.
Horas de estudo (B = 1,80, EP = 0,31, β = ,35, t = 5,78, p < ,001,
IC 95% [1,18, 2,42]) e GPA anterior (B = 8,52, EP = 1,95, β = ,28, t = 4,37,
p < ,001, IC 95% [4,66, 12,38]) foram preditores significativos, enquanto
frequência não foi (B = 0,15, EP = 0,12, β = ,08, t = 1,25, p = ,21,
IC 95% [-0,09, 0,39]). Multicolinearidade não foi uma preocupação
(todos VIF < 1,5).
```

#### Análise Bayesiana

```
Um teste t de amostras independentes Bayesiano foi conduzido usando priors
fracamente informativos (Normal(0, 1) para diferença de média). A distribuição
posterior indicou que o Grupo A teve uma pontuação mais alta do que o Grupo B
(M_diff = 6,8, intervalo credível 95% [3,2, 10,4]). O Fator de Bayes
BF₁₀ = 45,3 forneceu evidência muito forte para uma diferença entre grupos,
com probabilidade posterior de 99,8% de que a média do Grupo A excedia a do
Grupo B. Diagnósticos de convergência foram satisfatórios (todos R̂ < 1,01,
ESS > 1000).
```

---

## Estatística Bayesiana

### Quando Usar Métodos Bayesianos

Considere abordagens Bayesianas quando:
- Você tem informação prévia para incorporar
- Você quer afirmações de probabilidade diretas sobre hipóteses
- Tamanho de amostra é pequeno ou planejando coleta de dados sequencial
- Você precisa quantificar evidência para a hipótese nula
- O modelo é complexo (hierárquico, dados faltantes)

Veja `references/bayesian_statistics.md` para orientação abrangente sobre:
- Teorema de Bayes e interpretação
- Especificação de priors (informativos, fracamente informativos, não-informativos)
- Testes de hipótese Bayesianos com Fatores de Bayes
- Intervalos credíveis vs. intervalos de confiança
- Testes t Bayesianos, ANOVA, regressão e modelos hierárquicos
- Verificação de convergência do modelo e verificações preditivas posteriores

### Vantagens Principais

1. **Interpretação intuitiva**: "Dados os dados, há 95% de probabilidade de que o parâmetro esteja neste intervalo"
2. **Evidência para nulo**: Pode quantificar apoio para nenhum efeito
3. **Flexível**: Nenhuma preocupação com p-hacking; pode analisar dados conforme chegam
4. **Quantificação de incerteza**: Distribuição posterior completa

---

## Recursos

Esta habilidade inclui materiais de referência abrangentes:

### Diretório de Referências

- **test_selection_guide.md**: Árvore de decisão para escolher testes estatísticos apropriados
- **assumptions_and_diagnostics.md**: Orientação detalhada sobre verificação e tratamento de violações de pressupostos
- **effect_sizes_and_power.md**: Calculando, interpretando e relatando tamanhos de efeito; conduzindo análises de poder
- **bayesian_statistics.md**: Guia completo para métodos de análise Bayesiana
- **reporting_standards.md**: Diretrizes de relatório em estilo APA com exemplos

### Diretório de Scripts

- **assumption_checks.py**: Verificação automatizada de pressupostos com visualizações
  - `comprehensive_assumption_check()`: Fluxo de trabalho completo
  - `check_normality()`: Teste de normalidade com gráficos Q-Q
  - `check_homogeneity_of_variance()`: Teste de Levene com box plots
  - `check_linearity()`: Verificações de linearidade de regressão
  - `detect_outliers()`: Detecção de outliers com IQR e z-score

---

## Melhores Práticas

1. **Pré-registre análises** quando possível para distinguir confirmação de exploração
2. **Sempre verifique pressupostos** antes de interpretar resultados
3. **Relatar tamanhos de efeito** com intervalos de confiança
4. **Relatar todas as análises planejadas** incluindo resultados não-significativos
5. **Distinguir significância estatística de significância prática**
6. **Visualizar dados** antes e depois da análise
7. **Verificar diagnósticos** para regressão/ANOVA (gráficos de resíduos, VIF, etc.)
8. **Conduzir análises de sensibilidade** para avaliar robustez
9. **Compartilhar dados e código** para reprodutibilidade
10. **Ser transparente** sobre violações, transformações e decisões

---

## Armadilhas Comuns a Evitar

1. **P-hacking**: Não teste múltiplos caminhos até algo ser significativo
2. **HARKing**: Não apresente achados exploratórios como confirmatórios
3. **Ignorar pressupostos**: Verifique-os e relatar violações
4. **Confundir significância com importância**: p < ,05 ≠ efeito significativo
5. **Não relatar tamanhos de efeito**: Essencial para interpretação
6. **Cherry-picking**: Relatar todas as análises planejadas
7. **Interpretar mal valores p**: NÃO são probabilidade de que a hipótese seja verdadeira
8. **Comparações múltiplas**: Corrigir para erro family-wise quando apropriado
9. **Ignorar dados faltantes**: Entender mecanismo (MCAR, MAR, MNAR)
10. **Superinterpretar resultados não-significativos**: Ausência de evidência ≠ evidência de ausência

---

## Checklist de Início

Ao começar uma análise estatística:

- [ ] Definir questão de pesquisa e hipóteses
- [ ] Determinar teste estatístico apropriado (use test_selection_guide.md)
- [ ] Conduzir análise de poder para determinar tamanho de amostra
- [ ] Carregar e inspecionar dados
- [ ] Verificar dados faltantes e outliers
- [ ] Verificar pressupostos usando assumption_checks.py
- [ ] Executar análise primária
- [ ] Calcular tamanhos de efeito com intervalos de confiança
- [ ] Conduzir testes pós-hoc se necessário (com correções)
- [ ] Criar visualizações
- [ ] Escrever resultados seguindo reporting_standards.md
- [ ] Conduzir análises de sensibilidade
- [ ] Compartilhar dados e código

---

## Suporte e Leitura Adicional

Para dúvidas sobre:
- **Seleção de teste**: Veja references/test_selection_guide.md
- **Pressupostos**: Veja references/assumptions_and_diagnostics.md
- **Tamanhos de efeito**: Veja references/effect_sizes_and_power.md
- **Métodos Bayesianos**: Veja references/bayesian_statistics.md
- **Relatório**: Veja references/reporting_standards.md

**Livros-chave**:
- Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences*
- Field, A. (2013). *Discovering Statistics Using IBM SPSS Statistics*
- Gelman, A., & Hill, J. (2006). *Data Analysis Using Regression and Multilevel/Hierarchical Models*
- Kruschke, J. K. (2014). *Doing Bayesian Data Analysis*

**Recursos online**:
- Guia de Estilo APA: https://apastyle.apa.org/
- Consultoria Estatística: Cross Validated (stats.stackexchange.com)