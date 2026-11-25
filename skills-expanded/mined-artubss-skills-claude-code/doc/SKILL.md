---
name: "doc"
description: "Use quando a tarefa envolver leitura, criação ou edição de documentos `.docx`, especialmente quando a fidelidade de formatação ou layout é importante; prefira `python-docx` mais o `scripts/render_docx.py` incluído para verificações visuais."
author: openai
---


# Habilidade DOCX

## Quando usar
- Ler ou revisar conteúdo DOCX onde o layout importa (tabelas, diagramas, paginação).
- Criar ou editar arquivos DOCX com formatação profissional.
- Validar layout visual antes da entrega.

## Fluxo de trabalho
1. Prefira revisão visual (layout, tabelas, diagramas).
   - Se `soffice` e `pdftoppm` estiverem disponíveis, converta DOCX → PDF → PNGs.
   - Ou use `scripts/render_docx.py` (requer `pdf2image` e Poppler).
   - Se essas ferramentas faltarem, instale-as ou peça ao usuário para revisar as páginas renderizadas localmente.
2. Use `python-docx` para edições e criação estruturada (títulos, estilos, tabelas, listas).
3. Após cada mudança significativa, re-renderize e inspecione as páginas.
4. Se a revisão visual não for possível, extraia texto com `python-docx` como fallback e avise sobre risco de layout.
5. Mantenha outputs intermediários organizados e limpe após aprovação final.

## Convenções de temp e output
- Use `tmp/docs/` para arquivos intermediários; delete ao terminar.
- Escreva artefatos finais em `output/doc/` quando trabalhar neste repositório.
- Mantenha nomes de arquivo estáveis e descritivos.

## Dependências (instale se faltarem)
Prefira `uv` para gerenciamento de dependências.

Pacotes Python:
```
uv pip install python-docx pdf2image
```
Se `uv` não estiver disponível:
```
python3 -m pip install python-docx pdf2image
```
Ferramentas do sistema (para renderização):
```
# macOS (Homebrew)
brew install libreoffice poppler

# Ubuntu/Debian
sudo apt-get install -y libreoffice poppler-utils
```

Se a instalação não for possível neste ambiente, informe ao usuário qual dependência está faltando e como instalá-la localmente.

## Ambiente
Nenhuma variável de ambiente obrigatória.

## Comandos de renderização
DOCX → PDF:
```
soffice -env:UserInstallation=file:///tmp/lo_profile_$$ --headless --convert-to pdf --outdir $OUTDIR $INPUT_DOCX
```

PDF → PNGs:
```
pdftoppm -png $OUTDIR/$BASENAME.pdf $OUTDIR/$BASENAME
```

Helper incluído:
```
python3 scripts/render_docx.py /path/to/file.docx --output_dir /tmp/docx_pages
```

## Expectativas de qualidade
- Entregue um documento pronto para cliente: tipografia consistente, espaçamento, margens e hierarquia clara.
- Evite defeitos de formatação: texto cortado/sobreposto, tabelas quebradas, caracteres ilegíveis ou styling de template padrão.
- Gráficos, tabelas e visuais devem ser legíveis nas páginas renderizadas com alinhamento correto.
- Use apenas hífens ASCII. Evite U+2011 (hífen não-quebrável) e outros dashes Unicode.
- Citações e referências devem ser legíveis por humanos; nunca deixe tokens de ferramenta ou strings de placeholder.

## Verificações finais
- Re-renderize e inspecione cada página em zoom 100% antes da entrega final.
- Corrija qualquer problema de espaçamento, alinhamento ou paginação e repita o loop de renderização.
- Confirme que não há resquícios (arquivos temporários, renderizações duplicadas), a menos que o usuário peça para mantê-los.