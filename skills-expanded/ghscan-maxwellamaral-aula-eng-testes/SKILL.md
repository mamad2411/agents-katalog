---
name: revisar-material-didatico
description: Revisa materiais didáticos existentes deste repositório, como uma Aula, um Laboratório ou um par, avaliando clareza, legibilidade, coerência pedagógica e prontidão para uso. Use quando o usuário pedir revisão, diagnóstico ou verificação de material já criado; por padrão, apenas analisar e relatar, editando somente quando houver pedido explícito para corrigir, aplicar, atualizar ou implementar ajustes.
---

# Revisar material didático

Identificar problemas reais e melhorias úteis sem promover reescrita infinita ou alterações por preferência estilística.

## Definir o modo

- Por padrão: analisar, relatar e não alterar arquivos.
- Editar somente quando o usuário pedir explicitamente para corrigir, aplicar, atualizar ou implementar ajustes.

## Consultar as fontes

1. Ler `AGENTS.md`.
2. Consultar, conforme o material revisado:
   - `specs/projeto-pedagogico.md`;
   - `specs/padrao-aula.md`;
   - `specs/padrao-laboratorio.md`;
   - `specs/estrutura-site.md`;
   - página anterior relacionada;
   - página seguinte relacionada, quando existir;
   - materiais técnicos relacionados, quando existirem.

Tratar o pedido específico como definição do escopo da revisão. Não converter decisões revisáveis observadas nos materiais em regras permanentes.

## Avaliar

### Correção conceitual e progressão

- Verificar conceitos, exemplos, simplificações excessivas e afirmações absolutas.
- Confirmar que o material depende apenas de conhecimentos já introduzidos e não antecipa conteúdo sem necessidade.
- Avaliar se o conceito nasce de um problema compreensível, se a Aula prepara o Laboratório e se o Laboratório sustenta o passo seguinte.

### Escopo e legibilidade

- Avaliar se falta aprofundamento ou se há conteúdo excessivo.
- Confirmar que Python e as ferramentas apoiam o objetivo de VVTS sem tomar o protagonismo.
- Verificar parágrafos, listas, títulos, perguntas, código e admonitions conforme as specs.
- Sinalizar paredes de texto, redundâncias e destaques sem função semântica.

### Requisitos e experimentos

Em laboratórios, conferir especialmente:

- clareza sobre o que deve acontecer;
- dados e estados iniciais definidos;
- resultados observáveis;
- informações suficientes para execução;
- valores de previsão determinados;
- critérios de conclusão alinhados à atividade;
- roteiro autossuficiente sem prescrição desnecessária da implementação.

Quando houver experimento, verificar se a previsão é possível e determinada, a operação está especificada e o resultado permite comparação e evidencia o conceito pretendido. Não aceitar como observável um valor que apenas é retornado, mas nunca armazenado ou apresentado.

### Python, ferramentas e Quarto

- Verificar se somente recursos Python e ferramentas necessários foram introduzidos e se “Python e ferramentas em foco” permanece curto e contextualizado.
- Conferir coerência temporal com os materiais técnicos relacionados, inclusive referências ao que seria ensinado futuramente.
- Identificar detalhes de planejamento interno sem utilidade para compreender, executar, verificar, aprofundar ou entregar.
- Conferir YAML, Quarto Markdown, callouts, listas, código, links relativos e ausência de customizações desnecessárias.

## Classificar os achados

Classificar cada achado relevante:

- **NECESSÁRIO:** erro conceitual, ambiguidade real, requisito inexequível, inconsistência ou problema relevante;
- **RECOMENDADO:** melhoria clara de aprendizagem, clareza ou legibilidade;
- **OPCIONAL:** preferência editorial com benefício pequeno;
- **NÃO ALTERAR:** trecho avaliado e considerado adequado.

Priorizar itens necessários e recomendados. Evitar listas extensas de opcionais. Não propor mudança apenas porque outra redação também seria possível. Quando o material estiver bom, afirmá-lo claramente.

## Relatar

Apresentar relatório conciso com:

1. avaliação geral;
2. problemas necessários;
3. melhorias recomendadas;
4. opcionais somente quando realmente úteis;
5. aspectos que devem permanecer como estão;
6. conclusão: precisa de nova rodada, pronto após ajustes pontuais ou pronto para uso.

Ao revisar Aula e Laboratório juntos, incluir coerência entre ambos, continuidade com o par anterior e ponte para o próximo passo.

## Aplicar ajustes quando solicitado

1. Modificar somente os pontos solicitados ou aprovados.
2. Evitar reestruturações não pedidas e preservar alterações preexistentes do usuário.
3. Executar `uv run quarto render` ou `quarto render` e corrigir erros.
4. Verificar `git diff` e `git status`.
5. Relatar arquivos alterados e resultado do build.

Não fazer commit ou push sem solicitação explícita.
