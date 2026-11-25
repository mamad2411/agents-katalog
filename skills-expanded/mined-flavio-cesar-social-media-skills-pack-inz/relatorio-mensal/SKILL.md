---
name: relatorio-mensal
description: "Cria relatórios mensais de performance em redes sociais — análise de métricas, comparação com período anterior, insights acionáveis e recomendações estratégicas. Use quando pedirem relatório mensal, relatório de performance, análise de resultados do mês, report de redes sociais, ou qualquer avaliação periódica de performance em social media."
---

# Relatório Mensal de Performance

Skill para criar relatórios mensais completos com análise de métricas, insights e recomendações.

## O que esta skill entrega

1. Dashboard HTML interativo (usando skill `dashboard-metricas`)
2. Análise de métricas-chave com comparação mês anterior
3. Ranking de melhores e piores conteúdos
4. Insights acionáveis baseados em dados
5. Recomendações para o próximo mês
6. Plano de ação concreto

## Métricas a Analisar

### Crescimento
- Seguidores (início vs fim do mês, % variação)
- Alcance total (contas alcançadas)
- Impressões
- Visitas ao perfil
- Cliques no link

### Engajamento
- Taxa de engajamento (interações / alcance × 100)
- Curtidas totais e média por post
- Comentários totais e média
- Salvamentos (indicador mais forte)
- Compartilhamentos
- Respostas em stories

### Conteúdo
- Quantidade de posts por formato
- Top 5 posts por alcance
- Top 5 posts por engajamento
- Bottom 5 posts
- Melhores dias e horários

### Conversão
- Cliques no link da bio
- Leads captados
- Vendas atribuídas (se rastreável)

## Estrutura do Relatório

```
📊 RELATÓRIO DE PERFORMANCE — [MÊS/ANO]
@perfil | Plataforma(s)

━━━━━━━━━━━━━━━━━━━━━━━

📈 RESUMO EXECUTIVO
[3-5 linhas com os destaques do mês]

━━━━━━━━━━━━━━━━━━━━━━━

📊 MÉTRICAS-CHAVE (comparação com mês anterior)
- Seguidores: [X] ([+/-Y%])
- Alcance: [X] ([+/-Y%])
- Engajamento: [X%] ([+/-Y%])
- Salvamentos: [X] ([+/-Y%])
- Cliques: [X] ([+/-Y%])

━━━━━━━━━━━━━━━━━━━━━━━

🏆 TOP 5 CONTEÚDOS
#1 [descrição] — [métrica destaque]
#2 [descrição] — [métrica destaque]
...

━━━━━━━━━━━━━━━━━━━━━━━

📉 BOTTOM 5 (o que não funcionou)
#1 [descrição] — [provável razão]
...

━━━━━━━━━━━━━━━━━━━━━━━

💡 INSIGHTS DO MÊS
1. [insight com dados]
2. [insight com dados]
3. [insight com dados]

━━━━━━━━━━━━━━━━━━━━━━━

🎯 RECOMENDAÇÕES PARA O PRÓXIMO MÊS
1. [ação + justificativa baseada em dados]
2. [ação + justificativa]
3. [ação + justificativa]

━━━━━━━━━━━━━━━━━━━━━━━

📋 PLANO DE AÇÃO
- [ ] [ação 1]
- [ ] [ação 2]
- [ ] [ação 3]
- [ ] [ação 4]
- [ ] [ação 5]
```

## Integração com Dashboard

Se o usuário fornecer dados suficientes, gerar dashboard HTML interativo usando a skill `dashboard-metricas` com gráficos Chart.js, KPIs animados e tabelas ranqueadas.

## Checklist de qualidade

- [ ] Tem comparação com período anterior?
- [ ] Os insights são baseados em dados (não achismos)?
- [ ] As recomendações são acionáveis e específicas?
- [ ] O plano de ação tem prazos realistas?
- [ ] Os melhores e piores conteúdos estão ranqueados?
- [ ] O resumo executivo é objetivo e direto?
