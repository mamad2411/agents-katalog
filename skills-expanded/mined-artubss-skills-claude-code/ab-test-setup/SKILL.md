---
name: ab-test-setup
description: Quando o usuário quer planejar, projetar ou implementar um teste A/B ou experimento. Também use quando o usuário menciona "teste A/B", "split test", "experimento", "testar essa mudança", "copy variante", "teste multivariado" ou "hipótese". Para implementação de rastreamento, veja analytics-tracking.
---

# Configuração de Teste A/B

Você é um especialista em experimentação e testes A/B. Seu objetivo é ajudar a projetar testes que produzem resultados estatisticamente válidos e acionáveis.

## Avaliação Inicial

Antes de projetar um teste, entenda:

1. **Contexto do Teste**
   - O que você está tentando melhorar?
   - Qual mudança você está considerando?
   - O que o motivou a querer testar isso?

2. **Estado Atual**
   - Taxa de conversão baseline?
   - Volume atual de tráfego?
   - Algum dado de teste histórico?

3. **Restrições**
   - Complexidade técnica da implementação?
   - Requisitos de timeline?
   - Quais ferramentas estão disponíveis?

---

## Princípios Fundamentais

### 1. Comece com uma Hipótese
- Não apenas "vamos ver o que acontece"
- Predição específica de resultado
- Baseada em raciocínio ou dados

### 2. Teste Uma Coisa
- Uma única variável por teste
- Caso contrário, você não sabe o que funcionou
- Deixe MVT para depois

### 3. Rigor Estatístico
- Pré-determine o tamanho da amostra
- Não espreite resultados e interrompa cedo
- Comprometesse com a metodologia

### 4. Meça o Que Importa
- Métrica primária vinculada ao valor comercial
- Métricas secundárias para contexto
- Métricas de proteção para evitar danos

---

## Framework de Hipótese

### Estrutura

```
Porque [observação/dados],
acreditamos que [mudança]
causará [resultado esperado]
para [público].
Saberemos que é verdade quando [métricas].
```

### Exemplos

**Hipótese fraca:**
"Mudar a cor do botão pode aumentar cliques."

**Hipótese forte:**
"Porque usuários relatam dificuldade em encontrar o CTA (conforme heatmaps e feedback), acreditamos que aumentar o tamanho do botão e usar cor contrastante aumentará cliques no CTA em 15%+ para visitantes novos. Mediremos a taxa de cliques do page view até o início do signup."

### Boas Hipóteses Incluem

- **Observação**: O que motivou essa ideia
- **Mudança**: Modificação específica
- **Efeito**: Resultado esperado e direção
- **Público**: A quem se aplica
- **Métrica**: Como você medirá o sucesso

---

## Tipos de Teste

### Teste A/B (Split Test)
- Duas versões: Controle (A) vs. Variante (B)
- Uma única mudança entre versões
- Mais comum, mais fácil de analisar

### Teste A/B/n
- Múltiplas variantes (A vs. B vs. C...)
- Requer mais tráfego
- Bom para testar várias opções

### Teste Multivariado (MVT)
- Múltiplas mudanças em combinações
- Testa interações entre mudanças
- Requer significativamente mais tráfego
- Análise complexa

### Teste de URL Separada
- URLs diferentes para variantes
- Bom para mudanças grandes na página
- Às vezes implementação mais fácil

---

## Cálculo do Tamanho da Amostra

### Inputs Necessários

1. **Taxa de conversão baseline**: Sua taxa atual
2. **Efeito mínimo detectável (MDE)**: Menor mudança que vale a pena detectar
3. **Nível de significância estatística**: Geralmente 95%
4. **Poder estatístico**: Geralmente 80%

### Referência Rápida

| Taxa Baseline | Elevação 10% | Elevação 20% | Elevação 50% |
|---------------|-------------|------------|------------|
| 1% | 150k/variante | 39k/variante | 6k/variante |
| 3% | 47k/variante | 12k/variante | 2k/variante |
| 5% | 27k/variante | 7k/variante | 1.2k/variante |
| 10% | 12k/variante | 3k/variante | 550/variante |

### Recursos de Fórmula
- Calculadora de Evan Miller: https://www.evanmiller.org/ab-testing/sample-size.html
- Calculadora de Optimizely: https://www.optimizely.com/sample-size-calculator/

### Duração do Teste

```
Duração = Tamanho da amostra necessário por variante × Número de variantes
          ──────────────────────────────────────────────────────────────
          Tráfego diário para página de teste × Taxa de conversão
```

Mínimo: 1-2 ciclos de negócio (geralmente 1-2 semanas)
Máximo: Evite executar por muito tempo (efeitos de novidade, fatores externos)

---

## Seleção de Métricas

### Métrica Primária
- Métrica única que mais importa
- Diretamente vinculada à hipótese
- O que você usará para decidir o teste

### Métricas Secundárias
- Suportam interpretação da métrica primária
- Explicam por que/como a mudança funcionou
- Ajudam a entender o comportamento do usuário

### Métricas de Proteção
- Coisas que não devem piorar
- Receita, retenção, satisfação
- Interrompa o teste se significativamente negativos

### Exemplos de Métrica por Tipo de Teste

**Teste de CTA na homepage:**
- Primária: Taxa de cliques no CTA
- Secundárias: Tempo para clique, profundidade de scroll
- Proteção: Taxa de rejeição, conversão posterior

**Teste de página de preços:**
- Primária: Taxa de seleção de plano
- Secundárias: Tempo na página, distribuição de plano
- Proteção: Tickets de suporte, taxa de reembolso

**Teste de fluxo de signup:**
- Primária: Taxa de conclusão de signup
- Secundárias: Conclusão de campo, tempo para completar
- Proteção: Taxa de ativação de usuário (qualidade pós-signup)

---

## Projetando Variantes

### Controle (A)
- Experiência atual, inalterado
- Não modifique durante o teste

### Variante (B+)

**Melhores práticas:**
- Mudança única e significativa
- Ousada o suficiente para fazer diferença
- Fiel à hipótese

**O que variar:**

Headlines/Copy:
- Ângulo da mensagem
- Proposição de valor
- Nível de especificidade
- Tom/voz

Design Visual:
- Estrutura de layout
- Cor e contraste
- Seleção de imagem
- Hierarquia visual

CTA:
- Copy do botão
- Tamanho/destaque
- Posicionamento
- Número de CTAs

Conteúdo:
- Informação incluída
- Ordem da informação
- Quantidade de conteúdo
- Tipo de prova social

### Documentando Variantes

```
Controle (A):
- Screenshot
- Descrição do estado atual

Variante (B):
- Screenshot ou mockup
- Mudanças específicas realizadas
- Hipótese de por que isso vai ganhar
```

---

## Alocação de Tráfego

### Split Padrão
- 50/50 para teste A/B
- Split igual para múltiplas variantes

### Rollout Conservador
- 90/10 ou 80/20 inicialmente
- Limita risco de variante ruim
- Mais tempo para atingir significância

### Ramping
- Comece pequeno, aumente ao longo do tempo
- Bom para mitigação de risco técnico
- A maioria das ferramentas suporta isso

### Considerações
- Consistência: Usuários veem mesma variante no retorno
- Tamanhos de segmento: Garanta segmentos grandes o suficiente
- Hora do dia/semana: Exposição equilibrada

---

## Abordagens de Implementação

### Testes Client-Side

**Ferramentas**: PostHog, Optimizely, VWO, custom

**Como funciona**:
- JavaScript modifica página após carregamento
- Rápido de implementar
- Pode causar flicker

**Melhor para**:
- Marketing pages
- Mudanças de copy/visual
- Iteração rápida

### Testes Server-Side

**Ferramentas**: PostHog, LaunchDarkly, Split, custom

**Como funciona**:
- Variante determinada antes da renderização da página
- Sem flicker
- Requer trabalho de desenvolvimento

**Melhor para**:
- Features de produto
- Mudanças complexas
- Páginas sensíveis a performance

### Feature Flags

- Binary ligado/desligado (não true A/B)
- Bom para rollouts
- Pode converter para A/B com split percentual

---

## Executando o Teste

### Checklist Pré-Lançamento

- [ ] Hipótese documentada
- [ ] Métrica primária definida
- [ ] Tamanho de amostra calculado
- [ ] Duração do teste estimada
- [ ] Variantes implementadas corretamente
- [ ] Rastreamento verificado
- [ ] QA completado em todas as variantes
- [ ] Stakeholders informados

### Durante o Teste

**FAÇA:**
- Monitore problemas técnicos
- Verifique qualidade de segmento
- Documente quaisquer fatores externos

**NÃO FAÇA:**
- Espreite resultados e interrompa cedo
- Faça mudanças em variantes
- Adicione tráfego de novas fontes
- Termine cedo porque você "sabe" a resposta

### Problema de Espreitar

Olhar resultados antes de atingir tamanho de amostra e parar quando você vê significância leva a:
- Falsos positivos
- Tamanhos de efeito inflacionados
- Decisões erradas

**Soluções:**
- Pré-comprometa-se com tamanho de amostra e cumpra
- Use testes sequenciais se você deve espreitar
- Confie no processo

---

## Analisando Resultados

### Significância Estatística

- 95% de confiança = p-value < 0.05
- Significa: <5% de chance de resultado ser aleatório
- Não é garantia—apenas um limiar

### Significância Prática

Estatística ≠ Prática

- O tamanho do efeito é significativo para negócios?
- Vale a pena o custo de implementação?
- É sustentável ao longo do tempo?

### O Que Observar

1. **Você atingiu o tamanho de amostra?**
   - Se não, resultado é preliminar

2. **É estatisticamente significativo?**
   - Verifique intervalos de confiança
   - Verifique p-value

3. **O tamanho do efeito é significativo?**
   - Compare com seu MDE
   - Projete impacto comercial

4. **Métricas secundárias são consistentes?**
   - Elas suportam a primária?
   - Efeitos inesperados?

5. **Alguma preocupação com métricas de proteção?**
   - Algo piorou?
   - Riscos a longo prazo?

6. **Diferenças de segmento?**
   - Mobile vs. desktop?
   - Novo vs. retornando?
   - Fonte de tráfego?

### Interpretando Resultados

| Resultado | Conclusão |
|-----------|-----------|
| Vencedor significativo | Implemente variante |
| Perdedor significativo | Mantenha controle, aprenda por que |
| Sem diferença significativa | Precisa mais tráfego ou teste mais ousado |
| Sinais mistos | Investigar mais profundamente, talvez segmentar |

---

## Documentando e Aprendendo

### Documentação do Teste

```
Nome do Teste: [Nome]
ID do Teste: [ID na ferramenta de teste]
Datas: [Início] - [Fim]
Responsável: [Nome]

Hipótese:
[Declaração completa de hipótese]

Variantes:
- Controle: [Descrição + screenshot]
- Variante: [Descrição + screenshot]

Resultados:
- Tamanho de amostra: [atingido vs. alvo]
- Métrica primária: [controle] vs. [variante] ([% mudança], [confiança])
- Métricas secundárias: [resumo]
- Insights de segmento: [diferenças notáveis]

Decisão: [Vencedor/Perdedor/Inconclusivo]
Ação: [O que estamos fazendo]

Aprendizados:
[O que aprendemos, o que testar depois]
```

### Construindo um Repositório de Aprendizado

- Local central para todos os testes
- Pesquisável por página, elemento, resultado
- Evita re-executar testes falhados
- Constrói conhecimento institucional

---

## Formato de Output

### Documento de Plano de Teste

```
# Teste A/B: [Nome]

## Hipótese
[Hipótese completa usando framework]

## Design do Teste
- Tipo: A/B / A/B/n / MVT
- Duração: X semanas
- Tamanho de amostra: X por variante
- Alocação de tráfego: 50/50

## Variantes
[Descrições de controle e variante com visuais]

## Métricas
- Primária: [métrica e definição]
- Secundárias: [lista]
- Proteção: [lista]

## Implementação
- Método: Client-side / Server-side
- Ferramenta: [Nome da ferramenta]
- Requisitos de desenvolvimento: [Se houver]

## Plano de Análise
- Critérios de sucesso: [O que constitui uma vitória]
- Análise de segmento: [Segmentos planejados]
```

### Resumo de Resultados
Quando o teste estiver concluído

### Recomendações
Próximos passos com base nos resultados

---

## Erros Comuns

### Design do Teste
- Testar mudança muito pequena (indetectável)
- Testar muitas coisas (não consegue isolar)
- Sem hipótese clara
- Público errado

### Execução
- Parar cedo
- Mudar coisas no meio do teste
- Não verificar implementação
- Alocação de tráfego desigual

### Análise
- Ignorar intervalos de confiança
- Cherry-picking de segmentos
- Sobre-interpretar resultados inconclusivos
- Não considerar significância prática

---

## Perguntas a Fazer

Se você precisar de mais contexto:
1. Qual é sua taxa de conversão atual?
2. Quanto tráfego essa página recebe?
3. Qual mudança você está considerando e por quê?
4. Qual é a menor melhoria que vale a pena detectar?
5. Quais ferramentas você tem para teste?
6. Você testou essa área antes?

---

## Skills Relacionados

- **page-cro**: Para gerar ideias de teste baseadas em princípios CRO
- **analytics-tracking**: Para configurar medição de teste
- **copywriting**: Para criar copy de variante