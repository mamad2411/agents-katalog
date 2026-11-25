---
name: cs-kb-article
description: Redige um artigo para base de conhecimento a partir de um problema resolvido ou pergunta frequente. Use quando a resolução de um ticket vale ser documentada para self-service, a mesma pergunta continua aparecendo, um workaround precisa ser publicado, ou um problema conhecido deve ser comunicado aos clientes. / Draft a knowledge base article from a resolved issue or common question. Use when a ticket resolution is worth documenting for self-service, the same question keeps coming up, a workaround needs to be published, or a known issue should be communicated to customers.
argument-hint: "<problema resolvido ou ticket>"
---

# /cs-kb-article

> Se encontrar integrações não configuradas, verifique [CONNECTORS.md](../../CONNECTORS.md).

Redigir um artigo de base de conhecimento pronto para publicação a partir de um problema de suporte resolvido, pergunta frequente ou workaround documentado. Estrutura o conteúdo para pesquisabilidade e self-service.

## Usage

```
/cs-kb-article <problema resolvido, referência de ticket ou descrição do tópico>
```

Exemplos:
- `/cs-kb-article Como configurar SSO com Okta — resolvi isso para 3 clientes no mês passado`
- `/cs-kb-article Ticket #4521 — cliente não conseguia exportar dados com mais de 10k linhas`
- `/cs-kb-article Pergunta frequente: como configurar notificações via webhook`
- `/cs-kb-article Problema conhecido: gráficos do dashboard não carregam no Safari 16`

## Workflow

### 1. Entender o Material Fonte

Analisar o input para identificar:

- **Qual foi o problema?** O problema original, pergunta ou erro
- **Qual foi a solução?** A resolução, workaround ou resposta
- **Quem é afetado?** Tipo de usuário, nível de plano ou configuração
- **Qual é a frequência?** Problema único ou recorrente
- **Qual tipo de artigo se encaixa melhor?** How-to, troubleshooting, FAQ, problema conhecido ou referência (ver tipos de artigo abaixo)

Se uma referência de ticket for fornecida, buscar o contexto completo:

- **int-evo-crm** (`/int-evo-crm`): Puxar o thread do ticket, resolução e quaisquer notas internas
- **Notion MCP**: Verificar se um artigo similar já existe (atualizar vs. criar novo)
- **int-linear-review** (`/int-linear-review`) ou **Linear MCP**: Verificar se há bug report ou feature request relacionado

### 2. Redigir o Artigo

Usando a estrutura de artigo, padrões de formatação e boas práticas de pesquisabilidade abaixo:

- Seguir o template para o tipo de artigo escolhido (how-to, troubleshooting, FAQ, problema conhecido ou referência)
- Aplicar as boas práticas de pesquisabilidade: título em linguagem do cliente, frase de abertura em linguagem simples, mensagens de erro exatas, sinônimos comuns
- Manter escaneável: headers, passos numerados, parágrafos curtos

### 3. Gerar o Artigo

Apresentar o rascunho com metadados:

```
## Rascunho de Artigo KB

**Título:** [Título do artigo]
**Tipo:** [How-to / Troubleshooting / FAQ / Problema Conhecido / Referência]
**Categoria:** [Área de produto ou tópico]
**Tags:** [Tags pesquisáveis]
**Público:** [Todos os usuários / Admins / Desenvolvedores / Plano específico]

---

[Conteúdo completo do artigo — usando o template apropriado abaixo]

---

### Notas de Publicação
- **Fonte:** [Ticket #, conversa com cliente, ou discussão interna]
- **Artigos existentes para atualizar:** [Se isso tem sobreposição com conteúdo existente]
- **Revisão necessária de:** [SME ou time se precisar verificar precisão técnica]
- **Data de revisão sugerida:** [Quando revisitar para verificar precisão]
```

### 4. Oferecer Próximos Passos

Após gerar o artigo:
- "Quer que eu verifique se um artigo similar já existe no Notion?"
- "Devo ajustar a profundidade técnica para um público diferente?"
- "Quer que eu redija um artigo complementar (ex: um how-to para acompanhar este guia de troubleshooting)?"
- "Devo criar uma versão apenas interna com detalhes técnicos adicionais?"

---

## Estrutura de Artigo e Padrões de Formatação

### Elementos Universais de Artigo

Todo artigo KB deve incluir:

1. **Título**: Claro, pesquisável, descreve o resultado ou problema (não jargão interno)
2. **Overview**: 1-2 frases explicando o que o artigo cobre e para quem é
3. **Corpo**: Conteúdo estruturado adequado ao tipo de artigo
4. **Artigos relacionados**: Links para conteúdo complementar relevante
5. **Metadados**: Categoria, tags, público, data da última atualização

### Regras de Formatação

- **Usar headers (H2, H3)** para dividir o conteúdo em seções escaneáveis
- **Usar listas numeradas** para passos sequenciais
- **Usar listas de bullets** para itens não sequenciais
- **Usar negrito** para nomes de elementos de UI, termos-chave e ênfase
- **Usar blocos de código** para comandos, chamadas de API, mensagens de erro e valores de configuração
- **Usar tabelas** para comparações, opções ou dados de referência
- **Usar callouts/notas** para avisos, dicas e ressalvas importantes
- **Manter parágrafos curtos** — 2-4 frases no máximo
- **Uma ideia por seção** — se uma seção cobre dois tópicos, dividir

## Escrevendo para Pesquisabilidade

Artigos são inúteis se os clientes não conseguem encontrá-los. Otimizar cada artigo para busca:

### Boas Práticas de Título

| Bom Título | Título Ruim | Por quê |
|------------|-----------|-----|
| "Como configurar SSO com Okta" | "Configuração SSO" | Específico, inclui o nome da ferramenta que clientes buscam |
| "Fix: Dashboard mostra página em branco" | "Problema no Dashboard" | Inclui o sintoma que os clientes vivenciam |
| "Rate limits e quotas da API" | "Informações da API" | Inclui os termos específicos que clientes buscam |
| "Erro: 'Connection refused' ao importar dados" | "Problemas de Importação" | Inclui a mensagem de erro exata |

### Otimização de Palavras-Chave

- **Incluir mensagens de erro exatas** — clientes copiam e colam texto de erro na busca
- **Usar linguagem do cliente**, não terminologia interna — "não consigo fazer login" não "falha de autenticação"
- **Incluir sinônimos comuns** — "deletar/remover", "dashboard/página inicial", "exportar/baixar"
- **Adicionar fraseamentos alternativos** — abordar o mesmo problema de ângulos diferentes no overview
- **Taguear por áreas de produto** — garantir que categoria e tags correspondam à forma como clientes pensam sobre o produto

### Fórmula de Frase de Abertura

Começar cada artigo com uma frase que recoloca o problema ou tarefa em linguagem simples:

- **How-to**: "Este guia mostra como [realizar X]."
- **Troubleshooting**: "Se você estiver vendo [sintoma], este artigo explica como corrigir."
- **FAQ**: "[Pergunta nas palavras do cliente]? Aqui está a resposta."
- **Problema conhecido**: "Alguns usuários estão vivenciando [sintoma]. Aqui está o que sabemos e como contornar."

## Templates por Tipo de Artigo

### Artigos How-to

**Objetivo**: Instruções passo a passo para realizar uma tarefa.

**Estrutura**:
```
# Como [realizar tarefa]

[Overview — o que este guia cobre e quando usá-lo]

## Pré-requisitos
- [O que é necessário antes de começar]

## Passos
### 1. [Ação]
[Instrução com detalhes específicos]

### 2. [Ação]
[Instrução]

## Verificar se Funcionou
[Como confirmar o sucesso]

## Problemas Comuns
- [Problema]: [Solução]

## Artigos Relacionados
- [Links]
```

**Boas práticas**:
- Começar cada passo com um verbo
- Incluir o caminho específico: "Vá em Configurações > Integrações > Chaves de API"
- Mencionar o que o usuário deve ver após cada passo ("Você deve ver um banner verde de confirmação")
- Testar os passos você mesmo ou verificar com uma resolução recente de ticket

### Artigos de Troubleshooting

**Objetivo**: Diagnosticar e resolver um problema específico.

**Estrutura**:
```
# [Descrição do problema — o que o usuário vê]

## Sintomas
- [O que o usuário observa]

## Causa
[Por que isso acontece — explicação breve e sem jargão]

## Solução
### Opção 1: [Correção principal]
[Passos]

### Opção 2: [Alternativa se a Opção 1 não funcionar]
[Passos]

## Prevenção
[Como evitar isso no futuro]

## Ainda Com Problemas?
[Como obter ajuda]
```

**Boas práticas**:
- Começar com sintomas, não causas — clientes buscam pelo que veem
- Fornecer múltiplas soluções quando possível (correção mais provável primeiro)
- Incluir uma seção "Ainda com problemas?" que aponta para o suporte
- Se a causa raiz for complexa, manter a explicação voltada ao cliente simples

### Artigos FAQ

**Objetivo**: Resposta rápida a uma pergunta comum.

**Estrutura**:
```
# [Pergunta — nas palavras do cliente]

[Resposta direta — 1-3 frases]

## Detalhes
[Contexto adicional, nuances ou explicação se necessário]

## Perguntas Relacionadas
- [Link para FAQ relacionado]
- [Link para FAQ relacionado]
```

**Boas práticas**:
- Responder a pergunta na primeira frase
- Manter conciso — se a resposta precisa de um passo a passo, é um how-to, não um FAQ
- Agrupar FAQs relacionados e criar links entre eles

### Artigos de Problema Conhecido

**Objetivo**: Documentar um bug conhecido ou limitação com um workaround.

**Estrutura**:
```
# [Problema Conhecido]: [Descrição breve]

**Status:** [Investigando / Workaround Disponível / Correção em Progresso / Resolvido]
**Afetados:** [Quem/o que é afetado]
**Última atualização:** [Data]

## Sintomas
[O que os usuários vivenciam]

## Workaround
[Passos para contornar o problema, ou "Nenhum workaround disponível"]

## Prazo de Correção
[Data prevista de correção ou status atual]

## Atualizações
- [Data]: [Atualização]
```

**Boas práticas**:
- Manter o status atualizado — nada corrói a confiança mais rápido do que um artigo de problema conhecido desatualizado
- Atualizar o artigo quando a correção for lançada e marcar como resolvido
- Se resolvido, manter o artigo ativo por 30 dias para clientes ainda buscando os sintomas antigos

## Cadência de Revisão e Manutenção

Bases de conhecimento decaem sem manutenção. Seguir esse cronograma:

| Atividade | Frequência | Quem |
|----------|-----------|-----|
| **Revisão de novo artigo** | Antes de publicar | Revisão de par + SME para conteúdo técnico |
| **Auditoria de precisão** | Trimestral | Time de suporte revisa artigos de maior tráfego |
| **Verificação de conteúdo obsoleto** | Mensal | Sinalizar artigos não atualizados em 6+ meses |
| **Atualizações de problemas conhecidos** | Semanal | Atualizar status em todos os problemas conhecidos abertos |
| **Revisão de analytics** | Mensal | Verificar quais artigos têm baixas avaliações de utilidade ou altas taxas de rejeição |
| **Análise de gaps** | Trimestral | Identificar principais tópicos de tickets sem artigos KB |

### Ciclo de Vida do Artigo

1. **Rascunho**: Escrito, precisa de revisão
2. **Publicado**: Ativo e disponível para clientes
3. **Precisa de atualização**: Sinalizado para revisão (mudança de produto, feedback ou idade)
4. **Arquivado**: Não mais relevante mas preservado para referência
5. **Retirado**: Removido da base de conhecimento

### Quando Atualizar vs. Criar Novo

**Atualizar existente** quando:
- O produto mudou e os passos precisam ser atualizados
- O artigo está majoritariamente correto mas falta um detalhe
- Feedback indica que clientes estão confusos com uma seção específica
- Um workaround ou solução melhor foi encontrado

**Criar novo** quando:
- Uma nova feature ou área de produto precisa de documentação
- Um ticket resolvido revela um gap — nenhum artigo existe para esse tópico
- O artigo existente cobre muitos tópicos e deve ser dividido
- Um público diferente precisa da mesma informação explicada de forma diferente

## Taxonomia de Links e Categorização

### Estrutura de Categorias

Organizar artigos em uma hierarquia que corresponde à forma como os clientes pensam:

```
Primeiros Passos
├── Configuração de conta
├── Configuração inicial
└── Guias de início rápido

Features e How-tos
├── [Área de feature 1]
├── [Área de feature 2]
└── [Área de feature 3]

Integrações
├── [Integração 1]
├── [Integração 2]
└── Referência de API

Troubleshooting
├── Erros comuns
├── Problemas de performance
└── Problemas conhecidos

Billing e Conta
├── Planos e preços
├── Dúvidas de billing
└── Gerenciamento de conta
```

### Boas Práticas de Links

- **Link de troubleshooting para how-to**: "Para instruções de configuração, veja [Como configurar X]"
- **Link de how-to para troubleshooting**: "Se encontrar erros, veja [Troubleshooting X]"
- **Link de FAQ para artigos detalhados**: "Para um passo a passo completo, veja [Guia de X]"
- **Link de problemas conhecidos para workarounds**: Manter a cadeia do problema para a solução curta
- **Usar links relativos** dentro do KB — sobrevivem melhor a reestruturações do que URLs absolutas
- **Evitar links circulares** — se A linka para B, B não deve linkar de volta para A a menos que ambos sejam pontos de entrada genuinamente úteis

## Boas Práticas de Escrita KB

1. Escrever para o cliente que está frustrado e buscando uma resposta — ser claro, direto e útil
2. Todo artigo deve ser encontrável através de busca usando as palavras que um cliente digitaria
3. Testar seus artigos — seguir os passos você mesmo ou pedir a alguém não familiarizado com o tópico para segui-los
4. Manter artigos focados — um problema, uma solução. Dividir se um artigo estiver crescendo demais
5. Manter agressivamente — um artigo errado é pior que nenhum artigo
6. Rastrear o que está faltando — todo ticket que poderia ter sido um artigo KB é um gap de conteúdo
7. Medir impacto — artigos que não recebem tráfego ou não reduzem tickets precisam ser melhorados ou retirados
