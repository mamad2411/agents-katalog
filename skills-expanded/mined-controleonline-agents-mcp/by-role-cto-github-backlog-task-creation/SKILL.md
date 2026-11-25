# GitHub Backlog Task Creation

## Overview

Use esta skill quando o CTO receber uma solicitacao explicita para transformar URLs, telas ou escopos de produto em tarefas tecnicas no GitHub e organiza-las no backlog do ProjectV2.

Se a solicitacao chegar sem task, esta skill deve ser disparada primeiro: o CTO cria uma ou mais issues conforme o escopo independente e so depois libera a execucao.

## Ownership

Esta e uma atribuicao direta do CTO apenas para intake e estruturacao de trabalho, e tambem a porta obrigatoria de entrada quando ainda nao existir task:

- converter cada tela ou escopo independente em uma issue tecnica
- identificar o repositorio correto com evidencia do codigo, rota ou produto
- adicionar a issue ao ProjectV2 solicitado e posiciona-la em `Ready`
- deixar a execucao da tarefa para o agent responsavel pelo desenvolvimento

A criacao da tarefa nao autoriza o CTO a implementar o produto no lugar do Developer.

## Workflow

1. leia a solicitacao completa e separe os escopos independentes
2. confirme o repositorio de cada tarefa por busca de rota, componente, modulo ou documentacao; nao presuma o repositorio apenas pelo dominio
3. pesquise issues e PRs abertas ou fechadas pelo nome da tela, rota e objetivo para evitar duplicacao
4. quando ja houver acompanhamento equivalente, atualize ou referencie o item existente em vez de criar duplicata
5. crie exatamente uma issue para cada tela ou escopo independente solicitado
6. use titulo orientado a resultado, sem depender apenas do nome tecnico da rota
7. escreva o corpo com contexto, URL de referencia, objetivo tecnico, requisitos, criterios de aceite e observacoes de escopo
8. preserve os filtros, acoes, paginacao, ordenacao, estados de carregamento, vazio e erro existentes quando a tarefa envolver migracao de listagem
9. exija reutilizacao de componentes padrao existentes quando o solicitante indicar um componente como `defaultTable` ou `defaultUpload`
10. nao invente API, entidade, campo, label ou comportamento que nao tenha sido confirmado; registre pontos que dependem de descoberta tecnica
11. aplique uma unica label de tipo a cada issue nova: `bug`, `enhancement` ou `feature`
12. **label de página (obrigatória quando identificável):** se o relato/solicitação informar URL ou tela, ou se for possível identificar a página, aplique na issue uma label com o slug da página
    - extrair da URL o path principal (ex.: `https://staging.controleonline.com/client-details?clientId=15&...` → label `client-details`)
    - se não houver URL, inferir pelo texto (“tela de detalhes do cliente”, “My Companies”, rota conhecida)
    - formato: kebab-case; **sem** domínio, query string, hash ou IDs numéricos
    - uma label de página por issue (página principal do erro/escopo)
    - se a label ainda não existir no repositório, **criá-la**
    - ausência de página identificável não bloqueia a criação; registre no corpo que a página não foi determinada
13. nunca atribua assignee
14. **hands-on obrigatorio:** adicione cada issue ao ProjectV2 indicado (Project #1 da org) e defina o campo de status como `Ready` (ou coluna coerente); falha de associacao deve ser comentada na issue e nao e aceitavel como “feito”
15. confirme por leitura final a URL da issue, o repositorio, a associacao ao projeto, o tipo, a label de página (quando aplicável) e o status real no board
16. ao concluir, entregue uma lista curta com cada tarefa criada ou reutilizada, seu link e confirmacao de que esta no Project #1

## Issue Template

```markdown
## Tipo de demanda

[bug | enhancement | feature]

## Contexto

[Problema atual, tela afetada e URL de referencia.]

## Objetivo tecnico

[Resultado esperado e componente/padrao que deve ser reutilizado.]

## Requisitos

- [Comportamentos obrigatorios.]
- [Compatibilidade e preservacao funcional.]
- [Descobertas tecnicas que devem ser realizadas durante a implementacao.]

## Criterios de aceite

- [Resultado observavel.]
- [Estados e interacoes relevantes.]
- [Validacao de regressao.]

## Fora de escopo

[Limites conhecidos, quando necessarios.]
```

## DefaultTable Guidance

Para migracao de listagem para `defaultTable`, a issue deve pedir explicitamente:

- substituir a implementacao especifica da listagem pelo componente padrao do projeto
- manter colunas, dados, filtros, busca, ordenacao, paginacao e acoes que forem aplicaveis na tela atual
- manter navegacao, permissoes e integracoes existentes
- cobrir estados de carregamento, vazio e erro
- remover codigo sem uso
- validar responsividade e ausencia de regressao nos fluxos da tela

## Quality Bar

- nao criar uma issue agregada quando o pedido exigir uma tarefa por tela
- nao criar duplicata sem pesquisar o historico
- nao deixar issue apenas com URL e uma frase generica
- nao deixar task nova sem label de tipo
- nao deixar task nova com URL/tela identificável sem a label de página correspondente
- nao declarar que o item esta no backlog sem confirmar a mutacao no ProjectV2
- nao usar assignee como ownership
- nao fechar issues; fechamento continua pertencendo apenas a humanos
