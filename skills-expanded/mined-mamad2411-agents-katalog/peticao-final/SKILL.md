---
name: peticao-final
description: "Use para gerar, adaptar ou revisar para protocolo peticoes juridicas brasileiras completas (.docx), incluindo inicial, replica, recursos, embargos, cumprimento de sentenca e incidentes. Acione quando houver documentos do caso e necessidade de minuta final com fatos comprovados, fundamentos verificados e jurisprudencia real, preferencialmente STJ/TJBA."
---

# Peticao Final

Produzir peticoes juridicas brasileiras completas, personalizadas e prontas para revisao final, sempre com lastro documental, fundamentos conferidos e arquivo `.docx` no padrao do escritorio.

## Contrato

- Entregar peca final apenas quando houver base segura para tipo de peca, fase, partes, fatos essenciais, documentos, pedidos, valor da causa e prazo/competencia quando aplicaveis.
- Separar internamente `fato -> prova -> fundamento -> pedido`; nao compensar lacuna probatoria com retorica.
- Em fundamentos juridicos, nao abrir topico ou subtitulo sem fechar com pedido/providencia concreta; unir teses quando elas levarem ao mesmo pedido.
- Nunca inventar fatos, documentos, datas, valores, numeros de processo, qualificacoes, protocolos, julgados, sumulas ou temas.
- Nao citar jurisprudencia sem verificacao em fonte oficial ou base confiavel conferida no momento da tarefa. Se nao puder verificar, nao inserir na peca final.
- Priorizar o estilo do acervo do usuario, pesquisando exemplos recentes na ordem `2026 > 2025 > 2024 > 2023`.
- Tratar `completa` como completa em adequacao, nao em extensao: o modelo mais proximo do acervo e teto de estrutura, tamanho, numero de topicos, pedidos e citacoes.
- Nao criar topicos, pedidos subsidiarios, jurisprudencia, alineas ou fundamentacao abstrata quando os modelos equivalentes forem enxutos e a tese puder ser fechada em poucos paragrafos.
- Gerar `.docx` como saida padrao para peca final; texto no chat serve apenas para resumo, pendencias ou previa quando o usuario pedir.

## Fluxo

1. Identificar tipo de peca, objetivo processual, fase, rito, juizo/tribunal, partes, prazo, decisao atacada e pedidos pretendidos.
2. Ler a pasta do caso: PDFs, imagens, DOCX, mensagens, planilhas e textos. Usar OCR ou leitura visual quando a prova estiver em imagem.
3. Montar quadro interno de fatos, provas, inferencias, lacunas e riscos. Parar e pedir dados se faltar elemento essencial.
4. Buscar no acervo exemplos do mesmo tipo de peca e tema, sempre preferindo arquivos mais novos. Antes de redigir, escolher o modelo mais proximo e espelhar sua extensao, estrutura e densidade argumentativa, salvo necessidade concreta do caso.
5. Pesquisar fundamentos legais e jurisprudencia necessaria em fonte atual; usar STJ e TJBA antes de outros tribunais quando forem pertinentes.
6. Redigir a peca com estrutura adequada e estilo do escritorio.
7. Criar o `.docx` a partir de `assets/modelo-peticao.docx` ou gerar novo template com `scripts/build_template_docx.py`, preservando logo, rodape, hifenizacao e espacamentos padrao.
8. Auditar o arquivo com `scripts/audit_template_docx.py`; quando estiver entregando um `.docx`, renderizar e revisar visualmente com a skill `documents`.

## Referencias

Leia somente o necessario:

- `references/estilo-e-estrutura.md`: voz, ritmo, aberturas, titulos, pedidos e assinatura.
- `references/pecas-processuais.md`: estrutura por tipo de peca.
- `references/provas-e-documentos.md`: leitura da pasta do caso e mapa probatorio.
- `references/jurisprudencia-e-fundamentos.md`: pesquisa juridica sem alucinacao.
- `references/docx-e-checklist.md`: formatacao Word e checklist final.
- `references/sintese-cerebro.md`: sintese atualizada pelo script do acervo, quando existir.

## Scripts

- `scripts/build_template_docx.py`: gera `assets/modelo-peticao.docx` com A4, Helvetica, margens, logo, rodape, hifenizacao, estilos, espacamentos e assinatura padrao.
- `scripts/audit_template_docx.py`: confere as regras formais do template `.docx`, inclusive logo, rodape e hifenizacao.
- `scripts/mapear_cerebro_peticoes.py`: atualiza `references/sintese-cerebro.md` a partir do acervo em Markdown.
- `scripts/extrair_documentos_caso.py`: inventaria uma pasta do caso e gera um Markdown compacto com texto extraido de PDFs, imagens, DOCX e textos, usando OCR quando necessario.

## Ferramentas Locais Preferidas

- `rg`/`pdfgrep`: localizar termos sem carregar arquivos inteiros no contexto.
- `pdftotext`/`pdfinfo` (Poppler): extrair texto de PDFs pesquisaveis.
- `ocrmypdf` + `tesseract -l por+eng`: OCR de PDFs ou imagens escaneadas.
- `qpdf`/`ghostscript`: reparar, normalizar ou comprimir PDFs quando isso ajudar a leitura.
- `soffice` + Poppler: renderizar `.docx` para verificacao visual antes da entrega.

## Regras De Parada

Antes de redigir a versao final, parar e listar exatamente o que falta quando nao houver:

- identificacao minima das partes ou legitimidade aparente;
- juizo/tribunal, rito, fase ou via processual minimamente definidos;
- decisao atacada, prazo ou tempestividade em peca recursal;
- fatos essenciais e documentos minimos;
- pedido principal executavel;
- valor da causa ou criterio seguro de calculo;
- fonte segura para jurisprudencia que seja decisiva.

Se o usuario pedir rascunho apesar da lacuna, marcar expressamente como rascunho interno e nao apresentar como peca pronta para protocolo.

## Diretriz GPT-5.5

Em tarefas longas e documentais, explicitar para si o resultado esperado, os criterios de sucesso, as regras de evidencia, os limites do que pode ser inferido e o formato final. Usar raciocinio mais profundo para leitura de autos, prova, estrategia, fundamentacao e revisao final; usar respostas mais curtas apenas para status e pendencias. Esta orientacao segue as paginas oficiais da OpenAI sobre latest model, prompt guidance e reasoning models.
