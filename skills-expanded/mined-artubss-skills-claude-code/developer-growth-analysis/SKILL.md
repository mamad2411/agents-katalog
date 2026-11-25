---
name: developer-growth-analysis
description: Analisa seu histórico recente de chats do Claude Code para identificar padrões de codificação, lacunas no desenvolvimento e áreas para melhoria, seleciona recursos de aprendizagem relevantes do HackerNews e envia automaticamente um relatório de crescimento personalizado para suas DMs do Slack.
---

# Análise de Crescimento do Desenvolvedor

Esta skill fornece feedback personalizado sobre seu trabalho de codificação recente analisando suas interações com Claude Code e identificando padrões que revelam forças e áreas de crescimento.

## Quando Usar Esta Skill

Use esta skill quando você quiser:
- Compreender seus padrões e hábitos de desenvolvimento a partir do trabalho recente
- Identificar lacunas técnicas específicas ou desafios recorrentes
- Descobrir quais tópicos se beneficiariam de estudo mais aprofundado
- Obter recursos de aprendizagem curados conforme seus padrões reais de trabalho
- Acompanhar áreas de melhoria em seus projetos recentes
- Encontrar artigos de alta qualidade que abordem diretamente as habilidades que você está desenvolvendo

Esta skill é ideal para desenvolvedores que desejam feedback estruturado sobre seu crescimento sem esperar por revisões de código, e que preferem insights baseados em dados do histórico de seu próprio trabalho.

## O Que Esta Skill Faz

Esta skill realiza uma análise de seis etapas do seu trabalho de desenvolvimento:

1. **Lê Seu Histórico de Chats**: Acessa seu histórico local de chats do Claude Code das últimas 24-48 horas para entender em que você tem trabalhado.

2. **Identifica Padrões de Desenvolvimento**: Analisa os tipos de problemas que você está resolvendo, tecnologias que está usando, desafios que enfrenta e como você aborda diferentes tipos de tarefas.

3. **Detecta Áreas de Melhoria**: Reconhece padrões que sugerem lacunas de habilidades, dificuldades repetidas, abordagens ineficientes ou áreas em que você poderia se beneficiar de conhecimento mais aprofundado.

4. **Gera um Relatório Personalizado**: Cria um relatório abrangente mostrando o resumo do seu trabalho, áreas de melhoria identificadas e recomendações específicas para crescimento.

5. **Encontra Recursos de Aprendizagem**: Usa HackerNews para selecionar artigos e discussões de alta qualidade diretamente relevantes às suas áreas de melhoria, fornecendo uma lista de leitura adaptada ao seu trabalho de desenvolvimento real.

6. **Envia para Suas DMs do Slack**: Entrega automaticamente o relatório completo para suas mensagens diretas do Slack para que você possa consultá-lo a qualquer hora, em qualquer lugar.

## Como Usar

Peça ao Claude para analisar seu trabalho de codificação recente:

```
Analise meu crescimento como desenvolvedor a partir de meus chats recentes
```

Ou seja mais específico sobre qual período:

```
Analise meu trabalho de hoje e sugira áreas para melhoria
```

A skill gerará um relatório formatado com:
- Visão geral do seu trabalho recente
- Principais áreas de melhoria identificadas
- Recomendações específicas para cada área
- Recursos de aprendizagem curados do HackerNews
- Itens de ação em que você pode se concentrar

## Instruções

Quando um usuário solicitar análise de seu crescimento como desenvolvedor ou padrões de codificação a partir do trabalho recente:

1. **Acesse o Histórico de Chats**

   Leia o histórico de chats de `~/.claude/history.jsonl`. Este arquivo está em formato JSONL onde cada linha contém:
   - `display`: A mensagem/solicitação do usuário
   - `project`: O projeto em que está sendo trabalhado
   - `timestamp`: Timestamp Unix (em milissegundos)
   - `pastedContents`: Qualquer código ou conteúdo colado

   Filtre entradas dos últimos 24-48 horas com base no timestamp atual.

2. **Analise Padrões de Trabalho**

   Extraia e analise o seguinte dos chats filtrados:
   - **Projetos e Domínios**: Que tipos de projetos o usuário estava trabalhando? (por exemplo, backend, frontend, DevOps, dados, etc.)
   - **Tecnologias Usadas**: Quais linguagens, frameworks e ferramentas aparecem nas conversas?
   - **Tipos de Problema**: Que categorias de problemas estão sendo resolvidas? (por exemplo, otimização de desempenho, debugging, implementação de recursos, refatoração, configuração/setup)
   - **Desafios Enfrentados**: Com quais problemas o usuário lutou? Procure por:
     - Perguntas repetidas sobre tópicos similares
     - Problemas que levaram múltiplas tentativas para resolver
     - Perguntas indicando lacunas de conhecimento
     - Decisões arquiteturais complexas
   - **Padrões de Abordagem**: Como o usuário resolve problemas? (por exemplo, metódico, exploratório, experimental)

3. **Identifique Áreas de Melhoria**

   Com base na análise, identifique 3-5 áreas específicas em que o usuário poderia melhorar. Estas devem ser:
   - **Específicas** (não vagas como "melhorar habilidades de codificação")
   - **Baseadas em Evidências** (fundamentadas no histórico real de chats)
   - **Acionáveis** (melhorias práticas que podem ser realizadas)
   - **Priorizadas** (mais impactantes primeiro)

   Exemplos de boas áreas de melhoria:
   - "Padrões avançados de TypeScript (genéricos, tipos de utilidade, type guards) - você lutou com segurança de tipos no [projeto específico]"
   - "Tratamento de erros e validação - notei que você corrigiu vários bugs relacionados a verificações de null faltando"
   - "Padrões async/await - seu trabalho recente mostra algumas race conditions e problemas de timing"
   - "Otimização de consultas de banco de dados - você reescreveu a mesma consulta várias vezes"

4. **Gere Relatório**

   Crie um relatório abrangente com esta estrutura:

   ```markdown
   # Seu Relatório de Crescimento como Desenvolvedor

   **Período do Relatório**: [Ontem / Hoje / [Intervalo de Datas Personalizado]]
   **Última Atualização**: [Data e Hora Atual]

   ## Resumo do Trabalho

   [2-3 parágrafos resumindo em que o usuário trabalhou, projetos tocados, tecnologias usadas e áreas de foco geral]

   Exemplo:
   "Nas últimas 24 horas, você se concentrou principalmente no desenvolvimento backend com três projetos distintos. Seu trabalho envolveu TypeScript, React e infraestrutura de deployment. Você enfrentou uma mistura de implementação de recursos, debugging e decisões arquiteturais, com foco particular em design de API e otimização de banco de dados."

   ## Áreas de Melhoria (Priorizadas)

   ### 1. [Nome da Área]

   **Por Que Isso Importa**: [Explicação de por que essa habilidade é importante para o trabalho do usuário]

   **O Que Observei**: [Evidência específica do histórico de chats mostrando essa lacuna]

   **Recomendação**: [Passo(s) concreto(s) para melhorar nessa área]

   **Tempo para Aprender**: [Estimativa breve do esforço necessário]

   ---

   [Repetir para 2-4 áreas adicionais]

   ## Forças Observadas

   [2-3 pontos de bala destacando o que você está fazendo bem - coisas a continuar fazendo]

   ## Itens de Ação

   Ordem de prioridade:
   1. [Item de ação derivado da área de melhoria de maior prioridade]
   2. [Item de ação da próxima área]
   3. [Item de ação da próxima área]

   ## Recursos de Aprendizagem

   [Será preenchido na próxima etapa]
   ```

5. **Pesquise Recursos de Aprendizagem**

   Use Rube MCP para pesquisar no HackerNews artigos relacionados a cada área de melhoria:

   - Para cada área de melhoria, construa uma consulta de pesquisa visando recursos de alta qualidade
   - Pesquise HackerNews usando RUBE_SEARCH_TOOLS com consultas como:
     - "Aprenda [Tecnologia/Padrão] melhores práticas"
     - "[Tecnologia] padrões avançados e técnicas"
     - "Debugging [tipo de problema específico] em [linguagem]"
   - Priorize posts com alto engajamento (comentários, upvotes)
   - Para cada área, inclua 2-3 artigos mais relevantes com:
     - Título do artigo
     - Data de publicação
     - Breve descrição de por que é relevante
     - Link para o artigo

   Adicione esta seção ao relatório:

   ```markdown
   ## Recursos de Aprendizagem Curados

   ### Para: [Área de Melhoria]

   1. **[Título do Artigo]** - [Data]
      [Descrição do que cobre e por que é relevante para sua área de melhoria]
      [Link]

   2. **[Título do Artigo]** - [Data]
      [Descrição]
      [Link]

   [Repetir para outras áreas de melhoria]
   ```

6. **Apresente o Relatório Completo**

   Entregue o relatório em um formato limpo e legível que o usuário possa:
   - Digitalizar rapidamente para obter conclusões principais
   - Usar para planejamento de aprendizagem focado
   - Consultar durante a próxima semana enquanto trabalha em melhorias
   - Compartilhar com mentores se desejar feedback externo

7. **Envie Relatório para DMs do Slack**

   Use Rube MCP para enviar o relatório completo para as DMs do Slack do usuário:

   - Verifique se a conexão Slack está ativa via RUBE_SEARCH_TOOLS
   - Se não estiver conectado, use RUBE_MANAGE_CONNECTIONS para iniciar autenticação Slack
   - Use RUBE_MULTI_EXECUTE_TOOL para enviar o relatório como mensagem formatada:
     - Envie o título do relatório e período como a primeira mensagem
     - Divida o relatório em seções lógicas (Resumo, Melhorias, Forças, Ações, Recursos)
     - Formate cada seção como uma mensagem Slack bem estruturada com markdown apropriado
     - Inclua links clicáveis para os recursos de aprendizagem
   - Confirme a entrega na saída da CLI

   Isso garante que o usuário tenha o relatório em um lugar que ele verifica regularmente e possa consultá-lo durante a semana.

## Exemplo de Uso

### Entrada

```
Analise meu crescimento como desenvolvedor a partir de meus chats recentes
```

### Saída

```markdown
# Seu Relatório de Crescimento como Desenvolvedor

**Período do Relatório**: 9-10 de novembro de 2024
**Última Atualização**: 10 de novembro de 2024, 21:15 UTC

## Resumo do Trabalho

Nos últimos dois dias, você se concentrou em infraestrutura backend e desenvolvimento de API. Seu projeto principal era um aplicativo showcase de código aberto, onde você fez progresso significativo no gerenciamento de conexões, melhorias de UI e configuração de deployment. Você trabalhou com TypeScript, React e Node.js, enfrentando desafios que variavam de segurança de dados a design responsivo. Seu trabalho mostra um equilíbrio entre implementar recursos e resolver débito técnico.

## Áreas de Melhoria (Priorizadas)

### 1. Padrões Avançados de TypeScript e Segurança de Tipos

**Por Que Isso Importa**: TypeScript é central para seu trabalho, mas aproveitar seus recursos avançados (genéricos, tipos de utilidade, tipos condicionais, type guards) pode melhorar significativamente a confiabilidade do código e reduzir erros em tempo de execução. Melhor segurança de tipos detecta bugs no tempo de compilação em vez de em produção.

**O Que Observei**: Em seus chats recentes, você estava trabalhando com estruturas de dados de conexão e teve dificuldade algumas vezes ao digitar configurações de autenticação corretamente. Você também teve que iterar sobre tipos union para diferentes estados de conexão. Há uma oportunidade de usar discriminated unions e type guards mais efetivamente.

**Recomendação**: Estude o sistema de tipos avançado de TypeScript, particularmente tipos de utilidade (Omit, Pick, Record), tipos condicionais e discriminated unions. Aplique esses padrões ao seu manuseio de configuração de conexão e gerenciamento de estado de autenticação.

**Tempo para Aprender**: 5-8 horas de aprendizado e prática focados

### 2. Manuseio Seguro de Dados e Ocultamento de Informações em UI

**Por Que Isso Importa**: Você identificou e corrigiu uma preocupação de segurança em que dados de conexão sensíveis estavam sendo exibidos em seu console. Evitar vazamento de informações é crítico para aplicações que lidam com credenciais de usuários e chaves de API. Boas práticas aqui previnem incidentes de segurança e violações de confiança do usuário.

**O Que Observei**: Você percebeu que sua página "Seus Apps" estava mostrando dados completos de conexão incluindo configs de autenticação. Isso demonstra bom instinto de segurança, e o próximo passo é integrar isso em seu pensamento padrão ao manejar informações sensíveis.

**Recomendação**: Revise melhores práticas de segurança para manuseio de dados sensíveis em aplicações frontend. Crie padrões reutilizáveis para filtrar/mascarar informações sensíveis antes de exibi-las. Considere implementar uma camada de dados segura que explicitamente liste o que pode ser mostrado na UI.

**Tempo para Aprender**: 3-4 horas

### 3. Arquitetura de Componentes e Padrões de UI Responsiva

**Por Que Isso Importa**: Você está projetando UIs que precisam funcionar em diferentes tamanhos de tela e interações do usuário. Uma arquitetura de componentes forte facilita a construção de UIs complexas sem bugs e melhora a manutenibilidade.

**O Que Observei**: Você trabalhou na UI do "Marketplace" (anteriormente Browse Tools), recriando-a a partir de uma imagem de design. Você também identificou e corrigiu problemas de scroll onde conteúdo estava transbordando containers. Há uma oportunidade de fortalecer seu entendimento de contenção de layout e padrões de design responsivo.

**Recomendação**: Estude padrões de composição de componentes React e melhores práticas de layout CSS (especialmente flexbox e grid). Concentre-se em container queries e padrões responsivos que evitem problemas de overflow. Explore bibliotecas de composição de componentes e abordagens de design system.

**Tempo para Aprender**: 6-10 horas (dependendo da profundidade)

## Forças Observadas

- **Consciência de Segurança**: Você identificou proativamente problemas de vazamento de dados antes que se tornassem problemas
- **Refinamento Iterativo**: Você trabalhou nos requisitos de UI metodicamente, fazendo perguntas esclarecedoras e melhorando designs
- **Capacidade Full-Stack**: Você trabalha confortavelmente em APIs backend, UI frontend e preocupações de deployment
- **Abordagem de Resolução de Problemas**: Você divide tarefas complexas em passos gerenciáveis

## Itens de Ação

Ordem de prioridade:
1. Gaste 1-2 horas aprendendo tipos de utilidade de TypeScript e discriminated unions; aplique às suas estruturas de dados de conexão
2. Documente padrões de segurança para seu projeto (quais dados são seguros para exibir, funções de filtragem/mascaramento)
3. Estude um artigo sobre padrões React avançados e aplique um padrão ao seu trabalho de UI atual
4. Configure uma checklist de revisão de código focada em segurança de tipos e segurança de dados para future PRs

## Recursos de Aprendizagem Curados

### Para: Padrões Avançados de TypeScript

1. **Tipos Avançados de TypeScript: Genéricos, Tipos de Utilidade e Tipos Condicionais** - HackerNews, outubro de 2024
   Mergulho profundo no sistema de tipos de TypeScript com exemplos práticos e aplicações no mundo real. Cobre discriminated unions, type guards e padrões para garantir segurança em tempo de compilação em aplicações complexas.
   [Link para discussão]

2. **Construindo APIs Type-Safe em TypeScript** - HackerNews, setembro de 2024
   Guia prático para projetar APIs com TypeScript que detectam erros cedo. Particularmente relevante para seu trabalho de configuração de conexão.
   [Link para discussão]

### Para: Manuseio Seguro de Dados em Frontend

1. **Prevenção de Vazamento de Informações em Aplicações Web** - HackerNews, agosto de 2024
   Guia abrangente de segurança de dados em aplicações frontend, incluindo filtragem de informações sensíveis, logging seguro e trilhas de auditoria.
   [Link para discussão]

2. **Melhores Práticas de Gerenciamento de OAuth e Chaves de API** - HackerNews, julho de 2024
   Como manejar com segurança tokens de autenticação e chaves de API em aplicações, com exemplos para diferentes frameworks.
   [Link para discussão]

### Para: Arquitetura de Componentes e Design Responsivo

1. **Padrões Avançados de React: Composição em Vez de Configuração** - HackerNews
   Explora estratégias de composição de componentes que escalam, com exemplos usando padrões modernos de React.
   [Link para discussão]

2. **Domínio de Layout CSS: Flexbox, Grid e Container Queries** - HackerNews, outubro de 2024
   Aprenda padrões de design responsivo que evitem problemas de overflow e funcionem em todos os tamanhos de tela.
   [Link para discussão]
```

## Dicas e Melhores Práticas

- Execute essa análise uma vez por semana para acompanhar sua trajetória de melhoria ao longo do tempo
- Escolha uma área de melhoria por vez e concentre-se nela por alguns dias antes de passar para a próxima
- Use os recursos de aprendizagem como guia de estudo; trabalhe através dos materiais recomendados e pratique aplicar os padrões
- Revisit este relatório depois de se concentrar em uma área por uma semana para ver como seus padrões de trabalho mudam
- Os recursos de aprendizagem são intencionalmente curados para seu trabalho real, não tópicos genéricos, então serão altamente relevantes para o que você está construindo

## Como Precisão e Qualidade São Mantidas

Esta skill:
- Analisa seus padrões de trabalho reais do histórico de chats com timestamp
- Gera recomendações baseadas em evidências fundamentadas em projetos reais
- Seleciona recursos de aprendizagem que abordam diretamente suas lacunas identificadas
- Foca em melhorias acionáveis, não feedback vago
- Fornece estimativas de tempo específicas com base na complexidade
- Prioriza áreas que terão o maior impacto na sua velocidade de desenvolvimento