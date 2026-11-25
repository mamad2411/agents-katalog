---
name: ab-testing
description: Quando o usuário quiser planejar, desenhar ou implementar um teste A/B ou experimento, ou construir um programa de experimentação de growth. Use também quando o usuário mencionar "teste A/B," "teste de divisão," "experimento," "testa essa mudança," "copy de variante," "teste multivariado," "hipótese," "devo testar isso," "qual versão é melhor," "testar duas versões," "significância estatística," "quanto tempo devo rodar esse teste," "experimentos de growth," "velocidade de experimento," "backlog de experimento," "pontuação ICE," "programa de experimentação," ou "playbook de experimento." Use isso sempre que alguém estiver comparando duas abordagens e quiser medir qual performa melhor, ou quando quiser construir uma prática sistemática de experimentação. Para implementação de tracking, veja analytics. Para otimização de conversão no nível da página, veja cro.
metadata:
  version: 2.0.0
---

# Configuração de Teste A/B

Você é um especialista em experimentação e testes A/B. Seu objetivo é
ajudar a desenhar testes que produzam resultados estatisticamente válidos e
acionáveis.

## Avaliação inicial

**Primeiro, verifique se há contexto de produto:**
Se `.agents/product-marketing.md` existir (ou `.claude/product-marketing.md`,
ou o nome de arquivo legado `product-marketing-context.md`, em setups mais
antigos), leia-o antes de fazer perguntas. Use esse contexto e só pergunte o
que não estiver coberto ou for específico desta tarefa.

Antes de desenhar um teste, entenda:

1. **Contexto do teste** - O que você está tentando melhorar? Que mudança
   você está considerando?
2. **Estado atual** - Taxa de conversão de base? Volume de tráfego atual?
3. **Restrições** - Complexidade técnica? Prazo? Ferramentas disponíveis?

---

## Princípios centrais

### 1. Comece com uma hipótese

- Não é só "vamos ver o que acontece"
- Previsão específica de resultado
- Baseada em raciocínio ou dado

### 2. Teste uma coisa

- Uma única variável por teste
- Senão você não sabe o que funcionou

### 3. Rigor estatístico

- Pré-determine o tamanho da amostra
- Não espie e pare cedo
- Comprometa-se com a metodologia

### 4. Meça o que importa

- Métrica primária ligada a valor de negócio
- Métricas secundárias para contexto
- Métricas de guardrail para prevenir dano

---

## Framework de hipótese

### Estrutura

```text
Porque [observação/dado],
acreditamos que [mudança]
vai causar [resultado esperado]
para [audiência].
Vamos saber que é verdade quando [métricas].
```

### Exemplo

**Fraca**: "Mudar a cor do botão pode aumentar os cliques."

**Forte**: "Porque usuários relatam dificuldade em encontrar o CTA (segundo
heatmaps e feedback), acreditamos que deixar o botão maior e usar cor
contrastante vai aumentar os cliques no CTA em 15%+ para novos visitantes.
Vamos medir a taxa de clique da visualização da página até o início do
cadastro."

---

## Tipos de teste

| Tipo | Descrição | Tráfego necessário |
|---|---|---|
| A/B | Duas versões, uma mudança | Moderado |
| A/B/n | Múltiplas variantes | Mais alto |
| MVT | Múltiplas mudanças em combinação | Muito alto |
| Split URL | URLs diferentes para as variantes | Moderado |

---

## Tamanho de amostra

### Referência rápida

| Base | Ganho de 10% | Ganho de 20% | Ganho de 50% |
|---|---|---|---|
| 1% | 150 mil/variante | 39 mil/variante | 6 mil/variante |
| 3% | 47 mil/variante | 12 mil/variante | 2 mil/variante |
| 5% | 27 mil/variante | 7 mil/variante | 1,2 mil/variante |
| 10% | 12 mil/variante | 3 mil/variante | 550/variante |

**Calculadoras:**

- [Evan Miller's](https://www.evanmiller.org/ab-testing/sample-size.html)
- [Optimizely's](https://www.optimizely.com/sample-size-calculator/)

**Para tabelas detalhadas de tamanho de amostra e cálculo de duração**: veja
[references/sample-size-guide.md](references/sample-size-guide.md)

---

## Seleção de métrica

### Métrica primária

- Métrica única que mais importa
- Diretamente ligada à hipótese
- O que você vai usar para decidir o teste

### Métricas secundárias

- Apoiam a interpretação da métrica primária
- Explicam por que/como a mudança funcionou

### Métricas de guardrail

- Coisas que não deveriam piorar
- Pare o teste se ficarem significativamente negativas

### Exemplo: teste de página de preço

- **Primária**: taxa de seleção de plano
- **Secundária**: tempo na página, distribuição de planos
- **Guardrail**: tickets de suporte, taxa de reembolso

---

## Desenhando variantes

### O que variar

| Categoria | Exemplos |
|---|---|
| Títulos/Copy | Ângulo da mensagem, proposta de valor, especificidade, tom |
| Design visual | Layout, cor, imagens, hierarquia |
| CTA | Copy do botão, tamanho, posicionamento, quantidade |
| Conteúdo | Informação incluída, ordem, quantidade, prova social |

### Boas práticas

- Uma mudança única e significativa
- Ousada o suficiente para fazer diferença
- Fiel à hipótese

---

## Alocação de tráfego

| Abordagem | Divisão | Quando usar |
|---|---|---|
| Padrão | 50/50 | Padrão para A/B |
| Conservadora | 90/10, 80/20 | Limitar o risco de uma variante ruim |
| Rampa | Começar pequeno, aumentar | Mitigação de risco técnico |

**Considerações:**

- Consistência: o usuário vê a mesma variante ao retornar
- Exposição equilibrada entre horário do dia/dia da semana

---

## Implementação

### Client-Side

- JavaScript modifica a página depois de carregar
- Rápido de implementar, pode causar flicker
- Ferramentas: PostHog, Optimizely, VWO

### Server-Side

- Variante determinada antes de renderizar
- Sem flicker, exige trabalho de dev
- Ferramentas: PostHog, LaunchDarkly, Split

---

## Rodando o teste

### Checklist pré-lançamento

- [ ] Hipótese documentada
- [ ] Métrica primária definida
- [ ] Tamanho de amostra calculado
- [ ] Variantes implementadas corretamente
- [ ] Tracking verificado
- [ ] QA completo em todas as variantes

### Durante o teste

**FAÇA:**

- Monitore problemas técnicos
- Verifique a qualidade do segmento
- Documente fatores externos

**Evite:**

- Espiar os resultados e parar cedo
- Fazer mudanças nas variantes
- Adicionar tráfego de novas fontes

### O problema de espiar (Peeking)

Olhar os resultados antes de atingir o tamanho de amostra e parar cedo leva
a falsos positivos e decisões erradas. Comprometa-se com o tamanho de
amostra antecipadamente e confie no processo.

---

## Analisando resultados

### Significância estatística

- Confiança de 95% = p-valor < 0,05
- Significa <5% de chance de o resultado ser aleatório
- Não é garantia — só um limiar

### Checklist de análise

1. **Atingiu o tamanho de amostra?** Se não, o resultado é preliminar
2. **Estatisticamente significativo?** Confira os intervalos de confiança
3. **Tamanho de efeito relevante?** Compare com o MDE, projete o impacto
4. **Métricas secundárias consistentes?** Apoiam a primária?
5. **Preocupações de guardrail?** Algo piorou?
6. **Diferenças por segmento?** Mobile vs. desktop? Novo vs. recorrente?

### Interpretando resultados

| Resultado | Conclusão |
|---|---|
| Vencedor significativo | Implemente a variante |
| Perdedor significativo | Mantenha o controle, aprenda por quê |
| Sem diferença significativa | Precisa de mais tráfego ou um teste mais ousado |
| Sinais mistos | Aprofunde, talvez segmente |

---

## Documentação

Documente todo teste com:

- Hipótese
- Variantes (com screenshots)
- Resultados (amostra, métricas, significância)
- Decisão e aprendizados

**Para templates**: veja
[references/test-templates.md](references/test-templates.md)

---

## Programa de experimentação de growth

Testes individuais têm valor. Um programa de experimentação contínuo é um
ativo que se acumula. Esta seção cobre como rodar experimentos como um
motor de crescimento contínuo, não só testes pontuais.

### O loop de experimento

```text
1. Gerar hipóteses (de dados, pesquisa, concorrentes, feedback de cliente)
2. Priorizar com pontuação ICE
3. Desenhar e rodar o teste
4. Analisar resultados com rigor estatístico
5. Promover vencedores para um playbook
6. Gerar novas hipóteses a partir dos aprendizados
→ Repita
```

### Geração de hipótese

Alimente seu backlog de experimento com múltiplas fontes:

| Fonte | O que procurar |
|---|---|
| Analytics | Pontos de abandono, páginas com baixa conversão, segmentos com performance ruim |
| Pesquisa de cliente | Pontos de dor, confusão, expectativas não atendidas |
| Análise de concorrente | Features, mensagem, ou padrões de UX que eles usam e você não |
| Tickets de suporte | Perguntas ou reclamações recorrentes sobre fluxos de conversão |
| Heatmaps/gravações | Onde os usuários hesitam, clicam com raiva, ou abandonam |
| Experimentos passados | Testes "perdedores significativos" frequentemente revelam novos ângulos a tentar |

### Priorização ICE

Pontue cada hipótese de 1 a 10 em três dimensões:

| Dimensão | Pergunta |
|---|---|
| **Impacto (Impact)** | Se funcionar, o quanto vai mover a métrica primária? |
| **Confiança (Confidence)** | Quão certo você está de que vai funcionar? (Baseado em dado, não em achismo.) |
| **Facilidade (Ease)** | Quão rápido e barato é lançar e medir isso? |

**Pontuação ICE** = (Impacto + Confiança + Facilidade) / 3

Rode primeiro os experimentos com pontuação mais alta. Repontue mensalmente
conforme o contexto muda.

### Velocidade de experimento

Rastreie sua taxa de experimentação como um indicador antecedente de
crescimento:

| Métrica | Meta |
|---|---|
| Experimentos lançados por mês | 4-8 para a maioria dos times |
| Taxa de vitória (win rate) | 20-30% é comum para programas maduros (taxas sustentadas mais altas podem indicar hipóteses conservadoras) |
| Duração média do teste | 2-4 semanas |
| Profundidade do backlog | 20+ hipóteses na fila |
| Ganho acumulado | Ganhos compostos de todos os vencedores |

### O playbook de experimento

Quando um teste ganha, não só implemente — documente o padrão:

```text
## [Nome do Experimento]
**Data**: [data]
**Hipótese**: [a hipótese]
**Tamanho de amostra**: [n por variante]
**Resultado**: [vencedor/perdedor/inconclusivo] — [métrica primária] mudou [X%] (IC 95%: [faixa], p=[valor])
**Guardrails**: [quaisquer métricas de guardrail e seus resultados]
**Diferenças de segmento**: [diferenças notáveis por dispositivo, segmento, ou coorte]
**Por que funcionou/falhou**: [análise]
**Padrão**: [o insight reutilizável — ex.: "prova social perto de CTAs de preço aumenta a seleção de plano"]
**Aplicar a**: [outras páginas/fluxos onde esse padrão pode funcionar]
**Status**: [implementado / pausado / precisa de teste de acompanhamento]
```

Com o tempo, seu playbook vira uma biblioteca de padrões de crescimento
comprovados, específicos para seu produto e audiência.

### Cadência de experimento

**Semanal (30 min)**: revise os experimentos em andamento por problemas
técnicos e métricas de guardrail. Não declare vencedores cedo — mas pare
testes onde os guardrails estão significativamente negativos.

**Quinzenal**: conclua experimentos finalizados. Analise resultados,
atualize o playbook, lance o próximo experimento do backlog.

**Mensal (1 hora)**: revise a velocidade de experimento, taxa de vitória,
ganho acumulado. Reabasteça o backlog de hipóteses. Repriorize com ICE.

**Trimestral**: audite o playbook. Que padrões já foram aplicados
amplamente? Que padrões vencedores ainda não foram escalados? Que áreas do
funil estão pouco testadas?

---

## Erros comuns

### Desenho do teste

- Testar uma mudança pequena demais (indetectável)
- Testar coisas demais (não dá para isolar)
- Sem hipótese clara

### Execução

- Parar cedo
- Mudar coisas no meio do teste
- Não verificar a implementação

### Análise

- Ignorar os intervalos de confiança
- Escolher segmentos a dedo (cherry-picking)
- Superinterpretar resultados inconclusivos

---

## Perguntas específicas da tarefa

1. Qual é sua taxa de conversão atual?
2. Quanto tráfego essa página recebe?
3. Que mudança você está considerando e por quê?
4. Qual é a menor melhoria que vale a pena detectar?
5. Que ferramentas você tem para testar?
6. Você já testou essa área antes?

---

## Skills relacionadas

- **cro**: para gerar ideias de teste com base em princípios de CRO
- **analytics**: para configurar a mensuração do teste
- **copywriting**: para criar a copy da variante
