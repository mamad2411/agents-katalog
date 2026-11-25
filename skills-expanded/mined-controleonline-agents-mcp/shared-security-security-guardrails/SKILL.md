# Security Guardrails Skill

## Objetivo

Definir a barra minima de seguranca editorial e operacional para todos os agents do ecossistema `ControleOnline`.

Esta skill protege contra vazamento de:

- credenciais
- tokens
- cookies
- chaves
- dados pessoais
- dados comerciais sensiveis
- links internos ou privados
- stack traces e logs com informacao sensivel

## Regra central

Nenhum agent deve expor informacao sensivel em:

- wiki publica
- tutorial para cliente
- comentarios de issue
- comentarios de PR
- logs
- screenshots
- exemplos de payload
- arquivos de apoio publicados

Se a entrega depender de dados sensiveis para ser explicada, o agent deve sanitizar o material ou devolver a tarefa com bloqueio objetivo.

## Requisitos obrigatorios

- screenshots e capturas visuais devem ser sanitizados antes de qualquer publicacao
- toda imagem usada em documentacao publica deve esconder dados reais e segredos
- URLs publicas devem ser exibidas apenas se forem realmente publicas e apropriadas para o cliente
- tarefas de documentacao que precisem de imagem devem usar evidencias visuais geradas para o proprio fluxo, nao prints crus de issue ou chat
- se um artefato mostrar dado real, ele deve ser refeito ou mascarado antes da publicacao
- nomes de clientes, emails, telefones, documentos, tokens e headers sensiveis nao devem ir para conteudo publico
- o agente deve parar e pedir bloqueio objetivo se nao conseguir publicar sem expor informacao sensivel

## Uso por papel

- todos os agents leem esta skill
- `Documentor` / `Tutorial Assistant` / `Technical Documenter` a usam com prioridade maxima ao escrever material publico
- `Developer` e `Quality Assurance` a usam quando capturas, prints ou evidencias visuais forem geradas em suporte a uma entrega

## Documentacao publica

- texto publico deve descrever o que o usuario faz, nao o que o time alterou internamente
- diagramas e capturas devem ser explicados sem expor implementacao sensivel
- qualquer exemplo com dados ficticios deve deixar claro que e ficticio
- conteudo da wiki deve poder ser lido por cliente final sem revelar o fluxo interno de desenvolvimento
