---
name: tuck-bit-pt
description: "TuckBit é uma habilidade portátil para agentes de programação. Ajuda a selecionar o contexto, as ferramentas e as verificações certas sem comprometer a correção."
license: MIT
compatibility: Portable Agent Skills; project-scoped install only.
metadata:
  author: TuckBit contributors
  version: "0.4.0"
  locale: pt
---

# TuckBit — Português

> O núcleo da habilidade está traduzido; as referências técnicas permanecem temporariamente em inglês e precisam de revisão da comunidade.

Otimize resultados corretos e verificados por recurso utilizado, não apenas a contagem de tokens.

Quatro recursos padrão: registro, contexto, verificação e orçamento. Orquestração e métricas são opcionais.

## Método de trabalho

Comece pelo pedido exato do usuário, pelas instruções disponíveis e pelas ferramentas autorizadas. Preserve restrições, aprovações e verificações obrigatórias.

1. Defina o resultado, os limites, os riscos e quando parar; evite planos extensos para tarefas simples.
2. Encontre o código, a documentação e as ferramentas mais relevantes e específicas; amplie apenas quando necessário.
3. Prefira a descoberta nativa de ferramentas; metadados são sugestões, nunca autorização para executar.
4. Use um agente em tarefas pequenas; distribua trabalhos independentes somente com responsabilidades e critérios claros.
5. Execute testes específicos e, depois, todas as verificações obrigatórias na revisão final.
6. Entregue um resumo verificável de alterações, testes, riscos e bloqueios. Use checkpoints e evite consultas repetitivas.

## Carregue apenas a referência relevante

- `references/task-contract.md` — task contracts / host instructions.
- `references/workflows.md` — Fast / Standard / Deep workflows.
- `references/registry.md` — discovery and permission limits.
- `references/context.md` — source-linked evidence and checkpoints.
- `references/verification.md` — tests and integration checks.
- `references/budget.md` — bounded iterations.
- `references/orchestration.md` — optional independent agents.
- `references/metrics.md` — optional evaluation.

## Limites obrigatórios

Não pule verificações de segurança, reduza a correção, invente resultados, leia credenciais nem ignore aprovações. O ambiente hospedeiro controla as permissões.

**Prévia para desenvolvedores. Instalar não comprova ativação real nem economia de tokens.**
