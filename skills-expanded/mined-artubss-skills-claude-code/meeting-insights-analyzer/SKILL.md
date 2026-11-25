---
name: meeting-insights-analyzer
description: Analisa transcrições e gravações de reuniões para descobrir padrões comportamentais, insights de comunicação e feedback acionável. Identifica quando você evita conflito, usa palavras de preenchimento, domina conversas ou perde oportunidades de ouvir. Perfeito para profissionais que buscam melhorar suas habilidades de comunicação e liderança.
---

# Meeting Insights Analyzer

Esta skill transforma suas transcrições de reuniões em insights acionáveis sobre seus padrões de comunicação, ajudando você a se tornar um comunicador e líder mais eficaz.

## Quando Usar Esta Skill

- Analisar seus padrões de comunicação em múltiplas reuniões
- Obter feedback sobre seu estilo de liderança e facilitação
- Identificar quando você evita conversas difíceis
- Entender seus hábitos de fala e palavras de preenchimento
- Acompanhar melhorias em habilidades de comunicação ao longo do tempo
- Se preparar para avaliações de desempenho com exemplos concretos
- Orientar membros da equipe sobre seu estilo de comunicação

## O que Esta Skill Faz

1. **Reconhecimento de Padrões**: Identifica comportamentos recorrentes em reuniões como:
   - Evitação de conflito ou comunicação indireta
   - Proporções de fala e rodadas de fala
   - Padrões de fazer perguntas versus fazer afirmações
   - Indicadores de escuta ativa
   - Abordagens de tomada de decisão

2. **Análise de Comunicação**: Avalia a eficácia da comunicação:
   - Clareza e diretividade
   - Uso de palavras de preenchimento e linguagem hesitante
   - Padrões de tom e sentimento
   - Controle de reunião e facilitação

3. **Feedback Acionável**: Fornece exemplos específicos com timestamp:
   - O que aconteceu
   - Por que importa
   - Como melhorar

4. **Rastreamento de Tendências**: Compara padrões ao longo do tempo ao analisar múltiplas reuniões

## Como Usar

### Configuração Básica

1. Faça download das transcrições de suas reuniões para uma pasta (ex: `~/meetings/`)
2. Navegue até essa pasta no Claude Code
3. Solicite a análise que você deseja

### Exemplos de Início Rápido

```
Analise todas as reuniões nesta pasta e me diga quando evitei conflito.
```

```
Olhe minhas reuniões do mês passado e identifique meus padrões de comunicação.
```

```
Compare meu estilo de facilitação entre estas duas pastas de reuniões.
```

### Análise Avançada

```
Analise todas as transcrições nesta pasta e:
1. Identifique quando interrompi outros
2. Calcule minha proporção de fala
3. Encontre momentos em que evitei dar feedback direto
4. Rastreie meu uso de palavras de preenchimento
5. Mostre exemplos de boa escuta ativa
```

## Instruções

Quando um usuário solicita análise de reunião:

1. **Descobrir Dados Disponíveis**
   - Verificar a pasta para arquivos de transcrição (.txt, .md, .vtt, .srt, .docx)
   - Confirmar se os arquivos contêm rótulos de orador e timestamps
   - Confirmar o intervalo de datas das reuniões
   - Identificar o nome/identificador do usuário nas transcrições

2. **Esclarecer Objetivos de Análise**
   
   Se não especificado, pergunte o que ele deseja aprender:
   - Comportamentos específicos (evitação de conflito, interrupções, palavras de preenchimento)
   - Eficácia de comunicação (clareza, diretividade, escuta)
   - Habilidades de facilitação de reuniões
   - Padrões de fala e proporções
   - Áreas de crescimento para melhoria
   
3. **Analisar Padrões**

   Para cada insight solicitado:
   
   **Evitação de Conflito**:
   - Procurar linguagem hesitante ("talvez", "tipo", "eu acho")
   - Frases indiretas em vez de pedidos diretos
   - Mudar de assunto quando a tensão surge
   - Concordar sem compromisso ("é, mas...")
   - Não abordar problemas óbvios
   
   **Proporções de Fala**:
   - Calcular percentual de tempo de reunião falando
   - Contar interrupções (pelo usuário e dele)
   - Medir comprimento médio de turno de fala
   - Rastrear proporção de perguntas versus afirmações
   
   **Palavras de Preenchimento**:
   - Contar "ahn", "hã", "tipo", "sabe", "na verdade", etc.
   - Observar frequência por minuto ou por turno de fala
   - Identificar situações onde aumentam (nervoso, incerto)
   
   **Escuta Ativa**:
   - Perguntas que fazem referência aos pontos anteriores de outros
   - Parafrasear ou resumir ideias de outros
   - Construir sobre contribuições alheias
   - Fazer perguntas de esclarecimento
   
   **Liderança e Facilitação**:
   - Abordagem de tomada de decisão (diretiva versus colaborativa)
   - Como desacordos são tratados
   - Inclusão de participantes mais quietos
   - Gestão de tempo e controle de agenda
   - Clareza de acompanhamento e itens de ação

4. **Fornecer Exemplos Específicos**

   Para cada padrão encontrado, inclua:
   
   ```markdown
   ### [Nome do Padrão]
   
   **Descoberta**: [Resumo de uma frase do padrão]
   
   **Frequência**: [X vezes em Y reuniões]
   
   **Exemplos**:
   
   1. **[Nome/Data da Reunião]** - [Timestamp]
      
      **O que Aconteceu**:
      > [Citação real da transcrição]
      
      **Por Que Importa**:
      [Explicação do impacto ou oportunidade perdida]
      
      **Abordagem Melhor**:
      [Fraseado alternativo específico ou comportamento]
   
   [Repetir para 2-3 exemplos mais fortes]
   ```

5. **Sintetizar Insights**

   Após analisar todos os padrões, forneça:
   
   ```markdown
   # Resumo de Insights de Reunião
   
   **Período de Análise**: [Intervalo de datas]
   **Reuniões Analisadas**: [X reuniões]
   **Duração Total**: [X horas]
   
   ## Padrões-Chave Identificados
   
   ### 1. [Padrão Primário]
   - **Observado**: [O que você viu]
   - **Impacto**: [Por que importa]
   - **Recomendação**: [Como melhorar]
   
   ### 2. [Segundo Padrão]
   [Mesma estrutura]
   
   ## Pontos Fortes de Comunicação
   
   1. [Ponto forte 1 com exemplo]
   2. [Ponto forte 2 com exemplo]
   3. [Ponto forte 3 com exemplo]
   
   ## Oportunidades de Crescimento
   
   1. **[Área 1]**: [Conselho específico e acionável]
   2. **[Área 2]**: [Conselho específico e acionável]
   3. **[Área 3]**: [Conselho específico e acionável]
   
   ## Estatísticas de Fala
   
   - Tempo médio de fala: [X% da reunião]
   - Perguntas feitas: [X por reunião em média]
   - Palavras de preenchimento: [X por minuto]
   - Interrupções: [X dadas / Y recebidas por reunião]
   
   ## Próximos Passos
   
   [3-5 ações concretas para melhorar comunicação]
   ```

6. **Oferecer Opções de Acompanhamento**
   - Rastrear essas mesmas métricas em reuniões futuras
   - Aprofundamento em reuniões ou padrões específicos
   - Comparar com benchmarks do setor
   - Criar um plano de desenvolvimento pessoal de comunicação
   - Gerar resumo para avaliações de desempenho

## Exemplos

### Exemplo 1: Análise de Evitação de Conflito (Inspirado em Dan Shipper)

**Usuário**: "Faço download de todas as minhas gravações de reuniões e coloco em uma pasta. Me diga todas as vezes que evitei conflito de forma sutil."

**Saída**: 
```markdown
# Padrões de Evitação de Conflito

Encontrei 23 instâncias em 15 reuniões onde você usou comunicação 
indireta ou evitou abordar tensões diretamente.

## Padrão: Hesitação ao Dar Feedback Crítico

**Frequência**: 8 vezes em 7 reuniões

**Exemplo 1: 1:1 com Sarah** - 00:14:32

**O que Aconteceu**:
> "Então, eu estava pensando... talvez pudéssemos, tipo, 
> potencialmente considerar olhar o cronograma novamente? Quer dizer, 
> se você achar que faz sentido. Mas seja o que você achar melhor!"

**Por Que Importa**:
Você precisava abordar que o projeto de Sarah estava atrasado, 
mas a linguagem hesitante ("talvez", "potencialmente", "se você achar") 
e a deflexão no final ("seja o que você achar") tornaram fácil para ela 
perder a urgência.

**Abordagem Melhor**:
"Sarah, o projeto está duas semanas atrasado. Precisamos discutir 
o que está bloqueando o progresso e criar um novo cronograma hoje."

[Exemplos adicionais...]

## Recomendações

1. **Nomear o problema diretamente** na primeira frase
2. **Remover palavras hesitantes** como "talvez", "tipo", "tipo de"
3. **Fazer perguntas específicas** em vez de dar dicas
4. **Agendar conversas difíceis** em vez de levantá-las casualmente
```

### Exemplo 2: Facilitação de Liderança

**Usuário**: "Analise minhas reuniões de equipe e me diga sobre meu estilo de facilitação."

**Saída**: Fornece insights sobre:
- Quanto você fala versus membros da equipe (60% versus 40%)
- Se você faz perguntas ou afirmações (proporção 3:1)
- Como você lida com desacordos (tendência de resolver muito rápido)
- Quem fala menos e se você os inclui
- Exemplos de bons e perdidos momentos de facilitação

### Exemplo 3: Rastreamento de Desenvolvimento Pessoal

**Usuário**: "Compare minhas reuniões do Q1 versus Q2 para ver se melhorei minhas habilidades de escuta."

**Saída**: Cria uma análise comparativa mostrando:
- Diminuição de interrupções (8 por reunião → 3 por reunião)
- Aumento de perguntas de esclarecimento (2 → 7 por reunião)
- Melhoria em construir sobre as ideias de outros
- Exemplos específicos mostrando a diferença
- Áreas restantes para crescimento

## Dicas de Configuração

### Obtendo Transcrições de Reuniões

**Do Granola** (gratuito com assinatura do boletim da Lenny):
- Granola transcreve automaticamente suas reuniões
- Exporte transcrições para uma pasta: [Instruções sobre como]
- Aponte Claude Code para essa pasta

**Do Zoom**:
- Ative gravação em nuvem com transcrição
- Faça download de arquivos VTT ou SRT após reuniões
- Armazene em uma pasta dedicada

**Do Google Meet**:
- Use auto-transcrição do Google Docs
- Salve documentos de transcrição em uma pasta
- Faça download como arquivos .txt ou dê acesso do Claude Code

**Do Fireflies.ai, Otter.ai, etc.**:
- Exporte transcrições em lote
- Armazene em uma pasta local
- Execute análise na pasta

### Melhores Práticas

1. **Nomenclatura consistente**: Use formato `YYYY-MM-DD - Nome da Reunião.txt`
2. **Análise regular**: Revise mensalmente ou trimestralmente para tendências
3. **Consultas específicas**: Pergunte sobre um comportamento por vez para profundidade
4. **Privacidade**: Mantenha dados sensíveis de reuniões locais
5. **Orientado para ação**: Foque em uma área de melhoria por vez

## Solicitações Comuns de Análise

- "Quando evito conversas difíceis?"
- "Com que frequência interrompo outros?"
- "Qual é minha proporção de fala versus escuta?"
- "Faço boas perguntas?"
- "Como lido com desacordo?"
- "Sou inclusivo com todas as vozes?"
- "Uso muitas palavras de preenchimento?"
- "Quão claros são meus itens de ação?"
- "Fico na agenda ou me deixo levar?"
- "Como minha comunicação mudou ao longo do tempo?"

## Casos de Uso Relacionados

- Criar um plano de desenvolvimento pessoal a partir de insights
- Preparar materiais de avaliação de desempenho com exemplos
- Orientar relatórios diretos sobre comunicação
- Analisar chamadas de clientes para padrões de vendas ou suporte
- Estudar táticas e resultados de negociação