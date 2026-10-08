---
name: generate-docs
description: Gera documentação técnica de APIs e módulos a partir do código-fonte existente. Use quando o usuário pedir README técnico, Javadoc/KDoc, OpenAPI ou atualização de documentação após mudanças de código.
---

# Generate Docs

Use esta skill para criar, revisar e atualizar documentação técnica com consistência editorial.

## Início rápido

1. Identifique módulos, endpoints e contratos públicos impactados.
2. Gere rascunho de README, Javadoc/KDoc e OpenAPI.
3. Valide links, exemplos e consistência de termos.
4. Entregue versão final com changelog resumido.

## Quando usar

- Pedido de documentação de API.
- Atualização de docs após refatoração.
- Criação de README técnico para onboarding.
- Revisão de OpenAPI para publicar em portal interno.

## Workflow

Copie a checklist abaixo e marque o progresso:

```md
Progresso da Tarefa:
- [ ] Etapa 1: Ler código e contratos públicos
- [ ] Etapa 2: Gerar rascunho README/Javadoc/OpenAPI
- [ ] Etapa 3: Validar links e exemplos
- [ ] Etapa 4: Corrigir inconsistências
- [ ] Etapa 5: Entregar versão final
```

## Loop de feedback

1. Execute o validador de documentação.
2. Se falhar, corrija os problemas apontados.
3. Reexecute até passar.
4. Só então finalize.

## Dependências

- mkdocs
- pyyaml
- spectral-cli

## Progressive Disclosure

Para detalhes avançados, consulte arquivos de 1 nível:

- Padrão editorial: [reference/style-guide.md](reference/style-guide.md)
- Regras OpenAPI: [reference/openapi-rules.md](reference/openapi-rules.md)
- Exemplos de entrada/saída: [examples/input-output.md](examples/input-output.md)
- Validação automatizada: `scripts/validate_docs.py`

## Avaliação mínima

Use ao menos 3 cenários de avaliação:

1. Endpoint novo com documentação ausente.
2. Refatoração que altera contrato de resposta.
3. Atualização parcial de README com links quebrados.

Critérios esperados:

- Documentação cobre comportamento e uso.
- Exemplos executáveis e coerentes com API atual.
- Terminologia consistente em todo o material.
- Validação sem erros antes da entrega.
