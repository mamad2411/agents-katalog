---
name: data-validate
description: Valida uma análise antes de compartilhar — metodologia, precisão e verificações de viés. Use quando revisar uma análise antes de uma apresentação para stakeholders, verificar cálculos e lógica de agregação, conferir se os resultados de uma query SQL parecem corretos, ou avaliar se as conclusões são de fato suportadas pelos dados. Sempre rodar esta skill antes de compartilhar análises baseadas em Stripe, Omie, Licensing ou Evo CRM.
argument-hint: "<análise para revisar>"
---

# data-validate — Validar Análise Antes de Compartilhar

Revisar uma análise quanto à precisão, metodologia e possíveis vieses antes de compartilhar com stakeholders. Gera uma avaliação de confiança e sugestões de melhoria.

## Uso

```
/data-validate <análise para revisar>
```

A análise pode ser:
- Um documento ou relatório na conversa
- Um arquivo (markdown, notebook, planilha)
- Queries SQL e seus resultados
- Gráficos e seus dados subjacentes
- Uma descrição de metodologia e achados

## Fluxo de Trabalho

### 1. Revisar Metodologia e Premissas

Examinar:

- **Formulação da questão**: A análise está respondendo à pergunta certa? A questão pode ser interpretada de forma diferente?
- **Seleção de dados**: As tabelas/datasets corretos estão sendo usados? O intervalo de tempo é apropriado?
- **Definição de população**: A população da análise está corretamente definida? Há exclusões não intencionais?
- **Definições de métricas**: As métricas são definidas de forma clara e consistente? Correspondem a como os stakeholders as entendem?
- **Baseline e comparação**: A comparação é justa? Períodos de tempo, tamanhos de cohort e contextos são comparáveis?

### 2. Executar o Checklist de QA Pré-Entrega

Percorrer o checklist abaixo — qualidade dos dados, cálculo, razoabilidade e verificações de apresentação.

### 3. Verificar Armadilhas Analíticas Comuns

Revisar sistematicamente contra o catálogo detalhado de armadilhas abaixo (join explosivo, viés de sobrevivência, comparação de período incompleto, denominador variável, média de médias, desalinhamento de fuso horário, viés de seleção).

### 4. Verificar Cálculos e Agregações

Onde possível, fazer spot-checks:

- Recalcular alguns números-chave de forma independente
- Verificar se os subtotais somam corretamente aos totais
- Confirmar que os percentuais somam a ~100% onde esperado
- Validar que comparações AaA/MaM usam os períodos base corretos
- Verificar se os filtros são aplicados de forma consistente em todas as métricas

Aplicar as técnicas de verificação de sanidade de resultados abaixo.

### 5. Avaliar Visualizações

Se a análise inclui gráficos:

- Os eixos começam em valores apropriados (zero para gráficos de barras)?
- As escalas são consistentes entre gráficos de comparação?
- Os títulos dos gráficos descrevem com precisão o que é mostrado?
- A visualização poderia enganar um leitor rápido?
- Há eixos truncados, intervalos inconsistentes, ou efeitos 3D que distorcem a percepção?

### 6. Avaliar Narrativa e Conclusões

Revisar se:

- As conclusões são suportadas pelos dados mostrados
- Explicações alternativas são reconhecidas
- A incerteza é comunicada adequadamente
- As recomendações seguem logicamente dos achados
- O nível de confiança corresponde à força das evidências

### 7. Sugerir Melhorias

Fornecer sugestões específicas e acionáveis:

- Análises adicionais que fortaleceriam as conclusões
- Ressalvas ou limitações que devem ser anotadas
- Melhores visualizações ou enquadramentos para pontos-chave
- Contexto ausente que os stakeholders iriam querer

### 8. Gerar Avaliação de Confiança

Classificar a análise em uma escala de 3 níveis:

**Pronta para compartilhar** — A análise é metodologicamente sólida, cálculos verificados, ressalvas anotadas. Sugestões menores de melhoria mas nada bloqueando.

**Compartilhar com ressalvas anotadas** — A análise é majoritariamente correta mas tem limitações ou premissas específicas que devem ser comunicadas aos stakeholders. Listar as ressalvas obrigatórias.

**Precisa de revisão** — Encontrou erros específicos, problemas metodológicos, ou análises faltantes que devem ser abordados antes de compartilhar. Listar as mudanças necessárias com ordem de prioridade.

## Formato de Saída

```
## Relatório de Validação

### Avaliação Geral: [Pronta para compartilhar | Compartilhar com ressalvas | Precisa de revisão]

### Revisão de Metodologia
[Achados sobre abordagem, seleção de dados, definições]

### Problemas Encontrados
1. [Severidade: Alta/Média/Baixa] [Descrição do problema e impacto]
2. ...

### Spot-Checks de Cálculo
- [Métrica]: [Verificado / Discrepância encontrada]
- ...

### Revisão de Visualização
[Quaisquer problemas com gráficos ou apresentação visual]

### Melhorias Sugeridas
1. [Melhoria e por que é importante]
2. ...

### Ressalvas Obrigatórias para Stakeholders
- [Ressalva que deve ser comunicada]
- ...
```

---

## Checklist de QA Pré-Entrega

Percorrer este checklist antes de compartilhar qualquer análise com stakeholders.

### Verificações de Qualidade dos Dados

- [ ] **Verificação de fonte**: Confirmado quais tabelas/fontes de dados foram usadas. São as corretas para esta pergunta?
- [ ] **Atualidade**: Os dados são atuais o suficiente para a análise. A data "referente a" foi anotada.
- [ ] **Completude**: Sem lacunas inesperadas em séries temporais ou segmentos faltantes.
- [ ] **Tratamento de nulos**: Taxas de nulo verificadas em colunas-chave. Nulos são tratados adequadamente (excluídos, imputados ou sinalizados).
- [ ] **Deduplicação**: Confirmado que não há dupla contagem por joins ruins ou registros fonte duplicados.
- [ ] **Verificação de filtros**: Todas as cláusulas WHERE e filtros estão corretos. Sem exclusões não intencionais.
- [ ] **Fuso horário**: Timestamps estão alinhados (UTC no banco → BRT na exibição). Conversão aplicada corretamente.

### Verificações de Cálculo

- [ ] **Lógica de agregação**: GROUP BY inclui todas as colunas não-agregadas. Nível de agregação corresponde ao grain da análise.
- [ ] **Corretude do denominador**: Cálculos de taxa e percentual usam o denominador correto. Os denominadores são não-zero.
- [ ] **Alinhamento de datas**: As comparações usam o mesmo comprimento de período de tempo. Períodos parciais são excluídos ou anotados.
- [ ] **Corretude de joins**: Os tipos de JOIN são apropriados (INNER vs LEFT). Joins many-to-many não inflaram contagens.
- [ ] **Definições de métricas**: As métricas correspondem a como os stakeholders as definem. Quaisquer desvios são anotados.
- [ ] **Subtotais somam**: As partes somam ao todo onde esperado. Se não somam, explicar por quê (ex: sobreposição).

### Verificações de Razoabilidade

- [ ] **Magnitude**: Os números estão em um intervalo plausível. A receita não é negativa. Os percentuais estão entre 0-100%.
- [ ] **Continuidade de tendência**: Sem saltos ou quedas inexplicados em séries temporais.
- [ ] **Referência cruzada**: Os números-chave correspondem a outras fontes conhecidas (dashboards Stripe, relatórios do Omie, figuras anteriores).
- [ ] **Ordem de magnitude**: O MRR total está na ordem de grandeza certa. As contagens de instâncias correspondem às figuras conhecidas do Licensing.
- [ ] **Casos extremos**: O que acontece nos limites? Segmentos vazios, períodos sem atividade, novas entidades.

### Verificações de Apresentação

- [ ] **Precisão dos gráficos**: Gráficos de barras começam em zero. Os eixos são rotulados. As escalas são consistentes entre painéis.
- [ ] **Formatação de números**: Precisão apropriada. Formatação consistente de moeda (R$ para BRL, $ para USD). Separadores de milhares onde necessário.
- [ ] **Clareza dos títulos**: Títulos enunciam o insight, não apenas a métrica. Intervalos de datas são especificados.
- [ ] **Transparência de ressalvas**: Limitações e premissas conhecidas são declaradas explicitamente.
- [ ] **Reprodutibilidade**: Outra pessoa poderia recriar esta análise a partir da documentação fornecida.

## Armadilhas Comuns de Análise de Dados

### Join Explosivo

**O problema**: Um join many-to-many silenciosamente multiplica linhas, inflando contagens e somas.

**Como detectar**:
```sql
-- Verificar contagem de linhas antes e depois do join
SELECT COUNT(*) FROM instancias;  -- 1.000
SELECT COUNT(*) FROM instancias i JOIN eventos e ON i.id = e.instancia_id;  -- 3.500 (problemático!)

-- Sempre usar DISTINCT para contar entidades através de joins
SELECT COUNT(DISTINCT i.id) FROM instancias i JOIN eventos e ON i.id = e.instancia_id;
```

**Como prevenir**:
- Sempre verificar contagens de linhas após joins
- Se as contagens aumentam, investigar o relacionamento do join (é realmente 1:1 ou 1:N?)
- Usar `COUNT(DISTINCT id_entidade)` em vez de `COUNT(*)` ao contar entidades através de joins

### Viés de Sobrevivência

**O problema**: Analisar apenas entidades que existem hoje, ignorando as que foram deletadas, fizeram churn, ou falharam.

**Exemplos para o workspace**:
- Analisar comportamento de usuários "ativos" ignora os que cancelaram
- Ver "instâncias usando nossa plataforma" ignora as que avaliaram e saíram
- Estudar propriedades de outcomes "bem-sucedidos" sem os "malsucedidos"

**Como prevenir**: Perguntar "Quem NÃO está neste dataset?" antes de tirar conclusões.

### Comparação de Período Incompleto

**O problema**: Comparar um período parcial com um período completo.

**Exemplos**:
- "MRR de janeiro é R$ 500K vs. dezembro R$ 800K" — mas janeiro não terminou ainda
- "Novas instâncias desta semana estão abaixo" — verificado na quarta-feira, comparando com uma semana anterior completa

**Como prevenir**: Sempre filtrar para períodos completos, ou comparar mesmo-dia-do-mês / mesmo-número-de-dias.

### Denominador Variável

**O problema**: O denominador muda entre períodos, tornando as taxas incomparáveis.

**Exemplos**:
- Taxa de conversão melhora porque mudou como contar usuários "elegíveis"
- Taxa de churn muda porque a definição de "ativo" foi atualizada

**Como prevenir**: Usar definições consistentes em todos os períodos comparados. Anotar quaisquer mudanças de definição.

### Média de Médias

**O problema**: Fazer a média de médias pré-calculadas dá resultados errados quando os tamanhos dos grupos diferem.

**Exemplo**:
- Plano Pro: 100 clientes, MRR médio R$ 200
- Plano Enterprise: 10 clientes, MRR médio R$ 1.000
- Errado: Média das médias = (R$ 200 + R$ 1.000) / 2 = R$ 600
- Correto: Média ponderada = (100×R$ 200 + 10×R$ 1.000) / 110 = R$ 272,73

**Como prevenir**: Sempre agregar a partir dos dados brutos. Nunca fazer média de médias pré-agregadas.

### Desalinhamento de Fuso Horário

**O problema**: Diferentes fontes de dados usam fusos horários diferentes, causando desalinhamento.

**Exemplos no workspace**:
- Timestamps de eventos em UTC vs. datas na exibição em BRT
- Rollups diários que usam diferentes horários de corte
- Stripe reporta em UTC; exibição ao Davidson deve ser em BRT

**Como prevenir**: Padronizar todos os timestamps em um único fuso horário (UTC para armazenamento, BRT para exibição). Documentar o fuso horário usado.

```sql
-- Converter UTC para BRT corretamente no PostgreSQL
SELECT
    criado_em AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo' AS criado_em_brt
FROM eventos;

-- Truncar por dia em BRT
DATE_TRUNC('day', criado_em AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo')
```

### Viés de Seleção na Segmentação

**O problema**: Os segmentos são definidos pelo outcome que está sendo medido, criando lógica circular.

**Exemplos**:
- "Usuários que completaram o onboarding têm maior retenção" — obviamente, eles se auto-selecionaram
- "Instâncias power users geram mais tráfego" — elas se tornaram power users POR gerar mais tráfego

**Como prevenir**: Definir segmentos com base em características pré-tratamento, não em outcomes.

### Outras Armadilhas Estatísticas

- **Paradoxo de Simpson**: Tendência se inverte quando dados são agregados vs. segmentados
- **Correlação apresentada como causalidade** sem evidências de suporte
- **Tamanhos de amostra pequenos** levando a conclusões não confiáveis
- **Outliers afetando desproporcionalmente médias** (medianas deveriam ser usadas?)
- **Testes múltiplos / cherry-picking** de resultados significativos
- **Viés de look-ahead**: Usar informações futuras para explicar eventos passados
- **Intervalos de tempo selecionados a dedo** que favorecem uma narrativa particular

## Verificação de Sanidade de Resultados

### Verificações de Magnitude

Para qualquer número-chave na análise, verificar se passa no "teste do olfato":

| Tipo de Métrica | Verificação de Sanidade |
|---|---|
| Contagens de instâncias | Corresponde às figuras conhecidas de MAU do Licensing? |
| MRR | Está na ordem de grandeza certa vs. ARR conhecido do Stripe? |
| Taxas de conversão | Está entre 0% e 100%? Corresponde às figuras do dashboard? |
| Taxas de crescimento | 50%+ MoM de crescimento é realista, ou há um problema de dados? |
| Médias | A média é razoável dado o que se sabe sobre a distribuição? |
| Percentuais | Os percentuais dos segmentos somam a ~100%? |

### Técnicas de Validação Cruzada

1. **Calcular a mesma métrica de duas formas diferentes** e verificar se correspondem
2. **Fazer spot-check em registros individuais** — escolher algumas entidades específicas e rastrear seus dados manualmente
3. **Comparar com benchmarks conhecidos** — comparar com dashboards publicados, relatórios financeiros, ou análises anteriores
4. **Fazer engenharia reversa** — se o MRR total é X, o MRR por cliente multiplicado pelo número de clientes aproxima X?
5. **Verificações de limite** — o que acontece ao filtrar para um único dia, um único cliente, ou uma única categoria? Esses micro-resultados fazem sentido?

### Sinais de Alerta que Merecem Investigação

- Qualquer métrica que mudou mais de 50% período a período sem uma causa óbvia
- Contagens ou somas que são números redondos exatos (sugere um problema de filtro ou valor padrão)
- Taxas exatamente em 0% ou 100% (pode indicar dados incompletos)
- Resultados que confirmam perfeitamente a hipótese (a realidade geralmente é mais bagunçada)
- Valores idênticos entre períodos de tempo ou segmentos (sugere que a query está ignorando uma dimensão)

## Padrões de Documentação para Reprodutibilidade

### Template de Documentação de Análise

Toda análise não trivial deve incluir:

```markdown
## Análise: [Título]

### Pergunta
[A pergunta específica sendo respondida]

### Fontes de Dados
- Fonte: Stripe via `int-stripe` (referente a [data])
- Fonte: Licensing via `int-licensing` (referente a [data])
- Tabela: [schema.nome_da_tabela] (referente a [data])

### Definições
- [Métrica A]: [Exatamente como é calculada]
- [Segmento X]: [Exatamente como a participação é determinada]
- [Período de tempo]: [Data de início] a [data de fim], BRT (UTC-3)

### Metodologia
1. [Passo 1 da abordagem de análise]
2. [Passo 2]
3. [Passo 3]

### Premissas e Limitações
- [Premissa 1 e por que é razoável]
- [Limitação 1 e seu impacto potencial nas conclusões]

### Principais Achados
1. [Achado 1 com evidências de suporte]
2. [Achado 2 com evidências de suporte]

### Queries SQL
[Todas as queries usadas, com comentários]

### Ressalvas
- [Coisas que o leitor deve saber antes de agir com base nisso]
```

### Documentação de Código

Para qualquer código (SQL, Python) que possa ser reutilizado:

```python
"""
Análise: Retenção Mensal por Cohort
Autor: Davidson Gomes
Data: 2026-04-09
Fonte de Dados: tabela de eventos, tabela de clientes
Última Validação: 2026-04-09 — resultados corresponderam ao dashboard dentro de 2%

Propósito:
    Calcular cohorts de retenção mensal de usuários com base na data da primeira assinatura.

Premissas:
    - "Ativo" significa pelo menos um evento no mês
    - Exclui contas de teste/internas (tipo_usuario != 'interno')
    - Usa timestamps UTC, exibição em BRT

Saída:
    Matriz de retenção de cohort com linhas cohort_mes e colunas meses_desde_assinatura.
    Valores são taxas de retenção (0-100%).
"""
```

## Exemplos

```
/data-validate Revisar esta análise trimestral de MRR antes de eu enviar para o conselho: [análise]
```

```
/data-validate Verificar minha análise de churn — estou comparando taxas do Q4 com Q3 mas o Q4 tem uma janela de medição mais curta
```

```
/data-validate Aqui está uma query SQL e seus resultados para nosso funil de conversão do Evo CRM. A lógica parece certa? [query + resultados]
```

## Dicas

- Rodar `/data-validate` antes de qualquer apresentação ou decisão de alto impacto
- Mesmo análises rápidas se beneficiam de uma verificação de sanidade — leva um minuto e pode salvar a credibilidade
- Se a validação encontrar problemas, corrigi-los e re-validar
- Compartilhar o output da validação junto com a análise para construir a confiança dos stakeholders
- Para análises derivadas de múltiplas fontes (ex: Stripe + Omie), prestar atenção especial ao alinhamento de definições entre sistemas
