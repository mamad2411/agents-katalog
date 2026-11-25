---
name: skill-judge
description: Avalie o design de Agent Skills contra especificações oficiais e melhores práticas. Use ao revisar, auditar ou melhorar arquivos SKILL.md e pacotes de skills. Fornece pontuação multidimensional e sugestões de melhoria acionáveis.
---

# Skill Judge

Avalie Agent Skills contra especificações oficiais e padrões derivados de 17+ exemplos oficiais.

---

## Filosofia Central

### O que é uma Skill?

Uma Skill NÃO é um tutorial. Uma Skill é um **mecanismo de externalização de conhecimento**.

O conhecimento tradicional de IA fica trancado em parâmetros do modelo. Para ensinar novas capacidades:
```
Tradicional: Coletar dados → Cluster GPU → Treinar → Implantar nova versão
Custo: $10.000 - $1.000.000+
Prazo: Semanas a meses
```

Skills mudam isso:
```
Skill: Editar SKILL.md → Salvar → Entra em vigor na próxima invocação
Custo: $0
Prazo: Instantâneo
```

Este é o paradigma shift de "treinar IA" para "educar IA" — como um adaptador LoRA hot-swappable que não requer treinamento. Você edita um arquivo Markdown em linguagem natural, e o comportamento do modelo muda.

### A Fórmula Central

> **Skill de Qualidade = Conhecimento Exclusivo de Especialista − O que Claude Já Sabe**

O valor de uma Skill é medido por seu **delta de conhecimento** — a lacuna entre o que ela fornece e o que o modelo já sabe.

- **Conhecimento exclusivo de especialista**: Árvores de decisão, trade-offs, casos extremos, anti-padrões, frameworks de pensamento específicos do domínio — coisas que levam anos de experiência para acumular
- **O que Claude já sabe**: Conceitos básicos, uso de bibliotecas padrão, padrões de programação comuns, boas práticas gerais

Quando uma Skill explica "o que é PDF" ou "como escrever um for-loop", está comprimindo conhecimento que Claude já tem. Este é **desperdício de tokens** — a janela de contexto é um recurso público compartilhado com prompts do sistema, histórico de conversa, outras Skills e requisições do usuário.

### Tool vs Skill

| Conceito | Essência | Função | Exemplo |
|----------|----------|--------|---------|
| **Tool** | O que o modelo PODE fazer | Executar ações | bash, read_file, write_file, WebSearch |
| **Skill** | O que o modelo SABE como fazer | Guiar decisões | Processamento PDF, construção MCP, design frontend |

Tools definem limites de capacidade — sem a tool bash, o modelo não pode executar comandos.
Skills injetam conhecimento — sem a Skill frontend-design, o modelo produz UI genérica.

**A equação**:
```
Agent Geral + Skill Excelente = Agent Especialista em Domínio
```

Mesmo modelo Claude, Skills diferentes carregadas, torna-se especialistas diferentes.

### Três Tipos de Conhecimento em Skills

Ao avaliar, categorize cada seção:

| Tipo | Definição | Tratamento |
|------|-----------|-----------|
| **Especialista** | Claude genuinamente não sabe disso | Deve manter — este é o valor da Skill |
| **Ativação** | Claude sabe mas pode não pensar em | Manter se breve — serve como lembrete |
| **Redundante** | Claude definitivamente sabe disso | Deve deletar — desperdiça tokens |

A arte do design de Skill é maximizar conteúdo de Especialista, usar Ativação com moderação e eliminar Redundante sem piedade.

---

## Dimensões de Avaliação (120 pontos no total)

### D1: Delta de Conhecimento (20 pontos) — A DIMENSÃO CENTRAL

A dimensão mais importante. A Skill adiciona conhecimento genuinamente especialista?

| Pontuação | Critério |
|-----------|----------|
| 0-5 | Explica noções básicas que Claude conhece (o que é X, como escrever código, tutoriais de bibliotecas padrão) |
| 6-10 | Misto: algum conhecimento especialista diluído por conteúdo óbvio |
| 11-15 | Principalmente conhecimento especialista com redundância mínima |
| 16-20 | Puro delta de conhecimento — cada parágrafo justifica seus tokens |

**Sinais de alerta** (pontuação instantânea ≤5):
- Seções "O que é [conceito básico]"
- Tutoriais passo-a-passo para operações padrão
- Explicação de como usar bibliotecas comuns
- Boas práticas genéricas ("escreva código limpo", "trate erros")
- Definições de termos padrão da indústria

**Sinais positivos** (indicadores de alto delta de conhecimento):
- Árvores de decisão para escolhas não óbvias ("quando X falha, tente Y porque Z")
- Trade-offs que apenas um especialista conheceria ("A é mais rápido mas B lida com caso extremo C")
- Casos extremos de experiência real
- "NUNCA faça X porque [razão não óbvia]"
- Frameworks de pensamento específicos do domínio

**Perguntas de avaliação**:
1. Para cada seção, pergunte: "Claude já sabe disso?"
2. Se explicando algo, pergunte: "Isto está explicando PARA Claude ou POR Claude?"
3. Conte parágrafos que são Especialista vs Ativação vs Redundante

---

### D2: Mentalidade + Procedimentos Apropriados (15 pontos)

A Skill transfere **padrões de pensamento** especialista junto com **procedimentos necessários específicos do domínio**?

A diferença entre especialistas e novatos não é "saber como operar" — é "como pensar sobre o problema". Mas padrões de pensamento isolados não são suficientes quando Claude carece de conhecimento procedural específico do domínio.

**Distinção chave**:
| Tipo | Exemplo | Valor |
|------|---------|-------|
| **Padrões de pensamento** | "Antes de projetar, pergunte: O que torna isto memorável?" | Alto — molda tomada de decisão |
| **Procedimentos específicos de domínio** | "Workflow OOXML: desempacotar → editar XML → validar → empacotar" | Alto — Claude pode não saber disso |
| **Procedimentos genéricos** | "Passo 1: Abrir arquivo, Passo 2: Editar, Passo 3: Salvar" | Baixo — Claude já sabe |

| Pontuação | Critério |
|-----------|----------|
| 0-3 | Apenas procedimentos genéricos que Claude já conhece |
| 4-7 | Tem procedimentos de domínio mas faltam frameworks de pensamento |
| 8-11 | Bom equilíbrio: padrões de pensamento + workflows específicos de domínio |
| 12-15 | Nível especialista: molda pensamento E fornece procedimentos que Claude não conheceria |

**O que conta como procedimentos valiosos**:
- Workflows que Claude não foi treinado em (novas ferramentas, sistemas proprietários)
- Ordenação correta que não é óbvia (por exemplo, "validar ANTES de empacotar, não depois")
- Passos críticos fáceis de perder (por exemplo, "DEVE recalcular fórmulas após editar")
- Sequências específicas do domínio (por exemplo, processo de desenvolvimento em 4 fases do servidor MCP)

**O que conta como procedimentos redundantes**:
- Operações genéricas de arquivo (abrir, ler, escrever, salvar)
- Padrões de programação padrão (loops, condicionais, tratamento de erros)
- Uso comum de bibliotecas bem documentadas

**Padrões de pensamento especialista se parecem com**:
```markdown
Antes de [ação], pergunte-se:
- **Propósito**: Que problema isso resolve? Quem o usa?
- **Restrições**: Quais são os requisitos ocultos?
- **Diferenciação**: O que torna esta solução memorável?
```

**Procedimentos valiosos de domínio se parecem com**:
```markdown
### Workflow de Redlining (Claude não saberia essa sequência)
1. Converter para markdown: `pandoc --track-changes=all`
2. Mapear texto para XML: grep para texto em document.xml
3. Implementar mudanças em lotes de 3-10
4. Empacotar e verificar: confirme que TODAS as mudanças foram aplicadas
```

**Procedimentos genéricos redundantes se parecem com**:
```markdown
Passo 1: Abrir o arquivo
Passo 2: Encontrar a seção
Passo 3: Fazer a mudança
Passo 4: Salvar e testar
```

**O teste**:
1. Diz ao Claude O QUE pensar? (padrões de pensamento)
2. Diz ao Claude COMO fazer coisas que não saberia? (procedimentos de domínio)

Uma boa Skill fornece ambos quando necessário.

---

### D3: Qualidade de Anti-Padrões (15 pontos)

A Skill tem listas NUNCA efetivas?

**Por que isso importa**: Metade do conhecimento especialista é saber o que NÃO fazer. Um designer sênior vê gradiente roxo em fundo branco e instintivamente se arrepia — "muito gerado por IA". Esta intuição para "o que absolutamente não fazer" vem de pisar em inúmeras armadilhas.

Claude não pisou nessas armadilhas. Não sabe que a fonte Inter é exagerada, não sabe que gradientes roxos são a assinatura de conteúdo gerado por IA. Skills boas devem declarar explicitamente estes "absolutos nunca".

| Pontuação | Critério |
|-----------|----------|
| 0-3 | Nenhum anti-padrão mencionado |
| 4-7 | Advertências genéricas ("evite erros", "tenha cuidado", "considere casos extremos") |
| 8-11 | Lista NUNCA específica com alguma lógica |
| 12-15 | Anti-padrões de qualidade especialista com PORQUÊ — coisas que apenas experiência ensina |

**Anti-padrões especialistas** (específico + razão):
```markdown
NUNCA use estéticas genéricas geradas por IA como:
- Famílias de fontes exageradas (Inter, Roboto, Arial)
- Esquemas de cores clichês (particularmente gradientes roxos em fundos brancos)
- Layouts e padrões de componentes previsíveis
- Border-radius padrão em tudo
```

**Anti-padrões fracos** (vagos, sem lógica):
```markdown
Evite cometer erros.
Tenha cuidado com casos extremos.
Não escreva código ruim.
```

**O teste**: Um especialista leria a lista de anti-padrões e diria "sim, aprendi isso na prática"? Ou diria "isto é óbvio para todos"?

---

### D4: Conformidade com Especificação — Especialmente Descrição (15 pontos)

A Skill segue os requisitos de formato oficiais? **Foco especial na qualidade da descrição.**

| Pontuação | Critério |
|-----------|----------|
| 0-5 | Frontmatter faltando ou formato inválido |
| 6-10 | Tem frontmatter mas descrição é vaga ou incompleta |
| 11-13 | Frontmatter válido, descrição tem O QUE mas fraco no QUANDO |
| 14-15 | Perfeito: descrição abrangente com O QUE, QUANDO e palavras-chave de disparo |

**Requisitos de frontmatter**:
- `name`: minúsculas, alphanuméricas + hífens apenas, ≤64 caracteres
- `description`: **O CAMPO MAIS CRÍTICO** — determina se a skill é usada

---

**Por que descrição é O CAMPO MAIS IMPORTANTE**:

```
┌─────────────────────────────────────────────────────────────────────┐
│  FLUXO DE ATIVAÇÃO DE SKILL                                         │
│                                                                     │
│  Requisição Usuário → Agent vê TODAS as descrições → Decide qual   │
│                      de skills (apenas descrições,  ativar          │
│                      não corpos!)                                   │
│                                                                     │
│  Se descrição não corresponder → Skill NUNCA é carregada            │
│  Se descrição vaga → Skill pode não disparar quando deveria         │
│  Se descrição sem palavras-chave → Skill é invisível ao Agent      │
└─────────────────────────────────────────────────────────────────────┘
```

**A verdade brutal**: Uma Skill com conteúdo perfeito mas descrição pobre é **inútil** — nunca será ativada. A descrição é a **única chance** de contar ao Agent "use-me nestas situações".

---

**Descrição deve responder TRÊS perguntas**:

1. **O QUE**: O que essa Skill faz? (funcionalidade)
2. **QUANDO**: Em quais situações deve ser usada? (cenários de disparo)
3. **PALAVRAS-CHAVE**: Quais termos devem disparar essa Skill? (termos pesquisáveis)

**Descrição excelente** (todos os três elementos):
```yaml
description: "Criação, edição e análise abrangente de documentos com suporte
para mudanças rastreadas, comentários, preservação de formatação e extração de texto.
Quando Claude precisa trabalhar com documentos profissionais (arquivos .docx) para:
(1) Criar novos documentos, (2) Modificar ou editar conteúdo,
(3) Trabalhar com mudanças rastreadas, (4) Adicionar comentários, ou qualquer outra tarefa de documento"
```

Análise:
- O QUE: criação, edição, análise, mudanças rastreadas, comentários
- QUANDO: "Quando Claude precisa trabalhar com... para: (1)... (2)... (3)..."
- PALAVRAS-CHAVE: arquivos .docx, mudanças rastreadas, documentos profissionais

**Descrição pobre** (elementos faltando):
```yaml
description: "处理文档相关功能"
```

Problemas:
- O QUE: vago ("funcionalidade relacionada a documentos" — especificamente o quê?)
- QUANDO: faltando (quando o Agent deve usar isto?)
- PALAVRAS-CHAVE: faltando (nenhum ".docx", nenhum cenário específico)

**Outro exemplo pobre**:
```yaml
description: "Uma skill útil para várias tarefas"
```

Isto é inútil — Agent não sabe quando ativá-lo.

---

**Checklist de qualidade de descrição**:
- [ ] Lista capacidades específicas (não apenas "ajuda com X")
- [ ] Inclui cenários de disparo explícitos ("Use quando...", "Quando usuário pedir por...")
- [ ] Contém palavras-chave pesquisáveis (extensões de arquivo, termos de domínio, verbos de ação)
- [ ] Específica o suficiente para Agent saber EXATAMENTE quando usar
- [ ] Inclui cenários onde esta skill DEVE ser usada (não apenas "pode ser usada")

---

### D5: Divulgação Progressiva (15 pontos)

A Skill implementa camadas apropriadas de conteúdo?

O carregamento de Skill tem três camadas:
```
Camada 1: Metadados (sempre em memória)
          Apenas name + description
          ~100 tokens por skill

Camada 2: Corpo SKILL.md (carregado após disparo)
          Diretrizes detalhadas, exemplos de código, árvores de decisão
          Ideal: < 500 linhas

Camada 3: Recursos (carregados sob demanda)
          scripts/, references/, assets/
          Sem limite
```

| Pontuação | Critério |
|-----------|----------|
| 0-5 | Tudo despejado em SKILL.md (>500 linhas, sem estrutura) |
| 6-10 | Tem referências mas não é claro quando carregá-las |
| 11-13 | Bom agrupamento com disparadores OBRIGATÓRIOS presentes |
| 14-15 | Perfeito: árvores de decisão + disparadores explícitos + guia "NÃO Carregar" |

**Para Skills COM diretório de referências**, verifique Qualidade de Disparador de Carregamento:

| Qualidade de Disparador | Características |
|------------------------|-----------------|
| Pobre | Referências listadas no final, sem guia de carregamento |
| Medíocre | Alguns disparadores mas não integrados no workflow |
| Bom | Disparadores OBRIGATÓRIOS em etapas de workflow |
| Excelente | Detecção de cenário + disparadores condicionais + "NÃO Carregar" |

**O problema de carregamento**:
```
Carregar muito pouco ◄─────────────────────────────────► Carregar demais
- Referências ficam sem uso                  - Desperdiça espaço de contexto
- Agent não sabe quando carregar             - Informação irrelevante dilui conteúdo-chave
- Conhecimento está lá mas nunca acessado    - Overhead de tokens desnecessário
```

**Bom disparador de carregamento** (integrado ao workflow):
```markdown
### Criando Novo Documento

**OBRIGATÓRIO - LER ARQUIVO INTEIRO**: Antes de proceder, você DEVE ler
[`docx-js.md`](docx-js.md) (~500 linhas) completamente de início a fim.
**NUNCA configure limites de intervalo ao ler este arquivo.**

**NÃO carregar** `ooxml.md` ou `redlining.md` para esta tarefa.
```

**Disparador de carregamento ruim** (apenas listado):
```markdown
## Referências
- docx-js.md - para criar documentos
- ooxml.md - para editar
- redlining.md - para rastrear mudanças
```

**Para Skills simples** (sem referências, <100 linhas): Pontuação baseada em concisão e auto-contenção.

---

### D6: Calibração de Liberdade (15 pontos)

O nível de especificidade é apropriado para a fragilidade da tarefa?

Diferentes tarefas precisam de diferentes níveis de restrição. Isto é sobre combinar liberdade à fragilidade.

| Pontuação | Critério |
|-----------|----------|
| 0-5 | Severamente descombinado (scripts rígidos para tarefas criativas, vago para ops frágeis) |
| 6-10 | Parcialmente apropriado, algumas descombinações |
| 11-13 | Boa calibração para a maioria dos cenários |
| 14-15 | Calibração perfeita de liberdade em todo lugar |

**O espectro de liberdade**:

| Tipo de Tarefa | Deve Ter | Por Quê | Exemplo de Skill |
|----------------|----------|--------|------------------|
| Criativo/Design | Alta liberdade | Múltiplas abordagens válidas, diferenciação é valor | frontend-design |
| Revisão de código | Liberdade média | Princípios existem mas julgamento necessário | code-review |
| Operações de formato de arquivo | Baixa liberdade | Um byte errado corrompe arquivo, consistência crítica | docx, xlsx, pdf |

**Alta liberdade** (instruções baseadas em texto):
```markdown
Comprometa-se com uma direção OUSADA de estética. Escolha um extremo: brutalmente mínimo,
caos maximalista, retro-futurista, natural orgânico...
```

**Liberdade média** (pseudocódigo ou parametrizado):
```markdown
Prioridade de revisão:
1. Vulnerabilidades de segurança (deve corrigir)
2. Erros de lógica (deve corrigir)
3. Problemas de desempenho (deve corrigir)
4. Manutenibilidade (opcional)
```

**Baixa liberdade** (scripts específicos, passos exatos):
```markdown
**OBRIGATÓRIO**: Use script exato em `scripts/create-doc.py`
Parâmetros: --title "X" --author "Y"
NÃO modifique o script.
```

**O teste**: Pergunte "se Agent cometer um erro, qual é a consequência?"
- Consequência alta → Baixa liberdade
- Consequência baixa → Alta liberdade

---

### D7: Reconhecimento de Padrão (10 pontos)

A Skill segue um padrão oficial estabelecido?

Através da análise de 17 Skills oficiais, identificamos 5 padrões de design principais:

| Padrão | ~Linhas | Características Chave | Exemplo | Quando Usar |
|--------|---------|---------------------|---------|------------|
| **Mentalidade** | ~50 | Pensamento > técnica, lista NUNCA forte, alta liberdade | frontend-design | Tarefas criativas exigindo gosto |
| **Navegação** | ~30 | SKILL.md mínimo, roteia para sub-arquivos | internal-comms | Múltiplos cenários distintos |
| **Filosofia** | ~150 | Dois passos: Filosofia → Expressar, enfatiza artesanato | canvas-design | Arte/criação exigindo originalidade |
| **Processo** | ~200 | Workflow em fases, checkpoints, liberdade média | mcp-builder | Projetos complexos multi-etapa |
| **Ferramenta** | ~300 | Árvores de decisão, exemplos de código, baixa liberdade | docx, pdf, xlsx | Operações precisas em formatos específicos |

| Pontuação | Critério |
|-----------|----------|
| 0-3 | Nenhum padrão reconhecível, estrutura caótica |
| 4-6 | Segue parcialmente um padrão com desvios significativos |
| 7-8 | Padrão claro com desvios menores |
| 9-10 | Aplicação magistral de padrão apropriado |

**Guia de seleção de padrão**:

| Características de Sua Tarefa | Padrão Recomendado |
|------------------------------|-------------------|
| Precisa de gosto e criatividade | Mentalidade (~50 linhas) |
| Precisa de originalidade e qualidade de artesanato | Filosofia (~150 linhas) |
| Tem múltiplos sub-cenários distintos | Navegação (~30 linhas) |
| Projeto complexo multi-etapa | Processo (~200 linhas) |
| Operações precisas em formato específico | Ferramenta (~300 linhas) |

---

### D8: Usabilidade Prática (15 pontos)

Um Agent pode realmente usar essa Skill efetivamente?

| Pontuação | Critério |
|-----------|----------|
| 0-5 | Confuso, incompleto, contraditório ou guia não testado |
| 6-10 | Usável mas com lacunas notáveis |
| 11-13 | Guia claro para casos comuns |
| 14-15 | Cobertura abrangente incluindo casos extremos e tratamento de erros |

**Verifique**:
- **Árvores de decisão**: Para cenários multi-caminho, há guia claro sobre qual caminho seguir?
- **Exemplos de código**: Eles realmente funcionam? Ou são pseudocódigo que quebra?
- **Tratamento de erros**: E se a abordagem principal falhar? Há fallbacks?
- **Casos extremos**: Cenários incomuns mas realistas são cobertos?
- **Acionabilidade**: Agent pode agir imediatamente, ou precisa descobrir coisas?

**Boa usabilidade** (árvore de decisão + fallback):
```markdown
| Tarefa | Ferramenta Principal | Fallback | Quando Usar Fallback |
|--------|-------------------|----------|----------------------|
| Ler texto | pdftotext | PyMuPDF | Precisa info de layout |
| Extrair tabelas | camelot-py | tabula-py | camelot falha |

**Problemas comuns**:
- PDF escaneado: pdftotext retorna branco → Use OCR primeiro
- PDF criptografado: Erro de permissão → Use PyMuPDF com senha
```

**Usabilidade pobre** (vago):
```markdown
Use ferramentas apropriadas para processamento PDF.
Trate erros adequadamente.
Considere casos extremos.
```

---

## NUNCA Faça Ao Avaliar

- **NUNCA** dê pontuações altas apenas porque "parece profissional" ou é bem formatado
- **NUNCA** ignore desperdício de tokens — cada parágrafo redundante deve resultar em dedução
- **NUNCA** deixe comprimento impressioná-lo — uma Skill de 43 linhas pode superar uma de 500 linhas
- **NUNCA** pule mentalmente testar as árvores de decisão — elas realmente levam a escolhas corretas?
- **NUNCA** perdoe explicação de noções básicas com "mas fornece contexto útil"
- **NUNCA** ignore listas NUNCA faltando — se não há lista NUNCA, essa é uma lacuna significativa
- **NUNCA** presuma que todos os procedimentos são valiosos — distinga específicos de domínio de genéricos
- **NUNCA** subestime o campo de descrição — descrição pobre = skill nunca é usada
- **NUNCA** coloque informação "quando usar" apenas no corpo — Agent só vê descrição antes de carregar

---

## Protocolo de Avaliação

### Passo 1: Primeira Leitura — Varredura de Delta de Conhecimento

Leia SKILL.md completamente e para cada seção pergunte:
> "Claude já sabe disso?"

Marque cada seção como:
- **[E] Especialista**: Claude genuinamente não sabe disso — agregação de valor
- **[A] Ativação**: Claude sabe mas breve lembrete é útil — aceitável
- **[R] Redundante**: Claude definitivamente sabe disso — deve ser deletado

Calcule proporção aproximada: E:A:R
- Skill boa: >70% Especialista, <20% Ativação, <10% Redundante
- Skill medíocre: 40-70% Especialista, Ativação alta
- Skill ruim: <40% Especialista, Redundante alta

### Passo 2: Análise de Estrutura

```
[ ] Verifique validade de frontmatter
[ ] Conte linhas totais em SKILL.md
[ ] Liste todos arquivos de referência e seus tamanhos
[ ] Identifique qual padrão a Skill segue
[ ] Verifique disparadores de carregamento (se referências existem)
```

### Passo 3: Pontue Cada Dimensão

Para cada uma das 8 dimensões:
1. Encontre evidência específica (cite linhas relevantes)
2. Atribua pontuação com justificativa de uma linha
3. Note melhorias específicas se pontuação < máximo

### Passo 4: Calcule Total e Nota

```
Total = D1 + D2 + D3 + D4 + D5 + D6 + D7 + D8
Máximo = 120 pontos
```

**Escala de Nota** (baseada em percentual):
| Nota | Percentual | Significado |
|------|-----------|-----------|
| A | 90%+ (108+) | Excelente — Skill especialista pronta para produção |
| B | 80-89% (96-107) | Bom — pequenas melhorias necessárias |
| C | 70-79% (84-95) | Adequado — caminho claro de melhoria |
| D | 60-69% (72-83) | Abaixo da Média — problemas significativos |
| F | <60% (<72) | Pobre — precisa redesenho fundamental |

### Passo 5: Gere Relatório

```markdown
# Relatório de Avaliação de Skill: [Nome da Skill]

## Resumo
- **Pontuação Total**: X/120 (X%)
- **Nota**: [A/B/C/D/F]
- **Padrão**: [Mentalidade/Navegação/Filosofia/Processo/Ferramenta]
- **Proporção de Conhecimento**: E:A:R = X:Y:Z
- **Veredicto**: [Avaliação em uma sentença]

## Pontuações por Dimensão

| Dimensão | Pontuação | Máximo | Notas |
|----------|-----------|--------|-------|
| D1: Delta de Conhecimento | X | 20 | |
| D2: Mentalidade vs Mecânica | X | 15 | |
| D3: Qualidade de Anti-Padrão | X | 15 | |
| D4: Conformidade de Especificação | X | 15 | |
| D5: Divulgação Progressiva | X | 15 | |
| D6: Calibração de Liberdade | X | 15 | |
| D7: Reconhecimento de Padrão | X | 10 | |
| D8: Usabilidade Prática | X | 15 | |

## Problemas Críticos
[Liste problemas que devem ser corrigidos e impactam significativamente a efetividade da Skill]

## Top 3 Melhorias
1. [Melhoria de maior impacto