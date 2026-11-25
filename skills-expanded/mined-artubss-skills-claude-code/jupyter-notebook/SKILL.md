---
name: "jupyter-notebook"
description: "Use when the user asks to create, scaffold, or edit Jupyter notebooks (`.ipynb`) for experiments, explorations, or tutorials; prefer the bundled templates and run the helper script `new_notebook.py` to generate a clean starting notebook."
author: openai
---


# Habilidade Jupyter Notebook

Crie notebooks Jupyter limpos e reproduzíveis para dois modos primários:

- Experimentos e análise exploratória
- Tutoriais e guias orientados ao ensino

Prefira os templates bundled e o script helper para consistência estrutural e menos erros JSON.

## Quando usar
- Criar um novo notebook `.ipynb` do zero.
- Converter notas brutas ou scripts em um notebook estruturado.
- Refatorar um notebook existente para ser mais reproduzível e fácil de revisar.
- Construir experimentos ou tutoriais que serão lidos ou re-executados por outras pessoas.

## Árvore de decisão
- Se o pedido é exploratório, analítico ou orientado por hipótese, escolha `experiment`.
- Se o pedido é instrucional, passo a passo ou específico para audiência, escolha `tutorial`.
- Se estiver editando um notebook existente, trate como refatoração: preserve a intenção e melhore a estrutura.

## Caminho da habilidade (configurar uma vez)

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export JUPYTER_NOTEBOOK_CLI="$CODEX_HOME/skills/jupyter-notebook/scripts/new_notebook.py"
```

Skills de escopo do usuário são instaladas em `$CODEX_HOME/skills` (padrão: `~/.codex/skills`).

## Fluxo de trabalho
1. Defina a intenção.
Identifique o tipo de notebook: `experiment` ou `tutorial`.
Capture o objetivo, audiência e o que "pronto" significa.

2. Escafold a partir do template.
Use o script helper para evitar criar manualmente JSON raw do notebook.

```bash
uv run --python 3.12 python "$JUPYTER_NOTEBOOK_CLI" \
  --kind experiment \
  --title "Compare prompt variants" \
  --out output/jupyter-notebook/compare-prompt-variants.ipynb
```

```bash
uv run --python 3.12 python "$JUPYTER_NOTEBOOK_CLI" \
  --kind tutorial \
  --title "Intro to embeddings" \
  --out output/jupyter-notebook/intro-to-embeddings.ipynb
```

3. Preencha o notebook com passos pequenos e executáveis.
Mantenha cada célula de código focada em um passo.
Adicione células markdown curtas que expliquem o propósito e resultado esperado.
Evite outputs grandes e ruidosos quando um resumo curto é suficiente.

4. Aplique o padrão correto.
Para experimentos, siga `references/experiment-patterns.md`.
Para tutoriais, siga `references/tutorial-patterns.md`.

5. Edite com segurança ao trabalhar com notebooks existentes.
Preserve a estrutura do notebook; evite reordenar células a menos que melhore a história de cima para baixo.
Prefira edições direcionadas a reescritas completas.
Se precisar editar JSON raw, revise `references/notebook-structure.md` primeiro.

6. Valide o resultado.
Execute o notebook de cima para baixo quando o ambiente permitir.
Se a execução não for possível, diga explicitamente e indique como validar localmente.
Use a checklist de avaliação final em `references/quality-checklist.md`.

## Templates e script helper
- Templates ficam em `assets/experiment-template.ipynb` e `assets/tutorial-template.ipynb`.
- O script helper carrega um template, atualiza a célula de título e escreve um notebook.

Caminho do script:
- `$JUPYTER_NOTEBOOK_CLI` (instalação padrão: `$CODEX_HOME/skills/jupyter-notebook/scripts/new_notebook.py`)

## Convenções de temp e output
- Use `tmp/jupyter-notebook/` para arquivos intermediários; delete quando terminar.
- Escreva artefatos finais em `output/jupyter-notebook/` ao trabalhar neste repo.
- Use nomes de arquivo estáveis e descritivos (por exemplo, `ablation-temperature.ipynb`).

## Dependências (instale apenas quando necessário)
Prefira `uv` para gerenciamento de dependências.

Pacotes Python opcionais para execução local do notebook:

```bash
uv pip install jupyterlab ipykernel
```

O script scaffold bundled usa apenas a biblioteca padrão Python e não requer dependências extras.

## Ambiente
Nenhuma variável de ambiente obrigatória.

## Mapa de referência
- `references/experiment-patterns.md`: estrutura e heurísticas de experimentos.
- `references/tutorial-patterns.md`: estrutura de tutorial e fluxo de ensino.
- `references/notebook-structure.md`: formato JSON do notebook e regras de edição segura.
- `references/quality-checklist.md`: checklist de validação final.