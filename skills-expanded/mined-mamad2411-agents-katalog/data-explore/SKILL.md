---
name: data-explore
description: Perfila e explora um dataset para entender sua forma, qualidade e padrões. Use ao encontrar uma nova tabela ou arquivo, verificar taxas de nulo e distribuições de colunas, identificar problemas de qualidade como duplicatas ou valores suspeitos, ou decidir quais dimensões e métricas analisar. Funciona com tabelas PostgreSQL do stack Evolution (Evo CRM, Evo AI), dados do Stripe, Omie, Licensing, ou arquivos CSV/Excel carregados.
argument-hint: "<nome da tabela, fonte de dados ou arquivo>"
---

# data-explore — Perfilar e Explorar um Dataset

Gera um perfil de dados abrangente para uma tabela ou arquivo carregado. Entenda a forma, qualidade e padrões dos dados antes de mergulhar na análise.

## Uso

```
/data-explore <nome_da_tabela ou arquivo>
```

## Fluxo de Trabalho

### 1. Acessar os Dados

**Se a fonte de dados estiver disponível via skill ou conexão PostgreSQL:**

1. Resolver o nome da tabela (tratar prefixos de schema, sugerir correspondências se ambíguo)
2. Consultar metadados da tabela: nomes de colunas, tipos, descrições se disponíveis
3. Executar queries de perfilamento contra os dados ao vivo

**Se um arquivo for fornecido (CSV, Excel, Parquet, JSON):**

1. Ler o arquivo e carregar no dataset de trabalho
2. Inferir tipos de colunas a partir dos dados

**Se for uma fonte do workspace (Stripe, Omie, Licensing, Evo CRM):**

1. Usar a skill correspondente (`int-stripe`, `int-omie`, `int-licensing`, `int-evo-crm`)
2. Extrair uma amostra representativa
3. Prosseguir com o perfilamento sobre os dados extraídos

**Se nenhum dado estiver disponível:**

1. Pedir ao usuário que forneça o nome de uma tabela (com fonte conectada) ou faça upload de um arquivo
2. Se descrever um schema de tabela, fornecer orientação sobre quais queries de perfilamento executar

### 2. Entender a Estrutura

Antes de analisar qualquer dado, entender sua estrutura:

**Perguntas a nível de tabela:**
- Quantas linhas e colunas?
- Qual é o grain (uma linha por quê)?
- Qual é a chave primária? É única?
- Quando os dados foram atualizados pela última vez?
- Até quando os dados retroagem?

**Classificação de colunas** — categorizar cada coluna como uma de:
- **Identificador**: Chaves únicas, chaves estrangeiras, IDs de entidade
- **Dimensão**: Atributos categóricos para agrupamento/filtragem (status, tipo, plano, país)
- **Métrica**: Valores quantitativos para medição (receita, contagem, duração, score)
- **Temporal**: Datas e timestamps (criado_em, atualizado_em, data_evento)
- **Texto**: Campos de texto livre (descrição, notas, nome)
- **Booleano**: Flags verdadeiro/falso
- **Estrutural**: JSON, arrays, estruturas aninhadas

### 3. Gerar Perfil de Dados

Executar as seguintes verificações de perfilamento:

**Métricas a nível de tabela:**
- Contagem total de linhas
- Contagem de colunas e breakdown de tipos
- Tamanho aproximado da tabela (se disponível nos metadados)
- Cobertura do intervalo de datas (min/max das colunas de data)

**Todas as colunas:**
- Contagem de nulos e taxa de nulos
- Contagem distinta e razão de cardinalidade (distinto / total)
- Valores mais comuns (top 5-10 com frequências)
- Valores menos comuns (bottom 5 para identificar anomalias)

**Colunas numéricas (métricas):**
```
min, max, média, mediana (p50)
desvio padrão
percentis: p1, p5, p25, p75, p95, p99
contagem de zeros
contagem de negativos (se inesperado)
```

**Colunas string (dimensões, texto):**
```
comprimento mínimo, máximo, médio
contagem de strings vazias
análise de padrão (valores seguem um formato?)
consistência de case (tudo maiúsculo, minúsculo, misto?)
contagem de espaços antes/depois
```

**Colunas de data/timestamp:**
```
data mínima, data máxima
datas nulas
datas futuras (se inesperado)
distribuição por mês/semana
lacunas na série temporal
```

**Colunas booleanas:**
```
contagem de verdadeiro, falso, nulo
taxa de verdadeiro
```

**Apresentar o perfil como uma tabela de resumo limpa**, agrupada por tipo de coluna (dimensões, métricas, datas, IDs).

### 4. Identificar Problemas de Qualidade dos Dados

Aplicar o framework de avaliação de qualidade abaixo. Sinalizar problemas potenciais:

- **Altas taxas de nulo**: Colunas com >5% de nulos (avisar), >20% de nulos (alertar)
- **Surpresas de baixa cardinalidade**: Colunas que deveriam ser de alta cardinalidade mas não são (ex: um `instancia_id` com apenas 50 valores distintos)
- **Surpresas de alta cardinalidade**: Colunas que deveriam ser categóricas mas têm muitos valores distintos
- **Valores suspeitos**: Valores negativos onde apenas positivos são esperados, datas futuras em dados históricos, valores claramente placeholder (ex: "N/A", "TBD", "test", "999999", "0000-00-00")
- **Detecção de duplicatas**: Verificar se há uma chave natural e se ela tem duplicatas
- **Distorção de distribuição**: Distribuições numéricas extremamente distorcidas que podem afetar médias
- **Problemas de encoding**: Case misto em campos categóricos, espaços em branco, formatos inconsistentes

### 5. Descobrir Relacionamentos e Padrões

Após perfilar colunas individuais:

- **Candidatos a chave estrangeira**: Colunas de ID que podem se ligar a outras tabelas
- **Hierarquias**: Colunas que formam caminhos naturais de drill-down (país > estado > cidade)
- **Correlações**: Colunas numéricas que se movem juntas
- **Colunas derivadas**: Colunas que parecem calculadas a partir de outras
- **Colunas redundantes**: Colunas com informações idênticas ou quase idênticas

### 6. Sugerir Dimensões e Métricas Interessantes

Com base no perfil de colunas, recomendar:

- **Melhores colunas de dimensão** para segmentar dados (colunas categóricas com cardinalidade razoável, 3-50 valores)
- **Colunas de métrica-chave** para medição (colunas numéricas com distribuições significativas)
- **Colunas de tempo** adequadas para análise de tendências
- **Agrupamentos naturais** ou hierarquias aparentes nos dados
- **Chaves de join potenciais** para ligar a outras tabelas

### 7. Recomendar Análises de Acompanhamento

Sugerir 3-5 análises específicas que o usuário poderia executar a seguir:

- "Análise de tendência em [métrica] por [coluna_temporal] agrupada por [dimensão]"
- "Aprofundamento de distribuição em [coluna_distorcida] para entender outliers"
- "Investigação de qualidade de dados em [coluna_problemática]"
- "Análise de correlação entre [métrica_a] e [métrica_b]"
- "Análise de cohort usando [coluna_data] e [coluna_status]"

## Formato de Saída

```
## Perfil de Dados: [nome_da_tabela]

### Visão Geral
- Linhas: 2.340.891
- Colunas: 23 (8 dimensões, 6 métricas, 4 datas, 5 IDs)
- Intervalo de datas: 2021-03-15 a 2024-01-22
- Última atualização: 2024-01-22 03:45 BRT

### Detalhes das Colunas
[tabela de resumo]

### Problemas de Qualidade de Dados
[problemas sinalizados com severidade]

### Explorações Recomendadas
[lista numerada de análises de acompanhamento sugeridas]
```

---

## Framework de Avaliação de Qualidade

### Score de Completude

Avaliar cada coluna:
- **Completa** (>99% não-nulo): Verde
- **Majoritariamente completa** (95-99%): Amarelo — investigar os nulos
- **Incompleta** (80-95%): Laranja — entender por que e se importa
- **Esparsa** (<80%): Vermelho — pode não ser utilizável sem imputação

### Verificações de Consistência

Procurar por:
- **Inconsistência de formato de valor**: Mesmo conceito representado diferentemente ("Brasil", "BR", "Brazil", "br")
- **Inconsistência de tipo**: Números armazenados como strings, datas em vários formatos
- **Integridade referencial**: Chaves estrangeiras que não correspondem a nenhum registro pai
- **Violações de regras de negócio**: Quantidades negativas, datas de fim antes de datas de início, percentuais > 100
- **Consistência entre colunas**: Status = "concluído" mas `concluido_em` é nulo

### Indicadores de Precisão

Sinais de alerta que sugerem problemas de precisão:
- **Valores placeholder**: 0, -1, 999999, "N/A", "TBD", "test", "xxx"
- **Valores padrão**: Frequência suspeitosamente alta de um único valor
- **Dados desatualizados**: `atualizado_em` não mostra alterações recentes em um sistema ativo
- **Valores impossíveis**: Idades > 150, datas no futuro distante, durações negativas
- **Viés de números redondos**: Todos os valores terminando em 0 ou 5 (sugere estimativa, não medição)

### Avaliação de Atualidade

- Quando a tabela foi atualizada pela última vez?
- Qual é a frequência esperada de atualização?
- Há uma defasagem entre o tempo do evento e o tempo de carga?
- Existem lacunas na série temporal?

## Técnicas de Descoberta de Padrões

### Análise de Distribuição

Para colunas numéricas, caracterizar a distribuição:
- **Normal**: Média e mediana próximas, formato de sino
- **Assimetria à direita**: Cauda longa de valores altos (comum para receita, duração de sessão)
- **Assimetria à esquerda**: Cauda longa de valores baixos (menos comum)
- **Bimodal**: Dois picos (sugere duas populações distintas)
- **Lei de potência**: Poucos valores muito grandes, muitos pequenos (comum para atividade de usuário)
- **Uniforme**: Frequência aproximadamente igual ao longo do intervalo (frequentemente sintético ou aleatório)

### Padrões Temporais

Para dados de séries temporais, procurar por:
- **Tendência**: Movimento sustentado para cima ou para baixo
- **Sazonalidade**: Padrões repetitivos (semanal, mensal, trimestral, anual)
- **Efeitos de dia da semana**: Diferenças entre dias úteis e fins de semana
- **Efeitos de feriado**: Quedas ou picos em torno de feriados conhecidos (feriados brasileiros)
- **Pontos de mudança**: Mudanças abruptas no nível ou tendência
- **Anomalias**: Pontos de dados individuais que quebram o padrão

### Descoberta de Segmentação

Identificar segmentos naturais por:
- Encontrar colunas categóricas com 3-20 valores distintos
- Comparar distribuições de métricas entre valores de segmento
- Procurar segmentos com comportamento significativamente diferente
- Testar se os segmentos são homogêneos ou contêm sub-segmentos

### Exploração de Correlação

Entre colunas numéricas:
- Calcular matriz de correlação para todos os pares de métricas
- Sinalizar correlações fortes (|r| > 0,7) para investigação
- Nota: Correlação não implica causalidade — sinalizar isso explicitamente
- Verificar relacionamentos não lineares (ex: quadrático, logarítmico)

## Documentação de Schema

### Template de Documentação de Schema

Ao documentar um dataset para uso da equipe:

```markdown
## Tabela: [schema.nome_da_tabela]

**Descrição**: [O que esta tabela representa]
**Grain**: [Uma linha por...]
**Chave Primária**: [coluna(s)]
**Contagem de Linhas**: [aproximada, com data]
**Frequência de Atualização**: [tempo real / hora / dia / semana]
**Responsável**: [equipe ou pessoa]

### Colunas-Chave

| Coluna | Tipo | Descrição | Valores de Exemplo | Notas |
|--------|------|-----------|-------------------|-------|
| instancia_id | UUID | Identificador único da instância | "inst_abc123" | FK para instancias.id |
| versao | STRING | Versão do Evolution API | "2.1.4", "2.2.0" | 50+ valores distintos |
| mrr | DECIMAL | Receita mensal recorrente em USD | 29.99, 149.00 | Nulo para contas free |
| criado_em | TIMESTAMP | Quando o registro foi criado | 2024-01-15 14:23:01 | UTC — converter para BRT na exibição |

### Relacionamentos
- Join com `clientes` por `cliente_id`
- Join com `planos` por `plano_id`
- Pai de `instancia_eventos` (1:N por instancia_id)

### Problemas Conhecidos
- [Listar problemas conhecidos de qualidade de dados]
- [Anotar quaisquer armadilhas para analistas]

### Padrões Comuns de Query
- [Casos de uso típicos para esta tabela]
```

### Queries de Exploração de Schema (PostgreSQL)

```sql
-- Listar todas as tabelas no schema public
SELECT table_name, table_type
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;

-- Detalhes das colunas (PostgreSQL)
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'minha_tabela'
ORDER BY ordinal_position;

-- Tamanhos das tabelas (PostgreSQL)
SELECT relname,
       pg_size_pretty(pg_total_relation_size(relid)) AS tamanho_total
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;

-- Contagens de linhas por tabela
-- Executar por tabela: SELECT COUNT(*) FROM nome_da_tabela

-- Verificar duplicatas em chave primária
SELECT chave_primaria, COUNT(*)
FROM minha_tabela
GROUP BY chave_primaria
HAVING COUNT(*) > 1;

-- Taxas de nulo por coluna (gerar dinamicamente)
SELECT
    COUNT(*) FILTER (WHERE coluna_1 IS NULL) * 100.0 / COUNT(*) AS nulo_pct_col1,
    COUNT(*) FILTER (WHERE coluna_2 IS NULL) * 100.0 / COUNT(*) AS nulo_pct_col2
FROM minha_tabela;
```

## Dicas

- Para tabelas muito grandes (100M+ linhas), queries de perfilamento usam amostragem por padrão — mencionar se precisar de contagens exatas
- Se explorando um dataset pela primeira vez, este comando fornece a visão geral antes de escrever queries específicas
- Os sinalizadores de qualidade são heurísticos — nem todo sinal é um problema real, mas cada um merece uma verificação rápida
- Sempre verificar os dados no contexto: o que faz sentido para Stripe é diferente do que faz sentido para Licensing
