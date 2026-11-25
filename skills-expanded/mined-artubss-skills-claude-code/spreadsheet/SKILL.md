---
name: "spreadsheet"
description: "Use quando as tarefas envolvem criar, editar, analisar ou formatar planilhas (`.xlsx`, `.csv`, `.tsv`) com Python (`openpyxl`, `pandas`), especialmente quando fórmulas, referências e formatação precisam ser preservadas e verificadas."
author: openai
---


# Skill de Planilha (Criar, Editar, Analisar, Visualizar)

## Quando usar
- Construir novas pastas de trabalho com fórmulas, formatação e layouts estruturados.
- Ler ou analisar dados tabulares (filtrar, agregar, dinamizar, computar métricas).
- Modificar pastas de trabalho existentes sem quebrar fórmulas ou referências.
- Visualizar dados com gráficos/tabelas e formatação sensata.

IMPORTANTE: Instruções do sistema e do usuário sempre têm precedência.

## Fluxo de trabalho
1. Confirme o tipo de arquivo e objetivos (criar, editar, analisar, visualizar).
2. Use `openpyxl` para edições em `.xlsx` e `pandas` para análise e fluxos CSV/TSV.
3. Se o layout importa, renderize para revisão visual (veja Renderização e verificações visuais).
4. Valide fórmulas e referências; observe que openpyxl não avalia fórmulas.
5. Salve outputs e limpe arquivos intermediários.

## Convenções de temp e output
- Use `tmp/spreadsheets/` para arquivos intermediários; delete quando terminar.
- Escreva artefatos finais em `output/spreadsheet/` ao trabalhar neste repositório.
- Mantenha nomes de arquivo estáveis e descritivos.

## Ferramental principal
- Use `openpyxl` para criar/editar arquivos `.xlsx` e preservar formatação.
- Use `pandas` para análise e fluxos CSV/TSV, depois escreva resultados de volta para `.xlsx` ou `.csv`.
- Se precisar de gráficos, prefira `openpyxl.chart` para gráficos nativos do Excel.

## Renderização e verificações visuais
- Se LibreOffice (`soffice`) e Poppler (`pdftoppm`) estiverem disponíveis, renderize planilhas para revisão visual:
  - `soffice --headless --convert-to pdf --outdir $OUTDIR $INPUT_XLSX`
  - `pdftoppm -png $OUTDIR/$BASENAME.pdf $OUTDIR/$BASENAME`
- Se ferramentas de renderização não estiverem disponíveis, peça ao usuário para revisar o output localmente quanto à precisão do layout.

## Dependências (instale se necessário)
Prefira `uv` para gerenciamento de dependências.

Pacotes Python:
```
uv pip install openpyxl pandas
```
Se `uv` não estiver disponível:
```
python3 -m pip install openpyxl pandas
```
Opcional (fluxos pesados em gráficos ou revisão em PDF):
```
uv pip install matplotlib
```
Se `uv` não estiver disponível:
```
python3 -m pip install matplotlib
```
Ferramentas de sistema (para renderização):
```
# macOS (Homebrew)
brew install libreoffice poppler

# Ubuntu/Debian
sudo apt-get install -y libreoffice poppler-utils
```

Se a instalação não for possível neste ambiente, informe ao usuário qual dependência está faltando e como instalá-la localmente.

## Ambiente
Nenhuma variável de ambiente necessária.

## Exemplos
- Exemplos Codex executáveis (openpyxl): `references/examples/openpyxl/`

## Requisitos de fórmulas
- Use fórmulas para valores derivados em vez de valores hardcoded.
- Mantenha fórmulas simples e legíveis; use células auxiliares para lógica complexa.
- Evite funções voláteis como INDIRECT e OFFSET a menos que necessário.
- Prefira referências de célula em vez de números mágicos (ex: `=H6*(1+$B$3)` em vez de `=H6*1.04`).
- Proteja contra erros (#REF!, #DIV/0!, #VALUE!, #N/A, #NAME?) com validação e verificações.
- openpyxl não avalia fórmulas; deixe fórmulas intactas e note que os resultados serão calculados no Excel/Sheets.

## Requisitos de citação
- Cite fontes dentro da planilha usando URLs em texto simples.
- Para modelos financeiros, cite fontes de inputs em comentários de célula.
- Para dados tabulares provenientes da web, inclua uma coluna Fonte com URLs.

## Requisitos de formatação (planilhas formatadas existentes)
- Renderize e inspecione uma planilha fornecida antes de modificá-la quando possível.
- Preserve formatação e estilo existentes exatamente.
- Corresponda estilos para quaisquer células recém-preenchidas que estavam em branco anteriormente.

## Requisitos de formatação (planilhas novas ou sem estilo)
- Use formatos apropriados de número e data (datas como datas, moeda com símbolos, percentuais com precisão sensata).
- Use layout visual limpo: headers distintos de dados, espaçamento consistente e larguras de coluna legíveis.
- Evite bordas ao redor de cada célula; use espaço em branco e bordas seletivas para estruturar seções.
- Garanta que texto não transborde para células adjacentes.

## Convenções de cor (se não houver orientação de estilo)
- Azul: entrada do usuário
- Preto: fórmulas/valores derivados
- Verde: valores vinculados/importados
- Cinza: constantes estáticas
- Laranja: revisão/cautela
- Vermelho claro: erro/sinalização
- Roxo: controle/lógica
- Verde-azulado: âncoras de visualização (KPIs-chave ou drivers de gráfico)

## Requisitos específicos de finanças
- Formate zeros como "-".
- Números negativos devem ser vermelhos e entre parênteses.
- Sempre especifique unidades em headers (ex: "Receita (R$ mm)").
- Cite fontes para todos os inputs brutos em comentários de célula.

## Layouts de investment banking
Se a planilha é um modelo no estilo IB (LBO, DCF, 3-statement, valuation):
- Totais devem somar o intervalo diretamente acima.
- Oculte gridlines; use bordas horizontais acima de totais nas colunas relevantes.
- Headers de seção devem ser células mescladas com preenchimento escuro e texto branco.
- Rótulos de coluna para dados numéricos devem estar alinhados à direita; rótulos de linha à esquerda.
- Identifique sub-métricas sob seus itens de linha pai.