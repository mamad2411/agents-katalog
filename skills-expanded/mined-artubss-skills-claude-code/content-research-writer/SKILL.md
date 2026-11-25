---
name: content-research-writer
description: Auxilia na redação de conteúdo de alta qualidade através de pesquisa, adição de citações, melhoria de ganchos, iteração em esquemas e feedback em tempo real de cada seção. Transforma seu processo de escrita de esforço solo em parceria colaborativa.
---

# Content Research Writer

Esta skill funciona como seu parceiro de escrita, ajudando você a pesquisar, estruturar, redigir e refinar conteúdo mantendo sua voz e estilo únicos.

## Quando Usar Esta Skill

- Redigindo posts de blog, artigos ou newsletters
- Criando conteúdo educacional ou tutoriais
- Rascunhando artigos de thought leadership
- Pesquisando e escrevendo estudos de caso
- Produzindo documentação técnica com fontes
- Escrevendo com citações e referências apropriadas
- Melhorando ganchos e introduções
- Recebendo feedback seção por seção enquanto escreve

## O Que Esta Skill Faz

1. **Estruturação Colaborativa**: Ajuda você a organizar ideias em esquemas coerentes
2. **Assistência de Pesquisa**: Encontra informações relevantes e adiciona citações
3. **Melhoria de Gancho**: Fortalece sua abertura para capturar atenção
4. **Feedback por Seção**: Revisa cada seção conforme você escreve
5. **Preservação de Voz**: Mantém seu estilo e tom de escrita
6. **Gestão de Citações**: Adiciona e formata referências corretamente
7. **Refinamento Iterativo**: Ajuda você a melhorar através de múltiplos rascunhos

## Como Usar

### Configure Seu Ambiente de Escrita

Crie uma pasta dedicada para seu artigo:
```
mkdir ~/writing/my-article-title
cd ~/writing/my-article-title
```

Crie seu arquivo de rascunho:
```
touch article-draft.md
```

Abra Claude Code nesse diretório e comece a escrever.

### Fluxo de Trabalho Básico

1. **Comece com um esquema**:
```
Ajude-me a criar um esquema para um artigo sobre [tópico]
```

2. **Pesquise e adicione citações**:
```
Pesquise [tópico específico] e adicione citações ao meu esquema
```

3. **Melhore o gancho**:
```
Aqui está minha introdução. Ajude-me a deixar o gancho mais envolvente.
```

4. **Obtenha feedback por seção**:
```
Acabei de terminar a seção "Por Que Isso Importa". Revise e dê feedback.
```

5. **Refine e polua**:
```
Revise o rascunho completo quanto a fluxo, clareza e consistência.
```

## Instruções

Quando um usuário solicita assistência de escrita:

1. **Entenda o Projeto de Escrita**
   
   Faça perguntas de esclarecimento:
   - Qual é o tópico e argumento principal?
   - Qual é o público-alvo?
   - Qual é o comprimento/formato desejado?
   - Qual é seu objetivo? (educar, persuadir, entreter, explicar)
   - Há pesquisa ou fontes existentes para incluir?
   - Qual é seu estilo de escrita? (formal, conversacional, técnico)

2. **Estruturação Colaborativa**
   
   Ajude a estruturar o conteúdo:
   
   ```markdown
   # Esquema de Artigo: [Título]
   
   ## Gancho
   - [Linha de abertura/história/estatística]
   - [Por que o leitor deveria se importar]
   
   ## Introdução
   - Contexto e antecedentes
   - Declaração do problema
   - O que este artigo aborda
   
   ## Seções Principais
   
   ### Seção 1: [Título]
   - Ponto-chave A
   - Ponto-chave B
   - Exemplo/evidência
   - [Pesquisa necessária: tópico específico]
   
   ### Seção 2: [Título]
   - Ponto-chave C
   - Ponto-chave D
   - Dados/citação necessária
   
   ### Seção 3: [Título]
   - Ponto-chave E
   - Contra-argumentos
   - Resolução
   
   ## Conclusão
   - Resumo dos pontos principais
   - Call to action
   - Pensamento final
   
   ## To-Do de Pesquisa
   - [ ] Encontre dados sobre [tópico]
   - [ ] Obtenha exemplos de [conceito]
   - [ ] Fonte citação para [afirmação]
   ```
   
   **Itere no esquema**:
   - Ajuste com base em feedback
   - Garanta fluxo lógico
   - Identifique lacunas de pesquisa
   - Marque seções para aprofundamento

3. **Conduza Pesquisa**
   
   Quando usuário solicita pesquisa sobre um tópico:
   
   - Pesquise informações relevantes
   - Encontre fontes confiáveis
   - Extraia fatos-chave, citações e dados
   - Adicione citações no formato solicitado
   
   Exemplo de saída:
   ```markdown
   ## Pesquisa: Impacto de IA na Produtividade
   
   Principais Descobertas:
   
   1. **Ganhos de Produtividade**: Estudos mostram 40% de economia de tempo em 
      tarefas de criação de conteúdo [1]
   
   2. **Taxas de Adoção**: 67% dos profissionais de conhecimento usam ferramentas 
      de IA semanalmente [2]
   
   3. **Citação de Especialista**: "IA aumenta em vez de substituir criatividade 
      humana" - Dra. Jane Smith, MIT [3]
   
   Citações:
   [1] McKinsey Global Institute. (2024). "The Economic Potential 
       of Generative AI"
   [2] Stack Overflow Developer Survey (2024)
   [3] Smith, J. (2024). Entrevista MIT Technology Review
   
   Adicionado ao seu esquema na Seção 2.
   ```

4. **Melhore Ganchos**
   
   Quando usuário compartilha uma introdução, analise e fortaleça:
   
   **Análise do Gancho Atual**:
   - O que funciona: [elementos positivos]
   - O que pode ser mais forte: [áreas para melhoria]
   - Impacto emocional: [atual vs. potencial]
   
   **Alternativas Sugeridas**:
   
   Opção 1: [Afirmação corajosa]
   > [Exemplo]
   *Por que funciona: [explicação]*
   
   Opção 2: [História pessoal]
   > [Exemplo]
   *Por que funciona: [explicação]*
   
   Opção 3: [Dados surpreendentes]
   > [Exemplo]
   *Por que funciona: [explicação]*
   
   **Perguntas sobre gancho**:
   - Cria curiosidade?
   - Promete valor?
   - É específico o suficiente?
   - Corresponde ao público?

5. **Forneça Feedback por Seção**
   
   Conforme usuário escreve cada seção, revise para:
   
   ```markdown
   # Feedback: [Nome da Seção]
   
   ## O Que Funciona Bem ✓
   - [Força 1]
   - [Força 2]
   - [Força 3]
   
   ## Sugestões para Melhoria
   
   ### Clareza
   - [Problema específico] → [Correção sugerida]
   - [Frase complexa] → [Alternativa mais simples]
   
   ### Fluxo
   - [Problema de transição] → [Conexão melhor]
   - [Ordem de parágrafo] → [Reordenação sugerida]
   
   ### Evidência
   - [Afirmação que precisa suporte] → [Adicionar citação ou exemplo]
   - [Afirmação genérica] → [Tornar mais específica]
   
   ### Estilo
   - [Inconsistência de tom] → [Corresponder melhor sua voz]
   - [Escolha de palavra] → [Alternativa mais forte]
   
   ## Edições de Linhas Específicas
   
   Original:
   > [Citação exata do rascunho]
   
   Sugerido:
   > [Versão melhorada]
   
   Por quê: [Explicação]
   
   ## Perguntas para Considerar
   - [Pergunta provocadora 1]
   - [Pergunta provocadora 2]
   
   Pronto para a próxima seção!
   ```

6. **Preserve a Voz do Escritor**
   
   Princípios importantes:
   
   - **Aprenda seu estilo**: Leia amostras de escrita existentes
   - **Sugira, não substitua**: Ofereça opções, não diretivas
   - **Corresponda tom**: Formal, casual, técnico, amigável
   - **Respeite escolhas**: Se preferirem sua versão, apoie
   - **Melhore, não reescreva**: Torne sua escrita melhor, não diferente
   
   Pergunte periodicamente:
   - "Isso soa como você?"
   - "Este é o tom certo?"
   - "Devo ser mais/menos [formal/casual/técnico]?"

7. **Gestão de Citações**
   
   Lide com referências conforme preferência do usuário:
   
   **Citações Inline**:
   ```markdown
   Estudos mostram 40% de melhoria em produtividade (McKinsey, 2024).
   ```
   
   **Referências Numeradas**:
   ```markdown
   Estudos mostram 40% de melhoria em produtividade [1].
   
   [1] McKinsey Global Institute. (2024)...
   ```
   
   **Estilo Rodapé**:
   ```markdown
   Estudos mostram 40% de melhoria em produtividade^1
   
   ^1: McKinsey Global Institute. (2024)...
   ```
   
   Mantenha uma lista de citações em execução:
   ```markdown
   ## Referências
   
   1. Autor. (Ano). "Título". Publicação.
   2. Autor. (Ano). "Título". Publicação.
   ...
   ```

8. **Revisão Final e Polimento**
   
   Quando rascunho está completo, forneça feedback abrangente:
   
   ```markdown
   # Revisão de Rascunho Completo
   
   ## Avaliação Geral
   
   **Forças**:
   - [Força maior 1]
   - [Força maior 2]
   - [Força maior 3]
   
   **Impacto**: [Avaliação de efetividade geral]
   
   ## Estrutura e Fluxo
   - [Comentários sobre organização]
   - [Qualidade de transições]
   - [Avaliação de ritmo]
   
   ## Qualidade do Conteúdo
   - [Força do argumento]
   - [Suficiência de evidência]
   - [Efetividade de exemplos]
   
   ## Qualidade Técnica
   - Gramática e mecânica: [avaliação]
   - Consistência: [avaliação]
   - Citações: [verificação de completude]
   
   ## Legibilidade
   - Escore de clareza: [avaliação]
   - Variedade de sentença: [avaliação]
   - Comprimento de parágrafo: [avaliação]
   
   ## Sugestões de Polimento Final
   
   1. **Introdução**: [Melhorias específicas]
   2. **Corpo**: [Melhorias específicas]
   3. **Conclusão**: [Melhorias específicas]
   4. **Título**: [Opções se necessário]
   
   ## Checklist Pré-Publicação
   - [ ] Todas as afirmações com fontes
   - [ ] Citações formatadas
   - [ ] Exemplos claros
   - [ ] Transições suaves
   - [ ] Call to action presente
   - [ ] Revisado para erros de digitação
   
   Pronto para publicar! 🚀
   ```

## Exemplos

### Exemplo 1: Fluxo de Trabalho de Teresa Torres

**Usuário**: "Estou escrevendo um artigo sobre descoberta contínua. Ajude-me a criar um esquema."

**Processo**:
1. Colabora na estrutura do esquema
2. Identifica necessidades de pesquisa
3. Usuário começa a escrever introdução
4. Revisa e melhora o gancho
5. Usuário escreve cada seção
6. Fornece feedback após cada seção
7. Conduz pesquisa e adiciona citações
8. Revisão final do rascunho completo
9. Polimento e preparação para publicação

**Resultado**: Artigo bem pesquisado, com citações apropriadas, escrito na voz de Teresa com estrutura e fluxo fortes.

### Exemplo 2: Artigo Pesado em Pesquisa

**Usuário**: "Estou escrevendo sobre o impacto de IA em product management. Ajude-me a encontrar dados e exemplos atuais."

**Saída**:
```markdown
## Pesquisa Compilada

### Dados Recentes
- Gartner: 80% dos PMs usarão ferramentas de IA até 2025 [1]
- Pesquisa: 45% relatam entrega de features mais rápida [2]
- Estudo de caso: Priorização assistida por IA do Airbnb [3]

### Citações de Especialistas
- "IA amplifica julgamento de PM, não substitui" - Marty Cagan
- [Citações adicionais com fontes]

### Exemplos Reais
1. **Empresa A**: Usou IA para síntese de pesquisa de usuário
   - Resultado: Economia de 60% em tempo
   - Fonte: [citação]

2. **Empresa B**: Análise de roadmap assistida por IA
   - Resultado: Melhor alinhamento de stakeholder
   - Fonte: [citação]

Tudo adicionado ao seu esquema com citações apropriadas.
```

### Exemplo 3: Melhoria de Gancho

**Gancho Original do Usuário**:
> "Product management está mudando por causa de IA. Neste artigo, discutirei algumas formas como IA afeta product managers."

**Opções Melhoradas**:

**Opção 1 (Dados)**:
> "Mês passado, pedi a IA para analisar 500 entrevistas com clientes. Levou 30 minutos em vez de 3 semanas. Product management nunca será o mesmo."

**Opção 2 (Pergunta)**:
> "E se você pudesse conversar com todo cliente, ler cada avaliação e analisar cada ticket de suporte—tudo antes de seu café da manhã?"

**Opção 3 (História)**:
> "Sarah gastou duas semanas construindo a feature errada. Não porque não entendia seus usuários, mas porque não conseguia processar centenas de entrevistas rápido o bastante para ver o padrão."

### Exemplo 4: Feedback por Seção

**Usuário**: "Acabei de terminar minha seção 'Erros Comuns'. Pensamentos?"

**Resposta**:
```markdown
# Feedback: Seção Erros Comuns

## O Que Funciona Bem ✓
- Exemplos fortes (a história de notificação do Slack)
- Estrutura clara (3 erros, layout limpo)
- Conselho prático para cada erro

## Sugestões

### Torne Mais Específico
Seu segundo ponto diz "Priorização ruim" mas pode ser mais forte:

Atual:
> "Muitos times priorizam mal focando em features em vez de resultados."

Sugerido:
> "Assisti times entregar 14 features em um trimestre mas não mover nenhuma de suas métricas-chave. Priorizam atividade em vez de progresso."

### Adicione Dados
O terceiro erro se beneficiaria de evidência:
> "[Adicionar citação]: Estudos mostram times sem contato regular com usuários são 3x mais propensos a construir features não utilizadas [precisa fonte]"

### Melhoria de Fluxo
Considere reordenar: Erro 3 → Erro 2 → Erro 1
Isso constrói de impacto pequeno para grande.

Pronto para a próxima seção!
```

## Fluxos de Trabalho de Escrita

### Fluxo de Blog Post
1. Esquema junto
2. Pesquise pontos-chave
3. Escreva introdução → obtenha feedback
4. Escreva seções do corpo → feedback cada
5. Escreva conclusão → revisão final
6. Polimento e edição

### Fluxo de Newsletter
1. Discuta ideias de gancho
2. Esquema rápido (formato mais curto)
3. Rascunho em uma sessão
4. Revise quanto a clareza e links
5. Polimento rápido

### Fluxo de Tutorial Técnico
1. Esquema dos passos
2. Escreva exemplos de código
3. Adicione explicações
4. Teste instruções
5. Adicione seção de troubleshooting
6. Revisão final de acurácia

### Fluxo de Thought Leadership
1. Brainstorm ângulo único
2. Pesquise perspectivas existentes
3. Desenvolva sua tese
4. Escreva com POV forte
5. Adicione evidência suportadora
6. Elabore conclusão envolvente

## Dicas Pro

1. **Trabalhe em VS Code**: Melhor que Claude na web para escrita longa
2. **Uma seção por vez**: Obtenha feedback incrementalmente
3. **Salve pesquisa separadamente**: Mantenha arquivo research.md
4. **Versione seus rascunhos**: article-v1.md, article-v2.md, etc.
5. **Leia em voz alta**: Use feedback para identificar frases desajeitadas
6. **Defina prazos**: "Quero terminar o rascunho hoje"
7. **Faça pausas**: Escreva, obtenha feedback, pause, revise

## Organização de Arquivos

Estrutura recomendada para projetos de escrita:

```
~/writing/article-name/
├── outline.md          # Seu esquema
├── research.md         # Toda pesquisa e citações
├── draft-v1.md         # Primeiro rascunho
├── draft-v2.md         # Rascunho revisado
├── final.md            # Pronto para publicação
├── feedback.md         # Feedback coletado
└── sources/            # Materiais de referência
    ├── study1.pdf
    └── article2.md
```

## Melhores Práticas

### Para Pesquisa
- Verifique fontes antes de citar
- Use dados recentes quando possível
- Equilibre diferentes perspectivas
- Vincule a fontes originais

### Para Feedback
- Seja específico sobre o que você quer: "Isto é muito técnico?"
- Compartilhe suas preocupações: "Acho que esta seção arrasta"
- Faça perguntas: "Isto flui logicamente?"
- Solicite alternativas: "Qual é outra forma de explicar isto?"

### Para Voz
- Compartilhe exemplos de sua escrita
- Especifique preferências de tom
- Aponte matches bons: "Isso soa como eu!"
- Sinalize desencontros: "Muito formal para meu estilo"

## Casos de Uso Relacionados

- Criando posts de mídia social a partir de artigos
- Adaptando conteúdo para públicos diferentes
- Escrevendo newsletters por email
- Rascunhando documentação técnica
- Criando conteúdo de apresentação
- Escrevendo estudos de caso
- Desenvolvendo esquemas de curso