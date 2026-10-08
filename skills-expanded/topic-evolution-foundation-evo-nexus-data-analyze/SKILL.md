---
name: data-analyze
description: Responde perguntas sobre dados do workspace — de consultas rápidas a análises completas e relatórios formais. Use quando precisar buscar uma métrica específica (ex: MRR no Stripe, instâncias ativas no Licensing), investigar o que está causando uma variação de tendência, comparar segmentos ao longo do tempo, ou preparar um relatório de dados para stakeholders. Fontes disponíveis: Stripe (`int-stripe`), Omie (`int-omie`), Licensing (`int-licensing`), Evo CRM (`int-evo-crm`), Linear (`int-linear-review`).
argument-hint: "<pergunta em linguagem natural>"
---

# data-analyze — Responder Perguntas de Dados

Responde uma pergunta de dados, desde uma busca rápida até uma análise completa ou relatório formal.

## Uso

```
/data-analyze <pergunta em linguagem natural>
```

## Fluxo de Trabalho

### 1. Entender a Pergunta

Analisar a pergunta do usuário e determinar:

- **Nível de complexidade**:
  - **Resposta rápida**: Métrica única, filtro simples, busca factual (ex: "Quantos novos clientes assinaram no mês passado?")
  - **Análise completa**: Exploração multidimensional, análise de tendência, comparação (ex: "O que está causando a queda na taxa de conversão?")
  - **Relatório formal**: Investigação abrangente com metodologia, ressalvas e recomendações (ex: "Prepare uma revisão trimestral das métricas de assinatura")
- **Requisitos de dados**: Quais fontes, métricas, dimensões e intervalos de tempo são necessários
- **Formato de saída**: Número, tabela, gráfico, narrativa ou combinação

### 2. Coletar Dados

**Fontes de dados disponíveis no workspace:**

| Fonte | Skill | O que contém |
|-------|-------|-------------|
| **Stripe** | `int-stripe` | Cobranças, assinaturas, MRR, churn, clientes |
| **Omie** | `int-omie` | ERP — clientes, NF-e, contas a pagar/receber |
| **Licensing** | `int-licensing` | Instâncias Evolution API, versões, geo, telemetria |
| **Evo CRM** | `int-evo-crm` | Agentes, pipelines, conversas, usuários |
| **Linear** | `int-linear-review` | Issues, sprints, projetos, velocity |

**Se a fonte de dados estiver disponível:**
1. Usar a skill correspondente para buscar os dados
2. Se necessitar de SQL direto (PostgreSQL), escrever e executar a query
3. Se o resultado parecer inesperado, executar verificações de sanidade antes de prosseguir
4. Se a query falhar, depurar e tentar novamente (verificar nomes de colunas, referências de tabelas, sintaxe PostgreSQL)

**Se os dados precisarem ser fornecidos manualmente:**
1. Pedir ao usuário que forneça os dados de uma destas formas:
   - Colar resultados de query diretamente
   - Fazer upload de arquivo CSV ou Excel
   - Descrever o schema para que possamos escrever queries para ele executar
2. Após os dados serem fornecidos, prosseguir com a análise

### 3. Analisar

- Calcular métricas relevantes, agregações e comparações
- Identificar padrões, tendências, outliers e anomalias
- Comparar entre dimensões (períodos, segmentos, categorias)
- Para análises complexas, decompor o problema em sub-questões e abordar cada uma

### 4. Validar Antes de Apresentar

Antes de compartilhar resultados, executar verificações de validação:

- **Sanidade de contagem de linhas**: O número de registros faz sentido?
- **Verificação de nulos**: Existem nulos inesperados que poderiam distorcer resultados?
- **Verificação de magnitude**: Os números estão em um intervalo razoável?
- **Continuidade de tendência**: Séries temporais têm lacunas inesperadas?
- **Lógica de agregação**: Os subtotais somam corretamente aos totais?
- **Cruzamento com fontes conhecidas**: O MRR calculado bate com o painel do Stripe? As instâncias coincidem com o Licensing?

Se qualquer verificação levantar preocupações, investigar e registrar ressalvas.

### 5. Apresentar Resultados

**Para respostas rápidas:**
- Enunciar a resposta diretamente com contexto relevante
- Incluir a query ou chamada de API usada (em bloco de código) para reprodutibilidade

**Para análises completas:**
- Iniciar com o principal achado ou insight
- Suportar com tabelas de dados e/ou visualizações
- Anotar metodologia e quaisquer ressalvas
- Sugerir perguntas de acompanhamento

**Para relatórios formais:**
- Sumário executivo com principais conclusões
- Seção de metodologia explicando abordagem e fontes de dados
- Achados detalhados com evidências de suporte
- Ressalvas, limitações e notas de qualidade de dados
- Recomendações e próximos passos sugeridos

### 6. Visualizar Quando Útil

Quando um gráfico comunicaria resultados mais efetivamente do que uma tabela:

- Usar a skill `data-create-viz` para selecionar o tipo de gráfico correto
- Gerar visualização Python ou incorporar em dashboard HTML com tema Evolution
- Seguir boas práticas de visualização para clareza e precisão

## Exemplos

**Resposta rápida:**
```
/data-analyze Quantos novos clientes assinaram em março?
```

**Análise completa:**
```
/data-analyze O que está causando o aumento no volume de instâncias Evolution nos últimos 3 meses? Quebrar por versão e país.
```

**Relatório formal:**
```
/data-analyze Prepare uma análise de qualidade de dados da tabela de clientes do Evo CRM — completude, consistência e quaisquer problemas que devemos resolver.
```

## Dicas

- Seja específico sobre intervalos de tempo, segmentos ou métricas quando possível
- Se souber os nomes das tabelas ou campos da API, mencione-os para acelerar o processo
- Para perguntas complexas, a análise pode ser dividida em múltiplas queries ou chamadas de API
- Os resultados são sempre validados antes da apresentação — se algo parecer errado, será sinalizado
- Sempre especificar o fuso horário BRT (UTC-3) ao analisar datas e timestamps
