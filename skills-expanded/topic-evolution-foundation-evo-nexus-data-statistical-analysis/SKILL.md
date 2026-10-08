---
name: data-statistical-analysis
description: Aplica métodos estatísticos incluindo estatísticas descritivas, análise de tendências, detecção de outliers e testes de hipótese para dados do workspace. Use quando analisar distribuições de MRR/churn, testar se uma mudança de produto moveu métricas, detectar anomalias em instâncias do Licensing, calcular correlações, ou interpretar resultados estatísticos. Execução local via Python.
argument-hint: "<dados ou questão estatística>"
---

# data-statistical-analysis — Análise Estatística

Estatísticas descritivas, análise de tendências, detecção de outliers, testes de hipótese, e orientação sobre quando ser cauteloso com afirmações estatísticas.

## Metodologia de Estatísticas Descritivas

### Tendência Central

Escolher a medida correta de centro com base nos dados:

| Situação | Usar | Por quê |
|---|---|---|
| Distribuição simétrica, sem outliers | Média | Estimador mais eficiente |
| Distribuição assimétrica | Mediana | Robusta a outliers |
| Dados categóricos ou ordinais | Moda | Única opção para não-numéricos |
| Altamente assimétrico com outliers (ex: MRR por cliente) | Mediana + média | Reportar ambas; a diferença mostra assimetria |

**Sempre reportar média e mediana juntas para métricas de negócio.** Se divergirem significativamente, os dados são assimétricos e a média isolada é enganosa.

### Dispersão e Variabilidade

- **Desvio padrão**: Distância típica dos valores à média. Usar com dados normalmente distribuídos.
- **Intervalo interquartil (IQR)**: Distância do p25 ao p75. Robusto a outliers. Usar com dados assimétricos.
- **Coeficiente de variação (CV)**: DesvioPad / Média. Usar para comparar variabilidade entre métricas com escalas diferentes.
- **Amplitude**: Máximo menos mínimo. Sensível a outliers mas dá uma noção rápida da extensão dos dados.

### Percentis para Contexto de Negócio

Reportar percentis-chave para contar uma história mais rica do que a média isolada:

```
p1:   Fundo 1% (piso / valor mínimo típico)
p5:   Extremo baixo da faixa normal
p25:  Primeiro quartil
p50:  Mediana (cliente típico)
p75:  Terceiro quartil
p90:  Top 10% / clientes power user
p95:  Extremo alto da faixa normal
p99:  Top 1% / clientes extremos
```

**Exemplo de narrativa**: "O MRR mediano por cliente é R$ 420, mas os 10% melhores pagam mais de R$ 2.100/mês, puxando a média para R$ 780."

### Descrever Distribuições

Caracterizar cada distribuição numérica analisada:

- **Forma**: Normal, assimétrica à direita, assimétrica à esquerda, bimodal, uniforme, cauda pesada
- **Centro**: Média e mediana (e a diferença entre elas)
- **Dispersão**: Desvio padrão ou IQR
- **Outliers**: Quantos e quão extremos
- **Limites**: Há um piso natural (zero) ou teto (100%)?

## Análise de Tendências e Previsão

### Identificar Tendências

**Médias móveis** para suavizar ruído:
```python
import pandas as pd

# Média móvel de 7 dias (boa para dados diários com sazonalidade semanal)
df['ma_7d'] = df['metrica'].rolling(window=7, min_periods=1).mean()

# Média móvel de 28 dias (suaviza padrões semanais E mensais)
df['ma_28d'] = df['metrica'].rolling(window=28, min_periods=1).mean()
```

**Comparação período a período**:
- Semana a semana (SaS): Comparar com o mesmo dia da semana passada
- Mês a mês (MaM): Comparar com o mesmo mês anterior
- Ano a ano (AaA): Padrão ouro para negócios sazonais
- Mesmo dia do ano anterior: Comparar dia de calendário específico

**Taxas de crescimento**:
```
Crescimento simples: (atual - anterior) / anterior
CAGR: (final / inicial) ^ (1 / anos) - 1
Crescimento log: ln(atual / anterior) — melhor para séries voláteis
```

### Detecção de Sazonalidade

Verificar padrões periódicos:
1. Plotar a série temporal bruta — inspeção visual primeiro
2. Calcular médias por dia da semana: há um padrão semanal claro?
3. Calcular médias por mês do ano: há um ciclo anual?
4. Ao comparar períodos, sempre usar AaA ou comparações do mesmo período para evitar confundir tendência com sazonalidade
5. Para o mercado brasileiro, verificar efeitos de feriados nacionais e fim de mês de salário

### Previsão (Métodos Simples)

Para analistas de negócio (não cientistas de dados), usar métodos diretos:

- **Previsão ingênua**: Amanhã = hoje. Usar como baseline.
- **Ingênua sazonal**: Amanhã = mesmo dia da semana/ano passada.
- **Tendência linear**: Ajustar uma reta aos dados históricos. Apenas para tendências claramente lineares.
- **Previsão de média móvel**: Usar média histórica como previsão.

**Sempre comunicar incerteza**. Fornecer um intervalo, não uma estimativa pontual:
- "Esperamos 10K–12K novas instâncias no próximo mês com base na tendência de 3 meses"
- NÃO "Teremos exatamente 11.234 novas instâncias no próximo mês"

**Quando escalar para um cientista de dados**: Tendências não lineares, múltiplas sazonalidades, fatores externos (investimento em marketing, eventos como Evolution Summit), ou quando a precisão da previsão importa para alocação de recursos.

## Detecção de Outliers e Anomalias

### Métodos Estatísticos

**Método Z-score** (para dados normalmente distribuídos):
```python
z_scores = (df['valor'] - df['valor'].mean()) / df['valor'].std()
outliers = df[abs(z_scores) > 3]  # Mais de 3 desvios padrão
```

**Método IQR** (robusto a distribuições não-normais):
```python
Q1 = df['valor'].quantile(0.25)
Q3 = df['valor'].quantile(0.75)
IQR = Q3 - Q1
limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR
outliers = df[(df['valor'] < limite_inferior) | (df['valor'] > limite_superior)]
```

**Método percentil** (mais simples):
```python
outliers = df[(df['valor'] < df['valor'].quantile(0.01)) |
              (df['valor'] > df['valor'].quantile(0.99))]
```

### Tratamento de Outliers

NÃO remover outliers automaticamente. Em vez disso:

1. **Investigar**: Isso é um erro de dados, um valor extremo genuíno, ou uma população diferente?
2. **Erros de dados**: Corrigir ou remover (ex: valores negativos de MRR, timestamps no ano 1970)
3. **Extremos genuínos**: Manter mas considerar estatísticas robustas (mediana em vez de média)
4. **Populações diferentes**: Segmentar para análise separada (ex: clientes enterprise vs. SMB)

**Documentar o que foi feito**: "Excluímos 47 registros (0,3%) com valores de transação >R$50K, que representam pedidos bulk enterprise analisados separadamente."

### Detecção de Anomalias em Séries Temporais

Para detectar valores incomuns em uma série temporal:

1. Calcular valor esperado (média móvel ou mesmo período do ano anterior)
2. Calcular desvio do esperado
3. Sinalizar desvios além de um limiar (tipicamente 2-3 desvios padrão dos resíduos)
4. Distinguir entre anomalias pontuais (valor único incomum) e pontos de mudança (mudança sustentada)

**Exemplo prático para o Licensing:**
```python
# Detectar queda anormal de instâncias ativas
df['media_movel'] = df['instancias'].rolling(window=7).mean()
df['desvio'] = df['instancias'].std()
df['z_score'] = (df['instancias'] - df['media_movel']) / df['desvio']
anomalias = df[abs(df['z_score']) > 2.5]
print(f"Anomalias detectadas: {len(anomalias)} dias")
```

## Fundamentos de Teste de Hipótese

### Quando Usar

Usar testes de hipótese quando precisar determinar se uma diferença observada é provavelmente real ou poderia ser devida ao acaso. Cenários comuns:

- Resultados de A/B test: A variante B é realmente melhor do que A?
- Comparação antes/depois: A mudança no produto realmente moveu a métrica?
- Comparação de segmentos: Clientes enterprise realmente têm retenção maior?

### O Framework

1. **Hipótese nula (H0)**: Não há diferença (a suposição padrão)
2. **Hipótese alternativa (H1)**: Há uma diferença
3. **Escolher nível de significância (alfa)**: Tipicamente 0,05 (5% de chance de falso positivo)
4. **Calcular estatística de teste e valor-p**
5. **Interpretar**: Se p < alfa, rejeitar H0 (evidência de diferença real)

### Testes Comuns

| Cenário | Teste | Quando Usar |
|---|---|---|
| Comparar médias de dois grupos | t-test (independente) | Dados normais, dois grupos |
| Comparar proporções de dois grupos | z-test para proporções | Taxas de conversão, resultados binários |
| Comparar medições pareadas | t-test pareado | Antes/depois nas mesmas entidades |
| Comparar médias de 3+ grupos | ANOVA | Múltiplos segmentos ou variantes |
| Dados não-normais, dois grupos | Teste U de Mann-Whitney | Métricas assimétricas, dados ordinais |
| Associação entre categorias | Teste qui-quadrado | Duas variáveis categóricas |

**Código Python para testes comuns:**

```python
from scipy import stats

# t-test independente (ex: MRR médio entre dois planos)
grupo_a = df[df['plano'] == 'Pro']['mrr']
grupo_b = df[df['plano'] == 'Enterprise']['mrr']
t_stat, p_value = stats.ttest_ind(grupo_a, grupo_b)
print(f"t={t_stat:.3f}, p={p_value:.4f}")
print("Diferença estatisticamente significativa" if p_value < 0.05 else "Sem evidência de diferença")

# z-test para proporções (ex: taxa de conversão entre variantes)
from statsmodels.stats.proportion import proportions_ztest
contagens = [conversoes_a, conversoes_b]
nobs = [total_a, total_b]
z_stat, p_value = proportions_ztest(contagens, nobs)

# Teste qui-quadrado (ex: distribuição de planos por país)
contingencia = pd.crosstab(df['pais'], df['plano'])
chi2, p, dof, expected = stats.chi2_contingency(contingencia)
```

### Significância Estatística vs. Prática

**Significância estatística** significa que a diferença provavelmente não é devida ao acaso.

**Significância prática** significa que a diferença é grande o suficiente para importar para decisões de negócio.

Uma diferença pode ser estatisticamente significativa mas praticamente sem sentido (comum com amostras grandes). Sempre reportar:
- **Tamanho do efeito**: Quão grande é a diferença? (ex: "Variante B melhorou a conversão em 0,3 pontos percentuais")
- **Intervalo de confiança**: Qual é o intervalo de efeitos verdadeiros plausíveis?
- **Impacto no negócio**: O que isso se traduz em receita, usuários, ou outros termos de negócio?

### Considerações de Tamanho de Amostra

- Amostras pequenas produzem resultados não confiáveis, mesmo com valores-p significativos
- Regra geral para proporções: Precisa de pelo menos 30 eventos por grupo para confiabilidade básica
- Para detectar efeitos pequenos (ex: mudança de 1% na taxa de conversão), pode ser necessário milhares de observações por grupo
- Se a amostra é pequena, dizer explicitamente: "Com apenas 200 observações por grupo, temos poder limitado para detectar efeitos menores que X%"

```python
# Calcular tamanho de amostra necessário
from statsmodels.stats.power import TTestIndPower

analise = TTestIndPower()
n_necessario = analise.solve_power(
    effect_size=0.2,  # Tamanho do efeito (Cohen's d)
    alpha=0.05,       # Nível de significância
    power=0.8         # Poder desejado (80%)
)
print(f"Tamanho de amostra necessário por grupo: {n_necessario:.0f}")
```

## Quando Ser Cauteloso com Afirmações Estatísticas

### Correlação Não É Causalidade

Ao encontrar uma correlação, explicitamente considerar:
- **Causalidade reversa**: Talvez B cause A, não A cause B
- **Variáveis de confusão**: Talvez C cause tanto A quanto B
- **Coincidência**: Com variáveis suficientes, correlações espúrias são inevitáveis

**O que pode dizer**: "Clientes que usam o Evo CRM há mais de 6 meses têm 30% maior retenção"
**O que não pode dizer sem mais evidências**: "O Evo CRM causa 30% maior retenção"

### Problema de Comparações Múltiplas

Ao testar muitas hipóteses, algumas serão "significativas" por acaso:
- Testar 20 métricas a p=0,05 significa ~1 será falsamente significativa
- Se olhou para muitos segmentos antes de encontrar um diferente, anotar isso
- Ajustar para comparações múltiplas com correção de Bonferroni (dividir alfa pelo número de testes)

```python
# Correção de Bonferroni
n_testes = 10
alfa_corrigido = 0.05 / n_testes
print(f"Alfa corrigido por Bonferroni: {alfa_corrigido:.4f}")
```

### Paradoxo de Simpson

Uma tendência em dados agregados pode se inverter quando segmentada:
- Sempre verificar se a conclusão se mantém em segmentos-chave
- Exemplo: Conversão geral sobe, mas cai em todos os segmentos — porque o mix mudou para um segmento de maior conversão

### Viés de Sobrevivência

Só é possível analisar entidades que "sobreviveram" para estar no dataset:
- Analisar usuários ativos ignora os que fizeram churn
- Analisar instâncias Evolution ativas ignora as que foram canceladas
- Sempre perguntar: "Quem está faltando neste dataset, e sua inclusão mudaria a conclusão?"

### Falácia Ecológica

Tendências agregadas podem não se aplicar a indivíduos:
- "Países com maior penetração do Evolution têm maior crescimento" NÃO significa "clientes individuais com mais instâncias têm maior crescimento"
- Ter cuidado ao aplicar achados a nível de grupo a casos individuais

### Ancoragem em Números Específicos

Cuidado com falsa precisão:
- "O churn será 4,73% no próximo trimestre" implica mais certeza do que é garantida
- Preferir intervalos: "Esperamos churn entre 4–6% com base nos padrões históricos"
- Arredondar adequadamente: "Cerca de 5%" é frequentemente mais honesto que "4,73%"

## Exemplos de Análises Completas

### MRR — Análise Descritiva Completa

```python
import pandas as pd
import numpy as np
from scipy import stats

def analisar_mrr(df_stripe):
    """
    Análise descritiva completa de MRR por cliente.
    Entrada: DataFrame com colunas [cliente_id, mrr_usd, plano, pais]
    """
    mrr = df_stripe['mrr_usd']

    print("=== ANÁLISE DE MRR ===")
    print(f"\nN clientes: {len(mrr):,}")
    print(f"\n--- TENDÊNCIA CENTRAL ---")
    print(f"Média:   ${mrr.mean():,.2f}")
    print(f"Mediana: ${mrr.median():,.2f}")
    print(f"Moda:    ${mrr.mode().iloc[0]:,.2f}")

    print(f"\n--- DISPERSÃO ---")
    print(f"Desvio padrão: ${mrr.std():,.2f}")
    print(f"IQR: ${mrr.quantile(0.75) - mrr.quantile(0.25):,.2f}")
    print(f"CV: {mrr.std()/mrr.mean()*100:.1f}%")

    print(f"\n--- PERCENTIS ---")
    for p in [1, 5, 25, 50, 75, 90, 95, 99]:
        print(f"  p{p:>2}: ${mrr.quantile(p/100):,.2f}")

    print(f"\n--- FORMA DA DISTRIBUIÇÃO ---")
    skewness = stats.skew(mrr)
    kurtosis = stats.kurtosis(mrr)
    print(f"Assimetria: {skewness:.2f} ({'assimétrico à direita' if skewness > 0 else 'assimétrico à esquerda'})")
    print(f"Curtose: {kurtosis:.2f}")

    # Detecção de outliers via IQR
    Q1, Q3 = mrr.quantile(0.25), mrr.quantile(0.75)
    IQR = Q3 - Q1
    outliers = mrr[(mrr < Q1 - 1.5*IQR) | (mrr > Q3 + 1.5*IQR)]
    print(f"\n--- OUTLIERS ---")
    print(f"Detectados: {len(outliers)} ({len(outliers)/len(mrr)*100:.1f}%)")

    return {
        'n': len(mrr), 'media': mrr.mean(), 'mediana': mrr.median(),
        'std': mrr.std(), 'iqr': IQR, 'outliers': len(outliers)
    }
```

### Teste de Hipótese — A/B Test de Feature

```python
def analisar_ab_test(grupo_controle, grupo_variante, metrica='conversao'):
    """
    Análise completa de A/B test.
    Entrada: dois DataFrames com coluna da métrica
    """
    from scipy import stats

    a = grupo_controle[metrica]
    b = grupo_variante[metrica]

    print(f"=== A/B TEST: {metrica.upper()} ===")
    print(f"\nGrupo A (controle): n={len(a):,}, média={a.mean():.4f}")
    print(f"Grupo B (variante): n={len(b):,}, média={b.mean():.4f}")

    # Diferença e tamanho do efeito
    diff = b.mean() - a.mean()
    lift = diff / a.mean() * 100
    cohens_d = diff / np.sqrt((a.std()**2 + b.std()**2) / 2)

    print(f"\n--- IMPACTO ---")
    print(f"Diferença absoluta: {diff:+.4f}")
    print(f"Lift relativo: {lift:+.1f}%")
    print(f"Tamanho do efeito (Cohen's d): {cohens_d:.3f}")

    # Teste estatístico
    t_stat, p_value = stats.ttest_ind(a, b)
    ci = stats.t.interval(0.95, len(a)+len(b)-2,
                          loc=diff,
                          scale=stats.sem(pd.concat([a, b])))

    print(f"\n--- SIGNIFICÂNCIA ESTATÍSTICA ---")
    print(f"t={t_stat:.3f}, p={p_value:.4f}")
    print(f"IC 95%: [{ci[0]:+.4f}, {ci[1]:+.4f}]")
    print(f"Significativo? {'SIM' if p_value < 0.05 else 'NÃO'} (alfa=0.05)")

    if p_value < 0.05:
        print(f"\n✓ A variante B {'melhora' if diff > 0 else 'piora'} {metrica} "
              f"em {abs(lift):.1f}% (estatisticamente significativo)")
    else:
        print(f"\n✗ Sem evidência de diferença estatisticamente significativa")
```
